# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused acceptance tests for the bounded v3 N-to-N+8 storage lane.

The fixtures intentionally use schema-valid v3 roots over opaque producer
placeholders.  They test orchestration, ownership, ordering, and retry—not
contextual experiment correctness.  Role-specific producers and
``validate_world_v3_closure`` remain the authority for the latter.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Any, Mapping

import pytest

import agentic.experiments.world_v3_content_graph_runtime as runtime_module
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
)
from agentic.experiments.content_graph_transactions import (
    ContentGraphTransactionResult,
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    build_committed_object_handle,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.experiments.world_object_roles import (
    WORLD_V3_AUTHORITY_BOUNDARY,
    derive_content_object_edges,
)
from agentic.experiments.world_v3_content_graph_runtime import (
    DESCENDANT_REFLECTION_ROOT_KIND,
    FRESH_PROCESS_CPU_MEASUREMENT_SCOPE,
    FRESH_PROCESS_MEMORY_MEASUREMENT_SCOPE,
    FRESH_PROCESS_RECOVERY_AUTHORITY_BOUNDARY,
    INCOMPLETE_SUPPORT_AUTHORITY_BOUNDARY,
    MAX_WORLD_V3_FRESH_PROCESS_CPU_NS,
    MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS,
    MAX_WORLD_V3_FRESH_PROCESS_NS,
    MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES,
    MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES,
    MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES,
    MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES,
    MAX_WORLD_V3_LANE_COMMITTED_BYTES,
    MAX_WORLD_V3_LANE_COMMITS,
    MAX_WORLD_V3_LANE_LOCAL_OBJECTS,
    MAX_WORLD_V3_RECOVERY_CHILD_PROCESSES,
    MAX_WORLD_V3_RECOVERY_PHASE_NS,
    MAX_WORLD_V3_RECOVERY_TOTAL_NS,
    RECOVERY_AUTHORITY_BOUNDARY,
    WORLD_ORDER,
    FreshProcessRecoveryError,
    GraphStageProduct,
    WorldV3ContentGraphRuntime,
    run_canonical_descendant_experiment_v3,
)
from agentic.state.discovery_transaction import (
    CompareAndSwapError,
    DiscoveryTransactionStore,
    StateCorruptionError,
)


TARGET_ID = "world-v3-runtime-target"
RUN_ID = "world-v3-runtime-run"
PROGRAMME_ID = "world-v3-runtime-programme"
BRANCH_ID = "root"
DIGEST = "sha256:" + "a" * 64


def _state(generation: int, *, marker: str) -> dict[str, Any]:
    return {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "generation": generation,
        "programme_id": PROGRAMME_ID,
        "marker": marker,
    }


def _stage_path(generation: int, label: str) -> str:
    return (
        f"branches/{BRANCH_ID}/world-v3/g{generation}/objects/{label}.json"
    )


def _theory_path(label: str) -> str:
    return f"branches/{BRANCH_ID}/theory/g1/objects/{label}.json"


def _fake_theory_object(
    object_kind: str,
    label: str,
) -> PreparedContentObject:
    """Create exact bytes with a typed storage role but no semantic claim."""

    return prepare_content_object(
        object_kind=object_kind,
        value={"opaque_producer_fixture": label},
        path=_theory_path(label),
    )


def _base(object_kind: str, contract_version: str) -> dict[str, Any]:
    return {
        "schema_version": "3.0.0",
        "contract_version": contract_version,
        "object_kind": object_kind,
        "authority_boundary": dict(WORLD_V3_AUTHORITY_BOUNDARY),
    }


def _entry(world_id: str, object_ref: Mapping[str, Any]) -> dict[str, Any]:
    return {"world_id": world_id, "object_ref": dict(object_ref)}


def _commit_theory(
    root: Path,
) -> tuple[
    DiscoveryTransactionStore,
    ContentGraphTransactionResult,
    tuple[PreparedContentObject, ...],
    dict[str, PreparedContentObject],
]:
    store = DiscoveryTransactionStore(
        root,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )
    named: dict[str, PreparedContentObject] = {
        "literature": _fake_theory_object(
            "literature_production_input_bundle", "literature"
        ),
        "projection": _fake_theory_object(
            "world_projection_index_v3", "projection"
        ),
        "commission": _fake_theory_object(
            "world_matrix_commission_v3", "commission"
        ),
        "commission_binding": _fake_theory_object(
            "causal_materializer_binding_header_v3", "commission-binding"
        ),
        "certificate_binding": _fake_theory_object(
            "causal_materializer_binding_header_v3", "certificate-binding"
        ),
    }
    for ordinal, world_id in enumerate(WORLD_ORDER):
        named[f"request_{ordinal}"] = _fake_theory_object(
            "world_request_v3", f"request-{world_id}"
        )
        named[f"request_binding_{ordinal}"] = _fake_theory_object(
            "causal_materializer_binding_header_v3",
            f"request-binding-{world_id}",
        )
        named[f"observation_binding_{ordinal}"] = _fake_theory_object(
            "causal_materializer_binding_header_v3",
            f"observation-binding-{world_id}",
        )
        named[f"result_binding_{ordinal}"] = _fake_theory_object(
            "causal_materializer_binding_header_v3",
            f"result-binding-{world_id}",
        )
        named[f"reflection_binding_{ordinal}"] = _fake_theory_object(
            "causal_materializer_binding_header_v3",
            f"reflection-binding-{world_id}",
        )
    objects = tuple(
        sorted(named.values(), key=lambda row: str(row.ref["object_id"]))
    )
    object_ids = [str(row.ref["object_id"]) for row in objects]
    graph = build_content_object_graph(
        local_descriptors=[row.descriptor for row in objects],
        imported_handles=[],
        ordered_roots=object_ids,
        edges=[],
        topological_order=object_ids,
    )
    transaction = prepare_content_graph_transaction(
        expected_generation=0,
        state=_state(1, marker="theory-N"),
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 0),
        graph_artifact_path=f"branches/{BRANCH_ID}/theory/g1/graph.json",
        graph=graph,
        local_objects=objects,
    )
    result = commit_content_graph_transaction(
        store=store,
        transaction=transaction,
    )
    return store, result, objects, named


