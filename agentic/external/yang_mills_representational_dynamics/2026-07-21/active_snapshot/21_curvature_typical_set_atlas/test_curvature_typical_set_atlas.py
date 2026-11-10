import math
import unittest

import numpy as np

from curvature_typical_set_atlas import (
    center_atlas_coordinate,
    center_atlas_jacobian_ratio_bound,
    center_atlas_reconstruct,
    leverage_certificate,
    local_block_union_radius,
    local_block_union_upper,
    normalized_haar_jacobian,
    physical_covariance,
)


class TypicalSetAtlasTests(unittest.TestCase):
    def test_physical_dimension_and_hessian_spectrum(self):
        cert = leverage_certificate()
        self.assertEqual(cert.physical_scalar_dimension, 136)
        self.assertAlmostEqual(cert.hessian_min, 2.0, places=11)
        self.assertAlmostEqual(cert.hessian_max, 12.0, places=10)

    def test_covariance_annihilates_gauge_directions(self):
        block, _, covariance, _ = physical_covariance()
        self.assertLess(np.linalg.norm(covariance @ block.d0), 1e-12)

    def test_curvature_covariance_is_projector(self):
        _, _, _, curvature = physical_covariance()
        self.assertLess(np.linalg.norm(curvature @ curvature - curvature), 1e-11)

    def test_leverage_values(self):
        cert = leverage_certificate()
        self.assertAlmostEqual(cert.max_link_variance_coefficient, 0.12878857368564722)
        self.assertAlmostEqual(cert.max_four_link_variance_coefficient, 0.17946063737181953)
        self.assertAlmostEqual(cert.max_curvature_variance_coefficient, 0.685582010582011)

    def test_local_radius_matches_frozen_value(self):
        cert = leverage_certificate()
        radius = local_block_union_radius(216, 12, 3e-6 * cert.max_four_link_variance_coefficient, 0.0027927080803578997)
        self.assertAlmostEqual(radius, 0.006023157807602598)

    def test_certified_radius_meets_requested_union_bound(self):
        cert = leverage_certificate()
        delta = 0.0027927080803578997
        variance = 3e-6 * cert.max_four_link_variance_coefficient
        radius = local_block_union_radius(216, 12, variance, delta)
        self.assertLessEqual(local_block_union_upper(radius, 216, 12, variance), delta * (1 + 1e-12))

    def test_old_local_radius_has_no_union_certificate(self):
        cert = leverage_certificate()
        bound = local_block_union_upper(0.003, 216, 12, 3e-6 * cert.max_four_link_variance_coefficient)
        self.assertEqual(bound, 1.0)

    def test_dependency_is_not_used_in_union_formula(self):
        # The theorem depends only on marginal covariance operator bounds.
        independent = local_block_union_radius(10, 3, 0.2, 0.01)
        perfectly_correlated = local_block_union_radius(10, 3, 0.2, 0.01)
        self.assertEqual(independent, perfectly_correlated)

    def test_two_center_atlas_roundtrip(self):
        rng = np.random.default_rng(91)
        for _ in range(100):
            q = rng.normal(size=4)
            q /= np.linalg.norm(q)
            center, coordinate = center_atlas_coordinate(q)
            rebuilt = center_atlas_reconstruct(center, coordinate)
            self.assertTrue(np.allclose(q, rebuilt, atol=1e-12))
            self.assertLessEqual(np.linalg.norm(coordinate), math.pi / 2 + 1e-12)

    def test_negative_center_uses_second_chart(self):
        center, coordinate = center_atlas_coordinate([-1.0, 0.0, 0.0, 0.0])
        self.assertEqual(center, -1)
        self.assertTrue(np.allclose(coordinate, 0.0))

    def test_haar_jacobian_ratio(self):
        ratio = normalized_haar_jacobian(0.0) / normalized_haar_jacobian(math.pi / 2)
        self.assertAlmostEqual(ratio, center_atlas_jacobian_ratio_bound())

    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            local_block_union_radius(5, 3, 1.0, 1.0)

    def test_invalid_haar_radius_rejected(self):
        with self.assertRaises(ValueError):
            normalized_haar_jacobian(math.pi + 0.1)


if __name__ == "__main__":
    unittest.main()

