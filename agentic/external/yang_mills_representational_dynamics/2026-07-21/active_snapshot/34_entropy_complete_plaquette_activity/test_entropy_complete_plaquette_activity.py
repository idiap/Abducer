import unittest,math
from entropy_complete_plaquette_activity import *
class Tests(unittest.TestCase):
 def test_entropy_reduces_rate(self):
  c=certificate(.01);self.assertLess(c.radial_entropy_rate,c.bare_action_rate)
 def test_deficit_positive(self):self.assertGreater(certificate(.01).radial_entropy_deficit,0)
 def test_action_closes_at_eta(self):self.assertTrue(calibration()["action_only_would_close"])
 def test_entropy_fails_at_eta(self):self.assertFalse(calibration()["entropy_complete_closes"])
 def test_threshold_order(self):self.assertGreater(calibration()["required_free_energy_radius"],calibration()["entropy_convergence_radius"])
 def test_gap_positive(self):self.assertGreater(calibration()["gap_from_coherent_eta_to_required_radius"],0)
 def test_rate_threshold(self):
  r=radius_for_rate(ALPHA+2*math.log(DEGREE));self.assertAlmostEqual(radial_gaussian_rate(r*r/T,3),ALPHA+2*math.log(DEGREE),places=10)
 def test_free_threshold(self):self.assertAlmostEqual(certificate(radius_for_root_free_energy()).entropy_complete_root_free_energy,F_REQUIRED,places=10)
 def test_supercritical_free_energy(self):self.assertIsNone(certificate(.001).entropy_complete_root_free_energy)
 def test_invalid_radius(self):
  with self.assertRaises(ValueError):certificate(0)
 def test_invalid_rate(self):
  with self.assertRaises(ValueError):radius_for_rate(-1)
 def test_scope(self):self.assertFalse(calibration()["nonlinear_su2_partition_activity_proved"])
if __name__=="__main__":unittest.main()
