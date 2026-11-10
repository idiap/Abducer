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
"""Validate Gedanken experiment packets."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/gedanken_experiment_packet.schema.json"
DEFAULT = ROOT / "agentic/reports/gedanken_experiments/latest.json"


def rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("packets"), list):
        return [row for row in payload["packets"] if isinstance(row, dict)]
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    return []


def require_fields(item: dict[str, Any], fields: list[str], source: Path, subject: str) -> None:
    for field in fields:
        if field not in item:
            fail(f"{rel(source)} {subject} missing `{field}`")


def require_nonempty_list(item: dict[str, Any], field: str, source: Path, subject: str) -> None:
    if not isinstance(item.get(field), list) or not item[field]:
        fail(f"{rel(source)} {subject} needs non-empty `{field}`")


def validate_packet(packet: dict[str, Any], source: Path, schema: dict[str, Any]) -> None:
    require_fields(packet, schema["required_fields"], source, "packet")
    if packet.get("need_decision") not in schema["allowed_need_decisions"]:
        fail(f"{rel(source)} packet {packet.get('packet_id')} invalid need_decision")
    if packet.get("epistemic_status") not in schema["allowed_epistemic_status"]:
        fail(f"{rel(source)} packet {packet.get('packet_id')} invalid epistemic_status")
    if packet.get("graph_update_action") not in schema["allowed_graph_update_actions"]:
        fail(f"{rel(source)} packet {packet.get('packet_id')} invalid graph_update_action")
    for field in ["source_artifacts", "originating_cycle_ids", "originating_branch_ids", "trigger_criteria", "variables", "interventions", "expected_observations", "variants", "insight_hypotheses", "followup_cycle_tasks", "failure_modes"]:
        require_nonempty_list(packet, field, source, f"packet {packet.get('packet_id')}")
    need = packet.get("need_assessment", {})
    if not isinstance(need, dict):
        fail(f"{rel(source)} packet {packet.get('packet_id')} need_assessment must be an object")
    require_fields(need, schema["need_assessment_required_fields"], source, "need_assessment")
    if need.get("decision") != packet.get("need_decision"):
        fail(f"{rel(source)} packet {packet.get('packet_id')} need_assessment decision does not match need_decision")
    for list_field in ["criteria_met", "criteria_missing", "rejected_alternatives"]:
        require_nonempty_list(need, list_field, source, "need_assessment")
    if packet.get("need_decision") == "design_now":
        if len(need.get("criteria_met", [])) < 2:
            fail(f"{rel(source)} packet {packet.get('packet_id')} design_now needs at least two criteria_met")
        if len(need.get("rejected_alternatives", [])) < 1:
            fail(f"{rel(source)} packet {packet.get('packet_id')} design_now needs rejected_alternatives")
        if not clean_text(need.get("why_not_direct_derivation_or_probe")):
            fail(f"{rel(source)} packet {packet.get('packet_id')} design_now needs why_not_direct_derivation_or_probe")
    situation = packet.get("situation", {})
    if not isinstance(situation, dict):
        fail(f"{rel(source)} packet {packet.get('packet_id')} situation must be an object")
    require_fields(situation, schema["situation_required_fields"], source, "situation")
    if len(clean_text(situation.get("why_this_situation_is_informative")).split()) < 8:
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs a substantive informativeness rationale")
    if not isinstance(situation.get("non_claims"), list) or len(situation["non_claims"]) < 2:
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs non_claims to prevent overclaim")
    for index, variable in enumerate(packet["variables"], start=1):
        if not isinstance(variable, dict):
            fail(f"{rel(source)} variable {index} must be an object")
        require_fields(variable, schema["variable_required_fields"], source, f"variable {index}")
    for index, intervention in enumerate(packet["interventions"], start=1):
        if not isinstance(intervention, dict):
            fail(f"{rel(source)} intervention {index} must be an object")
        require_fields(intervention, schema["intervention_required_fields"], source, f"intervention {index}")
        if not isinstance(intervention.get("held_fixed"), list) or not intervention["held_fixed"]:
            fail(f"{rel(source)} intervention {index} needs held_fixed controls")
    for index, observation in enumerate(packet["expected_observations"], start=1):
        if not isinstance(observation, dict):
            fail(f"{rel(source)} observation {index} must be an object")
        require_fields(observation, schema["observation_required_fields"], source, f"observation {index}")
        if clean_text(observation.get("what_would_disconfirm_it")).lower() in {"nothing", "none", "not applicable", "n/a"}:
            fail(f"{rel(source)} observation {index} needs a real disconfirming condition")
    for index, variant in enumerate(packet["variants"], start=1):
        if not isinstance(variant, dict):
            fail(f"{rel(source)} variant {index} must be an object")
        require_fields(variant, schema["variant_required_fields"], source, f"variant {index}")
        if clean_text(variant.get("predicted_change")).lower() in {"none", "no change", "same", "unchanged"}:
            fail(f"{rel(source)} variant {index} needs a diagnostic predicted_change")
        if len(clean_text(variant.get("reason_for_variant")).split()) < 3:
            fail(f"{rel(source)} variant {index} needs a substantive reason_for_variant")
    transfer = packet.get("transfer_scope", {})
    if not isinstance(transfer, dict):
        fail(f"{rel(source)} packet {packet.get('packet_id')} transfer_scope must be an object")
    for field in ["transfer_verdict", "transfers", "does_not_transfer", "transfer_certificate_needed"]:
        if not clean_text(transfer.get(field)):
            fail(f"{rel(source)} packet {packet.get('packet_id')} transfer_scope missing `{field}`")
    if packet.get("graph_update_action") != "none":
        if not packet.get("affected_edge_ids") and not packet.get("affected_node_ids"):
            fail(f"{rel(source)} packet {packet.get('packet_id')} graph update needs affected nodes or edges")
        if not isinstance(packet.get("proposed_graph_updates"), list) or not packet["proposed_graph_updates"]:
            fail(f"{rel(source)} packet {packet.get('packet_id')} graph update needs proposed_graph_updates")
    if packet.get("need_decision") == "quarantine_as_analogy" and transfer.get("transfer_verdict") != "quarantine":
        fail(f"{rel(source)} packet {packet.get('packet_id')} quarantine_as_analogy needs quarantine transfer verdict")
    for index, task in enumerate(packet["followup_cycle_tasks"], start=1):
        if not isinstance(task, dict):
            fail(f"{rel(source)} followup task {index} must be an object")
        require_fields(task, schema["followup_required_fields"], source, f"followup task {index}")
        if task["action"] not in schema["allowed_followup_actions"]:
            fail(f"{rel(source)} followup task {index} invalid action")
        if not isinstance(task.get("required_skills"), list) or not task["required_skills"]:
            fail(f"{rel(source)} followup task {index} needs required_skills")
        if task.get("packet_id") != packet.get("packet_id"):
            fail(f"{rel(source)} followup task {index} packet_id does not match packet")
        for field in ["success_criterion", "failure_or_demotion_criterion", "transfer_verdict", "situation_title"]:
            if not clean_text(task.get(field)):
                fail(f"{rel(source)} followup task {index} missing actionable {field}")
    text = clean_text(packet).lower()
    for marker in ["transfer", "does not", "follow", "disconfirm", "validity"]:
        if marker not in text:
            fail(f"{rel(source)} packet {packet.get('packet_id')} lacks marker `{marker}`")
    forbidden = ["proves the theorem", "proof achieved", "solves yang-mills", "solves the target"]
    for phrase in forbidden:
        if phrase in text:
            fail(f"{rel(source)} packet {packet.get('packet_id')} overclaims: {phrase}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    schema = load_json_object(SCHEMA)
    paths = [ROOT / path if not Path(path).is_absolute() else Path(path) for path in args.paths]
    if not paths:
        if not DEFAULT.exists():
            print("No Gedanken experiment report yet; validator is idle.")
            return 0
        paths = [DEFAULT]
    count = 0
    for path in paths:
        rows = rows_from_payload(load_json_object(path))
        if not rows:
            fail(f"{rel(path)} contains no Gedanken experiment packets")
        for row in rows:
            validate_packet(row, path, schema)
            count += 1
    if not args.paths:
        fixture_dir = ROOT / "tests/fixtures/gedanken_experiments"
        for valid in sorted(fixture_dir.glob("valid*.json")):
            validate_packet(load_json_object(valid), valid, schema)
            count += 1
        for invalid in sorted(fixture_dir.glob("invalid*.json")):
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    validate_packet(load_json_object(invalid), invalid, schema)
            except SystemExit:
                pass
            else:
                fail(f"{rel(invalid)} should fail Gedanken validation")
    print(f"validated {count} Gedanken experiment packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
