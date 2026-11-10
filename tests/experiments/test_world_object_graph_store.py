# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Transaction-authority tests for content-addressed world-object graphs.

The portable graph tests exercise local DAG and filesystem behavior.  This file
tests the stronger causal boundary: graph bytes, object bytes, and imported
lineage must all come from one live ``VerifiedArtifactContext`` over exact
immutable commits.  The fixtures use small scientific placeholders because the
property under test is provenance, not experiment quality or physics content.
"""

from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import pytest

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    build_committed_object_handle,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.experiments.world_object_graph_store import (
    StoreVerifiedContentObjectGraph,
    build_content_graph_commit_reference,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedArtifactContextError,
    VerifiedCommit,
)


TARGET_ID = "content-graph-target"
RUN_ID = "content-graph-run"
PROGRAMME_ID = "content-graph-programme"
BRANCH_ID = "root"


def _state(generation: int) -> dict[str, Any]:
    return {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "generation": generation,
        "programme_id": PROGRAMME_ID,
        "theory_status": "storage-provenance-fixture-only",
    }


def _object_path(generation: int, name: str) -> str:
    return f"branches/root/content-graphs/g{generation}/objects/{name}.json"


def _graph_path(generation: int) -> str:
    return f"branches/root/content-graphs/g{generation}/graph.json"


def _prepared(
    generation: int,
    name: str,
    *,
    object_kind: str,
    value: Mapping[str, Any],
) -> PreparedContentObject:
    return prepare_content_object(
        object_kind=object_kind,
        value=value,
        path=_object_path(generation, name),
    )


def _commit_graph(
    store: DiscoveryTransactionStore,
    *,
    generation: int,
    local_objects: Sequence[PreparedContentObject],
    imported_handles: Sequence[Mapping[str, Any]],
    ordered_roots: Sequence[str],
    edges: Sequence[Mapping[str, Any]],
    topological_order: Sequence[str],
    graph_override: Mapping[str, Any] | None = None,
    extra_artifacts: Sequence[CommitArtifact] = (),
) -> tuple[VerifiedCommit, dict[str, Any]]:
    graph = (
        copy.deepcopy(dict(graph_override))
        if graph_override is not None
        else build_content_object_graph(
            local_descriptors=[row.descriptor for row in local_objects],
            imported_handles=imported_handles,
            ordered_roots=ordered_roots,
            edges=edges,
            topological_order=topological_order,
        )
    )
    namespace = Namespace(TARGET_ID, RUN_ID, BRANCH_ID, generation - 1)
    artifacts = [
        CommitArtifact(_graph_path(generation), canonical_json(graph), namespace),
        *(
            CommitArtifact(row.descriptor["path"], row.data, namespace)
            for row in local_objects
        ),
        *extra_artifacts,
    ]
    store.commit(
        expected_generation=generation - 1,
        state=_state(generation),
        artifacts=artifacts,
        idempotency_key=f"content-graph-generation-{generation}",
        request_digest=canonical_digest(
            {
                "generation": generation,
                "graph_digest": graph["graph_digest"],
                "extra_paths": [row.relative_path for row in extra_artifacts],
            }
        ),
    )
    return store.read_verified_commit(generation), graph


def _source_generation(
    store: DiscoveryTransactionStore,
) -> tuple[VerifiedCommit, dict[str, Any], PreparedContentObject]:
    source = _prepared(
        1,
        "shared-source",
        object_kind="world_matrix_commission",
        value={
            "kind": "shared-theory-and-literature-basis",
            "claim": "finite storage fixture; no physics authority",
        },
    )
    commit, graph = _commit_graph(
        store,
        generation=1,
        local_objects=[source],
        imported_handles=[],
        ordered_roots=[source.ref["object_id"]],
        edges=[],
        topological_order=[source.ref["object_id"]],
    )
    return commit, graph, source


def _reference(commit: VerifiedCommit, generation: int) -> dict[str, Any]:
    return build_content_graph_commit_reference(
        commit,
        programme_id=PROGRAMME_ID,
        graph_artifact_path=_graph_path(generation),
    )


def _refresh_reference_digest(reference: dict[str, Any]) -> None:
    """Rehash a forged reference so tests reach identity checks beyond self-hash."""

    reference["reference_digest"] = canonical_digest(
        {
            key: value
            for key, value in reference.items()
            if key != "reference_digest"
        }
    )


def _commit_import_generation(
    store: DiscoveryTransactionStore,
    *,
    source: PreparedContentObject,
    source_reference: Mapping[str, Any],
    generation: int = 2,
    handle_mutator: Callable[[dict[str, Any]], None] | None = None,
) -> tuple[VerifiedCommit, dict[str, Any], PreparedContentObject, dict[str, Any]]:
    handle = build_committed_object_handle(
        source_commit_reference=source_reference,
        object_ref=source.ref,
    )
    if handle_mutator is not None:
        handle_mutator(handle)
    root = _prepared(
        generation,
        "derived-root",
        object_kind="world_request",
        value={
            "kind": "derived-world-request",
            "source_object_id": handle["object_ref"]["object_id"],
        },
    )
    edge = {
        "source_object_id": handle["object_ref"]["object_id"],
        "target_object_id": root.ref["object_id"],
        "edge_kind": "request_dependency",
    }
    commit, graph = _commit_graph(
        store,
        generation=generation,
        local_objects=[root],
        imported_handles=[handle],
        ordered_roots=[root.ref["object_id"]],
        edges=[edge],
        topological_order=[handle["object_ref"]["object_id"], root.ref["object_id"]],
    )
    return commit, graph, root, handle


def _chain(root: Path) -> dict[str, Any]:
    store = DiscoveryTransactionStore(root, target_id=TARGET_ID, run_id=RUN_ID)
    source_commit, source_graph, source = _source_generation(store)
    current_commit, current_graph, current_root, handle = _commit_import_generation(
        store,
        source=source,
        source_reference=_reference(source_commit, 1),
    )
    return {
        "store": store,
        "source_commit": source_commit,
        "source_graph": source_graph,
        "source": source,
        "current_commit": current_commit,
        "current_graph": current_graph,
        "current_root": current_root,
        "handle": handle,
    }


def test_live_context_resolves_exact_prior_owner_and_returns_defensive_values(
    tmp_path: Path,
) -> None:
    chain = _chain(tmp_path / "store")
    store = chain["store"]
    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=2,
            graph_artifact_path=_graph_path(2),
        )
        closure = resolver.verify_closure()
        assert [row.ref["object_id"] for row in closure] == [
            chain["source"].ref["object_id"],
            chain["current_root"].ref["object_id"],
        ]
        first = resolver.resolve(chain["source"].ref["object_id"])
        first.value["claim"] = "caller forgery"
        first.ref["sha256"] = "sha256:" + "0" * 64
        second = resolver.resolve(chain["source"].ref["object_id"])
        assert second.value == chain["source"].value
        assert second.ref == chain["source"].ref
        graph_copy = resolver.graph
        graph_copy["ordered_roots"] = []
        assert resolver.graph["ordered_roots"] == [
            chain["current_root"].ref["object_id"]
        ]


def test_graph_commit_reference_has_no_transition_semantics(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    commit, _graph, _source = _source_generation(store)
    reference = _reference(commit, 1)
    assert reference["reference_kind"] == "portable_verified_content_graph_commit"
    assert reference["graph_artifact"]["artifact_kind"] == (
        "dynamic_experiment_content_object_graph"
    )
    assert reference["graph_artifact"]["path"] == _graph_path(1)
    assert "transition_kind" not in reference
    assert "transition_artifact" not in reference


@pytest.mark.parametrize(
    "field,value",
    [
        ("reference_kind", "portable_verified_discovery_commit"),
        ("artifact_kind", "world_matrix_aggregation"),
    ],
)
def test_graph_commit_reference_rejects_wrong_graph_kind(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / field, target_id=TARGET_ID, run_id=RUN_ID
    )
    commit, _graph, source = _source_generation(store)
    reference = _reference(commit, 1)
    if field == "reference_kind":
        reference[field] = value
    else:
        reference["graph_artifact"][field] = value
    _refresh_reference_digest(reference)
    with pytest.raises(ContractError):
        build_committed_object_handle(
            source_commit_reference=reference,
            object_ref=source.ref,
        )


@pytest.mark.parametrize(
    "attack",
    [
        "wrong_graph_path",
        "wrong_commit_identity",
        "wrong_reference_digest",
        "wrong_graph_digest",
    ],
)
def test_graph_commit_reference_runtime_rejects_wrong_path_identity_or_digest(
    tmp_path: Path,
    attack: str,
) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / attack, target_id=TARGET_ID, run_id=RUN_ID
    )
    source_commit, _graph, source = _source_generation(store)
    reference = _reference(source_commit, 1)
    if attack == "wrong_graph_path":
        object_descriptor = next(
            row
            for row in source_commit.manifest["artifacts"]
            if row["path"] == source.descriptor["path"]
        )
        reference["graph_artifact"].update(
            {
                "path": source.descriptor["path"],
                "sha256": object_descriptor["sha256"],
                "size_bytes": object_descriptor["size_bytes"],
            }
        )
        _refresh_reference_digest(reference)
    elif attack == "wrong_commit_identity":
        reference["commit_id"] = "commit.wrong-graph-owner"
        _refresh_reference_digest(reference)
    elif attack == "wrong_reference_digest":
        reference["reference_digest"] = "sha256:" + "0" * 64
    else:
        reference["graph_artifact"]["sha256"] = "sha256:" + "0" * 64
        _refresh_reference_digest(reference)

    _commit_import_generation(
        store,
        source=source,
        source_reference=reference,
    )
    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=2,
            graph_artifact_path=_graph_path(2),
        )
        with pytest.raises(StateCorruptionError):
            resolver.resolve_roots()


def test_legacy_fake_transition_reference_is_rejected(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    commit, _graph, source = _source_generation(store)
    graph_reference = _reference(commit, 1)
    graph_artifact = copy.deepcopy(graph_reference.pop("graph_artifact"))
    graph_artifact.pop("artifact_kind")
    graph_reference.update(
        {
            "reference_kind": "portable_verified_discovery_commit",
            "transition_kind": "theory_and_commission_anchor",
            "transition_artifact": graph_artifact,
        }
    )
    _refresh_reference_digest(graph_reference)
    with pytest.raises(ContractError):
        build_committed_object_handle(
            source_commit_reference=graph_reference,
            object_ref=source.ref,
        )


def test_resolver_rejects_stale_closed_and_cross_store_contexts(tmp_path: Path) -> None:
    chain = _chain(tmp_path / "store-a")
    store = chain["store"]
    other = DiscoveryTransactionStore(
        tmp_path / "store-b", target_id=TARGET_ID, run_id=RUN_ID
    )
    with store.verified_artifact_context() as context:
        with pytest.raises(ContractError, match="stale"):
            StoreVerifiedContentObjectGraph(
                store=store,
                context=context,
                generation=1,
                graph_artifact_path=_graph_path(1),
            )
        with pytest.raises(VerifiedArtifactContextError):
            StoreVerifiedContentObjectGraph(
                store=other,
                context=context,
                generation=2,
                graph_artifact_path=_graph_path(2),
            )
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=2,
            graph_artifact_path=_graph_path(2),
        )
    with pytest.raises(VerifiedArtifactContextError, match="closed"):
        resolver.resolve_roots()


@pytest.mark.parametrize("attack", ["wrong_commit", "missing_member", "not_prior"])
def test_import_handle_rejects_wrong_lineage_or_membership(
    tmp_path: Path,
    attack: str,
) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / attack, target_id=TARGET_ID, run_id=RUN_ID
    )
    source_commit, _graph, source = _source_generation(store)
    reference = _reference(source_commit, 1)

    def mutate(handle: dict[str, Any]) -> None:
        if attack == "wrong_commit":
            handle["source_commit_reference"]["commit_id"] = "commit.wrong-lineage"
            ref = handle["source_commit_reference"]
            ref["reference_digest"] = canonical_digest(
                {key: value for key, value in ref.items() if key != "reference_digest"}
            )
        elif attack == "missing_member":
            absent = prepare_content_object(
                object_kind="world_matrix_commission",
                value={"kind": "absent-but-well-formed-object"},
                path="branches/root/unused/absent.json",
            )
            handle["object_ref"] = copy.deepcopy(absent.ref)
        else:
            ref = handle["source_commit_reference"]
            ref["generation"] = 2
            ref["prior_generation"] = 1
            ref["reference_digest"] = canonical_digest(
                {key: value for key, value in ref.items() if key != "reference_digest"}
            )

    _commit_import_generation(
        store,
        source=source,
        source_reference=reference,
        handle_mutator=mutate,
    )
    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=2,
            graph_artifact_path=_graph_path(2),
        )
        with pytest.raises(StateCorruptionError):
            resolver.resolve_roots()


def test_same_bytes_from_transitive_reexport_are_wrong_lineage(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    commit1, _graph1, source = _source_generation(store)
    commit2, _graph2, _root2, _handle2 = _commit_import_generation(
        store,
        source=source,
        source_reference=_reference(commit1, 1),
    )
    # Generation 2 can resolve the bytes but does not own them.  Naming it as
    # the source in generation 3 must not launder identical bytes into a new
    # provenance lineage.
    _commit_import_generation(
        store,
        source=source,
        source_reference=_reference(commit2, 2),
        generation=3,
    )
    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=3,
            graph_artifact_path=_graph_path(3),
        )
        with pytest.raises(StateCorruptionError, match="transitive re-export"):
            resolver.resolve_roots()


def test_exact_commit_coverage_rejects_unmanifested_graph_member(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    source = _prepared(
        1,
        "source",
        object_kind="world_matrix_commission",
        value={"kind": "exact-coverage-source"},
    )
    namespace = Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 0)
    extra = CommitArtifact(
        "branches/root/content-graphs/g1/extra.json",
        canonical_json({"kind": "unmanifested-extra"}),
        namespace,
    )
    _commit_graph(
        store,
        generation=1,
        local_objects=[source],
        imported_handles=[],
        ordered_roots=[source.ref["object_id"]],
        edges=[],
        topological_order=[source.ref["object_id"]],
        extra_artifacts=[extra],
    )
    with store.verified_artifact_context() as context:
        with pytest.raises(StateCorruptionError, match="exactly one graph"):
            StoreVerifiedContentObjectGraph(
                store=store,
                context=context,
                generation=1,
                graph_artifact_path=_graph_path(1),
            )


def test_ambiguous_object_membership_is_rejected_from_verified_bytes(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    source = _prepared(
        1,
        "source",
        object_kind="world_matrix_commission",
        value={"kind": "ambiguous-source"},
    )
    alias = PreparedContentObject(
        value=source.value,
        data=source.data,
        ref=source.ref,
        descriptor={
            "ref": copy.deepcopy(source.ref),
            "path": _object_path(1, "alias"),
        },
    )
    graph = build_content_object_graph(
        local_descriptors=[source.descriptor],
        imported_handles=[],
        ordered_roots=[source.ref["object_id"]],
        edges=[],
        topological_order=[source.ref["object_id"]],
    )
    graph["local_descriptors"].append(copy.deepcopy(alias.descriptor))
    graph["graph_digest"] = canonical_digest(
        {key: value for key, value in graph.items() if key != "graph_digest"}
    )
    _commit_graph(
        store,
        generation=1,
        local_objects=[source, alias],
        imported_handles=[],
        ordered_roots=[source.ref["object_id"]],
        edges=[],
        topological_order=[source.ref["object_id"]],
        graph_override=graph,
    )
    with store.verified_artifact_context() as context:
        with pytest.raises(ContractError, match="IDs must be unique"):
            StoreVerifiedContentObjectGraph(
                store=store,
                context=context,
                generation=1,
                graph_artifact_path=_graph_path(1),
            )


def test_coordinated_object_and_graph_rehash_cannot_cross_commit_manifest(
    tmp_path: Path,
) -> None:
    store = DiscoveryTransactionStore(
        tmp_path / "store", target_id=TARGET_ID, run_id=RUN_ID
    )
    commit, _graph, source = _source_generation(store)
    forged = _prepared(
        1,
        "shared-source",
        object_kind="world_matrix_commission",
        value={"kind": "coordinated-rehash", "claim": "forged"},
    )
    forged_graph = build_content_object_graph(
        local_descriptors=[forged.descriptor],
        imported_handles=[],
        ordered_roots=[forged.ref["object_id"]],
        edges=[],
        topological_order=[forged.ref["object_id"]],
    )
    artifacts = commit.commit_path / "artifacts"
    (artifacts / source.descriptor["path"]).write_bytes(forged.data)
    (artifacts / _graph_path(1)).write_bytes(canonical_json(forged_graph))
    with pytest.raises(StateCorruptionError):
        with store.verified_artifact_context():
            pass


def test_transaction_graph_replays_after_whole_store_relocation(tmp_path: Path) -> None:
    original_root = tmp_path / "original"
    chain = _chain(original_root)
    relocated_root = tmp_path / "relocated"
    shutil.copytree(original_root, relocated_root)
    relocated = DiscoveryTransactionStore(
        relocated_root, target_id=TARGET_ID, run_id=RUN_ID
    )
    with relocated.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=relocated,
            context=context,
            generation=2,
            graph_artifact_path=_graph_path(2),
        )
        assert resolver.resolve(chain["source"].ref["object_id"]).value == (
            chain["source"].value
        )
