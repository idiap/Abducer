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
"""Validate YM artifact-or-stop control, fixtures, and generated reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from artifact_or_stop_control import (
    ALLOWED_NEXT_MODES,
    BLOCKER_ID,
    BLOCKER_REPORT,
    DEMOTION_PACKET_JSON,
    ENDPOINT_CONTRACT_JSON,
    ENDPOINT_PILOT_JSON,
    FORBIDDEN_AFTER_REPETITION,
    YM_TARGET_ID,
    evaluate_artifact_or_stop_packet,
)


CONTROL_SCHEMA = ROOT / "agentic/spec/artifact_or_stop_control.schema.json"
ENDPOINT_SCHEMA = ROOT / "agentic/spec/ym_endpoint_source_table.schema.json"
FIXTURE_DIR = ROOT / "tests/fixtures/artifact_or_stop"
GENERATIVE_FIXTURE = ROOT / "tests/generative/test_ym_artifact_or_stop_quality.md"
EXPECTED_VERDICTS = ROOT / "agentic/evals/ym_artifact_or_stop/expected_verdicts.json"


def require_path(path: Path) -> None:
    if not path.exists():
        fail(f"missing required artifact {rel(path)}")


def require(value: Any, message: str) -> None:
    if not value:
        fail(message)


def validate_schema_surfaces() -> None:
    for path in [CONTROL_SCHEMA, ENDPOINT_SCHEMA]:
        require_path(path)
        payload = load_json_object(path)
        required = payload.get("required", [])
        if not isinstance(required, list) or not required:
            fail(f"{rel(path)} must declare required fields")
    control = load_json_object(CONTROL_SCHEMA)
    required = set(control.get("required", []))
    for field in [
        "blocker_signature",
        "repetition_count",
        "required_artifact",
        "allowed_next_modes",
        "forbidden_next_modes",
        "promotion_condition",
        "demotion_condition",
        "quarantine_condition",
        "clay_progress_boundary",
    ]:
        require(field in required, f"{rel(CONTROL_SCHEMA)} missing required {field}")
    text = json.dumps(control)
    for mode in ALLOWED_NEXT_MODES:
        require(mode in text, f"{rel(CONTROL_SCHEMA)} does not expose allowed mode {mode}")
    for mode in FORBIDDEN_AFTER_REPETITION:
        require(mode in text, f"{rel(CONTROL_SCHEMA)} does not expose forbidden mode {mode}")


def validate_blocker_report() -> None:
    require_path(BLOCKER_REPORT)
    report = load_json_object(BLOCKER_REPORT)
    require(clean_text(report.get("target_id")) == YM_TARGET_ID, f"{rel(BLOCKER_REPORT)} wrong target")
    signatures = report.get("signatures", [])
    require(isinstance(signatures, list) and signatures, f"{rel(BLOCKER_REPORT)} has no signatures")
    endpoint = next((row for row in signatures if clean_text(row.get("blocker_signature")) == BLOCKER_ID), {})
    require(endpoint, f"{rel(BLOCKER_REPORT)} missing endpoint blocker signature")
    require(int(endpoint.get("repetition_count", 0) or 0) >= 3, "endpoint blocker repetition count must be >= 3")
    for field in ["first_cycle", "latest_cycle", "branch_ids", "missing_artifacts", "proposed_mode_switch", "blocker_kind"]:
        require(endpoint.get(field), f"endpoint blocker missing {field}")
    missing = {clean_text(item) for item in endpoint.get("missing_artifacts", [])}
    for marker in ["endpoint_source_table", "T_tail"]:
        require(marker in missing, f"endpoint blocker missing artifact marker {marker}")
    require(endpoint.get("proposed_mode_switch") == "artifact_sprint_required", "endpoint blocker must require artifact sprint")
    control = report.get("artifact_or_stop_control", {})
    require(control.get("broad_api_marathon_blocked") is True, "report must block broad endpoint API marathon")


def validate_endpoint_contract() -> None:
    require_path(ENDPOINT_CONTRACT_JSON)
    contract = load_json_object(ENDPOINT_CONTRACT_JSON)
    for field in load_json_object(ENDPOINT_SCHEMA).get("required", []):
        require(field in contract, f"{rel(ENDPOINT_CONTRACT_JSON)} missing {field}")
    samples = contract.get("seven_logZ_samples", [])
    require(isinstance(samples, list) and len(samples) == 7, "endpoint contract must contain exactly seven logZ samples")
    rules = contract.get("outcome_rules", {})
    for field in ["promote", "finite_falsifier", "quarantine"]:
        require(clean_text(rules.get(field)), f"endpoint contract missing outcome rule {field}")
    boundary = clean_text(contract.get("physical_relevance_boundary")).lower()
    for marker in ["continuum", "os/wightman", "spectral mass gap"]:
        require(marker in boundary, f"endpoint physical boundary must mention {marker}")
    status = contract.get("field_status", {})
    require(isinstance(status, dict) and "unknown" in status, "endpoint contract must type field status and unknowns")


def validate_endpoint_pilot_and_demotion() -> None:
    require_path(ENDPOINT_PILOT_JSON)
    pilot = load_json_object(ENDPOINT_PILOT_JSON)
    require(clean_text(pilot.get("target_id")) == YM_TARGET_ID, "pilot wrong target")
    require(clean_text(pilot.get("pilot_status")) in {"pilot_success", "needs_external_math", "underspecified_geometry", "impossible_current_route", "quarantine_recommended"}, "invalid pilot status")
    require(len(pilot.get("seven_source_sample_slots", [])) == 7, "pilot must record seven source sample slots")
    require(pilot.get("another_endpoint_marathon_allowed") is False, "pilot must decide another endpoint marathon is not allowed")
    require_path(DEMOTION_PACKET_JSON)
    demotion = load_json_object(DEMOTION_PACKET_JSON)
    for field in ["finite_support_value", "blocked_named_artifact", "release_to_exploration", "clay_progress_boundary"]:
        require(clean_text(demotion.get(field)), f"demotion packet missing {field}")
    require(demotion.get("no_nested_consolidation") is True, "demotion packet must block nested consolidation")


def validate_fixtures() -> None:
    expected = {
        "ym_endpoint_repeated_request_reject.json": False,
        "ym_endpoint_table_attach_accept.json": True,
        "ym_endpoint_quarantine_accept.json": True,
    }
    for name, valid in expected.items():
        path = FIXTURE_DIR / name
        require_path(path)
        packet = load_json_object(path)
        verdict = evaluate_artifact_or_stop_packet(packet)
        require(verdict["valid"] is valid, f"{rel(path)} expected valid={valid}, got {verdict}")
        if clean_text(packet.get("expected_verdict")):
            require(clean_text(verdict["verdict"]) == clean_text(packet.get("expected_verdict")), f"{rel(path)} expected verdict mismatch")
    require_path(GENERATIVE_FIXTURE)
    fixture_text = GENERATIVE_FIXTURE.read_text(encoding="utf-8")
    for marker in [
        "fluent packet with no endpoint artifact",
        "new wording of the same T_tail blocker",
        "table contract but no data",
        "negative I_gate interval",
        "physical impact without carrier",
    ]:
        require(marker in fixture_text, f"{rel(GENERATIVE_FIXTURE)} missing adversarial case marker `{marker}`")
    require_path(EXPECTED_VERDICTS)
    expected_payload = load_json_object(EXPECTED_VERDICTS)
    require(len(expected_payload.get("cases", [])) >= 5, "expected verdicts must cover at least five cases")


def main() -> int:
    validate_schema_surfaces()
    validate_blocker_report()
    validate_endpoint_contract()
    validate_endpoint_pilot_and_demotion()
    validate_fixtures()
    print("validated YM artifact-or-stop control, endpoint contract, pilot, demotion packet, and fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
