# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Concrete producers for the canonical theory-subordinate world lane.

This module composes the store-derived theory authority, the registered
argv-only causal producer, the dynamic experiment runtime, a receipt-backed
post-result reflective synthesizer, and the N+1..N+7 support transaction.  It
does not accept a caller-authored authority projection.  All five requests are
sealed before the first adapter executes, the five callbacks can run as one
parallel wave, and only the support lane owns serial commit capability.

The reflection callback is intentionally an explicit dependency: a fabricated
reflection object is not a substitute for a successful synthesizer receipt.
The resulting support reference remains a request for later theory reflection,
not a theory mutation, selection, proof, or physical-target result.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    stable_identifier,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore

from .canonical_support_lane import (
    AggregationProduction,
    CanonicalSupportLaneResult,
    WorldObservationProduction,
    build_local_production_receipt,
    run_canonical_theory_support_lane,
)
from .causal_producer_runtime import (
    CausalArtifactProducerRuntime,
    SealedCausalArtifact,
)
from .reflection import validate_experiment_reflection_receipt
from .runtime import (
    compile_experiment_spec,
    execute_experiment,
    triage_probe,
    validate_experiment_spec,
)
from .world_matrix import (
    COMMISSION_PRODUCER_ROLE,
    COMMISSION_STAGE_ID,
    EXECUTED_WORLD_IDS,
    EXPERIMENT_EXECUTION_PRODUCER_ROLE,
    EXPERIMENT_EXECUTION_STAGE_ID,
    FINAL_ADJUDICATION_PRODUCER_ROLE,
    FINAL_ADJUDICATION_STAGE_ID,
    MATRIX_AGGREGATION_PRODUCER_ROLE,
    MATRIX_AGGREGATION_STAGE_ID,
    NO_PROBE_DECISION_PRODUCER_ROLE,
    NO_PROBE_DECISION_STAGE_ID,
    POST_RESULT_REFLECTION_PRODUCER_ROLE,
    POST_RESULT_REFLECTION_STAGE_ID,
    PRE_EXPERIMENT_SCHEDULE_PRODUCER_ROLE,
    PRE_EXPERIMENT_SCHEDULE_STAGE_ID,
    WORLD_IDS,
    WORLD_OBSERVATION_PRODUCER_ROLE,
    WORLD_OBSERVATION_STAGE_ID,
    WORLD_REQUEST_PRODUCER_ROLE,
    WORLD_REQUEST_STAGE_ID,
    CommittedCausalEvidencePaths,
    bind_experiment_world_observation,
    build_experiment_no_probe_decision,
    build_experiment_world_observation_envelope,
    build_experiment_world_request,
    build_pre_execution_world_matrix_commission,
)


_PRODUCTION_BRANCH_ID = "canonical-world-support-production"
_WORLD_PRODUCER_ID = "canonical-world-observation-producer"
_AGGREGATION_PRODUCER_ID = "canonical-world-aggregation-producer"


@dataclass(frozen=True, slots=True)
class PostResultReflectionProduction:
    """Complete evidence needed to validate one actual result reflection."""

    reflection_receipt: Mapping[str, Any]
    source_reflection_packet: Mapping[str, Any]
    result_reflection_packet: Mapping[str, Any]
    synthesis_operator_receipt: Mapping[str, Any]


PostResultReflectionProducer = Callable[
    [str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Path],
    PostResultReflectionProduction,
]


@dataclass(frozen=True, slots=True)
class CanonicalWorldProducerPlan:
    """Pre-execution commission plus callbacks with no commit capability."""

    authority_projection: Mapping[str, Any]
    commission: Mapping[str, Any]
    commission_producer_binding: Mapping[str, Any]
    world_requests: Mapping[str, Mapping[str, Any]]
    world_request_producer_bindings: Mapping[str, Mapping[str, Any]]
    anchor_evidence_records: tuple[CommittedCausalEvidencePaths, ...]
    world_producers: Mapping[
        str, Callable[[Mapping[str, Any]], WorldObservationProduction]
    ]
    aggregation_producer: Callable[[Mapping[str, Any]], AggregationProduction]


