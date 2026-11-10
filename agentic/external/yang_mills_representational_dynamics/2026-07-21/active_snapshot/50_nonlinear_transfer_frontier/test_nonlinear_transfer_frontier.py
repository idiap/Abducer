import unittest
from nonlinear_transfer_frontier import *


class Tests(unittest.TestCase):
    def test_ten_stages(self): self.assertEqual(calibration()["frontier"]["stages_composed"],10)
    def test_geometry(self): self.assertTrue(calibration()["frontier"]["nonlinear_variance_geometry_proved"])
    def test_transfer_theorem(self): self.assertTrue(calibration()["frontier"]["normalized_tail_transfer_theorem_proved"])
    def test_restricted_closure(self): self.assertTrue(calibration()["frontier"]["restricted_continuous_channel_closed"])
    def test_physical_transfer_open(self): self.assertFalse(calibration()["frontier"]["physical_boundary_uniform_transfer_proved"])
    def test_ideal_repair(self): self.assertTrue(calibration()["frontier"]["ideal_tangent_repair_closed"])
    def test_link_repair_fails(self): self.assertFalse(calibration()["frontier"]["generic_single_star_link_repair_closed"])
    def test_repair_criterion(self): self.assertTrue(calibration()["frontier"]["coordinated_repair_criterion_proved"])
    def test_history_open(self): self.assertFalse(calibration()["frontier"]["physical_history_table_proved"])
    def test_center_barrier(self): self.assertTrue(calibration()["frontier"]["center_sector_minimum_barriers_proved"])
    def test_center_ratio_open(self): self.assertFalse(calibration()["frontier"]["center_sector_partition_ratios_proved"])
    def test_integer_needed(self): self.assertTrue(calibration()["frontier"]["integer_topology_carrier_required"])
    def test_topology_open(self): self.assertFalse(calibration()["frontier"]["complete_nonabelian_topology_controlled"])
    def test_no_basin(self): self.assertFalse(calibration()["frontier"]["one_scale_basin_entry_proved"])
    def test_no_gap(self): self.assertFalse(calibration()["frontier"]["continuum_mass_gap_proved"])


if __name__ == "__main__": unittest.main()
