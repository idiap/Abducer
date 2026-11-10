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
"""Dispatch typed discovery requests through executable registry bindings.

Registry entries contain argv arrays and independent validator argv arrays; shell
commands and self-attested validator payloads are intentionally unsupported.  A
receipt is written for every well-formed attempt and the command exits non-zero
when a required request did not succeed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    load_json,
    resolve_workspace_path,
    stable_identifier,
)
from agentic.discovery.receipts import (
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    ValidatorBinding,
    ValidatorDependencyProfile,
    ensure_evaluation_ready,
)


_SHELL_PROGRAMS = {"bash", "cmd", "fish", "powershell", "pwsh", "sh", "zsh"}
_TYPED_FACADE_CONTRACTS = {
    "canonical_central_conceptual_route": {
        "label": "central conceptual",
        "required_fields": {
            "route_id": "central-formal-conceptual-routes-v3",
            "production_status": "active_typed_python_api",
            "invocation_mode": (
                "typed_python_facade_with_live_store_verified_commit_and_process_wave"
            ),
            "generic_dispatch_enabled": False,
            "operator_registry_member": False,
            "python_api": "agentic.discovery:run_central_conceptual_routes",
            "structural_packet_validator": (
                "agentic.discovery:decode_central_conceptual_route_packet"
            ),
            "active_current_validator": (
                "agentic.discovery:"
                "reopen_authoritative_central_conceptual_route_packet"
            ),
            "serializable_cli_available": False,
        },
    },
    "canonical_descendant_experiment_route": {
        "label": "descendant",
        "required_fields": {
            "route_id": "canonical-descendant-experiment-v3",
            "production_status": "active_typed_python_api",
            "invocation_mode": "typed_python_facade_with_parallel_callbacks",
            "generic_dispatch_enabled": False,
            "operator_registry_member": False,
            "python_api": (
                "agentic.experiments:run_canonical_descendant_experiment_v3"
            ),
            "replay_is_producer": False,
        },
    },
}


def _argv(value: Any, *, context: str) -> tuple[str, ...]:
    """Validate an argv-only binding and exclude shell-evaluation commands."""

    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ContractError(f"{context} requires a non-empty argv array")
    if Path(value[0]).name.lower() in _SHELL_PROGRAMS or "-c" in value[1:]:
        raise ContractError(f"{context} may not use shell evaluation")
    return tuple(value)


def _dependency_paths(value: Any, *, context: str) -> tuple[str, ...]:
    """Translate typed registry paths into portable repository dependencies."""

    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ContractError(f"{context} requires non-empty dependency_paths")
    if len(value) != len(set(value)):
        raise ContractError(f"{context} dependency_paths must be unique")
    resolved: list[str] = []
    for raw in value:
        path = Path(raw)
        if path.is_absolute() or ".." in path.parts or "." in path.parts or "\\" in raw:
            raise ContractError(f"{context} dependency path is unsafe: {raw!r}")
        source = ROOT / path
        if not source.is_file():
            raise ContractError(f"{context} dependency path does not exist: {raw}")
        resolved.append(f"repo://{path.as_posix()}")
    return tuple(resolved)


def typed_facade_routes_from_registry(
    payload: Any,
) -> dict[str, dict[str, Any]]:
    """Expose typed-only routes as metadata without manufacturing executors."""

    if not isinstance(payload, dict):
        raise ContractError("operator registry must be an object")
    routes: dict[str, dict[str, Any]] = {}
    for key, contract in _TYPED_FACADE_CONTRACTS.items():
        route = payload.get(key)
        required = contract["required_fields"]
        if not isinstance(route, dict) or any(
            route.get(field) != expected
            for field, expected in required.items()
        ):
            raise ContractError(
                f"typed canonical {contract['label']} facade contract drift"
            )
        route_id = route["route_id"]
        if route_id in routes:
            raise ContractError("typed canonical facade route IDs must be unique")
        routes[route_id] = route
    return routes


def operator_bindings_from_registry(payload: Any) -> list[OperatorBinding]:
    """Translate strict JSON registry rows to executable bindings."""

    rows = payload.get("operators") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ContractError("operator registry requires an operators array")
    typed_routes = typed_facade_routes_from_registry(payload)
    for route_id in typed_routes:
        if any(
            isinstance(row, dict) and row.get("operator_id") == route_id
            for row in rows
        ):
            label = _TYPED_FACADE_CONTRACTS[
                next(
                    key
                    for key, contract in _TYPED_FACADE_CONTRACTS.items()
                    if contract["required_fields"]["route_id"] == route_id
                )
            ]["label"]
            raise ContractError(
                f"typed canonical {label} facade cannot be bound to the "
                "generic dispatcher"
            )
    bindings: list[OperatorBinding] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ContractError("operator registry rows must be objects")
        dispatch_enabled = row.get("dispatch_enabled", True)
        if type(dispatch_enabled) is not bool:
            raise ContractError("operator dispatch_enabled must be an exact boolean")
        if dispatch_enabled is False:
            if (
                row.get("production_status") != "history_only"
                or row.get("canonical_reachability") is not False
            ):
                raise ContractError(
                    "a disabled operator must be an explicit noncanonical history reader"
                )
            continue
        for field in ("operator_id", "version", "kind"):
            if not isinstance(row.get(field), str) or not row[field]:
                raise ContractError(f"operator registry row requires exact {field}")
        validators = []
        validator_rows = row.get("validators")
        if not isinstance(validator_rows, list) or not validator_rows:
            raise ContractError("operator registry row requires independent validators")
        for validator in validator_rows:
            if not isinstance(validator, dict):
                raise ContractError("validator registry row must be an object")
            if not isinstance(validator.get("validator_id"), str) or not isinstance(
                validator.get("version"), str
            ):
                raise ContractError("validator registry row requires exact ID and version")
            dependency_policy = str(validator.get("dependency_policy", ""))
            if dependency_policy == "derived_repository_closure_v2":
                dependency_paths: tuple[str, ...] = ()
                dependency_profile = ValidatorDependencyProfile.from_mapping(
                    validator.get("dependency_profile")
                )
                registry_digest = canonical_digest(payload)
            else:
                dependency_paths = _dependency_paths(
                    validator.get("dependency_paths"),
                    context=f"validator {validator['validator_id']}",
                )
                dependency_profile = None
                registry_digest = None
            validators.append(
                ValidatorBinding(
                    validator_id=validator["validator_id"],
                    version=validator["version"],
                    command=_argv(
                        validator.get("command"),
                        context=f"validator {validator['validator_id']}",
                    ),
                    dependency_paths=dependency_paths,
                    dependency_policy=dependency_policy,
                    timeout_seconds=float(validator.get("timeout_seconds", 60)),
                    dependency_profile=dependency_profile,
                    registry_digest=registry_digest,
                )
            )
        bindings.append(
            OperatorBinding(
                operator_id=row["operator_id"],
                version=row["version"],
                kind=row["kind"],
                command=_argv(
                    row.get("command"), context=f"operator {row['operator_id']}"
                ),
                validators=tuple(validators),
                timeout_seconds=float(row.get("timeout_seconds", 300)),
            )
        )
    return bindings


# Kept as a compatibility alias for existing callers and adversarial tests.
_bindings = operator_bindings_from_registry


def dispatch_request_batch(
    requests: list[dict[str, Any]],
    registry: dict[str, Any],
    *,
    workspace: Path,
    receipt_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Execute a batch and return receipts plus non-authoritative feedback candidates."""

    workspace = workspace.resolve()
    receipt_root = (
        receipt_root.resolve()
        if receipt_root.is_absolute()
        else (workspace / receipt_root).resolve()
    )
    try:
        receipt_root.relative_to(workspace)
    except ValueError as exc:
        raise ContractError("receipt root must remain inside the caller-provided workspace") from exc
    receipts = DiscoveryOperatorDispatcher(
        operator_bindings_from_registry(registry),
        workspace=workspace,
        receipt_store=ReceiptStore(receipt_root),
    ).dispatch_many(requests)
    return receipts, build_execution_manifest(registry, receipts, request_count=len(requests))


