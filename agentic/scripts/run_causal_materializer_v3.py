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
"""Copy one exact staged canonical input to one declared causal output.

The executable deliberately performs no semantic transformation.  It is named
and typed as a byte materializer so a successful receipt cannot be mistaken for
creative, theoretical, experimental, or physics authorship.
"""

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
    MAX_REQUEST_BYTES,
    canonical_json_bytes,
    decode_canonical_object,
    read_bounded_stdin,
    read_ref,
    tagged_sha256,
    write_create_only,
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


def _expected_base(identity: Mapping[str, Any]) -> str:
    return (
        ".canonical-causal-evidence-v3/"
        f"{identity['target_id']}/{identity['run_id']}/{identity['branch_id']}/"
        f"state-{identity['state_version']}"
    )


def materialize(request: Mapping[str, Any], *, workspace: Path) -> dict[str, Any]:
    """Validate one compact request and copy its exact staged bytes once."""

    if request.get("operator") != OPERATOR:
        raise ValueError("request names a different materializer")
    inputs = request.get("input_artifacts")
    outputs = request.get("declared_outputs")
    parameters = request.get("parameters")
    identity = request.get("identity")
    if not isinstance(inputs, list) or len(inputs) != 1:
        raise ValueError("materializer requires exactly one staged input descriptor")
    if not isinstance(outputs, list) or len(outputs) != 1:
        raise ValueError("materializer requires exactly one declared output")
    if not isinstance(parameters, Mapping) or set(parameters) != PARAMETER_KEYS:
        raise ValueError("materializer parameters are not the compact closed contract")
    if not isinstance(identity, Mapping) or inputs[0].get("namespace") != identity:
        raise ValueError("staged input namespace differs from request identity")
    if parameters.get("authority_boundary") != AUTHORITY_BOUNDARY:
        raise ValueError("materializer authority boundary drifted")
    if parameters.get("semantic_authorship") is not False:
        raise ValueError("byte materializer cannot claim semantic authorship")
    base = _expected_base(identity)
    input_path = str(inputs[0].get("path", ""))
    invocation_id = str(request.get("invocation_id", ""))
    expected_output = f"{base}/artifacts/{invocation_id}.json"
    if not input_path.startswith(f"{base}/staged-inputs/"):
        raise ValueError("staged input escaped the exact evidence namespace")
    if outputs != [expected_output] or input_path == expected_output:
        raise ValueError("materializer output escaped or aliased its input")
    data = read_ref(workspace, inputs[0], max_bytes=MAX_ARTIFACT_BYTES)
    value = decode_canonical_object(data, label="staged causal input")
    if tagged_sha256(canonical_json_bytes(value)) != parameters.get("artifact_digest"):
        raise ValueError("staged causal input differs from its semantic digest")
    write_create_only(
        workspace,
        expected_output,
        data,
        max_bytes=MAX_ARTIFACT_BYTES,
    )
    return {
        "artifacts": [{"path": expected_output}],
        "explicit_unknowns": [
            "semantic_authorship_unavailable",
            "theory_and_physics_authority_unavailable",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        request = read_bounded_stdin(
            max_bytes=MAX_REQUEST_BYTES,
            label="causal materializer request",
        )
        protocol = materialize(request, workspace=arguments.workspace)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical_json_bytes(protocol))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
