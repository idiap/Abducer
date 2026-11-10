# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for the independent theory-bound coordination ledger."""

from __future__ import annotations

import copy
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Mapping, Sequence

import pytest

from agentic.discovery import action_coordination_ledger as coordination
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    ActionReservationConflict,
    CoordinationStoreBoundaryError,
    ReservationTerminalConflict,
    TheoryHeadBindingError,
)
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
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
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    InjectedFailure,
    StateCorruptionError,
)


TARGET_ID = "coordination-ledger-target"
RUN_ID = "coordination-ledger-run"
PROGRAMME_ID = "coordination-ledger-programme"
BRANCH_ID = "theory"
SCHEDULE_ID = "schedule.theory-actions"
SCHEDULE_DIGEST = canonical_digest({"schedule": SCHEDULE_ID, "version": 1})


def _theory_store(root: Path) -> DiscoveryTransactionStore:
    return DiscoveryTransactionStore(root, target_id=TARGET_ID, run_id=RUN_ID)


def _object(generation: int, name: str) -> PreparedContentObject:
    return prepare_content_object(
        object_kind=(
            "world_projection_index_v3"
            if name == "theory-root"
            else "world_matrix_aggregation_root_v3"
        ),
        value={
            "fixture_kind": name,
            "generation": generation,
            "authority_boundary": "storage fixture only; no physics authority",
        },
        path=(
            f"branches/{BRANCH_ID}/content-graphs/g{generation}/objects/{name}.json"
        ),
    )


def _publish_theory_head(
    store: DiscoveryTransactionStore,
    generation: int,
    *,
    root_names: Sequence[str] = ("theory-root", "support-certificate"),
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
    graph_path = f"branches/{BRANCH_ID}/content-graphs/g{generation}/graph.json"
    prepared = prepare_content_graph_transaction(
        expected_generation=generation - 1,
        state={
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": generation,
            "programme_id": PROGRAMME_ID,
            "fixture_generation": generation,
        },
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, generation - 1),
        graph_artifact_path=graph_path,
        graph=graph,
        local_objects=objects,
    )
    return commit_content_graph_transaction(store=store, transaction=prepared)


def _setup(
    tmp_path: Path,
) -> tuple[DiscoveryTransactionStore, ContentGraphTransactionResult, ActionCoordinationLedger]:
    theory = _theory_store(tmp_path / "theory-store")
    head = _publish_theory_head(theory, 1)
    ledger = ActionCoordinationLedger(
        theory_store=theory,
        coordination_root=tmp_path / "coordination-store",
    )
    return theory, head, ledger


def _reserve(
    ledger: ActionCoordinationLedger,
    head: ContentGraphTransactionResult,
    *,
    consumer_id: str = "consumer.primary",
    action_ids: Sequence[str] = ("action.alpha", "action.beta"),
    support: bool = True,
    failpoint: str | None = None,
):
    return ledger.reserve(
        theory_commit_reference=head.commit_ref,
        theory_graph_reference=head.graph_ref,
        n_plus_7_support_root_references=(head.root_refs[-1],) if support else (),
        schedule_id=SCHEDULE_ID,
        schedule_digest=SCHEDULE_DIGEST,
        action_ids=action_ids,
        consumer_id=consumer_id,
        failpoint=failpoint,
    )


