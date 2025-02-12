###########
# develop an AI for a game in which two players take turns placing 1 × 2
# dominoes on a rectangular grid. One player must always place his dominoes vertically, and the other
# must always place his dominoes horizontally. The last player who successfully places a domino on the
# board wins.
# As with the Tile Puzzle, an infrastructure that is compatible with the provided GUI has been
# suggested. However, only the search method will be tested, so you are free to choose a different
# approach if you find it more convenient to do so.
# The representation used for this puzzle is a two-dimensional list of Boolean values, where True
# corresponds to a filled square and False corresponds to an empty square.

###########
import collections
import copy
import itertools
import random
import math


def create_dominoes_game(rows, cols):
    board = [[False for _ in range(cols)] for _ in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0

    def get_board(self):
        return self.board

    def reset(self):
        pass

    def is_legal_move(self, row, col, vertical):
        """
        Check if placing a domino at the given position is legal.
        Args:
            row: start row
            col: start col
            vertical: if true place vertically (down); else place horizontally (right)
        Returns:
            Boolean: if the move is legal
        """
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return False

        if vertical:
            # Vertical domino: (row,col) and (row+1, col)
            if row + 1 >= self.rows:
                return False
            return not (self.board[row][col] or self.board[row + 1][col])
        else:
            # Horizontal domino: (row,col) and (row, col+1)
            if col + 1 >= self.cols:
                return False
            return not (self.board[row][col] or self.board[row][col + 1])

    def legal_moves(self, vertical):
        row_limit = self.rows - 1 if vertical else self.rows
        col_limit = self.cols if vertical else self.cols - 1

        for row in range(row_limit):
            for col in range(col_limit):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row + 1][col] = True
        else:
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        # find at least one legal move
        for _ in self.legal_moves(vertical):
            return False
        return True

    def copy(self):
        board_copy = copy.deepcopy(self.board)
        return DominoesGame(board_copy)

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(move[0], move[1], vertical)
            yield (move, new_game)

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        """
        Find the best move for the current player using alpha-beta search.
        Args:
            vertical: If True, generate vertical moves; if False, generate horizontal moves
            limit: Maximum depth to search
        Returns:
            ((row, col), value, nodes_visited): Best move coordinates, its value, and nodes visited
        """

        def count_moves(game, is_vertical):
            return sum(1 for _ in game.legal_moves(is_vertical))

        def evaluate(game, is_vertical):
            # Value = current_player_moves - opponent_moves
            return count_moves(game, is_vertical) - count_moves(
                game, not is_vertical)

        nodes_visited = [0]  # List to allow modification in nested functions

        def max_value(game, is_vertical, depth, alpha, beta):
            if depth == 0 or game.game_over(is_vertical):
                nodes_visited[0] += 1
                return evaluate(game, is_vertical), None

            v = float('-inf')
            best_move = None

            for move, next_state in game.successors(is_vertical):
                min_val, _ = min_value(next_state, not is_vertical, depth - 1,
                                       alpha, beta)
                if min_val > v:
                    v = min_val
                    best_move = move
                alpha = max(alpha, v)
                if v >= beta:
                    break
            return v, best_move

        def min_value(game, is_vertical, depth, alpha, beta):
            if depth == 0 or game.game_over(is_vertical):
                nodes_visited[0] += 1
                return -evaluate(
                    game,
                    is_vertical), None  # Negate evaluation for min player

            v = float('inf')
            best_move = None

            for move, next_state in game.successors(is_vertical):
                max_val, _ = max_value(next_state, not is_vertical, depth - 1,
                                       alpha, beta)
                if max_val < v:
                    v = max_val
                    best_move = move
                beta = min(beta, v)
                if v <= alpha:
                    break
            return v, best_move

        # Start alpha-beta search
        value, move = max_value(self, vertical, limit, float('-inf'),
                                float('inf'))
        return (move, value, nodes_visited[0])
