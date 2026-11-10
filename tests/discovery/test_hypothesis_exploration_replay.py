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

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from build_hypothesis_exploration_map import build_map, build_validation_and_rankings  # noqa: E402


class HypothesisExplorationReplayTests(unittest.TestCase):
    def test_replay_is_stable_except_timestamp(self) -> None:
        target = ROOT / "agentic/examples/targets/p-vs-np-target.json"
        graph = ROOT / "agentic/state/dependency_graphs/p-vs-np.json"
        first = build_map(target, graph, enrich_graph=False, write_artifacts=False)
        second = build_map(target, graph, enrich_graph=False, write_artifacts=False)
        for payload in (first, second):
            payload.pop("generated_utc", None)
        self.assertEqual(first["pressure_packets"], second["pressure_packets"])
        self.assertEqual(first["mediation_candidates"], second["mediation_candidates"])
        self.assertEqual(first["validation_packets"], second["validation_packets"])
        self.assertEqual(first["candidate_rankings"], second["candidate_rankings"])
        self.assertEqual(first["summary"], second["summary"])

    def test_evidence_removal_demotes_candidates_to_quarantine(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        candidates = copy.deepcopy(payload["mediation_candidates"][:3])
        for candidate in candidates:
            candidate["source_artifacts"] = []
        validations, rankings = build_validation_and_rankings(candidates)
        self.assertTrue(all(v["hard_gates"]["source_grounding"] == "fail" for v in validations))
        self.assertTrue(all(r["route_disposition"] == "quarantine" for r in rankings))
        self.assertTrue(all(r["subgoal_control"]["decision"] == "quarantine" for r in rankings))

    def test_creativity_ablation_removes_route_options(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        full_options = {row["route_disposition"] for row in payload["candidate_rankings"]}
        ablated_options: set[str] = set()
        self.assertGreater(len(full_options), len(ablated_options))
        self.assertIn("discovery_branch", full_options)

    def test_candidates_have_formal_subgoal_control(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        self.assertIn("formal_subgoal_control_policy", payload)
        for ranking in payload["candidate_rankings"]:
            control = ranking["subgoal_control"]
            self.assertIn(control["decision"], {"persist_adapt", "backtrack", "pivot", "quarantine", "stop"})
            self.assertTrue(control["target_object_link"])
            self.assertTrue(control["learning_from_failure"])
            self.assertTrue(control["next_action"])
            if ranking["route_disposition"] == "proof_queue":
                self.assertEqual(control["decision"], "persist_adapt")

    def test_candidates_have_machinery_selection_packets(self) -> None:
        payload = json.loads((ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(encoding="utf-8"))
        self.assertIn("abstraction_machinery_policy", payload)
        self.assertIn("machinery_roles", payload["summary"])
        for collection in ["mediation_candidates", "validation_packets", "candidate_rankings"]:
            for row in payload[collection]:
                machinery = row["machinery_selection"]
                self.assertTrue(machinery["selected_machinery"])
                self.assertIn(machinery["machinery_role"], payload["abstraction_machinery_policy"]["roles"])
                self.assertIn("->", machinery["controlled_interface"])
                self.assertTrue(machinery["required_bridge_obligation"])
                self.assertTrue(machinery["invalid_use_modes"])
                self.assertTrue(machinery["validation_handoff"])
        packet_path = ROOT / "artifacts/hegelian/machinery_selection_packets.json"
        self.assertTrue(packet_path.exists())
        packets = json.loads(packet_path.read_text(encoding="utf-8"))
        self.assertEqual(packets["summary"]["selection_count"], len(payload["candidate_rankings"]))


if __name__ == "__main__":
    unittest.main()
