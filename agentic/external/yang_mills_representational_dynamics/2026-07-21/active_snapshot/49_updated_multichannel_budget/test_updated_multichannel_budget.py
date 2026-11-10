import unittest
from updated_multichannel_budget import *


class Tests(unittest.TestCase):
    def test_identity(self): self.assertTrue(calibration()["allocation"]["exact_budget_identity"])
    def test_residual_positive(self): self.assertGreater(calibration()["allocation"]["residual_budget"],0)
    def test_three_open_channels(self): self.assertEqual(len(calibration()["allocation"]["open_channels"]),3)
    def test_equal_ceilings(self): self.assertEqual(len(set(calibration()["allocation"]["channel_ceilings"])),1)
    def test_free_energy_positive(self): self.assertGreater(min(calibration()["allocation"]["required_free_energies"]),0)
    def test_continuous_releases_budget(self): self.assertTrue(calibration()["restricted_continuous_bound_releases_budget"])
    def test_single_star_unavailable(self): self.assertFalse(calibration()["single_star_repair_available_as_channel_bound"])
    def test_physical_open(self): self.assertFalse(calibration()["complete_physical_multichannel_ratio_proved"])
    def test_bad_shares(self):
        with self.assertRaises(ValueError): residual_allocation(.1,{"x":.01},["a","b"],[.2,.2])
    def test_exhausted(self):
        with self.assertRaises(ValueError): residual_allocation(.1,{"x":.1},["a"],[1])
    def test_negative(self):
        with self.assertRaises(ValueError): residual_allocation(.1,{"x":-.1},["a"],[1])
    def test_physical_logic(self):
        c=residual_allocation(.1,{"x":.01},["a"],[1],certified_premises_physical=True,open_bounds_proved=True)
        self.assertTrue(c.physical_union_bound_proved)
    def test_center_barrier_recorded(self): self.assertTrue(calibration()["channel_status"][1]["minimum_barrier_proved"])
    def test_integer_carrier_recorded(self): self.assertTrue(calibration()["channel_status"][3]["carrier_required"])


if __name__ == "__main__": unittest.main()
