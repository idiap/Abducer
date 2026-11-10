import math
import unittest

from one_scale_kr_composition import (
    calibration,
    kr_composition_certificate,
    local_reference_budget,
    radius_for_reference_share,
)


TARGET = 0.002430277501841998
CRITICAL = 0.0027927080803578997


class CompositionTheoremTests(unittest.TestCase):
    def test_positive_kernel_bounds_add(self):
        cert = kr_composition_certificate(0.1, 0.001, 0.0005, 0.002, 0.003)
        self.assertAlmostEqual(cert.combined_weighted_ceiling, math.exp(0.1) * 0.001 + 0.0005)

    def test_supercritical_sum_fails_target(self):
        cert = kr_composition_certificate(0.0, 0.0015, 0.001, 0.002, 0.003)
        self.assertFalse(cert.target_met)

    def test_negative_component_is_rejected(self):
        with self.assertRaises(ValueError):
            kr_composition_certificate(0.0, -0.1, 0.0, 0.2, 0.3)

    def test_invalid_ceiling_order_is_rejected(self):
        with self.assertRaises(ValueError):
            kr_composition_certificate(0.0, 0.1, 0.1, 0.3, 0.2)

    def test_physical_realization_is_not_implicit(self):
        cert = kr_composition_certificate(0.0, 0.001, 0.001, 0.0025, 0.003)
        self.assertFalse(cert.physical_kernel_decomposition_verified)


class RadiusBudgetTests(unittest.TestCase):
    def test_reference_budget_decreases_with_radius(self):
        small = local_reference_budget(0.0062)[2]
        large = local_reference_budget(0.0070)[2]
        self.assertGreater(small, large)

    def test_half_share_is_solved(self):
        radius = radius_for_reference_share(TARGET, 0.5)
        corrected = local_reference_budget(radius)[2]
        self.assertAlmostEqual(corrected, TARGET / 2.0, places=13)

    def test_selected_radius_is_inside_nonlinear_window(self):
        result = calibration()
        self.assertLess(result["selected_local_radius"], result["maximum_nonlinear_radius"])

    def test_residual_budget_is_positive(self):
        result = calibration()
        self.assertGreater(result["certificate"]["residual_bad_ceiling"], 0.0)
        self.assertTrue(result["nonempty_feasible_budget_region"])


class CalibrationTests(unittest.TestCase):
    def test_composed_target_is_met(self):
        result = calibration()
        cert = result["certificate"]
        self.assertTrue(cert["target_met"])
        self.assertTrue(cert["strict_cluster_subcritical"])
        self.assertAlmostEqual(cert["combined_weighted_ceiling"], TARGET, places=13)

    def test_equal_channel_budget_sums_to_square(self):
        result = calibration()
        self.assertAlmostEqual(
            4.0 * result["four_channel_equal_entry_budget"],
            result["four_channel_alternating_total_entry_budget"],
        )

    def test_full_su2_claim_remains_open(self):
        self.assertFalse(calibration()["full_su2_k_plus_r_inequality_proved"])


if __name__ == "__main__":
    unittest.main()
