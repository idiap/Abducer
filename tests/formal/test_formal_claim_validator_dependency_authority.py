# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial coverage for the formal-claim validator's derived closure."""

from __future__ import annotations

import copy
import dataclasses
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

import agentic.discovery.dependency_authority as dependency_authority
import agentic.discovery.theory_gate as theory_gate
from agentic.discovery.contracts import ContractError, bytes_digest
from agentic.discovery.dependency_authority import (
    DependencyAuthorityError,
    build_dependency_authority,
)
from agentic.discovery.receipts import (
    ValidatorBinding,
    _validator_authority_material,
    validator_dependency_policy_is_supported,
    verify_current_validator_authority,
)
from agentic.scripts.discovery_operator_registry import load_registry
from agentic.scripts.dispatch_discovery_operators import (
    operator_bindings_from_registry,
)


ROOT = Path(__file__).resolve().parents[2]


def _formal_binding(registry: dict[str, Any] | None = None) -> ValidatorBinding:
    payload = registry or load_registry()
    operator = next(
        row
        for row in operator_bindings_from_registry(payload)
        if row.operator_id == "formal-claim-producer"
    )
    return operator.validators[0]


def _formal_authority(
    tmp_path: Path,
) -> tuple[ValidatorBinding, dict[str, Any]]:
    binding = _formal_binding()
    authority, _command, _materials = _validator_authority_material(
        binding, tmp_path
    )
    return binding, authority


