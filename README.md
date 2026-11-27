# EED461: Design and Analysis of Algorithms (2026/2027)

Ain Shams University — Faculty of Engineering  
Computer Engineering and Software Systems Program

Python implementation of all 8 EED461 group project tasks, each solved using its assigned algorithmic design technique (standard library only, Python 3.8+).

## Repository Structure

```text
Algorithm/
├── main.py                        # CLI demo runner for all 8 tasks
├── README.md
├── tasks/
│   ├── __init__.py                # Package exports for all task functions
│   ├── task1_coin_removal.py      # Task 1 - Coin Removal (Greedy)
│   ├── task2_domino_tiling.py     # Task 2 - Domino Tiling (Brute Force)
│   ├── task3_switches.py          # Task 3 - Security Switches (Decrease and Conquer)
│   ├── task4_points.py            # Task 4 - Point Coloring (Iterative Improvement)
│   ├── task5_round_table.py       # Task 5 - King Arthur's Round Table (Dynamic Programming)
│   ├── task6_killing_squares.py   # Task 6 - Killing Squares (Dynamic Programming)
│   ├── task7_poison_test.py       # Task 7 - Poisoned Wine (Divide and Conquer)
│   └── task8_tromino.py           # Task 8 - Colored Tromino Tiling (Divide and Conquer)
└── tests/
    ├── __init__.py
    ├── test_task1.py              # Unit tests for Task 1
    ├── test_task2.py              # Unit tests for Task 2
    ├── test_task3.py              # Unit tests for Task 3
    ├── test_task4.py              # Unit tests for Task 4
    ├── test_task5.py              # Unit tests for Task 5
    ├── test_task6.py              # Unit tests for Task 6
    ├── test_task7.py              # Unit tests for Task 7
    └── test_task8.py              # Unit tests for Task 8
```

## Tasks Overview

| # | Task | Algorithmic Technique | Function | File |
| - | ---- | --------------------- | -------- | ---- |
| 1 | Coin Removal | Greedy | `removeCoins` | `tasks/task1_coin_removal.py` |
| 2 | Domino Tiling | Brute Force | `tileDominoes` | `tasks/task2_domino_tiling.py` |
| 3 | Security Switches | Decrease and Conquer | `turnOffSwitches` | `tasks/task3_switches.py` |
| 4 | Point Coloring | Iterative Improvement | `colorPoints` | `tasks/task4_points.py` |
| 5 | King Arthur's Round Table | Dynamic Programming | `seatKnights` | `tasks/task5_round_table.py` |
| 6 | Killing Squares | Dynamic Programming | `breakAllSquares` | `tasks/task6_killing_squares.py` |
| 7 | Poisoned Wine | Divide and Conquer | `designWineTests` | `tasks/task7_poison_test.py` |
| 8 | Colored Tromino Tiling | Divide and Conquer | `tileTromino` | `tasks/task8_tromino.py` |

## Task Details

### Task 1 — Coin Removal (`Greedy`)
- **Function:** `removeCoins(n: int, coins: Sequence[str]) -> tuple[bool, list[int]]`
- **File:** `tasks/task1_coin_removal.py`
- **Characterization:** A non-empty line of coins can be completely cleared **if and only if** the number of heads-up (`'H'`) coins is **odd** (an empty line `n == 0` is trivially cleared in `0` moves).
- **Strategy:** Scan left to right for the leftmost `'H'` at index `i`. Remove `i`, flip `i + 1` (if present), and cascade leftward to remove `i - 1, i - 2, ..., left` (each flipped from `'T'` to `'H'` by the previous removal). Advance `left = i + 1` and repeat.
- **Complexity:** Time `O(n)`, Space `O(n)`.

### Task 2 — Domino Tiling (`Brute Force`)
- **Function:** `tileDominoes(n: int, missing1: tuple[int, int], missing2: tuple[int, int]) -> tuple[bool, list[tuple[tuple[int, int], tuple[int, int]]]]`
- **File:** `tasks/task2_domino_tiling.py`
- **Assumptions:** `2 <= n <= 8` with 0-based `(row, col)` coordinates and `missing1 != missing2`. Each placed domino is represented as `((r1, c1), (r2, c2))`.
- **Strategy:** Verify equal counts of remaining black and white squares (which rules out odd `n` and same-color missing squares), then exhaustively search placements via recursive backtracking in row-major order, trying horizontal and vertical placements at the first uncovered cell.
- **Complexity:** Time `O(2^(n^2 / 2))` worst-case, Space `O(n^2)`.

### Task 3 — Security Switches (`Decrease and Conquer`)
- **Function:** `turnOffSwitches(n: int) -> tuple[int, list[int]]`
- **File:** `tasks/task3_switches.py`
- **Strategy:** Define `Off(j)` as the minimum toggle sequence turning off switches `j..n` (all starting ON). To turn off switch `j`, recursively turn off `j+2..n` (`Off(j+2)`), toggle `j`, undo `Off(j+2)` by reversing it (`On(j+2)`), and recursively turn off `j+1..n` (`Off(j+1)`).
- **Recurrence & Closed Form:** `T(k) = T(k - 1) + 2*T(k - 2) + 1`, with minimum moves `floor(2^(n + 1) / 3)` (Chinese Rings / Gray code sequence).
- **Complexity:** Time `O(2^n)` (output-sensitive; generates every toggle), Space `O(2^n)`.

