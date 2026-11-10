# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial acceptance tests for compact causal byte materialization v3.

The tests prove exact local staging, copying, retry, and dependency replay.  No
assertion treats the materializer as a semantic producer or grants theoretical,
experimental, external, or physics authority.
"""

from __future__ import annotations

import copy
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

import agentic.experiments.causal_producer_runtime_v3 as materializer_v3
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_payload,
)
from agentic.experiments.causal_producer_runtime_v3 import (
    BINDING_SCHEMA,
    CausalArtifactMaterializerRuntimeV3,
    LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY,
    VerifiedCausalMaterializationSnapshotV3,
    build_causal_materializer_dependency_authority_v3,
    revalidate_causal_materialization_snapshot_v3,
    snapshot_sealed_causal_materialization_v3,
    validate_causal_materializer_binding_v3,
)
from agentic.scripts.causal_materializer_io_v3 import MAX_ARTIFACT_BYTES


def _runtime(root: Path) -> CausalArtifactMaterializerRuntimeV3:
    return CausalArtifactMaterializerRuntimeV3(
        workspace=root,
        namespace=Namespace("causal-v3-target", "causal-v3-run", "causal-v3-branch", 3),
    )


def _seal(runtime: CausalArtifactMaterializerRuntimeV3):
    return runtime.seal(
        stage_id="causal-v3-stage",
        materializer_role="exact-byte-materializer",
        artifact_id="causal-v3-artifact",
        artifact={
            "schema_version": "1.0.0",
            "payload": "UNIQUE-STAGED-CONTENT-MUST-NOT-ENTER-BINDING",
            "ordinal": 7,
        },
    )


def _reseal_binding(binding: dict[str, object]) -> dict[str, object]:
    core = {
        key: value
        for key, value in binding.items()
        if key not in {"binding_id", "binding_digest"}
    }
    digest = canonical_digest(core)
    binding["binding_digest"] = digest
    binding["binding_id"] = stable_identifier("causal-materializer-binding-v3", digest)
    return binding


def test_compact_binding_references_staged_input_without_embedding_value(
    tmp_path: Path,
) -> None:
    sealed = _seal(_runtime(tmp_path))
    binding_bytes = canonical_json(sealed.binding)
    request_bytes = canonical_json(sealed.request)

    assert sealed.request["input_artifacts"] == [sealed.binding["staged_input_ref"]]
    assert sealed.request["parameters"]["semantic_authorship"] is False
    assert sealed.binding["semantic_authorship"] is False
    assert sealed.binding["authority_boundary"] == LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY
    for forbidden in (b'"artifact_value"', b'"bytes_base64"', b"UNIQUE-STAGED-CONTENT"):
        assert forbidden not in binding_bytes
        assert forbidden not in request_bytes

    refs = [
        sealed.binding["staged_input_ref"],
        sealed.binding["output_ref"],
        sealed.binding["history_ref"],
        sealed.binding["request_ref"],
        sealed.binding["successful_receipt_ref"],
        sealed.binding["clock_ref"],
    ]
    assert len({ref["path"] for ref in refs}) == len(refs)
    staged = tmp_path / sealed.binding["staged_input_ref"]["path"]
    output = tmp_path / sealed.binding["output_ref"]["path"]
    history = tmp_path / sealed.binding["history_ref"]["path"]
    assert staged.read_bytes() == output.read_bytes() == history.read_bytes()
    assert validate_causal_materializer_binding_v3(
        sealed.binding, workspace=tmp_path
    ) == sealed.binding


def test_successful_retry_reuses_first_request_attempt_clock_and_binding(
    tmp_path: Path,
) -> None:
    runtime = _runtime(tmp_path)
    first = _seal(runtime)
    second = _seal(runtime)

    assert second.request == first.request
    assert second.successful_receipt == first.successful_receipt
    assert second.binding == first.binding
    assert second.binding_path == first.binding_path
    assert second.receipt_paths == first.receipt_paths
    assert len(second.receipt_paths) == 1


def test_failed_attempt_is_durable_and_retry_is_contiguous(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _runtime(tmp_path)
    original = runtime._run_command
    fail_once = True

    def injected(command: tuple[str, ...], payload: bytes):
        nonlocal fail_once
        if fail_once and tuple(command) == runtime.worker_command:
            fail_once = False
            return subprocess.CompletedProcess(command, 2, b"", b"forced first failure")
        return original(command, payload)

    monkeypatch.setattr(runtime, "_run_command", injected)
    with pytest.raises(ContractError, match="attempt 1 failed"):
        _seal(runtime)
    sealed = _seal(runtime)

    assert [path.name for path in sealed.receipt_paths] == [
        "attempt-1.json",
        "attempt-2.json",
    ]
    assert sealed.binding["successful_attempt"] == 2
    assert len(sealed.binding["attempt_receipt_refs"]) == 2
    assert sealed.successful_receipt["attempt"] == 2


def test_same_intent_concurrency_has_one_first_wins_success(tmp_path: Path) -> None:
    runtime = _runtime(tmp_path)
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(lambda _index: _seal(runtime), range(5)))

    assert len({row.request["request_id"] for row in rows}) == 1
    assert len({row.successful_receipt["receipt_id"] for row in rows}) == 1
    assert len({row.binding["binding_id"] for row in rows}) == 1
    assert all(len(row.receipt_paths) == 1 for row in rows)


@pytest.mark.parametrize("attack", ["symlink", "hardlink", "fifo"])
def test_staged_input_rejects_links_and_special_files(
    tmp_path: Path,
    attack: str,
) -> None:
    runtime = _runtime(tmp_path)
    sealed = _seal(runtime)
    victim = tmp_path / sealed.binding["staged_input_ref"]["path"]
    original = victim.read_bytes()
    victim.unlink()
    outside = tmp_path / "outside.json"
    outside.write_bytes(original)
    if attack == "symlink":
        victim.symlink_to(outside)
    elif attack == "hardlink":
        os.link(outside, victim)
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("FIFO creation unavailable")
        os.mkfifo(victim)
    with pytest.raises(ContractError):
        _seal(runtime)


def test_fixed_artifact_ceiling_rejects_before_staging(tmp_path: Path) -> None:
    runtime = _runtime(tmp_path)
    with pytest.raises(ContractError, match="byte ceiling"):
        runtime.seal(
            stage_id="oversized-stage",
            materializer_role="exact-byte-materializer",
            artifact_id="oversized-artifact",
            artifact={"payload": "x" * MAX_ARTIFACT_BYTES},
        )
    assert not (tmp_path / ".canonical-causal-evidence-v3").exists()


def test_dependency_authority_is_transitive_explicit_and_drift_checked(
    tmp_path: Path,
) -> None:
    authority = build_causal_materializer_dependency_authority_v3()
    paths = {entry["path"] for entry in authority["entries"]}
    assert {
        "agentic/scripts/run_causal_materializer_v3.py",
        "agentic/scripts/validate_causal_materializer_v3.py",
        "agentic/scripts/causal_materializer_io_v3.py",
        "agentic/spec/dynamic_experiment_causal_materializer_binding_v3.schema.json",
        "agentic/spec/dynamic_experiment_causal_materializer_receipt_v3.schema.json",
        "agentic/spec/dynamic_experiment_causal_materializer_clock_v3.schema.json",
    }.issubset(paths)

    sealed = _seal(_runtime(tmp_path))
    forged = copy.deepcopy(sealed.binding)
    forged["dependency_authority"]["entries"][0]["content_digest"] = (
        "sha256:" + "0" * 64
    )
    forged["dependency_authority"]["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged["dependency_authority"].items()
            if key != "content_digest"
        }
    )
    _reseal_binding(forged)
    with pytest.raises(Exception, match="dependency authority"):
        validate_causal_materializer_binding_v3(forged, workspace=tmp_path)


def test_ref_or_attempt_reordering_and_schema_extension_fail_closed(
    tmp_path: Path,
) -> None:
    runtime = _runtime(tmp_path)
    original = runtime._run_command
    failed = True

    def injected(command: tuple[str, ...], payload: bytes):
        nonlocal failed
        if failed and tuple(command) == runtime.worker_command:
            failed = False
            return subprocess.CompletedProcess(command, 2, b"", b"forced")
        return original(command, payload)

    runtime._run_command = injected  # type: ignore[method-assign]
    with pytest.raises(ContractError):
        _seal(runtime)
    sealed = _seal(runtime)

    reordered = copy.deepcopy(sealed.binding)
    reordered["attempt_receipt_refs"].reverse()
    _reseal_binding(reordered)
    with pytest.raises(ContractError):
        validate_causal_materializer_binding_v3(reordered, workspace=tmp_path)

    extended = copy.deepcopy(sealed.binding)
    extended["unexpected"] = True
    _reseal_binding(extended)
    with pytest.raises(ContractError):
        validate_payload(extended, BINDING_SCHEMA)


def test_staged_or_output_mutation_breaks_replay(tmp_path: Path) -> None:
    sealed = _seal(_runtime(tmp_path))
    for field in ("staged_input_ref", "output_ref", "history_ref"):
        path = tmp_path / sealed.binding[field]["path"]
        original = path.read_bytes()
        path.write_bytes(b'{"mutated":true}')
        with pytest.raises(ContractError):
            validate_causal_materializer_binding_v3(sealed.binding, workspace=tmp_path)
        path.write_bytes(original)


def test_snapshot_reads_each_unique_ref_once_and_deduplicates_success_alias(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sealed = _seal(_runtime(tmp_path))
    ref_reads: list[str] = []
    binding_reads: list[str] = []
    original_read_ref = materializer_v3.read_ref
    original_safe_read = materializer_v3.safe_read

    def counted_read_ref(
        workspace: Path,
        ref: dict[str, object],
        *,
        max_bytes: int,
    ) -> bytes:
        ref_reads.append(str(ref["path"]))
        return original_read_ref(workspace, ref, max_bytes=max_bytes)

    def counted_safe_read(
        workspace: Path,
        relative_path: str,
        **kwargs: object,
    ) -> bytes:
        binding_reads.append(relative_path)
        return original_safe_read(workspace, relative_path, **kwargs)

    monkeypatch.setattr(materializer_v3, "read_ref", counted_read_ref)
    monkeypatch.setattr(materializer_v3, "safe_read", counted_safe_read)
    snapshot = snapshot_sealed_causal_materialization_v3(
        sealed,
        workspace=tmp_path,
    )

    all_ref_paths = [
        sealed.binding["staged_input_ref"]["path"],
        sealed.binding["request_ref"]["path"],
        *[
            ref["path"] for ref in sealed.binding["attempt_receipt_refs"]
        ],
        sealed.binding["successful_receipt_ref"]["path"],
        sealed.binding["output_ref"]["path"],
        sealed.binding["history_ref"]["path"],
        sealed.binding["clock_ref"]["path"],
    ]
    expected_unique = tuple(dict.fromkeys(all_ref_paths))
    assert isinstance(snapshot, VerifiedCausalMaterializationSnapshotV3)
    assert snapshot.captured_ref_paths == expected_unique
    assert ref_reads == list(expected_unique)
    assert ref_reads.count(sealed.binding["successful_receipt_ref"]["path"]) == 1
    assert len(binding_reads) == 1
    assert snapshot.successful_receipt_bytes is snapshot.attempt_receipt_bytes[-1]
    assert snapshot.binding == sealed.binding
    assert snapshot.request == sealed.request
    assert snapshot.successful_receipt == sealed.successful_receipt


@pytest.mark.parametrize("attack", ["mutation", "symlink", "hardlink", "fifo"])
def test_snapshot_rejects_mid_capture_leaf_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    attack: str,
) -> None:
    if attack == "fifo" and not hasattr(os, "mkfifo"):
        pytest.skip("FIFO creation unavailable")
    sealed = _seal(_runtime(tmp_path))
    target = tmp_path / sealed.binding["output_ref"]["path"]
    original_target = target.read_bytes()
    outside = tmp_path / f"mid-snapshot-{attack}.json"
    outside.write_bytes(original_target)
    original_read_ref = materializer_v3.read_ref
    attacked = False

    def attacking_read_ref(
        workspace: Path,
        ref: dict[str, object],
        *,
        max_bytes: int,
    ) -> bytes:
        nonlocal attacked
        data = original_read_ref(workspace, ref, max_bytes=max_bytes)
        if not attacked:
            attacked = True
            target.unlink()
            if attack == "mutation":
                target.write_bytes(b'{"mutated":true}')
            elif attack == "symlink":
                target.symlink_to(outside)
            elif attack == "hardlink":
                os.link(outside, target)
            else:
                os.mkfifo(target)
        return data

    monkeypatch.setattr(materializer_v3, "read_ref", attacking_read_ref)
    started = time.monotonic()
    with pytest.raises(ContractError):
        snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)
    assert time.monotonic() - started < 2.0


def test_captured_map_validation_survives_source_deletion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sealed = _seal(_runtime(tmp_path))
    original_validator = materializer_v3._validate_captured_materialization_v3
    validation_entered = False

    def deleting_validator(**kwargs: object):
        nonlocal validation_entered
        validation_entered = True
        captured = kwargs["captured"]
        assert isinstance(captured, dict)
        for relative_path in tuple(captured):
            (tmp_path / relative_path).unlink()
        sealed.binding_path.unlink()
        return original_validator(**kwargs)

    monkeypatch.setattr(
        materializer_v3,
        "_validate_captured_materialization_v3",
        deleting_validator,
    )
    snapshot = snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)

    assert validation_entered is True
    assert snapshot.binding == sealed.binding
    assert snapshot.staged_input == snapshot.output == snapshot.history
    assert snapshot.successful_receipt["status"] == "succeeded"


def test_snapshot_is_defensive_and_independent_after_source_mutation_or_deletion(
    tmp_path: Path,
) -> None:
    sealed = _seal(_runtime(tmp_path))
    snapshot = snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)
    expected_binding = snapshot.binding
    expected_request = snapshot.request
    expected_receipts = snapshot.attempt_receipts
    expected_artifact = snapshot.staged_input
    expected_clock = snapshot.clock
    expected_digest = snapshot.snapshot_digest
    replayed = snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)
    assert replayed.snapshot_digest == expected_digest
    assert replayed.binding_bytes == snapshot.binding_bytes

    first, *remaining = snapshot.captured_ref_paths
    (tmp_path / first).write_bytes(b'{"post_snapshot_mutation":true}')
    for relative_path in remaining:
        (tmp_path / relative_path).unlink()
    sealed.binding_path.unlink()

    returned_binding = snapshot.binding
    returned_binding["identity"]["target_id"] = "caller-mutation"
    returned_request = snapshot.request
    returned_request["parameters"]["semantic_authorship"] = True
    returned_receipts = snapshot.attempt_receipts
    returned_receipts[-1]["status"] = "failed"
    with pytest.raises(FrozenInstanceError):
        snapshot.snapshot_digest = "sha256:" + "0" * 64  # type: ignore[misc]

    assert snapshot.binding == expected_binding
    assert snapshot.request == expected_request
    assert snapshot.attempt_receipts == expected_receipts
    assert snapshot.staged_input == snapshot.output == snapshot.history == expected_artifact
    assert snapshot.clock == expected_clock
    assert snapshot.snapshot_digest == expected_digest
    assert snapshot.binding["semantic_authorship"] is False
    assert snapshot.successful_receipt["semantic_authorship"] is False


def test_public_detached_snapshot_replay_is_exact_and_workspace_independent(
    tmp_path: Path,
) -> None:
    """Adapters consume one public pure boundary, not private capture helpers."""

    sealed = _seal(_runtime(tmp_path))
    snapshot = snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)
    for relative_path in snapshot.captured_ref_paths:
        (tmp_path / relative_path).unlink()
    sealed.binding_path.unlink()

    replayed = revalidate_causal_materialization_snapshot_v3(snapshot)
    assert replayed == snapshot
    assert replayed is not snapshot
    assert replayed.binding["semantic_authorship"] is False
    assert replayed.successful_receipt["semantic_authorship"] is False
    assert replayed.captured_ref_paths == snapshot.captured_ref_paths

    with pytest.raises(ContractError, match="exact verified v3 type"):
        revalidate_causal_materialization_snapshot_v3(  # type: ignore[arg-type]
            object()
        )
    with pytest.raises(ContractError, match="pure causal replay"):
        revalidate_causal_materialization_snapshot_v3(
            replace(snapshot, snapshot_digest="sha256:" + "0" * 64)
        )
    with pytest.raises(ContractError):
        revalidate_causal_materialization_snapshot_v3(
            replace(snapshot, output_bytes=b'{"forged":true}')
        )


def test_snapshot_rejects_nonexact_seal_and_cross_binding_substitution(
    tmp_path: Path,
) -> None:
    runtime = _runtime(tmp_path)
    first = _seal(runtime)
    second = runtime.seal(
        stage_id="causal-v3-other-stage",
        materializer_role="exact-byte-materializer",
        artifact_id="causal-v3-other-artifact",
        artifact={"schema_version": "1.0.0", "payload": "other", "ordinal": 8},
    )

    with pytest.raises(ContractError, match="exact v3 seal type"):
        snapshot_sealed_causal_materialization_v3(
            object(),  # type: ignore[arg-type]
            workspace=tmp_path,
        )
    with pytest.raises(ContractError, match="paths differ"):
        snapshot_sealed_causal_materialization_v3(
            replace(first, binding_path=second.binding_path),
            workspace=tmp_path,
        )
    with pytest.raises(ContractError, match="cross binding"):
        snapshot_sealed_causal_materialization_v3(
            replace(first, request=second.request),
            workspace=tmp_path,
        )
    with pytest.raises(ContractError, match="cross binding"):
        snapshot_sealed_causal_materialization_v3(
            replace(first, successful_receipt=second.successful_receipt),
            workspace=tmp_path,
        )

    forged = copy.deepcopy(first.binding)
    forged["request_ref"] = copy.deepcopy(second.binding["request_ref"])
    _reseal_binding(forged)
    with pytest.raises(ContractError, match="request-to-binding"):
        validate_causal_materializer_binding_v3(forged, workspace=tmp_path)


def test_snapshot_type_is_not_a_semantic_authority(tmp_path: Path) -> None:
    sealed = _seal(_runtime(tmp_path))
    snapshot = snapshot_sealed_causal_materialization_v3(sealed, workspace=tmp_path)

    assert snapshot.binding["semantic_authorship"] is False
    assert snapshot.request["parameters"]["semantic_authorship"] is False
    assert all(
        receipt["semantic_authorship"] is False
        for receipt in snapshot.attempt_receipts
    )
    assert snapshot.binding["authority_boundary"] == LOCAL_MATERIALIZER_AUTHORITY_BOUNDARY
