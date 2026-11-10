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
"""Validate exact TODO selections through fresh, independently rerun evidence.

The selected decks are authority inputs, not passive configuration. Their exact
bytes, selected-row digests, ordering, and cardinality are frozen before any
acceptance command runs and reloaded after every command. A validator therefore
cannot earn success by weakening its own card or another selected card.
"""

from __future__ import annotations

import argparse
from collections import Counter
import dataclasses
import json
import sys
from pathlib import Path
from typing import Callable

from agentic_common import ROOT, clean_text, fail, rel
from validate_todos import load_todo_rows

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.todo_acceptance import (  # noqa: E402
    TodoAcceptanceError,
    receipt_annotation_path,
    resolve_safe_workspace_path,
    self_check,
    validate_acceptance_receipt,
)
from agentic.discovery.contracts import canonical_digest  # noqa: E402


TODOS = ROOT / "agentic/todos"


@dataclasses.dataclass(frozen=True, slots=True)
class _DeckSnapshot:
    """Exact selected TODO authority state frozen around command execution."""

    paths: tuple[Path, ...]
    selected_ids: frozenset[str] | None
    deck_bytes: tuple[tuple[str, bytes], ...]
    selected_rows: tuple[tuple[str, int, str, str], ...]
    selected_cardinality: int

    def assert_unchanged(self) -> None:
        """Reload decks and reject byte, row, ordering, or cardinality drift."""

        # Check bytes first so malformed or deleted rewrites fail with the
        # trust-boundary error rather than escaping through a parser exception.
        for relative, expected in self.deck_bytes:
            current_path = resolve_safe_workspace_path(
                ROOT,
                relative,
                context="TODO file",
                must_exist=True,
                require_file=True,
            )
            if current_path.read_bytes() != expected:
                raise TodoAcceptanceError(
                    f"selected TODO deck changed during fresh validation: {relative}"
                )
        current = _capture_deck_snapshot(list(self.paths), self.selected_ids)
        if current.selected_cardinality != self.selected_cardinality:
            raise TodoAcceptanceError(
                "selected TODO cardinality changed during fresh validation"
            )
        if current.selected_rows != self.selected_rows:
            raise TodoAcceptanceError(
                "selected TODO rows changed during fresh validation"
            )


def _capture_deck_snapshot(
    paths: list[Path], todo_ids: set[str] | frozenset[str] | None
) -> _DeckSnapshot:
    """Capture stable bytes plus exact parsed selected rows for every deck."""

    selected = frozenset(todo_ids) if todo_ids is not None else None
    deck_bytes: list[tuple[str, bytes]] = []
    selected_rows: list[tuple[str, int, str, str]] = []
    for path in paths:
        resolved = path.resolve()
        relative = resolved.relative_to(ROOT).as_posix()
        safe_path = resolve_safe_workspace_path(
            ROOT,
            relative,
            context="TODO file",
            must_exist=True,
            require_file=True,
        )
        before = safe_path.read_bytes()
        rows = load_todo_rows(safe_path)
        if safe_path.read_bytes() != before:
            raise TodoAcceptanceError(
                f"selected TODO deck changed while being loaded: {relative}"
            )
        deck_bytes.append((relative, before))
        for index, row in enumerate(rows):
            todo_id = clean_text(row.get("id"))
            if selected is None or todo_id in selected:
                selected_rows.append(
                    (relative, index, todo_id, canonical_digest(row))
                )
    return _DeckSnapshot(
        paths=tuple(path.resolve() for path in paths),
        selected_ids=selected,
        deck_bytes=tuple(deck_bytes),
        selected_rows=tuple(selected_rows),
        selected_cardinality=len(selected_rows),
    )


