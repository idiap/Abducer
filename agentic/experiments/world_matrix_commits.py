# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Canonical seven-commit persistence for the five-world experiment matrix.

The domain-level world-matrix validators intentionally know nothing about
persistence.  This module supplies the missing causal topology: one frozen
commission anchor, five one-envelope commits in ``WORLD_IDS`` order, and one
aggregation-only commit.  Producer work may finish in parallel, but canonical
acceptance is serialized and no caller can provide prior envelopes or a
certificate as uncommitted authority.

Every persisted locator is root-relative.  Absolute runtime paths occur only in
``VerifiedCommit`` and in concrete evidence resolvers reconstructed after a
commit has won CAS.  Thus copying or moving the whole transaction root preserves
all semantic identities and replay behavior.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    CommitResult,
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedArtifactContext,
    VerifiedCommit,
)

from .world_matrix import (
    CAUSAL_BINDING_V2_CONTRACT_VERSION,
    COMMISSION_PRODUCER_ROLE,
    COMMISSION_STAGE_ID,
    GOVERNED_CLOCK_EVIDENCE_V2_SCHEMA,
    MATRIX_AGGREGATION_PRODUCER_ROLE,
    MATRIX_AGGREGATION_STAGE_ID,
    WORLD_REQUEST_PRODUCER_ROLE,
    WORLD_REQUEST_STAGE_ID,
    WORLD_IDS,
    CommittedCausalEvidenceSnapshot,
    CommittedCausalEvidencePaths,
    CommittedCausalEvidenceResolver,
    build_experiment_world_request,
    require_authoritative_experiment_world_matrix_commission,
    validate_experiment_authority_projection,
    validate_experiment_causal_producer_binding,
    validate_experiment_world_matrix_certificate_v2,
    validate_experiment_world_observation_envelope,
    validate_experiment_world_request,
    validate_five_world_matrix,
    world_matrix_validation_cache_scope,
)


COMMIT_REFERENCE_SCHEMA = "discovery_commit_reference.schema.json"
VERIFIED_COMMIT_IDENTITY_SCHEMA = "discovery_verified_commit_identity.schema.json"
AGGREGATION_INPUT_SCHEMA = (
    "dynamic_experiment_world_matrix_aggregation_input_v1.schema.json"
)
WORLD_REQUEST_BATCH_SCHEMA = "dynamic_experiment_world_request_batch_v1.schema.json"
OBJECT_DESCRIPTOR_SCHEMA = (
    "dynamic_experiment_committed_object_descriptor_v1.schema.json"
)
ANCHOR_TRANSITION_SCHEMA = (
    "dynamic_experiment_world_matrix_anchor_transition_v2.schema.json"
)
OBSERVATION_TRANSITION_SCHEMA = (
    "dynamic_experiment_world_observation_transition_v2.schema.json"
)
AGGREGATION_TRANSITION_SCHEMA = (
    "dynamic_experiment_world_matrix_aggregation_transition_v2.schema.json"
)
WORLD_MATRIX_BRANCH_ID = "root"
_EVIDENCE_KINDS = (
    "producer_request",
    "producer_receipt",
    "artifact",
    "immutable_history",
    "governed_clock",
)
_EVIDENCE_OBJECT_KINDS = {
    "producer_request": "producer_request_evidence",
    "producer_receipt": "producer_receipt_evidence",
    "artifact": "producer_artifact_evidence",
    "immutable_history": "immutable_history_evidence",
    "governed_clock": "governed_clock_evidence",
}
_AUTHORITY_BOUNDARY = {
    "theory_first": True,
    "experiment_role": "secondary_theory_support_only",
    "theory_mutation_authorized": False,
    "certificate_authority_before_aggregation": False,
}


@dataclass(frozen=True, slots=True)
class PreparedWorldMatrixAnchor:
    """Pure anchor proposal whose files have not yet been made visible."""

    programme_id: str
    expected_generation: int
    next_state: Mapping[str, Any]
    transition: Mapping[str, Any]
    transition_artifact_path: str
    commit_artifacts: tuple[CommitArtifact, ...]
    idempotency_key: str
    request_digest: str


@dataclass(frozen=True, slots=True)
class VerifiedWorldMatrixCommit:
    """One committed transition plus its portable post-CAS reference."""

    transition: Mapping[str, Any]
    commit_reference: Mapping[str, Any]
    verified_commit: VerifiedCommit


@dataclass(frozen=True, slots=True)
class _VerifiedWorldTransitionSnapshot:
    """One transition and all evidence bytes from one verified store batch."""

    commit: VerifiedCommit
    transition: Mapping[str, Any]
    transition_bytes: bytes
    artifact_batch: Mapping[str, bytes]
    evidence_snapshots: tuple[CommittedCausalEvidenceSnapshot, ...]
    resolver: CommittedCausalEvidenceResolver


VerifiedWorldMatrixAnchorCommit = VerifiedWorldMatrixCommit
VerifiedWorldMatrixObservationCommit = VerifiedWorldMatrixCommit
VerifiedWorldMatrixAggregationCommit = VerifiedWorldMatrixCommit


def _self_digest(value: Mapping[str, Any], field: str) -> str:
    material = copy.deepcopy(dict(value))
    material.pop(field, None)
    return canonical_digest(material)


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StateCorruptionError(f"{label} is not one UTF-8 JSON value") from exc
    if not isinstance(value, dict):
        raise StateCorruptionError(f"{label} must contain one JSON object")
    return value


def _generation_only_next(commit: VerifiedCommit) -> dict[str, Any]:
    state = copy.deepcopy(dict(commit.state))
    if (
        state.get("target_id") is None
        or state.get("run_id") is None
        or state.get("generation") != commit.generation
    ):
        raise ContractError("verified state identity is incomplete")
    state["generation"] = commit.generation + 1
    return state


def _theory_projection(state: Mapping[str, Any]) -> dict[str, Any]:
    projection = copy.deepcopy(dict(state))
    projection.pop("generation", None)
    return projection


def _frozen_theory_digest(state: Mapping[str, Any]) -> str:
    return canonical_digest(_theory_projection(state))


def _projection_component_value(
    projection: Mapping[str, Any], component_kind: str
) -> dict[str, Any]:
    """Return one actual projection value, never a digest-only substitute."""

    matches = [
        row["value"]
        for row in projection.get("components", [])
        if row.get("component_kind") == component_kind
    ]
    if len(matches) != 1 or not isinstance(matches[0], Mapping):
        raise ContractError(
            f"experiment authority projection lacks one {component_kind!r} value"
        )
    return copy.deepcopy(dict(matches[0]))


def build_verified_commit_identity(commit: VerifiedCommit) -> dict[str, Any]:
    """Serialize exact commit identity without persisting its runtime-local path."""

    identity: dict[str, Any] = {
        "schema_version": "1.0.0",
        "identity_kind": "verified_discovery_commit",
        "target_id": commit.state["target_id"],
        "run_id": commit.state["run_id"],
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
        "frozen_theory_state_projection_digest": _frozen_theory_digest(commit.state),
    }
    identity["identity_digest"] = _self_digest(identity, "identity_digest")
    validate_payload(identity, VERIFIED_COMMIT_IDENTITY_SCHEMA)
    return identity


def _validate_verified_commit_identity(
    identity: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(identity))
    validate_payload(record, VERIFIED_COMMIT_IDENTITY_SCHEMA)
    if (
        record["generation"] != record["prior_generation"] + 1
        or record["identity_digest"] != _self_digest(record, "identity_digest")
    ):
        raise ContractError("verified commit identity is not self-consistent")
    return record


def _require_projection_matches_verified_ancestor(
    projection: Mapping[str, Any], prior_commit: VerifiedCommit
) -> dict[str, Any]:
    """Prove that the supplied world base is the literal prior committed state.

    The generic v2 projection permits arbitrary nonempty ancestor metadata.  A
    canonical transition needs a stronger boundary: the ancestor value must
    carry the exact state reopened from the transaction store, not merely the
    same namespace or a caller-authored digest.
    """

    ancestor = _projection_component_value(projection, "committed_ancestor")
    if (
        ancestor.get("generation") != prior_commit.generation
        or ancestor.get("state") != prior_commit.state
        or ancestor.get("state_semantic_digest")
        != prior_commit.state_semantic_digest
        or canonical_digest(ancestor.get("state"))
        != prior_commit.state_semantic_digest
    ):
        raise ContractError(
            "world commission committed ancestor differs from the verified prior commit"
        )
    return ancestor


def _require_generation_only_transition(
    prior: VerifiedCommit,
    next_state: Mapping[str, Any],
) -> tuple[str, str, str]:
    if next_state.get("generation") != prior.generation + 1:
        raise ContractError("world-matrix state did not advance exactly one generation")
    if _theory_projection(next_state) != _theory_projection(prior.state):
        raise ContractError("world-matrix commit attempted a non-generation state mutation")
    return (
        prior.state_semantic_digest,
        canonical_digest(next_state),
        _frozen_theory_digest(next_state),
    )


def _programme_id(commission: Mapping[str, Any]) -> str:
    try:
        claim = next(
            row["value"]
            for row in commission["authority_projection"]["components"]
            if row["component_kind"] == "registered_claim"
        )
        programme_id = claim["theory_programme_id"]
    except (KeyError, StopIteration, TypeError) as exc:
        raise ContractError("world commission lacks one registered programme") from exc
    return validate_identifier(programme_id, "programme_id")


def _base_path(programme_id: str) -> Path:
    validate_identifier(programme_id, "programme_id")
    return Path("branches") / WORLD_MATRIX_BRANCH_ID / "world-matrix" / programme_id


def _anchor_path(programme_id: str) -> str:
    return (_base_path(programme_id) / "anchor.json").as_posix()


def _observation_path(programme_id: str, ordinal: int) -> str:
    return (
        _base_path(programme_id)
        / "observations"
        / f"{ordinal:02d}-{WORLD_IDS[ordinal]}.json"
    ).as_posix()


def _aggregation_path(programme_id: str) -> str:
    return (_base_path(programme_id) / "aggregation.json").as_posix()


def _anchor_object_path(programme_id: str, name: str) -> str:
    return (_base_path(programme_id) / "objects" / "anchor" / name).as_posix()


