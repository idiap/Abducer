# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validation packet generation.

This is where every candidate's `expected_obligations` (set in `operators/library.py`)
actually get checked. There is no proof engine, SMT solver, or benchmark runner wired up
yet — `_status_for` is a deterministic stand-in that mostly checks "is the expected field
present on the target concept" and otherwise returns `partial`/`planned`. `planned` and
`unknown` are always treated as non-passing (Phase 8's rule), so a candidate can't be
silently accepted just because nothing actively failed.

NOTE: `CORE_REQUIRED` plus the `{"regime", "measurement", "risk"}` set are hardcoded here as
the hard-gate kinds; `DomainProfile.validation_gates` (declared per-domain in `domain.py`)
is *not* read by this module, so gates like physics' `anti_overfit` or LM's
`governance`/`efficiency` are descriptive only today and never actually block a decision —
see TODO.md Phase 19 for wiring the two together.
"""

from __future__ import annotations

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, Obligation, TransformationCandidate, ValidationPacket


CORE_REQUIRED = {"preservation", "resolution", "noncollapse", "residual_limit"}


def _status_for(kind: str, candidate: TransformationCandidate, concept: ConceptNode) -> tuple[str, str | None]:
    """Return (status, blocker) for one obligation kind. Mostly structural presence checks
    today (e.g. `regime` passes iff the target concept declares one); kinds with no
    deterministic check fall through to `planned`."""

    target = candidate.target_concept
    if kind == "preservation":
        return ("passed", None) if candidate.preservation_map else ("failed", "missing preservation map")
    if kind == "resolution":
        return ("passed", None) if candidate.resolution_mechanism else ("failed", "missing resolution")
    if kind == "noncollapse":
        if "vacuous" in " ".join(candidate.assumptions + candidate.unknowns).lower():
            return "failed", "candidate appears vacuous"
        return "passed", None
    if kind == "residual_limit":
        return ("passed", None) if candidate.residual_limits else ("failed", "missing residual limits")
    if kind == "regime":
        return ("passed", None) if target.get("regime") else ("failed", "missing declared regime")
    if kind == "measurement":
        return ("passed", None) if target.get("measurement_model") else ("failed", "missing measurement model")
    if kind == "limiting_case":
        return ("passed", None) if target.get("limiting_cases") else ("partial", "limiting map needs proof")
    if kind == "anti_overfit":
        if candidate.operator == "IntroduceLatentCarrier" and not target.get("measurement_model"):
            return "failed", "latent entity lacks measurement consequences"
        return "passed", None
    if kind == "risk":
        safety = target.get("safety", {})
        if candidate.operator in {"Toolify", "Agentify"} and not safety:
            return "failed", "side-effecting surface lacks safety gates"
        return "passed", None
    if kind == "governance":
        return ("passed", None) if target.get("governance") else ("partial", "monitoring not fully specified")
    if kind == "efficiency":
        return "partial", "latency and cost need empirical benchmark"
    if kind in {"universality", "coverage", "transfer", "adequacy"}:
        return "partial", "requires proof or example instantiation"
    return "planned", "no deterministic validator registered"


def _method_for(kind: str) -> str:
    if kind in {"preservation", "resolution", "noncollapse", "universality", "transfer", "adequacy"}:
        return "proof_plan"
    if kind in {"regime", "measurement", "anti_overfit", "risk", "governance", "efficiency"}:
        return "review"
    return "review"


def generate_validation_packet(
    concept: ConceptNode, candidate: TransformationCandidate
) -> ValidationPacket:
    """Check every expected obligation for one candidate and collect a `ValidationPacket`,
    with `hard_gate_failures` populated from the core obligations plus the
    regime/measurement/risk kinds whenever their status isn't `passed`."""

    kinds = list(dict.fromkeys(candidate.expected_obligations + list(CORE_REQUIRED)))
    obligations: list[Obligation] = []
    hard_gate_failures: list[str] = []

    for kind in kinds:
        status, blocker = _status_for(kind, candidate, concept)
        payload = {
            "kind": kind,
            "statement": f"{candidate.operator} satisfies {kind} for {concept.name}",
            "method": _method_for(kind),
            "status": status,
            "evidence": [candidate.id] if status == "passed" else [],
            "blocker": blocker,
        }
        payload["id"] = stable_id("obligation", {"candidate": candidate.id, "kind": kind})
        obligation = Obligation.model_validate(payload)
        obligations.append(obligation)
        if kind in CORE_REQUIRED and status != "passed":
            hard_gate_failures.append(f"{kind}: {blocker or status}")
        if kind in {"regime", "measurement", "risk"} and status == "failed":
            hard_gate_failures.append(f"{kind}: {blocker or status}")

    summary = "all hard gates passed" if not hard_gate_failures else "hard gates failed"
    return ValidationPacket(
        candidate_id=candidate.id,
        obligations=obligations,
        hard_gate_failures=hard_gate_failures,
        summary=summary,
    )


def validate_candidates(
    concept: ConceptNode, candidates: list[TransformationCandidate]
) -> list[ValidationPacket]:
    return [generate_validation_packet(concept, candidate) for candidate in candidates]
