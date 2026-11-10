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
"""Validate proof-depth control packets and anti-definitionality fixtures."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from proof_depth_control import PROMOTION_DECISIONS, QUALITY_DIMS, discover_proof_depth_packets


SCHEMA = ROOT / "agentic/spec/proof_depth_control.schema.json"
TRANSFER_SCHEMA = ROOT / "agentic/spec/proof_transfer_substance_audit.schema.json"
FIXTURE_DIR = ROOT / "tests/fixtures/proof_depth"
REPORT = ROOT / "agentic/reports/discovery_marathon/latest.json"


def require_nonempty(value: Any, source: Path, field: str) -> None:
    if not clean_text(value):
        fail(f"{rel(source)} missing {field}")


def require_dict(payload: dict[str, Any], source: Path, field: str) -> dict[str, Any]:
    value = payload.get(field)
    if not isinstance(value, dict):
        fail(f"{rel(source)} {field} must be an object")
    return value


def require_list(payload: dict[str, Any], source: Path, field: str, *, min_items: int = 1) -> list[Any]:
    value = payload.get(field)
    if not isinstance(value, list) or len([item for item in value if clean_text(item)]) < min_items:
        fail(f"{rel(source)} {field} must contain at least {min_items} nonempty item(s)")
    return value


def validate_quality_vector(vector: dict[str, Any], source: Path) -> None:
    for dim in QUALITY_DIMS:
        if dim not in vector:
            fail(f"{rel(source)} conceptual_quality_vector missing {dim}")
        item = vector[dim]
        if not isinstance(item, dict):
            fail(f"{rel(source)} conceptual_quality_vector.{dim} must be an object")
        for field in ["score", "evidence", "missing_evidence", "scope", "demotion_trigger"]:
            require_nonempty(item.get(field), source, f"conceptual_quality_vector.{dim}.{field}")
        try:
            score = int(item.get("score"))
        except (TypeError, ValueError):
            fail(f"{rel(source)} conceptual_quality_vector.{dim}.score must be an integer")
        if score < 0 or score > 5:
            fail(f"{rel(source)} conceptual_quality_vector.{dim}.score must be between 0 and 5")


def validate_transfer_audit(audit: dict[str, Any], source: Path, release_decision: str) -> None:
    transfer_schema = load_json_object(TRANSFER_SCHEMA)
    for field in transfer_schema["required_fields"]:
        require_nonempty(audit.get(field), source, f"transfer_substance_audit.{field}")
    verdict = clean_text(audit.get("verdict"))
    allowed = set(load_json_object(SCHEMA)["allowed_transfer_substance_verdicts"])
    if verdict not in allowed:
        fail(f"{rel(source)} invalid transfer substance verdict {verdict}")
    if release_decision in PROMOTION_DECISIONS and verdict not in set(transfer_schema["promotion_allowed_verdicts"]):
        fail(f"{rel(source)} cannot promote release_decision={release_decision} with transfer verdict {verdict}")
    if release_decision in PROMOTION_DECISIONS and verdict == "substantive_transfer":
        for field in ["stress_case_test", "failure_case_test", "consequence_delta", "prior_art_delta"]:
            text = clean_text(audit.get(field)).lower()
            if text.startswith("missing") or text.startswith("pending"):
                fail(f"{rel(source)} promoted transfer missing substantive {field}")


def validate_learning_event(event: dict[str, Any], source: Path, target_id: str) -> None:
    schema = load_json_object(ROOT / "agentic/spec/proof_inference_learning_event.schema.json")
    for field in schema["required_fields"]:
        require_nonempty(event.get(field), source, f"declarative_learning_event.{field}")
    if clean_text(event.get("target_id")) != target_id:
        fail(f"{rel(source)} learning event target_id does not match packet target_id")
    if clean_text(event.get("epistemic_status")) not in set(schema["allowed_event_types"]):
        fail(f"{rel(source)} invalid learning event epistemic_status {event.get('epistemic_status')}")


def validate_packet(packet: dict[str, Any], source: Path) -> None:
    schema = load_json_object(SCHEMA)
    for field in schema["required_fields"]:
        require_nonempty(packet.get(field), source, field)
    target_id = clean_text(packet.get("target_id"))
    if clean_text(packet.get("pressure_kind")) not in set(schema["allowed_pressure_kinds"]):
        fail(f"{rel(source)} invalid pressure_kind {packet.get('pressure_kind')}")
    release_decision = clean_text(packet.get("release_decision"))
    if release_decision not in set(schema["allowed_release_decisions"]):
        fail(f"{rel(source)} invalid release_decision {release_decision}")
    require_list(packet, source, "evidence")
    quality = require_dict(packet, source, "conceptual_quality_vector")
    validate_quality_vector(quality, source)
    transfer_audit = require_dict(packet, source, "transfer_substance_audit")
    validate_transfer_audit(transfer_audit, source, release_decision)
    same_domain = require_dict(packet, source, "same_domain_transfer_audit")
    for field in ["source_object", "target_object", "same_domain_status", "stress_or_failure_case", "validation_handoff"]:
        require_nonempty(same_domain.get(field), source, f"same_domain_transfer_audit.{field}")
    learning = require_dict(packet, source, "declarative_learning_event")
    validate_learning_event(learning, source, target_id)
    if release_decision in PROMOTION_DECISIONS:
        if clean_text(packet.get("nontriviality_status")) != "load_bearing":
            fail(f"{rel(source)} promoted packet must have nontriviality_status load_bearing")
        if clean_text(packet.get("depth_delta")) == "support_only_or_demoted":
            fail(f"{rel(source)} promoted packet cannot have support-only depth_delta")


def validate_path(path: Path) -> int:
    payload = load_json_object(path)
    if "packet_id" in payload and "release_decision" in payload:
        validate_packet(payload, path)
        return 1
    packets = discover_proof_depth_packets(payload)
    for packet in packets:
        validate_packet(packet, path)
    return len(packets)


def expect_invalid(path: Path) -> None:
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            validate_path(path)
    except SystemExit:
        return
    fail(f"{rel(path)} should fail proof-depth validation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    checked = 0
    if args.paths:
        for raw in args.paths:
            count = validate_path(Path(raw))
            if count == 0:
                fail(f"{raw} did not contain proof-depth packets")
            checked += count
        print(f"validated {checked} proof-depth packet(s)")
        return 0

    for valid in [
        "substantive_transfer_theorem_accept.json",
        "yang_mills_routea_geometric_gate.json",
        "pvsnp_carrier_uniformity_gate.json",
    ]:
        checked += validate_path(FIXTURE_DIR / valid)
    for invalid in ["definitional_transfer_theorem_reject.json", "yang_mills_routea_shallow_endpoint.json"]:
        expect_invalid(FIXTURE_DIR / invalid)
    if REPORT.exists():
        checked += validate_path(REPORT)
    print(f"validated {checked} proof-depth packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
