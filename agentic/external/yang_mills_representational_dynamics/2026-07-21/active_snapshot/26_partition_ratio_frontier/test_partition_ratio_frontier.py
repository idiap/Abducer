import math
import unittest

import numpy as np

from partition_ratio_frontier import (
    calibration,
    entropy_cancellation_counterexample,
    exact_weighted_bad_ratios,
    free_energy_certificate,
    partition_ratio_certificate,
    retained_state_counterexample,
)


class ExactRatioTests(unittest.TestCase):
    def test_full_normalizer_formula(self):
        ratios = exact_weighted_bad_ratios([1.0], [1.0], [2.0], [2.0])
        self.assertAlmostEqual(ratios[0], 0.5)

    def test_zero_mass_state_is_rejected(self):
        with self.assertRaises(ValueError):
            exact_weighted_bad_ratios([0.0], [0.0], [0.0], [1.0])

    def test_negative_partition_is_rejected(self):
        with self.assertRaises(ValueError):
            exact_weighted_bad_ratios([1.0], [-0.1], [0.0], [1.0])

    def test_certificate_takes_supremum_over_states(self):
        cert = partition_ratio_certificate(
            [1.0, 1.0], [0.0, 1.0], [0.1, 1.0], [1.0, 1.0], 0.4
        )
        self.assertAlmostEqual(cert.maximum_exact_weighted_bad_ratio, 0.5)
        self.assertFalse(cert.target_met)


class FreeEnergyTests(unittest.TestCase):
    def test_required_charge_is_exact(self):
        ell = 0.03
        q = 0.002
        cert = free_energy_certificate(ell, ell - math.log(q), q)
        self.assertAlmostEqual(cert.implied_weighted_ceiling, q)
        self.assertFalse(cert.strict_target_met)

    def test_extra_charge_gives_strict_margin(self):
        cert = free_energy_certificate(0.02, 7.0, 0.002)
        self.assertTrue(cert.strict_target_met)

    def test_invalid_target_is_rejected(self):
        with self.assertRaises(ValueError):
            free_energy_certificate(0.0, 1.0, 1.0)


class CounterexampleTests(unittest.TestCase):
    def test_entropy_can_cancel_large_action_charge(self):
        result = entropy_cancellation_counterexample(10.0)
        self.assertGreater(result["bad_probability"], 0.49)
        self.assertFalse(result["action_charge_alone_controls_probability"])

    def test_retained_state_supremum_is_essential(self):
        result = retained_state_counterexample()
        self.assertLess(result["first_state_bad_ratio"], 1e-8)
        self.assertAlmostEqual(result["second_state_bad_ratio"], 0.5)
        self.assertTrue(result["boundary_uniform_normalizer_control_required"])


class FrontierCalibrationTests(unittest.TestCase):
    def test_required_charge_is_finite(self):
        result = calibration()
        self.assertGreater(result["required_uniform_charged_free_energy"], 6.0)
        self.assertLess(result["required_uniform_charged_free_energy"], 8.0)

    def test_finite_kernel_existence_does_not_close_uniform_bound(self):
        result = calibration()
        self.assertTrue(result["finite_compact_positive_su2_conditional_kernel_exists"])
        self.assertFalse(result["uniform_physical_partition_ratio_bound_proved"])

    def test_no_basin_or_mass_gap_promotion(self):
        result = calibration()
        self.assertFalse(result["volume_uniform_one_scale_basin_entry_proved"])
        self.assertIn("Osterwalder-Schrader Hamiltonian gap", result["not_implied"])


if __name__ == "__main__":
    unittest.main()
