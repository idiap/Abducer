# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for the compact world content-object graph.

These tests establish the storage kernel before the canonical v2-to-v3
cutover.  They deliberately distinguish graph integrity from domain authority:
the graph must replay exact portable bytes and reject undeclared structure, but
it does not by itself authorize a producer, experiment, or physics conclusion.
"""

from __future__ import annotations

import copy
import os
import shutil
import time
from pathlib import Path

import pytest

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    VerifiedContentObjectGraph,
    build_content_object_graph,
    prepare_content_object,
    validate_content_object_graph,
)


def _write(root: Path, prepared: PreparedContentObject) -> None:
    descriptor = prepared.descriptor
    path = root / descriptor["path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(prepared.data)


def _reseal(graph: dict[str, object]) -> dict[str, object]:
    graph["graph_digest"] = canonical_digest(
        {key: value for key, value in graph.items() if key != "graph_digest"}
    )
    return graph


def _diamond(root: Path) -> tuple[dict[str, object], dict[str, object]]:
    shared = prepare_content_object(
        object_kind="world_matrix_commission",
        value={"kind": "shared-literature-and-theory", "value": 7},
        path="objects/shared.json",
    )
    request = prepare_content_object(
        object_kind="world_request",
        value={"kind": "world-request", "shared_id": shared.ref["object_id"]},
        path="objects/request.json",
    )
    envelope = prepare_content_object(
        object_kind="world_observation_envelope",
        value={"kind": "world-envelope", "shared_id": shared.ref["object_id"]},
        path="objects/envelope.json",
    )
    certificate = prepare_content_object(
        object_kind="world_matrix_certificate",
        value={
            "kind": "matrix-certificate",
            "request_id": request.ref["object_id"],
            "envelope_id": envelope.ref["object_id"],
        },
        path="objects/certificate.json",
    )
    for prepared in (shared, request, envelope, certificate):
        _write(root, prepared)
    edges = [
        {
            "source_object_id": shared.ref["object_id"],
            "target_object_id": request.ref["object_id"],
            "edge_kind": "request_dependency",
        },
        {
            "source_object_id": shared.ref["object_id"],
            "target_object_id": envelope.ref["object_id"],
            "edge_kind": "observation_dependency",
        },
        {
            "source_object_id": request.ref["object_id"],
            "target_object_id": certificate.ref["object_id"],
            "edge_kind": "aggregation_dependency",
        },
        {
            "source_object_id": envelope.ref["object_id"],
            "target_object_id": certificate.ref["object_id"],
            "edge_kind": "aggregation_dependency",
        },
    ]
    graph = build_content_object_graph(
        local_descriptors=[
            shared.descriptor,
            request.descriptor,
            envelope.descriptor,
            certificate.descriptor,
        ],
        imported_handles=[],
        ordered_roots=[certificate.ref["object_id"]],
        edges=edges,
        topological_order=[
            shared.ref["object_id"],
            request.ref["object_id"],
            envelope.ref["object_id"],
            certificate.ref["object_id"],
        ],
    )
    return graph, {
        "shared": shared,
        "request": request,
        "envelope": envelope,
        "certificate": certificate,
    }


def test_shared_object_is_stored_once_and_replays_after_relocation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "original"
    root.mkdir()
    graph, objects = _diamond(root)

    assert len(list(root.rglob("shared.json"))) == 1
    assert sum(
        row["ref"]["object_id"] == objects["shared"].ref["object_id"]
        for row in graph["local_descriptors"]
    ) == 1
    resolver = VerifiedContentObjectGraph(local_root=root, graph=graph)
    resolved = resolver.resolve_roots()[0]
    assert resolved.value == objects["certificate"].value
    assert resolver.resolve(objects["shared"].ref["object_id"]).value == (
        objects["shared"].value
    )

    relocated = tmp_path / "relocated"
    shutil.copytree(root, relocated)
    shutil.rmtree(root)
    reopened = VerifiedContentObjectGraph(local_root=relocated, graph=graph)
    assert reopened.resolve_roots()[0].data == objects["certificate"].data


def test_root_resolution_rejects_missing_prerequisite_bytes(tmp_path: Path) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    shared = next(
        row
        for row in graph["local_descriptors"]
        if row["ref"]["object_id"] == objects["shared"].ref["object_id"]
    )
    (root / shared["path"]).unlink()
    with pytest.raises(ContractError, match="exact graph coverage"):
        VerifiedContentObjectGraph(local_root=root, graph=graph).resolve_roots()


def test_root_resolution_rejects_unmanifested_local_file(tmp_path: Path) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, _objects = _diamond(root)
    (root / "objects" / "undeclared.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ContractError, match="exact graph coverage"):
        VerifiedContentObjectGraph(local_root=root, graph=graph).resolve_roots()


def test_cached_results_cannot_be_poisoned_by_callers(tmp_path: Path) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    resolver = VerifiedContentObjectGraph(local_root=root, graph=graph)
    first = resolver.resolve(objects["shared"].ref["object_id"])
    first.value["value"] = 999
    first.ref["object_kind"] = "world_request"
    second = resolver.resolve(objects["shared"].ref["object_id"])
    assert second.value == objects["shared"].value
    assert second.ref == objects["shared"].ref


@pytest.mark.parametrize("mutation", ["size", "sha256", "kind", "path"])
def test_resolver_rejects_descriptor_or_byte_identity_drift(
    tmp_path: Path,
    mutation: str,
) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    forged = copy.deepcopy(graph)
    row = next(
        item
        for item in forged["local_descriptors"]
        if item["ref"]["object_id"] == objects["certificate"].ref["object_id"]
    )
    if mutation == "size":
        row["ref"]["size_bytes"] += 1
    elif mutation == "sha256":
        row["ref"]["sha256"] = "sha256:" + "0" * 64
    elif mutation == "kind":
        row["ref"]["object_kind"] = "world_request"
    else:
        row["path"] = "objects/missing.json"
    _reseal(forged)
    resolver = VerifiedContentObjectGraph(local_root=root, graph=forged)
    with pytest.raises(ContractError):
        resolver.resolve(objects["certificate"].ref["object_id"])


def test_graph_rejects_dangling_cycle_alias_and_unreachable_object(
    tmp_path: Path,
) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)

    dangling = copy.deepcopy(graph)
    dangling["edges"][0]["source_object_id"] = "missing.object"
    with pytest.raises(ContractError):
        validate_content_object_graph(_reseal(dangling))

    cycle = copy.deepcopy(graph)
    cycle["edges"].append(
        {
            "source_object_id": objects["certificate"].ref["object_id"],
            "target_object_id": objects["shared"].ref["object_id"],
            "edge_kind": "history_dependency",
        }
    )
    with pytest.raises(ContractError):
        validate_content_object_graph(_reseal(cycle))

    alias = copy.deepcopy(graph)
    alias["local_descriptors"][1]["path"] = alias["local_descriptors"][0]["path"]
    with pytest.raises(ContractError):
        validate_content_object_graph(_reseal(alias))

    extra = prepare_content_object(
        object_kind="world_request",
        value={"kind": "unreachable"},
        path="objects/unreachable.json",
    )
    unreachable = copy.deepcopy(graph)
    unreachable["local_descriptors"].append(extra.descriptor)
    unreachable["topological_order"].insert(0, extra.ref["object_id"])
    with pytest.raises(ContractError, match="outside root closure"):
        validate_content_object_graph(_reseal(unreachable))


@pytest.mark.parametrize("unsafe", ["../escape.json", "/absolute.json", "a/./b.json"])
def test_descriptor_rejects_noncanonical_or_escaping_paths(unsafe: str) -> None:
    with pytest.raises(ContractError):
        prepare_content_object(
            object_kind="world_request",
            value={"kind": "unsafe-path"},
            path=unsafe,
        )


def test_resolver_rejects_noncanonical_json_even_after_coordinated_ref_change(
    tmp_path: Path,
) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    descriptor = next(
        row
        for row in graph["local_descriptors"]
        if row["ref"]["object_id"] == objects["request"].ref["object_id"]
    )
    path = root / descriptor["path"]
    noncanonical = b'{"shared_id": "x", "kind": "world-request"}'
    path.write_bytes(noncanonical)
    forged = copy.deepcopy(graph)
    row = next(
        item
        for item in forged["local_descriptors"]
        if item["ref"]["object_id"] == objects["request"].ref["object_id"]
    )
    row["ref"]["sha256"] = bytes_digest(noncanonical)
    row["ref"]["size_bytes"] = len(noncanonical)
    row["ref"]["semantic_digest"] = canonical_digest(
        {"shared_id": "x", "kind": "world-request"}
    )
    _reseal(forged)
    with pytest.raises(ContractError, match="canonical JSON"):
        VerifiedContentObjectGraph(local_root=root, graph=forged).resolve(
            objects["request"].ref["object_id"]
        )


@pytest.mark.parametrize("file_attack", ["symlink", "hardlink", "fifo"])
def test_component_safe_reader_rejects_link_and_special_file_attacks(
    tmp_path: Path,
    file_attack: str,
) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    descriptor = next(
        row
        for row in graph["local_descriptors"]
        if row["ref"]["object_id"] == objects["certificate"].ref["object_id"]
    )
    victim = root / descriptor["path"]
    original = victim.read_bytes()
    victim.unlink()
    if file_attack == "symlink":
        target = tmp_path / "outside.json"
        target.write_bytes(original)
        victim.symlink_to(target)
    elif file_attack == "hardlink":
        target = tmp_path / "outside.json"
        target.write_bytes(original)
        os.link(target, victim)
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("FIFO creation is unavailable")
        os.mkfifo(victim)
    started = time.monotonic()
    with pytest.raises(ContractError):
        VerifiedContentObjectGraph(local_root=root, graph=graph).resolve(
            objects["certificate"].ref["object_id"]
        )
    assert time.monotonic() - started < 1.0


def test_reader_rejects_symlinked_intermediate_directory(tmp_path: Path) -> None:
    root = tmp_path / "objects"
    root.mkdir()
    graph, objects = _diamond(root)
    real = root / "real"
    (root / "objects").rename(real)
    (root / "objects").symlink_to(real, target_is_directory=True)
    with pytest.raises(ContractError):
        VerifiedContentObjectGraph(local_root=root, graph=graph).resolve(
            objects["certificate"].ref["object_id"]
        )
