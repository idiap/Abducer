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
"""Build an intuition-first, literature-rebased high-risk theory portfolio."""

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

from agentic.discovery.contracts import ContractError, canonical_json, safe_relative_path
from agentic.discovery.hypotheses import (
    build_demo_high_risk_portfolio,
    forge_high_risk_portfolio,
)


def _load(path: Path) -> dict[str, Any]:
    """Load a JSON object containing charter, snapshot, and optional proposals."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load portfolio request {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("portfolio request must be a JSON object")
    return value


def _write(path: Path, payload: Any) -> None:
    """Atomically publish a content-addressed portfolio."""

    if path.name.lower() in {"latest", "latest.json", "current", "current.json"}:
        raise ContractError("mutable latest/current hypothesis outputs are forbidden")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
    ) as stream:
        temp = Path(stream.name)
        stream.write(canonical_json(payload) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def main(argv: list[str] | None = None) -> int:
    """Build the complete 8–12 candidate portfolio and write immutable JSON."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--requested-count", type=int, default=10)
    parser.add_argument("--relevance-floor", type=float, default=0.70)
    args = parser.parse_args(argv)
    try:
        if args.input is None:
            portfolio = build_demo_high_risk_portfolio()
        else:
            envelope = _load(args.input)
            portfolio = forge_high_risk_portfolio(
                envelope["charter"],
                envelope["literature_snapshot"],
                proposals=envelope.get("proposals"),
                requested_count=args.requested_count,
                relevance_floor=args.relevance_floor,
            )
        if args.output is None:
            target = safe_relative_path(portfolio["target_id"]).as_posix()
            output = (
                ROOT
                / "agentic"
                / "state"
                / "hypotheses"
                / target
                / f"{portfolio['portfolio_id']}.json"
            )
        else:
            output = args.output
        _write(output, portfolio)
        print(
            json.dumps(
                {
                    "portfolio_id": portfolio["portfolio_id"],
                    "target_id": portfolio["target_id"],
                    "candidate_count": len(portfolio["hypotheses"]),
                    "corner_count": len(portfolio["corner_coverage"]),
                    "protected_wildcards": portfolio[
                        "protected_wildcard_ids"
                    ],
                    "parallel_seed_count": len(
                        portfolio["parallel_branch_seeds"]
                    ),
                    "output": str(output),
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, KeyError) as exc:
        print(f"high-risk portfolio rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
