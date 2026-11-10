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

"""Validate essential target ledgers and target-relevance route gates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, load_json_object, rel


SCHEMA = ROOT / "agentic/spec/essential_target_ledger.schema.json"
LEDGERS = ROOT / "agentic/state/essential_target_ledgers"
FIXTURES = ROOT / "tests/fixtures/skill-depth"
YANG_MILLS_REQUIRED = {
    "existence",
    "nontriviality",
    "os-wightman-adequacy",
    "continuum-limit",
    "positive-mass-gap",
}


def require_fields(path: Path, payload: dict[str, Any], fields: list[str], subject: str) -> None:
    for field in fields:
        if field not in payload:
            fail(f"{rel(path)} {subject} missing `{field}`")


def validate_ledger(path: Path, schema: dict[str, Any]) -> None:
    payload = load_json_object(path)
    require_fields(path, payload, schema["required_fields"], "ledger")
    contract = payload.get("target_object_contract")
    if not isinstance(contract, dict):
        fail(f"{rel(path)} target_object_contract must be an object")
    require_fields(path, contract, schema["required_target_object_contract_fields"], "target_object_contract")
    for field in ["exact_target_object", "success_condition"]:
        if not str(contract.get(field, "")).strip():
            fail(f"{rel(path)} target_object_contract `{field}` must be non-empty")
    for field in ["nonweakening_commitments", "forbidden_nearby_problems", "acceptable_weakenings"]:
        if not isinstance(contract.get(field), list) or not contract[field]:
            fail(f"{rel(path)} target_object_contract `{field}` must be a non-empty list")
    commitments = payload["essential_commitments"]
    if not isinstance(commitments, list) or not commitments:
        fail(f"{rel(path)} requires non-empty essential_commitments")
    commitment_ids = set()
    for commitment in commitments:
        if not isinstance(commitment, dict):
            fail(f"{rel(path)} commitment entries must be objects")
        require_fields(path, commitment, schema["required_commitment_fields"], "commitment")
        commitment_ids.add(commitment["id"])
    if payload["target_id"] == "yang-mills-existence-and-mass-gap":
        missing = sorted(YANG_MILLS_REQUIRED - commitment_ids)
        if missing:
            fail(f"{rel(path)} Yang-Mills ledger missing commitments: {', '.join(missing)}")
        contract_text = " ".join(
            [
                str(contract.get("exact_target_object", "")),
                str(contract.get("success_condition", "")),
                " ".join(str(item) for item in contract.get("forbidden_nearby_problems", [])),
            ]
        ).lower()
        for marker in ["r^4", "compact simple", "continuum", "fixed-lattice", "mass gap"]:
            if marker not in contract_text:
                fail(f"{rel(path)} Yang-Mills target_object_contract lacks `{marker}`")
        missing_contract_commitments = sorted(YANG_MILLS_REQUIRED - set(contract.get("nonweakening_commitments", [])))
        if missing_contract_commitments:
            fail(f"{rel(path)} Yang-Mills target_object_contract missing nonweakening commitments: {missing_contract_commitments}")
    for route in payload["active_route_families"]:
        if not isinstance(route, dict):
            fail(f"{rel(path)} active_route_families entries must be objects")
        require_fields(path, route, schema["required_route_family_fields"], "route family")
        unknown = [item for item in route["required_commitment_ids"] if item not in commitment_ids]
        if unknown:
            fail(f"{rel(path)} route family {route['id']} cites unknown commitments: {unknown}")
    active = set(schema["active_decisions"])
    forbidden_high_drift = set(schema["forbidden_high_drift_active_decisions"])
    for ranking in payload["candidate_rankings"]:
        if not isinstance(ranking, dict):
            fail(f"{rel(path)} candidate_rankings entries must be objects")
        require_fields(path, ranking, schema["required_candidate_ranking_fields"], "candidate ranking")
        if ranking["drift_risk"] not in schema["allowed_drift_risk"]:
            fail(f"{rel(path)} invalid drift_risk `{ranking['drift_risk']}`")
        decision = ranking["routing_decision"]
        if decision not in schema["allowed_routing_decisions"]:
            fail(f"{rel(path)} invalid routing_decision `{decision}`")
        score = ranking["target_relevance_score"]
        if not isinstance(score, (int, float)) or not 0 <= score <= 1:
            fail(f"{rel(path)} ranking {ranking['ranking_id']} target_relevance_score must be 0..1")
        cited = ranking["cited_commitment_ids"]
        if not isinstance(cited, list) or not cited:
            fail(f"{rel(path)} ranking {ranking['ranking_id']} needs cited_commitment_ids")
        unknown = [item for item in cited if item not in commitment_ids]
        if unknown:
            fail(f"{rel(path)} ranking {ranking['ranking_id']} cites unknown commitments: {unknown}")
        if decision in active and score < schema["minimum_active_relevance"]:
            fail(f"{rel(path)} ranking {ranking['ranking_id']} active decision below target relevance floor")
        if decision in forbidden_high_drift and ranking["drift_risk"] == "high":
            fail(f"{rel(path)} ranking {ranking['ranking_id']} high-drift route cannot remain active")


def validate_generated_rankings() -> None:
    map_path = ROOT / "artifacts/hegelian/hypothesis_exploration_map.json"
    if not map_path.exists():
        return
    payload = load_json_object(map_path)
    for ranking in payload.get("candidate_rankings", []):
        for field in ["target_relevance_score", "drift_risk", "cited_commitment_ids"]:
            if field not in ranking:
                fail(f"{rel(map_path)} ranking {ranking.get('ranking_id')} missing `{field}`")


def main() -> int:
    schema = load_json_object(SCHEMA)
    paths = sorted(LEDGERS.glob("*.json")) + sorted(FIXTURES.glob("*_target_case.json")) + sorted(FIXTURES.glob("*_route_case.json"))
    if not paths:
        fail("no target relevance ledgers or fixtures found")
    for path in paths:
        validate_ledger(path, schema)
    validate_generated_rankings()
    print(f"validated {len(paths)} target relevance ledgers and fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
