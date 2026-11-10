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
"""Run or reopen the constructive four-route Category/HoTT production bundle.

``run`` consumes an already sealed request.  It does not invent the task,
literature projection, creativity packet, frozen ancestor, or domain rule:
those inputs and the separate rule precommit must validate before any worker
starts.  ``validate`` reexecutes every registered route and reopens the exact
request, terminal receipts, barrier, and packet bytes.  Both commands emit the
validated packet to stdout; neither publishes a theory or authorizes a physics
claim, experiment-led choice, theorem, continuum result, or Yang--Mills result.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import canonical_json, load_json  # noqa: E402
from agentic.discovery.formal_lens_production import (  # noqa: E402
    FormalLensProductionError,
    run_formal_lens_production,
    validate_formal_lens_production_bundle,
)
from agentic.discovery.formal_lens_registry import (  # noqa: E402
    REGISTRY_PATH,
    FormalLensRegistryError,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Execute four concurrent routes and persist their bundle.")
    run.add_argument("--request", type=Path, required=True, help="Sealed formal-lens request JSON.")
    run.add_argument("--output-root", type=Path, required=True, help="Parent for the request-ID bundle.")
    run.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    validate = commands.add_parser("validate", help="Reopen and replay one completed bundle.")
    validate.add_argument("--bundle", type=Path, required=True)
    validate.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "run":
            request = load_json(args.request)
            if not isinstance(request, dict):
                raise FormalLensProductionError("formal-lens request root must be an object")
            packet = run_formal_lens_production(
                request,
                args.output_root,
                registry_path=args.registry,
            )
        else:
            packet = validate_formal_lens_production_bundle(
                args.bundle,
                registry_path=args.registry,
            )
        sys.stdout.buffer.write(canonical_json(packet) + b"\n")
    except (FormalLensProductionError, FormalLensRegistryError, OSError, ValueError) as exc:
        print(f"formal-lens production rejected: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
