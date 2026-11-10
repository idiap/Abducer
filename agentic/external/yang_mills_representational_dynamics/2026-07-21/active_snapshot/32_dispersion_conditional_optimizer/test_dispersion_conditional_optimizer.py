import math,unittest
from dispersion_conditional_optimizer import *
class Tests(unittest.TestCase):
 def test_effective_radius(self):
  c=certificate(6e-6,.02);self.assertAlmostEqual(c.effective_rms_radius,.001)
 def test_energy_identity(self):
  c=certificate(6e-6,.02);self.assertAlmostEqual(c.denominator_energy_upper,6*(.001+c.selected_delta)**2)
 def test_gap_positive(self): self.assertGreater(certificate(6e-6,.02).finite_time_gap,0)
 def test_probability_nonnegative(self): self.assertGreaterEqual(certificate(6e-6,.02).probability_upper,0)
 def test_action_exponent(self): self.assertAlmostEqual(certificate(6e-6,.02).high_dispersion_action_exponent,1.)
 def test_boundary(self): self.assertGreater(maximum_dispersion_for_target(.0229),0)
 def test_strict_closure(self): self.assertTrue(calibration()["low_dispersion_channel_closed_conditionally"])
 def test_high_open(self): self.assertFalse(calibration()["high_dispersion_normalized_partition_bound_proved"])
 def test_complete_open(self): self.assertFalse(calibration()["complete_su2_kernel_proved"])
 def test_more_dispersion_worse(self):
  self.assertGreater(certificate(1.2e-4,.022).log_probability_upper,certificate(6e-5,.022).log_probability_upper)
 def test_invalid_dispersion(self):
  with self.assertRaises(ValueError):certificate(-1,.02)
 def test_invalid_target(self):
  with self.assertRaises(ValueError):certificate(0,.02,1)
 def test_scope(self): self.assertFalse(certificate(1e-5,.02).high_dispersion_partition_bound_proved)
if __name__=="__main__":unittest.main()
