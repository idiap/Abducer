# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Transaction-owned replay for immutable experiment content-object graphs.

``world_object_graph`` defines path-free object identities and a compact DAG,
but its portable filesystem resolver cannot itself prove which discovery commit
owns an object.  This module supplies that authority boundary.  A resolver is
minted from one *live* :class:`VerifiedArtifactContext` and the exact store that
minted it.  It reads graph and object bytes only from the context's already
verified in-memory commit snapshots; it never reopens an artifact pathname.

Every graph commit is deliberately closed: its manifest must contain exactly
one canonical graph document plus the graph's local object descriptors.  An
imported handle must identify a strictly earlier verified commit, that commit's
exact graph artifact, and an object locally owned by that graph.  Re-exporting
the same bytes from another generation is therefore not interchangeable with
the declared lineage.  Public reads recheck the context lease and return fresh
copies, so a closed, stale, cross-store, or caller-mutated resolver has no
authority.

This is storage provenance, not scientific provenance.  It does not establish
semantic derivation, producer authorship, experimental validity, conceptual
merit, physics value, or any theorem claim.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    validate_payload,
)
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedArtifactContext,
    VerifiedCommit,
)

from .world_object_graph import (
    COMMITTED_OBJECT_HANDLE_SCHEMA,
    ResolvedContentObject,
    build_content_object_ref,
    validate_content_object_graph,
)


CONTENT_GRAPH_COMMIT_REFERENCE_SCHEMA = (
    "dynamic_experiment_content_graph_commit_reference_v1.schema.json"
)
# Retain the short public constant for callers of this new module while making
# its value graph-specific.  It no longer names the discovery-transition schema.
COMMIT_REFERENCE_SCHEMA = CONTENT_GRAPH_COMMIT_REFERENCE_SCHEMA
_REFERENCE_KIND = "portable_verified_content_graph_commit"
_GRAPH_ARTIFACT_KIND = "dynamic_experiment_content_object_graph"


def _copy_mapping(value: Mapping[str, Any], label: str) -> dict[str, Any]:
    """Copy one mapping at a trust boundary and reject mapping lookalikes."""

    if not isinstance(value, Mapping):
        raise ContractError(f"{label} must be an object")
    return copy.deepcopy(dict(value))


def _canonical_path(raw: Any, label: str) -> str:
    """Return one canonical safe relative artifact path."""

    if not isinstance(raw, str):
        raise ContractError(f"{label} must be a string")
    path = safe_relative_path(raw).as_posix()
    if path != raw:
        raise ContractError(f"{label} is not canonical: {raw!r}")
    return path


def _self_digest(value: Mapping[str, Any], field: str) -> str:
    material = copy.deepcopy(dict(value))
    material.pop(field, None)
    return canonical_digest(material)


def _theory_projection_digest(state: Mapping[str, Any]) -> str:
    projection = copy.deepcopy(dict(state))
    projection.pop("generation", None)
    return canonical_digest(projection)


def _manifest_descriptor(commit: VerifiedCommit, path: str) -> dict[str, Any]:
    """Select one exact manifest descriptor without trusting a caller index."""

    matches = [row for row in commit.manifest["artifacts"] if row.get("path") == path]
    if len(matches) != 1:
        raise StateCorruptionError(
            f"verified commit lacks one exact graph artifact: {path}"
        )
    return copy.deepcopy(dict(matches[0]))


def build_content_graph_commit_reference(
    commit: VerifiedCommit,
    *,
    programme_id: str,
    graph_artifact_path: str,
) -> dict[str, Any]:
    """Build a graph-specific reference from one exact verified commit.

    A content graph is storage authority, not an experiment transition.  The
    serialized reference therefore names the exact graph artifact directly and
    carries no anchor/observation/aggregation label that could be mistaken for
    domain authority.
    """

    if type(commit) is not VerifiedCommit:
        raise ContractError("content-graph reference requires a VerifiedCommit")
    path = _canonical_path(graph_artifact_path, "graph artifact path")
    descriptor = _manifest_descriptor(commit, path)
    if commit.state.get("programme_id") != programme_id:
        raise ContractError(
            "content-graph reference programme differs from verified commit"
        )
    reference: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reference_kind": _REFERENCE_KIND,
        "programme_id": programme_id,
        "target_id": commit.state["target_id"],
        "run_id": commit.state["run_id"],
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
        "frozen_theory_state_projection_digest": _theory_projection_digest(
            commit.state
        ),
        "graph_artifact": {
            "artifact_kind": _GRAPH_ARTIFACT_KIND,
            "path": path,
            "sha256": descriptor["sha256"],
            "size_bytes": descriptor["size_bytes"],
        },
    }
    reference["reference_digest"] = _self_digest(reference, "reference_digest")
    validate_payload(reference, COMMIT_REFERENCE_SCHEMA)
    return reference


