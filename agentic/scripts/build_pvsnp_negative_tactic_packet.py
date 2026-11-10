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
"""Build route-specific negative tactic guidance for P vs NP marathon branches."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, stable_id, utc_now, write_json
from discovery_marathon_common import load_branches, load_cycles, load_run_state, write_markdown


TARGET_ID = "p-vs-np-target"
OUT_DIR = ROOT / "agentic/reports/pvsnp_negative_tactics"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
PRESSURE_BRIDGES = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
CONTRIBUTION_MONITOR = ROOT / "agentic/reports/scientific_contribution_monitor/latest.json"


ROUTE_MARKERS = [
    (
        "black_box_substitution_or_hardness_magnification",
        ["black-box", "black box", "magnification", "beta", "query", "exponent", "threshold", "barely"],
    ),
    (
        "padding_projection_or_sparse_valid_length",
        ["padding", "projection", "sparse", "valid length", "valid-length", "length map", "demagnification"],
    ),
    (
        "natural_property_or_combinatorial_lower_bound",
        ["natural", "largeness", "constructivity", "useful", "property", "pseudorandom", "prf"],
    ),
    (
        "mcsp_mktp_or_meta_complexity_carrier",
        ["mcsp", "mktp", "meta-complexity", "truth table", "row", "certificate", "kolmogorov"],
    ),
    (
        "proof_complexity_transfer",
        ["proof complexity", "proof-complexity", "resolution", "frege", "tautology", "proof system", "gaussian"],
    ),
]


FAMILY_GUIDANCE: dict[str, dict[str, Any]] = {
    "black_box_substitution_or_hardness_magnification": {
        "tactic_mode": "impossibility_theorem",
        "reason": "The decisive issue is whether positive target-query exponent beta and overhead q cap the transfer before it reaches all SAT exponents.",
        "method_class": "black-box target-circuit substitution interfaces with source size N, target query length n^beta, and overhead N^q",
        "carrier": "the transfer inequality SAT in SIZE(n^c) => source carrier in SIZE(N^{q+beta c+o(1)})",
        "conflict": "claimed all-exponent exclusion for NP not subset P/poly despite positive beta",
        "escape_conditions": [
            "beta=0 or genuinely subpolynomial target-query length",
            "a nonblackbox use of the SAT circuit not summarized by query exponent beta",
            "a source lower bound stronger than the transferred upper-bound window",
        ],
        "proof_obligations": [
            "Compute beta and q for the named carrier, including all padding and decoding overhead.",
            "Derive the exact exponent window q+beta*c+o(1) and identify which SAT exponents survive.",
            "Record relativization, algebrization, natural-proofs, and advice status for this interface.",
        ],
    },
    "padding_projection_or_sparse_valid_length": {
        "tactic_mode": "proof_by_contradiction",
        "reason": "The branch should test whether padding or projection merely relocates SAT hardness to sparse valid lengths.",
        "method_class": "projection/padding carriers that map target instances of length n into source objects of length N=n^k or sparse valid lengths",
        "carrier": "the assumed SAT circuit upper bound transported through the padding/projection map",
        "conflict": "a claimed weak-source lower bound that would imply NP not subset P/poly without paying sparse-valid-length hardness",
        "escape_conditions": [
            "a nonprojection carrier with target-preserving compression",
            "a uniform valid-length recognition theorem with no uncharged advice",
            "a source lower bound that is not equivalent to the target lower bound after unpadding",
        ],
        "proof_obligations": [
            "State the padding map, valid-length set, and unpadding circuit size exactly.",
            "Assume SAT in SIZE(n^c) and compute the induced source upper bound as a function of N.",
            "Show whether the contradiction uses the same target class and advice regime.",
        ],
    },
    "natural_property_or_combinatorial_lower_bound": {
        "tactic_mode": "impossibility_theorem",
        "reason": "The key question is whether the proposed lower-bound property is simultaneously large, constructive, and useful.",
        "method_class": "large constructive useful properties for the exact circuit class targeted by the branch",
        "carrier": "the natural-proofs tuple: largeness, constructivity, usefulness, and pseudorandom-function tension",
        "conflict": "cryptographic hardness or PRF assumptions for a class that the property claims to separate",
        "escape_conditions": [
            "non-large property",
            "nonconstructive or semantic property outside the efficient recognition requirement",
            "proof-system-specific object whose usefulness does not induce a large property of truth tables",
        ],
        "proof_obligations": [
            "Define the property and the circuit class against which it is useful.",
            "Estimate largeness/density and constructivity time.",
            "State the PRF or cryptographic assumption needed for the natural-proofs pressure.",
        ],
    },
    "mcsp_mktp_or_meta_complexity_carrier": {
        "tactic_mode": "falsifier_search",
        "reason": "The live risk is that a meta-complexity carrier supplies aggregate or advice-selected hardness rather than a uniform language lower bound.",
        "method_class": "MCSP/MKtP certificate carriers, hard-row selectors, and truth-table ranking mechanisms",
        "carrier": "row-hardness or certificate selection mechanism and its advice/uniformity ledger",
        "conflict": "claim of language hardness from a carrier that may only identify nonuniform hard rows",
        "escape_conditions": [
            "explicit advice-free row-hard certificate",
            "searchable certificate within the intended target class",
            "density control that avoids natural-property largeness pressure",
        ],
        "proof_obligations": [
            "Name the truth-table family, row selector, verifier, and certificate size.",
            "Check whether selection uses advice, ranking, or nonuniform hard-string choice.",
            "Test easy sparse tables and low-complexity rows as falsifiers.",
        ],
    },
    "proof_complexity_transfer": {
        "tactic_mode": "proof_by_contradiction",
        "reason": "The branch must determine whether proof-system hardness transfers to language hardness or remains a fixed-family proof lower bound.",
        "method_class": "proof-complexity carriers with verifier overhead and semantic transfer claims",
        "carrier": "proof-length lower bound plus semantic soundness bridge to SAT circuit lower bounds",
        "conflict": "shortcut proof families, recognition algorithms, Gaussian-elimination bypasses, or semantic targets that do not imply circuit lower bounds",
        "escape_conditions": [
            "typed proof system with a proven semantic bridge",
            "shortcut model explicitly excluded by the theorem hypotheses",
            "verifier overhead bounded inside the target class without advice leakage",
        ],
        "proof_obligations": [
            "State the proof system, formula family, proof-size bound, and semantic target.",
            "Test known shortcuts or algebraic/proof-recognition algorithms.",
            "Prove that the transfer reaches SAT circuit lower bounds rather than only proof lower bounds.",
        ],
    },
    "unclassified_pvsnp_pressure": {
        "tactic_mode": "constructive_bridge",
        "reason": "The branch has not yet typed its source object, target class, transfer interface, and obstruction family.",
        "method_class": "untyped P vs NP branch requiring pressure localization",
        "carrier": "none yet; construct the source object, target object, model, and route family first",
        "conflict": "none accepted until the branch names a target-preserving conflict target",
        "escape_conditions": [
            "classify the route family",
            "name a source object and target class",
            "state a computable parameter or finite falsifier",
        ],
        "proof_obligations": [
            "Run conceptual pressure localization before contradiction rhetoric.",
            "Extract the transfer theorem shape and barrier status.",
            "Only then choose contradiction, no-go theorem, falsifier search, or quarantine.",
        ],
    },
}


def route_family_from_text(text: str) -> str:
    lower = text.lower()
    for family, markers in ROUTE_MARKERS:
        if any(marker in lower for marker in markers):
            return family
    return "unclassified_pvsnp_pressure"


def route_family_for_branch(branch: dict[str, Any], local_text: str) -> str:
    branch_text = clean_text(
        {
            "title": branch.get("title", ""),
            "controlled_interface": branch.get("controlled_interface", ""),
            "hypothesis": branch.get("hypothesis", ""),
            "mathematical_mechanism": branch.get("mathematical_mechanism", ""),
            "dependencies": branch.get("dependencies", []),
        }
    ).lower()
    if any(term in branch_text for term in ["mcsp", "mktp", "meta-complexity", "truth table", "certificate"]):
        return "mcsp_mktp_or_meta_complexity_carrier"
    if any(term in branch_text for term in ["proof complexity", "proof-complexity", "resolution", "frege", "tautology", "proof system"]):
        return "proof_complexity_transfer"
    if any(term in branch_text for term in ["natural", "relativization", "algebrization", "barrier", "oracle"]):
        return "natural_property_or_combinatorial_lower_bound"
    if any(term in branch_text for term in ["padding", "projection", "valid length", "sparse valid"]):
        return "padding_projection_or_sparse_valid_length"
    if any(term in branch_text for term in ["magnification", "threshold", "beta", "weak lower bound", "barely"]):
        return "black_box_substitution_or_hardness_magnification"
    return route_family_from_text(local_text)


def tactic_mode_from_branch(text: str, family: str, blockers: int) -> str:
    lower = text.lower()
    if blockers >= 2 and family != "unclassified_pvsnp_pressure":
        return "impossibility_theorem"
    if "counterexample" in lower:
        return "falsifier_search"
    if family == "mcsp_mktp_or_meta_complexity_carrier" and any(term in lower for term in ["easy sparse", "advice leak", "advice leakage", "low-complexity row"]):
        return "falsifier_search"
    if family == "proof_complexity_transfer" and any(term in lower for term in ["gaussian shortcut", "semantic bypass", "recognition algorithm"]):
        return "falsifier_search"
    if any(term in lower for term in ["assume", "contradict", "derive upper bound", "proof by contradiction"]):
        return "proof_by_contradiction"
    return clean_text(FAMILY_GUIDANCE[family]["tactic_mode"])


def latest_outputs_for_branch(cycles: list[dict[str, Any]], branch_id: str, limit: int = 3) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for cycle in reversed(cycles):
        for output in cycle.get("branch_outputs", []):
            if isinstance(output, dict) and output.get("branch_id") == branch_id:
                hits.append({"cycle_id": cycle.get("cycle_id", ""), "output": output})
                break
        if len(hits) >= limit:
            break
    return list(reversed(hits))


def recommendation_for_branch(
    branch: dict[str, Any],
    cycles: list[dict[str, Any]],
    pressure_bridge: dict[str, Any],
    contribution_monitor: dict[str, Any],
) -> dict[str, Any]:
    branch_id = clean_text(branch.get("branch_id"))
    recent = latest_outputs_for_branch(cycles, branch_id)
    branch_local_text = clean_text(
        {
            "branch": branch,
            "recent_outputs": [row["output"] for row in recent],
        }
    )
    context_text = clean_text(
        {
            "pressure_bridge": pressure_bridge,
            "contribution_monitor": contribution_monitor,
        }
    )
    family = route_family_for_branch(branch, branch_local_text)
    guidance = FAMILY_GUIDANCE[family]
    blockers = int(branch.get("consecutive_low_learning_cycles", 0) or 0)
    tactic_mode = tactic_mode_from_branch(branch_local_text, family, blockers)
    if tactic_mode == clean_text(guidance["tactic_mode"]) and "near_stepping_stone" in context_text and family != "unclassified_pvsnp_pressure":
        tactic_mode = clean_text(guidance["tactic_mode"])
    if family == "unclassified_pvsnp_pressure" and blockers >= 2:
        tactic_mode = "backtrack"
    branch_control = {
        "constructive_bridge": "persist_adapt",
        "proof_by_contradiction": "persist_adapt",
        "impossibility_theorem": "pivot_to_scoped_no_go",
        "falsifier_search": "persist_with_falsifier_test",
        "backtrack": "backtrack",
        "quarantine": "quarantine",
        "stop": "stop",
    }.get(tactic_mode, "persist_adapt")
    contribution_text = "Potential paper-level stepping stone if the result becomes a scoped theorem or finite falsifier with prior-art boundary and explicit escape conditions."
    if tactic_mode == "constructive_bridge":
        contribution_text = "Not paper-ready yet; first type the branch objects and compute the route parameters that could become a theorem or obstruction."
    source_cycle_ids = [clean_text(row.get("cycle_id")) for row in recent if clean_text(row.get("cycle_id"))]
    return {
        "recommendation_id": stable_id("pvsnp.neg", branch_id, family, tactic_mode),
        "branch_id": branch_id,
        "branch_title": clean_text(branch.get("title") or branch.get("branch_title")),
        "route_family": family,
        "tactic_mode": tactic_mode,
        "reason_for_tactic": clean_text(guidance["reason"]),
        "exact_negation_or_method_class": clean_text(guidance["method_class"]),
        "contradiction_carrier_or_no_go_family": clean_text(guidance["carrier"]),
        "conflict_target": clean_text(guidance["conflict"]),
        "escape_conditions": guidance["escape_conditions"],
        "proof_obligations": guidance["proof_obligations"],
        "branch_control_decision": branch_control,
        "next_validation_handoff": (
            "Send this packet to pvsnp-symbolic-complexity-auditor for exact parameters, "
            "then to pvsnp-impossibility-theorem-forger and contradiction-route-auditor if the obstruction is theorem-shaped."
        ),
        "paper_contribution_potential": contribution_text,
        "source_cycle_ids": source_cycle_ids,
        "prompt_guidance": (
            f"Use tactic_mode={tactic_mode} for route_family={family}. "
            "Do not restate barriers; produce the local carrier, exact transfer or contradiction target, escape conditions, and validation handoff."
        ),
    }


def build_payload() -> dict[str, Any]:
    _, run_state = load_run_state(target_id=TARGET_ID)
    branches = load_branches(run_state) if run_state else []
    cycles = load_cycles(run_state) if run_state else []
    pressure_bridge = load_optional_json(PRESSURE_BRIDGES)
    contribution_monitor = load_optional_json(CONTRIBUTION_MONITOR)
    recommendations = [
        recommendation_for_branch(branch, cycles, pressure_bridge, contribution_monitor)
        for branch in branches
        if clean_text(branch.get("target_id")) == TARGET_ID
    ]
    high_value = [
        row
        for row in recommendations
        if row["tactic_mode"] in {"impossibility_theorem", "proof_by_contradiction", "falsifier_search"}
    ]
    return {
        "version": 1,
        "target_id": TARGET_ID,
        "generated_utc": utc_now(),
        "purpose": "Route-specific selection of contradiction, impossibility, falsifier, and constructive tactics for P vs NP discovery branches.",
        "source_artifacts": {
            "active_run": rel(ROOT / f"agentic/runs/discovery_marathons/{run_state.get('run_id', '')}/run_state.json") if run_state else "",
            "pressure_bridges": rel(PRESSURE_BRIDGES),
            "contribution_monitor": rel(CONTRIBUTION_MONITOR),
        },
        "policy_summary": [
            "Use contradiction only when the negated local subclaim has a carrier and an accepted conflict target.",
            "Use impossibility theorem formation only for scoped method classes with explicit parameters and escape conditions.",
            "Keep constructive exploration alive when beta=0, subpolynomial queries, nonblackbox use, non-naturalness, or advice-free certificates remain untested.",
            "Treat scoped no-go results and finite falsifiers as possible paper-level stepping stones.",
        ],
        "recommendations": recommendations,
        "recommended_next_move": clean_text(
            high_value[0]["prompt_guidance"] if high_value else "First classify route families, source objects, target classes, and transfer parameters."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# P vs NP Negative Tactic Packet",
        "",
        payload["purpose"],
        "",
        "## Policy",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["policy_summary"])
    lines.extend(["", "## Branch Recommendations", ""])
    for row in payload["recommendations"]:
        lines.extend(
            [
                f"### {row['branch_title'] or row['branch_id']}",
                "",
                f"- Route family: `{row['route_family']}`",
                f"- Tactic mode: `{row['tactic_mode']}`",
                f"- Branch control: `{row['branch_control_decision']}`",
                f"- Reason: {row['reason_for_tactic']}",
                f"- Method class / negation: {row['exact_negation_or_method_class']}",
                f"- Carrier: {row['contradiction_carrier_or_no_go_family']}",
                f"- Conflict target: {row['conflict_target']}",
                "- Escape conditions:",
            ]
        )
        lines.extend(f"  - {item}" for item in row["escape_conditions"])
        lines.append("- Proof obligations:")
        lines.extend(f"  - {item}" for item in row["proof_obligations"])
        lines.extend(
            [
                f"- Handoff: {row['next_validation_handoff']}",
                f"- Paper contribution potential: {row['paper_contribution_potential']}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    payload = build_payload()
    write_json(OUT_JSON, payload)
    write_markdown(OUT_MD, render_markdown(payload))
    print(f"wrote {rel(OUT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
