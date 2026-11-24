"""Task 2 - Domino Tiling (Required technique: Brute Force).

Problem:
    Consider an n x n chessboard (2 <= n <= 8) with two missing squares of
    opposite colors, given as 0-based (row, col) coordinates. Determine
    whether the remaining squares can be covered completely by nonoverlapping
    2 x 1 dominoes, each covering two horizontally or vertically adjacent
    squares. Return one valid tiling or report that none exists.

Representation Assumption:
    Each placed domino is represented as a pair of 0-based cell coordinates:
    ((r1, c1), (r2, c2)). Thus `dominoes` is a list of such coordinate pairs.

Brute Force Algorithm:
    1. Validate board size (2 <= n <= 8) and missing square coordinates.
    2. Check the necessary color-balance condition: since every 2 x 1 domino
       covers exactly one black square and one white square, a valid tiling
       requires equal counts of remaining black and white squares (which
       immediately rules out odd n, where n^2 - 2 is odd, as well as
       same-color missing squares).
    3. Exhaustively search for a valid tiling via recursive brute-force
       backtracking in row-major order:
       - Locate the first uncovered square (r, c).
       - If all squares are covered, a valid tiling has been found.
       - Otherwise, try placing a horizontal domino covering (r, c) and
         (r, c + 1), recursing on the remaining board.
       - If that fails, backtrack and try placing a vertical domino covering
         (r, c) and (r + 1, c), recursing on the remaining board.
       - If neither placement leads to a complete tiling, backtrack.

Complexity:
    - Time Complexity:  O(2^(n^2 / 2)) in the worst case (each of the
      (n^2 - 2) / 2 domino placements branches up to 2 ways: horizontal or
      vertical). For n <= 8, there are at most 31 dominoes.
    - Space Complexity: O(n^2) — for the n x n board state, recursion stack
      (depth <= n^2 / 2), and output list of dominoes.
"""

from typing import List, Sequence, Tuple

Cell = Tuple[int, int]
Domino = Tuple[Cell, Cell]


def _validate_cell(n: int, cell: Cell, name: str) -> None:
    if len(cell) != 2:
        raise ValueError(f"{name} must be a (row, col) pair, got {cell!r}")
    r, c = cell
    if not (0 <= r < n and 0 <= c < n):
        raise ValueError(
            f"{name}={(r, c)} is out of bounds for a {n}x{n} board"
        )


def tileDominoes(
    n: int, missing1: Cell, missing2: Cell
) -> Tuple[bool, List[Domino]]:
    """Find a valid 2 x 1 domino tiling of an n x n board missing two squares.

    Args:
        n: Board dimension (2 <= n <= 8).
        missing1: 0-based (row, col) of the first missing square.
        missing2: 0-based (row, col) of the second missing square.

    Returns:
        A tuple (possible, dominoes) where:
            - possible: True if a complete domino tiling exists, else False.
            - dominoes: List of ((r1, c1), (r2, c2)) pairs representing each
              placed domino (empty list if not possible).

    Raises:
        ValueError: If n is outside [2, 8], coordinates are out of bounds, or
            missing1 == missing2.
    """
    if not (2 <= n <= 8):
        raise ValueError(f"Board size n must satisfy 2 <= n <= 8, got {n}")

    _validate_cell(n, missing1, "missing1")
    _validate_cell(n, missing2, "missing2")

    if missing1 == missing2:
        raise ValueError("missing1 and missing2 must be distinct squares")

    # Necessary condition: each domino covers one square of each color,
    # so remaining black and white square counts must be equal.
    # (For odd n, n^2 - 2 is odd, so counts can never be equal.)
    color_counts = [0, 0]
    for r in range(n):
        for c in range(n):
            if (r, c) != missing1 and (r, c) != missing2:
                color_counts[(r + c) % 2] += 1

    if color_counts[0] != color_counts[1]:
        return False, []

    covered = [[False] * n for _ in range(n)]
    covered[missing1[0]][missing1[1]] = True
    covered[missing2[0]][missing2[1]] = True

    dominoes: List[Domino] = []
    total_cells = n * n

    def backtrack(pos: int) -> bool:
        while pos < total_cells:
            r, c = divmod(pos, n)
            if not covered[r][c]:
                break
            pos += 1
        else:
            # All remaining squares have been covered.
            return True

        # Choice 1: Place a horizontal domino at (r, c) and (r, c + 1).
        if c + 1 < n and not covered[r][c + 1]:
            covered[r][c] = True
            covered[r][c + 1] = True
            dominoes.append(((r, c), (r, c + 1)))

            if backtrack(pos + 1):
                return True

            dominoes.pop()
            covered[r][c] = False
            covered[r][c + 1] = False

        # Choice 2: Place a vertical domino at (r, c) and (r + 1, c).
        if r + 1 < n and not covered[r + 1][c]:
            covered[r][c] = True
            covered[r + 1][c] = True
            dominoes.append(((r, c), (r + 1, c)))

            if backtrack(pos + 1):
                return True

            dominoes.pop()
            covered[r][c] = False
            covered[r + 1][c] = False

        return False

    if backtrack(0):
        return True, dominoes
    return False, []