def _projection_components(
    projection: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    components: dict[str, dict[str, Any]] = {}
    for row in projection.get("components", []):
        if not isinstance(row, Mapping) or not isinstance(row.get("value"), Mapping):
            raise ContractError("committed world projection has a malformed component")
        kind = str(row.get("component_kind", ""))
        if not kind or kind in components:
            raise ContractError("committed world projection repeats a component")
        components[kind] = copy.deepcopy(dict(row["value"]))
    return components


def _resolver(
    sealed: tuple[SealedCausalArtifact, ...],
) -> Any:
    # Keep the concrete trusted resolver construction behind the production
    # runtime instead of admitting a caller callback or subclass.
    if not sealed:
        raise ContractError("causal resolution requires at least one sealed producer")
    from .world_matrix import CommittedCausalEvidenceResolver

    return CommittedCausalEvidenceResolver(
        tuple(item.evidence_paths for item in sealed)
    )


def _contained_run_root(workspace: Path, run_root: Path | None) -> Path:
    root = (
        workspace / ".canonical-world-support-runs"
        if run_root is None
        else (run_root if run_root.is_absolute() else workspace / run_root)
    ).resolve()
    try:
        root.relative_to(workspace)
    except ValueError as exc:
        raise ContractError("canonical world run root must remain inside the workspace") from exc
    return root


def _validate_lane_world_request(
    request: Mapping[str, Any],
    *,
    world_id: str,
    sealed_world_request: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(request))
    required = {
        "schema_version",
        "request_kind",
        "world_id",
        "world_request",
        "anchor_reference",
        "theory_mutation_authorized",
        "canonical_commit_order",
        "request_digest",
    }
    if (
        set(record) != required
        or record["schema_version"] != "1.0.0"
        or record["request_kind"]
        != "produce_one_theory_subordinate_world_observation"
        or record["world_id"] != world_id
        or record["world_request"] != dict(sealed_world_request)
        or record["theory_mutation_authorized"] is not False
        or record["canonical_commit_order"] != list(WORLD_IDS)
        or record["request_digest"]
        != canonical_digest(
            {key: value for key, value in record.items() if key != "request_digest"}
        )
    ):
        raise ContractError("world producer received a different support request")
    return record


def _reflection_evidence_parameter(
    production: PostResultReflectionProduction,
) -> dict[str, Any]:
    return {
        "source_reflection_packet": copy.deepcopy(
            dict(production.source_reflection_packet)
        ),
        "result_reflection_packet": copy.deepcopy(
            dict(production.result_reflection_packet)
        ),
        "synthesis_operator_receipt": copy.deepcopy(
            dict(production.synthesis_operator_receipt)
        ),
    }


def compile_canonical_world_spec_family(
    authority_projection: Mapping[str, Any],
    *,
    branch_id: str,
    registered_at: str,
    resource_budget: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Compile the fixed-claim four-world family from a derived projection.

    The family is a protocol-level falsifier matrix, not four independent
    scientific hypotheses.  Only adapter/model/resource interventions vary;
    the registered theory premise and every conceptual input remain fixed.
    """

    projection = copy.deepcopy(dict(authority_projection))
    components = _projection_components(projection)
    try:
        programme = components["theory_programme"]
        reflection = components["reflection_packet"]
        claim = components["registered_claim"]
    except KeyError as exc:
        raise ContractError("world spec compilation lacks committed theory inputs") from exc
    if claim.get("claim_kind") != "theory_premise":
        raise ContractError(
            "canonical falsifier matrix requires a registered theory premise"
        )
    triage = triage_probe(
        {
            "target_id": projection["target_id"],
            "theory_programme_id": claim["theory_programme_id"],
            "source_theory_programme_digest": claim[
                "source_theory_programme_digest"
            ],
            "source_reflection_packet_digest": claim[
                "source_reflection_packet_digest"
            ],
            "conceptual_system_ids": list(claim["conceptual_system_ids"]),
            "registered_theory_claims": [copy.deepcopy(claim)],
            "theoretical_question_id": claim["claim_id"],
            "question": claim["statement"],
            "programme_maturity": "formalization_ready",
            "probe_role": "falsifier",
            "decision_effect": {
                "if_supported": "retain the registered premise provisionally",
                "if_not_supported": "request reflective premise review",
            },
            "expected_conceptual_change": (
                "Localize whether the exact registered premise must be revised "
                "in a later reflective cycle."
            ),
            "theory_generated_justification": (
                "The committed reflective programme registered this exact premise "
                "as a discriminating correction condition."
            ),
            "candidate_methods": ["exact", "finite_model"],
            "state_version": projection["prior_state_version"],
        }
    )
    if triage["decision"] != "commission":
        raise ContractError("committed registered premise did not commission support")
    if (
        canonical_digest(programme) != claim["source_theory_programme_digest"]
        or reflection.get("packet_digest")
        != claim["source_reflection_packet_digest"]
    ):
        raise ContractError("registered claim crossed its committed theory or reflection")

    preregistration = {
        "hypothesis": "The registered premise survives the declared scoped probe.",
        "decision_rule": {"comparator": "==", "threshold": 1},
        "stopping_rule": "Stop at the declared exact result or bounded cutoff.",
        "analysis_plan": "Apply the frozen rule without changing the theory claim.",
        "registered_at": registered_at,
    }
    controls = [
        {
            "control_id": stable_identifier(
                "canonical-world-fixed-claim-control", claim["claim_id"]
            ),
            "variable": "registered_theory_claim",
            "value": claim["claim_digest"],
            "role": "held_fixed",
        }
    ]

    def request(adapter: str, model: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "run_id": projection["run_id"],
            "branch_id": branch_id,
            "adapter": adapter,
            "model": copy.deepcopy(dict(model)),
            "preregistration": copy.deepcopy(preregistration),
            "controls": copy.deepcopy(controls),
            "seed_policy": {
                "stochastic": False,
                "policy": "not_applicable",
            },
            "resource_budget": copy.deepcopy(dict(resource_budget)),
            "transfer_boundary": (
                "Protocol-level scoped theory support only; no theorem, theory "
                "selection, ontology mutation, or physical-target conclusion."
            ),
            "theory_effect_contract": {
                "tested_claim_id": claim["claim_id"],
                "tested_claim_kind": claim["claim_kind"],
                "target_relation": claim["target_relation"],
                "if_supported": "record_scoped_consistency_only",
                "if_falsified": "request_registered_premise_revision",
                "theory_identity_locked": True,
                "automatic_theory_selection": False,
                "automatic_proof": False,
            },
        }

    return {
        "neutral_inconclusive": compile_experiment_spec(
            triage,
            request(
                "finite_model",
                {
                    "variables": {"x": [0, 1, 2, 3]},
                    "predicate": "x >= 0",
                    "quantifier": "forall",
                    "max_states": 2,
                },
            ),
        ),
        "misleading_toy_positive": compile_experiment_spec(
            triage,
            request(
                "exact",
                {"operation": "equality", "left": "1", "right": "1"},
            ),
        ),
        "registered_premise_falsifier": compile_experiment_spec(
            triage,
            request(
                "exact",
                {"operation": "equality", "left": "1", "right": "2"},
            ),
        ),
        "operational_failure": compile_experiment_spec(
            triage,
            request("exact", {"operation": "unsupported_operation"}),
        ),
    }


def prepare_canonical_world_producer_plan(
    *,
    store: DiscoveryTransactionStore,
    theory_generation: int,
    workspace: Path,
    world_specs: Mapping[str, Mapping[str, Any]],
    reflection_producer: PostResultReflectionProducer,
    run_root: Path | None = None,
) -> CanonicalWorldProducerPlan:
    """Derive and seal every input needed before parallel world execution."""

    # This module is exported from agentic.experiments, while the projection
    # module imports the world contract.  Resolve the edge only when production
    # starts so package import remains acyclic.
    from agentic.discovery.committed_projection import (
        derive_committed_cycle_world_authority_projection,
    )

    workspace = workspace.resolve()
    if not workspace.is_dir():
        raise ContractError("canonical world producer workspace does not exist")
    if not callable(reflection_producer):
        raise ContractError("executed worlds require a post-result reflection producer")
    if set(world_specs) != set(EXECUTED_WORLD_IDS):
        raise ContractError("canonical world production requires exactly four executed specs")
    specs = {
        world_id: validate_experiment_spec(world_specs[world_id])
        for world_id in EXECUTED_WORLD_IDS
    }
    execution_root = _contained_run_root(workspace, run_root)
    projection = derive_committed_cycle_world_authority_projection(
        store, theory_generation
    )
    components = _projection_components(projection)
    required_components = {
        "adjudication_authority",
        "schedule",
        "reflection_packet",
    }
    if not required_components.issubset(components):
        raise ContractError("committed world projection lacks production authority")
    namespace = Namespace(
        store.target_id,
        store.run_id,
        _PRODUCTION_BRANCH_ID,
        theory_generation,
    )
    runtime = CausalArtifactProducerRuntime(
        workspace=workspace,
        namespace=namespace,
    )
    adjudication = components["adjudication_authority"]
    schedule = components["schedule"]
    base: list[SealedCausalArtifact] = []
    base.append(
        runtime.seal(
            stage_id=FINAL_ADJUDICATION_STAGE_ID,
            producer_role=FINAL_ADJUDICATION_PRODUCER_ROLE,
            artifact_id=stable_identifier(
                "final-adjudication-authority", canonical_digest(adjudication)
            ),
            artifact=adjudication,
        )
    )
    base.append(
        runtime.seal(
            stage_id=PRE_EXPERIMENT_SCHEDULE_STAGE_ID,
            producer_role=PRE_EXPERIMENT_SCHEDULE_PRODUCER_ROLE,
            artifact_id=str(
                schedule.get("schedule_id")
                or stable_identifier("pre-experiment-schedule", canonical_digest(schedule))
            ),
            artifact=schedule,
        )
    )
    commission = build_pre_execution_world_matrix_commission(
        projection,
        world_specs=specs,
        adjudication_producer_binding=base[0].binding,
        schedule_producer_binding=base[1].binding,
        evidence_resolver=_resolver(tuple(base)),
    )
    commission_sealed = runtime.seal(
        stage_id=COMMISSION_STAGE_ID,
        producer_role=COMMISSION_PRODUCER_ROLE,
        artifact_id=commission["commission_id"],
        artifact=commission,
    )
    base.append(commission_sealed)
    requests: dict[str, dict[str, Any]] = {}
    request_bindings: dict[str, dict[str, Any]] = {}
    for world_id in WORLD_IDS:
        request = build_experiment_world_request(
            commission,
            world_id,
            commission_producer_binding=commission_sealed.binding,
            evidence_resolver=_resolver(tuple(base)),
        )
        sealed_request = runtime.seal(
            stage_id=WORLD_REQUEST_STAGE_ID,
            producer_role=WORLD_REQUEST_PRODUCER_ROLE,
            artifact_id=request["request_id"],
            artifact=request,
            causal_parameters={
                "causal_input": {
                    "world_id": world_id,
                    "world_plan_digest": request["world_plan_digest"],
                    "commission_id": commission["commission_id"],
                    "commission_digest": commission["commission_digest"],
                    "commission_producer_binding_id": commission_sealed.binding[
                        "binding_id"
                    ],
                    "commission_producer_binding_digest": commission_sealed.binding[
                        "binding_digest"
                    ],
                }
            },
        )
        requests[world_id] = request
        request_bindings[world_id] = copy.deepcopy(dict(sealed_request.binding))
        base.append(sealed_request)
    frozen_base = tuple(base)
    source_reflection = components["reflection_packet"]

    def make_world_producer(
        world_id: str,
    ) -> Callable[[Mapping[str, Any]], WorldObservationProduction]:
        def produce(lane_request: Mapping[str, Any]) -> WorldObservationProduction:
            request = _validate_lane_world_request(
                lane_request,
                world_id=world_id,
                sealed_world_request=requests[world_id],
            )
            local = list(frozen_base)
            if world_id == "no_probe":
                decision = build_experiment_no_probe_decision(
                    commission,
                    world_request=requests[world_id],
                    world_request_producer_binding=request_bindings[world_id],
                    evidence_resolver=_resolver(tuple(local)),
                )
                execution = runtime.seal(
                    stage_id=NO_PROBE_DECISION_STAGE_ID,
                    producer_role=NO_PROBE_DECISION_PRODUCER_ROLE,
                    artifact_id=decision["decision_id"],
                    artifact=decision,
                )
                local.append(execution)
                observation = bind_experiment_world_observation(
                    commission,
                    world_id,
                    world_request=requests[world_id],
                    world_request_producer_binding=request_bindings[world_id],
                    observed_authority_projection=projection,
                    spec=None,
                    receipt=None,
                    execution_producer_binding=execution.binding,
                    reflection=None,
                    reflection_producer_binding=None,
                    no_probe_decision=decision,
                    evidence_resolver=_resolver(tuple(local)),
                )
            else:
                spec = specs[world_id]
                work_directory = execution_root / world_id
                receipt = execute_experiment(spec, work_directory)
                execution = runtime.seal(
                    stage_id=EXPERIMENT_EXECUTION_STAGE_ID,
                    producer_role=EXPERIMENT_EXECUTION_PRODUCER_ROLE,
                    artifact_id=receipt["receipt_id"],
                    artifact=receipt,
                )
                local.append(execution)
                produced_reflection = reflection_producer(
                    world_id,
                    copy.deepcopy(spec),
                    copy.deepcopy(receipt),
                    copy.deepcopy(source_reflection),
                    work_directory,
                )
                if type(produced_reflection) is not PostResultReflectionProduction:
                    raise ContractError(
                        "reflection producer returned an untyped or subclassed output"
                    )
                if dict(produced_reflection.source_reflection_packet) != source_reflection:
                    raise ContractError("post-result reflection crossed its committed source packet")
                reflection = copy.deepcopy(
                    dict(produced_reflection.reflection_receipt)
                )
                validate_experiment_reflection_receipt(
                    reflection,
                    spec,
                    receipt,
                    produced_reflection.source_reflection_packet,
                    produced_reflection.result_reflection_packet,
                    produced_reflection.synthesis_operator_receipt,
                    work_directory=work_directory,
                )
                reflection_sealed = runtime.seal(
                    stage_id=POST_RESULT_REFLECTION_STAGE_ID,
                    producer_role=POST_RESULT_REFLECTION_PRODUCER_ROLE,
                    artifact_id=reflection["reflection_receipt_id"],
                    artifact=reflection,
                    causal_parameters={
                        "post_result_reflection_evidence": (
                            _reflection_evidence_parameter(produced_reflection)
                        )
                    },
                )
                local.append(reflection_sealed)
                observation = bind_experiment_world_observation(
                    commission,
                    world_id,
                    world_request=requests[world_id],
                    world_request_producer_binding=request_bindings[world_id],
                    observed_authority_projection=projection,
                    spec=spec,
                    receipt=receipt,
                    execution_producer_binding=execution.binding,
                    reflection=reflection,
                    reflection_producer_binding=reflection_sealed.binding,
                    evidence_resolver=_resolver(tuple(local)),
                )
            observation_sealed = runtime.seal(
                stage_id=WORLD_OBSERVATION_STAGE_ID,
                producer_role=WORLD_OBSERVATION_PRODUCER_ROLE,
                artifact_id=observation["observation_id"],
                artifact=observation,
            )
            local.append(observation_sealed)
            envelope = build_experiment_world_observation_envelope(
                commission,
                observation,
                observation_producer_binding=observation_sealed.binding,
                evidence_resolver=_resolver(tuple(local)),
            )
            production_receipt = build_local_production_receipt(
                producer_id=_WORLD_PRODUCER_ID,
                invocation_id=stable_identifier(
                    "canonical-world-production",
                    world_id,
                    request["request_digest"],
                    envelope["envelope_digest"],
                ),
                request_digest=request["request_digest"],
                output=envelope,
            )
            return WorldObservationProduction(
                world_id=world_id,
                observation_envelope=envelope,
                evidence_records=tuple(item.evidence_paths for item in local),
                production_receipt=production_receipt,
            )

        return produce

    producers = {world_id: make_world_producer(world_id) for world_id in WORLD_IDS}

    def aggregate(lane_request: Mapping[str, Any]) -> AggregationProduction:
        request = copy.deepcopy(dict(lane_request))
        required = {
            "schema_version",
            "request_kind",
            "aggregation_input_manifest",
            "certificate",
            "theory_mutation_authorized",
            "only_permitted_downstream_effect",
            "request_digest",
        }
        if (
            set(request) != required
            or request["schema_version"] != "1.0.0"
            or request["request_kind"]
            != "produce_theory_subordinate_world_aggregation"
            or request["theory_mutation_authorized"] is not False
            or request["only_permitted_downstream_effect"]
            != "pending_next_cycle_reflection_only"
            or request["request_digest"]
            != canonical_digest(
                {
                    key: value
                    for key, value in request.items()
                    if key != "request_digest"
                }
            )
        ):
            raise ContractError("aggregation producer received a different committed prefix")
        certificate = copy.deepcopy(dict(request["certificate"]))
        sealed = runtime.seal(
            stage_id=MATRIX_AGGREGATION_STAGE_ID,
            producer_role=MATRIX_AGGREGATION_PRODUCER_ROLE,
            artifact_id=certificate["certificate_id"],
            artifact=certificate,
            causal_parameters={
                "aggregation_input_manifest": copy.deepcopy(
                    dict(request["aggregation_input_manifest"])
                )
            },
        )
        receipt = build_local_production_receipt(
            producer_id=_AGGREGATION_PRODUCER_ID,
            invocation_id=stable_identifier(
                "canonical-world-aggregation-production",
                request["request_digest"],
                sealed.binding["binding_id"],
            ),
            request_digest=request["request_digest"],
            output=sealed.binding,
        )
        return AggregationProduction(
            aggregation_producer_binding=sealed.binding,
            evidence_records=(sealed.evidence_paths,),
            production_receipt=receipt,
        )

    return CanonicalWorldProducerPlan(
        authority_projection=copy.deepcopy(projection),
        commission=copy.deepcopy(commission),
        commission_producer_binding=copy.deepcopy(commission_sealed.binding),
        world_requests=copy.deepcopy(requests),
        world_request_producer_bindings=copy.deepcopy(request_bindings),
        anchor_evidence_records=tuple(item.evidence_paths for item in frozen_base),
        world_producers=producers,
        aggregation_producer=aggregate,
    )


def run_canonical_world_support_production(
    *,
    store: DiscoveryTransactionStore,
    theory_generation: int,
    cycle_id: str,
    workspace: Path,
    world_specs: Mapping[str, Mapping[str, Any]],
    reflection_producer: PostResultReflectionProducer,
    run_root: Path | None = None,
    max_workers: int = 5,
    wave_timeout_seconds: float = 120.0,
) -> CanonicalSupportLaneResult:
    """Prepare real producers, then run the canonical serial commit protocol."""

    plan = prepare_canonical_world_producer_plan(
        store=store,
        theory_generation=theory_generation,
        workspace=workspace,
        world_specs=world_specs,
        reflection_producer=reflection_producer,
        run_root=run_root,
    )
    return run_canonical_theory_support_lane(
        store=store,
        theory_generation=theory_generation,
        cycle_id=cycle_id,
        commission=plan.commission,
        commission_producer_binding=plan.commission_producer_binding,
        world_requests=plan.world_requests,
        world_request_producer_bindings=plan.world_request_producer_bindings,
        anchor_evidence_records=plan.anchor_evidence_records,
        world_producers=plan.world_producers,
        aggregation_producer=plan.aggregation_producer,
        max_workers=max_workers,
        wave_timeout_seconds=wave_timeout_seconds,
    )


__all__ = [
    "CanonicalWorldProducerPlan",
    "PostResultReflectionProducer",
    "PostResultReflectionProduction",
    "compile_canonical_world_spec_family",
    "prepare_canonical_world_producer_plan",
    "run_canonical_world_support_production",
]
