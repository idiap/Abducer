import unittest

import numpy as np

from su2_block_linearized import (
    analyze_block,
    build_cubical_block,
    centered_transport_coefficient,
    exact_rational_rank,
    gaussian_conditional,
    nonlinear_fiber_margin,
    numerical_rank,
    scalar_decomposition,
)


class SU2BlockLinearizedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.block = build_cubical_block()
        cls.decomposition = scalar_decomposition(cls.block)
        cls.analysis = analyze_block()

    def test_frozen_block_cell_counts(self):
        self.assertEqual(len(self.block.vertices), 81)
        self.assertEqual(len(self.block.edges), 216)
        self.assertEqual(len(self.block.plaquettes), 216)

    def test_boundary_of_boundary_is_zero(self):
        self.assertEqual(np.count_nonzero(self.block.d1 @ self.block.d0), 0)

    def test_contractible_complex_has_only_gauge_flat_directions(self):
        self.assertEqual(numerical_rank(self.block.d0), 80)
        self.assertEqual(numerical_rank(self.block.d1), 136)
        self.assertEqual(
            self.block.d0.shape[0] - numerical_rank(self.block.d1), 80
        )

    def test_physical_and_fiber_dimensions(self):
        self.assertEqual(self.analysis.scalar_physical_dimension, 136)
        self.assertEqual(self.analysis.independent_coarse_fluxes, 17)
        self.assertEqual(self.analysis.scalar_fiber_dimension, 119)
        self.assertEqual(self.analysis.su2_physical_dimension, 408)
        self.assertEqual(self.analysis.su2_base_dimension, 51)
        self.assertEqual(self.analysis.su2_fiber_dimension, 357)

    def test_coarse_flux_rank_is_exactly_seventeen(self):
        self.assertEqual(exact_rational_rank(self.block.coarse_flux), 17)

    def test_coarse_flux_is_gauge_invariant_at_linear_order(self):
        residual = self.block.coarse_flux @ self.block.d0
        self.assertEqual(np.count_nonzero(residual), 0)

    def test_certified_coercivity_is_respected(self):
        self.assertAlmostEqual(self.analysis.physical_min_eigenvalue, 2.0, places=10)
        self.assertGreater(
            self.analysis.fiber_min_eigenvalue,
            self.analysis.certified_physical_lower_bound,
        )

    def test_gauge_quotient_is_essential(self):
        full_hessian = self.block.d1.T @ self.block.d1
        eigenvalues = np.linalg.eigvalsh(full_hessian)
        self.assertEqual(int(np.count_nonzero(eigenvalues < 1e-9)), 80)

    def test_centered_gaussian_covariance_is_base_independent(self):
        rank = self.analysis.independent_coarse_fluxes
        first = gaussian_conditional(np.zeros(rank), 0.2)
        second = gaussian_conditional(np.linspace(-0.1, 0.1, rank), 0.2)
        self.assertGreater(np.linalg.norm(first.mean - second.mean), 0.0)
        self.assertTrue(
            np.allclose(first.centered_covariance, second.centered_covariance)
        )

    def test_nonlinear_certificate_budget(self):
        self.assertAlmostEqual(nonlinear_fiber_margin(0.5), 1.5)
        self.assertAlmostEqual(centered_transport_coefficient(0.5, 0.5), 1.0 / 3.0)
        with self.assertRaises(ValueError):
            nonlinear_fiber_margin(2.0)

    def test_invalid_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            build_cubical_block(dimension=1)
        with self.assertRaises(ValueError):
            gaussian_conditional([0.0], 0.1)


if __name__ == "__main__":
    unittest.main()
