"""Unit tests for Task 7 - Poisoned Wine (Divide and Conquer)."""

import unittest

from tasks.task7_poison_test import (
    TOTAL_BARRELS,
    designWineTests,
    verify_wine_tests,
)


class TestTask7PoisonTest(unittest.TestCase):
    def test_insufficient_testers(self):
        for testers in (0, 1, 8, 9):
            possible, schedule, decoder = designWineTests(testers)
            self.assertFalse(possible)
            self.assertIsNone(schedule)
            self.assertIsNone(decoder)

    def test_minimum_sufficient_testers_10(self):
        possible, schedule, decoder = designWineTests(10)
        self.assertTrue(possible)
        self.assertIsNotNone(schedule)
        self.assertIsNotNone(decoder)
        self.assertEqual(len(schedule), 10)
        self.assertTrue(verify_wine_tests(10, schedule, decoder))

    def test_extra_testers(self):
        possible, schedule, decoder = designWineTests(12)
        self.assertTrue(possible)
        self.assertTrue(verify_wine_tests(12, schedule, decoder))

    def test_specific_bit_pattern_decoding(self):
        possible, _, decoder = designWineTests(10)
        self.assertTrue(possible)
        # Testers 0 and 2 die -> binary 0000000101 = barrel 5
        results = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(decoder(results), 5)

        # All 1000 barrels are within valid range
        for barrel in (0, 1, 511, 512, TOTAL_BARRELS - 1):
            bits = [(barrel >> t) & 1 for t in range(10)]
            self.assertEqual(decoder(bits), barrel)

    def test_invalid_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            designWineTests(-1)

        _, _, decoder = designWineTests(10)
        with self.assertRaises(ValueError):
            decoder([0, 1, 0])


if __name__ == "__main__":
    unittest.main()
