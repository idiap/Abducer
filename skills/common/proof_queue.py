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

"""Persistent proof-queue utilities for discovery/prove cycles."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from kb_context import canonical_artifacts_dir
from mathematical_layers import build_mathematical_layers
from kb_context import normalize_kb_ref
from proof_discovery_language import render_pdl_program_markdown
from proof_discovery_language import serialize_queue_entry_as_pdl
from queue_entry_interpretability import assess_queue_entry_interpretability


QUEUE_VERSION = 4
QUEUE_STATUSES = {
    "pending",
    "in_progress",
    "proved",
    "disproved",
    "blocked",
    "deferred",
    "prior_art_found",
}


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text or "").strip().lower()).strip("-")


def proof_queue_paths(repo_root: Path, kb_ref: str) -> tuple[Path, Path]:
    artifacts_dir = canonical_artifacts_dir(repo_root, kb_ref)
    return artifacts_dir / "proof-queue.json", artifacts_dir / "proof-queue.md"


def default_queue(*, kb_ref: str) -> dict[str, Any]:
    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": normalize_kb_ref(kb_ref),
            "queue_version": QUEUE_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "pending_count": 0,
            "in_progress_count": 0,
            "completed_count": 0,
        },
        "entries": [],
    }


def load_proof_queue(path: Path, *, kb_ref: str) -> dict[str, Any]:
    if not path.exists():
        return default_queue(kb_ref=kb_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default_queue(kb_ref=kb_ref)
    if not isinstance(payload, dict):
        return default_queue(kb_ref=kb_ref)
    payload.setdefault("metadata", {})
    payload.setdefault("entries", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["entries"], list):
        payload["entries"] = []
    payload["metadata"]["kb_ref"] = normalize_kb_ref(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"]["queue_version"] = QUEUE_VERSION
    _backfill_queue_contracts(payload, allow_status_change=True)
    _backfill_queue_pdl(payload)
    _refresh_queue_metadata(payload)
    return payload


def save_proof_queue(queue: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    _backfill_queue_contracts(queue, allow_status_change=True)
    _backfill_queue_pdl(queue)
    _refresh_queue_metadata(queue)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_proof_queue_markdown(queue), encoding="utf-8")


def _refresh_queue_metadata(queue: dict[str, Any]) -> None:
    metadata = queue.setdefault("metadata", {})
    entries = queue.setdefault("entries", [])
    pending = 0
    in_progress = 0
    completed = 0
    for row in entries:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status", "pending")).strip().lower() or "pending"
        if status == "pending":
            pending += 1
        elif status == "in_progress":
            in_progress += 1
        elif status in {"proved", "disproved", "blocked", "deferred", "prior_art_found"}:
            completed += 1
    metadata["queue_version"] = QUEUE_VERSION
    metadata["updated_utc"] = _utc_now()
    metadata["pending_count"] = pending
    metadata["in_progress_count"] = in_progress
    metadata["completed_count"] = completed


def _backfill_queue_pdl(queue: dict[str, Any]) -> None:
    for row in queue.get("entries", []):
        if isinstance(row, dict):
            _backfill_mathematical_layers(row)
            row["pdl_program"] = serialize_queue_entry_as_pdl(row)


def _backfill_mathematical_layers(entry: dict[str, Any]) -> None:
    current = entry.get("mathematical_layers")
    if isinstance(current, dict) and current.get("latex") and current.get("lean_style"):
        return
    entry["mathematical_layers"] = build_mathematical_layers(
        title=entry.get("title"),
        exact_statement=entry.get("conjecture_statement") or entry.get("claim_text"),
        route_synopsis=entry.get("route_synopsis"),
        bridge_name=entry.get("candidate_object"),
        invariant=entry.get("preserved_invariant"),
        mode=entry.get("restricted_regime_mode")
        or entry.get("proof_strategy_family")
        or ("equivalence-theorem" if "equivalence" in str(entry.get("missing_route_lemma", "")).lower() else "special-case"),
        source_statement_id=entry.get("source_statement_id"),
        target_statement_id=entry.get("target_statement_id"),
        source_excerpt=entry.get("source_excerpt"),
        target_excerpt=entry.get("target_excerpt"),
        admissibility_conditions=entry.get("admissibility_conditions"),
        first_nontrivial_lemma_title=entry.get("first_nontrivial_lemma_title") or entry.get("missing_route_lemma"),
        first_nontrivial_lemma_statement=entry.get("first_nontrivial_lemma_statement") or entry.get("missing_route_lemma"),
        negative_barrier_version=entry.get("negative_barrier_version") or entry.get("negative_route"),
    )


def _apply_interpretability_contract(entry: dict[str, Any], *, allow_status_change: bool) -> None:
    contract = assess_queue_entry_interpretability(entry)
    entry["interpretability_contract"] = contract
    entry["inference_diagnosis"] = (
        contract.get("inference_diagnosis") if isinstance(contract.get("inference_diagnosis"), dict) else {}
    )
    if not allow_status_change:
        return
    if bool(entry.get("retired_from_active_frontier")):
        entry["status"] = "deferred"
        entry["deferred_by"] = "inactive-discovery-frontier"
        entry["deferred_reason"] = str(
            entry.get("retired_reason")
            or entry.get("resolution_summary")
            or "Retired from the active discovery frontier."
        ).strip()
        return
    status = str(entry.get("status", "pending")).strip().lower() or "pending"
    deferred_by = str(entry.get("deferred_by", "")).strip()
    if contract.get("ready"):
        if status == "deferred" and deferred_by == "llm-interpretability-gate":
            entry["status"] = "pending"
            entry["deferred_by"] = ""
            entry["deferred_reason"] = ""
        return
    if status in {"pending", "deferred"}:
        entry["status"] = "deferred"
        entry["deferred_by"] = "llm-interpretability-gate"
        entry["deferred_reason"] = str(contract.get("summary", "")).strip()


def _backfill_queue_contracts(queue: dict[str, Any], *, allow_status_change: bool) -> None:
    for row in queue.get("entries", []):
        if isinstance(row, dict):
            _apply_interpretability_contract(row, allow_status_change=allow_status_change)


def _entry_key(entry: dict[str, Any]) -> str:
    return str(entry.get("queue_key") or "").strip()


def _claim_identity(entry: dict[str, Any]) -> tuple[str, str]:
    package_identity = str(
        entry.get("theorem_package_id")
        or entry.get("package_id")
        or entry.get("discovery_programme_id")
        or entry.get("expert_conjecture_id")
        or ""
    ).strip()
    if package_identity:
        return (
            str(entry.get("claim_type", "")).strip(),
            package_identity,
        )
    return (
        str(entry.get("claim_type", "")).strip(),
        str(
            entry.get("conjecture_id")
            or entry.get("candidate_object")
            or entry.get("abstraction_label")
            or ""
        ).strip(),
    )


def _normalized_text(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _entry_claim_text(entry: dict[str, Any]) -> str:
    return _normalized_text(entry.get("conjecture_statement") or entry.get("claim_text"))


def _entry_strategy(entry: dict[str, Any]) -> str:
    return _slugify(str(entry.get("proof_strategy_family") or "").strip())


def _entry_object_text(entry: dict[str, Any]) -> str:
    return _normalized_text(entry.get("candidate_object"))


def _entry_route_text(entry: dict[str, Any]) -> str:
    return _normalized_text(entry.get("route_synopsis"))


def _selection_bucket(entry: dict[str, Any]) -> int:
    claim = _entry_claim_text(entry)
    strategy = _entry_strategy(entry)
    object_text = _entry_object_text(entry)
    route_text = _entry_route_text(entry)
    witness_like = "witness" in object_text or "witness" in route_text
    obstruction_like = any(token in f"{object_text} {route_text}" for token in ("obstruction", "barrier", "no-go"))
    negative = (
        claim.startswith("no admissible")
        or " no admissible " in f" {claim} "
        or strategy in {"barrier", "no-go", "no-go-theorem"}
    )
    transport_like = (
        strategy in {"transport", "equivalence-transport"}
        or "transport law" in claim
        or "equivalence witness" in claim
    )
    constructive = (
        strategy in {
            "constructive-realization",
            "constructive-instantiation",
            "threshold-localization",
            "invariant-realization",
            "transport",
            "equivalence-transport",
        }
        or claim.startswith("there exists an admissible")
        or claim.startswith("for every admissible")
    )
    if negative:
        return 0
    if transport_like and witness_like:
        return 4
    if constructive and witness_like and not obstruction_like:
        return 3
    if transport_like:
        return 2
    if constructive and not obstruction_like:
        return 2
    if constructive:
        return 1
    return 0


def _strategy_rank(entry: dict[str, Any]) -> int:
    strategy = _entry_strategy(entry)
    ranks = {
        "transport": 5,
        "equivalence-transport": 5,
        "constructive-realization": 4,
        "constructive-instantiation": 4,
        "threshold-localization": 3,
        "invariant-realization": 2,
        "barrier": 0,
        "no-go": 0,
        "no-go-theorem": 0,
    }
    if strategy in ranks:
        return ranks[strategy]
    claim = _entry_claim_text(entry)
    if "transport law" in claim or "equivalence witness" in claim:
        return 4
    if claim.startswith("there exists an admissible") or claim.startswith("for every admissible"):
        return 2
    if claim.startswith("no admissible"):
        return 0
    return 1


def _claim_rank(entry: dict[str, Any]) -> int:
    claim = _entry_claim_text(entry)
    if claim.startswith("for every admissible"):
        return 3
    if claim.startswith("there exists an admissible"):
        return 2
    if claim.startswith("no admissible"):
        return 0
    if "transport law" in claim or "equivalence witness" in claim:
        return 2
    return 1


def _object_rank(entry: dict[str, Any]) -> int:
    object_text = _entry_object_text(entry)
    route_text = _entry_route_text(entry)
    score = 0
    if "witness" in object_text or "witness" in route_text:
        score += 2
    if "obstruction" in object_text or "barrier" in object_text or "no-go" in object_text:
        score -= 1
    return score


def _governor_decision_rank(entry: dict[str, Any]) -> int:
    decision = str(entry.get("governor_decision", "")).strip().lower()
    ranks = {
        "major_subresult_candidate": 3,
        "queue_for_proof": 2,
        "deepen": 1,
    }
    return ranks.get(decision, 0)


def _governor_major_rank(entry: dict[str, Any]) -> int:
    score = entry.get("governor_major_subresult_score", 0)
    try:
        numeric = int(score or 0)
    except (TypeError, ValueError):
        numeric = 0
    if entry.get("governor_major_subresult_candidate"):
        return max(numeric, 1)
    return numeric


def _governor_value_rank(entry: dict[str, Any]) -> float:
    score = entry.get("governor_value_score", 0.0)
    try:
        return float(score or 0.0)
    except (TypeError, ValueError):
        return 0.0


def queue_entry_selection_sort_key(entry: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -_selection_bucket(entry),
        -_governor_decision_rank(entry),
        -_governor_major_rank(entry),
        -_governor_value_rank(entry),
        -float(entry.get("priority", 0.0) or 0.0),
        -_strategy_rank(entry),
        -_claim_rank(entry),
        -_object_rank(entry),
        str(entry.get("queue_id") or entry.get("queue_key") or ""),
    )


def _next_queue_id_from_entries(entries: list[dict[str, Any]], *, kb_ref: str) -> str:
    prefix = f"proofq.{normalize_kb_ref(kb_ref)}."
    current_max = 0
    for row in entries:
        queue_id = str(row.get("queue_id", "")).strip()
        if not queue_id.startswith(prefix):
            continue
        suffix = queue_id[len(prefix) :]
        if suffix.isdigit():
            current_max = max(current_max, int(suffix))
    return f"{prefix}{current_max + 1:03d}"


def make_queue_key(*, bridge_id: str, claim_text: str, target_statement_id: str, claim_slug: str = "") -> str:
    return "|".join(
        [
            str(bridge_id or "").strip(),
            str(target_statement_id or "").strip(),
            _slugify(str(claim_slug or claim_text or ""))[:120],
        ]
    )


def _route_identity(entry: dict[str, Any]) -> tuple[str, str]:
    return (
        str(entry.get("bridge_id", "")).strip(),
        "|".join(
            [
                str(entry.get("target_statement_id", "")).strip(),
                *_claim_identity(entry),
            ]
        ).strip("|"),
    )


def enqueue_entries(queue: dict[str, Any], entries: list[dict[str, Any]]) -> tuple[int, int]:
    """Merge refreshed discovery entries into the persistent queue without resetting lifecycle state."""
    existing = {
        _entry_key(row): row
        for row in queue.get("entries", [])
        if isinstance(row, dict) and _entry_key(row)
    }
    existing_by_route = {
        _route_identity(row): row
        for row in queue.get("entries", [])
        if isinstance(row, dict) and any(_route_identity(row))
    }
    added = 0
    updated = 0
    queue_entries = [row for row in queue.get("entries", []) if isinstance(row, dict)]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = _entry_key(entry)
        if not key:
            continue
        reopen_on_refresh = bool(entry.get("reopen_on_refresh"))
        current = existing.get(key)
        if current is None:
            current = existing_by_route.get(_route_identity(entry))
        now = _utc_now()
        if current is None:
            materialized = dict(entry)
            materialized.pop("reopen_on_refresh", None)
            materialized.setdefault(
                "queue_id",
                _next_queue_id_from_entries(queue_entries, kb_ref=queue.get("metadata", {}).get("kb_ref", "")),
            )
            materialized.setdefault("status", "pending")
            materialized.setdefault("created_utc", now)
            materialized["updated_utc"] = now
            materialized.setdefault("attempt_ids", [])
            materialized["retired_from_active_frontier"] = bool(materialized.get("retired_from_active_frontier"))
            _backfill_mathematical_layers(materialized)
            _apply_interpretability_contract(materialized, allow_status_change=True)
            materialized["pdl_program"] = serialize_queue_entry_as_pdl(materialized)
            queue_entries.append(materialized)
            existing[key] = materialized
            existing_by_route[_route_identity(materialized)] = materialized
            added += 1
            continue
        current_status = str(current.get("status", "")).strip().lower()
        if current_status not in {"proved", "disproved", "blocked", "deferred", "prior_art_found"}:
            current["queue_key"] = key
            for field, value in entry.items():
                if field in {
                    "attempt_ids",
                    "created_utc",
                    "final_attempt_id",
                    "queue_id",
                    "reopen_on_refresh",
                    "resolution_summary",
                    "result_id",
                    "status",
                }:
                    continue
                if value not in (None, "", [], {}):
                    current[field] = value
            current["retired_from_active_frontier"] = bool(entry.get("retired_from_active_frontier", False))
            current["retired_reason"] = str(entry.get("retired_reason", "")).strip()
            if not current["retired_from_active_frontier"] and str(current.get("deferred_by", "")).strip() == "inactive-discovery-frontier":
                current["deferred_by"] = ""
                current["deferred_reason"] = ""
            current["updated_utc"] = now
            _backfill_mathematical_layers(current)
            _apply_interpretability_contract(current, allow_status_change=True)
            current["pdl_program"] = serialize_queue_entry_as_pdl(current)
            existing[key] = current
            existing_by_route[_route_identity(current)] = current
            updated += 1
        elif current_status in {"blocked", "deferred"}:
            current["queue_key"] = key
            for field, value in entry.items():
                if field in {
                    "attempt_ids",
                    "created_utc",
                    "final_attempt_id",
                    "queue_id",
                    "reopen_on_refresh",
                    "resolution_summary",
                    "result_id",
                    "status",
                }:
                    continue
                if value not in (None, "", [], {}):
                    current[field] = value
            current["retired_from_active_frontier"] = bool(entry.get("retired_from_active_frontier", False))
            current["retired_reason"] = str(entry.get("retired_reason", "")).strip()
            if not current["retired_from_active_frontier"] and str(current.get("deferred_by", "")).strip() == "inactive-discovery-frontier":
                current["deferred_by"] = ""
                current["deferred_reason"] = ""
            if reopen_on_refresh and not current["retired_from_active_frontier"]:
                current["status"] = "pending"
                current["final_attempt_id"] = ""
                current["result_id"] = ""
                current["resolution_summary"] = ""
                if str(current.get("deferred_by", "")).strip() in {
                    "inactive-discovery-frontier",
                    "llm-interpretability-gate",
                }:
                    current["deferred_by"] = ""
                    current["deferred_reason"] = ""
            current["updated_utc"] = now
            _backfill_mathematical_layers(current)
            _apply_interpretability_contract(current, allow_status_change=True)
            current["pdl_program"] = serialize_queue_entry_as_pdl(current)
            existing[key] = current
            existing_by_route[_route_identity(current)] = current
            updated += 1
    queue["entries"] = sorted(
        queue_entries,
        key=lambda item: (float(item.get("priority", 0.0) or 0.0), str(item.get("queue_id", ""))),
        reverse=True,
    )
    _refresh_queue_metadata(queue)
    return added, updated


def consume_next_entry(queue: dict[str, Any], *, attempt_id: str, queue_id: str = "") -> dict[str, Any]:
    selected: dict[str, Any] | None = None
    if queue_id:
        for row in queue.get("entries", []):
            if isinstance(row, dict) and str(row.get("queue_id", "")).strip() == queue_id:
                selected = row
                break
    else:
        pending = [
            row
            for row in queue.get("entries", [])
            if isinstance(row, dict) and str(row.get("status", "pending")).strip().lower() == "pending"
        ]
        if pending:
            pending.sort(key=queue_entry_selection_sort_key)
            selected = pending[0]
    if selected is None:
        raise ValueError("No pending proof-queue entry available.")
    _apply_interpretability_contract(selected, allow_status_change=True)
    contract = selected.get("interpretability_contract") if isinstance(selected.get("interpretability_contract"), dict) else {}
    if not contract.get("ready", True):
        raise ValueError(
            f"Queue entry `{selected.get('queue_id', '')}` is deferred by the LLM interpretability gate: "
            f"{contract.get('summary', 're-encode before retrying.')}"
        )
    status = str(selected.get("status", "pending")).strip().lower() or "pending"
    if status not in {"pending", "deferred"}:
        raise ValueError(f"Queue entry `{selected.get('queue_id', '')}` is not consumable from status `{status}`.")
    selected["status"] = "in_progress"
    selected["updated_utc"] = _utc_now()
    attempts = selected.get("attempt_ids", [])
    if not isinstance(attempts, list):
        attempts = []
    if attempt_id not in attempts:
        attempts.append(attempt_id)
    selected["attempt_ids"] = attempts
    _refresh_queue_metadata(queue)
    return selected


def finalize_queue_entry(
    queue: dict[str, Any],
    *,
    queue_id: str,
    outcome: str,
    result_id: str,
    attempt_id: str,
    summary: str,
) -> dict[str, Any]:
    normalized_outcome = str(outcome or "").strip().lower()
    if normalized_outcome not in QUEUE_STATUSES - {"pending", "in_progress"}:
        raise ValueError(f"Unsupported proof outcome `{outcome}`.")
    for row in queue.get("entries", []):
        if not isinstance(row, dict):
            continue
        if str(row.get("queue_id", "")).strip() != queue_id:
            continue
        row["status"] = normalized_outcome
        row["updated_utc"] = _utc_now()
        row["final_attempt_id"] = attempt_id
        row["result_id"] = result_id
        row["resolution_summary"] = str(summary or "").strip()
        _refresh_queue_metadata(queue)
        return row
    raise ValueError(f"Queue entry `{queue_id}` not found.")


def render_proof_queue_markdown(queue: dict[str, Any]) -> str:
    metadata = queue.get("metadata", {}) if isinstance(queue.get("metadata"), dict) else {}
    entries = [row for row in queue.get("entries", []) if isinstance(row, dict)]
    status_order = {
        "pending": 0,
        "in_progress": 1,
        "deferred": 2,
        "blocked": 3,
        "proved": 4,
        "disproved": 5,
        "prior_art_found": 6,
    }
    entries = sorted(
        entries,
        key=lambda row: (
            7 if (
                str(row.get("status", "")).strip().lower() == "deferred"
                and str(row.get("deferred_by", "")).strip() == "inactive-discovery-frontier"
            ) else status_order.get(str(row.get("status", "")).strip().lower(), 99),
            *queue_entry_selection_sort_key(row),
        ),
    )
    lines = [
        "# Proof Queue",
        "",
        f"- KB ref: {metadata.get('kb_ref', '')}",
        f"- Updated (UTC): {metadata.get('updated_utc', '')}",
        f"- Pending: {metadata.get('pending_count', 0)}",
        f"- In progress: {metadata.get('in_progress_count', 0)}",
        f"- Completed: {metadata.get('completed_count', 0)}",
        "",
        "| Rank | Queue ID | Status | Priority | Conjecture | Bridge | Target |",
        "|---|---|---|---:|---|---|---|",
    ]
    for idx, row in enumerate(entries, start=1):
        claim = str(row.get("conjecture_statement") or row.get("claim_text", "")).strip().replace("\n", " ")
        if len(claim) > 110:
            claim = claim[:107].rstrip() + "..."
        lines.append(
            "| "
            f"{idx} | {row.get('queue_id', '')} | {row.get('status', '')} | {float(row.get('priority', 0.0) or 0.0):.3f} | "
            f"{claim} | {row.get('bridge_id', '')} | {row.get('target_statement_id', '')} |"
        )
    if not entries:
        lines.append("| - | - | - | - | - | - | - |")
    lines.append("")
    for row in entries:
        pdl_program = row.get("pdl_program") if isinstance(row.get("pdl_program"), dict) else serialize_queue_entry_as_pdl(row)
        contract = row.get("interpretability_contract") if isinstance(row.get("interpretability_contract"), dict) else {}
        diagnosis = row.get("inference_diagnosis") if isinstance(row.get("inference_diagnosis"), dict) else {}
        math_layers = row.get("mathematical_layers") if isinstance(row.get("mathematical_layers"), dict) else {}
        latex_layer = math_layers.get("latex") if isinstance(math_layers.get("latex"), dict) else {}
        lean_layer = math_layers.get("lean_style") if isinstance(math_layers.get("lean_style"), dict) else {}
        blockers = contract.get("blockers") if isinstance(contract.get("blockers"), list) else []
        warnings = contract.get("warnings") if isinstance(contract.get("warnings"), list) else []
        symbol_rows = [
            f"{str(item.get('symbol', '')).strip()}: {str(item.get('meaning', '')).strip()}"
            for item in math_layers.get("symbol_ledger", [])
            if isinstance(item, dict) and str(item.get("symbol", "")).strip()
        ] if isinstance(math_layers.get("symbol_ledger"), list) else []
        lines.extend(
            [
                f"## {row.get('queue_id', '')}",
                "",
                f"- Status: {row.get('status', '')}",
                f"- Priority: {float(row.get('priority', 0.0) or 0.0):.3f}",
                f"- LLM interpretability: {contract.get('status', '')} (score={contract.get('score', 0)})",
                f"- Deferred by: {row.get('deferred_by', '')}",
                f"- Bridge: {row.get('bridge_id', '')}",
                f"- Source: {row.get('source_statement_id', '')}",
                f"- Target: {row.get('target_statement_id', '')}",
                f"- Claim type: {row.get('claim_type', '')}",
                f"- Conjecture: {row.get('conjecture_statement') or row.get('claim_text', '')}",
                f"- Route synopsis: {row.get('route_synopsis', '')}",
                f"- Route lemma under test: {row.get('missing_route_lemma', '')}",
                f"- Candidate object: {row.get('candidate_object', '')}",
                f"- Carrier kind: {row.get('carrier_kind', '')}",
                f"- Invariant: {row.get('preserved_invariant', '')}",
                f"- Source theorem excerpt: {row.get('source_excerpt', '')}",
                f"- Target theorem excerpt: {row.get('target_excerpt', '')}",
                f"- Gate summary: {contract.get('summary', '')}",
                f"- Gate blockers: {' | '.join(str(value) for value in blockers[:3])}",
                f"- Gate warnings: {' | '.join(str(value) for value in warnings[:3])}",
                f"- Context status: {diagnosis.get('context_status', '')}",
                f"- Inference status: {diagnosis.get('inference_status', '')}",
                f"- Minimal repair: {diagnosis.get('minimal_repair', '')}",
                f"- Certainty now: {diagnosis.get('certainty_now', '')}",
                f"- Certainty if well posed: {diagnosis.get('certainty_if_well_posed', '')}",
                f"- Quantifier signature: {math_layers.get('quantifier_signature', '')}",
                f"- Symbol ledger: {' | '.join(symbol_rows[:6])}",
                f"- LaTeX theorem: {latex_layer.get('theorem_statement', '')}",
                f"- Lean-style scaffold: {lean_layer.get('theorem_name', '')}",
                "",
            ]
        )
        lean_scaffold = str(lean_layer.get("scaffold", "")).strip()
        if lean_scaffold:
            lines.extend(
                [
                    "```lean",
                    lean_scaffold,
                    "```",
                    "",
                ]
            )
        lines.extend(render_pdl_program_markdown(pdl_program))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
