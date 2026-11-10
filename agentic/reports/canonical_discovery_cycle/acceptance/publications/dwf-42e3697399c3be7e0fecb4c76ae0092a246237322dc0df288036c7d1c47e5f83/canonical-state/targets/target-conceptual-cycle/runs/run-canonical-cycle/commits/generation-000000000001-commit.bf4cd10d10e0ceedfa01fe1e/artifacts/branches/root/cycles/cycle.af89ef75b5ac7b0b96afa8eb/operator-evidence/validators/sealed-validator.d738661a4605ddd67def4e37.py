"""Forge relevance-bound, structurally diverse high-risk theory portfolios.

Boldness here means changing primitives, relations, mechanisms, scales, or
explanatory direction while preserving the target's essential commitments. It
does not mean lexical surprise. Generation is deliberately two-pass: first an
intuition record is frozen without literature-conditioned pruning, then every
candidate is rebased against one exact target-scoped snapshot before Pareto
selection and parallel fan-out.
"""

from __future__ import annotations

import copy
import inspect
import itertools
import re
from typing import Any, Callable, Mapping, Sequence

from .contracts import ContractError, canonical_digest, stable_identifier, validate_payload
from .literature import build_demo_literature_snapshot, validate_snapshot


DEFAULT_CORNERS: tuple[str, ...] = (
    "ontology_inversion",
    "missing_mediator",
    "relation_process_first",
    "scale_regime_reversal",
    "cross_field_transfer",
    "unification_conjecture",
    "negative_theory",
    "counter_consensus",
    "emergence_stabilization",
    "conservative_control",
)
BENEFIT_AXES: tuple[str, ...] = (
    "conceptual_distance",
    "explanatory_upside",
    "unification_potential",
    "generativity",
    "coherence",
    "literature_distance",
    "tractability",
    "learning_if_false",
    "value_if_true",
)
MYSTICAL_MARKERS = re.compile(
    r"\b(magic|mystical|vibration|cosmic destiny|because consciousness wills)\b",
    re.I,
)
GENERATION_MODES = {
    "operator_instantiated_from_authored_proposals",
    "seed_free_deterministic",
    "seed_free_provider",
}
ELICITATION_DIMENSIONS: tuple[str, ...] = (
    "essential_relevance",
    "conceptual_depth",
    "unification",
    "corner_diversity",
    "correction_specificity",
)
HighRiskProvider = Callable[[Mapping[str, Any]], Mapping[str, Any] | Sequence[Mapping[str, Any]]]
HighRiskAdjudicator = Callable[[Mapping[str, Any]], Mapping[str, Any]]

_EXACT_REPLAYABILITY = "exact_callback_replay"
_SEED_FREE_CLAIM_BOUNDARY = (
    "Proposal-field-free generation does not establish creativity, quality, truth, "
    "novelty, conceptual depth, external preference, or efficacy."
)
_AUTHORED_CLAIM_BOUNDARY = (
    "The operator instantiated authored proposals or authored fallback templates; "
    "this is not proposal-field-free elicitation."
)
_STUDY_CLAIM_BOUNDARY = (
    "This study tests exact callback replay, known-template non-copy controls, "
    "repetition-invariant semantic differentiation, and internally correlated content "
    "adjudication. It establishes no creativity, discovery, conceptual-depth, truth, "
    "novelty, external-validation, theorem, physics-investment, or efficacy claim."
)
_ADJUDICATION_AUTHORITY_BOUNDARY = (
    "The adjudicator has distinct executable identity from the generator but remains "
    "an internally correlated protocol authority; no external preference follows."
)
_EXTERNAL_HUMAN_NULL = {
    "status": "unavailable",
    "assessor_count": 0,
    "reason": "No external human adjudication was supplied or executed.",
}
_SEED_FREEDOM_BOUNDARY = (
    "Explicit proposal fields are absent and known authored templates are screened; "
    "absence of unknown or latent conceptual influence is not established."
)


# Scores are relevance, distance, explanation, unification, generativity,
# coherence, literature distance, tractability, learning, truth probability,
# failure risk, and maturation cost. Keeping these independent prevents a cheap
# scalar threshold from erasing high-upside low-confidence proposals.
_TEMPLATES: tuple[dict[str, Any], ...] = (
    {
        "corner_family": "ontology_inversion",
        "mechanism_key": "obstruction-as-primary-object",
        "primitive": "obstruction_profile",
        "relation": "realizes_target_through_absence",
        "leap": "Treat the recurrent obstruction profile, rather than the incumbent witness, as the primary mathematical object.",
        "mechanism": "Functorially transport obstruction profiles across admissible representations; target success appears as a forbidden deformation class.",
        "affordance": "Turns repeated failure into an object that can compose, compare, and carry invariants.",
        "risk": "The profile may only rename ignorance and fail to recover concrete target witnesses.",
        "question": "Which nontrivial composition law makes obstruction profiles predictive rather than retrospective?",
        "scores": (0.92, 0.92, 0.72, 0.91, 0.72, 0.90, 0.31, 0.92, 0.96, 0.20, 0.80, 0.79),
        "wildcard": True,
    },
    {
        "corner_family": "missing_mediator",
        "mechanism_key": "latent-carrier-mediated-translation",
        "primitive": "latent_carrier",
        "relation": "mediates_incompatible_descriptions",
        "leap": "Introduce a carrier that records exactly what the rival descriptions cannot express about one another.",
        "mechanism": "A non-circular carrier exposes compatible local transports whose global coherence is equivalent to resolving the target pressure.",
        "affordance": "Makes the opposition expressible without collapsing either side into the other.",
        "risk": "The carrier may be defined by the desired conclusion or add no independent constraint.",
        "question": "What carrier axiom can be checked before the target conclusion and still reconstruct both rival descriptions?",
        "scores": (0.94, 0.82, 0.78, 0.84, 0.80, 0.76, 0.49, 0.80, 0.88, 0.34, 0.72, 0.66),
    },
    {
        "corner_family": "relation_process_first",
        "mechanism_key": "process-before-object-reconstruction",
        "primitive": "admissible_transition_process",
        "relation": "stabilizes_as_object",
        "leap": "Reconstruct stable target objects as equivalence classes of admissible transformation histories.",
        "mechanism": "Coherent processes are primary; an object exists only when histories satisfy a descent and stabilization condition.",
        "affordance": "Explains identity through preserved transition structure instead of assuming identity in advance.",
        "risk": "Process equivalence may erase the exact object or quantifier required by the target.",
        "question": "Which history equivalence preserves target nontriviality while yielding a stable reconstruction theorem?",
        "scores": (0.90, 0.86, 0.75, 0.83, 0.77, 0.80, 0.42, 0.82, 0.89, 0.30, 0.75, 0.70),
    },
    {
        "corner_family": "scale_regime_reversal",
        "mechanism_key": "global-constraint-local-realization",
        "primitive": "global_consistency_budget",
        "relation": "constrains_local_realizers",
        "leap": "Reverse the explanatory direction: global consistency budgets generate the admissible local mechanisms.",
        "mechanism": "A global invariant restricts local realizers before a limit is taken, preventing the usual order-of-limits information loss.",
        "affordance": "Makes regime transfer and noncommuting limits explicit theoretical objects.",
        "risk": "The global budget may presuppose the very local behavior it is meant to explain.",
        "question": "For which boundary regime do global-first and local-first constructions diverge on a target-relevant invariant?",
        "scores": (0.91, 0.78, 0.72, 0.76, 0.83, 0.72, 0.55, 0.78, 0.83, 0.39, 0.61, 0.58),
    },
    {
        "corner_family": "cross_field_transfer",
        "mechanism_key": "descent-obstruction-transfer",
        "primitive": "transported_descent_defect",
        "relation": "preserves_target_invariant_under_transfer",
        "leap": "Transfer a descent-defect mechanism from a neighboring field while auditing every preserved and broken invariant.",
        "mechanism": "The source mechanism is retained only on the subcategory where target quantifiers, composition, and boundary behavior commute with transport.",
        "affordance": "Imports a mature explanatory mechanism without treating analogy as identity.",
        "risk": "A broken invariant may carry all of the source mechanism's force.",
        "question": "Which preserved invariant is sufficient for the transported descent defect to constrain the target?",
        "scores": (0.93, 0.74, 0.76, 0.79, 0.72, 0.84, 0.47, 0.85, 0.87, 0.28, 0.76, 0.74),
    },
    {
        "corner_family": "unification_conjecture",
        "mechanism_key": "common-curvature-of-barriers",
        "primitive": "barrier_curvature",
        "relation": "projects_to_distinct_obstructions",
        "leap": "Model apparently different barriers as projections of one non-flat compatibility structure.",
        "mechanism": "A common curvature invariant produces distinct obstruction signatures in different regimes while retaining their boundary differences.",
        "affordance": "Unifies why routes fail without declaring their mathematical differences irrelevant.",
        "risk": "The abstraction may weaken each barrier until the unification becomes vacuous.",
        "question": "What boundary case forces the proposed common curvature to distinguish rather than erase two known barriers?",
        "scores": (0.95, 0.80, 0.90, 0.82, 0.82, 0.73, 0.48, 0.83, 0.91, 0.36, 0.66, 0.64),
    },
    {
        "corner_family": "negative_theory",
        "mechanism_key": "route-incompatibility-no-go",
        "primitive": "route_incompatibility_certificate",
        "relation": "forbids_joint_route_assumptions",
        "leap": "Seek a typed no-go theorem showing that a recurring family of attractive route assumptions cannot coexist.",
        "mechanism": "Minimal route commitments generate an incompatibility certificate with explicit quantifier and regime scope.",
        "affordance": "Converts expensive repeated failure into reusable negative knowledge and a sharper search space.",
        "risk": "The no-go may only cover an artificially narrow proxy family.",
        "question": "What minimal assumption subset still yields a non-circular incompatibility certificate?",
        "scores": (0.97, 0.66, 0.70, 0.75, 0.91, 0.58, 0.71, 0.94, 0.77, 0.58, 0.38, 0.42),
    },
    {
        "corner_family": "counter_consensus",
        "mechanism_key": "taboo-decomposition-release",
        "primitive": "nonstandard_decomposition",
        "relation": "releases_hidden_dependency",
        "leap": "Suspend the standard decomposition and test whether its independence assumption manufactures the central obstruction.",
        "mechanism": "A coupled decomposition retains a dependency normally quotiented away, allowing a new invariant to mediate the target pressure.",
        "affordance": "Exposes a contingent proof norm as a possible source of the apparent impossibility.",
        "risk": "Removing the standard decomposition may sacrifice the protected success that defines the target.",
        "question": "Can a coupled decomposition recover the incumbent success in a boundary case without reinstating the taboo assumption?",
        "scores": (0.91, 0.95, 0.86, 0.93, 0.67, 0.94, 0.24, 0.90, 0.98, 0.16, 0.86, 0.88),
        "wildcard": True,
    },
    {
        "corner_family": "emergence_stabilization",
        "mechanism_key": "coherent-fixed-point-emergence",
        "primitive": "coherence_fixed_point",
        "relation": "stabilizes_target_structure",
        "leap": "Treat target structure as an emergent fixed point of coherence repair rather than a primitive construction.",
        "mechanism": "Iterated local consistency repair converges only when an invariant compression condition holds, producing a non-vacuous stable object.",
        "affordance": "Connects construction, robustness, and explanatory compression in one dynamics.",
        "risk": "The fixed point may exist by definition or fail to recover the theorem's subject.",
        "question": "Which compression invariant makes the stabilization nontrivial and reconstructs the exact target object?",
        "scores": (0.89, 0.84, 0.81, 0.88, 0.74, 0.78, 0.43, 0.81, 0.90, 0.27, 0.78, 0.73),
    },
    {
        "corner_family": "conservative_control",
        "mechanism_key": "incumbent-mechanism-deepening",
        "primitive": "incumbent_refinement",
        "relation": "sharpens_known_mechanism",
        "leap": "Retain the incumbent ontology and isolate the smallest unresolved mechanism needed for ordinary deepening.",
        "mechanism": "Refine the existing route's weakest explicit dependency without adding a new ontological carrier.",
        "affordance": "Provides a matched control for whether radical restructuring creates genuine independent learning.",
        "risk": "Local refinement may remain trapped inside the incumbent conceptual bottleneck.",
        "question": "What is the smallest incumbent dependency whose resolution would change the target-relevant route?",
        "scores": (0.99, 0.18, 0.35, 0.42, 0.94, 0.22, 0.87, 0.62, 0.48, 0.68, 0.20, 0.28),
        "control": True,
    },
)

