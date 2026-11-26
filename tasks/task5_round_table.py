"""Task 5 - King Arthur's Round Table (Required technique: Dynamic Programming).

Problem:
    King Arthur wishes to seat n > 2 knights around a circular table without
    any two enemies sitting next to one another. Friendship and enmity are
    mutual (the friendship graph is undirected), and each knight is friends
    with at least half of all n knights (degree(v) >= n / 2). Design an
    algorithm that produces a valid circular seating.

Graph-Theoretic Characterization:
    - The problem corresponds to finding a Hamiltonian Cycle in the friendship
      graph G = (V, E) where vertices are knights and edges represent friendship.
    - Dirac's Theorem (1952): Any simple undirected graph with n >= 3 vertices
      and minimum vertex degree delta(G) >= n / 2 is guaranteed to contain a
      Hamiltonian cycle.
    - Hence, under the problem statement's condition ("each knight is friends
      with at least half of all n knights"), a valid circular seating is
      always mathematically guaranteed to exist.

Required Technique — Dynamic Programming (Bellman-Held-Karp Bitmask DP):
    1. Fix an arbitrary knight (knight 0) as the starting vertex without loss of
       generality to break cyclic symmetry.
    2. Define DP state:
       DP[mask][u] = True iff there exists a simple path starting at knight 0,
       visiting exactly the subset of knights indicated by `mask` (where bit i
       is 1 iff knight i has been visited), and ending at knight u.
    3. Base Case:
       DP[1 << 0][0] = True (only knight 0 visited, ending at knight 0).
       All other states initialized to False.
    4. Transition:
       For each mask containing bit 0, and for each active endpoint u in mask:
           For each neighbor v not in mask where friends[u][v] is True:
               DP[mask | (1 << v)][v] = True
    5. Cycle Completion:
       At the full mask (1 << n) - 1, find an ending knight u such that
       DP[full_mask][u] is True and friends[u][0] is True (closing the cycle).
    6. Reconstruction:
       Backtrack from u to 0 using the DP states to construct the exact circular
       order [0, v1, v2, ..., u].
    7. Large-Scale Fallback (n > 20):
       While Held-Karp DP is optimal for moderate n (n <= 20), for larger n
       where 2^n would exceed practical memory and execution time, the module
       provides a seamless fallback using Dirac's constructive cycle-extension
       algorithm in O(n^2) polynomial time.

Complexity:
    - Dynamic Programming:
        Time Complexity:  O(n^2 * 2^n) bitmask operations
        Space Complexity: O(2^n) words for bitmask-compressed DP states
    - Dirac Fallback (for n > 20):
        Time Complexity:  O(n^2)
        Space Complexity: O(n)
"""

from collections import deque
from typing import List, Sequence


def _validate_inputs(n: int, friends: Sequence[Sequence[bool]]) -> None:
    """Validate problem constraints on n and the friendship matrix."""
    if not isinstance(n, int):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n <= 2:
        raise ValueError(f"n must be greater than 2, got {n}")
    if len(friends) != n:
        raise ValueError(f"friends matrix must have {n} rows, got {len(friends)}")
    for i, row in enumerate(friends):
        if len(row) != n:
            raise ValueError(
                f"Row {i} in friends matrix must have length {n}, got {len(row)}"
            )
        for j, val in enumerate(row):
            if not isinstance(val, (bool, int)):
                raise TypeError(
                    f"friends[{i}][{j}] must be a boolean, got {type(val).__name__}"
                )
            if i != j and bool(val) != bool(friends[j][i]):
                raise ValueError(
                    f"Friendship must be mutual: friends[{i}][{j}] != friends[{j}][{i}]"
                )


def seatKnights(n: int, friends: Sequence[Sequence[bool]]) -> List[int]:
    """Find a valid circular seating of n knights using Dynamic Programming.

    Args:
        n: Number of knights (n > 2).
        friends: An n x n boolean matrix where friends[i][j] is True if knight i
            and knight j are friends, and False otherwise.

    Returns:
        A list of n knight indices [s_0, s_1, ..., s_{n-1}] representing their
        circular seating order around the table, such that adjacent knights
        (including s_{n-1} and s_0) are friends. Returns an empty list if no
        valid circular seating exists.

    Raises:
        ValueError: If n <= 2, friends matrix is not n x n, or friendship
            is not mutual.
        TypeError: If n is not an int or friends elements are not booleans.
    """
    _validate_inputs(n, friends)

    # For moderate n, use the required Held-Karp Dynamic Programming algorithm.
    # For n > 20, 2^n memory/time is intractable; fall back to Dirac's O(n^2) algorithm.
    if n <= 20:
        return _seat_knights_dp(n, friends)
    else:
        return _seat_knights_dirac(n, friends)


