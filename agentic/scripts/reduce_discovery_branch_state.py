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
"""Apply one typed learning delta through the authoritative CAS reducer."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, fsync_directory, load_json
from agentic.discovery.learning import LearningReducer, ReducerPolicy


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--expected-generation", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--plateau-threshold", type=int, default=3)
    parser.add_argument("--plateau-action", choices=("pivot", "backtrack", "exhaust"), default="pivot")
    args = parser.parse_args()
    state, delta = load_json(args.state), load_json(args.delta)
    if not isinstance(state, dict) or not isinstance(delta, dict):
        raise ContractError("state and delta must be JSON objects")
    reducer = LearningReducer(ReducerPolicy(args.plateau_threshold, args.plateau_action))
    next_state, receipt = reducer.reduce(state, delta, expected_generation=args.expected_generation)
    _atomic_json(args.output, next_state)
    _atomic_json(args.receipt, receipt)
    print(json.dumps({"generation": next_state["generation"], "transition": receipt["transition"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
