from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import unittest

import certified_refinement as cr


class ExactRefinementTests(unittest.TestCase):
    def test_stage52_history_is_reproduced_exactly(self):
        cert = cr.refine_partition(cr.stage52_kernel(), [0, 0, 1, 1])
        self.assertEqual(cert.history, ((0, 0, 1, 1), (0, 0, 1, 2), (0, 1, 2, 3)))
        self.assertEqual(cert.initial_defect, 1)
        self.assertEqual(cert.final_defect, 0)
        self.assertTrue(cert.stable)

    def test_stage52_splits_have_exact_witnesses(self):
        cert = cr.refine_partition(cr.stage52_kernel(), [0, 0, 1, 1])
        self.assertEqual(len(cert.witnesses), 2)
        self.assertTrue(cert.all_witnesses_verified)
        self.assertEqual(
            {(w.left_mass, w.right_mass) for w in cert.witnesses},
            {(Fraction(1), Fraction(0)), (Fraction(1, 10), Fraction(0))},
        )

    def test_tampered_witness_fails_closed(self):
        matrix = cr.stage52_kernel()
        cert = cr.refine_partition(matrix, [0, 0, 1, 1])
        witness = cert.witnesses[0]
        tampered = replace(witness, left_mass=witness.left_mass + 1)
        self.assertFalse(cr.verify_split_witness(matrix, cert.history[0], cert.history[1], tampered))

    def test_monotonicity_and_termination_bound(self):
        cert = cr.refine_partition(cr.stage52_kernel(), [0, 0, 1, 1])
        self.assertTrue(cert.monotone)
        self.assertTrue(cert.terminated)
        self.assertLessEqual(cert.strict_rounds, cert.termination_bound)

    def test_exhaustive_coarsest_stable_certificate(self):
        matrix = cr.stage52_kernel()
        final = cr.refine_partition(matrix, [0, 0, 1, 1]).history[-1]
        result = cr.exhaustive_coarsest_stable_check(matrix, [0, 0, 1, 1], final)
        self.assertEqual(result["partitions_enumerated"], 15)
        self.assertTrue(result["candidate_is_coarsest_stable"])

    def test_exhaustive_checker_rejects_unstable_candidate(self):
        result = cr.exhaustive_coarsest_stable_check(
            cr.stage52_kernel(), [0, 0, 1, 1], [0, 0, 1, 2]
        )
        self.assertFalse(result["candidate_is_coarsest_stable"])

    def test_stage52_permutation_equivariance(self):
        self.assertTrue(cr.equivariance_check(cr.stage52_kernel(), [0, 0, 1, 1], [2, 0, 3, 1]))

    def test_stage18_negative_regression_is_not_overclaimed(self):
        result = cr.stage18_moment_only_regression()
        self.assertTrue(result["indiscrete_partition_stable"])
        self.assertFalse(result["bernoulli_domination_holds"])
        self.assertFalse(result["refinement_detects_missing_history_from_indiscrete_seed"])

    def test_stage19_exact_weighted_identity(self):
        result = cr.stage19_weighted_two_state_regression()
        self.assertTrue(result["exact_QV_equals_qV"])
        self.assertIn("exact rational parsed", result["q_origin"])
        self.assertEqual(result["legacy_display_decimal"], "0.002430277501841998")
        self.assertEqual(result["weighted_row_ratios"], [result["q"], result["q"]])

    def test_stage24_unequal_persistence_splits_all_channels(self):
        result = cr.stage24_unequal_persistence_regression()
        cert = result["unequal_partition_certificate"]
        self.assertEqual(cert["history"], [[0, 1, 1, 1, 1], [0, 1, 2, 3, 4]])
        self.assertTrue(result["weighted_ceiling_at_most_q"])

    def test_stage24_equal_symmetry_and_unequal_equivariance(self):
        result = cr.stage24_unequal_persistence_regression()
        self.assertTrue(result["equal_channel_partition_remains_two_blocks"])
        self.assertTrue(result["equal_channel_symmetry_preserved"])
        self.assertTrue(result["unequal_kernel_relabeling_equivariant"])

    def test_delayed_distinction_saturates_bound(self):
        diagnostics = cr.state_explosion_diagnostics(6)
        self.assertTrue(all(item["bound_saturated"] for item in diagnostics))
        self.assertEqual(diagnostics[-1]["states"], 64)
        self.assertEqual(diagnostics[-1]["final_blocks"], 64)

    def test_invalid_float_input_is_rejected(self):
        with self.assertRaises(TypeError):
            cr.validate_kernel([[0.5, 0.5], [1, 0]])

    def test_negative_and_supermarkov_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            cr.validate_kernel([[1, -1], [0, 1]])
        with self.assertRaises(ValueError):
            cr.validate_kernel([[1, 1], [0, 1]])

    def test_nonsquare_and_partition_mismatch_are_rejected(self):
        with self.assertRaises(ValueError):
            cr.validate_kernel([[1, 0, 0], [0, 1, 0]])
        with self.assertRaises(ValueError):
            cr.refine_partition([[1, 0], [0, 1]], [0])

    def test_bad_permutation_is_rejected(self):
        with self.assertRaises(ValueError):
            cr.permute_kernel(cr.stage52_kernel(), [0, 0, 2, 3])

    def test_large_exhaustive_request_fails_closed(self):
        matrix = cr.delayed_distinction_kernel(9)
        with self.assertRaises(ValueError):
            cr.exhaustive_coarsest_stable_check(matrix, [0] + [1] * 8, list(range(9)))

    def test_scope_guardrails_are_false(self):
        scope = cr.results()["scope"]
        self.assertTrue(scope["abstract_finite_theorem"])
        self.assertFalse(scope["physical_su2_boundary_table_constructed"])
        self.assertFalse(scope["continuum_yang_mills"])
        self.assertFalse(scope["mass_gap"])


if __name__ == "__main__":
    unittest.main()
