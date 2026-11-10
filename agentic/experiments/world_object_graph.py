# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Content-addressed object graphs for compositional experiment worlds.

The v2 world contracts are exact but recursively embed commissions, requests,
observations, producer evidence, and literature projections.  This module
provides the v3 storage kernel: immutable objects are identified without paths,
local paths are manifest-scoped locators, and cross-generation objects are
named through exact commit-bound handles.  Graph headers contain references
only, so hashing or replaying a child never copies the hydrated descendant
tree.

This is deliberately a storage and replay primitive, not scientific authority.
It verifies canonical bytes, semantic identity, graph closure, and filesystem
containment.  A later canonical cutover must still bind domain identities,
producer semantics, N..N+7 ordering, and the theory-first physics boundary.
"""

from __future__ import annotations

import copy
import json
import os
import stat
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_payload,
)


CONTENT_OBJECT_REF_SCHEMA = "dynamic_experiment_content_object_ref_v1.schema.json"
CONTENT_OBJECT_DESCRIPTOR_SCHEMA = (
    "dynamic_experiment_content_object_descriptor_v1.schema.json"
)
COMMITTED_OBJECT_HANDLE_SCHEMA = (
    "dynamic_experiment_committed_object_handle_v1.schema.json"
)
CONTENT_OBJECT_GRAPH_SCHEMA = (
    "dynamic_experiment_content_object_graph_v1.schema.json"
)
CONTENT_OBJECT_ID_PREFIX = "world-content-object-v1"
MAX_CONTENT_OBJECT_BYTES = 16 * 1024 * 1024
MAX_CONTENT_OBJECTS = 4096
MAX_CONTENT_GRAPH_EDGES = 16384
MAX_CONTENT_GRAPH_BYTES = 16 * 1024 * 1024
MAX_CONTENT_GRAPH_TOTAL_OBJECT_BYTES = 512 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class PreparedContentObject:
    """One canonical object prepared for create-only transaction publication."""

    value: Mapping[str, Any]
    data: bytes
    ref: Mapping[str, Any]
    descriptor: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ResolvedContentObject:
    """Verified bytes and parsed value returned by a graph resolver."""

    ref: Mapping[str, Any]
    value: Mapping[str, Any]
    data: bytes


ImportResolver = Callable[[Mapping[str, Any]], ResolvedContentObject]


def _copy_mapping(value: Mapping[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{label} must be an object")
    return copy.deepcopy(dict(value))


def _canonical_relative_path(raw: str) -> str:
    relative = safe_relative_path(raw)
    canonical = relative.as_posix()
    if canonical != raw:
        raise ContractError(f"content-object path is not canonical: {raw!r}")
    return canonical


def build_content_object_ref(
    *,
    object_kind: str,
    data: bytes,
    semantic_value: Mapping[str, Any],
) -> dict[str, Any]:
    """Build path-free identity from exact bytes and canonical JSON meaning."""

    if not isinstance(data, bytes) or not data:
        raise ContractError("content-object bytes must be nonempty")
    if len(data) > MAX_CONTENT_OBJECT_BYTES:
        raise ContractError("content-object bytes exceed the fixed object ceiling")
    value = _copy_mapping(semantic_value, "content-object semantic value")
    if canonical_json(value) != data:
        raise ContractError(
            "content-object bytes must be the canonical JSON encoding of its value"
        )
    sha256 = bytes_digest(data)
    semantic_digest = canonical_digest(value)
    ref = {
        "object_id": stable_identifier(
            CONTENT_OBJECT_ID_PREFIX,
            object_kind,
            sha256,
            semantic_digest,
        ),
        "object_kind": object_kind,
        "sha256": sha256,
        "size_bytes": len(data),
        "semantic_digest": semantic_digest,
    }
    validate_payload(ref, CONTENT_OBJECT_REF_SCHEMA)
    return ref


def build_content_object_descriptor(
    *,
    ref: Mapping[str, Any],
    path: str,
) -> dict[str, Any]:
    """Attach one root-relative locator without changing object identity."""

    descriptor = {
        "ref": _copy_mapping(ref, "content-object ref"),
        "path": _canonical_relative_path(path),
    }
    validate_payload(descriptor, CONTENT_OBJECT_DESCRIPTOR_SCHEMA)
    return descriptor


def prepare_content_object(
    *,
    object_kind: str,
    value: Mapping[str, Any],
    path: str,
) -> PreparedContentObject:
    """Prepare canonical bytes, identity, and locator without writing storage."""

    copied = _copy_mapping(value, "content-object value")
    data = canonical_json(copied)
    ref = build_content_object_ref(
        object_kind=object_kind,
        data=data,
        semantic_value=copied,
    )
    descriptor = build_content_object_descriptor(ref=ref, path=path)
    return PreparedContentObject(
        value=copied,
        data=data,
        ref=ref,
        descriptor=descriptor,
    )


def build_committed_object_handle(
    *,
    source_commit_reference: Mapping[str, Any],
    object_ref: Mapping[str, Any],
) -> dict[str, Any]:
    """Name one object through an exact prior commit rather than a free path."""

    handle = {
        "source_commit_reference": _copy_mapping(
            source_commit_reference, "source commit reference"
        ),
        "object_ref": _copy_mapping(object_ref, "imported object ref"),
    }
    validate_payload(handle, COMMITTED_OBJECT_HANDLE_SCHEMA)
    return handle


def _graph_without_digest(graph: Mapping[str, Any]) -> dict[str, Any]:
    material = _copy_mapping(graph, "content-object graph")
    material.pop("graph_digest", None)
    return material


def validate_content_object_graph(
    graph: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate schema, identity closure, topological order, and graph digest."""

    local_input = graph.get("local_descriptors") if isinstance(graph, Mapping) else None
    imported_input = graph.get("imported_handles") if isinstance(graph, Mapping) else None
    edges_input = graph.get("edges") if isinstance(graph, Mapping) else None
    if (
        not isinstance(local_input, list)
        or not isinstance(imported_input, list)
        or not isinstance(edges_input, list)
    ):
        raise ContractError("content-object graph arrays are absent")
    if len(local_input) + len(imported_input) > MAX_CONTENT_OBJECTS:
        raise ContractError("content-object graph exceeds the fixed object-count ceiling")
    if len(edges_input) > MAX_CONTENT_GRAPH_EDGES:
        raise ContractError("content-object graph exceeds the fixed edge-count ceiling")
    record = _copy_mapping(graph, "content-object graph")
    if len(canonical_json(record)) > MAX_CONTENT_GRAPH_BYTES:
        raise ContractError("content-object graph exceeds the fixed manifest-byte ceiling")
    validate_payload(record, CONTENT_OBJECT_GRAPH_SCHEMA)
    if record["graph_digest"] != canonical_digest(_graph_without_digest(record)):
        raise ContractError("content-object graph digest is invalid")

    local = record["local_descriptors"]
    imported = record["imported_handles"]
    local_ids = [row["ref"]["object_id"] for row in local]
    imported_ids = [row["object_ref"]["object_id"] for row in imported]
    all_ids = local_ids + imported_ids
    if len(set(all_ids)) != len(all_ids):
        raise ContractError(
            "content-object IDs must be unique across local and imported objects"
        )
    local_paths = [row["path"] for row in local]
    if len(set(local_paths)) != len(local_paths):
        raise ContractError("content-object local paths must be unique")
    for path in local_paths:
        _canonical_relative_path(path)
    total_object_bytes = sum(
        row["ref"]["size_bytes"] for row in local
    ) + sum(row["object_ref"]["size_bytes"] for row in imported)
    if total_object_bytes > MAX_CONTENT_GRAPH_TOTAL_OBJECT_BYTES:
        raise ContractError("content-object graph exceeds the total-object-byte ceiling")

    order = record["topological_order"]
    if len(order) != len(all_ids) or set(order) != set(all_ids):
        raise ContractError(
            "content-object topological order must be an exact object-ID permutation"
        )
    roots = record["ordered_roots"]
    if any(root not in set(all_ids) for root in roots):
        raise ContractError("content-object graph names an undeclared root")

    position = {object_id: index for index, object_id in enumerate(order)}
    incoming: dict[str, set[str]] = {object_id: set() for object_id in all_ids}
    edge_keys: set[tuple[str, str, str]] = set()
    for edge in record["edges"]:
        source = edge["source_object_id"]
        target = edge["target_object_id"]
        key = (source, target, edge["edge_kind"])
        if source not in position or target not in position:
            raise ContractError("content-object edge names an undeclared object")
        if source == target:
            raise ContractError("content-object graph forbids self-edges")
        if key in edge_keys:
            raise ContractError("content-object graph contains a duplicate typed edge")
        edge_keys.add(key)
        if position[source] >= position[target]:
            raise ContractError(
                "content-object edge violates declared topological order"
            )
        incoming[target].add(source)

    # Roots are semantic entrypoints.  Traversing prerequisites backwards from
    # them must cover every declared object; otherwise an unreferenced object
    # could be smuggled into the manifest without participating in replay.
    covered: set[str] = set()
    pending = list(roots)
    while pending:
        object_id = pending.pop()
        if object_id in covered:
            continue
        covered.add(object_id)
        pending.extend(sorted(incoming[object_id]))
    if covered != set(all_ids):
        missing = sorted(set(all_ids) - covered)[0]
        raise ContractError(
            f"content-object graph contains an object outside root closure: {missing}"
        )
    return record


