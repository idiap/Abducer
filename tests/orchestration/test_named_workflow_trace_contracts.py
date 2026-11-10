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

import importlib.util
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[2]


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_trace_contracts_cover_execution_registry() -> None:
    generator = _load_module(ROOT / "agentic/scripts/generate_named_workflow_trace_contracts.py")
    validator = _load_module(ROOT / "agentic/scripts/validate_named_workflow_trace_contracts.py")
    execution = json.loads((ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text(encoding="utf-8"))
    persisted = json.loads((ROOT / "agentic/registries/named_workflow_trace_contracts.yaml").read_text(encoding="utf-8"))
    assert generator.build_contracts(execution) == persisted
    assert validator.validate(execution, persisted) == []
    schema = json.loads((ROOT / "agentic/spec/named_workflow_trace_contract.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(persisted)


def test_every_role_requires_semantics_not_only_control_events() -> None:
    trace = json.loads((ROOT / "agentic/registries/named_workflow_trace_contracts.yaml").read_text(encoding="utf-8"))
    roles = []
    for workflow in trace["workflows"]:
        roles.extend(workflow["steps"])
        for profile in workflow["profiles"]:
            roles.extend(profile["steps"])
            roles.extend(profile["specialists"])
    assert len(roles) == 74
    assert all(row["required_fields"] for row in roles)
    assert all("public_inference.warrant" in row["required_fields"] for row in roles)
    assert all(row["required_contrast"] for row in roles)
    assert all(row["authority_boundary"] for row in roles)
    assert {row["disposition"] for row in roles} >= {
        "semantic_event_required",
        "validator_event_required",
        "conditional_event_or_justified_na",
        "specialist_event_required",
    }


def test_route_a_retains_profile_and_specialist_structure() -> None:
    trace = json.loads((ROOT / "agentic/registries/named_workflow_trace_contracts.yaml").read_text(encoding="utf-8"))
    manuscript = next(row for row in trace["workflows"] if row["id"] == "manuscript_result_elaboration")
    route_a = next(row for row in manuscript["profiles"] if row["id"] == "route_a")
    assert len(route_a["steps"]) == 5
    assert len(route_a["specialists"]) == 10
    assert route_a["validation_tail_start"] == "certify_scope"
    assert route_a["validation_tail_adapter"] == {"from": "ResultCandidatePacket", "to": "RefinedResultCandidates"}
