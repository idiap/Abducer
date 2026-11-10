# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Loading and validation-linking helpers for abductive mechanism dossiers.

A mechanism dossier moves a conceptual crisis through four provisional stages:
abduction -> requirements -> counterfactual critique -> TODO backlog. None of these
stages is an accepted repair edge; `mechanism_validation_packet` turns the requirements
(optionally enriched by a critique and a TODO packet) into the same `ValidationPacket`
shape used for transformation candidates, so mechanism work can be tracked under the
same hard-gate discipline before it is ever proposed as a graph edge.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hegelian_solver.ids import stable_id
from hegelian_solver.io import read_structured
from hegelian_solver.schemas import (
    MechanismCounterfactualCritique,
    MechanismDossier,
    MechanismRequirementsPacket,
    MechanismTodoPacket,
    Obligation,
    ValidationPacket,
)

NON_PASSING_RESULTS = {"unknown", "needs_evidence"}


def load_mechanism_dossier(payload: dict[str, Any]) -> MechanismDossier:
    return MechanismDossier.model_validate(payload)


def load_mechanism_dossiers(path: str | Path) -> list[MechanismDossier]:
    """Load every mechanism dossier from a `mechanism_examples`-shaped file."""

    payload = read_structured(path)
    items = payload.get("mechanism_examples", payload) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("mechanism dossier file must contain a `mechanism_examples` list")
    return [load_mechanism_dossier(item) for item in items]


def _requirement_status(
    requirement_id: str, critique: MechanismCounterfactualCritique | None
) -> tuple[str, str | None]:
    if critique is None:
        return "planned", "not yet counterfactually tested"
    affecting = [
        test
        for test in critique.counterfactual_tests
        if requirement_id in test.affected_requirements
    ]
    if any(test.result == "fail" for test in affecting):
        test = next(test for test in affecting if test.result == "fail")
        return "failed", test.failure_signal
    if any(test.result in NON_PASSING_RESULTS for test in affecting):
        return "partial", "counterfactual test result is " + next(
            test.result for test in affecting if test.result in NON_PASSING_RESULTS
        )
    if affecting:
        return "passed", None
    return "planned", "not yet counterfactually tested"


def mechanism_validation_packet(
    requirements: MechanismRequirementsPacket,
    critique: MechanismCounterfactualCritique | None = None,
    todos: MechanismTodoPacket | None = None,
) -> ValidationPacket:
    """Build a `ValidationPacket` for a mechanism's requirements and open TODOs.

    Requirements marked `necessary` or `jointly_sufficient` are hard gates; their
    status comes from any counterfactual test that names them, defaulting to
    `planned` (a non-passing status, per the solver's obligation discipline) when
    no test has touched them yet. TODOs that `blocks_candidate_acceptance` are
    appended as additional hard gates until they are resolved into requirements.
    """

    candidate_id = f"mechanism::{requirements.mechanism_name}"
    obligations: list[Obligation] = []
    hard_gate_failures: list[str] = []

    for requirement in requirements.requirements:
        status, blocker = _requirement_status(requirement.id, critique)
        obligations.append(
            Obligation(
                id=stable_id("obligation", {"mechanism": candidate_id, "requirement": requirement.id}),
                kind=requirement.kind,
                statement=requirement.statement,
                method=requirement.validation_method,
                status=status,  # type: ignore[arg-type]
                evidence=[requirement.id] if status == "passed" else [],
                blocker=blocker,
            )
        )
        is_hard_gate = requirement.necessity_status in {"necessary", "jointly_sufficient"}
        if is_hard_gate and status != "passed":
            hard_gate_failures.append(f"{requirement.id}: {blocker or status}")

    if todos is not None:
        for group in todos.todo_groups:
            for todo in group.todos:
                if not todo.blocks_candidate_acceptance:
                    continue
                obligations.append(
                    Obligation(
                        id=stable_id("obligation", {"mechanism": candidate_id, "todo": todo.id}),
                        kind="mechanism_todo",
                        statement=todo.task,
                        method="review",
                        status="planned",
                        evidence=[],
                        blocker=todo.why_needed,
                    )
                )
                hard_gate_failures.append(f"{todo.id}: blocked pending {todo.acceptance_criterion}")

    summary = "all mechanism hard gates passed" if not hard_gate_failures else "mechanism hard gates open"
    return ValidationPacket(
        candidate_id=candidate_id,
        obligations=obligations,
        hard_gate_failures=hard_gate_failures,
        summary=summary,
    )


def mechanism_validation_packet_from_dossier(dossier: MechanismDossier) -> ValidationPacket:
    if dossier.mechanism_requirements_packet is None:
        raise ValueError(f"dossier `{dossier.id}` has no mechanism_requirements_packet to validate")
    return mechanism_validation_packet(
        dossier.mechanism_requirements_packet,
        dossier.mechanism_counterfactual_critique,
        dossier.mechanism_todo_packet,
    )
