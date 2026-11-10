"""Guarded research workflow transitions."""

from __future__ import annotations

from typing import Any

from tdr.domain.models import RunPhase, RunState, utc_now


ALLOWED_TRANSITIONS = {
    RunPhase.NEW.value: {RunPhase.SCOPED.value},
    RunPhase.SCOPED.value: {RunPhase.MAPPED.value},
    RunPhase.MAPPED.value: {RunPhase.PRESSURED.value},
    RunPhase.PRESSURED.value: {RunPhase.FRAGMENTED.value},
    RunPhase.FRAGMENTED.value: {RunPhase.REFLECTED.value},
    RunPhase.REFLECTED.value: {RunPhase.GENERATED.value},
    RunPhase.GENERATED.value: {RunPhase.GATED.value},
    RunPhase.GATED.value: {RunPhase.FORMALIZED.value},
    RunPhase.FORMALIZED.value: {RunPhase.INSTANTIATED.value, RunPhase.REFLECTED.value, RunPhase.GENERATED.value, RunPhase.REPRESENTATION_REVIEW.value},
    RunPhase.INSTANTIATED.value: {RunPhase.TESTED.value},
    RunPhase.TESTED.value: {RunPhase.SYNTHESIZED.value, RunPhase.GENERATED.value, RunPhase.REPRESENTATION_REVIEW.value},
    RunPhase.REPRESENTATION_REVIEW.value: {RunPhase.MAPPED.value, RunPhase.BLOCKED.value},
}

SKILL_PHASE = {
    "scope-research-context": RunPhase.SCOPED.value,
    "map-theory-fragment": RunPhase.MAPPED.value,
    "interpret-conceptual-pressure": RunPhase.PRESSURED.value,
    "detect-essential-fragmentation": RunPhase.FRAGMENTED.value,
    "run-philosophical-reflection": RunPhase.REFLECTED.value,
    "generate-theory-candidates": RunPhase.GENERATED.value,
    "evaluate-relevance": RunPhase.GATED.value,
    "formalize-candidate": RunPhase.FORMALIZED.value,
    "instantiate-concretely": RunPhase.INSTANTIATED.value,
    "falsify-candidate": RunPhase.TESTED.value,
    "synthesize-portfolio": RunPhase.SYNTHESIZED.value,
    "mutate-representation": RunPhase.REPRESENTATION_REVIEW.value,
}


def guards_pass(current: str, target: str, result: dict[str, Any]) -> tuple[bool, str]:
    if result.get("status") in {"invalid", "blocked"}:
        return False, f"skill returned {result.get('status')}"
    artifacts = result.get("artifacts", [])
    if target == RunPhase.REFLECTED.value:
        site = next((item for item in artifacts if "essentiality" in item), None)
        if site is not None and float(site.get("essentiality", 0.0)) < 0.45:
            return False, "fragmentation does not pass essentiality threshold"
    if target == RunPhase.GATED.value:
        if not any(item.get("eligible") or all(gate.get("passed") for gate in item.get("gates", {}).values()) for item in artifacts):
            return False, "pressure, leverage, and return gates have not all passed"
    if target == RunPhase.SYNTHESIZED.value:
        rows = [row for item in artifacts for row in item.get("frontier", [])]
        supportive = any(item.get("supportive_results") for item in artifacts) or any(row.get("supportive_results") for row in rows)
        adversarial = any(item.get("adversarial_results") for item in artifacts) or any(row.get("adversarial_results") for row in rows)
        if artifacts and not (supportive and adversarial):
            return False, "synthesis requires supportive and adversarial results"
    return True, "guards passed"


def next_phase(state: RunState, skill_name: str, result: dict[str, Any]) -> RunState:
    target = SKILL_PHASE.get(skill_name)
    if target is None or target == state.phase:
        return state
    if target not in ALLOWED_TRANSITIONS.get(state.phase, set()):
        state.failures.append({"skill": skill_name, "reason": f"illegal transition {state.phase}->{target}", "at": utc_now()})
        return state
    passed, reason = guards_pass(state.phase, target, result)
    if not passed:
        state.failures.append({"skill": skill_name, "reason": reason, "at": utc_now()})
        return state
    state.phase = target
    state.revision += 1
    state.history.append({"phase": target, "skill": skill_name, "at": utc_now()})
    return state
