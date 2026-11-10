# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Registry-aware assembly for named-workflow public traces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


CONTROL_FAMILIES = {
    "activation", "authorization", "control", "tool", "tool_control", "lifecycle",
    "skip", "failure", "gate", "handoff", "exit",
}
INFERENCE_FAMILIES = {
    "inference", "claim", "transformation", "validation", "alternative",
    "falsifier", "obligation", "failure", "handoff",
}


def _missing_required(event: dict[str, Any], requirement: dict[str, Any]) -> list[str]:
    fields = {
        "public_inference.question": event.get("question"),
        "public_inference.premises": event.get("premises"),
        "public_inference.warrant": event.get("warrant"),
        "public_inference.conclusion": event.get("conclusion"),
        "public_inference.scope": event.get("scope"),
        "evidence": event.get("evidence"),
        "authority": event.get("authority"),
        "alternatives": event.get("alternatives"),
        "falsifiers": event.get("falsifiers"),
        "handoff": event.get("handoff"),
        "obligations": event.get("obligations"),
    }
    return [name for name in requirement.get("required_fields", []) if not fields.get(name)]


def load_events(path: Path) -> list[dict[str, Any]]:
    """Load a JSON array/object or JSONL event source."""

    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        rows = payload.get("events", [])
        return [row for row in rows if isinstance(row, dict)]
    raise ValueError(f"{path} must contain events")


def _stable_id(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, ensure_ascii=False, sort_keys=True, default=str)
    return f"{prefix}.{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _normalize_event(row: dict[str, Any], index: int, run_id: str) -> dict[str, Any]:
    family = str(row.get("event_family") or row.get("family") or row.get("event_type") or "control").lower()
    if family.startswith("public_inference"):
        family = "inference"
    identity = row.get("identity") if isinstance(row.get("identity"), dict) else {}
    # The append-only v2 store and ReasoningLogger use ``public_inference``.
    # ``inference`` remains a read-only compatibility alias for pre-v2 sources.
    inference = row.get("public_inference") if isinstance(row.get("public_inference"), dict) else {}
    if not inference and isinstance(row.get("inference"), dict):
        inference = row["inference"]
    event_id = str(row.get("event_id") or identity.get("event_id") or _stable_id("event", run_id, index, row))
    sequence = row.get("sequence", identity.get("sequence", index + 1))
    try:
        sequence = int(sequence)
    except (TypeError, ValueError):
        sequence = index + 1
    parents = row.get(
        "causal_parent_event_ids",
        row.get("parent_event_ids", identity.get("causal_parent_event_ids", identity.get("parent_event_ids", []))),
    )
    evidence = row.get("evidence", inference.get("evidence", []))
    return {
        "event_id": event_id,
        "run_id": str(row.get("run_id") or identity.get("run_id") or run_id),
        "sequence": sequence,
        "timestamp": row.get("timestamp_utc") or row.get("timestamp") or identity.get("timestamp_utc") or identity.get("timestamp") or "",
        "event_family": family,
        "phase": row.get("phase") or identity.get("phase") or "",
        "step_id": row.get("step_id") or identity.get("step_id") or "",
        "skill": row.get("skill") or identity.get("skill") or "",
        "attempt": row.get("attempt", identity.get("attempt", 1)),
        "parent_event_ids": [str(x) for x in _list(parents)],
        "question": row.get("question") or inference.get("question") or "",
        "premises": _list(row.get("premises", inference.get("premises", []))),
        "operator": row.get("operator") or inference.get("operator") or inference.get("transformation") or "",
        "warrant": row.get("warrant") or inference.get("warrant") or "",
        "conclusion": row.get("conclusion") or inference.get("conclusion") or row.get("claim") or "",
        "assumptions": _list(row.get("assumptions", inference.get("assumptions", []))),
        "alternatives": _list(row.get("alternatives", inference.get("alternatives", []))),
        "falsifiers": _list(row.get("falsifiers", inference.get("falsifiers", []))),
        "evidence": _list(evidence),
        "scope": row.get("scope") or inference.get("scope") or {},
        "uncertainty": row.get("uncertainty", inference.get("uncertainty", "unknown")),
        "artifact_validation_status": row.get("artifact_validation_status", "unknown"),
        "claim_epistemic_status": row.get("claim_epistemic_status", row.get("epistemic_status", "unknown")),
        "workflow_disposition": row.get("workflow_disposition", row.get("decision", "unknown")),
        "authority": row.get("authority") if isinstance(row.get("authority"), dict) else {},
        "artifacts": _list(row.get("artifacts", row.get("artifact_refs", []))),
        "parent_artifact_ids": _list(row.get("parent_artifact_ids", identity.get("parent_artifact_ids", []))),
        "obligations": _list(row.get("obligations", [])),
        "handoff": row.get("handoff") if isinstance(row.get("handoff"), dict) else {},
        "trace_incomplete": bool(row.get("trace_incomplete", False)) or inference.get("trace_completeness") in {"partial", "trace_incomplete"},
    }


