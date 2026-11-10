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
"""Semantic compatibility boundary for the established trace visualizers."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tests/fixtures/reasoning_trace/main_workflow_baseline/compatibility_contract.json"


class MainWorkflowTraceCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_legacy_surfaces_retain_expert_visible_contract(self) -> None:
        for name, surface in self.contract["surfaces"].items():
            source = ROOT / surface["source"]
            self.assertTrue(source.is_file(), f"{name}: missing {surface['source']}")
            text = source.read_text(encoding="utf-8")
            self.assertRegex(text, rf"def\s+{re.escape(surface['renderer'])}\s*\(")
            for dom_id in surface["dom_ids"]:
                self.assertIn(f'id="{dom_id}"', text, f"{name}: missing #{dom_id}")
            for label in surface["labels"]:
                self.assertIn(label, text, f"{name}: missing expert surface {label!r}")
            for tab in surface.get("tabs", []):
                self.assertIn(f'data-tab="{tab}"', text, f"{name}: missing tab {tab}")

    def test_specialized_monitor_packet_embedding_is_stable(self) -> None:
        monitor = self.contract["surfaces"]["yang_mills_monitor"]
        text = (ROOT / monitor["source"]).read_text(encoding="utf-8")
        self.assertIn(f'id="{monitor["embedded_packet_id"]}"', text)
        self.assertIn('type="application/json"', text)
        self.assertIn("PACKET = ROOT / \"agentic/reports/reasoning_monitor/latest.json\"", text)
        self.assertIn("OUT = ROOT / \"agentic/reports/reasoning_monitor/latest.html\"", text)

    def test_legacy_html_sources_are_offline(self) -> None:
        remote_asset = re.compile(r"<(?:script|link|img)\\b[^>]*(?:src|href)=['\"]https?://", re.I)
        for name, surface in self.contract["surfaces"].items():
            text = (ROOT / surface["source"]).read_text(encoding="utf-8")
            self.assertIsNone(remote_asset.search(text), f"{name}: remote rendering dependency")


if __name__ == "__main__":
    unittest.main()