def test_reservation_is_separate_portable_and_exactly_theory_bound(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    theory_generation = theory.current_generation()

    result = _reserve(ledger, head)
    record = result.record

    assert theory.current_generation() == theory_generation == 1
    assert ledger.current_generation() == 1
    assert record["status"] == "reserved"
    assert record["schedule_id"] == SCHEDULE_ID
    assert record["schedule_digest"] == SCHEDULE_DIGEST
    assert record["action_ids"] == ["action.alpha", "action.beta"]
    assert record["theory_binding"]["commit_reference"] == head.commit_ref
    assert record["theory_binding"]["graph_reference"] == head.graph_ref
    assert record["theory_binding"]["n_plus_7_support_root_references"] == [
        head.root_refs[-1]
    ]
    assert record["theory_binding"]["observed_head"]["generation"] == 1
    assert record["authority_boundary"] == {
        "boundary_kind": "coordination_only_non_theory_non_selection",
        "may_mutate_theory_store": False,
        "may_select_theory": False,
        "may_promote_scientific_claims": False,
        "may_claim_proof_or_experiment_authority": False,
        "cross_store_atomicity_claimed": False,
        "head_check_scope": "read_only_point_in_time_observation",
    }
    serialized = canonical_json(result.as_dict()).decode("utf-8")
    assert str(tmp_path) not in serialized
    assert "commit_path" not in serialized


def test_finalize_rechecks_unchanged_head_and_is_exactly_idempotent(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, head)
    evidence = canonical_digest({"terminal": "evidence"})

    first = ledger.finalize(
        reservation.reservation_id,
        terminal_status="completed",
        terminal_evidence_digests=[evidence],
    )
    second = ledger.finalize(
        reservation.reservation_id,
        terminal_status="completed",
        terminal_evidence_digests=[evidence],
    )

    assert first == second == ledger.read_terminal(reservation.reservation_id)
    assert first.status == "completed"
    assert first.record["requested_terminal_status"] == "completed"
    assert first.record["theory_head_recheck"]["match"] is True
    assert first.record["theory_head_recheck"]["disposition_reason"] == "head_unchanged"
    assert ledger.current_generation() == 2
    assert theory.current_generation() == 1
    assert len(list((ledger.coordination_run_root / "commits").iterdir())) == 2


def test_finalize_persists_typed_rebase_required_on_theory_head_drift(
    tmp_path: Path,
) -> None:
    theory, first_head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, first_head)
    second_head = _publish_theory_head(theory, 2, root_names=("theory-root",))

    terminal = ledger.finalize(
        reservation.reservation_id,
        terminal_status="completed",
    )

    assert terminal.status == "rebase_required"
    assert terminal.record["requested_terminal_status"] == "completed"
    recheck = terminal.record["theory_head_recheck"]
    assert recheck["match"] is False
    assert recheck["disposition_reason"] == "theory_head_drift"
    assert recheck["expected_head"]["generation"] == 1
    assert recheck["observed_head"]["generation"] == 2
    assert recheck["observed_head"]["commit_id"] == second_head.commit_id
    assert theory.current_generation() == 2
    assert ledger.current_generation() == 2


