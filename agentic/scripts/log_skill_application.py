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

"""Append a control-plane skill application event."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_common import ROOT, utc_now


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--target-id", required=True)
    parser.add_argument("--workflow-id", required=True)
    parser.add_argument("--skill-id", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()
    out = ROOT / "agentic" / "traces" / "skill_applications" / f"{args.run_id}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "event": args.event,
        "run_id": args.run_id,
        "target_id": args.target_id,
        "workflow_id": args.workflow_id,
        "skill_id": args.skill_id,
        "timestamp_utc": utc_now(),
        "summary": args.summary,
        "evidence_paths": args.evidence,
    }
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
