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
│   └── task2_domino_tiling.py    # Task 2 - Domino Tiling (Brute Force)
└── tests/
    ├── __init__.py
    ├── test_task1.py             # Unit tests for Task 1
    └── test_task2.py             # Unit tests for Task 2
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

## Running Demos and Tests

Run all demo test cases:
```bash
python3 main.py
```

Run a specific task demo:
```bash
python3 main.py --task 1
python3 main.py --task 2
```

Run the full unit test suite:
```bash
python3 -m unittest discover -s tests -v
```