@pytest.mark.parametrize(
    ("failpoint", "visible_after_recovery"),
    [
        ("after_artifact_write:1", 0),
        ("after_commit_rename", 1),
    ],
)
def test_named_failpoint_retry_is_exactly_once(
    tmp_path: Path,
    failpoint: str,
    visible_after_recovery: int,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    with pytest.raises(InjectedFailure, match=failpoint):
        _reserve(ledger, head, failpoint=failpoint)

    assert ledger.current_generation() == visible_after_recovery
    first = _reserve(ledger, head)
    second = _reserve(ledger, head)
    assert first == second
    assert ledger.current_generation() == 1
    assert len(list((ledger.coordination_run_root / "commits").iterdir())) == 1


def test_failpoint_callback_is_rejected_without_any_store_mutation(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    with pytest.raises(ContractError, match="not a callback"):
        ledger.reserve(
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            schedule_id=SCHEDULE_ID,
            schedule_digest=SCHEDULE_DIGEST,
            action_ids=["action.alpha"],
            consumer_id="consumer.primary",
            failpoint=lambda _name: None,  # type: ignore[arg-type]
        )
    assert ledger.current_generation() == 0
    assert theory.current_generation() == 1


def test_concurrent_exact_reservation_collapses_to_one_commit(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    barrier = threading.Barrier(2)

    def reserve_exact() -> Any:
        barrier.wait(timeout=5)
        return _reserve(ledger, head)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _index: reserve_exact(), range(2)))

    assert results[0] == results[1]
    assert ledger.current_generation() == 1
    assert len(list((ledger.coordination_run_root / "commits").iterdir())) == 1


def test_concurrent_competing_consumers_have_one_durable_action_owner(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    barrier = threading.Barrier(2)

    def compete(consumer_id: str) -> tuple[str, Any]:
        barrier.wait(timeout=5)
        try:
            return "won", _reserve(
                ledger,
                head,
                consumer_id=consumer_id,
                action_ids=("action.shared",),
            )
        except ActionReservationConflict as exc:
            return "conflict", exc

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(compete, ("consumer.one", "consumer.two")))

    assert sorted(kind for kind, _value in outcomes) == ["conflict", "won"]
    winner = next(value for kind, value in outcomes if kind == "won")
    assert winner.record["action_ids"] == ["action.shared"]
    assert ledger.current_generation() == 1


def test_relocation_reopens_byte_identical_reservation_and_can_finalize(
    tmp_path: Path,
) -> None:
    theory_root = tmp_path / "theory-source"
    coordination_root = tmp_path / "coordination-source"
    theory = _theory_store(theory_root)
    head = _publish_theory_head(theory, 1)
    ledger = ActionCoordinationLedger(
        theory_store=theory, coordination_root=coordination_root
    )
    reservation = _reserve(ledger, head)

    relocated_theory_root = tmp_path / "theory-relocated"
    relocated_coordination_root = tmp_path / "coordination-relocated"
    shutil.copytree(theory_root, relocated_theory_root)
    shutil.copytree(coordination_root, relocated_coordination_root)
    relocated_theory = _theory_store(relocated_theory_root)
    relocated = ActionCoordinationLedger(
        theory_store=relocated_theory,
        coordination_root=relocated_coordination_root,
    )

    reopened = relocated.read_reservation(reservation.reservation_id)
    assert reopened == reservation
    assert canonical_json(reopened.as_dict()) == canonical_json(reservation.as_dict())
    terminal = relocated.finalize(
        reservation.reservation_id, terminal_status="released"
    )
    assert terminal.status == "released"
    assert terminal.record["theory_head_recheck"]["match"] is True
    assert relocated_theory.current_generation() == 1


def test_tampered_committed_record_fails_closed(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, head)
    commit_directory = next((ledger.coordination_run_root / "commits").iterdir())
    record_path = (
        commit_directory
        / "artifacts"
        / reservation.ledger_commit_reference["record_artifact"]["path"]
    )
    record_path.write_bytes(b"{}")

    with pytest.raises(StateCorruptionError):
        ledger.read_reservation(reservation.reservation_id)


def test_returned_records_and_commit_references_are_defensive(
    tmp_path: Path,
) -> None:
    _theory, head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, head)
    expected = reservation.as_dict()

    record = reservation.record
    commit_reference = reservation.ledger_commit_reference
    projection = reservation.as_dict()
    record["action_ids"].clear()
    record["theory_binding"]["commit_reference"]["commit_id"] = "commit.forged"
    commit_reference["record_artifact"]["path"] = "branches/forged.json"
    projection["record"]["status"] = "completed"

    assert reservation.as_dict() == expected
    assert ledger.read_reservation(reservation.reservation_id) == reservation


