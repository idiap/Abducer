import math
from pathlib import Path
import sys
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from frustrated_conditioning import (
    calibration,
    conditional_law_certificate,
    log_su2_image_kernel_shape,
    numerical_conditional_calibration,
    rate_obstruction_certificate,
    staple_realization_certificate,
)


class StapleGeometryTests(unittest.TestCase):
    def test_selected_link_has_six_incident_plaquettes(self):
        cert = staple_realization_certificate()
        self.assertEqual(cert.incidence_degree, 6)
        self.assertEqual(len(cert.incident_plaquette_indices), 6)

    def test_center_staple_map_is_surjective(self):
        cert = staple_realization_certificate()
        self.assertEqual(cert.center_staple_map_rank, 6)
        self.assertTrue(cert.surjective)

    def test_exactly_one_negative_staple_is_realized(self):
        cert = staple_realization_certificate(3)
        self.assertTrue(cert.target_realized)
        self.assertEqual(sum(cert.realized_staple_bits), 1)
        self.assertEqual(cert.realized_staple_bits[3], 1)
        self.assertGreaterEqual(len(cert.negative_center_link_indices), 1)

    def test_every_incident_target_can_be_realized(self):
        for position in range(6):
            cert = staple_realization_certificate(position)
            self.assertTrue(cert.target_realized)
            self.assertEqual(cert.realized_staple_bits[position], 1)

    def test_invalid_incident_target_is_rejected(self):
        with self.assertRaises(ValueError):
            staple_realization_certificate(6)


class ConditionalLawTests(unittest.TestCase):
    def test_conditional_law_has_five_aligned_and_one_frustrated_factor(self):
        cert = conditional_law_certificate()
        self.assertEqual(cert.identity_staples, 5)
        self.assertEqual(cert.negative_identity_staples, 1)
        self.assertTrue(cert.exact_center_conditioning)
        self.assertIn("p_t(U)^5", cert.density_formula)

    def test_log_image_shape_is_finite_and_class_symmetric_at_identity_scale(self):
        values = [
            log_su2_image_kernel_shape(theta, 0.02)
            for theta in (0.1, 0.5, 1.0, math.pi - 0.1)
        ]
        self.assertTrue(np.all(np.isfinite(values)))
        self.assertGreater(values[0], values[-1])

    def test_invalid_image_arguments_fail_closed(self):
        with self.assertRaises(ValueError):
            log_su2_image_kernel_shape(0.0, 0.02)
        with self.assertRaises(ValueError):
            log_su2_image_kernel_shape(0.5, 0.0)


class RateObstructionTests(unittest.TestCase):
    def test_exact_minimizer_and_frustrated_angle(self):
        cert = rate_obstruction_certificate()
        self.assertAlmostEqual(cert.minimizer_angle, math.pi / 6.0, places=14)
        self.assertAlmostEqual(
            cert.target_angle_at_minimizer, 5.0 * math.pi / 6.0, places=14
        )

    def test_exact_rate_gap_identity(self):
        rho = 0.0082
        cert = rate_obstruction_certificate(rho)
        expected = 6.0 * (5.0 * math.pi / 6.0 - rho) ** 2
        self.assertAlmostEqual(cert.good_event_rate_gap, expected, places=13)
        self.assertAlmostEqual(
            cert.good_event_rate_infimum - cert.minimum_rate,
            expected,
            places=13,
        )

    def test_stage09_chart_is_conditionally_bad_with_probability_tending_one(self):
        cert = rate_obstruction_certificate(0.0082)
        self.assertTrue(cert.bad_probability_tends_to_one)
        self.assertFalse(cert.uniform_microscopic_conditional_tail_possible)
        self.assertLess(cert.scaled_log_probability_limit, -40.0)

    def test_threshold_radius_removes_the_obstruction(self):
        cert = rate_obstruction_certificate(5.0 * math.pi / 6.0)
        self.assertEqual(cert.good_event_rate_gap, 0.0)
        self.assertFalse(cert.bad_probability_tends_to_one)

    def test_invalid_rate_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            rate_obstruction_certificate(0.0)
        with self.assertRaises(ValueError):
            rate_obstruction_certificate(0.1, 1)


class NumericalCalibrationTests(unittest.TestCase):
    def test_conditional_mode_approaches_pi_over_six(self):
        cert = numerical_conditional_calibration(0.01, quadrature_nodes=256)
        self.assertLess(abs(cert.mode_angle - math.pi / 6.0), 0.01)
        self.assertGreater(cert.target_angle_at_mode, 2.60)

    def test_scaled_log_probability_matches_rate_at_uv_witness(self):
        cert = numerical_conditional_calibration(3.0e-6, quadrature_nodes=512)
        self.assertLess(cert.scaled_rate_relative_error, 0.01)
        self.assertEqual(cert.bad_probability, 1.0)
        self.assertLess(cert.log_good_probability, -1.0e6)

    def test_smaller_time_improves_large_deviation_agreement(self):
        warm = numerical_conditional_calibration(0.05, quadrature_nodes=256)
        cold = numerical_conditional_calibration(0.01, quadrature_nodes=256)
        self.assertLess(
            cold.scaled_rate_relative_error, warm.scaled_rate_relative_error
        )

    def test_calibration_blocks_false_clay_promotion(self):
        data = calibration()
        self.assertEqual(data["claim_level"], "C2 restricted obstruction theorem")
        self.assertFalse(data["frontier_flags"]["dependent_polymer"])
        self.assertFalse(data["frontier_flags"]["continuum_yang_mills"])
        self.assertFalse(data["frontier_flags"]["hamiltonian_mass_gap"])
        self.assertIn("charges the frustrating", data["first_unproved_implication"])


if __name__ == "__main__":
    unittest.main()

