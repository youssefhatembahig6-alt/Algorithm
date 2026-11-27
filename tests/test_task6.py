"""Unit tests for Task 6 - Killing Squares (Dynamic Programming)."""

import unittest

from tasks.task6_killing_squares import breakAllSquares, verify_broken_squares


class TestTask6KillingSquares(unittest.TestCase):
    def test_zero_board(self):
        removed = breakAllSquares(0)
        self.assertEqual(removed, [])
        self.assertTrue(verify_broken_squares(0, removed))

    def test_known_minimum_counts_and_validity(self):
        # Known minimum toothpick removals to destroy all squares in an n x n grid:
        # n=1 -> 1, n=2 -> 3, n=3 -> 6, n=4 -> 9
        expected_min = {1: 1, 2: 3, 3: 6, 4: 9}
        for n, expected in expected_min.items():
            removed = breakAllSquares(n)
            self.assertEqual(
                len(removed), expected, f"Expected {expected} removals for n={n}"
            )
            self.assertTrue(
                verify_broken_squares(n, removed),
                f"Squares remain intact for n={n} with {removed}",
            )

    def test_invalid_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            breakAllSquares(-1)


if __name__ == "__main__":
    unittest.main()
