import math
import unittest

import numpy as np

from local_cylinder_comparison import (
    calibration,
    finite_positive_conditional_kernel,
    local_comparison_certificate,
    normalized_restriction_log_loss,
)


class RestrictionTheoremTests(unittest.TestCase):
    def test_zero_losses_give_zero(self):
        self.assertEqual(normalized_restriction_log_loss(0.0, 0.0), 0.0)

    def test_losses_add_in_log_space(self):
        value = normalized_restriction_log_loss(0.3, 0.2)
        self.assertAlmostEqual(value, 0.3 - math.log(0.8))

    def test_complement_one_is_rejected(self):
        with self.assertRaises(ValueError):
            normalized_restriction_log_loss(0.1, 1.0)

    def test_negative_oscillation_is_rejected(self):
        with self.assertRaises(ValueError):
            normalized_restriction_log_loss(-0.1, 0.1)


class LocalCertificateTests(unittest.TestCase):
    def test_per_support_accounting(self):
        cert = local_comparison_certificate(10, 0.1, 2.0, 0.1, 0.2)
        expected = (10 * 2.0 * 0.1**2 - math.log(0.9)) / 10
        self.assertAlmostEqual(cert.log_loss_per_support, expected)

    def test_target_can_close(self):
        cert = local_comparison_certificate(100, 0.01, 1.0, 0.001, 0.2)
        self.assertTrue(cert.target_met)

    def test_full_measure_is_not_promoted(self):
        cert = local_comparison_certificate(5, 0.1, 1.0, 0.1)
        self.assertFalse(cert.full_measure_comparison_proved)

    def test_boundary_uniformity_is_separate(self):
        cert = local_comparison_certificate(5, 0.1, 1.0, 0.1)
        self.assertFalse(cert.uniform_boundary_hypothesis_verified)


class FiniteKernelTests(unittest.TestCase):
    def test_kernel_normalizes_exactly(self):
        probabilities, cert = finite_positive_conditional_kernel([1, 2, 3], [1, 1, 0])
        self.assertAlmostEqual(float(np.sum(probabilities)), 1.0)
        self.assertAlmostEqual(cert.conditional_good_probability, 0.5)
        self.assertTrue(cert.normalized)

    def test_nonpositive_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            finite_positive_conditional_kernel([1, 0], [1, 0])


class FrozenCalibrationTests(unittest.TestCase):
    def test_local_cylinder_loss_is_small(self):
        result = calibration()
        loss = result["comparison"]["log_loss_per_support"]
        self.assertLess(loss, 5.0e-5)
        self.assertTrue(result["frozen_centered_reference_loss_target_closed"])

    def test_global_boundary_uniformity_remains_open(self):
        result = calibration()
        self.assertFalse(result["complete_boundary_uniform_su2_comparison_proved"])


if __name__ == "__main__":
    unittest.main()
