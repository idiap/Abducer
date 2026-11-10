# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Reservation-first execution of one frozen discovery-scheduler wave.

This module is the operational seam between a theory-first discovery schedule
and callbacks that can perform expensive or external work.  It deliberately
does not add scientific authority:

* the complete scheduler output and selected wave are validated before use;
* the action-kind policy, not a caller flag, decides whether the wave is
  theory-only or consumes a completed N+7 support aggregation;
* one exact action set is durably reserved in
  :class:`ActionCoordinationLedger` before any callback can run;
* a selected ``prove`` action is rejected for the dedicated attempt-specific
  proof-execution boundary instead of being exposed to a generic callback;
* every compliant callback path requests a durable terminal lifecycle; and
* the ledger alone derives ``rebase_required`` from its final point-in-time
  theory-head observation.

The support distinction avoids a causal circle.  ``probe`` is theory-only at
reservation time because it produces the later N+1 through N+7 support suffix.
Only ``reflect`` and ``reframe`` can consume an existing support suffix, and
they do so only when their frozen action contains both the closed
``requires_n_plus_7_support`` restriction and the exact aggregation-root
object-ID vector.  A separate boolean or caller-selected support vector is
never accepted.

The boundary is exactly-once only for callers that use this module and the
same coordination root.  Its advisory lock serializes reserve/callback/finalize
lifecycles across such callers while callbacks inside a declared parallel wave
still run concurrently.  The theory store and coordination store remain
separate: there is no cross-store atomicity, a theory head can change after the
terminal recheck, and neither a callback result nor a terminal record grants
truth, proof, experiment, selection, promotion, or physics authority.
"""

from __future__ import annotations

import copy
import dataclasses
import fcntl
import json
import os
import stat
from collections.abc import Callable, Iterator, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from types import MappingProxyType
from typing import Any

from agentic.discovery import action_coordination_ledger as ledger_protocol
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    CoordinationLedgerResult,
)
from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_digest,
    validate_identifier,
)
from agentic.discovery.scheduler import ACTION_KINDS


BOUNDARY_VERSION = "discovery-action-execution-boundary/1.0.0"
POST_RESULT_SUPPORT_MARKER = "requires_n_plus_7_support"
SUPPORT_ROOT_IDENTITY_FIELD = "n_plus_7_support_root_object_ids"
AGGREGATION_ROOT_KIND = "world_matrix_aggregation_root_v3"
MAX_PARALLEL_WORKERS = 32

_SCHEDULE_VERSION = "discovery-information-scheduler/2.0.0"
_WAVE_MODES = frozenset(
    {"parallel", "serial", "serial_constraint", "serial_gate"}
)
_CALLBACK_STATUSES = frozenset(
    {"completed", "failed", "released", "compensation_required"}
)
_SUPPORT_MARKER_KINDS = frozenset({"reflect", "reframe"})
_SCHEDULE_FIELDS = frozenset(
    {
        "scheduler_version",
        "target_id",
        "state_version",
        "input_digest",
        "schedule_id",
        "literature_investment_blocked",
        "conceptual_preference_authority",
        "actions",
        "waves",
        "pareto_layers",
        "priority_updates",
        "created_at",
        "consumption_log",
        "schedule_digest",
    }
)
_ACTION_FIELDS = frozenset(
    {
        "action_id",
        "kind",
        "target_id",
        "state_version",
        "branch_ids",
        "depends_on",
        "rationale",
        "priority_class",
        "restrictions",
        "payload",
        "status",
        "consumed_at",
        "consumer_receipt_id",
    }
)
_WAVE_FIELDS = frozenset({"wave_id", "mode", "action_ids"})
_EXECUTION_AUTHORITY_BOUNDARY: dict[str, Any] = {
    "boundary_kind": "reservation_first_operational_side_effect_only",
    "schedule_is_frozen": True,
    "support_requirement_is_schedule_derived": True,
    "reservation_precedes_callbacks": True,
    "terminal_head_check_is_point_in_time": True,
    "cross_store_atomicity_claimed": False,
    "may_select_or_modify_theory": False,
    "may_promote_scientific_claims": False,
    "may_grant_proof_or_experiment_authority": False,
    "may_grant_physics_result_authority": False,
}

# This is deliberately total over the imported scheduler vocabulary.  A future
# action kind cannot silently inherit theory-only treatment.
_ACTION_KIND_POLICY = {
    kind: (
        "dedicated_proof_execution_only"
        if kind == "prove"
        else "closed_post_result_marker"
        if kind in _SUPPORT_MARKER_KINDS
        else "theory_only"
    )
    for kind in ACTION_KINDS
}
if set(_ACTION_KIND_POLICY) != set(ACTION_KINDS):  # pragma: no cover - import guard
    raise RuntimeError("action execution policy is not total over ACTION_KINDS")
ACTION_KIND_SUPPORT_POLICY: Mapping[str, str] = MappingProxyType(
    _ACTION_KIND_POLICY
)


class FrozenScheduleError(ContractError):
    """Raised when scheduler bytes, action identity, or wave closure drift."""


class ActionSupportPolicyError(ContractError):
    """Raised when frozen schedule semantics and N+7 support disagree."""


class ActionLedgerRolloverRequired(ContractError):
    """Raised before reservation when two terminal-safe slots do not remain."""


class WorkerOutcomeProtocolError(ContractError):
    """Raised internally when a callback returns an untyped outcome."""


class ActionLifecycleFinalizationError(RuntimeError):
    """Raised when callbacks ran but no terminal record could be persisted."""

    def __init__(
        self,
        reservation: CoordinationLedgerResult,
        requested_status: str,
        cause: BaseException,
    ) -> None:
        self.reservation = reservation
        self.requested_status = requested_status
        self.cause = cause
        super().__init__(
            "action callbacks finished but coordination finalization failed; "
            f"reservation={reservation.reservation_id}, "
            f"requested_status={requested_status}"
        )


class ActionCallbackExecutionError(RuntimeError):
    """Raised after an exception-bearing wave has a durable terminal record."""

    def __init__(
        self,
        result: ActionWaveExecutionResult,
        failed_action_ids: Sequence[str],
    ) -> None:
        self.result = result
        self.failed_action_ids = tuple(failed_action_ids)
        super().__init__(
            "one or more reserved action callbacks raised after invocation; "
            f"terminal_status={result.terminal.status}, "
            f"action_ids={list(self.failed_action_ids)}"
        )


@dataclasses.dataclass(frozen=True, slots=True)
class ActionWorkerOutcome:
    """One callback's explicit operational result.

    ``failed`` means the callback attests that it produced no externally
    visible effect requiring repair.  A callback that may have produced a
    partial effect must return ``compensation_required``.  An uncaught
    exception is treated conservatively as ``compensation_required`` by the
    boundary because its effect state is unknown.
    """

    status: str
    evidence_digests: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in _CALLBACK_STATUSES:
            raise WorkerOutcomeProtocolError(
                f"unknown action worker outcome: {self.status!r}"
            )
        if type(self.evidence_digests) is not tuple:
            raise WorkerOutcomeProtocolError(
                "worker evidence digests must be an immutable tuple"
            )
        if len(self.evidence_digests) > ledger_protocol.MAX_TERMINAL_EVIDENCE_DIGESTS:
            raise WorkerOutcomeProtocolError(
                "worker evidence exceeds the terminal evidence count ceiling"
            )
        for value in self.evidence_digests:
            validate_digest(value)
        if (
            tuple(sorted(self.evidence_digests)) != self.evidence_digests
            or len(set(self.evidence_digests)) != len(self.evidence_digests)
        ):
            raise WorkerOutcomeProtocolError(
                "worker evidence digests must be sorted and unique"
            )


@dataclasses.dataclass(frozen=True, slots=True)
class ActionInvocation:
    """Immutable callback input with fresh defensive JSON projections."""

    schedule_id: str
    schedule_digest: str
    wave_id: str
    wave_mode: str
    support_requirement: str
    _action_data: bytes
    _reservation_data: bytes
    _support_root_data: tuple[bytes, ...]

    @property
    def action(self) -> Mapping[str, Any]:
        return _decode_mapping(self._action_data, "frozen invocation action")

    @property
    def reservation(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._reservation_data, "frozen invocation reservation"
        )

    @property
    def support_root_references(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(
            _decode_mapping(data, "frozen invocation support root")
            for data in self._support_root_data
        )

    @property
    def authority_boundary(self) -> Mapping[str, Any]:
        return copy.deepcopy(_EXECUTION_AUTHORITY_BOUNDARY)


ActionWorker = Callable[[ActionInvocation], ActionWorkerOutcome]


@dataclasses.dataclass(frozen=True, slots=True)
class ActionWaveExecutionResult:
    """Defensive receipt for one reservation-first wave lifecycle."""

    reservation: CoordinationLedgerResult
    terminal: CoordinationLedgerResult
    schedule_id: str
    schedule_digest: str
    wave_id: str
    support_requirement: str
    replayed_terminal: bool
    _outcome_data: tuple[bytes, ...]

    @property
    def worker_outcomes(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(
            _decode_mapping(data, "worker outcome record")
            for data in self._outcome_data
        )

    @property
    def authority_boundary(self) -> Mapping[str, Any]:
        return copy.deepcopy(_EXECUTION_AUTHORITY_BOUNDARY)

    def as_dict(self) -> dict[str, Any]:
        return {
            "boundary_version": BOUNDARY_VERSION,
            "schedule_id": self.schedule_id,
            "schedule_digest": self.schedule_digest,
            "wave_id": self.wave_id,
            "support_requirement": self.support_requirement,
            "replayed_terminal": self.replayed_terminal,
            "reservation": self.reservation.as_dict(),
            "terminal": self.terminal.as_dict(),
            "worker_outcomes": list(self.worker_outcomes),
            "authority_boundary": self.authority_boundary,
        }


def _decode_mapping(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise FrozenScheduleError(f"{label} must be immutable bytes")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FrozenScheduleError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise FrozenScheduleError(f"{label} is not one canonical JSON object")
    return value


def _freeze_mapping(value: Mapping[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise FrozenScheduleError(f"{label} must be an object")
    try:
        data = canonical_json(value)
    except (TypeError, ValueError) as exc:
        raise FrozenScheduleError(f"{label} is not canonical JSON") from exc
    return _decode_mapping(data, label)


def _string_vector(
    value: Any,
    *,
    label: str,
    nonempty: bool,
    sorted_required: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise FrozenScheduleError(f"{label} must be a string array")
    if nonempty and not value:
        raise FrozenScheduleError(f"{label} must be non-empty")
    if len(set(value)) != len(value):
        raise FrozenScheduleError(f"{label} must be unique")
    if sorted_required and value != sorted(value):
        raise FrozenScheduleError(f"{label} must be sorted")
    return list(value)


def _validate_action(
    raw: Mapping[str, Any],
    *,
    target_id: str,
    state_version: int,
) -> dict[str, Any]:
    action = _freeze_mapping(raw, "scheduled action")
    if set(action) != _ACTION_FIELDS:
        raise FrozenScheduleError("scheduled action shape is not exact")
    action_id = validate_identifier(action["action_id"], "action_id")
    kind = action["kind"]
    if kind not in ACTION_KIND_SUPPORT_POLICY:
        raise FrozenScheduleError(f"unknown scheduled action kind: {kind!r}")
    if action["target_id"] != target_id or action["state_version"] != state_version:
        raise FrozenScheduleError(
            "scheduled action target/state identity differs from its schedule"
        )
    branch_ids = _string_vector(
        action["branch_ids"],
        label="scheduled action branch_ids",
        nonempty=False,
        sorted_required=True,
    )
    dependencies = _string_vector(
        action["depends_on"],
        label="scheduled action depends_on",
        nonempty=False,
        sorted_required=True,
    )
    if action_id in dependencies:
        raise FrozenScheduleError("scheduled action cannot depend on itself")
    rationale = _string_vector(
        action["rationale"],
        label="scheduled action rationale",
        nonempty=True,
    )
    restrictions = _string_vector(
        action["restrictions"],
        label="scheduled action restrictions",
        nonempty=False,
    )
    priority_class = validate_identifier(
        action["priority_class"], "action priority_class"
    )
    payload = action["payload"]
    if not isinstance(payload, Mapping):
        raise FrozenScheduleError("scheduled action payload must be an object")
    if (
        action["status"] != "pending"
        or action["consumed_at"] is not None
        or action["consumer_receipt_id"] is not None
    ):
        raise FrozenScheduleError(
            "execution boundary requires an unconsumed frozen schedule"
        )
    identity_material = {
        "kind": kind,
        "target_id": target_id,
        "state_version": state_version,
        "branch_ids": branch_ids,
        "depends_on": dependencies,
        "payload": copy.deepcopy(dict(payload)),
    }
    if action_id != stable_identifier("action", identity_material):
        raise FrozenScheduleError(
            "scheduled action ID differs from its complete identity material"
        )

    marked = POST_RESULT_SUPPORT_MARKER in restrictions
    has_vector = SUPPORT_ROOT_IDENTITY_FIELD in payload
    if marked != has_vector:
        raise ActionSupportPolicyError(
            "post-result action requires both the support marker and root identity vector"
        )
    if marked:
        if ACTION_KIND_SUPPORT_POLICY[kind] != "closed_post_result_marker":
            raise ActionSupportPolicyError(
                "only reflect/reframe may carry the post-result support marker"
            )
        root_ids = _string_vector(
            payload[SUPPORT_ROOT_IDENTITY_FIELD],
            label="N+7 support root object IDs",
            nonempty=True,
        )
        if len(root_ids) != 1:
            raise ActionSupportPolicyError(
                "post-result action requires exactly one active N+7 aggregation root"
            )
        validate_identifier(root_ids[0], "N+7 support root object_id")
    return action


def _validate_wave(
    raw: Mapping[str, Any],
    *,
    known_action_ids: set[str],
) -> dict[str, Any]:
    wave = _freeze_mapping(raw, "scheduled action wave")
    if set(wave) != _WAVE_FIELDS:
        raise FrozenScheduleError("scheduled wave shape is not exact")
    wave_id = validate_identifier(wave["wave_id"], "wave_id")
    mode = wave["mode"]
    if mode not in _WAVE_MODES:
        raise FrozenScheduleError(f"unknown scheduled wave mode: {mode!r}")
    action_ids = _string_vector(
        wave["action_ids"], label="scheduled wave action_ids", nonempty=True
    )
    if not set(action_ids).issubset(known_action_ids):
        raise FrozenScheduleError("scheduled wave references an unknown action")
    identity_material: str | list[str]
    if mode in {"parallel", "serial"}:
        identity_material = action_ids
    else:
        if len(action_ids) != 1:
            raise FrozenScheduleError(
                "gate/constraint waves require exactly one scheduled action"
            )
        identity_material = action_ids[0]
    if wave_id != stable_identifier("wave", identity_material):
        raise FrozenScheduleError(
            "scheduled wave ID differs from its exact action vector"
        )
    if mode == "parallel" and len(action_ids) < 2:
        raise FrozenScheduleError("parallel wave requires at least two actions")
    if mode == "serial" and len(action_ids) != 1:
        raise FrozenScheduleError("serial wave requires exactly one action")
    return wave


def _validate_dependency_order(
    actions_by_id: Mapping[str, Mapping[str, Any]],
    waves: Sequence[Mapping[str, Any]],
) -> None:
    wave_index: dict[str, int] = {}
    for index, wave in enumerate(waves):
        for action_id in wave["action_ids"]:
            if action_id in wave_index:
                raise FrozenScheduleError(
                    "scheduled action appears in more than one wave"
                )
            wave_index[action_id] = index
    if set(wave_index) != set(actions_by_id):
        raise FrozenScheduleError(
            "scheduled waves must partition the complete action vector"
        )
    for action_id, action in actions_by_id.items():
        for dependency in action["depends_on"]:
            if dependency not in actions_by_id:
                raise FrozenScheduleError(
                    "scheduled action depends on an unknown action"
                )
            if wave_index[dependency] >= wave_index[action_id]:
                raise FrozenScheduleError(
                    "scheduled dependency must occur in an earlier wave"
                )


def _validate_frozen_schedule_and_wave(
    schedule: Mapping[str, Any],
    wave_id: str,
    *,
    theory_commit_reference: Mapping[str, Any],
    theory_graph_reference: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], tuple[dict[str, Any], ...]]:
    record = _freeze_mapping(schedule, "discovery schedule")
    if set(record) != _SCHEDULE_FIELDS:
        raise FrozenScheduleError("discovery schedule shape is not exact")
    if record["scheduler_version"] != _SCHEDULE_VERSION:
        raise FrozenScheduleError("unsupported discovery scheduler version")
    target_id = validate_identifier(record["target_id"], "schedule target_id")
    state_version = record["state_version"]
    if (
        isinstance(state_version, bool)
        or not isinstance(state_version, int)
        or state_version < 0
    ):
        raise FrozenScheduleError(
            "schedule state_version must be a non-negative integer"
        )
    validate_digest(record["input_digest"])
    validate_digest(record["schedule_digest"])
    expected_schedule_id = stable_identifier(
        "schedule", target_id, state_version, record["input_digest"]
    )
    if record["schedule_id"] != expected_schedule_id:
        raise FrozenScheduleError(
            "schedule ID differs from target, state, and input digest"
        )
    if (
        record["schedule_digest"]
        != canonical_digest(
            record,
            exclude_keys=("schedule_digest", "created_at", "consumption_log"),
        )
        or not isinstance(record["created_at"], str)
        or not record["created_at"]
        or record["consumption_log"] != []
        or type(record["literature_investment_blocked"]) is not bool
        or not isinstance(record["conceptual_preference_authority"], Mapping)
        or not isinstance(record["pareto_layers"], list)
        or not isinstance(record["priority_updates"], list)
    ):
        raise FrozenScheduleError(
            "schedule is not an exact unconsumed frozen scheduler result"
        )
    raw_actions = record["actions"]
    raw_waves = record["waves"]
    if (
        not isinstance(raw_actions, list)
        or not raw_actions
        or not all(isinstance(row, Mapping) for row in raw_actions)
        or not isinstance(raw_waves, list)
        or not raw_waves
        or not all(isinstance(row, Mapping) for row in raw_waves)
    ):
        raise FrozenScheduleError(
            "schedule requires non-empty action and wave arrays"
        )
    actions = tuple(
        _validate_action(
            raw, target_id=target_id, state_version=state_version
        )
        for raw in raw_actions
    )
    action_ids = [row["action_id"] for row in actions]
    if len(set(action_ids)) != len(action_ids):
        raise FrozenScheduleError("scheduled action IDs must be unique")
    actions_by_id = {row["action_id"]: row for row in actions}
    waves = tuple(
        _validate_wave(raw, known_action_ids=set(actions_by_id))
        for raw in raw_waves
    )
    wave_ids = [row["wave_id"] for row in waves]
    if len(set(wave_ids)) != len(wave_ids):
        raise FrozenScheduleError("scheduled wave IDs must be unique")
    _validate_dependency_order(actions_by_id, waves)
    selected = [row for row in waves if row["wave_id"] == wave_id]
    if len(selected) != 1:
        raise FrozenScheduleError("selected wave ID is absent or non-unique")

    commit_ref = _freeze_mapping(
        theory_commit_reference, "theory commit reference"
    )
    graph_ref = _freeze_mapping(
        theory_graph_reference, "theory graph reference"
    )
    if (
        commit_ref.get("target_id") != target_id
        or graph_ref.get("generation") != commit_ref.get("generation")
        or graph_ref.get("commit_reference_digest")
        != commit_ref.get("reference_digest")
    ):
        raise FrozenScheduleError(
            "schedule and content-graph theory reference identities disagree"
        )
    selected_actions = tuple(
        copy.deepcopy(actions_by_id[action_id])
        for action_id in selected[0]["action_ids"]
    )
    return record, selected[0], selected_actions


def _derive_support_binding(
    actions: Sequence[Mapping[str, Any]],
    *,
    theory_graph_reference: Mapping[str, Any],
    aggregation_root_reference: Mapping[str, Any] | None,
) -> tuple[str, tuple[dict[str, Any], ...]]:
    expected_vectors: list[tuple[str, ...]] = []
    requirement_modes: set[str] = set()
    for action in actions:
        marked = POST_RESULT_SUPPORT_MARKER in action["restrictions"]
        if marked:
            requirement_modes.add("n_plus_7_support_dependent")
            expected_vectors.append(
                tuple(action["payload"][SUPPORT_ROOT_IDENTITY_FIELD])
            )
        else:
            requirement_modes.add("theory_only")
    if len(requirement_modes) != 1:
        raise ActionSupportPolicyError(
            "one action wave cannot mix theory-only and support-dependent actions"
        )
    requirement = next(iter(requirement_modes))
    if requirement == "theory_only":
        if aggregation_root_reference is not None:
            raise ActionSupportPolicyError(
                "theory-only action wave rejects an N+7 support root"
            )
        return requirement, ()

    if aggregation_root_reference is None:
        raise ActionSupportPolicyError(
            "post-result action wave requires its exact active N+7 aggregation root"
        )
    if len(set(expected_vectors)) != 1:
        raise ActionSupportPolicyError(
            "post-result action wave names inconsistent support-root identities"
        )
    root = _freeze_mapping(
        aggregation_root_reference, "N+7 aggregation root reference"
    )
    expected_root_id = expected_vectors[0][0]
    if (
        root.get("object_kind") != AGGREGATION_ROOT_KIND
        or root.get("object_id") != expected_root_id
    ):
        raise ActionSupportPolicyError(
            "supplied N+7 aggregation root differs from the frozen action identity"
        )
    graph_ref = _freeze_mapping(
        theory_graph_reference, "theory graph reference"
    )
    ordered_roots = graph_ref.get("ordered_root_object_ids")
    if (
        not isinstance(ordered_roots, list)
        or not ordered_roots
        or ordered_roots[-1] != expected_root_id
        or ordered_roots.count(expected_root_id) != 1
    ):
        raise ActionSupportPolicyError(
            "frozen support identity is not the active final root of the current graph"
        )
    return requirement, (root,)


@contextmanager
def _coordination_execution_lock(
    ledger: ActionCoordinationLedger,
) -> Iterator[None]:
    """Serialize complete compliant lifecycles without claiming store authority."""

    root = ledger.coordination_root
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".action-execution-boundary.lock"
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise ContractError("cannot open the action execution boundary lock") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ContractError(
                "action execution boundary lock must be one regular file"
            )
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _require_terminal_capacity(ledger: ActionCoordinationLedger) -> None:
    current = ledger.current_generation()
    ceiling = ledger_protocol.MAX_LEDGER_RECORDS
    if (
        isinstance(ceiling, bool)
        or not isinstance(ceiling, int)
        or ceiling < 2
        or current + 2 > ceiling
    ):
        raise ActionLedgerRolloverRequired(
            "coordination ledger lacks two slots for an atomic operational "
            "reservation/terminal lifecycle; automatic rollover is forbidden "
            "because a new root could reuse an already claimed side effect"
        )


def _existing_terminal(
    ledger: ActionCoordinationLedger,
    reservation_id: str,
) -> CoordinationLedgerResult | None:
    try:
        return ledger.read_terminal(reservation_id)
    except ContractError as exc:
        expected = (
            "coordination reservation has no terminal record: "
            f"{reservation_id}"
        )
        if str(exc) == expected:
            return None
        raise


def _invocation(
    *,
    schedule: Mapping[str, Any],
    wave: Mapping[str, Any],
    action: Mapping[str, Any],
    support_requirement: str,
    support_roots: Sequence[Mapping[str, Any]],
    reservation: CoordinationLedgerResult,
) -> ActionInvocation:
    return ActionInvocation(
        schedule_id=str(schedule["schedule_id"]),
        schedule_digest=str(schedule["schedule_digest"]),
        wave_id=str(wave["wave_id"]),
        wave_mode=str(wave["mode"]),
        support_requirement=support_requirement,
        _action_data=canonical_json(action),
        _reservation_data=canonical_json(reservation.record),
        _support_root_data=tuple(canonical_json(row) for row in support_roots),
    )


def _outcome_record(
    *,
    action_id: str,
    status: str,
    evidence_digests: Sequence[str],
    callback_state: str,
    exception: BaseException | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "action_id": action_id,
        "status": status,
        "evidence_digests": list(evidence_digests),
        "callback_state": callback_state,
        "exception_digest": None,
    }
    if exception is not None:
        record["exception_digest"] = canonical_digest(
            {
                "module": type(exception).__module__,
                "type": type(exception).__qualname__,
                "message": str(exception),
            }
        )
    record["outcome_digest"] = canonical_digest(record)
    return record


def _invoke_one(
    callback: ActionWorker,
    invocation: ActionInvocation,
) -> tuple[ActionWorkerOutcome | None, BaseException | None]:
    try:
        outcome = callback(invocation)
        if type(outcome) is not ActionWorkerOutcome:
            raise WorkerOutcomeProtocolError(
                "action callback must return an exact ActionWorkerOutcome"
            )
        return outcome, None
    except BaseException as exc:  # finalization must precede propagation
        return None, exc


def _run_callbacks(
    *,
    wave: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]],
    callbacks: Mapping[str, ActionWorker],
    invocations: Mapping[str, ActionInvocation],
) -> tuple[list[dict[str, Any]], list[tuple[str, BaseException]]]:
    records: list[dict[str, Any]] = []
    errors: list[tuple[str, BaseException]] = []
    if wave["mode"] == "parallel":
        worker_count = min(len(actions), MAX_PARALLEL_WORKERS)
        with ThreadPoolExecutor(
            max_workers=worker_count,
            thread_name_prefix="discovery-action-wave",
        ) as pool:
            futures: dict[str, Future[tuple[ActionWorkerOutcome | None, BaseException | None]]] = {
                action["action_id"]: pool.submit(
                    _invoke_one,
                    callbacks[action["action_id"]],
                    invocations[action["action_id"]],
                )
                for action in actions
            }
            for action in actions:
                action_id = action["action_id"]
                outcome, error = futures[action_id].result()
                if error is not None:
                    errors.append((action_id, error))
                    records.append(
                        _outcome_record(
                            action_id=action_id,
                            status="compensation_required",
                            evidence_digests=(),
                            callback_state="raised_effect_state_unknown",
                            exception=error,
                        )
                    )
                else:
                    assert outcome is not None
                    records.append(
                        _outcome_record(
                            action_id=action_id,
                            status=outcome.status,
                            evidence_digests=outcome.evidence_digests,
                            callback_state="returned_typed_outcome",
                        )
                    )
        return records, errors

    stopped = False
    for action in actions:
        action_id = action["action_id"]
        if stopped:
            records.append(
                _outcome_record(
                    action_id=action_id,
                    status="released",
                    evidence_digests=(),
                    callback_state="not_invoked_after_serial_exception",
                )
            )
            continue
        outcome, error = _invoke_one(callbacks[action_id], invocations[action_id])
        if error is not None:
            stopped = True
            errors.append((action_id, error))
            records.append(
                _outcome_record(
                    action_id=action_id,
                    status="compensation_required",
                    evidence_digests=(),
                    callback_state="raised_effect_state_unknown",
                    exception=error,
                )
            )
        else:
            assert outcome is not None
            records.append(
                _outcome_record(
                    action_id=action_id,
                    status=outcome.status,
                    evidence_digests=outcome.evidence_digests,
                    callback_state="returned_typed_outcome",
                )
            )
    return records, errors


def _derive_terminal_status(
    outcome_records: Sequence[Mapping[str, Any]],
) -> str:
    statuses = [str(row["status"]) for row in outcome_records]
    if not statuses:
        raise WorkerOutcomeProtocolError("action wave produced no outcome records")
    if "compensation_required" in statuses:
        return "compensation_required"
    if all(status == "completed" for status in statuses):
        return "completed"
    if all(status == "released" for status in statuses):
        return "released"
    if "completed" in statuses:
        return "compensation_required"
    return "failed"


def _result(
    *,
    reservation: CoordinationLedgerResult,
    terminal: CoordinationLedgerResult,
    schedule: Mapping[str, Any],
    wave: Mapping[str, Any],
    support_requirement: str,
    replayed_terminal: bool,
    outcomes: Sequence[Mapping[str, Any]],
) -> ActionWaveExecutionResult:
    return ActionWaveExecutionResult(
        reservation=reservation,
        terminal=terminal,
        schedule_id=str(schedule["schedule_id"]),
        schedule_digest=str(schedule["schedule_digest"]),
        wave_id=str(wave["wave_id"]),
        support_requirement=support_requirement,
        replayed_terminal=replayed_terminal,
        _outcome_data=tuple(canonical_json(row) for row in outcomes),
    )


def execute_frozen_action_wave(
    *,
    ledger: ActionCoordinationLedger,
    schedule: Mapping[str, Any],
    wave_id: str,
    theory_commit_reference: Mapping[str, Any],
    theory_graph_reference: Mapping[str, Any],
    consumer_id: str,
    callbacks: Mapping[str, ActionWorker],
    aggregation_root_reference: Mapping[str, Any] | None = None,
    lifecycle_request: str = "execute",
) -> ActionWaveExecutionResult:
    """Reserve, invoke, and terminalize one exact frozen scheduler wave.

    ``lifecycle_request="release"`` reserves and terminalizes the wave without
    invoking callbacks.  Release consumes the schedule/action claims forever in
    this ledger; an exact retry reopens the existing terminal and never invokes
    a callback.  A real retry requires a newly frozen scheduler state with new
    schedule/action identities.  Automatic ledger rollover is forbidden.

    Callback exceptions are conservatively terminalized as
    ``compensation_required`` and then raised as
    :class:`ActionCallbackExecutionError`.  A typed ``failed`` outcome is
    reserved for a worker that can attest no compensatable side effect.
    """

    if type(ledger) is not ActionCoordinationLedger:
        raise ContractError("ledger must be an exact ActionCoordinationLedger")
    wave_id = validate_identifier(wave_id, "wave_id")
    consumer_id = validate_identifier(consumer_id, "consumer_id")
    if lifecycle_request not in {"execute", "release"}:
        raise ContractError(
            "action-wave lifecycle_request must be 'execute' or 'release'"
        )

    frozen_schedule, wave, actions = _validate_frozen_schedule_and_wave(
        schedule,
        wave_id,
        theory_commit_reference=theory_commit_reference,
        theory_graph_reference=theory_graph_reference,
    )
    dedicated_action_ids = [
        str(action["action_id"])
        for action in actions
        if ACTION_KIND_SUPPORT_POLICY[action["kind"]]
        == "dedicated_proof_execution_only"
    ]
    if dedicated_action_ids:
        raise ActionSupportPolicyError(
            "scheduled prove actions require the dedicated attempt-specific "
            "proof execution boundary"
        )
    if not isinstance(callbacks, Mapping):
        raise ContractError("action callbacks must be a mapping")
    support_requirement, support_roots = _derive_support_binding(
        actions,
        theory_graph_reference=theory_graph_reference,
        aggregation_root_reference=aggregation_root_reference,
    )
    action_ids = tuple(str(action["action_id"]) for action in actions)
    if lifecycle_request == "execute":
        if set(callbacks) != set(action_ids):
            raise ContractError(
                "callback keys must exactly equal the selected wave action IDs"
            )
        if any(not callable(callbacks[action_id]) for action_id in action_ids):
            raise ContractError("every selected action callback must be callable")
    elif callbacks:
        raise ContractError("released action wave cannot carry callbacks")

    with _coordination_execution_lock(ledger):
        _require_terminal_capacity(ledger)
        reservation = ledger.reserve(
            theory_commit_reference=theory_commit_reference,
            theory_graph_reference=theory_graph_reference,
            n_plus_7_support_root_references=support_roots,
            schedule_id=frozen_schedule["schedule_id"],
            schedule_digest=frozen_schedule["schedule_digest"],
            action_ids=action_ids,
            consumer_id=consumer_id,
        )
        existing = _existing_terminal(ledger, reservation.reservation_id)
        if existing is not None:
            return _result(
                reservation=reservation,
                terminal=existing,
                schedule=frozen_schedule,
                wave=wave,
                support_requirement=support_requirement,
                replayed_terminal=True,
                outcomes=(),
            )

        if lifecycle_request == "release":
            outcome_records = [
                _outcome_record(
                    action_id=action_id,
                    status="released",
                    evidence_digests=(),
                    callback_state="not_invoked_explicit_release",
                )
                for action_id in action_ids
            ]
            callback_errors: list[tuple[str, BaseException]] = []
        else:
            try:
                invocations = {
                    action["action_id"]: _invocation(
                        schedule=frozen_schedule,
                        wave=wave,
                        action=action,
                        support_requirement=support_requirement,
                        support_roots=support_roots,
                        reservation=reservation,
                    )
                    for action in actions
                }
                outcome_records, callback_errors = _run_callbacks(
                    wave=wave,
                    actions=actions,
                    callbacks=callbacks,
                    invocations=invocations,
                )
            except BaseException as exc:
                # Pool construction/submission can fail after reservation and
                # after an unknown subset of callbacks has started.  Treat the
                # entire wave as compensatable rather than leaking an
                # unterminated reservation or assuming that no effect occurred.
                outcome_records = [
                    _outcome_record(
                        action_id=action_id,
                        status="compensation_required",
                        evidence_digests=(),
                        callback_state=(
                            "worker_dispatch_failed_effect_state_unknown"
                        ),
                        exception=exc,
                    )
                    for action_id in action_ids
                ]
                callback_errors = [
                    (action_id, exc) for action_id in action_ids
                ]

        requested_status = _derive_terminal_status(outcome_records)
        wave_evidence_digest = canonical_digest(
            {
                "boundary_version": BOUNDARY_VERSION,
                "schedule_id": frozen_schedule["schedule_id"],
                "schedule_digest": frozen_schedule["schedule_digest"],
                "wave_id": wave["wave_id"],
                "support_requirement": support_requirement,
                "reservation_id": reservation.reservation_id,
                "outcomes": outcome_records,
                "requested_terminal_status": requested_status,
                "authority_boundary": _EXECUTION_AUTHORITY_BOUNDARY,
            }
        )
        try:
            terminal = ledger.finalize(
                reservation.reservation_id,
                terminal_status=requested_status,
                terminal_evidence_digests=(wave_evidence_digest,),
            )
        except BaseException as exc:
            raise ActionLifecycleFinalizationError(
                reservation, requested_status, exc
            ) from exc

        result = _result(
            reservation=reservation,
            terminal=terminal,
            schedule=frozen_schedule,
            wave=wave,
            support_requirement=support_requirement,
            replayed_terminal=False,
            outcomes=outcome_records,
        )
        if callback_errors:
            first_error = callback_errors[0][1]
            if isinstance(first_error, (KeyboardInterrupt, SystemExit)):
                if hasattr(first_error, "add_note"):
                    first_error.add_note(
                        "action callback lifecycle was terminalized as "
                        f"{terminal.status}; reservation={reservation.reservation_id}"
                    )
                raise first_error
            raise ActionCallbackExecutionError(
                result,
                [action_id for action_id, _error in callback_errors],
            ) from first_error
        return result


__all__ = [
    "ACTION_KIND_SUPPORT_POLICY",
    "AGGREGATION_ROOT_KIND",
    "ActionCallbackExecutionError",
    "ActionInvocation",
    "ActionLedgerRolloverRequired",
    "ActionLifecycleFinalizationError",
    "ActionSupportPolicyError",
    "ActionWaveExecutionResult",
    "ActionWorker",
    "ActionWorkerOutcome",
    "BOUNDARY_VERSION",
    "FrozenScheduleError",
    "MAX_PARALLEL_WORKERS",
    "POST_RESULT_SUPPORT_MARKER",
    "SUPPORT_ROOT_IDENTITY_FIELD",
    "WorkerOutcomeProtocolError",
    "execute_frozen_action_wave",
]
