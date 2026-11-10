# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Atomic publication and verified reopening for immutable content graphs.

This module is deliberately a generic storage kernel.  It assigns no meaning
to content-object kinds, graph edges, roots, or state beyond the structural
contracts needed to publish exactly one graph and all of its locally owned
objects.  Domain runtimes remain responsible for deciding what those objects
mean.

The public flow has three explicit phases:

``prepare_content_graph_transaction``
    freezes canonical state, graph, and object bytes and derives the only
    accepted request/idempotency identity from those bytes;
``commit_content_graph_transaction``
    verifies prior imported owners, then delegates one create-only CAS commit
    to :class:`DiscoveryTransactionStore`;
``reopen_content_graph_transaction``
    reopens the current head under one store-minted byte context, verifies the
    complete graph through :class:`StoreVerifiedContentObjectGraph`, and
    returns only compact commit, graph, and root references.

There are no semantic callbacks or experiment/world special cases.  Imported
handles may name only the exact earlier commit that locally owns their object;
transitive re-export is rejected both before publication and during reopening.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_identifier,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    CompareAndSwapError,
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedArtifactContext,
    VerifiedCommit,
)

from .world_object_graph import (
    MAX_CONTENT_GRAPH_BYTES,
    MAX_CONTENT_GRAPH_TOTAL_OBJECT_BYTES,
    MAX_CONTENT_OBJECT_BYTES,
    MAX_CONTENT_OBJECTS,
    PreparedContentObject,
    build_content_object_descriptor,
    build_content_object_ref,
    validate_content_object_graph,
)
from .world_object_graph_store import (
    StoreVerifiedContentObjectGraph,
    build_content_graph_commit_reference,
)


TRANSACTION_KIND = "content_graph_transaction"
GRAPH_REFERENCE_KIND = "committed_content_object_graph"
IDEMPOTENCY_PREFIX = "content-graph-transaction-v1"

# These are transaction-kernel ceilings, not aliases consulted dynamically by
# ``world_object_graph``.  Keeping explicit bounds here prevents a future graph
# implementation from silently widening the atomic publication surface.
MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS = MAX_CONTENT_OBJECTS
MAX_CONTENT_GRAPH_TRANSACTION_OBJECT_BYTES = MAX_CONTENT_OBJECT_BYTES
MAX_CONTENT_GRAPH_TRANSACTION_GRAPH_BYTES = MAX_CONTENT_GRAPH_BYTES
MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES = MAX_CONTENT_GRAPH_TOTAL_OBJECT_BYTES


@dataclass(frozen=True, slots=True)
class _SealedLocalObject:
    """Immutable descriptor and payload bytes retained by a prepared request."""

    descriptor_data: bytes
    object_data: bytes


@dataclass(frozen=True, slots=True)
class PreparedContentGraphTransaction:
    """A completely frozen, deterministic proposal for one next generation.

    The byte fields are intentionally private.  Public projections decode
    fresh values so mutation of a returned mapping cannot alter the proposal
    later compared or committed.
    """

    expected_generation: int
    namespace: Namespace
    graph_artifact_path: str
    request_digest: str
    idempotency_key: str
    _state_data: bytes
    _graph_data: bytes
    _local_objects: tuple[_SealedLocalObject, ...]

    @property
    def state(self) -> Mapping[str, Any]:
        """Return a fresh copy of the frozen canonical state."""

        return _decode_canonical_mapping(self._state_data, "prepared state")

    @property
    def graph(self) -> Mapping[str, Any]:
        """Return a fresh copy of the frozen canonical graph."""

        return _decode_canonical_mapping(self._graph_data, "prepared graph")

    @property
    def local_objects(self) -> tuple[PreparedContentObject, ...]:
        """Return fresh object wrappers over immutable payload bytes."""

        rows: list[PreparedContentObject] = []
        for sealed in self._local_objects:
            descriptor = _decode_canonical_mapping(
                sealed.descriptor_data, "prepared local descriptor"
            )
            value = _decode_canonical_mapping(
                sealed.object_data, "prepared local object"
            )
            rows.append(
                PreparedContentObject(
                    value=value,
                    data=memoryview(sealed.object_data).tobytes(),
                    ref=copy.deepcopy(descriptor["ref"]),
                    descriptor=descriptor,
                )
            )
        return tuple(rows)


