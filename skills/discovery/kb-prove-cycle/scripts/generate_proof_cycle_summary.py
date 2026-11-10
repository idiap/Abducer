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

"""Generate a summary of proved/disproved items from the proof cycle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from problem_mathlib import append_mathlib_result
from kb_context import kb_ref_from_artifacts_dir
from inference_diagnosis import refresh_attempt_inference_diagnosis
from inference_diagnosis import summarize_inference_diagnoses
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import save_mathlib_index
from problem_mathlib import write_mathlib_result_file
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


_TERMINAL_ATTEMPT_STATUSES = {"proved", "disproved", "blocked", "prior_art_found", "deferred"}
_TERMINAL_QUEUE_STATUSES = {"proved", "disproved", "blocked", "prior_art_found", "deferred"}
_ATTEMPT_TARGET_SYNC_FIELDS = (
    "title",
    "claim_text",
    "conjecture_statement",
    "source_statement_id",
    "target_statement_id",
    "source_excerpt",
    "target_excerpt",
    "route_synopsis",
    "candidate_object",
    "carrier_kind",
    "bridge_object_definition",
    "preserved_invariant",
    "missing_route_lemma",
    "first_nontrivial_lemma_title",
    "first_nontrivial_lemma_statement",
    "restricted_regime_mode",
    "regime_and_quantifiers",
    "admissibility_conditions",
    "independent_value_claim",
    "negative_barrier_version",
    "expert_gate",
    "branch_to_definition",
    "foundation_search",
    "interpretability_contract",
    "inference_diagnosis",
)


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_attempts(attempt_dir: Path) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    if not attempt_dir.exists():
        return attempts
    for path in sorted(attempt_dir.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        refresh_attempt_inference_diagnosis(payload)
        attempts.append(payload)
    return attempts


def _attempt_effective_status(attempt: dict[str, Any], *, queue_row: dict[str, Any] | None = None) -> str:
    queue_status = _clean_text(_ensure_dict(queue_row).get("status")).lower()
    top_status = _clean_text(attempt.get("status")).lower()
    final_status = _clean_text(_ensure_dict(attempt.get("final_assessment")).get("outcome")).lower()
    metadata_status = _clean_text(_ensure_dict(attempt.get("metadata")).get("status")).lower()
    current = next((item for item in (top_status, final_status, metadata_status) if item), "")
    if queue_status in _TERMINAL_ATTEMPT_STATUSES and current in {"", "pending", "in_progress"}:
        return queue_status
    return current or queue_status


def _queue_archive_reason(row: dict[str, Any]) -> str:
    status = _clean_text(row.get("status")).lower()
    deferred_by = _clean_text(row.get("deferred_by")).lower()
    diagnosis = _ensure_dict(row.get("inference_diagnosis"))
    context_status = _clean_text(diagnosis.get("context_status")).lower()
    if bool(row.get("retired_from_active_frontier")) or deferred_by == "inactive-discovery-frontier":
        return "inactive-discovery-frontier"
    if status in _TERMINAL_QUEUE_STATUSES and context_status == "ill-posed":
        return "legacy-ill-posed-terminal-packet"
    return ""


def _attempt_recency_key(attempt: dict[str, Any]) -> tuple[str, str]:
    metadata = _ensure_dict(attempt.get("metadata"))
    return (
        _clean_text(metadata.get("updated_utc")) or _clean_text(metadata.get("started_utc")),
        _clean_text(metadata.get("attempt_id")),
    )


def _latest_attempt_ids_by_scope(attempt_rows: list[dict[str, Any]]) -> dict[str, str]:
    latest: dict[str, tuple[tuple[str, str], str]] = {}
    for row in attempt_rows:
        if not isinstance(row, dict):
            continue
        metadata = _ensure_dict(row.get("metadata"))
        attempt_id = _clean_text(metadata.get("attempt_id"))
        if not attempt_id:
            continue
        queue_id = _clean_text(metadata.get("queue_id"))
        scope_id = queue_id or f"attempt:{attempt_id}"
        recency = _attempt_recency_key(row)
        incumbent = latest.get(scope_id)
        if incumbent is None or recency > incumbent[0]:
            latest[scope_id] = (recency, attempt_id)
    return {scope_id: payload[1] for scope_id, payload in latest.items()}


def _attempt_archive_reason(
    attempt: dict[str, Any],
    *,
    queue_rows: dict[str, dict[str, Any]],
    queue_archive_reasons: dict[str, str],
    latest_attempt_ids: dict[str, str],
) -> str:
    metadata = _ensure_dict(attempt.get("metadata"))
    queue_id = _clean_text(metadata.get("queue_id"))
    attempt_id = _clean_text(metadata.get("attempt_id"))
    if queue_id and queue_id in queue_archive_reasons:
        return f"queue:{queue_archive_reasons[queue_id]}"
    scope_id = queue_id or (f"attempt:{attempt_id}" if attempt_id else "")
    queue_row = _ensure_dict(queue_rows.get(queue_id))
    effective_status = _attempt_effective_status(attempt, queue_row=queue_row)
    if (
        scope_id
        and attempt_id
        and latest_attempt_ids.get(scope_id)
        and latest_attempt_ids[scope_id] != attempt_id
        and effective_status in _TERMINAL_ATTEMPT_STATUSES
    ):
        return "superseded-terminal-attempt"
    diagnosis = _ensure_dict(attempt.get("inference_diagnosis"))
    context_status = _clean_text(diagnosis.get("context_status")).lower()
    if not queue_id and effective_status in _TERMINAL_ATTEMPT_STATUSES and context_status == "ill-posed":
        return "legacy-ill-posed-terminal-packet"
    return ""


def _rewrite_attempt_artifacts(path: Path, attempt: dict[str, Any]) -> None:
    path.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path = path.with_suffix(".md")
    try:
        from start_proof_cycle import render_attempt_markdown
    except Exception:
        return
    md_path.write_text(render_attempt_markdown(attempt), encoding="utf-8")


def _load_attempts_synced(
    attempt_dir: Path,
    *,
    queue: dict[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    if not attempt_dir.exists():
        return attempts
    queue_rows = {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }
    for path in sorted(attempt_dir.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        changed = False
        metadata = _ensure_dict(payload.setdefault("metadata", {}))
        final_assessment = _ensure_dict(payload.setdefault("final_assessment", {}))
        queue_row = _ensure_dict(queue_rows.get(_clean_text(metadata.get("queue_id"))))
        target = _ensure_dict(payload.setdefault("target", {}))
        if queue_row:
            for field in _ATTEMPT_TARGET_SYNC_FIELDS:
                if field not in queue_row:
                    continue
                value = queue_row.get(field)
                if target.get(field) == value:
                    continue
                target[field] = value
                changed = True
            queue_status = _clean_text(queue_row.get("status")).lower()
            if queue_status:
                if _clean_text(payload.get("status")).lower() != queue_status:
                    payload["status"] = queue_status
                    changed = True
                if _clean_text(metadata.get("status")).lower() != queue_status:
                    metadata["status"] = queue_status
                    changed = True
                if queue_status in _TERMINAL_ATTEMPT_STATUSES and _clean_text(final_assessment.get("outcome")).lower() in {"", "pending", "in_progress"}:
                    final_assessment["outcome"] = queue_status
                    changed = True
                if (
                    queue_status in _TERMINAL_ATTEMPT_STATUSES
                    and not _clean_text(final_assessment.get("summary"))
                    and _clean_text(queue_row.get("resolution_summary"))
                ):
                    final_assessment["summary"] = _clean_text(queue_row.get("resolution_summary"))
                    changed = True
        refresh_attempt_inference_diagnosis(payload)
        attempts.append(payload)
        if changed:
            _rewrite_attempt_artifacts(path, payload)
    return attempts


def _slugify(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _clean_text(value).lower()).strip("-")


def _blocked_result_id(kb_ref: str, *, queue_id: str, attempt_id: str) -> str:
    token = _slugify(queue_id) or _slugify(attempt_id) or "blocked-result"
    return f"mathlib.{kb_ref}.blocked.{token}"


def _sync_blocked_attempts_into_mathlib(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    queue: dict[str, Any],
    mathlib: dict[str, Any],
) -> bool:
    """Backfill blocked proof attempts into InformalMathLib as negative local theorems."""

    attempts_dir = artifacts_dir / "proof-attempts"
    if not attempts_dir.exists():
        return False

    queue_rows = {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict)
    }
    existing_attempt_ids = {
        _clean_text(row.get("attempt_id"))
        for row in _ensure_list(mathlib.get("results"))
        if isinstance(row, dict)
    }
    existing_queue_ids = {
        _clean_text(row.get("queue_id"))
        for row in _ensure_list(mathlib.get("results"))
        if isinstance(row, dict)
    }
    mutated = False

    for attempt_path in sorted(attempts_dir.glob("*.json")):
        attempt = _load_json(attempt_path)
        if not attempt:
            continue
        metadata = _ensure_dict(attempt.get("metadata"))
        final_assessment = _ensure_dict(attempt.get("final_assessment"))
        proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
        target = _ensure_dict(attempt.get("target"))
        negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))
        queue_id = _clean_text(metadata.get("queue_id"))
        queue_row = _ensure_dict(queue_rows.get(queue_id))
        outcome = _attempt_effective_status(attempt, queue_row=queue_row)
        if outcome != "blocked":
            continue

        attempt_id = _clean_text(metadata.get("attempt_id"))
        if attempt_id in existing_attempt_ids or queue_id in existing_queue_ids:
            continue

        queue_status = _clean_text(queue_row.get("status")).lower()
        if queue_status and queue_status != "blocked":
            continue

        statement = (
            _clean_text(proof_attempt.get("result_statement"))
            or _clean_text(proof_attempt.get("theorem_statement"))
            or _clean_text(target.get("conjecture_statement"))
            or _clean_text(target.get("claim_text"))
            or _clean_text(queue_row.get("conjecture_statement"))
            or _clean_text(queue_row.get("claim_text"))
        )
        summary = (
            _clean_text(proof_attempt.get("result_summary"))
            or _clean_text(final_assessment.get("summary"))
            or _clean_text(negative_argument.get("effect_on_claim"))
            or _clean_text(queue_row.get("resolution_summary"))
            or _clean_text(queue_row.get("missing_route_lemma"))
        )
        if not statement and not summary:
            continue

        result = {
            "result_id": _blocked_result_id(kb_ref, queue_id=queue_id, attempt_id=attempt_id),
            "queue_id": queue_id,
            "attempt_id": attempt_id,
            "bridge_id": _clean_text(target.get("bridge_id")) or _clean_text(queue_row.get("bridge_id")),
            "source_statement_id": _clean_text(target.get("source_statement_id")) or _clean_text(queue_row.get("source_statement_id")),
            "target_statement_id": _clean_text(target.get("target_statement_id")) or _clean_text(queue_row.get("target_statement_id")),
            "outcome": "blocked",
            "title": _clean_text(target.get("title")) or _clean_text(queue_row.get("title")) or "Blocked route",
            "entry_kind": "negative-local-theorem",
            "statement": statement,
            "summary": summary,
            "tags": [
                _clean_text(target.get("candidate_object")) or _clean_text(queue_row.get("candidate_object")),
                _clean_text(target.get("preserved_invariant")) or _clean_text(queue_row.get("preserved_invariant")),
                _clean_text(target.get("proof_strategy_family")) or _clean_text(queue_row.get("proof_strategy_family")),
            ],
            "web_search_used": bool(_ensure_list(_ensure_dict(attempt.get("web_search_gate")).get("sources"))),
            "major_subresult_score": int(_ensure_dict(attempt.get("major_subresult_assessment")).get("score_total", 0) or 0),
            "major_subresult_candidate": bool(_ensure_dict(attempt.get("major_subresult_assessment")).get("qualifies")),
        }
        proof_markdown = attempt_path.with_suffix(".md").read_text(encoding="utf-8") if attempt_path.with_suffix(".md").exists() else ""
        artifact_path = write_mathlib_result_file(repo_root, kb_ref=kb_ref, result=result, proof_markdown=proof_markdown)
        result["artifact_path"] = str(artifact_path)
        append_mathlib_result(mathlib, result)
        existing_attempt_ids.add(attempt_id)
        existing_queue_ids.add(queue_id)
        mutated = True

    return mutated


def build_summary(
    *,
    kb_ref: str,
    queue: dict[str, Any],
    mathlib: dict[str, Any],
    attempts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Summarize proof-cycle state across InformalMathLib results and queue-level blocked routes."""
    results = [row for row in _ensure_list(mathlib.get("results")) if isinstance(row, dict)]
    proved = [row for row in results if _clean_text(row.get("outcome")) == "proved"]
    disproved = [row for row in results if _clean_text(row.get("outcome")) in {"disproved", "prior_art_found"}]
    produced_papers = [
        row
        for row in results
        if _clean_text(row.get("produced_paper_tex")) or _clean_text(row.get("produced_paper_pdf"))
    ]
    external_references = [
        row
        for row in results
        if _clean_text(row.get("entry_kind")) == "external-reference" or _clean_text(row.get("outcome")) == "external_reference"
    ]
    queue_entries = [row for row in _ensure_list(queue.get("entries")) if isinstance(row, dict)]
    queue_rows = {
        _clean_text(row.get("queue_id")): row
        for row in queue_entries
        if _clean_text(row.get("queue_id"))
    }
    queue_archive_reasons = {
        queue_id: reason
        for queue_id, reason in (
            (_clean_text(row.get("queue_id")), _queue_archive_reason(row))
            for row in queue_entries
        )
        if queue_id and reason
    }
    current_queue_entries = [
        row for row in queue_entries if _clean_text(row.get("queue_id")) not in queue_archive_reasons
    ]
    historical_queue_entries = [
        row for row in queue_entries if _clean_text(row.get("queue_id")) in queue_archive_reasons
    ]
    pending = [row for row in current_queue_entries if _clean_text(row.get("status")) == "pending"]
    in_progress = [row for row in current_queue_entries if _clean_text(row.get("status")) == "in_progress"]
    active_queue_entries = [
        row for row in current_queue_entries if _clean_text(row.get("status")) in {"pending", "in_progress"}
    ]
    blocked_mathlib = [row for row in results if _clean_text(row.get("outcome")) == "blocked"]
    blocked_queue = [
        {
            "result_id": _clean_text(row.get("result_id")) or _clean_text(row.get("queue_id")),
            "queue_id": _clean_text(row.get("queue_id")),
            "title": _clean_text(row.get("title")) or _clean_text(row.get("queue_id")) or "Blocked route",
            "statement": _clean_text(row.get("conjecture_statement") or row.get("claim_text")),
            "summary": _clean_text(row.get("resolution_summary")) or _clean_text(row.get("missing_route_lemma")),
            "artifact_path": "",
            "entry_kind": "blocked-queue-entry",
        }
        for row in queue_entries
        if _clean_text(row.get("status")) == "blocked"
    ]
    seen_blocked_ids: set[str] = set()
    blocked: list[dict[str, Any]] = []
    for row in [*blocked_mathlib, *blocked_queue]:
        row_id = _clean_text(row.get("queue_id")) or _clean_text(row.get("result_id"))
        if row_id in seen_blocked_ids:
            continue
        seen_blocked_ids.add(row_id)
        blocked.append(row)
    attempt_rows = [row for row in _ensure_list(attempts) if isinstance(row, dict)]
    latest_attempt_ids = _latest_attempt_ids_by_scope(attempt_rows)
    current_attempt_rows: list[dict[str, Any]] = []
    historical_attempt_rows: list[dict[str, Any]] = []
    for row in attempt_rows:
        archive_reason = _attempt_archive_reason(
            row,
            queue_rows=queue_rows,
            queue_archive_reasons=queue_archive_reasons,
            latest_attempt_ids=latest_attempt_ids,
        )
        if archive_reason:
            historical_attempt_rows.append(row)
            continue
        current_attempt_rows.append(row)
    active_attempt_rows = [
        row
        for row in current_attempt_rows
        if _attempt_effective_status(
            row,
            queue_row=_ensure_dict(queue_rows.get(_clean_text(_ensure_dict(row.get("metadata")).get("queue_id")))),
        )
        == "in_progress"
    ]
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "pending_count": len(pending),
            "in_progress_count": len(in_progress),
            "proved_count": len(proved),
            "disproved_count": len(disproved),
            "blocked_count": len(blocked),
            "produced_paper_count": len(produced_papers),
            "external_reference_count": len(external_references),
            "queue_current_count": len(current_queue_entries),
            "queue_historical_count": len(historical_queue_entries),
            "attempt_current_count": len(current_attempt_rows),
            "attempt_historical_count": len(historical_attempt_rows),
        },
        "diagnosis_overview": {
            "queue_active": summarize_inference_diagnoses(active_queue_entries),
            "queue": summarize_inference_diagnoses(current_queue_entries),
            "queue_historical": summarize_inference_diagnoses(historical_queue_entries),
            "attempts_active": summarize_inference_diagnoses(active_attempt_rows),
            "attempts": summarize_inference_diagnoses(current_attempt_rows),
            "attempts_historical": summarize_inference_diagnoses(historical_attempt_rows),
        },
        "proved": proved,
        "disproved": disproved,
        "blocked": blocked,
        "produced_papers": produced_papers,
        "external_references": external_references,
        "pending": pending[:8],
        "in_progress": in_progress[:8],
    }