def _workflow(registry: dict[str, Any], workflow_id: str) -> dict[str, Any]:
    for workflow in registry.get("workflows", []):
        if workflow.get("id") == workflow_id:
            return workflow
    raise ValueError(f"unknown named workflow: {workflow_id}")


def assemble_named_workflow_trace(
    registry: dict[str, Any], raw_events: Iterable[dict[str, Any]], *, workflow_id: str,
    run_id: str, profile_id: str = "", target: str = "", trace_contracts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Overlay observed records on the declared route without filling gaps."""

    workflow = _workflow(registry, workflow_id)
    profile = next((p for p in workflow.get("profiles", []) if p.get("id") == profile_id), None)
    if profile_id and profile is None:
        raise ValueError(f"unknown profile {profile_id!r} for {workflow_id}")
    declared = list((profile or {}).get("steps", []))
    if profile:
        tail_start = profile.get("validation_tail_start")
        base = list(workflow.get("steps", []))
        start = next((i for i, step in enumerate(base) if step.get("id") == tail_start), len(base))
        declared.extend(base[start:])
    else:
        declared = list(workflow.get("steps", []))

    requirement_rows: list[dict[str, Any]] = []
    tc_profile: dict[str, Any] = {}
    if trace_contracts:
        tc_workflow = next((w for w in trace_contracts.get("workflows", []) if w.get("id") == workflow_id), {})
        requirement_rows.extend(tc_workflow.get("steps", []))
        if profile_id:
            tc_profile = next((p for p in tc_workflow.get("profiles", []) if p.get("id") == profile_id), {})
            requirement_rows.extend(tc_profile.get("steps", []))
            requirement_rows.extend(tc_profile.get("specialists", []))
            specialists = [
                {"id": row.get("step_id"), "order": 25, "skill": row.get("skill"), "mode": "specialist",
                 "when": row.get("when"), "consumes": row.get("consumes", []), "produces": row.get("produces", [])}
                for row in tc_profile.get("specialists", [])
            ]
            insert_after = (profile or {}).get("specialist_after")
            insert_at = next((i + 1 for i, step in enumerate(declared) if step.get("id") == insert_after), len(declared))
            declared[insert_at:insert_at] = specialists
    # A trace-contract projection normally supplies specialist role IDs and
    # semantics.  The execution registry is still sufficient to preserve the
    # Route-A fan-out/join topology when callers intentionally omit that
    # optional projection.
    if profile and not any(step.get("mode") == "specialist" for step in declared):
        specialists = [
            {
                "id": skill.replace("-", "_"),
                "order": 25,
                "skill": skill,
                "mode": "specialist",
                "when": None,
                "consumes": ["RouteAOpenPointPlan"],
                "produces": [profile.get("specialist_output", "ResultCandidatePacket")],
            }
            for skill in profile.get("specialist_skills", [])
        ]
        insert_after = profile.get("specialist_after")
        insert_at = next((i + 1 for i, step in enumerate(declared) if step.get("id") == insert_after), len(declared))
        declared[insert_at:insert_at] = specialists
    requirements = {str(row.get("step_id") or row.get("role_id") or row.get("skill")): row for row in requirement_rows}

    events = [_normalize_event(row, i, run_id) for i, row in enumerate(raw_events)]
    events = [e for e in events if not e.get("run_id") or e.get("run_id") == run_id]
    events.sort(key=lambda e: (e["sequence"], e["event_id"]))
    ids = {e["event_id"] for e in events}
    diagnostics: list[dict[str, Any]] = []
    if len(ids) != len(events):
        seen: set[str] = set()
        for event in events:
            if event["event_id"] in seen:
                diagnostics.append({"kind": "duplicate_event", "event_id": event["event_id"], "reference": event["event_id"]})
            seen.add(event["event_id"])
    by_id = {e["event_id"]: e for e in events}
    for event in events:
        for parent in event["parent_event_ids"]:
            if parent not in ids:
                diagnostics.append({"kind": "missing_parent", "event_id": event["event_id"], "reference": parent})
            elif by_id[parent]["sequence"] >= event["sequence"]:
                diagnostics.append({"kind": "out_of_order_parent", "event_id": event["event_id"], "reference": parent})
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(event_id: str) -> bool:
        if event_id in visiting:
            return True
        if event_id in visited:
            return False
        visiting.add(event_id)
        cyclic = any(parent in by_id and visit(parent) for parent in by_id[event_id]["parent_event_ids"])
        visiting.remove(event_id); visited.add(event_id)
        return cyclic
    for event_id in sorted(ids):
        if event_id not in visited and visit(event_id):
            diagnostics.append({"kind": "causal_cycle", "event_id": event_id, "reference": event_id})

    route = []
    declared_ids = {str(step.get("id")) for step in declared}
    for step in declared:
        step_id = str(step.get("id"))
        observed = [
            e for e in events
            if e["step_id"] == step_id
            or (step.get("mode") == "specialist" and e.get("skill") == step.get("skill"))
        ]
        control = [e for e in observed if e["event_family"] in CONTROL_FAMILIES]
        semantic = [e for e in observed if e["event_family"] in INFERENCE_FAMILIES and (e["conclusion"] or e["trace_incomplete"])]
        skipped = any(e["event_family"] == "skip" or e["workflow_disposition"] in {"skipped", "not_applicable"} for e in observed)
        requirement = requirements.get(step_id, {})
        complete_semantic = [event for event in semantic if not _missing_required(event, requirement)]
        status = "observed" if control or semantic else "missing"
        if skipped:
            status = "justified_skip" if any(e["warrant"] or e["conclusion"] for e in observed) else "unexplained_skip"
        semantic_required = requirement.get("disposition", "semantic_event_required") not in {"control_event_only", "not_applicable"}
        if complete_semantic or not semantic_required or (step.get("mode") == "conditional" and skipped):
            gap = ""
        elif semantic:
            missing = sorted({field for event in semantic for field in _missing_required(event, requirement)})
            gap = "Public inference summary is incomplete: " + ", ".join(missing)
        else:
            gap = "No public inference summary was observed."
        route.append({
            "step_id": step_id, "order": step.get("order"), "skill": step.get("skill", ""),
            "mode": step.get("mode", "required"), "condition": step.get("when"),
            "consumes": step.get("consumes", []), "produces": step.get("produces", []),
            "status": status, "control_event_ids": [e["event_id"] for e in control],
            "inference_event_ids": [e["event_id"] for e in semantic], "observability_gap": gap,
            "semantic_complete_event_ids": [e["event_id"] for e in complete_semantic],
            "trace_requirement": requirement,
        })
    for event in events:
        specialist_skills = {str(step.get("skill")) for step in declared if step.get("mode") == "specialist"}
        if event["step_id"] and event["step_id"] not in declared_ids and event.get("skill") not in specialist_skills:
            diagnostics.append({"kind": "extra_step", "event_id": event["event_id"], "reference": event["step_id"]})

    gaps = [{"step_id": r["step_id"], "kind": "missing_public_inference", "detail": r["observability_gap"]} for r in route if r["observability_gap"]]
    return {
        "schema_version": "2.0",
        "identity": {"trace_id": _stable_id("trace", run_id, workflow_id, profile_id), "run_id": run_id,
                     "workflow_id": workflow_id, "workflow_version": workflow.get("version", ""),
                     "workflow_name": workflow.get("visible_name", workflow_id), "profile_id": profile_id,
                     "profile_name": (profile or {}).get("visible_name", ""), "target": target},
        "declared_route": route, "events": events, "observability_gaps": gaps,
        "diagnostics": diagnostics,
        "handoff_contracts": workflow.get("handoffs", []),
        "prohibitions": workflow.get("prohibitions", []),
        "specialist_skills": (profile or {}).get("specialist_skills", []),
        "validation_tail_start": (profile or {}).get("validation_tail_start", ""),
        "profile_topology": ({
            "specialist_after": profile.get("specialist_after", ""),
            "specialist_output": profile.get("specialist_output", ""),
            "specialist_step_ids": [row.get("step_id") for row in tc_profile.get("specialists", [])],
            "validation_tail_start": profile.get("validation_tail_start", ""),
            "validation_tail_adapter": profile.get("validation_tail_adapter", {}),
        } if profile else {}),
    }
