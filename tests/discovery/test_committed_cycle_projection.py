# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for store-only committed-cycle authority derivation.

These tests deliberately start with the full receipt-backed canonical fixture.
They then prove that the experiment base is generation ``N`` even though every
source producer honestly remains in the cycle's ``N-1`` namespace.  Attacks are
performed on private root copies so a failed substitution cannot contaminate a
later replay check.
"""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery import (
    committed_cycle_projection_artifact_paths,
    derive_committed_cycle_world_authority_projection,
    load_committed_cycle_projection_sources,
    replay_committed_cycle_world_authority_projection,
    run_canonical_discovery_cycle,
)
from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.experiments.world_matrix_commits import build_verified_commit_identity
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    StateCorruptionError,
)
from tests.discovery.test_canonical_discovery_cycle import CanonicalExercise


def _components(projection: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["component_kind"]: copy.deepcopy(row["value"])
        for row in projection["components"]
    }


@pytest.fixture(scope="module")
def committed_cycle(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    """Commit one genuine active-current cycle with a theory-requested probe."""

    fixture_root = tmp_path_factory.mktemp("committed-cycle-projection")
    exercise = CanonicalExercise(
        fixture_root,
        live=True,
        experiment=False,
        commission_support=True,
    )
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    store = DiscoveryTransactionStore(
        exercise.state_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    return {
        "exercise": exercise,
        "result": result,
        "store": store,
        "generation": result["committed_state_version"],
    }


def _copied_store(
    committed_cycle: dict[str, Any], destination: Path
) -> DiscoveryTransactionStore:
    exercise: CanonicalExercise = committed_cycle["exercise"]
    shutil.copytree(exercise.state_root, destination)
    return DiscoveryTransactionStore(
        destination,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )


def test_real_cycle_derives_from_one_verified_batch_and_exact_commit(
    committed_cycle: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    store: DiscoveryTransactionStore = committed_cycle["store"]
    generation = committed_cycle["generation"]
    calls: list[tuple[int, tuple[str, ...]]] = []
    original = store.read_verified_artifacts

    def counted_read(
        selected_generation: int, relative_paths: Any
    ) -> tuple[Any, dict[str, bytes]]:
        calls.append((selected_generation, tuple(relative_paths)))
        return original(selected_generation, relative_paths)

    monkeypatch.setattr(store, "read_verified_artifacts", counted_read)
    projection = derive_committed_cycle_world_authority_projection(
        store,
        generation,
    )
    assert calls == [
        (generation, committed_cycle_projection_artifact_paths(generation))
    ]

    sources = load_committed_cycle_projection_sources(store, generation)
    commit = sources.verified_commit
    values = _components(projection)
    ancestor = values["committed_ancestor"]
    assert projection["prior_state_version"] == generation
    assert ancestor["source_cycle_prior_state_version"] == generation - 1
    assert ancestor["matrix_base_generation"] == generation
    assert ancestor["generation"] == generation
    assert ancestor["state"] == commit.state
    assert ancestor["state_semantic_digest"] == commit.state_semantic_digest
    assert ancestor["verified_commit_identity"] == build_verified_commit_identity(
        commit
    )
    assert values["reflection_packet"] == sources.finalized_reflection
    assert values["schedule"] == sources.schedule
    assert sources.canonical_cycle["conceptual_authority"] == values[
        "conceptual_systems"
    ]["conceptual_authority"]

    producer_receipts = [
        *values["source_authority"]["producer_receipts"],
        *values["generator_authority"]["generator_receipts"],
        *values["generator_authority"]["adjudicator_receipts"],
    ]
    assert producer_receipts
    assert all(
        receipt["identity"]["state_version"] == generation - 1
        for receipt in producer_receipts
    )
    assert replay_committed_cycle_world_authority_projection(
        projection,
        store,
        generation,
    ) == projection


def test_uncommitted_caller_bytes_cannot_enter_derivation(
    committed_cycle: dict[str, Any], tmp_path: Path
) -> None:
    store: DiscoveryTransactionStore = committed_cycle["store"]
    generation = committed_cycle["generation"]
    expected = derive_committed_cycle_world_authority_projection(store, generation)
    forged = copy.deepcopy(_components(expected)["reflection_packet"])
    forged["support_probe"]["theoretical_question"] = (
        "An uncommitted caller-authored replacement question."
    )
    caller_path = tmp_path / "caller-finalized-reflection.json"
    caller_path.write_text(json.dumps(forged), encoding="utf-8")

    # The public API has no reflection/path/state injection port.  The extra
    # keyword must fail at the Python boundary, and merely placing bytes beside
    # the run cannot affect a fresh committed derivation.
    with pytest.raises(TypeError):
        derive_committed_cycle_world_authority_projection(
            store,
            generation,
            finalized_reflection=forged,  # type: ignore[call-arg]
        )
    assert derive_committed_cycle_world_authority_projection(
        store,
        generation,
    ) == expected


def test_same_semantic_state_under_different_commit_identity_is_rejected(
    committed_cycle: dict[str, Any], tmp_path: Path
) -> None:
    exercise: CanonicalExercise = committed_cycle["exercise"]
    first_store: DiscoveryTransactionStore = committed_cycle["store"]
    generation = committed_cycle["generation"]
    second_root = tmp_path / "different-commit-root"
    kwargs = exercise.cycle_kwargs()
    kwargs.update(
        {
            "state_root": second_root,
            "idempotency_key": "canonical-cycle-different-commit",
        }
    )
    second_result = run_canonical_discovery_cycle(**kwargs)
    second_store = DiscoveryTransactionStore(
        second_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    first_commit = first_store.read_verified_commit(generation)
    second_commit = second_store.read_verified_commit(generation)
    assert first_commit.state == second_commit.state
    assert first_commit.state_semantic_digest == second_commit.state_semantic_digest
    assert first_commit.commit_id != second_commit.commit_id
    assert first_commit.manifest_digest != second_commit.manifest_digest
    assert second_result["committed_state_version"] == generation

    first_projection = derive_committed_cycle_world_authority_projection(
        first_store,
        generation,
    )
    second_projection = derive_committed_cycle_world_authority_projection(
        second_store,
        generation,
    )
    first_identity = _components(first_projection)["committed_ancestor"][
        "verified_commit_identity"
    ]
    second_identity = _components(second_projection)["committed_ancestor"][
        "verified_commit_identity"
    ]
    assert first_identity != second_identity
    with pytest.raises(ContractError, match="not the committed-cycle derivation"):
        replay_committed_cycle_world_authority_projection(
            first_projection,
            second_store,
            generation,
        )


def test_semantic_projection_copy_substitution_fails_before_derivation(
    committed_cycle: dict[str, Any], tmp_path: Path
) -> None:
    destination = tmp_path / "substituted-root"
    store = _copied_store(committed_cycle, destination)
    generation = committed_cycle["generation"]
    commit = store.read_verified_commit(generation)
    package_paths = committed_cycle_projection_artifact_paths(generation)
    high_risk_path = next(
        path for path in package_paths if "/semantic/high_risk_portfolio/" in path
    )
    parallel_path = next(
        path for path in package_paths if "/semantic/parallel_portfolio/" in path
    )
    artifact_root = commit.commit_path / "artifacts"
    (artifact_root / high_risk_path).write_bytes(
        (artifact_root / parallel_path).read_bytes()
    )

    with pytest.raises(StateCorruptionError, match="artifact digest mismatch"):
        derive_committed_cycle_world_authority_projection(store, generation)


def test_projection_replays_after_whole_root_relocation_and_original_deletion(
    committed_cycle: dict[str, Any], tmp_path: Path
) -> None:
    source_root = tmp_path / "private-original-root"
    source_store = _copied_store(committed_cycle, source_root)
    generation = committed_cycle["generation"]
    expected = derive_committed_cycle_world_authority_projection(
        source_store,
        generation,
    )
    relocated_root = tmp_path / "relocated-root"
    shutil.copytree(source_root, relocated_root)
    shutil.rmtree(source_root)
    assert not source_root.exists()

    exercise: CanonicalExercise = committed_cycle["exercise"]
    relocated_store = DiscoveryTransactionStore(
        relocated_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    observed = derive_committed_cycle_world_authority_projection(
        relocated_store,
        generation,
    )
    assert observed == expected
    assert canonical_digest(observed) == canonical_digest(expected)
    assert replay_committed_cycle_world_authority_projection(
        expected,
        relocated_store,
        generation,
    ) == expected
