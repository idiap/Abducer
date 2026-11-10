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
"""Validate immutable dynamic-experiment receipts against their frozen specs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    load_json,
    resolve_workspace_path,
    validate_schema_file,
)
from agentic.experiments import receipt_staleness, validate_experiment_receipt  # noqa: E402


def _exact_role_path(
    roles: dict[str, object], role: str, workspace: Path
) -> Path:
    """Resolve one canonical role without inferring authority from directory shape."""

    raw = roles.get(role)
    values = raw if isinstance(raw, list) else [raw]
    if len(values) != 1 or not isinstance(values[0], str):
        raise ContractError(f"canonical cycle request must bind exactly one {role}")
    return resolve_workspace_path(workspace, values[0], must_exist=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipts", nargs="*", type=Path)
    parser.add_argument(
        "--cycle-request",
        type=Path,
        help="Canonical request whose experiment_receipt role must be validated.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Exact operator workspace named by --cycle-request.",
    )
    args = parser.parse_args()
    for schema in (
        "dynamic_probe_triage.schema.json",
        "dynamic_experiment_spec_v3.schema.json",
        "dynamic_experiment_receipt_v3.schema.json",
    ):
        validate_schema_file(schema)
    if (args.cycle_request is None) != (args.workspace is None):
        raise ContractError("--cycle-request and --workspace must be supplied together")
    paths = list(args.receipts)
    canonical_pairs: list[tuple[Path, Path]] = []
    if args.cycle_request is not None:
        if paths:
            raise ContractError(
                "positional receipts cannot be mixed with canonical request validation"
            )
        request = load_json(args.cycle_request)
        if not isinstance(request, dict):
            raise ContractError("canonical cycle request must be an object")
        roles = request.get("artifact_roles")
        if not isinstance(roles, dict):
            raise ContractError("canonical cycle request has no artifact_roles")
        workspace = args.workspace.resolve()
        role_spec_path = _exact_role_path(roles, "experiment_spec", workspace)
        operator_receipt_path = _exact_role_path(
            roles, "experiment_receipt", workspace
        )
        role_spec = load_json(role_spec_path)
        operator_receipt = load_json(operator_receipt_path)
        if not isinstance(role_spec, dict) or not isinstance(operator_receipt, dict):
            raise ContractError("canonical experiment spec/receipt roles must be objects")
        validate_experiment_receipt(
            operator_receipt,
            role_spec,
            work_directory=operator_receipt_path.parent,
        )
        experiment_id = operator_receipt.get("experiment_id")
        if not isinstance(experiment_id, str) or not experiment_id:
            raise ContractError("canonical experiment output has no experiment_id")
        immutable_receipt_paths = sorted(
            path
            for path in workspace.rglob(f"experiments/{experiment_id}/receipt.json")
            if (path.parent / "spec.json").is_file()
        )
        if len(immutable_receipt_paths) != 1:
            raise ContractError(
                "canonical experiment has no unique immutable runtime receipt/spec pair"
            )
        immutable_path = immutable_receipt_paths[0]
        immutable_spec_path = immutable_path.parent / "spec.json"
        immutable_spec = load_json(immutable_spec_path)
        immutable_receipt = load_json(immutable_path)
        if (
            canonical_digest(role_spec) != canonical_digest(immutable_spec)
            or canonical_digest(operator_receipt) != canonical_digest(immutable_receipt)
        ):
            raise ContractError(
                "canonical experiment role bytes differ from immutable runtime spec/receipt"
            )
        canonical_pairs.append((immutable_path, immutable_spec_path))
    elif not paths:
        paths = sorted((ROOT / "agentic" / "runs").glob("**/experiments/*/receipt.json"))
    pairs = canonical_pairs or [
        (receipt_path, receipt_path.parent / "spec.json") for receipt_path in paths
    ]
    for receipt_path, spec_path in pairs:
        if not spec_path.is_file():
            raise ContractError(f"missing frozen experiment spec beside {receipt_path}")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        validate_experiment_receipt(receipt, spec, work_directory=receipt_path.parent)
        stale = receipt_staleness(receipt, spec)
        if stale["stale"]:
            raise ContractError(f"stale receipt {receipt_path}: {stale['reasons']}")
    print(f"validated {len(pairs)} dynamic experiment receipt(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
