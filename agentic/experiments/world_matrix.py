# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Precommit one theory claim across the declared five experiment worlds.

The matrix is a controlled theory-support comparison, not five unrelated
experiments.  This module freezes the registered premise and every
adapter-independent spec field before execution, permits only the declared
adapter/model/resource interventions, and keeps even the no-probe world bound
to that same unexecuted commission.  Per-world bindings remain explicitly
non-authoritative: only the registered-premise falsifier may request a pending
reflective review, and no world may mutate theory, ontology, proof, or evidence.

The original v1 record is retained as a diagnostic compatibility projection.
It binds a spec family, but it contains only digests for most of the surrounding
theory state and therefore cannot authorize canonical execution.  The v2 lane
below is the authoritative boundary: it seals actual closed authority values,
their schema/projector identity, all five exact world plans, and the commission
bytes consumed by each pre-execution request.  Post-world observations carry
the actual authority projection again, so changed-path and denial claims are
computed rather than accepted from a caller.
"""

from __future__ import annotations

import base64
import contextlib
import contextvars
import copy
import datetime as dt
import functools
import json
import os
import stat
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from agentic.discovery.receipts import (
    validate_operator_receipt_identity,
    validate_operator_request_identity,
)

from .runtime import validate_experiment_receipt, validate_experiment_spec


COMMISSION_SCHEMA = "dynamic_experiment_world_matrix_commission_v1.schema.json"
COMMISSION_CONTRACT_VERSION = "dynamic-experiment-world-matrix-commission/1.0.0"
COMMISSION_V2_SCHEMA = "dynamic_experiment_world_matrix_commission_v2.schema.json"
OBSERVATION_V2_SCHEMA = "dynamic_experiment_world_matrix_observation_v2.schema.json"
CERTIFICATE_V2_SCHEMA = "dynamic_experiment_world_matrix_certificate_v2.schema.json"
CAUSAL_BINDING_V2_SCHEMA = (
    "dynamic_experiment_causal_producer_binding_v2.schema.json"
)
GOVERNED_CLOCK_EVIDENCE_V2_SCHEMA = (
    "dynamic_experiment_governed_clock_evidence_v2.schema.json"
)
REQUEST_V2_SCHEMA = "dynamic_experiment_world_request_v2.schema.json"
OBSERVATION_ENVELOPE_V2_SCHEMA = (
    "dynamic_experiment_world_observation_envelope_v2.schema.json"
)
COMMISSION_V2_CONTRACT_VERSION = (
    "dynamic-experiment-world-matrix-commission/2.0.0"
)
PROJECTION_V2_CONTRACT_VERSION = "experiment-authority-projection/2.0.0"
REQUEST_V2_CONTRACT_VERSION = "experiment-world-request/2.0.0"
OBSERVATION_V2_CONTRACT_VERSION = "experiment-world-observation/2.0.0"
CERTIFICATE_V2_CONTRACT_VERSION = "experiment-world-certificate/2.0.0"
CAUSAL_BINDING_V2_CONTRACT_VERSION = (
    "experiment-causal-producer-binding/2.0.0"
)
GOVERNED_CLOCK_EVIDENCE_V2_CONTRACT_VERSION = (
    "experiment-governed-clock-evidence/2.0.0"
)
OBSERVATION_ENVELOPE_V2_CONTRACT_VERSION = (
    "experiment-world-observation-envelope/2.0.0"
)
NO_PROBE_DECISION_V2_CONTRACT_VERSION = (
    "experiment-no-probe-decision/2.0.0"
)
MATRIX_SCOPE = (
    "declared_five_world_consistency_matrix_not_an_exhaustive_experiment_universe"
)
FIXED_SPEC_FIELDS = (
    "target_id", "run_id", "branch_id", "state_version", "theory_programme_id",
    "source_theory_programme_digest", "source_reflection_packet_digest",
    "conceptual_system_ids", "theoretical_question_id", "tested_theory_claim",
    "probe_role", "expected_conceptual_change", "triage_digest",
    "preregistration", "controls", "seed_policy", "transfer_boundary",
    "theory_effect_contract", "code_version",
)
PERMITTED_INTERVENTION_FIELDS = ("adapter", "model", "resource_budget")
DERIVED_EXECUTION_FIELDS = (
    "schema_version", "contract_version", "spec_id", "execution_id",
    "precommitted_receipt_id", "experiment_id", "execution_authority",
    "authority_digest", "code_digest", "observed_environment",
    "environment_digest", "created_at", "spec_digest",
)
WORLD_INTERVENTIONS = (
    {"world_id": "no_probe", "execution_disposition": "not_executed", "intervention_kind": "suppress_execution", "expected_statuses": [], "expected_epistemic_outcomes": [], "expected_effect_kinds": [], "pending_review_authorized": False},
    {"world_id": "neutral_inconclusive", "execution_disposition": "executed", "intervention_kind": "bounded_resource_cutoff", "expected_statuses": ["resource_exhausted"], "expected_epistemic_outcomes": ["inconclusive"], "expected_effect_kinds": ["no_theory_effect_inconclusive"], "pending_review_authorized": False},
    {"world_id": "misleading_toy_positive", "execution_disposition": "executed", "intervention_kind": "scoped_positive_fixture", "expected_statuses": ["succeeded"], "expected_epistemic_outcomes": ["supports_within_scope"], "expected_effect_kinds": ["bounded_consistency_signal_only"], "pending_review_authorized": False},
    {"world_id": "registered_premise_falsifier", "execution_disposition": "executed", "intervention_kind": "scoped_counterexample_fixture", "expected_statuses": ["counterexample"], "expected_epistemic_outcomes": ["falsifies_claim"], "expected_effect_kinds": ["registered_premise_revision_requested"], "pending_review_authorized": True},
    {"world_id": "operational_failure", "execution_disposition": "executed", "intervention_kind": "adapter_operational_failure", "expected_statuses": ["capability_unavailable", "deadline_exhausted", "solver_failure", "invalid_spec", "operational_failure"], "expected_epistemic_outcomes": ["not_evaluated"], "expected_effect_kinds": ["no_theory_effect_operational"], "pending_review_authorized": False},
)
WORLD_IDS = tuple(row["world_id"] for row in WORLD_INTERVENTIONS)
EXECUTED_WORLD_IDS = tuple(
    row["world_id"]
    for row in WORLD_INTERVENTIONS
    if row["execution_disposition"] == "executed"
)
_WORLD_BY_ID = {row["world_id"]: row for row in WORLD_INTERVENTIONS}
AUTHORITY_BOUNDARY = {
    "experiment_subordinate_to_theory": True,
    "theory_identity_changed": False,
    "ontology_mutation_authorized": False,
    "theory_selected": False,
    "proof_authorized": False,
    "physical_target_support_authorized": False,
    "automatic_evidence_relation_authorized": False,
    "schedule_mutation_authorized": False,
}
_BINDING_FIELDS = {
    "schema_version", "world_id", "commission_id", "commission_digest",
    "tested_claim_id", "tested_claim_digest", "execution_disposition",
    "spec_binding", "receipt_binding", "reflection_binding",
    "pending_review_status", "authority_boundary", "binding_digest",
}


_DOMAIN_VALIDATION_CACHE: contextvars.ContextVar[
    dict[tuple[Any, ...], tuple[dict[str, Any], dict[str, Any]]] | None
] = contextvars.ContextVar("world_matrix_domain_validation_cache", default=None)


@contextlib.contextmanager
def _world_matrix_validation_cache_context():
    """Share exact semantic-validation results within one causal operation."""

    existing = _DOMAIN_VALIDATION_CACHE.get()
    if existing is not None:
        yield existing
        return
    cache: dict[tuple[Any, ...], tuple[dict[str, Any], dict[str, Any]]] = {}
    token = _DOMAIN_VALIDATION_CACHE.set(cache)
    try:
        yield cache
    finally:
        _DOMAIN_VALIDATION_CACHE.reset(token)


def world_matrix_validation_cache_scope(function):
    """Decorate one complete operation with a re-entrant semantic cache.

    A cache hit is accepted only when the candidate mapping is exactly equal to
    the previously validated mapping under the same typed identity and
    validation expectations.  Thus repeated embedded commission/request/spec
    values are not revalidated, while a forged same-ID substitution still
    fails closed.  The cache is context-local and discarded before a public
    operation returns.
    """

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        with _world_matrix_validation_cache_context():
            return function(*args, **kwargs)

    return wrapped


def _memoized_domain_validation(
    key: tuple[Any, ...], value: Mapping[str, Any]
) -> dict[str, Any] | None:
    cache = _DOMAIN_VALIDATION_CACHE.get()
    if cache is None:
        return None
    entry = cache.get(key)
    if entry is None:
        return None
    original, validated = entry
    if dict(value) != original:
        raise ContractError("world-matrix semantic identity collision")
    return validated


def _remember_domain_validation(
    key: tuple[Any, ...], validated: dict[str, Any]
) -> dict[str, Any]:
    cache = _DOMAIN_VALIDATION_CACHE.get()
    if cache is not None:
        cache[key] = (validated, validated)
    return validated

# The projector is intentionally closed at the component boundary.  A caller
# must provide actual JSON objects for every listed component; a digest-only
# placeholder has no lawful image in this contract.
AUTHORITY_COMPONENT_ORDER = (
    "committed_ancestor",
    "theory_programme",
    "reflection_packet",
    "conceptual_systems",
    "genealogy",
    "source_authority",
    "registered_claim",
    "generator_authority",
    "adjudication_authority",
    "schedule",
)
PROJECTION_SCHEMA_AUTHORITY = {
    "schema_id": (
        "https://abducer.local/spec/"
        "dynamic_experiment_world_matrix_commission_v2.schema.json"
        "#/$defs/authorityProjection"
    ),
    "schema_version": "2.0.0",
    "schema_semantics_digest": canonical_digest(
        {
            "component_order": list(AUTHORITY_COMPONENT_ORDER),
            "values_required": True,
            "digest_only_components_forbidden": True,
            "closed_component_envelope": True,
        }
    ),
}
PROJECTION_COVERAGE_CONTRACT = {
    "coverage_scope": "complete_over_declared_projection_v2_only",
    "declared_component_order": list(AUTHORITY_COMPONENT_ORDER),
    "future_or_unlisted_fields_authorized": False,
    "coverage_digest": canonical_digest(
        {
            "coverage_scope": "complete_over_declared_projection_v2_only",
            "declared_component_order": list(AUTHORITY_COMPONENT_ORDER),
            "future_or_unlisted_fields_authorized": False,
        }
    ),
}
PROJECTION_PROJECTOR_AUTHORITY = {
    "projector_id": "complete-experiment-authority-projector",
    "projector_version": "2.0.0",
    "projector_semantics_digest": canonical_digest(
        {
            "projection": "exact_values_not_summaries",
            "ordering": list(AUTHORITY_COMPONENT_ORDER),
            "comparison": "recursive_json_pointer_equality",
            "omission_policy": "fail_closed",
        }
    ),
}
PERMITTED_INTERVENTION_PATHS = (
    "/experiment_spec/adapter",
    "/experiment_spec/model",
    "/experiment_spec/resource_budget",
)
BASELINE_WORLD_ID = "misleading_toy_positive"
V2_AUTHORITY_STATUS = "authoritative_pre_execution_complete_projection"
LOCAL_PROTOCOL_AUTHORITY_STATUS = (
    "local_protocol_valid_trusted_evidence_unresolved"
)
LEGACY_AUTHORITY_STATUS = "legacy_diagnostic_compatibility_only"
FINAL_ADJUDICATION_STAGE_ID = "final_adjudication"
PRE_EXPERIMENT_SCHEDULE_STAGE_ID = "pre_experiment_schedule"
COMMISSION_STAGE_ID = "world_matrix_commission"
WORLD_REQUEST_STAGE_ID = "world_request"
EXPERIMENT_EXECUTION_STAGE_ID = "experiment_execution"
NO_PROBE_DECISION_STAGE_ID = "no_probe_decision"
POST_RESULT_REFLECTION_STAGE_ID = "post_result_reflection"
WORLD_OBSERVATION_STAGE_ID = "world_observation"
MATRIX_AGGREGATION_STAGE_ID = "matrix_aggregation"

FINAL_ADJUDICATION_PRODUCER_ROLE = "synthesis_conceptual_adjudication"
PRE_EXPERIMENT_SCHEDULE_PRODUCER_ROLE = "discovery_schedule"
COMMISSION_PRODUCER_ROLE = "experiment_world_matrix_commission"
WORLD_REQUEST_PRODUCER_ROLE = "experiment_world_request"
EXPERIMENT_EXECUTION_PRODUCER_ROLE = (
    "dynamic_symbolic_simulation_experiment"
)
NO_PROBE_DECISION_PRODUCER_ROLE = "experiment_no_probe_decision"
POST_RESULT_REFLECTION_PRODUCER_ROLE = "experiment_result_reflection"
WORLD_OBSERVATION_PRODUCER_ROLE = "experiment_world_observation"
MATRIX_AGGREGATION_PRODUCER_ROLE = "experiment_world_matrix_aggregation"


class WorldMatrixFailureReason(str, Enum):
    """Stable machine-readable reasons for fail-closed v2 authority failures."""

    TRUSTED_EVIDENCE_REQUIRED = "trusted_evidence_required"
    EVIDENCE_RESOLVER_INVALID = "evidence_resolver_invalid"
    EVIDENCE_AUTHORITY_UNKNOWN = "evidence_authority_unknown"
    LOCAL_PROTOCOL_INVALID = "local_protocol_invalid"
    COMMITTED_REQUEST_BYTES_CHANGED = "committed_request_bytes_changed"
    COMMITTED_RECEIPT_BYTES_CHANGED = "committed_receipt_bytes_changed"
    COMMITTED_ARTIFACT_BYTES_CHANGED = "committed_artifact_bytes_changed"
    COMMITTED_HISTORY_BYTES_CHANGED = "committed_history_bytes_changed"
    COMMITTED_PATH_BINDING_CHANGED = "committed_path_binding_changed"
    COMMITTED_CLOCK_EVIDENCE_CHANGED = "committed_clock_evidence_changed"
    AUTHORITY_PROJECTION_CHANGED = "authority_projection_changed"
    NO_PROBE_EXECUTION_FORBIDDEN = "no_probe_execution_forbidden"
    WORLD_ENVELOPE_ORDER_INVALID = "world_envelope_order_invalid"
    SEPARATE_WORLD_PRODUCERS_REQUIRED = "separate_world_producers_required"


class WorldMatrixContractError(ContractError):
    """A world-matrix contract failure with a stable typed reason."""

    def __init__(
        self,
        reason: WorldMatrixFailureReason,
        message: str,
    ) -> None:
        self.reason = reason
        super().__init__(f"world_matrix[{reason.value}]: {message}")


@dataclass(frozen=True, slots=True)
class CommittedCausalEvidencePaths:
    """Trusted, immutable locators for one independently committed producer."""

    evidence_authority_id: str
    producer_request_path: Path
    producer_receipt_path: Path
    artifact_path: Path
    immutable_history_path: Path
    governed_clock_path: Path


@dataclass(frozen=True, slots=True)
class TrustedCausalEvidenceResolution:
    """Exact evidence reopened by the concrete resolver for one binding."""

    evidence_authority_id: str
    binding_id: str
    binding_digest: str
    stage_id: str
    producer_role: str
    target_id: str
    run_id: str
    state_version: int
    committed_file_digests: tuple[tuple[str, str], ...]
    governed_clock_evidence_digest: str
    trusted_evidence_resolved: bool = True


@dataclass(frozen=True, slots=True)
class CommittedCausalEvidenceSnapshot:
    """One transaction-verified, path-free evidence authority snapshot.

    This value is intentionally accepted only by the resolver's private
    transaction bridge.  It lets canonical replay validate the bytes returned
    by ``DiscoveryTransactionStore.read_verified_artifacts`` without reopening
    filesystem names after the store has verified them.
    """

    evidence_authority_id: str
    committed_paths: tuple[tuple[str, str], ...]
    committed_files: tuple[tuple[str, bytes], ...]


@dataclass(frozen=True, slots=True)
class _CommittedFileSnapshot:
    path: Path
    sha256: str
    size_bytes: int
    device: int
    inode: int
    modified_ns: int
    link_count: int


@dataclass(frozen=True, slots=True)
class _CommittedAuthorityEvidence:
    paths: CommittedCausalEvidencePaths | None
    snapshots: tuple[tuple[str, _CommittedFileSnapshot], ...]
    committed_paths: tuple[tuple[str, str], ...]
    snapshot_bytes: tuple[tuple[str, bytes], ...]
    governed_clock_value: dict[str, Any]


V2_AUTHORITY_BOUNDARY = {
    **AUTHORITY_BOUNDARY,
    "canonical_experiment_execution_authorized": True,
    "current_cycle_theory_mutation_authorized": False,
    "pending_review_deferred_to_next_cycle": True,
}
LOCAL_PROTOCOL_AUTHORITY_BOUNDARY = {
    **V2_AUTHORITY_BOUNDARY,
    "canonical_experiment_execution_authorized": False,
}
DERIVED_DENIALS = {
    "theory_identity_changed": False,
    "ontology_mutation_authorized": False,
    "theory_selected": False,
    "proof_authorized": False,
    "physical_target_support_authorized": False,
    "automatic_evidence_relation_authorized": False,
    "schedule_mutation_authorized": False,
    "current_cycle_theory_mutation_authorized": False,
    "experiment_led_ontology_authorized": False,
}


def _top_level_digest(value: Mapping[str, Any], field: str) -> str:
    material = copy.deepcopy(dict(value))
    material.pop(field, None)
    return canonical_digest(material)


def _identity_core(value: Mapping[str, Any], *fields: str) -> dict[str, Any]:
    """Copy a record while removing only its root identity/self-digest fields."""

    excluded = set(fields)
    return {
        key: copy.deepcopy(child)
        for key, child in value.items()
        if key not in excluded
    }


def _parse_governed_timestamp(value: Any, label: str) -> dt.datetime:
    """Parse one timezone-aware timestamp used as causal evidence."""

    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{label} is not an ISO date-time") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"{label} must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def _serialized_json_evidence(
    value: Mapping[str, Any], raw_bytes: bytes
) -> dict[str, Any]:
    """Bind an actual JSON value to the exact bytes that crossed a boundary."""

    if not isinstance(raw_bytes, bytes) or not raw_bytes:
        raise ContractError("causal evidence bytes must be nonempty")
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError("causal evidence bytes are not one UTF-8 JSON value") from exc
    copied = copy.deepcopy(dict(value))
    if decoded != copied:
        raise ContractError("causal evidence bytes differ from their actual JSON value")
    return {
        "value": copied,
        "value_digest": canonical_digest(copied),
        "bytes_base64": base64.b64encode(raw_bytes).decode("ascii"),
        "file_sha256": bytes_digest(raw_bytes),
        "byte_length": len(raw_bytes),
    }


def _reopen_serialized_json_evidence(
    evidence: Mapping[str, Any], label: str
) -> dict[str, Any]:
    """Reopen exact evidence bytes instead of trusting caller-written digests."""

    try:
        raw_bytes = base64.b64decode(
            str(evidence["bytes_base64"]), validate=True
        )
    except (KeyError, ValueError) as exc:
        raise ContractError(f"{label} bytes are not valid base64") from exc
    value = evidence.get("value")
    if not isinstance(value, Mapping):
        raise ContractError(f"{label} actual value must be an object")
    if (
        evidence.get("file_sha256") != bytes_digest(raw_bytes)
        or evidence.get("byte_length") != len(raw_bytes)
        or evidence.get("value_digest") != canonical_digest(value)
    ):
        raise ContractError(f"{label} byte or semantic digest is invalid")
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} bytes are not one UTF-8 JSON value") from exc
    if decoded != value:
        raise ContractError(f"{label} bytes differ from their actual value")
    return copy.deepcopy(dict(value))


def _producer_output_descriptors(
    request: Mapping[str, Any],
    receipt: Mapping[str, Any],
    declared_output_path: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the mutable output and its immutable per-attempt byte snapshot."""

    if declared_output_path not in request.get("declared_outputs", []):
        raise ContractError("causal producer request did not declare its artifact path")
    pairs = list(
        zip(
            receipt.get("output_artifacts", []),
            receipt.get("output_history_artifacts", []),
            strict=True,
        )
    )
    matches = [pair for pair in pairs if pair[0].get("path") == declared_output_path]
    if len(matches) != 1:
        raise ContractError("causal producer receipt lacks one exact output/history pair")
    output, history = matches[0]
    if (
        output.get("sha256") != history.get("sha256")
        or output.get("size_bytes") != history.get("size_bytes")
        or output.get("namespace") != history.get("namespace")
    ):
        raise ContractError("causal producer output/history bytes are not identical")
    return copy.deepcopy(dict(output)), copy.deepcopy(dict(history))


