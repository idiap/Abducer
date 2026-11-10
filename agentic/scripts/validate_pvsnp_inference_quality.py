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
"""Validate P vs NP inference-quality packets and fixtures."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/pvsnp_inference_quality_packet.schema.json"
FIXTURE_DIR = ROOT / "agentic/fixtures/pvsnp_inference_quality"
REPORT = ROOT / "agentic/reports/discovery_marathon/latest.json"
DOMAIN_TERMS = {
    "sat",
    "np",
    "p/poly",
    "circuit",
    "size",
    "reduction",
    "transfer",
    "advice",
    "oracle",
    "natural",
    "mcsp",
    "mktp",
    "proof",
    "beta",
    "quantifier",
}
GENERIC_BARRIER_TRIGGERS = {
    "natural proofs applies",
    "relativization applies",
    "algebrization applies",
    "barrier applies",
}


def clean_lower(value: Any) -> str:
    return clean_text(value).lower()


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


def allowed(schema: dict[str, Any], key: str) -> set[str]:
    value = schema.get(key)
    if not isinstance(value, list):
        fail(f"{rel(SCHEMA)} missing allowed list {key}")
    return {str(item) for item in value}


def validate_packet(payload: dict[str, Any], source: Path, schema: dict[str, Any]) -> None:
    for field in schema["required_fields"]:
        if field not in payload:
            fail(f"{rel(source)} missing required field {field}")
    if payload.get("target_id") != schema["allowed_target_id"]:
        fail(f"{rel(source)} target_id must be {schema['allowed_target_id']}")
    for field in ["packet_id", "branch_id", "inference_id", "source_statement", "target_statement"]:
        require_nonempty(payload.get(field), source, field)

    inference_rule = clean_text(payload.get("inference_rule"))
    if inference_rule not in allowed(schema, "allowed_inference_rules"):
        fail(f"{rel(source)} invalid inference_rule {inference_rule}")
    if clean_text(payload).lower().count("p vs np") + sum(term in clean_text(payload).lower() for term in DOMAIN_TERMS) < 3:
        fail(f"{rel(source)} packet is not P vs NP-specific enough")

    model = require_dict(payload, source, "model_context")
    for field in ["source_carrier", "target_class", "circuit_model", "reduction_type", "oracle_status"]:
        require_nonempty(model.get(field), source, f"model_context.{field}")
    if model["reduction_type"] not in allowed(schema, "allowed_reduction_types"):
        fail(f"{rel(source)} invalid reduction_type {model['reduction_type']}")

    quantifiers = require_dict(payload, source, "quantifier_context")
    for field, allowed_key in [
        ("length_regime", "allowed_length_regimes"),
        ("exponent_regime", "allowed_exponent_regimes"),
        ("uniformity", "allowed_uniformity"),
        ("advice_status", "allowed_advice_status"),
    ]:
        require_nonempty(quantifiers.get(field), source, f"quantifier_context.{field}")
        if quantifiers[field] not in allowed(schema, allowed_key):
            fail(f"{rel(source)} invalid {field} {quantifiers[field]}")

    parameters = require_dict(payload, source, "parameter_map")
    require_nonempty(parameters.get("input_length_map"), source, "parameter_map.input_length_map")
    side_conditions = require_list(payload, source, "side_conditions")
    require_list(payload, source, "correctness_criteria")
    require_list(payload, source, "failure_modes")
    require_list(payload, source, "reviewer_findings", min_items=0)

    barrier = require_dict(payload, source, "barrier_status")
    barrier_families = barrier.get("barrier_families")
    if not isinstance(barrier_families, list) or not barrier_families:
        fail(f"{rel(source)} barrier_status.barrier_families must be a nonempty list")
    unknown_barriers = [item for item in barrier_families if item not in allowed(schema, "allowed_barrier_families")]
    if unknown_barriers:
        fail(f"{rel(source)} invalid barrier_families {unknown_barriers}")

    derivation = require_dict(payload, source, "derivation_status")
    require_nonempty(derivation.get("status"), source, "derivation_status.status")
    if derivation["status"] not in allowed(schema, "allowed_derivation_status"):
        fail(f"{rel(source)} invalid derivation status {derivation['status']}")
    if not isinstance(derivation.get("theorem_shape"), bool):
        fail(f"{rel(source)} derivation_status.theorem_shape must be boolean")
    decision = clean_text(payload.get("decision"))
    if decision not in allowed(schema, "allowed_decisions"):
        fail(f"{rel(source)} invalid decision {decision}")
    handoff = require_dict(payload, source, "validation_handoff")
    require_nonempty(handoff.get("validator"), source, "validation_handoff.validator")

    text = clean_lower(payload)
    if inference_rule in {"transfer_inequality", "reduction"}:
        if model.get("reduction_type") == "unknown":
            fail(f"{rel(source)} transfer/reduction claim cannot have unknown reduction_type")
        require_nonempty(parameters.get("transfer_formula"), source, "parameter_map.transfer_formula")
        if "source hardness implies sat hardness" in clean_lower(parameters.get("transfer_formula")):
            fail(f"{rel(source)} transfer formula appears to reverse source-to-target implication without proof")
        if not any(token in clean_lower(parameters.get("transfer_formula")) for token in ["if", "then", "=>", "implies"]):
            fail(f"{rel(source)} transfer formula must express an implication")

    if quantifiers.get("advice_status") in {"hidden_advice_risk", "advice_leak_detected"} and decision == "accept_for_derivation":
        fail(f"{rel(source)} advice leak cannot be accepted for derivation without repair")

    trigger = clean_lower(barrier.get("trigger"))
    if trigger in GENERIC_BARRIER_TRIGGERS:
        fail(f"{rel(source)} barrier trigger is generic; name route-specific trigger conditions")
    if "natural_proofs" in barrier_families:
        barrier_text = clean_lower(barrier) + " " + " ".join(clean_lower(item) for item in side_conditions)
        for marker in ["largeness", "constructivity", "usefulness"]:
            if marker not in barrier_text:
                fail(f"{rel(source)} natural-proofs barrier missing {marker} check")

    if derivation.get("theorem_shape"):
        if derivation["status"] in {"heuristic_only", "invalid"}:
            fail(f"{rel(source)} theorem-shaped claim cannot have derivation status {derivation['status']}")
        if derivation["status"] in {"derivation_needed", "blocked_at_named_lemma"} and not clean_text(derivation.get("blocked_obligation")):
            fail(f"{rel(source)} theorem-shaped incomplete derivation needs blocked_obligation")

    if decision in {"accept_for_derivation", "review_only"} and not clean_text(handoff.get("next_skill")):
        fail(f"{rel(source)} accepted/reviewed packet needs validation_handoff.next_skill")


def discover_packets(payload: Any) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        candidate = payload.get("pvsnp_inference_quality")
        if isinstance(candidate, dict):
            packets.append(candidate)
        if isinstance(candidate, list):
            packets.extend(item for item in candidate if isinstance(item, dict))
        for key in ["inference_quality_packets", "packets"]:
            value = payload.get(key)
            if isinstance(value, list):
                packets.extend(item for item in value if isinstance(item, dict))
        for value in payload.values():
            if isinstance(value, (dict, list)):
                packets.extend(discover_packets(value))
    elif isinstance(payload, list):
        for item in payload:
            packets.extend(discover_packets(item))
    return packets


def validate_path(path: Path, schema: dict[str, Any]) -> int:
    payload = load_json_object(path)
    if "packet_id" in payload:
        validate_packet(payload, path, schema)
        return 1
    packets = discover_packets(payload)
    for packet in packets:
        validate_packet(packet, path, schema)
    return len(packets)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    schema = load_json_object(SCHEMA)
    checked = 0
    if args.paths:
        for raw in args.paths:
            checked += validate_path(Path(raw), schema)
        print(f"validated {checked} P vs NP inference-quality packet(s)")
        return 0

    valid = FIXTURE_DIR / "valid_transfer_packet.json"
    validate_packet(load_json_object(valid), valid, schema)
    checked += 1
    for invalid in sorted(FIXTURE_DIR.glob("invalid_*_packet.json")):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                validate_packet(load_json_object(invalid), invalid, schema)
        except SystemExit:
            continue
        fail(f"{rel(invalid)} should fail validation")

    if REPORT.exists():
        checked += validate_path(REPORT, schema)
    print(f"validated {checked} P vs NP inference-quality packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