def _observation_object_path(programme_id: str, ordinal: int) -> str:
    return (
        _base_path(programme_id)
        / "objects"
        / "observations"
        / f"{ordinal:02d}-{WORLD_IDS[ordinal]}-envelope.json"
    ).as_posix()


def _aggregation_object_path(programme_id: str, name: str) -> str:
    return (_base_path(programme_id) / "objects" / "aggregation" / name).as_posix()


def _walk_causal_bindings(
    value: Any,
    bindings: dict[str, dict[str, Any]],
) -> None:
    if isinstance(value, Mapping):
        if value.get("contract_version") == CAUSAL_BINDING_V2_CONTRACT_VERSION:
            binding = copy.deepcopy(dict(value))
            authority_id = str(binding.get("evidence_authority_id", ""))
            validate_identifier(authority_id, "evidence_authority_id")
            prior = bindings.get(authority_id)
            if prior is not None and prior != binding:
                raise ContractError("one evidence authority names different causal bindings")
            bindings[authority_id] = binding
            return
        for child in value.values():
            _walk_causal_bindings(child, bindings)
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for child in value:
            _walk_causal_bindings(child, bindings)


def _descriptor(path: str, data: bytes, *, object_kind: str) -> dict[str, Any]:
    """Describe exact JSON bytes and their decoded semantic identity."""

    relative = safe_relative_path(path).as_posix()
    if relative != path:
        raise ContractError(f"committed object path is not canonical: {path!r}")
    value = _json_object(data, relative)
    descriptor = {
        "path": relative,
        "sha256": bytes_digest(data),
        "size_bytes": len(data),
        "semantic_digest": canonical_digest(value),
        "object_kind": object_kind,
    }
    validate_payload(descriptor, OBJECT_DESCRIPTOR_SCHEMA)
    return descriptor


def validate_world_matrix_object_descriptor(
    descriptor: Mapping[str, Any],
    *,
    data: bytes,
    expected_kind: str,
    expected_path: str | None = None,
) -> dict[str, Any]:
    """Validate all five descriptor bindings against one exact byte snapshot.

    This public primitive is intentionally independent of filesystem paths.  A
    committed replay adds manifest coverage and link checks before calling it.
    """

    record = copy.deepcopy(dict(descriptor))
    validate_payload(record, OBJECT_DESCRIPTOR_SCHEMA)
    relative = safe_relative_path(record["path"]).as_posix()
    if relative != record["path"]:
        raise ContractError("committed object descriptor path is not canonical")
    if expected_path is not None:
        canonical_expected = safe_relative_path(expected_path).as_posix()
        if relative != canonical_expected:
            raise StateCorruptionError("committed object descriptor names the wrong path")
    if record["object_kind"] != expected_kind:
        raise StateCorruptionError("committed object descriptor has the wrong object kind")
    if len(data) != record["size_bytes"]:
        raise StateCorruptionError("committed object descriptor has the wrong byte size")
    if bytes_digest(data) != record["sha256"]:
        raise StateCorruptionError("committed object descriptor byte digest changed")
    value = _json_object(data, relative)
    if canonical_digest(value) != record["semantic_digest"]:
        raise StateCorruptionError("committed object descriptor semantic digest changed")
    return value


def _committed_object_artifact(
    value: Mapping[str, Any],
    *,
    path: str,
    object_kind: str,
    namespace: Namespace,
) -> tuple[CommitArtifact, dict[str, Any]]:
    """Freeze one complete domain object once and return its strict descriptor."""

    data = canonical_json(copy.deepcopy(dict(value)))
    return (
        CommitArtifact(path, data, namespace),
        _descriptor(path, data, object_kind=object_kind),
    )


def _prepare_commit_local_evidence(
    value: Any,
    *,
    resolver: CommittedCausalEvidenceResolver,
    programme_id: str,
    namespace: Namespace,
    exclude_authority_ids: frozenset[str] = frozenset(),
) -> tuple[tuple[CommitArtifact, ...], list[dict[str, Any]]]:
    """Copy the exact byte snapshots already validated for this transition.

    Semantic validation and commit preparation share one resolver.  The
    resolver returns its cached descriptor-backed snapshot, so a source name
    changed after validation can neither replace the winning bytes nor trigger
    a second unsafe read.
    """

    bindings: dict[str, dict[str, Any]] = {}
    _walk_causal_bindings(value, bindings)
    if not bindings:
        raise ContractError("world transition requires at least one causal binding")

    artifacts: list[CommitArtifact] = []
    manifest: list[dict[str, Any]] = []
    evidence_base = _base_path(programme_id) / "evidence"
    new_authority_ids = sorted(set(bindings) - set(exclude_authority_ids))
    if not new_authority_ids:
        raise ContractError("world transition introduced no new producer evidence")
    for authority_id in new_authority_ids:
        binding = bindings[authority_id]
        resolution, source_files = resolver.validated_file_snapshot(binding)
        if resolution.evidence_authority_id != authority_id:
            raise ContractError("validated evidence authority identity changed")
        logical_artifact = safe_relative_path(
            binding["artifact_evidence"]["declared_output_path"]
        )
        logical_history = safe_relative_path(
            binding["artifact_evidence"]["immutable_history_path"]
        )
        authority_base = evidence_base / authority_id
        relative_paths = {
            "producer_request": authority_base / "producer-request.json",
            "producer_receipt": authority_base / "producer-receipt.json",
            "artifact": authority_base / "artifact" / logical_artifact,
            "immutable_history": authority_base / "history" / logical_history,
            "governed_clock": authority_base / "governed-clock.json",
        }
        if set(source_files) != set(_EVIDENCE_KINDS):
            raise ContractError("validated evidence snapshot coverage changed")
        data_by_kind = {
            kind: source_files[kind] for kind in _EVIDENCE_KINDS[:-1]
        }
        source_clock_data = source_files["governed_clock"]
        source_clock = _json_object(source_clock_data, "governed clock evidence")
        if "committed_derivation" in source_clock:
            raise ContractError(
                "source governed clock must not already be a committed derivation"
            )
        committed_derivation: dict[str, Any] = {
            "schema_version": "1.0.0",
            "contract_version": "committed-governed-clock-derivation/1.0.0",
            "derivation_kind": "portable-relative-path-rebinding",
            "source_clock_evidence_digest": source_clock[
                "clock_evidence_digest"
            ],
            "source_bytes_sha256": bytes_digest(source_clock_data),
            "source_size_bytes": len(source_clock_data),
            "source_semantic_digest": canonical_digest(source_clock),
        }
        committed_derivation["derivation_digest"] = _self_digest(
            committed_derivation, "derivation_digest"
        )
        source_clock["committed_paths"] = {
            kind: relative_paths[kind].as_posix() for kind in _EVIDENCE_KINDS
        }
        source_clock["committed_derivation"] = committed_derivation
        source_clock["clock_evidence_digest"] = _self_digest(
            source_clock, "clock_evidence_digest"
        )
        validate_payload(source_clock, GOVERNED_CLOCK_EVIDENCE_V2_SCHEMA)
        data_by_kind["governed_clock"] = canonical_json(source_clock)

        file_rows: dict[str, dict[str, Any]] = {}
        for kind in _EVIDENCE_KINDS:
            relative = safe_relative_path(relative_paths[kind].as_posix()).as_posix()
            data = data_by_kind[kind]
            artifacts.append(CommitArtifact(relative, data, namespace))
            file_rows[kind] = _descriptor(
                relative,
                data,
                object_kind=_EVIDENCE_OBJECT_KINDS[kind],
            )
        manifest.append(
            {"evidence_authority_id": authority_id, "files": file_rows}
        )
    return tuple(artifacts), manifest


def _manifest_artifact(
    commit: VerifiedCommit,
    relative_path: str,
) -> Mapping[str, Any]:
    matches = [
        row for row in commit.manifest["artifacts"] if row["path"] == relative_path
    ]
    if len(matches) != 1:
        raise StateCorruptionError(
            f"commit lacks one exact transition artifact: {relative_path}"
        )
    return matches[0]


def _evidence_snapshots_from_verified_batch(
    commit: VerifiedCommit,
    transition: Mapping[str, Any],
    batch: Mapping[str, bytes],
) -> tuple[CommittedCausalEvidenceSnapshot, ...]:
    """Reconstruct typed evidence solely from a store-verified byte batch."""

    manifest = transition["commit_local_evidence_manifest"]
    if not isinstance(manifest, list) or not manifest:
        raise StateCorruptionError("world transition lacks commit-local evidence")
    described_paths: set[str] = set()
    snapshots: list[CommittedCausalEvidenceSnapshot] = []
    authority_ids: set[str] = set()
    for entry in manifest:
        authority_id = validate_identifier(
            entry["evidence_authority_id"], "evidence_authority_id"
        )
        if authority_id in authority_ids:
            raise StateCorruptionError("duplicate commit-local evidence authority")
        authority_ids.add(authority_id)
        path_rows: list[tuple[str, str]] = []
        file_rows: list[tuple[str, bytes]] = []
        for kind in _EVIDENCE_KINDS:
            descriptor = entry["files"][kind]
            relative_text = safe_relative_path(descriptor["path"]).as_posix()
            if relative_text != descriptor["path"]:
                raise StateCorruptionError("commit-local evidence path is not canonical")
            if relative_text in described_paths:
                raise StateCorruptionError("commit-local evidence path was reused")
            described_paths.add(relative_text)
            committed_descriptor = _manifest_artifact(commit, relative_text)
            if (
                committed_descriptor["sha256"] != descriptor["sha256"]
                or committed_descriptor["size_bytes"] != descriptor["size_bytes"]
            ):
                raise StateCorruptionError("evidence manifest differs from commit manifest")
            data = batch.get(relative_text)
            if not isinstance(data, bytes):
                raise StateCorruptionError("commit-local evidence is absent from verified batch")
            validate_world_matrix_object_descriptor(
                descriptor,
                data=data,
                expected_kind=_EVIDENCE_OBJECT_KINDS[kind],
                expected_path=relative_text,
            )
            path_rows.append((kind, relative_text))
            file_rows.append((kind, data))
        snapshots.append(
            CommittedCausalEvidenceSnapshot(
                evidence_authority_id=authority_id,
                committed_paths=tuple(path_rows),
                committed_files=tuple(file_rows),
            )
        )

    evidence_prefix = (_base_path(transition["programme_id"]) / "evidence").as_posix()
    committed_evidence_paths = {
        row["path"]
        for row in commit.manifest["artifacts"]
        if row["path"] == evidence_prefix
        or row["path"].startswith(evidence_prefix + "/")
    }
    if committed_evidence_paths != described_paths:
        raise StateCorruptionError("transition evidence manifest coverage is not exact")
    return tuple(snapshots)


