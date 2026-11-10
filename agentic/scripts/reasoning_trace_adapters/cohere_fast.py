# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Assemble public cohere-fast traces from observed Abducer lifecycle events.

The adapter preserves domain and parent/child lineage.  It never infers a
scientific conclusion from a successful control receipt or artifact digest.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


SUBSTANTIVE = {
    "public_inference", "inference", "transformation", "validation", "failure", "obligation",
}


def _trace_id(run_id: str, domain_id: str) -> str:
    return "trace." + hashlib.sha256(f"cohere_fast:{domain_id}:{run_id}".encode()).hexdigest()[:16]


def assemble_cohere_fast_trace(
    parent_contract: dict[str, Any],
    child_contracts: dict[str, Any],
    raw_events: Iterable[dict[str, Any]],
    *,
    run_id: str,
    domain_id: str,
    target: str,
    subworkflow_id: str = "",
    parent_run_id: str = "",
    execution_kind: str = "live",
) -> dict[str, Any]:
    workflow = parent_contract["workflow"]
    if workflow.get("id") != "cohere_fast":
        raise ValueError("cohere-fast parent contract required")
    if execution_kind not in {"live", "synthetic_fixture", "legacy_projection"}:
        raise ValueError("invalid execution kind")
    declared = list(child_contracts.get("subworkflows", []))
    if subworkflow_id:
        declared = [row for row in declared if row.get("id") == subworkflow_id]
        if not declared:
            raise ValueError(f"unknown cohere-fast subworkflow: {subworkflow_id}")

    events: list[dict[str, Any]] = []
    for index, source in enumerate(raw_events, 1):
        row = dict(source)
        if row.get("run_id", run_id) != run_id:
            continue
        if row.get("workflow_id", "cohere_fast") != "cohere_fast":
            raise ValueError("cross-workflow event in cohere-fast trace")
        if row.get("domain_id", domain_id) != domain_id:
            raise ValueError("cross-domain event in cohere-fast trace")
        evidence = row.get("evidence", []) if isinstance(row.get("evidence", []), list) else []
        for item in evidence:
            path = str(item.get("path", "")) if isinstance(item, dict) else ""
            if path.startswith("/") or (len(path) > 2 and path[1:3] in {":\\", ":/"}):
                raise ValueError("absolute evidence paths are forbidden in public traces")
        inference = row.get("public_inference", {}) if isinstance(row.get("public_inference"), dict) else {}
        family = str(row.get("event_family", "control"))
        # The canonical append-only v2 store emits ``public_inference``.  The
        # reporting packet uses the historical ``inference`` family, so
        # normalize only that canonical spelling and preserve every legacy
        # family already accepted by this adapter.
        if family == "public_inference":
            family = "inference"
        normalized = {
            "event_id": str(row.get("event_id", f"{run_id}.{index}")),
            "run_id": run_id,
            "sequence": int(row.get("sequence", index)),
            "timestamp": str(row.get("timestamp_utc", "")),
            "event_family": family,
            "phase": str(row.get("phase", row.get("subworkflow_id", ""))),
            "step_id": str(row.get("step_id", row.get("subworkflow_id", ""))),
            "skill": str(row.get("skill", "")),
            "attempt": int(row.get("attempt", 1)),
            "parent_event_ids": list(row.get("causal_parent_event_ids", row.get("parent_event_ids", []))),
            "question": str(inference.get("question", row.get("question", ""))),
            "premises": list(inference.get("premises", row.get("premises", []))),
            "operator": str(inference.get("operator", row.get("operator", ""))),
            "warrant": str(inference.get("warrant", row.get("warrant", ""))),
            "conclusion": str(inference.get("conclusion", row.get("conclusion", ""))),
            "assumptions": list(inference.get("assumptions", row.get("assumptions", []))),
            "alternatives": list(inference.get("alternatives", row.get("alternatives", []))),
            "falsifiers": list(inference.get("falsifiers", row.get("falsifiers", []))),
            "uncertainty": str(inference.get("uncertainty", row.get("uncertainty", "unknown"))),
            "scope": dict(inference.get("scope", row.get("scope", {}))),
            "evidence": evidence,
            "authority": dict(row.get("authority", {})),
            "obligations": list(row.get("obligations", [])),
            "artifacts": list(row.get("artifacts", [])),
            "handoff": dict(row.get("handoff", {})),
            "artifact_validation_status": str(row.get("artifact_validation_status", "not_checked")),
            "claim_epistemic_status": str(row.get("claim_epistemic_status", "not_applicable")),
            "workflow_disposition": str(row.get("workflow_disposition", "observed")),
            "trace_incomplete": inference.get("trace_completeness") in {"partial", "trace_incomplete"},
            "domain_id": domain_id,
            "subworkflow_id": str(row.get("subworkflow_id", "")),
            "parent_run_id": str(row.get("parent_run_id", parent_run_id)),
            "parent_event_id": str(row.get("parent_event_id", "")),
            "execution_kind": execution_kind,
            "claim_level": row.get("claim_level"),
        }
        if execution_kind != "live" and normalized["claim_epistemic_status"] in {"evidence_backed", "validated"}:
            normalized["claim_epistemic_status"] = "unknown"
            normalized["trace_incomplete"] = True
        events.append(normalized)
    events.sort(key=lambda row: (row["sequence"], row["event_id"]))

    route = []
    for child in declared:
        step_id = str(child["id"])
        observed = [event for event in events if event["step_id"] == step_id or event["subworkflow_id"] == step_id]
        semantic = [event for event in observed if event["event_family"] in SUBSTANTIVE and event["conclusion"]]
        control = [event for event in observed if event["event_family"] not in SUBSTANTIVE]
        skipped = any(event["event_family"] == "skip" or event["workflow_disposition"] == "skipped" for event in observed)
        route.append({
            "step_id": step_id, "order": child.get("order"), "skill": "cohere-fast-orchestrator",
            "mode": "conditional" if child.get("when") else "required", "condition": child.get("when"),
            "consumes": [child.get("input_type")], "produces": [child.get("return_type")],
            "status": "justified_skip" if skipped else ("observed" if observed else "missing"),
            "control_event_ids": [event["event_id"] for event in control],
            "inference_event_ids": [event["event_id"] for event in semantic],
            "semantic_complete_event_ids": [event["event_id"] for event in semantic if event["evidence"] or event["obligations"]],
            "observability_gap": "" if semantic or skipped else "No public inference summary was observed.",
        })
    gaps = [{"step_id": row["step_id"], "kind": "missing_public_inference", "detail": row["observability_gap"]} for row in route if row["observability_gap"]]
    return {
        "schema_version": "2.0",
        "identity": {
            "trace_id": _trace_id(run_id, domain_id), "run_id": run_id,
            "workflow_id": "cohere_fast", "workflow_version": workflow["version"],
            "workflow_name": "Cohere-fast", "profile_id": "", "profile_name": "",
            "target": target, "domain_id": domain_id, "subworkflow_id": subworkflow_id,
            "parent_run_id": parent_run_id, "execution_kind": execution_kind,
        },
        "declared_route": route, "events": events, "observability_gaps": gaps,
        "diagnostics": [], "profile_topology": {}, "legacy_projections": [],
    }
