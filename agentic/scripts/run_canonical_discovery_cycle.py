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
"""Commit one receipt-backed, theory-first discovery cycle.

The request document contains exact target/run/state identity, dispatcher
requests and receipts, and a semantic role map for their output paths.  This CLI
is intentionally thin: all validation, evaluation, ledger construction,
scheduling, and compare-and-swap behavior lives in
``agentic.discovery.cycle``.  The optional output file is a projection; the
transaction store remains authoritative.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.cycle import run_canonical_discovery_cycle  # noqa: E402
from agentic.discovery.contracts import ContractError  # noqa: E402


def _load(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read canonical cycle request {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ContractError("canonical cycle request must be a JSON object")
    return payload


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    """Write a non-authoritative result projection without partial bytes."""

    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True, help="Canonical cycle request JSON")
    parser.add_argument("--workspace", type=Path, default=ROOT, help="Artifact trust-boundary root")
    parser.add_argument("--state-root", type=Path, required=True, help="Canonical transaction-store root")
    parser.add_argument("--output", type=Path, help="Optional result projection JSON")
    args = parser.parse_args()
    request = _load(args.request)
    result = run_canonical_discovery_cycle(
        workspace=args.workspace,
        state_root=args.state_root,
        target_id=request["target_id"],
        run_id=request["run_id"],
        state_version=request["state_version"],
        operator_requests=request["operator_requests"],
        operator_receipts=request["operator_receipts"],
        artifact_roles=request["artifact_roles"],
        evaluator_identity=request["evaluator_identity"],
        evaluator_version=request.get("evaluator_version", "canonical-independent-evaluator/1.0.0"),
        proof_request=request.get("proof_request"),
        idempotency_key=request.get("idempotency_key"),
    )
    if args.output:
        _write_atomic(args.output, result)
    json.dump(result, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        print(f"canonical discovery cycle failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
