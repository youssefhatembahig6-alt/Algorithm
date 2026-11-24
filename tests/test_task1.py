"""Unit tests for Task 1 - Coin Removal (Greedy)."""

import itertools
import unittest

from tasks.task1_coin_removal import removeCoins, verify_solution


class TestTask1CoinRemoval(unittest.TestCase):
    def test_empty_row(self):
        possible, flips = removeCoins(0, [])
        self.assertTrue(possible)
        self.assertEqual(flips, [])

    def test_single_coin(self):
        possible_h, flips_h = removeCoins(1, ["H"])
        self.assertTrue(possible_h)
        self.assertEqual(flips_h, [0])
        self.assertTrue(verify_solution(1, ["H"], flips_h))

        possible_t, flips_t = removeCoins(1, ["T"])
        self.assertFalse(possible_t)
        self.assertEqual(flips_t, [])

    def test_report_sample_cases(self):
        # Case 1: Odd number of heads -> clearable
        coins1 = list("THTHH")
        possible1, flips1 = removeCoins(len(coins1), coins1)
        self.assertTrue(possible1)
        self.assertTrue(verify_solution(len(coins1), coins1, flips1))

        # Case 2: Even number of heads (PDF illustration row) -> impossible
        coins2 = list("THHTHH")
        possible2, flips2 = removeCoins(len(coins2), coins2)
        self.assertFalse(possible2)
        self.assertEqual(flips2, [])

        # Case 3: Single head at the far right -> full cascade left
        coins3 = list("TTTTH")
        possible3, flips3 = removeCoins(len(coins3), coins3)
        self.assertTrue(possible3)
        self.assertEqual(flips3, [4, 3, 2, 1, 0])
        self.assertTrue(verify_solution(len(coins3), coins3, flips3))

    def test_lowercase_input_supported(self):
        coins = list("tht")
        possible, flips = removeCoins(3, coins)
        self.assertTrue(possible)
        self.assertTrue(verify_solution(3, coins, flips))

    def test_exhaustive_all_rows_up_to_length_10(self):
        """Exhaustively verify all 2^n rows for 1 <= n <= 10."""
        for n in range(1, 11):
            for row in itertools.product(("H", "T"), repeat=n):
                heads = row.count("H")
                possible, flips = removeCoins(n, row)
                expected = heads % 2 == 1
                self.assertEqual(possible, expected, f"Failed on {row}")
                if expected:
                    self.assertTrue(
                        verify_solution(n, row, flips),
                        f"Invalid flip sequence {flips} for {row}",
                    )
                else:
                    self.assertEqual(flips, [])

    def test_large_input_linear_time(self):
        n = 10_000
        coins = ["T"] * (n - 1) + ["H"]
        possible, flips = removeCoins(n, coins)
        self.assertTrue(possible)
        self.assertEqual(len(flips), n)
        self.assertTrue(verify_solution(n, coins, flips))

    def test_invalid_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            removeCoins(-1, [])
        with self.assertRaises(ValueError):
            removeCoins(3, ["H", "T"])
        with self.assertRaises(ValueError):
            removeCoins(2, ["H", "X"])


if __name__ == "__main__":
    unittest.main()
