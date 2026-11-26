import sys
from pathlib import Path
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tasks.task5_round_table import seatKnights


class TestSeatKnights(unittest.TestCase):
    
    def is_valid_seating(self, n: int, friends: list[list[bool]], seating: list[int]) -> bool:
        """Helper method to verify all constraints of a valid circular seating."""
        if len(seating) != n:
            return False
        # Must contain every knight exactly once
        if set(seating) != set(range(n)):
            return False
        # Every adjacent pair (including wrap-around) must be friends
        for i in range(n):
            u = seating[i]
            v = seating[(i + 1) % n]
            if not friends[u][v]:
                return False
        return True

    def test_triangle_n3(self):
        # 3 knights, everyone is friends with everyone
        n = 3
        friends = [
            [False, True,  True],
            [True,  False, True],
            [True,  True,  False]
        ]
        seating = seatKnights(n, friends)
        self.assertTrue(self.is_valid_seating(n, friends, seating))

    def test_cycle_n4(self):
        # 4 knights, each has 2 friends (minimum required: n/2 = 2)
        # Valid cycle: 0 - 2 - 1 - 3 - 0
        n = 4
        friends = [
            [False, False, True,  True],
            [False, False, True,  True],
            [True,  True,  False, False],
            [True,  True,  False, False]
        ]
        seating = seatKnights(n, friends)
        self.assertTrue(self.is_valid_seating(n, friends, seating))

    def test_dirac_condition_n6(self):
        # 6 knights, each has at least 3 friends (Dirac's theorem threshold)
        n = 6
        friends = [[False] * n for _ in range(n)]
        # Create a 3-regular graph (prism graph)
        edges = [
            (0, 1), (1, 2), (2, 0), # Triangle 1
            (3, 4), (4, 5), (5, 3), # Triangle 2
            (0, 3), (1, 4), (2, 5)  # Connecting edges
        ]
        for u, v in edges:
            friends[u][v] = friends[v][u] = True
            
        seating = seatKnights(n, friends)
        self.assertTrue(self.is_valid_seating(n, friends, seating))

    def test_example_diagram_n8(self):
        # 8 knights where each has 4 friends
        n = 8
        friends = [[False] * n for _ in range(n)]
        # Connect each knight to +/- 1 and +/- 2 neighbors
        for i in range(n):
            for step in [1, 2]:
                neighbor = (i + step) % n
                friends[i][neighbor] = friends[neighbor][i] = True
                
        seating = seatKnights(n, friends)
        self.assertTrue(self.is_valid_seating(n, friends, seating))

    def test_impossible_seating(self):
        # Edge case where Dirac's condition is violated and no cycle exists
        # 4 knights forming a star graph centered at 0
        n = 4
        friends = [
            [False, True,  True,  True],
            [True,  False, False, False],
            [True,  False, False, False],
            [True,  False, False, False]
        ]
        seating = seatKnights(n, friends)
        self.assertEqual(seating, [])


if __name__ == "__main__":
    unittest.main()
