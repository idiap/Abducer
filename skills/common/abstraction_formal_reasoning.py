# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executable finite semantics for category/HoTT discovery packets.

The discovery skills intentionally use small finite models.  They are not
surrogates for the intended continuum mathematics; they make local claims such
as typing, composition, unit laws, associativity, inverse homotopies, predicate
transport, and a negative countermodel executable instead of self-attested.
Every accepted HoTT path points to one indexed finite fiber with the same type,
level, endpoints, and optional truth boundary.  Every negative witness is
replayed through a registry-bound local callable.  The finite HoTT model also
declares its path-inhabitance inventory complete over the listed terms and
truth boundaries; refutation queries close that inventory under reflexivity,
inversion, and concatenation before treating a pointwise boundary as empty.
"""

from __future__ import annotations

import copy
import inspect
from itertools import combinations
from typing import Any, Callable, Mapping, Sequence

from agentic.discovery.contracts import canonical_digest, stable_identifier
from skills.common.formal_dependency_authority import (
    _FormalDependencyRunContext,
    _build_formal_dependency_run_context,
    _validate_formal_dependency_run_context,
)
from skills.common.task_relation_compiler import (
    TaskRelationCompilerError,
    build_formal_delta_and_handback,
    build_task_relation_model_binding,
    compile_task_relation,
    validate_task_relation_model_binding,
)


class FormalReasoningError(ValueError):
    """Raised when a declared formal structure does not execute as claimed."""

    def __init__(self, message: str, *, reason_code: str = "formal_reasoning_invalid") -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _fail(message: str, *, reason_code: str = "formal_reasoning_invalid") -> None:
    raise FormalReasoningError(message, reason_code=reason_code)


HOTT_PATH_AMBIENT_TYPE_INVALID = "hott_path_ambient_type_invalid"
HOTT_PATH_INDEXED_BOUNDARY_INVALID = "hott_path_indexed_boundary_invalid"
HOTT_INVERSE_HOMOTOPY_BOUNDARY_INVALID = "hott_inverse_homotopy_boundary_invalid"
HOTT_INVERSE_BASE_BOUNDARY_INVALID = "hott_inverse_base_boundary_invalid"
HOTT_REFUTATION_PATH_INHABITED = "hott_refutation_path_inhabited"


FINITE_HOTT_PATH_SPACE_POLICY = {
    "semantics": "sealed_finite_indexed_path_inhabitance",
    "inventory_status": "complete_for_declared_terms_and_truth_boundaries",
    "closure_rules": ["reflexivity", "inversion", "concatenation"],
    "authority_boundary": (
        "Completeness is asserted only for this sealed finite calibration's "
        "declared terms and indexed truth boundaries; it is not a claim about "
        "the continuum target's identity types."
    ),
}


def _index(rows: Sequence[Mapping[str, Any]], key: str, label: str) -> dict[str, Mapping[str, Any]]:
    result = {str(row[key]): row for row in rows}
    if len(result) != len(rows):
        _fail(f"{label} identifiers must be unique")
    return result


def callable_digest(callable_: Callable[..., Any]) -> str:
    """Bind a local authority row to the exact callable source and module."""

    return canonical_digest(
        {
            "module": callable_.__module__,
            "qualname": callable_.__qualname__,
            "source": inspect.getsource(callable_),
        }
    )


def _bound_dependency_authority(
    context: _FormalDependencyRunContext | None,
) -> dict[str, Any]:
    """Reuse only an opaque, fully boundary-validated authority context.

    Public standalone calls still derive the exact closure.  The factorial
    runtime instead derives and validates that closure around the whole fan-out
    and passes an immutable context through this hot path.  Raw self-digested
    mappings are intentionally inadmissible: a digest proves consistency, not
    that the dependency closure was derived from the live repository.
    """

    if context is None:
        context = _build_formal_dependency_run_context()
    if not isinstance(context, _FormalDependencyRunContext):
        _fail("cached formal dependency authority requires a validated run context")
    return context.snapshot()


def _finite_action(
    row: Mapping[str, Any], source_ids: set[str], target_ids: set[str], *, label: str
) -> dict[str, str]:
    action_rows = list(row["action"])
    action = {str(item["source_element_id"]): str(item["target_element_id"]) for item in action_rows}
    if len(action) != len(action_rows) or set(action) != source_ids:
        _fail(f"{label} action must be a total single-valued map on its domain")
    if not set(action.values()).issubset(target_ids):
        _fail(f"{label} action leaves its declared codomain")
    return action


def _compose_finite(first: Mapping[str, str], second: Mapping[str, str]) -> dict[str, str]:
    try:
        return {source: second[middle] for source, middle in first.items()}
    except KeyError as exc:
        _fail(f"finite action composition is undefined at {exc.args[0]}")


def _finite_diagram(
    *,
    objects_rows: Sequence[Mapping[str, Any]],
    arrows_rows: Sequence[Mapping[str, Any]],
    compositions_rows: Sequence[Mapping[str, Any]],
    arrow_id_field: str,
    domain_field: str,
    codomain_field: str,
    label: str,
) -> dict[str, Any]:
    """Validate a finite concrete category, including closure and all laws."""

    objects = _index(objects_rows, "object_id", f"{label} object")
    all_elements: set[str] = set()
    elements: dict[str, set[str]] = {}
    for object_id, row in objects.items():
        values = [str(value) for value in row["element_ids"]]
        if len(values) != len(set(values)) or not values:
            _fail(f"{label} object {object_id} needs unique finite elements")
        if all_elements.intersection(values):
            _fail(f"{label} element identifiers must be globally unambiguous")
        elements[object_id] = set(values)
        all_elements.update(values)

    arrows = _index(arrows_rows, arrow_id_field, f"{label} arrow")
    actions: dict[str, dict[str, str]] = {}
    semantic_signatures: dict[tuple[str, str, tuple[tuple[str, str], ...]], str] = {}
    for arrow_id, row in arrows.items():
        domain = str(row[domain_field])
        codomain = str(row[codomain_field])
        if domain not in objects or codomain not in objects:
            _fail(f"{label} arrow {arrow_id} has a dangling endpoint")
        action = _finite_action(
            row, elements[domain], elements[codomain], label=f"{label} arrow {arrow_id}"
        )
        actions[arrow_id] = action
        signature = (domain, codomain, tuple(sorted(action.items())))
        if signature in semantic_signatures:
            _fail(
                f"{label} arrows {semantic_signatures[signature]} and {arrow_id} "
                "duplicate one extensional morphism"
            )
        semantic_signatures[signature] = arrow_id
        is_identity = bool(row["is_identity"])
        if is_identity and (domain != codomain or action != {value: value for value in elements[domain]}):
            _fail(f"{label} identity {arrow_id} is not the executable identity function")

    identities_by_object: dict[str, list[str]] = {object_id: [] for object_id in objects}
    for arrow_id, row in arrows.items():
        if row["is_identity"]:
            identities_by_object[str(row[domain_field])].append(arrow_id)
    if any(len(ids) != 1 for ids in identities_by_object.values()):
        _fail(f"{label} needs exactly one executable identity per object")

    expected_pairs = {
        (left_id, right_id)
        for left_id, left in arrows.items()
        for right_id, right in arrows.items()
        if left[codomain_field] == right[domain_field]
    }
    compositions = _index(compositions_rows, "composition_id", f"{label} composition")
    pair_rows: dict[tuple[str, str], Mapping[str, Any]] = {}
    pair_results: dict[tuple[str, str], str] = {}
    for composition_id, row in compositions.items():
        path = [str(value) for value in row["path_morphism_ids"]]
        if len(path) != 2 or any(value not in arrows for value in path):
            _fail(f"{label} composition {composition_id} must cite exactly two known arrows")
        pair = (path[0], path[1])
        if pair in pair_rows:
            _fail(f"{label} composition table duplicates {pair}")
        if pair not in expected_pairs:
            _fail(f"{label} composition {composition_id} is not composable")
        result_id = str(row["result_morphism_id"])
        if result_id not in arrows:
            _fail(f"{label} composition {composition_id} has no result arrow")
        left, right, result = arrows[pair[0]], arrows[pair[1]], arrows[result_id]
        if (
            result[domain_field] != left[domain_field]
            or result[codomain_field] != right[codomain_field]
            or actions[result_id] != _compose_finite(actions[pair[0]], actions[pair[1]])
        ):
            _fail(f"{label} composition {composition_id} does not execute to its result")
        if left["is_identity"] and result_id != pair[1]:
            _fail(f"{label} left unit law fails for {pair[1]}")
        if right["is_identity"] and result_id != pair[0]:
            _fail(f"{label} right unit law fails for {pair[0]}")
        pair_rows[pair] = row
        pair_results[pair] = result_id
    if set(pair_rows) != expected_pairs:
        missing = sorted(expected_pairs - set(pair_rows))
        extra = sorted(set(pair_rows) - expected_pairs)
        _fail(f"{label} composition table is not closed; missing={missing}, extra={extra}")

    for first_id, first in arrows.items():
        for second_id, second in arrows.items():
            if first[codomain_field] != second[domain_field]:
                continue
            for third_id, third in arrows.items():
                if second[codomain_field] != third[domain_field]:
                    continue
                left_result = pair_results[(pair_results[(first_id, second_id)], third_id)]
                right_result = pair_results[(first_id, pair_results[(second_id, third_id)])]
                if left_result != right_result:
                    _fail(
                        f"{label} associativity fails for {first_id}, {second_id}, {third_id}"
                    )
    return {
        "objects": objects,
        "arrows": arrows,
        "elements": elements,
        "actions": actions,
        "compositions": compositions,
        "pair_rows": pair_rows,
        "pair_results": pair_results,
        "identity_ids": {key: value[0] for key, value in identities_by_object.items()},
    }


def _finite_path_action(path_ids: Sequence[str], structure: Mapping[str, Any]) -> tuple[str, str, dict[str, str]]:
    arrows = structure["arrows"]
    actions = structure["actions"]
    if not path_ids or any(path_id not in arrows for path_id in path_ids):
        _fail("negative witness cites an unknown or empty finite path")
    path = [arrows[path_id] for path_id in path_ids]
    for left, right in zip(path, path[1:]):
        domain_field = "domain_id"
        codomain_field = "codomain_id"
        if left[codomain_field] != right[domain_field]:
            _fail("negative witness finite path is not composable")
    result = dict(actions[path_ids[0]])
    for path_id in path_ids[1:]:
        result = _compose_finite(result, actions[path_id])
    return str(path[0]["domain_id"]), str(path[-1]["codomain_id"]), result


def _category_countermodel(model: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    structure = _finite_diagram(
        objects_rows=model["objects"], arrows_rows=model["morphisms"],
        compositions_rows=model["compositions"], arrow_id_field="morphism_id",
        domain_field="domain_id", codomain_field="codomain_id", label="category",
    )
    left = _finite_path_action(witness["left_path_ids"], structure)
    right = _finite_path_action(witness["right_path_ids"], structure)
    if left[:2] != right[:2]:
        _fail("category countermodel paths do not share endpoints")
    counterexamples = [
        {
            "source_element_id": source,
            "left_output_element_id": left[2][source],
            "right_output_element_id": right[2][source],
        }
        for source in sorted(left[2])
        if left[2][source] != right[2][source]
    ]
    return {
        "result": "noncommuting" if counterexamples else "commuting",
        "source_object_id": left[0],
        "target_object_id": left[1],
        "left_action_digest": canonical_digest(left[2]),
        "right_action_digest": canonical_digest(right[2]),
        "counterexamples": counterexamples,
        "claim_authority": "finite_local_countermodel_only",
    }


def _physical_countermodel(model: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    adapted = {
        "objects": model["objects"],
        "morphisms": [
            {
                **copy.deepcopy(dict(row)),
                "morphism_id": row["step_id"],
            }
            for row in model["steps"]
        ],
        "compositions": model["compositions"],
    }
    return _category_countermodel(adapted, witness)


def _term_action(row: Mapping[str, Any], source: set[str], target: set[str], *, label: str) -> dict[str, str]:
    rows = list(row["term_action"])
    action = {str(item["source_term_id"]): str(item["target_term_id"]) for item in rows}
    if len(action) != len(rows) or set(action) != source or not set(action.values()).issubset(target):
        _fail(f"{label} must be a total typed term action")
    return action


def _fiber_action(row: Mapping[str, Any], source: set[str], target: set[str], *, label: str) -> dict[str, tuple[str, bool, bool]]:
    rows = list(row["fiber_action"])
    action = {
        str(item["source_term_id"]): (
            str(item["target_term_id"]), bool(item["source_truth"]), bool(item["target_truth"])
        )
        for item in rows
    }
    if len(action) != len(rows) or set(action) != source:
        _fail(f"{label} must cover each source fiber exactly once")
    if not {item[0] for item in action.values()}.issubset(target):
        _fail(f"{label} leaves its target type")
    return action


def _compose_fiber(
    first: Mapping[str, tuple[str, bool, bool]],
    second: Mapping[str, tuple[str, bool, bool]],
) -> dict[str, tuple[str, bool, bool]]:
    result: dict[str, tuple[str, bool, bool]] = {}
    for source, (middle, source_truth, middle_truth) in first.items():
        if middle not in second:
            _fail("transport composition is undefined on a transported term")
        target, next_source_truth, target_truth = second[middle]
        if middle_truth != next_source_truth:
            _fail("transport composition changes the predicate truth at its interface")
        result[source] = (target, source_truth, target_truth)
    return result


def _finite_path_inhabited(
    path_graphs: Mapping[
        tuple[int, str],
        Mapping[tuple[str, bool | None], set[tuple[str, bool | None]]],
    ],
    *,
    level: int,
    ambient_type_id: str,
    source_term_id: str,
    target_term_id: str,
    source_fiber_truth: bool | None,
    target_fiber_truth: bool | None,
) -> bool:
    """Decide one boundary in the sealed finite identity-groupoid closure."""

    source = (source_term_id, source_fiber_truth)
    target = (target_term_id, target_fiber_truth)
    if source == target:  # reflexivity is present even without a stored row
        return True
    adjacency = path_graphs.get((level, ambient_type_id), {})
    frontier = [source]
    visited = {source}
    while frontier:
        node = frontier.pop()
        for neighbour in adjacency.get(node, set()):
            if neighbour == target:
                return True
            if neighbour not in visited:
                visited.add(neighbour)
                frontier.append(neighbour)
    return False


def _hott_structure(model: Mapping[str, Any]) -> dict[str, Any]:
    policy = model.get("path_space_policy")
    expected_policy = FINITE_HOTT_PATH_SPACE_POLICY
    # The policy is part of the sealed model identity, not an unordered feature
    # declaration.  Exact equality rejects both duplicated and permuted closure
    # rules, so equivalent finite models have one canonical serialization.
    if not isinstance(policy, Mapping) or dict(policy) != expected_policy:
        _fail("finite HoTT path-space policy is not the exact sealed inhabitance contract")
    types = _index(model["types"], "type_id", "HoTT type")
    terms: dict[str, set[str]] = {}
    all_terms: set[str] = set()
    for type_id, row in types.items():
        values = [str(value) for value in row["term_ids"]]
        if not values or len(values) != len(set(values)) or all_terms.intersection(values):
            _fail("HoTT term identifiers must be nonempty, unique, and globally typed")
        terms[type_id] = set(values)
        all_terms.update(values)
    maps = _index(model["maps"], "map_id", "HoTT map")
    map_actions: dict[str, dict[str, str]] = {}
    for map_id, row in maps.items():
        source, target = str(row["domain_type_id"]), str(row["codomain_type_id"])
        if source not in types or target not in types:
            _fail(f"HoTT map {map_id} has a dangling endpoint")
        map_actions[map_id] = _term_action(row, terms[source], terms[target], label=f"HoTT map {map_id}")

    path_fibers = _index(model["path_fibers"], "fiber_id", "HoTT path fiber")
    paths = _index(model["paths"], "path_id", "HoTT path")
    if any(type(row["level"]) is not int or row["level"] != 1 for row in path_fibers.values()):
        _fail("finite HoTT path fibers with term endpoints must have level 1")
    referenced_fibers: set[str] = set()
    for path_id, row in paths.items():
        if type(row["level"]) is not int or row["level"] != 1:
            _fail(f"finite HoTT path {path_id} has term endpoints but is not level 1")
        ambient = str(row["ambient_type_id"])
        if ambient not in types or row["source_term_id"] not in terms[ambient] or row["target_term_id"] not in terms[ambient]:
            _fail(
                f"HoTT path {path_id} is not term-level typed",
                reason_code=HOTT_PATH_AMBIENT_TYPE_INVALID,
            )
        fiber_id = str(row["ambient_fiber_id"])
        fiber = path_fibers.get(fiber_id)
        if fiber is None:
            _fail(f"HoTT path {path_id} cites an unknown indexed fiber")
        referenced_fibers.add(fiber_id)
        boundary_fields = (
            "level",
            "ambient_type_id",
            "source_term_id",
            "target_term_id",
            "source_fiber_truth",
            "target_fiber_truth",
        )
        if any(row[field] != fiber[field] for field in boundary_fields):
            _fail(
                f"HoTT path {path_id} differs from its exact indexed fiber",
                reason_code=HOTT_PATH_INDEXED_BOUNDARY_INVALID,
            )
        source_truth, target_truth = (
            fiber["source_fiber_truth"],
            fiber["target_fiber_truth"],
        )
        if (source_truth is None) != (target_truth is None):
            _fail(f"HoTT path {path_id} has only one predicate-fiber boundary")
    if referenced_fibers != set(path_fibers):
        _fail("HoTT path-fiber index contains an unreferenced fiber")
    path_graphs: dict[
        tuple[int, str],
        dict[tuple[str, bool | None], set[tuple[str, bool | None]]],
    ] = {}
    for row in paths.values():
        graph = path_graphs.setdefault(
            (int(row["level"]), str(row["ambient_type_id"])), {}
        )
        source_node = (str(row["source_term_id"]), row["source_fiber_truth"])
        target_node = (str(row["target_term_id"]), row["target_fiber_truth"])
        graph.setdefault(source_node, set()).add(target_node)
        graph.setdefault(target_node, set()).add(source_node)

    equivalences = _index(model["equivalences"], "equivalence_id", "HoTT equivalence")
    for equivalence_id, row in equivalences.items():
        domain, codomain = str(row["domain_type_id"]), str(row["codomain_type_id"])
        forward = maps.get(str(row["forward_map_id"]))
        inverse = maps.get(str(row["inverse_map_id"]))
        if forward is None or inverse is None:
            _fail(f"equivalence {equivalence_id} cites an unknown map")
        if (forward["domain_type_id"], forward["codomain_type_id"]) != (domain, codomain):
            _fail(f"equivalence {equivalence_id} forward map is ill-typed")
        if (inverse["domain_type_id"], inverse["codomain_type_id"]) != (codomain, domain):
            _fail(f"equivalence {equivalence_id} inverse map is ill-typed")
        forward_action = map_actions[str(row["forward_map_id"])]
        inverse_action = map_actions[str(row["inverse_map_id"])]
        left_ids = [str(value) for value in row["left_inverse_homotopy_ids"]]
        right_ids = [str(value) for value in row["right_inverse_homotopy_ids"]]
        if len(left_ids) != len(terms[domain]) or len(right_ids) != len(terms[codomain]):
            _fail(f"equivalence {equivalence_id} lacks pointwise inverse homotopies")
        for term, path_id in zip(sorted(terms[domain]), left_ids):
            path = paths.get(path_id)
            composite = inverse_action[forward_action[term]]
            if path is None or path["level"] != 1 or path["ambient_type_id"] != domain or path["source_term_id"] != composite or path["target_term_id"] != term:
                _fail(
                    f"equivalence {equivalence_id} left inverse homotopy is not executable",
                    reason_code=HOTT_INVERSE_HOMOTOPY_BOUNDARY_INVALID,
                )
            if path["source_fiber_truth"] is not None or path["target_fiber_truth"] is not None:
                _fail(
                    f"equivalence {equivalence_id} left inverse homotopy changes its null base boundary",
                    reason_code=HOTT_INVERSE_BASE_BOUNDARY_INVALID,
                )
        for term, path_id in zip(sorted(terms[codomain]), right_ids):
            path = paths.get(path_id)
            composite = forward_action[inverse_action[term]]
            if path is None or path["level"] != 1 or path["ambient_type_id"] != codomain or path["source_term_id"] != composite or path["target_term_id"] != term:
                _fail(
                    f"equivalence {equivalence_id} right inverse homotopy is not executable",
                    reason_code=HOTT_INVERSE_HOMOTOPY_BOUNDARY_INVALID,
                )
            if path["source_fiber_truth"] is not None or path["target_fiber_truth"] is not None:
                _fail(
                    f"equivalence {equivalence_id} right inverse homotopy changes its null base boundary",
                    reason_code=HOTT_INVERSE_BASE_BOUNDARY_INVALID,
                )
        if any(inverse_action[forward_action[term]] != term for term in terms[domain]) or any(
            forward_action[inverse_action[term]] != term for term in terms[codomain]
        ):
            _fail(f"equivalence {equivalence_id} maps are not inverse on the finite terms")

    predicates = _index(model["transported_predicates"], "predicate_id", "transported predicate")
    predicate_fibers: dict[str, tuple[dict[str, bool], dict[str, bool]]] = {}
    for predicate_id, row in predicates.items():
        source, target = str(row["base_type_id"]), str(row["target_type_id"])
        if source not in types or target not in types:
            _fail(f"predicate {predicate_id} has a dangling source or target type")
        source_rows = list(row["source_fiber"])
        target_rows = list(row["target_fiber"])
        source_fiber = {str(item["term_id"]): bool(item["truth_value"]) for item in source_rows}
        target_fiber = {str(item["term_id"]): bool(item["truth_value"]) for item in target_rows}
        if len(source_fiber) != len(source_rows) or set(source_fiber) != terms[source]:
            _fail(f"predicate {predicate_id} source fiber is not total")
        if len(target_fiber) != len(target_rows) or set(target_fiber) != terms[target]:
            _fail(f"predicate {predicate_id} target fiber is not total")
        predicate_fibers[predicate_id] = (source_fiber, target_fiber)

    transports = _index(model["transports"], "transport_id", "transport")
    transport_actions: dict[str, dict[str, tuple[str, bool, bool]]] = {}
    for transport_id, row in transports.items():
        equivalence = equivalences.get(str(row["equivalence_id"]))
        predicate = predicates.get(str(row["predicate_id"]))
        source, target = str(row["source_type_id"]), str(row["target_type_id"])
        if equivalence is None or predicate is None:
            _fail(f"transport {transport_id} cites an unknown equivalence or predicate")
        if (equivalence["domain_type_id"], equivalence["codomain_type_id"]) != (source, target):
            _fail(f"transport {transport_id} endpoints differ from its equivalence")
        if (predicate["base_type_id"], predicate["target_type_id"]) != (source, target):
            _fail(f"transport {transport_id} predicate family has the wrong fibers")
        action = _fiber_action(row, terms[source], terms[target], label=f"transport {transport_id}")
        forward_action = map_actions[str(equivalence["forward_map_id"])]
        source_fiber, target_fiber = predicate_fibers[str(row["predicate_id"])]
        expected = {
            term: (forward_action[term], source_fiber[term], target_fiber[forward_action[term]])
            for term in terms[source]
        }
        if action != expected or any(source_truth != target_truth for _, source_truth, target_truth in action.values()):
            _fail(f"transport {transport_id} does not preserve its target-fiber predicate")
        transport_actions[transport_id] = action

    compositions = _index(model["transport_compositions"], "composition_id", "transport composition")
    for composition_id, row in compositions.items():
        path_ids = [str(value) for value in row["path_transport_ids"]]
        if len(path_ids) < 2 or any(value not in transports for value in path_ids):
            _fail(f"transport composition {composition_id} cites an invalid path")
        for left, right in zip(path_ids, path_ids[1:]):
            if transports[left]["target_type_id"] != transports[right]["source_type_id"]:
                _fail(f"transport composition {composition_id} is not composable")
        action = dict(transport_actions[path_ids[0]])
        for path_id in path_ids[1:]:
            action = _compose_fiber(action, transport_actions[path_id])
        result_id = str(row["result_transport_id"])
        if result_id not in transports or action != transport_actions[result_id]:
            _fail(f"transport composition {composition_id} does not execute to its result")

    cells = _index(model["coherence_cells"], "cell_id", "coherence cell")
    for cell_id, row in cells.items():
        source_ids = [str(value) for value in row["source_transport_ids"]]
        target_ids = [str(value) for value in row["target_transport_ids"]]
        for path_ids in (source_ids, target_ids):
            if len(path_ids) < 2 or any(value not in transports for value in path_ids):
                _fail(f"coherence cell {cell_id} has an unknown boundary transport")
            for left, right in zip(path_ids, path_ids[1:]):
                if transports[left]["target_type_id"] != transports[right]["source_type_id"]:
                    _fail(f"coherence cell {cell_id} boundary is not composable")
        source_endpoint = (transports[source_ids[0]]["source_type_id"], transports[source_ids[-1]]["target_type_id"])
        target_endpoint = (transports[target_ids[0]]["source_type_id"], transports[target_ids[-1]]["target_type_id"])
        if source_endpoint != target_endpoint or source_endpoint != (row["source_type_id"], row["target_type_id"]):
            _fail(f"coherence cell {cell_id} boundaries are not parallel")
        source_composition = compositions.get(str(row["source_composition_id"]))
        target_composition = compositions.get(str(row["target_composition_id"]))
        if source_composition is None or target_composition is None or source_composition["path_transport_ids"] != source_ids or target_composition["path_transport_ids"] != target_ids:
            _fail(f"coherence cell {cell_id} is not bound to its exact compositions")
        source_result = transport_actions[str(source_composition["result_transport_id"])]
        target_result = transport_actions[str(target_composition["result_transport_id"])]
        different_terms = sorted(term for term in source_result if source_result[term] != target_result[term])
        if row["status"] == "proved":
            pointwise_ids = [str(value) for value in row["pointwise_path_ids"]]
            source_terms = sorted(terms[str(row["source_type_id"])])
            if (
                different_terms
                or len(pointwise_ids) != len(source_terms)
                or len(set(pointwise_ids)) != len(pointwise_ids)
                or row["missing_path_term_ids"]
            ):
                _fail(f"coherence cell {cell_id} has no complete pointwise proof")
            for source_term, path_id in zip(source_terms, pointwise_ids):
                path = paths.get(path_id)
                source_boundary = source_result[source_term]
                target_boundary = target_result[source_term]
                expected_fiber = f"{cell_id}.fiber.{source_term.rsplit('.', 1)[-1]}"
                if (
                    path is None
                    or int(path["level"]) != int(row["level"]) - 1
                    or path["ambient_type_id"] != row["target_type_id"]
                    or path["ambient_fiber_id"] != expected_fiber
                    or path["source_term_id"] != source_boundary[0]
                    or path["target_term_id"] != target_boundary[0]
                    or path["source_fiber_truth"] != source_boundary[2]
                    or path["target_fiber_truth"] != target_boundary[2]
                ):
                    _fail(
                        f"coherence cell {cell_id} pointwise path {path_id} has the wrong "
                        "ambient type/fiber or composite boundary"
                    )
        elif row["status"] == "refuted":
            if (
                not different_terms
                or sorted(row["missing_path_term_ids"]) != different_terms
                or row["pointwise_path_ids"]
            ):
                _fail(f"coherence cell {cell_id} does not expose its exact missing paths")
            for source_term in different_terms:
                source_boundary = source_result[source_term]
                target_boundary = target_result[source_term]
                if _finite_path_inhabited(
                    path_graphs,
                    level=int(row["level"]) - 1,
                    ambient_type_id=str(row["target_type_id"]),
                    source_term_id=source_boundary[0],
                    target_term_id=target_boundary[0],
                    source_fiber_truth=source_boundary[2],
                    target_fiber_truth=target_boundary[2],
                ):
                    _fail(
                        f"coherence cell {cell_id} declares missing boundary for "
                        f"{source_term}, but its exact indexed path space is inhabited",
                        reason_code=HOTT_REFUTATION_PATH_INHABITED,
                    )
        elif row["pointwise_path_ids"] or row["missing_path_term_ids"]:
            _fail(
                f"coherence cell {cell_id} cannot declare proved or refuted "
                "pointwise evidence while its status is open or conditional"
            )

    policy = model["truncation_policy"]
    maximum_level = max([1] + [int(row["level"]) for row in cells.values()])
    open_cells = sorted(cell_id for cell_id, row in cells.items() if row["status"] != "proved")
    if int(policy["retained_through_level"]) < maximum_level:
        _fail("truncation policy erases a declared coherence level")
    if sorted(policy["open_cell_ids"]) != open_cells:
        _fail("truncation policy does not name every open coherence cell")
    if policy["application_status"] == "applied" and open_cells:
        _fail("truncation cannot be applied while coherence cells remain open")
    return {
        "types": types, "terms": terms, "maps": maps, "map_actions": map_actions,
        "paths": paths, "path_fibers": path_fibers,
        "equivalences": equivalences, "predicates": predicates,
        "transports": transports, "transport_actions": transport_actions,
        "compositions": compositions, "cells": cells,
    }


def _hott_countermodel(model: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    structure = _hott_structure(model)
    transports = structure["transports"]
    actions = structure["transport_actions"]

    def path_action(path_ids: Sequence[str]) -> tuple[str, str, dict[str, tuple[str, bool, bool]]]:
        if not path_ids or any(path_id not in transports for path_id in path_ids):
            _fail("HoTT countermodel cites an unknown transport")
        for left, right in zip(path_ids, path_ids[1:]):
            if transports[left]["target_type_id"] != transports[right]["source_type_id"]:
                _fail("HoTT countermodel transport path is not composable")
        result = dict(actions[path_ids[0]])
        for path_id in path_ids[1:]:
            result = _compose_fiber(result, actions[path_id])
        return str(transports[path_ids[0]]["source_type_id"]), str(transports[path_ids[-1]]["target_type_id"]), result

    left = path_action(witness["left_path_ids"])
    right = path_action(witness["right_path_ids"])
    if left[:2] != right[:2]:
        _fail("HoTT countermodel paths do not have parallel boundaries")
    counterexamples = [
        {
            "source_term_id": term,
            "left_target_term_id": left[2][term][0],
            "right_target_term_id": right[2][term][0],
            "left_truth": left[2][term][2],
            "right_truth": right[2][term][2],
        }
        for term in sorted(left[2])
        if left[2][term] != right[2][term]
    ]
    return {
        "result": "noncoherent" if counterexamples else "coherent",
        "source_type_id": left[0], "target_type_id": left[1],
        "left_transport_digest": canonical_digest(left[2]),
        "right_transport_digest": canonical_digest(right[2]),
        "counterexamples": counterexamples,
        "claim_authority": "finite_local_countermodel_only",
    }


WITNESS_VALIDATOR_REGISTRY: dict[str, dict[str, Any]] = {
    "finite-category-countermodel.v1": {
        "version": "1.0.0", "kind": "local_symbolic_countermodel", "runner": _category_countermodel,
    },
    "finite-hott-countermodel.v1": {
        "version": "1.0.0", "kind": "local_symbolic_countermodel", "runner": _hott_countermodel,
    },
    "finite-physical-diagram-countermodel.v1": {
        "version": "1.0.0", "kind": "local_symbolic_countermodel", "runner": _physical_countermodel,
    },
}


def _witness_core(witness: Mapping[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in witness.items() if key not in {"evidence", "certificate"}}


def build_negative_witness(
    *, model: Mapping[str, Any], validator_id: str, witness_kind: str, step_namespace: str,
    prefix: str, source_id: str, target_id: str, left_path_ids: Sequence[str],
    right_path_ids: Sequence[str], left_composite_id: str, right_composite_id: str,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    """Execute the registered countermodel and seal its exact output."""

    witness: dict[str, Any] = {
        "witness_kind": witness_kind,
        "diagram_id": f"{prefix}.diagram",
        "step_namespace": step_namespace,
        "source_id": source_id,
        "target_id": target_id,
        "left_path_ids": list(left_path_ids),
        "right_path_ids": list(right_path_ids),
        "left_composite_id": left_composite_id,
        "right_composite_id": right_composite_id,
        "exact_obstruction": "A registry-replayed finite countermodel computes unequal parallel composites.",
        "boundary_conditions": [
            "The finite carrier and every map action are sealed before replay.",
            "The countermodel localizes a burden and makes no continuum or theorem claim.",
        ],
        "exact": True,
    }
    entry = WITNESS_VALIDATOR_REGISTRY[validator_id]
    result = entry["runner"](model, witness)
    expected_result = "noncommuting" if witness_kind == "noncommutativity" else "noncoherent"
    if result["result"] != expected_result:
        _fail("declared negative witness has no executable counterexample")
    evidence = [{
        "evidence_id": f"{prefix}.countermodel-evidence",
        "artifact_path": "skills/common/abstraction_formal_reasoning.py",
        "claim": "The registered local validator replayed an unequal finite countermodel.",
        "payload": result,
        "content_digest": canonical_digest(result),
    }]
    witness_digest = canonical_digest(witness)
    evidence_digest = canonical_digest(evidence)
    input_digest = canonical_digest({"model": model, "witness": witness})
    output_digest = canonical_digest(result)
    executable_digest = callable_digest(entry["runner"])
    dependency_authority = _bound_dependency_authority(_dependency_context)
    receipt = {
        "validator_id": validator_id,
        "validator_version": entry["version"],
        "validator_kind": entry["kind"],
        "executable_digest": executable_digest,
        "input_digest": input_digest,
        "validated_witness_digest": witness_digest,
        "validated_evidence_digest": evidence_digest,
        "validated_output_digest": output_digest,
        "dependency_authority_digest": dependency_authority["content_digest"],
        "status": "passed",
    }
    receipt["receipt_id"] = stable_identifier("formal-witness-receipt", receipt)
    certificate = {
        "certificate_id": stable_identifier("formal-witness-certificate", witness_digest, output_digest),
        "kind": "countermodel",
        "result": expected_result,
        "witness_digest": witness_digest,
        "evidence_digest": evidence_digest,
        "validator_receipt": receipt,
    }
    return {**witness, "evidence": evidence, "certificate": certificate}


def validate_negative_witness(
    model: Mapping[str, Any], witness: Mapping[str, Any], *, expected_validator_id: str,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    entry = WITNESS_VALIDATOR_REGISTRY.get(expected_validator_id)
    if entry is None:
        _fail("negative witness validator is not in the approved local registry")
    certificate = witness["certificate"]
    receipt = certificate["validator_receipt"]
    if receipt["validator_id"] != expected_validator_id:
        _fail("negative witness cites the wrong registered validator")
    core = _witness_core(witness)
    witness_digest = canonical_digest(core)
    evidence = list(witness["evidence"])
    if len(evidence) != 1:
        _fail("negative witness must expose the one exact replay output")
    result = entry["runner"](model, core)
    evidence_digest = canonical_digest(evidence)
    output_digest = canonical_digest(result)
    expected_result = "noncommuting" if witness["witness_kind"] == "noncommutativity" else "noncoherent"
    expected_evidence = [{
        "evidence_id": evidence[0]["evidence_id"],
        "artifact_path": "skills/common/abstraction_formal_reasoning.py",
        "claim": "The registered local validator replayed an unequal finite countermodel.",
        "payload": result,
        "content_digest": output_digest,
    }]
    dependency_authority = _bound_dependency_authority(_dependency_context)
    expected_receipt = {
        "validator_id": expected_validator_id,
        "validator_version": entry["version"],
        "validator_kind": entry["kind"],
        "executable_digest": callable_digest(entry["runner"]),
        "input_digest": canonical_digest({"model": model, "witness": core}),
        "validated_witness_digest": witness_digest,
        "validated_evidence_digest": canonical_digest(expected_evidence),
        "validated_output_digest": output_digest,
        "dependency_authority_digest": dependency_authority["content_digest"],
        "status": "passed",
    }
    expected_receipt["receipt_id"] = stable_identifier("formal-witness-receipt", expected_receipt)
    if evidence != expected_evidence:
        _fail("negative witness evidence is not the registered replay output")
    if receipt != expected_receipt:
        _fail("negative witness receipt is not bound to the registered executable")
    if certificate != {
        "certificate_id": stable_identifier("formal-witness-certificate", witness_digest, output_digest),
        "kind": "countermodel", "result": expected_result,
        "witness_digest": witness_digest, "evidence_digest": canonical_digest(expected_evidence),
        "validator_receipt": expected_receipt,
    }:
        _fail("negative witness certificate does not match the replayed countermodel")
    if result["result"] != expected_result or not result["counterexamples"]:
        _fail("negative witness replay did not derive an obstruction")
    return result


def _action_rows(action: Mapping[str, str]) -> list[dict[str, str]]:
    return [
        {"source_element_id": source, "target_element_id": target}
        for source, target in sorted(action.items())
    ]


def _composition_table(
    prefix: str, arrows: Sequence[Mapping[str, Any]], *, left_pair: tuple[str, str],
    right_pair: tuple[str, str], left_id: str, right_id: str,
) -> list[dict[str, Any]]:
    by_id = {str(row["morphism_id"]): row for row in arrows}
    signature_to_id = {
        (row["domain_id"], row["codomain_id"], tuple(sorted(
            (item["source_element_id"], item["target_element_id"]) for item in row["action"]
        ))): row["morphism_id"]
        for row in arrows
    }
    rows: list[dict[str, Any]] = []
    for first_id, first in by_id.items():
        for second_id, second in by_id.items():
            if first["codomain_id"] != second["domain_id"]:
                continue
            first_action = {row["source_element_id"]: row["target_element_id"] for row in first["action"]}
            second_action = {row["source_element_id"]: row["target_element_id"] for row in second["action"]}
            result_action = _compose_finite(first_action, second_action)
            result_id = signature_to_id[(first["domain_id"], second["codomain_id"], tuple(sorted(result_action.items())))]
            pair = (first_id, second_id)
            composition_id = left_id if pair == left_pair else right_id if pair == right_pair else (
                f"{prefix}.compose.{first_id.rsplit('.', 1)[-1]}.{second_id.rsplit('.', 1)[-1]}"
            )
            rows.append({
                "composition_id": composition_id,
                "path_morphism_ids": [first_id, second_id],
                "result_morphism_id": result_id,
                "associativity_obligation_id": f"{composition_id}.associativity",
            })
    rows.sort(key=lambda row: (row["composition_id"] not in {left_id, right_id}, row["composition_id"]))
    return rows


def build_category_model_and_witness(
    prefix: str,
    obligation_id: str,
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
    _task_relation_binding: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build a finite category whose parallel composites differ extensionally."""

    a, b, c = f"{prefix}.A", f"{prefix}.B", f"{prefix}.C"
    a_terms = [f"{prefix}.a0", f"{prefix}.a1"]
    b_terms = [f"{prefix}.b0", f"{prefix}.b1"]
    c_terms = [f"{prefix}.c0", f"{prefix}.c1", f"{prefix}.c2"]
    f1, g1, f2, g2 = (f"{prefix}.{name}" for name in ("f1", "g1", "f2", "g2"))
    left_result, cross_one, cross_two, right_result = (
        f"{prefix}.{name}" for name in ("left-result", "cross-one", "cross-two", "right-result")
    )
    arrow_specs = [
        (f"{prefix}.idA", a, a, dict(zip(a_terms, a_terms)), True, "identity"),
        (f"{prefix}.idB", b, b, dict(zip(b_terms, b_terms)), True, "identity"),
        (f"{prefix}.idC", c, c, dict(zip(c_terms, c_terms)), True, "identity"),
        (f1, a, b, {a_terms[0]: b_terms[0], a_terms[1]: b_terms[1]}, False, "translation"),
        (g1, a, b, {a_terms[0]: b_terms[1], a_terms[1]: b_terms[0]}, False, "comparison"),
        (f2, b, c, {b_terms[0]: c_terms[0], b_terms[1]: c_terms[1]}, False, "normalization"),
        (g2, b, c, {b_terms[0]: c_terms[1], b_terms[1]: c_terms[2]}, False, "translation"),
        (left_result, a, c, {a_terms[0]: c_terms[0], a_terms[1]: c_terms[1]}, False, "composite"),
        (cross_one, a, c, {a_terms[0]: c_terms[1], a_terms[1]: c_terms[2]}, False, "composite"),
        (cross_two, a, c, {a_terms[0]: c_terms[1], a_terms[1]: c_terms[0]}, False, "composite"),
        (right_result, a, c, {a_terms[0]: c_terms[2], a_terms[1]: c_terms[1]}, False, "composite"),
    ]
    morphisms = [{
        "morphism_id": arrow_id, "name": f"Executable finite arrow {arrow_id}",
        "domain_id": domain, "codomain_id": codomain, "kind": kind,
        "mapping_rule": "Apply the sealed total action table to the finite carrier.",
        "action": _action_rows(action), "is_identity": identity,
    } for arrow_id, domain, codomain, action, identity, kind in arrow_specs]
    left_comp, right_comp = f"{prefix}.compose-left", f"{prefix}.compose-right"
    compositions = _composition_table(
        prefix, morphisms, left_pair=(f1, f2), right_pair=(g1, g2),
        left_id=left_comp, right_id=right_comp,
    )
    by_pair = {tuple(row["path_morphism_ids"]): row for row in compositions}
    cone_checks = []
    for candidate in (f1, g1):
        composition = by_pair[(candidate, f2)]
        cone_checks.append({
            "candidate_morphism_id": candidate,
            "composition_id": composition["composition_id"],
            "commutes": composition["result_morphism_id"] == left_result,
        })
    model = {
        "objects": [
            {"object_id": a, "name": "Frozen finite source presentation", "kind": "source", "carrier": "Two sealed source terms for executable law checks.", "element_ids": a_terms, "invariants": ["The target statement remains fixed at the source."]},
            {"object_id": b, "name": "Finite mediating presentation", "kind": "apex", "carrier": "Two sealed mediator terms for factorization checks.", "element_ids": b_terms, "invariants": ["The mediation interface retains its declared terms."]},
            {"object_id": c, "name": "Frozen finite target presentation", "kind": "target", "carrier": "Three sealed target terms exposing unequal composites.", "element_ids": c_terms, "invariants": ["The target statement remains fixed at the target."]},
        ],
        "morphisms": morphisms,
        "identities": [
            {"object_id": a, "morphism_id": f"{prefix}.idA"},
            {"object_id": b, "morphism_id": f"{prefix}.idB"},
            {"object_id": c, "morphism_id": f"{prefix}.idC"},
        ],
        "compositions": compositions,
        "universal_property": {
            "construction_id": f"{prefix}.finite-factorization",
            "source_object_id": a, "apex_object_id": b, "target_object_id": c,
            "target_morphism_id": left_result, "factor_out_morphism_id": f2,
            "mediating_morphism_ids": [f1, g1], "cone_checks": cone_checks,
            "unique_mediator_id": f1, "scope_complete": True,
            "uniqueness_obligation_id": f"{prefix}.finite-unique",
            "claim": "Within the complete finite source-to-apex hom-set, exactly one mediator reaches the target arrow.",
            "status": "proved",
        },
        "new_consequence": {
            "consequence_id": f"{prefix}.consequence",
            "statement": "The frozen target burden reduces to an extensional comparison of two total composites.",
            "derivation_refs": [left_comp, right_comp, f"{prefix}.finite-factorization"],
            "obligation_ids": [obligation_id],
            "new_dependency": "The obligation now depends on a replayable finite countermodel and an open target transfer.",
        },
    }
    if _task_relation_binding is not None:
        model["task_relation_binding"] = copy.deepcopy(dict(_task_relation_binding))
    _validate_category_structure(model, {obligation_id})
    witness = build_negative_witness(
        model=model, validator_id="finite-category-countermodel.v1",
        witness_kind="noncommutativity", step_namespace="morphism", prefix=prefix,
        source_id=a, target_id=c, left_path_ids=[f1, f2], right_path_ids=[g1, g2],
        left_composite_id=left_comp, right_composite_id=right_comp,
        _dependency_context=_dependency_context,
    )
    return model, witness


