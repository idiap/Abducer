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

"""Select mathematical machinery by proof role and controlled interface."""

from __future__ import annotations

from typing import Any

from agentic_common import clean_text, stable_id


ROLES = [
    "construction",
    "representation",
    "invariant_preservation",
    "transfer",
    "witness",
    "obstruction",
    "validation",
]

ROLE_DESCRIPTIONS = {
    "construction": "Builds the target object or a regulated approximation that can be transferred to it.",
    "representation": "Gives the target object a tractable mathematical form.",
    "invariant_preservation": "Keeps essential commitments unchanged across transformations.",
    "transfer": "Moves information between regimes, formalisms, limits, or reconstructed objects.",
    "witness": "Produces a detectable property that would certify the target claim.",
    "obstruction": "Explains why a naive route fails and what must be repaired.",
    "validation": "Checks that the route proves the intended target rather than a nearby proxy.",
}

POLICY = {
    "title": "Abstraction And Machinery Selection Policy",
    "purpose": "Choose mathematical and conceptual machinery by the proof role it controls.",
    "roles": ROLE_DESCRIPTIONS,
    "universal_chain": [
        "raw_target",
        "constructed_object",
        "usable_representation",
        "preserved_invariants",
        "transfer_bridge",
        "witness_or_decisive_test",
        "final_target_claim",
    ],
    "rejection_rules": [
        "Reject machinery that names a field without a controlled interface.",
        "Reject endpoint language used as construction machinery.",
        "Reject proxy evidence used as proof authority without transfer certification.",
        "Reject witness machinery before the target object and representation are available.",
    ],
}


def target_contract_from_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    contract = ledger.get("target_object_contract")
    if isinstance(contract, dict) and contract.get("exact_target_object"):
        return contract
    commitments = [
        clean_text(row.get("label"))
        for row in ledger.get("essential_commitments", [])
        if isinstance(row, dict) and clean_text(row.get("label"))
    ]
    return {
        "exact_target_object": clean_text(ledger.get("target_title")) or "active target object",
        "success_condition": "Satisfy all essential commitments in the active target ledger.",
        "nonweakening_commitments": commitments,
        "forbidden_nearby_problems": ledger.get("forbidden_drift_patterns", []),
        "acceptable_weakenings": ledger.get("accepted_weakenings", []),
    }


