#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate Abducer Looper target packets."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, parse_kb_statements, rel, repo_path


SCHEMA = ROOT / "agentic" / "spec" / "target_packet_schema.json"


def _require_string(packet: dict[str, Any], key: str, path: Path) -> str:
    value = packet.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{rel(path)} missing non-empty string field: {key}")
    return value


def _require_list(packet: dict[str, Any], key: str, path: Path) -> list[Any]:
    value = packet.get(key)
    if not isinstance(value, list):
        fail(f"{rel(path)} missing list field: {key}")
    return value


def validate_packet(path: Path) -> dict[str, Any]:
    schema = load_json_object(SCHEMA)
    packet = load_json_object(path)
    for field in schema["required_fields"]:
        if field not in packet:
            fail(f"{rel(path)} missing required field: {field}")

    target_id = _require_string(packet, "target_id", path)
    _require_string(packet, "raw_goal", path)
    desired_output = _require_string(packet, "desired_output_type", path)
    if desired_output not in schema["allowed_output_types"]:
        fail(f"{rel(path)} has unsupported desired_output_type: {desired_output}")

    kb = repo_path(_require_string(packet, "kb_path", path), must_exist=True)
    statements = parse_kb_statements(kb)
    main_claim_ids = _require_list(packet, "main_claim_ids", path)
    if not main_claim_ids:
        fail(f"{rel(path)} must name at least one main_claim_id")
    for claim_id in main_claim_ids:
        if not isinstance(claim_id, str) or claim_id not in statements:
            fail(f"{rel(path)} main_claim_id not found in {rel(kb)}: {claim_id}")

    quality_criteria = _require_list(packet, "quality_criteria", path)
    if not quality_criteria:
        fail(f"{rel(path)} needs at least one quality criterion")
    for row in quality_criteria:
        if not isinstance(row, dict):
            fail(f"{rel(path)} quality_criteria entries must be objects")
        for field in schema["quality_criterion_required_fields"]:
            if not clean_text(row.get(field)):
                fail(f"{rel(path)} quality criterion missing {field}")

    gates = _require_list(packet, "acceptance_gates", path)
    if not gates:
        fail(f"{rel(path)} needs at least one acceptance gate")
    blocking = 0
    for row in gates:
        if not isinstance(row, dict):
            fail(f"{rel(path)} acceptance_gates entries must be objects")
        for field in schema["acceptance_gate_required_fields"]:
            if field not in row:
                fail(f"{rel(path)} acceptance gate missing {field}")
        evidence = row.get("required_evidence")
        if not isinstance(evidence, list) or not evidence:
            fail(f"{rel(path)} acceptance gate {row.get('gate_id')} needs required_evidence")
        if bool(row.get("blocks_release")):
            blocking += 1
    if blocking == 0:
        fail(f"{rel(path)} must include at least one blocking acceptance gate")

    validation_targets = _require_list(packet, "validation_targets", path)
    for row in validation_targets:
        if not isinstance(row, dict):
            fail(f"{rel(path)} validation_targets entries must be objects")
        for field in schema["validation_target_required_fields"]:
            if not clean_text(row.get(field)):
                fail(f"{rel(path)} validation target missing {field}")

    evidence_paths = _require_list(packet, "evidence_paths", path)
    missing_evidence = []
    for raw in evidence_paths:
        if not isinstance(raw, str):
            fail(f"{rel(path)} evidence_paths entries must be strings")
        candidate = repo_path(raw)
        if not candidate.exists():
            missing_evidence.append(raw)
    if missing_evidence:
        fail(f"{rel(path)} has missing evidence paths: {', '.join(missing_evidence)}")

    for field in ["known_constraints", "unknowns"]:
        value = _require_list(packet, field, path)
        if not all(isinstance(item, str) and item.strip() for item in value):
            fail(f"{rel(path)} {field} must contain non-empty strings")

    return {"target_id": target_id, "kb_path": rel(kb), "main_claim_count": len(main_claim_ids)}


def discover_default_packets() -> list[Path]:
    paths = sorted((ROOT / "agentic" / "examples" / "targets").glob("*.json"))
    current = ROOT / "agentic" / "state" / "current_target.json"
    if current.exists():
        paths.append(current)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packets", nargs="*", help="Target packet paths. Defaults to agentic examples and current target.")
    args = parser.parse_args()

    paths = [Path(raw) for raw in args.packets] if args.packets else discover_default_packets()
    if not paths:
        fail("no target packets found")
    rows = [validate_packet(path) for path in paths]
    for row in rows:
        print(f"validated target {row['target_id']} ({row['main_claim_count']} claims) from {row['kb_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
