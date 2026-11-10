import unittest

from basin_os_frontier import (
    FrontierGates,
    Q_TARGET,
    audit_claim_level,
    calibration,
    cutoff_gap_collapse,
    eigenvalues_symmetric_two,
    one_scale_independence_counterexample,
    os_gap_handoff,
    temporal_gap,
    temporal_transfer,
)


class BasinOSFrontierTests(unittest.TestCase):
    def test_temporal_transfer_is_positive(self):
        top, second = eigenvalues_symmetric_two(temporal_transfer(0.2))
        self.assertGreater(second, 0.0)
        self.assertAlmostEqual(top, 1.0, places=14)

    def test_temporal_gap_is_epsilon(self):
        self.assertAlmostEqual(temporal_gap(0.013), 0.013, places=14)

    def test_one_scale_q_does_not_fix_temporal_gap(self):
        rows = one_scale_independence_counterexample([0.5, 0.001])
        self.assertEqual(rows[0]["spatial_weighted_ceiling"], rows[1]["spatial_weighted_ceiling"])
        self.assertGreater(rows[0]["temporal_gap"], 400 * rows[1]["temporal_gap"])

    def test_regulated_gaps_can_collapse(self):
        rows = cutoff_gap_collapse(12)
        self.assertTrue(all(row["regulated_gap"] > 0.0 for row in rows))
        self.assertLess(rows[-1]["regulated_gap"], rows[0]["regulated_gap"])

    def test_actual_claim_level_is_c2(self):
        gates = FrontierGates(False, False, False, False, False, False, False, False)
        out = audit_claim_level(gates)
        self.assertEqual(out["claim_level"], "C2")

    def test_regulator_ready_level_is_c4(self):
        gates = FrontierGates(True, True, True, True, False, False, False, False)
        self.assertEqual(audit_claim_level(gates)["claim_level"], "C4")

    def test_restricted_continuum_level_is_c5(self):
        gates = FrontierGates(True, True, True, True, True, True, True, False)
        self.assertEqual(audit_claim_level(gates)["claim_level"], "C5")

    def test_clay_level_requires_all_gates(self):
        gates = FrontierGates(True, True, True, True, True, True, True, True)
        self.assertEqual(audit_claim_level(gates)["claim_level"], "C6")

    def test_os_handoff_is_conditional(self):
        self.assertFalse(os_gap_handoff(0.4, False, True, True)["proved"])
        self.assertTrue(os_gap_handoff(0.4, True, True, True)["proved"])

    def test_invalid_mass_rejected(self):
        with self.assertRaises(ValueError):
            os_gap_handoff(0.0, True, True, True)

    def test_guardrails(self):
        self.assertFalse(any(calibration()["guardrails"].values()))


if __name__ == "__main__":
    unittest.main()
