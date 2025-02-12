def solve_distinct_disks(length, n):
    """
    Solve disks puzzle using A* search (distinct disks).
    -1 represents an empty cell.
    """

    def get_next_states(config):
        """Generate possible next states from the current configuration."""
        next_states = []
        for i in range(length):
            if config[i] != -1:
                # Move to adjacent cells
                for next_pos in [i - 1, i + 1]:
                    if 0 <= next_pos < length and config[next_pos] == -1:
                        new_config = list(config)
                        new_config[next_pos], new_config[i] = new_config[
                            i], new_config[next_pos]
                        next_states.append(new_config)

                # Jump over a disk
                for jump_pos in [i - 2, i + 2]:
                    if 0 <= jump_pos < length and config[jump_pos] == -1:
                        middle_pos = (i + jump_pos) // 2
                        if config[middle_pos] != -1:
                            new_config = list(config)
                            new_config[jump_pos], new_config[i] = new_config[
                                i], new_config[jump_pos]
                            next_states.append(new_config)
        return next_states

    def heuristic(config):
        """
        Heuristic cost for the configuration.
        Sum of the minimum number of moves each disk needs to reach its goal position.
        """
        total_cost = 0
        for pos, disk in enumerate(config):
            if disk != -1:
                goal_pos = length - 1 - disk  # Goal position for the disk
                dist = abs(goal_pos - pos)
                # Each move can cover up to 2 cells, so divide by 2
                total_cost += (dist + 1) // 2
        return total_cost

    # Initial setup
    initial_config = [-1] * length
    for i in range(n):
        initial_config[i] = i

    # Goal state
    goal_config = [-1] * length
    for i in range(n):
        goal_config[length - 1 - i] = i

    # Priority queue: (f_score, g_score, config, path)
    frontier = PriorityQueue()
    frontier.put(
        (heuristic(initial_config), 0, initial_config, [initial_config]))

    # Track the best g_score for each state
    g_scores = {tuple(initial_config): 0}

    while not frontier.empty():
        _, moves, current_config, path = frontier.get()

        if current_config == goal_config:
            return path

        if tuple(current_config) in g_scores and moves > g_scores[tuple(
                current_config)]:
            continue

        for next_config in get_next_states(current_config):
            next_g_score = moves + 1
            # found better path
            if tuple(next_config) not in g_scores or next_g_score < g_scores[
                    tuple(next_config)]:
                g_scores[tuple(next_config)] = next_g_score
                f_score = next_g_score + heuristic(next_config)
                frontier.put(
                    (f_score, next_g_score, next_config, path + [next_config]))
