import math
import unittest

from coherent_partition_optimizer import (
    HEAT_TIME,
    STAGE26_RESIDUAL_CEILING,
    TARGET_WEIGHTED_CEILING,
    calibration,
    curvature_threshold,
    joint_kr_certificate,
    log_conditional_bound,
    optimize_delta,
    stationary_delta,
    stationarity_balance,
)


class CoherentOptimizerTests(unittest.TestCase):
    def test_stationary_delta_ideal(self):
        delta, left, right = stationary_delta(HEAT_TIME, 0.0)
        self.assertLess(left, delta)
        self.assertLess(delta, right)
        self.assertAlmostEqual(delta, math.sqrt(HEAT_TIME / 2.0), delta=2.0e-9)

    def test_stationarity_residual(self):
        cert = optimize_delta(HEAT_TIME, 0.015, 0.001)
        self.assertAlmostEqual(cert.stationarity_left, cert.stationarity_right, places=7)
        self.assertLess(abs(cert.stationarity_residual), 1.0e-6)

    def test_local_minimum(self):
        cert = optimize_delta(HEAT_TIME, 0.015, 0.001)
        d = cert.selected_delta
        center = cert.log_probability_upper
        self.assertGreater(log_conditional_bound(HEAT_TIME, 0.015, 0.001, 0.99 * d), center)
        self.assertGreater(log_conditional_bound(HEAT_TIME, 0.015, 0.001, 1.01 * d), center)

    def test_matches_stage15_frozen_value(self):
        cert = optimize_delta(HEAT_TIME, 0.0082, 0.001)
        self.assertAlmostEqual(cert.log_probability_upper, 14.9745316916, places=8)

    def test_old_radius_does_not_close(self):
        cert = optimize_delta(HEAT_TIME, 2 * 0.00614955590043087, 0.001)
        self.assertEqual(cert.probability_upper, 1.0)

    def test_declared_threshold_hits_target(self):
        cert = curvature_threshold(STAGE26_RESIDUAL_CEILING, 0.001)
        self.assertAlmostEqual(cert.attained_log_bound, math.log(STAGE26_RESIDUAL_CEILING), places=10)
        self.assertTrue(cert.below_maximum_nonlinear_radius)

    def test_ideal_threshold_is_smaller(self):
        ideal = curvature_threshold(STAGE26_RESIDUAL_CEILING, 0.0)
        declared = curvature_threshold(STAGE26_RESIDUAL_CEILING, 0.001)
        self.assertLess(ideal.selected_curvature_radius, declared.selected_curvature_radius)

    def test_threshold_monotonicity_audit(self):
        self.assertTrue(curvature_threshold(0.01, 0.001).monotone_grid_verified)

    def test_joint_kr_closes_strictly(self):
        cert = joint_kr_certificate()
        self.assertTrue(cert.strict_target_met)
        self.assertLess(cert.combined_ceiling, TARGET_WEIGHTED_CEILING)

    def test_joint_radius_inside_window(self):
        cert = joint_kr_certificate()
        self.assertTrue(cert.radius_inside_nonlinear_window)
        self.assertLess(cert.selected_local_radius, cert.maximum_nonlinear_radius)

    def test_joint_claim_boundary(self):
        cert = joint_kr_certificate()
        self.assertFalse(cert.collar_occurrence_certified)
        self.assertFalse(cert.physical_kernel_decomposition_certified)

    def test_calibration(self):
        data = calibration()
        self.assertTrue(data["coherent_channel_budget_closed_conditionally"])
        self.assertFalse(data["full_nonlinear_su2_partition_ratio_proved"])

    def test_balance_invalid(self):
        with self.assertRaises(ValueError):
            stationarity_balance(-1.0, HEAT_TIME, 0.001, 6)

    def test_target_invalid(self):
        for target in (0.0, 1.0, math.nan):
            with self.assertRaises(ValueError):
                curvature_threshold(target, 0.001)

    def test_inadmissible_curvature(self):
        with self.assertRaises(ValueError):
            optimize_delta(HEAT_TIME, 0.002, 0.001)


if __name__ == "__main__":
    unittest.main()
