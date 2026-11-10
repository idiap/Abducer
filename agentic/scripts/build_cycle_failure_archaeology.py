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
"""Build the cycle failure archaeology report for a discovery marathon."""

from __future__ import annotations

import argparse

from agentic_common import rel
from cycle_failure_archaeology import build_for_active_run, write_failure_archaeology_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="", help="Target id; defaults to the active run target")
    parser.add_argument("--run-id", default="", help="Run id; defaults to the active run for the target")
    parser.add_argument("--since-cycle", type=int, default=0, help="Analyze cycles with index >= this value")
    parser.add_argument("--last", type=int, default=5, help="Analyze the last N cycles when --since-cycle is not set")
    parser.add_argument("--no-write", action="store_true", help="Build and print status without writing artifacts")
    args = parser.parse_args()
    report = build_for_active_run(args.target, args.run_id, since_cycle=args.since_cycle, last=args.last)
    if args.no_write:
        print(
            f"built failure archaeology for {report.get('cycle_set', {}).get('target_id', '')} "
            f"cycles={report.get('cycle_set', {}).get('cycle_ids', [])} "
            f"failure_detected={report.get('failure_detected')}"
        )
        return 0
    paths = write_failure_archaeology_report(report)
    print(f"Wrote {rel(paths['latest_json'])}")
    print(f"Wrote {rel(paths['latest_md'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
