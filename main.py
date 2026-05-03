import heapq
import time
from itertools import count

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GOAL_POSITIONS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE)}


def format_state(state):
    """Return a readable 3x3 grid string for a flattened puzzle state."""
    rows = [state[i : i + 3] for i in range(0, 9, 3)]
    return "\n".join(str(list(row)) for row in rows)


def parse_puzzle_input():
    """Read and validate a 3x3 puzzle from interactive user input."""
    print("Use 0 for the blank tile and commas between values (example: 1,2,3).")
    values = []

    for row_index in range(3):
        row = input(f"Numbers in row {row_index}: ").strip().split(",")
        if len(row) != 3:
            raise ValueError("Each row must contain exactly 3 comma-separated values.")

        try:
            row_values = [int(value.strip()) for value in row]
        except ValueError as exc:
            raise ValueError("All entries must be integers.") from exc

        values.extend(row_values)

    if set(values) != set(range(9)):
        raise ValueError("Puzzle must contain each number from 0 to 8 exactly once.")

    return tuple(values)


def is_solvable(state):
    """For a 3x3 puzzle, a state is solvable when inversion count is even."""
    numbers = [value for value in state if value != 0]
    inversions = 0

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1

    return inversions % 2 == 0


def misplaced_tiles(state):
    """Heuristic: count tiles that are not in the goal position (excluding blank)."""
    return sum(1 for index, value in enumerate(state) if value and value != GOAL_STATE[index])


def manhattan_distance(state):
    """Heuristic: sum of Manhattan distances from each tile to its goal position."""
    distance = 0

    for index, value in enumerate(state):
        if value == 0:
            continue

        row, col = divmod(index, 3)
        goal_row, goal_col = GOAL_POSITIONS[value]
        distance += abs(row - goal_row) + abs(col - goal_col)

    return distance


def neighbors(state):
    """Generate neighbor states reachable by moving the blank one step."""
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    moves = []

    if row > 0:
        moves.append((-3, "up"))
    if row < 2:
        moves.append((3, "down"))
    if col > 0:
        moves.append((-1, "left"))
    if col < 2:
        moves.append((1, "right"))

    for offset, move in moves:
        swap_index = zero_index + offset
        new_state = list(state)
        new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
        yield tuple(new_state), move


def reconstruct_moves(came_from, goal):
    """Rebuild the solution path as a list of move names from start to goal."""
    moves = []
    current = goal

    while current in came_from:
        previous, move = came_from[current]
        moves.append(move)
        current = previous

    moves.reverse()
    return moves


def choose_heuristic(algo):
    """Map CLI algorithm choice to the heuristic function used in search."""
    if algo == 1:
        return lambda _state: 0  # Uniform Cost Search
    if algo == 2:
        return misplaced_tiles
    if algo == 3:
        return manhattan_distance

    raise ValueError("Invalid algorithm choice. Pick 1, 2, or 3.")


def general_search(initial_state, algo, verbose=False):
    """Run UCS/A* and return search metrics plus the move sequence if solved."""
    heuristic = choose_heuristic(algo)
    frontier = []
    tie_breaker = count()

    start_h = heuristic(initial_state)
    heapq.heappush(frontier, (start_h, 0, next(tie_breaker), initial_state))

    g_score = {initial_state: 0}
    closed = set()
    came_from = {}
    max_queue_size = 1
    expanded_nodes = 0

    while frontier:
        max_queue_size = max(max_queue_size, len(frontier))
        f_score, depth, _, state = heapq.heappop(frontier)

        if state in closed:
            continue

        if verbose:
            print(f"Expanding state [g(n)={depth}, h(n)={f_score - depth}]")
            print(format_state(state))
            print()

        if state == GOAL_STATE:
            return {
                "solved": True,
                "moves": reconstruct_moves(came_from, state),
                "depth": depth,
                "expanded": expanded_nodes,
                "max_queue": max_queue_size,
            }

        closed.add(state)
        expanded_nodes += 1

        for next_state, move in neighbors(state):
            if next_state in closed:
                continue

            candidate_depth = depth + 1
            if candidate_depth >= g_score.get(next_state, float("inf")):
                continue

            g_score[next_state] = candidate_depth
            came_from[next_state] = (state, move)
            next_f = candidate_depth + heuristic(next_state)
            heapq.heappush(frontier, (next_f, candidate_depth, next(tie_breaker), next_state))

    return {
        "solved": False,
        "moves": [],
        "depth": -1,
        "expanded": expanded_nodes,
        "max_queue": max_queue_size,
    }


def main():
    try:
        initial_state = parse_puzzle_input()
    except ValueError as error:
        print(f"Input error: {error}")
        return

    if not is_solvable(initial_state):
        print("This puzzle configuration is not solvable.")
        return

    print(
        "Choice of algorithm:\n"
        "1. Uniform Cost Search\n"
        "2. A* with Misplaced Tile Heuristic\n"
        "3. A* with Manhattan Distance Heuristic"
    )

    try:
        algo = int(input("Enter 1, 2, or 3: ").strip())
    except ValueError:
        print("Algorithm choice must be an integer.")
        return

    start = time.time()
    result = general_search(initial_state, algo)
    duration = time.time() - start

    print("Initial state:")
    print(format_state(initial_state))
    print()

    if result["solved"]:
        print("Goal state reached.")
        print(f"Moves to solution: {len(result['moves'])}")
        print(f"Move sequence: {' -> '.join(result['moves']) if result['moves'] else '(already solved)'}")
    else:
        print("No solution found.")

    print(f"Nodes expanded: {result['expanded']}")
    print(f"Max queue size: {result['max_queue']}")
    print(f"Runtime (seconds): {duration:.6f}")


if __name__ == "__main__":
    main()
