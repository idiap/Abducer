# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Crash, concurrency, isolation, and idempotency tests for discovery commits."""

from __future__ import annotations

import json
import multiprocessing
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, Namespace, canonical_digest
from agentic.state.discovery_transaction import (
    CommitArtifact,
    CompareAndSwapError,
    ConcurrentRunError,
    DiscoveryTransactionStore,
    IdempotencyConflict,
    InjectedFailure,
    StateCorruptionError,
    VerifiedArtifactContext,
    VerifiedArtifactContextError,
    VerifiedCommit,
)


def _state(generation: int, *, note: str = "state") -> dict:
    return {
        "schema_version": "1.0.0",
        "target_id": "target-a",
        "run_id": "run-a",
        "generation": generation,
        "note": note,
    }


def _artifact(generation: int = 0, *, branch: str = "branch-a", content: bytes = b'{"delta":1}\n') -> CommitArtifact:
    return CommitArtifact(
        f"branches/{branch}/deltas/result.json",
        content,
        Namespace("target-a", "run-a", branch, generation),
    )


def _hold_lock(root: str, ready, release) -> None:
    store = DiscoveryTransactionStore(Path(root), target_id="target-a", run_id="run-a")
    with store.lock():
        ready.set()
        release.wait(10)


def _race_commit(root: str, note: str, queue) -> None:
    store = DiscoveryTransactionStore(Path(root), target_id="target-a", run_id="run-a")
    try:
        result = store.commit(
            expected_generation=0,
            state=_state(1, note=note),
            artifacts=[_artifact(content=note.encode())],
            idempotency_key=f"key-{note}",
            request_digest=canonical_digest(note),
        )
        queue.put(("committed", result.generation))
    except CompareAndSwapError:
        queue.put(("stale", None))


def _commit_for_integrity_attack(store: DiscoveryTransactionStore):
    """Create one ordinary commit whose durable files an attack can replace."""

    return store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[_artifact()],
        idempotency_key="integrity-attack",
        request_digest=canonical_digest("integrity-attack"),
    )


def test_atomic_commit_is_verified_readable_and_idempotent(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    request_digest = canonical_digest({"cycle": 1})
    result = store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[_artifact()],
        idempotency_key="cycle-1",
        request_digest=request_digest,
    )
    assert result.generation == 1
    assert store.current_generation() == 1
    assert store.read_state() == _state(1)
    repeated = store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[_artifact()],
        idempotency_key="cycle-1",
        request_digest=request_digest,
    )
    assert repeated.idempotent is True
    assert repeated.commit_id == result.commit_id
    assert len(list(store.commits_dir.iterdir())) == 1