def _anchor_product(
    named: Mapping[str, PreparedContentObject],
    *,
    anchor_id: str = "anchor.fixture",
) -> tuple[GraphStageProduct, PreparedContentObject]:
    generation = 2
    payload = {
        **_base(
            "world_matrix_anchor_root_v3",
            "experiment-world-anchor-root/3.0.0",
        ),
        "anchor_id": anchor_id,
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "prior_state_version": 0,
        "literature_input_ref": dict(named["literature"].ref),
        "projection_index_ref": dict(named["projection"].ref),
        "commission_ref": dict(named["commission"].ref),
        "commission_materializer_binding_ref": dict(
            named["commission_binding"].ref
        ),
        "world_requests": [
            _entry(world_id, named[f"request_{ordinal}"].ref)
            for ordinal, world_id in enumerate(WORLD_ORDER)
        ],
        "world_request_materializer_bindings": [
            _entry(world_id, named[f"request_binding_{ordinal}"].ref)
            for ordinal, world_id in enumerate(WORLD_ORDER)
        ],
        "world_order": list(WORLD_ORDER),
    }
    root = prepare_content_object(
        object_kind="world_matrix_anchor_root_v3",
        value=payload,
        path=_stage_path(generation, "anchor"),
    )
    return (
        GraphStageProduct(
            state=_state(generation, marker="anchor-N+1"),
            local_objects=(root,),
            root_object_id=str(root.ref["object_id"]),
        ),
        root,
    )


def _world_products(
    named: Mapping[str, PreparedContentObject],
    anchor_ref: Mapping[str, Any],
    *,
    first_envelope_id: str = "envelope.no_probe",
) -> tuple[dict[str, GraphStageProduct], dict[str, PreparedContentObject]]:
    products: dict[str, GraphStageProduct] = {}
    envelopes: dict[str, PreparedContentObject] = {}
    parent_ref = dict(anchor_ref)
    result_statuses = {
        "neutral_inconclusive": "inconclusive",
        "misleading_toy_positive": "scoped_positive",
        "registered_premise_falsifier": "registered_premise_falsified",
        "operational_failure": "operational_failure",
    }
    for ordinal, world_id in enumerate(WORLD_ORDER):
        generation = 3 + ordinal
        request_ref = dict(named[f"request_{ordinal}"].ref)
        local_objects: list[PreparedContentObject] = []
        observation_payload = {
            **_base(
                "world_observation_v3",
                "experiment-world-observation/3.0.0",
            ),
            "observation_id": f"observation.{world_id}",
            "world_id": world_id,
            "world_ordinal": ordinal,
            "commission_ref": dict(named["commission"].ref),
            "request_ref": request_ref,
            "result_effect": "next_cycle_reflection_only",
        }
        if world_id == "no_probe":
            decision = prepare_content_object(
                object_kind="world_no_probe_decision_v3",
                value={
                    **_base(
                        "world_no_probe_decision_v3",
                        "experiment-world-no-probe-decision/3.0.0",
                    ),
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "decision_id": "decision.no_probe",
                    "request_ref": request_ref,
                    "decision_kind": "precommitted_no_probe",
                    "execution_disposition": "not_executed",
                    "source_decision_digest": DIGEST,
                },
                path=_stage_path(generation, "no-probe-decision"),
            )
            local_objects.append(decision)
            observation_payload.update(
                {
                    "observation_kind": "no_probe_decision",
                    "no_probe_decision_ref": dict(decision.ref),
                }
            )
        else:
            result = prepare_content_object(
                object_kind="world_execution_result_v3",
                value={
                    **_base(
                        "world_execution_result_v3",
                        "experiment-world-execution-result/3.0.0",
                    ),
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "result_id": f"result.{world_id}",
                    "request_ref": request_ref,
                    "result_status": result_statuses[world_id],
                    "source_result_digest": DIGEST,
                    "result_effect": "next_cycle_reflection_only",
                },
                path=_stage_path(generation, f"result-{world_id}"),
            )
            reflection = prepare_content_object(
                object_kind="world_next_cycle_reflection_v3",
                value={
                    **_base(
                        "world_next_cycle_reflection_v3",
                        "experiment-world-next-cycle-reflection/3.0.0",
                    ),
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "reflection_id": f"reflection.{world_id}",
                    "result_ref": dict(result.ref),
                    "reflection_disposition": (
                        "pending_next_cycle_reflection_only"
                    ),
                    "source_reflection_digest": DIGEST,
                    "current_cycle_theory_mutation_authorized": False,
                },
                path=_stage_path(generation, f"reflection-{world_id}"),
            )
            local_objects.extend((result, reflection))
            observation_payload.update(
                {
                    "observation_kind": "executed_result_with_reflection",
                    "result_ref": dict(result.ref),
                    "request_materializer_binding_ref": dict(
                        named[f"request_binding_{ordinal}"].ref
                    ),
                    "result_materializer_binding_ref": dict(
                        named[f"result_binding_{ordinal}"].ref
                    ),
                    "reflection_ref": dict(reflection.ref),
                    "reflection_materializer_binding_ref": dict(
                        named[f"reflection_binding_{ordinal}"].ref
                    ),
                }
            )
        observation = prepare_content_object(
            object_kind="world_observation_v3",
            value=observation_payload,
            path=_stage_path(generation, f"observation-{world_id}"),
        )
        local_objects.append(observation)
        payload = {
            **_base(
                "world_observation_envelope_v3",
                "experiment-world-observation-envelope/3.0.0",
            ),
            "envelope_id": (
                first_envelope_id
                if ordinal == 0
                else f"envelope.{world_id}"
            ),
            "world_id": world_id,
            "world_ordinal": ordinal,
            "commission_ref": dict(named["commission"].ref),
            "observation_ref": dict(observation.ref),
            "observation_materializer_binding_ref": dict(
                named[f"observation_binding_{ordinal}"].ref
            ),
            "parent_root_ref": dict(parent_ref),
            "observation_materialization_scope": "typed_observation_storage_only",
            "experiment_execution_implied": False,
        }
        envelope = prepare_content_object(
            object_kind="world_observation_envelope_v3",
            value=payload,
            path=_stage_path(generation, f"envelope-{world_id}"),
        )
        products[world_id] = GraphStageProduct(
            state=_state(generation, marker=f"world-{world_id}"),
            local_objects=tuple((*local_objects, envelope)),
            root_object_id=str(envelope.ref["object_id"]),
        )
        envelopes[world_id] = envelope
        parent_ref = dict(envelope.ref)
    return products, envelopes


def _aggregation_product(
    named: Mapping[str, PreparedContentObject],
    anchor_ref: Mapping[str, Any],
    envelopes: Mapping[str, PreparedContentObject],
) -> GraphStageProduct:
    generation = 8
    certificate = prepare_content_object(
        object_kind="world_matrix_certificate_v3",
        value={
            **_base(
                "world_matrix_certificate_v3",
                "experiment-world-certificate/3.0.0",
            ),
            "certificate_id": "certificate.fixture",
            "commission_ref": dict(named["commission"].ref),
            "observation_envelopes": [
                _entry(world_id, envelopes[world_id].ref)
                for world_id in WORLD_ORDER
            ],
            "world_order": list(WORLD_ORDER),
            "result_effect": "next_cycle_reflection_only",
        },
        path=_stage_path(generation, "certificate"),
    )
    payload = {
        **_base(
            "world_matrix_aggregation_root_v3",
            "experiment-world-aggregation-root/3.0.0",
        ),
        "aggregation_id": "aggregation.fixture",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "anchor_root_ref": dict(anchor_ref),
        "observation_envelopes": [
            _entry(world_id, envelopes[world_id].ref)
            for world_id in WORLD_ORDER
        ],
        "certificate_ref": dict(certificate.ref),
        "certificate_materializer_binding_ref": dict(
            named["certificate_binding"].ref
        ),
        "world_order": list(WORLD_ORDER),
        "result_effect": "next_cycle_reflection_only",
    }
    root = prepare_content_object(
        object_kind="world_matrix_aggregation_root_v3",
        value=payload,
        path=_stage_path(generation, "aggregation"),
    )
    return GraphStageProduct(
        state=_state(generation, marker="aggregation-N+7"),
        local_objects=(certificate, root),
        root_object_id=str(root.ref["object_id"]),
    )


