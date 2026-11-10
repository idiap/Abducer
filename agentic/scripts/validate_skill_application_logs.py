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

"""Validate runtime skill application logs."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_common import ROOT, fail, load_json_object, rel


SCHEMA = ROOT / "agentic" / "spec" / "skill_application_log_schema.json"
LOGS = ROOT / "agentic" / "traces" / "skill_applications"


def main() -> int:
    schema = load_json_object(SCHEMA)
    paths = sorted(LOGS.glob("*.jsonl"))
    if not paths:
        fail("no skill application logs found")
    required = set(schema["required_fields"])
    lifecycle = set(schema["lifecycle_events"])
    for path in paths:
        seen_events: set[str] = set()
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"{rel(path)}:{line_no} invalid JSON: {exc}")
            missing = required - set(row)
            if missing:
                fail(f"{rel(path)}:{line_no} missing fields: {', '.join(sorted(missing))}")
            if row["event"] not in lifecycle:
                fail(f"{rel(path)}:{line_no} unknown lifecycle event: {row['event']}")
            seen_events.add(row["event"])
        if "skill_application_start" not in seen_events or "skill_application_complete" not in seen_events:
            fail(f"{rel(path)} missing start or complete lifecycle events")
    print(f"validated {len(paths)} skill application log files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