def build_content_object_graph(
    *,
    local_descriptors: Sequence[Mapping[str, Any]],
    imported_handles: Sequence[Mapping[str, Any]],
    ordered_roots: Sequence[str],
    edges: Sequence[Mapping[str, Any]],
    topological_order: Sequence[str],
) -> dict[str, Any]:
    """Build and validate one compact immutable-object dependency graph."""

    graph: dict[str, Any] = {
        "schema_version": "1.0.0",
        "graph_kind": "dynamic_experiment_content_object_graph",
        "local_descriptors": [
            _copy_mapping(row, "local content-object descriptor")
            for row in local_descriptors
        ],
        "imported_handles": [
            _copy_mapping(row, "imported content-object handle")
            for row in imported_handles
        ],
        "ordered_roots": list(ordered_roots),
        "edges": [
            _copy_mapping(row, "content-object graph edge") for row in edges
        ],
        "topological_order": list(topological_order),
    }
    graph["graph_digest"] = canonical_digest(graph)
    return validate_content_object_graph(graph)


def _decode_canonical_object(data: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not one UTF-8 JSON object") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} must contain one JSON object")
    if canonical_json(value) != data:
        raise ContractError(f"{label} bytes are not canonical JSON")
    return value


def _require_safe_open_capability() -> None:
    """Fail closed when this host cannot enforce the promised path boundary."""

    missing = [
        name
        for name in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")
        if not hasattr(os, name)
    ]
    if missing:
        raise ContractError(
            "content-object safe-open capability is unavailable: "
            + ", ".join(missing)
        )


