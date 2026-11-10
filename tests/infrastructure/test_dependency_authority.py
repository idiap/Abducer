# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial coverage for derived repository dependency authorities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.dependency_authority import (
    DependencyAuthorityError,
    build_dependency_authority,
    validate_dependency_authority,
)
from skills.common.formal_dependency_authority import (
    build_formal_dependency_authority,
    validate_formal_dependency_authority,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def local_profile(tmp_path: Path) -> dict[str, Any]:
    _write(tmp_path / "pkg/__init__.py", "\"\"\"Fixture package.\"\"\"\n")
    _write(
        tmp_path / "pkg/root.py",
        "from .helper import VALUE\nSCHEMA = 'example.schema.json'\nRESULT = VALUE\n",
    )
    _write(tmp_path / "pkg/helper.py", "VALUE = 1\n")
    _write(tmp_path / "docs/contract.md", "# Exact fixture contract\n")
    _write(
        tmp_path / "agentic/spec/example.schema.json",
        '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
        '"type":"object","properties":{"child":{"$ref":"nested.schema.json"}}}\n',
    )
    _write(
        tmp_path / "agentic/spec/nested.schema.json",
        '{"type":"object","additionalProperties":false}\n',
    )
    arguments = {
        "scope": "fixture_dependency_authority",
        "entry_python_paths": {"pkg/root.py": ("fixture_entry",)},
        "semantic_paths": {"docs/contract.md": ("fixture_contract",)},
        "authority_boundary": "Exact fixture bytes only; no correctness authority.",
        "repository_root": tmp_path,
        "runtime_distributions": {},
    }
    return {"root": tmp_path, "arguments": arguments}


def test_generic_authority_derives_import_schema_ref_and_semantic_closure(
    local_profile: dict[str, Any],
) -> None:
    arguments = local_profile["arguments"]
    authority = build_dependency_authority(**arguments)
    paths = {row["path"] for row in authority["entries"]}
    assert {
        "pkg/__init__.py",
        "pkg/root.py",
        "pkg/helper.py",
        "docs/contract.md",
        "agentic/spec/example.schema.json",
        "agentic/spec/nested.schema.json",
    } <= paths
    assert authority["schema_closure"] == {
        "literal_paths": ["agentic/spec/example.schema.json"],
        "referenced_paths": ["agentic/spec/nested.schema.json"],
    }
    assert authority["import_boundary"]["third_party_modules"] == []
    assert validate_dependency_authority(authority, **arguments) == authority


@pytest.mark.parametrize("drift", ["import_mutation", "deletion", "schema_drift"])
def test_generic_authority_rejects_import_mutation_deletion_and_schema_drift(
    local_profile: dict[str, Any], drift: str
) -> None:
    root = local_profile["root"]
    arguments = local_profile["arguments"]
    authority = build_dependency_authority(**arguments)
    if drift == "import_mutation":
        _write(root / "pkg/extra.py", "EXTRA = 2\n")
        _write(
            root / "pkg/root.py",
            "from .helper import VALUE\nfrom .extra import EXTRA\n"
            "SCHEMA = 'example.schema.json'\nRESULT = VALUE + EXTRA\n",
        )
    elif drift == "deletion":
        (root / "pkg/helper.py").unlink()
    else:
        _write(
            root / "agentic/spec/nested.schema.json",
            '{"type":"object","required":["changed"]}\n',
        )
    with pytest.raises(DependencyAuthorityError):
        validate_dependency_authority(authority, **arguments)


def test_new_local_import_enters_rebuilt_closure(local_profile: dict[str, Any]) -> None:
    root = local_profile["root"]
    arguments = local_profile["arguments"]
    before = build_dependency_authority(**arguments)
    _write(root / "pkg/extra.py", "EXTRA = 2\n")
    _write(
        root / "pkg/root.py",
        "from .helper import VALUE\nfrom .extra import EXTRA\n"
        "SCHEMA = 'example.schema.json'\nRESULT = VALUE + EXTRA\n",
    )
    after = build_dependency_authority(**arguments)
    assert "pkg/extra.py" in {row["path"] for row in after["entries"]}
    assert before["content_digest"] != after["content_digest"]


def _semantic_schema_profile(root: Path) -> dict[str, Any]:
    """Declare a schema only as semantic authority, never as a Python literal."""

    return {
        "scope": "semantic_schema_root_fixture",
        "entry_python_paths": {"entry.py": ("entry",)},
        "semantic_paths": {
            "schemas/root.schema.json": ("semantic_contract",),
        },
        "authority_boundary": "Exact local semantic-schema closure only.",
        "repository_root": root,
        "runtime_distributions": {},
    }


def test_semantic_schema_root_seeds_nested_and_cyclic_ref_closure(
    tmp_path: Path,
) -> None:
    _write(tmp_path / "entry.py", "VALUE = 1\n")
    _write(
        tmp_path / "schemas/root.schema.json",
        '{"$defs":{"local":{"type":"string"}},'
        '"properties":{"child":{"$ref":"nested/child.schema.json#/$defs/child"}}}\n',
    )
    _write(
        tmp_path / "schemas/nested/child.schema.json",
        '{"$defs":{"child":{"allOf":['
        '{"$ref":"../root.schema.json#/$defs/local"}]}}}\n',
    )

    arguments = _semantic_schema_profile(tmp_path)
    authority = build_dependency_authority(**arguments)
    entries = {row["path"]: row for row in authority["entries"]}
    assert "json_schema_semantic_root" in entries[
        "schemas/root.schema.json"
    ]["roles"]
    assert "json_schema_reference" in entries[
        "schemas/nested/child.schema.json"
    ]["roles"]
    assert authority["schema_closure"] == {
        "literal_paths": [],
        "referenced_paths": ["schemas/nested/child.schema.json"],
    }
    assert validate_dependency_authority(authority, **arguments) == authority


@pytest.mark.parametrize(
    ("reference", "message"),
    [
        ("missing.schema.json", "missing"),
        ("../../../outside.schema.json", "escapes repository"),
        ("https://schemas.example.test/remote.json", "bounded local authority"),
        ("urn:example:remote-schema", "bounded local authority"),
    ],
)
def test_semantic_schema_root_rejects_missing_escaping_and_remote_refs(
    tmp_path: Path, reference: str, message: str
) -> None:
    _write(tmp_path / "entry.py", "VALUE = 1\n")
    _write(
        tmp_path / "schemas/root.schema.json",
        '{"properties":{"child":{"$ref":' + repr(reference).replace("'", '"') + "}}}\n",
    )
    with pytest.raises(DependencyAuthorityError, match=message):
        build_dependency_authority(**_semantic_schema_profile(tmp_path))


def test_semantic_schema_nested_mutation_invalidates_authority(tmp_path: Path) -> None:
    _write(tmp_path / "entry.py", "VALUE = 1\n")
    _write(
        tmp_path / "schemas/root.schema.json",
        '{"properties":{"child":{"$ref":"nested.schema.json"}}}\n',
    )
    _write(tmp_path / "schemas/nested.schema.json", '{"type":"string"}\n')
    arguments = _semantic_schema_profile(tmp_path)
    authority = build_dependency_authority(**arguments)

    _write(tmp_path / "schemas/nested.schema.json", '{"type":"integer"}\n')
    with pytest.raises(DependencyAuthorityError, match="exact bounded"):
        validate_dependency_authority(authority, **arguments)


def test_semantic_schema_accepts_exact_absolute_local_id_and_rejects_duplicate_ids(
    tmp_path: Path,
) -> None:
    _write(tmp_path / "entry.py", "VALUE = 1\n")
    _write(
        tmp_path / "schemas/root.schema.json",
        '{"allOf":[{"$ref":"https://abducer.local/spec/a.schema.json"},'
        '{"$ref":"https://abducer.local/spec/b.schema.json"}]}\n',
    )
    duplicate = (
        '{"$id":"https://fixture.invalid/duplicate",'
        '"$schema":"https://json-schema.org/draft/2020-12/schema","type":"string"}\n'
    )
    _write(tmp_path / "agentic/spec/a.schema.json", duplicate)
    _write(tmp_path / "agentic/spec/b.schema.json", duplicate)
    with pytest.raises(DependencyAuthorityError, match="duplicate JSON-Schema"):
        build_dependency_authority(**_semantic_schema_profile(tmp_path))

    _write(
        tmp_path / "agentic/spec/b.schema.json",
        '{"$id":"https://fixture.invalid/distinct",'
        '"$schema":"https://json-schema.org/draft/2020-12/schema","type":"string"}\n',
    )
    authority = build_dependency_authority(**_semantic_schema_profile(tmp_path))
    assert {
        "agentic/spec/a.schema.json",
        "agentic/spec/b.schema.json",
    } <= set(authority["schema_closure"]["referenced_paths"])


def _script_profile(root: Path) -> dict[str, Any]:
    return {
        "scope": "script_local_import_fixture",
        "entry_python_paths": {"agentic/scripts/runner.py": ("script_entry",)},
        "semantic_paths": {"agentic/scripts/runner.py": ("script_contract",)},
        "authority_boundary": "Exact script-local import fixture only.",
        "repository_root": root,
        "runtime_distributions": {},
    }


def test_bare_import_resolves_against_importing_script_directory(
    tmp_path: Path,
) -> None:
    _write(tmp_path / "agentic/scripts/runner.py", "from sibling import VALUE\n")
    _write(tmp_path / "agentic/scripts/sibling.py", "VALUE = 1\n")
    authority = build_dependency_authority(**_script_profile(tmp_path))
    assert "agentic/scripts/sibling.py" in {
        row["path"] for row in authority["entries"]
    }


def test_bare_import_rejects_root_and_script_directory_ambiguity(
    tmp_path: Path,
) -> None:
    _write(tmp_path / "agentic/scripts/runner.py", "from sibling import VALUE\n")
    _write(tmp_path / "agentic/scripts/sibling.py", "VALUE = 1\n")
    _write(tmp_path / "sibling.py", "VALUE = 2\n")
    with pytest.raises(DependencyAuthorityError, match="ambiguous repository-local"):
        build_dependency_authority(**_script_profile(tmp_path))


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlink support is required")
def test_bare_import_rejects_script_local_symlink_escape(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _write(repository / "agentic/scripts/runner.py", "from sibling import VALUE\n")
    _write(tmp_path / "outside.py", "VALUE = 1\n")
    (repository / "agentic/scripts/sibling.py").symlink_to(tmp_path / "outside.py")
    with pytest.raises(DependencyAuthorityError, match="symlink"):
        build_dependency_authority(**_script_profile(repository))


def test_third_party_import_requires_exact_distribution_pin(tmp_path: Path) -> None:
    _write(tmp_path / "entry.py", "import jsonschema\n")
    arguments = {
        "scope": "third_party_fixture",
        "entry_python_paths": {"entry.py": ("entry",)},
        "semantic_paths": {"entry.py": ("semantic_identity",)},
        "authority_boundary": "Exact third-party fixture only.",
        "repository_root": tmp_path,
    }
    with pytest.raises(DependencyAuthorityError, match="runtime pin"):
        build_dependency_authority(**arguments)
    authority = build_dependency_authority(
        **arguments, runtime_distributions={"jsonschema": "jsonschema"}
    )
    assert authority["import_boundary"]["third_party_modules"][0]["module"] == "jsonschema"
    assert {row["name"] for row in authority["runtime_dependencies"]} == {
        "python",
        "jsonschema",
    }


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlink support is required")
def test_semantic_symlink_is_rejected(local_profile: dict[str, Any]) -> None:
    root = local_profile["root"]
    arguments = dict(local_profile["arguments"])
    link = root / "docs/link.md"
    link.symlink_to(root / "docs/contract.md")
    arguments["semantic_paths"] = {"docs/link.md": ("unsafe_contract",)}
    with pytest.raises(DependencyAuthorityError, match="symlink"):
        build_dependency_authority(**arguments)


def test_formal_authority_contains_real_import_and_schema_closure() -> None:
    authority = build_formal_dependency_authority()
    local_paths = set(authority["import_boundary"]["repository_local_python_paths"])
    assert {
        "agentic/discovery/hypotheses.py",
        "agentic/discovery/literature.py",
        "agentic/discovery/parallel.py",
    } <= local_paths
    assert {
        "agentic/spec/abstraction_forge_packet.schema.json",
        "agentic/spec/abstraction_parallel_evaluation.schema.json",
        "agentic/spec/ym_categorical_hott_bridge.schema.json",
        "agentic/spec/high_risk_hypothesis_portfolio.schema.json",
        "agentic/spec/seed_free_high_risk_elicitation.schema.json",
        "agentic/spec/target_literature_search_snapshot.schema.json",
        "agentic/spec/literature_assimilation_packet.schema.json",
        "agentic/spec/parallel_hypothesis_portfolio.schema.json",
    } <= set(authority["schema_closure"]["literal_paths"])
    assert validate_formal_dependency_authority(authority) == authority
