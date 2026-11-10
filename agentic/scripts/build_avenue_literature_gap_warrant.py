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
"""Build target-scoped literature-gap warrants before broad avenue investment."""

from __future__ import annotations

import argparse
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json
from avenue_literature_gap import (
    PVSNP_TARGET_ID,
    YM_TARGET_ID,
    target_warrant_dir,
    target_warrant_latest_json,
    target_warrant_latest_md,
)
from discovery_marathon_common import target_latest_json, write_markdown


TARGET_LITERATURE = ROOT / "agentic/reports/target_literature_evolution/latest.json"
MACRO_STRATEGY = ROOT / "agentic/reports/macro_strategy/latest.json"
PHYSICS_MATH = ROOT / "agentic/reports/physics_math_interpretation/latest.json"
STRATEGY_JUDGE = ROOT / "agentic/reports/strategy_progression_judge/latest.json"
SCIENTIFIC_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
VISUAL_CONCEPT = ROOT / "agentic/reports/visual_conceptualization/latest.json"
FAILURE_ARCH = ROOT / "agentic/reports/failure_archaeology/latest.json"
YM_PROOF_OBJECTS = (
    ROOT
    / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json"
)


def compact_refs(target_id: str) -> list[dict[str, Any]]:
    report = load_optional_json(TARGET_LITERATURE)
    if clean_text(report.get("target_id")) == target_id:
        refs = report.get("references", []) if isinstance(report.get("references"), list) else []
        return [
            {
                "ref_id": clean_text(ref.get("ref_id")),
                "authors": clean_text(ref.get("authors")),
                "year": ref.get("year"),
                "title": clean_text(ref.get("title")),
                "url": clean_text(ref.get("url")),
                "role": clean_text(ref.get("role")),
                "status": clean_text(ref.get("status")),
                "supports": clean_text(ref.get("supports")),
                "limitation": clean_text(ref.get("limitation")),
            }
            for ref in refs
            if isinstance(ref, dict) and clean_text(ref.get("ref_id"))
        ]
    if target_id == YM_TARGET_ID:
        return [
            {
                "ref_id": "ref.os-1973-1975",
                "authors": "K. Osterwalder and R. Schrader",
                "year": 1973,
                "title": "Axioms for Euclidean Green's Functions I-II",
                "url": "https://ncatlab.org/nlab/show/Osterwalder-Schrader%2Btheorem",
                "role": "axiomatic_bridge",
                "status": "canonical",
                "supports": "Provides reflection-positivity and Euclidean reconstruction criteria for OS/Wightman QFT.",
                "limitation": "It is a reconstruction criterion, not a construction of four-dimensional Yang-Mills or a Wilson endpoint-source theorem.",
            },
            {
                "ref_id": "ref.wilson-1974",
                "authors": "K. G. Wilson",
                "year": 1974,
                "title": "Confinement of Quarks",
                "url": "https://link.aps.org/doi/10.1103/PhysRevD.10.2445",
                "role": "physics_motivation",
                "status": "primary",
                "supports": "Introduces lattice gauge Wilson-loop carrier language and confinement intuition.",
                "limitation": "Strong-coupling lattice confinement does not prove same-theory continuum YM existence or OS spectral mass gap.",
            },
            {
                "ref_id": "ref.seiler-1982",
                "authors": "E. Seiler",
                "year": 1982,
                "title": "Gauge Theories as a Problem of Constructive Quantum Field Theory and Statistical Mechanics",
                "url": "https://doi.org/10.1007/BFb0090332",
                "role": "constructive_program",
                "status": "expert_survey",
                "supports": "Frames gauge theories as constructive field-theory and statistical-mechanics problems with lattice-to-continuum pressure.",
                "limitation": "It clarifies the program and obstacles rather than closing the four-dimensional continuum mass-gap problem.",
            },
            {
                "ref_id": "ref.balaban-1985",
                "authors": "T. Balaban",
                "year": 1985,
                "title": "Ultraviolet Stability of Three-Dimensional Lattice Pure Gauge Field Theories",
                "url": "https://inspirehep.net/literature/16302",
                "role": "constructive_program",
                "status": "primary",
                "supports": "Represents rigorous RG control language around cutoff, stability, and lattice gauge theory.",
                "limitation": "It does not provide the four-dimensional same-theory representation or endpoint artifact used by this local route.",
            },
            {
                "ref_id": "ref.jaffe-witten-clay",
                "authors": "A. Jaffe and E. Witten",
                "year": 2000,
                "title": "Quantum Yang-Mills Theory",
                "url": "https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf",
                "role": "problem_statement",
                "status": "canonical",
                "supports": "Defines the Clay target: construct nontrivial quantum Yang-Mills on four-dimensional space and prove a positive mass gap.",
                "limitation": "It defines the target and rigor standard but does not provide a solution or local Route A finite artifact.",
            },
            {
                "ref_id": "ref.douglas-2004",
                "authors": "M. R. Douglas",
                "year": 2004,
                "title": "Report on the Status of the Yang-Mills Millennium Prize Problem",
                "url": "https://www.claymath.org/library/annual_report/douglas_quantum_yang_mills.pdf",
                "role": "route_obstruction",
                "status": "expert_survey",
                "supports": "Explains the difficulty of converting physical YM understanding into a rigorous Millennium-problem proof.",
                "limitation": "It is a status report rather than the specific finite endpoint, representation, or spectral-transfer theorem sought here.",
            },
        ]
    if target_id == PVSNP_TARGET_ID:
        return [
            {
                "ref_id": "ref.cook-1971",
                "authors": "S. A. Cook",
                "year": 1971,
                "title": "The complexity of theorem-proving procedures",
                "url": "https://doi.org/10.1145/800157.805047",
                "role": "problem_foundation",
                "status": "canonical",
                "supports": "Introduces NP-completeness through SAT and makes reductions the central target-preserving language.",
                "limitation": "It does not provide lower-bound machinery for separating P from NP.",
            },
            {
                "ref_id": "ref.razborov-rudich-1997",
                "authors": "A. Razborov and S. Rudich",
                "year": 1997,
                "title": "Natural proofs",
                "url": "https://doi.org/10.1006/jcss.1997.1494",
                "role": "route_obstruction",
                "status": "canonical",
                "supports": "Shows why many circuit lower-bound properties collide with pseudorandomness assumptions.",
                "limitation": "It is a barrier criterion, not a complete prohibition on all nonnatural or proof-complexity routes.",
            },
            {
                "ref_id": "ref.aaronson-wigderson-2008",
                "authors": "S. Aaronson and A. Wigderson",
                "year": 2008,
                "title": "Algebrization: A new barrier in complexity theory",
                "url": "https://doi.org/10.1145/1374376.1374393",
                "role": "route_obstruction",
                "status": "canonical",
                "supports": "Extends relativization-style concerns and forces routes to state how they escape algebraic oracle worlds.",
                "limitation": "It does not rule out every proof-complexity, meta-complexity, or highly nonblackbox route.",
            },
            {
                "ref_id": "ref.murray-williams-2018",
                "authors": "C. Murray and R. Williams",
                "year": 2018,
                "title": "Circuit lower bounds for nondeterministic quasi-polytime",
                "url": "https://eccc.weizmann.ac.il/report/2017/188/",
                "role": "lower_bound_frontier",
                "status": "primary",
                "supports": "Illustrates the modern algorithms-to-lower-bounds frontier and the need for exact model and quantifier accounting.",
                "limitation": "It is not a direct P vs NP separation and still leaves target-preserving amplification gaps.",
            },
        ]
    return [
        {
            "ref_id": "ref.unknown-target-profile",
            "authors": "local target profile",
            "year": "current",
            "title": "Local target profile",
            "url": rel(target_latest_json(target_id)),
            "role": "local_profile",
            "status": "local",
            "supports": "Provides local problem language for warrant construction.",
            "limitation": "A real literature packet should replace this fallback before investment.",
        }
    ]