def _read_regular_no_follow(
    root: Path,
    relative_path: str,
    *,
    expected_size: int,
) -> bytes:
    """Read one file through component-wise directory FDs without following links."""

    if (
        isinstance(expected_size, bool)
        or not isinstance(expected_size, int)
        or expected_size <= 0
        or expected_size > MAX_CONTENT_OBJECT_BYTES
    ):
        raise ContractError("content-object expected size violates the fixed ceiling")
    _require_safe_open_capability()
    relative = safe_relative_path(relative_path)
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_DIRECTORY", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    descriptors: list[int] = []
    try:
        current = os.open(root, directory_flags)
        descriptors.append(current)
        for component in relative.parts[:-1]:
            current = os.open(component, directory_flags, dir_fd=current)
            descriptors.append(current)
        file_descriptor = os.open(relative.parts[-1], file_flags, dir_fd=current)
        descriptors.append(file_descriptor)
        metadata = os.fstat(file_descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ContractError(
                "content-object path is not one singly linked regular file"
            )
        if metadata.st_size != expected_size:
            raise ContractError("content-object file size differs from its ref")
        chunks: list[bytes] = []
        remaining = expected_size
        while True:
            chunk = os.read(file_descriptor, min(1024 * 1024, remaining + 1))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
            if remaining < 0:
                raise ContractError("content-object grew beyond its declared size")
        data = b"".join(chunks)
        if len(data) != expected_size:
            raise ContractError("content-object changed size while being read")
        return data
    except OSError as exc:
        raise ContractError(
            f"content-object path cannot be reopened safely: {relative_path}"
        ) from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _enumerate_tree_no_follow(root: Path) -> tuple[set[str], set[str]]:
    """Enumerate an object root without following links or accepting special files."""

    _require_safe_open_capability()
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_DIRECTORY", 0)
    )
    open_descriptors: list[int] = []
    files: set[str] = set()
    directories: set[str] = set()
    try:
        root_descriptor = os.open(root, directory_flags)
        open_descriptors.append(root_descriptor)
        pending: list[tuple[int, tuple[str, ...]]] = [(root_descriptor, ())]
        while pending:
            directory_descriptor, prefix = pending.pop()
            for name in sorted(os.listdir(directory_descriptor)):
                metadata = os.stat(
                    name,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
                relative_parts = (*prefix, name)
                relative = Path(*relative_parts).as_posix()
                if stat.S_ISDIR(metadata.st_mode):
                    child = os.open(
                        name,
                        directory_flags,
                        dir_fd=directory_descriptor,
                    )
                    open_descriptors.append(child)
                    directories.add(relative)
                    pending.append((child, relative_parts))
                elif stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1:
                    files.add(relative)
                else:
                    raise ContractError(
                        f"content-object tree contains a link or special file: {relative}"
                    )
        return files, directories
    except OSError as exc:
        raise ContractError("content-object tree cannot be enumerated safely") from exc
    finally:
        for descriptor in reversed(open_descriptors):
            os.close(descriptor)


class VerifiedContentObjectGraph:
    """Resolve a validated graph through one immutable local root and imports."""

    def __init__(
        self,
        *,
        local_root: Path,
        graph: Mapping[str, Any],
        import_resolver: ImportResolver | None = None,
    ) -> None:
        self._local_root = Path(local_root)
        self._graph = validate_content_object_graph(graph)
        self._import_resolver = import_resolver
        self._local = {
            row["ref"]["object_id"]: copy.deepcopy(row)
            for row in self._graph["local_descriptors"]
        }
        self._imported = {
            row["object_ref"]["object_id"]: copy.deepcopy(row)
            for row in self._graph["imported_handles"]
        }
        self._cache: dict[str, ResolvedContentObject] = {}
        self._expected_local_paths = {
            row["path"] for row in self._graph["local_descriptors"]
        }
        self._expected_local_directories = {
            Path(*Path(path).parts[:index]).as_posix()
            for path in self._expected_local_paths
            for index in range(1, len(Path(path).parts))
        }

    @property
    def graph(self) -> Mapping[str, Any]:
        """Return a defensive copy of the validated compact graph."""

        return copy.deepcopy(self._graph)

    @staticmethod
    def _defensive_result(
        resolved: ResolvedContentObject,
    ) -> ResolvedContentObject:
        """Return fresh mappings so a caller cannot poison verified cache state."""

        return ResolvedContentObject(
            ref=copy.deepcopy(dict(resolved.ref)),
            value=copy.deepcopy(dict(resolved.value)),
            data=bytes(resolved.data),
        )

    def _verify_exact_local_tree(self) -> None:
        files, directories = _enumerate_tree_no_follow(self._local_root)
        if files != self._expected_local_paths:
            raise ContractError(
                "content-object tree files differ from exact graph coverage"
            )
        if directories != self._expected_local_directories:
            raise ContractError(
                "content-object tree directories differ from exact graph coverage"
            )

    def _verify_data(
        self,
        *,
        ref: Mapping[str, Any],
        data: bytes,
        label: str,
    ) -> ResolvedContentObject:
        if len(data) != ref["size_bytes"] or bytes_digest(data) != ref["sha256"]:
            raise ContractError(f"{label} exact-byte identity differs from its ref")
        value = _decode_canonical_object(data, label=label)
        if canonical_digest(value) != ref["semantic_digest"]:
            raise ContractError(f"{label} semantic digest differs from its ref")
        replayed = build_content_object_ref(
            object_kind=ref["object_kind"],
            data=data,
            semantic_value=value,
        )
        if replayed != ref:
            raise ContractError(f"{label} object identity does not replay")
        return ResolvedContentObject(
            ref=copy.deepcopy(dict(ref)),
            value=value,
            data=bytes(data),
        )

    def resolve(self, object_id: str) -> ResolvedContentObject:
        """Resolve one local or prior-commit object and cache verified bytes."""

        if object_id in self._cache:
            return self._defensive_result(self._cache[object_id])
        if object_id in self._local:
            descriptor = self._local[object_id]
            data = _read_regular_no_follow(
                self._local_root,
                descriptor["path"],
                expected_size=descriptor["ref"]["size_bytes"],
            )
            resolved = self._verify_data(
                ref=descriptor["ref"],
                data=data,
                label=f"local content object {object_id}",
            )
        elif object_id in self._imported:
            if self._import_resolver is None:
                raise ContractError(
                    "content-object graph requires a verified import resolver"
                )
            handle = self._imported[object_id]
            candidate = self._import_resolver(copy.deepcopy(handle))
            if (
                not isinstance(candidate, ResolvedContentObject)
                or candidate.ref != handle["object_ref"]
            ):
                raise ContractError(
                    "import resolver returned a different committed content object"
                )
            resolved = self._verify_data(
                ref=handle["object_ref"],
                data=candidate.data,
                label=f"imported content object {object_id}",
            )
        else:
            raise ContractError(f"undeclared content-object ID: {object_id}")
        self._cache[object_id] = resolved
        return self._defensive_result(resolved)

    def verify_closure(self) -> tuple[ResolvedContentObject, ...]:
        """Verify exact local coverage and every object in dependency-first order."""

        self._verify_exact_local_tree()
        return tuple(
            self.resolve(object_id)
            for object_id in self._graph["topological_order"]
        )

    def resolve_roots(self) -> tuple[ResolvedContentObject, ...]:
        """Verify the complete dependency closure, then expose semantic roots."""

        self.verify_closure()
        return tuple(self.resolve(object_id) for object_id in self._graph["ordered_roots"])


__all__ = [
    "COMMITTED_OBJECT_HANDLE_SCHEMA",
    "CONTENT_OBJECT_DESCRIPTOR_SCHEMA",
    "CONTENT_OBJECT_GRAPH_SCHEMA",
    "CONTENT_OBJECT_ID_PREFIX",
    "CONTENT_OBJECT_REF_SCHEMA",
    "ImportResolver",
    "MAX_CONTENT_GRAPH_BYTES",
    "MAX_CONTENT_GRAPH_EDGES",
    "MAX_CONTENT_GRAPH_TOTAL_OBJECT_BYTES",
    "MAX_CONTENT_OBJECT_BYTES",
    "MAX_CONTENT_OBJECTS",
    "PreparedContentObject",
    "ResolvedContentObject",
    "VerifiedContentObjectGraph",
    "build_committed_object_handle",
    "build_content_object_descriptor",
    "build_content_object_graph",
    "build_content_object_ref",
    "prepare_content_object",
    "validate_content_object_graph",
]
