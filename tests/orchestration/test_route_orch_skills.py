# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTE = ROOT / "skills/orchestration/route/scripts/compile_route.py"
CAPABILITIES = ROOT / "skills/orchestration/orch/scripts/list_capabilities.py"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_rigid_profile_covers_every_essential_reasoning_type() -> None:
    types = load("agentic/registries/essential_reasoning_types.yaml")
    routes = load("agentic/registries/reasoning_capability_routes.yaml")
    skills = {row["name"] for row in load("agentic/registries/skill_registry.yaml")["skills"]}
    mappings = {row["skill"]: row for row in types["skill_mappings"]}
    type_ids = {row["id"] for row in types["reasoning_types"]}
    bindings = routes["profiles"][0]["bindings"]

    assert set(bindings) == type_ids
    for reasoning_type, skill in bindings.items():
        assert skill in skills
        mapping = mappings[skill]
        assert reasoning_type in {
            mapping["primary_type"],
            *mapping.get("secondary_types", []),
        }


def test_route_compiles_fixed_program_to_expected_bindings() -> None:
    result = run(str(ROUTE), "agentic/reasoning_flows/abducer_work_loop.prism")
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["executable"] is True
    assert payload["blockers"] == []
    assert {row["role"] for row in payload["registry_sources"]} == {
        "reasoning_types",
        "skills",
        "route_profiles",
    }
    assert all(len(row["sha256"]) == 64 for row in payload["registry_sources"])
    assert {row["alias"]: row["skill"] for row in payload["bindings"]} == {
        "a0": "kb-abduce",
        "d0": "kb-deduce",
        "r0": "counterexample-hunter",
        "e0": "epistemic-status-ledger",
    }


def test_route_fails_closed_for_gap_bearing_program() -> None:
    result = run(str(ROUTE), "agentic/reasoning_flows/target_navigation_loop.prism")
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert payload["executable"] is False
    assert any(row["kind"] == "unresolved_reasoning_gap" for row in payload["blockers"])


def test_route_rejects_reasoning_type_mismatch() -> None:
    result = run(
        str(ROUTE),
        "agentic/reasoning_flows/abducer_work_loop.prism",
        "--bind",
        "a0=kb-deduce",
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert any(row["kind"] == "mapping_mismatch" for row in payload["blockers"])


def test_orch_namespace_query_is_type_first_and_registry_backed() -> None:
    result = run(str(CAPABILITIES), "abductive_hypothesis_formation")
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["blocked"] is False
    assert payload["reasoning_type"] == "abductive_hypothesis_formation"
    assert payload["candidates"]
    assert len(payload["registry_sources"]) == 3
    assert payload["candidates"][0]["mapping_kind"] == "primary"
    assert all(row["skill"] != "orch" for row in payload["candidates"])


def test_route_and_orch_are_non_epistemic_control_skills() -> None:
    registry = load("agentic/registries/essential_reasoning_types.yaml")
    rows = {row["skill"]: row for row in registry["non_epistemic_materializers"]}
    assert rows["route"]["operational_role"] == "rigid_router"
    assert rows["orch"]["operational_role"] == "dynamic_orchestrator"

    route_text = (ROOT / "skills/orchestration/route/SKILL.md").read_text()
    orch_text = (ROOT / "skills/orchestration/orch/SKILL.md").read_text()
    assert "Do not replan" in route_text
    assert "type-before-skill selection" in orch_text
    assert "Delegate rigid binding to `$route`" in orch_text