def test_wrong_head_reference_and_nonroot_support_fail_before_coordination_write(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    forged_commit = copy.deepcopy(head.commit_ref)
    forged_commit["commit_id"] = "commit.forged"
    forged_commit["reference_digest"] = canonical_digest(
        {key: value for key, value in forged_commit.items() if key != "reference_digest"}
    )
    with pytest.raises(TheoryHeadBindingError):
        ledger.reserve(
            theory_commit_reference=forged_commit,
            theory_graph_reference=head.graph_ref,
            schedule_id=SCHEDULE_ID,
            schedule_digest=SCHEDULE_DIGEST,
            action_ids=["action.alpha"],
            consumer_id="consumer.primary",
        )

    forged_support = copy.deepcopy(head.root_refs[-1])
    forged_support["object_id"] = "world-content-object-v1.forged"
    with pytest.raises(TheoryHeadBindingError, match="not an exact root"):
        ledger.reserve(
            theory_commit_reference=head.commit_ref,
            theory_graph_reference=head.graph_ref,
            n_plus_7_support_root_references=[forged_support],
            schedule_id=SCHEDULE_ID,
            schedule_digest=SCHEDULE_DIGEST,
            action_ids=["action.alpha"],
            consumer_id="consumer.primary",
        )
    assert ledger.current_generation() == 0
    assert theory.current_generation() == 1


def test_coordination_root_must_be_physically_disjoint_from_theory_root(
    tmp_path: Path,
) -> None:
    theory_root = tmp_path / "theory"
    theory = _theory_store(theory_root)
    _publish_theory_head(theory, 1)

    with pytest.raises(CoordinationStoreBoundaryError, match="disjoint"):
        ActionCoordinationLedger(
            theory_store=theory,
            coordination_root=theory_root,
        )
    with pytest.raises(CoordinationStoreBoundaryError, match="disjoint"):
        ActionCoordinationLedger(
            theory_store=theory,
            coordination_root=theory_root / "nested-coordination",
        )
    assert theory.current_generation() == 1


def test_a_second_terminal_intent_conflicts_without_mutating_either_store(
    tmp_path: Path,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, head)
    first = ledger.finalize(reservation.reservation_id, terminal_status="failed")

    with pytest.raises(ReservationTerminalConflict, match="different terminal"):
        ledger.finalize(reservation.reservation_id, terminal_status="completed")
    assert ledger.current_generation() == 2
    assert theory.current_generation() == 1
    assert ledger.read_terminal(reservation.reservation_id) == first


def test_fixed_action_support_record_and_ledger_ceilings_are_enforced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theory, head, ledger = _setup(tmp_path)

    monkeypatch.setattr(coordination, "MAX_ACTIONS_PER_RESERVATION", 1)
    with pytest.raises(ContractError, match="action_ids exceeds"):
        _reserve(ledger, head, action_ids=("action.one", "action.two"))
    monkeypatch.setattr(coordination, "MAX_ACTIONS_PER_RESERVATION", 128)

    monkeypatch.setattr(coordination, "MAX_SUPPORT_ROOT_REFERENCES", 0)
    with pytest.raises(ContractError, match="support references exceed"):
        _reserve(ledger, head)
    monkeypatch.setattr(coordination, "MAX_SUPPORT_ROOT_REFERENCES", 16)

    monkeypatch.setattr(coordination, "MAX_RECORD_BYTES", 1)
    with pytest.raises(ContractError, match="record-byte ceiling"):
        _reserve(ledger, head, support=False)
    assert ledger.current_generation() == 0
    assert theory.current_generation() == 1

    monkeypatch.setattr(coordination, "MAX_RECORD_BYTES", 256 * 1024)
    monkeypatch.setattr(coordination, "MAX_LEDGER_RECORDS", 1)
    reservation = _reserve(ledger, head, support=False)
    with pytest.raises(ContractError, match="record ceiling"):
        ledger.finalize(reservation.reservation_id, terminal_status="released")
    assert ledger.current_generation() == 1


def test_fixed_terminal_evidence_ceiling_and_unknown_failpoint_are_enforced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theory, head, ledger = _setup(tmp_path)
    reservation = _reserve(ledger, head)
    monkeypatch.setattr(coordination, "MAX_TERMINAL_EVIDENCE_DIGESTS", 1)
    with pytest.raises(ContractError, match="evidence_digests exceeds"):
        ledger.finalize(
            reservation.reservation_id,
            terminal_status="completed",
            terminal_evidence_digests=[
                canonical_digest("one"),
                canonical_digest("two"),
            ],
        )
    with pytest.raises(ContractError, match="unknown coordination failpoint"):
        ledger.finalize(
            reservation.reservation_id,
            terminal_status="completed",
            failpoint="after_unregistered_boundary",
        )
    assert ledger.current_generation() == 1
    assert theory.current_generation() == 1