def render_markdown(report: dict[str, Any]) -> str:
    metadata = _ensure_dict(report.get("metadata"))
    diagnosis_overview = _ensure_dict(report.get("diagnosis_overview"))
    lines = [
        "# Proof Cycle Summary",
        "",
        f"- KB ref: {metadata.get('kb_ref', '')}",
        f"- Pending queue items: {metadata.get('pending_count', 0)}",
        f"- In progress: {metadata.get('in_progress_count', 0)}",
        f"- Proved: {metadata.get('proved_count', 0)}",
        f"- Disproved or prior-art negative: {metadata.get('disproved_count', 0)}",
        f"- Blocked negative findings: {metadata.get('blocked_count', 0)}",
        f"- Produced papers: {metadata.get('produced_paper_count', 0)}",
        f"- External references in InformalMathLib: {metadata.get('external_reference_count', 0)}",
        f"- Current queue rows: {metadata.get('queue_current_count', 0)}",
        f"- Historical queue archive rows: {metadata.get('queue_historical_count', 0)}",
        f"- Current attempt dossiers: {metadata.get('attempt_current_count', 0)}",
        f"- Historical attempt archive dossiers: {metadata.get('attempt_historical_count', 0)}",
        "",
        "## Context Vs Inference Diagnosis",
        "",
    ]
    for label, scope_note, row in (
        ("Queue Active", "Active queue rows only.", _ensure_dict(diagnosis_overview.get("queue_active"))),
        ("Queue", "Current non-archival queue rows.", _ensure_dict(diagnosis_overview.get("queue"))),
        (
            "Queue Historical Archive",
            "Retired or legacy ill-posed terminal queue rows.",
            _ensure_dict(diagnosis_overview.get("queue_historical")),
        ),
        ("Attempts Active", "Active attempt dossiers only.", _ensure_dict(diagnosis_overview.get("attempts_active"))),
        ("Attempts", "Latest current attempt dossiers after collapsing superseded retries.", _ensure_dict(diagnosis_overview.get("attempts"))),
        (
            "Attempts Historical Archive",
            "Superseded retries or attempts inherited from archived queue rows.",
            _ensure_dict(diagnosis_overview.get("attempts_historical")),
        ),
    ):
        if not row:
            continue
        context_counts = _ensure_dict(row.get("context_counts"))
        inference_counts = _ensure_dict(row.get("inference_counts"))
        lines.extend(
            [
                f"### {label}",
                "",
                f"- Scope: {scope_note}",
                f"- Count: {row.get('count', 0)}",
                (
                    f"- Context counts: well-posed={context_counts.get('well-posed', 0)}, "
                    f"partially-ill-posed={context_counts.get('partially-ill-posed', 0)}, "
                    f"ill-posed={context_counts.get('ill-posed', 0)}"
                ),
                (
                    f"- Inference counts: determined={inference_counts.get('determined', 0)}, "
                    f"underdetermined={inference_counts.get('underdetermined', 0)}, "
                    f"difficult-but-well-posed={inference_counts.get('difficult-but-well-posed', 0)}"
                ),
            ]
        )
        defect_rows = [item for item in _ensure_list(row.get("common_blocking_defects")) if isinstance(item, dict)]
        if defect_rows:
            defects = [f"{_clean_text(item.get('text'))} ({int(item.get('count', 0) or 0)})" for item in defect_rows]
            lines.append(f"- Common blocking defects: {' | '.join(defects)}")
        samples = _ensure_dict(row.get("sample_subjects"))
        ill_posed = [item for item in _ensure_list(samples.get("ill_posed")) if _clean_text(item)]
        difficult = [item for item in _ensure_list(samples.get("difficult_but_well_posed")) if _clean_text(item)]
        if ill_posed:
            lines.append(f"- Ill-posed samples: {', '.join(ill_posed)}")
        if difficult:
            lines.append(f"- Difficult-but-well-posed samples: {', '.join(difficult)}")
        lines.append("")
    lines.extend(
        [
        "## Proved",
        "",
    ])
    proved = [row for row in _ensure_list(report.get("proved")) if isinstance(row, dict)]
    if not proved:
        lines.append("- No proved results recorded yet.")
        lines.append("")
    for row in proved:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Result'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Statement: {row.get('statement', '')}",
                f"- Summary: {row.get('summary', '')}",
                f"- File: {row.get('artifact_path', '')}",
                "",
            ]
        )

    lines.extend(["## Disproved Or Prior-Art Negative Results", ""])
    disproved = [row for row in _ensure_list(report.get("disproved")) if isinstance(row, dict)]
    if not disproved:
        lines.append("- No disproved or prior-art negative results recorded yet.")
        lines.append("")
    for row in disproved:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Result'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Statement: {row.get('statement', '')}",
                f"- Summary: {row.get('summary', '')}",
                f"- File: {row.get('artifact_path', '')}",
                "",
            ]
        )

    lines.extend(["## Blocked Results", ""])
    blocked = [row for row in _ensure_list(report.get("blocked")) if isinstance(row, dict)]
    if not blocked:
        lines.append("- No blocked routes recorded yet.")
        lines.append("")
    for row in blocked:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Blocked Route'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Queue ID: {row.get('queue_id', '')}",
                f"- Statement: {row.get('statement', '')}",
                f"- Summary: {row.get('summary', '')}",
                f"- File: {row.get('artifact_path', '')}",
                "",
            ]
        )

    lines.extend(["## External References", ""])
    references = [row for row in _ensure_list(report.get("external_references")) if isinstance(row, dict)]
    if not references:
        lines.append("- No imported external theorems, definitions, or axioms recorded yet.")
        lines.append("")
    for row in references:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Reference'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Reference type: {row.get('reference_type', '')}",
                f"- Used for: {row.get('used_for', '')}",
                f"- Source: {row.get('source_name', '')} {row.get('source_url', '')}".strip(),
                f"- File: {row.get('artifact_path', '')}",
                "",
            ]
        )

    lines.extend(["## Produced Papers", ""])
    produced_papers = [row for row in _ensure_list(report.get("produced_papers")) if isinstance(row, dict)]
    if not produced_papers:
        lines.append("- No high-value intermediate-result papers produced yet.")
        lines.append("")
    for row in produced_papers:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Produced Paper'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Outcome: {row.get('outcome', '')}",
                f"- Major subresult score: {row.get('major_subresult_score', '')}",
                f"- TeX: {row.get('produced_paper_tex', '')}",
                f"- PDF: {row.get('produced_paper_pdf', '')}",
                "",
            ]
        )

    lines.extend(["## Queue Head", ""])
    pending = [row for row in _ensure_list(report.get("pending")) if isinstance(row, dict)]
    in_progress = [row for row in _ensure_list(report.get("in_progress")) if isinstance(row, dict)]
    if not in_progress and not pending:
        lines.append("- The proof queue is empty.")
        lines.append("")
    for section, rows in (("In progress", in_progress), ("Pending", pending)):
        lines.append(f"### {section}")
        lines.append("")
        if not rows:
            lines.append(f"- No {section.lower()} items.")
            lines.append("")
            continue
        for row in rows:
            lines.append(
                f"- `{row.get('queue_id', '')}` | {row.get('status', '')} | {row.get('conjecture_statement') or row.get('claim_text', '')}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_summary(report: dict[str, Any], *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")