@dataclass(frozen=True, slots=True)
class ContentGraphTransactionResult:
    """Compact, immutable receipt containing references rather than values."""

    request_digest: str
    idempotency_key: str
    _commit_reference_data: bytes
    _graph_reference_data: bytes
    _root_reference_data: tuple[bytes, ...]

    @property
    def commit_reference(self) -> Mapping[str, Any]:
        """Return a fresh portable verified-commit reference."""

        return _decode_canonical_mapping(
            self._commit_reference_data, "content-graph commit reference"
        )

    @property
    def graph_reference(self) -> Mapping[str, Any]:
        """Return a fresh compact graph reference."""

        return _decode_canonical_mapping(
            self._graph_reference_data, "committed content-graph reference"
        )

    @property
    def root_references(self) -> tuple[Mapping[str, Any], ...]:
        """Return fresh path-free references in declared root order."""

        return tuple(
            _decode_canonical_mapping(data, "committed root reference")
            for data in self._root_reference_data
        )

    # Short aliases make the three reference surfaces easy to consume without
    # introducing a second representation.
    @property
    def commit_ref(self) -> Mapping[str, Any]:
        return self.commit_reference

    @property
    def graph_ref(self) -> Mapping[str, Any]:
        return self.graph_reference

    @property
    def root_refs(self) -> tuple[Mapping[str, Any], ...]:
        return self.root_references

    @property
    def generation(self) -> int:
        return int(self.commit_reference["generation"])

    @property
    def commit_id(self) -> str:
        return str(self.commit_reference["commit_id"])

    def as_dict(self) -> dict[str, Any]:
        """Return one wholly defensive JSON-ready projection."""

        return {
            "request_digest": self.request_digest,
            "idempotency_key": self.idempotency_key,
            "commit_reference": self.commit_reference,
            "graph_reference": self.graph_reference,
            "root_references": list(self.root_references),
        }


@dataclass(frozen=True, slots=True)
class _AuditedGraphSnapshot:
    """Minimal ownership index for one context-verified historical graph."""

    generation: int
    graph_path: str
    local_refs: Mapping[str, Mapping[str, Any]]
    imported_handles: tuple[Mapping[str, Any], ...]