def _reflection_product(
    aggregation: GraphStageProduct,
    *,
    reflection_id: str = "reflection.fixture",
) -> GraphStageProduct:
    generation = 9
    aggregation_root = next(
        row
        for row in aggregation.local_objects
        if row.ref["object_id"] == aggregation.root_object_id
    )
    root = prepare_content_object(
        object_kind=DESCENDANT_REFLECTION_ROOT_KIND,
        value={
            **_base(
                DESCENDANT_REFLECTION_ROOT_KIND,
                "experiment-world-descendant-reflection-root/3.0.0",
            ),
            "reflection_id": reflection_id,
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "aggregation_root_ref": dict(aggregation_root.ref),
            "reflection_disposition": (
                "immutable_input_for_later_theory_reflection"
            ),
            "result_effect": "later_theory_cycle_reflection_input_only",
            "current_cycle_theory_mutation_authorized": False,
            "automatic_theory_selection_authorized": False,
            "proof_authorized": False,
            "physics_authority": False,
        },
        path=_stage_path(generation, "descendant-reflection"),
    )
    return GraphStageProduct(
        state=_state(generation, marker="immutable-reflection-N+8"),
        local_objects=(root,),
        root_object_id=str(root.ref["object_id"]),
    )


def _runtime_fixture(
    tmp_path: Path,
) -> tuple[
    DiscoveryTransactionStore,
    WorldV3ContentGraphRuntime,
    tuple[PreparedContentObject, ...],
    dict[str, PreparedContentObject],
    GraphStageProduct,
    dict[str, GraphStageProduct],
    dict[str, PreparedContentObject],
    GraphStageProduct,
]:
    store, theory_result, theory_objects, named = _commit_theory(
        tmp_path / "store"
    )
    runtime = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
    )
    anchor_product, anchor = _anchor_product(named)
    world_products, envelopes = _world_products(named, anchor.ref)
    aggregation = _aggregation_product(named, anchor.ref, envelopes)
    return (
        store,
        runtime,
        theory_objects,
        named,
        anchor_product,
        world_products,
        envelopes,
        aggregation,
    )


def _graph_at(store: DiscoveryTransactionStore, generation: int) -> dict[str, Any]:
    commit = store.read_verified_commit(generation)
    graph_paths = [
        row["path"]
        for row in commit.manifest["artifacts"]
        if row["path"].endswith("/graph.json")
    ]
    assert len(graph_paths) == 1
    _verified, artifacts = store.read_verified_artifacts(
        generation,
        graph_paths,
    )
    value = json.loads(artifacts[graph_paths[0]].decode("utf-8"))
    assert isinstance(value, dict)
    return value


def _complete_lane(
    runtime: WorldV3ContentGraphRuntime,
    *,
    anchor: GraphStageProduct,
    worlds: Mapping[str, GraphStageProduct],
    aggregation: GraphStageProduct,
) -> ContentGraphTransactionResult:
    runtime.commit_anchor(anchor)
    for world_id in reversed(WORLD_ORDER):
        runtime.submit_world_product(world_id, worlds[world_id])
    prefix = runtime.commit_ready_prefix()
    assert prefix.complete
    outcome = runtime.commit_aggregation(aggregation)
    assert outcome.result is not None
    return outcome.result


def _commit_invalid_n_plus_1(
    *,
    store: DiscoveryTransactionStore,
    graph_path: str,
    programme_id: str = PROGRAMME_ID,
) -> None:
    auxiliary = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"storage_only_adversary": True},
        path=_stage_path(2, "invalid-root"),
    )
    graph = build_content_object_graph(
        local_descriptors=[auxiliary.descriptor],
        imported_handles=[],
        ordered_roots=[str(auxiliary.ref["object_id"])],
        edges=[],
        topological_order=[str(auxiliary.ref["object_id"])],
    )
    state = _state(2, marker="invalid-N+1")
    state["programme_id"] = programme_id
    transaction = prepare_content_graph_transaction(
        expected_generation=1,
        state=state,
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 1),
        graph_artifact_path=graph_path,
        graph=graph,
        local_objects=(auxiliary,),
    )
    commit_content_graph_transaction(store=store, transaction=transaction)


