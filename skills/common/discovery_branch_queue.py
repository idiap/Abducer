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

"""Persistent discovery-branch state for routed conceptual search layers."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from knowledge_source_policy import build_knowledge_source_policy
from knowledge_source_policy import render_knowledge_source_policy_markdown
from proof_discovery_language import render_pdl_program_markdown
from proof_discovery_language import serialize_discovery_branch_as_pdl

BRANCH_QUEUE_VERSION = 1
BRANCH_STATUSES = {
    "pending",
    "active",
    "in_progress",
    "completed",
    "blocked",
    "deprioritized",
}


def _utc_now() -> str:
    """Return a UTC timestamp for persisted branch-state metadata."""

    return dt.datetime.now(dt.UTC).isoformat()


def _clean_text(value: Any) -> str:
    """Normalize free-form branch metadata into a stable single-line representation."""

    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    """Coerce arbitrary values into dictionary-shaped payloads."""

    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    """Coerce arbitrary values into list-shaped payloads."""

    return value if isinstance(value, list) else []


def _render_routing_heuristic_markdown(heuristic: dict[str, Any]) -> list[str]:
    """Render the categorical/HoTT routing heuristic in a compact branch-facing form."""

    if not heuristic:
        return []
    lines = [
        f"- Routing heuristic: recommended={heuristic.get('recommended', False)} | score={heuristic.get('score', 0)}/{heuristic.get('threshold', 0)}",
        f"- Decision rule: {heuristic.get('decision_rule', '')}",
        f"- Rationale: {heuristic.get('rationale', '')}",
    ]
    active_criteria = [
        _clean_text(row.get("detail"))
        for row in _ensure_list(heuristic.get("criteria"))
        if isinstance(row, dict) and bool(row.get("active")) and _clean_text(row.get("detail"))
    ]
    if active_criteria:
        lines.append("- Active criteria:")
        for item in active_criteria:
            lines.append(f"  - {item}")
    active_anti_triggers = [
        _clean_text(row.get("detail"))
        for row in _ensure_list(heuristic.get("anti_triggers"))
        if isinstance(row, dict) and bool(row.get("active")) and _clean_text(row.get("detail"))
    ]
    if active_anti_triggers:
        lines.append("- Active anti-triggers:")
        for item in active_anti_triggers:
            lines.append(f"  - {item}")
    return lines


def discovery_branch_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical machine-readable and narrative branch-state artifact paths."""

    return artifacts_dir / "discovery-branch-queue.json", artifacts_dir / "discovery-branch-queue.md"


def discovery_branch_dossier_dir(artifacts_dir: Path) -> Path:
    """Return the directory that stores one dossier per spawned discovery branch."""

    return artifacts_dir / "discovery-branches"


def default_discovery_branch_state(*, kb_ref: str) -> dict[str, Any]:
    """Construct an empty discovery-branch state object for a given problem."""

    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": _clean_text(kb_ref),
            "branch_queue_version": BRANCH_QUEUE_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "branch_count": 0,
            "active_count": 0,
            "pending_count": 0,
            "completed_count": 0,
            "blocked_count": 0,
            "deprioritized_count": 0,
        },
        "branches": [],
    }


