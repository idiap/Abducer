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
from reasoning_trace_print_model import build_print_inventory, canonical_json_bytes, select_print_lens  # noqa: E402


PACKET = ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json"


def test_inventory_is_deterministic_complete_and_non_mutating() -> None:
    packet = json.loads(PACKET.read_text())
    original = json.loads(PACKET.read_text())
    first = build_print_inventory(packet)
    second = build_print_inventory(packet)
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert packet == original
    assert {row["packet_field"] for row in first["field_dispositions"]} == set(packet)
    assert all(row["disposition"] in {"rendered", "summarized_with_complete_appendix", "not_applicable", "omitted_with_reason"} for row in first["field_dispositions"])
    for section in first["sections"]:
        assert section["item_count"] == len(section["items"])
        assert len(section["item_ids"]) == len(set(section["item_ids"]))


def test_inventory_preserves_semantically_meaningful_order() -> None:
    packet = json.loads(PACKET.read_text())
    inventory = build_print_inventory(packet)
    assert inventory["semantic_ids"]["declared_route"] == [row["step_id"] for row in packet["declared_route"]]
    assert inventory["semantic_ids"]["inferences"] == [row["event_id"] for row in packet["inferences"]]


def test_all_print_lenses_and_neutral_fallback_select_declaratively() -> None:
    registry = json.loads((ROOT / "agentic/registries/reasoning_trace_print_lenses.yaml").read_text())
    for key in registry["profiles"]:
        workflow, _, profile = key.partition(":")
        packet = {"identity": {"workflow_id": workflow, "profile_id": profile}, "lens": {}}
        selected = select_print_lens(packet, registry)
        assert selected["lens_id"] == key
        assert selected["required_contrasts"]
    fallback = select_print_lens({"identity": {"workflow_id": "future_workflow"}, "lens": {}}, registry)
    assert fallback["lens_id"] == "fallback"
    assert fallback["topology_mode"] == "neutral"


def test_chronology_is_not_retyped_as_support() -> None:
    packet = json.loads(PACKET.read_text())
    inventory = build_print_inventory(packet)
    graph = next(row for row in inventory["sections"] if row["section_id"] == "graph")
    original_edges = packet["graph"]["edges"]
    projected_edges = [{k: v for k, v in row.items() if k not in {"graph_kind", "print_semantic_id"}} for row in graph["items"] if row["graph_kind"] == "edge"]
    assert projected_edges == original_edges

