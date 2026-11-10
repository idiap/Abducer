import unittest
from coordinated_repair_frontier import *


class Tests(unittest.TestCase):
    def test_interval_nonempty(self):
        a,b=calibration()["nonlinear_split_interval"]; self.assertLess(a,b)
    def test_min_above_gaussian(self): self.assertGreater(calibration()["nonlinear_split_interval"][0],.00386)
    def test_curve_points(self): self.assertEqual(len(calibration()["remedy_curve"]),6)
    def test_actual_fails(self): self.assertFalse(calibration()["actual_single_star_route_closes_anywhere"])
    def test_allowed_positive(self): self.assertGreater(calibration()["maximum_admissible_spill_at_upper_split"],0)
    def test_reduction_needed(self): self.assertLess(calibration()["required_spill_reduction_factor"],1)
    def test_sufficient_condition(self): self.assertTrue(calibration()["coordinated_polymer_sufficient_condition_proved"])
    def test_physical_open(self): self.assertFalse(calibration()["physical_coordinated_repair_constructed"])
    def test_less_spill_improves(self):
        self.assertGreater(repair_free_energy(.006,.021,.2),repair_free_energy(.006,.021,1.0))
    def test_larger_required_tightens(self):
        self.assertLessEqual(admissible_spill_coefficient(.007,.021,9),admissible_spill_coefficient(.007,.021,7))
    def test_invalid_free_energy(self):
        with self.assertRaises(ValueError): repair_free_energy(0,.02,1)
    def test_invalid_admissibility(self):
        with self.assertRaises(ValueError): admissible_spill_coefficient(.03,.02,7)
    def test_curve_status_consistent(self):
        for p in calibration()["remedy_curve"]: self.assertEqual(p["closes"],p["free_energy"]>p["required_free_energy"])
    def test_best_is_upper(self):
        self.assertAlmostEqual(calibration()["best_actual_single_star_point"]["split_rms"],calibration()["nonlinear_split_interval"][1])


if __name__ == "__main__": unittest.main()
