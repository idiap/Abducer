import math
import sys
import unittest
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from su2_nonlinear_block_geometry import (
    action_initialization_certificate,
    build_block_complex,
    calibration,
    gauge_slice_certificate,
    incidence_certificate,
    plaquette_chart_certificate,
    plaquette_log,
    product_log_bounds,
    quaternion_inverse,
    quaternion_multiply,
    solve_local_coulomb_slice,
    su2_exp,
    su2_log,
    transform_link_field,
)


class QuaternionTests(unittest.TestCase):
    def test_exp_log_round_trip(self):
        for a in (
            np.array([0.0, 0.0, 0.0]),
            np.array([0.2, -0.1, 0.05]),
            np.array([-0.4, 0.3, 0.1]),
        ):
            self.assertTrue(np.allclose(su2_log(su2_exp(a)), a, atol=1e-13))

    def test_quaternion_inverse(self):
        q = su2_exp([0.2, -0.3, 0.1])
        identity = quaternion_multiply(q, quaternion_inverse(q))
        self.assertTrue(np.allclose(identity, [1.0, 0.0, 0.0, 0.0], atol=1e-13))

    def test_cut_locus_rejected(self):
        with self.assertRaises(ValueError):
            su2_log([-1.0, 0.0, 0.0, 0.0])

    def test_commuting_plaquette_is_exactly_linear(self):
        local = np.array(
            [[0.01, 0.0, 0.0], [0.02, 0.0, 0.0],
             [0.003, 0.0, 0.0], [0.004, 0.0, 0.0]]
        )
        expected = local[0] + local[1] - local[2] - local[3]
        self.assertTrue(np.allclose(plaquette_log(local), expected, atol=1e-13))

    def test_bch_remainder_respects_taylor_bound(self):
        rng = np.random.default_rng(20260720)
        radius = 0.003
        bound = product_log_bounds(4, radius)
        for _ in range(50):
            local = rng.normal(size=(4, 3))
            local *= 0.9 * radius / np.linalg.norm(local)
            linear = local[0] + local[1] - local[2] - local[3]
            remainder = np.linalg.norm(plaquette_log(local) - linear)
            self.assertLessEqual(remainder, 0.5 * bound.map_second_bound * radius**2)


class IncidenceTests(unittest.TestCase):
    def test_exact_block_counts_and_degrees(self):
        cert = incidence_certificate()
        self.assertEqual((cert.vertices, cert.links, cert.plaquettes), (81, 216, 216))
        self.assertEqual(cert.max_vertex_degree, 8)
        self.assertEqual(cert.max_link_plaquette_degree, 6)
        self.assertEqual(cert.plaquette_boundary_links, 4)
        self.assertEqual((cert.gauge_rank, cert.curvature_rank), (80, 136))
        self.assertEqual((cert.independent_coarse_fluxes, cert.fiber_dimension_scalar), (17, 119))

    def test_complex_and_operator_spectra(self):
        block = build_block_complex()
        self.assertEqual(float(np.linalg.norm(block.d1 @ block.d0)), 0.0)
        self.assertAlmostEqual(np.linalg.norm(block.d0, 2), math.sqrt(12.0), places=12)
        self.assertAlmostEqual(np.linalg.norm(block.d1, 2), math.sqrt(12.0), places=12)
        eig = np.linalg.eigvalsh(block.d1.T @ block.d1)
        positive = eig[eig > 1e-9]
        self.assertAlmostEqual(float(positive[0]), 2.0, places=12)


