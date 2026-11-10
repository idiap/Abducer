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
"""Build P vs NP pressure-to-bridge abstraction candidates.

The script is intentionally deterministic but not a placeholder: it scans the
P vs NP KB and recent marathon artifacts for named complexity-theoretic
pressure signals, then maps those signals to bridge abstractions with proof
obligations, falsifiers, and skill handoffs.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
DEFAULT_MD = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.md"
KB = ROOT / "KB/p-vs-np.kb.md"
CYCLES = ROOT / "agentic/runs/discovery_marathons/p-vs-np-marathon/cycles"
SUBWORKFLOW = ROOT / "agentic/reports/subworkflow_integration/latest.md"


PRESSURE_TERMS: dict[str, list[str]] = {
    "hardness_magnification_ceiling": [
        "hardness magnification",
        "bounded exponent",
        "all-polynomial",
        "barely-superlinear",
        "exponent window",
    ],
    "black_box_substitution_cap": [
        "black-box",
        "oracle",
        "substitution",
        "beta",
        "target-query",
        "sat query",
    ],
    "meta_complexity_carrier_debt": [
        "mcsp",
        "mktp",
        "gap-mcsp",
        "kt-complexity",
        "truth table",
    ],
    "proof_complexity_transfer_gap": [
        "proof-complexity",
        "tautology",
        "resolution",
        "frege",
        "ips",
        "certificate",
    ],
    "naturalness_density_pressure": [
        "natural",
        "largeness",
        "constructive",
        "density",
        "pseudorandom",
        "prf",
    ],
    "padding_projection_debt": [
        "padding",
        "projection",
        "sparse",
        "valid length",
        "length map",
    ],
    "advice_uniformity_leakage": [
        "advice",
        "nonuniform",
        "uniform",
        "preprocessing",
        "p/poly",
    ],
    "relativization_algebrization_boundary": [
        "relativ",
        "algebr",
        "oracle",
        "nonrelativizing",
        "nonalgebrizing",
    ],
}


@dataclass(frozen=True)
class BridgeProfile:
    bridge_id: str
    title: str
    pressure_types: tuple[str, ...]
    source_object: str
    target_object: str
    bridge_abstraction: str
    difficulty_hypothesis: str
    controlled_interface: str
    preserved_invariant: str
    proof_obligation: str
    symbolic_probe: str
    falsifiers: tuple[str, ...]
    persist_condition: str
    pivot_condition: str
    validation_handoff: tuple[str, ...]
    paper_safe_narrative: str


PROFILES: tuple[BridgeProfile, ...] = (
    BridgeProfile(
        bridge_id="pvsnp-bridge-001",
        title="Subpolynomial nonblackbox interface bridge",
        pressure_types=("black_box_substitution_cap", "hardness_magnification_ceiling", "padding_projection_debt"),
        source_object="a barely-superlinear source carrier L_N with lower bound SIZE(L_N)>N^{1+epsilon}",
        target_object="SAT lower bounds strong enough to imply NP not subset P/poly",
        bridge_abstraction=(
            "Replace plain black-box SAT-oracle substitution by an interface whose target-circuit dependence is "
            "beta=0 or N^{o(1)}, or by a genuinely nonblackbox use of the target circuit that cannot be counted as "
            "N^{q+beta c} gate substitution."
        ),
        difficulty_hypothesis=(
            "The route is hard because positive query-length exponent beta converts any fixed epsilon source margin "
            "into only a finite SAT exponent window, so the bridge must remove or structurally transform the beta*c term."
        ),
        controlled_interface=(
            "State ordinary overhead q, target-query length exponent beta, adaptivity model, advice accounting, and "
            "whether the target circuit is used as a replaceable oracle gate or as a nonblackbox object."
        ),
        preserved_invariant="same nonuniform circuit model, same valid lengths, no hidden advice, and all-exponent target quantifier",
        proof_obligation=(
            "Prove a transfer theorem in which SAT in SIZE(n^c) induces source circuits below N^{1+epsilon} for every fixed c, "
            "or prove a no-go theorem that every black-box interface with beta>0 gives only c<(1+epsilon-q)/beta."
        ),
        symbolic_probe="Run audit_transfer.py with exact a=1+epsilon, q, beta; promote only if beta=0 with positive margin or a certified nonblackbox escape is supplied.",
        falsifiers=(
            "beta>0 and q<1+epsilon yields only a bounded exponent window.",
            "q>=1+epsilon lets the interface consume the source lower-bound margin.",
            "nonblackbox use is merely oracle substitution in disguise.",
        ),
        persist_condition="Persist only if the next step computes q and beta for a named carrier and identifies the nonblackbox operation that blocks gate-by-gate substitution.",
        pivot_condition="Pivot to a no-go theorem if two named carriers still produce beta>0 or q>=1+epsilon under exact audit.",
        validation_handoff=("pvsnp-symbolic-complexity-auditor", "pvsnp-impossibility-theorem-forger", "contradiction-route-auditor"),
        paper_safe_narrative=(
            "The bridge problem is not the existence of a hard carrier alone, but the construction of an interface whose "
            "dependence on hypothetical SAT circuits does not reintroduce the target exponent."
        ),
    ),
    BridgeProfile(
        bridge_id="pvsnp-bridge-002",
        title="Searchable succinct meta-complexity certificate bridge",
        pressure_types=("meta_complexity_carrier_debt", "advice_uniformity_leakage", "naturalness_density_pressure"),
        source_object="sound O(m)-bit certificates for high MCSP/MKtP truth tables with bounded source-length gaps",
        target_object="a uniform E or NP-adjacent language with explicit circuit lower bounds",
        bridge_abstraction=(
            "Use searchable certificates as the carrier instead of advised hard truth tables, so that uniform search "
            "rather than nonuniform choice selects the hard slice."
        ),
        difficulty_hypothesis=(
            "The hard part is not defining MCSP; it is finding compact sound certificates whose existence is frequent enough "
            "to build a uniform language without making the accepted set large and constructive."
        ),
        controlled_interface=(
            "Verifier V, decoder D, certificate length, verifier time, source gap kappa, soundness threshold epsilon, "
            "density of accepted codes, and deterministic search schedule."
        ),
        preserved_invariant="uniform construction of the target language, no advice-selected hard strings, and exact worst-case lower-bound soundness",
        proof_obligation=(
            "Show that accepted certificate pairs exist in every kappa-gap interval, have O(m)-bit descriptions, are searchable in 2^{O(m)}, "
            "and soundly imply CC(f_u)>2^{epsilon m}."
        ),
        symbolic_probe="Audit delta<epsilon/kappa transfer and test whether certificate length or verifier time remains single-exponential in target length.",
        falsifiers=(
            "Accepted pairs exist only through advice or nonuniform selection.",
            "Certificate length or verifier time becomes m^{1+Omega(1)} in the exponent and leaves E.",
            "The accepted certificate set is dense, polynomial-time decidable, and useful, triggering natural-proof pressure.",
        ),
        persist_condition="Persist if a named proof or meta-complexity object gives compact sound certificates with explicit gap coverage and no advice.",
        pivot_condition="Backtrack if certificate existence is equivalent to the target lower bound or if searchability destroys the target class.",
        validation_handoff=("pvsnp-qualitative-complexity-reasoner", "pvsnp-symbolic-complexity-auditor", "paper-contribution-readiness-judge"),
        paper_safe_narrative=(
            "The proposed abstraction shifts attention from hard truth tables to uniformly searchable certificates of hardness, "
            "making advice leakage and naturalness the central tests."
        ),
    ),
    BridgeProfile(
        bridge_id="pvsnp-bridge-003",
        title="Proof-complexity lower-bound certificate bridge",
        pressure_types=("proof_complexity_transfer_gap", "meta_complexity_carrier_debt", "naturalness_density_pressure"),
        source_object="lower-bound tautologies LB(u,s) in a specified Cook-Reckhow proof system",
        target_object="circuit lower bounds or meta-complexity hardness statements connected to P vs NP",
        bridge_abstraction=(
            "Treat proof objects as the medium connecting semantic circuit lower bounds to verifiable mathematical evidence, "
            "with the proof system acting as the controlled interface."
        ),
        difficulty_hypothesis=(
            "The route is hard because a proof certificate must be short enough to search or verify while still soundly certifying "
            "a semantic lower bound that is usually as hard as the target."
        ),
        controlled_interface=(
            "Tautology family, proof system, proof length bound, verifier complexity, semantic soundness of LB(u,s), and target lower-bound transfer."
        ),
        preserved_invariant="same proof system, explicit soundness statement, no replacement of semantic lower bound by syntactic proof length alone",
        proof_obligation=(
            "For a named proof system Psys, formulate LB(u,2^{epsilon m}); prove that short Psys proofs imply searchable hardness witnesses, "
            "or prove that any such bridge would yield a route-specific no-go."
        ),
        symbolic_probe="Compute witness length, proof length, verifier overhead, and resulting target exponent margin before claiming transfer.",
        falsifiers=(
            "The proof length needed is already exponential beyond the target class.",
            "The tautology certifies only proof-system hardness, not circuit lower bounds for f_u.",
            "The route collapses into known proof-complexity lower-bound conjectures without a new carrier interface.",
        ),
        persist_condition="Persist if a concrete proof system and tautology family make the semantic soundness and search overhead explicit.",
        pivot_condition="Pivot by converting to an impossibility theorem if the bridge requires proof lower bounds as hard as the intended circuit lower bound.",
        validation_handoff=("pvsnp-impossibility-theorem-forger", "pvsnp-symbolic-complexity-auditor", "kb-macro-proof-paper-writer"),
        paper_safe_narrative=(
            "A proof-complexity bridge is valuable only if the proof object does more than rename semantic hardness; it must control how "
            "hardness evidence is verified and transported."
        ),
    ),
    BridgeProfile(
        bridge_id="pvsnp-bridge-004",
        title="Sparse non-natural property bridge",
        pressure_types=("naturalness_density_pressure", "relativization_algebrization_boundary", "advice_uniformity_leakage"),
        source_object="truth-table or meta-complexity property intended to be useful against polynomial-size circuits",
        target_object="non-natural lower-bound evidence compatible with cryptographic pseudorandomness barriers",
        bridge_abstraction=(
            "Constrain the property to be nonlarge, sparse, nonconstructive in the forbidden sense, or proof-system mediated, "
            "while preserving enough usefulness to imply the target lower bound."
        ),
        difficulty_hypothesis=(
            "The route is hard because usefulness against a rich circuit class plus efficient constructivity tends to create a natural property "
            "unless largeness or constructivity is explicitly broken."
        ),
        controlled_interface="Property density, constructivity time, usefulness class, PRF assumption, and whether the property is defined on all truth tables or a sparse valid slice.",
        preserved_invariant="usefulness against the target circuit class without claiming a large constructive property",
        proof_obligation=(
            "Prove either non-largeness, nonconstructivity, or a proof-mediated escape while retaining a formal implication from property membership to target lower bound."
        ),
        symbolic_probe="Build a natural-proof ledger with largeness, constructivity, usefulness, and PRF-status fields for the candidate property.",
        falsifiers=(
            "The property is dense and decidable in polynomial time over truth tables.",
            "Usefulness is stated only for a weaker circuit class than the target route needs.",
            "The sparse slice has no transfer certificate back to the target theorem.",
        ),
        persist_condition="Persist only if the property names exactly which natural-proof premise fails and how usefulness survives.",
        pivot_condition="Pivot to barrier exposition or no-go if largeness, constructivity, and usefulness all remain present.",
        validation_handoff=("pvsnp-conceptual-pressure-localizer", "pvsnp-impossibility-theorem-forger", "prior-art-importer"),
        paper_safe_narrative=(
            "The bridge must show where naturalness is avoided, not merely assert that the route is non-natural."
        ),
    ),
    BridgeProfile(
        bridge_id="pvsnp-bridge-005",
        title="All-exponent quantifier-lift bridge",
        pressure_types=("hardness_magnification_ceiling", "padding_projection_debt", "advice_uniformity_leakage"),
        source_object="a family of source lower bounds indexed by target exponent or padding parameter",
        target_object="NP not subset P/poly, requiring exclusion of every fixed polynomial exponent",
        bridge_abstraction=(
            "Turn a bounded-window transfer into a cofinal family of source obligations, each indexed so that every target exponent c is eventually covered."
        ),
        difficulty_hypothesis=(
            "The route is hard because a single barely-superlinear lower bound generally excludes only a fixed exponent window; all-polynomial separation needs a quantifier-lift mechanism."
        ),
        controlled_interface="Index set, padding map, source lower-bound strength as a function of c, valid-length coverage, and uniformity of the family.",
        preserved_invariant="the universal quantifier over polynomial circuit exponents and the same nonuniform target class",
        proof_obligation=(
            "For every fixed c, construct a source instance with margin a_c and overhead q_c,beta_c satisfying a_c>q_c+beta_c c while preserving valid lengths and model identity."
        ),
        symbolic_probe="Use exact transfer audits across several symbolic c regimes and prove the parameter family is cofinal rather than finite.",
        falsifiers=(
            "The source obligation for exponent c is already equivalent to excluding SAT circuits of exponent c.",
            "Valid source lengths become sparse without a target-preserving coverage certificate.",
            "Uniformity or advice changes with c in a way that weakens the target theorem.",
        ),
        persist_condition="Persist if the next step states a parameterized theorem covering arbitrary c with explicit overhead functions.",
        pivot_condition="Quarantine if the family only repeats the same bounded window or if each indexed source lower bound carries the original target difficulty.",
        validation_handoff=("pvsnp-symbolic-complexity-auditor", "pvsnp-qualitative-complexity-reasoner", "next-experiment-queue-ranker"),
        paper_safe_narrative=(
            "A convincing magnification bridge must carry the all-exponent quantifier, not merely improve a fixed numerical threshold."
        ),
    ),
    BridgeProfile(
        bridge_id="pvsnp-bridge-006",
        title="Route-specific impossibility bridge",
        pressure_types=("black_box_substitution_cap", "padding_projection_debt", "relativization_algebrization_boundary"),
        source_object="a method class such as black-box SAT substitution, projection magnification, or relativizing counting diagonalization",
        target_object="a theorem explaining why that method class cannot imply P != NP or NP not subset P/poly under stated assumptions",
        bridge_abstraction=(
            "Treat persistent failure as a candidate obstruction theorem with precise hypotheses, excluded method class, escape conditions, and proof skeleton."
        ),
        difficulty_hypothesis=(
            "Some branches are hard because their method class structurally loses the target quantifier; in that case the bridge is a negative theorem, not another positive search loop."
        ),
        controlled_interface="Method-class axioms, exact target, transfer formula, barrier signature, and escape conditions not ruled out.",
        preserved_invariant="no-go conclusion is limited to the method class actually formalized",
        proof_obligation=(
            "State and prove that every method satisfying the method-class axioms yields only a bounded exponent window, a sparse-length proxy, or a relativizing/algebrizing result."
        ),
        symbolic_probe="Derive the contradiction or cap using exact transfer formulas and check nonvacuity by listing a covered example and an escape example.",
        falsifiers=(
            "The theorem rules out methods broader than its hypotheses justify.",
            "The obstruction is already a known barrier with no route-specific refinement.",
            "An escape condition covers the active branch, so the no-go does not apply.",
        ),
        persist_condition="Persist if the theorem statement has nonvacuous examples, exact assumptions, and a new route-specific consequence.",
        pivot_condition="Reject if it only paraphrases natural proofs, relativization, or algebrization without a new controlled interface.",
        validation_handoff=("pvsnp-impossibility-theorem-forger", "contradiction-route-auditor", "paper-contribution-readiness-judge"),
        paper_safe_narrative=(
            "A negative result can be a scientific contribution when it identifies the exact bridge condition under which a family of approaches loses the target."
        ),
    ),
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def collect_corpus() -> dict[str, str]:
    corpus: dict[str, str] = {
        "KB/p-vs-np.kb.md": read_text(KB),
        "agentic/reports/subworkflow_integration/latest.md": read_text(SUBWORKFLOW),
    }
    if CYCLES.exists():
        for path in sorted(CYCLES.glob("cycle-*.md")):
            corpus[str(path.relative_to(ROOT))] = read_text(path)
    return corpus


def term_counts(corpus: dict[str, str]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    evidence: dict[str, list[str]] = {key: [] for key in PRESSURE_TERMS}
    for rel_path, text in corpus.items():
        lower = text.lower()
        for pressure, terms in PRESSURE_TERMS.items():
            score = sum(lower.count(term) for term in terms)
            if score:
                counts[pressure] += score
                evidence[pressure].append(rel_path)
    return {"counts": dict(counts), "evidence": evidence}


def extract_cycle_evidence(corpus: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel_path, text in corpus.items():
        if "/cycles/" not in rel_path:
            continue
        cycle_id = Path(rel_path).stem
        headings = re.findall(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        gaps = re.findall(r"Blocking gap:\s*(.+)", text)
        experiments = re.findall(r"## Next Experiment\s*\n\n(.+?)(?=\n#|\n##|\Z)", text, flags=re.DOTALL)
        if headings or gaps or experiments:
            rows.append(
                {
                    "cycle_id": cycle_id,
                    "source": rel_path,
                    "branch_headlines": "; ".join(h.strip() for h in headings[:4]),
                    "blocking_gap": " ".join(g.strip() for g in gaps[:2]),
                    "next_experiment": " ".join(e.strip().replace("\n", " ") for e in experiments[:2]),
                }
            )
    return rows


def score_profile(profile: BridgeProfile, counts: dict[str, int]) -> int:
    return sum(counts.get(pressure, 0) for pressure in profile.pressure_types)


def build_candidates(corpus: dict[str, str]) -> dict[str, Any]:
    signals = term_counts(corpus)
    counts = {key: int(value) for key, value in signals["counts"].items()}
    cycle_evidence = extract_cycle_evidence(corpus)
    candidates = []
    for profile in PROFILES:
        score = score_profile(profile, counts)
        evidence_paths = sorted(
            {
                path
                for pressure in profile.pressure_types
                for path in signals["evidence"].get(pressure, [])
            }
        )
        candidates.append(
            {
                "id": profile.bridge_id,
                "title": profile.title,
                "priority_score": score,
                "pressure_types": list(profile.pressure_types),
                "evidence_paths": evidence_paths[:12],
                "difficulty_hypothesis": profile.difficulty_hypothesis,
                "bridge_abstraction": profile.bridge_abstraction,
                "source_object": profile.source_object,
                "target_object": profile.target_object,
                "controlled_interface": profile.controlled_interface,
                "preserved_invariant": profile.preserved_invariant,
                "proof_obligation": profile.proof_obligation,
                "symbolic_probe": profile.symbolic_probe,
                "falsifiers": list(profile.falsifiers),
                "when_to_persist": profile.persist_condition,
                "when_to_pivot": profile.pivot_condition,
                "validation_handoff": list(profile.validation_handoff),
                "paper_safe_narrative": profile.paper_safe_narrative,
                "status": "active_bridge_candidate" if score else "available_if_pressure_appears",
            }
        )
    candidates.sort(key=lambda row: (-int(row["priority_score"]), row["id"]))
    return {
        "version": 1,
        "target_id": "p-vs-np-target",
        "purpose": "Convert P vs NP conceptual pressures and difficulty hypotheses into target-preserving bridge abstractions.",
        "source_artifacts": sorted(corpus),
        "pressure_signal_counts": counts,
        "cycle_evidence": cycle_evidence,
        "bridge_candidates": candidates,
        "recommended_next_move": recommend(candidates),
        "non_claims": [
            "These bridge candidates do not prove P != NP.",
            "A pressure signal is not progress unless a bridge obligation is validated in the same target model.",
            "Negative no-go bridges are contribution candidates only after theorem-shaped formalization and nonvacuity checks.",
        ],
    }


def recommend(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    active = [row for row in candidates if int(row["priority_score"]) > 0]
    top = active[0] if active else candidates[0]
    return {
        "bridge_id": top["id"],
        "title": top["title"],
        "action": (
            "Run the symbolic or no-go handoff for this bridge before adding more exploratory cycles; "
            "the next cycle should compute an interface parameter, prove an obstruction theorem, or demote the bridge."
        ),
        "skills": top["validation_handoff"],
        "payoff_criterion": top["proof_obligation"],
        "stop_condition": top["when_to_pivot"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# P vs NP Pressure Bridge Abstractions",
        "",
        f"- Target: `{payload['target_id']}`",
        f"- Purpose: {payload['purpose']}",
        "",
        "## Pressure Signals",
        "",
    ]
    for key, count in sorted(payload["pressure_signal_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {count}")
    lines.extend(["", "## Recommended Next Move", ""])
    rec = payload["recommended_next_move"]
    lines.extend(
        [
            f"- Bridge: `{rec['bridge_id']}` {rec['title']}",
            f"- Action: {rec['action']}",
            f"- Payoff criterion: {rec['payoff_criterion']}",
            f"- Stop condition: {rec['stop_condition']}",
            f"- Skills: {', '.join(rec['skills'])}",
            "",
            "## Bridge Candidates",
            "",
        ]
    )
    for row in payload["bridge_candidates"]:
        lines.extend(
            [
                f"### {row['id']} - {row['title']}",
                "",
                f"- Priority score: `{row['priority_score']}`",
                f"- Pressures: {', '.join(f'`{p}`' for p in row['pressure_types'])}",
                f"- Difficulty hypothesis: {row['difficulty_hypothesis']}",
                f"- Bridge abstraction: {row['bridge_abstraction']}",
                f"- Source object: {row['source_object']}",
                f"- Target object: {row['target_object']}",
                f"- Controlled interface: {row['controlled_interface']}",
                f"- Proof obligation: {row['proof_obligation']}",
                f"- Symbolic probe: {row['symbolic_probe']}",
                f"- When to persist: {row['when_to_persist']}",
                f"- When to pivot: {row['when_to_pivot']}",
                f"- Paper-safe narrative: {row['paper_safe_narrative']}",
                "- Falsifiers:",
            ]
        )
        for falsifier in row["falsifiers"]:
            lines.append(f"  - {falsifier}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    parser.add_argument("--markdown", default=str(DEFAULT_MD))
    args = parser.parse_args()
    payload = build_candidates(collect_corpus())
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = Path(args.markdown)
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} and {md.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
