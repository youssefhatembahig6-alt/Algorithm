"""
Task 4 - Point Coloring           (technique: Iterative Improvement)

Goal: color n distinct points 'B'/'W' so that on every horizontal / vertical
line containing points, |#B - #W| <= 1.

Model
-----
On every line, sort its points and pair them up consecutively
(1st-2nd, 3rd-4th, ...); at most one point per line is left unpaired.
Each point lies on one horizontal and one vertical line, so it has at most
one horizontal pair-edge and one vertical pair-edge  ->  every vertex has
degree <= 2, and the graph is a set of paths and EVEN cycles
(edges alternate horizontal / vertical).

An edge is "bad" if both endpoints have the same color.
If no edge is bad, every pair on every line is B+W, so each line differs
by at most one (the unpaired point)  ->  valid coloring.

Iterative improvement
---------------------
  1. Start with ANY coloring (all black - the worst case).
  2. While a bad edge e=(u,v) exists:
        walk along the path/cycle from v (away from u) and flip the whole
        segment of vertices until just before the next bad edge g
        (or to the end of the path).
        Flipping a contiguous segment only changes the status of its two
        boundary edges: e becomes good, g (if reached) becomes good too.
  3. The number of bad edges strictly decreases each iteration, so the
     algorithm always terminates (in <= n/2 improvements) with a valid
     coloring.  (In a cycle the number of bad edges is even, so a second
     bad edge is always found before wrapping around.)
"""
from collections import defaultdict


def colorPoints(n: int, points: list) -> list:
    pts = [tuple(p) for p in points[:n]]
    if len(set(pts)) != len(pts):
        raise ValueError("points must be distinct")
    n = len(pts)

    # ---- build the pairing graph -------------------------------------
    edges = []                              # (u, v)
    adj = [[] for _ in range(n)]            # adj[u] = list of edge ids

    def add_pairs(groups):
        for idxs in groups.values():
            for a in range(0, len(idxs) - 1, 2):
                u, v = idxs[a], idxs[a + 1]
                adj[u].append(len(edges))
                adj[v].append(len(edges))
                edges.append((u, v))

    rows, cols = defaultdict(list), defaultdict(list)
    for i, (x, y) in enumerate(pts):
        rows[y].append(i)                   # horizontal line: same y
        cols[x].append(i)                   # vertical line:   same x
    for g in rows.values():
        g.sort(key=lambda i: pts[i][0])
    for g in cols.values():
        g.sort(key=lambda i: pts[i][1])
    add_pairs(rows)
    add_pairs(cols)

    # ---- 1. arbitrary initial coloring --------------------------------
    color = [0] * n                         # 0 = black, 1 = white

    def bad(e):
        u, v = edges[e]
        return color[u] == color[v]

    def other(e, u):
        a, b = edges[e]
        return b if a == u else a

    # ---- 2. iterative improvement -------------------------------------
    improved = True
    while improved:
        improved = False
        for e in range(len(edges)):
            if not bad(e):
                continue
            u, v = edges[e]
            segment, cur, cur_e = [v], v, e
            while True:
                nxt_edges = [f for f in adj[cur] if f != cur_e]
                if not nxt_edges:           # reached the end of a path
                    break
                f = nxt_edges[0]
                nxt = other(f, cur)
                if bad(f) or nxt == u:      # next bad edge (or wrapped round)
                    break
                segment.append(nxt)
                cur, cur_e = nxt, f
            for w in segment:               # flip the whole segment
                color[w] ^= 1
            improved = True

    return ['B' if c == 0 else 'W' for c in color]


# --------------------------------------------------------------------------
def is_valid(points: list, colors: list) -> bool:
    lines = defaultdict(lambda: [0, 0])
    for (x, y), c in zip(points, colors):
        k = 0 if c == 'B' else 1
        lines[('h', y)][k] += 1
        lines[('v', x)][k] += 1
    return all(abs(b - w) <= 1 for b, w in lines.values())


if __name__ == "__main__":
    import random

    tests = {
        "Test 1 (2x2 square)": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "Test 2 (one row of 5)": [(i, 0) for i in range(5)],
        "Test 3 (mixed)": [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1),
                           (1, 2), (2, 2), (3, 2), (3, 0), (3, 3)],
    }
    for name, pts in tests.items():
        cols = colorPoints(len(pts), pts)
        print(f"{name}\n  points = {pts}\n  colors = {cols}\n"
              f"  valid  = {is_valid(pts, cols)}")

    # randomized stress test
    random.seed(1)
    for _ in range(2000):
        m = random.randint(1, 60)
        size = random.randint(2, 8)
        pts = list({(random.randrange(size), random.randrange(size))
                    for _ in range(m)})
        assert is_valid(pts, colorPoints(len(pts), pts))
    print("\nRandom stress test: 2000 cases, all valid")
