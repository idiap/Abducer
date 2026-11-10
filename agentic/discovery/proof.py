# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Proof contracts with v2 execution surfaces held inert as history only."""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import os
import stat
import threading
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from agentic.discovery.budgets import (
    ResourceBudget,
    complete_governed_process_environment,
    contained_path,
    minimal_replacement_environment,
    validate_job_id,
    validate_v2_process_event,
)
from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    file_digest,
    safe_relative_path,
    stable_identifier,
    utc_now,
    validate_instance,
    validate_payload,
)


SPEC_ROOT = Path(__file__).resolve().parents[1] / "spec"
HANDOFF_SCHEMA = SPEC_ROOT / "discovery_proof_handoff.schema.json"
PRELAUNCH_CAPABILITY_SCHEMA = (
    SPEC_ROOT / "discovery_proof_prelaunch_capability_v3.schema.json"
)
RECEIPT_SCHEMA = SPEC_ROOT / "discovery_proof_receipt.schema.json"
HISTORICAL_HANDOFF_SCHEMA = (
    SPEC_ROOT / "history" / "discovery_proof_handoff_v1.schema.json"
)
HISTORICAL_RECEIPT_SCHEMA = (
    SPEC_ROOT / "history" / "discovery_proof_receipt_v1.schema.json"
)
WORKER_SCHEMA = SPEC_ROOT / "discovery_proof_worker_protocol.schema.json"
HANDOFF_CONTRACT_VERSION = "discovery-proof-handoff/3.0.0"
RECEIPT_CONTRACT_VERSION = "discovery-proof-receipt/2.0.0"
RECEIPT_AUTHORITY_BOUNDARY = (
    "trusted_local_process_bytes_protocol_and_claim_bound_certificate_with_no_"
    "checker_soundness_theorem_truth_conceptual_merit_or_physics_authority"
)
_RESOURCE_LIMITED = {
    "deadline_exhausted",
    "cpu_exhausted",
    "out_of_memory",
    "disk_exhausted",
    "network_exhausted",
    "token_exhausted",
    "request_exhausted",
    "spend_exhausted",
    "input_exhausted",
    "output_exhausted",
}
_HANDOFF_NULLS = {
    "truth_authority": False,
    "checker_soundness_authority": False,
    "theorem_authority": False,
    "physics_authority": False,
    "theory_selection_authority": False,
    "same_cycle_theory_mutation": False,
    "serialized_execution_authority": False,
    "cryptographic_authenticity": False,
}
_DEFAULT_EXECUTION_POLICY = {
    "replacement_environment_policy": "minimal_exact_v1",
    "input_limit_bytes": 1_048_576,
    "stdout_limit_bytes": 1_048_576,
    "stderr_limit_bytes": 1_048_576,
    "filesystem_isolation": "unavailable",
    "network_isolation": "unavailable",
    "trusted_local_worker_required": True,
}
_FORMAL_PROOF_RUNTIME_CONTRACT = {
    "runtime_id": "canonical-formal-proof-runtime",
    "runtime_version": "3.0.0",
    "worker_protocol": "discovery-proof-worker-protocol/1.0.0",
    "execution_claim_protocol": "coordination-proof-execution-claim/1.0.0",
    "runtime_root_mode": "derived_from_one_shot_execution_claim",
    "generic_callback_allowed": False,
    "live_execution_claim_required": True,
    "same_cycle_theory_mutation": False,
}
_FORMAL_PROOF_RESOURCE_LIMITS = {
    "wall_time_seconds": 120.0,
    "grace_period_seconds": 0.25,
    "cpu_seconds": 120.0,
    "memory_bytes": 768 * 1024 * 1024,
    "disk_bytes": 64 * 1024 * 1024,
    "network_bytes": 0,
    "token_count": 0,
    "request_count": 0,
    "cost_usd": 0.0,
}
_PROOF_BLOCKING_RESTRICTIONS = frozenset(
    {"no_active_investment", "literature_blind"}
)
_PROOF_PRELAUNCH_CAPABILITY_FACTORY_SEAL = object()
_PROOF_PRELAUNCH_CAPABILITY_BOUNDARY = (
    "one_shot_live_unclaimed_postcommit_proof_prelaunch_capability_with_"
    "durable_claim_cas_only_at_consumption_and_inert_serialized_projection_"
    "no_rehydration_retry_truth_theory_selection_or_physics_authority"
)
_RETIRED_V2_EXECUTION_MESSAGE = (
    "proof execution v2 is history-only and cannot authorize launch; "
    "use proof_v3_facade.run_committed_proof_action_v3 with committed "
    "theory authority and its live proof-v3 prelaunch capability"
)


class ProofExecutionAuthorizationV2:
    """Historical type name that can no longer mint execution authority."""

    __slots__ = ()

    def __init__(
        self,
        payload: Mapping[str, Any],
        source_authorization: object,
        *,
        _factory_seal: object | None = None,
    ) -> None:
        del payload, source_authorization, _factory_seal
        raise TypeError(_RETIRED_V2_EXECUTION_MESSAGE)

    def __init_subclass__(cls, **_kwargs: Any) -> None:
        raise TypeError("ProofExecutionAuthorizationV2 is sealed")

    def __setattr__(self, _name: str, _value: object) -> None:
        raise TypeError("proof execution authorization is immutable")

    def _snapshot(self) -> dict[str, Any]:
        raise ContractError(_RETIRED_V2_EXECUTION_MESSAGE)


def issue_proof_execution_authorization(
    reserved_authorization: object,
) -> ProofExecutionAuthorizationV2:
    """Reject the retired v2 authority issuer without inspecting its input."""

    del reserved_authorization
    raise ContractError(_RETIRED_V2_EXECUTION_MESSAGE)


def _validate_proof_execution_authorization(
    value: object,
) -> tuple[dict[str, Any], dict[str, Any]]:
    del value
    raise ContractError(_RETIRED_V2_EXECUTION_MESSAGE)


def proof_execution_authorization_projection(
    value: ProofExecutionAuthorizationV2,
) -> dict[str, Any]:
    """Return evidence about a currently valid capability, never a replacement for it."""

    projection, _ = _validate_proof_execution_authorization(value)
    return copy.deepcopy(projection)


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    """Encode exact portable bytes for sealed live proof-v3 objects."""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


class ProofPrelaunchCapability:
    """Opaque preclaim authority whose durable CAS occurs only at consumption.

    Issuance observes and binds one exact unclaimed reservation but performs no
    execution claim.  Threads, aliases, independently issued capabilities, and
    forked process copies therefore all meet the same durable ledger CAS at the
    immediate prelaunch boundary.  Any consumption attempt permanently spends
    this local object, including attempts that fail before or after the CAS.
    """

    __slots__ = (
        "_factory_seal",
        "_projection_bytes",
        "_projection_bytes_digest",
        "_coordination_ledger",
        "_theory_authorization",
        "_handoff_bytes",
        "_reservation_id",
        "_execution_claim_id",
        "_consume_lock",
        "_state",
    )

    def __init__(
        self,
        projection: Mapping[str, Any],
        *,
        coordination_ledger: object,
        theory_authorization: object,
        handoff: Mapping[str, Any],
        reservation_id: str,
        execution_claim_id: str,
        _factory_seal: object | None = None,
    ) -> None:
        if _factory_seal is not _PROOF_PRELAUNCH_CAPABILITY_FACTORY_SEAL:
            raise TypeError(
                "ProofPrelaunchCapability is issued only by the canonical "
                "unclaimed-reservation factory"
            )
        projection_bytes = _canonical_json_bytes(dict(projection))
        handoff_bytes = _canonical_json_bytes(dict(handoff))
        object.__setattr__(self, "_factory_seal", _factory_seal)
        object.__setattr__(self, "_projection_bytes", projection_bytes)
        object.__setattr__(
            self,
            "_projection_bytes_digest",
            bytes_digest(projection_bytes),
        )
        object.__setattr__(self, "_coordination_ledger", coordination_ledger)
        object.__setattr__(self, "_theory_authorization", theory_authorization)
        object.__setattr__(self, "_handoff_bytes", handoff_bytes)
        object.__setattr__(self, "_reservation_id", reservation_id)
        object.__setattr__(self, "_execution_claim_id", execution_claim_id)
        object.__setattr__(self, "_consume_lock", threading.Lock())
        object.__setattr__(self, "_state", "fresh")

    def __init_subclass__(cls, **_kwargs: Any) -> None:
        raise TypeError("ProofPrelaunchCapability is sealed")

    def __setattr__(self, _name: str, _value: object) -> None:
        raise TypeError("proof prelaunch capability is immutable")

    def __copy__(self) -> None:
        raise TypeError("proof prelaunch capability cannot be copied")

    def __deepcopy__(self, _memo: object) -> None:
        raise TypeError("proof prelaunch capability cannot be deep-copied")

    def __reduce__(self) -> None:
        raise TypeError("proof prelaunch capability cannot be serialized")

    def __reduce_ex__(self, _protocol: int) -> None:
        raise TypeError("proof prelaunch capability cannot be serialized")

    def _snapshot(self) -> dict[str, Any]:
        return json.loads(self._projection_bytes)


