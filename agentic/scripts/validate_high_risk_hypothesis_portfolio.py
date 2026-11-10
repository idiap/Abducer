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
"""Validate structural diversity, Pareto protection, and literature rebase."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError
from agentic.discovery.hypotheses import (
    build_demo_high_risk_portfolio,
    validate_high_risk_portfolio,
)


def main(argv: list[str] | None = None) -> int:
    """Validate named portfolios or one complete in-memory self-check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)
    try:
        portfolios = (
            [json.loads(path.read_text(encoding="utf-8")) for path in args.paths]
            if args.paths
            else [build_demo_high_risk_portfolio()]
        )
        for portfolio in portfolios:
            validate_high_risk_portfolio(portfolio)
        print(
            json.dumps(
                {
                    "validated_portfolios": len(portfolios),
                    "candidate_count": sum(
                        len(portfolio["hypotheses"])
                        for portfolio in portfolios
                    ),
                    "protected_wildcard_count": sum(
                        len(portfolio["protected_wildcard_ids"])
                        for portfolio in portfolios
                    ),
                    "status": "passed",
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(f"high-risk hypothesis portfolio invalid: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
