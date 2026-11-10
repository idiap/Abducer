# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial one-action/one-attempt proof coordination tests."""

from __future__ import annotations

import copy
import datetime as dt
import os
import pickle
import runpy
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest

import agentic.discovery.theory_gate as theory_gate
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    ActionReservationConflict,
    ProofExecutionClaimConsumed,
    TheoryHeadBindingError,
)
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
)
from agentic.discovery.proof import (
    ProofPrelaunchCapability,
    _consume_proof_prelaunch_capability,
    build_postcommit_proof_handoff,
    claim_proof_execution_capability,
    issue_proof_prelaunch_capability,
    proof_prelaunch_capability_projection,
)
from agentic.state.discovery_transaction import CommitArtifact, InjectedFailure


def _canonical_proof_source(root: Path) -> dict[str, Any]:
    module = runpy.run_path(
        str(Path(__file__).parents[1] / "discovery" / "test_discovery_theory_gate.py")
    )
    fixture = module["_canonical_fixture"](
        root, formal_seed_mode="ready_exact"
    )
    authorization = module["_verify"](fixture)
    return {
        "fixture": fixture,
        "authorization": authorization,
        "handoff": build_postcommit_proof_handoff(authorization),
    }


@pytest.fixture(scope="module")
def proof_source(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    return _canonical_proof_source(tmp_path_factory.mktemp("proof-ledger-source"))


def _ledger(source: dict[str, Any], root: Path) -> ActionCoordinationLedger:
    return ActionCoordinationLedger(
        theory_store=source["fixture"]["store"],
        coordination_root=root,
    )


@pytest.mark.expensive
def test_proof_attempt_reservation_is_exact_idempotent_and_action_exclusive(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    ledger = _ledger(proof_source, tmp_path / "coordination")
    theory_generation = proof_source["fixture"]["store"].current_generation()
    first = ledger.reserve_proof_attempt(
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
        attempt_number=1,
    )
    second = ledger.reserve_proof_attempt(
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
        attempt_number=1,
    )
    assert first == second
    assert ledger.current_generation() == 1
    assert proof_source["fixture"]["store"].current_generation() == theory_generation
    record = first.record
    handoff = proof_source["handoff"]
    assert record["status"] == "proof_attempt_reserved"
    assert record["schedule_id"] == handoff["schedule_id"]
    assert record["action_id"] == handoff["scheduled_action_id"]
    assert record["action_digest"] == handoff["scheduled_action_digest"]
    assert record["handoff_id"] == handoff["handoff_id"]
    assert record["handoff_digest"] == handoff["content_digest"]
    assert record["formal_claim_authority_id"] == handoff[
        "formal_claim_authority_id"
    ]
    assert record["producer_receipt_id"] == handoff["producer_receipt_id"]
    assert record["proof_runtime_ref"] == f"proof-runtime/{record['attempt_id']}"
    assert str(tmp_path) not in str(record)

    with pytest.raises(ActionReservationConflict, match="already reserved"):
        ledger.reserve_proof_attempt(
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            attempt_number=2,
        )
    with pytest.raises(ContractError, match="live runtime-verified"):
        ledger.reserve_proof_attempt(
            theory_authorization=dict(proof_source["authorization"]),
            handoff=proof_source["handoff"],
        )


@pytest.mark.expensive
def test_competing_live_claims_have_one_durable_launch_winner(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    root = tmp_path / "coordination"
    first_ledger = _ledger(proof_source, root)
    reservation = first_ledger.reserve_proof_attempt(
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
    )
    second_ledger = _ledger(proof_source, root)
    capabilities = (
        issue_proof_prelaunch_capability(
            coordination_ledger=first_ledger,
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
        ),
        issue_proof_prelaunch_capability(
            coordination_ledger=second_ledger,
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
        ),
    )
    barrier = threading.Barrier(2)

    def compete(capability: ProofPrelaunchCapability) -> tuple[str, Any]:
        barrier.wait(timeout=10)
        try:
            return "won", _consume_proof_prelaunch_capability(capability)
        except ProofExecutionClaimConsumed as exc:
            return "consumed", exc

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(compete, capabilities))
    assert sorted(kind for kind, _value in outcomes) == ["consumed", "won"]
    winner = next(value for kind, value in outcomes if kind == "won")
    projection, _handoff, _reservation, claim, claim_reference = winner
    assert projection["capability_kind"] == (
        "one_shot_unclaimed_postcommit_proof_prelaunch"
    )
    assert projection["reservation_id"] == reservation.reservation_id
    assert projection["action_id"] == reservation.record["action_id"]
    assert projection["attempt_id"] == reservation.record["attempt_id"]
    assert projection["durable_claim_present_in_projection"] is False
    assert projection["projection_only"] is True
    assert projection["authoritative_for_execution"] is False
    assert projection["serialized_reconstruction_allowed"] is False
    assert claim["status"] == "proof_execution_claimed"
    assert claim["execution_claim_id"] == projection["execution_claim_id"]
    deadline = claim["deadline_revalidation"]
    evaluated_at = dt.datetime.fromisoformat(
        deadline["evaluated_at"].replace("Z", "+00:00")
    )
    consume_before = dt.datetime.fromisoformat(
        deadline["consume_before"].replace("Z", "+00:00")
    )
    assert evaluated_at <= consume_before
    assert deadline["clock_authority_digest"] == deadline[
        "clock_authority"
    ]["authority_digest"]
    assert deadline["live_capability_revalidated"] is True
    assert deadline["cross_store_atomicity_claimed"] is False
    assert claim_reference["generation"] == 2
    assert first_ledger.current_generation() == 2


@pytest.mark.expensive
def test_postrename_claim_failure_is_durably_consumed_and_never_reissued(
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
    with pytest.raises(InjectedFailure, match="after_commit_rename"):
        _consume_proof_prelaunch_capability(
            capability,
            failpoint="after_commit_rename",
        )
    with pytest.raises(ContractError, match="already spent"):
        _consume_proof_prelaunch_capability(capability)
    reopened = _ledger(proof_source, root)
    with pytest.raises(ProofExecutionClaimConsumed, match="already consumed"):
        issue_proof_prelaunch_capability(
            coordination_ledger=reopened,
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
        )
    assert reopened.current_generation() == 2


@pytest.mark.expensive
def test_theory_head_drift_blocks_prelaunch_claim_without_coordination_write(
    tmp_path: Path,
) -> None:
    source = _canonical_proof_source(tmp_path / "source")
    ledger = _ledger(source, tmp_path / "coordination")
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
    store = source["fixture"]["store"]
    next_state = copy.deepcopy(store.read_state(1))
    assert next_state is not None
    next_state["generation"] = 2
    store.commit(
        expected_generation=1,
        state=next_state,
        artifacts=(
            CommitArtifact(
                relative_path="branches/root/tests/proof-head-drift.json",
                content=b"{}\n",
                namespace=Namespace(
                    store.target_id,
                    store.run_id,
                    "root",
                    1,
                ),
            ),
        ),
        idempotency_key="proof-head-drift",
        request_digest=canonical_digest({"proof_head_drift": True}),
    )
    with pytest.raises(
        (ContractError, TheoryHeadBindingError),
        match="stale|current theory head|head changed",
    ):
        _consume_proof_prelaunch_capability(capability)
    with pytest.raises(ContractError, match="already spent"):
        _consume_proof_prelaunch_capability(capability)
    assert ledger.current_generation() == 1


@pytest.mark.expensive
def test_expiry_between_prelaunch_issuance_and_consumption_burns_without_claim(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger = _ledger(proof_source, tmp_path / "coordination")
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
    consume_before = dt.datetime.fromisoformat(
        proof_source["handoff"]["literature_consume_before"].replace(
            "Z", "+00:00"
        )
    )
    monkeypatch.setattr(
        theory_gate,
        "_system_utc_now",
        lambda: consume_before + dt.timedelta(microseconds=1),
    )
    with pytest.raises(ContractError, match="consume-before"):
        _consume_proof_prelaunch_capability(capability)
    with pytest.raises(ContractError, match="already spent"):
        _consume_proof_prelaunch_capability(capability)
    assert ledger.current_generation() == 1
    with pytest.raises(ContractError, match="unknown proof execution claim"):
        ledger.read_proof_execution_claim(
            reservation.record["execution_claim_id"]
        )


@pytest.mark.expensive
def test_prelaunch_capability_is_inert_noncopyable_nonserializable_and_one_shot(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    ledger = _ledger(proof_source, tmp_path / "coordination")
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
    projection = proof_prelaunch_capability_projection(capability)
    assert projection["content_digest"].startswith("sha256:")
    assert str(tmp_path) not in str(projection)
    assert projection["projection_phase"] == "before_durable_execution_claim"
    assert "execution_claim_digest" not in projection
    assert "execution_claim_commit_reference" not in projection
    assert ledger.current_generation() == 1
    with pytest.raises(ContractError, match="unknown proof execution claim"):
        ledger.read_proof_execution_claim(projection["execution_claim_id"])

    with pytest.raises(TypeError, match="cannot be copied"):
        copy.copy(capability)
    with pytest.raises(TypeError, match="cannot be deep-copied"):
        copy.deepcopy(capability)
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        with pytest.raises(TypeError, match="cannot be serialized"):
            pickle.dumps(capability, protocol=protocol)
    with pytest.raises(TypeError, match="issued only"):
        ProofPrelaunchCapability(
            projection,
            coordination_ledger=ledger,
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
            execution_claim_id=projection["execution_claim_id"],
        )
    with pytest.raises(ContractError, match="live sealed"):
        proof_prelaunch_capability_projection(projection)  # type: ignore[arg-type]
    with pytest.raises(ContractError, match="claim-before-capability"):
        claim_proof_execution_capability(
            coordination_ledger=ledger,
            theory_authorization=proof_source["authorization"],
            handoff=proof_source["handoff"],
            reservation_id=reservation.reservation_id,
        )

    first = _consume_proof_prelaunch_capability(capability)
    assert first[0] == projection
    assert first[3]["status"] == "proof_execution_claimed"
    assert ledger.current_generation() == 2
    with pytest.raises(ContractError, match="already spent"):
        _consume_proof_prelaunch_capability(capability)


@pytest.mark.expensive
@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires POSIX fork")
def test_forked_copies_contend_on_one_durable_prelaunch_claim(
    proof_source: dict[str, Any],
    tmp_path: Path,
) -> None:
    ledger = _ledger(proof_source, tmp_path / "coordination")
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
    read_fd, write_fd = os.pipe()
    child_ids: list[int] = []
    for _index in range(2):
        child_id = os.fork()
        if child_id == 0:
            os.close(read_fd)
            try:
                _consume_proof_prelaunch_capability(capability)
                outcome = b"won\n"
            except ProofExecutionClaimConsumed:
                outcome = b"consumed\n"
            except BaseException as exc:  # pragma: no cover - diagnostic path
                outcome = f"error:{type(exc).__name__}:{exc}\n".encode("utf-8")
            try:
                os.write(write_fd, outcome)
            finally:
                os.close(write_fd)
            os._exit(0)
        child_ids.append(child_id)
    os.close(write_fd)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(read_fd, 4096)
        if not chunk:
            break
        chunks.append(chunk)
    os.close(read_fd)
    for child_id in child_ids:
        _pid, status = os.waitpid(child_id, 0)
        assert os.waitstatus_to_exitcode(status) == 0
    outcomes = b"".join(chunks).decode("utf-8").splitlines()
    assert sorted(outcomes) == ["consumed", "won"]
    assert ledger.current_generation() == 2
    claim = ledger.read_proof_execution_claim(
        reservation.record["execution_claim_id"]
    )
    assert claim.record["status"] == "proof_execution_claimed"
    with pytest.raises(ProofExecutionClaimConsumed, match="already consumed"):
        _consume_proof_prelaunch_capability(capability)