def _validate_commit_reference(
    reference: Mapping[str, Any],
    *,
    commit: VerifiedCommit,
) -> tuple[dict[str, Any], str]:
    """Recompute a serialized reference against one store-verified commit."""

    record = _copy_mapping(reference, "source commit reference")
    validate_payload(record, COMMIT_REFERENCE_SCHEMA)
    graph_path = _canonical_path(
        record["graph_artifact"]["path"], "source graph artifact path"
    )
    if (
        record["reference_kind"] != _REFERENCE_KIND
        or record["graph_artifact"]["artifact_kind"] != _GRAPH_ARTIFACT_KIND
        or record["generation"] != record["prior_generation"] + 1
        or record["reference_digest"]
        != _self_digest(record, "reference_digest")
    ):
        raise StateCorruptionError("source commit reference is not self-consistent")
    expected_identity = (
        commit.state["target_id"],
        commit.state["run_id"],
        commit.generation,
        commit.prior_generation,
        commit.commit_id,
        commit.manifest_digest,
        commit.state_file_digest,
        commit.state_semantic_digest,
        _theory_projection_digest(commit.state),
    )
    observed_identity = (
        record["target_id"],
        record["run_id"],
        record["generation"],
        record["prior_generation"],
        record["commit_id"],
        record["manifest_digest"],
        record["state_file_digest"],
        record["state_semantic_digest"],
        record["frozen_theory_state_projection_digest"],
    )
    if observed_identity != expected_identity:
        raise StateCorruptionError("source commit reference names a different commit")
    if commit.state.get("programme_id") != record["programme_id"]:
        raise StateCorruptionError("source commit reference programme differs")
    descriptor = _manifest_descriptor(commit, graph_path)
    declared = record["graph_artifact"]
    if (
        declared["sha256"] != descriptor["sha256"]
        or declared["size_bytes"] != descriptor["size_bytes"]
    ):
        raise StateCorruptionError("source graph descriptor differs from commit manifest")
    return record, graph_path


def _decode_canonical_object(data: bytes, label: str) -> dict[str, Any]:
    """Decode exact canonical JSON bytes without accepting alternate spellings."""

    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StateCorruptionError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise StateCorruptionError(f"{label} is not one canonical JSON object")
    return value


def _verify_object_bytes(
    ref: Mapping[str, Any], data: bytes, *, label: str
) -> ResolvedContentObject:
    """Recompute every path-free content identity from store-verified bytes."""

    expected = _copy_mapping(ref, f"{label} ref")
    if len(data) != expected["size_bytes"] or bytes_digest(data) != expected["sha256"]:
        raise StateCorruptionError(f"{label} exact bytes differ from its ref")
    value = _decode_canonical_object(data, label)
    if canonical_digest(value) != expected["semantic_digest"]:
        raise StateCorruptionError(f"{label} semantic digest differs from its ref")
    replayed = build_content_object_ref(
        object_kind=expected["object_kind"], data=data, semantic_value=value
    )
    if replayed != expected:
        raise StateCorruptionError(f"{label} content-derived identity differs")
    return ResolvedContentObject(ref=expected, value=value, data=bytes(data))


@dataclass(frozen=True, slots=True)
class _VerifiedGraphSnapshot:
    """One graph and its locally owned objects from a single verified batch."""

    commit: VerifiedCommit
    graph_path: str
    graph: Mapping[str, Any]
    local_objects: Mapping[str, ResolvedContentObject]
    imported_handles: Mapping[str, Mapping[str, Any]]