def _topological_order(
    object_ids: set[str],
    edges: list[dict[str, str]],
) -> list[str]:
    incoming = {object_id: 0 for object_id in object_ids}
    outgoing = {object_id: [] for object_id in object_ids}
    for edge in edges:
        source = edge["source_object_id"]
        target = edge["target_object_id"]
        incoming[target] += 1
        outgoing[source].append(target)
    ready = sorted(
        object_id for object_id, count in incoming.items() if count == 0
    )
    ordered: list[str] = []
    while ready:
        source = ready.pop(0)
        ordered.append(source)
        for target in sorted(outgoing[source]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    assert len(ordered) == len(object_ids)
    return ordered


def _write_fake_worker(
    path: Path,
    *,
    interpreter: str,
    body: str,
) -> Path:
    path.write_text(
        f"#!{interpreter}\n{body}\n",
        encoding="utf-8",
    )
    path.chmod(0o700)
    return path


def _identity_attack_worker_body(field: str) -> str:
    return f"""
import copy
import hashlib
import json
import os
import sys

def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

request = json.load(sys.stdin)
output = {{
    "schema_version": "1.0.0",
    "output_kind": "world_v3_fresh_process_recovery",
    "protocol_version": request["protocol_version"],
    "request_digest": request["request_digest"],
    "request_nonce": request["request_nonce"],
    "executable_identity": copy.deepcopy(request["executable_identity"]),
    "worker_module_identity": copy.deepcopy(
        request["worker_module_identity"]
    ),
    "environment_identity": copy.deepcopy(
        request["environment_identity"]
    ),
    "process_identity": {{
        "pid": os.getpid(),
        "parent_pid": os.getppid(),
        "process_group_id": os.getpgrp(),
        "session_id": os.getsid(0),
    }},
    "worker_cwd": request["worker_cwd"],
    "store_identity": {{
        "root": request["store_root"],
        "target_id": request["target_id"],
        "run_id": request["run_id"],
        "theory_generation": request["theory_generation"],
        "theory_result_digest": request["theory_result_digest"],
        "head_generation": request["theory_generation"],
    }},
    "relocation_identity": copy.deepcopy(request["relocation_identity"]),
    "recovered_commit_count": 1,
    "recovered_local_object_count": 0,
    "recovered_committed_payload_bytes": 0,
    "lane_digest": "sha256:" + "0" * 64,
    "owner_catalog_count": 0,
    "owner_catalog_digest": "sha256:" + "0" * 64,
    "world_generations": [],
    "aggregation_result_digest": None,
    "in_process_recovery": {{}},
}}
if {field!r} == "request_digest":
    output["request_digest"] = "sha256:" + "1" * 64
else:
    output["executable_identity"]["sha256"] = "sha256:" + "2" * 64
output["output_digest"] = "sha256:" + hashlib.sha256(
    canonical(output)
).hexdigest()
sys.stdout.buffer.write(canonical(output))
"""


@pytest.mark.expensive
def test_parallel_completion_commits_exact_n_to_n_plus_7_direct_owner_route(
    tmp_path: Path,
) -> None:
    (
        store,
        runtime,
        theory_objects,
        named,
        anchor_product,
        world_products,
        envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path)
    anchor_result = runtime.commit_anchor(anchor_product)
    assert anchor_result.generation == 2

    # A five-party barrier makes this test fail if the runtime ever replaces
    # parallel completion with sequential producer invocation.
    barrier = threading.Barrier(len(WORLD_ORDER))

    def producer(world_id: str):
        def run() -> GraphStageProduct:
            barrier.wait(timeout=5)
            return world_products[world_id]

        return run

    parallel = runtime.run_world_producers(
        {world_id: producer(world_id) for world_id in WORLD_ORDER}
    )
    assert parallel.failures == ()
    assert parallel.prefix.complete
    assert [row.world_id for row in parallel.prefix.committed_worlds] == list(
        WORLD_ORDER
    )
    assert [row.generation for row in parallel.prefix.committed_worlds] == [
        3,
        4,
        5,
        6,
        7,
    ]

    aggregation_commit = runtime.commit_aggregation(aggregation)
    assert aggregation_commit.committed
    assert aggregation_commit.incomplete_support is None
    assert aggregation_commit.result is not None
    assert aggregation_commit.result.generation == 8
    assert store.current_generation() == 8

    # Every predecessor is imported from the commit that locally owns it.  No
    # later graph re-exports an anchor or sibling on another object's behalf.
    for ordinal, world_id in enumerate(WORLD_ORDER):
        graph = _graph_at(store, 3 + ordinal)
        sources = {
            row["object_ref"]["object_id"]: row["source_commit_reference"][
                "generation"
            ]
            for row in graph["imported_handles"]
        }
        expected_parent_id = (
            anchor_result.root_refs[0]["object_id"]
            if ordinal == 0
            else envelopes[WORLD_ORDER[ordinal - 1]].ref["object_id"]
        )
        assert sources[expected_parent_id] == 2 + ordinal
        assert sources[named["commission"].ref["object_id"]] == 1
        assert (
            sources[named[f"observation_binding_{ordinal}"].ref["object_id"]]
            == 1
        )

    aggregation_graph = _graph_at(store, 8)
    aggregation_sources = {
        row["object_ref"]["object_id"]: row["source_commit_reference"][
            "generation"
        ]
        for row in aggregation_graph["imported_handles"]
    }
    assert aggregation_sources[anchor_result.root_refs[0]["object_id"]] == 2
    for ordinal, world_id in enumerate(WORLD_ORDER):
        assert (
            aggregation_sources[envelopes[world_id].ref["object_id"]]
            == 3 + ordinal
        )
    assert aggregation_sources[named["certificate_binding"].ref["object_id"]] == 1
    assert len(runtime.owner_catalog) == (
        len(theory_objects)
        + len(anchor_product.local_objects)
        + sum(
            len(world_products[world_id].local_objects)
            for world_id in WORLD_ORDER
        )
        + len(aggregation.local_objects)
    )

    # The executed-world graph includes the local result -> reflection ->
    # observation chain, proving that non-root role objects contribute their
    # own payload-derived edges rather than acting as opaque sidecars.
    executed_graph = _graph_at(store, 4)
    executed_edges = {
        (
            row["source_object_id"],
            row["target_object_id"],
            row["edge_kind"],
        )
        for row in executed_graph["edges"]
    }
    executed_product = world_products["neutral_inconclusive"]
    by_kind = {
        row.ref["object_kind"]: row for row in executed_product.local_objects
    }
    assert (
        by_kind["world_execution_result_v3"].ref["object_id"],
        by_kind["world_next_cycle_reflection_v3"].ref["object_id"],
        "semantic_derivation",
    ) in executed_edges
    assert (
        by_kind["world_next_cycle_reflection_v3"].ref["object_id"],
        by_kind["world_observation_v3"].ref["object_id"],
        "semantic_derivation",
    ) in executed_edges


@pytest.mark.expensive
def test_partial_completion_is_typed_and_aggregation_cannot_cross_gap(
    tmp_path: Path,
) -> None:
    (
        store,
        runtime,
        _theory_objects,
        named,
        anchor_product,
        world_products,
        _envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path)
    runtime.commit_anchor(anchor_product)

    def failed_no_probe() -> GraphStageProduct:
        raise RuntimeError("bounded producer failure")

    producers = {
        "no_probe": failed_no_probe,
        **{
            world_id: (lambda product=world_products[world_id]: product)
            for world_id in WORLD_ORDER[1:]
        },
    }
    outcome = runtime.run_world_producers(producers)
    assert [failure.world_id for failure in outcome.failures] == ["no_probe"]
    assert outcome.prefix.committed_worlds == ()
    incomplete = outcome.prefix.incomplete_support
    assert incomplete is not None
    assert incomplete.committed_world_ids == ()
    assert incomplete.ready_but_blocked_world_ids == WORLD_ORDER[1:]
    assert incomplete.not_ready_world_ids == ("no_probe",)
    assert incomplete.failed_world_ids == ("no_probe",)
    assert incomplete.next_world_id == "no_probe"
    assert incomplete.next_expected_generation == 3
    assert incomplete.authority_boundary == INCOMPLETE_SUPPORT_AUTHORITY_BOUNDARY
    assert canonical_json(incomplete.as_dict())
    assert store.current_generation() == 2

    blocked = runtime.commit_aggregation(
        aggregation,
        failed_world_ids=("no_probe",),
    )
    assert not blocked.committed
    assert blocked.result is None
    assert blocked.incomplete_support == incomplete
    assert store.current_generation() == 2

    # Selective retry of only the missing prefix member releases all already
    # retained siblings in one deterministic serial prefix.
    runtime.submit_world_product("no_probe", world_products["no_probe"])
    recovered = runtime.commit_ready_prefix()
    assert recovered.complete
    assert [row.generation for row in recovered.committed_worlds] == [
        3,
        4,
        5,
        6,
        7,
    ]


@pytest.mark.expensive
def test_exact_retry_is_byte_identical_and_conflicting_cas_loser_isolated(
    tmp_path: Path,
) -> None:
    store, theory_result, theory_objects, named = _commit_theory(
        tmp_path / "store"
    )
    first = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
    )
    exact_retry = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
    )
    conflicting_loser = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
    )
    anchor_product, anchor = _anchor_product(named)

    winning = first.commit_anchor(anchor_product)
    retried = exact_retry.commit_anchor(anchor_product)
    assert retried == winning
    assert canonical_json(retried.as_dict()) == canonical_json(winning.as_dict())
    assert store.current_generation() == 2

    conflict, _different_anchor = _anchor_product(
        named,
        anchor_id="anchor.conflicting-cas-loser",
    )
    with pytest.raises(CompareAndSwapError):
        conflicting_loser.commit_anchor(conflict)
    assert conflicting_loser.anchor_result is None
    assert store.current_generation() == 2

    worlds, _envelopes = _world_products(named, anchor.ref)
    first.submit_world_product("no_probe", worlds["no_probe"])
    initial_prefix = first.commit_ready_prefix()
    initial_receipt = initial_prefix.committed_worlds[0].result
    first.submit_world_product("no_probe", worlds["no_probe"])
    retried_prefix = first.commit_ready_prefix()
    assert retried_prefix.committed_worlds[0].result == initial_receipt
    assert canonical_json(
        retried_prefix.committed_worlds[0].result.as_dict()
    ) == canonical_json(initial_receipt.as_dict())
    assert store.current_generation() == 3