def _transition_object_descriptors(
    transition: Mapping[str, Any],
) -> tuple[Mapping[str, Any], ...]:
    """Return the complete descriptor vector for one strict v2 transition."""

    transition_kind = transition.get("transition_kind")
    if transition_kind == "theory_and_commission_anchor":
        validate_payload(transition, ANCHOR_TRANSITION_SCHEMA)
        rows = [
            transition["commission_object"],
            transition["commission_producer_binding_object"],
            *transition["world_request_objects"],
            *transition["world_request_producer_binding_objects"],
        ]
    elif transition_kind == "world_observation":
        validate_payload(transition, OBSERVATION_TRANSITION_SCHEMA)
        rows = [transition["observation_envelope_object"]]
    elif transition_kind == "world_matrix_aggregation":
        validate_payload(transition, AGGREGATION_TRANSITION_SCHEMA)
        rows = [
            transition["certificate_object"],
            transition["aggregation_producer_binding_object"],
        ]
    else:
        raise StateCorruptionError("unknown committed world transition kind")
    paths = [row.get("path") for row in rows if isinstance(row, Mapping)]
    if len(paths) != len(rows) or len(paths) != len(set(paths)):
        raise StateCorruptionError("world transition reused a committed object path")
    return tuple(rows)


def _read_verified_transition_snapshot(
    *,
    context: VerifiedArtifactContext,
    generation: int,
    programme_id: str,
    transition_path: str,
) -> _VerifiedWorldTransitionSnapshot:
    """Read one transition, objects, and evidence from one verified context."""

    relative_transition = safe_relative_path(transition_path).as_posix()
    manifest_paths = context.artifact_paths(generation)
    commit, batch = context.read_artifacts(generation, manifest_paths)
    transition_bytes = batch.get(relative_transition)
    if not isinstance(transition_bytes, bytes):
        raise StateCorruptionError("world transition is absent from verified batch")
    transition = _json_object(transition_bytes, relative_transition)
    object_descriptors = _transition_object_descriptors(transition)
    evidence_prefix = (_base_path(programme_id) / "evidence").as_posix()
    evidence_paths = [
        descriptor["path"]
        for entry in transition["commit_local_evidence_manifest"]
        for descriptor in entry["files"].values()
    ]
    object_paths = [descriptor["path"] for descriptor in object_descriptors]
    expected_paths = [relative_transition, *object_paths, *evidence_paths]
    if len(expected_paths) != len(set(expected_paths)):
        raise StateCorruptionError("world commit descriptor paths are not unique")
    if set(manifest_paths) != set(expected_paths):
        raise StateCorruptionError(
            "world commit artifact coverage is not exactly transition, objects, and evidence"
        )
    snapshots = _evidence_snapshots_from_verified_batch(
        commit, transition, batch
    )
    resolver = CommittedCausalEvidenceResolver._from_verified_artifact_snapshots(
        snapshots
    )
    return _VerifiedWorldTransitionSnapshot(
        commit=commit,
        transition=transition,
        transition_bytes=transition_bytes,
        artifact_batch=dict(batch),
        evidence_snapshots=snapshots,
        resolver=resolver,
    )


def _load_committed_object(
    snapshot: _VerifiedWorldTransitionSnapshot,
    descriptor: Mapping[str, Any],
    *,
    expected_kind: str,
    expected_path: str,
    cache: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]],
) -> dict[str, Any]:
    """Load and validate one unique object exactly once in a causal replay."""

    record = copy.deepcopy(dict(descriptor))
    path = record.get("path")
    if not isinstance(path, str):
        raise StateCorruptionError("committed object descriptor lacks a path")
    key = (snapshot.commit.generation, path)
    prior = cache.get(key)
    if prior is not None:
        prior_descriptor, prior_value = prior
        if prior_descriptor != record:
            raise StateCorruptionError("one committed object path has different descriptors")
        return prior_value
    committed_descriptor = _manifest_artifact(snapshot.commit, path)
    if (
        committed_descriptor["sha256"] != record.get("sha256")
        or committed_descriptor["size_bytes"] != record.get("size_bytes")
    ):
        raise StateCorruptionError("object descriptor differs from commit manifest")
    data = snapshot.artifact_batch.get(path)
    if not isinstance(data, bytes):
        raise StateCorruptionError("committed object is absent from verified batch")
    value = validate_world_matrix_object_descriptor(
        record,
        data=data,
        expected_kind=expected_kind,
        expected_path=expected_path,
    )
    if canonical_json(value) != data:
        raise StateCorruptionError("committed domain object bytes are not canonical JSON")
    cache[key] = (record, value)
    return value


def _combined_resolver(
    rows: Sequence[_VerifiedWorldTransitionSnapshot],
) -> CommittedCausalEvidenceResolver:
    by_authority: dict[str, CommittedCausalEvidenceSnapshot] = {}
    for row in rows:
        for snapshot in row.evidence_snapshots:
            authority_id = snapshot.evidence_authority_id
            if authority_id in by_authority:
                raise StateCorruptionError(
                    "one evidence authority was reused across committed transitions"
                )
            by_authority[authority_id] = snapshot
    if not by_authority:
        raise StateCorruptionError("combined world evidence is empty")
    return CommittedCausalEvidenceResolver._from_verified_artifact_snapshots(
        list(by_authority.values())
    )


def _evidence_authority_ids(
    rows: Sequence[_VerifiedWorldTransitionSnapshot],
) -> frozenset[str]:
    """Return the exact producer-evidence ownership accumulated by a prefix."""

    return frozenset(
        snapshot.evidence_authority_id
        for row in rows
        for snapshot in row.evidence_snapshots
    )


def build_world_matrix_commit_reference(
    commit: VerifiedCommit,
    *,
    programme_id: str,
    transition_kind: str,
    transition_artifact_path: str,
) -> dict[str, Any]:
    """Build a serialized reference containing content identity but no root."""

    relative = safe_relative_path(transition_artifact_path).as_posix()
    descriptor = _manifest_artifact(commit, relative)
    reference: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reference_kind": "portable_verified_discovery_commit",
        "programme_id": validate_identifier(programme_id, "programme_id"),
        "target_id": commit.state["target_id"],
        "run_id": commit.state["run_id"],
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
        "frozen_theory_state_projection_digest": _frozen_theory_digest(commit.state),
        "transition_kind": transition_kind,
        "transition_artifact": {
            "path": relative,
            "sha256": descriptor["sha256"],
            "size_bytes": descriptor["size_bytes"],
        },
    }
    reference["reference_digest"] = _self_digest(reference, "reference_digest")
    validate_payload(reference, COMMIT_REFERENCE_SCHEMA)
    return reference


