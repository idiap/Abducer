import math, unittest
from frechet_collar_charge import *

class Tests(unittest.TestCase):
 def test_identity(self): self.assertLess(commuting_frechet_certificate((-1.,-.5,.5,1.)).identity_error,1e-14)
 def test_center(self): self.assertAlmostEqual(commuting_frechet_certificate((1.,2.,3.)).frechet_center,2.)
 def test_minimizer(self): self.assertAlmostEqual(commuting_frechet_certificate((1.,2.,3.)).link_energy_minimizer,-2.)
 def test_radius(self): self.assertAlmostEqual(commuting_frechet_certificate((-2.,1.)).covering_radius,1.5)
 def test_factor_two(self): self.assertEqual(covering_charge_certificate(.01).exponent_amplification,2.)
 def test_corrected_charge(self): self.assertAlmostEqual(covering_charge_certificate(.01).corrected_energy_charge,1e-4)
 def test_exponent(self): self.assertAlmostEqual(covering_charge_certificate(.003).corrected_gibbs_exponent,1.5)
 def test_uniform(self): self.assertTrue(covering_charge_certificate(.01).link_value_uniform)
 def test_not_probability(self): self.assertFalse(covering_charge_certificate(.01).normalized_probability_proved)
 def test_frechet_lower(self): self.assertEqual(frechet_energy_lower_bound(.2),.2)
 def test_invalid(self):
  for x in (0,-1,math.inf):
   with self.assertRaises(ValueError): covering_charge_certificate(x)
 def test_invalid_angles(self):
  with self.assertRaises(ValueError): commuting_frechet_certificate((0,4))
 def test_calibration_scope(self): self.assertFalse(calibration()["complete_partition_ratio_proved"])
if __name__=="__main__": unittest.main()
