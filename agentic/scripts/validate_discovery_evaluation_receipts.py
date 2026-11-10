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
"""Validate independent discovery-evaluation receipts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, validate_schema_file  # noqa: E402
from agentic.discovery.evaluation import validate_evaluation_receipt  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipts", nargs="*", type=Path)
    args = parser.parse_args()
    validate_schema_file("discovery_evaluation_receipt.schema.json")
    receipts: list[dict] = []
    for path in args.receipts:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and "evaluation_receipts" in payload:
            wrapped = payload["evaluation_receipts"]
            if not isinstance(wrapped, list) or not wrapped:
                raise ContractError(
                    f"canonical wrapper has no evaluation receipts: {path}"
                )
            receipts.extend(wrapped)
        elif isinstance(payload, dict):
            receipts.append(payload)
        else:
            raise ContractError(f"evaluation input must be an object: {path}")
    for receipt in receipts:
        validate_evaluation_receipt(receipt)
    print(f"validated {len(receipts)} discovery evaluation receipt(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
