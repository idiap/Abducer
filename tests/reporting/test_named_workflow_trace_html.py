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
"""Semantic and offline HTML checks for all named-workflow trace lenses."""

from __future__ import annotations

import json
import html as html_module
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))
from build_public_reasoning_monitor_packet import build_packet  # noqa: E402
from generate_public_reasoning_trace_html import VIEWS, render  # noqa: E402
from reasoning_trace_adapters import assemble_named_workflow_trace  # noqa: E402
from tests.orchestration import test_named_workflow_realistic_trace_scenarios as scenarios  # noqa: E402


class NamedWorkflowTraceHtmlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.helper = scenarios.NamedWorkflowRealisticTraceScenarios()
        scenarios.NamedWorkflowRealisticTraceScenarios.setUpClass()
        cls.registry = cls.helper.registry
        cls.lenses = cls.helper.lenses
        cls.cases = cls.helper.cases

    def _report(self, case):
        run_id = f"fixture.{case['workflow_id']}.{case.get('profile_id', 'base')}"
        trace = assemble_named_workflow_trace(
            self.registry, self.helper._events(case), workflow_id=case["workflow_id"],
            run_id=run_id, profile_id=case.get("profile_id", ""), target=case["target"],
            trace_contracts=self.helper.trace_contracts,
        )
        packet = build_packet(trace, self.lenses)
        return packet, render(packet)

    def test_all_workflow_reports_embed_the_validated_semantic_packet(self) -> None:
        for case in self.cases:
            with self.subTest(workflow=case["workflow_id"], profile=case.get("profile_id")):
                packet, html = self._report(case)
                match = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', html, re.S)
                self.assertIsNotNone(match)
                self.assertEqual(json.loads(match.group(1)), packet)
                self.assertEqual(packet["identity"]["workflow_id"], case["workflow_id"])
                self.assertTrue(any(case["negative"] in row.get("text", "") for row in packet["claims"]))
                self.assertTrue(any(row.get("relation") == "refutes" for row in packet["evidence"]))
                self.assertTrue(any(case["falsifier"] == row.get("requirement") for row in packet["obligations"]))
                self.assertTrue(packet["scope_ledger"] and packet["authority_ledger"] and packet["handoffs"])

    def test_reports_are_offline_accessible_and_have_every_expert_view(self) -> None:
        _, html = self._report(self.cases[0])
        lower = html.lower()
        for marker in ("<script src=", "<link ", "http://", "https://", "@import", "<img "):
            self.assertNotIn(marker, lower)
        self.assertIn('aria-label="Filter visible trace cards"', html)
        self.assertIn('role="tablist"', html)
        self.assertIn('@media(max-width:700px)', html)
        for key, label in VIEWS:
            self.assertIn(f'data-view="{key}"', html)
            self.assertIn(html_module.escape(label), html)

    def test_untrusted_content_is_not_executable_markup(self) -> None:
        packet, _ = self._report(self.cases[0])
        packet["lens"]["visible_name"] = '</script><script id="injected">alert(1)</script>'
        html = render(packet)
        self.assertNotIn('<script id="injected">', html)
        embedded = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', html, re.S)
        self.assertIsNotNone(embedded)
        self.assertIn("\\u003c/script>", embedded.group(1))

    def test_route_a_identity_and_scope_are_explicit(self) -> None:
        case = next(row for row in self.cases if row.get("profile_id") == "route_a")
        packet, html = self._report(case)
        self.assertEqual(packet["identity"]["profile_id"], "route_a")
        payload = json.dumps(packet).lower()
        for marker in ("finite", "continuum", "same-theory", "endpoint"):
            self.assertIn(marker, payload)
        self.assertIn("route_a", html)


if __name__ == "__main__":
    unittest.main()
