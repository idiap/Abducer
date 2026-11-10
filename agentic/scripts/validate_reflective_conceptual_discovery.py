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
"""Validate reflective discovery packets and their theory-first invariants."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import canonical_digest, validate_payload  # noqa: E402
from agentic.discovery.reflection import validate_packet_invariants  # noqa: E402


def validate_packet(packet: dict) -> None:
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    claimed = packet["packet_digest"]
    unsigned = dict(packet)
    unsigned.pop("packet_digest", None)
    if claimed != canonical_digest(unsigned):
        raise ValueError("packet digest mismatch")
    validate_packet_invariants(packet)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packets", nargs="*", help="Packet JSON paths. With none, schema and generative case contracts are checked.")
    args = parser.parse_args()
    paths = [Path(item) for item in args.packets]
    try:
        if not paths:
            validate_payload  # Ensure import and schema dependency load.
            from agentic.discovery.contracts import validate_schema_file
            validate_schema_file("reflective_conceptual_discovery_packet.schema.json")
            case_path = ROOT / "tests/generative/reflective_conceptual_discovery_cases.jsonl"
            if not case_path.is_file() or not case_path.read_text(encoding="utf-8").strip():
                raise ValueError("missing reflective conceptual discovery generative cases")
            print("validated reflective discovery schema and generative case contract; no live packet supplied")
            return 0
        for path in paths:
            validate_packet(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(paths)} reflective conceptual discovery packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
