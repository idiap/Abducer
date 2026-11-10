# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for the generic content-graph transaction kernel."""

from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any, Mapping, Sequence

import pytest

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_json,
)
from agentic.experiments import content_graph_transactions as transactions
from agentic.experiments.content_graph_transactions import (
    ContentGraphTransactionResult,
    PreparedContentGraphTransaction,
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
    reopen_content_graph_transaction,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    build_committed_object_handle,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    CompareAndSwapError,
    DiscoveryTransactionStore,
    IdempotencyConflict,
    InjectedFailure,
    StateCorruptionError,
)


TARGET_ID = "content-transaction-target"
RUN_ID = "content-transaction-run"
PROGRAMME_ID = "content-transaction-programme"
BRANCH_ID = "root"


def _state(
    generation: int,
    *,
    target_id: str = TARGET_ID,
    run_id: str = RUN_ID,
    marker: str = "generic-storage-fixture",
) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "run_id": run_id,
        "generation": generation,
        "programme_id": PROGRAMME_ID,
        "marker": marker,
    }


def _namespace(
    expected_generation: int,
    *,
    target_id: str = TARGET_ID,
    run_id: str = RUN_ID,
    branch_id: str = BRANCH_ID,
) -> Namespace:
    return Namespace(target_id, run_id, branch_id, expected_generation)


def _graph_path(generation: int, *, branch_id: str = BRANCH_ID) -> str:
    return f"branches/{branch_id}/content-graphs/g{generation}/graph.json"


def _object_path(
    generation: int, name: str, *, branch_id: str = BRANCH_ID
) -> str:
    return f"branches/{branch_id}/content-graphs/g{generation}/objects/{name}.json"


def _object(
    generation: int,
    name: str,
    *,
    value: Mapping[str, Any] | None = None,
    object_kind: str = "world_request",
    branch_id: str = BRANCH_ID,
) -> PreparedContentObject:
    return prepare_content_object(
        object_kind=object_kind,
        value=(
            {"fixture": name, "generation": generation}
            if value is None
            else value
        ),
        path=_object_path(generation, name, branch_id=branch_id),
    )


def _graph(
    *,
    local_objects: Sequence[PreparedContentObject],
    imported_handles: Sequence[Mapping[str, Any]] = (),
    ordered_roots: Sequence[str] | None = None,
    edges: Sequence[Mapping[str, Any]] = (),
    topological_order: Sequence[str] | None = None,
) -> dict[str, Any]:
    local_ids = [row.ref["object_id"] for row in local_objects]
    imported_ids = [row["object_ref"]["object_id"] for row in imported_handles]
    order = (
        [*imported_ids, *local_ids]
        if topological_order is None
        else list(topological_order)
    )
    roots = local_ids if ordered_roots is None else list(ordered_roots)
    return build_content_object_graph(
        local_descriptors=[row.descriptor for row in local_objects],
        imported_handles=imported_handles,
        ordered_roots=roots,
        edges=edges,
        topological_order=order,
    )


def _proposal(
    generation: int,
    *,
    local_objects: Sequence[PreparedContentObject] | None = None,
    graph: Mapping[str, Any] | None = None,
    marker: str = "generic-storage-fixture",
    branch_id: str = BRANCH_ID,
) -> tuple[PreparedContentGraphTransaction, dict[str, Any], tuple[PreparedContentObject, ...]]:
    objects = tuple(local_objects or (_object(generation, "root", branch_id=branch_id),))
    graph_value = _graph(local_objects=objects) if graph is None else copy.deepcopy(dict(graph))
    prepared = prepare_content_graph_transaction(
        expected_generation=generation - 1,
        state=_state(generation, marker=marker),
        namespace=_namespace(generation - 1, branch_id=branch_id),
        graph_artifact_path=_graph_path(generation, branch_id=branch_id),
        graph=graph_value,
        local_objects=objects,
    )
    return prepared, graph_value, objects


def _store(root: Path) -> DiscoveryTransactionStore:
    return DiscoveryTransactionStore(root, target_id=TARGET_ID, run_id=RUN_ID)