def _copy_mapping(value: Mapping[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{label} must be an object")
    return copy.deepcopy(dict(value))


def _decode_canonical_mapping(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise ContractError(f"{label} must be immutable bytes")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise ContractError(f"{label} is not one canonical JSON object")
    return value


def _decode_committed_mapping(data: bytes, label: str) -> dict[str, Any]:
    try:
        return _decode_canonical_mapping(data, label)
    except ContractError as exc:
        raise StateCorruptionError(str(exc)) from exc


def _canonical_branch_path(raw: Any, namespace: Namespace, label: str) -> str:
    if not isinstance(raw, str):
        raise ContractError(f"{label} must be a string")
    relative = safe_relative_path(raw)
    canonical = relative.as_posix()
    if canonical != raw:
        raise ContractError(f"{label} is not canonical: {raw!r}")
    required_prefix = Path("branches") / namespace.branch_id
    try:
        relative.relative_to(required_prefix)
    except ValueError as exc:
        raise ContractError(
            f"{label} must be branch-local under {required_prefix}: {raw!r}"
        ) from exc
    return canonical


def _validate_expected_generation(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContractError("expected_generation must be a non-negative integer")
    return value


def _extract_supplied_identity(
    prepared: PreparedContentObject,
) -> tuple[str, str]:
    try:
        object_id = prepared.descriptor["ref"]["object_id"]
        path = prepared.descriptor["path"]
    except (KeyError, TypeError) as exc:
        raise ContractError("prepared local object has no complete descriptor") from exc
    if not isinstance(object_id, str) or not isinstance(path, str):
        raise ContractError("prepared local object descriptor identity is malformed")
    return object_id, path


def _normalize_local_object(
    prepared: PreparedContentObject,
    *,
    namespace: Namespace,
) -> tuple[dict[str, Any], bytes, bytes]:
    """Rebuild one caller-supplied prepared object from its exact bytes."""

    if type(prepared) is not PreparedContentObject:
        raise ContractError("local objects must be exact PreparedContentObject values")
    if type(prepared.data) is not bytes or not prepared.data:
        raise ContractError("prepared local object bytes must be nonempty bytes")
    data = memoryview(prepared.data).tobytes()
    if len(data) > MAX_CONTENT_GRAPH_TRANSACTION_OBJECT_BYTES:
        raise ContractError(
            "prepared local object exceeds the transaction object-byte ceiling"
        )
    value = _copy_mapping(prepared.value, "prepared local object value")
    if canonical_json(value) != data:
        raise ContractError(
            "prepared local object bytes differ from its canonical value"
        )
    supplied_ref = _copy_mapping(prepared.ref, "prepared local object ref")
    try:
        object_kind = supplied_ref["object_kind"]
    except KeyError as exc:
        raise ContractError("prepared local object ref lacks object_kind") from exc
    rebuilt_ref = build_content_object_ref(
        object_kind=object_kind,
        data=data,
        semantic_value=value,
    )
    if supplied_ref != rebuilt_ref:
        raise ContractError("prepared local object ref is not content-derived")
    supplied_descriptor = _copy_mapping(
        prepared.descriptor, "prepared local object descriptor"
    )
    try:
        path = _canonical_branch_path(
            supplied_descriptor["path"], namespace, "local object path"
        )
    except KeyError as exc:
        raise ContractError("prepared local object descriptor lacks path") from exc
    rebuilt_descriptor = build_content_object_descriptor(ref=rebuilt_ref, path=path)
    if supplied_descriptor != rebuilt_descriptor:
        raise ContractError(
            "prepared local object descriptor differs from its ref and path"
        )
    return rebuilt_descriptor, data, canonical_json(rebuilt_descriptor)


def _expected_artifact_descriptors(
    transaction: PreparedContentGraphTransaction,
) -> list[dict[str, Any]]:
    namespace = transaction.namespace.as_dict()
    descriptors = [
        {
            "path": transaction.graph_artifact_path,
            "sha256": bytes_digest(transaction._graph_data),
            "size_bytes": len(transaction._graph_data),
            "namespace": namespace,
        }
    ]
    for row in transaction._local_objects:
        descriptor = _decode_canonical_mapping(
            row.descriptor_data, "prepared local descriptor"
        )
        descriptors.append(
            {
                "path": descriptor["path"],
                "sha256": bytes_digest(row.object_data),
                "size_bytes": len(row.object_data),
                "namespace": namespace,
            }
        )
    return descriptors


def prepare_content_graph_transaction(
    *,
    expected_generation: int,
    state: Mapping[str, Any],
    namespace: Namespace,
    graph_artifact_path: str,
    graph: Mapping[str, Any],
    local_objects: Sequence[PreparedContentObject],
) -> PreparedContentGraphTransaction:
    """Freeze and validate one exact content-graph publication request."""

    expected = _validate_expected_generation(expected_generation)
    if type(namespace) is not Namespace:
        raise ContractError("content-graph transaction requires an exact Namespace")
    if namespace.state_version != expected:
        raise ContractError(
            "content-graph namespace must be bound to expected_generation"
        )
    state_record = _copy_mapping(state, "content-graph transaction state")
    if (
        state_record.get("target_id") != namespace.target_id
        or state_record.get("run_id") != namespace.run_id
        or state_record.get("generation") != expected + 1
    ):
        raise ContractError(
            "state target/run and next generation must match the transaction namespace"
        )
    validate_identifier(state_record.get("programme_id"), "programme_id")
    state_data = canonical_json(state_record)
    graph_path = _canonical_branch_path(
        graph_artifact_path, namespace, "graph artifact path"
    )

    if isinstance(local_objects, (str, bytes)) or not isinstance(
        local_objects, Sequence
    ):
        raise ContractError("local_objects must be a sequence")
    supplied = tuple(local_objects)
    if len(supplied) > MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS:
        raise ContractError(
            "content-graph transaction exceeds the fixed object-count ceiling"
        )
    supplied_ids: list[str] = []
    supplied_paths: list[str] = []
    for row in supplied:
        if type(row) is not PreparedContentObject:
            raise ContractError(
                "local objects must be exact PreparedContentObject values"
            )
        object_id, path = _extract_supplied_identity(row)
        supplied_ids.append(object_id)
        supplied_paths.append(path)
    if len(set(supplied_ids)) != len(supplied_ids):
        raise ContractError("prepared local object IDs must be unique")
    if len(set(supplied_paths)) != len(supplied_paths):
        raise ContractError("prepared local object paths must be unique")

    graph_record = validate_content_object_graph(graph)
    graph_data = canonical_json(graph_record)
    if len(graph_data) > MAX_CONTENT_GRAPH_TRANSACTION_GRAPH_BYTES:
        raise ContractError(
            "content-graph transaction exceeds the fixed graph-byte ceiling"
        )
    graph_object_count = len(graph_record["local_descriptors"]) + len(
        graph_record["imported_handles"]
    )
    if graph_object_count > MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS:
        raise ContractError(
            "content-graph transaction exceeds the fixed object-count ceiling"
        )

    supplied_by_id = dict(zip(supplied_ids, supplied, strict=True))
    graph_local_ids = [
        descriptor["ref"]["object_id"]
        for descriptor in graph_record["local_descriptors"]
    ]
    missing = sorted(set(graph_local_ids) - set(supplied_by_id))
    extra = sorted(set(supplied_by_id) - set(graph_local_ids))
    if missing:
        raise ContractError(f"graph local object is missing: {missing[0]}")
    if extra:
        raise ContractError(f"undeclared local object was supplied: {extra[0]}")

    sealed: list[_SealedLocalObject] = []
    total_bytes = len(state_data) + len(graph_data)
    for graph_descriptor in graph_record["local_descriptors"]:
        object_id = graph_descriptor["ref"]["object_id"]
        rebuilt_descriptor, data, descriptor_data = _normalize_local_object(
            supplied_by_id[object_id], namespace=namespace
        )
        if rebuilt_descriptor != graph_descriptor:
            raise ContractError(
                f"supplied local object differs from graph descriptor: {object_id}"
            )
        if rebuilt_descriptor["path"] == graph_path:
            raise ContractError("graph artifact path collides with a local object path")
        sealed.append(
            _SealedLocalObject(
                descriptor_data=descriptor_data,
                object_data=data,
            )
        )
        total_bytes += len(data)
    if total_bytes > MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES:
        raise ContractError(
            "content-graph transaction exceeds the fixed total commit-byte ceiling"
        )

    artifact_identity = [
        {
            "path": graph_path,
            "sha256": bytes_digest(graph_data),
            "size_bytes": len(graph_data),
            "graph_digest": graph_record["graph_digest"],
        },
        *(
            {
                "path": descriptor["path"],
                "sha256": bytes_digest(row.object_data),
                "size_bytes": len(row.object_data),
                "object_ref": descriptor["ref"],
            }
            for row, descriptor in (
                (
                    sealed_row,
                    _decode_canonical_mapping(
                        sealed_row.descriptor_data, "prepared local descriptor"
                    ),
                )
                for sealed_row in sealed
            )
        ),
    ]
    identity_material = {
        "schema_version": "1.0.0",
        "transaction_kind": TRANSACTION_KIND,
        "expected_generation": expected,
        "namespace": namespace.as_dict(),
        "state": {
            "sha256": bytes_digest(state_data),
            "size_bytes": len(state_data),
            "semantic_digest": canonical_digest(state_record),
        },
        "artifacts": artifact_identity,
    }
    request_digest = canonical_digest(identity_material)
    idempotency_key = stable_identifier(
        IDEMPOTENCY_PREFIX,
        namespace.target_id,
        namespace.run_id,
        namespace.branch_id,
        expected,
        request_digest,
    )
    return PreparedContentGraphTransaction(
        expected_generation=expected,
        namespace=namespace,
        graph_artifact_path=graph_path,
        request_digest=request_digest,
        idempotency_key=idempotency_key,
        _state_data=state_data,
        _graph_data=graph_data,
        _local_objects=tuple(sealed),
    )


def _revalidate_prepared(
    transaction: PreparedContentGraphTransaction,
) -> PreparedContentGraphTransaction:
    if type(transaction) is not PreparedContentGraphTransaction:
        raise ContractError(
            "commit requires an exact PreparedContentGraphTransaction"
        )
    rebuilt = prepare_content_graph_transaction(
        expected_generation=transaction.expected_generation,
        state=transaction.state,
        namespace=transaction.namespace,
        graph_artifact_path=transaction.graph_artifact_path,
        graph=transaction.graph,
        local_objects=transaction.local_objects,
    )
    if rebuilt != transaction:
        raise ContractError("prepared content-graph transaction identity was mutated")
    return rebuilt


def _manifest_descriptor(commit: VerifiedCommit, path: str) -> dict[str, Any]:
    matches = [row for row in commit.manifest["artifacts"] if row.get("path") == path]
    if len(matches) != 1:
        raise StateCorruptionError(
            f"verified commit lacks one exact artifact descriptor: {path}"
        )
    return copy.deepcopy(dict(matches[0]))


def _verify_committed_local_object(
    *,
    descriptor: Mapping[str, Any],
    manifest_descriptor: Mapping[str, Any],
    data: bytes,
) -> dict[str, Any]:
    ref = _copy_mapping(descriptor["ref"], "committed local object ref")
    if (
        manifest_descriptor.get("sha256") != ref.get("sha256")
        or manifest_descriptor.get("size_bytes") != ref.get("size_bytes")
        or len(data) != ref.get("size_bytes")
        or bytes_digest(data) != ref.get("sha256")
    ):
        raise StateCorruptionError(
            "committed local object descriptor differs from verified bytes"
        )
    value = _decode_committed_mapping(data, "committed local object")
    try:
        replayed = build_content_object_ref(
            object_kind=ref["object_kind"], data=data, semantic_value=value
        )
    except (ContractError, KeyError, TypeError) as exc:
        raise StateCorruptionError(
            "committed local object identity cannot be replayed"
        ) from exc
    if replayed != ref:
        raise StateCorruptionError(
            "committed local object identity differs from exact bytes"
        )
    return ref


def _audit_historical_graph(
    *,
    context: VerifiedArtifactContext,
    generation: int,
    graph_path: str,
    memo: dict[tuple[int, str], _AuditedGraphSnapshot],
    visiting: set[tuple[int, str]],
) -> _AuditedGraphSnapshot:
    """Audit one historical graph and recursively prove imported ownership."""

    key = (generation, graph_path)
    cached = memo.get(key)
    if cached is not None:
        return cached
    if key in visiting:
        raise StateCorruptionError("historical content graphs contain a cycle")
    visiting.add(key)
    try:
        commit = context.read_commit(generation)
        manifest_paths = context.artifact_paths(generation)
        _same_commit, batch = context.read_artifacts(generation, manifest_paths)
        graph_data = batch.get(graph_path)
        if not isinstance(graph_data, bytes):
            raise StateCorruptionError("historical graph artifact is absent")
        graph_manifest_descriptor = _manifest_descriptor(commit, graph_path)
        if (
            len(graph_data) != graph_manifest_descriptor.get("size_bytes")
            or bytes_digest(graph_data) != graph_manifest_descriptor.get("sha256")
        ):
            raise StateCorruptionError(
                "historical graph bytes differ from their manifest descriptor"
            )
        decoded = _decode_committed_mapping(graph_data, "historical content graph")
        try:
            graph = validate_content_object_graph(decoded)
        except ContractError as exc:
            raise StateCorruptionError("historical content graph is invalid") from exc
        local_paths = [row["path"] for row in graph["local_descriptors"]]
        if graph_path in local_paths or len(local_paths) != len(set(local_paths)):
            raise StateCorruptionError(
                "historical graph and local object paths are not disjoint"
            )
        expected_paths = {graph_path, *local_paths}
        if set(manifest_paths) != expected_paths or set(batch) != expected_paths:
            raise StateCorruptionError(
                "historical commit is not exactly one graph and its local objects"
            )
        local_refs: dict[str, Mapping[str, Any]] = {}
        for descriptor in graph["local_descriptors"]:
            path = descriptor["path"]
            data = batch.get(path)
            if not isinstance(data, bytes):
                raise StateCorruptionError("historical local object is absent")
            ref = _verify_committed_local_object(
                descriptor=descriptor,
                manifest_descriptor=_manifest_descriptor(commit, path),
                data=data,
            )
            local_refs[ref["object_id"]] = ref
        snapshot = _AuditedGraphSnapshot(
            generation=generation,
            graph_path=graph_path,
            local_refs=local_refs,
            imported_handles=tuple(
                copy.deepcopy(row) for row in graph["imported_handles"]
            ),
        )
        memo[key] = snapshot
        for handle in snapshot.imported_handles:
            _audit_import_handle(
                context=context,
                handle=handle,
                importing_generation=generation,
                memo=memo,
                visiting=visiting,
                candidate=False,
            )
        return snapshot
    finally:
        visiting.discard(key)


def _audit_import_handle(
    *,
    context: VerifiedArtifactContext,
    handle: Mapping[str, Any],
    importing_generation: int,
    memo: dict[tuple[int, str], _AuditedGraphSnapshot],
    visiting: set[tuple[int, str]],
    candidate: bool,
) -> None:
    """Require a handle to name its object's exact prior local owner."""

    try:
        source_reference = _copy_mapping(
            handle["source_commit_reference"], "source commit reference"
        )
        object_ref = _copy_mapping(handle["object_ref"], "imported object ref")
        source_generation = source_reference["generation"]
        source_graph_path = source_reference["graph_artifact"]["path"]
        object_id = object_ref["object_id"]
    except (KeyError, TypeError) as exc:
        error = ContractError if candidate else StateCorruptionError
        raise error("imported object handle is incomplete") from exc
    if (
        isinstance(source_generation, bool)
        or not isinstance(source_generation, int)
        or source_generation <= 0
        or source_generation >= importing_generation
    ):
        error = ContractError if candidate else StateCorruptionError
        raise error("imported object must come from a strictly prior generation")
    source_commit = context.read_commit(source_generation)
    try:
        expected_reference = build_content_graph_commit_reference(
            source_commit,
            programme_id=source_reference["programme_id"],
            graph_artifact_path=source_graph_path,
        )
    except (ContractError, KeyError, TypeError) as exc:
        error = ContractError if candidate else StateCorruptionError
        raise error("imported source commit reference cannot be replayed") from exc
    if source_reference != expected_reference:
        error = ContractError if candidate else StateCorruptionError
        raise error("imported source commit reference is not exact")
    source = _audit_historical_graph(
        context=context,
        generation=source_generation,
        graph_path=source_graph_path,
        memo=memo,
        visiting=visiting,
    )
    owned_ref = source.local_refs.get(object_id)
    if owned_ref is None:
        imported_ids = {
            row["object_ref"]["object_id"] for row in source.imported_handles
        }
        error = ContractError if candidate else StateCorruptionError
        if object_id in imported_ids:
            raise error(
                "import handle names a transitive re-export, not the direct owner"
            )
        raise error("imported object is absent from its declared source graph")
    if owned_ref != object_ref:
        error = ContractError if candidate else StateCorruptionError
        raise error("imported object ref differs from exact local ownership")


def _preflight_imports(
    *,
    store: DiscoveryTransactionStore,
    transaction: PreparedContentGraphTransaction,
) -> None:
    """Validate current CAS position and all imported owners under one lease."""

    with store.verified_artifact_context() as context:
        current = context.current_generation
        allowed = {
            transaction.expected_generation,
            transaction.expected_generation + 1,
        }
        if current not in allowed:
            raise CompareAndSwapError(
                "content-graph preflight is stale: "
                f"expected {transaction.expected_generation} or exact retry head "
                f"{transaction.expected_generation + 1}, current {current}"
            )
        graph = transaction.graph
        memo: dict[tuple[int, str], _AuditedGraphSnapshot] = {}
        visiting: set[tuple[int, str]] = set()
        for handle in graph["imported_handles"]:
            _audit_import_handle(
                context=context,
                handle=handle,
                importing_generation=transaction.expected_generation + 1,
                memo=memo,
                visiting=visiting,
                candidate=True,
            )


def commit_content_graph_transaction(
    *,
    store: DiscoveryTransactionStore,
    transaction: PreparedContentGraphTransaction,
    failpoint: str | None = None,
) -> ContentGraphTransactionResult:
    """Atomically commit one prepared graph and reopen its verified references."""

    if type(store) is not DiscoveryTransactionStore:
        raise ContractError("content-graph commit requires an exact transaction store")
    if failpoint is not None and not isinstance(failpoint, str):
        raise ContractError("content-graph failpoint must be a name, not a callback")
    prepared = _revalidate_prepared(transaction)
    if (
        store.target_id != prepared.namespace.target_id
        or store.run_id != prepared.namespace.run_id
    ):
        raise ContractError("content-graph transaction belongs to a different store")
    _preflight_imports(store=store, transaction=prepared)
    artifacts = [
        CommitArtifact(
            prepared.graph_artifact_path,
            prepared._graph_data,
            prepared.namespace,
        ),
        *(
            CommitArtifact(
                _decode_canonical_mapping(
                    row.descriptor_data, "prepared local descriptor"
                )["path"],
                row.object_data,
                prepared.namespace,
            )
            for row in prepared._local_objects
        ),
    ]
    committed = store.commit(
        expected_generation=prepared.expected_generation,
        state=prepared.state,
        artifacts=artifacts,
        idempotency_key=prepared.idempotency_key,
        request_digest=prepared.request_digest,
        failpoint=failpoint,
    )
    if committed.generation != prepared.expected_generation + 1:
        raise StateCorruptionError(
            "content-graph commit returned an unexpected generation"
        )
    reopened = reopen_content_graph_transaction(
        store=store,
        generation=committed.generation,
        graph_artifact_path=prepared.graph_artifact_path,
    )
    if (
        reopened.request_digest != prepared.request_digest
        or reopened.idempotency_key != prepared.idempotency_key
    ):
        raise StateCorruptionError(
            "reopened content-graph transaction identity differs from preparation"
        )
    return reopened


def _namespace_from_manifest_descriptor(
    descriptor: Mapping[str, Any],
) -> Namespace:
    raw = descriptor.get("namespace")
    if not isinstance(raw, Mapping) or set(raw) != {
        "target_id",
        "run_id",
        "branch_id",
        "state_version",
    }:
        raise StateCorruptionError("graph manifest namespace is not exact")
    try:
        return Namespace.from_mapping(raw)
    except ContractError as exc:
        raise StateCorruptionError("graph manifest namespace is invalid") from exc


def reopen_content_graph_transaction(
    *,
    store: DiscoveryTransactionStore,
    generation: int,
    graph_artifact_path: str,
) -> ContentGraphTransactionResult:
    """Reopen the current committed graph and return reference-only results."""

    if type(store) is not DiscoveryTransactionStore:
        raise ContractError("content-graph reopen requires an exact transaction store")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation <= 0:
        raise ContractError("content-graph generation must be a positive integer")
    if not isinstance(graph_artifact_path, str):
        raise ContractError("graph artifact path must be a string")
    relative = safe_relative_path(graph_artifact_path)
    if relative.as_posix() != graph_artifact_path:
        raise ContractError("graph artifact path must be canonical")

    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=generation,
            graph_artifact_path=graph_artifact_path,
        )
        resolved_roots = resolver.resolve_roots()
        graph = resolver.graph
        commit = context.read_commit(generation)
        manifest_paths = context.artifact_paths(generation)
        _same_commit, batch = context.read_artifacts(generation, manifest_paths)
        graph_descriptor = _manifest_descriptor(commit, graph_artifact_path)
        namespace = _namespace_from_manifest_descriptor(graph_descriptor)
        if namespace.state_version != generation - 1:
            raise StateCorruptionError(
                "graph namespace is not bound to the exact prior generation"
            )
        local_objects: list[PreparedContentObject] = []
        for descriptor in graph["local_descriptors"]:
            path = descriptor["path"]
            data = batch.get(path)
            if not isinstance(data, bytes):
                raise StateCorruptionError("committed local object is absent")
            value = _decode_committed_mapping(data, "committed local object")
            local_objects.append(
                PreparedContentObject(
                    value=value,
                    data=memoryview(data).tobytes(),
                    ref=copy.deepcopy(descriptor["ref"]),
                    descriptor=copy.deepcopy(descriptor),
                )
            )
        try:
            prepared = prepare_content_graph_transaction(
                expected_generation=generation - 1,
                state=commit.state,
                namespace=namespace,
                graph_artifact_path=graph_artifact_path,
                graph=graph,
                local_objects=local_objects,
            )
        except ContractError as exc:
            raise StateCorruptionError(
                "committed content-graph transaction cannot be reproduced"
            ) from exc
        if list(commit.manifest["artifacts"]) != _expected_artifact_descriptors(
            prepared
        ):
            raise StateCorruptionError(
                "committed artifact vector differs from the transaction kernel"
            )
        if (
            commit.manifest.get("request_digest") != prepared.request_digest
            or commit.manifest.get("idempotency_key") != prepared.idempotency_key
        ):
            raise StateCorruptionError(
                "committed request/idempotency identity is not byte-derived"
            )
        try:
            programme_id = commit.state["programme_id"]
        except KeyError as exc:
            raise StateCorruptionError("committed graph state lacks programme_id") from exc
        commit_reference = build_content_graph_commit_reference(
            commit,
            programme_id=programme_id,
            graph_artifact_path=graph_artifact_path,
        )
        graph_reference = {
            "schema_version": "1.0.0",
            "reference_kind": GRAPH_REFERENCE_KIND,
            "generation": generation,
            "graph_digest": graph["graph_digest"],
            "commit_reference_digest": commit_reference["reference_digest"],
            "graph_artifact": copy.deepcopy(commit_reference["graph_artifact"]),
            "object_count": len(graph["topological_order"]),
            "local_object_count": len(graph["local_descriptors"]),
            "imported_object_count": len(graph["imported_handles"]),
            "ordered_root_object_ids": list(graph["ordered_roots"]),
        }
        root_reference_data = tuple(
            canonical_json(root.ref) for root in resolved_roots
        )
        return ContentGraphTransactionResult(
            request_digest=prepared.request_digest,
            idempotency_key=prepared.idempotency_key,
            _commit_reference_data=canonical_json(commit_reference),
            _graph_reference_data=canonical_json(graph_reference),
            _root_reference_data=root_reference_data,
        )


__all__ = [
    "ContentGraphTransactionResult",
    "GRAPH_REFERENCE_KIND",
    "MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES",
    "MAX_CONTENT_GRAPH_TRANSACTION_GRAPH_BYTES",
    "MAX_CONTENT_GRAPH_TRANSACTION_OBJECT_BYTES",
    "MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS",
    "PreparedContentGraphTransaction",
    "TRANSACTION_KIND",
    "commit_content_graph_transaction",
    "prepare_content_graph_transaction",
    "reopen_content_graph_transaction",
]