def source_provenance(target_id: str, avenue_id: str) -> list[dict[str, str]]:
    candidates = [
        TARGET_LITERATURE,
        target_latest_json(target_id),
        MACRO_STRATEGY,
        PHYSICS_MATH,
        STRATEGY_JUDGE,
        SCIENTIFIC_MONITOR,
        VISUAL_CONCEPT,
        FAILURE_ARCH,
    ]
    if target_id == YM_TARGET_ID:
        candidates.append(YM_PROOF_OBJECTS)
    output = []
    for path in candidates:
        if not path.exists():
            continue
        output.append(
            {
                "source": rel(path),
                "scope": f"local source scan for {avenue_id}",
                "finding": "Used as bounded provenance for the warrant; not a claim that external literature search is complete.",
            }
        )
    if len(output) < 2:
        output.append(
            {
                "source": "local static target-profile fallback",
                "scope": f"minimal local provenance for {avenue_id}",
                "finding": "Insufficient for broad investment; the validator should force literature-gap reframe if other fields are weak.",
            }
        )
    return output


def closest(refs: list[dict[str, Any]], ref_ids: list[str], avenue: str) -> list[dict[str, Any]]:
    by_id = {clean_text(ref.get("ref_id")): ref for ref in refs}
    selected = [by_id[ref_id] for ref_id in ref_ids if ref_id in by_id]
    if len(selected) < 3:
        selected.extend([ref for ref in refs if ref not in selected][: 3 - len(selected)])
    return [
        {
            "ref_id": clean_text(ref.get("ref_id")),
            "authors": clean_text(ref.get("authors")),
            "year": ref.get("year"),
            "title": clean_text(ref.get("title")),
            "url": clean_text(ref.get("url")),
            "relevance": clean_text(ref.get("supports")) or f"Closest known literature context for {avenue}.",
            "limitation_for_this_avenue": clean_text(ref.get("limitation"))
            or "Does not by itself supply the avenue's claimed bridge, artifact, or route decision.",
        }
        for ref in selected[:5]
    ]


