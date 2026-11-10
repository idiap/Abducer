import math
import unittest

from su2_haar_entropy import (
    calibration,
    cubic_volume_bounds,
    entropy_certificate,
    normalized_haar_ball_volume,
    normalized_haar_shell_volume,
    normalized_haar_sphere_density,
    two_center_atlas_certificate,
)


class HaarEntropyTests(unittest.TestCase):
    def test_endpoints(self):
        self.assertEqual(normalized_haar_ball_volume(0.0), 0.0)
        self.assertEqual(normalized_haar_ball_volume(math.pi), 1.0)

    def test_hemisphere(self):
        self.assertAlmostEqual(normalized_haar_ball_volume(math.pi / 2), 0.5, places=14)

    def test_complement_symmetry(self):
        for r in (0.1, 0.7, 1.2):
            self.assertAlmostEqual(
                normalized_haar_ball_volume(r) + normalized_haar_ball_volume(math.pi - r),
                1.0,
                places=13,
            )

    def test_small_branch_matches_formula(self):
        r = 9.0e-4
        direct = (r - math.sin(r) * math.cos(r)) / math.pi
        self.assertAlmostEqual(normalized_haar_ball_volume(r), direct, delta=3.0e-17)

    def test_density_is_derivative(self):
        r, h = 0.4, 1.0e-6
        numerical = (normalized_haar_ball_volume(r + h) - normalized_haar_ball_volume(r - h)) / (2 * h)
        self.assertAlmostEqual(numerical, normalized_haar_sphere_density(r), places=9)

    def test_shell_additivity(self):
        self.assertAlmostEqual(
            normalized_haar_shell_volume(0.1, 0.5) + normalized_haar_shell_volume(0.5, 0.9),
            normalized_haar_shell_volume(0.1, 0.9),
            places=14,
        )

    def test_zero_shell(self):
        self.assertEqual(normalized_haar_shell_volume(0.2, 0.2), 0.0)

    def test_cubic_bounds(self):
        for r in (1.0e-6, 0.01, 0.2, 0.8, 1.0):
            lo, hi = cubic_volume_bounds(r)
            exact = normalized_haar_ball_volume(r)
            self.assertLessEqual(lo, exact + 2.0e-15 * max(1.0, exact))
            self.assertLessEqual(exact, hi + 2.0e-15 * max(1.0, exact))

    def test_entropy_bracket(self):
        cert = entropy_certificate(0.00614955590043087)
        self.assertTrue(cert.exact_inside_bounds)
        self.assertLessEqual(cert.entropy_lower, cert.exact_negative_log_volume)
        self.assertLessEqual(cert.exact_negative_log_volume, cert.entropy_upper)

    def test_entropy_decreases_with_radius(self):
        self.assertGreater(
            entropy_certificate(0.005).exact_negative_log_volume,
            entropy_certificate(0.01).exact_negative_log_volume,
        )

    def test_atlas(self):
        cert = two_center_atlas_certificate()
        self.assertTrue(cert.union_covers_su2)
        self.assertTrue(cert.overlap_has_haar_measure_zero)
        self.assertAlmostEqual(cert.ball_mass, 0.5)

    def test_calibration_active_radii(self):
        data = calibration()
        self.assertEqual(len(data["active_radii"]), 7)
        self.assertTrue(all(x["exact_inside_bounds"] for x in data["active_radii"].values()))

    def test_invalid_radius(self):
        for r in (-0.1, math.pi + 0.01, math.inf, math.nan):
            with self.assertRaises(ValueError):
                normalized_haar_ball_volume(r)

    def test_invalid_shell_order(self):
        with self.assertRaises(ValueError):
            normalized_haar_shell_volume(0.5, 0.1)

    def test_bounds_scope(self):
        with self.assertRaises(ValueError):
            cubic_volume_bounds(1.01)


if __name__ == "__main__":
    unittest.main()