_COMMITTED_CONTENT_REASONS = {
    "producer_request": WorldMatrixFailureReason.COMMITTED_REQUEST_BYTES_CHANGED,
    "producer_receipt": WorldMatrixFailureReason.COMMITTED_RECEIPT_BYTES_CHANGED,
    "artifact": WorldMatrixFailureReason.COMMITTED_ARTIFACT_BYTES_CHANGED,
    "immutable_history": WorldMatrixFailureReason.COMMITTED_HISTORY_BYTES_CHANGED,
    "governed_clock": WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
}


def _canonical_committed_path(
    value: Path,
    label: str,
    *,
    must_exist: bool,
) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            f"{label} must be an absolute committed path",
        )
    try:
        resolved = path.resolve(strict=must_exist)
    except OSError as exc:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            f"{label} cannot be resolved",
        ) from exc
    if resolved != path:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            f"{label} contains a path or symlink substitution",
        )
    return path


def _normalize_committed_evidence_paths(
    supplied: CommittedCausalEvidencePaths,
    *,
    clock_must_exist: bool,
) -> CommittedCausalEvidencePaths:
    if type(supplied) is not CommittedCausalEvidencePaths:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
            "resolver records must be concrete CommittedCausalEvidencePaths",
        )
    validate_identifier(supplied.evidence_authority_id, "evidence_authority_id")
    names = (
        "producer_request_path",
        "producer_receipt_path",
        "artifact_path",
        "immutable_history_path",
        "governed_clock_path",
    )
    normalized: dict[str, Path] = {}
    for name in names:
        normalized[name] = _canonical_committed_path(
            getattr(supplied, name),
            name,
            must_exist=clock_must_exist or name != "governed_clock_path",
        )
    if len(set(normalized.values())) != len(normalized):
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            "request, receipt, artifact, history, and clock need distinct paths",
        )
    return CommittedCausalEvidencePaths(
        evidence_authority_id=supplied.evidence_authority_id,
        **normalized,
    )


def _snapshot_committed_file(
    path: Path,
    *,
    content_reason: WorldMatrixFailureReason,
) -> tuple[_CommittedFileSnapshot, bytes]:
    """Read one source through a single no-follow descriptor snapshot.

    Name-based ``lstat`` followed by ``Path.read_bytes`` leaves a substitution
    window.  Opening with ``O_NOFOLLOW`` and checking the same descriptor
    before and after the read makes the copied bytes the object that was
    actually validated.  Multiple hard links are rejected because a second
    writable name would defeat the intended immutable-source boundary.
    """

    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = -1
    try:
        descriptor = os.open(path, flags)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise OSError("committed evidence is not one singly linked regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
    except OSError as exc:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            f"committed evidence path is unavailable: {path}",
        ) from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_mode,
        before.st_nlink,
        before.st_size,
        before.st_mtime_ns,
        before.st_ctime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    )
    named_identity = (
        named_after.st_dev,
        named_after.st_ino,
        named_after.st_mode,
        named_after.st_nlink,
        named_after.st_size,
        named_after.st_mtime_ns,
        named_after.st_ctime_ns,
    )
    if identity_before != identity_after or identity_after != named_identity:
        raise WorldMatrixContractError(
            content_reason,
            f"committed evidence changed while being read: {path}",
        )
    return (
        _CommittedFileSnapshot(
            path=path,
            sha256=bytes_digest(raw),
            size_bytes=len(raw),
            device=after.st_dev,
            inode=after.st_ino,
            modified_ns=after.st_mtime_ns,
            link_count=after.st_nlink,
        ),
        raw,
    )


def _reopen_committed_file(
    snapshot: _CommittedFileSnapshot,
    *,
    content_reason: WorldMatrixFailureReason,
) -> bytes:
    path = _canonical_committed_path(
        snapshot.path,
        "committed evidence",
        must_exist=True,
    )
    current, raw = _snapshot_committed_file(path, content_reason=content_reason)
    if (current.device, current.inode) != (snapshot.device, snapshot.inode):
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
            f"committed evidence file identity changed: {path}",
        )
    if (
        current.sha256 != snapshot.sha256
        or current.size_bytes != snapshot.size_bytes
        or current.modified_ns != snapshot.modified_ns
        or current.link_count != snapshot.link_count
    ):
        raise WorldMatrixContractError(
            content_reason,
            f"committed evidence bytes changed: {path}",
        )
    return raw


def _parse_governed_clock_evidence(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, Mapping):
            raise TypeError("clock evidence must be an object")
        record = copy.deepcopy(dict(value))
        validate_payload(record, GOVERNED_CLOCK_EVIDENCE_V2_SCHEMA)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ContractError) as exc:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
            "governed clock evidence is invalid",
        ) from exc
    if record["clock_evidence_digest"] != _top_level_digest(
        record, "clock_evidence_digest"
    ):
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
            "governed clock evidence digest changed",
        )
    committed_derivation = record.get("committed_derivation")
    if committed_derivation is not None and committed_derivation[
        "derivation_digest"
    ] != _top_level_digest(committed_derivation, "derivation_digest"):
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
            "committed governed clock derivation digest changed",
        )
    return record


