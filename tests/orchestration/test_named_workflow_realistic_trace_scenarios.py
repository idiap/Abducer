#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""End-to-end semantic fixtures for every named workflow and Route-A."""

from __future__ import annotations

import json
import hashlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))
from build_public_reasoning_monitor_packet import build_packet  # noqa: E402
from build_reasoning_trace_coverage import build_coverage  # noqa: E402
from reasoning_trace_adapters import assemble_named_workflow_trace  # noqa: E402
from validate_public_reasoning_trace import validate_trace  # noqa: E402


class NamedWorkflowRealisticTraceScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads((ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text())
        cls.lenses = json.loads((ROOT / "agentic/registries/reasoning_trace_lenses.yaml").read_text())
        cls.trace_contracts = json.loads((ROOT / "agentic/registries/named_workflow_trace_contracts.yaml").read_text())
        cls.cases = json.loads((ROOT / "tests/fixtures/reasoning_trace/named_workflow_semantics.json").read_text())["cases"]

    def _declared_steps(self, case):
        workflow = next(row for row in self.registry["workflows"] if row["id"] == case["workflow_id"])
        if not case.get("profile_id"):
            return workflow["steps"]
        profile = next(row for row in workflow["profiles"] if row["id"] == case["profile_id"])
        start = next(i for i, row in enumerate(workflow["steps"]) if row["id"] == profile["validation_tail_start"])
        specialist = [{"id": skill, "skill": skill, "mode": "specialist", "consumes": ["RouteAOpenPointPlan"], "produces": ["ResultCandidatePacket"]} for skill in profile["specialist_skills"]]
        return profile["steps"] + specialist + workflow["steps"][start:]

    def _trace_requirement(self, case, step):
        """Resolve the canonical expert trace contract for a fixture step."""
        workflow = next(row for row in self.trace_contracts["workflows"] if row["id"] == case["workflow_id"])
        candidates = list(workflow["steps"])
        if case.get("profile_id"):
            profile = next(row for row in workflow["profiles"] if row["id"] == case["profile_id"])
            candidates += profile["steps"] + profile["specialists"]
        return next(
            row for row in candidates
            if row.get("step_id") == step["id"] or row.get("skill") == step["skill"]
        )

    def _events(self, case):
        events = []
        sequence = 1
        previous = None
        for index, step in enumerate(self._declared_steps(case)):
            step_id = step["id"]
            requirement = self._trace_requirement(case, step)
            consumed = (requirement.get("consumes") or step.get("consumes") or ["WorkflowEvidence"])[0]
            produced = (requirement.get("produces") or step.get("produces") or ["WorkflowAssessment"])[0]
            operator = requirement.get("inference_operator") or f"{step_id.replace('_', '-')}-assessment"
            control_id = f"{case['workflow_id']}.{case.get('profile_id', 'base')}.{step_id}.control"
            events.append({"event_id": control_id, "run_id": f"fixture.{case['workflow_id']}.{case.get('profile_id', 'base')}", "sequence": sequence, "event_family": "authorization", "step_id": step_id, "skill": step["skill"], "parent_event_ids": [previous] if previous else [], "workflow_disposition": "authorized"})
            sequence += 1
            semantic_id = control_id.replace(".control", ".inference")
            is_negative = index == max(1, len(self._declared_steps(case)) // 2)
            conclusion = (
                f"{step_id} rejects {produced}: {case['negative']}"
                if is_negative else
                f"{step_id} produces {produced}: {case['conclusion']}"
            )
            events.append({
                "event_id": semantic_id, "run_id": events[-1]["run_id"], "sequence": sequence,
                "event_family": "failure" if is_negative else "inference", "step_id": step_id, "skill": step["skill"],
                "parent_event_ids": [control_id],
                "question": f"At {step_id}, how does {consumed} bear on {produced}? {case['question']}",
                "premises": [{"type": "artifact", "statement": f"{consumed}: {case['premise']}"}],
                "operator": operator,
                "warrant": (
                    f"At {step_id}, {operator} checks {consumed} before emitting {produced}. "
                    f"Authority boundary: {requirement['authority_boundary']}"
                ),
                "conclusion": conclusion,
                "alternatives": [{
                    "candidate": f"Do not emit {produced}: {case['negative']}",
                    "disposition": "rejected" if not is_negative else "accepted",
                    "reason": f"{requirement['required_contrast']} Negative evidence controls promotion."
                }],
                "falsifiers": [case["falsifier"]], "scope": case["scope"], "uncertainty": "bounded by the declared artifact and open obligations",
                "evidence": [{"relation": "refutes" if is_negative else "supports", "path": "tests/fixtures/reasoning_trace/evidence/workflow-evidence.json", "digest": "61c8ddbab2b6d4dded3cbe6cf9348c5fd6c658796985c80675774399043f4a90", "artifact_type": consumed}],
                "artifact_validation_status": "integrity_valid", "claim_epistemic_status": "quarantined" if is_negative else "evidence_backed",
                "workflow_disposition": "failed" if is_negative else "accepted",
                "authority": {"exercised": [f"{step_id}-assessment"], "absent": ["unscoped-epistemic-upgrade"], "prohibitions_checked": ["no hidden scope promotion"]},
                "obligations": [{"requirement": case["falsifier"], "status": "open"}] if is_negative else []
            })
            sequence += 1
            previous = semantic_id
        events.append({"event_id": f"{case['workflow_id']}.handoff", "run_id": events[-1]["run_id"], "sequence": sequence, "event_family": "handoff", "step_id": "", "parent_event_ids": [previous], "conclusion": f"Typed handoff to {case['handoff']}", "warrant": "The exit disposition and open obligations are explicit.", "handoff": {"destination_workflow_id": case["handoff"], "accepted": True}, "workflow_disposition": "handed_off"})
        return events

    def test_every_workflow_builds_a_semantically_distinct_packet(self) -> None:
        self.assertEqual(len(self.cases), 7)
        conclusions = set()
        for case in self.cases:
            with self.subTest(workflow=case["workflow_id"], profile=case.get("profile_id")):
                trace = assemble_named_workflow_trace(
                    self.registry, self._events(case), workflow_id=case["workflow_id"],
                    run_id=f"fixture.{case['workflow_id']}.{case.get('profile_id', 'base')}",
                    profile_id=case.get("profile_id", ""), target=case["target"],
                    trace_contracts=self.trace_contracts,
                )
                packet = build_packet(trace, self.lenses)
                self.assertEqual([issue.render() for issue in validate_trace(trace)], [])
                self.assertEqual(packet["identity"]["workflow_id"], case["workflow_id"])
                self.assertTrue(packet["claims"])
                self.assertTrue(any(row.get("relation") == "refutes" for row in packet["evidence"]))
                self.assertTrue(packet["alternatives_and_failures"])
                self.assertTrue(packet["scope_ledger"])
                self.assertTrue(packet["authority_ledger"])
                self.assertTrue(packet["handoffs"])
                self.assertTrue(any(row.get("requirement") == case["falsifier"] for row in packet["obligations"]))
                self.assertEqual(packet["coverage"]["evidence_resolution"], 1.0)
                self.assertFalse(
                    any(row["claim_id"].endswith(".handoff") for row in packet["claims"]),
                    "control-plane handoffs must not be counted as scientific claims",
                )
                coverage = build_coverage(trace, self.trace_contracts)
                self.assertEqual(coverage["summary"]["semantic_covered"]["percent"], 100.0)
                self.assertEqual(coverage["summary"]["authority_covered"]["percent"], 100.0)
                conclusions.add(case["conclusion"])
        self.assertEqual(len(conclusions), 7)

    def test_fixture_inferences_are_step_specific(self) -> None:
        """A green workflow percentage must not hide copy-pasted rationales."""
        for case in self.cases:
            inferences = [row for row in self._events(case) if row["event_family"] in {"inference", "failure"}]
            with self.subTest(workflow=case["workflow_id"], profile=case.get("profile_id")):
                self.assertEqual(len({row["question"] for row in inferences}), len(inferences))
                self.assertEqual(len({row["warrant"] for row in inferences}), len(inferences))
                self.assertEqual(len({row["conclusion"] for row in inferences}), len(inferences))
                self.assertTrue(all(row["operator"] for row in inferences))

    def test_all_evidence_references_resolve_with_matching_digest(self) -> None:
        for case in self.cases:
            for event in self._events(case):
                for evidence in event.get("evidence", []):
                    path = ROOT / evidence["path"]
                    self.assertTrue(path.is_file(), evidence["path"])
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    self.assertEqual(digest, evidence["digest"])

    def test_route_a_fixture_includes_specialist_provenance(self) -> None:
        case = next(row for row in self.cases if row.get("profile_id") == "route_a")
        events = self._events(case)
        specialists = {row["skill"] for row in events if row.get("skill", "").startswith("routea-")}
        workflow = next(row for row in self.registry["workflows"] if row["id"] == case["workflow_id"])
        profile = next(row for row in workflow["profiles"] if row["id"] == "route_a")
        self.assertTrue(set(profile["specialist_skills"]).issubset(specialists))
        scope_text = json.dumps(events)
        for boundary in ["finite", "continuum", "same-theory", "endpoint"]:
            self.assertIn(boundary, scope_text)


if __name__ == "__main__":
    unittest.main()