### Task 4 — Point Coloring (`Iterative Improvement`)
- **Function:** `colorPoints(n: int, points: list) -> list[str]`
- **File:** `tasks/task4_points.py`
- **Strategy:** Pair consecutive points on every horizontal and vertical line to form a bipartite degree-`<= 2` graph of paths and even cycles. Starting from an all-black coloring, iteratively locate a "bad" monochromatic edge `(u, v)`, walk along its path/cycle until the next bad edge or path endpoint, and flip the colors of that segment. Each iteration strictly reduces the number of bad edges until every line satisfies `|#B - #W| <= 1`.
- **Complexity:** Time `O(n^2)` worst-case (`<= n / 2` improvements), Space `O(n)`.

### Task 5 — King Arthur's Round Table (`Dynamic Programming`)
- **Function:** `seatKnights(n: int, friends: list[list[bool]]) -> list[int]`
- **File:** `tasks/task5_round_table.py`
- **Graph-Theoretic Characterization:** Equivalent to finding a **Hamiltonian Cycle** in the undirected friendship graph $G = (V, E)$. By **Dirac's Theorem (1952)**, if $n \ge 3$ and every vertex has degree $\ge n / 2$, a Hamiltonian cycle is guaranteed to exist.
- **Strategy:** Uses **Bellman–Held–Karp bitmask DP** with knight `0` fixed as the start. `dp[mask][u]` tracks reachability of subset `mask` ending at `u`, and `parent[mask][u]` reconstructs the cycle once an endpoint `u` in `full_mask` is friends with knight `0`.
- **Complexity:** Time `O(n^2 * 2^n)`, Space `O(n * 2^n)`.

### Task 6 — Killing Squares (`Dynamic Programming`)
- **Function:** `breakAllSquares(n: int) -> list[tuple[int, int]]`
- **File:** `tasks/task6_killing_squares.py`
- **Representation:** Horizontal toothpicks are encoded as `(row, col)` with `0 <= row <= n`, `0 <= col < n`; vertical toothpicks as `(n + 1 + row, col)` with `0 <= row < n`, `0 <= col <= n`.
- **Strategy:** Enumerate all axis-aligned squares of sizes `1..n` and precompute a bitmask `coverage[e]` of squares broken by each toothpick `e`. Memoized top-down bitmask DP (`dp(mask)`) selects an unbroken square with highest boundary coverage and branches on removing each of its boundary toothpicks to find the minimum hitting set.
- **Complexity:** Exponential in the number of squares $S = n(n + 1)(2n + 1) / 6$ in the worst case, pruned via memoization.

### Task 7 — Poisoned Wine (`Divide and Conquer`)
- **Function:** `designWineTests(testers: int) -> tuple[bool, dict[int, list[int]] | None, Callable | None]`
- **File:** `tasks/task7_poison_test.py`
- **Strategy:** Since 5 weeks = 35 days and the poison takes 30 days, only one round of testing is possible (`2^testers >= 1000` is required; 10 testers suffice since `2^10 = 1024 >= 1000`, while 8 testers do not since `2^8 = 256 < 1000`). Recursively divide the barrel interval `[0, 2^testers)` into left and right halves, assigning each level's tester to taste all valid barrels in the right halves. Decoding performs a binary-search halving from `[0, 2^testers)` down to the unique poisoned barrel.
- **Complexity:** Schedule construction `O(testers * barrels)`, decoding `O(testers)`, Space `O(testers * barrels)`.

### Task 8 — Colored Tromino Tiling (`Divide and Conquer`)
- **Function:** `tileTromino(n: int, missingRow: int, missingCol: int) -> list[Tromino]`
- **File:** `tasks/task8_tromino.py`
- **Strategy:**
  - **Divide:** Split the `2^n x 2^n` board into four `2^(n-1) x 2^(n-1)` quadrants and place one center L-tromino covering the three center cells outside the quadrant containing the missing square.
  - **Conquer:** Recursively tile and 3-color (`R`, `G`, `B`) each quadrant down to the `2x2` base case.
  - **Combine:** Fix quadrant 0's colors and search over color permutations for the other three quadrants and center tromino (`6^3 * 3 = 648` constant choices) so no edge-adjacent trominoes share a color across quadrant seams.
- **Complexity:** For $N = 4^n$ cells, recurrence $T(N) = 4T(N/4) + O(N)$ gives Time `O(N log N) = O(n * 4^n)`, Space `O(4^n)`.

## Running Demos and Tests

Run all demo test cases:
```bash
python3 main.py
```

Run a specific task demo (`1` through `8`):
```bash
python3 main.py --task 1
python3 main.py --task 6
python3 main.py --task 8
```

Run the full unit test suite:
```bash
python3 -m unittest discover -s tests -v
```

Run a single task's unit tests:
```bash
python3 -m unittest tests.test_task6 -v
```
