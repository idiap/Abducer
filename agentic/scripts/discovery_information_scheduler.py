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
"""Create or exactly-once consume a theory-first discovery action schedule."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.scheduler import consume_action_file, schedule_discovery_actions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--consume", type=Path)
    parser.add_argument("--action-id")
    parser.add_argument("--state-version", type=int)
    parser.add_argument("--consumer-receipt-id")
    args = parser.parse_args()
    if args.consume:
        if args.action_id is None or args.state_version is None or args.consumer_receipt_id is None:
            parser.error("--consume requires --action-id, --state-version, and --consumer-receipt-id")
        schedule = consume_action_file(
            args.consume,
            args.action_id,
            expected_state_version=args.state_version,
            consumer_receipt_id=args.consumer_receipt_id,
        )
    else:
        if args.state is None:
            parser.error("state is required when not consuming")
        state = json.loads(args.state.read_text(encoding="utf-8"))
        schedule = schedule_discovery_actions(state)
    rendered = json.dumps(schedule, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
