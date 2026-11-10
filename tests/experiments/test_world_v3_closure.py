# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Whole-closure adversaries for the thin world-v3 contextual replay.

These tests construct all fifteen strict domain variants locally and attach
real portable materializer fragments.  The fixture deliberately deletes the
materializer workspaces before validation: only content-object bytes and exact
generation membership survive.  The resulting evidence is a local causal and
storage protocol test, not evidence that any experiment or physics claim is
true.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import pytest

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    stable_identifier,
)
from agentic.discovery.literature_production_commitment import (
    build_portable_literature_production_input_bundle,
)
from agentic.evals.ym_representational_dynamics_20260721.literature_production_chain import (
    build_publication_disabled_literature_production_chain,
)
from agentic.experiments.causal_materializer_content_graph_v3 import (
    prepare_portable_causal_materialization_fragment_v3,
)
from agentic.experiments.causal_producer_runtime_v3 import (
    CausalArtifactMaterializerRuntimeV3,
    snapshot_sealed_causal_materialization_v3,
)
from agentic.experiments.content_graph_transactions import (
    ContentGraphTransactionResult,
    commit_content_graph_transaction,
    prepare_content_graph_transaction,
)
from agentic.experiments.world_object_graph import (
    PreparedContentObject,
    ResolvedContentObject,
    build_committed_object_handle,
    build_content_object_graph,
    prepare_content_object,
)
from agentic.experiments.world_object_roles import (
    WORLD_V3_AUTHORITY_BOUNDARY,
    derive_content_object_edges,
)
from agentic.experiments.world_v3_closure import (
    PROJECTION_COMPONENT_ORDER,
    WORLD_ORDER,
    validate_world_v3_closure,
    validate_world_v3_descendant_closure,
)
from agentic.experiments.world_v3_content_graph_runtime import (
    GraphStageProduct,
    run_canonical_descendant_experiment_v3,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


TARGET_ID = "world-v3-closure-target"
RUN_ID = "world-v3-closure-run"
THEORY_GENERATION = 12
MANIFEST_PATH = "committed/literature-production/manifest.json"


@dataclass(frozen=True)
class ClosureFixture:
    objects: tuple[ResolvedContentObject, ...]
    generations: dict[str, int]
    aggregation_ref: dict[str, Any]
    refs_by_label: dict[str, dict[str, Any]]
    source_roots_removed: bool


def _base(object_kind: str, contract_version: str) -> dict[str, Any]:
    return {
        "schema_version": "3.0.0",
        "contract_version": contract_version,
        "object_kind": object_kind,
        "authority_boundary": dict(WORLD_V3_AUTHORITY_BOUNDARY),
    }


def _world_entry(world_id: str, object_ref: Mapping[str, Any]) -> dict[str, Any]:
    return {"world_id": world_id, "object_ref": copy.deepcopy(dict(object_ref))}


def _minimal_receipt(*, state_version: int, label: str) -> dict[str, Any]:
    """Build one successful, content-derived local receipt fixture.

    The contextual validator uses the receipt only as exact theory ancestry; it
    deliberately does not elevate this fixture into producer independence.
    Even so, the receipt exercises the full successful-receipt contract:
    original and immutable-history artifacts agree byte-for-byte, and a passed
    validator receipt binds an explicit (fixture-only) executable authority.
    """

    namespace = {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "branch_id": "root",
        "state_version": state_version,
    }
    request_digest = canonical_digest(
        {"label": label, "state_version": state_version, "kind": "fixture"}
    )
    request_id = stable_identifier("opreq", request_digest)
    output_value = {
        "label": label,
        "state_version": state_version,
        "fixture_scope": "ancestry-only",
    }
    output_digest = canonical_digest(output_value)
    output_size = len(canonical_json(output_value))
    output_artifact = {
        "path": f"fixture-output/{label}.json",
        "sha256": output_digest,
        "size_bytes": output_size,
        "namespace": namespace,
    }
    invocation_id = stable_identifier("invocation", label, state_version)
    history_artifact = {
        **output_artifact,
        "path": (
            f".discovery-history/{TARGET_ID}/{RUN_ID}/root/"
            f"state-{state_version}/{invocation_id}/attempt-1/outputs/"
            f"{label}.json"
        ),
    }
    validator_id = "world-v3-fixture-receipt-validator"
    validator_version = "1.0.0"
    validator_source_value = {
        "validator_id": validator_id,
        "validator_version": validator_version,
        "fixture_scope": "receipt-shape-and-byte-binding-only",
    }
    validator_source_digest = canonical_digest(validator_source_value)
    validator_source_size = len(canonical_json(validator_source_value))
    validator_snapshot = {
        "path": (
            f".discovery-history/{TARGET_ID}/{RUN_ID}/root/"
            f"state-{state_version}/{invocation_id}/attempt-1/validators/"
            f"{validator_id}/source.json"
        ),
        "sha256": validator_source_digest,
        "size_bytes": validator_source_size,
        "namespace": namespace,
    }
    validator_authority: dict[str, Any] = {
        "schema_version": "1.0.0",
        "binding_kind": "callable",
        "validator_id": validator_id,
        "validator_version": validator_version,
        "runtime_identity": {
            "kind": "callable",
            "callable_id": validator_id,
        },
        "dependency_identities": [],
        "dependency_policy": "declared_only",
        "files": [
            {
                "roles": ["callable_source"],
                "path_scope": "repository_relative",
                "runtime_path": "tests/experiments/test_world_v3_closure.py",
                "sha256": validator_source_digest,
                "size_bytes": validator_source_size,
                "snapshot_descriptor": validator_snapshot,
            }
        ],
        "coverage": {
            "bound": [
                "fixture receipt shape and exact output/history byte identity"
            ],
            "excluded": [
                "undeclared transitive imports beyond explicit dependency paths",
                "scientific truth, independence, and producer authority",
            ],
        },
    }
    validator_authority["authority_digest"] = canonical_digest(
        validator_authority
    )
    validator_receipt: dict[str, Any] = {
        "validator_id": validator_id,
        "validator_version": validator_version,
        "validator_code_digest": validator_authority["authority_digest"],
        "validator_authority": validator_authority,
        "request_id": request_id,
        "input_digest": canonical_digest(
            {"label": label, "state_version": state_version}
        ),
        "started_at": "2026-07-22T10:00:00Z",
        "completed_at": "2026-07-22T10:00:01Z",
        "status": "passed",
        "artifact_digests": [output_digest],
        "output_artifacts": [history_artifact],
    }
    validator_receipt["receipt_digest"] = canonical_digest(
        validator_receipt
    )
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "request_id": request_id,
        "request_digest": request_digest,
        "invocation_id": invocation_id,
        "attempt": 1,
        "operator": {
            "operator_id": "world-v3-fixture-producer",
            "version": "1.0.0",
            "kind": "theory",
        },
        "identity": namespace,
        "required": True,
        "input_digest": validator_receipt["input_digest"],
        "started_at": "2026-07-22T10:00:00Z",
        "completed_at": "2026-07-22T10:00:01Z",
        "duration_seconds": 1.0,
        "status": "succeeded",
        "exit_code": 0,
        "stdout_digest": canonical_digest({"stdout": label}),
        "stderr_digest": canonical_digest({"stderr": ""}),
        "output_artifacts": [output_artifact],
        "output_history_artifacts": [history_artifact],
        "explicit_unknowns": [
            "fixture receipt is not independent producer authority"
        ],
        "validator_receipts": [validator_receipt],
    }
    core_digest = canonical_digest(record)
    record["receipt_id"] = stable_identifier(
        "opreceipt",
        request_id,
        1,
        core_digest,
    )
    record["receipt_digest"] = canonical_digest(record)
    return record


