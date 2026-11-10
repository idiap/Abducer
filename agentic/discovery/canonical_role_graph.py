# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Fail-closed reopening of the committed canonical projection-role graph.

This module deliberately has no registry input and no caller-supplied role
payload input.  It reopens the bounded role set already sealed by
``committed_projection`` and turns that evidence into a portable graph:

* the verified commit is the sole graph root;
* package and original-role descriptors come from its verified manifest;
* semantic nodes contain the exact validated payload reopened from the store;
* operator-produced roles require their exact successful producer receipt; and
* the literature input remains explicitly external instead of acquiring a
  fictitious producer.

The graph is a committed-evidence reachability graph, not a claim that its
display edges exhaust the scientific causal structure of a discovery cycle.
It grants no truth, novelty, conceptual-depth, or physics-result authority.
Missing mandatory evidence returns a typed ``unavailable`` result.  Digest,
schema, namespace, producer, or cross-binding failures return a typed
``invalid`` result.  Neither failure result exposes a partial graph.
"""

from __future__ import annotations

import copy
import dataclasses
import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from agentic.discovery.committed_projection import (
    committed_cycle_projection_artifact_paths,
    load_committed_cycle_projection_sources,
)
from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
)
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    StateCorruptionError,
    VerifiedCommit,
)


CANONICAL_ROLE_GRAPH_CONTRACT_VERSION = "canonical-role-graph/1.0.0"

# This is a mandatory evidence contract, not a fallback source of payloads or
# producers.  A row only becomes a graph node after the committed loader has
# independently reopened and verified its exact payload and producer binding.
_MANDATORY_SEMANTIC_ROLES: tuple[tuple[str, int, str | None], ...] = (
    ("literature_production_input_bundle", 0, None),
    (
        "source_routing_pre_map_policy",
        0,
        "source-routing-pre-map-policy-producer",
    ),
    (
        "source_routing_realization",
        0,
        "source-routing-realization-producer",
    ),
    ("high_risk_portfolio", 0, "high-risk-hypothesis-forger"),
    ("parallel_portfolio", 0, "parallel-hypothesis-portfolio"),
    ("reflective_packets", 0, "reflective-conceptual-discovery"),
    ("reflective_packets", 1, "reflective-theory-synthesizer"),
    (
        "parent_conceptual_adjudication",
        0,
        "blind-conceptual-preference-adjudicator",
    ),
    (
        "synthesis_conceptual_adjudication",
        0,
        "blind-conceptual-preference-adjudicator",
    ),
)
_MANDATORY_CORE_SOURCES: tuple[str, ...] = (
    "canonical_cycle",
    "finalized_reflection",
    "operator_evidence",
    "schedule",
)
_UNAVAILABLE_ROLE_PREFIX = "committed cycle lacks required projection source "


@dataclasses.dataclass(frozen=True, slots=True)
class CanonicalRoleGraphReopenResult:
    """Typed terminal result whose graph accessor always returns a fresh value."""

    status: Literal["valid", "unavailable", "invalid"]
    reason_code: str
    verified_theory_generation: int | None
    failure_class: str | None
    detail: str
    _graph_bytes: bytes | None = dataclasses.field(default=None, repr=False)

    @property
    def graph(self) -> dict[str, Any] | None:
        """Return a detached graph, or ``None`` for every fail-closed outcome."""

        if self._graph_bytes is None:
            return None
        value = json.loads(self._graph_bytes)
        if not isinstance(value, dict):  # pragma: no cover - construction invariant
            raise RuntimeError("canonical role graph bytes are not an object")
        return value

    @property
    def result_digest(self) -> str:
        """Digest the terminal disposition and, when valid, its graph identity."""

        graph = self.graph
        return canonical_digest(
            {
                "status": self.status,
                "reason_code": self.reason_code,
                "verified_theory_generation": self.verified_theory_generation,
                "failure_class": self.failure_class,
                "detail": self.detail,
                "graph_digest": None if graph is None else graph["graph_digest"],
            }
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a portable detached representation of this terminal result."""

        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "verified_theory_generation": self.verified_theory_generation,
            "failure_class": self.failure_class,
            "detail": self.detail,
            "graph": self.graph,
            "result_digest": self.result_digest,
        }


