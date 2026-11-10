# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Production-boundary tests for reservation-first discovery action waves."""

from __future__ import annotations

import copy
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Sequence

import pytest

from agentic.discovery import action_coordination_ledger as ledger_protocol
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    ActionReservationConflict,
)
from agentic.discovery.action_execution_boundary import (
    ACTION_KIND_SUPPORT_POLICY,
    ActionCallbackExecutionError,
    ActionLedgerRolloverRequired,
    ActionSupportPolicyError,
    ActionWorkerOutcome,
    POST_RESULT_SUPPORT_MARKER,
    SUPPORT_ROOT_IDENTITY_FIELD,
    execute_frozen_action_wave,
)
from agentic.discovery.contracts import (
    Namespace,
    canonical_digest,
    stable_identifier,
)
from agentic.discovery.scheduler import (
    ACTION_KINDS,
    schedule_discovery_actions,
)
from agentic.experiments.content_graph_transactions import (
    ContentGraphTransactionResult,
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


TARGET_ID = "action-execution-boundary-target"
RUN_ID = "action-execution-boundary-run"
PROGRAMME_ID = "action-execution-boundary-programme"
BRANCH_ID = "theory"


def _theory_store(root: Path) -> DiscoveryTransactionStore:
    return DiscoveryTransactionStore(
        root,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )


def _object(
    generation: int,
    name: str,
) -> PreparedContentObject:
    return prepare_content_object(
        object_kind=(
            "world_matrix_aggregation_root_v3"
            if name == "support-aggregation"
            else "world_projection_index_v3"
        ),
        value={
            "fixture_kind": name,
            "generation": generation,
            "authority_boundary": (
                "storage fixture only; no experiment or physics authority"
            ),
        },
        path=(
            f"branches/{BRANCH_ID}/content-graphs/g{generation}/"
            f"objects/{name}.json"
        ),
    )


def _publish_theory_head(
    store: DiscoveryTransactionStore,
    generation: int,
    *,
    root_names: Sequence[str] = ("theory-root", "support-aggregation"),
) -> ContentGraphTransactionResult:
    objects = tuple(_object(generation, name) for name in root_names)
    object_ids = [row.ref["object_id"] for row in objects]
    graph = build_content_object_graph(
        local_descriptors=[row.descriptor for row in objects],
        imported_handles=[],
        ordered_roots=object_ids,
        edges=[],
        topological_order=object_ids,
    )
    graph_path = (
        f"branches/{BRANCH_ID}/content-graphs/g{generation}/graph.json"
    )
    prepared = prepare_content_graph_transaction(
        expected_generation=generation - 1,
        state={
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": generation,
            "programme_id": PROGRAMME_ID,
            "fixture_generation": generation,
        },
        namespace=Namespace(
            TARGET_ID,
            RUN_ID,
            BRANCH_ID,
            generation - 1,
        ),
        graph_artifact_path=graph_path,
        graph=graph,
        local_objects=objects,
    )
    return commit_content_graph_transaction(
        store=store,
        transaction=prepared,
    )


def _branch(branch_id: str, *, unification: float = 0.6) -> dict[str, Any]:
    return {
        "branch_id": branch_id,
        "status": "incubating",
        "maturity": "incubating",
        "conceptual_corner": branch_id,
        "semantic_prompt_digest": canonical_digest(
            {"semantic_prompt": branch_id}
        ),
        "depends_on": [],
        "dependency_ids": [],
        "theory_virtues": {
            "essential_relevance": 1.0,
            "root_tension_contact": 0.8,
            "expected_understanding_gain": 0.8,
            "expected_unification_gain": unification,
            "conceptual_fertility": 0.8,
            "programme_impact": 0.8,
            "maturity": 0.4,
        },
        "estimated_cost": 1.0,
        "premature_closure_risk": 0.2,
    }


def _schedule(
    *,
    state_version: int = 1,
    branches: Sequence[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], str]:
    schedule = schedule_discovery_actions(
        {
            "target_id": TARGET_ID,
            "state_version": state_version,
            "literature": {
                "status": "validated_current",
                "snapshot_id": "snapshot.current",
                "assimilated_snapshot_id": "snapshot.current",
            },
            "branches": list(branches or (_branch("branch-one"),)),
            "semantic_plateau_limit": 3,
            "required_conceptual_corners": [],
            "new_evidence": [],
        }
    )
    branch_action_ids = {
        row["action_id"] for row in schedule["actions"] if row["branch_ids"]
    }
    matching_waves = [
        row
        for row in schedule["waves"]
        if set(row["action_ids"]).issubset(branch_action_ids)
        and row["action_ids"]
    ]
    assert len(matching_waves) == 1
    return schedule, matching_waves[0]["wave_id"]


def _mark_post_result(
    schedule: dict[str, Any],
    *,
    root_object_id: str,
) -> tuple[dict[str, Any], str]:
    marked = copy.deepcopy(schedule)
    selected = [row for row in marked["actions"] if row["branch_ids"]]
    assert len(selected) == 1
    action = selected[0]
    assert action["kind"] == "reflect"
    old_action_id = action["action_id"]
    action["restrictions"].append(POST_RESULT_SUPPORT_MARKER)
    action["payload"][SUPPORT_ROOT_IDENTITY_FIELD] = [root_object_id]
    action["action_id"] = stable_identifier(
        "action",
        {
            "kind": action["kind"],
            "target_id": action["target_id"],
            "state_version": action["state_version"],
            "branch_ids": action["branch_ids"],
            "depends_on": action["depends_on"],
            "payload": action["payload"],
        },
    )
    wave = next(
        row for row in marked["waves"] if old_action_id in row["action_ids"]
    )
    wave["action_ids"] = [action["action_id"]]
    wave["wave_id"] = stable_identifier("wave", wave["action_ids"])
    marked["schedule_digest"] = canonical_digest(
        marked,
        exclude_keys=("schedule_digest", "created_at", "consumption_log"),
    )
    return marked, wave["wave_id"]


def _mark_prove(schedule: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Retarget one frozen branch wave without leaving a stale identity."""

    marked = copy.deepcopy(schedule)
    selected = [row for row in marked["actions"] if row["branch_ids"]]
    assert len(selected) == 1
    action = selected[0]
    old_action_id = action["action_id"]
    action["kind"] = "prove"
    action["payload"]["requested_kind"] = "prove"
    action["action_id"] = stable_identifier(
        "action",
        {
            "kind": action["kind"],
            "target_id": action["target_id"],
            "state_version": action["state_version"],
            "branch_ids": action["branch_ids"],
            "depends_on": action["depends_on"],
            "payload": action["payload"],
        },
    )
    wave = next(
        row for row in marked["waves"] if old_action_id in row["action_ids"]
    )
    wave["action_ids"] = [action["action_id"]]
    wave["wave_id"] = stable_identifier("wave", wave["action_ids"])
    marked["schedule_digest"] = canonical_digest(
        marked,
        exclude_keys=("schedule_digest", "created_at", "consumption_log"),
    )
    return marked, wave["wave_id"]


def _setup(
    tmp_path: Path,
) -> tuple[
    DiscoveryTransactionStore,
    ContentGraphTransactionResult,
    ActionCoordinationLedger,
]:
    theory = _theory_store(tmp_path / "theory-store")
    head = _publish_theory_head(theory, 1)
    ledger = ActionCoordinationLedger(
        theory_store=theory,
        coordination_root=tmp_path / "coordination-store",
    )
    return theory, head, ledger


def _selected_action_ids(
    schedule: dict[str, Any],
    wave_id: str,
) -> tuple[str, ...]:
    wave = next(row for row in schedule["waves"] if row["wave_id"] == wave_id)
    return tuple(wave["action_ids"])


def test_policy_is_total_and_probe_is_theory_only() -> None:
    assert set(ACTION_KIND_SUPPORT_POLICY) == ACTION_KINDS
    assert ACTION_KIND_SUPPORT_POLICY["probe"] == "theory_only"
    assert ACTION_KIND_SUPPORT_POLICY["reflect"] == "closed_post_result_marker"
    assert ACTION_KIND_SUPPORT_POLICY["reframe"] == "closed_post_result_marker"
    assert (
        ACTION_KIND_SUPPORT_POLICY["prove"]
        == "dedicated_proof_execution_only"
    )


@pytest.mark.parametrize("lifecycle_request", ("execute", "release"))
def test_prove_wave_is_rejected_before_callback_or_ledger_lifecycle(
    tmp_path: Path,
    lifecycle_request: str,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    schedule, _wave_id = _schedule()
    prove_schedule, prove_wave_id = _mark_prove(schedule)
    action_id = _selected_action_ids(prove_schedule, prove_wave_id)[0]
    callback_calls: list[str] = []

    def forbidden_callback(_invocation):
        callback_calls.append(action_id)
        return ActionWorkerOutcome("completed")

    with pytest.raises(
        ActionSupportPolicyError,
        match="dedicated attempt-specific proof execution boundary",
    ):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=prove_schedule,
            wave_id=prove_wave_id,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            consumer_id=f"consumer.prove.{lifecycle_request}",
            callbacks={action_id: forbidden_callback},
            lifecycle_request=lifecycle_request,
        )

    assert callback_calls == []
    assert ledger.current_generation() == 0
    assert theory.current_generation() == 1


def test_callback_observes_durable_reservation_and_conflict_runs_no_side_effect(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    schedule, wave_id = _schedule()
    action_ids = _selected_action_ids(schedule, wave_id)
    observations: list[str] = []

    def worker(invocation):
        reopened = ledger.read_reservation(
            invocation.reservation["reservation_id"]
        )
        assert reopened.status == "reserved"
        assert reopened.record["action_ids"] == sorted(action_ids)
        observations.append(invocation.action["action_id"])
        return ActionWorkerOutcome(
            "completed",
            (canonical_digest({"worker": invocation.action["action_id"]}),),
        )

    completed = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.primary",
        callbacks={action_ids[0]: worker},
    )
    assert completed.terminal.status == "completed"
    assert observations == list(action_ids)
    assert ledger.current_generation() == 2
    assert theory.current_generation() == 1

    second_schedule, second_wave = _schedule(state_version=2)
    second_action_ids = _selected_action_ids(second_schedule, second_wave)
    ledger.reserve(
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        schedule_id=second_schedule["schedule_id"],
        schedule_digest=second_schedule["schedule_digest"],
        action_ids=second_action_ids,
        consumer_id="consumer.manual-owner",
    )
    side_effects: list[str] = []
    with pytest.raises(ActionReservationConflict):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=second_schedule,
            wave_id=second_wave,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            consumer_id="consumer.competing",
            callbacks={
                second_action_ids[0]: lambda _invocation: (
                    side_effects.append("forbidden")
                    or ActionWorkerOutcome("completed")
                )
            },
        )
    assert side_effects == []


def test_support_requirement_is_derived_from_frozen_post_result_marker(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    schedule, theory_wave = _schedule()
    theory_action_id = _selected_action_ids(schedule, theory_wave)[0]
    aggregation = head.root_refs[-1]

    with pytest.raises(
        ActionSupportPolicyError,
        match="theory-only action wave rejects",
    ):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=schedule,
            wave_id=theory_wave,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            aggregation_root_reference=aggregation,
            consumer_id="consumer.theory",
            callbacks={
                theory_action_id: lambda _invocation: ActionWorkerOutcome(
                    "completed"
                )
            },
        )

    marked, support_wave = _mark_post_result(
        schedule,
        root_object_id=aggregation["object_id"],
    )
    support_action_id = _selected_action_ids(marked, support_wave)[0]
    with pytest.raises(
        ActionSupportPolicyError,
        match="requires its exact active",
    ):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=marked,
            wave_id=support_wave,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            consumer_id="consumer.support.missing",
            callbacks={
                support_action_id: lambda _invocation: ActionWorkerOutcome(
                    "completed"
                )
            },
        )

    with pytest.raises(
        ActionSupportPolicyError,
        match="differs from the frozen action identity",
    ):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=marked,
            wave_id=support_wave,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            aggregation_root_reference=head.root_refs[0],
            consumer_id="consumer.support.mismatched",
            callbacks={
                support_action_id: lambda _invocation: ActionWorkerOutcome(
                    "completed"
                )
            },
        )

    callback_support: list[tuple[dict[str, Any], ...]] = []

    def supported_worker(invocation):
        callback_support.append(
            tuple(dict(row) for row in invocation.support_root_references)
        )
        return ActionWorkerOutcome("completed")

    result = execute_frozen_action_wave(
        ledger=ledger,
        schedule=marked,
        wave_id=support_wave,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        aggregation_root_reference=aggregation,
        consumer_id="consumer.support",
        callbacks={support_action_id: supported_worker},
    )
    assert result.support_requirement == "n_plus_7_support_dependent"
    assert callback_support == [(dict(aggregation),)]
    assert (
        result.reservation.record["theory_binding"][
            "n_plus_7_support_root_references"
        ]
        == [aggregation]
    )


def test_callback_exception_is_terminalized_before_it_is_raised(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    schedule, wave_id = _schedule()
    action_id = _selected_action_ids(schedule, wave_id)[0]

    def exploding_worker(_invocation):
        raise RuntimeError("worker failed after an unknown effect boundary")

    with pytest.raises(ActionCallbackExecutionError) as captured:
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=schedule,
            wave_id=wave_id,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            consumer_id="consumer.exploding",
            callbacks={action_id: exploding_worker},
        )
    result = captured.value.result
    assert result.terminal.status == "compensation_required"
    assert result.terminal.record["requested_terminal_status"] == (
        "compensation_required"
    )
    assert result.worker_outcomes[0]["callback_state"] == (
        "raised_effect_state_unknown"
    )
    assert ledger.read_terminal(result.reservation.reservation_id) == (
        result.terminal
    )
    assert theory.current_generation() == 1


def test_typed_failure_is_finalized_without_compensation_escalation(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    schedule, wave_id = _schedule()
    action_id = _selected_action_ids(schedule, wave_id)[0]
    result = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.typed-failure",
        callbacks={
            action_id: lambda _invocation: ActionWorkerOutcome(
                "failed",
                (canonical_digest({"failure": "no external effect"}),),
            )
        },
    )
    assert result.terminal.status == "failed"
    assert result.worker_outcomes[0]["status"] == "failed"


def test_release_consumes_claim_and_retry_requires_new_frozen_schedule(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    schedule, wave_id = _schedule()
    first_action_id = _selected_action_ids(schedule, wave_id)[0]
    released = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.release",
        callbacks={},
        lifecycle_request="release",
    )
    assert released.terminal.status == "released"
    assert released.worker_outcomes[0]["callback_state"] == (
        "not_invoked_explicit_release"
    )

    exact_retry_calls: list[str] = []
    exact_retry = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.release",
        callbacks={
            first_action_id: lambda _invocation: (
                exact_retry_calls.append("forbidden")
                or ActionWorkerOutcome("completed")
            )
        },
    )
    assert exact_retry.replayed_terminal is True
    assert exact_retry.terminal == released.terminal
    assert exact_retry.worker_outcomes == ()
    assert exact_retry_calls == []

    retry_schedule, retry_wave = _schedule(state_version=2)
    retry_action_id = _selected_action_ids(retry_schedule, retry_wave)[0]
    retry_calls: list[str] = []
    retry = execute_frozen_action_wave(
        ledger=ledger,
        schedule=retry_schedule,
        wave_id=retry_wave,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.release.retry",
        callbacks={
            retry_action_id: lambda _invocation: (
                retry_calls.append("new-schedule")
                or ActionWorkerOutcome("completed")
            )
        },
    )
    assert retry.terminal.status == "completed"
    assert retry_calls == ["new-schedule"]


def test_theory_head_drift_is_ledger_derived_rebase_required(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    schedule, wave_id = _schedule()
    action_id = _selected_action_ids(schedule, wave_id)[0]

    def advance_head(_invocation):
        _publish_theory_head(theory, 2)
        return ActionWorkerOutcome("completed")

    result = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.head-drift",
        callbacks={action_id: advance_head},
    )
    assert result.terminal.record["requested_terminal_status"] == "completed"
    assert result.terminal.status == "rebase_required"
    assert result.terminal.record["theory_head_recheck"]["match"] is False
    assert result.terminal.record["theory_head_recheck"][
        "disposition_reason"
    ] == "theory_head_drift"
    assert theory.current_generation() == 2


def test_parallel_wave_callbacks_share_one_prior_reservation(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    left = _branch("branch-left", unification=0.9)
    right = _branch("branch-right", unification=0.4)
    left["theory_virtues"]["expected_understanding_gain"] = 0.4
    right["theory_virtues"]["expected_understanding_gain"] = 0.9
    schedule, wave_id = _schedule(
        branches=(left, right)
    )
    action_ids = _selected_action_ids(schedule, wave_id)
    assert len(action_ids) == 2
    wave = next(row for row in schedule["waves"] if row["wave_id"] == wave_id)
    assert wave["mode"] == "parallel"
    callback_barrier = threading.Barrier(2)
    observed: list[tuple[str, str]] = []
    observed_lock = threading.Lock()

    def worker(invocation):
        callback_barrier.wait(timeout=5)
        reopened = ledger.read_reservation(
            invocation.reservation["reservation_id"]
        )
        with observed_lock:
            observed.append(
                (invocation.action["action_id"], reopened.reservation_id)
            )
        return ActionWorkerOutcome("completed")

    result = execute_frozen_action_wave(
        ledger=ledger,
        schedule=schedule,
        wave_id=wave_id,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.parallel",
        callbacks={action_id: worker for action_id in action_ids},
    )
    assert result.terminal.status == "completed"
    assert {action_id for action_id, _reservation_id in observed} == set(
        action_ids
    )
    assert {
        reservation_id for _action_id, reservation_id in observed
    } == {result.reservation.reservation_id}


def test_two_ledger_instances_have_one_cross_store_action_owner(
    tmp_path: Path,
) -> None:
    theory, head, first = _setup(tmp_path)
    second = ActionCoordinationLedger(
        theory_store=theory,
        coordination_root=first.coordination_root,
    )
    schedule, wave_id = _schedule()
    action_id = _selected_action_ids(schedule, wave_id)[0]
    start = threading.Barrier(2)
    side_effects: list[str] = []
    side_effect_lock = threading.Lock()

    def compete(
        ledger: ActionCoordinationLedger,
        consumer_id: str,
    ) -> tuple[str, Any]:
        start.wait(timeout=5)

        def worker(_invocation):
            with side_effect_lock:
                side_effects.append(consumer_id)
            return ActionWorkerOutcome("completed")

        try:
            return (
                "won",
                execute_frozen_action_wave(
                    ledger=ledger,
                    schedule=schedule,
                    wave_id=wave_id,
                    theory_commit_reference=head.commit_ref,
                    theory_graph_reference=head.graph_ref,
                    consumer_id=consumer_id,
                    callbacks={action_id: worker},
                ),
            )
        except ActionReservationConflict as exc:
            return "conflict", exc

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = (
            pool.submit(compete, first, "consumer.first"),
            pool.submit(compete, second, "consumer.second"),
        )
        outcomes = [future.result(timeout=10) for future in futures]

    assert sorted(kind for kind, _value in outcomes) == ["conflict", "won"]
    assert len(side_effects) == 1
    winner = next(value for kind, value in outcomes if kind == "won")
    assert winner.terminal.status == "completed"
    assert first.current_generation() == second.current_generation() == 2


def test_record_ceiling_requests_rollover_before_another_callback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    monkeypatch.setattr(ledger_protocol, "MAX_LEDGER_RECORDS", 2)
    first_schedule, first_wave = _schedule()
    first_action_id = _selected_action_ids(first_schedule, first_wave)[0]
    first = execute_frozen_action_wave(
        ledger=ledger,
        schedule=first_schedule,
        wave_id=first_wave,
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        consumer_id="consumer.history.first",
        callbacks={
            first_action_id: lambda _invocation: ActionWorkerOutcome(
                "completed"
            )
        },
    )
    assert first.terminal.status == "completed"
    assert ledger.current_generation() == 2

    later_schedule, later_wave = _schedule(state_version=2)
    later_action_id = _selected_action_ids(later_schedule, later_wave)[0]
    later_callbacks: list[str] = []
    with pytest.raises(
        ActionLedgerRolloverRequired,
        match="automatic rollover is forbidden",
    ):
        execute_frozen_action_wave(
            ledger=ledger,
            schedule=later_schedule,
            wave_id=later_wave,
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            consumer_id="consumer.history.second",
            callbacks={
                later_action_id: lambda _invocation: (
                    later_callbacks.append("forbidden")
                    or ActionWorkerOutcome("completed")
                )
            },
        )
    assert later_callbacks == []
    assert ledger.current_generation() == 2
