import unittest,numpy as np
from canonical_plaquette_witness import *
class Tests(unittest.TestCase):
 def test_counts(self):self.assertEqual(len(incidence_sets()),216)
 def test_plaquettes(self):self.assertEqual(len(plaquette_boundary_links()),216)
 def test_capacity(self):self.assertEqual(max(map(len,plaquette_boundary_links())),4)
 def test_boundary_degree(self):self.assertTrue(all(len(x)==4 for x in plaquette_boundary_links()))
 def test_single(self):
  r=np.ones(216);self.assertEqual(len(canonical_witnesses(r,[0],.5)),1)
 def test_tie_lexicographic(self):
  r=np.ones(216);w=canonical_witnesses(r,[0],.5);self.assertEqual(w[0],min(incidence_sets()[0]))
 def test_capacity_sharp(self):self.assertEqual(calibration()["capacity_four_sharpness"]["maximum_witness_multiplicity"],4)
 def test_lower_bound(self):self.assertTrue(calibration()["capacity_four_sharpness"]["capacity_bound_met"])
 def test_gauge_invariant(self):self.assertTrue(calibration()["capacity_four_sharpness"]["gauge_invariant"])
 def test_missing_witness(self):
  with self.assertRaises(ValueError):canonical_witnesses(np.zeros(216),[0],.1)
 def test_invalid_link(self):
  with self.assertRaises(ValueError):canonical_witnesses(np.ones(216),[999],.1)
 def test_invalid_radii(self):
  with self.assertRaises(ValueError):canonical_witnesses([1,2],[0],.1)
 def test_history_open(self):self.assertFalse(calibration()["physical_history_uniform_selection_proved"])
if __name__=="__main__":unittest.main()
