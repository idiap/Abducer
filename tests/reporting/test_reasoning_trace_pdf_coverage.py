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

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from build_reasoning_trace_pdf_coverage import build_coverage


def test_pdf_coverage_is_independent_and_detects_projection_omission() -> None:
    packet = {
        "identity": {"workflow_id": "w"}, "coverage": {"semantic_coverage": 1.0},
        "declared_route": [{"step_id": "s1"}],
        "inferences": [{"event_id": "i1", "conclusion": "bounded result"}],
        "claims": [], "evidence": [], "obligations": [], "handoffs": [],
        "alternatives_and_failures": [], "authority_ledger": [], "graph": {"nodes": []}, "lens": {},
    }
    inventory = {"semantic_ids": {"route_steps": ["s1"], "inferences": ["i1"]}}
    report = build_coverage(packet, inventory, "w s1 i1 bounded result public rationale chain-of-thought")
    assert report["source_coverage"]["semantic_coverage"] == 1.0
    assert report["projection_coverage"]["complete"] is True
    omitted = build_coverage(packet, inventory, "w s1 public rationale chain-of-thought")
    assert omitted["source_coverage"]["semantic_coverage"] == 1.0
    assert omitted["projection_coverage"]["complete"] is False
    assert omitted["projection_coverage"]["pdf_id_visible"] == 1
