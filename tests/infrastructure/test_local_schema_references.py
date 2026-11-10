# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Runtime JSON-Schema resolution is exact, local, and mutation sensitive."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

import agentic.discovery.contracts as contracts
from agentic.discovery.contracts import ContractError, canonical_digest, validate_instance


def _source_binding() -> dict:
    payload = {
        "schema_version": "1.0.0",
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "source_manifest_path": "agentic/external/manifest.json",
        "source_manifest_sha256": "sha256:" + "1" * 64,
        "source_archive_path": "agentic/external/source.zip",
        "source_archive_sha256": "sha256:d34b5daca880bed58e2fa908d7dbaa137c55b9f1980b89dcdc26498528e7492f",
        "source_archive_size_bytes": 55272541,
        "frontier_capture_path": "agentic/evals/frontier.json",
        "frontier_capture_sha256": "sha256:" + "2" * 64,
        "frontier_capture_id": "capture.fixture",
        "coverage_cutoff": "2026-07-22T00:00:00Z",
        "freshness_at_execution": "active_current",
        "search_completed_at": "2026-07-22T00:00:00Z",
        "consume_before": "2026-07-22T06:00:00Z",
        "committed_at": "2026-07-22T00:01:00Z",
        "license_status": "unknown",
        "authorship_status": "unknown",
        "authority_boundary": "Fixture provenance only; no scientific authority.",
    }
    payload["content_digest"] = canonical_digest(payload)
    return payload


def _registered_binding() -> dict:
    payload = {
        "schema_version": "2.0.0",
        "binding_id": "ym-current-publication." + "3" * 24,
        "status": "current_publication",
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "run_id": "ym21-canonical-parent-20260721",
        "cycle_id": "cycle.fixture",
        "commit_id": "commit.fixture",
        "profile_id": "ym-representational-dynamics-20260721",
        "profile_version": "1.0.0",
        "profile_authority_digest": "sha256:" + "4" * 64,
        "publication_root": "agentic/reports/ym",
        "immutable_index_snapshot_path": "agentic/reports/ym/indexes/index.json",
        "immutable_index_snapshot_sha256": "sha256:" + "5" * 64,
        "bundle_id": "ym-" + "6" * 64,
        "bundle_path": "agentic/reports/ym/publications/bundle",
        "bundle_manifest_digest": "sha256:" + "7" * 64,
        "evidence_id": "evidence-" + "8" * 64,
        "evidence_path": "agentic/reports/ym/evidence/evidence",
        "evidence_manifest_digest": "sha256:" + "9" * 64,
        "locators": {
            "cycle_path": "agentic/reports/ym/cycle.json",
            "cycle_request_path": "agentic/reports/ym/request.json",
            "state_root": "agentic/reports/ym/state",
            "workspace": "agentic/reports/ym/workspace",
            "receipt_root": "agentic/reports/ym/receipts",
        },
        "legacy_archives": [{}],
        "source_provenance": _source_binding(),
        "validation_status": "passed",
        "authority_boundary": "Fixture binding only; no scientific authority.",
    }
    payload["content_digest"] = canonical_digest(payload)
    return payload


def test_repository_local_schema_reference_resolves_and_validates_nested_data() -> None:
    binding = _registered_binding()
    validate_instance(binding, "ym_registered_publication_binding.schema.json")
    broken = copy.deepcopy(binding)
    broken["source_provenance"]["source_archive_sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ContractError, match="source_archive_sha256"):
        validate_instance(broken, "ym_registered_publication_binding.schema.json")


def test_schema_reference_resolution_never_fetches_untrusted_uris(tmp_path: Path) -> None:
    schema = tmp_path / "remote.schema.json"
    schema.write_text(
        '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
        '"$id":"https://fixture.invalid/root.schema.json",'
        '"$ref":"https://untrusted.invalid/remote.schema.json"}',
        encoding="utf-8",
    )
    with pytest.raises(ContractError, match="schema reference resolution failed"):
        validate_instance({}, schema)


def _schema(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_document_relative_reference_works_without_root_id(tmp_path: Path) -> None:
    child = tmp_path / "nested/child.schema.json"
    _schema(
        child,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string"},
    )
    root = tmp_path / "root.schema.json"
    _schema(
        root,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "properties": {"value": {"$ref": "nested/child.schema.json"}},
        },
    )
    validate_instance({"value": "ok"}, root)
    with pytest.raises(ContractError, match="is not of type 'string'"):
        validate_instance({"value": 1}, root)


@pytest.mark.parametrize("kind", ["absolute_path", "file_uri"])
def test_absolute_local_reference_is_exact_and_confined(
    tmp_path: Path, kind: str
) -> None:
    child = tmp_path / "nested/child.schema.json"
    _schema(
        child,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "integer"},
    )
    reference = str(child) if kind == "absolute_path" else child.as_uri()
    root = tmp_path / f"{kind}.schema.json"
    _schema(
        root,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "$ref": reference},
    )
    validate_instance(2, root)
    with pytest.raises(ContractError, match="is not of type 'integer'"):
        validate_instance("2", root)