def _relocate_authority_files(
    authority: dict[str, Any], destination: Path
) -> Path:
    repository = destination / "relocated-repository"
    for row in authority["files"]:
        if row["path_scope"] != "repository_relative":
            continue
        source = ROOT / row["runtime_path"]
        target = repository / row["runtime_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return repository


def _derived_closure(authority: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row
        for row in authority["dependency_identities"]
        if row["kind"] == "derived_repository_closure_v2"
    ]
    assert len(rows) == 1
    return rows[0]["authority"]


@pytest.mark.parametrize(
    ("authority", "expected"),
    [
        (
            {
                "dependency_policy": "declared_only",
                "coverage": {
                    "excluded": [
                        "undeclared transitive imports beyond explicit dependency paths"
                    ]
                },
                "dependency_identities": [],
            },
            True,
        ),
        (
            {
                "dependency_policy": "derived_repository_closure_v2",
                "coverage": {"excluded": []},
                "dependency_identities": [
                    {
                        "kind": "derived_repository_closure_v2",
                        "authority": {"authority_digest": "sha256:" + "0" * 64},
                    }
                ],
            },
            True,
        ),
        (
            {
                "dependency_policy": "derived_repository_closure_v2",
                "coverage": {"excluded": []},
                "dependency_identities": [],
            },
            False,
        ),
        (
            {
                "dependency_policy": "derived_repository_closure_v2",
                "coverage": {"excluded": []},
                "dependency_identities": [
                    {
                        "kind": "derived_repository_closure_v2",
                        "authority": {},
                    },
                    {"kind": "substituted", "authority": {}},
                ],
            },
            False,
        ),
        (
            {
                "dependency_policy": "derived_repository_closure_v2",
                "coverage": {"excluded": []},
                "dependency_identities": [
                    {"kind": "substituted", "authority": {}}
                ],
            },
            False,
        ),
    ],
    ids=(
        "legacy-declared-exclusion",
        "derived-exact",
        "derived-omitted",
        "derived-extra",
        "derived-substituted",
    ),
)
def test_theory_gate_accepts_only_supported_validator_dependency_policy(
    authority: dict[str, Any], expected: bool
) -> None:
    assert validator_dependency_policy_is_supported(authority) is expected
    assert (
        theory_gate.validator_dependency_policy_is_supported
        is validator_dependency_policy_is_supported
    )


def test_formal_validator_derives_complete_captured_roots_and_runtime_pins(
    tmp_path: Path,
) -> None:
    binding, authority = _formal_authority(tmp_path)
    closure = _derived_closure(authority)
    paths = {row["path"] for row in closure["entries"]}
    roots = {
        (row["kind"], row["path"])
        for row in closure["declared_roots"]
    }

    assert binding.dependency_policy == "derived_repository_closure_v2"
    assert binding.dependency_paths == ()
    assert {
        ("entry_python", "agentic/scripts/run_discovery_operator_protocol.py"),
        (
            "entry_python",
            "agentic/scripts/validate_discovery_operator_protocol.py",
        ),
        ("entry_python", "agentic/scripts/dispatch_discovery_operators.py"),
        ("entry_python", "agentic/scripts/discovery_operator_registry.py"),
        (
            "semantic",
            "agentic/spec/discovery_formal_claim_schedule_binding_v1.schema.json",
        ),
        (
            "semantic",
            "agentic/registries/discovery_operator_registry.yaml",
        ),
        ("semantic", "skills/reasoning/formal-claim-producer/SKILL.md"),
    } <= roots
    assert {
        "agentic/discovery/__init__.py",
        "agentic/discovery/formal_claim_authority.py",
        "agentic/discovery/receipts.py",
        "agentic/spec/discovery_formal_claim_schedule_binding_v1.schema.json",
        "agentic/spec/discovery_proof_handoff.schema.json",
    } <= paths
    assert {
        row["name"] for row in closure["runtime_dependencies"]
    } == {"python", "jsonschema", "referencing"}
    assert all(
        row["version"] and row["version"] != "unknown"
        for row in closure["runtime_dependencies"]
    )
    assert "no truth, proof, theorem" in closure["authority_boundary"]
    material_rows = {
        row["runtime_path"]: row
        for row in authority["files"]
        if row["path_scope"] == "repository_relative"
    }
    assert set(material_rows) == paths
    for entry in closure["entries"]:
        row = material_rows[entry["path"]]
        assert row["sha256"] == entry["content_digest"]
        assert row["size_bytes"] == entry["byte_size"]


def test_current_formal_validator_closure_is_relocation_safe(
    tmp_path: Path,
) -> None:
    binding, authority = _formal_authority(tmp_path)
    repository = _relocate_authority_files(authority, tmp_path)
    verify_current_validator_authority(
        authority, binding, repository_root=repository
    )


@pytest.mark.parametrize("mutation", ["omitted", "extra", "substituted"])
def test_current_verification_rejects_mutated_closure_entries(
    tmp_path: Path, mutation: str
) -> None:
    binding, authority = _formal_authority(tmp_path)
    repository = _relocate_authority_files(authority, tmp_path)
    changed = copy.deepcopy(authority)
    entries = _derived_closure(changed)["entries"]
    if mutation == "omitted":
        entries.pop()
    elif mutation == "extra":
        extra = copy.deepcopy(entries[-1])
        extra["path"] = "agentic/spec/injected-extra.schema.json"
        entries.append(extra)
    else:
        entries[-1]["path"] = "agentic/spec/substituted.schema.json"

    with pytest.raises(ContractError, match="derived repository closure differs"):
        verify_current_validator_authority(
            changed, binding, repository_root=repository
        )


@pytest.mark.parametrize("mutation", ["omitted", "extra", "role_substitution"])
def test_current_verification_rejects_mutated_closure_file_bijection(
    tmp_path: Path, mutation: str
) -> None:
    binding, authority = _formal_authority(tmp_path)
    repository = _relocate_authority_files(authority, tmp_path)
    changed = copy.deepcopy(authority)
    local_index = next(
        index
        for index, row in enumerate(changed["files"])
        if row["path_scope"] == "repository_relative"
    )
    if mutation == "omitted":
        changed["files"].pop(local_index)
        message = "closure differs from registry"
    elif mutation == "extra":
        changed["files"].append(copy.deepcopy(changed["files"][local_index]))
        changed["files"][-1]["runtime_path"] = "agentic/spec/injected.json"
        message = "closure differs from registry"
    else:
        changed["files"][local_index]["roles"].append("substituted_role")
        message = "substituted closure roles"

    with pytest.raises(ContractError, match=message):
        verify_current_validator_authority(
            changed, binding, repository_root=repository
        )


def test_current_verification_rejects_one_byte_and_lazy_ref_drift(
    tmp_path: Path,
) -> None:
    binding, authority = _formal_authority(tmp_path)
    repository = _relocate_authority_files(authority, tmp_path)
    source = repository / "agentic/discovery/formal_claim_authority.py"
    source.write_bytes(source.read_bytes() + b"\n# one-byte-class drift\n")
    with pytest.raises(ContractError, match="derived repository closure differs"):
        verify_current_validator_authority(
            authority, binding, repository_root=repository
        )

    repository = _relocate_authority_files(authority, tmp_path / "lazy")
    lazy_schema = repository / "agentic/spec/formal-claim-lazy-attack.schema.json"
    lazy_schema.write_text('{"type":"null"}\n', encoding="utf-8")
    schedule = (
        repository
        / "agentic/spec/discovery_formal_claim_schedule_binding_v1.schema.json"
    )
    payload = json.loads(schedule.read_text(encoding="utf-8"))
    payload["allOf"] = [{"$ref": "formal-claim-lazy-attack.schema.json"}]
    schedule.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ContractError, match="derived repository closure differs"):
        verify_current_validator_authority(
            authority, binding, repository_root=repository
        )


def test_formal_validator_rejects_workspace_import_shadowing(
    tmp_path: Path,
) -> None:
    shadow = (
        tmp_path
        / "agentic/scripts/validate_discovery_operator_protocol.py"
    )
    shadow.parent.mkdir(parents=True)
    shadow.write_text("raise SystemExit('shadow')\n", encoding="utf-8")

    with pytest.raises(ContractError, match="import shadowing"):
        _validator_authority_material(_formal_binding(), tmp_path)


