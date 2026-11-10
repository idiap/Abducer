# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Crash-boundary matrix for the one-shot proof prelaunch capability.

The capability is process-local and must become spent after every consumption
attempt.  The durable coordination transaction is the recovery authority:
crashes before commit publication leave the reservation unclaimed, whereas
crashes at or after publication preserve exactly one claim and never authorize
another launch.  These tests exercise both halves of that boundary separately
from the broader proof-coordination adversarial suite.
"""

from __future__ import annotations

import runpy
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    CoordinationLedgerResult,
    ProofExecutionClaimConsumed,
)
from agentic.discovery.contracts import ContractError
from agentic.discovery.proof import (
    ProofPrelaunchCapability,
    _consume_proof_prelaunch_capability,
    issue_proof_prelaunch_capability,
)
from agentic.state.discovery_transaction import InjectedFailure


# Reuse the canonical current-theory/proof fixture rather than constructing a
# second, subtly different authority chain for crash-only tests.
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


@pytest.fixture(scope="module")
def proof_source(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    """Build one canonical live source shared by the isolated crash matrix."""

    return _canonical_proof_source(
        tmp_path_factory.mktemp("proof-prelaunch-crash-source")
    )


def _reserve_with_capabilities(
    source: dict[str, Any],
    root: Path,
    *,
    count: int,
) -> tuple[
    ActionCoordinationLedger,
    CoordinationLedgerResult,
    tuple[ProofPrelaunchCapability, ...],
]:
    ledger = _ledger(source, root)
    reservation = ledger.reserve_proof_attempt(
        theory_authorization=source["authorization"],
        handoff=source["handoff"],
    )
    capabilities = tuple(
        issue_proof_prelaunch_capability(
            coordination_ledger=ledger,
            theory_authorization=source["authorization"],
            handoff=source["handoff"],
            reservation_id=reservation.reservation_id,
        )
        for _index in range(count)
    )
    return ledger, reservation, capabilities


def _assert_capability_spent(capability: ProofPrelaunchCapability) -> None:
    """Observe the irreversible local state through the public failure mode."""

    with pytest.raises(ContractError, match="already spent"):
        _consume_proof_prelaunch_capability(capability)


def _assert_only_durable_claim(
    ledger: ActionCoordinationLedger,
    claim_id: str,
) -> CoordinationLedgerResult:
    """Reopen one exact claim and prove no second claim generation appeared."""

    generation, state = ledger._load_state()
    assert generation == 2
    assert set(state["proof_execution_claims"]) == {claim_id}
    claim = ledger.read_proof_execution_claim(claim_id)
    assert claim.record["execution_claim_id"] == claim_id
    assert claim.record["status"] == "proof_execution_claimed"
    return claim


def _assert_new_issuance_rejected(
    source: dict[str, Any],
    root: Path,
    reservation_id: str,
) -> None:
    """Check independent ledger instances cannot respawn claim authority."""

    for candidate_ledger in (_ledger(source, root), _ledger(source, root)):
        with pytest.raises(
            ProofExecutionClaimConsumed,
            match="already consumed",
        ):
            issue_proof_prelaunch_capability(
                coordination_ledger=candidate_ledger,
                theory_authorization=source["authorization"],
                handoff=source["handoff"],
                reservation_id=reservation_id,
            )
        assert candidate_ledger.current_generation() == 2


@pytest.mark.expensive
@pytest.mark.parametrize("failpoint", _EARLY_FAILPOINTS)
def test_early_claim_crash_spends_attempt_but_recovery_allows_new_winner(
    proof_source: dict[str, Any],
    tmp_path: Path,
    failpoint: str,
) -> None:
    """Prepublication crashes recover the unclaimed reservation, never the cap."""

    root = tmp_path / "coordination"
    _ledger_before_crash, reservation, capabilities = _reserve_with_capabilities(
        proof_source,
        root,
        count=1,
    )
    attempted = capabilities[0]
    claim_id = str(reservation.record["execution_claim_id"])

    with pytest.raises(InjectedFailure, match=failpoint):
        _consume_proof_prelaunch_capability(
            attempted,
            failpoint=failpoint,
        )
    _assert_capability_spent(attempted)

    recovered = _ledger(proof_source, root)
    generation, state = recovered._load_state()
    assert generation == 1
    assert state["proof_execution_claims"] == {}
    with pytest.raises(ContractError, match="unknown proof execution claim"):
        recovered.read_proof_execution_claim(claim_id)

    replacement = issue_proof_prelaunch_capability(
        coordination_ledger=recovered,
        theory_authorization=proof_source["authorization"],
        handoff=proof_source["handoff"],
        reservation_id=reservation.reservation_id,
    )
    consumed = _consume_proof_prelaunch_capability(replacement)
    assert consumed[3]["execution_claim_id"] == claim_id
    durable = _assert_only_durable_claim(recovered, claim_id)
    assert durable.record == consumed[3]


@pytest.mark.expensive
@pytest.mark.parametrize("failpoint", _LATE_FAILPOINTS)
def test_late_claim_crash_recovers_one_claim_and_every_capability_rejects(
    proof_source: dict[str, Any],
    tmp_path: Path,
    failpoint: str,
) -> None:
    """Postpublication crashes preserve the winner but never revive its object."""

    root = tmp_path / "coordination"
    _ledger_before_crash, reservation, capabilities = _reserve_with_capabilities(
        proof_source,
        root,
        count=2,
    )
    attempted, preissued_contender = capabilities
    claim_id = str(reservation.record["execution_claim_id"])

    with pytest.raises(InjectedFailure, match=failpoint):
        _consume_proof_prelaunch_capability(
            attempted,
            failpoint=failpoint,
        )
    _assert_capability_spent(attempted)

    recovered = _ledger(proof_source, root)
    _assert_only_durable_claim(recovered, claim_id)
    with pytest.raises(
        ProofExecutionClaimConsumed,
        match="already consumed",
    ):
        _consume_proof_prelaunch_capability(preissued_contender)
    _assert_capability_spent(preissued_contender)
    _assert_new_issuance_rejected(
        proof_source,
        root,
        reservation.reservation_id,
    )
    _assert_only_durable_claim(recovered, claim_id)


@pytest.mark.expensive
def test_failure_after_verified_result_reopen_keeps_claim_and_blocks_new_caps(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A caller-side crash after verified reopening cannot erase the committed CAS."""

    root = tmp_path / "coordination"
    ledger, reservation, capabilities = _reserve_with_capabilities(
        proof_source,
        root,
        count=2,
    )
    attempted, preissued_contender = capabilities
    claim_id = str(reservation.record["execution_claim_id"])
    original = ActionCoordinationLedger._result_for_record
    reopened_claims: list[str] = []

    def fail_once_after_result_reopen(
        self: ActionCoordinationLedger,
        record: Mapping[str, Any],
    ) -> CoordinationLedgerResult:
        result = original(self, record)
        if record.get("record_kind") == "proof_execution_claim" and not reopened_claims:
            assert result.record["execution_claim_id"] == claim_id
            assert result.ledger_generation == 2
            reopened_claims.append(claim_id)
            raise InjectedFailure("after_result_reopen")
        return result

    monkeypatch.setattr(
        ActionCoordinationLedger,
        "_result_for_record",
        fail_once_after_result_reopen,
    )
    with pytest.raises(InjectedFailure, match="after_result_reopen"):
        _consume_proof_prelaunch_capability(attempted)
    assert reopened_claims == [claim_id]
    _assert_capability_spent(attempted)

    recovered = _ledger(proof_source, root)
    _assert_only_durable_claim(recovered, claim_id)
    with pytest.raises(
        ProofExecutionClaimConsumed,
        match="already consumed",
    ):
        _consume_proof_prelaunch_capability(preissued_contender)
    _assert_capability_spent(preissued_contender)
    _assert_new_issuance_rejected(
        proof_source,
        root,
        reservation.reservation_id,
    )
    _assert_only_durable_claim(recovered, claim_id)