def test_duplicate_nested_ids_and_basename_aliases_fail_closed(tmp_path: Path) -> None:
    duplicate_id = "https://fixture.invalid/schema/duplicate"
    for name in ("a", "b"):
        _schema(
            tmp_path / f"nested/{name}.schema.json",
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": duplicate_id,
                "type": "string",
            },
        )
    root = tmp_path / "duplicates.schema.json"
    _schema(
        root,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "allOf": [
                {"$ref": "nested/a.schema.json"},
                {"$ref": "nested/b.schema.json"},
            ],
        },
    )
    with pytest.raises(ContractError, match="duplicate_id"):
        validate_instance("value", root)

    _schema(
        tmp_path / "only-at-root.schema.json",
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string"},
    )
    missing = tmp_path / "missing.schema.json"
    _schema(
        missing,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "nested/only-at-root.schema.json",
        },
    )
    with pytest.raises(ContractError, match="local_schema\[missing\]"):
        validate_instance("value", missing)


def test_structural_cache_rechecks_instance_and_referenced_schema_bytes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root.schema.json"
    child = tmp_path / "child.schema.json"
    _schema(root, {"$ref": "child.schema.json"})
    _schema(child, {"type": "array", "items": {"type": "string"}})
    validate_instance(["ok"], root, cache_json_structure=True)
    validate_instance(["ok"], root, cache_json_structure=True)
    with pytest.raises(contracts.SchemaValidationError):
        validate_instance([1], root, cache_json_structure=True)
    # A tuple serializes like a list but is not a JSON-Schema array.
    with pytest.raises(contracts.SchemaValidationError):
        validate_instance(("ok",), root, cache_json_structure=True)
    before = child.stat()
    encoded = child.read_bytes().replace(b'string', b'number')
    child.write_bytes(encoded)
    os.utime(child, ns=(before.st_atime_ns, before.st_mtime_ns))
    with pytest.raises(contracts.SchemaValidationError):
        validate_instance(["ok"], root, cache_json_structure=True)
    child.unlink()
    replacement = tmp_path / "replacement.schema.json"
    _schema(replacement, {"type": "array", "items": {"type": "string"}})
    child.symlink_to(replacement)
    with pytest.raises(ContractError, match="symlink"):
        validate_instance(["ok"], root, cache_json_structure=True)


def test_meta_validation_cache_observes_same_path_byte_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "mutable.schema.json"
    original = contracts.Draft202012Validator.check_schema
    calls = 0

    def counted(schema: dict, *args: object, **kwargs: object) -> None:
        nonlocal calls
        calls += 1
        original(schema, *args, **kwargs)

    contracts._meta_validated_schema_bytes.cache_clear()
    monkeypatch.setattr(contracts.Draft202012Validator, "check_schema", counted)
    _schema(
        path,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string"},
    )
    validate_instance("ok", path)
    validate_instance("ok", path)
    assert calls == 1
    _schema(
        path,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": 7},
    )
    with pytest.raises(ContractError, match="invalid JSON Schema"):
        validate_instance("ok", path)
    assert calls == 2


def test_schema_path_alias_normalization_keeps_inner_symlinks_unsafe(
    tmp_path: Path,
) -> None:
    real = tmp_path / "real"
    root = real / "root.schema.json"
    _schema(
        root,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"},
    )
    outer_alias = tmp_path / "outer-alias"
    outer_alias.symlink_to(real, target_is_directory=True)
    validate_instance({}, outer_alias / root.name)

    child = real / "child.schema.json"
    _schema(
        child,
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string"},
    )
    (real / "linked.schema.json").symlink_to(child)
    with pytest.raises(ContractError, match="local_schema\[symlink\]"):
        validate_instance("value", real / "linked.schema.json")
