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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_pdf_projection_is_packet_driven_and_additive() -> None:
    source = (ROOT / "agentic/scripts/generate_public_reasoning_trace_latex.py").read_text(encoding="utf-8")
    assert "generate_public_reasoning_trace_html" not in source
    assert "html.parser" not in source
    assert "def render_tex(packet" in source
    assert "build_print_inventory(packet" in source


def test_all_html_expert_views_have_documented_pdf_dispositions() -> None:
    html_source = (ROOT / "agentic/scripts/generate_public_reasoning_trace_html.py").read_text(encoding="utf-8")
    contract = (ROOT / "docs/architecture/reasoning-trace-pdf-compatibility.md").read_text(encoding="utf-8")
    for label in (
        "Overview", "Workflow Route", "Inference Graph", "Timeline", "Claims & Evidence",
        "Alternatives & Failures", "Scope", "Decisions & Gates", "Obligations",
        "Artifacts & Receipts", "Authority", "Handoffs", "Trace Coverage",
    ):
        assert label in html_source
        assert f"| {label} |" in contract


def test_monitor_packet_schema_remains_the_single_semantic_contract() -> None:
    schema = json.loads((ROOT / "agentic/spec/public_reasoning_monitor_packet.schema.json").read_text())
    assert schema["title"] == "Workflow-neutral public reasoning monitor packet"
    doc = (ROOT / "docs/architecture/reasoning-trace-pdf-compatibility.md").read_text()
    assert "sole semantic source" in doc
    assert "Chronology does not imply support or entailment" in doc

