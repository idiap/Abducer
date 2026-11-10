#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate Abducer hypothesis exploration artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path
from abstraction_machinery_selection import validate_machinery_shape
from formal_subgoal_control import validate_control_shape


SCHEMA = ROOT / "agentic/spec/hypothesis_exploration_map.schema.json"
CONTROL_SCHEMA = ROOT / "agentic/spec/formal_subgoal_control.schema.json"


DISPOSITION_DECISION_COMPATIBILITY = {
    "proof_queue": {"persist_adapt"},
    "discovery_branch": {"persist_adapt"},
    "revision_loop": {"backtrack", "persist_adapt"},
    "evidence_task": {"quarantine", "persist_adapt"},
    "quarantine": {"quarantine"},
    "reject": {"stop", "quarantine"},
    "stop": {"stop"},
}


def require_object_list(payload: dict[str, Any], key: str, path: Path) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        fail(f"{rel(path)} missing list field: {key}")
    rows = []
    for row in value:
        if not isinstance(row, dict):
            fail(f"{rel(path)} {key} entries must be objects")
        rows.append(row)
    return rows


def require_fields(row: dict[str, Any], fields: list[str], *, label: str, path: Path) -> None:
    for field in fields:
        if field not in row:
            fail(f"{rel(path)} {label} missing {field}: {row.get('candidate_id') or row.get('pressure_id') or row}")


