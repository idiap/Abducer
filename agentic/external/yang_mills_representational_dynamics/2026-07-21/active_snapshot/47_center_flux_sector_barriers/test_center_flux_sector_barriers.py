import unittest
from center_flux_sector_barriers import *


class Tests(unittest.TestCase):
    def test_labels(self): self.assertEqual(validate_label([0]*6),(0,)*6)
    def test_invalid_label(self):
        with self.assertRaises(ValueError): validate_label([0]*5)
    def test_zero_weight(self): self.assertEqual(sector_minimum_weight([0]*6),0)
    def test_single_weight(self): self.assertEqual(sector_minimum_weight([1,0,0,0,0,0]),4)
    def test_all_weight(self): self.assertEqual(sector_minimum_weight([1]*6),24)
    def test_representative_weight(self): self.assertEqual(int(representative([1,0,0,0,0,0]).sum()),4)
    def test_plane_flux_propagates(self): self.assertEqual(plane_fluxes(representative([1,0,0,0,0,0]),0,1),(1,1,1,1))
    def test_cocycles(self): self.assertTrue(certificate().explicit_representatives_are_cocycles)
    def test_exact_preserves(self): self.assertTrue(certificate().exact_coboundaries_preserve_flux)
    def test_binomial_counts(self): self.assertEqual(certificate().weight_multiplicities,(1,6,15,20,15,6,1))
    def test_64_sectors(self): self.assertEqual(certificate().sectors,64)
    def test_ratio_decreases(self): self.assertLess(minimum_representative_ratio(2),minimum_representative_ratio(1))
    def test_ratio_inverse(self): self.assertAlmostEqual(minimum_representative_ratio(charge_for_ratio(.01)),.01,places=12)
    def test_restricted_closes(self): self.assertTrue(calibration()["restricted_minimal_representative_model"]["target_met"])
    def test_full_partition_open(self): self.assertFalse(calibration()["certificate"]["complete_sector_partition_ratio_proved"])


if __name__ == "__main__": unittest.main()
