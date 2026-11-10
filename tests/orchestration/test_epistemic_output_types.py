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

import copy
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "agentic/registries/epistemic_output_types.yaml"
SCHEMA = ROOT / "agentic/spec/epistemic_output.schema.json"
KB_SCHEMA = ROOT / "agentic/spec/knowledge_base.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_output_typology_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/validate_epistemic_output_types.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "10 output kinds" in result.stdout
    assert "8 reasoning codomains" in result.stdout


def test_refutation_and_calibration_codomains_cannot_create_positive_claims() -> None:
    payload = load(REGISTRY)
    codomains = {row["reasoning_type"]: row for row in payload["reasoning_codomains"]}
    not_refuted = next(row for row in codomains["R"]["variants"] if row["id"] == "not_refuted")
    assert not any(value.startswith("Claim:") for value in not_refuted["members"])
    assert {"Evidence:search_trace", "Decision:bounded_nonrefutation"} <= set(not_refuted["members"])
    calibrated = codomains["E"]["variants"][0]["members"]
    assert not any(value.startswith(("Claim:", "Evidence:")) for value in calibrated)
    assert {"Decision:epistemic_status", "Relation:calibrates"} <= set(calibrated)


def test_zero_authority_output_kinds_are_explicit() -> None:
    payload = load(REGISTRY)
    kinds = {row["id"]: row for row in payload["output_kinds"]}
    for kind in ("KnowledgeBase", "Evidence", "Model", "Plan", "Presentation"):
        assert kinds[kind]["claim_effects"] == ["none"]
    assert "reasoning:source_dereference_required" in kinds["Presentation"]["admissible_consumers"]


def test_knowledge_base_schema_preserves_version_and_member_authority() -> None:
    payload = {
        "schema_version": "1.0.0",
        "kb_id": "ym",
        "version_id": "ym-v4",
        "predecessor_version_id": "ym-v3",
        "scope": {"description": "Yang-Mills working knowledge", "domains": ["ym"]},
        "world_assumption": "open",
        "consistency_policy": "paraconsistent",
        "revision_policy": "versioned",
        "members": [{"output_id": "claim-gap", "kind": "Claim", "status": "contested"}],
        "provenance": {"required": True, "source_refs": ["source:local-kb"]},
        "open_conflicts": [],
    }
    jsonschema.validate(payload, load(KB_SCHEMA))
    invalid = copy.deepcopy(payload)
    invalid["members"][0]["kind"] = "ValidatedClaim"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, load(KB_SCHEMA))


def test_epistemic_output_schema_enforces_kind_specific_authority() -> None:
    schema = load(SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)
    valid = {
        "schema_version": "0.1",
        "output_id": "out-observation-1",
        "kind": "Evidence",
        "reasoning_occurrence_id": "m0",
        "epistemic_modality": "simulated",
        "claim_effect": "none",
        "scope": {"regime": "finite model"},
        "provenance": ["sha256:" + "a" * 64],
        "taints": ["simulation-only"],
        "open_obligations": ["model-to-target bridge"],
        "mutability": "immutable",
        "terminality": "nonterminal",
        "payload": {"subtype": "simulation_trace"},
    }
    jsonschema.validate(valid, schema)
    unsafe = copy.deepcopy(valid)
    unsafe["claim_effect"] = "introduce"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(unsafe, schema)
    presentation = copy.deepcopy(valid)
    presentation.update({"output_id": "out-paper-1", "kind": "Presentation", "epistemic_modality": "communicative"})
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(presentation, schema)


def test_artifact_examples_are_faceted_not_equated_with_output_kinds() -> None:
    payload = load(REGISTRY)
    examples = {row["artifact_type"]: row for row in payload["artifact_examples"]}
    assert {"Claim:conditional_entailment", "Relation:entails_given", "Obligation:proof"} <= set(examples["LemmaChain"]["contains"])
    assert examples["DomainEvidencePacket"]["mapping_status"] == "underspecified"
    assert examples["IntegratedPaperDraft"]["contains"][0].startswith("Presentation:")
