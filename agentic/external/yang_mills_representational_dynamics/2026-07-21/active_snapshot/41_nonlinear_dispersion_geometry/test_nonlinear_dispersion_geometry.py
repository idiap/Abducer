import math
import unittest
import numpy as np
from nonlinear_dispersion_geometry import *


class Tests(unittest.TestCase):
    def test_metric_origin(self): self.assertEqual(metric_factor(0), 1)
    def test_metric_strict(self): self.assertLess(metric_factor(.1), 1)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError): metric_factor(math.pi / 2)
    def test_invalid_variance(self):
        with self.assertRaises(ValueError): variance_proxy_bounds(1, 0, .1)
    def test_bounds_order(self):
        c = variance_proxy_bounds(6, .2, .1); self.assertLessEqual(c.pairwise_proxy_lower, c.pairwise_proxy_upper)
    def test_symmetric_star_size(self): self.assertEqual(len(symmetric_star(np.eye(3) * .01)), 6)
    def test_symmetric_bounds(self):
        c = calibration(); x = c["symmetric_noncommuting_example"]
        self.assertTrue(x["lower_bound_met"] and x["upper_bound_met"])
    def test_proxy_positive(self): self.assertGreater(pairwise_proxy(symmetric_star(np.eye(3) * .01)), 0)
    def test_conjugation_invariance(self):
        star = symmetric_star(np.eye(3) * .01); h = su2_exp((.2, -.1, .3))
        self.assertAlmostEqual(pairwise_proxy(star), pairwise_proxy(conjugate_star(star, h)), places=12)
    def test_bad_quaternion(self):
        with self.assertRaises(ValueError): su2_distance((2,0,0,0), (1,0,0,0))
    def test_chart_loss_tiny(self): self.assertGreater(calibration()["metric_factor_squared"], .9999)
    def test_gauge_invariant_status(self): self.assertTrue(calibration()["variance_proxy_theorem"]["gauge_invariant"])
    def test_physical_comparison_open(self): self.assertFalse(calibration()["complete_nonlinear_measure_comparison_proved"])


if __name__ == "__main__": unittest.main()