def _seat_knights_dp(n: int, friends: Sequence[Sequence[bool]]) -> List[int]:
    """Held-Karp Bitmask Dynamic Programming for Hamiltonian Cycle."""
    # Precompute bitmasks of friends for fast bitwise transitions
    adj_mask = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and friends[i][j]:
                adj_mask[i] |= 1 << j

    full_mask = (1 << n) - 1

    # dp[mask] is an integer bitmask where bit u is 1 iff there is a simple path
    # starting at knight 0 visiting the subset `mask` and ending at knight u.
    dp = [0] * (1 << n)
    dp[1] = 1  # Base case: path starting at 0 with mask {0} ending at 0

    # Only iterate over masks where knight 0 is included (odd masks)
    for mask in range(1, full_mask, 2):
        endpoints = dp[mask]
        if not endpoints:
            continue

        while endpoints:
            # Extract the lowest set bit u (active path endpoint)
            u = (endpoints & -endpoints).bit_length() - 1
            endpoints &= endpoints - 1

            # Candidate unvisited friends of u
            unvisited_neighbors = adj_mask[u] & ~mask
            while unvisited_neighbors:
                v = (unvisited_neighbors & -unvisited_neighbors).bit_length() - 1
                unvisited_neighbors &= unvisited_neighbors - 1
                dp[mask | (1 << v)] |= 1 << v

    # Check which endpoints u in the full mask can close the cycle back to 0
    full_endpoints = dp[full_mask]
    closing_endpoint = None
    for u in range(1, n):
        if (full_endpoints & (1 << u)) and (adj_mask[u] & 1):
            closing_endpoint = u
            break

    if closing_endpoint is None:
        return []

    # Reconstruct the circular seating backwards from closing_endpoint to 0
    seating = [closing_endpoint]
    curr = closing_endpoint
    curr_mask = full_mask

    while curr != 0:
        prev_mask = curr_mask ^ (1 << curr)
        for p in range(n):
            if (
                (curr_mask & (1 << p))
                and (dp[prev_mask] & (1 << p))
                and (adj_mask[p] & (1 << curr))
            ):
                seating.append(p)
                curr = p
                curr_mask = prev_mask
                break

    seating.reverse()
    return seating


def _seat_knights_dirac(n: int, friends: Sequence[Sequence[bool]]) -> List[int]:
    """Constructive O(n^2) algorithm for Hamiltonian Cycle in Dirac graphs.

    Used as an efficient fallback when n > 20 where Held-Karp DP would exceed
    memory limits.
    """
    adj = [[bool(friends[i][j]) if i != j else False for j in range(n)] for i in range(n)]

    # Find an initial edge to start the path
    start_u, start_v = None, None
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j]:
                start_u, start_v = i, j
                break
        if start_u is not None:
            break

    if start_u is None:
        return []

    path = deque([start_u, start_v])
    in_path = [False] * n
    in_path[start_u] = in_path[start_v] = True

    while True:
        # Extend path greedily from head (left)
        while True:
            head = path[0]
            extended = False
            for v in range(n):
                if not in_path[v] and adj[head][v]:
                    path.appendleft(v)
                    in_path[v] = True
                    extended = True
                    break
            if not extended:
                break

        # Extend path greedily from tail (right)
        while True:
            tail = path[-1]
            extended = False
            for v in range(n):
                if not in_path[v] and adj[tail][v]:
                    path.append(v)
                    in_path[v] = True
                    extended = True
                    break
            if not extended:
                break

        p_list = list(path)
        k = len(p_list)

        # Check if head and tail can close directly into a cycle
        if adj[p_list[0]][p_list[-1]]:
            cycle = p_list
        else:
            # By Dirac's condition, there exists i such that (p[0], p[i+1]) in E
            # and (p[-1], p[i]) in E, allowing cycle formation.
            found_cross = False
            for i in range(k - 1):
                if adj[p_list[0]][p_list[i + 1]] and adj[p_list[-1]][p_list[i]]:
                    cycle = p_list[: i + 1] + p_list[i + 1 :][::-1]
                    found_cross = True
                    break
            if not found_cross:
                return []

        if len(cycle) == n:
            return cycle

        # Find an unvisited vertex x adjacent to some vertex in cycle to enlarge path
        found_extension = False
        in_cycle = set(cycle)
        for j, node in enumerate(cycle):
            for x in range(n):
                if not in_path[x] and adj[node][x]:
                    # Break cycle at node and attach x
                    new_path = cycle[j:] + cycle[:j]
                    path = deque([x] + new_path)
                    in_path[x] = True
                    found_extension = True
                    break
            if found_extension:
                break

        if not found_extension:
            return []