def build_execution_manifest(
    registry: dict[str, Any],
    receipts: list[dict[str, Any]],
    *,
    request_count: int | None = None,
) -> dict[str, Any]:
    """Describe actual executions and uncommitted feedback-edge candidates.

    This deliberately cannot mark an edge consumed or committed. The canonical
    cycle/reducer must turn a candidate into a separate durable feedback edge.
    """

    by_operator = {row["operator_id"]: row for row in registry["operators"]}
    executions: list[dict[str, Any]] = []
    feedback_candidates: list[dict[str, Any]] = []
    for receipt in receipts:
        operator_id = receipt["operator"]["operator_id"]
        executions.append(
            {
                "request_id": receipt["request_id"],
                "receipt_id": receipt["receipt_id"],
                "operator_id": operator_id,
                "operator_version": receipt["operator"]["version"],
                "status": receipt["status"],
                "input_digest": receipt["input_digest"],
                "output_artifacts": receipt["output_artifacts"],
                "validator_receipts": receipt["validator_receipts"],
            }
        )
        if receipt["status"] == "succeeded":
            feedback_candidates.append(
                {
                    "producer_receipt_id": receipt["receipt_id"],
                    "operator_id": operator_id,
                    "candidate_consumer_ids": list(
                        by_operator.get(operator_id, {}).get("required_consumers", [])
                    ),
                    "consumed": False,
                    "consumer_event_id": None,
                    "state_edge_committed": False,
                    "authority_boundary": (
                        "Candidate only: the canonical reducer/cycle must record actual "
                        "consumption and a committed state edge."
                    ),
                }
            )
    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_id": stable_identifier(
            "operator-execution-manifest",
            [receipt["receipt_id"] for receipt in receipts],
        ),
        "registry_id": registry.get("registry_id"),
        "registry_digest": canonical_digest(registry),
        "request_count": len(receipts) if request_count is None else request_count,
        "receipt_count": len(receipts),
        "executions": executions,
        "feedback_edge_candidates": feedback_candidates,
        "feedback_committed": False,
    }
    manifest["manifest_digest"] = canonical_digest(manifest)
    return manifest


