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
"""Build failure archaeology and failed-hypothesis premortem packets."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, slugify, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state, markdown_list, target_report_dir, write_markdown


REPORT_ROOT = ROOT / "agentic/reports/failure_archaeology/targets"
DEFAULT_WINDOW = 5


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    match = re.search(r"(\d+)$", raw)
    return int(match.group(1)) if match else 0


def selected_cycles(cycles: list[dict[str, Any]], *, since_cycle: int = 0, last: int = DEFAULT_WINDOW) -> list[dict[str, Any]]:
    ordered = sorted(cycles, key=cycle_number)
    if since_cycle:
        scoped = [cycle for cycle in ordered if cycle_number(cycle) >= since_cycle]
    else:
        scoped = ordered[-max(1, last) :]
    return scoped


def branch_outputs(cycles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for cycle in cycles:
        for output in cycle.get("branch_outputs", []) if isinstance(cycle.get("branch_outputs"), list) else []:
            if isinstance(output, dict):
                row = dict(output)
                row["_cycle_id"] = clean_text(cycle.get("cycle_id"))
                outputs.append(row)
    return outputs


def first_lemma(output: dict[str, Any]) -> dict[str, Any]:
    lemmas = output.get("candidate_lemmas", [])
    return lemmas[0] if isinstance(lemmas, list) and lemmas and isinstance(lemmas[0], dict) else {}


def normalize_signature(text: str) -> str:
    lowered = clean_text(text).lower()
    lowered = re.sub(r"cycle\s*\d+", "cycle", lowered)
    lowered = re.sub(r"\b\d+(?:\.\d+)?\b", "N", lowered)
    return lowered[:420]


def repeated_blockers(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for output in outputs:
        blocker = clean_text(output.get("attempted_derivation", {}).get("blocking_gap"))
        if not blocker:
            continue
        rows.append(
            {
                "signature": normalize_signature(blocker),
                "text": blocker,
                "cycle_id": clean_text(output.get("_cycle_id")),
                "branch_id": clean_text(output.get("branch_id")),
                "branch_title": clean_text(output.get("branch_title")),
            }
        )
    counts = Counter(row["signature"] for row in rows if row["signature"])
    repeated = []
    for signature, count in counts.most_common():
        if count < 2:
            continue
        examples = [row for row in rows if row["signature"] == signature]
        repeated.append(
            {
                "signature": signature,
                "repetition_count": count,
                "cycle_ids": sorted({row["cycle_id"] for row in examples if row["cycle_id"]}),
                "branch_ids": sorted({row["branch_id"] for row in examples if row["branch_id"]}),
                "example": examples[-1]["text"],
            }
        )
    return repeated


def text_blob(value: Any) -> str:
    return clean_text(value).lower()


def contains_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def control_decisions(outputs: list[dict[str, Any]]) -> list[str]:
    return [
        clean_text(output.get("control_decision", {}).get("decision"))
        for output in outputs
        if clean_text(output.get("control_decision", {}).get("decision"))
    ]


def investment_decisions(outputs: list[dict[str, Any]]) -> list[str]:
    decisions = []
    for output in outputs:
        gate = output.get("physical_relevance_impact", {}).get("major_publication_gate", {})
        decision = clean_text(gate.get("investment_decision"))
        if decision:
            decisions.append(decision)
    return decisions


def artifact_debt(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    markers = [
        "compute",
        "certify",
        "table",
        "interval",
        "tail",
        "bound",
        "quadrature",
        "stencil",
        "artifact",
        "proof object",
    ]
    rows = []
    seen: set[str] = set()
    for output in outputs:
        next_experiment = clean_text(output.get("next_experiment"))
        blocker = clean_text(output.get("attempted_derivation", {}).get("blocking_gap"))
        joined = f"{blocker} {next_experiment}".lower()
        if not contains_any(joined, markers):
            continue
        item = {
            "branch_id": clean_text(output.get("branch_id")),
            "branch_title": clean_text(output.get("branch_title")),
            "missing_artifact_or_test": next_experiment or blocker,
            "blocking_gap": blocker,
        }
        key = normalize_signature(item["missing_artifact_or_test"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(item)
    return rows[:8]


def detect_failure_signatures(target_id: str, outputs: list[dict[str, Any]], repeated: list[dict[str, Any]]) -> list[dict[str, Any]]:
    text = text_blob(outputs)
    decisions = " ".join(control_decisions(outputs)).lower()
    investments = investment_decisions(outputs)
    signatures = [
        {
            "signature": "artifact_debt",
            "detected": contains_any(text, ["table", "interval", "tail", "stencil", "quadrature", "proof object"]),
            "why_it_matters": "A branch cannot move by reasoning alone when promotion depends on a named missing artifact.",
            "prompt_heuristic": "Before proof search, ask: which concrete table, interval, bound, code output, or theorem must exist for this hypothesis to become live?",
            "pre_cycle_gate": "If the artifact is absent after repeated blockers, route to artifact_sprint, falsifier_sprint, demotion, or quarantine.",
        },
        {
            "signature": "proxy_shift",
            "detected": contains_any(text, ["proxy", "boundary theory", "counterterm", "different theory", "model change"]),
            "why_it_matters": "A proof route can become easier by silently changing the object instead of solving the target problem.",
            "prompt_heuristic": "Ask whether the source object and target object remain in the same theory, regulator, observable family, and validity regime.",
            "pre_cycle_gate": "Quarantine until same-domain transfer or same-theory carrier preservation is explicit.",
        },
        {
            "signature": "finite_to_global_gap",
            "detected": contains_any(text, ["finite", "fixed", "cutoff", "continuum", "infinite-volume", "clay", "global"]),
            "why_it_matters": "Finite support work can be valuable but does not by itself produce continuum, asymptotic, or Clay-level progress.",
            "prompt_heuristic": "Ask which finite claim is honest and which continuum/asymptotic/non-claim boundary remains untouched.",
            "pre_cycle_gate": "Demote to support-only unless the next artifact directly tests a target-facing transfer gate.",
        },
        {
            "signature": "uniformity_gap",
            "detected": contains_any(text, ["uniform", "nonuniform", "tail", "t_tail", "cutoff-uniform", "volume", "limit"]),
            "why_it_matters": "A bound that is not uniform across the relevant limit can explain local success and global failure at the same time.",
            "prompt_heuristic": "Ask which parameter, cutoff, volume, source, or limit must be uniform, and what would falsify uniformity.",
            "pre_cycle_gate": "Require a uniform bound ledger or a quarantine decision before promotion.",
        },
        {
            "signature": "definitional_transfer",
            "detected": contains_any(text, ["definitional", "defined as", "tautolog", "bridge image", "circular"]),
            "why_it_matters": "A transfer theorem is low value if it defines the target property as the image of the source property.",
            "prompt_heuristic": "Ask whether source and target properties remain independently meaningful after the bridge is removed.",
            "pre_cycle_gate": "Reframe or demote until the transfer has independent source and target content.",
        },
        {
            "signature": "no_decisive_falsifier",
            "detected": not contains_any(text, ["falsifier", "negative interval", "counterexample", "quarantine", "demote", "pivot"]),
            "why_it_matters": "A hypothesis that cannot fail will usually keep generating plausible but non-decisive cycles.",
            "prompt_heuristic": "Ask for the cheapest pass/fail test whose failure changes the route state.",
            "pre_cycle_gate": "Block ordinary proof search until a falsifier or artifact sprint exists.",
        },
        {
            "signature": "low_publication_reward",
            "detected": any(decision and decision != "invest_high_physics_reward" for decision in investments),
            "why_it_matters": "A correct lemma can still be a poor investment if it cannot change field understanding or support a major paper.",
            "prompt_heuristic": "Ask what a field reader would understand differently if this succeeds, and whether that difference is publication-weighty.",
            "pre_cycle_gate": "Do not invest ordinary cycles unless the major-publication gate is invest_high_physics_reward.",
        },
        {
            "signature": "repeated_blocker",
            "detected": bool(repeated) or contains_any(decisions, ["quarantine", "blocked", "stop"]),
            "why_it_matters": "Repeating the same blocker means the branch has stopped learning unless the next cycle produces the named artifact or a new representation.",
            "prompt_heuristic": "Ask whether the next cycle changes the blocker type, produces the missing artifact, or only rephrases the same obligation.",
            "pre_cycle_gate": "Route to artifact_sprint, falsifier_sprint, publication_demotion, or quarantine.",
        },
    ]
    if target_id == "yang-mills-existence-and-mass-gap-target":
        signatures.extend(
            [
                {
                    "signature": "missing_physical_carrier",
                    "detected": not contains_any(text, ["wilson", "schwinger", "os hilbert", "observable", "spectral", "cumulant"]),
                    "why_it_matters": "YM work without a physical carrier can drift into mathematically tidy but physically irrelevant estimates.",
                    "prompt_heuristic": "Ask which gauge-invariant observable, Schwinger family, OS Hilbert object, spectral object, or cumulant witness carries the claim.",
                    "pre_cycle_gate": "Reframe or quarantine until the physical carrier is named.",
                },
                {
                    "signature": "noncommuting_limits",
                    "detected": contains_any(text, ["cutoff", "continuum", "volume", "regulator", "rg", "limit"]),
                    "why_it_matters": "YM routes often fail because local regulator arguments do not commute with continuum, volume, or reconstruction limits.",
                    "prompt_heuristic": "Ask for an order-of-limits ledger and the first limit where the carrier might disappear.",
                    "pre_cycle_gate": "Require limit-order assumptions and a falsifier before claiming physics relevance.",
                },
            ]
        )
    return signatures


def hard_problem_diagnosis(target_id: str, outputs: list[dict[str, Any]]) -> dict[str, Any]:
    text = text_blob(outputs)
    physics = []
    mathematics = []
    representation = []
    if target_id == "yang-mills-existence-and-mass-gap-target":
        if contains_any(text, ["same-theory", "same theory"]):
            physics.append("Same-theory transfer is hard because the carrier must survive without changing regulator, observable algebra, boundary sector, or normalization.")
        if contains_any(text, ["wilson", "schwinger", "os", "spectral", "hamiltonian", "mass gap"]):
            physics.append("The route must connect gauge-invariant Euclidean observables to OS/Wightman reconstruction or spectral data without smuggling in a proxy object.")
        if contains_any(text, ["continuum", "cutoff", "regulator", "rg", "volume", "uniform"]):
            physics.append("Cutoff, volume, and regulator limits are not passive bookkeeping; they can destroy local positivity, cumulant witnesses, or spectral carriers.")
        if contains_any(text, ["nontrivial", "cumulant", "non-gaussian"]):
            physics.append("Nontriviality has to be carried by a same-theory observable witness, not by formal nonzero terms in a changed or fixed-regulator model.")
    if contains_any(text, ["positivity", "reflection", "os positivity", "positive"]):
        mathematics.append("Positivity is fragile under projection, Schur/Feshbach reduction, closure topology, endpoint singular terms, and source aggregation.")
    if contains_any(text, ["interval", "tail", "t_tail", "bound", "uniform"]):
        mathematics.append("The decisive sign or transfer claim depends on interval arithmetic and uniform tail bounds, so qualitative reasoning cannot close the gate.")
    if contains_any(text, ["source", "stencil", "kappa", "derivative", "quadrature"]):
        mathematics.append("Source-derivative data are high-order and equivalence-class dependent; the proof needs exact objects, not narrative source geometry.")
    if contains_any(text, ["definitional", "circular", "transfer", "bridge"]):
        mathematics.append("Bridge theorems risk circularity unless source and target properties remain independently meaningful.")
    if contains_any(text, ["raw", "too weak", "too strong", "fragmented", "coarse", "representation"]):
        representation.append("The failed cycles exposed a representation-fit problem: some carriers were too coarse to decide the gate, while raw local objects were too fragmented to transfer.")
    if contains_any(text, ["endpoint", "class", "equivalence", "aggregation"]):
        representation.append("The efficient representation must encode endpoint/source equivalence classes and aggregate before clipping; otherwise the sign problem is mislocalized.")
    return {
        "physics_hardness": physics or ["The cycle set did not expose enough target-specific physics language to diagnose a physics-hardness channel."],
        "mathematical_hardness": mathematics or ["The cycle set did not expose a concrete mathematical-hardness channel beyond ordinary proof incompleteness."],
        "representation_hardness": representation or ["No explicit representation-fit failure was detected; require a concept-gap audit before another broad cycle."],
    }


def choose_disposition(failure_detected: bool, debts: list[dict[str, Any]], signatures: list[dict[str, Any]]) -> str:
    detected = {row["signature"] for row in signatures if row.get("detected")}
    if "low_publication_reward" in detected:
        return "reframe_before_investment"
    if debts and ("artifact_debt" in detected or "repeated_blocker" in detected):
        return "persist_with_new_artifact_gate"
    if "proxy_shift" in detected or "missing_physical_carrier" in detected:
        return "quarantine_until_new_evidence"
    if "finite_to_global_gap" in detected:
        return "demote_to_support_only"
    if failure_detected:
        return "falsifier_or_negative_result"
    return "persist_with_explicit_premortem"


def build_failure_archaeology_report(
    run_state: dict[str, Any],
    cycles: list[dict[str, Any]],
    *,
    since_cycle: int = 0,
    last: int = DEFAULT_WINDOW,
) -> dict[str, Any]:
    target_id = clean_text(run_state.get("target_id"))
    scoped = selected_cycles(cycles, since_cycle=since_cycle, last=last)
    outputs = branch_outputs(scoped)
    repeated = repeated_blockers(outputs)
    debts = artifact_debt(outputs)
    decisions = control_decisions(outputs)
    failure_detected = bool(
        repeated
        or debts
        or any(contains_any(decision.lower(), ["quarantine", "demote", "blocked", "stop", "fail"]) for decision in decisions)
    )
    signatures = detect_failure_signatures(target_id, outputs, repeated)
    diagnosis = hard_problem_diagnosis(target_id, outputs)
    cycle_ids = [clean_text(cycle.get("cycle_id")) for cycle in scoped]
    branch_ids = sorted({clean_text(output.get("branch_id")) for output in outputs if clean_text(output.get("branch_id"))})
    disposition = choose_disposition(failure_detected, debts, signatures)
    failed_hypothesis = {
        "claim": clean_text(first_lemma(outputs[-1]).get("statement")) if outputs else "",
        "source_object": next(
            (item for output in outputs for item in first_lemma(output).get("definitions", []) if "source object" in clean_text(item).lower()),
            "",
        ),
        "target_object": next(
            (item for output in outputs for item in first_lemma(output).get("definitions", []) if "target object" in clean_text(item).lower()),
            "",
        ),
        "bridge_or_carrier": next(
            (
                item
                for output in outputs
                for item in first_lemma(output).get("definitions", [])
                if any(marker in clean_text(item).lower() for marker in ["carrier", "bridge", "controlled interface", "observable"])
            ),
            "",
        ),
        "non_claim_boundary": clean_text(outputs[-1].get("attempted_derivation", {}).get("why_not_yet_a_proof")) if outputs else "",
    }
    why_failed = []
    if repeated:
        why_failed.append("The cycle set repeatedly named the same blocker instead of producing the artifact, theorem, or falsifier that would decide it.")
    if debts:
        why_failed.append("The route became artifact-bound: the next proof move depends on missing tables, intervals, tails, source data, or explicit certificates.")
    if any(row.get("signature") == "low_publication_reward" and row.get("detected") for row in signatures):
        why_failed.append("At least one branch failed the major-publication investment gate and should not receive ordinary proof-search budget.")
    if not why_failed:
        why_failed.append("No deterministic failure was detected, but future cycles still require a premortem before investment.")
    why_not = [
        "Local progress can hide global fragility: each cycle may sharpen a lemma while delaying the artifact or transfer condition that actually decides the route.",
        "The workflow previously asked whether the branch was target-linked, but not always whether the precise missing artifact was already visible before the cycle began.",
        "A successful representation can be misleading when it explains the obstruction after the fact but does not expose the earliest cheap falsifier before investment.",
    ]
    if target_id == "yang-mills-existence-and-mass-gap-target":
        why_not.append(
            "In YM, finite Wilson/OS vocabulary can look physically promising before same-theory carrier survival, cutoff-uniformity, and continuum/spectral gates are separately certified."
        )
    return {
        "schema": "abducer.cycle_failure_archaeology.v1",
        "generated_utc": utc_now(),
        "generated_by_skills": [
            "failure-archaeology-explainer",
            "failed-hypothesis-anticipator",
            "abducer-failure-signal-cartographer",
            "physical-relevance-impact-auditor",
        ],
        "cycle_set": {
            "cycle_set_id": stable_id("failure-set", run_state.get("run_id"), target_id, cycle_ids),
            "target_id": target_id,
            "run_id": clean_text(run_state.get("run_id")),
            "cycle_ids": cycle_ids,
            "cycle_indices": [cycle_number(cycle) for cycle in scoped],
            "branch_ids": branch_ids,
            "window_policy": f"since_cycle={since_cycle}" if since_cycle else f"last={last}",
        },
        "failure_detected": failure_detected,
        "failure_summary": clean_text(" ".join(why_failed)),
        "smallest_honest_failed_hypothesis": failed_hypothesis,
        "hard_problem_diagnosis": diagnosis,
        "why_failed": why_failed,
        "why_not_anticipated": why_not,
        "repeated_blockers": repeated,
        "artifact_debt": debts,
        "anticipation_heuristics": signatures,
        "learning_for_future_cycles": [
            "Before investing in a hypothesis, ask for the earliest artifact or falsifier that could have revealed this failure.",
            "Treat repeated blockers as evidence that the branch needs artifact sprint, falsifier sprint, demotion, or quarantine.",
            "Separate hard-but-live proof debt from low-learning repetition by requiring new object-level information at each major cycle set.",
        ],
        "required_workflow_change": [
            "Attach failure_archaeology after every failed major cycle set.",
            "Run failed-hypothesis-anticipator before ordinary proof search on any branch emerging from a failed set.",
            "Expose the disposition in reports and queue selection before another marathon.",
        ],
        "route_disposition": disposition,
        "evidence_paths": [
            rel(ROOT / "agentic/runs/discovery_marathons" / slugify(clean_text(run_state.get("run_id"))) / "run_state.json"),
            *[
                rel(ROOT / "agentic/runs/discovery_marathons" / slugify(clean_text(run_state.get("run_id"))) / "cycles" / f"{slugify(cycle_id)}.json")
                for cycle_id in cycle_ids
            ],
        ],
        "validation_handoff": "agentic/scripts/validate_cycle_failure_archaeology.py",
    }


def target_failure_dir(target_id: str) -> Path:
    return REPORT_ROOT / slugify(target_id)


def render_failure_archaeology_markdown(report: dict[str, Any]) -> str:
    cycle_set = report.get("cycle_set", {})
    diagnosis = report.get("hard_problem_diagnosis", {})
    lines = [
        "# Cycle Failure Archaeology",
        "",
        f"Target: `{cycle_set.get('target_id', '')}`",
        f"Run: `{cycle_set.get('run_id', '')}`",
        f"Cycle set: `{cycle_set.get('cycle_set_id', '')}`",
        f"Cycles: `{cycle_set.get('cycle_ids', [])}`",
        f"Failure detected: `{report.get('failure_detected')}`",
        f"Disposition: `{report.get('route_disposition')}`",
        "",
        "## Failure Summary",
        "",
        clean_text(report.get("failure_summary")),
        "",
        "## Why This Was Hard",
        "",
        "Physics hardness:",
        "",
        markdown_list(diagnosis.get("physics_hardness", [])),
        "Mathematical hardness:",
        "",
        markdown_list(diagnosis.get("mathematical_hardness", [])),
        "Representation hardness:",
        "",
        markdown_list(diagnosis.get("representation_hardness", [])),
        "## Why It Failed",
        "",
        markdown_list(report.get("why_failed", [])),
        "## Why We Did Not Anticipate It",
        "",
        markdown_list(report.get("why_not_anticipated", [])),
        "## Anticipatory Heuristics",
        "",
    ]
    for row in report.get("anticipation_heuristics", []):
        lines.extend(
            [
                f"### {row.get('signature')}",
                "",
                f"Detected: `{row.get('detected')}`",
                "",
                f"Why it matters: {clean_text(row.get('why_it_matters'))}",
                "",
                f"Prompt heuristic: {clean_text(row.get('prompt_heuristic'))}",
                "",
                f"Pre-cycle gate: {clean_text(row.get('pre_cycle_gate'))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Required Workflow Change",
            "",
            markdown_list(report.get("required_workflow_change", [])),
            "## Evidence",
            "",
            markdown_list(report.get("evidence_paths", [])),
            f"Validation handoff: `{report.get('validation_handoff')}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_failure_archaeology_report(report: dict[str, Any]) -> dict[str, Path]:
    target_id = clean_text(report.get("cycle_set", {}).get("target_id"))
    out_dir = target_failure_dir(target_id)
    latest_json = out_dir / "latest.json"
    latest_md = out_dir / "latest.md"
    write_json(latest_json, report)
    write_markdown(latest_md, render_failure_archaeology_markdown(report))
    return {"latest_json": latest_json, "latest_md": latest_md}


def summary_for_discovery_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "cycle_set_id": report.get("cycle_set", {}).get("cycle_set_id", ""),
        "cycle_ids": report.get("cycle_set", {}).get("cycle_ids", []),
        "failure_detected": report.get("failure_detected", False),
        "failure_summary": report.get("failure_summary", ""),
        "route_disposition": report.get("route_disposition", ""),
        "detected_heuristics": [
            row.get("signature")
            for row in report.get("anticipation_heuristics", [])
            if row.get("detected")
        ],
        "latest_json": rel(target_failure_dir(report.get("cycle_set", {}).get("target_id", "")) / "latest.json"),
        "latest_md": rel(target_failure_dir(report.get("cycle_set", {}).get("target_id", "")) / "latest.md"),
    }


def build_for_active_run(target_id: str = "", run_id: str = "", *, since_cycle: int = 0, last: int = DEFAULT_WINDOW) -> dict[str, Any]:
    _, run_state = load_run_state(run_id or None, target_id or None)
    cycles = load_cycles(run_state) if run_state else []
    return build_failure_archaeology_report(run_state, cycles, since_cycle=since_cycle, last=last)
