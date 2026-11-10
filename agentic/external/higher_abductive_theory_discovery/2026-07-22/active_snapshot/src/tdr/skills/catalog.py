"""The complete executable catalogue of bounded epistemic operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from tdr.atlas import map_fragment, propose_morphism
from tdr.domain.models import (
    ResearchContext,
    ResultStatus,
    bounded,
    jsonable,
    require_fields,
    result,
    stable_id,
)
from tdr.domain.schema import validate_payload, validate_skill_result
from tdr.generation import generate_candidates
from tdr.pressures import interpret_pressures
from tdr.reflection import detect_fragmentation, diagnose_defect, profile_meaning, run_reflection
from tdr.relevance import evaluate_candidate, pareto_frontier
from tdr.validation import falsify, formalize, instantiate, prove_transport


SkillFunction = Callable[[dict[str, Any]], Any]


@dataclass(frozen=True, slots=True)
class SkillSpec:
    name: str
    purpose: str
    role: str
    required: tuple[str, ...]
    output_kind: str
    budget: dict[str, float]
    function: SkillFunction
    human_gate: str | None = None


def _blocked(skill: str, payload: dict[str, Any], missing: list[str], message: str = "missing required inputs"):
    return result(
        ResultStatus.BLOCKED,
        uncertainties=[{"kind": "missing_input", "fields": missing}],
        next_actions=[{"skill": skill, "action": "supply_fields", "fields": missing}],
        messages=[message],
        skill=skill,
        inputs=payload,
    )


def scope_research_context(payload: dict[str, Any]):
    missing = require_fields(payload, ("question", "goals"))
    if missing:
        return _blocked("scope-research-context", payload, missing)
    goals = [str(item) for item in payload["goals"]]
    success = [str(item) for item in payload.get("success_criteria", [])]
    stop = [str(item) for item in payload.get("stop_criteria", [])]
    if not success:
        success = [f"produce a discriminating result for: {goal}" for goal in goals]
    if not stop:
        stop = ["declared resource budget is exhausted", "no eligible candidate remains on the frontier"]
    context = ResearchContext(
        context_id=str(payload.get("context_id") or stable_id("context", [payload["question"], goals])),
        question=str(payload["question"]),
        goals=goals,
        scope=dict(payload.get("scope") or {"status": "explicitly unspecified"}),
        protected_commitments=[str(item) for item in payload.get("protected_commitments", [])],
        success_criteria=success,
        stop_criteria=stop,
        budgets={key: float(value) for key, value in (payload.get("budgets") or {"steps": 50, "tokens": 100000, "wall_seconds": 3600}).items()},
    )
    review = not bool(payload.get("scope"))
    return result(
        ResultStatus.PARTIAL if review else ResultStatus.COMPLETED,
        artifacts=[context],
        uncertainties=[{"field": "scope", "value": 0.7, "reason": "scope was not explicitly supplied"}] if review else [],
        next_actions=[{"skill": "map-theory-fragment", "context_id": context.context_id}],
        messages=["Context is staged; changing goals or protected commitments requires human approval."],
        skill="scope-research-context",
        inputs=payload,
    )


def map_theory_fragment(payload: dict[str, Any]):
    if not payload.get("sources"):
        return _blocked("map-theory-fragment", payload, ["sources"])
    fragment = map_fragment(payload)
    unsourced = [claim for claim in fragment.claims if not claim.get("source_ref") and claim.get("status") != "conjecture"]
    status = ResultStatus.INVALID if unsourced else ResultStatus.COMPLETED
    return result(
        status,
        artifacts=[fragment],
        claims=[{"text": claim.get("text"), "epistemic_status": claim.get("status")} for claim in fragment.claims],
        uncertainties=[{"field": "claim", "reason": "nonconjectural claim lacks source", "claim": item} for item in unsourced],
        next_actions=[{"skill": "propose-theory-morphism", "fragment_id": fragment.fragment_id}, {"skill": "interpret-conceptual-pressure"}],
        skill="map-theory-fragment",
        inputs=payload,
    )


def propose_theory_morphism(payload: dict[str, Any]):
    missing = require_fields(payload, ("source_fragment", "target_fragment"))
    if missing:
        return _blocked("propose-theory-morphism", payload, missing)
    morphism = propose_morphism(payload)
    status = ResultStatus.COMPLETED if morphism.total_on_declared_domain and not morphism.obligations else ResultStatus.PARTIAL
    return result(
        status,
        artifacts=[morphism],
        uncertainties=[{"kind": "unproved_obligation", "text": item} for item in morphism.obligations],
        next_actions=[{"skill": "prove-transport", "morphism_id": morphism.morphism_id}],
        skill="propose-theory-morphism",
        inputs=payload,
    )


def interpret_conceptual_pressure(payload: dict[str, Any]):
    if not (payload.get("events") or payload.get("anomalies")):
        return _blocked("interpret-conceptual-pressure", payload, ["events"])
    pressures = interpret_pressures(payload)
    status = ResultStatus.COMPLETED if pressures else ResultStatus.INVALID
    solution_leak = [item.pressure_id for item in pressures if item.preferred_solution]
    return result(
        status,
        artifacts=pressures,
        uncertainties=[{"pressure_id": item, "reason": "preferred solution retained separately from pressure"} for item in solution_leak],
        next_actions=[{"skill": "profile-concept-meaning", "pressure_id": item.pressure_id} for item in pressures],
        skill="interpret-conceptual-pressure",
        inputs=payload,
    )


def profile_concept_meaning(payload: dict[str, Any]):
    missing = require_fields(payload, ("concept_id", "theory_id"))
    if missing:
        return _blocked("profile-concept-meaning", payload, missing)
    profile = profile_meaning(payload)
    unknown = [name for name, value in profile.uncertainty.items() if value >= 0.99]
    return result(
        ResultStatus.PARTIAL if unknown else ResultStatus.COMPLETED,
        artifacts=[profile],
        uncertainties=[{"field": name, "value": 1.0, "reason": "component marked unknown"} for name in unknown],
        next_actions=[{"skill": "detect-essential-fragmentation", "concept_id": profile.concept_id}],
        skill="profile-concept-meaning",
        inputs=payload,
    )


def detect_essential_fragmentation(payload: dict[str, Any]):
    if len(payload.get("profiles", [])) < 2:
        return _blocked("detect-essential-fragmentation", payload, ["profiles"], "two meaning profiles are required")
    site = detect_fragmentation(payload)
    status = ResultStatus.COMPLETED if site.essentiality >= 0.45 else ResultStatus.PARTIAL
    next_actions = []
    if site.essentiality >= 0.45:
        next_actions.append({"skill": "run-philosophical-reflection", "site_id": site.site_id})
    else:
        next_actions.append({"action": "retain_as_nonessential_mismatch", "site_id": site.site_id})
    if site.human_review_required:
        next_actions.append({"action": "human_review", "reason": "repair touches protected or operational commitments"})
    return result(
        status,
        artifacts=[site],
        uncertainties=[{"kind": "repair_estimate", "value": 0.35}],
        next_actions=next_actions,
        skill="detect-essential-fragmentation",
        inputs=payload,
    )


def run_philosophical_reflection(payload: dict[str, Any]):
    if not payload.get("site"):
        return _blocked("run-philosophical-reflection", payload, ["site"])
    record = run_reflection(payload)
    valid = bool(record.anticipated_losses and record.counterworlds and record.formal_obligations and len(record.lens_outputs) >= 8)
    return result(
        ResultStatus.COMPLETED if valid else ResultStatus.INVALID,
        artifacts=[record],
        claims=[{"text": item["description"], "epistemic_status": "redescription-not-fact"} for item in record.redescriptions],
        uncertainties=[{"kind": "interpretive_plurality", "reason": item} for item in record.contradictions],
        next_actions=[{"skill": "diagnose-categorical-defect", "reflection_id": record.reflection_id}],
        skill="run-philosophical-reflection",
        inputs=payload,
    )


def diagnose_categorical_defect(payload: dict[str, Any]):
    missing = require_fields(payload, ("site", "reflection"))
    if missing:
        return _blocked("diagnose-categorical-defect", payload, missing)
    defects = diagnose_defect(payload)
    metaphorical = [item for item in defects if item.get("metaphorical")]
    return result(
        ResultStatus.PARTIAL if metaphorical else ResultStatus.COMPLETED,
        artifacts=defects,
        uncertainties=[{"defect_id": item["defect_id"], "reason": "mapping remains metaphorical until typed"} for item in metaphorical],
        next_actions=[{"skill": "generate-theory-candidates"}],
        skill="diagnose-categorical-defect",
        inputs=payload,
    )


def generate_theory_candidates(payload: dict[str, Any]):
    if not payload.get("pressures"):
        return _blocked("generate-theory-candidates", payload, ["pressures"])
    candidates = generate_candidates(payload)
    modes = {item.mode for item in candidates}
    diverse = len(modes) >= min(4, len(payload.get("modes", ["local", "bridge", "mechanism", "mutation"])))
    hooks = all(item.atlas_patch and item.validation_tasks for item in candidates)
    status = ResultStatus.COMPLETED if diverse and hooks else ResultStatus.PARTIAL if candidates else ResultStatus.INVALID
    return result(
        status,
        artifacts=candidates,
        claims=[{"candidate_id": item.candidate_id, "text": item.formal_move, "epistemic_status": "conjectural"} for item in candidates],
        uncertainties=[{"candidate_id": item.candidate_id, **item.uncertainty} for item in candidates],
        next_actions=[{"skill": "evaluate-relevance", "candidate_id": item.candidate_id} for item in candidates],
        skill="generate-theory-candidates",
        inputs=payload,
        seed=int(payload.get("seed", 0)),
    )


def evaluate_relevance(payload: dict[str, Any]):
    candidates = payload.get("candidates")
    if candidates is None:
        candidates = [payload.get("candidate")] if payload.get("candidate") else []
    if not candidates:
        return _blocked("evaluate-relevance", payload, ["candidate or candidates"])
    evaluations = [evaluate_candidate({**payload, "candidate": candidate}) for candidate in candidates]
    frontier = pareto_frontier(evaluations)
    return result(
        ResultStatus.COMPLETED,
        artifacts=evaluations + [{"frontier": [item.get("candidate_id") for item in frontier]}],
        uncertainties=[{"kind": "context_dependence", "reason": "weights and dependency graph may change priority"}],
        next_actions=[{"skill": "formalize-candidate", "candidate_id": item.get("candidate_id")} for item in frontier],
        messages=["Relevance is an allocation heuristic, not a truth or novelty judgment."],
        skill="evaluate-relevance",
        inputs=payload,
    )


def formalize_candidate(payload: dict[str, Any]):
    if not payload.get("candidate"):
        return _blocked("formalize-candidate", payload, ["candidate"])
    outcome = formalize(payload)
    status = ResultStatus.BLOCKED if outcome.status == "blocked" else ResultStatus.PARTIAL if outcome.obligations_remaining else ResultStatus.COMPLETED
    return result(
        status,
        artifacts=[outcome],
        uncertainties=[{"kind": "proof_obligation", "text": item} for item in outcome.obligations_remaining],
        next_actions=[{"skill": "instantiate-concretely", "candidate_id": outcome.candidate_id}] if status != ResultStatus.BLOCKED else [],
        skill="formalize-candidate",
        inputs=payload,
    )


def prove_transport_skill(payload: dict[str, Any]):
    if not payload.get("morphism"):
        return _blocked("prove-transport", payload, ["morphism"])
    outcome = prove_transport(payload)
    status = ResultStatus.COMPLETED if outcome.status == "passed" else ResultStatus.PARTIAL if outcome.status == "partial" else ResultStatus.BLOCKED
    return result(
        status,
        artifacts=[outcome],
        uncertainties=[{"kind": "transport_obligation", "text": item} for item in outcome.obligations_remaining],
        skill="prove-transport",
        inputs=payload,
    )


def instantiate_concretely(payload: dict[str, Any]):
    if not payload.get("candidate"):
        return _blocked("instantiate-concretely", payload, ["candidate"])
    outcome = instantiate(payload)
    status = ResultStatus.PARTIAL if outcome.status == "partial" else ResultStatus.BLOCKED
    return result(
        status,
        artifacts=[outcome],
        uncertainties=[{"kind": "concrete_obligation", "text": item} for item in outcome.obligations_remaining],
        next_actions=[{"skill": "falsify-candidate", "candidate_id": outcome.candidate_id}],
        skill="instantiate-concretely",
        inputs=payload,
    )


def falsify_candidate(payload: dict[str, Any]):
    if not payload.get("candidate"):
        return _blocked("falsify-candidate", payload, ["candidate"])
    outcome = falsify(payload)
    status = ResultStatus.COMPLETED if outcome.status in {"passed", "falsified"} else ResultStatus.PARTIAL
    return result(
        status,
        artifacts=[outcome],
        claims=[{"text": item, "epistemic_status": "falsifying-condition"} for item in outcome.falsifying_conditions],
        uncertainties=[{"kind": "untested_adversarial_case", "text": item} for item in outcome.obligations_remaining],
        next_actions=[{"skill": "synthesize-portfolio"}],
        skill="falsify-candidate",
        inputs=payload,
    )


def mutate_representation(payload: dict[str, Any]):
    failures = [dict(item) for item in payload.get("failures", [])]
    reasons: dict[str, int] = {}
    for failure in failures:
        reason = str(failure.get("structural_reason") or failure.get("reason") or "unknown")
        reasons[reason] = reasons.get(reason, 0) + 1
    repeated = [(reason, count) for reason, count in reasons.items() if count >= 2]
    if not repeated:
        return _blocked("mutate-representation", payload, ["repeated structured failures"], "representation mutation requires a repeated failure pattern")
    reason, count = max(repeated, key=lambda item: item[1])
    proposal = {
        "mutation_id": stable_id("mutation", [reason, count]),
        "trigger": {"reason": reason, "count": count},
        "new_object_grammar": ["context", "presentation", "invariant", "obstruction", "boundary witness"],
        "new_morphism_grammar": ["context change", "partial interpretation", "lax coherence", "scope restriction"],
        "migration_functor": {
            "objects": "map each existing fragment to a presentation in its declared context",
            "morphisms": "map total morphisms directly; represent partial maps with explicit domain objects",
            "higher_cells": "retain witnesses and retype unresolved equivalences as lax cells",
        },
        "information_lost": ["unqualified global object identity"],
        "newly_expressible": [reason, "scope-indexed equivalence", "failed coherence as an obstruction object"],
        "unblocked_pressure_ids": [str(item) for item in payload.get("sterile_pressure_ids", [])],
        "human_review_required": True,
    }
    return result(
        ResultStatus.PARTIAL,
        artifacts=[proposal],
        uncertainties=[{"kind": "migration_risk", "value": 0.75}],
        next_actions=[{"action": "human_review", "reason": "migration may change accepted representation"}],
        skill="mutate-representation",
        inputs=payload,
    )


def synthesize_portfolio(payload: dict[str, Any]):
    candidates = [dict(item) for item in payload.get("candidates", [])]
    evaluations = [dict(item) for item in payload.get("evaluations", [])]
    validations = [dict(item) for item in payload.get("validations", [])]
    if not candidates or not evaluations:
        return _blocked("synthesize-portfolio", payload, ["candidates", "evaluations"])
    frontier = pareto_frontier(evaluations)
    by_candidate: dict[str, list[dict[str, Any]]] = {}
    for validation in validations:
        by_candidate.setdefault(str(validation.get("candidate_id")), []).append(validation)
    ranking: list[dict[str, Any]] = []
    for evaluation in frontier:
        candidate_id = str(evaluation.get("candidate_id"))
        checks = by_candidate.get(candidate_id, [])
        falsified = any(item.get("status") == "falsified" for item in checks)
        supportive = [item for item in checks if item.get("status") in {"passed", "partial"} and item.get("validator_role") != "adversarial-critic"]
        adversarial = [item for item in checks if item.get("validator_role") == "adversarial-critic"]
        ranking.append({
            "candidate_id": candidate_id,
            "priority_index": evaluation.get("priority_index"),
            "recommendation": "reject" if falsified else "continue_discriminating_validation" if not (supportive and adversarial) else "eligible_for_human_promotion_review",
            "supportive_results": supportive,
            "adversarial_results": adversarial,
            "unresolved": [item for check in checks for item in check.get("obligations_remaining", [])],
        })
    portfolio_identity = [
        {"candidate_id": item["candidate_id"], "priority_index": item["priority_index"], "recommendation": item["recommendation"]}
        for item in ranking
    ]
    synthesis = {
        "portfolio_id": stable_id("portfolio", portfolio_identity),
        "frontier": ranking,
        "disagreement": payload.get("disagreement", []),
        "uncertainty": payload.get("uncertainty", {"novelty": "unassessed", "external_validity": "unassessed"}),
        "next_discriminating_actions": [
            {"candidate_id": item["candidate_id"], "action": "run cheapest outstanding supportive and adversarial check"}
            for item in ranking if item["recommendation"] == "continue_discriminating_validation"
        ],
        "human_review_required": any(item["recommendation"] == "eligible_for_human_promotion_review" for item in ranking),
    }
    return result(
        ResultStatus.COMPLETED,
        artifacts=[synthesis],
        uncertainties=[{"kind": "portfolio_uncertainty", "value": synthesis["uncertainty"]}],
        next_actions=synthesis["next_discriminating_actions"],
        skill="synthesize-portfolio",
        inputs=payload,
    )


def audit_reasoning_run(payload: dict[str, Any]):
    trace = [dict(item) for item in payload.get("trace", [])]
    if not trace:
        return _blocked("audit-reasoning-run", payload, ["trace"])
    findings: list[dict[str, Any]] = []
    generation_roles: dict[str, str] = {}
    validation_roles: dict[str, set[str]] = {}
    for index, event in enumerate(trace):
        provenance_ok = all(event.get(field) for field in ("skill_name", "input_hash", "result_hash", "role"))
        if not provenance_ok:
            findings.append({"severity": "error", "event": index, "check": "provenance", "message": "incomplete replay tuple"})
        candidate_id = str(event.get("candidate_id", ""))
        if event.get("skill_name") == "generate-theory-candidates" and candidate_id:
            generation_roles[candidate_id] = str(event.get("role"))
        if event.get("skill_name") in {"formalize-candidate", "falsify-candidate", "instantiate-concretely"} and candidate_id:
            validation_roles.setdefault(candidate_id, set()).add(str(event.get("role")))
        if float(event.get("budget_used", 0.0)) > float(event.get("budget_limit", float("inf"))):
            findings.append({"severity": "error", "event": index, "check": "budget", "message": "budget exceeded"})
        if event.get("scope_hash_before") and event.get("scope_hash_after") and event["scope_hash_before"] != event["scope_hash_after"] and not event.get("human_approval"):
            findings.append({"severity": "error", "event": index, "check": "scope_drift", "message": "scope changed without approval"})
    for candidate_id, role in generation_roles.items():
        if role in validation_roles.get(candidate_id, set()):
            findings.append({"severity": "error", "candidate_id": candidate_id, "check": "role_separation", "message": "generator validated its own output"})
    checks = {
        "provenance": not any(item["check"] == "provenance" for item in findings),
        "role_separation": not any(item["check"] == "role_separation" for item in findings),
        "budget": not any(item["check"] == "budget" for item in findings),
        "drift": not any(item["check"] == "scope_drift" for item in findings),
        "replay": all(event.get("input_hash") and event.get("result_hash") for event in trace),
    }
    report = {"audit_id": stable_id("audit", trace), "checks": checks, "findings": findings, "passed": all(checks.values())}
    return result(
        ResultStatus.COMPLETED if report["passed"] else ResultStatus.INVALID,
        artifacts=[report],
        next_actions=[] if report["passed"] else [{"action": "remediate_integrity_findings"}],
        skill="audit-reasoning-run",
        inputs=payload,
    )


CATALOG: dict[str, SkillSpec] = {}


def _register(name: str, purpose: str, role: str, required: tuple[str, ...], output_kind: str, function: SkillFunction, human_gate: str | None = None):
    CATALOG[name] = SkillSpec(name, purpose, role, required, output_kind, {"steps": 1, "wall_seconds": 60}, function, human_gate)


_register("scope-research-context", "Freeze the question, scope, goals, protections, success, stop criteria, and budgets.", "portfolio-controller", ("question", "goals"), "ResearchContext", scope_research_context, "goal or protected-commitment change")
_register("map-theory-fragment", "Extract source-addressable typed theory fragments while retaining regime metadata.", "atlas-cartographer", ("sources",), "TheoryFragment", map_theory_fragment)
_register("propose-theory-morphism", "Stage a symbol and scope interpretation with explicit satisfaction obligations.", "atlas-cartographer", ("source_fragment", "target_fragment"), "TheoryMorphism", propose_theory_morphism)
_register("interpret-conceptual-pressure", "Localize anomalies, proof blockers, explanatory gaps, and pragmatic needs without presupposing solutions.", "pressure-interpreter", ("events",), "PressureItem[]", interpret_conceptual_pressure)
_register("profile-concept-meaning", "Reconstruct all nine dimensions of a concept's role in its native theory.", "meaning-profiler", ("concept_id", "theory_id"), "MeaningProfile", profile_concept_meaning)
_register("detect-essential-fragmentation", "Attempt cheap repairs and measure consequential residual mismatch and protected loss.", "fragmentation-analyst", ("profiles",), "FragmentationSite", detect_essential_fragmentation, "operational or ontological repair")
_register("run-philosophical-reflection", "Run eight independent lenses and compile redescription, loss, counterworld, and obligation records.", "philosophical-reflector", ("site",), "ReflectionRecord", run_philosophical_reflection, "genuine ontological or value choice")
_register("diagnose-categorical-defect", "Compile reflection into typed representability, coherence, descent, factorization, adjunction, or obstruction problems.", "structural-diagnostician", ("site", "reflection"), "DefectCandidate[]", diagnose_categorical_defect)
_register("generate-theory-candidates", "Generate and normalize a diverse local, bridge, mechanism, and representation-mutation portfolio.", "generative-theorist", ("pressures",), "HypothesisPackage[]", generate_theory_candidates)
_register("evaluate-relevance", "Apply pressure, leverage, and return gates, then compute a contextual relevance vector and penalties.", "relevance-analyst", ("candidate",), "RelevanceEvaluation", evaluate_relevance)
_register("formalize-candidate", "Compile a candidate into formal skeletons and exact proof obligations.", "formalizer-and-prover", ("candidate",), "ValidationOutcome", formalize_candidate)
_register("prove-transport", "Check theorem transport, totality, scope, satisfaction, and nontriviality.", "formalizer-and-prover", ("morphism",), "ValidationOutcome", prove_transport_skill)
_register("instantiate-concretely", "Construct mathematical or physical return plans, models, observables, and error obligations.", "concrete-instantiator", ("candidate",), "ValidationOutcome", instantiate_concretely)
_register("falsify-candidate", "Search degenerate cases, scope boundaries, rivals, vacuity, protected losses, and hidden auxiliaries.", "adversarial-critic", ("candidate",), "ValidationOutcome", falsify_candidate)
_register("mutate-representation", "Propose a new object/morphism grammar only after repeated structured failures.", "meta-representation-critic", ("failures",), "RepresentationMutation", mutate_representation, "migration of accepted content")
_register("synthesize-portfolio", "Retain the Pareto frontier, validation disagreements, uncertainty, and next discriminating actions.", "portfolio-controller", ("candidates", "evaluations"), "PortfolioSynthesis", synthesize_portfolio, "promotion as substantive theory")
_register("audit-reasoning-run", "Audit provenance, authority separation, budgets, scope drift, and replay completeness.", "integrity-auditor", ("trace",), "IntegrityReport", audit_reasoning_run)


def list_skills() -> list[dict[str, Any]]:
    return [
        {
            "name": spec.name,
            "purpose": spec.purpose,
            "role": spec.role,
            "required": list(spec.required),
            "output_kind": spec.output_kind,
            "budget": spec.budget,
            "human_gate": spec.human_gate,
        }
        for spec in CATALOG.values()
    ]


def execute_skill(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    if name not in CATALOG:
        raise KeyError(f"unknown skill: {name}")
    clean = validate_payload(payload)
    result_value = CATALOG[name].function(clean)
    output = result_value.to_dict() if hasattr(result_value, "to_dict") else jsonable(result_value)
    validate_skill_result(output)
    return output