def base_warrant(target_id: str, avenue_id: str, title: str, refs: list[dict[str, Any]], ref_ids: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "avenue_id": avenue_id,
        "avenue_title": title,
        "closest_known_results": closest(refs, ref_ids, title),
        "source_search_provenance": source_provenance(target_id, avenue_id),
        "validation_handoff": {
            "validator": "agentic/scripts/validate_avenue_literature_gap_warrant.py",
            "next_skill": "literature-gap-relevance-auditor",
            "required_before": "new broad branch_exploration or broad_branch_exploration investment",
        },
    }


def ym_routea_warrant(refs: list[dict[str, Any]]) -> dict[str, Any]:
    packet = base_warrant(
        YM_TARGET_ID,
        "ym.routea.endpoint_source_table",
        "Route A finite Wilson/OS endpoint-source table",
        refs,
        ["ref.os-1973-1975", "ref.wilson-1974", "ref.jaffe-witten-clay", "ref.douglas-2004"],
    )
    packet.update(
        {
            "smallest_honest_claim": (
                "A finite reflected-Wilson Schur-Feshbach endpoint theorem or worked H,K collar table can isolate a "
                "same-theory OS-positivity obstruction before any continuum mass-gap claim is made."
            ),
            "mathematical_or_physical_object": (
                "Gauge-invariant reflected Wilson observable blocks, their finite OS quotient matrix, and the H,K endpoint "
                "or hairpin source terms whose signs decide the local obstruction."
            ),
            "target_commitments_touched": [
                "OS/Wightman reconstruction",
                "same-theory continuum construction",
                "gauge-invariant observable density",
            ],
            "gap_statement": (
                "The actionable gap is not generic reflection positivity. It is the missing finite endpoint-source table that "
                "would tell whether the current Wilson collar obstruction is a real same-theory artifact or only a symbolic "
                "Schur-Feshbach skeleton."
            ),
            "why_not_already_known": (
                "The cited OS and lattice literature provides reconstruction criteria and regulated gauge carriers, but the "
                "local report has not yet exhibited the explicit reflected-Wilson H,K endpoint data, sign budget, and same-theory "
                "transfer boundary needed for this route."
            ),
            "relevance_threshold": {
                "score": 4,
                "threshold": 4,
                "criterion": "Invest only if the next cycle produces the finite theorem, endpoint table, or falsifying sign calculation.",
                "evidence": "The route touches OS positivity and Wilson observables, but only the concrete endpoint artifact can prevent another abstract loop.",
            },
            "physics_or_field_impact": {
                "score": 4,
                "claim": "A certified endpoint obstruction would explain where Wilson-observable reflection positivity fails or survives in the same theory.",
                "evidence": "The object is a gauge-invariant Wilson carrier connected to OS reconstruction and continuum transfer pressure.",
                "missing": "Uniform continuum transfer and spectral-gap reconstruction remain outside this finite artifact.",
            },
            "unification_power": {
                "score": 4,
                "mechanism": "One finite quotient-positivity calculation compresses Wilson carrier choice, OS reflection positivity, and boundary-collar endpoint control.",
                "compresses": [
                    "finite Wilson observable algebra",
                    "reflection-positive OS quotient constraint",
                    "H,K endpoint sign and remainder accounting",
                ],
                "new_requirement_exposed": "The artifact must state the same-theory transfer boundary that separates a finite theorem from a continuum physics claim.",
            },
            "route_decision_power": {
                "score": 5,
                "decides": "Whether Route A has a concrete finite theorem/counterexample package or should stop broad exploration.",
                "next_decisive_test": "Produce the endpoint source table with definitions, equations, signs, failure cases, and validator-visible transfer limits.",
            },
            "novelty_boundary": (
                "Novelty can only be claimed for the explicit reflected-Wilson endpoint artifact and its obstruction consequence; "
                "OS reconstruction, lattice Wilson carriers, and Schur complements are reused machinery."
            ),
            "disqualifier_matrix": [
                {
                    "disqualifier": "prior_art_absorbs_artifact",
                    "test": "A cited constructive-QFT or lattice gauge source already contains the same finite endpoint table and obstruction.",
                    "decision_if_triggered": "do_not_invest_prior_art_collision",
                    "status": "not_triggered_by_local_sources",
                },
                {
                    "disqualifier": "proxy_observable",
                    "test": "The calculation uses a toy matrix, non-gauge-invariant object, or symbolic collar with no Wilson carrier.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "open",
                },
                {
                    "disqualifier": "artifact_debt",
                    "test": "The next cycle repeats the route narrative without the endpoint table, theorem, or sign/falsifier artifact.",
                    "decision_if_triggered": "artifact_sprint_only",
                    "status": "active",
                },
            ],
            "explicit_unknowns": [
                "Whether the H,K endpoint entries have a sign pattern strong enough for a finite obstruction.",
                "Whether the endpoint artifact survives same-theory Wilson/OPE transfer rather than changing theory.",
                "Whether the finite theorem is publishable as a narrow mathematical-physics contribution after prior-art positioning.",
            ],
            "allowed_next_modes": ["artifact_sprint", "falsifier_sprint", "proof_delivery"],
            "investment_decision": "artifact_sprint_only",
        }
    )
    return packet


