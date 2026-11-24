"""Task 1 - Coin Removal (Required technique: Greedy).

Problem:
    A line of n coins lies on a table, each showing either heads ('H') or
    tails ('T'). A move removes any heads-up coin and then flips its immediate
    neighbors, if present. Two coins count as neighbors only if they were
    adjacent in the original line; removing a coin does not close the gap.
    Determine precisely which starting rows can be cleared and give a valid
    removal sequence.

Characterization:
    - An empty row (n == 0) is trivially cleared with 0 moves.
    - A non-empty row can be cleared if and only if the number of heads ('H')
      is ODD.

Greedy Algorithm:
    Scan from left to right maintaining the start index `left` of the
    remaining uncleared suffix. Whenever we find the leftmost heads-up coin
    at index `i`:
        1. Remove coin `i` (appending `i` to the removal sequence).
        2. If `i + 1 < n`, flip `coins[i + 1]`.
        3. Because every coin in `[left .. i - 1]` is currently 'T', removing
           `i` flips `i - 1` to 'H', which cascades leftward: remove
           `i - 1`, `i - 2`, ..., `left` in order.
        4. Advance `left = i + 1` and continue scanning rightward.

Complexity:
    - Time Complexity:  O(n) — each coin is scanned and removed once.
    - Space Complexity: O(n) — for the working copy of coins and output list.
"""

from typing import List, Sequence, Tuple


def removeCoins(n: int, coins: Sequence[str]) -> Tuple[bool, List[int]]:
    """Determine if a row of coins can be cleared and return a removal sequence.

    Args:
        n: Number of coins in the line (n >= 0).
        coins: Sequence of length n containing 'H' (heads) or 'T' (tails).

    Returns:
        A tuple (possible, flips) where:
            - possible: True if all coins can be removed, False otherwise.
            - flips: 0-based indices of coins in the order they are removed
              (empty list if not possible or if n == 0).

    Raises:
        ValueError: If n is negative, len(coins) != n, or coins contains
            invalid characters.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if len(coins) != n:
        raise ValueError(f"Expected {n} coins, got {len(coins)}")

    state: List[str] = []
    heads_count = 0
    for idx, coin in enumerate(coins):
        c = coin.upper()
        if c not in ("H", "T"):
            raise ValueError(
                f"Invalid coin value {coin!r} at index {idx}; expected 'H' or 'T'"
            )
        state.append(c)
        if c == "H":
            heads_count += 1

    if n == 0:
        return True, []

    # A non-empty line of coins can be cleared iff the number of 'H' is odd.
    if heads_count % 2 == 0:
        return False, []

    flips: List[int] = []
    left = 0

    for i in range(n):
        if state[i] == "H":
            # Greedy choice: remove the leftmost heads-up coin at index i.
            flips.append(i)
            state[i] = "_"

            # Flip immediate right neighbor if present.
            if i + 1 < n and state[i + 1] != "_":
                state[i + 1] = "T" if state[i + 1] == "H" else "H"

            # Removing i flips i - 1 from 'T' to 'H', cascading all the way
            # back to `left`.
            for j in range(i - 1, left - 1, -1):
                flips.append(j)
                state[j] = "_"

            left = i + 1

    return True, flips


def verify_solution(n: int, coins: Sequence[str], flips: Sequence[int]) -> bool:
    """Simulate a removal sequence to verify it legally clears all coins."""
    if len(flips) != n:
        return False

    state = [c.upper() for c in coins]
    for idx in flips:
        if not (0 <= idx < n) or state[idx] != "H":
            return False
        state[idx] = "_"
        if idx - 1 >= 0 and state[idx - 1] != "_":
            state[idx - 1] = "T" if state[idx - 1] == "H" else "H"
        if idx + 1 < n and state[idx + 1] != "_":
            state[idx + 1] = "T" if state[idx + 1] == "H" else "H"

    return all(c == "_" for c in state)


def _run_demo() -> None:
    print("=" * 60)
    print("Task 1 - Coin Removal (Greedy)")
    print("=" * 60)

    sample_cases = [
        ("Case 1 (Odd heads - clearable)", list("THTHH")),
        ("Case 2 (Even heads - impossible)", list("THHTHH")),
        ("Case 3 (Single head at end)", list("TTTTH")),
        ("Case 4 (All heads, odd n=5)", list("HHHHH")),
    ]

    for label, coins in sample_cases:
        n = len(coins)
        possible, flips = removeCoins(n, coins)
        print(f"\n{label}")
        print(f"  Input:    n={n}, coins={coins}")
        print(f"  Possible: {possible}")
        print(f"  Flips:    {flips}")
        if possible:
            assert verify_solution(n, coins, flips), "Verification failed!"
            print("  Verified: Valid removal sequence.")


if __name__ == "__main__":
    _run_demo()