class CommittedCausalEvidenceResolver:
    """Resolve one immutable evidence snapshot for every producer binding.

    Path-backed construction first records source identity.  The first
    successful ``resolve`` reopens through a no-follow descriptor, validates
    those exact bytes, and caches them.  All later consumers—including the CAS
    preparation path—reuse that validated byte snapshot instead of rereading a
    mutable pathname.  Canonical replay uses the private transaction bridge and
    starts directly from one store-verified in-memory batch.
    """

    def __init__(
        self,
        records: Sequence[CommittedCausalEvidencePaths],
        *,
        portable_root: Path | None = None,
        portable_roots: Mapping[str, Path] | None = None,
    ) -> None:
        if not records or isinstance(records, (str, bytes, bytearray)):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                "resolver requires at least one committed evidence record",
            )
        if portable_root is not None and portable_roots is not None:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                "portable evidence accepts one shared root or authority roots, not both",
            )
        resolved_portable_root: Path | None = None
        if portable_root is not None:
            try:
                resolved_portable_root = Path(portable_root).resolve(strict=True)
            except OSError as exc:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    "portable evidence root is unavailable",
                ) from exc
            if not resolved_portable_root.is_dir():
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    "portable evidence root must be a committed directory",
                )
        resolved_portable_roots: dict[str, Path] = {}
        if portable_roots is not None:
            for authority_id, root in portable_roots.items():
                validate_identifier(authority_id, "evidence_authority_id")
                try:
                    resolved = Path(root).resolve(strict=True)
                except OSError as exc:
                    raise WorldMatrixContractError(
                        WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                        "portable authority evidence root is unavailable",
                    ) from exc
                if not resolved.is_dir():
                    raise WorldMatrixContractError(
                        WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                        "portable authority evidence root must be a committed directory",
                    )
                resolved_portable_roots[authority_id] = resolved
        authorities: dict[str, _CommittedAuthorityEvidence] = {}
        all_paths: set[Path] = set()
        for supplied in records:
            paths = _normalize_committed_evidence_paths(
                supplied, clock_must_exist=True
            )
            if paths.evidence_authority_id in authorities:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                    "duplicate evidence authority identity",
                )
            path_rows = {
                "producer_request": paths.producer_request_path,
                "producer_receipt": paths.producer_receipt_path,
                "artifact": paths.artifact_path,
                "immutable_history": paths.immutable_history_path,
                "governed_clock": paths.governed_clock_path,
            }
            if all_paths.intersection(path_rows.values()):
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    "committed evidence paths were reused across authorities",
                )
            all_paths.update(path_rows.values())
            snapshots: list[tuple[str, _CommittedFileSnapshot]] = []
            raw_by_kind: dict[str, bytes] = {}
            for kind, path in path_rows.items():
                snapshot, raw = _snapshot_committed_file(
                    path, content_reason=_COMMITTED_CONTENT_REASONS[kind]
                )
                snapshots.append((kind, snapshot))
                raw_by_kind[kind] = raw
            clock = _parse_governed_clock_evidence(raw_by_kind["governed_clock"])
            authority_root = (
                resolved_portable_root
                if resolved_portable_root is not None
                else resolved_portable_roots.get(paths.evidence_authority_id)
            )
            if authority_root is None:
                expected_paths = {
                    kind: str(path) for kind, path in path_rows.items()
                }
            else:
                expected_paths = {}
                for kind, path in path_rows.items():
                    try:
                        relative = path.relative_to(authority_root)
                    except ValueError as exc:
                        raise WorldMatrixContractError(
                            WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                            "portable evidence escaped its committed root",
                        ) from exc
                    expected_paths[kind] = safe_relative_path(
                        relative.as_posix()
                    ).as_posix()
            if (
                clock["evidence_authority_id"] != paths.evidence_authority_id
                or clock["committed_paths"] != expected_paths
            ):
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    "governed clock authority or committed path table changed",
                )
            authorities[paths.evidence_authority_id] = _CommittedAuthorityEvidence(
                paths=paths,
                snapshots=tuple(snapshots),
                committed_paths=tuple(
                    (kind, expected_paths[kind])
                    for kind in _COMMITTED_CONTENT_REASONS
                ),
                snapshot_bytes=tuple(
                    (kind, raw_by_kind[kind])
                    for kind in _COMMITTED_CONTENT_REASONS
                ),
                governed_clock_value=clock,
            )
        if resolved_portable_roots and set(resolved_portable_roots) != set(authorities):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                "portable authority root coverage differs from evidence authorities",
            )
        self._authorities = authorities
        self._validated_snapshots: dict[
            tuple[str, str],
            tuple[TrustedCausalEvidenceResolution, tuple[tuple[str, bytes], ...]],
        ] = {}

    @classmethod
    def _from_verified_artifact_snapshots(
        cls,
        snapshots: Sequence[CommittedCausalEvidenceSnapshot],
    ) -> "CommittedCausalEvidenceResolver":
        """Bridge an exact transaction batch into the normal validator.

        Callers must obtain every supplied byte from one
        ``read_verified_artifacts`` result.  The bridge performs shape, path,
        clock, authority, and uniqueness checks but deliberately has no path
        fallback: replay cannot silently reopen a name after verification.
        """

        if not snapshots or isinstance(snapshots, (str, bytes, bytearray)):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                "verified replay requires at least one evidence snapshot",
            )
        authorities: dict[str, _CommittedAuthorityEvidence] = {}
        all_paths: set[str] = set()
        expected_kinds = tuple(_COMMITTED_CONTENT_REASONS)
        for supplied in snapshots:
            if type(supplied) is not CommittedCausalEvidenceSnapshot:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                    "verified replay evidence must use the typed snapshot boundary",
                )
            authority_id = validate_identifier(
                supplied.evidence_authority_id, "evidence_authority_id"
            )
            if authority_id in authorities:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                    "duplicate verified evidence authority identity",
                )
            try:
                paths = dict(supplied.committed_paths)
                files = dict(supplied.committed_files)
            except (TypeError, ValueError) as exc:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                    "verified evidence rows are malformed",
                ) from exc
            if (
                len(paths) != len(supplied.committed_paths)
                or len(files) != len(supplied.committed_files)
                or tuple(kind for kind, _ in supplied.committed_paths)
                != expected_kinds
                or tuple(kind for kind, _ in supplied.committed_files)
                != expected_kinds
                or set(paths) != set(expected_kinds)
                or set(files) != set(expected_kinds)
            ):
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                    "verified evidence must cover each exact evidence kind once",
                )
            normalized_paths: dict[str, str] = {}
            for kind in expected_kinds:
                path = paths[kind]
                if not isinstance(path, str):
                    raise WorldMatrixContractError(
                        WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                        "verified evidence path is not text",
                    )
                normalized = safe_relative_path(path).as_posix()
                if normalized != path or normalized in all_paths:
                    raise WorldMatrixContractError(
                        WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                        "verified evidence path is unsafe or reused",
                    )
                raw = files[kind]
                if not isinstance(raw, bytes) or not raw:
                    raise WorldMatrixContractError(
                        _COMMITTED_CONTENT_REASONS[kind],
                        "verified evidence bytes are empty or not immutable bytes",
                    )
                normalized_paths[kind] = normalized
                all_paths.add(normalized)
            clock = _parse_governed_clock_evidence(files["governed_clock"])
            if "committed_derivation" not in clock:
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
                    "transaction-replayed clock lacks a committed derivation",
                )
            if (
                clock["evidence_authority_id"] != authority_id
                or clock["committed_paths"] != normalized_paths
            ):
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    "verified clock authority or committed path table changed",
                )
            authorities[authority_id] = _CommittedAuthorityEvidence(
                paths=None,
                snapshots=(),
                committed_paths=tuple(
                    (kind, normalized_paths[kind]) for kind in expected_kinds
                ),
                snapshot_bytes=tuple(
                    (kind, files[kind]) for kind in expected_kinds
                ),
                governed_clock_value=clock,
            )
        resolver = cls.__new__(cls)
        resolver._authorities = authorities
        resolver._validated_snapshots = {}
        return resolver

    def resolve(
        self,
        binding: Mapping[str, Any],
    ) -> TrustedCausalEvidenceResolution:
        """Independently reopen all five committed files for one local binding."""

        record = copy.deepcopy(dict(binding))
        authority_id = record.get("evidence_authority_id")
        authority = self._authorities.get(authority_id)
        if authority is None:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_AUTHORITY_UNKNOWN,
                "binding has no record in the trusted evidence resolver",
            )
        if record.get("local_protocol_valid") is not True:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.LOCAL_PROTOCOL_INVALID,
                "binding did not pass the local causal protocol",
            )
        cache_key = (str(authority_id), canonical_digest(record))
        cached = self._validated_snapshots.get(cache_key)
        if cached is not None:
            return cached[0]
        if authority.paths is None:
            reopened = dict(authority.snapshot_bytes)
        else:
            reopened: dict[str, bytes] = {}
            for kind, snapshot in authority.snapshots:
                reopened[kind] = _reopen_committed_file(
                    snapshot, content_reason=_COMMITTED_CONTENT_REASONS[kind]
                )
        clock = _parse_governed_clock_evidence(reopened["governed_clock"])
        if clock != authority.governed_clock_value:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
                "governed clock evidence differs from its trusted snapshot",
            )
        evidence_bytes = {
            "producer_request": base64.b64decode(
                record["producer_request"]["bytes_base64"], validate=True
            ),
            "producer_receipt": base64.b64decode(
                record["producer_receipt"]["bytes_base64"], validate=True
            ),
            "artifact": base64.b64decode(
                record["artifact_evidence"]["bytes_base64"], validate=True
            ),
        }
        for kind, expected in evidence_bytes.items():
            if reopened[kind] != expected:
                raise WorldMatrixContractError(
                    _COMMITTED_CONTENT_REASONS[kind],
                    f"{kind} differs from independently committed bytes",
                )
        if reopened["immutable_history"] != evidence_bytes["artifact"]:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.COMMITTED_HISTORY_BYTES_CHANGED,
                "immutable history differs from the sealed artifact bytes",
            )
        request = record["producer_request"]["value"]
        evidence = record["artifact_evidence"]
        expected_clock = {
            "evidence_authority_id": authority_id,
            "binding_id": record["binding_id"],
            "binding_digest": record["binding_digest"],
            "stage_id": record["stage_id"],
            "producer_role": record["producer_role"],
            "target_id": record["target_id"],
            "run_id": record["run_id"],
            "state_version": record["state_version"],
            "declared_output_path": evidence["declared_output_path"],
            "immutable_history_path": evidence["immutable_history_path"],
            "governed_timestamps": record["governed_timestamps"],
        }
        if any(clock.get(key) != value for key, value in expected_clock.items()):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.COMMITTED_CLOCK_EVIDENCE_CHANGED,
                "clock authority does not bind the exact producer transcript",
            )
        if request.get("parameters", {}).get("evidence_authority_id") != authority_id:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_AUTHORITY_UNKNOWN,
                "producer request did not predeclare its evidence authority",
            )
        logical_paths = {
            "artifact": evidence["declared_output_path"],
            "immutable_history": evidence["immutable_history_path"],
        }
        authority_paths = dict(authority.committed_paths)
        committed_paths = {
            "artifact": Path(authority_paths["artifact"]),
            "immutable_history": Path(authority_paths["immutable_history"]),
        }
        for kind, logical_text in logical_paths.items():
            logical = Path(logical_text)
            if (
                logical.is_absolute()
                or not logical.parts
                or any(part in {"", ".", ".."} for part in logical.parts)
                or committed_paths[kind].parts[-len(logical.parts) :]
                != logical.parts
            ):
                raise WorldMatrixContractError(
                    WorldMatrixFailureReason.COMMITTED_PATH_BINDING_CHANGED,
                    f"sealed {kind} path does not preserve its declared suffix",
                )
        resolution = TrustedCausalEvidenceResolution(
            evidence_authority_id=authority_id,
            binding_id=record["binding_id"],
            binding_digest=record["binding_digest"],
            stage_id=record["stage_id"],
            producer_role=record["producer_role"],
            target_id=record["target_id"],
            run_id=record["run_id"],
            state_version=record["state_version"],
            committed_file_digests=tuple(
                (kind, bytes_digest(reopened[kind]))
                for kind in (
                    "producer_request",
                    "producer_receipt",
                    "artifact",
                    "immutable_history",
                    "governed_clock",
                )
            ),
            governed_clock_evidence_digest=clock["clock_evidence_digest"],
        )
        self._validated_snapshots[cache_key] = (
            resolution,
            tuple(
                (kind, reopened[kind]) for kind in _COMMITTED_CONTENT_REASONS
            ),
        )
        return resolution

    def validated_file_snapshot(
        self,
        binding: Mapping[str, Any],
    ) -> tuple[TrustedCausalEvidenceResolution, dict[str, bytes]]:
        """Return the exact bytes already validated for ``binding``.

        ``resolve`` populates the immutable cache on first use.  This accessor
        never reopens a pathname, which is the essential guarantee needed by
        commit preparation after semantic validation has completed.
        """

        record = copy.deepcopy(dict(binding))
        resolution = self.resolve(record)
        cache_key = (
            resolution.evidence_authority_id,
            canonical_digest(record),
        )
        cached = self._validated_snapshots.get(cache_key)
        if cached is None or cached[0] != resolution:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
                "validated evidence snapshot cache is unavailable",
            )
        return resolution, dict(cached[1])


def _require_trusted_evidence_resolver(
    evidence_resolver: CommittedCausalEvidenceResolver | None,
) -> CommittedCausalEvidenceResolver:
    if evidence_resolver is None:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.TRUSTED_EVIDENCE_REQUIRED,
            "canonical authority requires committed evidence resolution",
        )
    if type(evidence_resolver) is not CommittedCausalEvidenceResolver:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.EVIDENCE_RESOLVER_INVALID,
            "canonical authority rejects callbacks, subclasses, and no-op hooks",
        )
    return evidence_resolver


def build_governed_clock_evidence(
    binding: Mapping[str, Any],
    *,
    evidence_paths: CommittedCausalEvidencePaths,
) -> dict[str, Any]:
    """Build the separately committed clock/path witness for one local binding."""

    record = copy.deepcopy(dict(binding))
    paths = _normalize_committed_evidence_paths(
        evidence_paths, clock_must_exist=False
    )
    if record.get("evidence_authority_id") != paths.evidence_authority_id:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.EVIDENCE_AUTHORITY_UNKNOWN,
            "clock evidence authority differs from the causal binding",
        )
    committed_paths = {
        "producer_request": str(paths.producer_request_path),
        "producer_receipt": str(paths.producer_receipt_path),
        "artifact": str(paths.artifact_path),
        "immutable_history": str(paths.immutable_history_path),
        "governed_clock": str(paths.governed_clock_path),
    }
    clock: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": GOVERNED_CLOCK_EVIDENCE_V2_CONTRACT_VERSION,
        "evidence_authority_id": paths.evidence_authority_id,
        "binding_id": record["binding_id"],
        "binding_digest": record["binding_digest"],
        "stage_id": record["stage_id"],
        "producer_role": record["producer_role"],
        "target_id": record["target_id"],
        "run_id": record["run_id"],
        "state_version": record["state_version"],
        "declared_output_path": record["artifact_evidence"]["declared_output_path"],
        "immutable_history_path": record["artifact_evidence"][
            "immutable_history_path"
        ],
        "committed_paths": committed_paths,
        "governed_timestamps": copy.deepcopy(record["governed_timestamps"]),
    }
    clock["clock_evidence_digest"] = _top_level_digest(
        clock, "clock_evidence_digest"
    )
    validate_payload(clock, GOVERNED_CLOCK_EVIDENCE_V2_SCHEMA)
    return clock


def build_experiment_causal_producer_binding(
    *,
    stage_id: str,
    producer_role: str,
    artifact_id: str,
    artifact_value: Mapping[str, Any],
    artifact_bytes: bytes,
    producer_request: Mapping[str, Any],
    producer_request_bytes: bytes,
    producer_receipt: Mapping[str, Any],
    producer_receipt_bytes: bytes,
    declared_output_path: str,
    sealed_at: str,
    clock_authority_id: str,
    evidence_authority_id: str,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Bind one actual producer invocation to one immutable JSON artifact.

    The binding is deliberately external to the artifact it certifies.  It
    carries the complete operator request and receipt, the exact immutable
    output-history bytes, and a governed sealing instant.  Canonical consumers
    Local validation proves protocol consistency only.  Canonical consumers
    additionally supply the concrete committed-evidence resolver after the
    request, receipt, artifact, history, and clock files have been sealed.
    """

    request = copy.deepcopy(dict(producer_request))
    receipt = copy.deepcopy(dict(producer_receipt))
    artifact = copy.deepcopy(dict(artifact_value))
    validate_operator_request_identity(request)
    validate_operator_receipt_identity(receipt, request)
    if receipt.get("status") != "succeeded":
        raise ContractError("causal producer must have a succeeded receipt")
    identity = request["identity"]
    parameters = request.get("parameters", {})
    validate_identifier(evidence_authority_id, "evidence_authority_id")
    artifact_digest = canonical_digest(artifact)
    if (
        parameters.get("causal_stage_id") != stage_id
        or parameters.get("producer_role") != producer_role
        or parameters.get("artifact_id") != artifact_id
        or parameters.get("artifact_digest") != artifact_digest
        or parameters.get("evidence_authority_id") != evidence_authority_id
    ):
        raise ContractError("producer request did not predeclare exact role/stage/artifact")
    output, history = _producer_output_descriptors(
        request, receipt, declared_output_path
    )
    if (
        history["sha256"] != bytes_digest(artifact_bytes)
        or history["size_bytes"] != len(artifact_bytes)
    ):
        raise ContractError("actual artifact bytes differ from immutable receipt history")
    requested_at = str(request["requested_at"])
    started_at = str(receipt["started_at"])
    completed_at = str(receipt["completed_at"])
    if not (
        _parse_governed_timestamp(requested_at, "producer request time")
        <= _parse_governed_timestamp(started_at, "producer start time")
        <= _parse_governed_timestamp(completed_at, "producer completion time")
        <= _parse_governed_timestamp(sealed_at, "artifact seal time")
    ):
        raise ContractError("producer request/receipt/seal timestamps are out of order")
    governed_core = {
        "clock_authority_id": clock_authority_id,
        "requested_at": requested_at,
        "started_at": started_at,
        "completed_at": completed_at,
        "sealed_at": sealed_at,
    }
    binding: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": CAUSAL_BINDING_V2_CONTRACT_VERSION,
        "local_protocol_valid": True,
        "evidence_authority_id": evidence_authority_id,
        "stage_id": stage_id,
        "producer_role": producer_role,
        "target_id": identity["target_id"],
        "run_id": identity["run_id"],
        "state_version": identity["state_version"],
        "producer_request": _serialized_json_evidence(
            request, producer_request_bytes
        ),
        "producer_receipt": _serialized_json_evidence(
            receipt, producer_receipt_bytes
        ),
        "artifact_evidence": {
            **_serialized_json_evidence(artifact, artifact_bytes),
            "artifact_id": artifact_id,
            "declared_output_path": declared_output_path,
            "immutable_history_path": history["path"],
            "output_descriptor": output,
            "history_descriptor": history,
        },
        "governed_timestamps": {
            **governed_core,
            "clock_authority_digest": canonical_digest(governed_core),
        },
    }
    binding["binding_id"] = stable_identifier(
        "experiment-causal-producer-binding-v2", canonical_digest(binding)
    )
    binding["binding_digest"] = _top_level_digest(binding, "binding_digest")
    return validate_experiment_causal_producer_binding(
        binding,
        expected_stage_id=stage_id,
        expected_producer_role=producer_role,
        expected_artifact=artifact,
        expected_artifact_id=artifact_id,
        evidence_resolver=evidence_resolver,
    )


def validate_experiment_causal_producer_binding(
    binding: Mapping[str, Any],
    *,
    expected_stage_id: str | None = None,
    expected_producer_role: str | None = None,
    expected_artifact: Mapping[str, Any] | None = None,
    expected_artifact_id: str | None = None,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Validate locally, then optionally reopen independent committed evidence."""

    memo_key = (
        "causal_producer_binding",
        binding.get("binding_id"),
        binding.get("binding_digest"),
        expected_stage_id,
        expected_producer_role,
        expected_artifact_id,
        evidence_resolver is not None,
    )
    cached = _memoized_domain_validation(memo_key, binding)
    if cached is not None:
        if (
            expected_artifact is not None
            and cached["artifact_evidence"]["value"] != dict(expected_artifact)
        ):
            raise ContractError("causal producer binding names different artifact bytes")
        return cached
    record = copy.deepcopy(dict(binding))
    validate_payload(record, CAUSAL_BINDING_V2_SCHEMA)
    request = _reopen_serialized_json_evidence(
        record["producer_request"], "producer request"
    )
    receipt = _reopen_serialized_json_evidence(
        record["producer_receipt"], "producer receipt"
    )
    artifact = _reopen_serialized_json_evidence(
        record["artifact_evidence"], "producer artifact"
    )
    validate_operator_request_identity(request)
    validate_operator_receipt_identity(receipt, request)
    if receipt.get("status") != "succeeded":
        raise ContractError("causal producer receipt is not successful")
    identity = request["identity"]
    parameters = request.get("parameters", {})
    evidence = record["artifact_evidence"]
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != CAUSAL_BINDING_V2_CONTRACT_VERSION
        or record["local_protocol_valid"] is not True
        or record["target_id"] != identity["target_id"]
        or record["run_id"] != identity["run_id"]
        or record["state_version"] != identity["state_version"]
        or parameters.get("causal_stage_id") != record["stage_id"]
        or parameters.get("producer_role") != record["producer_role"]
        or parameters.get("artifact_id") != evidence["artifact_id"]
        or parameters.get("artifact_digest") != canonical_digest(artifact)
        or parameters.get("evidence_authority_id")
        != record["evidence_authority_id"]
    ):
        raise ContractError("causal producer identity/role/artifact request drift")
    output, history = _producer_output_descriptors(
        request, receipt, evidence["declared_output_path"]
    )
    raw_artifact = base64.b64decode(evidence["bytes_base64"], validate=True)
    if (
        output != evidence["output_descriptor"]
        or history != evidence["history_descriptor"]
        or history["path"] != evidence["immutable_history_path"]
        or history["sha256"] != bytes_digest(raw_artifact)
        or history["size_bytes"] != len(raw_artifact)
    ):
        raise ContractError("causal producer immutable artifact history drift")
    governed = record["governed_timestamps"]
    governed_core = {
        key: governed[key]
        for key in (
            "clock_authority_id",
            "requested_at",
            "started_at",
            "completed_at",
            "sealed_at",
        )
    }
    if (
        governed["requested_at"] != request["requested_at"]
        or governed["started_at"] != receipt["started_at"]
        or governed["completed_at"] != receipt["completed_at"]
        or governed["clock_authority_digest"] != canonical_digest(governed_core)
        or not (
            _parse_governed_timestamp(governed["requested_at"], "request time")
            <= _parse_governed_timestamp(governed["started_at"], "start time")
            <= _parse_governed_timestamp(governed["completed_at"], "completion time")
            <= _parse_governed_timestamp(governed["sealed_at"], "seal time")
        )
    ):
        raise ContractError("causal producer governed timestamps are invalid")
    if expected_stage_id is not None and record["stage_id"] != expected_stage_id:
        raise ContractError("causal producer binding belongs to the wrong stage")
    if (
        expected_producer_role is not None
        and record["producer_role"] != expected_producer_role
    ):
        raise ContractError("causal producer binding belongs to the wrong role")
    if expected_artifact is not None and artifact != dict(expected_artifact):
        raise ContractError("causal producer binding names different artifact bytes")
    if expected_artifact_id is not None and evidence["artifact_id"] != expected_artifact_id:
        raise ContractError("causal producer binding names a different artifact identity")
    expected_id = stable_identifier(
        "experiment-causal-producer-binding-v2",
        canonical_digest(_identity_core(record, "binding_id", "binding_digest")),
    )
    if (
        record["binding_id"] != expected_id
        or record["binding_digest"] != _top_level_digest(record, "binding_digest")
    ):
        raise ContractError("causal producer binding identity is invalid")
    if evidence_resolver is not None:
        _require_trusted_evidence_resolver(evidence_resolver).resolve(record)
    return _remember_domain_validation(memo_key, record)


