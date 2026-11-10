import math
import unittest

import numpy as np

import h1_vacuum_weight as h1


class VacuumDoobTests(unittest.TestCase):
    def test_transfer_is_positive_definite(self):
        transfer, _ = h1.two_sector_transfer(0.01)
        self.assertGreater(np.linalg.eigvalsh(transfer)[0], 0.0)

    def test_doob_kernel_is_stochastic_and_stationary(self):
        transfer, mask = h1.two_sector_transfer(0.01)
        result = h1.doob_transform(transfer, mask)
        cert = result["certificate"]
        self.assertLess(cert["row_sum_error"], 1e-13)
        self.assertLess(cert["stationarity_error"], 1e-13)
        self.assertLess(cert["detailed_balance_error"], 1e-13)

    def test_inverse_amplitude_identity(self):
        transfer, mask = h1.two_sector_transfer(0.01)
        result = h1.doob_transform(transfer, mask)
        self.assertLess(result["certificate"]["inverse_amplitude_identity_error"], 1e-13)
        self.assertTrue(np.allclose(
            result["weighted_bad_ratios"], result["normalized_transfer_amplitude_rows"]
        ))

    def test_vacuum_is_strictly_positive(self):
        transfer, mask = h1.two_sector_transfer(0.01)
        result = h1.doob_transform(transfer, mask)
        self.assertGreater(min(result["vacuum_amplitude"]), 0.0)
        self.assertGreaterEqual(min(result["forward_cost_weight"]), 1.0)

    def test_zero_vacuum_component_is_rejected(self):
        transfer = [[1.0, 0.0], [0.0, 0.5]]
        mask = [[0.0, 1.0], [0.0, 1.0]]
        with self.assertRaises(ValueError):
            h1.doob_transform(transfer, mask)


class PerronOptimalityTests(unittest.TestCase):
    def test_four_channel_declared_weight_is_perron_optimal(self):
        q = 0.002430277501841998
        kernel, weight = h1.multichannel_star_kernel(q, 4)
        computed, cert = h1.perron_certificate(kernel, weight)
        self.assertTrue(cert.optimal_within_positive_weights)
        self.assertAlmostEqual(cert.spectral_radius, q, places=14)
        self.assertAlmostEqual(cert.weighted_ceiling, q, places=14)
        self.assertAlmostEqual(cert.scalar_row_ceiling, 1.0, places=14)
        self.assertTrue(np.allclose(computed, weight))

    def test_arbitrary_weight_cannot_beat_perron_floor(self):
        q = 0.02
        kernel, _ = h1.multichannel_star_kernel(q, 3)
        _, cert = h1.perron_certificate(kernel, [1.0, 20.0, 30.0, 40.0])
        self.assertGreaterEqual(cert.weighted_ceiling + 1e-13, cert.spectral_radius)
        self.assertFalse(cert.optimal_within_positive_weights)

    def test_bad_superprobability_kernel_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.perron_certificate([[0.0, 1.1], [1.0, 0.0]])


class IterationTests(unittest.TestCase):
    def test_chain_bounds_hold_through_twelve_steps(self):
        kernel, weight = h1.multichannel_star_kernel(0.02, 4)
        result = h1.chain_certificate(kernel, weight, 12)
        self.assertTrue(result["all_bounds_hold"])
        self.assertAlmostEqual(result["rows"][1]["exact_bad_chain_mass"], 0.02**2)

    def test_cluster_threshold_is_strict(self):
        result = h1.cluster_certificate(0.002430277501841998, 18, 0.1)
        self.assertTrue(result.strict_subcritical)
        self.assertLess(result.branching_ratio, 1.0)

    def test_critical_equality_is_not_accepted(self):
        qcrit = math.exp(-0.1) / 18**2
        result = h1.cluster_certificate(qcrit, 18, 0.1)
        self.assertFalse(result.strict_subcritical)


class ConventionAndScopeTests(unittest.TestCase):
    def test_inverse_and_amplitude_roles_are_not_interchangeable(self):
        result = h1.convention_counterexample(0.01)
        self.assertLess(result["inverse_identity_error"], 1e-13)
        self.assertGreater(result["amplitude_identity_error"], 1e-4)

    def test_finite_positivity_is_not_uniformity(self):
        result = h1.nonuniformity_counterexample(20)
        self.assertFalse(result["uniform_weight_bound_exists"])
        self.assertGreater(result["last_maximum_weight"], 1e8)

    def test_calibration_preserves_yang_mills_guardrails(self):
        result = h1.calibration()
        handoff = result["yang_mills_handoff"]
        self.assertFalse(handoff["physical_normalized_bad_kernel_constructed"])
        self.assertFalse(handoff["one_scale_basin_entry"])
        self.assertFalse(handoff["repeated_rg"])
        self.assertFalse(handoff["continuum_os_gap"])

    def test_prior_state_weight_stages_are_consistent(self):
        result = h1.cross_stage_consistency()
        self.assertTrue(result["all_targets_agree"])
        self.assertTrue(result["branching_constants_agree"])


if __name__ == "__main__":
    unittest.main()
