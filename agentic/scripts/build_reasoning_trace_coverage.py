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
"""Build auditable control and semantic coverage for one public trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, load_json_object, write_json


DEFAULT_CONTRACTS = ROOT / "agentic/registries/named_workflow_trace_contracts.yaml"
DEFAULT_JSON = ROOT / "agentic/reports/reasoning_trace_coverage/latest.json"
CONTROL_FAMILIES = {"activation", "authorization", "tool_control", "control", "skip", "failure", "exit", "handoff"}
SEMANTIC_FAMILIES = {"public_inference", "inference", "transformation", "validation", "obligation", "failure", "handoff"}


def _find_workflow(registry: dict[str, Any], workflow_id: str) -> dict[str, Any]:
    for workflow in registry.get("workflows", []):
        if workflow.get("id") == workflow_id:
            return workflow
    raise ValueError(f"unknown trace workflow {workflow_id!r}")


def _value(event: dict[str, Any], dotted: str) -> Any:
    if dotted.startswith("public_inference."):
        leaf = dotted.split(".", 1)[1]
        public = event.get("public_inference")
        return public.get(leaf) if isinstance(public, dict) else event.get(leaf)
    return event.get(dotted)


def _percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 1) if denominator else 100.0


def build_coverage(
    trace: dict[str, Any], contracts: dict[str, Any], *, visible_event_ids: set[str] | None = None
) -> dict[str, Any]:
    identity = trace.get("identity") if isinstance(trace.get("identity"), dict) else trace
    workflow_id = str(identity.get("workflow_id", ""))
    profile_id = str(identity.get("profile_id") or "")
    workflow = _find_workflow(contracts, workflow_id)
    requirements = list(workflow.get("steps", []))
    profile = next((row for row in workflow.get("profiles", []) if row.get("id") == profile_id), None)
    if profile_id and profile is None:
        raise ValueError(f"unknown trace profile {profile_id!r}")
    if profile:
        requirements = list(profile.get("steps", [])) + list(profile.get("specialists", []))
        tail_start = profile.get("validation_tail_start")
        base = list(workflow.get("steps", []))
        start = next((index for index, row in enumerate(base) if row.get("step_id") == tail_start), len(base))
        requirements.extend(base[start:])

    events = [row for row in trace.get("events", []) if isinstance(row, dict)]
    route_by_step = {
        row.get("step_id"): row for row in trace.get("declared_route", []) if isinstance(row, dict)
    }
    rows: list[dict[str, Any]] = []
    known_steps: set[str] = set()
    all_event_ids = {str(row.get("event_id", "")) for row in events}
    visible = all_event_ids if visible_event_ids is None else visible_event_ids

    for requirement in requirements:
        step_id = str(requirement.get("step_id") or requirement.get("skill") or "")
        known_steps.add(step_id)
        observed = [event for event in events if event.get("step_id") == step_id or (
            requirement.get("mode") == "specialist" and event.get("skill") == requirement.get("skill")
        )]
        control = [event for event in observed if event.get("event_family") in CONTROL_FAMILIES]
        semantic = [event for event in observed if event.get("event_family") in SEMANTIC_FAMILIES]
        route = route_by_step.get(step_id, {})
        skipped = route.get("status") in {"justified_skip", "unexplained_skip"} or any(
            event.get("event_family") == "skip" or event.get("workflow_disposition") in {"skipped", "not_applicable"}
            for event in observed
        )
        justified = skipped and (route.get("status") == "justified_skip" or any(event.get("warrant") or event.get("conclusion") for event in observed))
        disposition = "justified_na" if justified else "unjustified_skip" if skipped else "executed" if observed else "missing"
        required_fields = list(requirement.get("required_fields", []))
        present_fields = sorted({field for field in required_fields if any(_value(event, field) not in (None, "", [], {}) for event in semantic)})
        missing_fields = sorted(set(required_fields) - set(present_fields)) if not justified else []
        evidence_roles = {
            item.get("relation") for event in semantic for item in event.get("evidence", []) if isinstance(item, dict)
        }
        expected_roles = set(requirement.get("evidence_roles", []))
        semantic_complete = bool(semantic) and not missing_fields
        html_visible = bool(semantic) and all(str(event.get("event_id", "")) in visible for event in semantic)
        rows.append({
            "workflow_id": workflow_id,
            "profile_id": profile_id or None,
            "step_id": step_id,
            "skill": requirement.get("skill", ""),
            "mode": requirement.get("mode", "required"),
            "disposition": disposition,
            "control_event_ids": [event.get("event_id") for event in control],
            "semantic_event_ids": [event.get("event_id") for event in semantic],
            "control_covered": bool(control),
            "semantic_covered": semantic_complete or justified,
            "evidence_resolved": bool(semantic) and bool(evidence_roles),
            "negative_evidence_covered": bool(evidence_roles & {"refutes", "constrains"}),
            "authority_covered": bool(semantic) and all(bool(event.get("authority")) for event in semantic),
            "html_visible": html_visible or justified,
            "present_fields": present_fields,
            "missing_fields": missing_fields,
            "missing_evidence_roles": sorted(expected_roles - evidence_roles),
            "nearest_evidence_source": requirement.get("consumes", []),
        })

    required_rows = [row for row in rows if row["disposition"] != "justified_na"]
    metrics = {}
    for key in ("control_covered", "semantic_covered", "evidence_resolved", "negative_evidence_covered", "authority_covered", "html_visible"):
        count = sum(bool(row[key]) for row in required_rows)
        metrics[key] = {"covered": count, "total": len(required_rows), "percent": _percent(count, len(required_rows))}

    orphan_events = [
        event.get("event_id") for event in events
        if event.get("step_id") and event.get("step_id") not in known_steps and event.get("event_family") not in {"activation", "exit", "handoff"}
    ]
    unresolved_handoffs = [
        event.get("event_id") for event in events if event.get("event_family") == "handoff"
        and not (event.get("handoff") or {}).get("accepted", False)
    ]
    return {
        "schema_version": "1.0.0",
        "workflow_id": workflow_id,
        "profile_id": profile_id or None,
        "run_id": identity.get("run_id", ""),
        "summary": metrics,
        "requirements": rows,
        "orphan_event_ids": orphan_events,
        "unresolved_handoff_event_ids": unresolved_handoffs,
        "observability_gaps": trace.get("observability_gaps", []),
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [f"# Reasoning trace coverage: {report['workflow_id']}", ""]
    if report.get("profile_id"):
        lines.extend([f"Profile: `{report['profile_id']}`", ""])
    lines.extend(["| Dimension | Covered | Total | Percent |", "|---|---:|---:|---:|"])
    for name, value in report["summary"].items():
        lines.append(f"| {name.replace('_', ' ').title()} | {value['covered']} | {value['total']} | {value['percent']:.1f}% |")
    lines.extend(["", "## Requirements", "", "| Step | Disposition | Control | Semantic | Missing |", "|---|---|---:|---:|---|"])
    for row in report["requirements"]:
        missing = ", ".join(row["missing_fields"]) or "—"
        lines.append(f"| `{row['step_id']}` | {row['disposition']} | {'yes' if row['control_covered'] else 'no'} | {'yes' if row['semantic_covered'] else 'no'} | {missing} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    trace = load_json_object(args.trace if args.trace.is_absolute() else ROOT / args.trace)
    contracts = load_json_object(args.contracts if args.contracts.is_absolute() else ROOT / args.contracts)
    report = build_coverage(trace, contracts)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    markdown = args.markdown or output.with_suffix(".md")
    if not markdown.is_absolute():
        markdown = ROOT / markdown
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(to_markdown(report), encoding="utf-8")
    print(json.dumps({"output": str(output), "semantic_percent": report["summary"]["semantic_covered"]["percent"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
