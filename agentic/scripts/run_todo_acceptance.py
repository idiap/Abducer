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
"""Run one structured TODO's acceptance commands into an immutable receipt.

Both the TODO deck and receipt destination are repository-relative trust-boundary
paths. Destination validation happens before command execution, and writing uses
exclusive creation so reruns can confirm identical evidence but never overwrite it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "agentic/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.todo_acceptance import (  # noqa: E402
    TodoAcceptanceError,
    resolve_safe_workspace_path,
    run_acceptance,
)
from validate_todos import load_todo_rows  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--todo-file", type=Path, required=True)
    parser.add_argument("--todo-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=900)
    args = parser.parse_args()
    # Reject unsafe destinations before expensive commands or directory writes.
    output_raw = str(args.output)
    output = resolve_safe_workspace_path(
        ROOT, output_raw, context="receipt output"
    )
    todo_file = resolve_safe_workspace_path(
        ROOT,
        str(args.todo_file),
        context="TODO file",
        must_exist=True,
        require_file=True,
    )
    rows = [row for row in load_todo_rows(todo_file) if row.get("id") == args.todo_id]
    if len(rows) != 1:
        raise TodoAcceptanceError(f"expected one TODO {args.todo_id}, found {len(rows)}")
    receipt = run_acceptance(
        rows[0], todo_file=todo_file, workspace=ROOT,
        timeout_seconds=args.timeout_seconds,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output = resolve_safe_workspace_path(
        ROOT, output_raw, context="receipt output"
    )
    encoded = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    try:
        with output.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        if output.read_text(encoding="utf-8") != encoded:
            raise TodoAcceptanceError(f"immutable receipt collision: {output}")
    print(f"{receipt['overall_status']}: {args.todo_id} -> {output.relative_to(ROOT)}")
    return 0 if receipt["overall_status"] == "passed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TodoAcceptanceError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
