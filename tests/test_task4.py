"""Unit tests for Task 4 - Point Coloring (Iterative Improvement)."""

import random
import unittest

from tasks.task4_points import colorPoints, is_valid


class TestTask4PointColoring(unittest.TestCase):
    def test_empty_and_single_point(self):
        self.assertEqual(colorPoints(0, []), [])

        pts = [(3, 4)]
        colors = colorPoints(1, pts)
        self.assertEqual(len(colors), 1)
        self.assertIn(colors[0], ("B", "W"))
        self.assertTrue(is_valid(pts, colors))

    def test_sample_cases(self):
        cases = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(i, 0) for i in range(5)],
            [(0, i) for i in range(6)],
            [
                (0, 0), (1, 0), (2, 0), (0, 1), (2, 1),
                (1, 2), (2, 2), (3, 2), (3, 0), (3, 3),
            ],
        ]
        for pts in cases:
            colors = colorPoints(len(pts), pts)
            self.assertEqual(len(colors), len(pts))
            self.assertTrue(set(colors) <= {"B", "W"})
            self.assertTrue(is_valid(pts, colors))

    def test_randomized_grids(self):
        rng = random.Random(42)
        for _ in range(500):
            m = rng.randint(1, 50)
            size = rng.randint(2, 8)
            pts = list(
                {(rng.randrange(size), rng.randrange(size)) for _ in range(m)}
            )
            colors = colorPoints(len(pts), pts)
            self.assertTrue(is_valid(pts, colors))

    def test_duplicate_points_raise_value_error(self):
        with self.assertRaises(ValueError):
            colorPoints(2, [(1, 1), (1, 1)])


if __name__ == "__main__":
    unittest.main()