def load_discovery_branch_state(path: Path, *, kb_ref: str) -> dict[str, Any]:
    """Load persisted branch state while repairing missing or malformed structure."""

    if not path.exists():
        return default_discovery_branch_state(kb_ref=kb_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default_discovery_branch_state(kb_ref=kb_ref)
    if not isinstance(payload, dict):
        return default_discovery_branch_state(kb_ref=kb_ref)
    payload.setdefault("metadata", {})
    payload.setdefault("branches", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["branches"], list):
        payload["branches"] = []
    payload["metadata"]["kb_ref"] = _clean_text(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"]["branch_queue_version"] = BRANCH_QUEUE_VERSION
    return payload


def _refresh_branch_metadata(state: dict[str, Any]) -> None:
    """Recompute aggregate branch counts from the materialized branch rows."""

    meta = _ensure_dict(state.get("metadata"))
    branches = [row for row in _ensure_list(state.get("branches")) if isinstance(row, dict)]
    counts = {
        "active_count": 0,
        "pending_count": 0,
        "completed_count": 0,
        "blocked_count": 0,
        "deprioritized_count": 0,
    }
    for row in branches:
        status = _clean_text(row.get("status")).lower()
        if status == "active":
            counts["active_count"] += 1
        elif status in {"pending", "in_progress"}:
            counts["pending_count"] += 1
        elif status == "completed":
            counts["completed_count"] += 1
        elif status == "blocked":
            counts["blocked_count"] += 1
        elif status == "deprioritized":
            counts["deprioritized_count"] += 1
    meta["branch_queue_version"] = BRANCH_QUEUE_VERSION
    meta["updated_utc"] = _utc_now()
    meta["branch_count"] = len(branches)
    meta.update(counts)
    state["metadata"] = meta


def render_discovery_branch_markdown(state: dict[str, Any]) -> str:
    """Render the current discovery branches as an external-expert-readable search board."""

    meta = _ensure_dict(state.get("metadata"))
    branches = [row for row in _ensure_list(state.get("branches")) if isinstance(row, dict)]
    lines = [
        "# Discovery Branch Queue",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Branches: {meta.get('branch_count', 0)}",
        f"- Active: {meta.get('active_count', 0)}",
        f"- Pending: {meta.get('pending_count', 0)}",
        f"- Completed: {meta.get('completed_count', 0)}",
        f"- Blocked: {meta.get('blocked_count', 0)}",
        f"- Deprioritized: {meta.get('deprioritized_count', 0)}",
        "",
        "## Branches",
        "",
    ]
    if not branches:
        lines.append("- No discovery branches materialized.")
        lines.append("")
        return "\n".join(lines)
    for row in branches:
        lines.extend(
            [
                f"### {row.get('branch_id', '')}",
                "",
                f"- Status: {row.get('status', '')}",
                f"- Kind: {row.get('layer_kind', '')}",
                f"- Target: {row.get('target_label', '')}",
                f"- Routing priority: {float(row.get('routing_priority', 0.0) or 0.0):.3f}",
                f"- Governor decision: {row.get('governor_decision', '')}",
                f"- Governor value score: {float(row.get('governor_value_score', 0.0) or 0.0):.3f}",
                f"- Governor major candidate: {bool(row.get('governor_major_candidate'))}",
                f"- Dispatch rank: {row.get('dispatch_rank', 0)}",
                f"- Breakthrough families: {', '.join(_ensure_list(row.get('linked_breakthrough_families')))}",
                f"- Obstruction classes: {', '.join(_ensure_list(row.get('linked_obstruction_classes')))}",
                f"- Queue IDs: {', '.join(_ensure_list(row.get('linked_queue_ids')))}",
                f"- Attempt count: {int(row.get('attempt_count', 0) or 0)}",
                f"- Activation reason: {row.get('activation_reason', '')}",
                f"- Governor rationale: {row.get('governor_rationale', '')}",
                f"- Last outcome summary: {row.get('last_outcome_summary', '')}",
                f"- Dossier: {row.get('dossier_md', '')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def save_discovery_branch_state(state: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    """Persist the discovery-branch state in JSON and Markdown form."""

    for row in _ensure_list(state.get("branches")):
        if isinstance(row, dict):
            row["pdl_program"] = serialize_discovery_branch_as_pdl(row)
    _refresh_branch_metadata(state)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_discovery_branch_markdown(state), encoding="utf-8")


def select_discovery_branches(
    state: dict[str, Any],
    *,
    statuses: set[str] | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Return branch rows matching the requested lifecycle states in execution order."""

    wanted = {status.strip().lower() for status in (statuses or {"active"}) if str(status).strip()}
    rows = [
        row
        for row in _ensure_list(state.get("branches"))
        if isinstance(row, dict) and _clean_text(row.get("status")).lower() in wanted
    ]
    rows.sort(
        key=lambda row: (
            int(row.get("dispatch_rank", 0) or 0),
            -float(row.get("routing_priority", 0.0) or 0.0),
            _clean_text(row.get("branch_id")),
        )
    )
    if limit is not None:
        return rows[: max(0, int(limit))]
    return rows


def record_discovery_branch_execution(
    state: dict[str, Any],
    *,
    branch_id: str,
    execution_id: str,
    status: str,
    summary: str,
    artifact_json: str = "",
    artifact_md: str = "",
) -> dict[str, Any]:
    """Persist the latest execution metadata for one discovery branch."""

    normalized_branch_id = _clean_text(branch_id)
    normalized_status = _clean_text(status).lower() or "in_progress"
    if normalized_status not in BRANCH_STATUSES:
        raise ValueError(f"Unsupported discovery-branch status `{status}`.")
    for row in _ensure_list(state.get("branches")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("branch_id")) != normalized_branch_id:
            continue
        row["status"] = normalized_status
        row["attempt_count"] = int(row.get("attempt_count", 0) or 0) + 1
        row["last_execution_id"] = _clean_text(execution_id)
        row["last_execution_json"] = _clean_text(artifact_json)
        row["last_execution_md"] = _clean_text(artifact_md)
        row["last_outcome_summary"] = _clean_text(summary)
        row["updated_utc"] = _utc_now()
        _refresh_branch_metadata(state)
        return row
    raise ValueError(f"Discovery branch `{branch_id}` not found.")


def _branch_status_for_dispatch(*, dispatch_rank: int, activate_top_k: int) -> tuple[str, str]:
    """Choose the initial lifecycle state for a spawned branch from its dispatch rank."""

    if dispatch_rank <= max(1, activate_top_k):
        return "active", "Selected into the current discovery frontier by routed dispatch priority."
    return "pending", "Materialized as a deferred discovery branch awaiting activation."


def materialize_discovery_branches(
    *,
    routing: dict[str, Any],
    existing_state: dict[str, Any] | None = None,
    artifacts_dir: Path | None = None,
    activate_top_k: int = 4,
) -> dict[str, Any]:
    """Merge a routed discovery plan into persistent branch rows and per-branch dossiers."""

    kb_ref = _clean_text(_ensure_dict(routing.get("metadata")).get("kb_ref"))
    state = existing_state if isinstance(existing_state, dict) else default_discovery_branch_state(kb_ref=kb_ref)
    state.setdefault("metadata", {})
    state.setdefault("branches", [])

    existing_rows = {
        _clean_text(row.get("branch_id")): row
        for row in _ensure_list(state.get("branches"))
        if isinstance(row, dict) and _clean_text(row.get("branch_id"))
    }
    materialized_rows: list[dict[str, Any]] = []
    now = _utc_now()
    dossier_root = discovery_branch_dossier_dir(artifacts_dir) if artifacts_dir else None

    for layer in [row for row in _ensure_list(routing.get("discovery_layers")) if isinstance(row, dict)]:
        branch_id = _clean_text(layer.get("layer_id"))
        if not branch_id:
            continue
        current = existing_rows.get(branch_id)
        dispatch_rank = int(layer.get("dispatch_rank", 0) or 0)
        default_status, activation_reason = _branch_status_for_dispatch(
            dispatch_rank=dispatch_rank,
            activate_top_k=activate_top_k,
        )
        if current is None:
            row = {
                "branch_id": branch_id,
                "created_utc": now,
                "status": default_status,
                "activation_reason": activation_reason,
                "attempt_count": 0,
                "last_outcome_summary": "",
            }
        else:
            row = dict(current)
            terminal = _clean_text(row.get("status")).lower() in {"completed", "blocked", "deprioritized"}
            if not terminal:
                row["status"] = default_status
                row["activation_reason"] = activation_reason
        row.update(
            {
                "updated_utc": now,
                "kb_ref": kb_ref,
                "layer_kind": _clean_text(layer.get("layer_kind")),
                "target_id": _clean_text(layer.get("target_id")),
                "target_label": _clean_text(layer.get("target_label")),
                "routing_priority": float(layer.get("routing_priority", 0.0) or 0.0),
                "dispatch_rank": dispatch_rank,
                "dispatch_round": int(layer.get("dispatch_round", 0) or 0),
                "spawn_reason": _clean_text(layer.get("spawn_reason")),
                "rationale": _clean_text(layer.get("rationale")),
                "linked_queue_ids": [_clean_text(value) for value in _ensure_list(layer.get("linked_queue_ids")) if _clean_text(value)],
                "linked_breakthrough_families": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("linked_breakthrough_families"))
                    if _clean_text(value)
                ],
                "linked_obstruction_classes": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("linked_obstruction_classes"))
                    if _clean_text(value)
                ],
                "required_move": _clean_text(layer.get("required_move")),
                "abstraction_required": _clean_text(layer.get("abstraction_required")),
                "minimal_theorem_shape": _clean_text(layer.get("minimal_theorem_shape")),
                "system_prompt": _clean_text(layer.get("system_prompt")),
                "user_task": _clean_text(layer.get("user_task")),
                "required_questions": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("required_questions"))
                    if _clean_text(value)
                ],
                "expected_deliverables": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("expected_deliverables"))
                    if _clean_text(value)
                ],
                "stop_criteria": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("stop_criteria"))
                    if _clean_text(value)
                ],
                "search_modes": [_clean_text(value) for value in _ensure_list(layer.get("search_modes")) if _clean_text(value)],
                "anti_patterns": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("anti_patterns"))
                    if _clean_text(value)
                ],
                "routing_heuristic": _ensure_dict(layer.get("routing_heuristic")),
                "epistemic_lens": _clean_text(layer.get("epistemic_lens")),
                "lens_artifacts": _ensure_dict(layer.get("lens_artifacts")),
                "negative_outputs": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("negative_outputs"))
                    if _clean_text(value)
                ],
                "sample_theorem_targets": [
                    _clean_text(value)
                    for value in _ensure_list(layer.get("sample_theorem_targets"))
                    if _clean_text(value)
                ],
                "external_framework_search": _ensure_dict(layer.get("external_framework_search")),
            }
        )
        if dossier_root is not None:
            dossier_json = dossier_root / f"{branch_id}.json"
            dossier_md = dossier_root / f"{branch_id}.md"
            row["dossier_json"] = str(dossier_json)
            row["dossier_md"] = str(dossier_md)
        row["pdl_program"] = serialize_discovery_branch_as_pdl(row)
        materialized_rows.append(row)

    materialized_rows.sort(
        key=lambda row: (
            0 if _clean_text(row.get("status")).lower() == "active" else 1,
            int(row.get("dispatch_rank", 0) or 0),
            -float(row.get("routing_priority", 0.0) or 0.0),
            _clean_text(row.get("branch_id")),
        )
    )
    state["metadata"] = _ensure_dict(state.get("metadata"))
    state["metadata"]["kb_ref"] = kb_ref
    state["branches"] = materialized_rows
    _refresh_branch_metadata(state)
    return state


