# 8 Puzzle Solver

A clean and fast Python implementation of the 8-puzzle solver using:

- Uniform Cost Search (UCS)
- A* with Misplaced Tiles heuristic
- A* with Manhattan Distance heuristic

## What was improved

- Replaced expensive `deepcopy`-based state expansion with immutable tuple states.
- Replaced linear queue scans with a heap-based priority queue (`heapq`).
- Added robust input validation and solvability checking.
- Removed global mutable search state for safer, cleaner logic.
- Added clear code comments and improved output metrics.

## Requirements

- Python 3.8+

## Run

```bash
python3 main.py
```

Then enter 3 rows of the puzzle using comma-separated values, for example:

```text
Numbers in row 0: 1,2,3
Numbers in row 1: 4,0,6
Numbers in row 2: 7,5,8
```

Choose the algorithm:

```text
1. Uniform Cost Search
2. A* with Misplaced Tile Heuristic
3. A* with Manhattan Distance Heuristic
```

## Notes

- Use `0` for the blank tile.
- The program validates that numbers `0..8` are each used exactly once.
- The program checks solvability before searching.

## Output Metrics

For each run, the solver prints:

- Whether the goal was reached
- Number of moves in the solution
- Move sequence
- Nodes expanded
- Maximum queue size
- Runtime in seconds