def _validate_reference_value(reference: Mapping[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(dict(reference))
    validate_payload(record, COMMIT_REFERENCE_SCHEMA)
    safe_relative_path(record["transition_artifact"]["path"])
    if record["generation"] != record["prior_generation"] + 1:
        raise ContractError("portable commit reference generation is not contiguous")
    if record["reference_digest"] != _self_digest(record, "reference_digest"):
        raise ContractError("portable commit reference digest is invalid")
    return record


def build_world_matrix_aggregation_input_manifest(
    *,
    anchor_reference: Mapping[str, Any],
    observation_references: Sequence[Mapping[str, Any]],
    commission_id: str,
    commission_digest: str,
) -> dict[str, Any]:
    """Bind aggregation to the ordered six committed transition identities."""

    anchor = _validate_reference_value(anchor_reference)
    if anchor["transition_kind"] != "theory_and_commission_anchor":
        raise ContractError("aggregation input anchor has the wrong transition kind")
    if len(observation_references) != len(WORLD_IDS):
        raise ContractError("aggregation input requires five observation commits")
    observations = [
        _validate_reference_value(reference)
        for reference in observation_references
    ]
    for ordinal, reference in enumerate(observations):
        if (
            reference["transition_kind"] != "world_observation"
            or reference["programme_id"] != anchor["programme_id"]
            or reference["target_id"] != anchor["target_id"]
            or reference["run_id"] != anchor["run_id"]
            or reference["generation"] != anchor["generation"] + ordinal + 1
            or reference["prior_generation"] != reference["generation"] - 1
            or reference["frozen_theory_state_projection_digest"]
            != anchor["frozen_theory_state_projection_digest"]
        ):
            raise ContractError("aggregation input commit vector is not one ordered chain")
    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "input_kind": "ordered_committed_world_matrix_inputs",
        "programme_id": anchor["programme_id"],
        "target_id": anchor["target_id"],
        "run_id": anchor["run_id"],
        "commission_id": validate_identifier(commission_id, "commission_id"),
        "commission_digest": commission_digest,
        "anchor_commit": copy.deepcopy(anchor),
        "observation_commits": copy.deepcopy(observations),
        "world_ids": list(WORLD_IDS),
    }
    manifest["input_digest"] = _self_digest(manifest, "input_digest")
    validate_payload(manifest, AGGREGATION_INPUT_SCHEMA)
    return manifest


def _validate_aggregation_input_manifest(
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(manifest))
    validate_payload(record, AGGREGATION_INPUT_SCHEMA)
    expected = build_world_matrix_aggregation_input_manifest(
        anchor_reference=record["anchor_commit"],
        observation_references=record["observation_commits"],
        commission_id=record["commission_id"],
        commission_digest=record["commission_digest"],
    )
    if record != expected:
        raise ContractError("aggregation input manifest digest or ordering changed")
    return record


def _require_aggregation_producer_input(
    binding: Mapping[str, Any], manifest: Mapping[str, Any]
) -> None:
    """Require the producer request—not only its output—to name all six commits."""

    try:
        requested = binding["producer_request"]["value"]["parameters"][
            "aggregation_input_manifest"
        ]
    except (KeyError, TypeError) as exc:
        raise ContractError(
            "aggregation producer request lacks the committed input manifest"
        ) from exc
    if requested != manifest:
        raise ContractError(
            "aggregation producer request consumed different committed inputs"
        )


def _world_request_causal_input(
    *,
    commission: Mapping[str, Any],
    commission_binding: Mapping[str, Any],
    request: Mapping[str, Any],
) -> dict[str, Any]:
    """Describe the exact predecessor that a request producer must declare."""

    return {
        "world_id": request["world_id"],
        "world_plan_digest": request["world_plan_digest"],
        "commission_id": commission["commission_id"],
        "commission_digest": commission["commission_digest"],
        "commission_producer_binding_id": commission_binding["binding_id"],
        "commission_producer_binding_digest": commission_binding[
            "binding_digest"
        ],
    }


def build_world_request_batch(
    *,
    commission: Mapping[str, Any],
    commission_producer_binding: Mapping[str, Any],
    world_requests: Mapping[str, Mapping[str, Any]],
    world_request_producer_bindings: Mapping[str, Mapping[str, Any]],
    evidence_resolver: CommittedCausalEvidenceResolver,
) -> dict[str, Any]:
    """Validate and order all five requests before the anchor can commit."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    commission_binding = validate_experiment_causal_producer_binding(
        commission_producer_binding,
        expected_stage_id=COMMISSION_STAGE_ID,
        expected_producer_role=COMMISSION_PRODUCER_ROLE,
        expected_artifact=sealed,
        expected_artifact_id=sealed["commission_id"],
        evidence_resolver=evidence_resolver,
    )
    if set(world_requests) != set(WORLD_IDS) or set(
        world_request_producer_bindings
    ) != set(WORLD_IDS):
        raise ContractError(
            "world request batch requires exactly one request and producer per world"
        )
    requests: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    for world_id in WORLD_IDS:
        request = validate_experiment_world_request(
            sealed,
            world_requests[world_id],
            evidence_resolver=evidence_resolver,
        )
        binding = validate_experiment_causal_producer_binding(
            world_request_producer_bindings[world_id],
            expected_stage_id=WORLD_REQUEST_STAGE_ID,
            expected_producer_role=WORLD_REQUEST_PRODUCER_ROLE,
            expected_artifact=request,
            expected_artifact_id=request["request_id"],
            evidence_resolver=evidence_resolver,
        )
        try:
            declared_input = binding["producer_request"]["value"]["parameters"][
                "causal_input"
            ]
        except (KeyError, TypeError) as exc:
            raise ContractError(
                f"world request producer {world_id} lacks its exact causal input"
            ) from exc
        if (
            request["world_id"] != world_id
            or request["commission_input"] != sealed
            or request["commission_producer_binding"] != commission_binding
            or declared_input
            != _world_request_causal_input(
                commission=sealed,
                commission_binding=commission_binding,
                request=request,
            )
        ):
            raise ContractError(
                f"world request producer {world_id} consumed a different predecessor"
            )
        requests.append(request)
        bindings.append(binding)

    uniqueness_vectors = (
        [request["request_id"] for request in requests],
        [binding["binding_id"] for binding in bindings],
        [binding["evidence_authority_id"] for binding in bindings],
        [
            binding["producer_request"]["value"]["request_id"]
            for binding in bindings
        ],
        [
            binding["producer_receipt"]["value"]["receipt_id"]
            for binding in bindings
        ],
        [
            binding["producer_receipt"]["value"]["invocation_id"]
            for binding in bindings
        ],
        [
            binding["artifact_evidence"]["immutable_history_path"]
            for binding in bindings
        ],
    )
    if any(len(values) != len(set(values)) for values in uniqueness_vectors):
        raise ContractError("world request batch reused producer or request identity")
    batch: dict[str, Any] = {
        "schema_version": "1.0.0",
        "batch_kind": "ordered_pre_execution_world_requests",
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "world_order": list(WORLD_IDS),
        "requests": requests,
        "request_producer_bindings": bindings,
    }
    batch["batch_digest"] = _self_digest(batch, "batch_digest")
    validate_payload(batch, WORLD_REQUEST_BATCH_SCHEMA)
    return batch


def _validate_world_request_batch(
    batch: Mapping[str, Any],
    *,
    commission: Mapping[str, Any],
    commission_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver,
) -> dict[str, Any]:
    record = copy.deepcopy(dict(batch))
    validate_payload(record, WORLD_REQUEST_BATCH_SCHEMA)
    expected = build_world_request_batch(
        commission=commission,
        commission_producer_binding=commission_producer_binding,
        world_requests={
            world_id: record["requests"][ordinal]
            for ordinal, world_id in enumerate(WORLD_IDS)
        },
        world_request_producer_bindings={
            world_id: record["request_producer_bindings"][ordinal]
            for ordinal, world_id in enumerate(WORLD_IDS)
        },
        evidence_resolver=evidence_resolver,
    )
    if record != expected:
        raise ContractError("world request batch content, order, or digest changed")
    return record


def _reopen_world_matrix_transition_snapshot(
    store: DiscoveryTransactionStore,
    reference: Mapping[str, Any],
    *,
    expected_programme_id: str | None = None,
    expected_transition_kind: str | None = None,
    context: VerifiedArtifactContext | None = None,
) -> tuple[dict[str, Any], _VerifiedWorldTransitionSnapshot]:
    """Reopen a reference and its exact transition/evidence byte batch."""

    if context is None:
        with store.verified_artifact_context() as verified_context:
            return _reopen_world_matrix_transition_snapshot(
                store,
                reference,
                expected_programme_id=expected_programme_id,
                expected_transition_kind=expected_transition_kind,
                context=verified_context,
            )
    context.assert_owned_by(store)

    record = _validate_reference_value(reference)
    if record["target_id"] != store.target_id or record["run_id"] != store.run_id:
        raise ContractError("portable commit reference crossed target/run")
    if expected_programme_id is not None and record["programme_id"] != expected_programme_id:
        raise ContractError("portable commit reference crossed programme")
    if expected_transition_kind is not None and record["transition_kind"] != expected_transition_kind:
        raise ContractError("portable commit reference has the wrong transition kind")
    snapshot = _read_verified_transition_snapshot(
        context=context,
        generation=record["generation"],
        programme_id=record["programme_id"],
        transition_path=record["transition_artifact"]["path"],
    )
    commit = snapshot.commit
    expected = build_world_matrix_commit_reference(
        commit,
        programme_id=record["programme_id"],
        transition_kind=record["transition_kind"],
        transition_artifact_path=record["transition_artifact"]["path"],
    )
    if record != expected:
        raise StateCorruptionError("portable commit reference differs from immutable commit")
    transition = snapshot.transition
    if (
        transition.get("programme_id") != record["programme_id"]
        or transition.get("transition_kind") != record["transition_kind"]
        or transition.get("expected_commit_generation") != record["generation"]
    ):
        raise StateCorruptionError("portable reference names a different transition")
    return record, snapshot


def reopen_world_matrix_commit_reference(
    store: DiscoveryTransactionStore,
    reference: Mapping[str, Any],
    *,
    expected_programme_id: str | None = None,
    expected_transition_kind: str | None = None,
) -> VerifiedCommit:
    """Reopen a portable reference exclusively through verified commit bytes."""

    _, snapshot = _reopen_world_matrix_transition_snapshot(
        store,
        reference,
        expected_programme_id=expected_programme_id,
        expected_transition_kind=expected_transition_kind,
    )
    return snapshot.commit


def _validate_anchor_transition(
    snapshot: _VerifiedWorldTransitionSnapshot,
    *,
    resolver: CommittedCausalEvidenceResolver,
    object_cache: dict[
        tuple[int, str], tuple[dict[str, Any], dict[str, Any]]
    ],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(snapshot.transition))
    validate_payload(record, ANCHOR_TRANSITION_SCHEMA)
    if record["transition_digest"] != _self_digest(record, "transition_digest"):
        raise ContractError("world-matrix anchor transition digest drifted")
    programme_id = record["programme_id"]
    commission = _load_committed_object(
        snapshot,
        record["commission_object"],
        expected_kind="world_matrix_commission",
        expected_path=_anchor_object_path(programme_id, "commission.json"),
        cache=object_cache,
    )
    commission_binding = _load_committed_object(
        snapshot,
        record["commission_producer_binding_object"],
        expected_kind="causal_producer_binding",
        expected_path=_anchor_object_path(
            programme_id, "commission-producer-binding.json"
        ),
        cache=object_cache,
    )
    requests = [
        _load_committed_object(
            snapshot,
            descriptor,
            expected_kind="world_request",
            expected_path=_anchor_object_path(
                programme_id, f"requests/{ordinal:02d}-{world_id}.json"
            ),
            cache=object_cache,
        )
        for ordinal, (world_id, descriptor) in enumerate(
            zip(WORLD_IDS, record["world_request_objects"], strict=True)
        )
    ]
    request_bindings = [
        _load_committed_object(
            snapshot,
            descriptor,
            expected_kind="causal_producer_binding",
            expected_path=_anchor_object_path(
                programme_id,
                f"request-producer-bindings/{ordinal:02d}-{world_id}.json",
            ),
            cache=object_cache,
        )
        for ordinal, (world_id, descriptor) in enumerate(
            zip(
                WORLD_IDS,
                record["world_request_producer_binding_objects"],
                strict=True,
            )
        )
    ]
    projection = validate_experiment_authority_projection(
        commission["authority_projection"]
    )
    prior_identity = _validate_verified_commit_identity(
        record["prior_commit_identity"]
    )
    ancestor = _projection_component_value(projection, "committed_ancestor")
    commission = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=resolver
    )
    binding = validate_experiment_causal_producer_binding(
        commission_binding,
        expected_stage_id=COMMISSION_STAGE_ID,
        expected_producer_role=COMMISSION_PRODUCER_ROLE,
        expected_artifact=commission,
        expected_artifact_id=commission["commission_id"],
        evidence_resolver=resolver,
    )
    request_batch_value: dict[str, Any] = {
        "schema_version": "1.0.0",
        "batch_kind": "ordered_pre_execution_world_requests",
        "commission_id": commission["commission_id"],
        "commission_digest": commission["commission_digest"],
        "world_order": list(WORLD_IDS),
        "requests": requests,
        "request_producer_bindings": request_bindings,
        "batch_digest": record["world_request_batch_digest"],
    }
    request_batch = _validate_world_request_batch(
        request_batch_value,
        commission=commission,
        commission_producer_binding=binding,
        evidence_resolver=resolver,
    )
    if (
        record["expected_commit_generation"] != record["prior_generation"] + 1
        or record["programme_id"] != _programme_id(commission)
        or record["target_id"] != commission["target_id"]
        or record["run_id"] != commission["run_id"]
        or record["prior_generation"] != commission["prior_state_version"]
        or prior_identity["target_id"] != record["target_id"]
        or prior_identity["run_id"] != record["run_id"]
        or prior_identity["generation"] != record["prior_generation"]
        or prior_identity["state_semantic_digest"]
        != record["prior_state_semantic_digest"]
        or prior_identity["frozen_theory_state_projection_digest"]
        != record["frozen_theory_state_projection_digest"]
        or ancestor.get("generation") != prior_identity["generation"]
        or canonical_digest(ancestor.get("state"))
        != prior_identity["state_semantic_digest"]
        or ancestor.get("state_semantic_digest")
        != prior_identity["state_semantic_digest"]
        or record["authority_projection_id"] != projection["projection_id"]
        or record["authority_projection_digest"] != projection["projection_digest"]
        or record["commission_id"] != commission["commission_id"]
        or record["commission_digest"] != commission["commission_digest"]
        or record["world_request_batch_digest"] != request_batch["batch_digest"]
        or record["world_order"] != list(WORLD_IDS)
        or record["observed_world_ids"] != []
        or record["missing_world_ids"] != list(WORLD_IDS)
        or record["observation_count"] != 0
        or record["new_observation_count"] != 0
        or record["status"] != "commissioned"
        or record["certificate"] is not None
        or record["changed_state_paths"] != ["/generation"]
        or record["theory_state_changed"] is not False
        or record["authority_boundary"] != _AUTHORITY_BOUNDARY
    ):
        raise ContractError("world-matrix anchor transition drifted")
    hydrated = copy.deepcopy(record)
    hydrated["authority_projection"] = projection
    hydrated["commission"] = commission
    hydrated["commission_producer_binding"] = binding
    hydrated["world_request_batch"] = request_batch
    return hydrated


@world_matrix_validation_cache_scope
def prepare_canonical_world_matrix_anchor(
    *,
    prior_commit: VerifiedCommit,
    cycle_id: str,
    authority_projection: Mapping[str, Any],
    commission: Mapping[str, Any],
    commission_producer_binding: Mapping[str, Any],
    world_requests: Mapping[str, Mapping[str, Any]],
    world_request_producer_bindings: Mapping[str, Mapping[str, Any]],
    evidence_records: Sequence[CommittedCausalEvidencePaths],
) -> PreparedWorldMatrixAnchor:
    """Prepare anchor bytes without publishing any sidecar or state."""

    validate_identifier(cycle_id, "cycle_id")
    source_resolver = CommittedCausalEvidenceResolver(evidence_records)
    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=source_resolver
    )
    projection = validate_experiment_authority_projection(authority_projection)
    if projection != sealed["authority_projection"]:
        raise ContractError("anchor projection differs from the exact commission")
    _require_projection_matches_verified_ancestor(projection, prior_commit)
    programme_id = _programme_id(sealed)
    if (
        prior_commit.state["target_id"] != sealed["target_id"]
        or prior_commit.state["run_id"] != sealed["run_id"]
        or prior_commit.generation != sealed["prior_state_version"]
    ):
        raise ContractError("anchor commission crossed the verified prior commit")
    binding = validate_experiment_causal_producer_binding(
        commission_producer_binding,
        expected_stage_id=COMMISSION_STAGE_ID,
        expected_producer_role=COMMISSION_PRODUCER_ROLE,
        expected_artifact=sealed,
        expected_artifact_id=sealed["commission_id"],
        evidence_resolver=source_resolver,
    )
    request_batch = build_world_request_batch(
        commission=sealed,
        commission_producer_binding=binding,
        world_requests=world_requests,
        world_request_producer_bindings=world_request_producer_bindings,
        evidence_resolver=source_resolver,
    )
    next_state = _generation_only_next(prior_commit)
    prior_digest, next_digest, frozen_digest = _require_generation_only_transition(
        prior_commit, next_state
    )
    namespace = Namespace(
        sealed["target_id"],
        sealed["run_id"],
        WORLD_MATRIX_BRANCH_ID,
        prior_commit.generation,
    )
    evidence_artifacts, evidence_manifest = _prepare_commit_local_evidence(
        {
            "commission": sealed,
            "commission_producer_binding": binding,
            "world_request_batch": request_batch,
        },
        resolver=source_resolver,
        programme_id=programme_id,
        namespace=namespace,
    )
    commission_artifact, commission_descriptor = _committed_object_artifact(
        sealed,
        path=_anchor_object_path(programme_id, "commission.json"),
        object_kind="world_matrix_commission",
        namespace=namespace,
    )
    commission_binding_artifact, commission_binding_descriptor = (
        _committed_object_artifact(
            binding,
            path=_anchor_object_path(
                programme_id, "commission-producer-binding.json"
            ),
            object_kind="causal_producer_binding",
            namespace=namespace,
        )
    )
    request_artifacts: list[CommitArtifact] = []
    request_descriptors: list[dict[str, Any]] = []
    request_binding_descriptors: list[dict[str, Any]] = []
    for ordinal, world_id in enumerate(WORLD_IDS):
        request_artifact, request_descriptor = _committed_object_artifact(
            request_batch["requests"][ordinal],
            path=_anchor_object_path(
                programme_id, f"requests/{ordinal:02d}-{world_id}.json"
            ),
            object_kind="world_request",
            namespace=namespace,
        )
        request_binding_artifact, request_binding_descriptor = (
            _committed_object_artifact(
                request_batch["request_producer_bindings"][ordinal],
                path=_anchor_object_path(
                    programme_id,
                    f"request-producer-bindings/{ordinal:02d}-{world_id}.json",
                ),
                object_kind="causal_producer_binding",
                namespace=namespace,
            )
        )
        request_artifacts.extend((request_artifact, request_binding_artifact))
        request_descriptors.append(request_descriptor)
        request_binding_descriptors.append(request_binding_descriptor)
    transition: dict[str, Any] = {
        "schema_version": "2.0.0",
        "transition_kind": "theory_and_commission_anchor",
        "programme_id": programme_id,
        "target_id": sealed["target_id"],
        "run_id": sealed["run_id"],
        "prior_generation": prior_commit.generation,
        "prior_commit_identity": build_verified_commit_identity(prior_commit),
        "expected_commit_generation": prior_commit.generation + 1,
        "cycle_id": cycle_id,
        "authority_projection_id": projection["projection_id"],
        "authority_projection_digest": projection["projection_digest"],
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "commission_object": commission_descriptor,
        "commission_producer_binding_object": commission_binding_descriptor,
        "world_request_objects": request_descriptors,
        "world_request_producer_binding_objects": request_binding_descriptors,
        "world_request_batch_digest": request_batch["batch_digest"],
        "world_order": list(WORLD_IDS),
        "observed_world_ids": [],
        "missing_world_ids": list(WORLD_IDS),
        "observation_count": 0,
        "new_observation_count": 0,
        "status": "commissioned",
        "certificate": None,
        "prior_state_semantic_digest": prior_digest,
        "next_state_semantic_digest": next_digest,
        "changed_state_paths": ["/generation"],
        "theory_state_changed": False,
        "frozen_theory_state_projection_digest": frozen_digest,
        "commit_local_evidence_manifest": evidence_manifest,
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    transition["transition_digest"] = _self_digest(
        transition, "transition_digest"
    )
    validate_payload(transition, ANCHOR_TRANSITION_SCHEMA)
    transition_path = _anchor_path(programme_id)
    transition_bytes = canonical_json(transition)
    artifacts = (
        *evidence_artifacts,
        commission_artifact,
        commission_binding_artifact,
        *request_artifacts,
        CommitArtifact(transition_path, transition_bytes, namespace),
    )
    request_digest = canonical_digest(
        {
            "transition": transition,
            "artifacts": sorted(
                (
                    {
                        "path": artifact.relative_path,
                        "sha256": bytes_digest(
                            artifact.content
                            if isinstance(artifact.content, bytes)
                            else artifact.content.read_bytes()
                        ),
                    }
                    for artifact in artifacts
                ),
                key=lambda row: row["path"],
            ),
        }
    )
    return PreparedWorldMatrixAnchor(
        programme_id=programme_id,
        expected_generation=prior_commit.generation,
        next_state=next_state,
        transition=transition,
        transition_artifact_path=transition_path,
        commit_artifacts=tuple(artifacts),
        idempotency_key=stable_identifier(
            "world-anchor", sealed["commission_id"], prior_commit.generation
        ),
        request_digest=request_digest,
    )


@world_matrix_validation_cache_scope
def finalize_canonical_world_matrix_anchor(
    *,
    store: DiscoveryTransactionStore,
    commit_result: CommitResult,
    prepared: PreparedWorldMatrixAnchor,
) -> VerifiedWorldMatrixAnchorCommit:
    with store.verified_artifact_context() as context:
        snapshot = _read_verified_transition_snapshot(
            context=context,
            generation=commit_result.generation,
            programme_id=prepared.programme_id,
            transition_path=prepared.transition_artifact_path,
        )
        commit = snapshot.commit
        if (
            commit.commit_id != commit_result.commit_id
            or commit.manifest_digest != commit_result.manifest_digest
            or commit.state != prepared.next_state
        ):
            raise StateCorruptionError("winning anchor commit differs from prepared bytes")
        transition = snapshot.transition
        if transition != prepared.transition:
            raise StateCorruptionError("winning anchor transition differs from prepared bytes")
        sealed = _validate_anchor_transition(
            snapshot,
            resolver=snapshot.resolver,
            object_cache={},
        )
        prior_commit = context.read_commit(commit.prior_generation)
        if (
            sealed["prior_commit_identity"]
            != build_verified_commit_identity(prior_commit)
            or sealed["prior_state_semantic_digest"]
            != prior_commit.state_semantic_digest
            or sealed["next_state_semantic_digest"] != commit.state_semantic_digest
            or sealed["frozen_theory_state_projection_digest"]
            != _frozen_theory_digest(commit.state)
        ):
            raise StateCorruptionError("anchor state binding differs from committed state")
        reference = build_world_matrix_commit_reference(
            commit,
            programme_id=prepared.programme_id,
            transition_kind="theory_and_commission_anchor",
            transition_artifact_path=prepared.transition_artifact_path,
        )
        return VerifiedWorldMatrixCommit(sealed, reference, commit)


@world_matrix_validation_cache_scope
def commit_canonical_world_matrix_anchor(
    *,
    store: DiscoveryTransactionStore,
    expected_generation: int,
    cycle_id: str,
    authority_projection: Mapping[str, Any],
    commission: Mapping[str, Any],
    commission_producer_binding: Mapping[str, Any],
    world_requests: Mapping[str, Mapping[str, Any]],
    world_request_producer_bindings: Mapping[str, Mapping[str, Any]],
    evidence_records: Sequence[CommittedCausalEvidencePaths],
    failpoint: str | Callable[[str], None] | None = None,
) -> VerifiedWorldMatrixAnchorCommit:
    prior = store.read_verified_commit(expected_generation)
    prepared = prepare_canonical_world_matrix_anchor(
        prior_commit=prior,
        cycle_id=cycle_id,
        authority_projection=authority_projection,
        commission=commission,
        commission_producer_binding=commission_producer_binding,
        world_requests=world_requests,
        world_request_producer_bindings=world_request_producer_bindings,
        evidence_records=evidence_records,
    )
    result = store.commit(
        expected_generation=expected_generation,
        state=prepared.next_state,
        artifacts=prepared.commit_artifacts,
        idempotency_key=prepared.idempotency_key,
        request_digest=prepared.request_digest,
        failpoint=failpoint,
    )
    return finalize_canonical_world_matrix_anchor(
        store=store, commit_result=result, prepared=prepared
    )


def _validate_observation_transition(
    snapshot: _VerifiedWorldTransitionSnapshot,
    *,
    anchor_transition: Mapping[str, Any],
    resolver: CommittedCausalEvidenceResolver,
    object_cache: dict[
        tuple[int, str], tuple[dict[str, Any], dict[str, Any]]
    ],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(snapshot.transition))
    validate_payload(record, OBSERVATION_TRANSITION_SCHEMA)
    if record["transition_digest"] != _self_digest(record, "transition_digest"):
        raise ContractError("world observation transition digest drifted")
    ordinal = record["ordinal"]
    expected_world = WORLD_IDS[ordinal]
    envelope_value = _load_committed_object(
        snapshot,
        record["observation_envelope_object"],
        expected_kind="world_observation_envelope",
        expected_path=_observation_object_path(record["programme_id"], ordinal),
        cache=object_cache,
    )
    envelope = validate_experiment_world_observation_envelope(
        anchor_transition["commission"],
        envelope_value,
        evidence_resolver=resolver,
    )
    embedded_request = envelope["observation"]["world_request"]
    anchored_request = anchor_transition["world_request_batch"]["requests"][
        ordinal
    ]
    anchored_request_binding = anchor_transition["world_request_batch"][
        "request_producer_bindings"
    ][ordinal]
    if (
        record["programme_id"] != anchor_transition["programme_id"]
        or record["target_id"] != anchor_transition["target_id"]
        or record["run_id"] != anchor_transition["run_id"]
        or record["world_id"] != expected_world
        or envelope["world_id"] != expected_world
        or record["commission_id"] != anchor_transition["commission_id"]
        or record["commission_digest"] != anchor_transition["commission_digest"]
        or embedded_request["commission_input"] != anchor_transition["commission"]
        or embedded_request["commission_producer_binding"]
        != anchor_transition["commission_producer_binding"]
        or embedded_request != anchored_request
        or envelope["observation"]["world_request_producer_binding"]
        != anchored_request_binding
        or record["expected_commit_generation"]
        != record["anchor_commit"]["generation"] + ordinal + 1
        or record["observation_count"] != ordinal + 1
        or record["new_observation_count"] != 1
        or record["observed_world_ids"] != list(WORLD_IDS[: ordinal + 1])
        or record["missing_world_ids"] != list(WORLD_IDS[ordinal + 1 :])
        or record["status"]
        != ("ready_for_aggregation" if ordinal == 4 else "observations_in_progress")
        or record["certificate"] is not None
        or len(record["prior_observation_commits"]) != ordinal
        or record["parent_commit"]
        != (
            record["anchor_commit"]
            if ordinal == 0
            else record["prior_observation_commits"][-1]
        )
        or record["changed_state_paths"] != ["/generation"]
        or record["theory_state_changed"] is not False
        or record["authority_boundary"] != _AUTHORITY_BOUNDARY
    ):
        raise ContractError("world observation transition drifted")
    hydrated = copy.deepcopy(record)
    hydrated["observation_envelope"] = envelope
    return hydrated


@world_matrix_validation_cache_scope
def commit_canonical_world_matrix_observation(
    *,
    store: DiscoveryTransactionStore,
    anchor_reference: Mapping[str, Any],
    expected_generation: int,
    observation_envelope: Mapping[str, Any],
    evidence_records: Sequence[CommittedCausalEvidencePaths],
    failpoint: str | Callable[[str], None] | None = None,
) -> VerifiedWorldMatrixObservationCommit:
    chain = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor_reference,
        through_generation=expected_generation,
    )
    if chain["aggregation_transition"] is not None:
        raise ContractError("world matrix is already aggregated")
    ordinal = len(chain["observation_transitions"])
    if ordinal >= len(WORLD_IDS):
        raise ContractError("five observations are committed; aggregation is next")
    parent: VerifiedCommit = chain["verified_commits"][-1]
    if parent.generation != expected_generation:
        raise ContractError("observation expected generation differs from replay parent")
    source_resolver = CommittedCausalEvidenceResolver(evidence_records)
    anchor = chain["anchor_transition"]
    envelope = validate_experiment_world_observation_envelope(
        anchor["commission"],
        observation_envelope,
        evidence_resolver=source_resolver,
    )
    if envelope["world_id"] != WORLD_IDS[ordinal]:
        raise ContractError("observation is not the next canonical world")
    next_state = _generation_only_next(parent)
    prior_digest, next_digest, frozen_digest = _require_generation_only_transition(
        parent, next_state
    )
    namespace = Namespace(
        store.target_id, store.run_id, WORLD_MATRIX_BRANCH_ID, parent.generation
    )
    evidence_artifacts, evidence_manifest = _prepare_commit_local_evidence(
        envelope,
        resolver=source_resolver,
        programme_id=anchor["programme_id"],
        namespace=namespace,
        exclude_authority_ids=_evidence_authority_ids(
            [
                chain["anchor_transition_snapshot"],
                *chain["observation_transition_snapshots"],
            ]
        ),
    )
    envelope_artifact, envelope_descriptor = _committed_object_artifact(
        envelope,
        path=_observation_object_path(anchor["programme_id"], ordinal),
        object_kind="world_observation_envelope",
        namespace=namespace,
    )
    transition: dict[str, Any] = {
        "schema_version": "2.0.0",
        "transition_kind": "world_observation",
        "programme_id": anchor["programme_id"],
        "target_id": store.target_id,
        "run_id": store.run_id,
        "anchor_commit": copy.deepcopy(dict(chain["anchor_reference"])),
        "parent_commit": copy.deepcopy(dict(chain["commit_references"][-1])),
        "prior_observation_commits": copy.deepcopy(
            list(chain["observation_references"])
        ),
        "expected_commit_generation": parent.generation + 1,
        "ordinal": ordinal,
        "world_id": WORLD_IDS[ordinal],
        "commission_id": anchor["commission_id"],
        "commission_digest": anchor["commission_digest"],
        "observation_envelope_object": envelope_descriptor,
        "observed_world_ids": list(WORLD_IDS[: ordinal + 1]),
        "missing_world_ids": list(WORLD_IDS[ordinal + 1 :]),
        "observation_count": ordinal + 1,
        "new_observation_count": 1,
        "status": (
            "ready_for_aggregation" if ordinal == 4 else "observations_in_progress"
        ),
        "certificate": None,
        "prior_state_semantic_digest": prior_digest,
        "next_state_semantic_digest": next_digest,
        "changed_state_paths": ["/generation"],
        "theory_state_changed": False,
        "frozen_theory_state_projection_digest": frozen_digest,
        "commit_local_evidence_manifest": evidence_manifest,
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    transition["transition_digest"] = _self_digest(
        transition, "transition_digest"
    )
    validate_payload(transition, OBSERVATION_TRANSITION_SCHEMA)
    transition_path = _observation_path(anchor["programme_id"], ordinal)
    artifacts = (
        *evidence_artifacts,
        envelope_artifact,
        CommitArtifact(transition_path, canonical_json(transition), namespace),
    )
    request_digest = canonical_digest(
        {
            "transition": transition,
            "artifact_digests": sorted(
                bytes_digest(
                    artifact.content
                    if isinstance(artifact.content, bytes)
                    else artifact.content.read_bytes()
                )
                for artifact in artifacts
            ),
        }
    )
    result = store.commit(
        expected_generation=parent.generation,
        state=next_state,
        artifacts=artifacts,
        idempotency_key=stable_identifier(
            "world-observation",
            anchor["commission_id"],
            ordinal,
            envelope["envelope_id"],
        ),
        request_digest=request_digest,
        failpoint=failpoint,
    )
    replayed = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor_reference,
        through_generation=result.generation,
    )
    committed_snapshot = replayed["observation_transition_snapshots"][-1]
    committed = committed_snapshot.commit
    if committed_snapshot.transition != transition or committed.state != next_state:
        raise StateCorruptionError("winning observation commit differs from proposed bytes")
    reference = replayed["observation_references"][-1]
    return VerifiedWorldMatrixCommit(
        replayed["observation_transitions"][-1], reference, committed
    )


def _validate_aggregation_transition(
    snapshot: _VerifiedWorldTransitionSnapshot,
    *,
    anchor_transition: Mapping[str, Any],
    envelopes: Sequence[Mapping[str, Any]],
    resolver: CommittedCausalEvidenceResolver,
    object_cache: dict[
        tuple[int, str], tuple[dict[str, Any], dict[str, Any]]
    ],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(snapshot.transition))
    validate_payload(record, AGGREGATION_TRANSITION_SCHEMA)
    if record["transition_digest"] != _self_digest(record, "transition_digest"):
        raise ContractError("world aggregation transition digest drifted")
    certificate_value = _load_committed_object(
        snapshot,
        record["certificate_object"],
        expected_kind="world_matrix_certificate",
        expected_path=_aggregation_object_path(
            record["programme_id"], "certificate.json"
        ),
        cache=object_cache,
    )
    binding_value = _load_committed_object(
        snapshot,
        record["aggregation_producer_binding_object"],
        expected_kind="causal_producer_binding",
        expected_path=_aggregation_object_path(
            record["programme_id"], "aggregation-producer-binding.json"
        ),
        cache=object_cache,
    )
    input_manifest = _validate_aggregation_input_manifest(
        record["aggregation_input_manifest"]
    )
    expected_input_manifest = build_world_matrix_aggregation_input_manifest(
        anchor_reference=record["anchor_commit"],
        observation_references=record["observation_commits"],
        commission_id=record["commission_id"],
        commission_digest=record["commission_digest"],
    )
    certificate = validate_experiment_world_matrix_certificate_v2(
        anchor_transition["commission"],
        envelopes,
        certificate_value,
        evidence_resolver=resolver,
    )
    binding = validate_experiment_causal_producer_binding(
        binding_value,
        expected_stage_id=MATRIX_AGGREGATION_STAGE_ID,
        expected_producer_role=MATRIX_AGGREGATION_PRODUCER_ROLE,
        expected_artifact=certificate,
        expected_artifact_id=certificate["certificate_id"],
        evidence_resolver=resolver,
    )
    _require_aggregation_producer_input(binding, input_manifest)
    if (
        record["programme_id"] != anchor_transition["programme_id"]
        or record["target_id"] != anchor_transition["target_id"]
        or record["run_id"] != anchor_transition["run_id"]
        or record["commission_id"] != anchor_transition["commission_id"]
        or record["commission_digest"] != anchor_transition["commission_digest"]
        or record["world_ids"] != list(WORLD_IDS)
        or record["observation_count"] != len(WORLD_IDS)
        or record["new_observation_count"] != 0
        or record["status"] != "complete"
        or record["parent_commit"] != record["observation_commits"][-1]
        or input_manifest != expected_input_manifest
        or record["expected_commit_generation"]
        != record["anchor_commit"]["generation"] + len(WORLD_IDS) + 1
        or record["changed_state_paths"] != ["/generation"]
        or record["theory_state_changed"] is not False
        or record["authority_boundary"] != _AUTHORITY_BOUNDARY
    ):
        raise ContractError("world aggregation transition drifted")
    hydrated = copy.deepcopy(record)
    hydrated["certificate"] = certificate
    hydrated["aggregation_producer_binding"] = binding
    return hydrated


def _derive_certificate_from_replayed_world_prefix(
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive a certificate solely from an already verified committed prefix."""

    if chain["aggregation_transition"] is not None:
        raise ContractError("world matrix is already aggregated")
    if (
        chain["status"] != "ready_for_aggregation"
        or len(chain["observation_transitions"]) != len(WORLD_IDS)
        or len(chain["observation_envelopes"]) != len(WORLD_IDS)
    ):
        raise ContractError("certificate derivation requires five committed observations")
    prefix_snapshots = [
        chain["anchor_transition_snapshot"],
        *chain["observation_transition_snapshots"],
    ]
    return validate_five_world_matrix(
        chain["anchor_transition"]["commission"],
        chain["observation_envelopes"],
        evidence_resolver=_combined_resolver(prefix_snapshots),
    )


@world_matrix_validation_cache_scope
def derive_canonical_world_matrix_certificate(
    store: DiscoveryTransactionStore,
    anchor_reference: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive the pre-aggregation certificate from committed bytes only.

    The function accepts no evidence paths or caller-authored envelopes.  It
    holds one verified artifact context across exact prefix replay and
    certificate derivation, and rejects incomplete, historical-extra, or
    already aggregated chains.
    """

    with store.verified_artifact_context() as context:
        chain = replay_canonical_world_matrix_commit_chain(
            store=store,
            anchor_reference=anchor_reference,
            verified_context=context,
        )
        if (
            chain["chain_terminal_generation"] != context.current_generation
            or chain["replay_scope"] != "active_current"
        ):
            raise ContractError(
                "certificate derivation requires the active committed observation prefix"
            )
        return _derive_certificate_from_replayed_world_prefix(chain)


@world_matrix_validation_cache_scope
def commit_canonical_world_matrix_aggregation(
    *,
    store: DiscoveryTransactionStore,
    anchor_reference: Mapping[str, Any],
    expected_generation: int,
    aggregation_producer_binding: Mapping[str, Any],
    evidence_records: Sequence[CommittedCausalEvidencePaths],
    failpoint: str | Callable[[str], None] | None = None,
) -> VerifiedWorldMatrixAggregationCommit:
    chain = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor_reference,
        through_generation=expected_generation,
    )
    if len(chain["observation_transitions"]) != len(WORLD_IDS):
        raise ContractError("aggregation requires five committed observations")
    if chain["aggregation_transition"] is not None:
        raise ContractError("world matrix is already aggregated")
    parent: VerifiedCommit = chain["verified_commits"][-1]
    prefix_snapshots = [
        chain["anchor_transition_snapshot"],
        *chain["observation_transition_snapshots"],
    ]
    certificate = _derive_certificate_from_replayed_world_prefix(chain)
    source_resolver = CommittedCausalEvidenceResolver(evidence_records)
    binding = validate_experiment_causal_producer_binding(
        aggregation_producer_binding,
        expected_stage_id=MATRIX_AGGREGATION_STAGE_ID,
        expected_producer_role=MATRIX_AGGREGATION_PRODUCER_ROLE,
        expected_artifact=certificate,
        expected_artifact_id=certificate["certificate_id"],
        evidence_resolver=source_resolver,
    )
    input_manifest = build_world_matrix_aggregation_input_manifest(
        anchor_reference=chain["anchor_reference"],
        observation_references=chain["observation_references"],
        commission_id=chain["anchor_transition"]["commission_id"],
        commission_digest=chain["anchor_transition"]["commission_digest"],
    )
    _require_aggregation_producer_input(binding, input_manifest)
    next_state = _generation_only_next(parent)
    prior_digest, next_digest, frozen_digest = _require_generation_only_transition(
        parent, next_state
    )
    anchor = chain["anchor_transition"]
    namespace = Namespace(
        store.target_id, store.run_id, WORLD_MATRIX_BRANCH_ID, parent.generation
    )
    evidence_artifacts, evidence_manifest = _prepare_commit_local_evidence(
        binding,
        resolver=source_resolver,
        programme_id=anchor["programme_id"],
        namespace=namespace,
        exclude_authority_ids=_evidence_authority_ids(prefix_snapshots),
    )
    certificate_artifact, certificate_descriptor = _committed_object_artifact(
        certificate,
        path=_aggregation_object_path(anchor["programme_id"], "certificate.json"),
        object_kind="world_matrix_certificate",
        namespace=namespace,
    )
    aggregation_binding_artifact, aggregation_binding_descriptor = (
        _committed_object_artifact(
            binding,
            path=_aggregation_object_path(
                anchor["programme_id"], "aggregation-producer-binding.json"
            ),
            object_kind="causal_producer_binding",
            namespace=namespace,
        )
    )
    transition: dict[str, Any] = {
        "schema_version": "2.0.0",
        "transition_kind": "world_matrix_aggregation",
        "programme_id": anchor["programme_id"],
        "target_id": store.target_id,
        "run_id": store.run_id,
        "anchor_commit": copy.deepcopy(dict(chain["anchor_reference"])),
        "parent_commit": copy.deepcopy(dict(chain["observation_references"][-1])),
        "observation_commits": copy.deepcopy(list(chain["observation_references"])),
        "expected_commit_generation": parent.generation + 1,
        "commission_id": anchor["commission_id"],
        "commission_digest": anchor["commission_digest"],
        "world_ids": list(WORLD_IDS),
        "observation_count": len(WORLD_IDS),
        "new_observation_count": 0,
        "status": "complete",
        "certificate_object": certificate_descriptor,
        "aggregation_input_manifest": input_manifest,
        "aggregation_producer_binding_object": aggregation_binding_descriptor,
        "prior_state_semantic_digest": prior_digest,
        "next_state_semantic_digest": next_digest,
        "changed_state_paths": ["/generation"],
        "theory_state_changed": False,
        "frozen_theory_state_projection_digest": frozen_digest,
        "commit_local_evidence_manifest": evidence_manifest,
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    transition["transition_digest"] = _self_digest(
        transition, "transition_digest"
    )
    validate_payload(transition, AGGREGATION_TRANSITION_SCHEMA)
    transition_path = _aggregation_path(anchor["programme_id"])
    artifacts = (
        *evidence_artifacts,
        certificate_artifact,
        aggregation_binding_artifact,
        CommitArtifact(transition_path, canonical_json(transition), namespace),
    )
    result = store.commit(
        expected_generation=parent.generation,
        state=next_state,
        artifacts=artifacts,
        idempotency_key=stable_identifier(
            "world-aggregation", anchor["commission_id"], certificate["certificate_id"]
        ),
        request_digest=canonical_digest(
            {
                "transition": transition,
                "artifact_digests": sorted(
                    bytes_digest(
                        artifact.content
                        if isinstance(artifact.content, bytes)
                        else artifact.content.read_bytes()
                    )
                    for artifact in artifacts
                ),
            }
        ),
        failpoint=failpoint,
    )
    replayed = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor_reference,
        through_generation=result.generation,
    )
    committed_snapshot = replayed["aggregation_transition_snapshot"]
    if committed_snapshot is None:
        raise StateCorruptionError("winning aggregation commit was not replayed")
    committed = committed_snapshot.commit
    if committed_snapshot.transition != transition or committed.state != next_state:
        raise StateCorruptionError("winning aggregation commit differs from proposed bytes")
    return VerifiedWorldMatrixCommit(
        replayed["aggregation_transition"],
        replayed["aggregation_reference"],
        committed,
    )


@world_matrix_validation_cache_scope
def replay_canonical_world_matrix_commit_chain(
    *,
    store: DiscoveryTransactionStore,
    anchor_reference: Mapping[str, Any],
    through_generation: int | None = None,
    verified_context: VerifiedArtifactContext | None = None,
) -> dict[str, Any]:
    """Rebuild an exact active or historical canonical world prefix.

    ``through_generation`` selects historical replay explicitly.  When the
    store has advanced beyond the seven-transition chain, replay stops at the
    aggregation by contract but reports that terminal and the newer store head
    separately; it never silently presents the old certificate as current.
    Without ``verified_context`` this function opens one lock-scoped context
    and verifies the entire immutable prefix exactly once.  Supplying a live
    context permits several replay views over that same cached byte authority.
    """

    if verified_context is None:
        with store.verified_artifact_context() as context:
            return replay_canonical_world_matrix_commit_chain(
                store=store,
                anchor_reference=anchor_reference,
                through_generation=through_generation,
                verified_context=context,
            )
    verified_context.assert_owned_by(store)
    object_cache: dict[
        tuple[int, str], tuple[dict[str, Any], dict[str, Any]]
    ] = {}

    anchor_ref, anchor_snapshot = _reopen_world_matrix_transition_snapshot(
        store,
        anchor_reference,
        expected_transition_kind="theory_and_commission_anchor",
        context=verified_context,
    )
    anchor_commit = anchor_snapshot.commit
    anchor = _validate_anchor_transition(
        anchor_snapshot,
        resolver=anchor_snapshot.resolver,
        object_cache=object_cache,
    )
    prior = verified_context.read_commit(anchor_commit.prior_generation)
    expected_anchor_state = _generation_only_next(prior)
    if (
        anchor_commit.state != expected_anchor_state
        or anchor["prior_commit_identity"] != build_verified_commit_identity(prior)
        or _require_projection_matches_verified_ancestor(
            anchor["authority_projection"], prior
        )
        != _projection_component_value(
            anchor["authority_projection"], "committed_ancestor"
        )
        or anchor["prior_state_semantic_digest"] != prior.state_semantic_digest
        or anchor["next_state_semantic_digest"] != anchor_commit.state_semantic_digest
        or anchor["frozen_theory_state_projection_digest"]
        != _frozen_theory_digest(anchor_commit.state)
    ):
        raise StateCorruptionError("anchor state is not a generation-only transition")

    current = verified_context.current_generation
    selected_terminal = current if through_generation is None else through_generation
    if (
        isinstance(selected_terminal, bool)
        or not isinstance(selected_terminal, int)
        or selected_terminal < anchor_commit.generation
        or selected_terminal > current
    ):
        raise ContractError("world replay terminal generation is unavailable")
    maximum = anchor_commit.generation + len(WORLD_IDS) + 1
    chain_terminal = min(selected_terminal, maximum)

    commits: list[VerifiedCommit] = [anchor_commit]
    references: list[dict[str, Any]] = [copy.deepcopy(anchor_ref)]
    observation_snapshots: list[_VerifiedWorldTransitionSnapshot] = []
    observation_transitions: list[dict[str, Any]] = []
    observation_references: list[dict[str, Any]] = []
    envelopes: list[dict[str, Any]] = []
    parent = anchor_commit
    for ordinal in range(len(WORLD_IDS)):
        generation = anchor_commit.generation + ordinal + 1
        if generation > chain_terminal:
            break
        path = _observation_path(anchor["programme_id"], ordinal)
        snapshot = _read_verified_transition_snapshot(
            context=verified_context,
            generation=generation,
            programme_id=anchor["programme_id"],
            transition_path=path,
        )
        commit = snapshot.commit
        resolver = _combined_resolver(
            [anchor_snapshot, *observation_snapshots, snapshot]
        )
        sealed = _validate_observation_transition(
            snapshot,
            anchor_transition=anchor,
            resolver=resolver,
            object_cache=object_cache,
        )
        expected_state = _generation_only_next(parent)
        if (
            commit.prior_generation != parent.generation
            or commit.state != expected_state
            or sealed["prior_state_semantic_digest"] != parent.state_semantic_digest
            or sealed["next_state_semantic_digest"] != commit.state_semantic_digest
            or sealed["frozen_theory_state_projection_digest"]
            != anchor["frozen_theory_state_projection_digest"]
            or sealed["anchor_commit"] != anchor_ref
            or sealed["prior_observation_commits"] != observation_references
            or sealed["parent_commit"] != references[-1]
        ):
            raise StateCorruptionError("observation commit ancestry or theory state drifted")
        reference = build_world_matrix_commit_reference(
            commit,
            programme_id=anchor["programme_id"],
            transition_kind="world_observation",
            transition_artifact_path=path,
        )
        commits.append(commit)
        references.append(reference)
        observation_snapshots.append(snapshot)
        observation_transitions.append(sealed)
        observation_references.append(reference)
        envelopes.append(sealed["observation_envelope"])
        parent = commit

    aggregation_transition: dict[str, Any] | None = None
    aggregation_reference: dict[str, Any] | None = None
    aggregation_snapshot: _VerifiedWorldTransitionSnapshot | None = None
    aggregation_generation = anchor_commit.generation + len(WORLD_IDS) + 1
    if aggregation_generation <= chain_terminal:
        if len(observation_transitions) != len(WORLD_IDS):
            raise StateCorruptionError("aggregation was interposed before five observations")
        path = _aggregation_path(anchor["programme_id"])
        aggregation_snapshot = _read_verified_transition_snapshot(
            context=verified_context,
            generation=aggregation_generation,
            programme_id=anchor["programme_id"],
            transition_path=path,
        )
        commit = aggregation_snapshot.commit
        resolver = _combined_resolver(
            [anchor_snapshot, *observation_snapshots, aggregation_snapshot]
        )
        sealed = _validate_aggregation_transition(
            aggregation_snapshot,
            anchor_transition=anchor,
            envelopes=envelopes,
            resolver=resolver,
            object_cache=object_cache,
        )
        expected_state = _generation_only_next(parent)
        if (
            commit.prior_generation != parent.generation
            or commit.state != expected_state
            or sealed["prior_state_semantic_digest"] != parent.state_semantic_digest
            or sealed["next_state_semantic_digest"] != commit.state_semantic_digest
            or sealed["frozen_theory_state_projection_digest"]
            != anchor["frozen_theory_state_projection_digest"]
            or sealed["anchor_commit"] != anchor_ref
            or sealed["observation_commits"] != observation_references
            or sealed["parent_commit"] != observation_references[-1]
        ):
            raise StateCorruptionError("aggregation commit ancestry or theory state drifted")
        aggregation_reference = build_world_matrix_commit_reference(
            commit,
            programme_id=anchor["programme_id"],
            transition_kind="world_matrix_aggregation",
            transition_artifact_path=path,
        )
        aggregation_transition = sealed
        commits.append(commit)
        references.append(aggregation_reference)

    if aggregation_transition is not None:
        status = "complete"
    elif len(observation_transitions) == len(WORLD_IDS):
        status = "ready_for_aggregation"
    elif observation_transitions:
        status = "observations_in_progress"
    else:
        status = "commissioned"
    chain_is_store_head = chain_terminal == current
    active_current_authority = (
        aggregation_transition is not None
        and aggregation_generation == current
        and chain_is_store_head
    )
    if active_current_authority:
        authority_status = "active_current_aggregated"
    elif aggregation_transition is not None:
        authority_status = "historical_aggregated"
    else:
        authority_status = "inactive_incomplete"
    return {
        "status": status,
        "authority_status": authority_status,
        "active_current_authority": active_current_authority,
        "replay_scope": "active_current" if chain_is_store_head else "historical",
        "selected_terminal_generation": selected_terminal,
        "chain_terminal_generation": chain_terminal,
        "store_current_generation": current,
        "programme_id": anchor["programme_id"],
        "anchor_transition": anchor,
        "anchor_reference": copy.deepcopy(anchor_ref),
        "observation_transitions": observation_transitions,
        "observation_references": observation_references,
        "observation_envelopes": envelopes,
        "aggregation_transition": aggregation_transition,
        "aggregation_reference": aggregation_reference,
        "certificate": (
            None
            if aggregation_transition is None
            else aggregation_transition["certificate"]
        ),
        "verified_commits": commits,
        "commit_references": references,
        "anchor_transition_snapshot": anchor_snapshot,
        "observation_transition_snapshots": observation_snapshots,
        "aggregation_transition_snapshot": aggregation_snapshot,
        "verified_object_count": len(object_cache),
    }


def require_active_canonical_world_matrix_commit_chain(
    *,
    store: DiscoveryTransactionStore,
    anchor_reference: Mapping[str, Any],
) -> dict[str, Any]:
    """Require aggregation itself to be the current committed generation."""

    replay = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor_reference,
    )
    if replay["active_current_authority"] is not True:
        raise ContractError(
            "active world-matrix authority requires aggregation at current generation"
        )
    return replay


__all__ = [
    "AGGREGATION_TRANSITION_SCHEMA",
    "AGGREGATION_INPUT_SCHEMA",
    "ANCHOR_TRANSITION_SCHEMA",
    "COMMIT_REFERENCE_SCHEMA",
    "OBSERVATION_TRANSITION_SCHEMA",
    "OBJECT_DESCRIPTOR_SCHEMA",
    "WORLD_REQUEST_BATCH_SCHEMA",
    "PreparedWorldMatrixAnchor",
    "VerifiedWorldMatrixAggregationCommit",
    "VerifiedWorldMatrixAnchorCommit",
    "VerifiedWorldMatrixCommit",
    "VerifiedWorldMatrixObservationCommit",
    "build_world_matrix_commit_reference",
    "build_verified_commit_identity",
    "build_world_matrix_aggregation_input_manifest",
    "build_world_request_batch",
    "commit_canonical_world_matrix_aggregation",
    "commit_canonical_world_matrix_anchor",
    "commit_canonical_world_matrix_observation",
    "derive_canonical_world_matrix_certificate",
    "finalize_canonical_world_matrix_anchor",
    "prepare_canonical_world_matrix_anchor",
    "reopen_world_matrix_commit_reference",
    "require_active_canonical_world_matrix_commit_chain",
    "replay_canonical_world_matrix_commit_chain",
    "validate_world_matrix_object_descriptor",
]