def _validate_category_structure(model: Mapping[str, Any], obligation_ids: set[str]) -> dict[str, Any]:
    structure = _finite_diagram(
        objects_rows=model["objects"], arrows_rows=model["morphisms"],
        compositions_rows=model["compositions"], arrow_id_field="morphism_id",
        domain_field="domain_id", codomain_field="codomain_id", label="category",
    )
    identities = list(model["identities"])
    if len(identities) != len(structure["objects"]) or len({row["object_id"] for row in identities}) != len(identities):
        _fail("category identity ledger must cover each object exactly once")
    for row in identities:
        if structure["identity_ids"].get(str(row["object_id"])) != row["morphism_id"]:
            _fail("category identity ledger differs from the executable identity")
    universal = model["universal_property"]
    source, apex, target = universal["source_object_id"], universal["apex_object_id"], universal["target_object_id"]
    if any(object_id not in structure["objects"] for object_id in (source, apex, target)):
        _fail("universal property has an unknown object")
    target_arrow = structure["arrows"].get(str(universal["target_morphism_id"]))
    factor_out = structure["arrows"].get(str(universal["factor_out_morphism_id"]))
    if target_arrow is None or (target_arrow["domain_id"], target_arrow["codomain_id"]) != (source, target):
        _fail("universal property target arrow is ill-typed")
    if factor_out is None or (factor_out["domain_id"], factor_out["codomain_id"]) != (apex, target):
        _fail("universal property factor-out arrow is ill-typed")
    complete_candidates = sorted(
        arrow_id for arrow_id, arrow in structure["arrows"].items()
        if (arrow["domain_id"], arrow["codomain_id"]) == (source, apex)
    )
    if universal["scope_complete"] is not True or sorted(universal["mediating_morphism_ids"]) != complete_candidates:
        _fail("universal-property mediator scope is not the complete finite hom-set")
    checks = _index(universal["cone_checks"], "candidate_morphism_id", "universal cone check")
    if set(checks) != set(complete_candidates):
        _fail("universal property lacks one commuting-cone check per mediator")
    commuting: list[str] = []
    for candidate, row in checks.items():
        pair = (candidate, str(universal["factor_out_morphism_id"]))
        composition = structure["compositions"].get(str(row["composition_id"]))
        if composition is None or tuple(composition["path_morphism_ids"]) != pair:
            _fail("universal cone check cites the wrong composition")
        actual = structure["actions"][composition["result_morphism_id"]] == structure["actions"][universal["target_morphism_id"]]
        if bool(row["commutes"]) != actual:
            _fail("universal cone commutation flag is not executable")
        if actual:
            commuting.append(candidate)
    if universal["status"] == "proved" and (
        len(commuting) != 1 or universal["unique_mediator_id"] != commuting[0]
    ):
        _fail("proved universal property lacks one extensionally unique mediator")
    consequence = model["new_consequence"]
    derivations = set(structure["arrows"]) | set(structure["compositions"]) | {universal["construction_id"]}
    if not set(consequence["derivation_refs"]).issubset(derivations) or not set(consequence["obligation_ids"]).issubset(obligation_ids):
        _fail("categorical consequence has a dangling derivation or obligation")
    return structure