def ym_representational_warrant(refs: list[dict[str, Any]]) -> dict[str, Any]:
    packet = base_warrant(
        YM_TARGET_ID,
        "ym.representational_dynamics",
        "Representational dynamics frontier for Yang-Mills",
        refs,
        ["ref.seiler-1982", "ref.balaban-1985", "ref.jaffe-witten-clay", "ref.douglas-2004"],
    )
    packet.update(
        {
            "smallest_honest_claim": (
                "A representational-dynamics route is worth broad investment only if it identifies a new efficient representation "
                "that preserves gauge-invariant observables, same-theory limits, OS positivity, and nontriviality witnesses better "
                "than the current Wilson/RG language."
            ),
            "mathematical_or_physical_object": (
                "Representation morphisms over gauge-invariant observable families, regulator/RG maps, Schwinger-function coherence, "
                "and OS spectral-transfer data."
            ),
            "target_commitments_touched": [
                "same-theory continuum construction",
                "OS/Wightman reconstruction",
                "nontriviality of the field",
                "positive spectral mass gap",
            ],
            "gap_statement": (
                "The literature-aware gap is an efficient representation that simultaneously preserves gauge covariance, reflection "
                "positivity, continuum limiting data, and a nontrivial spectral carrier. The current workflow names this ambition but "
                "has not yet isolated the representation that makes the coupled requirements easier."
            ),
            "why_not_already_known": (
                "Constructive and RG sources frame lattice-to-continuum control, while the Clay target demands same-theory mass gap. "
                "The local imported overlay is a research program, not a demonstrated representation theorem that closes those coupled gates."
            ),
            "relevance_threshold": {
                "score": 4,
                "threshold": 4,
                "criterion": "Invest only after the representation names preserved objects, primitive operations, invariants, and a falsifier.",
                "evidence": "The route could change the proof language around several Clay gates, but the efficient-representation requirement is still underdetermined.",
            },
            "physics_or_field_impact": {
                "score": 5,
                "claim": "A successful representation could change how YM existence, nontriviality, and mass-gap transfer are jointly understood.",
                "evidence": "It aims at gauge-invariant observables, RG/regulator coherence, OS reconstruction, and spectral data at once.",
                "missing": "No concrete representation theorem yet distinguishes it from a declarative overlay.",
            },
            "unification_power": {
                "score": 5,
                "mechanism": "A single representation calculus would compress regulator choice, RG basin entry, observable recovery, OS positivity, and spectral transfer.",
                "compresses": [
                    "gauge-invariant observable recovery",
                    "regulator and RG coherence",
                    "reflection positivity and spectral transfer",
                    "nontriviality witness selection",
                ],
                "new_requirement_exposed": "State the efficient-representation contract and a decisive counterexample if the representation cannot preserve a target commitment.",
            },
            "route_decision_power": {
                "score": 3,
                "decides": "Whether the workflow should open broad representational exploration or first produce a sharper representation contract.",
                "next_decisive_test": "Write a representation contract with objects, invariants, cheap operations, equivalence policy, transfer interface, and falsifiers.",
            },
            "novelty_boundary": (
                "Novelty would lie in a concrete representation theorem or counterexample, not in renaming standard constructive-QFT "
                "or RG obligations as representational dynamics."
            ),
            "disqualifier_matrix": [
                {
                    "disqualifier": "programmatic_renaming",
                    "test": "The route restates RG, OS, or Wilson requirements without a new representation object or theorem.",
                    "decision_if_triggered": "reframe_gap_before_investment",
                    "status": "active",
                },
                {
                    "disqualifier": "target_commitment_loss",
                    "test": "The representation loses gauge covariance, reflection positivity, nontriviality, or same-theory continuum data.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "open",
                },
                {
                    "disqualifier": "prior_art_absorbs_claim",
                    "test": "A cited constructive/RG theorem already supplies the same representation theorem under the same assumptions.",
                    "decision_if_triggered": "do_not_invest_prior_art_collision",
                    "status": "not_triggered_by_local_sources",
                },
            ],
            "explicit_unknowns": [
                "Which representation object is strictly better than existing Wilson, Schwinger, RG, or OS formulations.",
                "Which target commitment the representation makes cheaper without moving proof debt elsewhere.",
                "Which falsifier would kill the route after one contract-writing pass.",
            ],
            "allowed_next_modes": ["literature_gap_reframe", "artifact_sprint", "falsifier_sprint"],
            "investment_decision": "reframe_gap_before_investment",
        }
    )
    return packet