def refresh_summary_from_sources(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    queue: dict[str, Any] | None = None,
    mathlib: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Rebuild the proof-cycle summary from the current queue and InformalMathLib source of truth."""

    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    mathlib_json, mathlib_md = mathlib_paths(repo_root, kb_ref)
    queue_payload = queue if isinstance(queue, dict) else load_proof_queue(queue_json, kb_ref=kb_ref)
    mathlib_payload = mathlib if isinstance(mathlib, dict) else load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    if _sync_blocked_attempts_into_mathlib(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue_payload,
        mathlib=mathlib_payload,
    ):
        save_mathlib_index(mathlib_payload, json_path=mathlib_json, md_path=mathlib_md)
    report = build_summary(
        kb_ref=kb_ref,
        queue=queue_payload,
        mathlib=mathlib_payload,
        attempts=_load_attempts_synced(artifacts_dir / "proof-attempts", queue=queue_payload),
    )
    write_summary(
        report,
        output_json=artifacts_dir / "proof-cycle-summary.json",
        output_md=artifacts_dir / "proof-cycle-summary.md",
    )
    return report


def main() -> int:
    logger = ReasoningLogger("kb-prove-cycle-summary")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--mathlib-json", default="", help="Optional InformalMathLib index JSON path.")
    ap.add_argument("--output-json", default="", help="Optional proof-cycle-summary JSON path.")
    ap.add_argument("--output-md", default="", help="Optional proof-cycle-summary Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for proof cycle summary.")

    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    mathlib_json, _ = mathlib_paths(repo_root, kb_ref)
    if args.queue_json:
        queue_json = Path(args.queue_json)
    if args.mathlib_json:
        mathlib_json = Path(args.mathlib_json)
    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "proof-cycle-summary.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "proof-cycle-summary.md"

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    report = build_summary(
        kb_ref=kb_ref,
        queue=queue,
        mathlib=mathlib,
        attempts=_load_attempts_synced(artifacts_dir / "proof-attempts", queue=queue),
    )
    write_summary(report, output_json=output_json, output_md=output_md)

    logger.step(
        "Generated proof cycle summary",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"proved={report['metadata']['proved_count']}",
                f"disproved={report['metadata']['disproved_count']}",
                f"pending={report['metadata']['pending_count']}",
            ]
        ),
        surface_focus="proof-cycle-summary",
        surface_stage="prove-cycle",
        surface_metrics=report["metadata"],
        surface_taxonomy={"reasoning_types": ["prove-cycle", "summary"]},
    )
    logger.add_output("proof_cycle_summary_json", output_json)
    logger.add_output("proof_cycle_summary_md", output_md)
    log_path = logger.finalize(
        "success",
        summary=f"Generated proof cycle summary for `{kb_ref}`.",
    )
    print(f"[OK] Wrote proof cycle summary JSON: {output_json}")
    print(f"[OK] Wrote proof cycle summary Markdown: {output_md}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
