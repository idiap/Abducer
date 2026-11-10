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

"""Profile the conceptual breakthrough types required by the blocked discovery frontier."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

_SKILLS_ROOT = Path(__file__).resolve().parents[3]
_COMMON_DIR = _SKILLS_ROOT / "common"
_PROVE_SCRIPT_DIR = _SKILLS_ROOT / "discovery" / "kb-prove-cycle" / "scripts"
for _path in (_COMMON_DIR, _PROVE_SCRIPT_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from generate_proof_queue_report import compile_pdf
from discovery_lens_heuristic import build_categorical_pathway_heuristic
from discovery_lens_heuristic import build_hott_pathway_heuristic
from discovery_branch_queue import discovery_branch_paths
from discovery_branch_queue import load_discovery_branch_state
from discovery_branch_queue import materialize_discovery_branches
from discovery_branch_queue import save_discovery_branch_state
from discovery_branch_queue import write_discovery_branch_dossiers
from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


BREAKTHROUGH_TEMPLATES: dict[str, dict[str, Any]] = {
    "carrier-realization": {
        "breakthrough_family": "realization",
        "required_move": "Turn a typed but schematic carrier into an explicit mathematical object family with admissibility conditions and a forcing theorem.",
        "abstraction_required": "An explicit obstruction family, witness family, surrogate promise problem, or quantitative measure that is realized from the source theorem rather than only named by role.",
        "minimal_theorem_shape": "If source theorem S holds in regime R, then one can construct an explicit carrier C with admissibility conditions A such that C preserves invariant I and supports a route-specific forcing lemma to target T.",
        "major_subresult_type": "bridge object/tool",
        "search_modes": [
            "explicit carrier construction",
            "equivalence search between live carrier encodings",
            "surrogate problem design with forcing semantics",
        ],
        "anti_patterns": [
            "renaming the carrier without adding realizability conditions",
            "adding more obligations without exhibiting a concrete carrier family",
        ],
    },
    "formula-size-transport": {
        "breakthrough_family": "transport",
        "required_move": "Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.",
        "abstraction_required": "A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.",
        "minimal_theorem_shape": "For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.",
        "major_subresult_type": "transfer principle",
        "search_modes": [
            "cross-model transport principle",
            "invariant-preserving compilation theorem",
            "representation normal form for formula-size transfer",
        ],
        "anti_patterns": [
            "assuming the target theorem already provides the transport",
            "strengthening the source lower bound without addressing the model shift",
        ],
    },
    "target-alignment": {
        "breakthrough_family": "alignment",
        "required_move": "Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.",
        "abstraction_required": "An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.",
        "minimal_theorem_shape": "Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.",
        "major_subresult_type": "transfer principle",
        "search_modes": [
            "object-class correspondence search",
            "normal-form mediation",
            "dual characterization of the target object",
        ],
        "anti_patterns": [
            "treating topical similarity as object equivalence",
            "adding a stronger carrier without specifying the target object class map",
        ],
    },
    "pit-upgrade": {
        "breakthrough_family": "explicitness",
        "required_move": "Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.",
        "abstraction_required": "An explicit generator, certificate family, or algebraic witness system that is constructive enough for PIT rather than merely semantic.",
        "minimal_theorem_shape": "If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.",
        "major_subresult_type": "bridge object/tool",
        "search_modes": [
            "explicit extractor or generator search",
            "certificate map construction",
            "semantic-to-algorithmic upgrade theorem",
        ],
        "anti_patterns": [
            "equating a black-box hitting-set statement with an explicit generator",
            "rephrasing derandomization as semantics without uniformity or efficiency",
        ],
    },
    "explicitness-gap": {
        "breakthrough_family": "explicitness",
        "required_move": "Add uniform, explicit, efficiently constructible content to an otherwise semantic object.",
        "abstraction_required": "A uniform construction rule, extractor, or explicit family indexed by input length and class parameters.",
        "minimal_theorem_shape": "For every length parameter n, the existential object C_n can be constructed or certified explicitly in time class X while preserving property P.",
        "major_subresult_type": "bridge object/tool",
        "search_modes": [
            "uniformization",
            "effective construction",
            "certificate extraction",
        ],
        "anti_patterns": [
            "accepting existence without algorithmic access",
            "shifting to a broader semantic object that is still non-explicit",
        ],
    },
    "local-reduction-barrier": {
        "breakthrough_family": "barrier-aware transfer",
        "required_move": "Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.",
        "abstraction_required": "A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.",
        "minimal_theorem_shape": "Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.",
        "major_subresult_type": "barrier result",
        "search_modes": [
            "barrier-aware gadget design",
            "impossibility theorem search",
            "reduction regime decomposition",
        ],
        "anti_patterns": [
            "ignoring the known local-reduction barrier theorem",
            "using generic NP-hardness language without locality constraints",
        ],
    },
    "schema-to-examples": {
        "breakthrough_family": "constructive instantiation",
        "required_move": "Turn an abstract schema into explicit natural example families or prove that the schema cannot instantiate naturally in the current way.",
        "abstraction_required": "A construction template, example-generating reduction family, or a canonicalization principle for natural examples.",
        "minimal_theorem_shape": "From abstract schema S, construct an explicit family of natural instances E_n satisfying properties P and realizing target theorem T.",
        "major_subresult_type": "standalone theorem",
        "search_modes": [
            "canonical example construction",
            "template instantiation",
            "example-preserving reduction search",
        ],
        "anti_patterns": [
            "restating the schema as if it already supplied examples",
            "listing examples without a constructive route from the local abstraction",
        ],
    },
    "characterization-bridge": {
        "breakthrough_family": "semantic bridge",
        "required_move": "Bridge a local definitional object to a global characterization theorem.",
        "abstraction_required": "A semantic correspondence, duality, witness extraction principle, or completeness notion that turns the local definition into the target biconditional.",
        "minimal_theorem_shape": "Local definitional object D has property P if and only if global characterization condition Q holds, with both directions proved at the right level of abstraction.",
        "major_subresult_type": "transfer principle",
        "search_modes": [
            "semantic correspondence theorem",
            "duality or normal form search",
            "two-way implication decomposition",
        ],
        "anti_patterns": [
            "normalizing syntax without adding semantic force",
            "treating a definition as if it already contained the characterization",
        ],
    },
    "general-magnification": {
        "breakthrough_family": "alignment",
        "required_move": "Map a problem-specific carrier into a general magnification framework without losing the quantitative threshold that matters.",
        "abstraction_required": "A general-purpose sparse-problem or distinguisher formulation that faithfully receives the local carrier.",
        "minimal_theorem_shape": "Problem-specific object C induces general object G with preserved sparsity or approximation parameters sufficient to trigger the general magnification theorem.",
        "major_subresult_type": "transfer principle",
        "search_modes": [
            "generalization by faithful embedding",
            "parameter-preserving reformulation",
            "problem-specific to generic theorem bridge",
        ],
        "anti_patterns": [
            "moving to the generic theorem without a preserved parameter map",
            "using the general theorem only as motivation rather than as a typed target",
        ],
    },
    "target-grounding": {
        "breakthrough_family": "bridge-specificity",
        "required_move": "Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.",
        "abstraction_required": "No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.",
        "minimal_theorem_shape": "Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.",
        "major_subresult_type": "research recommendation",
        "search_modes": [
            "activation theorem search",
            "hypothesis verification search",
            "bridge-localization refinement",
        ],
        "anti_patterns": [
            "rediscovering the target theorem",
            "claiming novelty at the target instead of at the activation bridge",
        ],
    },
}

DEFAULT_TEMPLATE = {
    "breakthrough_family": "abstraction-search",
    "required_move": "Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.",
    "abstraction_required": "A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.",
    "minimal_theorem_shape": "State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.",
    "major_subresult_type": "exploratory-conjecture",
    "search_modes": ["typed abstraction search", "bridge split", "counterfactual sharpening"],
    "anti_patterns": ["repeating the same blocked statement without new typed structure"],
}


FAMILY_PROMPT_TEMPLATES: dict[str, dict[str, Any]] = {
    "abstraction-search": {
        "prompt_title": "Abstraction Search Prompt",
        "system_prompt": (
            "You are searching for the minimal conceptual breakthrough that would turn a blocked route into a typed theorem target. "
            "Do not restate the blocked lemma. Identify the sharper carrier, invariant, or bridge law that would make the next theorem materially more specific."
        ),
        "user_task": (
            "Restate the obstruction as a missing abstraction problem, propose 2-4 typed bridge candidates, "
            "and state the first theorem-pair-specific lemma each candidate would make possible."
        ),
        "required_questions": [
            "What typed object would add mathematical content beyond the current schematic carrier?",
            "What route-specific theorem would become stateable if that object existed?",
            "Which candidate clarifies the negative route if it fails?",
        ],
    },
    "realization": {
        "prompt_title": "Carrier Realization Prompt",
        "system_prompt": (
            "You are converting a typed but schematic carrier into an explicit mathematical object family. "
            "Do not rename the carrier. Produce admissibility conditions, a realizability route from the source theorem, and the forcing lemma needed at the target."
        ),
        "user_task": (
            "Construct or sharply constrain an explicit witness family, obstruction family, surrogate promise problem, or quantitative measure "
            "that realizes the blocked route from source theorem to target theorem."
        ),
        "required_questions": [
            "What is the concrete carrier set, map, family, or measure?",
            "How is it built from the source theorem rather than postulated?",
            "What admissibility conditions prevent it from being only a relabeling?",
        ],
    },
    "transport": {
        "prompt_title": "Transport Principle Prompt",
        "system_prompt": (
            "You are searching for an invariant-preserving transport theorem across a model shift. "
            "Do not strengthen the source theorem unless it changes the transport mechanism. Focus on the cross-model map and the preserved quantitative parameter."
        ),
        "user_task": (
            "State the strongest plausible transport law, compilation theorem, or normal form that could move the current carrier into the target model "
            "without losing the invariant needed for the payoff."
        ),
        "required_questions": [
            "What exact quantity must be preserved across the model shift?",
            "What transformed carrier should live in the target model?",
            "What is the first obstruction showing why naive transport fails?",
        ],
    },
    "alignment": {
        "prompt_title": "Alignment Theorem Prompt",
        "system_prompt": (
            "You are aligning a local carrier class with the object class demanded by an existing target theorem. "
            "Topical similarity is not enough. Search for equivalence, correspondence, or a mediating normal form."
        ),
        "user_task": (
            "Describe the object-class map from the current carrier to the target theorem's object class, "
            "including the quantitative property that must survive the correspondence."
        ),
        "required_questions": [
            "What is the target theorem's exact object class?",
            "How does the local carrier induce an object in that class?",
            "Which parameter or sparsity threshold is hardest to preserve?",
        ],
    },
    "explicitness": {
        "prompt_title": "Explicitness Upgrade Prompt",
        "system_prompt": (
            "You are upgrading a semantic or existential object into an explicit algorithmic one. "
            "Do not accept existence without uniformity, efficiency, or extractability."
        ),
        "user_task": (
            "Search for an explicit generator, certificate family, extractor, or uniform construction rule that turns the blocked semantic object "
            "into a derandomization-ready or algorithmically inspectable premise."
        ),
        "required_questions": [
            "What part of the current object is only existential or semantic?",
            "What explicit structure would replace that existential step?",
            "What efficiency class is required for the upgraded object to matter?",
        ],
    },
    "barrier-aware transfer": {
        "prompt_title": "Barrier-Aware Transfer Prompt",
        "system_prompt": (
            "You are searching under an explicit barrier theorem. "
            "Either construct a transfer that survives the barrier's constraints or sharpen the impossibility theorem. "
            "Do not use generic hardness language that ignores the reduction regime."
        ),
        "user_task": (
            "Describe a barrier-aware gadget family or impossibility result for the blocked transfer, with locality bounds and preserved witness structure made explicit."
        ),
        "required_questions": [
            "What exact barrier theorem constrains the route?",
            "What locality or regime parameter must any positive construction respect?",
            "What negative theorem would be a contribution if positive transfer fails?",
        ],
    },
    "constructive instantiation": {
        "prompt_title": "Constructive Instantiation Prompt",
        "system_prompt": (
            "You are turning an abstract schema into explicit mathematical examples. "
            "Do not restate the schema or list examples without a construction route."
        ),
        "user_task": (
            "Search for a construction template, reduction family, or canonicalization principle that produces explicit natural instances from the abstract schema."
        ),
        "required_questions": [
            "What is the first explicit instance family that should be produced?",
            "What reduction or construction template yields that family?",
            "If the construction fails, what does that say about the schema's naturality?",
        ],
    },
    "semantic bridge": {
        "prompt_title": "Semantic Bridge Prompt",
        "system_prompt": (
            "You are bridging a local definitional object to a global characterization theorem. "
            "Syntactic normalization is insufficient. Search for the missing semantic equivalence, duality, or witness-extraction principle."
        ),
        "user_task": (
            "Decompose the biconditional or characterization gap into the minimal semantic implications that would connect the local definition to the global theorem."
        ),
        "required_questions": [
            "What semantic content is missing from the current definition-level object?",
            "Which direction of the characterization is harder and why?",
            "What duality or witness principle could mediate the bridge?",
        ],
    },
    "bridge-specificity": {
        "prompt_title": "Activation Theorem Prompt",
        "system_prompt": (
            "The target theorem is already known. Your task is to identify the local activation theorem that would verify its hypotheses from current artifacts. "
            "Do not rediscover the target theorem."
        ),
        "user_task": (
            "State the activation theorem under search, name the exact target hypothesis that is still unverified, and identify the local bridge object or transfer law needed to verify it."
        ),
        "required_questions": [
            "Which target-theorem hypothesis is still open locally?",
            "What bridge-local theorem would certify that hypothesis?",
            "What novelty remains once the target theorem itself is removed from search?",
        ],
    },
}


CATEGORICAL_TRIGGER_FAMILIES = {
    "realization",
    "transport",
    "alignment",
    "semantic bridge",
    "barrier-aware transfer",
    "constructive instantiation",
    "bridge-specificity",
}


HOTT_TRIGGER_FAMILIES = {
    "alignment",
    "realization",
    "explicitness",
    "semantic bridge",
    "transport",
}


def _lens_negative_outputs(lens_id: str) -> list[str]:
    if lens_id == "categorical-reframing":
        return [
            "non_commuting_route",
            "missing_universal_object",
            "non_functorial_transport",
            "broken_factorization",
        ]
    return [
        "no_equivalence_witness",
        "transport_incoherent",
        "weak_equivalence_only",
        "identity_mismatch",
    ]


def _categorical_lens_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    matched = [
        row
        for row in rows
        if _clean_text(row.get("breakthrough_family")) in CATEGORICAL_TRIGGER_FAMILIES
        or any(
            token in _text_blob(row)
            for token in {
                "transport",
                "composition",
                "correspondence",
                "object class",
                "normal form",
                "model shift",
                "factor",
            }
        )
    ]
    heuristic = build_categorical_pathway_heuristic(matched)
    if len(matched) < 2 or not heuristic.get("recommended"):
        return None
    queue_ids = _union_queue_ids(matched, limit=12)
    obstructions = [
        _clean_text(row.get("obstruction_class"))
        for row in matched
        if _clean_text(row.get("obstruction_class"))
    ]
    diagram_candidates = [
        _clean_text(
            f"Diagram candidate: local route for `{_clean_text(row.get('obstruction_class'))}` should factor from source-side object to mediating carrier implementing `{_clean_text(row.get('abstraction_required'))}` and then into the target activation interface."
        )
        for row in matched[:3]
    ]
    commutativity = [
        _clean_text(
            f"Commutativity obligation: the route for `{_clean_text(row.get('obstruction_class'))}` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses."
        )
        for row in matched[:3]
    ]
    universal_candidates = [
        _clean_text(
            f"Universal-property candidate: search for an intermediate object universal for mediating `{_clean_text(row.get('required_move'))}`."
        )
        for row in matched[:3]
    ]
    return {
        "breakthrough_family": "categorical-reframing",
        "prompt_title": "Categorical Reframing Prompt",
        "obstruction_class": "structural-composition-gap",
        "linked_queue_ids": queue_ids,
        "linked_breakthrough_families": _union_families(matched),
        "linked_reference_ids": _union_text(matched, "reference_ids"),
        "required_move": "Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.",
        "abstraction_required": "A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.",
        "minimal_theorem_shape": "There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.",
        "search_modes": [
            "diagram construction",
            "commutativity checking",
            "factorization search",
            "universal-property search",
            "adjunction-style dualization",
        ],
        "anti_patterns": [
            "renaming route components as categorical objects without reducing proof debt",
            "drawing a diagram without specifying the morphisms or the commutativity claim",
        ],
        "system_prompt": (
            "Use category theory as a structural and compositional discovery lens, not as decorative abstraction. "
            "Identify the source object, target object, typed morphisms already available, and the diagram that should commute if the route is real. "
            "Search for a mediating object with a universal property, test whether the route factors through it, and classify failure as no morphism, non-functorial transport, broken naturality, missing factorization, or failed universal property."
        ),
        "user_task": (
            "Reframe the blocked frontier as a family of diagrammatic composition problems. "
            "State candidate objects, morphisms, commutative squares, factorization claims, and universal properties that would make the live routes structurally compose."
        ),
        "required_questions": [
            "What are the source object, target object, and typed morphisms already present in the route?",
            "What diagram should commute if the route is legitimate?",
            "What mediating object would be universal for this route?",
            "Does the route fail because there is no morphism, because the square does not commute, or because the factorization is missing?",
        ],
        "sample_theorem_targets": [
            _clean_text(
                "Prove that the current route factors through a mediating carrier with a universal property, or show that no such factorization exists under the present invariants."
            )
        ],
        "epistemic_lens": "category-theoretic",
        "routing_heuristic": heuristic,
        "lens_artifacts": {
            "diagram_candidates": diagram_candidates,
            "commutativity_obligations": commutativity,
            "universal_property_candidates": universal_candidates,
            "equivalence_claims": [],
            "transport_obligations": [],
            "coherence_failures": [],
            "negative_outputs": _lens_negative_outputs("categorical-reframing"),
        },
    }


def _hott_lens_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    matched = [
        row
        for row in rows
        if _clean_text(row.get("breakthrough_family")) in HOTT_TRIGGER_FAMILIES
        or any(
            token in _text_blob(row)
            for token in {
                "equivalence",
                "correspondence",
                "representation",
                "normal form",
                "same",
                "transport",
                "coherence",
            }
        )
    ]
    heuristic = build_hott_pathway_heuristic(matched)
    if len(matched) < 2 or not heuristic.get("recommended"):
        return None
    queue_ids = _union_queue_ids(matched, limit=12)
    equivalence_claims = [
        _clean_text(
            f"Equivalence claim: determine whether the live carrier for `{_clean_text(row.get('obstruction_class'))}` is identical to, equivalent to, or only analogous with the target-side object class."
        )
        for row in matched[:3]
    ]
    transport_obligations = [
        _clean_text(
            f"Transport obligation: move the invariant across the proposed equivalence for `{_clean_text(row.get('obstruction_class'))}` without changing the target claim."
        )
        for row in matched[:3]
    ]
    coherence_failures = [
        _clean_text(
            f"Coherence failure probe: check whether different identifications of the carrier for `{_clean_text(row.get('obstruction_class'))}` induce the same transported statement."
        )
        for row in matched[:3]
    ]
    return {
        "breakthrough_family": "equivalence-coherence-reframing",
        "prompt_title": "Equivalence / Coherence Reframing Prompt",
        "obstruction_class": "equivalence-coherence-gap",
        "linked_queue_ids": queue_ids,
        "linked_breakthrough_families": _union_families(matched),
        "linked_reference_ids": _union_text(matched, "reference_ids"),
        "required_move": "Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.",
        "abstraction_required": "A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.",
        "minimal_theorem_shape": "Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.",
        "search_modes": [
            "equivalence witness search",
            "transport-law search",
            "coherence checking",
            "identity-vs-equivalence discrimination",
        ],
        "anti_patterns": [
            "treating topical similarity as equivalence",
            "using representation changes without stating what transports and what fails to transport",
        ],
        "system_prompt": (
            "Use HoTT as an equivalence and coherence discovery lens, not as a replacement foundation. "
            "Type the active concepts and bridge objects, ask whether two formulations are equal, equivalent, or only analogous, "
            "search for transportable invariants, and classify failure as no equivalence witness, incoherent transport, or weak equivalence where strict identity is needed."
        ),
        "user_task": (
            "Reframe the blocked frontier as a problem about sameness, equivalence, transport, and coherence. "
            "State the candidate equivalence claims, the transport obligations they would induce, and the coherence failures that currently block the route."
        ),
        "required_questions": [
            "Which active concepts should be treated as types, and which concrete witnesses should be treated as terms?",
            "Are the live operationalizations equal, equivalent, incomparable, or only analogous?",
            "What invariant or theorem hypothesis must transport along the proposed equivalence?",
            "Where does coherence fail when the same route is identified in two different ways?",
        ],
        "sample_theorem_targets": [
            _clean_text(
                "Exhibit an equivalence witness between the two live carrier formulations and prove that the target-relevant invariant transports coherently; otherwise prove that only weak equivalence is available."
            )
        ],
        "epistemic_lens": "hott",
        "routing_heuristic": heuristic,
        "lens_artifacts": {
            "diagram_candidates": [],
            "commutativity_obligations": [],
            "universal_property_candidates": [],
            "equivalence_claims": equivalence_claims,
            "transport_obligations": transport_obligations,
            "coherence_failures": coherence_failures,
            "negative_outputs": _lens_negative_outputs("equivalence-coherence-reframing"),
        },
    }


def _synthetic_lens_prompt_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows = _profile_rows(report)
    synthetic: list[dict[str, Any]] = []
    categorical = _categorical_lens_row(rows)
    hott = _hott_lens_row(rows)
    if categorical:
        synthetic.append(categorical)
    if hott:
        synthetic.append(hott)
    return synthetic


EPISTEMIC_PATTERN_TEMPLATES: dict[str, dict[str, Any]] = {
    "invariant-discovery": {
        "prompt_title": "Invariant Discovery Prompt",
        "system_prompt": (
            "You are searching for the invariant that the current route is really trying to preserve, expose, or measure. "
            "Do not begin from the named bridge object. Begin from the quantity, structure, or monotone property that would survive the route and explain the payoff."
        ),
        "user_task": (
            "Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route."
        ),
        "required_questions": [
            "What quantity or structure must survive every legitimate route variant?",
            "Which candidate invariant is strong enough to force the payoff but weak enough to be realizable?",
            "How would failure of the invariant candidate sharpen the obstruction class?",
        ],
    },
    "regime-localization": {
        "prompt_title": "Regime Localization Prompt",
        "system_prompt": (
            "You are searching for the smallest model, threshold, asymptotic regime, or promise-gap setting in which the route might first become true. "
            "Do not ask for the full theorem immediately if a more local regime would already be a major contribution."
        ),
        "user_task": (
            "Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme."
        ),
        "required_questions": [
            "Which regime change most plausibly removes the current obstruction without trivializing the result?",
            "What is the first nontrivial threshold at which the route may become true?",
            "Would a localized theorem already count as an independently valuable subresult?",
        ],
    },
    "problem-representation-shift": {
        "prompt_title": "Problem Representation Shift Prompt",
        "system_prompt": (
            "You are testing whether the blocked route is misrepresented rather than false. "
            "Search for an alternative encoding, normal form, dual object, or reformulation in which the route becomes mathematically transparent."
        ),
        "user_task": (
            "Propose representation changes that preserve the source-side content but expose a better target interface, and state the first theorem each representation would make possible."
        ),
        "required_questions": [
            "Which part of the current representation hides the real inferential structure?",
            "What alternative object language or normal form would expose the missing bridge?",
            "What mathematical content must stay invariant under the representation change?",
        ],
    },
    "counterexample-led-concept-formation": {
        "prompt_title": "Counterexample-Led Concept Formation Prompt",
        "system_prompt": (
            "Use failure as a discovery tool. Search for near-counterexamples, barrier analogs, and route-breaking examples, then ask what concept would separate the surviving cases from the failures."
        ),
        "user_task": (
            "Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures."
        ),
        "required_questions": [
            "What is the nearest counterexample or barrier analog to the current route?",
            "Which current concept fails to distinguish the positive and negative cases?",
            "What new concept becomes visible only after inspecting the failure pattern?",
        ],
    },
    "route-decomposition": {
        "prompt_title": "Route Decomposition Prompt",
        "system_prompt": (
            "The current route may be carrying too many inferential roles at once. Decompose it into smaller interfaces, each with its own object, invariant, and theorem target."
        ),
        "user_task": (
            "Split the blocked route into a sequence of subinterfaces, identify the minimal theorem at each interface, and state which subresult would already be valuable if the full route remained open."
        ),
        "required_questions": [
            "Which inferential roles are currently being conflated in one bridge object?",
            "What is the smallest theorem that isolates each role?",
            "Which decomposed segment is most likely to produce a standalone contribution?",
        ],
    },
    "hybridization-of-partial-bridges": {
        "prompt_title": "Hybrid Bridge Synthesis Prompt",
        "system_prompt": (
            "Do not assume one bridge object must do all the work. Search for a hybrid route in which two partial bridges compose, with each bridge carrying a distinct inferential burden."
        ),
        "user_task": (
            "Identify complementary partial bridges, specify their composition order, and state the intermediate theorem that would let them work together."
        ),
        "required_questions": [
            "Which blocked routes solve different parts of the same theorem pair?",
            "What intermediate object or theorem would allow the partial bridges to compose?",
            "What failure would show that the hybrid route is illegitimate rather than merely incomplete?",
        ],
    },
}


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _latex_escape(value: Any) -> str:
    text = _clean_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.replace("->", r"$\rightarrow$ ")
    text = text.replace("`", "'")
    return text


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _queue_index(queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }


def _profile_row(row: dict[str, Any], queue_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    obstruction = _clean_text(row.get("name")).lower()
    template = {**DEFAULT_TEMPLATE, **_ensure_dict(BREAKTHROUGH_TEMPLATES.get(obstruction))}
    queue_ids = [_clean_text(value) for value in _ensure_list(row.get("queue_ids")) if _clean_text(value)]
    priorities = [
        _safe_float(_ensure_dict(queue_rows.get(queue_id)).get("priority"))
        for queue_id in queue_ids
    ]
    top_priority = max(priorities, default=0.0)
    pressure = round(sum(priorities), 3)
    theorem_shapes = []
    for queue_id in queue_ids[:3]:
        queue_row = _ensure_dict(queue_rows.get(queue_id))
        theorem_shapes.append(
            _clean_text(queue_row.get("conjecture_statement") or queue_row.get("claim_text"))
        )
    return {
        "obstruction_class": _clean_text(row.get("name")),
        "breakthrough_family": template["breakthrough_family"],
        "required_move": template["required_move"],
        "abstraction_required": template["abstraction_required"],
        "minimal_theorem_shape": template["minimal_theorem_shape"],
        "major_subresult_type": template["major_subresult_type"],
        "search_modes": list(template["search_modes"]),
        "anti_patterns": list(template["anti_patterns"]),
        "queue_ids": queue_ids,
        "queue_titles": [
            _clean_text(_ensure_dict(queue_rows.get(queue_id)).get("title")) or queue_id
            for queue_id in queue_ids
        ],
        "reference_ids": [_clean_text(value) for value in _ensure_list(row.get("reference_ids")) if _clean_text(value)],
        "reference_titles": [_clean_text(value) for value in _ensure_list(row.get("titles")) if _clean_text(value)],
        "effect_notes": [_clean_text(value) for value in _ensure_list(row.get("what_changed")) if _clean_text(value)],
        "top_priority": top_priority,
        "pressure_score": pressure,
        "sample_theorem_targets": [value for value in theorem_shapes if value],
    }


def build_report(*, prior_art: dict[str, Any], queue: dict[str, Any], kb_ref: str) -> dict[str, Any]:
    queue_rows = _queue_index(queue)
    obstruction_rows = [
        _profile_row(row, queue_rows)
        for row in _ensure_list(prior_art.get("obstruction_map"))
        if isinstance(row, dict) and _clean_text(row.get("name"))
    ]
    obstruction_rows.sort(key=lambda row: (row["pressure_score"], row["top_priority"], row["obstruction_class"]), reverse=True)
    summary_lines = [
        "The discovery layer should stop restating blocked lemmas as if they were already search strategies.",
        "Most frontier pressure is now in bridge-layer breakthroughs: realization, transport, alignment, explicitness, and semantic bridging.",
        "Target-grounded routes should be treated as activation-theorem searches, not as target-theorem discovery.",
    ]
    if obstruction_rows:
        top = obstruction_rows[0]
        summary_lines.append(
            f"The highest-pressure breakthrough family is `{top['breakthrough_family']}` via obstruction class `{top['obstruction_class']}`."
        )
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "profile_count": len(obstruction_rows),
            "covered_queue_count": len({queue_id for row in obstruction_rows for queue_id in row["queue_ids"]}),
        },
        "search_justification": _clean_text(prior_art.get("search_justification")),
        "summary": summary_lines,
        "profiles": obstruction_rows,
    }


def build_prompt_pack(report: dict[str, Any]) -> dict[str, Any]:
    profiles = [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]
    prompt_rows: list[dict[str, Any]] = []
    seen_families: set[str] = set()
    for row in profiles:
        family = _clean_text(row.get("breakthrough_family")) or "abstraction-search"
        if family in seen_families:
            continue
        seen_families.add(family)
        template = {**FAMILY_PROMPT_TEMPLATES.get("abstraction-search", {}), **FAMILY_PROMPT_TEMPLATES.get(family, {})}
        prompt_rows.append(
            {
                "breakthrough_family": family,
                "prompt_title": template.get("prompt_title", f"{family.title()} Prompt"),
                "obstruction_class": _clean_text(row.get("obstruction_class")),
                "linked_queue_ids": list(row.get("queue_ids", [])),
                "linked_reference_ids": list(row.get("reference_ids", [])),
                "required_move": _clean_text(row.get("required_move")),
                "abstraction_required": _clean_text(row.get("abstraction_required")),
                "minimal_theorem_shape": _clean_text(row.get("minimal_theorem_shape")),
                "search_modes": list(row.get("search_modes", [])),
                "anti_patterns": list(row.get("anti_patterns", [])),
                "system_prompt": _clean_text(template.get("system_prompt")),
                "user_task": _clean_text(template.get("user_task")),
                "required_questions": list(template.get("required_questions", [])),
                "sample_theorem_targets": list(row.get("sample_theorem_targets", []))[:2],
                "routing_heuristic": _ensure_dict(row.get("routing_heuristic")),
            }
        )
    prompt_rows.extend(_synthetic_lens_prompt_rows(report))
    return {
        "metadata": {
            "kb_ref": _ensure_dict(report.get("metadata")).get("kb_ref", ""),
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "prompt_family_count": len(prompt_rows),
            "epistemic_pattern_count": 0,
        },
        "summary": [
            "Each breakthrough family now carries a distinct discovery prompt contract.",
            "Discovery should branch by conceptual move type rather than by blocked route label alone.",
            "The prompt packs below are intended to be reused by discovery, governance, and expert-handoff layers.",
            "Synthetic category-theoretic and HoTT reframing families are added when the blocked frontier shows structural-composition or equivalence-coherence pressure across multiple routes.",
        ],
        "prompt_packs": prompt_rows,
        "epistemic_patterns": [],
    }


def _text_blob(row: dict[str, Any]) -> str:
    parts: list[str] = [
        _clean_text(row.get("required_move")),
        _clean_text(row.get("abstraction_required")),
        _clean_text(row.get("minimal_theorem_shape")),
        _clean_text(row.get("obstruction_class")),
        _clean_text(row.get("breakthrough_family")),
    ]
    parts.extend(_clean_text(value) for value in _ensure_list(row.get("search_modes")))
    parts.extend(_clean_text(value) for value in _ensure_list(row.get("sample_theorem_targets")))
    return " ".join(parts).lower()


def _profiles_matching(report: dict[str, Any], *, tokens: set[str] | None = None, families: set[str] | None = None) -> list[dict[str, Any]]:
    rows = [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]
    matched: list[dict[str, Any]] = []
    for row in rows:
        family = _clean_text(row.get("breakthrough_family"))
        if families and family in families:
            matched.append(row)
            continue
        if tokens:
            blob = _text_blob(row)
            if any(token in blob for token in tokens):
                matched.append(row)
    return matched


def _union_queue_ids(rows: list[dict[str, Any]], *, limit: int = 10) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        for queue_id in [_clean_text(value) for value in _ensure_list(row.get("queue_ids")) if _clean_text(value)]:
            if queue_id in seen:
                continue
            seen.add(queue_id)
            ordered.append(queue_id)
            if len(ordered) >= limit:
                return ordered
    return ordered


def _union_families(rows: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        family = _clean_text(row.get("breakthrough_family"))
        if not family or family in seen:
            continue
        seen.add(family)
        ordered.append(family)
    return ordered


def _build_epistemic_patterns(report: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]
    if not profiles:
        return []

    covered_queue_count = int(_ensure_dict(report.get("metadata")).get("covered_queue_count", 0) or 0)
    patterns: list[dict[str, Any]] = []

    def add_pattern(pattern_id: str, rows: list[dict[str, Any]], rationale: str) -> None:
        if not rows:
            return
        template = _ensure_dict(EPISTEMIC_PATTERN_TEMPLATES.get(pattern_id))
        if not template:
            return
        patterns.append(
            {
                "pattern_id": pattern_id,
                "prompt_title": template.get("prompt_title", pattern_id),
                "linked_breakthrough_families": _union_families(rows),
                "linked_obstruction_classes": [
                    _clean_text(row.get("obstruction_class"))
                    for row in rows
                    if _clean_text(row.get("obstruction_class"))
                ],
                "linked_queue_ids": _union_queue_ids(rows),
                "rationale": _clean_text(rationale),
                "system_prompt": _clean_text(template.get("system_prompt")),
                "user_task": _clean_text(template.get("user_task")),
                "required_questions": list(template.get("required_questions", [])),
                "search_modes": sorted({mode for row in rows for mode in _ensure_list(row.get("search_modes")) if _clean_text(mode)}),
                "anti_patterns": sorted({item for row in rows for item in _ensure_list(row.get("anti_patterns")) if _clean_text(item)}),
                "sample_theorem_targets": [item for row in rows for item in _ensure_list(row.get("sample_theorem_targets")) if _clean_text(item)][:2],
            }
        )

    invariant_rows = _profiles_matching(
        report,
        tokens={"invariant", "preserve", "measure"},
        families={"abstraction-search", "realization", "transport", "alignment", "semantic bridge"},
    )
    add_pattern(
        "invariant-discovery",
        invariant_rows,
        "Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.",
    )

    regime_rows = _profiles_matching(
        report,
        tokens={"regime", "model shift", "formula-size", "locality", "threshold"},
        families={"transport", "barrier-aware transfer", "bridge-specificity"},
    )
    add_pattern(
        "regime-localization",
        regime_rows,
        "The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.",
    )

    representation_rows = _profiles_matching(
        report,
        tokens={"normal form", "translation", "object class", "correspondence", "representation"},
        families={"alignment", "semantic bridge", "transport", "abstraction-search"},
    )
    add_pattern(
        "problem-representation-shift",
        representation_rows,
        "Several blocked routes look misrepresented rather than simply false, so representation change is itself a discovery pattern.",
    )

    counterexample_rows = _profiles_matching(
        report,
        tokens={"barrier", "obstruction", "negative", "falsif", "impossibility"},
        families={"barrier-aware transfer", "semantic bridge", "abstraction-search", "realization"},
    )
    if covered_queue_count >= 6 and len(counterexample_rows) < 2:
        counterexample_rows = profiles[:2]
    add_pattern(
        "counterexample-led-concept-formation",
        counterexample_rows,
        "The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.",
    )

    decomposition_rows = [row for row in profiles if len(_ensure_list(row.get("queue_ids"))) >= 4 or _safe_float(row.get("pressure_score")) >= 3.0]
    add_pattern(
        "route-decomposition",
        decomposition_rows,
        "High-pressure obstruction classes are carrying multiple inferential roles at once, so route decomposition is needed before more local search.",
    )

    overlap_pairs: list[dict[str, Any]] = []
    for idx, left in enumerate(profiles):
        left_ids = {_clean_text(value) for value in _ensure_list(left.get("queue_ids")) if _clean_text(value)}
        left_family = _clean_text(left.get("breakthrough_family"))
        for right in profiles[idx + 1 :]:
            right_family = _clean_text(right.get("breakthrough_family"))
            if not left_ids or not right_family or right_family == left_family:
                continue
            right_ids = {_clean_text(value) for value in _ensure_list(right.get("queue_ids")) if _clean_text(value)}
            if left_ids & right_ids:
                overlap_pairs.extend([left, right])
    add_pattern(
        "hybridization-of-partial-bridges",
        overlap_pairs,
        "Some blocked routes sit at the intersection of multiple breakthrough families, which is evidence that one bridge object may be insufficient and a composed route should be explored.",
    )

    seen_ids: set[str] = set()
    unique_patterns: list[dict[str, Any]] = []
    for row in patterns:
        pattern_id = _clean_text(row.get("pattern_id"))
        if not pattern_id or pattern_id in seen_ids:
            continue
        seen_ids.add(pattern_id)
        unique_patterns.append(row)
    return unique_patterns


def build_expanded_prompt_pack(report: dict[str, Any]) -> dict[str, Any]:
    prompt_pack = build_prompt_pack(report)
    patterns = _build_epistemic_patterns(report)
    prompt_pack["metadata"]["epistemic_pattern_count"] = len(patterns)
    prompt_pack["summary"] = [
        *prompt_pack.get("summary", []),
        "Cross-cutting epistemic patterns are included to cover discovery moves that are not reducible to one bridge family.",
    ]
    prompt_pack["epistemic_patterns"] = patterns
    return prompt_pack


def _slug(value: Any) -> str:
    text = _clean_text(value).lower()
    slug = []
    last_was_dash = False
    for char in text:
        if char.isalnum():
            slug.append(char)
            last_was_dash = False
            continue
        if not last_was_dash:
            slug.append("-")
            last_was_dash = True
    return "".join(slug).strip("-") or "item"


def _profile_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]


def _linked_profile_rows(
    report: dict[str, Any],
    *,
    family: str = "",
    obstruction_class: str = "",
    families: list[str] | None = None,
    obstruction_classes: list[str] | None = None,
) -> list[dict[str, Any]]:
    rows = _profile_rows(report)
    family_set = {_clean_text(value) for value in (families or []) if _clean_text(value)}
    obstruction_set = {_clean_text(value) for value in (obstruction_classes or []) if _clean_text(value)}
    if _clean_text(family):
        family_set.add(_clean_text(family))
    if _clean_text(obstruction_class):
        obstruction_set.add(_clean_text(obstruction_class))
    matched: list[dict[str, Any]] = []
    for row in rows:
        row_family = _clean_text(row.get("breakthrough_family"))
        row_obstruction = _clean_text(row.get("obstruction_class"))
        if family_set and row_family in family_set:
            matched.append(row)
            continue
        if obstruction_set and row_obstruction in obstruction_set:
            matched.append(row)
    return matched


def _union_text(rows: list[dict[str, Any]], field: str, *, limit: int = 12) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        for value in [_clean_text(item) for item in _ensure_list(row.get(field)) if _clean_text(item)]:
            if value in seen:
                continue
            seen.add(value)
            ordered.append(value)
            if len(ordered) >= limit:
                return ordered
    return ordered


def _discovery_deliverables(
    *,
    layer_kind: str,
    target_label: str,
    minimal_theorem_shape: str,
    abstraction_required: str,
) -> list[str]:
    if layer_kind == "breakthrough-family":
        return [
            _clean_text(f"State one theorem-shaped candidate centered on `{target_label}` satisfying `{minimal_theorem_shape}`."),
            _clean_text(f"Make `{abstraction_required}` explicit enough that an expert could inspect the object or transfer law."),
            "Record one decisive negative route explaining what would fail if this discovery layer does not land.",
        ]
    return [
        _clean_text(f"Produce one reframing under `{target_label}` that changes the search state rather than restating the blocked lemma."),
        _clean_text(f"Connect the reframing back to a theorem-shaped objective compatible with `{minimal_theorem_shape}`."),
        "Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.",
    ]


def _discovery_stop_criteria(
    *,
    layer_kind: str,
    anti_patterns: list[str],
    target_label: str,
) -> list[str]:
    criteria = [
        "Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.",
        "Stop after one explicit positive candidate and one explicit failure probe have both been recorded.",
    ]
    if anti_patterns:
        criteria.insert(0, _clean_text(f"Stop immediately if the branch collapses into the anti-pattern `{anti_patterns[0]}`."))
    if layer_kind == "epistemic-pattern":
        criteria.append(
            _clean_text(
                f"Escalate if `{target_label}` only re-labels the blocked frontier instead of reducing proof debt or changing the representation."
            )
        )
    else:
        criteria.append(
            _clean_text(
                f"Escalate if `{target_label}` remains purely schematic after the first explicit object or theorem candidate."
            )
        )
    return criteria


FOUNDATION_FRAMEWORK_HINTS: dict[str, list[str]] = {
    "abstraction-search": [
        "proof complexity",
        "pseudorandomness / derandomization",
        "coding-theoretic hardness surrogates",
    ],
    "realization": [
        "proof complexity witness measures",
        "coding theory",
        "pseudorandom objects and hardness amplification",
    ],
    "transport": [
        "formula lower-bound transfer frameworks",
        "communication complexity model-transfer methods",
        "representation/normal-form theorems in circuit complexity",
    ],
    "alignment": [
        "sparse-object and distinguisher frameworks",
        "duality or correspondence theorems",
        "representation-theoretic normal forms",
    ],
    "explicitness": [
        "derandomization and generator frameworks",
        "algebraic certificate constructions",
        "extractor / hitter frameworks",
    ],
    "barrier-aware transfer": [
        "lower-bound barrier frameworks",
        "local-reduction impossibility theory",
        "gadget and locality-preservation frameworks",
    ],
    "constructive instantiation": [
        "canonical example construction frameworks",
        "natural proof or canonicalization methods",
        "explicit reduction template families",
    ],
    "semantic bridge": [
        "duality frameworks",
        "characterization theorems in proof complexity",
        "semantic completeness correspondences",
    ],
    "bridge-specificity": [
        "activation-theorem frameworks",
        "hypothesis-verification templates from neighboring areas",
    ],
    "invariant-discovery": [
        "potential / energy method frameworks",
        "monotone measure frameworks",
        "certificate-complexity and witness-measure theories",
    ],
    "regime-localization": [
        "threshold and regime-restriction frameworks",
        "restricted-model lower-bound programmes",
    ],
    "problem-representation-shift": [
        "normal-form frameworks",
        "equivalent reformulation theorems",
        "model/encoding correspondence theories",
    ],
    "counterexample-led-concept-formation": [
        "barrier and impossibility frameworks",
        "minimal obstruction and forbidden-configuration theories",
    ],
    "route-decomposition": [
        "interface decomposition frameworks",
        "multi-stage lifting and factorization methods",
    ],
    "hybridization-of-partial-bridges": [
        "composed transfer frameworks",
        "hybrid argument methods",
        "multi-interface reduction theories",
    ],
    "categorical-reframing": [
        "category-theoretic composition and factorization methods",
        "universal-property and adjunction frameworks",
        "diagrammatic commutativity methods",
    ],
    "equivalence-coherence-reframing": [
        "homotopy type theory",
        "equivalence and transport frameworks",
        "coherence and identity-type methods",
    ],
}


def _external_framework_search_gate(layer: dict[str, Any]) -> dict[str, Any]:
    layer_kind = _clean_text(layer.get("layer_kind"))
    target_id = _clean_text(layer.get("target_id"))
    linked_families = {
        _clean_text(value)
        for value in _ensure_list(layer.get("linked_breakthrough_families"))
        if _clean_text(value)
    }
    queue_count = len([value for value in _ensure_list(layer.get("linked_queue_ids")) if _clean_text(value)])
    search_modes = " ".join(_clean_text(value) for value in _ensure_list(layer.get("search_modes"))).lower()
    anti_patterns = [_clean_text(value) for value in _ensure_list(layer.get("anti_patterns")) if _clean_text(value)]

    structural_trigger = any(
        token in search_modes
        for token in ("equivalence", "correspondence", "normal form", "transport", "compilation", "duality", "extractor", "generator")
    )
    pattern_trigger = target_id in {
        "invariant-discovery",
        "problem-representation-shift",
        "hybridization-of-partial-bridges",
        "route-decomposition",
        "regime-localization",
    }
    family_trigger = bool(
        linked_families
        & {
            "abstraction-search",
            "realization",
            "transport",
            "alignment",
            "explicitness",
            "semantic bridge",
            "barrier-aware transfer",
        }
    )
    breadth_trigger = queue_count >= 3 or len(linked_families) >= 2
    recommend = structural_trigger or pattern_trigger or family_trigger or breadth_trigger

    framework_regions: list[str] = []
    for family in ([target_id] if layer_kind == "epistemic-pattern" else []) + sorted(linked_families):
        framework_regions.extend(FOUNDATION_FRAMEWORK_HINTS.get(family, []))
    if not framework_regions and target_id:
        framework_regions.extend(FOUNDATION_FRAMEWORK_HINTS.get(target_id, []))
    framework_regions = list(dict.fromkeys([_clean_text(value) for value in framework_regions if _clean_text(value)]))

    target_label = _clean_text(layer.get("target_label")) or target_id
    missing_move = _clean_text(layer.get("required_move"))
    minimal_theorem_shape = _clean_text(layer.get("minimal_theorem_shape"))
    query_templates = []
    if recommend:
        query_templates = [
            _clean_text(f"mathematical framework for {target_label} with preserved invariant and bridge theorem"),
            _clean_text(f"{target_label} correspondence theorem transport invariant"),
            _clean_text(f"{target_label} framework {missing_move} theorem"),
        ]
        if minimal_theorem_shape:
            query_templates.append(_clean_text(f"theorem or framework matching: {minimal_theorem_shape}"))
    return {
        "recommended": recommend,
        "mode": "targeted-foundation-search" if recommend else "local-only",
        "justification": _clean_text(
            "Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem."
            if recommend
            else "Keep the branch local because the current layer is still specific enough to refine without framework search."
        ),
        "heuristic_triggers": [
            trigger
            for trigger, active in (
                ("structural-analogy", structural_trigger),
                ("cross-family-pressure", breadth_trigger),
                ("pattern-level-reframing", pattern_trigger),
                ("bridge-family-foundation-gap", family_trigger),
            )
            if active
        ],
        "local_prerequisites": [
            "Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.",
            "State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.",
            "Reject at least one purely topical analogy before searching for an external framework.",
        ],
        "candidate_framework_regions": framework_regions[:5],
        "query_templates": query_templates[:4],
        "import_rule": "If an external theorem, definition, axiom, or named framework becomes proof-relevant, import it into InformalMathLib rather than leaving it as loose inspiration.",
        "anti_patterns": anti_patterns[:2],
    }


def _layer_priority(
    *,
    base_pressure: float,
    queue_count: int,
    reference_count: int,
    family_count: int,
    layer_kind: str,
) -> float:
    priority = base_pressure + 0.045 * queue_count + 0.03 * reference_count + 0.04 * family_count
    if layer_kind == "breakthrough-family":
        priority += 0.12
    return round(priority, 3)


def _build_discovery_layers(report: dict[str, Any], prompt_pack: dict[str, Any]) -> list[dict[str, Any]]:
    layers: list[dict[str, Any]] = []
    family_rows = [row for row in _ensure_list(prompt_pack.get("prompt_packs")) if isinstance(row, dict)]
    pattern_rows = [row for row in _ensure_list(prompt_pack.get("epistemic_patterns")) if isinstance(row, dict)]

    for row in family_rows:
        family = _clean_text(row.get("breakthrough_family")) or "abstraction-search"
        linked_profiles = _linked_profile_rows(
            report,
            family=family,
            obstruction_class=_clean_text(row.get("obstruction_class")),
        )
        queue_ids = [_clean_text(value) for value in _ensure_list(row.get("linked_queue_ids")) if _clean_text(value)]
        reference_ids = [_clean_text(value) for value in _ensure_list(row.get("linked_reference_ids")) if _clean_text(value)]
        linked_obstructions = [
            _clean_text(value)
            for value in [_clean_text(profile.get("obstruction_class")) for profile in linked_profiles]
            if value
        ]
        sample_targets = [_clean_text(value) for value in _ensure_list(row.get("sample_theorem_targets")) if _clean_text(value)]
        base_pressure = max((_safe_float(profile.get("pressure_score")) for profile in linked_profiles), default=0.0)
        layers.append(
            {
                "layer_id": f"disclayer.{_clean_text(_ensure_dict(report.get('metadata')).get('kb_ref'))}.family.{_slug(family)}",
                "layer_kind": "breakthrough-family",
                "target_id": family,
                "target_label": _clean_text(row.get("prompt_title")) or family,
                "routing_priority": _layer_priority(
                    base_pressure=base_pressure,
                    queue_count=len(queue_ids),
                    reference_count=len(reference_ids),
                    family_count=1,
                    layer_kind="breakthrough-family",
                ),
                "spawn_reason": _clean_text(
                    f"Spawn a dedicated `{family}` discovery layer because obstruction `{row.get('obstruction_class', '')}` carries repeated pressure across the blocked frontier."
                ),
                "rationale": _clean_text(row.get("required_move")),
                "status": "pending",
                "linked_queue_ids": queue_ids,
                "linked_reference_ids": reference_ids,
                "linked_breakthrough_families": [
                    _clean_text(value)
                    for value in (_ensure_list(row.get("linked_breakthrough_families")) or [family])
                    if _clean_text(value)
                ],
                "linked_obstruction_classes": linked_obstructions or [_clean_text(row.get("obstruction_class"))],
                "required_move": _clean_text(row.get("required_move")),
                "abstraction_required": _clean_text(row.get("abstraction_required")),
                "minimal_theorem_shape": _clean_text(row.get("minimal_theorem_shape")),
                "system_prompt": _clean_text(row.get("system_prompt")),
                "user_task": _clean_text(row.get("user_task")),
                "required_questions": list(row.get("required_questions", [])),
                "search_modes": list(row.get("search_modes", [])),
                "anti_patterns": list(row.get("anti_patterns", [])),
                "sample_theorem_targets": sample_targets[:2],
                "routing_heuristic": _ensure_dict(row.get("routing_heuristic")),
                "epistemic_lens": _clean_text(row.get("epistemic_lens")),
                "lens_artifacts": _ensure_dict(row.get("lens_artifacts")),
                "negative_outputs": [
                    _clean_text(value)
                    for value in _ensure_list(_ensure_dict(row.get("lens_artifacts")).get("negative_outputs"))
                    if _clean_text(value)
                ],
                "expected_deliverables": _discovery_deliverables(
                    layer_kind="breakthrough-family",
                    target_label=family,
                    minimal_theorem_shape=_clean_text(row.get("minimal_theorem_shape")),
                    abstraction_required=_clean_text(row.get("abstraction_required")),
                ),
                "stop_criteria": _discovery_stop_criteria(
                    layer_kind="breakthrough-family",
                    anti_patterns=list(row.get("anti_patterns", [])),
                    target_label=family,
                ),
            }
        )
        layers[-1]["external_framework_search"] = _external_framework_search_gate(layers[-1])

    for row in pattern_rows:
        pattern_id = _clean_text(row.get("pattern_id"))
        linked_profiles = _linked_profile_rows(
            report,
            families=[_clean_text(value) for value in _ensure_list(row.get("linked_breakthrough_families"))],
            obstruction_classes=[_clean_text(value) for value in _ensure_list(row.get("linked_obstruction_classes"))],
        )
        queue_ids = [_clean_text(value) for value in _ensure_list(row.get("linked_queue_ids")) if _clean_text(value)]
        linked_families = [
            _clean_text(value)
            for value in _ensure_list(row.get("linked_breakthrough_families"))
            if _clean_text(value)
        ]
        reference_ids = _union_text(linked_profiles, "reference_ids")
        base_pressure = max((_safe_float(profile.get("pressure_score")) for profile in linked_profiles), default=0.0)
        layers.append(
            {
                "layer_id": f"disclayer.{_clean_text(_ensure_dict(report.get('metadata')).get('kb_ref'))}.pattern.{_slug(pattern_id)}",
                "layer_kind": "epistemic-pattern",
                "target_id": pattern_id,
                "target_label": _clean_text(row.get("prompt_title")) or pattern_id,
                "routing_priority": _layer_priority(
                    base_pressure=base_pressure,
                    queue_count=len(queue_ids),
                    reference_count=len(reference_ids),
                    family_count=len(linked_families),
                    layer_kind="epistemic-pattern",
                ),
                "spawn_reason": _clean_text(
                    f"Spawn `{pattern_id}` as a cross-cutting discovery layer because the blocked frontier spans multiple breakthrough families and needs a broader reframing."
                ),
                "rationale": _clean_text(row.get("rationale")),
                "status": "pending",
                "linked_queue_ids": queue_ids,
                "linked_reference_ids": reference_ids,
                "linked_breakthrough_families": linked_families,
                "linked_obstruction_classes": [
                    _clean_text(value)
                    for value in _ensure_list(row.get("linked_obstruction_classes"))
                    if _clean_text(value)
                ],
                "required_move": _clean_text(row.get("rationale")),
                "abstraction_required": _clean_text(row.get("user_task")),
                "minimal_theorem_shape": _clean_text(
                    (_ensure_list(row.get("sample_theorem_targets")) or [""])[0]
                ),
                "system_prompt": _clean_text(row.get("system_prompt")),
                "user_task": _clean_text(row.get("user_task")),
                "required_questions": list(row.get("required_questions", [])),
                "search_modes": list(row.get("search_modes", [])),
                "anti_patterns": list(row.get("anti_patterns", [])),
                "sample_theorem_targets": [
                    _clean_text(value)
                    for value in _ensure_list(row.get("sample_theorem_targets"))
                    if _clean_text(value)
                ][:2],
                "routing_heuristic": _ensure_dict(row.get("routing_heuristic")),
                "epistemic_lens": _clean_text(row.get("epistemic_lens")),
                "lens_artifacts": _ensure_dict(row.get("lens_artifacts")),
                "negative_outputs": [
                    _clean_text(value)
                    for value in _ensure_list(_ensure_dict(row.get("lens_artifacts")).get("negative_outputs"))
                    if _clean_text(value)
                ],
                "expected_deliverables": _discovery_deliverables(
                    layer_kind="epistemic-pattern",
                    target_label=pattern_id,
                    minimal_theorem_shape=_clean_text((_ensure_list(row.get("sample_theorem_targets")) or [""])[0]),
                    abstraction_required=_clean_text(row.get("user_task")),
                ),
                "stop_criteria": _discovery_stop_criteria(
                    layer_kind="epistemic-pattern",
                    anti_patterns=list(row.get("anti_patterns", [])),
                    target_label=pattern_id,
                ),
            }
        )
        layers[-1]["external_framework_search"] = _external_framework_search_gate(layers[-1])
    return layers


def _build_dispatch_plan(layers: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    remaining = [dict(layer) for layer in layers]
    selected: list[dict[str, Any]] = []
    seen_targets: set[str] = set()
    seen_families: set[str] = set()
    while remaining:
        last_kind = _clean_text(selected[-1].get("layer_kind")) if selected else ""

        def sort_key(layer: dict[str, Any]) -> tuple[Any, ...]:
            layer_kind = _clean_text(layer.get("layer_kind"))
            linked_families = {
                _clean_text(value)
                for value in _ensure_list(layer.get("linked_breakthrough_families"))
                if _clean_text(value)
            }
            target_id = _clean_text(layer.get("target_id"))
            repeated_kind_penalty = 1 if last_kind and layer_kind == last_kind else 0
            no_new_family_penalty = 1 if linked_families and linked_families <= seen_families else 0
            repeated_target_penalty = 1 if target_id in seen_targets else 0
            return (
                repeated_kind_penalty,
                no_new_family_penalty,
                repeated_target_penalty,
                -_safe_float(layer.get("routing_priority")),
                -len(_ensure_list(layer.get("linked_queue_ids"))),
                target_id,
            )

        next_layer = sorted(remaining, key=sort_key)[0]
        remaining.remove(next_layer)
        selected.append(next_layer)
        seen_targets.add(_clean_text(next_layer.get("target_id")))
        for family in _ensure_list(next_layer.get("linked_breakthrough_families")):
            family_text = _clean_text(family)
            if family_text:
                seen_families.add(family_text)

    for rank, layer in enumerate(selected, start=1):
        layer["dispatch_rank"] = rank
        layer["dispatch_round"] = ((rank - 1) // 3) + 1

    rounds: list[dict[str, Any]] = []
    for start in range(0, len(selected), 3):
        batch = selected[start : start + 3]
        round_number = (start // 3) + 1
        round_families = []
        for row in batch:
            round_families.extend(
                [
                    _clean_text(value)
                    for value in _ensure_list(row.get("linked_breakthrough_families"))
                    if _clean_text(value)
                ]
            )
        rounds.append(
            {
                "round_number": round_number,
                "layer_ids": [_clean_text(row.get("layer_id")) for row in batch if _clean_text(row.get("layer_id"))],
                "rationale": _clean_text(
                    "Alternate targeted family branches with broader epistemic patterns to avoid collapsing into one depth-first line of search."
                ),
                "covered_breakthrough_families": list(dict.fromkeys(round_families)),
            }
        )
    return selected, rounds


def build_discovery_pattern_routing(report: dict[str, Any], prompt_pack: dict[str, Any]) -> dict[str, Any]:
    layers = _build_discovery_layers(report, prompt_pack)
    ordered_layers, rounds = _build_dispatch_plan(layers)
    return {
        "metadata": {
            "kb_ref": _ensure_dict(report.get("metadata")).get("kb_ref", ""),
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "layer_count": len(ordered_layers),
            "family_layer_count": sum(1 for row in ordered_layers if _clean_text(row.get("layer_kind")) == "breakthrough-family"),
            "pattern_layer_count": sum(1 for row in ordered_layers if _clean_text(row.get("layer_kind")) == "epistemic-pattern"),
            "dispatch_round_count": len(rounds),
        },
        "summary": [
            "Discovery layers are now spawned from prompt packs rather than stored only as passive prompt artifacts.",
            "Routing alternates breakthrough-family branches with cross-cutting epistemic-pattern branches to avoid indeterminate depth-first search.",
            "Each layer records its own theorem target, stop criteria, and expected deliverables so discovery remains inspectable and finite.",
            "Each layer also carries a local-first heuristic for when to search externally for a mathematical framework with similar structural properties.",
        ],
        "routing_policy": [
            "Prioritize pressure on the blocked frontier, but enforce diversity across layer kinds and breakthrough families.",
            "Use family-specific layers to attack concrete bridge defects and epistemic-pattern layers to change representation, invariants, or decomposition when local search stalls.",
            "Escalate or stop when a layer only reproduces its anti-patterns or fails to yield a theorem-shaped claim.",
            "Trigger external framework search only after a recorded local failure, and only when the missing move is better modeled as a borrowed foundation than as another local lemma.",
        ],
        "recommended_layer_order": [
            {
                "dispatch_rank": int(row.get("dispatch_rank", 0) or 0),
                "layer_id": _clean_text(row.get("layer_id")),
                "target_id": _clean_text(row.get("target_id")),
                "layer_kind": _clean_text(row.get("layer_kind")),
                "routing_priority": _safe_float(row.get("routing_priority")),
            }
            for row in ordered_layers
        ],
        "dispatch_rounds": rounds,
        "discovery_layers": ordered_layers,
    }


def spawn_discovery_branches(
    routing: dict[str, Any],
    *,
    artifacts_dir: Path,
    activate_top_k: int = 4,
) -> tuple[dict[str, Any], tuple[Path, Path], list[dict[str, str]]]:
    """Turn routed discovery layers into persistent branch state plus branch dossiers."""

    kb_ref = _clean_text(_ensure_dict(routing.get("metadata")).get("kb_ref")) or kb_ref_from_artifacts_dir(artifacts_dir)
    branch_json, branch_md = discovery_branch_paths(artifacts_dir)
    state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
    state = materialize_discovery_branches(
        routing=routing,
        existing_state=state,
        artifacts_dir=artifacts_dir,
        activate_top_k=max(1, activate_top_k),
    )
    save_discovery_branch_state(state, json_path=branch_json, md_path=branch_md)
    dossiers = write_discovery_branch_dossiers(state, artifacts_dir=artifacts_dir)
    return state, (branch_json, branch_md), dossiers


def _lens_artifact_sections_markdown(lens_artifacts: dict[str, Any]) -> list[str]:
    sections: list[str] = []
    field_titles = [
        ("diagram_candidates", "Diagram Candidates"),
        ("commutativity_obligations", "Commutativity Obligations"),
        ("universal_property_candidates", "Universal Property Candidates"),
        ("equivalence_claims", "Equivalence Claims"),
        ("transport_obligations", "Transport Obligations"),
        ("coherence_failures", "Coherence Failures"),
        ("negative_outputs", "Negative Outputs"),
    ]
    for field, title in field_titles:
        values = [_clean_text(value) for value in _ensure_list(lens_artifacts.get(field)) if _clean_text(value)]
        if not values:
            continue
        sections.extend(["", f"#### {title}", ""])
        for item in values:
            sections.append(f"- {item}")
    return sections


def _routing_heuristic_sections_markdown(heuristic: dict[str, Any]) -> list[str]:
    heuristic = _ensure_dict(heuristic)
    if not heuristic:
        return []
    sections = [
        "",
        "#### Routing Heuristic",
        "",
        f"- Recommended: {heuristic.get('recommended', False)}",
        f"- Score: {heuristic.get('score', 0)} / threshold {heuristic.get('threshold', 0)}",
        f"- Decision rule: {heuristic.get('decision_rule', '')}",
        f"- Rationale: {heuristic.get('rationale', '')}",
    ]
    criteria = [row for row in _ensure_list(heuristic.get("criteria")) if isinstance(row, dict)]
    if criteria:
        sections.extend(["", "#### Active Criteria", ""])
        for row in criteria:
            if row.get("active"):
                sections.append(f"- {row.get('criterion_id', '')}: {row.get('detail', '')}")
    anti = [row for row in _ensure_list(heuristic.get("anti_triggers")) if isinstance(row, dict) and row.get("active")]
    if anti:
        sections.extend(["", "#### Anti-Triggers", ""])
        for row in anti:
            sections.append(f"- {row.get('trigger_id', '')}: {row.get('detail', '')}")
    return sections


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    profiles = [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]
    lines = [
        "# Discovery Breakthrough Profile",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Breakthrough profiles: {meta.get('profile_count', 0)}",
        f"- Covered queue items: {meta.get('covered_queue_count', 0)}",
        "",
        "## Discovery Diagnosis",
        "",
        f"{report.get('search_justification', '')}",
        "",
        "## Summary",
        "",
    ]
    for item in _ensure_list(report.get("summary")):
        if _clean_text(item):
            lines.append(f"- {item}")
    lines.append("")
    lines.extend(["## Breakthrough Profiles", ""])
    for row in profiles:
        lines.extend(
            [
                f"### {row.get('obstruction_class', '')}",
                "",
                f"- Breakthrough family: {row.get('breakthrough_family', '')}",
                f"- Pressure score: {row.get('pressure_score', 0.0):.3f}",
                f"- Top queue priority: {row.get('top_priority', 0.0):.3f}",
                f"- Required move: {row.get('required_move', '')}",
                f"- Abstraction required: {row.get('abstraction_required', '')}",
                f"- Minimal theorem shape: {row.get('minimal_theorem_shape', '')}",
                f"- Major subresult type: {row.get('major_subresult_type', '')}",
                f"- Queue IDs: {', '.join(row.get('queue_ids', []))}",
                f"- Reference IDs: {', '.join(row.get('reference_ids', []))}",
                "",
                "#### Search Modes",
                "",
            ]
        )
        for item in row.get("search_modes", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Anti-Patterns", ""])
        for item in row.get("anti_patterns", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Effect Notes", ""])
        for item in row.get("effect_notes", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Sample Frontier Statements", ""])
        for item in row.get("sample_theorem_targets", []):
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_prompt_pack_markdown(prompt_pack: dict[str, Any]) -> str:
    meta = _ensure_dict(prompt_pack.get("metadata"))
    rows = [row for row in _ensure_list(prompt_pack.get("prompt_packs")) if isinstance(row, dict)]
    patterns = [row for row in _ensure_list(prompt_pack.get("epistemic_patterns")) if isinstance(row, dict)]
    lines = [
        "# Discovery Family Prompts",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Prompt families: {meta.get('prompt_family_count', 0)}",
        f"- Epistemic patterns: {meta.get('epistemic_pattern_count', 0)}",
        "",
        "## Summary",
        "",
    ]
    for item in _ensure_list(prompt_pack.get("summary")):
        if _clean_text(item):
            lines.append(f"- {item}")
    lines.extend(["", "## Prompt Packs", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row.get('breakthrough_family', '')}",
                "",
                f"- Prompt title: {row.get('prompt_title', '')}",
                f"- Epistemic lens: {row.get('epistemic_lens', '')}",
                f"- Obstruction class: {row.get('obstruction_class', '')}",
                f"- Required move: {row.get('required_move', '')}",
                f"- Abstraction required: {row.get('abstraction_required', '')}",
                f"- Minimal theorem shape: {row.get('minimal_theorem_shape', '')}",
                f"- Linked queue IDs: {', '.join(row.get('linked_queue_ids', []))}",
                "",
                "#### System Prompt",
                "",
                row.get("system_prompt", ""),
                "",
                "#### User Task",
                "",
                row.get("user_task", ""),
                "",
                "#### Required Questions",
                "",
            ]
        )
        for item in row.get("required_questions", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Search Modes", ""])
        for item in row.get("search_modes", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Anti-Patterns", ""])
        for item in row.get("anti_patterns", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Sample Theorem Targets", ""])
        for item in row.get("sample_theorem_targets", []):
            lines.append(f"- {item}")
        lines.extend(_routing_heuristic_sections_markdown(_ensure_dict(row.get("routing_heuristic"))))
        lines.extend(_lens_artifact_sections_markdown(_ensure_dict(row.get("lens_artifacts"))))
        lines.append("")
    lines.extend(["## Cross-Cutting Epistemic Patterns", ""])
    for row in patterns:
        lines.extend(
            [
                f"### {row.get('pattern_id', '')}",
                "",
                f"- Prompt title: {row.get('prompt_title', '')}",
                f"- Rationale: {row.get('rationale', '')}",
                f"- Linked breakthrough families: {', '.join(row.get('linked_breakthrough_families', []))}",
                f"- Linked queue IDs: {', '.join(row.get('linked_queue_ids', []))}",
                "",
                "#### System Prompt",
                "",
                row.get("system_prompt", ""),
                "",
                "#### User Task",
                "",
                row.get("user_task", ""),
                "",
                "#### Required Questions",
                "",
            ]
        )
        for item in row.get("required_questions", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Search Modes", ""])
        for item in row.get("search_modes", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Anti-Patterns", ""])
        for item in row.get("anti_patterns", []):
            lines.append(f"- {item}")
        lines.extend(["", "#### Sample Theorem Targets", ""])
        for item in row.get("sample_theorem_targets", []):
            lines.append(f"- {item}")
        lines.extend(_routing_heuristic_sections_markdown(_ensure_dict(row.get("routing_heuristic"))))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_discovery_lens_artifacts(report: dict[str, Any], prompt_pack: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
    lenses = []
    routing_index = {
        _clean_text(row.get("target_id")): row
        for row in _ensure_list(routing.get("discovery_layers"))
        if isinstance(row, dict) and _clean_text(row.get("target_id"))
    }
    for row in _ensure_list(prompt_pack.get("prompt_packs")):
        if not isinstance(row, dict):
            continue
        family = _clean_text(row.get("breakthrough_family"))
        if family not in {"categorical-reframing", "equivalence-coherence-reframing"}:
            continue
        route_row = _ensure_dict(routing_index.get(family))
        lenses.append(
            {
                "lens_id": family,
                "prompt_title": _clean_text(row.get("prompt_title")),
                "epistemic_lens": _clean_text(row.get("epistemic_lens")),
                "required_move": _clean_text(row.get("required_move")),
                "linked_queue_ids": [
                    _clean_text(value)
                    for value in _ensure_list(row.get("linked_queue_ids"))
                    if _clean_text(value)
                ],
                "linked_breakthrough_families": [
                    _clean_text(value)
                    for value in _ensure_list(route_row.get("linked_breakthrough_families"))
                    if _clean_text(value)
                ],
                "routing_heuristic": _ensure_dict(row.get("routing_heuristic")),
                "lens_artifacts": _ensure_dict(row.get("lens_artifacts")),
            }
        )
    return {
        "metadata": {
            "kb_ref": _ensure_dict(report.get("metadata")).get("kb_ref", ""),
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "lens_count": len(lenses),
        },
        "summary": [
            "Category theory is used here as a structural/compositional discovery lens for composition, mediation, commutativity, and universal properties.",
            "HoTT is used here as an equivalence/coherence discovery lens for sameness, transport, and representation coherence.",
            "Neither lens replaces PDL. Each enriches the outer discovery logic with a specific mode of material inference.",
        ],
        "lenses": lenses,
    }


def render_discovery_lens_artifacts_markdown(artifacts: dict[str, Any]) -> str:
    meta = _ensure_dict(artifacts.get("metadata"))
    lines = [
        "# Discovery Lens Artifacts",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Lenses: {meta.get('lens_count', 0)}",
        "",
        "## Summary",
        "",
    ]
    for item in _ensure_list(artifacts.get("summary")):
        if _clean_text(item):
            lines.append(f"- {item}")
    lines.extend(["", "## Lenses", ""])
    for row in _ensure_list(artifacts.get("lenses")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {row.get('lens_id', '')}",
                "",
                f"- Prompt title: {row.get('prompt_title', '')}",
                f"- Epistemic lens: {row.get('epistemic_lens', '')}",
                f"- Required move: {row.get('required_move', '')}",
                f"- Linked queue IDs: {', '.join(_ensure_list(row.get('linked_queue_ids')))}",
                f"- Linked breakthrough families: {', '.join(_ensure_list(row.get('linked_breakthrough_families')))}",
            ]
        )
        lines.extend(_routing_heuristic_sections_markdown(_ensure_dict(row.get("routing_heuristic"))))
        lines.extend(_lens_artifact_sections_markdown(_ensure_dict(row.get("lens_artifacts"))))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_discovery_pattern_routing_markdown(routing: dict[str, Any]) -> str:
    meta = _ensure_dict(routing.get("metadata"))
    layers = [row for row in _ensure_list(routing.get("discovery_layers")) if isinstance(row, dict)]
    rounds = [row for row in _ensure_list(routing.get("dispatch_rounds")) if isinstance(row, dict)]
    lines = [
        "# Discovery Pattern Routing",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Discovery layers: {meta.get('layer_count', 0)}",
        f"- Family layers: {meta.get('family_layer_count', 0)}",
        f"- Pattern layers: {meta.get('pattern_layer_count', 0)}",
        f"- Dispatch rounds: {meta.get('dispatch_round_count', 0)}",
        "",
        "## Summary",
        "",
    ]
    for item in _ensure_list(routing.get("summary")):
        if _clean_text(item):
            lines.append(f"- {item}")
    lines.extend(["", "## Routing Policy", ""])
    for item in _ensure_list(routing.get("routing_policy")):
        if _clean_text(item):
            lines.append(f"- {item}")
    lines.extend(["", "## Recommended Dispatch Order", ""])
    for row in _ensure_list(routing.get("recommended_layer_order")):
        if not isinstance(row, dict):
            continue
        lines.append(
            f"1. `{row.get('layer_id', '')}` | {row.get('layer_kind', '')} | {row.get('target_id', '')} | priority {float(row.get('routing_priority', 0.0)):.3f}"
        )
    lines.extend(["", "## Dispatch Rounds", ""])
    for row in rounds:
        lines.append(f"### Round {row.get('round_number', 0)}")
        lines.append("")
        lines.append(f"- Rationale: {row.get('rationale', '')}")
        lines.append(f"- Layers: {', '.join(_ensure_list(row.get('layer_ids')))}")
        lines.append(f"- Covered breakthrough families: {', '.join(_ensure_list(row.get('covered_breakthrough_families')))}")
        lines.append("")
    lines.extend(["## Discovery Layers", ""])
    for row in layers:
        lines.extend(
            [
                f"### {row.get('layer_id', '')}",
                "",
                f"- Kind: {row.get('layer_kind', '')}",
                f"- Target: {row.get('target_id', '')}",
                f"- Routing priority: {float(row.get('routing_priority', 0.0)):.3f}",
                f"- Dispatch rank: {row.get('dispatch_rank', 0)}",
                f"- Dispatch round: {row.get('dispatch_round', 0)}",
                f"- Spawn reason: {row.get('spawn_reason', '')}",
                f"- Rationale: {row.get('rationale', '')}",
                f"- Linked queue IDs: {', '.join(_ensure_list(row.get('linked_queue_ids')))}",
                f"- Linked breakthrough families: {', '.join(_ensure_list(row.get('linked_breakthrough_families')))}",
                f"- Linked obstruction classes: {', '.join(_ensure_list(row.get('linked_obstruction_classes')))}",
                f"- Epistemic lens: {row.get('epistemic_lens', '')}",
                "",
                "#### System Prompt",
                "",
                row.get("system_prompt", ""),
                "",
                "#### User Task",
                "",
                row.get("user_task", ""),
                "",
                "#### Expected Deliverables",
                "",
            ]
        )
        for item in _ensure_list(row.get("expected_deliverables")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Stop Criteria", ""])
        for item in _ensure_list(row.get("stop_criteria")):
            lines.append(f"- {item}")
        gate = _ensure_dict(row.get("external_framework_search"))
        lines.extend(["", "#### External Framework Search Heuristic", ""])
        lines.append(f"- Recommended: {gate.get('recommended', False)}")
        lines.append(f"- Mode: {gate.get('mode', '')}")
        lines.append(f"- Justification: {gate.get('justification', '')}")
        lines.append(f"- Triggers: {', '.join(_ensure_list(gate.get('heuristic_triggers')))}")
        lines.append(f"- Candidate framework regions: {', '.join(_ensure_list(gate.get('candidate_framework_regions')))}")
        lines.extend(["", "#### Local Prerequisites Before Browsing", ""])
        for item in _ensure_list(gate.get("local_prerequisites")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Query Templates", ""])
        for item in _ensure_list(gate.get("query_templates")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Required Questions", ""])
        for item in _ensure_list(row.get("required_questions")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Search Modes", ""])
        for item in _ensure_list(row.get("search_modes")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Anti-Patterns", ""])
        for item in _ensure_list(row.get("anti_patterns")):
            lines.append(f"- {item}")
        lines.extend(["", "#### Sample Theorem Targets", ""])
        for item in _ensure_list(row.get("sample_theorem_targets")):
            lines.append(f"- {item}")
        lines.extend(_routing_heuristic_sections_markdown(_ensure_dict(row.get("routing_heuristic"))))
        lines.extend(_lens_artifact_sections_markdown(_ensure_dict(row.get("lens_artifacts"))))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    profiles = [row for row in _ensure_list(report.get("profiles")) if isinstance(row, dict)]
    sections: list[str] = []
    for row in profiles:
        pressure_text = f"{row.get('pressure_score', 0.0):.3f}"
        sections.append(
            "\n".join(
                [
                    rf"\section{{{_latex_escape(row.get('obstruction_class'))}}}",
                    rf"\textbf{{Breakthrough family.}} {_latex_escape(row.get('breakthrough_family'))}",
                    "",
                    rf"\textbf{{Pressure score.}} {_latex_escape(pressure_text)}",
                    "",
                    rf"\textbf{{Required move.}} {_latex_escape(row.get('required_move'))}",
                    "",
                    rf"\textbf{{Abstraction required.}} {_latex_escape(row.get('abstraction_required'))}",
                    "",
                    rf"\textbf{{Minimal theorem shape.}} {_latex_escape(row.get('minimal_theorem_shape'))}",
                    "",
                    rf"\textbf{{Major subresult type.}} {_latex_escape(row.get('major_subresult_type'))}",
                    "",
                    r"\subsection*{Search Modes}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("search_modes", [])],
                    r"\end{itemize}",
                    r"\subsection*{Anti-Patterns}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("anti_patterns", [])],
                    r"\end{itemize}",
                ]
            )
        )
    if not sections:
        sections.append("No breakthrough profiles recorded.")
    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Discovery Breakthrough Profile for {_latex_escape(meta.get('kb_ref'))}}}
}}

\title{{Discovery Breakthrough Profile for \texttt{{{_latex_escape(meta.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report classifies the blocked discovery frontier by the conceptual breakthrough required to make progress. It reframes the frontier from missing theorems to breakthrough families such as realization, transport, alignment, explicitness, constructive instantiation, and semantic bridging.
\end{{abstract}}

\section{{Summary}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(report.get('summary')) if _clean_text(item))}
\end{{itemize}}

{chr(10).join(sections)}

\end{{document}}
""" 


