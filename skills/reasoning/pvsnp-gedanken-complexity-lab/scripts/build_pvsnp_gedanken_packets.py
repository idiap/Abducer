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
"""Build P vs NP Gedanken experiment packets with essential conclusions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic_common import ROOT, clean_text, load_optional_json, stable_id, utc_now, write_json


PVSNP_OUT = ROOT / "agentic/reports/pvsnp_gedanken_experiments/latest.json"
PVSNP_MD = ROOT / "agentic/reports/pvsnp_gedanken_experiments/latest.md"
GENERAL_OUT = ROOT / "agentic/reports/gedanken_experiments/latest.json"
GENERAL_MD = ROOT / "agentic/reports/gedanken_experiments/latest.md"
BRIDGES = ROOT / "agentic/reports/pvsnp_pressure_bridges/latest.json"
RUN_DIR = ROOT / "agentic/runs/discovery_marathons/p-vs-np-marathon/cycles"


@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    title: str
    bridge_id: str
    pressure: str
    purpose: str
    minimal_world: str
    carrier: str
    contrast: str
    varied: tuple[str, str, str]
    controls: tuple[str, ...]
    expected_pattern: str
    teaches: str
    disconfirms: str
    variant: tuple[str, str, str]
    essential: tuple[str, str, str, str]
    follow_action: str
    follow_description: str
    follow_success: str
    follow_failure: str
    skills: tuple[str, ...]
    graph_edge: str


EXPERIMENTS: tuple[Experiment, ...] = (
    Experiment(
        experiment_id="pvsnp-gedanken-001",
        title="Oracle substitution microscope for the beta ceiling",
        bridge_id="pvsnp-bridge-001",
        pressure="black_box_substitution_cap",
        purpose="Elicit why a positive target-query exponent turns a hard carrier into only a bounded SAT-exponent exclusion.",
        minimal_world="A source language L_N decided by a SAT-oracle circuit with ordinary overhead N^q and SAT queries of length N^beta, against a lower bound SIZE(L_N)>N^{1+epsilon}.",
        carrier="Exact exponent model SIZE(L_N) <= N^q * (N^beta)^c after substituting hypothetical SAT circuits of size m^c.",
        contrast="Compare beta>0 with beta=0 while holding q, epsilon, model, and valid lengths fixed.",
        varied=("beta", "target-query length exponent", "varied between positive constant, o(1), and zero"),
        controls=("source lower-bound exponent 1+epsilon", "ordinary overhead q", "nonuniform circuit model", "no hidden advice"),
        expected_pattern="When beta>0, the contradiction window is c<(1+epsilon-q)/beta; when beta=0 and q<1+epsilon, the beta*c leakage disappears.",
        teaches="The decisive obstruction is not the carrier alone but the interface term beta*c introduced by black-box substitution.",
        disconfirms="A named nonblackbox transfer theorem in which SAT circuits cannot be substituted gate-by-gate and no beta*c upper bound is derivable.",
        variant=("set-beta-zero", "Force query length to be N^{o(1)} or independent of target exponent c.", "The bounded window should either become all-exponent compatible or expose a different overhead q obstruction."),
        essential=(
            "Positive beta is the intuitive source of exponent-window collapse.",
            "Formally, black-box substitution yields N^{q+beta c}, so fixed epsilon cannot cover all c if beta>0.",
            "Route control should demand q,beta computation before another magnification cycle.",
            "Next action: run exact transfer audit and convert repeated beta>0 outcomes into a no-go theorem.",
        ),
        follow_action="compute",
        follow_description="Run an exact transfer audit for the active carrier with symbolic q and beta, then classify all-exponent, bounded-window, or no-window outcome.",
        follow_success="The branch names q, beta, the target class, and whether the beta*c term is structurally unavoidable.",
        follow_failure="If q and beta cannot be named, backtrack to pressure localization rather than continuing proof search.",
        skills=("pvsnp-symbolic-complexity-auditor", "pvsnp-impossibility-theorem-forger"),
        graph_edge="pvsnp.rel.beta-ceiling-controls-magnification",
    ),
    Experiment(
        experiment_id="pvsnp-gedanken-002",
        title="Advised hard string versus searchable certificate",
        bridge_id="pvsnp-bridge-002",
        pressure="meta_complexity_carrier_debt",
        purpose="Elicit why MCSP/MKtP carrier routes need uniformly searchable evidence of hardness, not merely hard truth tables selected by advice.",
        minimal_world="For each length m, imagine either an advised high-complexity truth table y_m or a searchable pair (u,pi) accepted by verifier V and decoded by D into f_u.",
        carrier="Verifier-decoder system V(1^m,u,pi), D(u,z), certificate length O(m), search time 2^{O(m)}, and soundness CC(f_u)>2^{epsilon m}.",
        contrast="Compare nonuniform advice selection with deterministic exhaustive search over compact certificates.",
        varied=("selection_mode", "hard-object selection mechanism", "varied between advice-selected table and uniformly searchable certificate"),
        controls=("soundness threshold epsilon", "decoder model", "target uniform language", "bounded source-length gap kappa"),
        expected_pattern="Advice selection gives hard objects without a uniform language; compact searchable certificates can generate a uniform E-style language if gap coverage and verifier time hold.",
        teaches="The carrier must make hardness evidence searchable without turning into a large constructive natural property.",
        disconfirms="A proof that accepted certificate pairs are compact, sound, gap-dense, and non-natural while remaining searchable in the target time.",
        variant=("stretch-certificate", "Increase certificate length or verifier time to m^{1+Omega(1)} in the exponent.", "The target language should leave E or lose the claimed transfer."),
        essential=(
            "The key intuition is the difference between existence of hard strings and uniform access to hard strings.",
            "Formally, the bridge needs O(m)-bit sound certificates and kappa-gap coverage to transfer an exponent delta<epsilon/kappa.",
            "Route control should focus on certificate length, verifier time, gap coverage, and naturalness rather than more MCSP slogans.",
            "Next action: instantiate V,D for a proof-complexity or meta-complexity object and audit search time plus naturalness.",
        ),
        follow_action="derive",
        follow_description="Formalize the V,D certificate transfer theorem with epsilon, kappa, certificate length, verifier time, and no-advice conditions.",
        follow_success="The theorem states exactly when searchable certificates yield a uniform lower-bound language and what naturalness premise is avoided.",
        follow_failure="If certificates are advice-selected or dense constructive useful properties, pivot to natural-proof/no-advice obstruction.",
        skills=("pvsnp-qualitative-complexity-reasoner", "pvsnp-symbolic-complexity-auditor", "pvsnp-pressure-bridge-forger"),
        graph_edge="pvsnp.rel.searchable-certificate-controls-uniform-hardness",
    ),
    Experiment(
        experiment_id="pvsnp-gedanken-003",
        title="Naturalness toggle board for sparse properties",
        bridge_id="pvsnp-bridge-004",
        pressure="naturalness_density_pressure",
        purpose="Elicit which natural-proof premise must fail for a property route to remain plausible.",
        minimal_world="A truth-table property P with toggles for largeness, polynomial-time constructivity over truth tables, usefulness against polynomial-size circuits, and PRF-compatible circuit class.",
        carrier="Four-field natural-proof ledger: density(P), constructivity(P), usefulness(P,C), and PRF-risk(C).",
        contrast="Compare dense constructive useful property with sparse or proof-mediated useful property.",
        varied=("density_constructivity_profile", "natural-proof premise profile", "varied by switching largeness or constructivity off while preserving usefulness"),
        controls=("target circuit class", "truth-table representation", "usefulness implication", "cryptographic barrier assumption"),
        expected_pattern="If largeness, constructivity, and usefulness all remain present, the route hits natural-proof pressure; if one premise fails, the route must prove usefulness survives.",
        teaches="Non-naturalness is not a label; it is a specific failed premise plus a surviving lower-bound implication.",
        disconfirms="A formal property whose failed natural-proof premise is named and whose usefulness against the target circuit class is still proved.",
        variant=("restore-largeness", "Make the sparse property dense while keeping constructivity and usefulness.", "The natural-proof pressure should reappear under PRF assumptions."),
        essential=(
            "The fundamental intuition is that avoiding natural proofs requires breaking a precise premise, not avoiding the word natural.",
            "Formally, the property must fail largeness or constructivity or change proof mediation while retaining usefulness.",
            "Route control should reject property routes that do not publish a naturalness ledger.",
            "Next action: build a ledger for the active property and demote it if all three natural-proof premises remain present.",
        ),
        follow_action="formalize",
        follow_description="Build a natural-proof ledger for the active property with density, constructivity, usefulness, PRF-risk, and escape premise.",
        follow_success="The property states exactly which natural-proof premise fails and why the target usefulness implication survives.",
        follow_failure="If density, constructivity, and usefulness all hold, pivot to a barrier/no-go explanation.",
        skills=("pvsnp-conceptual-pressure-localizer", "pvsnp-impossibility-theorem-forger"),
        graph_edge="pvsnp.rel.naturalness-ledger-controls-property-route",
    ),
    Experiment(
        experiment_id="pvsnp-gedanken-004",
        title="All-exponent quantifier-lift switch",
        bridge_id="pvsnp-bridge-005",
        pressure="all_exponent_quantifier_gap",
        purpose="Elicit the difference between excluding a fixed circuit exponent and proving NP not subset P/poly.",
        minimal_world="A family of source carriers indexed by target exponent c, each with overheads q_c,beta_c and source margin a_c.",
        carrier="Quantifier model: for every fixed c, require a_c>q_c+beta_c c under one target-preserving construction scheme.",
        contrast="Compare one fixed source lower bound with a cofinal family covering arbitrary c.",
        varied=("target_exponent_c", "universal polynomial exponent", "varied over arbitrary fixed constants"),
        controls=("target class NP not subset P/poly", "same circuit model", "valid-length coverage", "uniform rule for the family"),
        expected_pattern="A fixed carrier covers only a window of c; a genuine quantifier lift must provide a uniform way to cover every fixed c without hiding the target lower bound.",
        teaches="All-polynomial separation is a quantifier problem, not merely a numerical threshold improvement.",
        disconfirms="A parameterized source family with explicit overhead functions satisfying the transfer inequality for every fixed c without circular source obligations.",
        variant=("fix-c", "Freeze c at one small value.", "The branch may look successful locally, showing why fixed-exponent tests are misleading."),
        essential=(
            "The intuition is that P/poly separation quantifies over every polynomial exponent.",
            "Formally, a bounded exponent window is not NP not subset P/poly unless there is a cofinal lift over c.",
            "Route control should ask whether each new carrier broadens quantifier coverage or repeats the same finite window.",
            "Next action: state a parameterized theorem over c or quarantine the route as bounded-window only.",
        ),
        follow_action="falsify",
        follow_description="Test whether the active source family covers arbitrary c or only restates a bounded exponent window.",
        follow_success="The branch emits a cofinal parameter family or a no-go theorem explaining why no such family exists in the method class.",
        follow_failure="If only fixed-c evidence appears, quarantine as proxy progress.",
        skills=("pvsnp-symbolic-complexity-auditor", "pvsnp-impossibility-theorem-forger", "next-experiment-queue-ranker"),
        graph_edge="pvsnp.rel.all-exponent-quantifier-controls-target-progress",
    ),
    Experiment(
        experiment_id="pvsnp-gedanken-005",
        title="Proof-system certificate bench for semantic lower bounds",
        bridge_id="pvsnp-bridge-003",
        pressure="proof_complexity_transfer_gap",
        purpose="Elicit when proof-complexity objects help certify semantic circuit hardness rather than merely relocating the original difficulty.",
        minimal_world="A lower-bound tautology LB(u,s) in a named Cook-Reckhow proof system, with proof length ell(m), verifier time T_V(m), and semantic soundness CC(f_u)>s.",
        carrier="Proof-system bench with knobs for proof length, verifier time, semantic soundness, and searchability of proofs.",
        contrast="Compare short verifiable semantic certificates with proof lower-bound obligations as hard as the target.",
        varied=("proof_length", "length of proof or certificate", "varied from O(m) to exponential or unavailable"),
        controls=("proof system", "semantic meaning of LB(u,s)", "decoder for f_u", "target transfer theorem"),
        expected_pattern="Short sound proofs can feed the searchable certificate bridge; missing or huge proofs relocate the target difficulty into proof complexity.",
        teaches="Proof-complexity is useful only when the proof object controls semantic hardness and search overhead at the same time.",
        disconfirms="A named proof system and tautology family with short sound proofs that yield searchable high-complexity functions.",
        variant=("semantic-to-syntactic-only", "Drop the semantic soundness link and keep only proof-system hardness.", "The bridge should stop implying circuit lower bounds, exposing a proxy shift."),
        essential=(
            "The intuition is that proof objects can organize evidence, but only semantic soundness connects them to circuit lower bounds.",
            "Formally, proof length and verifier time must fit the target search bound while LB(u,s) soundly implies CC(f_u)>s.",
            "Route control should reject proof-complexity moves that lose the semantic lower-bound interface.",
            "Next action: choose a proof system and LB tautology, then audit proof length, verifier time, and semantic implication.",
        ),
        follow_action="formalize",
        follow_description="Specify a proof system and LB(u,s) tautology family, then state the semantic soundness and proof-length requirements.",
        follow_success="The bridge says whether proof objects can supply searchable high-complexity certificates or only relocate the hard lower bound.",
        follow_failure="If semantic soundness or proof-length control is absent, pivot to an impossibility theorem about the method class.",
        skills=("pvsnp-impossibility-theorem-forger", "pvsnp-symbolic-complexity-auditor", "contradiction-route-auditor"),
        graph_edge="pvsnp.rel.proof-certificate-controls-semantic-hardness",
    ),
)


def recent_cycle_sources() -> list[str]:
    if not RUN_DIR.exists():
        return []
    return [str(path.relative_to(ROOT)) for path in sorted(RUN_DIR.glob("cycle-*.json"))[-5:]]


def bridge_lookup() -> dict[str, dict[str, Any]]:
    payload = load_optional_json(BRIDGES)
    rows = payload.get("bridge_candidates", []) if isinstance(payload, dict) else []
    return {str(row.get("id")): row for row in rows if isinstance(row, dict)}


def need_assessment(exp: Experiment) -> dict[str, Any]:
    return {
        "decision": "design_now",
        "criteria_met": [
            f"The active P vs NP pressure `{exp.pressure}` has a concrete mechanism that can be isolated in a small complexity-theory world.",
            "The situation has a controlled contrast, a disconfirming observation, and a follow-up skill handoff.",
        ],
        "criteria_missing": [
            "The imagined observation still needs a derivation, exact audit, or theorem statement before it becomes evidence."
        ],
        "rejected_alternatives": ["run_more_marathon_cycles_first", "treat_as_direct_proof", "generic_sat_example"],
        "why_not_direct_derivation_or_probe": (
            "The pressure is conceptual: before proving or computing, the loop must isolate which variable or interface "
            "would make the branch succeed or fail."
        ),
    }


def packet_for_experiment(exp: Experiment, bridge: dict[str, Any], sources: list[str]) -> dict[str, Any]:
    packet_id = stable_id("gedanken.packet", "p-vs-np-target", exp.experiment_id, exp.bridge_id)
    variant_id, changed_condition, predicted_change = exp.variant
    varied_id, varied_role, held_fixed_or_varied = exp.varied
    conclusion_keys = ["decisive_intuition", "formal_lesson", "route_control_consequence", "next_action"]
    essential = dict(zip(conclusion_keys, exp.essential, strict=True))
    bridge_sources = list(dict.fromkeys([*sources, "agentic/reports/pvsnp_pressure_bridges/latest.json"]))
    return {
        "packet_id": packet_id,
        "target_id": "p-vs-np-target",
        "created_utc": utc_now(),
        "source_artifacts": bridge_sources,
        "originating_cycle_ids": ["pvsnp-pressure-bridge-report"],
        "originating_branch_ids": [exp.bridge_id],
        "need_decision": "design_now",
        "need_assessment": need_assessment(exp),
        "trigger_criteria": [exp.pressure, exp.bridge_id, clean_text(bridge.get("title") or exp.title)],
        "situation": {
            "title": exp.title,
            "purpose": exp.purpose,
            "minimal_world": exp.minimal_world,
            "mathematical_carrier": exp.carrier,
            "controlled_contrast": exp.contrast,
            "why_this_situation_is_informative": (
                f"It makes `{exp.pressure}` observable by varying `{varied_id}` while holding the target model and "
                "transfer commitments fixed."
            ),
            "non_claims": [
                "This does not prove P != NP.",
                "This does not prove NP is not contained in P/poly.",
                "This only extracts route intuition that requires a follow-up proof, audit, or no-go theorem.",
            ],
        },
        "variables": [
            {
                "id": varied_id,
                "role": varied_role,
                "control_status": "varied",
                "held_fixed_or_varied": held_fixed_or_varied,
                "validity_regime": "P vs NP bridge/proxy analysis with explicit source and target models",
            },
            {
                "id": "target_class",
                "role": "target theorem boundary",
                "control_status": "held_fixed",
                "held_fixed_or_varied": "held fixed as P != NP or NP not subset P/poly, not a proxy claim",
                "validity_regime": "same-model target-preserving transfer",
            },
            {
                "id": "transfer_certificate",
                "role": "condition required before intuition can affect the proof route",
                "control_status": "dependent",
                "held_fixed_or_varied": "observed as present or missing after follow-up",
                "validity_regime": "post-Gedanken validation handoff",
            },
        ],
        "interventions": [
            {
                "id": f"vary-{varied_id}",
                "operation": f"Vary `{varied_id}` across the controlled contrast: {exp.contrast}",
                "varied_variable": varied_id,
                "held_fixed": list(exp.controls),
                "predicted_direction": exp.expected_pattern,
                "decision_value": exp.teaches,
            }
        ],
        "expected_observations": [
            {
                "id": f"observe-{varied_id}",
                "observable": exp.expected_pattern,
                "expected_pattern": exp.expected_pattern,
                "what_it_would_teach": exp.teaches,
                "what_would_disconfirm_it": exp.disconfirms,
            }
        ],
        "variants": [
            {
                "id": variant_id,
                "changed_condition": changed_condition,
                "predicted_change": predicted_change,
                "reason_for_variant": "It changes the decisive pressure variable while preserving the surrounding target model.",
            }
        ],
        "insight_hypotheses": list(exp.essential),
        "essential_conclusions": essential,
        "transfer_scope": {
            "transfer_verdict": "needs_certificate",
            "transfers": f"The route intuition about `{exp.pressure}` and its controlled variable `{varied_id}`.",
            "does_not_transfer": "Truth of P vs NP, actual circuit lower bounds, or theorem-level progress without the follow-up certificate.",
            "transfer_certificate_needed": exp.follow_success,
        },
        "affected_node_ids": [f"pvsnp.node.{exp.pressure}", f"pvsnp.node.{exp.bridge_id}"],
        "affected_edge_ids": [exp.graph_edge],
        "graph_update_action": "annotate_edge",
        "proposed_graph_updates": [
            {
                "edge_id": exp.graph_edge,
                "action": "annotate_edge",
                "epistemic_status": "conceptual_probe",
                "rationale": essential["route_control_consequence"],
            }
        ],
        "followup_cycle_tasks": [
            {
                "action": exp.follow_action,
                "description": exp.follow_description,
                "success_criterion": exp.follow_success,
                "failure_or_demotion_criterion": exp.follow_failure,
                "required_skills": list(exp.skills),
                "packet_id": packet_id,
                "situation_title": exp.title,
                "transfer_verdict": "needs_certificate",
            },
            {
                "action": "rank_next_experiment",
                "description": f"Use the essential conclusions from `{exp.title}` to rank whether {exp.bridge_id} should persist, pivot, or become a no-go theorem.",
                "success_criterion": "The queue item names the decisive variable, payoff criterion, and stop condition.",
                "failure_or_demotion_criterion": "If the queue only repeats the story without a computation or theorem-shaped handoff, quarantine as conceptual-only.",
                "required_skills": ["next-experiment-queue-ranker", "pvsnp-pressure-bridge-forger"],
                "packet_id": packet_id,
                "situation_title": exp.title,
                "transfer_verdict": "needs_certificate",
            },
        ],
        "failure_modes": [
            "The situation is treated as evidence rather than intuition.",
            "The follow-up does not compute, derive, falsify, formalize, or rank a concrete next move.",
            "The branch changes target class or hides advice/uniformity assumptions.",
        ],
        "epistemic_status": "conceptual_probe",
        "validation_handoff": "python agentic/scripts/validate_pvsnp_gedanken_conclusions.py && python agentic/scripts/validate_gedanken_experiment_packets.py",
    }


def build_payload() -> dict[str, Any]:
    bridges = bridge_lookup()
    sources = recent_cycle_sources()
    packets = [packet_for_experiment(exp, bridges.get(exp.bridge_id, {}), sources) for exp in EXPERIMENTS]
    return {
        "version": 1,
        "target_id": "p-vs-np-target",
        "generated_utc": utc_now(),
        "generation_mode": "pvsnp_complexity_gedanken_from_pressure_bridges",
        "source_report": str(BRIDGES.relative_to(ROOT)),
        "live_packet_count": len(packets),
        "quarantine_count": 0,
        "queue_handoff_count": sum(len(packet["followup_cycle_tasks"]) for packet in packets),
        "packets": packets,
        "essential_conclusions_summary": [
            packet["essential_conclusions"] for packet in packets
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# P vs NP Gedanken Experiments",
        "",
        f"- Target: `{payload['target_id']}`",
        f"- Packets: `{len(payload['packets'])}`",
        f"- Generation mode: `{payload['generation_mode']}`",
        "",
        "## Essential Conclusions",
        "",
    ]
    for packet in payload["packets"]:
        lines.append(f"### {packet['situation']['title']}")
        lines.append("")
        for key, value in packet["essential_conclusions"].items():
            lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        lines.append("")
    lines.append("## Packets")
    lines.append("")
    for packet in payload["packets"]:
        lines.extend(
            [
                f"### {packet['situation']['title']}",
                "",
                f"- Packet: `{packet['packet_id']}`",
                f"- Bridge: `{packet['originating_branch_ids'][0]}`",
                f"- Pressure: `{packet['trigger_criteria'][0]}`",
                f"- Minimal world: {packet['situation']['minimal_world']}",
                f"- Controlled contrast: {packet['situation']['controlled_contrast']}",
                f"- Expected observation: {packet['expected_observations'][0]['expected_pattern']}",
                f"- Transfer certificate: {packet['transfer_scope']['transfer_certificate_needed']}",
                "- Follow-up tasks:",
            ]
        )
        for task in packet["followup_cycle_tasks"]:
            lines.append(f"  - `{task['action']}` {task['description']}")
        lines.append("")
    return "\n".join(lines)


def write_payload(payload: dict[str, Any], write_general: bool) -> None:
    write_json(PVSNP_OUT, payload)
    PVSNP_MD.parent.mkdir(parents=True, exist_ok=True)
    PVSNP_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    if write_general:
        write_json(GENERAL_OUT, payload)
        GENERAL_MD.parent.mkdir(parents=True, exist_ok=True)
        GENERAL_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-general", action="store_true", help="Also write the standard Gedanken report path.")
    args = parser.parse_args()
    payload = build_payload()
    write_payload(payload, write_general=args.write_general)
    print(f"Wrote {PVSNP_OUT.relative_to(ROOT)}")
    print(f"Wrote {PVSNP_MD.relative_to(ROOT)}")
    if args.write_general:
        print(f"Wrote {GENERAL_OUT.relative_to(ROOT)}")
        print(f"Wrote {GENERAL_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
