"""Task 8 - Colored Tromino Tiling (Required technique: Divide and Conquer).

Problem:
    Tile a 2^n x 2^n board (n >= 2) with one missing square using L-shaped
    trominoes colored with at most 3 colors (R, G, B) such that no two
    edge-adjacent trominoes share the same color.

Divide and Conquer Strategy:
    - Divide: split the 2^n x 2^n board into four 2^(n-1) x 2^(n-1) quadrants
      and place one center L-tromino covering the three center cells outside
      the quadrant containing the missing square.
    - Conquer: recursively tile and 3-color each quadrant (base case: 2x2
      board with one missing square = one L-tromino).
    - Combine: keep quadrant 0's colors fixed and search over color
      permutations for the remaining three quadrants plus the center tromino
      (6^3 * 3 = 648 constant choices) to eliminate all seam color conflicts.

Complexity (N = 4^n cells, (N - 1) / 3 trominoes):
    - Recurrence: T(N) = 4 * T(N / 4) + O(N)
    - Time Complexity:  O(N log N) = O(n * 4^n)
    - Space Complexity: O(N) = O(4^n)
"""

import itertools
import sys
from dataclasses import dataclass
from typing import List, Tuple

sys.setrecursionlimit(10000)

COLORS = ("R", "G", "B")
PERMS = list(itertools.permutations(range(3)))


@dataclass
class Tromino:
    cells: Tuple[Tuple[int, int], ...]
    color: str = ""
    _c: int = 0

    def __repr__(self):
        return f"Tromino(cells={list(self.cells)}, color='{self.color}')"


def _combine(grid, top, left, size, groups, center):
    """Recolor quadrants so all neighboring trominoes have different colors."""
    half = size // 2
    midr, midc = top + half, left + half

    gid = {id(center): 4}
    for group_index, trominoes in enumerate(groups):
        for tromino in trominoes:
            gid[id(tromino)] = group_index

    pairs = set()

    def look(r, c, r2, c2):
        a, b = grid[r][c], grid[r2][c2]
        if a is None or b is None or a is b:
            return
        pairs.add((gid[id(a)], a._c, gid[id(b)], b._c))

    # Check the horizontal and vertical borders between quadrants.
    for c in range(left, left + size):
        look(midr - 1, c, midr, c)

    for r in range(top, top + size):
        look(r, midc - 1, r, midc)

    # Check neighbors of the center tromino.
    for r, c in center.cells:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            r2, c2 = r + dr, c + dc
            if top <= r2 < top + size and left <= c2 < left + size:
                look(r, c, r2, c2)

    # Keep quadrant 0 fixed and try all color permutations for the others.
    for p1, p2, p3 in itertools.product(PERMS, repeat=3):
        for center_color in range(3):
            permutations = [(0, 1, 2), p1, p2, p3,
                            (center_color,) * 3]

            if all(
                permutations[ga][ca] != permutations[gb][cb]
                for ga, ca, gb, cb in pairs
            ):
                for group_index, trominoes in enumerate(groups):
                    for tromino in trominoes:
                        tromino._c = permutations[group_index][tromino._c]

                center._c = center_color
                return

    raise RuntimeError("No valid coloring found.")


def _solve(grid, top, left, size, missing_row, missing_col):
    """Solve one square region that contains exactly one missing cell."""
    # Base case: a 2x2 board needs exactly one L-tromino.
    if size == 2:
        cells = tuple(
            (r, c)
            for r in (top, top + 1)
            for c in (left, left + 1)
            if (r, c) != (missing_row, missing_col)
        )
        tromino = Tromino(cells, _c=0)

        for r, c in cells:
            grid[r][c] = tromino

        return [tromino]

    half = size // 2
    middle_row, middle_col = top + half, left + half

    # The four cells around the center, one in each quadrant.
    centers = {
        (0, 0): (middle_row - 1, middle_col - 1),
        (0, 1): (middle_row - 1, middle_col),
        (1, 0): (middle_row, middle_col - 1),
        (1, 1): (middle_row, middle_col),
    }

    hole_quadrant = (
        0 if missing_row < middle_row else 1,
        0 if missing_col < middle_col else 1,
    )

    # DIVIDE: place one center tromino in the other three quadrants.
    center = Tromino(
        tuple(cell for quadrant, cell in centers.items()
              if quadrant != hole_quadrant)
    )

    # CONQUER: recursively solve all four quadrants.
    groups = []
    for quadrant_row in (0, 1):
        for quadrant_col in (0, 1):
            quadrant = (quadrant_row, quadrant_col)
            new_top = top + quadrant_row * half
            new_left = left + quadrant_col * half

            if quadrant == hole_quadrant:
                hole_row, hole_col = missing_row, missing_col
            else:
                hole_row, hole_col = centers[quadrant]

            groups.append(
                _solve(grid, new_top, new_left, half, hole_row, hole_col)
            )

    for r, c in center.cells:
        grid[r][c] = center

    # COMBINE: choose colors that satisfy the boundaries.
    _combine(grid, top, left, size, groups, center)

    return [center] + [
        tromino for group in groups for tromino in group
    ]


