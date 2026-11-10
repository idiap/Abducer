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
"""Translate PMP symbolic interfaces into analytic estimate obligations."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, stable_id, utc_now, write_json


SYMBOLIC = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
FINITE_INTERFACES = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
OUT_DIR = ROOT / "agentic/reports/analytic_estimate_obligations"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


def obligation(
    key: str,
    title: str,
    mathematical_object: str,
    validity_regime: str,
    formula_dependency: str,
    certifies: str,
    falsifies: str,
    queue_priority: int,
    required_skills: list[str],
) -> dict[str, Any]:
    return {
        "id": f"obl.{key}",
        "title": title,
        "mathematical_object": mathematical_object,
        "validity_regime": validity_regime,
        "source_formula_id": formula_dependency,
        "what_would_certify_it": certifies,
        "what_would_falsify_it": falsifies,
        "epistemic_status": "analytic_obligation",
        "queue_priority": queue_priority,
        "required_skills": required_skills,
        "transfer_boundary": "The obligation can connect finite algebra to Yang-Mills only if it is proved in the same reflected Wilson observable algebra and survives the continuum transfer regime.",
    }


def build_report() -> dict[str, Any]:
    symbolic = load_json_object(SYMBOLIC)
    finite = load_json_object(FINITE_INTERFACES) if FINITE_INTERFACES.exists() else {}
    finite_packets = finite.get("packets", []) if isinstance(finite.get("packets"), list) else []
    finite_packet = finite_packets[0] if finite_packets else {}
    source_cycles = finite_packet.get("source_cycle_ids") or symbolic.get("source_cycle_ids", [])
    obligations = [
        obligation(
            "boundary-ope-factor-extraction",
            "Extract boundary OPE quotient factors",
            "B_ij factors induced by collar-collapse products of reflected Wilson observables",
            "reflection-plane collar collapse after fixed finite-family positivity is typed",
            "id.det-normalized-hermitian-3x3",
            "Uniformly defined B_ij enter the normalized quotient without untracked contact leakage.",
            "B_ij is regulator-family dependent or cannot be realized in the same observable algebra.",
            96,
            ["physics-regime-map-builder", "limit-convergence-behavior-auditor", "abducer-obligation-gatekeeper"],
        ),
        obligation(
            "additive-contact-control",
            "Control additive contact terms",
            "C_ij additive contact terms in reflected finite families",
            "continuum transfer of Wilson hairpin collar observables",
            "id.det-normalized-hermitian-3x3",
            "Contacts vanish, are positive in the needed cone, or are absorbed into a certified quotient normalization.",
            "Contacts shift the finite determinant sign or invalidate pairwise-to-family transfer.",
            94,
            ["limit-convergence-behavior-auditor", "qualitative-physics-falsifier", "entailment-gap-auditor"],
        ),
        obligation(
            "quotient-phase-coboundary-control",
            "Prove quotient phase is controlled or name the obstruction",
            "Phi = arg(Q_12 Q_23 Q_31)",
            "finite Wilson hairpin quotient family with diagonal rephasing freedom",
            "id.rephasing-holonomy",
            "Phi is a coboundary removable by diagonal rephasing or is bounded so the determinant remains nonnegative.",
            "A non-removable holonomy makes det(Q) negative in an admissible finite family.",
            99,
            ["monotonicity-sensitivity-prober", "dimensional-symmetry-constraint-checker", "qualitative-physics-falsifier"],
        ),
        obligation(
            "modulus-quotient-psd",
            "Prove real modulus quotient positivity",
            "real matrix of quotient moduli rho_ij",
            "finite reflected observable family before continuum promotion",
            "id.principal-minors",
            "All principal minors of the modulus quotient satisfy the PSD inequalities needed by the bridge.",
            "Pairwise bounds hold while the three-by-three determinant is negative.",
            93,
            ["qualitative-toy-model-builder", "abducer-obligation-gatekeeper", "entailment-gap-auditor"],
        ),
        obligation(
            "same-theory-observable-realization",
            "Realize the quotient matrix in the same Yang-Mills observable algebra",
            "Q_ij generated by gauge-invariant reflected Wilson observables",
            "OS-positive continuum Schwinger-function reconstruction candidate",
            "id.det-normalized-hermitian-3x3",
            "The finite quotient carrier is not a proxy: it comes from the same theory and same limiting observable sector.",
            "The matrix is only an analogy or fixed-cutoff artifact and cannot update proof status.",
            100,
            ["abducer-obligation-gatekeeper", "kb-end-to-end-proof-critic", "review-reasoner-epistemologist"],
        ),
        obligation(
            "finite-family-observable-density",
            "Prove finite-family observable density is not lost",
            "finite reflected Wilson observable families used to form quotient matrices",
            "OS-positive continuum candidate before spectral promotion",
            "carrier.quotient_3x3",
            "The finite families used by the quotient interface approximate a dense gauge-invariant excitation sector after reconstruction.",
            "The quotient carrier sees only a thin proxy sector and cannot control the target spectral problem.",
            91,
            ["abducer-obligation-gatekeeper", "entailment-gap-auditor", "long-horizon-route-portfolio-manager"],
        ),
    ]
    finite_classes = {
        item.get("class")
        for item in finite_packet.get("analytic_obligations", [])
        if isinstance(item, dict)
    }
    for item in obligations:
        if item["id"].endswith("boundary-ope-factor-extraction"):
            item["obligation_class"] = "boundary_ope_estimate"
        elif item["id"].endswith("additive-contact-control"):
            item["obligation_class"] = "contact_control"
        elif item["id"].endswith("quotient-phase-coboundary-control"):
            item["obligation_class"] = "phase_coboundary_control"
        elif item["id"].endswith("modulus-quotient-psd"):
            item["obligation_class"] = "modulus_psd_control"
        elif item["id"].endswith("same-theory-observable-realization"):
            item["obligation_class"] = "same_theory_realization"
        else:
            item["obligation_class"] = "observable_density"
        item["finite_interface_dependency"] = finite_packet.get("packet_id", "")
        item["source_side_conditions"] = [condition.get("id") for condition in finite_packet.get("side_conditions", []) if isinstance(condition, dict)]
    queue = [
        {
            "queue_id": stable_id("pmp.queue", item["id"], item["queue_priority"]),
            "source_obligation_id": item["id"],
            "next_experiment": item["title"],
            "priority_score": item["queue_priority"],
            "priority_band": "high" if item["queue_priority"] >= 90 else "medium",
            "payoff_criteria": [
                item["what_would_certify_it"],
                item["what_would_falsify_it"],
                "The result must keep finite algebra separate from same-theory analytic transfer.",
            ],
            "required_skills": sorted(set(item["required_skills"] + ["next-experiment-queue-ranker"])),
            "epistemic_status": "analytic_obligation",
        }
        for item in sorted(obligations, key=lambda row: row["queue_priority"], reverse=True)
    ]
    return {
        "version": 1,
        "target_id": symbolic["target_id"],
        "generated_utc": utc_now(),
        "source_artifacts": [str(SYMBOLIC.relative_to(ROOT))],
        "finite_interface_artifacts": [str(FINITE_INTERFACES.relative_to(ROOT))] if finite_packet else [],
        "source_cycle_ids": source_cycles,
        "status": "analytic_obligations_ready",
        "symbolic_formula_count": len(symbolic.get("identities", [])),
        "finite_interface_packet_count": len(finite_packets),
        "finite_interface_obligation_classes": sorted(finite_classes),
        "obligations": obligations,
        "next_experiment_queue_items": queue,
        "proof_safety": {
            "numeric_results_promote_proof": False,
            "finite_matrix_algebra_is_proof": False,
            "required_transfer_certificate": "same-theory reflected Wilson observable realization plus continuum-uniform estimate",
        },
        "validation_handoff": "python agentic/scripts/validate_analytic_estimate_obligations.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Analytic Estimate Obligations",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Status: `{report['status']}`",
        "",
    ]
    for item in report["obligations"]:
        lines.append(f"## {item['title']}")
        lines.append(f"- Object: {item['mathematical_object']}")
        lines.append(f"- Regime: {item['validity_regime']}")
        lines.append(f"- Certifies: {item['what_would_certify_it']}")
        lines.append(f"- Falsifies: {item['what_would_falsify_it']}")
        lines.append(f"- Status: `{item['epistemic_status']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
