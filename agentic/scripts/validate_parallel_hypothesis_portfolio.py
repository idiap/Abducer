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
"""Validate isolated parallel execution, partial success, dissent, and CAS."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
    validate_parallel_portfolio,
)


def _self_check() -> dict:
    """Run a mixed success/failure portfolio whose valid siblings must survive."""

    portfolio = build_demo_high_risk_portfolio()
    manifest = build_parallel_manifest(
        portfolio,
        base_theory_state_version=2,
        resource_budget={
            "wall_seconds": 30,
            "max_workers": 4,
            "cost_units": 20,
            "storage_bytes": 1_000_000,
            "matched_budget_baseline_corner_coverage": 1,
        },
    )
    failed_id = manifest["branch_requests"][0]["branch_id"]
    dissent_id = manifest["branch_requests"][-1]["branch_id"]

    def worker(request: dict) -> dict:
        if request["branch_id"] == failed_id:
            raise RuntimeError("deliberate partial-failure self-check")
        return {
            "theory_delta": {
                "delta_class": "perspective_shift",
                "mechanism_key": request["mechanism_key"],
            },
            "claims": [
                {
                    "proposition": "A shared explanatory carrier is required.",
                    "stance": (
                        "oppose"
                        if request["branch_id"] == dissent_id
                        else "support"
                    ),
                }
            ],
            "genealogy": [request["hypothesis_id"]],
            "conceptual_learning": True,
            "is_dissent": request["branch_id"] == dissent_id,
        }

    return run_parallel_hypothesis_portfolio(
        manifest, worker, cas_merge=lambda expected, proposal: expected + 1
    )


def main(argv: list[str] | None = None) -> int:
    """Validate named run packets or execute the complete self-check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)
    try:
        packets = (
            [json.loads(path.read_text(encoding="utf-8")) for path in args.paths]
            if args.paths
            else [_self_check()]
        )
        for packet in packets:
            validate_parallel_portfolio(packet)
        print(
            json.dumps(
                {
                    "validated_portfolios": len(packets),
                    "attempt_count": sum(
                        len(packet["attempt_receipts"]) for packet in packets
                    ),
                    "preserved_success_count": sum(
                        len(
                            packet["partial_failure_ledger"][
                                "preserved_branch_ids"
                            ]
                        )
                        for packet in packets
                    ),
                    "status": "passed",
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(f"parallel hypothesis portfolio invalid: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
