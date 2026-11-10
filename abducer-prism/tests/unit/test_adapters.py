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

import tomllib
from pathlib import Path

import pytest
from to_prism.adapters import AdapterError, generate_python_adapter_package


def test_python_adapter_is_installable_entry_point_leaf(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    implementation = source / "transform.py"
    implementation.write_text(
        "def transform(text):\n    return text.upper()\n", encoding="utf-8"
    )
    project = tmp_path / "project"

    package = generate_python_adapter_package(
        source_root=source,
        project_root=project,
        specifications=[
            {
                "operation": "example.transform",
                "source_path": "transform.py",
                "function": "transform",
                "input_type": "ClaimNormalizationRequest",
                "output_type": "NormalizedClaimText",
                "input_field": "source_claim_text",
                "output_field": "normalized_claim_text",
            }
        ],
    )

    assert package == project / "adapters"
    metadata = tomllib.loads((package / "pyproject.toml").read_text(encoding="utf-8"))
    bindings = metadata["project"]["entry-points"]["prism.python_effects"]
    assert bindings == {
        "example.transform": "converted_prism_adapters.effects:effect_1"
    }
    assert (
        package / "src/converted_prism_adapters/upstream/leaf_1.py"
    ).read_bytes() == implementation.read_bytes()
    effects = (package / "src/converted_prism_adapters/effects.py").read_text()
    assert "except Exception as exc:" in effects
    assert "result = Err(message)" in effects


@pytest.mark.parametrize(
    "specification",
    [
        {"operation": "Bad Operation", "source_path": "leaf.py", "function": "run"},
        {"operation": "valid.op", "source_path": "../outside.py", "function": "run"},
        {"operation": "valid.op", "source_path": "leaf.py", "function": "not-call()"},
    ],
)
def test_python_adapter_rejects_ambiguous_bindings(
    tmp_path: Path, specification: dict[str, str]
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "leaf.py").write_text(
        "def run(value):\n    return value\n", encoding="utf-8"
    )
    (tmp_path / "outside.py").write_text(
        "def run(value):\n    return value\n", encoding="utf-8"
    )

    with pytest.raises(AdapterError):
        generate_python_adapter_package(
            source_root=source,
            project_root=tmp_path / "project",
            specifications=[specification],
        )


def test_python_adapter_rejects_duplicate_operations(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "leaf.py").write_text(
        "def run(value):\n    return value\n", encoding="utf-8"
    )
    specification = {
        "operation": "valid.op",
        "source_path": "leaf.py",
        "function": "run",
        "input_type": "ReviewedLeafRequest",
        "output_type": "ReviewedLeafResponse",
        "input_field": "source_value",
        "output_field": "returned_value",
    }
    with pytest.raises(AdapterError, match="duplicate logical operation"):
        generate_python_adapter_package(
            source_root=source,
            project_root=tmp_path / "project",
            specifications=[specification, specification],
        )