def test_formal_validator_rejects_registry_current_mismatch(
    tmp_path: Path,
) -> None:
    binding, authority = _formal_authority(tmp_path)
    repository = _relocate_authority_files(authority, tmp_path)
    stale_binding = dataclasses.replace(
        binding, registry_digest="sha256:" + "0" * 64
    )
    with pytest.raises(ContractError, match="registry/current mismatch"):
        verify_current_validator_authority(
            authority, stale_binding, repository_root=repository
        )


def test_registry_rejects_substituted_formal_dependency_root(
    tmp_path: Path,
) -> None:
    registry = load_registry()
    formal = next(
        row
        for row in registry["operators"]
        if row["operator_id"] == "formal-claim-producer"
    )
    profile = formal["validators"][0]["dependency_profile"]
    profile["semantic_paths"]["agentic/spec/discovery_operator_receipt.schema.json"] = (
        profile["semantic_paths"].pop(
            "agentic/spec/discovery_formal_claim_schedule_binding_v1.schema.json"
        )
    )
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match="derived dependency profile drift"):
        load_registry(path)


def test_dependency_builder_rejects_capture_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    root_module = package / "root.py"
    root_module.write_text("VALUE = 1\n", encoding="utf-8")
    semantic = tmp_path / "contract.md"
    semantic.write_text("exact bytes\n", encoding="utf-8")
    original = dependency_authority._capture_regular_file
    raced = False

    def capture_then_mutate(
        root: Path, relative: str
    ) -> tuple[bytes, tuple[int, ...]]:
        nonlocal raced
        captured = original(root, relative)
        if relative == "pkg/root.py" and not raced:
            raced = True
            root_module.write_text("VALUE = 2\n", encoding="utf-8")
        return captured

    monkeypatch.setattr(
        dependency_authority, "_capture_regular_file", capture_then_mutate
    )
    with pytest.raises(DependencyAuthorityError, match="changed after capture"):
        build_dependency_authority(
            scope="capture_race_fixture",
            entry_python_paths={"pkg/root.py": ("entry",)},
            semantic_paths={"contract.md": ("semantic",)},
            authority_boundary="Exact captured fixture bytes only.",
            repository_root=tmp_path,
            runtime_distributions={},
        )


def test_dependency_builder_rejects_ancestor_directory_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A retained parent dirfd must never follow a replacement directory."""

    package = tmp_path / "pkg"
    package.mkdir()
    (package / "__init__.py").write_text("SOURCE = 'trusted'\n", encoding="utf-8")
    (package / "root.py").write_text("VALUE = 'trusted'\n", encoding="utf-8")
    attacker = tmp_path / "attacker-pkg"
    attacker.mkdir()
    (attacker / "__init__.py").write_text("SOURCE = 'attacker'\n", encoding="utf-8")
    (attacker / "root.py").write_text("VALUE = 'attacker'\n", encoding="utf-8")
    semantic = tmp_path / "contract.md"
    semantic.write_text("exact trusted bytes\n", encoding="utf-8")
    retained = tmp_path / "retained-trusted-pkg"
    real_open = dependency_authority.os.open
    swapped = False

    def open_then_swap_ancestor(
        path: str | bytes | Path,
        flags: int,
        mode: int = 0o777,
        *,
        dir_fd: int | None = None,
    ) -> int:
        nonlocal swapped
        descriptor = real_open(path, flags, mode, dir_fd=dir_fd)
        if path == "pkg" and dir_fd is not None and not swapped:
            swapped = True
            package.rename(retained)
            attacker.rename(package)
        return descriptor

    monkeypatch.setattr(dependency_authority.os, "open", open_then_swap_ancestor)
    with pytest.raises(DependencyAuthorityError, match="changed after capture"):
        build_dependency_authority(
            scope="ancestor_swap_fixture",
            entry_python_paths={"pkg/root.py": ("entry",)},
            semantic_paths={"contract.md": ("semantic",)},
            authority_boundary="Exact component-wise trusted fixture bytes only.",
            repository_root=tmp_path,
            runtime_distributions={},
        )
    assert swapped is True


def test_captured_entry_digests_are_exact_bytes(tmp_path: Path) -> None:
    binding, authority = _formal_authority(tmp_path)
    closure = _derived_closure(authority)
    rows = {
        row["runtime_path"]: row
        for row in authority["files"]
        if row["path_scope"] == "repository_relative"
    }
    assert binding.dependency_profile is not None
    for entry in closure["entries"]:
        assert rows[entry["path"]]["sha256"] == entry["content_digest"]
        assert entry["content_digest"].startswith("sha256:")
        source = ROOT / entry["path"]
        assert bytes_digest(source.read_bytes()) == entry["content_digest"]
