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
"""Validate the current YM publication pointer or its registered immutable binding."""

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
from canonical_publication_engine import validate_profile_current  # noqa: E402
from ym_canonical_publication_20260721 import (  # noqa: E402
    DEFAULT_YM_PUBLICATION_ROOT,
    build_ym_profile,
    resolve_registered_ym_publication,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publication-root", type=Path, default=DEFAULT_YM_PUBLICATION_ROOT
    )
    parser.add_argument("--registered-binding", action="store_true")
    args = parser.parse_args()
    try:
        result = (
            resolve_registered_ym_publication()
            if args.registered_binding
            else validate_profile_current(
                publication_root=args.publication_root,
                profile=build_ym_profile(),
                authority_repository_root=ROOT,
            )
        )
    except (ContractError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
