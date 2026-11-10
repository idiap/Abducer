import math
import unittest

from heat_kernel_influence import (
    calibrate,
    circle_heat_kernel,
    gaussian_translation_limit,
    total_variation_translate,
)


class HeatKernelInfluenceTests(unittest.TestCase):
    def test_kernel_is_nonnegative_at_calibration_points(self):
        for t in (1.0, 0.2, 0.05):
            for k in range(128):
                theta = -math.pi + 2.0 * math.pi * k / 128
                self.assertGreaterEqual(circle_heat_kernel(theta, t), -1e-12)

    def test_translation_by_zero_has_zero_tv(self):
        self.assertLess(total_variation_translate(0.2, 0.0, 4096), 1e-12)

    def test_tv_is_symmetric_in_shift(self):
        plus = total_variation_translate(0.2, 1.1, 4096)
        minus = total_variation_translate(0.2, -1.1, 4096)
        self.assertAlmostEqual(plus, minus, places=10)

    def test_fixed_nonzero_shift_approaches_one(self):
        values = [
            total_variation_translate(t, math.pi, 8192)
            for t in (0.5, 0.2, 0.1, 0.05)
        ]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))
        self.assertGreater(values[-1], 0.999)

    def test_sqrt_t_shift_has_nontrivial_gaussian_limit(self):
        scale = 0.5
        expected = gaussian_translation_limit(scale)
        observed = total_variation_translate(0.02, scale * math.sqrt(0.02), 16384)
        self.assertAlmostEqual(observed, expected, delta=0.006)

    def test_calibration_schema(self):
        rows = calibrate([0.5, 0.1], grid_size=4096)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].heat_time, 0.5)
        self.assertLessEqual(rows[0].fixed_shift_tv, 1.0)

    def test_invalid_parameters_fail_closed(self):
        with self.assertRaises(ValueError):
            circle_heat_kernel(0.0, 0.0)
        with self.assertRaises(ValueError):
            total_variation_translate(0.1, 1.0, 127)


if __name__ == "__main__":
    unittest.main()
