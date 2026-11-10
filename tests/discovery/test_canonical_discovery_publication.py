# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for profile-driven, pointer-last canonical publication.

The lightweight toy profile isolates storage invariants from scientific-cycle
cost.  One real DWF fixture then proves its derived evidence uses logical
locators and remains byte-stable across independent plan/publish staging roots.
"""

from __future__ import annotations

import copy
import json
import multiprocessing
import os
import runpy
import shutil
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

import canonical_publication_engine as engine  # noqa: E402
from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    bytes_digest,
    canonical_digest,
)
from canonical_discovery_publication import (  # noqa: E402
    plan_publication,
    publish_current,
    validate_current_publication,
)
from canonical_publication_engine import (  # noqa: E402
    PublicationContractError,
    PublicationProfile,
    PublicationSource,
    plan_profile_publication,
    publish_profile_current,
    validate_profile_current,
)


def _encoded(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_encoded(value))


def _toy_source(root: Path, marker: str) -> PublicationSource:
    state = root / "state"
    workspace = root / "workspace"
    commit = state / "commits" / f"commit-{marker}"
    commit.mkdir(parents=True)
    workspace.mkdir(parents=True)
    _write_json(commit / "manifest.json", {"marker": marker})
    (workspace / "payload.txt").write_text(marker, encoding="utf-8")
    cycle = root / "cycle.json"
    _write_json(
        cycle,
        {
            "target_id": "toy-target",
            "run_id": "toy-run",
            "cycle_id": f"cycle-{marker}",
            "commit_id": f"commit-{marker}",
            "commit_path": str(commit),
            "manifest_path": str(commit / "manifest.json"),
            "transaction_root": str(state),
            "authority_boundary": "toy structural publication authority only",
            "events": [{"occurred_at": "2026-07-22T00:00:00Z"}],
        },
    )
    return PublicationSource(
        cycle_path=cycle,
        state_root=state,
        workspace=workspace,
        target_id="toy-target",
        run_id="toy-run",
    )


def _authority(marker: str = "authority-a") -> dict[str, Any]:
    encoded = marker.encode()
    value: dict[str, Any] = {
        "authority_version": "2.0.0",
        "scope": "toy_publication_profile",
        "declared_roots": [
            {"kind": "entry_python", "path": "toy.py", "roles": ["toy"]}
        ],
        "entries": [
            {
                "path": "toy.py",
                "roles": ["toy"],
                "byte_size": len(encoded),
                "content_digest": bytes_digest(encoded),
            }
        ],
        "schema_closure": {"literal_paths": [], "referenced_paths": []},
        "import_boundary": {
            "policy": "conservative_repository_local_ast_import_closure_v2",
            "repository_local_python_paths": ["toy.py"],
            "stdlib_modules": [],
            "third_party_modules": [],
        },
        "runtime_dependencies": [{"name": "python", "version": "3"}],
        "authority_boundary": "toy structural publication authority only",
    }
    value["content_digest"] = canonical_digest(value)
    return value


def _toy_profile(
    *, version: str = "1.0.0", evidence_marker: str = "evidence-a"
) -> PublicationProfile:
    authority = _authority()

    def validate_core(
        locators: Mapping[str, Any], _authority_root: Path
    ) -> Mapping[str, Any]:
        if not Path(locators["cycle_path"]).is_file():
            raise ContractError("toy cycle is absent")
        return {"status": "passed"}

    def build_evidence(
        locators: Mapping[str, Any], _authority_root: Path
    ) -> Mapping[str, bytes]:
        bundle = Path(locators["cycle_path"]).parent
        logical = {
            name: path.relative_to(bundle).as_posix()
            for name, path in locators.items()
            if isinstance(path, Path)
        }
        return {
            "toy-evidence.json": _encoded(
                {"marker": evidence_marker, "logical_locators": logical}
            )
        }

    def validate_evidence(
        locators: Mapping[str, Any], evidence: Path, authority_root: Path
    ) -> Mapping[str, Any]:
        expected = build_evidence(locators, authority_root)["toy-evidence.json"]
        if (evidence / "toy-evidence.json").read_bytes() != expected:
            raise ContractError("toy evidence differs from replay")
        return {"status": "validated"}

    return PublicationProfile(
        profile_id="toy-profile",
        profile_version=version,
        bundle_prefix="toy",
        authority_boundary="toy structural publication authority only",
        build_authority=lambda _root: copy.deepcopy(authority),
        validate_core=validate_core,
        build_evidence=build_evidence,
        validate_evidence=validate_evidence,
        semantic_contract={"evidence_marker": evidence_marker},
    )


def _snapshot(publication_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    pointer = json.loads((publication_root / engine.INDEX_NAME).read_text())
    snapshot = json.loads((publication_root / pointer["snapshot_path"]).read_text())
    return pointer, snapshot


def _publish_worker(source: PublicationSource, root: str, marker: str, queue: Any) -> None:
    try:
        result = publish_profile_current(
            source=source,
            profile=_toy_profile(evidence_marker=marker),
            publication_root=Path(root),
        )
        queue.put(
            (
                "ok",
                marker,
                result["bundle_id"],
                result["evidence_id"],
                result["profile_authority_digest"],
            )
        )
    except Exception as exc:  # pragma: no cover - child failure is asserted in parent
        queue.put(("error", type(exc).__name__, str(exc)))


def test_plan_is_read_only_deterministic_and_publish_is_idempotent(tmp_path: Path) -> None:
    source = _toy_source(tmp_path / "source", "a")
    profile = _toy_profile()
    publication = tmp_path / "publication"
    first = plan_profile_publication(
        source=source, profile=profile, publication_root=publication
    )
    second = plan_profile_publication(
        source=source, profile=profile, publication_root=publication
    )
    assert not publication.exists()
    assert (first["bundle_id"], first["evidence_id"]) == (
        second["bundle_id"],
        second["evidence_id"],
    )
    published = publish_profile_current(
        source=source, profile=profile, publication_root=publication
    )
    assert published["bundle_id"] == first["bundle_id"]
    assert published["evidence_id"] == first["evidence_id"]
    before = (publication / engine.INDEX_NAME).read_bytes()
    replay = publish_profile_current(
        source=source, profile=profile, publication_root=publication
    )
    assert replay["core_created"] is False
    assert replay["evidence_created"] is False
    assert replay["index_updated"] is False
    assert (publication / engine.INDEX_NAME).read_bytes() == before


def test_same_core_evidence_versioning_and_a_b_a_history(tmp_path: Path) -> None:
    publication = tmp_path / "publication"
    source_a = _toy_source(tmp_path / "a", "a")
    source_b = _toy_source(tmp_path / "b", "b")
    a1 = publish_profile_current(
        source=source_a, profile=_toy_profile(), publication_root=publication
    )
    a2 = publish_profile_current(
        source=source_a,
        profile=_toy_profile(version="2.0.0"),
        publication_root=publication,
    )
    assert a1["bundle_id"] == a2["bundle_id"]
    assert a1["evidence_id"] != a2["evidence_id"]
    b = publish_profile_current(
        source=source_b,
        profile=_toy_profile(version="2.0.0"),
        publication_root=publication,
    )
    final = publish_profile_current(
        source=source_a,
        profile=_toy_profile(version="2.0.0"),
        publication_root=publication,
    )
    _, snapshot = _snapshot(publication)
    current = (final["bundle_id"], final["evidence_id"])
    history = [(row["bundle_id"], row["evidence_id"]) for row in snapshot["history"]]
    assert current not in history
    assert len(history) == len(set(history))
    assert (a1["bundle_id"], a1["evidence_id"]) in history
    assert (b["bundle_id"], b["evidence_id"]) in history


def test_portable_tree_and_internal_storage_symlink_rejection(tmp_path: Path) -> None:
    source = _toy_source(tmp_path / "source", "a")
    profile = _toy_profile()
    publication = tmp_path / "publication"
    publish_profile_current(source=source, profile=profile, publication_root=publication)
    moved = tmp_path / "moved"
    shutil.copytree(publication, moved)
    assert validate_profile_current(
        publication_root=moved, profile=profile
    )["status"] == "passed"
    indexes = moved / engine.INDEX_DIRECTORY
    external = tmp_path / "external-indexes"
    indexes.rename(external)
    indexes.symlink_to(external, target_is_directory=True)
    with pytest.raises(PublicationContractError) as captured:
        validate_profile_current(publication_root=moved, profile=profile)
    assert captured.value.reason_code == "path_symlink"


def test_public_path_surfaces_report_stable_reason_codes(tmp_path: Path) -> None:
    """Callers can classify unsafe inputs without parsing exception prose."""

    source = _toy_source(tmp_path / "source", "a")
    profile = _toy_profile()

    linked_cycle = tmp_path / "linked-cycle.json"
    linked_cycle.symlink_to(source.cycle_path)
    with pytest.raises(PublicationContractError) as captured:
        plan_profile_publication(
            source=replace(source, cycle_path=linked_cycle),
            profile=profile,
            publication_root=tmp_path / "unused-publication",
        )
    assert captured.value.reason_code == "path_symlink"

    real_root = tmp_path / "real-publication"
    real_root.mkdir()
    linked_root = tmp_path / "linked-publication"
    linked_root.symlink_to(real_root, target_is_directory=True)
    with pytest.raises(PublicationContractError) as captured:
        plan_profile_publication(
            source=source, profile=profile, publication_root=linked_root
        )
    assert captured.value.reason_code == "path_symlink"

    file_root = tmp_path / "publication-file"
    file_root.write_text("not a directory", encoding="utf-8")
    with pytest.raises(PublicationContractError) as captured:
        plan_profile_publication(
            source=source, profile=profile, publication_root=file_root
        )
    assert captured.value.reason_code == "path_not_directory"

    lock_root = tmp_path / "lock-publication"
    lock_root.mkdir()
    external_lock = tmp_path / "external-lock"
    external_lock.write_text("", encoding="utf-8")
    (lock_root / engine.LOCK_NAME).symlink_to(external_lock)
    with pytest.raises(PublicationContractError) as captured:
        publish_profile_current(
            source=source, profile=profile, publication_root=lock_root
        )
    assert captured.value.reason_code == "path_symlink"

    publication = tmp_path / "pointer-publication"
    publish_profile_current(
        source=source, profile=profile, publication_root=publication
    )
    pointer = publication / engine.INDEX_NAME
    retained_pointer = publication / "retained-pointer.json"
    pointer.rename(retained_pointer)
    pointer.symlink_to(retained_pointer.name)
    with pytest.raises(PublicationContractError) as captured:
        validate_profile_current(publication_root=publication, profile=profile)
    assert captured.value.reason_code == "path_symlink"


def test_nested_reserved_names_are_hashed_and_sources_reject_links_and_specials(
    tmp_path: Path,
) -> None:
    source = _toy_source(tmp_path / "source", "a")
    nested = source.workspace / "nested" / engine.BUNDLE_MANIFEST
    nested.parent.mkdir()
    nested.write_text("first", encoding="utf-8")
    first = plan_profile_publication(
        source=source, profile=_toy_profile(), publication_root=tmp_path / "p"
    )
    nested.write_text("second", encoding="utf-8")
    second = plan_profile_publication(
        source=source, profile=_toy_profile(), publication_root=tmp_path / "p"
    )
    assert first["bundle_id"] != second["bundle_id"]

    linked_source = _toy_source(tmp_path / "linked", "a")
    (linked_source.workspace / "link").symlink_to(linked_source.cycle_path)
    with pytest.raises(PublicationContractError) as captured:
        plan_profile_publication(
            source=linked_source,
            profile=_toy_profile(),
            publication_root=tmp_path / "linked-publication",
        )
    assert captured.value.reason_code == "source_symlink"

    if hasattr(os, "mkfifo"):
        special_source = _toy_source(tmp_path / "special", "a")
        os.mkfifo(special_source.workspace / "fifo")
        with pytest.raises(PublicationContractError) as captured:
            plan_profile_publication(
                source=special_source,
                profile=_toy_profile(),
                publication_root=tmp_path / "special-publication",
            )
        assert captured.value.reason_code == "special_file"


def test_concurrent_source_swap_and_after_plan_mutation_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _toy_source(tmp_path / "source", "a")
    outside = tmp_path / "outside"
    outside.write_text("outside", encoding="utf-8")
    original = engine._copy_tree_contents
    swapped = False

    def swap_before_copy(tree: Path, destination: Path) -> None:
        nonlocal swapped
        if tree.resolve() == source.workspace.resolve() and not swapped:
            swapped = True
            payload = source.workspace / "payload.txt"
            payload.unlink()
            payload.symlink_to(outside)
        original(tree, destination)

    monkeypatch.setattr(engine, "_copy_tree_contents", swap_before_copy)
    with pytest.raises(PublicationContractError) as captured:
        plan_profile_publication(
            source=source,
            profile=_toy_profile(),
            publication_root=tmp_path / "publication",
        )
    assert captured.value.reason_code == "source_symlink"
    monkeypatch.setattr(engine, "_copy_tree_contents", original)

    second = _toy_source(tmp_path / "second", "a")

    def mutate_after_plan(phase: str) -> None:
        if phase == "after_plan":
            (second.workspace / "payload.txt").write_text("mutated", encoding="utf-8")

    with pytest.raises(ContractError, match="source changed"):
        publish_profile_current(
            source=second,
            profile=_toy_profile(),
            publication_root=tmp_path / "second-publication",
            failpoint=mutate_after_plan,
        )


@pytest.mark.parametrize(
    "phase",
    [
        "after_bundle_install",
        "after_evidence_install",
        "after_archive_install",
        "after_snapshot_install",
        "before_pointer_replace",
        "after_pointer_replace",
    ],
)
def test_every_late_failpoint_preserves_exact_prior_pointer(
    tmp_path: Path, phase: str
) -> None:
    source_a = _toy_source(tmp_path / "a", "a")
    source_b = _toy_source(tmp_path / "b", "b")
    publication = tmp_path / "publication"
    profile = _toy_profile()
    publish_profile_current(source=source_a, profile=profile, publication_root=publication)
    before = (publication / engine.INDEX_NAME).read_bytes()

    def fail(current: str) -> None:
        if current == phase:
            raise RuntimeError(f"failpoint:{phase}")

    with pytest.raises(RuntimeError, match=phase):
        publish_profile_current(
            source=source_b,
            profile=profile,
            publication_root=publication,
            failpoint=fail,
        )
    assert (publication / engine.INDEX_NAME).read_bytes() == before
    assert validate_profile_current(
        publication_root=publication, profile=profile
    )["bundle_id"] != plan_profile_publication(
        source=source_b, profile=profile, publication_root=publication
    )["bundle_id"]


def test_authority_drift_and_archive_source_mutation_fail_before_pointer(
    tmp_path: Path,
) -> None:
    source_a = _toy_source(tmp_path / "a", "a")
    source_b = _toy_source(tmp_path / "b", "b")
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / "old.txt").write_text("old", encoding="utf-8")
    publication = tmp_path / "publication"
    profile = _toy_profile()
    publish_profile_current(
        source=source_a,
        profile=profile,
        publication_root=publication,
        legacy_bundle=legacy,
    )
    before = (publication / engine.INDEX_NAME).read_bytes()
    legacy.joinpath("old.txt").write_text("changed", encoding="utf-8")
    with pytest.raises(ContractError, match="archive/source-retention"):
        publish_profile_current(
            source=source_b,
            profile=profile,
            publication_root=publication,
            legacy_bundle=legacy,
        )
    assert (publication / engine.INDEX_NAME).read_bytes() == before

    calls = 0
    authority_a = _authority("a")
    authority_b = _authority("b")

    def drifting(_root: Path) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return copy.deepcopy(authority_a if calls < 3 else authority_b)

    drifting_profile = replace(profile, build_authority=drifting)
    clean_publication = tmp_path / "clean-publication"
    publish_profile_current(
        source=source_a, profile=profile, publication_root=clean_publication
    )
    clean_before = (clean_publication / engine.INDEX_NAME).read_bytes()
    with pytest.raises(ContractError, match="authority has drifted"):
        publish_profile_current(
            source=source_b,
            profile=drifting_profile,
            publication_root=clean_publication,
        )
    assert (clean_publication / engine.INDEX_NAME).read_bytes() == clean_before


def test_profile_authority_binds_defaults_keyword_defaults_closures_and_nested_digests(
    tmp_path: Path,
) -> None:
    profile = _toy_profile()

    def make_callback(bound_value: str):
        def callback(
            _locators: Mapping[str, Any],
            _authority_root: Path,
            default_value: str = "default-a",
            *,
            policy: str = "policy-a",
        ) -> Mapping[str, Any]:
            return {
                "status": "passed",
                "bound_value": bound_value,
                "default_value": default_value,
                "policy": policy,
            }

        return callback

    first = engine._callable_authority(make_callback("closure-a"), "validate_core")
    changed_closure = engine._callable_authority(
        make_callback("closure-b"), "validate_core"
    )
    changed_defaults_callable = make_callback("closure-a")
    changed_defaults_callable.__defaults__ = ("default-b",)
    changed_defaults_callable.__kwdefaults__ = {"policy": "policy-b"}
    changed_defaults = engine._callable_authority(
        changed_defaults_callable, "validate_core"
    )
    assert first["code_digest"] == changed_closure["code_digest"]
    assert first["closure_cells_digest"] != changed_closure["closure_cells_digest"]
    assert first["defaults_digest"] != changed_defaults["defaults_digest"]
    assert (
        first["keyword_defaults_digest"]
        != changed_defaults["keyword_defaults_digest"]
    )

    authority = engine._build_profile_authority(profile, ROOT)
    tampered = copy.deepcopy(authority)
    tampered["profile_semantics"]["semantic_contract"]["evidence_marker"] = "forged"
    semantic_unsigned = copy.deepcopy(tampered["profile_semantics"])
    semantic_unsigned.pop("content_digest")
    tampered["profile_semantics"]["content_digest"] = canonical_digest(
        semantic_unsigned
    )
    unsigned = copy.deepcopy(tampered)
    unsigned.pop("content_digest")
    tampered["content_digest"] = canonical_digest(unsigned)
    with pytest.raises(ContractError, match="semantic-contract digest mismatch"):
        engine._validate_authority_shape(tampered)


def test_profile_authority_rejects_rehashed_role_and_dependency_tampering() -> None:
    authority = engine._build_profile_authority(_toy_profile(), ROOT)

    relabelled = copy.deepcopy(authority)
    callable_authority = relabelled["profile_semantics"]["callables"][
        "validate_core"
    ]
    callable_authority["role"] = "validate_evidence"
    callable_unsigned = copy.deepcopy(callable_authority)
    callable_unsigned.pop("identity_digest")
    callable_authority["identity_digest"] = canonical_digest(callable_unsigned)
    semantic_unsigned = copy.deepcopy(relabelled["profile_semantics"])
    semantic_unsigned.pop("content_digest")
    relabelled["profile_semantics"]["content_digest"] = canonical_digest(
        semantic_unsigned
    )
    authority_unsigned = copy.deepcopy(relabelled)
    authority_unsigned.pop("content_digest")
    relabelled["content_digest"] = canonical_digest(authority_unsigned)
    with pytest.raises(ContractError, match="callable authority role differs"):
        engine._validate_authority_shape(relabelled)

    dependency_tamper = copy.deepcopy(authority)
    dependency_tamper["entries"][0]["byte_size"] += 1
    dependency_unsigned = copy.deepcopy(dependency_tamper)
    dependency_unsigned.pop("content_digest")
    dependency_tamper["content_digest"] = canonical_digest(dependency_unsigned)
    with pytest.raises(ContractError, match="dependency authority digest mismatch"):
        engine._validate_authority_shape(dependency_tamper)


def test_profile_authority_distinguishes_closure_state_and_fails_on_opaque_defaults() -> None:
    profile = _toy_profile()

    def callback_with(bound_value: str):
        def callback(
            _locators: Mapping[str, Any], _authority_root: Path
        ) -> Mapping[str, Any]:
            return {"status": "passed", "bound_value": bound_value}

        return callback

    first = engine._build_profile_authority(
        replace(profile, validate_core=callback_with("first")), ROOT
    )
    second = engine._build_profile_authority(
        replace(profile, validate_core=callback_with("second")), ROOT
    )
    assert first["profile_semantics"]["semantic_contract"] == second[
        "profile_semantics"
    ]["semantic_contract"]
    assert first["content_digest"] != second["content_digest"]

    opaque = object()

    def callback_with_opaque_default(
        _locators: Mapping[str, Any],
        _authority_root: Path,
        policy: object = opaque,
    ) -> Mapping[str, Any]:
        return {"status": "passed", "policy": str(policy)}

    with pytest.raises(ContractError, match="cannot canonically bind object"):
        engine._build_profile_authority(
            replace(profile, validate_core=callback_with_opaque_default), ROOT
        )


def test_v1_index_migrates_without_reauthorizing_legacy(tmp_path: Path) -> None:
    publication = tmp_path / "publication"
    profile = _toy_profile()
    source_a = _toy_source(tmp_path / "a", "a")
    source_b = _toy_source(tmp_path / "b", "b")
    publish_profile_current(source=source_a, profile=profile, publication_root=publication)
    _, selected = _snapshot(publication)
    current = selected["current"]
    legacy_evidence = publication / "evidence" / current["bundle_id"]
    shutil.copytree(publication / current["evidence_path"], legacy_evidence)
    legacy_row = {
        key: current[key]
        for key in (
            "bundle_id",
            "bundle_path",
            "bundle_manifest_digest",
            "evidence_manifest_digest",
            "target_id",
            "run_id",
            "cycle_id",
            "commit_id",
            "published_utc",
        )
    }
    legacy_row["evidence_path"] = f"evidence/{current['bundle_id']}"
    v1: dict[str, Any] = {
        "schema_version": "1.0.0",
        "index_kind": "canonical_discovery_publication_index",
        "current": legacy_row,
        "history": [],
        "legacy_archives": [],
        "authority_boundary": "historical non-current publication",
    }
    v1["index_digest"] = canonical_digest(v1)
    (publication / engine.INDEX_NAME).write_bytes(_encoded(v1))
    migrated = publish_profile_current(
        source=source_b, profile=profile, publication_root=publication
    )
    assert migrated["legacy_publication_count"] == 1
    _, snapshot = _snapshot(publication)
    assert snapshot["legacy_publications"] == [legacy_row]


def test_legacy_row_rejects_rehashed_id_without_manifest_content_suffix(
    tmp_path: Path,
) -> None:
    publication = tmp_path / "publication"
    result = publish_profile_current(
        source=_toy_source(tmp_path / "source", "a"),
        profile=_toy_profile(),
        publication_root=publication,
    )
    _, snapshot = _snapshot(publication)
    current = snapshot["current"]
    forged_id = f"toy-{'0' * 64}"

    forged_bundle = publication / "publications" / forged_id
    shutil.copytree(publication / current["bundle_path"], forged_bundle)
    bundle_manifest_path = forged_bundle / engine.BUNDLE_MANIFEST
    bundle_manifest = json.loads(bundle_manifest_path.read_text(encoding="utf-8"))
    bundle_manifest["content_id"] = forged_id
    bundle_manifest_path.write_bytes(_encoded(bundle_manifest))

    forged_evidence = publication / "evidence" / forged_id
    shutil.copytree(publication / current["evidence_path"], forged_evidence)
    evidence_manifest_path = forged_evidence / engine.EVIDENCE_MANIFEST
    evidence_manifest = json.loads(evidence_manifest_path.read_text(encoding="utf-8"))
    evidence_manifest["metadata"]["bundle_id"] = forged_id
    evidence_manifest_path.write_bytes(_encoded(evidence_manifest))

    forged_row = {
        **current,
        "bundle_id": forged_id,
        "bundle_path": f"publications/{forged_id}",
        "evidence_path": f"evidence/{forged_id}",
        "bundle_manifest_digest": bytes_digest(bundle_manifest_path.read_bytes()),
        "evidence_manifest_digest": bytes_digest(evidence_manifest_path.read_bytes()),
    }
    assert result["bundle_id"] != forged_id
    with pytest.raises(ContractError, match="legacy publication row is not exactly bound"):
        engine._validate_legacy_publication(forged_row, publication)


def test_two_process_publishers_serialize_to_valid_current_and_history(
    tmp_path: Path,
) -> None:
    context = multiprocessing.get_context("fork")
    source_a = _toy_source(tmp_path / "a", "a")
    source_b = _toy_source(tmp_path / "b", "b")
    publication = tmp_path / "publication"
    queue = context.Queue()
    processes = [
        context.Process(
            target=_publish_worker,
            args=(source, str(publication), marker, queue),
        )
        for source, marker in ((source_a, "a"), (source_b, "b"))
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join(30)
        assert process.exitcode == 0
    results = [queue.get(timeout=5) for _ in processes]
    assert all(row[0] == "ok" for row in results), results
    _, snapshot = _snapshot(publication)
    selected = next(
        row
        for row in results
        if (row[2], row[3])
        == (
            snapshot["current"]["bundle_id"],
            snapshot["current"]["evidence_id"],
        )
    )
    validated = validate_profile_current(
        publication_root=publication,
        profile=_toy_profile(evidence_marker=selected[1]),
    )
    assert validated["status"] == "passed"
    assert validated["profile_authority_digest"] == selected[4]
    wrong_marker = next(row[1] for row in results if row[1] != selected[1])
    with pytest.raises(ContractError, match="profile authority has drifted"):
        validate_profile_current(
            publication_root=publication,
            profile=_toy_profile(evidence_marker=wrong_marker),
        )
    identities = {
        (snapshot["current"]["bundle_id"], snapshot["current"]["evidence_id"]),
        *[(row["bundle_id"], row["evidence_id"]) for row in snapshot["history"]],
    }
    assert identities == {(row[2], row[3]) for row in results}


@pytest.fixture(scope="module")
def dwf_published(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = tmp_path_factory.mktemp("canonical-dwf-publication")
    module = runpy.run_path(
        str(Path(__file__).with_name("test_canonical_discovery_acceptance.py"))
    )
    candidate = module["_paths"](root / "candidate", live=True)
    publication = root / "publication"
    plan = plan_publication(**candidate, publication_root=publication)
    result = publish_current(**candidate, publication_root=publication)
    return {"candidate": candidate, "publication": publication, "plan": plan, "result": result}


@pytest.mark.skip(
    reason="User-deferred: real DWF fixture requires a current descendant-v3 lineage; "
    "its experiment operator is retired. See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_real_dwf_plan_publish_evidence_is_stable_and_logically_portable(
    dwf_published: dict[str, Any],
) -> None:
    assert dwf_published["plan"]["bundle_id"] == dwf_published["result"]["bundle_id"]
    assert dwf_published["plan"]["evidence_id"] == dwf_published["result"]["evidence_id"]
    result = validate_current_publication(
        publication_root=dwf_published["publication"]
    )
    assert result["status"] == "passed"
    evidence_root = (
        dwf_published["publication"] / "evidence" / result["evidence_id"]
    )
    combined = b"".join(
        path.read_bytes() for path in evidence_root.iterdir() if path.is_file()
    )
    assert str(dwf_published["publication"]).encode() not in combined
    assert b'"canonical_cycle_path": "cycle-result.json"' in (
        evidence_root / "reachability-report.json"
    ).read_bytes()