def verify_tiling(
    n: int, missing1: Cell, missing2: Cell, dominoes: Sequence[Domino]
) -> bool:
    """Verify that `dominoes` forms a valid, nonoverlapping tiling."""
    expected_dominoes = (n * n - 2) // 2
    if (n * n - 2) % 2 != 0 or len(dominoes) != expected_dominoes:
        return False

    seen = {missing1, missing2}
    for cell_a, cell_b in dominoes:
        r1, c1 = cell_a
        r2, c2 = cell_b
        if not (0 <= r1 < n and 0 <= c1 < n and 0 <= r2 < n and 0 <= c2 < n):
            return False
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        if cell_a in seen or cell_b in seen:
            return False
        seen.add(cell_a)
        seen.add(cell_b)

    return len(seen) == n * n


def format_board(
    n: int, missing1: Cell, missing2: Cell, dominoes: Sequence[Domino]
) -> str:
    """Render the tiled board as an aligned ASCII grid."""
    grid = [["  "] * n for _ in range(n)]
    grid[missing1[0]][missing1[1]] = "XX"
    grid[missing2[0]][missing2[1]] = "XX"

    for idx, (cell_a, cell_b) in enumerate(dominoes, start=1):
        label = f"{idx:02d}"
        grid[cell_a[0]][cell_a[1]] = label
        grid[cell_b[0]][cell_b[1]] = label

    return "\n".join("  " + " ".join(row) for row in grid)


def _run_demo() -> None:
    print("=" * 60)
    print("Task 2 - Domino Tiling (Brute Force)")
    print("=" * 60)

    sample_cases = [
        ("Case 1 (4x4 board - PDF example)", 4, (0, 0), (3, 2)),
        ("Case 2 (3x3 odd board - impossible)", 3, (0, 0), (0, 1)),
        ("Case 3 (6x6 board - opposite corners adjacent)", 6, (0, 0), (5, 4)),
        ("Case 4 (8x8 chessboard - opposite colors)", 8, (0, 1), (7, 7)),
    ]

    for label, n, m1, m2 in sample_cases:
        possible, dominoes = tileDominoes(n, m1, m2)
        print(f"\n{label}")
        print(f"  Input:    n={n}, missing1={m1}, missing2={m2}")
        print(f"  Possible: {possible}")
        if possible:
            assert verify_tiling(n, m1, m2, dominoes), "Verification failed!"
            print(f"  Dominoes ({len(dominoes)}): {dominoes}")
            print("  Board:")
            print(format_board(n, m1, m2, dominoes))
        else:
            print("  Dominoes: []")


if __name__ == "__main__":
    _run_demo()
