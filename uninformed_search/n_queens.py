########
# Solver for the n-queens problem, wherein n queens are to be placed
# on an n × n chessboard so that no pair of queens can attack each other. In chess, a queen
# can attack any piece that lies in the same row, column, or diagonal as itself.
########

import math


def num_placements_all(n):
    """
    returns number of ways to place n queens on nxn board

    Args:
        n (int): dimension of n
    """
    return math.comb(n * n, n)


def num_placements_one_per_row(n):
    """
    returns number of ways to place n queens on nxn board
    each row contains one queen

    Args:
        n (int): dimension n
    """
    return n**n


def n_queens_valid(board):
    """
    index represents row
    value represents column
    configuration is valid if no two queens in the same column and diagonal
    return True if valid False if not

    Args:
        board (List[int]): represent board configuration
    """
    n = len(board)
    for i in range(n):  # iterate through each queen
        for j in range(i + 1, n):  # compare with queens after curr queen
            # checks if two queens are in the same column
            if board[i] == board[j]:
                return False
            if abs(i - j) == abs(board[i] - board[j]):
                return False
    return True


def n_queens_solutions(n):

    def n_queens_helper(board):
        """
        helper to recursively generate valid n-queens placement

        Args:
            n (int)
            board (List[int])
        """
        if len(board) == n:
            yield board
            return

        for col in range(n):
            new_board = board + [col]
            if n_queens_valid(new_board):
                yield from n_queens_helper(new_board)

    return list(n_queens_helper([]))
