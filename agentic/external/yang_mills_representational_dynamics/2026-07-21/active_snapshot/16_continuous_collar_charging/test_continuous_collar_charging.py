import math
import unittest

import numpy as np

from continuous_collar_charging import (
    collar_charge_certificate,
    compatibility_certificate,
    radial_gaussian_rate,
    relative_distance_errors,
    scaled_radius_for_rate,
    su2_distance,
)


def exp_axis(theta, axis):
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    return np.concatenate(([math.cos(theta)], math.sin(theta) * axis))


class QuaternionGeometryTests(unittest.TestCase):
    def test_center_antipodes_have_distance_pi(self):
        self.assertAlmostEqual(su2_distance([1, 0, 0, 0], [-1, 0, 0, 0]), math.pi)

    def test_left_multiplication_preserves_all_relative_distances(self):
        u = exp_axis(0.71, [1, 2, 3])
        staples = [
            exp_axis(0.13, [1, 0, 0]),
            exp_axis(0.28, [0, 1, 0]),
            exp_axis(0.19, [0, 0, 1]),
        ]
        self.assertLess(max(relative_distance_errors(u, staples)), 1e-12)

    def test_nonunit_quaternion_fails_closed(self):
        with self.assertRaises(ValueError):
            su2_distance([2, 0, 0, 0], [1, 0, 0, 0])


class ChargeTests(unittest.TestCase):
    def test_charge_constants_follow_triangle_and_square_inequalities(self):
        cert = collar_charge_certificate(0.003)
        self.assertAlmostEqual(cert.guaranteed_single_curvature_above, 0.0015)
        self.assertAlmostEqual(cert.guaranteed_incident_energy_above, 0.003**2 / 2)
        self.assertTrue(cert.link_value_uniform)

    def test_charge_does_not_itself_establish_probability(self):
        self.assertFalse(collar_charge_certificate(0.001).probability_bound_certified)

    def test_invalid_charge_inputs_fail_closed(self):
        for eta in (0.0, -1.0, math.pi):
            with self.assertRaises(ValueError):
                collar_charge_certificate(eta)


class CompatibilityTests(unittest.TestCase):
    def test_frozen_witness_is_incompatible_with_local_charge(self):
        cert = compatibility_certificate()
        self.assertFalse(cert.energy_charge_meets_target)
        self.assertFalse(cert.radial_charge_meets_target)
        self.assertTrue(cert.multi_link_repair_required)

    def test_maximum_charge_radius_combines_both_thresholds(self):
        cert = compatibility_certificate()
        self.assertAlmostEqual(
            cert.maximum_single_charge_radius,
            0.0082 / (2 * math.sqrt(6)),
        )

    def test_radial_rate_is_zero_below_three_dimensional_mean(self):
        self.assertEqual(radial_gaussian_rate(2.99), 0.0)

    def test_rate_inverse_is_consistent(self):
        s = scaled_radius_for_rate(7.0)
        self.assertAlmostEqual(radial_gaussian_rate(s), 7.0, places=11)

    def test_smaller_time_can_meet_energy_target(self):
        baseline = compatibility_certificate()
        cert = compatibility_certificate(heat_time=0.9 * baseline.maximum_time_for_energy_target)
        self.assertTrue(cert.energy_charge_meets_target)

    def test_radial_requirement_is_stricter_than_total_energy_requirement(self):
        cert = compatibility_certificate()
        self.assertLess(cert.maximum_time_for_radial_target, cert.maximum_time_for_energy_target)

    def test_no_false_full_measure_claim_is_encoded_in_scope(self):
        cert = compatibility_certificate()
        self.assertFalse(cert.frozen_witness_compatible)


if __name__ == "__main__":
    unittest.main()
