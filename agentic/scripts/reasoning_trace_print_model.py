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
"""Deterministic, non-epistemic print projection of a monitor packet.

The print inventory is an accounting layer.  It does not derive claims or
change statuses; it only assigns packet facts to the PDF body or its complete
audit appendices.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LENSES = ROOT / "agentic/registries/reasoning_trace_print_lenses.yaml"
PUBLIC_RATIONALE_BOUNDARY = (
    "Inspectable public rationale and evidence only. The inventory must not "
    "contain private chain-of-thought or derive scientific claims from layout, "
    "chronology, control authorization, or artifact integrity."
)


def canonical_json_bytes(value: Any) -> bytes:
    """Return stable UTF-8 JSON bytes for digests and committed inventories."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _clone(value: Any) -> Any:
    return copy.deepcopy(value)


def _rows(value: Any) -> list[dict[str, Any]]:
    return [_clone(row) for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}.{canonical_sha256(value)[:16]}"


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def load_print_lenses(path: Path = DEFAULT_LENSES) -> dict[str, Any]:
    # Registry files use JSON syntax so no YAML dependency is required.
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("print lens registry must be an object")
    return value


def select_print_lens(packet: dict[str, Any], registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """Select a descriptor without introducing workflow branches in rendering."""
    registry = registry or load_print_lenses()
    identity = packet.get("identity", {}) if isinstance(packet.get("identity"), dict) else {}
    workflow_id = str(identity.get("workflow_id", ""))
    profile_id = str(identity.get("profile_id", ""))
    key = f"{workflow_id}:{profile_id}" if profile_id else workflow_id
    selected = _clone(registry.get("fallback", {}))
    selected.update(_clone(registry.get("profiles", {}).get(key, {})))
    # Retain the packet lens wording where a registry does not override it.
    packet_lens = packet.get("lens", {}) if isinstance(packet.get("lens"), dict) else {}
    for field in ("visible_name", "focus_question", "spine_label"):
        if not selected.get(field) and packet_lens.get(field):
            selected[field] = packet_lens[field]
    selected["lens_id"] = key if key in registry.get("profiles", {}) else "fallback"
    selected["source_lens_id"] = packet_lens.get("lens_id", "fallback")
    return selected


LANES: tuple[tuple[str, str, str, str], ...] = (
    ("declared_route", "Declared route", "body", "step_id"),
    ("inferences", "Expert inference dossiers", "body", "event_id"),
    ("claims", "Claims", "appendix", "claim_id"),
    ("evidence", "Typed evidence", "appendix", "evidence_id"),
    ("alternatives_and_failures", "Alternatives, falsifiers, and failures", "body", "alternative_id"),
    ("scope_ledger", "Scope transitions", "body", "event_id"),
    ("decisions_and_gates", "Decisions and gates", "appendix", "event_id"),
    ("obligations", "Open and discharged obligations", "body", "obligation_id"),
    ("artifacts_and_receipts", "Artifacts and receipts", "appendix", "artifact_id"),
    ("authority_ledger", "Authority exercised and absent", "body", "event_id"),
    ("handoffs", "Handoffs", "body", "event_id"),
    ("timeline", "Complete chronology", "appendix", "event_id"),
    ("specialized_projections", "Specialized projections", "appendix", "projection_id"),
)


def _lane_items(packet: dict[str, Any], lane: str, id_field: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows = _rows(packet.get(lane, []))
    ids: list[str] = []
    for index, row in enumerate(rows):
        semantic_id = str(row.get(id_field) or _stable_id(lane.rstrip("s"), [index, row]))
        # Add the projection ID only to the inventory copy, never to the packet.
        row.setdefault("print_semantic_id", semantic_id)
        ids.append(semantic_id)
    return rows, _unique(ids)


def _graph_items(packet: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    graph = packet.get("graph", {}) if isinstance(packet.get("graph"), dict) else {}
    items: list[dict[str, Any]] = []
    ids: list[str] = []
    for kind in ("nodes", "edges"):
        for index, source in enumerate(_rows(graph.get(kind, []))):
            if kind == "nodes":
                semantic_id = str(source.get("id") or _stable_id("node", [index, source]))
            else:
                semantic_id = _stable_id("edge", [source.get("source"), source.get("type"), source.get("target"), index])
            item = {"graph_kind": kind[:-1], "print_semantic_id": semantic_id, **source}
            items.append(item)
            ids.append(semantic_id)
    return items, _unique(ids)


def build_print_inventory(
    packet: dict[str, Any],
    profile: dict[str, Any] | None = None,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Account deterministically for every packet lane and semantic ID.

    Meaningful source order is preserved. Only descriptor sets such as required
    contrasts are normalized, because no chronology or entailment is implied by
    their order.
    """
    if not isinstance(packet, dict):
        raise TypeError("packet must be an object")
    selected = _clone(profile) if profile is not None else select_print_lens(packet, registry)
    selected.setdefault("lens_id", "explicit" if profile is not None else "fallback")
    selected["required_contrasts"] = sorted(_unique(str(x) for x in selected.get("required_contrasts", [])))
    sections: list[dict[str, Any]] = []
    semantic_ids: dict[str, list[str]] = {}
    for lane, title, destination, id_field in LANES:
        items, ids = _lane_items(packet, lane, id_field)
        semantic_ids[lane] = ids
        disposition = "rendered" if destination == "body" else "summarized_with_complete_appendix"
        reason = ""
        if not items:
            disposition = "not_applicable"
            reason = "The validated packet records no items in this lane."
        sections.append({
            "section_id": lane,
            "title": title,
            "disposition": disposition,
            "reason": reason,
            "item_ids": ids,
            "item_count": len(items),
            "items": items,
        })
    graph_items, graph_ids = _graph_items(packet)
    semantic_ids["graph"] = graph_ids
    sections.append({
        "section_id": "graph", "title": "Causal and workflow graph", "disposition": "summarized_with_complete_appendix",
        "reason": "" if graph_items else "The validated packet records no graph nodes or edges.",
        "item_ids": graph_ids, "item_count": len(graph_items), "items": graph_items,
    })
    profile_topology = packet.get("profile_topology", {}) if isinstance(packet.get("profile_topology"), dict) else {}
    sections.append({
        "section_id": "profile_topology", "title": "Profile topology", "disposition": "rendered" if profile_topology else "not_applicable",
        "reason": "" if profile_topology else "No specialized profile topology applies.",
        "item_ids": ["profile-topology"] if profile_topology else [], "item_count": 1 if profile_topology else 0,
        "items": [{"print_semantic_id": "profile-topology", **_clone(profile_topology)}] if profile_topology else [],
    })
    semantic_ids["profile_topology"] = ["profile-topology"] if profile_topology else []

    field_destinations = {
        "schema_version": "build provenance", "identity": "cover identity", "lens": "cover and print profile",
        "declared_route": "workflow route body", "timeline": "complete chronology appendix",
        "inferences": "expert inference dossiers", "claims": "claim ledger appendix", "evidence": "evidence ledger appendix",
        "scope_ledger": "scope body and appendix", "alternatives_and_failures": "negative-path body",
        "decisions_and_gates": "decision and gate appendix", "obligations": "obligation body and appendix",
        "artifacts_and_receipts": "artifact appendix", "authority_ledger": "authority body and appendix",
        "handoffs": "handoff body", "coverage": "validation dashboard", "graph": "graph summary and complete edge appendix",
        "profile_topology": "route topology body", "specialized_projections": "specialized projection appendix",
    }
    field_dispositions = []
    for field in packet:
        destination = field_destinations.get(field)
        if destination:
            disposition = "rendered" if field not in {"timeline", "claims", "evidence", "decisions_and_gates", "artifacts_and_receipts", "graph", "specialized_projections"} else "summarized_with_complete_appendix"
            field_dispositions.append({"packet_field": field, "disposition": disposition, "destination": destination, "reason": ""})
        else:
            field_dispositions.append({"packet_field": field, "disposition": "omitted_with_reason", "destination": "omission ledger", "reason": "Unknown extension field; no scientific interpretation is permitted."})
    field_dispositions.sort(key=lambda row: row["packet_field"])
    return {
        "schema_version": "1.0",
        "packet_digest": canonical_sha256(packet),
        "identity": _clone(packet.get("identity", {})),
        "lens": selected,
        "sections": sections,
        "semantic_ids": semantic_ids,
        "field_dispositions": field_dispositions,
        "limits": {"body_inference_limit": None, "appendix_complete": True, "split_volume_records": []},
        "public_rationale_boundary": PUBLIC_RATIONALE_BOUNDARY,
    }


def section(inventory: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next((row for row in inventory.get("sections", []) if row.get("section_id") == section_id), {
        "section_id": section_id, "title": section_id.replace("_", " ").title(), "disposition": "not_applicable",
        "reason": "Lane not present in inventory.", "item_ids": [], "item_count": 0, "items": [],
    })
