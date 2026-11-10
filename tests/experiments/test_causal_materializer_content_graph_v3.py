# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial acceptance tests for portable causal materialization graphs.

The local v3 materializer proves exact copying while its workspace is live.
These tests prove that its adapter preserves the full protocol as one path-free,
mergeable content-graph fragment and that pure replay still succeeds after the
source workspace and original transaction store no longer exist.  Nothing here
promotes byte-copy evidence into scientific, semantic, proof, or physics
authority.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

import pytest

import agentic.experiments.causal_materializer_content_graph_v3 as portable
from agentic.discovery.contracts import ContractError, Namespace, canonical_json
from agentic.experiments.causal_materializer_content_graph_v3 import (
    ARTIFACT_KIND,
    ATTEMPT_KIND,
    BINDING_HEADER_KIND,
    CLOCK_KIND,
    DEPENDENCY_KIND,
    EVIDENCE_HEADER_KIND,
    MAX_PORTABLE_FRAGMENT_OBJECTS,
    REQUEST_KIND,
    prepare_portable_causal_materialization_fragment_v3,
    validate_portable_causal_materialization_closure_v3,
)
from agentic.experiments.causal_producer_runtime_v3 import (
    CausalArtifactMaterializerRuntimeV3,
    snapshot_sealed_causal_materialization_v3,
)
from agentic.experiments.content_graph_transactions import (
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
    reopen_content_graph_transaction,
)
from agentic.experiments.world_object_graph import (
    ResolvedContentObject,
    build_content_object_graph,
)
from agentic.experiments.world_object_graph_store import (
    StoreVerifiedContentObjectGraph,
)
from agentic.experiments.world_object_roles import (
    RoleAuthority,
    content_object_role,
    validate_payload_derived_edges,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


TARGET_ID = "portable-materializer-target"
RUN_ID = "portable-materializer-run"
BRANCH_ID = "root"
PROGRAMME_ID = "portable-materializer-programme"
GRAPH_PATH = "branches/root/content-graphs/g1/graph.json"
OBJECT_PREFIX = "branches/root/content-graphs/g1/portable"
REPO_ROOT = Path(__file__).resolve().parents[2]


def _runtime(root: Path) -> CausalArtifactMaterializerRuntimeV3:
    root.mkdir(parents=True, exist_ok=True)
    return CausalArtifactMaterializerRuntimeV3(
        workspace=root,
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 0),
    )


def _seal_snapshot(
    root: Path,
    *,
    artifact: Mapping[str, Any] | None = None,
):
    runtime = _runtime(root)
    sealed = runtime.seal(
        stage_id="portable-stage",
        materializer_role="exact-byte-materializer",
        artifact_id="portable-artifact",
        artifact=(
            {
                "schema_version": "1.0.0",
                "payload": "portable-content-graph-fixture",
                "ordinal": 7,
            }
            if artifact is None
            else artifact
        ),
    )
    return snapshot_sealed_causal_materialization_v3(sealed, workspace=root)


def _fragment(snapshot):
    return prepare_portable_causal_materialization_fragment_v3(
        snapshot,
        object_path_prefix=OBJECT_PREFIX,
    )


def _resolved(fragment) -> tuple[ResolvedContentObject, ...]:
    return tuple(
        ResolvedContentObject(
            ref=copy.deepcopy(dict(row.ref)),
            value=copy.deepcopy(dict(row.value)),
            data=bytes(row.data),
        )
        for row in fragment.local_objects
    )


def _contains_key(value: Any, forbidden: str) -> bool:
    if isinstance(value, Mapping):
        return forbidden in value or any(
            _contains_key(child, forbidden) for child in value.values()
        )
    if isinstance(value, list):
        return any(_contains_key(child, forbidden) for child in value)
    return False


def _graph(fragment) -> dict[str, Any]:
    objects = fragment.local_objects
    return build_content_object_graph(
        local_descriptors=[row.descriptor for row in objects],
        imported_handles=(),
        ordered_roots=[fragment.binding_root_ref["object_id"]],
        edges=fragment.edges,
        topological_order=fragment.topological_order,
    )