_AUTHORED_TEMPLATE_REFERENCE_DIGEST = canonical_digest(_TEMPLATES)
_SEED_FREE_OPERATORS: tuple[tuple[str, str, str, str], ...] = (
    ("ontology_inversion", "retype", "counterobject", "tracks_asymmetry_through"),
    ("missing_mediator", "interpose", "translation_carrier", "mediates_without_identifying"),
    ("relation_process_first", "historicize", "transition_record", "stabilizes_under_composition"),
    ("scale_regime_reversal", "reverse", "regime_budget", "constrains_before_limiting"),
    ("cross_field_transfer", "transport", "invariant_filter", "admits_only_preserved_structure"),
    ("unification_conjecture", "factor", "common_generator", "projects_with_residual_difference"),
    ("negative_theory", "forbid", "incompatibility_witness", "certifies_joint_failure"),
    ("counter_consensus", "suspend", "coupled_decomposition", "retains_discarded_dependency"),
    ("emergence_stabilization", "iterate", "repair_fixed_point", "emerges_after_coherence_repair"),
    ("conservative_control", "refine", "incumbent_dependency", "sharpens_without_retyping"),
)


def _without(payload: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    """Copy an envelope while excluding circular digest fields."""

    result = copy.deepcopy(dict(payload))
    for key in keys:
        result.pop(key, None)
    return result


def _callable_digest(callback: Callable[..., Any]) -> str:
    """Fingerprint callable code for a receipt without claiming dependency closure."""

    code = getattr(callback, "__code__", None)
    try:
        source = inspect.getsource(callback)
    except (OSError, TypeError):
        source = None
    return canonical_digest(
        {
            "module": getattr(callback, "__module__", "unknown"),
            "qualname": getattr(callback, "__qualname__", repr(callback)),
            "source": source,
            "bytecode": code.co_code.hex() if code is not None else None,
            "constants": [repr(item) for item in code.co_consts] if code is not None else [],
            "names": list(code.co_names) if code is not None else [],
        }
    )


def build_hidden_elicitation_prompt(
    *,
    prompt_id: str,
    target_id: str,
    theory_state_digest: str,
    literature_snapshot_digest: str,
    prompt_text: str,
) -> dict[str, Any]:
    """Seal a target-bound prompt; studies disclose only its digest, not its text."""

    prompt = {
        "schema_version": "1.0",
        "prompt_id": prompt_id,
        "target_id": target_id,
        "theory_state_digest": theory_state_digest,
        "literature_snapshot_digest": literature_snapshot_digest,
        "prompt_text": prompt_text.strip(),
    }
    if not prompt["prompt_id"] or not prompt["prompt_text"]:
        raise ContractError("hidden elicitation prompt requires prompt_id and prompt_text")
    prompt["content_digest"] = canonical_digest(_without(prompt, "content_digest"))
    return prompt


def _validate_hidden_prompt(
    prompt: Mapping[str, Any],
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> None:
    required = {
        "schema_version",
        "prompt_id",
        "target_id",
        "theory_state_digest",
        "literature_snapshot_digest",
        "prompt_text",
        "content_digest",
    }
    if set(prompt) != required or prompt.get("schema_version") != "1.0":
        raise ContractError("hidden elicitation prompt has an invalid strict shape")
    if prompt["content_digest"] != canonical_digest(_without(prompt, "content_digest")):
        raise ContractError("hidden elicitation prompt digest mismatch")
    if prompt["target_id"] != charter["target_id"] or prompt["target_id"] != snapshot["target_id"]:
        raise ContractError("hidden elicitation prompt target mismatch")
    if prompt["theory_state_digest"] != charter["theory_state_digest"]:
        raise ContractError("hidden elicitation prompt theory-state mismatch")
    if prompt["literature_snapshot_digest"] != snapshot["content_digest"]:
        raise ContractError("hidden elicitation prompt literature digest mismatch")


def _generation_provenance(
    source_proposals: Sequence[Mapping[str, Any]],
    *,
    proposals_were_supplied: bool,
    requested: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Normalize mode naming and prevent provider outputs being called authored-free."""

    proposals_digest = canonical_digest(list(source_proposals))
    if requested is None:
        return {
            "mode": "operator_instantiated_from_authored_proposals",
            "generator_authority_id": (
                "operator.supplied-proposals"
                if proposals_were_supplied
                else "high-risk-forger.authored-templates.v1"
            ),
            "generator_authority_digest": (
                proposals_digest
                if proposals_were_supplied
                else _AUTHORED_TEMPLATE_REFERENCE_DIGEST
            ),
            "proposal_request_digest": None,
            "source_proposals_digest": proposals_digest,
            "authored_template_reference_digest": _AUTHORED_TEMPLATE_REFERENCE_DIGEST,
            "claim_boundary": _AUTHORED_CLAIM_BOUNDARY,
        }
    provenance = copy.deepcopy(dict(requested))
    required = {
        "mode",
        "generator_authority_id",
        "generator_authority_digest",
        "proposal_request_digest",
        "source_proposals_digest",
        "authored_template_reference_digest",
        "claim_boundary",
    }
    if set(provenance) != required:
        raise ContractError("seed-free generation provenance has an invalid strict shape")
    if provenance["mode"] not in {"seed_free_deterministic", "seed_free_provider"}:
        raise ContractError("external generation provenance must name a seed-free mode")
    if provenance["source_proposals_digest"] != proposals_digest:
        raise ContractError("seed-free proposal output digest mismatch")
    if provenance["authored_template_reference_digest"] is not None:
        raise ContractError("seed-free modes cannot cite authored proposals as their source")
    if provenance["proposal_request_digest"] is None:
        raise ContractError("proposal-field-free modes require an exact request digest")
    if provenance["claim_boundary"] != _SEED_FREE_CLAIM_BOUNDARY:
        raise ContractError("proposal-field-free provenance claim boundary mismatch")
    return provenance


def structural_signature(candidate: Mapping[str, Any]) -> str:
    """Hash primitives, mechanism, maturation question, and genealogy—not prose."""

    ontology = candidate.get("ontology_delta", {})
    return canonical_digest(
        {
            "primitives": sorted(ontology.get("new_primitives", [])),
            "relations": sorted(ontology.get("new_relations", [])),
            "mechanism_key": candidate.get("mechanism_key"),
            "maturation_question": " ".join(
                str(candidate.get("maturation_question", "")).lower().split()
            ),
            "genealogy": sorted(candidate.get("genealogy", [])),
        }
    )


def blind_articulation_digest(candidate: Mapping[str, Any]) -> str:
    """Hash only the pre-literature conceptual articulation."""

    return canonical_digest(
        {
            "hypothesis_id": candidate["hypothesis_id"],
            "corner_family": candidate["corner_family"],
            "intuition_provenance": candidate["intuition_provenance"],
            "intuitive_leap": candidate["intuitive_leap"],
            "mechanism": candidate["mechanism"],
            "mechanism_key": candidate["mechanism_key"],
            "ontology_delta": candidate["ontology_delta"],
            "target_pressures_addressed": candidate[
                "target_pressures_addressed"
            ],
            "target_commitments": candidate["target_commitments"],
            "protected_successes": candidate["protected_successes"],
            "assumptions_or_invariants_risked": candidate[
                "assumptions_or_invariants_risked"
            ],
            "explanatory_upside": candidate["explanatory_upside"],
            "unification_upside": candidate["unification_upside"],
            "value_if_right": candidate["value_if_right"],
            "learning_value_if_wrong": candidate["learning_value_if_wrong"],
            "maturation_question": candidate["maturation_question"],
            "correction_conditions": candidate["correction_conditions"],
            "boundary_case": candidate["boundary_case"],
            "genealogy": candidate["genealogy"],
        }
    )


def _dominates(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Return Pareto dominance with reward axes maximized and costs minimized."""

    lq, rq = left["quality_axes"], right["quality_axes"]
    lr, rr = left["risk_axes"], right["risk_axes"]
    weak = all(float(lq[axis]) >= float(rq[axis]) for axis in BENEFIT_AXES)
    weak = weak and float(lr["failure_risk"]) <= float(rr["failure_risk"])
    weak = weak and float(lr["maturation_cost"]) <= float(rr["maturation_cost"])
    strict = any(float(lq[axis]) > float(rq[axis]) for axis in BENEFIT_AXES)
    strict = strict or float(lr["failure_risk"]) < float(rr["failure_risk"])
    strict = strict or float(lr["maturation_cost"]) < float(rr["maturation_cost"])
    return weak and strict


def _template_candidate(
    template: Mapping[str, Any],
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    """Articulate one intuition before applying its mandatory literature relation."""

    target_id = str(charter["target_id"])
    target_statement = str(charter["target_statement"])
    pressures = [str(item) for item in charter["root_tensions"]]
    commitments = [str(item) for item in charter["target_commitments"]]
    protected = [str(item) for item in charter["protected_successes"]]
    (
        relevance,
        distance,
        explanation,
        unification,
        generativity,
        coherence,
        literature_distance,
        tractability,
        learning,
        truth_probability,
        failure_risk,
        cost,
    ) = template["scores"]
    family = str(template["corner_family"])
    hypothesis_id = stable_identifier(
        "hypothesis", target_id, family, template["mechanism_key"], template["question"]
    )
    is_control = bool(template.get("control"))
    is_wildcard = bool(template.get("wildcard"))
    candidate: dict[str, Any] = {
        "hypothesis_id": hypothesis_id,
        "corner_family": family,
        "concept_lifecycle_state": "conceptually_articulated",
        "maturation_status": "theory_question_open" if is_control else "parallel_ready",
        "truth_status": "not_assessed",
        "intuition_provenance": {
            "mode": "blind_intuition_first",
            "trigger": pressures[index % len(pressures)],
            "pre_literature_statement": str(template["leap"]),
        },
        "intuitive_leap": f"For {target_statement}: {template['leap']}",
        "mechanism": str(template["mechanism"]),
        "mechanism_key": str(template["mechanism_key"]),
        "ontology_delta": {
            "new_primitives": [str(template["primitive"])],
            "new_relations": [str(template["relation"])],
            "removed_or_retyped": (
                ["incumbent_primary_explanatory_direction"] if not is_control else []
            ),
            "affordance": str(template["affordance"]),
        },
        "target_pressures_addressed": [pressures[index % len(pressures)]],
        "target_commitments": commitments,
        "protected_successes": protected,
        "assumptions_or_invariants_risked": [
            str(
                charter.get("forbidden_target_drift")
                or "Target identity and quantifier scope must not drift."
            ),
            str(template["risk"]),
        ],
        "explanatory_upside": f"If right, {template['affordance'].lower()}",
        "unification_upside": (
            "Unify the named pressure with at least one neighboring obstruction "
            "while explicitly preserving boundary-regime differences."
        ),
        "value_if_right": (
            f"High theoretical value: the mechanism would reorganize how {target_id} "
            "is represented and which obligations become expressible."
        ),
        "learning_value_if_wrong": (
            f"A failure would localize this structural possibility: {template['risk']}"
        ),
        "risk_axes": {
            "probability_of_truth": truth_probability,
            "failure_risk": failure_risk,
            "maturation_cost": cost,
        },
        "quality_axes": {
            "essential_relevance": relevance,
            "conceptual_distance": distance,
            "explanatory_upside": explanation,
            "unification_potential": unification,
            "generativity": generativity,
            "coherence": coherence,
            "literature_distance": literature_distance,
            "tractability": tractability,
            "learning_if_false": learning,
            "value_if_true": max(explanation, unification, generativity),
        },
        "literature_relation": "pending_rebase",
        "literature_source_ids": [],
        "literature_rebase_receipt": {},
        "blind_articulation_digest": "",
        "novelty_claim": False,
        "non_claim_boundary": (
            "Absence of a matching source is not evidence of novelty; this remains "
            "a conceptual seed, not a theorem or empirical result."
        ),
        "maturation_question": str(template["question"]),
        "correction_conditions": [
            (
                f"Demote if the proposed {template['primitive']} is definitionally "
                "equivalent to the desired conclusion."
            ),
            (
                "Reframe if literature shows the mechanism is anticipated but a "
                "preserved structural difference remains."
            ),
            (
                "Retire if its boundary case changes the target statement or "
                "destroys every protected success."
            ),
        ],
        "boundary_case": str(template["risk"]),
        "premortem": {
            "failure_signatures": [
                str(template["risk"]),
                "The mechanism collapses to a renamed incumbent route.",
            ],
            "earliest_decisive_theory_test": str(template["question"]),
            "disposition": (
                "artifact_sprint"
                if is_wildcard
                else ("invest" if not is_control else "falsifier_sprint")
            ),
        },
        "branch_independence_signature": {
            "unique_primitives": [str(template["primitive"])],
            "unique_mechanism": str(template["mechanism"]),
            "forbidden_cross_branch_context": [
                "Other branch conclusions before the blind divergence barrier",
                "Mutable global latest/current literature or theory reports",
            ],
            "required_context": [
                "Frozen target charter",
                "Frozen theory digest",
                "Frozen target literature digest",
            ],
            "overlaps_with_hypothesis_ids": [],
        },
        "genealogy": [
            stable_identifier("intuition", target_id, family, template["leap"])
        ],
        "structural_signature": "",
        "selection_status": "control" if is_control else "dominated",
        "is_wildcard": is_wildcard,
        "is_control": is_control,
    }
    candidate["structural_signature"] = structural_signature(candidate)
    candidate["blind_articulation_digest"] = blind_articulation_digest(
        candidate
    )
    return candidate


def _rebase_candidate(
    candidate: Mapping[str, Any],
    *,
    snapshot: Mapping[str, Any],
    index: int,
    requested_relation: str | None = None,
    requested_source_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Perform the second pass against one frozen target-scoped snapshot.

    This function is intentionally separate from articulation: callers can
    inspect or persist the pre-literature intuition before any source relation
    is allowed to affect selection.
    """

    rebased = copy.deepcopy(dict(candidate))
    available = [item["source_id"] for item in snapshot["sources"]]
    source_ids = (
        list(requested_source_ids)
        if requested_source_ids is not None
        else ([available[index % len(available)]] if available else [])
    )
    if not set(source_ids).issubset(available):
        raise ContractError(
            f"candidate {candidate['hypothesis_id']} cites a source outside the frozen snapshot"
        )
    relation = requested_relation
    if not relation or relation == "pending_rebase":
        relation = "coverage_unknown"
        if source_ids:
            relation = {
                "cross_field_transfer": "cross_field_bridge",
                "negative_theory": "partly_anticipated",
                "conservative_control": "partly_anticipated",
            }.get(str(candidate["corner_family"]), "apparently_open")
    rebased["literature_relation"] = relation
    rebased["literature_source_ids"] = source_ids
    rebased["concept_lifecycle_state"] = (
        "literature_rebased"
        if snapshot["provenance_mode"] == "live"
        else "incubating"
    )
    rebased["literature_rebase_receipt"] = {
        "receipt_id": stable_identifier(
            "hypothesis-rebase",
            rebased["hypothesis_id"],
            rebased["blind_articulation_digest"],
            snapshot["content_digest"],
            relation,
            source_ids,
        ),
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "blind_articulation_digest": rebased[
            "blind_articulation_digest"
        ],
        "relation": relation,
        "source_ids": source_ids,
        "status": (
            "completed"
            if snapshot["provenance_mode"] == "live"
            else "provisional_local_only"
        ),
    }
    return rebased


def _normalize_proposal(
    raw: Mapping[str, Any],
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    """Overlay an explicit proposal on a complete structural template."""

    family = str(
        raw.get("corner_family") or DEFAULT_CORNERS[index % len(DEFAULT_CORNERS)]
    )
    template = next(
        (item for item in _TEMPLATES if item["corner_family"] == family),
        _TEMPLATES[index % len(_TEMPLATES)],
    )
    candidate = _template_candidate(
        template, charter=charter, snapshot=snapshot, index=index
    )
    for key, value in raw.items():
        if key in {
            "literature_relation",
            "literature_source_ids",
            "literature_rebase_receipt",
            "concept_lifecycle_state",
            "selection_status",
            "blind_articulation_digest",
        }:
            continue
        candidate[key] = copy.deepcopy(value)
    if "hypothesis_id" not in raw:
        candidate["hypothesis_id"] = stable_identifier(
            "hypothesis",
            charter["target_id"],
            candidate["corner_family"],
            candidate["mechanism_key"],
            candidate["maturation_question"],
        )
    candidate["structural_signature"] = structural_signature(candidate)
    candidate["blind_articulation_digest"] = blind_articulation_digest(
        candidate
    )
    return candidate


def _pairwise_matrix(
    candidates: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Expose structural overlap so parallel independence is inspectable."""

    rows: list[dict[str, Any]] = []
    for left, right in itertools.combinations(candidates, 2):
        lp = set(left["ontology_delta"]["new_primitives"])
        rp = set(right["ontology_delta"]["new_primitives"])
        union = lp | rp
        overlap = len(lp & rp) / len(union) if union else 1.0
        same_mechanism = left["mechanism_key"] == right["mechanism_key"]
        same_question = " ".join(left["maturation_question"].lower().split()) == " ".join(
            right["maturation_question"].lower().split()
        )
        same_genealogy = bool(set(left["genealogy"]) & set(right["genealogy"]))
        independent = not same_mechanism and not same_question and overlap < 0.67
        rows.append(
            {
                "left_id": left["hypothesis_id"],
                "right_id": right["hypothesis_id"],
                "structural_overlap": round(overlap, 6),
                "shared_primitives": sorted(lp & rp),
                "same_mechanism": same_mechanism,
                "same_maturation_question": same_question,
                "shared_genealogy": same_genealogy,
                "independent": independent,
            }
        )
    return rows


def forge_high_risk_portfolio(
    charter: Mapping[str, Any],
    literature_snapshot: Mapping[str, Any],
    *,
    proposals: Sequence[Mapping[str, Any]] | None = None,
    requested_count: int = 10,
    relevance_floor: float = 0.70,
    generation_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create 8–12 blind-first hypotheses, rebase, deduplicate, and Pareto-select."""

    required_charter = {
        "target_id",
        "target_statement",
        "theory_state_digest",
        "root_tensions",
        "target_commitments",
        "protected_successes",
        "forbidden_target_drift",
    }
    missing = sorted(required_charter - charter.keys())
    if missing:
        raise ContractError(f"discovery charter is missing: {', '.join(missing)}")
    if not 8 <= requested_count <= 12:
        raise ContractError("major high-risk portfolios require 8 to 12 candidates")
    if (
        not charter["root_tensions"]
        or not charter["target_commitments"]
        or not charter["protected_successes"]
    ):
        raise ContractError(
            "charter tensions, commitments, and protected successes must be non-empty"
        )
    validate_snapshot(literature_snapshot)
    if literature_snapshot["target_id"] != charter["target_id"]:
        raise ContractError(
            "a literature snapshot for one target cannot rebase another target's hypotheses"
        )
    if literature_snapshot["theory_state_digest"] != charter["theory_state_digest"]:
        raise ContractError(
            "portfolio and literature snapshot must freeze the same theory-state digest"
        )

    source_proposals = (
        list(proposals) if proposals is not None else list(_TEMPLATES[:requested_count])
    )
    if not 8 <= len(source_proposals) <= 12:
        raise ContractError("proposal set must contain 8 to 12 candidates")
    normalized_generation_provenance = _generation_provenance(
        source_proposals,
        proposals_were_supplied=proposals is not None,
        requested=generation_provenance,
    )
    # First freeze the articulated intuitions. Literature fields remain pending
    # by construction, so source consensus cannot anchor initial corner choice.
    blind_hypotheses = [
        (
            _normalize_proposal(
                item,
                charter=charter,
                snapshot=literature_snapshot,
                index=index,
            )
            if proposals is not None
            else _template_candidate(
                item,
                charter=charter,
                snapshot=literature_snapshot,
                index=index,
            )
        )
        for index, item in enumerate(source_proposals)
    ]
    # Only after all blind candidates exist do we assign source relations. This
    # is the mandatory second pass and occurs before deduplication or selection.
    hypotheses = [
        _rebase_candidate(
            candidate,
            snapshot=literature_snapshot,
            index=index,
            requested_relation=(
                str(source_proposals[index].get("literature_relation"))
                if proposals is not None
                and source_proposals[index].get("literature_relation")
                else None
            ),
            requested_source_ids=(
                list(source_proposals[index].get("literature_source_ids", []))
                if proposals is not None
                and "literature_source_ids" in source_proposals[index]
                else None
            ),
        )
        for index, candidate in enumerate(blind_hypotheses)
    ]

    # Structural equivalence is independent of wording. Duplicate records remain
    # visible as negative design evidence but are never purchased as branches.
    signature_groups: dict[str, list[dict[str, Any]]] = {}
    for candidate in hypotheses:
        signature_groups.setdefault(candidate["structural_signature"], []).append(
            candidate
        )
    duplicate_groups: list[list[str]] = []
    for group in signature_groups.values():
        if len(group) <= 1:
            continue
        ids = sorted(item["hypothesis_id"] for item in group)
        duplicate_groups.append(ids)
        for duplicate in sorted(group, key=lambda item: item["hypothesis_id"])[1:]:
            duplicate["selection_status"] = "structural_duplicate"

    eligible = [
        item
        for item in hypotheses
        if item["quality_axes"]["essential_relevance"] >= relevance_floor
        and item["selection_status"] != "structural_duplicate"
    ]
    for candidate in hypotheses:
        if candidate["quality_axes"]["essential_relevance"] < relevance_floor:
            candidate["selection_status"] = "below_relevance"
    dominated_by: dict[str, list[str]] = {
        candidate["hypothesis_id"]: [
            rival["hypothesis_id"]
            for rival in eligible
            if rival is not candidate and _dominates(rival, candidate)
        ]
        for candidate in eligible
    }
    nondominated = {
        hypothesis_id
        for hypothesis_id, dominators in dominated_by.items()
        if not dominators
    }
    wildcard_candidates = [
        item
        for item in eligible
        if item["is_wildcard"]
        and item["risk_axes"]["probability_of_truth"] <= 0.35
        and item["quality_axes"]["value_if_true"] >= 0.80
        and item["hypothesis_id"] in nondominated
    ]
    protected_wildcards = [
        item["hypothesis_id"] for item in wildcard_candidates[:2]
    ]
    wildcards_available = bool(charter.get("wildcards_available", True))
    fewer_wildcards_reason = charter.get("fewer_wildcards_reason")
    if wildcards_available and len(protected_wildcards) < 2:
        raise ContractError(
            "at least two relevant, high-upside, nondominated low-confidence "
            "wildcards must be protected when available"
        )
    if not wildcards_available and not fewer_wildcards_reason:
        raise ContractError(
            "a target-grounded reason is required when two viable wildcards are unavailable"
        )
    controls = [item["hypothesis_id"] for item in hypotheses if item["is_control"]]
    if not controls:
        raise ContractError("the portfolio requires a conservative control")
    for candidate in eligible:
        hypothesis_id = candidate["hypothesis_id"]
        if candidate["is_control"]:
            candidate["selection_status"] = "control"
        elif hypothesis_id in protected_wildcards:
            candidate["selection_status"] = "protected_wildcard"
        elif hypothesis_id in nondominated:
            candidate["selection_status"] = "selected_pareto"
        else:
            candidate["selection_status"] = "dominated"

    matrix = _pairwise_matrix(hypotheses)
    overlap_lookup: dict[str, list[str]] = {
        item["hypothesis_id"]: [] for item in hypotheses
    }
    for row in matrix:
        if not row["independent"]:
            overlap_lookup[row["left_id"]].append(row["right_id"])
            overlap_lookup[row["right_id"]].append(row["left_id"])
    for candidate in hypotheses:
        candidate["branch_independence_signature"][
            "overlaps_with_hypothesis_ids"
        ] = sorted(overlap_lookup[candidate["hypothesis_id"]])

    selected = [
        item
        for item in hypotheses
        if item["selection_status"] in {"selected_pareto", "protected_wildcard"}
    ]
    branch_seeds = [
        {
            "branch_id": stable_identifier(
                "theory-branch",
                item["hypothesis_id"],
                item["structural_signature"],
            ),
            "hypothesis_id": item["hypothesis_id"],
            "corner_family": item["corner_family"],
            "mechanism_key": item["mechanism_key"],
            "unique_primitives": list(
                item["ontology_delta"]["new_primitives"]
            ),
            "maturation_question": item["maturation_question"],
            "first_theory_actions": [
                item["premortem"]["earliest_decisive_theory_test"],
                (
                    "Articulate a minimal formal object and one "
                    "target-preserving boundary case."
                ),
            ],
            "forbidden_cross_branch_context": item[
                "branch_independence_signature"
            ]["forbidden_cross_branch_context"],
            "structural_signature": item["structural_signature"],
            "genealogy": list(item["genealogy"]),
            "literature_relation": item["literature_relation"],
            "literature_source_ids": list(item["literature_source_ids"]),
            "is_wildcard": item["is_wildcard"],
        }
        for item in selected
    ]
    portfolio: dict[str, Any] = {
        "schema_version": "2.0",
        "portfolio_id": stable_identifier(
            "high-risk-portfolio",
            charter["target_id"],
            charter["theory_state_digest"],
            literature_snapshot["content_digest"],
            normalized_generation_provenance,
            [item["structural_signature"] for item in hypotheses],
        ),
        "target_id": charter["target_id"],
        "theory_state_digest": charter["theory_state_digest"],
        "literature_snapshot_id": literature_snapshot["snapshot_id"],
        "literature_snapshot_digest": literature_snapshot["content_digest"],
        "generation_provenance": normalized_generation_provenance,
        "generation_policy": {
            "requested_count": len(hypotheses),
            "corner_families_required": (
                list(DEFAULT_CORNERS[:6])
                if bool(charter.get("target_supports_six_corners", True))
                else sorted({item["corner_family"] for item in hypotheses})
            ),
            "anchoring_controls": [
                (
                    "Freeze each pre-literature intuition statement before "
                    "source relations are assigned."
                ),
                (
                    "Use literature to sharpen or reframe, never to infer "
                    "novelty from absent matches."
                ),
            ],
            "target_relevance_floor": relevance_floor,
            "target_supports_six_corners": bool(
                charter.get("target_supports_six_corners", True)
            ),
            "fewer_corners_reason": charter.get("fewer_corners_reason"),
            "wildcards_available": wildcards_available,
            "fewer_wildcards_reason": fewer_wildcards_reason,
        },
        "phase_trace": [
            "blind_intuition_first",
            "frontier_literature_rebase",
            "structural_deduplication",
            "relevance_constrained_pareto",
        ],
        "hypotheses": hypotheses,
        "corner_coverage": sorted(
            {
                item["corner_family"]
                for item in hypotheses
                if item["selection_status"] != "structural_duplicate"
            }
        ),
        "pairwise_distinction_matrix": matrix,
        "structural_duplicate_groups": sorted(duplicate_groups),
        "pareto_assessment": [
            {
                "hypothesis_id": item["hypothesis_id"],
                "nondominated": item["hypothesis_id"] in nondominated,
                "dominated_by": sorted(
                    dominated_by.get(item["hypothesis_id"], [])
                ),
                "selection_status": item["selection_status"],
            }
            for item in hypotheses
        ],
        "protected_wildcard_ids": protected_wildcards,
        "control_hypothesis_ids": controls,
        "parallel_branch_seeds": branch_seeds,
        "explicit_unknowns": [
            "Conceptual worth does not establish truth probability.",
            (
                "No-match literature relations are bounded by the frozen query "
                "and provider coverage."
            ),
            "Formal consequences remain open until the maturation question is answered.",
        ],
    }
    portfolio["content_digest"] = canonical_digest(
        _without(portfolio, "content_digest")
    )
    validate_high_risk_portfolio(
        portfolio, literature_snapshot=literature_snapshot
    )
    return portfolio


def validate_high_risk_portfolio(
    portfolio: Mapping[str, Any],
    *,
    literature_snapshot: Mapping[str, Any] | None = None,
) -> None:
    """Enforce conceptual rather than lexical diversity and honest uncertainty."""

    validate_payload(
        dict(portfolio), "high_risk_hypothesis_portfolio.schema.json"
    )
    if portfolio["content_digest"] != canonical_digest(
        _without(portfolio, "content_digest")
    ):
        raise ContractError("high-risk portfolio content digest mismatch")
    if portfolio["schema_version"] == "1.0":
        if "generation_provenance" in portfolio:
            raise ContractError("legacy v1 portfolio cannot be retrofitted with generation provenance")
    else:
        provenance = portfolio["generation_provenance"]
        if provenance["mode"] not in GENERATION_MODES:
            raise ContractError("unsupported high-risk generation mode")
        if provenance["mode"] == "operator_instantiated_from_authored_proposals":
            if provenance["authored_template_reference_digest"] != _AUTHORED_TEMPLATE_REFERENCE_DIGEST:
                raise ContractError("authored portfolio template-reference digest mismatch")
            if provenance["proposal_request_digest"] is not None:
                raise ContractError("authored portfolio cannot claim a provider request")
            if provenance["claim_boundary"] != _AUTHORED_CLAIM_BOUNDARY:
                raise ContractError("authored portfolio claim boundary mismatch")
        elif provenance["authored_template_reference_digest"] is not None:
            raise ContractError("seed-free portfolio cannot cite authored proposals as its source")
        else:
            if provenance["proposal_request_digest"] is None:
                raise ContractError("proposal-field-free portfolio requires a request digest")
            if provenance["claim_boundary"] != _SEED_FREE_CLAIM_BOUNDARY:
                raise ContractError("proposal-field-free portfolio claim boundary mismatch")
    if literature_snapshot is not None:
        validate_snapshot(literature_snapshot)
        if portfolio["target_id"] != literature_snapshot["target_id"]:
            raise ContractError(
                "portfolio target differs from its frozen literature target"
            )
        if (
            portfolio["literature_snapshot_digest"]
            != literature_snapshot["content_digest"]
        ):
            raise ContractError(
                "portfolio does not cite the exact frozen literature digest"
            )
    hypotheses = list(portfolio["hypotheses"])
    if not 8 <= len(hypotheses) <= 12:
        raise ContractError(
            "a major portfolio must contain 8 to 12 articulated candidates"
        )
    active = [
        item
        for item in hypotheses
        if item["selection_status"]
        in {"selected_pareto", "protected_wildcard", "control"}
    ]
    corners = {
        item["corner_family"]
        for item in hypotheses
        if item["selection_status"] != "structural_duplicate"
    }
    if (
        portfolio["generation_policy"]["target_supports_six_corners"]
        and len(corners) < 6
    ):
        raise ContractError(
            "major portfolio lacks six genuine structural corner families"
        )
    if (
        not portfolio["generation_policy"]["target_supports_six_corners"]
        and not portfolio["generation_policy"]["fewer_corners_reason"]
    ):
        raise ContractError(
            "fewer genuine corners requires a target-grounded reason"
        )
    ids = {item["hypothesis_id"] for item in hypotheses}
    if len(ids) != len(hypotheses):
        raise ContractError("hypothesis identifiers must be unique")
    for candidate in hypotheses:
        expected_signature = structural_signature(candidate)
        if candidate["structural_signature"] != expected_signature:
            raise ContractError(
                f"structural signature mismatch for {candidate['hypothesis_id']}"
            )
        expected_blind_digest = blind_articulation_digest(candidate)
        if candidate["blind_articulation_digest"] != expected_blind_digest:
            raise ContractError(
                f"blind articulation digest mismatch for {candidate['hypothesis_id']}"
            )
        rebase_receipt = candidate["literature_rebase_receipt"]
        if (
            rebase_receipt["blind_articulation_digest"]
            != candidate["blind_articulation_digest"]
            or rebase_receipt["snapshot_digest"]
            != portfolio["literature_snapshot_digest"]
            or rebase_receipt["relation"]
            != candidate["literature_relation"]
            or rebase_receipt["source_ids"]
            != candidate["literature_source_ids"]
        ):
            raise ContractError(
                f"literature rebase receipt mismatch for {candidate['hypothesis_id']}"
            )
        text = " ".join(
            [
                candidate["intuitive_leap"],
                candidate["mechanism"],
                candidate["explanatory_upside"],
                candidate["value_if_right"],
            ]
        )
        if MYSTICAL_MARKERS.search(text):
            raise ContractError(
                f"mystical or novelty-theatre candidate rejected: "
                f"{candidate['hypothesis_id']}"
            )
        if (
            not candidate["target_pressures_addressed"]
            or not candidate["target_commitments"]
        ):
            raise ContractError(
                f"target-free candidate rejected: {candidate['hypothesis_id']}"
            )
        if candidate["novelty_claim"]:
            raise ContractError(
                "an absent literature match cannot establish novelty"
            )
        if (
            candidate["literature_relation"] != "coverage_unknown"
            and not candidate["literature_source_ids"]
        ):
            raise ContractError(
                f"uncited literature relation for {candidate['hypothesis_id']}"
            )
        if candidate["literature_relation"] == "pending_rebase":
            raise ContractError(
                f"active candidate was not literature-rebased: "
                f"{candidate['hypothesis_id']}"
            )
        if (
            not candidate["correction_conditions"]
            or not candidate["boundary_case"].strip()
        ):
            raise ContractError(
                f"candidate lacks correction or non-vacuity boundary: "
                f"{candidate['hypothesis_id']}"
            )
    active_signatures = [item["structural_signature"] for item in active]
    if len(active_signatures) != len(set(active_signatures)):
        raise ContractError(
            "structurally equivalent candidates cannot both remain active"
        )
    pareto = {
        item["hypothesis_id"]: item for item in portfolio["pareto_assessment"]
    }
    wildcard_ids = list(portfolio["protected_wildcard_ids"])
    if (
        portfolio["generation_policy"]["wildcards_available"]
        and len(wildcard_ids) < 2
    ):
        raise ContractError(
            "two high-upside, low-confidence wildcards must survive scalar pruning"
        )
    if (
        not portfolio["generation_policy"]["wildcards_available"]
        and not portfolio["generation_policy"]["fewer_wildcards_reason"]
    ):
        raise ContractError(
            "fewer protected wildcards requires a target-grounded reason"
        )
    for hypothesis_id in wildcard_ids:
        candidate = next(
            (
                item
                for item in hypotheses
                if item["hypothesis_id"] == hypothesis_id
            ),
            None,
        )
        if candidate is None or not candidate["is_wildcard"]:
            raise ContractError(
                "protected wildcard ID does not identify an articulated wildcard"
            )
        if not pareto[hypothesis_id]["nondominated"]:
            raise ContractError(
                "protected wildcards must be relevance-constrained and nondominated"
            )
        if (
            candidate["risk_axes"]["probability_of_truth"] > 0.35
            or candidate["quality_axes"]["value_if_true"] < 0.80
        ):
            raise ContractError(
                "wildcard does not keep low confidence and high reward separate"
            )
    controls = set(portfolio["control_hypothesis_ids"])
    if not controls or not controls.issubset(ids):
        raise ContractError("a valid conservative control is required")
    selected_ids = {
        item["hypothesis_id"]
        for item in hypotheses
        if item["selection_status"] in {"selected_pareto", "protected_wildcard"}
    }
    seed_ids = {
        item["hypothesis_id"] for item in portfolio["parallel_branch_seeds"]
    }
    if seed_ids != selected_ids:
        raise ContractError(
            "parallel branch seeds must exactly represent the selected independent portfolio"
        )
    expected_pairs = len(hypotheses) * (len(hypotheses) - 1) // 2
    if len(portfolio["pairwise_distinction_matrix"]) != expected_pairs:
        raise ContractError(
            "pairwise structural overlap matrix is incomplete"
        )


def _content_words(value: str) -> list[str]:
    stop = {
        "about", "after", "again", "also", "because", "before", "between",
        "could", "from", "have", "into", "must", "that", "their", "there",
        "these", "this", "through", "under", "what", "when", "where", "which",
        "while", "with", "without", "would", "target", "theory",
    }
    return [
        token for token in re.findall(r"[a-z][a-z0-9_-]+", value.lower())
        if len(token) >= 4 and token not in stop
    ]


def _known_authored_prompt_seed_audit(prompt_text: str) -> dict[str, Any]:
    """Screen prompt text against the known authored deck without claiming purity."""

    lowered = prompt_text.lower()
    prompt_tokens = set(_content_words(prompt_text))
    exact_matches: list[str] = []
    nearest_similarity = 0.0
    nearest_corner = _TEMPLATES[0]["corner_family"]
    for template in _TEMPLATES:
        for marker_name in ("mechanism_key", "primitive", "relation"):
            marker = str(template[marker_name]).lower()
            if marker in lowered:
                exact_matches.append(f"{template['corner_family']}:{marker_name}")
        template_tokens = set(
            _content_words(
                " ".join(
                    str(template[key])
                    for key in ("leap", "mechanism", "question")
                )
            )
        )
        union = prompt_tokens | template_tokens
        similarity = len(prompt_tokens & template_tokens) / len(union) if union else 1.0
        if similarity > nearest_similarity:
            nearest_similarity = similarity
            nearest_corner = str(template["corner_family"])
    copied = bool(exact_matches) or nearest_similarity >= 0.72
    return {
        "status": "failed" if copied else "passed",
        "known_authored_reference_digest": _AUTHORED_TEMPLATE_REFERENCE_DIGEST,
        "similarity_threshold": 0.72,
        "nearest_authored_corner": nearest_corner,
        "nearest_similarity": round(nearest_similarity, 6),
        "exact_marker_matches": sorted(set(exact_matches)),
        "boundary": (
            "This screen detects only the repository's known authored deck and cannot "
            "establish freedom from unknown or latent proposal influence."
        ),
    }


def _seed_free_protocol_proposals(request: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Procedurally articulate proposals from the sealed prompt and charter.

    This is a deterministic protocol control, not evidence of autonomous
    creativity.  It uses no entry from ``_TEMPLATES`` and receives no proposal
    seeds, expected answers, or adjudication scores.
    """

    charter = request["charter"]
    count = int(request["requested_count"])
    repetition = int(request["repetition_index"])
    corpus = " ".join(
        [
            str(request["hidden_prompt_text"]),
            str(charter["target_statement"]),
            *[str(item) for item in charter["root_tensions"]],
        ]
    )
    words = sorted(set(_content_words(corpus))) or ["structure", "constraint", "relation"]
    proposals: list[dict[str, Any]] = []
    wildcard_indices = {0, 1}
    control_index = count - 1
    pressures = [str(item) for item in charter["root_tensions"]]
    for index in range(count):
        family, operation, primitive_base, relation_base = _SEED_FREE_OPERATORS[
            index % len(_SEED_FREE_OPERATORS)
        ]
        anchor = words[(repetition * 3 + index) % len(words)]
        contrast = words[(repetition * 5 + index + 1) % len(words)]
        primitive = f"{primitive_base}_{anchor}_r{repetition}"
        relation = f"{relation_base}_{contrast}_r{repetition}"
        is_control = index == control_index
        is_wildcard = index in wildcard_indices and not is_control
        mechanism_key = f"elicited-{operation}-{anchor}-{contrast}-r{repetition}-{index}"
        leap = (
            f"{operation.capitalize()} the relation between {anchor} and {contrast} so the "
            "named pressure is represented by an independently correctable structure."
        )
        mechanism = (
            f"The primitive {primitive} acts through {relation}; it preserves the declared "
            f"target commitments while exposing when {anchor} constrains {contrast}."
        )
        boundary = (
            f"The proposal collapses if {primitive} can only be defined by assuming the "
            "target conclusion or erases the protected boundary regime."
        )
        if is_wildcard and index == 0:
            quality = (0.91, 0.98, 0.96, 0.81, 0.98, 0.66, 0.96, 0.26, 0.98, 0.98)
            risk = (0.16, 0.87, 0.82)
        elif is_wildcard:
            quality = (0.92, 0.95, 0.82, 0.98, 0.95, 0.69, 0.94, 0.29, 0.97, 0.98)
            risk = (0.19, 0.83, 0.88)
        elif is_control:
            quality = (0.98, 0.18, 0.44, 0.40, 0.58, 0.92, 0.28, 0.90, 0.60, 0.60)
            risk = (0.62, 0.23, 0.30)
        else:
            quality = (
                0.90,
                0.62 + 0.03 * (index % 4),
                0.70 + 0.02 * (index % 5),
                0.67 + 0.025 * ((index + 2) % 5),
                0.72 + 0.02 * ((index + 1) % 4),
                0.74,
                0.62,
                0.58 + 0.02 * (index % 3),
                0.78,
                0.79,
            )
            risk = (0.37, 0.58 + 0.02 * (index % 3), 0.57 + 0.02 * ((index + 1) % 3))
        proposals.append(
            {
                "corner_family": "conservative_control" if is_control else family,
                "maturation_status": "theory_question_open" if is_control else "parallel_ready",
                "truth_status": "not_assessed",
                "intuition_provenance": {
                    "mode": "blind_intuition_first",
                    "trigger": pressures[index % len(pressures)],
                    "pre_literature_statement": leap,
                },
                "intuitive_leap": f"For {charter['target_statement']}: {leap}",
                "mechanism": mechanism,
                "mechanism_key": mechanism_key,
                "ontology_delta": {
                    "new_primitives": [primitive],
                    "new_relations": [relation],
                    "removed_or_retyped": [] if is_control else [f"incumbent_{anchor}_priority"],
                    "affordance": f"Makes the {anchor}-{contrast} dependency explicit and independently revisable.",
                },
                "target_pressures_addressed": (
                    pressures[:2] if family == "unification_conjecture" else [pressures[index % len(pressures)]]
                ),
                "target_commitments": list(charter["target_commitments"]),
                "protected_successes": list(charter["protected_successes"]),
                "assumptions_or_invariants_risked": [str(charter["forbidden_target_drift"]), boundary],
                "explanatory_upside": f"If right, explain why {anchor} and {contrast} co-vary under one typed mechanism.",
                "unification_upside": f"Unify the {anchor} and {contrast} pressures while retaining their boundary differences.",
                "value_if_right": "Potentially high conceptual value; no truth or efficacy follows from articulation.",
                "learning_value_if_wrong": f"Failure localizes whether {anchor} can constrain {contrast} independently.",
                "risk_axes": {"probability_of_truth": risk[0], "failure_risk": risk[1], "maturation_cost": risk[2]},
                "quality_axes": {
                    "essential_relevance": quality[0],
                    **dict(zip(BENEFIT_AXES, quality[1:], strict=True)),
                },
                "novelty_claim": False,
                "non_claim_boundary": "No literature no-match, generator output, or score establishes novelty or truth.",
                "maturation_question": f"Which target-preserving case distinguishes {relation} from a renamed incumbent dependency?",
                "correction_conditions": [
                    f"Demote if {primitive} is definitionally equivalent to the desired conclusion.",
                    f"Reframe if {relation} preserves no independently stated invariant.",
                    "Retire if the exact target or every protected success changes.",
                ],
                "boundary_case": boundary,
                "premortem": {
                    "failure_signatures": [boundary, "The mechanism is only lexical restatement."],
                    "earliest_decisive_theory_test": f"Define {primitive} before using the target conclusion.",
                    "disposition": "falsifier_sprint" if is_control else ("artifact_sprint" if is_wildcard else "invest"),
                },
                "branch_independence_signature": {
                    "unique_primitives": [primitive],
                    "unique_mechanism": mechanism,
                    "forbidden_cross_branch_context": ["Other elicitation outputs before the blind scoring barrier"],
                    "required_context": ["Frozen charter", "Frozen theory digest", "Frozen literature digest"],
                    "overlaps_with_hypothesis_ids": [],
                },
                "genealogy": [stable_identifier("seed-free-intuition", request["request_digest"], repetition, index)],
                "is_wildcard": is_wildcard,
                "is_control": is_control,
            }
        )
    return proposals


def _resolve_authority(
    callback: Callable[..., Any],
    supplied: Mapping[str, Any] | None,
    *,
    default_id: str,
    default_class: str,
    require_explicit: bool,
) -> dict[str, Any]:
    digest = _callable_digest(callback)
    if supplied is None:
        if require_explicit:
            raise ContractError("custom elicitation callables require explicit authority metadata")
        return {
            "authority_id": default_id,
            "authority_class": default_class,
            "callable_digest": digest,
            "replayability": _EXACT_REPLAYABILITY,
        }
    allowed = {
        "authority_id",
        "authority_class",
        "expected_callable_digest",
        "replayability",
    }
    if not set(supplied).issubset(allowed) or not supplied.get("authority_id") or not supplied.get("authority_class"):
        raise ContractError("callable authority metadata has an invalid strict shape")
    expected = supplied.get("expected_callable_digest")
    if expected is not None and expected != digest:
        raise ContractError("callable authority digest mismatch")
    replayability = supplied.get("replayability", _EXACT_REPLAYABILITY)
    if replayability != _EXACT_REPLAYABILITY:
        raise ContractError(
            "non-replayable elicitation authorities are unsupported and unverifiable"
        )
    return {
        "authority_id": str(supplied["authority_id"]),
        "authority_class": str(supplied["authority_class"]),
        "callable_digest": digest,
        "replayability": _EXACT_REPLAYABILITY,
    }


def _template_copy_control(portfolio: Mapping[str, Any]) -> dict[str, Any]:
    template_texts = [
        _content_words(" ".join(str(item[key]) for key in ("leap", "mechanism", "question")))
        for item in _TEMPLATES
    ]
    rows = []
    for candidate in portfolio["hypotheses"]:
        candidate_tokens = set(
            _content_words(" ".join([candidate["intuitive_leap"], candidate["mechanism"], candidate["maturation_question"]]))
        )
        best_similarity = 0.0
        best_index = 0
        for index, template_tokens in enumerate(template_texts):
            union = candidate_tokens | set(template_tokens)
            similarity = len(candidate_tokens & set(template_tokens)) / len(union) if union else 1.0
            if similarity > best_similarity:
                best_similarity, best_index = similarity, index
        template = _TEMPLATES[best_index]
        primitives = set(candidate["ontology_delta"]["new_primitives"])
        relations = set(candidate["ontology_delta"]["new_relations"])
        exact_mechanism = candidate["mechanism_key"] == template["mechanism_key"]
        exact_structure = template["primitive"] in primitives and template["relation"] in relations
        copied = exact_mechanism or exact_structure or best_similarity >= 0.72
        rows.append(
            {
                "hypothesis_id": candidate["hypothesis_id"],
                "candidate_digest": candidate["blind_articulation_digest"],
                "nearest_authored_corner": template["corner_family"],
                "nearest_similarity": round(best_similarity, 6),
                "exact_mechanism_key": exact_mechanism,
                "exact_primitive_relation": exact_structure,
                "copy_detected": copied,
            }
        )
    return {
        "authored_template_reference_digest": _AUTHORED_TEMPLATE_REFERENCE_DIGEST,
        "similarity_threshold": 0.72,
        "status": "failed" if any(row["copy_detected"] for row in rows) else "passed",
        "candidate_results": rows,
    }


def _blind_candidate_content(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "intuitive_leap": candidate["intuitive_leap"],
        "mechanism": candidate["mechanism"],
        "ontology_delta": candidate["ontology_delta"],
        "target_pressures_addressed": candidate["target_pressures_addressed"],
        "target_commitments": candidate["target_commitments"],
        "protected_successes": candidate["protected_successes"],
        "explanatory_upside": candidate["explanatory_upside"],
        "unification_upside": candidate["unification_upside"],
        "maturation_question": candidate["maturation_question"],
        "correction_conditions": candidate["correction_conditions"],
        "boundary_case": candidate["boundary_case"],
    }


def _deterministic_content_adjudicator(request: Mapping[str, Any]) -> dict[str, Any]:
    target_words = set(_content_words(" ".join(request["evaluation_context"]["target_text"])))
    mechanisms = [row["content"]["mechanism"] for row in request["candidates"]]
    primitives = [tuple(row["content"]["ontology_delta"]["new_primitives"]) for row in request["candidates"]]
    ratings = []
    for row in request["candidates"]:
        content = row["content"]
        text = " ".join(str(value) for value in [content["intuitive_leap"], content["mechanism"], content["explanatory_upside"]])
        words = set(_content_words(text))
        overlap = len(words & target_words) / max(1, min(len(target_words), 12))
        relevance = min(0.99, 0.42 + 0.38 * overlap + (0.16 if content["target_pressures_addressed"] else 0.0))
        causal = any(marker in text.lower() for marker in ("through", "when", "constrain", "preserve", "because"))
        depth = min(0.99, 0.42 + 0.14 * len(content["ontology_delta"]["new_primitives"]) + 0.14 * len(content["ontology_delta"]["new_relations"]) + (0.18 if causal else 0.0) + (0.08 if content["maturation_question"] else 0.0))
        unification = min(0.99, 0.34 + 0.18 * min(2, len(content["target_pressures_addressed"])) + (0.22 if "unif" in content["unification_upside"].lower() else 0.0) + (0.14 if "differ" in content["unification_upside"].lower() else 0.0))
        mechanism_unique = mechanisms.count(content["mechanism"]) == 1
        primitive_unique = primitives.count(tuple(content["ontology_delta"]["new_primitives"])) == 1
        diversity = 0.94 if mechanism_unique and primitive_unique else (0.58 if mechanism_unique or primitive_unique else 0.20)
        corrections = content["correction_conditions"]
        specificity = min(0.99, 0.30 + 0.12 * min(4, len(corrections)) + (0.16 if any("if" in item.lower() for item in corrections) else 0.0) + (0.15 if content["boundary_case"] else 0.0))
        scores = {
            "essential_relevance": round(relevance, 6),
            "conceptual_depth": round(depth, 6),
            "unification": round(unification, 6),
            "corner_diversity": round(diversity, 6),
            "correction_specificity": round(specificity, 6),
        }
        ratings.append(
            {
                "candidate_alias": row["candidate_alias"],
                "scores": scores,
                "warrants": {
                    "essential_relevance": ["target_pressures_addressed", canonical_digest(content["target_pressures_addressed"])],
                    "conceptual_depth": ["mechanism+ontology_delta+maturation_question", canonical_digest([content["mechanism"], content["ontology_delta"], content["maturation_question"]])],
                    "unification": ["unification_upside+target_pressures_addressed", canonical_digest([content["unification_upside"], content["target_pressures_addressed"]])],
                    "corner_diversity": ["set-relative mechanism+primitive uniqueness", canonical_digest([content["mechanism"], content["ontology_delta"]["new_primitives"]])],
                    "correction_specificity": ["correction_conditions+boundary_case", canonical_digest([corrections, content["boundary_case"]])],
                },
            }
        )
    return {"ratings": ratings}


def _validate_adjudication_response(response: Mapping[str, Any], aliases: Sequence[str]) -> None:
    if set(response) != {"ratings"} or not isinstance(response["ratings"], list):
        raise ContractError("adjudicator response must contain only ratings")
    observed_aliases = [row.get("candidate_alias") for row in response["ratings"]]
    if len(observed_aliases) != len(aliases) or len(set(observed_aliases)) != len(aliases):
        raise ContractError("adjudicator must return exactly one rating per blind candidate")
    if set(observed_aliases) != set(aliases):
        raise ContractError("adjudicator response aliases differ from blind candidates")
    for row in response["ratings"]:
        if set(row) != {"candidate_alias", "scores", "warrants"}:
            raise ContractError("adjudicator rating has an invalid strict shape")
        if set(row["scores"]) != set(ELICITATION_DIMENSIONS) or set(row["warrants"]) != set(ELICITATION_DIMENSIONS):
            raise ContractError("adjudicator must score and warrant all five distinct dimensions")
        if any(
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= float(score) <= 1
            for score in row["scores"].values()
        ):
            raise ContractError("adjudication scores must be bounded in [0,1]")
        for warrant in row["warrants"].values():
            if (
                not isinstance(warrant, (list, tuple))
                or len(warrant) != 2
                or not isinstance(warrant[0], str)
                or not warrant[0]
                or not isinstance(warrant[1], str)
                or not re.fullmatch(r"sha256:[a-f0-9]{64}", warrant[1])
            ):
                raise ContractError(
                    "every adjudication dimension needs a typed content-digest warrant"
                )


def _normalize_provider_output(response: Any) -> dict[str, Any]:
    """Normalize the two supported JSON callback shapes without dropping fields."""

    if isinstance(response, Mapping):
        if set(response) != {"proposals"}:
            raise ContractError("provider object response must contain only proposals")
        raw_proposals = response["proposals"]
        response_shape = "proposals_object"
    elif isinstance(response, Sequence) and not isinstance(response, (str, bytes, bytearray)):
        raw_proposals = response
        response_shape = "proposal_sequence"
    else:
        raise ContractError("high-risk provider must return a proposal sequence or strict object")
    if not isinstance(raw_proposals, Sequence) or isinstance(
        raw_proposals, (str, bytes, bytearray)
    ):
        raise ContractError("high-risk provider proposals must be a sequence")
    proposals = [copy.deepcopy(dict(item)) for item in raw_proposals if isinstance(item, Mapping)]
    if len(proposals) != len(raw_proposals):
        raise ContractError("high-risk provider must return proposal objects")
    canonical_response: Any = (
        {"proposals": proposals} if response_shape == "proposals_object" else proposals
    )
    return {
        "response_shape": response_shape,
        "proposals": proposals,
        "proposal_digest": canonical_digest(proposals),
        "raw_response_digest": canonical_digest(canonical_response),
    }


def _prompt_seal(prompt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "prompt_id": prompt["prompt_id"],
        "prompt_content_digest": prompt["content_digest"],
        "hidden_prompt_digest": canonical_digest(prompt["prompt_text"]),
        "known_authored_seed_audit": _known_authored_prompt_seed_audit(
            str(prompt["prompt_text"])
        ),
    }


def _scheduled_prompt(
    prompts: Sequence[Mapping[str, Any]], seed_digest: str, repetition_index: int
) -> Mapping[str, Any]:
    ordered = sorted(prompts, key=lambda item: item["content_digest"])
    offset = int(seed_digest.removeprefix("sha256:")[:8], 16) % len(ordered)
    return ordered[(offset + repetition_index) % len(ordered)]


def _build_provider_request(
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    prompt: Mapping[str, Any],
    repetition_index: int,
    requested_count: int,
) -> dict[str, Any]:
    request = {
        "schema_version": "1.0",
        "target_id": charter["target_id"],
        "theory_state_digest": charter["theory_state_digest"],
        "literature_snapshot_id": snapshot["snapshot_id"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "prompt_id": prompt["prompt_id"],
        "hidden_prompt_digest": canonical_digest(prompt["prompt_text"]),
        "hidden_prompt_text": prompt["prompt_text"],
        "charter": copy.deepcopy(dict(charter)),
        "repetition_index": repetition_index,
        "requested_count": requested_count,
        "proposal_seed_status": "absent",
        "expected_answer_status": "withheld",
        "adjudication_rubric_status": "withheld",
    }
    request["request_digest"] = canonical_digest(_without(request, "request_digest"))
    return request


def _build_blind_request(
    portfolio: Mapping[str, Any],
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    seed_digest: str,
    repetition_index: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    blind_rows: list[dict[str, Any]] = []
    alias_resolution: list[dict[str, Any]] = []
    for candidate in portfolio["hypotheses"]:
        content = _blind_candidate_content(candidate)
        content_digest = canonical_digest(content)
        alias = stable_identifier(
            "candidate",
            seed_digest,
            repetition_index,
            candidate["hypothesis_id"],
            content_digest,
        )
        blind_rows.append({"candidate_alias": alias, "content": content})
        alias_resolution.append(
            {
                "candidate_alias": alias,
                "hypothesis_id": candidate["hypothesis_id"],
                "content_digest": content_digest,
            }
        )
    if len({row["candidate_alias"] for row in blind_rows}) != len(blind_rows):
        raise ContractError("blind candidate aliases must be unique")
    blind_rows.sort(
        key=lambda row: canonical_digest(
            [seed_digest, repetition_index, row["candidate_alias"]]
        )
    )
    request = {
        "schema_version": "1.0",
        "evaluation_context": {
            "target_id": charter["target_id"],
            "theory_state_digest": charter["theory_state_digest"],
            "literature_snapshot_digest": snapshot["content_digest"],
            "target_text": [
                str(charter["target_statement"]),
                *[str(item) for item in charter["root_tensions"]],
                *[str(item) for item in charter["target_commitments"]],
            ],
            "generator_identity_status": "withheld",
            "prompt_text_status": "withheld",
            "self_scores_status": "withheld",
        },
        "counterbalanced_alias_order": [row["candidate_alias"] for row in blind_rows],
        "candidates": blind_rows,
    }
    request["request_digest"] = canonical_digest(_without(request, "request_digest"))
    return request, sorted(alias_resolution, key=lambda row: row["candidate_alias"])


def _dimension_means(ratings: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    return {
        dimension: round(
            sum(float(row["scores"][dimension]) for row in ratings) / len(ratings),
            6,
        )
        for dimension in ELICITATION_DIMENSIONS
    }


def semantic_hypothesis_signature(candidate: Mapping[str, Any]) -> str:
    """Hash semantic content after removing repetition-only naming markers."""

    def normalized(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {key: normalized(child) for key, child in sorted(value.items())}
        if isinstance(value, (list, tuple)):
            return [normalized(child) for child in value]
        if isinstance(value, str):
            text = value.lower()
            text = re.sub(r"(?:(?<=_)r|(?<=-)r)\d+\b", "", text)
            return " ".join(text.split())
        return value

    return canonical_digest(
        normalized(
            {
                "corner_family": candidate["corner_family"],
                "mechanism": candidate["mechanism"],
                "ontology_delta": candidate["ontology_delta"],
                "target_pressures_addressed": candidate["target_pressures_addressed"],
                "explanatory_upside": candidate["explanatory_upside"],
                "unification_upside": candidate["unification_upside"],
                "maturation_question": candidate["maturation_question"],
                "correction_conditions": candidate["correction_conditions"],
                "boundary_case": candidate["boundary_case"],
            }
        )
    )


def _diversity_report(repetitions: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    nominal_decks = [
        sorted(item["structural_signature"] for item in repetition["portfolio"]["hypotheses"])
        for repetition in repetitions
    ]
    semantic_decks = [
        sorted(
            semantic_hypothesis_signature(item)
            for item in repetition["portfolio"]["hypotheses"]
        )
        for repetition in repetitions
    ]
    deck_digests = [canonical_digest(deck) for deck in nominal_decks]
    semantic_deck_digests = [canonical_digest(deck) for deck in semantic_decks]
    overlaps = []
    for left, right in itertools.combinations(range(len(nominal_decks)), 2):
        left_nominal, right_nominal = set(nominal_decks[left]), set(nominal_decks[right])
        nominal_union = left_nominal | right_nominal
        left_semantic, right_semantic = set(semantic_decks[left]), set(semantic_decks[right])
        semantic_union = left_semantic | right_semantic
        overlaps.append(
            {
                "left_repetition": left,
                "right_repetition": right,
                "structural_signature_jaccard": round(
                    len(left_nominal & right_nominal) / len(nominal_union)
                    if nominal_union
                    else 1.0,
                    6,
                ),
                "semantic_signature_jaccard": round(
                    len(left_semantic & right_semantic) / len(semantic_union)
                    if semantic_union
                    else 1.0,
                    6,
                ),
            }
        )
    unique_signatures = len(set(itertools.chain.from_iterable(nominal_decks)))
    unique_semantic_signatures = len(set(itertools.chain.from_iterable(semantic_decks)))
    corner_counts = [
        len({item["corner_family"] for item in row["portfolio"]["hypotheses"]})
        for row in repetitions
    ]
    corner_requirements = [
        6 if row["portfolio"]["generation_policy"]["target_supports_six_corners"] else 1
        for row in repetitions
    ]
    passed = (
        len(repetitions) >= 5
        and len(set(semantic_deck_digests)) == len(semantic_decks)
        and unique_semantic_signatures > len(semantic_decks[0])
        and all(actual >= required for actual, required in zip(corner_counts, corner_requirements, strict=True))
    )
    return {
        "status": "passed" if passed else "failed",
        "basis": "repetition_invariant_semantic_content_without_run_markers_or_genealogy",
        "repetition_count": len(nominal_decks),
        "unique_deck_count": len(set(deck_digests)),
        "unique_semantic_deck_count": len(set(semantic_deck_digests)),
        "unique_structural_signature_count": unique_signatures,
        "unique_semantic_signature_count": unique_semantic_signatures,
        "deck_digests": deck_digests,
        "semantic_deck_digests": semantic_deck_digests,
        "corner_family_counts": corner_counts,
        "pairwise_repetition_overlap": overlaps,
        "claim_boundary": (
            "Passing establishes repetition-invariant protocol differentiation only; "
            "it does not establish creativity, novelty, depth, or external value."
        ),
    }


def _study_eligibility(controls_pass: bool) -> dict[str, str]:
    internal = "eligible_internal_only" if controls_pass else "withheld_failed_controls"
    return {
        "internal_exploration": internal,
        "internal_refinement": internal,
        "theorem_investment": "requires_distinct_formal_evidence",
        "physics_investment": "requires_distinct_domain_evidence",
        "efficacy_claim": "not_authorized",
        "authority_basis": "internal_protocol_controls_only",
    }


def _build_elicitation_repetition(
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    prompts: Sequence[Mapping[str, Any]],
    seed_digest: str,
    repetition_index: int,
    requested_count: int,
    generation_mode: str,
    generation_callback: HighRiskProvider,
    generator_authority: Mapping[str, Any],
    adjudication_callback: HighRiskAdjudicator,
    adjudicator_authority: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one complete repetition from exact replayable callback results."""

    prompt = _scheduled_prompt(prompts, seed_digest, repetition_index)
    request = _build_provider_request(
        charter=charter,
        snapshot=snapshot,
        prompt=prompt,
        repetition_index=repetition_index,
        requested_count=requested_count,
    )
    provider_output = _normalize_provider_output(
        generation_callback(copy.deepcopy(request))
    )
    proposals = provider_output["proposals"]
    if len(proposals) != requested_count:
        raise ContractError("provider proposal count differs from the sealed request")
    provenance = {
        "mode": generation_mode,
        "generator_authority_id": generator_authority["authority_id"],
        "generator_authority_digest": generator_authority["callable_digest"],
        "proposal_request_digest": request["request_digest"],
        "source_proposals_digest": provider_output["proposal_digest"],
        "authored_template_reference_digest": None,
        "claim_boundary": _SEED_FREE_CLAIM_BOUNDARY,
    }
    portfolio = forge_high_risk_portfolio(
        charter,
        snapshot,
        proposals=proposals,
        requested_count=requested_count,
        generation_provenance=provenance,
    )
    copy_control = _template_copy_control(portfolio)
    blind_request, alias_resolution = _build_blind_request(
        portfolio,
        charter=charter,
        snapshot=snapshot,
        seed_digest=seed_digest,
        repetition_index=repetition_index,
    )
    response = adjudication_callback(copy.deepcopy(blind_request))
    if not isinstance(response, Mapping):
        raise ContractError("adjudicator must return an object")
    adjudication_response = copy.deepcopy(dict(response))
    _validate_adjudication_response(
        adjudication_response, blind_request["counterbalanced_alias_order"]
    )
    repetition: dict[str, Any] = {
        "repetition_id": stable_identifier(
            "elicitation-repetition",
            request["request_digest"],
            provider_output["proposal_digest"],
        ),
        "repetition_index": repetition_index,
        "prompt_seal": _prompt_seal(prompt),
        "provider_receipt": {
            **copy.deepcopy(dict(generator_authority)),
            "request_digest": request["request_digest"],
            "output_digest": provider_output["proposal_digest"],
            "raw_response_digest": provider_output["raw_response_digest"],
            "status": "completed",
        },
        "provider_output": provider_output,
        "provider_output_seal": {
            "proposal_count": len(proposals),
            "proposal_digest": provider_output["proposal_digest"],
            "raw_response_digest": provider_output["raw_response_digest"],
            "sealed_before_adjudication": True,
        },
        "portfolio": portfolio,
        "authored_template_copy_control": copy_control,
        "blind_adjudication": {
            "authority": copy.deepcopy(dict(adjudicator_authority)),
            "request_digest": blind_request["request_digest"],
            "response_digest": canonical_digest(adjudication_response),
            "counterbalanced_alias_order": blind_request[
                "counterbalanced_alias_order"
            ],
            "alias_resolution": alias_resolution,
            "ratings": adjudication_response["ratings"],
            "dimension_means": _dimension_means(
                adjudication_response["ratings"]
            ),
            "authority_boundary": _ADJUDICATION_AUTHORITY_BOUNDARY,
        },
    }
    repetition["content_digest"] = canonical_digest(
        _without(repetition, "content_digest")
    )
    return repetition


def _assemble_elicitation_study(
    *,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    prompts: Sequence[Mapping[str, Any]],
    repetitions: Sequence[Mapping[str, Any]],
    requested_count: int,
    seed_digest: str,
    generation_mode: str,
    generator_authority: Mapping[str, Any],
    adjudicator_authority: Mapping[str, Any],
) -> dict[str, Any]:
    diversity = _diversity_report(repetitions)
    controls_pass = diversity["status"] == "passed" and all(
        row["authored_template_copy_control"]["status"] == "passed"
        for row in repetitions
    )
    prompt_seals = [
        {
            "prompt_id": prompt["prompt_id"],
            "target_id": prompt["target_id"],
            "theory_state_digest": prompt["theory_state_digest"],
            "literature_snapshot_digest": prompt["literature_snapshot_digest"],
            **_prompt_seal(prompt),
        }
        for prompt in sorted(prompts, key=lambda item: item["prompt_id"])
    ]
    study: dict[str, Any] = {
        "schema_version": "1.0",
        "study_id": stable_identifier(
            "seed-free-high-risk-study",
            charter["target_id"],
            snapshot["content_digest"],
            seed_digest,
            [row["content_digest"] for row in repetitions],
        ),
        "target_id": charter["target_id"],
        "theory_state_digest": charter["theory_state_digest"],
        "literature_snapshot_id": snapshot["snapshot_id"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "generation_mode": generation_mode,
        "generator_authority": copy.deepcopy(dict(generator_authority)),
        "adjudicator_authority": copy.deepcopy(dict(adjudicator_authority)),
        "authority_separation": "logical_and_executable_authority_distinct_internal_correlation_disclosed",
        "protocol": {
            "repetitions": len(repetitions),
            "requested_count": requested_count,
            "counterbalance_seed_digest": seed_digest,
            "proposal_seed_status": "absent",
            "seed_freedom_boundary": _SEED_FREEDOM_BOUNDARY,
            "hidden_prompt_count": len(prompts),
            "authored_template_reference_digest": _AUTHORED_TEMPLATE_REFERENCE_DIGEST,
            "dimensions": list(ELICITATION_DIMENSIONS),
            "callback_replay_requirement": _EXACT_REPLAYABILITY,
        },
        "hidden_prompt_seals": prompt_seals,
        "repetitions": [copy.deepcopy(dict(row)) for row in repetitions],
        "repeated_diversity": diversity,
        "study_status": (
            "protocol_completed"
            if controls_pass
            else "protocol_completed_with_failed_controls"
        ),
        "eligibility": _study_eligibility(controls_pass),
        "external_human_evidence": copy.deepcopy(_EXTERNAL_HUMAN_NULL),
        "claim_boundary": _STUDY_CLAIM_BOUNDARY,
    }
    study["content_digest"] = canonical_digest(_without(study, "content_digest"))
    return study


def run_seed_free_high_risk_elicitation(
    charter: Mapping[str, Any],
    literature_snapshot: Mapping[str, Any],
    *,
    hidden_prompts: Sequence[Mapping[str, Any]],
    repetitions: int = 5,
    requested_count: int = 10,
    counterbalance_seed: str = "high-risk-counterbalance-v1",
    provider: HighRiskProvider | None = None,
    provider_authority: Mapping[str, Any] | None = None,
    adjudicator: HighRiskAdjudicator | None = None,
    adjudicator_authority: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run repeated proposal-field-free elicitation and blind internal scoring."""

    validate_snapshot(literature_snapshot)
    if repetitions < 5:
        raise ContractError("seed-free elicitation requires at least five repetitions")
    if not 8 <= requested_count <= 12 or not hidden_prompts:
        raise ContractError("elicitation requires 8-12 proposals and at least one hidden prompt")
    if not isinstance(counterbalance_seed, str) or not counterbalance_seed:
        raise ContractError("counterbalance seed must be a non-empty string")
    prompts = [copy.deepcopy(dict(item)) for item in hidden_prompts]
    for prompt in prompts:
        _validate_hidden_prompt(prompt, charter=charter, snapshot=literature_snapshot)
        if _known_authored_prompt_seed_audit(str(prompt["prompt_text"]))["status"] != "passed":
            raise ContractError("hidden prompt failed the known-authored proposal-seed screen")
    if len({item["prompt_id"] for item in prompts}) != len(prompts):
        raise ContractError("hidden prompt identifiers must be unique")
    generation_callback = provider or _seed_free_protocol_proposals
    generation_mode = "seed_free_provider" if provider is not None else "seed_free_deterministic"
    provider_receipt = _resolve_authority(
        generation_callback,
        provider_authority,
        default_id="high-risk.seed-free-protocol-generator.v1",
        default_class="deterministic_internal_protocol",
        require_explicit=provider is not None,
    )
    adjudication_callback = adjudicator or _deterministic_content_adjudicator
    adjudicator_receipt = _resolve_authority(
        adjudication_callback,
        adjudicator_authority,
        default_id="high-risk.blind-content-adjudicator.v1",
        default_class="internal_correlated_content_protocol",
        require_explicit=adjudicator is not None,
    )
    if provider_receipt["authority_id"] == adjudicator_receipt["authority_id"]:
        raise ContractError("generator and adjudicator authority IDs must be distinct")
    if provider_receipt["callable_digest"] == adjudicator_receipt["callable_digest"]:
        raise ContractError("generator and adjudicator executable authorities must be distinct")
    seed_digest = canonical_digest(counterbalance_seed)
    repetition_packets = [
        _build_elicitation_repetition(
            charter=charter,
            snapshot=literature_snapshot,
            prompts=prompts,
            seed_digest=seed_digest,
            repetition_index=repetition_index,
            requested_count=requested_count,
            generation_mode=generation_mode,
            generation_callback=generation_callback,
            generator_authority=provider_receipt,
            adjudication_callback=adjudication_callback,
            adjudicator_authority=adjudicator_receipt,
        )
        for repetition_index in range(repetitions)
    ]
    study = _assemble_elicitation_study(
        charter=charter,
        snapshot=literature_snapshot,
        prompts=prompts,
        repetitions=repetition_packets,
        requested_count=requested_count,
        seed_digest=seed_digest,
        generation_mode=generation_mode,
        generator_authority=provider_receipt,
        adjudicator_authority=adjudicator_receipt,
    )
    validate_seed_free_high_risk_elicitation(
        study,
        charter=charter,
        literature_snapshot=literature_snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=counterbalance_seed,
        provider=provider,
        provider_authority=provider_authority,
        adjudicator=adjudicator,
        adjudicator_authority=adjudicator_authority,
    )
    return study


def validate_seed_free_high_risk_elicitation(
    study: Mapping[str, Any],
    *,
    charter: Mapping[str, Any],
    literature_snapshot: Mapping[str, Any],
    hidden_prompts: Sequence[Mapping[str, Any]],
    counterbalance_seed: str = "high-risk-counterbalance-v1",
    provider: HighRiskProvider | None = None,
    provider_authority: Mapping[str, Any] | None = None,
    adjudicator: HighRiskAdjudicator | None = None,
    adjudicator_authority: Mapping[str, Any] | None = None,
) -> None:
    """Rebuild the study from replayable callbacks and require exact equality."""

    validate_payload(dict(study), "seed_free_high_risk_elicitation.schema.json")
    validate_snapshot(literature_snapshot)
    if study["content_digest"] != canonical_digest(_without(study, "content_digest")):
        raise ContractError("seed-free high-risk study digest mismatch")
    if not isinstance(counterbalance_seed, str) or not counterbalance_seed:
        raise ContractError("counterbalance seed must be a non-empty string")
    if study["target_id"] != charter["target_id"] or study["target_id"] != literature_snapshot["target_id"]:
        raise ContractError("seed-free high-risk study target mismatch")
    if study["theory_state_digest"] != charter["theory_state_digest"] or study["literature_snapshot_digest"] != literature_snapshot["content_digest"]:
        raise ContractError("seed-free high-risk study state or literature digest mismatch")
    prompts = [copy.deepcopy(dict(item)) for item in hidden_prompts]
    if not prompts or len({item["prompt_id"] for item in prompts}) != len(prompts):
        raise ContractError("hidden prompt identifiers must be non-empty and unique")
    for prompt in prompts:
        _validate_hidden_prompt(prompt, charter=charter, snapshot=literature_snapshot)
        if _known_authored_prompt_seed_audit(str(prompt["prompt_text"]))["status"] != "passed":
            raise ContractError("hidden prompt failed the known-authored proposal-seed screen")
    generation_callback = provider or _seed_free_protocol_proposals
    adjudication_callback = adjudicator or _deterministic_content_adjudicator
    expected_generator = _resolve_authority(
        generation_callback,
        provider_authority,
        default_id="high-risk.seed-free-protocol-generator.v1",
        default_class="deterministic_internal_protocol",
        require_explicit=provider is not None,
    )
    expected_adjudicator = _resolve_authority(
        adjudication_callback,
        adjudicator_authority,
        default_id="high-risk.blind-content-adjudicator.v1",
        default_class="internal_correlated_content_protocol",
        require_explicit=adjudicator is not None,
    )
    if (
        expected_generator["authority_id"] == expected_adjudicator["authority_id"]
        or expected_generator["callable_digest"]
        == expected_adjudicator["callable_digest"]
    ):
        raise ContractError("generator and adjudicator executable authorities must be distinct")
    if study["generator_authority"] != expected_generator:
        raise ContractError("study generator authority metadata mismatch")
    if study["adjudicator_authority"] != expected_adjudicator:
        raise ContractError("study adjudicator authority metadata mismatch")
    expected_mode = "seed_free_provider" if provider is not None else "seed_free_deterministic"
    if study["generation_mode"] != expected_mode:
        raise ContractError("study generation mode differs from supplied callback mode")
    if len(study["repetitions"]) < 5 or study["protocol"]["repetitions"] != len(study["repetitions"]):
        raise ContractError("study does not contain the required repeated executions")
    if [row["repetition_index"] for row in study["repetitions"]] != list(
        range(len(study["repetitions"]))
    ):
        raise ContractError("repetition indices must be unique, ordered, and contiguous")
    seed_digest = canonical_digest(counterbalance_seed)
    expected_repetitions = []
    for index, actual in enumerate(study["repetitions"]):
        expected = _build_elicitation_repetition(
            charter=charter,
            snapshot=literature_snapshot,
            prompts=prompts,
            seed_digest=seed_digest,
            repetition_index=index,
            requested_count=study["protocol"]["requested_count"],
            generation_mode=expected_mode,
            generation_callback=generation_callback,
            generator_authority=expected_generator,
            adjudication_callback=adjudication_callback,
            adjudicator_authority=expected_adjudicator,
        )
        if actual["prompt_seal"] != expected["prompt_seal"]:
            raise ContractError("repetition prompt seal or schedule mismatch")
        if actual["provider_output"] != expected["provider_output"]:
            raise ContractError("provider output differs from exact callback replay")
        if actual["provider_output_seal"] != expected["provider_output_seal"]:
            raise ContractError("provider output seal differs from exact callback replay")
        if actual["provider_receipt"] != expected["provider_receipt"]:
            raise ContractError("provider receipt differs from exact authority-bound replay")
        if actual["portfolio"] != expected["portfolio"]:
            raise ContractError("portfolio differs from the replayed provider proposal deck")
        if actual["blind_adjudication"] != expected["blind_adjudication"]:
            raise ContractError("blind adjudication differs from exact callback replay")
        if actual != expected:
            raise ContractError("elicitation repetition differs from exact callback replay")
        expected_repetitions.append(expected)
    expected_study = _assemble_elicitation_study(
        charter=charter,
        snapshot=literature_snapshot,
        prompts=prompts,
        repetitions=expected_repetitions,
        requested_count=study["protocol"]["requested_count"],
        seed_digest=seed_digest,
        generation_mode=expected_mode,
        generator_authority=expected_generator,
        adjudicator_authority=expected_adjudicator,
    )
    if study["hidden_prompt_seals"] != expected_study["hidden_prompt_seals"]:
        raise ContractError("hidden prompt seals differ from supplied prompt contents")
    if study["protocol"] != expected_study["protocol"]:
        raise ContractError("elicitation protocol fields differ from exact replay")
    if study["repeated_diversity"] != expected_study["repeated_diversity"]:
        raise ContractError("cross-repetition diversity report does not recompute")
    if study["study_status"] != expected_study["study_status"]:
        raise ContractError("study status differs from recomputed control outcomes")
    if study["eligibility"] != expected_study["eligibility"]:
        raise ContractError("study eligibility exceeds recomputed internal authority")
    if study["external_human_evidence"] != _EXTERNAL_HUMAN_NULL:
        raise ContractError("external-human evidence must remain an honest typed null")
    if study["claim_boundary"] != _STUDY_CLAIM_BOUNDARY:
        raise ContractError("study claim boundary mismatch")
    if dict(study) != expected_study:
        raise ContractError("study differs from exact replayable protocol construction")


def replay_seed_free_high_risk_elicitation(
    study: Mapping[str, Any],
    charter: Mapping[str, Any],
    literature_snapshot: Mapping[str, Any],
    *,
    hidden_prompts: Sequence[Mapping[str, Any]],
    counterbalance_seed: str,
    provider: HighRiskProvider | None = None,
    provider_authority: Mapping[str, Any] | None = None,
    adjudicator: HighRiskAdjudicator | None = None,
    adjudicator_authority: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    replayed = run_seed_free_high_risk_elicitation(
        charter,
        literature_snapshot,
        hidden_prompts=hidden_prompts,
        repetitions=study["protocol"]["repetitions"],
        requested_count=study["protocol"]["requested_count"],
        counterbalance_seed=counterbalance_seed,
        provider=provider,
        provider_authority=provider_authority,
        adjudicator=adjudicator,
        adjudicator_authority=adjudicator_authority,
    )
    return {
        "same_seed_exact_replay": dict(study) == replayed,
        "expected_study_digest": study["content_digest"],
        "replayed_study_digest": replayed["content_digest"],
    }


def build_demo_high_risk_portfolio(
    literature_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct a complete local-only portfolio for validator self-checks."""

    snapshot = (
        copy.deepcopy(dict(literature_snapshot))
        if literature_snapshot is not None
        else build_demo_literature_snapshot(target_id="demo-target")
    )
    return forge_high_risk_portfolio(
        {
            "target_id": snapshot["target_id"],
            "target_statement": (
                "Explain the exact target pressure without replacing it by an "
                "easier proxy."
            ),
            "theory_state_digest": snapshot["theory_state_digest"],
            "root_tensions": [
                "Local witnesses do not yet explain global structure.",
                "Several recurrent failures lack a unified mechanism.",
            ],
            "target_commitments": [
                "Preserve the target statement, quantifiers, and nontriviality."
            ],
            "protected_successes": [
                "Recover the incumbent theory in its verified boundary regime."
            ],
            "forbidden_target_drift": (
                "Do not substitute a lexical, average-case, or finite-only proxy."
            ),
        },
        snapshot,
    )


__all__ = [
    "DEFAULT_CORNERS",
    "ELICITATION_DIMENSIONS",
    "GENERATION_MODES",
    "blind_articulation_digest",
    "build_hidden_elicitation_prompt",
    "build_demo_high_risk_portfolio",
    "forge_high_risk_portfolio",
    "replay_seed_free_high_risk_elicitation",
    "run_seed_free_high_risk_elicitation",
    "semantic_hypothesis_signature",
    "structural_signature",
    "validate_high_risk_portfolio",
    "validate_seed_free_high_risk_elicitation",
]
