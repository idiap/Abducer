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
"""Shared helpers for avenue literature-gap warrants."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, rel, slugify


YM_TARGET_ID = "yang-mills-existence-and-mass-gap-target"
PVSNP_TARGET_ID = "p-vs-np-target"
OUT_ROOT = ROOT / "agentic/reports/avenue_literature_gap_warrants/targets"
VALID_INVESTMENT_DECISIONS = {
    "invest_in_avenue",
    "artifact_sprint_only",
    "reframe_gap_before_investment",
    "do_not_invest_prior_art_collision",
    "quarantine_low_relevance",
}
EXPLORATION_MODES = {"branch_exploration", "broad_branch_exploration"}


def target_warrant_dir(target_id: str) -> Path:
    return OUT_ROOT / slugify(target_id)


def target_warrant_latest_json(target_id: str) -> Path:
    return target_warrant_dir(target_id) / "latest.json"


def target_warrant_latest_md(target_id: str) -> Path:
    return target_warrant_dir(target_id) / "latest.md"


def load_target_warrant_package(target_id: str) -> dict[str, Any]:
    return load_optional_json(target_warrant_latest_json(target_id))


def package_warrants(package: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(package.get("warrants"), list):
        return [row for row in package["warrants"] if isinstance(row, dict)]
    if package.get("avenue_id"):
        return [package]
    return []


def load_target_warrants(target_id: str) -> list[dict[str, Any]]:
    rows = package_warrants(load_target_warrant_package(target_id))
    if rows:
        return rows
    directory = target_warrant_dir(target_id)
    if not directory.exists():
        return []
    output = []
    for path in sorted(directory.glob("*.json")):
        if path.name == "latest.json":
            continue
        payload = load_optional_json(path)
        if payload.get("avenue_id"):
            output.append(payload)
    return output


def classify_branch_avenue(branch: dict[str, Any]) -> str:
    target_id = clean_text(branch.get("target_id"))
    text = clean_text(branch).lower()
    if target_id == YM_TARGET_ID:
        if any(marker in text for marker in ["route a", "routea", "wilson", "schur", "feshbach", "endpoint", "collar", "hairpin"]):
            return "ym.routea.endpoint_source_table"
        if any(marker in text for marker in ["representational", "representation", "rg", "regulator", "schwinger", "basin"]):
            return "ym.representational_dynamics"
        if any(marker in text for marker in ["visual", "analogy", "metaphor", "conceptualization"]):
            return "ym.visual_conceptualization"
        return "ym.routea.endpoint_source_table"
    if target_id == PVSNP_TARGET_ID:
        if any(marker in text for marker in ["formula footprints", "row", "support", "rup", "cdcl"]):
            return "pvsnp.formula_footprints_literature_gap"
        if any(marker in text for marker in ["barrier", "natural", "relativ", "algebr", "oracle"]):
            return "pvsnp.barrier_aware_bridge_gap"
        return "pvsnp.bridge_route_gap"
    return f"{slugify(target_id)}.general_literature_gap"


def warrant_for_avenue(target_id: str, avenue_id: str) -> dict[str, Any]:
    for warrant in load_target_warrants(target_id):
        if clean_text(warrant.get("avenue_id")) == clean_text(avenue_id):
            return warrant
    warrants = load_target_warrants(target_id)
    return warrants[0] if warrants else {}


def warrant_for_branch(branch: dict[str, Any]) -> dict[str, Any]:
    target_id = clean_text(branch.get("target_id"))
    return warrant_for_avenue(target_id, classify_branch_avenue(branch))


def warrant_summary(warrant: dict[str, Any]) -> dict[str, Any]:
    if not warrant:
        return {
            "avenue_id": "",
            "investment_decision": "missing_warrant",
            "allowed_next_modes": ["literature_gap_reframe"],
            "warrant_path": "",
            "effect": "Do not start a new broad avenue until a literature-gap warrant exists.",
        }
    decision = clean_text(warrant.get("investment_decision"))
    modes = warrant.get("allowed_next_modes", []) if isinstance(warrant.get("allowed_next_modes"), list) else []
    effect = {
        "invest_in_avenue": "Branch exploration is allowed because the warrant names a relevant, literature-positioned gap.",
        "artifact_sprint_only": "Broad exploration is blocked; only the named artifact, calculation, falsifier, or proof packet is allowed.",
        "reframe_gap_before_investment": "Do a literature-gap reframe before spending another broad research cycle.",
        "do_not_invest_prior_art_collision": "Stop or reframe because closest known work appears to absorb the proposed novelty.",
        "quarantine_low_relevance": "Quarantine ordinary proof search until a higher-impact gap is named.",
    }.get(decision, "Warrant decision is not recognized; treat as blocked until validation is repaired.")
    return {
        "avenue_id": clean_text(warrant.get("avenue_id")),
        "avenue_title": clean_text(warrant.get("avenue_title")),
        "investment_decision": decision,
        "allowed_next_modes": modes,
        "relevance_score": warrant.get("relevance_threshold", {}).get("score"),
        "impact_score": warrant.get("physics_or_field_impact", {}).get("score"),
        "unification_score": warrant.get("unification_power", {}).get("score"),
        "route_decision_score": warrant.get("route_decision_power", {}).get("score"),
        "smallest_honest_claim": clean_text(warrant.get("smallest_honest_claim")),
        "gap_statement": clean_text(warrant.get("gap_statement")),
        "next_decisive_test": clean_text(warrant.get("route_decision_power", {}).get("next_decisive_test")),
        "warrant_path": rel(target_warrant_latest_json(clean_text(warrant.get("target_id")))),
        "effect": effect,
    }


def branch_warrant_allows_exploration(branch: dict[str, Any]) -> bool:
    summary = warrant_summary(warrant_for_branch(branch))
    decision = clean_text(summary.get("investment_decision"))
    modes = set(summary.get("allowed_next_modes", []))
    return decision == "invest_in_avenue" and bool(modes.intersection(EXPLORATION_MODES))
