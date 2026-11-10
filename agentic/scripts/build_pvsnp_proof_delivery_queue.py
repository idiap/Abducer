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
"""Build the highest-priority P vs NP proof-delivery queue."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, utc_now, write_json


TARGET_ID = "p-vs-np-target"
OUT_DIR = ROOT / "agentic/reports/pvsnp_proof_delivery_queue"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
STRATEGY_JUDGE = ROOT / "agentic/reports/strategy_progression_judge/latest.json"
PAPER_PROJECT = ROOT / "agentic/reports/paper_projects/p-vs-np-transfer-obstruction-certificate/latest.json"
INFERENCE_QUALITY = ROOT / "agentic/reports/pvsnp_inference_quality/latest.json"
SOURCE_DRAFT_PATH = "agentic/imports/pvsnp/source_documents/parity_magnification_full_row_barrier (1).tex"

PROOF_DELIVERY_SKILLS = [
    "proof-delivery-workflow-orchestrator",
    "proof-obligation-formalizer",
    "lemma-chain-proof-builder",
    "proof-gap-countermodel-splitter",
    "proof-quality-gatekeeper",
]

PVSNP_REVIEW_SKILLS = [
    "pvsnp-forcedrows-proof-workflow",
    "pvsnp-inference-quality-controller",
    "pvsnp-reduction-consistency-reviewer",
    "pvsnp-quantifier-uniformity-reviewer",
    "pvsnp-barrier-specificity-reviewer",
    "pvsnp-proof-complexity-transfer-reviewer",
]

PVSNP_DISCOVERY_SKILLS = [
    "pvsnp-conceptual-pressure-localizer",
    "pvsnp-pressure-bridge-forger",
    "pvsnp-qualitative-complexity-reasoner",
    "pvsnp-symbolic-complexity-auditor",
    "pvsnp-proof-derivation-builder",
    "pvsnp-impossibility-theorem-forger",
    "pvsnp-negative-tactic-selector",
]

EXTRACTED_PROOF_ASSETS = [
    {
        "anchor": (
            "Draft sections 2-3; Proposition 'Exponent-window lemma', Lemma 'Batched substitution', "
            "Theorem 'Beta-zero parity transfer', Corollary 'Conditional magnification'"
        ),
        "proof_status": "proved_in_draft_needs_formal_audit",
        "contribution": (
            "Separates positive target-query exponent debt from the beta-zero all-polynomial-exponent "
            "transfer needed for SAT not in P/poly."
        ),
    },
    {
        "anchor": "Draft section 4; Lemma 'Equality patching' and Corollary 'Residual threshold'",
        "proof_status": "proved_in_draft_needs_formal_audit",
        "contribution": (
            "Turns sparse exceptional rows into cheap equality patches, giving the residual robustness "
            "threshold for any source lower bound."
        ),
    },
    {
        "anchor": (
            "Draft section 5; Theorem 'Naturalization of functional certificates' and Corollary "
            "'Conditional natural-proofs obstruction'"
        ),
        "proof_status": "proved_in_draft_needs_barrier_scope_audit",
        "contribution": (
            "Shows dense truth-table-constructive functional certificates become natural properties in "
            "the matched-length regime."
        ),
    },
    {
        "anchor": (
            "Draft section 6; Theorem 'Row-forcing theorem', Corollary 'Full-row barrier for parity', "
            "Corollary 'Oracle-query lower bound'"
        ),
        "proof_status": "proved_in_draft_needs_parser_boundary",
        "contribution": (
            "Classifies occurrence-relativizing certificates by forcing complete parity rows and paying "
            "Omega(M_n s_n/n) occurrence access."
        ),
    },
    {
        "anchor": (
            "Draft section 8 and appendix; Proposition 'Parser-to-query consequence', Proposition "
            "'Approximate affine-incidence sketch', Proposition 'One-sided forcing'"
        ),
        "proof_status": "proved_in_draft_or_conditional_needs_handoff",
        "contribution": (
            "Supplies proof-system, diagnostic upper-bound, and one-sided variants that can become "
            "paper modules once assumptions are explicit."
        ),
    },
]

EXTRACTED_OPEN_DIRECTIONS = [
    {
        "anchor": "Draft section 7; Open Problem 'Formula-semantic extraction'",
        "problem": (
            "For a concrete strong proof system formalizing lower bounds for H_n^SAT, prove functional "
            "extraction, occurrence-relativizing transcript extraction, or a precise nonrelativizing "
            "SAT-semantic obstruction."
        ),
    },
    {
        "anchor": "Draft discussion; paragraph 'An explicit hard generator'",
        "problem": (
            "Construct a label-independent batched generator with q,rho < 1+epsilon and prove the SAT "
            "parity carrier lower bound above n^{1+epsilon}."
        ),
    },
    {
        "anchor": "Draft discussion; paragraph 'A strong-system instantiation'",
        "problem": (
            "Choose a concrete proof formalism, specify accessible SAT facts, and decide whether short "
            "proofs admit the parser-to-query property."
        ),
    },
    {
        "anchor": "Draft discussion; paragraph 'Aggregator design'",
        "problem": (
            "Find aggregators with a better tradeoff between beta-zero transfer cost, certificate "
            "complexity, proof locality, and algebraic structure."
        ),
    },
    {
        "anchor": "Draft discussion plus appendix 'Incidence sketches as upper-bound falsifiers'",
        "problem": (
            "Turn low-rank or sparse incidence diagnostics into either explicit falsifiers or a "
            "nonrelativizing normal-form theorem strong enough to support lower bounds."
        ),
    },
]


def common_fields() -> dict[str, Any]:
    strategy = load_optional_json(STRATEGY_JUDGE)
    paper = load_optional_json(PAPER_PROJECT)
    iq = load_optional_json(INFERENCE_QUALITY)
    return {
        "target_id": TARGET_ID,
        "paper_project_id": clean_text(paper.get("paper_project_id")) or "p-vs-np-transfer-obstruction-certificate",
        "source_strategy_judge": rel(STRATEGY_JUDGE),
        "source_paper_project": rel(PAPER_PROJECT),
        "source_inference_quality": rel(INFERENCE_QUALITY),
        "source_parity_magnification_draft": SOURCE_DRAFT_PATH,
        "strategy_decision": clean_text(strategy.get("decision")) or clean_text(strategy.get("progression_judgement", {}).get("decision")),
        "current_iq_status": clean_text(iq.get("summary", {}).get("quality_gate_status")),
    }


def item(
    *,
    queue_id: str,
    rank: int,
    title: str,
    next_analysis: str,
    theorem_goal: str,
    source_object: str,
    target_object: str,
    proof_outputs: list[str],
    proof_steps: list[str],
    success_criteria: list[str],
    demotion_criteria: list[str],
    required_skills: list[str],
    paper_handoff: str,
    source_anchor: str,
    proof_status: str,
) -> dict[str, Any]:
    return {
        "queue_id": queue_id,
        "rank": rank,
        "queue_source": "proof_delivery_priority",
        "priority_score": 10000 - rank,
        "priority_band": "proof-delivery-highest",
        "branch_control": "run_before_broad_exploration",
        "title": title,
        "next_experiment": next_analysis,
        "next_analysis": next_analysis,
        "theorem_goal": theorem_goal,
        "source_object": source_object,
        "source_anchor": source_anchor,
        "proof_status": proof_status,
        "target_object": target_object,
        "transfer_condition": (
            "The output must preserve the P vs NP target relation while remaining a scoped route-specific "
            "theorem, proof audit, or blocked extraction obligation, not a claim of P != NP."
        ),
        "proof_outputs": proof_outputs,
        "validation_steps": proof_steps,
        "success_criteria": success_criteria,
        "demotion_criteria": demotion_criteria,
        "stop_criteria": demotion_criteria,
        "do_not_stop_if": [
            "A named lemma can still be proved, repaired, or refuted locally.",
            "The current run can emit a live pvsnp_inference_quality packet.",
            "A countermodel would become a route-specific no-go theorem rather than mere failure.",
        ],
        "required_skills": sorted(set(required_skills)),
        "paper_handoff": paper_handoff,
        "validation_handoff": [
            "agentic/scripts/validate_pvsnp_proof_delivery_queue.py",
            "agentic/scripts/validate_pvsnp_inference_quality.py",
            "agentic/scripts/validate_pvsnp_result_refinement_packet.py",
        ],
    }


def build_items() -> list[dict[str, Any]]:
    all_main_skills = PROOF_DELIVERY_SKILLS + PVSNP_REVIEW_SKILLS + PVSNP_DISCOVERY_SKILLS
    return [
        item(
            queue_id="pvsnp.paper.bit-explicit-parser-formulaeval-boundary",
            rank=1,
            title="Prove the TransparentRowSupport_N theorem pair and stop selector-case accumulation",
            next_analysis=(
                "Proof-delivery task sharpened from cycles 103-107: stop adding isolated selector classes and consolidate "
                "interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete FormulaEval cases "
                "under one TransparentRowSupport_N abstraction. Prove the positive Gamma-extension theorem for transparent "
                "row support, prove the private-row/unread-enable-bit countermodel theorem for hidden semantic support, "
                "and state RealSATInfluenceRealizer_N as the exact remaining escape rather than a vague semantic gap."
            ),
            theorem_goal=(
                "TransparentRowSupport_N theorem pair: if a Psys_sym FormulaEval mechanism has visible selector code, "
                "advice-free enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and "
                "no hidden support advice, then Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N gives the parser-to-circuit falsifier "
                "N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} for LB_N(1+epsilon). If any visibility, extensionality, "
                "or influence-closure condition fails, construct the private-row/unread-enable-bit countermodel to surface "
                "occurrence completion."
            ),
            source_object=(
                "Cycles 103-107 FormulaEval selector packets over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with "
                "M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, polylog formula length, bit-explicit Psys_bEF "
                "parser costs, and selector cases including interval unions, full scans, ROBDD, guarded dDNNF, "
                "projected dDNNF, and influence-complete extension rules."
            ),
            target_object=(
                "A paper-core theorem/countermodel pair replacing the selector zoo: one transparent-support theorem, "
                "one hidden-support countermodel theorem, examples as corollaries, and RealSATInfluenceRealizer_N as an open problem."
            ),
            proof_outputs=[
                "formal definition of TransparentRowSupport_N with visible selector code, row enumeration/full scan, influence closure, row expansion, same-theory parser, and no-hidden-advice clauses",
                "positive theorem deriving Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N and the subthreshold parser-to-circuit falsifier",
                "countermodel theorem using a private row or unread enable bit when support visibility, selector extensionality, or influence closure fails",
                "corollary table showing interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete extension rules as examples, not new main routes",
                "explicit open-problem statement for RealSATInfluenceRealizer_N and AC0 output-sensitive enumeration",
                "support-density q-trichotomy lemma for |K_idx(pi)|/M_N >= N^{epsilon-q-o(1)} as a corollary of the Gamma theorem",
                "live pvsnp_inference_quality packet",
                "paper-ready theorem/countermodel text with non-claims and no generic barrier restatement",
            ],
            proof_steps=[
                "Proof step: define TransparentRowSupport_N as a reusable finite proof-system interface over Psys_sym FormulaEval lines.",
                "Proof step: prove that every transparent FormulaEval line contributes either a certified enumerator charge U_N or a full-scan charge F_FE N^{1+q+o(1)}, plus the row-expansion charge X_N.",
                "Proof step: extend the existing bit-explicit Psys_bEF line induction to Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N.",
                "Proof step: derive the upper-bound falsifier N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon) in the same nonuniform SIZE model.",
                "Proof step: prove the hidden-support countermodel: if a FormulaEval row can influence the proof without being visible and charged, two transcripts agree while the selected support or carrier parity differs.",
                "Proof step: demote additional selector classes to examples unless they prove or refute a TransparentRowSupport_N clause.",
                "Proof step: run proof-quality, barrier-specificity, quantifier-uniformity, proof-complexity-transfer, and inference-quality reviewers before promotion.",
            ],
            success_criteria=[
                "TransparentRowSupport_N is formal enough that an independent reader can decide whether a FormulaEval rule satisfies it.",
                "Gamma_trans(pi) is derived rather than asserted, and the falsifier inequality states rho, q, epsilon, U_N, X_N, eta, tau, E_N, and all o(1) regimes.",
                "The private-row/unread-enable-bit countermodel is stated as a theorem with hypotheses, not as a metaphor.",
                "Selector cases are reorganized into examples/corollaries; no new selector family is promoted as a separate main contribution.",
                "The output advances a paper-level subgoal: a clean theorem pair and open-problem boundary, not another restatement of the obstruction ladder.",
            ],
            demotion_criteria=[
                "Demote if the work adds another selector class without changing the TransparentRowSupport_N definition, theorem, or countermodel.",
                "Demote if Gamma_trans(pi), K_idx(pi), U_N, X_N, or the transcript upper bound is named without a derivation.",
                "Demote if semantic FormulaEval is described as generic power rather than handled by RealSATInfluenceRealizer_N or the private-row countermodel.",
                "Demote if the branch broadens into MCSP/MKtP, natural-proofs folklore, or generic barriers before the theorem pair is written.",
            ],
            required_skills=all_main_skills,
            paper_handoff="Make this the next paper-critical theorem/countermodel target: if it only adds selector examples, it is looping; if it proves TransparentRowSupport_N or the hidden-support countermodel, it moves toward a claimable scoped note.",
            source_anchor="Cycles 103-107 plus result-refinement packet transparent_row_support_packet.",
            proof_status="cycle_0107_consolidation_next_move",
        ),
        item(
            queue_id="pvsnp.paper.l1201-least-closed-support-proof-audit",
            rank=2,
            title="Write the L120.1 least-closed support proof-audit packet",
            next_analysis=(
                "Turn cycle 120's least prefix-closed reachable FormulaEval support cone into a referee-checkable proof packet. "
                "The task is to define the fixed-point computation of K_dag(pi), give verifier-visible dependency-closure "
                "pseudocode, prove the Gamma_dag line-induction invariant, and test the theorem on one projected-dDNNF "
                "FormulaEval example plus one unread-enable-bit counterexample."
            ),
            theorem_goal=(
                "LeastClosedTransparentSupport_N / L120.1: for a Psys_sym^dag proof pi whose FormulaEval lines expose "
                "parent pointers and support certificates, the least prefix-closed reachable cone K_dag(pi) from the final "
                "LB_N line is the minimal charged object needed for the parser-to-circuit falsifier "
                "N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}."
            ),
            source_object=(
                "Cycle 120 theorem claims over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), Psys_sym^dag FormulaEval lines, "
                "dependency edges from later symbolic uses to earlier row supports, and the cost ledger "
                "Gamma_dag(pi)=Gamma_bEF(pi)+U(K_dag(pi))+X(K_dag(pi))."
            ),
            target_object=(
                "A self-contained proof-audit packet that an independent reader can run mentally or mechanically: input pi,N; "
                "compute K_dag(pi); either certify prefix-closed support and Gamma_dag, or return the first hidden reachable row "
                "with its private-row/unread-enable-bit countermodel."
            ),
            proof_outputs=[
                "formal definition of the dependency graph, reachable final cone, and least fixed point K_dag(pi)",
                "pseudocode for the verifier-visible closure computation with termination and monotonicity proof",
                "proof of Gamma_dag(pi)=Gamma_bEF(pi)+U(K_dag(pi))+X(K_dag(pi)) by prefix line induction",
                "same-model upper-bound falsifier inequality including rho, epsilon, q, E_pi, and all o(1) regimes",
                "worked projected-dDNNF FormulaEval example showing how K_dag, U, X, and Gamma_dag are computed",
                "worked unread-enable-bit counterexample returning the first hidden reachable row",
                "live pvsnp_inference_quality packet for L120.1",
            ],
            proof_steps=[
                "Proof step: define the line-dependency DAG, support-token universe, and ancestor relation from the final LB_N line.",
                "Proof step: prove the least fixed point K_dag(pi) exists, is unique, and is computable from proof syntax and N without advice.",
                "Proof step: prove unreachable FormulaEval rows can be deleted without changing the retained line induction.",
                "Proof step: prove each retained FormulaEval support either pays U(K)+X(K) or triggers the first-hidden-row falsifier.",
                "Proof step: instantiate the positive and negative examples and attach an inference-quality packet before promotion.",
            ],
            success_criteria=[
                "The fixed-point algorithm for K_dag(pi) is explicit enough to implement or audit line by line.",
                "Gamma_dag is derived from the closure invariant, not asserted by analogy with Gamma_trans.",
                "The projected-dDNNF example and unread-enable-bit counterexample both exercise the theorem boundary.",
                "The result states that it is a scoped parser/falsifier theorem and not evidence for P != NP.",
            ],
            demotion_criteria=[
                "Demote if K_dag(pi) is described informally without a computable closure algorithm.",
                "Demote if the proof does not distinguish reachable support from the full selector zoo.",
                "Demote if the examples do not compute charges or do not expose a first hidden reachable row.",
                "Demote if the theorem silently assumes full semantic SAT influence instead of charging it.",
            ],
            required_skills=all_main_skills,
            paper_handoff="Use as the immediate proof-audit packet for cycle 120 and as the concrete next theorem module before any new marathon exploration.",
            source_anchor="Cycle 120; discovery marathon latest report lines for L120.1, K_dag(pi), Gamma_dag, projected-dDNNF, and unread-enable-bit counterexample.",
            proof_status="cycle_0120_next_missing_proof_audit",
        ),
        item(
            queue_id="pvsnp.paper.realsat-influence-realizer-boundary",
            rank=3,
            title="Resolve or quarantine RealSATInfluenceRealizer_N for one concrete semantic FormulaEval rule",
            next_analysis=(
                "Attack the exact remaining full-semantic FormulaEval gap instead of naming it abstractly. Choose one concrete "
                "semantic FormulaEval rule, such as Tseitin-extension equality plus bounded self-reduction, and either produce "
                "an advice-free nonrelativizing realizer listing all influencing rows with charges, or prove a rule-specific "
                "private-row/no-realizer countermodel."
            ),
            theorem_goal=(
                "RealSATInfluenceRealizer_N boundary theorem: full semantic FormulaEval can be folded into the transparent "
                "support theorem only when proof syntax and N uniformly determine an influence-closed row set R_A, same-theory "
                "row expansions, and a charged overhead R_N before the semantic rule is used."
            ),
            source_object=(
                "Semantic FormulaEval-SAT rules over H_N^SAT generated rows where real SAT semantics, formula equality, "
                "Tseitin extensions, or self-reduction may make a proof line depend on rows not visible in a syntactic "
                "TransparentRowSupport_N certificate."
            ),
            target_object=(
                "A yes/no boundary for one named semantic rule: either a valid RealSATInfluenceRealizer_N certificate with "
                "Gamma_real=Gamma_bEF+U+X+R_N, or a finite countermodel showing why that semantic rule remains quarantined."
            ),
            proof_outputs=[
                "selected semantic FormulaEval rule with exact bit fields, formula objects, and allowed SAT/equality facts",
                "definition of semantic influence Infl(A), row set R_A, realizer output format, and overhead R_N",
                "advice-free realizer proof, or a private-row/no-realizer theorem for the selected rule",
                "same-theory expansion certificates or a proof that such certificates cannot be uniformly extracted",
                "updated non-claims explaining that unresolved semantic FormulaEval is a model boundary, not a P vs NP barrier slogan",
                "live pvsnp_inference_quality packet reviewed by barrier-specificity and proof-complexity reviewers",
            ],
            proof_steps=[
                "Proof step: pick exactly one semantic FormulaEval rule and freeze its proof-system syntax.",
                "Proof step: define which generated SAT rows can influence the rule value and what counts as a charged witness.",
                "Proof step: attempt to construct R_A and same-theory expansions from proof syntax and N alone.",
                "Proof step: if the construction fails, build the private-row/unread-enable-bit countermodel for that rule.",
                "Proof step: record whether the rule joins the transparent theorem or remains quarantined as semantic power.",
            ],
            success_criteria=[
                "The selected semantic rule is concrete enough that the realizer or countermodel is independently checkable.",
                "All influence rows are uniformly listed and charged, or the exact unchargeable semantic step is named.",
                "The output eliminates vague language about semantic FormulaEval and replaces it with a rule-level theorem or no-go.",
            ],
            demotion_criteria=[
                "Demote if RealSATInfluenceRealizer_N is only restated without choosing a semantic rule.",
                "Demote if the row set uses SAT-truth advice or hidden nonuniform row selection.",
                "Demote if the claimed realizer omits R_N from the Gamma ledger.",
                "Demote if the negative result does not identify the first semantic inference that cannot be charged.",
            ],
            required_skills=all_main_skills,
            paper_handoff="Use as the exact open-boundary paragraph for full semantic FormulaEval, or as a theorem if the chosen rule admits a realizer.",
            source_anchor="Cycle 120 RealSATInfluenceRealizer_N boundary plus proof-delivery queue Formula-semantic extraction open problem.",
            proof_status="named_semantic_gap_needs_rule_level_resolution",
        ),
        item(
            queue_id="pvsnp.paper.l120-theorem-countermodel-package",
            rank=4,
            title="Package the cycle-120 theorem/countermodel pair as a paper-ready module",
            next_analysis=(
                "Assemble the least-closed transparent-support theorem, hidden-support countermodel, RealSATInfluenceRealizer_N "
                "open boundary, q-trichotomy support-density corollary, and selector-example table into one coherent paper "
                "module. The package must be readable without marathon context."
            ),
            theorem_goal=(
                "Paper module: a scoped parser/falsifier contribution for FormulaEval in beta-zero parity magnification, "
                "showing exactly when transparent FormulaEval yields a same-model upper-bound falsifier and exactly where "
                "hidden semantic influence escapes the controlled interface."
            ),
            source_object=(
                "Cycles 116-120, especially L120.1 LeastClosedTransparentSupport_N, L120.2 UnreachableSupportDeletion_N, "
                "L120.3 FirstHiddenReachableUse_N, and the branch outputs that state Gamma_dag, hidden-row falsifiers, "
                "and q<epsilon/q=epsilon/q>epsilon support-density cases."
            ),
            target_object=(
                "A paper-ready theorem/countermodel section with definitions, theorem statements, proof sketches, examples, "
                "non-claims, and a handoff to the broader parity magnification/full-row barrier draft."
            ),
            proof_outputs=[
                "definition ledger for H_N^SAT, Psys_sym^dag, K_dag(pi), Gamma_bEF, U(K), X(K), E_pi, and LB_N(1+epsilon)",
                "theorem statement and proof sketch for the least-closed transparent support upper-bound falsifier",
                "countermodel theorem for first hidden reachable support using private rows or unread enable bits",
                "RealSATInfluenceRealizer_N open-boundary box with exact input, output, overhead, and non-claims",
                "q-trichotomy support-density corollary for q<epsilon, q=epsilon, and q>epsilon",
                "example table demoting interval-union, scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete rules to corollaries/examples",
                "paper-ready prose with no pipeline jargon and no claim of P != NP progress",
            ],
            proof_steps=[
                "Proof step: consolidate definitions and notation from cycles 116-120 into one local ledger.",
                "Proof step: write theorem/countermodel statements before examples, so selector cases cannot become separate main routes.",
                "Proof step: attach proof sketches that cite the L120.1 audit packet and RealSAT boundary item where needed.",
                "Proof step: state non-claims and model boundaries explicitly.",
                "Proof step: validate against proof-delivery and inference-quality gates.",
            ],
            success_criteria=[
                "The module is understandable as a standalone paper section.",
                "The positive theorem, negative countermodel, and semantic open boundary are separated cleanly.",
                "Examples are corollaries/examples only; no new selector zoo is created.",
                "The paper handoff preserves the scoped claim and does not oversell P vs NP progress.",
            ],
            demotion_criteria=[
                "Demote if the package is a report summary rather than theorem/countermodel text.",
                "Demote if it depends on marathon-specific workflow language.",
                "Demote if it blurs transparent extensional FormulaEval with full semantic SAT FormulaEval.",
                "Demote if it omits the q-trichotomy or the non-claims.",
            ],
            required_skills=[
                "proof-delivery-workflow-orchestrator",
                "proof-obligation-formalizer",
                "lemma-chain-proof-builder",
                "proof-gap-countermodel-splitter",
                "proof-quality-gatekeeper",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
                "pvsnp-proof-complexity-transfer-reviewer",
                "pvsnp-symbolic-complexity-auditor",
            ],
            paper_handoff="Use as the publishable scoped note/module if the full semantic realizer remains open.",
            source_anchor="Cycles 116-120 and the current mathematical story in the discovery marathon report.",
            proof_status="paper_module_missing_after_cycle_0120",
        ),
        item(
            queue_id="pvsnp.paper.l120-inference-quality-gate-closure",
            rank=5,
            title="Close the L120 inference-quality and marker gaps before promotion",
            next_analysis=(
                "Prepare the promotion gate for the L120 theorem work. Emit a fresh pvsnp_inference_quality packet for the "
                "least-closed support theorem, run the reviewer stack, and repair any source/target/model/validity marker "
                "gaps before treating the theorem package as a paper result."
            ),
            theorem_goal=(
                "Validation theorem for promotion readiness: every L120 claim has explicit source object, target object, "
                "controlled interface, target-preserving condition, reduction direction, quantifiers, advice discipline, "
                "barrier scope, and proof-complexity transfer status."
            ),
            source_object=(
                "The live L120 claims, the 93 active inference-quality packets, and the discovery report warning that not all "
                "source/target/same-theory/validity markers are globally present."
            ),
            target_object=(
                "A repaired inference-quality packet and gate report that says exactly which L120 claims are promotable, "
                "which are conditional, and which remain blocked at RealSATInfluenceRealizer_N."
            ),
            proof_outputs=[
                "new pvsnp_inference_quality packet for L120.1 and the L120 theorem/countermodel package",
                "reviewer findings from reduction consistency, quantifier uniformity, barrier specificity, proof-complexity transfer, and meta-complexity carrier checks",
                "marker-gap repair table for source object, target object, controlled interface, target-preserving condition, and validity regimes",
                "promotion verdict separating proved scoped theorem, conditional theorem, open boundary, and non-claims",
                "validator output from validate_pvsnp_inference_quality.py and validate_pvsnp_proof_delivery_queue.py",
            ],
            proof_steps=[
                "Proof step: write the IQ packet from the actual theorem text, not from a marathon summary.",
                "Proof step: run each reviewer lens and convert objections into proof obligations or demotion notes.",
                "Proof step: repair missing markers in the queue/report artifacts if validation finds them.",
                "Proof step: record a final promotion verdict before paper integration.",
            ],
            success_criteria=[
                "The L120 theorem package has a live IQ packet that passes validation.",
                "No source/target/model/validity marker is implicit.",
                "Reviewer objections are either discharged, converted to named obligations, or marked as demotion blockers.",
                "The promotion verdict is conservative and explicitly says what is not proved.",
            ],
            demotion_criteria=[
                "Demote if the IQ packet claims P vs NP progress rather than a scoped parser/falsifier result.",
                "Demote if source and target models are not the same nonuniform SIZE model.",
                "Demote if RealSATInfluenceRealizer_N is treated as solved without a rule-level proof.",
                "Demote if validation fails and the failure is not converted into a concrete repair item.",
            ],
            required_skills=[
                "pvsnp-inference-quality-controller",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
                "pvsnp-proof-complexity-transfer-reviewer",
                "pvsnp-meta-complexity-carrier-reviewer",
                "proof-quality-gatekeeper",
                "proof-obligation-formalizer",
            ],
            paper_handoff="Use as the final gate before promoting the L120 module into the paper draft or queueing another proof attempt.",
            source_anchor="P vs NP inference-quality report and discovery marathon research-quality marker warning after cycle 120.",
            proof_status="promotion_gate_missing_after_cycle_0120",
        ),
        item(
            queue_id="pvsnp.paper.full-row-barrier-proof-audit",
            rank=6,
            title="Audit and package the draft's proved beta-zero/full-row barrier theorem chain",
            next_analysis=(
                "Proof-audit task extracted from the draft theorem stack: rebuild the exponent-window, batched substitution, "
                "beta-zero transfer, equality patching, naturalization, row-forcing, parity full-row, parser-to-query, "
                "incidence-sketch, and one-sided forcing proofs as a dependency-checked proof packet."
            ),
            theorem_goal=(
                "Verified theorem-chain packet: beta-zero transfers remove exponent debt; functional certificates naturalize; "
                "occurrence-relativizing parity certificates pay Omega(M_n s_n/n)."
            ),
            source_object="The draft's proposition/lemma/theorem environments and their dependency graph.",
            target_object="A paper-ready proof packet with explicit hypotheses, quantifiers, non-claims, and theorem dependencies.",
            proof_outputs=[
                "dependency graph of all proved draft statements",
                "definition ledger for H_n^SAT, H_n^y, F_{n,A}^z, Phi_n, C_b(A_M), Q_pi, R_b(Q,alpha), and p_x",
                "formal proof-obligation list for every theorem/proposition/corollary",
                "gap report separating proved, conditional, and open components",
                "paper-ready proof summary with no pipeline jargon",
            ],
            proof_steps=[
                "Proof step: extract every theorem/proposition/corollary proof from the draft and list its exact assumptions.",
                "Proof step: check exponent arithmetic and the beta-zero disappearance of the target circuit exponent c.",
                "Proof step: verify that equality patching and residual threshold use only row exceptions and O(n) equality predicates.",
                "Proof step: verify naturalization hypotheses are dense, constructive, and functional over arbitrary label tables.",
                "Proof step: verify row-forcing uses occurrence-completion soundness and not real SAT semantics.",
            ],
            success_criteria=[
                "Every proved draft statement has assumptions, conclusion, proof dependencies, and barrier scope recorded.",
                "No step silently upgrades occurrence-label statements to formula-label or full proof-system statements.",
                "The theorem chain is ready for paper insertion or referee-style proof checking.",
            ],
            demotion_criteria=[
                "Demote if any proof uses an unstated uniformity, density, constructivity, or formula-realizability assumption.",
                "Demote if theorem dependencies are circular or if the draft's non-claims are not preserved.",
            ],
            required_skills=[
                "proof-delivery-workflow-orchestrator",
                "proof-obligation-formalizer",
                "lemma-chain-proof-builder",
                "proof-quality-gatekeeper",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
                "pvsnp-proof-complexity-transfer-reviewer",
            ],
            paper_handoff="Use as the proof backbone of the parity magnification/full-row barrier paper.",
            source_anchor="Draft sections 2-8 plus appendices: all theorem/proposition/corollary proof environments.",
            proof_status="proved_in_draft_needs_formal_audit",
        ),
        item(
            queue_id="pvsnp.paper.explicit-hard-generator-open-problem",
            rank=7,
            title="Attack the explicit hard-generator/source-lower-bound open problem",
            next_analysis=(
                "Open-problem task extracted from the draft discussion: construct or rule out a label-independent batched generator "
                "with polylogarithmic SAT instances, M_n=n^{q+o(1)}, generator size n^{rho+o(1)}, q,rho<1+epsilon, and a "
                "provable general-circuit lower bound Ckt(H_n^SAT)>n^{1+epsilon-o(1)}."
            ),
            theorem_goal="Source-lower-bound theorem or impossibility diagnosis for a concrete beta-zero SAT parity carrier.",
            source_object="Candidate batched generator G_n and parity carrier H_n^SAT from polylog-length SAT formulas.",
            target_object="A source lower bound strong enough to activate the beta-zero magnification corollary, or a precise obstruction explaining why the candidate collapses.",
            proof_outputs=[
                "candidate generator specification with q, rho, d, and formula universe U_n",
                "incidence sketch/rank/falsifier audit",
                "attempted lower-bound proof obligations",
                "blocked-lemma or impossibility packet if lower-bound proof fails",
                "paper paragraph stating whether this supplies or fails to supply the central source problem",
            ],
            proof_steps=[
                "Proof step: define the generator and compute q, rho, d, |U_n|, collision structure, and formula-realizability constraints.",
                "Proof step: run incidence-sketch falsification before claiming lower-bound promise.",
                "Proof step: attempt a lower-bound route or derive an impossibility/upper-bound certificate.",
                "Proof step: verify that any lower bound is for general circuits on the scalar carrier, not only incidence rank or restricted models.",
            ],
            success_criteria=[
                "A concrete generator is named with verified beta-zero transfer parameters.",
                "The branch produces either a real lower-bound lemma, a reproducible upper-bound falsifier, or a sharp reason it cannot be the source problem.",
                "Any claimed progress distinguishes scalar circuit lower bounds from incidence-linear diagnostics.",
            ],
            demotion_criteria=[
                "Demote if no explicit generator is specified.",
                "Demote if the evidence is only high rank, randomness intuition, or incidence complexity without a general-circuit lower-bound bridge.",
                "Demote if q or rho fails the stated threshold needed by the transfer theorem.",
            ],
            required_skills=[
                "proof-delivery-workflow-orchestrator",
                "lemma-chain-proof-builder",
                "proof-gap-countermodel-splitter",
                "proof-quality-gatekeeper",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-qualitative-complexity-reasoner",
                "pvsnp-impossibility-theorem-forger",
                "pvsnp-conceptual-pressure-localizer",
                "pvsnp-forcedrows-proof-workflow",
                "pvsnp-barrier-specificity-reviewer",
            ],
            paper_handoff="Promote only if it delivers an explicit generator theorem, falsifier, or principled obstruction.",
            source_anchor="Draft discussion paragraph 'An explicit hard generator'.",
            proof_status="central_open_problem_from_draft",
        ),
        item(
            queue_id="pvsnp.paper.strong-system-parser-instantiation",
            rank=8,
            title="Instantiate the parser-to-query consequence for a concrete strong proof system",
            next_analysis=(
                "Open-problem/proof task extracted from the draft's strong-system paragraph and Proposition parser-to-query: "
                "choose a concrete proof formalism for lower-bound statements, define exactly which formula equality and SAT "
                "semantic facts it can access, and prove or refute the parser property that maps accepted proofs pi to "
                "occurrence transcripts Q_pi."
            ),
            theorem_goal="Concrete parser-to-query instantiation theorem or counterexample for a named proof system.",
            source_object="Named proof formalism, proof pi, verifier/parser, and allowed SAT/equality axioms.",
            target_object="A proof-system-specific theorem linking proof length/access to Omega(M_n s_n/n), or an escape principle that blocks the link.",
            proof_outputs=[
                "proof-system syntax and verifier model",
                "allowed SAT facts and formula-equality principles",
                "parser pi -> (Q_pi, alpha_pi) definition or countermodel",
                "quantitative p(T,n) exposure bound",
                "paper-ready proof-system consequence or limitation",
            ],
            proof_steps=[
                "Proof step: select the proof formalism and define the lower-bound sentence it proves.",
                "Proof step: map each proof rule to functional, occurrence-local, or formula-semantic behavior.",
                "Proof step: prove parser invariance under occurrence completions or construct a rule-level countermodel.",
                "Proof step: if parser holds, derive the Omega(M_n s_n/n) access/proof-size consequence.",
            ],
            success_criteria=[
                "The selected proof system and its SAT access are explicit enough for independent checking.",
                "The parser property is proved with a quantitative p(T,n), or a precise semantic escape is isolated.",
                "The output is not a generic 'strong systems are hard' statement; it names the exact proof rule that matters.",
            ],
            demotion_criteria=[
                "Demote if the proof system remains unnamed or if its SAT facts are unspecified.",
                "Demote if the parser theorem assumes occurrence locality instead of deriving it.",
                "Demote if a negative answer does not identify the formula-semantic principle defeating occurrence-wise completion.",
            ],
            required_skills=[
                "proof-delivery-workflow-orchestrator",
                "proof-obligation-formalizer",
                "lemma-chain-proof-builder",
                "proof-gap-countermodel-splitter",
                "proof-quality-gatekeeper",
                "pvsnp-forcedrows-proof-workflow",
                "pvsnp-inference-quality-controller",
                "pvsnp-proof-complexity-transfer-reviewer",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-negative-tactic-selector",
            ],
            paper_handoff="Use to turn the conditional parser-to-query proposition into a named proof-system result or a precise open boundary.",
            source_anchor="Draft discussion paragraph 'A strong-system instantiation' and Proposition 'Parser-to-query consequence'.",
            proof_status="open_problem_with_conditional_proposition",
        ),
        item(
            queue_id="pvsnp.paper.incidence-falsifier-normal-form",
            rank=9,
            title="Use incidence sketches as falsifiers and define the missing normal-form bridge",
            next_analysis=(
                "Proof/diagnostic task extracted from the appendix and discussion: for candidate generators, search for low-rank "
                "or sparse affine-incidence sketches p_x=sum_i a_i(x)b_i off a small exceptional set, and state the exact "
                "nonrelativizing normal-form theorem that would be needed to turn absence of such sketches into lower-bound evidence."
            ),
            theorem_goal="Incidence-falsifier theorem plus normal-form open problem for translating diagnostics into lower bounds.",
            source_object="Generated formula universe U_n, incidence vectors p_x in F^{U_n}, coefficient functions a_i, sketch vectors b_i, and exception set B_n.",
            target_object="A reproducible upper-bound falsifier or a clearly scoped normal-form theorem needed before incidence diagnostics can support source lower bounds.",
            proof_outputs=[
                "incidence representation and sketch-search protocol",
                "upper-bound theorem application Ckt(H_n^y) <= O(A_n+K+E_n n)",
                "candidate-generator falsifier report",
                "normal-form theorem statement separating scalar circuits from incidence compression",
                "paper-ready diagnostic subsection",
            ],
            proof_steps=[
                "Proof step: instantiate U_n and p_x for the candidate carrier.",
                "Proof step: attempt affine/sparse incidence sketches and compute A_n, K, and E_n.",
                "Proof step: if a sketch is found, derive the explicit upper-bound contradiction to the proposed source lower bound.",
                "Proof step: if no sketch is found, record this only as nonproof evidence and state the missing scalar-circuit normal form.",
            ],
            success_criteria=[
                "Every candidate generator is checked for the appendix's explicit upper-bound mechanism before promotion.",
                "The output never treats absence of a sketch as a lower bound.",
                "The normal-form bridge is stated as a theorem obligation with assumptions strong enough to imply scalar circuit hardness.",
            ],
            demotion_criteria=[
                "Demote if the branch uses incidence rank as a lower bound without a scalar-circuit bridge.",
                "Demote if K, A_n, E_n, or exceptional-row patch cost are not computed or bounded.",
                "Demote if the diagnostic does not feed either a falsifier or a specific normal-form theorem.",
            ],
            required_skills=[
                "proof-obligation-formalizer",
                "lemma-chain-proof-builder",
                "proof-gap-countermodel-splitter",
                "proof-quality-gatekeeper",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-meta-complexity-carrier-reviewer",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-barrier-specificity-reviewer",
            ],
            paper_handoff="Add as the generator-screening and upper-bound-falsifier module in the paper.",
            source_anchor="Draft appendix 'Incidence sketches as upper-bound falsifiers' and discussion paragraph 'From diagnostics to lower bounds'.",
            proof_status="proved_diagnostic_plus_open_bridge",
        ),
        item(
            queue_id="pvsnp.paper.aggregator-design-open-problem",
            rank=10,
            title="Search aggregator designs beyond parity with explicit transfer and certificate tradeoffs",
            next_analysis=(
                "Open-direction task extracted from the draft: compare parity with alternative aggregators by computing transfer cost, "
                "C_0(A_M), C_1(A_M), one-sided certificate behavior, algebraic structure, and whether the aggregator preserves "
                "beta-zero all-exponent SAT transfer without reopening easy selector/separator certificates."
            ),
            theorem_goal="Aggregator tradeoff theorem or no-go table identifying which aggregators preserve the desired certificate debt.",
            source_object="Candidate row aggregator family A_M and batched SAT labels y(G_{n,j}(x)).",
            target_object="A ranked set of aggregator candidates with proof-relevant certificate-complexity and transfer-cost guarantees.",
            proof_outputs=[
                "aggregator candidate list",
                "computed C_0(A_M), C_1(A_M), circuit size, and one-sided behavior",
                "beta-zero transfer audit for each aggregator",
                "qualitative explanation of proof locality versus algebraic exploitable structure",
                "paper-ready aggregator-design paragraph or appendix",
            ],
            proof_steps=[
                "Proof step: compute certificate complexities for each candidate aggregator.",
                "Proof step: verify size O(M) or record the exact transfer cost penalty.",
                "Proof step: test whether one-sided SAT evidence can cheaply force rows.",
                "Proof step: promote only candidates that improve some tradeoff without losing the all-polynomial-exponent transfer.",
            ],
            success_criteria=[
                "Parity remains justified or a better aggregator is identified by explicit C_b(A_M) and transfer calculations.",
                "Any proposed aggregator has proof-locality consequences stated as theorem obligations, not analogies.",
                "The output explains whether it strengthens, weakens, or complements the full-row barrier.",
            ],
            demotion_criteria=[
                "Demote if aggregator comparison does not compute C_0 and C_1.",
                "Demote if the aggregator creates a cheap one-sided certificate that defeats the intended full-row burden.",
                "Demote if transfer cost reintroduces positive beta exponent debt.",
            ],
            required_skills=[
                "pvsnp-qualitative-complexity-reasoner",
                "pvsnp-symbolic-complexity-auditor",
                "pvsnp-conceptual-pressure-localizer",
                "proof-obligation-formalizer",
                "proof-quality-gatekeeper",
                "pvsnp-barrier-specificity-reviewer",
            ],
            paper_handoff="Use to justify parity's role or to add an aggregator-comparison extension section.",
            source_anchor="Draft discussion paragraph 'Aggregator design' plus appendix 'A one-sided version of row forcing'.",
            proof_status="open_direction_from_draft",
        ),
        item(
            queue_id="pvsnp.paper.occurrence-row-forcing-proposition-delivery",
            rank=11,
            title="Deliver the occurrence-local row-forcing theorem as a standalone scoped contribution",
            next_analysis=(
                "Proof-delivery task extracted from the proved row-forcing section: package the occurrence-completion theorem, "
                "parity full-row corollary, adaptive verifier corollary, and one-sided variant as a standalone barrier theorem "
                "with exact scope."
            ),
            theorem_goal="Standalone occurrence-local certificate-debt theorem for beta-zero parity carriers.",
            source_object="Completion-sound partial transcript (Q,alpha), forced rows R_b(Q,alpha), aggregator certificate complexity C_b(A_M), and patch circuits.",
            target_object="A scoped publishable theorem: occurrence-relativizing lower-bound certificates must pay full-row cost for parity.",
            proof_outputs=[
                "formal theorem and corollaries with all constants/quantifiers explicit",
                "row-spoofing completion construction",
                "equality-patching dependency proof",
                "adaptive verifier interpretation",
                "paper-ready theorem statement and proof",
            ],
            proof_steps=[
                "Proof step: restate completion soundness, forced rows, and certificate complexity without SAT-semantics leakage.",
                "Proof step: reconstruct baseline completion z^(b) and verify it extends the transcript.",
                "Proof step: patch forced rows and derive |R_b|=Omega(s_n/n).",
                "Proof step: specialize to parity and adaptive verifiers.",
            ],
            success_criteria=[
                "The theorem is independently understandable without the rest of the P vs NP discovery machinery.",
                "The proof states exactly why formula-semantic SAT proofs are outside scope.",
                "The theorem can be cited as the paper's local-certificate barrier contribution.",
            ],
            demotion_criteria=[
                "Demote if the proof assumes formula-realizability or SAT semantics.",
                "Demote if the sparse patch construction does not produce a circuit below the claimed threshold.",
                "Demote if the theorem cannot state its non-claims cleanly.",
            ],
            required_skills=[
                "pvsnp-forcedrows-proof-workflow",
                "proof-obligation-formalizer",
                "lemma-chain-proof-builder",
                "proof-quality-gatekeeper",
                "pvsnp-reduction-consistency-reviewer",
                "pvsnp-quantifier-uniformity-reviewer",
                "pvsnp-barrier-specificity-reviewer",
            ],
            paper_handoff="Promote as the scoped standalone contribution if the broader formula-semantic extraction remains open.",
            source_anchor="Draft section 'Occurrence-local certificates and the full-row barrier' plus appendix 'A one-sided version of row forcing'.",
            proof_status="proved_in_draft_needs_standalone_packaging",
        ),
    ]


def build_report() -> dict[str, Any]:
    common = common_fields()
    items = build_items()
    return {
        "version": 2,
        "generated_utc": utc_now(),
        "status": "pvsnp_proof_delivery_queue_ready",
        "target_id": TARGET_ID,
        **common,
        "queue_policy": {
            "priority_rule": (
                "Items extracted from the parity magnification draft's open problems and proofs outrank broad "
                "exploration until discharged, blocked at a named lemma, or demoted by countermodel."
            ),
            "promotion_rule": "A queue item completes only by emitting a proof packet and passing inference-quality/proof-quality gates.",
            "anti_loop_rule": (
                "Do not add another broad marathon cycle while the top formula-semantic extraction task has no proof "
                "attempt, countermodel, or named semantic-escape disposition."
            ),
        },
        "extracted_from_draft": {
            "source": SOURCE_DRAFT_PATH,
            "proof_assets": EXTRACTED_PROOF_ASSETS,
            "open_directions": EXTRACTED_OPEN_DIRECTIONS,
        },
        "items": items,
        "top_item_id": items[0]["queue_id"],
        "validation_handoff": "python agentic/scripts/validate_pvsnp_proof_delivery_queue.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    extracted = report["extracted_from_draft"]
    lines = [
        "# P vs NP Proof Delivery Queue",
        "",
        f"- Status: `{report['status']}`",
        f"- Target: `{report['target_id']}`",
        f"- Top item: `{report['top_item_id']}`",
        f"- Source draft: `{extracted['source']}`",
        "",
        "## Extracted Proof Assets",
        "",
    ]
    for asset in extracted["proof_assets"]:
        lines.extend(
            [
                f"- **{asset['proof_status']}**: {asset['contribution']}",
                f"  Source: {asset['anchor']}",
            ]
        )
    lines.extend(["", "## Extracted Open Directions", ""])
    for direction in extracted["open_directions"]:
        lines.extend(
            [
                f"- **{direction['anchor']}**",
                f"  {direction['problem']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Queue Policy",
            "",
            f"- Priority: {report['queue_policy']['priority_rule']}",
            f"- Promotion: {report['queue_policy']['promotion_rule']}",
            f"- Anti-loop: {report['queue_policy']['anti_loop_rule']}",
            "",
            "## Highest-Priority Proof Items",
            "",
        ]
    )
    for row in report["items"]:
        lines.extend(
            [
                f"### {row['rank']}. {row['title']}",
                "",
                f"- Queue ID: `{row['queue_id']}`",
                f"- Priority score: `{row['priority_score']}`",
                f"- Proof status: `{row['proof_status']}`",
                f"- Source anchor: {row['source_anchor']}",
                f"- Next analysis: {row['next_analysis']}",
                f"- Theorem goal: {row['theorem_goal']}",
                f"- Source object: {row['source_object']}",
                f"- Target object: {row['target_object']}",
                f"- Paper handoff: {row['paper_handoff']}",
                "",
                "Proof outputs:",
                *[f"- {output}" for output in row["proof_outputs"]],
                "",
                "Success criteria:",
                *[f"- {criterion}" for criterion in row["success_criteria"]],
                "",
                "Demotion criteria:",
                *[f"- {criterion}" for criterion in row["demotion_criteria"]],
                "",
                "Required skills:",
                *[f"- `{skill}`" for skill in row["required_skills"]],
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
