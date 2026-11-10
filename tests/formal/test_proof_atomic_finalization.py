# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial proof-terminalization, outbox, and recovery-state tests.

These tests begin only after the one-shot execution claim has been durably
consumed.  Terminal projections are inert evidence: the coordination ledger
must commit one terminal bundle, its exact byte attachments, receipt/index
records, and one pending N+1 request in the same generation without restoring
launch authority.  Later intake commits an exact theory-side reconciliation
outbox at N+1; coordination may consume that outbox after further verified
descendants without respawning or granting proof authority.
"""

from __future__ import annotations

import copy
import errno
import json
import multiprocessing
import os
import runpy
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Mapping

import pytest

import agentic.discovery.action_coordination_ledger as coordination_ledger
import agentic.discovery.proof_execution as proof_execution
import agentic.discovery.theory_gate as theory_gate
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    ProofExecutionClaimConsumed,
    ProofResultIntakeStale,
    ProofTerminalConflict,
)
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
)
from agentic.discovery.proof import (
    _consume_proof_prelaunch_capability,
    issue_proof_prelaunch_capability,
)
from agentic.discovery.proof_execution import (
    ProofExecutionClaimBinding,
    ProofExecutionTerminalResult,
    StagedProofInvocation,
    build_proof_terminal_replay_attachments,
    build_proof_execution_claim_binding,
    build_proof_execution_terminal_result,
    build_staging_rejection_terminal,
    build_staged_proof_invocation_recovery_attachments,
    validate_proof_execution_terminal_result,
    validate_terminal_result_projection,
)
from agentic.discovery.proof_v3_facade import (
    execute_proof_v3,
    reconcile_committed_proof_action_v3,
    reopen_consumed_proof_result_v3,
    run_committed_proof_action_v3,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    InjectedFailure,
    StateCorruptionError,
)


_SHARED_HELPERS = runpy.run_path(
    str(Path(__file__).with_name("test_proof_action_coordination_ledger.py"))
)
_canonical_proof_source = _SHARED_HELPERS["_canonical_proof_source"]
_ledger = _SHARED_HELPERS["_ledger"]

_EARLY_FAILPOINTS = (
    "after_state_write",
    "after_artifact_write:1",
    "after_manifest_write",
    "after_journal_prepared",
)
_LATE_FAILPOINTS = (
    "after_commit_rename",
    "after_pointer_write",
    "after_journal_complete",
)
_ALL_FAILPOINTS = _EARLY_FAILPOINTS + _LATE_FAILPOINTS


@pytest.fixture(scope="module")
def proof_source(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    return _canonical_proof_source(
        tmp_path_factory.mktemp("proof-atomic-terminal-source")
    )


def _claimed_case(
    source: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    ledger = _ledger(source, root)
    reservation = ledger.reserve_proof_attempt(
        theory_authorization=source["authorization"],
        handoff=source["handoff"],
    )
    capability = issue_proof_prelaunch_capability(
        coordination_ledger=ledger,
        theory_authorization=source["authorization"],
        handoff=source["handoff"],
        reservation_id=reservation.reservation_id,
    )
    (
        prelaunch,
        handoff,
        reserved_record,
        claim,
        claim_reference,
    ) = _consume_proof_prelaunch_capability(capability)
    binding = build_proof_execution_claim_binding(
        prelaunch_projection=prelaunch,
        handoff=handoff,
        reservation=reserved_record,
        execution_claim=claim,
        execution_claim_reference=claim_reference,
    )
    return {
        "ledger": ledger,
        "reservation": reservation,
        "claim": claim,
        "binding": binding,
        "root": root,
    }


def _staging_terminal(
    binding: ProofExecutionClaimBinding,
    *,
    reason_code: str = "staging_policy_rejected",
    observed_at: str = "2026-07-23T12:00:00Z",
) -> ProofExecutionTerminalResult:
    return build_staging_rejection_terminal(
        binding,
        reason_code=reason_code,
        observed_at=observed_at,
    )


def _redigest(value: dict[str, Any], field: str) -> None:
    value[field] = canonical_digest(
        {key: item for key, item in value.items() if key != field}
    )


@pytest.mark.expensive
def test_claimed_gap_is_read_only_then_terminalizes_once_with_exact_replay(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    case = _claimed_case(proof_source, root)
    ledger: ActionCoordinationLedger = case["ledger"]
    reservation = case["reservation"]
    binding: ProofExecutionClaimBinding = case["binding"]
    theory_generation = proof_source["fixture"]["store"].current_generation()

    recovery = ledger.read_proof_terminal_recovery_state(
        reservation.reservation_id
    )
    assert recovery["status"] == "claimed_without_terminal"
    assert recovery["terminal_bundle_present"] is False
    assert recovery["claim_remains_spent"] is True
    assert recovery["respawn_authorized"] is False
    assert recovery["abandonment_finalization_authorized"] is False
    assert recovery["caller_supplied_time_allowed"] is False
    assert {
        row["reason_code"] for row in recovery["required_recovery_paths"]
    } == {
        "launch_not_observed_abandoned",
        "execution_outcome_unknown_abandoned",
    }
    assert {
        row["governed_condition_required"]
        for row in recovery["required_recovery_paths"]
    } == {"expired_executor_lease"}
    assert not any(recovery["authority_nulls"].values())
    expected_recovery_digest = canonical_digest(
        {
            key: value
            for key, value in recovery.items()
            if key != "recovery_state_digest"
        }
    )
    assert recovery["recovery_state_digest"] == expected_recovery_digest
    assert ledger.current_generation() == 2
    with pytest.raises(ContractError, match="no terminal bundle"):
        ledger.read_proof_terminal_bundle(reservation.reservation_id)
    with pytest.raises(ProofExecutionClaimConsumed, match="already consumed"):
        issue_proof_prelaunch_capability(
            coordination_ledger=_ledger(proof_source, root),
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
        )

    abandoned = build_proof_execution_terminal_result(
        binding,
        terminal_status="abandoned_uncertain",
        execution_status="uncertain",
        proof_verdict="not_evaluated",
        reason_code="launch_not_observed_abandoned",
        started_at="2026-07-23T12:00:00Z",
        completed_at="2026-07-23T12:00:00Z",
    )
    with pytest.raises(ContractError, match="governed expired executor lease"):
        ledger.finalize_proof_execution(abandoned)
    assert ledger.current_generation() == 2

    terminal = _staging_terminal(binding)
    committed = ledger.finalize_proof_execution(terminal)
    assert committed.ledger_generation == 3
    assert committed.status == "staging_rejected"
    record = committed.record
    assert record["requested_terminal_status"] == "staging_rejected"
    terminalization = record["lifecycle_terminalization"]
    assert terminalization["action_terminalized"] is True
    assert terminalization["attempt_terminalized"] is True
    assert terminalization["claim_remains_spent"] is True
    assert terminalization["respawn_authorized"] is False
    assert record["theory_head_recheck"]["match"] is True
    assert record["terminal_receipt"]["operational_evidence_only"] is True
    assert record["terminal_receipt"]["same_cycle_theory_mutation"] is False
    membership = record["receipt_index_membership"]
    assert membership["unique_terminal_for_reservation"] is True
    assert membership["unique_terminal_for_attempt"] is True
    reflection = record["pending_n_plus_one_reflection_request"]
    assert reflection["request_status"] == "pending"
    assert (
        reflection["required_theory_generation_relation"]
        == "distinct_descendant_n_plus_one"
    )
    assert reflection["same_cycle_theory_mutation_authorized"] is False
    assert reflection["theory_mutation_performed"] is False
    assert reflection["proof_result_intake_consumed"] is False
    assert not any(reflection["authority_nulls"].values())
    replay_names = {
        row["logical_name"] for row in record["attachment_descriptors"]
    }
    assert replay_names == {
        "typed_replay/binding/prelaunch-projection.json",
        "typed_replay/binding/handoff.json",
        "typed_replay/binding/reservation.json",
        "typed_replay/binding/execution-claim.json",
        "typed_replay/binding/execution-claim-reference.json",
        "typed_replay/binding/projection.json",
    }
    assert record["launch_boundary_checkpoint"] is None
    attached = committed.ledger_commit_reference["attached_artifacts"]
    assert len(attached) == len(replay_names) + 3
    assert all(
        f"/{record['attempt_id']}/terminal/" in row["path"]
        for row in attached
    )
    assert proof_source["fixture"]["store"].current_generation() == (
        theory_generation
    )

    reopened_ledger = _ledger(proof_source, root)
    reopened = reopened_ledger.read_proof_terminal_bundle(
        reservation.reservation_id
    )
    retried = reopened_ledger.finalize_proof_execution(
        copy.deepcopy(terminal),
    )
    assert reopened == committed
    assert retried == committed
    assert reopened_ledger.current_generation() == 3
    generation, state = reopened_ledger._load_state()
    assert generation == 3
    assert state["record_count"] == 3
    assert set(state["proof_terminal_bundles"]) == {
        reservation.reservation_id
    }
    recovered_terminal = reopened_ledger.read_proof_terminal_recovery_state(
        reservation.reservation_id
    )
    assert recovered_terminal["status"] == "terminal_bundle_recovered"
    assert recovered_terminal["terminal_bundle_id"] == record[
        "terminal_bundle_id"
    ]
    assert recovered_terminal["respawn_authorized"] is False

    conflicting = _staging_terminal(
        binding,
        reason_code="different_staging_rejection",
        observed_at="2026-07-23T12:00:01Z",
    )
    with pytest.raises(ProofTerminalConflict, match="different terminal request"):
        reopened_ledger.finalize_proof_execution(conflicting)
    assert reopened_ledger.current_generation() == 3


@pytest.mark.expensive
@pytest.mark.parametrize("failpoint", _ALL_FAILPOINTS)
def test_terminal_transaction_failpoints_recover_exactly_one_bundle(
    proof_source: dict[str, Any],
    tmp_path: Path,
    failpoint: str,
) -> None:
    root = tmp_path / failpoint.replace(":", "-")
    case = _claimed_case(proof_source, root)
    reservation = case["reservation"]
    terminal_result = _staging_terminal(case["binding"])

    with pytest.raises(InjectedFailure, match=failpoint):
        case["ledger"].finalize_proof_execution(
            terminal_result,
            failpoint=failpoint,
        )

    recovered = _ledger(proof_source, root)
    generation, state = recovered._load_state()
    if failpoint in _EARLY_FAILPOINTS:
        assert generation == 2
        assert state["proof_terminal_bundles"] == {}
        gap = recovered.read_proof_terminal_recovery_state(
            reservation.reservation_id
        )
        assert gap["status"] == "claimed_without_terminal"
        assert gap["respawn_authorized"] is False
        with pytest.raises(ContractError, match="no terminal bundle"):
            recovered.read_proof_terminal_bundle(reservation.reservation_id)
        terminal = recovered.finalize_proof_execution(
            terminal_result,
        )
    else:
        assert generation == 3
        terminal = recovered.read_proof_terminal_bundle(
            reservation.reservation_id
        )

    retried = _ledger(proof_source, root).finalize_proof_execution(
        terminal_result,
    )
    assert retried == terminal
    assert retried.ledger_generation == 3
    final_generation, final_state = recovered._load_state()
    assert final_generation == 3
    assert final_state["record_count"] == 3
    assert set(final_state["proof_terminal_bundles"]) == {
        reservation.reservation_id
    }
    assert (
        recovered.read_proof_terminal_recovery_state(
            reservation.reservation_id
        )["status"]
        == "terminal_bundle_recovered"
    )


@pytest.mark.expensive
def test_terminal_head_drift_records_rebase_without_theory_mutation(
    tmp_path: Path,
) -> None:
    source = _canonical_proof_source(tmp_path / "source")
    case = _claimed_case(source, tmp_path / "coordination")
    terminal = _staging_terminal(case["binding"])
    store = source["fixture"]["store"]
    source_generation = store.current_generation()
    next_state = copy.deepcopy(store.read_state(source_generation))
    assert next_state is not None
    next_state["generation"] = source_generation + 1
    store.commit(
        expected_generation=source_generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=(
                    "branches/root/tests/proof-terminal-head-drift.json"
                ),
                content=b"{}\n",
                namespace=Namespace(
                    store.target_id,
                    store.run_id,
                    "root",
                    source_generation,
                ),
            ),
        ),
        idempotency_key="proof-terminal-head-drift",
        request_digest=canonical_digest(
            {"proof_terminal_head_drift": True}
        ),
    )

    result = case["ledger"].finalize_proof_execution(terminal)
    assert result.status == "rebase_required"
    assert result.record["requested_terminal_status"] == "staging_rejected"
    recheck = result.record["theory_head_recheck"]
    assert recheck["match"] is False
    assert recheck["disposition_reason"] == "theory_head_drift"
    assert recheck["effective_terminal_status"] == "rebase_required"
    reflection = result.record["pending_n_plus_one_reflection_request"]
    assert reflection["head_match"] is False
    assert reflection["rebase_required"] is True
    assert reflection["effective_terminal_status"] == "rebase_required"
    assert reflection["same_cycle_theory_mutation_authorized"] is False
    assert reflection["theory_mutation_performed"] is False
    assert store.current_generation() == source_generation + 1


@pytest.mark.expensive
def test_two_ledger_threads_converge_on_one_terminal_commit(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    case = _claimed_case(proof_source, root)
    terminal = _staging_terminal(case["binding"])
    ledgers = (
        _ledger(proof_source, root),
        _ledger(proof_source, root),
    )
    barrier = threading.Barrier(2)

    def finalize(candidate: ActionCoordinationLedger) -> Any:
        barrier.wait(timeout=30)
        return candidate.finalize_proof_execution(terminal)

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(finalize, ledgers))
    assert outcomes[0] == outcomes[1]
    assert outcomes[0].ledger_generation == 3
    generation, state = ledgers[0]._load_state()
    assert generation == 3
    assert state["record_count"] == 3
    assert len(state["proof_terminal_bundles"]) == 1


@pytest.mark.expensive
@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires POSIX fork")
def test_forked_finalizers_converge_without_reissuing_launch_authority(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    case = _claimed_case(proof_source, root)
    terminal = _staging_terminal(case["binding"])
    context = multiprocessing.get_context("fork")
    gate = context.Event()
    output = context.Queue()

    def finalize_in_child() -> None:
        try:
            gate.wait(timeout=60)
            result = _ledger(proof_source, root).finalize_proof_execution(
                terminal,
            )
            output.put(("ok", result.as_dict()))
        except BaseException as exc:  # pragma: no cover - parent reports detail
            output.put(("error", f"{type(exc).__name__}: {exc}"))

    processes = [
        context.Process(target=finalize_in_child)
        for _index in range(2)
    ]
    for process in processes:
        process.start()
    gate.set()
    outcomes = [output.get(timeout=180) for _index in processes]
    for process in processes:
        process.join(timeout=180)
        assert not process.is_alive()
        assert process.exitcode == 0
    output.close()

    assert [kind for kind, _value in outcomes] == ["ok", "ok"]
    assert outcomes[0][1] == outcomes[1][1]
    recovered = _ledger(proof_source, root)
    generation, state = recovered._load_state()
    assert generation == 3
    assert state["record_count"] == 3
    assert len(state["proof_terminal_bundles"]) == 1
    recovery = recovered.read_proof_terminal_recovery_state(
        case["reservation"].reservation_id
    )
    assert recovery["claim_remains_spent"] is True
    assert recovery["respawn_authorized"] is False


@pytest.mark.expensive
def test_strict_bundle_validator_rejects_nested_authority_and_index_tamper(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    case = _claimed_case(proof_source, tmp_path / "coordination")
    result = case["ledger"].finalize_proof_execution(
        _staging_terminal(case["binding"]),
    )
    generation, state = case["ledger"]._load_state()
    assert generation == 3
    reservation_id = case["reservation"].reservation_id
    reservation = state["proof_attempt_reservations"][reservation_id]
    claim = state["proof_execution_claims"][
        reservation["execution_claim_id"]
    ]
    original = result.record

    def receipt_authority(record: dict[str, Any]) -> None:
        receipt = record["terminal_receipt"]
        receipt["same_cycle_theory_mutation"] = True
        _redigest(receipt, "receipt_digest")

    def index_plurality(record: dict[str, Any]) -> None:
        membership = record["receipt_index_membership"]
        membership["unique_terminal_for_attempt"] = False
        _redigest(membership, "membership_digest")

    def reflection_authority(record: dict[str, Any]) -> None:
        reflection = record["pending_n_plus_one_reflection_request"]
        reflection["same_cycle_theory_mutation_authorized"] = True
        _redigest(reflection, "request_digest")

    def attachment_path(record: dict[str, Any]) -> None:
        record["attachment_descriptors"] = [
            {
                "attachment_kind": "checker_output",
                "logical_name": "checker_output",
                "source_relative_path": None,
                "artifact_path": (
                    "branches/coordination/proof-attempts/"
                    f"{record['attempt_id']}/terminal/evidence/substituted.bin"
                ),
                "sha256": "0" * 64,
                "byte_length": 0,
                "roles": ["checker_output"],
                "executable": False,
            }
        ]
        record["attachment_set_digest"] = canonical_digest(
            record["attachment_descriptors"]
        )

    mutators: tuple[Callable[[dict[str, Any]], None], ...] = (
        receipt_authority,
        index_plurality,
        reflection_authority,
        attachment_path,
    )
    for mutate in mutators:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        _redigest(candidate, "terminal_bundle_digest")
        with pytest.raises(StateCorruptionError):
            case["ledger"]._validate_proof_terminal_bundle_record(
                candidate,
                reservation=reservation,
                claim=claim,
                checkpoint=None,
            )


@pytest.mark.expensive
def test_retained_executor_bytes_are_mandatory_and_substitution_safe(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    ledger = _ledger(proof_source, root)
    reservation = ledger.reserve_proof_attempt(
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
    )
    capability = issue_proof_prelaunch_capability(
        coordination_ledger=ledger,
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
        reservation_id=reservation.reservation_id,
    )
    terminal = execute_proof_v3(capability)
    attachments = build_proof_terminal_replay_attachments(terminal)
    assert attachments

    logical_name = sorted(attachments)[0]
    omitted = dict(attachments)
    omitted.pop(logical_name)
    with pytest.raises(ContractError, match="exactly cover"):
        ledger.finalize_proof_execution(
            terminal,
            attachment_bytes=omitted,
        )
    substituted = dict(attachments)
    substituted[logical_name] = attachments[logical_name] + b"\x00"
    with pytest.raises(ContractError, match="differs from exact typed replay"):
        ledger.finalize_proof_execution(
            terminal,
            attachment_bytes=substituted,
        )

    exact = ledger.finalize_proof_execution(
        terminal,
        attachment_bytes=attachments,
    )
    reopened = ledger.read_proof_terminal_bundle(
        reservation.reservation_id
    )
    assert exact == reopened
    assert exact.ledger_generation == 4
    expected_paths = {
        row["artifact_path"]
        for row in exact.record["attachment_descriptors"]
    }
    committed_paths = {
        row["path"]
        for row in exact.ledger_commit_reference["attached_artifacts"]
    }
    derived_paths = {
        row["artifact_path"]
        for row in exact.record["derived_artifact_descriptors"]
    }
    assert committed_paths == expected_paths | derived_paths
    assert exact.record["lifecycle_terminalization"][
        "respawn_authorized"
    ] is False


@pytest.mark.expensive
def test_proof_v3_facade_runs_one_live_attempt_and_consumes_its_outbox(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proof_source = _canonical_proof_source(tmp_path / "facade-source")
    ledger = _ledger(proof_source, tmp_path / "facade-coordination")
    result = run_committed_proof_action_v3(
        ledger=ledger,
        theory_authorization=proof_source["authorization"],
    )

    assert result.launched_by_this_call is True
    assert result.reservation.record["attempt_number"] == 1
    assert result.terminal.record["reservation_id"] == (
        result.reservation.reservation_id
    )
    assert result.terminal.record["lifecycle_terminalization"][
        "respawn_authorized"
    ] is False
    assert result.intake.status == "proof_result_intake_consumed"
    assert result.intake.record["descendant_theory_head"]["generation"] == 2
    assert result.intake.record["theory_outbox"]["outbox_digest"] == (
        result.intake.record["theory_head_recheck"]["theory_outbox_digest"]
    )
    assert reopen_consumed_proof_result_v3(
        ledger=ledger,
        reservation_id=result.reservation.reservation_id,
    ) == result.intake

    spawn_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def forbidden_spawn(*args: Any, **kwargs: Any) -> Any:
        spawn_calls.append((args, kwargs))
        raise AssertionError("proof reconciliation attempted to respawn")

    monkeypatch.setattr(
        proof_execution.ResourceGovernor,
        "run_process",
        forbidden_spawn,
    )
    coordination_generation = ledger.current_generation()
    theory_generation = proof_source["fixture"]["store"].current_generation()
    reconciled = reconcile_committed_proof_action_v3(
        ledger=ledger,
        reservation_id=result.reservation.reservation_id,
    )
    assert reconciled.launched_by_this_call is False
    assert reconciled.reservation == result.reservation
    assert reconciled.terminal == result.terminal
    assert reconciled.intake == result.intake
    assert spawn_calls == []
    assert ledger.current_generation() == coordination_generation
    assert (
        proof_source["fixture"]["store"].current_generation()
        == theory_generation
    )


@pytest.mark.expensive
@pytest.mark.parametrize(
    "mutate",
    (
        lambda value: value.__setitem__("binding_digest", "f" * 64),
        lambda value: (
            value.__setitem__("terminal_status", "completed"),
            value.__setitem__("terminal_phase", "staging"),
            value.__setitem__("proof_verdict", "inconclusive"),
            value.__setitem__("completed_at", "2026-07-23T11:59:59Z"),
        ),
    ),
    ids=("detached-binding", "rehashed-inconsistent-shape"),
)
def test_serialized_terminal_decoder_is_history_only_and_cannot_commit(
    proof_source: dict[str, Any],
    tmp_path: Path,
    mutate: Callable[[dict[str, Any]], Any],
) -> None:
    case = _claimed_case(proof_source, tmp_path / "coordination")
    projection = validate_proof_execution_terminal_result(
        _staging_terminal(case["binding"])
    )
    mutate(projection)
    _redigest(projection, "content_digest")

    # Historical decoding remains available, including for old projections
    # whose cross-field semantics were not closed at serialization time.
    assert validate_terminal_result_projection(projection) == projection
    with pytest.raises(ContractError, match="history-only"):
        case["ledger"].finalize_proof_execution(projection)
    assert case["ledger"].current_generation() == 2


def _staged_invocation(
    case: Mapping[str, Any],
) -> StagedProofInvocation:
    binding = case["binding"]
    runtime_fd: int | None = None
    try:
        runtime_root, runtime_fd = proof_execution._create_runtime_root(
            case["ledger"].coordination_run_root,
            binding.projection["proof_runtime_ref"],
        )
        invocation, _profile, _authority = (
            proof_execution._stage_current_builtin_invocation(
                binding,
                runtime_root=runtime_root,
                runtime_fd=runtime_fd,
            )
        )
        return invocation
    finally:
        if runtime_fd is not None:
            os.close(runtime_fd)


def _force_expired_executor_lease(
    monkeypatch: pytest.MonkeyPatch,
    claim: Mapping[str, Any],
) -> None:
    _observed_at, clock_authority, clock_digest = (
        theory_gate.read_proof_recovery_clock_evidence()
    )
    monkeypatch.setattr(
        theory_gate,
        "read_proof_recovery_clock_evidence",
        lambda: (
            claim["executor_lease"]["expires_at"],
            clock_authority,
            clock_digest,
        ),
    )


@pytest.mark.expensive
def test_failed_checkpoint_recovers_from_bounded_claim_seed_without_respawn(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "coordination"
    case = _claimed_case(proof_source, root)
    claim = case["claim"]
    claim_result = case["ledger"].read_proof_execution_claim(
        claim["execution_claim_id"]
    )
    seed = claim_result.record["recovery_seed"]
    assert seed["seed_phase"] == "claim_binding"
    assert seed["attachment_count"] == 3
    assert seed["reconstructible_from_verified_commit"] is True
    assert seed["serialized_launch_authority"] is False
    assert seed["respawn_authorized"] is False
    assert len(
        claim_result.ledger_commit_reference["attached_artifacts"]
    ) == 3

    invocation = _staged_invocation(case)
    original_commit = case["ledger"]._store.commit

    def storage_full(*_args: Any, **_kwargs: Any) -> Any:
        raise OSError(errno.ENOSPC, "proof checkpoint storage full")

    monkeypatch.setattr(case["ledger"]._store, "commit", storage_full)
    with pytest.raises(OSError, match="proof checkpoint storage full"):
        case["ledger"].record_proof_launch_boundary_checkpoint(
            binding=case["binding"],
            invocation=invocation,
        )
    monkeypatch.setattr(case["ledger"]._store, "commit", original_commit)
    generation, state = case["ledger"]._load_state()
    assert generation == 2
    assert state["proof_launch_checkpoints"] == {}

    def respawn_forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("terminal recovery must not spawn")

    monkeypatch.setattr(
        proof_execution.ResourceGovernor,
        "run_process",
        respawn_forbidden,
    )
    _force_expired_executor_lease(monkeypatch, claim)
    theory_generation = proof_source["fixture"]["store"].current_generation()
    recovered = _ledger(
        proof_source, root
    ).recover_proof_terminal_gap(case["reservation"].reservation_id)
    terminal = recovered.record["terminal_projection"]
    assert recovered.ledger_generation == 4
    assert recovered.status == "abandoned_uncertain"
    assert terminal["reason_code"] == "launch_not_observed_abandoned"
    assert terminal["invocation_id"] is None
    assert terminal["process_event"] is None
    assert terminal["resource_receipt"] is None
    assert terminal["checker_output"] is None
    assert terminal["certificate"] is None
    assert terminal["artifacts"] == []
    generation, state = case["ledger"]._load_state()
    assert generation == 4
    assert state["record_count"] == 4
    recovery_claim = state["proof_terminal_recovery_claims"][
        case["reservation"].reservation_id
    ]
    assert recovery_claim["ledger_generation"] == 3
    assert recovery_claim["respawn_authorized"] is False
    recovery_state = case[
        "ledger"
    ].read_proof_terminal_recovery_state(
        case["reservation"].reservation_id
    )
    assert recovery_state["recovery_claim_present"] is True
    assert recovery_state["terminal_bundle_present"] is True
    assert recovery_state["abandonment_finalization_authorized"] is False
    assert proof_source["fixture"]["store"].current_generation() == (
        theory_generation
    )

    with pytest.raises(
        ProofTerminalConflict,
        match="recovery claim already won",
    ):
        case["ledger"].finalize_proof_execution(
            _staging_terminal(case["binding"])
        )


@pytest.mark.expensive
def test_recovery_seed_ceilings_reject_combined_max_shape_before_checkpoint(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _claimed_case(proof_source, tmp_path / "coordination")
    invocation = _staged_invocation(case)
    invocation_seed = (
        build_staged_proof_invocation_recovery_attachments(invocation)
    )
    claim_count = int(
        case["claim"]["recovery_seed"]["attachment_count"]
    )
    combined_count = claim_count + len(invocation_seed)
    assert len(invocation_seed) < combined_count - 1
    assert (
        coordination_ledger.MAX_PROOF_RECOVERY_SEED_BYTES
        + proof_execution.MAX_CHECKER_OUTPUT_BYTES
        + proof_execution.MAX_STAGED_FILE_BYTES
        + coordination_ledger.PROOF_TERMINAL_METADATA_RESERVE_BYTES
        <= coordination_ledger.MAX_PROOF_TERMINAL_ATTACHMENT_BYTES
    )
    assert (
        len(canonical_json(case["claim"]))
        <= coordination_ledger.MAX_PROOF_RECORD_BYTES
    )

    monkeypatch.setattr(
        coordination_ledger,
        "MAX_PROOF_RECOVERY_SEED_ATTACHMENTS",
        combined_count - 1,
    )
    with pytest.raises(
        ContractError,
        match="reserved terminal recovery capacity",
    ):
        case["ledger"].record_proof_launch_boundary_checkpoint(
            binding=case["binding"],
            invocation=invocation,
        )
    generation, state = case["ledger"]._load_state()
    assert generation == 2
    assert state["proof_launch_checkpoints"] == {}


@pytest.mark.expensive
def test_two_clean_process_recoverers_converge_without_respawn(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    case = _claimed_case(proof_source, root)
    invocation = _staged_invocation(case)
    checkpoint = case["ledger"].record_proof_launch_boundary_checkpoint(
        binding=case["binding"],
        invocation=invocation,
    )
    assert checkpoint.ledger_generation == 3
    assert checkpoint.record["recovery_seed"]["seed_phase"] == (
        "staged_invocation"
    )
    theory_store = proof_source["fixture"]["store"]
    theory_generation = theory_store.current_generation()
    gate_path = tmp_path / "recoverers.go"
    config = {
        "theory_root": str(theory_store.root),
        "coordination_root": str(root),
        "target_id": theory_store.target_id,
        "run_id": theory_store.run_id,
        "reservation_id": case["reservation"].reservation_id,
        "expires_at": case["claim"]["executor_lease"]["expires_at"],
        "gate_path": str(gate_path),
    }
    script = r"""