def test_verified_commit_reopens_latest_and_historical_identity(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    first = store.commit(
        expected_generation=0,
        state=_state(1, note="first"),
        artifacts=[_artifact()],
        idempotency_key="verified-generation-1",
        request_digest=canonical_digest("verified-generation-1"),
    )
    second = store.commit(
        expected_generation=1,
        state=_state(2, note="second"),
        artifacts=[_artifact(1, content=b'{"delta":2}\n')],
        idempotency_key="verified-generation-2",
        request_digest=canonical_digest("verified-generation-2"),
    )

    latest = store.read_verified_commit()
    historical = store.read_verified_commit(1)

    assert isinstance(latest, VerifiedCommit)
    assert (latest.generation, latest.prior_generation) == (2, 1)
    assert latest.commit_id == second.commit_id
    assert latest.commit_path == second.commit_path
    assert latest.manifest_digest == second.manifest_digest
    assert latest.state == _state(2, note="second")
    assert latest.state_file_digest == latest.manifest["state_digest"]
    assert latest.state_semantic_digest == latest.manifest["state_semantic_digest"]
    assert latest.state_semantic_digest == canonical_digest(latest.state)

    assert (historical.generation, historical.prior_generation) == (1, 0)
    assert historical.commit_id == first.commit_id
    assert historical.commit_path == first.commit_path
    assert historical.manifest_digest == first.manifest_digest
    assert historical.state == _state(1, note="first")

    # Returned mappings are defensive copies, not mutable store authority.
    latest.state["note"] = "caller mutation"
    latest.manifest["commit_id"] = "caller mutation"
    assert store.read_verified_commit(2).state == _state(2, note="second")
    assert store.read_verified_commit(2).commit_id == second.commit_id


@pytest.mark.parametrize("generation", [None, 0, -1, True])
def test_verified_commit_rejects_absent_or_non_commit_generation(
    tmp_path: Path, generation: int | None
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    with pytest.raises(ContractError, match="positive integer"):
        store.read_verified_commit(generation)


def test_verified_commit_rejects_unknown_positive_generation(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[],
        idempotency_key="known-generation",
        request_digest=canonical_digest("known-generation"),
    )
    with pytest.raises(ContractError, match="unknown generation: 2"):
        store.read_verified_commit(2)


def test_verified_commit_ignores_and_repairs_forged_pointer(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    result = store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[],
        idempotency_key="pointer-independent",
        request_digest=canonical_digest("pointer-independent"),
    )
    store.pointer_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "target_id": "target-a",
                "run_id": "run-a",
                "generation": 999,
                "commit_id": "forged",
                "commit_directory": "forged",
                "manifest_digest": canonical_digest("forged"),
            }
        ),
        encoding="utf-8",
    )

    reopened = store.read_verified_commit()
    repaired = json.loads(store.pointer_path.read_text(encoding="utf-8"))

    assert reopened.commit_id == result.commit_id
    assert reopened.generation == 1
    assert repaired["commit_id"] == result.commit_id
    assert repaired["generation"] == 1


def test_verified_commit_reopens_after_store_root_relocation(tmp_path: Path) -> None:
    source_root = tmp_path / "source-root"
    moved_root = tmp_path / "moved-root"
    store = DiscoveryTransactionStore(source_root, target_id="target-a", run_id="run-a")
    result = store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[_artifact()],
        idempotency_key="relocatable-generation",
        request_digest=canonical_digest("relocatable-generation"),
    )
    source_root.rename(moved_root)

    reopened = DiscoveryTransactionStore(
        moved_root, target_id="target-a", run_id="run-a"
    ).read_verified_commit(1)

    assert reopened.commit_id == result.commit_id
    assert reopened.manifest_digest == result.manifest_digest
    assert reopened.commit_path.is_relative_to(moved_root.resolve())
    assert reopened.state == _state(1)
    assert str(source_root.resolve()) not in json.dumps(reopened.manifest)


def test_verified_artifact_batch_returns_exact_bytes_from_one_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    first = _artifact(content=b'{"delta":1}\n')
    second = _artifact(branch="branch-b", content=b'{"delta":2}\n')
    committed = store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[first, second],
        idempotency_key="verified-artifact-batch",
        request_digest=canonical_digest("verified-artifact-batch"),
    )
    artifact_reads: list[str] = []
    original_snapshot = store._snapshot_regular_at  # noqa: SLF001

    def count_artifact_snapshot(parent_fd: int, name: str, *, label: str) -> bytes:
        if label.startswith("commit artifact "):
            artifact_reads.append(label)
        return original_snapshot(parent_fd, name, label=label)

    monkeypatch.setattr(store, "_snapshot_regular_at", count_artifact_snapshot)
    verified, artifacts = store.read_verified_artifacts(
        1,
        [
            "branches/branch-b/deltas/result.json",
            "branches/branch-a/deltas/result.json",
        ],
    )

    assert verified.commit_id == committed.commit_id
    assert verified.manifest_digest == committed.manifest_digest
    assert list(artifacts) == [
        "branches/branch-b/deltas/result.json",
        "branches/branch-a/deltas/result.json",
    ]
    assert artifacts == {
        "branches/branch-b/deltas/result.json": b'{"delta":2}\n',
        "branches/branch-a/deltas/result.json": b'{"delta":1}\n',
    }
    assert len(artifact_reads) == 2
    assert len(set(artifact_reads)) == 2
    with pytest.raises(TypeError):
        artifacts["branches/branch-a/deltas/result.json"][0] = 0  # type: ignore[index]