def _terminal(
    *,
    status: Literal["valid", "unavailable", "invalid"],
    reason_code: str,
    generation: int | None,
    detail: str,
    failure_class: str | None = None,
    graph: Mapping[str, Any] | None = None,
) -> CanonicalRoleGraphReopenResult:
    if status == "valid":
        if graph is None or failure_class is not None:
            raise RuntimeError("valid canonical role graph result is malformed")
        graph_bytes = canonical_json(graph)
    else:
        if graph is not None or failure_class is None:
            raise RuntimeError("failed canonical role graph result is malformed")
        graph_bytes = None
    return CanonicalRoleGraphReopenResult(
        status=status,
        reason_code=reason_code,
        verified_theory_generation=generation,
        failure_class=failure_class,
        detail=detail,
        _graph_bytes=graph_bytes,
    )


def _role_key(role: str, role_index: int) -> str:
    return f"{role}[{role_index}]"


def _descriptor_map(commit: VerifiedCommit) -> dict[str, dict[str, Any]]:
    rows = commit.manifest.get("artifacts")
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise ContractError("verified commit artifact manifest is not an array")
    descriptors: dict[str, dict[str, Any]] = {}
    for raw in rows:
        if not isinstance(raw, Mapping):
            raise ContractError("verified commit artifact descriptor is not an object")
        path = raw.get("path")
        if not isinstance(path, str) or not path:
            raise ContractError("verified commit artifact descriptor lacks a path")
        if path in descriptors:
            raise ContractError(f"verified commit repeats artifact descriptor {path!r}")
        descriptors[path] = copy.deepcopy(dict(raw))
    return descriptors


def _one_binding(
    rows: Any,
    *,
    label: str,
    predicate: Any,
) -> dict[str, Any]:
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise ContractError(f"{label} binding collection is not an array")
    matches = [
        copy.deepcopy(dict(row))
        for row in rows
        if isinstance(row, Mapping) and predicate(row)
    ]
    if len(matches) != 1:
        raise ContractError(f"committed role graph requires exactly one {label} binding")
    return matches[0]


def _commit_identity(commit: VerifiedCommit) -> dict[str, Any]:
    state = commit.state
    if not isinstance(state, Mapping):
        raise ContractError("verified commit state is not an object")
    target_id = state.get("target_id")
    run_id = state.get("run_id")
    if not isinstance(target_id, str) or not isinstance(run_id, str):
        raise ContractError("verified commit state lacks target/run identity")
    identity = {
        "target_id": target_id,
        "run_id": run_id,
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
    }
    identity["identity_digest"] = canonical_digest(identity)
    return identity


def _add_edge(
    edges: list[dict[str, str]],
    source: str,
    target: str,
    relation: str,
) -> None:
    edges.append({"from": source, "to": target, "relation": relation})


def _require_graph_reachability(
    nodes: Sequence[Mapping[str, Any]],
    edges: Sequence[Mapping[str, Any]],
    *,
    root_node_id: str,
    mandatory_role_node_ids: Sequence[str],
) -> None:
    node_ids = [row.get("node_id") for row in nodes]
    if (
        any(not isinstance(node_id, str) or not node_id for node_id in node_ids)
        or len(set(node_ids)) != len(node_ids)
        or root_node_id not in node_ids
    ):
        raise ContractError("canonical role graph node identity is invalid")
    known = set(node_ids)
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in known}
    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        relation = edge.get("relation")
        if (
            source not in known
            or target not in known
            or not isinstance(relation, str)
            or not relation
        ):
            raise ContractError("canonical role graph edge is invalid")
        adjacency[source].add(target)
    reached = {root_node_id}
    frontier = [root_node_id]
    while frontier:
        source = frontier.pop()
        for target in sorted(adjacency[source]):
            if target not in reached:
                reached.add(target)
                frontier.append(target)
    missing = sorted(known - reached)
    if missing:
        raise ContractError(
            "canonical role graph contains unreachable evidence nodes: "
            + ", ".join(missing)
        )
    if any(node_id not in reached for node_id in mandatory_role_node_ids):
        raise ContractError("canonical role graph has an unreachable mandatory role")


