import math
import unittest

from tempered_equivalence import (
    additive_error_countermodel,
    calibration,
    changing_space_example,
    duhamel_certificate,
    equivalence_constants,
    exact_weighted_ceiling,
    exponentially_weighted_error_budget,
    non_tempered_chart_countermodel,
    scalar_coboundary_example,
    state_dependent_equivalence_certificate,
    support_growth_countermodel,
    zero_error_without_homogeneous_rate_countermodel,
)


class StateDependentEquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.kernels = [
            [[0.10, 0.08, 0.02], [0.03, 0.20, 0.04]],
            [[0.15, 0.02], [0.01, 0.12], [0.06, 0.03]],
            [[0.11], [0.09]],
        ]
        self.v = [[1.0, 2.0], [1.5, 2.5, 4.0], [1.2, 3.0], [2.0]]
        self.w = [[1.1, 1.7], [2.1, 2.0, 5.2], [1.8, 2.4], [2.6]]

    def test_sharp_equivalence_constants(self):
        a, b = equivalence_constants([1.0, 2.0, 4.0], [2.0, 1.0, 6.0])
        self.assertEqual(a, 0.5)
        self.assertEqual(b, 2.0)

    def test_changing_dimensions_and_step_bounds(self):
        cert = state_dependent_equivalence_certificate(
            self.kernels, self.v, self.w, [0.5, 1.0, 1.5]
        )
        self.assertEqual(cert.dimensions, [2, 3, 2, 1])
        self.assertTrue(cert.step_bounds_hold)
        self.assertTrue(cert.product_bounds_hold)

    def test_centered_log_decomposition(self):
        cert = state_dependent_equivalence_certificate(
            self.kernels, self.v, self.w, [0.5, 1.0, 1.5]
        )
        direct = math.log(cert.w_product_ceiling / cert.v_product_ceiling)
        self.assertAlmostEqual(
            direct,
            cert.endpoint_log_coboundary + cert.exact_centered_log_distortion,
            places=14,
        )
        self.assertTrue(cert.centered_log_bound_holds)
        self.assertLessEqual(
            abs(cert.rate_remainder), cert.rate_remainder_bound + 1.0e-14
        )

    def test_constant_state_dependent_equivalence_has_linear_width_budget(self):
        kernels = [[[0.5, 0.0], [0.0, 0.5]]] * 30
        v = [[1.0, 1.0]] * 31
        w = [[1.0, 2.0]] * 31
        cert = state_dependent_equivalence_certificate(kernels, v, w, [1.0] * 30)
        self.assertAlmostEqual(cert.endpoint_log_coboundary, 0.0)
        self.assertAlmostEqual(cert.cumulative_projective_width / 30.0, math.log(2.0))
        # The robust theorem refuses to call a uniformly wide chart tempered
        # per unit step, even though this diagonal example happens to cancel.
        self.assertAlmostEqual(cert.v_physical_rate, cert.w_physical_rate)

    def test_scalar_coboundary_telescopes_exactly(self):
        result = scalar_coboundary_example(80, 0.72)
        cert = result["certificate"]
        self.assertTrue(result["projective_width_zero"])
        self.assertAlmostEqual(
            result["exact_product_ratio"], result["endpoint_scalar_ratio"], places=13
        )
        self.assertAlmostEqual(cert["exact_centered_log_distortion"], 0.0, places=13)

    def test_tempered_scalar_endpoint_vanishes_per_length(self):
        short = scalar_coboundary_example(16)["tempered_endpoint_log_per_length"]
        long = scalar_coboundary_example(1024)["tempered_endpoint_log_per_length"]
        self.assertLess(long, short / 5.0)

    def test_exact_ceiling(self):
        q = exact_weighted_ceiling([[0.0, 0.04], [1.0, 0.0]], [1.0, 1.0], [1.0, 5.0])
        self.assertEqual(q, 1.0)

    def test_changing_example_serializable_scalars(self):
        result = changing_space_example()
        self.assertTrue(result["step_bounds_hold"])
        self.assertTrue(result["centered_log_bound_holds"])


