"""Unit tests for Task 5 - King Arthur's Round Table (Dynamic Programming)."""

import unittest

from tasks.task5_round_table import seatKnights, verify_seating


class TestTask5RoundTable(unittest.TestCase):
    def test_triangle_n3(self):
        n = 3
        friends = [
            [False, True, True],
            [True, False, True],
            [True, True, False],
        ]
        seating = seatKnights(n, friends)
        self.assertTrue(verify_seating(n, friends, seating))

    def test_cycle_n4(self):
        n = 4
        friends = [
            [False, False, True, True],
            [False, False, True, True],
            [True, True, False, False],
            [True, True, False, False],
        ]
        seating = seatKnights(n, friends)
        self.assertTrue(verify_seating(n, friends, seating))

    def test_dirac_condition_n6(self):
        n = 6
        friends = [[False] * n for _ in range(n)]
        edges = [
            (0, 1), (1, 2), (2, 0),
            (3, 4), (4, 5), (5, 3),
            (0, 3), (1, 4), (2, 5),
        ]
        for u, v in edges:
            friends[u][v] = friends[v][u] = True

        seating = seatKnights(n, friends)
        self.assertTrue(verify_seating(n, friends, seating))

    def test_example_diagram_n8(self):
        n = 8
        friends = [[False] * n for _ in range(n)]
        for i in range(n):
            for step in (1, 2):
                neighbor = (i + step) % n
                friends[i][neighbor] = friends[neighbor][i] = True

        seating = seatKnights(n, friends)
        self.assertTrue(verify_seating(n, friends, seating))

    def test_impossible_seating_and_small_n(self):
        friends = [
            [False, True, True, True],
            [True, False, False, False],
            [True, False, False, False],
            [True, False, False, False],
        ]
        self.assertEqual(seatKnights(4, friends), [])
        self.assertEqual(seatKnights(2, [[False, True], [True, False]]), [])


if __name__ == "__main__":
    unittest.main()