def _manual_artifacts(
    prepared: PreparedContentGraphTransaction,
    *,
    omit_local: bool = False,
    extra: bool = False,
    replace_first_local: bytes | None = None,
) -> list[CommitArtifact]:
    rows = [
        CommitArtifact(
            prepared.graph_artifact_path,
            canonical_json(prepared.graph),
            prepared.namespace,
        )
    ]
    if not omit_local:
        for index, local in enumerate(prepared.local_objects):
            data = (
                replace_first_local
                if index == 0 and replace_first_local is not None
                else local.data
            )
            rows.append(
                CommitArtifact(local.descriptor["path"], data, prepared.namespace)
            )
    if extra:
        rows.append(
            CommitArtifact(
                f"branches/{prepared.namespace.branch_id}/content-graphs/extra.json",
                canonical_json({"unexpected": True}),
                prepared.namespace,
            )
        )
    return rows


def _commit(
    store: DiscoveryTransactionStore,
    generation: int,
    **proposal_kwargs: Any,
) -> tuple[ContentGraphTransactionResult, PreparedContentGraphTransaction, tuple[PreparedContentObject, ...]]:
    prepared, _graph_value, objects = _proposal(generation, **proposal_kwargs)
    result = commit_content_graph_transaction(store=store, transaction=prepared)
    return result, prepared, objects


def test_atomic_commit_reopens_exact_graph_objects_and_compact_references(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    first = _object(1, "first")
    second = _object(1, "second")
    prepared, graph, _objects = _proposal(
        1,
        local_objects=[first, second],
        graph=_graph(local_objects=[first, second]),
    )

    result = commit_content_graph_transaction(store=store, transaction=prepared)
    reopened = reopen_content_graph_transaction(
        store=store,
        generation=1,
        graph_artifact_path=_graph_path(1),
    )
    commit = store.read_verified_commit(1)

    assert result == reopened
    assert commit.manifest["request_digest"] == prepared.request_digest
    assert commit.manifest["idempotency_key"] == prepared.idempotency_key
    assert [row["path"] for row in commit.manifest["artifacts"]] == [
        _graph_path(1),
        first.descriptor["path"],
        second.descriptor["path"],
    ]
    assert result.commit_ref["reference_kind"] == (
        "portable_verified_content_graph_commit"
    )
    assert result.graph_ref == {
        "schema_version": "1.0.0",
        "reference_kind": "committed_content_object_graph",
        "generation": 1,
        "graph_digest": graph["graph_digest"],
        "commit_reference_digest": result.commit_ref["reference_digest"],
        "graph_artifact": result.commit_ref["graph_artifact"],
        "object_count": 2,
        "local_object_count": 2,
        "imported_object_count": 0,
        "ordered_root_object_ids": [
            first.ref["object_id"],
            second.ref["object_id"],
        ],
    }
    assert result.root_refs == (first.ref, second.ref)
    assert "value" not in result.as_dict()
    assert "local_descriptors" not in result.graph_ref


def test_preparation_is_canonical_and_independent_of_input_object_order() -> None:
    first = _object(1, "first")
    second = _object(1, "second")
    graph = _graph(local_objects=[first, second])
    left = prepare_content_graph_transaction(
        expected_generation=0,
        state=_state(1),
        namespace=_namespace(0),
        graph_artifact_path=_graph_path(1),
        graph=graph,
        local_objects=[first, second],
    )
    right = prepare_content_graph_transaction(
        expected_generation=0,
        state={
            "marker": "generic-storage-fixture",
            "programme_id": PROGRAMME_ID,
            "generation": 1,
            "run_id": RUN_ID,
            "target_id": TARGET_ID,
        },
        namespace=_namespace(0),
        graph_artifact_path=_graph_path(1),
        graph=copy.deepcopy(graph),
        local_objects=[second, first],
    )
    assert left == right
    assert left.request_digest == right.request_digest
    assert left.idempotency_key == right.idempotency_key


@pytest.mark.parametrize(
    "case",
    [
        "namespace_generation",
        "state_generation",
        "state_target",
        "branch_path",
    ],
)
def test_wrong_namespace_state_generation_or_branch_path_is_rejected(
    case: str,
) -> None:
    local = _object(1, "root")
    namespace = _namespace(1 if case == "namespace_generation" else 0)
    state = _state(2 if case == "state_generation" else 1)
    if case == "state_target":
        state["target_id"] = "different-target"
    graph_path = (
        "branches/sibling/content-graphs/g1/graph.json"
        if case == "branch_path"
        else _graph_path(1)
    )
    with pytest.raises(ContractError):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=state,
            namespace=namespace,
            graph_artifact_path=graph_path,
            graph=_graph(local_objects=[local]),
            local_objects=[local],
        )