def ym_visual_warrant(refs: list[dict[str, Any]]) -> dict[str, Any]:
    packet = base_warrant(
        YM_TARGET_ID,
        "ym.visual_conceptualization",
        "Visual conceptualization as a hypothesis seed for Yang-Mills",
        refs,
        ["ref.os-1973-1975", "ref.wilson-1974", "ref.jaffe-witten-clay"],
    )
    packet.update(
        {
            "smallest_honest_claim": (
                "Property-preserving visual analogies can explain YM proof tensions and seed hypotheses, but they are not an avenue "
                "for broad proof investment unless they produce a concrete route mutation, artifact, falsifier, or representation requirement."
            ),
            "mathematical_or_physical_object": (
                "Visual metaphors for Wilson loops, reflection-positive mirrors, regulator flow, continuum limits, and spectral gaps, each with a property-preservation ledger."
            ),
            "target_commitments_touched": [
                "gauge-invariant observable density",
                "OS/Wightman reconstruction",
                "positive spectral mass gap",
            ],
            "gap_statement": (
                "The gap is not in existing physics literature but in the workflow's ability to use analogies without proxy shift. "
                "A useful analogy must preserve formal properties and create a testable theorem consequence."
            ),
            "why_not_already_known": (
                "Visual explanations of gauge theory are common, but a property-preserving analogy ledger that gates proof-route mutation is a workflow artifact, not an established mathematical result."
            ),
            "relevance_threshold": {
                "score": 2,
                "threshold": 4,
                "criterion": "Allow only explanation or hypothesis-seeding unless the analogy yields a concrete artifact or falsifier.",
                "evidence": "The current visual cycle can improve conceptual understanding but has weak independent publication value.",
            },
            "physics_or_field_impact": {
                "score": 2,
                "claim": "Impact is pedagogical or heuristic until a preservation audit produces a testable YM proof obligation.",
                "evidence": "It can highlight noncommuting limits or proxy shifts, but it does not by itself change a physical carrier.",
                "missing": "A new theorem, artifact, or falsifier tied to a Wilson/OS/spectral carrier.",
            },
            "unification_power": {
                "score": 2,
                "mechanism": "The metaphor may put several tensions in one picture, but visual compression is not mathematical unification.",
                "compresses": [
                    "intuition about locality versus global reflection",
                    "intuition about regulator flow versus continuum limit",
                ],
                "new_requirement_exposed": "Every analogy must declare preserved properties, distortions, and the exact route consequence before influencing proof search.",
            },
            "route_decision_power": {
                "score": 2,
                "decides": "Whether a visual artifact remains explanation-only or becomes a hypothesis seed after preservation audit.",
                "next_decisive_test": "Run the preservation auditor and require one concrete artifact, falsifier, route mutation, or representation requirement.",
            },
            "novelty_boundary": (
                "Novelty is limited to a workflow heuristic for disciplined analogy use; it is not a YM theorem or physical result until a preserved property yields a proof obligation."
            ),
            "disqualifier_matrix": [
                {
                    "disqualifier": "proxy_shift",
                    "test": "The image suggests a theorem by hiding gauge invariance, reflection positivity, or continuum transfer.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "active",
                },
                {
                    "disqualifier": "no_route_consequence",
                    "test": "The analogy has no artifact, falsifier, counterfactual, route mutation, or representation requirement.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "active",
                },
                {
                    "disqualifier": "literature_collision",
                    "test": "The analogy merely paraphrases a standard visualization already present in field pedagogy.",
                    "decision_if_triggered": "do_not_invest_prior_art_collision",
                    "status": "open",
                },
            ],
            "explicit_unknowns": [
                "Which visual metaphors preserve enough formal structure to seed a real hypothesis.",
                "Whether any analogy can expose a new efficient representation requirement.",
                "Whether the analogy misleads by flattening noncommuting limits or same-theory constraints.",
            ],
            "allowed_next_modes": ["quarantine", "falsifier_sprint", "artifact_sprint"],
            "investment_decision": "quarantine_low_relevance",
        }
    )
    return packet


