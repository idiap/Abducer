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

"""Archive big-deal Yang-Mills milestones as LaTeX summaries and paper drafts."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, load_optional_json, rel, slugify, utc_now, write_json


MONITOR = ROOT / "agentic/reports/reasoning_monitor/latest.json"
LONG_HORIZON = ROOT / "agentic/reports/long_horizon/latest.json"
BRIDGE_PACKETS = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
GEDANKEN_PACKETS = ROOT / "agentic/reports/gedanken_experiments/latest.json"
OUT_DIR = ROOT / "agentic/reports/big_deal_goal_archive"
OUT_JSON = OUT_DIR / "latest.json"
OUT_MD = OUT_DIR / "latest.md"
OUT_TEX = OUT_DIR / "latest.tex"
OUT_PAPER_TEX = OUT_DIR / "paper_argument_draft.tex"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"
REACHED_STATUSES = {"achieved", "potentially_achieved", "potential_breakthrough_signal", "certified_breakthrough"}


def latex_escape(value: Any) -> str:
    text = clean_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def itemize(items: list[Any]) -> str:
    rows = [clean_text(item) for item in items if clean_text(item)]
    if not rows:
        return "\\begin{itemize}\\item None recorded.\\end{itemize}"
    body = "\n".join(f"\\item {latex_escape(row)}" for row in rows)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}"


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    monitor = load_json_object(MONITOR)
    long_horizon = load_optional_json(LONG_HORIZON)
    bridge_packets = load_optional_json(BRIDGE_PACKETS)
    gedanken_packets = load_optional_json(GEDANKEN_PACKETS)
    return monitor, long_horizon, bridge_packets, gedanken_packets


def milestone_card(row: dict[str, Any]) -> dict[str, Any]:
    status = clean_text(row.get("current_status"))
    return {
        "milestone_id": row.get("milestone_id", ""),
        "label": row.get("label", ""),
        "current_status": status,
        "archive_triggered": status in REACHED_STATUSES,
        "why_big_deal": row.get("why_big_deal", ""),
        "potentially_achieved_when": row.get("potentially_achieved_when", ""),
        "success_signal": row.get("success_signal", ""),
        "certification_evidence": row.get("certification_evidence", []),
        "disqualifiers": row.get("disqualifiers", []),
        "next_action": row.get("next_action", ""),
        "linked_commitments": row.get("linked_commitments", []),
    }


def build_report() -> dict[str, Any]:
    monitor, long_horizon, bridge_packets, gedanken_packets = load_inputs()
    milestones = [milestone_card(row) for row in monitor.get("success_milestones", {}).get("items", []) if isinstance(row, dict)]
    reached = [row for row in milestones if row["archive_triggered"]]
    archive_status = "activated" if reached else "armed_no_reached_goal"
    strategy = monitor.get("interpretative_strategy_story", {})
    learning_summary = []
    for beat in strategy.get("story_beats", []):
        if not isinstance(beat, dict):
            continue
        learning_summary.append(
            {
                "phase": beat.get("phase", ""),
                "headline": beat.get("headline", ""),
                "physics_story": beat.get("physics_story", ""),
                "non_payoff": beat.get("why_it_did_not_pay_off") or beat.get("remaining_blockers") or beat.get("why_this_is_the_next_goal", []),
                "what_we_learned": beat.get("what_we_learned", []),
                "decision": beat.get("decision", ""),
                "moved_to": beat.get("moved_to", ""),
            }
        )
    paper_argument = {
        "status": "draft_activated" if reached else "draft_scaffold_waiting_for_trigger",
        "claim_scope": (
            "A paper argument is activated only for milestones with certification evidence attached to the same continuum Yang-Mills object: "
            "the gauge-field construction, OS reconstruction, nontriviality witness, and spectral-gap witness must all be read from one limiting theory. "
            "Until then, the draft records the intended argument shape without claiming a proof."
        ),
        "argument_spine": [
            "State the reached milestone and its exact certification evidence.",
            "Identify the same-theory gauge-field object carrying construction, reconstruction, nontriviality, and spectral content.",
            "Present the mathematical bridge lemmas used to move from Euclidean Schwinger data and gauge-invariant observables to the milestone claim.",
            "List disqualifier tests and how each was ruled out.",
            "State remaining obligations and the boundary between achieved progress and unresolved Clay target commitments.",
        ],
    }
    artifacts = {
        "process_summary_tex": rel(OUT_TEX),
        "paper_argument_draft_tex": rel(OUT_PAPER_TEX),
        "archive_json": rel(OUT_JSON),
        "archive_markdown": rel(OUT_MD),
    }
    g_packets = gedanken_packets.get("packets", [])
    if not isinstance(g_packets, list):
        g_packets = []
    gedanken_release_summary = {
        "packet_count": len(g_packets),
        "live_packet_count": int(gedanken_packets.get("live_packet_count") or 0),
        "queue_handoff_count": int(gedanken_packets.get("queue_handoff_count") or 0),
        "quarantine_count": int(gedanken_packets.get("quarantine_count") or 0),
        "invalid_packet_count": 0,
        "proof_safety_status": (
            "conceptual_probes_only"
            if g_packets
            else "no_gedanken_packets_available"
        ),
        "branch_control_effect": (
            "Gedanken packets may affect branch control only through validated follow-up queue items, transfer verdicts, and qualitative graph annotations. "
            "They are not counted as proof progress unless a later derivation, computation, or source-backed certificate discharges the relevant obligation."
        ),
    }
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": monitor.get("target", {}).get("target_id", ""),
        "archive_status": archive_status,
        "trigger_policy": {
            "reached_statuses": sorted(REACHED_STATUSES),
            "required_action": "When any success milestone enters a reached status, retain a LaTeX process summary and a paper-argument draft.",
            "proof_safety_rule": "The paper draft must distinguish certified progress from a full Yang-Mills proof unless all Clay commitments are discharged in the same theory.",
        },
        "watched_milestones": milestones,
        "reached_milestones": reached,
        "strategy_learning_summary": learning_summary,
        "paper_argument": paper_argument,
        "skill_coherence_status": long_horizon.get("skill_ecosystem_coherence", {}).get("status", ""),
        "bridge_packet_count": len(bridge_packets.get("packets", [])) if isinstance(bridge_packets.get("packets"), list) else 0,
        "gedanken_release_summary": gedanken_release_summary,
        "artifacts": artifacts,
        "source_artifacts": [
            rel(MONITOR),
            rel(LONG_HORIZON),
            rel(BRIDGE_PACKETS),
            rel(GEDANKEN_PACKETS),
            "agentic/reports/hamiltonian_gap_derivation/latest.md",
            "agentic/reports/physics_math_interpretation/latest.md",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Big-Deal Goal Archive",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Archive status: `{report['archive_status']}`",
        f"- Reached milestones: `{len(report['reached_milestones'])}`",
        "",
        "## Trigger Policy",
        "",
        f"- Reached statuses: `{', '.join(report['trigger_policy']['reached_statuses'])}`",
        f"- Required action: {report['trigger_policy']['required_action']}",
        f"- Proof safety rule: {report['trigger_policy']['proof_safety_rule']}",
        "",
        "## Watched Milestones",
        "",
    ]
    for milestone in report["watched_milestones"]:
        lines.extend(
            [
                f"### {milestone['label']}",
                "",
                f"- Status: `{milestone['current_status']}`",
                f"- Archive triggered: `{milestone['archive_triggered']}`",
                f"- Why big deal: {milestone['why_big_deal']}",
                f"- Potentially achieved when: {milestone['potentially_achieved_when']}",
                f"- Success signal: {milestone['success_signal']}",
                f"- Next action: {milestone['next_action']}",
                "",
            ]
        )
    lines.extend(["## Physics Mechanism Learning Carried Into Any Paper Draft", ""])
    for beat in report["strategy_learning_summary"]:
        lines.append(f"- `{beat['phase']}`: {beat['headline']}")
        if beat.get("physics_story"):
            lines.append(f"  - Physics mechanism: {beat['physics_story']}")
        for learned in beat.get("what_we_learned", []):
            lines.append(f"  - Physics lesson: {learned}")
    gedanken = report.get("gedanken_release_summary", {})
    lines.extend(
        [
            "",
            "## Gedanken Experiment Release Summary",
            "",
            f"- Packet count: `{gedanken.get('packet_count', 0)}`",
            f"- Live packet count: `{gedanken.get('live_packet_count', 0)}`",
            f"- Queue handoff count: `{gedanken.get('queue_handoff_count', 0)}`",
            f"- Quarantine count: `{gedanken.get('quarantine_count', 0)}`",
            f"- Invalid packet count: `{gedanken.get('invalid_packet_count', 0)}`",
            f"- Proof-safety status: `{gedanken.get('proof_safety_status', '')}`",
            f"- Branch-control effect: {gedanken.get('branch_control_effect', '')}",
        ]
    )
    lines.extend(["", "## Generated Artifacts", ""])
    for label, path in report["artifacts"].items():
        lines.append(f"- `{label}`: `{path}`")
    return "\n".join(lines) + "\n"


def render_process_tex(report: dict[str, Any]) -> str:
    reached_text = "No milestone has been marked as reached yet." if not report["reached_milestones"] else "Reached milestones are archived below."
    parts = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage{amsmath,amssymb}",
        r"\title{Yang--Mills Big-Deal Goal Process Summary}",
        r"\author{Abducer Long-Horizon Monitor}",
        r"\date{}",
        r"\begin{document}",
        r"\maketitle",
        r"\section*{Archive Status}",
        latex_escape(f"Status: {report['archive_status']}. {reached_text}"),
        r"\section*{Trigger Policy}",
        itemize(
            [
                f"Reached statuses: {', '.join(report['trigger_policy']['reached_statuses'])}",
                report["trigger_policy"]["required_action"],
                report["trigger_policy"]["proof_safety_rule"],
            ]
        ),
        r"\section*{Watched Big-Deal Milestones}",
    ]
    for milestone in report["watched_milestones"]:
        parts.extend(
            [
                f"\\subsection*{{{latex_escape(milestone['label'])}}}",
                itemize(
                    [
                        f"Status: {milestone['current_status']}",
                        f"Archive triggered: {milestone['archive_triggered']}",
                        f"Why this is a big deal: {milestone['why_big_deal']}",
                        f"Potentially achieved when: {milestone['potentially_achieved_when']}",
                        f"Success signal: {milestone['success_signal']}",
                        f"Next action: {milestone['next_action']}",
                    ]
                ),
                r"\paragraph{Certification Evidence}",
                itemize(milestone.get("certification_evidence", [])),
                r"\paragraph{Disqualifiers}",
                itemize(milestone.get("disqualifiers", [])),
            ]
        )
    parts.extend([r"\section*{Physics Mechanism Learning From Strategy Attempts}"])
    for beat in report["strategy_learning_summary"]:
        parts.extend(
            [
                f"\\subsection*{{{latex_escape(beat['headline'])}}}",
                r"\paragraph{Physics mechanism}",
                latex_escape(beat.get("physics_story", "")),
                r"\paragraph{What did not pay off or remains blocked}",
                itemize(beat.get("non_payoff", [])),
                r"\paragraph{What was learned physically}",
                itemize(beat.get("what_we_learned", [])),
                r"\paragraph{Decision}",
                latex_escape(beat.get("decision", "")),
            ]
        )
    gedanken = report.get("gedanken_release_summary", {})
    parts.extend(
        [
            r"\section*{Gedanken Experiment Release Summary}",
            itemize(
                [
                    f"Packet count: {gedanken.get('packet_count', 0)}",
                    f"Live packet count: {gedanken.get('live_packet_count', 0)}",
                    f"Queue handoff count: {gedanken.get('queue_handoff_count', 0)}",
                    f"Quarantine count: {gedanken.get('quarantine_count', 0)}",
                    f"Invalid packet count: {gedanken.get('invalid_packet_count', 0)}",
                    f"Proof-safety status: {gedanken.get('proof_safety_status', '')}",
                    gedanken.get("branch_control_effect", ""),
                ]
            ),
        ]
    )
    parts.append(r"\end{document}")
    return "\n\n".join(parts) + "\n"


def render_paper_tex(report: dict[str, Any]) -> str:
    activated = bool(report["reached_milestones"])
    title = "Draft Paper Argument for a Reached Yang--Mills Milestone" if activated else "Dormant Paper-Argument Draft for Yang--Mills Milestone Certification"
    abstract = (
        "This draft is activated because at least one monitored milestone has reached a certified or potential-breakthrough status."
        if activated
        else "No monitored milestone has reached the archive trigger. This document records the argument shape that will be filled only after certification evidence is attached."
    )
    parts = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage{amsmath,amssymb,amsthm}",
        f"\\title{{{latex_escape(title)}}}",
        r"\author{Abducer Long-Horizon Monitor}",
        r"\date{}",
        r"\newtheorem{claim}{Claim}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        latex_escape(abstract),
        r"\end{abstract}",
        r"\section{Claim Scope}",
        latex_escape(report["paper_argument"]["claim_scope"]),
        r"\section{Argument Spine}",
        itemize(report["paper_argument"]["argument_spine"]),
    ]
    if activated:
        parts.append(r"\section{Reached Milestones}")
        for milestone in report["reached_milestones"]:
            parts.extend(
                [
                    f"\\begin{{claim}}[{latex_escape(milestone['label'])}]",
                    latex_escape(milestone["success_signal"]),
                    r"\end{claim}",
                    r"\paragraph{Certification evidence}",
                    itemize(milestone.get("certification_evidence", [])),
                    r"\paragraph{Disqualifiers checked}",
                    itemize(milestone.get("disqualifiers", [])),
                ]
            )
    else:
        parts.extend(
            [
                r"\section{Activation Condition}",
                latex_escape(
                    "The draft remains dormant until at least one milestone has status achieved, potentially_achieved, potential_breakthrough_signal, or certified_breakthrough."
                ),
                r"\section{Current Non-Claim}",
                latex_escape(
                    "The current Yang-Mills run has useful bridge-lemma packets and monitoring artifacts, but no big-deal milestone is certified as reached."
                ),
            ]
        )
    parts.extend(
        [
            r"\section{Physics Mechanism Learning To Preserve}",
            itemize([learned for beat in report["strategy_learning_summary"] for learned in beat.get("what_we_learned", [])]),
            r"\section{Gedanken Experiment Boundary}",
            latex_escape(report.get("gedanken_release_summary", {}).get("branch_control_effect", "")),
            r"\section{Proof-Safety Boundary}",
            latex_escape(report["trigger_policy"]["proof_safety_rule"]),
            r"\end{document}",
        ]
    )
    return "\n\n".join(parts) + "\n"


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    OUT_TEX.write_text(render_process_tex(report), encoding="utf-8")
    OUT_PAPER_TEX.write_text(render_paper_tex(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"Wrote {rel(OUT_TEX)}")
    print(f"Wrote {rel(OUT_PAPER_TEX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