def build_discovery_branch_dossier(branch: dict[str, Any]) -> dict[str, Any]:
    """Build the inspectable dossier for one spawned discovery branch."""

    source_policy = build_knowledge_source_policy(
        stage="discovery",
        target_label=_clean_text(branch.get("target_label")),
        target_kind=_clean_text(branch.get("layer_kind")) or "discovery branch",
        mathlib_hit_count=0,
        external_framework_recommended=bool(_ensure_dict(branch.get("external_framework_search")).get("recommended")),
    )
    return {
        "metadata": {
            "branch_id": _clean_text(branch.get("branch_id")),
            "kb_ref": _clean_text(branch.get("kb_ref")),
            "generated_utc": _utc_now(),
            "status": _clean_text(branch.get("status")),
        },
        "branch": {
            "layer_kind": _clean_text(branch.get("layer_kind")),
            "target_id": _clean_text(branch.get("target_id")),
            "target_label": _clean_text(branch.get("target_label")),
            "routing_priority": float(branch.get("routing_priority", 0.0) or 0.0),
            "dispatch_rank": int(branch.get("dispatch_rank", 0) or 0),
            "dispatch_round": int(branch.get("dispatch_round", 0) or 0),
            "spawn_reason": _clean_text(branch.get("spawn_reason")),
            "rationale": _clean_text(branch.get("rationale")),
            "linked_queue_ids": list(_ensure_list(branch.get("linked_queue_ids"))),
            "linked_breakthrough_families": list(_ensure_list(branch.get("linked_breakthrough_families"))),
            "linked_obstruction_classes": list(_ensure_list(branch.get("linked_obstruction_classes"))),
        },
        "prompt_contract": {
            "required_move": _clean_text(branch.get("required_move")),
            "abstraction_required": _clean_text(branch.get("abstraction_required")),
            "minimal_theorem_shape": _clean_text(branch.get("minimal_theorem_shape")),
            "system_prompt": _clean_text(branch.get("system_prompt")),
            "user_task": _clean_text(branch.get("user_task")),
            "required_questions": list(_ensure_list(branch.get("required_questions"))),
        },
        "execution_contract": {
            "expected_deliverables": list(_ensure_list(branch.get("expected_deliverables"))),
            "stop_criteria": list(_ensure_list(branch.get("stop_criteria"))),
            "search_modes": list(_ensure_list(branch.get("search_modes"))),
            "anti_patterns": list(_ensure_list(branch.get("anti_patterns"))),
            "routing_heuristic": _ensure_dict(branch.get("routing_heuristic")),
            "epistemic_lens": _clean_text(branch.get("epistemic_lens")),
            "lens_artifacts": _ensure_dict(branch.get("lens_artifacts")),
            "negative_outputs": list(_ensure_list(branch.get("negative_outputs"))),
            "sample_theorem_targets": list(_ensure_list(branch.get("sample_theorem_targets"))),
        },
        "knowledge_source_policy": source_policy,
        "external_framework_search": _ensure_dict(branch.get("external_framework_search")),
        "pdl_program": serialize_discovery_branch_as_pdl(branch),
    }