def pvsnp_bridge_warrant(refs: list[dict[str, Any]]) -> dict[str, Any]:
    packet = base_warrant(
        PVSNP_TARGET_ID,
        "pvsnp.bridge_route_gap",
        "Target-preserving P vs NP bridge route",
        refs,
        ["ref.cook-1971", "ref.razborov-rudich-1997", "ref.aaronson-wigderson-2008", "ref.murray-williams-2018"],
    )
    packet.update(
        {
            "smallest_honest_claim": (
                "A P vs NP avenue is investable only if it names a target-preserving source object, target class, reduction or proof-system "
                "interface, quantifier regime, and barrier status before any global separation rhetoric."
            ),
            "mathematical_or_physical_object": (
                "Boolean complexity bridge object connecting restricted lower-bound, proof-complexity, meta-complexity, or formula-footprint evidence to the main P vs NP target."
            ),
            "target_commitments_touched": [
                "Boolean model preservation",
                "uniformity and advice accounting",
                "barrier-aware lower-bound transfer",
            ],
            "gap_statement": (
                "The relevant research gap is a sharply typed bridge that avoids known barrier and quantifier leaks. The current workflow must prove, disprove, or quarantine such a bridge rather than accumulate partial analogies."
            ),
            "why_not_already_known": (
                "Classical NP-completeness and barrier literature frames the target and common obstructions, while modern lower-bound frontiers show restricted progress. The local avenue has not yet demonstrated a bridge that survives model, advice, and exponent transfer."
            ),
            "relevance_threshold": {
                "score": 3,
                "threshold": 4,
                "criterion": "Invest broadly only when a concrete bridge theorem or obstruction lemma can be stated with quantified transfer.",
                "evidence": "The route family is important, but most branch outputs remain at risk of moving proof debt into the bridge.",
            },
            "physics_or_field_impact": {
                "score": 4,
                "claim": "For complexity theory, impact means changing how a lower-bound route transfers to the Boolean main problem under barriers.",
                "evidence": "The route touches reductions, proof complexity, lower bounds, and barrier-aware transfer.",
                "missing": "A checked theorem or no-go statement for the exact bridge object.",
            },
            "unification_power": {
                "score": 4,
                "mechanism": "One typed bridge could unify restricted lower bounds, proof-system evidence, quantifier transfer, and barrier status.",
                "compresses": [
                    "source lower-bound evidence",
                    "target Boolean class consequence",
                    "uniformity/advice accounting",
                    "barrier status",
                ],
                "new_requirement_exposed": "The bridge must expose length regime, exponent window, reduction direction, and advice status as first-class obligations.",
            },
            "route_decision_power": {
                "score": 3,
                "decides": "Whether the next cycle should prove a scoped bridge/no-go theorem or reframe the gap before more broad exploration.",
                "next_decisive_test": "State the source theorem, target theorem, parameter map, barrier status, and one falsifier or countermodel for the bridge.",
            },
            "novelty_boundary": (
                "Novelty cannot be 'another P vs NP route'. It must be the exact bridge theorem, obstruction lemma, parameter calculation, or disqualifier test not already covered by known reductions and barriers."
            ),
            "disqualifier_matrix": [
                {
                    "disqualifier": "barrier_slogan",
                    "test": "The branch cites natural proofs, relativization, or algebrization without checking the exact property or oracle/algebraic interface.",
                    "decision_if_triggered": "reframe_gap_before_investment",
                    "status": "active",
                },
                {
                    "disqualifier": "advice_or_uniformity_leak",
                    "test": "The bridge selects hard objects, rows, formulas, or certificates nonuniformly without paying advice.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "open",
                },
                {
                    "disqualifier": "prior_art_absorbs_bridge",
                    "test": "Known lower-bound, proof-complexity, or meta-complexity literature already proves the bridge under the same assumptions.",
                    "decision_if_triggered": "do_not_invest_prior_art_collision",
                    "status": "open",
                },
            ],
            "explicit_unknowns": [
                "Whether the source lower-bound object is independently easier than the target separation.",
                "Whether the bridge preserves the target class without hidden advice.",
                "Whether the route has a scoped no-go theorem that is more valuable than another proof attempt.",
            ],
            "allowed_next_modes": ["literature_gap_reframe", "artifact_sprint", "falsifier_sprint", "proof_delivery"],
            "investment_decision": "reframe_gap_before_investment",
        }
    )
    return packet


