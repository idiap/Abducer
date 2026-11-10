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
"""Run a typed theory-first reflective conceptual discovery cycle."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.workflow import DiscoveryWorkflowError, build_reflective_discovery_packet  # noqa: E402


def _write_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(raw_temp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(raw_temp):
            os.unlink(raw_temp)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", help="Typed discovery request JSON. Reads stdin when omitted.")
    parser.add_argument("--output", help="Write packet atomically; stdout when omitted.")
    parser.add_argument("--stage", choices=["full", "reflect"], default="full", help="Registry-compatible stage selector; both validate the complete packet contract.")
    args = parser.parse_args()
    try:
        raw = Path(args.request).read_text(encoding="utf-8") if args.request else sys.stdin.read()
        request = json.loads(raw)
        packet = build_reflective_discovery_packet(request)
    except (OSError, json.JSONDecodeError, DiscoveryWorkflowError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.output:
        _write_atomic(Path(args.output), packet)
    else:
        print(json.dumps(packet, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