def test_prepared_transaction_cannot_commit_to_another_store_namespace(
    tmp_path: Path,
) -> None:
    prepared, _graph_value, _objects = _proposal(1)
    other = DiscoveryTransactionStore(
        tmp_path / "other", target_id="other-target", run_id=RUN_ID
    )
    with pytest.raises(ContractError, match="different store"):
        commit_content_graph_transaction(store=other, transaction=prepared)
    assert other.current_generation() == 0


@pytest.mark.parametrize("duplicate", ["object_id", "path"])
def test_duplicate_local_object_id_or_path_is_rejected(duplicate: str) -> None:
    first = _object(1, "first", value={"same": True})
    if duplicate == "object_id":
        second = prepare_content_object(
            object_kind=first.ref["object_kind"],
            value=first.value,
            path=_object_path(1, "second"),
        )
    else:
        second = prepare_content_object(
            object_kind="world_request",
            value={"different": True},
            path=first.descriptor["path"],
        )
    expected_message = "object IDs" if duplicate == "object_id" else "paths"
    with pytest.raises(ContractError, match=expected_message):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=_graph(local_objects=[first]),
            local_objects=[first, second],
        )


@pytest.mark.parametrize("mismatch", ["missing", "extra"])
def test_graph_and_supplied_local_objects_must_match_exactly(mismatch: str) -> None:
    first = _object(1, "first")
    second = _object(1, "second")
    graph_objects = [first, second] if mismatch == "missing" else [first]
    supplied = [first] if mismatch == "missing" else [first, second]
    with pytest.raises(ContractError, match=mismatch if mismatch == "missing" else "undeclared"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=_graph(local_objects=graph_objects),
            local_objects=supplied,
        )


def test_graph_artifact_cannot_alias_a_local_object_path() -> None:
    local = _object(1, "root")
    with pytest.raises(ContractError, match="collides"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=local.descriptor["path"],
            graph=_graph(local_objects=[local]),
            local_objects=[local],
        )


def test_stale_compare_and_swap_proposal_is_rejected(tmp_path: Path) -> None:
    store = _store(tmp_path / "store")
    stale, _graph_value, _objects = _proposal(1, marker="stale")
    current, _other_graph, _other_objects = _proposal(1, marker="winner")
    commit_content_graph_transaction(store=store, transaction=current)
    with pytest.raises(CompareAndSwapError):
        commit_content_graph_transaction(store=store, transaction=stale)
    assert store.current_generation() == 1