def validate_category_model(
    model: Mapping[str, Any], witness: Mapping[str, Any], obligation_ids: set[str],
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    structure = _validate_category_structure(model, obligation_ids)
    left = tuple(witness["left_path_ids"])
    right = tuple(witness["right_path_ids"])
    left_row = structure["compositions"].get(str(witness["left_composite_id"]))
    right_row = structure["compositions"].get(str(witness["right_composite_id"]))
    if left_row is None or right_row is None or tuple(left_row["path_morphism_ids"]) != left or tuple(right_row["path_morphism_ids"]) != right:
        _fail("category witness is not bound to its exact composition rows")
    result = validate_negative_witness(
        model,
        witness,
        expected_validator_id="finite-category-countermodel.v1",
        _dependency_context=_dependency_context,
    )
    if (result["source_object_id"], result["target_object_id"]) != (witness["source_id"], witness["target_id"]):
        _fail("category witness replay has different endpoints")
    return result


def _term_rows(action: Mapping[str, str]) -> list[dict[str, str]]:
    return [{"source_term_id": source, "target_term_id": target} for source, target in sorted(action.items())]


def _truth_rows(values: Mapping[str, bool]) -> list[dict[str, Any]]:
    return [{"term_id": term, "truth_value": truth} for term, truth in sorted(values.items())]


def build_hott_model_and_witness(
    prefix: str,
    obligation_id: str,
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
    _task_relation_binding: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build finite equivalences with indexed homotopy fibers and a failed 2-cell."""

    a, b, c = f"{prefix}.A", f"{prefix}.B", f"{prefix}.C"
    terms = {
        a: [f"{prefix}.a0", f"{prefix}.a1"],
        b: [f"{prefix}.b0", f"{prefix}.b1"],
        c: [f"{prefix}.c0", f"{prefix}.c1"],
    }
    maps: list[dict[str, Any]] = []
    paths: list[dict[str, Any]] = []
    path_fibers: list[dict[str, Any]] = []
    equivalences: list[dict[str, Any]] = []

    def add_path(
        *,
        path_id: str,
        level: int,
        ambient_type_id: str,
        source_term_id: str,
        target_term_id: str,
        source_fiber_truth: bool | None,
        target_fiber_truth: bool | None,
        constructor: str,
        fiber_id: str | None = None,
    ) -> None:
        """Create one path and its exact finite fiber-index row together."""

        exact_fiber_id = fiber_id or f"{path_id}.identity-fiber"
        boundary = {
            "level": level,
            "ambient_type_id": ambient_type_id,
            "source_term_id": source_term_id,
            "target_term_id": target_term_id,
            "source_fiber_truth": source_fiber_truth,
            "target_fiber_truth": target_fiber_truth,
        }
        path_fibers.append({"fiber_id": exact_fiber_id, **boundary})
        paths.append(
            {
                "path_id": path_id,
                "ambient_fiber_id": exact_fiber_id,
                **boundary,
                "constructor": constructor,
            }
        )

    def add_equivalence(tag: str, source: str, target: str, action: dict[str, str]) -> str:
        forward_id, inverse_id = f"{prefix}.map{tag}", f"{prefix}.inv{tag}"
        inverse_action = {value: key for key, value in action.items()}
        maps.extend([
            {"map_id": forward_id, "domain_type_id": source, "codomain_type_id": target, "mapping_rule": "Apply the sealed finite forward term table.", "term_action": _term_rows(action)},
            {"map_id": inverse_id, "domain_type_id": target, "codomain_type_id": source, "mapping_rule": "Apply the sealed finite inverse term table.", "term_action": _term_rows(inverse_action)},
        ])
        left_ids, right_ids = [], []
        for term in sorted(terms[source]):
            path_id = f"{prefix}.left-{tag}-{term.rsplit('.', 1)[-1]}"
            composite = inverse_action[action[term]]
            add_path(
                path_id=path_id,
                level=1,
                ambient_type_id=source,
                source_term_id=composite,
                target_term_id=term,
                source_fiber_truth=None,
                target_fiber_truth=None,
                constructor="Pointwise inverse-after-forward homotopy.",
            )
            left_ids.append(path_id)
        for term in sorted(terms[target]):
            path_id = f"{prefix}.right-{tag}-{term.rsplit('.', 1)[-1]}"
            composite = action[inverse_action[term]]
            add_path(
                path_id=path_id,
                level=1,
                ambient_type_id=target,
                source_term_id=composite,
                target_term_id=term,
                source_fiber_truth=None,
                target_fiber_truth=None,
                constructor="Pointwise forward-after-inverse homotopy.",
            )
            right_ids.append(path_id)
        equivalence_id = f"{prefix}.eq{tag}"
        equivalences.append({
            "equivalence_id": equivalence_id, "domain_type_id": source, "codomain_type_id": target,
            "forward_map_id": forward_id, "inverse_map_id": inverse_id,
            "left_inverse_homotopy_ids": left_ids, "right_inverse_homotopy_ids": right_ids,
            "status": "proved",
        })
        return equivalence_id

    eq_ab1 = add_equivalence("AB1", a, b, dict(zip(terms[a], terms[b])))
    eq_ab2 = add_equivalence("AB2", a, b, {terms[a][0]: terms[b][1], terms[a][1]: terms[b][0]})
    eq_bc1 = add_equivalence("BC1", b, c, dict(zip(terms[b], terms[c])))
    eq_bc2 = add_equivalence("BC2", b, c, dict(zip(terms[b], terms[c])))
    eq_ac1 = add_equivalence("AC1", a, c, dict(zip(terms[a], terms[c])))
    eq_ac2 = add_equivalence("AC2", a, c, {terms[a][0]: terms[c][1], terms[a][1]: terms[c][0]})
    map_by_id = {row["map_id"]: row for row in maps}
    eq_by_id = {row["equivalence_id"]: row for row in equivalences}
    predicates: list[dict[str, Any]] = []
    transports: list[dict[str, Any]] = []

    def add_transport(
        tag: str,
        equivalence_id: str,
        source_truth_override: Mapping[str, bool] | None = None,
    ) -> str:
        equivalence = eq_by_id[equivalence_id]
        source, target = equivalence["domain_type_id"], equivalence["codomain_type_id"]
        forward = map_by_id[equivalence["forward_map_id"]]
        action = {row["source_term_id"]: row["target_term_id"] for row in forward["term_action"]}
        source_truth = (
            {str(term): bool(value) for term, value in source_truth_override.items()}
            if source_truth_override is not None
            else {term: index == 0 for index, term in enumerate(terms[source])}
        )
        if set(source_truth) != set(terms[source]):
            _fail(f"transport {tag} source truth override is not total")
        target_truth = {term: False for term in terms[target]}
        for source_term, target_term in action.items():
            target_truth[target_term] = source_truth[source_term]
        predicate_id = f"{prefix}.predicate-{tag}"
        predicates.append({
            "predicate_id": predicate_id, "name": f"Finite transported predicate {tag}",
            "base_type_id": source, "target_type_id": target, "codomain_universe": 0,
            "source_statement": "The sealed Boolean predicate on every source term.",
            "target_statement": "The exact image Boolean predicate on every target term.",
            "source_fiber": _truth_rows(source_truth), "target_fiber": _truth_rows(target_truth),
            "preservation_obligation_id": obligation_id,
        })
        transport_id = f"{prefix}.{tag}"
        transports.append({
            "transport_id": transport_id, "equivalence_id": equivalence_id,
            "predicate_id": predicate_id, "source_type_id": source, "target_type_id": target,
            "mapping_rule": "Transport the sealed Boolean fiber along the exact forward equivalence map.",
            "fiber_action": [
                {"source_term_id": source_term, "target_term_id": target_term,
                 "source_truth": source_truth[source_term], "target_truth": target_truth[target_term]}
                for source_term, target_term in sorted(action.items())
            ],
        })
        return transport_id

    t_ab1, t_ab2 = add_transport("tAB1", eq_ab1), add_transport("tAB2", eq_ab2)
    t_ab2_row = next(row for row in transports if row["transport_id"] == t_ab2)
    t_ab2_target_truth = {
        row["target_term_id"]: bool(row["target_truth"])
        for row in t_ab2_row["fiber_action"]
    }
    t_bc1 = add_transport("tBC1", eq_bc1)
    t_bc2 = add_transport("tBC2", eq_bc2, t_ab2_target_truth)
    t_ac1, t_ac2 = add_transport("tAC1", eq_ac1), add_transport("tAC2", eq_ac2)
    left_comp, right_comp = f"{prefix}.transport-left", f"{prefix}.transport-right"
    cell_id = f"{prefix}.coherence-two-cell"
    proved_cell_id = f"{prefix}.coherence-reflexive-cell"
    left_result_action = {
        row["source_term_id"]: (
            row["target_term_id"], row["source_truth"], row["target_truth"]
        )
        for row in next(
            row for row in transports if row["transport_id"] == t_ac1
        )["fiber_action"]
    }
    pointwise_ids: list[str] = []
    for source_term in sorted(terms[a]):
        path_id = f"{proved_cell_id}.path.{source_term.rsplit('.', 1)[-1]}"
        target_term, _source_truth, target_truth = left_result_action[source_term]
        add_path(
            path_id=path_id,
            level=1,
            ambient_type_id=c,
            source_term_id=target_term,
            target_term_id=target_term,
            source_fiber_truth=target_truth,
            target_fiber_truth=target_truth,
            constructor="Reflexive pointwise path between the exact composite predicate boundaries.",
            fiber_id=f"{proved_cell_id}.fiber.{source_term.rsplit('.', 1)[-1]}",
        )
        pointwise_ids.append(path_id)
    model = {
        "path_space_policy": copy.deepcopy(FINITE_HOTT_PATH_SPACE_POLICY),
        "types": [
            {"type_id": type_id, "name": f"Finite presentation type {type_id}", "universe_level": 1, "truncation_level": 1, "term_ids": type_terms, "constructors": ["Two sealed finite constructors for executable transport."]}
            for type_id, type_terms in terms.items()
        ],
        "maps": maps, "paths": paths, "path_fibers": path_fibers,
        "transported_predicates": predicates,
        "equivalences": equivalences, "transports": transports,
        "transport_compositions": [
            {"composition_id": left_comp, "path_transport_ids": [t_ab1, t_bc1], "result_transport_id": t_ac1},
            {"composition_id": right_comp, "path_transport_ids": [t_ab2, t_bc2], "result_transport_id": t_ac2},
        ],
        "coherence_cells": [
            {
                "cell_id": proved_cell_id, "level": 2,
                "source_transport_ids": [t_ab1, t_bc1], "target_transport_ids": [t_ab1, t_bc1],
                "source_composition_id": left_comp, "target_composition_id": left_comp,
                "source_type_id": a, "target_type_id": c,
                "pointwise_path_ids": pointwise_ids, "missing_path_term_ids": [],
                "coherence_statement": "The identical composite boundaries have exact pointwise paths in their target predicate fibers.",
                "status": "proved",
            },
            {
                "cell_id": cell_id, "level": 2,
                "source_transport_ids": [t_ab1, t_bc1], "target_transport_ids": [t_ab2, t_bc2],
                "source_composition_id": left_comp, "target_composition_id": right_comp,
                "source_type_id": a, "target_type_id": c,
                "pointwise_path_ids": [], "missing_path_term_ids": sorted(terms[a]),
                "coherence_statement": "The two parallel predicate transports require pointwise target-fiber paths.",
                "status": "refuted",
            },
        ],
        "truncation_policy": {
            "default_level": 1, "retained_through_level": 2,
            "application_status": "deferred", "open_cell_ids": [cell_id],
            "truncation_after_obligation_ids": [obligation_id],
            "justification": "Retain the failed two-cell and its term countermodel until the target obligation closes.",
        },
        "new_consequence": {
            "consequence_id": f"{prefix}.consequence",
            "statement": "Path independence becomes one term-level missing two-cell over target predicate fibers.",
            "derivation_refs": [left_comp, right_comp, cell_id],
            "obligation_ids": [obligation_id],
            "new_dependency": "The target now depends on a replayable transport countermodel before truncation.",
        },
    }
    if _task_relation_binding is not None:
        model["task_relation_binding"] = copy.deepcopy(dict(_task_relation_binding))
    _validate_hott_structure(model, {obligation_id})
    witness = build_negative_witness(
        model=model, validator_id="finite-hott-countermodel.v1",
        witness_kind="noncoherence", step_namespace="transport", prefix=prefix,
        source_id=a, target_id=c, left_path_ids=[t_ab1, t_bc1], right_path_ids=[t_ab2, t_bc2],
        left_composite_id=left_comp, right_composite_id=right_comp,
        _dependency_context=_dependency_context,
    )
    return model, witness


def _validate_hott_structure(model: Mapping[str, Any], obligation_ids: set[str]) -> dict[str, Any]:
    structure = _hott_structure(model)
    consequence = model["new_consequence"]
    derivations = set(structure["paths"]) | set(structure["equivalences"]) | set(structure["transports"]) | set(structure["compositions"]) | set(structure["cells"])
    if not set(consequence["derivation_refs"]).issubset(derivations) or not set(consequence["obligation_ids"]).issubset(obligation_ids):
        _fail("HoTT consequence has a dangling derivation or obligation")
    predicate_obligations = {row["preservation_obligation_id"] for row in structure["predicates"].values()}
    if not predicate_obligations.issubset(obligation_ids):
        _fail("transported predicate cites an unknown target obligation")
    if not set(model["truncation_policy"]["truncation_after_obligation_ids"]).issubset(obligation_ids):
        _fail("truncation boundary cites an unknown target obligation")
    return structure


def validate_hott_model(
    model: Mapping[str, Any], witness: Mapping[str, Any], obligation_ids: set[str],
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    structure = _validate_hott_structure(model, obligation_ids)
    left_row = structure["compositions"].get(str(witness["left_composite_id"]))
    right_row = structure["compositions"].get(str(witness["right_composite_id"]))
    if left_row is None or right_row is None or left_row["path_transport_ids"] != witness["left_path_ids"] or right_row["path_transport_ids"] != witness["right_path_ids"]:
        _fail("HoTT witness is not bound to its exact transport compositions")
    result = validate_negative_witness(
        model,
        witness,
        expected_validator_id="finite-hott-countermodel.v1",
        _dependency_context=_dependency_context,
    )
    if (result["source_type_id"], result["target_type_id"]) != (witness["source_id"], witness["target_id"]):
        _fail("HoTT witness replay has different endpoints")
    return result


def build_physical_diagram_and_witness(
    prefix: str,
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build a finite physical-carrier diagram with executable limit-order failure."""

    category, _ = build_category_model_and_witness(
        prefix,
        f"{prefix}.physical-obligation",
        _dependency_context=_dependency_context,
    )
    objects = [
        {"object_id": row["object_id"], "physical_carrier": f"Gauge-invariant finite calibration carrier for {row['object_id']}",
         "element_ids": row["element_ids"], "invariants": row["invariants"]}
        for row in category["objects"]
    ]
    steps = [
        {"step_id": row["morphism_id"], "kind": "identity" if row["is_identity"] else "morphism",
         "domain_id": row["domain_id"], "codomain_id": row["codomain_id"],
         "physical_map": "Execute the sealed finite regulator/core comparison table.",
         "action": row["action"], "is_identity": row["is_identity"]}
        for row in category["morphisms"]
    ]
    diagram = {"objects": objects, "steps": steps, "compositions": category["compositions"]}
    witness = build_negative_witness(
        model=diagram, validator_id="finite-physical-diagram-countermodel.v1",
        witness_kind="noncommutativity", step_namespace="morphism", prefix=prefix,
        source_id=f"{prefix}.A", target_id=f"{prefix}.C",
        left_path_ids=[f"{prefix}.f1", f"{prefix}.f2"],
        right_path_ids=[f"{prefix}.g1", f"{prefix}.g2"],
        left_composite_id=f"{prefix}.compose-left", right_composite_id=f"{prefix}.compose-right",
        _dependency_context=_dependency_context,
    )
    return diagram, witness


def validate_physical_diagram(
    diagram: Mapping[str, Any],
    witness: Mapping[str, Any],
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    adapted = [
        {**copy.deepcopy(dict(row)), "morphism_id": row["step_id"]}
        for row in diagram["steps"]
    ]
    structure = _finite_diagram(
        objects_rows=diagram["objects"], arrows_rows=adapted,
        compositions_rows=diagram["compositions"], arrow_id_field="morphism_id",
        domain_field="domain_id", codomain_field="codomain_id", label="physical diagram",
    )
    left_row = structure["compositions"].get(str(witness["left_composite_id"]))
    right_row = structure["compositions"].get(str(witness["right_composite_id"]))
    if left_row is None or right_row is None or left_row["path_morphism_ids"] != witness["left_path_ids"] or right_row["path_morphism_ids"] != witness["right_path_ids"]:
        _fail("physical witness is not bound to its exact composition rows")
    return validate_negative_witness(
        diagram,
        witness,
        expected_validator_id="finite-physical-diagram-countermodel.v1",
        _dependency_context=_dependency_context,
    )


TASK_SEMANTIC_TRANSLATION_INVALID = "task_semantic_translation_invalid"


def _derive_task_semantic_translation(case: Mapping[str, Any], lens: str) -> dict[str, Any]:
    """Compile declared meaning while preserving the legacy artifact field name."""

    try:
        return compile_task_relation(case, lens)
    except TaskRelationCompilerError as exc:
        _fail(str(exc), reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)


def _task_projection(model: Mapping[str, Any], witness: Mapping[str, Any], translation: Mapping[str, Any]) -> dict[str, Any]:
    try:
        return validate_task_relation_model_binding(translation, model, witness)
    except TaskRelationCompilerError as exc:
        _fail(str(exc), reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)


def _task_translation_receipt(case: Mapping[str, Any], translation: Mapping[str, Any], model: Mapping[str, Any], witness: Mapping[str, Any], replay: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if dict(translation) != _derive_task_semantic_translation(case, str(translation["lens"])):
        _fail("task semantic translation does not independently replay", reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)
    projection = _task_projection(model, witness, translation)
    identity = {
        "model_digest": canonical_digest(model), "witness_digest": canonical_digest(witness),
        **projection,
    }
    core = {
        "validator_id": "meaning-derived-task-relation-replay.v2",
        "replay_kind": "independent_meaning_recompile_plus_finite_isomorphism_normalization",
        "case_digest": canonical_digest(case), "translation_digest": canonical_digest(translation),
        "model_identity": identity, "countermodel_output_digest": canonical_digest(replay),
        "status": "passed",
    }
    return {**core, "receipt_id": stable_identifier("task-semantic-receipt", core)}, identity


def _task_delta_and_handback(translation: Mapping[str, Any], identity: Mapping[str, Any], replay: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        return build_formal_delta_and_handback(translation, identity, replay)
    except TaskRelationCompilerError as exc:
        _fail(str(exc), reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)


def validate_task_derived_artifact(
    case: Mapping[str, Any], artifact: Mapping[str, Any], *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    """Independently replay task meaning; digest rebinding cannot repair a semantic swap."""

    lens = str(artifact.get("lens"))
    expected = _derive_task_semantic_translation(case, lens)
    if artifact.get("semantic_translation") != expected:
        _fail("task, carrier, quantifier, or falsifier translation changed", reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)
    obligation_id = str(case["obligation_id"])
    replay = (
        validate_category_model(artifact["model"], artifact["negative_witness"], {obligation_id}, _dependency_context=_dependency_context)
        if lens == "categorical" else
        validate_hott_model(artifact["model"], artifact["negative_witness"], {obligation_id}, _dependency_context=_dependency_context)
    )
    receipt, identity = _task_translation_receipt(case, expected, artifact["model"], artifact["negative_witness"], replay)
    delta, handback = _task_delta_and_handback(expected, identity, replay)
    required = {
        "formalization_scope": "task_derived_finite_semantic_translation",
        "task_derived_model_identity": identity, "semantic_translation_receipt": receipt,
        "task_derived_formal_delta": delta, "physics_handback": handback,
    }
    if any(artifact.get(key) != value for key, value in required.items()):
        _fail("task-derived identity, receipt, delta, or physics handback changed", reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)
    core = {key: copy.deepcopy(value) for key, value in artifact.items() if key != "artifact_digest"}
    if artifact.get("artifact_digest") != canonical_digest(core):
        _fail("task-derived artifact digest is stale", reason_code=TASK_SEMANTIC_TRANSLATION_INVALID)
    return {"status": "valid", "translation_receipt_id": receipt["receipt_id"], "countermodel_result": replay["result"]}


def _forge_case_artifact(
    case: Mapping[str, Any],
    lens: str,
    dependency_context: _FormalDependencyRunContext,
    *,
    presentation_id: str | None = None,
) -> dict[str, Any]:
    dependency_authority = dependency_context.snapshot()
    translation = _derive_task_semantic_translation(case, lens) if "task_semantics" in case else None
    if presentation_id is not None and (not isinstance(presentation_id, str) or not presentation_id.strip()):
        _fail("presentation_id must be a nonempty string")
    prefix = (
        f"runtime.presentation.{lens}.{canonical_digest(presentation_id).removeprefix('sha256:')[:24]}"
        if translation and presentation_id is not None
        else translation["formal_projection"]["semantic_prefix"]
        if translation
        else f"runtime.{lens}.{case['case_id']}"
    )
    relation_binding = build_task_relation_model_binding(translation) if translation else None
    obligation_id = str(case["obligation_id"])
    if lens == "categorical":
        model, witness = build_category_model_and_witness(
            prefix, obligation_id, _dependency_context=dependency_context,
            _task_relation_binding=relation_binding,
        )
        replay = validate_category_model(
            model,
            witness,
            {obligation_id},
            _dependency_context=dependency_context,
        )
        skill_id = "categorical-concept-forger"
    elif lens == "hott":
        model, witness = build_hott_model_and_witness(
            prefix, obligation_id, _dependency_context=dependency_context,
            _task_relation_binding=relation_binding,
        )
        replay = validate_hott_model(
            model,
            witness,
            {obligation_id},
            _dependency_context=dependency_context,
        )
        skill_id = "hott-equivalence-coherence-forger"
    else:
        _fail(f"unknown formal forger lens {lens}")
    artifact: dict[str, Any] = {
        "skill_id": skill_id,
        "skill_version": "4.0.0-task-derived" if translation else "3.0.0-generic-internal",
        "lens": lens,
        "case_id": case["case_id"], "target_id": case["target_id"],
        "case_digest": canonical_digest(case), "obligation_id": obligation_id,
        "model": model, "negative_witness": witness,
        "countermodel_output_digest": canonical_digest(replay),
        "target_preserved": True, "derived_consequence": True,
        "correction_test_precommitted": True,
        "authority_boundary": (
            "Task-derived finite translation and local burden handback only; no physical, continuum, theorem, or value authority."
            if translation else
            "Generic internal finite-structure plumbing only; no task-semantic or physics-decision authority."
        ),
        "dependency_authority_digest": dependency_authority["content_digest"],
    }
    if translation:
        receipt, identity = _task_translation_receipt(case, translation, model, witness, replay)
        delta, handback = _task_delta_and_handback(translation, identity, replay)
        artifact.update({
            "formalization_scope": "task_derived_finite_semantic_translation",
            "semantic_translation": translation,
            "task_derived_model_identity": identity,
            "semantic_translation_receipt": receipt,
            "task_derived_formal_delta": delta,
            "physics_handback": handback,
        })
    artifact["artifact_digest"] = canonical_digest(artifact)
    if translation:
        validate_task_derived_artifact(case, artifact, _dependency_context=dependency_context)
    return artifact


def forge_case_artifact(
    case: Mapping[str, Any], lens: str, *, presentation_id: str | None = None
) -> dict[str, Any]:
    """Run one forger; an optional presentation label cannot change meaning."""

    return _forge_case_artifact(
        case,
        lens,
        _build_formal_dependency_run_context(),
        presentation_id=presentation_id,
    )


def _negative_controls() -> list[dict[str, Any]]:
    empty = {field: [] for field in (
        "typed_obligations", "witness_checks", "consequences", "unification_links", "correction_tests"
    )}
    return [
        {"control_id": "decorative-keywords", "control_kind": "decorative", "candidate": {"theory_delta": {"evaluation_evidence": copy.deepcopy(empty), "surface_form": "category functor equivalence coherence universal transport"}}, "expected_zero": True},
        {"control_id": "target-restatement", "control_kind": "restatement", "candidate": {"theory_delta": {"evaluation_evidence": copy.deepcopy(empty), "surface_form": "The frozen target is repeated without a new dependency."}}, "expected_zero": True},
        {"control_id": "unsigned-sham-witness", "control_kind": "sham", "candidate": {"theory_delta": {"evaluation_evidence": {**copy.deepcopy(empty), "witness_checks": [{"certificate_bound": False}]}, "surface_form": "A diagram is asserted but no registry replay succeeds."}}, "expected_zero": True},
    ]


def run_condition_forger(
    arm: str,
    cases: Sequence[Mapping[str, Any]],
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    """Execute one condition under an outer-boundary dependency authority."""

    if _dependency_context is None:
        _dependency_context = _build_formal_dependency_run_context()
    dependency_authority = _bound_dependency_authority(_dependency_context)
    dependency_authority_digest = dependency_authority["content_digest"]
    frozen_cases = [copy.deepcopy(dict(case)) for case in cases]
    artifacts: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    if arm in {"categorical", "combined"}:
        selected = [case for case in frozen_cases if case["preferred_lens"] == "categorical"]
        artifacts.extend(
            _forge_case_artifact(case, "categorical", _dependency_context)
            for case in selected
        )
        bindings.append({"skill_id": "categorical-concept-forger", "version": "4.0.0", "executable_digest": callable_digest(forge_case_artifact), "dependency_authority_digest": dependency_authority_digest})
    if arm in {"hott", "combined"}:
        selected = [case for case in frozen_cases if case["preferred_lens"] == "hott"]
        artifacts.extend(
            _forge_case_artifact(case, "hott", _dependency_context)
            for case in selected
        )
        bindings.append({"skill_id": "hott-equivalence-coherence-forger", "version": "4.0.0", "executable_digest": callable_digest(forge_case_artifact), "dependency_authority_digest": dependency_authority_digest})
    evidence = {
        "typed_obligations": [
            {"evidence_id": f"obligation.{row['case_id']}", "localized": True, "artifact_digest": row["artifact_digest"]}
            for row in artifacts
        ],
        "witness_checks": [
            {"evidence_id": f"witness.{row['case_id']}", "certificate_bound": True, "artifact_digest": row["artifact_digest"]}
            for row in artifacts
        ],
        "consequences": [
            {"evidence_id": f"consequence.{row['case_id']}", "derived_from_obligation": True, "artifact_digest": row["artifact_digest"]}
            for row in artifacts
        ],
        "unification_links": [
            {"evidence_id": f"unification.{left['case_id']}.{right['case_id']}", "preserves_difference": True,
             "left_artifact_digest": left["artifact_digest"], "right_artifact_digest": right["artifact_digest"]}
            for left, right in combinations(artifacts, 2)
        ],
        "correction_tests": [
            {"evidence_id": f"correction.{row['case_id']}", "discriminating": True, "artifact_digest": row["artifact_digest"]}
            for row in artifacts
        ],
    }
    if arm == "incumbent":
        bindings.append({"skill_id": "reflective-theory-synthesizer", "version": "control-v1", "executable_digest": canonical_digest("incumbent-restatement-control-v1"), "dependency_authority_digest": dependency_authority_digest})
    if arm == "no_abstraction":
        bindings.append({"skill_id": "reflective-conceptual-discovery", "version": "control-v1", "executable_digest": canonical_digest("no-abstraction-control-v1"), "dependency_authority_digest": dependency_authority_digest})
    result: dict[str, Any] = {
        "arm": arm, "case_suite_digest": canonical_digest(frozen_cases),
        "case_ids": [case["case_id"] for case in frozen_cases],
        "forger_bindings": bindings, "artifacts": artifacts,
        "evaluation_evidence": evidence, "negative_controls": _negative_controls(),
        "authority_class": "internal_protocol_calibration",
        "conceptual_value_authorized": False, "physics_value_authorized": False,
        "dependency_authority": dependency_authority,
    }
    result["result_digest"] = canonical_digest(result)
    return result


def validate_condition_forger_result(
    result: Mapping[str, Any],
    arm: str,
    cases: Sequence[Mapping[str, Any]],
    *,
    _dependency_context: _FormalDependencyRunContext | None = None,
) -> dict[str, Any]:
    if _dependency_context is None:
        _dependency_context = _validate_formal_dependency_run_context(
            result["dependency_authority"]
        )
    else:
        dependency_authority = _bound_dependency_authority(_dependency_context)
        if result["dependency_authority"] != dependency_authority:
            _fail("condition output changed the run-boundary dependency authority")
    expected = run_condition_forger(
        arm, cases, _dependency_context=_dependency_context
    )
    if dict(result) != expected:
        _fail("sealed condition output is not an exact replay of the registered forger")
    return expected


__all__ = [
    "FormalReasoningError", "WITNESS_VALIDATOR_REGISTRY", "build_category_model_and_witness",
    "build_hott_model_and_witness", "build_physical_diagram_and_witness", "callable_digest",
    "forge_case_artifact", "run_condition_forger", "validate_category_model",
    "validate_condition_forger_result", "validate_hott_model", "validate_negative_witness",
    "validate_physical_diagram", "validate_task_derived_artifact",
]