@dataclass(frozen=True, slots=True)
class StoreVerifiedOwnedContentObject:
    """One resolved object paired with its exact direct owning commit.

    The commit reference is minted or replayed under the same live verified
    artifact context as the object bytes.  It therefore cannot be replaced by
    a caller-authored generation table when a descendant graph is promoted as
    active-current authority.
    """

    resolved: ResolvedContentObject
    owner_commit_reference: Mapping[str, Any]


class StoreVerifiedContentObjectGraph:
    """Resolve one current graph and exact prior owners under a live store lease.

    The constructor requires the active head generation.  Historical graphs are
    reachable only through a committed imported handle, preventing a caller from
    silently treating a stale graph as current authority.  Every public method
    revalidates the exact context/store lease before consulting cached bytes.
    """

    def __init__(
        self,
        *,
        store: DiscoveryTransactionStore,
        context: VerifiedArtifactContext,
        generation: int,
        graph_artifact_path: str,
    ) -> None:
        if type(store) is not DiscoveryTransactionStore:
            raise ContractError("content-graph resolver requires an exact transaction store")
        if type(context) is not VerifiedArtifactContext:
            raise ContractError("content-graph resolver requires a store-minted context")
        context.assert_owned_by(store)
        if generation != context.current_generation:
            raise ContractError("content-graph resolver generation is stale or not current")
        self._store = store
        self._context = context
        self._snapshot_cache: dict[tuple[int, str], _VerifiedGraphSnapshot] = {}
        self._object_cache: dict[
            tuple[int, str, str], ResolvedContentObject
        ] = {}
        self._root = self._load_snapshot(
            generation, _canonical_path(graph_artifact_path, "graph artifact path")
        )

    def _assert_live(self) -> None:
        """Reject closed, copied, cross-thread, or cross-store context use."""

        self._context.assert_owned_by(self._store)

    @staticmethod
    def _defensive(value: ResolvedContentObject) -> ResolvedContentObject:
        return ResolvedContentObject(
            ref=copy.deepcopy(dict(value.ref)),
            value=copy.deepcopy(dict(value.value)),
            data=bytes(value.data),
        )

    def _load_snapshot(self, generation: int, graph_path: str) -> _VerifiedGraphSnapshot:
        """Load a complete graph only from one context-verified artifact batch."""

        self._assert_live()
        key = (generation, graph_path)
        cached = self._snapshot_cache.get(key)
        if cached is not None:
            return cached
        manifest_paths = self._context.artifact_paths(generation)
        commit, batch = self._context.read_artifacts(generation, manifest_paths)
        graph_data = batch.get(graph_path)
        if not isinstance(graph_data, bytes):
            raise StateCorruptionError("committed graph artifact is absent")
        graph_descriptor = _manifest_descriptor(commit, graph_path)
        if (
            len(graph_data) != graph_descriptor["size_bytes"]
            or bytes_digest(graph_data) != graph_descriptor["sha256"]
        ):
            raise StateCorruptionError("committed graph bytes differ from manifest")
        decoded_graph = _decode_canonical_object(
            graph_data, "committed content-object graph"
        )
        if decoded_graph.get("graph_kind") != _GRAPH_ARTIFACT_KIND:
            raise StateCorruptionError(
                "referenced graph artifact is not a valid content-object graph"
            )
        graph = validate_content_object_graph(decoded_graph)
        local_paths = [row["path"] for row in graph["local_descriptors"]]
        if graph_path in local_paths or len(local_paths) != len(set(local_paths)):
            raise StateCorruptionError("graph artifact and local object paths collide")
        expected_paths = {graph_path, *local_paths}
        if set(manifest_paths) != expected_paths or set(batch) != expected_paths:
            raise StateCorruptionError(
                "commit manifest is not exactly one graph and its local objects"
            )
        local_objects: dict[str, ResolvedContentObject] = {}
        for descriptor in graph["local_descriptors"]:
            path = _canonical_path(descriptor["path"], "local object path")
            committed_descriptor = _manifest_descriptor(commit, path)
            ref = descriptor["ref"]
            if (
                committed_descriptor["sha256"] != ref["sha256"]
                or committed_descriptor["size_bytes"] != ref["size_bytes"]
            ):
                raise StateCorruptionError(
                    "local object descriptor differs from commit manifest"
                )
            data = batch.get(path)
            if not isinstance(data, bytes):
                raise StateCorruptionError("local graph object is absent from verified batch")
            resolved = _verify_object_bytes(
                ref, data, label=f"committed content object {ref['object_id']}"
            )
            local_objects[ref["object_id"]] = resolved
        imported = {
            row["object_ref"]["object_id"]: copy.deepcopy(dict(row))
            for row in graph["imported_handles"]
        }
        snapshot = _VerifiedGraphSnapshot(
            commit=commit,
            graph_path=graph_path,
            graph=copy.deepcopy(graph),
            local_objects=local_objects,
            imported_handles=imported,
        )
        self._snapshot_cache[key] = snapshot
        return snapshot

    def _resolve_in(
        self,
        snapshot: _VerifiedGraphSnapshot,
        object_id: str,
        stack: frozenset[tuple[int, str, str]],
    ) -> ResolvedContentObject:
        key = (snapshot.commit.generation, snapshot.graph_path, object_id)
        cached = self._object_cache.get(key)
        if cached is not None:
            return cached
        if key in stack:
            raise StateCorruptionError("cross-commit content graph contains a cycle")
        local = snapshot.local_objects.get(object_id)
        if local is not None:
            self._object_cache[key] = local
            return local
        handle = snapshot.imported_handles.get(object_id)
        if handle is None:
            raise StateCorruptionError(
                f"content object is absent from exact graph membership: {object_id}"
            )
        validate_payload(handle, COMMITTED_OBJECT_HANDLE_SCHEMA)
        source_reference = handle["source_commit_reference"]
        source_generation = source_reference["generation"]
        if source_generation >= snapshot.commit.generation:
            raise StateCorruptionError(
                "imported content object does not come from a prior generation"
            )
        source_commit = self._context.read_commit(source_generation)
        _record, source_graph_path = _validate_commit_reference(
            source_reference, commit=source_commit
        )
        source = self._load_snapshot(source_generation, source_graph_path)
        # Handles name the direct owning commit.  A graph that merely imported
        # identical bytes cannot launder itself into the object's provenance.
        source_value = source.local_objects.get(object_id)
        if source_value is None:
            if object_id in source.imported_handles:
                raise StateCorruptionError(
                    "import handle names a transitive re-export, not the owning commit"
                )
            raise StateCorruptionError(
                "imported object is missing from its declared source graph"
            )
        if source_value.ref != handle["object_ref"]:
            raise StateCorruptionError(
                "imported object ref differs from exact source graph membership"
            )
        resolved = self._resolve_in(source, object_id, stack | {key})
        if resolved.ref != handle["object_ref"]:
            raise StateCorruptionError("imported object identity changed during resolution")
        self._object_cache[key] = resolved
        return resolved

    def _owner_in(
        self,
        snapshot: _VerifiedGraphSnapshot,
        object_id: str,
        stack: frozenset[tuple[int, str, str]],
    ) -> tuple[ResolvedContentObject, dict[str, Any]]:
        """Resolve the direct owner without accepting a transitive re-export."""

        key = (snapshot.commit.generation, snapshot.graph_path, object_id)
        if key in stack:
            raise StateCorruptionError("cross-commit content graph contains a cycle")
        local = snapshot.local_objects.get(object_id)
        if local is not None:
            reference = build_content_graph_commit_reference(
                snapshot.commit,
                programme_id=str(snapshot.commit.state["programme_id"]),
                graph_artifact_path=snapshot.graph_path,
            )
            return local, reference
        handle = snapshot.imported_handles.get(object_id)
        if handle is None:
            raise StateCorruptionError(
                f"content object is absent from exact graph membership: {object_id}"
            )
        validate_payload(handle, COMMITTED_OBJECT_HANDLE_SCHEMA)
        source_reference = copy.deepcopy(dict(handle["source_commit_reference"]))
        source_generation = source_reference["generation"]
        if source_generation >= snapshot.commit.generation:
            raise StateCorruptionError(
                "imported content object does not come from a prior generation"
            )
        source_commit = self._context.read_commit(source_generation)
        replayed_reference, source_graph_path = _validate_commit_reference(
            source_reference,
            commit=source_commit,
        )
        source = self._load_snapshot(source_generation, source_graph_path)
        source_value = source.local_objects.get(object_id)
        if source_value is None:
            if object_id in source.imported_handles:
                raise StateCorruptionError(
                    "import handle names a transitive re-export, not the owning commit"
                )
            raise StateCorruptionError(
                "imported object is missing from its declared source graph"
            )
        if source_value.ref != handle["object_ref"]:
            raise StateCorruptionError(
                "imported object ref differs from exact source graph membership"
            )
        resolved = self._resolve_in(source, object_id, stack | {key})
        if resolved.ref != handle["object_ref"]:
            raise StateCorruptionError("imported object identity changed during resolution")
        return resolved, replayed_reference

    @property
    def graph(self) -> Mapping[str, Any]:
        """Return a defensive current graph while the context remains live."""

        self._assert_live()
        return copy.deepcopy(dict(self._root.graph))

    def resolve(self, object_id: str) -> ResolvedContentObject:
        """Resolve one exact current-graph member with commit lineage intact."""

        self._assert_live()
        if not isinstance(object_id, str):
            raise ContractError("content object ID must be a string")
        return self._defensive(self._resolve_in(self._root, object_id, frozenset()))

    def verify_closure(self) -> tuple[ResolvedContentObject, ...]:
        """Resolve every DAG member once in declared dependency-first order."""

        self._assert_live()
        return tuple(
            self.resolve(object_id)
            for object_id in self._root.graph["topological_order"]
        )

    def verify_closure_with_direct_owners(
        self,
    ) -> tuple[StoreVerifiedOwnedContentObject, ...]:
        """Return the recursive active closure with exact direct owners.

        A terminal descendant graph imports only its immediate predecessor
        root.  Replaying just that graph would therefore omit the predecessor's
        locally owned dependency graph and could not validate the semantic
        N..N+8 closure.  Walk every imported direct-owner graph once, in
        dependency-first order, while retaining the commit that actually owns
        each object.  Identical bytes cannot be laundered through a later
        importing graph because :meth:`_owner_in` still rejects transitive
        re-export as ownership.
        """

        self._assert_live()
        rows: list[StoreVerifiedOwnedContentObject] = []
        by_id: dict[str, StoreVerifiedOwnedContentObject] = {}
        visited_graphs: set[tuple[int, str]] = set()

        def visit(snapshot: _VerifiedGraphSnapshot) -> None:
            graph_key = (snapshot.commit.generation, snapshot.graph_path)
            if graph_key in visited_graphs:
                return
            visited_graphs.add(graph_key)
            for object_id in snapshot.graph["topological_order"]:
                handle = snapshot.imported_handles.get(object_id)
                if handle is not None:
                    validate_payload(handle, COMMITTED_OBJECT_HANDLE_SCHEMA)
                    source_reference = handle["source_commit_reference"]
                    source_generation = source_reference["generation"]
                    source_commit = self._context.read_commit(source_generation)
                    _reference, source_graph_path = _validate_commit_reference(
                        source_reference,
                        commit=source_commit,
                    )
                    visit(
                        self._load_snapshot(
                            source_generation,
                            source_graph_path,
                        )
                    )
                resolved, owner = self._owner_in(
                    snapshot,
                    object_id,
                    frozenset(),
                )
                candidate = StoreVerifiedOwnedContentObject(
                    resolved=self._defensive(resolved),
                    owner_commit_reference=copy.deepcopy(owner),
                )
                existing = by_id.get(object_id)
                if existing is None:
                    by_id[object_id] = candidate
                    rows.append(candidate)
                elif existing != candidate:
                    raise StateCorruptionError(
                        "recursive content closure assigns two direct owners"
                    )

        visit(self._root)
        return tuple(rows)

    def resolve_roots(self) -> tuple[ResolvedContentObject, ...]:
        """Verify the complete closure before returning defensive root values."""

        self.verify_closure()
        return tuple(
            self.resolve(object_id) for object_id in self._root.graph["ordered_roots"]
        )


__all__ = [
    "COMMIT_REFERENCE_SCHEMA",
    "CONTENT_GRAPH_COMMIT_REFERENCE_SCHEMA",
    "StoreVerifiedContentObjectGraph",
    "StoreVerifiedOwnedContentObject",
    "build_content_graph_commit_reference",
]
