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
"""Build a target-scoped visual conceptualization packet."""

from __future__ import annotations

import argparse

from agentic_common import rel
from discovery_marathon_common import load_cycles, load_run_state
from visual_conceptualization import (
    DEFAULT_WINDOW,
    build_visual_conceptualization_report,
    write_visual_conceptualization_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-id", "--target", dest="target_id", default="")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--concept", default="")
    parser.add_argument("--last", type=int, default=DEFAULT_WINDOW)
    parser.add_argument("--source-report", default="")
    args = parser.parse_args()
    _, run_state = load_run_state(args.run_id or None, args.target_id or None)
    if not run_state:
        raise SystemExit("no active discovery marathon run found for the requested target/run")
    cycles = load_cycles(run_state)
    report = build_visual_conceptualization_report(
        run_state,
        cycles,
        concept=args.concept,
        last=args.last,
        source_report=args.source_report,
    )
    paths = write_visual_conceptualization_report(report)
    print(f"Wrote {rel(paths['latest_json'])}")
    print(f"Wrote {rel(paths['latest_md'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
