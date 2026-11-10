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

"""Validate the big-deal milestone archive and paper-draft trigger."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path


REPORT = ROOT / "agentic/reports/big_deal_goal_archive/latest.json"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def text_at(path: Path) -> str:
    if not path.exists():
        fail(f"missing archive artifact: {rel(path)}")
    return path.read_text(encoding="utf-8")


def artifact_path(report: dict[str, Any], key: str) -> Path:
    raw = report.get("artifacts", {}).get(key)
    require(clean_text(raw), f"{rel(REPORT)} missing artifact path `{key}`")
    return repo_path(str(raw), must_exist=True)


def main() -> int:
    report = load_json_object(REPORT)
    require(report.get("target_id") == TARGET_ID, f"{rel(REPORT)} target is not Yang-Mills")
    require(report.get("archive_status") in {"armed_no_reached_goal", "activated"}, f"{rel(REPORT)} invalid archive status")
    policy = report.get("trigger_policy", {})
    reached_statuses = policy.get("reached_statuses", [])
    require(isinstance(reached_statuses, list) and "achieved" in reached_statuses, f"{rel(REPORT)} trigger policy lacks achieved status")
    require("LaTeX process summary" in policy.get("required_action", ""), f"{rel(REPORT)} trigger policy does not require process LaTeX")
    require("paper-argument draft" in policy.get("required_action", ""), f"{rel(REPORT)} trigger policy does not require paper argument")
    require("full Yang-Mills proof" in policy.get("proof_safety_rule", ""), f"{rel(REPORT)} proof safety rule must prevent overclaiming")
    watched = report.get("watched_milestones", [])
    reached = report.get("reached_milestones", [])
    require(isinstance(watched, list) and len(watched) >= 5, f"{rel(REPORT)} needs watched milestones")
    require(isinstance(reached, list), f"{rel(REPORT)} reached_milestones must be a list")
    if reached:
        require(report["archive_status"] == "activated", f"{rel(REPORT)} reached milestones require activated archive")
    else:
        require(report["archive_status"] == "armed_no_reached_goal", f"{rel(REPORT)} empty reached milestones should be armed")
    for index, milestone in enumerate(watched, start=1):
        require(isinstance(milestone, dict), f"{rel(REPORT)} watched milestone {index} must be an object")
        for field in ["label", "current_status", "why_big_deal", "success_signal", "next_action"]:
            require(clean_text(milestone.get(field)), f"{rel(REPORT)} watched milestone {index} missing {field}")
    learning = report.get("strategy_learning_summary", [])
    require(isinstance(learning, list) and len(learning) >= 4, f"{rel(REPORT)} needs strategy learning summary")
    for index, beat in enumerate(learning, start=1):
        require(isinstance(beat, dict), f"{rel(REPORT)} learning beat {index} must be an object")
        require(clean_text(beat.get("physics_story")), f"{rel(REPORT)} learning beat {index} needs physics_story")
        require(len(beat.get("what_we_learned", [])) >= 2, f"{rel(REPORT)} learning beat {index} needs learning notes")
    gedanken = report.get("gedanken_release_summary", {})
    require(isinstance(gedanken, dict), f"{rel(REPORT)} needs gedanken_release_summary")
    for field in ["packet_count", "live_packet_count", "queue_handoff_count", "quarantine_count", "invalid_packet_count"]:
        require(isinstance(gedanken.get(field), int), f"{rel(REPORT)} gedanken summary missing integer `{field}`")
    require(
        gedanken.get("proof_safety_status") in {"conceptual_probes_only", "no_gedanken_packets_available"},
        f"{rel(REPORT)} must distinguish conceptual probe status",
    )
    require("not counted as proof progress" in gedanken.get("branch_control_effect", ""), f"{rel(REPORT)} must state Gedanken proof-safety boundary")
    process_tex = artifact_path(report, "process_summary_tex")
    paper_tex = artifact_path(report, "paper_argument_draft_tex")
    process_text = text_at(process_tex)
    paper_text = text_at(paper_tex)
    for phrase in ["Big-Deal Goal Process Summary", "Watched Big-Deal Milestones", "Physics Mechanism Learning From Strategy Attempts", "Gedanken Experiment Release Summary"]:
        require(phrase in process_text, f"{rel(process_tex)} missing phrase `{phrase}`")
    for phrase in ["Argument Spine", "Claim Scope", "Gedanken Experiment Boundary", "Proof-Safety Boundary"]:
        require(phrase in paper_text, f"{rel(paper_tex)} missing phrase `{phrase}`")
    if reached:
        require("Reached Milestones" in paper_text, f"{rel(paper_tex)} must include reached milestones section")
    else:
        require("No monitored milestone has reached" in paper_text, f"{rel(paper_tex)} must state dormant status")
    print(f"validated big-deal goal archive: {report['archive_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