def tileTromino(n: int, missingRow: int, missingCol: int) -> List[Tromino]:
    """Return a colored tiling for a 2^n by 2^n board with one missing cell."""
    if n < 2:
        raise ValueError("n must be greater than 1.")

    size = 2 ** n

    if not (0 <= missingRow < size and 0 <= missingCol < size):
        raise ValueError("The missing square is outside the board.")

    grid = [[None] * size for _ in range(size)]
    tiles = _solve(grid, 0, 0, size, missingRow, missingCol)

    for tromino in tiles:
        tromino.color = COLORS[tromino._c]

    return tiles


def verify(n, missing_row, missing_col, tiles):
    """Check coverage, no overlap, L-shapes, and neighboring colors."""
    size = 2 ** n
    seen = {}

    for index, tromino in enumerate(tiles):
        rows = {cell[0] for cell in tromino.cells}
        cols = {cell[1] for cell in tromino.cells}

        assert (
            len(tromino.cells) == 3 and len(rows) == 2 and len(cols) == 2
        ), "A tile is not an L-shape."

        for cell in tromino.cells:
            assert cell not in seen, "Two trominoes overlap."
            seen[cell] = index

    assert len(seen) == size * size - 1, "The board is not fully covered."
    assert (missing_row, missing_col) not in seen, "The missing cell is covered."

    for (row, col), index in seen.items():
        for dr, dc in ((1, 0), (0, 1)):
            neighbor_index = seen.get((row + dr, col + dc))

            if neighbor_index is not None and neighbor_index != index:
                assert (
                    tiles[index].color != tiles[neighbor_index].color
                ), "Adjacent trominoes have the same color."

    return True


def render(n, missing_row, missing_col, tiles):
    """Return a text representation of the board."""
    size = 2 ** n
    grid = [
        [
            "X" if (row, col) == (missing_row, missing_col) else "."
            for col in range(size)
        ]
        for row in range(size)
    ]

    for tromino in tiles:
        for row, col in tromino.cells:
            grid[row][col] = tromino.color

    return "\n".join(" ".join(row) for row in grid)


def run_case(name, n, missing_row, missing_col):
    print("=" * 60)
    print(
        f"{name}: n={n}, board={2**n}x{2**n}, "
        f"missing=({missing_row}, {missing_col})"
    )

    tiles = tileTromino(n, missing_row, missing_col)
    expected = (4 ** n - 1) // 3

    print(f"Trominoes placed: {len(tiles)} (expected {expected})")
    print("Legend: R/G/B = tromino color, X = missing square")
    print(render(n, missing_row, missing_col, tiles))

    verify(n, missing_row, missing_col, tiles)
    print("VERIFIED: coverage, no overlap, L-shapes, and valid colors.")

    if n == 2:
        for tromino in tiles:
            print(" ", tromino)


def _run_demo() -> None:
    print("=" * 60)
    print("Task 8 - Colored Tromino Tiling (Divide and Conquer)")
    print("=" * 60)
    run_case("Case 1 (n=2, corner hole)", 2, 0, 0)
    run_case("Case 2 (n=3, middle hole)", 3, 3, 4)
    run_case("Case 3 (n=4, last cell)", 4, 15, 15)


def main() -> None:
    if len(sys.argv) == 4:
        run_case("Custom", *map(int, sys.argv[1:]))
    else:
        _run_demo()


if __name__ == "__main__":
    main()
