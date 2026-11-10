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
"""Validate one categorical concept-forge packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.common.abstraction_discovery_validation import (  # noqa: E402
    AbstractionValidationError,
    validate_forge_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("evaluation", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.packet.read_text(encoding="utf-8"))
        evaluation = json.loads(args.evaluation.read_text(encoding="utf-8"))
        result = validate_forge_packet(payload, expected_lens="categorical", parallel_evaluation=evaluation)
    except (OSError, json.JSONDecodeError, AbstractionValidationError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
