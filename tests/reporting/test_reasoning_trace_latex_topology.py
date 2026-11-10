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


def test_every_route_step_and_graph_edge_has_a_textual_representation() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json").read_text())
    inventory = build_print_inventory(packet)
    tex = render_tex(packet, inventory, inventory["lens"])
    assert tex.count(r"\hypertarget{trace-step-") == len(packet["declared_route"])
    graph = next(row for row in inventory["sections"] if row["section_id"] == "graph")
    assert len([row for row in graph["items"] if row["graph_kind"] == "edge"]) == len(packet["graph"]["edges"])
    assert "precedes is chronology; supports/refutes/constrains are epistemic relations" in tex


def test_route_a_print_lens_exposes_fork_join_tail_and_scope_boundary() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/manuscript_result_elaboration-route_a.packet.json").read_text())
    inventory = build_print_inventory(packet)
    tex = render_tex(packet, inventory, inventory["lens"])
    assert inventory["lens"]["topology_mode"] == "fork_join"
    assert len(packet["declared_route"]) == 22
    normalized = tex.replace(r"\allowbreak{}", "")
    for phrase in ("same-theory identity versus analogy", "symbolic check versus proof", "finite versus continuum boundary", "specialist output versus integrated result", "fork/join result versus common validation tail"):
        assert phrase in normalized
    for role in packet["profile_topology"]["specialist_step_ids"]:
        assert role.replace("_", r"\_") in normalized
    edge_types = {row["type"] for row in packet["graph"]["edges"]}
    assert {"branches", "joins", "refines"} <= edge_types


def test_neutral_fallback_renders_without_workflow_branch() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json").read_text())
    packet["identity"]["workflow_id"] = "future_workflow"
    packet["identity"]["profile_id"] = ""
    tex = render_tex(packet)
    assert "Public Reasoning Trace" in tex
    assert "Topology mode" in tex and "neutral" in tex
