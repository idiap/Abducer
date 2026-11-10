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
"""Reopen one registered N-to-N+8 descendant experiment chain read-only.

The typed Python facade owns production because world producers are live,
bounded callbacks rather than serializable command text.  This command is the
registry-facing independent replay boundary: it accepts only store locators,
reopens the exact theory root, reconstructs the descendant runtime, and emits
a compact active-current summary.  It never executes an experiment or writes
canonical state.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from agentic.discovery.contracts import ContractError, canonical_json, validate_identifier
from agentic.experiments.world_v3_content_graph_runtime import (
    WorldV3ContentGraphRuntime,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


MAX_REQUEST_BYTES = 64 * 1024


def _relative_path(raw: Any, label: str) -> str:
    if not isinstance(raw, str) or not raw:
        raise ContractError(f"{label} must be a non-empty relative path")
    path = PurePosixPath(raw)
    if path.is_absolute() or "." in path.parts or ".." in path.parts or "\\" in raw:
        raise ContractError(f"{label} is not a canonical relative path")
    return path.as_posix()


def validate_request(request: dict[str, Any], *, workspace: Path) -> dict[str, Any]:
    """Reopen exact active bytes and return authority-bounded chronology."""

    required = {
        "store_root",
        "target_id",
        "run_id",
        "theory_generation",
        "theory_graph_artifact_path",
        "branch_id",
    }
    if set(request) != required:
        raise ContractError("descendant replay request has an open or incomplete shape")
    target_id = validate_identifier(request["target_id"], "target_id")
    run_id = validate_identifier(request["run_id"], "run_id")
    branch_id = validate_identifier(request["branch_id"], "branch_id")
    generation = request["theory_generation"]
    if type(generation) is not int or generation < 1:
        raise ContractError("theory_generation must be a positive integer")
    store_relative = _relative_path(request["store_root"], "store_root")
    graph_path = _relative_path(
        request["theory_graph_artifact_path"],
        "theory_graph_artifact_path",
    )
    root = (workspace / store_relative).resolve(strict=True)
    try:
        root.relative_to(workspace)
    except ValueError as exc:
        raise ContractError("descendant store root escaped the workspace") from exc
    store = DiscoveryTransactionStore(root, target_id=target_id, run_id=run_id)
    runtime = WorldV3ContentGraphRuntime.recover_from_store(
        store=store,
        theory_generation=generation,
        theory_graph_artifact_path=graph_path,
        branch_id=branch_id,
    )
    verified = runtime.require_active_current_descendant_closure()
    return {
        "schema_version": "1.0.0",
        "validation_kind": "canonical_world_v3_descendant_active_current",
        "target_id": verified.support_prefix.target_id,
        "run_id": verified.support_prefix.run_id,
        "theory_generation": generation,
        "anchor_generation": generation + 1,
        "world_generations": list(verified.support_prefix.world_generations),
        "aggregation_generation": generation + 7,
        "reflection_generation": verified.reflection_generation,
        "reflection_root_ref": verified.reflection_root_ref,
        "result_effect": verified.result_effect,
        "current_cycle_theory_mutation_authorized": False,
        "automatic_theory_selection_authorized": False,
        "proof_authorized": False,
        "physics_authority": False,
        "authority_boundary": (
            "active_current_local_descendant_chronology_only_no_truth_proof_"
            "experiment_value_theory_selection_or_physics_authority"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    workspace = args.workspace.resolve(strict=True)
    raw = sys.stdin.buffer.read(MAX_REQUEST_BYTES + 1)
    try:
        if not raw or len(raw) > MAX_REQUEST_BYTES:
            raise ContractError("descendant replay request is absent or too large")
        request = json.loads(raw.decode("utf-8"))
        if not isinstance(request, dict) or canonical_json(request) != raw:
            raise ContractError("descendant replay request is not canonical JSON")
        result = validate_request(request, workspace=workspace)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
