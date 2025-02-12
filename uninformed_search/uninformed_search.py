########
# Lights out puzzle game
# The Lights Out puzzle consists of an m × n grid of lights, each of which has two states: on and off.
# The goal of the puzzle is to turn all the lights off, with the caveat that whenever a light is toggled, its
# neighbors above, below, to the left, and to the right will be toggled as well. If a light along the edge
# of the board is toggled, then fewer than four other lights will be affected, as the missing neighbors
# will be ignored.
########
from collections import deque
import random
import copy


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.COLS = len(board[0])  # dimension of columns
        self.ROWS = len(board)  # dimension of rows

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        """
        toggles light located at given row and column
        as well as neighbors

        Args:
            row (int): row coordinate
            col (int): column coordinate
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.board[row][col] = not self.board[row][col]  # toggle the cell
        for dr, dc in directions:
            if 0 <= dr + row < self.ROWS and 0 <= dc + col < self.COLS:
                self.board[dr + row][dc +
                                     col] = not self.board[dr + row][dc + col]

    def scramble(self):
        """
        performing moves with 0.5 probability for each cell
        """
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        """
        returns True if all lights on board are off

        """
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col]:
                    return False
        return True

    def copy(self):
        """
        create deep copy of puzzle
        """
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # need to create new deep copy puzzle
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield (row, col), new_puzzle

    def find_solution(self):
        """
        find_solution BFS search 

        Returns:
            optimal moves (list)
        """
        initial_state = tuple(tuple(row) for row in self.board)
        queue = deque()
        queue.append((initial_state, []))
        visited = set()
        visited.add(initial_state)
        while queue:
            curr_state, path = queue.popleft()
            # if all cells are turned off
            if all(not cell for row in curr_state for cell in row):
                return path
            curr_puzzle = LightsOutPuzzle([list(row) for row in curr_state])
            # call successors to et all possible next states (boards)
            # check if it's the solved state
            for move, new_puzzle in curr_puzzle.successors():
                new_state = tuple(tuple(row) for row in new_puzzle.get_board())
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [move]))
        return None  # no sol found


def create_puzzle(rows, cols):
    board = [[False] * cols for _ in range(rows)]
    return LightsOutPuzzle(board)