def _proof_prelaunch_capability_material(
    *,
    handoff: Mapping[str, Any],
    reservation_result: object,
) -> dict[str, Any]:
    from agentic.discovery.action_coordination_ledger import (
        CoordinationLedgerResult,
    )

    if type(reservation_result) is not CoordinationLedgerResult:
        raise ContractError(
            "proof prelaunch capability requires one verified reservation result"
        )
    reservation = dict(reservation_result.record)
    reservation_reference = dict(reservation_result.ledger_commit_reference)
    source_binding = reservation.get("source_theory_binding")
    if (
        reservation.get("record_kind") != "proof_attempt_reservation"
        or reservation.get("handoff_id") != handoff.get("handoff_id")
        or reservation.get("handoff_digest") != handoff.get("content_digest")
        or reservation.get("action_id") != handoff.get("scheduled_action_id")
        or reservation.get("action_digest")
        != handoff.get("scheduled_action_digest")
        or reservation.get("formal_claim_authority_id")
        != handoff.get("formal_claim_authority_id")
        or reservation.get("formal_claim_authority_digest")
        != handoff.get("formal_claim_authority_digest")
        or reservation.get("producer_receipt_id")
        != handoff.get("producer_receipt_id")
        or reservation.get("producer_receipt_digest")
        != handoff.get("producer_receipt_digest")
        or not isinstance(source_binding, Mapping)
    ):
        raise ContractError(
            "proof prelaunch reservation does not bind its exact handoff and action"
        )
    core: dict[str, Any] = {
        "schema_version": 3,
        "capability_kind": "one_shot_unclaimed_postcommit_proof_prelaunch",
        "projection_phase": "before_durable_execution_claim",
        "target_id": handoff["target_id"],
        "run_id": handoff["run_id"],
        "cycle_id": handoff["cycle_id"],
        "branch_id": handoff["branch_id"],
        "source_commit_generation": handoff["source_commit_generation"],
        "source_commit_id": handoff["source_commit_id"],
        "source_manifest_digest": handoff["source_manifest_digest"],
        "source_state_file_digest": handoff["source_state_file_digest"],
        "source_state_semantic_digest": handoff["source_state_semantic_digest"],
        "theory_authorization_digest": handoff["theory_authorization_digest"],
        "theory_authorization_basis_digest": handoff[
            "theory_authorization_basis_digest"
        ],
        "literature_authority_basis_digest": handoff[
            "literature_authority_basis_digest"
        ],
        "schedule_id": handoff["schedule_id"],
        "schedule_digest": handoff["schedule_digest"],
        "action_id": handoff["scheduled_action_id"],
        "action_digest": handoff["scheduled_action_digest"],
        "handoff_id": handoff["handoff_id"],
        "handoff_digest": handoff["content_digest"],
        "formal_claim_authority_id": handoff["formal_claim_authority_id"],
        "formal_claim_authority_digest": handoff[
            "formal_claim_authority_digest"
        ],
        "producer_receipt_id": handoff["producer_receipt_id"],
        "producer_receipt_digest": handoff["producer_receipt_digest"],
        "hypothesis_id": handoff["hypothesis_id"],
        "conceptual_system_ids": copy.deepcopy(handoff["conceptual_system_ids"]),
        "conjecture_id": handoff["conjecture_id"],
        "obligation_id": handoff["obligation_id"],
        "proof_adapter": handoff["proof_adapter"],
        "execution_plan_digest": handoff["execution_plan_digest"],
        "attempt_number": reservation["attempt_number"],
        "attempt_id": reservation["attempt_id"],
        "reservation_id": reservation["reservation_id"],
        "reservation_digest": reservation["reservation_digest"],
        "execution_claim_id": reservation["execution_claim_id"],
        "reservation_commit_reference": reservation_reference,
        "reservation_commit_reference_digest": reservation_reference[
            "reference_digest"
        ],
        "source_theory_head_digest": source_binding["observed_head"][
            "head_digest"
        ],
        "proof_runtime_ref": reservation["proof_runtime_ref"],
        "resource_budget_digest": reservation["resource_budget_digest"],
        "literature_consume_before": reservation["literature_consume_before"],
        "durable_claim_present_in_projection": False,
        "projection_only": True,
        "authoritative_for_execution": False,
        "live_capability_required": True,
        "one_shot": True,
        "serialized_reconstruction_allowed": False,
        "authority_boundary": _PROOF_PRELAUNCH_CAPABILITY_BOUNDARY,
    }
    core["capability_id"] = stable_identifier(
        "proof-prelaunch-capability-v3",
        core["reservation_id"],
        core["reservation_digest"],
        core["execution_claim_id"],
        core["handoff_digest"],
        core["source_theory_head_digest"],
    )
    core["content_digest"] = _self_digest(core)
    validate_payload(core, PRELAUNCH_CAPABILITY_SCHEMA)
    return core


def _proof_claim_is_present(
    coordination_ledger: object,
    execution_claim_id: str,
) -> bool:
    _generation, state = coordination_ledger._load_state()
    claims = state.get("proof_execution_claims")
    if not isinstance(claims, Mapping):
        raise ContractError("proof coordination state lacks its claim table")
    return execution_claim_id in claims


def issue_proof_prelaunch_capability(
    *,
    coordination_ledger: object,
    theory_authorization: object,
    handoff: Mapping[str, Any],
    reservation_id: str,
) -> ProofPrelaunchCapability:
    """Bind one live unclaimed reservation without performing its durable CAS."""

    from agentic.discovery.action_coordination_ledger import (
        ActionCoordinationLedger,
        ProofExecutionClaimConsumed,
    )

    if type(coordination_ledger) is not ActionCoordinationLedger:
        raise ContractError(
            "proof prelaunch issuance requires an exact ActionCoordinationLedger"
        )
    current_handoff = reopen_current_proof_handoff(theory_authorization, handoff)
    reservation_result = coordination_ledger.read_proof_attempt(reservation_id)
    projection = _proof_prelaunch_capability_material(
        handoff=current_handoff,
        reservation_result=reservation_result,
    )
    if _proof_claim_is_present(
        coordination_ledger, projection["execution_claim_id"]
    ):
        raise ProofExecutionClaimConsumed(
            "proof execution claim is already consumed: "
            f"{projection['execution_claim_id']}"
        )
    return ProofPrelaunchCapability(
        projection,
        coordination_ledger=coordination_ledger,
        theory_authorization=theory_authorization,
        handoff=current_handoff,
        reservation_id=reservation_id,
        execution_claim_id=projection["execution_claim_id"],
        _factory_seal=_PROOF_PRELAUNCH_CAPABILITY_FACTORY_SEAL,
    )


def claim_proof_execution_capability(**_kwargs: object) -> None:
    """Reject the incorrect historical claim-before-mint capability order."""

    raise ContractError(
        "claim-before-capability issuance is retired; issue an unclaimed proof "
        "prelaunch capability and consume its durable CAS at the spawn boundary"
    )


