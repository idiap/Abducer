# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Public in-process boundary for current proof-v3 execution and intake.

Proof launch authority is an opaque, one-shot ``ProofPrelaunchCapability``.
It cannot be reconstructed from JSON, a path, a command line, or a worker
request, so this facade deliberately exposes no serializable CLI.  The
canonical caller obtains that live capability from the postcommit action
ledger, calls :func:`execute_proof_v3`, and later calls
:func:`consume_proof_result_v3` with the exact reservation identity.

Execution returns only after the terminal bundle is durably finalized.
Consumption returns only after the distinct N+1 theory-side reconciliation
outbox is in the active verified commit prefix and its one-shot coordination
record is durable.  Neither operation grants checker soundness, theorem truth,
theory selection, same-cycle mutation, or physics authority.
"""

from __future__ import annotations

import dataclasses

from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
    CoordinationLedgerResult,
)
from agentic.discovery.contracts import ContractError
from agentic.discovery.proof import (
    ProofPrelaunchCapability,
    build_postcommit_proof_handoff,
    issue_proof_prelaunch_capability,
)
from agentic.discovery.proof_execution import (
    ProofExecutionTerminalResult,
    _execute_current_proof_v3,
)
from agentic.discovery.theory_gate import VerifiedTheoryAuthorization


@dataclasses.dataclass(frozen=True, slots=True)
class ProofV3ActionResult:
    """Durable production outcome for one exact committed prove action."""

    reservation: CoordinationLedgerResult
    terminal: CoordinationLedgerResult
    intake: CoordinationLedgerResult
    launched_by_this_call: bool


def execute_proof_v3(
    capability: ProofPrelaunchCapability,
) -> ProofExecutionTerminalResult:
    """Consume one live capability and return its durable terminal bundle.

    No command, dependency path, retry flag, handoff projection, or caller
    callback is accepted here.  The proof executor derives and reopens every
    such input from the capability's committed reservation before the sole
    governed spawn.
    """

    if type(capability) is not ProofPrelaunchCapability:
        raise ContractError(
            "proof-v3 execution requires one exact live prelaunch capability"
        )
    return _execute_current_proof_v3(capability)


def reconcile_committed_proof_action_v3(
    *,
    ledger: ActionCoordinationLedger,
    reservation_id: str,
) -> ProofV3ActionResult:
    """Finish a previously terminalized action without reissuing launch.

    This is the only retry/recovery-facing production seam. It reopens the
    immutable reservation and terminal bundle, then either consumes the exact
    N+1 outbox or returns the durable typed supersession of a lost N+1 slot.
    """

    if type(ledger) is not ActionCoordinationLedger:
        raise ContractError(
            "proof-v3 reconciliation requires an exact coordination ledger"
        )
    reservation = ledger.read_proof_attempt(reservation_id)
    terminal = ledger.read_proof_terminal_bundle(reservation_id)
    intake = ledger.consume_proof_result_intake(reservation_id)
    return ProofV3ActionResult(
        reservation=reservation,
        terminal=terminal,
        intake=intake,
        launched_by_this_call=False,
    )


def run_committed_proof_action_v3(
    *,
    ledger: ActionCoordinationLedger,
    theory_authorization: VerifiedTheoryAuthorization,
) -> ProofV3ActionResult:
    """Run the sole production proof route from committed authority.

    Handoff, prove action, attempt-one identity, runtime, dependency bytes,
    command, durable claim, and checker launch are all derived internally.
    The caller cannot supply or override any of them. A crash after the claim
    must use :func:`reconcile_committed_proof_action_v3`; this function never
    respawns a spent claim.
    """

    if type(ledger) is not ActionCoordinationLedger:
        raise ContractError(
            "proof-v3 production execution requires an exact coordination ledger"
        )
    if not isinstance(theory_authorization, VerifiedTheoryAuthorization):
        raise ContractError(
            "proof-v3 production execution requires committed theory authority"
        )
    handoff = build_postcommit_proof_handoff(theory_authorization)
    reservation = ledger.reserve_proof_attempt(
        theory_authorization=theory_authorization,
        handoff=handoff,
    )
    capability = issue_proof_prelaunch_capability(
        coordination_ledger=ledger,
        theory_authorization=theory_authorization,
        handoff=handoff,
        reservation_id=reservation.reservation_id,
    )
    executed = execute_proof_v3(capability)
    if (
        executed.durably_finalized is not True
        or executed.durable_bundle is None
        or executed.durable_bundle.get("reservation_id")
        != reservation.reservation_id
    ):
        raise ContractError(
            "proof-v3 executor returned without its exact durable terminal"
        )
    terminal = ledger.read_proof_terminal_bundle(
        reservation.reservation_id
    )
    intake = ledger.consume_proof_result_intake(
        reservation.reservation_id
    )
    return ProofV3ActionResult(
        reservation=reservation,
        terminal=terminal,
        intake=intake,
        launched_by_this_call=True,
    )


def consume_proof_result_v3(
    *,
    ledger: ActionCoordinationLedger,
    reservation_id: str,
) -> CoordinationLedgerResult:
    """Recover and consume one terminal result through its N+1 outbox.

    Exact retries reopen the existing claim, theory descendant, outbox, and
    consumption. A source-theory fork after the claim returns a durable typed
    supersession; later verified descendants are allowed because either the
    exact N+1 outbox or the exact N+1 occupying commit remains authenticated
    in their active prefix.
    """

    if type(ledger) is not ActionCoordinationLedger:
        raise ContractError(
            "proof-v3 result intake requires an exact coordination ledger"
        )
    return ledger.consume_proof_result_intake(reservation_id)


def reopen_consumed_proof_result_v3(
    *,
    ledger: ActionCoordinationLedger,
    reservation_id: str,
) -> CoordinationLedgerResult:
    """Reopen one consumed result and revalidate its theory-side outbox."""

    if type(ledger) is not ActionCoordinationLedger:
        raise ContractError(
            "proof-v3 result reopening requires an exact coordination ledger"
        )
    return ledger.read_proof_result_intake_consumption(reservation_id)


__all__ = [
    "ProofV3ActionResult",
    "consume_proof_result_v3",
    "execute_proof_v3",
    "reconcile_committed_proof_action_v3",
    "reopen_consumed_proof_result_v3",
    "run_committed_proof_action_v3",
]
