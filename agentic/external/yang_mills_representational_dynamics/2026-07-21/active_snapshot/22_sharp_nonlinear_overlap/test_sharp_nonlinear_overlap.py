import math
import unittest

import numpy as np

from sharp_nonlinear_overlap import (
    EXACT_ORIGIN_SECOND_DERIVATIVE,
    complete_local_certificate,
    exact_origin_second_derivative_norm,
    leverage_certificate,
    local_block_union_radius,
    maximal_certified_radius,
    maximal_old_certificate_radius,
    numerical_origin_mixed_hessian,
    origin_coefficient_matrix,
    origin_hessian_action,
    sharp_overlap_certificate,
)


class SharpOverlapTests(unittest.TestCase):
    def setUp(self):
        leverage = leverage_certificate()
        self.required = local_block_union_radius(
            216,
            12,
            3e-6 * leverage.max_four_link_variance_coefficient,
            0.0027927080803578997,
        )

    def test_origin_matrix_is_skew(self):
        matrix = origin_coefficient_matrix()
        self.assertTrue(np.allclose(matrix.T, -matrix))

    def test_exact_origin_norm(self):
        self.assertAlmostEqual(exact_origin_second_derivative_norm(), 1 + math.sqrt(2))
        self.assertAlmostEqual(EXACT_ORIGIN_SECOND_DERIVATIVE, exact_origin_second_derivative_norm())

    def test_quaternion_bracket_normalization_by_finite_difference(self):
        rng = np.random.default_rng(123)
        left = rng.normal(size=(4, 3))
        right = rng.normal(size=(4, 3))
        left /= np.linalg.norm(left)
        right /= np.linalg.norm(right)
        analytic = origin_hessian_action(left, right)
        numerical = numerical_origin_mixed_hessian(left, right, 2e-5)
        self.assertTrue(np.allclose(analytic, numerical, atol=2e-6))

    def test_refined_second_derivative_is_far_below_crude_bound(self):
        cert = sharp_overlap_certificate(self.required)
        self.assertLess(cert.refined_second_derivative_bound, 3.0)
        self.assertGreater(cert.crude_third_derivative_bound, 40.0)

    def test_required_radius_is_certified(self):
        cert = sharp_overlap_certificate(self.required)
        self.assertTrue(complete_local_certificate(cert))
        self.assertGreater(cert.generated_base_margin, 0.6)
        self.assertLess(cert.centered_transport_coefficient, 0.07)

    def test_required_hessian_remainder(self):
        cert = sharp_overlap_certificate(self.required)
        self.assertAlmostEqual(cert.total_hessian_remainder, 0.4746710865657404, places=11)

    def test_radial_heat_budget_is_small(self):
        cert = sharp_overlap_certificate(self.required)
        self.assertLess(cert.radial_action_budget, 2e-5)

    def test_budget_decomposition(self):
        cert = sharp_overlap_certificate(self.required)
        total = cert.metric_distortion_budget + cert.radial_action_budget + cert.curvature_chain_budget
        self.assertAlmostEqual(total, cert.total_hessian_remainder)

    def test_sharp_radius_exceeds_typical_radius(self):
        maximum = maximal_certified_radius()
        self.assertGreater(maximum, self.required)
        self.assertGreater(maximum / self.required, 1.8)

    def test_old_radius_is_below_typical_radius(self):
        self.assertLess(maximal_old_certificate_radius(), self.required)

    def test_eta_increases_on_frozen_range(self):
        radii = np.linspace(0.002, 0.012, 8)
        values = [sharp_overlap_certificate(float(r)).total_hessian_remainder for r in radii]
        self.assertTrue(all(left < right for left, right in zip(values, values[1:])))

    def test_large_radius_fails_base_coercivity(self):
        cert = sharp_overlap_certificate(0.02)
        self.assertFalse(cert.generated_base_coercive)

    def test_invalid_radius_rejected(self):
        with self.assertRaises(ValueError):
            sharp_overlap_certificate(0.0)

    def test_quotient_singular_floor_positive_at_required_radius(self):
        cert = sharp_overlap_certificate(self.required)
        self.assertGreater(cert.nonlinear_physical_singular_floor, 1.3)


if __name__ == "__main__":
    unittest.main()