def _require_causal_precedence(
    earlier: Mapping[str, Any], later: Mapping[str, Any], label: str
) -> None:
    """Require a sealed upstream artifact before the next producer request."""

    earlier_sealed = _parse_governed_timestamp(
        earlier["governed_timestamps"]["sealed_at"], f"{label} upstream seal"
    )
    later_requested = _parse_governed_timestamp(
        later["governed_timestamps"]["requested_at"], f"{label} downstream request"
    )
    if earlier_sealed > later_requested:
        raise ContractError(f"{label} producer causality is timestamp-inverted")


def validate_experiment_authority_projection_coverage(
    commission_schema: Mapping[str, Any],
) -> dict[str, Any]:
    """Fail when code and schema disagree about the declared v2 authority surface."""

    try:
        projection = commission_schema["$defs"]["authorityProjection"]
        properties = projection["properties"]
        schema_order = properties["component_order"]["const"]
        schema_kinds = properties["components"]["items"]["properties"][
            "component_kind"
        ]["enum"]
        minimum = properties["components"]["minItems"]
        maximum = properties["components"]["maxItems"]
    except (KeyError, TypeError) as exc:
        raise ContractError("v2 authority projection schema lacks coverage metadata") from exc
    expected = list(AUTHORITY_COMPONENT_ORDER)
    if (
        schema_order != expected
        or schema_kinds != expected
        or minimum != len(expected)
        or maximum != len(expected)
        or "coverage_contract" not in projection.get("required", [])
    ):
        raise ContractError("v2 authority projection code/schema coverage drift")
    return copy.deepcopy(PROJECTION_COVERAGE_CONTRACT)


def _json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _json_pointer_changes(
    expected: Any,
    observed: Any,
    *,
    path: str = "",
) -> list[str]:
    """Return exact leaf JSON-pointer changes, including omissions and extras."""

    if isinstance(expected, Mapping) and isinstance(observed, Mapping):
        paths: list[str] = []
        keys = sorted(set(expected) | set(observed))
        for key in keys:
            child_path = f"{path}/{_json_pointer_token(str(key))}"
            if key not in expected or key not in observed:
                paths.append(child_path)
                continue
            paths.extend(
                _json_pointer_changes(
                    expected[key], observed[key], path=child_path
                )
            )
        return paths
    if (
        isinstance(expected, Sequence)
        and not isinstance(expected, (str, bytes, bytearray))
        and isinstance(observed, Sequence)
        and not isinstance(observed, (str, bytes, bytearray))
    ):
        paths = []
        length = max(len(expected), len(observed))
        for index in range(length):
            child_path = f"{path}/{index}"
            if index >= len(expected) or index >= len(observed):
                paths.append(child_path)
                continue
            paths.extend(
                _json_pointer_changes(
                    expected[index], observed[index], path=child_path
                )
            )
        return paths
    return [] if expected == observed else [path or "/"]


def _path_is_permitted(path: str) -> bool:
    return any(
        path == root or path.startswith(root + "/")
        for root in PERMITTED_INTERVENTION_PATHS
    )


def _projection_components(
    projection: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        row["component_kind"]: row
        for row in projection["components"]
    }


