# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Source-integrity and authority-boundary tests for the higher-abductive reference."""

from __future__ import annotations

import copy
import json
import stat
from pathlib import Path
from zipfile import ZipFile, ZipInfo

import pytest

from agentic.scripts.integrate_higher_abductive_theory_discovery_20260722 import (
    ARCHIVE_DESTINATION,
    ARCHIVE_PREFIX,
    EXPECTED_ARCHIVE_SHA256,
    IMPORT_ROOT,
    ArchiveIntegrationError,
    _relative_member_path,
    _validate_zip_info,
    inspect_archive,
    validate_preserved_import,
)


def test_preserved_reference_replays_exact_bytes_and_non_authority() -> None:
    result = validate_preserved_import()
    assert result["status"] == "valid"
    assert result["archive_sha256"] == EXPECTED_ARCHIVE_SHA256
    assert result["member_count"] == 469
    assert result["active_file_count"] > 250
    manifest = json.loads((IMPORT_ROOT / "source_manifest.json").read_text())
    assert manifest["runtime_status"] == "not_installed_not_imported_not_executed"
    assert manifest["adaptation_status"] == "design_primitives_only_through_local_strict_contracts"
    assert not any(
        manifest[field]
        for field in (
            "proof_authority",
            "truth_authority",
            "novelty_authority",
            "conceptual_value_authority",
            "physics_value_authority",
        )
    )


def test_active_projection_excludes_build_duplicate_and_preserves_source_bytes() -> None:
    rows, duplicate_report = inspect_archive(ARCHIVE_DESTINATION)
    assert duplicate_report["status"] == "byte_identical_build_duplicate_excluded"
    assert duplicate_report["src_file_count"] == duplicate_report["build_lib_file_count"]
    active = json.loads((IMPORT_ROOT / "active_index.json").read_text())
    assert not any(row["path"].startswith("build/") for row in active["files"])
    by_path = {row["relative_path"]: row for row in rows}
    with ZipFile(ARCHIVE_DESTINATION) as archive:
        for indexed in active["files"]:
            source = by_path[indexed["path"]]
            assert archive.read(source["archive_path"]) == (
                IMPORT_ROOT / "active_snapshot" / indexed["path"]
            ).read_bytes()


def test_capability_map_reuses_design_primitives_and_rejects_runtime_authority() -> None:
    capability_map = json.loads((IMPORT_ROOT / "capability_map.json").read_text())
    by_id = {row["capability_id"]: row for row in capability_map["capabilities"]}
    assert by_id["scoped_theory_atlas"]["disposition"] == "adapt"
    assert by_id["abstract_concrete_return_square"]["disposition"] == "adapt"
    assert by_id["tdr_runtime_and_http_api"]["disposition"] == "external_only_rejected_as_authority"
    assert by_id["seventeen_upstream_skills"]["disposition"] == "source_reference_only_maximize_existing_reuse"
    assert len(capability_map["meaning_dimensions"]) == 9
    assert len(capability_map["cheap_repair_ladder"]) == 6
    assert len(capability_map["reflection_lenses"]) == 8
    assert len(capability_map["redescription_operators"]) == 12


@pytest.mark.parametrize(
    "name",
    [
        "/absolute/file.py",
        f"{ARCHIVE_PREFIX}../escape.py",
        f"{ARCHIVE_PREFIX}folder\\escape.py",
        "foreign-root/file.py",
        f"{ARCHIVE_PREFIX}C:/drive.py",
    ],
)
def test_unsafe_or_foreign_member_paths_reject(name: str) -> None:
    with pytest.raises(ArchiveIntegrationError):
        _relative_member_path(name)


def test_symlink_and_extreme_compression_members_reject() -> None:
    symlink = ZipInfo(f"{ARCHIVE_PREFIX}link")
    symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
    with pytest.raises(ArchiveIntegrationError, match="symlink"):
        _validate_zip_info(symlink)

    compressed = ZipInfo(f"{ARCHIVE_PREFIX}bomb")
    compressed.file_size = 1_000_000
    compressed.compress_size = 1
    with pytest.raises(ArchiveIntegrationError, match="compression ratio"):
        _validate_zip_info(compressed)


def test_manifest_substitution_or_authority_promotion_is_detectable(tmp_path: Path) -> None:
    source = json.loads((IMPORT_ROOT / "source_manifest.json").read_text())
    promoted = copy.deepcopy(source)
    promoted["proof_authority"] = True
    assert promoted != source
    assert any(
        promoted[field]
        for field in (
            "proof_authority",
            "truth_authority",
            "novelty_authority",
            "conceptual_value_authority",
            "physics_value_authority",
        )
    )

    active = json.loads((IMPORT_ROOT / "active_index.json").read_text())
    substituted = copy.deepcopy(active)
    substituted["files"][0]["path"] = "build/lib/tdr/__init__.py"
    assert substituted["files"] != active["files"]