@pytest.mark.expensive
def test_later_ready_world_cannot_fabricate_or_substitute_predecessor(
    tmp_path: Path,
) -> None:
    (
        store,
        runtime,
        _theory_objects,
        named,
        anchor_product,
        original_worlds,
        _envelopes,
        _aggregation,
    ) = _runtime_fixture(tmp_path)
    anchor_result = runtime.commit_anchor(anchor_product)

    # The later product is completed against the original no-probe envelope.
    # A different valid no-probe product is then committed.  Generation N+3
    # must remain absent because the later product cannot substitute that root.
    alternative_worlds, _alternative_envelopes = _world_products(
        named,
        anchor_result.root_refs[0],
        first_envelope_id="envelope.alternative-no-probe",
    )
    runtime.submit_world_product(
        "neutral_inconclusive",
        original_worlds["neutral_inconclusive"],
    )
    partial = runtime.commit_ready_prefix()
    assert partial.committed_worlds == ()
    assert partial.incomplete_support is not None
    assert partial.incomplete_support.ready_but_blocked_world_ids == (
        "neutral_inconclusive",
    )

    runtime.submit_world_product("no_probe", alternative_worlds["no_probe"])
    with pytest.raises(
        ContractError,
        match="exact committed predecessor",
    ):
        runtime.commit_ready_prefix()
    assert [row.world_id for row in runtime.committed_worlds] == ["no_probe"]
    assert store.current_generation() == 3


@pytest.mark.expensive
def test_unreachable_extra_local_object_is_rejected_before_anchor_commit(
    tmp_path: Path,
) -> None:
    (
        store,
        runtime,
        _theory_objects,
        named,
        anchor_product,
        _world_products,
        _envelopes,
        _aggregation,
    ) = _runtime_fixture(tmp_path)
    extra = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"unreferenced": True},
        path=_stage_path(2, "unreachable-extra"),
    )
    smuggled = GraphStageProduct(
        state=anchor_product.state,
        local_objects=(*anchor_product.local_objects, extra),
        root_object_id=anchor_product.root_object_id,
    )
    with pytest.raises(ContractError, match="outside root closure"):
        runtime.commit_anchor(smuggled)
    assert runtime.anchor_result is None
    assert store.current_generation() == 1

    # Content identity is path-free.  Re-preparing a theory-owned object under
    # a stage path must not let the stage claim a second direct owner.
    theory_literature = named["literature"]
    reowned_literature = prepare_content_object(
        object_kind=str(theory_literature.ref["object_kind"]),
        value=theory_literature.value,
        path=_stage_path(2, "reowned-literature"),
    )
    assert reowned_literature.ref == theory_literature.ref
    reowned = GraphStageProduct(
        state=anchor_product.state,
        local_objects=(*anchor_product.local_objects, reowned_literature),
        root_object_id=anchor_product.root_object_id,
    )
    with pytest.raises(ContractError, match="already has a committed direct owner"):
        runtime.commit_anchor(reowned)
    assert runtime.anchor_result is None
    assert store.current_generation() == 1

    # Neither rejected proposal poisons the coordinator: the original exact
    # anchor remains retryable and becomes the sole N+1 commit.
    committed = runtime.commit_anchor(anchor_product)
    assert committed.generation == 2
    assert store.current_generation() == 2