def warrants_for_target(target_id: str) -> list[dict[str, Any]]:
    refs = compact_refs(target_id)
    if target_id == YM_TARGET_ID:
        return [ym_routea_warrant(refs), ym_representational_warrant(refs), ym_visual_warrant(refs)]
    if target_id == PVSNP_TARGET_ID:
        return [pvsnp_bridge_warrant(refs)]
    return [
        {
            **base_warrant(target_id, f"{target_id}.general_gap", "General literature-gap warrant", refs, []),
            "smallest_honest_claim": "A new avenue requires target-specific literature positioning before broad investment.",
            "mathematical_or_physical_object": "Unspecified target object requiring literature-gap reframe.",
            "target_commitments_touched": ["target-specific commitments"],
            "gap_statement": "No target-specific gap has been generated for this target.",
            "why_not_already_known": "The workflow lacks enough target-specific literature provenance to justify broad investment.",
            "relevance_threshold": {
                "score": 1,
                "threshold": 4,
                "criterion": "Generate target literature first.",
                "evidence": "Fallback packet only.",
            },
            "physics_or_field_impact": {
                "score": 1,
                "claim": "Unknown field impact.",
                "evidence": "Fallback packet only.",
                "missing": "Target literature and source objects.",
            },
            "unification_power": {
                "score": 1,
                "mechanism": "No unifying mechanism specified.",
                "compresses": ["unknown source pressure", "unknown target pressure"],
                "new_requirement_exposed": "Build a target-specific literature profile.",
            },
            "route_decision_power": {
                "score": 1,
                "decides": "Nothing beyond requiring reframe.",
                "next_decisive_test": "Run target literature source curation.",
            },
            "novelty_boundary": "No novelty boundary exists until literature curation is complete.",
            "disqualifier_matrix": [
                {
                    "disqualifier": "missing_literature",
                    "test": "No target literature packet is available.",
                    "decision_if_triggered": "reframe_gap_before_investment",
                    "status": "triggered",
                },
                {
                    "disqualifier": "vague_gap",
                    "test": "The gap is not target-specific.",
                    "decision_if_triggered": "quarantine_low_relevance",
                    "status": "triggered",
                },
                {
                    "disqualifier": "unknown_prior_art",
                    "test": "Closest known results are not named.",
                    "decision_if_triggered": "do_not_invest_prior_art_collision",
                    "status": "open",
                },
            ],
            "explicit_unknowns": ["closest known results", "target-specific source object"],
            "allowed_next_modes": ["literature_gap_reframe"],
            "investment_decision": "reframe_gap_before_investment",
        }
    ]


