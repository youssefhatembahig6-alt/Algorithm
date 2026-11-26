"""Unit tests for Task 5 - King Arthur's Round Table (Dynamic Programming)."""

import random
import unittest
from typing import List

from tasks.task5_round_table import seatKnights, verify_seating


def make_complete_graph(n: int) -> List[List[bool]]:
    """Generate adjacency matrix for complete graph K_n."""
    return [[i != j for j in range(n)] for i in range(n)]


def make_cycle_with_chords(n: int, chord_distance: int = 1) -> List[List[bool]]:
    """Generate an n-knight graph where each knight is friends with neighbors within chord_distance."""
    matrix = [[False] * n for _ in range(n)]
    for i in range(n):
        for d in range(1, chord_distance + 1):
            matrix[i][(i + d) % n] = True
            matrix[i][(i - d) % n] = True
    return matrix


class TestTask5RoundTable(unittest.TestCase):
    def test_invalid_inputs_raise_errors(self):
        # n <= 2
        with self.assertRaises(ValueError):
            seatKnights(2, [[False, True], [True, False]])
        with self.assertRaises(ValueError):
            seatKnights(0, [])
        with self.assertRaises(ValueError):
            seatKnights(-3, [])
        with self.assertRaises(TypeError):
            seatKnights(3.5, [[False] * 3 for _ in range(3)])  # type: ignore

        # Dimension mismatch
        with self.assertRaises(ValueError):
            seatKnights(3, [[False, True], [True, False]])  # 2 rows instead of 3
        with self.assertRaises(ValueError):
            seatKnights(3, [[False, True, True], [True, False], [True, True, False]])

        # Asymmetric matrix (friendship must be mutual)
        asym = [[False, True, False], [False, False, True], [True, False, False]]
        with self.assertRaises(ValueError):
            seatKnights(3, asym)

    def test_triangle_n3(self):
        # Smallest valid input: n = 3
        # Complete triangle: all 3 are friends
        friends = make_complete_graph(3)
        seating = seatKnights(3, friends)
        self.assertEqual(len(seating), 3)
        self.assertTrue(verify_seating(3, friends, seating))

        # Triangle where degree condition is not satisfied and no cycle
        # e.g., 0-1 are friends, but 2 has no friends
        sparse = [
            [False, True, False],
            [True, False, False],
            [False, False, False],
        ]
        self.assertEqual(seatKnights(3, sparse), [])

    def test_complete_graphs(self):
        for n in (4, 5, 6, 7, 8):
            friends = make_complete_graph(n)
            seating = seatKnights(n, friends)
            self.assertEqual(len(seating), n)
            self.assertTrue(
                verify_seating(n, friends, seating),
                f"Failed on complete graph K_{n}",
            )

    def test_tight_dirac_degree_even_and_odd(self):
        # n = 4: min degree = 2 (n / 2 = 2.0). A simple 4-cycle C_4
        c4 = make_cycle_with_chords(4, chord_distance=1)
        seating_c4 = seatKnights(4, c4)
        self.assertEqual(len(seating_c4), 4)
        self.assertTrue(verify_seating(4, c4, seating_c4))

        # n = 5: min degree = 3 (ceil(5 / 2) = 3). Cycle C_5 with chords distance 1 and 2 (K_5 - no chords missing)
        c5 = make_cycle_with_chords(5, chord_distance=2)
        seating_c5 = seatKnights(5, c5)
        self.assertEqual(len(seating_c5), 5)
        self.assertTrue(verify_seating(5, c5, seating_c5))

        # n = 6: min degree = 3 (n / 2 = 3.0). Cycle C_6 plus opposite chords
        c6 = [[False] * 6 for _ in range(6)]
        for i in range(6):
            c6[i][(i + 1) % 6] = c6[(i + 1) % 6][i] = True
            c6[i][(i + 3) % 6] = c6[(i + 3) % 6][i] = True
        # Verify min degree is exactly 3
        for i in range(6):
            self.assertEqual(sum(c6[i]), 3)
        seating_c6 = seatKnights(6, c6)
        self.assertEqual(len(seating_c6), 6)
        self.assertTrue(verify_seating(6, c6, seating_c6))

        # n = 8: min degree = 4 (n / 2 = 4.0). Cycle C_8 with chord distance 2
        c8 = make_cycle_with_chords(8, chord_distance=2)
        for i in range(8):
            self.assertEqual(sum(c8[i]), 4)
        seating_c8 = seatKnights(8, c8)
        self.assertEqual(len(seating_c8), 8)
        self.assertTrue(verify_seating(8, c8, seating_c8))

    def test_pdf_illustration_case(self):
        """Case illustrated in Task 5 of the project PDF: 8 knights around a round table."""
        n = 8
        # Knights with friends +/- 1 and chords (e.g. +/- 2 and diameter)
        friends = [[False] * n for _ in range(n)]
        for i in range(n):
            for delta in (1, 2, 4):
                friends[i][(i + delta) % n] = friends[(i + delta) % n][i] = True

        seating = seatKnights(n, friends)
        self.assertEqual(len(seating), n)
        self.assertTrue(verify_seating(n, friends, seating))

    def test_impossible_graphs_return_empty(self):
        # Two disconnected cliques K_3 and K_3 (n = 6, degree = 2 < 3)
        friends = [[False] * 6 for _ in range(6)]
        for i in range(3):
            for j in range(3):
                if i != j:
                    friends[i][j] = True
        for i in range(3, 6):
            for j in range(3, 6):
                if i != j:
                    friends[i][j] = True

        self.assertEqual(seatKnights(6, friends), [])

        # Star graph S_5: center 0 connected to 1, 2, 3, 4, but leaves have degree 1 < 2.5
        star = [[False] * 5 for _ in range(5)]
        for i in range(1, 5):
            star[0][i] = star[i][0] = True
        self.assertEqual(seatKnights(5, star), [])

    def test_random_dirac_graphs(self):
        """Generate random graphs guaranteed to satisfy Dirac's condition deg >= n/2."""
        rng = random.Random(42)
        for n in (4, 5, 6, 7, 8, 9, 10):
            req_deg = (n + 1) // 2
            # Start with a Hamiltonian cycle to guarantee connectedness, then add random edges until min degree >= n/2
            perm = list(range(n))
            rng.shuffle(perm)
            mat = [[False] * n for _ in range(n)]
            for i in range(n):
                u, v = perm[i], perm[(i + 1) % n]
                mat[u][v] = mat[v][u] = True

            # Add edges until each vertex has at least req_deg
            for u in range(n):
                while sum(mat[u]) < req_deg:
                    candidates = [v for v in range(n) if v != u and not mat[u][v]]
                    if not candidates:
                        break
                    v = rng.choice(candidates)
                    mat[u][v] = mat[v][u] = True

            seating = seatKnights(n, mat)
            self.assertEqual(len(seating), n, f"Failed for Dirac random graph with n={n}")
            self.assertTrue(
                verify_seating(n, mat, seating),
                f"Invalid seating for Dirac random graph with n={n}",
            )

    def test_moderate_scale_dp(self):
        """Test DP on moderate sizes (n = 12 and n = 14) to verify performance."""
        for n in (12, 14):
            friends = make_cycle_with_chords(n, chord_distance=n // 4 + 1)
            seating = seatKnights(n, friends)
            self.assertEqual(len(seating), n)
            self.assertTrue(verify_seating(n, friends, seating))

    def test_large_scale_fallback(self):
        """Test n > 20 to ensure polynomial Dirac fallback executes properly."""
        n = 26
        friends = make_cycle_with_chords(n, chord_distance=n // 4 + 1)
        seating = seatKnights(n, friends)
        self.assertEqual(len(seating), n)
        self.assertTrue(verify_seating(n, friends, seating))


if __name__ == "__main__":
    unittest.main()
