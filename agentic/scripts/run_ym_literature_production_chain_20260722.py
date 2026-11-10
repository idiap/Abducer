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
"""Execute or replay-validate the sealed 2026-07-22 YM theory chain.

This entry point is deliberately publication-disabled.  It reuses the
production-chain implementation; it does not renew the literature capture,
perform a live search, commission a world, or promote any truth, novelty,
creativity, physics-value, or theorem claim.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_json,
    load_json,
)
from agentic.evals.ym_representational_dynamics_20260721.literature_production_chain import (  # noqa: E402
    CODE_ROOT,
    DEFAULT_AUTHORITY_ROOT,
    build_publication_disabled_literature_production_chain,
    validate_literature_production_chain_manifest,
)


def _write_exclusive(path: Path, payload: bytes) -> None:
    """Create one manifest without following links or replacing prior evidence."""

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--authority-root",
        type=Path,
        default=DEFAULT_AUTHORITY_ROOT,
        help="Directory containing the exact checked-in capture bundle.",
    )
    parser.add_argument(
        "--code-root",
        type=Path,
        default=CODE_ROOT,
        help="Repository root whose code and dependency bytes are bound.",
    )
    parser.add_argument(
        "--execution-started-at",
        help="Injected RFC3339 replay time; cannot renew source freshness.",
    )
    parser.add_argument(
        "--validate-manifest",
        type=Path,
        help="Replay-validate an existing manifest instead of building one.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Exclusively create this file; omit to emit canonical JSON to stdout.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.validate_manifest is not None and args.execution_started_at is not None:
        _parser().error(
            "--execution-started-at is a build input and cannot accompany "
            "--validate-manifest"
        )
    try:
        if args.validate_manifest is None:
            manifest = build_publication_disabled_literature_production_chain(
                authority_root=args.authority_root,
                code_root=args.code_root,
                execution_started_at=args.execution_started_at,
            )
        else:
            candidate = load_json(args.validate_manifest)
            if not isinstance(candidate, dict):
                raise ContractError("literature production manifest must be an object")
            manifest = validate_literature_production_chain_manifest(
                candidate,
                authority_root=args.authority_root,
                code_root=args.code_root,
            )
        encoded = canonical_json(manifest) + b"\n"
        if args.output is None:
            sys.stdout.buffer.write(encoded)
        else:
            _write_exclusive(args.output, encoded)
    except (ContractError, OSError, ValueError) as exc:
        print(f"literature production chain rejected: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
