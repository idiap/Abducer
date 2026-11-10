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
from pathlib import Path

from prism.language.core.types import ASSURANCE_TYPES, PROVENANCE_TYPES, SCALAR_TYPES

from to_prism.fingerprint import fingerprint_tree
from to_prism.generation import generate_project
from to_prism.schemas import validate_document

TO_PRISM = Path(__file__).resolve().parents[2]
PRISM = TO_PRISM / ".venv/bin/prism"


def _prism(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(PRISM), *arguments],
        cwd=TO_PRISM,
        text=True,
        capture_output=True,
        check=False,
    )


def test_type_gallery_and_layered_example_check_compile_and_run() -> None:
    for path in (
        "examples/type_gallery/types.prism",
        "examples/layered_release_review/main.prism",
    ):
        checked = _prism("check", path)
        assert checked.returncode == 0, checked.stderr
        compiled = _prism("compile", path)
        assert compiled.returncode == 0, compiled.stderr

    executed = _prism(
        "run", "examples/layered_release_review/main.prism", "--handler", "fake"
    )
    assert executed.returncode == 0, executed.stderr
    assert json.loads(executed.stdout)["status"] == "accepted"


def test_taxonomy_names_every_core_primitive_provenance_and_assurance_type() -> None:
    taxonomy = (TO_PRISM / "references/type-taxonomy.md").read_text(encoding="utf-8")
    for name in SCALAR_TYPES | PROVENANCE_TYPES | ASSURANCE_TYPES:
        assert f"`{name}" in taxonomy, name
    for method in (
        "Deductive",
        "Abductive",
        "Inductive",
        "Analogical",
        "Contrastive",
        "ModelBased",
        "Refutational",
        "Evidential",
    ):
        assert f"`{method}`" in taxonomy


def test_machine_taxonomy_has_a_bounded_example_derived_type_budget() -> None:
    taxonomy = json.loads(
        (TO_PRISM / "references/semantic-taxonomy.json").read_text(encoding="utf-8")
    )
    seeds = {item["id"]: item for item in taxonomy["example_derived_boundary_seeds"]}

    assert set(seeds) == {
        "rank_hypotheses",
        "retrieve_scientific_statements",
        "query_database",
        "review_informal_argument",
        "formalize_equation",
    }
    assert taxonomy["type_budget"]["extension_rule"].startswith("Start coarse")
    assert seeds["formalize_equation"]["output"] == "FormalizedEquation"
    assert "sympy_expression" in seeds["formalize_equation"]["required_output_fields"]
    assert {item["id"] for item in taxonomy["inference_classes"]} == {
        "formal",
        "material_defeasible",
        "representational",
        "symbolic_computational",
    }


def test_incident_example_is_a_valid_project_semantic_taxonomy() -> None:
    path = (
        TO_PRISM
        / "examples/epistemic_incident_diagnosis/project-semantic-taxonomy.json"
    )
    assert (
        validate_document(json.loads(path.read_text()), "project-semantic-taxonomy")
        == []
    )


def test_conversion_example_generates_without_source_mutation(tmp_path: Path) -> None:
    example = TO_PRISM / "examples/conversion_input"
    source = example / "source"
    plan = json.loads((example / "approved-plan.json").read_text(encoding="utf-8"))
    before = fingerprint_tree(source).digest

    generated = generate_project(
        source_root=source,
        output_root=tmp_path / "prism_project",
        model=plan,
        prism_executable=str(PRISM),
        bundle=False,
        handler="fake",
    )

    assert generated.main.is_file()
    assert (
        generated.root / "generated/assess_release_claim_support_skill_1.prism"
    ).is_file()
    assert fingerprint_tree(source).digest == before
