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
"""Build the endpoint kappa_4 incidence certificate for the paper handoff."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state


TARGET_ID = "yang-mills-existence-and-mass-gap-target"
OUT_DIR = ROOT / "agentic/reports/endpoint_incidence_certificate"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    try:
        return int(raw.split("-")[-1])
    except ValueError:
        return 0


def branch_output(cycle: dict[str, Any]) -> dict[str, Any]:
    outputs = cycle.get("branch_outputs", [])
    return outputs[0] if outputs and isinstance(outputs[0], dict) else {}


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if lemmas and isinstance(lemmas[0], dict) else {}


def load_source_cycles() -> list[dict[str, Any]]:
    _, run_state = load_run_state()
    if not run_state:
        return []
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")]
    selected = [cycle for cycle in cycles if 252 <= cycle_number(cycle) <= 254]
    return selected or cycles[-3:]


def verify_seven_point_stencil() -> dict[str, Any]:
    """Verify the seven-point fourth-derivative stencil with exact rational arithmetic."""
    coeffs = {
        -3: Fraction(-1, 6),
        -2: Fraction(2, 1),
        -1: Fraction(-13, 2),
        0: Fraction(28, 3),
        1: Fraction(-13, 2),
        2: Fraction(2, 1),
        3: Fraction(-1, 6),
    }
    moments = {power: sum(coeff * Fraction(k) ** power for k, coeff in coeffs.items()) for power in range(9)}
    # The Taylor coefficient for the first un-cancelled term after the fourth
    # derivative is moment_8 / 8!, so the absolute error is 7*h^4*M_8/240.
    error_coeff = moments[8] / Fraction(40320, 1)
    return {
        "stencil_id": "seven_point_fourth_derivative",
        "coefficients": {str(k): f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator) for k, value in coeffs.items()},
        "moment_checks": {
            str(power): f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)
            for power, value in moments.items()
        },
        "normalizes_fourth_derivative": moments[4] == 24,
        "cancels_orders": [power for power in [0, 1, 2, 3, 5, 6, 7] if moments[power] == 0],
        "first_uncancelled_error_order": 8,
        "signed_error_coefficient": f"{error_coeff.numerator}/{error_coeff.denominator}",
        "absolute_error_bound": "abs(kappa_4 - D_h,7 f) <= (7/240) h^4 M_8",
        "epistemic_status": "exact_rational_verification",
    }


def build_symbolic_dominance_certificate() -> dict[str, Any]:
    weights = {"12": 2, "13": -4, "23": -4}
    return {
        "certificate_id": "endpoint_kappa4_incidence_dominance",
        "null_vector": {"symbol": "z", "value": [1, 1, -2], "valid_when": "z spans the post-H,K Schur-Feshbach null channel of the locked three-hairpin block."},
        "pair_weights": weights,
        "endpoint_cumulant_model": {
            "formula": "kappa_{4,v}(b_ij,v) = -chi_v B_ij,v + epsilon_ij,v",
            "conditions": [
                "chi_v >= 0 is certified in the small heat-kernel endpoint-box regime.",
                "B_ij,v is the nonnegative singlet incidence norm or root-quartic source value for pair ij at endpoint v.",
                "epsilon_ij,v contains image, BCH, transport, and higher-order heat-kernel remainders.",
            ],
            "epistemic_status": "local_asymptotic_certificate_pending_remainders",
        },
        "dominance_functional": {
            "formula": "D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v",
            "dangerous_part": "[D_v]_+ = max(D_v, 0)",
            "safe_condition": "2 B_12,v <= 4 B_13,v + 4 B_23,v",
            "meaning": "Only 12-endpoint dominance can lower the Schur-Feshbach scalar through the leading compact-group endpoint kappa_4 term.",
        },
        "certified_lower_bound": {
            "formula": "S_null >= M_G - C_col sum_v chi_v [D_v]_+ - C_col sum_{v,ij} |w_ij| |epsilon_ij,v| - |E_tail|",
            "color_factor": "C_col = g_a^4/24 * (T_F/N)^2",
            "promotion_condition": "The finite endpoint block passes when the right-hand side is strictly positive in the same regulator window.",
            "falsifier_condition": "A same-theory falsifier requires certified positive dominance whose prefactored size exceeds M_G plus all remainders and tails.",
        },
        "non_claims": [
            "This does not compute the actual three-hairpin endpoint table.",
            "This does not prove OS positivity or a Yang-Mills mass gap.",
            "This certificate is a paper-ready finite calculation target, not a continuum promotion.",
        ],
        "epistemic_status": "symbolic_incidence_certificate",
    }


def build_incidence_table_schema() -> list[dict[str, Any]]:
    rows = []
    for endpoint_class in ["left_boundary_endpoint", "right_boundary_endpoint", "coalesced_corner_endpoint", "tail_interface_endpoint"]:
        rows.append(
            {
                "endpoint_class": endpoint_class,
                "required_entries": ["B_12,v", "B_13,v", "B_23,v", "chi_v", "epsilon_12,v", "epsilon_13,v", "epsilon_23,v", "tail_share"],
                "dominance_to_compute": "D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v",
                "current_status": "geometry_not_yet_enumerated",
                "validation_action": "Draw the regulated plaquette-sheet endpoint box, record oriented pair incidences, compute B_ij,v, then evaluate [D_v]_+.",
            }
        )
    return rows


def source_cycle_cards(cycles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards = []
    for cycle in cycles:
        output = branch_output(cycle)
        lemma = first_lemma(output)
        cards.append(
            {
                "cycle_id": clean_text(cycle.get("cycle_id")),
                "branch_title": clean_text(output.get("branch_title")),
                "learning": clean_text(output.get("mathematical_learning")),
                "next_experiment": clean_text(output.get("next_experiment")),
                "equation_labels": [clean_text(eq.get("label")) for eq in lemma.get("equations", []) if isinstance(eq, dict)],
            }
        )
    return cards


def build_report() -> dict[str, Any]:
    cycles = load_source_cycles()
    source_ids = [clean_text(cycle.get("cycle_id")) for cycle in cycles]
    symbolic = build_symbolic_dominance_certificate()
    stencil = verify_seven_point_stencil()
    table_schema = build_incidence_table_schema()
    return {
        "version": 1,
        "target_id": TARGET_ID,
        "generated_utc": utc_now(),
        "certificate_id": stable_id("endpoint-incidence", TARGET_ID, source_ids, symbolic["dominance_functional"]["formula"]),
        "status": "endpoint_incidence_certificate_ready_geometry_pending",
        "source_cycle_ids": source_ids,
        "source_cycles": source_cycle_cards(cycles),
        "purpose": "Turn the post-H,K endpoint kappa_4 discovery into a paper-checkable finite incidence certificate and an explicit worked-calculation queue.",
        "symbolic_dominance_certificate": symbolic,
        "seven_point_stencil_verification": stencil,
        "incidence_table_schema": table_schema,
        "next_work_queue": [
            {
                "rank": 1,
                "task": "Enumerate actual endpoint boxes for the locked three-hairpin plaquette sheets.",
                "payoff": "Fills the B_12,v, B_13,v, B_23,v table required by the endpoint dominance theorem.",
                "stop_when": "Stop only after every endpoint class has either a certified B-table row or a stated geometry obstruction.",
                "required_skills": ["endpoint-worked-calculation-packager", "dimensional-symmetry-constraint-checker", "next-experiment-queue-ranker"],
            },
            {
                "rank": 2,
                "task": "Evaluate D_+ = sum_v [2B_12,v - 4B_13,v - 4B_23,v]_+ for the enumerated table.",
                "payoff": "Decides whether the compact-group endpoint kappa_4 term is safe, dangerous, or neutral in the actual null channel.",
                "stop_when": "Stop only when the sign and magnitude of every positive-dominance endpoint are accounted for.",
                "required_skills": ["endpoint-worked-calculation-packager", "symbolic-matrix-probe", "next-experiment-queue-ranker"],
            },
            {
                "rank": 3,
                "task": "Certify epsilon_ij,v and E_tail with the seven-point source-derivative or heat-kernel remainder bounds.",
                "payoff": "Turns the symbolic dominance result into a finite paper theorem or a finite falsifier.",
                "stop_when": "Stop only when the interval for S_null is positive, negative, or explicitly too wide to promote.",
                "required_skills": ["analytic-estimate-obligation-builder", "endpoint-worked-calculation-packager", "next-experiment-queue-ranker"],
            },
        ],
        "paper_claim_boundary": {
            "claimable_now": "A finite endpoint kappa_4 incidence certificate: only [D_v]_+ can be dangerous under the stated heat-kernel asymptotic and cancellation assumptions.",
            "not_claimable_yet": "The actual three-hairpin endpoint block passes or fails; the geometric B-table and remainder intervals are still missing.",
            "paper_section_target": "Endpoint kappa_4 incidence dominance theorem and worked-calculation protocol.",
        },
        "validation_handoff": "python agentic/scripts/validate_endpoint_incidence_certificate.py",
    }


def render_markdown(report: dict[str, Any]) -> str:
    cert = report["symbolic_dominance_certificate"]
    dom = cert["dominance_functional"]
    lower = cert["certified_lower_bound"]
    stencil = report["seven_point_stencil_verification"]
    lines = [
        "# Endpoint Incidence Certificate",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Status: `{report['status']}`",
        f"- Source cycles: `{', '.join(report['source_cycle_ids'])}`",
        "",
        "## Dominance Functional",
        "",
        f"- Formula: `{dom['formula']}`",
        f"- Dangerous part: `{dom['dangerous_part']}`",
        f"- Safe condition: `{dom['safe_condition']}`",
        f"- Meaning: {dom['meaning']}",
        "",
        "## Certified Lower Bound",
        "",
        f"- Formula: `{lower['formula']}`",
        f"- Color factor: `{lower['color_factor']}`",
        f"- Promotion: {lower['promotion_condition']}",
        f"- Falsifier: {lower['falsifier_condition']}",
        "",
        "## Seven-Point Stencil",
        "",
        f"- Coefficients: `{stencil['coefficients']}`",
        f"- Moment checks: `{stencil['moment_checks']}`",
        f"- Error bound: `{stencil['absolute_error_bound']}`",
        "",
        "## Incidence Table To Fill",
        "",
    ]
    for row in report["incidence_table_schema"]:
        lines.append(f"### {row['endpoint_class']}")
        lines.append(f"- Entries: `{', '.join(row['required_entries'])}`")
        lines.append(f"- Dominance: `{row['dominance_to_compute']}`")
        lines.append(f"- Status: `{row['current_status']}`")
        lines.append(f"- Validation action: {row['validation_action']}")
        lines.append("")
    lines.extend(["## Next Work Queue", ""])
    for item in report["next_work_queue"]:
        lines.append(f"{item['rank']}. {item['task']}")
        lines.append(f"   - Payoff: {item['payoff']}")
        lines.append(f"   - Stop when: {item['stop_when']}")
    lines.extend(["", "## Claim Boundary", ""])
    for key, value in report["paper_claim_boundary"].items():
        lines.append(f"- `{key}`: {value}")
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
