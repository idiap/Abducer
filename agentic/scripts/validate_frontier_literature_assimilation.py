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
"""Validate claim-level literature assimilation and scheduling causality."""

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
    assimilate_literature,
    build_demo_literature_snapshot,
    validate_assimilation,
)


def _self_check() -> tuple[dict, dict]:
    """Build a causal spawn plus justified-no-change local-only fixture."""

    snapshot = build_demo_literature_snapshot()
    mappings = []
    for index, source in enumerate(snapshot["sources"]):
        mappings.append(
            {
                "source_id": source["source_id"],
                "theory_object_ids": [f"demo-concept-{index}"],
                "object_kinds": ["concept"],
                "relation": "reframes" if index == 0 else "leaves_open",
                "conceptual_change": (
                    "Spawn a relation-first conceptual branch."
                    if index == 0
                    else "No change: the source is confined to a disjoint regime."
                ),
                "event_type": "spawn" if index == 0 else "justified_no_change",
                "coverage_limits": list(snapshot["coverage_limits"]),
                "confidence": "medium",
            }
        )
    packet = assimilate_literature(
        snapshot,
        theory_state_digest=snapshot["theory_state_digest"],
        theory_mappings=mappings,
        hypotheses=[
            {
                "hypothesis_id": "demo-hypothesis",
                "genealogy": ["pre-search-intuition"],
                "literature_relation": "partly_anticipated",
                "source_ids": [snapshot["sources"][0]["source_id"]],
                "routing_effect": "sharpen",
            }
        ],
    )
    return packet, snapshot


def main(argv: list[str] | None = None) -> int:
    """Validate a packet and its exact snapshot, or run a complete self-check."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", nargs="?", type=Path)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.packet is None:
            packet, snapshot = _self_check()
        else:
            if args.snapshot is None:
                raise ContractError("--snapshot is required with a packet path")
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        validate_assimilation(packet, snapshot=snapshot)
        print(
            json.dumps(
                {
                    "packet_id": packet["packet_id"],
                    "mapping_count": len(packet["theory_mappings"]),
                    "hypothesis_rebase_status": packet[
                        "hypothesis_rebase_status"
                    ],
                    "status": "passed",
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(f"frontier literature assimilation invalid: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
