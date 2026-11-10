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
"""Evaluate a discovery delta independently on structural theory virtues."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.evaluation import evaluate_discovery_delta  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--genealogy", type=Path)
    parser.add_argument("--evaluator", required=True)
    parser.add_argument("--invocation", required=True)
    parser.add_argument("--version", default="discovery-evaluator/1.0.0")
    parser.add_argument("--deterministic-validator", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    genealogy = json.loads(args.genealogy.read_text(encoding="utf-8")) if args.genealogy else []
    receipt = evaluate_discovery_delta(
        candidate,
        evaluator_identity=args.evaluator,
        evaluator_invocation_id=args.invocation,
        evaluator_version=args.version,
        genealogy=genealogy,
        deterministic_validator=args.deterministic_validator,
    )
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
