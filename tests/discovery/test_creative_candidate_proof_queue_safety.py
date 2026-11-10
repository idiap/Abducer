# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class CreativeCandidateProofQueueSafetyTests(unittest.TestCase):
    def test_proof_queue_candidates_have_no_failed_hard_gates(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        validations = {row["candidate_id"]: row for row in payload["validation_packets"]}
        proof_rankings = [row for row in payload["candidate_rankings"] if row["route_disposition"] == "proof_queue"]
        self.assertTrue(proof_rankings, "fixture should include proof queue dispositions")
        for ranking in proof_rankings:
            packet = validations[ranking["candidate_id"]]
            self.assertNotIn("fail", packet["hard_gates"].values())
            self.assertEqual(packet["hard_gates"]["source_grounding"], "pass")
            self.assertEqual(packet["hard_gates"]["proof_queue_readiness"], "pass")

    def test_exploratory_candidates_do_not_claim_proof_queue(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        candidates = {row["candidate_id"]: row for row in payload["mediation_candidates"]}
        for ranking in payload["candidate_rankings"]:
            candidate = candidates[ranking["candidate_id"]]
            if candidate["creative_operation"] in {"bridge_invention", "abstraction_formation", "carrier_introduction", "analogy_transport"}:
                self.assertNotEqual(ranking["route_disposition"], "proof_queue")


if __name__ == "__main__":
    unittest.main()
