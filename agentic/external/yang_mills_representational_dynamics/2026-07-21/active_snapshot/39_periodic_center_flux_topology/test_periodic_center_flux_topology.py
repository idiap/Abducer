import unittest,numpy as np
from periodic_center_flux_topology import *
class Tests(unittest.TestCase):
 def test_cell_counts(self):self.assertEqual((certificate().vertices,certificate().edges,certificate().plaquettes,certificate().three_cells,certificate().four_cells),(16,64,96,64,16))
 def test_ranks(self):self.assertEqual(certificate().ranks,(15,45,45,15))
 def test_betti(self):self.assertEqual(certificate().betti_numbers,(1,4,6,4,1))
 def test_complex(self):self.assertTrue(certificate().consecutive_compositions_zero)
 def test_six_fluxes(self):self.assertEqual(certificate().flux_representatives,6)
 def test_independent(self):self.assertTrue(certificate().independent_flux_classes)
 def test_sectors(self):self.assertEqual(certificate().center_flux_sectors,64)
 def test_no_instanton(self):self.assertFalse(certificate().integer_instanton_charge_represented)
 def test_flux_cocycle(self):
  *_,d2,d3=periodic_complex();self.assertFalse((d2@flux_representatives()%2).any())
 def test_augmented_rank(self):self.assertEqual(certificate().augmented_exact_rank,51)
 def test_d1d0(self):
  V,E,P,C,Q,d0,d1,d2,d3=periodic_complex();self.assertFalse((d1@d0%2).any())
 def test_d3d2(self):
  V,E,P,C,Q,d0,d1,d2,d3=periodic_complex();self.assertFalse((d3@d2%2).any())
 def test_labels(self):self.assertEqual(len(calibration()["flux_labels"]),6)
 def test_scope(self):self.assertIn("instanton",calibration()["scope"])
if __name__=="__main__":unittest.main()