def test_verified_artifact_context_is_store_minted_bound_and_immutable(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)
    same_namespace_store = DiscoveryTransactionStore(
        tmp_path, target_id="target-a", run_id="run-a"
    )

    with pytest.raises(VerifiedArtifactContextError):
        VerifiedArtifactContext(store=store)
    forged = object.__new__(VerifiedArtifactContext)
    with pytest.raises(VerifiedArtifactContextError):
        forged.assert_owned_by(store)

    with store.verified_artifact_context() as context:
        context.assert_owned_by(store)
        with pytest.raises(VerifiedArtifactContextError):
            context.assert_owned_by(same_namespace_store)
        with pytest.raises(AttributeError):
            context.target_id = "target-forged"  # type: ignore[misc]
        with pytest.raises(AttributeError):
            context._snapshots = ()  # type: ignore[attr-defined]

        first = context.read_commit(1)
        first.manifest["target_id"] = "target-forged"  # type: ignore[index]
        first.state["note"] = "mutated"  # type: ignore[index]
        second = context.read_commit(1)
        assert second.manifest["target_id"] == "target-a"
        assert second.state == _state(1)

    with pytest.raises(VerifiedArtifactContextError):
        context.read_commit(1)


def test_verified_artifact_context_rejects_copied_lease_and_slot_mutation(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)
    same_namespace_store = DiscoveryTransactionStore(
        tmp_path, target_id="target-a", run_id="run-a"
    )

    with store.verified_artifact_context() as context:
        private_names = {
            "store": "_VerifiedArtifactContext__store",
            "target_id": "_VerifiedArtifactContext__target_id",
            "run_id": "_VerifiedArtifactContext__run_id",
            "snapshots": "_VerifiedArtifactContext__snapshots",
            "lease_id": "_VerifiedArtifactContext__lease_id",
        }
        original = {
            label: getattr(context, private_name)
            for label, private_name in private_names.items()
        }

        forged = object.__new__(VerifiedArtifactContext)
        for label, private_name in private_names.items():
            object.__setattr__(forged, private_name, original[label])
        with pytest.raises(
            VerifiedArtifactContextError,
            match="binding is forged or mutated",
        ):
            forged.read_commit(1)

        attacks = (
            ("store", same_namespace_store),
            ("target_id", "target-forged"),
            ("run_id", "run-forged"),
            ("snapshots", tuple([*original["snapshots"]])),
            ("lease_id", "0" * 32),
        )
        for label, replacement in attacks:
            private_name = private_names[label]
            object.__setattr__(context, private_name, replacement)
            try:
                with pytest.raises(VerifiedArtifactContextError):
                    context.read_commit(1)
            finally:
                object.__setattr__(context, private_name, original[label])
            assert context.read_commit(1).generation == 1


def test_verified_artifact_context_is_thread_owned_and_blocks_store_access(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)

    def cross_thread_context_read(context: VerifiedArtifactContext) -> str:
        try:
            context.read_commit(1)
        except VerifiedArtifactContextError as exc:
            return str(exc)
        return "unexpected-success"

    def cross_thread_store_read() -> str:
        try:
            store.current_generation()
        except VerifiedArtifactContextError as exc:
            return str(exc)
        return "unexpected-success"

    with store.verified_artifact_context() as context:
        with ThreadPoolExecutor(max_workers=2) as executor:
            context_result = executor.submit(cross_thread_context_read, context)
            store_result = executor.submit(cross_thread_store_read)
            assert "owning thread" in context_result.result(timeout=2)
            assert "nested store access" in store_result.result(timeout=2)
        assert context.read_commit(1).generation == 1

    assert store.current_generation() == 1


