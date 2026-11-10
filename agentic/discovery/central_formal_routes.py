# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Process-isolated orchestration for the closed conceptual-formal kernel.

This module gives Category Theory and HoTT a central but conditional role in
conceptual discovery.  One locally committed, byte-sealed conceptual core is
offered without mutation to four equal-opportunity routes: Category, HoTT,
their combination, and a capable nonformal control.  The formal routes reuse
the exact three Category and four HoTT transformations in
``formal_concept_transformations``; no eighth transformation can enter through
labels or configuration.

The existing task-relation compiler and registered formal-lens producers remain
the authority for task applicability and for replaying a separately
precommitted domain decision.  The seven-transformation kernel supplies the
constructive conceptual witnesses.  Each witness is replayed again in the
parent process before a route is accepted.  Cross-transformation writes are
merged in forward and reverse kernel order, so conflicts and order sensitivity
are explicit rather than hidden by a preferred evaluation order.

Every route is launched through :class:`ResearchWorkerAdapter` in a distinct
supervised process.  Exact request, response, worker, terminal, and terminal
barrier receipts are written create-once; the aggregate packet is written
last.  Failure, timeout, inapplicability, free completion, protected erasure,
conflict, order sensitivity, and an unchanged domain decision all quarantine a
route while preserving sibling results.

These records are local protocol evidence only.  They preserve source, truth,
creativity, depth, unification, physics-value, theorem, continuum,
Yang--Mills, and independence nulls.  No route is ranked merely because it uses
formal vocabulary, and experiments remain secondary theory-requested
falsifiers.
"""

from __future__ import annotations

import copy
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from skills.common.formal_concept_transformations import (
    CATEGORY_RELATION_KINDS,
    CONSTRUCTOR_IDS,
    HOTT_RELATION_KINDS,
    RELATION_KINDS,
    construct_descent_coherence,
    construct_equivalence_coherence,
    construct_functorial_transfer,
    construct_identity_transport,
    construct_mediator_factorization,
    construct_noncommutativity_localization,
    construct_path_independence,
    validate_conceptual_core,
    validate_semantic_delta,
)
from skills.common.task_relation_compiler import compile_task_relation

from .budgets import ResourceBudget, contained_path
from .contracts import (
    ROOT,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_identifier,
)
from .formal_lens_production import validate_formal_lens_production_request
from .formal_lens_registry import (
    ROUTE_ORDER as REGISTERED_ROUTE_ORDER,
    load_formal_lens_producer_registry,
)
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    receipt_summary,
    validate_research_worker_receipt,
)


SCHEMA_VERSION = "1.0.0"
ROUTE_ORDER = ("categorical", "hott", "combined", "capable_nonformal")
KERNEL_ORDER = (
    "noncommuting_composition",
    "mediating_factorization",
    "functorial_transfer",
    "identity_transport",
    "equivalence_coherence",
    "path_independence",
    "descent_coherence",
)
ROUTE_KERNEL = {
    "categorical": KERNEL_ORDER[:3],
    "hott": KERNEL_ORDER[3:],
    "combined": KERNEL_ORDER,
    "capable_nonformal": (),
}
_CONSTRUCTORS: dict[str, Callable[..., dict[str, Any]]] = {
    "noncommuting_composition": construct_noncommutativity_localization,
    "mediating_factorization": construct_mediator_factorization,
    "functorial_transfer": construct_functorial_transfer,
    "identity_transport": construct_identity_transport,
    "equivalence_coherence": construct_equivalence_coherence,
    "path_independence": construct_path_independence,
    "descent_coherence": construct_descent_coherence,
}
_FAULT_MODES = {None, "exit_nonzero", "invalid_json", "hang"}
_ENTITY_FIELDS = {
    "primitive": ("primitives", "primitive_id"),
    "relation": ("relations", "relation_id"),
    "observable": ("observables", "observable_id"),
    "inhabitant": ("inhabitants", "inhabitant_id"),
    "burden": ("burdens", "burden_id"),
}
_AUTHORITY_NULLS = (
    "source_authority",
    "truth",
    "creativity",
    "relevance",
    "conceptual_depth",
    "philosophical_understanding",
    "unification_power",
    "formal_advantage",
    "abstraction_value",
    "physics_value",
    "physical_equivalence",
    "theorem",
    "continuum_construction",
    "Osterwalder_Schrader_reconstruction",
    "spectral_result",
    "mass_gap",
    "Yang_Mills_result",
    "external_efficacy",
    "generalization",
    "hidden_input_independence",
    "cognitive_independence",
    "semantic_independence",
)
_COMPOSITION_POLICY = {
    "kernel_order": list(KERNEL_ORDER),
    "categorical_transformations": list(KERNEL_ORDER[:3]),
    "hott_transformations": list(KERNEL_ORDER[3:]),
    "route_order": list(ROUTE_ORDER),
    "execution_mode": "four_distinct_supervised_processes",
    "combination_mode": "independent_deltas_from_one_common_ancestor",
    "conflict_semantics": "same_typed_entity_with_different_payload_quarantines",
    "order_semantics": "forward_and_reverse_typed_write_folds_must_match",
    "terminal_barrier_required": True,
    "no_invocation_preference": True,
    "capable_nonformal_equal_opportunity": True,
    "process_overlap_hold_seconds": 0.25,
}
_DEFAULT_BUDGET = {
    "budget_id": "central-formal-route-worker-budget.v1",
    "wall_time_seconds": 30.0,
    "grace_period_seconds": 0.25,
    "cpu_seconds": 30.0,
    "memory_bytes": 768 * 1024 * 1024,
    "disk_bytes": 16 * 1024 * 1024,
    "network_bytes": 0,
    "token_count": 0,
    "request_count": 0,
    "cost_usd": 0.0,
    "absolute_deadline": None,
}


class CentralFormalRouteError(ValueError):
    """Fail-closed error for a central formal-route request or durable bundle."""


def _strict(raw: Mapping[str, Any], expected: set[str], label: str) -> None:
    if not isinstance(raw, Mapping) or set(raw) != expected:
        keys = set(raw) if isinstance(raw, Mapping) else set()
        raise CentralFormalRouteError(
            f"{label} keys differ; missing={sorted(expected - keys)}, "
            f"extra={sorted(keys - expected)}"
        )


def _without(raw: Mapping[str, Any], field: str) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in raw.items() if key != field}


def _seal(raw: Mapping[str, Any], field: str) -> dict[str, Any]:
    if field in raw:
        raise CentralFormalRouteError(f"cannot reseal existing {field}")
    result = copy.deepcopy(dict(raw))
    result[field] = canonical_digest(result)
    return result


def _assert_digest(raw: Mapping[str, Any], field: str, label: str) -> None:
    if raw.get(field) != canonical_digest(_without(raw, field)):
        raise CentralFormalRouteError(f"{label} {field} mismatch")


def _digest_text(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith("sha256:")
        or len(value) != 71
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        raise CentralFormalRouteError(f"{label} must be one lowercase sha256 digest")
    return value


def _kernel_is_closed() -> None:
    if (
        tuple(REGISTERED_ROUTE_ORDER) != ROUTE_ORDER
        or tuple(CATEGORY_RELATION_KINDS) != KERNEL_ORDER[:3]
        or tuple(HOTT_RELATION_KINDS) != KERNEL_ORDER[3:]
        or tuple(RELATION_KINDS) != KERNEL_ORDER
        or set(CONSTRUCTOR_IDS) != set(KERNEL_ORDER)
        or set(_CONSTRUCTORS) != set(KERNEL_ORDER)
    ):
        raise CentralFormalRouteError(
            "the central formal kernel is not the exact registered 3+4 transformation closure"
        )


def seal_transformation_plan(
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Seal one relation-specific plan without executing or grading it."""

    kind = relation_hypothesis.get("relation_kind")
    if kind not in KERNEL_ORDER:
        raise CentralFormalRouteError("transformation plan uses a label outside the closed kernel")
    core = {
        "plan_id": stable_identifier(
            "central-formal-transformation-plan",
            kind,
            relation_hypothesis,
            witness,
            consequence_contract,
        ),
        "relation_kind": kind,
        "relation_hypothesis": copy.deepcopy(dict(relation_hypothesis)),
        "witness": copy.deepcopy(dict(witness)),
        "consequence_contract": copy.deepcopy(dict(consequence_contract)),
    }
    return _seal(core, "plan_digest")


