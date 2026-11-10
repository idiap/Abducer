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

"""Validate Yang-Mills bridge-lemma packets."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
MARKDOWN = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.md"
CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return clean_text(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_packet(packet: dict[str, Any], index: int) -> None:
    subject = f"packet {index} ({packet.get('title', 'unknown')})"
    for field in [
        "packet_id",
        "title",
        "source_route_id",
        "route_family",
        "lemma_statement",
        "source_objects",
        "target_objects",
        "definitions",
        "assumptions",
        "equations",
        "proof_obligations",
        "failure_tests",
        "contradiction_branches",
        "conditional_skill_triggers",
        "next_recursive_subgoals",
        "promotion_condition",
        "same_theory_invariant",
    ]:
        require(field in packet, f"{rel(REPORT)} {subject} missing `{field}`")
    text = flatten(packet).lower()
    for marker in ["yang-mills", "gauge-invariant", "continuum", "os", "same", "theory"]:
        require(marker in text, f"{rel(REPORT)} {subject} lacks marker `{marker}`")
    require(len(packet["source_objects"]) >= 3, f"{rel(REPORT)} {subject} needs source objects")
    require(len(packet["target_objects"]) >= 3, f"{rel(REPORT)} {subject} needs target objects")
    require(len(packet["definitions"]) >= 3, f"{rel(REPORT)} {subject} needs definitions")
    require(len(packet["assumptions"]) >= 3, f"{rel(REPORT)} {subject} needs assumptions")
    require(len(packet["proof_obligations"]) >= 4, f"{rel(REPORT)} {subject} needs proof obligations")
    require(len(packet["failure_tests"]) >= 3, f"{rel(REPORT)} {subject} needs failure tests")
    require(len(packet["next_recursive_subgoals"]) >= 3, f"{rel(REPORT)} {subject} needs next recursive subgoals")
    require("same" in packet["same_theory_invariant"].lower(), f"{rel(REPORT)} {subject} same-theory invariant is weak")
    contradiction_branches = packet["contradiction_branches"]
    require(isinstance(contradiction_branches, list) and contradiction_branches, f"{rel(REPORT)} {subject} needs contradiction branches")
    for branch_index, branch in enumerate(contradiction_branches, start=1):
        require(isinstance(branch, dict), f"{rel(REPORT)} {subject} contradiction branch {branch_index} must be an object")
        for field in [
            "branch_id",
            "strategy",
            "exact_negation",
            "contradiction_carrier",
            "derived_consequence",
            "conflict_target",
            "audit_skill",
            "learning_if_failed",
        ]:
            require(clean_text(branch.get(field)), f"{rel(REPORT)} {subject} contradiction branch {branch_index} missing {field}")
        for field in ["preserved_commitments", "proof_obligations", "failure_modes"]:
            require(isinstance(branch.get(field), list), f"{rel(REPORT)} {subject} contradiction branch {branch_index} {field} must be a list")
        branch_text = flatten(branch).lower()
        for marker in ["same"]:
            require(marker in branch_text, f"{rel(REPORT)} {subject} contradiction branch {branch_index} lacks marker `{marker}`")
        require(branch["audit_skill"] == "contradiction-route-auditor", f"{rel(REPORT)} {subject} contradiction branch {branch_index} lacks auditor handoff")
        require(len(branch["preserved_commitments"]) >= 3, f"{rel(REPORT)} {subject} contradiction branch {branch_index} needs preserved commitments")
        require(len(branch["proof_obligations"]) >= 3, f"{rel(REPORT)} {subject} contradiction branch {branch_index} needs proof obligations")
        require(len(branch["failure_modes"]) >= 3, f"{rel(REPORT)} {subject} contradiction branch {branch_index} needs failure modes")
    for equation_index, equation in enumerate(packet["equations"], start=1):
        require(isinstance(equation, dict), f"{rel(REPORT)} {subject} equation {equation_index} must be an object")
        for field in ["label", "display", "latex", "valid_when"]:
            require(clean_text(equation.get(field)), f"{rel(REPORT)} {subject} equation {equation_index} missing {field}")
        require(len(clean_text(equation["valid_when"]).split()) >= 10, f"{rel(REPORT)} {subject} equation {equation_index} validity condition too thin")
    skills = {row.get("skill") for row in packet["conditional_skill_triggers"] if isinstance(row, dict)}
    require(skills, f"{rel(REPORT)} {subject} needs conditional skill triggers")
    require("kb-contradiction-strategist" in skills, f"{rel(REPORT)} {subject} should trigger kb-contradiction-strategist")
    require("contradiction-route-auditor" in skills, f"{rel(REPORT)} {subject} should trigger contradiction-route-auditor")
    if "RG-to-OS" in packet["title"]:
        require("prior-art-importer" in skills, f"{rel(REPORT)} {subject} should trigger prior-art-importer")
        require("Balaban" in flatten(packet), f"{rel(REPORT)} {subject} lacks Balaban content")
    if "Decay-to-Hamiltonian" in packet["title"]:
        require("evidence-acquisition-planner" in skills, f"{rel(REPORT)} {subject} should trigger evidence-acquisition-planner")
        require("spectrally determining" in text, f"{rel(REPORT)} {subject} lacks observable density content")


def main() -> int:
    report = load_json_object(REPORT)
    current = load_json_object(CURRENT_TARGET)
    require(report.get("target_id") == TARGET_ID, f"{rel(REPORT)} target is not Yang-Mills")
    require(current.get("target_id") == TARGET_ID, f"{rel(CURRENT_TARGET)} active target is not Yang-Mills")
    require(report.get("quality_gate") == "pass", f"{rel(REPORT)} quality gate is {report.get('quality_gate')}")
    require(report.get("long_horizon_status") == "pass", f"{rel(REPORT)} long-horizon status is not pass")
    require(report.get("skill_coherence_status") == "pass", f"{rel(REPORT)} skill coherence status is not pass")
    packets = report.get("packets", [])
    require(isinstance(packets, list) and len(packets) >= 2, f"{rel(REPORT)} needs at least two bridge packets")
    families = {packet.get("route_family") for packet in packets if isinstance(packet, dict)}
    require("Balaban RG continuum-control route" in families, f"{rel(REPORT)} missing Balaban bridge packet")
    require("Euclidean correlator-decay to spectral-gap route" in families, f"{rel(REPORT)} missing decay-to-gap bridge packet")
    for index, packet in enumerate(packets, start=1):
        require(isinstance(packet, dict), f"{rel(REPORT)} packet {index} must be an object")
        validate_packet(packet, index)
    require(MARKDOWN.exists(), f"missing rendered packet markdown: {rel(MARKDOWN)}")
    md = MARKDOWN.read_text(encoding="utf-8")
    for phrase in ["RG-to-OS Continuum Passage", "Cutoff-Uniform Decay-to-Hamiltonian-Gap", "Proof By Contradiction Branches", "Same-theory invariant"]:
        require(phrase in md, f"{rel(MARKDOWN)} missing visible phrase `{phrase}`")
    print(f"validated Yang-Mills bridge lemma packets ({len(packets)} packets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
