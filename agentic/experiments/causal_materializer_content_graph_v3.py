# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compile local causal-materializer evidence into a portable graph fragment.

The v3 byte materializer deliberately writes compact filesystem references: its
local binding can prove what a subprocess copied while the workspace is live,
but it cannot be reopened after that workspace disappears.  This module is the
one-way authority adapter.  It first replays a read-once
``VerifiedCausalMaterializationSnapshotV3`` and then emits only immutable,
path-free content objects:

* one opaque artifact object aliases the verified staged, output, and history
  bytes instead of storing three copies;
* one request record, every failed/timed-out/successful attempt, one clock, and
  one path-free dependency projection preserve protocol history;
* six typed structural evidence headers distinguish the logical evidence roles;
* one structural binding root is the only materializer object active v3 worlds
  may reference.

The result is a mergeable graph fragment, not a transaction.  A world runtime
must merge its objects, edges, and order into the single content graph committed
for that generation.  Reopening is pure over store-verified content objects and
never consults the source workspace.  All authority remains exact local byte-
copy protocol evidence: no object in this module authors or interprets physics.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
)
from agentic.scripts.causal_materializer_io_v3 import (
    MAX_ARTIFACT_BYTES,
    MAX_ATTEMPTS,
)

from .causal_producer_runtime_v3 import (
    CEILINGS,
    DEPENDENCY_AUTHORITY_BOUNDARY,
    LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
    VerifiedCausalMaterializationSnapshotV3,
    revalidate_causal_materialization_snapshot_v3,
)
from .world_object_graph import (
    PreparedContentObject,
    ResolvedContentObject,
    prepare_content_object,
)
from .world_object_roles import (
    HEADER_AUTHORITY_BOUNDARY,
    derive_content_object_edges,
    seal_content_object_header,
    validate_content_object_payload,
    validate_payload_derived_edges,
    validate_role_bound_object,
)


ARTIFACT_KIND = "causal_materializer_artifact_evidence_v3"
REQUEST_KIND = "causal_materializer_request_record_v3"
ATTEMPT_KIND = "causal_materializer_attempt_record_v3"
CLOCK_KIND = "causal_materializer_clock_record_v3"
DEPENDENCY_KIND = "causal_materializer_dependency_record_v3"
EVIDENCE_HEADER_KIND = "causal_materializer_evidence_header_v3"
BINDING_HEADER_KIND = "causal_materializer_binding_header_v3"

EVIDENCE_KINDS = (
    "staged_input",
    "producer_request",
    "attempt_receipts",
    "producer_artifact",
    "immutable_history",
    "governed_clock",
)
ROOT_EVIDENCE_FIELDS = {
    "staged_input": "staged_input_evidence_header_ref",
    "producer_request": "producer_request_evidence_header_ref",
    "attempt_receipts": "attempt_receipts_evidence_header_ref",
    "producer_artifact": "producer_artifact_evidence_header_ref",
    "immutable_history": "immutable_history_evidence_header_ref",
    "governed_clock": "governed_clock_evidence_header_ref",
}

# At MAX_ATTEMPTS the fragment contains one artifact, one request, 32 attempt
# records, one clock, one dependency projection, six headers, and one root.
MAX_PORTABLE_FRAGMENT_OBJECTS = MAX_ATTEMPTS + 11
MAX_PORTABLE_DEPENDENCY_COMPONENTS = 64
MAX_PORTABLE_FRAGMENT_BYTES = 32 * 1024 * 1024
MAX_PORTABLE_PREFIX_BYTES = 512


@dataclass(frozen=True, slots=True)
class _SealedFragmentObject:
    """Canonical object bytes plus a descriptor-only storage locator."""

    object_kind: str
    path: str
    data: bytes


