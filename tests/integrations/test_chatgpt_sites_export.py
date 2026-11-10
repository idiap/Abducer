# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""The Sites library retains canonical sources without including runtime state."""

import hashlib
import json

import pytest

from integrations.chatgpt.catalog import Catalog
from integrations.chatgpt import sites_export


def test_library_matches_canonical_skill_contract_and_graph_sources():
    catalog = Catalog(sites_export.ROOT)
    library = sites_export.build_library()
    assert library["release"] == catalog.release
    assert len(library["skills"]) == len(catalog.skills) == 221
    assert len(library["workflows"]) == len(catalog.native.rows) == 34
    assert library["capabilities"]["graph_count"] == len(catalog.viewers) == 19
    assert not library["capabilities"]["native_execution"]
    assert not library["capabilities"]["scientific_truth_verified"]
    assert library["capabilities"]["chat_guided_research"]
    for skill in library["skills"]:
        raw = (sites_export.ROOT / skill["path"]).read_bytes()
        assert skill["content"] == raw.decode("utf-8-sig")
        assert skill["sha256"] == hashlib.sha256(raw).hexdigest()
        assert set(skill) == {"name", "description", "content", "path", "sha256"}
    for workflow in library["workflows"]:
        detail = catalog.get_workflow(workflow["id"])
        assert workflow["contract"] == detail["workflow"]["contract"]
        assert workflow["viewer"] == detail["viewer"]
        assert workflow["graph"] == (
            detail["viewer"]["graph"] if detail["viewer"] else None
        )
        assert workflow["execution_status"] == "inspectable"


def test_export_is_deterministic_and_excludes_unregistered_files(tmp_path):
    # Catalog-backed export has no filesystem discovery. Extra caller files are
    # outside its allowlist and must not leak into a deployment library.
    unregistered = tmp_path / "private-run-secret.txt"
    unregistered.write_text("private-test-marker")
    first = sites_export.export_bytes()
    assert first == sites_export.export_bytes()
    assert b"private-test-marker" not in first
    assert len(first) <= sites_export.MAX_EXPORT_BYTES
    assert set(json.loads(first)) == {
        "schema_version",
        "release",
        "skills",
        "workflows",
        "capabilities",
    }


def test_failed_verification_preserves_existing_output(tmp_path, monkeypatch):
    output = tmp_path / "library.json"
    output.write_bytes(b"previous-good-export")

    class InvalidCatalog:
        def __init__(self, root):
            raise ValueError("Canonical source drift")

    monkeypatch.setattr(sites_export, "Catalog", InvalidCatalog)
    with pytest.raises(ValueError, match="Canonical source drift"):
        sites_export.main(["--output", str(output)])
    assert output.read_bytes() == b"previous-good-export"


def test_export_budget_rejects_oversized_library(monkeypatch):
    monkeypatch.setattr(sites_export, "MAX_EXPORT_BYTES", 5)
    with pytest.raises(ValueError, match="export budget"):
        sites_export.export_bytes()


def test_cli_writes_expected_complete_library(tmp_path, capsys):
    output = tmp_path / "nested/library.json"
    assert sites_export.main(["--output", str(output)]) == 0
    assert output.read_bytes() == sites_export.export_bytes()
    assert json.loads(capsys.readouterr().out)["skills"] == 221
    assert list(output.parent.iterdir()) == [output]