def _build_graph(
    store: DiscoveryTransactionStore,
    preflight_commit: VerifiedCommit,
    sources: Any,
) -> dict[str, Any]:
    commit = sources.verified_commit
    if _commit_identity(commit) != _commit_identity(preflight_commit):
        raise ContractError("canonical role graph crossed verified commit snapshots")
    source_index = sources.source_index
    if not isinstance(source_index, Mapping):
        raise ContractError("committed projection source index is not an object")
    descriptors = _descriptor_map(commit)
    paths = committed_cycle_projection_artifact_paths(commit.generation)
    index_path = paths[0]
    if index_path not in descriptors:
        raise ContractError("committed projection source index is not manifest-covered")

    root_node_id = "verified-commit"
    index_node_id = "projection-source-index"
    nodes: list[dict[str, Any]] = [
        {
            "node_id": root_node_id,
            "node_kind": "verified_commit",
            "identity": _commit_identity(commit),
        },
        {
            "node_id": index_node_id,
            "node_kind": "projection_source_index",
            "package_descriptor": copy.deepcopy(descriptors[index_path]),
            "payload": copy.deepcopy(dict(source_index)),
            "payload_digest": canonical_digest(source_index),
        },
    ]
    edges: list[dict[str, str]] = []
    _add_edge(
        edges,
        root_node_id,
        index_node_id,
        "manifest_contains_verified_artifact",
    )

    core_values: dict[str, Mapping[str, Any]] = {
        "canonical_cycle": sources.canonical_cycle,
        "finalized_reflection": sources.finalized_reflection,
        "operator_evidence": sources.operator_evidence,
        "schedule": sources.schedule,
    }
    core_node_ids: dict[str, str] = {}
    for source_name in _MANDATORY_CORE_SOURCES:
        binding = _one_binding(
            source_index.get("core_bindings"),
            label=f"core source {source_name}",
            predicate=lambda row, source_name=source_name: row.get("source_name")
            == source_name,
        )
        package_path = binding.get("package_path")
        if not isinstance(package_path, str) or package_path not in descriptors:
            raise ContractError(f"core source {source_name} is not manifest-covered")
        value = core_values[source_name]
        if not isinstance(value, Mapping):
            raise ContractError(f"core source {source_name} is not an object")
        node_id = f"core:{source_name}"
        core_node_ids[source_name] = node_id
        nodes.append(
            {
                "node_id": node_id,
                "node_kind": "committed_reducer_core",
                "source_name": source_name,
                "package_descriptor": copy.deepcopy(descriptors[package_path]),
                "source_binding": binding,
                "payload": copy.deepcopy(dict(value)),
                "payload_digest": canonical_digest(value),
            }
        )
        _add_edge(
            edges,
            root_node_id,
            node_id,
            "manifest_contains_verified_artifact",
        )
        _add_edge(
            edges,
            index_node_id,
            node_id,
            "index_binds_core_artifact",
        )

    semantic_bindings = source_index.get("semantic_role_bindings")
    receipt_node_ids: dict[str, str] = {}
    mandatory_role_node_ids: list[str] = []
    required_role_keys: list[str] = []
    for role, role_index, expected_operator in _MANDATORY_SEMANTIC_ROLES:
        role_key = _role_key(role, role_index)
        required_role_keys.append(role_key)
        binding = _one_binding(
            semantic_bindings,
            label=f"semantic role {role_key}",
            predicate=lambda row, role=role, role_index=role_index: (
                row.get("semantic_role") == role
                and row.get("role_index") == role_index
            ),
        )
        if binding.get("availability") != "available":
            raise ContractError(_UNAVAILABLE_ROLE_PREFIX + role_key)
        package_path = binding.get("package_path")
        original_path = binding.get("original_sealed_path")
        if (
            not isinstance(package_path, str)
            or package_path not in descriptors
            or not isinstance(original_path, str)
            or original_path not in descriptors
        ):
            raise ContractError(f"semantic role {role_key} is not manifest-covered")
        payload = sources.semantic_payloads.get((role, role_index))
        if not isinstance(payload, Mapping):
            raise ContractError(
                f"committed loader did not reopen mandatory semantic role {role_key}"
            )

        role_node_id = f"role:{role_key}"
        original_node_id = f"original-role-artifact:{role_key}"
        mandatory_role_node_ids.append(role_node_id)
        producer_binding: dict[str, Any] | None
        if expected_operator is None:
            if (
                binding.get("source_kind") != "external_role_artifact"
                or any(
                    binding.get(field) is not None
                    for field in (
                        "producer_receipt_id",
                        "producer_request_id",
                        "producer_operator_id",
                        "producer_descriptor",
                    )
                )
            ):
                raise ContractError(
                    f"external mandatory role {role_key} acquired producer metadata"
                )
            producer_binding = None
        else:
            receipt_id = binding.get("producer_receipt_id")
            candidates = sources.producers_by_role.get(role, ())
            receipts = [
                copy.deepcopy(dict(row))
                for row in candidates
                if isinstance(row, Mapping) and row.get("receipt_id") == receipt_id
            ]
            if len(receipts) != 1:
                raise ContractError(
                    f"mandatory role {role_key} lacks its exact reopened producer"
                )
            receipt = receipts[0]
            operator = receipt.get("operator")
            if (
                not isinstance(receipt_id, str)
                or not isinstance(operator, Mapping)
                or operator.get("operator_id") != expected_operator
                or binding.get("producer_operator_id") != expected_operator
                or receipt.get("status") != "succeeded"
            ):
                raise ContractError(
                    f"mandatory role {role_key} crossed its producer contract"
                )
            receipt_node_id = receipt_node_ids.get(receipt_id)
            if receipt_node_id is None:
                receipt_node_id = f"producer-receipt:{receipt_id}"
                receipt_node_ids[receipt_id] = receipt_node_id
                nodes.append(
                    {
                        "node_id": receipt_node_id,
                        "node_kind": "validated_successful_producer_receipt",
                        "receipt_id": receipt_id,
                        "payload": receipt,
                        "payload_digest": canonical_digest(receipt),
                    }
                )
                _add_edge(
                    edges,
                    core_node_ids["operator_evidence"],
                    receipt_node_id,
                    "operator_evidence_contains_validated_receipt",
                )
            _add_edge(
                edges,
                receipt_node_id,
                original_node_id,
                "successful_receipt_binds_original_output",
            )
            _add_edge(
                edges,
                receipt_node_id,
                role_node_id,
                "successful_receipt_binds_verified_package_copy",
            )
            producer_binding = {
                "receipt_id": receipt_id,
                "request_id": binding.get("producer_request_id"),
                "operator_id": binding.get("producer_operator_id"),
                "output_descriptor": copy.deepcopy(
                    binding.get("producer_descriptor")
                ),
            }

        nodes.extend(
            [
                {
                    "node_id": original_node_id,
                    "node_kind": "original_sealed_role_artifact",
                    "semantic_role": role,
                    "role_index": role_index,
                    "manifest_descriptor": copy.deepcopy(
                        descriptors[original_path]
                    ),
                },
                {
                    "node_id": role_node_id,
                    "node_kind": "mandatory_semantic_role",
                    "semantic_role": role,
                    "role_index": role_index,
                    "source_kind": binding.get("source_kind"),
                    "package_descriptor": copy.deepcopy(
                        descriptors[package_path]
                    ),
                    "original_descriptor": copy.deepcopy(
                        descriptors[original_path]
                    ),
                    "source_binding": binding,
                    "producer_binding": producer_binding,
                    "payload": copy.deepcopy(dict(payload)),
                    "payload_digest": canonical_digest(payload),
                },
            ]
        )
        _add_edge(
            edges,
            root_node_id,
            original_node_id,
            "manifest_contains_original_role_artifact",
        )
        _add_edge(
            edges,
            root_node_id,
            role_node_id,
            "manifest_contains_verified_artifact",
        )
        _add_edge(
            edges,
            index_node_id,
            role_node_id,
            "index_binds_mandatory_semantic_role",
        )
        _add_edge(
            edges,
            role_node_id,
            original_node_id,
            "package_payload_is_exact_copy_of_original_role_bytes",
        )

    nodes.sort(key=lambda row: str(row["node_id"]))
    edges.sort(
        key=lambda row: (row["from"], row["to"], row["relation"])
    )
    _require_graph_reachability(
        nodes,
        edges,
        root_node_id=root_node_id,
        mandatory_role_node_ids=mandatory_role_node_ids,
    )
    graph: dict[str, Any] = {
        "schema_version": "1.0.0",
        "contract_version": CANONICAL_ROLE_GRAPH_CONTRACT_VERSION,
        "graph_kind": "committed_canonical_projection_role_evidence",
        "target_id": store.target_id,
        "run_id": store.run_id,
        "verified_theory_generation": commit.generation,
        "root_node_id": root_node_id,
        "required_role_keys": required_role_keys,
        "nodes": nodes,
        "edges": edges,
        "authority_boundary": {
            "source_authority": "one verified immutable discovery commit only",
            "caller_role_payload_authority": None,
            "registry_metadata_as_role_evidence": None,
            "missing_role_synthesis_authority": None,
            "external_independence_authority": None,
            "truth_authority": None,
            "novelty_authority": None,
            "conceptual_depth_authority": None,
            "physics_result_authority": None,
        },
    }
    graph["graph_digest"] = canonical_digest(graph)
    return graph