@dataclass(frozen=True, slots=True)
class PreparedPortableCausalMaterializationFragmentV3:
    """A defensive graph fragment ready to merge into one generation graph."""

    snapshot_digest: str
    _objects: tuple[_SealedFragmentObject, ...]
    _edge_data: tuple[bytes, ...]
    _topological_order: tuple[str, ...]
    _binding_root_ref_data: bytes
    _successful_receipt_ref_data: bytes

    @property
    def local_objects(self) -> tuple[PreparedContentObject, ...]:
        """Rebuild fresh prepared objects so caller mutation cannot alter the fragment."""

        rows: list[PreparedContentObject] = []
        for sealed in self._objects:
            value = _decode_mapping(sealed.data, "portable fragment object")
            rows.append(
                prepare_content_object(
                    object_kind=sealed.object_kind,
                    value=value,
                    path=sealed.path,
                )
            )
        return tuple(rows)

    @property
    def edges(self) -> tuple[dict[str, str], ...]:
        """Return defensive copies of the exact payload-derived edge vector."""

        return tuple(
            _decode_mapping(data, "portable fragment edge")  # type: ignore[return-value]
            for data in self._edge_data
        )

    @property
    def topological_order(self) -> tuple[str, ...]:
        """Return dependency-first object IDs for deterministic graph composition."""

        return tuple(self._topological_order)

    @property
    def binding_root_ref(self) -> dict[str, Any]:
        """Return the sole materializer reference admissible to active v3 worlds."""

        return _decode_mapping(
            self._binding_root_ref_data, "portable materializer binding-root ref"
        )

    @property
    def successful_receipt_ref(self) -> dict[str, Any]:
        """Return the terminal attempt ref; no second success object is serialized."""

        return _decode_mapping(
            self._successful_receipt_ref_data,
            "portable materializer successful-receipt ref",
        )

    @property
    def total_object_bytes(self) -> int:
        """Report unique committed object bytes, including the artifact exactly once."""

        return sum(len(row.data) for row in self._objects)


@dataclass(frozen=True, slots=True)
class VerifiedPortableCausalMaterializationV3:
    """Path-free result of replaying one committed materialization closure."""

    source_snapshot_digest: str
    successful_attempt: int
    consumed_object_ids: tuple[str, ...]
    _binding_root_ref_data: bytes
    _artifact_ref_data: bytes
    _request_ref_data: bytes
    _attempt_ref_data: tuple[bytes, ...]
    _clock_ref_data: bytes

    @property
    def binding_root_ref(self) -> dict[str, Any]:
        return _decode_mapping(self._binding_root_ref_data, "verified binding-root ref")

    @property
    def artifact_ref(self) -> dict[str, Any]:
        return _decode_mapping(self._artifact_ref_data, "verified artifact ref")

    @property
    def request_ref(self) -> dict[str, Any]:
        return _decode_mapping(self._request_ref_data, "verified request ref")

    @property
    def attempt_refs(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            _decode_mapping(data, "verified attempt ref")
            for data in self._attempt_ref_data
        )

    @property
    def successful_receipt_ref(self) -> dict[str, Any]:
        return self.attempt_refs[-1]

    @property
    def clock_ref(self) -> dict[str, Any]:
        return _decode_mapping(self._clock_ref_data, "verified clock ref")


