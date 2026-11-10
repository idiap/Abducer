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
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/workflow_paper/modeling_evidence_index.json"


def run_script(relative: str, *args: Path) -> None:
    subprocess.run([sys.executable, str(ROOT / relative), *(str(arg) for arg in args)], check=True)


def assert_schema(instance_path: Path, schema_name: str) -> None:
    schema = json.loads((ROOT / "agentic/spec" / schema_name).read_text())
    Draft202012Validator(schema).validate(json.loads(instance_path.read_text()))


def test_functional_workflow_and_execution_models_preserve_evidence_boundaries(tmp_path: Path) -> None:
    functional = tmp_path / "functional-model.json"
    workflow = tmp_path / "workflow-model.json"
    execution = tmp_path / "execution-evidence.json"
    run_script("proj_skills/framework-functional-modeler/scripts/build_functional_model.py", FIXTURE, functional)
    run_script("proj_skills/framework-workflow-modeler/scripts/build_workflow_model.py", FIXTURE, workflow)
    run_script("proj_skills/framework-execution-evidence-assessor/scripts/assess_execution_evidence.py", FIXTURE, execution)

    functional_data = json.loads(functional.read_text())
    workflow_data = json.loads(workflow.read_text())
    execution_data = json.loads(execution.read_text())
    assert_schema(functional, "framework_paper_functional_capability_model.schema.json")
    assert_schema(workflow, "framework_paper_workflow_structure_model.schema.json")
    assert_schema(execution, "framework_paper_execution_evidence_model.schema.json")
    capabilities = {item["capability_id"]: item for item in functional_data["capabilities"]}
    assert "observed posture" in capabilities["cap-orchestration-and-control"]["purpose"]
    assert "declared posture" in capabilities["cap-reporting"]["purpose"]
    assert {edge["edge_type"] for edge in workflow_data["edges"]} == {"gates", "persists_to", "feeds_back_to"}
    assert workflow_data["failure_paths"]
    statuses = {item["assessment_id"]: item["status"] for item in execution_data["assessments"]}
    assert any("test source exists" in item for item in execution_data["missing_evidence"])
    assert statuses["exec-ev-run"] == "verified"
    assert len({functional_data["input_digest"], workflow_data["input_digest"], execution_data["input_digest"]}) == 1


def test_abstraction_is_bidirectionally_traceable_and_claims_are_gated(tmp_path: Path) -> None:
    functional, workflow, execution = [tmp_path / name for name in ("functional.json", "workflow.json", "execution.json")]
    run_script("proj_skills/framework-functional-modeler/scripts/build_functional_model.py", FIXTURE, functional)
    run_script("proj_skills/framework-workflow-modeler/scripts/build_workflow_model.py", FIXTURE, workflow)
    run_script("proj_skills/framework-execution-evidence-assessor/scripts/assess_execution_evidence.py", FIXTURE, execution)
    model, notation, ledger = tmp_path / "framework-model.json", tmp_path / "notation.tex", tmp_path / "claim-ledger.json"
    run_script("proj_skills/framework-abstraction-synthesizer/scripts/synthesize_framework_abstraction.py", functional, workflow, execution, model, notation)
    run_script("proj_skills/framework-paper-claim-curator/scripts/curate_claim_ledger.py", model, ledger,
               Path("--candidates"), ROOT / "tests/fixtures/workflow_paper/unsupported_claim_candidates.json")

    model_data = json.loads(model.read_text())
    ledger_data = json.loads(ledger.read_text())
    assert_schema(model, "framework_paper_framework_abstraction_model.schema.json")
    assert_schema(ledger, "framework_paper_claim_ledger.schema.json")
    construct_ids = {item["construct_id"] for item in model_data["constructs"]}
    assert construct_ids
    assert all(item["evidence_ids"] for item in model_data["constructs"])
    assert all(item["construct_id"] in construct_ids and item["concrete_ids"] for item in model_data["trace_links"])
    assert "\\newcommand" in notation.read_text()
    withheld = [claim for claim in ledger_data["claims"] if claim["resolution"] == "withheld"]
    assert len(withheld) == 4
    accepted = [claim for claim in ledger_data["claims"] if claim["resolution"] == "accepted"]
    assert all(claim["claim_class"] == "descriptive" for claim in accepted)
    assert all("runtime" in claim["limitations"][0] for claim in accepted)


def test_abstraction_rejects_mixed_snapshots(tmp_path: Path) -> None:
    functional = {"input_digest": "a", "digest": "f", "capabilities": []}
    workflow = {"input_digest": "b", "digest": "w", "nodes": [], "edges": []}
    execution = {"input_digest": "a", "digest": "e", "assessments": []}
    paths = []
    for name, value in zip(("f", "w", "e"), (functional, workflow, execution)):
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(value))
        paths.append(path)
    completed = subprocess.run(
        [sys.executable, str(ROOT / "proj_skills/framework-abstraction-synthesizer/scripts/synthesize_framework_abstraction.py"),
         *(str(path) for path in paths), str(tmp_path / "out.json"), str(tmp_path / "notation.tex")],
        text=True, capture_output=True,
    )
    assert completed.returncode != 0
    assert "share one input digest" in completed.stderr
