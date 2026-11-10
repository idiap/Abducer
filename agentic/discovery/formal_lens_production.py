# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Constructive, task-semantic Category/HoTT production with physics handback.

Category Theory and HoTT are useful here as languages for inventing mediators,
transport, and higher coherence, not as prestige labels or automatic truth
engines.  This module runs four registered routes over one byte-identical
ancestor: categorical completion, HoTT coherence completion, their conjunction,
and a capable nonformal control.  The formal routes first replay a meaning-bound
finite countermodel from the existing formal kernel.  They may alter a separately
precommitted domain decision only after constructing and validating a new model:

* the categorical route builds the finite coequalizer of two noncommuting
  composites and verifies its commuting square and finite factorization law;
* the HoTT route adjoins exact pointwise paths and one bounded level-two
  coherence cell while keeping judgmental equality, identity paths,
  equivalence, truncation, universe, and univalence claims distinct.

If construction is explicitly unavailable, a predicate toggle is evaluated only
as ``hypothetical_assumption_away_sensitivity`` and quarantined.  A constructed
model whose frozen decision does not change is also quarantined.  Every route
returns the exact carrier, regime, quantifiers, changed burden, correction,
falsifier, untouched physics gates, and authority nulls.  Thus finite structure
can redirect reflection without becoming evidence of physics value, physical
equivalence, a theorem, a continuum construction, a mass gap, or Yang--Mills.

The four routes synchronize through a real in-process thread barrier.  Their
receipts truthfully state that no process/kernel/filesystem/network isolation or
cognitive independence was established.  The CLI persists one immutable request,
four terminal receipts, and one terminal barrier before writing the packet last;
retry reopens exact bytes rather than silently replacing them.
"""

from __future__ import annotations

import copy
import itertools
import json
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Mapping, Sequence

from skills.common.abstraction_formal_reasoning import (
    build_category_model_and_witness,
    build_hott_model_and_witness,
    validate_category_model,
    validate_hott_model,
)
from skills.common.task_relation_compiler import (
    build_task_relation_model_binding,
    compile_task_relation,
    validate_task_relation_model_binding,
)

from .contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    load_json,
    stable_identifier,
    validate_payload,
)
from .formal_lens_registry import (
    REGISTRY_PATH,
    ROUTE_ORDER,
    FormalLensProducerBinding,
    load_formal_lens_producer_registry,
)


REQUEST_SCHEMA = "formal_lens_production_request.schema.json"
PACKET_SCHEMA = "formal_lens_production_packet.schema.json"
_ROUTE_KINDS = {
    "categorical": "category_theory",
    "hott": "homotopy_type_theory",
    "combined": "combined_formal",
    "capable_nonformal": "capable_nonformal_control",
}
_ISOLATION_ASSURANCE = {
    "process_isolation": False,
    "kernel_isolation": False,
    "filesystem_isolation": False,
    "network_isolation": False,
    "hidden_input_independence": False,
    "cognitive_independence": False,
    "semantic_independence": False,
}
_EXECUTION_CONTRACT = {
    "scheduler": "ThreadPoolExecutor",
    "max_workers": 4,
    "start_barrier_parties": 4,
    "routes_share_only_frozen_request_bytes": True,
    "route_results_collected_after_terminal_barrier": True,
    "execution_backend": "shared_process_thread_pool",
    "process_isolation": False,
    "kernel_isolation": False,
    "filesystem_isolation": False,
    "network_isolation": False,
    "hidden_input_independence_authorized": False,
    "cognitive_independence_authorized": False,
    "semantic_independence_authorized": False,
    "claim_scope": "concurrent_local_protocol_routes_only",
}
_AUTHORITY_NULLS = [
    "external_or_cognitive_independence",
    "creativity",
    "relevance",
    "conceptual_depth",
    "philosophical_understanding",
    "unification_power",
    "abstraction_value",
    "physics_value",
    "physical_equivalence",
    "continuum_construction",
    "Osterwalder_Schrader_reconstruction",
    "theorem",
    "spectral_result",
    "mass_gap",
    "Yang_Mills_result",
]
_AUTHORITY_BOUNDARY = {
    "theory_first": True,
    "experiments_secondary": True,
    "automatic_theory_selection": False,
    "formal_routes_internal_only": True,
    "truth_authorized": False,
    "creativity_authorized": False,
    "conceptual_depth_authorized": False,
    "unification_power_authorized": False,
    "abstraction_value_authorized": False,
    "physics_value_authorized": False,
    "theorem_authorized": False,
    "continuum_authorized": False,
    "yang_mills_authorized": False,
    "publication_authorized": False,
}


class FormalLensProductionError(ContractError):
    """Raised when constructive production or exact replay fails closed."""


def _without(record: Mapping[str, Any], field: str) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in record.items() if key != field}


def _assert_self_digest(record: Mapping[str, Any], field: str, label: str) -> None:
    if record.get(field) != canonical_digest(_without(record, field)):
        raise FormalLensProductionError(f"{label} digest mismatch")


def _seal(record: dict[str, Any], field: str) -> dict[str, Any]:
    if field in record:
        raise FormalLensProductionError(f"cannot reseal existing {field}")
    record[field] = canonical_digest(record)
    return record


def _decision(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Project a decision without a task-relation trigger annotation."""

    return {
        "decision_id": raw["decision_id"],
        "decision_kind": raw["decision_kind"],
        "action": raw["action"],
        "target_burden_id": raw["target_burden_id"],
    }


def _evaluate_rule(rule: Mapping[str, Any], values: Mapping[str, bool]) -> dict[str, Any]:
    """Replay the separately precommitted, first-match decision rule."""

    for clause in sorted(rule["clauses"], key=lambda row: row["priority"]):
        if all(values[item["predicate_id"]] is item["equals"] for item in clause["all_of"]):
            return _decision(clause["decision"])
    return _decision(rule["default_decision"])


