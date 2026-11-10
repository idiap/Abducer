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
"""Validate avenue literature-gap warrants and acceptance/rejection fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from avenue_literature_gap import (
    EXPLORATION_MODES,
    PVSNP_TARGET_ID,
    VALID_INVESTMENT_DECISIONS,
    YM_TARGET_ID,
    target_warrant_latest_json,
)


SCHEMA_PATH = ROOT / "agentic/spec/avenue_literature_gap_warrant.schema.json"
FIXTURE_DIR = ROOT / "tests/fixtures/avenue_literature_gap"
DEFAULT_TARGETS = [YM_TARGET_ID, PVSNP_TARGET_ID]
VAGUE_GAP_PATTERNS = [
    "no one has tried this",
    "not found in literature",
    "seems novel",
    "could be interesting",
    "new approach",
    "novel because different",
]
YM_PHYSICS_MARKERS = [
    "wilson",
    "schwinger",
    "os",
    "wightman",
    "hamiltonian",
    "spectral",
    "gauge-invariant",
    "nontriviality",
    "mass gap",
]
YM_TARGET_GATES = {
    "same-theory continuum construction",
    "OS/Wightman reconstruction",
    "gauge-invariant observable density",
    "nontriviality of the field",
    "positive spectral mass gap",
}
PVSNP_MARKERS = [
    "boolean",
    "complexity",
    "lower-bound",
    "lower bound",
    "reduction",
    "proof-complexity",
    "proof complexity",
    "uniformity",
    "advice",
    "barrier",
    "circuit",
]


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def score(packet: dict[str, Any], *path: str) -> int:
    value: Any = packet
    for key in path:
        value = value.get(key, {}) if isinstance(value, dict) else {}
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1


def text_has_specificity(value: Any) -> bool:
    text = clean_text(value).lower()
    if len(text.split()) < 8:
        return False
    return not any(pattern in text for pattern in VAGUE_GAP_PATTERNS)


def validate_warrant_shape(warrant: dict[str, Any], source: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "target_id",
        "avenue_id",
        "avenue_title",
        "smallest_honest_claim",
        "mathematical_or_physical_object",
        "target_commitments_touched",
        "closest_known_results",
        "source_search_provenance",
        "gap_statement",
        "why_not_already_known",
        "relevance_threshold",
        "physics_or_field_impact",
        "unification_power",
        "route_decision_power",
        "novelty_boundary",
        "disqualifier_matrix",
        "explicit_unknowns",
        "allowed_next_modes",
        "investment_decision",
        "validation_handoff",
    ]
    for field in required:
        if not warrant.get(field):
            errors.append(f"missing {field}")
    if errors:
        return errors

    if warrant.get("investment_decision") not in VALID_INVESTMENT_DECISIONS:
        errors.append(f"invalid investment_decision {warrant.get('investment_decision')}")
    for field in ["smallest_honest_claim", "gap_statement", "why_not_already_known", "novelty_boundary"]:
        if not text_has_specificity(warrant.get(field)):
            errors.append(f"{field} is too vague or generic")
    refs = as_list(warrant.get("closest_known_results"))
    if len(refs) < 3:
        errors.append("closest_known_results needs at least three named entries")
    for index, ref in enumerate(refs, start=1):
        for field in ["ref_id", "title", "relevance", "limitation_for_this_avenue"]:
            if not clean_text(ref.get(field)):
                errors.append(f"closest_known_results item {index} missing {field}")
        if not text_has_specificity(ref.get("limitation_for_this_avenue")):
            errors.append(f"closest_known_results item {index} limitation is too vague")
    provenance = as_list(warrant.get("source_search_provenance"))
    if len(provenance) < 2:
        errors.append("source_search_provenance needs at least two local or literature sources")
    for index, row in enumerate(provenance, start=1):
        if not clean_text(row.get("source")) or not clean_text(row.get("scope")) or not clean_text(row.get("finding")):
            errors.append(f"source_search_provenance item {index} is incomplete")
    if not any("agentic/reports" in clean_text(row.get("source")) or "KB/" in clean_text(row.get("source")) for row in provenance):
        errors.append("source_search_provenance must cite at least one repo-local evidence artifact")

    relevance = warrant.get("relevance_threshold", {})
    impact = warrant.get("physics_or_field_impact", {})
    unification = warrant.get("unification_power", {})
    route = warrant.get("route_decision_power", {})
    for name, packet in [
        ("relevance_threshold", relevance),
        ("physics_or_field_impact", impact),
        ("unification_power", unification),
        ("route_decision_power", route),
    ]:
        if not isinstance(packet, dict):
            errors.append(f"{name} must be an object")
            continue
        if not isinstance(packet.get("score"), int) or not 0 <= int(packet.get("score")) <= 5:
            errors.append(f"{name}.score must be an integer from 0 to 5")
    if not isinstance(unification.get("compresses"), list) or len(unification.get("compresses", [])) < 2:
        errors.append("unification_power.compresses needs at least two pressures")
    if not text_has_specificity(unification.get("mechanism")):
        errors.append("unification_power.mechanism is too vague")
    if not text_has_specificity(route.get("next_decisive_test")):
        errors.append("route_decision_power.next_decisive_test is too vague")

    disqualifiers = as_list(warrant.get("disqualifier_matrix"))
    if len(disqualifiers) < 3:
        errors.append("disqualifier_matrix needs at least three tests")
    for index, item in enumerate(disqualifiers, start=1):
        for field in ["disqualifier", "test", "decision_if_triggered"]:
            if not clean_text(item.get(field)):
                errors.append(f"disqualifier_matrix item {index} missing {field}")
        if item.get("decision_if_triggered") not in {
            "reframe_gap_before_investment",
            "do_not_invest_prior_art_collision",
            "quarantine_low_relevance",
            "artifact_sprint_only",
        }:
            errors.append(f"disqualifier_matrix item {index} has invalid decision_if_triggered")
    if len(as_list(warrant.get("explicit_unknowns"))) < 2:
        errors.append("explicit_unknowns needs at least two unknowns")
    modes = set(as_list(warrant.get("allowed_next_modes")))
    if not modes:
        errors.append("allowed_next_modes must be nonempty")

    handoff = warrant.get("validation_handoff", {})
    if clean_text(handoff.get("validator")) != "agentic/scripts/validate_avenue_literature_gap_warrant.py":
        errors.append("validation_handoff.validator must point to this validator")
    if clean_text(handoff.get("next_skill")) != "literature-gap-relevance-auditor":
        errors.append("validation_handoff.next_skill must be literature-gap-relevance-auditor")
    if not SCHEMA_PATH.exists():
        errors.append(f"missing schema {rel(SCHEMA_PATH)}")
    return errors


def validate_decision_semantics(warrant: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = clean_text(warrant.get("investment_decision"))
    modes = set(as_list(warrant.get("allowed_next_modes")))
    relevance_score = score(warrant, "relevance_threshold", "score")
    impact_score = score(warrant, "physics_or_field_impact", "score")
    unification_score = score(warrant, "unification_power", "score")
    route_score = score(warrant, "route_decision_power", "score")
    triggered = [
        item
        for item in as_list(warrant.get("disqualifier_matrix"))
        if clean_text(item.get("status")).lower() in {"triggered", "confirmed", "active_blocker"}
    ]
    if decision == "invest_in_avenue":
        if relevance_score < 4 or impact_score < 4 or unification_score < 3 or route_score < 3:
            errors.append("invest_in_avenue requires high relevance, impact, unification, and route-decision scores")
        if not modes.intersection(EXPLORATION_MODES):
            errors.append("invest_in_avenue must allow branch_exploration or broad_branch_exploration")
        if triggered:
            errors.append("invest_in_avenue cannot have triggered blocking disqualifiers")
    elif decision == "artifact_sprint_only":
        if modes.intersection(EXPLORATION_MODES):
            errors.append("artifact_sprint_only cannot allow broad exploration modes")
        if not modes.intersection({"artifact_sprint", "falsifier_sprint", "proof_delivery"}):
            errors.append("artifact_sprint_only must allow artifact, falsifier, or proof_delivery work")
        if route_score < 3:
            errors.append("artifact_sprint_only requires route-decision score at least 3")
    elif decision == "reframe_gap_before_investment":
        if "literature_gap_reframe" not in modes:
            errors.append("reframe_gap_before_investment must allow literature_gap_reframe")
        if modes.intersection(EXPLORATION_MODES):
            errors.append("reframe_gap_before_investment cannot allow broad exploration")
    elif decision == "do_not_invest_prior_art_collision":
        joined = clean_text(warrant).lower()
        if "prior" not in joined or "collision" not in joined:
            errors.append("prior-art rejection must explicitly name a prior-art collision")
        if modes.intersection(EXPLORATION_MODES):
            errors.append("prior-art rejection cannot allow broad exploration")
    elif decision == "quarantine_low_relevance":
        if "quarantine" not in modes:
            errors.append("quarantine_low_relevance must allow quarantine mode")
        if relevance_score >= 4 and impact_score >= 4 and unification_score >= 3:
            errors.append("quarantine_low_relevance is inconsistent with high relevance and impact scores")
    return errors


def validate_target_semantics(warrant: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    target_id = clean_text(warrant.get("target_id"))
    joined = clean_text(warrant).lower()
    commitments = {clean_text(item) for item in as_list(warrant.get("target_commitments_touched"))}
    if target_id == YM_TARGET_ID:
        if not any(marker in joined for marker in YM_PHYSICS_MARKERS):
            errors.append("YM warrant must name a physical carrier or Clay-facing physics marker")
        if not commitments.intersection(YM_TARGET_GATES):
            errors.append("YM warrant must touch a Clay-facing target gate")
        if "physical" not in joined and "field" not in joined:
            errors.append("YM warrant must state physics or field-facing impact")
        if "unification" not in joined and "compress" not in joined:
            errors.append("YM warrant must state unification power")
    if target_id == PVSNP_TARGET_ID:
        if not any(marker in joined for marker in PVSNP_MARKERS):
            errors.append("P vs NP warrant must use complexity-theoretic target language")
        for marker in ["source", "target", "uniform", "barrier"]:
            if marker not in joined:
                errors.append(f"P vs NP warrant missing {marker} accounting")
    return errors


def warrant_errors(warrant: dict[str, Any], source: Path) -> list[str]:
    errors = validate_warrant_shape(warrant, source)
    if errors:
        return errors
    errors.extend(validate_decision_semantics(warrant))
    errors.extend(validate_target_semantics(warrant))
    return errors


def package_warrants(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("warrants"), list):
        return [row for row in payload["warrants"] if isinstance(row, dict)]
    if payload.get("avenue_id"):
        return [payload]
    return []


def document_errors(payload: dict[str, Any], source: Path) -> list[str]:
    warrants = package_warrants(payload)
    if not warrants:
        return ["document contains neither an avenue warrant nor a warrant package"]
    errors: list[str] = []
    if payload.get("warrants"):
        if clean_text(payload.get("status")) != "implemented":
            errors.append("warrant package status must be implemented")
        if int(payload.get("warrant_count", 0)) != len(warrants):
            errors.append("warrant package warrant_count does not match warrants length")
    for index, warrant in enumerate(warrants, start=1):
        for error in warrant_errors(warrant, source):
            errors.append(f"warrant {index} {clean_text(warrant.get('avenue_id'))}: {error}")
    return errors


def validate_expected(path: Path) -> None:
    payload = load_json_object(path)
    expectation = clean_text(payload.get("validation_expectation") or "accept")
    expected_fragment = clean_text(payload.get("expected_failure_contains")).lower()
    errors = document_errors(payload, path)
    if expectation == "accept":
        if errors:
            fail(f"{rel(path)} should validate but failed: {errors}")
        return
    if expectation == "reject":
        if not errors:
            fail(f"{rel(path)} should fail validation but passed")
        if expected_fragment and expected_fragment not in " | ".join(errors).lower():
            fail(f"{rel(path)} failed for the wrong reason: {errors}; expected fragment `{expected_fragment}`")
        return
    fail(f"{rel(path)} has invalid validation_expectation {expectation}")


def default_paths() -> list[Path]:
    paths = [target_warrant_latest_json(target_id) for target_id in DEFAULT_TARGETS if target_warrant_latest_json(target_id).exists()]
    if FIXTURE_DIR.exists():
        paths.extend(sorted(FIXTURE_DIR.glob("*.json")))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    paths = [Path(path) for path in args.paths] or default_paths()
    if not paths:
        print("No avenue literature-gap warrants found; validator is idle.")
        return 0
    for path in paths:
        validate_expected(path)
    print(f"validated {len(paths)} avenue literature-gap warrant document(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
