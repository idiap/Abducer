import math
import unittest

from good_collar_coherence import (
    calibration,
    center_frustration_coherence_radius,
    commuting_minimizer,
    commuting_stress_certificate,
    good_collar_rate_certificate,
)


class GoodCollarRateTests(unittest.TestCase):
    def test_stage09_witness_has_positive_rate_gap(self):
        cert = good_collar_rate_certificate()
        self.assertTrue(cert.rate_concentration_certified)
        self.assertAlmostEqual(cert.uniform_rate_gap_lower, 0.0082**2 - 6e-6)

    def test_threshold_is_rho_over_sqrt_degree(self):
        cert = good_collar_rate_certificate()
        self.assertAlmostEqual(cert.admissible_coherence_threshold, 0.0082 / math.sqrt(6))

    def test_boundary_threshold_is_not_certified(self):
        eta = 0.0082 / math.sqrt(6)
        cert = good_collar_rate_certificate(coherence_radius=eta)
        self.assertFalse(cert.rate_concentration_certified)
        self.assertAlmostEqual(cert.uniform_rate_gap_lower, 0.0, places=18)

    def test_gap_decreases_with_coherence_radius(self):
        small = good_collar_rate_certificate(coherence_radius=0.0005)
        large = good_collar_rate_certificate(coherence_radius=0.001)
        self.assertGreater(small.uniform_rate_gap_lower, large.uniform_rate_gap_lower)

    def test_more_staples_require_tighter_coherence(self):
        low = good_collar_rate_certificate(incident_staples=4)
        high = good_collar_rate_certificate(incident_staples=6)
        self.assertGreater(low.admissible_coherence_threshold, high.admissible_coherence_threshold)

    def test_invalid_inputs_fail_closed(self):
        for kwargs in (
            {"curvature_radius": 0.0},
            {"coherence_radius": -1.0},
            {"incident_staples": 1},
            {"curvature_radius": math.pi},
        ):
            with self.assertRaises(ValueError):
                good_collar_rate_certificate(**kwargs)


class CommutingCalibrationTests(unittest.TestCase):
    def test_commuting_minimizer_is_negative_mean(self):
        angles = (-0.1, 0.1, 0.1)
        minimizer, deviations = commuting_minimizer(angles)
        self.assertAlmostEqual(minimizer, -sum(angles) / 3)
        self.assertAlmostEqual(max(deviations), 4 / 30)

    def test_extreme_box_enumeration_is_sharp(self):
        cert = commuting_stress_certificate()
        self.assertEqual(cert.extreme_assignments_checked, 64)
        self.assertAlmostEqual(cert.worst_target_deviation, cert.exact_box_bound)

    def test_scalar_bound_is_better_than_general_metric_bound(self):
        cert = commuting_stress_certificate()
        self.assertLess(cert.exact_box_bound, cert.general_metric_bound)

    def test_nonconvex_commuting_chart_rejected(self):
        with self.assertRaises(ValueError):
            commuting_minimizer((math.pi / 2, 0.0))


class ScopeAndObstructionTests(unittest.TestCase):
    def test_center_frustration_is_far_outside_uv_collar(self):
        self.assertAlmostEqual(center_frustration_coherence_radius(), math.pi / 2)
        self.assertGreater(center_frustration_coherence_radius(), 0.001)

    def test_calibration_excludes_stage10_boundary(self):
        cert = calibration()
        self.assertTrue(cert.center_frustration_excluded)
        self.assertGreater(cert.negative_log_proxy, 0.0)

    def test_no_false_full_measure_promotion(self):
        cert = calibration().rate_certificate
        self.assertFalse(cert.collar_failure_probability_certified)
        self.assertFalse(cert.full_measure_certified)


if __name__ == "__main__":
    unittest.main()

