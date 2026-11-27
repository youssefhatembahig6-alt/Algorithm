"""Task 6 - Killing Squares / Toothpick Removal (Required technique: Dynamic Programming).

Problem:
    Given an n x n grid formed by unit-length toothpicks (2 * n * (n + 1)
    toothpicks in total), find a minimum set of toothpicks to remove so that
    no axis-aligned square of any size 1..n remains intact.

Coordinate Representation:
    - Horizontal toothpicks: (row, col) with row in 0..n, col in 0..n-1.
    - Vertical toothpicks:   (n + 1 + row, col) with row in 0..n-1, col in 0..n.

Dynamic Programming Strategy:
    - Enumerate all squares of size 1..n (total S = n(n+1)(2n+1)/6) and
      precompute a bitmask `coverage[e]` of which squares each toothpick breaks.
    - State `dp(mask)`: minimum additional toothpicks needed to break all
      remaining squares given the bitmask `mask` of already-broken squares.
    - Transition: pick an unbroken square and branch on removing each of its
      boundary toothpicks, memoizing results with `lru_cache`.

Complexity:
    - Time Complexity:  Exponential in the number of squares S = O(n^3) in the
      worst case, heavily pruned by memoization and choosing high-coverage
      unbroken squares first.
    - Space Complexity: O(2^S) worst-case memoization table.
"""

from functools import lru_cache
from typing import List, Sequence, Tuple


def breakAllSquares(n: int) -> List[Tuple[int, int]]:
    """Return a minimum list of toothpick coordinates to break all squares."""

    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return []

    # Step 1: Create all toothpicks
    # H = horizontal, V = vertical
    edges = []

    for r in range(n + 1):
        for c in range(n):
            edges.append(("H", r, c))

    for r in range(n):
        for c in range(n + 1):
            edges.append(("V", r, c))

    edge_id = {edge: i for i, edge in enumerate(edges)}

    # Step 2: Generate all squares and their boundaries
    squares = []
    coverage = [0] * len(edges)

    for size in range(1, n + 1):
        for r in range(n - size + 1):
            for c in range(n - size + 1):

                boundary = []

                # Top and bottom edges
                for j in range(size):
                    boundary.append(edge_id[("H", r, c + j)])
                    boundary.append(edge_id[("H", r + size, c + j)])

                # Left and right edges
                for j in range(size):
                    boundary.append(edge_id[("V", r + j, c)])
                    boundary.append(edge_id[("V", r + j, c + size)])

                squares.append(boundary)

    # Step 3: Calculate which squares each toothpick can break
    for i, boundary in enumerate(squares):
        for edge in boundary:
            coverage[edge] |= (1 << i)

    total_squares = len(squares)
    FULL = (1 << total_squares) - 1

    # Step 4: Dynamic Programming with memoization
    choice = {}

    @lru_cache(maxsize=None)
    def dp(mask):

        # Base case: all squares are broken
        if mask == FULL:
            return 0

        # Find an unbroken square
        # Prefer one whose edges cover many squares
        best_square = None
        best_score = -1

        for i, boundary in enumerate(squares):
            if not (mask & (1 << i)):

                score = sum(coverage[e].bit_count()
                            for e in boundary)

                if score > best_score:
                    best_score = score
                    best_square = boundary

        # Try removing each of its four boundary toothpicks
        minimum = float("inf")
        best_edge = None

        for edge in best_square:

            new_mask = mask | coverage[edge]

            cost = 1 + dp(new_mask)

            if cost < minimum:
                minimum = cost
                best_edge = edge

        choice[mask] = best_edge

        return minimum

    # Step 5: Calculate the minimum number of removals
    dp(0)

    # Step 6: Reconstruct the optimal solution
    removed = []
    mask = 0

    while mask != FULL:

        edge = choice[mask]
        removed.append(edge)

        mask |= coverage[edge]

    # Step 7: Convert toothpicks to (row, col)
    # Horizontal: row = 0 ... n
    # Vertical: row = n+1 ... 2n
    result = []

    for edge in removed:
        direction, r, c = edges[edge]

        if direction == "H":
            result.append((r, c))
        else:
            result.append((n + 1 + r, c))

    return result


def verify_broken_squares(n: int, removed: Sequence[Tuple[int, int]]) -> bool:
    """Verify that removing the given toothpicks breaks every square in an n x n grid."""
    if n < 0:
        return False
    if n == 0:
        return len(removed) == 0

    removed_set = set()
    for row, col in removed:
        if 0 <= row <= n and 0 <= col < n:
            removed_set.add(("H", row, col))
        elif n + 1 <= row <= 2 * n and 0 <= col <= n:
            removed_set.add(("V", row - (n + 1), col))
        else:
            return False

    for size in range(1, n + 1):
        for r in range(n - size + 1):
            for c in range(n - size + 1):
                boundary = set()
                for j in range(size):
                    boundary.add(("H", r, c + j))
                    boundary.add(("H", r + size, c + j))
                    boundary.add(("V", r + j, c))
                    boundary.add(("V", r + j, c + size))
                if boundary.isdisjoint(removed_set):
                    return False

    return True


def _run_demo() -> None:
    print("=" * 60)
    print("Task 6 - Killing Squares (Dynamic Programming)")
    print("=" * 60)

    for n in range(1, 5):
        removed = breakAllSquares(n)
        assert verify_broken_squares(n, removed), f"Verification failed for n={n}!"
        print(f"\nBoard: {n} x {n}")
        print(f"  Minimum toothpicks: {len(removed)}")
        print(f"  Removed toothpicks: {removed}")
        print("  Verified: All squares broken.")


if __name__ == "__main__":
    _run_demo()
