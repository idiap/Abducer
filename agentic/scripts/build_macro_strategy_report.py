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
"""Build macro strategy synthesis from the accumulated discovery story."""

from __future__ import annotations

import json
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json
from discovery_marathon_common import LATEST_JSON, write_markdown


OUT_DIR = ROOT / "agentic/reports/macro_strategy"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
TARGET_LITERATURE = ROOT / "agentic/reports/target_literature_evolution/latest.json"
CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"
QUALITATIVE_GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"
FINITE_ALGEBRA = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
ANALYTIC_OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def cycle_rows() -> list[dict[str, Any]]:
    report = load_optional_json(LATEST_JSON)
    rows = report.get("cycle_summaries", [])
    return [row for row in rows if isinstance(row, dict) and row.get("valid_as_research_cycle")]


def cycle_number(row: dict[str, Any]) -> int:
    try:
        return int(clean_text(row.get("cycle_id")).split("-")[-1])
    except ValueError:
        return 0


def matching_cycles(rows: list[dict[str, Any]], terms: list[str], limit: int = 6) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        text = clean_text(
            " ".join(
                [
                    row.get("branch_title", ""),
                    row.get("mathematical_learning", ""),
                    row.get("blocking_gap", ""),
                    row.get("next_experiment", ""),
                ]
            )
        )
        if contains_any(text, terms):
            selected.append(
                {
                    "cycle_id": clean_text(row.get("cycle_id")),
                    "branch_title": clean_text(row.get("branch_title")),
                    "learning": clean_text(row.get("mathematical_learning")),
                    "next_experiment": clean_text(row.get("next_experiment")),
                }
            )
    return selected[-limit:]


def score_strategy(rows: list[dict[str, Any]], terms: list[str]) -> int:
    matches = len(matching_cycles(rows, terms, limit=999))
    return min(100, 42 + matches * 8)


