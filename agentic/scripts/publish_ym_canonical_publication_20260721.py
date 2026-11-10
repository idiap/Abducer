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
"""Plan or publish one fresh YM canonical candidate through the generic engine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for path in (ROOT, ROOT / "agentic/scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from agentic.discovery.contracts import ContractError  # noqa: E402
from ym_canonical_publication_20260721 import (  # noqa: E402
    DEFAULT_YM_PUBLICATION_ROOT,
    LEGACY_YM_ROOT,
    bind_registered_ym_publication,
    plan_ym_publication,
    publish_ym_publication,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument(
        "--publication-root", type=Path, default=DEFAULT_YM_PUBLICATION_ROOT
    )
    parser.add_argument("--legacy-root", type=Path, default=LEGACY_YM_ROOT)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--publish", action="store_true")
    parser.add_argument(
        "--bind",
        action="store_true",
        help="after full publication validation, atomically replace the registered binding last",
    )
    args = parser.parse_args()
    if args.bind and not args.publish:
        parser.error("--bind requires --publish")
    try:
        result = (
            plan_ym_publication(
                source_root=args.source_root,
                publication_root=args.publication_root,
                legacy_root=args.legacy_root,
            )
            if args.plan
            else publish_ym_publication(
                source_root=args.source_root,
                publication_root=args.publication_root,
                legacy_root=args.legacy_root,
            )
        )
        if args.bind:
            result = {**result, "registered_binding": bind_registered_ym_publication(args.publication_root)}
    except (ContractError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
