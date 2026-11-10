# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused adversarial tests for store-derived canonical role reopening."""

from __future__ import annotations

import copy
import inspect
import shutil
from collections import deque
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.canonical_role_graph import reopen_canonical_role_graph
from agentic.discovery.committed_projection import (
    committed_cycle_projection_artifact_paths,
    load_committed_cycle_projection_sources,
)
from agentic.discovery.contracts import canonical_digest
from agentic.discovery.cycle import run_canonical_discovery_cycle
from agentic.state.discovery_transaction import DiscoveryTransactionStore
from tests.discovery.test_canonical_discovery_cycle import CanonicalExercise


_REQUIRED_ROLE_KEYS = [
    "literature_production_input_bundle[0]",
    "source_routing_pre_map_policy[0]",
    "source_routing_realization[0]",
    "high_risk_portfolio[0]",
    "parallel_portfolio[0]",
    "reflective_packets[0]",
    "reflective_packets[1]",
    "parent_conceptual_adjudication[0]",
    "synthesis_conceptual_adjudication[0]",
]


@pytest.fixture(scope="module")
def committed_cycle(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = tmp_path_factory.mktemp("canonical-role-graph")
    exercise = CanonicalExercise(
        root,
        live=True,
        experiment=False,
        commission_support=True,
    )
    cycle = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    store = DiscoveryTransactionStore(
        exercise.state_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    return {
        "exercise": exercise,
        "cycle": cycle,
        "store": store,
        "generation": cycle["committed_state_version"],
    }


def _copied_store(
    committed_cycle: dict[str, Any],
    destination: Path,
) -> DiscoveryTransactionStore:
    exercise: CanonicalExercise = committed_cycle["exercise"]
    shutil.copytree(exercise.state_root, destination)
    return DiscoveryTransactionStore(
        destination,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )


def _node_map(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["node_id"]: row for row in graph["nodes"]}


def test_reopens_exact_committed_roles_without_a_metadata_injection_port(
    committed_cycle: dict[str, Any],
) -> None:
    store: DiscoveryTransactionStore = committed_cycle["store"]
    generation = committed_cycle["generation"]
    assert tuple(inspect.signature(reopen_canonical_role_graph).parameters) == (
        "store",
        "verified_theory_generation",
    )

    result = reopen_canonical_role_graph(store, generation)
    assert result.status == "valid"
    assert result.reason_code == "committed_role_graph_reopened"
    assert result.failure_class is None
    graph = result.graph
    assert graph is not None
    assert graph["required_role_keys"] == _REQUIRED_ROLE_KEYS
    graph_without_digest = copy.deepcopy(graph)
    assert graph_without_digest.pop("graph_digest") == canonical_digest(
        graph_without_digest
    )
    assert graph["authority_boundary"]["registry_metadata_as_role_evidence"] is None
    assert graph["authority_boundary"]["missing_role_synthesis_authority"] is None

    sources = load_committed_cycle_projection_sources(store, generation)
    nodes = _node_map(graph)
    for role_key in _REQUIRED_ROLE_KEYS:
        role, raw_index = role_key[:-1].split("[")
        role_index = int(raw_index)
        node = nodes[f"role:{role_key}"]
        assert node["payload"] == sources.semantic_payloads[(role, role_index)]
        assert node["payload_digest"] == canonical_digest(node["payload"])
    literature = nodes["role:literature_production_input_bundle[0]"]
    assert literature["source_kind"] == "external_role_artifact"
    assert literature["producer_binding"] is None
    for role_key in _REQUIRED_ROLE_KEYS[1:]:
        assert nodes[f"role:{role_key}"]["producer_binding"] is not None

    # Frozen result bytes prevent a caller mutation from becoming replay state.
    graph["nodes"].clear()
    reopened_again = result.graph
    assert reopened_again is not None
    assert reopened_again["nodes"]
    assert reopened_again["graph_digest"] == result.graph["graph_digest"]


def test_every_evidence_and_mandatory_role_node_is_reachable_from_commit(
    committed_cycle: dict[str, Any],
) -> None:
    result = reopen_canonical_role_graph(
        committed_cycle["store"],
        committed_cycle["generation"],
    )
    graph = result.graph
    assert graph is not None
    nodes = _node_map(graph)
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in nodes}
    for edge in graph["edges"]:
        adjacency[edge["from"]].add(edge["to"])

    reached = {graph["root_node_id"]}
    pending = deque([graph["root_node_id"]])
    while pending:
        for target in sorted(adjacency[pending.popleft()]):
            if target not in reached:
                reached.add(target)
                pending.append(target)
    assert reached == set(nodes)
    assert all(f"role:{role_key}" in reached for role_key in _REQUIRED_ROLE_KEYS)

    producer_edges = {
        (edge["from"], edge["to"])
        for edge in graph["edges"]
        if edge["relation"]
        == "successful_receipt_binds_verified_package_copy"
    }
    for role_key in _REQUIRED_ROLE_KEYS[1:]:
        role_node = nodes[f"role:{role_key}"]
        receipt_id = role_node["producer_binding"]["receipt_id"]
        assert (
            f"producer-receipt:{receipt_id}",
            f"role:{role_key}",
        ) in producer_edges


def test_genuinely_absent_mandatory_roles_are_typed_unavailable(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(tmp_path, live=False, experiment=False)
    cycle = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    store = DiscoveryTransactionStore(
        exercise.state_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )

    result = reopen_canonical_role_graph(
        store,
        cycle["committed_state_version"],
    )
    assert result.status == "unavailable"
    assert result.reason_code == "mandatory_role_unavailable"
    assert result.failure_class == "missing_mandatory_role"
    assert "source_routing_pre_map_policy[0]" in result.detail
    assert result.graph is None
    assert result.as_dict()["graph"] is None


def test_manifest_covered_role_byte_tamper_is_typed_invalid(
    committed_cycle: dict[str, Any],
    tmp_path: Path,
) -> None:
    store = _copied_store(committed_cycle, tmp_path / "tampered-store")
    generation = committed_cycle["generation"]
    commit = store.read_verified_commit(generation)
    role_path = next(
        path
        for path in committed_cycle_projection_artifact_paths(generation)
        if "/semantic/high_risk_portfolio/" in path
    )
    artifact_path = commit.commit_path / "artifacts" / role_path
    artifact_path.write_bytes(artifact_path.read_bytes() + b" ")

    result = reopen_canonical_role_graph(store, generation)
    assert result.status == "invalid"
    assert result.reason_code in {
        "verified_commit_integrity_failure",
        "committed_role_graph_integrity_failure",
    }
    assert result.failure_class == "state_corruption"
    assert result.graph is None
