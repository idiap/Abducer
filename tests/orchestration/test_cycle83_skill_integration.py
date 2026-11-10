# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for cycle-83 theory-first and Yang--Mills skill integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "agentic/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_repo_skills import validate_skill  # noqa: E402
from validate_skill_depth import check_skill  # noqa: E402
import validate_skill_taxonomy_projections as taxonomy_validation  # noqa: E402


CENTRAL = {
    "reflective-conceptual-discovery": "skills/orchestration/reflective-conceptual-discovery",
    "frontier-literature-assimilator": "skills/reasoning/frontier-literature-assimilator",
    "high-risk-hypothesis-forger": "skills/reasoning/high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio": "skills/orchestration/parallel-hypothesis-portfolio",
    "dynamic-symbolic-simulation-experimenter": "skills/reasoning/dynamic-symbolic-simulation-experimenter",
    "reflective-theory-synthesizer": "skills/reasoning/reflective-theory-synthesizer",
}
YM_PROOF = {
    "ym-prove-adaptive-block-domination": "skills/yang_mills/ym-prove-adaptive-block-domination",
    "ym-prove-conditional-partition-ratio": "skills/yang_mills/ym-prove-conditional-partition-ratio",
    "ym-prove-state-weighted-defect-transfer": "skills/yang_mills/ym-prove-state-weighted-defect-transfer",
}
ALL_NINE = {**CENTRAL, **YM_PROOF}


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_nine_skills_are_registered_and_taxonomy_projection_is_valid() -> None:
    registry = _json("agentic/registries/skill_registry.yaml")["skills"]
    quality = _json("agentic/registries/skill_quality_registry.yaml")["skill_quality"]
    projections = _json("registry/skill_projections/abducer_skill_projections.json")["skills"]
    by_registry = {row["name"]: row for row in registry}
    by_quality = {row["name"]: row for row in quality}
    by_projection = {row["skill_name"]: row for row in projections}

    assert set(ALL_NINE) <= set(by_registry)
    assert set(ALL_NINE) <= set(by_quality)
    assert set(ALL_NINE) <= set(by_projection)
    assert len(by_registry) == len(registry)
    assert len(by_quality) == len(quality)
    assert len(by_projection) == len(projections)
    for name, path in ALL_NINE.items():
        assert by_registry[name]["path"] == path
        assert by_quality[name]["status"] == "promoted"
        assert by_projection[name]["path"] == path
        assert by_projection[name]["skill_depth"]["status"] == "promoted"
        assert by_projection[name]["skill_depth"]["critical_findings"] == 0
    assert taxonomy_validation.main() == 0


def test_dispatch_keeps_reflection_central_and_ym_proofs_conditional() -> None:
    phases = {
        row["phase"]: row
        for row in _json("agentic/registries/discovery_marathon_skill_dispatch.yaml")["phases"]
    }
    assert phases["current_literature_assimilation_rebase"]["required_skills"] == [
        "frontier-literature-assimilator"
    ]
    assert phases["high_risk_intuition_generation"]["required_skills"] == [
        "high-risk-hypothesis-forger"
    ]
    assert phases["parallel_hypothesis_maturation"]["required_skills"] == [
        "parallel-hypothesis-portfolio"
    ]
    assert phases["reflective_parent_synthesis"]["required_skills"] == [
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
        "blind-conceptual-preference-adjudicator",
    ]
    assert "dynamic-symbolic-simulation-experimenter" in phases[
        "theory_requested_symbolic_simulation_support"
    ]["conditional_skills"]

    overlay = phases["yang_mills_representational_dynamics_overlay"]
    assert overlay["target_scope"] == "yang-mills-existence-and-mass-gap-target"
    assert set(YM_PROOF) <= set(overlay["conditional_skills"])
    assert set(YM_PROOF).isdisjoint(overlay["legacy_advisory_skills"])


def test_all_nine_skills_pass_repository_quick_validation_and_are_catalogued() -> None:
    catalog = (ROOT / "docs/reference/skills.md").read_text(encoding="utf-8")
    for name, path in ALL_NINE.items():
        assert validate_skill(ROOT / path) == []
        assert f"../{path}/SKILL.md" in catalog
        agent = (ROOT / path / "agents/openai.yaml").read_text(encoding="utf-8")
        assert f"${name}" in agent


def test_three_ym_proof_skills_meet_depth_and_exact_scope_contracts() -> None:
    schema = _json("agentic/spec/skill_depth_review_schema.json")
    required_headings = {
        "## Exact Target and Version Scope",
        "## Required Inputs",
        "## Mathematical Invariants",
        "## Epistemic Discipline",
        "## Output Contract",
        "## Failure/Demotion",
        "## Validation Handoff",
    }
    for name, path in YM_PROOF.items():
        skill_dir = ROOT / path
        result = check_skill(skill_dir, schema)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        assert result["status"] == "pass", (name, result)
        assert result["critical_findings"] == 0
        assert all(heading in text for heading in required_headings)
        assert "yang-mills-existence-and-mass-gap-target" in text
        assert "/2026-07-21/active_snapshot/" in text
