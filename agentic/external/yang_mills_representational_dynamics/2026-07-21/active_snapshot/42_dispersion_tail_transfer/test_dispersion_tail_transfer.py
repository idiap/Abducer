import unittest
from dispersion_tail_transfer import *


class Tests(unittest.TestCase):
    def test_remainder_positive(self): self.assertGreater(logarithmic_remainder_per_staple(.006), 0)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError): logarithmic_remainder_per_staple(0)
    def test_reference_reduced(self): self.assertLess(reference_rms_threshold(.006, .02, .0003), .006)
    def test_reference_nonnegative(self): self.assertEqual(reference_rms_threshold(.0001, .02, .001), 0)
    def test_event_inclusion(self): self.assertTrue(calibration()["certificate"]["event_inclusion_proved"])
    def test_normalized_theorem(self): self.assertTrue(calibration()["certificate"]["normalized_transfer_theorem_proved"])
    def test_restricted_closes(self): self.assertTrue(calibration()["restricted_centered_reference_high_channel_closed"])
    def test_reference_above_gaussian_minimum(self): self.assertGreater(calibration()["certificate"]["reference_rms_threshold"], .00386)
    def test_full_transfer_open(self): self.assertFalse(calibration()["certificate"]["complete_nonlinear_transfer_proved"])
    def test_density_premise_open(self): self.assertFalse(calibration()["physical_boundary_uniform_density_comparison_proved"])
    def test_complement_premise_open(self): self.assertFalse(calibration()["physical_boundary_uniform_complement_bound_proved"])
    def test_uniform_premises_close_abstractly(self):
        c = calibration()["certificate"]
        x = transfer_certificate(.006, .006023157807602598, c["comparison_log_loss"], c["chart_complement_upper"], c["target_probability"], True, True)
        self.assertTrue(x.complete_nonlinear_transfer_proved)
    def test_bad_probability(self):
        with self.assertRaises(ValueError): transfer_certificate(.006, .006, 0, 1, .1)
    def test_probability_sum(self):
        c = calibration()["certificate"]
        self.assertGreaterEqual(c["transferred_probability_upper"], c["chart_complement_upper"])


if __name__ == "__main__": unittest.main()
