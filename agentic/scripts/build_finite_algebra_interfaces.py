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
"""Build non-Lean finite algebra interface packets for ESR."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state


OUT_DIR = ROOT / "agentic/reports/finite_algebra_interfaces"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
SYMBOLIC_PROBE = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def backend_name() -> str:
    try:
        import sympy as sp  # type: ignore

        return f"sympy-{sp.__version__}"
    except Exception:
        return "manual_fallback"


def source_cycles() -> list[str]:
    _, run_state = load_run_state()
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")] if run_state else []
    selected = []
    for cycle in cycles:
        raw = clean_text(cycle.get("cycle_id", "cycle-0000"))
        try:
            number = int(raw.split("-")[-1])
        except ValueError:
            number = 0
        if 198 <= number <= 205:
            selected.append(raw)
    return selected or [clean_text(cycle.get("cycle_id")) for cycle in cycles[-8:]] or ["cycle-window-unavailable"]


def build_packet() -> dict[str, Any]:
    symbolic = load_optional_json(SYMBOLIC_PROBE)
    backend = symbolic.get("symbolic_backend") or backend_name()
    cycles = symbolic.get("source_cycle_ids") or source_cycles()
    exact_identities = symbolic.get("identities") or [
        {
            "id": "id.det-normalized-hermitian-3x3",
            "name": "normalized Hermitian three-by-three determinant",
            "formula": "det(Q)=1-rho12^2-rho23^2-rho13^2+2*rho12*rho23*rho13*cos(Phi)",
            "latex": r"\det Q = 1-\rho_{12}^{2}-\rho_{23}^{2}-\rho_{13}^{2}+2\rho_{12}\rho_{23}\rho_{13}\cos\Phi",
            "valid_when": "Q is normalized Hermitian with diagonal one and Phi=arg(Q_12 Q_23 Q_31).",
            "derivation_method": "manual finite determinant expansion",
            "epistemic_status": "symbolic_formula",
        }
    ]
    for identity in exact_identities:
        identity.setdefault("symbolic_backend", backend)
        identity.setdefault("epistemic_status", "symbolic_formula")
    packet = {
        "packet_id": stable_id("esr.interface", TARGET_ID, "quotient-3x3", cycles),
        "target_id": TARGET_ID,
        "source_cycle_ids": cycles,
        "created_utc": utc_now(),
        "carrier": {
            "id": "carrier.quotient_3x3",
            "name": "normalized Hermitian three-observable quotient matrix",
            "mathematical_type": "finite 3x3 Hermitian matrix interface",
            "scope": "finite reflected observable family before continuum or spectral promotion",
            "validity_boundary": "The carrier is finite algebra only; it becomes Yang-Mills-relevant only through same-theory observable realization and continuum-uniform analytic estimates.",
        },
        "variables": [
            {"symbol": "Q", "meaning": "normalized quotient Gram matrix", "domain": "Hermitian 3x3 matrices with diagonal one", "held_fixed_or_varied": "carrier"},
            {"symbol": "rho_ij", "meaning": "modulus of Q_ij", "domain": "0 <= rho_ij <= 1 when 2x2 minors are nonnegative", "held_fixed_or_varied": "varied"},
            {"symbol": "Phi", "meaning": "cycle holonomy arg(Q_12 Q_23 Q_31)", "domain": "R / 2*pi Z", "held_fixed_or_varied": "varied"},
            {"symbol": "D", "meaning": "diagonal unitary rephasing", "domain": "U(1)^3 modulo global phase", "held_fixed_or_varied": "gauge freedom"},
        ],
        "exact_identities": exact_identities,
        "side_conditions": [
            {"id": "side.hermitian", "condition": "Q=Q*", "why_needed": "PSD and principal minors are Hermitian matrix notions.", "failure_effect": "The determinant formula no longer licenses positivity conclusions."},
            {"id": "side.normalized-diagonal", "condition": "Q_ii=1", "why_needed": "The determinant formula is normalized by the diagonal Gram entries.", "failure_effect": "Additional scale factors enter all minors and quotient comparisons."},
            {"id": "side.nonzero-quotient-entries", "condition": "quotient denominators are nonzero", "why_needed": "Schur/Hadamard quotient and phase variables must be defined.", "failure_effect": "The interface must backtrack to support-restricted or regularized quotient definitions."},
            {"id": "side.phase-convention", "condition": "Phi=arg(Q_12 Q_23 Q_31) modulo diagonal rephasing", "why_needed": "Only the cycle product phase is invariant under local diagonal phase choices.", "failure_effect": "A coordinate phase may be mistaken for a real obstruction."},
            {"id": "side.finite-family-scope", "condition": "all entries come from one finite reflected observable family", "why_needed": "Mixing carriers would turn the determinant test into an analogy.", "failure_effect": "The packet is quarantined as proxy algebra."},
        ],
        "falsifier_templates": [
            {
                "id": "fals.det-negative-pairwise-pass",
                "epistemic_status": "falsifier_shape",
                "preserved_assumptions": ["Q=Q*", "Q_ii=1", "0 <= rho_ij <= 1"],
                "changed_condition": "Phi or the three moduli make det(Q)<0",
                "disconfirming_observation": "pairwise minors pass while the 3x3 determinant is negative",
                "branch_control_effect": "Demote any route claiming pairwise quotient damping implies finite-family positivity.",
                "numeric_search_allowed": "only as bounded falsifier selection after the symbolic formula is recorded",
            },
            {
                "id": "fals.nonzero-cycle-holonomy",
                "epistemic_status": "falsifier_shape",
                "preserved_assumptions": ["same support graph", "diagonal unitary rephasing allowed"],
                "changed_condition": "cycle product phase is not a coboundary",
                "disconfirming_observation": "no diagonal D removes all quotient phases on the support graph",
                "branch_control_effect": "Require a phase-control lemma before Schur quotient positivity transfer.",
                "numeric_search_allowed": "not needed for the algebraic coboundary obstruction",
            },
            {
                "id": "fals.modulus-quotient-minor-negative",
                "epistemic_status": "falsifier_shape",
                "preserved_assumptions": ["phase removed or ignored", "real modulus quotient formed"],
                "changed_condition": "a higher principal minor of the modulus quotient is negative",
                "disconfirming_observation": "real pairwise bounds do not produce PSD modulus quotient",
                "branch_control_effect": "Backtrack from modulus-only positivity transfer to analytic PSD estimates.",
                "numeric_search_allowed": "bounded search allowed only to rank which minor/family is sharpest",
            },
            {
                "id": "fals.additive-contact-nonzero",
                "epistemic_status": "falsifier_shape",
                "preserved_assumptions": ["finite reflected observable family", "collar-collapse setup"],
                "changed_condition": "additive contact term C_ij survives normalization",
                "disconfirming_observation": "the quotient identity fails to represent the continuum carrier without extra contact terms",
                "branch_control_effect": "Route next work to contact-control estimates rather than determinant algebra.",
                "numeric_search_allowed": "no; this is an analytic same-theory estimate obligation",
            },
        ],
        "analytic_obligations": [
            {"id": "obl.same-theory-observable-realization", "class": "same_theory_realization", "source_formula_id": "id.det-normalized-hermitian-3x3", "target_relevance": "prevents the finite matrix from being a proxy"},
            {"id": "obl.quotient-phase-coboundary-control", "class": "phase_coboundary_control", "source_formula_id": "id.rephasing-holonomy", "target_relevance": "decides whether holonomy blocks positivity transfer"},
            {"id": "obl.boundary-ope-factor-extraction", "class": "boundary_ope_estimate", "source_formula_id": "id.det-normalized-hermitian-3x3", "target_relevance": "connects collar-collapse data to quotient entries"},
            {"id": "obl.additive-contact-control", "class": "contact_control", "source_formula_id": "id.det-normalized-hermitian-3x3", "target_relevance": "prevents contact terms from changing determinant sign"},
            {"id": "obl.modulus-quotient-psd", "class": "modulus_psd_control", "source_formula_id": "id.principal-minors", "target_relevance": "tests whether modulus-only transfer is enough"},
        ],
        "non_claims": [
            "This packet is not Lean checked.",
            "This packet is not theorem-prover output.",
            "This packet is not continuum Yang-Mills proof progress.",
            "This packet is not a simulation.",
            "This packet does not prove a mass gap.",
        ],
        "epistemic_status": "equational_interface",
        "validation_handoff": "python agentic/scripts/validate_finite_algebra_interfaces.py",
    }
    return packet


def render_markdown(report: dict[str, Any]) -> str:
    packet = report["packets"][0]
    lines = [
        "# Finite Algebra Interfaces",
        "",
        f"- Target: `{packet['target_id']}`",
        f"- Packet: `{packet['packet_id']}`",
        f"- Status: `{packet['epistemic_status']}`",
        f"- Carrier: {packet['carrier']['name']}",
        "",
        "## Exact Identities",
        "",
    ]
    for identity in packet["exact_identities"]:
        lines.append(f"### {identity['name']}")
        lines.append(f"\\[{identity['latex']}\\]")
        lines.append(f"- Valid when: {identity['valid_when']}")
        lines.append(f"- Backend: `{identity['symbolic_backend']}`")
        lines.append("")
    lines.extend(["## Side Conditions", ""])
    for condition in packet["side_conditions"]:
        lines.append(f"- `{condition['id']}` {condition['condition']}: {condition['why_needed']}")
    lines.extend(["", "## Formula-Derived Falsifier Shapes", ""])
    for falsifier in packet["falsifier_templates"]:
        lines.append(f"- `{falsifier['id']}`: {falsifier['disconfirming_observation']} -> {falsifier['branch_control_effect']}")
    lines.extend(["", "## Non-Claims", ""])
    for claim in packet["non_claims"]:
        lines.append(f"- {claim}")
    return "\n".join(lines) + "\n"


def main() -> int:
    packet = build_packet()
    report = {
        "version": 1,
        "generated_utc": utc_now(),
        "status": "ready",
        "packets": [packet],
        "summary": {
            "packet_count": 1,
            "identity_count": len(packet["exact_identities"]),
            "side_condition_count": len(packet["side_conditions"]),
            "falsifier_template_count": len(packet["falsifier_templates"]),
            "analytic_obligation_count": len(packet["analytic_obligations"]),
            "proof_safe": True,
        },
        "validation_handoff": "python agentic/scripts/validate_finite_algebra_interfaces.py",
    }
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
