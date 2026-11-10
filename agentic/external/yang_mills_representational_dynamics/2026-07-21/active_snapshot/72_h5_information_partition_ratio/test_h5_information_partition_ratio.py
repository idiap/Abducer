import math
import unittest

from h5_information_partition_ratio import (
    calibration,
    collapsing_normalizer_counterexample,
    condition_on_event,
    data_processing_certificate,
    event_kl_certificate,
    interacting_common_bit_certificate,
    kl_divergence,
    multiplicity_counterexample,
    partition_ratio_certificate,
    product_all_bad_certificate,
    product_tensorization_certificate,
)


class EventKLTests(unittest.TestCase):
    def setUp(self):
        self.mu = [0.1, 0.2, 0.3, 0.4]
        self.event = [False, False, True, True]

    def test_known_kl_value(self):
        self.assertAlmostEqual(kl_divergence([0.5, 0.5], [0.25, 0.75]), 0.14384103622589042)

    def test_support_mismatch_returns_infinity(self):
        self.assertTrue(math.isinf(kl_divergence([0.0, 1.0], [1.0, 0.0])))

    def test_event_chain_rule_for_hostile_candidate(self):
        cert = event_kl_certificate(self.mu, self.event, [0.0, 0.0, 0.01, 0.99])
        self.assertLess(abs(cert["chain_rule_residual"]), 1e-14)
        self.assertGreater(cert["conditional_excess"], 0.0)

    def test_conditioned_measure_is_variational_minimizer(self):
        conditioned, mass = condition_on_event(self.mu, self.event)
        cert = event_kl_certificate(self.mu, self.event, conditioned)
        self.assertTrue(cert["is_minimizer"])
        self.assertAlmostEqual(cert["divergence_to_mu"], -math.log(mass))

    def test_nu_outside_event_is_rejected(self):
        with self.assertRaises(ValueError):
            event_kl_certificate(self.mu, self.event, [0.1, 0.0, 0.4, 0.5])

    def test_zero_mass_event_is_rejected(self):
        with self.assertRaises(ValueError):
            condition_on_event([1.0, 0.0], [False, True])

    def test_unnormalized_distribution_is_rejected(self):
        with self.assertRaises(ValueError):
            kl_divergence([0.4, 0.4], [0.5, 0.5])


class DataProcessingTests(unittest.TestCase):
    def test_strict_coarse_graining(self):
        cert = data_processing_certificate(
            [0.18, 0.12, 0.42, 0.28], [0.1, 0.2, 0.3, 0.4], [0, 0, 1, 1]
        )
        self.assertTrue(cert["passes"])
        self.assertGreater(cert["data_processing_gap"], 0.0)

    def test_identity_map_has_zero_gap(self):
        cert = data_processing_certificate([0.4, 0.6], [0.5, 0.5], ["a", "b"])
        self.assertLess(abs(cert["data_processing_gap"]), 1e-15)

    def test_wrong_label_count_is_rejected(self):
        with self.assertRaises(ValueError):
            data_processing_certificate([0.4, 0.6], [0.5, 0.5], [0])


class PartitionRatioTests(unittest.TestCase):
    def test_probability_ratio_equivalence_at_boundary(self):
        cert = partition_ratio_certificate(3.0, 17.0, 0.15)
        self.assertTrue(cert["equivalence"])
        self.assertTrue(cert["probability_bound"])
        self.assertLess(abs(cert["algebraic_residual"]), 1e-15)

    def test_failed_bound_is_equivalent(self):
        cert = partition_ratio_certificate(4.0, 16.0, 0.15)
        self.assertTrue(cert["equivalence"])
        self.assertFalse(cert["probability_bound"])
        self.assertFalse(cert["ratio_bound"])

    def test_collapsed_or_invalid_partition_is_rejected(self):
        with self.assertRaises(ValueError):
            partition_ratio_certificate(1.0, 0.0, 0.1)
        with self.assertRaises(ValueError):
            partition_ratio_certificate(1.0, 1.0, 1.0)


class ObstructionTests(unittest.TestCase):
    def test_multiplicity_overwhelms_action_five(self):
        cert = multiplicity_counterexample(1000, 5.0)
        self.assertGreater(cert["bad_probability"], 0.87)
        self.assertGreater(cert["entropy_minus_action"], 0.0)

    def test_collapsing_bad_numerator_does_not_suppress_probability(self):
        rows = collapsing_normalizer_counterexample(range(1, 21))
        self.assertLess(rows[-1]["z_bad"], rows[0]["z_bad"])
        self.assertGreater(rows[-1]["bad_probability"], 0.999999)

    def test_invalid_counterexample_level_is_rejected(self):
        with self.assertRaises(ValueError):
            collapsing_normalizer_counterexample([0])


class QuasiFactorizationTests(unittest.TestCase):
    def test_product_tensorization_chain_rule(self):
        local = [[0.8, 0.2], [0.7, 0.3], [0.6, 0.4]]
        nu = [0.22, 0.08, 0.05, 0.15, 0.06, 0.14, 0.10, 0.20]
        cert = product_tensorization_certificate(local, nu)
        self.assertTrue(cert["passes"])
        self.assertLess(abs(cert["chain_rule_residual"]), 1e-14)
        self.assertAlmostEqual(cert["tensorization_gap"], cert["total_correlation"])

    def test_product_all_bad_cost_is_additive(self):
        cert = product_all_bad_certificate(12, 0.2)
        self.assertLess(abs(cert["additivity_residual"]), 1e-14)
        self.assertAlmostEqual(cert["all_bad_probability"], 0.2**12)

    def test_interaction_breaks_product_constant_one(self):
        cert = interacting_common_bit_certificate(8, 0.2)
        self.assertTrue(cert["full_support"])
        self.assertTrue(cert["product_c_qf_one_fails"])
        self.assertLess(cert["admissible_c_qf_ceiling"], 0.126)

    def test_interacting_ceiling_collapses_along_family(self):
        small = interacting_common_bit_certificate(4, 0.2)
        large = interacting_common_bit_certificate(20, 0.2)
        self.assertLess(large["admissible_c_qf_ceiling"], small["admissible_c_qf_ceiling"])
        self.assertAlmostEqual(large["admissible_c_qf_ceiling"], 0.05, places=12)

    def test_full_support_semantics_survive_float_underflow(self):
        cert = interacting_common_bit_certificate(40, 0.2)
        self.assertEqual(cert["regularization_log_epsilon"], -1600)
        self.assertTrue(cert["float_regularization_underflowed"])
        self.assertTrue(cert["full_support"])
        self.assertAlmostEqual(cert["admissible_c_qf_ceiling"], 1.0 / 40.0)

    def test_wrong_joint_dimension_is_rejected(self):
        with self.assertRaises(ValueError):
            product_tensorization_certificate([[0.5, 0.5], [0.5, 0.5]], [0.5, 0.5])


class FrontierTests(unittest.TestCase):
    def test_all_physical_guardrails_remain_false(self):
        self.assertFalse(any(calibration()["guardrails"].values()))


if __name__ == "__main__":
    unittest.main()
