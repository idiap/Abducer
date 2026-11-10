import unittest,math
from linearized_dispersion_spectrum import *
class Tests(unittest.TestCase):
 def test_eight_interior_links(self):self.assertEqual(spectrum_certificate().six_staple_links,8)
 def test_rank_five(self):self.assertEqual(len(spectrum_certificate().nonzero_eigenvalues),5)
 def test_contraction(self):self.assertLessEqual(spectrum_certificate().maximum_eigenvalue,1+1e-10)
 def test_positive_spectrum(self):self.assertGreater(min(spectrum_certificate().nonzero_eigenvalues),0)
 def test_zero_below_mean(self):self.assertEqual(chernoff_rate(spectrum_certificate().nonzero_eigenvalues,1e-9),0)
 def test_rate_increases(self):
  v=spectrum_certificate().nonzero_eigenvalues;self.assertGreater(chernoff_rate(v,2e-4),chernoff_rate(v,1e-4))
 def test_upper_converges(self):self.assertTrue(calibration()["upper_endpoint_tail"]["entropy_convergent"])
 def test_upper_meets_free_energy(self):self.assertTrue(calibration()["upper_endpoint_tail"]["required_free_energy_met"])
 def test_interval_nonempty(self):self.assertTrue(calibration()["common_dispersion_parameter_exists"])
 def test_midpoint_meets(self):self.assertTrue(calibration()["selected_midpoint_tail"]["required_free_energy_met"])
 def test_threshold(self):self.assertAlmostEqual(tail_certificate(radius_for_free_energy()).rooted_free_energy_lower,F_REQUIRED,places=9)
 def test_dependence_retained(self):self.assertTrue(tail_certificate(.006).dependence_retained)
 def test_nonlinear_open(self):self.assertFalse(tail_certificate(.006).nonlinear_su2_transfer_proved)
 def test_invalid_radius(self):
  with self.assertRaises(ValueError):tail_certificate(0)
 def test_invalid_chernoff(self):
  with self.assertRaises(ValueError):chernoff_rate((),1)
if __name__=="__main__":unittest.main()
