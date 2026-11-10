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
REGISTRY = ROOT / "agentic/registries/essential_reasoning_types.yaml"


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_epistemic_types_are_separate_from_operational_capabilities() -> None:
    payload = load()
    type_ids = {row["id"] for row in payload["reasoning_types"]}
    assert len(type_ids) == 8
    assert type_ids.isdisjoint(payload["scope"]["excluded_as_essential_types"])
    assert {row["family"] for row in payload["reasoning_types"]} == {
        "core_inference", "epistemic_control"
    }


def test_mapping_is_many_to_many_and_orchestrator_does_not_inherit_authority() -> None:
    payload = load()
    assert any(row["secondary_types"] for row in payload["skill_mappings"])
    counts: dict[str, int] = {}
    for row in payload["skill_mappings"]:
        for reasoning_type in [row["primary_type"], *row["secondary_types"]]:
            counts[reasoning_type] = counts.get(reasoning_type, 0) + 1
    assert all(count >= 2 for count in counts.values())
    isolated = {row["skill"]: row for row in payload["non_epistemic_materializers"]}
    assert isolated["cohere-fast-orchestrator"]["reasoning_relation"] == (
        "composes_but_does_not_itself_instantiate"
    )


def test_reasoning_styles_end_in_testing_or_calibration() -> None:
    payload = load()
    safe_tail = {"critical_refutational_testing", "evidential_status_calibration"}
    for style in payload["reasoning_styles"]:
        assert safe_tail.intersection(style["composition"])
        assert style["required_guards"]


def test_registry_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/validate_essential_reasoning_types.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "36 curated skill mappings" in result.stdout
