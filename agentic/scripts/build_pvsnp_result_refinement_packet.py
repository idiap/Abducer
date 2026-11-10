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
"""Build a P vs NP result-elaboration packet from the timeline paper draft."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json


PAPER_JSON = ROOT / "agentic/reports/timeline_paper/latest.json"
PAPER_PROJECT_ID = "p-vs-np-transfer-obstruction-certificate"
PAPER_PROJECT_MANIFEST = ROOT / "agentic/reports/paper_projects" / PAPER_PROJECT_ID / "latest.json"
MARATHON_RUN_DIR = ROOT / "agentic/runs/discovery_marathons/p-vs-np-marathon"
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/p-vs-np-transfer-obstruction-certificate"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"

SKILLS = [
    "results-theorem-scope-certifier",
    "results-finite-object-formalizer",
    "results-proof-packet-deriver",
    "results-prior-art-disqualifier-auditor",
    "results-paper-readiness-gatekeeper",
    "results-critical-self-refiner",
    "results-narrative-integrator",
]


def build_scope() -> dict[str, Any]:
    return {
        "scope_id": "pvsnp.scope.transfer-envelope-obstruction",
        "smallest_honest_claim": (
            "For a named P vs NP bridge route whose source carrier H_N is upper-bounded from SAT circuits by "
            "SIZE(H_N) <= N^{q+beta c+o(1)}, a barely-superlinear lower bound SIZE(H_N)>N^a rules out only target "
            "exponents c satisfying a>q+beta c. Therefore beta>0 gives a bounded-window obstruction, not an NP not subset P/poly result."
        ),
        "result_form": "scoped_no_go_or_transfer_gate",
        "covered_domain": [
            "bridge routes that explicitly name source carrier H_N, target SAT_m or NP-complete target, circuit model, length map, and transfer envelope",
            "nonuniform circuit-size consequences parameterized by a fixed target exponent c",
            "method-class diagnostics for hardness-magnification, meta-complexity, proof-object, or nonblackbox carriers when q and beta are computable",
        ],
        "excluded_domain": [
            "a proof of P != NP",
            "a proof that SAT is outside P/poly",
            "routes whose source lower bound is already equivalent to the target separation",
            "claims with hidden hard-row advice, unspecified circuit model, or unnamed target-preserving transfer",
        ],
        "conditional_extension_domain": [
            "all-exponent lift if beta=0 or beta=o(1) with positive margin and no advice leakage",
            "cofinal indexed carrier families a_c>q_c+beta_c c with uniform construction and target-relevant valid lengths",
            "searchable certificate bridges if existence, searchability, soundness, density, and advice-freeness are proved",
        ],
        "definitions_needed": ["H_N", "SAT_m", "a", "q", "beta", "circuit model", "length map", "advice ledger"],
        "hypotheses": [
            "SAT in SIZE(n^c) is interpreted in the same circuit model used to measure H_N.",
            "The transfer theorem constructs H_N circuits of size at most N^{q+beta c+o(1)} without uncounted advice.",
            "The lower bound SIZE(H_N)>N^a holds on the same source lengths and in the same model.",
        ],
        "non_claims": ["does not prove P != NP", "does not prove SAT notin P/poly", "does not settle unrestricted lower bounds"],
        "promotion_boundary": "Promote only as a scoped transfer/no-go note until a named carrier proof and prior-art boundary are complete.",
        "epistemic_status": "conditional_scoped_no_go_packet",
    }


def build_finite_object() -> dict[str, Any]:
    return {
        "object_id": "pvsnp.object.transfer-envelope",
        "name": "target-preserving transfer envelope",
        "notation_table": {
            "H_N": "source carrier language, truth-table family, meta-complexity predicate, or proof-mediated object",
            "SAT_m": "target SAT slice at input length m",
            "a": "claimed source lower-bound exponent",
            "q": "source-side overhead exponent independent of target exponent c",
            "beta": "target-query-length or target-circuit-use exponent multiplying c",
            "A": "advice, row-selection, or nonuniform leakage ledger",
        },
        "ambient_universe": "families of Boolean functions/languages with explicit length maps and circuit-size measures",
        "validity_regime": "fixed circuit model, explicit uniformity/advice convention, target-relevant lengths, no hidden hard-row selection",
        "worked_example": {
            "name": "projection carrier with polynomial embedding length",
            "inclusion": "ell(N)=N^{alpha+o(1)} yields SIZE(H_N)<=O(N log N)+ell(N)^c and excludes only alpha c<1+epsilon",
            "lesson": "positive alpha is beta-like exponent debt; the route demagnifies into a bounded target-exponent window",
        },
        "non_example": {
            "name": "unnamed hard row",
            "reason": "selecting a hard truth-table row without searchable/advice-free construction moves the target lower bound into advice",
        },
        "proof_use_contract": [
            "bounded-window lemma uses a,q,beta to derive the exact contradiction threshold",
            "all-exponent gate uses beta and parameter family discipline to decide whether P/poly-level promotion is even possible",
            "certificate gate uses A and search exponent to expose naturalness or advice leakage",
        ],
        "falsifier": "If beta>0 and a is fixed, large c survives; if q>=a, no target exponent is ruled out.",
        "epistemic_status": "definition_ready_example_tested",
    }


def build_proof_packet() -> dict[str, Any]:
    return {
        "theorem_id": "pvsnp.thm.bounded-window-transfer-obstruction",
        "proof_status": "conditional_theorem",
        "theorem_statement": (
            "Assume a route-specific transfer theorem: SAT in SIZE(n^c) implies SIZE(H_N)<=N^{q+beta c+o(1)} "
            "in the same model and without uncounted advice. If also SIZE(H_N)>N^a infinitely often or eventually "
            "on the same valid lengths, then the route contradicts SAT in SIZE(n^c) only when a>q+beta c."
        ),
        "definitions_used": ["H_N", "SAT_m", "a", "q", "beta", "length map", "circuit model"],
        "hypotheses_used": [
            "same-model transfer theorem",
            "source lower bound in matching model and length regime",
            "no uncounted nonuniform advice or hard-row selector",
        ],
        "proof_steps": [
            "Assume SAT has circuits of size n^c in the stated model.",
            "Apply the transfer theorem to obtain H_N circuits of size N^{q+beta c+o(1)}.",
            "Compare this upper bound with the source lower bound N^a.",
            "A contradiction is obtained exactly when q+beta c<a after absorbing o(1).",
            "If beta>0 and a,q are fixed, sufficiently large c violates the inequality, so the route cannot establish all-exponent P/poly exclusion.",
        ],
        "equations": [
            r"\mathrm{SAT}\in\mathrm{SIZE}(n^c)\Rightarrow \mathrm{SIZE}(H_N)\le N^{q+\beta c+o(1)}",
            r"\mathrm{SIZE}(H_N)>N^a\quad\Longrightarrow\quad a>q+\beta c",
            r"\forall c\; a_c>q_c+\beta_c c\quad\text{is required for an all-exponent lift}",
        ],
        "blocked_step_or_countermodel": (
            "A paper-level positive bridge still needs one named carrier or proof system with computed q,beta, advice cost, and certificate-search exponent. "
            "Without that, the current result is a scoped obstruction framework rather than a new unconditional lower bound."
        ),
        "manuscript_theorem_text": (
            "The transfer-envelope lemma should be stated in the formal core as a conditional theorem and used to classify branch outcomes: "
            "bounded-window obstruction, all-exponent candidate, or demoted proxy route."
        ),
        "limitations_paragraph": (
            "The lemma is elementary once the transfer envelope is known. The scientific value lies in forcing each route to expose q, beta, "
            "advice leakage, and barrier status before any P vs NP implication is advertised."
        ),
        "validation_handoff": "Run the P vs NP inference-quality validator and a prior-art/disqualifier audit before novelty language.",
    }


def build_prior_art() -> dict[str, Any]:
    return {
        "claimability_decision": "claimable_after_repair",
        "prior_art_table": [
            {
                "area": "hardness magnification",
                "shared_hypothesis": "weak source lower bounds are transferred to stronger target consequences",
                "boundary": "this packet claims only an exact transfer-envelope gate unless a named magnification theorem is instantiated",
            },
            {
                "area": "MCSP/MKtP and meta-complexity",
                "shared_hypothesis": "source carriers can encode lower-bound evidence",
                "boundary": "certificate existence, searchability, soundness, density, and advice-freeness remain open gates",
            },
            {
                "area": "natural proofs / relativization / algebrization",
                "shared_hypothesis": "broad method classes may be disqualified",
                "boundary": "barrier status must be attached to the exact theorem, not cited as a slogan",
            },
        ],
        "disqualifier_matrix": [
            {"gate": "target-equivalent source lower bound", "status": "open_gate", "repair": "prove source lower bound is genuinely weaker or state scoped no-go"},
            {"gate": "hidden advice or hard-row leakage", "status": "open_gate", "repair": "add advice ledger and searchable row/certificate discipline"},
            {"gate": "positive beta bounded-window collapse", "status": "active_falsifier", "repair": "find beta=0, beta=o(1), cofinal family, or demote route"},
            {"gate": "known/subsumed theorem", "status": "prior_art_needed", "repair": "compare exact statement against hardness magnification and meta-complexity literature"},
        ],
        "novelty_boundary": "The claimable contribution is a disciplined route-classification theorem packet, not a new separation.",
        "overclaim_boundary": "Do not say the method advances P != NP unless the all-exponent lift or named carrier proof is discharged.",
        "repair_tasks": [
            "Instantiate one named carrier/proof system and compute q,beta,A.",
            "Write a prior-art paragraph comparing the transfer-envelope gate to known magnification frameworks.",
            "Run inference-quality review for model preservation, advice discipline, and quantifier regime.",
        ],
    }


def build_readiness() -> dict[str, Any]:
    return {
        "readiness_decision": "paper_scaffold_ready_for_theorem_consolidation",
        "gate_table": {
            "claim_statement_ready": True,
            "definitions_ready": True,
            "proof_packet_ready": True,
            "prior_art_boundary_ready": False,
            "disqualifiers_closed": False,
            "overclaim_boundary_ready": True,
            "manuscript_insertion_ready": True,
        },
        "missing_blockers": [
            "unify the selector zoo under one TransparentRowSupport_N definition rather than accumulating more cases",
            "write the positive theorem and private-row countermodel theorem as the main paper pair",
            "complete nearest-work comparison before strong novelty language",
            "prove or demote RealSATInfluenceRealizer_N as an explicit open problem rather than leaving it as semantic fog",
        ],
        "permitted_paper_claim": (
            "A scoped parser/falsifier obstruction note: transparent FormulaEval row support has an exact Gamma charge, "
            "while hidden semantic FormulaEval support is blocked by a private-row countermodel."
        ),
        "forbidden_language": [
            "proof of P != NP",
            "SAT outside P/poly",
            "barrier escaped",
            "new lower bound without a named carrier proof",
        ],
        "insertion_plan": {
            "abstract": "state scoped route-classification contribution and non-claim boundary",
            "formal_core": "state bounded-window theorem, all-exponent gate, and certificate gate",
            "worked_section": "use projection/MCSP examples as transfer-envelope calculations",
            "discussion": "present prior-art repairs and disqualifier gates as next paper tasks",
        },
        "next_action": "Write the TransparentRowSupport_N theorem/countermodel pair as the paper core before running more exploratory cycles.",
    }


def build_transparent_row_support_packet() -> dict[str, Any]:
    return {
        "object_id": "pvsnp.object.transparent-row-support",
        "name": "TransparentRowSupport_N",
        "status": "consolidation_target",
        "smallest_honest_claim": (
            "The recent FormulaEval selector cases should be collapsed into one abstraction: a FormulaEval mechanism is "
            "target-preserving exactly when the selected row support is proof-visible, advice-free, influence-closed, "
            "enumerable or explicitly scan-charged, and row-expanded inside the same Gamma ledger."
        ),
        "definition_fields": {
            "visible_selector_code": "the proof displays the row predicate, extension rule, or enumerator certificate used to select rows",
            "row_enumeration_or_scan_charge": "either RowSetEnumerator_N outputs selected rows with certified cost U_N or the parser pays the full scan charge F_FE N^{1+q+o(1)}",
            "influence_closure": "every row whose SAT value can change a FormulaEval line is included in the charged support",
            "row_expansion_charge": "each distinct selected row contributes the complete occurrence/SAT expansion term, typically N times the row count or T_N M_N in projected formulations",
            "same_theory_parser": "all support, selector, extension, and SAT occurrence conventions are read by the same proof verifier and circuit model",
            "no_hidden_advice": "row support cannot be supplied by nonuniform tables, semantic oracles, or private enable bits unless charged",
        },
        "generic_positive_theorem": {
            "theorem_id": "pvsnp.thm.transparent-row-support-gamma-falsifier",
            "statement": (
                "If a Psys_sym FormulaEval mechanism satisfies TransparentRowSupport_N with discovery charge U_N, "
                "row-support size T_N, and FormulaEval expansion charge X_N, then the existing bEF parser extends to "
                "Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N. If N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, "
                "the alleged LB_N(1+epsilon) certificate is falsified in the same nonuniform SIZE model."
            ),
            "proof_spine": [
                "Parse all bEF, SATeq, bounded-SR_h, and extension dependencies into Gamma_bEF.",
                "Use visible selector or enumerator fields to compute the complete FormulaEval row support or pay full scan.",
                "Apply influence closure so every SAT row that can alter a FormulaEval line enters the charged support.",
                "Expand each charged row into the same occurrence/SAT representation used by the carrier H_N^SAT.",
                "Compose the public generator, parsed transcript, and residual patches into a nonuniform circuit for H_N^SAT.",
                "Contradict LB_N(1+epsilon) exactly when the total size is subthreshold.",
            ],
            "examples_subsumed": [
                "interval-union FormulaEval",
                "proof-visible selector scan",
                "ROBDD selector",
                "guarded deterministic decomposable NNF selector",
                "projected guarded-dDNNF with witness or projected-enumerator charge",
            ],
        },
        "generic_countermodel_theorem": {
            "theorem_id": "pvsnp.thm.hidden-formulaeval-private-row-countermodel",
            "statement": (
                "If a FormulaEval mechanism lacks visible row support, selector extensionality, influence closure, or a charged "
                "semantic-realizer, then a private-row or unread-enable-bit construction gives two proof surfaces with the same "
                "parsed transcript but different FormulaEval dependence or carrier parity. Occurrence completion is therefore invalid."
            ),
            "countermodel_spine": [
                "Choose a row r* not present in the parsed support Q_pi.",
                "Let a hidden enable bit or semantic selector decide whether r* participates in FormulaEval.",
                "Keep all displayed proof bits and charged occurrence neighborhoods fixed.",
                "Flip the uncharged SAT/FormulaEval value at r*.",
                "The parser outputs the same transcript while the selected support or H_N^SAT parity changes.",
            ],
            "blocked_escape": "RealSATInfluenceRealizer_N remains the only possible escape: it must force every semantically influential row into visible, charged support.",
        },
        "stop_rule": (
            "Do not add more selector classes unless they either instantiate TransparentRowSupport_N as a nontrivial example "
            "needed by the paper or disprove one of its definition fields. The next cycle must draft/prove the generic theorem pair."
        ),
        "paper_core_sections": [
            "Definition: TransparentRowSupport_N",
            "Theorem: Transparent FormulaEval mechanisms extend Gamma and yield the parser-to-circuit falsifier",
            "Countermodel: hidden semantic FormulaEval fails by private-row/unread-enable-bit spoofing",
            "Examples: interval unions, scans, ROBDD, guarded dDNNF, projected selectors",
            "Open problem: RealSATInfluenceRealizer_N and prior-art boundary",
        ],
        "evidence_cycles": ["cycle-0103", "cycle-0104", "cycle-0105", "cycle-0106", "cycle-0107"],
        "epistemic_status": "near_certified_note_core_pending_formal_writeup",
    }


def build_report() -> dict[str, Any]:
    paper = load_json_object(PAPER_JSON)
    source_artifacts = [
        rel(PAPER_JSON),
        paper.get("artifacts", {}).get("tex", ""),
        paper.get("artifacts", {}).get("pdf", ""),
    ]
    for cycle_id in range(103, 108):
        cycle_path = MARATHON_RUN_DIR / "cycles" / f"cycle-{cycle_id:04d}.json"
        if cycle_path.exists():
            source_artifacts.append(rel(cycle_path))
    if PAPER_PROJECT_MANIFEST.exists():
        source_artifacts.insert(0, rel(PAPER_PROJECT_MANIFEST))
    report = {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": "p-vs-np-target",
        "paper_project_id": PAPER_PROJECT_ID,
        "paper_project_manifest": rel(PAPER_PROJECT_MANIFEST) if PAPER_PROJECT_MANIFEST.exists() else "",
        "packet_id": stable_id("pvsnp-result-refinement", paper.get("paper_id", ""), paper.get("generated_utc", "")),
        "status": "pvsnp_result_refinement_ready",
        "source_artifacts": source_artifacts,
        "invoked_skills": SKILLS,
        "draft_artifacts": paper.get("artifacts", {}),
        "theorem_scope": build_scope(),
        "finite_object": build_finite_object(),
        "proof_packet": build_proof_packet(),
        "transparent_row_support_packet": build_transparent_row_support_packet(),
        "prior_art_disqualifier_audit": build_prior_art(),
        "readiness_gate": build_readiness(),
        "critical_self_refinement": {
            "deterministic_checks": ["TeX/PDF compilation", "target-leak scan", "P vs NP paper validator", "LaTeX section validator"],
            "generative_work": ["carrier instantiation", "certificate soundness proof", "prior-art positioning paragraph"],
            "rejected_generic_moves": ["repeat hardness magnification promise", "add more timeline chronology", "claim barrier escape without theorem-specific status"],
            "next_executable_validation": "python agentic/scripts/validate_pvsnp_result_refinement_packet.py",
        },
        "narrative_integration": {
            "narrative_spine": [
                "P vs NP creates all-exponent lower-bound pressure.",
                "Bridge routes are meaningful only through target-preserving transfer envelopes.",
                "Positive beta explains exponent demagnification; hidden FormulaEval support explains semantic proof-system leakage.",
                "The new paper core is the TransparentRowSupport_N theorem/countermodel pair.",
                "The paper remains a scoped parser/falsifier obstruction note until prior-art and RealSATInfluenceRealizer_N gates close.",
            ],
            "paper_update_plan": [
                "Promote TransparentRowSupport_N from cycle evidence into a formal definition.",
                "Write the Gamma extension theorem and private-row countermodel theorem as the main result pair.",
                "Move selector cases into examples, not new main claims.",
                "Add a prior-art paragraph around hardness magnification, MCSP/MKtP, natural proofs, relativization, and algebrization.",
                "Close with RealSATInfluenceRealizer_N and AC0 output-sensitive enumeration as exact open problems.",
            ],
        },
        "epistemic_status": "paper_scaffold_ready_for_theorem_consolidation",
    }
    return report


def render_markdown(report: dict[str, Any]) -> str:
    scope = report["theorem_scope"]
    readiness = report["readiness_gate"]
    transparent = report["transparent_row_support_packet"]
    lines = [
        "# P vs NP Result Refinement Packet",
        "",
        f"- Status: `{report['status']}`",
        f"- Target: `{report['target_id']}`",
        f"- Paper project: `{report['paper_project_id']}`",
        f"- Epistemic status: `{report['epistemic_status']}`",
        "",
        "## Smallest Honest Claim",
        "",
        scope["smallest_honest_claim"],
        "",
        "## Current Consolidation Target",
        "",
        f"- Object: `{transparent['name']}`",
        f"- Status: `{transparent['status']}`",
        f"- Claim: {transparent['smallest_honest_claim']}",
        "",
        "### Theorem Pair",
        "",
        f"- Positive theorem: {transparent['generic_positive_theorem']['statement']}",
        f"- Countermodel theorem: {transparent['generic_countermodel_theorem']['statement']}",
        "",
        "### Stop Rule",
        "",
        transparent["stop_rule"],
        "",
        "## Readiness",
        "",
        f"- Decision: `{readiness['readiness_decision']}`",
        f"- Permitted claim: {readiness['permitted_paper_claim']}",
        "",
        "## Missing Blockers",
        "",
        *[f"- {item}" for item in readiness["missing_blockers"]],
        "",
        "## Next Paper Actions",
        "",
        *[f"- {item}" for item in report["narrative_integration"]["paper_update_plan"]],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