def strategy_packet(
    *,
    strategy_id: str,
    title: str,
    route_family: str,
    macro_thesis: str,
    physics_picture: str,
    why_now: str,
    what_to_compute_next: list[str],
    success_condition: list[str],
    failure_or_pivot_condition: list[str],
    literature_refs: list[str],
    active_skills: list[str],
    terms: list[str],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    evidence = matching_cycles(rows, terms)
    return {
        "strategy_id": strategy_id,
        "title": title,
        "route_family": route_family,
        "priority_score": score_strategy(rows, terms),
        "macro_thesis": macro_thesis,
        "physics_picture": physics_picture,
        "why_now": why_now,
        "evidence_from_story": evidence,
        "what_to_compute_next": what_to_compute_next,
        "success_condition": success_condition,
        "failure_or_pivot_condition": failure_or_pivot_condition,
        "linked_literature_refs": literature_refs,
        "active_skills": active_skills,
        "status": "primary_macro_strategy" if evidence else "watch_strategy",
        "epistemic_status": "interpretive_synthesis_from_story",
    }


def build_report() -> dict[str, Any]:
    marathon = load_optional_json(LATEST_JSON)
    target_id = clean_text(marathon.get("target_id")) or "yang-mills-existence-and-mass-gap-target"
    rows = sorted(cycle_rows(), key=cycle_number)
    literature = load_optional_json(TARGET_LITERATURE)
    contribution = load_optional_json(CONTRIBUTION_MONITOR)
    qualitative = load_optional_json(QUALITATIVE_GRAPH)
    finite = load_optional_json(FINITE_ALGEBRA)
    analytic = load_optional_json(ANALYTIC_OBLIGATIONS)
    if target_id == "p-vs-np-target":
        strategies = [
            strategy_packet(
                strategy_id="macro.pvsnp-black-box-transfer-audit",
                title="Black-box transfer and exponent-window audit",
                route_family="Complexity lower-bound transfer",
                macro_thesis=(
                    "Treat every proposed magnification route as an explicit transfer inequality from SAT in SIZE(n^c) "
                    "or NP subset P/poly to a source-carrier upper bound."
                ),
                physics_picture=(
                    "For this complexity-theory target, read the physical picture as a proof-dynamics picture: "
                    "the target circuit is a resource flowing through an interface. Positive query-length exponent beta "
                    "amplifies the target exponent c and prevents a barely-superlinear source lower bound from ruling out all polynomial-size SAT circuits."
                ),
                why_now=(
                    "The latest cycle isolated max{a,q+beta c} as the active obstruction, so the next work must compute a, q, and beta rather than restate magnification."
                ),
                what_to_compute_next=[
                    "For the selected carrier, compute source exponent a, interface overhead q, and target-query exponent beta.",
                    "Derive the induced source upper bound under SAT in SIZE(n^c).",
                    "Promote only if beta=0, beta=o(1), or the use of the SAT circuit is genuinely nonblackbox.",
                ],
                success_condition=[
                    "A formal transfer theorem states source object, target class, model, and exponent inequality.",
                    "The theorem distinguishes bounded-exponent exclusion from NP not subset P/poly.",
                    "The branch yields a computable falsifier for black-box substitution routes.",
                ],
                failure_or_pivot_condition=[
                    "Every tested carrier has positive beta and only excludes c below a finite threshold.",
                    "The interface size q already exceeds the barely-superlinear threshold.",
                    "The route cannot name the model and quantifier pattern in one statement.",
                ],
                literature_refs=["ref.cook-1971", "ref.karp-1972", "ref.hardness-magnification-modern"],
                active_skills=[
                    "pvsnp-symbolic-complexity-auditor",
                    "pvsnp-qualitative-complexity-reasoner",
                    "pvsnp-conceptual-pressure-localizer",
                    "entailment-gap-auditor",
                    "progression-payoff-judge",
                ],
                terms=["black-box", "beta", "query", "sat", "size", "exponent", "interface", "carrier"],
                rows=rows,
            ),
            strategy_packet(
                strategy_id="macro.pvsnp-padding-projection-demagnification",
                title="Padding and projection demagnification as a no-go route",
                route_family="Projection carrier obstruction",
                macro_thesis=(
                    "Use the padding/projection failures as theorem material: projection carriers either give only bounded exponent windows "
                    "or move the real proof burden into sparse valid-length lower bounds."
                ),
                physics_picture=(
                    "The conceptual mechanism is proof-debt conservation. Padding changes the coordinate system, but projection back to SAT reveals "
                    "that the supposedly weak source lower bound already encodes the hard target lower bound."
                ),
                why_now=(
                    "Cycles 1-5 repeatedly converted padding optimism into exact exponent inequalities and sparse-length obligations."
                ),
                what_to_compute_next=[
                    "State the projection-carrier dichotomy as a standalone no-go theorem.",
                    "Define the length map N(n), projection overhead, and target exponent window.",
                    "List escape conditions: subpolynomial embedding, nonprojection carrier, or nonblackbox use.",
                ],
                success_condition=[
                    "The no-go theorem has precise hypotheses and a proof skeleton.",
                    "It explains why the route fails without claiming P vs NP.",
                    "It identifies which nonprojection alternatives remain open.",
                ],
                failure_or_pivot_condition=[
                    "The statement merely repeats padding folklore without a new quantified obstruction.",
                    "The theorem accidentally rules out nonprojection or nonblackbox routes.",
                    "The proof depends on a stronger source lower bound than advertised.",
                ],
                literature_refs=["ref.hardness-magnification-modern", "ref.nonuniform-circuit-lower-bounds", "ref.natural-proofs"],
                active_skills=[
                    "pvsnp-symbolic-complexity-auditor",
                    "pvsnp-impossibility-theorem-forger",
                    "contradiction-route-auditor",
                    "paper-contribution-readiness-judge",
                    "scientific-contribution-detector",
                ],
                terms=["padding", "projection", "sparse", "valid length", "demagnifies", "dichotomy", "lower bounds"],
                rows=rows,
            ),
            strategy_packet(
                strategy_id="macro.pvsnp-meta-complexity-carrier-pressure",
                title="Meta-complexity carrier pressure",
                route_family="MCSP/MKtP/GapMCSP route analysis",
                macro_thesis=(
                    "Use MCSP, MKtP, or GapMCSP only after the carrier's verifier overhead, density, naturalness, advice leakage, and target transfer are stated."
                ),
                physics_picture=(
                    "The meta-complexity carrier is a diagnostic medium: it can reveal whether a weak source lower bound really transfers, "
                    "or whether constructivity, largeness, and nonuniform advice absorb the intended separation."
                ),
                why_now=(
                    "Cycles 1, 2, 4, 5, and 6 all point to MCSP/MKtP as the next plausible nonprojection test, but cycle 6 already exposed a fixed-threshold ceiling."
                ),
                what_to_compute_next=[
                    "Instantiate one carrier with N, n, threshold s, verifier overhead, and circuit model.",
                    "Check natural-proof largeness and constructivity conditions.",
                    "Compute whether SAT in SIZE(n^c) yields carrier circuits below the claimed threshold.",
                ],
                success_condition=[
                    "The carrier avoids pure projection demagnification.",
                    "The transfer is target-preserving for NP not subset P/poly, not only a proxy consequence.",
                    "Barrier status is explicit and does not rely on hidden advice leakage.",
                ],
                failure_or_pivot_condition=[
                    "The induced upper bound remains N^{q+beta c+o(1)} with positive beta.",
                    "The lower-bound property is natural without an escape certificate.",
                    "The carrier proves only bounded-exponent or non-target consequences.",
                ],
                literature_refs=["ref.mcsp", "ref.mktp", "ref.razborov-rudich-1997", "ref.aaronson-wigderson-2009"],
                active_skills=[
                    "pvsnp-conceptual-pressure-localizer",
                    "pvsnp-symbolic-complexity-auditor",
                    "pvsnp-qualitative-complexity-reasoner",
                    "counterexample-hunter",
                    "kb-concept-bridge-planner",
                ],
                terms=["mcsp", "mktp", "gapmcsp", "meta-complexity", "truth table", "natural", "advice", "verifier"],
                rows=rows,
            ),
            strategy_packet(
                strategy_id="macro.pvsnp-nonblackbox-escape-search",
                title="Nonblackbox or subpolynomial-interface escape search",
                route_family="Escape-condition construction",
                macro_thesis=(
                    "The search should now aim at the exact escape left open by the no-go evidence: a target-preserving carrier with subpolynomial queries "
                    "or a genuinely nonblackbox use of the SAT circuit."
                ),
                physics_picture=(
                    "The route needs a new interaction pattern with the target circuit. If the circuit is only queried as a black box at polynomially growing target length, "
                    "the beta-ceiling reappears; a real escape must change that interface."
                ),
                why_now=(
                    "Cycle 7 localized the remaining opening as N^{o(1)} target queries, sub-N^{1+epsilon} interface size, and a valid lower-bound carrier."
                ),
                what_to_compute_next=[
                    "Test a succinct local-consistency or proof-complexity carrier.",
                    "Compute a, q, and beta before making any magnification claim.",
                    "Run the projection-demagnification falsifier and barrier audit immediately.",
                ],
                success_condition=[
                    "A carrier is target-preserving and not a disguised projection route.",
                    "The interface has beta=0 or o(1), or the construction is nonblackbox in a formally stated sense.",
                    "The next theorem can be stated as either a positive transfer or a no-go lemma.",
                ],
                failure_or_pivot_condition=[
                    "The carrier uses polynomial target queries after all.",
                    "The proof obligation becomes as hard as the original P vs NP/P-poly target.",
                    "The route cannot avoid naturalness, advice leakage, or algebrization pressure.",
                ],
                literature_refs=["ref.proof-complexity", "ref.algebrization", "ref.hardness-magnification-modern"],
                active_skills=[
                    "pvsnp-symbolic-complexity-auditor",
                    "pvsnp-impossibility-theorem-forger",
                    "pvsnp-qualitative-complexity-reasoner",
                    "kb-gap-abstraction-conjecturer",
                    "abducer-refinement-route-ranker",
                ],
                terms=["nonblackbox", "non-blackbox", "subpolynomial", "succinct", "local-consistency", "proof-complexity", "n^{o(1)}"],
                rows=rows,
            ),
        ]
        strategies.sort(key=lambda item: -int(item["priority_score"]))
        for index, strategy in enumerate(strategies, start=1):
            strategy["rank"] = index
        return {
            "version": 1,
            "generated_utc": utc_now(),
            "target_id": target_id,
            "headline": "Current macro strategy: compute the transfer exponents or turn the route into a no-go theorem.",
            "strategy_status": "active_macro_strategy_synthesis",
            "physics_language_standard": (
                "For P vs NP, strategy language must speak in complexity-theoretic mechanisms: verification versus search, "
                "SAT circuit lower bounds, nonuniformity, barriers, transfer exponents, carriers, and quantifier strength."
            ),
            "story_basis": {
                "research_cycle_count": len(rows),
                "latest_cycle_id": rows[-1].get("cycle_id", "") if rows else "",
                "dominant_branch": rows[-1].get("branch_title", "") if rows else "",
                "target_literature_report": rel(TARGET_LITERATURE),
                "contribution_monitor": rel(CONTRIBUTION_MONITOR),
                "qualitative_graph": "target-specific qualitative complexity graph pending",
                "finite_algebra": "finite algebra is replaced by exact symbolic complexity-transfer audits",
                "analytic_obligations": "complexity transfer obligations are carried by cycle queue items and symbolic exponent-window checks",
                "qualitative_relation_count": 0,
                "finite_packet_count": 0,
                "analytic_obligation_count": 0,
                "good_enough_contributions": int(contribution.get("metrics", {}).get("good_enough_count", 0)) if isinstance(contribution, dict) else 0,
                "literature_stage_count": len(literature.get("literature_stages", [])) if isinstance(literature, dict) else 0,
            },
            "macro_strategies": strategies,
            "recommended_next_posture": {
                "primary": "Compute a, q, and beta for the next proposed carrier before any broader marathon continuation.",
                "secondary": "Package padding/projection and black-box substitution failures as bounded no-go theorem candidates.",
                "handoff": "Promote only a formal transfer theorem or route-specific impossibility theorem toward paper form.",
                "avoid": "Do not spend cycles restating hardness magnification without a carrier, model, quantifier regime, and falsifier.",
            },
        }
    strategies = [
        strategy_packet(
            strategy_id="macro.os-reflection-positivity-wilson-collar",
            title="OS reflection positivity through Wilson collar quotients",
            route_family="Euclidean reconstruction / reflection positivity",
            macro_thesis=(
                "Treat the mass-gap problem as first requiring a same-theory Euclidean positivity bridge: "
                "Wilson-loop observables near a reflection plane must define positive Schwinger data that survive collar collapse and continuum passage."
            ),
            physics_picture=(
                "The physical picture is a Euclidean half-space experiment. Gauge-invariant Wilson hairpins approach the reflection plane; "
                "their reflected Gram matrix is a finite shadow of the Hilbert-space inner product that OS reconstruction would later produce. "
                "If the quotient matrix develops a negative tangent direction, phase holonomy, or Schur-complement obstruction, the route fails before any Hamiltonian gap claim is meaningful."
            ),
            why_now=(
                "The recent cycles repeatedly sharpened finite PSD tangent-cone tests near the rank-one quotient. "
                "This is now the most concrete bridge between the generated mathematics and the Clay requirement that the quantum theory be reconstructed, not postulated."
            ),
            what_to_compute_next=[
                "Compute first-order boundary-OPE kernels H for three- and four-hairpin reflected Wilson families with a common boundary footprint.",
                "Test H on the zero-sum subspace and, when ker(PHP) is nontrivial, compute the second-order Schur complement form.",
                "Record whether the obstruction is a same-theory Wilson observable obstruction or only an artifact of the finite collar model.",
            ],
            success_condition=[
                "A controlled reflected Wilson family yields PSD finite Gram quotients under stated OS assumptions.",
                "The collar limit keeps the observable algebra, reflection map, and continuum target object fixed.",
                "The result produces a bridge lemma or a publishable finite obstruction with explicit assumptions.",
            ],
            failure_or_pivot_condition=[
                "A negative zero-sum direction, nontrivial phase holonomy, or failed Schur-complement condition appears in the same theory.",
                "The boundary OPE remainder cannot be controlled uniformly in the collar/cutoff regime.",
                "The construction only describes a proxy boundary sector rather than the reconstructed Yang-Mills observable algebra.",
            ],
            literature_refs=["ref.os-1973-1975", "ref.jaffe-witten-clay", "ref.wilson-1974"],
            active_skills=[
                "kb-contradiction-strategist",
                "finite-algebra-interface-builder",
                "qualitative-physics-falsifier",
                "contribution-oriented-subgoal-manager",
            ],
            terms=["reflection", "positivity", "os", "wilson", "hairpin", "collar", "quotient", "schur", "kernel", "psd"],
            rows=rows,
        ),
        strategy_packet(
            strategy_id="macro.rg-continuum-construction",
            title="RG and continuum construction discipline",
            route_family="Constructive QFT / renormalization group",
            macro_thesis=(
                "Keep every local finite calculation subordinate to the real constructive burden: build a nontrivial continuum Yang-Mills object "
                "with regulator-uniform estimates, not merely a lattice or fixed-cutoff theory."
            ),
            physics_picture=(
                "Asymptotic freedom says the ultraviolet side is controllable in principle, while confinement lives in the infrared. "
                "The constructive strategy is therefore a double-scale story: remove the UV cutoff without losing positivity or gauge invariance, "
                "then prevent the infrared/spectral information from evaporating in the infinite-volume continuum limit."
            ),
            why_now=(
                "The active story keeps running into collar, cutoff, boundary-OPE, and uniform-remainder gaps. "
                "That means the macro strategy must keep asking which estimates are stable under regulator removal."
            ),
            what_to_compute_next=[
                "For each finite obstruction or quotient identity, name the cutoff, volume, collar parameter, and required uniform bound.",
                "Promote only formulas that state what remains bounded or convergent as the regulator is removed.",
                "Use prior-art and evidence tasks to check whether Balaban-style RG estimates can support the required Wilson observable family.",
            ],
            success_condition=[
                "A candidate bridge names a limiting Schwinger family or equivalent continuum object.",
                "Reflection positivity, gauge invariance, and observable nontriviality are preserved under the same limiting procedure.",
                "The route can state the exact uniform estimate still missing.",
            ],
            failure_or_pivot_condition=[
                "The argument works only at fixed lattice spacing, finite volume, or strong coupling with no continuum transfer.",
                "Constants needed for the gap or positivity degenerate to zero in the limit.",
                "The limit becomes Gaussian, empty, or changes the gauge theory.",
            ],
            literature_refs=["ref.gross-wilczek-1973", "ref.politzer-1973", "ref.balaban-1985", "ref.glimm-jaffe-1981"],
            active_skills=[
                "target-literature-evolution-narrator",
                "prior-art-importer",
                "evidence-acquisition-planner",
                "abducer-obligation-gatekeeper",
            ],
            terms=["continuum", "cutoff", "uniform", "rg", "balaban", "boundary ope", "limit", "remainder"],
            rows=rows,
        ),
        strategy_packet(
            strategy_id="macro.spectral-gap-after-reconstruction",
            title="Spectral gap only after reconstruction",
            route_family="Hamiltonian / mass-gap witness",
            macro_thesis=(
                "Do not chase a Hamiltonian gap in isolation. The spectral statement matters only after the Hilbert space, vacuum, Hamiltonian, "
                "and gauge-invariant excitation sector are reconstructed from the same Euclidean theory."
            ),
            physics_picture=(
                "The mass gap is the energy cost of the lightest non-vacuum excitation, physically the glueball-like scale in pure gauge theory. "
                "Euclidean correlator decay is useful because OS reconstruction can turn decay into spectral support, but only if the observable family is dense enough in the physical sector."
            ),
            why_now=(
                "The current route has learned that finite OS positivity tests are upstream of spectral language. "
                "The spectral strategy remains essential, but it should be activated as a witness layer once reconstruction and observable-density conditions are typed."
            ),
            what_to_compute_next=[
                "Maintain a premise ledger for H, Omega, P_perp, and gauge-invariant observable density.",
                "Convert any Euclidean decay estimate into an explicit spectral theorem statement with validity conditions.",
                "Reject any gap claim whose Hilbert space or vacuum is postulated rather than reconstructed.",
            ],
            success_condition=[
                "OS-positive continuum Schwinger functions reconstruct a physical Hilbert space, vacuum, and Hamiltonian.",
                "Gauge-invariant observables create a dense enough non-vacuum sector.",
                "A cutoff-uniform decay or direct spectral lower bound excludes spectrum in (0, Delta).",
            ],
            failure_or_pivot_condition=[
                "The decay estimate is only fixed-regulator or applies to a non-determining observable family.",
                "The Hamiltonian is introduced before reconstruction.",
                "The claimed gap lives in a different theory from the constructed continuum object.",
            ],
            literature_refs=["ref.streater-wightman-1964", "ref.os-1973-1975", "ref.jaffe-witten-clay"],
            active_skills=[
                "kb-proof-sketcher",
                "kb-end-to-end-proof-critic",
                "hamiltonian-gap-derivation",
                "entailment-gap-auditor",
            ],
            terms=["spectral", "mass gap", "hamiltonian", "decay", "hilbert", "vacuum", "observable density"],
            rows=rows,
        ),
        strategy_packet(
            strategy_id="macro.finite-obstruction-science",
            title="Publishable finite obstruction science",
            route_family="Finite algebra / falsifier-driven discovery",
            macro_thesis=(
                "Treat finite Wilson-quotient algebra as a source of serious scientific contributions: even before solving the Clay problem, "
                "a sharp obstruction, tangent-cone criterion, or phase falsifier can be a reusable result."
            ),
            physics_picture=(
                "A finite reflected Wilson matrix is a small interferometer for gauge-invariant boundary data. "
                "Its determinant, zero-sum tangent form, holonomy, and Schur complement reveal whether a proposed Euclidean positivity mechanism can even reach the Hilbert-space inner product."
            ),
            why_now=(
                "The contribution monitor currently marks multiple obstruction candidates as handoff-ready. "
                "That means the strategy should stop endless exploration of those branches and convert the best obstruction into validation and paper form."
            ),
            what_to_compute_next=[
                "Select the strongest finite obstruction candidate and write the smallest honest theorem statement.",
                "Run prior-art comparison for quotient positivity, correlation matrices, reflection positivity, and Wilson-loop boundary OPEs.",
                "Draft a scoped note with assumptions, exact finite criterion, falsifiers, and limits.",
            ],
            success_condition=[
                "The finite criterion is mathematically exact under stated assumptions.",
                "The criterion is useful even if the full Yang-Mills problem remains open.",
                "The paper handoff separates same-theory claims from proxy or model claims.",
            ],
            failure_or_pivot_condition=[
                "The obstruction is already standard prior art with no new formulation or workflow implication.",
                "The finite carrier cannot be connected to Yang-Mills observables even as a bounded diagnostic.",
                "The result is only a report artifact and not a reusable mathematical object.",
            ],
            literature_refs=["ref.os-1973-1975", "ref.wilson-1974", "ref.jaffe-witten-clay"],
            active_skills=[
                "scientific-contribution-detector",
                "contribution-value-assessor",
                "scientific-contribution-paper-handoff",
                "prior-art-importer",
            ],
            terms=["determinant", "falsifier", "obstruction", "holonomy", "schur", "finite", "quotient", "contribution"],
            rows=rows,
        ),
    ]
    strategies.sort(key=lambda item: -int(item["priority_score"]))
    for index, strategy in enumerate(strategies, start=1):
        strategy["rank"] = index
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": load_optional_json(LATEST_JSON).get("target_id", "yang-mills-existence-and-mass-gap-target"),
        "headline": "Current macro strategy: prove or falsify the Euclidean-to-Hilbert bridge before making spectral-gap claims.",
        "strategy_status": "active_macro_strategy_synthesis",
        "physics_language_standard": (
            "Strategies must speak in terms of Yang-Mills gauge fields, Wilson observables, Schwinger functions, reflection positivity, "
            "continuum limits, reconstructed Hilbert space, and spectral gap witnesses."
        ),
        "story_basis": {
            "research_cycle_count": len(rows),
            "latest_cycle_id": rows[-1].get("cycle_id", "") if rows else "",
            "dominant_branch": rows[-1].get("branch_title", "") if rows else "",
            "target_literature_report": rel(TARGET_LITERATURE),
            "contribution_monitor": rel(CONTRIBUTION_MONITOR),
            "qualitative_graph": rel(QUALITATIVE_GRAPH),
            "finite_algebra": rel(FINITE_ALGEBRA),
            "analytic_obligations": rel(ANALYTIC_OBLIGATIONS),
            "qualitative_relation_count": len(qualitative.get("edges", [])) if isinstance(qualitative, dict) else 0,
            "finite_packet_count": int(finite.get("summary", {}).get("packet_count", 0)) if isinstance(finite, dict) else 0,
            "analytic_obligation_count": len(analytic.get("obligations", [])) if isinstance(analytic, dict) else 0,
            "good_enough_contributions": int(contribution.get("metrics", {}).get("good_enough_count", 0)) if isinstance(contribution, dict) else 0,
            "literature_stage_count": len(literature.get("literature_stages", [])) if isinstance(literature, dict) else 0,
        },
        "macro_strategies": strategies,
        "recommended_next_posture": {
            "primary": "Run the OS/Wilson-collar route until the finite tangent-cone obstruction is either certified or demoted.",
            "secondary": "Keep RG/continuum construction as the transfer discipline for every finite calculation.",
            "handoff": "Convert the strongest finite obstruction candidate into validation and paper form when prior-art checks pass.",
            "avoid": "Do not pivot to Hamiltonian spectral-gap claims before reconstruction and observable-density premises are explicit.",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Macro Strategy Report",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Headline: {report['headline']}",
        f"- Status: `{report['strategy_status']}`",
        "",
        "## Recommended Next Posture",
        "",
    ]
    for key, value in report["recommended_next_posture"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Macro Strategies", ""])
    for strategy in report["macro_strategies"]:
        lines.extend(
            [
                f"### {strategy['rank']}. {strategy['title']}",
                "",
                f"- Route family: `{strategy['route_family']}`",
                f"- Priority score: `{strategy['priority_score']}`",
                f"- Thesis: {strategy['macro_thesis']}",
                f"- Physics picture: {strategy['physics_picture']}",
                f"- Why now: {strategy['why_now']}",
                f"- Literature refs: `{', '.join(strategy['linked_literature_refs'])}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    write_markdown(OUT_MD, render_markdown(report))
    print(f"wrote {rel(OUT_JSON)}")
    print(f"wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