def render_prompt_pack_tex(prompt_pack: dict[str, Any]) -> str:
    meta = _ensure_dict(prompt_pack.get("metadata"))
    rows = [row for row in _ensure_list(prompt_pack.get("prompt_packs")) if isinstance(row, dict)]
    patterns = [row for row in _ensure_list(prompt_pack.get("epistemic_patterns")) if isinstance(row, dict)]
    sections: list[str] = []
    for row in rows:
        sections.append(
            "\n".join(
                [
                    rf"\section{{{_latex_escape(row.get('breakthrough_family'))}}}",
                    rf"\textbf{{Prompt title.}} {_latex_escape(row.get('prompt_title'))}",
                    "",
                    rf"\textbf{{Obstruction class.}} {_latex_escape(row.get('obstruction_class'))}",
                    "",
                    rf"\textbf{{Required move.}} {_latex_escape(row.get('required_move'))}",
                    "",
                    rf"\textbf{{Abstraction required.}} {_latex_escape(row.get('abstraction_required'))}",
                    "",
                    rf"\textbf{{Minimal theorem shape.}} {_latex_escape(row.get('minimal_theorem_shape'))}",
                    "",
                    r"\subsection*{System Prompt}",
                    _latex_escape(row.get("system_prompt")),
                    "",
                    r"\subsection*{User Task}",
                    _latex_escape(row.get("user_task")),
                    "",
                    r"\subsection*{Required Questions}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("required_questions", [])],
                    r"\end{itemize}",
                    r"\subsection*{Search Modes}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("search_modes", [])],
                    r"\end{itemize}",
                ]
            )
        )
    for row in patterns:
        sections.append(
            "\n".join(
                [
                    rf"\section{{{_latex_escape(row.get('pattern_id'))}}}",
                    rf"\textbf{{Prompt title.}} {_latex_escape(row.get('prompt_title'))}",
                    "",
                    rf"\textbf{{Rationale.}} {_latex_escape(row.get('rationale'))}",
                    "",
                    rf"\textbf{{Linked families.}} {_latex_escape(', '.join(row.get('linked_breakthrough_families', [])))}",
                    "",
                    r"\subsection*{System Prompt}",
                    _latex_escape(row.get("system_prompt")),
                    "",
                    r"\subsection*{User Task}",
                    _latex_escape(row.get("user_task")),
                    "",
                    r"\subsection*{Required Questions}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("required_questions", [])],
                    r"\end{itemize}",
                    r"\subsection*{Search Modes}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in row.get("search_modes", [])],
                    r"\end{itemize}",
                ]
            )
        )
    if not sections:
        sections.append("No discovery-family prompt packs recorded.")
    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Discovery Family Prompts for {_latex_escape(meta.get('kb_ref'))}}}
}}

