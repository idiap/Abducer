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
"""Build property-preserving visual conceptualization packets."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, slugify, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, markdown_list, write_markdown


REPORT_ROOT = ROOT / "agentic/reports/visual_conceptualization/targets"
DEFAULT_WINDOW = 5
PROPERTY_CATEGORIES = [
    "invariant",
    "symmetry",
    "locality_globality",
    "order_monotonicity",
    "positivity_sign",
    "limiting_behavior",
    "physical_carrier",
    "proof_obligation",
]


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    match = re.search(r"(\d+)$", raw)
    return int(match.group(1)) if match else 0


def selected_cycles(cycles: list[dict[str, Any]], *, last: int = DEFAULT_WINDOW) -> list[dict[str, Any]]:
    ordered = sorted(cycles, key=cycle_number)
    return ordered[-max(1, last) :]


def branch_outputs(cycles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for cycle in cycles:
        for output in cycle.get("branch_outputs", []) if isinstance(cycle.get("branch_outputs"), list) else []:
            if isinstance(output, dict):
                row = dict(output)
                row["_cycle_id"] = clean_text(cycle.get("cycle_id"))
                outputs.append(row)
    return outputs


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if isinstance(lemmas, list) and lemmas and isinstance(lemmas[0], dict) else {}


def property_row(category: str, formal: str, visual: str, verdict: str, rationale: str) -> dict[str, str]:
    return {
        "category": category,
        "formal_property": clean_text(formal),
        "visual_counterpart": clean_text(visual),
        "preservation_verdict": verdict,
        "rationale": clean_text(rationale),
    }


def hypothesis(
    kind: str,
    text: str,
    route_consequence: str,
    required_artifact: str,
    falsifier: str,
    reward: str,
) -> dict[str, str]:
    return {
        "kind": kind,
        "hypothesis": clean_text(text),
        "route_consequence": clean_text(route_consequence),
        "required_artifact": clean_text(required_artifact),
        "falsifier": clean_text(falsifier),
        "expected_physics_reward": clean_text(reward),
    }


def audit(verdict: str, consequence: str, revision: str = "") -> dict[str, Any]:
    return {
        "audit_verdict": verdict,
        "physical_relevance_verdict": "carrier_explicit" if verdict not in {"quarantine", "reject"} else "carrier_or_preservation_incomplete",
        "proof_search_value": "usable only through the allowed route consequence",
        "allowed_route_consequence": clean_text(consequence),
        "required_revision": clean_text(revision),
    }


def ym_conceptualizations() -> list[dict[str, Any]]:
    """Return a deterministic YM pilot covering both accepted and quarantined analogies."""
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "concept_id": "ym.visual.wilson-holonomy-thread",
            "formal_focus": {
                "type": "concept",
                "name": "Wilson loop observable",
                "statement": "A gauge-invariant Wilson loop records holonomy around a closed contour and can carry same-theory nontriviality through Euclidean observables.",
                "proof_pressure": "Keep the carrier gauge-invariant while moving from finite reflected blocks toward OS-positive Schwinger data.",
                "physical_carrier": "Wilson loop / gauge-invariant holonomy observable",
            },
            "main_concepts": ["Wilson loop", "holonomy", "gauge invariance", "closed contour", "same-theory observable carrier"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "fiber",
                "title": "Closed threads woven through a gauge fabric",
                "description": "A closed thread can be pulled through local gauge coordinate changes while the traced holonomy carried by the loop remains the inspectable object.",
                "why_selected": "The image preserves loop-closure, gauge-coordinate redundancy, and carrier identity better than a point-particle picture.",
            },
            "property_preservation_table": [
                property_row("invariant", "Trace/closed-loop holonomy is gauge invariant.", "The color of a closed thread is unchanged by local frame relabeling.", "preserved", "Closure blocks endpoint gauge-frame dependence."),
                property_row("symmetry", "Gauge transformations act locally but observables must be invariant.", "The fabric frame can twist without changing the closed thread's recorded color.", "preserved", "The metaphor keeps gauge redundancy distinct from observable content."),
                property_row("locality_globality", "The loop is nonlocal but built from local link transport.", "A thread accumulates local twists into one closed global trace.", "preserved", "The analogy preserves local-to-global accumulation."),
                property_row("order_monotonicity", "No monotone order is inherent without an area-law or correlation inequality.", "Thread length alone does not order physical strength.", "absent", "This prevents the image from inventing monotonicity."),
                property_row("positivity_sign", "Reflection positivity is not automatic for every compressed Wilson construction.", "A visible thread may still fail a mirror-overlap sign test.", "partially_preserved", "The image warns that carrier identity does not settle positivity."),
                property_row("limiting_behavior", "The observable must survive cutoff and continuum limits.", "Threads must remain identifiable as the fabric mesh is refined.", "partially_preserved", "The image exposes the mesh-refinement survival question but does not prove it."),
                property_row("physical_carrier", "Gauge-invariant Wilson observable carries the claim.", "The closed thread is the carrier, not the coordinate grid.", "preserved", "The image keeps the observable central."),
                property_row("proof_obligation", "Show same-theory carrier survival and positivity transfer.", "Prove the thread survives mirror tests and mesh refinement.", "preserved", "The proof obligation is visible as survival under reflection and refinement."),
            ],
            "distortion_ledger": [
                "The thread image can make gauge invariance look topological only; the actual Wilson observable depends on connection and representation data.",
                "The image does not supply OS positivity or a mass gap.",
                "It can hide endpoint/source derivative bookkeeping unless paired with a table artifact.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "missing_artifact",
                    "Build a same-theory Wilson-carrier certificate before any transfer theorem is promoted.",
                    "artifact_sprint",
                    "same-theory carrier certificate linking finite reflected Wilson blocks to OS-positive Schwinger candidates",
                    "Find a regulator change where the closed-loop carrier is replaced by a boundary-sector proxy.",
                    "High: it would clarify whether the route speaks about YM observables rather than an auxiliary model.",
                )
            ],
            "non_claim_boundary": "The metaphor does not establish an area law, OS positivity, continuum existence, or a positive mass gap.",
            "audit": audit("usable_for_hypothesis_generation", "same-theory carrier certificate"),
            "status": "hypothesis_seed",
        }
    )
    rows.append(
        {
            "concept_id": "ym.visual.reflection-positive-mirror-cone",
            "formal_focus": {
                "type": "property",
                "name": "Reflection positivity",
                "statement": "Reflection positivity requires nonnegative pairings between reflected observables and future observables.",
                "proof_pressure": "A compression or source aggregation must preserve the positive cone, not merely preserve notation.",
                "physical_carrier": "OS reflection-positive Schwinger/Wilson observable family",
            },
            "main_concepts": ["OS positivity", "reflection", "positive cone", "observable pairing", "same-theory transfer"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "tension_field",
                "title": "A mirror that only accepts vectors inside a positive cone",
                "description": "The reflected half-space is a mirror test: only observables whose reflected overlap remains in the positive cone can pass.",
                "why_selected": "It makes sign fragility visible and ties positivity to a cone-preservation obligation.",
            },
            "property_preservation_table": [
                property_row("invariant", "The positivity condition is invariant under admissible observable reparameterization.", "Cone membership is unchanged by coordinate labels.", "preserved", "The cone is the object, not a coordinate drawing."),
                property_row("symmetry", "Reflection is an involution.", "The mirror operation flips twice to return the original side.", "preserved", "The involutive structure is directly represented."),
                property_row("locality_globality", "Half-space localization matters for OS reconstruction.", "Only one side and its reflected partner participate in the mirror test.", "preserved", "The visual split matches time-reflection localization."),
                property_row("order_monotonicity", "Cone inclusion supports order-like reasoning.", "Moving deeper into the cone makes positivity more robust.", "partially_preserved", "The image is useful only for cone inclusion, not arbitrary monotonicity."),
                property_row("positivity_sign", "Pairings must be nonnegative.", "The mirror rejects vectors whose reflected overlap points outside the cone.", "preserved", "Sign is the main preserved property."),
                property_row("limiting_behavior", "Cone closure must survive limit operations.", "A vector near the cone boundary can fall out under projection or limiting motion.", "partially_preserved", "The metaphor highlights endpoint fragility."),
                property_row("physical_carrier", "OS-positive observables are the reconstruction carrier.", "The vector being tested is the observable family.", "preserved", "The carrier is explicit."),
                property_row("proof_obligation", "Certify positivity after compression/source aggregation.", "Show the mirror test still accepts the compressed vector.", "preserved", "The exact next proof artifact is visible."),
            ],
            "distortion_ledger": [
                "A Euclidean cone image can hide the infinite-dimensional functional-analytic closure problem.",
                "Cone geometry may suggest convexity properties not available for every transformed object.",
                "It does not justify Schur/Feshbach transfer by itself.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "falsifier",
                    "Treat every proposed compression as a mirror-cone test before branch promotion.",
                    "falsifier_sprint",
                    "finite reflection-positivity interval certificate for the compressed Wilson block",
                    "Exhibit one reflected observable pair whose compressed pairing is negative.",
                    "High: a positive or negative cone test directly decides whether the route can remain same-theory.",
                )
            ],
            "non_claim_boundary": "The mirror-cone metaphor does not prove OS reconstruction or positivity preservation under unvalidated reductions.",
            "audit": audit("usable_for_hypothesis_generation", "reflection-positivity interval certificate"),
            "status": "hypothesis_seed",
        }
    )
    rows.append(
        {
            "concept_id": "ym.visual.schur-feshbach-shadow-bridge",
            "formal_focus": {
                "type": "obstruction",
                "name": "Schur/Feshbach compression",
                "statement": "A Schur/Feshbach reduction can expose an effective block, but positivity and carrier identity may be lost under projection or endpoint terms.",
                "proof_pressure": "Prevent the compression from becoming a proxy theorem about an easier effective object.",
                "physical_carrier": "Compressed Wilson/OS block, carrier incomplete until certified",
            },
            "main_concepts": ["Schur complement", "Feshbach map", "projection", "effective block", "endpoint terms", "positivity loss"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "lens",
                "title": "A shadow bridge cast by a load-bearing bridge",
                "description": "The shadow outlines an effective route, but it cannot carry weight unless one proves which beams and loads survived projection.",
                "why_selected": "The image exposes why a reduction can be explanatory while still being unsafe for transfer.",
            },
            "property_preservation_table": [
                property_row("invariant", "Schur complement preserves selected spectral/algebraic information under hypotheses.", "The shadow preserves some outline of the bridge.", "partially_preserved", "Only selected information is carried."),
                property_row("symmetry", "Symmetry may survive if the projection respects it.", "A symmetric bridge can cast an asymmetric shadow if the light is skewed.", "partially_preserved", "Projection geometry matters."),
                property_row("locality_globality", "Local block elimination can change global coupling.", "Removing supports changes load paths across the whole bridge.", "partially_preserved", "The image reveals hidden global effects."),
                property_row("order_monotonicity", "Schur complements have conditional order properties.", "A darker shadow does not imply a stronger bridge.", "distorted", "The metaphor warns against invented monotonicity."),
                property_row("positivity_sign", "Positivity can fail under endpoint or domain changes.", "A shadow cannot certify that the bridge carries positive load.", "distorted", "This is the central danger."),
                property_row("limiting_behavior", "Endpoint singularities and cutoffs may not commute with compression.", "The shadow changes discontinuously as the light approaches an endpoint.", "partially_preserved", "The image captures endpoint fragility."),
                property_row("physical_carrier", "The effective block may not be a same-theory observable carrier.", "The shadow is not the physical bridge.", "distorted", "This triggers quarantine unless certified."),
                property_row("proof_obligation", "Supply positivity, carrier, and endpoint certificates.", "Inspect beams, loads, and endpoint shadows before crossing.", "preserved", "The required artifact is explicit."),
            ],
            "distortion_ledger": [
                "The metaphor is deliberately dangerous: it can make the effective object seem target-equivalent before proof.",
                "It does not preserve physical carrier identity without an external certificate.",
                "It can hide noncommuting endpoint and cutoff limits.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "quarantine_test",
                    "Quarantine Schur/Feshbach branches until a positivity-and-carrier certificate is computed.",
                    "quarantine",
                    "endpoint source table plus compressed-pairing positivity interval",
                    "A negative compressed reflected pairing or a carrier mismatch under regulator refinement.",
                    "High if passed, but currently unsafe: it would decide whether the compression is a real bridge or only a shadow.",
                )
            ],
            "non_claim_boundary": "This analogy is not usable as proof support; it is a warning device until the missing certificates exist.",
            "audit": audit("quarantine", "endpoint source table plus positivity interval", "Require explicit carrier and positivity certificates before using the metaphor for hypothesis promotion."),
            "status": "quarantine",
        }
    )
    rows.append(
        {
            "concept_id": "ym.visual.uniform-tail-flood-barrier",
            "formal_focus": {
                "type": "obligation",
                "name": "Cutoff-uniform tail bound",
                "statement": "The T_tail contribution must be bounded uniformly across the relevant cutoff/source/volume regime.",
                "proof_pressure": "Local interval success cannot promote if the tail barrier changes height with the cutoff.",
                "physical_carrier": "Wilson/OS observable family across regulator refinement",
            },
            "main_concepts": ["uniform bound", "tail estimate", "cutoff", "source interval", "volume limit", "order of limits"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "flow",
                "title": "A flood barrier that must hold at every reservoir height",
                "description": "A tail estimate is a barrier against uncontrolled contribution; it is useful only if it does not need rebuilding for each cutoff height.",
                "why_selected": "The image preserves uniformity pressure and exposes why one fixed-scale estimate is insufficient.",
            },
            "property_preservation_table": [
                property_row("invariant", "The bound must be stated independent of the moving cutoff parameter.", "The barrier height must not depend on one reservoir snapshot.", "preserved", "Uniformity is central."),
                property_row("symmetry", "Symmetry is secondary unless used in the tail estimate.", "Barrier symmetry is not the decisive feature.", "absent", "No symmetry is invented."),
                property_row("locality_globality", "Local tail terms affect global limit claims.", "A small leak can flood the downstream basin.", "preserved", "The image shows local failure becoming global."),
                property_row("order_monotonicity", "Tail dominance may require monotone envelopes.", "Water level envelopes bound all future heights.", "partially_preserved", "Useful only when a monotone majorant exists."),
                property_row("positivity_sign", "Tail sign can decide a positivity interval.", "Leaks can push the level below the safe mark.", "partially_preserved", "Sign effect is visible but not proved."),
                property_row("limiting_behavior", "The estimate must survive cutoff/volume/source limits.", "The barrier must hold while the reservoir size changes.", "preserved", "Limit-uniformity is exactly represented."),
                property_row("physical_carrier", "The same observable family must remain controlled across refinement.", "The same channel flows through every reservoir height.", "preserved", "Carrier continuity is explicit."),
                property_row("proof_obligation", "Produce a uniform tail ledger or demote the branch.", "Publish the barrier design for all water heights.", "preserved", "The missing artifact is obvious."),
            ],
            "distortion_ledger": [
                "The image can overstate monotonicity if the tail is oscillatory or sign-changing.",
                "It does not show endpoint source equivalence classes unless paired with the source table.",
                "It should not be used to infer continuum control before the order-of-limits ledger exists.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "missing_artifact",
                    "Build a cutoff-uniform T_tail ledger before any finite positivity result is treated as target-facing.",
                    "artifact_sprint",
                    "uniform tail bound ledger with cutoff/source/volume parameters and failure thresholds",
                    "Find a parameter sequence where the required tail barrier height diverges.",
                    "High: it directly attacks the finite-to-global gap that blocked the latest YM cycles.",
                )
            ],
            "non_claim_boundary": "The flood-barrier metaphor does not prove a uniform estimate; it only makes the required estimate non-optional.",
            "audit": audit("usable_for_hypothesis_generation", "uniform tail bound ledger"),
            "status": "hypothesis_seed",
        }
    )
    rows.append(
        {
            "concept_id": "ym.visual.os-reconstruction-bridge",
            "formal_focus": {
                "type": "theorem-route",
                "name": "OS reconstruction bridge",
                "statement": "OS-positive Euclidean Schwinger data can reconstruct a Hilbert-space theory with spectral interpretation under the full axiom package.",
                "proof_pressure": "Do not confuse finite OS-like positivity with full reconstruction data.",
                "physical_carrier": "OS Hilbert object reconstructed from Schwinger/Wilson data",
            },
            "main_concepts": ["OS axioms", "Schwinger functions", "Hilbert reconstruction", "spectral condition", "mass gap"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "bridge",
                "title": "A developing bridge from Euclidean blueprints to spectral load tests",
                "description": "Euclidean data are the blueprint; OS reconstruction is the certified bridge; spectral objects are load tests on the completed structure.",
                "why_selected": "The bridge image separates source data, transfer theorem, and target spectral interpretation.",
            },
            "property_preservation_table": [
                property_row("invariant", "Axiom-preserving reconstruction must preserve correlation content.", "The bridge must match the blueprint's load-bearing coordinates.", "partially_preserved", "Only full axiom compliance preserves content."),
                property_row("symmetry", "Euclidean invariance must transfer to the reconstructed theory.", "Blueprint symmetries must become bridge symmetries.", "preserved", "Symmetry transfer is explicit."),
                property_row("locality_globality", "Local Euclidean data must support global Hilbert reconstruction.", "Local plans assemble into a global bridge.", "partially_preserved", "Assembly obligations remain."),
                property_row("order_monotonicity", "No simple monotonicity carries reconstruction.", "More blueprint pages do not automatically mean a stronger bridge.", "absent", "The analogy avoids false monotonicity."),
                property_row("positivity_sign", "Reflection positivity is load-bearing.", "The bridge collapses if mirror beams fail sign tests.", "preserved", "Positivity is central."),
                property_row("limiting_behavior", "Continuum and infinite-volume limits must produce admissible Schwinger data.", "The bridge must survive replacing temporary supports with permanent ones.", "preserved", "Limit survival is explicit."),
                property_row("physical_carrier", "The reconstructed OS Hilbert object carries spectral claims.", "The completed bridge is where spectral load tests occur.", "preserved", "The carrier is named."),
                property_row("proof_obligation", "Certify full OS axiom package, not only a finite positivity proxy.", "Inspect every load-bearing span before crossing.", "preserved", "The route gate is clear."),
            ],
            "distortion_ledger": [
                "Bridge imagery can make reconstruction look automatic once positivity is present.",
                "It may understate regularity, clustering, and continuum existence obligations.",
                "It does not prove a spectral gap unless a spectral carrier and gap estimate are supplied.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "route_mutation",
                    "Split the YM route into separate blueprint, bridge, and load-test artifacts.",
                    "reframe",
                    "OS reconstruction obligation ledger separating positivity, regularity, clustering, and spectral gap gates",
                    "A finite positivity certificate with no corresponding OS axiom ledger.",
                    "High: it prevents definitional transfer and clarifies what would change field understanding.",
                )
            ],
            "non_claim_boundary": "The metaphor does not establish OS reconstruction from the current finite packets.",
            "audit": audit("usable_for_hypothesis_generation", "OS reconstruction obligation ledger"),
            "status": "hypothesis_seed",
        }
    )
    rows.append(
        {
            "concept_id": "ym.visual.mass-gap-resonance-chamber",
            "formal_focus": {
                "type": "target-property",
                "name": "Mass gap spectral carrier",
                "statement": "A mass gap is a positive lower spectral separation above the vacuum sector in the reconstructed theory.",
                "proof_pressure": "Keep the spectral claim downstream of a same-theory reconstructed Hilbert object.",
                "physical_carrier": "Spectral object in the OS/Wightman/Hamiltonian theory",
            },
            "main_concepts": ["vacuum sector", "spectral gap", "correlation decay", "OS reconstruction", "physical mass"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "resonance",
                "title": "A resonance chamber with no low audible mode above the ground tone",
                "description": "The vacuum is the ground tone; a mass gap means the next allowed resonance is separated by a real silent interval.",
                "why_selected": "The metaphor preserves spectral separation while warning that the chamber must be the reconstructed same-theory object.",
            },
            "property_preservation_table": [
                property_row("invariant", "Spectral separation is invariant under unitary equivalence of the reconstructed theory.", "The silent interval survives relabeling of the chamber coordinates.", "preserved", "The gap is not a coordinate artifact."),
                property_row("symmetry", "Physical symmetries constrain the spectrum.", "Chamber symmetry constrains allowed resonant modes.", "partially_preserved", "The analogy captures constraint but not full representation theory."),
                property_row("locality_globality", "Mass gap is global spectral information tied to large-scale correlation behavior.", "A chamber-wide silence cannot be heard from one local panel alone.", "preserved", "The image distinguishes local checks from global spectrum."),
                property_row("order_monotonicity", "Spectral lower bounds are order statements after reconstruction.", "The first audible mode sits above a threshold.", "preserved", "The ordering of modes is represented."),
                property_row("positivity_sign", "Hilbert-space positivity is prerequisite for spectral interpretation.", "A chamber with negative load-bearing material has no trustworthy resonance test.", "partially_preserved", "Positivity is prerequisite, not the gap itself."),
                property_row("limiting_behavior", "The gap must survive continuum and infinite-volume limits.", "The silent interval must remain as temporary walls are removed.", "preserved", "Limit survival is central."),
                property_row("physical_carrier", "The spectral object carries the mass claim.", "The chamber, not the blueprint, carries resonances.", "preserved", "Carrier identity is explicit."),
                property_row("proof_obligation", "Prove reconstruction plus a positive spectral lower bound.", "Build the chamber and measure the first resonance threshold.", "preserved", "The route cannot skip reconstruction."),
            ],
            "distortion_ledger": [
                "Resonance imagery can suggest a discrete finite spectrum; YM requires the correct infinite-volume spectral statement.",
                "It can hide the difference between exponential decay heuristics and a proven spectral gap.",
                "It does not justify transferring a finite matrix gap to continuum YM.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "falsifier",
                    "Add an order-of-limits falsifier for any route that infers a spectral gap before reconstruction.",
                    "falsifier_sprint",
                    "order-of-limits ledger connecting finite Wilson data, OS reconstruction, and spectral lower bound",
                    "A limit order where the finite gap or decay witness disappears before the spectral object is constructed.",
                    "High: it protects the Clay target from finite-matrix overclaim while preserving meaningful route tests.",
                )
            ],
            "non_claim_boundary": "The resonance image is not evidence for a positive mass gap; it only locates the target property and its carrier.",
            "audit": audit("usable_for_hypothesis_generation", "order-of-limits spectral falsifier"),
            "status": "hypothesis_seed",
        }
    )
    return rows


def generic_conceptualizations(target_id: str, outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest = outputs[-1] if outputs else {}
    lemma = first_lemma(latest)
    statement = clean_text(lemma.get("statement") or latest.get("mathematical_learning") or "Target-preserving bridge route")
    return [
        {
            "concept_id": stable_id("visual.generic", target_id, statement),
            "formal_focus": {
                "type": "proof-route",
                "name": clean_text(latest.get("branch_title") or "Target-preserving bridge"),
                "statement": statement,
                "proof_pressure": clean_text(latest.get("attempted_derivation", {}).get("blocking_gap") or "Separate explanation from proof obligation."),
                "physical_carrier": "not_applicable_or_not_named",
            },
            "main_concepts": ["source object", "target object", "bridge", "invariant", "falsifier"],
            "key_properties": PROPERTY_CATEGORIES,
            "visual_metaphor": {
                "family": "bridge",
                "title": "A load-bearing bridge with inspected beams",
                "description": "A route is usable only when each support beam corresponds to a preserved formal property.",
                "why_selected": "The image keeps transfer obligations visible.",
            },
            "property_preservation_table": [
                property_row(category, f"{category} must be explicitly mapped.", f"The corresponding beam must be inspected for {category}.", "partially_preserved", "Generic fallback requires a target-specific audit before use.")
                for category in PROPERTY_CATEGORIES
            ],
            "distortion_ledger": [
                "Generic bridge imagery can hide source-target mismatch.",
                "The metaphor is explanation-only until target-specific carriers and falsifiers are named.",
            ],
            "hypothesis_inspiration": [
                hypothesis(
                    "representation_requirement",
                    "Name the preserved property ledger before another proof-search cycle.",
                    "reframe",
                    "property-preservation ledger",
                    "A claimed transfer with no independently meaningful source and target properties.",
                    "Unknown until target-specific relevance is audited.",
                )
            ],
            "non_claim_boundary": "This generic metaphor is not proof evidence.",
            "audit": audit("usable_for_explanation", "property-preservation ledger", "Replace generic bridge with target-specific metaphor before hypothesis promotion."),
            "status": "explanation_only",
        }
    ]


def build_visual_conceptualization_report(
    run_state: dict[str, Any],
    cycles: list[dict[str, Any]],
    *,
    concept: str = "",
    last: int = DEFAULT_WINDOW,
    source_report: str = "",
) -> dict[str, Any]:
    target_id = clean_text(run_state.get("target_id"))
    scoped = selected_cycles(cycles, last=last)
    outputs = branch_outputs(scoped)
    conceptualizations = (
        ym_conceptualizations()
        if target_id == "yang-mills-existence-and-mass-gap-target"
        else generic_conceptualizations(target_id, outputs)
    )
    if concept:
        needle = clean_text(concept).lower()
        filtered = [
            row
            for row in conceptualizations
            if needle in clean_text(row.get("concept_id")).lower()
            or needle in clean_text(row.get("formal_focus", {}).get("name")).lower()
        ]
        conceptualizations = filtered or conceptualizations
    cycle_ids = [clean_text(cycle.get("cycle_id")) for cycle in scoped]
    route_outputs = [
        item
        for row in conceptualizations
        for item in row.get("hypothesis_inspiration", [])
        if clean_text(item.get("route_consequence"))
    ]
    return {
        "schema": "abducer.visual_conceptualization_packet.v1",
        "generated_utc": utc_now(),
        "generated_by_skills": [
            "visual-theorem-conceptualizer",
            "visual-analogy-preservation-auditor",
            "physical-relevance-impact-auditor",
            "proof-depth-release-gate",
        ],
        "target_id": target_id,
        "run_id": clean_text(run_state.get("run_id")),
        "source_context": {
            "cycle_ids": cycle_ids,
            "cycle_indices": [cycle_number(cycle) for cycle in scoped],
            "source_report": clean_text(source_report),
            "trigger": "deep_reflection_visual_conceptualization",
            "window_policy": f"last={last}",
        },
        "summary": {
            "concept_count": len(conceptualizations),
            "hypothesis_output_count": len(route_outputs),
            "quarantined_or_rejected_count": sum(
                1
                for row in conceptualizations
                if clean_text(row.get("audit", {}).get("audit_verdict")) in {"quarantine", "reject"}
                or clean_text(row.get("status")) in {"quarantine", "reject"}
            ),
            "route_consequences": sorted({clean_text(item.get("route_consequence")) for item in route_outputs if clean_text(item.get("route_consequence"))}),
            "core_diagnosis": "Visual metaphors are used as property-preservation probes and hypothesis generators, not as proof evidence.",
        },
        "visual_conceptualizations": conceptualizations,
        "workflow_caps": {
            "max_reflection_passes_per_failed_major_cycle_set": 1,
            "promotion_requires": "At least one audited route mutation, missing artifact, falsifier, counterfactual variant, or representation requirement.",
            "no_investment_verdict": "If no property-preserving route consequence is emitted, keep the analogy explanation-only and do not open a new branch.",
        },
        "evidence_paths": [
            rel(ROOT / "agentic/runs/discovery_marathons" / slugify(clean_text(run_state.get("run_id"))) / "run_state.json"),
            *[
                rel(ROOT / "agentic/runs/discovery_marathons" / slugify(clean_text(run_state.get("run_id"))) / "cycles" / f"{slugify(cycle_id)}.json")
                for cycle_id in cycle_ids
            ],
        ],
        "validation_handoff": "agentic/scripts/validate_visual_conceptualization_packet.py",
    }


def target_visual_dir(target_id: str) -> Path:
    return REPORT_ROOT / slugify(target_id)


def render_visual_markdown(report: dict[str, Any]) -> str:
    source = report.get("source_context", {})
    summary = report.get("summary", {})
    lines = [
        "# Visual Conceptualization Packet",
        "",
        f"Target: `{report.get('target_id', '')}`",
        f"Run: `{report.get('run_id', '')}`",
        f"Cycles: `{source.get('cycle_ids', [])}`",
        f"Conceptualizations: `{summary.get('concept_count', 0)}`",
        f"Quarantined or rejected: `{summary.get('quarantined_or_rejected_count', 0)}`",
        "",
        "## Core Diagnosis",
        "",
        clean_text(summary.get("core_diagnosis")),
        "",
        "## Route Consequences",
        "",
        markdown_list(summary.get("route_consequences", [])),
    ]
    for row in report.get("visual_conceptualizations", []):
        focus = row.get("formal_focus", {})
        metaphor = row.get("visual_metaphor", {})
        audit_row = row.get("audit", {})
        lines.extend(
            [
                f"## {clean_text(focus.get('name'))}",
                "",
                f"Concept id: `{row.get('concept_id')}`",
                f"Status: `{row.get('status')}`",
                f"Physical carrier: `{clean_text(focus.get('physical_carrier'))}`",
                "",
                clean_text(focus.get("statement")),
                "",
                f"Metaphor family: `{clean_text(metaphor.get('family'))}`",
                f"Metaphor: **{clean_text(metaphor.get('title'))}**",
                "",
                clean_text(metaphor.get("description")),
                "",
                "### Preserved And Distorted Properties",
                "",
            ]
        )
        for prop in row.get("property_preservation_table", []):
            lines.append(
                f"- `{prop.get('category')}` `{prop.get('preservation_verdict')}`: "
                f"{clean_text(prop.get('formal_property'))} -> {clean_text(prop.get('visual_counterpart'))}. "
                f"{clean_text(prop.get('rationale'))}"
            )
        lines.extend(
            [
                "",
                "### Distortion Ledger",
                "",
                markdown_list(row.get("distortion_ledger", [])),
                "### Hypothesis Inspiration",
                "",
            ]
        )
        for item in row.get("hypothesis_inspiration", []):
            lines.extend(
                [
                    f"- `{clean_text(item.get('kind'))}` {clean_text(item.get('hypothesis'))}",
                    f"  Route consequence: `{clean_text(item.get('route_consequence'))}`",
                    f"  Required artifact: {clean_text(item.get('required_artifact'))}",
                    f"  Falsifier: {clean_text(item.get('falsifier'))}",
                ]
            )
        lines.extend(
            [
                "",
                f"Audit verdict: `{clean_text(audit_row.get('audit_verdict'))}`",
                f"Allowed route consequence: `{clean_text(audit_row.get('allowed_route_consequence'))}`",
                "",
                f"Non-claim boundary: {clean_text(row.get('non_claim_boundary'))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Evidence",
            "",
            markdown_list(report.get("evidence_paths", [])),
            f"Validation handoff: `{report.get('validation_handoff')}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_visual_conceptualization_report(report: dict[str, Any]) -> dict[str, Path]:
    target_id = clean_text(report.get("target_id"))
    out_dir = target_visual_dir(target_id)
    latest_json = out_dir / "latest.json"
    latest_md = out_dir / "latest.md"
    write_json(latest_json, report)
    write_markdown(latest_md, render_visual_markdown(report))
    return {"latest_json": latest_json, "latest_md": latest_md}


def summary_for_discovery_report(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary", {})
    first = report.get("visual_conceptualizations", [{}])[0] if report.get("visual_conceptualizations") else {}
    metaphor = first.get("visual_metaphor", {}) if isinstance(first, dict) else {}
    return {
        "target_id": report.get("target_id", ""),
        "concept_count": summary.get("concept_count", 0),
        "hypothesis_output_count": summary.get("hypothesis_output_count", 0),
        "quarantined_or_rejected_count": summary.get("quarantined_or_rejected_count", 0),
        "route_consequences": summary.get("route_consequences", []),
        "headline_metaphor": clean_text(metaphor.get("title")),
        "headline_family": clean_text(metaphor.get("family")),
        "latest_json": rel(target_visual_dir(report.get("target_id", "")) / "latest.json"),
        "latest_md": rel(target_visual_dir(report.get("target_id", "")) / "latest.md"),
        "validator": report.get("validation_handoff", "agentic/scripts/validate_visual_conceptualization_packet.py"),
    }


def build_for_active_run(target_id: str = "", run_id: str = "", *, concept: str = "", last: int = DEFAULT_WINDOW) -> dict[str, Any]:
    _, run_state = load_run_state(run_id or None, target_id or None)
    cycles = load_cycles(run_state) if run_state else []
    return build_visual_conceptualization_report(run_state, cycles, concept=concept, last=last)
