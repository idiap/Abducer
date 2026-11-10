# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compact causal byte-materialization evidence, additive to historical v2.

V2 embeds a complete artifact value and several base64 copies in every producer
binding.  This v3 module instead stages canonical input bytes once and carries
only exact bounded file references through the request, attempts, output,
history, clock, and final binding.  Its subprocess copies bytes; it does not
author, interpret, select, or validate scientific content.

The module is intentionally not wired into the canonical world route yet.  That
cutover must be a separate migration after v3 replay and performance evidence is
green, leaving all historical v2 readers and committed artifacts unchanged.
"""

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    stable_identifier,
    utc_now,
    validate_identifier,
    validate_payload,
)
from agentic.discovery.dependency_authority import (
    build_dependency_authority,
    validate_dependency_authority,
)
from agentic.scripts.causal_materializer_io_v3 import (
    CausalMaterializerIOError,
    MAX_ARTIFACT_BYTES,
    MAX_ATTEMPTS,
    MAX_BINDING_BYTES,
    MAX_PATH_BYTES,
    MAX_RECEIPT_BYTES,
    MAX_REQUEST_BYTES,
    SUBPROCESS_TIMEOUT_SECONDS,
    canonical_json_bytes,
    decode_canonical_object,
    evidence_ref,
    read_ref,
    safe_read,
    tagged_sha256,
    write_create_only,
)


MATERIALIZER_OPERATOR_ID = "canonical-causal-byte-materializer-v3"
MATERIALIZER_OPERATOR_VERSION = "3.0.0"
MATERIALIZER_OPERATOR_KIND = "support_probe"
MATERIALIZER_VALIDATOR_ID = "canonical-causal-byte-materializer-validator-v3"
MATERIALIZER_VALIDATOR_VERSION = "3.0.0"
LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY = (
    "local_exact_byte_materialization_only_not_semantic_authorship_external_"
    "independence_theory_selection_proof_or_physics_authority"
)
DEPENDENCY_AUTHORITY_BOUNDARY = (
    "exact_local_dependency_environment_and_executable_identity_only_not_external_"
    "truth_theorem_or_physics_authority"
)
COMPACT_REF_SCHEMA = "dynamic_experiment_compact_evidence_ref_v3.schema.json"
RECEIPT_SCHEMA = "dynamic_experiment_causal_materializer_receipt_v3.schema.json"
CLOCK_SCHEMA = "dynamic_experiment_causal_materializer_clock_v3.schema.json"
BINDING_SCHEMA = "dynamic_experiment_causal_materializer_binding_v3.schema.json"
REQUEST_SCHEMA = "discovery_operator_request.schema.json"
EVIDENCE_ROOT = Path(".canonical-causal-evidence-v3")
OPERATOR = {
    "operator_id": MATERIALIZER_OPERATOR_ID,
    "version": MATERIALIZER_OPERATOR_VERSION,
    "kind": MATERIALIZER_OPERATOR_KIND,
}
CEILINGS = {
    "max_artifact_bytes": MAX_ARTIFACT_BYTES,
    "max_request_bytes": MAX_REQUEST_BYTES,
    "max_receipt_bytes": MAX_RECEIPT_BYTES,
    "max_binding_bytes": MAX_BINDING_BYTES,
    "max_path_bytes": MAX_PATH_BYTES,
    "max_attempts": MAX_ATTEMPTS,
    "subprocess_timeout_seconds": SUBPROCESS_TIMEOUT_SECONDS,
}
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
_DEPENDENCY_ENTRIES = {
    "agentic/scripts/run_causal_materializer_v3.py": ("materializer_executable",),
    "agentic/scripts/validate_causal_materializer_v3.py": ("validator_executable",),
}
_DEPENDENCY_SEMANTICS = {
    "agentic/experiments/causal_producer_runtime_v3.py": ("orchestration_source",),
    "agentic/spec/dynamic_experiment_causal_materializer_binding_v3.schema.json": ("binding_contract",),
    "agentic/spec/dynamic_experiment_causal_materializer_receipt_v3.schema.json": ("receipt_contract",),
    "agentic/spec/dynamic_experiment_causal_materializer_clock_v3.schema.json": ("clock_contract",),
    "agentic/spec/dynamic_experiment_compact_evidence_ref_v3.schema.json": ("file_reference_contract",),
    "agentic/spec/discovery_operator_request.schema.json": ("request_contract",),
}


@dataclass(frozen=True, slots=True)
class SealedCausalMaterializationV3:
    """One compact binding plus its separately reopenable protocol records."""

    binding: Mapping[str, Any]
    binding_path: Path
    request: Mapping[str, Any]
    request_path: Path
    successful_receipt: Mapping[str, Any]
    receipt_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class VerifiedCausalMaterializationSnapshotV3:
    """Immutable, read-once capture of one locally sealed materialization.

    Canonical bytes are the stored state. Decoded properties create a fresh
    object on every access, so a graph adapter cannot mutate verified evidence
    or accidentally depend on source files after the snapshot. The terminal
    successful receipt aliases the final attempt bytes; it is never captured or
    stored for a second time.
    """

    snapshot_digest: str
    binding_bytes: bytes
    staged_input_bytes: bytes
    request_bytes: bytes
    attempt_receipt_bytes: tuple[bytes, ...]
    output_bytes: bytes
    history_bytes: bytes
    clock_bytes: bytes
    captured_ref_paths: tuple[str, ...]

    @staticmethod
    def _value(data: bytes, *, label: str) -> dict[str, Any]:
        return decode_canonical_object(data, label=label)

    @property
    def binding(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the verified binding."""

        return self._value(self.binding_bytes, label="snapshot materializer binding")

    @property
    def staged_input(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the staged artifact."""

        return self._value(self.staged_input_bytes, label="snapshot staged input")

    @property
    def request(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the durable request."""

        return self._value(self.request_bytes, label="snapshot materializer request")

    @property
    def attempt_receipts(self) -> tuple[dict[str, Any], ...]:
        """Return defensive decoded copies in contiguous attempt order."""

        return tuple(
            self._value(data, label=f"snapshot materializer receipt {index}")
            for index, data in enumerate(self.attempt_receipt_bytes, start=1)
        )

    @property
    def successful_receipt_bytes(self) -> bytes:
        """Return the final attempt bytes without duplicating their capture."""

        return self.attempt_receipt_bytes[-1]

    @property
    def successful_receipt(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the terminal success receipt."""

        return self._value(
            self.successful_receipt_bytes,
            label="snapshot successful materializer receipt",
        )

    @property
    def output(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the materialized output."""

        return self._value(self.output_bytes, label="snapshot materialized output")

    @property
    def history(self) -> dict[str, Any]:
        """Return a defensive decoded copy of immutable output history."""

        return self._value(self.history_bytes, label="snapshot materializer history")

    @property
    def clock(self) -> dict[str, Any]:
        """Return a defensive decoded copy of the governed clock."""

        return self._value(self.clock_bytes, label="snapshot materializer clock")


def build_causal_materializer_dependency_authority_v3(
    *, repository_root: Path | None = None
) -> dict[str, Any]:
    """Derive the exact worker/validator import and schema closure."""

    authority = build_dependency_authority(
        scope="dynamic-experiment-runtime-v3",
        entry_python_paths=_DEPENDENCY_ENTRIES,
        semantic_paths=_DEPENDENCY_SEMANTICS,
        authority_boundary=DEPENDENCY_AUTHORITY_BOUNDARY,
        repository_root=repository_root or Path(__file__).resolve().parents[2],
        runtime_distributions={},
    )
    if len(authority["entries"]) > 64 or len(canonical_json(authority)) > 512 * 1024:
        raise ContractError("materializer dependency authority exceeds its fixed ceiling")
    return authority


def _validate_dependency_authority(record: Mapping[str, Any]) -> dict[str, Any]:
    return validate_dependency_authority(
        record,
        scope="dynamic-experiment-runtime-v3",
        entry_python_paths=_DEPENDENCY_ENTRIES,
        semantic_paths=_DEPENDENCY_SEMANTICS,
        authority_boundary=DEPENDENCY_AUTHORITY_BOUNDARY,
        repository_root=Path(__file__).resolve().parents[2],
        runtime_distributions={},
    )


def _base(namespace: Namespace) -> Path:
    return (
        EVIDENCE_ROOT
        / namespace.target_id
        / namespace.run_id
        / namespace.branch_id
        / f"state-{namespace.state_version}"
    )


def _ref(
    *, path: str, data: bytes, namespace: Namespace, schema: bool = True
) -> dict[str, Any]:
    value = evidence_ref(path=path, data=data, namespace=namespace.as_dict())
    if schema:
        validate_payload(value, COMPACT_REF_SCHEMA)
    return value


def _request_digest(request: Mapping[str, Any]) -> str:
    return canonical_digest(
        {key: value for key, value in request.items() if key not in {"request_id", "request_digest"}}
    )


def _input_digest(request: Mapping[str, Any]) -> str:
    return canonical_digest(
        {
            "identity": request["identity"],
            "operator": request["operator"],
            "parameters": request["parameters"],
            "input_artifacts": request["input_artifacts"],
            "declared_outputs": request["declared_outputs"],
        }
    )


def _validate_request(request: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(request))
    validate_payload(value, REQUEST_SCHEMA)
    if value["operator"] != OPERATOR or set(value["parameters"]) != PARAMETER_KEYS:
        raise ContractError("materializer request is not the closed compact contract")
    if value["parameters"]["semantic_authorship"] is not False:
        raise ContractError("materializer request cannot claim semantic authorship")
    if value["parameters"]["authority_boundary"] != LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY:
        raise ContractError("materializer request authority boundary drifted")
    if len(value["input_artifacts"]) != 1 or len(value["declared_outputs"]) != 1:
        raise ContractError("materializer request must bind one input and one output")
    if value["input_digest"] != _input_digest(value):
        raise ContractError("materializer request input digest is invalid")
    if value["request_digest"] != _request_digest(value):
        raise ContractError("materializer request digest is invalid")
    if value["request_id"] != stable_identifier("opreq", value["request_digest"]):
        raise ContractError("materializer request identity is invalid")
    if len(canonical_json(value)) > MAX_REQUEST_BYTES:
        raise ContractError("materializer request exceeds its fixed byte ceiling")
    return value


def _build_request(
    *,
    namespace: Namespace,
    invocation_id: str,
    input_ref: Mapping[str, Any],
    output_path: str,
    parameters: Mapping[str, Any],
) -> dict[str, Any]:
    request: dict[str, Any] = {
        "schema_version": "1.0.0",
        "invocation_id": invocation_id,
        "operator": dict(OPERATOR),
        "identity": namespace.as_dict(),
        "required": True,
        "requested_at": utc_now(),
        "parameters": copy.deepcopy(dict(parameters)),
        "input_artifacts": [copy.deepcopy(dict(input_ref))],
        "declared_outputs": [output_path],
    }
    request["input_digest"] = _input_digest(request)
    request["request_digest"] = _request_digest(request)
    request["request_id"] = stable_identifier("opreq", request["request_digest"])
    return _validate_request(request)


def _receipt_without_identity(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in receipt.items()
        if key not in {"receipt_id", "receipt_digest"}
    }


def _validate_receipt(receipt: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(receipt))
    validate_payload(value, RECEIPT_SCHEMA)
    if (
        value["semantic_authorship"] is not False
        or value["authority_boundary"] != LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY
    ):
        raise ContractError("materializer receipt exceeds byte-materialization authority")
    if (
        value["request_id"] != request["request_id"]
        or value["request_digest"] != request["request_digest"]
        or value["invocation_id"] != request["invocation_id"]
        or value["operator"] != OPERATOR
        or value["input_ref"] != request["input_artifacts"][0]
    ):
        raise ContractError("materializer receipt differs from its exact request")
    digest = canonical_digest(_receipt_without_identity(value))
    if value["receipt_digest"] != digest or value["receipt_id"] != stable_identifier(
        "materializer-receipt-v3", request["request_id"], value["attempt"], digest
    ):
        raise ContractError("materializer receipt identity is invalid")
    return value


def _parse_utc(raw: str) -> dt.datetime:
    try:
        value = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ContractError(f"invalid governed UTC timestamp: {raw!r}") from exc
    if value.tzinfo is None:
        raise ContractError("governed timestamp lacks a timezone")
    return value.astimezone(dt.UTC)


def _binding_core(binding: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in binding.items()
        if key not in {"binding_id", "binding_digest"}
    }


def _clock_core(clock: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in clock.items()
        if key not in {"clock_id", "clock_digest"}
    }


def validate_causal_materializer_binding_v3(
    binding: Mapping[str, Any],
    *,
    workspace: Path,
) -> dict[str, Any]:
    """Replay through the read-once snapshot core and return a defensive value."""

    return _snapshot_binding_v3(binding, workspace=workspace).binding


def _validate_binding_envelope_v3(
    binding: Mapping[str, Any],
) -> tuple[dict[str, Any], bytes, dict[str, Any], Namespace]:
    """Validate path-independent binding identity and authority."""

    value = copy.deepcopy(dict(binding))
    encoded = canonical_json(value)
    if len(encoded) > MAX_BINDING_BYTES:
        raise ContractError("compact materializer binding exceeds its byte ceiling")
    if b'"artifact_value"' in encoded or b'"bytes_base64"' in encoded:
        raise ContractError("compact materializer binding embeds forbidden artifact material")
    validate_payload(value, BINDING_SCHEMA)
    digest = canonical_digest(_binding_core(value))
    if value["binding_digest"] != digest or value["binding_id"] != stable_identifier(
        "causal-materializer-binding-v3", digest
    ):
        raise ContractError("compact materializer binding identity is invalid")
    if value["ceilings"] != CEILINGS:
        raise ContractError("compact materializer ceilings drifted")
    if (
        value["semantic_authorship"] is not False
        or value["authority_boundary"] != LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY
    ):
        raise ContractError("materializer binding exceeds byte-materialization authority")
    dependency = _validate_dependency_authority(value["dependency_authority"])
    if dependency["content_digest"] != value["dependency_authority"]["content_digest"]:
        raise ContractError("materializer executable dependency authority drifted")
    return value, encoded, dependency, Namespace.from_mapping(value["identity"])


def _capture_plan_v3(
    value: Mapping[str, Any],
    *,
    namespace: Namespace,
) -> tuple[tuple[dict[str, Any], int, str], ...]:
    """Build one ordered read plan, coalescing exact reference aliases."""

    described: list[tuple[Mapping[str, Any], int, str]] = [
        (
            value["staged_input_ref"],
            MAX_ARTIFACT_BYTES,
            "committed staged materializer input",
        ),
        (value["request_ref"], MAX_REQUEST_BYTES, "durable materializer request"),
        *[
            (ref, MAX_RECEIPT_BYTES, f"materializer attempt receipt {index}")
            for index, ref in enumerate(value["attempt_receipt_refs"], start=1)
        ],
        (
            value["successful_receipt_ref"],
            MAX_RECEIPT_BYTES,
            "successful materializer receipt",
        ),
        (value["output_ref"], MAX_ARTIFACT_BYTES, "materialized causal output"),
        (
            value["history_ref"],
            MAX_ARTIFACT_BYTES,
            "immutable materializer output history",
        ),
        (value["clock_ref"], MAX_REQUEST_BYTES, "materializer governed clock"),
    ]
    expected_namespace = namespace.as_dict()
    unique: dict[str, tuple[dict[str, Any], int, str]] = {}
    for raw_ref, max_bytes, label in described:
        ref = copy.deepcopy(dict(raw_ref))
        validate_payload(ref, COMPACT_REF_SCHEMA)
        if ref["namespace"] != expected_namespace:
            raise ContractError("compact materializer references cross namespace boundaries")
        prior = unique.get(ref["path"])
        if prior is not None:
            if prior[0] != ref:
                raise ContractError("one evidence path has conflicting compact descriptors")
            continue
        unique[ref["path"]] = (ref, max_bytes, label)
    return tuple(unique.values())


def _capture_refs_once_v3(
    workspace: Path,
    plan: Sequence[tuple[Mapping[str, Any], int, str]],
) -> dict[str, bytes]:
    """Open every unique compact reference exactly once."""

    captured: dict[str, bytes] = {}
    for ref, max_bytes, _label in plan:
        try:
            captured[ref["path"]] = read_ref(workspace, ref, max_bytes=max_bytes)
        except CausalMaterializerIOError as exc:
            raise ContractError(str(exc)) from exc
    return captured


def _captured_bytes_v3(
    captured: Mapping[str, bytes],
    ref: Mapping[str, Any],
) -> bytes:
    """Resolve one descriptor solely from the already captured byte map."""

    path = ref["path"]
    try:
        data = captured[path]
    except KeyError as exc:
        raise ContractError(f"captured materializer evidence is missing {path}") from exc
    if len(data) != ref["size_bytes"] or tagged_sha256(data) != ref["sha256"]:
        raise ContractError("captured materializer evidence differs from its descriptor")
    return data


def _decode_captured_v3(
    captured: Mapping[str, bytes],
    ref: Mapping[str, Any],
    *,
    label: str,
) -> tuple[dict[str, Any], bytes]:
    data = _captured_bytes_v3(captured, ref)
    try:
        return decode_canonical_object(data, label=label), data
    except CausalMaterializerIOError as exc:
        raise ContractError(str(exc)) from exc


def _validate_captured_materialization_v3(
    *,
    value: Mapping[str, Any],
    binding_bytes: bytes,
    dependency: Mapping[str, Any],
    plan: Sequence[tuple[Mapping[str, Any], int, str]],
    captured: Mapping[str, bytes],
) -> VerifiedCausalMaterializationSnapshotV3:
    """Replay all evidence causality without filesystem access after capture."""

    expected_paths = tuple(ref["path"] for ref, _ceiling, _label in plan)
    if tuple(captured) != expected_paths:
        raise ContractError("captured materializer evidence set or order drifted")
    try:
        decoded_binding = decode_canonical_object(
            binding_bytes, label="captured materializer binding"
        )
    except CausalMaterializerIOError as exc:
        raise ContractError(str(exc)) from exc
    if decoded_binding != value:
        raise ContractError("captured materializer binding bytes drifted")

    input_value, input_bytes = _decode_captured_v3(
        captured,
        value["staged_input_ref"],
        label="committed staged materializer input",
    )
    if canonical_digest(input_value) != value["artifact_digest"]:
        raise ContractError("staged materializer input semantic digest drifted")
    request, request_bytes = _decode_captured_v3(
        captured,
        value["request_ref"],
        label="durable materializer request",
    )
    request = _validate_request(request)
    parameters = request["parameters"]
    if (
        request["invocation_id"] != value["invocation_id"]
        or request["identity"] != value["identity"]
        or request["input_artifacts"] != [value["staged_input_ref"]]
        or parameters["causal_stage_id"] != value["stage_id"]
        or parameters["materializer_role"] != value["materializer_role"]
        or parameters["artifact_id"] != value["artifact_id"]
        or parameters["artifact_digest"] != value["artifact_digest"]
        or parameters["evidence_authority_id"] != value["evidence_authority_id"]
        or parameters["dependency_authority_digest"] != dependency["content_digest"]
    ):
        raise ContractError("compact materializer request-to-binding causality drifted")

    receipts: list[dict[str, Any]] = []
    receipt_bytes: list[bytes] = []
    for index, ref in enumerate(value["attempt_receipt_refs"], start=1):
        receipt, encoded_receipt = _decode_captured_v3(
            captured,
            ref,
            label=f"materializer attempt receipt {index}",
        )
        receipt = _validate_receipt(receipt, request)
        if receipt["attempt"] != index:
            raise ContractError("materializer attempt history is not contiguous")
        receipts.append(receipt)
        receipt_bytes.append(encoded_receipt)
    successful = [receipt for receipt in receipts if receipt["status"] == "succeeded"]
    if (
        len(successful) != 1
        or successful[0] != receipts[-1]
        or value["successful_attempt"] != len(receipts)
        or value["successful_receipt_ref"] != value["attempt_receipt_refs"][-1]
    ):
        raise ContractError("materializer success is not the terminal contiguous attempt")
    success = successful[0]
    if success["output_ref"] != value["output_ref"] or success["history_ref"] != value["history_ref"]:
        raise ContractError("materializer success differs from bound output/history refs")
    output_value, output_bytes = _decode_captured_v3(
        captured,
        value["output_ref"],
        label="materialized causal output",
    )
    history_value, history_bytes = _decode_captured_v3(
        captured,
        value["history_ref"],
        label="immutable materializer output history",
    )
    if input_bytes != output_bytes or input_bytes != history_bytes:
        raise ContractError("materializer input, output, and history bytes differ")
    if input_value != output_value or input_value != history_value:
        raise ContractError("materializer semantic projections differ")

    clock, clock_bytes = _decode_captured_v3(
        captured,
        value["clock_ref"],
        label="materializer governed clock",
    )
    validate_payload(clock, CLOCK_SCHEMA)
    clock_digest = canonical_digest(_clock_core(clock))
    if clock["clock_digest"] != clock_digest or clock["clock_id"] != stable_identifier(
        "causal-materializer-clock-v3", clock_digest
    ):
        raise ContractError("materializer clock identity is invalid")
    if (
        clock["invocation_id"] != value["invocation_id"]
        or clock["request_ref"] != value["request_ref"]
        or clock["receipt_ref"] != value["successful_receipt_ref"]
        or clock["requested_at"] != request["requested_at"]
        or clock["started_at"] != success["started_at"]
        or clock["completed_at"] != success["completed_at"]
        or clock["sealed_at"] != success["completed_at"]
    ):
        raise ContractError("materializer clock does not bind the successful attempt")
    ordered = [
        _parse_utc(clock[field])
        for field in ("requested_at", "started_at", "completed_at", "sealed_at")
    ]
    if ordered != sorted(ordered):
        raise ContractError("materializer governed timestamps are out of order")

    snapshot_digest = canonical_digest(
        {
            "snapshot_kind": "verified-causal-materialization-v3",
            "binding_sha256": tagged_sha256(binding_bytes),
            "captured_evidence": [
                {
                    "path": ref["path"],
                    "descriptor_sha256": tagged_sha256(canonical_json(dict(ref))),
                    "content_sha256": tagged_sha256(captured[ref["path"]]),
                    "size_bytes": len(captured[ref["path"]]),
                }
                for ref, _ceiling, _label in plan
            ],
        }
    )
    return VerifiedCausalMaterializationSnapshotV3(
        snapshot_digest=snapshot_digest,
        binding_bytes=bytes(binding_bytes),
        staged_input_bytes=bytes(input_bytes),
        request_bytes=bytes(request_bytes),
        attempt_receipt_bytes=tuple(bytes(data) for data in receipt_bytes),
        output_bytes=bytes(output_bytes),
        history_bytes=bytes(history_bytes),
        clock_bytes=bytes(clock_bytes),
        captured_ref_paths=expected_paths,
    )


def _snapshot_binding_v3(
    binding: Mapping[str, Any],
    *,
    workspace: Path,
    binding_bytes: bytes | None = None,
) -> VerifiedCausalMaterializationSnapshotV3:
    """Capture and replay one binding through the shared read-once core."""

    workspace = Path(workspace).resolve(strict=True)
    value, canonical_binding, dependency, namespace = _validate_binding_envelope_v3(
        binding
    )
    encoded_binding = canonical_binding if binding_bytes is None else bytes(binding_bytes)
    plan = _capture_plan_v3(value, namespace=namespace)
    captured = _capture_refs_once_v3(workspace, plan)
    return _validate_captured_materialization_v3(
        value=value,
        binding_bytes=encoded_binding,
        dependency=dependency,
        plan=plan,
        captured=captured,
    )


def revalidate_causal_materialization_snapshot_v3(
    snapshot: VerifiedCausalMaterializationSnapshotV3,
) -> VerifiedCausalMaterializationSnapshotV3:
    """Purely replay one detached snapshot through the public v3 boundary.

    Portable graph adapters must not couple themselves to the runtime's private
    capture-plan helpers.  This function accepts only the exact snapshot type,
    rebuilds its alias-aware captured-byte map, replays binding/dependency/
    request/attempt/output/history/clock causality, and returns a fresh verified
    snapshot without consulting the source workspace.  Its authority remains
    local byte-materialization provenance and never semantic authorship.
    """

    if type(snapshot) is not VerifiedCausalMaterializationSnapshotV3:
        raise ContractError("snapshot replay requires the exact verified v3 type")
    binding = snapshot.binding
    value, binding_bytes, dependency, namespace = _validate_binding_envelope_v3(
        binding
    )
    if snapshot.binding_bytes != binding_bytes:
        raise ContractError("snapshot binding bytes differ from their canonical value")

    described: list[tuple[Mapping[str, Any], bytes]] = [
        (value["staged_input_ref"], snapshot.staged_input_bytes),
        (value["request_ref"], snapshot.request_bytes),
        *zip(
            value["attempt_receipt_refs"],
            snapshot.attempt_receipt_bytes,
            strict=True,
        ),
        (value["successful_receipt_ref"], snapshot.successful_receipt_bytes),
        (value["output_ref"], snapshot.output_bytes),
        (value["history_ref"], snapshot.history_bytes),
        (value["clock_ref"], snapshot.clock_bytes),
    ]
    captured: dict[str, bytes] = {}
    descriptors: dict[str, dict[str, Any]] = {}
    for raw_ref, raw_data in described:
        if type(raw_data) is not bytes:
            raise ContractError("snapshot evidence must be exact immutable bytes")
        ref = copy.deepcopy(dict(raw_ref))
        path = str(ref["path"])
        prior = captured.get(path)
        if prior is not None and (prior != raw_data or descriptors[path] != ref):
            raise ContractError("snapshot aliases one source path to different evidence")
        captured.setdefault(path, bytes(raw_data))
        descriptors.setdefault(path, ref)
    if tuple(captured) != snapshot.captured_ref_paths:
        raise ContractError("snapshot captured-path order differs from its binding")

    plan = _capture_plan_v3(value, namespace=namespace)
    verified = _validate_captured_materialization_v3(
        value=value,
        binding_bytes=binding_bytes,
        dependency=dependency,
        plan=plan,
        captured=captured,
    )
    if verified != snapshot:
        raise ContractError("snapshot fields differ from pure causal replay")
    return verified


def snapshot_sealed_causal_materialization_v3(
    sealed: SealedCausalMaterializationV3,
    *,
    workspace: Path,
) -> VerifiedCausalMaterializationSnapshotV3:
    """Read one exact seal once and detach verified evidence from local paths."""

    if type(sealed) is not SealedCausalMaterializationV3:
        raise ContractError("sealed materialization must have the exact v3 seal type")
    workspace = Path(workspace).resolve(strict=True)
    value, canonical_binding, dependency, namespace = _validate_binding_envelope_v3(
        sealed.binding
    )
    try:
        sealed_request_bytes = canonical_json(dict(sealed.request))
        sealed_success_bytes = canonical_json(dict(sealed.successful_receipt))
    except (TypeError, ValueError) as exc:
        raise ContractError("sealed materialization projections are invalid") from exc

    binding_relative = (
        _base(namespace) / "bindings" / f"{value['invocation_id']}.json"
    ).as_posix()
    expected_binding_path = workspace / binding_relative
    expected_request_path = workspace / value["request_ref"]["path"]
    expected_receipt_paths = tuple(
        workspace / ref["path"] for ref in value["attempt_receipt_refs"]
    )
    if (
        Path(sealed.binding_path) != expected_binding_path
        or Path(sealed.request_path) != expected_request_path
        or tuple(Path(path) for path in sealed.receipt_paths) != expected_receipt_paths
    ):
        raise ContractError("sealed materialization paths differ from its exact binding")
    try:
        stored_binding = safe_read(
            workspace,
            binding_relative,
            max_bytes=MAX_BINDING_BYTES,
            expected_sha256=tagged_sha256(canonical_binding),
            expected_size=len(canonical_binding),
        )
    except CausalMaterializerIOError as exc:
        raise ContractError(str(exc)) from exc

    plan = _capture_plan_v3(value, namespace=namespace)
    captured = _capture_refs_once_v3(workspace, plan)
    snapshot = _validate_captured_materialization_v3(
        value=value,
        binding_bytes=stored_binding,
        dependency=dependency,
        plan=plan,
        captured=captured,
    )
    if (
        snapshot.request_bytes != sealed_request_bytes
        or snapshot.successful_receipt_bytes != sealed_success_bytes
    ):
        raise ContractError("sealed materialization projections cross binding boundaries")
    return snapshot


class CausalArtifactMaterializerRuntimeV3:
    """Stage, materialize, validate, and seal compact local causal evidence."""

    def __init__(self, *, workspace: Path, namespace: Namespace) -> None:
        raw_workspace = Path(workspace)
        if raw_workspace.is_symlink() or not raw_workspace.is_dir():
            raise ContractError("materializer workspace must be an existing real directory")
        self.workspace = raw_workspace.resolve(strict=True)
        self.namespace = namespace
        self.worker_command = (
            sys.executable,
            str(Path(__file__).resolve().parents[1] / "scripts" / "run_causal_materializer_v3.py"),
            "--workspace",
            str(self.workspace),
        )
        self.validator_command = (
            sys.executable,
            str(Path(__file__).resolve().parents[1] / "scripts" / "validate_causal_materializer_v3.py"),
            "--workspace",
            str(self.workspace),
        )

    @contextlib.contextmanager
    def _invocation_lock(self, relative_path: str) -> Iterator[None]:
        """Serialize attempt allocation; immutable evidence still uses atomic links."""

        try:
            write_create_only(
                self.workspace,
                relative_path,
                b"causal-materializer-v3-lock\n",
                max_bytes=128,
            )
            absolute = self.workspace / relative_path
            flags = os.O_RDWR | os.O_CLOEXEC | os.O_NOFOLLOW
            descriptor = os.open(absolute, flags)
            metadata = os.fstat(descriptor)
            if not os.path.isfile(absolute) or metadata.st_nlink != 1:
                raise ContractError("materializer invocation lock is not a regular single-link file")
        except (OSError, CausalMaterializerIOError) as exc:
            raise ContractError("materializer invocation lock cannot be opened safely") from exc
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def _run_command(
        self, command: Sequence[str], payload: bytes
    ) -> subprocess.CompletedProcess[bytes]:
        """Single overridable subprocess seam used by retry adversarial tests."""

        return subprocess.run(
            list(command),
            cwd=self.workspace,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
            check=False,
        )

    def _attempts(
        self,
        *,
        base: Path,
        invocation_id: str,
        request: Mapping[str, Any],
    ) -> list[tuple[dict[str, Any], dict[str, Any], Path]]:
        directory = self.workspace / base / "attempts" / invocation_id
        if not directory.exists():
            return []
        if directory.is_symlink() or not directory.is_dir():
            raise ContractError("materializer attempt root is not a real directory")
        numbered: list[tuple[int, str]] = []
        for path in directory.iterdir():
            match = re.fullmatch(r"attempt-([1-9][0-9]*)\.json", path.name)
            if match is None:
                raise ContractError("materializer attempt root contains an unexpected entry")
            numbered.append((int(match.group(1)), path.name))
        numbered.sort()
        if [row[0] for row in numbered] != list(range(1, len(numbered) + 1)) or len(
            numbered
        ) > MAX_ATTEMPTS:
            raise ContractError("materializer attempt history is not contiguous and bounded")
        attempts: list[tuple[dict[str, Any], dict[str, Any], Path]] = []
        for index, name in numbered:
            relative = (base / "attempts" / invocation_id / name).as_posix()
            try:
                data = safe_read(
                    self.workspace,
                    relative,
                    max_bytes=MAX_RECEIPT_BYTES,
                )
            except CausalMaterializerIOError as exc:
                raise ContractError(str(exc)) from exc
            receipt = _validate_receipt(
                decode_canonical_object(data, label=f"materializer attempt {index}"),
                request,
            )
            if receipt["attempt"] != index:
                raise ContractError("materializer attempt path and identity differ")
            attempts.append(
                (
                    receipt,
                    _ref(path=relative, data=data, namespace=self.namespace),
                    self.workspace / relative,
                )
            )
        return attempts

    def _execute_attempt(
        self,
        *,
        base: Path,
        request: Mapping[str, Any],
        attempt: int,
        input_ref: Mapping[str, Any],
        dependency_digest: str,
    ) -> tuple[dict[str, Any], dict[str, Any], Path]:
        started_at = utc_now()
        monotonic_start = time.monotonic()
        status = "failed"
        exit_code: int | None = None
        stdout = b""
        stderr = b""
        output_ref: dict[str, Any] | None = None
        history_ref: dict[str, Any] | None = None
        validator = {
            "validator_id": MATERIALIZER_VALIDATOR_ID,
            "version": MATERIALIZER_VALIDATOR_VERSION,
            "status": "not_run",
            "dependency_authority_digest": dependency_digest,
            "stdout_digest": tagged_sha256(b""),
            "stderr_digest": tagged_sha256(b""),
            "exit_code": None,
        }
        error: dict[str, Any] | None = None
        try:
            worker = self._run_command(self.worker_command, canonical_json(dict(request)))
            exit_code, stdout, stderr = worker.returncode, worker.stdout, worker.stderr
            if len(stdout) > 64 * 1024 or len(stderr) > 64 * 1024:
                raise ContractError("materializer subprocess diagnostics exceed their ceiling")
            if worker.returncode != 0:
                raise subprocess.CalledProcessError(
                    worker.returncode,
                    self.worker_command,
                    output=worker.stdout,
                    stderr=worker.stderr,
                )
            protocol = decode_canonical_object(stdout, label="materializer worker protocol")
            if set(protocol) != {"artifacts", "explicit_unknowns"}:
                raise ContractError("materializer worker protocol is not closed")
            declared_output = request["declared_outputs"][0]
            if protocol["artifacts"] != [{"path": declared_output}]:
                raise ContractError("materializer worker reported a different output")
            output_bytes = safe_read(
                self.workspace,
                declared_output,
                max_bytes=MAX_ARTIFACT_BYTES,
            )
            output_ref = _ref(
                path=declared_output,
                data=output_bytes,
                namespace=self.namespace,
            )
            validator_protocol = canonical_json(
                {"request": dict(request), "output_ref": output_ref}
            )
            checked = self._run_command(self.validator_command, validator_protocol)
            if len(checked.stdout) > 64 * 1024 or len(checked.stderr) > 64 * 1024:
                raise ContractError("materializer validator diagnostics exceed their ceiling")
            validator = {
                **validator,
                "status": "passed" if checked.returncode == 0 else "failed",
                "stdout_digest": tagged_sha256(checked.stdout),
                "stderr_digest": tagged_sha256(checked.stderr),
                "exit_code": checked.returncode,
            }
            if checked.returncode != 0:
                raise subprocess.CalledProcessError(
                    checked.returncode,
                    self.validator_command,
                    output=checked.stdout,
                    stderr=checked.stderr,
                )
            history_path = (
                base
                / "history"
                / request["invocation_id"]
                / f"attempt-{attempt}.json"
            ).as_posix()
            write_create_only(
                self.workspace,
                history_path,
                output_bytes,
                max_bytes=MAX_ARTIFACT_BYTES,
            )
            history_ref = _ref(
                path=history_path,
                data=output_bytes,
                namespace=self.namespace,
            )
            status = "succeeded"
        except subprocess.TimeoutExpired as exc:
            status = "timed_out"
            error = {
                "error_type": type(exc).__name__,
                "message_digest": canonical_digest(str(exc)),
            }
        except Exception as exc:
            status = "failed"
            error = {
                "error_type": type(exc).__name__[:128],
                "message_digest": canonical_digest(str(exc)),
            }
        completed_at = utc_now()
        receipt: dict[str, Any] = {
            "schema_version": "3.0.0",
            "receipt_kind": "causal_byte_materializer_attempt",
            "request_id": request["request_id"],
            "request_digest": request["request_digest"],
            "invocation_id": request["invocation_id"],
            "attempt": attempt,
            "operator": dict(OPERATOR),
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_seconds": min(
                60.0, round(max(0.0, time.monotonic() - monotonic_start), 6)
            ),
            "status": status,
            "exit_code": exit_code,
            "stdout_digest": tagged_sha256(stdout),
            "stderr_digest": tagged_sha256(stderr),
            "input_ref": copy.deepcopy(dict(input_ref)),
            "output_ref": output_ref if status == "succeeded" else None,
            "history_ref": history_ref if status == "succeeded" else None,
            "validator": validator,
            "error": None if status == "succeeded" else error,
        }
        receipt_digest = canonical_digest(receipt)
        receipt["receipt_id"] = stable_identifier(
            "materializer-receipt-v3", request["request_id"], attempt, receipt_digest
        )
        receipt["receipt_digest"] = receipt_digest
        receipt = _validate_receipt(receipt, request)
        receipt_data = canonical_json(receipt)
        relative = (
            base / "attempts" / request["invocation_id"] / f"attempt-{attempt}.json"
        ).as_posix()
        write_create_only(
            self.workspace,
            relative,
            receipt_data,
            max_bytes=MAX_RECEIPT_BYTES,
        )
        return (
            receipt,
            _ref(path=relative, data=receipt_data, namespace=self.namespace),
            self.workspace / relative,
        )

    def _finalize(
        self,
        *,
        base: Path,
        stage_id: str,
        materializer_role: str,
        artifact_id: str,
        artifact_digest: str,
        evidence_authority_id: str,
        request: Mapping[str, Any],
        request_ref: Mapping[str, Any],
        input_ref: Mapping[str, Any],
        attempts: Sequence[tuple[dict[str, Any], dict[str, Any], Path]],
        dependency_authority: Mapping[str, Any],
    ) -> SealedCausalMaterializationV3:
        success, success_ref, _success_path = attempts[-1]
        if success["status"] != "succeeded":
            raise ContractError("cannot finalize an unsuccessful materializer attempt")
        clock: dict[str, Any] = {
            "schema_version": "3.0.0",
            "clock_kind": "causal_byte_materializer_governed_clock",
            "clock_authority_id": "canonical-local-governed-utc-clock",
            "invocation_id": request["invocation_id"],
            "request_ref": copy.deepcopy(dict(request_ref)),
            "receipt_ref": copy.deepcopy(dict(success_ref)),
            "requested_at": request["requested_at"],
            "started_at": success["started_at"],
            "completed_at": success["completed_at"],
            "sealed_at": success["completed_at"],
            "ordering_verified": True,
        }
        clock_digest = canonical_digest(clock)
        clock["clock_id"] = stable_identifier("causal-materializer-clock-v3", clock_digest)
        clock["clock_digest"] = clock_digest
        validate_payload(clock, CLOCK_SCHEMA)
        clock_data = canonical_json(clock)
        clock_path = (base / "clocks" / f"{request['invocation_id']}.json").as_posix()
        write_create_only(
            self.workspace,
            clock_path,
            clock_data,
            max_bytes=MAX_REQUEST_BYTES,
        )
        clock_ref = _ref(path=clock_path, data=clock_data, namespace=self.namespace)
        binding: dict[str, Any] = {
            "schema_version": "3.0.0",
            "contract_version": "experiment-causal-byte-materializer-binding/3.0.0",
            "capability_kind": "causal_byte_materializer",
            "materialization_semantics": "exact_canonical_input_bytes_copied_without_interpretation",
            "local_protocol_valid": True,
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "evidence_authority_id": evidence_authority_id,
            "stage_id": stage_id,
            "materializer_role": materializer_role,
            "artifact_id": artifact_id,
            "artifact_digest": artifact_digest,
            "identity": self.namespace.as_dict(),
            "invocation_id": request["invocation_id"],
            "staged_input_ref": copy.deepcopy(dict(input_ref)),
            "request_ref": copy.deepcopy(dict(request_ref)),
            "attempt_receipt_refs": [copy.deepcopy(row[1]) for row in attempts],
            "successful_attempt": len(attempts),
            "successful_receipt_ref": copy.deepcopy(dict(success_ref)),
            "output_ref": copy.deepcopy(success["output_ref"]),
            "history_ref": copy.deepcopy(success["history_ref"]),
            "clock_ref": clock_ref,
            "dependency_authority": copy.deepcopy(dict(dependency_authority)),
            "ceilings": dict(CEILINGS),
        }
        binding_digest = canonical_digest(binding)
        binding["binding_id"] = stable_identifier(
            "causal-materializer-binding-v3", binding_digest
        )
        binding["binding_digest"] = binding_digest
        validate_payload(binding, BINDING_SCHEMA)
        binding_data = canonical_json(binding)
        binding_path = (base / "bindings" / f"{request['invocation_id']}.json").as_posix()
        write_create_only(
            self.workspace,
            binding_path,
            binding_data,
            max_bytes=MAX_BINDING_BYTES,
        )
        validated = validate_causal_materializer_binding_v3(
            binding,
            workspace=self.workspace,
        )
        return SealedCausalMaterializationV3(
            binding=validated,
            binding_path=self.workspace / binding_path,
            request=copy.deepcopy(dict(request)),
            request_path=self.workspace / request_ref["path"],
            successful_receipt=copy.deepcopy(success),
            receipt_paths=tuple(row[2] for row in attempts),
        )

    def seal(
        self,
        *,
        stage_id: str,
        materializer_role: str,
        artifact_id: str,
        artifact: Mapping[str, Any],
    ) -> SealedCausalMaterializationV3:
        """Stage one input and idempotently reuse or execute its exact invocation."""

        validate_identifier(stage_id, "stage_id")
        validate_identifier(materializer_role, "materializer_role")
        validate_identifier(artifact_id, "artifact_id")
        if not isinstance(artifact, Mapping):
            raise ContractError("materializer artifact must be one JSON object")
        artifact_bytes = canonical_json(dict(artifact))
        if not artifact_bytes or len(artifact_bytes) > MAX_ARTIFACT_BYTES:
            raise ContractError("materializer artifact exceeds its fixed byte ceiling")
        artifact_value = decode_canonical_object(artifact_bytes, label="materializer artifact")
        artifact_digest = canonical_digest(artifact_value)
        base = _base(self.namespace)
        input_id = stable_identifier(
            "causal-materializer-input-v3",
            self.namespace.as_dict(),
            artifact_id,
            artifact_digest,
        )
        input_path = (base / "staged-inputs" / f"{input_id}.json").as_posix()
        try:
            write_create_only(
                self.workspace,
                input_path,
                artifact_bytes,
                max_bytes=MAX_ARTIFACT_BYTES,
            )
        except CausalMaterializerIOError as exc:
            raise ContractError(str(exc)) from exc
        input_ref = _ref(path=input_path, data=artifact_bytes, namespace=self.namespace)
        dependency = build_causal_materializer_dependency_authority_v3()
        invocation_id = stable_identifier(
            "causal-materializer-invocation-v3",
            self.namespace.as_dict(),
            stage_id,
            materializer_role,
            artifact_id,
            input_ref,
            dependency["content_digest"],
        )
        evidence_authority_id = stable_identifier(
            "causal-materializer-authority-v3", invocation_id
        )
        output_path = (base / "artifacts" / f"{invocation_id}.json").as_posix()
        parameters = {
            "causal_stage_id": stage_id,
            "materializer_role": materializer_role,
            "artifact_id": artifact_id,
            "artifact_digest": artifact_digest,
            "evidence_authority_id": evidence_authority_id,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "semantic_authorship": False,
            "dependency_authority_digest": dependency["content_digest"],
        }
        request_path = (base / "requests" / f"{invocation_id}.json").as_posix()
        lock_path = (base / "locks" / f"{invocation_id}.lock").as_posix()
        with self._invocation_lock(lock_path):
            absolute_request = self.workspace / request_path
            if absolute_request.exists() or absolute_request.is_symlink():
                request_data = safe_read(
                    self.workspace,
                    request_path,
                    max_bytes=MAX_REQUEST_BYTES,
                )
                request = _validate_request(
                    decode_canonical_object(request_data, label="durable materializer request")
                )
            else:
                request = _build_request(
                    namespace=self.namespace,
                    invocation_id=invocation_id,
                    input_ref=input_ref,
                    output_path=output_path,
                    parameters=parameters,
                )
                request_data = canonical_json(request)
                write_create_only(
                    self.workspace,
                    request_path,
                    request_data,
                    max_bytes=MAX_REQUEST_BYTES,
                )
            expected_intent = {
                "invocation_id": invocation_id,
                "operator": OPERATOR,
                "identity": self.namespace.as_dict(),
                "parameters": parameters,
                "input_artifacts": [input_ref],
                "declared_outputs": [output_path],
            }
            if any(request.get(key) != expected for key, expected in expected_intent.items()):
                raise ContractError("durable first-wins request differs from causal intent")
            request_ref = _ref(
                path=request_path,
                data=request_data,
                namespace=self.namespace,
            )
            attempts = self._attempts(
                base=base,
                invocation_id=invocation_id,
                request=request,
            )
            successes = [row for row in attempts if row[0]["status"] == "succeeded"]
            if successes:
                if len(successes) != 1 or successes[0] != attempts[-1]:
                    raise ContractError("materializer attempt history continues after success")
            else:
                if len(attempts) >= MAX_ATTEMPTS:
                    raise ContractError("materializer exhausted its fixed attempt ceiling")
                attempt = self._execute_attempt(
                    base=base,
                    request=request,
                    attempt=len(attempts) + 1,
                    input_ref=input_ref,
                    dependency_digest=dependency["content_digest"],
                )
                attempts = [*attempts, attempt]
                if attempt[0]["status"] != "succeeded":
                    raise ContractError(
                        f"causal byte materializer attempt {len(attempts)} {attempt[0]['status']}"
                    )
            return self._finalize(
                base=base,
                stage_id=stage_id,
                materializer_role=materializer_role,
                artifact_id=artifact_id,
                artifact_digest=artifact_digest,
                evidence_authority_id=evidence_authority_id,
                request=request,
                request_ref=request_ref,
                input_ref=input_ref,
                attempts=attempts,
                dependency_authority=dependency,
            )


__all__ = [
    "BINDING_SCHEMA",
    "CEILINGS",
    "CausalArtifactMaterializerRuntimeV3",
    "DEPENDENCY_AUTHORITY_BOUNDARY",
    "LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY",
    "MATERIALIZER_OPERATOR_ID",
    "MATERIALIZER_OPERATOR_KIND",
    "MATERIALIZER_OPERATOR_VERSION",
    "MATERIALIZER_VALIDATOR_ID",
    "MATERIALIZER_VALIDATOR_VERSION",
    "SealedCausalMaterializationV3",
    "VerifiedCausalMaterializationSnapshotV3",
    "build_causal_materializer_dependency_authority_v3",
    "revalidate_causal_materialization_snapshot_v3",
    "snapshot_sealed_causal_materialization_v3",
    "validate_causal_materializer_binding_v3",
]
