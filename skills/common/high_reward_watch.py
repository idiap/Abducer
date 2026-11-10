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

"""Persistent watch-state for high-value intermediate results that justify continued work."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


WATCH_VERSION = 1
SIGNAL_STATUSES = {"pending", "active", "completed", "expired"}


def _utc_now() -> str:
    """Return the current UTC timestamp for persisted watch metadata."""

    return dt.datetime.now(dt.UTC).isoformat()


def _clean_text(value: Any) -> str:
    """Normalize free-form values into a stable single-line string."""

    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    """Coerce arbitrary values into dictionary-shaped payloads."""

    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    """Coerce arbitrary values into list-shaped payloads."""

    return value if isinstance(value, list) else []


def _safe_int(value: Any, default: int = 0) -> int:
    """Parse an integer-like value while preserving a fallback."""

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def high_reward_watch_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical JSON and Markdown paths for the high-reward watch artifact."""

    return artifacts_dir / "high-reward-watch.json", artifacts_dir / "high-reward-watch.md"


def default_high_reward_watch(*, kb_ref: str) -> dict[str, Any]:
    """Construct an empty high-reward watch for one problem."""

    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": _clean_text(kb_ref),
            "watch_version": WATCH_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "signal_count": 0,
            "pending_count": 0,
            "active_count": 0,
            "completed_count": 0,
            "expired_count": 0,
            "active_signal_id": "",
        },
        "signals": [],
    }


