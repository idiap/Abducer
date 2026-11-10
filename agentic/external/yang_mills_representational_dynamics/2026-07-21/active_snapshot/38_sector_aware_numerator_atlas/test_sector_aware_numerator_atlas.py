import unittest,math
from sector_aware_numerator_atlas import *
class Tests(unittest.TestCase):
 def test_union(self):self.assertAlmostEqual(union_ceiling([.1,.2]),.3)
 def test_equal_budget(self):self.assertTrue(all(abs(x-.2) <1e-14 for x in allocation_certificate(.1,[.2]*5).shares))
 def test_exhaustion(self):self.assertTrue(allocation_certificate(.1,[.2]*5).exact_budget_exhausted)
 def test_five_channels(self):self.assertEqual(len(allocation_certificate(.1,[.2]*5).channels),5)
 def test_free_energy(self):self.assertAlmostEqual(allocation_certificate(.1,[.2]*5).required_free_energies[0],-math.log(.02))
 def test_loss_increases_requirement(self):self.assertGreater(allocation_certificate(.1,[.2]*5,[1,0,0,0,0]).required_free_energies[0],allocation_certificate(.1,[.2]*5).required_free_energies[0])
 def test_ownership(self):self.assertTrue(allocation_certificate(.1,[.2]*5).ownership_labels_retained)
 def test_physical_open(self):self.assertFalse(allocation_certificate(.1,[.2]*5).physical_channel_bounds_proved)
 def test_statuses(self):self.assertEqual(len(channel_status()),5)
 def test_total_vs_equal(self):self.assertGreater(calibration()["equal_channel_free_energy_without_loss"],calibration()["single_total_free_energy"])
 def test_invalid_share_sum(self):
  with self.assertRaises(ValueError):allocation_certificate(.1,[.1]*5)
 def test_invalid_ratio(self):
  with self.assertRaises(ValueError):union_ceiling([-.1])
 def test_calibration_open(self):self.assertFalse(calibration()["physical_union_bound_proved"])
if __name__=="__main__":unittest.main()
