import math
import unittest

import numpy as np

from dependent_gaussian_polymers import (
    curvature_projection,
    joint_tail_certificate,
    maximum_heat_time,
    polymer_certificate,
    projection_certificate,
    radial_gaussian_rate,
)


class ProjectionTests(unittest.TestCase):
    def test_projection_rank_and_dimensions(self):
        cert = projection_certificate()
        self.assertEqual(cert.scalar_curvature_rank, 136)
        self.assertEqual(cert.color_curvature_dimension, 408)
        self.assertEqual(cert.ambient_color_dimension, 648)

    def test_projection_is_symmetric_and_idempotent(self):
        p = curvature_projection()
        self.assertLess(np.linalg.norm(p - p.T), 1e-10)
        self.assertLess(np.linalg.norm(p @ p - p), 1e-10)

    def test_covariance_is_an_ambient_contraction(self):
        cert = projection_certificate()
        self.assertTrue(cert.covariance_contraction_certified)
        self.assertGreaterEqual(cert.minimum_eigenvalue, -1e-10)
        self.assertLessEqual(cert.maximum_eigenvalue, 1.0 + 1e-10)


class JointTailTests(unittest.TestCase):
    def test_rate_formula_matches_closed_expression(self):
        s = 12.0
        expected = 0.5 * (s - 3.0 - 3.0 * math.log(s / 3.0))
        self.assertAlmostEqual(radial_gaussian_rate(s), expected)

    def test_rate_is_zero_below_radial_mean_threshold(self):
        self.assertEqual(radial_gaussian_rate(3.0), 0.0)
        self.assertEqual(radial_gaussian_rate(2.0), 0.0)

    def test_joint_bound_exponentiates_in_set_size_without_independence(self):
        one = joint_tail_certificate(1)
        six = joint_tail_certificate(6)
        self.assertAlmostEqual(six.joint_probability_upper, one.joint_probability_upper**6)
        self.assertFalse(six.independence_assumed)
        self.assertTrue(six.dependence_retained)

    def test_smaller_time_improves_rate(self):
        small = joint_tail_certificate(heat_time=2e-6)
        large = joint_tail_certificate(heat_time=3e-6)
        self.assertGreater(small.joint_rate_per_plaquette, large.joint_rate_per_plaquette)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            radial_gaussian_rate(0.0)
        with self.assertRaises(ValueError):
            joint_tail_certificate(0)


class PolymerTests(unittest.TestCase):
    def test_stage09_witness_is_strictly_subcritical(self):
        cert = polymer_certificate()
        self.assertTrue(cert.dependent_gaussian_polymer_certified)
        self.assertLess(cert.branching_ratio, 1.0)
        self.assertLess(cert.rooted_weighted_connected_sum_upper, 1.0)

    def test_maximum_heat_time_is_above_witness(self):
        cert = polymer_certificate()
        self.assertGreater(cert.maximum_certified_heat_time, cert.heat_time)
        self.assertGreater(cert.witness_heat_time_slack, 0.0)

    def test_threshold_solves_branching_equality(self):
        cert = polymer_certificate()
        t_star = maximum_heat_time(cert.curvature_radius, cert.alpha, cert.adjacency_degree)
        boundary = polymer_certificate(t_star, cert.curvature_radius, cert.alpha)
        self.assertAlmostEqual(boundary.branching_ratio, 1.0, places=10)

    def test_larger_time_fails_the_declared_counting_bound(self):
        cert = polymer_certificate(heat_time=4e-6)
        self.assertFalse(cert.dependent_gaussian_polymer_certified)
        self.assertTrue(math.isinf(cert.rooted_weighted_connected_sum_upper))

    def test_no_false_nonlinear_or_rg_promotion(self):
        cert = polymer_certificate()
        self.assertFalse(cert.mayer_activity_expansion_certified)
        self.assertFalse(cert.nonlinear_su2_polymer_certified)
        self.assertFalse(cert.repeated_rg_certified)


if __name__ == "__main__":
    unittest.main()