def load_high_reward_watch(path: Path, *, kb_ref: str) -> dict[str, Any]:
    """Load a persisted high-reward watch while repairing malformed structure."""

    if not path.exists():
        return default_high_reward_watch(kb_ref=kb_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default_high_reward_watch(kb_ref=kb_ref)
    if not isinstance(payload, dict):
        return default_high_reward_watch(kb_ref=kb_ref)
    payload.setdefault("metadata", {})
    payload.setdefault("signals", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["signals"], list):
        payload["signals"] = []
    payload["metadata"]["kb_ref"] = _clean_text(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"]["watch_version"] = WATCH_VERSION
    _refresh_watch_metadata(payload)
    return payload


def _refresh_watch_metadata(watch: dict[str, Any]) -> None:
    """Recompute aggregate watch counts from the materialized signals."""

    meta = _ensure_dict(watch.get("metadata"))
    signals = [row for row in _ensure_list(watch.get("signals")) if isinstance(row, dict)]
    counts = {
        "pending_count": 0,
        "active_count": 0,
        "completed_count": 0,
        "expired_count": 0,
    }
    active_signal_id = ""
    for row in signals:
        status = _clean_text(row.get("status")).lower()
        if status == "pending":
            counts["pending_count"] += 1
        elif status == "active":
            counts["active_count"] += 1
            if not active_signal_id:
                active_signal_id = _clean_text(row.get("signal_id"))
        elif status == "completed":
            counts["completed_count"] += 1
        elif status == "expired":
            counts["expired_count"] += 1
    meta["watch_version"] = WATCH_VERSION
    meta["updated_utc"] = _utc_now()
    meta["signal_count"] = len(signals)
    meta["active_signal_id"] = active_signal_id
    meta.update(counts)
    watch["metadata"] = meta


def render_high_reward_watch_markdown(watch: dict[str, Any]) -> str:
    """Render the high-reward watch as a concise continuation ledger."""

    meta = _ensure_dict(watch.get("metadata"))
    signals = [row for row in _ensure_list(watch.get("signals")) if isinstance(row, dict)]
    lines = [
        "# High-Reward Watch",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Updated (UTC): {meta.get('updated_utc', '')}",
        f"- Signals: {meta.get('signal_count', 0)}",
        f"- Pending: {meta.get('pending_count', 0)}",
        f"- Active: {meta.get('active_count', 0)}",
        f"- Completed: {meta.get('completed_count', 0)}",
        f"- Expired: {meta.get('expired_count', 0)}",
        f"- Active signal: {meta.get('active_signal_id', '')}",
        "",
    ]
    if not signals:
        lines.append("- No high-reward continuation signals recorded.")
        lines.append("")
        return "\n".join(lines)
    for row in signals:
        lines.extend(
            [
                f"## {row.get('signal_id', '')}",
                "",
                f"- Status: {row.get('status', '')}",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Queue ID: {row.get('queue_id', '')}",
                f"- Outcome: {row.get('outcome', '')}",
                f"- Title: {row.get('title', '')}",
                f"- Score: {row.get('major_subresult_score', 0)}",
                f"- Recommended extension cycles: {row.get('recommended_extension_cycles', 0)}",
                f"- Activated at cycle: {row.get('activated_at_cycle', '')}",
                f"- Rationale: {row.get('continuation_rationale', '')}",
                f"- Follow-up proof queue IDs: {', '.join(_ensure_list(row.get('follow_up_prove_queue_ids')))}",
                f"- Follow-up discovery branch IDs: {', '.join(_ensure_list(row.get('follow_up_discovery_branch_ids')))}",
                f"- Resolution note: {row.get('resolution_note', '')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def save_high_reward_watch(watch: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    """Persist the high-reward watch in JSON and Markdown form."""

    _refresh_watch_metadata(watch)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(watch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_high_reward_watch_markdown(watch), encoding="utf-8")


def _next_signal_id(watch: dict[str, Any], *, kb_ref: str) -> str:
    """Allocate the next monotonic signal identifier for the watch."""

    prefix = f"highreward.{_clean_text(kb_ref)}."
    current_max = 0
    for row in _ensure_list(watch.get("signals")):
        if not isinstance(row, dict):
            continue
        signal_id = _clean_text(row.get("signal_id"))
        if not signal_id.startswith(prefix):
            continue
        suffix = signal_id[len(prefix) :]
        if suffix.isdigit():
            current_max = max(current_max, int(suffix))
    return f"{prefix}{current_max + 1:03d}"


def append_high_reward_signal(watch: dict[str, Any], signal: dict[str, Any], *, kb_ref: str) -> dict[str, Any]:
    """Append or refresh a normalized high-reward signal in the persistent watch."""

    normalized = dict(signal)
    normalized.setdefault("signal_id", _next_signal_id(watch, kb_ref=kb_ref))
    normalized.setdefault("status", "pending")
    normalized.setdefault("created_utc", _utc_now())
    normalized["updated_utc"] = _utc_now()
    normalized["recommended_extension_cycles"] = max(
        1,
        _safe_int(normalized.get("recommended_extension_cycles"), 4),
    )
    existing_by_result = {
        _clean_text(row.get("result_id")): row
        for row in _ensure_list(watch.get("signals"))
        if isinstance(row, dict) and _clean_text(row.get("result_id"))
    }
    current = existing_by_result.get(_clean_text(normalized.get("result_id")))
    if current is None:
        watch.setdefault("signals", []).append(normalized)
        _refresh_watch_metadata(watch)
        return normalized
    for field, value in normalized.items():
        if value not in (None, "", [], {}):
            current[field] = value
    current["updated_utc"] = _utc_now()
    _refresh_watch_metadata(watch)
    return current


def update_signal_status(
    watch: dict[str, Any],
    *,
    signal_id: str,
    status: str,
    note: str = "",
    activated_at_cycle: int | None = None,
) -> dict[str, Any]:
    """Update one signal lifecycle state while preserving the rest of the watch."""

    normalized_signal_id = _clean_text(signal_id)
    normalized_status = _clean_text(status).lower() or "pending"
    if normalized_status not in SIGNAL_STATUSES:
        raise ValueError(f"Unsupported high-reward signal status `{status}`.")
    for row in _ensure_list(watch.get("signals")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("signal_id")) != normalized_signal_id:
            continue
        row["status"] = normalized_status
        row["updated_utc"] = _utc_now()
        if note:
            row["resolution_note"] = _clean_text(note)
        if activated_at_cycle is not None:
            row["activated_at_cycle"] = int(activated_at_cycle)
        _refresh_watch_metadata(watch)
        return row
    raise ValueError(f"High-reward signal `{signal_id}` not found.")


def _queue_followup_counts(signal: dict[str, Any], queue: dict[str, Any]) -> dict[str, int]:
    """Count live proof-queue follow-ups attached to one signal."""

    wanted = {
        _clean_text(value)
        for value in _ensure_list(signal.get("follow_up_prove_queue_ids"))
        if _clean_text(value)
    }
    counts = {"pending": 0, "in_progress": 0}
    if not wanted:
        return counts
    for row in _ensure_list(queue.get("entries")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("queue_id")) not in wanted:
            continue
        status = _clean_text(row.get("status")).lower()
        if status == "pending":
            counts["pending"] += 1
        elif status == "in_progress":
            counts["in_progress"] += 1
    return counts


def _branch_followup_counts(signal: dict[str, Any], branch_state: dict[str, Any]) -> dict[str, int]:
    """Count live discovery-branch follow-ups attached to one signal."""

    wanted = {
        _clean_text(value)
        for value in _ensure_list(signal.get("follow_up_discovery_branch_ids"))
        if _clean_text(value)
    }
    counts = {"pending": 0, "in_progress": 0, "active": 0}
    if not wanted:
        return counts
    for row in _ensure_list(branch_state.get("branches")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("branch_id")) not in wanted:
            continue
        status = _clean_text(row.get("status")).lower()
        if status == "pending":
            counts["pending"] += 1
        elif status == "in_progress":
            counts["in_progress"] += 1
        elif status == "active":
            counts["active"] += 1
    return counts


def signal_live_followups(
    signal: dict[str, Any],
    *,
    queue: dict[str, Any],
    branch_state: dict[str, Any],
) -> dict[str, Any]:
    """Summarize whether a signal still has live proof or discovery work attached to it."""

    queue_counts = _queue_followup_counts(signal, queue)
    branch_counts = _branch_followup_counts(signal, branch_state)
    live_total = sum(queue_counts.values()) + sum(branch_counts.values())
    return {
        "queue": queue_counts,
        "branches": branch_counts,
        "live_total": live_total,
        "has_live_followups": live_total > 0,
    }


def select_high_reward_signal_for_continuation(
    watch: dict[str, Any],
    *,
    queue: dict[str, Any],
    branch_state: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Choose the strongest pending or active signal that still has live follow-up work."""

    candidates = [row for row in _ensure_list(watch.get("signals")) if isinstance(row, dict)]
    ranked: list[tuple[int, int, dict[str, Any], dict[str, Any]]] = []
    for row in candidates:
        status = _clean_text(row.get("status")).lower()
        if status not in {"pending", "active"}:
            continue
        followup_status = signal_live_followups(row, queue=queue, branch_state=branch_state)
        if not followup_status["has_live_followups"]:
            continue
        rank = 0 if status == "active" else 1
        score = _safe_int(row.get("major_subresult_score"))
        ranked.append((rank, -score, row, followup_status))
    ranked.sort(key=lambda item: (item[0], item[1], _clean_text(item[2].get("signal_id"))))
    if not ranked:
        return None, {"has_live_followups": False, "live_total": 0, "queue": {}, "branches": {}}
    _rank, _score, signal, followup_status = ranked[0]
    return signal, followup_status