class ChartAndSliceTests(unittest.TestCase):
    def test_product_log_requires_convergent_ball(self):
        with self.assertRaises(ValueError):
            product_log_bounds(4, 0.5)

    def test_plaquette_chart_is_bilipschitz_on_coulomb_slice(self):
        cert = plaquette_chart_certificate(0.003)
        self.assertTrue(cert.injective_on_coulomb_slice)
        self.assertGreater(cert.nonlinear_physical_min_singular_value, 1.35)
        self.assertLess(cert.inverse_lipschitz_bound, 0.75)

    def test_excessive_chart_rejected(self):
        with self.assertRaises(ValueError):
            plaquette_chart_certificate(0.1)

    def test_gauge_slice_contraction_and_chart_entry(self):
        cert = gauge_slice_certificate(0.0002, 0.0006, 0.003)
        self.assertTrue(cert.contraction_certified)
        self.assertTrue(cert.action_chart_entry_certified)
        self.assertLess(cert.contraction_coefficient, 0.06)
        self.assertGreater(cert.ball_mapping_slack, 0.0)

    def test_gauge_slice_fails_closed_when_ball_is_too_small(self):
        cert = gauge_slice_certificate(0.001, 0.0001, 0.003)
        self.assertFalse(cert.contraction_certified)
        self.assertFalse(cert.action_chart_entry_certified)

    def test_numerical_coulomb_solver(self):
        block = build_block_complex()
        rng = np.random.default_rng(8)
        field = rng.normal(size=(len(block.edges), 3))
        field *= 1e-4 / np.linalg.norm(field)
        phi, transformed, iterations, residual = solve_local_coulomb_slice(field)
        self.assertLessEqual(residual, 1e-12)
        self.assertLess(iterations, 12)
        self.assertLess(np.linalg.norm(phi), 0.0006)
        self.assertLess(np.linalg.norm(transformed), 0.003)

    def test_plaquette_class_angle_is_gauge_invariant(self):
        block = build_block_complex()
        rng = np.random.default_rng(9)
        field = rng.normal(size=(len(block.edges), 3)) * 2e-4
        phi = rng.normal(size=(len(block.vertices), 3)) * 3e-4
        transformed = transform_link_field(field, phi, block)
        edge_index = {edge: i for i, edge in enumerate(block.edges)}
        x, mu, nu = block.plaquettes[37]
        ids = [
            edge_index[(x, mu)],
            edge_index[(tuple(v + (1 if i == mu else 0) for i, v in enumerate(x)), nu)],
            edge_index[(tuple(v + (1 if i == nu else 0) for i, v in enumerate(x)), mu)],
            edge_index[(x, nu)],
        ]
        before = np.linalg.norm(plaquette_log(field[ids]))
        after = np.linalg.norm(plaquette_log(transformed[ids]))
        self.assertAlmostEqual(before, after, places=12)


class ActionCertificateTests(unittest.TestCase):
    def test_default_initializes_all_five_local_norm_components(self):
        cert = action_initialization_certificate()
        self.assertTrue(cert.local_norm_initialized)
        self.assertLess(cert.eps_fiber, cert.lambda_fiber)
        self.assertTrue(cert.fiber_contraction_certified)
        self.assertTrue(cert.generated_base_coercive)
        self.assertGreater(cert.generated_base_margin, 0.35)

    def test_stage06_formulas_cross_check(self):
        stage06 = HERE.parent / "06_one_step_effective_action"
        sys.path.insert(0, str(stage06))
        from one_step_effective_action import LocalActionNorm, one_step_certificate

        cert = action_initialization_certificate()
        checked = one_step_certificate(
            cert.lambda_fiber,
            cert.lambda_base,
            cert.fiber_radius,
            LocalActionNorm(
                cert.eps_fiber,
                cert.eps_cross,
                cert.eps_base,
                cert.tau_fiber,
                cert.tau_cross,
            ),
        )
        self.assertAlmostEqual(
            checked.centered_transport_coefficient,
            cert.centered_transport_coefficient,
            places=14,
        )
        self.assertAlmostEqual(
            checked.generated_base_margin, cert.generated_base_margin, places=14
        )

    def test_large_chart_exhausts_local_margin(self):
        with self.assertRaises(ValueError):
            action_initialization_certificate(time_max=0.2, local_link_radius=0.01)

    def test_scope_flags_block_false_mass_gap_promotion(self):
        cert = action_initialization_certificate()
        self.assertFalse(cert.full_measure_certified)
        self.assertFalse(cert.polymer_certified)
        self.assertFalse(cert.continuum_certified)
        self.assertFalse(cert.mass_gap_certified)

    def test_calibration_records_probability_obstruction(self):
        data = calibration()
        tail = data["small_chart_probability_obstruction"]
        self.assertGreater(tail["lower"], 0.9999)
        self.assertLessEqual(tail["lower"], tail["upper"])


if __name__ == "__main__":
    unittest.main()
