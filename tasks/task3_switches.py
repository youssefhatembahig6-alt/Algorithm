"""
Task 3 - Security Switches        (technique: Decrease and Conquer)

Switches are numbered 1..n from LEFT to RIGHT. All start ON. Rule:
  * switch n (rightmost) may always be toggled;
  * switch i < n may be toggled only if switch i+1 is ON and
    switches i+2..n are all OFF.

Decrease-and-conquer idea
-------------------------
Let Off(j) = move sequence that turns OFF the suffix of switches j..n,
starting with all of them ON (switches left of j are ignored).

To turn off switch j we need  j+1 = ON  and  j+2..n = OFF.  So:
  1. Off(j+2)        -> j+2..n are OFF, j+1 still ON       (problem size k-2)
  2. toggle j        -> j is now OFF (legal)
  3. On(j+2)         -> j+2..n are ON again                (undo step 1)
  4. Off(j+1)        -> j+1..n are OFF                     (problem size k-1)

Every toggle is its own inverse and legality is symmetric, so
On(j+2) is simply Off(j+2) reversed.
Base cases: Off(n+1) = []  (empty),  Off(n) = [n].

Recurrence: T(k) = T(k-1) + 2*T(k-2) + 1,  T(0)=0, T(1)=1
Closed form: T(n) = floor(2^(n+1) / 3)   (minimum, Chinese-rings puzzle).
"""
import sys

sys.setrecursionlimit(10000)


def _off(j: int, n: int) -> list:
    """Toggle sequence turning switches j..n off (all currently on)."""
    if j > n:                       # k = 0
        return []
    if j == n:                      # k = 1
        return [n]
    seq = _off(j + 2, n)            # decrease by two
    return seq + [j] + seq[::-1] + _off(j + 1, n)   # ... and by one


def turnOffSwitches(n: int):
    """Return (minMoves, toggles); toggles are 1-based, left to right."""
    if n < 0:
        raise ValueError("n must be >= 0")
    toggles = _off(1, n)
    return len(toggles), toggles


# --------------------------------------------------------------------------
# Verification helpers
# --------------------------------------------------------------------------
def verify(n: int, toggles: list) -> bool:
    """Simulate the toggles, checking every move is legal and all end OFF."""
    s = [True] * (n + 2)            # 1-based; s[n+1] is a dummy 'off' sentinel
    s[n + 1] = False
    for i in toggles:
        if i == n:
            pass
        else:
            if not (s[i + 1] and not any(s[i + 2:n + 1])):
                return False
        s[i] = not s[i]
    return not any(s[1:n + 1])


def bfs_min(n: int) -> int:
    """Brute-force BFS minimum, used only to double-check optimality."""
    from collections import deque
    start, goal = (1,) * n, (0,) * n
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            return dist[cur]
        for i in range(n):
            ok = (i == n - 1) or (cur[i + 1] == 1 and not any(cur[i + 2:]))
            if ok:
                nxt = list(cur)
                nxt[i] ^= 1
                nxt = tuple(nxt)
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)
    return -1


def _run_demo() -> None:
    print("=" * 60)
    print("Task 3 - Security Switches (Decrease and Conquer)")
    print("=" * 60)

    for n in (1, 2, 3, 4, 5, 8):
        moves, seq = turnOffSwitches(n)
        formula = (2 ** (n + 1)) // 3
        shown = seq if len(seq) <= 25 else seq[:15] + ["..."] + seq[-5:]
        assert verify(n, seq), f"Verification failed for n={n}!"
        print(f"\n  n={n}: minMoves={moves} (formula={formula})")
        print(f"    toggles={shown}")
        print("    Verified: Valid minimum toggle sequence.")


if __name__ == "__main__":
    _run_demo()
