# EED461: Design and Analysis of Algorithms (2026/2027)

Ain Shams University — Faculty of Engineering  
Computer Engineering and Software Systems Program

Python implementation of the EED461 group project tasks, each using its assigned algorithmic technique.

## Repository Structure

```text
Algorithm/
├── main.py                       # CLI demo runner for implemented tasks
├── tasks/
│   ├── __init__.py
│   ├── task1_coin_removal.py     # Task 1 - Coin Removal (Greedy)
│   ├── task2_domino_tiling.py    # Task 2 - Domino Tiling (Brute Force)
│   └── task5_round_table.py      # Task 5 - King Arthur's Round Table (Dynamic Programming)
└── tests/
    ├── __init__.py
    ├── test_task1.py             # Unit tests for Task 1
    ├── test_task2.py             # Unit tests for Task 2
    └── test_task5.py             # Unit tests for Task 5
```

## Implemented Tasks

### Task 1 — Coin Removal (`Greedy`)
- **Function:** `removeCoins(n: int, coins: Sequence[str]) -> tuple[bool, list[int]]`
- **File:** `tasks/task1_coin_removal.py`
- **Characterization:** A non-empty line of coins can be completely cleared **if and only if** the number of heads-up (`'H'`) coins is **odd** (an empty line `n == 0` is trivially cleared in `0` moves).
- **Greedy Strategy:** Scan left to right for the leftmost `'H'` at index `i`. Remove `i`, flip `i + 1` (if present), and immediately cascade leftward to remove `i - 1, i - 2, ..., left` (each flipped from `'T'` to `'H'` by the previous removal). Advance `left = i + 1` and repeat.
- **Complexity:**
  - Time: `O(n)`
  - Space: `O(n)`

### Task 2 — Domino Tiling (`Brute Force`)
- **Function:** `tileDominoes(n: int, missing1: tuple[int, int], missing2: tuple[int, int]) -> tuple[bool, list[tuple[tuple[int, int], tuple[int, int]]]]`
- **File:** `tasks/task2_domino_tiling.py`
- **Assumptions:**
  - `2 <= n <= 8` with 0-based `(row, col)` coordinates and `missing1 != missing2`.
  - Each domino in the returned list is represented as a pair of adjacent cell coordinates `((r1, c1), (r2, c2))`.
- **Brute Force Strategy:** First check that the remaining black and white square counts are equal (odd `n` leaves `n^2 - 2` odd squares, so no tiling exists). Then exhaustively search placements via recursive backtracking in row-major order: at the first uncovered square `(r, c)`, try placing a horizontal domino `(r, c)-(r, c+1)` and, if that fails, backtrack and try a vertical domino `(r, c)-(r+1, c)`.
- **Complexity:**
  - Time: `O(2^(n^2 / 2))` worst-case
  - Space: `O(n^2)`

### Task 5 — King Arthur's Round Table (`Dynamic Programming`)
- **Function:** `seatKnights(n: int, friends: list[list[bool]]) -> list[int]`
- **File:** `tasks/task5_round_table.py`
- **Graph-Theoretic Characterization:**
  - Finding a valid circular seating where adjacent knights are friends is equivalent to finding a **Hamiltonian Cycle** in the undirected friendship graph $G = (V, E)$.
  - **Dirac's Theorem (1952):** In any simple undirected graph with $n \ge 3$ vertices, if every vertex has degree $\ge n / 2$, the graph contains a Hamiltonian cycle. Under this condition, a valid circular seating is guaranteed to exist.
- **Dynamic Programming Strategy:**
  - Uses the **Bellman-Held-Karp bitmask DP** algorithm:
    - Fix knight 0 as starting vertex to eliminate rotational symmetry.
    - State: `dp[mask][u]` is `True` if there is a path starting at knight 0 visiting the subset of knights `mask` and ending at knight `u`.
    - Parent: `parent[mask][u]` tracks the predecessor knight to reconstruct the seating order.
    - Transitions: From endpoint `u` in `mask`, extend to an unvisited friend `v` (`friends[u][v] == True`), updating `dp[mask | (1 << v)][v] = True` and `parent[mask | (1 << v)][v] = u`.
    - Closing cycle: In `full_mask = (1 << n) - 1`, locate an endpoint `u` with `friends[u][0] == True`, then backtrack predecessors to recover the circular seating.
- **Complexity:**
  - Time: `O(n^2 * 2^n)`
  - Space: `O(n * 2^n)`

## Running Demos and Tests

Run all demo test cases:
```bash
python3 main.py
```

Run a specific task demo:
```bash
python3 main.py --task 1
python3 main.py --task 2
python3 main.py --task 5
```

Run the unit tests:
```bash
python3 -m unittest discover -s tests -v
```