def test_verified_artifact_context_rejects_nested_store_lock_without_waiting(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)

    started = time.perf_counter()
    with store.verified_artifact_context():
        with pytest.raises(VerifiedArtifactContextError):
            store.current_generation()
    assert time.perf_counter() - started < 1.0


@pytest.mark.parametrize(
    ("paths", "message"),
    [
        (["branches/branch-a/deltas/missing.json"], "not manifest-covered"),
        (["../outside.json"], "unsafe artifact path"),
        (
            [
                "branches/branch-a/deltas/result.json",
                "branches/branch-a/deltas/result.json",
            ],
            "duplicate verified artifact path",
        ),
        (["branches/branch-a/deltas/./result.json"], "not canonical"),
    ],
)
def test_verified_artifact_batch_rejects_unsafe_or_uncovered_paths(
    tmp_path: Path,
    paths: list[str],
    message: str,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)

    with pytest.raises(ContractError, match=message):
        store.read_verified_artifacts(1, paths)


def test_verified_artifact_batch_rejects_unknown_generation_and_scalar_paths(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    _commit_for_integrity_attack(store)
    with pytest.raises(ContractError, match="unknown generation"):
        store.read_verified_artifacts(2, [])
    with pytest.raises(ContractError, match="sequence"):
        store.read_verified_artifacts(1, "branches/branch-a/deltas/result.json")  # type: ignore[arg-type]


def test_verified_artifact_batch_fails_closed_on_link_swap_during_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    committed = _commit_for_integrity_attack(store)
    artifact = committed.commit_path / "artifacts/branches/branch-a/deltas/result.json"
    outside = tmp_path / "raced-artifact"
    original_snapshot = store._snapshot_regular_at  # noqa: SLF001
    swapped = False

    def swap_after_snapshot(parent_fd: int, name: str, *, label: str) -> bytes:
        nonlocal swapped
        data = original_snapshot(parent_fd, name, label=label)
        if label.startswith("commit artifact ") and not swapped:
            artifact.rename(outside)
            artifact.symlink_to(outside)
            swapped = True
        return data

    monkeypatch.setattr(store, "_snapshot_regular_at", swap_after_snapshot)
    with pytest.raises(StateCorruptionError, match="substituted during artifact enumeration"):
        store.read_verified_artifacts(1, ["branches/branch-a/deltas/result.json"])

    assert outside.read_bytes() == b'{"delta":1}\n'


def test_two_concurrent_runners_cannot_commit_same_generation(tmp_path: Path) -> None:
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    processes = [context.Process(target=_race_commit, args=(str(tmp_path), note, queue)) for note in ("a", "b")]
    for process in processes:
        process.start()
    results = [queue.get(timeout=15) for _ in processes]
    for process in processes:
        process.join(timeout=15)
        assert process.exitcode == 0
    assert sorted(result[0] for result in results) == ["committed", "stale"]
    assert DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a").current_generation() == 1


def test_nonblocking_lock_proves_only_one_active_runner(tmp_path: Path) -> None:
    context = multiprocessing.get_context("spawn")
    ready, release = context.Event(), context.Event()
    process = context.Process(target=_hold_lock, args=(str(tmp_path), ready, release))
    process.start()
    assert ready.wait(10)
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    with pytest.raises(ConcurrentRunError):
        with store.lock(blocking=False):
            pass
    release.set()
    process.join(timeout=15)
    assert process.exitcode == 0


@pytest.mark.parametrize(
    ("failpoint", "expected_generation"),
    [
        ("after_state_write", 0),
        ("after_artifact_write:1", 0),
        ("after_manifest_write", 0),
        ("after_journal_prepared", 0),
        ("after_commit_rename", 1),
        ("after_pointer_write", 1),
        ("after_journal_complete", 1),
    ],
)
def test_failpoints_recover_prior_or_complete_next_never_mixed(
    tmp_path: Path, failpoint: str, expected_generation: int
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    with pytest.raises(InjectedFailure, match=failpoint):
        store.commit(
            expected_generation=0,
            state=_state(1),
            artifacts=[_artifact()],
            idempotency_key="crash-cycle",
            request_digest=canonical_digest("frozen"),
            failpoint=failpoint,
        )
    recovered = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    assert recovered.recover() == expected_generation
    assert recovered.read_state() == (_state(1) if expected_generation == 1 else None)
    assert not any(recovered.staging_dir.iterdir())


def test_signal_like_interruptions_release_lock_and_recover_deterministically(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path / "sigint", target_id="target-a", run_id="run-a")

    def sigint(name: str) -> None:
        if name == "after_journal_prepared":
            raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        store.commit(
            expected_generation=0, state=_state(1), artifacts=[_artifact()],
            idempotency_key="sigint", request_digest=canonical_digest("sigint"), failpoint=sigint,
        )
    assert store.recover() == 0
    with store.lock(blocking=False):
        pass

    terminated = DiscoveryTransactionStore(tmp_path / "sigterm", target_id="target-a", run_id="run-a")

    def sigterm(name: str) -> None:
        if name == "after_commit_rename":
            raise SystemExit(143)

    with pytest.raises(SystemExit):
        terminated.commit(
            expected_generation=0, state=_state(1), artifacts=[_artifact()],
            idempotency_key="sigterm", request_digest=canonical_digest("sigterm"), failpoint=sigterm,
        )
    assert terminated.recover() == 1
    assert terminated.read_state() == _state(1)


def test_retry_after_visible_crash_purchases_no_duplicate_commit(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    digest = canonical_digest("same inputs")
    with pytest.raises(InjectedFailure):
        store.commit(
            expected_generation=0, state=_state(1), artifacts=[_artifact()],
            idempotency_key="same-key", request_digest=digest, failpoint="after_commit_rename",
        )
    result = store.commit(
        expected_generation=0, state=_state(1), artifacts=[_artifact()],
        idempotency_key="same-key", request_digest=digest,
    )
    assert result.idempotent is True
    assert result.generation == 1
    assert len(list(store.commits_dir.iterdir())) == 1


def test_idempotency_key_cannot_be_reused_for_changed_frozen_inputs(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    store.commit(
        expected_generation=0, state=_state(1), artifacts=[_artifact()],
        idempotency_key="same-key", request_digest=canonical_digest("inputs-a"),
    )
    with pytest.raises(IdempotencyConflict):
        store.commit(
            expected_generation=1, state=_state(2), artifacts=[_artifact(1)],
            idempotency_key="same-key", request_digest=canonical_digest("inputs-b"),
        )


def test_idempotency_requires_exact_prior_state_and_artifact_vector(tmp_path: Path) -> None:
    """A key identifies one frozen transition, not merely a caller digest."""

    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    request_digest = canonical_digest("same-caller-digest")
    store.commit(
        expected_generation=0,
        state=_state(1),
        artifacts=[_artifact()],
        idempotency_key="exact-transition",
        request_digest=request_digest,
    )

    with pytest.raises(IdempotencyConflict, match="prior_generation"):
        store.commit(
            expected_generation=1,
            state=_state(2),
            artifacts=[_artifact(1)],
            idempotency_key="exact-transition",
            request_digest=request_digest,
        )
    with pytest.raises(IdempotencyConflict, match="state_(?:bytes|digest)"):
        store.commit(
            expected_generation=0,
            state=_state(1, note="changed-state"),
            artifacts=[_artifact()],
            idempotency_key="exact-transition",
            request_digest=request_digest,
        )
    with pytest.raises(IdempotencyConflict, match="artifact_vector"):
        store.commit(
            expected_generation=0,
            state=_state(1),
            artifacts=[_artifact(content=b'{"delta":2}\n')],
            idempotency_key="exact-transition",
            request_digest=request_digest,
        )
    with pytest.raises(IdempotencyConflict, match="artifact_vector"):
        store.commit(
            expected_generation=0,
            state=_state(1),
            artifacts=[_artifact(branch="branch-b")],
            idempotency_key="exact-transition",
            request_digest=request_digest,
        )


@pytest.mark.parametrize(
    "request_digest",
    [
        "sha256:",
        "sha256:" + "0" * 63,
        "sha256:" + "0" * 65,
        "sha256:" + "A" * 64,
        "sha512:" + "0" * 64,
    ],
)
def test_commit_rejects_every_noncanonical_sha256_digest(
    tmp_path: Path, request_digest: str
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    with pytest.raises(ContractError, match="invalid canonical digest"):
        store.commit(
            expected_generation=0,
            state=_state(1),
            artifacts=[_artifact()],
            idempotency_key="bad-digest",
            request_digest=request_digest,
        )
    assert store.current_generation() == 0


@pytest.mark.parametrize(
    "artifact",
    [
        CommitArtifact("branches/branch-a/result.json", b"x", Namespace("other-target", "run-a", "branch-a", 0)),
        CommitArtifact("branches/branch-a/result.json", b"x", Namespace("target-a", "other-run", "branch-a", 0)),
        CommitArtifact("branches/branch-a/result.json", b"x", Namespace("target-a", "run-a", "branch-a", 9)),
        CommitArtifact("branches/branch-b/result.json", b"x", Namespace("target-a", "run-a", "branch-a", 0)),
    ],
)
def test_stale_cross_target_run_state_or_sibling_artifact_is_rejected(
    tmp_path: Path, artifact: CommitArtifact
) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    with pytest.raises(ContractError):
        store.commit(
            expected_generation=0, state=_state(1), artifacts=[artifact],
            idempotency_key="bad-artifact", request_digest=canonical_digest("bad"),
        )


def test_workers_cannot_use_global_latest_paths(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    artifact = CommitArtifact(
        "branches/branch-a/latest.json", b"x", Namespace("target-a", "run-a", "branch-a", 0)
    )
    with pytest.raises(ContractError, match="latest"):
        store.commit(
            expected_generation=0, state=_state(1), artifacts=[artifact],
            idempotency_key="latest-path", request_digest=canonical_digest("bad"),
        )


def test_partial_worker_failure_preserves_valid_sibling_and_retries_only_failure(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    frozen = canonical_digest({"theory": "t1", "literature": "l1"})
    valid_path = store.store_branch_result(
        wave_id="wave-1", branch_id="branch-a", invocation_id="inv-a", frozen_inputs_digest=frozen,
        status="validated", payload={"theory_delta": "survives"},
    )
    failed_path = store.store_branch_result(
        wave_id="wave-1", branch_id="branch-b", invocation_id="inv-b", frozen_inputs_digest=frozen,
        status="failed", payload={"error": "worker crash"},
    )
    assert store.read_branch_result(valid_path, wave_id="wave-1", branch_id="branch-a", frozen_inputs_digest=frozen)["status"] == "validated"
    assert store.read_branch_result(failed_path, wave_id="wave-1", branch_id="branch-b", frozen_inputs_digest=frozen)["status"] == "failed"
    assert store.plan_retry(wave_id="wave-1", branch_ids=["branch-a", "branch-b"], frozen_inputs_digest=frozen) == ["branch-b"]
    changed = canonical_digest({"theory": "t2", "literature": "l1"})
    assert store.plan_retry(wave_id="wave-1", branch_ids=["branch-a", "branch-b"], frozen_inputs_digest=changed) == ["branch-a", "branch-b"]
    with pytest.raises(ContractError, match="sibling/global"):
        store.read_branch_result(valid_path, wave_id="wave-1", branch_id="branch-b", frozen_inputs_digest=frozen)


def test_monotonic_allocations_do_not_reuse_ids_after_artifact_changes(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    assert store.allocate_identity("cycle") == "cycle-000000000001"
    assert store.allocate_identity("invocation") == "invocation-000000000001"
    (store.run_root / "unrelated-file").write_text("does not affect allocation", encoding="utf-8")
    assert store.allocate_identity("cycle") == "cycle-000000000002"
    assert store.allocate_identity("invocation") == "invocation-000000000002"


def test_corrupt_pointer_is_quarantined_and_repaired_from_manifest(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    store.commit(
        expected_generation=0, state=_state(1), artifacts=[_artifact()],
        idempotency_key="pointer-test", request_digest=canonical_digest("pointer"),
    )
    store.pointer_path.write_text("{broken", encoding="utf-8")
    assert store.recover() == 1
    repaired = json.loads(store.pointer_path.read_text(encoding="utf-8"))
    assert repaired["generation"] == 1
    assert list(store.run_root.glob("state-pointer.corrupt.*.json"))


def test_immutable_commit_corruption_is_never_silently_repaired(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    result = store.commit(
        expected_generation=0, state=_state(1), artifacts=[_artifact()],
        idempotency_key="corrupt-test", request_digest=canonical_digest("corrupt"),
    )
    (result.commit_path / "state.json").write_text('{"tampered":true}\n', encoding="utf-8")
    with pytest.raises(StateCorruptionError, match="state digest"):
        store.recover()


def test_forged_journal_traversal_is_quarantined_without_touching_target(
    tmp_path: Path,
) -> None:
    """Journal text can never turn recovery into an arbitrary tree deletion."""

    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    victim = tmp_path / "victim"
    victim.mkdir()
    marker = victim / "must-survive.txt"
    marker.write_text("outside staging", encoding="utf-8")
    transaction_id = "commit." + "0" * 24
    forged = {
        "schema_version": "1.0.0",
        "transaction_id": transaction_id,
        "target_id": "target-a",
        "run_id": "run-a",
        "generation": 1,
        "stage_directory": "../../../../victim",
        "commit_directory": f"generation-000000000001-{transaction_id}",
        "manifest_digest": canonical_digest("forged-manifest"),
        "status": "prepared",
    }
    journal_path = store.journal_dir / f"{transaction_id}.json"
    journal_path.write_text(json.dumps(forged), encoding="utf-8")

    with pytest.raises(StateCorruptionError, match="invalid journal.*quarantined"):
        store.recover()

    assert marker.read_text(encoding="utf-8") == "outside staging"
    assert not journal_path.exists()
    assert list(store.journal_quarantine_dir.iterdir())


def test_linked_journal_stage_is_quarantined_without_following_target(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    with pytest.raises(InjectedFailure, match="after_journal_prepared"):
        store.commit(
            expected_generation=0,
            state=_state(1),
            artifacts=[_artifact()],
            idempotency_key="linked-stage",
            request_digest=canonical_digest("linked-stage"),
            failpoint="after_journal_prepared",
        )
    stage = next(store.staging_dir.iterdir())
    outside = tmp_path / "outside-stage-target"
    stage.rename(outside)
    marker = outside / "must-survive.txt"
    marker.write_text("do not follow", encoding="utf-8")
    stage.symlink_to(outside, target_is_directory=True)

    with pytest.raises(StateCorruptionError, match="unsafe staged transaction quarantined"):
        store.recover()

    assert marker.read_text(encoding="utf-8") == "do not follow"
    assert not any(store.staging_dir.iterdir())
    assert list(store.staging_quarantine_dir.iterdir())
    assert list(store.journal_quarantine_dir.iterdir())


@pytest.mark.parametrize("location", ["state", "manifest", "journal", "artifact"])
def test_commit_verification_rejects_symlinked_core_files(
    tmp_path: Path,
    location: str,
) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    result = _commit_for_integrity_attack(store)
    paths = {
        "state": result.commit_path / "state.json",
        "manifest": result.commit_path / "manifest.json",
        "journal": store.journal_dir / f"{result.commit_id}.json",
        "artifact": result.commit_path / "artifacts/branches/branch-a/deltas/result.json",
    }
    attacked = paths[location]
    target = tmp_path / f"{location}-symlink-target"
    attacked.rename(target)
    attacked.symlink_to(target)

    with pytest.raises(StateCorruptionError):
        store.recover()

    assert target.is_file()


@pytest.mark.parametrize("location", ["state", "manifest", "journal", "artifact"])
def test_commit_verification_rejects_special_core_files_without_blocking(
    tmp_path: Path,
    location: str,
) -> None:
    """A FIFO must be rejected from metadata; verification must never open-block."""

    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    result = _commit_for_integrity_attack(store)
    paths = {
        "state": result.commit_path / "state.json",
        "manifest": result.commit_path / "manifest.json",
        "journal": store.journal_dir / f"{result.commit_id}.json",
        "artifact": result.commit_path / "artifacts/branches/branch-a/deltas/result.json",
    }
    attacked = paths[location]
    attacked.unlink()
    os.mkfifo(attacked)

    with pytest.raises(StateCorruptionError):
        store.recover()


def test_artifact_intermediate_directory_symlink_is_never_traversed(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    result = _commit_for_integrity_attack(store)
    directory = result.commit_path / "artifacts/branches/branch-a/deltas"
    outside = tmp_path / "outside-artifact-directory"
    directory.rename(outside)
    directory.symlink_to(outside, target_is_directory=True)

    with pytest.raises(StateCorruptionError, match="link or special"):
        store.recover()

    assert (outside / "result.json").is_file()


def test_unmanifested_artifact_link_is_rejected_by_exact_enumeration(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    result = _commit_for_integrity_attack(store)
    outside = tmp_path / "unmanifested-target"
    outside.write_bytes(b"unmanifested")
    extra = result.commit_path / "artifacts/branches/branch-a/deltas/extra.json"
    extra.symlink_to(outside)

    with pytest.raises(StateCorruptionError, match="link or special"):
        store.recover()

    assert outside.read_bytes() == b"unmanifested"


def test_commit_discovery_rejects_directory_symlink(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    outside = tmp_path / "fake-commit-target"
    outside.mkdir()
    fake = store.commits_dir / "generation-000000000001-commit.000000000000000000000000"
    fake.symlink_to(outside, target_is_directory=True)

    with pytest.raises(StateCorruptionError, match="commit entry.*link or special"):
        store.recover()


def test_core_file_hard_link_count_is_rejected(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path / "store", target_id="target-a", run_id="run-a")
    result = _commit_for_integrity_attack(store)
    state_path = result.commit_path / "state.json"
    mirror = tmp_path / "state-hard-link"
    os.link(state_path, mirror)

    with pytest.raises(StateCorruptionError, match="one-link regular file"):
        store.recover()

    assert mirror.read_bytes() == state_path.read_bytes()


def test_rollback_creates_a_new_auditable_generation(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    store.commit(
        expected_generation=0, state=_state(1, note="good"), artifacts=[],
        idempotency_key="generation-1", request_digest=canonical_digest("one"),
    )
    store.commit(
        expected_generation=1, state=_state(2, note="bad"), artifacts=[],
        idempotency_key="generation-2", request_digest=canonical_digest("two"),
    )
    result = store.rollback(
        expected_generation=2, to_generation=1, reason="generation two failed semantic validation",
        idempotency_key="rollback-2-to-1",
    )
    state = store.read_state()
    assert result.generation == 3
    assert state["note"] == "good"
    assert state["rollback"]["restored_from_generation"] == 1
    assert store.current_generation() == 3