def _write_immutable(path: Path, payload: dict[str, Any]) -> None:
    """Create one immutable canonical manifest, accepting identical replay."""

    encoded = canonical_json(payload) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == encoded:
            return
        raise ContractError(f"execution manifest conflict at {path}")
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def main() -> int:
    """Run request batches without suppressing valid siblings after a failure."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, default=ROOT)
    parser.add_argument("--receipts", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        help="Optional workspace-relative immutable execution/feedback-candidate manifest.",
    )
    args = parser.parse_args()
    request_payload = load_json(args.requests)
    requests = request_payload.get("requests") if isinstance(request_payload, dict) else request_payload
    if not isinstance(requests, list):
        raise ContractError("request file must be an array or contain a requests array")
    registry_payload = load_json(args.registry)
    if not isinstance(registry_payload, dict):
        raise ContractError("operator registry must be an object")
    workspace = args.workspace.resolve()
    receipts, manifest = dispatch_request_batch(
        requests,
        registry_payload,
        workspace=workspace,
        receipt_root=args.receipts,
    )
    manifest_path = None
    if args.manifest:
        manifest_path = resolve_workspace_path(workspace, args.manifest)
        _write_immutable(manifest_path, manifest)
    ready = True
    try:
        ensure_evaluation_ready(requests, receipts, workspace=workspace)
    except ContractError:
        ready = False
    print(
        json.dumps(
            {
                "request_count": len(requests),
                "receipt_count": len(receipts),
                "statuses": {status: sum(r["status"] == status for r in receipts) for status in {
                    "succeeded", "failed", "timed_out", "skipped"
                }},
                "evaluation_ready": ready,
                "manifest": (
                    manifest_path.relative_to(workspace).as_posix()
                    if manifest_path is not None
                    else None
                ),
                "feedback_committed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if ready else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
