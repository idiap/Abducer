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
"""Build a structured formal-physics derivation for the timeline paper."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json
from build_timeline_paper_blueprint import OUT_JSON as BLUEPRINT_JSON
from build_timeline_paper_interpretation import OUT_JSON as INTERPRETATION_JSON
from target_profiles import target_profile
from timeline_paper_common import latex_escape, safe_tex_math, tex_itemize


OUT_DIR = ROOT / "agentic/reports/timeline_formal_derivation"
OUT_JSON = OUT_DIR / "latest.json"
OUT_TEX = OUT_DIR / "latest.tex"
SCHEMA = ROOT / "agentic/spec/timeline_formal_derivation.schema.json"


def has_wilson_content(units: list[dict]) -> bool:
    text = " ".join(row.get("content", "") for row in units).lower()
    return any(token in text for token in ["wilson", "os", "schur", "gram", "reflection", "kappa"])


def build_pvsnp_derivation(blueprint: dict, units: list[dict]) -> dict:
    source_ids = [row["unit_id"] for row in units if row.get("argument_role") in {"proof_step", "calculation_input", "validation_boundary", "claim"}][:24]
    definitions = [
        {
            "symbol": "H_N",
            "text": "A source carrier language, truth-table family, meta-complexity predicate, or proof-mediated object indexed by source length N.",
            "latex": r"H_N\subseteq\{0,1\}^{N}\quad\text{or}\quad H_N:\{0,1\}^{N}\to\{0,1\}",
            "valid_when": "The carrier is explicitly constructed or specified without nonuniform hard-row advice.",
            "source_unit_ids": source_ids[:4],
        },
        {
            "symbol": "SAT_m",
            "text": "The target SAT language or SAT truth-table slice at input length m, used as the reference NP-complete target.",
            "latex": r"\mathrm{SAT}_m=\mathrm{SAT}\cap\{0,1\}^m",
            "valid_when": "The reduction or transfer states how source length N maps to target length m.",
            "source_unit_ids": source_ids[:4],
        },
        {
            "symbol": "a,q,beta",
            "text": "The source lower-bound exponent, overhead exponent, and target-query-length exponent in a transfer inequality.",
            "latex": r"\mathrm{SIZE}(H_N)\le N^{q+\beta c+o(1)}\quad\text{from}\quad \mathrm{SAT}\in\mathrm{SIZE}(n^c)",
            "valid_when": "All padding, decoding, verifier, and advice costs are counted in the same circuit model.",
            "source_unit_ids": source_ids[:6],
        },
    ]
    assumptions = [
        "The source carrier H_N and target class are named before any transfer claim is made.",
        "The circuit model is fixed throughout the transfer, including uniformity and advice conventions.",
        "The transfer from SAT circuits to source-carrier circuits has an explicit exponent envelope q+beta*c+o(1).",
        "Barrier status is route-specific: naturalness, relativization, algebrization, and advice leakage are attached to the actual theorem shape.",
    ]
    propositions = [
        {
            "name": "Bounded-window transfer obstruction",
            "statement": "A barely-superlinear source lower bound excludes only the target exponents that fit below the transferred upper-bound envelope.",
            "latex": r"\mathrm{SIZE}(H_N)>N^a\ \wedge\ \mathrm{SAT}\in\mathrm{SIZE}(n^c)\Rightarrow \mathrm{SIZE}(H_N)\le N^{q+\beta c+o(1)}\quad\Longrightarrow\quad a>q+\beta c",
            "proof_steps": [
                "Assume SAT has nonuniform circuits of size n^c in the stated model.",
                "Apply the route transfer to build source-carrier circuits of size N^{q+beta c+o(1)}.",
                "Contradict the source lower bound only for those c with a>q+beta c.",
                "If beta>0, a fixed a excludes at most a bounded exponent window.",
            ],
            "valid_when": "The source and target circuit models, length map, and overhead exponents are unchanged across the implication.",
            "source_unit_ids": source_ids,
        },
        {
            "name": "All-exponent lift gate",
            "statement": "A route can support NP not subset P/poly only if it preserves the all-exponent quantifier or supplies a cofinal indexed family.",
            "latex": r"\forall c\ \exists N_0\ \forall N\ge N_0:\quad a_c>q_c+\beta_c c",
            "proof_steps": [
                "P/poly exclusion requires ruling out every fixed polynomial exponent c for SAT or an NP-complete target.",
                "For each c, the source lower bound must outrun the transferred upper bound.",
                "If the same source theorem has beta>0 and fixed a, large c survives.",
                "Thus promotion needs beta=0 with positive margin or a cofinal parameter family with no advice leakage.",
            ],
            "valid_when": "The parameter family is uniform or advice-accounted and valid on target-relevant lengths.",
            "source_unit_ids": source_ids,
        },
        {
            "name": "Searchable certificate gate",
            "statement": "A meta-complexity or proof-object bridge is useful only when certificates are frequent, searchable, sound, and advice-free without becoming a large constructive natural property.",
            "latex": r"\exists u,\pi\ \bigl(|\pi|=O(m)\wedge V(u,\pi)=1\bigr)\Rightarrow CC(f_u)>2^{\epsilon m}",
            "proof_steps": [
                "State the verifier, decoder, certificate length, and search schedule.",
                "Prove that accepted pairs exist in every required gap interval.",
                "Prove soundness from certificate acceptance to the claimed circuit lower bound.",
                "Audit whether the accepted set is large and constructive, or whether row selection leaks advice.",
            ],
            "valid_when": "The verifier and search live inside the intended target class and do not choose hard rows nonuniformly.",
            "source_unit_ids": source_ids,
        },
    ]
    calculations = [
        {
            "name": "Direct-cluster soundness falsifier",
            "statement": "Odd-charge Tseitin-style parity ambiguity is a finite falsifier for local consistency claims that do not bind the target row semantically.",
            "latex": r"\mathrm{LocalConsistent}(C)\not\Rightarrow \mathrm{DirectClusterSound}(C,k)",
            "valid_when": "The tested proof system exposes only local projections or bounded-width proof views and lacks a global parity-binding axiom.",
            "source_unit_ids": source_ids,
        }
    ]
    obligations = [
        "Instantiate one named proof system or meta-complexity carrier and compute q, beta, advice cost, and certificate-search exponent.",
        "Prove the direct-cluster or parity-binding lemma, or exhibit the odd-charge Tseitin counterexample for that named system.",
        "Run a prior-art boundary check against hardness magnification, MCSP/MKtP, natural-proofs, and proof-complexity transfer literature.",
        "State whether the surviving result is a positive bridge theorem, a scoped no-go theorem, or a demoted route diagnostic.",
    ]
    return {
        "derivation_id": stable_id("formal-derivation", blueprint.get("blueprint_id"), "pvsnp-transfer"),
        "target_family": "pvsnp_transfer_obstruction",
        "mathematical_object": "Target-preserving transfer envelope for P vs NP bridge routes.",
        "derivation_label": "Formal Complexity Derivation",
        "definitions": definitions,
        "assumptions": assumptions,
        "propositions": propositions,
        "calculations": calculations,
        "unresolved_obligations": obligations,
        "non_claims": blueprint.get("non_claims", []),
    }


def build_yang_mills_derivation(blueprint: dict, units: list[dict]) -> dict:
    source_ids = [row["unit_id"] for row in units if row.get("argument_role") in {"proof_step", "calculation_input", "validation_boundary"}][:24]
    definitions = [
        {
            "symbol": "N_eta(i,j)",
            "text": "Reflected Euclidean Gram matrix of a finite family of gauge-invariant Wilson collar observables.",
            "latex": r"N_\eta(i,j)=\langle \Theta W_i^{(\eta)},W_j^{(\eta)}\rangle",
            "valid_when": "The expectation is taken in the same regulated Yang-Mills measure being tested.",
            "source_unit_ids": source_ids[:4],
        },
        {
            "symbol": "M_eta",
            "text": "Normalized reflected Wilson quotient after boundary/diagonal renormalization.",
            "latex": r"M_\eta=\widehat N_\eta\oslash \widehat B_\eta",
            "valid_when": "The denominator boundary factor is nonzero and extracted from the same observable family.",
            "source_unit_ids": source_ids[:4],
        },
        {
            "symbol": "P",
            "text": "Projection away from the rank-one constant OS direction.",
            "latex": r"P=I-\frac{\mathbf 1\mathbf 1^*}{n}",
            "valid_when": "The finite block is normalized so the vacuum/constant sector is represented by the span of \\mathbf 1.",
            "source_unit_ids": source_ids[:4],
        },
    ]
    assumptions = [
        "The chosen observable family is gauge-invariant and reflected across a common Euclidean reflection plane.",
        "The quotient matrix has an expansion M_eta=11^*+eta H+eta^2K+O(eta^3) with Hermitian H and K.",
        "The O(eta^3) remainder is uniform on the finite observable block.",
        "The finite quotient is a legitimate same-theory shadow of OS reconstruction rather than a proxy matrix.",
    ]
    propositions = [
        {
            "name": "First-order quotient positivity",
            "statement": "If the reflected quotient is OS-positive for small positive eta, then PHP is positive semidefinite on 1^perp.",
            "latex": r"P H P\succeq 0",
            "proof_steps": [
                "Take any v in 1^perp so the rank-one term contributes zero.",
                "Expand v^*M_eta v to first order in eta.",
                "OS positivity for both sufficiently small signs/regimes forces the leading nonzero quadratic form to be nonnegative.",
            ],
            "valid_when": "The expansion and positivity claim hold in the same regulated theory and normalization.",
            "source_unit_ids": source_ids,
        },
        {
            "name": "Second-order Schur-Feshbach obstruction",
            "statement": "If PHP has a null sector, the Schur-corrected second-order form must be nonnegative on that sector.",
            "latex": r"\Omega_2=P\left(K-n^{-2}H\mathbf 1\mathbf 1^*HP\right)P,\qquad w^*\Omega_2w\ge0\ \text{for } w\in\ker(PHP)\cap\mathbf 1^\perp",
            "proof_steps": [
                "Separate the large constant direction from the quotient sector.",
                "Apply the finite Schur/Feshbach reduction to remove one-body normalization leakage.",
                "Evaluate the remaining second-order form on the null vectors of PHP.",
            ],
            "valid_when": "The rank-one sector and boundary normalization are the same ones used in the Wilson quotient.",
            "source_unit_ids": source_ids,
        },
    ]
    calculations = [
        {
            "name": "Endpoint kappa-four certificate",
            "statement": "The post-H,K endpoint term is controlled by a signed incidence dominance functional and heat-kernel cumulant bounds.",
            "latex": r"R_{\mathrm{end}}=C_{\mathrm{col}}\sum_v(2\kappa_{4,v}(b_{12,v})-4\kappa_{4,v}(b_{13,v})-4\kappa_{4,v}(b_{23,v}))+E_{\mathrm{tail}}",
            "valid_when": "Disconnected Wick-square terms have been placed in the positive margin and endpoint boxes are enumerated in the same collar regulator.",
            "source_unit_ids": source_ids,
        }
    ]
    obligations = [
        "Compute H and K for the first concrete reflected Wilson collar or hairpin block.",
        "Enumerate the endpoint incidence table for B_12,v, B_13,v, and B_23,v.",
        "Prove uniform collar/cutoff control of boundary-OPE and tail remainders.",
        "Show the finite quotient transfers into the same OS-reconstructed continuum theory.",
    ]
    return {
        "derivation_id": stable_id("formal-derivation", blueprint.get("blueprint_id"), "wilson-os"),
        "target_family": "yang_mills_wilson_os",
        "mathematical_object": "Reflected Wilson Gram quotient near the OS reflection plane.",
        "derivation_label": "Formal Physics Derivation",
        "definitions": definitions,
        "assumptions": assumptions,
        "propositions": propositions,
        "calculations": calculations,
        "unresolved_obligations": obligations,
        "non_claims": blueprint.get("non_claims", []),
    }


def build_generic_derivation(blueprint: dict, units: list[dict]) -> dict:
    source_ids = [row["unit_id"] for row in units[:12]]
    return {
        "derivation_id": stable_id("formal-derivation", blueprint.get("blueprint_id"), "generic"),
        "target_family": "generic_timeline_object",
        "mathematical_object": blueprint.get("primary_mathematical_object") or "active timeline mathematical object",
        "derivation_label": "Formal Mathematical Derivation",
        "definitions": [
            {
                "symbol": "X",
                "text": "The active mathematical object selected by the paper blueprint.",
                "latex": r"X=\text{active object}",
                "valid_when": "The object is source-covered by interpreted report units.",
                "source_unit_ids": source_ids,
            }
        ],
        "assumptions": ["The object and validation handoff are supported by interpreted report units."],
        "propositions": [
            {
                "name": "Scoped local claim",
                "statement": "The paper may claim only the local object-level result licensed by the blueprint.",
                "latex": r"\text{local claim}(X)\not\Rightarrow\text{global target theorem}",
                "proof_steps": ["Separate local evidence from global target commitments.", "State the missing validation handoff explicitly."],
                "valid_when": "No target-preserving transfer proof is available.",
                "source_unit_ids": source_ids,
            }
        ],
        "calculations": [],
        "unresolved_obligations": ["Instantiate a target-specific formal derivation from the interpreted units."],
        "non_claims": blueprint.get("non_claims", []),
    }


def render_tex(report: dict) -> str:
    blocks = [
        rf"\section{{{latex_escape(report.get('derivation_label') or 'Formal Mathematical Derivation')}}}",
        r"\label{sec:formal-derivation}",
        "This section is generated from structured definitions, assumptions, propositions, calculations, and unresolved obligations. It states a local paper-level object and does not claim the global target theorem.",
        r"\subsection{Definitions}",
    ]
    for row in report["definitions"]:
        blocks.append(rf"\paragraph{{{latex_escape(row['symbol'])}.}} {latex_escape(row['text'])}")
        blocks.append("\\[\n" + safe_tex_math(row["latex"]) + "\n\\]")
        blocks.append(rf"\emph{{Valid when:}} {latex_escape(row['valid_when'])}")
    blocks.append(r"\subsection{Assumptions}")
    blocks.append(tex_itemize(report["assumptions"]))
    blocks.append(r"\subsection{Local Propositions}")
    for row in report["propositions"]:
        blocks.append(rf"\paragraph{{{latex_escape(row['name'])}.}} {latex_escape(row['statement'])}")
        blocks.append("\\[\n" + safe_tex_math(row["latex"]) + "\n\\]")
        blocks.append(r"\emph{Proof steps.}")
        blocks.append(tex_itemize(row.get("proof_steps", [])))
        blocks.append(rf"\emph{{Valid when:}} {latex_escape(row['valid_when'])}")
    if report["calculations"]:
        blocks.append(r"\subsection{Worked Calculation Interface}")
        for row in report["calculations"]:
            blocks.append(rf"\paragraph{{{latex_escape(row['name'])}.}} {latex_escape(row['statement'])}")
            blocks.append("\\[\n" + safe_tex_math(row["latex"]) + "\n\\]")
            blocks.append(rf"\emph{{Valid when:}} {latex_escape(row['valid_when'])}")
    blocks.append(r"\subsection{Unresolved Obligations}")
    blocks.append(tex_itemize(report["unresolved_obligations"]))
    blocks.append(r"\subsection{Non-Claims}")
    blocks.append(tex_itemize(report["non_claims"]))
    return "\n\n".join(blocks) + "\n"


def build_report() -> dict:
    blueprint = load_json_object(BLUEPRINT_JSON)
    interpretation = load_json_object(INTERPRETATION_JSON)
    units = interpretation.get("units", [])
    profile = target_profile(blueprint.get("target_id") or interpretation.get("target_id"))
    if profile["target_id"] == "p-vs-np-target":
        body = build_pvsnp_derivation(blueprint, units)
    elif profile["target_id"] == "yang-mills-existence-and-mass-gap-target" or has_wilson_content(units):
        body = build_yang_mills_derivation(blueprint, units)
    else:
        body = build_generic_derivation(blueprint, units)
    body.update(
        {
            "version": 1,
            "generated_utc": utc_now(),
            "target_id": profile["target_id"],
            "target_display_name": profile.get("display_name", profile["target_id"]),
            "schema": rel(SCHEMA),
            "status": "timeline_formal_derivation_ready",
            "source_blueprint": rel(BLUEPRINT_JSON),
            "source_interpretation": rel(INTERPRETATION_JSON),
            "artifacts": {"json": rel(OUT_JSON), "tex": rel(OUT_TEX)},
            "epistemic_status": "formal_derivation_validation_needed",
            "validation_handoff": "python agentic/scripts/validate_timeline_formal_derivation.py",
        }
    )
    body["latex"] = render_tex(body)
    return body


def main() -> int:
    report = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, {key: value for key, value in report.items() if key != "latex"})
    OUT_TEX.write_text(report["latex"], encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_TEX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