@pytest.mark.expensive
def test_complete_lane_recovers_after_relocation_in_a_fresh_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (
        store,
        runtime,
        theory_objects,
        _named,
        anchor,
        worlds,
        _envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path)
    expected_aggregation = _complete_lane(
        runtime,
        anchor=anchor,
        worlds=worlds,
        aggregation=aggregation,
    )
    theory_result = runtime.theory_result
    source = store.root
    relocated = tmp_path / "relocated-store"
    shutil.copytree(source, relocated)
    shutil.rmtree(source)
    assert not source.exists()

    relocated_store = DiscoveryTransactionStore(
        relocated,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )
    recovered = WorldV3ContentGraphRuntime.recover(
        store=relocated_store,
        theory_generation=1,
        theory_result=theory_result,
    )
    assert recovered.aggregation_result == expected_aggregation
    assert [row.generation for row in recovered.committed_worlds] == [
        3,
        4,
        5,
        6,
        7,
    ]
    assert len(recovered.owner_catalog) == len(runtime.owner_catalog)
    assert len(recovered.owner_catalog) > len(theory_objects)

    receipt = recovered.recovery_measurement
    assert receipt is not None
    assert receipt.commit_count == MAX_WORLD_V3_LANE_COMMITS
    assert receipt.local_object_count <= MAX_WORLD_V3_LANE_LOCAL_OBJECTS
    assert receipt.committed_payload_bytes <= MAX_WORLD_V3_LANE_COMMITTED_BYTES
    assert (
        receipt.child_processes_spawned
        == MAX_WORLD_V3_RECOVERY_CHILD_PROCESSES
        == 0
    )
    assert 0 < receipt.cold_recovery_elapsed_ns <= MAX_WORLD_V3_RECOVERY_PHASE_NS
    assert 0 < receipt.warm_reopen_elapsed_ns <= MAX_WORLD_V3_RECOVERY_PHASE_NS
    assert 0 < receipt.uncached_replay_elapsed_ns <= MAX_WORLD_V3_RECOVERY_PHASE_NS
    assert (
        receipt.total_recovery_elapsed_ns
        == receipt.cold_recovery_elapsed_ns
        + receipt.warm_reopen_elapsed_ns
        + receipt.uncached_replay_elapsed_ns
    )
    assert receipt.total_recovery_elapsed_ns <= MAX_WORLD_V3_RECOVERY_TOTAL_NS
    assert receipt.exact_warm_reopen
    assert receipt.exact_uncached_replay
    assert receipt.authority_boundary == RECOVERY_AUTHORITY_BOUNDARY
    receipt_data = receipt.as_dict()
    receipt_digest = receipt_data.pop("receipt_digest")
    assert receipt_digest == canonical_digest(receipt_data)

    retried = recovered.commit_aggregation(aggregation)
    assert retried.result == expected_aggregation
    assert canonical_json(retried.result.as_dict()) == canonical_json(
        expected_aggregation.as_dict()
    )
    assert relocated_store.current_generation() == 8

    monkeypatch.setenv(
        "WORLD_V3_PARENT_ONLY_SECRET",
        "must-not-cross-the-scrubbed-boundary",
    )
    fresh = WorldV3ContentGraphRuntime.recover_in_fresh_process(
        store=relocated_store,
        theory_generation=1,
        theory_result=theory_result,
        relocated_from=source,
    )
    assert fresh.head_generation == 8
    assert fresh.recovered_commit_count == MAX_WORLD_V3_LANE_COMMITS
    assert fresh.recovered_local_object_count == receipt.local_object_count
    assert (
        fresh.recovered_committed_payload_bytes
        == receipt.committed_payload_bytes
    )
    assert fresh.lane_digest == receipt.lane_digest
    assert fresh.in_process_recovery.lane_digest == receipt.lane_digest
    assert fresh.in_process_recovery.exact_warm_reopen
    assert fresh.in_process_recovery.exact_uncached_replay
    assert 0 < fresh.launch_to_exit_elapsed_ns <= MAX_WORLD_V3_FRESH_PROCESS_NS
    assert (
        fresh.parent_supervision_elapsed_ns
        >= fresh.launch_to_exit_elapsed_ns
    )
    assert 0 <= fresh.child_cpu_elapsed_ns <= MAX_WORLD_V3_FRESH_PROCESS_CPU_NS
    assert (
        0
        < fresh.peak_process_group_rss_bytes
        <= MAX_WORLD_V3_FRESH_PROCESS_RSS_BYTES
    )
    assert fresh.launched_process_count == 1
    assert (
        fresh.peak_observed_process_group_members
        == MAX_WORLD_V3_FRESH_PROCESS_GROUP_MEMBERS
        == 1
    )
    assert fresh.terminal_process_group_members == 0
    assert fresh.returncode == 0
    assert fresh.deadline_ns == MAX_WORLD_V3_FRESH_PROCESS_NS
    assert 0 < fresh.request_bytes <= MAX_WORLD_V3_FRESH_PROCESS_REQUEST_BYTES
    assert 0 < fresh.stdout_bytes <= MAX_WORLD_V3_FRESH_PROCESS_STDOUT_BYTES
    assert fresh.stderr_bytes == 0 < MAX_WORLD_V3_FRESH_PROCESS_STDERR_BYTES
    assert fresh.request_digest.startswith("sha256:")
    assert fresh.worker_output_digest.startswith("sha256:")
    assert fresh.output_payload_digest.startswith("sha256:")
    assert fresh.launch_argv_digest.startswith("sha256:")
    assert fresh.authority_boundary == FRESH_PROCESS_RECOVERY_AUTHORITY_BOUNDARY
    assert (
        fresh.executable_identity["identity_kind"]
        == "python_executable"
    )
    assert (
        fresh.worker_module_identity["identity_kind"]
        == "world_v3_recovery_worker_module"
    )
    assert (
        "WORLD_V3_PARENT_ONLY_SECRET"
        not in fresh.environment_identity["keys"]
    )
    relocation = fresh.relocation_identity
    assert relocation["mode"] == "copy_then_delete_source"
    assert relocation["source_root"] == str(source)
    assert relocation["source_absent_at_launch"] is True
    assert relocation["source_absent_after_exit"] is True
    assert relocation["destination_root"] == str(relocated.resolve())
    assert relocation["destination_present_at_launch"] is True
    assert relocation["destination_present_after_exit"] is True
    assert relocation["verified_lane_digest"] == receipt.lane_digest
    process_identity = fresh.process_identity
    assert (
        process_identity["pid"]
        == process_identity["process_group_id"]
        == process_identity["session_id"]
    )
    assert process_identity["parent_pid"] == os.getpid()
    fresh_data = fresh.as_dict()
    assert fresh_data["cpu_time_unit"] == "nanoseconds"
    assert (
        fresh_data["cpu_measurement_scope"]
        == FRESH_PROCESS_CPU_MEASUREMENT_SCOPE
    )
    assert fresh_data["memory_unit"] == "bytes"
    assert (
        fresh_data["memory_measurement_scope"]
        == FRESH_PROCESS_MEMORY_MEASUREMENT_SCOPE
    )
    fresh_digest = fresh_data.pop("receipt_digest")
    assert fresh_digest == canonical_digest(fresh_data)

    gapped_root = tmp_path / "gapped-store"
    shutil.copytree(relocated, gapped_root)
    gapped_store = DiscoveryTransactionStore(
        gapped_root,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )
    missing = next(
        path
        for path in gapped_store.commits_dir.iterdir()
        if path.name.startswith("generation-000000000004-")
    )
    shutil.rmtree(missing)
    with pytest.raises(StateCorruptionError):
        WorldV3ContentGraphRuntime.recover(
            store=gapped_store,
            theory_generation=1,
            theory_result=theory_result,
        )


