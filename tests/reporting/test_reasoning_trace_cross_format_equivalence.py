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

from generate_public_reasoning_trace_html import render
from validate_public_reasoning_trace_pdf import extract_html_packet, packet_semantic_ids


def test_html_embeds_exact_packet_and_semantic_ids_are_lane_separated(tmp_path: Path) -> None:
    packet_path = next((ROOT / "tests/fixtures/reasoning_trace/generated").glob("*.packet.json"))
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    html_path = tmp_path / "trace.html"
    html_path.write_text(render(packet), encoding="utf-8")
    assert extract_html_packet(html_path) == packet
    ids = packet_semantic_ids(packet)
    assert ids["route_steps"]
    assert ids["inferences"]
    assert ids["claims"]

