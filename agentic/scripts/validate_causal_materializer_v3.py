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
"""Independently replay exact input-to-output byte materialization v3."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Mapping


CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from agentic.scripts.causal_materializer_io_v3 import (  # noqa: E402
    MAX_ARTIFACT_BYTES,
    MAX_RECEIPT_BYTES,
    decode_canonical_object,
    read_bounded_stdin,
    read_ref,
    tagged_sha256,
)


OPERATOR = {
    "operator_id": "canonical-causal-byte-materializer-v3",
    "version": "3.0.0",
    "kind": "support_probe",
}
AUTHORITY_BOUNDARY = (
    "local_exact_byte_materialization_only_not_semantic_authorship_external_"
    "independence_theory_selection_proof_or_physics_authority"
)
PARAMETER_KEYS = {
    "causal_stage_id",
    "materializer_role",
    "artifact_id",
    "artifact_digest",
    "evidence_authority_id",
    "authority_boundary",
    "semantic_authorship",
    "dependency_authority_digest",
}


def validate(protocol: Mapping[str, Any], *, workspace: Path) -> None:
    """Reject any descriptor, namespace, path, digest, or byte-copy drift."""

    if set(protocol) != {"request", "output_ref"}:
        raise ValueError("validator protocol is not the closed v3 contract")
    request = protocol.get("request")
    output_ref = protocol.get("output_ref")
    if not isinstance(request, Mapping) or not isinstance(output_ref, Mapping):
        raise ValueError("validator protocol lacks request or output reference")
    if request.get("operator") != OPERATOR:
        raise ValueError("validator received another operator")
    inputs = request.get("input_artifacts")
    outputs = request.get("declared_outputs")
    parameters = request.get("parameters")
    identity = request.get("identity")
    if not isinstance(inputs, list) or len(inputs) != 1:
        raise ValueError("validator requires one staged input")
    if not isinstance(outputs, list) or len(outputs) != 1:
        raise ValueError("validator requires one declared output")
    if not isinstance(parameters, Mapping) or set(parameters) != PARAMETER_KEYS:
        raise ValueError("validator received noncompact parameters")
    if parameters.get("authority_boundary") != AUTHORITY_BOUNDARY:
        raise ValueError("validator authority boundary drifted")
    if parameters.get("semantic_authorship") is not False:
        raise ValueError("validator cannot grant semantic authorship")
    if not isinstance(identity, Mapping):
        raise ValueError("validator request identity is absent")
    if inputs[0].get("namespace") != identity or output_ref.get("namespace") != identity:
        raise ValueError("validator evidence namespace drifted")
    if output_ref.get("path") != outputs[0]:
        raise ValueError("validator output reference differs from the declaration")
    expected_base = (
        ".canonical-causal-evidence-v3/"
        f"{identity['target_id']}/{identity['run_id']}/{identity['branch_id']}/"
        f"state-{identity['state_version']}"
    )
    expected_output = f"{expected_base}/artifacts/{request['invocation_id']}.json"
    if outputs != [expected_output]:
        raise ValueError("validator output escaped its exact namespace")
    input_bytes = read_ref(workspace, inputs[0], max_bytes=MAX_ARTIFACT_BYTES)
    output_bytes = read_ref(workspace, output_ref, max_bytes=MAX_ARTIFACT_BYTES)
    value = decode_canonical_object(input_bytes, label="validator staged input")
    if tagged_sha256(input_bytes) != parameters.get("artifact_digest"):
        raise ValueError("validator input semantic digest drifted")
    if output_bytes != input_bytes or decode_canonical_object(
        output_bytes, label="validator materialized output"
    ) != value:
        raise ValueError("materialized output bytes differ from staged input")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        protocol = read_bounded_stdin(
            max_bytes=MAX_RECEIPT_BYTES,
            label="causal materializer validator protocol",
        )
        validate(protocol, workspace=arguments.workspace)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
