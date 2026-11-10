#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Target-specific discovery profile metadata.

The profiles keep long-horizon runs from silently importing the language,
barriers, and success criteria of another target.
"""

from __future__ import annotations

from typing import Any


DEFAULT_TARGET_ID = "yang-mills-existence-and-mass-gap-target"


TARGET_PROFILES: dict[str, dict[str, Any]] = {
    "yang-mills-existence-and-mass-gap-target": {
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "slug": "yang-mills-existence-and-mass-gap",
        "display_name": "Yang-Mills existence and mass gap",
        "domain": "mathematical physics",
        "strategy_tab_label": "Physics & Maths Strategy",
        "story_tab_label": "Physics Story",
        "branch_prompt_header": "You are running one branch of Abducer's Yang-Mills discovery marathon.",
        "work_standard": (
            "The work must be substantive mathematical-physics discovery work: sharpen bridge lemmas, state definitions and "
            "assumptions, expose equations with validity conditions, attempt derivations, name blocking gaps, add falsifiers, "
            "preserve the Clay target commitments, and say whether the local mathematics changes a physical carrier or remains "
            "support-only pending a physical handoff."
        ),
        "definition_prefixes": [
            "source object:",
            "target object:",
            "controlled interface:",
            "same-theory condition:",
        ],
        "validity_examples": [
            "Valid when the reflected Wilson observables...",
            "Applies after diagonal normalization...",
            "Requires the same-theory boundary OPE...",
        ],
        "consistency_markers": ["same-theory"],
        "decisive_target_invariant": (
            "Current decisive target invariant: do not merely restate the Wilson/OS obstruction ladder or the imported "
            "representational-dynamics programme. The cycle must aim at one contribution-making move: (1) prove a finite "
            "Route A theorem, compute the concrete H,K Wilson collar/hairpin case, or bound the post-H,K R/kappa_4 endpoint term; "
            "(2) advance a representational-dynamics frontier gate such as gauge-invariant observable density, same-theory "
            "nontriviality witness selection, reflection-positive continuum topology, regulator/RG basin entry, large-field/topology "
            "control, fibered block estimates, continuum Schwinger coherence, or OS spectral transfer; (3) explain the physical "
            "carrier and general field-facing impact of the move; or (4) explicitly say the branch is looping and backtrack, repair, "
            "or quarantine it."
        ),
        "anti_repetition_instructions": [
            (
                "If recent branch memory already contains the three-hairpin threshold `8m^2+2R12-4R13-4R23`, do not spend the cycle "
                "restating that threshold. The next contribution-making move must compute, decompose, estimate, or falsify the connected "
                "boundary-OPE polarization term R: name the regulator, the Wilson contraction or cumulant being evaluated, the cancellation "
                "being used, and the sign/size condition that would promote or demote the branch."
            ),
            (
                "If recent branch memory already contains the symbolic toy threshold `lambda=-m^2/3` or `R_ij=lambda L_ij^2`, do not "
                "repeat symbolic-model analysis. Move to the actual Yang-Mills input: write the connected Wilson cumulant or plaquette-sheet "
                "contraction that defines R_ij, identify color/geometric factors, and state the first calculable bound or sign test."
            ),
        ],
        "forbidden_cross_target_terms": [
            "hardness magnification",
            "natural proof barrier",
            "relativization",
            "algebrization",
            "mcsp",
            "p/poly",
        ],
        "stepping_stone_forms": [
            {
                "form": "finite_os_obstruction_theorem",
                "object": "finite reflected-Wilson OS quotient theorem",
                "audience": "mathematical physicists and constructive QFT researchers",
                "novelty_axis": "a finite positivity obstruction stated with explicit Wilson-observable assumptions",
                "decisive_validation": "prove the finite theorem and show which same-theory Wilson/OPE transfer remains open",
                "disqualifiers": ["proxy observable algebra", "vacuous positivity", "fixed-cutoff artifact"],
            },
            {
                "form": "worked_wilson_collar_calculation",
                "object": "explicit Wilson collar or hairpin H,K calculation",
                "audience": "gauge theory and constructive field theory researchers",
                "novelty_axis": "a reproducible finite calculation that changes the OS obstruction status",
                "decisive_validation": "compute or parameterize H,K and test the first- and second-order PSD gates",
                "disqualifiers": ["uncontrolled collar remainder", "not gauge-invariant", "no sign or eigenvalue consequence"],
            },
            {
                "form": "same_theory_transfer_lemma",
                "object": "same-theory Euclidean-to-Hilbert or Wilson-to-Schwinger transfer lemma",
                "audience": "mathematical physics proof theorists",
                "novelty_axis": "a typed bridge that prevents finite calculations from drifting to a proxy theory",
                "decisive_validation": "state source object, target object, topology, and uniformity burden",
                "disqualifiers": ["silent change of theory", "postulated Hilbert space", "nonuniform continuum limit"],
            },
        ],
        "paper_relevance_criteria": [
            {
                "dimension": "conceptual_depth",
                "good_enough": "The result engages a core Yang-Mills bridge obligation rather than a surface analogy: same-theory construction, OS positivity, Wilson observable algebra, boundary OPE, quotient positivity, or spectral reconstruction.",
                "strong_signals": ["same-theory", "wilson", "os", "boundary ope", "schur", "quotient", "spectral", "uniform remainder"],
                "missing_if_weak": "Name the exact Yang-Mills bridge obligation, source object, target object, and validity regime affected by the result.",
            },
            {
                "dimension": "conceptual_novelty",
                "good_enough": "The result contributes a new finite obstruction, bridge lemma, worked Wilson calculation, or transfer boundary rather than repackaging OS or Schur-Feshbach machinery.",
                "strong_signals": ["finite obstruction", "worked calculation", "endpoint", "hairpin", "collar", "kappa", "same-theory transfer"],
                "missing_if_weak": "Separate standard OS/Schur machinery from the new reflected-Wilson object or calculation.",
            },
            {
                "dimension": "unblocking_power",
                "good_enough": "The result decides a concrete next move: prove the finite theorem, compute H,K, certify transfer, backtrack, or quarantine a proxy branch.",
                "strong_signals": ["compute", "prove", "falsifier", "quarantine", "backtrack", "validation handoff", "sign", "eigenvalue"],
                "missing_if_weak": "State which blocked proof obligation becomes decidable and what calculation or theorem would decide it.",
            },
            {
                "dimension": "applicability",
                "good_enough": "The object can be reused across Wilson families, boundary collars, quotient positivity checks, or reconstruction interfaces under stated assumptions.",
                "strong_signals": ["family", "observable algebra", "uniform", "transfer", "regime", "assumptions", "reusable"],
                "missing_if_weak": "State the family of observables/regulators and the assumptions under which the result transfers.",
            },
            {
                "dimension": "understanding_gain",
                "good_enough": "The result explains where the proof pressure lives: finite positivity, same-theory transfer, continuum control, nontriviality, or spectral witness.",
                "strong_signals": ["because", "pressure", "why", "blocking gap", "mechanism", "transfer debt", "remainder"],
                "missing_if_weak": "Explain what the result teaches about why the Yang-Mills route is hard or where the proof debt moves.",
            },
            {
                "dimension": "physical_relevance_and_general_impact",
                "good_enough": "The result names a physical carrier, target gate, and unification-power payoff: gauge-invariant Wilson/Schwinger observables, OS Hilbert reconstruction, nontriviality, continuum control, or the Hamiltonian spectral-gap interface are compressed by one mechanism rather than listed as adjacent aspirations.",
                "strong_signals": ["physical carrier", "gauge-invariant", "wilson", "schwinger", "os hilbert", "hamiltonian", "spectral", "mass gap", "nontriviality", "general impact", "unification power", "unifies"],
                "missing_if_weak": "State what a mathematical physicist would understand differently, which separate physical/proof pressures are unified, and why the result is not merely an incremental finite or algebraic contribution.",
            },
        ],
        "physical_relevance_criteria": {
            "required_carriers": [
                "gauge-invariant Wilson observable",
                "continuum Schwinger-function family",
                "OS Hilbert-space observable or excitation-sector object",
                "Hamiltonian or spectral-measure object",
                "nontriviality witness such as a connected cumulant",
            ],
            "required_target_gates": [
                "same-theory continuum construction",
                "OS/Wightman reconstruction",
                "gauge-invariant observable density",
                "nontriviality of the field",
                "positive spectral mass gap",
            ],
            "impact_test": (
                "A branch is physically relevant only if it says how success or failure changes a physical carrier, one Clay-gate "
                "obligation, field-facing understanding, and unification power. Otherwise it is support-only or an incremental-math drift risk."
            ),
            "unification_power_test": (
                "Name which previously separate carriers, target gates, estimates, representations, or route pressures are unified by "
                "one mechanism, and what new hypothesis or proof obligation this compression exposes."
            ),
            "demote_when": [
                "no physical carrier is named",
                "the result remains a fixed-cutoff or finite-volume artifact without transfer conditions",
                "the observable algebra is a proxy or toy theory",
                "the spectral-gap or OS-Hilbert interface is only gestured at",
                "the general impact is internal workflow progress rather than physics understanding",
                "the branch accumulates adjacent lemmas without a unifying mechanism or representation",
            ],
        },
        "main_problem_balance": {
            "local_subgoal_scope": (
                "Finite Route A subgoals: the reflected-Wilson Schur-Feshbach theorem, explicit H,K collar or hairpin objects, "
                "and post-H,K endpoint-box R/kappa_4 sign or interval certificates."
            ),
            "larger_problem_boundary": (
                "The Clay problem still requires a four-dimensional Yang-Mills quantum field theory satisfying the OS/Wightman "
                "axioms, a nontrivial continuum limit, and a positive Hamiltonian mass gap in the same theory."
            ),
            "allowed_claim": (
                "A consolidation may claim only a finite theorem, worked Wilson calculation, same-theory transfer boundary, or "
                "route-deciding obstruction whose assumptions and non-claims are explicit."
            ),
            "forbidden_claims": [
                "A finite reflected-Wilson obstruction proves the continuum mass gap.",
                "Endpoint-box positivity at fixed cutoff supplies OS/Wightman reconstruction.",
                "A same-theory marker replaces a continuum transfer theorem.",
                "A symbolic collar or toy calculation stands in for a gauge-invariant Wilson construction.",
            ],
            "larger_problem_gate_map": [
                "construction_of_same_theory_measure",
                "os_wightman_reconstruction",
                "nontrivial_continuum_limit",
                "positive_spectral_mass_gap",
            ],
            "balance_test": (
                "Every local subgoal must name which larger YM gate it changes, which gate remains untouched, and why the "
                "local claim is still valuable without implying the full mass gap theorem."
            ),
        },
        "publication_consolidation_policy": {
            "max_completion_cycles": 4,
            "max_recursion_depth": 1,
            "allowed_cycle_types": [
                "proof_completion",
                "counterexample_or_falsifier",
                "finite_computation_or_symbolic_parameterization",
                "prior_art_boundary",
                "manuscript_integration",
            ],
            "stop_conditions": [
                "publication_ready_subgoal",
                "precise_demotion",
                "blocked_named_lemma",
                "budget_exhausted_release_to_exploration",
            ],
            "recursion_guard": (
                "Do not open a nested publication-consolidation loop from inside a consolidation loop. Any sublemma, appendix, "
                "or side calculation must fit inside the current cycle budget or be deferred to conceptual exploration."
            ),
        },
        "representational_dynamics_overlay": {
            "source_index": "agentic/reports/ym_representational_dynamics_integration/source_index.json",
            "proof_objects": "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json",
            "validator": "agentic/scripts/validate_ym_workflow_integration.py",
            "required_cycle_focus": [
                "freeze exact Clay target and claim level",
                "state preserved gauge-invariant observables and recovery maps",
                "declare representation morphisms, invariants, and error budgets",
                "choose regulator/RG obligations with large-field and topology controls",
                "separate restricted finite evidence from continuum and OS spectral-transfer hypotheses",
                "emit frontier audit and demotion trigger before promotion",
            ],
            "hard_frontier_gates": [
                "volume- and cutoff-uniform full-measure basin entry",
                "large-field and topological summability across RG steps",
                "regulator-independent continuum Schwinger functions",
                "OS positivity, observable density, and physical-unit spectral transfer",
            ],
        },
    },
    "p-vs-np-target": {
        "target_id": "p-vs-np-target",
        "slug": "p-vs-np",
        "display_name": "P vs NP",
        "domain": "computational complexity theory",
        "strategy_tab_label": "Complexity Strategy",
        "story_tab_label": "Proof Strategy Story",
        "branch_prompt_header": "You are running one branch of Abducer's P vs NP discovery marathon.",
        "work_standard": (
            "The work must be substantive complexity-theory discovery work: sharpen route lemmas, state source and target models, "
            "track reductions and quantitative thresholds, expose barrier interactions, attempt derivations, name blocking gaps, "
            "add falsifiers, and preserve the distinction between route-level progress and the main P != NP conjecture."
        ),
        "definition_prefixes": [
            "source object:",
            "target object:",
            "controlled interface:",
            "target-preserving condition:",
        ],
        "validity_examples": [
            "Valid when the source lower-bound model is explicitly named...",
            "Applies after the reduction preserves uniformity and threshold parameters...",
            "Requires the target-preserving complexity-class transfer...",
        ],
        "consistency_markers": ["target-preserving", "same-framework"],
        "decisive_target_invariant": (
            "Current decisive target invariant: do not merely restate P vs NP, hardness magnification, or barrier folklore. The cycle must aim at "
            "one contribution-making move: (1) prove or refute a route-specific bridge lemma with named source model, target class, and threshold; "
            "(2) compute or formalize a concrete quantitative transfer from a weak lower bound, MCSP/meta-complexity carrier, proof-complexity object, "
            "or derandomization object; or (3) certify that a route fails because relativization, natural proofs, algebrization, nonuniform leakage, "
            "or quantitative threshold collapse blocks the intended transfer. If it cannot do one of these, explicitly backtrack, repair, or quarantine it."
        ),
        "anti_repetition_instructions": [
            (
                "If recent branch memory already says that a hardness-magnification theorem is promising, do not repeat that slogan. Name the exact "
                "barely-nontrivial lower bound, source model, target consequence, and quantitative parameter that must be preserved."
            ),
            (
                "If recent branch memory already invokes a barrier, do not merely cite the barrier. State the formal obstruction it creates for this "
                "route and whether the proposed object is nonrelativizing, non-natural, non-algebrizing, or only outside the known barrier's scope."
            ),
        ],
        "forbidden_cross_target_terms": [
            "yang-mills",
            "wilson",
            "os-positive",
            "reflection positivity",
            "schwinger",
            "wightman",
            "gauge-invariant",
            "mass gap",
            "hamiltonian spectral",
            "hairpin",
            "collar",
        ],
        "stepping_stone_forms": [
            {
                "form": "quantitative_transfer_obstruction",
                "object": "exact transfer inequality or exponent-window obstruction",
                "audience": "complexity theorists studying lower-bound barriers and hardness magnification",
                "novelty_axis": "replace route optimism with explicit a,q,beta or threshold-collapse conditions",
                "decisive_validation": "derive the inequality and compare against known magnification/barrier literature",
                "disqualifiers": ["bounded-window only", "target-equivalent source lower bound", "advice leakage"],
            },
            {
                "form": "route_specific_no_go",
                "object": "barrier-aware impossibility theorem for a named route family",
                "audience": "complexity theorists evaluating proof-method limitations",
                "novelty_axis": "turn a barrier pressure into a specific method-class no-go",
                "decisive_validation": "state the exact relativization, naturalness, algebrization, or model premise",
                "disqualifiers": ["generic barrier citation", "escape premise untyped", "wrong target model"],
            },
            {
                "form": "searchable_certificate_bridge",
                "object": "MCSP/MKtP or proof-object certificate bridge",
                "audience": "meta-complexity, derandomization, and proof-complexity researchers",
                "novelty_axis": "replace nonuniform hard-row choice with searchable advice-free certificates",
                "decisive_validation": "prove certificate existence, searchability, soundness, and no advice leakage",
                "disqualifiers": ["certificate existence target-equivalent", "ranked decoder leakage", "natural property"],
            },
            {
                "form": "restricted_model_transfer_boundary",
                "object": "restricted-model lower-bound transfer envelope",
                "audience": "complexity theorists comparing restricted and unrestricted lower bounds",
                "novelty_axis": "identify exactly why a restricted lower bound fails or survives as P-vs-NP evidence",
                "decisive_validation": "compute the compiler envelope B_mu,T(m,k) and exhibit easy-function falsifiers",
                "disqualifiers": ["P-easy hard instance", "no compiler envelope", "proxy lower bound"],
            },
            {
                "form": "all_exponent_quantifier_lift",
                "object": "cofinal all-exponent transfer family",
                "audience": "hardness magnification and nonuniform lower-bound researchers",
                "novelty_axis": "separate fixed-window consequences from NP not subset P/poly-level claims",
                "decisive_validation": "for every c, construct source margin and overhead satisfying a_c>q_c+beta_c c",
                "disqualifiers": ["same bounded window", "exponent-indexed advice", "source assumption as hard as target"],
            },
        ],
        "paper_relevance_criteria": [
            {
                "dimension": "conceptual_depth",
                "good_enough": "The result works at the level of a real P vs NP proof obstruction or bridge: source carrier, target class, circuit model, reduction/transfer map, quantifier regime, and barrier status are all explicit.",
                "strong_signals": ["source", "target", "circuit", "sat", "p/poly", "nonuniform", "uniform", "quantifier", "barrier", "transfer"],
                "missing_if_weak": "Name the source carrier/language, target class, circuit model, transfer map, and quantifier regime before treating the result as paper-relevant.",
            },
            {
                "dimension": "conceptual_novelty",
                "good_enough": "The result adds a new exact obstruction, bridge, no-go, or certificate interface relative to known hardness magnification, MCSP/MKtP, proof-complexity, natural-proofs, relativization, or algebrization families.",
                "strong_signals": ["exact", "beta", "q", "threshold", "collapse", "mcsp", "mktp", "certificate", "no-go", "nonblackbox"],
                "missing_if_weak": "Separate the reused barrier/magnification literature from the new theorem, calculation, carrier, or obstruction being claimed.",
            },
            {
                "dimension": "unblocking_power",
                "good_enough": "The result changes route priority by proving a transfer, exposing a quantitative loss, ruling out a method class, or identifying the precise bounded calculation that would decide the branch.",
                "strong_signals": ["falsifier", "pivot", "backtrack", "quarantine", "collapse", "lower bound", "advice leakage", "all-exponent", "subpolynomial"],
                "missing_if_weak": "State the decisive branch-level test and how its outcome changes continue, adapt, backtrack, pivot, or handoff.",
            },
            {
                "dimension": "applicability",
                "good_enough": "The result is reusable across a nontrivial family of carriers, reductions, restricted models, proof systems, or certificate constructions under explicit assumptions and transfer inequalities.",
                "strong_signals": ["carrier", "family", "restricted model", "proof-complexity", "derandomization", "compiler envelope", "searchable", "assumptions"],
                "missing_if_weak": "State which route families or models the result applies to, and which assumptions prevent proxy drift.",
            },
            {
                "dimension": "understanding_gain",
                "good_enough": "The result clarifies why the route is hard: where proof debt moves, which exponent or advice term destroys the transfer, or which barrier premise actually binds.",
                "strong_signals": ["because", "why", "pressure", "blocking gap", "advice", "natural", "relativization", "algebrization", "proof debt", "threshold"],
                "missing_if_weak": "Explain what the result teaches about the obstacle, not merely that the route is promising or blocked.",
            },
        ],
    },
}


def target_profile(target_id: str | None) -> dict[str, Any]:
    selected = (target_id or DEFAULT_TARGET_ID).strip() or DEFAULT_TARGET_ID
    profile = TARGET_PROFILES.get(selected)
    if profile:
        return dict(profile)
    if selected == "markov-kakutani-fixed-point-theorem-target":
        profile = target_profile("generic-fixed-point-target")
        profile.update(
            target_id=selected,
            slug="markov-kakutani-fixed-point-theorem",
            display_name="Markov-Kakutani finite-family fixed-point theorem",
            branch_prompt_header="Reconstruct and validate one proof route for the known finite-family Markov-Kakutani theorem.",
            decisive_target_invariant=(
                "Give an actual proof or counterexample, not a plan. Preserve compactness, convexity, "
                "continuity, affinity and commutativity. Use subnets in nonmetrizable compact spaces. "
                "State the Cesaro telescoping identity, explain invariance of fixed sets, and prove the "
                "finite-family induction. This is known-theorem reconstruction; make no novelty claim. "
                "The repository source is KB/markov-kakutani-fixed-point-theorem.kb.md."
            ),
        )
        return profile
    return {
        "target_id": selected,
        "slug": selected.replace("-target", ""),
        "display_name": selected,
        "domain": "mathematics",
        "strategy_tab_label": "Mathematical Strategy",
        "story_tab_label": "Proof Strategy Story",
        "branch_prompt_header": f"You are running one branch of Abducer's {selected} discovery marathon.",
        "work_standard": (
            "The work must be substantive mathematical discovery work: sharpen bridge lemmas, state definitions and assumptions, "
            "expose equations with validity conditions, attempt derivations, name blocking gaps, add falsifiers, and preserve target commitments."
        ),
        "definition_prefixes": ["source object:", "target object:", "controlled interface:", "target-preserving condition:"],
        "validity_examples": ["Valid when the source object and target object are both explicitly named..."],
        "consistency_markers": ["target-preserving"],
        "decisive_target_invariant": (
            "Current decisive target invariant: do not restate the problem. Produce a target-preserving lemma, calculation, falsifier, "
            "or explicit backtrack/quarantine decision."
        ),
        "anti_repetition_instructions": [],
        "forbidden_cross_target_terms": [],
        "stepping_stone_forms": [
            {
                "form": "bridge_or_obstruction",
                "object": "target-preserving bridge, obstruction, probe, or conceptual mechanism",
                "audience": "domain experts",
                "novelty_axis": "a bounded object changes route priority or proof obligations",
                "decisive_validation": "state a finite proof, calculation, falsifier, or source-backed comparison",
                "disqualifiers": ["proxy problem", "unbounded validation", "no target relation"],
            }
        ],
        "paper_relevance_criteria": [
            {
                "dimension": "conceptual_depth",
                "good_enough": "The result engages a core target commitment with explicit source object, target object, assumptions, and validation handoff.",
                "strong_signals": ["source", "target", "assumption", "validation", "bridge", "obstruction"],
                "missing_if_weak": "Name the mathematical object and target-preserving handoff affected by the result.",
            },
            {
                "dimension": "conceptual_novelty",
                "good_enough": "The result contributes a new bounded bridge, obstruction, probe, mechanism, or comparison class rather than restating known background.",
                "strong_signals": ["new", "exact", "finite", "obstruction", "bridge", "mechanism", "falsifier"],
                "missing_if_weak": "Separate reused machinery from the new claim or object.",
            },
            {
                "dimension": "unblocking_power",
                "good_enough": "The result changes a route decision through a finite proof, calculation, falsifier, or validation handoff.",
                "strong_signals": ["decide", "compute", "prove", "falsifier", "backtrack", "pivot", "handoff"],
                "missing_if_weak": "State the decisive test and how it changes route priority.",
            },
            {
                "dimension": "applicability",
                "good_enough": "The result applies beyond one local cycle under stated assumptions and boundary conditions.",
                "strong_signals": ["family", "general", "assumptions", "regime", "transfer", "reusable"],
                "missing_if_weak": "State the class of cases and validity regime.",
            },
            {
                "dimension": "understanding_gain",
                "good_enough": "The result explains why the route succeeds, fails, or moves proof debt.",
                "strong_signals": ["because", "why", "mechanism", "pressure", "blocking gap", "proof debt"],
                "missing_if_weak": "State what becomes better understood.",
            },
        ],
    }


def profile_prompt_block(target_id: str | None) -> str:
    profile = target_profile(target_id)
    prefixes = ", ".join(f"`{item}`" for item in profile["definition_prefixes"])
    examples = ", ".join(f"`{item}`" for item in profile["validity_examples"])
    anti_repetition = "\n\n".join(profile.get("anti_repetition_instructions", []))
    balance = profile.get("main_problem_balance", {})
    consolidation = profile.get("publication_consolidation_policy", {})
    ym_overlay = profile.get("representational_dynamics_overlay", {})
    physical_relevance = profile.get("physical_relevance_criteria", {})
    balance_block = ""
    if isinstance(balance, dict) and isinstance(consolidation, dict) and balance:
        balance_block = (
            "Local-subgoal/main-problem balance:\n"
            f"- Local scope: {balance.get('local_subgoal_scope', '')}\n"
            f"- Larger target boundary: {balance.get('larger_problem_boundary', '')}\n"
            f"- Allowed claim: {balance.get('allowed_claim', '')}\n"
            f"- Balance test: {balance.get('balance_test', '')}\n"
            f"- Publication consolidation limit: at most {consolidation.get('max_completion_cycles', 4)} completion cycles, "
            f"recursion depth at most {consolidation.get('max_recursion_depth', 1)}, then release back to conceptual exploration.\n\n"
        )
    ym_overlay_block = ""
    if isinstance(ym_overlay, dict) and ym_overlay:
        focus = "; ".join(ym_overlay.get("required_cycle_focus", []))
        gates = "; ".join(ym_overlay.get("hard_frontier_gates", []))
        ym_overlay_block = (
            "Yang-Mills representational dynamics overlay:\n"
            f"- Source index: {ym_overlay.get('source_index', '')}\n"
            f"- Proof objects: {ym_overlay.get('proof_objects', '')}\n"
            f"- Validator: {ym_overlay.get('validator', '')}\n"
            f"- Required cycle focus: {focus}\n"
            f"- Hard frontier gates: {gates}\n"
            "- Treat imported package results as restricted, conditional, or support-only unless a frontier hypothesis is independently discharged.\n\n"
        )
    physical_relevance_block = ""
    if isinstance(physical_relevance, dict) and physical_relevance:
        carriers = "; ".join(physical_relevance.get("required_carriers", []))
        gates = "; ".join(physical_relevance.get("required_target_gates", []))
        demote = "; ".join(physical_relevance.get("demote_when", []))
        physical_relevance_block = (
            "Physical relevance and general impact gate:\n"
            f"- Required physical carriers: {carriers}\n"
            f"- Required target gates: {gates}\n"
            f"- Impact test: {physical_relevance.get('impact_test', '')}\n"
            f"- Unification-power test: {physical_relevance.get('unification_power_test', '')}\n"
            f"- Demote when: {demote}\n"
            "- Use the phrases `physical carrier`, `physical relevance`, `general impact`, and `unification power` in substantive branch fields when "
            "the branch is making or denying a physics-facing contribution.\n\n"
        )
    return (
        f"{profile['branch_prompt_header']}\n"
        "Return only the JSON object required by the provided output schema. Do not edit files.\n\n"
        f"{profile['work_standard']}\n\n"
        "Keep the JSON complete and compact. Prefer short expert mathematical sentences over long paragraphs. Do not include markdown fences, "
        "commentary outside JSON, or giant literature-style explanations inside string fields. Return syntactically valid JSON only: "
        "escape embedded quotes, avoid raw newlines inside strings, and prefer ASCII identifiers unless a field explicitly requires LaTeX.\n\n"
        "Validation requirements: candidate_lemmas[0].definitions must include four strings beginning exactly with "
        f"{prefixes}. The output text must also use the words `falsifier` and `valid` in substantive contexts. "
        "Every candidate_lemmas[0].equations item must include a `valid_when` sentence of at least eight words that explains "
        "the mathematical regime where the formula applies; do not use terse values such as `always`, `by definition`, "
        f"`same regime`, or `valid for the above`. Good examples include {examples}.\n\n"
        "The `gedanken_experiment_design` object is mandatory. It must be a concrete target-preserving thought experiment, "
        "not an empty planning scaffold: name the mathematical situation, one varied variable, at least two held-fixed controls, "
        "the expected observation, and the transfer certificate needed before the intuition may affect proof obligations.\n\n"
        f"{profile['decisive_target_invariant']}\n\n"
        f"{balance_block}"
        f"{ym_overlay_block}"
        f"{physical_relevance_block}"
        f"{anti_repetition}\n\n"
    )


def default_discovery_programs(target_id: str | None) -> list[dict[str, Any]]:
    profile = target_profile(target_id)
    if profile["target_id"] == "p-vs-np-target":
        return [
            {
                "title": "Hardness-Magnification Bridge Realization",
                "machinery_role": "route_bridge",
                "controlled_interface": "barely-nontrivial lower bound -> major class separation consequence",
                "hypothesis": (
                    "A route-specific hardness-magnification bridge may become proof-relevant only if the source model, target class, "
                    "and quantitative threshold survive transfer without nonuniform leakage."
                ),
                "mathematical_mechanism": (
                    "Name the exact weak lower bound, carrier problem, parameter regime, and amplification theorem needed to move from "
                    "a local lower-bound witness toward NP not in P/poly or another target-preserving separation."
                ),
                "dependencies": ["hardness magnification theorem", "source lower-bound model", "target class consequence"],
                "falsifiers": ["threshold collapse", "model mismatch", "nonuniform leakage"],
                "promotion_signal": "A bridge lemma states source model, target consequence, and preserved quantitative threshold.",
                "pivot_signal": "The bridge cannot preserve the threshold or only restates a known magnification theorem.",
            },
            {
                "title": "Barrier-Aware Lower-Bound Route",
                "machinery_role": "barrier_control",
                "controlled_interface": "proposed lower-bound method -> relativization/natural-proof/algebrization audit",
                "hypothesis": (
                    "A lower-bound route is worth pursuing only when its proof object is typed against known barriers rather than merely "
                    "described as nonstandard."
                ),
                "mathematical_mechanism": (
                    "For each proposed route object, state whether it relativizes, naturalizes, algebrizes, or escapes by using a feature "
                    "outside the known barrier hypothesis."
                ),
                "dependencies": ["relativization audit", "natural proof audit", "algebrization audit"],
                "falsifiers": ["barrier hypothesis applies unchanged", "escape feature is undefined", "route loses explicitness"],
                "promotion_signal": "The route names a formal barrier mismatch that is relevant to the target theorem.",
                "pivot_signal": "The route cannot say which barrier it avoids or why.",
            },
            {
                "title": "MCSP / Meta-Complexity Carrier Transfer",
                "machinery_role": "carrier_transfer",
                "controlled_interface": "MCSP-type witness object -> circuit lower-bound or derandomization consequence",
                "hypothesis": (
                    "A meta-complexity carrier may concentrate structural information that ordinary circuit lower-bound routes cannot access directly."
                ),
                "mathematical_mechanism": (
                    "Formalize the carrier, its explicitness condition, and the extraction theorem needed to turn it into a lower-bound, PIT, "
                    "or derandomization consequence."
                ),
                "dependencies": ["MCSP carrier", "extraction theorem", "explicitness condition"],
                "falsifiers": ["carrier is not explicit", "extraction loses the needed class", "consequence is only nonuniform"],
                "promotion_signal": "A carrier-transfer lemma gives a checkable target-preserving consequence.",
                "pivot_signal": "The carrier cannot be connected to an accepted complexity-theoretic consequence.",
            },
        ]
    return [
        {
            "title": "Target-object bridge construction",
            "machinery_role": "construction",
            "controlled_interface": "raw target -> typed target object",
            "hypothesis": "A durable run can start by restating the target object and bridge obligations.",
            "mathematical_mechanism": "Use target navigation and dependency cartography to expose source and target objects.",
            "dependencies": ["target packet", "dependency graph", "essential target ledger"],
            "falsifiers": ["source object missing", "target object missing", "bridge obligation untyped"],
            "promotion_signal": "A target-preserving bridge lemma is stated with checkable assumptions.",
            "pivot_signal": "Repeated attempts cannot name a target-preserving source or target object.",
        }
    ]