def build_core_commit(
    conceptual_core: Mapping[str, Any],
    formal_request: Mapping[str, Any],
    *,
    state_generation: int,
    source_transformation_receipt_digest: str,
) -> dict[str, Any]:
    """Commit one sealed transformed core before any route is selected."""

    core = validate_conceptual_core(conceptual_core)
    formal = validate_formal_lens_production_request(formal_request)
    source_digest = _digest_text(
        source_transformation_receipt_digest,
        "source_transformation_receipt_digest",
    )
    record = {
        "commit_id": stable_identifier(
            "central-formal-core-commit",
            core["content_digest"],
            formal["request_digest"],
            state_generation,
            source_digest,
        ),
        "core_digest": core["content_digest"],
        "state_generation": state_generation,
        "source_transformation_receipt_digest": source_digest,
        "formal_request_digest": formal["request_digest"],
        "central_creativity_packet_digest": formal["central_creativity_input"][
            "packet_digest"
        ],
        "current_literature_projection_digest": formal[
            "current_literature_projection"
        ]["projection_digest"],
        "authority_class": "local_committed_transformed_core_no_source_or_truth_authority",
        "sealed_before_routes": True,
        "committed": True,
    }
    return _seal(record, "commit_digest")


def build_central_formal_route_request(
    *,
    orchestration_id: str,
    identity: Mapping[str, Any],
    transformed_core: Mapping[str, Any],
    formal_lens_request: Mapping[str, Any],
    transformations: Mapping[str, Mapping[str, Any]],
    source_transformation_receipt_digest: str,
    route_fault_modes: Mapping[str, str | None] | None = None,
    worker_budget: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build and validate the exact common-core four-route request."""

    validate_identifier(orchestration_id, "orchestration_id")
    formal = validate_formal_lens_production_request(formal_lens_request)
    generation = identity.get("state_generation")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        raise CentralFormalRouteError("identity.state_generation must be a nonnegative integer")
    commit = build_core_commit(
        transformed_core,
        formal,
        state_generation=generation,
        source_transformation_receipt_digest=source_transformation_receipt_digest,
    )
    if set(transformations) != set(KERNEL_ORDER):
        raise CentralFormalRouteError("request requires exactly one plan for each closed-kernel kind")
    plans = [copy.deepcopy(dict(transformations[kind])) for kind in KERNEL_ORDER]
    faults = (
        {route_id: None for route_id in ROUTE_ORDER}
        if route_fault_modes is None
        else dict(route_fault_modes)
    )
    registry_binding = load_formal_lens_producer_registry()[1]
    raw = {
        "schema_version": SCHEMA_VERSION,
        "orchestration_id": orchestration_id,
        "identity": copy.deepcopy(dict(identity)),
        "transformed_core": copy.deepcopy(dict(transformed_core)),
        "core_commit": commit,
        "formal_lens_request": copy.deepcopy(formal),
        "formal_registry_binding": registry_binding,
        "transformations": plans,
        "composition_policy": copy.deepcopy(_COMPOSITION_POLICY),
        "route_fault_modes": faults,
        "worker_budget": copy.deepcopy(dict(worker_budget or _DEFAULT_BUDGET)),
        "authority_boundary": _authority_boundary(),
    }
    request = _seal(raw, "request_digest")
    return validate_central_formal_route_request(request)


def _authority_boundary() -> dict[str, Any]:
    return {
        "theory_first": True,
        "experiments_secondary_theory_requested_falsifiers_only": True,
        "automatic_theory_selection": False,
        "route_invocation_preference_authorized": False,
        "local_protocol_evidence_only": True,
        "source_authority_authorized": False,
        "truth_authorized": False,
        "creativity_authorized": False,
        "relevance_authorized": False,
        "conceptual_depth_authorized": False,
        "philosophical_understanding_authorized": False,
        "unification_power_authorized": False,
        "formal_advantage_authorized": False,
        "physics_value_authorized": False,
        "theorem_authorized": False,
        "continuum_authorized": False,
        "yang_mills_authorized": False,
        "hidden_input_independence_authorized": False,
        "cognitive_independence_authorized": False,
        "semantic_independence_authorized": False,
    }


def validate_central_formal_route_request(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the sealed core, 3+4 kernel, registry, and precommitted rule."""

    _kernel_is_closed()
    request = copy.deepcopy(dict(raw))
    _strict(
        request,
        {
            "schema_version",
            "orchestration_id",
            "identity",
            "transformed_core",
            "core_commit",
            "formal_lens_request",
            "formal_registry_binding",
            "transformations",
            "composition_policy",
            "route_fault_modes",
            "worker_budget",
            "authority_boundary",
            "request_digest",
        },
        "central formal-route request",
    )
    if request["schema_version"] != SCHEMA_VERSION:
        raise CentralFormalRouteError("central formal-route schema version drift")
    validate_identifier(request["orchestration_id"], "orchestration_id")
    _strict(
        request["identity"],
        {"target_id", "run_id", "branch_id", "state_generation"},
        "central formal-route identity",
    )
    for field in ("target_id", "run_id", "branch_id"):
        validate_identifier(request["identity"][field], f"identity.{field}")
    generation = request["identity"]["state_generation"]
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        raise CentralFormalRouteError("identity.state_generation must be a nonnegative integer")

    core = validate_conceptual_core(request["transformed_core"])
    formal = validate_formal_lens_production_request(request["formal_lens_request"])
    semantics = formal["task_case"]["task_semantics"]
    if (
        core["target_id"] != request["identity"]["target_id"]
        or core["target_id"] != formal["identity"]["target_id"]
        or core["obligation_id"] != formal["task_case"]["obligation_id"]
        or formal["identity"]["state_version"] != generation
    ):
        raise CentralFormalRouteError("core, route identity, and formal request do not share one target state")
    if (
        core["physical_carrier"] != semantics["physical_carrier"]
        or core["regime"] != semantics["regime"]
        or [row["statement"] for row in core["quantifiers"]] != semantics["quantifiers"]
    ):
        raise CentralFormalRouteError(
            "conceptual core and domain task differ in carrier, regime, or quantifiers"
        )

    commit = request["core_commit"]
    _strict(
        commit,
        {
            "commit_id",
            "core_digest",
            "state_generation",
            "source_transformation_receipt_digest",
            "formal_request_digest",
            "central_creativity_packet_digest",
            "current_literature_projection_digest",
            "authority_class",
            "sealed_before_routes",
            "committed",
            "commit_digest",
        },
        "conceptual core commit",
    )
    _assert_digest(commit, "commit_digest", "conceptual core commit")
    _digest_text(commit["source_transformation_receipt_digest"], "source receipt digest")
    expected_commit = {
        "core_digest": core["content_digest"],
        "state_generation": generation,
        "formal_request_digest": formal["request_digest"],
        "central_creativity_packet_digest": formal["central_creativity_input"][
            "packet_digest"
        ],
        "current_literature_projection_digest": formal[
            "current_literature_projection"
        ]["projection_digest"],
        "authority_class": "local_committed_transformed_core_no_source_or_truth_authority",
        "sealed_before_routes": True,
        "committed": True,
    }
    if any(commit[field] != value for field, value in expected_commit.items()):
        raise CentralFormalRouteError("conceptual core commit does not bind the common route ancestor")

    registry_binding = load_formal_lens_producer_registry()[1]
    if request["formal_registry_binding"] != registry_binding:
        raise CentralFormalRouteError("formal producer registry binding is stale or substituted")
    plans = request["transformations"]
    if not isinstance(plans, list) or len(plans) != len(KERNEL_ORDER):
        raise CentralFormalRouteError("central formal route requires seven ordered plans")
    for expected_kind, plan in zip(KERNEL_ORDER, plans, strict=True):
        _strict(
            plan,
            {
                "plan_id",
                "relation_kind",
                "relation_hypothesis",
                "witness",
                "consequence_contract",
                "plan_digest",
            },
            f"{expected_kind} transformation plan",
        )
        _assert_digest(plan, "plan_digest", f"{expected_kind} transformation plan")
        if (
            plan["relation_kind"] != expected_kind
            or plan["relation_hypothesis"].get("relation_kind") != expected_kind
        ):
            raise CentralFormalRouteError(
                "formal labels cannot substitute for an exact closed-kernel transformation"
            )
    if request["composition_policy"] != _COMPOSITION_POLICY:
        raise CentralFormalRouteError("composition, conflict, order, or equal-opportunity policy drift")
    faults = request["route_fault_modes"]
    if (
        not isinstance(faults, Mapping)
        or set(faults) != set(ROUTE_ORDER)
        or any(value not in _FAULT_MODES for value in faults.values())
    ):
        raise CentralFormalRouteError("route fault modes must cover the exact four-route order")
    try:
        ResourceBudget.from_mapping(request["worker_budget"])
    except (TypeError, ValueError) as exc:
        raise CentralFormalRouteError(f"invalid central route worker budget: {exc}") from exc
    if request["authority_boundary"] != _authority_boundary():
        raise CentralFormalRouteError("central formal-route authority nulls were weakened")
    _assert_digest(request, "request_digest", "central formal-route request")
    return request


class _ImmediateRouteContext:
    """Satisfy the registered callable contract inside one isolated process."""

    def __init__(self, route_id: str) -> None:
        self.route_id = route_id
        self.entered = False

    def await_start(self, route_id: str) -> None:
        if self.entered or route_id != self.route_id:
            raise CentralFormalRouteError("registered route entered a foreign or repeated start gate")
        self.entered = True


def _construct_delta(
    core: Mapping[str, Any], plan: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    kind = str(plan["relation_kind"])
    delta = _CONSTRUCTORS[kind](
        core,
        plan["relation_hypothesis"],
        plan["witness"],
        plan["consequence_contract"],
    )
    replay = validate_semantic_delta(delta)
    if replay["relation_kind"] != kind or replay["constructor_id"] != CONSTRUCTOR_IDS[kind]:
        raise CentralFormalRouteError("constructive witness replay returned a foreign kernel identity")
    return delta, replay


def _changed_entities(delta: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Project typed writes so forward/reverse folds expose hidden conflicts."""

    before = delta["before_core"]
    after = delta["after_core"]
    writes: list[dict[str, Any]] = []
    for entity_kind, (collection, id_field) in _ENTITY_FIELDS.items():
        before_rows = {row[id_field]: row for row in before[collection]}
        after_rows = {row[id_field]: row for row in after[collection]}
        for entity_id in sorted(set(before_rows) | set(after_rows)):
            old = before_rows.get(entity_id)
            new = after_rows.get(entity_id)
            if old != new:
                writes.append(
                    {
                        "entity_kind": entity_kind,
                        "entity_id": entity_id,
                        "payload": copy.deepcopy(new),
                    }
                )
    return writes


def _fold_writes(
    kinds: Sequence[str], writes_by_kind: Mapping[str, Sequence[Mapping[str, Any]]]
) -> str:
    state: dict[str, Any] = {}
    for kind in kinds:
        for write in writes_by_kind[kind]:
            key = f"{write['entity_kind']}:{write['entity_id']}"
            state[key] = copy.deepcopy(write["payload"])
    return canonical_digest(state)


def _composition_analysis(
    selected_kinds: Sequence[str], deltas: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    writes_by_kind = {
        kind: _changed_entities(delta)
        for kind, delta in zip(selected_kinds, deltas, strict=True)
    }
    by_entity: dict[str, list[dict[str, Any]]] = {}
    for kind in selected_kinds:
        for write in writes_by_kind[kind]:
            key = f"{write['entity_kind']}:{write['entity_id']}"
            by_entity.setdefault(key, []).append({"relation_kind": kind, **write})
    conflicts = []
    for entity_key, rows in sorted(by_entity.items()):
        payload_digests = {canonical_digest(row["payload"]) for row in rows}
        if len(rows) > 1 and len(payload_digests) > 1:
            conflicts.append(
                {
                    "entity_key": entity_key,
                    "relation_kinds": [row["relation_kind"] for row in rows],
                    "payload_digests": sorted(payload_digests),
                }
            )
    forward = _fold_writes(selected_kinds, writes_by_kind)
    reverse = _fold_writes(tuple(reversed(selected_kinds)), writes_by_kind)
    order_sensitive = forward != reverse
    record = {
        "mode": "independent_deltas_from_one_common_ancestor",
        "selected_relation_kinds": list(selected_kinds),
        "typed_write_set_digests": {
            kind: canonical_digest(writes_by_kind[kind]) for kind in selected_kinds
        },
        "conflicts": conflicts,
        "forward_fold_digest": forward,
        "reverse_fold_digest": reverse,
        "order_sensitive": order_sensitive,
        "composition_status": (
            "quarantined_conflicting_order_sensitive"
            if conflicts or order_sensitive
            else "commutative_common_ancestor_union"
        ),
    }
    return _seal(record, "composition_digest")


def _route_compilations(
    formal_request: Mapping[str, Any], route_id: str
) -> list[dict[str, Any]]:
    lenses = (
        ("categorical",)
        if route_id == "categorical"
        else ("hott",)
        if route_id == "hott"
        else ("categorical", "hott")
        if route_id == "combined"
        else ()
    )
    return [compile_task_relation(formal_request["task_case"], lens) for lens in lenses]


def _route_is_applicable(compilations: Sequence[Mapping[str, Any]], route_id: str) -> bool:
    return route_id == "capable_nonformal" or bool(compilations) and all(
        row["lens_selection"]["status"] == "applicable" for row in compilations
    )


def _quarantine_reasons(
    *,
    route_id: str,
    applicable: bool,
    deltas: Sequence[Mapping[str, Any]],
    registered_result: Mapping[str, Any],
    composition: Mapping[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if not applicable:
        reasons.append("inapplicable_task_relation")
    if route_id == "capable_nonformal":
        if not registered_result["rule_replay"]["actual_decision_changed"]:
            reasons.append("unchanged_domain_decision")
        return reasons
    if applicable and not deltas:
        reasons.append("label_only_no_constructive_witness")
    if any(
        row["construction"]["construction_origin"] == "free_completion_counterfactual"
        or row["obstruction_transition"]["after_status"] == "counterfactual_only"
        for row in deltas
    ):
        reasons.append("freely_adjoined_or_assumption_away")
    if any(row["observable_preservation"]["protected_erasure_detected"] for row in deltas):
        reasons.append("protected_observable_erasure")
    if composition["conflicts"]:
        reasons.append("conflicting_transformations")
    if composition["order_sensitive"]:
        reasons.append("order_sensitive_composition")
    if deltas and not any(
        row["obstruction_transition"]["decision_flip_authorized"] for row in deltas
    ):
        reasons.append("no_constructive_obstruction_removal")
    if not registered_result["rule_replay"]["actual_decision_changed"]:
        reasons.append("unchanged_domain_decision")
    if registered_result["rule_replay"]["replay_status"] == (
        "hypothetical_assumption_away_sensitivity"
    ):
        reasons.append("freely_adjoined_or_assumption_away")
    return list(dict.fromkeys(reasons))


def _physics_handback(
    request: Mapping[str, Any],
    route_id: str,
    registered_result: Mapping[str, Any],
    deltas: Sequence[Mapping[str, Any]],
    reasons: Sequence[str],
) -> dict[str, Any]:
    semantics = request["formal_lens_request"]["task_case"]["task_semantics"]
    replay = registered_result["rule_replay"]
    eligible = not reasons and route_id != "capable_nonformal"
    burdens = [
        {
            "relation_kind": row["relation_hypothesis"]["relation_kind"],
            "after_status": row["obstruction_transition"]["after_status"],
            "changed_burden": row["semantic_delta"]["changed_burden"],
        }
        for row in deltas
    ]
    if not burdens:
        burdens = [
            {
                "relation_kind": "capable_nonformal_control",
                "after_status": "unchanged",
                "changed_burden": registered_result["physics_handback"]["changed_burden"],
            }
        ]
    record = {
        "handback_id": stable_identifier(
            "central-formal-physics-handback",
            request["request_digest"],
            route_id,
            [row["content_digest"] for row in deltas],
            list(reasons),
        ),
        "route_id": route_id,
        "handback_status": (
            "eligible_internal_conceptual_candidate"
            if eligible
            else "quarantined_non_investment"
        ),
        "target_id": request["identity"]["target_id"],
        "obligation_id": request["transformed_core"]["obligation_id"],
        "physical_carrier": semantics["physical_carrier"],
        "regime": semantics["regime"],
        "quantifiers": copy.deepcopy(semantics["quantifiers"]),
        "changed_burdens": burdens,
        "correction": semantics["correction"],
        "falsifier": semantics["falsifier"],
        "physics_next_actions": [
            row["physics_handback"]["physics_next_action"] for row in deltas
        ],
        "untouched_physics_gates": copy.deepcopy(semantics["untouched_physics_gates"]),
        "precommitted_domain_decision": copy.deepcopy(replay["baseline_decision"]),
        "eligible_domain_decision": copy.deepcopy(
            replay["intervened_decision"] if eligible else replay["baseline_decision"]
        ),
        "counterfactual_route_decision": copy.deepcopy(replay["intervened_decision"]),
        "decision_changed": bool(eligible and replay["actual_decision_changed"]),
        "quarantine_reasons": list(reasons),
        "source_authority_status": "input_provenance_preserved_no_source_truth_authority",
        "experiment_role": "secondary_theory_requested_falsifier_only",
        "authority_nulls": list(_AUTHORITY_NULLS),
        "authority_boundary": _authority_boundary(),
    }
    return _seal(record, "handback_digest")


def _worker_records(
    route_id: str,
    plans: Sequence[Mapping[str, Any]],
    deltas: Sequence[Mapping[str, Any]],
    replays: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for plan, delta, replay in zip(plans, deltas, replays, strict=True):
        summary = {
            "relation_kind": plan["relation_kind"],
            "constructor_id": replay["constructor_id"],
            "after_status": replay["after_status"],
            "witness_digest": delta["construction"]["witness_digest"],
            "protected_erasure_detected": replay["protected_erasure_detected"],
        }
        records.append(
            {
                "task_id": plan["plan_id"],
                "category_check": (
                    {
                        **summary,
                        "mismatch_elements": (
                            ["protected_observable_erasure"]
                            if replay["protected_erasure_detected"]
                            else []
                        ),
                    }
                    if replay["lens"] == "categorical"
                    else None
                ),
                "hott_check": (
                    {
                        **summary,
                        "round_trip_holds": (
                            replay["after_status"] != "counterfactual_only"
                            and not replay["protected_erasure_detected"]
                        ),
                    }
                    if replay["lens"] == "hott"
                    else None
                ),
                "semantic_delta": copy.deepcopy(delta),
            }
        )
    if not records:
        records.append(
            {
                "task_id": f"{route_id}.equal-opportunity-control",
                "category_check": None,
                "hott_check": None,
                "semantic_delta": None,
            }
        )
    model_projection = [
        {
            "task_id": row["task_id"],
            "category": row["category_check"],
            "hott": row["hott_check"],
        }
        for row in records
    ]
    witness_projection = [
        {
            "task_id": row["task_id"],
            "category_mismatches": (
                row["category_check"].get("mismatch_elements", [])
                if isinstance(row["category_check"], Mapping)
                else []
            ),
            "hott_round_trip": (
                row["hott_check"].get("round_trip_holds")
                if isinstance(row["hott_check"], Mapping)
                else None
            ),
        }
        for row in records
    ]
    formal_execution = {
        "model_digest": canonical_digest(model_projection),
        "witness_digest": canonical_digest(witness_projection),
        "theorem_authorized": False,
        "continuum_authorized": False,
        "physics_value_authorized": False,
        "conceptual_advantage_authorized": False,
    }
    return records, formal_execution


def execute_central_formal_route_payload(payload_raw: Mapping[str, Any]) -> dict[str, Any]:
    """Execute one route deterministically inside a research-worker process."""

    payload = copy.deepcopy(dict(payload_raw))
    _strict(
        payload,
        {
            "schema_version",
            "route_id",
            "orchestration_request",
            "common_core_digest",
            "payload_digest",
        },
        "central formal worker payload",
    )
    _assert_digest(payload, "payload_digest", "central formal worker payload")
    route_id = payload["route_id"]
    if route_id not in ROUTE_ORDER:
        raise CentralFormalRouteError("worker payload names an unknown route")
    request = validate_central_formal_route_request(payload["orchestration_request"])
    if payload["common_core_digest"] != request["transformed_core"]["content_digest"]:
        raise CentralFormalRouteError("route received a substituted common conceptual core")

    bindings, registry_binding = load_formal_lens_producer_registry()
    binding = {row.route_id: row for row in bindings}[route_id]
    if registry_binding != request["formal_registry_binding"]:
        raise CentralFormalRouteError("worker registry differs from the request precommit")
    context = _ImmediateRouteContext(route_id)
    registered_result = binding.function(
        copy.deepcopy(request["formal_lens_request"]),
        context,
    )
    if not context.entered:
        raise CentralFormalRouteError("registered route did not enter its process-local start gate")

    compilations = _route_compilations(request["formal_lens_request"], route_id)
    applicable = _route_is_applicable(compilations, route_id)
    plan_by_kind = {row["relation_kind"]: row for row in request["transformations"]}
    selected_kinds = ROUTE_KERNEL[route_id] if applicable else ()
    selected_plans = [plan_by_kind[kind] for kind in selected_kinds]
    constructed = [
        _construct_delta(request["transformed_core"], plan) for plan in selected_plans
    ]
    deltas = [row[0] for row in constructed]
    replays = [row[1] for row in constructed]
    composition = _composition_analysis(selected_kinds, deltas)
    reasons = _quarantine_reasons(
        route_id=route_id,
        applicable=applicable,
        deltas=deltas,
        registered_result=registered_result,
        composition=composition,
    )
    handback = _physics_handback(
        request,
        route_id,
        registered_result,
        deltas,
        reasons,
    )
    records, formal_execution = _worker_records(
        route_id,
        selected_plans,
        deltas,
        replays,
    )
    return {
        "output_kind": "formal_lens",
        "route_id": route_id,
        "request_digest": request["request_digest"],
        "common_core_digest": request["transformed_core"]["content_digest"],
        "core_commit_digest": request["core_commit"]["commit_digest"],
        "formal_registry_binding_digest": registry_binding["binding_digest"],
        "kernel_binding": {
            "relation_kinds": list(KERNEL_ORDER),
            "constructor_ids": [
                CONSTRUCTOR_IDS[kind] for kind in KERNEL_ORDER
            ],
            "closed_kernel": True,
        },
        "task_relation_compilations": compilations,
        "registered_domain_route": registered_result,
        "composition": composition,
        "records": records,
        "formal_execution": formal_execution,
        "physics_handback": handback,
        "disposition": (
            "eligible_internal_conceptual_candidate"
            if not reasons and route_id != "capable_nonformal"
            else "quarantined_non_investment"
        ),
        "equal_opportunity": {
            "executed": True,
            "matched_common_core": True,
            "invocation_bonus": False,
            "ranking_or_preference_emitted": False,
        },
        "authority_boundary": _authority_boundary(),
    }


def _route_payload(request: Mapping[str, Any], route_id: str) -> dict[str, Any]:
    return _seal(
        {
            "schema_version": SCHEMA_VERSION,
            "route_id": route_id,
            "orchestration_request": copy.deepcopy(dict(request)),
            "common_core_digest": request["transformed_core"]["content_digest"],
        },
        "payload_digest",
    )


def _write_immutable_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Create canonical JSON once, or verify that an existing file is exact."""

    data = canonical_json(payload) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
            raise CentralFormalRouteError(f"immutable artifact collision at {path}")
        return
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except Exception:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise


def _load_object(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise CentralFormalRouteError(f"required artifact is not one regular file: {path}")
    try:
        raw = json.loads(path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CentralFormalRouteError(f"artifact is not JSON: {path}") from exc
    if not isinstance(raw, dict):
        raise CentralFormalRouteError(f"artifact root must be an object: {path}")
    return raw


def _descriptor(role: str, relative_path: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    data = canonical_json(payload) + b"\n"
    return {
        "role": role,
        "relative_path": relative_path,
        "sha256": bytes_digest(data),
        "byte_length": len(data),
    }


def _process_receipt_relative_path(
    bundle: Path, receipt: Mapping[str, Any], receipt_path: Path
) -> str:
    try:
        return receipt_path.relative_to(bundle).as_posix()
    except ValueError as exc:
        raise CentralFormalRouteError("research-worker receipt escaped the formal bundle") from exc


def _response_record(
    route_id: str,
    worker_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    return _seal(
        {
            "response_id": stable_identifier(
                "central-formal-route-response",
                route_id,
                worker_receipt["content_digest"],
            ),
            "route_id": route_id,
            "worker_receipt_id": worker_receipt["receipt_id"],
            "worker_receipt_digest": worker_receipt["content_digest"],
            "outcome_status": worker_receipt["outcome_status"],
            "output": copy.deepcopy(
                worker_receipt["response_payload"]["output"]
                if worker_receipt["outcome_status"] == "accepted"
                else None
            ),
            "failure": copy.deepcopy(worker_receipt["failure"]),
        },
        "response_digest",
    )


def _terminal_record(
    bundle: Path,
    route_id: str,
    request_payload: Mapping[str, Any],
    response: Mapping[str, Any],
    worker_receipt: Mapping[str, Any],
    worker_receipt_path: Path,
) -> dict[str, Any]:
    output = response["output"]
    status = (
        "failed"
        if worker_receipt["outcome_status"] != "accepted"
        else "completed"
        if output["disposition"] == "eligible_internal_conceptual_candidate"
        else "quarantined"
    )
    event = worker_receipt["process_event"]
    return _seal(
        {
            "terminal_id": stable_identifier(
                "central-formal-route-terminal",
                route_id,
                request_payload["payload_digest"],
                response["response_digest"],
            ),
            "route_id": route_id,
            "terminal_status": status,
            "common_core_digest": request_payload["common_core_digest"],
            "route_request_digest": request_payload["payload_digest"],
            "response_digest": response["response_digest"],
            "worker_receipt_id": worker_receipt["receipt_id"],
            "worker_receipt_digest": worker_receipt["content_digest"],
            "worker_receipt_relative_path": _process_receipt_relative_path(
                bundle, worker_receipt, worker_receipt_path
            ),
            "process_id": event["pid"],
            "process_started_at": event["started_at"],
            "process_completed_at": event["completed_at"],
            "process_status": worker_receipt["process_status"],
            "process_termination": event["termination"],
            "descendant_leak_detected": event["descendant_leak_detected"],
            "stdout_drain_incomplete": event["stdout_drain_incomplete"],
            "stderr_drain_incomplete": event["stderr_drain_incomplete"],
            "late_output_admissible": False,
            "failure": copy.deepcopy(worker_receipt["failure"]),
        },
        "terminal_digest",
    )


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _terminal_barrier(
    request: Mapping[str, Any],
    terminals: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    pids = [row["process_id"] for row in terminals]
    distinct_processes = all(isinstance(pid, int) and pid > 0 for pid in pids) and (
        len(set(pids)) == len(ROUTE_ORDER)
    )
    overlap = False
    if distinct_processes:
        latest_start = max(_parse_time(row["process_started_at"]) for row in terminals)
        earliest_end = min(_parse_time(row["process_completed_at"]) for row in terminals)
        overlap = latest_start < earliest_end
    all_terminal = len(terminals) == len(ROUTE_ORDER) and all(
        row["terminal_status"] in {"completed", "quarantined", "failed"}
        and not row["descendant_leak_detected"]
        and not row["stdout_drain_incomplete"]
        and not row["stderr_drain_incomplete"]
        for row in terminals
    )
    record = {
        "barrier_id": stable_identifier(
            "central-formal-terminal-barrier",
            request["request_digest"],
            [row["terminal_digest"] for row in terminals],
        ),
        "expected_routes": list(ROUTE_ORDER),
        "terminal_ids": [row["terminal_id"] for row in terminals],
        "terminal_digests": [row["terminal_digest"] for row in terminals],
        "all_routes_terminal": all_terminal,
        "all_routes_started_as_distinct_processes": distinct_processes,
        "parallel_process_overlap_observed": overlap,
        "collected_after_all_process_futures_terminal": True,
        "late_outputs_admissible": False,
        "completed_routes": [
            row["route_id"] for row in terminals if row["terminal_status"] == "completed"
        ],
        "quarantined_routes": [
            row["route_id"] for row in terminals if row["terminal_status"] == "quarantined"
        ],
        "failed_routes": [
            row["route_id"] for row in terminals if row["terminal_status"] == "failed"
        ],
    }
    return _seal(record, "barrier_digest")


def _artifact_manifest(
    request: Mapping[str, Any],
    route_payloads: Mapping[str, Mapping[str, Any]],
    responses: Mapping[str, Mapping[str, Any]],
    terminals: Mapping[str, Mapping[str, Any]],
    worker_receipts: Mapping[str, Mapping[str, Any]],
    barrier: Mapping[str, Any],
) -> dict[str, Any]:
    files = [_descriptor("orchestration_request", "request.json", request)]
    for route_id in ROUTE_ORDER:
        files.extend(
            [
                _descriptor(
                    "route_request",
                    f"route-requests/{route_id}.json",
                    route_payloads[route_id],
                ),
                _descriptor(
                    "route_response",
                    f"route-responses/{route_id}.json",
                    responses[route_id],
                ),
                _descriptor(
                    "route_terminal",
                    f"route-terminals/{route_id}.json",
                    terminals[route_id],
                ),
                _descriptor(
                    "research_worker_receipt",
                    terminals[route_id]["worker_receipt_relative_path"],
                    worker_receipts[route_id],
                ),
            ]
        )
    files.append(_descriptor("terminal_barrier", "terminal-barrier.json", barrier))
    return {
        "bundle_relative_root": request["orchestration_id"],
        "files": files,
        "atomic_last_packet_path": "central-formal-route-packet.json",
    }


def _build_packet(
    request: Mapping[str, Any],
    route_payloads: Mapping[str, Mapping[str, Any]],
    responses: Mapping[str, Mapping[str, Any]],
    terminals: Mapping[str, Mapping[str, Any]],
    worker_receipts: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    ordered_terminals = [terminals[route_id] for route_id in ROUTE_ORDER]
    barrier = _terminal_barrier(request, ordered_terminals)
    if not barrier["all_routes_terminal"]:
        raise CentralFormalRouteError("terminal barrier observed an unterminated or leaking route")
    packet = _seal(
        {
            "schema_version": SCHEMA_VERSION,
            "packet_id": stable_identifier(
                "central-formal-route-packet",
                request["request_digest"],
                barrier["barrier_digest"],
            ),
            "orchestration_id": request["orchestration_id"],
            "request_digest": request["request_digest"],
            "common_core_digest": request["transformed_core"]["content_digest"],
            "core_commit_digest": request["core_commit"]["commit_digest"],
            "formal_registry_binding": copy.deepcopy(
                request["formal_registry_binding"]
            ),
            "route_terminals": copy.deepcopy(ordered_terminals),
            "terminal_barrier": barrier,
            "production_status": (
                "partial_failure"
                if barrier["failed_routes"]
                else "complete_with_quarantine"
                if barrier["quarantined_routes"]
                else "complete_internal_protocol"
            ),
            "preferred_route": None,
            "selection_rule": "no_route_preferred_by_formal_invocation",
            "artifact_manifest": _artifact_manifest(
                request,
                route_payloads,
                responses,
                terminals,
                worker_receipts,
                barrier,
            ),
            "authority_boundary": _authority_boundary(),
        },
        "packet_digest",
    )
    return packet, barrier


def _approved_dependencies() -> list[Path]:
    return [
        ROOT / "agentic/discovery/central_formal_routes.py",
        ROOT / "agentic/discovery/formal_lens_production.py",
        ROOT / "agentic/discovery/formal_lens_registry.py",
        ROOT / "agentic/registries/formal_lens_producer_registry.yaml",
        ROOT / "agentic/spec/formal_conceptual_delta_v2.schema.json",
        ROOT / "agentic/spec/formal_lens_production_packet.schema.json",
        ROOT / "agentic/spec/formal_lens_production_request.schema.json",
        ROOT / "agentic/spec/task_relation_compilation.schema.json",
        ROOT / "skills/common/formal_concept_transformations.py",
        ROOT / "skills/common/task_relation_compiler.py",
        ROOT / "skills/common/abstraction_formal_reasoning.py",
        ROOT / "skills/common/formal_dependency_authority.py",
        ROOT / "skills/common/theory_atlas_defect_compiler.py",
    ]


def run_central_formal_routes(
    request_raw: Mapping[str, Any],
    output_root: Path | str,
) -> dict[str, Any]:
    """Run the four routes concurrently in distinct processes and seal a bundle."""

    request = validate_central_formal_route_request(request_raw)
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    bundle = contained_path(root, request["orchestration_id"])
    bundle.mkdir(parents=True, exist_ok=True)
    packet_path = contained_path(bundle, "central-formal-route-packet.json")
    if packet_path.exists():
        return validate_central_formal_route_bundle(bundle)

    _write_immutable_json(contained_path(bundle, "request.json"), request)
    route_payloads = {
        route_id: _route_payload(request, route_id) for route_id in ROUTE_ORDER
    }
    for route_id, payload in route_payloads.items():
        _write_immutable_json(
            contained_path(bundle, "route-requests", f"{route_id}.json"),
            payload,
        )

    adapter = ResearchWorkerAdapter(
        study_id="central-formal-route-process-wave",
        run_root=contained_path(bundle, "processes"),
        worker_script=ROOT / "agentic/scripts/run_central_formal_route_worker.py",
        approved_dependency_paths=_approved_dependencies(),
        input_limit_bytes=8 * 1024 * 1024,
        stdout_limit_bytes=16 * 1024 * 1024,
        stderr_limit_bytes=512 * 1024,
    )

    def launch(route_id: str) -> dict[str, Any]:
        return adapter.invoke(
            role="formal_lens",
            operation="formal_lens",
            invocation_context={
                "orchestration_id": request["orchestration_id"],
                "route_id": route_id,
                "request_digest": request["request_digest"],
                "common_core_digest": request["transformed_core"]["content_digest"],
            },
            payload=route_payloads[route_id],
            budget=request["worker_budget"],
            fault_mode=request["route_fault_modes"][route_id],
        )

    worker_receipts: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=len(ROUTE_ORDER)) as pool:
        futures = {pool.submit(launch, route_id): route_id for route_id in ROUTE_ORDER}
        for future in as_completed(futures):
            worker_receipts[futures[future]] = future.result()

    responses: dict[str, dict[str, Any]] = {}
    terminals: dict[str, dict[str, Any]] = {}
    for route_id in ROUTE_ORDER:
        receipt = worker_receipts[route_id]
        receipt_path = contained_path(
            adapter.run_directory,
            *Path(receipt["receipt_ref"]).parts,
        )
        response = _response_record(route_id, receipt)
        terminal = _terminal_record(
            bundle,
            route_id,
            route_payloads[route_id],
            response,
            receipt,
            receipt_path,
        )
        responses[route_id] = response
        terminals[route_id] = terminal
        _write_immutable_json(
            contained_path(bundle, "route-responses", f"{route_id}.json"),
            response,
        )
        _write_immutable_json(
            contained_path(bundle, "route-terminals", f"{route_id}.json"),
            terminal,
        )

    packet, barrier = _build_packet(
        request,
        route_payloads,
        responses,
        terminals,
        worker_receipts,
    )
    _write_immutable_json(contained_path(bundle, "terminal-barrier.json"), barrier)
    _write_immutable_json(packet_path, packet)
    return validate_central_formal_route_bundle(bundle)


def _verify_descriptor(bundle: Path, row: Mapping[str, Any]) -> None:
    path = contained_path(bundle, *Path(row["relative_path"]).parts)
    if path.is_symlink() or not path.is_file():
        raise CentralFormalRouteError("manifest artifact is absent or not regular")
    data = path.read_bytes()
    if len(data) != row["byte_length"] or bytes_digest(data) != row["sha256"]:
        raise CentralFormalRouteError("manifest artifact bytes differ from the sealed descriptor")


def validate_central_formal_route_bundle(bundle_path: Path | str) -> dict[str, Any]:
    """Reopen all immutable artifacts and independently replay accepted witnesses."""

    bundle = Path(bundle_path).resolve()
    request = validate_central_formal_route_request(
        _load_object(contained_path(bundle, "request.json"))
    )
    if bundle.name != request["orchestration_id"]:
        raise CentralFormalRouteError("bundle path differs from the orchestration identity")
    route_payloads: dict[str, dict[str, Any]] = {}
    responses: dict[str, dict[str, Any]] = {}
    terminals: dict[str, dict[str, Any]] = {}
    worker_receipts: dict[str, dict[str, Any]] = {}
    for route_id in ROUTE_ORDER:
        payload = _load_object(
            contained_path(bundle, "route-requests", f"{route_id}.json")
        )
        expected_payload = _route_payload(request, route_id)
        if payload != expected_payload:
            raise CentralFormalRouteError("route request substituted the common conceptual core")
        route_payloads[route_id] = payload

        response = _load_object(
            contained_path(bundle, "route-responses", f"{route_id}.json")
        )
        _assert_digest(response, "response_digest", f"{route_id} response")
        terminal = _load_object(
            contained_path(bundle, "route-terminals", f"{route_id}.json")
        )
        _assert_digest(terminal, "terminal_digest", f"{route_id} terminal")
        if response["route_id"] != route_id or terminal["route_id"] != route_id:
            raise CentralFormalRouteError("response or terminal route identity mismatch")
        receipt_path = contained_path(
            bundle, *Path(terminal["worker_receipt_relative_path"]).parts
        )
        receipt = validate_research_worker_receipt(
            _load_object(receipt_path),
            receipt_path=receipt_path,
            require_live_authority=response["outcome_status"] == "accepted",
        )
        receipt_summary(receipt, receipt_path=receipt_path)
        expected_response = _response_record(route_id, receipt)
        if response != expected_response:
            raise CentralFormalRouteError("route response differs from its worker receipt")
        expected_terminal = _terminal_record(
            bundle,
            route_id,
            payload,
            response,
            receipt,
            receipt_path,
        )
        if terminal != expected_terminal:
            raise CentralFormalRouteError("route terminal differs from process evidence")
        if receipt["outcome_status"] == "accepted":
            expected_output = execute_central_formal_route_payload(payload)
            if canonical_json(response["output"]) != canonical_json(expected_output):
                raise CentralFormalRouteError(
                    "accepted route output differs from independent constructive replay"
                )
        responses[route_id] = response
        terminals[route_id] = terminal
        worker_receipts[route_id] = receipt

    packet, expected_barrier = _build_packet(
        request,
        route_payloads,
        responses,
        terminals,
        worker_receipts,
    )
    barrier = _load_object(contained_path(bundle, "terminal-barrier.json"))
    if barrier != expected_barrier:
        raise CentralFormalRouteError("terminal barrier differs from exact terminal receipts")
    disk_packet = _load_object(
        contained_path(bundle, "central-formal-route-packet.json")
    )
    if disk_packet != packet:
        raise CentralFormalRouteError("central formal-route packet differs from exact replay")
    for descriptor in packet["artifact_manifest"]["files"]:
        _verify_descriptor(bundle, descriptor)
    for directory, expected_names in (
        ("route-requests", {f"{route_id}.json" for route_id in ROUTE_ORDER}),
        ("route-responses", {f"{route_id}.json" for route_id in ROUTE_ORDER}),
        ("route-terminals", {f"{route_id}.json" for route_id in ROUTE_ORDER}),
    ):
        actual = {
            path.name
            for path in contained_path(bundle, directory).iterdir()
            if path.is_file()
        }
        if actual != expected_names:
            raise CentralFormalRouteError(
                f"unexpected or late artifact in {directory}: {sorted(actual ^ expected_names)}"
            )
    return disk_packet


__all__ = [
    "CentralFormalRouteError",
    "KERNEL_ORDER",
    "ROUTE_KERNEL",
    "ROUTE_ORDER",
    "build_central_formal_route_request",
    "build_core_commit",
    "execute_central_formal_route_payload",
    "run_central_formal_routes",
    "seal_transformation_plan",
    "validate_central_formal_route_bundle",
    "validate_central_formal_route_request",
]
