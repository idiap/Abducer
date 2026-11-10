import math
import unittest

from nonlinear_activity_transfer import (
    effective_weight,
    multiscale_composition_certificate,
    transfer_certificate,
)


class EffectiveWeightTests(unittest.TestCase):
    def test_two_channels_add_at_activity_level(self):
        J, kappa, K = 6.0, 0.2, 7.0
        self.assertAlmostEqual(effective_weight(J, kappa, K), math.exp(kappa - J) + math.exp(-K))

    def test_better_gaussian_rate_reduces_weight(self):
        self.assertLess(effective_weight(7.0, 0.2, 7.0), effective_weight(6.0, 0.2, 7.0))

    def test_larger_comparison_loss_increases_weight(self):
        self.assertGreater(effective_weight(7.0, 0.3, 7.0), effective_weight(7.0, 0.2, 7.0))

    def test_larger_collar_rate_reduces_weight(self):
        self.assertLess(effective_weight(7.0, 0.2, 8.0), effective_weight(7.0, 0.2, 7.0))

    def test_invalid_inputs_fail_closed(self):
        for args in ((0.0, 0.2, 7.0), (7.0, -0.1, 7.0), (7.0, 0.2, 0.0)):
            with self.assertRaises(ValueError):
                effective_weight(*args)


class TransferBudgetTests(unittest.TestCase):
    def test_declared_witness_is_subcritical(self):
        cert = transfer_certificate()
        self.assertTrue(cert.abstract_transfer_certified)
        self.assertTrue(cert.declared_parameters_subcritical)
        self.assertGreater(cert.effective_weight_slack, 0.0)
        self.assertLess(cert.rooted_weighted_activity_sum_upper, 1.0)

    def test_critical_weight_is_exact_counting_threshold(self):
        cert = transfer_certificate()
        expected = math.exp(-cert.alpha) / cert.adjacency_degree**2
        self.assertAlmostEqual(cert.critical_effective_weight, expected)

    def test_maximum_kappa_has_positive_budget(self):
        cert = transfer_certificate()
        self.assertGreater(cert.maximum_kappa_without_collar_failures, cert.nonlinear_comparison_loss_kappa)

    def test_minimum_collar_rate_is_below_declared_rate(self):
        cert = transfer_certificate()
        self.assertLess(cert.minimum_K_at_declared_kappa, cert.charged_collar_rate_K)

    def test_excessive_comparison_loss_fails(self):
        cert = transfer_certificate(kappa=1.0)
        self.assertFalse(cert.declared_parameters_subcritical)
        self.assertTrue(math.isinf(cert.minimum_K_at_declared_kappa))

    def test_no_false_su2_or_basin_promotion(self):
        cert = transfer_certificate()
        self.assertFalse(cert.mayer_activity_identification_certified)
        self.assertFalse(cert.nonlinear_su2_hypotheses_verified)
        self.assertFalse(cert.basin_entry_certified)


class MultiscaleTests(unittest.TestCase):
    def test_finite_declared_registry_is_summable(self):
        params = ((7.0, 0.2, 7.2), (7.5, 0.2, 7.7), (8.0, 0.2, 8.2))
        cert = multiscale_composition_certificate(params)
        self.assertTrue(cert.all_declared_scales_subcritical)
        self.assertTrue(cert.finite_registry_summable)
        self.assertEqual(cert.scale_count, 3)

    def test_one_failed_scale_fails_registry(self):
        cert = multiscale_composition_certificate(((7.0, 0.2, 7.2), (4.0, 1.0, 4.0)))
        self.assertFalse(cert.all_declared_scales_subcritical)
        self.assertFalse(cert.finite_registry_summable)

    def test_empty_registry_rejected(self):
        with self.assertRaises(ValueError):
            multiscale_composition_certificate(())

    def test_abstract_sum_does_not_verify_rg_maps(self):
        cert = multiscale_composition_certificate(((7.0, 0.2, 7.2),))
        self.assertFalse(cert.infinite_scale_uniformity_verified)
        self.assertFalse(cert.actual_rg_maps_verified)


if __name__ == "__main__":
    unittest.main()
