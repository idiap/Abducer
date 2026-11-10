import math
import unittest

import numpy as np

import hypothesis_probes as probes


class HypothesisProbeTests(unittest.TestCase):
    def test_h1_weighted_kernel_beats_scalar_ceiling(self):
        result = probes.h1_vacuum_weight_probe(0.08)
        self.assertTrue(math.isclose(result["weighted_ceiling"], 0.08, rel_tol=1e-13))
        self.assertTrue(math.isclose(result["spectral_radius"], 0.08, rel_tol=1e-13))
        self.assertEqual(result["scalar_row_ceiling"], 1.0)

    def test_h2_uniformity_is_required(self):
        result = probes.h2_lyapunov_gap_probe()
        self.assertTrue(math.isclose(result["uniform_physical_rate"], result["expected_uniform_rate"]))
        self.assertTrue(0.0 < result["finite_horizon_nonuniform_rate"] < 0.02)
        self.assertEqual(result["asymptotic_nonuniform_rate"], 0.0)

    def test_h3_single_star_cross_checks_paper05(self):
        result = probes.h3_polymer_spill_probe()
        self.assertTrue(result["single_star_matches_exact_paper05_spectrum"])
        one = result["nested_polymer_probes"]["one_star"]
        self.assertEqual(one["zero_spill_modes"], 0)
        self.assertEqual(one["positive_modes"], 5)

    def test_h4_center_plus_charge_is_not_compositionally_complete(self):
        result = probes.h4_graded_cocycle_probe()
        collision = result["contextual_collision"]
        self.assertFalse(result["center_plus_pfaffian_is_compositionally_sufficient"])
        self.assertNotEqual(collision["left_blocked_charge"], collision["right_blocked_charge"])

    def test_h5_free_energy_identities_and_entropy_counterexample(self):
        result = probes.h5_free_energy_probe()
        self.assertLess(result["variational_identity_error"], 1e-13)
        self.assertTrue(result["data_processing_verified"])
        self.assertGreater(result["action_only_counterexample"]["normalized_bad_probability"], 0.8)

    def test_h6_representation_paths_do_not_commute(self):
        result = probes.h6_representation_curvature_probe()
        self.assertGreater(result["centering_orientation_commutator_rank"], 0)
        self.assertGreater(result["centering_orientation_commutator_norm"], 0.0)
        self.assertFalse(result["path_independent"])

    def test_h7_two_center_atlas_reconstructs(self):
        result = probes.h7_atlas_locality_probe(1000)
        self.assertLessEqual(result["maximum_two_center_radius"], math.pi / 2 + 1e-13)
        self.assertLess(result["maximum_reconstruction_error"], 1e-12)
        self.assertEqual(result["minus_identity_selected_center"], -1)
        self.assertEqual(result["minus_identity_local_radius"], 0.0)

    def test_h8_refinement_reaches_lumpable_state(self):
        result = probes.h8_completeness_detector_probe()
        self.assertGreater(result["initial_lumpability_defect"], 0.0)
        self.assertEqual(result["final_lumpability_defect"], 0.0)
        self.assertEqual(len(set(result["stable_partition"])), 4)

    def test_h9_incomplete_core_overestimates_gap(self):
        result = probes.h9_os_density_probe()
        self.assertGreater(result["apparent_rate_seen_by_incomplete_high_mode_core"], result["true_nonvacuum_gap"])
        self.assertGreater(result["positive_time_gram_minimum_eigenvalue"], -1e-12)
        self.assertFalse(result["wilson_area_law_used"])

    def test_h10_recovery_is_observable_selective(self):
        result = probes.h10_recovery_probe()
        self.assertLess(result["invariant_observable_recovery_error"], 1e-14)
        self.assertTrue(np.isclose(result["gauge_variant_recovery_error"], 1.0))

    def test_minimal_operator_system_substrate_is_coherent(self):
        result = probes.substrate_operator_system_probe()
        self.assertGreaterEqual(result["minimum_fine_state_eigenvalue"], -1e-14)
        self.assertLess(result["two_step_direct_state_coherence_error"], 1e-14)
        self.assertLess(result["observable_state_pairing_error"], 1e-14)

    def test_complete_result_has_all_hypotheses_and_scope_guardrails(self):
        result = probes.run_all()
        self.assertTrue(set(f"H{i}" for i in range(1, 11)).issubset(result))
        self.assertFalse(result["scope"]["physical_one_scale_basin_entry"])
        self.assertFalse(result["scope"]["continuum_yang_mills"])
        self.assertFalse(result["scope"]["hamiltonian_mass_gap"])


if __name__ == "__main__":
    unittest.main()