def verify_seating(n: int, friends: Sequence[Sequence[bool]], seating: Sequence[int]) -> bool:
    """Verify that seating is a valid circular seating of all n knights.

    Checks:
        1. seating contains exactly n knights.
        2. Every knight in 0..n-1 appears exactly once.
        3. Every pair of adjacent knights (including wrap-around) are friends.
    """
    if len(seating) != n:
        return False
    if set(seating) != set(range(n)):
        return False

    for i in range(n):
        u = seating[i]
        v = seating[(i + 1) % n]
        if not friends[u][v]:
            return False

    return True


def _run_demo() -> None:
    """Demonstrate Task 5 with sample test cases."""
    print("=" * 60)
    print("Task 5 - King Arthur's Round Table (Dynamic Programming)")
    print("=" * 60)

    # Helper to create friendship matrices easily
    def make_clique(size: int) -> List[List[bool]]:
        return [[i != j for j in range(size)] for i in range(size)]

    # Case 1: n = 4, complete graph K_4 (degree 3 >= 2)
    friends1 = make_clique(4)

    # Case 2: n = 6, each knight has deg 3 >= 3 (tight Dirac bound)
    # Circular friends: each knight friends with +/- 1 and opposite
    friends2 = [[False] * 6 for _ in range(6)]
    for i in range(6):
        friends2[i][(i + 1) % 6] = friends2[(i + 1) % 6][i] = True
        friends2[i][(i + 3) % 6] = friends2[(i + 3) % 6][i] = True

    # Case 3: n = 8 (King Arthur's Round Table illustrated in PDF)
    # Each knight friends with +/- 1, +/- 2 (deg 4 >= 4)
    friends3 = [[False] * 8 for _ in range(8)]
    for i in range(8):
        for delta in (1, 2):
            friends3[i][(i + delta) % 8] = friends3[(i + delta) % 8][i] = True

    # Case 4: Impossible seating (two disjoint components, degree condition violated)
    friends4 = [[False] * 6 for _ in range(6)]
    for i in range(3):
        for j in range(3):
            if i != j:
                friends4[i][j] = True
    for i in range(3, 6):
        for j in range(3, 6):
            if i != j:
                friends4[i][j] = True

    sample_cases = [
        ("Case 1 (n=4 Complete Graph)", 4, friends1),
        ("Case 2 (n=6 Tight Dirac Degree = 3)", 6, friends2),
        ("Case 3 (n=8 PDF Illustrated Round Table)", 8, friends3),
        ("Case 4 (n=6 Disjoint / Impossible Graph)", 6, friends4),
    ]

    for label, n, matrix in sample_cases:
        seating = seatKnights(n, matrix)
        print(f"\n{label}")
        print(f"  Knights count: n = {n}")
        min_deg = min(sum(bool(matrix[i][j]) for j in range(n) if i != j) for i in range(n))
        print(f"  Minimum degree in graph: {min_deg} (Dirac bound: n/2 = {n/2})")
        if seating:
            print(f"  Seating order: {seating}")
            # Format nicely as circular table
            cycle_str = " -> ".join(str(k) for k in seating) + f" -> {seating[0]}"
            print(f"  Table arrangement: {cycle_str}")
            is_valid = verify_seating(n, matrix, seating)
            assert is_valid, "Verification failed!"
            print(f"  Verified: Valid circular seating.")
        else:
            print("  Seating order: None (No valid circular seating exists).")


if __name__ == "__main__":
    _run_demo()
