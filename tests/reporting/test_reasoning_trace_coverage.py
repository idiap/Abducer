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
"""Coverage accounting keeps control execution separate from public reasoning."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _module():
    path = ROOT / "agentic/scripts/build_reasoning_trace_coverage.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("trace_coverage", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class ReasoningTraceCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _module()
        cls.contracts = json.loads((ROOT / "agentic/registries/named_workflow_trace_contracts.yaml").read_text())

    def _trace(self, events):
        return {
            "identity": {"workflow_id": "theorem_proof_delivery", "run_id": "run.coverage", "profile_id": ""},
            "declared_route": [], "events": events, "observability_gaps": []
        }

    def test_control_only_run_is_not_semantically_complete(self) -> None:
        workflow = next(row for row in self.contracts["workflows"] if row["id"] == "theorem_proof_delivery")
        events = [{"event_id": f"control.{i}", "step_id": step["step_id"], "event_family": "authorization"} for i, step in enumerate(workflow["steps"])]
        report = self.mod.build_coverage(self._trace(events), self.contracts)
        self.assertEqual(report["summary"]["control_covered"]["percent"], 100.0)
        self.assertEqual(report["summary"]["semantic_covered"]["percent"], 0.0)

    def test_justified_conditional_na_is_not_penalized(self) -> None:
        event = {"event_id": "skip.1", "step_id": "split_gap_or_countermodel", "event_family": "skip", "warrant": "No lemma was blocked or false.", "workflow_disposition": "skipped"}
        trace = self._trace([event])
        trace["declared_route"] = [{"step_id": "split_gap_or_countermodel", "status": "justified_skip"}]
        report = self.mod.build_coverage(trace, self.contracts)
        row = next(row for row in report["requirements"] if row["step_id"] == "split_gap_or_countermodel")
        self.assertEqual(row["disposition"], "justified_na")
        self.assertTrue(row["semantic_covered"])

    def test_missing_fields_are_attributed_to_step(self) -> None:
        event = {"event_id": "infer.1", "step_id": "formalize_obligations", "event_family": "inference", "conclusion": "Obligations split."}
        report = self.mod.build_coverage(self._trace([event]), self.contracts)
        row = next(row for row in report["requirements"] if row["step_id"] == "formalize_obligations")
        self.assertIn("public_inference.warrant", row["missing_fields"])
        self.assertEqual(row["nearest_evidence_source"], ["ProofDeliveryPlan"])


if __name__ == "__main__":
    unittest.main()
