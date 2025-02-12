########
# The Eight Puzzle consists of a 3 × 3 board of sliding tiles with a single empty space.
# For each configuration, the only possible moves are to swap the empty tile with one of its
# neighboring tiles. The goal state for the puzzle consists of tiles 1-3 in the top
#  row, tiles 4-6 in the middle row, and tiles 7 and 8 in the bottom row,
#  with the empty space in the lower-right corner.
########
import random
import copy
from queue import PriorityQueue
import math


def create_tile_puzzle(rows, cols):

    board = [[0] * cols for _ in range(rows)]
    num = 1
    for row in range(rows):
        for col in range(cols):
            board[row][col] = num
            num += 1
    board[-1][-1] = 0  # last cell is empty
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.COLS = len(board[0])
        self.ROWS = len(board)
        # initial position of empty tile
        self.empty_position = (self.ROWS - 1, self.COLS - 1)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == 0:
                    self.empty_position = (row, col)
                    break

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        row_empty, col_empty = self.empty_position

        if direction == "up":
            if 0 <= row_empty - 1 < self.ROWS:
                self.board[row_empty][col_empty],\
                self.board[row_empty - 1][col_empty]\
                = self.board[row_empty - 1][col_empty],\
                    self.board[row_empty][col_empty]
                self.empty_position = (row_empty - 1, col_empty)
                return True

        elif direction == "down":
            if 0 <= row_empty + 1 < self.ROWS:
                self.board[row_empty][col_empty],\
                     self.board[row_empty + 1][col_empty]\
                     = self.board[row_empty + 1][col_empty],\
                    self.board[row_empty][col_empty]
                self.empty_position = (row_empty + 1, col_empty)
                return True

        elif direction == "right":
            if 0 <= col_empty + 1 < self.COLS:
                self.board[row_empty][col_empty],\
                     self.board[row_empty][col_empty + 1]\
                     = self.board[row_empty][col_empty + 1],\
                    self.board[row_empty][col_empty]
                self.empty_position = (row_empty, col_empty + 1)
                return True

        elif direction == "left":
            if 0 <= col_empty - 1 < self.COLS:
                self.board[row_empty][col_empty],\
                     self.board[row_empty][col_empty - 1]\
                     = self.board[row_empty][col_empty - 1],\
                    self.board[row_empty][col_empty]
                self.empty_position = (row_empty, col_empty - 1)
                return True

        return False

    def scramble(self, num_moves):

        moves = ["up", "down", "left", "right"]

        for _ in range(num_moves):
            move = random.choice(moves)
            while not self.perform_move(move):
                move = random.choice(moves)

    def is_solved(self):
        num = 1
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if i == self.ROWS - 1 and j == self.COLS - 1:
                    return self.board[i][j] == 0
                if self.board[i][j] != num:
                    return False
                num += 1
        return True

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        moves = ["up", "down", "left", "right"]
        row_empty, col_empty = self.empty_position
        move_deltas = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        for move in moves:
            dr, dc = move_deltas[move]
            new_row, new_col = row_empty + dr, col_empty + dc
            if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
                # shallow copy of each row to create new board
                new_board = [row[:] for row in self.board]
                new_board[row_empty][col_empty], new_board[new_row][new_col] = \
                new_board[new_row][new_col], new_board[row_empty][col_empty]

                yield (move, TilePuzzle(new_board))

    # Required
    def _reverse_move(self, move):
        reverse_move = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        return reverse_move[move]

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
            return

        if len(moves) >= limit:
            return

        for move, new_puzzle in self.successors():
            if moves and move == self._reverse_move(moves[-1]):
                continue
            yield from new_puzzle.iddfs_helper(limit, moves + [move])

    def find_solutions_iddfs(self):
        """
        IDDFS search
        Iterative deepening depth-first search to find all optimal solutions
        """
        limit = 0
        found_solution = False

        while not found_solution:
            solutions = list(self.iddfs_helper(limit, []))
            if solutions:
                found_solution = True
                for solution in solutions:
                    yield solution
            limit += 1

    # Required
    def manhattan_dist(self, board):
        """Calculate Manhattan distance heuristic for the given board"""
        dist = 0
        for row in range(self.ROWS):
            for col in range(self.COLS):
                val = board[row][col]
                if val != 0:  # Skip the empty tile
                    goal_row, goal_col = divmod(val - 1, self.COLS)
                    dist += abs(row - goal_row) + abs(col - goal_col)
        return dist

    def __lt__(self, other):
        """PriorityQueue comparison, 
        less than
        self.manhattan_dist(self.board) < other.manhattan_dist(other.board)
        """
        return False

    def find_solution_a_star(self):
        """A* search using Manhattan distance heuristic"""
        frontier = PriorityQueue()
        visited = set()

        # Initial state
        start_puzzle = self.copy()
        # <f, g, move, puzzle> -> initial f = g+h = 0+h = h
        frontier.put((self.manhattan_dist(self.board), 0, [], start_puzzle))
        visited.add(tuple(map(tuple, self.board)))

        while not frontier.empty():
            _, g, moves, curr_puzzle = frontier.get()

            if curr_puzzle.is_solved():
                return moves

            for move, next_puzzle in curr_puzzle.successors():
                board_tuple = tuple(tuple(row) for row in next_puzzle.board)

                if board_tuple not in visited:
                    visited.add(board_tuple)
                    g_new = g + 1
                    h_new = self.manhattan_dist(next_puzzle.board)
                    f_new = g_new + h_new
                    frontier.put((f_new, g_new, moves + [move], next_puzzle))

        return None
