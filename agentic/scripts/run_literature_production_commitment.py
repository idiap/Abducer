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
"""Build or reopen a portable pre-commission literature input receipt.

The command persists no runtime root in its output and has no publication or
world-commissioning mode.  ``build`` emits the strict descriptor/receipt;
``reopen`` validates the receipt against exact manifest bytes and emits only
the bounded consumer projection.
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
from agentic.discovery.literature_production_commitment import (  # noqa: E402
    build_portable_literature_production_input_receipt,
    reopen_portable_literature_production_input,
)


def _write_exclusive(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _add_output(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output",
        type=Path,
        help="Exclusively create this file; omit to emit canonical JSON to stdout.",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    build = commands.add_parser(
        "build", help="Build a receipt from one root-relative manifest."
    )
    build.add_argument("--root", type=Path, required=True)
    build.add_argument(
        "--manifest-path",
        required=True,
        help="Canonical immutable POSIX path relative to --root.",
    )
    _add_output(build)

    reopen = commands.add_parser(
        "reopen", help="Reopen exact bytes and emit the bounded projection."
    )
    reopen.add_argument("--root", type=Path, required=True)
    reopen.add_argument("--receipt", type=Path, required=True)
    _add_output(reopen)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "build":
            output = build_portable_literature_production_input_receipt(
                args.root,
                args.manifest_path,
            )
        else:
            receipt = load_json(args.receipt)
            if not isinstance(receipt, dict):
                raise ContractError("literature input receipt must be one object")
            output = reopen_portable_literature_production_input(
                args.root,
                receipt,
            )
        data = canonical_json(output) + b"\n"
        if args.output is None:
            sys.stdout.buffer.write(data)
        else:
            _write_exclusive(args.output, data)
    except (ContractError, OSError, ValueError) as exc:
        print(f"literature production commitment rejected: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
