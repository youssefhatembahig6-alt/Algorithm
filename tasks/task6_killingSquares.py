from functools import lru_cache


def breakAllSquares(n: int):

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
