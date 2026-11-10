import math
import unittest

import numpy as np

from multichannel_state_weights import (
    calibration,
    canonical_star_weight,
    minimal_star_ceiling,
    star_bad_kernel,
    star_feasibility_expression,
    star_weight_certificate,
)


class StarKernelTests(unittest.TestCase):
    def test_kernel_has_declared_rows(self):
        matrix = star_bad_kernel([0.01, 0.02], [1.0, 0.8], [0.0, 0.1])
        self.assertEqual(matrix.shape, (3, 3))
        self.assertAlmostEqual(matrix[0].sum(), 0.03)
        self.assertAlmostEqual(matrix[2].sum(), 0.9)

    def test_superprobability_row_is_rejected(self):
        with self.assertRaises(ValueError):
            star_bad_kernel([0.8, 0.4], [1, 1], [0, 0])

    def test_persistence_at_target_is_impossible(self):
        with self.assertRaises(ValueError):
            canonical_star_weight(0.1, [1.0], [0.1])

    def test_forced_transition_creates_large_weight(self):
        weight = canonical_star_weight(0.01, [1.0], [0.0])
        self.assertAlmostEqual(weight[1], 100.0)


class ExactFeasibilityTests(unittest.TestCase):
    def test_two_state_formula_recovers_square_root(self):
        entry = 1.0e-6
        minimum = minimal_star_ceiling([entry], [1.0], [0.0])
        self.assertAlmostEqual(minimum, math.sqrt(entry), places=13)

    def test_multichannel_formula_recovers_total_square_root(self):
        entries = [1.0e-6, 3.0e-6]
        minimum = minimal_star_ceiling(entries, [1, 1], [0, 0])
        self.assertAlmostEqual(minimum, math.sqrt(sum(entries)), places=13)

    def test_root_expression_is_exact(self):
        q = 0.02
        entries = [q * q / 2, q * q / 2]
        expression = star_feasibility_expression(q, entries, [1, 1], [0, 0])
        self.assertAlmostEqual(expression, q)

    def test_weighted_ceiling_can_beat_scalar_ceiling(self):
        q = 0.02
        _, _, cert = star_weight_certificate(
            q, [q * q], [1.0], [0.0], 0.03
        )
        self.assertAlmostEqual(cert.scalar_row_ceiling, 1.0)
        self.assertAlmostEqual(cert.weighted_ceiling, q)
        self.assertTrue(cert.feasible)

    def test_excess_entry_rate_fails(self):
        q = 0.02
        _, _, cert = star_weight_certificate(
            q, [2.0 * q * q], [1.0], [0.0], 0.03
        )
        self.assertFalse(cert.feasible)


class CalibrationTests(unittest.TestCase):
    def test_four_channels_are_jointly_feasible(self):
        result = calibration()
        self.assertEqual(len(result["channels"]), 4)
        self.assertTrue(result["certificate"]["feasible"])
        self.assertAlmostEqual(
            result["minimal_weighted_ceiling"],
            result["target_weighted_ceiling"],
            places=13,
        )

    def test_entry_budget_is_q_squared(self):
        result = calibration()
        self.assertAlmostEqual(
            result["total_entry_budget"], result["target_weighted_ceiling"] ** 2
        )

    def test_topology_state_is_not_silently_claimed(self):
        result = calibration()
        self.assertFalse(result["topology_label_available_on_current_local_block"])
        self.assertFalse(result["physical_su2_entry_rates_proved"])


if __name__ == "__main__":
    unittest.main()
