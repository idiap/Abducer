import itertools
import math
import unittest

from adaptive_stochastic_domination import (
    all_intersection_moments_bounded,
    calibration,
    domination_budget,
    intersection_probability,
    maximum_history_conditional,
    moment_counterexample,
    union_probability,
)


def bernoulli_product(n, q):
    return {
        state: math.prod(q if bit else 1 - q for bit in state)
        for state in itertools.product((0, 1), repeat=n)
    }


class DistributionTests(unittest.TestCase):
    def test_product_field_has_history_bound_q(self):
        distribution = bernoulli_product(4, 0.2)
        self.assertAlmostEqual(maximum_history_conditional(distribution), 0.2)

    def test_product_intersection_probability(self):
        distribution = bernoulli_product(3, 0.3)
        self.assertAlmostEqual(intersection_probability(distribution, (0, 2)), 0.3**2)

    def test_union_probability_for_product_field(self):
        distribution = bernoulli_product(3, 0.3)
        self.assertAlmostEqual(union_probability(distribution), 1 - 0.7**3)

    def test_invalid_distribution_fails_closed(self):
        with self.assertRaises(ValueError):
            maximum_history_conditional({(0,): 0.2, (1,): 0.2})

    def test_invalid_order_fails_closed(self):
        with self.assertRaises(ValueError):
            maximum_history_conditional(bernoulli_product(2, 0.5), (0, 0))


class CounterexampleTests(unittest.TestCase):
    def test_all_intersection_moment_bounds_hold(self):
        distribution = {(1, 0): 0.5, (0, 1): 0.5}
        self.assertTrue(all_intersection_moments_bounded(distribution, 0.5))

    def test_union_event_blocks_stochastic_domination(self):
        cert = moment_counterexample()
        self.assertEqual(cert.actual_union_probability, 1.0)
        self.assertEqual(cert.iid_union_probability, 0.75)
        self.assertFalse(cert.stochastic_domination_holds)

    def test_history_conditional_detects_hidden_anticorrelation(self):
        self.assertEqual(moment_counterexample().maximum_history_conditional, 1.0)

    def test_moments_are_not_reported_as_sufficient(self):
        self.assertFalse(moment_counterexample().moment_bounds_suffice_for_domination)


class BudgetTests(unittest.TestCase):
    def test_stage14_weight_is_subcritical_under_adaptive_premise(self):
        result = calibration()
        self.assertTrue(result.domination_budget.subcritical)
        self.assertTrue(result.abstract_conversion_gate_closed)

    def test_shared_uniform_theorem_avoids_mayer_identification(self):
        budget = domination_budget(1e-4)
        self.assertTrue(budget.shared_uniform_coupling_theorem_proved)
        self.assertFalse(budget.mayer_activity_identification_required)

    def test_supercritical_weight_has_infinite_rooted_bound(self):
        budget = domination_budget(0.1)
        self.assertFalse(budget.subcritical)
        self.assertTrue(math.isinf(budget.rooted_connected_sum_upper))

    def test_unverified_premise_blocks_domination_conclusion(self):
        budget = domination_budget(1e-4, adaptive_history_bound_verified=False)
        self.assertFalse(budget.stochastic_domination_conclusion_under_premise)

    def test_calibration_does_not_promote_to_full_su2(self):
        result = calibration()
        self.assertFalse(result.full_su2_adaptive_history_bound_verified)
        self.assertFalse(result.full_su2_stochastic_domination_verified)

    def test_invalid_budget_fails_closed(self):
        for value in (-0.1, 1.0):
            with self.assertRaises(ValueError):
                domination_budget(value)


if __name__ == "__main__":
    unittest.main()
