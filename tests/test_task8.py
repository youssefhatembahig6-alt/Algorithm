"""Unit tests for Task 8 - Colored Tromino Tiling (Divide and Conquer)."""

import unittest

from tasks.task8_tromino import tileTromino, verify


class TestTask8TrominoTiling(unittest.TestCase):
    def test_sample_cases(self):
        cases = [(2, 0, 0), (3, 3, 4), (4, 15, 15)]
        for n, row, col in cases:
            tiles = tileTromino(n, row, col)
            self.assertEqual(len(tiles), (4 ** n - 1) // 3)
            self.assertTrue(verify(n, row, col, tiles))

    def test_every_hole_up_to_n4(self):
        for n in (2, 3, 4):
            size = 2 ** n
            for row in range(size):
                for col in range(size):
                    tiles = tileTromino(n, row, col)
                    self.assertTrue(verify(n, row, col, tiles))

    def test_n5_board(self):
        tiles = tileTromino(5, 13, 21)
        self.assertEqual(len(tiles), (4 ** 5 - 1) // 3)
        self.assertTrue(verify(5, 13, 21, tiles))

    def test_invalid_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            tileTromino(1, 0, 0)
        with self.assertRaises(ValueError):
            tileTromino(2, 4, 0)
        with self.assertRaises(ValueError):
            tileTromino(2, -1, 0)


if __name__ == "__main__":
    unittest.main()
