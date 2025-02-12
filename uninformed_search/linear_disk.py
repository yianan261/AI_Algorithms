########
#The starting configuration of this puzzle is a row of ℓ cells, with disks located on cells 0 through n − 1.
# The goal is to move the disks to the end of the row using a constrained set of actions. At each step, a
# disk can only be moved to an adjacent empty cell, or to an empty cell two spaces away if another
# disk is located on the intervening square. Given these restrictions, it can be seen that in many cases,
# no movements will be possible for the majority of the disks. For example, from the starting position,
# the only two options are to move the last disk from cell n − 1 to cell n, or to move the second-to-last
# disk from cell n − 2 to cell n.
########
from collections import deque


def solve_identical_disks(length, n):
    """
    Breadth first graph search solution (uninformed search)

    Args:
        length (int): length of cells
        n (int): number of disks

    Returns:
        List: list of optimal moves
    """
    # 1: disk, 0: empty
    # intial state: disks in first n cells
    start = [1] * n + [0] * (length - n)
    # goal: disks in last n cells
    goal = [0] * (length - n) + [1] * n
    queue = deque([(start, [])])  # <state, moves: List[(start,end)]>
    visited = set()

    def neighbors(state):
        # generate all valid moves from curr state
        moves = []
        for i in range(length):
            if state[i] == 1:
                if i + 1 < length and state[i + 1] == 0:
                    new_state = state[:]
                    new_state[i] = 0
                    new_state[i + 1] = 1  # move disk
                    moves.append((new_state, (i, i + 1)))  # <start,end>
                # jump over another disk
                if i + 2 < length and state[i + 1] == 1:
                    if state[i + 2] == 0:
                        new_state = state[:]
                        new_state[i] = 0
                        new_state[i + 2] = 1
                        moves.append((new_state, (i, i + 2)))
        return moves

    while queue:
        curr_state, curr_moves = queue.popleft()
        if curr_state == goal:
            return curr_moves
        state = tuple(curr_state)
        if state not in visited:
            visited.add(state)
            for new_state, move in neighbors(curr_state):
                queue.append((new_state, curr_moves + [move]))
    return []  # no solution


def solve_distinct_disks(length, n):
    start = list(range(1, n + 1)) + [0] * (length - n)
    goal = [0] * (length - n) + list(range(n, 0, -1))

    queue = deque([(start, [])])  # <state:List[int], moves: List[<start,end>])
    visited = set()

    def neighbors(state):
        moves = []
        for i in range(length):
            if state[i] != 0:  # disk at position i
                if i + 1 < length and state[i + 1] == 0:
                    new_state = state[:]
                    new_state[i], new_state[i + 1] = new_state[i +
                                                               1], new_state[i]
                    moves.append((new_state, (i, i + 1)))
                if i + 2 < length and state[i + 1] != 0 and state[i + 2] == 0:
                    new_state = state[:]
                    new_state[i], new_state[i + 2] = new_state[i +
                                                               2], new_state[i]
                    moves.append((new_state, (i, i + 2)))
                if i - 1 >= 0 and state[i - 1] == 0:
                    new_state = state[:]
                    new_state[i], new_state[i - 1] = new_state[i -
                                                               1], new_state[i]
                    moves.append((new_state, (i, i - 1)))
                if i - 2 >= 0 and state[i - 1] != 0 and state[i - 2] == 0:
                    new_state = state[:]
                    new_state[i], new_state[i - 2] = new_state[i -
                                                               2], new_state[i]
                    moves.append((new_state, (i, i - 2)))
        return moves

    while queue:
        curr_state, curr_moves = queue.popleft()

        if curr_state == goal:
            return curr_moves

        state_tuple = tuple(curr_state)
        if state_tuple not in visited:
            visited.add(state_tuple)
            for new_state, move in neighbors(curr_state):
                queue.append((new_state, curr_moves + [move]))

    return []
