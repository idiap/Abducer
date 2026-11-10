import unittest

from advanced_regulator_calibration import (
    advanced_calibration,
    blocking_calibration,
    circle_good_field_tail,
    heat_kernel_wilson_tv,
    su2_antipodal_tv,
    su2_heat_kernel,
)


class AdvancedRegulatorCalibrationTests(unittest.TestCase):
    def test_su2_kernel_normalization(self):
        import math

        t = 0.2
        n = 4096
        dx = math.pi / n
        integral = 0.0
        for k in range(n):
            theta = (k + 0.5) * dx
            integral += (
                su2_heat_kernel(theta, t)
                * (2.0 / math.pi)
                * math.sin(theta) ** 2
            )
        self.assertAlmostEqual(dx * integral, 1.0, delta=2e-8)

    def test_su2_antipodal_tv_degenerates(self):
        values = [su2_antipodal_tv(t, 4096) for t in (0.5, 0.2, 0.1, 0.05)]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))
        self.assertGreater(values[-1], 0.999)

    def test_circle_tail_is_probability(self):
        tail = circle_good_field_tail(0.1, 2.0, 8192)
        self.assertGreater(tail, 0.0)
        self.assertLess(tail, 1.0)

    def test_circle_tail_decreases_with_radius(self):
        small = circle_good_field_tail(0.1, 1.0, 8192)
        large = circle_good_field_tail(0.1, 2.0, 8192)
        self.assertGreater(small, large)

    def test_heat_kernel_wilson_match_improves_at_small_time(self):
        coarse = heat_kernel_wilson_tv(0.5, 8192)
        fine = heat_kernel_wilson_tv(0.05, 8192)
        self.assertGreater(coarse, fine)

    def test_convolution_blocking_reduces_fixed_shift_sensitivity(self):
        rows = blocking_calibration(0.02, [1, 2, 5, 10])
        values = [row["fixed_shift_tv"] for row in rows]
        self.assertTrue(all(a > b for a, b in zip(values, values[1:])))

    def test_advanced_schema_and_proxy(self):
        row = advanced_calibration([0.2], 4096)[0]
        self.assertGreater(row.optimistic_degree_8_proxy, 0.0)
        self.assertLessEqual(row.su2_antipodal_tv, 1.0)


if __name__ == "__main__":
    unittest.main()
