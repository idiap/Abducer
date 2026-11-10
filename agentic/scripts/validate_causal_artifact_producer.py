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
"""Independently validate one canonical local causal-artifact invocation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    validate_digest,
    validate_identifier,
    verify_artifact_descriptor,
)


OPERATOR = {
    "operator_id": "canonical-causal-artifact-producer",
    "version": "1.0.0",
    "kind": "support_probe",
}
AUTHORITY_BOUNDARY = (
    "local dispatcher and byte validator evidence only; no external "
    "independence, physical-target, proof, theory-selection, or theory-mutation authority"
)


def _read_protocol() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ContractError(f"stdin is not causal validator protocol JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("causal validator protocol must be an object")
    return value


def validate(protocol: Mapping[str, Any], *, workspace: Path) -> None:
    request = protocol.get("request")
    artifacts = protocol.get("artifacts")
    if not isinstance(request, Mapping):
        raise ContractError("causal validator protocol lacks its producer request")
    if request.get("operator") != OPERATOR:
        raise ContractError("causal validator received another operator")
    if request.get("input_artifacts") != []:
        raise ContractError("causal producer request gained ambient input artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        raise ContractError("causal validator requires exactly one output artifact")
    declared = request.get("declared_outputs")
    if not isinstance(declared, list) or len(declared) != 1:
        raise ContractError("causal producer request must declare exactly one output")
    descriptor = artifacts[0]
    if not isinstance(descriptor, Mapping) or descriptor.get("path") != declared[0]:
        raise ContractError("causal validator output differs from the declared path")
    namespace = Namespace.from_mapping(request.get("identity", {}))
    invocation_id = validate_identifier(str(request.get("invocation_id", "")), "invocation_id")
    expected_path = (
        Path(".canonical-causal-evidence")
        / namespace.target_id
        / namespace.run_id
        / namespace.branch_id
        / f"state-{namespace.state_version}"
        / "artifacts"
        / f"{invocation_id}.json"
    ).as_posix()
    if declared[0] != expected_path:
        raise ContractError("causal producer output escaped its exact namespace")
    output_path = verify_artifact_descriptor(descriptor, workspace, namespace)

    parameters = request.get("parameters")
    if not isinstance(parameters, Mapping):
        raise ContractError("causal producer parameters are absent")
    required = {
        "causal_stage_id",
        "producer_role",
        "artifact_id",
        "artifact_digest",
        "artifact_value",
        "evidence_authority_id",
        "authority_boundary",
    }
    if not required.issubset(parameters):
        raise ContractError("causal producer parameters omit required identity fields")
    for field in (
        "causal_stage_id",
        "producer_role",
        "artifact_id",
        "evidence_authority_id",
    ):
        validate_identifier(str(parameters[field]), field)
    validate_digest(str(parameters["artifact_digest"]))
    artifact = parameters["artifact_value"]
    if not isinstance(artifact, Mapping):
        raise ContractError("causal producer artifact must be one JSON object")
    if parameters["artifact_digest"] != canonical_digest(artifact):
        raise ContractError("causal producer artifact digest is invalid")
    if parameters["authority_boundary"] != AUTHORITY_BOUNDARY:
        raise ContractError("causal producer overstated its local authority")
    if output_path.read_bytes() != canonical_json(dict(artifact)):
        raise ContractError("causal producer output bytes differ from the requested artifact")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        validate(_read_protocol(), workspace=arguments.workspace.resolve())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