def test_same_idempotency_key_with_different_frozen_artifacts_conflicts(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    prepared, _graph_value, _objects = _proposal(1)
    store.commit(
        expected_generation=0,
        state=prepared.state,
        artifacts=_manual_artifacts(
            prepared,
            replace_first_local=canonical_json({"forged": "different bytes"}),
        ),
        idempotency_key=prepared.idempotency_key,
        request_digest=prepared.request_digest,
    )
    with pytest.raises(IdempotencyConflict, match="artifact_vector"):
        commit_content_graph_transaction(store=store, transaction=prepared)
    assert store.current_generation() == 1


def test_previsible_partial_failure_leaves_no_mixed_commit_and_exact_retry_wins(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    prepared, _graph_value, _objects = _proposal(1)
    with pytest.raises(InjectedFailure, match="after_artifact_write:1"):
        commit_content_graph_transaction(
            store=store,
            transaction=prepared,
            failpoint="after_artifact_write:1",
        )
    assert store.current_generation() == 0

    result = commit_content_graph_transaction(store=store, transaction=prepared)
    assert result.generation == 1
    commit = store.read_verified_commit(1)
    assert set(row["path"] for row in commit.manifest["artifacts"]) == {
        _graph_path(1),
        prepared.local_objects[0].descriptor["path"],
    }


def test_visible_first_wins_retry_is_byte_identical_and_creates_one_commit(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    prepared, _graph_value, _objects = _proposal(1)
    with pytest.raises(InjectedFailure, match="after_commit_rename"):
        commit_content_graph_transaction(
            store=store,
            transaction=prepared,
            failpoint="after_commit_rename",
        )

    first_retry = commit_content_graph_transaction(store=store, transaction=prepared)
    second_retry = commit_content_graph_transaction(store=store, transaction=prepared)
    assert first_retry == second_retry
    assert canonical_json(first_retry.as_dict()) == canonical_json(
        second_retry.as_dict()
    )
    assert store.current_generation() == 1
    assert len(list(store.commits_dir.iterdir())) == 1


def test_failpoint_callbacks_are_not_an_extension_surface(tmp_path: Path) -> None:
    store = _store(tmp_path / "store")
    prepared, _graph_value, _objects = _proposal(1)
    with pytest.raises(ContractError, match="not a callback"):
        commit_content_graph_transaction(
            store=store,
            transaction=prepared,
            failpoint=lambda _name: None,  # type: ignore[arg-type]
        )
    assert store.current_generation() == 0


def test_returned_commit_graph_and_root_references_are_defensive(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    result, _prepared, objects = _commit(store, 1)
    expected = result.as_dict()

    commit_ref = result.commit_ref
    graph_ref = result.graph_ref
    root_refs = result.root_refs
    projection = result.as_dict()
    commit_ref["graph_artifact"]["path"] = "branches/root/forged.json"
    graph_ref["ordered_root_object_ids"].clear()
    root_refs[0]["sha256"] = "sha256:" + "0" * 64
    projection["commit_reference"]["commit_id"] = "commit.forged"
    projection["root_references"].clear()

    assert result.as_dict() == expected
    assert result.root_refs == (objects[0].ref,)
    assert all("value" not in ref and "data" not in ref for ref in result.root_refs)


def test_relocation_reopens_byte_identical_reference_receipt(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    destination_root = tmp_path / "relocated"
    source_store = _store(source_root)
    result, _prepared, _objects = _commit(source_store, 1)
    shutil.copytree(source_root, destination_root)

    relocated_store = _store(destination_root)
    relocated = reopen_content_graph_transaction(
        store=relocated_store,
        generation=1,
        graph_artifact_path=_graph_path(1),
    )
    assert relocated == result
    assert canonical_json(relocated.as_dict()) == canonical_json(result.as_dict())


@pytest.mark.parametrize("artifact_attack", ["missing", "extra"])
def test_reopen_rejects_missing_or_extra_committed_artifact(
    tmp_path: Path,
    artifact_attack: str,
) -> None:
    store = _store(tmp_path / artifact_attack)
    prepared, _graph_value, _objects = _proposal(1)
    store.commit(
        expected_generation=0,
        state=prepared.state,
        artifacts=_manual_artifacts(
            prepared,
            omit_local=artifact_attack == "missing",
            extra=artifact_attack == "extra",
        ),
        idempotency_key=prepared.idempotency_key,
        request_digest=prepared.request_digest,
    )
    with pytest.raises(StateCorruptionError, match="exactly one graph"):
        reopen_content_graph_transaction(
            store=store,
            generation=1,
            graph_artifact_path=_graph_path(1),
        )


def test_historical_generation_is_stale_and_old_proposal_cannot_reopen(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    first_result, first_prepared, _objects = _commit(store, 1)
    _second_result, _second_prepared, _second_objects = _commit(store, 2)

    with pytest.raises(ContractError, match="stale or not current"):
        reopen_content_graph_transaction(
            store=store,
            generation=first_result.generation,
            graph_artifact_path=_graph_path(1),
        )
    with pytest.raises(CompareAndSwapError, match="stale"):
        commit_content_graph_transaction(store=store, transaction=first_prepared)


def test_direct_prior_owner_import_succeeds_but_transitive_reexport_fails(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    source = _object(
        1,
        "source",
        object_kind="world_matrix_commission",
        value={"fixture": "prior-owned-content"},
    )
    first_prepared, _first_graph, _ = _proposal(1, local_objects=[source])
    first = commit_content_graph_transaction(store=store, transaction=first_prepared)

    direct_handle = build_committed_object_handle(
        source_commit_reference=first.commit_ref,
        object_ref=source.ref,
    )
    second_root = _object(2, "second-root")
    direct_edge = {
        "source_object_id": source.ref["object_id"],
        "target_object_id": second_root.ref["object_id"],
        "edge_kind": "content_dependency",
    }
    second_graph = _graph(
        local_objects=[second_root],
        imported_handles=[direct_handle],
        ordered_roots=[second_root.ref["object_id"]],
        edges=[direct_edge],
        topological_order=[source.ref["object_id"], second_root.ref["object_id"]],
    )
    second_prepared, _graph_value, _ = _proposal(
        2, local_objects=[second_root], graph=second_graph
    )
    second = commit_content_graph_transaction(store=store, transaction=second_prepared)
    assert second.graph_ref["imported_object_count"] == 1

    laundering_handle = build_committed_object_handle(
        source_commit_reference=second.commit_ref,
        object_ref=source.ref,
    )
    third_root = _object(3, "third-root")
    laundering_edge = {
        "source_object_id": source.ref["object_id"],
        "target_object_id": third_root.ref["object_id"],
        "edge_kind": "content_dependency",
    }
    third_graph = _graph(
        local_objects=[third_root],
        imported_handles=[laundering_handle],
        ordered_roots=[third_root.ref["object_id"]],
        edges=[laundering_edge],
        topological_order=[source.ref["object_id"], third_root.ref["object_id"]],
    )
    third_prepared, _graph_value, _ = _proposal(
        3, local_objects=[third_root], graph=third_graph
    )
    with pytest.raises(ContractError, match="transitive re-export"):
        commit_content_graph_transaction(store=store, transaction=third_prepared)
    assert store.current_generation() == 2


def test_wrong_exact_source_commit_reference_fails_before_publication(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path / "store")
    source = _object(1, "source")
    first_prepared, _graph_value, _ = _proposal(1, local_objects=[source])
    first = commit_content_graph_transaction(store=store, transaction=first_prepared)
    forged_reference = copy.deepcopy(first.commit_ref)
    forged_reference["commit_id"] = "commit." + "0" * 24
    # Keep the outer handle schema-valid enough to reach exact replay by also
    # recomputing its self digest.
    forged_reference["reference_digest"] = transactions.canonical_digest(
        {
            key: value
            for key, value in forged_reference.items()
            if key != "reference_digest"
        }
    )
    handle = build_committed_object_handle(
        source_commit_reference=forged_reference,
        object_ref=source.ref,
    )
    root = _object(2, "root")
    graph = _graph(
        local_objects=[root],
        imported_handles=[handle],
        ordered_roots=[root.ref["object_id"]],
        edges=[
            {
                "source_object_id": source.ref["object_id"],
                "target_object_id": root.ref["object_id"],
                "edge_kind": "content_dependency",
            }
        ],
        topological_order=[source.ref["object_id"], root.ref["object_id"]],
    )
    prepared, _graph_value, _ = _proposal(2, local_objects=[root], graph=graph)
    with pytest.raises(ContractError, match="not exact"):
        commit_content_graph_transaction(store=store, transaction=prepared)
    assert store.current_generation() == 1


def test_fixed_object_byte_ceiling_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = _object(1, "root")
    monkeypatch.setattr(
        transactions,
        "MAX_CONTENT_GRAPH_TRANSACTION_OBJECT_BYTES",
        len(local.data) - 1,
    )
    with pytest.raises(ContractError, match="object-byte ceiling"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=_graph(local_objects=[local]),
            local_objects=[local],
        )


def test_fixed_graph_byte_ceiling_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = _object(1, "root")
    graph = _graph(local_objects=[local])
    monkeypatch.setattr(
        transactions,
        "MAX_CONTENT_GRAPH_TRANSACTION_GRAPH_BYTES",
        len(canonical_json(graph)) - 1,
    )
    with pytest.raises(ContractError, match="graph-byte ceiling"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=graph,
            local_objects=[local],
        )


def test_fixed_total_commit_byte_ceiling_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = _object(1, "root")
    graph = _graph(local_objects=[local])
    exact_size = len(canonical_json(_state(1))) + len(canonical_json(graph)) + len(
        local.data
    )
    monkeypatch.setattr(
        transactions,
        "MAX_CONTENT_GRAPH_TRANSACTION_COMMIT_BYTES",
        exact_size - 1,
    )
    with pytest.raises(ContractError, match="total commit-byte ceiling"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=graph,
            local_objects=[local],
        )


def test_fixed_object_count_ceiling_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = _object(1, "root")
    monkeypatch.setattr(transactions, "MAX_CONTENT_GRAPH_TRANSACTION_OBJECTS", 0)
    with pytest.raises(ContractError, match="object-count ceiling"):
        prepare_content_graph_transaction(
            expected_generation=0,
            state=_state(1),
            namespace=_namespace(0),
            graph_artifact_path=_graph_path(1),
            graph=_graph(local_objects=[local]),
            local_objects=[local],
        )