def _reopen_proof_prelaunch_capability(
    value: object,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    from agentic.discovery.action_coordination_ledger import (
        ActionCoordinationLedger,
    )

    if (
        type(value) is not ProofPrelaunchCapability
        or value._factory_seal is not _PROOF_PRELAUNCH_CAPABILITY_FACTORY_SEAL
        or bytes_digest(value._projection_bytes)
        != value._projection_bytes_digest
        or type(value._coordination_ledger) is not ActionCoordinationLedger
    ):
        raise ContractError(
            "proof execution requires one live sealed prelaunch capability"
        )
    try:
        stored_handoff = json.loads(value._handoff_bytes)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError("proof prelaunch capability handoff bytes are invalid") from exc
    current_handoff = reopen_current_proof_handoff(
        value._theory_authorization,
        stored_handoff,
    )
    reservation_result = value._coordination_ledger.read_proof_attempt(
        value._reservation_id
    )
    reservation = dict(reservation_result.record)
    observed_head = value._coordination_ledger._current_theory_head()
    if observed_head != reservation["source_theory_binding"]["observed_head"]:
        raise ContractError("theory head changed before proof execution claim")
    expected = _proof_prelaunch_capability_material(
        handoff=current_handoff,
        reservation_result=reservation_result,
    )
    supplied = value._snapshot()
    if (
        supplied != expected
        or supplied.get("content_digest") != _self_digest(supplied)
        or supplied.get("projection_only") is not True
        or supplied.get("authoritative_for_execution") is not False
        or supplied.get("durable_claim_present_in_projection") is not False
        or supplied.get("serialized_reconstruction_allowed") is not False
    ):
        raise ContractError(
            "proof prelaunch capability differs from exact live reconstruction"
        )
    return supplied, current_handoff, reservation


def proof_prelaunch_capability_projection(
    value: ProofPrelaunchCapability,
) -> dict[str, Any]:
    """Return inert preclaim evidence without consuming launch authority."""

    projection, _handoff, _reservation = _reopen_proof_prelaunch_capability(value)
    return copy.deepcopy(projection)


def _consume_proof_prelaunch_capability(
    value: ProofPrelaunchCapability,
    *,
    failpoint: str | None = None,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Spend locally and perform the sole durable CAS immediately prelaunch."""

    from agentic.discovery.action_coordination_ledger import (
        CoordinationLedgerResult,
    )

    if type(value) is not ProofPrelaunchCapability:
        raise ContractError("proof execution requires an exact prelaunch capability")
    with value._consume_lock:
        if value._state != "fresh":
            raise ContractError("proof prelaunch capability is already spent")
        object.__setattr__(value, "_state", "claiming")
        try:
            projection, handoff, reservation = (
                _reopen_proof_prelaunch_capability(value)
            )
            claim_result = value._coordination_ledger.claim_proof_execution(
                theory_authorization=value._theory_authorization,
                handoff=handoff,
                reservation_id=value._reservation_id,
                failpoint=failpoint,
            )
            if type(claim_result) is not CoordinationLedgerResult:
                raise ContractError(
                    "proof execution claim did not return verified durable evidence"
                )
            claim = dict(claim_result.record)
            claim_reference = dict(claim_result.ledger_commit_reference)
            if (
                claim.get("record_kind") != "proof_execution_claim"
                or claim.get("execution_claim_id")
                != projection["execution_claim_id"]
                or claim.get("reservation_id") != reservation["reservation_id"]
                or claim.get("reservation_digest")
                != reservation["reservation_digest"]
                or claim.get("action_id") != projection["action_id"]
                or claim.get("action_digest") != projection["action_digest"]
                or claim.get("attempt_id") != projection["attempt_id"]
                or claim.get("handoff_id") != projection["handoff_id"]
                or claim.get("handoff_digest") != projection["handoff_digest"]
            ):
                raise ContractError(
                    "durable proof claim differs from its prelaunch capability"
                )
            return projection, handoff, reservation, claim, claim_reference
        finally:
            object.__setattr__(value, "_state", "spent")


def _self_digest(value: Mapping[str, Any], field: str = "content_digest") -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def statement_digest(statement: str) -> str:
    """Return a display-text digest; it carries no proof semantic authority."""

    if not isinstance(statement, str) or not statement.strip():
        raise ContractError("proof display statement must be non-empty")
    return canonical_digest({"display_statement": " ".join(statement.split())})


def _formal_claim(request: Mapping[str, Any]) -> dict[str, Any]:
    supplied = request.get("formal_claim")
    if isinstance(supplied, Mapping):
        return copy.deepcopy(dict(supplied))
    adapter = str(request.get("proof_adapter") or "")
    payload = request.get("proof_payload")
    if not isinstance(payload, Mapping):
        raise ContractError("current proof handoff requires a formal_claim")
    if "failed_premise" in payload:
        raise ContractError("caller-authored failed-premise verification is forbidden")
    if adapter == "exact":
        operation = payload.get("operation", "equality")
        if operation == "equality" and set(payload) <= {"operation", "left", "right"}:
            return {
                "claim_kind": "exact_equality",
                "operation": "equality",
                "left": payload.get("left"),
                "right": payload.get("right"),
            }
        if operation == "integer_predicate" and set(payload) <= {
            "operation",
            "variables",
            "predicate",
        }:
            return {
                "claim_kind": "exact_integer_predicate",
                "operation": "integer_predicate",
                "variables": copy.deepcopy(payload.get("variables")),
                "predicate": payload.get("predicate"),
            }
    if adapter == "finite_model" and set(payload) <= {
        "variables",
        "predicate",
        "quantifier",
        "max_states",
    }:
        return {"claim_kind": "finite_model", **copy.deepcopy(dict(payload))}
    if adapter == "lean" and "source" not in payload:
        return {
            "claim_kind": "lean_proposition",
            "imports": list(payload.get("imports", [])),
            "proposition": payload.get("proposition"),
            "proof_term": payload.get("proof_term"),
            "axiom_policy": payload.get("axiom_policy", "no_nonstandard_axioms"),
        }
    raise ContractError(
        "proof payload cannot be promoted to a current formal claim; provide a closed formal_claim"
    )


def _execution_plan(request: Mapping[str, Any], claim: Mapping[str, Any]) -> dict[str, Any]:
    supplied = request.get("execution_plan")
    if isinstance(supplied, Mapping):
        return copy.deepcopy(dict(supplied))
    adapter = str(request.get("proof_adapter") or "")
    payload = request.get("proof_payload")
    payload = payload if isinstance(payload, Mapping) else {}
    if adapter in {"exact", "finite_model"}:
        return {"kind": "builtin_worker"}
    if adapter == "lean":
        executable = payload.get("executable", "lean")
        if claim.get("proof_term"):
            return {"kind": "lean", "executable": str(executable)}
        return {"kind": "not_ready", "reason": "Lean proof body is not available"}
    if adapter == "command":
        command = payload.get("command")
        if not isinstance(command, list) or not command:
            return {
                "kind": "not_ready",
                "reason": "external checker command and claim-bound protocol are not available",
            }
        if "expected_artifact_digest" in payload or "failed_premise" in payload:
            raise ContractError(
                "legacy expected-artifact or caller-verified-premise command plans are forbidden"
            )
        return {
            "kind": "external_checker",
            "command": list(command),
            "checker_identity": str(payload.get("checker_identity") or ""),
            "checker_version": str(payload.get("checker_version") or ""),
            "protocol_version": "claim-bound-checker-result/1.0.0",
            "artifact_policy": str(payload.get("artifact_policy", "none")),
            "controlled_output_path": payload.get("controlled_output_path"),
        }
    raise ContractError(f"unknown proof adapter {adapter!r}")


def _origin_receipts(request: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = request.get("origin_receipts")
    if not isinstance(rows, list) or not rows:
        raise ContractError(
            "current proof handoff requires exact origin receipt descriptors, not IDs alone"
        )
    normalized = [copy.deepcopy(dict(row)) for row in rows if isinstance(row, Mapping)]
    if len(normalized) != len(rows):
        raise ContractError("proof origin receipt descriptor is not an object")
    normalized.sort(
        key=lambda row: (
            str(row.get("receipt_id")),
            str(row.get("semantic_role")),
            str(row.get("output_path")),
        )
    )
    ids = [str(row.get("receipt_id")) for row in normalized]
    if len(set(ids)) != len(ids):
        raise ContractError("proof origin receipt IDs must be unique")
    return normalized


def _current_handoff_core(request: Mapping[str, Any]) -> dict[str, Any]:
    claim = _formal_claim(request)
    formal_claim_digest = canonical_digest(claim)
    conjecture_id = str(request.get("conjecture_id") or "")
    if not conjecture_id:
        raise ContractError("proof handoff requires conjecture_id")
    obligation_id = str(
        request.get("obligation_id")
        or stable_identifier("proof-obligation-v2", conjecture_id, formal_claim_digest)
    )
    display_statement = str(
        request.get("display_statement", request.get("statement", ""))
    )
    statement_digest(display_statement)
    literature = request.get("literature_authority")
    ancestry = request.get("theory_ancestry")
    if not isinstance(literature, Mapping) or not isinstance(ancestry, Mapping):
        raise ContractError(
            "current proof handoff requires exact literature and theory ancestry records"
        )
    origin_prior = int(
        request.get("origin_prior_state_version", request.get("state_version", -1))
    )
    theory_generation = int(request.get("theory_generation", origin_prior + 1))
    core = {
        "schema_version": 2,
        "contract_version": HANDOFF_CONTRACT_VERSION,
        "target_id": str(request.get("target_id") or ""),
        "run_id": validate_job_id(str(request.get("run_id"))),
        "cycle_id": str(request.get("cycle_id") or ""),
        "branch_id": validate_job_id(str(request.get("branch_id"))),
        "origin_prior_state_version": origin_prior,
        "theory_generation": theory_generation,
        "concept_id": str(request.get("concept_id") or ""),
        "conceptual_system_ids": sorted(
            set(str(value) for value in request.get("conceptual_system_ids", []))
        ),
        "hypothesis_id": str(request.get("hypothesis_id") or ""),
        "conjecture_id": conjecture_id,
        "obligation_id": obligation_id,
        "supersedes_obligation_id": (
            str(request["supersedes_obligation_id"])
            if request.get("supersedes_obligation_id") is not None
            else None
        ),
        "display_statement": display_statement,
        "statement_authority": (
            "display_only_formal_claim_is_the_sole_proof_semantic_authority"
        ),
        "formal_claim": claim,
        "formal_claim_digest": formal_claim_digest,
        "literature_authority": copy.deepcopy(dict(literature)),
        "theory_ancestry": copy.deepcopy(dict(ancestry)),
        "proof_adapter": str(request.get("proof_adapter") or ""),
        "execution_plan": _execution_plan(request, claim),
        "origin_receipts": _origin_receipts(request),
        "return_to_theory_programme_id": str(
            request.get("return_to_theory_programme_id") or ""
        ),
        "resource_budget": asdict(
            ResourceBudget.from_mapping(
                copy.deepcopy(dict(request.get("resource_budget", {})))
            )
        ),
        "execution_policy": copy.deepcopy(
            dict(request.get("execution_policy", _DEFAULT_EXECUTION_POLICY))
        ),
        "authority_nulls": copy.deepcopy(_HANDOFF_NULLS),
        "created_at": str(request.get("created_at") or utc_now()),
    }
    return core


def _formal_action_binding(
    theory_authorization: Mapping[str, Any],
    formal_authority: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    join_raw = theory_authorization.get("formal_claim_schedule_join")
    if not isinstance(join_raw, Mapping):
        raise ContractError("theory authorization lacks its formal-claim schedule join")
    join = copy.deepcopy(dict(join_raw))
    if (
        join.get("status") != "ready_prove_pending"
        or join.get("join_digest") != canonical_digest(
            join, exclude_keys=("join_digest",)
        )
    ):
        raise ContractError("formal proof handoff requires one ready gate-replayed join")
    schedule_raw = theory_authorization.get("schedule")
    if not isinstance(schedule_raw, Mapping):
        raise ContractError("theory authorization lacks its committed schedule")
    schedule = copy.deepcopy(dict(schedule_raw))
    actions = [
        copy.deepcopy(dict(action))
        for action in schedule.get("actions", [])
        if isinstance(action, Mapping) and action.get("action_id") == join["action_id"]
    ]
    if len(actions) != 1:
        raise ContractError("formal proof handoff requires one exact scheduled action")
    action = actions[0]
    binding_raw = action.get("payload", {}).get("formal_claim_binding")
    if not isinstance(binding_raw, Mapping):
        raise ContractError("scheduled prove action lacks its formal-claim binding")
    binding = copy.deepcopy(dict(binding_raw))
    validate_instance(
        binding, "discovery_formal_claim_schedule_binding_v1.schema.json"
    )
    expected_binding = {
        "schema_version": 1,
        "binding_kind": "registered_formal_claim_prove_action",
        "producer_operator_id": formal_authority["producer_operator_id"],
        "producer_request_id": formal_authority["producer_request_id"],
        "producer_request_digest": formal_authority["producer_request_digest"],
        "producer_receipt_id": formal_authority["producer_receipt_id"],
        "producer_receipt_digest": formal_authority["producer_receipt_digest"],
        "producer_input_digest": formal_authority[
            "producer_input_content_digest"
        ],
        "consumer_event_id": formal_authority["semantic_consumer_event_id"],
        "consumer_event_hash": formal_authority["semantic_consumer_event_hash"],
        "semantic_row_id": formal_authority["semantic_row_id"],
        "semantic_row_digest": formal_authority["semantic_row_digest"],
        "output_id": formal_authority["producer_output_id"],
        "output_digest": formal_authority["output_content_digest"],
        "source_theory_generation": formal_authority[
            "source_theory_generation"
        ],
        "conjecture_id": formal_authority["conjecture_id"],
        "formal_claim_digest": formal_authority["formal_claim_digest"],
        "execution_plan_digest": formal_authority["execution_plan_digest"],
    }
    if binding != expected_binding:
        raise ContractError(
            "scheduled prove binding differs from committed formal-claim authority"
        )
    if (
        action.get("kind") != "prove"
        or action.get("status") != "pending"
        or action.get("consumed_at") is not None
        or action.get("consumer_receipt_id") is not None
        or action.get("branch_ids") != [formal_authority["branch_id"]]
        or action.get("target_id") != formal_authority["target_id"]
        or action.get("state_version")
        != formal_authority["source_prior_state_version"]
        or action.get("priority_class")
        != "registered_formal_claim_continuation"
        or set(action.get("restrictions", [])).intersection(
            _PROOF_BLOCKING_RESTRICTIONS
        )
        or join.get("output_id") != formal_authority["producer_output_id"]
        or join.get("producer_receipt_id")
        != formal_authority["producer_receipt_id"]
        or join.get("action_id") != action["action_id"]
        or join.get("binding_digest") != canonical_digest(binding)
    ):
        raise ContractError(
            "scheduled prove action differs from its gate-replayed formal authority"
        )
    return action, binding, join


def _postcommit_proof_handoff_material(
    theory_authorization: object,
) -> dict[str, Any]:
    from agentic.discovery.formal_claim_authority import (
        build_formal_claim_authority_v2,
    )
    from agentic.discovery.theory_gate import validate_authorization_at_use

    authorization = validate_authorization_at_use(
        theory_authorization,
        allowed_statuses=("verified_active_current",),
    )
    formal_authority = build_formal_claim_authority_v2(theory_authorization)
    action, binding, join = _formal_action_binding(
        authorization, formal_authority
    )
    if (
        authorization.get("commit_id") != formal_authority["source_commit_id"]
        or authorization.get("manifest_digest")
        != formal_authority["source_manifest_digest"]
        or authorization.get("committed_state_version")
        != formal_authority["source_commit_generation"]
        or authorization.get("transaction_head_generation")
        != formal_authority["source_commit_generation"]
        or authorization.get("authorization_digest")
        != formal_authority["theory_authorization_digest"]
        or authorization.get("authorization_basis_digest")
        != formal_authority["theory_authorization_basis_digest"]
        or authorization.get("literature_authority_basis_digest")
        != formal_authority["literature_authority_basis_digest"]
    ):
        raise ContractError("formal proof handoff crossed its current theory commit")
    consume_before = formal_authority["literature_consume_before"]
    authorized_at = authorization.get("literature_present_use_evaluated_at")
    if not isinstance(authorized_at, str) or not authorized_at:
        raise ContractError("formal proof handoff lacks its immutable gate decision time")
    action_digest = canonical_digest(action)
    obligation_id = stable_identifier(
        "proof-obligation-v3",
        formal_authority["authority_id"],
        formal_authority["content_digest"],
        action["action_id"],
        action_digest,
        formal_authority["formal_claim_digest"],
    )
    budget = asdict(
        ResourceBudget.from_mapping(
            {
                "budget_id": stable_identifier(
                    "formal-proof-resource-budget-v3",
                    formal_authority["authority_id"],
                    action["action_id"],
                    consume_before,
                ),
                **_FORMAL_PROOF_RESOURCE_LIMITS,
                "absolute_deadline": consume_before,
            }
        )
    )
    origin_receipts = [
        {
            "receipt_id": formal_authority["producer_receipt_id"],
            "receipt_digest": formal_authority["producer_receipt_digest"],
            "semantic_role": "formal_claim_output",
            "output_path": formal_authority["output_path"],
            "output_digest": formal_authority["output_file_digest"],
        }
    ]
    core: dict[str, Any] = {
        "schema_version": 3,
        "contract_version": HANDOFF_CONTRACT_VERSION,
        "formal_claim_authority_id": formal_authority["authority_id"],
        "formal_claim_authority_digest": formal_authority["content_digest"],
        "theory_authorization_digest": authorization["authorization_digest"],
        "theory_authorization_basis_digest": authorization[
            "authorization_basis_digest"
        ],
        "literature_authority_basis_digest": authorization[
            "literature_authority_basis_digest"
        ],
        "source_commit_generation": formal_authority[
            "source_commit_generation"
        ],
        "source_commit_id": formal_authority["source_commit_id"],
        "source_manifest_digest": formal_authority["source_manifest_digest"],
        "source_state_file_digest": formal_authority[
            "source_state_file_digest"
        ],
        "source_state_semantic_digest": formal_authority[
            "source_state_semantic_digest"
        ],
        "schedule_id": authorization["schedule_id"],
        "schedule_digest": authorization["schedule_digest"],
        "scheduled_action_id": action["action_id"],
        "scheduled_action_digest": action_digest,
        "scheduled_action": action,
        "formal_claim_schedule_binding": binding,
        "formal_claim_schedule_binding_digest": canonical_digest(binding),
        "formal_claim_schedule_join": join,
        "formal_claim_schedule_join_digest": join["join_digest"],
        "producer_operator_id": formal_authority["producer_operator_id"],
        "producer_request_id": formal_authority["producer_request_id"],
        "producer_request_digest": formal_authority["producer_request_digest"],
        "producer_receipt_id": formal_authority["producer_receipt_id"],
        "producer_receipt_digest": formal_authority["producer_receipt_digest"],
        "producer_output_id": formal_authority["producer_output_id"],
        "producer_output_digest": formal_authority["output_content_digest"],
        "producer_output_path": formal_authority["output_path"],
        "producer_output_file_digest": formal_authority["output_file_digest"],
        "semantic_consumer_event_id": formal_authority[
            "semantic_consumer_event_id"
        ],
        "semantic_consumer_event_hash": formal_authority[
            "semantic_consumer_event_hash"
        ],
        "target_id": formal_authority["target_id"],
        "run_id": formal_authority["run_id"],
        "cycle_id": formal_authority["source_cycle_id"],
        "branch_id": formal_authority["branch_id"],
        "origin_prior_state_version": formal_authority[
            "source_prior_state_version"
        ],
        "theory_generation": formal_authority["source_theory_generation"],
        "concept_id": formal_authority["concept_id"],
        "conceptual_system_ids": copy.deepcopy(
            formal_authority["conceptual_system_ids"]
        ),
        "hypothesis_id": formal_authority["hypothesis_id"],
        "conjecture_id": formal_authority["conjecture_id"],
        "obligation_id": obligation_id,
        "supersedes_obligation_id": None,
        "display_statement": formal_authority["display_statement"],
        "statement_authority": (
            "display_only_formal_claim_is_the_sole_proof_semantic_authority"
        ),
        "formal_claim": copy.deepcopy(formal_authority["formal_claim"]),
        "formal_claim_digest": formal_authority["formal_claim_digest"],
        "literature_authority": copy.deepcopy(
            formal_authority["literature_authority"]
        ),
        "literature_consume_before": consume_before,
        "theory_ancestry": copy.deepcopy(formal_authority["theory_ancestry"]),
        "proof_adapter": formal_authority["proof_adapter"],
        "execution_plan": copy.deepcopy(formal_authority["execution_plan"]),
        "execution_plan_digest": formal_authority["execution_plan_digest"],
        "origin_receipts": origin_receipts,
        "return_to_theory_programme_id": formal_authority[
            "source_theory_programme_id"
        ],
        "resource_budget": budget,
        "execution_policy": copy.deepcopy(_DEFAULT_EXECUTION_POLICY),
        "runtime_contract": copy.deepcopy(_FORMAL_PROOF_RUNTIME_CONTRACT),
        "projection_only": True,
        "postcommit_reopen_required": True,
        "authority_nulls": copy.deepcopy(_HANDOFF_NULLS),
        "authorized_at": authorized_at,
    }
    core["handoff_id"] = stable_identifier(
        "proof-handoff-v3",
        obligation_id,
        formal_authority["authority_id"],
        formal_authority["content_digest"],
        authorization["schedule_id"],
        authorization["schedule_digest"],
        action["action_id"],
        action_digest,
        canonical_digest(_FORMAL_PROOF_RUNTIME_CONTRACT),
        canonical_digest(budget),
        canonical_digest(_DEFAULT_EXECUTION_POLICY),
        consume_before,
        authorized_at,
    )
    core["content_digest"] = _self_digest(core)
    return core


def build_postcommit_proof_handoff(theory_authorization: object) -> dict[str, Any]:
    """Build the sole current inert handoff from one live committed gate."""

    handoff = _postcommit_proof_handoff_material(theory_authorization)
    validate_proof_handoff(handoff)
    return handoff


def reopen_current_proof_handoff(
    theory_authorization: object,
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    """Rebuild a current handoff and reject any detached or stale projection."""

    payload = validate_proof_handoff(handoff)
    rebuilt = build_postcommit_proof_handoff(theory_authorization)
    if rebuilt != payload:
        raise ContractError("proof handoff differs from current committed reconstruction")
    return rebuilt


def build_proof_handoff(source: object) -> dict[str, Any]:
    """Compatibility name for the post-commit factory; mappings are forbidden."""

    from agentic.discovery.theory_gate import VerifiedTheoryAuthorization

    if not isinstance(source, VerifiedTheoryAuthorization):
        raise ContractError(
            "raw caller-built proof handoffs are forbidden; provide a live theory capability"
        )
    return build_postcommit_proof_handoff(source)


def validate_proof_handoff(handoff: Mapping[str, Any]) -> dict[str, Any]:
    """Validate an inert v3 projection; this never establishes currentness."""

    if handoff.get("schema_version") in {1, 2}:
        raise ContractError("proof handoff v1/v2 is historical_decode_only")
    payload = copy.deepcopy(dict(handoff))
    validate_payload(payload, HANDOFF_SCHEMA)
    if payload["formal_claim_digest"] != canonical_digest(payload["formal_claim"]):
        raise ContractError("proof formal claim digest mismatch")
    if payload["content_digest"] != _self_digest(payload):
        raise ContractError("proof handoff content digest mismatch")
    if (
        payload["theory_generation"]
        != payload["origin_prior_state_version"] + 1
        or payload["source_commit_generation"] != payload["theory_generation"]
    ):
        raise ContractError("proof handoff theory generation is not the direct successor")
    if payload["authority_nulls"] != _HANDOFF_NULLS:
        raise ContractError("proof handoff authority nulls differ")
    if (
        payload["scheduled_action_id"] != payload["scheduled_action"]["action_id"]
        or payload["scheduled_action_digest"]
        != canonical_digest(payload["scheduled_action"])
        or payload["formal_claim_schedule_binding"]
        != payload["scheduled_action"]["payload"].get("formal_claim_binding")
        or payload["formal_claim_schedule_binding_digest"]
        != canonical_digest(payload["formal_claim_schedule_binding"])
        or payload["formal_claim_schedule_join_digest"]
        != payload["formal_claim_schedule_join"]["join_digest"]
        or payload["formal_claim_schedule_join"]["join_digest"]
        != canonical_digest(
            payload["formal_claim_schedule_join"], exclude_keys=("join_digest",)
        )
        or payload["formal_claim_schedule_join"]["action_id"]
        != payload["scheduled_action_id"]
        or payload["formal_claim_schedule_join"]["binding_digest"]
        != payload["formal_claim_schedule_binding_digest"]
        or payload["formal_claim_schedule_join"]["output_id"]
        != payload["producer_output_id"]
        or payload["formal_claim_schedule_join"]["producer_receipt_id"]
        != payload["producer_receipt_id"]
    ):
        raise ContractError("proof handoff schedule/action join mismatch")
    action = payload["scheduled_action"]
    action_identity_material = {
        "kind": action["kind"],
        "target_id": action["target_id"],
        "state_version": action["state_version"],
        "branch_ids": action["branch_ids"],
        "depends_on": action["depends_on"],
        "payload": action["payload"],
    }
    if (
        action["action_id"]
        != stable_identifier("action", action_identity_material)
        or action["target_id"] != payload["target_id"]
        or action["state_version"] != payload["origin_prior_state_version"]
        or action["branch_ids"] != [payload["branch_id"]]
        or action["kind"] != "prove"
        or action["status"] != "pending"
        or action["consumed_at"] is not None
        or action["consumer_receipt_id"] is not None
        or set(action["restrictions"]).intersection(
            _PROOF_BLOCKING_RESTRICTIONS
        )
    ):
        raise ContractError("proof handoff scheduled action identity is invalid")
    binding = payload["formal_claim_schedule_binding"]
    if (
        binding["producer_operator_id"] != payload["producer_operator_id"]
        or binding["producer_request_id"] != payload["producer_request_id"]
        or binding["producer_request_digest"] != payload["producer_request_digest"]
        or binding["producer_receipt_id"] != payload["producer_receipt_id"]
        or binding["producer_receipt_digest"] != payload["producer_receipt_digest"]
        or binding["consumer_event_id"]
        != payload["semantic_consumer_event_id"]
        or binding["consumer_event_hash"]
        != payload["semantic_consumer_event_hash"]
        or binding["output_id"] != payload["producer_output_id"]
        or binding["output_digest"] != payload["producer_output_digest"]
        or binding["source_theory_generation"] != payload["theory_generation"]
        or binding["conjecture_id"] != payload["conjecture_id"]
        or binding["formal_claim_digest"] != payload["formal_claim_digest"]
        or binding["execution_plan_digest"] != payload["execution_plan_digest"]
    ):
        raise ContractError("proof handoff producer/action binding mismatch")
    expected_budget = asdict(
        ResourceBudget.from_mapping(
            {
                "budget_id": stable_identifier(
                    "formal-proof-resource-budget-v3",
                    payload["formal_claim_authority_id"],
                    payload["scheduled_action_id"],
                    payload["literature_consume_before"],
                ),
                **_FORMAL_PROOF_RESOURCE_LIMITS,
                "absolute_deadline": payload["literature_consume_before"],
            }
        )
    )
    try:
        authorized_at = dt.datetime.fromisoformat(
            payload["authorized_at"].replace("Z", "+00:00")
        )
        consume_before = dt.datetime.fromisoformat(
            payload["literature_consume_before"].replace("Z", "+00:00")
        )
    except (TypeError, ValueError) as exc:
        raise ContractError("proof handoff temporal binding is not ISO date-time") from exc
    if (
        payload["execution_plan_digest"]
        != canonical_digest(payload["execution_plan"])
        or payload["execution_plan"].get("kind") == "not_ready"
        or payload["literature_authority"]["basis_status"] != "current"
        or payload["literature_consume_before"]
        != payload["literature_authority"]["consume_before"]
        or payload["resource_budget"] != expected_budget
        or payload["runtime_contract"] != _FORMAL_PROOF_RUNTIME_CONTRACT
        or payload["execution_policy"] != _DEFAULT_EXECUTION_POLICY
        or len(payload["conceptual_system_ids"]) != 1
        or not set(payload["conceptual_system_ids"]).issubset(
            payload["theory_ancestry"]["preferred_system_ids"]
        )
        or authorized_at.tzinfo is None
        or consume_before.tzinfo is None
        or authorized_at.astimezone(dt.timezone.utc)
        > consume_before.astimezone(dt.timezone.utc)
    ):
        raise ContractError("proof handoff current semantic/runtime binding mismatch")
    origins = payload["origin_receipts"]
    if origins != sorted(
        origins,
        key=lambda row: (row["receipt_id"], row["semantic_role"], row["output_path"]),
    ) or len({row["receipt_id"] for row in origins}) != len(origins):
        raise ContractError("proof origin receipt descriptors are not canonical and unique")
    expected_origin = {
        "receipt_id": payload["producer_receipt_id"],
        "receipt_digest": payload["producer_receipt_digest"],
        "semantic_role": "formal_claim_output",
        "output_path": payload["producer_output_path"],
        "output_digest": payload["producer_output_file_digest"],
    }
    if len(origins) != 1 or origins[0] != expected_origin:
        raise ContractError("proof origin receipt is not the formal producer receipt")
    expected_obligation_id = stable_identifier(
        "proof-obligation-v3",
        payload["formal_claim_authority_id"],
        payload["formal_claim_authority_digest"],
        payload["scheduled_action_id"],
        payload["scheduled_action_digest"],
        payload["formal_claim_digest"],
    )
    expected_handoff_id = stable_identifier(
        "proof-handoff-v3",
        expected_obligation_id,
        payload["formal_claim_authority_id"],
        payload["formal_claim_authority_digest"],
        payload["schedule_id"],
        payload["schedule_digest"],
        payload["scheduled_action_id"],
        payload["scheduled_action_digest"],
        canonical_digest(payload["runtime_contract"]),
        canonical_digest(payload["resource_budget"]),
        canonical_digest(payload["execution_policy"]),
        payload["literature_consume_before"],
        payload["authorized_at"],
    )
    if (
        payload["obligation_id"] != expected_obligation_id
        or payload["handoff_id"] != expected_handoff_id
    ):
        raise ContractError("proof handoff or obligation identity is not derived")
    return payload


def ensure_single_obligation(
    obligations: Sequence[Mapping[str, Any]],
    handoff: Mapping[str, Any],
    *,
    theory_authorization: object,
) -> tuple[list[dict[str, Any]], dict[str, Any], bool]:
    """Keep identity stable only after reopening the live committed handoff."""

    handoff = reopen_current_proof_handoff(theory_authorization, handoff)
    output = [copy.deepcopy(dict(row)) for row in obligations]
    same_conjecture = [
        row for row in output if row.get("conjecture_id") == handoff["conjecture_id"]
    ]
    for row in same_conjecture:
        if row.get("formal_claim_digest") == handoff["formal_claim_digest"]:
            if row.get("obligation_id") != handoff["obligation_id"]:
                raise ContractError("same formal claim has conflicting obligation identity")
            if row.get("content_digest") == handoff["content_digest"]:
                return output, copy.deepcopy(dict(row)), False
            output.append(handoff)
            return output, handoff, True
    if same_conjecture:
        expected = {str(row.get("obligation_id")) for row in same_conjecture}
        if handoff.get("supersedes_obligation_id") not in expected:
            raise ContractError(
                "a changed formal claim must explicitly supersede its prior obligation"
            )
    output.append(handoff)
    return output, handoff, True






def _file_authority(path: Path, *, executable: bool) -> dict[str, Any]:
    if path.is_symlink():
        raise ContractError(f"execution authority file is a symlink: {path}")
    resolved = path.resolve(strict=True)
    status = resolved.stat()
    if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
        raise ContractError(f"execution authority file is not a singly linked regular file: {path}")
    if executable and not os.access(resolved, os.X_OK):
        raise ContractError(f"execution authority file is not executable: {path}")
    return {
        "path": str(resolved),
        "sha256": file_digest(resolved),
        "byte_length": status.st_size,
        "executable": executable,
    }






def _worker_request(
    handoff: Mapping[str, Any], attempt_id: str
) -> dict[str, Any]:
    request = {
        "schema_version": 1,
        "message_kind": "proof_worker_request",
        "request_id": stable_identifier(
            "proof-worker-request-v1", attempt_id, handoff["formal_claim_digest"]
        ),
        "attempt_id": attempt_id,
        "adapter": handoff["proof_adapter"],
        "handoff_id": handoff["handoff_id"],
        "handoff_content_digest": handoff["content_digest"],
        "formal_claim": copy.deepcopy(handoff["formal_claim"]),
        "formal_claim_digest": handoff["formal_claim_digest"],
        "execution_plan": copy.deepcopy(handoff["execution_plan"]),
        "resource_budget": copy.deepcopy(handoff["resource_budget"]),
        "authority_boundary": (
            "worker_evaluates_only_the_exact_claim_and_has_no_theory_truth_or_"
            "physics_authority"
        ),
    }
    request["content_digest"] = _self_digest(request)
    validate_payload(request, WORKER_SCHEMA)
    return request


def _parse_canonical_object(event: Mapping[str, Any], label: str) -> dict[str, Any]:
    if (
        event.get("status") != "succeeded"
        or event.get("stdout_truncated") is not False
        or event.get("stdout_drain_incomplete") is not False
        or event.get("stdout_utf8_valid") is not True
    ):
        raise ContractError(f"{label} lacks complete successful UTF-8 stdout")
    raw = str(event.get("stdout", ""))
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContractError(f"{label} is not JSON") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} is not a JSON object")
    if raw.strip() != _canonical_json_bytes(value).decode("utf-8"):
        raise ContractError(f"{label} is not canonical JSON")
    return value


def _certificate(
    handoff: Mapping[str, Any],
    verdict: str,
    checker_kind: str,
    scoped: Mapping[str, Any],
) -> dict[str, Any]:
    row = {
        "schema_version": 1,
        "certificate_kind": verdict,
        "formal_claim_digest": handoff["formal_claim_digest"],
        "handoff_digest": handoff["content_digest"],
        "checker_kind": checker_kind,
        "scoped_certificate": copy.deepcopy(dict(scoped)),
        "authority_boundary": (
            "certificate_valid_only_for_the_exact_formal_claim_and_declared_"
            "checker_scope"
        ),
    }
    row["content_digest"] = _self_digest(row)
    return row


def _artifact_evidence(
    workspace: Path,
    declared: Mapping[str, Any] | None,
    *,
    baseline: set[str],
    policy: str,
) -> dict[str, Any] | None:
    if declared is None:
        if policy == "required_new_regular_file":
            raise ContractError("checker omitted its required new artifact")
        return None
    if policy == "none" or set(declared) != {
        "relative_path",
        "sha256",
        "byte_length",
    }:
        raise ContractError("checker artifact declaration violates its closed policy")
    relative = safe_relative_path(str(declared["relative_path"]), forbid_latest=True)
    if relative.as_posix() in baseline:
        raise ContractError("checker artifact existed before this attempt")
    path = contained_path(workspace, *relative.parts)
    before = os.lstat(path)
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ContractError("checker artifact is not a new singly linked regular file")
    payload = path.read_bytes()
    after = os.lstat(path)
    stable = (before.st_dev, before.st_ino, before.st_mode, before.st_nlink, before.st_size)
    if stable != (after.st_dev, after.st_ino, after.st_mode, after.st_nlink, after.st_size):
        raise ContractError("checker artifact changed while it was being validated")
    digest = "sha256:" + hashlib.sha256(payload).hexdigest()
    if digest != declared["sha256"] or len(payload) != declared["byte_length"]:
        raise ContractError("checker artifact bytes differ from its claim-bound response")
    return {
        "relative_path": relative.as_posix(),
        "sha256": digest,
        "byte_length": len(payload),
        "device": before.st_dev,
        "inode": before.st_ino,
        "mode": before.st_mode,
        "nlink": before.st_nlink,
    }


def _operational_failure(event: Mapping[str, Any]) -> tuple[str, str, dict[str, Any]]:
    status = str(event.get("status") or "worker_failed")
    execution = "resource_limited" if status in _RESOURCE_LIMITED else "failed"
    return (
        execution,
        "not_evaluated",
        {
            "kind": "operational_failure",
            "process_status": status,
            "reason": "proof process did not complete with an accepted protocol response",
        },
    )


def _interpret_process(
    handoff: Mapping[str, Any],
    attempt_id: str,
    event: Mapping[str, Any],
    workspace: Path,
    *,
    baseline: set[str],
) -> tuple[str, str, dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    if event.get("status") != "succeeded":
        execution, verdict, result = _operational_failure(event)
        return execution, verdict, result, None, None
    adapter = handoff["proof_adapter"]
    if adapter in {"exact", "finite_model"}:
        response = _parse_canonical_object(event, "built-in proof worker response")
        validate_payload(response, WORKER_SCHEMA)
        request = _worker_request(handoff, attempt_id)
        expected = {
            "request_id": request["request_id"],
            "attempt_id": attempt_id,
            "handoff_id": handoff["handoff_id"],
            "handoff_content_digest": handoff["content_digest"],
            "formal_claim_digest": handoff["formal_claim_digest"],
            "adapter": adapter,
        }
        if any(response.get(key) != value for key, value in expected.items()):
            raise ContractError("built-in worker response crossed its claim or attempt")
        expected_response_id = stable_identifier(
            "proof-worker-response-v1",
            request["request_id"],
            response["proof_verdict"],
            response["result"],
            response["certificate"],
        )
        if response["response_id"] != expected_response_id:
            raise ContractError("built-in worker response identity is not derived")
        if response["content_digest"] != _self_digest(response):
            raise ContractError("built-in worker response digest mismatch")
        worker_verdict = response["proof_verdict"]
        verdict = {
            "claim_validated_within_declared_scope": "proof_validated",
            "counterexample_validated_within_declared_scope": "counterexample_validated",
            "inconclusive": "inconclusive",
        }[worker_verdict]
        certificate = None
        if verdict in {"proof_validated", "counterexample_validated"}:
            if not isinstance(response.get("certificate"), Mapping):
                raise ContractError("decisive worker response lacks a scoped certificate")
            certificate = _certificate(
                handoff,
                verdict,
                "builtin_exact" if adapter == "exact" else "builtin_finite_model",
                response["certificate"],
            )
        return (
            "succeeded",
            verdict,
            {
                "kind": "builtin_worker_response",
                "response_digest": response["content_digest"],
                "worker_verdict": worker_verdict,
            },
            certificate,
            None,
        )
    if adapter == "lean":
        claim = handoff["formal_claim"]
        source_path = workspace / "Claim.lean"
        source_digest = file_digest(source_path)
        if "sorryAx" in str(event.get("stdout", "")) + str(event.get("stderr", "")):
            raise ContractError("Lean result depends on a forbidden sorry/admit axiom")
        scoped = {
            "proposition": claim["proposition"],
            "source_digest": source_digest,
            "axiom_policy": claim["axiom_policy"],
        }
        return (
            "succeeded",
            "proof_validated",
            {
                "kind": "lean_check",
                "proposition": claim["proposition"],
                "source_digest": source_digest,
            },
            _certificate(handoff, "proof_validated", "lean_kernel", scoped),
            None,
        )
    response = _parse_canonical_object(event, "external checker response")
    expected_keys = {
        "schema_version",
        "response_id",
        "request_id",
        "attempt_id",
        "handoff_id",
        "handoff_content_digest",
        "formal_claim_digest",
        "proof_verdict",
        "scoped_certificate",
        "artifact",
        "authority_boundary",
        "content_digest",
    }
    if set(response) != expected_keys or response.get("schema_version") != 1:
        raise ContractError("external checker response shape is not closed")
    request_id = stable_identifier(
        "external-checker-request-v1", attempt_id, handoff["formal_claim_digest"]
    )
    expected = {
        "request_id": request_id,
        "attempt_id": attempt_id,
        "handoff_id": handoff["handoff_id"],
        "handoff_content_digest": handoff["content_digest"],
        "formal_claim_digest": handoff["formal_claim_digest"],
        "authority_boundary": (
            "checker_response_is_claim_bound_but_checker_soundness_is_not_"
            "established_by_the_runtime"
        ),
    }
    if any(response.get(key) != value for key, value in expected.items()):
        raise ContractError("external checker response crossed its claim or attempt")
    expected_response_id = stable_identifier(
        "external-checker-response-v1",
        request_id,
        response["proof_verdict"],
        response["scoped_certificate"],
        response["artifact"],
    )
    if response["response_id"] != expected_response_id:
        raise ContractError("external checker response identity is not derived")
    if response["content_digest"] != _self_digest(response):
        raise ContractError("external checker response digest mismatch")
    worker_verdict = response["proof_verdict"]
    verdict_map = {
        "claim_validated_within_declared_scope": "proof_validated",
        "counterexample_validated_within_declared_scope": "counterexample_validated",
        "failed_premise_validated_within_declared_scope": "failed_premise_validated",
        "inconclusive": "inconclusive",
    }
    if worker_verdict not in verdict_map:
        raise ContractError("external checker verdict is unregistered")
    verdict = verdict_map[worker_verdict]
    scoped = response.get("scoped_certificate")
    certificate = None
    if verdict != "inconclusive":
        if not isinstance(scoped, Mapping):
            raise ContractError("decisive checker verdict lacks a scoped certificate")
        certificate = _certificate(
            handoff, verdict, "external_checker", scoped
        )
    plan = handoff["execution_plan"]
    artifact = _artifact_evidence(
        workspace,
        response.get("artifact"),
        baseline=baseline,
        policy=str(plan["artifact_policy"]),
    )
    return (
        "succeeded",
        verdict,
        {
            "kind": "external_checker_response",
            "response_digest": response["content_digest"],
            "checker_identity": plan["checker_identity"],
            "checker_version": plan["checker_version"],
        },
        certificate,
        artifact,
    )


def _ledger_events(
    handoff: Mapping[str, Any],
    attempt_id: str,
    execution_status: str,
    proof_verdict: str,
) -> list[dict[str, Any]]:
    base = {
        key: handoff[key]
        for key in (
            "target_id",
            "run_id",
            "cycle_id",
            "branch_id",
            "origin_prior_state_version",
            "theory_generation",
            "concept_id",
            "hypothesis_id",
            "conjecture_id",
            "obligation_id",
        )
    }
    terminal = {
        **base,
        "attempt_id": attempt_id,
        "event_type": "proof_attempt_terminal",
        "execution_status": execution_status,
        "proof_verdict": proof_verdict,
        "hypothesis_update": None,
        "branch_update": None,
        "operational_is_not_epistemic": execution_status != "succeeded",
    }
    events = [terminal]
    decisions = {
        "proof_validated": (
            "proof_certificate_validated",
            "eligible_for_independent_proof_criticism",
            None,
        ),
        "counterexample_validated": (
            "verified_counterexample",
            "refuted_within_certificate_scope",
            "backtrack_or_pivot",
        ),
        "failed_premise_validated": (
            "verified_failed_premise",
            "request_next_cycle_premise_reflection",
            "backtrack_or_reframe",
        ),
    }
    if proof_verdict in decisions:
        event_type, hypothesis_update, branch_update = decisions[proof_verdict]
        events.append(
            {
                **base,
                "attempt_id": attempt_id,
                "event_type": event_type,
                "execution_status": execution_status,
                "proof_verdict": proof_verdict,
                "hypothesis_update": hypothesis_update,
                "branch_update": branch_update,
                "operational_is_not_epistemic": False,
            }
        )
    return events


def _reflective_assimilation(
    handoff: Mapping[str, Any], execution_status: str, proof_verdict: str
) -> dict[str, Any]:
    recommendation = (
        "Independently criticize the claim-bound certificate in the next theory cycle."
        if proof_verdict == "proof_validated"
        else "Assimilate the scoped counterexample in the next theory cycle."
        if proof_verdict == "counterexample_validated"
        else "Review the checker-validated failed premise in the next theory cycle."
        if proof_verdict == "failed_premise_validated"
        else "Preserve the theory unchanged; the proof attempt supplied no decisive certificate."
    )
    return {
        "theory_programme_id": handoff["return_to_theory_programme_id"],
        "recommendation": recommendation,
        "authority_boundary": (
            "proof_runtime_returns_claim_bound_results_to_reflection_and_does_"
            "not_select_theory"
        ),
    }


def _not_started_reason(handoff: Mapping[str, Any]) -> str | None:
    if handoff["literature_authority"]["basis_status"] != "current":
        return "literature basis must be active-current before proof"
    plan = handoff["execution_plan"]
    if plan["kind"] == "not_ready":
        return str(plan["reason"])
    return None


def _validate_execution_authority(
    authority: Mapping[str, Any], handoff: Mapping[str, Any]
) -> None:
    if authority.get("content_digest") != _self_digest(authority):
        raise ContractError("proof execution authority digest mismatch")
    if (
        authority.get("formal_claim_digest") != handoff["formal_claim_digest"]
        or authority.get("handoff_digest") != handoff["content_digest"]
    ):
        raise ContractError("proof execution authority crossed its handoff")
    for descriptor in authority.get("files", []):
        if not isinstance(descriptor, Mapping):
            raise ContractError("proof execution file authority is malformed")
        observed = _file_authority(
            Path(str(descriptor["path"])), executable=descriptor["executable"]
        )
        if observed != descriptor:
            raise ContractError("proof execution authority file changed")


def validate_proof_receipt(
    receipt: Mapping[str, Any],
    handoff: Mapping[str, Any],
    *,
    expected_authorization_projection: Mapping[str, Any] | None = None,
) -> None:
    handoff = validate_proof_handoff(handoff)
    if expected_authorization_projection is None:
        raise ContractError(
            "current proof receipt validation requires live authorization evidence"
        )
    if receipt.get("schema_version") == 1:
        raise ContractError("proof receipt v1 is historical_decode_only")
    payload = copy.deepcopy(dict(receipt))
    validate_payload(payload, RECEIPT_SCHEMA)
    if payload["content_digest"] != _self_digest(payload):
        raise ContractError("proof receipt content digest mismatch")
    if payload["handoff_digest"] != handoff["content_digest"]:
        raise ContractError("proof receipt is stale for this handoff")
    fields = (
        "handoff_id",
        "formal_claim_digest",
        "target_id",
        "run_id",
        "cycle_id",
        "branch_id",
        "origin_prior_state_version",
        "theory_generation",
        "concept_id",
        "conceptual_system_ids",
        "hypothesis_id",
        "conjecture_id",
        "obligation_id",
        "proof_adapter",
    )
    for field in fields:
        if payload[field] != handoff[field]:
            raise ContractError(f"proof receipt/handoff mismatch for {field}")
    proof_authorization = payload["proof_execution_authorization"]
    if proof_authorization["content_digest"] != _self_digest(proof_authorization):
        raise ContractError("proof execution authorization projection digest mismatch")
    authorization_bindings = {
        "target_id": handoff["target_id"],
        "run_id": handoff["run_id"],
        "cycle_id": handoff["cycle_id"],
        "branch_id": handoff["branch_id"],
        "obligation_id": handoff["obligation_id"],
        "handoff_id": handoff["handoff_id"],
        "handoff_digest": handoff["content_digest"],
        "formal_claim_digest": handoff["formal_claim_digest"],
        "source_state_generation": handoff["theory_generation"],
    }
    if any(
        proof_authorization.get(key) != value
        for key, value in authorization_bindings.items()
    ):
        raise ContractError("proof execution authorization crossed its handoff ancestry")
    if (
        expected_authorization_projection is not None
        and proof_authorization != expected_authorization_projection
    ):
        raise ContractError("proof receipt differs from its live execution capability")
    attempt_id = stable_identifier(
        "proof-attempt-v2",
        handoff["obligation_id"],
        payload["attempt_number"],
        handoff["content_digest"],
    )
    if payload["attempt_id"] != attempt_id or payload["receipt_id"] != stable_identifier(
        "proof-receipt-v2", attempt_id, handoff["content_digest"]
    ):
        raise ContractError("proof attempt or receipt identity mismatch")
    try:
        started = dt.datetime.fromisoformat(payload["started_at"].replace("Z", "+00:00"))
        completed = dt.datetime.fromisoformat(
            payload["completed_at"].replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ContractError("proof receipt timestamps are invalid") from exc
    if started.tzinfo is None or completed.tzinfo is None or completed < started:
        raise ContractError("proof receipt completion precedes its start")
    workspace = payload["workspace"]
    if workspace["content_digest"] != _self_digest(workspace):
        raise ContractError("proof workspace descriptor digest mismatch")
    proof_root = Path(workspace["proof_root"]).resolve(strict=True)
    expected_workspace = contained_path(
        proof_root, *safe_relative_path(workspace["attempt_directory"]).parts
    ).resolve(strict=True)
    if str(expected_workspace) != workspace["resolved_path"]:
        raise ContractError("proof workspace descriptor path mismatch")
    authority = payload["execution_authority"]
    _validate_execution_authority(authority, handoff)
    process = payload["process_event"]
    resource = payload["resource_receipt"]
    if resource["budget"] != handoff["resource_budget"]:
        raise ContractError("proof resource budget differs from its handoff")
    if payload["resource_receipt_digest"] != canonical_digest(resource):
        raise ContractError("proof resource receipt digest mismatch")
    expected_resource_status = (
        "succeeded"
        if payload["execution_status"] in {"not_started", "succeeded"}
        else "worker_failed"
    )
    if resource["status"] != expected_resource_status:
        raise ContractError("proof resource receipt status differs from execution")
    baseline: set[str] = {"tmp", "Claim.lean"}
    if process is None:
        if resource["events"] or payload["execution_status"] != "not_started":
            raise ContractError("not-started proof receipt carries process evidence")
        reason = _not_started_reason(handoff)
        if reason is None:
            raise ContractError("proof receipt omitted a process for an executable handoff")
        expected_semantics = (
            "not_started",
            "not_evaluated",
            {"kind": "not_started", "reason": reason},
            None,
            None,
        )
    else:
        if resource["events"] != [process]:
            raise ContractError("proof process event differs from its sole resource event")
        if authority["logical_command"] != process["command"]:
            raise ContractError("proof process command differs from execution authority")
        base_environment = (
            minimal_replacement_environment(expected_workspace, create_temporary=False)
            if process.get("supervision_attempt") is not None
            else None
        )
        expected_environment = (
            complete_governed_process_environment(
                base_environment,
                deadline=resource["deadline"],
                budget=resource["budget"],
            )
            if base_environment is not None
            else None
        )
        try:
            validate_v2_process_event(
                process,
                accepted=process.get("status") == "succeeded",
                expected_workspace=expected_workspace,
                expected_replacement_environment=expected_environment,
                require_live_execution_authority=True,
            )
        except ValueError as exc:
            raise ContractError(f"proof v2 process replay failed: {exc}") from exc
        expected_semantics = _interpret_process(
            handoff,
            attempt_id,
            process,
            expected_workspace,
            baseline=baseline,
        )
    execution, verdict, result, certificate, artifact = expected_semantics
    if (
        payload["execution_status"] != execution
        or payload["proof_verdict"] != verdict
        or payload["result"] != result
        or payload["certificate"] != certificate
        or payload["artifact"] != artifact
    ):
        raise ContractError("proof receipt semantic projection differs from process protocol")
    expected_events = _ledger_events(handoff, attempt_id, execution, verdict)
    if payload["ledger_events"] != expected_events:
        raise ContractError("proof receipt ledger events are not parent-derived")
    if payload["reflective_assimilation"] != _reflective_assimilation(
        handoff, execution, verdict
    ):
        raise ContractError("proof reflective assimilation differs from its verdict")
    if payload["authority_boundary"] != RECEIPT_AUTHORITY_BOUNDARY:
        raise ContractError("proof receipt authority boundary mismatch")




def reopen_indexed_proof_receipt(
    index_path: Path | str,
    proof_authorization: ProofExecutionAuthorizationV2,
) -> dict[str, Any]:
    del index_path, proof_authorization
    raise ContractError(_RETIRED_V2_EXECUTION_MESSAGE)


def run_proof_continuation(
    proof_authorization: ProofExecutionAuthorizationV2,
    run_directory: Path | str,
    *,
    attempt_number: int = 1,
) -> dict[str, Any]:
    """Reject the retired v2 runner before filesystem or process activity."""

    del proof_authorization, run_directory, attempt_number
    raise ContractError(_RETIRED_V2_EXECUTION_MESSAGE)


def decode_historical_proof_handoff_v1(
    handoff: Mapping[str, Any], *, expected_artifact_digest: str
) -> dict[str, Any]:
    payload = copy.deepcopy(dict(handoff))
    validate_payload(payload, HISTORICAL_HANDOFF_SCHEMA)
    if canonical_digest(payload) != expected_artifact_digest:
        raise ContractError("historical proof handoff artifact digest mismatch")
    return {
        "status": "historical_decode_only",
        "authoritative_for_execution_or_theory": False,
        "artifact_digest": expected_artifact_digest,
        "payload": payload,
    }


def decode_historical_proof_receipt_v1(
    receipt: Mapping[str, Any], *, expected_artifact_digest: str
) -> dict[str, Any]:
    payload = copy.deepcopy(dict(receipt))
    validate_payload(payload, HISTORICAL_RECEIPT_SCHEMA)
    if canonical_digest(payload) != expected_artifact_digest:
        raise ContractError("historical proof receipt artifact digest mismatch")
    return {
        "status": "historical_decode_only",
        "authoritative_for_execution_or_theory": False,
        "artifact_digest": expected_artifact_digest,
        "payload": payload,
    }
