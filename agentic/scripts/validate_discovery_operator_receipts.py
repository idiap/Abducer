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
"""Validate operator schemas or a concrete request/receipt execution set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError, load_json, validate_schema_file
from agentic.discovery.receipts import ensure_evaluation_ready


def main() -> int:
    """Perform read-only receipt validation; never refresh tracked artifacts."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--workspace", type=Path, default=ROOT)
    args = parser.parse_args()
    validate_schema_file("discovery_operator_request.schema.json")
    validate_schema_file("discovery_operator_receipt.schema.json")
    if args.requests is None and args.receipts is None:
        print("operator request and receipt schemas are valid")
        return 0
    if args.requests is None or args.receipts is None:
        raise ContractError("--requests and --receipts must be supplied together")
    request_payload, receipt_payload = load_json(args.requests), load_json(args.receipts)
    requests = request_payload
    if isinstance(request_payload, dict):
        requests = request_payload.get(
            "requests", request_payload.get("operator_requests")
        )
    receipts = receipt_payload
    if isinstance(receipt_payload, dict):
        receipts = receipt_payload.get(
            "receipts", receipt_payload.get("operator_receipts")
        )
    if not isinstance(requests, list) or not isinstance(receipts, list):
        raise ContractError(
            "validation inputs must be arrays or canonical "
            "requests/operator_requests and receipts/operator_receipts wrappers"
        )
    ensure_evaluation_ready(requests, receipts, workspace=args.workspace)
    print(json.dumps({"valid_requests": len(requests), "valid_receipts": len(receipts)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