def render_discovery_branch_dossier_markdown(dossier: dict[str, Any]) -> str:
    """Render one discovery branch dossier as a guided search brief for expert inspection."""

    meta = _ensure_dict(dossier.get("metadata"))
    branch = _ensure_dict(dossier.get("branch"))
    prompt_contract = _ensure_dict(dossier.get("prompt_contract"))
    execution = _ensure_dict(dossier.get("execution_contract"))
    source_policy = _ensure_dict(dossier.get("knowledge_source_policy"))
    gate = _ensure_dict(dossier.get("external_framework_search"))
    lines = [
        f"# Discovery Branch {meta.get('branch_id', '')}",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Status: {meta.get('status', '')}",
        f"- Kind: {branch.get('layer_kind', '')}",
        f"- Target: {branch.get('target_label', '')}",
        f"- Routing priority: {float(branch.get('routing_priority', 0.0) or 0.0):.3f}",
        f"- Dispatch rank: {branch.get('dispatch_rank', 0)}",
        "",
        "## Why This Branch Exists",
        "",
        f"{branch.get('spawn_reason', '')}",
        "",
        f"{branch.get('rationale', '')}",
        "",
        "## Discovery Contract",
        "",
        f"- Required move: {prompt_contract.get('required_move', '')}",
        f"- Abstraction required: {prompt_contract.get('abstraction_required', '')}",
        f"- Minimal theorem shape: {prompt_contract.get('minimal_theorem_shape', '')}",
        f"- Linked queue IDs: {', '.join(_ensure_list(branch.get('linked_queue_ids')))}",
        f"- Linked breakthrough families: {', '.join(_ensure_list(branch.get('linked_breakthrough_families')))}",
        "",
        "## System Prompt",
        "",
        prompt_contract.get("system_prompt", ""),
        "",
        "## User Task",
        "",
        prompt_contract.get("user_task", ""),
        "",
        "## Required Questions",
        "",
    ]
    for item in _ensure_list(prompt_contract.get("required_questions")):
        lines.append(f"- {item}")
    lines.extend(["", "## Expected Deliverables", ""])
    for item in _ensure_list(execution.get("expected_deliverables")):
        lines.append(f"- {item}")
    lines.extend(["", "## Stop Criteria", ""])
    for item in _ensure_list(execution.get("stop_criteria")):
        lines.append(f"- {item}")
    lines.extend(["", "## Search Modes", ""])
    for item in _ensure_list(execution.get("search_modes")):
        lines.append(f"- {item}")
    lines.extend(["", "## Anti-Patterns", ""])
    for item in _ensure_list(execution.get("anti_patterns")):
        lines.append(f"- {item}")
    lines.extend(["", "## Lens Artifacts", ""])
    heuristic = _ensure_dict(execution.get("routing_heuristic"))
    lines.extend(_render_routing_heuristic_markdown(heuristic))
    lines.append(f"- Epistemic lens: {execution.get('epistemic_lens', '')}")
    for label, field in (
        ("Diagram candidates", "diagram_candidates"),
        ("Commutativity obligations", "commutativity_obligations"),
        ("Universal property candidates", "universal_property_candidates"),
        ("Equivalence claims", "equivalence_claims"),
        ("Transport obligations", "transport_obligations"),
        ("Coherence failures", "coherence_failures"),
    ):
        values = [item for item in _ensure_list(_ensure_dict(execution.get("lens_artifacts")).get(field)) if _clean_text(item)]
        if not values:
            continue
        lines.append(f"- {label}:")
        for item in values:
            lines.append(f"  - {item}")
    negative_outputs = [item for item in _ensure_list(execution.get("negative_outputs")) if _clean_text(item)]
    if negative_outputs:
        lines.append("- Negative outputs:")
        for item in negative_outputs:
            lines.append(f"  - {item}")
    lines.extend(["", "## Sample Theorem Targets", ""])
    for item in _ensure_list(execution.get("sample_theorem_targets")):
        lines.append(f"- {item}")
    lines.extend(["", "## Knowledge Source Invocation Policy", ""])
    lines.extend(render_knowledge_source_policy_markdown(source_policy))
    lines.extend([""])
    lines.extend(render_pdl_program_markdown(_ensure_dict(dossier.get("pdl_program"))))
    lines.extend(["", "## External Framework Search Heuristic", ""])
    lines.append(f"- Recommended: {gate.get('recommended', False)}")
    lines.append(f"- Mode: {gate.get('mode', '')}")
    lines.append(f"- Justification: {gate.get('justification', '')}")
    lines.append(f"- Candidate framework regions: {', '.join(_ensure_list(gate.get('candidate_framework_regions')))}")
    lines.extend(["", "## Local Prerequisites Before Browsing", ""])
    for item in _ensure_list(gate.get("local_prerequisites")):
        lines.append(f"- {item}")
    lines.extend(["", "## Query Templates", ""])
    for item in _ensure_list(gate.get("query_templates")):
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def write_discovery_branch_dossiers(state: dict[str, Any], *, artifacts_dir: Path) -> list[dict[str, str]]:
    """Write one JSON/Markdown dossier per branch and return their path records."""

    dossier_root = discovery_branch_dossier_dir(artifacts_dir)
    dossier_root.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, str]] = []
    for branch in [row for row in _ensure_list(state.get("branches")) if isinstance(row, dict)]:
        branch_id = _clean_text(branch.get("branch_id"))
        if not branch_id:
            continue
        dossier = build_discovery_branch_dossier(branch)
        json_path = dossier_root / f"{branch_id}.json"
        md_path = dossier_root / f"{branch_id}.md"
        json_path.write_text(json.dumps(dossier, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_path.write_text(render_discovery_branch_dossier_markdown(dossier), encoding="utf-8")
        outputs.append({"branch_id": branch_id, "json": str(json_path), "md": str(md_path)})
    return outputs
