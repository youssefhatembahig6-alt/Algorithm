"""Task 7 - Poisoned Wine (Required technique: Divide and Conquer).

Problem:
    One of 1,000 wine barrels is poisoned. Any amount of the poison causes
    death exactly 30 days after tasting. A king has a feast in five weeks
    (35 days) and may use ten testers. Determine whether he can identify the
    barrel in time, whether eight testers would also suffice, and construct
    testing plans that allow the poisoned barrel to be identified.

Divide and Conquer Strategy:
    - Because 5 weeks = 35 days and the poison takes 30 days, only ONE round
      of simultaneous testing is possible (35 < 60 days). Each tester yields
      one binary outcome (alive = 0, dead = 1), so `k` testers can distinguish
      at most 2^k barrels.
    - 10 testers suffice since 2^10 = 1024 >= 1000; 8 testers do NOT suffice
      since 2^8 = 256 < 1000.
    - Divide: recursively split the current interval of barrels `[lo, hi)`
      into two halves: left half `[lo, mid)` and right half `[mid, hi)`.
      Assign the current level's tester to taste all barrels in the right half.
    - Conquer: recursively apply the next tester to both halves independently
      (in parallel, since all tastings happen in the single round).
    - Combine (Decode): start with the full interval `[0, 2^testers)` and,
      for each tester from top level down, discard the left half if the tester
      died (1) or the right half if the tester survived (0) until a single
      barrel remains.

Complexity:
    - Time Complexity:  O(testers * barrels) = O(B log B) to build the
      schedule; O(testers) = O(log B) to decode the poisoned barrel.
    - Space Complexity: O(testers * barrels) = O(B log B) to store the
      testing schedule.
"""

from typing import Callable, Dict, List, Optional, Sequence, Tuple

TOTAL_BARRELS = 1000


def designWineTests(
    testers: int,
) -> Tuple[bool, Optional[Dict[int, List[int]]], Optional[Callable[[Sequence[int]], int]]]:
    """Design a single-round divide-and-conquer testing plan for 1,000 barrels.

    Args:
        testers: Number of available wine testers (testers >= 0).

    Returns:
        A tuple (possible, schedule, decoder):
            - possible: True if 2^testers >= 1000, else False.
            - schedule: Dict mapping tester index -> list of barrel indices
              (None if not possible).
            - decoder: Callable taking a sequence of 0/1 outcomes (1 = died)
              and returning the 0-based poisoned barrel index (None if not
              possible).

    Raises:
        ValueError: If testers < 0.
    """
    if testers < 0:
        raise ValueError(f"testers must be non-negative, got {testers}")

    barrels = TOTAL_BARRELS
    capacity = 1 << testers

    # Only 1 round fits in 5 weeks (35 days < 2 * 30 days), so 2^testers >= 1000 is required.
    if capacity < barrels:
        return False, None, None

    # Step 1 (Divide & Conquer): recursively bisect [0, 2^testers) by level.
    schedule: Dict[int, List[int]] = {t: [] for t in range(testers)}

    def divide_and_assign(level: int, lo: int, hi: int) -> None:
        if level < 0 or lo >= barrels:
            return
        mid = (lo + hi) // 2
        # Tester `level` tastes all valid barrels in the right half [mid, hi).
        for barrel in range(mid, min(hi, barrels)):
            schedule[level].append(barrel)
        divide_and_assign(level - 1, lo, mid)
        divide_and_assign(level - 1, mid, hi)

    divide_and_assign(testers - 1, 0, capacity)

    # Step 2 (Binary-search decoder): halve [0, 2^testers) using each tester's outcome.
    def decoder(results: Sequence[int]) -> int:
        if len(results) != testers:
            raise ValueError(
                f"Expected {testers} test results, got {len(results)}"
            )
        lo, hi = 0, capacity
        for level in range(testers - 1, -1, -1):
            mid = (lo + hi) // 2
            if results[level] == 1:  # Tester died -> poisoned barrel is in right half
                lo = mid
            else:                    # Tester survived -> poisoned barrel is in left half
                hi = mid
        return lo

    return True, schedule, decoder


def verify_wine_tests(
    testers: int,
    schedule: Dict[int, List[int]],
    decoder: Callable[[Sequence[int]], int],
) -> bool:
    """Verify that every barrel 0..999 is uniquely and accurately decoded."""
    for poisoned in range(TOTAL_BARRELS):
        results = [1 if poisoned in schedule[t] else 0 for t in range(testers)]
        if decoder(results) != poisoned:
            return False
    return True


def _run_demo() -> None:
    print("=" * 60)
    print("Task 7 - Poisoned Wine (Divide and Conquer)")
    print("=" * 60)

    for testers in (8, 9, 10):
        possible, schedule, decoder = designWineTests(testers)
        print(f"\nTesters = {testers} (capacity 2^{testers} = {2 ** testers})")
        print(f"  Possible: {possible}")
        if possible and schedule is not None and decoder is not None:
            sample_barrel = 357
            results = [
                1 if sample_barrel in schedule[t] else 0
                for t in range(testers)
            ]
            decoded = decoder(results)
            assert decoded == sample_barrel
            assert verify_wine_tests(testers, schedule, decoder)
            print(f"  Sample poisoned barrel: {sample_barrel}")
            print(f"  Tester outcomes (1=died): {results}")
            print(f"  Decoded barrel: {decoded}")
            print("  Verified: All 1,000 barrels decode uniquely.")


if __name__ == "__main__":
    _run_demo()
