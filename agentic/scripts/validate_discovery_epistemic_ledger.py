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
"""Read-only validation for epistemic schemas and optional concrete ledgers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, validate_schema_file
from agentic.discovery.ledger import EpistemicLedger, reduce_events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    validate_schema_file("discovery_epistemic_event.schema.json")
    validate_schema_file("discovery_epistemic_state.schema.json")
    if args.ledger:
        state = reduce_events(EpistemicLedger(args.ledger).read())
        print(f"valid ledger: {state['event_count']} events, generation {state['generation']}")
    else:
        print("epistemic event and state schemas are valid")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
