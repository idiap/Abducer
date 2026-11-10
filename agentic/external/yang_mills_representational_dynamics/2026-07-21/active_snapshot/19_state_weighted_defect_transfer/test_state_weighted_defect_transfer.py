import itertools
import math
import unittest

import numpy as np

from state_weighted_defect_transfer import (
    alternating_cost_kernel,
    bad_chain_probability_upper,
    cluster_certificate,
    is_connected_subset,
    moment_only_counterexample,
    rooted_connected_set_count_upper,
    validate_bad_kernel,
    weighted_kernel_certificate,
)


class WeightedTransferTests(unittest.TestCase):
    def test_alternating_kernel_has_forced_scalar_step(self):
        q, v = alternating_cost_kernel(0.01)
        cert = weighted_kernel_certificate(q, v)
        self.assertAlmostEqual(cert.scalar_row_ceiling, 1.0)
        self.assertAlmostEqual(cert.weighted_ceiling, 0.01)

    def test_weighted_ceiling_matches_spectral_radius(self):
        q, v = alternating_cost_kernel(0.002430277501841998)
        cert = weighted_kernel_certificate(q, v)
        self.assertAlmostEqual(cert.weighted_ceiling, cert.spectral_radius, places=14)

    def test_two_step_probability_telescopes(self):
        q = 0.02
        matrix, _ = alternating_cost_kernel(q)
        self.assertAlmostEqual(matrix[0, 1] * matrix[1, 0], q**2)
        self.assertAlmostEqual(bad_chain_probability_upper(1.0, q, 2), q**2)

    def test_stage18_threshold_is_subcritical(self):
        cert = cluster_certificate(0.002430277501841998, 18, 0.1)
        self.assertTrue(cert.subcritical)
        self.assertAlmostEqual(cert.branching_ratio, 0.8702225337961371)
        self.assertAlmostEqual(cert.rooted_sum_upper, 0.020695981332153383)

    def test_critical_value_is_rejected_strictly(self):
        qcrit = math.exp(-0.1) / 18**2
        self.assertFalse(cluster_certificate(qcrit, 18, 0.1).subcritical)

    def test_root_moment_scales_cluster_bound(self):
        one = cluster_certificate(0.001, 18, 0.1, 1.0)
        three = cluster_certificate(0.001, 18, 0.1, 3.0)
        self.assertAlmostEqual(three.rooted_sum_upper, 3.0 * one.rooted_sum_upper)

    def test_moment_counterexample(self):
        result = moment_only_counterexample()
        self.assertTrue(result["intersection_moments_hold"])
        self.assertFalse(result["bernoulli_domination_holds"])
        self.assertGreater(result["p_union"], result["bernoulli_union"])

    def test_connected_count_bound_on_cycle(self):
        adjacency = [[1, 5], [0, 2], [1, 3], [2, 4], [3, 5], [4, 0]]
        for size in range(1, 7):
            count = sum(
                1
                for subset in itertools.combinations(range(6), size)
                if 0 in subset and is_connected_subset(adjacency, subset)
            )
            self.assertLessEqual(count, rooted_connected_set_count_upper(2, size))

    def test_disconnected_subset_detected(self):
        adjacency = [[1], [0, 2], [1, 3], [2]]
        self.assertFalse(is_connected_subset(adjacency, {0, 3}))

    def test_negative_kernel_rejected(self):
        with self.assertRaises(ValueError):
            validate_bad_kernel([[0.0, -0.1], [0.0, 0.0]])

    def test_superprobability_row_rejected(self):
        with self.assertRaises(ValueError):
            validate_bad_kernel([[0.7, 0.4], [0.0, 0.0]])

    def test_invalid_weight_rejected(self):
        with self.assertRaises(ValueError):
            weighted_kernel_certificate(np.eye(2), [1.0, 0.0])

    def test_supercritical_cluster_has_infinite_bound(self):
        cert = cluster_certificate(0.01, 18, 0.1)
        self.assertFalse(cert.subcritical)
        self.assertTrue(math.isinf(cert.rooted_sum_upper))


if __name__ == "__main__":
    unittest.main()