def _validate_selection(paths: list[Path], requested_ids: list[str]) -> set[str] | None:
    """Require unique deck identities and exact coverage of requested IDs."""

    normalized = [clean_text(value) for value in requested_ids]
    if any(not value for value in normalized):
        raise TodoAcceptanceError("selected TODO IDs must be non-empty")
    if len(normalized) != len(set(normalized)):
        raise TodoAcceptanceError("selected TODO IDs must be unique")
    path_keys = [path.resolve() for path in paths]
    if len(path_keys) != len(set(path_keys)):
        raise TodoAcceptanceError("TODO files must be unique")
    counts: Counter[str] = Counter()
    for path in paths:
        for row in load_todo_rows(path):
            todo_id = clean_text(row.get("id"))
            if not todo_id:
                raise TodoAcceptanceError(f"{rel(path)} contains a TODO without an ID")
            counts[todo_id] += 1
    duplicates = sorted(todo_id for todo_id, count in counts.items() if count != 1)
    if duplicates:
        raise TodoAcceptanceError(
            "TODO IDs must occur exactly once: " + ", ".join(duplicates)
        )
    if not normalized:
        return None
    missing = sorted(set(normalized) - counts.keys())
    if missing:
        raise TodoAcceptanceError(
            "selected TODO IDs were not found exactly once: " + ", ".join(missing)
        )
    return set(normalized)


def validate_file(
    path: Path,
    *,
    todo_ids: set[str] | None = None,
    timeout_seconds: float = 900,
    state_guard: Callable[[], None] | None = None,
) -> int:
    """Validate resolved rows and freshly rerun their declared commands."""

    if state_guard is not None:
        state_guard()
    rows = load_todo_rows(path)
    if todo_ids is not None:
        rows = [row for row in rows if clean_text(row.get("id")) in todo_ids]
    unresolved: list[str] = []
    missing_evidence: list[str] = []
    stale_evidence: list[str] = []
    for row in rows:
        todo_id = clean_text(row.get("id"))
        status = clean_text(row.get("status"))
        evidence = row.get("evidence", [])
        if status != "resolved":
            unresolved.append(f"{todo_id}:{status or 'missing'}")
            continue
        if not isinstance(evidence, list) or not evidence:
            missing_evidence.append(todo_id)
            continue
        # New discovery/YM decks require receipts. Historical decks retain
        # their established evidence convention unless explicitly upgraded.
        if todo_id.startswith(("DWF-", "YM21-")):
            try:
                receipt_path = receipt_annotation_path(row, workspace=ROOT)
                encoded_receipt = receipt_path.read_bytes()
                receipt = json.loads(encoded_receipt)
                validate_acceptance_receipt(
                    receipt,
                    row,
                    todo_file=path,
                    workspace=ROOT,
                    reexecute_commands=True,
                    timeout_seconds=timeout_seconds,
                    state_guard=state_guard,
                )
                if receipt_path.read_bytes() != encoded_receipt:
                    raise TodoAcceptanceError(
                        "immutable acceptance receipt changed during validation"
                    )
            except (OSError, json.JSONDecodeError, TodoAcceptanceError, ValueError) as exc:
                stale_evidence.append(f"{todo_id}:{exc}")
    if unresolved:
        if "remaining_open_points" in path.name:
            print(f"skipped completion enforcement for intentionally open backlog {rel(path)}")
            return len(rows)
        fail(f"{rel(path)} has unresolved TODOs: {', '.join(unresolved)}")
    if missing_evidence:
        fail(f"{rel(path)} resolved TODOs missing evidence: {', '.join(missing_evidence)}")
    if stale_evidence:
        fail(f"{rel(path)} has stale or failed acceptance evidence: {'; '.join(stale_evidence)}")
    if state_guard is not None:
        state_guard()
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--todo-file", action="append", default=[])
    parser.add_argument("--todo-id", action="append", default=[])
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=900)
    args = parser.parse_args()
    if args.self_check:
        self_check(ROOT)
        print("validated TODO acceptance receipt schema and staleness self-check")
        return 0
    paths = [
        resolve_safe_workspace_path(
            ROOT,
            item,
            context="TODO file",
            must_exist=True,
            require_file=True,
        )
        for item in args.todo_file
    ] if args.todo_file else sorted(TODOS.glob("*_todos.yaml"))
    if not paths:
        fail("no TODO files found")
    selected = _validate_selection(paths, args.todo_id)
    deck_snapshot = _capture_deck_snapshot(paths, selected)
    deck_snapshot.assert_unchanged()
    total = sum(
        validate_file(
            path,
            todo_ids=selected,
            timeout_seconds=args.timeout_seconds,
            state_guard=deck_snapshot.assert_unchanged,
        )
        for path in paths
    )
    deck_snapshot.assert_unchanged()
    print(f"validated {total} resolved TODO cards across {len(paths)} TODO files")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TodoAcceptanceError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