class AdditiveAndCountermodelTests(unittest.TestCase):
    def test_duhamel_identity_nonstationary(self):
        cert = duhamel_certificate([0.5, 0.2, 0.8], [0.1, 0.03, 0.04], 2.0)
        self.assertLess(cert.identity_error, 1.0e-15)
        self.assertAlmostEqual(cert.exact_iterate, cert.duhamel_sum, places=15)

    def test_exponentially_weighted_budget(self):
        budget = exponentially_weighted_error_budget(
            [math.exp(-2.0), math.exp(-4.0)], [1.0, 2.0], 1.0
        )
        self.assertAlmostEqual(budget, math.exp(-1.0) + math.exp(-2.0))

    def test_summable_additive_errors_destroy_rate(self):
        result = additive_error_countermodel()
        rates = [row["effective_rate"] for row in result["rows"]]
        self.assertTrue(all(a > b for a, b in zip(rates, rates[1:])))
        self.assertLess(result["last_effective_rate"], 0.03)
        self.assertGreater(
            result["rows"][-1]["target_weighted_budget"],
            result["rows"][0]["target_weighted_budget"],
        )

    def test_zero_errors_do_not_replace_homogeneous_decay(self):
        cert = zero_error_without_homogeneous_rate_countermodel(32)
        self.assertEqual(cert["exponentially_weighted_error_budget"], 0.0)
        self.assertEqual(cert["homogeneous_product"], 1.0)
        self.assertEqual(cert["terminal_iterate"], 1.0)
        self.assertEqual(cert["terminal_effective_rate"], 0.0)
        self.assertFalse(cert["target_positive_rate_certified"])

    def test_non_tempered_chart_manufactures_raw_mass(self):
        result = non_tempered_chart_countermodel(50, 0.37)
        self.assertAlmostEqual(result["v_raw_rate"], 0.0)
        self.assertAlmostEqual(result["w_raw_rate"], 0.37, places=13)
        self.assertAlmostEqual(result["root_times_product"], 1.0, places=12)
        self.assertAlmostEqual(result["physical_identity_correlation"], 1.0)

    def test_support_growth_exactly_cancels(self):
        result = support_growth_countermodel(30.0, 0.8, 0.8)
        self.assertAlmostEqual(result["observed_bound"], 1.0, places=13)
        self.assertAlmostEqual(result["observed_effective_rate"], 0.0, places=13)

    def test_support_growth_can_overrun(self):
        result = support_growth_countermodel(30.0, 0.8, 1.0)
        self.assertGreater(result["observed_bound"], 1.0)
        self.assertAlmostEqual(result["observed_effective_rate"], -0.2, places=13)

    def test_guardrails_stay_false(self):
        self.assertTrue(all(value is False for value in calibration()["guardrails"].values()))


class HostileValidationTests(unittest.TestCase):
    def test_reject_nonpositive_weight(self):
        with self.assertRaises(ValueError):
            equivalence_constants([1.0, 0.0], [1.0, 1.0])

    def test_reject_weight_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            equivalence_constants([1.0], [1.0, 2.0])

    def test_reject_kernel_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            state_dependent_equivalence_certificate(
                [[[0.2, 0.3]]], [[1.0], [1.0]], [[1.0], [1.0]], [1.0]
            )

    def test_reject_negative_kernel_entry(self):
        with self.assertRaises(ValueError):
            exact_weighted_ceiling([[-0.1]], [1.0], [1.0])

    def test_reject_superprobability_row(self):
        with self.assertRaises(ValueError):
            exact_weighted_ceiling([[1.01]], [1.0], [1.0])

    def test_reject_zero_logarithmic_ceiling(self):
        with self.assertRaises(ValueError):
            exact_weighted_ceiling([[0.0]], [1.0], [1.0])

    def test_reject_nonpositive_length(self):
        with self.assertRaises(ValueError):
            state_dependent_equivalence_certificate(
                [[[0.5]]], [[1.0], [1.0]], [[1.0], [1.0]], [0.0]
            )

    def test_reject_mismatched_duhamel_inputs(self):
        with self.assertRaises(ValueError):
            duhamel_certificate([0.5], [0.1, 0.2], 1.0)

    def test_reject_negative_additive_error(self):
        with self.assertRaises(ValueError):
            duhamel_certificate([0.5], [-0.1], 1.0)


if __name__ == "__main__":
    unittest.main()