def _yang_mills_alignment(family: str) -> dict[str, Any]:
    text = family.lower()
    if "balaban" in text or "rg" in text:
        return {
            "selected_machinery": "renormalisation group and multiscale control",
            "machinery_role": "construction",
            "supporting_roles": ["representation", "transfer", "validation"],
            "current_bottleneck": "construction-to-reconstruction transfer",
            "why_this_is_the_bottleneck": "Scale control must become OS-positive continuum Schwinger functions before any spectral claim belongs to the target theory.",
            "controlled_interface": "regulated gauge-field measures or effective actions -> continuum Schwinger-function object",
            "assumptions_required": [
                "regulated compact simple gauge-field objects are defined",
                "uniform multiscale estimates are available",
                "reflection positivity or a route to OS positivity is preserved",
            ],
            "output_obligation": "Produce a continuum Yang-Mills Schwinger-function family with nontrivial gauge-invariant observables.",
            "required_bridge_obligation": "RG-to-OS bridge lemma with topology, limiting objects, positivity preservation, and nontriviality witness.",
            "why_best_available": "The active obstruction is construction and cutoff removal; RG directly controls scale dependence rather than postulating the continuum object.",
            "machinery_needed_because": "The target cannot be reached by a spectral endpoint until a same-theory continuum object exists.",
            "machinery_not_yet_allowed": "Do not use RG control itself as a mass-gap proof without a same-theory spectral witness.",
            "invalid_use_modes": [
                "Treating finite-volume or small-field RG control as continuum construction.",
                "Counting ultraviolet stability as an infrared mass gap.",
                "Losing gauge invariance or OS positivity in the limit.",
            ],
            "example_alignment": "Yang-Mills: Balaban-style RG is construction machinery for the continuum object, not the final gap witness.",
        }
    if "correlator" in text or "spectral-gap" in text:
        return {
            "selected_machinery": "Euclidean correlator decay and spectral-measure analysis",
            "machinery_role": "witness",
            "supporting_roles": ["transfer", "validation"],
            "current_bottleneck": "cutoff-uniform spectral transfer",
            "why_this_is_the_bottleneck": "A decay estimate is meaningful for the Clay target only if constants and observables survive continuum reconstruction.",
            "controlled_interface": "gauge-invariant Euclidean time correlations -> Hamiltonian spectral support away from zero",
            "assumptions_required": [
                "OS-positive continuum Schwinger functions exist",
                "observables are gauge invariant and spectrally determining",
                "decay constants remain bounded below during cutoff removal",
            ],
            "output_obligation": "Prove support of relevant spectral measures is bounded away from zero.",
            "required_bridge_obligation": "Decay-to-gap lemma with OS reconstruction, observable density, and cutoff-uniform constants.",
            "why_best_available": "The active obstruction is a mass-gap witness; spectral measures are the direct bridge from Euclidean decay to Hamiltonian spectrum.",
            "machinery_needed_because": "The target requires a positive lower spectral threshold, not only existence of the theory.",
            "machinery_not_yet_allowed": "Do not treat fixed-lattice or strong-coupling decay as a continuum gap proof.",
            "invalid_use_modes": [
                "Using observables that do not generate the physical excitation sector.",
                "Allowing decay constants to vanish under cutoff removal.",
                "Separating the decay estimate from the reconstructed continuum theory.",
            ],
            "example_alignment": "Yang-Mills: correlator decay is witness machinery for the gap, conditional on OS reconstruction and same-theory transfer.",
        }
    if "os" in text or "wightman" in text:
        return {
            "selected_machinery": "Osterwalder-Schrader reconstruction",
            "machinery_role": "transfer",
            "supporting_roles": ["representation", "validation"],
            "current_bottleneck": "Euclidean-to-Hilbert-space transfer",
            "why_this_is_the_bottleneck": "Hamiltonian spectral statements require a physical Hilbert space reconstructed from the same Euclidean data.",
            "controlled_interface": "OS-positive Schwinger functions -> Hilbert space, vacuum, observables, and Hamiltonian",
            "assumptions_required": [
                "Schwinger functions satisfy OS axioms",
                "gauge-invariant observable class is identified",
                "nontriviality survives the OS null quotient",
            ],
            "output_obligation": "Construct H_YM, Omega, H, and the gauge-invariant observable algebra from the limiting data.",
            "required_bridge_obligation": "OS reconstruction packet with positivity, domain, vacuum, and spectral semantics.",
            "why_best_available": "The active obstruction is transfer from Euclidean construction to spectral language.",
            "machinery_needed_because": "Without reconstruction, Hamiltonian notation is only an endpoint slogan.",
            "machinery_not_yet_allowed": "Do not assert a Hamiltonian gap before H and the vacuum sector are reconstructed.",
            "invalid_use_modes": [
                "Postulating the Hilbert space instead of reconstructing it.",
                "Applying reconstruction to a different regulated theory.",
                "Ignoring null sectors or too-small observable algebras.",
            ],
            "example_alignment": "Yang-Mills: OS reconstruction is transfer machinery from Euclidean Schwinger data to Hamiltonian spectral claims.",
        }
    if "hamiltonian" in text:
        return {
            "selected_machinery": "Hamiltonian spectral formulation",
            "machinery_role": "validation",
            "supporting_roles": ["witness"],
            "current_bottleneck": "reconstruction premise availability",
            "why_this_is_the_bottleneck": "The Hamiltonian endpoint validates the gap only after H_YM, Omega, H, and P_perp are constructed.",
            "controlled_interface": "reconstructed physical Hilbert space -> final spectral gap statement",
            "assumptions_required": [
                "OS/Wightman reconstruction has produced H_YM and H",
                "vacuum and vacuum-orthogonal sector are identified",
                "observables determine the excitation sector",
            ],
            "output_obligation": "Verify Spec(H restricted to the vacuum-orthogonal sector) is bounded below by Delta > 0.",
            "required_bridge_obligation": "Hamiltonian endpoint checklist mapping every spectral object to reconstruction premises.",
            "why_best_available": "The final claim is spectral, so Hamiltonian language is the right endpoint validator.",
            "machinery_needed_because": "The framework must know what would count as the mass-gap theorem after construction succeeds.",
            "machinery_not_yet_allowed": "Do not use Hamiltonian notation as construction machinery.",
            "invalid_use_modes": [
                "Assuming H_YM, Omega, or H before reconstruction.",
                "Using a finite-lattice transfer matrix as the continuum Hamiltonian.",
                "Treating the spectral inequality as proved because it has been written down.",
            ],
            "example_alignment": "Yang-Mills: Hamiltonian spectral theory is endpoint validation machinery, not the construction spine.",
        }
    return {
        "selected_machinery": "target-led abstraction refinement",
        "machinery_role": "obstruction",
        "supporting_roles": ["validation"],
        "current_bottleneck": "untyped route interface",
        "why_this_is_the_bottleneck": "The route cannot be ranked by method quality until it names the object and interface it controls.",
        "controlled_interface": "untyped route pressure -> typed bridge obligation",
        "assumptions_required": ["active target ledger", "candidate source evidence", "route-family classification"],
        "output_obligation": "Classify the route by construction, representation, invariant, transfer, witness, obstruction, or validation role.",
        "required_bridge_obligation": "Machinery-classification lemma naming the controlled interface and invalid-use modes.",
        "why_best_available": "The route is not yet specific enough for stronger machinery.",
        "machinery_needed_because": "Untyped routes must be made auditable before proof or discovery budget is spent.",
        "machinery_not_yet_allowed": "Do not promote a named method until its proof role and interface are typed.",
        "invalid_use_modes": [
            "Generic method naming.",
            "Solving a nearby proxy problem.",
            "Omitting target-object identity.",
        ],
        "example_alignment": "Yang-Mills: generic QFT or analogy routes remain obstruction/evidence tasks until the exact transfer role is named.",
    }


