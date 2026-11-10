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
"""Replay a versioned epistemic fixture and verify its expected state digest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, canonical_digest, load_json
from agentic.discovery.ledger import replay_fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--print-state", action="store_true")
    args = parser.parse_args()
    fixture = load_json(args.fixture)
    if not isinstance(fixture, dict):
        raise ContractError("fixture must be an object")
    state = replay_fixture(fixture)
    if args.print_state:
        print(json.dumps(state, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(json.dumps({"event_count": state["event_count"], "state_digest": canonical_digest(state)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
