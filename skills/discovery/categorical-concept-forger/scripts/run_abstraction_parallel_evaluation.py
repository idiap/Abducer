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
"""Execute the five-arm category/HoTT internal protocol calibration."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.common.abstraction_parallel_evaluation import run_abstraction_parallel_evaluation  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("envelope", type=Path)
    args = parser.parse_args()
    try:
        envelope = json.loads(args.envelope.read_text(encoding="utf-8"))
        report = run_abstraction_parallel_evaluation(
            literature_snapshot=envelope["literature_snapshot"],
            assimilation_packet=envelope["assimilation_packet"],
            source_portfolio=envelope["source_portfolio"],
            cases=envelope["cases"],
            repetitions=int(envelope.get("repetitions", 6)),
            max_workers=int(envelope.get("max_workers", 5)),
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
