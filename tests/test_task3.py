"""Unit tests for Task 3 - Security Switches (Decrease and Conquer)."""

import unittest

from tasks.task3_switches import bfs_min, turnOffSwitches, verify


class TestTask3SecuritySwitches(unittest.TestCase):
    def test_base_cases(self):
        moves0, seq0 = turnOffSwitches(0)
        self.assertEqual(moves0, 0)
        self.assertEqual(seq0, [])
        self.assertTrue(verify(0, seq0))

        moves1, seq1 = turnOffSwitches(1)
        self.assertEqual(moves1, 1)
        self.assertEqual(seq1, [1])
        self.assertTrue(verify(1, seq1))

    def test_closed_form_and_validity(self):
        for n in range(1, 13):
            moves, seq = turnOffSwitches(n)
            expected = (2 ** (n + 1)) // 3
            self.assertEqual(moves, expected, f"Move count mismatch for n={n}")
            self.assertEqual(len(seq), moves)
            self.assertTrue(verify(n, seq), f"Invalid sequence for n={n}")

    def test_optimality_against_bfs(self):
        for n in range(1, 10):
            moves, _ = turnOffSwitches(n)
            self.assertEqual(moves, bfs_min(n), f"Non-optimal for n={n}")

    def test_invalid_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            turnOffSwitches(-1)


if __name__ == "__main__":
    unittest.main()