def test_fragment_is_path_free_one_copy_typed_and_exactly_payload_derived(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "materializer"
    snapshot = _seal_snapshot(workspace)
    fragment = _fragment(snapshot)
    objects = fragment.local_objects
    by_kind: dict[str, list[Any]] = {}
    for row in objects:
        by_kind.setdefault(str(row.ref["object_kind"]), []).append(row)

    assert len(objects) == 12 == snapshot.binding["successful_attempt"] + 11
    assert len(objects) <= MAX_PORTABLE_FRAGMENT_OBJECTS
    assert {kind: len(rows) for kind, rows in by_kind.items()} == {
        DEPENDENCY_KIND: 1,
        ARTIFACT_KIND: 1,
        REQUEST_KIND: 1,
        ATTEMPT_KIND: 1,
        CLOCK_KIND: 1,
        EVIDENCE_HEADER_KIND: 6,
        BINDING_HEADER_KIND: 1,
    }
    assert fragment.successful_receipt_ref == by_kind[ATTEMPT_KIND][-1].ref
    assert fragment.binding_root_ref == by_kind[BINDING_HEADER_KIND][0].ref

    headers = {
        row.value["evidence_kind"]: row.value
        for row in by_kind[EVIDENCE_HEADER_KIND]
    }
    artifact_ref = dict(by_kind[ARTIFACT_KIND][0].ref)
    assert {
        tuple(headers[kind]["evidence_payload_refs"])[0]["object_id"]
        for kind in ("staged_input", "producer_artifact", "immutable_history")
    } == {artifact_ref["object_id"]}
    assert headers["attempt_receipts"]["evidence_payload_refs"][-1] == (
        fragment.successful_receipt_ref
    )

    protocol_rows = [
        row for row in objects if row.ref["object_kind"] != ARTIFACT_KIND
    ]
    assert all(not _contains_key(row.value, "path") for row in protocol_rows)
    protocol_bytes = b"".join(row.data for row in protocol_rows)
    assert str(workspace).encode("utf-8") not in protocol_bytes
    assert b'"artifact_value"' not in protocol_bytes
    assert b'"bytes_base64"' not in protocol_bytes
    dependency = by_kind[DEPENDENCY_KIND][0].value
    assert dependency["components"]
    assert all("path" not in row for row in dependency["components"])
    assert all("path" not in row for row in dependency["declared_roots"])

    expected_edges = validate_payload_derived_edges(
        objects=tuple((row.ref, row.value) for row in objects),
        declared_edges=fragment.edges,
    )
    assert tuple(fragment.edges) == expected_edges
    assert len(fragment.edges) == 18
    position = {
        object_id: index
        for index, object_id in enumerate(fragment.topological_order)
    }
    assert all(
        position[edge["source_object_id"]] < position[edge["target_object_id"]]
        for edge in fragment.edges
    )
    graph = _graph(fragment)
    assert graph["ordered_roots"] == [fragment.binding_root_ref["object_id"]]

    replay = validate_portable_causal_materialization_closure_v3(
        _resolved(fragment), fragment.binding_root_ref
    )
    assert replay.source_snapshot_digest == snapshot.snapshot_digest
    assert replay.successful_attempt == 1
    assert replay.artifact_ref == artifact_ref
    assert replay.successful_receipt_ref == fragment.successful_receipt_ref
    assert len(replay.consumed_object_ids) == len(objects)

    assert content_object_role(BINDING_HEADER_KIND).authority is (
        RoleAuthority.STRUCTURAL_REFERENCE
    )
    assert content_object_role("causal_materializer_binding_v3").authority is (
        RoleAuthority.SEMANTIC_DOMAIN
    )

    returned_ref = fragment.binding_root_ref
    returned_ref["object_id"] = "caller-forgery"
    assert fragment.binding_root_ref["object_id"] != "caller-forgery"
    returned_objects = fragment.local_objects
    returned_objects[0].value["record_id"] = "caller-forgery"
    assert fragment.local_objects[0].value["record_id"] != "caller-forgery"

    wrong_edges = [copy.deepcopy(row) for row in fragment.edges]
    wrong_edges[0]["edge_kind"] = "content_dependency"
    with pytest.raises(ContractError, match="payload-derived"):
        validate_payload_derived_edges(
            objects=tuple((row.ref, row.value) for row in objects),
            declared_edges=wrong_edges,
        )


def test_failed_attempts_and_unreferenced_workspace_orphans_are_preserved_correctly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "retry-materializer"
    runtime = _runtime(workspace)
    original = runtime._run_command
    fail_once = True
    orphan_marker = b"UNREFERENCED-WORKER-ORPHAN-MUST-NOT-BE-COMMITTED"

    def injected(command: tuple[str, ...], payload: bytes):
        nonlocal fail_once
        if fail_once and tuple(command) == runtime.worker_command:
            fail_once = False
            (workspace / "worker-orphan.json").write_bytes(orphan_marker)
            return subprocess.CompletedProcess(command, 2, b"", b"forced failure")
        return original(command, payload)

    monkeypatch.setattr(runtime, "_run_command", injected)
    with pytest.raises(ContractError, match="attempt 1 failed"):
        runtime.seal(
            stage_id="portable-stage",
            materializer_role="exact-byte-materializer",
            artifact_id="portable-artifact",
            artifact={"schema_version": "1.0.0", "payload": "retry-fixture"},
        )
    sealed = runtime.seal(
        stage_id="portable-stage",
        materializer_role="exact-byte-materializer",
        artifact_id="portable-artifact",
        artifact={"schema_version": "1.0.0", "payload": "retry-fixture"},
    )
    snapshot = snapshot_sealed_causal_materialization_v3(
        sealed, workspace=workspace
    )
    fragment = _fragment(snapshot)
    attempts = [
        row
        for row in fragment.local_objects
        if row.ref["object_kind"] == ATTEMPT_KIND
    ]

    assert [row.value["attempt"] for row in attempts] == [1, 2]
    assert [row.value["status"] for row in attempts] == ["failed", "succeeded"]
    assert [row.value["materialized_copy_status"] for row in attempts] == [
        "not_available",
        "exact_input_output_history_alias_verified",
    ]
    assert fragment.successful_receipt_ref == attempts[-1].ref
    assert len(fragment.local_objects) == 13
    assert orphan_marker not in b"".join(row.data for row in fragment.local_objects)
    replay = validate_portable_causal_materialization_closure_v3(
        _resolved(fragment), fragment.binding_root_ref
    )
    assert replay.successful_attempt == 2
    assert replay.attempt_refs == tuple(dict(row.ref) for row in attempts)


def test_direct_snapshot_closure_prefix_and_ceiling_forgeries_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot = _seal_snapshot(tmp_path / "materializer")
    fragment = _fragment(snapshot)
    forged_snapshot = replace(snapshot, staged_input_bytes=b'{"forged":true}')
    with pytest.raises(ContractError):
        _fragment(forged_snapshot)

    resolved = list(_resolved(fragment))
    with pytest.raises(ContractError, match="lacks a referenced object"):
        validate_portable_causal_materialization_closure_v3(
            resolved[1:], fragment.binding_root_ref
        )

    first = resolved[0]
    resolved[0] = ResolvedContentObject(
        ref=first.ref,
        value=first.value,
        data=b'{"canonical_but_not_the_declared_value":true}',
    )
    with pytest.raises(ContractError, match="resolved bytes differ"):
        validate_portable_causal_materialization_closure_v3(
            resolved, fragment.binding_root_ref
        )

    for prefix in ("", "../escape", "branches//root"):
        with pytest.raises(ContractError):
            prepare_portable_causal_materialization_fragment_v3(
                snapshot, object_path_prefix=prefix
            )

    monkeypatch.setattr(portable, "MAX_PORTABLE_FRAGMENT_OBJECTS", 1)
    with pytest.raises(ContractError, match="object ceiling"):
        _fragment(snapshot)


def test_atomic_commit_reopens_after_relocation_source_deletion_and_fresh_process(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "materializer"
    snapshot = _seal_snapshot(workspace)
    fragment = _fragment(snapshot)
    graph = _graph(fragment)
    state = {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "generation": 1,
        "programme_id": PROGRAMME_ID,
        "theory_status": "storage-provenance-fixture-only",
    }
    transaction = prepare_content_graph_transaction(
        expected_generation=0,
        state=state,
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 0),
        graph_artifact_path=GRAPH_PATH,
        graph=graph,
        local_objects=fragment.local_objects,
    )
    original_store_root = tmp_path / "original-store"
    store = DiscoveryTransactionStore(
        original_store_root, target_id=TARGET_ID, run_id=RUN_ID
    )
    committed = commit_content_graph_transaction(store=store, transaction=transaction)
    reopened = reopen_content_graph_transaction(
        store=store, generation=1, graph_artifact_path=GRAPH_PATH
    )
    assert committed == reopened
    assert committed.root_refs == (fragment.binding_root_ref,)
    with store.verified_artifact_context() as context:
        resolver = StoreVerifiedContentObjectGraph(
            store=store,
            context=context,
            generation=1,
            graph_artifact_path=GRAPH_PATH,
        )
        closure = resolver.verify_closure()
        replay = validate_portable_causal_materialization_closure_v3(
            closure, resolver.resolve_roots()[0].ref
        )
        assert replay.source_snapshot_digest == snapshot.snapshot_digest

    relocated_store_root = tmp_path / "relocated-store"
    shutil.copytree(original_store_root, relocated_store_root)
    shutil.rmtree(workspace)
    shutil.rmtree(original_store_root)
    assert not workspace.exists()
    assert not original_store_root.exists()

    script = """
import json
import sys
from pathlib import Path
from agentic.experiments.causal_materializer_content_graph_v3 import validate_portable_causal_materialization_closure_v3
from agentic.experiments.world_object_graph_store import StoreVerifiedContentObjectGraph
from agentic.state.discovery_transaction import DiscoveryTransactionStore
root = Path(sys.argv[1])
store = DiscoveryTransactionStore(root, target_id=sys.argv[2], run_id=sys.argv[3])
with store.verified_artifact_context() as context:
    resolver = StoreVerifiedContentObjectGraph(store=store, context=context, generation=1, graph_artifact_path=sys.argv[4])
    closure = resolver.verify_closure()
    result = validate_portable_causal_materialization_closure_v3(closure, resolver.resolve_roots()[0].ref)
    print(json.dumps({"digest": result.source_snapshot_digest, "attempt": result.successful_attempt, "objects": len(result.consumed_object_ids)}, sort_keys=True))
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(relocated_store_root),
            TARGET_ID,
            RUN_ID,
            GRAPH_PATH,
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    fresh = json.loads(completed.stdout)
    assert fresh == {
        "attempt": 1,
        "digest": snapshot.snapshot_digest,
        "objects": len(fragment.local_objects),
    }


def test_multi_megabyte_artifact_is_serialized_once_with_bounded_adapter_cost(
    tmp_path: Path,
) -> None:
    marker = "UNIQUE-LARGE-PORTABLE-ARTIFACT-MARKER"
    snapshot = _seal_snapshot(
        tmp_path / "large-materializer",
        artifact={
            "schema_version": "1.0.0",
            "payload": marker + ("x" * 2_500_000),
        },
    )
    started = time.monotonic()
    fragment = _fragment(snapshot)
    elapsed = time.monotonic() - started
    objects = fragment.local_objects

    assert sum(row.data.count(marker.encode("utf-8")) for row in objects) == 1
    assert sum(row.ref["object_kind"] == ARTIFACT_KIND for row in objects) == 1
    assert fragment.total_object_bytes < len(snapshot.staged_input_bytes) * 2
    assert elapsed < 10.0
    replay = validate_portable_causal_materialization_closure_v3(
        _resolved(fragment), fragment.binding_root_ref
    )
    assert replay.artifact_ref["size_bytes"] == len(snapshot.staged_input_bytes)
