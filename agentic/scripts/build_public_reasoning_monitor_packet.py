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
"""Build the workflow-neutral expert monitor packet from an assembled trace."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agentic_common import ROOT, load_json_object, write_json  # noqa: E402


# Control-plane conclusions explain execution but are not scientific claims.
# This allow-list prevents exits and handoffs from inflating claim coverage.
SUBSTANTIVE_CLAIM_FAMILIES = {
    "inference", "claim", "transformation", "validation", "failure",
    "alternative", "falsifier", "obligation",
}


def _id(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, ensure_ascii=False, sort_keys=True, default=str)
    return f"{prefix}.{hashlib.sha256(raw.encode()).hexdigest()[:14]}"


def _rows(value: Any) -> list[dict[str, Any]]:
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def _lens(lenses: dict[str, Any], workflow_id: str, profile_id: str) -> dict[str, Any]:
    key = f"{workflow_id}:{profile_id}" if profile_id else workflow_id
    selected = dict(lenses.get("fallback", {}))
    selected.update(lenses.get("lenses", {}).get(key, {}))
    selected["lens_id"] = key if key in lenses.get("lenses", {}) else "fallback"
    return selected


def build_packet(trace: dict[str, Any], lenses: dict[str, Any]) -> dict[str, Any]:
    identity = dict(trace.get("identity", {}))
    selected_lens = _lens(lenses, str(identity.get("workflow_id", "")), str(identity.get("profile_id", "")))
    events = _rows(trace.get("events", []))
    event_ids = {str(e.get("event_id")) for e in events}
    evidence: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    obligations: list[dict[str, Any]] = []
    alternatives: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    scopes: list[dict[str, Any]] = []
    authorities: list[dict[str, Any]] = []
    handoffs: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for event in events:
        event_id = str(event.get("event_id"))
        nodes.append({"id": event_id, "type": "event", "label": event.get("conclusion") or event.get("question") or event.get("event_family"), "step_id": event.get("step_id", "")})
        for parent in event.get("parent_event_ids", []):
            if parent in event_ids:
                edges.append({"source": parent, "target": event_id, "type": "precedes"})
        event_evidence_ids = []
        for index, item in enumerate(_rows(event.get("evidence", []))):
            evidence_id = str(item.get("evidence_id") or _id("evidence", event_id, index, item))
            relation = str(item.get("relation") or "background")
            card = {**item, "evidence_id": evidence_id, "event_id": event_id, "relation": relation}
            evidence.append(card); event_evidence_ids.append(evidence_id)
            nodes.append({"id": evidence_id, "type": "evidence", "label": item.get("label") or item.get("path") or evidence_id, "relation": relation})
            edges.append({"source": evidence_id, "target": event_id, "type": relation if relation in {"supports", "refutes", "constrains"} else "background"})
        event_obligation_ids = []
        for index, item in enumerate(_rows(event.get("obligations", []))):
            obligation_id = str(item.get("obligation_id") or _id("obligation", event_id, index, item))
            obligations.append({**item, "obligation_id": obligation_id, "event_id": event_id})
            event_obligation_ids.append(obligation_id)
            nodes.append({"id": obligation_id, "type": "obligation", "label": item.get("requirement") or obligation_id})
            edges.append({"source": event_id, "target": obligation_id, "type": "produces"})
        conclusion = str(event.get("conclusion") or "")
        if conclusion and event.get("event_family") in SUBSTANTIVE_CLAIM_FAMILIES:
            incomplete = bool(event.get("trace_incomplete")) or not bool(event_evidence_ids or event_obligation_ids)
            claims.append({"claim_id": event_id, "event_id": event_id, "text": conclusion,
                           "epistemic_status": event.get("claim_epistemic_status", "unknown"),
                           "integrity_status": event.get("artifact_validation_status", "unknown"),
                           "workflow_disposition": event.get("workflow_disposition", "unknown"),
                           "evidence_ids": event_evidence_ids, "obligation_ids": event_obligation_ids,
                           "trace_incomplete": incomplete, "scope": event.get("scope", {})})
        for index, item in enumerate(event.get("alternatives", [])):
            card = item if isinstance(item, dict) else {"description": str(item)}
            alternatives.append({**card, "kind": "alternative", "event_id": event_id, "alternative_id": _id("alternative", event_id, index, card)})
        for index, item in enumerate(event.get("falsifiers", [])):
            card = item if isinstance(item, dict) else {"description": str(item)}
            alternatives.append({**card, "kind": "falsifier", "event_id": event_id, "alternative_id": _id("falsifier", event_id, index, card)})
        if event.get("event_family") == "failure":
            alternatives.append({"kind": "failure", "event_id": event_id, "description": conclusion or event.get("warrant") or "Recorded failure"})
        if event.get("scope"):
            scopes.append({"event_id": event_id, "step_id": event.get("step_id", ""), "scope": event["scope"]})
        if event.get("authority"):
            authorities.append({"event_id": event_id, "step_id": event.get("step_id", ""), **event["authority"]})
        if event.get("handoff"):
            handoffs.append({"event_id": event_id, **event["handoff"]})
        if event.get("event_family") in {"gate", "validation", "authorization", "control"}:
            decisions.append({"event_id": event_id, "step_id": event.get("step_id", ""), "family": event.get("event_family"),
                              "disposition": event.get("workflow_disposition", "unknown"), "reason": event.get("warrant") or conclusion})
        for index, item in enumerate(_rows(event.get("artifacts", []))):
            artifact_id = str(item.get("artifact_id") or item.get("receipt_id") or _id("artifact", event_id, index, item))
            artifacts.append({**item, "artifact_id": artifact_id, "event_id": event_id})
            nodes.append({"id": artifact_id, "type": "artifact", "label": item.get("path") or item.get("artifact_type") or artifact_id})
            edges.append({"source": event_id, "target": artifact_id, "type": "produces"})

    route = _rows(trace.get("declared_route", []))
    for step in route:
        step_node = f"step:{step.get('step_id')}"
        nodes.append({"id": step_node, "type": "step", "label": step.get("step_id"), "status": step.get("status")})
        for event_id in step.get("control_event_ids", []) + step.get("inference_event_ids", []):
            edges.append({"source": step_node, "target": event_id, "type": "contains"})
    topology = trace.get("profile_topology", {}) if isinstance(trace.get("profile_topology"), dict) else {}
    specialist_ids = set(topology.get("specialist_step_ids", []))
    for left, right in zip(route, route[1:]):
        if left.get("step_id") in specialist_ids or right.get("step_id") in specialist_ids:
            continue
        edges.append({"source": f"step:{left.get('step_id')}", "target": f"step:{right.get('step_id')}", "type": "precedes"})
    if specialist_ids:
        fork = topology.get("specialist_after")
        last_specialist_index = max(i for i, row in enumerate(route) if row.get("step_id") in specialist_ids)
        join = next((row.get("step_id") for row in route[last_specialist_index + 1:] if row.get("step_id") not in specialist_ids), "")
        for specialist_id in sorted(specialist_ids):
            edges.append({"source": f"step:{fork}", "target": f"step:{specialist_id}", "type": "branches"})
            if join:
                edges.append({"source": f"step:{specialist_id}", "target": f"step:{join}", "type": "joins"})
        tail = topology.get("validation_tail_start")
        if join and tail:
            edges.append({"source": f"step:{join}", "target": f"step:{tail}", "type": "refines",
                          "adapter": topology.get("validation_tail_adapter", {})})

    declared_count = len(route)
    control_count = sum(bool(r.get("control_event_ids")) or r.get("status") == "justified_skip" for r in route)
    semantic_count = sum(bool(r.get("semantic_complete_event_ids")) or (r.get("mode") == "conditional" and r.get("status") == "justified_skip") for r in route)
    resolved_evidence = sum(bool(c["evidence_ids"] or c["obligation_ids"]) for c in claims)
    coverage = {
        "declared_steps": declared_count, "control_covered_steps": control_count, "semantic_covered_steps": semantic_count,
        "control_coverage": round(control_count / declared_count, 4) if declared_count else 1.0,
        "semantic_coverage": round(semantic_count / declared_count, 4) if declared_count else 1.0,
        "evidence_resolution": round(resolved_evidence / len(claims), 4) if claims else 0.0,
        "trace_gaps": len(trace.get("observability_gaps", [])), "gaps": trace.get("observability_gaps", []),
        "diagnostics": trace.get("diagnostics", []),
    }
    inferences = [e for e in events if e.get("event_family") in {"inference", "claim", "transformation", "validation", "alternative", "falsifier", "obligation"}]
    return {
        "schema_version": "1.0", "identity": identity, "lens": selected_lens,
        "declared_route": route, "timeline": events, "inferences": inferences, "claims": claims,
        "evidence": evidence, "scope_ledger": scopes, "alternatives_and_failures": alternatives,
        "decisions_and_gates": decisions, "obligations": obligations, "artifacts_and_receipts": artifacts,
        "authority_ledger": authorities, "handoffs": handoffs, "coverage": coverage,
        "graph": {"nodes": nodes, "edges": edges}, "profile_topology": topology,
        "specialized_projections": trace.get("legacy_projections", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True, type=Path)
    parser.add_argument("--lenses", type=Path, default=ROOT / "agentic/registries/reasoning_trace_lenses.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "agentic/reports/public_reasoning_trace/latest.packet.json")
    args = parser.parse_args()
    packet = build_packet(load_json_object(args.trace), load_json_object(args.lenses))
    write_json(args.output, packet)
    print(json.dumps({"output": str(args.output), "claims": len(packet["claims"]), "nodes": len(packet["graph"]["nodes"])}, sort_keys=True))


if __name__ == "__main__":
    main()