def _decode_mapping(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise ContractError(f"{label} must be immutable bytes")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise ContractError(f"{label} is not one canonical JSON object")
    return value


def _record_without_identity(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in record.items()
        if key not in {"record_id", "record_digest"}
    }


def _seal_record(record: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(record))
    value.pop("record_id", None)
    value.pop("record_digest", None)
    digest = canonical_digest(value)
    value["record_id"] = stable_identifier(
        "portable-causal-materializer-record-v3", value["record_kind"], digest
    )
    value["record_digest"] = digest
    return validate_content_object_payload(str(value["record_kind"]), value)


def _verify_record_identity(record: Mapping[str, Any]) -> None:
    digest = canonical_digest(_record_without_identity(record))
    expected_id = stable_identifier(
        "portable-causal-materializer-record-v3", record["record_kind"], digest
    )
    if record.get("record_digest") != digest or record.get("record_id") != expected_id:
        raise ContractError("portable materializer record identity is invalid")


def _header_identity_material(header: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in header.items()
        if key not in {"header_id", "header_digest"}
    }


def _seal_header(header: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(header))
    value.pop("header_id", None)
    value.pop("header_digest", None)
    value["header_id"] = stable_identifier(
        "portable-causal-materializer-header-v3",
        value["header_kind"],
        canonical_digest(value),
    )
    return seal_content_object_header(value)


def _verify_header_identity(header: Mapping[str, Any]) -> None:
    expected_id = stable_identifier(
        "portable-causal-materializer-header-v3",
        header["header_kind"],
        canonical_digest(_header_identity_material(header)),
    )
    if header.get("header_id") != expected_id:
        raise ContractError("portable materializer header identity is invalid")


def _component_id(entry: Mapping[str, Any]) -> str:
    return stable_identifier(
        "portable-causal-materializer-dependency-component-v3",
        canonical_digest(dict(entry)),
    )


def _dependency_projection(
    dependency: Mapping[str, Any], *, snapshot_digest: str
) -> dict[str, Any]:
    """Replace source paths with committed component identities and commitments."""

    entries = [copy.deepcopy(dict(row)) for row in dependency["entries"]]
    if not entries or len(entries) > MAX_PORTABLE_DEPENDENCY_COMPONENTS:
        raise ContractError("materializer dependency closure exceeds its portable ceiling")
    by_path: dict[str, str] = {}
    components: list[dict[str, Any]] = []
    for entry in entries:
        path = entry["path"]
        if path in by_path:
            raise ContractError("materializer dependency closure repeats a source path")
        component_id = _component_id(entry)
        by_path[path] = component_id
        components.append(
            {
                "component_id": component_id,
                "source_entry_commitment": canonical_digest(entry),
                "roles": list(entry["roles"]),
                "byte_size": entry["byte_size"],
                "content_digest": entry["content_digest"],
            }
        )

    def component_for(path: str, label: str) -> str:
        try:
            return by_path[path]
        except KeyError as exc:
            raise ContractError(f"portable dependency {label} lacks a closed component") from exc

    roots: list[dict[str, Any]] = []
    for raw_root in dependency["declared_roots"]:
        root = copy.deepcopy(dict(raw_root))
        commitment = canonical_digest(root)
        roots.append(
            {
                "root_id": stable_identifier(
                    "portable-causal-materializer-dependency-root-v3", commitment
                ),
                "source_root_commitment": commitment,
                "kind": root["kind"],
                "roles": list(root["roles"]),
                "component_id": component_for(root["path"], "declared root"),
            }
        )
    schema_closure = dependency["schema_closure"]
    import_boundary = dependency["import_boundary"]
    return _seal_record(
        {
            "schema_version": "3.0.0",
            "contract_version": "causal-byte-materializer-portable-dependency/3.0.0",
            "record_kind": DEPENDENCY_KIND,
            "source_snapshot_digest": snapshot_digest,
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "source_dependency_authority_digest": dependency["content_digest"],
            "scope": dependency["scope"],
            "source_authority_boundary": dependency["authority_boundary"],
            "declared_roots": roots,
            "components": components,
            "schema_closure": {
                "literal_component_ids": [
                    component_for(path, "literal schema")
                    for path in schema_closure["literal_paths"]
                ],
                "referenced_component_ids": [
                    component_for(path, "referenced schema")
                    for path in schema_closure["referenced_paths"]
                ],
            },
            "import_boundary": {
                "policy": import_boundary["policy"],
                "repository_local_python_component_ids": [
                    component_for(path, "repository-local import")
                    for path in import_boundary["repository_local_python_paths"]
                ],
                "stdlib_modules": list(import_boundary["stdlib_modules"]),
                "third_party_modules": list(import_boundary["third_party_modules"]),
            },
            "runtime_dependencies": copy.deepcopy(dependency["runtime_dependencies"]),
        }
    )


def _portable_request(
    *,
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    artifact_ref: Mapping[str, Any],
) -> dict[str, Any]:
    source = snapshot.request
    binding = snapshot.binding
    return _seal_record(
        {
            "schema_version": "3.0.0",
            "contract_version": "causal-byte-materializer-portable-request/3.0.0",
            "record_kind": REQUEST_KIND,
            "source_snapshot_digest": snapshot.snapshot_digest,
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "source_request_id": source["request_id"],
            "source_request_digest": source["request_digest"],
            "invocation_id": source["invocation_id"],
            "operator": copy.deepcopy(source["operator"]),
            "identity": copy.deepcopy(source["identity"]),
            "required": source["required"],
            "requested_at": source["requested_at"],
            "parameters": copy.deepcopy(source["parameters"]),
            "artifact_ref": copy.deepcopy(dict(artifact_ref)),
            "declared_artifact_id": binding["artifact_id"],
            "declared_artifact_digest": binding["artifact_digest"],
        }
    )


def _portable_attempt(
    *,
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    source: Mapping[str, Any],
    request_ref: Mapping[str, Any],
    artifact_ref: Mapping[str, Any],
) -> dict[str, Any]:
    return _seal_record(
        {
            "schema_version": "3.0.0",
            "contract_version": "causal-byte-materializer-portable-attempt/3.0.0",
            "record_kind": ATTEMPT_KIND,
            "source_snapshot_digest": snapshot.snapshot_digest,
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "source_receipt_id": source["receipt_id"],
            "source_receipt_digest": source["receipt_digest"],
            "request_ref": copy.deepcopy(dict(request_ref)),
            "artifact_ref": copy.deepcopy(dict(artifact_ref)),
            "request_id": source["request_id"],
            "request_digest": source["request_digest"],
            "invocation_id": source["invocation_id"],
            "attempt": source["attempt"],
            "operator": copy.deepcopy(source["operator"]),
            "started_at": source["started_at"],
            "completed_at": source["completed_at"],
            "duration_seconds": source["duration_seconds"],
            "status": source["status"],
            "exit_code": source["exit_code"],
            "stdout_digest": source["stdout_digest"],
            "stderr_digest": source["stderr_digest"],
            "validator": copy.deepcopy(source["validator"]),
            "error": copy.deepcopy(source["error"]),
            "materialized_copy_status": (
                "exact_input_output_history_alias_verified"
                if source["status"] == "succeeded"
                else "not_available"
            ),
        }
    )


def _portable_clock(
    *,
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    request_ref: Mapping[str, Any],
    successful_receipt_ref: Mapping[str, Any],
) -> dict[str, Any]:
    source = snapshot.clock
    return _seal_record(
        {
            "schema_version": "3.0.0",
            "contract_version": "causal-byte-materializer-portable-clock/3.0.0",
            "record_kind": CLOCK_KIND,
            "source_snapshot_digest": snapshot.snapshot_digest,
            "semantic_authorship": False,
            "authority_boundary": LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
            "source_clock_id": source["clock_id"],
            "source_clock_digest": source["clock_digest"],
            "clock_authority_id": source["clock_authority_id"],
            "invocation_id": source["invocation_id"],
            "request_ref": copy.deepcopy(dict(request_ref)),
            "successful_receipt_ref": copy.deepcopy(dict(successful_receipt_ref)),
            "requested_at": source["requested_at"],
            "started_at": source["started_at"],
            "completed_at": source["completed_at"],
            "sealed_at": source["sealed_at"],
            "ordering_verified": source["ordering_verified"],
        }
    )


def _evidence_header(
    *,
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    evidence_kind: str,
    payload_refs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    binding = snapshot.binding
    return _seal_header(
        {
            "schema_version": "3.0.0",
            "contract_version": "causal-byte-materializer-portable-evidence-header/3.0.0",
            "header_kind": EVIDENCE_HEADER_KIND,
            "source_snapshot_digest": snapshot.snapshot_digest,
            "semantic_authorship": False,
            "authority_boundary": dict(HEADER_AUTHORITY_BOUNDARY),
            "evidence_authority_id": binding["evidence_authority_id"],
            "stage_id": binding["stage_id"],
            "materializer_role": binding["materializer_role"],
            "identity": copy.deepcopy(binding["identity"]),
            "evidence_kind": evidence_kind,
            "evidence_payload_refs": [copy.deepcopy(dict(ref)) for ref in payload_refs],
            "successful_attempt": (
                binding["successful_attempt"]
                if evidence_kind == "attempt_receipts"
                else None
            ),
        }
    )


def _binding_header(
    *,
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    dependency_ref: Mapping[str, Any],
    headers: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    binding = snapshot.binding
    value: dict[str, Any] = {
        "schema_version": "3.0.0",
        "contract_version": "causal-byte-materializer-portable-binding-header/3.0.0",
        "header_kind": BINDING_HEADER_KIND,
        "source_snapshot_digest": snapshot.snapshot_digest,
        "semantic_authorship": False,
        "authority_boundary": dict(HEADER_AUTHORITY_BOUNDARY),
        "source_binding_id": binding["binding_id"],
        "source_binding_digest": binding["binding_digest"],
        "capability_kind": binding["capability_kind"],
        "materialization_semantics": binding["materialization_semantics"],
        "local_protocol_valid": binding["local_protocol_valid"],
        "evidence_authority_id": binding["evidence_authority_id"],
        "stage_id": binding["stage_id"],
        "materializer_role": binding["materializer_role"],
        "artifact_id": binding["artifact_id"],
        "artifact_digest": binding["artifact_digest"],
        "identity": copy.deepcopy(binding["identity"]),
        "invocation_id": binding["invocation_id"],
        "dependency_record_ref": copy.deepcopy(dict(dependency_ref)),
        "successful_attempt": binding["successful_attempt"],
        "artifact_alias_policy": "one_content_object_for_verified_staged_output_history_bytes",
        "ceilings": copy.deepcopy(binding["ceilings"]),
    }
    for evidence_kind, field in ROOT_EVIDENCE_FIELDS.items():
        value[field] = copy.deepcopy(dict(headers[evidence_kind]))
    return _seal_header(value)


def _path_prefix(raw: str, *, snapshot_digest: str) -> str:
    if not isinstance(raw, str) or not raw:
        raise ContractError("portable materializer object prefix must be nonempty")
    prefix = safe_relative_path(raw).as_posix()
    if prefix != raw or len(prefix.encode("utf-8")) > MAX_PORTABLE_PREFIX_BYTES:
        raise ContractError("portable materializer object prefix is not canonical and bounded")
    token = snapshot_digest.removeprefix("sha256:")[:24]
    return f"{prefix}/materialization-{token}"


def _contains_source_locator(value: Any, source_paths: frozenset[str]) -> bool:
    if isinstance(value, Mapping):
        return any(
            key == "path"
            or _contains_source_locator(child, source_paths)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(_contains_source_locator(child, source_paths) for child in value)
    return isinstance(value, str) and value in source_paths


def prepare_portable_causal_materialization_fragment_v3(
    snapshot: VerifiedCausalMaterializationSnapshotV3,
    *,
    object_path_prefix: str,
) -> PreparedPortableCausalMaterializationFragmentV3:
    """Compile one verified local seal into a mergeable, path-free DAG fragment."""

    verified = revalidate_causal_materialization_snapshot_v3(snapshot)
    prefix = _path_prefix(object_path_prefix, snapshot_digest=verified.snapshot_digest)

    artifact = prepare_content_object(
        object_kind=ARTIFACT_KIND,
        value=verified.staged_input,
        path=f"{prefix}/artifact.json",
    )
    request_value = _portable_request(snapshot=verified, artifact_ref=artifact.ref)
    request = prepare_content_object(
        object_kind=REQUEST_KIND,
        value=request_value,
        path=f"{prefix}/request.json",
    )

    attempts: list[PreparedContentObject] = []
    for source in verified.attempt_receipts:
        attempt_value = _portable_attempt(
            snapshot=verified,
            source=source,
            request_ref=request.ref,
            artifact_ref=artifact.ref,
        )
        attempts.append(
            prepare_content_object(
                object_kind=ATTEMPT_KIND,
                value=attempt_value,
                path=f"{prefix}/attempt-{source['attempt']:02d}.json",
            )
        )
    successful = attempts[-1]

    clock_value = _portable_clock(
        snapshot=verified,
        request_ref=request.ref,
        successful_receipt_ref=successful.ref,
    )
    clock = prepare_content_object(
        object_kind=CLOCK_KIND,
        value=clock_value,
        path=f"{prefix}/clock.json",
    )
    dependency_value = _dependency_projection(
        verified.binding["dependency_authority"],
        snapshot_digest=verified.snapshot_digest,
    )
    dependency = prepare_content_object(
        object_kind=DEPENDENCY_KIND,
        value=dependency_value,
        path=f"{prefix}/dependency.json",
    )

    header_payloads: dict[str, Sequence[Mapping[str, Any]]] = {
        "staged_input": (artifact.ref,),
        "producer_request": (request.ref,),
        "attempt_receipts": tuple(row.ref for row in attempts),
        "producer_artifact": (artifact.ref,),
        "immutable_history": (artifact.ref,),
        "governed_clock": (clock.ref,),
    }
    headers: dict[str, PreparedContentObject] = {}
    for evidence_kind in EVIDENCE_KINDS:
        value = _evidence_header(
            snapshot=verified,
            evidence_kind=evidence_kind,
            payload_refs=header_payloads[evidence_kind],
        )
        headers[evidence_kind] = prepare_content_object(
            object_kind=EVIDENCE_HEADER_KIND,
            value=value,
            path=f"{prefix}/header-{evidence_kind.replace('_', '-')}.json",
        )
    root_value = _binding_header(
        snapshot=verified,
        dependency_ref=dependency.ref,
        headers={kind: headers[kind].ref for kind in EVIDENCE_KINDS},
    )
    root = prepare_content_object(
        object_kind=BINDING_HEADER_KIND,
        value=root_value,
        path=f"{prefix}/binding-root.json",
    )

    ordered_objects = (
        dependency,
        artifact,
        request,
        *attempts,
        clock,
        *(headers[kind] for kind in EVIDENCE_KINDS),
        root,
    )
    if len(ordered_objects) > MAX_PORTABLE_FRAGMENT_OBJECTS:
        raise ContractError("portable materializer fragment exceeds its object ceiling")
    total_bytes = sum(len(row.data) for row in ordered_objects)
    if total_bytes > MAX_PORTABLE_FRAGMENT_BYTES:
        raise ContractError("portable materializer fragment exceeds its byte ceiling")

    # Protocol values must not retain active workspace locators.  The opaque
    # scientific artifact is deliberately excluded: a user payload may itself
    # discuss a domain concept named ``path`` without becoming a locator.
    source_paths = frozenset(verified.captured_ref_paths)
    for row in ordered_objects:
        if row is artifact:
            continue
        if _contains_source_locator(row.value, source_paths):
            raise ContractError("portable materializer protocol retained a source locator")

    edges: list[dict[str, str]] = []
    for row in ordered_objects:
        edges.extend(derive_content_object_edges(object_ref=row.ref, payload=row.value))
    validate_payload_derived_edges(
        objects=tuple((row.ref, row.value) for row in ordered_objects),
        declared_edges=edges,
    )
    order = tuple(str(row.ref["object_id"]) for row in ordered_objects)
    positions = {object_id: index for index, object_id in enumerate(order)}
    if any(
        positions[edge["source_object_id"]] >= positions[edge["target_object_id"]]
        for edge in edges
    ):
        raise ContractError("portable materializer fragment is not dependency-first")

    return PreparedPortableCausalMaterializationFragmentV3(
        snapshot_digest=verified.snapshot_digest,
        _objects=tuple(
            _SealedFragmentObject(
                object_kind=str(row.ref["object_kind"]),
                path=str(row.descriptor["path"]),
                data=bytes(row.data),
            )
            for row in ordered_objects
        ),
        _edge_data=tuple(canonical_json(edge) for edge in edges),
        _topological_order=order,
        _binding_root_ref_data=canonical_json(root.ref),
        _successful_receipt_ref_data=canonical_json(successful.ref),
    )


def _parse_utc(raw: Any) -> dt.datetime:
    if not isinstance(raw, str):
        raise ContractError("portable materializer timestamp is not a string")
    try:
        value = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("portable materializer timestamp is invalid") from exc
    if value.tzinfo is None:
        raise ContractError("portable materializer timestamp lacks a timezone")
    return value.astimezone(dt.UTC)


def _verify_dependency_projection(record: Mapping[str, Any]) -> None:
    components = record["components"]
    component_ids: set[str] = set()
    for component in components:
        expected = stable_identifier(
            "portable-causal-materializer-dependency-component-v3",
            component["source_entry_commitment"],
        )
        if component["component_id"] != expected or expected in component_ids:
            raise ContractError("portable dependency component identity is invalid")
        component_ids.add(expected)
    for root in record["declared_roots"]:
        expected = stable_identifier(
            "portable-causal-materializer-dependency-root-v3",
            root["source_root_commitment"],
        )
        if root["root_id"] != expected or root["component_id"] not in component_ids:
            raise ContractError("portable dependency root identity is invalid")
    referenced = [
        *record["schema_closure"]["literal_component_ids"],
        *record["schema_closure"]["referenced_component_ids"],
        *record["import_boundary"]["repository_local_python_component_ids"],
    ]
    if any(component_id not in component_ids for component_id in referenced):
        raise ContractError("portable dependency relation names an absent component")


def validate_portable_causal_materialization_closure_v3(
    objects: Sequence[ResolvedContentObject],
    binding_root_ref: Mapping[str, Any],
) -> VerifiedPortableCausalMaterializationV3:
    """Replay one portable binding solely from store-verified content objects.

    ``objects`` may be the complete closure of a larger world graph.  Only the
    exact objects reachable from ``binding_root_ref`` are consumed; unrelated
    world objects cannot strengthen or change byte-materialization authority.
    """

    if isinstance(objects, (str, bytes)) or not isinstance(objects, Sequence):
        raise ContractError("portable materializer closure must be a sequence")
    by_id: dict[str, ResolvedContentObject] = {}
    for resolved in objects:
        if type(resolved) is not ResolvedContentObject:
            raise ContractError("portable closure requires exact resolved objects")
        # A store resolver already supplies this invariant, but replay remains
        # fail-closed when called directly: a caller cannot pair a valid ref and
        # decoded value with different raw bytes and thereby counterfeit the
        # staged/output/history alias proof.
        if (
            type(resolved.data) is not bytes
            or canonical_json(dict(resolved.value)) != resolved.data
        ):
            raise ContractError(
                "portable closure resolved bytes differ from their canonical value"
            )
        object_id = str(resolved.ref["object_id"])
        if object_id in by_id:
            raise ContractError("portable closure repeats a content object")
        by_id[object_id] = resolved

    consumed: list[str] = []

    def resolve(raw_ref: Mapping[str, Any], expected_kind: str) -> ResolvedContentObject:
        ref = copy.deepcopy(dict(raw_ref))
        if ref.get("object_kind") != expected_kind:
            raise ContractError("portable closure reference names the wrong object kind")
        try:
            resolved = by_id[str(ref["object_id"])]
        except KeyError as exc:
            raise ContractError("portable closure lacks a referenced object") from exc
        if dict(resolved.ref) != ref:
            raise ContractError("portable closure object differs from its exact ref")
        validate_role_bound_object(ref, resolved.value)
        if ref["object_id"] not in consumed:
            consumed.append(str(ref["object_id"]))
        return resolved

    root_resolved = resolve(binding_root_ref, BINDING_HEADER_KIND)
    root = copy.deepcopy(dict(root_resolved.value))
    _verify_header_identity(root)
    if root["semantic_authorship"] is not False or root["local_protocol_valid"] is not True:
        raise ContractError("portable binding root exceeds local byte-copy authority")
    if root["ceilings"] != CEILINGS:
        raise ContractError("portable binding root ceilings drifted")

    dependency_resolved = resolve(root["dependency_record_ref"], DEPENDENCY_KIND)
    dependency = copy.deepcopy(dict(dependency_resolved.value))
    _verify_record_identity(dependency)
    _verify_dependency_projection(dependency)

    headers: dict[str, tuple[dict[str, Any], list[ResolvedContentObject]]] = {}
    expected_common = {
        "source_snapshot_digest": root["source_snapshot_digest"],
        "evidence_authority_id": root["evidence_authority_id"],
        "stage_id": root["stage_id"],
        "materializer_role": root["materializer_role"],
        "identity": root["identity"],
    }
    expected_payload_kind = {
        "staged_input": ARTIFACT_KIND,
        "producer_request": REQUEST_KIND,
        "attempt_receipts": ATTEMPT_KIND,
        "producer_artifact": ARTIFACT_KIND,
        "immutable_history": ARTIFACT_KIND,
        "governed_clock": CLOCK_KIND,
    }
    for evidence_kind in EVIDENCE_KINDS:
        header_ref = root[ROOT_EVIDENCE_FIELDS[evidence_kind]]
        header_resolved = resolve(header_ref, EVIDENCE_HEADER_KIND)
        header = copy.deepcopy(dict(header_resolved.value))
        _verify_header_identity(header)
        if header["evidence_kind"] != evidence_kind or any(
            header[key] != expected for key, expected in expected_common.items()
        ):
            raise ContractError("portable evidence header crosses a binding boundary")
        payloads = [
            resolve(ref, expected_payload_kind[evidence_kind])
            for ref in header["evidence_payload_refs"]
        ]
        headers[evidence_kind] = (header, payloads)

    artifact_rows = [
        headers[kind][1][0]
        for kind in ("staged_input", "producer_artifact", "immutable_history")
    ]
    artifact_ref = dict(artifact_rows[0].ref)
    if any(dict(row.ref) != artifact_ref or row.data != artifact_rows[0].data for row in artifact_rows):
        raise ContractError("portable staged/output/history evidence is not one exact alias")
    artifact = copy.deepcopy(dict(artifact_rows[0].value))
    if canonical_digest(artifact) != root["artifact_digest"]:
        raise ContractError("portable artifact semantic digest differs from its binding")

    request_resolved = headers["producer_request"][1][0]
    request = copy.deepcopy(dict(request_resolved.value))
    _verify_record_identity(request)
    if (
        request["source_snapshot_digest"] != root["source_snapshot_digest"]
        or request["artifact_ref"] != artifact_ref
        or request["invocation_id"] != root["invocation_id"]
        or request["identity"] != root["identity"]
        or request["parameters"]["causal_stage_id"] != root["stage_id"]
        or request["parameters"]["materializer_role"] != root["materializer_role"]
        or request["parameters"]["artifact_id"] != root["artifact_id"]
        or request["parameters"]["artifact_digest"] != root["artifact_digest"]
        or request["parameters"]["evidence_authority_id"] != root["evidence_authority_id"]
        or request["declared_artifact_id"] != root["artifact_id"]
        or request["declared_artifact_digest"] != root["artifact_digest"]
    ):
        raise ContractError("portable request differs from its binding root")

    receipt_header, receipt_rows = headers["attempt_receipts"]
    attempts = [copy.deepcopy(dict(row.value)) for row in receipt_rows]
    if (
        len(attempts) != root["successful_attempt"]
        or receipt_header["successful_attempt"] != len(attempts)
        or [row["attempt"] for row in attempts] != list(range(1, len(attempts) + 1))
        or [row["status"] for row in attempts].count("succeeded") != 1
        or attempts[-1]["status"] != "succeeded"
    ):
        raise ContractError("portable attempt history is not contiguous and terminal")
    for index, attempt in enumerate(attempts, start=1):
        _verify_record_identity(attempt)
        expected_copy = (
            "exact_input_output_history_alias_verified"
            if index == len(attempts)
            else "not_available"
        )
        if (
            attempt["source_snapshot_digest"] != root["source_snapshot_digest"]
            or attempt["request_ref"] != dict(request_resolved.ref)
            or attempt["artifact_ref"] != artifact_ref
            or attempt["request_id"] != request["source_request_id"]
            or attempt["request_digest"] != request["source_request_digest"]
            or attempt["invocation_id"] != root["invocation_id"]
            or attempt["materialized_copy_status"] != expected_copy
        ):
            raise ContractError("portable attempt crosses request or artifact boundaries")

    clock_resolved = headers["governed_clock"][1][0]
    clock = copy.deepcopy(dict(clock_resolved.value))
    _verify_record_identity(clock)
    successful_ref = dict(receipt_rows[-1].ref)
    if (
        clock["source_snapshot_digest"] != root["source_snapshot_digest"]
        or clock["request_ref"] != dict(request_resolved.ref)
        or clock["successful_receipt_ref"] != successful_ref
        or clock["invocation_id"] != root["invocation_id"]
    ):
        raise ContractError("portable clock crosses request or receipt boundaries")
    ordered_times = [
        _parse_utc(clock[field])
        for field in ("requested_at", "started_at", "completed_at", "sealed_at")
    ]
    if ordered_times != sorted(ordered_times):
        raise ContractError("portable governed clock is out of order")

    if (
        dependency["source_snapshot_digest"] != root["source_snapshot_digest"]
        or dependency["source_dependency_authority_digest"]
        != request["parameters"]["dependency_authority_digest"]
        or dependency["source_authority_boundary"] != DEPENDENCY_AUTHORITY_BOUNDARY
    ):
        raise ContractError("portable dependency record differs from request authority")

    protocol_values = [root, dependency, request, *attempts, clock]
    protocol_values.extend(header for header, _payloads in headers.values())
    if any(_contains_source_locator(value, frozenset()) for value in protocol_values):
        raise ContractError("portable materializer closure contains an active path field")

    return VerifiedPortableCausalMaterializationV3(
        source_snapshot_digest=root["source_snapshot_digest"],
        successful_attempt=root["successful_attempt"],
        consumed_object_ids=tuple(consumed),
        _binding_root_ref_data=canonical_json(dict(binding_root_ref)),
        _artifact_ref_data=canonical_json(artifact_ref),
        _request_ref_data=canonical_json(dict(request_resolved.ref)),
        _attempt_ref_data=tuple(canonical_json(dict(row.ref)) for row in receipt_rows),
        _clock_ref_data=canonical_json(dict(clock_resolved.ref)),
    )


__all__ = [
    "ARTIFACT_KIND",
    "ATTEMPT_KIND",
    "BINDING_HEADER_KIND",
    "CLOCK_KIND",
    "DEPENDENCY_KIND",
    "EVIDENCE_HEADER_KIND",
    "MAX_PORTABLE_DEPENDENCY_COMPONENTS",
    "MAX_PORTABLE_FRAGMENT_BYTES",
    "MAX_PORTABLE_FRAGMENT_OBJECTS",
    "PreparedPortableCausalMaterializationFragmentV3",
    "REQUEST_KIND",
    "VerifiedPortableCausalMaterializationV3",
    "prepare_portable_causal_materialization_fragment_v3",
    "validate_portable_causal_materialization_closure_v3",
]