def test_fresh_process_supervisor_rejects_timeout_and_protocol_attacks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store, theory_result, _objects, _named = _commit_theory(
        tmp_path / "fresh-process-attack-store"
    )
    real_executable = sys.executable

    timeout_worker = _write_fake_worker(
        tmp_path / "timeout-worker",
        interpreter=real_executable,
        body="import time\ntime.sleep(30)",
    )
    monkeypatch.setattr(
        runtime_module.sys,
        "executable",
        str(timeout_worker),
    )
    real_popen = runtime_module.subprocess.Popen
    timeout_pids = []

    def record_spawn(command, *args, **kwargs):
        process = real_popen(command, *args, **kwargs)
        if command[0] == str(timeout_worker):
            timeout_pids.append(process.pid)
        return process

    # Observe the parent's actual spawn. A 100 ms timeout can terminate the
    # interpreter before it runs a worker-side PID-file handshake.
    monkeypatch.setattr(runtime_module.subprocess, "Popen", record_spawn)
    started = time.monotonic()
    with pytest.raises(
        FreshProcessRecoveryError,
        match="deadline_exceeded",
    ) as timed_out:
        WorldV3ContentGraphRuntime.recover_in_fresh_process(
            store=store,
            theory_generation=1,
            theory_result=theory_result,
            deadline_ns=100_000_000,
        )
    assert timed_out.value.failure_kind == "deadline_exceeded"
    assert time.monotonic() - started < 2.0
    assert len(timeout_pids) == 1
    timeout_pid = timeout_pids[0]
    with pytest.raises(ProcessLookupError):
        os.kill(timeout_pid, 0)

    malformed_worker = _write_fake_worker(
        tmp_path / "malformed-worker",
        interpreter=real_executable,
        body="import sys\nsys.stdin.buffer.read()\nsys.stdout.write('{')",
    )
    monkeypatch.setattr(
        runtime_module.sys,
        "executable",
        str(malformed_worker),
    )
    with pytest.raises(
        FreshProcessRecoveryError,
        match="malformed_output",
    ):
        WorldV3ContentGraphRuntime.recover_in_fresh_process(
            store=store,
            theory_generation=1,
            theory_result=theory_result,
        )

    tamper_worker = _write_fake_worker(
        tmp_path / "tamper-worker",
        interpreter=real_executable,
        body=(
            "import json, sys\n"
            "json.load(sys.stdin)\n"
            "sys.stdout.write(json.dumps("
            "{'output_digest': 'sha256:' + '0' * 64}, "
            "sort_keys=True, separators=(',', ':')))"
        ),
    )
    monkeypatch.setattr(
        runtime_module.sys,
        "executable",
        str(tamper_worker),
    )
    with pytest.raises(
        FreshProcessRecoveryError,
        match="output_tamper",
    ):
        WorldV3ContentGraphRuntime.recover_in_fresh_process(
            store=store,
            theory_generation=1,
            theory_result=theory_result,
        )

    for field, failure_kind in (
        ("request_digest", "request_identity_error"),
        ("executable_identity", "output_identity_error"),
    ):
        identity_worker = _write_fake_worker(
            tmp_path / f"{field}-worker",
            interpreter=real_executable,
            body=_identity_attack_worker_body(field),
        )
        monkeypatch.setattr(
            runtime_module.sys,
            "executable",
            str(identity_worker),
        )
        with pytest.raises(
            FreshProcessRecoveryError,
            match=failure_kind,
        ) as rejected:
            WorldV3ContentGraphRuntime.recover_in_fresh_process(
                store=store,
                theory_generation=1,
                theory_result=theory_result,
            )
        assert rejected.value.failure_kind == failure_kind

    monkeypatch.setattr(
        runtime_module.sys,
        "executable",
        real_executable,
    )
    still_present = tmp_path / "not-deleted-source"
    still_present.mkdir()
    with pytest.raises(
        FreshProcessRecoveryError,
        match="relocation_identity_error",
    ):
        WorldV3ContentGraphRuntime.recover_in_fresh_process(
            store=store,
            theory_generation=1,
            theory_result=theory_result,
            relocated_from=still_present,
        )


@pytest.mark.expensive
def test_partial_recovery_resumes_longest_prefix_and_rejects_head_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (
        store,
        runtime,
        _theory_objects,
        _named,
        anchor,
        worlds,
        _envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path)
    anchor_result = runtime.commit_anchor(anchor)
    runtime.submit_world_product(
        "neutral_inconclusive",
        worlds["neutral_inconclusive"],
    )
    runtime.submit_world_product("no_probe", worlds["no_probe"])
    partial = runtime.commit_ready_prefix()
    assert [row.generation for row in partial.committed_worlds] == [3, 4]
    assert store.current_generation() == 4

    actual_current_generation = store.current_generation
    monkeypatch.setattr(
        store,
        "current_generation",
        lambda: actual_current_generation() + 1,
    )
    with pytest.raises(ContractError, match="head drifted"):
        WorldV3ContentGraphRuntime.recover(
            store=store,
            theory_generation=1,
            theory_result=runtime.theory_result,
        )
    monkeypatch.setattr(store, "current_generation", actual_current_generation)

    recovered = WorldV3ContentGraphRuntime.recover(
        store=store,
        theory_generation=1,
        theory_result=runtime.theory_result,
    )
    assert recovered.commit_anchor(anchor) == anchor_result
    recovered.submit_world_product("no_probe", worlds["no_probe"])
    exact_prefix = recovered.commit_ready_prefix()
    assert [row.generation for row in exact_prefix.committed_worlds] == [3, 4]
    assert store.current_generation() == 4

    for world_id in reversed(WORLD_ORDER[2:]):
        recovered.submit_world_product(world_id, worlds[world_id])
    resumed = recovered.commit_ready_prefix()
    assert resumed.complete
    assert [row.generation for row in resumed.committed_worlds] == [
        3,
        4,
        5,
        6,
        7,
    ]
    aggregate = recovered.commit_aggregation(aggregation)
    assert aggregate.result is not None
    assert aggregate.result.generation == 8
    assert store.current_generation() == 8


@pytest.mark.expensive
def test_recovery_rejects_wrong_identity_paths_roots_and_programmes(
    tmp_path: Path,
) -> None:
    store, theory_result, _objects, _named = _commit_theory(
        tmp_path / "identity-store"
    )
    with pytest.raises(ContractError, match="generation differs"):
        WorldV3ContentGraphRuntime.recover(
            store=store,
            theory_generation=2,
            theory_result=theory_result,
        )
    foreign_store = DiscoveryTransactionStore(
        tmp_path / "foreign-store",
        target_id="foreign-target",
        run_id=RUN_ID,
    )
    with pytest.raises(ContractError, match="cross another target or run"):
        WorldV3ContentGraphRuntime.recover(
            store=foreign_store,
            theory_generation=1,
            theory_result=theory_result,
        )
    other_store, other_result, _other_objects, _other_named = _commit_theory(
        tmp_path / "other-theory-store"
    )
    assert other_store.current_generation() == 1
    assert other_result != theory_result
    with pytest.raises(ContractError, match="explicit theory"):
        WorldV3ContentGraphRuntime.recover(
            store=store,
            theory_generation=1,
            theory_result=other_result,
        )

    adversaries = (
        (
            "wrong-path",
            f"branches/{BRANCH_ID}/not-world-v3/g2/graph.json",
            PROGRAMME_ID,
            "fixed world-v3 graph path",
        ),
        (
            "wrong-root",
            f"branches/{BRANCH_ID}/world-v3/g2/graph.json",
            PROGRAMME_ID,
            "wrong local root kind",
        ),
        (
            "wrong-programme",
            f"branches/{BRANCH_ID}/world-v3/g2/graph.json",
            "cross-programme",
            "programme",
        ),
    )
    for label, graph_path, programme_id, message in adversaries:
        bad_store, bad_theory, _bad_objects, _bad_named = _commit_theory(
            tmp_path / label
        )
        _commit_invalid_n_plus_1(
            store=bad_store,
            graph_path=graph_path,
            programme_id=programme_id,
        )
        with pytest.raises(StateCorruptionError, match=message):
            WorldV3ContentGraphRuntime.recover(
                store=bad_store,
                theory_generation=1,
                theory_result=bad_theory,
            )


