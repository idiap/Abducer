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
"""Run-scoped, append-only storage for public reasoning events.

The store uses a lock plus atomic replacement: a process interruption leaves either
the previous complete JSONL file or the next complete one, never a partial event.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_ROOT = ROOT / "agentic" / "traces" / "public_reasoning"
SCHEMA_VERSION = "2.0.0"


class TraceStoreError(ValueError):
    """Raised when an event would violate run identity or causal integrity."""


def _safe_id(value: object, label: str) -> str:
    text = str(value or "").strip()
    if not text or not re.fullmatch(r"[A-Za-z0-9._:-]+", text):
        raise TraceStoreError(f"{label} must match [A-Za-z0-9._:-]+")
    return text


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def stable_event_id(event: dict[str, Any]) -> str:
    identity = {
        key: event.get(key)
        for key in ("run_id", "workflow_id", "workflow_version", "phase", "step_id", "skill", "attempt", "event_family", "idempotency_key")
    }
    return "evt-" + hashlib.sha256(_canonical(identity)).hexdigest()[:24]


def validate_status_semantics(event: dict[str, Any]) -> None:
    """Reject authority-free epistemic upgrades and unsupported scope widening."""

    inference = event.get("public_inference") if isinstance(event.get("public_inference"), dict) else {}
    authority = event.get("authority") if isinstance(event.get("authority"), dict) else {}
    evidence = event.get("evidence") if isinstance(event.get("evidence"), list) else []
    exercised = authority.get("exercised") if isinstance(authority.get("exercised"), list) else []
    status = str(event.get("claim_epistemic_status", ""))
    if status in {"evidence_backed", "validated"} and (
        not str(inference.get("warrant", "")).strip() or not evidence or not exercised
    ):
        raise TraceStoreError(f"{status} claims require a public warrant, evidence, and explicit authority")
    scope = inference.get("scope") if isinstance(inference.get("scope"), dict) else {}
    before = str(scope.get("before", "")).strip()
    after = str(scope.get("after", "")).strip()
    if before and after and before != after and (
        not str(inference.get("warrant", "")).strip() or not evidence or not exercised
    ):
        raise TraceStoreError("scope transition requires a public warrant, evidence, and explicit authority")


def _atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


@contextmanager
def _run_lock(run_dir: Path) -> Iterator[None]:
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / ".lock").open("a+", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def read_events(run_id: str, *, store_root: Path = DEFAULT_STORE_ROOT) -> list[dict[str, Any]]:
    path = store_root / "runs" / _safe_id(run_id, "run_id") / "events.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise TraceStoreError(f"non-object event in {path}")
            rows.append(value)
    return rows


def append_event(
    event: dict[str, Any],
    *,
    store_root: Path = DEFAULT_STORE_ROOT,
    latest_name: str | None = None,
    link_to_latest: bool = False,
) -> dict[str, Any]:
    """Append one event, returning the stored event (or existing idempotent row)."""

    candidate = dict(event)
    candidate["schema_version"] = SCHEMA_VERSION
    run_id = _safe_id(candidate.get("run_id"), "run_id")
    candidate["run_id"] = run_id
    for required in ("workflow_id", "workflow_version", "target", "phase", "event_family"):
        if not str(candidate.get(required, "")).strip():
            raise TraceStoreError(f"missing {required}")
    candidate.setdefault("attempt", 1)
    candidate.setdefault("causal_parent_event_ids", [])
    candidate.setdefault("parent_artifact_ids", [])
    candidate.setdefault("artifact_validation_status", "not_checked")
    candidate.setdefault("claim_epistemic_status", "not_applicable")
    candidate.setdefault("workflow_disposition", "observed")
    candidate.setdefault("evidence", [])
    candidate.setdefault("authority", {"exercised": [], "absent": [], "prohibitions_checked": []})
    candidate.setdefault(
        "public_inference",
        {
            "question": "",
            "premises": [],
            "operator": "",
            "warrant": "",
            "conclusion": "",
            "assumptions": [],
            "alternatives": [],
            "falsifiers": [],
            "uncertainty": "",
            "scope": {"regime": "", "model": "", "before": "", "after": ""},
            "trace_completeness": "not_applicable",
        },
    )
    validate_status_semantics(candidate)
    candidate["event_id"] = _safe_id(candidate.get("event_id") or stable_event_id(candidate), "event_id")

    run_dir = store_root / "runs" / run_id
    with _run_lock(run_dir):
        rows = read_events(run_id, store_root=store_root)
        by_id = {str(row.get("event_id")): row for row in rows}
        if candidate["event_id"] in by_id:
            previous = by_id[candidate["event_id"]]
            if link_to_latest and not candidate["causal_parent_event_ids"]:
                candidate["causal_parent_event_ids"] = list(previous.get("causal_parent_event_ids", []))
            # Sequence and source timestamp are store-assigned and excluded when
            # checking whether a retry has the same stable meaning.
            comparable = lambda row: {k: v for k, v in row.items() if k not in {"sequence", "timestamp_utc"}}
            if comparable(previous) != comparable(candidate):
                raise TraceStoreError(f"event_id {candidate['event_id']} was reused with different content")
            return previous

        if link_to_latest and not candidate["causal_parent_event_ids"] and rows:
            candidate["causal_parent_event_ids"] = [str(rows[-1]["event_id"])]

        unknown_parents = sorted(set(candidate["causal_parent_event_ids"]) - set(by_id))
        if unknown_parents:
            raise TraceStoreError(f"unknown causal parent(s): {', '.join(unknown_parents)}")
        candidate["sequence"] = len(rows) + 1
        candidate.setdefault("timestamp_utc", dt.datetime.now(dt.UTC).isoformat())
        rows.append(candidate)
        _atomic_write(run_dir / "events.jsonl", "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows))

        first = rows[0]
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "workflow_id": first["workflow_id"],
            "workflow_version": first["workflow_version"],
            "profile_id": first.get("profile_id"),
            "target": first["target"],
            "event_count": len(rows),
            "first_event_id": first["event_id"],
            "latest_event_id": candidate["event_id"],
            "status": "running",
        }
        _atomic_write(run_dir / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        if latest_name:
            latest = store_root / "latest" / f"{_safe_id(latest_name, 'latest_name')}.json"
            _atomic_write(latest, json.dumps(candidate, indent=2, sort_keys=True) + "\n")
        return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", type=Path)
    parser.add_argument("--store-root", type=Path, default=DEFAULT_STORE_ROOT)
    parser.add_argument("--latest-name")
    args = parser.parse_args()
    value = json.loads(args.event.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TraceStoreError("event input must be an object")
    print(json.dumps(append_event(value, store_root=args.store_root, latest_name=args.latest_name), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
