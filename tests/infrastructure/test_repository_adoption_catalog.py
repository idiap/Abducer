# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Discovery must preserve scoped names, reject ambiguity, and invent no calls."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("repository_adoption_catalog", ROOT / "proj_skills/scripts/repository_adoption_catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


def write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill(root: Path, directory: str, name: str) -> None:
    write(root, directory + "/SKILL.md", f"---\nname: {name}\ndescription: Test contract\n---\n\n# Contract\n")


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    skill(tmp_path, "skills/domain/public", "public")
    skill(tmp_path, "proj_skills/project-state-profiler", "project-state-profiler")
    write(tmp_path, catalog.PUBLIC_REGISTRY, json.dumps({"skills": [{"name": "public", "path": "skills/domain/public"}]}))
    write(tmp_path, catalog.PROJECT_CATALOG, json.dumps({"skills": ["project-state-profiler"]}))
    write(tmp_path, catalog.OPERATIONS, json.dumps({"schema_version": "abducer.repository-adoption-operations/v1", "operations": []}))
    return tmp_path


def test_instruction_only_does_not_invent_callable(repository: Path) -> None:
    result = catalog.build_catalog(repository)
    profiler = next(row for row in result["skills"] if row["name"] == "project-state-profiler")
    assert profiler["implementation_kind"] == "instruction-only"
    assert profiler["invocation_mode"] == "instruction"
    assert profiler["operation_ids"] == []
    assert profiler["helper_sources"] == []
    assert profiler["field_provenance"]["canonical_authority"] == catalog.PROJECT_CATALOG


def test_helper_does_not_become_operation(repository: Path) -> None:
    write(repository, "proj_skills/project-state-profiler/scripts/helper.py", "raise RuntimeError('must not execute')\n")
    result = catalog.build_catalog(repository)
    profiler = next(row for row in result["skills"] if row["name"] == "project-state-profiler")
    assert profiler["implementation_kind"] == "instruction-with-helpers"
    assert profiler["operation_ids"] == []


def test_private_scope_preserves_overlapping_public_name(repository: Path) -> None:
    skill(repository, "skills/domain_specific/ym/public", "public")
    result = catalog.build_catalog(repository)
    assert {row["skill_id"] for row in result["skills"] if row["name"] == "public"} == {"skills:public", "cohere_fast/ym:public"}


def test_same_scope_duplicate_fails(repository: Path) -> None:
    skill(repository, "prism_me/first", "repeated")
    skill(repository, "prism_me/second", "repeated")
    with pytest.raises(catalog.CatalogError, match="duplicate scoped skill"):
        catalog.build_catalog(repository)


def test_registry_disagreement_fails(repository: Path) -> None:
    skill(repository, "skills/domain/unregistered", "unregistered")
    with pytest.raises(catalog.CatalogError, match="registry/discovery disagreement"):
        catalog.build_catalog(repository)


def test_missing_registry_source_fails(repository: Path) -> None:
    (repository / "skills/domain/public/SKILL.md").unlink()
    with pytest.raises(catalog.CatalogError, match="registry paths not discovered"):
        catalog.build_catalog(repository)


def test_duplicate_registry_and_operation_fail(repository: Path) -> None:
    source = repository / catalog.PUBLIC_REGISTRY
    payload = json.loads(source.read_text())
    payload["skills"] *= 2
    source.write_text(json.dumps(payload))
    with pytest.raises(catalog.CatalogError, match="duplicate public registry"):
        catalog.build_catalog(repository)
    payload["skills"] = payload["skills"][:1]
    source.write_text(json.dumps(payload))
    write(repository, "script.py", "")
    operation = {"operation_id": "pilot", "implementation": "script.py"}
    write(repository, catalog.OPERATIONS, json.dumps({"schema_version": "abducer.repository-adoption-operations/v1", "operations": [operation, operation]}))
    with pytest.raises(catalog.CatalogError, match="duplicate operation"):
        catalog.build_catalog(repository)


def test_reference_sources_classified_not_installed(repository: Path) -> None:
    fixtures = {
        "external/vendor/example": "vendored",
        ".prism/request/source/skill": "request-local-reference",
        "abducer-prism/tests/fixtures/skill": "fixture",
        "docs/generated/skill": "generated",
        "agentic/retired/skill": "retired",
    }
    for directory in fixtures:
        skill(repository, directory, "public")
    result = catalog.build_catalog(repository)
    assert len(result["skills"]) == 2
    assert {row["path"].removesuffix("/SKILL.md"): row["disposition"] for row in result["excluded_sources"]} == fixtures


def test_unknown_roots_fail_instead_of_silently_omitting(repository: Path) -> None:
    skill(repository, "surprise/skill", "unknown")
    with pytest.raises(catalog.CatalogError, match="unclassified skill root"):
        catalog.build_catalog(repository)


def test_generated_projection_is_deterministic_and_stale_checked(repository: Path) -> None:
    assert catalog.main(["--repository-root", str(repository), "--write"]) == 0
    assert catalog.main(["--repository-root", str(repository), "--check"]) == 0
    output = repository / "docs/generated/repository-adoption-catalog.json"
    before = output.read_bytes()
    assert catalog.main(["--repository-root", str(repository), "--write"]) == 0
    assert output.read_bytes() == before
    write(repository, "prism_me/new/SKILL.md", "---\nname: new\n---\n")
    with pytest.raises(SystemExit) as error:
        catalog.main(["--repository-root", str(repository), "--check"])
    assert error.value.code == 1


def test_operation_paths_cannot_escape_repository(repository: Path) -> None:
    write(repository, catalog.OPERATIONS, json.dumps({"schema_version": "abducer.repository-adoption-operations/v1", "operations": [{"operation_id": "unsafe", "implementation": "../escape.py"}]}))
    with pytest.raises(catalog.CatalogError, match="invalid operation fields"):
        catalog.build_catalog(repository)


def test_nested_derived_sources_are_not_canonical(repository: Path) -> None:
    skill(repository, "skills/domain/fixtures/duplicate", "public")
    skill(repository, "proj_skills/generated/duplicate", "project-state-profiler")
    result = catalog.build_catalog(repository)
    assert len(result["skills"]) == 2
    assert {row["disposition"] for row in result["excluded_sources"]} == {"fixture", "generated"}


def test_unknown_operation_cannot_be_registered(repository: Path) -> None:
    sidecar = json.loads((ROOT / catalog.OPERATIONS).read_text())
    op = sidecar["operations"][0]
    op["operation_id"] = "arbitrary-callable"
    sidecar["operations"] = [op]
    write(repository, catalog.OPERATIONS, json.dumps(sidecar))
    with pytest.raises(catalog.CatalogError, match="unknown or changed fixed operation binding"):
        catalog.build_catalog(repository)