def test_recovery_rejects_local_reownership_of_an_imported_anchor(
    tmp_path: Path,
) -> None:
    store, theory_result, theory_objects, named = _commit_theory(
        tmp_path / "reowner-store"
    )
    runtime = WorldV3ContentGraphRuntime(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
    )
    anchor_product, anchor = _anchor_product(named)
    runtime.commit_anchor(anchor_product)
    worlds, _envelopes = _world_products(named, anchor.ref)
    no_probe = worlds["no_probe"]
    reowned_anchor = prepare_content_object(
        object_kind=str(anchor.ref["object_kind"]),
        value=anchor.value,
        path=_stage_path(3, "reowned-anchor"),
    )
    assert reowned_anchor.ref == anchor.ref
    local_objects = tuple(
        sorted(
            (*no_probe.local_objects, reowned_anchor),
            key=lambda row: str(row.ref["object_id"]),
        )
    )
    edges: list[dict[str, str]] = []
    for row in local_objects:
        edges.extend(
            derive_content_object_edges(
                object_ref=row.ref,
                payload=row.value,
            )
        )
    local_ids = {str(row.ref["object_id"]) for row in local_objects}
    theory_refs = {
        str(row.ref["object_id"]): row.ref for row in theory_objects
    }
    imported_ids = sorted(
        {
            edge["source_object_id"]
            for edge in edges
            if edge["source_object_id"] not in local_ids
        }
    )
    imported_handles = [
        build_committed_object_handle(
            source_commit_reference=theory_result.commit_ref,
            object_ref=theory_refs[object_id],
        )
        for object_id in imported_ids
    ]
    all_ids = local_ids | set(imported_ids)
    graph = build_content_object_graph(
        local_descriptors=[row.descriptor for row in local_objects],
        imported_handles=imported_handles,
        ordered_roots=[no_probe.root_object_id],
        edges=edges,
        topological_order=_topological_order(all_ids, edges),
    )
    transaction = prepare_content_graph_transaction(
        expected_generation=2,
        state=no_probe.state,
        namespace=Namespace(TARGET_ID, RUN_ID, BRANCH_ID, 2),
        graph_artifact_path=f"branches/{BRANCH_ID}/world-v3/g3/graph.json",
        graph=graph,
        local_objects=local_objects,
    )
    commit_content_graph_transaction(store=store, transaction=transaction)
    with pytest.raises(StateCorruptionError, match="locally reowns"):
        WorldV3ContentGraphRuntime.recover(
            store=store,
            theory_generation=1,
            theory_result=theory_result,
        )


@pytest.mark.expensive
def test_descendant_reflection_is_mandatory_n_plus_8_and_recovers(
    tmp_path: Path,
) -> None:
    (
        store,
        runtime,
        _theory_objects,
        _named,
        anchor,
        worlds,
        _envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path / "descendant-reflection")
    aggregation_result = _complete_lane(
        runtime,
        anchor=anchor,
        worlds=worlds,
        aggregation=aggregation,
    )
    assert aggregation_result.generation == 8
    reflection = _reflection_product(aggregation)
    committed = runtime.commit_descendant_reflection(reflection)
    assert committed.result.generation == 9
    assert committed.result.root_refs[0]["object_kind"] == (
        DESCENDANT_REFLECTION_ROOT_KIND
    )
    assert store.current_generation() == 9
    assert runtime.commit_descendant_reflection(reflection) == committed

    recovered = WorldV3ContentGraphRuntime.recover(
        store=store,
        theory_generation=1,
        theory_result=runtime.theory_result,
    )
    assert recovered.reflection_result == committed.result
    assert recovered.aggregation_result == aggregation_result
    assert recovered.recovery_measurement is not None
    assert recovered.recovery_measurement.commit_count == 9


def test_descendant_reflection_rejects_a_different_aggregation(
    tmp_path: Path,
) -> None:
    (
        _store,
        runtime,
        _theory_objects,
        _named,
        anchor,
        worlds,
        _envelopes,
        aggregation,
    ) = _runtime_fixture(tmp_path / "wrong-descendant-aggregation")
    _complete_lane(
        runtime,
        anchor=anchor,
        worlds=worlds,
        aggregation=aggregation,
    )
    valid = _reflection_product(aggregation)
    root = valid.local_objects[0]
    forged_value = dict(root.value)
    forged_value["aggregation_root_ref"] = dict(anchor.local_objects[-1].ref)
    forged = prepare_content_object(
        object_kind=DESCENDANT_REFLECTION_ROOT_KIND,
        value=forged_value,
        path=_stage_path(9, "wrong-descendant-aggregation"),
    )
    with pytest.raises(ContractError, match="schema validation|later-cycle boundary"):
        runtime.commit_descendant_reflection(
            GraphStageProduct(
                state=valid.state,
                local_objects=(forged,),
                root_object_id=str(forged.ref["object_id"]),
            )
        )


def test_public_descendant_facade_runs_parallel_and_commits_exact_chronology(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store, theory_result, theory_objects, named = _commit_theory(
        tmp_path / "public-descendant-facade"
    )
    anchor_product, anchor = _anchor_product(named)
    world_products, envelopes = _world_products(named, anchor.ref)
    aggregation = _aggregation_product(named, anchor.ref, envelopes)
    reflection = _reflection_product(aggregation)
    barrier = threading.Barrier(len(WORLD_ORDER))

    def producer(world_id: str):
        def run() -> GraphStageProduct:
            barrier.wait(timeout=5)
            return world_products[world_id]

        return run

    sentinel = object()

    def contextual_boundary(self: WorldV3ContentGraphRuntime) -> object:
        # Contextual semantic replay has its own full-closure tests.  This
        # integration probe isolates the public composition boundary while
        # retaining the real transaction kernel and real concurrent wave.
        assert self.reflection_result is not None
        assert self.reflection_result.generation == self.theory_generation + 8
        assert store.current_generation() == self.theory_generation + 8
        return sentinel

    monkeypatch.setattr(
        WorldV3ContentGraphRuntime,
        "require_active_current_descendant_closure",
        contextual_boundary,
    )
    result = run_canonical_descendant_experiment_v3(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
        anchor_product=anchor_product,
        world_producers={
            world_id: producer(world_id) for world_id in WORLD_ORDER
        },
        aggregation_product=aggregation,
        reflection_product=reflection,
    )
    assert result.anchor.generation == 2
    assert [row.generation for row in result.worlds] == [3, 4, 5, 6, 7]
    assert result.aggregation.generation == 8
    assert result.reflection.generation == 9
    assert result.verified_descendant_closure is sentinel
    assert set(result.parallel_production.completion_order) == set(WORLD_ORDER)
    assert result.parallel_production.failures == ()
