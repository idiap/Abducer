import json
import math
import tempfile
import unittest
from pathlib import Path

import h1_same_measure as h1


class ReflectionPositiveTransferTests(unittest.TestCase):
    def test_primary_transfer_is_symmetric_positive_definite(self):
        transfer, _ = h1.rare_sector_family(0.05)
        data = h1.spectral_data(transfer)
        self.assertTrue(data["reflection_positive"])
        self.assertGreater(data["minimum_transfer_eigenvalue"], 0.0)
        self.assertLess(data["perron_residual"], 1e-13)
        self.assertLess(data["gram_reconstruction_error"], 1e-15)

    def test_nonsymmetric_transfer_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.validate_transfer([[1.0, 0.1], [0.2, 1.0]])

    def test_indefinite_transfer_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.validate_transfer([[1.0, 2.0], [2.0, 1.0]])

    def test_semidefinite_transfer_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.validate_transfer([[1.0, 1.0], [1.0, 1.0]])

    def test_nonpositive_or_nonfinite_entries_are_rejected(self):
        for matrix in (
            [[1.0, 0.0], [0.0, 1.0]],
            [[1.0, -0.1], [-0.1, 1.0]],
            [[1.0, math.inf], [math.inf, 1.0]],
        ):
            with self.subTest(matrix=matrix), self.assertRaises(ValueError):
                h1.validate_transfer(matrix)


class SameMeasureIdentityTests(unittest.TestCase):
    def setUp(self):
        transfer, mask = h1.rare_sector_family(0.05)
        self.cert = h1.same_measure_certificate(transfer, mask)

    def test_gibbs_and_temporal_kernels_are_identical(self):
        self.assertTrue(self.cert["same_measure_realization"])
        self.assertEqual(self.cert["gibbs_edge_weight"], self.cert["temporal_transfer"])

    def test_doob_is_stochastic_stationary_and_reversible(self):
        checks = self.cert["checks"]
        self.assertLess(checks["doob_row_sum_error"], 1e-13)
        self.assertLess(checks["stationarity_error"], 1e-13)
        self.assertLess(checks["detailed_balance_error"], 1e-13)

    def test_bad_kernel_is_masked_doob_subkernel(self):
        self.assertTrue(self.cert["checks"]["bad_is_doob_subkernel"])
        for bad_row, doob_row in zip(self.cert["bad_subkernel"], self.cert["doob_kernel"]):
            for bad, full in zip(bad_row, doob_row):
                self.assertLessEqual(bad, full)

    def test_inverse_vacuum_identity_is_exact(self):
        self.assertLess(self.cert["checks"]["inverse_vacuum_identity_error"], 1e-13)
        self.assertEqual(len(self.cert["weighted_bad_ratios"]), 2)
        for left, right in zip(
            self.cert["weighted_bad_ratios"], self.cert["masked_transfer_rows_over_lambda0"]
        ):
            self.assertAlmostEqual(left, right, places=14)

    def test_inverse_weight_is_nontrivial_and_root_moment_finite(self):
        weight = self.cert["inverse_vacuum_weight"]
        self.assertEqual(min(weight), 1.0)
        self.assertGreater(max(weight), 10.0)
        self.assertTrue(math.isfinite(self.cert["stationary_root_moment"]))
        expected = sum(
            p * v for p, v in zip(self.cert["stationary_state"], self.cert["inverse_vacuum_weight"])
        )
        self.assertAlmostEqual(self.cert["stationary_root_moment"], expected, places=14)

    def test_mask_outside_unit_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.same_measure_certificate([[1.0, 0.1], [0.1, 0.5]], [[0.0, 1.01], [0.0, 0.0]])

    def test_wrong_shape_mask_is_rejected(self):
        with self.assertRaises(ValueError):
            h1.same_measure_certificate([[1.0, 0.1], [0.1, 0.5]], [[1.0]])


class TemporalCountermodelTests(unittest.TestCase):
    def test_exact_counterfamily_formulas(self):
        for delta in (0.5, 0.1, 1e-3):
            with self.subTest(delta=delta):
                row = h1.counterfamily_row(delta)
                self.assertLess(row["q_error"], 1e-14)
                self.assertLess(row["gap_error"], 1e-13)

    def test_small_bad_ceiling_and_gap_both_tend_down(self):
        result = h1.implication_counterexample(16)
        self.assertTrue(result["q_strictly_decreases"])
        self.assertTrue(result["gap_strictly_decreases"])
        self.assertLess(result["last_q"], 2e-5)
        self.assertLess(result["last_gap"], 4e-5)
        self.assertFalse(result["uniform_positive_gap_forced_by_q_upper_bound"])

    def test_each_countermodel_has_unique_vacuum_and_positive_gap(self):
        for delta in (0.25, 0.01, 1e-5):
            transfer, mask = h1.closing_gap_family(delta)
            cert = h1.same_measure_certificate(transfer, mask)
            self.assertTrue(cert["spectral"]["vacuum_unique"])
            self.assertGreater(cert["spectral"]["temporal_gap"], 0.0)
            self.assertTrue(cert["spectral"]["reflection_positive"])

    def test_family_endpoints_and_invalid_level_count_are_rejected(self):
        for delta in (0.0, 1.0, -0.1, math.nan):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                h1.closing_gap_family(delta)
        with self.assertRaises(ValueError):
            h1.implication_counterexample(1)


class SerializationAndScopeTests(unittest.TestCase):
    def test_result_serializes_and_round_trips(self):
        result = h1.calibration()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "result.json"
            target.write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["stage"], 68)

    def test_physical_guardrails_remain_false(self):
        guardrails = h1.calibration()["guardrails"]
        self.assertTrue(guardrails["finite_reflection_positive_calibration"])
        self.assertTrue(guardrails["bad_subkernel_from_same_finite_measure"])
        for name in (
            "physical_su2_retained_kernel_constructed",
            "boundary_uniform_root_moment_proved",
            "cutoff_uniform_temporal_gap_proved",
            "continuum_measure_constructed",
            "os_axioms_verified",
            "stochastic_domination_inferred_from_moments",
            "yang_mills_mass_gap_proved",
        ):
            self.assertFalse(guardrails[name], name)


if __name__ == "__main__":
    unittest.main()
