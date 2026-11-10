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
"""Validate qualitative physics relation packets."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_array, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/qualitative_physics_relation_packet.schema.json"
DEFAULT_PACKET = ROOT / "agentic/reports/qualitative_relation_packets/latest.json"


def rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("packets"), list):
        return [row for row in payload["packets"] if isinstance(row, dict)]
    if isinstance(payload, dict):
        return [payload]
    return []


def require_fields(item: dict[str, Any], fields: list[str], source: Path, subject: str) -> None:
    for field in fields:
        if field not in item:
            fail(f"{rel(source)} {subject} missing `{field}`")


def validate_packet(packet: dict[str, Any], source: Path, schema: dict[str, Any]) -> None:
    require_fields(packet, schema["required_fields"], source, "packet")
    if not packet.get("source_artifacts"):
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs source_artifacts")
    allowed_status = set(schema["allowed_epistemic_status"])
    if packet.get("epistemic_status") not in allowed_status:
        fail(f"{rel(source)} packet {packet.get('packet_id')} invalid epistemic_status")
    variables = packet.get("variables", [])
    regimes = packet.get("regimes", [])
    relations = packet.get("relations", [])
    if not isinstance(variables, list) or len(variables) < 2:
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs at least two variables")
    if not isinstance(regimes, list) or not regimes:
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs regimes")
    if not isinstance(relations, list) or not relations:
        fail(f"{rel(source)} packet {packet.get('packet_id')} needs relations")
    variable_ids = set()
    for index, variable in enumerate(variables, start=1):
        if not isinstance(variable, dict):
            fail(f"{rel(source)} variable {index} must be an object")
        require_fields(variable, schema["variable_required_fields"], source, f"variable {index}")
        variable_ids.add(clean_text(variable["id"]))
        if variable.get("independent_or_dependent") not in schema["allowed_variable_dependence"]:
            fail(f"{rel(source)} variable {variable.get('id')} invalid independent_or_dependent")
        if not variable.get("source_artifacts"):
            fail(f"{rel(source)} variable {variable.get('id')} needs source_artifacts")
    regime_ids = set()
    for index, regime in enumerate(regimes, start=1):
        if not isinstance(regime, dict):
            fail(f"{rel(source)} regime {index} must be an object")
        require_fields(regime, schema["regime_required_fields"], source, f"regime {index}")
        regime_ids.add(clean_text(regime["id"]))
    for index, relation in enumerate(relations, start=1):
        if not isinstance(relation, dict):
            fail(f"{rel(source)} relation {index} must be an object")
        require_fields(relation, schema["relation_required_fields"], source, f"relation {index}")
        if relation.get("relation_kind") not in schema["allowed_relation_kinds"]:
            fail(f"{rel(source)} relation {relation.get('id')} invalid relation_kind")
        if relation.get("epistemic_status") not in allowed_status:
            fail(f"{rel(source)} relation {relation.get('id')} invalid epistemic_status")
        if clean_text(relation.get("source_variable")) not in variable_ids:
            fail(f"{rel(source)} relation {relation.get('id')} source_variable not found")
        if clean_text(relation.get("target_variable")) not in variable_ids:
            fail(f"{rel(source)} relation {relation.get('id')} target_variable not found")
        if not set(relation.get("valid_regime_ids", [])) <= regime_ids:
            fail(f"{rel(source)} relation {relation.get('id')} references unknown regime")
        for list_field in ["assumptions", "failure_modes", "evidence_paths"]:
            if not isinstance(relation.get(list_field), list) or not relation[list_field]:
                fail(f"{rel(source)} relation {relation.get('id')} needs {list_field}")
        text = clean_text(relation).lower()
        if "proof" in text and relation.get("epistemic_status") in {"heuristic", "conjectural"} and "proof_obligation" not in text:
            fail(f"{rel(source)} relation {relation.get('id')} risks proof overclaim")


def load_payload(path: Path) -> Any:
    if path.name.endswith(".json") or path.suffix in {".yaml", ".yml"}:
        payload = load_json_object(path) if path.read_text(encoding="utf-8").lstrip().startswith("{") else load_json_array(path)
        return payload
    return load_json_object(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    schema = load_json_object(SCHEMA)
    paths = [ROOT / path if not Path(path).is_absolute() else Path(path) for path in args.paths]
    if not paths:
        if not DEFAULT_PACKET.exists():
            print("No qualitative relation packet report yet; validator is idle.")
            return 0
        paths = [DEFAULT_PACKET]
    count = 0
    for path in paths:
        payload = load_payload(path)
        rows = rows_from_payload(payload)
        if not rows:
            fail(f"{rel(path)} contains no qualitative relation packets")
        for row in rows:
            validate_packet(row, path, schema)
            count += 1
    if not args.paths:
        fixtures = ROOT / "tests/fixtures/qualitative_physics"
        for fixture in sorted(fixtures.glob("*_probe.json")) + [fixtures / "valid_packet.json"]:
            if fixture.exists():
                for row in rows_from_payload(load_payload(fixture)):
                    validate_packet(row, fixture, schema)
                    count += 1
        for fixture in [fixtures / "invalid_missing_regime.json", fixtures / "invalid_missing_evidence.json"]:
            if fixture.exists():
                try:
                    with contextlib.redirect_stderr(io.StringIO()):
                        for row in rows_from_payload(load_payload(fixture)):
                            validate_packet(row, fixture, schema)
                except SystemExit:
                    pass
                else:
                    fail(f"{rel(fixture)} should fail qualitative relation validation")
    print(f"validated {count} qualitative relation packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
