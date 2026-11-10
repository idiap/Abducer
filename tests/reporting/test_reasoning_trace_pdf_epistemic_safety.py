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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from validate_public_reasoning_trace_pdf import _required_pdf_strings


def test_required_pdf_semantics_include_complete_expert_dossiers_and_topology() -> None:
    packets = [json.loads(path.read_text(encoding="utf-8")) for path in (ROOT / "tests/fixtures/reasoning_trace/generated").glob("*.packet.json")]
    assert len(packets) == 7
    for packet in packets:
        sentinels = _required_pdf_strings(packet)
        locations = {location for location, _ in sentinels}
        assert any(location.endswith(".conclusion") for location in locations)
        assert any(location.endswith(".warrant") for location in locations)
        assert any(".premises[" in location for location in locations)
        assert any(".scope." in location for location in locations)
        assert any(location.endswith(".artifact_validation_status") for location in locations)
        assert any(location.endswith(".claim_epistemic_status") for location in locations)
        assert any(location.endswith(".workflow_disposition") for location in locations)
        assert any(location.startswith("declared_route[") for location in locations)
        assert any(location.startswith("graph.edges[") for location in locations)
        assert any(location.startswith("evidence[") for location in locations)
        assert any(location.startswith("authority_ledger[") for location in locations)
        assert any(location.startswith("alternatives_and_failures[") for location in locations)
