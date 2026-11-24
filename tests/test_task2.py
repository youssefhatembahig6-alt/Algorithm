"""Unit tests for Task 2 - Domino Tiling (Brute Force)."""

import unittest

from tasks.task2_domino_tiling import tileDominoes, verify_tiling


class TestTask2DominoTiling(unittest.TestCase):
    def test_report_sample_cases(self):
        # Case 1: 4x4 board from the PDF diagram
        ok1, doms1 = tileDominoes(4, (0, 0), (3, 2))
        self.assertTrue(ok1)
        self.assertTrue(verify_tiling(4, (0, 0), (3, 2), doms1))

        # Case 2: 3x3 odd board -> impossible (7 remaining squares)
        ok2, doms2 = tileDominoes(3, (0, 0), (0, 1))
        self.assertFalse(ok2)
        self.assertEqual(doms2, [])

        # Case 3: 6x6 board with opposite-color missing squares
        ok3, doms3 = tileDominoes(6, (0, 0), (5, 4))
        self.assertTrue(ok3)
        self.assertTrue(verify_tiling(6, (0, 0), (5, 4), doms3))

        # Case 4: 8x8 board with opposite-color missing squares
        ok4, doms4 = tileDominoes(8, (0, 1), (7, 7))
        self.assertTrue(ok4)
        self.assertTrue(verify_tiling(8, (0, 1), (7, 7), doms4))

    def test_all_odd_board_sizes_impossible(self):
        for n in (3, 5, 7):
            ok, doms = tileDominoes(n, (0, 0), (0, 1))
            self.assertFalse(ok)
            self.assertEqual(doms, [])

    def test_same_color_missing_squares_impossible(self):
        for n in (2, 4, 6, 8):
            ok, doms = tileDominoes(n, (0, 0), (n - 1, n - 1))
            self.assertFalse(ok)
            self.assertEqual(doms, [])

    def test_exhaustive_all_opposite_color_pairs_n2_n4_n6(self):
        """Verify Gomory's theorem on all opposite-color pairs for n = 2, 4, 6."""
        for n in (2, 4, 6):
            evens = [(r, c) for r in range(n) for c in range(n) if (r + c) % 2 == 0]
            odds = [(r, c) for r in range(n) for c in range(n) if (r + c) % 2 == 1]
            for m1 in evens:
                for m2 in odds:
                    ok, doms = tileDominoes(n, m1, m2)
                    self.assertTrue(ok, f"Expected tiling for n={n}, {m1}, {m2}")
                    self.assertTrue(
                        verify_tiling(n, m1, m2, doms),
                        f"Invalid tiling for n={n}, {m1}, {m2}",
                    )

    def test_exhaustive_n8_representative_and_tricky_pairs(self):
        pairs = [
            ((0, 0), (0, 1)),
            ((0, 0), (7, 6)),
            ((1, 7), (2, 7)),
            ((3, 3), (4, 3)),
            ((0, 7), (7, 7)),
            ((2, 2), (5, 4)),
        ]
        for m1, m2 in pairs:
            ok, doms = tileDominoes(8, m1, m2)
            self.assertTrue(ok, f"Expected tiling for n=8, {m1}, {m2}")
            self.assertTrue(verify_tiling(8, m1, m2, doms))

    def test_invalid_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            tileDominoes(1, (0, 0), (0, 0))
        with self.assertRaises(ValueError):
            tileDominoes(9, (0, 0), (0, 1))
        with self.assertRaises(ValueError):
            tileDominoes(4, (0, 0), (0, 0))
        with self.assertRaises(ValueError):
            tileDominoes(4, (-1, 0), (0, 1))
        with self.assertRaises(ValueError):
            tileDominoes(4, (0, 0), (4, 1))


if __name__ == "__main__":
    unittest.main()
