import math
import unittest

from chart_density_comparison import (
    calibration,
    density_comparison_certificate,
    gaussian_ball_log_mass,
    log_chi_square_cdf,
    radius_for_log_mass,
    radius_for_loss_target,
)


class GaussianMassTests(unittest.TestCase):
    def test_one_dimensional_cdf_matches_error_function(self):
        threshold = 2.3
        expected = math.erf(math.sqrt(threshold / 2.0))
        self.assertAlmostEqual(math.exp(log_chi_square_cdf(1, threshold)), expected, places=13)

    def test_deep_lower_tail_remains_finite_in_log_domain(self):
        value = log_chi_square_cdf(408, 3.0)
        self.assertTrue(math.isfinite(value))
        self.assertLess(value, -700.0)

    def test_ball_mass_increases_with_radius(self):
        a = gaussian_ball_log_mass(12, 1e-3, 0.05)
        b = gaussian_ball_log_mass(12, 1e-3, 0.08)
        self.assertLess(a, b)

    def test_invalid_mass_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            log_chi_square_cdf(0, 1.0)
        with self.assertRaises(ValueError):
            gaussian_ball_log_mass(3, -1.0, 1.0)


class ComparisonTests(unittest.TestCase):
    def test_oscillation_and_coverage_add_in_log_space(self):
        cert = density_comparison_certificate(2.0, 0.5, -3.0, 5, 1.0)
        self.assertAlmostEqual(cert.oscillation_loss, 0.5)
        self.assertAlmostEqual(cert.coverage_loss, 3.0)
        self.assertAlmostEqual(cert.total_log_comparison_loss, 3.5)

    def test_support_normalization_is_explicit(self):
        cert = density_comparison_certificate(1.0, 0.1, -1.0, 10, 0.2)
        self.assertAlmostEqual(cert.comparison_loss_per_support, 0.101)
        self.assertTrue(cert.target_met)

    def test_invalid_log_mass_fails_closed(self):
        with self.assertRaises(ValueError):
            density_comparison_certificate(1.0, 1.0, 0.1, 1)

    def test_comparison_does_not_promote_to_full_measure(self):
        cert = density_comparison_certificate(1.0, 0.1, -0.1, 1)
        self.assertFalse(cert.full_measure_certified)


class CalibrationTests(unittest.TestCase):
    def test_stage08_action_oscillation_is_small(self):
        result = calibration()
        self.assertLess(result.density_comparison.oscillation_loss, 1e-4)

    def test_certified_inner_ball_coverage_dominates_loss(self):
        result = calibration()
        self.assertGreater(result.density_comparison.coverage_loss, 800.0)
        self.assertFalse(result.density_comparison.target_met)

    def test_required_radius_is_a_diagnostic_enlargement(self):
        result = calibration()
        self.assertGreater(result.radius_enlargement_factor_for_loss_target, 8.0)
        self.assertFalse(result.stage08_chart_enlargement_certified)

    def test_radius_inverts_declared_log_mass(self):
        radius = radius_for_log_mass(20, 1e-3, -0.1)
        self.assertAlmostEqual(gaussian_ball_log_mass(20, 1e-3, radius), -0.1, places=10)

    def test_loss_radius_meets_boundary(self):
        radius = radius_for_loss_target(20, 1e-3, 0.5, 10, 0.2)
        loss = (0.5 * radius**2 - gaussian_ball_log_mass(20, 1e-3, radius)) / 10
        self.assertAlmostEqual(loss, 0.2, places=10)


if __name__ == "__main__":
    unittest.main()
