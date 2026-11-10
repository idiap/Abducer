# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Deterministic N-to-N+8 storage orchestration for v3 experiment worlds.

This module composes the existing content-graph transaction kernel; it does not
replace that kernel and does not decide whether any experiment result is
scientifically correct.  Its narrow job is to preserve one storage schedule:

``theory N -> anchor N+1 -> five worlds N+2..N+6 -> aggregation N+7
-> immutable reflection input N+8``.

World producers may finish in parallel and in any order.  They return inert,
path-bound :class:`GraphStageProduct` values.  The single coordinator freezes
those values and commits only the longest ready prefix in the closed world
order.  A later world can therefore be ready without being allowed to pretend
that its predecessor is already committed.

Every cross-generation dependency is resolved through one flattened catalog
of direct owners.  Catalog entries are minted only from store-verified commits;
the runtime never manufactures a sibling observation or re-exports a
transitively imported object.  Every locally owned stage object is
role-validated and contributes its payload-derived edges.  Complete
cross-object experiment semantics still belong to the public contextual world
validator and role-specific producers, not to this storage scheduler.
"""

from __future__ import annotations

import copy
import heapq
import json
import os
import resource
import secrets
import selectors
import signal
import stat
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
)
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedArtifactContext,
    VerifiedCommit,
)

from .content_graph_transactions import (
    ContentGraphTransactionResult,
    MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES,
    MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS,
    PreparedContentGraphTransaction,
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
    reopen_content_graph_transaction,
)
from .world_object_graph import (
    PreparedContentObject,
    build_content_object_ref,
    build_committed_object_handle,
    build_content_object_graph,
    prepare_content_object,
    validate_content_object_graph,
)
from .world_object_graph_store import (
    StoreVerifiedContentObjectGraph,
    build_content_graph_commit_reference,
)
from .world_object_roles import (
    derive_content_object_edges,
    validate_role_bound_object,
)


WORLD_ORDER = (
    "no_probe",
    "neutral_inconclusive",
    "misleading_toy_positive",
    "registered_premise_falsifier",
    "operational_failure",
)
ANCHOR_ROOT_KIND = "world_matrix_anchor_root_v3"
WORLD_ROOT_KIND = "world_observation_envelope_v3"
AGGREGATION_ROOT_KIND = "world_matrix_aggregation_root_v3"
DESCENDANT_REFLECTION_ROOT_KIND = "world_matrix_descendant_reflection_root_v3"
INCOMPLETE_SUPPORT_AUTHORITY_BOUNDARY = (
    "storage_readiness_only_no_semantic_theory_truth_proof_or_physics_authority"
)
RECOVERY_AUTHORITY_BOUNDARY = (
    "local_store_byte_and_order_replay_only_no_semantic_scientific_truth_proof_"
    "experiment_value_or_physics_authority"
)
MAX_WORLD_V3_LANE_COMMITS = 8
MAX_WORLD_V3_DESCENDANT_COMMITS = 9
MAX_WORLD_V3_LANE_LOCAL_OBJECTS = (
    MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS * MAX_WORLD_V3_DESCENDANT_COMMITS
)
MAX_WORLD_V3_LANE_COMMITTED_BYTES = (
    MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES * MAX_WORLD_V3_DESCENDANT_COMMITS
)
MAX_WORLD_V3_RECOVERY_CHILD_PROCESSES = 0
MAX_WORLD_V3_RECOVERY_PHASE_NS = 30_000_000_000
MAX_WORLD_V3_RECOVERY_TOTAL_NS = MAX_WORLD_V3_RECOVERY_PHASE_NS * 3
MAX_WORLD_V3_FRESH_PROCESS_NS = MAX_WORLD_V3_RECOVERY_PHASE_NS
MAX_WORLD_V3_FRESH_PROCESS_CPU_NS = 60_000_000_000
MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES = 512 * 1024 * 1024
MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS = 1
MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES = 256 * 1024
MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES = 512 * 1024
MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES = 64 * 1024
WORLD_V3_FRESH_PROCESS_METRIC_SAMPLE_NS = 100_000_000
WORLD_V3_FRESH_PROCESS_TERMINATION_GRACE_NS = 250_000_000
WORLD_V3_FRESH_PROCESS_PROTOCOL_VERSION = "1.0.0"
FRESH_PROCESS_RECOVERY_AUTHORITY_BOUNDARY = (
    "parent_supervised_local_storage_replay_only_no_semantic_scientific_truth_"
    "proof_experiment_value_or_physics_authority"
)
FRESH_PROCESS_CPU_MEASUREMENT_SCOPE = (
    "parent_resource_getrusage_rusage_children_delta_including_the_worker_and_"
    "bounded_process_metric_sampler_children"
)
FRESH_PROCESS_MEMORY_MEASUREMENT_SCOPE = (
    "parent_ps_sampled_sum_rss_for_the_isolated_worker_process_group"
)
_FRESH_PROCESS_ENVIRONMENT = {
    "LANG": "C",
    "LC_ALL": "C",
    "PYTHONCOERCECLOCALE": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONHASHSEED": "0",
    "PYTHONUTF8": "1",
}


@dataclass(frozen=True, slots=True)
class GraphStageProduct:
    """One producer-completed, not-yet-committed stage payload.

    ``state`` must describe the generation that the product will create.
    Objects must already have deterministic branch-local paths.  The
    coordinator defensively rebuilds every object from canonical bytes before
    retaining it, so mutation after submission cannot change a later commit.
    """

    state: Mapping[str, Any]
    local_objects: tuple[PreparedContentObject, ...]
    root_object_id: str


@dataclass(frozen=True, slots=True)
class CommittedWorld:
    """One world root committed at its fixed ordinal-derived generation."""

    world_id: str
    world_ordinal: int
    generation: int
    result: ContentGraphTransactionResult


@dataclass(frozen=True, slots=True)
class IncompleteWorldSupport:
    """Typed, non-scientific explanation of why aggregation is not ready."""

    theory_generation: int
    anchor_generation: int
    committed_world_ids: tuple[str, ...]
    ready_but_blocked_world_ids: tuple[str, ...]
    not_ready_world_ids: tuple[str, ...]
    failed_world_ids: tuple[str, ...]
    next_world_id: str | None
    next_expected_generation: int | None
    aggregation_permitted: bool = False
    authority_boundary: str = INCOMPLETE_SUPPORT_AUTHORITY_BOUNDARY

    def as_dict(self) -> dict[str, Any]:
        """Return a stable JSON-ready projection for logs and typed handoff."""

        return {
            "support_kind": "incomplete_world_support",
            "theory_generation": self.theory_generation,
            "anchor_generation": self.anchor_generation,
            "committed_world_ids": list(self.committed_world_ids),
            "ready_but_blocked_world_ids": list(
                self.ready_but_blocked_world_ids
            ),
            "not_ready_world_ids": list(self.not_ready_world_ids),
            "failed_world_ids": list(self.failed_world_ids),
            "next_world_id": self.next_world_id,
            "next_expected_generation": self.next_expected_generation,
            "aggregation_permitted": self.aggregation_permitted,
            "authority_boundary": self.authority_boundary,
        }


@dataclass(frozen=True, slots=True)
class WorldPrefixCommit:
    """Current deterministic serial-commit prefix and readiness status."""

    committed_worlds: tuple[CommittedWorld, ...]
    incomplete_support: IncompleteWorldSupport | None

    @property
    def complete(self) -> bool:
        """Report structural completion only, never scientific success."""

        return self.incomplete_support is None


@dataclass(frozen=True, slots=True)
class WorldProducerFailure:
    """Bounded producer failure retained without changing sibling products."""

    world_id: str
    failure_kind: str
    exception_type: str
    message: str


@dataclass(frozen=True, slots=True)
class ParallelWorldProduction:
    """Outcome of parallel completion followed by serial prefix publication."""

    completion_order: tuple[str, ...]
    failures: tuple[WorldProducerFailure, ...]
    prefix: WorldPrefixCommit


@dataclass(frozen=True, slots=True)
class AggregationCommit:
    """Aggregation result or the typed incomplete support that forbids it."""

    result: ContentGraphTransactionResult | None
    incomplete_support: IncompleteWorldSupport | None

    @property
    def committed(self) -> bool:
        return self.result is not None


@dataclass(frozen=True, slots=True)
class DescendantReflectionCommit:
    """The mandatory immutable N+8 return, with no current-theory authority."""

    result: ContentGraphTransactionResult


@dataclass(frozen=True, slots=True)
class CanonicalDescendantExperimentV3Result:
    """Public result of the sole active N-to-N+8 experiment production route."""

    theory_generation: int
    anchor: ContentGraphTransactionResult
    worlds: tuple[CommittedWorld, ...]
    aggregation: ContentGraphTransactionResult
    reflection: ContentGraphTransactionResult
    parallel_production: ParallelWorldProduction
    verified_descendant_closure: Any
    authority_boundary: str = (
        "active_current_local_descendant_chronology_only_no_truth_proof_"
        "experiment_value_theory_selection_or_physics_authority"
    )


@dataclass(frozen=True, slots=True)
class RecoveryMeasurementReceipt:
    """Truthful local measurements for one exact three-pass lane recovery."""

    theory_generation: int
    head_generation: int
    commit_count: int
    local_object_count: int
    committed_payload_bytes: int
    child_processes_spawned: int
    cold_recovery_elapsed_ns: int
    warm_reopen_elapsed_ns: int
    uncached_replay_elapsed_ns: int
    total_recovery_elapsed_ns: int
    lane_digest: str
    exact_warm_reopen: bool
    exact_uncached_replay: bool
    authority_boundary: str = RECOVERY_AUTHORITY_BOUNDARY

    def as_dict(self) -> dict[str, Any]:
        """Return fixed ceilings, measurements, and a self-derived receipt ID."""

        payload: dict[str, Any] = {
            "schema_version": "1.0.0",
            "receipt_kind": "world_v3_content_graph_recovery_measurement",
            "theory_generation": self.theory_generation,
            "head_generation": self.head_generation,
            "commit_count": self.commit_count,
            "local_object_count": self.local_object_count,
            "committed_payload_bytes": self.committed_payload_bytes,
            "child_processes_spawned": self.child_processes_spawned,
            "cold_recovery_elapsed_ns": self.cold_recovery_elapsed_ns,
            "warm_reopen_elapsed_ns": self.warm_reopen_elapsed_ns,
            "uncached_replay_elapsed_ns": self.uncached_replay_elapsed_ns,
            "total_recovery_elapsed_ns": self.total_recovery_elapsed_ns,
            "lane_digest": self.lane_digest,
            "exact_warm_reopen": self.exact_warm_reopen,
            "exact_uncached_replay": self.exact_uncached_replay,
            "limits": {
                "max_commits": MAX_WORLD_V3_DESCENDANT_COMMITS,
                "max_local_objects": MAX_WORLD_V3_LANE_LOCAL_OBJECTS,
                "max_committed_payload_bytes": (
                    MAX_WORLD_V3_LANE_COMMITTED_BYTES
                ),
                "max_child_processes": MAX_WORLD_V3_RECOVERY_CHILD_PROCESSES,
                "max_each_recovery_phase_ns": (
                    MAX_WORLD_V3_RECOVERY_PHASE_NS
                ),
                "max_total_recovery_elapsed_ns": (
                    MAX_WORLD_V3_RECOVERY_TOTAL_NS
                ),
            },
            "authority_boundary": self.authority_boundary,
        }
        payload["receipt_digest"] = canonical_digest(payload)
        return payload


@dataclass(frozen=True, slots=True)
class FreshProcessRecoveryReceipt:
    """Parent-observed receipt for one separately supervised recovery process."""

    request_digest: str
    worker_output_digest: str
    output_payload_digest: str
    theory_generation: int
    head_generation: int
    recovered_commit_count: int
    recovered_local_object_count: int
    recovered_committed_payload_bytes: int
    lane_digest: str
    launch_to_exit_elapsed_ns: int
    parent_supervision_elapsed_ns: int
    child_cpu_elapsed_ns: int
    peak_process_group_rss_bytes: int
    launched_process_count: int
    peak_observed_process_group_members: int
    terminal_process_group_members: int
    returncode: int
    deadline_ns: int
    request_bytes: int
    stdout_bytes: int
    stderr_bytes: int
    launch_argv_digest: str
    in_process_recovery: RecoveryMeasurementReceipt
    _executable_identity_data: bytes
    _worker_module_identity_data: bytes
    _environment_identity_data: bytes
    _relocation_identity_data: bytes
    _process_identity_data: bytes
    authority_boundary: str = FRESH_PROCESS_RECOVERY_AUTHORITY_BOUNDARY

    @property
    def executable_identity(self) -> dict[str, Any]:
        return _decode_canonical_mapping(
            self._executable_identity_data,
            "fresh-process executable identity",
        )

    @property
    def worker_module_identity(self) -> dict[str, Any]:
        return _decode_canonical_mapping(
            self._worker_module_identity_data,
            "fresh-process worker-module identity",
        )

    @property
    def environment_identity(self) -> dict[str, Any]:
        return _decode_canonical_mapping(
            self._environment_identity_data,
            "fresh-process environment identity",
        )

    @property
    def relocation_identity(self) -> dict[str, Any]:
        return _decode_canonical_mapping(
            self._relocation_identity_data,
            "fresh-process relocation identity",
        )

    @property
    def process_identity(self) -> dict[str, Any]:
        return _decode_canonical_mapping(
            self._process_identity_data,
            "fresh-process process identity",
        )

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": "1.0.0",
            "receipt_kind": "world_v3_fresh_process_recovery",
            "request_digest": self.request_digest,
            "worker_output_digest": self.worker_output_digest,
            "output_payload_digest": self.output_payload_digest,
            "theory_generation": self.theory_generation,
            "head_generation": self.head_generation,
            "recovered_commit_count": self.recovered_commit_count,
            "recovered_local_object_count": self.recovered_local_object_count,
            "recovered_committed_payload_bytes": (
                self.recovered_committed_payload_bytes
            ),
            "lane_digest": self.lane_digest,
            "launch_to_exit_elapsed_ns": self.launch_to_exit_elapsed_ns,
            "parent_supervision_elapsed_ns": (
                self.parent_supervision_elapsed_ns
            ),
            "child_cpu_elapsed_ns": self.child_cpu_elapsed_ns,
            "cpu_time_unit": "nanoseconds",
            "cpu_measurement_scope": FRESH_PROCESS_CPU_MEASUREMENT_SCOPE,
            "peak_process_group_rss_bytes": (
                self.peak_process_group_rss_bytes
            ),
            "memory_unit": "bytes",
            "memory_measurement_scope": (
                FRESH_PROCESS_MEMORY_MEASUREMENT_SCOPE
            ),
            "process_counts": {
                "launched": self.launched_process_count,
                "peak_observed_group_members": (
                    self.peak_observed_process_group_members
                ),
                "terminal_group_members": (
                    self.terminal_process_group_members
                ),
            },
            "returncode": self.returncode,
            "deadline_ns": self.deadline_ns,
            "request_bytes": self.request_bytes,
            "stdout_bytes": self.stdout_bytes,
            "stderr_bytes": self.stderr_bytes,
            "launch_argv_digest": self.launch_argv_digest,
            "executable_identity": self.executable_identity,
            "worker_module_identity": self.worker_module_identity,
            "environment_identity": self.environment_identity,
            "relocation_identity": self.relocation_identity,
            "process_identity": self.process_identity,
            "in_process_recovery": self.in_process_recovery.as_dict(),
            "limits": {
                "max_launch_to_exit_elapsed_ns": (
                    MAX_WORLD_V3_FRESH_PROCESS_NS
                ),
                "max_child_cpu_elapsed_ns": (
                    MAX_WORLD_V3_FRESH_PROCESS_CPU_NS
                ),
                "max_process_group_rss_bytes": (
                    MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES
                ),
                "max_process_group_members": (
                    MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS
                ),
                "max_request_bytes": (
                    MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES
                ),
                "max_stdout_bytes": (
                    MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES
                ),
                "max_stderr_bytes": (
                    MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES
                ),
            },
            "authority_boundary": self.authority_boundary,
        }
        payload["receipt_digest"] = canonical_digest(payload)
        return payload


class FreshProcessRecoveryError(ContractError):
    """A typed operational failure from the parent process supervisor."""

    def __init__(self, failure_kind: str, detail: str) -> None:
        self.failure_kind = failure_kind
        super().__init__(f"{failure_kind}: {detail}")


class MissingCommittedDependency(ContractError):
    """A product references bytes with no store-minted direct owner."""

    def __init__(self, object_ids: Sequence[str]) -> None:
        self.object_ids = tuple(sorted(set(object_ids)))
        super().__init__(
            "stage product lacks committed direct owners: "
            + ", ".join(self.object_ids)
        )


@dataclass(frozen=True, slots=True)
class _FrozenStageProduct:
    """Canonical private copy retained between producer completion and commit."""

    state_data: bytes
    local_objects: tuple[PreparedContentObject, ...]
    root_object_id: str

    @property
    def state(self) -> dict[str, Any]:
        value = json.loads(self.state_data.decode("utf-8"))
        if not isinstance(value, dict):
            raise ContractError("frozen stage state is not one JSON object")
        return value


@dataclass(frozen=True, slots=True)
class _DirectOwner:
    """Path-free object identity paired with its exact owning commit."""

    object_ref_data: bytes
    commit_reference_data: bytes

    @property
    def object_ref(self) -> dict[str, Any]:
        value = json.loads(self.object_ref_data.decode("utf-8"))
        if not isinstance(value, dict):
            raise ContractError("catalog object ref is not one JSON object")
        return value

    @property
    def commit_reference(self) -> dict[str, Any]:
        value = json.loads(self.commit_reference_data.decode("utf-8"))
        if not isinstance(value, dict):
            raise ContractError("catalog commit ref is not one JSON object")
        return value


WorldProducer = Callable[[], GraphStageProduct]


@dataclass(frozen=True, slots=True)
class _RecoveredCommit:
    """One transaction reproduced from a verified context without path trust."""

    result: ContentGraphTransactionResult
    graph: Mapping[str, Any]
    local_objects: tuple[PreparedContentObject, ...]
    frozen_product: _FrozenStageProduct | None
    root: PreparedContentObject | None
    committed_payload_bytes: int


@dataclass(frozen=True, slots=True)
class _RecoveredLane:
    """Private deterministic projection shared by all three recovery passes."""

    head_generation: int
    theory_result: ContentGraphTransactionResult
    catalog: Mapping[str, _DirectOwner]
    anchor: _RecoveredCommit | None
    worlds: tuple[tuple[str, _RecoveredCommit], ...]
    aggregation: _RecoveredCommit | None
    reflection: _RecoveredCommit | None
    local_object_count: int
    committed_payload_bytes: int
    lane_digest: str


def _decode_canonical_mapping(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StateCorruptionError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise StateCorruptionError(f"{label} is not one canonical JSON object")
    return value


def _manifest_descriptor(commit: VerifiedCommit, path: str) -> dict[str, Any]:
    matches = [row for row in commit.manifest["artifacts"] if row.get("path") == path]
    if len(matches) != 1:
        raise StateCorruptionError(
            f"recovered commit lacks one exact artifact descriptor: {path}"
        )
    return copy.deepcopy(dict(matches[0]))


def _result_from_recovered_commit(
    *,
    commit: VerifiedCommit,
    graph: Mapping[str, Any],
    graph_path: str,
    programme_id: str,
    request_digest: str,
    idempotency_key: str,
) -> ContentGraphTransactionResult:
    """Rebuild the compact public receipt from verified commit and graph bytes."""

    commit_ref = build_content_graph_commit_reference(
        commit,
        programme_id=programme_id,
        graph_artifact_path=graph_path,
    )
    graph_ref = {
        "schema_version": "1.0.0",
        "reference_kind": "committed_content_object_graph",
        "generation": commit.generation,
        "graph_digest": graph["graph_digest"],
        "commit_reference_digest": commit_ref["reference_digest"],
        "graph_artifact": copy.deepcopy(commit_ref["graph_artifact"]),
        "object_count": len(graph["topological_order"]),
        "local_object_count": len(graph["local_descriptors"]),
        "imported_object_count": len(graph["imported_handles"]),
        "ordered_root_object_ids": list(graph["ordered_roots"]),
    }
    refs_by_id = {
        row["ref"]["object_id"]: row["ref"]
        for row in graph["local_descriptors"]
    }
    refs_by_id.update(
        {
            row["object_ref"]["object_id"]: row["object_ref"]
            for row in graph["imported_handles"]
        }
    )
    try:
        root_refs = tuple(refs_by_id[object_id] for object_id in graph["ordered_roots"])
    except KeyError as exc:
        raise StateCorruptionError(
            "recovered graph root lacks one exact membership ref"
        ) from exc
    return ContentGraphTransactionResult(
        request_digest=request_digest,
        idempotency_key=idempotency_key,
        _commit_reference_data=canonical_json(commit_ref),
        _graph_reference_data=canonical_json(graph_ref),
        _root_reference_data=tuple(canonical_json(ref) for ref in root_refs),
    )


def _recover_one_commit(
    *,
    context: VerifiedArtifactContext,
    generation: int,
    graph_path: str,
    programme_id: str,
    expected_root_kind: str | None,
    branch_id: str,
    phase_started_ns: int,
) -> _RecoveredCommit:
    """Reproduce one graph transaction entirely from context-verified bytes."""

    if time.perf_counter_ns() - phase_started_ns > MAX_WORLD_V3_RECOVERY_PHASE_NS:
        raise ContractError("world-v3 recovery exceeded its fixed phase-time ceiling")
    commit = context.read_commit(generation)
    if (
        commit.state.get("target_id") != context.target_id
        or commit.state.get("run_id") != context.run_id
        or commit.state.get("programme_id") != programme_id
        or commit.state.get("generation") != generation
    ):
        raise StateCorruptionError(
            "recovered commit crosses target/run/programme/generation identity"
        )
    manifest_paths = context.artifact_paths(generation)
    _same_commit, batch = context.read_artifacts(generation, manifest_paths)
    graph_data = batch.get(graph_path)
    if not isinstance(graph_data, bytes):
        raise StateCorruptionError(
            f"fixed world-v3 graph path is absent at generation {generation}"
        )
    try:
        graph = validate_content_object_graph(
            _decode_canonical_mapping(graph_data, "recovered content graph")
        )
    except ContractError as exc:
        raise StateCorruptionError("recovered content graph is invalid") from exc
    local_objects: list[PreparedContentObject] = []
    for descriptor in graph["local_descriptors"]:
        path = descriptor["path"]
        data = batch.get(path)
        if not isinstance(data, bytes):
            raise StateCorruptionError("recovered local object bytes are absent")
        value = _decode_canonical_mapping(data, "recovered local object")
        try:
            ref = build_content_object_ref(
                object_kind=str(descriptor["ref"]["object_kind"]),
                data=data,
                semantic_value=value,
            )
            rebuilt = prepare_content_object(
                object_kind=str(ref["object_kind"]),
                value=value,
                path=path,
            )
        except ContractError as exc:
            raise StateCorruptionError(
                "recovered local object identity cannot be replayed"
            ) from exc
        if rebuilt.ref != descriptor["ref"] or rebuilt.data != data:
            raise StateCorruptionError(
                "recovered local object differs from its graph descriptor"
            )
        local_objects.append(rebuilt)
    expected_paths = {
        graph_path,
        *(row.descriptor["path"] for row in local_objects),
    }
    if set(manifest_paths) != expected_paths or set(batch) != expected_paths:
        raise StateCorruptionError(
            "recovered commit is not exactly one graph and its local objects"
        )
    graph_manifest = _manifest_descriptor(commit, graph_path)
    try:
        namespace = Namespace.from_mapping(graph_manifest["namespace"])
    except (ContractError, KeyError, TypeError) as exc:
        raise StateCorruptionError("recovered graph namespace is invalid") from exc
    if (
        namespace.target_id != context.target_id
        or namespace.run_id != context.run_id
        or namespace.branch_id != branch_id
        or namespace.state_version != generation - 1
    ):
        raise StateCorruptionError(
            "recovered graph namespace differs from fixed lane identity"
        )
    try:
        prepared = prepare_content_graph_transaction(
            expected_generation=generation - 1,
            state=commit.state,
            namespace=namespace,
            graph_artifact_path=graph_path,
            graph=graph,
            local_objects=local_objects,
        )
    except ContractError as exc:
        raise StateCorruptionError(
            "recovered content-graph transaction cannot be reproduced"
        ) from exc
    expected_descriptors = [
        {
            "path": graph_path,
            "sha256": bytes_digest(graph_data),
            "size_bytes": len(graph_data),
            "namespace": namespace.as_dict(),
        },
        *(
            {
                "path": row.descriptor["path"],
                "sha256": bytes_digest(row.data),
                "size_bytes": len(row.data),
                "namespace": namespace.as_dict(),
            }
            for row in local_objects
        ),
    ]
    if list(commit.manifest["artifacts"]) != expected_descriptors:
        raise StateCorruptionError(
            "recovered artifact vector differs from transaction reproduction"
        )
    if (
        commit.manifest.get("request_digest") != prepared.request_digest
        or commit.manifest.get("idempotency_key") != prepared.idempotency_key
    ):
        raise StateCorruptionError(
            "recovered request/idempotency identity is not byte-derived"
        )
    result = _result_from_recovered_commit(
        commit=commit,
        graph=graph,
        graph_path=graph_path,
        programme_id=programme_id,
        request_digest=prepared.request_digest,
        idempotency_key=prepared.idempotency_key,
    )
    frozen_product: _FrozenStageProduct | None = None
    root: PreparedContentObject | None = None
    if expected_root_kind is not None:
        if len(graph["ordered_roots"]) != 1:
            raise StateCorruptionError(
                "recovered world-v3 stage must have one exact root"
            )
        root_id = graph["ordered_roots"][0]
        local_by_id = {
            str(row.ref["object_id"]): row for row in local_objects
        }
        root = local_by_id.get(root_id)
        if root is None or root.ref["object_kind"] != expected_root_kind:
            raise StateCorruptionError(
                "recovered world-v3 stage has the wrong local root kind"
            )
        frozen_product = _freeze_product(
            GraphStageProduct(
                state=commit.state,
                local_objects=tuple(local_objects),
                root_object_id=root_id,
            )
        )
        expected_edges: list[dict[str, str]] = []
        for row in local_objects:
            try:
                expected_edges.extend(
                    derive_content_object_edges(
                        object_ref=row.ref,
                        payload=row.value,
                    )
                )
            except ContractError as exc:
                raise StateCorruptionError(
                    "recovered local role object is invalid"
                ) from exc
        def edge_key(row: Mapping[str, Any]) -> tuple[str, str, str]:
            return (
                str(row["source_object_id"]),
                str(row["target_object_id"]),
                str(row["edge_kind"]),
            )

        if sorted(graph["edges"], key=edge_key) != sorted(
            expected_edges, key=edge_key
        ):
            raise StateCorruptionError(
                "recovered graph edges differ from all local role payloads"
            )
    committed_payload_bytes = (
        sum(len(data) for data in batch.values())
        + len(canonical_json(commit.state))
        + len(canonical_json(commit.manifest))
    )
    return _RecoveredCommit(
        result=result,
        graph=graph,
        local_objects=tuple(local_objects),
        frozen_product=frozen_product,
        root=root,
        committed_payload_bytes=committed_payload_bytes,
    )


def _audit_recovery_lane(
    *,
    context: VerifiedArtifactContext,
    theory_generation: int,
    theory_result: ContentGraphTransactionResult,
    branch_id: str,
    phase_started_ns: int,
) -> _RecoveredLane:
    """Audit the exact available N..N+8 prefix and rebuild direct owners."""

    head = context.current_generation
    if head < theory_generation or head > theory_generation + 8:
        raise ContractError("world-v3 recovery head lies outside the fixed N..N+8 lane")
    commit_count = head - theory_generation + 1
    if commit_count > MAX_WORLD_V3_DESCENDANT_COMMITS:
        raise ContractError("world-v3 recovery exceeds the fixed commit ceiling")
    programme_id = str(theory_result.commit_ref["programme_id"])
    catalog: dict[str, _DirectOwner] = {}
    receipt_vector: list[Mapping[str, Any]] = []
    local_object_count = 0
    committed_payload_bytes = 0

    def account(recovered: _RecoveredCommit, *, allow_theory_imports: bool) -> None:
        nonlocal local_object_count, committed_payload_bytes
        if allow_theory_imports:
            for handle in recovered.graph["imported_handles"]:
                object_id = str(handle["object_ref"]["object_id"])
                proposed = _DirectOwner(
                    object_ref_data=canonical_json(handle["object_ref"]),
                    commit_reference_data=canonical_json(
                        handle["source_commit_reference"]
                    ),
                )
                current = catalog.get(object_id)
                if current is not None and current != proposed:
                    raise StateCorruptionError(
                        "recovered theory import has two direct owners"
                    )
                catalog[object_id] = proposed
        else:
            for handle in recovered.graph["imported_handles"]:
                object_id = str(handle["object_ref"]["object_id"])
                owner = catalog.get(object_id)
                if owner is None:
                    raise StateCorruptionError(
                        "recovered stage imports an object with no earlier direct owner"
                    )
                if (
                    owner.object_ref != handle["object_ref"]
                    or owner.commit_reference
                    != handle["source_commit_reference"]
                ):
                    raise StateCorruptionError(
                        "recovered import differs from the exact direct owner"
                    )
        local_ids = {
            str(row.ref["object_id"]) for row in recovered.local_objects
        }
        reowned = sorted(local_ids & set(catalog))
        if reowned:
            raise StateCorruptionError(
                "recovered stage locally reowns an imported/prior object"
            )
        commit_data = canonical_json(recovered.result.commit_ref)
        for row in recovered.local_objects:
            catalog[str(row.ref["object_id"])] = _DirectOwner(
                object_ref_data=canonical_json(row.ref),
                commit_reference_data=commit_data,
            )
        local_object_count += len(recovered.local_objects)
        committed_payload_bytes += recovered.committed_payload_bytes
        if local_object_count > MAX_WORLD_V3_LANE_LOCAL_OBJECTS:
            raise ContractError("world-v3 recovery exceeds the fixed object ceiling")
        if committed_payload_bytes > MAX_WORLD_V3_LANE_COMMITTED_BYTES:
            raise ContractError("world-v3 recovery exceeds the fixed byte ceiling")
        receipt_vector.append(recovered.result.as_dict())
        if time.perf_counter_ns() - phase_started_ns > MAX_WORLD_V3_RECOVERY_PHASE_NS:
            raise ContractError("world-v3 recovery exceeded its fixed phase-time ceiling")

    if theory_generation > 1:
        prior_paths = context.artifact_paths(theory_generation - 1)
        prior_graph_paths = tuple(
            path for path in prior_paths if path.endswith("/graph.json")
        )
        if len(prior_graph_paths) != 1:
            raise ContractError(
                "world-v3 recovery requires one exact immediate precommit graph"
            )
        prior = _recover_one_commit(
            context=context,
            generation=theory_generation - 1,
            graph_path=prior_graph_paths[0],
            programme_id=programme_id,
            expected_root_kind=None,
            branch_id=branch_id,
            phase_started_ns=phase_started_ns,
        )
        prior_commit_data = canonical_json(prior.result.commit_ref)
        for row in prior.local_objects:
            catalog[str(row.ref["object_id"])] = _DirectOwner(
                object_ref_data=canonical_json(row.ref),
                commit_reference_data=prior_commit_data,
            )

    theory_path = str(theory_result.graph_ref["graph_artifact"]["path"])
    theory = _recover_one_commit(
        context=context,
        generation=theory_generation,
        graph_path=theory_path,
        programme_id=programme_id,
        expected_root_kind=None,
        branch_id=branch_id,
        phase_started_ns=phase_started_ns,
    )
    if theory.result != theory_result:
        raise ContractError(
            "explicit theory generation/result identity does not match verified bytes"
        )
    account(theory, allow_theory_imports=True)

    anchor: _RecoveredCommit | None = None
    worlds: list[tuple[str, _RecoveredCommit]] = []
    aggregation: _RecoveredCommit | None = None
    reflection: _RecoveredCommit | None = None
    if head >= theory_generation + 1:
        anchor = _recover_one_commit(
            context=context,
            generation=theory_generation + 1,
            graph_path=(
                f"branches/{branch_id}/world-v3/"
                f"g{theory_generation + 1}/graph.json"
            ),
            programme_id=programme_id,
            expected_root_kind=ANCHOR_ROOT_KIND,
            branch_id=branch_id,
            phase_started_ns=phase_started_ns,
        )
        account(anchor, allow_theory_imports=False)
        assert anchor.root is not None
        if (
            anchor.root.value["target_id"] != context.target_id
            or anchor.root.value["run_id"] != context.run_id
            or anchor.root.value["prior_state_version"] != theory_generation - 1
        ):
            raise StateCorruptionError(
                "recovered anchor differs from explicit theory identity"
            )

    for ordinal, world_id in enumerate(WORLD_ORDER):
        generation = theory_generation + 2 + ordinal
        if head < generation:
            break
        recovered = _recover_one_commit(
            context=context,
            generation=generation,
            graph_path=(
                f"branches/{branch_id}/world-v3/g{generation}/graph.json"
            ),
            programme_id=programme_id,
            expected_root_kind=WORLD_ROOT_KIND,
            branch_id=branch_id,
            phase_started_ns=phase_started_ns,
        )
        account(recovered, allow_theory_imports=False)
        assert recovered.root is not None
        if ordinal == 0:
            if anchor is None:
                raise StateCorruptionError("recovered first world lacks its anchor")
            expected_parent = anchor.result.root_refs[0]
        else:
            expected_parent = worlds[ordinal - 1][1].result.root_refs[0]
        if (
            recovered.root.value["world_id"] != world_id
            or recovered.root.value["world_ordinal"] != ordinal
            or recovered.root.value["parent_root_ref"] != expected_parent
        ):
            raise StateCorruptionError(
                "recovered world root differs from its fixed slot/predecessor"
            )
        worlds.append((world_id, recovered))

    if head >= theory_generation + 7:
        aggregation = _recover_one_commit(
            context=context,
            generation=theory_generation + 7,
            graph_path=(
                f"branches/{branch_id}/world-v3/"
                f"g{theory_generation + 7}/graph.json"
            ),
            programme_id=programme_id,
            expected_root_kind=AGGREGATION_ROOT_KIND,
            branch_id=branch_id,
            phase_started_ns=phase_started_ns,
        )
        account(aggregation, allow_theory_imports=False)
        assert aggregation.root is not None
        expected_envelopes = [
            {
                "world_id": world_id,
                "object_ref": recovered.result.root_refs[0],
            }
            for world_id, recovered in worlds
        ]
        if (
            anchor is None
            or len(worlds) != len(WORLD_ORDER)
            or aggregation.root.value["target_id"] != context.target_id
            or aggregation.root.value["run_id"] != context.run_id
            or aggregation.root.value["anchor_root_ref"]
            != anchor.result.root_refs[0]
            or aggregation.root.value["observation_envelopes"]
            != expected_envelopes
        ):
            raise StateCorruptionError(
                "recovered aggregation differs from the exact committed matrix"
            )
    if head == theory_generation + 8:
        reflection = _recover_one_commit(
            context=context,
            generation=head,
            graph_path=f"branches/{branch_id}/world-v3/g{head}/graph.json",
            programme_id=programme_id,
            expected_root_kind=DESCENDANT_REFLECTION_ROOT_KIND,
            branch_id=branch_id,
            phase_started_ns=phase_started_ns,
        )
        account(reflection, allow_theory_imports=False)
        assert reflection.root is not None and aggregation is not None
        if (
            reflection.root.value["target_id"] != context.target_id
            or reflection.root.value["run_id"] != context.run_id
            or reflection.root.value["aggregation_root_ref"]
            != aggregation.result.root_refs[0]
            or reflection.root.value["current_cycle_theory_mutation_authorized"]
            is not False
            or reflection.root.value["automatic_theory_selection_authorized"]
            is not False
        ):
            raise StateCorruptionError(
                "recovered descendant reflection differs from exact aggregation"
            )
    lane_digest = canonical_digest(
        {
            "theory_generation": theory_generation,
            "head_generation": head,
            "commit_receipts": receipt_vector,
            "direct_owner_catalog": [
                {
                    "object_id": object_id,
                    "owner_generation": owner.commit_reference["generation"],
                    "object_ref": owner.object_ref,
                }
                for object_id, owner in sorted(catalog.items())
            ],
        }
    )
    return _RecoveredLane(
        head_generation=head,
        theory_result=theory.result,
        catalog=catalog,
        anchor=anchor,
        worlds=tuple(worlds),
        aggregation=aggregation,
        reflection=reflection,
        local_object_count=local_object_count,
        committed_payload_bytes=committed_payload_bytes,
        lane_digest=lane_digest,
    )


def _freeze_object(value: PreparedContentObject) -> PreparedContentObject:
    """Rebuild one exact object so caller-owned mappings cannot drift."""

    if type(value) is not PreparedContentObject:
        raise ContractError("stage products require exact PreparedContentObject values")
    if type(value.data) is not bytes or canonical_json(value.value) != value.data:
        raise ContractError("stage object value differs from its canonical bytes")
    try:
        object_kind = str(value.ref["object_kind"])
        path = str(value.descriptor["path"])
    except (KeyError, TypeError) as exc:
        raise ContractError("stage object lacks one complete descriptor") from exc
    rebuilt = prepare_content_object(
        object_kind=object_kind,
        value=copy.deepcopy(dict(value.value)),
        path=path,
    )
    if (
        rebuilt.ref != value.ref
        or rebuilt.descriptor != value.descriptor
        or rebuilt.data != value.data
    ):
        raise ContractError("stage object identity is not derived from its exact bytes")
    return rebuilt


def _freeze_product(value: GraphStageProduct) -> _FrozenStageProduct:
    """Seal product state and normalize local-object order by content ID."""

    if type(value) is not GraphStageProduct:
        raise ContractError("producer must return an exact GraphStageProduct")
    if not isinstance(value.state, Mapping):
        raise ContractError("stage product state must be an object")
    if not isinstance(value.root_object_id, str):
        raise ContractError("stage product root_object_id must be a string")
    objects = tuple(_freeze_object(row) for row in value.local_objects)
    by_id = {str(row.ref["object_id"]): row for row in objects}
    if len(by_id) != len(objects):
        raise ContractError("stage product contains duplicate local object IDs")
    if value.root_object_id not in by_id:
        raise ContractError("stage product root is not locally owned")
    ordered = tuple(by_id[object_id] for object_id in sorted(by_id))
    return _FrozenStageProduct(
        state_data=canonical_json(copy.deepcopy(dict(value.state))),
        local_objects=ordered,
        root_object_id=value.root_object_id,
    )


def _stable_topological_order(
    object_ids: Sequence[str],
    edges: Sequence[Mapping[str, str]],
) -> list[str]:
    """Return a lexical Kahn order so producer completion cannot affect bytes."""

    nodes = set(object_ids)
    outgoing: dict[str, set[str]] = {node: set() for node in nodes}
    indegree: dict[str, int] = {node: 0 for node in nodes}
    for edge in edges:
        source = edge["source_object_id"]
        target = edge["target_object_id"]
        if source not in nodes or target not in nodes:
            raise ContractError("stage edge names an object outside the flat catalog")
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    ready = [node for node, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        source = heapq.heappop(ready)
        order.append(source)
        for target in sorted(outgoing[source]):
            indegree[target] -= 1
            if indegree[target] == 0:
                heapq.heappush(ready, target)
    if len(order) != len(nodes):
        raise ContractError("stage payload-derived dependency graph contains a cycle")
    return order


class WorldV3ContentGraphRuntime:
    """Single-writer coordinator for the fixed v3 N-to-N+8 storage lane.

    Construct one runtime while ``theory_result`` is the current verified head.
    Producers themselves may run concurrently; all catalog mutation and commits
    remain in the calling coordinator thread.  :meth:`recover` reconstructs an
    exact partial or complete prefix without caller-supplied object payloads.
    """

    def __init__(
        self,
        *,
        store: DiscoveryTransactionStore,
        theory_result: ContentGraphTransactionResult,
        theory_owned_objects: Sequence[PreparedContentObject],
        branch_id: str = "root",
    ) -> None:
        if type(store) is not DiscoveryTransactionStore:
            raise ContractError("world-v3 runtime requires an exact transaction store")
        if type(theory_result) is not ContentGraphTransactionResult:
            raise ContractError("world-v3 runtime requires an exact theory graph result")
        if not isinstance(branch_id, str):
            raise ContractError("world-v3 branch_id must be a string")
        self._store = store
        self._theory_result = theory_result
        self._theory_generation = theory_result.generation
        self._branch_id = branch_id
        self._programme_id = str(theory_result.commit_ref["programme_id"])
        if (
            theory_result.commit_ref["target_id"] != store.target_id
            or theory_result.commit_ref["run_id"] != store.run_id
        ):
            raise ContractError("theory result belongs to a different transaction store")
        if store.current_generation() != self._theory_generation:
            raise ContractError("theory result must be the current verified graph head")
        reopened = reopen_content_graph_transaction(
            store=store,
            generation=self._theory_generation,
            graph_artifact_path=str(
                theory_result.graph_ref["graph_artifact"]["path"]
            ),
        )
        if reopened != theory_result:
            raise ContractError("theory result is not the exact store-reopened receipt")

        self._catalog: dict[str, _DirectOwner] = {}
        self._anchor_product: _FrozenStageProduct | None = None
        self._anchor_result: ContentGraphTransactionResult | None = None
        self._ready_worlds: dict[str, _FrozenStageProduct] = {}
        self._committed_worlds: dict[str, CommittedWorld] = {}
        self._aggregation_product: _FrozenStageProduct | None = None
        self._aggregation_result: ContentGraphTransactionResult | None = None
        self._reflection_product: _FrozenStageProduct | None = None
        self._reflection_result: ContentGraphTransactionResult | None = None
        self._recovery_measurement: RecoveryMeasurementReceipt | None = None
        self._register_immediate_precommit_catalog()
        self._register_theory_catalog(theory_owned_objects)

    @classmethod
    def recover_from_store(
        cls,
        *,
        store: DiscoveryTransactionStore,
        theory_generation: int,
        theory_graph_artifact_path: str,
        branch_id: str = "root",
    ) -> WorldV3ContentGraphRuntime:
        """Recover a fixed lane without trusting a caller-supplied theory receipt.

        Historical content-graph receipts cannot be reopened through the live
        production helper because that helper deliberately requires its
        generation to be the current store head.  Recovery has a different
        authority boundary: this method reconstructs the historical theory
        receipt from one store-minted verified context, then delegates the
        complete N..N+8 cold/warm/uncached audit to :meth:`recover`.
        """

        if type(store) is not DiscoveryTransactionStore:
            raise ContractError(
                "world-v3 store recovery requires an exact transaction store"
            )
        if type(theory_generation) is not int or theory_generation < 1:
            raise ContractError(
                "world-v3 store recovery theory generation must be positive"
            )
        if (
            not isinstance(theory_graph_artifact_path, str)
            or not theory_graph_artifact_path
        ):
            raise ContractError(
                "world-v3 theory graph artifact path must be non-empty"
            )
        canonical_path = PurePosixPath(theory_graph_artifact_path)
        if (
            canonical_path.is_absolute()
            or canonical_path.as_posix() != theory_graph_artifact_path
            or "." in canonical_path.parts
            or ".." in canonical_path.parts
            or "\\" in theory_graph_artifact_path
        ):
            raise ContractError(
                "world-v3 theory graph artifact path must be canonical and relative"
            )
        if not isinstance(branch_id, str):
            raise ContractError("world-v3 recovery branch_id must be a string")

        with store.verified_artifact_context() as context:
            head = context.current_generation
            if head < theory_generation or head > theory_generation + 8:
                raise ContractError(
                    "world-v3 recovery head lies outside the fixed N..N+8 lane"
                )
            theory_commit = context.read_commit(theory_generation)
            programme_id = theory_commit.state.get("programme_id")
            if not isinstance(programme_id, str) or not programme_id:
                raise StateCorruptionError(
                    "recovered theory commit lacks one programme identity"
                )
            phase_started_ns = time.perf_counter_ns()
            theory_result = _recover_one_commit(
                context=context,
                generation=theory_generation,
                graph_path=theory_graph_artifact_path,
                programme_id=programme_id,
                expected_root_kind=None,
                branch_id=branch_id,
                phase_started_ns=phase_started_ns,
            ).result

        return cls.recover(
            store=store,
            theory_generation=theory_generation,
            theory_result=theory_result,
            branch_id=branch_id,
        )

    @classmethod
    def recover(
        cls,
        *,
        store: DiscoveryTransactionStore,
        theory_generation: int,
        theory_result: ContentGraphTransactionResult,
        branch_id: str = "root",
    ) -> WorldV3ContentGraphRuntime:
        """Recover one exact fixed-path lane through cold, warm, and uncached replay.

        The supplied theory receipt is the explicit trust root.  Every later
        commit is reconstructed from store-verified bytes, its local owners are
        added to a fresh flat catalog, and its imports must point back to those
        exact owners.  The method spawns no child process; the separate
        fresh-process test exercises portability of this same entrypoint.
        """

        if type(store) is not DiscoveryTransactionStore:
            raise ContractError("world-v3 recovery requires an exact transaction store")
        if type(theory_generation) is not int or theory_generation < 1:
            raise ContractError("world-v3 recovery theory generation must be positive")
        if type(theory_result) is not ContentGraphTransactionResult:
            raise ContractError("world-v3 recovery requires an exact theory result")
        if theory_result.generation != theory_generation:
            raise ContractError(
                "explicit theory generation differs from its result identity"
            )
        if not isinstance(branch_id, str):
            raise ContractError("world-v3 recovery branch_id must be a string")
        if (
            theory_result.commit_ref["target_id"] != store.target_id
            or theory_result.commit_ref["run_id"] != store.run_id
        ):
            raise ContractError(
                "world-v3 recovery cannot cross another target or run"
            )

        with store.verified_artifact_context() as context:
            cold_started = time.perf_counter_ns()
            cold = _audit_recovery_lane(
                context=context,
                theory_generation=theory_generation,
                theory_result=theory_result,
                branch_id=branch_id,
                phase_started_ns=cold_started,
            )
            cold_elapsed = time.perf_counter_ns() - cold_started
            warm_started = time.perf_counter_ns()
            warm = _audit_recovery_lane(
                context=context,
                theory_generation=theory_generation,
                theory_result=theory_result,
                branch_id=branch_id,
                phase_started_ns=warm_started,
            )
            warm_elapsed = time.perf_counter_ns() - warm_started
        # Opening a new store-minted context forces one independent, uncached
        # exact end-to-end replay rather than treating the warm pass as enough.
        with store.verified_artifact_context() as context:
            uncached_started = time.perf_counter_ns()
            uncached = _audit_recovery_lane(
                context=context,
                theory_generation=theory_generation,
                theory_result=theory_result,
                branch_id=branch_id,
                phase_started_ns=uncached_started,
            )
            uncached_elapsed = time.perf_counter_ns() - uncached_started
        if any(
            elapsed > MAX_WORLD_V3_RECOVERY_PHASE_NS
            for elapsed in (cold_elapsed, warm_elapsed, uncached_elapsed)
        ):
            raise ContractError("world-v3 recovery exceeded its fixed phase-time ceiling")
        total_elapsed = cold_elapsed + warm_elapsed + uncached_elapsed
        if total_elapsed > MAX_WORLD_V3_RECOVERY_TOTAL_NS:
            raise ContractError("world-v3 recovery exceeded its fixed total-time ceiling")
        if store.current_generation() != uncached.head_generation:
            raise ContractError("world-v3 recovery head drifted after exact replay")
        exact_warm = (
            warm.lane_digest == cold.lane_digest
            and warm.local_object_count == cold.local_object_count
            and warm.committed_payload_bytes == cold.committed_payload_bytes
        )
        exact_uncached = (
            uncached.lane_digest == cold.lane_digest
            and uncached.local_object_count == cold.local_object_count
            and uncached.committed_payload_bytes == cold.committed_payload_bytes
        )
        if not exact_warm or not exact_uncached:
            raise StateCorruptionError(
                "world-v3 cold/warm/uncached recovery projections disagree"
            )

        runtime = object.__new__(cls)
        runtime._store = store
        runtime._theory_result = theory_result
        runtime._theory_generation = theory_generation
        runtime._branch_id = branch_id
        runtime._programme_id = str(theory_result.commit_ref["programme_id"])
        runtime._catalog = dict(uncached.catalog)
        runtime._anchor_product = (
            uncached.anchor.frozen_product
            if uncached.anchor is not None
            else None
        )
        runtime._anchor_result = (
            uncached.anchor.result if uncached.anchor is not None else None
        )
        runtime._ready_worlds = {
            world_id: recovered.frozen_product
            for world_id, recovered in uncached.worlds
            if recovered.frozen_product is not None
        }
        runtime._committed_worlds = {
            world_id: CommittedWorld(
                world_id=world_id,
                world_ordinal=ordinal,
                generation=theory_generation + 2 + ordinal,
                result=recovered.result,
            )
            for ordinal, (world_id, recovered) in enumerate(uncached.worlds)
        }
        runtime._aggregation_product = (
            uncached.aggregation.frozen_product
            if uncached.aggregation is not None
            else None
        )
        runtime._aggregation_result = (
            uncached.aggregation.result
            if uncached.aggregation is not None
            else None
        )
        runtime._reflection_product = (
            uncached.reflection.frozen_product
            if uncached.reflection is not None
            else None
        )
        runtime._reflection_result = (
            uncached.reflection.result
            if uncached.reflection is not None
            else None
        )
        runtime._recovery_measurement = RecoveryMeasurementReceipt(
            theory_generation=theory_generation,
            head_generation=uncached.head_generation,
            commit_count=uncached.head_generation - theory_generation + 1,
            local_object_count=uncached.local_object_count,
            committed_payload_bytes=uncached.committed_payload_bytes,
            child_processes_spawned=0,
            cold_recovery_elapsed_ns=cold_elapsed,
            warm_reopen_elapsed_ns=warm_elapsed,
            uncached_replay_elapsed_ns=uncached_elapsed,
            total_recovery_elapsed_ns=total_elapsed,
            lane_digest=uncached.lane_digest,
            exact_warm_reopen=exact_warm,
            exact_uncached_replay=exact_uncached,
        )
        return runtime

    @classmethod
    def recover_in_fresh_process(
        cls,
        *,
        store: DiscoveryTransactionStore,
        theory_generation: int,
        theory_result: ContentGraphTransactionResult,
        branch_id: str = "root",
        relocated_from: Path | str | None = None,
        deadline_ns: int = MAX_WORLD_V3_FRESH_PROCESS_NS,
    ) -> FreshProcessRecoveryReceipt:
        """Recover in one scrubbed, parent-supervised POSIX process group."""

        return _recover_world_v3_in_fresh_process(
            store=store,
            theory_generation=theory_generation,
            theory_result=theory_result,
            branch_id=branch_id,
            relocated_from=relocated_from,
            deadline_ns=deadline_ns,
        )

    @property
    def theory_generation(self) -> int:
        return self._theory_generation

    @property
    def theory_result(self) -> ContentGraphTransactionResult:
        """Return the explicit verified theory commit that roots this lane."""

        return self._theory_result

    @property
    def recovery_measurement(self) -> RecoveryMeasurementReceipt | None:
        """Return recovery measurements, or ``None`` for a newly started lane."""

        return self._recovery_measurement

    @property
    def anchor_result(self) -> ContentGraphTransactionResult | None:
        return self._anchor_result

    @property
    def committed_worlds(self) -> tuple[CommittedWorld, ...]:
        return tuple(
            self._committed_worlds[world_id]
            for world_id in WORLD_ORDER
            if world_id in self._committed_worlds
        )

    @property
    def aggregation_result(self) -> ContentGraphTransactionResult | None:
        return self._aggregation_result

    @property
    def reflection_result(self) -> ContentGraphTransactionResult | None:
        """Return the N+8 immutable return when the canonical lane is complete."""

        return self._reflection_result

    @property
    def owner_catalog(self) -> tuple[tuple[str, int], ...]:
        """Expose only object ID and direct-owner generation for audit."""

        return tuple(
            sorted(
                (
                    object_id,
                    int(owner.commit_reference["generation"]),
                )
                for object_id, owner in self._catalog.items()
            )
        )

    def expected_generation_for_world(self, world_id: str) -> int:
        """Return the one generation assigned to a closed world identifier."""

        try:
            ordinal = WORLD_ORDER.index(world_id)
        except ValueError as exc:
            raise ContractError(f"unknown world-v3 world_id: {world_id!r}") from exc
        return self._theory_generation + 2 + ordinal

    def _register_theory_catalog(
        self,
        supplied_objects: Sequence[PreparedContentObject],
    ) -> None:
        """Verify that the initial flat catalog is exactly theory-N local data."""

        frozen = tuple(_freeze_object(row) for row in supplied_objects)
        supplied_by_id = {str(row.ref["object_id"]): row for row in frozen}
        if len(supplied_by_id) != len(frozen):
            raise ContractError("theory owner catalog contains duplicate object IDs")
        graph_path = str(self._theory_result.graph_ref["graph_artifact"]["path"])
        with self._store.verified_artifact_context() as context:
            resolver = StoreVerifiedContentObjectGraph(
                store=self._store,
                context=context,
                generation=self._theory_generation,
                graph_artifact_path=graph_path,
            )
            graph = resolver.graph
            owned_closure = resolver.verify_closure_with_direct_owners()
            local_ids = {
                str(row["ref"]["object_id"]) for row in graph["local_descriptors"]
            }
            if set(supplied_by_id) != local_ids:
                raise ContractError(
                    "theory owner catalog must equal all locally owned theory objects"
                )
            for object_id, supplied in supplied_by_id.items():
                resolved = resolver.resolve(object_id)
                if (
                    resolved.ref != supplied.ref
                    or resolved.value != supplied.value
                    or resolved.data != supplied.data
                ):
                    raise ContractError(
                        "theory owner catalog differs from store-verified bytes"
                    )
        for owned in owned_closure:
            object_id = str(owned.resolved.ref["object_id"])
            self._catalog[object_id] = _DirectOwner(
                object_ref_data=canonical_json(owned.resolved.ref),
                commit_reference_data=canonical_json(
                    owned.owner_commit_reference
                ),
            )

    def _register_immediate_precommit_catalog(self) -> None:
        """Seed only exact direct owners from the committed N-1 graph.

        The anchor's committed-ancestor carrier must point to genuine N-1
        evidence without re-owning those bytes at theory N.  This bounded
        lookup admits only the immediately preceding verified commit and one
        exact content graph; it is not a general stale-history authority API.
        """

        generation = self._theory_generation - 1
        if generation < 1:
            return
        with self._store.verified_artifact_context() as context:
            paths = context.artifact_paths(generation)
            graph_paths = tuple(path for path in paths if path.endswith("/graph.json"))
            if len(graph_paths) != 1:
                raise ContractError(
                    "world-v3 theory N requires one exact N-1 content graph"
                )
            recovered = _recover_one_commit(
                context=context,
                generation=generation,
                graph_path=graph_paths[0],
                programme_id=self._programme_id,
                expected_root_kind=None,
                branch_id=self._branch_id,
                phase_started_ns=time.perf_counter_ns(),
            )
        commit_data = canonical_json(recovered.result.commit_ref)
        for row in recovered.local_objects:
            object_id = str(row.ref["object_id"])
            if object_id in self._catalog:
                raise ContractError(
                    "precommit owner collides with an existing runtime owner"
                )
            self._catalog[object_id] = _DirectOwner(
                object_ref_data=canonical_json(row.ref),
                commit_reference_data=commit_data,
            )

    def _register_committed_locals(
        self,
        local_objects: Sequence[PreparedContentObject],
        result: ContentGraphTransactionResult,
    ) -> None:
        """Mint direct-owner entries only after exact content-graph reopening."""

        commit_data = canonical_json(result.commit_ref)
        for row in local_objects:
            object_id = str(row.ref["object_id"])
            proposed = _DirectOwner(
                object_ref_data=canonical_json(row.ref),
                commit_reference_data=commit_data,
            )
            current = self._catalog.get(object_id)
            if current is not None and current != proposed:
                raise ContractError(
                    "one content object cannot acquire two direct owners in one lane"
                )
            self._catalog[object_id] = proposed

    def _validate_state(
        self,
        product: _FrozenStageProduct,
        *,
        generation: int,
    ) -> None:
        state = product.state
        if (
            state.get("target_id") != self._store.target_id
            or state.get("run_id") != self._store.run_id
            or state.get("programme_id") != self._programme_id
            or state.get("generation") != generation
        ):
            raise ContractError(
                "stage state must preserve target/run/programme and fixed generation"
            )

    def _root(
        self,
        product: _FrozenStageProduct,
        *,
        expected_kind: str,
        generation: int,
    ) -> PreparedContentObject:
        self._validate_state(product, generation=generation)
        by_id = {
            str(row.ref["object_id"]): row for row in product.local_objects
        }
        root = by_id[product.root_object_id]
        if root.ref["object_kind"] != expected_kind:
            raise ContractError(
                f"stage root must have object kind {expected_kind!r}"
            )
        validate_role_bound_object(root.ref, root.value)
        required_prefix = (
            f"branches/{self._branch_id}/world-v3/g{generation}/objects/"
        )
        for row in product.local_objects:
            if not str(row.descriptor["path"]).startswith(required_prefix):
                raise ContractError(
                    "stage local object path is not bound to its fixed generation"
                )
        return root

    def _build_transaction(
        self,
        product: _FrozenStageProduct,
        *,
        generation: int,
        expected_root_kind: str,
    ) -> PreparedContentGraphTransaction:
        """Build one deterministic graph from local bytes and direct owners."""

        self._root(
            product,
            expected_kind=expected_root_kind,
            generation=generation,
        )
        local_by_id = {
            str(row.ref["object_id"]): row for row in product.local_objects
        }
        reowned_ids = sorted(set(local_by_id) & set(self._catalog))
        if reowned_ids:
            raise ContractError(
                "stage local object already has a committed direct owner: "
                + reowned_ids[0]
            )
        # A stage is a local role-object closure, not a root plus arbitrary
        # sidecars.  Deriving every local object's references both validates
        # each strict role payload and makes local request/result/reflection or
        # certificate chains participate in the graph.  The generic graph
        # validator below then rejects any extra local object outside the
        # declared root's backwards closure.
        edges: list[dict[str, str]] = []
        for row in product.local_objects:
            edges.extend(
                derive_content_object_edges(
                    object_ref=row.ref,
                    payload=row.value,
                )
            )
        edges.sort(
            key=lambda row: (
                row["source_object_id"],
                row["target_object_id"],
                row["edge_kind"],
            )
        )
        imported_ids = sorted(
            {
                edge["source_object_id"]
                for edge in edges
                if edge["source_object_id"] not in local_by_id
            }
        )
        missing = [object_id for object_id in imported_ids if object_id not in self._catalog]
        if missing:
            raise MissingCommittedDependency(missing)
        handles = [
            build_committed_object_handle(
                source_commit_reference=self._catalog[object_id].commit_reference,
                object_ref=self._catalog[object_id].object_ref,
            )
            for object_id in imported_ids
        ]
        all_ids = [*local_by_id, *imported_ids]
        order = _stable_topological_order(all_ids, edges)
        graph = build_content_object_graph(
            local_descriptors=[
                local_by_id[object_id].descriptor
                for object_id in sorted(local_by_id)
            ],
            imported_handles=handles,
            ordered_roots=[product.root_object_id],
            edges=edges,
            topological_order=order,
        )
        expected_generation = generation - 1
        return prepare_content_graph_transaction(
            expected_generation=expected_generation,
            state=product.state,
            namespace=Namespace(
                self._store.target_id,
                self._store.run_id,
                self._branch_id,
                expected_generation,
            ),
            graph_artifact_path=(
                f"branches/{self._branch_id}/world-v3/g{generation}/graph.json"
            ),
            graph=graph,
            local_objects=product.local_objects,
        )

    def _commit_product(
        self,
        product: _FrozenStageProduct,
        *,
        generation: int,
        expected_root_kind: str,
    ) -> ContentGraphTransactionResult:
        transaction = self._build_transaction(
            product,
            generation=generation,
            expected_root_kind=expected_root_kind,
        )
        result = commit_content_graph_transaction(
            store=self._store,
            transaction=transaction,
        )
        if result.generation != generation:
            raise ContractError("content-graph kernel returned a non-fixed generation")
        root = next(
            row
            for row in product.local_objects
            if row.ref["object_id"] == product.root_object_id
        )
        if result.root_refs != (root.ref,):
            raise ContractError("committed graph root differs from the stage product")
        self._register_committed_locals(product.local_objects, result)
        return result

    def commit_anchor(
        self,
        product: GraphStageProduct,
    ) -> ContentGraphTransactionResult:
        """Commit or byte-identically retry the sole N+1 anchor."""

        frozen = _freeze_product(product)
        if self._anchor_product is not None and frozen != self._anchor_product:
            raise ContractError("a different anchor product is already registered")
        generation = self._theory_generation + 1
        root = self._root(
            frozen,
            expected_kind=ANCHOR_ROOT_KIND,
            generation=generation,
        )
        if (
            root.value["target_id"] != self._store.target_id
            or root.value["run_id"] != self._store.run_id
            or root.value["prior_state_version"] != self._theory_generation - 1
        ):
            raise ContractError(
                "anchor scalar identity differs from the committed N-1 precommit state"
            )
        if self._anchor_result is None:
            committed = self._commit_product(
                frozen,
                generation=generation,
                expected_root_kind=ANCHOR_ROOT_KIND,
            )
            # Failed validation or CAS must not poison selective retry with an
            # uncommitted proposal.  Register product identity only after the
            # storage kernel returns its exact reopened receipt.
            self._anchor_product = frozen
            self._anchor_result = committed
        return self._anchor_result

    def submit_world_product(
        self,
        world_id: str,
        product: GraphStageProduct,
    ) -> None:
        """Freeze one completion without granting it permission to commit."""

        try:
            ordinal = WORLD_ORDER.index(world_id)
        except ValueError as exc:
            raise ContractError(f"unknown world-v3 world_id: {world_id!r}") from exc
        frozen = _freeze_product(product)
        generation = self.expected_generation_for_world(world_id)
        root = self._root(
            frozen,
            expected_kind=WORLD_ROOT_KIND,
            generation=generation,
        )
        if (
            root.value["world_id"] != world_id
            or root.value["world_ordinal"] != ordinal
        ):
            raise ContractError("world product discriminator differs from its slot")
        existing = self._ready_worlds.get(world_id)
        committed = self._committed_worlds.get(world_id)
        if existing is not None and existing != frozen:
            raise ContractError("a different product is already registered for this world")
        if committed is not None and existing != frozen:
            raise ContractError("a committed world cannot be replaced")
        self._ready_worlds[world_id] = frozen

    def _assert_world_parent(
        self,
        world_id: str,
        product: _FrozenStageProduct,
    ) -> None:
        ordinal = WORLD_ORDER.index(world_id)
        root = next(
            row
            for row in product.local_objects
            if row.ref["object_id"] == product.root_object_id
        )
        if ordinal == 0:
            if self._anchor_result is None:
                raise ContractError("the no-probe world requires the committed anchor")
            expected_parent = self._anchor_result.root_refs[0]
        else:
            predecessor = self._committed_worlds.get(WORLD_ORDER[ordinal - 1])
            if predecessor is None:
                raise ContractError("world predecessor is not committed")
            expected_parent = predecessor.result.root_refs[0]
        if root.value["parent_root_ref"] != expected_parent:
            raise ContractError(
                "world parent_root_ref is not the exact committed predecessor"
            )

    def _incomplete(
        self,
        *,
        failed_world_ids: Sequence[str] = (),
    ) -> IncompleteWorldSupport | None:
        committed_ids = tuple(
            world_id for world_id in WORLD_ORDER if world_id in self._committed_worlds
        )
        if len(committed_ids) == len(WORLD_ORDER):
            return None
        next_world_id = WORLD_ORDER[len(committed_ids)]
        ready_blocked = tuple(
            world_id
            for world_id in WORLD_ORDER[len(committed_ids) + 1 :]
            if world_id in self._ready_worlds
        )
        not_ready = tuple(
            world_id
            for world_id in WORLD_ORDER[len(committed_ids) :]
            if world_id not in self._ready_worlds
        )
        return IncompleteWorldSupport(
            theory_generation=self._theory_generation,
            anchor_generation=self._theory_generation + 1,
            committed_world_ids=committed_ids,
            ready_but_blocked_world_ids=ready_blocked,
            not_ready_world_ids=not_ready,
            failed_world_ids=tuple(
                world_id
                for world_id in WORLD_ORDER
                if world_id in set(failed_world_ids)
            ),
            next_world_id=next_world_id,
            next_expected_generation=self.expected_generation_for_world(
                next_world_id
            ),
        )

    def commit_ready_prefix(
        self,
        *,
        failed_world_ids: Sequence[str] = (),
    ) -> WorldPrefixCommit:
        """Serially commit exactly the longest currently ready world prefix."""

        if self._anchor_result is None:
            raise ContractError("world commits require the exact committed anchor")
        next_ordinal = len(self._committed_worlds)
        while next_ordinal < len(WORLD_ORDER):
            world_id = WORLD_ORDER[next_ordinal]
            product = self._ready_worlds.get(world_id)
            if product is None:
                break
            self._assert_world_parent(world_id, product)
            generation = self.expected_generation_for_world(world_id)
            result = self._commit_product(
                product,
                generation=generation,
                expected_root_kind=WORLD_ROOT_KIND,
            )
            self._committed_worlds[world_id] = CommittedWorld(
                world_id=world_id,
                world_ordinal=next_ordinal,
                generation=generation,
                result=result,
            )
            next_ordinal += 1
        return WorldPrefixCommit(
            committed_worlds=self.committed_worlds,
            incomplete_support=self._incomplete(
                failed_world_ids=failed_world_ids
            ),
        )

    def run_world_producers(
        self,
        producers: Mapping[str, WorldProducer],
        *,
        max_workers: int = len(WORLD_ORDER),
    ) -> ParallelWorldProduction:
        """Run isolated completions in parallel and publish from one thread."""

        if not isinstance(producers, Mapping):
            raise ContractError("world producers must be a world-id mapping")
        unknown = sorted(set(producers) - set(WORLD_ORDER))
        if unknown:
            raise ContractError(f"unknown world producer: {unknown[0]}")
        if (
            isinstance(max_workers, bool)
            or not isinstance(max_workers, int)
            or max_workers < 1
            or max_workers > len(WORLD_ORDER)
        ):
            raise ContractError("world producer worker count must be between one and five")
        for world_id, producer in producers.items():
            if not callable(producer):
                raise ContractError(f"world producer is not callable: {world_id}")

        completion_order: list[str] = []
        failures: list[WorldProducerFailure] = []
        future_world: dict[Future[GraphStageProduct], str] = {}
        with ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="world-v3-producer",
        ) as executor:
            for world_id in WORLD_ORDER:
                producer = producers.get(world_id)
                if producer is not None:
                    future_world[executor.submit(producer)] = world_id
            for future in as_completed(future_world):
                world_id = future_world[future]
                completion_order.append(world_id)
                try:
                    self.submit_world_product(world_id, future.result())
                except Exception as exc:
                    failures.append(
                        WorldProducerFailure(
                            world_id=world_id,
                            failure_kind="producer_or_product_failure",
                            exception_type=type(exc).__name__,
                            message=str(exc),
                        )
                    )
                self.commit_ready_prefix(
                    failed_world_ids=[row.world_id for row in failures]
                )
        prefix = self.commit_ready_prefix(
            failed_world_ids=[row.world_id for row in failures]
        )
        return ParallelWorldProduction(
            completion_order=tuple(completion_order),
            failures=tuple(
                sorted(failures, key=lambda row: WORLD_ORDER.index(row.world_id))
            ),
            prefix=prefix,
        )

    def commit_aggregation(
        self,
        product: GraphStageProduct,
        *,
        failed_world_ids: Sequence[str] = (),
    ) -> AggregationCommit:
        """Commit N+7 only from the five exact store-minted world roots."""

        incomplete = self._incomplete(failed_world_ids=failed_world_ids)
        if incomplete is not None:
            return AggregationCommit(result=None, incomplete_support=incomplete)
        frozen = _freeze_product(product)
        if (
            self._aggregation_product is not None
            and self._aggregation_product != frozen
        ):
            raise ContractError("a different aggregation product is already registered")
        generation = self._theory_generation + 7
        root = self._root(
            frozen,
            expected_kind=AGGREGATION_ROOT_KIND,
            generation=generation,
        )
        if (
            root.value["target_id"] != self._store.target_id
            or root.value["run_id"] != self._store.run_id
            or root.value["anchor_root_ref"] != self._anchor_result.root_refs[0]
        ):
            raise ContractError("aggregation scalar or anchor identity drifted")
        expected_envelopes = [
            {
                "world_id": world_id,
                "object_ref": self._committed_worlds[world_id].result.root_refs[0],
            }
            for world_id in WORLD_ORDER
        ]
        if root.value["observation_envelopes"] != expected_envelopes:
            raise ContractError(
                "aggregation does not name the exact five committed world roots"
            )
        if self._aggregation_result is None:
            committed = self._commit_product(
                frozen,
                generation=generation,
                expected_root_kind=AGGREGATION_ROOT_KIND,
            )
            self._aggregation_product = frozen
            self._aggregation_result = committed
        return AggregationCommit(
            result=self._aggregation_result,
            incomplete_support=None,
        )

    def commit_descendant_reflection(
        self,
        product: GraphStageProduct,
    ) -> DescendantReflectionCommit:
        """Commit the sole N+8 immutable return from the exact N+7 root."""

        if self._aggregation_result is None:
            raise ContractError(
                "descendant reflection requires the exact committed aggregation"
            )
        frozen = _freeze_product(product)
        if self._reflection_product is not None and frozen != self._reflection_product:
            raise ContractError(
                "a different descendant reflection product is already registered"
            )
        generation = self._theory_generation + 8
        root = self._root(
            frozen,
            expected_kind=DESCENDANT_REFLECTION_ROOT_KIND,
            generation=generation,
        )
        if (
            root.value["target_id"] != self._store.target_id
            or root.value["run_id"] != self._store.run_id
            or root.value["aggregation_root_ref"]
            != self._aggregation_result.root_refs[0]
            or root.value["reflection_disposition"]
            != "immutable_input_for_later_theory_reflection"
            or root.value["result_effect"]
            != "later_theory_cycle_reflection_input_only"
            or root.value["current_cycle_theory_mutation_authorized"] is not False
            or root.value["automatic_theory_selection_authorized"] is not False
            or root.value["proof_authorized"] is not False
            or root.value["physics_authority"] is not False
        ):
            raise ContractError(
                "descendant reflection exceeds its exact later-cycle boundary"
            )
        if self._reflection_result is None:
            committed = self._commit_product(
                frozen,
                generation=generation,
                expected_root_kind=DESCENDANT_REFLECTION_ROOT_KIND,
            )
            self._reflection_product = frozen
            self._reflection_result = committed
        return DescendantReflectionCommit(result=self._reflection_result)

    def require_active_current_descendant_closure(self) -> Any:
        """Reopen and validate N+8 under one exact current-head store context."""

        if self._reflection_result is None:
            raise ContractError(
                "active canonical experiment authority requires N+8 reflection"
            )
        expected_generation = self._theory_generation + 8
        if self._store.current_generation() != expected_generation:
            raise ContractError(
                "descendant experiment closure is stale or not the active current head"
            )
        from .world_v3_closure import validate_world_v3_descendant_closure

        graph_path = str(
            self._reflection_result.graph_ref["graph_artifact"]["path"]
        )
        with self._store.verified_artifact_context() as context:
            if context.current_generation != expected_generation:
                raise ContractError(
                    "descendant experiment current head drifted before replay"
                )
            resolver = StoreVerifiedContentObjectGraph(
                store=self._store,
                context=context,
                generation=expected_generation,
                graph_artifact_path=graph_path,
            )
            owned = resolver.verify_closure_with_direct_owners()
            objects = tuple(row.resolved for row in owned)
            generations = {
                str(row.resolved.ref["object_id"]): int(
                    row.owner_commit_reference["generation"]
                )
                for row in owned
            }
            verified = validate_world_v3_descendant_closure(
                objects,
                self._reflection_result.root_refs[0],
                theory_generation=self._theory_generation,
                committed_generations=generations,
            )
            context.assert_owned_by(self._store)
        if (
            self._store.current_generation() != expected_generation
            or verified.reflection_root_ref
            != self._reflection_result.root_refs[0]
        ):
            raise ContractError(
                "descendant experiment authority ceased to be exact active-current"
            )
        return verified


def run_canonical_descendant_experiment_v3(
    *,
    store: DiscoveryTransactionStore,
    theory_result: ContentGraphTransactionResult,
    theory_owned_objects: Sequence[PreparedContentObject],
    anchor_product: GraphStageProduct,
    world_producers: Mapping[str, WorldProducer],
    aggregation_product: GraphStageProduct,
    reflection_product: GraphStageProduct,
    branch_id: str = "root",
    max_workers: int = len(WORLD_ORDER),
) -> CanonicalDescendantExperimentV3Result:
    """Execute the mandatory theory-subordinate descendant chronology.

    World callbacks run concurrently but have no commit capability.  The
    coordinator serializes their frozen products in the closed world order,
    commits N+7 aggregation and N+8 immutable reflection, then reopens the
    complete active closure under a store-minted current-head context.  Any
    partial producer wave remains noncanonical and cannot return this type.
    """

    runtime = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_owned_objects,
        branch_id=branch_id,
    )
    anchor = runtime.commit_anchor(anchor_product)
    parallel = runtime.run_world_producers(
        world_producers,
        max_workers=max_workers,
    )
    if parallel.failures or not parallel.prefix.complete:
        failed = ", ".join(row.world_id for row in parallel.failures)
        raise ContractError(
            "canonical descendant experiment production is incomplete"
            + (f": {failed}" if failed else "")
        )
    aggregation = runtime.commit_aggregation(aggregation_product)
    if aggregation.result is None:
        raise ContractError(
            "canonical descendant aggregation remained structurally incomplete"
        )
    reflection = runtime.commit_descendant_reflection(reflection_product).result
    verified = runtime.require_active_current_descendant_closure()
    return CanonicalDescendantExperimentV3Result(
        theory_generation=runtime.theory_generation,
        anchor=anchor,
        worlds=runtime.committed_worlds,
        aggregation=aggregation.result,
        reflection=reflection,
        parallel_production=parallel,
        verified_descendant_closure=verified,
    )


def _file_content_identity(path: Path, *, label: str) -> dict[str, Any]:
    """Identify one executable/module by absolute locator and exact bytes."""

    absolute = path.absolute()
    try:
        resolved = absolute.resolve(strict=True)
        metadata = resolved.stat()
        data = resolved.read_bytes()
    except OSError as exc:
        raise FreshProcessRecoveryError(
            "identity_error",
            f"{label} cannot be read exactly",
        ) from exc
    if not stat.S_ISREG(metadata.st_mode) or len(data) != metadata.st_size:
        raise FreshProcessRecoveryError(
            "identity_error",
            f"{label} is not one stable regular file",
        )
    identity = {
        "identity_kind": label,
        "launch_path": str(absolute),
        "resolved_path": str(resolved),
        "size_bytes": len(data),
        "sha256": bytes_digest(data),
        "launch_path_is_symlink": absolute.is_symlink(),
    }
    identity["identity_digest"] = canonical_digest(identity)
    return identity


def _fresh_environment_identity(
    environment: Mapping[str, str],
) -> dict[str, Any]:
    identity = {
        "identity_kind": "scrubbed_worker_environment",
        "keys": sorted(environment),
        "environment_digest": canonical_digest(dict(environment)),
    }
    identity["identity_digest"] = canonical_digest(identity)
    return identity


def _relocation_request_identity(
    *,
    destination_root: Path,
    relocated_from: Path | str | None,
) -> dict[str, Any]:
    source_root: Path | None = None
    if relocated_from is not None:
        source_root = Path(relocated_from).absolute()
        if source_root.exists() or source_root.is_symlink():
            raise FreshProcessRecoveryError(
                "relocation_identity_error",
                "relocation source must be absent before launch",
            )
        if source_root == destination_root:
            raise FreshProcessRecoveryError(
                "relocation_identity_error",
                "relocation source and destination must differ",
            )
    identity = {
        "identity_kind": "world_v3_store_relocation",
        "mode": "copy_then_delete_source" if source_root else "in_place",
        "source_root": str(source_root) if source_root else None,
        "source_absent_at_launch": (
            source_root is not None
            and not source_root.exists()
            and not source_root.is_symlink()
        ),
        "destination_root": str(destination_root),
        "destination_present_at_launch": destination_root.is_dir(),
    }
    identity["identity_digest"] = canonical_digest(identity)
    return identity


def _fresh_process_limits() -> dict[str, int]:
    return {
        "deadline_ns": MAX_WORLD_V3_FRESH_PROCESS_NS,
        "cpu_ns": MAX_WORLD_V3_FRESH_PROCESS_CPU_NS,
        "rss_bytes": MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES,
        "process_group_members": MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS,
        "request_bytes": MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES,
        "stdout_bytes": MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES,
        "stderr_bytes": MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES,
    }


def _result_from_protocol_mapping(
    value: Mapping[str, Any],
) -> ContentGraphTransactionResult:
    try:
        result = ContentGraphTransactionResult(
            request_digest=str(value["request_digest"]),
            idempotency_key=str(value["idempotency_key"]),
            _commit_reference_data=canonical_json(value["commit_reference"]),
            _graph_reference_data=canonical_json(value["graph_reference"]),
            _root_reference_data=tuple(
                canonical_json(row) for row in value["root_references"]
            ),
        )
        result.as_dict()
    except (KeyError, TypeError, ContractError) as exc:
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "theory result protocol projection is invalid",
        ) from exc
    if result.as_dict() != dict(value):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "theory result protocol projection has extra or changed fields",
        )
    return result


def _validate_recovery_measurement_mapping(
    value: Mapping[str, Any],
) -> RecoveryMeasurementReceipt:
    integer_fields = (
        "theory_generation",
        "head_generation",
        "commit_count",
        "local_object_count",
        "committed_payload_bytes",
        "child_processes_spawned",
        "cold_recovery_elapsed_ns",
        "warm_reopen_elapsed_ns",
        "uncached_replay_elapsed_ns",
        "total_recovery_elapsed_ns",
    )
    if any(type(value.get(name)) is not int for name in integer_fields):
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "in-process receipt integer fields are invalid",
        )
    if any(int(value[name]) < 0 for name in integer_fields):
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "in-process receipt contains a negative measurement",
        )
    if (
        type(value.get("exact_warm_reopen")) is not bool
        or type(value.get("exact_uncached_replay")) is not bool
        or not isinstance(value.get("lane_digest"), str)
    ):
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "in-process receipt exactness fields are invalid",
        )
    try:
        receipt = RecoveryMeasurementReceipt(
            theory_generation=int(value["theory_generation"]),
            head_generation=int(value["head_generation"]),
            commit_count=int(value["commit_count"]),
            local_object_count=int(value["local_object_count"]),
            committed_payload_bytes=int(value["committed_payload_bytes"]),
            child_processes_spawned=int(
                value["child_processes_spawned"]
            ),
            cold_recovery_elapsed_ns=int(
                value["cold_recovery_elapsed_ns"]
            ),
            warm_reopen_elapsed_ns=int(
                value["warm_reopen_elapsed_ns"]
            ),
            uncached_replay_elapsed_ns=int(
                value["uncached_replay_elapsed_ns"]
            ),
            total_recovery_elapsed_ns=int(
                value["total_recovery_elapsed_ns"]
            ),
            lane_digest=str(value["lane_digest"]),
            exact_warm_reopen=bool(value["exact_warm_reopen"]),
            exact_uncached_replay=bool(value["exact_uncached_replay"]),
            authority_boundary=str(value["authority_boundary"]),
        )
    except KeyError as exc:
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "in-process receipt is incomplete",
        ) from exc
    if receipt.as_dict() != dict(value):
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "in-process receipt digest, limits, or fields differ",
        )
    return receipt


def _process_group_exists(process_group_id: int) -> bool:
    try:
        os.killpg(process_group_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _sample_process_group(
    process_group_id: int,
) -> tuple[int, int]:
    ps_path = Path("/bin/ps")
    command = (
        [str(ps_path), "-axo", "pgid=,rss="]
        if ps_path.exists()
        else ["ps", "-axo", "pgid=,rss="]
    )
    try:
        sampled = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=0.25,
            env=dict(_FRESH_PROCESS_ENVIRONMENT),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise FreshProcessRecoveryError(
            "process_measurement_error",
            "parent could not sample the worker process group",
        ) from exc
    if sampled.returncode != 0:
        raise FreshProcessRecoveryError(
            "process_measurement_error",
            "parent process-group sampler returned a failure",
        )
    members = 0
    rss_kib = 0
    for line in sampled.stdout.splitlines():
        columns = line.split()
        if len(columns) != 2:
            continue
        try:
            group_id, row_rss_kib = int(columns[0]), int(columns[1])
        except ValueError:
            continue
        if group_id == process_group_id:
            members += 1
            rss_kib += row_rss_kib
    return members, rss_kib * 1024


def _terminate_fresh_process_group(
    process: subprocess.Popen[bytes],
) -> str:
    if process.pid <= 0 or process.pid == os.getpgrp():
        raise FreshProcessRecoveryError(
            "process_isolation_error",
            "refusing to signal a non-worker process group",
        )
    if not _process_group_exists(process.pid):
        if process.poll() is None:
            process.wait(timeout=0.05)
        return "already_terminal"
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return "already_terminal"
    grace_deadline = (
        time.monotonic_ns() + WORLD_V3_FRESH_PROCESS_TERMINATION_GRACE_NS
    )
    while time.monotonic_ns() < grace_deadline:
        process.poll()
        if not _process_group_exists(process.pid):
            break
        time.sleep(0.005)
    if _process_group_exists(process.pid):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=0.25)
    except subprocess.TimeoutExpired as exc:
        raise FreshProcessRecoveryError(
            "process_termination_error",
            "worker process group could not be reaped",
        ) from exc
    if _process_group_exists(process.pid):
        raise FreshProcessRecoveryError(
            "process_termination_error",
            "worker descendants survived group termination",
        )
    return "terminated"


def _decode_fresh_process_output(data: bytes) -> dict[str, Any]:
    if len(data) > MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES:
        raise FreshProcessRecoveryError(
            "output_limit_error",
            "fresh-process stdout exceeded its fixed byte ceiling",
        )
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FreshProcessRecoveryError(
            "malformed_output",
            "fresh-process output is not UTF-8 JSON",
        ) from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise FreshProcessRecoveryError(
            "malformed_output",
            "fresh-process output is not one canonical JSON object",
        )
    output_digest = value.get("output_digest")
    material = copy.deepcopy(value)
    material.pop("output_digest", None)
    if (
        not isinstance(output_digest, str)
        or output_digest != canonical_digest(material)
    ):
        raise FreshProcessRecoveryError(
            "output_tamper",
            "fresh-process output digest is invalid",
        )
    return value


def _validate_fresh_process_output(
    data: bytes,
    *,
    request: Mapping[str, Any],
    expected_pid: int,
    expected_parent_pid: int,
) -> tuple[dict[str, Any], RecoveryMeasurementReceipt]:
    value = _decode_fresh_process_output(data)
    required = {
        "schema_version",
        "output_kind",
        "protocol_version",
        "request_digest",
        "request_nonce",
        "executable_identity",
        "worker_module_identity",
        "environment_identity",
        "process_identity",
        "worker_cwd",
        "store_identity",
        "relocation_identity",
        "recovered_commit_count",
        "recovered_local_object_count",
        "recovered_committed_payload_bytes",
        "lane_digest",
        "owner_catalog_count",
        "owner_catalog_digest",
        "world_generations",
        "aggregation_result_digest",
        "in_process_recovery",
        "output_digest",
    }
    if set(value) != required:
        raise FreshProcessRecoveryError(
            "malformed_output",
            "fresh-process output field set differs from the protocol",
        )
    if (
        value["schema_version"] != "1.0.0"
        or value["output_kind"] != "world_v3_fresh_process_recovery"
        or value["protocol_version"]
        != WORLD_V3_FRESH_PROCESS_PROTOCOL_VERSION
    ):
        raise FreshProcessRecoveryError(
            "output_identity_error",
            "fresh-process output protocol identity differs",
        )
    if (
        value["request_digest"] != request["request_digest"]
        or value["request_nonce"] != request["request_nonce"]
    ):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process output request identity differs",
        )
    for field in (
        "executable_identity",
        "worker_module_identity",
        "environment_identity",
        "worker_cwd",
        "relocation_identity",
    ):
        if value[field] != request[field]:
            raise FreshProcessRecoveryError(
                "output_identity_error",
                f"fresh-process output {field} differs",
            )
    process_identity = value["process_identity"]
    expected_process_identity = {
        "pid": expected_pid,
        "parent_pid": expected_parent_pid,
        "process_group_id": expected_pid,
        "session_id": expected_pid,
    }
    if process_identity != expected_process_identity:
        raise FreshProcessRecoveryError(
            "process_identity_error",
            "fresh-process output process/session identity differs",
        )
    store_identity = value["store_identity"]
    if (
        not isinstance(store_identity, Mapping)
        or store_identity.get("root") != request["store_root"]
        or store_identity.get("target_id") != request["target_id"]
        or store_identity.get("run_id") != request["run_id"]
        or store_identity.get("theory_generation")
        != request["theory_generation"]
        or store_identity.get("theory_result_digest")
        != request["theory_result_digest"]
    ):
        raise FreshProcessRecoveryError(
            "store_identity_error",
            "fresh-process output store/theory identity differs",
        )
    in_process_value = value["in_process_recovery"]
    if not isinstance(in_process_value, Mapping):
        raise FreshProcessRecoveryError(
            "malformed_output",
            "fresh-process output lacks its in-process receipt",
        )
    in_process = _validate_recovery_measurement_mapping(in_process_value)
    if (
        value["recovered_commit_count"] != in_process.commit_count
        or value["recovered_local_object_count"]
        != in_process.local_object_count
        or value["recovered_committed_payload_bytes"]
        != in_process.committed_payload_bytes
        or value["lane_digest"] != in_process.lane_digest
        or store_identity.get("head_generation")
        != in_process.head_generation
    ):
        raise FreshProcessRecoveryError(
            "output_tamper",
            "fresh-process summary differs from its exact in-process receipt",
        )
    if (
        in_process.theory_generation != request["theory_generation"]
        or in_process.child_processes_spawned != 0
    ):
        raise FreshProcessRecoveryError(
            "output_identity_error",
            "fresh-process in-process receipt crosses its request identity",
        )
    return value, in_process


def _fresh_process_worker_output(
    request: Mapping[str, Any],
) -> dict[str, Any]:
    expected_keys = {
        "schema_version",
        "request_kind",
        "protocol_version",
        "request_nonce",
        "target_id",
        "run_id",
        "store_root",
        "theory_generation",
        "theory_result",
        "theory_result_digest",
        "branch_id",
        "executable_identity",
        "worker_module_identity",
        "environment",
        "environment_identity",
        "worker_cwd",
        "relocation_identity",
        "limits",
        "request_digest",
    }
    if set(request) != expected_keys:
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process request field set differs from the protocol",
        )
    material = copy.deepcopy(dict(request))
    request_digest = material.pop("request_digest")
    if request_digest != canonical_digest(material):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process request digest is invalid",
        )
    if (
        request["schema_version"] != "1.0.0"
        or request["request_kind"] != "world_v3_fresh_process_recovery"
        or request["protocol_version"]
        != WORLD_V3_FRESH_PROCESS_PROTOCOL_VERSION
        or request["limits"] != _fresh_process_limits()
    ):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process request protocol or limits differ",
        )
    actual_environment = dict(os.environ)
    if (
        request["environment"] != actual_environment
        or request["environment_identity"]
        != _fresh_environment_identity(actual_environment)
    ):
        raise FreshProcessRecoveryError(
            "environment_identity_error",
            "fresh-process environment is not the exact scrubbed environment",
        )
    executable_identity = _file_content_identity(
        Path(sys.executable),
        label="python_executable",
    )
    module_identity = _file_content_identity(
        Path(__file__),
        label="world_v3_recovery_worker_module",
    )
    if (
        request["executable_identity"] != executable_identity
        or request["worker_module_identity"] != module_identity
        or request["worker_cwd"] != str(Path.cwd().resolve())
    ):
        raise FreshProcessRecoveryError(
            "worker_identity_error",
            "fresh-process executable, module, or cwd identity differs",
        )
    relocation = request["relocation_identity"]
    if not isinstance(relocation, Mapping):
        raise FreshProcessRecoveryError(
            "relocation_identity_error",
            "fresh-process relocation identity is absent",
        )
    relocation_material = copy.deepcopy(dict(relocation))
    relocation_digest = relocation_material.pop("identity_digest", None)
    if relocation_digest != canonical_digest(relocation_material):
        raise FreshProcessRecoveryError(
            "relocation_identity_error",
            "fresh-process relocation identity digest is invalid",
        )
    source_root = relocation.get("source_root")
    if source_root is not None:
        source = Path(str(source_root))
        if source.exists() or source.is_symlink():
            raise FreshProcessRecoveryError(
                "relocation_identity_error",
                "relocation source reappeared before worker recovery",
            )
    if (
        relocation.get("destination_root") != request["store_root"]
        or not Path(str(request["store_root"])).is_dir()
    ):
        raise FreshProcessRecoveryError(
            "relocation_identity_error",
            "relocation destination differs from the requested store",
        )
    theory_value = request["theory_result"]
    if (
        not isinstance(theory_value, Mapping)
        or request["theory_result_digest"]
        != canonical_digest(dict(theory_value))
    ):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process theory result digest is invalid",
        )
    theory_result = _result_from_protocol_mapping(theory_value)
    store = DiscoveryTransactionStore(
        Path(str(request["store_root"])),
        target_id=str(request["target_id"]),
        run_id=str(request["run_id"]),
    )
    runtime = WorldV3ContentGraphRuntime.recover(
        store=store,
        theory_generation=int(request["theory_generation"]),
        theory_result=theory_result,
        branch_id=str(request["branch_id"]),
    )
    measurement = runtime.recovery_measurement
    if measurement is None:
        raise FreshProcessRecoveryError(
            "output_validation_error",
            "fresh recovery did not produce its in-process receipt",
        )
    owner_catalog = list(runtime.owner_catalog)
    aggregation_digest = (
        canonical_digest(runtime.aggregation_result.as_dict())
        if runtime.aggregation_result is not None
        else None
    )
    output: dict[str, Any] = {
        "schema_version": "1.0.0",
        "output_kind": "world_v3_fresh_process_recovery",
        "protocol_version": WORLD_V3_FRESH_PROCESS_PROTOCOL_VERSION,
        "request_digest": request["request_digest"],
        "request_nonce": request["request_nonce"],
        "executable_identity": executable_identity,
        "worker_module_identity": module_identity,
        "environment_identity": request["environment_identity"],
        "process_identity": {
            "pid": os.getpid(),
            "parent_pid": os.getppid(),
            "process_group_id": os.getpgrp(),
            "session_id": os.getsid(0),
        },
        "worker_cwd": request["worker_cwd"],
        "store_identity": {
            "root": request["store_root"],
            "target_id": request["target_id"],
            "run_id": request["run_id"],
            "theory_generation": request["theory_generation"],
            "theory_result_digest": request["theory_result_digest"],
            "head_generation": measurement.head_generation,
        },
        "relocation_identity": copy.deepcopy(dict(relocation)),
        "recovered_commit_count": measurement.commit_count,
        "recovered_local_object_count": measurement.local_object_count,
        "recovered_committed_payload_bytes": (
            measurement.committed_payload_bytes
        ),
        "lane_digest": measurement.lane_digest,
        "owner_catalog_count": len(owner_catalog),
        "owner_catalog_digest": canonical_digest(owner_catalog),
        "world_generations": [
            row.generation for row in runtime.committed_worlds
        ],
        "aggregation_result_digest": aggregation_digest,
        "in_process_recovery": measurement.as_dict(),
    }
    output["output_digest"] = canonical_digest(output)
    return output


def _fresh_process_worker_main() -> int:
    """Read one bounded canonical request and emit one canonical response."""

    os.environ.pop("__CF_USER_TEXT_ENCODING", None)
    try:
        data = sys.stdin.buffer.read(
            MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES + 1
        )
        if len(data) > MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES:
            raise FreshProcessRecoveryError(
                "request_limit_error",
                "fresh-process request exceeds its fixed byte ceiling",
            )
        request = _decode_canonical_mapping(
            data,
            "fresh-process recovery request",
        )
        output = _fresh_process_worker_output(request)
        sys.stdout.buffer.write(canonical_json(output))
        sys.stdout.buffer.flush()
        return 0
    except BaseException as exc:
        diagnostic = (
            f"{type(exc).__name__}: {str(exc)}"
        ).encode("utf-8", errors="replace")
        sys.stderr.buffer.write(
            diagnostic[:MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES]
        )
        sys.stderr.buffer.flush()
        return 70


def _recover_world_v3_in_fresh_process(
    *,
    store: DiscoveryTransactionStore,
    theory_generation: int,
    theory_result: ContentGraphTransactionResult,
    branch_id: str,
    relocated_from: Path | str | None,
    deadline_ns: int,
) -> FreshProcessRecoveryReceipt:
    """Launch, bound, verify, and account for one recovery worker."""

    if os.name != "posix" or not hasattr(os, "killpg"):
        raise FreshProcessRecoveryError(
            "process_isolation_error",
            "fresh-process recovery requires POSIX process-group controls",
        )
    if type(store) is not DiscoveryTransactionStore:
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process recovery requires an exact transaction store",
        )
    if type(theory_generation) is not int or theory_generation < 1:
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process theory generation must be positive",
        )
    if type(theory_result) is not ContentGraphTransactionResult:
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process recovery requires an exact theory result",
        )
    if (
        type(deadline_ns) is not int
        or deadline_ns <= 0
        or deadline_ns > MAX_WORLD_V3_FRESH_PROCESS_NS
    ):
        raise FreshProcessRecoveryError(
            "deadline_error",
            "fresh-process deadline must be positive and at most the fixed maximum",
        )
    if not isinstance(branch_id, str):
        raise FreshProcessRecoveryError(
            "request_identity_error",
            "fresh-process branch identity must be a string",
        )
    destination_root = store.root.resolve(strict=True)
    relocation_identity = _relocation_request_identity(
        destination_root=destination_root,
        relocated_from=relocated_from,
    )
    executable_identity = _file_content_identity(
        Path(sys.executable),
        label="python_executable",
    )
    executable_path = Path(
        str(executable_identity["launch_path"])
    )
    if not os.access(executable_path, os.X_OK):
        raise FreshProcessRecoveryError(
            "identity_error",
            "Python launch path is not executable",
        )
    module_identity = _file_content_identity(
        Path(__file__),
        label="world_v3_recovery_worker_module",
    )
    worker_cwd = Path(__file__).resolve().parents[2]
    environment = dict(_FRESH_PROCESS_ENVIRONMENT)
    environment_identity = _fresh_environment_identity(environment)
    theory_projection = theory_result.as_dict()
    request: dict[str, Any] = {
        "schema_version": "1.0.0",
        "request_kind": "world_v3_fresh_process_recovery",
        "protocol_version": WORLD_V3_FRESH_PROCESS_PROTOCOL_VERSION,
        "request_nonce": secrets.token_hex(16),
        "target_id": store.target_id,
        "run_id": store.run_id,
        "store_root": str(destination_root),
        "theory_generation": theory_generation,
        "theory_result": theory_projection,
        "theory_result_digest": canonical_digest(theory_projection),
        "branch_id": branch_id,
        "executable_identity": executable_identity,
        "worker_module_identity": module_identity,
        "environment": environment,
        "environment_identity": environment_identity,
        "worker_cwd": str(worker_cwd),
        "relocation_identity": relocation_identity,
        "limits": _fresh_process_limits(),
    }
    request["request_digest"] = canonical_digest(request)
    request_data = canonical_json(request)
    if len(request_data) > MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES:
        raise FreshProcessRecoveryError(
            "request_limit_error",
            "fresh-process request exceeds its fixed byte ceiling",
        )
    command = [
        str(executable_path),
        "-c",
        # The package exports this module, so `-m` would execute an already
        # imported module again and emit a runpy warning on protocol stderr.
        "from agentic.experiments.world_v3_content_graph_runtime "
        "import _fresh_process_worker_main; "
        "raise SystemExit(_fresh_process_worker_main())",
    ]
    launch_argv_digest = canonical_digest(command)
    started_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
    launched_ns = time.perf_counter_ns()
    absolute_deadline_ns = launched_ns + deadline_ns
    process: subprocess.Popen[bytes] | None = None
    selector: selectors.BaseSelector | None = None
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    stdout_total = 0
    stderr_total = 0
    peak_members = 0
    peak_rss_bytes = 0
    exit_observed_ns: int | None = None
    try:
        process = subprocess.Popen(
            command,
            cwd=str(worker_cwd),
            env=environment,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            start_new_session=True,
        )
        if (
            process.stdin is None
            or process.stdout is None
            or process.stderr is None
        ):
            raise FreshProcessRecoveryError(
                "process_launch_error",
                "fresh-process protocol pipes were not created",
            )
        process.stdin.write(request_data)
        process.stdin.close()
        selector = selectors.DefaultSelector()
        for stream, label in (
            (process.stdout, "stdout"),
            (process.stderr, "stderr"),
        ):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, data=label)
        next_sample_ns = launched_ns
        while selector.get_map() or process.poll() is None:
            now_ns = time.perf_counter_ns()
            if now_ns >= absolute_deadline_ns:
                raise FreshProcessRecoveryError(
                    "deadline_exceeded",
                    "fresh-process recovery exceeded its absolute deadline",
                )
            if now_ns >= next_sample_ns:
                members, rss_bytes = _sample_process_group(process.pid)
                peak_members = max(peak_members, members)
                peak_rss_bytes = max(peak_rss_bytes, rss_bytes)
                if members > MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS:
                    raise FreshProcessRecoveryError(
                        "process_count_exceeded",
                        "fresh-process worker created an unauthorized descendant",
                    )
                if rss_bytes > MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES:
                    raise FreshProcessRecoveryError(
                        "memory_exceeded",
                        "fresh-process worker exceeded its fixed RSS ceiling",
                    )
                next_sample_ns = (
                    now_ns + WORLD_V3_FRESH_PROCESS_METRIC_SAMPLE_NS
                )
            remaining_seconds = max(
                0.0,
                (absolute_deadline_ns - time.perf_counter_ns()) / 1e9,
            )
            for key, _mask in selector.select(
                timeout=min(0.02, remaining_seconds)
            ):
                try:
                    chunk = os.read(key.fileobj.fileno(), 64 * 1024)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                if key.data == "stdout":
                    stdout_total += len(chunk)
                    if stdout_total > MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES:
                        raise FreshProcessRecoveryError(
                            "output_limit_error",
                            "fresh-process stdout exceeded its fixed byte ceiling",
                        )
                    stdout_chunks.append(chunk)
                else:
                    stderr_total += len(chunk)
                    if stderr_total > MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES:
                        raise FreshProcessRecoveryError(
                            "output_limit_error",
                            "fresh-process stderr exceeded its fixed byte ceiling",
                        )
                    stderr_chunks.append(chunk)
            if process.poll() is not None and exit_observed_ns is None:
                exit_observed_ns = time.perf_counter_ns()
        process.wait(timeout=0)
        if exit_observed_ns is None:
            exit_observed_ns = time.perf_counter_ns()
        terminal_members, _terminal_rss = _sample_process_group(process.pid)
        if terminal_members != 0 or _process_group_exists(process.pid):
            raise FreshProcessRecoveryError(
                "descendant_leak",
                "fresh-process worker left a live process-group member",
            )
        stdout = b"".join(stdout_chunks)
        stderr = b"".join(stderr_chunks)
        if process.returncode != 0:
            detail = stderr.decode("utf-8", errors="replace")
            raise FreshProcessRecoveryError(
                "worker_failed",
                f"fresh-process worker exited {process.returncode}: {detail}",
            )
        if stderr:
            raise FreshProcessRecoveryError(
                "unexpected_stderr",
                "successful fresh-process recovery emitted stderr bytes",
            )
        output, in_process = _validate_fresh_process_output(
            stdout,
            request=request,
            expected_pid=process.pid,
            expected_parent_pid=os.getpid(),
        )
    except BaseException:
        if process is not None and (
            process.poll() is None or _process_group_exists(process.pid)
        ):
            _terminate_fresh_process_group(process)
        raise
    finally:
        if selector is not None:
            selector.close()
        if process is not None:
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    stream.close()
    completed_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
    child_cpu_elapsed_ns = int(
        max(
            0.0,
            (
                completed_rusage.ru_utime
                + completed_rusage.ru_stime
                - started_rusage.ru_utime
                - started_rusage.ru_stime
            ),
        )
        * 1_000_000_000
    )
    if child_cpu_elapsed_ns > MAX_WORLD_V3_FRESH_PROCESS_CPU_NS:
        raise FreshProcessRecoveryError(
            "cpu_exceeded",
            "fresh-process recovery exceeded its fixed child-CPU ceiling",
        )
    launch_to_exit_elapsed_ns = exit_observed_ns - launched_ns
    if launch_to_exit_elapsed_ns > deadline_ns:
        raise FreshProcessRecoveryError(
            "deadline_exceeded",
            "fresh-process launch-to-exit time exceeded its deadline",
        )
    source_root = relocation_identity["source_root"]
    source_absent_after_exit = (
        source_root is None
        or (
            not Path(str(source_root)).exists()
            and not Path(str(source_root)).is_symlink()
        )
    )
    if not source_absent_after_exit or not destination_root.is_dir():
        raise FreshProcessRecoveryError(
            "relocation_identity_error",
            "relocation identity changed during fresh-process recovery",
        )
    receipt_relocation = copy.deepcopy(relocation_identity)
    receipt_relocation["source_absent_after_exit"] = (
        source_absent_after_exit if source_root is not None else None
    )
    receipt_relocation["destination_present_after_exit"] = (
        destination_root.is_dir()
    )
    receipt_relocation["verified_lane_digest"] = in_process.lane_digest
    receipt_relocation.pop("identity_digest")
    receipt_relocation["identity_digest"] = canonical_digest(
        receipt_relocation
    )
    parent_supervision_elapsed_ns = time.perf_counter_ns() - launched_ns
    return FreshProcessRecoveryReceipt(
        request_digest=str(request["request_digest"]),
        worker_output_digest=bytes_digest(stdout),
        output_payload_digest=str(output["output_digest"]),
        theory_generation=theory_generation,
        head_generation=in_process.head_generation,
        recovered_commit_count=in_process.commit_count,
        recovered_local_object_count=in_process.local_object_count,
        recovered_committed_payload_bytes=(
            in_process.committed_payload_bytes
        ),
        lane_digest=in_process.lane_digest,
        launch_to_exit_elapsed_ns=launch_to_exit_elapsed_ns,
        parent_supervision_elapsed_ns=parent_supervision_elapsed_ns,
        child_cpu_elapsed_ns=child_cpu_elapsed_ns,
        peak_process_group_rss_bytes=peak_rss_bytes,
        launched_process_count=1,
        peak_observed_process_group_members=peak_members,
        terminal_process_group_members=0,
        returncode=int(process.returncode),
        deadline_ns=deadline_ns,
        request_bytes=len(request_data),
        stdout_bytes=len(stdout),
        stderr_bytes=len(stderr),
        launch_argv_digest=launch_argv_digest,
        in_process_recovery=in_process,
        _executable_identity_data=canonical_json(executable_identity),
        _worker_module_identity_data=canonical_json(module_identity),
        _environment_identity_data=canonical_json(environment_identity),
        _relocation_identity_data=canonical_json(receipt_relocation),
        _process_identity_data=canonical_json(output["process_identity"]),
    )


__all__ = [
    "AGGREGATION_ROOT_KIND",
    "ANCHOR_ROOT_KIND",
    "AggregationCommit",
    "CommittedWorld",
    "CanonicalDescendantExperimentV3Result",
    "DESCENDANT_REFLECTION_ROOT_KIND",
    "DescendantReflectionCommit",
    "FRESH_PROCESS_CPU_MEASUREMENT_SCOPE",
    "FRESH_PROCESS_MEMORY_MEASUREMENT_SCOPE",
    "FRESH_PROCESS_RECOVERY_AUTHORITY_BOUNDARY",
    "FreshProcessRecoveryError",
    "FreshProcessRecoveryReceipt",
    "GraphStageProduct",
    "INCOMPLETE_SUPPORT_AUTHORITY_BOUNDARY",
    "IncompleteWorldSupport",
    "MAX_WORLD_V3_LANE_COMMITTED_BYTES",
    "MAX_WORLD_V3_LANE_COMMITS",
    "MAX_WORLD_V3_DESCENDANT_COMMITS",
    "MAX_WORLD_V3_LANE_LOCAL_OBJECTS",
    "MAX_WORLD_V3_FRESH_PROCESS_CPU_NS",
    "MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS",
    "MAX_WORLD_V3_FRESH_PROCESS_NS",
    "MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES",
    "MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES",
    "MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES",
    "MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES",
    "MAX_WORLD_V3_RECOVERY_CHILD_PROCESSES",
    "MAX_WORLD_V3_RECOVERY_PHASE_NS",
    "MAX_WORLD_V3_RECOVERY_TOTAL_NS",
    "MissingCommittedDependency",
    "ParallelWorldProduction",
    "RECOVERY_AUTHORITY_BOUNDARY",
    "RecoveryMeasurementReceipt",
    "WORLD_ORDER",
    "WORLD_ROOT_KIND",
    "WorldPrefixCommit",
    "WorldProducer",
    "WorldProducerFailure",
    "WorldV3ContentGraphRuntime",
    "run_canonical_descendant_experiment_v3",
]


if __name__ == "__main__":
    if sys.argv[1:] != ["--fresh-process-recovery-worker"]:
        raise SystemExit(64)
    raise SystemExit(_fresh_process_worker_main())
