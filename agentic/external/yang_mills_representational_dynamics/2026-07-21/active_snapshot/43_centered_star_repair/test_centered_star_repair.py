import unittest
import numpy as np
from centered_star_repair import *


class Tests(unittest.TestCase):
    def test_projection_idempotent(self):
        p = centered_projection(6); self.assertLess(np.linalg.norm(p @ p - p), 1e-12)
    def test_projection_rank(self): self.assertEqual(np.linalg.matrix_rank(centered_projection(6)), 5)
    def test_invalid_projection(self):
        with self.assertRaises(ValueError): centered_projection(1)
    def test_mean_preserved(self):
        x = np.arange(18).reshape(6,3); y = repair_centered(x,.5)
        self.assertLess(np.linalg.norm(x.mean(0)-y.mean(0)),1e-12)
    def test_rms_scales(self):
        x = np.arange(18).reshape(6,3); self.assertAlmostEqual(centered_rms(repair_centered(x,.4)),.4*centered_rms(x))
    def test_invalid_contraction(self):
        with self.assertRaises(ValueError): repair_centered(np.zeros((6,3)),1)
    def test_dimension(self): self.assertEqual(calibration()["certificate"]["centered_dimension"],15)
    def test_maps_to_good(self): self.assertTrue(calibration()["certificate"]["maps_chart_into_good_region"])
    def test_action_drop_positive(self): self.assertGreater(calibration()["certificate"]["minimum_action_drop"],0)
    def test_jacobian_counted(self): self.assertGreater(calibration()["certificate"]["log_jacobian_loss"],0)
    def test_ideal_closes(self): self.assertTrue(calibration()["ideal_tangent_star_repair_closes"])
    def test_lift_open(self): self.assertFalse(calibration()["nonlinear_link_realizability_proved"])
    def test_spillover_open(self): self.assertFalse(calibration()["external_plaquette_spillover_included"])
    def test_invalid_certificate(self):
        with self.assertRaises(ValueError): repair_certificate(6,3,3e-6,.006,.005,.004)


if __name__ == "__main__": unittest.main()