def validate_formal_lens_production_request(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Validate all cross-object digests and the independent decision precommit."""

    request = copy.deepcopy(dict(raw))
    validate_payload(request, REQUEST_SCHEMA)
    task_case = request["task_case"]
    semantics = task_case["task_semantics"]
    if request["identity"]["target_id"] != task_case["target_id"]:
        raise FormalLensProductionError("request identity and task target differ")
    if request["task_case_digest"] != canonical_digest(task_case):
        raise FormalLensProductionError("task case digest mismatch")
    creativity = request["central_creativity_input"]
    if creativity["packet_digest"] != canonical_digest(creativity["content"]):
        raise FormalLensProductionError("central creativity packet digest mismatch")
    literature = request["current_literature_projection"]
    if literature["projection_digest"] != canonical_digest(literature["content"]):
        raise FormalLensProductionError("current literature projection digest mismatch")

    rule = request["domain_decision_rule"]
    _assert_self_digest(rule, "rule_digest", "domain decision rule")
    precommit = request["domain_decision_rule_precommit"]
    _assert_self_digest(precommit, "precommit_digest", "domain decision rule precommit")
    if (
        precommit["rule_id"] != rule["rule_id"]
        or precommit["rule_digest"] != rule["rule_digest"]
        or precommit["committed_before_formal_routes"] is not True
    ):
        raise FormalLensProductionError("decision precommit does not bind the frozen rule")

    ancestor = request["frozen_task_semantic_ancestor"]
    _assert_self_digest(ancestor, "ancestor_digest", "frozen task-semantic ancestor")
    expected_ancestor = {
        "task_case_digest": request["task_case_digest"],
        "central_creativity_packet_digest": creativity["packet_digest"],
        "current_literature_projection_digest": literature["projection_digest"],
        "domain_decision_rule_digest": rule["rule_digest"],
    }
    if any(ancestor[field] != value for field, value in expected_ancestor.items()):
        raise FormalLensProductionError("frozen ancestor does not bind every semantic input")
    if ancestor["state_generation"] != request["identity"]["state_version"]:
        raise FormalLensProductionError("frozen ancestor generation differs from request state")
    _assert_self_digest(request, "request_digest", "formal-lens production request")

    predicates = rule["predicates"]
    predicate_ids = [row["predicate_id"] for row in predicates]
    if len(predicate_ids) != len(set(predicate_ids)):
        raise FormalLensProductionError("decision predicates must have unique IDs")
    predicate_set = set(predicate_ids)
    priorities = [row["priority"] for row in rule["clauses"]]
    clause_ids = [row["clause_id"] for row in rule["clauses"]]
    if len(priorities) != len(set(priorities)) or len(clause_ids) != len(set(clause_ids)):
        raise FormalLensProductionError("decision clauses need unique IDs and priorities")
    for clause in rule["clauses"]:
        condition_ids = [row["predicate_id"] for row in clause["all_of"]]
        if len(condition_ids) != len(set(condition_ids)) or not set(condition_ids) <= predicate_set:
            raise FormalLensProductionError("decision clause has duplicate or unknown predicates")

    bindings = rule["obstruction_bindings"]
    categorical = set(bindings["categorical"])
    hott = set(bindings["hott"])
    if not categorical <= predicate_set or not hott <= predicate_set or categorical & hott:
        raise FormalLensProductionError("lens obstruction predicates must be known and disjoint")
    baseline = {row["predicate_id"]: row["baseline_value"] for row in predicates}
    if any(baseline[predicate_id] for predicate_id in categorical | hott):
        raise FormalLensProductionError("an obstruction-bound predicate cannot be true at baseline")
    baseline_decision = _evaluate_rule(rule, baseline)
    if baseline_decision != _decision(semantics["incumbent_decision"]):
        raise FormalLensProductionError("precommitted baseline rule does not replay the incumbent decision")

    obligation_id = task_case["obligation_id"]
    all_decisions = [
        rule["default_decision"],
        *(row["decision"] for row in rule["clauses"]),
        semantics["incumbent_decision"],
        *semantics["lens_decisions"].values(),
    ]
    if any(row["target_burden_id"] != obligation_id for row in all_decisions):
        raise FormalLensProductionError("a domain decision targets a foreign burden")
    relation_ids = {row["relation_id"] for row in semantics["task_relations"]}
    if len(relation_ids) != len(semantics["task_relations"]):
        raise FormalLensProductionError("task relation identifiers must be unique")
    for lens, candidate in semantics["lens_decisions"].items():
        if candidate["trigger_relation_id"] not in relation_ids:
            raise FormalLensProductionError(f"{lens} decision cites an unknown task relation")
    return request


class _RouteExecutionContext:
    """Coordinate a real concurrent start without claiming worker isolation."""

    def __init__(self, barrier: threading.Barrier | None) -> None:
        self._barrier = barrier
        self._lock = threading.Lock()
        self._entered: set[str] = set()
        self._thread_ids: set[int] = set()

    def await_start(self, route_id: str) -> None:
        if route_id not in ROUTE_ORDER:
            raise FormalLensProductionError(f"unknown route entered start barrier: {route_id}")
        with self._lock:
            if route_id in self._entered:
                raise FormalLensProductionError(f"route entered the start barrier twice: {route_id}")
            self._entered.add(route_id)
            self._thread_ids.add(threading.get_ident())
        if self._barrier is not None:
            try:
                self._barrier.wait(timeout=30.0)
            except threading.BrokenBarrierError as exc:
                raise FormalLensProductionError("formal-lens concurrent start barrier broke") from exc

    def assert_parallel_wave(self) -> None:
        if self._barrier is None:
            return
        if self._entered != set(ROUTE_ORDER) or len(self._thread_ids) != len(ROUTE_ORDER):
            raise FormalLensProductionError("formal routes did not occupy four concurrent worker threads")


def _baseline_formal_artifact(
    request: Mapping[str, Any], lens: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Recompile task meaning and replay one exact finite obstruction."""

    case = request["task_case"]
    compilation = compile_task_relation(case, lens)
    if compilation["lens_selection"]["status"] != "applicable":
        raise FormalLensProductionError(f"{lens} route is not applicable to a declared task relation")
    binding = build_task_relation_model_binding(compilation)
    prefix = compilation["formal_projection"]["semantic_prefix"]
    obligation_id = case["obligation_id"]
    if lens == "categorical":
        model, witness = build_category_model_and_witness(
            prefix,
            obligation_id,
            _task_relation_binding=binding,
        )
        replay = validate_category_model(model, witness, {obligation_id})
    else:
        model, witness = build_hott_model_and_witness(
            prefix,
            obligation_id,
            _task_relation_binding=binding,
        )
        replay = validate_hott_model(model, witness, {obligation_id})
    validate_task_relation_model_binding(compilation, model, witness)
    baseline = {
        "compilation_digest": compilation["compilation_digest"],
        "model_digest": canonical_digest(model),
        "witness_digest": canonical_digest(witness),
        "countermodel_output_digest": canonical_digest(replay),
        "countermodel_result": replay["result"],
        "authority_boundary": "meaning_bound_finite_obstruction_only_no_legacy_decision_authority",
    }
    baseline["artifact_digest"] = canonical_digest(baseline)
    return compilation, model, witness, {**replay, "baseline_artifact_digest": baseline["artifact_digest"]}


def _obstruction(
    lens: str,
    compilation: Mapping[str, Any],
    model: Mapping[str, Any],
    witness: Mapping[str, Any],
    replay: Mapping[str, Any],
) -> dict[str, Any]:
    counterexamples: list[dict[str, Any]] = []
    for row in replay["counterexamples"]:
        if lens == "categorical":
            counterexamples.append(
                {
                    "input_id": row["source_element_id"],
                    "left_output_id": row["left_output_element_id"],
                    "right_output_id": row["right_output_element_id"],
                    "left_truth": None,
                    "right_truth": None,
                }
            )
        else:
            counterexamples.append(
                {
                    "input_id": row["source_term_id"],
                    "left_output_id": row["left_target_term_id"],
                    "right_output_id": row["right_target_term_id"],
                    "left_truth": row["left_truth"],
                    "right_truth": row["right_truth"],
                }
            )
    result: dict[str, Any] = {
        "obstruction_id": stable_identifier(
            "formal-obstruction",
            lens,
            compilation["compilation_digest"],
            canonical_digest(counterexamples),
        ),
        "lens": lens,
        "obstruction_kind": (
            "noncommuting_composition" if lens == "categorical" else "missing_transport_coherence"
        ),
        "task_relation_ids": copy.deepcopy(compilation["selected_relation_ids"]),
        "baseline_artifact_digest": replay["baseline_artifact_digest"],
        "baseline_model_digest": canonical_digest(model),
        "baseline_witness_digest": canonical_digest(witness),
        "validator_receipt_id": witness["certificate"]["validator_receipt"]["receipt_id"],
        "replay_result": replay["result"],
        "counterexamples": counterexamples,
    }
    return _seal(result, "witness_digest")


def _role_binding_ids(compilation: Mapping[str, Any], role: str) -> list[str]:
    rows = [
        *compilation["primitive_bindings"],
        *compilation["invariant_bindings"],
        *compilation["target_bindings"],
    ]
    result = [row["binding_id"] for row in rows if row["canonical_formal_role"] == role]
    if not result:
        raise FormalLensProductionError(f"meaning compiler produced no {role} bindings")
    return result


def _action(rows: Sequence[Mapping[str, Any]], source: str, target: str) -> list[dict[str, str]]:
    return [
        {source: row[source], target: row[target]}
        for row in sorted(rows, key=lambda item: str(item[source]))
    ]


def _category_completion(
    compilation: Mapping[str, Any],
    model: Mapping[str, Any],
    witness: Mapping[str, Any],
    obstruction: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct and verify the finite coequalizer of the obstructed composites."""

    objects_by_id = {row["object_id"]: row for row in model["objects"]}
    morphisms = {row["morphism_id"]: row for row in model["morphisms"]}
    compositions = {row["composition_id"]: row for row in model["compositions"]}
    left_row = compositions[witness["left_composite_id"]]
    right_row = compositions[witness["right_composite_id"]]
    left_morphism = morphisms[left_row["result_morphism_id"]]
    right_morphism = morphisms[right_row["result_morphism_id"]]
    left_action = _action(left_morphism["action"], "source_element_id", "target_element_id")
    right_action = _action(right_morphism["action"], "source_element_id", "target_element_id")
    if [row["source_element_id"] for row in left_action] != [
        row["source_element_id"] for row in right_action
    ]:
        raise FormalLensProductionError("categorical witness composites have different source carriers")

    target_id = witness["target_id"]
    target_members = list(objects_by_id[target_id]["element_ids"])
    parent = {member: member for member in target_members}

    def find(member: str) -> str:
        while parent[member] != member:
            parent[member] = parent[parent[member]]
            member = parent[member]
        return member

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            keep, merge = sorted((left_root, right_root))
            parent[merge] = keep

    for row in obstruction["counterexamples"]:
        union(row["left_output_id"], row["right_output_id"])
    classes_by_root: dict[str, list[str]] = {}
    for member in target_members:
        classes_by_root.setdefault(find(member), []).append(member)
    class_rows: list[dict[str, Any]] = []
    member_to_class: dict[str, str] = {}
    for members in sorted((sorted(values) for values in classes_by_root.values())):
        class_id = stable_identifier(
            "coequalizer-class", compilation["compilation_digest"], members
        )
        class_rows.append({"class_id": class_id, "target_member_ids": members})
        member_to_class.update({member: class_id for member in members})

    quotient_id = stable_identifier(
        "category-coequalizer", compilation["compilation_digest"], class_rows
    )
    quotient_morphism_id = stable_identifier(
        "category-quotient-morphism", compilation["compilation_digest"], quotient_id
    )
    factored_id = stable_identifier(
        "category-factored-composite", compilation["compilation_digest"], quotient_id
    )
    quotient_action = [
        {"source_id": member, "target_id": member_to_class[member]}
        for member in sorted(target_members)
    ]

    def postcompose(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
        return [
            {"source_id": row["source_element_id"], "target_id": member_to_class[row["target_element_id"]]}
            for row in rows
        ]

    left_post = postcompose(left_action)
    right_post = postcompose(right_action)
    if left_post != right_post:
        raise FormalLensProductionError("constructed categorical quotient does not equalize both composites")

    relation_id = compilation["selected_relation_ids"][0]
    formal_roles = {
        row["role"]: row for row in compilation["formal_projection"]["carriers"]
    }
    category_objects = [
        {
            "object_id": formal_roles[role]["formal_id"],
            "role": role,
            "semantic_binding_ids": _role_binding_ids(compilation, role),
            "carrier_member_ids": copy.deepcopy(formal_roles[role]["member_ids"]),
        }
        for role in ("source", "mediator", "target")
    ]
    category_objects.append(
        {
            "object_id": quotient_id,
            "role": "coequalizer",
            "semantic_binding_ids": copy.deepcopy(compilation["selected_relation_ids"]),
            "carrier_member_ids": [row["class_id"] for row in class_rows],
        }
    )
    source_id = witness["source_id"]
    projected_morphisms = [
        {
            "morphism_id": left_morphism["morphism_id"],
            "domain_object_id": source_id,
            "codomain_object_id": target_id,
            "morphism_kind": "task_route",
            "relation_id": relation_id,
            "action": [
                {"source_id": row["source_element_id"], "target_id": row["target_element_id"]}
                for row in left_action
            ],
        },
        {
            "morphism_id": right_morphism["morphism_id"],
            "domain_object_id": source_id,
            "codomain_object_id": target_id,
            "morphism_kind": "task_route",
            "relation_id": relation_id,
            "action": [
                {"source_id": row["source_element_id"], "target_id": row["target_element_id"]}
                for row in right_action
            ],
        },
        {
            "morphism_id": quotient_morphism_id,
            "domain_object_id": target_id,
            "codomain_object_id": quotient_id,
            "morphism_kind": "quotient",
            "relation_id": relation_id,
            "action": quotient_action,
        },
        {
            "morphism_id": factored_id,
            "domain_object_id": source_id,
            "codomain_object_id": quotient_id,
            "morphism_kind": "factored",
            "relation_id": relation_id,
            "action": left_post,
        },
    ]
    composition_rows = [
        {
            "composition_id": stable_identifier(
                "category-completion-composition", side, compilation["compilation_digest"]
            ),
            "path_morphism_ids": [route["morphism_id"], quotient_morphism_id],
            "result_action_digest": canonical_digest(post),
            "associative_on_declared_carrier": True,
        }
        for side, route, post in (
            ("left", projected_morphisms[0], left_post),
            ("right", projected_morphisms[1], right_post),
        )
    ]

    # Exhaust the maps C -> {0,1}.  Compatibility means each generated
    # coequalizer class has one value; then its factor through Q is forced.
    compatible_maps = 0
    unique_factorizations = 0
    for values in itertools.product((0, 1), repeat=len(target_members)):
        candidate = dict(zip(target_members, values, strict=True))
        compatible = all(
            len({candidate[member] for member in row["target_member_ids"]}) == 1
            for row in class_rows
        )
        if compatible:
            compatible_maps += 1
            factor = {
                row["class_id"]: candidate[row["target_member_ids"][0]]
                for row in class_rows
            }
            if all(factor[member_to_class[member]] == candidate[member] for member in target_members):
                unique_factorizations += 1
    if compatible_maps == 0 or unique_factorizations != compatible_maps:
        raise FormalLensProductionError("finite categorical factorization is absent or nonunique")

    model_core: dict[str, Any] = {
        "construction_kind": "finite_coequalizer_commuting_completion",
        "objects": category_objects,
        "morphisms": projected_morphisms,
        "composition": composition_rows,
        "coequalizer_classes": class_rows,
        "commuting_completion": {
            "left_postcomposition": left_post,
            "right_postcomposition": right_post,
            "pointwise_equal": True,
        },
        "naturality_checks": [
            {
                "relation_id": selected_relation_id,
                "left_action_digest": canonical_digest(left_post),
                "right_action_digest": canonical_digest(right_post),
                "commutes": True,
            }
            for selected_relation_id in compilation["selected_relation_ids"]
        ],
        "universal_property": {
            "property_kind": "finite_coequalizer_factorization",
            "finite_candidate_maps_checked": 2 ** len(target_members),
            "factorizations_found": compatible_maps,
            "unique_factorization_for_every_compatible_map": True,
        },
        "protected_structure": {
            "invariants": copy.deepcopy(compilation["task_contract"]["invariants"]),
            "preservation_status": "retained_as_open_translation_obligations",
            "physics_transfer_authorized": False,
        },
        "construction_valid": True,
    }
    return _seal(model_core, "model_digest")


def _hott_completion(
    compilation: Mapping[str, Any],
    model: Mapping[str, Any],
    witness: Mapping[str, Any],
    obstruction: Mapping[str, Any],
) -> dict[str, Any]:
    """Adjoin exact finite pointwise paths and one bounded coherence cell."""

    if any(row["left_truth"] is not row["right_truth"] for row in obstruction["counterexamples"]):
        raise FormalLensProductionError(
            "HoTT coherence cannot be constructed across unequal protected predicate fibers"
        )
    bindings_by_role = {
        role: _role_binding_ids(compilation, role) for role in ("source", "mediator", "target")
    }
    roles_by_type = {
        row["formal_id"]: row["role"] for row in compilation["formal_projection"]["carriers"]
    }
    projected_types = [
        {
            "type_id": row["type_id"],
            "semantic_binding_ids": bindings_by_role[roles_by_type[row["type_id"]]],
            "term_ids": copy.deepcopy(row["term_ids"]),
            "universe_level": row["universe_level"],
            "truncation_level": row["truncation_level"],
        }
        for row in model["types"]
    ]
    relation_id = compilation["selected_relation_ids"][0]
    projected_maps = [
        {
            "map_id": row["map_id"],
            "source_type_id": row["domain_type_id"],
            "target_type_id": row["codomain_type_id"],
            "relation_id": relation_id,
            "term_action": [
                {"source_id": item["source_term_id"], "target_id": item["target_term_id"]}
                for item in row["term_action"]
            ],
        }
        for row in model["maps"]
    ]
    projected_equivalences = [
        {
            "equivalence_id": row["equivalence_id"],
            "forward_map_id": row["forward_map_id"],
            "inverse_map_id": row["inverse_map_id"],
            "inverse_homotopies_valid": True,
            "treated_as_identity": False,
        }
        for row in model["equivalences"]
    ]
    transports = {row["transport_id"]: row for row in model["transports"]}
    projected_compositions = []
    for row in model["transport_compositions"]:
        action = transports[row["result_transport_id"]]["fiber_action"]
        projected_compositions.append(
            {
                "composition_id": row["composition_id"],
                "transport_ids": copy.deepcopy(row["path_transport_ids"]),
                "pointwise_action_digest": canonical_digest(action),
            }
        )
    paths = [
        {
            "path_id": stable_identifier(
                "hott-coherence-path",
                compilation["compilation_digest"],
                row["input_id"],
                row["left_output_id"],
                row["right_output_id"],
            ),
            "level": 1,
            "ambient_type_id": witness["target_id"],
            "source_term_id": row["left_output_id"],
            "target_term_id": row["right_output_id"],
            "constructor": "freely_adjoined_pointwise_coherence_path",
            "predicate_truth_preserved": True,
        }
        for row in obstruction["counterexamples"]
    ]
    if len({row["path_id"] for row in paths}) != len(paths):
        raise FormalLensProductionError("HoTT completion produced duplicate pointwise paths")
    cell = {
        "cell_id": stable_identifier(
            "hott-coherence-cell", compilation["compilation_digest"], paths
        ),
        "level": 2,
        "source_composition_id": witness["left_composite_id"],
        "target_composition_id": witness["right_composite_id"],
        "pointwise_path_ids": [row["path_id"] for row in paths],
        "all_boundaries_inhabited": True,
        "coherent": True,
    }
    model_core: dict[str, Any] = {
        "construction_kind": "finite_pointwise_transport_coherence_completion",
        "types": projected_types,
        "maps": projected_maps,
        "equivalences": projected_equivalences,
        "transport_compositions": projected_compositions,
        "adjoined_paths": paths,
        "coherence_cell": cell,
        "equality_boundaries": {
            "judgmental_equality_claimed": False,
            "identity_paths_constructed": True,
            "equivalences_validated_as_finite_bijections": True,
            "equivalence_collapsed_to_identity": False,
            "transport_scope": "declared_finite_predicate_fibers_only",
            "truncation_scope": "retain_through_constructed_level_2_cell_no_higher_claim",
            "univalence_assumed": False,
            "universe_scope": "one_declared_finite_local_universe_only",
            "higher_coherence_scope": "exact_constructed_cell_only",
        },
        "protected_structure": {
            "invariants": copy.deepcopy(compilation["task_contract"]["invariants"]),
            "preservation_status": "retained_as_open_translation_obligations",
            "physics_transfer_authorized": False,
        },
        "construction_valid": True,
    }
    return _seal(model_core, "model_digest")


def _formal_component(request: Mapping[str, Any], lens: str) -> dict[str, Any]:
    compilation, model, witness, replay = _baseline_formal_artifact(request, lens)
    obstruction = _obstruction(lens, compilation, model, witness, replay)
    mode = request["lens_policy"]["construction_modes"][lens]
    if mode == "constructive_finite_completion":
        intervention = (
            _category_completion(compilation, model, witness, obstruction)
            if lens == "categorical"
            else _hott_completion(compilation, model, witness, obstruction)
        )
        status = "constructively_removed"
        derivation_kind = (
            "validated_categorical_completion"
            if lens == "categorical"
            else "validated_hott_coherence_completion"
        )
        evidence_digest = intervention["model_digest"]
    else:
        intervention = None
        status = "hypothetical_assumption_away_sensitivity"
        derivation_kind = "hypothetical_assumption_away_not_actual"
        evidence_digest = obstruction["witness_digest"]
    component: dict[str, Any] = {
        "lens": lens,
        "semantic_compilation": compilation,
        "obstruction": obstruction,
        "construction_mode": mode,
        "intervened_model": intervention,
        "construction_status": status,
        "predicate_derivations": [
            {
                "predicate_id": predicate_id,
                "value": True,
                "derivation_kind": derivation_kind,
                "evidence_digest": evidence_digest,
            }
            for predicate_id in request["domain_decision_rule"]["obstruction_bindings"][lens]
        ],
    }
    return _seal(component, "component_digest")


def _is_applicable(request: Mapping[str, Any], lens: str) -> bool:
    compilation = compile_task_relation(request["task_case"], lens)
    return compilation["lens_selection"]["status"] == "applicable"


def _predicate_rows(
    request: Mapping[str, Any],
    values: Mapping[str, bool],
    derivation_kinds: Mapping[str, str],
    evidence: Mapping[str, str],
) -> list[dict[str, Any]]:
    return [
        {
            "predicate_id": row["predicate_id"],
            "value": values[row["predicate_id"]],
            "derivation_kind": derivation_kinds[row["predicate_id"]],
            "evidence_digest": evidence[row["predicate_id"]],
        }
        for row in request["domain_decision_rule"]["predicates"]
    ]


def _rule_replay(
    request: Mapping[str, Any],
    route_id: str,
    applied_components: Sequence[Mapping[str, Any]],
    hypothetical_components: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rule = request["domain_decision_rule"]
    baseline = {row["predicate_id"]: row["baseline_value"] for row in rule["predicates"]}
    actual = dict(baseline)
    hypothetical = dict(baseline) if hypothetical_components else None
    base_kind = {
        predicate_id: (
            "unchanged_capable_nonformal_control"
            if route_id == "capable_nonformal"
            else "declared_baseline"
        )
        for predicate_id in baseline
    }
    base_evidence = {
        row["predicate_id"]: canonical_digest(row) for row in rule["predicates"]
    }
    actual_kind = dict(base_kind)
    actual_evidence = dict(base_evidence)
    for component in applied_components:
        lens = component["lens"]
        derivation_kind = (
            "validated_categorical_completion"
            if lens == "categorical"
            else "validated_hott_coherence_completion"
        )
        for predicate_id in rule["obstruction_bindings"][lens]:
            actual[predicate_id] = True
            actual_kind[predicate_id] = derivation_kind
            actual_evidence[predicate_id] = component["component_digest"]
    hypothetical_kind = dict(base_kind)
    hypothetical_evidence = dict(base_evidence)
    if hypothetical is not None:
        for component in hypothetical_components:
            for predicate_id in rule["obstruction_bindings"][component["lens"]]:
                hypothetical[predicate_id] = True
                hypothetical_kind[predicate_id] = "hypothetical_assumption_away_not_actual"
                hypothetical_evidence[predicate_id] = component["obstruction"]["witness_digest"]

    baseline_decision = _evaluate_rule(rule, baseline)
    actual_decision = _evaluate_rule(rule, actual)
    hypothetical_decision = _evaluate_rule(rule, hypothetical) if hypothetical is not None else None
    actual_changed = actual_decision != baseline_decision
    hypothetical_changed = bool(
        hypothetical_decision is not None and hypothetical_decision != baseline_decision
    )
    replay_status = (
        "hypothetical_assumption_away_sensitivity"
        if hypothetical is not None
        else "constructive_decision_change"
        if actual_changed
        else "quarantined_no_decision_change"
    )
    replay: dict[str, Any] = {
        "precommit_digest": request["domain_decision_rule_precommit"]["precommit_digest"],
        "rule_digest": rule["rule_digest"],
        "baseline_predicates": _predicate_rows(
            request,
            baseline,
            {predicate_id: "declared_baseline" for predicate_id in baseline},
            base_evidence,
        ),
        "intervened_predicates": _predicate_rows(
            request, actual, actual_kind, actual_evidence
        ),
        "hypothetical_predicates": (
            _predicate_rows(request, hypothetical, hypothetical_kind, hypothetical_evidence)
            if hypothetical is not None
            else None
        ),
        "baseline_decision": baseline_decision,
        "intervened_decision": actual_decision,
        "hypothetical_decision": hypothetical_decision,
        "actual_decision_changed": actual_changed,
        "hypothetical_decision_changed": hypothetical_changed,
        "replay_status": replay_status,
    }
    return _seal(replay, "replay_digest")


def _nonformal_analysis(request: Mapping[str, Any]) -> dict[str, Any]:
    semantics = request["task_case"]["task_semantics"]
    analysis: dict[str, Any] = {
        "pressure": semantics["pressure"],
        "direct_burden": (
            "Retain the incumbent primitives, compare the declared relation-specific correction, "
            "and do not mutate formal obstruction predicates without a construction."
        ),
        "correction": semantics["correction"],
        "falsifier": semantics["falsifier"],
        "formal_predicates_mutated": False,
    }
    return _seal(analysis, "analysis_digest")


def _changed_burden(
    components: Sequence[Mapping[str, Any]], nonformal: Mapping[str, Any] | None
) -> str:
    rows = [
        consequence["changed_burden"]
        for component in components
        for consequence in component["semantic_compilation"]["lens_consequences"]
    ]
    if rows:
        return " ".join(rows)
    if nonformal is not None:
        return str(nonformal["direct_burden"])
    return "No lens-native relation was available; preserve the incumbent burden under quarantine."


def _route_result(
    request: Mapping[str, Any],
    route_id: str,
    components: Sequence[Mapping[str, Any]],
    nonformal: Mapping[str, Any] | None,
) -> dict[str, Any]:
    assumption_components = [
        row
        for row in components
        if row["construction_status"] == "hypothetical_assumption_away_sensitivity"
    ]
    constructive_components = [
        row for row in components if row["construction_status"] == "constructively_removed"
    ]
    if route_id == "combined" and len(constructive_components) != 2:
        applied: list[Mapping[str, Any]] = []
        hypothetical = list(components)
    else:
        applied = constructive_components
        hypothetical = assumption_components
    replay = _rule_replay(request, route_id, applied, hypothetical)

    if route_id in {"categorical", "hott"} and replay["actual_decision_changed"]:
        declared = _decision(request["task_case"]["task_semantics"]["lens_decisions"][route_id])
        if replay["intervened_decision"] != declared:
            raise FormalLensProductionError(
                f"{route_id} constructive decision differs from its task-relation declaration"
            )
    semantics = request["task_case"]["task_semantics"]
    carrier = semantics["physical_carrier"]
    physics_facing = bool(
        isinstance(carrier, str)
        and carrier
        and not carrier.startswith("not_applicable_non_physics:")
    )
    constructive_change = bool(
        replay["actual_decision_changed"]
        and applied
        and not hypothetical
        and physics_facing
    )
    if hypothetical:
        handback_status = "hypothetical_assumption_away_sensitivity"
    elif constructive_change:
        handback_status = "internal_constructive_decision_probe"
    else:
        handback_status = "quarantined_no_decision_change"
    handback: dict[str, Any] = {
        "handback_status": handback_status,
        "changed_burden": _changed_burden(components, nonformal),
        "correction": semantics["correction"],
        "falsifier": semantics["falsifier"],
        "physical_carrier": carrier,
        "regime": semantics["regime"],
        "quantifiers": copy.deepcopy(semantics["quantifiers"]),
        "untouched_physics_gates": copy.deepcopy(semantics["untouched_physics_gates"]),
        "baseline_decision": replay["baseline_decision"],
        "intervened_decision": replay["intervened_decision"],
        "experiment_role": "secondary_theory_requested_falsifier_only",
        "authority_nulls": list(_AUTHORITY_NULLS),
        "physics_value_authorized": False,
        "investment_authorized": False,
    }
    _seal(handback, "handback_digest")
    result: dict[str, Any] = {
        "route_id": route_id,
        "route_kind": _ROUTE_KINDS[route_id],
        "formal_components": copy.deepcopy(list(components)),
        "nonformal_analysis": copy.deepcopy(nonformal),
        "rule_replay": replay,
        "disposition": (
            "internal_constructive_candidate"
            if constructive_change
            else "quarantined_non_investment"
        ),
        "physics_handback": handback,
    }
    return _seal(result, "result_digest")


def produce_categorical_route(
    request: Mapping[str, Any], execution_context: _RouteExecutionContext
) -> dict[str, Any]:
    """Produce the categorical route only when a native relation selects it."""

    execution_context.await_start("categorical")
    components = [_formal_component(request, "categorical")] if _is_applicable(request, "categorical") else []
    return _route_result(request, "categorical", components, None)


def produce_hott_route(
    request: Mapping[str, Any], execution_context: _RouteExecutionContext
) -> dict[str, Any]:
    """Produce the HoTT route with explicit identity/equivalence boundaries."""

    execution_context.await_start("hott")
    components = [_formal_component(request, "hott")] if _is_applicable(request, "hott") else []
    return _route_result(request, "hott", components, None)


def produce_combined_route(
    request: Mapping[str, Any], execution_context: _RouteExecutionContext
) -> dict[str, Any]:
    """Require both native formal lenses before applying either intervention."""

    execution_context.await_start("combined")
    applicable = all(_is_applicable(request, lens) for lens in ("categorical", "hott"))
    components = (
        [_formal_component(request, lens) for lens in ("categorical", "hott")]
        if applicable
        else []
    )
    return _route_result(request, "combined", components, None)


def produce_capable_nonformal_route(
    request: Mapping[str, Any], execution_context: _RouteExecutionContext
) -> dict[str, Any]:
    """Run the matched direct-reasoning control without mutating formal facts."""

    execution_context.await_start("capable_nonformal")
    nonformal = _nonformal_analysis(request)
    return _route_result(request, "capable_nonformal", [], nonformal)


def _terminal_receipt(
    binding: FormalLensProducerBinding,
    request: Mapping[str, Any],
    registry_binding: Mapping[str, Any],
    execution_context: _RouteExecutionContext,
) -> dict[str, Any]:
    try:
        result = binding.function(copy.deepcopy(dict(request)), execution_context)
        failure = None
        terminal_status = (
            "completed"
            if result["disposition"] == "internal_constructive_candidate"
            else "quarantined"
        )
    except Exception as exc:  # terminal receipts preserve sibling success
        message = str(exc).strip() or type(exc).__name__
        message = message[:2000]
        result = None
        terminal_status = "failed"
        failure = {
            "error_type": type(exc).__name__,
            "message": message,
            "message_digest": canonical_digest(message),
        }
    receipt: dict[str, Any] = {
        "receipt_id": stable_identifier(
            "formal-route-receipt",
            request["formal_request_id"],
            binding.route_id,
            binding.producer_id,
            request["request_digest"],
        ),
        "route_id": binding.route_id,
        "producer_id": binding.producer_id,
        "request_digest": request["request_digest"],
        "frozen_ancestor_digest": request["frozen_task_semantic_ancestor"]["ancestor_digest"],
        "registry_binding_digest": registry_binding["binding_digest"],
        "execution_backend": "shared_process_thread_pool",
        "terminal_status": terminal_status,
        "result": result,
        "failure": failure,
        "isolation_assurance": copy.deepcopy(_ISOLATION_ASSURANCE),
        "authority_boundary": "concurrent_local_protocol_execution_only",
    }
    return _seal(receipt, "receipt_digest")


def _barrier(receipts: Sequence[Mapping[str, Any]], request_digest: str) -> dict[str, Any]:
    failed = [row["route_id"] for row in receipts if row["terminal_status"] == "failed"]
    barrier: dict[str, Any] = {
        "barrier_id": stable_identifier(
            "formal-route-terminal-barrier",
            request_digest,
            [row["receipt_digest"] for row in receipts],
        ),
        "expected_routes": list(ROUTE_ORDER),
        "terminal_receipt_ids": [row["receipt_id"] for row in receipts],
        "terminal_receipt_digests": [row["receipt_digest"] for row in receipts],
        "all_routes_terminal": True,
        "failed_routes": failed,
    }
    return _seal(barrier, "barrier_digest")


def _canonical_file_descriptor(role: str, relative_path: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    data = canonical_json(payload) + b"\n"
    return {
        "role": role,
        "relative_path": relative_path,
        "sha256": bytes_digest(data),
        "byte_length": len(data),
    }


def _artifact_manifest(
    request: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
    barrier: Mapping[str, Any],
) -> dict[str, Any]:
    files = [_canonical_file_descriptor("request", "request.json", request)]
    files.extend(
        _canonical_file_descriptor(
            "route_receipt", f"receipts/{row['route_id']}.json", row
        )
        for row in receipts
    )
    files.append(_canonical_file_descriptor("terminal_barrier", "terminal-barrier.json", barrier))
    return {
        "bundle_relative_root": request["formal_request_id"],
        "files": files,
        "atomic_last_packet_path": "formal-lens-production-packet.json",
    }


def _production_status(receipts: Sequence[Mapping[str, Any]]) -> str:
    if any(row["terminal_status"] == "failed" for row in receipts):
        return "partial_failure"
    if any(row["terminal_status"] == "quarantined" for row in receipts):
        return "complete_with_quarantine"
    return "complete_internal_protocol"


def _build_packet(
    request: Mapping[str, Any],
    registry_binding: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    barrier = _barrier(receipts, request["request_digest"])
    packet: dict[str, Any] = {
        "schema_version": "1.0.0",
        "packet_id": stable_identifier(
            "formal-lens-production-packet",
            request["formal_request_id"],
            request["request_digest"],
            [row["receipt_digest"] for row in receipts],
        ),
        "formal_request_id": request["formal_request_id"],
        "request_digest": request["request_digest"],
        "frozen_ancestor_digest": request["frozen_task_semantic_ancestor"]["ancestor_digest"],
        "registry_binding": copy.deepcopy(dict(registry_binding)),
        "execution_contract": copy.deepcopy(_EXECUTION_CONTRACT),
        "route_receipts": copy.deepcopy(list(receipts)),
        "terminal_barrier": barrier,
        "production_status": _production_status(receipts),
        "artifact_manifest": _artifact_manifest(request, receipts, barrier),
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    return _seal(packet, "packet_digest")


def _replay_receipts(
    bindings: Sequence[FormalLensProducerBinding],
    request: Mapping[str, Any],
    registry_binding: Mapping[str, Any],
) -> list[dict[str, Any]]:
    context = _RouteExecutionContext(None)
    return [
        _terminal_receipt(binding, request, registry_binding, context)
        for binding in bindings
    ]


def validate_formal_lens_production_packet(
    request_raw: Mapping[str, Any],
    packet_raw: Mapping[str, Any],
    *,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    """Re-execute all registered routes and reject digest-only rebinding."""

    request = validate_formal_lens_production_request(request_raw)
    packet = copy.deepcopy(dict(packet_raw))
    validate_payload(packet, PACKET_SCHEMA)
    _assert_self_digest(packet, "packet_digest", "formal-lens production packet")
    bindings, registry_binding = load_formal_lens_producer_registry(registry_path)
    if packet["registry_binding"] != registry_binding:
        raise FormalLensProductionError("formal-lens packet registry binding is stale")
    if (
        packet["formal_request_id"] != request["formal_request_id"]
        or packet["request_digest"] != request["request_digest"]
        or packet["frozen_ancestor_digest"]
        != request["frozen_task_semantic_ancestor"]["ancestor_digest"]
    ):
        raise FormalLensProductionError("formal-lens packet binds a different request or ancestor")
    receipts = packet["route_receipts"]
    if [row["route_id"] for row in receipts] != list(ROUTE_ORDER):
        raise FormalLensProductionError("formal-lens terminal receipts are not a route bijection")
    expected_receipts = _replay_receipts(bindings, request, registry_binding)
    if receipts != expected_receipts:
        raise FormalLensProductionError("formal-lens route receipt differs from executable replay")
    expected_packet = _build_packet(request, registry_binding, expected_receipts)
    if packet != expected_packet:
        raise FormalLensProductionError("formal-lens packet/barrier/manifest differs from replay")
    return packet


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise FormalLensProductionError(f"formal-lens bundle path is not a regular directory: {path}")


def _write_exact(path: Path, payload: Mapping[str, Any]) -> None:
    """Create canonical bytes once; exact retry reuses them, drift fails."""

    _ensure_directory(path.parent)
    data = canonical_json(payload) + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags, 0o600)
    except FileExistsError:
        if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
            raise FormalLensProductionError(f"immutable formal-lens artifact conflicts: {path}")
        return
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _load_object(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise FormalLensProductionError(f"formal-lens artifact is unavailable: {path}")
    raw = load_json(path)
    if not isinstance(raw, dict) or path.read_bytes() != canonical_json(raw) + b"\n":
        raise FormalLensProductionError(f"formal-lens artifact is not canonical JSON: {path}")
    return raw


def run_formal_lens_production(
    request_raw: Mapping[str, Any],
    output_root: Path,
    *,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    """Run four concurrent routes and persist terminal evidence atomically last."""

    request = validate_formal_lens_production_request(request_raw)
    output_root = Path(output_root)
    _ensure_directory(output_root)
    bundle = output_root / request["formal_request_id"]
    _ensure_directory(bundle)
    packet_path = bundle / "formal-lens-production-packet.json"
    if packet_path.exists():
        existing = validate_formal_lens_production_bundle(bundle, registry_path=registry_path)
        if existing["request_digest"] != request["request_digest"]:
            raise FormalLensProductionError("completed formal-lens bundle has a different request")
        return existing

    _write_exact(bundle / "request.json", request)
    bindings, registry_binding = load_formal_lens_producer_registry(registry_path)
    context = _RouteExecutionContext(threading.Barrier(len(bindings)))
    receipts_by_route: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=len(bindings), thread_name_prefix="formal-lens") as executor:
        futures: dict[Future[dict[str, Any]], str] = {
            executor.submit(
                _terminal_receipt,
                binding,
                request,
                registry_binding,
                context,
            ): binding.route_id
            for binding in bindings
        }
        for future in as_completed(futures):
            route_id = futures[future]
            receipts_by_route[route_id] = future.result()
    context.assert_parallel_wave()
    receipts = [receipts_by_route[route_id] for route_id in ROUTE_ORDER]
    for receipt in receipts:
        _write_exact(bundle / "receipts" / f"{receipt['route_id']}.json", receipt)
    terminal_barrier = _barrier(receipts, request["request_digest"])
    _write_exact(bundle / "terminal-barrier.json", terminal_barrier)
    packet = _build_packet(request, registry_binding, receipts)
    validate_formal_lens_production_packet(
        request, packet, registry_path=registry_path
    )
    _write_exact(packet_path, packet)
    return validate_formal_lens_production_bundle(bundle, registry_path=registry_path)


def validate_formal_lens_production_bundle(
    bundle_root: Path,
    *,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    """Reopen every exact file, validate the barrier, and require packet-last."""

    bundle = Path(bundle_root)
    if bundle.is_symlink() or not bundle.is_dir():
        raise FormalLensProductionError("formal-lens bundle root must be a regular directory")
    request = _load_object(bundle / "request.json")
    packet = _load_object(bundle / "formal-lens-production-packet.json")
    validated = validate_formal_lens_production_packet(
        request, packet, registry_path=registry_path
    )
    expected_payloads: dict[str, Mapping[str, Any]] = {"request.json": request}
    expected_payloads.update(
        {
            f"receipts/{row['route_id']}.json": row
            for row in packet["route_receipts"]
        }
    )
    expected_payloads["terminal-barrier.json"] = packet["terminal_barrier"]
    descriptor_paths = [row["relative_path"] for row in packet["artifact_manifest"]["files"]]
    if descriptor_paths != list(expected_payloads):
        raise FormalLensProductionError("formal-lens artifact manifest order or membership drift")
    for descriptor in packet["artifact_manifest"]["files"]:
        relative = descriptor["relative_path"]
        path = bundle.joinpath(*Path(relative).parts)
        payload = expected_payloads[relative]
        data = canonical_json(payload) + b"\n"
        if (
            path.is_symlink()
            or not path.is_file()
            or path.read_bytes() != data
            or descriptor["sha256"] != bytes_digest(data)
            or descriptor["byte_length"] != len(data)
        ):
            raise FormalLensProductionError(f"formal-lens artifact descriptor drift: {relative}")
    expected_files = {
        *expected_payloads,
        "formal-lens-production-packet.json",
    }
    actual_files = {
        path.relative_to(bundle).as_posix()
        for path in bundle.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual_files != expected_files or any(path.is_symlink() for path in bundle.rglob("*")):
        raise FormalLensProductionError("formal-lens bundle has extra, missing, or linked artifacts")
    return validated


__all__ = [
    "FormalLensProductionError",
    "produce_capable_nonformal_route",
    "produce_categorical_route",
    "produce_combined_route",
    "produce_hott_route",
    "run_formal_lens_production",
    "validate_formal_lens_production_bundle",
    "validate_formal_lens_production_packet",
    "validate_formal_lens_production_request",
]