def package_for_target(target_id: str) -> dict[str, Any]:
    warrants = warrants_for_target(target_id)
    decision_counts: dict[str, int] = {}
    for warrant in warrants:
        decision = clean_text(warrant.get("investment_decision")) or "missing"
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": target_id,
        "status": "implemented",
        "purpose": (
            "Target-scoped preinvestment literature-gap warrants. Broad proof-search investment is blocked unless an avenue "
            "has a validated warrant with enough novelty, field impact, unification power, and route-decision power."
        ),
        "warrant_count": len(warrants),
        "investment_decision_counts": decision_counts,
        "warrants": warrants,
        "report_paths": {
            "latest_json": rel(target_warrant_latest_json(target_id)),
            "latest_md": rel(target_warrant_latest_md(target_id)),
        },
        "validation_handoff": {
            "validator": "agentic/scripts/validate_avenue_literature_gap_warrant.py",
            "dispatch_phase": "avenue_literature_gap_precheck",
            "report_integration": "agentic/scripts/build_discovery_marathon_report.py and agentic/scripts/generate_discovery_marathon_html.py",
        },
    }


def render_markdown(package: dict[str, Any]) -> str:
    lines = [
        "# Avenue Literature-Gap Warrants",
        "",
        f"Target: `{package['target_id']}`",
        f"Status: `{package['status']}`",
        f"Warrants: `{package['warrant_count']}`",
        f"Investment decisions: `{package['investment_decision_counts']}`",
        "",
        package["purpose"],
        "",
    ]
    for warrant in package.get("warrants", []):
        lines.extend(
            [
                f"## {clean_text(warrant.get('avenue_title'))}",
                "",
                f"- Avenue: `{clean_text(warrant.get('avenue_id'))}`",
                f"- Decision: `{clean_text(warrant.get('investment_decision'))}`",
                f"- Allowed next modes: `{', '.join(warrant.get('allowed_next_modes', []))}`",
                f"- Relevance score: `{warrant.get('relevance_threshold', {}).get('score')}`",
                f"- Field-impact score: `{warrant.get('physics_or_field_impact', {}).get('score')}`",
                f"- Unification score: `{warrant.get('unification_power', {}).get('score')}`",
                f"- Route-decision score: `{warrant.get('route_decision_power', {}).get('score')}`",
                "",
                f"Smallest honest claim: {clean_text(warrant.get('smallest_honest_claim'))}",
                "",
                f"Gap statement: {clean_text(warrant.get('gap_statement'))}",
                "",
                f"Why not already known: {clean_text(warrant.get('why_not_already_known'))}",
                "",
                "Closest known results:",
                "",
            ]
        )
        for ref in warrant.get("closest_known_results", []):
            lines.append(
                f"- `{clean_text(ref.get('ref_id'))}` {clean_text(ref.get('authors'))} ({ref.get('year')}), "
                f"{clean_text(ref.get('title'))}: {clean_text(ref.get('limitation_for_this_avenue'))}"
            )
        lines.extend(["", "Disqualifiers:", ""])
        for item in warrant.get("disqualifier_matrix", []):
            lines.append(
                f"- `{clean_text(item.get('disqualifier'))}` -> `{clean_text(item.get('decision_if_triggered'))}`: "
                f"{clean_text(item.get('test'))}"
            )
        lines.append("")
    lines.extend(
        [
            "## Validation",
            "",
            f"Run `{package.get('validation_handoff', {}).get('validator')}` before starting or promoting broad branch exploration.",
            "",
        ]
    )
    return "\n".join(lines)


def write_package(target_id: str) -> dict[str, Any]:
    package = package_for_target(target_id)
    directory = target_warrant_dir(target_id)
    directory.mkdir(parents=True, exist_ok=True)
    for warrant in package["warrants"]:
        name = clean_text(warrant["avenue_id"]).split(".")[-1].replace("-", "_")
        if warrant["avenue_id"] == "ym.routea.endpoint_source_table":
            path = directory / "routea_endpoint_warrant.json"
        elif warrant["avenue_id"] == "ym.representational_dynamics":
            path = directory / "representational_dynamics_warrant.json"
        elif warrant["avenue_id"] == "ym.visual_conceptualization":
            path = directory / "visual_conceptualization_warrant.json"
        else:
            path = directory / f"{name}_warrant.json"
        write_json(path, warrant)
    write_json(target_warrant_latest_json(target_id), package)
    write_markdown(target_warrant_latest_md(target_id), render_markdown(package))
    return package


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-id", action="append", dest="target_ids")
    args = parser.parse_args()
    target_ids = args.target_ids or [YM_TARGET_ID, PVSNP_TARGET_ID]
    packages = [write_package(target_id) for target_id in target_ids]
    for package in packages:
        print(
            f"Wrote {package['warrant_count']} avenue literature-gap warrant(s) for {package['target_id']} "
            f"to {package['report_paths']['latest_json']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