def validate_map(path: Path) -> dict[str, Any]:
    schema = load_json_object(SCHEMA)
    control_schema = load_json_object(CONTROL_SCHEMA)
    payload = load_json_object(path)
    for field in schema["required_fields"]:
        if field not in payload:
            fail(f"{rel(path)} missing required field: {field}")
    repo_path(str(payload["kb_path"]), must_exist=True)
    repo_path(str(payload["source_graph"]), must_exist=True)
    allowed_pressure = set(schema["allowed_pressure_types"])
    allowed_epistemic = set(schema["allowed_epistemic_status"])
    allowed_dispositions = set(schema["allowed_dispositions"])
    allowed_control_decisions = set(control_schema["allowed_decisions"])
    operation_ids = {row["id"] for row in require_object_list(payload, "creative_operations", path)}
    if len(operation_ids) < 10:
        fail(f"{rel(path)} must define the full conceptual creativity operation set")
    pressures = require_object_list(payload, "pressure_packets", path)
    pressure_ids = set()
    for row in pressures:
        require_fields(row, load_json_object(ROOT / "agentic/spec/conceptual_pressure_packet.schema.json")["required_fields"], label="pressure", path=path)
        pressure_id = clean_text(row["pressure_id"])
        if not pressure_id or pressure_id in pressure_ids:
            fail(f"{rel(path)} missing or duplicate pressure_id: {pressure_id}")
        pressure_ids.add(pressure_id)
        if row["pressure_type"] not in allowed_pressure:
            fail(f"{rel(path)} pressure {pressure_id} invalid type: {row['pressure_type']}")
        if not row["source_artifacts"]:
            fail(f"{rel(path)} pressure {pressure_id} lacks source artifacts")
    candidates = require_object_list(payload, "mediation_candidates", path)
    candidate_ids = set()
    seen_operations = set()
    for row in candidates:
        require_fields(row, schema["required_candidate_fields"], label="candidate", path=path)
        candidate_id = clean_text(row["candidate_id"])
        if not candidate_id or candidate_id in candidate_ids:
            fail(f"{rel(path)} missing or duplicate candidate_id: {candidate_id}")
        candidate_ids.add(candidate_id)
        if row["creative_operation"] not in operation_ids:
            fail(f"{rel(path)} candidate {candidate_id} unknown operation: {row['creative_operation']}")
        seen_operations.add(row["creative_operation"])
        if row["epistemic_status"] not in allowed_epistemic:
            fail(f"{rel(path)} candidate {candidate_id} invalid epistemic status: {row['epistemic_status']}")
        ok, reason = validate_control_shape(row.get("subgoal_control"))
        if not ok:
            fail(f"{rel(path)} candidate {candidate_id} invalid subgoal_control: {reason}")
        if row["subgoal_control"]["decision"] not in allowed_control_decisions:
            fail(f"{rel(path)} candidate {candidate_id} invalid control decision: {row['subgoal_control']['decision']}")
        ok, reason = validate_machinery_shape(row.get("machinery_selection"))
        if not ok:
            fail(f"{rel(path)} candidate {candidate_id} invalid machinery_selection: {reason}")
        if "->" not in row["machinery_selection"].get("controlled_interface", ""):
            fail(f"{rel(path)} candidate {candidate_id} machinery_selection must state a controlled interface arrow")
        for pressure_id in row["source_pressure_ids"]:
            if pressure_id not in pressure_ids:
                fail(f"{rel(path)} candidate {candidate_id} references unknown pressure: {pressure_id}")
        if not row["validation_requirements"]:
            fail(f"{rel(path)} candidate {candidate_id} lacks validation requirements")
    if len(seen_operations) < 4:
        fail(f"{rel(path)} expected diverse creative operations, saw {sorted(seen_operations)}")
    validations = require_object_list(payload, "validation_packets", path)
    validation_by_candidate = {}
    for row in validations:
        require_fields(row, schema["required_validation_fields"], label="validation", path=path)
        if row["candidate_id"] not in candidate_ids:
            fail(f"{rel(path)} validation references unknown candidate: {row['candidate_id']}")
        validation_by_candidate[row["candidate_id"]] = row
        if row["route_disposition"] not in allowed_dispositions:
            fail(f"{rel(path)} validation invalid disposition: {row['route_disposition']}")
        ok, reason = validate_control_shape(row.get("subgoal_control"))
        if not ok:
            fail(f"{rel(path)} validation {row['packet_id']} invalid subgoal_control: {reason}")
        ok, reason = validate_machinery_shape(row.get("machinery_selection"))
        if not ok:
            fail(f"{rel(path)} validation {row['packet_id']} invalid machinery_selection: {reason}")
        hard_gates = row.get("hard_gates")
        if not isinstance(hard_gates, dict) or set(hard_gates) != set(load_json_object(ROOT / "agentic/spec/abducer_validation_packet.schema.json")["hard_gates"]):
            fail(f"{rel(path)} validation {row['packet_id']} has incomplete hard gates")
        if "fail" in hard_gates.values() and row["route_disposition"] not in {"quarantine", "reject"}:
            fail(f"{rel(path)} failed hard gate must quarantine or reject: {row['packet_id']}")
    if set(validation_by_candidate) != candidate_ids:
        fail(f"{rel(path)} not every candidate has a validation packet")
    rankings = require_object_list(payload, "candidate_rankings", path)
    dispositions = set()
    for row in rankings:
        require_fields(row, schema["required_ranking_fields"], label="ranking", path=path)
        if row["candidate_id"] not in candidate_ids:
            fail(f"{rel(path)} ranking references unknown candidate: {row['candidate_id']}")
        if row["route_disposition"] not in allowed_dispositions:
            fail(f"{rel(path)} ranking invalid disposition: {row['route_disposition']}")
        ok, reason = validate_control_shape(row.get("subgoal_control"))
        if not ok:
            fail(f"{rel(path)} ranking {row['ranking_id']} invalid subgoal_control: {reason}")
        ok, reason = validate_machinery_shape(row.get("machinery_selection"))
        if not ok:
            fail(f"{rel(path)} ranking {row['ranking_id']} invalid machinery_selection: {reason}")
        if row["route_disposition"] == "proof_queue" and row["machinery_selection"].get("machinery_role") == "obstruction":
            fail(f"{rel(path)} ranking {row['ranking_id']} proof_queue cannot be driven by untyped obstruction machinery")
        decision = row["subgoal_control"]["decision"]
        compatible = DISPOSITION_DECISION_COMPATIBILITY[row["route_disposition"]]
        if decision not in compatible:
            fail(
                f"{rel(path)} ranking {row['ranking_id']} incompatible disposition/control: "
                f"{row['route_disposition']} vs {decision}"
            )
        if decision == "persist_adapt" and int(row["subgoal_control"].get("repeated_blocker_count", 0)) >= 2:
            fail(f"{rel(path)} ranking {row['ranking_id']} repeats blockers while persisting without action")
        dispositions.add(row["route_disposition"])
        if not row["changed_routing_decision"]:
            fail(f"{rel(path)} ranking must record route-changing behavior: {row['ranking_id']}")
    if len(dispositions) < 2:
        fail(f"{rel(path)} expected multiple route dispositions, saw {sorted(dispositions)}")
    trace = payload["refinement_trace"]
    if not isinstance(trace, dict) or not trace.get("cycles"):
        fail(f"{rel(path)} missing refinement trace cycles")
    summary = payload["summary"]
    if summary.get("candidate_count") != len(candidates):
        fail(f"{rel(path)} summary candidate_count mismatch")
    if summary.get("route_changing_candidates", 0) < 1:
        fail(f"{rel(path)} expected route-changing candidates")
    return {"path": rel(path), "candidates": len(candidates), "dispositions": sorted(dispositions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maps", nargs="*", default=[])
    args = parser.parse_args()
    paths = [Path(raw) for raw in args.maps] or [ROOT / "artifacts/hegelian/hypothesis_exploration_map.json"]
    for path in paths:
        row = validate_map(path)
        print(f"validated hypothesis exploration map {row['path']} ({row['candidates']} candidates, dispositions={row['dispositions']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