def machinery_selection_for_candidate(
    candidate: dict[str, Any],
    target_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blueprint = candidate.get("route_blueprint", {}) if isinstance(candidate.get("route_blueprint"), dict) else {}
    family = clean_text(blueprint.get("route_family")) or clean_text(candidate.get("creative_operation")) or "unclassified route"
    alignment = _yang_mills_alignment(family)
    contract = target_contract or {}
    target_object = clean_text(contract.get("exact_target_object")) or "active target object"
    selection = {
        "selection_id": stable_id("machinery-selection", candidate.get("candidate_id", ""), family, alignment["machinery_role"]),
        "target_object_link": target_object,
        "route_family": family,
        **alignment,
        "target_contract_summary": {
            "success_condition": clean_text(contract.get("success_condition")),
            "nonweakening_commitments": contract.get("nonweakening_commitments", []),
            "forbidden_nearby_problems": contract.get("forbidden_nearby_problems", []),
            "acceptable_weakenings": contract.get("acceptable_weakenings", []),
        },
        "validation_handoff": "agentic/scripts/validate_hypothesis_exploration.py",
    }
    return selection


def validate_machinery_shape(selection: Any) -> tuple[bool, str]:
    if not isinstance(selection, dict):
        return False, "machinery_selection must be an object"
    required = [
        "selection_id",
        "selected_machinery",
        "machinery_role",
        "supporting_roles",
        "current_bottleneck",
        "why_this_is_the_bottleneck",
        "controlled_interface",
        "target_object_link",
        "assumptions_required",
        "output_obligation",
        "required_bridge_obligation",
        "why_best_available",
        "machinery_needed_because",
        "machinery_not_yet_allowed",
        "invalid_use_modes",
        "validation_handoff",
        "example_alignment",
    ]
    missing = [field for field in required if field not in selection]
    if missing:
        return False, f"missing fields: {', '.join(missing)}"
    if selection.get("machinery_role") not in ROLES:
        return False, f"invalid machinery_role: {selection.get('machinery_role')}"
    for field in [
        "selected_machinery",
        "current_bottleneck",
        "why_this_is_the_bottleneck",
        "controlled_interface",
        "target_object_link",
        "output_obligation",
        "required_bridge_obligation",
        "why_best_available",
        "machinery_needed_because",
        "machinery_not_yet_allowed",
        "validation_handoff",
        "example_alignment",
    ]:
        if not clean_text(selection.get(field)):
            return False, f"{field} must be non-empty"
    for field in ["supporting_roles", "assumptions_required", "invalid_use_modes"]:
        if not isinstance(selection.get(field), list) or not selection[field]:
            return False, f"{field} must be a non-empty list"
    return True, ""


def summarize_machinery_portfolio(selections: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {role: 0 for role in ROLES}
    bottlenecks: dict[str, int] = {}
    for selection in selections:
        role = selection.get("machinery_role")
        if role in counts:
            counts[role] += 1
        for supporting_role in selection.get("supporting_roles", []):
            if supporting_role in counts:
                counts[supporting_role] += 1
        bottleneck = clean_text(selection.get("current_bottleneck")) or "unknown"
        bottlenecks[bottleneck] = bottlenecks.get(bottleneck, 0) + 1
    missing_core_roles = [role for role in ["construction", "transfer", "witness", "validation"] if counts.get(role, 0) == 0]
    return {
        "selection_count": len(selections),
        "role_counts": counts,
        "bottleneck_counts": dict(sorted(bottlenecks.items())),
        "missing_core_roles": missing_core_roles,
        "portfolio_read": (
            "A coherent long-horizon portfolio needs construction, transfer, witness, and validation roles to connect the "
            "target object to its final claim."
        ),
    }
