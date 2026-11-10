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
import html
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from generate_public_reasoning_trace_html import VIEWS, render  # noqa: E402


class PublicReasoningTraceHtmlTests(unittest.TestCase):
    def packet(self) -> dict:
        return {
            "schema_version": "1.0", "identity": {"trace_id": "trace-1", "run_id": "run-1", "workflow_id": "test"},
            "lens": {"visible_name": "Expert <Trace>", "accent": "#123456", "focus_question": "Why?", "spine_label": "Test spine"},
            "declared_route": [{"step_id": "s1", "skill": "skill", "mode": "required", "status": "observed", "observability_gap": ""}],
            "timeline": [], "inferences": [{"event_id": "e1", "sequence": 1, "event_family": "inference", "step_id": "s1", "question": "Q <script>alert(1)</script>", "premises": [], "operator": "deduce", "warrant": "W", "conclusion": "C", "uncertainty": "low", "scope": {}}],
            "claims": [{"claim_id": "e1", "text": "C", "epistemic_status": "conjectural", "integrity_status": "valid", "workflow_disposition": "continue", "evidence_ids": ["ev1"], "obligation_ids": [], "trace_incomplete": False, "scope": {}}],
            "evidence": [{"evidence_id": "ev1", "relation": "supports", "path": "artifacts/evidence.json"}],
            "scope_ledger": [], "alternatives_and_failures": [], "decisions_and_gates": [], "obligations": [],
            "artifacts_and_receipts": [], "authority_ledger": [], "handoffs": [],
            "coverage": {"declared_steps": 1, "control_coverage": 1.0, "semantic_coverage": 1.0, "evidence_resolution": 1.0, "trace_gaps": 0},
            "graph": {"nodes": [], "edges": []}, "profile_topology": {}, "specialized_projections": [],
        }

    def test_is_offline_self_contained_and_has_all_expert_views(self) -> None:
        page = render(self.packet()); lower = page.lower()
        for forbidden in ['<script src=', '<link ', 'http://', 'https://', '@import', '<img ']:
            self.assertNotIn(forbidden, lower)
        for key, label in VIEWS:
            self.assertIn(f'data-view="{key}"', page)
            self.assertIn(html.escape(label), page)
        self.assertIn('aria-label="Filter visible trace cards"', page)

    def test_embedded_packet_round_trips_without_script_injection(self) -> None:
        page = render(self.packet())
        match = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', page, re.S)
        self.assertIsNotNone(match)
        embedded = json.loads(match.group(1))
        self.assertEqual(embedded, self.packet())
        self.assertNotIn("<script>alert(1)</script>", match.group(1))

    def test_renderer_is_descriptor_driven(self) -> None:
        source = (ROOT / "agentic/scripts/generate_public_reasoning_trace_html.py").read_text(encoding="utf-8")
        for workflow_id in ["theorem_proof_delivery", "route_a", "deep_review_and_reorientation"]:
            self.assertNotIn(workflow_id, source)

    def test_tabs_are_keyboard_operable_and_associated_with_panels(self) -> None:
        page = render(self.packet())
        for key, _ in VIEWS:
            self.assertIn(f'id="tab-{key}"', page)
            self.assertIn(f'aria-controls="view-{key}"', page)
            self.assertIn(f'aria-labelledby="tab-{key}"', page)
        self.assertIn("event.key==='ArrowRight'", page)
        self.assertIn("event.key==='ArrowLeft'", page)
        self.assertIn("event.key==='Home'", page)
        self.assertIn("event.key==='End'", page)

    def test_large_trace_rendering_is_bounded_without_truncating_embedded_packet(self) -> None:
        packet = self.packet()
        packet["timeline"] = [
            {"event_id": f"event-{index}", "sequence": index, "event_family": "control"}
            for index in range(2501)
        ]
        page = render(packet)
        embedded = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', page, re.S)
        self.assertIsNotNone(embedded)
        self.assertEqual(len(json.loads(embedded.group(1))["timeline"]), 2501)
        self.assertIn("MAX_VISIBLE_CARDS=2000", page)
        self.assertIn("The complete validated packet remains embedded", page)


if __name__ == "__main__":
    unittest.main()
