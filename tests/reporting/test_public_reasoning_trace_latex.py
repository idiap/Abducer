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
from generate_public_reasoning_trace_latex import render_tex  # noqa: E402
from reasoning_trace_print_model import build_print_inventory  # noqa: E402


def _packet(name: str = "theorem_proof_delivery") -> dict:
    return json.loads((ROOT / f"tests/fixtures/reasoning_trace/generated/{name}.packet.json").read_text())


def test_render_is_byte_deterministic_and_contains_mandatory_sections() -> None:
    packet = _packet()
    inventory = build_print_inventory(packet)
    first = render_tex(packet, inventory, inventory["lens"])
    second = render_tex(packet, inventory, inventory["lens"])
    assert first.encode() == second.encode()
    for heading in (
        "Expert reading contract", "Validation dashboard", "Declared route and topology",
        "Expert inference dossiers", "Cross-cutting validation ledgers", "Complete chronological lifecycle ledger",
        "Causal and workflow graph ledger", "Projection completeness and omission ledger", "Build provenance",
    ):
        assert heading in first
    assert inventory["packet_digest"] in first.replace(r"\allowbreak{}", "")


def test_packet_values_never_enter_preamble_or_raw_tex_context() -> None:
    packet = _packet()
    packet["lens"]["visible_name"] = r"Evil \end{document} \input{/etc/passwd}"
    inventory = build_print_inventory(packet)
    tex = render_tex(packet, inventory, inventory["lens"])
    preamble, body = tex.split(r"\begin{document}", 1)
    assert "Evil" not in preamble
    assert r"\input{/etc/passwd}" not in body
    assert r"\textbackslash{}input" in body


def test_empty_lanes_are_visible_not_silently_dropped() -> None:
    packet = _packet()
    for lane in ("inferences", "alternatives_and_failures", "obligations", "handoffs", "graph"):
        packet[lane] = {"nodes": [], "edges": []} if lane == "graph" else []
    tex = render_tex(packet)
    assert "No substantive inferences were recorded" in tex
    assert "No alternative, falsifier, or failure was recorded" in tex
    assert "No graph edges recorded" in tex
