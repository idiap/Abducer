# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import yaml

from hegelian_solver.domain import domain_profile
from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.io import read_structured
from hegelian_solver.schemas import PhysicalConcept, all_schema_models
from hegelian_solver.schemas.json_schema import export_json_schemas


ROOT = Path(__file__).resolve().parents[2]


def test_json_schema_export_for_public_artifacts(tmp_path):
    written = export_json_schemas(tmp_path)

    assert len(written) == len(all_schema_models())
    assert (tmp_path / "ConceptNode.schema.json").exists()
    assert (tmp_path / "SolverTrace.schema.json").exists()
    assert (tmp_path / "ReasoningLog.schema.json").exists()


def test_domain_detection_routes_physics_fixture():
    raw = read_structured(ROOT / "hegelian_solver/examples/newtonian_mechanics.yaml")
    profile = domain_profile(raw)
    concept = formalize_concept(raw, profile)

    assert profile.domain == "physical_concept"
    assert isinstance(concept, PhysicalConcept)
    assert "measurement_model" in profile.required_fields


def test_same_phrase_can_route_by_context():
    math_profile = domain_profile({"name": "Field", "axioms": ["field axioms"]})
    physics_profile = domain_profile({"name": "Field", "observables": ["electric field"], "measurement": {}})

    assert math_profile.domain == "mathematical_concept"
    assert physics_profile.domain == "physical_concept"


def test_skill_folders_have_valid_frontmatter():
    for skill_md in (ROOT / "agents").glob("*/SKILL.md"):
        text = skill_md.read_text()
        assert text.startswith("---\n")
        frontmatter = text.split("---", 2)[1]
        parsed = yaml.safe_load(frontmatter)
        assert parsed["name"] == skill_md.parent.name
        assert parsed["description"]


def test_retrospective_input_skills_are_integrated():
    agents = ROOT / "agents"
    expected = {
        "hegelian-input-typology",
        "hegelian-retrospective-evolution-formalizer",
        "hegelian-web-expansion-scout",
        "hegelian-field-tension-elicitor",
        "hegelian-tension-evidence-cartographer",
        "hegelian-conceptual-crisis-formalizer",
        "hegelian-abductive-mechanism-hypothesizer",
        "hegelian-mechanism-requirements-formalizer",
        "hegelian-mechanism-counterfactual-critic",
        "hegelian-mechanism-todo-elicitor",
    }

    assert expected.issubset({path.name for path in agents.iterdir() if path.is_dir()})
    orchestrator = (agents / "hegelian-solver-orchestrator" / "SKILL.md").read_text()
    assert "hegelian-input-typology" in orchestrator
    assert "hegelian-retrospective-evolution-formalizer" in orchestrator
    assert "hegelian-web-expansion-scout" in orchestrator
    assert "hegelian-field-tension-elicitor" in orchestrator
    assert "hegelian-tension-evidence-cartographer" in orchestrator
    assert "hegelian-conceptual-crisis-formalizer" in orchestrator
    assert "hegelian-abductive-mechanism-hypothesizer" in orchestrator
    assert "hegelian-mechanism-requirements-formalizer" in orchestrator
    assert "hegelian-mechanism-counterfactual-critic" in orchestrator
    assert "hegelian-mechanism-todo-elicitor" in orchestrator
    web_skill = (agents / "hegelian-web-expansion-scout" / "SKILL.md").read_text()
    assert "required | recommended | not_needed | forbidden_by_user" in web_skill
    typology = (agents / "hegelian-input-typology" / "SKILL.md").read_text()
    assert "field_tension_request" in typology
    mechanism_skill = (agents / "hegelian-abductive-mechanism-hypothesizer" / "SKILL.md").read_text()
    assert "necessary_mediator" in mechanism_skill
    assert "defeater" in mechanism_skill


def test_area_concept_trace_builder_is_integrated():
    agents = ROOT / "agents"
    assert (agents / "hegelian-area-concept-trace-builder" / "SKILL.md").exists()

    trace_skill = (agents / "hegelian-area-concept-trace-builder" / "SKILL.md").read_text()
    assert "area_conceptual_trace" in trace_skill
    assert "confidence: high | medium | low" in trace_skill
    assert "hegelian-web-expansion-scout" in trace_skill

    typology = (agents / "hegelian-input-typology" / "SKILL.md").read_text()
    assert "area_trace_request" in typology
    assert "hegelian-area-concept-trace-builder" in typology

    orchestrator = (agents / "hegelian-solver-orchestrator" / "SKILL.md").read_text()
    assert "hegelian-area-concept-trace-builder" in orchestrator


def test_conceptual_creativity_reasoner_is_integrated():
    agents = ROOT / "agents"
    assert (agents / "hegelian-conceptual-creativity-reasoner" / "SKILL.md").exists()

    skill = (agents / "hegelian-conceptual-creativity-reasoner" / "SKILL.md").read_text()
    assert "closure_completion" in skill
    assert "governance_safety_scaffold" in skill
    assert "repair | affordance_creation | mixed" in skill
    assert "why_creative_not_corrective" in skill

    orchestrator = (agents / "hegelian-solver-orchestrator" / "SKILL.md").read_text()
    assert "hegelian-conceptual-creativity-reasoner" in orchestrator