def _registered_claim(projection: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(
        _projection_components(projection)["registered_claim"]["value"]
    )


def _reflection_packet_identity_digest(
    projection: Mapping[str, Any],
) -> str:
    """Resolve the reflection's domain identity, not its projection envelope.

    Canonical reflective packets carry a conventional self-digest that excludes
    only ``packet_digest``.  The authority projection separately hashes the
    complete value, including that self-digest.  Those two identities have
    different jobs: a registered claim must bind the former.  Small generic v2
    fixtures predating canonical packets remain compatible by using the full
    component digest only when no domain self-digest is present.
    """

    component = _projection_components(projection)["reflection_packet"]
    reflection = component["value"]
    packet_digest = reflection.get("packet_digest")
    if packet_digest is None:
        return str(component["value_digest"])
    if (
        not isinstance(packet_digest, str)
        or not packet_digest
        or packet_digest
        != canonical_digest(reflection, exclude_keys=("packet_digest",))
    ):
        raise ContractError(
            "experiment authority reflection packet self-digest is invalid"
        )
    return packet_digest


def _world_plan(
    commission: Mapping[str, Any], world_id: str
) -> dict[str, Any]:
    for plan in commission["world_plans"]:
        if plan["world_id"] == world_id:
            return plan
    raise ContractError(f"v2 commission lacks world plan {world_id!r}")


def _fixed_spec_semantics(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Project exactly the spec fields that interventions may not change."""

    return {field: copy.deepcopy(spec[field]) for field in FIXED_SPEC_FIELDS}


def _family_identity_core(family: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in family.items()
        if key not in {"family_id", "family_digest"}
    }


def _commission_identity_core(commission: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in commission.items()
        if key not in {"commission_id", "commission_digest"}
    }


def build_experiment_world_matrix_commission(
    reference_spec: Mapping[str, Any],
    *,
    committed_ancestor_byte_digest: str,
    generator_projection_digest: str,
    schedule_projection_digest: str,
) -> dict[str, Any]:
    """Freeze one registered-premise spec family before any world executes."""

    spec = validate_experiment_spec(reference_spec)
    claim = spec["tested_theory_claim"]
    effect = spec["theory_effect_contract"]
    if (
        spec["probe_role"] != "falsifier"
        or claim["claim_kind"] != "theory_premise"
        or effect["tested_claim_kind"] != "theory_premise"
        or effect["if_supported"] != "record_scoped_consistency_only"
        or effect["if_falsified"] != "request_registered_premise_revision"
    ):
        raise ContractError(
            "five-world commission requires one registered-premise falsifier contract"
        )
    fixed = _fixed_spec_semantics(spec)
    family: dict[str, Any] = {
        "fixed_spec_fields": list(FIXED_SPEC_FIELDS),
        "fixed_spec_semantics": fixed,
        "fixed_semantic_core_digest": canonical_digest(fixed),
        "permitted_intervention_fields": list(PERMITTED_INTERVENTION_FIELDS),
        "derived_execution_fields": list(DERIVED_EXECUTION_FIELDS),
    }
    family["family_id"] = stable_identifier(
        "experiment-spec-family", canonical_digest(_family_identity_core(family))
    )
    family["family_digest"] = _top_level_digest(family, "family_digest")
    commission: dict[str, Any] = {
        "schema_version": "1.0.0",
        "contract_version": COMMISSION_CONTRACT_VERSION,
        "matrix_scope": MATRIX_SCOPE,
        "target_id": spec["target_id"],
        "run_id": spec["run_id"],
        "prior_state_version": spec["state_version"],
        "theory_programme_binding": {
            "theory_programme_id": spec["theory_programme_id"],
            "source_theory_programme_digest": spec[
                "source_theory_programme_digest"
            ],
            "source_reflection_packet_digest": spec[
                "source_reflection_packet_digest"
            ],
            "conceptual_system_ids": list(spec["conceptual_system_ids"]),
        },
        "spec_family": family,
        "world_interventions": copy.deepcopy(list(WORLD_INTERVENTIONS)),
        "generation_binding": {
            "committed_ancestor_byte_digest": committed_ancestor_byte_digest,
            "generator_projection_digest": generator_projection_digest,
            "schedule_projection_digest": schedule_projection_digest,
        },
        "claim_invariant_across_all_worlds": True,
        "no_probe_binds_unexecuted_commission": True,
        "authority_boundary": copy.deepcopy(AUTHORITY_BOUNDARY),
    }
    commission["commission_id"] = stable_identifier(
        "experiment-world-matrix-commission",
        canonical_digest(_commission_identity_core(commission)),
    )
    commission["commission_digest"] = _top_level_digest(
        commission, "commission_digest"
    )
    validate_experiment_world_matrix_commission(commission)
    return commission


def validate_experiment_world_matrix_commission(
    commission: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a commission's schema, identities, and one-claim invariants."""

    record = copy.deepcopy(dict(commission))
    validate_payload(record, COMMISSION_SCHEMA)
    family = record["spec_family"]
    fixed = family["fixed_spec_semantics"]
    claim = fixed["tested_theory_claim"]
    effect = fixed["theory_effect_contract"]
    if claim["claim_digest"] != canonical_digest(
        claim, exclude_keys=("claim_digest",)
    ):
        raise ContractError("five-world commission tested-claim digest is invalid")
    programme = record["theory_programme_binding"]
    if (
        fixed["target_id"] != record["target_id"]
        or fixed["run_id"] != record["run_id"]
        or fixed["state_version"] != record["prior_state_version"]
        or claim["claim_id"] != fixed["theoretical_question_id"]
        or claim["theory_programme_id"] != programme["theory_programme_id"]
        or claim["source_theory_programme_digest"]
        != programme["source_theory_programme_digest"]
        or claim["source_reflection_packet_digest"]
        != programme["source_reflection_packet_digest"]
        or claim["conceptual_system_ids"] != programme["conceptual_system_ids"]
    ):
        raise ContractError("five-world commission crossed its exact theory claim")
    if (
        effect["tested_claim_id"] != claim["claim_id"]
        or effect["tested_claim_kind"] != claim["claim_kind"]
        or effect["target_relation"] != claim["target_relation"]
        or effect["if_supported"] != "record_scoped_consistency_only"
        or effect["if_falsified"] != "request_registered_premise_revision"
        or effect["theory_identity_locked"] is not True
        or effect["automatic_theory_selection"] is not False
        or effect["automatic_proof"] is not False
    ):
        raise ContractError("five-world commission theory-effect contract drift")
    if family["fixed_semantic_core_digest"] != canonical_digest(fixed):
        raise ContractError("five-world commission fixed spec core digest is invalid")
    expected_family_id = stable_identifier(
        "experiment-spec-family", canonical_digest(_family_identity_core(family))
    )
    if (
        family["family_id"] != expected_family_id
        or family["family_digest"] != _top_level_digest(family, "family_digest")
    ):
        raise ContractError("five-world commission spec-family identity is invalid")
    expected_commission_id = stable_identifier(
        "experiment-world-matrix-commission",
        canonical_digest(_commission_identity_core(record)),
    )
    if (
        record["commission_id"] != expected_commission_id
        or record["commission_digest"]
        != _top_level_digest(record, "commission_digest")
    ):
        raise ContractError("five-world commission identity or digest is invalid")
    return record


def _validate_spec_against_commission(
    commission: Mapping[str, Any], spec: Mapping[str, Any]
) -> dict[str, Any]:
    validated = validate_experiment_spec(spec)
    if _fixed_spec_semantics(validated) != commission["spec_family"][
        "fixed_spec_semantics"
    ]:
        raise ContractError(
            "experiment world changed the commission's exact claim/spec family"
        )
    return validated


def _reflection_binding(
    commission: Mapping[str, Any],
    world_id: str,
    spec: Mapping[str, Any],
    receipt: Mapping[str, Any],
    reflection: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(reflection))
    validate_payload(record, "dynamic_experiment_reflection_receipt_v1.schema.json")
    if record["reflection_digest"] != _top_level_digest(
        record, "reflection_digest"
    ):
        raise ContractError("experiment world reflection digest is invalid")
    experiment_binding = record["experiment_binding"]
    claim = commission["spec_family"]["fixed_spec_semantics"][
        "tested_theory_claim"
    ]
    if (
        experiment_binding["spec_id"] != spec["spec_id"]
        or experiment_binding["receipt_id"] != receipt["receipt_id"]
        or experiment_binding["spec_digest"] != spec["spec_digest"]
        or experiment_binding["receipt_content_digest"]
        != receipt["receipt_content_digest"]
        or experiment_binding["tested_claim_id"] != claim["claim_id"]
        or experiment_binding["tested_claim_digest"] != claim["claim_digest"]
        or record["epistemic_outcome"] != receipt["epistemic_outcome"]
    ):
        raise ContractError("experiment world reflection crossed its commission chain")
    pending = world_id == "registered_premise_falsifier"
    delta = record["typed_delta"]
    if pending:
        if (
            record["decision"] != "pending_registered_premise_review"
            or delta["status"] != "pending"
            or delta["kind"] != "registered_premise_review"
            or delta["tested_claim_id"] != claim["claim_id"]
            or delta["tested_claim_digest"] != claim["claim_digest"]
        ):
            raise ContractError("registered-premise world lacks its exact pending review")
    elif (
        record["decision"] != "record_only"
        or delta["status"] != "none"
        or delta["kind"] != "none"
        or delta["tested_claim_id"] is not None
    ):
        raise ContractError("non-falsifier world acquired a pending review")
    return {
        "reflection_receipt_id": record["reflection_receipt_id"],
        "reflection_digest": record["reflection_digest"],
        "decision": record["decision"],
        "typed_delta_digest": delta["delta_digest"],
    }


def bind_experiment_world_to_commission(
    commission: Mapping[str, Any],
    world_id: str,
    *,
    spec: Mapping[str, Any] | None,
    receipt: Mapping[str, Any] | None,
    reflection: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Bind one observed world to the exact pre-execution commission."""

    sealed = validate_experiment_world_matrix_commission(commission)
    contract = _WORLD_BY_ID.get(world_id)
    if contract is None:
        raise ContractError(f"unknown experiment matrix world: {world_id}")
    claim = sealed["spec_family"]["fixed_spec_semantics"]["tested_theory_claim"]
    spec_binding = receipt_binding = reflection_binding = None
    pending_status = "none"
    if contract["execution_disposition"] == "not_executed":
        if any(value is not None for value in (spec, receipt, reflection)):
            raise ContractError("no-probe world must keep its commission unexecuted")
    else:
        if not all(isinstance(value, Mapping) for value in (spec, receipt, reflection)):
            raise ContractError("executed experiment world lacks spec, receipt, or reflection")
        assert spec is not None and receipt is not None and reflection is not None
        validated_spec = _validate_spec_against_commission(sealed, spec)
        validate_experiment_receipt(receipt, validated_spec)
        effect_kind = receipt["theory_effect"]["effect_kind"]
        if (
            receipt["status"] not in contract["expected_statuses"]
            or receipt["epistemic_outcome"]
            not in contract["expected_epistemic_outcomes"]
            or effect_kind not in contract["expected_effect_kinds"]
        ):
            raise ContractError(f"world {world_id} outcome crossed its precommitment")
        spec_binding = {
            "spec_id": validated_spec["spec_id"],
            "spec_digest": validated_spec["spec_digest"],
            "precommitted_receipt_id": validated_spec["precommitted_receipt_id"],
            "spec_family_digest": sealed["spec_family"]["family_digest"],
        }
        receipt_binding = {
            "receipt_id": receipt["receipt_id"],
            "receipt_content_digest": receipt["receipt_content_digest"],
            "status": receipt["status"],
            "epistemic_outcome": receipt["epistemic_outcome"],
            "effect_kind": effect_kind,
        }
        reflection_binding = _reflection_binding(
            sealed, world_id, validated_spec, receipt, reflection
        )
        pending_status = (
            "pending" if contract["pending_review_authorized"] else "none"
        )
    binding: dict[str, Any] = {
        "schema_version": "1.0.0",
        "world_id": world_id,
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "tested_claim_id": claim["claim_id"],
        "tested_claim_digest": claim["claim_digest"],
        "execution_disposition": contract["execution_disposition"],
        "spec_binding": spec_binding,
        "receipt_binding": receipt_binding,
        "reflection_binding": reflection_binding,
        "pending_review_status": pending_status,
        "authority_boundary": copy.deepcopy(AUTHORITY_BOUNDARY),
    }
    binding["binding_digest"] = _top_level_digest(binding, "binding_digest")
    return binding


def validate_five_world_matrix_bindings(
    commission: Mapping[str, Any], bindings: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Prove all five observations share one commission and one tested claim."""

    sealed = validate_experiment_world_matrix_commission(commission)
    if len(bindings) != len(WORLD_IDS):
        raise ContractError("five-world commission requires exactly five bindings")
    by_world: dict[str, dict[str, Any]] = {}
    claim = sealed["spec_family"]["fixed_spec_semantics"]["tested_theory_claim"]
    for source in bindings:
        binding = copy.deepcopy(dict(source))
        if set(binding) != _BINDING_FIELDS:
            raise ContractError("experiment world commission binding is not schema-closed")
        if binding["binding_digest"] != _top_level_digest(
            binding, "binding_digest"
        ):
            raise ContractError("experiment world commission binding digest is invalid")
        world_id = binding["world_id"]
        if world_id in by_world or world_id not in _WORLD_BY_ID:
            raise ContractError("experiment world commission binding is duplicate or unknown")
        contract = _WORLD_BY_ID[world_id]
        if (
            binding["commission_id"] != sealed["commission_id"]
            or binding["commission_digest"] != sealed["commission_digest"]
            or binding["tested_claim_id"] != claim["claim_id"]
            or binding["tested_claim_digest"] != claim["claim_digest"]
            or binding["execution_disposition"] != contract["execution_disposition"]
            or binding["authority_boundary"] != AUTHORITY_BOUNDARY
        ):
            raise ContractError("experiment world binding crossed its exact commission")
        if world_id == "no_probe":
            if any(
                binding[field] is not None
                for field in ("spec_binding", "receipt_binding", "reflection_binding")
            ):
                raise ContractError("no-probe binding executed its sealed commission")
        else:
            spec_binding = binding["spec_binding"]
            receipt_binding = binding["receipt_binding"]
            reflection_binding = binding["reflection_binding"]
            if not all(
                isinstance(value, Mapping)
                for value in (spec_binding, receipt_binding, reflection_binding)
            ):
                raise ContractError(f"world {world_id} lacks an executed binding chain")
            if (
                spec_binding["spec_family_digest"]
                != sealed["spec_family"]["family_digest"]
                or spec_binding["precommitted_receipt_id"]
                != receipt_binding["receipt_id"]
                or receipt_binding["status"] not in contract["expected_statuses"]
                or receipt_binding["epistemic_outcome"]
                not in contract["expected_epistemic_outcomes"]
                or receipt_binding["effect_kind"]
                not in contract["expected_effect_kinds"]
            ):
                raise ContractError(f"world {world_id} binding outcome drift")
        expected_pending = (
            "pending" if contract["pending_review_authorized"] else "none"
        )
        if binding["pending_review_status"] != expected_pending:
            raise ContractError(f"world {world_id} pending-review authority drift")
        by_world[world_id] = binding
    if set(by_world) != set(WORLD_IDS):
        raise ContractError("five-world commission is missing a declared world")
    certificate: dict[str, Any] = {
        "schema_version": "1.0.0",
        "authority_status": LEGACY_AUTHORITY_STATUS,
        "canonical_execution_authorized": False,
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "world_ids": list(WORLD_IDS),
        "tested_claim_id": claim["claim_id"],
        "tested_claim_digest": claim["claim_digest"],
        "spec_family_digest": sealed["spec_family"]["family_digest"],
        "no_probe_binds_unexecuted_commission": True,
        "only_permitted_delta": "registered_premise_review_pending",
        "theory_identity_changed": False,
        "theory_selected": False,
        "proof_authorized": False,
        "automatic_evidence_relation_recorded": False,
    }
    certificate["certificate_digest"] = canonical_digest(certificate)
    return certificate


def build_experiment_authority_projection(
    *,
    target_id: str,
    run_id: str,
    prior_state_version: int,
    committed_ancestor: Mapping[str, Any],
    theory_programme: Mapping[str, Any],
    reflection_packet: Mapping[str, Any],
    conceptual_systems: Mapping[str, Any],
    genealogy: Mapping[str, Any],
    source_authority: Mapping[str, Any],
    registered_claim: Mapping[str, Any],
    generator_authority: Mapping[str, Any],
    adjudication_authority: Mapping[str, Any],
    schedule: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the closed actual-value base over which all five worlds range.

    The named arguments are deliberate: omission must fail at the Python call
    boundary, and every component is copied into the artifact rather than being
    replaced by a digest.  Component digests are indexes over those values, not
    substitutes for them.
    """

    supplied = {
        "committed_ancestor": committed_ancestor,
        "theory_programme": theory_programme,
        "reflection_packet": reflection_packet,
        "conceptual_systems": conceptual_systems,
        "genealogy": genealogy,
        "source_authority": source_authority,
        "registered_claim": registered_claim,
        "generator_authority": generator_authority,
        "adjudication_authority": adjudication_authority,
        "schedule": schedule,
    }
    components: list[dict[str, Any]] = []
    for component_kind in AUTHORITY_COMPONENT_ORDER:
        value = supplied[component_kind]
        if not isinstance(value, Mapping) or not value:
            raise ContractError(
                f"authority component {component_kind!r} must carry an actual nonempty object"
            )
        copied = copy.deepcopy(dict(value))
        components.append(
            {
                "component_kind": component_kind,
                "value": copied,
                "value_digest": canonical_digest(copied),
            }
        )
    projection: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": PROJECTION_V2_CONTRACT_VERSION,
        "target_id": target_id,
        "run_id": run_id,
        "prior_state_version": prior_state_version,
        "projection_schema_authority": copy.deepcopy(
            PROJECTION_SCHEMA_AUTHORITY
        ),
        "projector_authority": copy.deepcopy(PROJECTION_PROJECTOR_AUTHORITY),
        "coverage_contract": copy.deepcopy(PROJECTION_COVERAGE_CONTRACT),
        "component_order": list(AUTHORITY_COMPONENT_ORDER),
        "components": components,
    }
    projection["projection_id"] = stable_identifier(
        "experiment-authority-projection-v2",
        canonical_digest(projection),
    )
    projection["projection_digest"] = _top_level_digest(
        projection, "projection_digest"
    )
    return validate_experiment_authority_projection(projection)


def validate_experiment_authority_projection(
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate closed projection identities and exact component values."""

    memo_key = (
        "authority_projection",
        projection.get("projection_id"),
        projection.get("projection_digest"),
    )
    cached = _memoized_domain_validation(memo_key, projection)
    if cached is not None:
        return cached
    record = copy.deepcopy(dict(projection))
    required = {
        "schema_version",
        "contract_version",
        "projection_id",
        "target_id",
        "run_id",
        "prior_state_version",
        "projection_schema_authority",
        "projector_authority",
        "coverage_contract",
        "component_order",
        "components",
        "projection_digest",
    }
    if set(record) != required:
        raise ContractError("experiment authority projection is not schema-closed")
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != PROJECTION_V2_CONTRACT_VERSION
        or record["projection_schema_authority"]
        != PROJECTION_SCHEMA_AUTHORITY
        or record["projector_authority"] != PROJECTION_PROJECTOR_AUTHORITY
        or record["coverage_contract"] != PROJECTION_COVERAGE_CONTRACT
        or record["component_order"] != list(AUTHORITY_COMPONENT_ORDER)
    ):
        raise ContractError("experiment authority projection contract drift")
    if len(record["components"]) != len(AUTHORITY_COMPONENT_ORDER):
        raise ContractError("experiment authority projection omitted a component")
    observed_order: list[str] = []
    for row in record["components"]:
        if not isinstance(row, Mapping) or set(row) != {
            "component_kind",
            "value",
            "value_digest",
        }:
            raise ContractError("experiment authority component is not closed")
        observed_order.append(row["component_kind"])
        value = row["value"]
        if not isinstance(value, Mapping) or not value:
            raise ContractError(
                "experiment authority projection cannot use digest-only or empty components"
            )
        if row["value_digest"] != canonical_digest(value):
            raise ContractError("experiment authority component digest is invalid")
    if observed_order != list(AUTHORITY_COMPONENT_ORDER):
        raise ContractError("experiment authority component order or identity changed")
    claim = _registered_claim(record)
    if (
        claim.get("claim_kind") != "theory_premise"
        or claim.get("claim_digest")
        != canonical_digest(claim, exclude_keys=("claim_digest",))
    ):
        raise ContractError(
            "experiment authority projection requires one digest-valid registered premise"
        )
    systems = _projection_components(record)["conceptual_systems"]["value"]
    if systems.get("ordered_system_ids") != claim.get("conceptual_system_ids"):
        raise ContractError(
            "experiment authority conceptual-system projection crossed the registered claim"
        )
    expected_id = stable_identifier(
        "experiment-authority-projection-v2",
        canonical_digest(
            _identity_core(record, "projection_id", "projection_digest")
        ),
    )
    if (
        record["projection_id"] != expected_id
        or record["projection_digest"]
        != _top_level_digest(record, "projection_digest")
    ):
        raise ContractError("experiment authority projection identity is invalid")
    return _remember_domain_validation(memo_key, record)


def _intervention_projection(spec: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "adapter": copy.deepcopy(spec["adapter"]),
        "model": copy.deepcopy(spec["model"]),
        "resource_budget": copy.deepcopy(spec["resource_budget"]),
    }


def _claim_binding(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim_id": claim["claim_id"],
        "claim_digest": claim["claim_digest"],
        "claim_kind": claim["claim_kind"],
        "theory_programme_id": claim["theory_programme_id"],
        "source_theory_programme_digest": claim[
            "source_theory_programme_digest"
        ],
        "source_reflection_packet_digest": claim[
            "source_reflection_packet_digest"
        ],
        "conceptual_system_ids": list(claim["conceptual_system_ids"]),
    }


def _build_world_plan(
    world_id: str,
    *,
    spec: Mapping[str, Any] | None,
    baseline_intervention: Mapping[str, Any],
) -> dict[str, Any]:
    contract = _WORLD_BY_ID[world_id]
    if contract["execution_disposition"] == "not_executed":
        experiment_spec = None
        spec_digest = None
        intervention = None
        changes: list[str] = []
    else:
        if spec is None:
            raise ContractError(f"executed world {world_id} lacks an exact planned spec")
        experiment_spec = copy.deepcopy(dict(spec))
        spec_digest = experiment_spec["spec_digest"]
        intervention = _intervention_projection(experiment_spec)
        changes = _json_pointer_changes(
            baseline_intervention,
            intervention,
            path="/experiment_spec",
        )
        if any(not _path_is_permitted(path) for path in changes):
            raise ContractError(
                f"world {world_id} changed a non-intervention spec path"
            )
    plan: dict[str, Any] = {
        "world_id": world_id,
        "execution_disposition": contract["execution_disposition"],
        "intervention_kind": contract["intervention_kind"],
        "expected_statuses": list(contract["expected_statuses"]),
        "expected_epistemic_outcomes": list(
            contract["expected_epistemic_outcomes"]
        ),
        "expected_effect_kinds": list(contract["expected_effect_kinds"]),
        "pending_review_authorized": contract["pending_review_authorized"],
        "experiment_spec": experiment_spec,
        "spec_digest": spec_digest,
        "intervention_projection": intervention,
        "intervention_changed_paths": changes,
    }
    plan["plan_digest"] = _top_level_digest(plan, "plan_digest")
    return plan


def _validate_commission_base_producer_bindings(
    projection: Mapping[str, Any],
    bindings: Sequence[Mapping[str, Any]],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None,
) -> list[dict[str, Any]]:
    """Reopen the actual adjudication and schedule producers in fixed order."""

    requirements = (
        (
            FINAL_ADJUDICATION_STAGE_ID,
            FINAL_ADJUDICATION_PRODUCER_ROLE,
            "adjudication_authority",
        ),
        (
            PRE_EXPERIMENT_SCHEDULE_STAGE_ID,
            PRE_EXPERIMENT_SCHEDULE_PRODUCER_ROLE,
            "schedule",
        ),
    )
    if len(bindings) != len(requirements):
        raise ContractError(
            "commission requires exactly adjudication and schedule producer bindings"
        )
    components = _projection_components(projection)
    validated: list[dict[str, Any]] = []
    for supplied, (stage_id, producer_role, component_kind) in zip(
        bindings, requirements, strict=True
    ):
        row = validate_experiment_causal_producer_binding(
            supplied,
            expected_stage_id=stage_id,
            expected_producer_role=producer_role,
            expected_artifact=components[component_kind]["value"],
            evidence_resolver=evidence_resolver,
        )
        if (
            row["target_id"] != projection["target_id"]
            or row["run_id"] != projection["run_id"]
            or row["state_version"] != projection["prior_state_version"]
        ):
            raise ContractError(
                f"{component_kind} producer crossed the commission namespace"
            )
        validated.append(row)
    uniqueness_fields = (
        "binding_id",
        "producer_request.value.request_id",
        "producer_receipt.value.receipt_id",
        "artifact_evidence.immutable_history_path",
    )
    for field in uniqueness_fields:
        parts = field.split(".")
        values: list[Any] = []
        for row in validated:
            value: Any = row
            for part in parts:
                value = value[part]
            values.append(value)
        if len(set(values)) != len(values):
            raise ContractError("adjudication and schedule reused producer evidence")
    return validated


def build_pre_execution_world_matrix_commission(
    authority_projection: Mapping[str, Any],
    *,
    world_specs: Mapping[str, Mapping[str, Any]],
    adjudication_producer_binding: Mapping[str, Any],
    schedule_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Seal actual authority and all exact plans before any world request.

    ``world_specs`` must contain the four executed worlds.  The fifth plan is
    the same commission intentionally left unexecuted, never a different
    no-probe artifact.
    """

    projection = validate_experiment_authority_projection(authority_projection)
    trusted_resolver = (
        None
        if evidence_resolver is None
        else _require_trusted_evidence_resolver(evidence_resolver)
    )
    base_bindings = _validate_commission_base_producer_bindings(
        projection,
        [adjudication_producer_binding, schedule_producer_binding],
        evidence_resolver=trusted_resolver,
    )
    if set(world_specs) != set(EXECUTED_WORLD_IDS):
        raise ContractError(
            "v2 commission requires exact specs for all four executed worlds"
        )
    specs = {
        world_id: validate_experiment_spec(world_specs[world_id])
        for world_id in EXECUTED_WORLD_IDS
    }
    reference = specs[BASELINE_WORLD_ID]
    fixed = _fixed_spec_semantics(reference)
    claim = _registered_claim(projection)
    components = _projection_components(projection)
    if (
        fixed["target_id"] != projection["target_id"]
        or fixed["run_id"] != projection["run_id"]
        or fixed["state_version"] != projection["prior_state_version"]
        or fixed["tested_theory_claim"] != claim
        or fixed["theoretical_question_id"] != claim["claim_id"]
        or components["theory_programme"]["value_digest"]
        != claim["source_theory_programme_digest"]
        or _reflection_packet_identity_digest(projection)
        != claim["source_reflection_packet_digest"]
    ):
        raise ContractError(
            "v2 commission spec family crossed its complete authority projection"
        )
    for world_id, spec in specs.items():
        if _fixed_spec_semantics(spec) != fixed:
            raise ContractError(
                f"world {world_id} changed a non-intervention fixed spec field"
            )
    baseline = _intervention_projection(reference)
    family: dict[str, Any] = {
        "reference_world_id": BASELINE_WORLD_ID,
        "fixed_spec_fields": list(FIXED_SPEC_FIELDS),
        "fixed_spec_semantics": copy.deepcopy(fixed),
        "fixed_semantic_core_digest": canonical_digest(fixed),
        "baseline_intervention": baseline,
        "permitted_intervention_paths": list(PERMITTED_INTERVENTION_PATHS),
        "derived_execution_fields": list(DERIVED_EXECUTION_FIELDS),
    }
    family["family_id"] = stable_identifier(
        "experiment-spec-family-v2", canonical_digest(family)
    )
    family["family_digest"] = _top_level_digest(family, "family_digest")
    plans = [
        _build_world_plan(
            world_id,
            spec=specs.get(world_id),
            baseline_intervention=baseline,
        )
        for world_id in WORLD_IDS
    ]
    canonical_authorized = trusted_resolver is not None
    commission: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": COMMISSION_V2_CONTRACT_VERSION,
        "local_protocol_valid": True,
        "authority_status": (
            V2_AUTHORITY_STATUS
            if canonical_authorized
            else LOCAL_PROTOCOL_AUTHORITY_STATUS
        ),
        "canonical_execution_authorized": canonical_authorized,
        "matrix_scope": MATRIX_SCOPE,
        "target_id": projection["target_id"],
        "run_id": projection["run_id"],
        "prior_state_version": projection["prior_state_version"],
        "authority_projection": projection,
        "registered_claim_binding": _claim_binding(claim),
        "spec_family": family,
        "world_plan_order": list(WORLD_IDS),
        "world_plans": plans,
        "base_producer_bindings": base_bindings,
        "claim_invariant_across_all_worlds": True,
        "no_probe_binds_unexecuted_commission": True,
        "authority_boundary": copy.deepcopy(
            V2_AUTHORITY_BOUNDARY
            if canonical_authorized
            else LOCAL_PROTOCOL_AUTHORITY_BOUNDARY
        ),
    }
    commission["commission_id"] = stable_identifier(
        "experiment-world-matrix-commission-v2",
        canonical_digest(commission),
    )
    commission["commission_digest"] = _top_level_digest(
        commission, "commission_digest"
    )
    return validate_experiment_world_matrix_commission_v2(
        commission, evidence_resolver=trusted_resolver
    )


def validate_experiment_world_matrix_commission_v2(
    commission: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Validate the only commission version allowed to authorize execution."""

    memo_key = (
        "world_matrix_commission_v2",
        commission.get("commission_id"),
        commission.get("commission_digest"),
        evidence_resolver is not None,
    )
    cached = _memoized_domain_validation(memo_key, commission)
    if cached is not None:
        return cached
    record = copy.deepcopy(dict(commission))
    validate_payload(record, COMMISSION_V2_SCHEMA)
    canonical_authorized = record["canonical_execution_authorized"] is True
    expected_status = (
        V2_AUTHORITY_STATUS
        if canonical_authorized
        else LOCAL_PROTOCOL_AUTHORITY_STATUS
    )
    expected_boundary = (
        V2_AUTHORITY_BOUNDARY
        if canonical_authorized
        else LOCAL_PROTOCOL_AUTHORITY_BOUNDARY
    )
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != COMMISSION_V2_CONTRACT_VERSION
        or record["local_protocol_valid"] is not True
        or record["authority_status"] != expected_status
        or record["authority_boundary"] != expected_boundary
        or record["world_plan_order"] != list(WORLD_IDS)
    ):
        raise ContractError("v2 world commission authority contract drift")
    trusted_resolver = None
    if canonical_authorized:
        trusted_resolver = _require_trusted_evidence_resolver(evidence_resolver)
    elif evidence_resolver is not None:
        trusted_resolver = _require_trusted_evidence_resolver(evidence_resolver)
    projection = validate_experiment_authority_projection(
        record["authority_projection"]
    )
    base_bindings = _validate_commission_base_producer_bindings(
        projection,
        record["base_producer_bindings"],
        evidence_resolver=trusted_resolver,
    )
    if record["base_producer_bindings"] != base_bindings:
        raise ContractError("commission base producer bindings drifted")
    claim = _registered_claim(projection)
    if (
        record["target_id"] != projection["target_id"]
        or record["run_id"] != projection["run_id"]
        or record["prior_state_version"] != projection["prior_state_version"]
        or record["registered_claim_binding"] != _claim_binding(claim)
    ):
        raise ContractError("v2 world commission crossed its authority base")
    family = record["spec_family"]
    fixed = family["fixed_spec_semantics"]
    if (
        family["reference_world_id"] != BASELINE_WORLD_ID
        or family["fixed_spec_fields"] != list(FIXED_SPEC_FIELDS)
        or family["fixed_semantic_core_digest"] != canonical_digest(fixed)
        or family["permitted_intervention_paths"]
        != list(PERMITTED_INTERVENTION_PATHS)
        or family["derived_execution_fields"] != list(DERIVED_EXECUTION_FIELDS)
        or family["family_id"]
        != stable_identifier(
            "experiment-spec-family-v2",
            canonical_digest(
                _identity_core(family, "family_id", "family_digest")
            ),
        )
        or family["family_digest"]
        != _top_level_digest(family, "family_digest")
    ):
        raise ContractError("v2 world commission spec family is invalid")
    if len(record["world_plans"]) != len(WORLD_IDS):
        raise ContractError("v2 world commission omitted a world plan")
    for index, plan in enumerate(record["world_plans"]):
        world_id = WORLD_IDS[index]
        contract = _WORLD_BY_ID[world_id]
        if (
            plan["world_id"] != world_id
            or plan["execution_disposition"]
            != contract["execution_disposition"]
            or plan["intervention_kind"] != contract["intervention_kind"]
            or plan["expected_statuses"] != contract["expected_statuses"]
            or plan["expected_epistemic_outcomes"]
            != contract["expected_epistemic_outcomes"]
            or plan["expected_effect_kinds"]
            != contract["expected_effect_kinds"]
            or plan["pending_review_authorized"]
            != contract["pending_review_authorized"]
            or plan["plan_digest"] != _top_level_digest(plan, "plan_digest")
        ):
            raise ContractError(f"v2 world plan {world_id} drifted")
        if world_id == "no_probe":
            if any(
                plan[field] is not None
                for field in (
                    "experiment_spec",
                    "spec_digest",
                    "intervention_projection",
                )
            ) or plan["intervention_changed_paths"] != []:
                raise ContractError("v2 no-probe plan must remain unexecuted")
            continue
        spec = validate_experiment_spec(plan["experiment_spec"])
        intervention = _intervention_projection(spec)
        changes = _json_pointer_changes(
            family["baseline_intervention"],
            intervention,
            path="/experiment_spec",
        )
        if (
            _fixed_spec_semantics(spec) != fixed
            or spec["spec_digest"] != plan["spec_digest"]
            or intervention != plan["intervention_projection"]
            or changes != plan["intervention_changed_paths"]
            or any(not _path_is_permitted(path) for path in changes)
        ):
            raise ContractError(f"v2 world plan {world_id} changed sealed semantics")
    components = _projection_components(projection)
    if (
        fixed["tested_theory_claim"] != claim
        or fixed["target_id"] != record["target_id"]
        or fixed["run_id"] != record["run_id"]
        or fixed["state_version"] != record["prior_state_version"]
        or components["theory_programme"]["value_digest"]
        != claim["source_theory_programme_digest"]
        or _reflection_packet_identity_digest(projection)
        != claim["source_reflection_packet_digest"]
    ):
        raise ContractError("v2 world commission claim/base projection mismatch")
    expected_id = stable_identifier(
        "experiment-world-matrix-commission-v2",
        canonical_digest(
            _identity_core(record, "commission_id", "commission_digest")
        ),
    )
    if (
        record["commission_id"] != expected_id
        or record["commission_digest"]
        != _top_level_digest(record, "commission_digest")
    ):
        raise ContractError("v2 world commission identity is invalid")
    return _remember_domain_validation(memo_key, record)


def experiment_world_matrix_authority_status(
    commission: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> str:
    """Classify v1 as diagnostic and v2 as execution-authoritative."""

    version = commission.get("schema_version")
    if version == "1.0.0":
        validate_experiment_world_matrix_commission(commission)
        return LEGACY_AUTHORITY_STATUS
    if version == "2.0.0":
        validated = validate_experiment_world_matrix_commission_v2(
            commission, evidence_resolver=evidence_resolver
        )
        return str(validated["authority_status"])
    raise ContractError("unknown experiment world commission version")


def require_authoritative_experiment_world_matrix_commission(
    commission: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Fail closed unless the supplied commission is the complete v2 form."""

    if commission.get("schema_version") != "2.0.0":
        if commission.get("schema_version") == "1.0.0":
            validate_experiment_world_matrix_commission(commission)
            raise ContractError(
                "legacy v1 world commission is diagnostic-only and cannot authorize canonical execution"
            )
        raise ContractError("canonical execution requires a v2 world commission")
    trusted_resolver = _require_trusted_evidence_resolver(evidence_resolver)
    validated = validate_experiment_world_matrix_commission_v2(
        commission, evidence_resolver=trusted_resolver
    )
    if (
        validated["local_protocol_valid"] is not True
        or validated["canonical_execution_authorized"] is not True
        or validated["authority_status"] != V2_AUTHORITY_STATUS
    ):
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.TRUSTED_EVIDENCE_REQUIRED,
            "a local-only commission cannot authorize canonical execution",
        )
    return validated


def _require_binding_namespace(
    binding: Mapping[str, Any],
    commission: Mapping[str, Any],
    label: str,
) -> None:
    if (
        binding["target_id"] != commission["target_id"]
        or binding["run_id"] != commission["run_id"]
        or binding["state_version"] != commission["prior_state_version"]
    ):
        raise ContractError(f"{label} crossed the exact commission namespace")


def build_experiment_world_request(
    commission: Mapping[str, Any],
    world_id: str,
    *,
    commission_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Create the immutable input that must exist before execution/no-probe."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    if world_id not in WORLD_IDS:
        raise ContractError(f"unknown v2 experiment world {world_id!r}")
    commission_binding = validate_experiment_causal_producer_binding(
        commission_producer_binding,
        expected_stage_id=COMMISSION_STAGE_ID,
        expected_producer_role=COMMISSION_PRODUCER_ROLE,
        expected_artifact=sealed,
        expected_artifact_id=sealed["commission_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(commission_binding, sealed, "commission producer")
    for upstream in sealed["base_producer_bindings"]:
        _require_causal_precedence(
            upstream, commission_binding, "authority-to-commission"
        )
    plan = _world_plan(sealed, world_id)
    spec = plan["experiment_spec"]
    request: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": REQUEST_V2_CONTRACT_VERSION,
        "world_id": world_id,
        "execution_disposition": plan["execution_disposition"],
        "commission_input": sealed,
        "commission_input_digest": canonical_digest(sealed),
        "commission_producer_binding": commission_binding,
        "world_plan_digest": plan["plan_digest"],
        "planned_spec_id": None if spec is None else spec["spec_id"],
        "planned_spec_digest": None if spec is None else spec["spec_digest"],
    }
    request["request_id"] = stable_identifier(
        "experiment-world-request-v2", canonical_digest(request)
    )
    request["request_digest"] = _top_level_digest(request, "request_digest")
    return validate_experiment_world_request(
        sealed, request, evidence_resolver=evidence_resolver
    )


def validate_experiment_world_request(
    commission: Mapping[str, Any],
    request: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    memo_key = (
        "world_request_v2",
        request.get("request_id"),
        request.get("request_digest"),
        commission.get("commission_id"),
        commission.get("commission_digest"),
        evidence_resolver is not None,
    )
    cached = _memoized_domain_validation(memo_key, request)
    if cached is not None:
        return cached
    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    record = copy.deepcopy(dict(request))
    validate_payload(record, REQUEST_V2_SCHEMA)
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != REQUEST_V2_CONTRACT_VERSION
        or record["commission_input"] != sealed
        or record["commission_input_digest"] != canonical_digest(sealed)
    ):
        raise ContractError(
            "world request did not consume the exact full pre-execution commission"
        )
    commission_binding = validate_experiment_causal_producer_binding(
        record["commission_producer_binding"],
        expected_stage_id=COMMISSION_STAGE_ID,
        expected_producer_role=COMMISSION_PRODUCER_ROLE,
        expected_artifact=sealed,
        expected_artifact_id=sealed["commission_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(commission_binding, sealed, "commission producer")
    for upstream in sealed["base_producer_bindings"]:
        _require_causal_precedence(
            upstream, commission_binding, "authority-to-commission"
        )
    plan = _world_plan(sealed, record["world_id"])
    spec = plan["experiment_spec"]
    if (
        record["execution_disposition"] != plan["execution_disposition"]
        or record["world_plan_digest"] != plan["plan_digest"]
        or record["planned_spec_id"]
        != (None if spec is None else spec["spec_id"])
        or record["planned_spec_digest"]
        != (None if spec is None else spec["spec_digest"])
    ):
        raise ContractError("world request crossed its exact sealed plan")
    expected_id = stable_identifier(
        "experiment-world-request-v2",
        canonical_digest(
            _identity_core(record, "request_id", "request_digest")
        ),
    )
    if (
        record["request_id"] != expected_id
        or record["request_digest"]
        != _top_level_digest(record, "request_digest")
    ):
        raise ContractError("v2 world request identity is invalid")
    return _remember_domain_validation(memo_key, record)


def build_experiment_no_probe_decision(
    commission: Mapping[str, Any],
    *,
    world_request: Mapping[str, Any],
    world_request_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Build the separately producible decision for the unexecuted world."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    request = validate_experiment_world_request(
        sealed, world_request, evidence_resolver=evidence_resolver
    )
    if request["world_id"] != "no_probe":
        raise ContractError("no-probe decision requires the no_probe request")
    request_binding = validate_experiment_causal_producer_binding(
        world_request_producer_binding,
        expected_stage_id=WORLD_REQUEST_STAGE_ID,
        expected_producer_role=WORLD_REQUEST_PRODUCER_ROLE,
        expected_artifact=request,
        expected_artifact_id=request["request_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(request_binding, sealed, "world request producer")
    _require_causal_precedence(
        request["commission_producer_binding"],
        request_binding,
        "commission-to-world-request",
    )
    decision: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": NO_PROBE_DECISION_V2_CONTRACT_VERSION,
        "world_id": "no_probe",
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "request_id": request["request_id"],
        "request_digest": request["request_digest"],
        "request_producer_binding_id": request_binding["binding_id"],
        "request_producer_binding_digest": request_binding["binding_digest"],
        "execution_disposition": "not_executed",
        "execution_attempted": False,
        "experiment_receipt_expected": False,
    }
    decision["decision_id"] = stable_identifier(
        "experiment-no-probe-decision-v2", canonical_digest(decision)
    )
    decision["decision_digest"] = _top_level_digest(
        decision, "decision_digest"
    )
    return validate_experiment_no_probe_decision(
        sealed,
        decision,
        world_request=request,
        world_request_producer_binding=request_binding,
        evidence_resolver=evidence_resolver,
    )


def validate_experiment_no_probe_decision(
    commission: Mapping[str, Any],
    decision: Mapping[str, Any],
    *,
    world_request: Mapping[str, Any],
    world_request_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Recompute the unexecuted-world decision from its separately sealed request."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    request = validate_experiment_world_request(
        sealed, world_request, evidence_resolver=evidence_resolver
    )
    request_binding = validate_experiment_causal_producer_binding(
        world_request_producer_binding,
        expected_stage_id=WORLD_REQUEST_STAGE_ID,
        expected_producer_role=WORLD_REQUEST_PRODUCER_ROLE,
        expected_artifact=request,
        expected_artifact_id=request["request_id"],
        evidence_resolver=evidence_resolver,
    )
    record = copy.deepcopy(dict(decision))
    required = {
        "schema_version",
        "contract_version",
        "decision_id",
        "world_id",
        "commission_id",
        "commission_digest",
        "request_id",
        "request_digest",
        "request_producer_binding_id",
        "request_producer_binding_digest",
        "execution_disposition",
        "execution_attempted",
        "experiment_receipt_expected",
        "decision_digest",
    }
    if set(record) != required:
        raise ContractError("no-probe decision is not schema-closed")
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != NO_PROBE_DECISION_V2_CONTRACT_VERSION
        or record["world_id"] != "no_probe"
        or request["world_id"] != "no_probe"
        or record["commission_id"] != sealed["commission_id"]
        or record["commission_digest"] != sealed["commission_digest"]
        or record["request_id"] != request["request_id"]
        or record["request_digest"] != request["request_digest"]
        or record["request_producer_binding_id"] != request_binding["binding_id"]
        or record["request_producer_binding_digest"]
        != request_binding["binding_digest"]
        or record["execution_disposition"] != "not_executed"
        or record["execution_attempted"] is not False
        or record["experiment_receipt_expected"] is not False
    ):
        raise ContractError("no-probe decision crossed its exact request or authority")
    expected_id = stable_identifier(
        "experiment-no-probe-decision-v2",
        canonical_digest(_identity_core(record, "decision_id", "decision_digest")),
    )
    if (
        record["decision_id"] != expected_id
        or record["decision_digest"] != _top_level_digest(record, "decision_digest")
    ):
        raise ContractError("no-probe decision identity is invalid")
    return record


def _validate_world_request_producer_binding(
    commission: Mapping[str, Any],
    request: Mapping[str, Any],
    binding: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None,
) -> dict[str, Any]:
    row = validate_experiment_causal_producer_binding(
        binding,
        expected_stage_id=WORLD_REQUEST_STAGE_ID,
        expected_producer_role=WORLD_REQUEST_PRODUCER_ROLE,
        expected_artifact=request,
        expected_artifact_id=request["request_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(row, commission, "world request producer")
    _require_causal_precedence(
        request["commission_producer_binding"],
        row,
        "commission-to-world-request",
    )
    return row


def _observation_producer_chain(observation: Mapping[str, Any]) -> list[dict[str, Any]]:
    chain = [
        copy.deepcopy(observation["world_request"]["commission_producer_binding"]),
        copy.deepcopy(observation["world_request_producer_binding"]),
        copy.deepcopy(observation["execution_producer_binding"]),
    ]
    if observation["reflection_producer_binding"] is not None:
        chain.append(copy.deepcopy(observation["reflection_producer_binding"]))
    return chain


def bind_experiment_world_observation(
    commission: Mapping[str, Any],
    world_id: str,
    *,
    world_request: Mapping[str, Any],
    world_request_producer_binding: Mapping[str, Any],
    observed_authority_projection: Mapping[str, Any],
    spec: Mapping[str, Any] | None,
    receipt: Mapping[str, Any] | None,
    execution_producer_binding: Mapping[str, Any],
    reflection: Mapping[str, Any] | None,
    reflection_producer_binding: Mapping[str, Any] | None,
    no_probe_decision: Mapping[str, Any] | None = None,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Bind one observation to actual request/execution/reflection producers."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    request = validate_experiment_world_request(
        sealed, world_request, evidence_resolver=evidence_resolver
    )
    request_binding = _validate_world_request_producer_binding(
        sealed,
        request,
        world_request_producer_binding,
        evidence_resolver=evidence_resolver,
    )
    if request["world_id"] != world_id:
        raise ContractError("world observation request belongs to a different world")
    observed = validate_experiment_authority_projection(observed_authority_projection)
    authority_changes = _json_pointer_changes(
        sealed["authority_projection"], observed, path="/authority_projection"
    )
    if authority_changes:
        raise ContractError(
            "post-world complete authority projection changed: "
            + ", ".join(authority_changes)
        )
    plan = _world_plan(sealed, world_id)
    experiment_spec = experiment_receipt = reflection_receipt = decision = None
    if world_id == "no_probe":
        if any(value is not None for value in (spec, receipt, reflection)):
            raise ContractError(
                "no-probe observation must consume the commission without execution"
            )
        if reflection_producer_binding is not None or not isinstance(
            no_probe_decision, Mapping
        ):
            raise ContractError("no-probe observation requires only its decision producer")
        decision = validate_experiment_no_probe_decision(
            sealed,
            no_probe_decision,
            world_request=request,
            world_request_producer_binding=request_binding,
            evidence_resolver=evidence_resolver,
        )
        execution_binding = validate_experiment_causal_producer_binding(
            execution_producer_binding,
            expected_stage_id=NO_PROBE_DECISION_STAGE_ID,
            expected_producer_role=NO_PROBE_DECISION_PRODUCER_ROLE,
            expected_artifact=decision,
            expected_artifact_id=decision["decision_id"],
            evidence_resolver=evidence_resolver,
        )
        reflection_binding = None
    else:
        if no_probe_decision is not None or not all(
            isinstance(value, Mapping) for value in (spec, receipt, reflection)
        ):
            raise ContractError(
                f"executed world {world_id} lacks spec, receipt, or reflection"
            )
        if not isinstance(reflection_producer_binding, Mapping):
            raise ContractError(f"executed world {world_id} lacks reflection producer")
        assert spec is not None and receipt is not None and reflection is not None
        experiment_spec = validate_experiment_spec(spec)
        if experiment_spec != plan["experiment_spec"]:
            raise ContractError("world executed a spec not sealed by its commission")
        experiment_receipt = copy.deepcopy(dict(receipt))
        validate_experiment_receipt(experiment_receipt, experiment_spec)
        effect_kind = experiment_receipt["theory_effect"]["effect_kind"]
        if (
            experiment_receipt["status"] not in plan["expected_statuses"]
            or experiment_receipt["epistemic_outcome"]
            not in plan["expected_epistemic_outcomes"]
            or effect_kind not in plan["expected_effect_kinds"]
        ):
            raise ContractError(f"world {world_id} outcome crossed its exact plan")
        execution_binding = validate_experiment_causal_producer_binding(
            execution_producer_binding,
            expected_stage_id=EXPERIMENT_EXECUTION_STAGE_ID,
            expected_producer_role=EXPERIMENT_EXECUTION_PRODUCER_ROLE,
            expected_artifact=experiment_receipt,
            expected_artifact_id=experiment_receipt["receipt_id"],
            evidence_resolver=evidence_resolver,
        )
        reflection_receipt = copy.deepcopy(dict(reflection))
        _reflection_binding(
            sealed,
            world_id,
            experiment_spec,
            experiment_receipt,
            reflection_receipt,
        )
        reflection_binding = validate_experiment_causal_producer_binding(
            reflection_producer_binding,
            expected_stage_id=POST_RESULT_REFLECTION_STAGE_ID,
            expected_producer_role=POST_RESULT_REFLECTION_PRODUCER_ROLE,
            expected_artifact=reflection_receipt,
            expected_artifact_id=reflection_receipt["reflection_receipt_id"],
            evidence_resolver=evidence_resolver,
        )
    _require_binding_namespace(execution_binding, sealed, "execution producer")
    _require_causal_precedence(
        request_binding, execution_binding, "world-request-to-execution"
    )
    if reflection_binding is not None:
        _require_binding_namespace(reflection_binding, sealed, "reflection producer")
        _require_causal_precedence(
            execution_binding, reflection_binding, "execution-to-reflection"
        )
    observation: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": OBSERVATION_V2_CONTRACT_VERSION,
        "world_id": world_id,
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "world_request": request,
        "world_request_producer_binding": request_binding,
        "observed_authority_projection": observed,
        "authority_projection_changed_paths": authority_changes,
        "intervention_changed_paths": copy.deepcopy(plan["intervention_changed_paths"]),
        "unauthorized_changed_paths": [],
        "experiment_spec": experiment_spec,
        "experiment_receipt": experiment_receipt,
        "no_probe_decision": decision,
        "execution_producer_binding": execution_binding,
        "reflection_receipt": reflection_receipt,
        "reflection_producer_binding": reflection_binding,
        "authority_boundary": copy.deepcopy(V2_AUTHORITY_BOUNDARY),
    }
    observation["production_bindings_digest"] = canonical_digest(
        _observation_producer_chain(observation)
    )
    observation["observation_id"] = stable_identifier(
        "experiment-world-observation-v2", canonical_digest(observation)
    )
    observation["observation_digest"] = _top_level_digest(
        observation, "observation_digest"
    )
    return validate_experiment_world_observation(
        sealed, observation, evidence_resolver=evidence_resolver
    )


def validate_experiment_world_observation(
    commission: Mapping[str, Any],
    observation: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Reopen one observation and every actual producer in its causal chain."""

    memo_key = (
        "world_observation_v2",
        observation.get("observation_id"),
        observation.get("observation_digest"),
        commission.get("commission_id"),
        commission.get("commission_digest"),
        evidence_resolver is not None,
    )
    cached = _memoized_domain_validation(memo_key, observation)
    if cached is not None:
        return cached
    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    record = copy.deepcopy(dict(observation))
    validate_payload(record, OBSERVATION_V2_SCHEMA)
    request = validate_experiment_world_request(
        sealed, record["world_request"], evidence_resolver=evidence_resolver
    )
    request_binding = _validate_world_request_producer_binding(
        sealed,
        request,
        record["world_request_producer_binding"],
        evidence_resolver=evidence_resolver,
    )
    world_id = record["world_id"]
    if (
        request["world_id"] != world_id
        or record["commission_id"] != sealed["commission_id"]
        or record["commission_digest"] != sealed["commission_digest"]
        or record["authority_boundary"] != V2_AUTHORITY_BOUNDARY
    ):
        raise ContractError("world observation crossed its exact commission")
    observed = validate_experiment_authority_projection(
        record["observed_authority_projection"]
    )
    authority_changes = _json_pointer_changes(
        sealed["authority_projection"], observed, path="/authority_projection"
    )
    if record["authority_projection_changed_paths"] != authority_changes:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.AUTHORITY_PROJECTION_CHANGED,
            "world observation changed-path audit is not exact",
        )
    if authority_changes:
        raise WorldMatrixContractError(
            WorldMatrixFailureReason.AUTHORITY_PROJECTION_CHANGED,
            "post-world complete authority projection changed: "
            + ", ".join(authority_changes),
        )
    plan = _world_plan(sealed, world_id)
    if (
        record["intervention_changed_paths"] != plan["intervention_changed_paths"]
        or any(not _path_is_permitted(path) for path in record["intervention_changed_paths"])
        or record["unauthorized_changed_paths"] != []
    ):
        raise ContractError("world observation intervention-path audit drift")
    if world_id == "no_probe":
        if any(
            record[field] is not None
            for field in ("experiment_spec", "experiment_receipt", "reflection_receipt", "reflection_producer_binding")
        ):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.NO_PROBE_EXECUTION_FORBIDDEN,
                "no-probe observation executed its commission",
            )
        decision = validate_experiment_no_probe_decision(
            sealed,
            record["no_probe_decision"],
            world_request=request,
            world_request_producer_binding=request_binding,
            evidence_resolver=evidence_resolver,
        )
        execution_binding = validate_experiment_causal_producer_binding(
            record["execution_producer_binding"],
            expected_stage_id=NO_PROBE_DECISION_STAGE_ID,
            expected_producer_role=NO_PROBE_DECISION_PRODUCER_ROLE,
            expected_artifact=decision,
            expected_artifact_id=decision["decision_id"],
            evidence_resolver=evidence_resolver,
        )
        reflection_binding = None
    else:
        if record["no_probe_decision"] is not None:
            raise ContractError("executed world contains a no-probe decision")
        spec = validate_experiment_spec(record["experiment_spec"])
        if spec != plan["experiment_spec"]:
            raise ContractError("world observation contains an unplanned spec")
        receipt = record["experiment_receipt"]
        reflection = record["reflection_receipt"]
        validate_experiment_receipt(receipt, spec)
        effect_kind = receipt["theory_effect"]["effect_kind"]
        if (
            receipt["status"] not in plan["expected_statuses"]
            or receipt["epistemic_outcome"] not in plan["expected_epistemic_outcomes"]
            or effect_kind not in plan["expected_effect_kinds"]
        ):
            raise ContractError(f"world {world_id} observation outcome drift")
        execution_binding = validate_experiment_causal_producer_binding(
            record["execution_producer_binding"],
            expected_stage_id=EXPERIMENT_EXECUTION_STAGE_ID,
            expected_producer_role=EXPERIMENT_EXECUTION_PRODUCER_ROLE,
            expected_artifact=receipt,
            expected_artifact_id=receipt["receipt_id"],
            evidence_resolver=evidence_resolver,
        )
        _reflection_binding(sealed, world_id, spec, receipt, reflection)
        reflection_binding = validate_experiment_causal_producer_binding(
            record["reflection_producer_binding"],
            expected_stage_id=POST_RESULT_REFLECTION_STAGE_ID,
            expected_producer_role=POST_RESULT_REFLECTION_PRODUCER_ROLE,
            expected_artifact=reflection,
            expected_artifact_id=reflection["reflection_receipt_id"],
            evidence_resolver=evidence_resolver,
        )
    _require_binding_namespace(execution_binding, sealed, "execution producer")
    _require_causal_precedence(
        request_binding, execution_binding, "world-request-to-execution"
    )
    if reflection_binding is not None:
        _require_binding_namespace(reflection_binding, sealed, "reflection producer")
        _require_causal_precedence(
            execution_binding, reflection_binding, "execution-to-reflection"
        )
    chain = _observation_producer_chain(record)
    if record["production_bindings_digest"] != canonical_digest(chain):
        raise ContractError("world observation producer-binding chain drift")
    expected_id = stable_identifier(
        "experiment-world-observation-v2",
        canonical_digest(_identity_core(record, "observation_id", "observation_digest")),
    )
    if (
        record["observation_id"] != expected_id
        or record["observation_digest"] != _top_level_digest(record, "observation_digest")
    ):
        raise ContractError("world observation identity is invalid")
    return _remember_domain_validation(memo_key, record)


def build_experiment_world_observation_envelope(
    commission: Mapping[str, Any],
    observation: Mapping[str, Any],
    *,
    observation_producer_binding: Mapping[str, Any],
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Seal one independently produced observation for parallel aggregation."""

    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    observed = validate_experiment_world_observation(
        sealed, observation, evidence_resolver=evidence_resolver
    )
    producer = validate_experiment_causal_producer_binding(
        observation_producer_binding,
        expected_stage_id=WORLD_OBSERVATION_STAGE_ID,
        expected_producer_role=WORLD_OBSERVATION_PRODUCER_ROLE,
        expected_artifact=observed,
        expected_artifact_id=observed["observation_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(producer, sealed, "observation producer")
    _require_causal_precedence(
        _observation_producer_chain(observed)[-1],
        producer,
        "world-result-to-observation",
    )
    envelope: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": OBSERVATION_ENVELOPE_V2_CONTRACT_VERSION,
        "world_id": observed["world_id"],
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "observation": observed,
        "observation_producer_binding": producer,
    }
    envelope["envelope_id"] = stable_identifier(
        "experiment-world-observation-envelope-v2", canonical_digest(envelope)
    )
    envelope["envelope_digest"] = _top_level_digest(envelope, "envelope_digest")
    return validate_experiment_world_observation_envelope(
        sealed, envelope, evidence_resolver=evidence_resolver
    )


def validate_experiment_world_observation_envelope(
    commission: Mapping[str, Any],
    envelope: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    memo_key = (
        "world_observation_envelope_v2",
        envelope.get("envelope_id"),
        envelope.get("envelope_digest"),
        commission.get("commission_id"),
        commission.get("commission_digest"),
        evidence_resolver is not None,
    )
    cached = _memoized_domain_validation(memo_key, envelope)
    if cached is not None:
        return cached
    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    record = copy.deepcopy(dict(envelope))
    validate_payload(record, OBSERVATION_ENVELOPE_V2_SCHEMA)
    observation = validate_experiment_world_observation(
        sealed, record["observation"], evidence_resolver=evidence_resolver
    )
    producer = validate_experiment_causal_producer_binding(
        record["observation_producer_binding"],
        expected_stage_id=WORLD_OBSERVATION_STAGE_ID,
        expected_producer_role=WORLD_OBSERVATION_PRODUCER_ROLE,
        expected_artifact=observation,
        expected_artifact_id=observation["observation_id"],
        evidence_resolver=evidence_resolver,
    )
    _require_binding_namespace(producer, sealed, "observation producer")
    _require_causal_precedence(
        _observation_producer_chain(observation)[-1],
        producer,
        "world-result-to-observation",
    )
    if (
        record["schema_version"] != "2.0.0"
        or record["contract_version"] != OBSERVATION_ENVELOPE_V2_CONTRACT_VERSION
        or record["world_id"] != observation["world_id"]
        or record["commission_id"] != sealed["commission_id"]
        or record["commission_digest"] != sealed["commission_digest"]
    ):
        raise ContractError("observation envelope crossed its exact world/base")
    expected_id = stable_identifier(
        "experiment-world-observation-envelope-v2",
        canonical_digest(_identity_core(record, "envelope_id", "envelope_digest")),
    )
    if (
        record["envelope_id"] != expected_id
        or record["envelope_digest"] != _top_level_digest(record, "envelope_digest")
    ):
        raise ContractError("observation envelope identity is invalid")
    return _remember_domain_validation(memo_key, record)


def _require_separate_world_producers(envelopes: Sequence[Mapping[str, Any]]) -> None:
    binding_rows: list[Mapping[str, Any]] = []
    for envelope in envelopes:
        observation = envelope["observation"]
        binding_rows.extend(
            [
                observation["world_request_producer_binding"],
                observation["execution_producer_binding"],
                envelope["observation_producer_binding"],
            ]
        )
        if observation["reflection_producer_binding"] is not None:
            binding_rows.append(observation["reflection_producer_binding"])
    extractors = (
        lambda row: row["binding_id"],
        lambda row: row["producer_request"]["value"]["request_id"],
        lambda row: row["producer_receipt"]["value"]["receipt_id"],
        lambda row: row["artifact_evidence"]["declared_output_path"],
        lambda row: row["artifact_evidence"]["immutable_history_path"],
    )
    for extract in extractors:
        values = [extract(row) for row in binding_rows]
        if len(values) != len(set(values)):
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.SEPARATE_WORLD_PRODUCERS_REQUIRED,
                "five-world aggregation requires separately bound actual observations",
            )


def _derive_five_world_certificate(
    commission: Mapping[str, Any],
    observation_envelopes: Sequence[Mapping[str, Any]],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    sealed = require_authoritative_experiment_world_matrix_commission(
        commission, evidence_resolver=evidence_resolver
    )
    if len(observation_envelopes) != len(WORLD_IDS):
        raise ContractError("v2 matrix requires exactly five observation envelopes")
    envelopes: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    for index, envelope in enumerate(observation_envelopes):
        sealed_envelope = validate_experiment_world_observation_envelope(
            sealed, envelope, evidence_resolver=evidence_resolver
        )
        if sealed_envelope["world_id"] != WORLD_IDS[index]:
            raise WorldMatrixContractError(
                WorldMatrixFailureReason.WORLD_ENVELOPE_ORDER_INVALID,
                "v2 matrix envelope order or world identity changed",
            )
        envelopes.append(sealed_envelope)
        observations.append(sealed_envelope["observation"])
    _require_separate_world_producers(envelopes)
    claim = _registered_claim(sealed["authority_projection"])
    falsifier = observations[WORLD_IDS.index("registered_premise_falsifier")]
    delta = falsifier["reflection_receipt"]["typed_delta"]
    if (
        delta["status"] != "pending"
        or delta["kind"] != "registered_premise_review"
        or delta["tested_claim_id"] != claim["claim_id"]
        or delta["tested_claim_digest"] != claim["claim_digest"]
    ):
        raise ContractError("v2 matrix lacks its one registered pending review")
    world_bindings = []
    for envelope, observation in zip(envelopes, observations, strict=True):
        world_bindings.append(
            {
                "world_id": observation["world_id"],
                "envelope_id": envelope["envelope_id"],
                "envelope_digest": envelope["envelope_digest"],
                "observation_id": observation["observation_id"],
                "observation_digest": observation["observation_digest"],
                "observation_producer_binding_id": envelope[
                    "observation_producer_binding"
                ]["binding_id"],
                "observation_producer_binding_digest": envelope[
                    "observation_producer_binding"
                ]["binding_digest"],
                "request_id": observation["world_request"]["request_id"],
                "request_digest": observation["world_request"]["request_digest"],
                "request_producer_binding_id": observation[
                    "world_request_producer_binding"
                ]["binding_id"],
                "request_producer_binding_digest": observation[
                    "world_request_producer_binding"
                ]["binding_digest"],
            }
        )
    path_rows = [
        {
            "world_id": row["world_id"],
            "authority_projection_changed_paths": row[
                "authority_projection_changed_paths"
            ],
            "intervention_changed_paths": row["intervention_changed_paths"],
            "unauthorized_changed_paths": row["unauthorized_changed_paths"],
        }
        for row in observations
    ]
    producer_summary = [
        {
            "world_id": envelope["world_id"],
            "observation_production_bindings_digest": envelope["observation"][
                "production_bindings_digest"
            ],
            "observation_producer_binding_id": envelope[
                "observation_producer_binding"
            ]["binding_id"],
            "observation_producer_binding_digest": envelope[
                "observation_producer_binding"
            ]["binding_digest"],
        }
        for envelope in envelopes
    ]
    certificate: dict[str, Any] = {
        "schema_version": "2.0.0",
        "contract_version": CERTIFICATE_V2_CONTRACT_VERSION,
        "local_protocol_valid": True,
        "authority_status": V2_AUTHORITY_STATUS,
        "canonical_execution_authorized": True,
        "commission_id": sealed["commission_id"],
        "commission_digest": sealed["commission_digest"],
        "authority_projection_id": sealed["authority_projection"]["projection_id"],
        "authority_projection_digest": sealed["authority_projection"]["projection_digest"],
        "registered_claim_binding": _claim_binding(claim),
        "world_ids": list(WORLD_IDS),
        "world_bindings": world_bindings,
        "changed_path_audit": {
            "permitted_intervention_paths": list(PERMITTED_INTERVENTION_PATHS),
            "worlds": path_rows,
            "all_authority_projections_equal": True,
            "all_unauthorized_changed_paths_absent": True,
        },
        "pending_review": {
            "status": "pending_next_cycle_reflection_only",
            "world_id": "registered_premise_falsifier",
            "tested_claim_id": claim["claim_id"],
            "tested_claim_digest": claim["claim_digest"],
            "requested_followup_kind": delta["requested_followup_kind"],
            "current_cycle_authority_projection_changed": False,
            "direct_current_cycle_mutation_authorized": False,
        },
        "derived_denials": copy.deepcopy(DERIVED_DENIALS),
        "production_bindings_digest": canonical_digest(producer_summary),
        "authority_boundary": copy.deepcopy(V2_AUTHORITY_BOUNDARY),
    }
    certificate["certificate_id"] = stable_identifier(
        "experiment-world-matrix-certificate-v2", canonical_digest(certificate)
    )
    certificate["certificate_digest"] = _top_level_digest(
        certificate, "certificate_digest"
    )
    validate_payload(certificate, CERTIFICATE_V2_SCHEMA)
    return certificate


def validate_five_world_matrix(
    commission: Mapping[str, Any],
    observation_envelopes: Sequence[Mapping[str, Any]],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Aggregate five separately sealed observations over one exact base."""

    return _derive_five_world_certificate(
        commission, observation_envelopes, evidence_resolver=evidence_resolver
    )


def validate_experiment_world_matrix_certificate_v2(
    commission: Mapping[str, Any],
    observation_envelopes: Sequence[Mapping[str, Any]],
    certificate: Mapping[str, Any],
    *,
    evidence_resolver: CommittedCausalEvidenceResolver | None = None,
) -> dict[str, Any]:
    """Reopen a v2 certificate and reject caller-authored denial fields."""

    supplied = copy.deepcopy(dict(certificate))
    validate_payload(supplied, CERTIFICATE_V2_SCHEMA)
    expected = _derive_five_world_certificate(
        commission, observation_envelopes, evidence_resolver=evidence_resolver
    )
    if supplied != expected:
        raise ContractError(
            "five-world certificate denial or pending-review derivation drift"
        )
    return supplied


__all__ = [
    "AUTHORITY_BOUNDARY",
    "AUTHORITY_COMPONENT_ORDER",
    "BASELINE_WORLD_ID",
    "CAUSAL_BINDING_V2_CONTRACT_VERSION",
    "CAUSAL_BINDING_V2_SCHEMA",
    "CERTIFICATE_V2_CONTRACT_VERSION",
    "CERTIFICATE_V2_SCHEMA",
    "COMMISSION_CONTRACT_VERSION",
    "COMMISSION_PRODUCER_ROLE",
    "COMMISSION_STAGE_ID",
    "COMMISSION_V2_CONTRACT_VERSION",
    "COMMISSION_V2_SCHEMA",
    "CommittedCausalEvidenceResolver",
    "EXECUTED_WORLD_IDS",
    "EXPERIMENT_EXECUTION_PRODUCER_ROLE",
    "EXPERIMENT_EXECUTION_STAGE_ID",
    "FINAL_ADJUDICATION_PRODUCER_ROLE",
    "FINAL_ADJUDICATION_STAGE_ID",
    "LEGACY_AUTHORITY_STATUS",
    "MATRIX_SCOPE",
    "NO_PROBE_DECISION_PRODUCER_ROLE",
    "NO_PROBE_DECISION_STAGE_ID",
    "NO_PROBE_DECISION_V2_CONTRACT_VERSION",
    "OBSERVATION_ENVELOPE_V2_CONTRACT_VERSION",
    "OBSERVATION_ENVELOPE_V2_SCHEMA",
    "OBSERVATION_V2_CONTRACT_VERSION",
    "OBSERVATION_V2_SCHEMA",
    "PERMITTED_INTERVENTION_PATHS",
    "POST_RESULT_REFLECTION_PRODUCER_ROLE",
    "POST_RESULT_REFLECTION_STAGE_ID",
    "PRE_EXPERIMENT_SCHEDULE_PRODUCER_ROLE",
    "PRE_EXPERIMENT_SCHEDULE_STAGE_ID",
    "PROJECTION_COVERAGE_CONTRACT",
    "PROJECTION_V2_CONTRACT_VERSION",
    "REQUEST_V2_CONTRACT_VERSION",
    "REQUEST_V2_SCHEMA",
    "V2_AUTHORITY_BOUNDARY",
    "V2_AUTHORITY_STATUS",
    "WORLD_OBSERVATION_PRODUCER_ROLE",
    "WORLD_OBSERVATION_STAGE_ID",
    "WORLD_IDS",
    "WORLD_REQUEST_PRODUCER_ROLE",
    "WORLD_REQUEST_STAGE_ID",
    "bind_experiment_world_to_commission",
    "bind_experiment_world_observation",
    "build_experiment_authority_projection",
    "build_experiment_causal_producer_binding",
    "build_experiment_world_matrix_commission",
    "build_experiment_no_probe_decision",
    "build_experiment_world_observation_envelope",
    "build_experiment_world_request",
    "build_pre_execution_world_matrix_commission",
    "experiment_world_matrix_authority_status",
    "require_authoritative_experiment_world_matrix_commission",
    "validate_experiment_authority_projection",
    "validate_experiment_authority_projection_coverage",
    "validate_experiment_causal_producer_binding",
    "validate_experiment_no_probe_decision",
    "validate_experiment_world_matrix_certificate_v2",
    "validate_experiment_world_matrix_commission",
    "validate_experiment_world_matrix_commission_v2",
    "validate_experiment_world_observation",
    "validate_experiment_world_observation_envelope",
    "validate_experiment_world_request",
    "validate_five_world_matrix",
    "validate_five_world_matrix_bindings",
    "world_matrix_validation_cache_scope",
]
