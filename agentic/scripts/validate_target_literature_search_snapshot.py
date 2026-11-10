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
"""Validate immutable target-scoped search snapshots and semantic provenance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import ContractError
from agentic.discovery.literature import (
    build_demo_literature_snapshot,
    validate_snapshot,
)


def main(argv: list[str] | None = None) -> int:
    """Validate every named snapshot or an in-memory local-only self-check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)
    try:
        snapshots = (
            [json.loads(path.read_text(encoding="utf-8")) for path in args.paths]
            if args.paths
            else [build_demo_literature_snapshot()]
        )
        for snapshot in snapshots:
            validate_snapshot(snapshot)
        print(
            json.dumps(
                {
                    "validated_snapshots": len(snapshots),
                    "targets": sorted(
                        {snapshot["target_id"] for snapshot in snapshots}
                    ),
                    "status": "passed",
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(f"target literature snapshot invalid: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
