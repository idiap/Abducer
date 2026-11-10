# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Local archive defaults must survive replay without deleting their inputs."""

from pathlib import Path
import sys
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

import integrate_ym_representational_dynamics as legacy  # noqa: E402
import validate_cohere_fast_source_manifest as cohere  # noqa: E402


def test_legacy_extraction_preserves_local_archives_on_repeat(tmp_path, monkeypatch):
    archive_root = tmp_path / "source_archives"
    archive_root.mkdir()
    sources = [archive_root / "research.zip", archive_root / "skills.zip"]
    for source in sources:
        with ZipFile(source, "w") as archive:
            archive.writestr("example.txt", source.name)
    original = [p.read_bytes() for p in sources]
    for name in ["RESEARCH_ROOT", "SKILL_BUNDLE_ROOT", "REPORT_ROOT", "PROOF_OBJECT_ROOT", "SMOKE_ROOT"]:
        monkeypatch.setattr(legacy, name, tmp_path / name)
    monkeypatch.setattr(legacy, "ROOT", tmp_path)
    monkeypatch.setattr(legacy, "ARCHIVE_ROOT", archive_root)
    monkeypatch.setattr(legacy, "SOURCE_RESEARCH_ZIP", sources[0])
    monkeypatch.setattr(legacy, "SOURCE_SKILL_ZIP", sources[1])
    monkeypatch.setattr(legacy, "rel", lambda p: str(p.relative_to(tmp_path)))
    for _ in range(2):
        legacy.extract_archives()
        assert [p.read_bytes() for p in sources] == original
        assert (legacy.RESEARCH_ROOT / "example.txt").read_text() == "research.zip"


def test_source_manifest_accepts_local_archive_override(tmp_path, monkeypatch):
    monkeypatch.setattr(cohere, "ROOT", tmp_path)
    source = tmp_path / "source_archives/source.zip"
    source.parent.mkdir()
    with ZipFile(source, "w") as archive:
        archive.writestr("README.md", "Source fixture")
    manifest, _, _ = cohere.records(source)
    assert manifest["archive"] == "source_archives/source.zip"
    assert manifest["member_count"] == 1


def test_missing_archive_explains_override(tmp_path):
    with pytest.raises(SystemExit, match="supply --archive PATH"):
        cohere.records(tmp_path / "missing.zip")
