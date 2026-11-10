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
"""Plan or execute one atomic canonical-discovery publication."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "agentic/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.contracts import ContractError  # noqa: E402
from canonical_discovery_publication import (  # noqa: E402
    DEFAULT_PUBLICATION_ROOT,
    plan_publication,
    publish_current,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True, type=Path)
    parser.add_argument("--cycle-request", required=True, type=Path)
    parser.add_argument("--state-root", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--receipt-root", required=True, type=Path)
    parser.add_argument("--target-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--publication-root", type=Path, default=DEFAULT_PUBLICATION_ROOT)
    parser.add_argument("--legacy-bundle", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    kwargs = {
        "cycle_path": args.cycle,
        "cycle_request_path": args.cycle_request,
        "state_root": args.state_root,
        "workspace": args.workspace,
        "receipt_root": args.receipt_root,
        "target_id": args.target_id,
        "run_id": args.run_id,
        "publication_root": args.publication_root,
        "legacy_bundle": args.legacy_bundle,
    }
    try:
        result = plan_publication(**kwargs) if args.plan else publish_current(**kwargs)
    except (ContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
