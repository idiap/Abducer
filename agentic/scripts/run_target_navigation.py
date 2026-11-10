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
"""Run one target-bound navigation slice and emit an evidence-sensitive release.

Navigation artifacts remain compatible with the historical control plane, but
release authority is new: every run has a unique append-only identity and a
machine-readable receipt. Missing literature, failed validators, or absent
feedback-effective operator evidence yields an honest hold—not a failed receipt
and never an unconditional promotion.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from agentic_common import ROOT, kb_ref_from_path, load_json_object, rel, repo_path, utc_now, write_json
from build_hypothesis_exploration_map import build_map
from build_target_dependency_graph import GraphBuilder, render_markdown
from validate_target_navigation_release import (
    ReleaseValidationError,
    canonical_theory_evidence_from_reachability,
    validate_release_receipt,
)
from validate_target_packets import validate_packet

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    file_digest,
    validate_identifier,
)
from agentic.discovery.literature import (  # noqa: E402
    resolve_present_literature_freshness,
)


DEFAULT_TARGET = ROOT / "agentic" / "examples" / "targets" / "p-vs-np-target.json"


def new_run_id(*, now: datetime | None = None, entropy: str | None = None) -> str:
    """Allocate a collision-resistant identifier independently of file counts."""

    timestamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%S%fZ")
    suffix = (entropy or uuid.uuid4().hex)[:12]
    return validate_identifier(f"navigation-{timestamp}-{suffix}", "run_id")


def run_cmd(args: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Execute one argv-only repository command and preserve its exact output."""

    result = subprocess.run(
        [sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(args)}")
    return result


def log_event(
    run_id: str,
    target_id: str,
    workflow_id: str,
    event: str,
    skill: str,
    summary: str,
    evidence: list[str] | None = None,
) -> None:
    args = [
        "agentic/scripts/log_skill_application.py", "--run-id", run_id,
        "--target-id", target_id, "--workflow-id", workflow_id,
        "--skill-id", skill, "--event", event, "--summary", summary,
    ]
    for item in evidence or []:
        args.extend(["--evidence", item])
    run_cmd(args)


def write_frontier(graph: dict[str, Any]) -> None:
    frontier = {
        "target_id": graph["target_id"], "graph_id": graph["graph_id"],
        "frontier_count": len(graph["frontier"]), "frontier": graph["frontier"][:80],
        "next_workflow_recommendation": "Continue with theory, proof-debt, or route-lemma nodes before claiming mathematical progress.",
    }
    write_json(ROOT / "agentic/state/dependency_frontier.json", frontier)
    lines = [
        "# Dependency Frontier", "", f"- Target: `{graph['target_id']}`",
        f"- Open frontier nodes: {len(graph['frontier'])}", "", "## Recommended Next Action", "",
        frontier["next_workflow_recommendation"], "", "## Top Frontier Nodes", "",
    ]
    lines.extend(
        f"- `{row['id']}` ({row['status']}): {row['next_action'] or row['blocker']}"
        for row in graph["frontier"][:25]
    )
    out = ROOT / "agentic/reports/dependency_frontier/latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def manifest_for_target(target_id: str) -> str:
    specific = ROOT / "registry" / "tasks" / f"{target_id}-navigation" / "task_registry.json"
    return rel(specific) if specific.exists() else "registry/tasks/target-navigation/task_registry.json"


def _validator_receipt(
    *, validator_id: str, target_id: str, run_id: str, state_version: int,
    command: Sequence[str], valid_override: bool | None = None,
) -> dict[str, Any]:
    started = utc_now()
    result = run_cmd(command, check=False)
    completed = utc_now()
    valid = result.returncode == 0 if valid_override is None else valid_override
    output = {
        "command": list(command), "exit_code": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
    }
    return {
        "receipt_id": f"validator.{validator_id}.{run_id}",
        "target_id": target_id, "run_id": run_id, "state_version": state_version,
        "status": "completed" if result.returncode == 0 else "failed", "valid": bool(valid),
        "completed_utc": completed, "output_digest": canonical_digest(output),
        "_started_utc": started,
    }


def _literature_binding(
    target_id: str, *, now: datetime | None = None
) -> dict[str, Any] | None:
    """Select a target-local packet only after injected-clock freshness replay."""

    root = ROOT / "agentic/state/literature" / target_id
    candidates: list[tuple[str, Path, dict[str, Any]]] = []
    if root.is_dir():
        for path in root.rglob("*.json"):
            try:
                payload = load_json_object(path)
            except (OSError, ValueError):
                continue
            selected = payload.get("selected_snapshot")
            resolution = payload.get("resolution")
            if payload.get("target_id") != target_id or not isinstance(
                selected, dict
            ) or not isinstance(resolution, dict):
                continue
            try:
                present = resolve_present_literature_freshness(payload, now=now)
            except (ContractError, KeyError, TypeError, ValueError):
                continue
            if (
                present["active_investment_gate"] == "pass"
                and present["freshness_status"] == "current"
            ):
                candidates.append((str(selected.get("search_completed_at", "")), path, payload))
    if not candidates:
        return None
    _, path, packet = max(candidates, key=lambda item: (item[0], item[1].as_posix()))
    selected = packet["selected_snapshot"]
    return {
        "literature_snapshot_id": selected["snapshot_id"],
        "literature_snapshot_digest": selected["content_digest"],
        "assimilation_receipt_id": packet["packet_id"],
        "path": rel(path),
    }


def _literature_validator(
    target_id: str, run_id: str, state_version: int, binding: dict[str, Any] | None
) -> dict[str, Any]:
    valid = binding is not None
    payload = {
        "target_id": target_id,
        "binding": binding,
        "rule": "newest validated target-local assimilation whose bounded freshness passes at resolution time",
    }
    return {
        "receipt_id": f"validator.target-literature.{run_id}",
        "target_id": target_id, "run_id": run_id, "state_version": state_version,
        "status": "completed", "valid": valid, "completed_utc": utc_now(),
        "output_digest": canonical_digest(payload),
    }


def _public_validator(receipt: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in receipt.items() if not key.startswith("_")}


def _write_immutable_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        if path.read_text(encoding="utf-8") != encoded:
            raise RuntimeError(f"immutable release collision: {path}")


def build_release_receipt(
    *, target_id: str, run_id: str, state_version: int,
    validator_receipts: Sequence[dict[str, Any]], trace_path: Path,
    literature_binding: dict[str, Any] | None,
    canonical_theory_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a valid promote-or-hold receipt from exact controlling evidence."""

    public = [_public_validator(item) for item in validator_receipts]
    gates = [
        {
            "gate_id": item["receipt_id"].split(f".{run_id}", 1)[0].removeprefix("validator."),
            "required": True,
            "status": "pass" if item["status"] == "completed" and item.get("valid") else "fail",
            "controlling_receipt_ids": [item["receipt_id"]],
        }
        for item in public
    ]
    promotable = (
        all(gate["status"] == "pass" for gate in gates)
        and canonical_theory_evidence is not None
    )
    binding = literature_binding or {
        "literature_snapshot_id": "missing-target-scoped-literature",
        "literature_snapshot_digest": "sha256:" + "0" * 64,
        "assimilation_receipt_id": "missing-target-scoped-assimilation",
    }
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0", "release_id": f"release.{run_id}",
        "target_id": target_id, "run_id": run_id, "state_version": state_version,
        "literature_snapshot_id": binding["literature_snapshot_id"],
        "literature_snapshot_digest": binding["literature_snapshot_digest"],
        "assimilation_receipt_id": binding["assimilation_receipt_id"],
        "created_utc": utc_now(), "gate_results": gates, "validator_receipts": public,
        "trace_digest": file_digest(trace_path) if trace_path.is_file() else canonical_digest([]),
        "operator_trace_path": rel(trace_path),
        "canonical_theory_evidence": canonical_theory_evidence,
        "authorization_scope": (
            "target_navigation_continuation"
            if promotable
            else "no_continuation_authorized"
        ),
        "authority_exclusions": [
            "experiment_theory_selection",
            "literature_novelty_promotion",
            "theorem_or_truth_promotion",
        ],
        "decision": "promote" if promotable else "hold",
        "decision_reasons": (
            [
                "Every required target/run/state-bound validator, current-literature gate, "
                "and exact canonical six-operator feedback chain passed.",
                "Promotion governs navigation continuation only; it is not theorem or truth promotion.",
            ]
            if promotable
            else [
                "Promotion is held until every required validator, current target-scoped literature gate, and exact canonical theory evidence pass.",
                *[f"Blocking gate: {gate['gate_id']}" for gate in gates if gate["status"] != "pass"],
                *([] if canonical_theory_evidence is not None else ["Blocking evidence: canonical theory authorization is absent."]),
            ]
        ),
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    validate_release_receipt(receipt)
    return receipt


def _render_release(receipt: dict[str, Any], graph: dict[str, Any], manifest: str) -> str:
    blockers = [gate["gate_id"] for gate in receipt["gate_results"] if gate["status"] != "pass"]
    lines = [
        f"# Target Navigation Release {receipt['run_id']}", "",
        f"- Target: `{receipt['target_id']}`", f"- State version: `{receipt['state_version']}`",
        f"- Decision: `{receipt['decision']}`", f"- Visible manifest: `{manifest}`",
        f"- Authorization scope: `{receipt['authorization_scope']}`",
        f"- Literature snapshot: `{receipt['literature_snapshot_id']}`",
        f"- Canonical theory commit: `{(receipt.get('canonical_theory_evidence') or {}).get('commit_id', 'absent')}`",
        f"- Dependency nodes: `{graph['summary']['node_count']}`",
        f"- Open frontier nodes: `{graph['summary']['frontier_count']}`", "",
        "This receipt governs the navigation/control-plane slice only; it does not promote a mathematical theorem.",
        f"Excluded authorities: `{', '.join(receipt['authority_exclusions'])}`.", "",
        "## Required Gates", "",
    ]
    lines.extend(f"- `{gate['gate_id']}`: `{gate['status']}`" for gate in receipt["gate_results"])
    lines.extend(["", "## Blocking Evidence", ""])
    lines.extend([f"- `{item}`" for item in blockers] or ["- None."])
    lines.extend(["", "## Rollback", "", "The run is append-only. Consumers can ignore this run ID and retain the prior target-bound release; no historical receipt is overwritten.", ""])
    return "\n".join(lines)


def resolve_target_path(raw: str | None) -> Path:
    if raw:
        return repo_path(raw, must_exist=True)
    current = ROOT / "agentic/state/current_target.json"
    return current if current.exists() else DEFAULT_TARGET


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", help="Target packet JSON path.")
    parser.add_argument("--run-id", help="Explicit unique run ID; generated when omitted.")
    parser.add_argument("--state-version", type=int)
    parser.add_argument("--canonical-cycle", type=Path)
    parser.add_argument("--canonical-state-root", type=Path)
    parser.add_argument("--canonical-receipt-root", type=Path)
    parser.add_argument("--canonical-workspace", type=Path)
    parser.add_argument("--canonical-run-id")
    args = parser.parse_args()
    if args.state_version is not None and args.state_version < 0:
        raise SystemExit("--state-version must be non-negative")
    run_id = validate_identifier(args.run_id, "run_id") if args.run_id else new_run_id()
    target_path = resolve_target_path(args.target)
    validate_packet(target_path)
    target = load_json_object(target_path)
    target_id = target["target_id"]
    canonical_paths = (
        args.canonical_cycle,
        args.canonical_state_root,
        args.canonical_receipt_root,
        args.canonical_workspace,
    )
    if any(canonical_paths) and not all(canonical_paths):
        raise SystemExit("all four canonical evidence paths must be supplied together")
    canonical_cycle: dict[str, Any] | None = None
    if all(canonical_paths):
        canonical_cycle = load_json_object(args.canonical_cycle)
        if canonical_cycle.get("target_id") != target_id:
            raise SystemExit("canonical cycle target does not match navigation target")
        if args.canonical_run_id and canonical_cycle.get("run_id") != args.canonical_run_id:
            raise SystemExit("--canonical-run-id does not match canonical cycle")
        committed_version = canonical_cycle.get("committed_state_version")
        if not isinstance(committed_version, int) or isinstance(committed_version, bool):
            raise SystemExit("canonical cycle has no valid committed state version")
        if args.state_version is not None and args.state_version != committed_version:
            raise SystemExit("--state-version does not match canonical committed state")
        state_version = committed_version
    else:
        state_version = args.state_version if args.state_version is not None else 0
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    workflow_id = f"{kb_ref}-target-navigation-run"
    write_json(ROOT / "agentic/state/current_target.json", target)

    log_event(run_id, target_id, workflow_id, "skill_application_start", "looper-target-goal-enricher", "Loaded validated target packet.", [rel(target_path)])
    log_event(run_id, target_id, workflow_id, "skill_application_context_loaded", "looper-target-dependency-cartographer", "Loaded target KB and artifact context.", target["evidence_paths"])

    builder = GraphBuilder(target)
    graph = builder.build()
    graph_json = ROOT / "agentic/state/dependency_graphs" / f"{kb_ref}.json"
    graph_md = ROOT / "agentic/reports/dependency_closure" / f"{kb_ref}.md"
    write_json(graph_json, graph)
    graph_md.parent.mkdir(parents=True, exist_ok=True)
    graph_md.write_text(render_markdown(graph), encoding="utf-8")
    hypothesis_map = build_map(target_path, graph_json)
    graph = load_json_object(graph_json)
    graph_md.write_text(render_markdown(graph), encoding="utf-8")
    write_frontier(graph)
    log_event(run_id, target_id, workflow_id, "skill_application_action_taken", "looper-target-dependency-cartographer", "Built recursive dependency graph.", [rel(graph_json)])
    log_event(run_id, target_id, workflow_id, "skill_application_action_taken", "abducer-mediation-candidate-generator", f"Built {hypothesis_map['summary']['candidate_count']} conceptual candidates.", ["artifacts/hegelian/hypothesis_exploration_map.json"])

    # Report construction is part of the run; release gates below are evaluated
    # separately so failure remains visible in a hold receipt.
    for command in (
        ["agentic/scripts/run_compliance_report.py"],
        ["agentic/scripts/run_drift_monitors.py"],
        ["agentic/scripts/run_frame_adequacy_report.py"],
        ["agentic/scripts/run_workflow_hub_report.py"],
    ):
        run_cmd(command, check=False)

    release_dir = ROOT / "agentic/reports/releases/targets" / target_id / "runs" / run_id
    reachability_json = release_dir / "canonical-reachability.json"
    reachability_md = release_dir / "canonical-reachability.md"
    if canonical_cycle is not None:
        operator_feedback_command = [
            "agentic/scripts/run_skill_reachability_audit.py",
            "--receipt-root", str(args.canonical_receipt_root),
            "--artifact-root", str(args.canonical_workspace),
            "--canonical-cycle", str(args.canonical_cycle),
            "--canonical-state-root", str(args.canonical_state_root),
            "--target-id", target_id,
            "--run-id", str(canonical_cycle["run_id"]),
            "--json-output", str(reachability_json),
            "--markdown-output", str(reachability_md),
            "--require-feedback-effective",
        ]
    else:
        operator_feedback_command = [
            "agentic/scripts/run_skill_reachability_audit.py",
            "--json-output", str(reachability_json),
            "--markdown-output", str(reachability_md),
            "--require-feedback-effective",
        ]
    validator_commands = [
        ("target-packet", ["agentic/scripts/validate_target_packets.py", rel(target_path)]),
        ("dependency-graph", ["agentic/scripts/validate_dependency_graph.py", rel(graph_json)]),
        ("skill-links", ["agentic/scripts/validate_skill_links.py"]),
        ("operator-feedback", operator_feedback_command),
        ("hook-contract", ["agentic/scripts/run_hook_contract_tests.py"]),
    ]
    validators = [
        _validator_receipt(
            validator_id=name, target_id=target_id, run_id=run_id,
            state_version=state_version, command=command,
        )
        for name, command in validator_commands
    ]
    canonical_theory_evidence: dict[str, Any] | None = None
    if canonical_cycle is not None and reachability_json.is_file():
        try:
            canonical_theory_evidence = canonical_theory_evidence_from_reachability(
                load_json_object(reachability_json)
            )
        except (OSError, ValueError, ReleaseValidationError):
            canonical_theory_evidence = None
    if canonical_theory_evidence is not None:
        literature_edge = next(
            (
                edge
                for edge in canonical_cycle.get("feedback_edges", [])
                if edge.get("producer_operator_id") == "frontier-literature-assimilator"
            ),
            None,
        )
        if literature_edge is None:
            canonical_theory_evidence = None
            literature = None
        else:
            literature = {
                "literature_snapshot_id": canonical_theory_evidence["literature_snapshot_id"],
                "literature_snapshot_digest": canonical_theory_evidence["literature_snapshot_digest"],
                "assimilation_receipt_id": literature_edge["producer_receipt_id"],
                "path": str(args.canonical_cycle),
            }
    else:
        literature = _literature_binding(target_id)
    validators.append(_literature_validator(target_id, run_id, state_version, literature))
    trace_path = ROOT / "agentic/traces/skill_applications" / f"{run_id}.jsonl"
    receipt = build_release_receipt(
        target_id=target_id, run_id=run_id, state_version=state_version,
        validator_receipts=validators, trace_path=trace_path,
        literature_binding=literature,
        canonical_theory_evidence=canonical_theory_evidence,
    )
    release_json = release_dir / "release.json"
    release_md = release_dir / "release.md"
    _write_immutable_json(release_json, receipt)
    release_md.parent.mkdir(parents=True, exist_ok=True)
    release_md.write_text(_render_release(receipt, graph, manifest_for_target(target_id)), encoding="utf-8")
    log_event(run_id, target_id, workflow_id, "skill_application_gate_evaluated", "looper-workflow-contract-governor", f"Release decision is {receipt['decision']} from exact gate receipts.", [rel(release_json)])
    log_event(run_id, target_id, workflow_id, "skill_application_complete", "looper-release-promoter", f"Recorded append-only {receipt['decision']} receipt; no theorem claim was made.", [rel(release_json)])
    run_cmd(["agentic/scripts/render_skill_application_log.py"], check=False)
    print(f"Wrote {rel(graph_json)}, {rel(graph_md)}, and {rel(release_json)} ({receipt['decision']})")
    return 0 if receipt["decision"] == "promote" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
