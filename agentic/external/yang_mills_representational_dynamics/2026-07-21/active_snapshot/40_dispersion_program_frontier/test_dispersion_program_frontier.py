import unittest
from dispersion_program_frontier import *
class Tests(unittest.TestCase):
 def test_ten_stages(self):self.assertEqual(frontier().stages_composed,10)
 def test_charge(self):self.assertTrue(frontier().corrected_covering_charge)
 def test_low_closed(self):self.assertTrue(frontier().low_dispersion_conditional_closed)
 def test_action_route(self):self.assertTrue(frontier().action_only_plaquette_route_closed)
 def test_entropy_route_fails(self):self.assertFalse(frontier().entropy_complete_plaquette_route_closed)
 def test_dispersion_gaussian_closes(self):self.assertTrue(frontier().dependent_gaussian_dispersion_split_closed)
 def test_adaptive_theorem(self):self.assertTrue(frontier().adaptive_implication_proved)
 def test_physical_history_open(self):self.assertFalse(frontier().physical_history_premise_proved)
 def test_repair_theorem(self):self.assertTrue(frontier().repair_congestion_theorem_proved)
 def test_repair_physical_open(self):self.assertFalse(frontier().physical_repair_map_proved)
 def test_flux(self):self.assertTrue(frontier().center_flux_carrier_proved)
 def test_instanton_open(self):self.assertFalse(frontier().integer_topology_controlled)
 def test_no_basin(self):self.assertFalse(frontier().one_scale_basin_entry_proved)
 def test_no_gap(self):self.assertFalse(frontier().continuum_mass_gap_proved)
 def test_interval(self):
  lo,hi=calibration()["gaussian_common_interval"];self.assertLess(lo,hi)
if __name__=="__main__":unittest.main()
