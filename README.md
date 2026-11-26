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
- **Function:** `seatKnights(n: int, friends: Sequence[Sequence[bool]]) -> list[int]`
- **File:** `tasks/task5_round_table.py`
- **Graph-Theoretic Characterization:**
  - Finding a valid circular seating where adjacent knights are friends is equivalent to finding a **Hamiltonian Cycle** in the undirected friendship graph $G = (V, E)$.
  - **Dirac's Theorem (1952):** In any simple undirected graph with $n \ge 3$ vertices, if every vertex has degree $\ge n / 2$, the graph contains a Hamiltonian cycle. Hence, a valid seating is mathematically guaranteed to exist.
- **Dynamic Programming Strategy:**
  - Uses the **Bellman-Held-Karp bitmask DP** algorithm:
    - Fix knight 0 as starting vertex.
    - State: $DP[mask][u]$ indicates whether there exists a simple path starting at knight 0 visiting the subset of knights `mask` and ending at knight $u$.
    - Transitions: From endpoint $u$ in `mask`, transition to an unvisited friend $v$ by setting bit $v$ in `mask | (1 << v)`.
    - Closing cycle: In the full mask $(2^n - 1)$, find an endpoint $u$ adjacent to knight 0, and reconstruct the circular seating backwards in $O(n^2)$ time.
  - For $n > 20$, an $O(n^2)$ constructive Dirac path-extension fallback is provided to handle large inputs without running out of memory.
- **Complexity:**
  - Time: `O(n^2 * 2^n)` bitmask operations for DP (or `O(n^2)` for $n > 20$)
  - Space: `O(2^n)` words for bitmask-compressed DP states

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

Run the full unit test suite:
```bash
python3 -m unittest discover -s tests -v
```