\title{{Discovery Family Prompts for \texttt{{{_latex_escape(meta.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report materializes family-specific discovery prompts from the current blocked frontier. Each prompt pack corresponds to a conceptual breakthrough family such as realization, transport, alignment, explicitness, constructive instantiation, or semantic bridging.
\end{{abstract}}

\section{{Summary}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(prompt_pack.get('summary')) if _clean_text(item))}
\end{{itemize}}

{chr(10).join(sections)}

\end{{document}}
""" 


def render_discovery_lens_artifacts_tex(artifacts: dict[str, Any]) -> str:
    meta = _ensure_dict(artifacts.get("metadata"))
    sections: list[str] = []
    for row in _ensure_list(artifacts.get("lenses")):
        if not isinstance(row, dict):
            continue
        lens_artifacts = _ensure_dict(row.get("lens_artifacts"))
        sections.append(
            "\n".join(
                [
                    rf"\section{{{_latex_escape(row.get('lens_id'))}}}",
                    rf"\textbf{{Prompt title.}} {_latex_escape(row.get('prompt_title'))}",
                    "",
                    rf"\textbf{{Epistemic lens.}} {_latex_escape(row.get('epistemic_lens'))}",
                    "",
                    rf"\textbf{{Required move.}} {_latex_escape(row.get('required_move'))}",
                    "",
                    rf"\textbf{{Linked queue IDs.}} {_latex_escape(', '.join(_ensure_list(row.get('linked_queue_ids'))))}",
                    "",
                    rf"\textbf{{Linked breakthrough families.}} {_latex_escape(', '.join(_ensure_list(row.get('linked_breakthrough_families'))))}",
                    "",
                    r"\subsection*{Lens Artifacts}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[
                        rf"\item \textbf{{{_latex_escape(title)}}}: {_latex_escape('; '.join(_ensure_list(lens_artifacts.get(field))))}"
                        for field, title in (
                            ("diagram_candidates", "Diagram candidates"),
                            ("commutativity_obligations", "Commutativity obligations"),
                            ("universal_property_candidates", "Universal property candidates"),
                            ("equivalence_claims", "Equivalence claims"),
                            ("transport_obligations", "Transport obligations"),
                            ("coherence_failures", "Coherence failures"),
                            ("negative_outputs", "Negative outputs"),
                        )
                        if _ensure_list(lens_artifacts.get(field))
                    ],
                    r"\end{itemize}",
                ]
            )
        )
    if not sections:
        sections.append("No discovery lens artifacts recorded.")
    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Discovery Lens Artifacts for {_latex_escape(meta.get('kb_ref'))}}}
}}

\title{{Discovery Lens Artifacts for \texttt{{{_latex_escape(meta.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report records the structured discovery artifacts produced by the category-theoretic and HoTT reframing lenses. These lenses complement the outer proof-discovery language by exposing composition, mediation, equivalence, transport, and coherence obligations explicitly.
\end{{abstract}}

\section{{Summary}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(artifacts.get('summary')) if _clean_text(item))}
\end{{itemize}}

{chr(10).join(sections)}

\end{{document}}
"""


def render_discovery_pattern_routing_tex(routing: dict[str, Any]) -> str:
    meta = _ensure_dict(routing.get("metadata"))
    layers = [row for row in _ensure_list(routing.get("discovery_layers")) if isinstance(row, dict)]
    rounds = [row for row in _ensure_list(routing.get("dispatch_rounds")) if isinstance(row, dict)]
    sections: list[str] = []
    sections.append(
        "\n".join(
            [
                r"\section{Dispatch Rounds}",
                *[
                    "\n".join(
                        [
                            rf"\subsection*{{Round {_latex_escape(row.get('round_number'))}}}",
                            rf"\textbf{{Rationale.}} {_latex_escape(row.get('rationale'))}",
                            "",
                            rf"\textbf{{Layers.}} {_latex_escape(', '.join(_ensure_list(row.get('layer_ids'))))}",
                            "",
                            rf"\textbf{{Covered breakthrough families.}} {_latex_escape(', '.join(_ensure_list(row.get('covered_breakthrough_families'))))}",
                        ]
                    )
                    for row in rounds
                ],
            ]
        )
    )
    for row in layers:
        routing_priority_text = f"{_safe_float(row.get('routing_priority')):.3f}"
        gate = _ensure_dict(row.get("external_framework_search"))
        sections.append(
            "\n".join(
                [
                    rf"\section{{{_latex_escape(row.get('layer_id'))}}}",
                    rf"\textbf{{Kind.}} {_latex_escape(row.get('layer_kind'))}",
                    "",
                    rf"\textbf{{Target.}} {_latex_escape(row.get('target_id'))}",
                    "",
                    rf"\textbf{{Routing priority.}} {_latex_escape(routing_priority_text)}",
                    "",
                    rf"\textbf{{Dispatch rank.}} {_latex_escape(row.get('dispatch_rank'))}",
                    "",
                    rf"\textbf{{Spawn reason.}} {_latex_escape(row.get('spawn_reason'))}",
                    "",
                    rf"\textbf{{Rationale.}} {_latex_escape(row.get('rationale'))}",
                    "",
                    r"\subsection*{System Prompt}",
                    _latex_escape(row.get("system_prompt")),
                    "",
                    r"\subsection*{User Task}",
                    _latex_escape(row.get("user_task")),
                    "",
                    r"\subsection*{Expected Deliverables}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(row.get("expected_deliverables"))],
                    r"\end{itemize}",
                    r"\subsection*{Stop Criteria}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(row.get("stop_criteria"))],
                    r"\end{itemize}",
                    r"\subsection*{External Framework Search Heuristic}",
                    rf"\textbf{{Recommended.}} {_latex_escape(gate.get('recommended'))}",
                    "",
                    rf"\textbf{{Mode.}} {_latex_escape(gate.get('mode'))}",
                    "",
                    rf"\textbf{{Justification.}} {_latex_escape(gate.get('justification'))}",
                    "",
                    rf"\textbf{{Triggers.}} {_latex_escape(', '.join(_ensure_list(gate.get('heuristic_triggers'))))}",
                    "",
                    rf"\textbf{{Candidate framework regions.}} {_latex_escape(', '.join(_ensure_list(gate.get('candidate_framework_regions'))))}",
                    "",
                    r"\subsection*{Local Prerequisites Before Browsing}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(gate.get("local_prerequisites"))],
                    r"\end{itemize}",
                    r"\subsection*{Query Templates}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(gate.get("query_templates"))],
                    r"\end{itemize}",
                    r"\subsection*{Required Questions}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(row.get("required_questions"))],
                    r"\end{itemize}",
                    r"\subsection*{Search Modes}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *[rf"\item {_latex_escape(item)}" for item in _ensure_list(row.get("search_modes"))],
                    r"\end{itemize}",
                ]
            )
        )
    if not sections:
        sections.append("No discovery routing layers recorded.")
    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Discovery Pattern Routing for {_latex_escape(meta.get('kb_ref'))}}}
}}

\title{{Discovery Pattern Routing for \texttt{{{_latex_escape(meta.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report turns blocked-frontier prompt packs into an executable discovery-routing layer. It spawns dedicated discovery layers per breakthrough family and per cross-cutting epistemic pattern, then orders them to avoid collapsing into one depth-first search line.
\end{{abstract}}

\section{{Summary}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(routing.get('summary')) if _clean_text(item))}
\end{{itemize}}

\section{{Routing Policy}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(routing.get('routing_policy')) if _clean_text(item))}
\end{{itemize}}

{chr(10).join(sections)}

\end{{document}}
"""


def main() -> int:
    logger = ReasoningLogger("kb-discovery-breakthrough-profiler")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--prior-art-json", default="", help="Optional prior-art-pass-report JSON path.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--output-json", default="", help="Optional breakthrough-profile JSON path.")
    ap.add_argument("--output-md", default="", help="Optional breakthrough-profile Markdown path.")
    ap.add_argument("--output-tex", default="", help="Optional breakthrough-profile TeX path.")
    ap.add_argument("--output-pdf", default="", help="Optional breakthrough-profile PDF path.")
    ap.add_argument("--prompt-output-json", default="", help="Optional discovery-family-prompts JSON path.")
    ap.add_argument("--prompt-output-md", default="", help="Optional discovery-family-prompts Markdown path.")
    ap.add_argument("--prompt-output-tex", default="", help="Optional discovery-family-prompts TeX path.")
    ap.add_argument("--prompt-output-pdf", default="", help="Optional discovery-family-prompts PDF path.")
    ap.add_argument("--routing-output-json", default="", help="Optional discovery-pattern-routing JSON path.")
    ap.add_argument("--routing-output-md", default="", help="Optional discovery-pattern-routing Markdown path.")
    ap.add_argument("--routing-output-tex", default="", help="Optional discovery-pattern-routing TeX path.")
    ap.add_argument("--routing-output-pdf", default="", help="Optional discovery-pattern-routing PDF path.")
    ap.add_argument("--lens-output-json", default="", help="Optional discovery-lens-artifacts JSON path.")
    ap.add_argument("--lens-output-md", default="", help="Optional discovery-lens-artifacts Markdown path.")
    ap.add_argument("--lens-output-tex", default="", help="Optional discovery-lens-artifacts TeX path.")
    ap.add_argument("--lens-output-pdf", default="", help="Optional discovery-lens-artifacts PDF path.")
    ap.add_argument("--activate-top-k", type=int, default=4, help="Number of routed discovery branches to activate immediately.")
    ap.add_argument("--latex-engine", default="auto", help="LaTeX engine preference.")
    ap.add_argument(
        "--compile-pdf",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compile the generated TeX to PDF.",
    )
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for breakthrough profile.")

    prior_art_json = Path(args.prior_art_json) if args.prior_art_json else artifacts_dir / "prior-art-pass-report.json"
    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    if args.queue_json:
        queue_json = Path(args.queue_json)
    if not prior_art_json.is_absolute():
        prior_art_json = (repo_root / prior_art_json).resolve()
    if not queue_json.is_absolute():
        queue_json = (repo_root / queue_json).resolve()

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "discovery-breakthrough-profile.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "discovery-breakthrough-profile.md"
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "discovery-breakthrough-profile.tex"
    output_pdf = Path(args.output_pdf) if args.output_pdf else artifacts_dir / "discovery-breakthrough-profile.pdf"
    prompt_output_json = Path(args.prompt_output_json) if args.prompt_output_json else artifacts_dir / "discovery-family-prompts.json"
    prompt_output_md = Path(args.prompt_output_md) if args.prompt_output_md else artifacts_dir / "discovery-family-prompts.md"
    prompt_output_tex = Path(args.prompt_output_tex) if args.prompt_output_tex else artifacts_dir / "discovery-family-prompts.tex"
    prompt_output_pdf = Path(args.prompt_output_pdf) if args.prompt_output_pdf else artifacts_dir / "discovery-family-prompts.pdf"
    routing_output_json = Path(args.routing_output_json) if args.routing_output_json else artifacts_dir / "discovery-pattern-routing.json"
    routing_output_md = Path(args.routing_output_md) if args.routing_output_md else artifacts_dir / "discovery-pattern-routing.md"
    routing_output_tex = Path(args.routing_output_tex) if args.routing_output_tex else artifacts_dir / "discovery-pattern-routing.tex"
    routing_output_pdf = Path(args.routing_output_pdf) if args.routing_output_pdf else artifacts_dir / "discovery-pattern-routing.pdf"
    lens_output_json = Path(args.lens_output_json) if args.lens_output_json else artifacts_dir / "discovery-lens-artifacts.json"
    lens_output_md = Path(args.lens_output_md) if args.lens_output_md else artifacts_dir / "discovery-lens-artifacts.md"
    lens_output_tex = Path(args.lens_output_tex) if args.lens_output_tex else artifacts_dir / "discovery-lens-artifacts.tex"
    lens_output_pdf = Path(args.lens_output_pdf) if args.lens_output_pdf else artifacts_dir / "discovery-lens-artifacts.pdf"
    if not output_json.is_absolute():
        output_json = (repo_root / output_json).resolve()
    if not output_md.is_absolute():
        output_md = (repo_root / output_md).resolve()
    if not output_tex.is_absolute():
        output_tex = (repo_root / output_tex).resolve()
    if not output_pdf.is_absolute():
        output_pdf = (repo_root / output_pdf).resolve()
    if not prompt_output_json.is_absolute():
        prompt_output_json = (repo_root / prompt_output_json).resolve()
    if not prompt_output_md.is_absolute():
        prompt_output_md = (repo_root / prompt_output_md).resolve()
    if not prompt_output_tex.is_absolute():
        prompt_output_tex = (repo_root / prompt_output_tex).resolve()
    if not prompt_output_pdf.is_absolute():
        prompt_output_pdf = (repo_root / prompt_output_pdf).resolve()
    if not routing_output_json.is_absolute():
        routing_output_json = (repo_root / routing_output_json).resolve()
    if not routing_output_md.is_absolute():
        routing_output_md = (repo_root / routing_output_md).resolve()
    if not routing_output_tex.is_absolute():
        routing_output_tex = (repo_root / routing_output_tex).resolve()
    if not routing_output_pdf.is_absolute():
        routing_output_pdf = (repo_root / routing_output_pdf).resolve()
    if not lens_output_json.is_absolute():
        lens_output_json = (repo_root / lens_output_json).resolve()
    if not lens_output_md.is_absolute():
        lens_output_md = (repo_root / lens_output_md).resolve()
    if not lens_output_tex.is_absolute():
        lens_output_tex = (repo_root / lens_output_tex).resolve()
    if not lens_output_pdf.is_absolute():
        lens_output_pdf = (repo_root / lens_output_pdf).resolve()

    prior_art = _load_json(prior_art_json)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    report = build_report(prior_art=prior_art, queue=queue, kb_ref=kb_ref)
    prompt_pack = build_expanded_prompt_pack(report)
    routing = build_discovery_pattern_routing(report, prompt_pack)
    lens_artifacts = build_discovery_lens_artifacts(report, prompt_pack, routing)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_json.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_md.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_tex.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_pdf.parent.mkdir(parents=True, exist_ok=True)
    routing_output_json.parent.mkdir(parents=True, exist_ok=True)
    routing_output_md.parent.mkdir(parents=True, exist_ok=True)
    routing_output_tex.parent.mkdir(parents=True, exist_ok=True)
    routing_output_pdf.parent.mkdir(parents=True, exist_ok=True)
    lens_output_json.parent.mkdir(parents=True, exist_ok=True)
    lens_output_md.parent.mkdir(parents=True, exist_ok=True)
    lens_output_tex.parent.mkdir(parents=True, exist_ok=True)
    lens_output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")
    prompt_output_json.write_text(json.dumps(prompt_pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prompt_output_md.write_text(render_prompt_pack_markdown(prompt_pack), encoding="utf-8")
    prompt_output_tex.write_text(render_prompt_pack_tex(prompt_pack), encoding="utf-8")
    routing_output_json.write_text(json.dumps(routing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    routing_output_md.write_text(render_discovery_pattern_routing_markdown(routing), encoding="utf-8")
    routing_output_tex.write_text(render_discovery_pattern_routing_tex(routing), encoding="utf-8")
    lens_output_json.write_text(json.dumps(lens_artifacts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lens_output_md.write_text(render_discovery_lens_artifacts_markdown(lens_artifacts), encoding="utf-8")
    lens_output_tex.write_text(render_discovery_lens_artifacts_tex(lens_artifacts), encoding="utf-8")
    branch_state, branch_paths, branch_dossiers = spawn_discovery_branches(
        routing,
        artifacts_dir=artifacts_dir,
        activate_top_k=max(1, args.activate_top_k),
    )
    if args.compile_pdf:
        compile_pdf(output_tex, output_pdf, preferred_engine=args.latex_engine)
        compile_pdf(prompt_output_tex, prompt_output_pdf, preferred_engine=args.latex_engine)
        compile_pdf(routing_output_tex, routing_output_pdf, preferred_engine=args.latex_engine)
        compile_pdf(lens_output_tex, lens_output_pdf, preferred_engine=args.latex_engine)

    logger.step(
        "Generated discovery breakthrough profile",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"profile_count={report.get('metadata', {}).get('profile_count', 0)}",
                f"covered_queue_count={report.get('metadata', {}).get('covered_queue_count', 0)}",
                f"discovery_layers={routing.get('metadata', {}).get('layer_count', 0)}",
                f"branch_count={branch_state.get('metadata', {}).get('branch_count', 0)}",
            ]
        ),
        surface_focus="discovery-breakthrough-profile",
        surface_stage="discovery",
        surface_metrics={
            "profile_count": int(report.get("metadata", {}).get("profile_count", 0) or 0),
            "covered_queue_count": int(report.get("metadata", {}).get("covered_queue_count", 0) or 0),
            "discovery_layers": int(routing.get("metadata", {}).get("layer_count", 0) or 0),
            "branch_count": int(branch_state.get("metadata", {}).get("branch_count", 0) or 0),
        },
        surface_taxonomy={"reasoning_types": ["discovery", "breakthrough-profiling"]},
    )
    logger.add_output("discovery_breakthrough_profile_json", output_json)
    logger.add_output("discovery_breakthrough_profile_md", output_md)
    logger.add_output("discovery_breakthrough_profile_tex", output_tex)
    logger.add_output("discovery_family_prompts_json", prompt_output_json)
    logger.add_output("discovery_family_prompts_md", prompt_output_md)
    logger.add_output("discovery_family_prompts_tex", prompt_output_tex)
    logger.add_output("discovery_pattern_routing_json", routing_output_json)
    logger.add_output("discovery_pattern_routing_md", routing_output_md)
    logger.add_output("discovery_pattern_routing_tex", routing_output_tex)
    logger.add_output("discovery_lens_artifacts_json", lens_output_json)
    logger.add_output("discovery_lens_artifacts_md", lens_output_md)
    logger.add_output("discovery_lens_artifacts_tex", lens_output_tex)
    logger.add_output("discovery_branch_queue_json", branch_paths[0])
    logger.add_output("discovery_branch_queue_md", branch_paths[1])
    for row in branch_dossiers[:6]:
        logger.add_output(f"discovery_branch_{_slug(row.get('branch_id'))}_md", Path(row["md"]))
    if args.compile_pdf:
        logger.add_output("discovery_breakthrough_profile_pdf", output_pdf)
        logger.add_output("discovery_family_prompts_pdf", prompt_output_pdf)
        logger.add_output("discovery_pattern_routing_pdf", routing_output_pdf)
        logger.add_output("discovery_lens_artifacts_pdf", lens_output_pdf)
    log_path = logger.finalize(
        "success",
        summary=f"Generated discovery breakthrough profile for `{kb_ref}`.",
    )
    print(f"[OK] Wrote breakthrough profile JSON: {output_json}")
    print(f"[OK] Wrote breakthrough profile Markdown: {output_md}")
    print(f"[OK] Wrote breakthrough profile TeX: {output_tex}")
    print(f"[OK] Wrote discovery family prompts JSON: {prompt_output_json}")
    print(f"[OK] Wrote discovery family prompts Markdown: {prompt_output_md}")
    print(f"[OK] Wrote discovery family prompts TeX: {prompt_output_tex}")
    print(f"[OK] Wrote discovery pattern routing JSON: {routing_output_json}")
    print(f"[OK] Wrote discovery pattern routing Markdown: {routing_output_md}")
    print(f"[OK] Wrote discovery pattern routing TeX: {routing_output_tex}")
    print(f"[OK] Wrote discovery lens artifacts JSON: {lens_output_json}")
    print(f"[OK] Wrote discovery lens artifacts Markdown: {lens_output_md}")
    print(f"[OK] Wrote discovery lens artifacts TeX: {lens_output_tex}")
    print(f"[OK] Wrote discovery branch queue JSON: {branch_paths[0]}")
    print(f"[OK] Wrote discovery branch queue Markdown: {branch_paths[1]}")
    if args.compile_pdf:
        print(f"[OK] Wrote breakthrough profile PDF: {output_pdf}")
        print(f"[OK] Wrote discovery family prompts PDF: {prompt_output_pdf}")
        print(f"[OK] Wrote discovery pattern routing PDF: {routing_output_pdf}")
        print(f"[OK] Wrote discovery lens artifacts PDF: {lens_output_pdf}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
