# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Independent durable coordination for theory-bound action lifecycles.

The canonical discovery store is scientific authority: advancing its head means
publishing a new theory/support generation.  Reserving or finishing an action is
operational bookkeeping and must not consume such a generation.  This module
therefore keeps reservations and terminal records in a distinct
``DiscoveryTransactionStore`` rooted outside the theory store.

Every reservation binds the exact *current* portable content-graph commit and
graph references, optional path-free N+7 support roots, a schedule, and an
action set.  Finalization performs a mandatory read-only theory-head recheck.
Head drift is persisted as ``rebase_required``; it is never repaired by writing
the theory store.  The boundary is intentionally point-in-time rather than a
cross-store transaction: these records coordinate work, but grant no theory
selection, scientific promotion, proof, experiment, or physics authority.
"""

from __future__ import annotations

import copy
import dataclasses
import datetime as dt
import json
import math
import os
import threading
from collections.abc import Mapping, Sequence
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
    validate_digest,
    validate_identifier,
)
from agentic.experiments.content_graph_transactions import (
    reopen_content_graph_transaction,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    CompareAndSwapError,
    DiscoveryTransactionStore,
    IdempotencyConflict,
    StateCorruptionError,
    VerifiedCommit,
)


LEDGER_KIND = "independent_action_coordination_ledger"
LEDGER_SCHEMA_VERSION = "2.0.0"
LEGACY_LEDGER_SCHEMA_VERSION = "1.0.0"
RESERVATION_STATUS = "reserved"
PROOF_RESERVATION_STATUS = "proof_attempt_reserved"
PROOF_EXECUTION_CLAIM_STATUS = "proof_execution_claimed"
PROOF_TERMINAL_RECOVERY_CLAIM_STATUS = "proof_terminal_recovery_claimed"
PROOF_RESULT_INTAKE_CLAIM_STATUS = "proof_result_intake_claimed"
PROOF_RESULT_INTAKE_CONSUMED_STATUS = "proof_result_intake_consumed"
PROOF_RESULT_INTAKE_SUPERSEDED_STATUS = "proof_result_intake_superseded"
REBASE_REQUIRED_STATUS = "rebase_required"
TERMINAL_STATUSES = frozenset(
    {"completed", "failed", "released", "compensation_required"}
)

# Fixed protocol ceilings.  They are intentionally local constants rather than
# aliases to another subsystem so widening a schedule or content-graph contract
# cannot silently widen this operational ledger.
MAX_ACTIONS_PER_RESERVATION = 128
MAX_SUPPORT_ROOT_REFERENCES = 16
MAX_TERMINAL_EVIDENCE_DIGESTS = 64
MAX_REFERENCE_BYTES = 64 * 1024
MAX_THEORY_BINDING_BYTES = 512 * 1024
MAX_RECORD_BYTES = 256 * 1024
MAX_PROOF_RECORD_BYTES = 4 * 1024 * 1024
MAX_LEDGER_RECORDS = 1024
MAX_LEDGER_STATE_BYTES = 32 * 1024 * 1024
MAX_CAS_RETRIES = 8
MAX_PROOF_TERMINAL_ATTACHMENTS = 1036
MAX_PROOF_TERMINAL_ATTACHMENT_BYTES = 800 * 1024 * 1024
MAX_PROOF_RECOVERY_SEED_ATTACHMENTS = 520
MAX_PROOF_RECOVERY_SEED_BYTES = 520 * 1024 * 1024
PROOF_TERMINAL_METADATA_RESERVE_BYTES = 16 * 1024 * 1024
MAX_PROOF_EXECUTOR_LEASE_SECONDS = 900
PROOF_EXECUTOR_RECOVERY_MARGIN_SECONDS = 60

_COORDINATION_BRANCH_ID = "coordination"
_NAMED_FAILPOINTS = frozenset(
    {
        "after_state_write",
        "after_artifact_write:1",
        "after_manifest_write",
        "after_journal_prepared",
        "after_commit_rename",
        "after_pointer_write",
        "after_journal_complete",
    }
)
_AUTHORITY_BOUNDARY: dict[str, Any] = {
    "boundary_kind": "coordination_only_non_theory_non_selection",
    "may_mutate_theory_store": False,
    "may_select_theory": False,
    "may_promote_scientific_claims": False,
    "may_claim_proof_or_experiment_authority": False,
    "cross_store_atomicity_claimed": False,
    "head_check_scope": "read_only_point_in_time_observation",
}
_PROOF_COORDINATION_BOUNDARY: dict[str, Any] = {
    **_AUTHORITY_BOUNDARY,
    "boundary_kind": "one_action_one_attempt_proof_coordination_only",
    "serialized_projection_is_execution_authority": False,
    "live_theory_capability_required": True,
    "live_execution_claim_required": True,
    "execution_claim_is_one_shot": True,
    "durable_bounded_executor_lease_required": True,
    "durable_launch_boundary_checkpoint_required_before_spawn": True,
    "generic_callback_route_allowed": False,
}
_PROOF_TERMINAL_BOUNDARY: dict[str, Any] = {
    **_PROOF_COORDINATION_BOUNDARY,
    "boundary_kind": "atomic_proof_terminal_and_pending_n_plus_one_only",
    "accepts_live_launch_authority": False,
    "terminal_projection_is_launch_authority": False,
    "claim_remains_spent": True,
    "respawn_authorized": False,
    "same_cycle_theory_mutation_authorized": False,
    "pending_n_plus_one_intake_required": True,
    "abandonment_requires_governed_expired_executor_lease": True,
}
_PROOF_RESULT_INTAKE_BOUNDARY: dict[str, Any] = {
    "boundary_kind": "one_shot_proof_result_later_reflection_intake_only",
    "may_commit_distinct_descendant_reflection_intake": True,
    "may_mutate_existing_theory_objects": False,
    "may_select_theory": False,
    "may_promote_scientific_claims": False,
    "may_claim_proof_or_checker_soundness": False,
    "same_cycle_theory_mutation_authorized": False,
    "semantic_reflection_performed": False,
    "cross_store_atomicity_claimed": False,
    "theory_side_reconciliation_outbox_required": True,
    "verified_active_prefix_descendant_required_at_consumption": True,
    "one_shot_coordination_claim_required": True,
    "one_shot_coordination_consumption_required": True,
}
_PROOF_RESULT_INTAKE_SUPERSESSION_BOUNDARY: dict[str, Any] = {
    **_PROOF_RESULT_INTAKE_BOUNDARY,
    "boundary_kind": "terminal_proof_result_intake_supersession_only",
    "may_commit_distinct_descendant_reflection_intake": False,
    "theory_side_reconciliation_outbox_required": False,
    "one_shot_coordination_consumption_required": False,
    "terminal_supersession_record_required": True,
    "recommission_requires_new_identity": True,
}
_PROOF_DERIVED_ARTIFACT_FIELDS = {
    "terminal_receipt": "terminal_receipt",
    "receipt_index_membership": "receipt_index_membership",
    "pending_n_plus_one_reflection_request": (
        "pending_n_plus_one_reflection_request"
    ),
}
_TYPED_TERMINAL_REPLAY_PREFIX = "typed_replay/"
_TYPED_TERMINAL_REPLAY_BINDING_NAMES = frozenset(
    {
        "typed_replay/binding/prelaunch-projection.json",
        "typed_replay/binding/handoff.json",
        "typed_replay/binding/reservation.json",
        "typed_replay/binding/execution-claim.json",
        "typed_replay/binding/execution-claim-reference.json",
        "typed_replay/binding/projection.json",
    }
)
_PROOF_CLAIM_RECOVERY_SEED_NAMES = frozenset(
    {
        "typed_replay/binding/prelaunch-projection.json",
        "typed_replay/binding/handoff.json",
        "typed_replay/binding/reservation.json",
    }
)
_PROOF_INVOCATION_RECOVERY_FIXED_NAMES = frozenset(
    {
        "typed_replay/invocation/projection.json",
        "typed_replay/invocation/dependency-authority.json",
        "typed_replay/invocation/executable-authority.json",
        "typed_replay/invocation/stdin.bin",
    }
)
_PROOF_INVOCATION_RECOVERY_FILE_PREFIX = "typed_replay/invocation/files/"
_THEORY_CONTEXT_LOCKS: dict[tuple[int, int], threading.RLock] = {}


class CoordinationStoreBoundaryError(ContractError):
    """Raised when coordination and theory do not occupy disjoint roots."""


class TheoryHeadBindingError(ContractError):
    """Raised when a proposed reservation does not bind the current graph head."""


class ActionReservationConflict(ContractError):
    """Raised when another reservation already owns a schedule/action pair."""


class ReservationTerminalConflict(ContractError):
    """Raised when a reservation already has a different terminal request."""


class ProofExecutionClaimConsumed(ContractError):
    """Raised whenever a durable one-shot proof launch claim already exists."""


class ProofTerminalConflict(ContractError):
    """Raised when one proof reservation already has another terminal request."""


class ProofExecutorLeaseExpired(ContractError):
    """Raised when an executor reaches the launch boundary after lease expiry."""


class ProofLaunchCheckpointConflict(ContractError):
    """Raised when one attempt already has another launch-boundary checkpoint."""


class ProofTerminalRecoveryNotReady(ContractError):
    """Raised while the bounded executor lease still owns the terminal gap."""


class ProofRecoverySeedUnavailable(ContractError):
    """Raised when historical coordination bytes cannot reconstruct recovery."""


class ProofResultIntakeConflict(ContractError):
    """Raised when a proof-result intake lost its exact descendant CAS."""


class ProofResultIntakeStale(ContractError):
    """Raised before claiming an intake whose source theory is no longer current."""


class ProofResultIntakeInactive(ContractError):
    """Raised when the exact descendant stopped being current before consumption."""


class CoordinationConcurrencyError(ContractError):
    """Raised after the fixed CAS retry budget is exhausted."""


@dataclasses.dataclass(frozen=True, slots=True)
class CoordinationLedgerResult:
    """Portable defensive result for one reservation or terminal record.

    Runtime-local commit paths are deliberately absent.  Both mappings are
    decoded afresh from private canonical bytes on every access, so caller
    mutation cannot change a later retry or comparison.
    """

    _record_data: bytes
    _ledger_commit_reference_data: bytes

    @property
    def record(self) -> Mapping[str, Any]:
        return _decode_canonical_mapping(self._record_data, "coordination record")

    @property
    def ledger_commit_reference(self) -> Mapping[str, Any]:
        return _decode_canonical_mapping(
            self._ledger_commit_reference_data,
            "coordination ledger commit reference",
        )

    @property
    def reservation_id(self) -> str:
        return str(self.record["reservation_id"])

    @property
    def status(self) -> str:
        return str(self.record["status"])

    @property
    def ledger_generation(self) -> int:
        return int(self.ledger_commit_reference["generation"])

    def as_dict(self) -> dict[str, Any]:
        return {
            "record": self.record,
            "ledger_commit_reference": self.ledger_commit_reference,
        }


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
        raise StateCorruptionError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise StateCorruptionError(f"{label} is not one canonical JSON object")
    return value


def _self_digest(value: Mapping[str, Any], field: str) -> str:
    material = copy.deepcopy(dict(value))
    material.pop(field, None)
    return canonical_digest(material)


def _parse_canonical_utc_timestamp(value: object, label: str) -> dt.datetime:
    """Decode one durable ``Z`` timestamp without accepting alternate spellings."""

    if type(value) is not str or not value.endswith("Z"):
        raise StateCorruptionError(f"{label} must be one canonical UTC timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise StateCorruptionError(
            f"{label} must be one canonical UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != dt.timedelta(0):
        raise StateCorruptionError(f"{label} must be one canonical UTC timestamp")
    parsed = parsed.astimezone(dt.timezone.utc)
    if parsed.isoformat().replace("+00:00", "Z") != value:
        raise StateCorruptionError(f"{label} must be one canonical UTC timestamp")
    return parsed


def _validate_governed_clock_authority(value: object) -> dict[str, Any]:
    """Validate the exact unauthenticated local-clock manifest stored at claim."""

    if not isinstance(value, Mapping):
        raise StateCorruptionError(
            "proof execution clock authority must be an object"
        )
    authority = copy.deepcopy(dict(value))
    expected_values: dict[str, Any] = {
        "schema_version": "1.0.0",
        "authority_id": "abducer-system-utc-clock.v1",
        "authority_kind": "closed_registry_local_process_wall_clock",
        "implementation_module": "agentic.discovery.theory_gate",
        "implementation_symbol": "_system_utc_now",
        "time_scale": "UTC",
        "resolution": "microsecond",
        "authority_scope": "ephemeral_present_investment_decision_only",
        "caller_supplied_instants_allowed": False,
        "authentication_status": "not_externally_authenticated",
        "trust_boundary": "current_process_host_clock_and_checkout",
    }
    if set(authority) != {
        *expected_values,
        "implementation_digest",
        "authority_digest",
    }:
        raise StateCorruptionError(
            "proof execution clock authority shape is not exact"
        )
    try:
        validate_digest(authority["implementation_digest"])
        validate_digest(authority["authority_digest"])
    except ContractError as exc:
        raise StateCorruptionError(
            "proof execution clock authority digest is malformed"
        ) from exc
    if (
        any(authority[field] != expected for field, expected in expected_values.items())
        or authority["authority_digest"]
        != canonical_digest(authority, exclude_keys=("authority_digest",))
    ):
        raise StateCorruptionError(
            "proof execution clock authority is inconsistent"
        )
    return authority


def _validate_recovery_clock_authority(value: object) -> dict[str, Any]:
    """Validate the closed recovery-only host-clock authority manifest."""

    if not isinstance(value, Mapping):
        raise StateCorruptionError(
            "proof recovery clock authority must be an object"
        )
    authority = copy.deepcopy(dict(value))
    expected_values: dict[str, Any] = {
        "schema_version": "1.0.0",
        "authority_id": "abducer-proof-executor-recovery-utc-clock.v1",
        "authority_kind": (
            "closed_registry_local_process_wall_clock_recovery_only"
        ),
        "implementation_module": "agentic.discovery.theory_gate",
        "implementation_symbol": "_system_utc_now",
        "time_scale": "UTC",
        "resolution": "microsecond",
        "authority_scope": (
            "proof_executor_lease_checkpoint_and_expiry_recovery_only"
        ),
        "caller_supplied_instants_allowed": False,
        "readable_after_investment_expiry": True,
        "may_validate_present_investment": False,
        "may_authorize_launch": False,
        "may_authorize_respawn": False,
        "may_mutate_theory": False,
        "authentication_status": "not_externally_authenticated",
        "trust_boundary": "current_process_host_clock_and_checkout",
    }
    if set(authority) != {
        *expected_values,
        "implementation_digest",
        "authority_digest",
    }:
        raise StateCorruptionError(
            "proof recovery clock authority shape is not exact"
        )
    try:
        validate_digest(authority["implementation_digest"])
        validate_digest(authority["authority_digest"])
    except ContractError as exc:
        raise StateCorruptionError(
            "proof recovery clock authority digest is malformed"
        ) from exc
    if (
        any(
            authority[field] != expected
            for field, expected in expected_values.items()
        )
        or authority["authority_digest"]
        != canonical_digest(authority, exclude_keys=("authority_digest",))
    ):
        raise StateCorruptionError(
            "proof recovery clock authority is inconsistent"
        )
    return authority


def _executor_lease(
    *,
    reservation: Mapping[str, Any],
    issued_at: str,
) -> dict[str, Any]:
    """Derive one non-renewable lease that strictly contains process budget."""

    issued = _parse_canonical_utc_timestamp(
        issued_at, "proof executor lease issued_at"
    )
    budget = reservation.get("resource_budget")
    if not isinstance(budget, Mapping):
        raise ContractError("proof executor lease requires a resource budget")
    wall = budget.get("wall_time_seconds")
    grace = budget.get("grace_period_seconds")
    if (
        isinstance(wall, bool)
        or not isinstance(wall, (int, float))
        or not math.isfinite(float(wall))
        or float(wall) <= 0
        or isinstance(grace, bool)
        or not isinstance(grace, (int, float))
        or not math.isfinite(float(grace))
        or float(grace) < 0
    ):
        raise ContractError(
            "proof executor lease resource duration is invalid"
        )
    duration = (
        math.ceil(float(wall) + float(grace))
        + PROOF_EXECUTOR_RECOVERY_MARGIN_SECONDS
    )
    if duration > MAX_PROOF_EXECUTOR_LEASE_SECONDS:
        raise ContractError(
            "proof resource duration exceeds the fixed executor-lease ceiling"
        )
    expires = issued + dt.timedelta(seconds=duration)
    lease: dict[str, Any] = {
        "schema_version": "1.0.0",
        "lease_kind": "bounded_single_executor_recovery_lease",
        "lease_id": stable_identifier(
            "proof-executor-lease-v1",
            reservation["reservation_digest"],
            reservation["execution_claim_id"],
            issued_at,
            duration,
        ),
        "reservation_id": reservation["reservation_id"],
        "reservation_digest": reservation["reservation_digest"],
        "execution_claim_id": reservation["execution_claim_id"],
        "attempt_id": reservation["attempt_id"],
        "proof_runtime_ref": reservation["proof_runtime_ref"],
        "issued_at": issued_at,
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
        "lease_duration_seconds": duration,
        "resource_wall_time_seconds": float(wall),
        "resource_grace_period_seconds": float(grace),
        "recovery_margin_seconds": PROOF_EXECUTOR_RECOVERY_MARGIN_SECONDS,
        "maximum_lease_seconds": MAX_PROOF_EXECUTOR_LEASE_SECONDS,
        "bounded": True,
        "renewable": False,
        "launch_boundary_checkpoint_required_before_spawn": True,
        "expiry_authorizes_respawn": False,
        "pid_only_death_authority": False,
        "caller_supplied_time_allowed": False,
        "authority_scope": (
            "abandonment_classification_only_no_launch_or_proof_authority"
        ),
    }
    lease["lease_digest"] = _self_digest(lease, "lease_digest")
    return lease


def _validate_executor_lease(
    value: object,
    *,
    reservation: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise StateCorruptionError("proof executor lease must be an object")
    lease = copy.deepcopy(dict(value))
    if set(lease) != {
        "schema_version",
        "lease_kind",
        "lease_id",
        "lease_digest",
        "reservation_id",
        "reservation_digest",
        "execution_claim_id",
        "attempt_id",
        "proof_runtime_ref",
        "issued_at",
        "expires_at",
        "lease_duration_seconds",
        "resource_wall_time_seconds",
        "resource_grace_period_seconds",
        "recovery_margin_seconds",
        "maximum_lease_seconds",
        "bounded",
        "renewable",
        "launch_boundary_checkpoint_required_before_spawn",
        "expiry_authorizes_respawn",
        "pid_only_death_authority",
        "caller_supplied_time_allowed",
        "authority_scope",
    }:
        raise StateCorruptionError("proof executor lease shape is not exact")
    issued = _parse_canonical_utc_timestamp(
        lease["issued_at"], "proof executor lease issued_at"
    )
    expires = _parse_canonical_utc_timestamp(
        lease["expires_at"], "proof executor lease expires_at"
    )
    expected = _executor_lease(
        reservation=reservation,
        issued_at=lease["issued_at"],
    )
    if (
        lease != expected
        or expires <= issued
        or lease["lease_duration_seconds"] > MAX_PROOF_EXECUTOR_LEASE_SECONDS
    ):
        raise StateCorruptionError("proof executor lease is inconsistent")
    return lease


def _validate_launch_checkpoint(
    value: object,
    *,
    reservation: Mapping[str, Any],
    claim: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise StateCorruptionError(
            "proof launch-boundary checkpoint must be an object"
        )
    checkpoint = copy.deepcopy(dict(value))
    required_fields = {
        "schema_version",
        "record_kind",
        "checkpoint_id",
        "checkpoint_digest",
        "reservation_id",
        "reservation_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "attempt_id",
        "ledger_generation",
        "checkpoint_status",
        "binding_id",
        "binding_digest",
        "invocation_id",
        "invocation_digest",
        "executor_lease_id",
        "executor_lease_digest",
        "lease_expires_at",
        "observed_at",
        "clock_authority",
        "clock_authority_digest",
        "lease_active_at_checkpoint",
        "launch_may_have_occurred_after_checkpoint",
        "launch_observed_by_checkpoint",
        "process_evidence_recorded",
        "pid_evidence_used",
        "respawn_authorized",
        "authority_scope",
    }
    if set(checkpoint) not in {
        frozenset(required_fields),
        frozenset(required_fields | {"recovery_seed"}),
    }:
        raise StateCorruptionError(
            "proof launch-boundary checkpoint shape is not exact"
        )
    lease = _validate_executor_lease(
        claim.get("executor_lease"),
        reservation=reservation,
    )
    clock = _validate_recovery_clock_authority(
        checkpoint["clock_authority"]
    )
    observed = _parse_canonical_utc_timestamp(
        checkpoint["observed_at"],
        "proof launch-boundary observed_at",
    )
    issued = _parse_canonical_utc_timestamp(
        lease["issued_at"],
        "proof launch-boundary lease issued_at",
    )
    expires = _parse_canonical_utc_timestamp(
        checkpoint["lease_expires_at"],
        "proof launch-boundary lease_expires_at",
    )
    if (
        checkpoint["schema_version"] != "1.0.0"
        or checkpoint["record_kind"]
        != "proof_launch_boundary_checkpoint"
        or checkpoint["reservation_id"] != reservation["reservation_id"]
        or checkpoint["reservation_digest"]
        != reservation["reservation_digest"]
        or checkpoint["execution_claim_id"] != claim["execution_claim_id"]
        or checkpoint["execution_claim_digest"]
        != claim["execution_claim_digest"]
        or checkpoint["attempt_id"] != reservation["attempt_id"]
        or checkpoint["checkpoint_status"] != "launch_boundary_entered"
        or checkpoint["executor_lease_id"] != lease["lease_id"]
        or checkpoint["executor_lease_digest"] != lease["lease_digest"]
        or checkpoint["lease_expires_at"] != lease["expires_at"]
        or checkpoint["clock_authority_digest"]
        != clock["authority_digest"]
        or observed < issued
        or observed >= expires
        or checkpoint["lease_active_at_checkpoint"] is not True
        or checkpoint[
            "launch_may_have_occurred_after_checkpoint"
        ] is not True
        or checkpoint["launch_observed_by_checkpoint"] is not False
        or checkpoint["process_evidence_recorded"] is not False
        or checkpoint["pid_evidence_used"] is not False
        or checkpoint["respawn_authorized"] is not False
        or checkpoint["authority_scope"]
        != "conservative_launch_boundary_only_no_process_outcome_claim"
        or checkpoint["checkpoint_id"]
        != stable_identifier(
            "proof-launch-boundary-checkpoint-v1",
            claim["execution_claim_digest"],
            checkpoint["binding_digest"],
            checkpoint["invocation_digest"],
        )
        or checkpoint["checkpoint_digest"]
        != _self_digest(checkpoint, "checkpoint_digest")
    ):
        raise StateCorruptionError(
            "proof launch-boundary checkpoint is inconsistent"
        )
    for field in (
        "checkpoint_id",
        "binding_id",
        "invocation_id",
    ):
        validate_identifier(checkpoint[field], field)
    for field in (
        "checkpoint_digest",
        "binding_digest",
        "invocation_digest",
        "executor_lease_digest",
        "clock_authority_digest",
    ):
        validate_digest(checkpoint[field])
    if (
        isinstance(checkpoint["ledger_generation"], bool)
        or not isinstance(checkpoint["ledger_generation"], int)
        or checkpoint["ledger_generation"] <= 0
    ):
        raise StateCorruptionError(
            "proof launch-boundary checkpoint generation is invalid"
        )
    if "recovery_seed" in checkpoint:
        _validate_proof_recovery_seed(
            checkpoint["recovery_seed"],
            expected_phase="staged_invocation",
        )
    return checkpoint


def _validate_proof_terminal_recovery_claim(
    value: object,
    *,
    reservation: Mapping[str, Any],
    claim: Mapping[str, Any],
    checkpoint: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Replay the exact winner of one expired-lease recovery CAS."""

    if not isinstance(value, Mapping):
        raise StateCorruptionError(
            "proof terminal recovery claim must be an object"
        )
    record = copy.deepcopy(dict(value))
    if set(record) != {
        "schema_version",
        "record_kind",
        "recovery_claim_id",
        "recovery_claim_digest",
        "reservation_id",
        "reservation_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "attempt_id",
        "ledger_generation",
        "status",
        "executor_lease_id",
        "executor_lease_digest",
        "launch_boundary_checkpoint_digest",
        "claim_recovery_seed_digest",
        "checkpoint_recovery_seed_digest",
        "recovery_clock_observation",
        "selected_reason_code",
        "terminal_observed_at",
        "claim_remains_spent",
        "respawn_authorized",
        "authority_scope",
    }:
        raise StateCorruptionError(
            "proof terminal recovery claim shape is not exact"
        )
    claim_seed = claim.get("recovery_seed")
    if not isinstance(claim_seed, Mapping):
        raise StateCorruptionError(
            "proof terminal recovery claim lacks its claim recovery seed"
        )
    validated_claim_seed = _validate_proof_recovery_seed(
        claim_seed,
        expected_phase="claim_binding",
    )
    checkpoint_seed: dict[str, Any] | None = None
    if checkpoint is not None:
        raw_checkpoint_seed = checkpoint.get("recovery_seed")
        if not isinstance(raw_checkpoint_seed, Mapping):
            raise StateCorruptionError(
                "proof terminal recovery claim lacks its checkpoint recovery seed"
            )
        checkpoint_seed = _validate_proof_recovery_seed(
            raw_checkpoint_seed,
            expected_phase="staged_invocation",
        )
    observation = _copy_mapping(
        record["recovery_clock_observation"],
        "proof terminal recovery clock observation",
    )
    if set(observation) != {
        "observation_kind",
        "observation_digest",
        "observed_at",
        "clock_authority",
        "clock_authority_digest",
        "executor_lease_id",
        "executor_lease_digest",
        "lease_expires_at",
        "lease_expired",
        "investment_deadline_revalidation_not_performed",
        "recovery_only",
        "caller_supplied_time_used",
        "pid_only_death_inference_used",
        "respawn_authorized",
    }:
        raise StateCorruptionError(
            "proof terminal recovery clock observation shape is not exact"
        )
    clock = _validate_recovery_clock_authority(
        observation["clock_authority"]
    )
    lease = _validate_executor_lease(
        claim["executor_lease"],
        reservation=reservation,
    )
    observed = _parse_canonical_utc_timestamp(
        observation["observed_at"],
        "proof terminal recovery observed_at",
    )
    expires = _parse_canonical_utc_timestamp(
        lease["expires_at"],
        "proof terminal recovery lease_expires_at",
    )
    terminal_observed_at = (
        observed.replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    selected_reason = (
        "launch_not_observed_abandoned"
        if checkpoint is None
        else "execution_outcome_unknown_abandoned"
    )
    checkpoint_digest = (
        None if checkpoint is None else checkpoint["checkpoint_digest"]
    )
    checkpoint_seed_digest = (
        None if checkpoint_seed is None else checkpoint_seed["seed_digest"]
    )
    expected_id = stable_identifier(
        "proof-terminal-recovery-claim-v1",
        claim["execution_claim_digest"],
        lease["lease_digest"],
        checkpoint_digest,
        validated_claim_seed["seed_digest"],
        checkpoint_seed_digest,
        observation["observation_digest"],
    )
    if (
        record["schema_version"] != "1.0.0"
        or record["record_kind"] != "proof_terminal_recovery_claim"
        or record["recovery_claim_id"] != expected_id
        or record["reservation_id"] != reservation["reservation_id"]
        or record["reservation_digest"] != reservation["reservation_digest"]
        or record["execution_claim_id"] != claim["execution_claim_id"]
        or record["execution_claim_digest"]
        != claim["execution_claim_digest"]
        or record["attempt_id"] != reservation["attempt_id"]
        or record["status"] != PROOF_TERMINAL_RECOVERY_CLAIM_STATUS
        or record["executor_lease_id"] != lease["lease_id"]
        or record["executor_lease_digest"] != lease["lease_digest"]
        or record["launch_boundary_checkpoint_digest"]
        != checkpoint_digest
        or record["claim_recovery_seed_digest"]
        != validated_claim_seed["seed_digest"]
        or record["checkpoint_recovery_seed_digest"]
        != checkpoint_seed_digest
        or observation["observation_kind"]
        != "governed_proof_executor_lease_recovery_observation"
        or observation["clock_authority_digest"]
        != clock["authority_digest"]
        or observation["executor_lease_id"] != lease["lease_id"]
        or observation["executor_lease_digest"] != lease["lease_digest"]
        or observation["lease_expires_at"] != lease["expires_at"]
        or observed < expires
        or observation["lease_expired"] is not True
        or observation[
            "investment_deadline_revalidation_not_performed"
        ] is not True
        or observation["recovery_only"] is not True
        or observation["caller_supplied_time_used"] is not False
        or observation["pid_only_death_inference_used"] is not False
        or observation["respawn_authorized"] is not False
        or observation["observation_digest"]
        != _self_digest(observation, "observation_digest")
        or record["selected_reason_code"] != selected_reason
        or record["terminal_observed_at"] != terminal_observed_at
        or record["claim_remains_spent"] is not True
        or record["respawn_authorized"] is not False
        or record["authority_scope"]
        != "expired_lease_terminalization_only_no_launch_or_respawn"
        or record["recovery_claim_digest"]
        != _self_digest(record, "recovery_claim_digest")
        or len(canonical_json(record)) > MAX_PROOF_RECORD_BYTES
        or isinstance(record["ledger_generation"], bool)
        or not isinstance(record["ledger_generation"], int)
        or record["ledger_generation"] <= claim["ledger_generation"]
        or (
            checkpoint is not None
            and record["ledger_generation"] <= checkpoint["ledger_generation"]
        )
    ):
        raise StateCorruptionError(
            "proof terminal recovery claim is inconsistent"
        )
    return record


def _validate_recovery_abandonment_authority(
    value: object,
    *,
    reservation: Mapping[str, Any],
    claim: Mapping[str, Any],
    recovery_claim: Mapping[str, Any],
    terminal: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay one expired-lease abandonment authority from durable contents."""

    if not isinstance(value, Mapping):
        raise StateCorruptionError(
            "proof recovery abandonment authority must be an object"
        )
    authority = copy.deepcopy(dict(value))
    if set(authority) != {
        "authority_kind",
        "authority_digest",
        "reservation_id",
        "execution_claim_id",
        "execution_claim_digest",
        "recovery_claim_id",
        "recovery_claim_digest",
        "executor_lease",
        "recovery_clock_observation",
        "launch_boundary_checkpoint",
        "selected_reason_code",
        "process_evidence_available",
        "process_evidence_fabrication_allowed",
        "caller_time_authority",
        "pid_only_death_authority",
        "respawn_authorized",
        "proof_authority",
        "theory_mutation_authority",
    }:
        raise StateCorruptionError(
            "proof recovery abandonment authority shape is not exact"
        )
    lease = _validate_executor_lease(
        authority["executor_lease"],
        reservation=reservation,
    )
    observation = _copy_mapping(
        authority["recovery_clock_observation"],
        "proof recovery clock observation",
    )
    if set(observation) != {
        "observation_kind",
        "observation_digest",
        "observed_at",
        "clock_authority",
        "clock_authority_digest",
        "executor_lease_id",
        "executor_lease_digest",
        "lease_expires_at",
        "lease_expired",
        "investment_deadline_revalidation_not_performed",
        "recovery_only",
        "caller_supplied_time_used",
        "pid_only_death_inference_used",
        "respawn_authorized",
    }:
        raise StateCorruptionError(
            "proof recovery clock observation shape is not exact"
        )
    clock = _validate_recovery_clock_authority(
        observation["clock_authority"]
    )
    observed = _parse_canonical_utc_timestamp(
        observation["observed_at"], "proof recovery observed_at"
    )
    expires = _parse_canonical_utc_timestamp(
        observation["lease_expires_at"],
        "proof recovery lease_expires_at",
    )
    raw_checkpoint = authority["launch_boundary_checkpoint"]
    checkpoint = (
        None
        if raw_checkpoint is None
        else _validate_launch_checkpoint(
            raw_checkpoint,
            reservation=reservation,
            claim=claim,
        )
    )
    selected_reason = (
        "launch_not_observed_abandoned"
        if checkpoint is None
        else "execution_outcome_unknown_abandoned"
    )
    if (
        authority["authority_kind"]
        != "expired_executor_lease_abandonment_authority"
        or authority["reservation_id"] != reservation["reservation_id"]
        or authority["execution_claim_id"] != claim["execution_claim_id"]
        or authority["execution_claim_digest"]
        != claim["execution_claim_digest"]
        or authority["recovery_claim_id"]
        != recovery_claim["recovery_claim_id"]
        or authority["recovery_claim_digest"]
        != recovery_claim["recovery_claim_digest"]
        or observation != recovery_claim["recovery_clock_observation"]
        or observation["observation_kind"]
        != "governed_proof_executor_lease_recovery_observation"
        or observation["clock_authority_digest"]
        != clock["authority_digest"]
        or observation["executor_lease_id"] != lease["lease_id"]
        or observation["executor_lease_digest"] != lease["lease_digest"]
        or observation["lease_expires_at"] != lease["expires_at"]
        or observed < expires
        or observation["lease_expired"] is not True
        or observation[
            "investment_deadline_revalidation_not_performed"
        ] is not True
        or observation["recovery_only"] is not True
        or observation["caller_supplied_time_used"] is not False
        or observation["pid_only_death_inference_used"] is not False
        or observation["respawn_authorized"] is not False
        or observation["observation_digest"]
        != _self_digest(observation, "observation_digest")
        or authority["selected_reason_code"] != selected_reason
        or terminal["reason_code"] != selected_reason
        or terminal["started_at"]
        != recovery_claim["terminal_observed_at"]
        or terminal["completed_at"]
        != recovery_claim["terminal_observed_at"]
        or authority["process_evidence_available"] is not False
        or authority[
            "process_evidence_fabrication_allowed"
        ] is not False
        or authority["caller_time_authority"] is not False
        or authority["pid_only_death_authority"] is not False
        or authority["respawn_authorized"] is not False
        or authority["proof_authority"] is not False
        or authority["theory_mutation_authority"] is not False
        or authority["authority_digest"]
        != _self_digest(authority, "authority_digest")
    ):
        raise StateCorruptionError(
            "proof recovery abandonment authority is inconsistent"
        )
    return authority


def _proof_terminal_base_path(attempt_id: str) -> str:
    attempt_id = validate_identifier(attempt_id, "attempt_id")
    return (
        f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
        f"{attempt_id}/terminal"
    )


def _proof_terminal_attachment_descriptors(
    terminal: Mapping[str, Any],
    *,
    attempt_id: str,
) -> list[dict[str, Any]]:
    """Derive the closed attachment set from one inert terminal projection."""

    base = _proof_terminal_base_path(attempt_id)
    descriptors: list[dict[str, Any]] = []

    def add_embedded(
        *,
        field: str,
        digest_field: str,
        attachment_kind: str,
        filename: str,
        role: str,
    ) -> None:
        value = terminal.get(field)
        digest = terminal.get(digest_field)
        if value is None:
            if digest is not None:
                raise ContractError(
                    f"proof terminal {field} digest exists without evidence"
                )
            return
        if not isinstance(value, Mapping):
            raise ContractError(f"proof terminal {field} must be an object")
        data = canonical_json(value)
        if digest != bytes_digest(data):
            raise ContractError(
                f"proof terminal {field} digest differs from its exact bytes"
            )
        descriptors.append(
            {
                "attachment_kind": attachment_kind,
                "logical_name": field,
                "source_relative_path": None,
                "artifact_path": f"{base}/evidence/{filename}",
                "sha256": bytes_digest(data),
                "byte_length": len(data),
                "roles": [role],
                "executable": False,
            }
        )

    add_embedded(
        field="process_event",
        digest_field="process_event_digest",
        attachment_kind="process_event",
        filename="process-event.json",
        role="process_evidence",
    )
    add_embedded(
        field="resource_receipt",
        digest_field="resource_receipt_digest",
        attachment_kind="resource_receipt",
        filename="resource-receipt.json",
        role="resource_evidence",
    )
    add_embedded(
        field="certificate",
        digest_field="certificate_digest",
        attachment_kind="certificate",
        filename="certificate.json",
        role="certificate",
    )

    checker = terminal.get("checker_output")
    if checker is not None:
        if not isinstance(checker, Mapping) or set(checker) != {
            "sha256",
            "byte_length",
            "canonical_response_accepted",
        }:
            raise ContractError(
                "proof terminal checker-output descriptor shape is not exact"
            )
        validate_digest(checker["sha256"])
        if (
            isinstance(checker["byte_length"], bool)
            or not isinstance(checker["byte_length"], int)
            or checker["byte_length"] < 0
            or type(checker["canonical_response_accepted"]) is not bool
        ):
            raise ContractError(
                "proof terminal checker-output descriptor is invalid"
            )
        descriptors.append(
            {
                "attachment_kind": "checker_output",
                "logical_name": "checker_output",
                "source_relative_path": None,
                "artifact_path": f"{base}/evidence/checker-output.bin",
                "sha256": checker["sha256"],
                "byte_length": checker["byte_length"],
                "roles": ["checker_output"],
                "executable": False,
            }
        )

    artifacts = terminal.get("artifacts")
    if not isinstance(artifacts, list):
        raise ContractError("proof terminal artifacts must be a list")
    if len(artifacts) > MAX_PROOF_TERMINAL_ATTACHMENTS - 4:
        raise ContractError("proof terminal artifact count exceeds its ceiling")
    paths: list[str] = []
    for raw in artifacts:
        if not isinstance(raw, Mapping) or set(raw) != {
            "relative_path",
            "roles",
            "sha256",
            "byte_length",
            "executable",
        }:
            raise ContractError(
                "proof terminal result-artifact descriptor shape is not exact"
            )
        relative_path = safe_relative_path(
            raw["relative_path"], forbid_latest=True
        ).as_posix()
        if relative_path != raw["relative_path"]:
            raise ContractError(
                "proof terminal result-artifact path is not canonical"
            )
        roles = raw["roles"]
        if (
            not isinstance(roles, list)
            or any(not isinstance(role, str) or not role for role in roles)
            or roles != sorted(set(roles))
            or "result_artifact" not in roles
            or raw["executable"] is not False
            or isinstance(raw["byte_length"], bool)
            or not isinstance(raw["byte_length"], int)
            or raw["byte_length"] < 0
        ):
            raise ContractError(
                "proof terminal result-artifact descriptor is invalid"
            )
        validate_digest(raw["sha256"])
        paths.append(relative_path)
        descriptors.append(
            {
                "attachment_kind": "result_artifact",
                "logical_name": f"result_artifact/{relative_path}",
                "source_relative_path": relative_path,
                "artifact_path": (
                    f"{base}/evidence/result-artifacts/{relative_path}"
                ),
                "sha256": raw["sha256"],
                "byte_length": raw["byte_length"],
                "roles": list(roles),
                "executable": False,
            }
        )
    if paths != sorted(set(paths)):
        raise ContractError(
            "proof terminal result-artifact paths are not canonical and unique"
        )
    descriptors.sort(key=lambda row: str(row["logical_name"]))
    if (
        len(descriptors) > MAX_PROOF_TERMINAL_ATTACHMENTS
        or len({row["logical_name"] for row in descriptors})
        != len(descriptors)
        or len({row["artifact_path"] for row in descriptors})
        != len(descriptors)
        or sum(int(row["byte_length"]) for row in descriptors)
        > MAX_PROOF_TERMINAL_ATTACHMENT_BYTES
    ):
        raise ContractError("proof terminal attachment set exceeds its ceiling")
    return descriptors


def _proof_terminal_replay_attachment_descriptors(
    replay_bytes: Mapping[str, bytes],
    *,
    attempt_id: str,
) -> list[dict[str, Any]]:
    """Describe exact private typed-construction bytes without granting launch."""

    base = _proof_terminal_base_path(attempt_id)
    descriptors: list[dict[str, Any]] = []
    for logical_name, supplied in sorted(replay_bytes.items()):
        if not logical_name.startswith(_TYPED_TERMINAL_REPLAY_PREFIX):
            continue
        canonical_name = safe_relative_path(
            logical_name, forbid_latest=True
        ).as_posix()
        if canonical_name != logical_name or type(supplied) is not bytes:
            raise ContractError(
                "proof terminal typed-replay attachment is not exact"
            )
        data = memoryview(supplied).tobytes()
        source_relative_path = (
            logical_name.removeprefix(
                "typed_replay/invocation/files/"
            )
            if logical_name.startswith(
                "typed_replay/invocation/files/"
            )
            else None
        )
        descriptors.append(
            {
                "attachment_kind": "typed_terminal_replay",
                "logical_name": logical_name,
                "source_relative_path": source_relative_path,
                "artifact_path": f"{base}/{logical_name}",
                "sha256": bytes_digest(data),
                "byte_length": len(data),
                "roles": ["typed_terminal_replay"],
                "executable": False,
            }
        )
    if not _TYPED_TERMINAL_REPLAY_BINDING_NAMES.issubset(
        {str(row["logical_name"]) for row in descriptors}
    ):
        raise ContractError(
            "proof terminal lacks its exact durable claim-binding bytes"
        )
    return descriptors


def _proof_recovery_seed_attachment_descriptors(
    attachment_bytes: Mapping[str, bytes],
    *,
    attempt_id: str,
    seed_phase: str,
) -> list[dict[str, Any]]:
    """Describe one bounded inert recovery seed committed before any spawn."""

    if seed_phase not in {"claim_binding", "staged_invocation"}:
        raise ContractError("proof recovery seed phase is unregistered")
    if not isinstance(attachment_bytes, Mapping):
        raise ContractError("proof recovery seed attachment bytes must be an object")
    base = (
        f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
        f"{validate_identifier(attempt_id, 'attempt_id')}/recovery-seed/"
        f"{seed_phase}"
    )
    descriptors: list[dict[str, Any]] = []
    for logical_name, supplied in sorted(attachment_bytes.items()):
        canonical_name = safe_relative_path(
            logical_name, forbid_latest=True
        ).as_posix()
        if (
            canonical_name != logical_name
            or type(supplied) is not bytes
        ):
            raise ContractError(
                "proof recovery seed attachment is not exact"
            )
        data = memoryview(supplied).tobytes()
        source_relative_path = (
            logical_name.removeprefix(
                _PROOF_INVOCATION_RECOVERY_FILE_PREFIX
            )
            if logical_name.startswith(
                _PROOF_INVOCATION_RECOVERY_FILE_PREFIX
            )
            else None
        )
        descriptors.append(
            {
                "attachment_kind": "proof_recovery_seed",
                "logical_name": logical_name,
                "source_relative_path": source_relative_path,
                "artifact_path": f"{base}/{logical_name}",
                "sha256": bytes_digest(data),
                "byte_length": len(data),
                "roles": ["proof_recovery_seed"],
                "executable": False,
            }
        )
    return descriptors


def _build_proof_recovery_seed(
    attachment_bytes: Mapping[str, bytes],
    *,
    attempt_id: str,
    seed_phase: str,
) -> dict[str, Any]:
    descriptors = _proof_recovery_seed_attachment_descriptors(
        attachment_bytes,
        attempt_id=attempt_id,
        seed_phase=seed_phase,
    )
    seed: dict[str, Any] = {
        "schema_version": "1.0.0",
        "seed_kind": "bounded_inert_proof_terminal_recovery_seed",
        "seed_phase": seed_phase,
        "attachment_descriptors": descriptors,
        "attachment_set_digest": canonical_digest(descriptors),
        "attachment_count": len(descriptors),
        "total_bytes": sum(int(row["byte_length"]) for row in descriptors),
        "maximum_combined_recovery_seed_bytes": (
            MAX_PROOF_RECOVERY_SEED_BYTES
        ),
        "reconstructible_from_verified_commit": True,
        "serialized_launch_authority": False,
        "respawn_authorized": False,
    }
    seed["seed_digest"] = _self_digest(seed, "seed_digest")
    return _validate_proof_recovery_seed(seed, expected_phase=seed_phase)


def _validate_proof_recovery_seed(
    value: object,
    *,
    expected_phase: str,
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise StateCorruptionError("proof recovery seed must be an object")
    seed = copy.deepcopy(dict(value))
    if set(seed) != {
        "schema_version",
        "seed_kind",
        "seed_phase",
        "attachment_descriptors",
        "attachment_set_digest",
        "attachment_count",
        "total_bytes",
        "maximum_combined_recovery_seed_bytes",
        "reconstructible_from_verified_commit",
        "serialized_launch_authority",
        "respawn_authorized",
        "seed_digest",
    }:
        raise StateCorruptionError("proof recovery seed shape is not exact")
    descriptors = seed["attachment_descriptors"]
    if not isinstance(descriptors, list):
        raise StateCorruptionError(
            "proof recovery seed descriptors must be an array"
        )
    if any(
        not isinstance(row, Mapping)
        or isinstance(row.get("byte_length"), bool)
        or not isinstance(row.get("byte_length"), int)
        or int(row["byte_length"]) < 0
        for row in descriptors
    ):
        raise StateCorruptionError(
            "proof recovery seed descriptor is invalid"
        )
    logical_names = [str(row.get("logical_name", "")) for row in descriptors]
    artifact_paths = [str(row.get("artifact_path", "")) for row in descriptors]
    if (
        seed["schema_version"] != "1.0.0"
        or seed["seed_kind"]
        != "bounded_inert_proof_terminal_recovery_seed"
        or seed["seed_phase"] != expected_phase
        or descriptors
        != sorted(descriptors, key=lambda row: str(row.get("logical_name", "")))
        or len(descriptors) > MAX_PROOF_RECOVERY_SEED_ATTACHMENTS
        or len(logical_names) != len(set(logical_names))
        or len(artifact_paths) != len(set(artifact_paths))
        or seed["attachment_count"] != len(descriptors)
        or seed["total_bytes"]
        != sum(int(row["byte_length"]) for row in descriptors)
        or seed["total_bytes"] > MAX_PROOF_RECOVERY_SEED_BYTES
        or seed["maximum_combined_recovery_seed_bytes"]
        != MAX_PROOF_RECOVERY_SEED_BYTES
        or seed["attachment_set_digest"] != canonical_digest(descriptors)
        or seed["reconstructible_from_verified_commit"] is not True
        or seed["serialized_launch_authority"] is not False
        or seed["respawn_authorized"] is not False
        or seed["seed_digest"] != _self_digest(seed, "seed_digest")
    ):
        raise StateCorruptionError("proof recovery seed is inconsistent")
    names = set(logical_names)
    if expected_phase == "claim_binding":
        if names != _PROOF_CLAIM_RECOVERY_SEED_NAMES:
            raise StateCorruptionError(
                "proof claim recovery seed coverage is not exact"
            )
    elif (
        not _PROOF_INVOCATION_RECOVERY_FIXED_NAMES.issubset(names)
        or any(
            name not in _PROOF_INVOCATION_RECOVERY_FIXED_NAMES
            and not name.startswith(
                _PROOF_INVOCATION_RECOVERY_FILE_PREFIX
            )
            for name in names
        )
    ):
        raise StateCorruptionError(
            "proof invocation recovery seed coverage is not exact"
        )
    for row in descriptors:
        if (
            not isinstance(row, Mapping)
            or set(row)
            != {
                "attachment_kind",
                "logical_name",
                "source_relative_path",
                "artifact_path",
                "sha256",
                "byte_length",
                "roles",
                "executable",
            }
            or row["attachment_kind"] != "proof_recovery_seed"
            or safe_relative_path(
                row["logical_name"], forbid_latest=True
            ).as_posix()
            != row["logical_name"]
            or row["roles"] != ["proof_recovery_seed"]
            or row["executable"] is not False
            or isinstance(row["byte_length"], bool)
            or not isinstance(row["byte_length"], int)
            or row["byte_length"] < 0
        ):
            raise StateCorruptionError(
                "proof recovery seed descriptor is invalid"
            )
        validate_digest(row["sha256"])
    return seed


def _validated_proof_recovery_seed_artifacts(
    seed: Mapping[str, Any],
    attachment_bytes: Mapping[str, bytes],
) -> tuple[tuple[str, bytes], ...]:
    expected_names = {
        str(row["logical_name"]) for row in seed["attachment_descriptors"]
    }
    if set(attachment_bytes) != expected_names:
        raise ContractError(
            "proof recovery seed bytes do not exactly cover its descriptors"
        )
    frozen: list[tuple[str, bytes]] = []
    for row in seed["attachment_descriptors"]:
        logical_name = str(row["logical_name"])
        supplied = attachment_bytes[logical_name]
        if type(supplied) is not bytes:
            raise ContractError(
                "proof recovery seed attachment must be exact bytes"
            )
        data = memoryview(supplied).tobytes()
        if (
            bytes_digest(data) != row["sha256"]
            or len(data) != row["byte_length"]
        ):
            raise ContractError(
                "proof recovery seed bytes differ from their descriptor"
            )
        frozen.append((str(row["artifact_path"]), data))
    return tuple(frozen)


def _validated_proof_terminal_attachment_bytes(
    terminal: Mapping[str, Any],
    descriptors: Sequence[Mapping[str, Any]],
    attachment_bytes: Mapping[str, bytes],
) -> tuple[tuple[str, bytes], ...]:
    """Bind every declared terminal descriptor to one exact immutable byte value."""

    if not isinstance(attachment_bytes, Mapping):
        raise ContractError("proof terminal attachment_bytes must be an object")
    expected_names = {str(row["logical_name"]) for row in descriptors}
    if set(attachment_bytes) != expected_names:
        raise ContractError(
            "proof terminal attachment bytes do not exactly cover its descriptors"
        )
    embedded_fields = {
        "process_event": "process_event",
        "resource_receipt": "resource_receipt",
        "certificate": "certificate",
    }
    frozen: list[tuple[str, bytes]] = []
    for descriptor in descriptors:
        logical_name = str(descriptor["logical_name"])
        supplied = attachment_bytes[logical_name]
        if type(supplied) is not bytes:
            raise ContractError(
                f"proof terminal attachment {logical_name!r} must be exact bytes"
            )
        data = memoryview(supplied).tobytes()
        if (
            bytes_digest(data) != descriptor["sha256"]
            or len(data) != descriptor["byte_length"]
        ):
            raise ContractError(
                f"proof terminal attachment {logical_name!r} differs from its descriptor"
            )
        embedded_field = embedded_fields.get(logical_name)
        if (
            embedded_field is not None
            and data != canonical_json(terminal[embedded_field])
        ):
            raise ContractError(
                f"proof terminal attachment {logical_name!r} differs from embedded evidence"
            )
        frozen.append((str(descriptor["artifact_path"]), data))
    return tuple(frozen)


def _proof_terminal_derived_artifact_descriptors(
    *,
    attempt_id: str,
    terminal_receipt: Mapping[str, Any],
    receipt_index_membership: Mapping[str, Any],
    pending_n_plus_one_reflection_request: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Describe the three derived records committed beside the terminal bundle."""

    base = _proof_terminal_base_path(attempt_id)
    values = {
        "terminal_receipt": (
            f"{base}/terminal-receipt.json",
            terminal_receipt,
        ),
        "receipt_index_membership": (
            f"{base}/terminal-index-membership.json",
            receipt_index_membership,
        ),
        "pending_n_plus_one_reflection_request": (
            f"{base}/pending-n-plus-one-reflection-request.json",
            pending_n_plus_one_reflection_request,
        ),
    }
    descriptors: list[dict[str, Any]] = []
    for artifact_kind, (artifact_path, value) in sorted(values.items()):
        data = canonical_json(value)
        descriptors.append(
            {
                "artifact_kind": artifact_kind,
                "artifact_path": artifact_path,
                "sha256": bytes_digest(data),
                "byte_length": len(data),
            }
        )
    return descriptors


def _proof_terminal_request_digest(
    *,
    reservation: Mapping[str, Any],
    claim: Mapping[str, Any],
    terminal_projection_digest: str,
    attachment_set_digest: str,
) -> str:
    return canonical_digest(
        {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "request_kind": "finalize_one_claimed_proof_attempt",
            "reservation_id": reservation["reservation_id"],
            "reservation_digest": reservation["reservation_digest"],
            "execution_claim_id": claim["execution_claim_id"],
            "execution_claim_digest": claim["execution_claim_digest"],
            "terminal_projection_digest": terminal_projection_digest,
            "attachment_set_digest": attachment_set_digest,
        }
    )


def _durable_json_size(value: Mapping[str, Any]) -> int:
    return len(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ) + 1


def _validate_failpoint(failpoint: str | None) -> str | None:
    if failpoint is None:
        return None
    if type(failpoint) is not str:
        raise ContractError("coordination failpoint must be a name, not a callback")
    if failpoint not in _NAMED_FAILPOINTS:
        raise ContractError(f"unknown coordination failpoint: {failpoint!r}")
    return failpoint


def _validate_identifier_sequence(
    values: Sequence[str],
    *,
    label: str,
    ceiling: int,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ContractError(f"{label} must be a sequence")
    if not values:
        raise ContractError(f"{label} must be non-empty")
    if len(values) > ceiling:
        raise ContractError(f"{label} exceeds its fixed count ceiling")
    normalized = tuple(
        sorted(validate_identifier(value, label.rstrip("s")) for value in values)
    )
    if len(set(normalized)) != len(normalized):
        raise ContractError(f"{label} must be unique")
    return normalized


def _validate_digest_sequence(
    values: Sequence[str], *, label: str, ceiling: int
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ContractError(f"{label} must be a sequence")
    if len(values) > ceiling:
        raise ContractError(f"{label} exceeds its fixed count ceiling")
    copied: list[str] = []
    for value in values:
        validate_digest(value)
        copied.append(value)
    normalized = tuple(sorted(copied))
    if len(set(normalized)) != len(normalized):
        raise ContractError(f"{label} must be unique")
    return normalized


def _roots_are_disjoint(left: Path, right: Path) -> bool:
    return (
        left != right
        and left not in right.parents
        and right not in left.parents
    )


def _head_observation(commit: VerifiedCommit) -> dict[str, Any]:
    observation: dict[str, Any] = {
        "observation_kind": "verified_current_theory_head",
        "target_id": commit.state["target_id"],
        "run_id": commit.state["run_id"],
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
    }
    observation["head_digest"] = _self_digest(observation, "head_digest")
    return observation


def _validate_head_observation(
    observation: Mapping[str, Any], *, target_id: str, run_id: str
) -> dict[str, Any]:
    record = _copy_mapping(observation, "theory-head observation")
    if set(record) != {
        "observation_kind",
        "target_id",
        "run_id",
        "generation",
        "prior_generation",
        "commit_id",
        "manifest_digest",
        "state_file_digest",
        "state_semantic_digest",
        "head_digest",
    }:
        raise StateCorruptionError("theory-head observation shape is not exact")
    if (
        record["observation_kind"] != "verified_current_theory_head"
        or record["target_id"] != target_id
        or record["run_id"] != run_id
        or isinstance(record["generation"], bool)
        or not isinstance(record["generation"], int)
        or record["generation"] <= 0
        or record["prior_generation"] != record["generation"] - 1
        or record["head_digest"] != _self_digest(record, "head_digest")
    ):
        raise StateCorruptionError("theory-head observation is inconsistent")
    validate_identifier(record["commit_id"], "theory commit_id")
    for field in (
        "manifest_digest",
        "state_file_digest",
        "state_semantic_digest",
        "head_digest",
    ):
        validate_digest(record[field])
    return record


def _record_path(record: Mapping[str, Any]) -> str:
    reservation_id = str(record.get("reservation_id", ""))
    if record["record_kind"] == "action_reservation":
        return f"branches/{_COORDINATION_BRANCH_ID}/reservations/{reservation_id}.json"
    if record["record_kind"] == "action_reservation_terminal":
        return f"branches/{_COORDINATION_BRANCH_ID}/terminals/{reservation_id}.json"
    if record["record_kind"] == "proof_attempt_reservation":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/reservation.json"
        )
    if record["record_kind"] == "proof_execution_claim":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/execution-claim.json"
        )
    if record["record_kind"] == "proof_launch_boundary_checkpoint":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/launch-boundary-checkpoint.json"
        )
    if record["record_kind"] == "proof_terminal_recovery_claim":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/terminal-recovery-claim.json"
        )
    if record["record_kind"] == "proof_execution_terminal_bundle":
        return f"{_proof_terminal_base_path(str(record['attempt_id']))}/terminal-bundle.json"
    if record["record_kind"] == "proof_result_intake_claim":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/result-intake-claim.json"
        )
    if record["record_kind"] == "proof_result_intake_consumption":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/result-intake-consumption.json"
        )
    if record["record_kind"] == "proof_result_intake_supersession":
        return (
            f"branches/{_COORDINATION_BRANCH_ID}/proof-attempts/"
            f"{record['attempt_id']}/result-intake-supersession.json"
        )
    raise StateCorruptionError("unknown coordination record kind")


