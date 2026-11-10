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
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic_common import load_json_object  # noqa: E402
from build_public_reasoning_monitor_packet import build_packet  # noqa: E402
from reasoning_trace_adapters import assemble_named_workflow_trace  # noqa: E402
from reasoning_trace_adapters import adapt_legacy_projection  # noqa: E402


class PublicReasoningTraceAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_json_object(ROOT / "agentic/registries/named_workflow_contracts.yaml")
        cls.contracts = load_json_object(ROOT / "agentic/registries/named_workflow_trace_contracts.yaml")
        cls.lenses = load_json_object(ROOT / "agentic/registries/reasoning_trace_lenses.yaml")

    def events(self) -> list[dict]:
        return [
            {"event_id": "control-1", "run_id": "run-1", "sequence": 1, "event_family": "authorization",
             "step_id": "orchestrate_delivery", "workflow_disposition": "allowed"},
            {"event_id": "infer-1", "run_id": "run-1", "sequence": 2, "event_family": "transformation",
             "step_id": "orchestrate_delivery", "parent_event_ids": ["control-1"],
             "question": "Which exact theorem is being delivered?", "premises": ["Statement S"],
             "operator": "decompose_exact_statement", "warrant": "The queue item fixes S.",
             "conclusion": "Deliver S without strengthening its quantifiers.",
             "claim_epistemic_status": "proposed", "artifact_validation_status": "valid",
             "workflow_disposition": "continue", "scope": {"statement": "S"},
             "evidence": [{"evidence_id": "ev-1", "relation": "supports", "path": "artifacts/proof-queue.json"}],
             "authority": {"exercised": "planning", "absent": ["proof_acceptance"]}},
        ]

    def assemble(self, events: list[dict] | None = None, **kwargs) -> dict:
        return assemble_named_workflow_trace(self.registry, events or self.events(), workflow_id="theorem_proof_delivery",
                                             run_id="run-1", trace_contracts=self.contracts, **kwargs)

    def test_overlay_is_deterministic_and_preserves_gaps(self) -> None:
        first = self.assemble(); second = self.assemble()
        self.assertEqual(first, second)
        self.assertEqual(first["declared_route"][0]["status"], "observed")
        self.assertFalse(first["declared_route"][0]["observability_gap"])
        self.assertTrue(any(x["step_id"] == "formalize_obligations" for x in first["observability_gaps"]))

    def test_control_success_does_not_manufacture_a_claim(self) -> None:
        trace = self.assemble([self.events()[0]])
        packet = build_packet(trace, self.lenses)
        self.assertEqual(packet["claims"], [])
        self.assertEqual(packet["coverage"]["semantic_covered_steps"], 0)
        self.assertGreater(packet["coverage"]["trace_gaps"], 0)

    def test_canonical_v2_event_preserves_public_rationale_and_causality(self) -> None:
        events = [
            {
                "event_id": "control-v2", "run_id": "run-1", "sequence": 1,
                "timestamp_utc": "2026-08-05T12:00:00+00:00",
                "event_family": "authorization", "step_id": "orchestrate_delivery",
                "workflow_disposition": "authorized",
            },
            {
                "event_id": "inference-v2", "run_id": "run-1", "sequence": 2,
                "timestamp_utc": "2026-08-05T12:00:01+00:00",
                "event_family": "public_inference", "step_id": "orchestrate_delivery",
                "causal_parent_event_ids": ["control-v2"],
                "parent_artifact_ids": ["proof-queue-1"],
                "public_inference": {
                    "question": "Which exact theorem is being delivered?",
                    "premises": [{"type": "artifact", "statement": "Statement S is queued."}],
                    "operator": "decompose_exact_statement", "warrant": "The queue item fixes S.",
                    "conclusion": "Deliver S without strengthening its quantifiers.",
                    "assumptions": [], "alternatives": [], "falsifiers": [],
                    "uncertainty": "Proof is still pending.",
                    "scope": {"regime": "formal", "model": "S", "before": "S", "after": "S"},
                    "trace_completeness": "complete",
                },
                "evidence": [{"relation": "supports", "path": "artifacts/proof-queue.json"}],
                "authority": {"exercised": ["planning"], "absent": ["proof_acceptance"]},
            },
        ]
        trace = self.assemble(events)
        inference = trace["events"][1]
        self.assertEqual(inference["parent_event_ids"], ["control-v2"])
        self.assertEqual(inference["parent_artifact_ids"], ["proof-queue-1"])
        self.assertEqual(inference["warrant"], "The queue item fixes S.")
        self.assertEqual(inference["conclusion"], "Deliver S without strengthening its quantifiers.")
        self.assertEqual(inference["timestamp"], "2026-08-05T12:00:01+00:00")
        packet = build_packet(trace, self.lenses)
        self.assertIn(
            {"source": "control-v2", "target": "inference-v2", "type": "precedes"},
            packet["graph"]["edges"],
        )
        self.assertEqual(packet["claims"][0]["text"], "Deliver S without strengthening its quantifiers.")

    def test_packet_keeps_integrity_and_epistemic_status_separate(self) -> None:
        packet = build_packet(self.assemble(), self.lenses)
        claim = packet["claims"][0]
        self.assertEqual(claim["integrity_status"], "valid")
        self.assertEqual(claim["epistemic_status"], "proposed")
        self.assertEqual(claim["evidence_ids"], ["ev-1"])
        self.assertEqual(packet["lens"]["lens_id"], "theorem_proof_delivery")

    def test_route_a_exposes_specialist_fan_out_join_and_tail(self) -> None:
        trace = assemble_named_workflow_trace(self.registry, [], workflow_id="manuscript_result_elaboration", run_id="route-a-1",
                                              profile_id="route_a", trace_contracts=self.contracts)
        specialist_steps = [r for r in trace["declared_route"] if r["mode"] == "specialist"]
        self.assertEqual(len(specialist_steps), 10)
        packet = build_packet(trace, self.lenses)
        edge_types = {edge["type"] for edge in packet["graph"]["edges"]}
        self.assertTrue({"branches", "joins", "refines"}.issubset(edge_types))
        self.assertEqual(packet["profile_topology"]["specialist_output"], "ResultCandidatePacket")
        self.assertEqual(packet["lens"]["lens_id"], "manuscript_result_elaboration:route_a")

    def test_causal_diagnostics_are_visible(self) -> None:
        events = self.events() + [{"event_id": "bad", "sequence": 3, "event_family": "control", "step_id": "gate_proof", "parent_event_ids": ["missing"]}]
        trace = self.assemble(events)
        self.assertIn("missing_parent", {x["kind"] for x in trace["diagnostics"]})

    def test_every_named_workflow_has_a_declarative_lens(self) -> None:
        expected = {w["id"] for w in self.registry["workflows"]}
        actual = set(self.lenses["lenses"])
        self.assertTrue(expected.issubset(actual))
        self.assertIn("manuscript_result_elaboration:route_a", actual)

    def test_legacy_adapter_is_read_only_and_does_not_invent_claims(self) -> None:
        descriptor = adapt_legacy_projection("yang_mills_monitor", {"version": 1, "candidate_routes": [{"status": "pass"}]},
                                             "agentic/reports/reasoning_monitor/latest.json")
        self.assertTrue(descriptor["read_only"])
        self.assertEqual(descriptor["public_inference_status"], "trace_incomplete")
        self.assertNotIn("claims", descriptor)


if __name__ == "__main__":
    unittest.main()