class _FixtureBuilder:
    """Construct one exact closure while deduplicating content-addressed atoms."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.materializer_root = root / "materializer-source"
        self.materializer_root.mkdir(parents=True)
        self.objects: dict[str, ResolvedContentObject] = {}
        self.generations: dict[str, int] = {}
        self.refs_by_label: dict[str, dict[str, Any]] = {}

    def add_prepared(
        self,
        prepared: PreparedContentObject,
        *,
        generation: int,
        label: str | None = None,
    ) -> ResolvedContentObject:
        object_id = str(prepared.ref["object_id"])
        resolved = ResolvedContentObject(
            ref=copy.deepcopy(dict(prepared.ref)),
            value=copy.deepcopy(dict(prepared.value)),
            data=bytes(prepared.data),
        )
        existing = self.objects.get(object_id)
        if existing is not None and (
            existing.ref != resolved.ref
            or existing.value != resolved.value
            or existing.data != resolved.data
        ):
            raise AssertionError("fixture object ID collision")
        self.objects[object_id] = resolved
        self.generations[object_id] = min(
            generation,
            self.generations.get(object_id, generation),
        )
        if label is not None:
            self.refs_by_label[label] = copy.deepcopy(dict(prepared.ref))
        return resolved

    def add(
        self,
        *,
        object_kind: str,
        value: Mapping[str, Any],
        generation: int,
        label: str,
    ) -> ResolvedContentObject:
        prepared = prepare_content_object(
            object_kind=object_kind,
            value=value,
            path=f"world-v3/{label}.json",
        )
        return self.add_prepared(
            prepared,
            generation=generation,
            label=label,
        )

    def materialize(
        self,
        expected: ResolvedContentObject,
        *,
        owner_generation: int,
        label: str,
    ) -> dict[str, Any]:
        """Attach the real path-free materializer protocol for exact bytes."""

        runtime = CausalArtifactMaterializerRuntimeV3(
            workspace=self.materializer_root,
            namespace=Namespace(
                TARGET_ID,
                RUN_ID,
                "root",
                owner_generation,
            ),
        )
        safe_label = label.replace("_", "-")
        sealed = runtime.seal(
            stage_id=f"world-v3-{safe_label}",
            materializer_role="exact-byte-materializer",
            artifact_id=f"artifact-{safe_label}",
            artifact=expected.value,
        )
        snapshot = snapshot_sealed_causal_materialization_v3(
            sealed,
            workspace=self.materializer_root,
        )
        fragment = prepare_portable_causal_materialization_fragment_v3(
            snapshot,
            object_path_prefix=f"portable/{safe_label}",
        )
        for prepared in fragment.local_objects:
            self.add_prepared(prepared, generation=owner_generation)
        self.refs_by_label[f"binding.{label}"] = fragment.binding_root_ref
        return fragment.binding_root_ref


def _build_fixture(root: Path) -> ClosureFixture:
    builder = _FixtureBuilder(root)
    n = THEORY_GENERATION

    manifest_root = root / "literature-source"
    manifest = build_publication_disabled_literature_production_chain(
        execution_started_at="2026-07-22T12:39:01Z"
    )
    manifest_file = manifest_root / MANIFEST_PATH
    manifest_file.parent.mkdir(parents=True)
    manifest_file.write_bytes(canonical_json(manifest) + b"\n")
    literature_value = build_portable_literature_production_input_bundle(
        manifest_root,
        MANIFEST_PATH,
    )
    literature = builder.add(
        object_kind="literature_production_input_bundle",
        value=literature_value,
        generation=n,
        label="literature",
    )

    receipt_n = builder.add(
        object_kind="producer_receipt_evidence",
        value=_minimal_receipt(state_version=n, label="theory-n"),
        generation=n,
        label="receipt-theory-n",
    )
    receipt_prior = builder.add(
        object_kind="producer_receipt_evidence",
        value=_minimal_receipt(state_version=n - 1, label="theory-n-minus-1"),
        generation=n - 1,
        label="receipt-theory-n-minus-1",
    )
    precommit_state = builder.add(
        object_kind="immutable_history_evidence",
        value={
            "schema_version": "1.0.0",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": n - 1,
            "theory_state": "frozen-precommit-state",
        },
        generation=n - 1,
        label="precommit-state",
    )
    ancestor = builder.add(
        object_kind="world_precommit_ancestor_carrier_v3",
        value={
            **_base(
                "world_precommit_ancestor_carrier_v3",
                "experiment-world-precommit-ancestor-carrier/3.0.0",
            ),
            "ancestor_id": "ancestor.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "precommit_state_version": n - 1,
            "ancestry_relation": "committed_generation_N_minus_1",
            "precommit_state_ref": dict(precommit_state.ref),
            "precommit_state_semantic_digest": precommit_state.ref[
                "semantic_digest"
            ],
            "precommit_receipt_ref": dict(receipt_prior.ref),
        },
        generation=n + 1,
        label="ancestor",
    )

    carrier_kinds = (
        "theory_programme",
        "reflection_packet",
        "conceptual_systems",
        "genealogy",
        "registered_claim",
        "generator_authority",
        "adjudication_authority",
        "schedule",
        "experiment_spec_family",
    )
    carriers: dict[str, ResolvedContentObject] = {}
    carrier_sources: dict[str, ResolvedContentObject] = {}
    for carrier_kind in carrier_kinds:
        source = builder.add(
            object_kind="producer_artifact_evidence",
            value={
                "schema_version": "1.0.0",
                "artifact_kind": carrier_kind,
                "target_id": TARGET_ID,
                "run_id": RUN_ID,
                "state_version": n,
                "content": f"exact source for {carrier_kind}",
            },
            generation=n,
            label=f"source-{carrier_kind}",
        )
        carrier = builder.add(
            object_kind="world_theory_carrier_v3",
            value={
                **_base(
                    "world_theory_carrier_v3",
                    "experiment-world-theory-carrier/3.0.0",
                ),
                "carrier_id": f"carrier.{carrier_kind}",
                "carrier_kind": carrier_kind,
                "source_ref": dict(source.ref),
                "source_semantic_digest": source.ref["semantic_digest"],
                "source_receipt_ref": dict(receipt_n.ref),
            },
            generation=n + 1,
            label=f"carrier-{carrier_kind}",
        )
        carrier_sources[carrier_kind] = source
        carriers[carrier_kind] = carrier

    component_payloads: dict[str, ResolvedContentObject] = {
        "committed_ancestor": ancestor,
        "source_authority": literature,
        **{
            kind: carriers[kind]
            for kind in PROJECTION_COMPONENT_ORDER
            if kind not in {"committed_ancestor", "source_authority"}
        },
    }
    components: list[ResolvedContentObject] = []
    for component_kind in PROJECTION_COMPONENT_ORDER:
        components.append(
            builder.add(
                object_kind="world_projection_component_v3",
                value={
                    **_base(
                        "world_projection_component_v3",
                        "experiment-world-projection-component/3.0.0",
                    ),
                    "component_id": f"component.{component_kind}",
                    "component_kind": component_kind,
                    "component_payload_ref": dict(
                        component_payloads[component_kind].ref
                    ),
                },
                generation=n + 1,
                label=f"component-{component_kind}",
            )
        )
    projection = builder.add(
        object_kind="world_projection_index_v3",
        value={
            **_base(
                "world_projection_index_v3",
                "experiment-world-projection-index/3.0.0",
            ),
            "projection_id": "projection.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "prior_state_version": n - 1,
            "components": [
                {
                    "component_kind": component_kind,
                    "object_ref": dict(component.ref),
                }
                for component_kind, component in zip(
                    PROJECTION_COMPONENT_ORDER,
                    components,
                    strict=True,
                )
            ],
        },
        generation=n + 1,
        label="projection",
    )

    adjudication_binding = builder.materialize(
        carrier_sources["adjudication_authority"],
        owner_generation=n + 1,
        label="adjudication-source",
    )
    schedule_binding = builder.materialize(
        carrier_sources["schedule"],
        owner_generation=n + 1,
        label="schedule-source",
    )
    commission = builder.add(
        object_kind="world_matrix_commission_v3",
        value={
            **_base(
                "world_matrix_commission_v3",
                "dynamic-experiment-world-matrix-commission/3.0.0",
            ),
            "commission_id": "commission.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "prior_state_version": n - 1,
            "projection_index_ref": dict(projection.ref),
            "registered_claim_ref": dict(carriers["registered_claim"].ref),
            "spec_family_ref": dict(carriers["experiment_spec_family"].ref),
            "adjudication_materializer_binding_ref": adjudication_binding,
            "schedule_materializer_binding_ref": schedule_binding,
            "world_order": list(WORLD_ORDER),
        },
        generation=n + 1,
        label="commission",
    )

    plans: list[ResolvedContentObject] = []
    requests: list[ResolvedContentObject] = []
    request_bindings: list[dict[str, Any]] = []
    intervention_kinds = (
        "suppress_execution",
        "bounded_resource_cutoff",
        "scoped_positive_fixture",
        "scoped_counterexample_fixture",
        "adapter_operational_failure",
    )
    for ordinal, (world_id, intervention_kind) in enumerate(
        zip(WORLD_ORDER, intervention_kinds, strict=True)
    ):
        disposition = "not_executed" if ordinal == 0 else "executed"
        plan = builder.add(
            object_kind="world_plan_v3",
            value={
                **_base(
                    "world_plan_v3",
                    "experiment-world-plan/3.0.0",
                ),
                "plan_id": f"plan.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "commission_ref": dict(commission.ref),
                "execution_disposition": disposition,
                "intervention_kind": intervention_kind,
                "source_plan_digest": canonical_digest(
                    {"world_id": world_id, "plan": intervention_kind}
                ),
            },
            generation=n + 1,
            label=f"plan-{world_id}",
        )
        request = builder.add(
            object_kind="world_request_v3",
            value={
                **_base(
                    "world_request_v3",
                    "experiment-world-request/3.0.0",
                ),
                "request_id": f"request.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "execution_disposition": disposition,
                "commission_ref": dict(commission.ref),
                "world_plan_ref": dict(plan.ref),
            },
            generation=n + 1,
            label=f"request-{world_id}",
        )
        plans.append(plan)
        requests.append(request)
        request_bindings.append(
            builder.materialize(
                request,
                owner_generation=n + 1,
                label=f"request-{world_id}",
            )
        )

    commission_binding = builder.materialize(
        commission,
        owner_generation=n + 1,
        label="commission",
    )
    anchor = builder.add(
        object_kind="world_matrix_anchor_root_v3",
        value={
            **_base(
                "world_matrix_anchor_root_v3",
                "experiment-world-anchor-root/3.0.0",
            ),
            "anchor_id": "anchor.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "prior_state_version": n - 1,
            "literature_input_ref": dict(literature.ref),
            "projection_index_ref": dict(projection.ref),
            "commission_ref": dict(commission.ref),
            "commission_materializer_binding_ref": commission_binding,
            "world_requests": [
                _world_entry(world_id, request.ref)
                for world_id, request in zip(WORLD_ORDER, requests, strict=True)
            ],
            "world_request_materializer_bindings": [
                _world_entry(world_id, binding)
                for world_id, binding in zip(
                    WORLD_ORDER,
                    request_bindings,
                    strict=True,
                )
            ],
            "world_order": list(WORLD_ORDER),
        },
        generation=n + 1,
        label="anchor",
    )

    envelopes: list[ResolvedContentObject] = []
    prior_parent_ref = dict(anchor.ref)
    result_statuses = {
        "neutral_inconclusive": "inconclusive",
        "misleading_toy_positive": "scoped_positive",
        "registered_premise_falsifier": "registered_premise_falsified",
        "operational_failure": "operational_failure",
    }
    for ordinal, (world_id, request, request_binding) in enumerate(
        zip(WORLD_ORDER, requests, request_bindings, strict=True)
    ):
        generation = n + 2 + ordinal
        observation_base: dict[str, Any] = {
            **_base(
                "world_observation_v3",
                "experiment-world-observation/3.0.0",
            ),
            "observation_id": f"observation.{world_id}",
            "world_id": world_id,
            "world_ordinal": ordinal,
            "commission_ref": dict(commission.ref),
            "request_ref": dict(request.ref),
            "result_effect": "next_cycle_reflection_only",
        }
        if ordinal == 0:
            decision = builder.add(
                object_kind="world_no_probe_decision_v3",
                value={
                    **_base(
                        "world_no_probe_decision_v3",
                        "experiment-world-no-probe-decision/3.0.0",
                    ),
                    "decision_id": "decision.no-probe",
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "request_ref": dict(request.ref),
                    "decision_kind": "precommitted_no_probe",
                    "execution_disposition": "not_executed",
                    "source_decision_digest": canonical_digest(
                        {"world_id": world_id, "decision": "no-probe"}
                    ),
                },
                generation=generation,
                label="decision-no-probe",
            )
            observation_base.update(
                {
                    "observation_kind": "no_probe_decision",
                    "no_probe_decision_ref": dict(decision.ref),
                }
            )
        else:
            result = builder.add(
                object_kind="world_execution_result_v3",
                value={
                    **_base(
                        "world_execution_result_v3",
                        "experiment-world-execution-result/3.0.0",
                    ),
                    "result_id": f"result.{world_id}",
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "request_ref": dict(request.ref),
                    "result_status": result_statuses[world_id],
                    "source_result_digest": canonical_digest(
                        {"world_id": world_id, "result": result_statuses[world_id]}
                    ),
                    "result_effect": "next_cycle_reflection_only",
                },
                generation=generation,
                label=f"result-{world_id}",
            )
            reflection = builder.add(
                object_kind="world_next_cycle_reflection_v3",
                value={
                    **_base(
                        "world_next_cycle_reflection_v3",
                        "experiment-world-next-cycle-reflection/3.0.0",
                    ),
                    "reflection_id": f"reflection.{world_id}",
                    "world_id": world_id,
                    "world_ordinal": ordinal,
                    "result_ref": dict(result.ref),
                    "reflection_disposition": (
                        "pending_next_cycle_reflection_only"
                    ),
                    "source_reflection_digest": canonical_digest(
                        {"world_id": world_id, "reflection": "pending"}
                    ),
                    "current_cycle_theory_mutation_authorized": False,
                },
                generation=generation,
                label=f"reflection-{world_id}",
            )
            result_binding = builder.materialize(
                result,
                owner_generation=generation,
                label=f"result-{world_id}",
            )
            reflection_binding = builder.materialize(
                reflection,
                owner_generation=generation,
                label=f"reflection-{world_id}",
            )
            observation_base.update(
                {
                    "observation_kind": "executed_result_with_reflection",
                    "result_ref": dict(result.ref),
                    "request_materializer_binding_ref": request_binding,
                    "result_materializer_binding_ref": result_binding,
                    "reflection_ref": dict(reflection.ref),
                    "reflection_materializer_binding_ref": reflection_binding,
                }
            )
        observation = builder.add(
            object_kind="world_observation_v3",
            value=observation_base,
            generation=generation,
            label=f"observation-{world_id}",
        )
        observation_binding = builder.materialize(
            observation,
            owner_generation=generation,
            label=f"observation-{world_id}",
        )
        envelope = builder.add(
            object_kind="world_observation_envelope_v3",
            value={
                **_base(
                    "world_observation_envelope_v3",
                    "experiment-world-observation-envelope/3.0.0",
                ),
                "envelope_id": f"envelope.{world_id}",
                "world_id": world_id,
                "world_ordinal": ordinal,
                "commission_ref": dict(commission.ref),
                "observation_ref": dict(observation.ref),
                "observation_materializer_binding_ref": observation_binding,
                "parent_root_ref": prior_parent_ref,
                "observation_materialization_scope": (
                    "typed_observation_storage_only"
                ),
                "experiment_execution_implied": False,
            },
            generation=generation,
            label=f"envelope-{world_id}",
        )
        envelopes.append(envelope)
        prior_parent_ref = dict(envelope.ref)

    certificate = builder.add(
        object_kind="world_matrix_certificate_v3",
        value={
            **_base(
                "world_matrix_certificate_v3",
                "experiment-world-certificate/3.0.0",
            ),
            "certificate_id": "certificate.world-v3",
            "commission_ref": dict(commission.ref),
            "observation_envelopes": [
                _world_entry(world_id, envelope.ref)
                for world_id, envelope in zip(
                    WORLD_ORDER,
                    envelopes,
                    strict=True,
                )
            ],
            "world_order": list(WORLD_ORDER),
            "result_effect": "next_cycle_reflection_only",
        },
        generation=n + 7,
        label="certificate",
    )
    certificate_binding = builder.materialize(
        certificate,
        owner_generation=n + 7,
        label="certificate",
    )
    aggregation = builder.add(
        object_kind="world_matrix_aggregation_root_v3",
        value={
            **_base(
                "world_matrix_aggregation_root_v3",
                "experiment-world-aggregation-root/3.0.0",
            ),
            "aggregation_id": "aggregation.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "anchor_root_ref": dict(anchor.ref),
            "observation_envelopes": [
                _world_entry(world_id, envelope.ref)
                for world_id, envelope in zip(
                    WORLD_ORDER,
                    envelopes,
                    strict=True,
                )
            ],
            "certificate_ref": dict(certificate.ref),
            "certificate_materializer_binding_ref": certificate_binding,
            "world_order": list(WORLD_ORDER),
            "result_effect": "next_cycle_reflection_only",
        },
        generation=n + 7,
        label="aggregation",
    )

    # The portable fragments are now sufficient.  Deleting both source roots
    # makes path dependence or a second live materializer read observable.
    shutil.rmtree(builder.materializer_root)
    shutil.rmtree(manifest_root)
    return ClosureFixture(
        objects=tuple(builder.objects.values()),
        generations=copy.deepcopy(builder.generations),
        aggregation_ref=copy.deepcopy(dict(aggregation.ref)),
        refs_by_label=copy.deepcopy(builder.refs_by_label),
        source_roots_removed=(
            not builder.materializer_root.exists() and not manifest_root.exists()
        ),
    )


@pytest.fixture(scope="module")
def closure_fixture(tmp_path_factory: pytest.TempPathFactory) -> ClosureFixture:
    return _build_fixture(tmp_path_factory.mktemp("world-v3-closure"))


def _without_object(
    fixture: ClosureFixture,
    object_ref: Mapping[str, Any],
) -> tuple[tuple[ResolvedContentObject, ...], dict[str, int]]:
    object_id = str(object_ref["object_id"])
    return (
        tuple(
            resolved
            for resolved in fixture.objects
            if resolved.ref["object_id"] != object_id
        ),
        {
            key: value
            for key, value in fixture.generations.items()
            if key != object_id
        },
    )


def _replace_root(
    fixture: ClosureFixture,
    mutate: Any,
) -> tuple[
    tuple[ResolvedContentObject, ...],
    dict[str, int],
    dict[str, Any],
]:
    old_id = fixture.aggregation_ref["object_id"]
    old = next(row for row in fixture.objects if row.ref["object_id"] == old_id)
    value = copy.deepcopy(dict(old.value))
    mutate(value)
    replacement = prepare_content_object(
        object_kind="world_matrix_aggregation_root_v3",
        value=value,
        path="adversary/aggregation.json",
    )
    replacement_resolved = ResolvedContentObject(
        ref=dict(replacement.ref),
        value=dict(replacement.value),
        data=bytes(replacement.data),
    )
    objects = tuple(
        replacement_resolved if row.ref["object_id"] == old_id else row
        for row in fixture.objects
    )
    generations = {
        key: value
        for key, value in fixture.generations.items()
        if key != old_id
    }
    generations[replacement.ref["object_id"]] = THEORY_GENERATION + 7
    return objects, generations, dict(replacement.ref)


def _descendant_closure(
    fixture: ClosureFixture,
) -> tuple[tuple[ResolvedContentObject, ...], dict[str, int], dict[str, Any]]:
    reflection = prepare_content_object(
        object_kind="world_matrix_descendant_reflection_root_v3",
        value={
            **_base(
                "world_matrix_descendant_reflection_root_v3",
                "experiment-world-descendant-reflection-root/3.0.0",
            ),
            "reflection_id": "reflection.world-v3",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "aggregation_root_ref": copy.deepcopy(fixture.aggregation_ref),
            "reflection_disposition": (
                "immutable_input_for_later_theory_reflection"
            ),
            "result_effect": "later_theory_cycle_reflection_input_only",
            "current_cycle_theory_mutation_authorized": False,
            "automatic_theory_selection_authorized": False,
            "proof_authorized": False,
            "physics_authority": False,
        },
        path="world-v3/descendant-reflection.json",
    )
    resolved = ResolvedContentObject(
        ref=copy.deepcopy(dict(reflection.ref)),
        value=copy.deepcopy(dict(reflection.value)),
        data=bytes(reflection.data),
    )
    generations = copy.deepcopy(fixture.generations)
    generations[reflection.ref["object_id"]] = THEORY_GENERATION + 8
    return (
        (*fixture.objects, resolved),
        generations,
        copy.deepcopy(dict(reflection.ref)),
    )


@pytest.mark.expensive
def test_complete_world_v3_closure_replays_after_source_deletion_and_relocation(
    closure_fixture: ClosureFixture,
) -> None:
    assert closure_fixture.source_roots_removed
    verified = validate_world_v3_closure(
        closure_fixture.objects,
        closure_fixture.aggregation_ref,
        theory_generation=THEORY_GENERATION,
        committed_generations=closure_fixture.generations,
    )
    assert verified.target_id == TARGET_ID
    assert verified.run_id == RUN_ID
    assert verified.prior_state_version == THEORY_GENERATION - 1
    assert verified.world_ids == WORLD_ORDER
    assert verified.world_generations == tuple(
        THEORY_GENERATION + 2 + index for index in range(5)
    )
    assert verified.result_effect == "next_cycle_reflection_only"
    assert verified.aggregation_root_ref == closure_fixture.aggregation_ref
    assert len(verified.observation_envelope_refs) == 5
    assert len(verified.materializer_binding_ids) == 22

    # Defensive result projections cannot poison later replay.
    escaped = verified.aggregation_root_ref
    escaped["object_kind"] = "forged"
    assert verified.aggregation_root_ref == closure_fixture.aggregation_ref


@pytest.mark.expensive
def test_descendant_closure_requires_exact_immutable_n_plus_8_return(
    closure_fixture: ClosureFixture,
) -> None:
    objects, generations, reflection_ref = _descendant_closure(closure_fixture)
    verified = validate_world_v3_descendant_closure(
        objects,
        reflection_ref,
        theory_generation=THEORY_GENERATION,
        committed_generations=generations,
    )
    assert verified.reflection_generation == THEORY_GENERATION + 8
    assert verified.reflection_root_ref == reflection_ref
    assert verified.support_prefix.aggregation_root_ref == (
        closure_fixture.aggregation_ref
    )
    assert verified.current_cycle_theory_mutation_authorized is False
    assert verified.automatic_theory_selection_authorized is False
    assert verified.proof_authorized is False
    assert verified.physics_authority is False

    with pytest.raises(ContractError, match=r"requires the N\+8 reflection root"):
        validate_world_v3_descendant_closure(
            closure_fixture.objects,
            closure_fixture.aggregation_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=closure_fixture.generations,
        )


def _semantic_topological_order(
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


def _prepared_semantic_generation(
    fixture: ClosureFixture,
    generation: int,
) -> tuple[PreparedContentObject, ...]:
    prepared: list[PreparedContentObject] = []
    for row in fixture.objects:
        object_id = str(row.ref["object_id"])
        if fixture.generations[object_id] != generation:
            continue
        value = prepare_content_object(
            object_kind=str(row.ref["object_kind"]),
            value=row.value,
            path=(
                f"branches/root/world-v3/g{generation}/objects/"
                f"{object_id}.json"
            ),
        )
        assert value.ref == row.ref
        prepared.append(value)
    return tuple(sorted(prepared, key=lambda row: str(row.ref["object_id"])))


def _commit_semantic_generation(
    *,
    store: DiscoveryTransactionStore,
    generation: int,
    local_objects: tuple[PreparedContentObject, ...],
    owner_catalog: dict[str, tuple[dict[str, Any], dict[str, Any]]],
) -> ContentGraphTransactionResult:
    edges: list[dict[str, str]] = []
    for row in local_objects:
        edges.extend(
            derive_content_object_edges(object_ref=row.ref, payload=row.value)
        )
    local_ids = {str(row.ref["object_id"]) for row in local_objects}
    imported_ids = sorted(
        {
            edge["source_object_id"]
            for edge in edges
            if edge["source_object_id"] not in local_ids
        }
    )
    imported_handles = [
        build_committed_object_handle(
            source_commit_reference=owner_catalog[object_id][1],
            object_ref=owner_catalog[object_id][0],
        )
        for object_id in imported_ids
    ]
    all_ids = local_ids | set(imported_ids)
    graph = build_content_object_graph(
        local_descriptors=[row.descriptor for row in local_objects],
        imported_handles=imported_handles,
        ordered_roots=sorted(local_ids),
        edges=edges,
        topological_order=_semantic_topological_order(all_ids, edges),
    )
    transaction = prepare_content_graph_transaction(
        expected_generation=generation - 1,
        state={
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": generation,
            "programme_id": "semantic-world-v3-programme",
            "marker": f"semantic-seed-g{generation}",
        },
        namespace=Namespace(TARGET_ID, RUN_ID, "root", generation - 1),
        graph_artifact_path=(
            f"branches/root/world-v3/g{generation}/graph.json"
        ),
        graph=graph,
        local_objects=local_objects,
    )
    result = commit_content_graph_transaction(store=store, transaction=transaction)
    for row in local_objects:
        owner_catalog[str(row.ref["object_id"])] = (
            copy.deepcopy(dict(row.ref)),
            copy.deepcopy(dict(result.commit_ref)),
        )
    return result


def _semantic_stage_product(
    fixture: ClosureFixture,
    generation: int,
    *,
    root_kind: str,
    world_id: str | None = None,
) -> GraphStageProduct:
    local_objects = _prepared_semantic_generation(fixture, generation)
    roots = [
        row
        for row in local_objects
        if row.ref["object_kind"] == root_kind
        and (world_id is None or row.value.get("world_id") == world_id)
    ]
    assert len(roots) == 1
    return GraphStageProduct(
        state={
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": generation,
            "programme_id": "semantic-world-v3-programme",
            "marker": f"semantic-descendant-g{generation}",
        },
        local_objects=local_objects,
        root_object_id=str(roots[0].ref["object_id"]),
    )


def _run_descendant_replay(
    *,
    workspace: Path,
    store_root: str,
    theory_graph_artifact_path: str,
) -> subprocess.CompletedProcess[bytes]:
    request = {
        "store_root": store_root,
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "theory_generation": THEORY_GENERATION,
        "theory_graph_artifact_path": theory_graph_artifact_path,
        "branch_id": "root",
    }
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "agentic.scripts.validate_world_v3_descendant_chain",
            "--workspace",
            str(workspace),
        ],
        cwd=Path(__file__).resolve().parents[2],
        input=canonical_json(request),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


@pytest.mark.expensive
@pytest.mark.timeout(600)
def test_store_backed_facade_and_fresh_replay_are_one_semantic_chain(
    tmp_path: Path,
    closure_fixture: ClosureFixture,
) -> None:
    store_root = tmp_path / "semantic-store"
    store = DiscoveryTransactionStore(
        store_root,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )
    owner_catalog: dict[
        str, tuple[dict[str, Any], dict[str, Any]]
    ] = {}
    for generation in range(1, THEORY_GENERATION - 1):
        bootstrap = prepare_content_object(
            object_kind="canonical_cycle_auxiliary_artifact",
            value={
                "bootstrap_only": True,
                "generation": generation,
            },
            path=(
                f"branches/root/bootstrap/g{generation}/objects/root.json"
            ),
        )
        _commit_semantic_generation(
            store=store,
            generation=generation,
            local_objects=(bootstrap,),
            owner_catalog=owner_catalog,
        )
    _commit_semantic_generation(
        store=store,
        generation=THEORY_GENERATION - 1,
        local_objects=_prepared_semantic_generation(
            closure_fixture, THEORY_GENERATION - 1
        ),
        owner_catalog=owner_catalog,
    )
    theory_objects = _prepared_semantic_generation(
        closure_fixture, THEORY_GENERATION
    )
    theory_result = _commit_semantic_generation(
        store=store,
        generation=THEORY_GENERATION,
        local_objects=theory_objects,
        owner_catalog=owner_catalog,
    )

    anchor = _semantic_stage_product(
        closure_fixture,
        THEORY_GENERATION + 1,
        root_kind="world_matrix_anchor_root_v3",
    )
    worlds = {
        world_id: _semantic_stage_product(
            closure_fixture,
            THEORY_GENERATION + 2 + ordinal,
            root_kind="world_observation_envelope_v3",
            world_id=world_id,
        )
        for ordinal, world_id in enumerate(WORLD_ORDER)
    }
    aggregation = _semantic_stage_product(
        closure_fixture,
        THEORY_GENERATION + 7,
        root_kind="world_matrix_aggregation_root_v3",
    )
    descendant_objects, descendant_generations, reflection_ref = (
        _descendant_closure(closure_fixture)
    )
    reflection_resolved = next(
        row
        for row in descendant_objects
        if row.ref["object_id"] == reflection_ref["object_id"]
    )
    reflection_object = prepare_content_object(
        object_kind=str(reflection_resolved.ref["object_kind"]),
        value=reflection_resolved.value,
        path="branches/root/world-v3/g20/objects/reflection.json",
    )
    reflection = GraphStageProduct(
        state={
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "generation": THEORY_GENERATION + 8,
            "programme_id": "semantic-world-v3-programme",
            "marker": "semantic-descendant-g20",
        },
        local_objects=(reflection_object,),
        root_object_id=str(reflection_object.ref["object_id"]),
    )
    result = run_canonical_descendant_experiment_v3(
        store=store,
        theory_result=theory_result,
        theory_owned_objects=theory_objects,
        anchor_product=anchor,
        world_producers={
            world_id: (lambda product=worlds[world_id]: product)
            for world_id in WORLD_ORDER
        },
        aggregation_product=aggregation,
        reflection_product=reflection,
    )
    assert result.reflection.generation == THEORY_GENERATION + 8
    assert result.verified_descendant_closure.reflection_root_ref == (
        reflection_ref
    )
    assert result.verified_descendant_closure.proof_authorized is False
    assert result.verified_descendant_closure.physics_authority is False
    validate_world_v3_descendant_closure(
        descendant_objects,
        reflection_ref,
        theory_generation=THEORY_GENERATION,
        committed_generations=descendant_generations,
    )

    theory_graph_path = str(
        theory_result.graph_ref["graph_artifact"]["path"]
    )
    replay = _run_descendant_replay(
        workspace=tmp_path,
        store_root="semantic-store",
        theory_graph_artifact_path=theory_graph_path,
    )
    assert replay.returncode == 0, replay.stderr.decode()
    replayed = json.loads(replay.stdout)
    assert replayed["reflection_generation"] == THEORY_GENERATION + 8
    assert replayed["result_effect"] == (
        "later_theory_cycle_reflection_input_only"
    )

    escaped = _run_descendant_replay(
        workspace=tmp_path,
        store_root="../semantic-store",
        theory_graph_artifact_path=theory_graph_path,
    )
    assert escaped.returncode == 2
    assert b"canonical relative path" in escaped.stderr

    tampered_root = tmp_path / "tampered-store"
    shutil.copytree(store_root, tampered_root)
    tampered_store = DiscoveryTransactionStore(
        tampered_root,
        target_id=TARGET_ID,
        run_id=RUN_ID,
    )
    terminal = tampered_store.read_verified_commit(THEORY_GENERATION + 8)
    artifact_path = next(
        row["path"]
        for row in terminal.manifest["artifacts"]
        if row["path"].endswith("/reflection.json")
    )
    (terminal.commit_path / "artifacts" / artifact_path).write_bytes(
        b'{"tampered":true}'
    )
    tampered = _run_descendant_replay(
        workspace=tmp_path,
        store_root="tampered-store",
        theory_graph_artifact_path=theory_graph_path,
    )
    assert tampered.returncode == 2
    assert b"digest mismatch" in tampered.stderr

    stale = prepare_content_object(
        object_kind="canonical_cycle_auxiliary_artifact",
        value={"stale_head_adversary": True},
        path="branches/root/stale/g21/objects/root.json",
    )
    _commit_semantic_generation(
        store=store,
        generation=THEORY_GENERATION + 9,
        local_objects=(stale,),
        owner_catalog=owner_catalog,
    )
    stale_replay = _run_descendant_replay(
        workspace=tmp_path,
        store_root="semantic-store",
        theory_graph_artifact_path=theory_graph_path,
    )
    assert stale_replay.returncode == 2
    assert b"active current head" in stale_replay.stderr or b"N+8" in (
        stale_replay.stderr
    )


@pytest.mark.expensive
def test_descendant_closure_rejects_wrong_generation_or_extra_n_plus_8_authority(
    closure_fixture: ClosureFixture,
) -> None:
    objects, generations, reflection_ref = _descendant_closure(closure_fixture)
    wrong_generation = copy.deepcopy(generations)
    wrong_generation[reflection_ref["object_id"]] = THEORY_GENERATION + 7
    with pytest.raises(ContractError, match=r"exact N\+8"):
        validate_world_v3_descendant_closure(
            objects,
            reflection_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=wrong_generation,
        )

    extra = next(
        row for row in closure_fixture.objects if row.ref["object_id"] != reflection_ref["object_id"]
    )
    extra_generation = copy.deepcopy(generations)
    extra_generation[extra.ref["object_id"]] = THEORY_GENERATION + 8
    with pytest.raises(ContractError, match="authority beyond"):
        validate_world_v3_descendant_closure(
            objects,
            reflection_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=extra_generation,
        )
@pytest.mark.expensive
def test_partial_or_sixth_world_closure_is_rejected(
    closure_fixture: ClosureFixture,
) -> None:
    objects, generations = _without_object(
        closure_fixture,
        closure_fixture.refs_by_label[
            "result-registered_premise_falsifier"
        ],
    )
    with pytest.raises(ContractError):
        validate_world_v3_closure(
            objects,
            closure_fixture.aggregation_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=generations,
        )

    plan = next(
        row
        for row in closure_fixture.objects
        if row.ref["object_id"]
        == closure_fixture.refs_by_label["plan-no_probe"]["object_id"]
    )
    sixth_value = copy.deepcopy(dict(plan.value))
    sixth_value["plan_id"] = "plan.unreachable-sixth-world"
    sixth = prepare_content_object(
        object_kind="world_plan_v3",
        value=sixth_value,
        path="adversary/sixth-plan.json",
    )
    sixth_resolved = ResolvedContentObject(
        ref=dict(sixth.ref),
        value=dict(sixth.value),
        data=bytes(sixth.data),
    )
    extra_objects = (*closure_fixture.objects, sixth_resolved)
    extra_generations = {
        **closure_fixture.generations,
        sixth.ref["object_id"]: THEORY_GENERATION + 1,
    }
    with pytest.raises(ContractError, match="exact supplied object closure|exactly 5"):
        validate_world_v3_closure(
            extra_objects,
            closure_fixture.aggregation_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=extra_generations,
        )


@pytest.mark.expensive
def test_cross_run_and_certificate_splice_are_rejected_after_rehash(
    closure_fixture: ClosureFixture,
) -> None:
    objects, generations, root_ref = _replace_root(
        closure_fixture,
        lambda value: value.__setitem__("run_id", "foreign-run"),
    )
    with pytest.raises(ContractError, match="crosses target or run"):
        validate_world_v3_closure(
            objects,
            root_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=generations,
        )

    foreign_certificate = closure_fixture.refs_by_label["commission"]
    objects, generations, root_ref = _replace_root(
        closure_fixture,
        lambda value: value.__setitem__(
            "certificate_ref",
            copy.deepcopy(foreign_certificate),
        ),
    )
    with pytest.raises(ContractError):
        validate_world_v3_closure(
            objects,
            root_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=generations,
        )


@pytest.mark.expensive
@pytest.mark.parametrize(
    ("label", "forged_generation"),
    (
        ("precommit-state", THEORY_GENERATION),
        ("anchor", THEORY_GENERATION + 2),
        ("envelope-neutral_inconclusive", THEORY_GENERATION + 4),
        ("result-misleading_toy_positive", THEORY_GENERATION + 1),
        ("certificate", THEORY_GENERATION + 6),
        ("aggregation", THEORY_GENERATION + 6),
    ),
)
def test_generation_and_forward_authority_attacks_fail_closed(
    closure_fixture: ClosureFixture,
    label: str,
    forged_generation: int,
) -> None:
    generations = copy.deepcopy(closure_fixture.generations)
    generations[
        closure_fixture.refs_by_label[label]["object_id"]
    ] = forged_generation
    with pytest.raises(ContractError):
        validate_world_v3_closure(
            closure_fixture.objects,
            closure_fixture.aggregation_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=generations,
        )


@pytest.mark.expensive
def test_generation_membership_is_total_and_cannot_be_relocated_to_another_id(
    closure_fixture: ClosureFixture,
) -> None:
    generations = copy.deepcopy(closure_fixture.generations)
    removed_id = closure_fixture.refs_by_label["anchor"]["object_id"]
    generation = generations.pop(removed_id)
    generations["world-content-object-v1.forged-membership"] = generation
    with pytest.raises(ContractError, match="membership differs"):
        validate_world_v3_closure(
            closure_fixture.objects,
            closure_fixture.aggregation_ref,
            theory_generation=THEORY_GENERATION,
            committed_generations=generations,
        )


@pytest.mark.expensive
def test_path_free_closure_replays_in_a_fresh_process(
    closure_fixture: ClosureFixture,
    tmp_path: Path,
) -> None:
    bundle = {
        "theory_generation": THEORY_GENERATION,
        "aggregation_ref": closure_fixture.aggregation_ref,
        "objects": [
            {
                "ref": dict(resolved.ref),
                "value": dict(resolved.value),
                "generation": closure_fixture.generations[
                    resolved.ref["object_id"]
                ],
            }
            for resolved in closure_fixture.objects
        ],
    }
    bundle_path = tmp_path / "closure.json"
    bundle_path.write_bytes(canonical_json(bundle))
    script = r"""
import json
import sys
from pathlib import Path
from agentic.discovery.contracts import canonical_json
from agentic.experiments.world_object_graph import ResolvedContentObject
from agentic.experiments.world_v3_closure import validate_world_v3_closure

bundle = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
objects = tuple(
    ResolvedContentObject(
        ref=row["ref"],
        value=row["value"],
        data=canonical_json(row["value"]),
    )
    for row in bundle["objects"]
)
generations = {
    row["ref"]["object_id"]: row["generation"]
    for row in bundle["objects"]
}
verified = validate_world_v3_closure(
    objects,
    bundle["aggregation_ref"],
    theory_generation=bundle["theory_generation"],
    committed_generations=generations,
)
print(json.dumps({
    "target_id": verified.target_id,
    "run_id": verified.run_id,
    "world_ids": list(verified.world_ids),
    "aggregation_ref": verified.aggregation_root_ref,
}, sort_keys=True))
"""
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-c", script, str(bundle_path)],
        cwd=Path(__file__).resolve().parents[2],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=90,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    replay = json.loads(completed.stdout)
    assert replay == {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "world_ids": list(WORLD_ORDER),
        "aggregation_ref": closure_fixture.aggregation_ref,
    }
