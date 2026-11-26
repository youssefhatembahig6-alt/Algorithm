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
    - Under the problem statement's condition ("each knight is friends with at
      least half of all n knights"), a valid circular seating is guaranteed
      to exist.

Technique — Bitmask Dynamic Programming (Held-Karp):
    - State: dp[mask][u] = True if there is a path visiting the subset of knights
      in 'mask', starting at knight 0 and ending at knight u.
    - Parent: parent[mask][u] tracks the predecessor knight to reconstruct the path.
    - Knight 0 is fixed as the starting point to break rotational symmetry.
    - Time Complexity: O(n^2 * 2^n)
    - Space Complexity: O(n * 2^n)
"""

from typing import List, Sequence


def seatKnights(n: int, friends: List[List[bool]]) -> List[int]:
    """
    Finds a valid circular seating for n knights such that adjacent knights are friends,
    using Bitmask Dynamic Programming.
    
    Args:
        n: Number of knights (n > 2).
        friends: An n x n boolean adjacency matrix where friends[i][j] is True 
                 if knight i and knight j are friends.
                 
    Returns:
        A list of integers representing the seating order (0-indexed: 0 to n-1).
        Returns an empty list if no valid seating exists.
    """
    if n <= 2:
        return []

    # dp[mask][u] = True if there is a path visiting the subset of knights in 'mask',
    # starting at knight 0 and ending at knight u.
    dp = [[False] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    # Fix knight 0 as the starting point to break rotational symmetry
    dp[1][0] = True

    # Iterate through all subsets of knights
    for mask in range(1, 1 << n):
        # Skip subsets that don't include knight 0
        if not (mask & 1):
            continue
            
        for u in range(n):
            if dp[mask][u]:
                # Try extending the path from u to an unvisited friend v
                for v in range(1, n):
                    if not (mask & (1 << v)) and friends[u][v]:
                        next_mask = mask | (1 << v)
                        if not dp[next_mask][v]:
                            dp[next_mask][v] = True
                            parent[next_mask][v] = u

    # Check if any complete Hamiltonian path can close the cycle back to knight 0
    full_mask = (1 << n) - 1
    end_knight = -1
    for u in range(1, n):
        if dp[full_mask][u] and friends[u][0]:
            end_knight = u
            break

    if end_knight == -1:
        return []

    # Reconstruct the circular seating path
    seating = []
    curr = end_knight
    curr_mask = full_mask
    
    while curr != -1:
        seating.append(curr)
        prev = parent[curr_mask][curr]
        curr_mask ^= (1 << curr)
        curr = prev

    seating.reverse()
    return seating


def verify_seating(n: int, friends: Sequence[Sequence[bool]], seating: Sequence[int]) -> bool:
    """Verify that seating is a valid circular seating of all n knights."""
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

    # Case 1: n = 3, Triangle
    friends1 = [
        [False, True, True],
        [True, False, True],
        [True, True, False],
    ]

    # Case 2: n = 4, Cycle (n/2 = 2)
    friends2 = [
        [False, False, True, True],
        [False, False, True, True],
        [True, True, False, False],
        [True, True, False, False],
    ]

    # Case 3: n = 8, Diagram from assignment
    n3 = 8
    friends3 = [[False] * n3 for _ in range(n3)]
    for i in range(n3):
        for step in [1, 2]:
            neighbor = (i + step) % n3
            friends3[i][neighbor] = friends3[neighbor][i] = True

    # Case 4: Impossible seating (star graph)
    friends4 = [
        [False, True, True, True],
        [True, False, False, False],
        [True, False, False, False],
        [True, False, False, False],
    ]

    sample_cases = [
        ("Case 1 (n=3 Triangle)", 3, friends1),
        ("Case 2 (n=4 Cycle)", 4, friends2),
        ("Case 3 (n=8 Assignment Diagram)", 8, friends3),
        ("Case 4 (n=4 Impossible Star Graph)", 4, friends4),
    ]

    for label, n, matrix in sample_cases:
        seating = seatKnights(n, matrix)
        print(f"\n{label}")
        print(f"  Knights count: n = {n}")
        if seating:
            print(f"  Seating order: {seating}")
            cycle_str = " -> ".join(str(k) for k in seating) + f" -> {seating[0]}"
            print(f"  Table arrangement: {cycle_str}")
            assert verify_seating(n, matrix, seating), "Verification failed!"
            print("  Verified: Valid circular seating.")
        else:
            print("  Seating order: None (No valid circular seating exists).")


if __name__ == "__main__":
    _run_demo()