class ActionCoordinationLedger:
    """CAS/idempotent operational ledger over a read-only theory dependency."""

    def __init__(
        self,
        *,
        theory_store: DiscoveryTransactionStore,
        coordination_root: Path,
    ) -> None:
        if type(theory_store) is not DiscoveryTransactionStore:
            raise ContractError("theory_store must be an exact DiscoveryTransactionStore")
        root = Path(coordination_root).resolve()
        if not _roots_are_disjoint(theory_store.root, root):
            raise CoordinationStoreBoundaryError(
                "coordination root must be disjoint from the theory store root"
            )
        self._theory_store = theory_store
        self._coordination_root = root
        self._store = DiscoveryTransactionStore(
            root,
            target_id=theory_store.target_id,
            run_id=theory_store.run_id,
        )

    @property
    def coordination_root(self) -> Path:
        """Return the runtime-local store root; it is never serialized."""

        return self._coordination_root

    @property
    def coordination_run_root(self) -> Path:
        """Return the runtime-local run root for diagnostics and governance."""

        return self._store.run_root

    def current_generation(self) -> int:
        return self._store.current_generation()

    def _current_theory_head(self) -> dict[str, Any]:
        lock = _THEORY_CONTEXT_LOCKS.setdefault(
            (os.getpid(), id(self._theory_store)),
            threading.RLock(),
        )
        with lock:
            with self._theory_store.verified_artifact_context() as context:
                generation = context.current_generation
                if generation <= 0:
                    raise TheoryHeadBindingError(
                        "action coordination requires an initialized theory head"
                    )
                return _head_observation(context.read_commit(generation))

    def _require_current_theory_head(
        self, expected: Mapping[str, Any]
    ) -> dict[str, Any]:
        expected_record = _validate_head_observation(
            expected,
            target_id=self._theory_store.target_id,
            run_id=self._theory_store.run_id,
        )
        observed = self._current_theory_head()
        if observed != expected_record:
            raise TheoryHeadBindingError(
                "theory head changed before the coordination reservation"
            )
        return observed

    def _freeze_theory_binding(
        self,
        *,
        theory_commit_reference: Mapping[str, Any],
        theory_graph_reference: Mapping[str, Any],
        n_plus_7_support_root_references: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        commit_reference = _copy_mapping(
            theory_commit_reference, "theory commit reference"
        )
        graph_reference = _copy_mapping(
            theory_graph_reference, "theory graph reference"
        )
        for label, value in (
            ("theory commit reference", commit_reference),
            ("theory graph reference", graph_reference),
        ):
            if len(canonical_json(value)) > MAX_REFERENCE_BYTES:
                raise ContractError(f"{label} exceeds the fixed reference-byte ceiling")
        if (
            isinstance(n_plus_7_support_root_references, (str, bytes))
            or not isinstance(n_plus_7_support_root_references, Sequence)
        ):
            raise ContractError("N+7 support root references must be a sequence")
        if len(n_plus_7_support_root_references) > MAX_SUPPORT_ROOT_REFERENCES:
            raise ContractError("N+7 support references exceed the fixed count ceiling")
        support_references = tuple(
            _copy_mapping(row, "N+7 support root reference")
            for row in n_plus_7_support_root_references
        )
        support_keys: list[bytes] = []
        for reference in support_references:
            data = canonical_json(reference)
            if len(data) > MAX_REFERENCE_BYTES:
                raise ContractError(
                    "N+7 support reference exceeds the fixed reference-byte ceiling"
                )
            support_keys.append(data)
        if len(set(support_keys)) != len(support_keys):
            raise ContractError("N+7 support root references must be unique")

        try:
            generation = commit_reference["generation"]
            graph_path = commit_reference["graph_artifact"]["path"]
            reopened = reopen_content_graph_transaction(
                store=self._theory_store,
                generation=generation,
                graph_artifact_path=graph_path,
            )
        except (KeyError, TypeError, ContractError) as exc:
            raise TheoryHeadBindingError(
                "theory references do not reopen the exact current content graph"
            ) from exc
        if (
            reopened.commit_ref != commit_reference
            or reopened.graph_ref != graph_reference
        ):
            raise TheoryHeadBindingError(
                "theory commit/graph references differ from verified current bytes"
            )
        available_roots = {
            canonical_json(reference): reference for reference in reopened.root_refs
        }
        if any(key not in available_roots for key in support_keys):
            raise TheoryHeadBindingError(
                "an N+7 support reference is not an exact root of the theory graph"
            )
        observation = self._current_theory_head()
        if observation["generation"] != generation:
            raise TheoryHeadBindingError(
                "theory head changed while its graph binding was being verified"
            )
        reference_identity = (
            commit_reference.get("commit_id"),
            commit_reference.get("manifest_digest"),
            commit_reference.get("state_file_digest"),
            commit_reference.get("state_semantic_digest"),
        )
        observed_identity = (
            observation["commit_id"],
            observation["manifest_digest"],
            observation["state_file_digest"],
            observation["state_semantic_digest"],
        )
        if reference_identity != observed_identity:
            raise TheoryHeadBindingError(
                "theory commit reference differs from the observed current head"
            )
        binding: dict[str, Any] = {
            "binding_kind": "exact_current_theory_content_graph",
            "commit_reference": commit_reference,
            "graph_reference": graph_reference,
            "n_plus_7_support_root_references": list(support_references),
            "observed_head": observation,
        }
        binding["binding_digest"] = _self_digest(binding, "binding_digest")
        if len(canonical_json(binding)) > MAX_THEORY_BINDING_BYTES:
            raise ContractError("theory binding exceeds the fixed byte ceiling")
        return binding

    def _empty_state(self) -> dict[str, Any]:
        return {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "ledger_kind": LEDGER_KIND,
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "generation": 0,
            "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
            "reservations": {},
            "terminal_records": {},
            "proof_attempt_reservations": {},
            "proof_execution_claims": {},
            "proof_launch_checkpoints": {},
            "proof_terminal_recovery_claims": {},
            "proof_terminal_bundles": {},
            "proof_result_intake_claims": {},
            "proof_result_intake_consumptions": {},
            "proof_result_intake_resolutions": {},
            "action_claims": {},
            "attempt_claims": {},
            "record_count": 0,
        }

    def _load_state(self) -> tuple[int, dict[str, Any]]:
        state = self._store.read_state()
        if state is None:
            return 0, self._empty_state()
        record = copy.deepcopy(state)
        self._validate_state(record)
        if record["schema_version"] == LEGACY_LEDGER_SCHEMA_VERSION:
            record["schema_version"] = LEDGER_SCHEMA_VERSION
            record["proof_attempt_reservations"] = {}
            record["proof_execution_claims"] = {}
            record["proof_terminal_bundles"] = {}
            record["proof_result_intake_claims"] = {}
            record["proof_result_intake_consumptions"] = {}
            record["proof_result_intake_resolutions"] = {}
            record["attempt_claims"] = {}
        record.setdefault("proof_launch_checkpoints", {})
        record.setdefault("proof_terminal_recovery_claims", {})
        record.setdefault("proof_result_intake_claims", {})
        record.setdefault("proof_result_intake_consumptions", {})
        record.setdefault("proof_result_intake_resolutions", {})
        return int(record["generation"]), record

    def _validate_theory_binding(self, value: Mapping[str, Any]) -> dict[str, Any]:
        binding = _copy_mapping(value, "stored theory binding")
        if set(binding) != {
            "binding_kind",
            "commit_reference",
            "graph_reference",
            "n_plus_7_support_root_references",
            "observed_head",
            "binding_digest",
        }:
            raise StateCorruptionError("stored theory binding shape is not exact")
        if (
            binding["binding_kind"] != "exact_current_theory_content_graph"
            or binding["binding_digest"] != _self_digest(binding, "binding_digest")
            or len(canonical_json(binding)) > MAX_THEORY_BINDING_BYTES
        ):
            raise StateCorruptionError("stored theory binding is invalid")
        _validate_head_observation(
            binding["observed_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        if not isinstance(binding["n_plus_7_support_root_references"], list):
            raise StateCorruptionError("stored support references are not an array")
        if len(binding["n_plus_7_support_root_references"]) > MAX_SUPPORT_ROOT_REFERENCES:
            raise StateCorruptionError("stored support reference ceiling was exceeded")
        for reference in (
            binding["commit_reference"],
            binding["graph_reference"],
            *binding["n_plus_7_support_root_references"],
        ):
            if not isinstance(reference, Mapping) or len(canonical_json(reference)) > MAX_REFERENCE_BYTES:
                raise StateCorruptionError("stored compact reference is invalid")
        return binding

    def _validate_reservation_record(
        self, value: Mapping[str, Any], *, expected_id: str
    ) -> dict[str, Any]:
        record = _copy_mapping(value, "stored action reservation")
        if set(record) != {
            "schema_version",
            "record_kind",
            "reservation_id",
            "target_id",
            "run_id",
            "ledger_generation",
            "consumer_id",
            "schedule_id",
            "schedule_digest",
            "action_ids",
            "theory_binding",
            "status",
            "reservation_request_digest",
            "authority_boundary",
            "reservation_digest",
        }:
            raise StateCorruptionError("stored reservation shape is not exact")
        if (
            record["schema_version"]
            not in {LEGACY_LEDGER_SCHEMA_VERSION, LEDGER_SCHEMA_VERSION}
            or record["record_kind"] != "action_reservation"
            or record["reservation_id"] != expected_id
            or record["target_id"] != self._store.target_id
            or record["run_id"] != self._store.run_id
            or record["status"] != RESERVATION_STATUS
            or record["authority_boundary"] != _AUTHORITY_BOUNDARY
            or record["reservation_digest"]
            != _self_digest(record, "reservation_digest")
            or len(canonical_json(record)) > MAX_RECORD_BYTES
        ):
            raise StateCorruptionError("stored reservation is inconsistent")
        validate_identifier(record["reservation_id"], "reservation_id")
        validate_identifier(record["consumer_id"], "consumer_id")
        validate_identifier(record["schedule_id"], "schedule_id")
        validate_digest(record["schedule_digest"])
        validate_digest(record["reservation_request_digest"])
        if (
            isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= 0
            or not isinstance(record["action_ids"], list)
            or not record["action_ids"]
            or len(record["action_ids"]) > MAX_ACTIONS_PER_RESERVATION
            or record["action_ids"] != sorted(record["action_ids"])
            or len(set(record["action_ids"])) != len(record["action_ids"])
        ):
            raise StateCorruptionError("stored reservation action vector is invalid")
        for action_id in record["action_ids"]:
            validate_identifier(action_id, "action_id")
        self._validate_theory_binding(record["theory_binding"])
        return record

    def _validate_terminal_record(
        self,
        value: Mapping[str, Any],
        *,
        reservation: Mapping[str, Any],
    ) -> dict[str, Any]:
        record = _copy_mapping(value, "stored action terminal")
        if set(record) != {
            "schema_version",
            "record_kind",
            "terminal_id",
            "reservation_id",
            "reservation_digest",
            "target_id",
            "run_id",
            "ledger_generation",
            "requested_terminal_status",
            "status",
            "terminal_evidence_digests",
            "theory_head_recheck",
            "terminal_request_digest",
            "authority_boundary",
            "terminal_digest",
        }:
            raise StateCorruptionError("stored terminal shape is not exact")
        if (
            record["schema_version"]
            not in {LEGACY_LEDGER_SCHEMA_VERSION, LEDGER_SCHEMA_VERSION}
            or record["record_kind"] != "action_reservation_terminal"
            or record["reservation_id"] != reservation["reservation_id"]
            or record["reservation_digest"] != reservation["reservation_digest"]
            or record["target_id"] != self._store.target_id
            or record["run_id"] != self._store.run_id
            or record["requested_terminal_status"] not in TERMINAL_STATUSES
            or record["status"]
            not in TERMINAL_STATUSES | {REBASE_REQUIRED_STATUS}
            or record["authority_boundary"] != _AUTHORITY_BOUNDARY
            or record["terminal_digest"] != _self_digest(record, "terminal_digest")
            or len(canonical_json(record)) > MAX_RECORD_BYTES
        ):
            raise StateCorruptionError("stored terminal is inconsistent")
        validate_identifier(record["terminal_id"], "terminal_id")
        validate_digest(record["terminal_request_digest"])
        evidence = record["terminal_evidence_digests"]
        if (
            not isinstance(evidence, list)
            or evidence != sorted(evidence)
            or len(evidence) > MAX_TERMINAL_EVIDENCE_DIGESTS
            or len(set(evidence)) != len(evidence)
        ):
            raise StateCorruptionError("stored terminal evidence vector is invalid")
        for digest in evidence:
            validate_digest(digest)
        recheck = _copy_mapping(
            record["theory_head_recheck"], "stored theory-head recheck"
        )
        if set(recheck) != {
            "recheck_kind",
            "expected_head",
            "observed_head",
            "match",
            "disposition_reason",
            "recheck_digest",
        }:
            raise StateCorruptionError("stored theory-head recheck shape is not exact")
        expected = _validate_head_observation(
            recheck["expected_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        observed = _validate_head_observation(
            recheck["observed_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        matches = expected == observed
        if (
            recheck["recheck_kind"] != "mandatory_theory_head_recheck"
            or recheck["match"] is not matches
            or recheck["disposition_reason"]
            != ("head_unchanged" if matches else "theory_head_drift")
            or recheck["recheck_digest"] != _self_digest(recheck, "recheck_digest")
            or (matches and record["status"] != record["requested_terminal_status"])
            or (not matches and record["status"] != REBASE_REQUIRED_STATUS)
        ):
            raise StateCorruptionError("stored theory-head recheck is inconsistent")
        return record

    def _validate_proof_source_binding(
        self, value: Mapping[str, Any]
    ) -> dict[str, Any]:
        binding = _copy_mapping(value, "stored proof source binding")
        if set(binding) != {
            "binding_kind",
            "theory_authorization_digest",
            "theory_authorization_basis_digest",
            "literature_authority_basis_digest",
            "source_commit_id",
            "source_manifest_digest",
            "source_state_file_digest",
            "source_state_semantic_digest",
            "observed_head",
            "binding_digest",
        }:
            raise StateCorruptionError("stored proof source binding shape is not exact")
        observed = _validate_head_observation(
            binding["observed_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        if (
            binding["binding_kind"] != "exact_current_postcommit_proof_action"
            or binding["binding_digest"] != _self_digest(binding, "binding_digest")
            or binding["source_commit_id"] != observed["commit_id"]
            or binding["source_manifest_digest"] != observed["manifest_digest"]
            or binding["source_state_file_digest"] != observed["state_file_digest"]
            or binding["source_state_semantic_digest"]
            != observed["state_semantic_digest"]
        ):
            raise StateCorruptionError("stored proof source binding is invalid")
        for field in (
            "theory_authorization_digest",
            "theory_authorization_basis_digest",
            "literature_authority_basis_digest",
            "source_manifest_digest",
            "source_state_file_digest",
            "source_state_semantic_digest",
            "binding_digest",
        ):
            validate_digest(binding[field])
        return binding

    def _validate_proof_reservation_record(
        self, value: Mapping[str, Any], *, expected_id: str
    ) -> dict[str, Any]:
        record = _copy_mapping(value, "stored proof-attempt reservation")
        if set(record) != {
            "schema_version",
            "record_kind",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "target_id",
            "run_id",
            "ledger_generation",
            "status",
            "source_theory_binding",
            "schedule_id",
            "schedule_digest",
            "action_id",
            "action_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "formal_claim_authority_id",
            "formal_claim_authority_digest",
            "producer_receipt_id",
            "producer_receipt_digest",
            "literature_consume_before",
            "proof_runtime_ref",
            "resource_budget",
            "resource_budget_digest",
            "reservation_request_digest",
            "authority_boundary",
        }:
            raise StateCorruptionError("stored proof reservation shape is not exact")
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"] != "proof_attempt_reservation"
            or record["reservation_id"] != expected_id
            or record["target_id"] != self._store.target_id
            or record["run_id"] != self._store.run_id
            or record["status"] != PROOF_RESERVATION_STATUS
            or record["authority_boundary"] != _PROOF_COORDINATION_BOUNDARY
            or record["reservation_digest"]
            != _self_digest(record, "reservation_digest")
            or record["resource_budget_digest"]
            != canonical_digest(record["resource_budget"])
            or safe_relative_path(record["proof_runtime_ref"]).as_posix()
            != record["proof_runtime_ref"]
            or len(canonical_json(record)) > MAX_RECORD_BYTES
        ):
            raise StateCorruptionError("stored proof reservation is inconsistent")
        for field in (
            "reservation_id",
            "execution_claim_id",
            "schedule_id",
            "action_id",
            "attempt_id",
            "handoff_id",
            "formal_claim_authority_id",
            "producer_receipt_id",
        ):
            validate_identifier(record[field], field)
        for field in (
            "reservation_digest",
            "schedule_digest",
            "action_digest",
            "handoff_digest",
            "formal_claim_authority_digest",
            "producer_receipt_digest",
            "resource_budget_digest",
            "reservation_request_digest",
        ):
            validate_digest(record[field])
        if (
            isinstance(record["attempt_number"], bool)
            or not isinstance(record["attempt_number"], int)
            or record["attempt_number"] <= 0
            or isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= 0
            or not isinstance(record["resource_budget"], Mapping)
        ):
            raise StateCorruptionError("stored proof reservation counters are invalid")
        self._validate_proof_source_binding(record["source_theory_binding"])
        return record

    def _validate_proof_execution_claim_record(
        self,
        value: Mapping[str, Any],
        *,
        reservation: Mapping[str, Any],
    ) -> dict[str, Any]:
        record = _copy_mapping(value, "stored proof execution claim")
        required_fields = {
            "schema_version",
            "record_kind",
            "execution_claim_id",
            "execution_claim_digest",
            "reservation_id",
            "reservation_digest",
            "target_id",
            "run_id",
            "ledger_generation",
            "status",
            "action_id",
            "action_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "source_theory_head_recheck",
            "deadline_revalidation",
            "executor_lease",
            "authority_boundary",
        }
        if set(record) not in {
            frozenset(required_fields),
            frozenset(required_fields | {"recovery_seed"}),
        }:
            raise StateCorruptionError("stored proof execution claim shape is not exact")
        recheck = _copy_mapping(
            record["source_theory_head_recheck"], "proof execution head recheck"
        )
        deadline = _copy_mapping(
            record["deadline_revalidation"], "proof execution deadline revalidation"
        )
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"] != "proof_execution_claim"
            or record["execution_claim_id"] != reservation["execution_claim_id"]
            or record["reservation_id"] != reservation["reservation_id"]
            or record["reservation_digest"] != reservation["reservation_digest"]
            or record["target_id"] != self._store.target_id
            or record["run_id"] != self._store.run_id
            or record["status"] != PROOF_EXECUTION_CLAIM_STATUS
            or record["authority_boundary"] != _PROOF_COORDINATION_BOUNDARY
            or record["execution_claim_digest"]
            != _self_digest(record, "execution_claim_digest")
            or any(
                record[field] != reservation[field]
                for field in (
                    "action_id",
                    "action_digest",
                    "attempt_id",
                    "attempt_number",
                    "handoff_id",
                    "handoff_digest",
                )
            )
        ):
            raise StateCorruptionError("stored proof execution claim is inconsistent")
        expected_head = _validate_head_observation(
            recheck.get("expected_head", {}),
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        observed_head = _validate_head_observation(
            recheck.get("observed_head", {}),
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        if (
            set(recheck)
            != {"recheck_kind", "expected_head", "observed_head", "match", "recheck_digest"}
            or recheck["recheck_kind"] != "prelaunch_exact_theory_head_recheck"
            or recheck["match"] is not True
            or expected_head != observed_head
            or recheck["recheck_digest"] != _self_digest(recheck, "recheck_digest")
        ):
            raise StateCorruptionError("stored proof execution revalidation is invalid")
        if set(deadline) != {
            "revalidation_kind",
            "theory_authorization_digest",
            "evaluated_at",
            "clock_authority",
            "clock_authority_digest",
            "consume_before",
            "live_capability_revalidated",
            "cross_store_atomicity_claimed",
            "revalidation_digest",
        }:
            raise StateCorruptionError(
                "stored proof execution deadline shape is not exact"
            )
        clock_authority = _validate_governed_clock_authority(
            deadline["clock_authority"]
        )
        evaluated_at = _parse_canonical_utc_timestamp(
            deadline["evaluated_at"], "proof execution evaluated_at"
        )
        consume_before = _parse_canonical_utc_timestamp(
            deadline["consume_before"], "proof execution consume_before"
        )
        if (
            deadline["revalidation_kind"]
            != "governed_deadline_revalidated_at_prelaunch"
            or deadline["theory_authorization_digest"]
            != reservation["source_theory_binding"]["theory_authorization_digest"]
            or deadline["clock_authority_digest"]
            != clock_authority["authority_digest"]
            or deadline["consume_before"]
            != reservation["literature_consume_before"]
            or evaluated_at > consume_before
            or deadline["live_capability_revalidated"] is not True
            or deadline["cross_store_atomicity_claimed"] is not False
            or deadline["revalidation_digest"]
            != _self_digest(deadline, "revalidation_digest")
        ):
            raise StateCorruptionError("stored proof execution revalidation is invalid")
        lease = _validate_executor_lease(
            record["executor_lease"],
            reservation=reservation,
        )
        if lease["issued_at"] != deadline["evaluated_at"]:
            raise StateCorruptionError(
                "proof executor lease crossed its claim-time observation"
            )
        if "recovery_seed" in record:
            _validate_proof_recovery_seed(
                record["recovery_seed"],
                expected_phase="claim_binding",
            )
        return record

    def _validate_proof_terminal_bundle_record(
        self,
        value: Mapping[str, Any],
        *,
        reservation: Mapping[str, Any],
        claim: Mapping[str, Any],
        checkpoint: Mapping[str, Any] | None,
        recovery_claim: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Validate one exact terminal bundle without manufacturing launch authority."""

        from agentic.discovery.proof_execution import (
            TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT,
            terminal_projection_requires_launch_checkpoint,
            validate_terminal_result_projection,
        )

        record = _copy_mapping(value, "stored proof terminal bundle")
        if set(record) != {
            "schema_version",
            "record_kind",
            "terminal_bundle_id",
            "terminal_bundle_digest",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "execution_claim_digest",
            "target_id",
            "run_id",
            "ledger_generation",
            "status",
            "requested_terminal_status",
            "schedule_id",
            "schedule_digest",
            "action_id",
            "action_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "source_theory_head",
            "launch_boundary_checkpoint",
            "terminal_projection",
            "terminal_projection_digest",
            "attachment_descriptors",
            "attachment_set_digest",
            "lifecycle_terminalization",
            "theory_head_recheck",
            "terminal_receipt",
            "receipt_index_membership",
            "pending_n_plus_one_reflection_request",
            "recovery_authority",
            "derived_artifact_descriptors",
            "terminal_request_digest",
            "authority_boundary",
        }:
            raise StateCorruptionError(
                "stored proof terminal bundle shape is not exact"
            )
        try:
            terminal = validate_terminal_result_projection(
                record["terminal_projection"],
                expected_binding_digest=(
                    None
                    if checkpoint is None
                    else str(checkpoint["binding_digest"])
                ),
            )
        except ContractError as exc:
            raise StateCorruptionError(
                "stored proof terminal projection is invalid"
            ) from exc
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"] != "proof_execution_terminal_bundle"
            or record["reservation_id"] != reservation["reservation_id"]
            or record["reservation_digest"] != reservation["reservation_digest"]
            or record["execution_claim_id"] != claim["execution_claim_id"]
            or record["execution_claim_digest"] != claim["execution_claim_digest"]
            or record["target_id"] != self._store.target_id
            or record["run_id"] != self._store.run_id
            or record["authority_boundary"] != _PROOF_TERMINAL_BOUNDARY
            or record["terminal_bundle_digest"]
            != _self_digest(record, "terminal_bundle_digest")
            or record["terminal_projection_digest"] != terminal["content_digest"]
            or record["requested_terminal_status"] != terminal["terminal_status"]
            or len(canonical_json(record)) > MAX_PROOF_RECORD_BYTES
            or any(
                record[field] != reservation[field]
                for field in (
                    "schedule_id",
                    "schedule_digest",
                    "action_id",
                    "action_digest",
                    "attempt_id",
                    "attempt_number",
                    "handoff_id",
                    "handoff_digest",
                )
            )
            or any(
                terminal[field] != record[field]
                for field in (
                    "reservation_id",
                    "reservation_digest",
                    "execution_claim_id",
                    "execution_claim_digest",
                    "attempt_id",
                    "attempt_number",
                    "handoff_id",
                    "handoff_digest",
                )
            )
        ):
            raise StateCorruptionError(
                "stored proof terminal bundle is inconsistent"
            )
        checkpoint_required = terminal_projection_requires_launch_checkpoint(
            terminal
        )
        stored_checkpoint = record["launch_boundary_checkpoint"]
        if checkpoint is None:
            if stored_checkpoint is not None or checkpoint_required:
                raise StateCorruptionError(
                    "launch-or-later proof terminal lacks its exact checkpoint"
                )
        else:
            if (
                stored_checkpoint != dict(checkpoint)
                or terminal["binding_id"] != checkpoint["binding_id"]
                or terminal["binding_digest"] != checkpoint["binding_digest"]
                or terminal["invocation_id"] != checkpoint["invocation_id"]
                or terminal["invocation_digest"]
                != checkpoint["invocation_digest"]
                or checkpoint["ledger_generation"]
                >= record["ledger_generation"]
            ):
                raise StateCorruptionError(
                    "stored proof terminal crossed its launch checkpoint"
                )
        validate_identifier(record["terminal_bundle_id"], "terminal_bundle_id")
        validate_identifier(terminal["terminal_id"], "terminal_id")
        for field in (
            "terminal_bundle_digest",
            "execution_claim_digest",
            "reservation_digest",
            "schedule_digest",
            "action_digest",
            "handoff_digest",
            "terminal_projection_digest",
            "attachment_set_digest",
            "terminal_request_digest",
        ):
            validate_digest(record[field])
        if (
            isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= 0
        ):
            raise StateCorruptionError(
                "stored proof terminal generation is invalid"
            )

        source_head = _validate_head_observation(
            record["source_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        if source_head != reservation["source_theory_binding"]["observed_head"]:
            raise StateCorruptionError(
                "stored proof terminal crossed its source theory head"
            )
        raw_recheck = _copy_mapping(
            record["theory_head_recheck"],
            "stored proof terminal theory-head recheck",
        )
        if set(raw_recheck) != {
            "recheck_kind",
            "expected_head",
            "observed_head",
            "match",
            "disposition_reason",
            "requested_terminal_status",
            "effective_terminal_status",
            "recheck_digest",
        }:
            raise StateCorruptionError(
                "stored proof terminal head-recheck shape is not exact"
            )
        expected_head = _validate_head_observation(
            raw_recheck["expected_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        observed_head = _validate_head_observation(
            raw_recheck["observed_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        head_matches = expected_head == observed_head
        effective_status = (
            terminal["terminal_status"]
            if head_matches
            else REBASE_REQUIRED_STATUS
        )
        if (
            raw_recheck["recheck_kind"]
            != "proof_terminalization_theory_head_recheck"
            or expected_head != source_head
            or raw_recheck["match"] is not head_matches
            or raw_recheck["disposition_reason"]
            != ("head_unchanged" if head_matches else "theory_head_drift")
            or raw_recheck["requested_terminal_status"]
            != terminal["terminal_status"]
            or raw_recheck["effective_terminal_status"] != effective_status
            or raw_recheck["recheck_digest"]
            != _self_digest(raw_recheck, "recheck_digest")
            or record["status"] != effective_status
        ):
            raise StateCorruptionError(
                "stored proof terminal head recheck is inconsistent"
            )

        try:
            expected_terminal_attachments = _proof_terminal_attachment_descriptors(
                terminal,
                attempt_id=reservation["attempt_id"],
            )
        except ContractError as exc:
            raise StateCorruptionError(
                "stored proof terminal attachment descriptors are invalid"
            ) from exc
        if (
            not isinstance(record["attachment_descriptors"], list)
            or record["attachment_descriptors"]
            != sorted(
                record["attachment_descriptors"],
                key=lambda row: str(row["logical_name"]),
            )
            or record["attachment_set_digest"]
            != canonical_digest(record["attachment_descriptors"])
        ):
            raise StateCorruptionError(
                "stored proof terminal attachments are inconsistent"
            )
        terminal_names = {
            str(row["logical_name"])
            for row in expected_terminal_attachments
        }
        actual_terminal_attachments = [
            row
            for row in record["attachment_descriptors"]
            if str(row.get("logical_name")) in terminal_names
        ]
        replay_attachments = [
            row
            for row in record["attachment_descriptors"]
            if str(row.get("logical_name", "")).startswith(
                _TYPED_TERMINAL_REPLAY_PREFIX
            )
        ]
        replay_names = {
            str(row.get("logical_name")) for row in replay_attachments
        }
        descriptor_names = [
            str(row.get("logical_name"))
            for row in record["attachment_descriptors"]
        ]
        descriptor_paths = [
            str(row.get("artifact_path"))
            for row in record["attachment_descriptors"]
        ]
        if (
            actual_terminal_attachments != expected_terminal_attachments
            or len(descriptor_names) != len(set(descriptor_names))
            or len(descriptor_paths) != len(set(descriptor_paths))
            or set(descriptor_names) != terminal_names | replay_names
            or not _TYPED_TERMINAL_REPLAY_BINDING_NAMES.issubset(
                replay_names
            )
            or (
                checkpoint is None
                and TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT in replay_names
            )
            or (
                checkpoint is not None
                and TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT not in replay_names
            )
            or len(record["attachment_descriptors"])
            > MAX_PROOF_TERMINAL_ATTACHMENTS
            or sum(
                int(row.get("byte_length", -1))
                for row in record["attachment_descriptors"]
            )
            > MAX_PROOF_TERMINAL_ATTACHMENT_BYTES
        ):
            raise StateCorruptionError(
                "stored proof typed-replay attachment coverage is invalid"
            )
        for row in replay_attachments:
            logical_name = str(row.get("logical_name", ""))
            expected_path = (
                f"{_proof_terminal_base_path(reservation['attempt_id'])}/"
                f"{logical_name}"
            )
            if (
                set(row)
                != {
                    "attachment_kind",
                    "logical_name",
                    "source_relative_path",
                    "artifact_path",
                    "sha256",
                    "byte_length",
                    "roles",
                    "executable",
                }
                or row["attachment_kind"] != "typed_terminal_replay"
                or safe_relative_path(
                    logical_name, forbid_latest=True
                ).as_posix()
                != logical_name
                or row["artifact_path"] != expected_path
                or row["roles"] != ["typed_terminal_replay"]
                or row["executable"] is not False
                or isinstance(row["byte_length"], bool)
                or not isinstance(row["byte_length"], int)
                or row["byte_length"] < 0
            ):
                raise StateCorruptionError(
                    "stored proof typed-replay descriptor is invalid"
                )
            validate_digest(row["sha256"])
        recovery_authority = record["recovery_authority"]
        if terminal["terminal_status"] == "abandoned_uncertain":
            if recovery_claim is None:
                raise StateCorruptionError(
                    "abandoned proof terminal lacks its durable recovery claim"
                )
            _validate_recovery_abandonment_authority(
                recovery_authority,
                reservation=reservation,
                claim=claim,
                recovery_claim=recovery_claim,
                terminal=terminal,
            )
        elif recovery_authority is not None or recovery_claim is not None:
            raise StateCorruptionError(
                "non-recovery proof terminal crossed recovery authority"
            )

        terminalization = _copy_mapping(
            record["lifecycle_terminalization"],
            "proof lifecycle terminalization",
        )
        if set(terminalization) != {
            "terminalization_kind",
            "schedule_id",
            "schedule_digest",
            "action_id",
            "action_digest",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "execution_claim_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "requested_terminal_status",
            "effective_terminal_status",
            "action_terminalized",
            "attempt_terminalized",
            "claim_remains_spent",
            "respawn_authorized",
            "terminalization_digest",
        }:
            raise StateCorruptionError(
                "proof lifecycle terminalization shape is not exact"
            )
        terminalization_matches = {
            "schedule_id": reservation["schedule_id"],
            "schedule_digest": reservation["schedule_digest"],
            "action_id": reservation["action_id"],
            "action_digest": reservation["action_digest"],
            "reservation_id": reservation["reservation_id"],
            "reservation_digest": reservation["reservation_digest"],
            "execution_claim_id": claim["execution_claim_id"],
            "execution_claim_digest": claim["execution_claim_digest"],
            "attempt_id": reservation["attempt_id"],
            "attempt_number": reservation["attempt_number"],
            "handoff_id": reservation["handoff_id"],
            "handoff_digest": reservation["handoff_digest"],
            "requested_terminal_status": terminal["terminal_status"],
            "effective_terminal_status": effective_status,
        }
        if (
            terminalization["terminalization_kind"]
            != "one_reserved_prove_action_and_attempt_terminalized"
            or any(
                terminalization[field] != expected
                for field, expected in terminalization_matches.items()
            )
            or terminalization["action_terminalized"] is not True
            or terminalization["attempt_terminalized"] is not True
            or terminalization["claim_remains_spent"] is not True
            or terminalization["respawn_authorized"] is not False
            or terminalization["terminalization_digest"]
            != _self_digest(terminalization, "terminalization_digest")
        ):
            raise StateCorruptionError(
                "proof lifecycle terminalization is inconsistent"
            )

        receipt = _copy_mapping(
            record["terminal_receipt"], "proof terminal receipt"
        )
        if set(receipt) != {
            "schema_version",
            "receipt_kind",
            "receipt_id",
            "terminal_bundle_id",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "execution_claim_digest",
            "action_id",
            "action_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "terminal_id",
            "terminal_projection_digest",
            "requested_terminal_status",
            "effective_terminal_status",
            "execution_status",
            "proof_verdict",
            "reason_code",
            "attachment_set_digest",
            "source_theory_head_digest",
            "theory_head_recheck_digest",
            "operational_evidence_only",
            "same_cycle_theory_mutation",
            "authority_nulls",
            "receipt_digest",
        }:
            raise StateCorruptionError("proof terminal receipt shape is not exact")
        expected_bundle_id = stable_identifier(
            "proof-terminal-bundle-v1",
            reservation["reservation_digest"],
            claim["execution_claim_digest"],
            terminal["content_digest"],
            record["attachment_set_digest"],
            raw_recheck["recheck_digest"],
            effective_status,
        )
        expected_receipt_id = stable_identifier(
            "proof-terminal-receipt-v1",
            expected_bundle_id,
            terminal["content_digest"],
            record["attachment_set_digest"],
            raw_recheck["recheck_digest"],
        )
        receipt_matches = {
            "terminal_bundle_id": expected_bundle_id,
            "reservation_id": reservation["reservation_id"],
            "reservation_digest": reservation["reservation_digest"],
            "execution_claim_id": claim["execution_claim_id"],
            "execution_claim_digest": claim["execution_claim_digest"],
            "action_id": reservation["action_id"],
            "action_digest": reservation["action_digest"],
            "attempt_id": reservation["attempt_id"],
            "attempt_number": reservation["attempt_number"],
            "handoff_id": reservation["handoff_id"],
            "handoff_digest": reservation["handoff_digest"],
            "terminal_id": terminal["terminal_id"],
            "terminal_projection_digest": terminal["content_digest"],
            "requested_terminal_status": terminal["terminal_status"],
            "effective_terminal_status": effective_status,
            "execution_status": terminal["execution_status"],
            "proof_verdict": terminal["proof_verdict"],
            "reason_code": terminal["reason_code"],
            "attachment_set_digest": record["attachment_set_digest"],
            "source_theory_head_digest": source_head["head_digest"],
            "theory_head_recheck_digest": raw_recheck["recheck_digest"],
            "authority_nulls": terminal["authority_nulls"],
        }
        if (
            record["terminal_bundle_id"] != expected_bundle_id
            or receipt["schema_version"] != "1.0.0"
            or receipt["receipt_kind"]
            != "proof_execution_terminal_receipt"
            or receipt["receipt_id"] != expected_receipt_id
            or any(
                receipt[field] != expected
                for field, expected in receipt_matches.items()
            )
            or receipt["operational_evidence_only"] is not True
            or receipt["same_cycle_theory_mutation"] is not False
            or receipt["receipt_digest"]
            != _self_digest(receipt, "receipt_digest")
        ):
            raise StateCorruptionError("proof terminal receipt is inconsistent")

        membership = _copy_mapping(
            record["receipt_index_membership"],
            "proof terminal receipt-index membership",
        )
        if set(membership) != {
            "schema_version",
            "index_kind",
            "membership_id",
            "target_id",
            "run_id",
            "reservation_id",
            "execution_claim_id",
            "attempt_id",
            "action_id",
            "terminal_bundle_id",
            "terminal_id",
            "terminal_projection_digest",
            "receipt_id",
            "receipt_digest",
            "unique_terminal_for_reservation",
            "unique_terminal_for_attempt",
            "membership_digest",
        }:
            raise StateCorruptionError(
                "proof terminal receipt-index shape is not exact"
            )
        expected_membership_id = stable_identifier(
            "proof-terminal-membership-v1",
            self._store.target_id,
            self._store.run_id,
            reservation["reservation_id"],
            reservation["attempt_id"],
        )
        membership_matches = {
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "reservation_id": reservation["reservation_id"],
            "execution_claim_id": claim["execution_claim_id"],
            "attempt_id": reservation["attempt_id"],
            "action_id": reservation["action_id"],
            "terminal_bundle_id": expected_bundle_id,
            "terminal_id": terminal["terminal_id"],
            "terminal_projection_digest": terminal["content_digest"],
            "receipt_id": receipt["receipt_id"],
            "receipt_digest": receipt["receipt_digest"],
        }
        if (
            membership["schema_version"] != "1.0.0"
            or membership["index_kind"]
            != "proof_execution_terminal_receipt_membership"
            or membership["membership_id"] != expected_membership_id
            or any(
                membership[field] != expected
                for field, expected in membership_matches.items()
            )
            or membership["unique_terminal_for_reservation"] is not True
            or membership["unique_terminal_for_attempt"] is not True
            or membership["membership_digest"]
            != _self_digest(membership, "membership_digest")
        ):
            raise StateCorruptionError(
                "proof terminal receipt-index membership is inconsistent"
            )

        reflection = _copy_mapping(
            record["pending_n_plus_one_reflection_request"],
            "pending N+1 proof-result reflection request",
        )
        if set(reflection) != {
            "schema_version",
            "request_kind",
            "request_id",
            "request_status",
            "source_theory_head",
            "finalization_observed_head",
            "source_theory_generation",
            "requested_n_plus_one_generation",
            "head_match",
            "rebase_required",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "execution_claim_digest",
            "schedule_id",
            "schedule_digest",
            "action_id",
            "action_digest",
            "attempt_id",
            "attempt_number",
            "handoff_id",
            "handoff_digest",
            "terminal_bundle_id",
            "terminal_id",
            "terminal_projection_digest",
            "terminal_receipt_id",
            "terminal_receipt_digest",
            "receipt_index_membership_id",
            "receipt_index_membership_digest",
            "requested_terminal_status",
            "effective_terminal_status",
            "execution_status",
            "proof_verdict",
            "reason_code",
            "attachment_set_digest",
            "required_theory_generation_relation",
            "same_cycle_theory_mutation_authorized",
            "theory_mutation_performed",
            "proof_result_intake_consumed",
            "epistemic_effect",
            "authority_nulls",
            "request_digest",
        }:
            raise StateCorruptionError(
                "pending N+1 proof-result request shape is not exact"
            )
        expected_request_id = stable_identifier(
            "proof-result-reflection-request-v1",
            reservation["reservation_id"],
            claim["execution_claim_digest"],
            terminal["content_digest"],
            receipt["receipt_digest"],
            membership["membership_digest"],
            source_head["head_digest"],
        )
        reflection_matches = {
            "source_theory_head": source_head,
            "finalization_observed_head": observed_head,
            "source_theory_generation": source_head["generation"],
            "requested_n_plus_one_generation": source_head["generation"] + 1,
            "head_match": head_matches,
            "rebase_required": not head_matches,
            "reservation_id": reservation["reservation_id"],
            "reservation_digest": reservation["reservation_digest"],
            "execution_claim_id": claim["execution_claim_id"],
            "execution_claim_digest": claim["execution_claim_digest"],
            "schedule_id": reservation["schedule_id"],
            "schedule_digest": reservation["schedule_digest"],
            "action_id": reservation["action_id"],
            "action_digest": reservation["action_digest"],
            "attempt_id": reservation["attempt_id"],
            "attempt_number": reservation["attempt_number"],
            "handoff_id": reservation["handoff_id"],
            "handoff_digest": reservation["handoff_digest"],
            "terminal_bundle_id": expected_bundle_id,
            "terminal_id": terminal["terminal_id"],
            "terminal_projection_digest": terminal["content_digest"],
            "terminal_receipt_id": receipt["receipt_id"],
            "terminal_receipt_digest": receipt["receipt_digest"],
            "receipt_index_membership_id": membership["membership_id"],
            "receipt_index_membership_digest": membership["membership_digest"],
            "requested_terminal_status": terminal["terminal_status"],
            "effective_terminal_status": effective_status,
            "execution_status": terminal["execution_status"],
            "proof_verdict": terminal["proof_verdict"],
            "reason_code": terminal["reason_code"],
            "attachment_set_digest": record["attachment_set_digest"],
            "authority_nulls": terminal["authority_nulls"],
        }
        if (
            reflection["schema_version"] != "1.0.0"
            or reflection["request_kind"]
            != "pending_n_plus_one_proof_result_reflection"
            or reflection["request_id"] != expected_request_id
            or reflection["request_status"] != "pending"
            or any(
                reflection[field] != expected
                for field, expected in reflection_matches.items()
            )
            or reflection["required_theory_generation_relation"]
            != "distinct_descendant_n_plus_one"
            or reflection["same_cycle_theory_mutation_authorized"] is not False
            or reflection["theory_mutation_performed"] is not False
            or reflection["proof_result_intake_consumed"] is not False
            or reflection["epistemic_effect"]
            != "pending_only_no_same_cycle_theory_mutation"
            or reflection["request_digest"]
            != _self_digest(reflection, "request_digest")
        ):
            raise StateCorruptionError(
                "pending N+1 proof-result request is inconsistent"
            )

        expected_derived = _proof_terminal_derived_artifact_descriptors(
            attempt_id=reservation["attempt_id"],
            terminal_receipt=receipt,
            receipt_index_membership=membership,
            pending_n_plus_one_reflection_request=reflection,
        )
        expected_request_digest = _proof_terminal_request_digest(
            reservation=reservation,
            claim=claim,
            terminal_projection_digest=terminal["content_digest"],
            attachment_set_digest=record["attachment_set_digest"],
        )
        if (
            record["derived_artifact_descriptors"] != expected_derived
            or record["terminal_request_digest"] != expected_request_digest
        ):
            raise StateCorruptionError(
                "stored proof terminal durable artifacts are inconsistent"
            )
        return record

    def _validate_proof_result_intake_claim_record(
        self,
        value: Mapping[str, Any],
        *,
        terminal: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Replay one durable claim over an exact pending v3 terminal request."""

        record = _copy_mapping(value, "stored proof-result intake claim")
        if set(record) != {
            "schema_version",
            "record_kind",
            "intake_claim_id",
            "intake_claim_digest",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "execution_claim_digest",
            "attempt_id",
            "terminal_bundle_id",
            "terminal_bundle_digest",
            "terminal_receipt_id",
            "terminal_receipt_digest",
            "reflection_request_id",
            "reflection_request_digest",
            "source_theory_head",
            "requested_descendant_generation",
            "transition_plan",
            "ledger_generation",
            "status",
            "claim_remains_one_shot",
            "coordination_consumed",
            "authority_boundary",
        }:
            raise StateCorruptionError(
                "stored proof-result intake claim shape is not exact"
            )
        reflection = _copy_mapping(
            terminal["pending_n_plus_one_reflection_request"],
            "proof-result intake source request",
        )
        source_head = _validate_head_observation(
            record["source_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        plan = _copy_mapping(
            record["transition_plan"],
            "proof-result intake transition plan",
        )
        if set(plan) != {
            "plan_kind",
            "source_generation",
            "descendant_generation",
            "intake_event_id",
            "intake_event_hash",
            "intake_event_deduplication_key",
            "intake_artifact_path",
            "intake_artifact_sha256",
            "intake_artifact_size_bytes",
            "theory_outbox_id",
            "theory_outbox_digest",
            "theory_outbox_artifact_path",
            "theory_outbox_artifact_sha256",
            "theory_outbox_artifact_size_bytes",
            "next_state_semantic_digest",
            "theory_commit_idempotency_key",
            "theory_commit_request_digest",
            "direct_theory_selection",
            "direct_theory_status_mutation",
            "semantic_reflection_performed",
            "plan_digest",
        }:
            raise StateCorruptionError(
                "stored proof-result intake transition plan shape is not exact"
            )
        expected_claim_id = stable_identifier(
            "proof-result-intake-claim-v1",
            terminal["reservation_id"],
            terminal["terminal_bundle_digest"],
            reflection["request_digest"],
            source_head["head_digest"],
        )
        expected_artifact_path = (
            "branches/proof-reflection/reflections/"
            f"{reflection['request_id']}.json"
        )
        expected_outbox_id = stable_identifier(
            "proof-result-intake-theory-outbox-v1",
            expected_claim_id,
            terminal["terminal_bundle_digest"],
            reflection["request_digest"],
        )
        expected_outbox_path = (
            "branches/proof-reflection/outbox/"
            f"{expected_outbox_id}.json"
        )
        expected_idempotency_key = stable_identifier(
            "proof-result-intake-theory-commit-v1",
            expected_claim_id,
            reflection["request_id"],
        )
        expected_theory_request_digest = canonical_digest(
            {
                "intake_claim_id": expected_claim_id,
                "source_theory_head_digest": source_head["head_digest"],
                "reflection_request_digest": reflection["request_digest"],
                "intake_event_hash": plan["intake_event_hash"],
                "intake_artifact_sha256": plan["intake_artifact_sha256"],
                "theory_outbox_digest": plan["theory_outbox_digest"],
                "theory_outbox_artifact_sha256": plan[
                    "theory_outbox_artifact_sha256"
                ],
                "next_state_semantic_digest": plan[
                    "next_state_semantic_digest"
                ],
            }
        )
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"] != "proof_result_intake_claim"
            or record["intake_claim_id"] != expected_claim_id
            or record["reservation_id"] != terminal["reservation_id"]
            or record["reservation_digest"] != terminal["reservation_digest"]
            or record["execution_claim_id"] != terminal["execution_claim_id"]
            or record["execution_claim_digest"]
            != terminal["execution_claim_digest"]
            or record["attempt_id"] != terminal["attempt_id"]
            or record["terminal_bundle_id"] != terminal["terminal_bundle_id"]
            or record["terminal_bundle_digest"]
            != terminal["terminal_bundle_digest"]
            or record["terminal_receipt_id"]
            != terminal["terminal_receipt"]["receipt_id"]
            or record["terminal_receipt_digest"]
            != terminal["terminal_receipt"]["receipt_digest"]
            or record["reflection_request_id"] != reflection["request_id"]
            or record["reflection_request_digest"]
            != reflection["request_digest"]
            or source_head != terminal["source_theory_head"]
            or record["requested_descendant_generation"]
            != source_head["generation"] + 1
            or reflection["source_theory_head"] != source_head
            or reflection["requested_n_plus_one_generation"]
            != source_head["generation"] + 1
            or reflection["request_status"] != "pending"
            or reflection["head_match"] is not True
            or reflection["rebase_required"] is not False
            or reflection["proof_result_intake_consumed"] is not False
            or terminal["status"] == REBASE_REQUIRED_STATUS
            or terminal["theory_head_recheck"]["match"] is not True
            or plan["plan_kind"]
            != "deterministic_pending_reflection_event_commit"
            or plan["source_generation"] != source_head["generation"]
            or plan["descendant_generation"]
            != source_head["generation"] + 1
            or safe_relative_path(
                plan["intake_artifact_path"], forbid_latest=True
            ).as_posix()
            != expected_artifact_path
            or plan["theory_outbox_id"] != expected_outbox_id
            or safe_relative_path(
                plan["theory_outbox_artifact_path"],
                forbid_latest=True,
            ).as_posix()
            != expected_outbox_path
            or plan["theory_commit_idempotency_key"]
            != expected_idempotency_key
            or plan["theory_commit_request_digest"]
            != expected_theory_request_digest
            or plan["direct_theory_selection"] is not False
            or plan["direct_theory_status_mutation"] is not False
            or plan["semantic_reflection_performed"] is not False
            or plan["plan_digest"] != _self_digest(plan, "plan_digest")
            or record["status"] != PROOF_RESULT_INTAKE_CLAIM_STATUS
            or record["claim_remains_one_shot"] is not True
            or record["coordination_consumed"] is not False
            or record["authority_boundary"] != _PROOF_RESULT_INTAKE_BOUNDARY
            or record["intake_claim_digest"]
            != _self_digest(record, "intake_claim_digest")
            or isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= terminal["ledger_generation"]
            or isinstance(plan["intake_artifact_size_bytes"], bool)
            or not isinstance(plan["intake_artifact_size_bytes"], int)
            or plan["intake_artifact_size_bytes"] <= 0
            or isinstance(plan["theory_outbox_artifact_size_bytes"], bool)
            or not isinstance(
                plan["theory_outbox_artifact_size_bytes"], int
            )
            or plan["theory_outbox_artifact_size_bytes"] <= 0
            or len(canonical_json(record)) > MAX_PROOF_RECORD_BYTES
        ):
            raise StateCorruptionError(
                "stored proof-result intake claim is inconsistent"
            )
        for field in (
            "intake_claim_id",
            "reservation_id",
            "execution_claim_id",
            "attempt_id",
            "terminal_bundle_id",
            "terminal_receipt_id",
            "reflection_request_id",
            "intake_event_id",
            "theory_outbox_id",
            "theory_commit_idempotency_key",
        ):
            validate_identifier(
                plan[field]
                if field in plan
                else record[field],
                field,
            )
        for field in (
            "intake_claim_digest",
            "reservation_digest",
            "execution_claim_digest",
            "terminal_bundle_digest",
            "terminal_receipt_digest",
            "reflection_request_digest",
        ):
            validate_digest(record[field])
        for field in (
            "intake_event_hash",
            "intake_event_deduplication_key",
            "intake_artifact_sha256",
            "theory_outbox_digest",
            "theory_outbox_artifact_sha256",
            "next_state_semantic_digest",
            "theory_commit_request_digest",
            "plan_digest",
        ):
            validate_digest(plan[field])
        return record

    def _validate_proof_result_intake_consumption_record(
        self,
        value: Mapping[str, Any],
        *,
        claim: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Replay consumption of one exact outbox in the active theory prefix."""

        record = _copy_mapping(
            value, "stored proof-result intake consumption"
        )
        if set(record) != {
            "schema_version",
            "record_kind",
            "intake_consumption_id",
            "intake_consumption_digest",
            "intake_claim_id",
            "intake_claim_digest",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "attempt_id",
            "reflection_request_id",
            "reflection_request_digest",
            "source_theory_head",
            "descendant_theory_head",
            "theory_outbox",
            "theory_head_recheck",
            "transition_plan_digest",
            "ledger_generation",
            "status",
            "request_status_before",
            "request_status_after",
            "proof_result_intake_consumed",
            "semantic_reflection_performed",
            "authority_boundary",
        }:
            raise StateCorruptionError(
                "stored proof-result intake consumption shape is not exact"
            )
        source_head = _validate_head_observation(
            record["source_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        descendant = _validate_head_observation(
            record["descendant_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        recheck = _copy_mapping(
            record["theory_head_recheck"],
            "proof-result intake theory-head recheck",
        )
        if set(recheck) != {
            "recheck_kind",
            "expected_descendant_head",
            "observed_current_head",
            "descendant_relationship",
            "theory_outbox_digest",
            "match",
            "recheck_digest",
        }:
            raise StateCorruptionError(
                "proof-result intake theory-head recheck shape is not exact"
            )
        observed_current = _validate_head_observation(
            recheck["observed_current_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        outbox = _copy_mapping(
            record["theory_outbox"],
            "proof-result intake theory outbox reference",
        )
        if set(outbox) != {
            "outbox_id",
            "outbox_digest",
            "artifact_path",
            "artifact_sha256",
            "artifact_size_bytes",
        }:
            raise StateCorruptionError(
                "proof-result intake theory outbox reference shape is not exact"
            )
        plan = claim["transition_plan"]
        expected_outbox = {
            "outbox_id": plan["theory_outbox_id"],
            "outbox_digest": plan["theory_outbox_digest"],
            "artifact_path": plan["theory_outbox_artifact_path"],
            "artifact_sha256": plan[
                "theory_outbox_artifact_sha256"
            ],
            "artifact_size_bytes": plan[
                "theory_outbox_artifact_size_bytes"
            ],
        }
        relationship = (
            "current"
            if observed_current == descendant
            else "verified_ancestor"
        )
        expected_id = stable_identifier(
            "proof-result-intake-consumption-v1",
            claim["intake_claim_digest"],
            descendant["head_digest"],
            plan["plan_digest"],
        )
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"]
            != "proof_result_intake_consumption"
            or record["intake_consumption_id"] != expected_id
            or record["intake_claim_id"] != claim["intake_claim_id"]
            or record["intake_claim_digest"]
            != claim["intake_claim_digest"]
            or record["reservation_id"] != claim["reservation_id"]
            or record["reservation_digest"] != claim["reservation_digest"]
            or record["execution_claim_id"] != claim["execution_claim_id"]
            or record["attempt_id"] != claim["attempt_id"]
            or record["reflection_request_id"]
            != claim["reflection_request_id"]
            or record["reflection_request_digest"]
            != claim["reflection_request_digest"]
            or source_head != claim["source_theory_head"]
            or descendant["generation"]
            != source_head["generation"] + 1
            or descendant["prior_generation"] != source_head["generation"]
            or record["transition_plan_digest"]
            != plan["plan_digest"]
            or outbox != expected_outbox
            or recheck["recheck_kind"]
            != "proof_result_intake_descendant_verified_in_active_prefix"
            or recheck["expected_descendant_head"] != descendant
            or observed_current["generation"] < descendant["generation"]
            or recheck["descendant_relationship"] != relationship
            or recheck["theory_outbox_digest"]
            != outbox["outbox_digest"]
            or recheck["match"] is not True
            or recheck["recheck_digest"]
            != _self_digest(recheck, "recheck_digest")
            or record["status"] != PROOF_RESULT_INTAKE_CONSUMED_STATUS
            or record["request_status_before"] != "pending"
            or record["request_status_after"] != "consumed"
            or record["proof_result_intake_consumed"] is not True
            or record["semantic_reflection_performed"] is not False
            or record["authority_boundary"]
            != _PROOF_RESULT_INTAKE_BOUNDARY
            or record["intake_consumption_digest"]
            != _self_digest(record, "intake_consumption_digest")
            or isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= claim["ledger_generation"]
            or len(canonical_json(record)) > MAX_PROOF_RECORD_BYTES
        ):
            raise StateCorruptionError(
                "stored proof-result intake consumption is inconsistent"
            )
        for field in (
            "intake_consumption_id",
            "intake_claim_id",
            "reservation_id",
            "execution_claim_id",
            "attempt_id",
            "reflection_request_id",
            "outbox_id",
        ):
            validate_identifier(
                outbox[field] if field == "outbox_id" else record[field],
                field,
            )
        for field in (
            "intake_consumption_digest",
            "intake_claim_digest",
            "reservation_digest",
            "reflection_request_digest",
            "transition_plan_digest",
            "outbox_digest",
            "artifact_sha256",
        ):
            validate_digest(
                outbox[field]
                if field in {"outbox_digest", "artifact_sha256"}
                else record[field]
            )
        return record

    def _validate_proof_result_intake_resolution_record(
        self,
        value: Mapping[str, Any],
        *,
        claim: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Replay a terminal supersession after the claimed N+1 slot was lost.

        The original claim remains immutable and one-shot.  This second record
        closes its lifecycle without pretending that unrelated descendant
        theory consumed the proof result.  Any later recommission must start
        from a new formal claim, schedule action, reservation, and attempt.
        """

        record = _copy_mapping(
            value, "stored proof-result intake supersession"
        )
        if set(record) != {
            "schema_version",
            "record_kind",
            "resolution_id",
            "resolution_digest",
            "intake_claim_id",
            "intake_claim_digest",
            "reservation_id",
            "reservation_digest",
            "execution_claim_id",
            "attempt_id",
            "reflection_request_id",
            "reflection_request_digest",
            "source_theory_head",
            "claimed_descendant_generation",
            "occupying_theory_head",
            "observed_current_head",
            "transition_plan_digest",
            "ledger_generation",
            "status",
            "resolution_reason",
            "source_in_active_prefix",
            "coordination_claim_terminalized",
            "coordination_consumed",
            "claimed_transition_committed",
            "theory_outbox_committed",
            "semantic_reflection_performed",
            "recommission_authorized",
            "required_recommission_identity",
            "authority_boundary",
        }:
            raise StateCorruptionError(
                "stored proof-result intake supersession shape is not exact"
            )
        source = _validate_head_observation(
            record["source_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        occupant = _validate_head_observation(
            record["occupying_theory_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        observed = _validate_head_observation(
            record["observed_current_head"],
            target_id=self._store.target_id,
            run_id=self._store.run_id,
        )
        plan = claim["transition_plan"]
        expected_id = stable_identifier(
            "proof-result-intake-supersession-v1",
            claim["intake_claim_digest"],
            occupant["head_digest"],
            plan["plan_digest"],
        )
        if (
            record["schema_version"] != LEDGER_SCHEMA_VERSION
            or record["record_kind"]
            != "proof_result_intake_supersession"
            or record["resolution_id"] != expected_id
            or record["intake_claim_id"] != claim["intake_claim_id"]
            or record["intake_claim_digest"]
            != claim["intake_claim_digest"]
            or record["reservation_id"] != claim["reservation_id"]
            or record["reservation_digest"] != claim["reservation_digest"]
            or record["execution_claim_id"] != claim["execution_claim_id"]
            or record["attempt_id"] != claim["attempt_id"]
            or record["reflection_request_id"]
            != claim["reflection_request_id"]
            or record["reflection_request_digest"]
            != claim["reflection_request_digest"]
            or source != claim["source_theory_head"]
            or record["claimed_descendant_generation"]
            != plan["descendant_generation"]
            or occupant["generation"] != plan["descendant_generation"]
            or occupant["prior_generation"] != plan["source_generation"]
            or observed["generation"] < occupant["generation"]
            or record["transition_plan_digest"] != plan["plan_digest"]
            or record["status"]
            != PROOF_RESULT_INTAKE_SUPERSEDED_STATUS
            or record["resolution_reason"]
            != "claimed_n_plus_one_generation_occupied_by_different_verified_commit"
            or record["source_in_active_prefix"] is not True
            or record["coordination_claim_terminalized"] is not True
            or record["coordination_consumed"] is not False
            or record["claimed_transition_committed"] is not False
            or record["theory_outbox_committed"] is not False
            or record["semantic_reflection_performed"] is not False
            or record["recommission_authorized"] is not False
            or record["required_recommission_identity"]
            != "new_formal_claim_schedule_action_reservation_attempt_and_intake_claim"
            or record["authority_boundary"]
            != _PROOF_RESULT_INTAKE_SUPERSESSION_BOUNDARY
            or record["resolution_digest"]
            != _self_digest(record, "resolution_digest")
            or isinstance(record["ledger_generation"], bool)
            or not isinstance(record["ledger_generation"], int)
            or record["ledger_generation"] <= claim["ledger_generation"]
            or len(canonical_json(record)) > MAX_PROOF_RECORD_BYTES
        ):
            raise StateCorruptionError(
                "stored proof-result intake supersession is inconsistent"
            )
        for field in (
            "resolution_id",
            "intake_claim_id",
            "reservation_id",
            "execution_claim_id",
            "attempt_id",
            "reflection_request_id",
        ):
            validate_identifier(record[field], field)
        for field in (
            "resolution_digest",
            "intake_claim_digest",
            "reservation_digest",
            "reflection_request_digest",
            "transition_plan_digest",
        ):
            validate_digest(record[field])
        return record

    def _validate_state(self, state: Mapping[str, Any]) -> None:
        legacy_fields = {
            "schema_version",
            "ledger_kind",
            "target_id",
            "run_id",
            "generation",
            "authority_boundary",
            "reservations",
            "terminal_records",
            "action_claims",
            "record_count",
        }
        current_fields = legacy_fields | {
            "proof_attempt_reservations",
            "proof_execution_claims",
            "proof_launch_checkpoints",
            "proof_terminal_recovery_claims",
            "proof_terminal_bundles",
            "proof_result_intake_claims",
            "proof_result_intake_consumptions",
            "proof_result_intake_resolutions",
            "attempt_claims",
        }
        intake_fields = {
            "proof_result_intake_claims",
            "proof_result_intake_consumptions",
            "proof_result_intake_resolutions",
        }
        pre_resolution_fields = current_fields - {
            "proof_result_intake_resolutions"
        }
        prior_current_fields = current_fields - intake_fields
        pre_recovery_fields = prior_current_fields - {
            "proof_terminal_recovery_claims"
        }
        earliest_current_fields = pre_recovery_fields - {
            "proof_launch_checkpoints"
        }
        claim_only_fields = pre_resolution_fields - {
            "proof_result_intake_consumptions"
        }
        version = state.get("schema_version")
        if (
            version == LEGACY_LEDGER_SCHEMA_VERSION
            and set(state) != legacy_fields
        ) or (
            version == LEDGER_SCHEMA_VERSION
            and frozenset(state)
            not in {
                frozenset(current_fields),
                frozenset(pre_resolution_fields),
                frozenset(claim_only_fields),
                frozenset(prior_current_fields),
                frozenset(pre_recovery_fields),
                frozenset(earliest_current_fields),
            }
        ):
            raise StateCorruptionError("coordination ledger state shape is not exact")
        if (
            version not in {LEGACY_LEDGER_SCHEMA_VERSION, LEDGER_SCHEMA_VERSION}
            or state["ledger_kind"] != LEDGER_KIND
            or state["target_id"] != self._store.target_id
            or state["run_id"] != self._store.run_id
            or state["authority_boundary"] != _AUTHORITY_BOUNDARY
            or isinstance(state["generation"], bool)
            or not isinstance(state["generation"], int)
            or state["generation"] <= 0
            or not isinstance(state["reservations"], Mapping)
            or not isinstance(state["terminal_records"], Mapping)
            or not isinstance(state["action_claims"], Mapping)
        ):
            raise StateCorruptionError("coordination ledger state identity is invalid")
        if version == LEDGER_SCHEMA_VERSION and (
            not isinstance(state["proof_attempt_reservations"], Mapping)
            or not isinstance(state["proof_execution_claims"], Mapping)
            or not isinstance(state.get("proof_launch_checkpoints", {}), Mapping)
            or not isinstance(
                state.get("proof_terminal_recovery_claims", {}),
                Mapping,
            )
            or not isinstance(state["proof_terminal_bundles"], Mapping)
            or not isinstance(
                state.get("proof_result_intake_claims", {}),
                Mapping,
            )
            or not isinstance(
                state.get("proof_result_intake_consumptions", {}),
                Mapping,
            )
            or not isinstance(
                state.get("proof_result_intake_resolutions", {}),
                Mapping,
            )
            or not isinstance(state["attempt_claims"], Mapping)
        ):
            raise StateCorruptionError(
                "proof coordination table shape is invalid"
            )
        reservations = {
            reservation_id: self._validate_reservation_record(
                value, expected_id=reservation_id
            )
            for reservation_id, value in state["reservations"].items()
        }
        terminals: dict[str, dict[str, Any]] = {}
        for reservation_id, value in state["terminal_records"].items():
            reservation = reservations.get(reservation_id)
            if reservation is None:
                raise StateCorruptionError("terminal record has no reservation")
            terminals[reservation_id] = self._validate_terminal_record(
                value, reservation=reservation
            )
        proof_reservations: dict[str, dict[str, Any]] = {}
        proof_claims: dict[str, dict[str, Any]] = {}
        proof_checkpoints: dict[str, dict[str, Any]] = {}
        proof_recovery_claims: dict[str, dict[str, Any]] = {}
        proof_terminals: dict[str, dict[str, Any]] = {}
        proof_intake_claims: dict[str, dict[str, Any]] = {}
        proof_intake_consumptions: dict[str, dict[str, Any]] = {}
        proof_intake_resolutions: dict[str, dict[str, Any]] = {}
        if version == LEDGER_SCHEMA_VERSION:
            proof_reservations = {
                reservation_id: self._validate_proof_reservation_record(
                    value, expected_id=reservation_id
                )
                for reservation_id, value in state[
                    "proof_attempt_reservations"
                ].items()
            }
            for claim_id, value in state["proof_execution_claims"].items():
                reservation_id = str(value.get("reservation_id", ""))
                reservation = proof_reservations.get(reservation_id)
                if reservation is None or claim_id != reservation.get(
                    "execution_claim_id"
                ):
                    raise StateCorruptionError(
                        "proof execution claim has no exact reservation"
                    )
                proof_claims[claim_id] = self._validate_proof_execution_claim_record(
                    value, reservation=reservation
                )
            for reservation_id, value in state.get(
                "proof_launch_checkpoints", {}
            ).items():
                reservation = proof_reservations.get(reservation_id)
                if reservation is None:
                    raise StateCorruptionError(
                        "proof launch checkpoint has no exact reservation"
                    )
                claim = proof_claims.get(reservation["execution_claim_id"])
                if claim is None:
                    raise StateCorruptionError(
                        "proof launch checkpoint has no exact execution claim"
                    )
                proof_checkpoints[reservation_id] = (
                    _validate_launch_checkpoint(
                        value,
                        reservation=reservation,
                        claim=claim,
                    )
                )
            for reservation_id, value in state.get(
                "proof_terminal_recovery_claims", {}
            ).items():
                reservation = proof_reservations.get(reservation_id)
                if reservation is None:
                    raise StateCorruptionError(
                        "proof terminal recovery claim has no exact reservation"
                    )
                claim = proof_claims.get(reservation["execution_claim_id"])
                if claim is None:
                    raise StateCorruptionError(
                        "proof terminal recovery claim has no execution claim"
                    )
                proof_recovery_claims[reservation_id] = (
                    _validate_proof_terminal_recovery_claim(
                        value,
                        reservation=reservation,
                        claim=claim,
                        checkpoint=proof_checkpoints.get(reservation_id),
                    )
                )
            for reservation_id, value in state["proof_terminal_bundles"].items():
                reservation = proof_reservations.get(reservation_id)
                if reservation is None:
                    raise StateCorruptionError(
                        "proof terminal bundle has no exact reservation"
                    )
                claim = proof_claims.get(reservation["execution_claim_id"])
                if claim is None:
                    raise StateCorruptionError(
                        "proof terminal bundle has no exact execution claim"
                    )
                proof_terminals[
                    reservation_id
                ] = self._validate_proof_terminal_bundle_record(
                    value,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=proof_checkpoints.get(reservation_id),
                    recovery_claim=proof_recovery_claims.get(
                        reservation_id
                    ),
                )
            for reservation_id, value in state.get(
                "proof_result_intake_claims", {}
            ).items():
                terminal = proof_terminals.get(reservation_id)
                if terminal is None:
                    raise StateCorruptionError(
                        "proof-result intake claim has no exact terminal"
                    )
                proof_intake_claims[reservation_id] = (
                    self._validate_proof_result_intake_claim_record(
                        value,
                        terminal=terminal,
                    )
                )
            for reservation_id, value in state.get(
                "proof_result_intake_consumptions", {}
            ).items():
                claim = proof_intake_claims.get(reservation_id)
                if claim is None:
                    raise StateCorruptionError(
                        "proof-result intake consumption has no exact claim"
                    )
                proof_intake_consumptions[reservation_id] = (
                    self._validate_proof_result_intake_consumption_record(
                        value,
                        claim=claim,
                    )
                )
            for reservation_id, value in state.get(
                "proof_result_intake_resolutions", {}
            ).items():
                claim = proof_intake_claims.get(reservation_id)
                if claim is None:
                    raise StateCorruptionError(
                        "proof-result intake supersession has no exact claim"
                    )
                if reservation_id in proof_intake_consumptions:
                    raise StateCorruptionError(
                        "proof-result intake cannot be consumed and superseded"
                    )
                proof_intake_resolutions[reservation_id] = (
                    self._validate_proof_result_intake_resolution_record(
                        value,
                        claim=claim,
                    )
                )
        count = (
            len(reservations)
            + len(terminals)
            + len(proof_reservations)
            + len(proof_claims)
            + len(proof_checkpoints)
            + len(proof_recovery_claims)
            + len(proof_terminals)
            + len(proof_intake_claims)
            + len(proof_intake_consumptions)
            + len(proof_intake_resolutions)
        )
        if (
            state["record_count"] != count
            or count > MAX_LEDGER_RECORDS
            or _durable_json_size(state) > MAX_LEDGER_STATE_BYTES
        ):
            raise StateCorruptionError("coordination ledger state ceiling is invalid")
        expected_claims: dict[str, dict[str, str]] = {}
        for reservation in reservations.values():
            for action_id in reservation["action_ids"]:
                claim_id = self._claim_id(reservation["schedule_id"], action_id)
                if claim_id in expected_claims:
                    raise StateCorruptionError("two reservations own one action claim")
                expected_claims[claim_id] = {
                    "schedule_id": reservation["schedule_id"],
                    "action_id": action_id,
                    "reservation_id": reservation["reservation_id"],
                }
        expected_attempt_claims: dict[str, dict[str, str]] = {}
        for reservation in proof_reservations.values():
            claim_id = self._claim_id(
                reservation["schedule_id"], reservation["action_id"]
            )
            if claim_id in expected_claims:
                raise StateCorruptionError("two reservations own one action claim")
            expected_claims[claim_id] = {
                "schedule_id": reservation["schedule_id"],
                "action_id": reservation["action_id"],
                "reservation_id": reservation["reservation_id"],
            }
            if reservation["attempt_id"] in expected_attempt_claims:
                raise StateCorruptionError("two reservations own one proof attempt")
            expected_attempt_claims[reservation["attempt_id"]] = {
                "attempt_id": reservation["attempt_id"],
                "action_id": reservation["action_id"],
                "reservation_id": reservation["reservation_id"],
            }
        if copy.deepcopy(dict(state["action_claims"])) != expected_claims:
            raise StateCorruptionError("coordination action-claim index is not exact")
        if version == LEDGER_SCHEMA_VERSION and copy.deepcopy(
            dict(state["attempt_claims"])
        ) != expected_attempt_claims:
            raise StateCorruptionError("coordination attempt-claim index is not exact")
        for record in (
            *reservations.values(),
            *terminals.values(),
            *proof_reservations.values(),
            *proof_claims.values(),
            *proof_checkpoints.values(),
            *proof_recovery_claims.values(),
            *proof_terminals.values(),
            *proof_intake_claims.values(),
            *proof_intake_consumptions.values(),
            *proof_intake_resolutions.values(),
        ):
            if record["ledger_generation"] > state["generation"]:
                raise StateCorruptionError("coordination record is from a future generation")

    def _claim_id(self, schedule_id: str, action_id: str) -> str:
        return stable_identifier(
            "coordination-action-claim-v1",
            self._store.target_id,
            self._store.run_id,
            schedule_id,
            action_id,
        )

    def _ensure_state_ceiling(self, state: Mapping[str, Any]) -> None:
        count = int(state["record_count"])
        if count > MAX_LEDGER_RECORDS:
            raise ContractError("coordination ledger exceeds the fixed record ceiling")
        if _durable_json_size(state) > MAX_LEDGER_STATE_BYTES:
            raise ContractError("coordination ledger exceeds the fixed state-byte ceiling")

    def _commit_record(
        self,
        *,
        expected_generation: int,
        state: Mapping[str, Any],
        record: Mapping[str, Any],
        idempotency_key: str,
        request_digest: str,
        failpoint: str | None,
        reject_idempotent_replay: bool = False,
        extra_artifacts: Sequence[CommitArtifact] = (),
    ) -> CoordinationLedgerResult:
        data = canonical_json(record)
        record_ceiling = (
            MAX_PROOF_RECORD_BYTES
            if str(record.get("record_kind", "")).startswith("proof_")
            else MAX_RECORD_BYTES
        )
        if len(data) > record_ceiling:
            raise ContractError("coordination record exceeds the fixed record-byte ceiling")
        result = self._store.commit(
            expected_generation=expected_generation,
            state=state,
            artifacts=(
                CommitArtifact(
                    relative_path=_record_path(record),
                    content=data,
                    namespace=Namespace(
                        self._store.target_id,
                        self._store.run_id,
                        _COORDINATION_BRANCH_ID,
                        expected_generation,
                    ),
                ),
                *tuple(extra_artifacts),
            ),
            idempotency_key=idempotency_key,
            request_digest=request_digest,
            failpoint=failpoint,
        )
        if reject_idempotent_replay and result.idempotent:
            raise ProofExecutionClaimConsumed(
                "proof execution claim is already consumed: "
                f"{record.get('execution_claim_id', '')}"
            )
        return self._result_for_record(record)

    def _result_for_record(
        self, record: Mapping[str, Any]
    ) -> CoordinationLedgerResult:
        generation = int(record["ledger_generation"])
        path = _record_path(record)
        requested_paths = [path]
        recovery_seed: dict[str, Any] | None = None
        if (
            record["record_kind"]
            in {
                "proof_execution_claim",
                "proof_launch_boundary_checkpoint",
            }
            and isinstance(record.get("recovery_seed"), Mapping)
        ):
            recovery_seed = _validate_proof_recovery_seed(
                record["recovery_seed"],
                expected_phase=(
                    "claim_binding"
                    if record["record_kind"] == "proof_execution_claim"
                    else "staged_invocation"
                ),
            )
            requested_paths.extend(
                str(row["artifact_path"])
                for row in recovery_seed["attachment_descriptors"]
            )
        if record["record_kind"] == "proof_execution_terminal_bundle":
            requested_paths.extend(
                str(row["artifact_path"])
                for row in record["attachment_descriptors"]
            )
            requested_paths.extend(
                str(row["artifact_path"])
                for row in record["derived_artifact_descriptors"]
            )
        if len(requested_paths) != len(set(requested_paths)):
            raise StateCorruptionError(
                "coordination record artifact paths are not unique"
            )
        commit, artifacts = self._store.read_verified_artifacts(
            generation, requested_paths
        )
        data = artifacts[path]
        decoded = _decode_canonical_mapping(data, "committed coordination record")
        if decoded != record:
            raise StateCorruptionError(
                "committed coordination artifact differs from ledger state"
            )
        descriptors = [
            row for row in commit.manifest["artifacts"] if row.get("path") == path
        ]
        if len(descriptors) != 1:
            raise StateCorruptionError(
                "coordination commit lacks one exact record artifact"
            )
        descriptor = descriptors[0]
        if (
            descriptor.get("sha256") != bytes_digest(data)
            or descriptor.get("size_bytes") != len(data)
        ):
            raise StateCorruptionError(
                "coordination record descriptor differs from verified bytes"
            )
        attached_artifacts: list[dict[str, Any]] = []
        if recovery_seed is not None:
            manifest_by_path = {
                str(row.get("path")): row
                for row in commit.manifest["artifacts"]
            }
            expected_manifest_paths = {
                path,
                *(
                    str(row["artifact_path"])
                    for row in recovery_seed["attachment_descriptors"]
                ),
            }
            if set(manifest_by_path) != expected_manifest_paths:
                raise StateCorruptionError(
                    "proof recovery seed commit artifact coverage is not exact"
                )
            for row in recovery_seed["attachment_descriptors"]:
                artifact_path = str(row["artifact_path"])
                artifact_bytes = artifacts[artifact_path]
                manifest_row = manifest_by_path.get(artifact_path)
                if (
                    bytes_digest(artifact_bytes) != row["sha256"]
                    or len(artifact_bytes) != row["byte_length"]
                    or manifest_row is None
                    or manifest_row.get("sha256") != row["sha256"]
                    or manifest_row.get("size_bytes") != row["byte_length"]
                ):
                    raise StateCorruptionError(
                        "proof recovery seed committed attachment is inconsistent"
                    )
                attached_artifacts.append(
                    {
                        "path": artifact_path,
                        "sha256": row["sha256"],
                        "size_bytes": row["byte_length"],
                    }
                )
        if record["record_kind"] == "proof_execution_terminal_bundle":
            expected_supplemental: dict[str, tuple[str, int]] = {
                str(row["artifact_path"]): (
                    str(row["sha256"]),
                    int(row["byte_length"]),
                )
                for row in record["attachment_descriptors"]
            }
            derived_by_kind = {
                "terminal_receipt": record["terminal_receipt"],
                "receipt_index_membership": record[
                    "receipt_index_membership"
                ],
                "pending_n_plus_one_reflection_request": record[
                    "pending_n_plus_one_reflection_request"
                ],
            }
            for row in record["derived_artifact_descriptors"]:
                artifact_kind = str(row["artifact_kind"])
                expected_bytes = canonical_json(
                    derived_by_kind[artifact_kind]
                )
                if (
                    row["sha256"] != bytes_digest(expected_bytes)
                    or row["byte_length"] != len(expected_bytes)
                ):
                    raise StateCorruptionError(
                        "proof terminal derived artifact descriptor is invalid"
                    )
                expected_supplemental[str(row["artifact_path"])] = (
                    str(row["sha256"]),
                    int(row["byte_length"]),
                )
            manifest_by_path = {
                str(row.get("path")): row
                for row in commit.manifest["artifacts"]
            }
            for artifact_path, (sha256, byte_length) in sorted(
                expected_supplemental.items()
            ):
                artifact_bytes = artifacts[artifact_path]
                manifest_row = manifest_by_path.get(artifact_path)
                if (
                    bytes_digest(artifact_bytes) != sha256
                    or len(artifact_bytes) != byte_length
                    or manifest_row is None
                    or manifest_row.get("sha256") != sha256
                    or manifest_row.get("size_bytes") != byte_length
                ):
                    raise StateCorruptionError(
                        "proof terminal committed attachment is inconsistent"
                    )
                attached_artifacts.append(
                    {
                        "path": artifact_path,
                        "sha256": sha256,
                        "size_bytes": byte_length,
                    }
                )
            state = self._store.read_state(generation)
            if state is None:
                raise StateCorruptionError(
                    "proof terminal commit lost its ledger state"
                )
            reservation = self._validate_proof_reservation_record(
                state["proof_attempt_reservations"].get(
                    record["reservation_id"]
                ),
                expected_id=record["reservation_id"],
            )
            claim = self._validate_proof_execution_claim_record(
                state["proof_execution_claims"].get(
                    record["execution_claim_id"]
                ),
                reservation=reservation,
            )
            raw_checkpoint = state["proof_launch_checkpoints"].get(
                record["reservation_id"]
            )
            checkpoint = (
                None
                if raw_checkpoint is None
                else _validate_launch_checkpoint(
                    raw_checkpoint,
                    reservation=reservation,
                    claim=claim,
                )
            )
            raw_recovery_claim = state.get(
                "proof_terminal_recovery_claims", {}
            ).get(record["reservation_id"])
            recovery_claim = (
                None
                if raw_recovery_claim is None
                else _validate_proof_terminal_recovery_claim(
                    raw_recovery_claim,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                )
            )
            if (
                self._validate_proof_terminal_bundle_record(
                    record,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                    recovery_claim=recovery_claim,
                )
                != dict(record)
            ):
                raise StateCorruptionError(
                    "proof terminal record failed durable bundle replay"
                )
            if (
                state["proof_terminal_bundles"].get(
                    record["reservation_id"]
                )
                != record
            ):
                raise StateCorruptionError(
                    "proof terminal record differs from its durable ledger state"
                )
            from agentic.discovery.proof_execution import (
                replay_proof_terminal_from_durable_bytes,
            )

            try:
                replayed = replay_proof_terminal_from_durable_bytes(
                    record["terminal_projection"],
                    attachment_bytes={
                        str(row["logical_name"]): artifacts[
                            str(row["artifact_path"])
                        ]
                        for row in record["attachment_descriptors"]
                    },
                    expected_reservation=reservation,
                    expected_execution_claim=claim,
                    expected_launch_checkpoint=checkpoint,
                )
            except ContractError as exc:
                raise StateCorruptionError(
                    "proof terminal durable typed replay is invalid"
                ) from exc
            if replayed != record["terminal_projection"]:
                raise StateCorruptionError(
                    "proof terminal durable typed replay changed its projection"
                )
        reference: dict[str, Any] = {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "reference_kind": "portable_coordination_ledger_commit",
            "ledger_kind": LEDGER_KIND,
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "generation": commit.generation,
            "prior_generation": commit.prior_generation,
            "commit_id": commit.commit_id,
            "manifest_digest": commit.manifest_digest,
            "state_file_digest": commit.state_file_digest,
            "state_semantic_digest": commit.state_semantic_digest,
            "record_artifact": {
                "path": path,
                "sha256": descriptor["sha256"],
                "size_bytes": descriptor["size_bytes"],
            },
        }
        if attached_artifacts:
            reference["attached_artifacts"] = attached_artifacts
        reference["reference_digest"] = _self_digest(
            reference, "reference_digest"
        )
        return CoordinationLedgerResult(
            _record_data=memoryview(data).tobytes(),
            _ledger_commit_reference_data=canonical_json(reference),
        )

    def reserve(
        self,
        *,
        theory_commit_reference: Mapping[str, Any],
        theory_graph_reference: Mapping[str, Any],
        schedule_id: str,
        schedule_digest: str,
        action_ids: Sequence[str],
        consumer_id: str,
        n_plus_7_support_root_references: Sequence[Mapping[str, Any]] = (),
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Reserve one exact action set without advancing the theory head."""

        checked_failpoint = _validate_failpoint(failpoint)
        schedule_id = validate_identifier(schedule_id, "schedule_id")
        validate_digest(schedule_digest)
        consumer_id = validate_identifier(consumer_id, "consumer_id")
        actions = _validate_identifier_sequence(
            action_ids,
            label="action_ids",
            ceiling=MAX_ACTIONS_PER_RESERVATION,
        )
        binding = self._freeze_theory_binding(
            theory_commit_reference=theory_commit_reference,
            theory_graph_reference=theory_graph_reference,
            n_plus_7_support_root_references=n_plus_7_support_root_references,
        )
        request_material = {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "request_kind": "reserve_theory_bound_actions",
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "schedule_id": schedule_id,
            "schedule_digest": schedule_digest,
            "action_ids": list(actions),
            "consumer_id": consumer_id,
            "theory_binding_digest": binding["binding_digest"],
        }
        request_digest = canonical_digest(request_material)
        reservation_id = stable_identifier(
            "coordination-reservation-v1", request_material
        )
        idempotency_key = stable_identifier(
            "coordination-reserve-v1", reservation_id, request_digest
        )

        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            existing = state["reservations"].get(reservation_id)
            if existing is not None:
                validated = self._validate_reservation_record(
                    existing, expected_id=reservation_id
                )
                if validated["reservation_request_digest"] != request_digest:
                    raise ActionReservationConflict(
                        "reservation identity was reused with different frozen inputs"
                    )
                return self._result_for_record(validated)
            for action_id in actions:
                claim_id = self._claim_id(schedule_id, action_id)
                owner = state["action_claims"].get(claim_id)
                if owner is not None:
                    raise ActionReservationConflict(
                        f"schedule action is already reserved: {action_id}"
                    )
            if int(state["record_count"]) + 1 > MAX_LEDGER_RECORDS:
                raise ContractError("coordination ledger exceeds the fixed record ceiling")
            # This is the last read-only theory operation before the independent
            # coordination CAS.  A later cross-store race remains deliberately
            # non-authoritative and is caught by the mandatory finalization check.
            self._require_current_theory_head(binding["observed_head"])
            ledger_generation = expected_generation + 1
            reservation: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "action_reservation",
                "reservation_id": reservation_id,
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "ledger_generation": ledger_generation,
                "consumer_id": consumer_id,
                "schedule_id": schedule_id,
                "schedule_digest": schedule_digest,
                "action_ids": list(actions),
                "theory_binding": copy.deepcopy(binding),
                "status": RESERVATION_STATUS,
                "reservation_request_digest": request_digest,
                "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
            }
            reservation["reservation_digest"] = _self_digest(
                reservation, "reservation_digest"
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["reservations"][reservation_id] = reservation
            for action_id in actions:
                claim_id = self._claim_id(schedule_id, action_id)
                next_state["action_claims"][claim_id] = {
                    "schedule_id": schedule_id,
                    "action_id": action_id,
                    "reservation_id": reservation_id,
                }
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=reservation,
                    idempotency_key=idempotency_key,
                    request_digest=request_digest,
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "coordination reservation exhausted the fixed CAS retry ceiling"
        )

    def _prepare_proof_attempt(
        self,
        *,
        theory_authorization: object,
        handoff: Mapping[str, Any],
        attempt_number: int,
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        from agentic.discovery.proof import reopen_current_proof_handoff
        from agentic.discovery.theory_gate import validate_authorization_at_use

        if (
            isinstance(attempt_number, bool)
            or not isinstance(attempt_number, int)
            or attempt_number <= 0
        ):
            raise ContractError("proof attempt_number must be positive")
        authorization = validate_authorization_at_use(
            theory_authorization,
            allowed_statuses=("verified_active_current",),
        )
        current_handoff = reopen_current_proof_handoff(
            theory_authorization, handoff
        )
        if (
            Path(str(authorization["transaction_root"])).resolve()
            != self._theory_store.root
            or authorization["target_id"] != self._store.target_id
            or authorization["run_id"] != self._store.run_id
            or current_handoff["target_id"] != self._store.target_id
            or current_handoff["run_id"] != self._store.run_id
        ):
            raise TheoryHeadBindingError(
                "proof attempt crossed its exact theory or coordination store"
            )
        observed = self._current_theory_head()
        if (
            observed["generation"] != current_handoff["source_commit_generation"]
            or observed["commit_id"] != current_handoff["source_commit_id"]
            or observed["manifest_digest"]
            != current_handoff["source_manifest_digest"]
            or observed["state_file_digest"]
            != current_handoff["source_state_file_digest"]
            or observed["state_semantic_digest"]
            != current_handoff["source_state_semantic_digest"]
        ):
            raise TheoryHeadBindingError(
                "proof attempt source commit is not the current theory head"
            )
        source_binding: dict[str, Any] = {
            "binding_kind": "exact_current_postcommit_proof_action",
            "theory_authorization_digest": current_handoff[
                "theory_authorization_digest"
            ],
            "theory_authorization_basis_digest": current_handoff[
                "theory_authorization_basis_digest"
            ],
            "literature_authority_basis_digest": current_handoff[
                "literature_authority_basis_digest"
            ],
            "source_commit_id": current_handoff["source_commit_id"],
            "source_manifest_digest": current_handoff[
                "source_manifest_digest"
            ],
            "source_state_file_digest": current_handoff[
                "source_state_file_digest"
            ],
            "source_state_semantic_digest": current_handoff[
                "source_state_semantic_digest"
            ],
            "observed_head": observed,
        }
        source_binding["binding_digest"] = _self_digest(
            source_binding, "binding_digest"
        )
        attempt_id = stable_identifier(
            "proof-attempt-v3",
            self._store.target_id,
            self._store.run_id,
            current_handoff["source_commit_id"],
            current_handoff["handoff_id"],
            current_handoff["content_digest"],
            current_handoff["schedule_id"],
            current_handoff["schedule_digest"],
            current_handoff["scheduled_action_id"],
            current_handoff["scheduled_action_digest"],
            attempt_number,
        )
        execution_claim_id = stable_identifier(
            "proof-execution-claim-v2",
            attempt_id,
            current_handoff["content_digest"],
            source_binding["binding_digest"],
        )
        request_material: dict[str, Any] = {
            "schema_version": LEDGER_SCHEMA_VERSION,
            "request_kind": "reserve_one_postcommit_proof_attempt",
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "source_theory_binding_digest": source_binding["binding_digest"],
            "schedule_id": current_handoff["schedule_id"],
            "schedule_digest": current_handoff["schedule_digest"],
            "action_id": current_handoff["scheduled_action_id"],
            "action_digest": current_handoff["scheduled_action_digest"],
            "attempt_id": attempt_id,
            "attempt_number": attempt_number,
            "handoff_id": current_handoff["handoff_id"],
            "handoff_digest": current_handoff["content_digest"],
            "formal_claim_authority_id": current_handoff[
                "formal_claim_authority_id"
            ],
            "formal_claim_authority_digest": current_handoff[
                "formal_claim_authority_digest"
            ],
            "producer_receipt_id": current_handoff["producer_receipt_id"],
            "producer_receipt_digest": current_handoff[
                "producer_receipt_digest"
            ],
            "literature_consume_before": current_handoff[
                "literature_consume_before"
            ],
            "proof_runtime_ref": f"proof-runtime/{attempt_id}",
            "resource_budget_digest": canonical_digest(
                current_handoff["resource_budget"]
            ),
            "execution_claim_id": execution_claim_id,
        }
        request_material["reservation_request_digest"] = canonical_digest(
            request_material
        )
        reservation_id = stable_identifier(
            "proof-attempt-reservation-v2", request_material
        )
        identity = {
            **request_material,
            "reservation_id": reservation_id,
        }
        return current_handoff, source_binding, identity

    def reserve_proof_attempt(
        self,
        *,
        theory_authorization: object,
        handoff: Mapping[str, Any],
        attempt_number: int = 1,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """CAS-reserve one exact prove action and derived attempt identity."""

        checked_failpoint = _validate_failpoint(failpoint)
        current_handoff, source_binding, identity = self._prepare_proof_attempt(
            theory_authorization=theory_authorization,
            handoff=handoff,
            attempt_number=attempt_number,
        )
        reservation_id = identity["reservation_id"]
        request_digest = identity["reservation_request_digest"]
        action_claim_id = self._claim_id(
            identity["schedule_id"], identity["action_id"]
        )
        idempotency_key = stable_identifier(
            "proof-attempt-reserve-v2", reservation_id, request_digest
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            existing = state["proof_attempt_reservations"].get(reservation_id)
            if existing is not None:
                validated = self._validate_proof_reservation_record(
                    existing, expected_id=reservation_id
                )
                if validated["reservation_request_digest"] != request_digest:
                    raise ActionReservationConflict(
                        "proof reservation identity was reused with different inputs"
                    )
                return self._result_for_record(validated)
            owner = state["action_claims"].get(action_claim_id)
            if owner is not None:
                raise ActionReservationConflict(
                    f"schedule prove action is already reserved: {identity['action_id']}"
                )
            attempt_owner = state["attempt_claims"].get(identity["attempt_id"])
            if attempt_owner is not None:
                raise ActionReservationConflict(
                    f"proof attempt is already reserved: {identity['attempt_id']}"
                )
            if int(state["record_count"]) + 1 > MAX_LEDGER_RECORDS:
                raise ContractError("coordination ledger exceeds the fixed record ceiling")
            self._require_current_theory_head(source_binding["observed_head"])
            ledger_generation = expected_generation + 1
            reservation: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_attempt_reservation",
                "reservation_id": reservation_id,
                "execution_claim_id": identity["execution_claim_id"],
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "ledger_generation": ledger_generation,
                "status": PROOF_RESERVATION_STATUS,
                "source_theory_binding": copy.deepcopy(source_binding),
                "schedule_id": identity["schedule_id"],
                "schedule_digest": identity["schedule_digest"],
                "action_id": identity["action_id"],
                "action_digest": identity["action_digest"],
                "attempt_id": identity["attempt_id"],
                "attempt_number": identity["attempt_number"],
                "handoff_id": identity["handoff_id"],
                "handoff_digest": identity["handoff_digest"],
                "formal_claim_authority_id": identity[
                    "formal_claim_authority_id"
                ],
                "formal_claim_authority_digest": identity[
                    "formal_claim_authority_digest"
                ],
                "producer_receipt_id": identity["producer_receipt_id"],
                "producer_receipt_digest": identity["producer_receipt_digest"],
                "literature_consume_before": identity[
                    "literature_consume_before"
                ],
                "proof_runtime_ref": identity["proof_runtime_ref"],
                "resource_budget": copy.deepcopy(
                    current_handoff["resource_budget"]
                ),
                "resource_budget_digest": identity["resource_budget_digest"],
                "reservation_request_digest": request_digest,
                "authority_boundary": copy.deepcopy(
                    _PROOF_COORDINATION_BOUNDARY
                ),
            }
            reservation["reservation_digest"] = _self_digest(
                reservation, "reservation_digest"
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_attempt_reservations"][reservation_id] = reservation
            next_state["action_claims"][action_claim_id] = {
                "schedule_id": identity["schedule_id"],
                "action_id": identity["action_id"],
                "reservation_id": reservation_id,
            }
            next_state["attempt_claims"][identity["attempt_id"]] = {
                "attempt_id": identity["attempt_id"],
                "action_id": identity["action_id"],
                "reservation_id": reservation_id,
            }
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=reservation,
                    idempotency_key=idempotency_key,
                    request_digest=request_digest,
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof-attempt reservation exhausted the fixed CAS retry ceiling"
        )

    def claim_proof_execution(
        self,
        *,
        theory_authorization: object,
        handoff: Mapping[str, Any],
        reservation_id: str,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Consume the one-shot prelaunch claim; an existing claim never reissues."""

        from agentic.discovery.theory_gate import (
            validate_authorization_at_use_with_temporal_evidence,
        )

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(reservation_id, "reservation_id")
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw = state["proof_attempt_reservations"].get(reservation_id)
            if raw is None:
                raise ContractError(f"unknown proof-attempt reservation: {reservation_id}")
            reservation = self._validate_proof_reservation_record(
                raw, expected_id=reservation_id
            )
            current_handoff, source_binding, identity = self._prepare_proof_attempt(
                theory_authorization=theory_authorization,
                handoff=handoff,
                attempt_number=reservation["attempt_number"],
            )
            if (
                identity["reservation_id"] != reservation_id
                or source_binding != reservation["source_theory_binding"]
                or any(
                    identity[field] != reservation[field]
                    for field in (
                        "execution_claim_id",
                        "schedule_id",
                        "schedule_digest",
                        "action_id",
                        "action_digest",
                        "attempt_id",
                        "attempt_number",
                        "handoff_id",
                        "handoff_digest",
                        "formal_claim_authority_id",
                        "formal_claim_authority_digest",
                        "producer_receipt_id",
                        "producer_receipt_digest",
                        "literature_consume_before",
                        "proof_runtime_ref",
                        "resource_budget_digest",
                    )
                )
                or current_handoff["resource_budget"]
                != reservation["resource_budget"]
            ):
                raise ContractError(
                    "proof execution claim differs from its exact live reservation"
                )
            claim_id = reservation["execution_claim_id"]
            if claim_id in state["proof_execution_claims"]:
                raise ProofExecutionClaimConsumed(
                    f"proof execution claim is already consumed: {claim_id}"
                )
            expected_head = reservation["source_theory_binding"]["observed_head"]
            observed_head = self._current_theory_head()
            if observed_head != expected_head:
                raise TheoryHeadBindingError(
                    "theory head changed before proof execution claim"
                )
            (
                claim_authorization,
                evaluated_at,
                clock_authority,
                clock_authority_digest,
            ) = validate_authorization_at_use_with_temporal_evidence(
                theory_authorization,
                allowed_statuses=("verified_active_current",),
            )
            present_decision = claim_authorization.get(
                "present_investment_decision"
            )
            if (
                not isinstance(present_decision, Mapping)
                or claim_authorization.get("authorization_digest")
                != current_handoff["theory_authorization_digest"]
                or claim_authorization.get("authorization_digest")
                != reservation["source_theory_binding"][
                    "theory_authorization_digest"
                ]
                or present_decision.get("consume_before")
                != reservation["literature_consume_before"]
                or present_decision.get("clock_authority") != clock_authority
                or present_decision.get("clock_authority_digest")
                != clock_authority_digest
            ):
                raise ContractError(
                    "proof execution deadline evidence crossed its authorization"
                )
            head_recheck: dict[str, Any] = {
                "recheck_kind": "prelaunch_exact_theory_head_recheck",
                "expected_head": copy.deepcopy(expected_head),
                "observed_head": observed_head,
                "match": True,
            }
            head_recheck["recheck_digest"] = _self_digest(
                head_recheck, "recheck_digest"
            )
            deadline_revalidation: dict[str, Any] = {
                "revalidation_kind": "governed_deadline_revalidated_at_prelaunch",
                "theory_authorization_digest": current_handoff[
                    "theory_authorization_digest"
                ],
                "evaluated_at": evaluated_at.isoformat().replace(
                    "+00:00", "Z"
                ),
                "clock_authority": clock_authority,
                "clock_authority_digest": clock_authority_digest,
                "consume_before": reservation["literature_consume_before"],
                "live_capability_revalidated": True,
                "cross_store_atomicity_claimed": False,
            }
            deadline_revalidation["revalidation_digest"] = _self_digest(
                deadline_revalidation, "revalidation_digest"
            )
            executor_lease = _executor_lease(
                reservation=reservation,
                issued_at=deadline_revalidation["evaluated_at"],
            )
            from agentic.discovery.proof import (
                _proof_prelaunch_capability_material,
            )
            from agentic.discovery.proof_execution import (
                build_proof_claim_recovery_seed_attachments,
            )

            prelaunch_projection = _proof_prelaunch_capability_material(
                handoff=current_handoff,
                reservation_result=self._result_for_record(reservation),
            )
            recovery_seed_bytes = (
                build_proof_claim_recovery_seed_attachments(
                    prelaunch_projection=prelaunch_projection,
                    handoff=current_handoff,
                    reservation=reservation,
                )
            )
            recovery_seed = _build_proof_recovery_seed(
                recovery_seed_bytes,
                attempt_id=reservation["attempt_id"],
                seed_phase="claim_binding",
            )
            ledger_generation = expected_generation + 1
            claim: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_execution_claim",
                "execution_claim_id": claim_id,
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "ledger_generation": ledger_generation,
                "status": PROOF_EXECUTION_CLAIM_STATUS,
                "action_id": reservation["action_id"],
                "action_digest": reservation["action_digest"],
                "attempt_id": reservation["attempt_id"],
                "attempt_number": reservation["attempt_number"],
                "handoff_id": reservation["handoff_id"],
                "handoff_digest": reservation["handoff_digest"],
                "source_theory_head_recheck": head_recheck,
                "deadline_revalidation": deadline_revalidation,
                "executor_lease": executor_lease,
                "recovery_seed": recovery_seed,
                "authority_boundary": copy.deepcopy(
                    _PROOF_COORDINATION_BOUNDARY
                ),
            }
            claim["execution_claim_digest"] = _self_digest(
                claim, "execution_claim_digest"
            )
            self._validate_proof_execution_claim_record(
                claim,
                reservation=reservation,
            )
            request_digest = claim["execution_claim_digest"]
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_execution_claims"][claim_id] = claim
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            namespace = Namespace(
                self._store.target_id,
                self._store.run_id,
                _COORDINATION_BRANCH_ID,
                expected_generation,
            )
            recovery_seed_artifacts = tuple(
                CommitArtifact(
                    relative_path=artifact_path,
                    content=data,
                    namespace=namespace,
                )
                for artifact_path, data in (
                    _validated_proof_recovery_seed_artifacts(
                        recovery_seed,
                        recovery_seed_bytes,
                    )
                )
            )
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=claim,
                    idempotency_key=stable_identifier(
                        "proof-execution-claim-v2", claim_id, request_digest
                    ),
                    request_digest=request_digest,
                    failpoint=checked_failpoint,
                    reject_idempotent_replay=True,
                    extra_artifacts=recovery_seed_artifacts,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof execution claim exhausted the fixed CAS retry ceiling"
        )

    def record_proof_launch_boundary_checkpoint(
        self,
        *,
        binding: object,
        invocation: object,
    ) -> CoordinationLedgerResult:
        """Persist the sole conservative boundary that must precede spawn.

        The checkpoint never says that a process exists.  Its presence means
        only that a later crash may have crossed the launch call; its absence
        proves the current executor contract had not yet reached that call.
        """

        from agentic.discovery.proof_execution import (
            MAX_CHECKER_OUTPUT_BYTES,
            MAX_STAGED_FILE_BYTES,
            ProofExecutionClaimBinding,
            StagedProofInvocation,
            build_staged_proof_invocation_recovery_attachments,
            validate_proof_execution_claim_binding,
            validate_staged_proof_invocation,
        )

        if (
            type(binding) is not ProofExecutionClaimBinding
            or type(invocation) is not StagedProofInvocation
            or invocation.claim_binding != binding
        ):
            raise ContractError(
                "proof launch checkpoint requires exact binding and invocation objects"
            )
        binding_projection = validate_proof_execution_claim_binding(binding)
        invocation_projection = validate_staged_proof_invocation(invocation)
        invocation_recovery_seed_bytes = (
            build_staged_proof_invocation_recovery_attachments(invocation)
        )
        reservation_id = validate_identifier(
            str(binding_projection.get("reservation_id", "")), "reservation_id"
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw_reservation = state["proof_attempt_reservations"].get(
                reservation_id
            )
            if raw_reservation is None:
                raise ContractError(
                    f"unknown proof-attempt reservation: {reservation_id}"
                )
            reservation = self._validate_proof_reservation_record(
                raw_reservation,
                expected_id=reservation_id,
            )
            raw_claim = state["proof_execution_claims"].get(
                reservation["execution_claim_id"]
            )
            if raw_claim is None:
                raise ContractError(
                    "proof launch checkpoint requires a spent execution claim"
                )
            claim = self._validate_proof_execution_claim_record(
                raw_claim,
                reservation=reservation,
            )
            raw_claim_seed = claim.get("recovery_seed")
            if not isinstance(raw_claim_seed, Mapping):
                raise ProofRecoverySeedUnavailable(
                    "proof execution claim predates bounded recovery seed persistence"
                )
            claim_seed = _validate_proof_recovery_seed(
                raw_claim_seed,
                expected_phase="claim_binding",
            )
            invocation_recovery_seed = _build_proof_recovery_seed(
                invocation_recovery_seed_bytes,
                attempt_id=reservation["attempt_id"],
                seed_phase="staged_invocation",
            )
            combined_seed_bytes = (
                int(claim_seed["total_bytes"])
                + int(invocation_recovery_seed["total_bytes"])
            )
            combined_seed_attachments = (
                int(claim_seed["attachment_count"])
                + int(invocation_recovery_seed["attachment_count"])
            )
            if (
                MAX_PROOF_RECOVERY_SEED_BYTES
                + MAX_CHECKER_OUTPUT_BYTES
                + MAX_STAGED_FILE_BYTES
                + PROOF_TERMINAL_METADATA_RESERVE_BYTES
                > MAX_PROOF_TERMINAL_ATTACHMENT_BYTES
            ):
                raise ContractError(
                    "proof recovery and terminal persistence ceilings are misaligned"
                )
            if (
                combined_seed_bytes > MAX_PROOF_RECOVERY_SEED_BYTES
                or combined_seed_attachments
                > MAX_PROOF_RECOVERY_SEED_ATTACHMENTS
            ):
                raise ContractError(
                    "proof staged invocation exceeds its reserved terminal recovery capacity"
                )
            if (
                binding_projection.get("execution_claim_id")
                != claim["execution_claim_id"]
                or binding_projection.get("execution_claim_digest")
                != claim["execution_claim_digest"]
                or binding_projection.get("reservation_digest")
                != reservation["reservation_digest"]
                or binding_projection.get("attempt_id")
                != reservation["attempt_id"]
                or invocation_projection.get("binding_id")
                != binding_projection.get("binding_id")
                or invocation_projection.get("binding_digest")
                != binding_projection.get("content_digest")
                or invocation_projection.get("attempt_id")
                != reservation["attempt_id"]
            ):
                raise ContractError(
                    "proof launch checkpoint crossed its claim or invocation"
                )
            existing = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            if existing is not None:
                validated = _validate_launch_checkpoint(
                    existing,
                    reservation=reservation,
                    claim=claim,
                )
                if (
                    validated["binding_digest"]
                    != binding_projection["content_digest"]
                    or validated["invocation_digest"]
                    != invocation_projection["content_digest"]
                ):
                    raise ProofLaunchCheckpointConflict(
                        "proof attempt already has another launch checkpoint"
                    )
                return self._result_for_record(validated)

            from agentic.discovery.theory_gate import (
                read_proof_recovery_clock_evidence,
            )

            observed_at, clock_authority, clock_digest = (
                read_proof_recovery_clock_evidence()
            )
            lease = _validate_executor_lease(
                claim["executor_lease"],
                reservation=reservation,
            )
            if _parse_canonical_utc_timestamp(
                observed_at, "proof launch checkpoint observed_at"
            ) >= _parse_canonical_utc_timestamp(
                lease["expires_at"], "proof executor lease expires_at"
            ):
                raise ProofExecutorLeaseExpired(
                    "proof executor lease expired before the launch boundary"
                )
            ledger_generation = expected_generation + 1
            checkpoint: dict[str, Any] = {
                "schema_version": "1.0.0",
                "record_kind": "proof_launch_boundary_checkpoint",
                "checkpoint_id": stable_identifier(
                    "proof-launch-boundary-checkpoint-v1",
                    claim["execution_claim_digest"],
                    binding_projection["content_digest"],
                    invocation_projection["content_digest"],
                ),
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim["execution_claim_id"],
                "execution_claim_digest": claim[
                    "execution_claim_digest"
                ],
                "attempt_id": reservation["attempt_id"],
                "ledger_generation": ledger_generation,
                "checkpoint_status": "launch_boundary_entered",
                "binding_id": binding_projection["binding_id"],
                "binding_digest": binding_projection["content_digest"],
                "invocation_id": invocation_projection["invocation_id"],
                "invocation_digest": invocation_projection["content_digest"],
                "executor_lease_id": lease["lease_id"],
                "executor_lease_digest": lease["lease_digest"],
                "lease_expires_at": lease["expires_at"],
                "observed_at": observed_at,
                "clock_authority": clock_authority,
                "clock_authority_digest": clock_digest,
                "lease_active_at_checkpoint": True,
                "launch_may_have_occurred_after_checkpoint": True,
                "launch_observed_by_checkpoint": False,
                "process_evidence_recorded": False,
                "pid_evidence_used": False,
                "respawn_authorized": False,
                "authority_scope": (
                    "conservative_launch_boundary_only_no_process_outcome_claim"
                ),
                "recovery_seed": invocation_recovery_seed,
            }
            checkpoint["checkpoint_digest"] = _self_digest(
                checkpoint, "checkpoint_digest"
            )
            _validate_launch_checkpoint(
                checkpoint,
                reservation=reservation,
                claim=claim,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_launch_checkpoints"][
                reservation_id
            ] = checkpoint
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            namespace = Namespace(
                self._store.target_id,
                self._store.run_id,
                _COORDINATION_BRANCH_ID,
                expected_generation,
            )
            recovery_seed_artifacts = tuple(
                CommitArtifact(
                    relative_path=artifact_path,
                    content=data,
                    namespace=namespace,
                )
                for artifact_path, data in (
                    _validated_proof_recovery_seed_artifacts(
                        invocation_recovery_seed,
                        invocation_recovery_seed_bytes,
                    )
                )
            )
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=checkpoint,
                    idempotency_key=stable_identifier(
                        "proof-launch-boundary-checkpoint-v1",
                        checkpoint["checkpoint_id"],
                    ),
                    request_digest=checkpoint["checkpoint_digest"],
                    failpoint=None,
                    extra_artifacts=recovery_seed_artifacts,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof launch checkpoint exhausted the fixed CAS retry ceiling"
        )

    def _read_proof_recovery_seed_attachment_bytes(
        self,
        record: Mapping[str, Any],
        *,
        expected_phase: str,
    ) -> dict[str, bytes]:
        """Reopen one exact seed only through its verified owning commit."""

        raw_seed = record.get("recovery_seed")
        if not isinstance(raw_seed, Mapping):
            raise ProofRecoverySeedUnavailable(
                f"proof {expected_phase} recovery seed is unavailable"
            )
        seed = _validate_proof_recovery_seed(
            raw_seed,
            expected_phase=expected_phase,
        )
        self._result_for_record(record)
        requested_paths = [
            str(row["artifact_path"])
            for row in seed["attachment_descriptors"]
        ]
        _commit, artifacts = self._store.read_verified_artifacts(
            int(record["ledger_generation"]),
            requested_paths,
        )
        return {
            str(row["logical_name"]): memoryview(
                artifacts[str(row["artifact_path"])]
            ).tobytes()
            for row in seed["attachment_descriptors"]
        }

    def _claim_proof_terminal_recovery(
        self,
        reservation_id: str,
        *,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """CAS-claim one expired terminal gap without granting process authority."""

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw_reservation = state["proof_attempt_reservations"].get(
                reservation_id
            )
            if raw_reservation is None:
                raise ContractError(
                    f"unknown proof-attempt reservation: {reservation_id}"
                )
            reservation = self._validate_proof_reservation_record(
                raw_reservation,
                expected_id=reservation_id,
            )
            raw_claim = state["proof_execution_claims"].get(
                reservation["execution_claim_id"]
            )
            if raw_claim is None:
                raise ContractError(
                    f"proof attempt has no durable execution claim: {reservation_id}"
                )
            claim = self._validate_proof_execution_claim_record(
                raw_claim,
                reservation=reservation,
            )
            raw_checkpoint = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            checkpoint = (
                None
                if raw_checkpoint is None
                else _validate_launch_checkpoint(
                    raw_checkpoint,
                    reservation=reservation,
                    claim=claim,
                )
            )
            raw_existing_recovery = state[
                "proof_terminal_recovery_claims"
            ].get(reservation_id)
            existing_recovery = (
                None
                if raw_existing_recovery is None
                else _validate_proof_terminal_recovery_claim(
                    raw_existing_recovery,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                )
            )
            raw_bundle = state["proof_terminal_bundles"].get(
                reservation_id
            )
            if raw_bundle is not None:
                bundle = self._validate_proof_terminal_bundle_record(
                    raw_bundle,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                    recovery_claim=existing_recovery,
                )
                return self._result_for_record(bundle)
            if existing_recovery is not None:
                return self._result_for_record(existing_recovery)

            raw_claim_seed = claim.get("recovery_seed")
            if not isinstance(raw_claim_seed, Mapping):
                raise ProofRecoverySeedUnavailable(
                    "proof claim has no clean-process recovery seed"
                )
            claim_seed = _validate_proof_recovery_seed(
                raw_claim_seed,
                expected_phase="claim_binding",
            )
            checkpoint_seed: dict[str, Any] | None = None
            if checkpoint is not None:
                raw_checkpoint_seed = checkpoint.get("recovery_seed")
                if not isinstance(raw_checkpoint_seed, Mapping):
                    raise ProofRecoverySeedUnavailable(
                        "proof checkpoint has no clean-process invocation seed"
                    )
                checkpoint_seed = _validate_proof_recovery_seed(
                    raw_checkpoint_seed,
                    expected_phase="staged_invocation",
                )

            from agentic.discovery.theory_gate import (
                read_proof_recovery_clock_evidence,
            )

            observed_at, clock_authority, clock_digest = (
                read_proof_recovery_clock_evidence()
            )
            lease = _validate_executor_lease(
                claim["executor_lease"],
                reservation=reservation,
            )
            observed = _parse_canonical_utc_timestamp(
                observed_at, "proof terminal recovery observed_at"
            )
            expires = _parse_canonical_utc_timestamp(
                lease["expires_at"],
                "proof terminal recovery lease_expires_at",
            )
            if observed < expires:
                raise ProofTerminalRecoveryNotReady(
                    "proof terminal recovery requires the governed expired "
                    "executor lease"
                )
            observation: dict[str, Any] = {
                "observation_kind": (
                    "governed_proof_executor_lease_recovery_observation"
                ),
                "observed_at": observed_at,
                "clock_authority": clock_authority,
                "clock_authority_digest": clock_digest,
                "executor_lease_id": lease["lease_id"],
                "executor_lease_digest": lease["lease_digest"],
                "lease_expires_at": lease["expires_at"],
                "lease_expired": True,
                "investment_deadline_revalidation_not_performed": True,
                "recovery_only": True,
                "caller_supplied_time_used": False,
                "pid_only_death_inference_used": False,
                "respawn_authorized": False,
            }
            observation["observation_digest"] = _self_digest(
                observation, "observation_digest"
            )
            selected_reason = (
                "launch_not_observed_abandoned"
                if checkpoint is None
                else "execution_outcome_unknown_abandoned"
            )
            checkpoint_digest = (
                None
                if checkpoint is None
                else checkpoint["checkpoint_digest"]
            )
            checkpoint_seed_digest = (
                None
                if checkpoint_seed is None
                else checkpoint_seed["seed_digest"]
            )
            recovery_claim_id = stable_identifier(
                "proof-terminal-recovery-claim-v1",
                claim["execution_claim_digest"],
                lease["lease_digest"],
                checkpoint_digest,
                claim_seed["seed_digest"],
                checkpoint_seed_digest,
                observation["observation_digest"],
            )
            ledger_generation = expected_generation + 1
            recovery_claim: dict[str, Any] = {
                "schema_version": "1.0.0",
                "record_kind": "proof_terminal_recovery_claim",
                "recovery_claim_id": recovery_claim_id,
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim["execution_claim_id"],
                "execution_claim_digest": claim[
                    "execution_claim_digest"
                ],
                "attempt_id": reservation["attempt_id"],
                "ledger_generation": ledger_generation,
                "status": PROOF_TERMINAL_RECOVERY_CLAIM_STATUS,
                "executor_lease_id": lease["lease_id"],
                "executor_lease_digest": lease["lease_digest"],
                "launch_boundary_checkpoint_digest": checkpoint_digest,
                "claim_recovery_seed_digest": claim_seed["seed_digest"],
                "checkpoint_recovery_seed_digest": checkpoint_seed_digest,
                "recovery_clock_observation": observation,
                "selected_reason_code": selected_reason,
                "terminal_observed_at": (
                    observed.replace(microsecond=0)
                    .isoformat()
                    .replace("+00:00", "Z")
                ),
                "claim_remains_spent": True,
                "respawn_authorized": False,
                "authority_scope": (
                    "expired_lease_terminalization_only_no_launch_or_respawn"
                ),
            }
            recovery_claim["recovery_claim_digest"] = _self_digest(
                recovery_claim, "recovery_claim_digest"
            )
            _validate_proof_terminal_recovery_claim(
                recovery_claim,
                reservation=reservation,
                claim=claim,
                checkpoint=checkpoint,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_terminal_recovery_claims"][
                reservation_id
            ] = recovery_claim
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=recovery_claim,
                    idempotency_key=stable_identifier(
                        "proof-terminal-recovery-claim-v1",
                        reservation_id,
                        recovery_claim["recovery_claim_digest"],
                    ),
                    request_digest=recovery_claim[
                        "recovery_claim_digest"
                    ],
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof terminal recovery claim exhausted the fixed CAS retry ceiling"
        )

    def recover_proof_terminal_gap(
        self,
        reservation_id: str,
        *,
        failpoint: str | None = None,
        terminal_failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Terminalize one expired claimed gap from durable bytes, never spawn."""

        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        claimed = self._claim_proof_terminal_recovery(
            reservation_id,
            failpoint=failpoint,
        )
        if claimed.record["record_kind"] == (
            "proof_execution_terminal_bundle"
        ):
            return claimed

        _generation, state = self._load_state()
        reservation = self._validate_proof_reservation_record(
            state["proof_attempt_reservations"][reservation_id],
            expected_id=reservation_id,
        )
        claim = self._validate_proof_execution_claim_record(
            state["proof_execution_claims"][
                reservation["execution_claim_id"]
            ],
            reservation=reservation,
        )
        raw_checkpoint = state["proof_launch_checkpoints"].get(
            reservation_id
        )
        checkpoint = (
            None
            if raw_checkpoint is None
            else _validate_launch_checkpoint(
                raw_checkpoint,
                reservation=reservation,
                claim=claim,
            )
        )
        recovery_claim = _validate_proof_terminal_recovery_claim(
            state["proof_terminal_recovery_claims"][reservation_id],
            reservation=reservation,
            claim=claim,
            checkpoint=checkpoint,
        )
        claim_result = self._result_for_record(claim)

        from agentic.discovery.proof_execution import (
            build_proof_execution_terminal_result,
            replay_proof_execution_claim_binding_from_recovery_bytes,
            replay_staged_proof_invocation_from_recovery_bytes,
        )

        binding = (
            replay_proof_execution_claim_binding_from_recovery_bytes(
                attachment_bytes=(
                    self._read_proof_recovery_seed_attachment_bytes(
                        claim,
                        expected_phase="claim_binding",
                    )
                ),
                expected_reservation=reservation,
                execution_claim=claim,
                execution_claim_reference=(
                    claim_result.ledger_commit_reference
                ),
            )
        )
        invocation = (
            None
            if checkpoint is None
            else replay_staged_proof_invocation_from_recovery_bytes(
                binding,
                attachment_bytes=(
                    self._read_proof_recovery_seed_attachment_bytes(
                        checkpoint,
                        expected_phase="staged_invocation",
                    )
                ),
            )
        )
        observed_at = recovery_claim["terminal_observed_at"]
        terminal = build_proof_execution_terminal_result(
            binding,
            terminal_status="abandoned_uncertain",
            execution_status="uncertain",
            proof_verdict="not_evaluated",
            reason_code=recovery_claim["selected_reason_code"],
            started_at=observed_at,
            completed_at=observed_at,
            invocation=invocation,
        )
        return self.finalize_proof_execution(
            terminal,
            failpoint=terminal_failpoint,
        )

    def finalize_proof_execution(
        self,
        terminal_result: object,
        *,
        attachment_bytes: Mapping[str, bytes] | None = None,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Atomically persist one terminal attempt and one inert N+1 request.

        Current finalization requires the exact typed result object.  Serialized
        projection decoders remain history-only and cannot create a bundle.
        The private binding/invocation bytes are persisted for full typed replay
        and can never authorize a retry or respawn.
        """

        from agentic.discovery.proof_execution import (
            ProofExecutionTerminalResult,
            TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT,
            build_proof_terminal_replay_attachments,
            replay_proof_terminal_from_durable_bytes,
            terminal_projection_requires_launch_checkpoint,
            validate_proof_execution_terminal_result,
        )

        checked_failpoint = _validate_failpoint(failpoint)
        if type(terminal_result) is not ProofExecutionTerminalResult:
            raise ContractError(
                "current proof finalization requires one exact typed terminal; "
                "serialized projections are history-only"
            )
        terminal = validate_proof_execution_terminal_result(terminal_result)
        exact_replay_bytes = build_proof_terminal_replay_attachments(
            terminal_result
        )
        if attachment_bytes is not None:
            if not isinstance(attachment_bytes, Mapping):
                raise ContractError(
                    "proof terminal attachment_bytes must be an object"
                )
            supplied = {
                str(name): (
                    memoryview(data).tobytes()
                    if type(data) is bytes
                    else data
                )
                for name, data in attachment_bytes.items()
            }
            if set(supplied) != set(exact_replay_bytes):
                raise ContractError(
                    "proof terminal attachment bytes do not exactly cover "
                    "the typed replay closure"
                )
            if supplied != exact_replay_bytes:
                raise ContractError(
                    "proof terminal attachment differs from exact typed replay bytes"
                )
        reservation_id = validate_identifier(
            terminal["reservation_id"], "reservation_id"
        )
        recovery_authority: dict[str, Any] | None = None
        if terminal["terminal_status"] == "abandoned_uncertain":
            recovery_claim_result = self._claim_proof_terminal_recovery(
                reservation_id
            )
            if recovery_claim_result.record["record_kind"] == (
                "proof_execution_terminal_bundle"
            ):
                if (
                    recovery_claim_result.record.get("terminal_projection")
                    == terminal
                ):
                    return recovery_claim_result
                raise ProofTerminalConflict(
                    "proof reservation already has a different terminal request"
                )
            recovery = self.read_proof_terminal_recovery_state(
                reservation_id
            )
            if recovery["terminal_bundle_present"]:
                reopened = self.read_proof_terminal_bundle(reservation_id)
                if (
                    dict(reopened.record).get("terminal_projection")
                    == terminal
                ):
                    return reopened
                raise ProofTerminalConflict(
                    "proof reservation already has a different terminal request"
                )
            recovery_authority = recovery.get("abandonment_authority")
            if (
                recovery["abandonment_finalization_authorized"] is not True
                or not isinstance(recovery_authority, Mapping)
                or terminal["reason_code"]
                != recovery_authority.get("selected_reason_code")
                or terminal["started_at"]
                != recovery_claim_result.record["terminal_observed_at"]
                or terminal["completed_at"]
                != recovery_claim_result.record["terminal_observed_at"]
                or terminal["process_event"] is not None
                or terminal["resource_receipt"] is not None
                or terminal["checker_output"] is not None
                or terminal["certificate"] is not None
                or terminal["artifacts"]
            ):
                raise ContractError(
                    "abandoned proof finalization requires the exact governed "
                    "expired executor lease classification without fabricated "
                    "process evidence"
                )
            recovery_authority = copy.deepcopy(
                dict(recovery_authority)
            )
        claim_id = validate_identifier(
            terminal["execution_claim_id"], "execution_claim_id"
        )
        attempt_id = validate_identifier(terminal["attempt_id"], "attempt_id")

        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw_reservation = state["proof_attempt_reservations"].get(
                reservation_id
            )
            raw_claim = state["proof_execution_claims"].get(claim_id)
            if raw_reservation is None:
                raise ContractError(
                    f"unknown proof-attempt reservation: {reservation_id}"
                )
            reservation = self._validate_proof_reservation_record(
                raw_reservation,
                expected_id=reservation_id,
            )
            if raw_claim is None:
                raise ContractError(
                    f"unknown proof execution claim: {claim_id}"
                )
            claim = self._validate_proof_execution_claim_record(
                raw_claim,
                reservation=reservation,
            )
            if (
                claim_id != reservation["execution_claim_id"]
                or terminal["reservation_digest"]
                != reservation["reservation_digest"]
                or terminal["execution_claim_digest"]
                != claim["execution_claim_digest"]
                or terminal["attempt_id"] != reservation["attempt_id"]
                or terminal["attempt_number"] != reservation["attempt_number"]
                or terminal["handoff_id"] != reservation["handoff_id"]
                or terminal["handoff_digest"] != reservation["handoff_digest"]
            ):
                raise ContractError(
                    "proof terminal projection crossed its reservation or claim"
                )
            raw_checkpoint = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            checkpoint = (
                None
                if raw_checkpoint is None
                else _validate_launch_checkpoint(
                    raw_checkpoint,
                    reservation=reservation,
                    claim=claim,
                )
            )
            raw_recovery_claim = state[
                "proof_terminal_recovery_claims"
            ].get(reservation_id)
            recovery_claim = (
                None
                if raw_recovery_claim is None
                else _validate_proof_terminal_recovery_claim(
                    raw_recovery_claim,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                )
            )
            if recovery_claim is not None:
                if terminal["terminal_status"] != "abandoned_uncertain":
                    raise ProofTerminalConflict(
                        "proof terminal recovery claim already won the "
                        "reservation terminalization CAS"
                    )
                if (
                    recovery_authority is None
                    or recovery_authority.get("recovery_claim_id")
                    != recovery_claim["recovery_claim_id"]
                    or recovery_authority.get("recovery_claim_digest")
                    != recovery_claim["recovery_claim_digest"]
                ):
                    raise ContractError(
                        "abandoned proof terminal crossed its durable "
                        "recovery claim"
                    )
            elif terminal["terminal_status"] == "abandoned_uncertain":
                raise ContractError(
                    "abandoned proof terminal lacks its durable recovery claim"
                )
            if (
                terminal_projection_requires_launch_checkpoint(terminal)
                and checkpoint is None
            ):
                raise ContractError(
                    "launch-or-later proof terminal lacks its exact durable checkpoint"
                )
            durable_replay_bytes = dict(exact_replay_bytes)
            if checkpoint is not None:
                durable_replay_bytes[
                    TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT
                ] = canonical_json(checkpoint)
            replayed = replay_proof_terminal_from_durable_bytes(
                terminal,
                attachment_bytes=durable_replay_bytes,
                expected_reservation=reservation,
                expected_execution_claim=claim,
                expected_launch_checkpoint=checkpoint,
            )
            if replayed != terminal:
                raise ContractError(
                    "proof terminal typed replay changed its projection"
                )
            descriptors = sorted(
                [
                    *_proof_terminal_attachment_descriptors(
                        terminal,
                        attempt_id=attempt_id,
                    ),
                    *_proof_terminal_replay_attachment_descriptors(
                        durable_replay_bytes,
                        attempt_id=attempt_id,
                    ),
                ],
                key=lambda row: str(row["logical_name"]),
            )
            if (
                len(descriptors) > MAX_PROOF_TERMINAL_ATTACHMENTS
                or sum(int(row["byte_length"]) for row in descriptors)
                > MAX_PROOF_TERMINAL_ATTACHMENT_BYTES
            ):
                raise ContractError(
                    "proof terminal typed replay closure exceeds its ceiling"
                )
            frozen_attachments = _validated_proof_terminal_attachment_bytes(
                terminal,
                descriptors,
                durable_replay_bytes,
            )
            attachment_set_digest = canonical_digest(descriptors)
            request_digest = _proof_terminal_request_digest(
                reservation=reservation,
                claim=claim,
                terminal_projection_digest=terminal["content_digest"],
                attachment_set_digest=attachment_set_digest,
            )
            existing = state["proof_terminal_bundles"].get(reservation_id)
            if existing is not None:
                validated = self._validate_proof_terminal_bundle_record(
                    existing,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                    recovery_claim=recovery_claim,
                )
                if validated["terminal_request_digest"] != request_digest:
                    raise ProofTerminalConflict(
                        "proof reservation already has a different terminal request"
                    )
                return self._result_for_record(validated)

            source_head = _validate_head_observation(
                reservation["source_theory_binding"]["observed_head"],
                target_id=self._store.target_id,
                run_id=self._store.run_id,
            )
            observed_head = self._current_theory_head()
            head_matches = observed_head == source_head
            effective_status = (
                terminal["terminal_status"]
                if head_matches
                else REBASE_REQUIRED_STATUS
            )
            recheck: dict[str, Any] = {
                "recheck_kind": "proof_terminalization_theory_head_recheck",
                "expected_head": source_head,
                "observed_head": observed_head,
                "match": head_matches,
                "disposition_reason": (
                    "head_unchanged" if head_matches else "theory_head_drift"
                ),
                "requested_terminal_status": terminal["terminal_status"],
                "effective_terminal_status": effective_status,
            }
            recheck["recheck_digest"] = _self_digest(
                recheck, "recheck_digest"
            )
            bundle_id = stable_identifier(
                "proof-terminal-bundle-v1",
                reservation["reservation_digest"],
                claim["execution_claim_digest"],
                terminal["content_digest"],
                attachment_set_digest,
                recheck["recheck_digest"],
                effective_status,
            )
            terminalization: dict[str, Any] = {
                "terminalization_kind": (
                    "one_reserved_prove_action_and_attempt_terminalized"
                ),
                "schedule_id": reservation["schedule_id"],
                "schedule_digest": reservation["schedule_digest"],
                "action_id": reservation["action_id"],
                "action_digest": reservation["action_digest"],
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim_id,
                "execution_claim_digest": claim["execution_claim_digest"],
                "attempt_id": reservation["attempt_id"],
                "attempt_number": reservation["attempt_number"],
                "handoff_id": reservation["handoff_id"],
                "handoff_digest": reservation["handoff_digest"],
                "requested_terminal_status": terminal["terminal_status"],
                "effective_terminal_status": effective_status,
                "action_terminalized": True,
                "attempt_terminalized": True,
                "claim_remains_spent": True,
                "respawn_authorized": False,
            }
            terminalization["terminalization_digest"] = _self_digest(
                terminalization, "terminalization_digest"
            )
            receipt_id = stable_identifier(
                "proof-terminal-receipt-v1",
                bundle_id,
                terminal["content_digest"],
                attachment_set_digest,
                recheck["recheck_digest"],
            )
            receipt: dict[str, Any] = {
                "schema_version": "1.0.0",
                "receipt_kind": "proof_execution_terminal_receipt",
                "receipt_id": receipt_id,
                "terminal_bundle_id": bundle_id,
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim_id,
                "execution_claim_digest": claim["execution_claim_digest"],
                "action_id": reservation["action_id"],
                "action_digest": reservation["action_digest"],
                "attempt_id": reservation["attempt_id"],
                "attempt_number": reservation["attempt_number"],
                "handoff_id": reservation["handoff_id"],
                "handoff_digest": reservation["handoff_digest"],
                "terminal_id": terminal["terminal_id"],
                "terminal_projection_digest": terminal["content_digest"],
                "requested_terminal_status": terminal["terminal_status"],
                "effective_terminal_status": effective_status,
                "execution_status": terminal["execution_status"],
                "proof_verdict": terminal["proof_verdict"],
                "reason_code": terminal["reason_code"],
                "attachment_set_digest": attachment_set_digest,
                "source_theory_head_digest": source_head["head_digest"],
                "theory_head_recheck_digest": recheck["recheck_digest"],
                "operational_evidence_only": True,
                "same_cycle_theory_mutation": False,
                "authority_nulls": copy.deepcopy(
                    terminal["authority_nulls"]
                ),
            }
            receipt["receipt_digest"] = _self_digest(
                receipt, "receipt_digest"
            )
            membership: dict[str, Any] = {
                "schema_version": "1.0.0",
                "index_kind": "proof_execution_terminal_receipt_membership",
                "membership_id": stable_identifier(
                    "proof-terminal-membership-v1",
                    self._store.target_id,
                    self._store.run_id,
                    reservation_id,
                    reservation["attempt_id"],
                ),
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "reservation_id": reservation_id,
                "execution_claim_id": claim_id,
                "attempt_id": reservation["attempt_id"],
                "action_id": reservation["action_id"],
                "terminal_bundle_id": bundle_id,
                "terminal_id": terminal["terminal_id"],
                "terminal_projection_digest": terminal["content_digest"],
                "receipt_id": receipt_id,
                "receipt_digest": receipt["receipt_digest"],
                "unique_terminal_for_reservation": True,
                "unique_terminal_for_attempt": True,
            }
            membership["membership_digest"] = _self_digest(
                membership, "membership_digest"
            )
            reflection: dict[str, Any] = {
                "schema_version": "1.0.0",
                "request_kind": (
                    "pending_n_plus_one_proof_result_reflection"
                ),
                "request_id": stable_identifier(
                    "proof-result-reflection-request-v1",
                    reservation_id,
                    claim["execution_claim_digest"],
                    terminal["content_digest"],
                    receipt["receipt_digest"],
                    membership["membership_digest"],
                    source_head["head_digest"],
                ),
                "request_status": "pending",
                "source_theory_head": source_head,
                "finalization_observed_head": observed_head,
                "source_theory_generation": source_head["generation"],
                "requested_n_plus_one_generation": (
                    source_head["generation"] + 1
                ),
                "head_match": head_matches,
                "rebase_required": not head_matches,
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim_id,
                "execution_claim_digest": claim["execution_claim_digest"],
                "schedule_id": reservation["schedule_id"],
                "schedule_digest": reservation["schedule_digest"],
                "action_id": reservation["action_id"],
                "action_digest": reservation["action_digest"],
                "attempt_id": reservation["attempt_id"],
                "attempt_number": reservation["attempt_number"],
                "handoff_id": reservation["handoff_id"],
                "handoff_digest": reservation["handoff_digest"],
                "terminal_bundle_id": bundle_id,
                "terminal_id": terminal["terminal_id"],
                "terminal_projection_digest": terminal["content_digest"],
                "terminal_receipt_id": receipt_id,
                "terminal_receipt_digest": receipt["receipt_digest"],
                "receipt_index_membership_id": membership["membership_id"],
                "receipt_index_membership_digest": membership[
                    "membership_digest"
                ],
                "requested_terminal_status": terminal["terminal_status"],
                "effective_terminal_status": effective_status,
                "execution_status": terminal["execution_status"],
                "proof_verdict": terminal["proof_verdict"],
                "reason_code": terminal["reason_code"],
                "attachment_set_digest": attachment_set_digest,
                "required_theory_generation_relation": (
                    "distinct_descendant_n_plus_one"
                ),
                "same_cycle_theory_mutation_authorized": False,
                "theory_mutation_performed": False,
                "proof_result_intake_consumed": False,
                "epistemic_effect": (
                    "pending_only_no_same_cycle_theory_mutation"
                ),
                "authority_nulls": copy.deepcopy(
                    terminal["authority_nulls"]
                ),
            }
            reflection["request_digest"] = _self_digest(
                reflection, "request_digest"
            )
            derived_descriptors = (
                _proof_terminal_derived_artifact_descriptors(
                    attempt_id=reservation["attempt_id"],
                    terminal_receipt=receipt,
                    receipt_index_membership=membership,
                    pending_n_plus_one_reflection_request=reflection,
                )
            )
            ledger_generation = expected_generation + 1
            bundle: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_execution_terminal_bundle",
                "terminal_bundle_id": bundle_id,
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "execution_claim_id": claim_id,
                "execution_claim_digest": claim["execution_claim_digest"],
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "ledger_generation": ledger_generation,
                "status": effective_status,
                "requested_terminal_status": terminal["terminal_status"],
                "schedule_id": reservation["schedule_id"],
                "schedule_digest": reservation["schedule_digest"],
                "action_id": reservation["action_id"],
                "action_digest": reservation["action_digest"],
                "attempt_id": reservation["attempt_id"],
                "attempt_number": reservation["attempt_number"],
                "handoff_id": reservation["handoff_id"],
                "handoff_digest": reservation["handoff_digest"],
                "source_theory_head": source_head,
                "launch_boundary_checkpoint": copy.deepcopy(checkpoint),
                "terminal_projection": terminal,
                "terminal_projection_digest": terminal["content_digest"],
                "attachment_descriptors": descriptors,
                "attachment_set_digest": attachment_set_digest,
                "lifecycle_terminalization": terminalization,
                "theory_head_recheck": recheck,
                "terminal_receipt": receipt,
                "receipt_index_membership": membership,
                "pending_n_plus_one_reflection_request": reflection,
                "recovery_authority": recovery_authority,
                "derived_artifact_descriptors": derived_descriptors,
                "terminal_request_digest": request_digest,
                "authority_boundary": copy.deepcopy(
                    _PROOF_TERMINAL_BOUNDARY
                ),
            }
            bundle["terminal_bundle_digest"] = _self_digest(
                bundle, "terminal_bundle_digest"
            )
            self._validate_proof_terminal_bundle_record(
                bundle,
                reservation=reservation,
                claim=claim,
                checkpoint=checkpoint,
                recovery_claim=recovery_claim,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_terminal_bundles"][reservation_id] = bundle
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            namespace = Namespace(
                self._store.target_id,
                self._store.run_id,
                _COORDINATION_BRANCH_ID,
                expected_generation,
            )
            extra_artifacts = [
                CommitArtifact(
                    relative_path=artifact_path,
                    content=data,
                    namespace=namespace,
                )
                for artifact_path, data in frozen_attachments
            ]
            derived_values = {
                "terminal_receipt": receipt,
                "receipt_index_membership": membership,
                "pending_n_plus_one_reflection_request": reflection,
            }
            extra_artifacts.extend(
                CommitArtifact(
                    relative_path=str(row["artifact_path"]),
                    content=canonical_json(
                        derived_values[str(row["artifact_kind"])]
                    ),
                    namespace=namespace,
                )
                for row in derived_descriptors
            )
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=bundle,
                    idempotency_key=stable_identifier(
                        "proof-terminal-finalize-v1",
                        reservation_id,
                        request_digest,
                    ),
                    request_digest=request_digest,
                    failpoint=checked_failpoint,
                    extra_artifacts=tuple(extra_artifacts),
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof terminal finalization exhausted the fixed CAS retry ceiling"
        )

    def _build_proof_result_intake_transition(
        self,
        *,
        terminal: Mapping[str, Any],
        intake_claim_id: str,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        tuple[CommitArtifact, CommitArtifact],
    ]:
        """Derive the exact event, state, reconciliation outbox, and plan."""

        from agentic.discovery.ledger import build_event, reduce_from_state

        source_head = _validate_head_observation(
            terminal["source_theory_head"],
            target_id=self._theory_store.target_id,
            run_id=self._theory_store.run_id,
        )
        source_state = self._theory_store.read_state(
            source_head["generation"]
        )
        if source_state is None:
            raise StateCorruptionError(
                "proof-result intake source theory state is absent"
            )
        reflection = _copy_mapping(
            terminal["pending_n_plus_one_reflection_request"],
            "proof-result intake source request",
        )
        payload: dict[str, Any] = {
            "schema_version": "1.0.0",
            "reflection_kind": (
                "proof_result_intake_for_later_semantic_reflection"
            ),
            "intake_claim_id": intake_claim_id,
            "source_request_id": reflection["request_id"],
            "source_request_digest": reflection["request_digest"],
            "source_terminal_bundle_id": terminal["terminal_bundle_id"],
            "source_terminal_bundle_digest": terminal[
                "terminal_bundle_digest"
            ],
            "source_terminal_receipt_id": terminal[
                "terminal_receipt"
            ]["receipt_id"],
            "source_terminal_receipt_digest": terminal[
                "terminal_receipt"
            ]["receipt_digest"],
            "source_theory_generation": source_head["generation"],
            "consumer_theory_generation": source_head["generation"] + 1,
            "intake_status": "consumed_pending_later_reflection",
            "proof_result_intake_consumed": True,
            "semantic_reflection_performed": False,
            "same_cycle_theory_mutation": False,
            "direct_theory_selection": False,
            "direct_theory_status_mutation": False,
            "authority_nulls": {
                "proof_authority": False,
                "checker_soundness_authority": False,
                "truth_authority": False,
                "theorem_authority": False,
                "physics_authority": False,
                "theory_selection_authority": False,
                "same_cycle_mutation_authority": False,
            },
        }
        event = build_event(
            sequence=int(source_state["event_count"]) + 1,
            previous_event_hash=str(source_state["last_event_hash"]),
            namespace=Namespace(
                self._theory_store.target_id,
                self._theory_store.run_id,
                "proof-reflection",
                source_head["generation"],
            ),
            event_type="reflection_recorded",
            entity_type="reflection",
            entity_id=stable_identifier(
                "proof-result-reflection-intake-v1",
                reflection["request_id"],
                intake_claim_id,
            ),
            payload=payload,
            actor="proof-result-reflection-intake-v3",
            source_receipt_ids=[
                terminal["terminal_receipt"]["receipt_id"]
            ],
            occurred_at=terminal["terminal_projection"][
                "completed_at"
            ],
        )
        next_state = reduce_from_state(source_state, [event])
        event_bytes = canonical_json(event)
        artifact_path = (
            "branches/proof-reflection/reflections/"
            f"{reflection['request_id']}.json"
        )
        outbox_id = stable_identifier(
            "proof-result-intake-theory-outbox-v1",
            intake_claim_id,
            terminal["terminal_bundle_digest"],
            reflection["request_digest"],
        )
        outbox_path = (
            "branches/proof-reflection/outbox/"
            f"{outbox_id}.json"
        )
        outbox_core: dict[str, Any] = {
            "schema_version": "1.0.0",
            "outbox_kind": (
                "proof_result_intake_coordination_reconciliation"
            ),
            "outbox_id": outbox_id,
            "intake_claim_id": intake_claim_id,
            "source_theory_head": source_head,
            "requested_descendant_generation": source_head["generation"] + 1,
            "terminal_bundle_id": terminal["terminal_bundle_id"],
            "terminal_bundle_digest": terminal["terminal_bundle_digest"],
            "terminal_receipt_id": terminal["terminal_receipt"]["receipt_id"],
            "terminal_receipt_digest": terminal["terminal_receipt"][
                "receipt_digest"
            ],
            "reflection_request_id": reflection["request_id"],
            "reflection_request_digest": reflection["request_digest"],
            "intake_event_id": event["event_id"],
            "intake_event_hash": event["event_hash"],
            "reconciliation_status": (
                "pending_coordination_consumption"
            ),
            "coordination_consumption_recorded_in_theory": False,
            "semantic_reflection_performed": False,
            "same_cycle_theory_mutation": False,
            "direct_theory_selection": False,
            "authority_nulls": copy.deepcopy(
                payload["authority_nulls"]
            ),
        }
        outbox = {
            **outbox_core,
            "outbox_digest": _self_digest(
                outbox_core, "outbox_digest"
            ),
        }
        outbox_bytes = canonical_json(outbox)
        idempotency_key = stable_identifier(
            "proof-result-intake-theory-commit-v1",
            intake_claim_id,
            reflection["request_id"],
        )
        request_digest = canonical_digest(
            {
                "intake_claim_id": intake_claim_id,
                "source_theory_head_digest": source_head["head_digest"],
                "reflection_request_digest": reflection["request_digest"],
                "intake_event_hash": event["event_hash"],
                "intake_artifact_sha256": bytes_digest(event_bytes),
                "theory_outbox_digest": outbox["outbox_digest"],
                "theory_outbox_artifact_sha256": bytes_digest(
                    outbox_bytes
                ),
                "next_state_semantic_digest": canonical_digest(next_state),
            }
        )
        plan: dict[str, Any] = {
            "plan_kind": "deterministic_pending_reflection_event_commit",
            "source_generation": source_head["generation"],
            "descendant_generation": source_head["generation"] + 1,
            "intake_event_id": event["event_id"],
            "intake_event_hash": event["event_hash"],
            "intake_event_deduplication_key": event[
                "deduplication_key"
            ],
            "intake_artifact_path": artifact_path,
            "intake_artifact_sha256": bytes_digest(event_bytes),
            "intake_artifact_size_bytes": len(event_bytes),
            "theory_outbox_id": outbox_id,
            "theory_outbox_digest": outbox["outbox_digest"],
            "theory_outbox_artifact_path": outbox_path,
            "theory_outbox_artifact_sha256": bytes_digest(outbox_bytes),
            "theory_outbox_artifact_size_bytes": len(outbox_bytes),
            "next_state_semantic_digest": canonical_digest(next_state),
            "theory_commit_idempotency_key": idempotency_key,
            "theory_commit_request_digest": request_digest,
            "direct_theory_selection": False,
            "direct_theory_status_mutation": False,
            "semantic_reflection_performed": False,
        }
        plan["plan_digest"] = _self_digest(plan, "plan_digest")
        event_artifact = CommitArtifact(
            relative_path=artifact_path,
            content=event_bytes,
            namespace=Namespace(
                self._theory_store.target_id,
                self._theory_store.run_id,
                "proof-reflection",
                source_head["generation"],
            ),
        )
        outbox_artifact = CommitArtifact(
            relative_path=outbox_path,
            content=outbox_bytes,
            namespace=Namespace(
                self._theory_store.target_id,
                self._theory_store.run_id,
                "proof-reflection",
                source_head["generation"],
            ),
        )
        return (
            plan,
            event,
            outbox,
            next_state,
            (event_artifact, outbox_artifact),
        )

    @staticmethod
    def _proof_result_intake_outbox_reference(
        plan: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Project the immutable theory-side reconciliation outbox."""

        return {
            "outbox_id": plan["theory_outbox_id"],
            "outbox_digest": plan["theory_outbox_digest"],
            "artifact_path": plan["theory_outbox_artifact_path"],
            "artifact_sha256": plan[
                "theory_outbox_artifact_sha256"
            ],
            "artifact_size_bytes": plan[
                "theory_outbox_artifact_size_bytes"
            ],
        }

    def _reopen_proof_result_intake_descendant(
        self,
        *,
        terminal: Mapping[str, Any],
        intake_claim: Mapping[str, Any],
        descendant_theory_head: Mapping[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Reopen the exact outbox-bearing descendant in the active prefix.

        The theory store is a verified append-only linear prefix.  Once the
        N+1 outbox commit exists, later N+2 or newer theory commits cannot
        invalidate that exact ancestry.  Reconciliation therefore requires
        prefix membership rather than the racy condition that N+1 remain the
        current head until the independent coordination store commits.
        """

        descendant = _validate_head_observation(
            descendant_theory_head,
            target_id=self._theory_store.target_id,
            run_id=self._theory_store.run_id,
        )
        (
            plan,
            event,
            outbox,
            _next_state,
            _artifacts,
        ) = self._build_proof_result_intake_transition(
            terminal=terminal,
            intake_claim_id=intake_claim["intake_claim_id"],
        )
        if plan != intake_claim["transition_plan"]:
            raise StateCorruptionError(
                "proof-result intake plan changed before reconciliation"
            )
        artifact_paths = [
            plan["intake_artifact_path"],
            plan["theory_outbox_artifact_path"],
        ]
        with self._theory_store.verified_artifact_context() as context:
            if context.current_generation < descendant["generation"]:
                raise ProofResultIntakeInactive(
                    "proof-result intake descendant is outside the active "
                    "verified theory prefix"
                )
            reopened, artifact_bytes = context.read_artifacts(
                descendant["generation"],
                artifact_paths,
            )
            current = context.read_commit(context.current_generation)
        reopened_head = _head_observation(reopened)
        current_head = _head_observation(current)
        if (
            reopened_head != descendant
            or reopened.prior_generation != plan["source_generation"]
            or reopened.state_semantic_digest
            != plan["next_state_semantic_digest"]
            or artifact_bytes[plan["intake_artifact_path"]]
            != canonical_json(event)
            or artifact_bytes[plan["theory_outbox_artifact_path"]]
            != canonical_json(outbox)
        ):
            raise StateCorruptionError(
                "proof-result intake descendant or theory outbox failed "
                "exact verified reopening"
            )
        relationship = (
            "current" if current_head == descendant else "verified_ancestor"
        )
        recheck: dict[str, Any] = {
            "recheck_kind": (
                "proof_result_intake_descendant_verified_in_active_prefix"
            ),
            "expected_descendant_head": descendant,
            "observed_current_head": current_head,
            "descendant_relationship": relationship,
            "theory_outbox_digest": outbox["outbox_digest"],
            "match": True,
        }
        recheck["recheck_digest"] = _self_digest(
            recheck, "recheck_digest"
        )
        return (
            descendant,
            self._proof_result_intake_outbox_reference(plan),
            recheck,
        )

    def _inspect_proof_result_intake_slot(
        self,
        *,
        terminal: Mapping[str, Any],
        intake_claim: Mapping[str, Any],
        recorded_observed_head: Mapping[str, Any] | None = None,
    ) -> tuple[bool, dict[str, Any], dict[str, Any]]:
        """Classify the immutable claimed N+1 slot under one verified prefix.

        A matching slot is recognized from the transaction identity, semantic
        state, exact artifact vector, and exact bytes. Merely finding a commit
        at N+1 is never enough to claim that this intake wrote it.
        """

        plan, event, outbox, _next_state, _artifacts = (
            self._build_proof_result_intake_transition(
                terminal=terminal,
                intake_claim_id=intake_claim["intake_claim_id"],
            )
        )
        if plan != intake_claim["transition_plan"]:
            raise StateCorruptionError(
                "proof-result intake plan changed while classifying N+1"
            )
        source_head = intake_claim["source_theory_head"]
        source_generation = int(plan["source_generation"])
        descendant_generation = int(plan["descendant_generation"])
        expected_paths = (
            plan["intake_artifact_path"],
            plan["theory_outbox_artifact_path"],
        )
        recorded = (
            None
            if recorded_observed_head is None
            else _validate_head_observation(
                recorded_observed_head,
                target_id=self._theory_store.target_id,
                run_id=self._theory_store.run_id,
            )
        )
        with self._theory_store.verified_artifact_context() as context:
            if context.current_generation < descendant_generation:
                raise ProofResultIntakeInactive(
                    "claimed proof-result intake N+1 slot is not in the "
                    "active verified theory prefix"
                )
            if (
                recorded is not None
                and context.current_generation < recorded["generation"]
            ):
                raise ProofResultIntakeInactive(
                    "recorded proof-result intake supersession head is not "
                    "in the active verified theory prefix"
                )
            source_commit = context.read_commit(source_generation)
            occupant_commit = context.read_commit(descendant_generation)
            current_commit = context.read_commit(context.current_generation)
            recorded_commit = (
                None
                if recorded is None
                else context.read_commit(recorded["generation"])
            )
            artifact_paths = context.artifact_paths(descendant_generation)
            artifact_bytes: dict[str, bytes] = {}
            if (
                len(artifact_paths) == len(expected_paths)
                and set(artifact_paths) == set(expected_paths)
            ):
                _commit, artifact_bytes = context.read_artifacts(
                    descendant_generation,
                    expected_paths,
                )
        reopened_source = _head_observation(source_commit)
        occupant = _head_observation(occupant_commit)
        current = _head_observation(current_commit)
        if reopened_source != source_head:
            raise StateCorruptionError(
                "proof-result intake source left the active verified prefix"
            )
        if occupant["prior_generation"] != source_generation:
            raise StateCorruptionError(
                "proof-result intake N+1 occupant is not a direct descendant"
            )
        if (
            recorded is not None
            and (
                recorded_commit is None
                or _head_observation(recorded_commit) != recorded
            )
        ):
            raise StateCorruptionError(
                "proof-result intake supersession observation failed exact "
                "active-prefix reopening"
            )
        exact_claimed_transition = (
            occupant_commit.manifest["idempotency_key"]
            == plan["theory_commit_idempotency_key"]
            and occupant_commit.manifest["request_digest"]
            == plan["theory_commit_request_digest"]
            and occupant_commit.state_semantic_digest
            == plan["next_state_semantic_digest"]
            and len(artifact_paths) == len(expected_paths)
            and set(artifact_paths) == set(expected_paths)
            and artifact_bytes.get(plan["intake_artifact_path"])
            == canonical_json(event)
            and artifact_bytes.get(plan["theory_outbox_artifact_path"])
            == canonical_json(outbox)
        )
        return exact_claimed_transition, occupant, current

    def _reopen_proof_result_intake_supersession(
        self,
        *,
        terminal: Mapping[str, Any],
        intake_claim: Mapping[str, Any],
        resolution: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Reopen a terminal loser against the exact active theory prefix."""

        validated = self._validate_proof_result_intake_resolution_record(
            resolution,
            claim=intake_claim,
        )
        exact, occupant, _current = self._inspect_proof_result_intake_slot(
            terminal=terminal,
            intake_claim=intake_claim,
            recorded_observed_head=validated["observed_current_head"],
        )
        if exact:
            raise StateCorruptionError(
                "proof-result intake was superseded despite its exact "
                "transition occupying N+1"
            )
        if occupant != validated["occupying_theory_head"]:
            raise StateCorruptionError(
                "proof-result intake supersession changed its N+1 occupant"
            )
        return validated

    def _claim_proof_result_intake(
        self,
        reservation_id: str,
        *,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Claim one current pending request before touching theory state."""

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw_terminal = state["proof_terminal_bundles"].get(
                reservation_id
            )
            if raw_terminal is None:
                raise ContractError(
                    "proof-result intake requires one current v3 terminal bundle"
                )
            reservation = self._validate_proof_reservation_record(
                state["proof_attempt_reservations"][reservation_id],
                expected_id=reservation_id,
            )
            claim = self._validate_proof_execution_claim_record(
                state["proof_execution_claims"][
                    reservation["execution_claim_id"]
                ],
                reservation=reservation,
            )
            checkpoint_raw = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            checkpoint = (
                None
                if checkpoint_raw is None
                else _validate_launch_checkpoint(
                    checkpoint_raw,
                    reservation=reservation,
                    claim=claim,
                )
            )
            recovery_raw = state[
                "proof_terminal_recovery_claims"
            ].get(reservation_id)
            recovery_claim = (
                None
                if recovery_raw is None
                else _validate_proof_terminal_recovery_claim(
                    recovery_raw,
                    reservation=reservation,
                    claim=claim,
                    checkpoint=checkpoint,
                )
            )
            terminal = self._validate_proof_terminal_bundle_record(
                raw_terminal,
                reservation=reservation,
                claim=claim,
                checkpoint=checkpoint,
                recovery_claim=recovery_claim,
            )
            raw_consumption = state[
                "proof_result_intake_consumptions"
            ].get(reservation_id)
            raw_resolution = state[
                "proof_result_intake_resolutions"
            ].get(reservation_id)
            raw_existing = state["proof_result_intake_claims"].get(
                reservation_id
            )
            if raw_existing is not None:
                existing = self._validate_proof_result_intake_claim_record(
                    raw_existing,
                    terminal=terminal,
                )
                if raw_consumption is not None:
                    consumed = (
                        self._validate_proof_result_intake_consumption_record(
                            raw_consumption,
                            claim=existing,
                        )
                    )
                    return self._result_for_record(consumed)
                if raw_resolution is not None:
                    resolved = self._reopen_proof_result_intake_supersession(
                        terminal=terminal,
                        intake_claim=existing,
                        resolution=raw_resolution,
                    )
                    return self._result_for_record(resolved)
                return self._result_for_record(existing)
            source_head = _validate_head_observation(
                terminal["source_theory_head"],
                target_id=self._theory_store.target_id,
                run_id=self._theory_store.run_id,
            )
            if (
                terminal["status"] == REBASE_REQUIRED_STATUS
                or terminal["theory_head_recheck"]["match"] is not True
                or terminal["pending_n_plus_one_reflection_request"][
                    "head_match"
                ]
                is not True
                or self._current_theory_head() != source_head
            ):
                raise ProofResultIntakeStale(
                    "proof-result intake source theory is not active-current"
                )
            reflection = terminal[
                "pending_n_plus_one_reflection_request"
            ]
            intake_claim_id = stable_identifier(
                "proof-result-intake-claim-v1",
                reservation_id,
                terminal["terminal_bundle_digest"],
                reflection["request_digest"],
                source_head["head_digest"],
            )
            plan, _event, _outbox, _next_state, _artifacts = (
                self._build_proof_result_intake_transition(
                    terminal=terminal,
                    intake_claim_id=intake_claim_id,
                )
            )
            ledger_generation = expected_generation + 1
            intake_claim: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_result_intake_claim",
                "intake_claim_id": intake_claim_id,
                "reservation_id": reservation_id,
                "reservation_digest": terminal["reservation_digest"],
                "execution_claim_id": terminal["execution_claim_id"],
                "execution_claim_digest": terminal[
                    "execution_claim_digest"
                ],
                "attempt_id": terminal["attempt_id"],
                "terminal_bundle_id": terminal["terminal_bundle_id"],
                "terminal_bundle_digest": terminal[
                    "terminal_bundle_digest"
                ],
                "terminal_receipt_id": terminal["terminal_receipt"][
                    "receipt_id"
                ],
                "terminal_receipt_digest": terminal[
                    "terminal_receipt"
                ]["receipt_digest"],
                "reflection_request_id": reflection["request_id"],
                "reflection_request_digest": reflection["request_digest"],
                "source_theory_head": source_head,
                "requested_descendant_generation": (
                    source_head["generation"] + 1
                ),
                "transition_plan": plan,
                "ledger_generation": ledger_generation,
                "status": PROOF_RESULT_INTAKE_CLAIM_STATUS,
                "claim_remains_one_shot": True,
                "coordination_consumed": False,
                "authority_boundary": copy.deepcopy(
                    _PROOF_RESULT_INTAKE_BOUNDARY
                ),
            }
            intake_claim["intake_claim_digest"] = _self_digest(
                intake_claim, "intake_claim_digest"
            )
            self._validate_proof_result_intake_claim_record(
                intake_claim,
                terminal=terminal,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_result_intake_claims"][
                reservation_id
            ] = intake_claim
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=intake_claim,
                    idempotency_key=stable_identifier(
                        "proof-result-intake-claim-v1",
                        reservation_id,
                        intake_claim["intake_claim_digest"],
                    ),
                    request_digest=intake_claim["intake_claim_digest"],
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof-result intake claim exhausted the fixed CAS retry ceiling"
        )

    def _commit_proof_result_intake_theory(
        self,
        reservation_id: str,
        *,
        failpoint: str | None = None,
    ) -> dict[str, Any]:
        """Commit exactly one deterministic N+1 reflection-intake event."""

        checked_failpoint = _validate_failpoint(failpoint)
        _generation, state = self._load_state()
        terminal_raw = state["proof_terminal_bundles"].get(
            reservation_id
        )
        claim_raw = state["proof_result_intake_claims"].get(
            reservation_id
        )
        if terminal_raw is None or claim_raw is None:
            raise ContractError(
                "proof-result theory commit requires its terminal and claim"
            )
        reservation = self._validate_proof_reservation_record(
            state["proof_attempt_reservations"][reservation_id],
            expected_id=reservation_id,
        )
        execution_claim = self._validate_proof_execution_claim_record(
            state["proof_execution_claims"][
                reservation["execution_claim_id"]
            ],
            reservation=reservation,
        )
        checkpoint_raw = state["proof_launch_checkpoints"].get(
            reservation_id
        )
        checkpoint = (
            None
            if checkpoint_raw is None
            else _validate_launch_checkpoint(
                checkpoint_raw,
                reservation=reservation,
                claim=execution_claim,
            )
        )
        recovery_raw = state[
            "proof_terminal_recovery_claims"
        ].get(reservation_id)
        recovery_claim = (
            None
            if recovery_raw is None
            else _validate_proof_terminal_recovery_claim(
                recovery_raw,
                reservation=reservation,
                claim=execution_claim,
                checkpoint=checkpoint,
            )
        )
        terminal = self._validate_proof_terminal_bundle_record(
            terminal_raw,
            reservation=reservation,
            claim=execution_claim,
            checkpoint=checkpoint,
            recovery_claim=recovery_claim,
        )
        intake_claim = self._validate_proof_result_intake_claim_record(
            claim_raw,
            terminal=terminal,
        )
        plan, event, _outbox, next_state, artifacts_to_commit = (
            self._build_proof_result_intake_transition(
                terminal=terminal,
                intake_claim_id=intake_claim["intake_claim_id"],
            )
        )
        if plan != intake_claim["transition_plan"]:
            raise StateCorruptionError(
                "proof-result intake transition changed after its claim"
            )
        try:
            self._theory_store.commit(
                expected_generation=plan["source_generation"],
                state=next_state,
                artifacts=artifacts_to_commit,
                idempotency_key=plan[
                    "theory_commit_idempotency_key"
                ],
                request_digest=plan["theory_commit_request_digest"],
                failpoint=checked_failpoint,
            )
        except (CompareAndSwapError, IdempotencyConflict) as exc:
            raise ProofResultIntakeConflict(
                "proof-result intake lost the distinct descendant theory "
                "commit to a fork"
            ) from exc
        commit = self._theory_store.read_verified_commit(
            plan["descendant_generation"]
        )
        descendant = _head_observation(commit)
        reopened, _outbox_reference, _recheck = (
            self._reopen_proof_result_intake_descendant(
                terminal=terminal,
                intake_claim=intake_claim,
                descendant_theory_head=descendant,
            )
        )
        if commit.state != next_state:
            raise StateCorruptionError(
                "proof-result intake descendant differs from its claim"
            )
        return reopened

    def _finalize_proof_result_intake_consumption(
        self,
        reservation_id: str,
        *,
        descendant_theory_head: Mapping[str, Any],
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Consume coordination once the exact N+1 outbox is in active history."""

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        descendant = _validate_head_observation(
            descendant_theory_head,
            target_id=self._theory_store.target_id,
            run_id=self._theory_store.run_id,
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            claim_raw = state["proof_result_intake_claims"].get(
                reservation_id
            )
            terminal_raw = state["proof_terminal_bundles"].get(
                reservation_id
            )
            if claim_raw is None or terminal_raw is None:
                raise ContractError(
                    "proof-result intake consumption requires its claim"
                )
            reservation = self._validate_proof_reservation_record(
                state["proof_attempt_reservations"][reservation_id],
                expected_id=reservation_id,
            )
            execution_claim = self._validate_proof_execution_claim_record(
                state["proof_execution_claims"][
                    reservation["execution_claim_id"]
                ],
                reservation=reservation,
            )
            checkpoint_raw = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            checkpoint = (
                None
                if checkpoint_raw is None
                else _validate_launch_checkpoint(
                    checkpoint_raw,
                    reservation=reservation,
                    claim=execution_claim,
                )
            )
            recovery_raw = state[
                "proof_terminal_recovery_claims"
            ].get(reservation_id)
            recovery_claim = (
                None
                if recovery_raw is None
                else _validate_proof_terminal_recovery_claim(
                    recovery_raw,
                    reservation=reservation,
                    claim=execution_claim,
                    checkpoint=checkpoint,
                )
            )
            terminal = self._validate_proof_terminal_bundle_record(
                terminal_raw,
                reservation=reservation,
                claim=execution_claim,
                checkpoint=checkpoint,
                recovery_claim=recovery_claim,
            )
            intake_claim = (
                self._validate_proof_result_intake_claim_record(
                    claim_raw,
                    terminal=terminal,
                )
            )
            resolution_raw = state[
                "proof_result_intake_resolutions"
            ].get(reservation_id)
            if resolution_raw is not None:
                resolved = self._reopen_proof_result_intake_supersession(
                    terminal=terminal,
                    intake_claim=intake_claim,
                    resolution=resolution_raw,
                )
                return self._result_for_record(resolved)
            existing_raw = state[
                "proof_result_intake_consumptions"
            ].get(reservation_id)
            if existing_raw is not None:
                existing = (
                    self._validate_proof_result_intake_consumption_record(
                        existing_raw,
                        claim=intake_claim,
                    )
                )
                if existing["descendant_theory_head"] != descendant:
                    raise ProofResultIntakeConflict(
                        "proof-result intake already consumed another descendant"
                    )
                self._reopen_proof_result_intake_descendant(
                    terminal=terminal,
                    intake_claim=intake_claim,
                    descendant_theory_head=descendant,
                )
                return self._result_for_record(existing)
            plan = intake_claim["transition_plan"]
            if (
                descendant["generation"]
                != plan["descendant_generation"]
                or descendant["prior_generation"]
                != plan["source_generation"]
                or descendant["state_semantic_digest"]
                != plan["next_state_semantic_digest"]
            ):
                raise ProofResultIntakeConflict(
                    "proof-result intake descendant crossed its claimed plan"
                )
            descendant, outbox_reference, recheck = (
                self._reopen_proof_result_intake_descendant(
                    terminal=terminal,
                    intake_claim=intake_claim,
                    descendant_theory_head=descendant,
                )
            )
            ledger_generation = expected_generation + 1
            consumption: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_result_intake_consumption",
                "intake_consumption_id": stable_identifier(
                    "proof-result-intake-consumption-v1",
                    intake_claim["intake_claim_digest"],
                    descendant["head_digest"],
                    plan["plan_digest"],
                ),
                "intake_claim_id": intake_claim["intake_claim_id"],
                "intake_claim_digest": intake_claim[
                    "intake_claim_digest"
                ],
                "reservation_id": reservation_id,
                "reservation_digest": intake_claim[
                    "reservation_digest"
                ],
                "execution_claim_id": intake_claim[
                    "execution_claim_id"
                ],
                "attempt_id": intake_claim["attempt_id"],
                "reflection_request_id": intake_claim[
                    "reflection_request_id"
                ],
                "reflection_request_digest": intake_claim[
                    "reflection_request_digest"
                ],
                "source_theory_head": intake_claim[
                    "source_theory_head"
                ],
                "descendant_theory_head": descendant,
                "theory_outbox": outbox_reference,
                "theory_head_recheck": recheck,
                "transition_plan_digest": plan["plan_digest"],
                "ledger_generation": ledger_generation,
                "status": PROOF_RESULT_INTAKE_CONSUMED_STATUS,
                "request_status_before": "pending",
                "request_status_after": "consumed",
                "proof_result_intake_consumed": True,
                "semantic_reflection_performed": False,
                "authority_boundary": copy.deepcopy(
                    _PROOF_RESULT_INTAKE_BOUNDARY
                ),
            }
            consumption["intake_consumption_digest"] = _self_digest(
                consumption, "intake_consumption_digest"
            )
            self._validate_proof_result_intake_consumption_record(
                consumption,
                claim=intake_claim,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_result_intake_consumptions"][
                reservation_id
            ] = consumption
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=consumption,
                    idempotency_key=stable_identifier(
                        "proof-result-intake-consumption-v1",
                        reservation_id,
                        consumption["intake_consumption_digest"],
                    ),
                    request_digest=consumption[
                        "intake_consumption_digest"
                    ],
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof-result intake consumption exhausted the fixed CAS retry ceiling"
        )

    def _terminalize_proof_result_intake_supersession(
        self,
        reservation_id: str,
        *,
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Terminalize a claimed intake whose immutable N+1 slot was lost."""

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            terminal_raw = state["proof_terminal_bundles"].get(
                reservation_id
            )
            claim_raw = state["proof_result_intake_claims"].get(
                reservation_id
            )
            if terminal_raw is None or claim_raw is None:
                raise ContractError(
                    "proof-result intake supersession requires its terminal "
                    "and immutable claim"
                )
            reservation = self._validate_proof_reservation_record(
                state["proof_attempt_reservations"][reservation_id],
                expected_id=reservation_id,
            )
            execution_claim = self._validate_proof_execution_claim_record(
                state["proof_execution_claims"][
                    reservation["execution_claim_id"]
                ],
                reservation=reservation,
            )
            checkpoint_raw = state["proof_launch_checkpoints"].get(
                reservation_id
            )
            checkpoint = (
                None
                if checkpoint_raw is None
                else _validate_launch_checkpoint(
                    checkpoint_raw,
                    reservation=reservation,
                    claim=execution_claim,
                )
            )
            recovery_raw = state[
                "proof_terminal_recovery_claims"
            ].get(reservation_id)
            recovery_claim = (
                None
                if recovery_raw is None
                else _validate_proof_terminal_recovery_claim(
                    recovery_raw,
                    reservation=reservation,
                    claim=execution_claim,
                    checkpoint=checkpoint,
                )
            )
            terminal = self._validate_proof_terminal_bundle_record(
                terminal_raw,
                reservation=reservation,
                claim=execution_claim,
                checkpoint=checkpoint,
                recovery_claim=recovery_claim,
            )
            intake_claim = self._validate_proof_result_intake_claim_record(
                claim_raw,
                terminal=terminal,
            )
            consumption_raw = state[
                "proof_result_intake_consumptions"
            ].get(reservation_id)
            if consumption_raw is not None:
                consumed = (
                    self._validate_proof_result_intake_consumption_record(
                        consumption_raw,
                        claim=intake_claim,
                    )
                )
                self._reopen_proof_result_intake_descendant(
                    terminal=terminal,
                    intake_claim=intake_claim,
                    descendant_theory_head=consumed[
                        "descendant_theory_head"
                    ],
                )
                return self._result_for_record(consumed)
            resolution_raw = state[
                "proof_result_intake_resolutions"
            ].get(reservation_id)
            if resolution_raw is not None:
                resolved = self._reopen_proof_result_intake_supersession(
                    terminal=terminal,
                    intake_claim=intake_claim,
                    resolution=resolution_raw,
                )
                return self._result_for_record(resolved)
            exact, occupant, current = self._inspect_proof_result_intake_slot(
                terminal=terminal,
                intake_claim=intake_claim,
            )
            if exact:
                return self._finalize_proof_result_intake_consumption(
                    reservation_id,
                    descendant_theory_head=occupant,
                    failpoint=checked_failpoint,
                )
            plan = intake_claim["transition_plan"]
            ledger_generation = expected_generation + 1
            resolution: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "proof_result_intake_supersession",
                "resolution_id": stable_identifier(
                    "proof-result-intake-supersession-v1",
                    intake_claim["intake_claim_digest"],
                    occupant["head_digest"],
                    plan["plan_digest"],
                ),
                "intake_claim_id": intake_claim["intake_claim_id"],
                "intake_claim_digest": intake_claim[
                    "intake_claim_digest"
                ],
                "reservation_id": reservation_id,
                "reservation_digest": intake_claim[
                    "reservation_digest"
                ],
                "execution_claim_id": intake_claim[
                    "execution_claim_id"
                ],
                "attempt_id": intake_claim["attempt_id"],
                "reflection_request_id": intake_claim[
                    "reflection_request_id"
                ],
                "reflection_request_digest": intake_claim[
                    "reflection_request_digest"
                ],
                "source_theory_head": intake_claim[
                    "source_theory_head"
                ],
                "claimed_descendant_generation": plan[
                    "descendant_generation"
                ],
                "occupying_theory_head": occupant,
                "observed_current_head": current,
                "transition_plan_digest": plan["plan_digest"],
                "ledger_generation": ledger_generation,
                "status": PROOF_RESULT_INTAKE_SUPERSEDED_STATUS,
                "resolution_reason": (
                    "claimed_n_plus_one_generation_occupied_by_different_"
                    "verified_commit"
                ),
                "source_in_active_prefix": True,
                "coordination_claim_terminalized": True,
                "coordination_consumed": False,
                "claimed_transition_committed": False,
                "theory_outbox_committed": False,
                "semantic_reflection_performed": False,
                "recommission_authorized": False,
                "required_recommission_identity": (
                    "new_formal_claim_schedule_action_reservation_attempt_"
                    "and_intake_claim"
                ),
                "authority_boundary": copy.deepcopy(
                    _PROOF_RESULT_INTAKE_SUPERSESSION_BOUNDARY
                ),
            }
            resolution["resolution_digest"] = _self_digest(
                resolution, "resolution_digest"
            )
            self._validate_proof_result_intake_resolution_record(
                resolution,
                claim=intake_claim,
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["proof_result_intake_resolutions"][
                reservation_id
            ] = resolution
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=resolution,
                    idempotency_key=stable_identifier(
                        "proof-result-intake-supersession-v1",
                        reservation_id,
                        resolution["resolution_digest"],
                    ),
                    request_digest=resolution["resolution_digest"],
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "proof-result intake supersession exhausted the fixed CAS "
            "retry ceiling"
        )

    def recover_proof_result_intake(
        self,
        reservation_id: str,
        *,
        claim_failpoint: str | None = None,
        theory_failpoint: str | None = None,
        consume_failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Recover claim, distinct N+1 commit, and consumption idempotently."""

        claimed = self._claim_proof_result_intake(
            reservation_id,
            failpoint=claim_failpoint,
        )
        if claimed.record["record_kind"] == (
            "proof_result_intake_consumption"
        ):
            return self.read_proof_result_intake_consumption(
                reservation_id
            )
        if claimed.record["record_kind"] == (
            "proof_result_intake_supersession"
        ):
            return self.read_proof_result_intake_resolution(
                reservation_id
            )
        try:
            descendant = self._commit_proof_result_intake_theory(
                reservation_id,
                failpoint=theory_failpoint,
            )
        except ProofResultIntakeConflict:
            return self._terminalize_proof_result_intake_supersession(
                reservation_id,
                failpoint=consume_failpoint,
            )
        return self._finalize_proof_result_intake_consumption(
            reservation_id,
            descendant_theory_head=descendant,
            failpoint=consume_failpoint,
        )

    def consume_proof_result_intake(
        self,
        reservation_id: str,
        *,
        claim_failpoint: str | None = None,
        theory_failpoint: str | None = None,
        consume_failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Consume one proof result; exact retry is the recovery operation."""

        return self.recover_proof_result_intake(
            reservation_id,
            claim_failpoint=claim_failpoint,
            theory_failpoint=theory_failpoint,
            consume_failpoint=consume_failpoint,
        )

    def finalize(
        self,
        reservation_id: str,
        *,
        terminal_status: str,
        terminal_evidence_digests: Sequence[str] = (),
        failpoint: str | None = None,
    ) -> CoordinationLedgerResult:
        """Persist a terminal lifecycle result after mandatory head recheck.

        ``rebase_required`` is derived, never caller supplied.  If the current
        theory head differs from the exact reservation observation, the desired
        lifecycle status is retained as intent but the persisted status is the
        typed rebase result.
        """

        checked_failpoint = _validate_failpoint(failpoint)
        reservation_id = validate_identifier(reservation_id, "reservation_id")
        if terminal_status not in TERMINAL_STATUSES:
            raise ContractError(
                f"unknown requested reservation terminal status: {terminal_status!r}"
            )
        evidence = _validate_digest_sequence(
            terminal_evidence_digests,
            label="terminal_evidence_digests",
            ceiling=MAX_TERMINAL_EVIDENCE_DIGESTS,
        )

        for _attempt in range(MAX_CAS_RETRIES):
            expected_generation, state = self._load_state()
            raw_reservation = state["reservations"].get(reservation_id)
            if raw_reservation is None:
                raise ContractError(f"unknown coordination reservation: {reservation_id}")
            reservation = self._validate_reservation_record(
                raw_reservation, expected_id=reservation_id
            )
            terminal_request_material = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "request_kind": "finalize_theory_bound_actions",
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "requested_terminal_status": terminal_status,
                "terminal_evidence_digests": list(evidence),
            }
            request_digest = canonical_digest(terminal_request_material)
            existing = state["terminal_records"].get(reservation_id)
            if existing is not None:
                validated = self._validate_terminal_record(
                    existing, reservation=reservation
                )
                if validated["terminal_request_digest"] != request_digest:
                    raise ReservationTerminalConflict(
                        "reservation already has a different terminal request"
                    )
                return self._result_for_record(validated)
            if int(state["record_count"]) + 1 > MAX_LEDGER_RECORDS:
                raise ContractError("coordination ledger exceeds the fixed record ceiling")

            expected_head = _validate_head_observation(
                reservation["theory_binding"]["observed_head"],
                target_id=self._store.target_id,
                run_id=self._store.run_id,
            )
            observed_head = self._current_theory_head()
            matches = observed_head == expected_head
            effective_status = (
                terminal_status if matches else REBASE_REQUIRED_STATUS
            )
            recheck: dict[str, Any] = {
                "recheck_kind": "mandatory_theory_head_recheck",
                "expected_head": expected_head,
                "observed_head": observed_head,
                "match": matches,
                "disposition_reason": (
                    "head_unchanged" if matches else "theory_head_drift"
                ),
            }
            recheck["recheck_digest"] = _self_digest(
                recheck, "recheck_digest"
            )
            ledger_generation = expected_generation + 1
            terminal: dict[str, Any] = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "record_kind": "action_reservation_terminal",
                "terminal_id": stable_identifier(
                    "coordination-terminal-v1",
                    terminal_request_material,
                    effective_status,
                    recheck["recheck_digest"],
                ),
                "reservation_id": reservation_id,
                "reservation_digest": reservation["reservation_digest"],
                "target_id": self._store.target_id,
                "run_id": self._store.run_id,
                "ledger_generation": ledger_generation,
                "requested_terminal_status": terminal_status,
                "status": effective_status,
                "terminal_evidence_digests": list(evidence),
                "theory_head_recheck": recheck,
                "terminal_request_digest": request_digest,
                "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
            }
            terminal["terminal_digest"] = _self_digest(
                terminal, "terminal_digest"
            )
            next_state = copy.deepcopy(state)
            next_state["generation"] = ledger_generation
            next_state["terminal_records"][reservation_id] = terminal
            next_state["record_count"] = int(state["record_count"]) + 1
            self._ensure_state_ceiling(next_state)
            idempotency_key = stable_identifier(
                "coordination-finalize-v1", reservation_id, request_digest
            )
            try:
                return self._commit_record(
                    expected_generation=expected_generation,
                    state=next_state,
                    record=terminal,
                    idempotency_key=idempotency_key,
                    request_digest=request_digest,
                    failpoint=checked_failpoint,
                )
            except (CompareAndSwapError, IdempotencyConflict):
                continue
        raise CoordinationConcurrencyError(
            "coordination finalization exhausted the fixed CAS retry ceiling"
        )

    def read_reservation(self, reservation_id: str) -> CoordinationLedgerResult:
        reservation_id = validate_identifier(reservation_id, "reservation_id")
        _generation, state = self._load_state()
        record = state["reservations"].get(reservation_id)
        if record is None:
            raise ContractError(f"unknown coordination reservation: {reservation_id}")
        validated = self._validate_reservation_record(
            record, expected_id=reservation_id
        )
        return self._result_for_record(validated)

    def read_terminal(self, reservation_id: str) -> CoordinationLedgerResult:
        reservation_id = validate_identifier(reservation_id, "reservation_id")
        _generation, state = self._load_state()
        reservation = state["reservations"].get(reservation_id)
        terminal = state["terminal_records"].get(reservation_id)
        if reservation is None or terminal is None:
            raise ContractError(
                f"coordination reservation has no terminal record: {reservation_id}"
            )
        validated_reservation = self._validate_reservation_record(
            reservation, expected_id=reservation_id
        )
        validated = self._validate_terminal_record(
            terminal, reservation=validated_reservation
        )
        return self._result_for_record(validated)

    def read_proof_attempt(
        self, reservation_id: str
    ) -> CoordinationLedgerResult:
        """Reopen one immutable proof-attempt reservation projection."""

        reservation_id = validate_identifier(reservation_id, "reservation_id")
        _generation, state = self._load_state()
        record = state["proof_attempt_reservations"].get(reservation_id)
        if record is None:
            raise ContractError(f"unknown proof-attempt reservation: {reservation_id}")
        validated = self._validate_proof_reservation_record(
            record, expected_id=reservation_id
        )
        return self._result_for_record(validated)

    def read_proof_execution_claim(
        self, execution_claim_id: str
    ) -> CoordinationLedgerResult:
        """Reopen consumed-claim evidence without reissuing launch authority."""

        execution_claim_id = validate_identifier(
            execution_claim_id, "execution_claim_id"
        )
        _generation, state = self._load_state()
        record = state["proof_execution_claims"].get(execution_claim_id)
        if record is None:
            raise ContractError(
                f"unknown proof execution claim: {execution_claim_id}"
            )
        reservation = state["proof_attempt_reservations"].get(
            record.get("reservation_id")
        )
        if reservation is None:
            raise StateCorruptionError(
                "proof execution claim lost its reservation"
            )
        validated_reservation = self._validate_proof_reservation_record(
            reservation, expected_id=str(reservation["reservation_id"])
        )
        validated = self._validate_proof_execution_claim_record(
            record, reservation=validated_reservation
        )
        return self._result_for_record(validated)

    def read_proof_terminal_recovery_state(
        self, reservation_id: str
    ) -> dict[str, Any]:
        """Describe a spent claim's terminal gap without authorizing recovery.

        A durable claim is sufficient to forbid every respawn, but it does not
        prove that an executor is dead or that a governed lease expired.  This
        read-only projection therefore makes the gap explicit and names the two
        future abandonment routes without treating caller time or missing local
        process state as recovery authority.
        """

        reservation_id = validate_identifier(reservation_id, "reservation_id")
        _generation, state = self._load_state()
        reservation = state["proof_attempt_reservations"].get(reservation_id)
        if reservation is None:
            raise ContractError(
                f"unknown proof-attempt reservation: {reservation_id}"
            )
        validated_reservation = self._validate_proof_reservation_record(
            reservation,
            expected_id=reservation_id,
        )
        claim_id = validated_reservation["execution_claim_id"]
        claim = state["proof_execution_claims"].get(claim_id)
        if claim is None:
            raise ContractError(
                f"proof attempt has no durable execution claim: {reservation_id}"
            )
        validated_claim = self._validate_proof_execution_claim_record(
            claim,
            reservation=validated_reservation,
        )
        raw_checkpoint = state["proof_launch_checkpoints"].get(
            reservation_id
        )
        validated_checkpoint = (
            None
            if raw_checkpoint is None
            else _validate_launch_checkpoint(
                raw_checkpoint,
                reservation=validated_reservation,
                claim=validated_claim,
            )
        )
        raw_recovery_claim = state.get(
            "proof_terminal_recovery_claims", {}
        ).get(reservation_id)
        validated_recovery_claim = (
            None
            if raw_recovery_claim is None
            else _validate_proof_terminal_recovery_claim(
                raw_recovery_claim,
                reservation=validated_reservation,
                claim=validated_claim,
                checkpoint=validated_checkpoint,
            )
        )
        raw_bundle = state["proof_terminal_bundles"].get(reservation_id)
        validated_bundle: dict[str, Any] | None = None
        if raw_bundle is not None:
            validated_bundle = self._validate_proof_terminal_bundle_record(
                raw_bundle,
                reservation=validated_reservation,
                claim=validated_claim,
                checkpoint=validated_checkpoint,
                recovery_claim=validated_recovery_claim,
            )
        from agentic.discovery.theory_gate import (
            read_proof_recovery_clock_evidence,
        )

        lease = _validate_executor_lease(
            validated_claim["executor_lease"],
            reservation=validated_reservation,
        )
        if validated_recovery_claim is None:
            observed_at, clock_authority, clock_digest = (
                read_proof_recovery_clock_evidence()
            )
            observed_instant = _parse_canonical_utc_timestamp(
                observed_at, "proof recovery observed_at"
            )
            expires_instant = _parse_canonical_utc_timestamp(
                lease["expires_at"], "proof executor lease expires_at"
            )
            lease_expired = observed_instant >= expires_instant
            clock_observation: dict[str, Any] = {
                "observation_kind": (
                    "governed_proof_executor_lease_recovery_observation"
                ),
                "observed_at": observed_at,
                "clock_authority": clock_authority,
                "clock_authority_digest": clock_digest,
                "executor_lease_id": lease["lease_id"],
                "executor_lease_digest": lease["lease_digest"],
                "lease_expires_at": lease["expires_at"],
                "lease_expired": lease_expired,
                "investment_deadline_revalidation_not_performed": True,
                "recovery_only": True,
                "caller_supplied_time_used": False,
                "pid_only_death_inference_used": False,
                "respawn_authorized": False,
            }
            clock_observation["observation_digest"] = _self_digest(
                clock_observation, "observation_digest"
            )
        else:
            clock_observation = copy.deepcopy(
                validated_recovery_claim["recovery_clock_observation"]
            )
            lease_expired = True
        selected_reason = (
            None
            if validated_recovery_claim is None
            else validated_recovery_claim["selected_reason_code"]
        )
        abandonment_authority: dict[str, Any] | None = None
        if (
            validated_bundle is None
            and validated_recovery_claim is not None
        ):
            abandonment_authority = {
                "authority_kind": (
                    "expired_executor_lease_abandonment_authority"
                ),
                "reservation_id": reservation_id,
                "execution_claim_id": claim_id,
                "execution_claim_digest": validated_claim[
                    "execution_claim_digest"
                ],
                "recovery_claim_id": validated_recovery_claim[
                    "recovery_claim_id"
                ],
                "recovery_claim_digest": validated_recovery_claim[
                    "recovery_claim_digest"
                ],
                "executor_lease": copy.deepcopy(lease),
                "recovery_clock_observation": copy.deepcopy(
                    clock_observation
                ),
                "launch_boundary_checkpoint": copy.deepcopy(
                    validated_checkpoint
                ),
                "selected_reason_code": selected_reason,
                "process_evidence_available": False,
                "process_evidence_fabrication_allowed": False,
                "caller_time_authority": False,
                "pid_only_death_authority": False,
                "respawn_authorized": False,
                "proof_authority": False,
                "theory_mutation_authority": False,
            }
            abandonment_authority["authority_digest"] = _self_digest(
                abandonment_authority, "authority_digest"
            )
        recovery_state: dict[str, Any] = {
            "schema_version": "1.0.0",
            "recovery_state_kind": (
                "proof_claim_terminal_recovery_observation"
            ),
            "target_id": self._store.target_id,
            "run_id": self._store.run_id,
            "reservation_id": reservation_id,
            "reservation_digest": validated_reservation[
                "reservation_digest"
            ],
            "execution_claim_id": claim_id,
            "execution_claim_digest": validated_claim[
                "execution_claim_digest"
            ],
            "schedule_id": validated_reservation["schedule_id"],
            "schedule_digest": validated_reservation["schedule_digest"],
            "action_id": validated_reservation["action_id"],
            "action_digest": validated_reservation["action_digest"],
            "attempt_id": validated_reservation["attempt_id"],
            "attempt_number": validated_reservation["attempt_number"],
            "handoff_id": validated_reservation["handoff_id"],
            "handoff_digest": validated_reservation["handoff_digest"],
            "source_theory_head": copy.deepcopy(
                validated_reservation["source_theory_binding"][
                    "observed_head"
                ]
            ),
            "claim_deadline_revalidation": copy.deepcopy(
                validated_claim["deadline_revalidation"]
            ),
            "executor_lease": lease,
            "launch_boundary_checkpoint": copy.deepcopy(
                validated_checkpoint
            ),
            "recovery_claim_present": (
                validated_recovery_claim is not None
            ),
            "recovery_claim_id": (
                None
                if validated_recovery_claim is None
                else validated_recovery_claim["recovery_claim_id"]
            ),
            "recovery_claim_digest": (
                None
                if validated_recovery_claim is None
                else validated_recovery_claim["recovery_claim_digest"]
            ),
            "recovery_clock_observation": clock_observation,
            "status": (
                "claimed_without_terminal"
                if validated_bundle is None
                else "terminal_bundle_recovered"
            ),
            "terminal_bundle_present": validated_bundle is not None,
            "terminal_bundle_id": (
                None
                if validated_bundle is None
                else validated_bundle["terminal_bundle_id"]
            ),
            "terminal_bundle_digest": (
                None
                if validated_bundle is None
                else validated_bundle["terminal_bundle_digest"]
            ),
            "terminal_status": (
                None
                if validated_bundle is None
                else validated_bundle["status"]
            ),
            "claim_remains_spent": True,
            "respawn_authorized": False,
            "abandonment_finalization_authorized": (
                abandonment_authority is not None
            ),
            "abandonment_authority": abandonment_authority,
            "selected_abandonment_reason_code": (
                None
                if abandonment_authority is None
                else selected_reason
            ),
            "abandonment_authority_status": (
                "available_from_cas_claimed_governed_expired_executor_lease"
                if abandonment_authority is not None
                else "available_for_cas_recovery_claim"
                if validated_bundle is None and lease_expired
                else "unavailable_before_governed_executor_lease_expiry"
                if validated_bundle is None and not lease_expired
                else "not_applicable_already_terminal"
            ),
            "caller_supplied_time_allowed": False,
            "required_recovery_paths": [
                {
                    "reason_code": "launch_not_observed_abandoned",
                    "process_evidence_required": False,
                    "governed_condition_required": (
                        "expired_executor_lease"
                    ),
                },
                {
                    "reason_code": "execution_outcome_unknown_abandoned",
                    "process_evidence_required": False,
                    "governed_condition_required": (
                        "expired_executor_lease"
                    ),
                },
            ],
            "same_cycle_theory_mutation_authorized": False,
            "theory_mutation_performed": False,
            "authority_nulls": {
                "launch_authority": False,
                "respawn_authority": False,
                "dead_owner_inference": False,
                "caller_time_authority": False,
                "proof_truth_authority": False,
                "checker_soundness_authority": False,
                "theorem_authority": False,
                "physics_authority": False,
            },
        }
        recovery_state["recovery_state_digest"] = canonical_digest(
            recovery_state
        )
        return recovery_state

    def read_proof_terminal_bundle(
        self, reservation_id: str
    ) -> CoordinationLedgerResult:
        """Reopen terminal evidence without reissuing proof launch authority."""

        reservation_id = validate_identifier(reservation_id, "reservation_id")
        _generation, state = self._load_state()
        reservation = state["proof_attempt_reservations"].get(reservation_id)
        bundle = state["proof_terminal_bundles"].get(reservation_id)
        if reservation is None or bundle is None:
            raise ContractError(
                f"proof reservation has no terminal bundle: {reservation_id}"
            )
        validated_reservation = self._validate_proof_reservation_record(
            reservation,
            expected_id=reservation_id,
        )
        claim = state["proof_execution_claims"].get(
            validated_reservation["execution_claim_id"]
        )
        if claim is None:
            raise StateCorruptionError(
                "proof terminal bundle lost its execution claim"
            )
        validated_claim = self._validate_proof_execution_claim_record(
            claim,
            reservation=validated_reservation,
        )
        raw_checkpoint = state["proof_launch_checkpoints"].get(
            reservation_id
        )
        validated_checkpoint = (
            None
            if raw_checkpoint is None
            else _validate_launch_checkpoint(
                raw_checkpoint,
                reservation=validated_reservation,
                claim=validated_claim,
            )
        )
        raw_recovery_claim = state.get(
            "proof_terminal_recovery_claims", {}
        ).get(reservation_id)
        validated_recovery_claim = (
            None
            if raw_recovery_claim is None
            else _validate_proof_terminal_recovery_claim(
                raw_recovery_claim,
                reservation=validated_reservation,
                claim=validated_claim,
                checkpoint=validated_checkpoint,
            )
        )
        validated = self._validate_proof_terminal_bundle_record(
            bundle,
            reservation=validated_reservation,
            claim=validated_claim,
            checkpoint=validated_checkpoint,
            recovery_claim=validated_recovery_claim,
        )
        return self._result_for_record(validated)

    def read_proof_result_intake_claim(
        self, reservation_id: str
    ) -> CoordinationLedgerResult:
        """Reopen one pending or already-consumed intake claim."""

        reservation_id = validate_identifier(
            reservation_id, "reservation_id"
        )
        _generation, state = self._load_state()
        terminal_raw = state["proof_terminal_bundles"].get(
            reservation_id
        )
        claim_raw = state["proof_result_intake_claims"].get(
            reservation_id
        )
        if terminal_raw is None or claim_raw is None:
            raise ContractError(
                f"proof reservation has no result-intake claim: {reservation_id}"
            )
        reservation = self._validate_proof_reservation_record(
            state["proof_attempt_reservations"][reservation_id],
            expected_id=reservation_id,
        )
        execution_claim = self._validate_proof_execution_claim_record(
            state["proof_execution_claims"][
                reservation["execution_claim_id"]
            ],
            reservation=reservation,
        )
        checkpoint_raw = state["proof_launch_checkpoints"].get(
            reservation_id
        )
        checkpoint = (
            None
            if checkpoint_raw is None
            else _validate_launch_checkpoint(
                checkpoint_raw,
                reservation=reservation,
                claim=execution_claim,
            )
        )
        recovery_raw = state[
            "proof_terminal_recovery_claims"
        ].get(reservation_id)
        recovery_claim = (
            None
            if recovery_raw is None
            else _validate_proof_terminal_recovery_claim(
                recovery_raw,
                reservation=reservation,
                claim=execution_claim,
                checkpoint=checkpoint,
            )
        )
        terminal = self._validate_proof_terminal_bundle_record(
            terminal_raw,
            reservation=reservation,
            claim=execution_claim,
            checkpoint=checkpoint,
            recovery_claim=recovery_claim,
        )
        claim = self._validate_proof_result_intake_claim_record(
            claim_raw,
            terminal=terminal,
        )
        return self._result_for_record(claim)

    def read_proof_result_intake_consumption(
        self, reservation_id: str
    ) -> CoordinationLedgerResult:
        """Reopen exact consumed coordination and descendant evidence."""

        claim_result = self.read_proof_result_intake_claim(
            reservation_id
        )
        _generation, state = self._load_state()
        raw = state["proof_result_intake_consumptions"].get(
            reservation_id
        )
        if raw is None:
            raise ContractError(
                "proof reservation result intake is not consumed"
            )
        consumed = (
            self._validate_proof_result_intake_consumption_record(
                raw,
                claim=claim_result.record,
            )
        )
        terminal_result = self.read_proof_terminal_bundle(reservation_id)
        descendant, outbox_reference, _recheck = (
            self._reopen_proof_result_intake_descendant(
                terminal=terminal_result.record,
                intake_claim=claim_result.record,
                descendant_theory_head=consumed[
                    "descendant_theory_head"
                ],
            )
        )
        if (
            descendant != consumed["descendant_theory_head"]
            or outbox_reference != consumed["theory_outbox"]
        ):
            raise StateCorruptionError(
                "proof-result intake consumed descendant failed reopening"
            )
        return self._result_for_record(consumed)

    def read_proof_result_intake_resolution(
        self, reservation_id: str
    ) -> CoordinationLedgerResult:
        """Reopen a terminal supersession against exact active-prefix heads."""

        claim_result = self.read_proof_result_intake_claim(
            reservation_id
        )
        _generation, state = self._load_state()
        raw = state["proof_result_intake_resolutions"].get(
            reservation_id
        )
        if raw is None:
            raise ContractError(
                "proof reservation result intake is not superseded"
            )
        terminal_result = self.read_proof_terminal_bundle(reservation_id)
        resolved = self._reopen_proof_result_intake_supersession(
            terminal=terminal_result.record,
            intake_claim=claim_result.record,
            resolution=raw,
        )
        return self._result_for_record(resolved)


__all__ = [
    "ActionCoordinationLedger",
    "ActionReservationConflict",
    "CoordinationConcurrencyError",
    "CoordinationLedgerResult",
    "CoordinationStoreBoundaryError",
    "LEDGER_KIND",
    "LEGACY_LEDGER_SCHEMA_VERSION",
    "MAX_ACTIONS_PER_RESERVATION",
    "MAX_CAS_RETRIES",
    "MAX_LEDGER_RECORDS",
    "MAX_LEDGER_STATE_BYTES",
    "MAX_PROOF_RECORD_BYTES",
    "MAX_PROOF_RECOVERY_SEED_ATTACHMENTS",
    "MAX_PROOF_RECOVERY_SEED_BYTES",
    "MAX_PROOF_TERMINAL_ATTACHMENTS",
    "MAX_PROOF_TERMINAL_ATTACHMENT_BYTES",
    "MAX_PROOF_EXECUTOR_LEASE_SECONDS",
    "MAX_RECORD_BYTES",
    "MAX_REFERENCE_BYTES",
    "MAX_SUPPORT_ROOT_REFERENCES",
    "MAX_TERMINAL_EVIDENCE_DIGESTS",
    "MAX_THEORY_BINDING_BYTES",
    "REBASE_REQUIRED_STATUS",
    "RESERVATION_STATUS",
    "PROOF_EXECUTION_CLAIM_STATUS",
    "PROOF_RESULT_INTAKE_CLAIM_STATUS",
    "PROOF_RESULT_INTAKE_CONSUMED_STATUS",
    "PROOF_RESULT_INTAKE_SUPERSEDED_STATUS",
    "PROOF_EXECUTOR_RECOVERY_MARGIN_SECONDS",
    "PROOF_RESERVATION_STATUS",
    "ProofExecutionClaimConsumed",
    "ProofExecutorLeaseExpired",
    "ProofLaunchCheckpointConflict",
    "ProofRecoverySeedUnavailable",
    "ProofResultIntakeConflict",
    "ProofResultIntakeInactive",
    "ProofResultIntakeStale",
    "ProofTerminalConflict",
    "ProofTerminalRecoveryNotReady",
    "ReservationTerminalConflict",
    "TERMINAL_STATUSES",
    "TheoryHeadBindingError",
]
