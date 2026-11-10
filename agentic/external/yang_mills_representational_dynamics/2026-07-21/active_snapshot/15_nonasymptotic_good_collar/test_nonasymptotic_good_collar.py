import math
import unittest

from nonasymptotic_good_collar import (
    calibration,
    finite_collar_certificate,
    maximum_heat_time_for_target,
    normalized_haar_ball_volume,
    search_delta,
)


class HaarVolumeTests(unittest.TestCase):
    def test_ball_volume_matches_s3_formula(self):
        r = 0.2
        self.assertAlmostEqual(
            normalized_haar_ball_volume(r),
            (r - 0.5 * math.sin(2 * r)) / math.pi,
        )

    def test_ball_volume_is_increasing(self):
        self.assertLess(normalized_haar_ball_volume(0.001), normalized_haar_ball_volume(0.002))

    def test_invalid_ball_radius_fails_closed(self):
        for value in (0.0, -1.0, math.pi):
            with self.assertRaises(ValueError):
                normalized_haar_ball_volume(value)


class FiniteBoundTests(unittest.TestCase):
    def test_frozen_bound_retains_prefactor_and_is_trivial(self):
        search = search_delta(3e-6, 0.0082, 0.001)
        cert = finite_collar_certificate(3e-6, 0.0082, 0.001, search.selected_delta)
        self.assertGreater(cert.log_bad_probability_upper_raw, 0.0)
        self.assertEqual(cert.bad_probability_upper, 1.0)

    def test_smaller_time_makes_bound_nontrivial(self):
        search = search_delta(8e-7, 0.0082, 0.001)
        cert = finite_collar_certificate(8e-7, 0.0082, 0.001, search.selected_delta)
        self.assertLess(cert.bad_probability_upper, 1e-4)

    def test_energy_gap_is_exact_declared_expression(self):
        cert = finite_collar_certificate(1e-6, 0.0082, 0.001, 0.0003)
        self.assertAlmostEqual(cert.finite_time_energy_gap, 0.0082**2 - 6 * 0.0013**2)

    def test_larger_coherence_radius_worsens_bound(self):
        a = finite_collar_certificate(8e-7, 0.0082, 0.0008, 0.0003)
        b = finite_collar_certificate(8e-7, 0.0082, 0.0010, 0.0003)
        self.assertLess(a.log_bad_probability_upper_raw, b.log_bad_probability_upper_raw)

    def test_invalid_gap_fails_closed(self):
        with self.assertRaises(ValueError):
            finite_collar_certificate(1e-6, 0.0082, 0.0033, 0.001)


class ThresholdTests(unittest.TestCase):
    def test_delta_search_is_admissible_and_not_claimed_optimal(self):
        search = search_delta(1e-6, 0.0082, 0.001)
        self.assertGreater(search.selected_delta, 0.0)
        self.assertLess(search.selected_delta, search.admissible_delta_upper)
        self.assertFalse(search.global_optimality_claimed)

    def test_target_threshold_is_below_frozen_time(self):
        q = math.exp(-0.1) / 18**2
        time, delta = maximum_heat_time_for_target(q)
        self.assertLess(time, 3e-6)
        self.assertGreater(time, 8e-7)
        cert = finite_collar_certificate(time, 0.0082, 0.001, delta)
        self.assertAlmostEqual(cert.log_bad_probability_upper_raw, math.log(q), places=8)

    def test_calibration_exposes_scope(self):
        result = calibration()
        self.assertTrue(result.radial_monotonicity_used)
        self.assertFalse(result.frozen_witness.collar_probability_certified)
        self.assertFalse(result.frozen_witness.full_su2_block_measure_certified)

    def test_invalid_target_fails_closed(self):
        for value in (0.0, 1.0, -0.1):
            with self.assertRaises(ValueError):
                maximum_heat_time_for_target(value)


if __name__ == "__main__":
    unittest.main()