def reopen_canonical_role_graph(
    store: DiscoveryTransactionStore,
    verified_theory_generation: int,
) -> CanonicalRoleGraphReopenResult:
    """Reopen one bounded canonical role graph from committed bytes only.

    The function intentionally returns terminal typed outcomes instead of
    inviting callers to catch integrity errors and continue with registry
    defaults.  A valid result contains a fully detached graph.  An unavailable
    or invalid result contains no graph and therefore cannot be used as partial
    role authority.
    """

    if (
        isinstance(verified_theory_generation, bool)
        or not isinstance(verified_theory_generation, int)
        or verified_theory_generation <= 0
    ):
        return _terminal(
            status="invalid",
            reason_code="invalid_verified_theory_generation",
            generation=None,
            failure_class="caller_contract",
            detail="verified theory generation must be a positive integer",
        )
    generation = verified_theory_generation
    if not isinstance(store, DiscoveryTransactionStore):
        return _terminal(
            status="invalid",
            reason_code="invalid_discovery_transaction_store",
            generation=generation,
            failure_class="caller_contract",
            detail="canonical role reopening requires a discovery transaction store",
        )

    try:
        preflight_commit = store.read_verified_commit(generation)
    except StateCorruptionError:
        return _terminal(
            status="invalid",
            reason_code="verified_commit_integrity_failure",
            generation=generation,
            failure_class="state_corruption",
            detail="the selected immutable commit failed verification",
        )
    except ContractError:
        return _terminal(
            status="unavailable",
            reason_code="verified_theory_generation_unavailable",
            generation=generation,
            failure_class="missing_verified_generation",
            detail="the selected verified theory generation is not available",
        )
    except OSError:
        return _terminal(
            status="unavailable",
            reason_code="verified_store_unavailable",
            generation=generation,
            failure_class="store_io",
            detail="the committed discovery store could not be reopened",
        )

    try:
        descriptors = _descriptor_map(preflight_commit)
        required_paths = committed_cycle_projection_artifact_paths(generation)
    except ContractError:
        return _terminal(
            status="invalid",
            reason_code="verified_commit_manifest_invalid",
            generation=generation,
            failure_class="contract_integrity",
            detail="the verified commit does not expose a valid artifact manifest",
        )
    missing_paths = [path for path in required_paths if path not in descriptors]
    if missing_paths:
        return _terminal(
            status="unavailable",
            reason_code="mandatory_projection_package_unavailable",
            generation=generation,
            failure_class="missing_committed_artifact",
            detail=(
                "the verified commit omits "
                f"{len(missing_paths)} mandatory canonical projection artifact(s)"
            ),
        )

    try:
        sources = load_committed_cycle_projection_sources(store, generation)
        graph = _build_graph(store, preflight_commit, sources)
    except StateCorruptionError:
        return _terminal(
            status="invalid",
            reason_code="committed_role_graph_integrity_failure",
            generation=generation,
            failure_class="state_corruption",
            detail="committed role-graph bytes failed immutable verification",
        )
    except ContractError as exc:
        message = str(exc)
        if message.startswith(_UNAVAILABLE_ROLE_PREFIX):
            return _terminal(
                status="unavailable",
                reason_code="mandatory_role_unavailable",
                generation=generation,
                failure_class="missing_mandatory_role",
                detail=message,
            )
        return _terminal(
            status="invalid",
            reason_code="committed_role_graph_invalid",
            generation=generation,
            failure_class="contract_integrity",
            detail="committed role evidence failed exact cross-binding validation",
        )
    except OSError:
        return _terminal(
            status="unavailable",
            reason_code="verified_store_unavailable",
            generation=generation,
            failure_class="store_io",
            detail="the committed discovery store could not be reopened",
        )

    return _terminal(
        status="valid",
        reason_code="committed_role_graph_reopened",
        generation=generation,
        detail="all mandatory roles were reopened from exact committed evidence",
        graph=graph,
    )
