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
"""Build exact symbolic finite-matrix probes for the PMP layer."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state


OUT_DIR = ROOT / "agentic/reports/symbolic_matrix_probe"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def optional_backend() -> dict[str, Any]:
    try:
        import sympy as sp  # type: ignore

        rho12, rho23, rho13, phi = sp.symbols("rho12 rho23 rho13 Phi", real=True)
        q12 = rho12
        q23 = rho23
        q31 = rho13 * sp.exp(sp.I * phi)
        matrix = sp.Matrix(
            [
                [1, q12, sp.conjugate(q31)],
                [q12, 1, q23],
                [q31, q23, 1],
            ]
        )
        determinant = sp.simplify(sp.expand(matrix.det().rewrite(sp.cos)))
        return {
            "backend": f"sympy-{sp.__version__}",
            "derivation_note": "Symbolically computed as the determinant of a normalized Hermitian quotient matrix.",
            "raw_backend_formula": str(determinant),
        }
    except Exception as exc:  # pragma: no cover - environment dependent
        return {
            "backend": "manual_fallback",
            "derivation_note": f"SymPy unavailable or unsuitable; used exact known three-by-three Hermitian determinant formula ({exc}).",
            "raw_backend_formula": "",
        }


def source_cycles() -> list[str]:
    _, run_state = load_run_state()
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")] if run_state else []
    selected = [clean_text(cycle.get("cycle_id")) for cycle in cycles if 198 <= int(clean_text(cycle.get("cycle_id", "cycle-0000")).split("-")[-1] or 0) <= 205]
    return selected or [clean_text(cycle.get("cycle_id")) for cycle in cycles[-8:]] or ["cycle-window-unavailable"]


def build_report() -> dict[str, Any]:
    backend = optional_backend()
    cycles = source_cycles()
    determinant_latex = r"1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}+2\rho_{12}\rho_{23}\rho_{13}\cos\Phi"
    packet = {
        "version": 1,
        "target_id": TARGET_ID,
        "generated_utc": utc_now(),
        "source_cycle_ids": cycles,
        "status": "symbolic_formula",
        "symbolic_backend": backend["backend"],
        "probe_decision": {
            "packet_id": stable_id("pmp.decision", TARGET_ID, "three-hairpin-quotient"),
            "target_id": TARGET_ID,
            "decision": "derive_symbolically",
            "carrier": {
                "name": "three-observable normalized Hermitian quotient matrix",
                "mathematical_type": "finite 3x3 Hermitian PSD interface",
                "variables": ["rho12", "rho23", "rho13", "Phi"],
                "validity_conditions": [
                    "Q is Hermitian.",
                    "Q_ii = 1 for i in {1,2,3}.",
                    "Q_ij = rho_ij exp(i theta_ij) with 0 <= rho_ij <= 1.",
                    "Phi = arg(Q_12 Q_23 Q_31) is invariant under diagonal rephasing.",
                ],
            },
            "question": "When do pairwise normalized quotient moduli and holonomy give a positive finite Gram interface?",
            "symbolic_first_attempt": {
                "available": True,
                "method": backend["backend"],
                "expected_output": "determinant, pairwise minors, holonomy, and falsifier inequalities",
                "why_sufficient_or_not": "It fully types the finite algebra interface, but leaves Yang-Mills analytic realization and uniform estimates open.",
            },
            "analytic_estimate_target": {
                "needed": True,
                "objects": ["boundary OPE factors", "additive contacts", "quotient phase", "modulus quotient minors", "same-theory observable realization"],
                "certifies": "The finite quotient interface is realized by reflected Wilson observables in the continuum transfer regime.",
                "falsifies": "A negative determinant, non-removable quotient holonomy, or failed same-theory realization blocks the positivity bridge.",
            },
            "numeric_probe_if_needed": {
                "allowed": False,
                "bounded_domain": [],
                "stopping_condition": "No numeric search is needed for the exact determinant.",
                "expected_decision_value": "Numeric search may later calibrate sharp phase/modulus bounds only after analytic obligations are named.",
                "non_proof_boundary": "A numeric sample is never Yang-Mills proof progress.",
            },
            "dependencies": ["docs/research-methods/parsimonious-probe-policy.md", "agentic/spec/parsimonious_probe_decision.schema.json"],
            "transfer_boundary": "Finite matrix algebra supplies a bridge interface, not a construction of continuum Yang-Mills or a spectral gap.",
            "epistemic_status": "symbolic_formula",
            "source_cycle_ids": cycles,
            "validation_handoff": "python agentic/scripts/validate_symbolic_matrix_probe.py",
        },
        "identities": [
            {
                "id": "id.det-normalized-hermitian-3x3",
                "name": "normalized Hermitian three-by-three determinant",
                "latex": rf"\det Q = {determinant_latex}",
                "formula": "det(Q)=1-rho12^2-rho23^2-rho13^2+2*rho12*rho23*rho13*cos(Phi)",
                "valid_when": "Q is a normalized Hermitian 3x3 quotient matrix, 0 <= rho_ij <= 1, and Phi is the gauge-invariant cycle phase arg(Q_12 Q_23 Q_31).",
                "derivation_method": backend["derivation_note"],
                "epistemic_status": "symbolic_formula",
            },
            {
                "id": "id.principal-minors",
                "name": "pairwise minor constraints",
                "latex": r"1-\rho_{ij}^{2}\ge 0\quad(1\le i<j\le3)",
                "formula": "rho_ij <= 1 for every pair",
                "valid_when": "Each two-by-two principal minor of Q is required to be nonnegative.",
                "derivation_method": "principal minor expansion",
                "epistemic_status": "symbolic_formula",
            },
            {
                "id": "id.rephasing-holonomy",
                "name": "diagonal rephasing invariant",
                "latex": r"\Phi=\arg(Q_{12}Q_{23}Q_{31})",
                "formula": "Phi=theta12+theta23+theta31 modulo 2*pi",
                "valid_when": "Q is compared modulo diagonal unitary rephasings DQD*.",
                "derivation_method": "cycle-product invariance under vertex phase cancellation",
                "epistemic_status": "symbolic_formula",
            },
        ],
        "falsifier_templates": [
            {
                "id": "fals.det-negative",
                "condition": "pairwise minors hold but det(Q) < 0",
                "latex": rf"1-\rho_{{12}}^2-\rho_{{23}}^2-\rho_{{13}}^2+2\rho_{{12}}\rho_{{23}}\rho_{{13}}\cos\Phi < 0",
                "decision_effect": "Demote any branch claiming pairwise quotient positivity suffices for finite-family positivity.",
            },
            {
                "id": "fals.nonzero-holonomy",
                "condition": "Phi is not 0 modulo pi after diagonal rephasing",
                "latex": r"\Phi\not\equiv 0\pmod{\pi}",
                "decision_effect": "Require phase-control or coboundary lemma before Schur quotient positivity transfer.",
            },
        ],
        "analytic_obligation_seeds": [
            "boundary OPE coefficient extraction for B_ij",
            "additive contact term control for C_ij",
            "same-theory quotient phase control for Phi",
            "modulus quotient PSD estimates",
            "observable realization in the reflected Wilson algebra",
        ],
        "non_claims": [
            "This is not a Yang-Mills existence proof.",
            "This does not establish a continuum Hilbert space.",
            "This does not prove a spectral gap.",
            "This is not a simulation.",
        ],
        "validation_handoff": "python agentic/scripts/validate_symbolic_matrix_probe.py",
    }
    return packet


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Symbolic Matrix Probe",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Status: `{report['status']}`",
        f"- Backend: `{report['symbolic_backend']}`",
        "",
        "## Exact Interfaces",
        "",
    ]
    for identity in report["identities"]:
        lines.append(f"### {identity['name']}")
        lines.append(f"\\[{identity['latex']}\\]")
        lines.append(f"- Valid when: {identity['valid_when']}")
        lines.append(f"- Status: `{identity['epistemic_status']}`")
        lines.append("")
    lines.extend(["## Falsifier Templates", ""])
    for item in report["falsifier_templates"]:
        lines.append(f"- `{item['id']}`: {item['condition']} ({item['decision_effect']})")
    lines.extend(["", "## Non-Claims", ""])
    for item in report["non_claims"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