import json
import sys
import time
from pathlib import Path

import agentic.discovery.proof_execution as proof_execution
import agentic.discovery.theory_gate as theory_gate
from agentic.discovery.action_coordination_ledger import ActionCoordinationLedger
from agentic.state.discovery_transaction import DiscoveryTransactionStore

config = json.loads(sys.argv[1])
deadline = time.monotonic() + 30
while not Path(config["gate_path"]).exists():
    if time.monotonic() >= deadline:
        raise RuntimeError("recovery start gate timed out")
    time.sleep(0.01)
_observed_at, clock_authority, clock_digest = (
    theory_gate.read_proof_recovery_clock_evidence()
)
theory_gate.read_proof_recovery_clock_evidence = lambda: (
    config["expires_at"],
    clock_authority,
    clock_digest,
)
def respawn_forbidden(*_args, **_kwargs):
    raise AssertionError("clean-process recovery attempted to spawn")
proof_execution.ResourceGovernor.run_process = respawn_forbidden
store = DiscoveryTransactionStore(
    Path(config["theory_root"]),
    target_id=config["target_id"],
    run_id=config["run_id"],
)
ledger = ActionCoordinationLedger(
    theory_store=store,
    coordination_root=Path(config["coordination_root"]),
)
result = ledger.recover_proof_terminal_gap(config["reservation_id"])
print(json.dumps(result.as_dict(), sort_keys=True))
"""
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(Path(__file__).parents[2])
    children = [
        subprocess.Popen(
            [sys.executable, "-c", script, json.dumps(config)],
            cwd=str(Path(__file__).parents[2]),
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for _index in range(2)
    ]
    gate_path.write_text("recover\n", encoding="utf-8")
    outcomes: list[dict[str, Any]] = []
    for child in children:
        stdout, stderr = child.communicate(timeout=180)
        assert child.returncode == 0, stderr
        outcomes.append(json.loads(stdout.strip().splitlines()[-1]))
    assert outcomes[0] == outcomes[1]

    reopened = _ledger(proof_source, root)
    generation, state = reopened._load_state()
    assert generation == 5
    assert state["record_count"] == 5
    assert len(state["proof_terminal_recovery_claims"]) == 1
    assert len(state["proof_terminal_bundles"]) == 1
    recovery_claim = state["proof_terminal_recovery_claims"][
        case["reservation"].reservation_id
    ]
    assert recovery_claim["ledger_generation"] == 4
    terminal_result = reopened.read_proof_terminal_bundle(
        case["reservation"].reservation_id
    )
    terminal = terminal_result.record["terminal_projection"]
    assert terminal_result.ledger_generation == 5
    assert terminal["reason_code"] == (
        "execution_outcome_unknown_abandoned"
    )
    assert terminal["invocation_id"] == invocation.projection[
        "invocation_id"
    ]
    assert terminal["process_event"] is None
    assert terminal["resource_receipt"] is None
    assert terminal["checker_output"] is None
    assert terminal["certificate"] is None
    assert terminal["artifacts"] == []
    assert terminal_result.record["recovery_authority"][
        "recovery_claim_digest"
    ] == recovery_claim["recovery_claim_digest"]
    assert theory_store.current_generation() == theory_generation


@pytest.mark.expensive
def test_clean_recovery_head_drift_is_rebase_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _canonical_proof_source(tmp_path / "source")
    case = _claimed_case(source, tmp_path / "coordination")
    _force_expired_executor_lease(monkeypatch, case["claim"])
    store = source["fixture"]["store"]
    source_generation = store.current_generation()
    next_state = copy.deepcopy(store.read_state(source_generation))
    assert next_state is not None
    next_state["generation"] = source_generation + 1
    store.commit(
        expected_generation=source_generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=(
                    "branches/root/tests/proof-recovery-head-drift.json"
                ),
                content=b"{}\n",
                namespace=Namespace(
                    store.target_id,
                    store.run_id,
                    "root",
                    source_generation,
                ),
            ),
        ),
        idempotency_key="proof-recovery-head-drift",
        request_digest=canonical_digest(
            {"proof_recovery_head_drift": True}
        ),
    )

    recovered = case["ledger"].recover_proof_terminal_gap(
        case["reservation"].reservation_id
    )
    assert recovered.status == "rebase_required"
    assert recovered.record["requested_terminal_status"] == (
        "abandoned_uncertain"
    )
    assert recovered.record["theory_head_recheck"]["match"] is False
    assert recovered.record["theory_head_recheck"][
        "disposition_reason"
    ] == "theory_head_drift"
    assert recovered.record["pending_n_plus_one_reflection_request"][
        "rebase_required"
    ] is True
    assert store.current_generation() == source_generation + 1


@pytest.mark.expensive
def test_launch_terminal_requires_exact_checkpoint_not_projection_convention(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    case = _claimed_case(proof_source, tmp_path / "coordination")
    invocation = _staged_invocation(case)
    terminal = build_proof_execution_terminal_result(
        case["binding"],
        terminal_status="spawn_failed",
        execution_status="not_started",
        proof_verdict="not_evaluated",
        reason_code="governed_spawn_raised",
        started_at="2026-07-23T12:00:00Z",
        completed_at="2026-07-23T12:00:00Z",
        invocation=invocation,
    )

    with pytest.raises(ContractError, match="lacks its exact durable checkpoint"):
        case["ledger"].finalize_proof_execution(terminal)
    assert case["ledger"].current_generation() == 2


@pytest.mark.expensive
def test_checkpoint_rejects_serialized_inputs_and_detached_invocation(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    case = _claimed_case(proof_source, tmp_path / "coordination")
    invocation = _staged_invocation(case)
    with pytest.raises(ContractError, match="exact binding and invocation objects"):
        case["ledger"].record_proof_launch_boundary_checkpoint(
            binding=case["binding"].projection,
            invocation=invocation.projection,
        )
    assert case["ledger"].current_generation() == 2

    checkpoint = case["ledger"].record_proof_launch_boundary_checkpoint(
        binding=case["binding"],
        invocation=invocation,
    )
    assert checkpoint.ledger_generation == 3
    detached_root = (
        tmp_path
        / "detached-runtime"
        / case["binding"].projection["proof_runtime_ref"]
    )
    detached_invocation = StagedProofInvocation(
        claim_binding=case["binding"],
        runtime_route=invocation.runtime_route,
        stdin=invocation.stdin,
        files=invocation.files,
        logical_argv=invocation.logical_argv,
        materialized_argv=(
            invocation.materialized_argv[0],
            "-I",
            "-B",
            str(
                detached_root
                / "agentic/scripts/run_discovery_proof_worker_v3.py"
            ),
        ),
        artifact_policy=invocation.artifact_policy,
        _dependency_authority_bytes=invocation._dependency_authority_bytes,
        _executable_authority_bytes=invocation._executable_authority_bytes,
    )
    terminal = build_proof_execution_terminal_result(
        case["binding"],
        terminal_status="spawn_failed",
        execution_status="not_started",
        proof_verdict="not_evaluated",
        reason_code="governed_spawn_raised",
        started_at="2026-07-23T12:00:00Z",
        completed_at="2026-07-23T12:00:00Z",
        invocation=detached_invocation,
    )
    with pytest.raises(
        ContractError, match="checkpoint crossed its binding or invocation"
    ):
        case["ledger"].finalize_proof_execution(terminal)
    assert case["ledger"].current_generation() == 3


def _advance_theory_without_semantic_proof_effect(
    store: Any,
    *,
    label: str,
) -> None:
    generation = store.current_generation()
    next_state = copy.deepcopy(store.read_state(generation))
    assert next_state is not None
    next_state["generation"] = generation + 1
    store.commit(
        expected_generation=generation,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path=f"branches/root/tests/{label}.json",
                content=b"{}\n",
                namespace=Namespace(
                    store.target_id,
                    store.run_id,
                    "root",
                    generation,
                ),
            ),
        ),
        idempotency_key=f"proof-result-intake-{label}",
        request_digest=canonical_digest({label: True}),
    )


@pytest.mark.expensive
def test_proof_result_intake_recovers_each_boundary_exactly_once(
    tmp_path: Path,
) -> None:
    source = _canonical_proof_source(tmp_path / "source")
    case = _claimed_case(source, tmp_path / "coordination")
    ledger = case["ledger"]
    reservation_id = case["reservation"].reservation_id
    source_state = copy.deepcopy(source["fixture"]["store"].read_state(1))
    terminal = ledger.finalize_proof_execution(
        _staging_terminal(case["binding"])
    )
    assert terminal.record[
        "pending_n_plus_one_reflection_request"
    ]["proof_result_intake_consumed"] is False

    with pytest.raises(InjectedFailure, match="after_state_write"):
        ledger.consume_proof_result_intake(
            reservation_id,
            claim_failpoint="after_state_write",
        )
    assert ledger._load_state()[1]["proof_result_intake_claims"] == {}

    with pytest.raises(InjectedFailure, match="after_commit_rename"):
        ledger.consume_proof_result_intake(
            reservation_id,
            theory_failpoint="after_commit_rename",
        )
    generation, coordination = ledger._load_state()
    assert generation == 4
    assert len(coordination["proof_result_intake_claims"]) == 1
    assert coordination["proof_result_intake_consumptions"] == {}
    assert source["fixture"]["store"].current_generation() == 2

    with pytest.raises(InjectedFailure, match="after_state_write"):
        ledger.consume_proof_result_intake(
            reservation_id,
            consume_failpoint="after_state_write",
        )
    assert ledger.current_generation() == 4
    assert source["fixture"]["store"].current_generation() == 2

    consumed = ledger.consume_proof_result_intake(reservation_id)
    assert consumed.ledger_generation == 5
    assert consumed.status == "proof_result_intake_consumed"
    assert consumed.record["request_status_before"] == "pending"
    assert consumed.record["request_status_after"] == "consumed"
    assert consumed.record["source_theory_head"]["generation"] == 1
    assert consumed.record["descendant_theory_head"]["generation"] == 2
    assert consumed.record["theory_head_recheck"][
        "descendant_relationship"
    ] == "current"
    assert consumed.record["theory_outbox"]["outbox_id"].startswith(
        "proof-result-intake-theory-outbox-v1."
    )
    assert consumed == ledger.consume_proof_result_intake(reservation_id)
    assert consumed == ledger.read_proof_result_intake_consumption(
        reservation_id
    )

    plan = ledger.read_proof_result_intake_claim(
        reservation_id
    ).record["transition_plan"]
    _commit, artifacts = source[
        "fixture"
    ]["store"].read_verified_artifacts(
        2,
        [
            plan["intake_artifact_path"],
            plan["theory_outbox_artifact_path"],
        ],
    )
    outbox = json.loads(
        artifacts[plan["theory_outbox_artifact_path"]]
    )
    assert outbox["outbox_id"] == plan["theory_outbox_id"]
    assert outbox["outbox_digest"] == plan["theory_outbox_digest"]
    assert (
        canonical_digest(
            {
                key: value
                for key, value in outbox.items()
                if key != "outbox_digest"
            }
        )
        == outbox["outbox_digest"]
    )
    assert outbox["reconciliation_status"] == (
        "pending_coordination_consumption"
    )
    assert outbox["coordination_consumption_recorded_in_theory"] is False
    assert outbox["semantic_reflection_performed"] is False

    descendant_state = source["fixture"]["store"].read_state(2)
    assert descendant_state is not None and source_state is not None
    for field in (
        "branches",
        "hypotheses",
        "conceptual_systems",
        "active_theory_constellation",
    ):
        assert descendant_state[field] == source_state[field]
    reflection = next(
        row
        for row in descendant_state["reflections"].values()
        if row.get("intake_claim_id")
        == consumed.record["intake_claim_id"]
    )
    assert reflection["proof_result_intake_consumed"] is True
    assert reflection["semantic_reflection_performed"] is False
    assert reflection["same_cycle_theory_mutation"] is False
    assert terminal.record[
        "pending_n_plus_one_reflection_request"
    ]["proof_result_intake_consumed"] is False


@pytest.mark.expensive
def test_proof_result_intake_rejects_stale_fork_and_reconciles_later_head(
    tmp_path: Path,
) -> None:
    stale_source = _canonical_proof_source(tmp_path / "stale-source")
    stale = _claimed_case(stale_source, tmp_path / "stale-coordination")
    stale["ledger"].finalize_proof_execution(
        _staging_terminal(stale["binding"])
    )
    _advance_theory_without_semantic_proof_effect(
        stale_source["fixture"]["store"],
        label="stale-before-claim",
    )
    with pytest.raises(ProofResultIntakeStale, match="not active-current"):
        stale["ledger"].consume_proof_result_intake(
            stale["reservation"].reservation_id
        )
    assert stale["ledger"]._load_state()[1][
        "proof_result_intake_claims"
    ] == {}

    fork_source = _canonical_proof_source(tmp_path / "fork-source")
    fork = _claimed_case(fork_source, tmp_path / "fork-coordination")
    fork["ledger"].finalize_proof_execution(
        _staging_terminal(fork["binding"])
    )
    with pytest.raises(InjectedFailure, match="after_state_write"):
        fork["ledger"].consume_proof_result_intake(
            fork["reservation"].reservation_id,
            theory_failpoint="after_state_write",
        )
    _advance_theory_without_semantic_proof_effect(
        fork_source["fixture"]["store"],
        label="fork-after-claim",
    )
    fork_reservation_id = fork["reservation"].reservation_id
    superseded = fork["ledger"].consume_proof_result_intake(
        fork_reservation_id
    )
    assert superseded.status == "proof_result_intake_superseded"
    assert superseded.record["source_theory_head"]["generation"] == 1
    assert superseded.record["claimed_descendant_generation"] == 2
    assert superseded.record["occupying_theory_head"]["generation"] == 2
    assert superseded.record["observed_current_head"]["generation"] == 2
    assert superseded.record["coordination_claim_terminalized"] is True
    assert superseded.record["coordination_consumed"] is False
    assert superseded.record["claimed_transition_committed"] is False
    assert superseded.record["theory_outbox_committed"] is False
    assert superseded.record["semantic_reflection_performed"] is False
    assert superseded.record["recommission_authorized"] is False
    assert superseded.record["required_recommission_identity"] == (
        "new_formal_claim_schedule_action_reservation_attempt_and_intake_claim"
    )
    _generation, fork_coordination = fork["ledger"]._load_state()
    assert fork_coordination["proof_result_intake_consumptions"] == {}
    assert list(fork_coordination["proof_result_intake_resolutions"]) == [
        fork_reservation_id
    ]
    assert superseded == fork["ledger"].consume_proof_result_intake(
        fork_reservation_id
    )
    assert superseded == fork[
        "ledger"
    ].read_proof_result_intake_resolution(fork_reservation_id)
    with pytest.raises(ContractError, match="not consumed"):
        fork["ledger"].read_proof_result_intake_consumption(
            fork_reservation_id
        )

    _advance_theory_without_semantic_proof_effect(
        fork_source["fixture"]["store"],
        label="later-head-after-supersession",
    )
    assert superseded == fork[
        "ledger"
    ].read_proof_result_intake_resolution(fork_reservation_id)

    advanced_source = _canonical_proof_source(
        tmp_path / "advanced-source"
    )
    advanced = _claimed_case(
        advanced_source,
        tmp_path / "advanced-coordination",
    )
    advanced["ledger"].finalize_proof_execution(
        _staging_terminal(advanced["binding"])
    )
    with pytest.raises(InjectedFailure, match="after_state_write"):
        advanced["ledger"].consume_proof_result_intake(
            advanced["reservation"].reservation_id,
            consume_failpoint="after_state_write",
        )
    _advance_theory_without_semantic_proof_effect(
        advanced_source["fixture"]["store"],
        label="advance-after-outbox-before-consumption",
    )
    consumed = advanced["ledger"].consume_proof_result_intake(
        advanced["reservation"].reservation_id
    )
    assert consumed.record["descendant_theory_head"]["generation"] == 2
    assert consumed.record["theory_head_recheck"][
        "observed_current_head"
    ]["generation"] == 3
    assert consumed.record["theory_head_recheck"][
        "descendant_relationship"
    ] == "verified_ancestor"
    assert consumed == advanced[
        "ledger"
    ].read_proof_result_intake_consumption(
        advanced["reservation"].reservation_id
    )


@pytest.mark.expensive
def test_same_reservation_concurrent_intake_commits_one_outbox_and_consumption(
    tmp_path: Path,
) -> None:
    source = _canonical_proof_source(tmp_path / "concurrent-source")
    case = _claimed_case(source, tmp_path / "concurrent-coordination")
    case["ledger"].finalize_proof_execution(
        _staging_terminal(case["binding"])
    )
    reservation_id = case["reservation"].reservation_id

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(
                case["ledger"].consume_proof_result_intake,
                reservation_id,
            )
            for _index in range(2)
        ]
        results = [future.result() for future in futures]

    assert results[0] == results[1]
    assert source["fixture"]["store"].current_generation() == 2
    _generation, coordination = case["ledger"]._load_state()
    assert list(coordination["proof_result_intake_claims"]) == [
        reservation_id
    ]
    assert list(coordination["proof_result_intake_consumptions"]) == [
        reservation_id
    ]
    plan = results[0].record["theory_outbox"]
    commit = source["fixture"]["store"].read_verified_commit(2)
    assert [
        row["path"]
        for row in commit.manifest["artifacts"]
        if row["path"] == plan["artifact_path"]
    ] == [plan["artifact_path"]]


@pytest.mark.expensive
@pytest.mark.parametrize(
    ("terminal_failpoint", "terminal_was_durable"),
    (
        ("after_state_write", False),
        ("after_commit_rename", True),
    ),
)
def test_recovery_claim_to_terminal_failpoints_bind_time_and_never_respawn(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    terminal_failpoint: str,
    terminal_was_durable: bool,
) -> None:
    source = _canonical_proof_source(
        tmp_path / terminal_failpoint.replace(":", "-")
    )
    case = _claimed_case(source, tmp_path / f"coord-{terminal_failpoint}")
    reservation_id = case["reservation"].reservation_id
    _force_expired_executor_lease(monkeypatch, case["claim"])

    def respawn_forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("terminal recovery must never respawn")

    monkeypatch.setattr(
        proof_execution.ResourceGovernor,
        "run_process",
        respawn_forbidden,
    )
    with pytest.raises(InjectedFailure, match=terminal_failpoint):
        case["ledger"].recover_proof_terminal_gap(
            reservation_id,
            terminal_failpoint=terminal_failpoint,
        )
    generation, state = case["ledger"]._load_state()
    assert len(state["proof_terminal_recovery_claims"]) == 1
    assert bool(state["proof_terminal_bundles"]) is terminal_was_durable
    recovery_claim = state["proof_terminal_recovery_claims"][
        reservation_id
    ]

    if not terminal_was_durable:
        original_commit = case["ledger"]._store.commit

        def storage_full(*_args: Any, **_kwargs: Any) -> Any:
            raise OSError(errno.ENOSPC, "terminal storage remains full")

        monkeypatch.setattr(case["ledger"]._store, "commit", storage_full)
        with pytest.raises(OSError, match="terminal storage remains full"):
            case["ledger"].recover_proof_terminal_gap(reservation_id)
        monkeypatch.setattr(case["ledger"]._store, "commit", original_commit)
        assert case["ledger"].current_generation() == generation

    recovered = case["ledger"].recover_proof_terminal_gap(reservation_id)
    projection = recovered.record["terminal_projection"]
    assert projection["started_at"] == recovery_claim["terminal_observed_at"]
    assert projection["completed_at"] == recovery_claim[
        "terminal_observed_at"
    ]
    assert recovered == case["ledger"].recover_proof_terminal_gap(
        reservation_id
    )

    tampered = copy.deepcopy(projection)
    tampered["started_at"] = "2026-07-23T00:00:00Z"
    reservation = state["proof_attempt_reservations"][reservation_id]
    with pytest.raises(StateCorruptionError):
        coordination_ledger._validate_recovery_abandonment_authority(
            recovered.record["recovery_authority"],
            reservation=reservation,
            claim=case["claim"],
            recovery_claim=recovery_claim,
            terminal=tampered,
        )
