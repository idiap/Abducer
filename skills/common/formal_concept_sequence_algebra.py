# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Bounded exact sequence algebra for finite conceptual transformations.

The seven constructors in :mod:`formal_concept_transformations` are partial:
their witnesses are meaningful only on cores for which every cited primitive,
relation, inhabitant, and protected observable remains available.  This module
composes exactly two such transformations by actually applying them in both
orders.  It never substitutes a union of independent common-ancestor deltas
for sequential composition.

Each ordered path replays its first delta, validates the intermediate core,
re-applies the residual plan to that exact core, and replays the residual
delta.  The two completed paths form the critical pair.  Exact equality is
checked first; otherwise a bounded canonical graph form accepts only harmless
internal identifier relabelling while preserving the target, obligation,
carrier, regime, quantifiers, statements, relation actions, protected values,
inhabitant boundaries, and burden semantics.  If the exact permutation search
would exceed its declared ceiling, the result is typed ``ceiling_unavailable``
rather than guessed.

Valid non-isomorphic order results are retained as productive plural
candidates.  Protected-observable erasure and free-completion/assumption-away
paths are always quarantined.  Handback content is derived only from replayed
transformation witnesses and their burden, correction, and falsifier fields.
Truth, conceptual merit, physics, theorem, continuum, proof, investment, and
experiment-selection authority remain unavailable.
"""

from __future__ import annotations

import copy
import itertools
import math
from collections import defaultdict
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_identifier,
    validate_instance,
)
from skills.common.formal_concept_transformations import (
    CATEGORY_RELATION_KINDS,
    HOTT_RELATION_KINDS,
    FormalConceptTransformationError,
    construct_categorical_transformation,
    construct_hott_transformation,
    validate_conceptual_core,
    validate_semantic_delta,
)


SCHEMA = "formal_concept_sequence_algebra_v1.schema.json"
CONDITIONED_SCHEMA = "formal_conditioned_concept_sequence_v1.schema.json"
SCHEMA_VERSION = "1.0.0"
CANONICALIZATION_VERSION = "bounded-conceptual-core-isomorphism.v1"
DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS = 4096
MAX_ISOMORPHISM_PERMUTATIONS = 65536

FORMAL_CONCEPT_SEQUENCE_INVALID = "formal_concept_sequence_invalid"
FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID = (
    "formal_concept_sequence_replay_invalid"
)
FORMAL_CONCEPT_ISOMORPHISM_INVALID = (
    "formal_concept_isomorphism_invalid"
)

_PLAN_KEYS = {
    "transformation_id",
    "relation_hypothesis",
    "witness",
    "consequence_contract",
}
_COLLECTION_IDS = {
    "primitives": "primitive_id",
    "relations": "relation_id",
    "observables": "observable_id",
    "inhabitants": "inhabitant_id",
    "burdens": "burden_id",
}
_PUBLIC_NODE_KINDS = {
    "primitive",
    "member",
    "relation",
    "observable",
    "inhabitant",
    "burden",
    "evidence",
}
_AUTHORITY_BOUNDARY = {
    "finite_local_replay_only": True,
    "truth_authority": None,
    "conceptual_merit_authority": None,
    "physics_authority": None,
    "theorem_authority": None,
    "physical_equivalence_authorized": False,
    "continuum_authorized": False,
    "proof_authorized": False,
    "investment_authorized": False,
    "experiment_selection_authorized": False,
}


class FormalConceptSequenceError(ValueError):
    """Typed fail-closed error for sequence construction or exact replay."""

    def __init__(self, message: str, *, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: {message}")


def _fail(message: str, reason_code: str) -> None:
    raise FormalConceptSequenceError(message, reason_code=reason_code)


def _seal(raw: Mapping[str, Any], digest_field: str) -> dict[str, Any]:
    payload = copy.deepcopy(dict(raw))
    payload.pop(digest_field, None)
    payload[digest_field] = canonical_digest(payload)
    return payload


def _strict(
    raw: Any,
    expected: set[str],
    label: str,
    *,
    reason_code: str = FORMAL_CONCEPT_SEQUENCE_INVALID,
) -> Mapping[str, Any]:
    if not isinstance(raw, Mapping):
        _fail(f"{label} must be a mapping", reason_code)
    keys = set(raw)
    if keys != expected:
        _fail(
            f"{label} keys differ; missing={sorted(expected - keys)}, "
            f"extra={sorted(keys - expected)}",
            reason_code,
        )
    return raw


def _identifier(value: Any, label: str) -> str:
    try:
        return validate_identifier(value, label)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_SEQUENCE_INVALID)
    raise AssertionError("unreachable")


def _validate_ceiling(value: Any) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < 1
        or value > MAX_ISOMORPHISM_PERMUTATIONS
    ):
        _fail(
            "max_isomorphism_permutations must be an integer in "
            f"[1, {MAX_ISOMORPHISM_PERMUTATIONS}]",
            FORMAL_CONCEPT_ISOMORPHISM_INVALID,
        )
    return value


def _validate_plan(raw: Mapping[str, Any]) -> dict[str, Any]:
    plan = copy.deepcopy(
        dict(_strict(raw, _PLAN_KEYS, "transformation plan"))
    )
    _identifier(plan["transformation_id"], "transformation_id")
    relation = plan["relation_hypothesis"]
    if not isinstance(relation, Mapping):
        _fail(
            "transformation relation_hypothesis must be a mapping",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )
    kind = relation.get("relation_kind")
    if kind not in CATEGORY_RELATION_KINDS + HOTT_RELATION_KINDS:
        _fail(
            "transformation plan has an unsupported relation kind",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )
    if not isinstance(plan["witness"], Mapping):
        _fail(
            "transformation witness must be a mapping",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )
    if not isinstance(plan["consequence_contract"], Mapping):
        _fail(
            "transformation consequence_contract must be a mapping",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )
    return plan


def _constructor_for(plan: Mapping[str, Any]):
    kind = plan["relation_hypothesis"]["relation_kind"]
    if kind in CATEGORY_RELATION_KINDS:
        return construct_categorical_transformation
    if kind in HOTT_RELATION_KINDS:
        return construct_hott_transformation
    _fail(
        "transformation plan has an unsupported relation kind",
        FORMAL_CONCEPT_SEQUENCE_INVALID,
    )
    raise AssertionError("unreachable")


def _unavailable_replay(
    input_core_digest: str,
    *,
    status: str,
) -> dict[str, Any]:
    return _seal(
        {
            "status": status,
            "input_core_digest": input_core_digest,
            "delta_id": None,
            "delta_digest": None,
            "before_core_digest": None,
            "after_core_digest": None,
            "exact_input_boundary": False,
            "semantic_delta_replayed": False,
            "after_core_validated": False,
        },
        "replay_digest",
    )


def _replay_delta(
    input_core: Mapping[str, Any],
    delta: Mapping[str, Any],
) -> dict[str, Any]:
    replay = validate_semantic_delta(delta)
    validated_after = validate_conceptual_core(
        delta["after_core"], allow_free=True
    )
    exact_boundary = (
        canonical_json(input_core) == canonical_json(delta["before_core"])
    )
    if not exact_boundary:
        _fail(
            "a sequential delta does not start at its exact input core",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    if validated_after["content_digest"] != delta["after_core"][
        "content_digest"
    ]:
        _fail(
            "a sequential delta returned a stale intermediate core",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    return _seal(
        {
            "status": "valid",
            "input_core_digest": input_core["content_digest"],
            "delta_id": replay["delta_id"],
            "delta_digest": replay["content_digest"],
            "before_core_digest": delta["before_core"]["content_digest"],
            "after_core_digest": validated_after["content_digest"],
            "exact_input_boundary": True,
            "semantic_delta_replayed": True,
            "after_core_validated": True,
        },
        "replay_digest",
    )


def _apply_plan(
    input_core: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    constructor = _constructor_for(plan)
    try:
        delta = constructor(
            input_core,
            plan["relation_hypothesis"],
            plan["witness"],
            plan["consequence_contract"],
        )
        replay = _replay_delta(input_core, delta)
    except FormalConceptTransformationError as exc:
        return {
            "status": "unavailable",
            "reason_code": exc.reason_code,
            "delta": None,
            "replay": _unavailable_replay(
                input_core["content_digest"], status="unavailable"
            ),
        }
    return {
        "status": "applied",
        "reason_code": None,
        "delta": delta,
        "replay": replay,
    }


def _application_summary(
    plan: Mapping[str, Any],
    application: Mapping[str, Any],
) -> dict[str, Any]:
    delta = application["delta"]
    summary = {
        "transformation_id": plan["transformation_id"],
        "status": application["status"],
        "reason_code": application["reason_code"],
        "delta_id": None if delta is None else delta["delta_id"],
        "delta_digest": None if delta is None else delta["content_digest"],
        "after_status": (
            None
            if delta is None
            else delta["obstruction_transition"]["after_status"]
        ),
        "replay_digest": application["replay"]["replay_digest"],
    }
    return _seal(summary, "application_digest")


def _quarantine_reason(delta: Mapping[str, Any]) -> str | None:
    if delta["observable_preservation"]["protected_erasure_detected"]:
        return "protected_observable_erasure"
    if (
        delta["construction"]["construction_origin"]
        == "free_completion_counterfactual"
        or delta["obstruction_transition"]["after_status"]
        == "counterfactual_only"
    ):
        return "free_completion_has_no_inhabitation_authority"
    return None


def _dedupe_text(values: Sequence[Any]) -> list[str]:
    result: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            _fail(
                "witness-derived handback text is invalid",
                FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
            )
        if value not in result:
            result.append(value)
    return result


def _witness_differences(
    deltas: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    burdens = _dedupe_text(
        [row["semantic_delta"]["changed_burden"] for row in deltas]
    )
    corrections = _dedupe_text(
        [row["semantic_delta"]["correction"] for row in deltas]
    )
    falsifiers = _dedupe_text(
        [row["semantic_delta"]["falsifier"] for row in deltas]
    )
    return _seal(
        {
            "delta_ids": [row["delta_id"] for row in deltas],
            "witness_digests": [
                row["construction"]["witness_digest"] for row in deltas
            ],
            "burden_statements": burdens,
            "corrections": corrections,
            "falsifiers": falsifiers,
            "loss_ledger_digests": [
                canonical_digest(row["semantic_delta"]["loss_ledger"])
                for row in deltas
            ],
        },
        "difference_digest",
    )


def _critical_pair(
    base_core: Mapping[str, Any],
    first_plan: Mapping[str, Any],
    second_plan: Mapping[str, Any],
    first_application: Mapping[str, Any],
) -> dict[str, Any]:
    order = [
        first_plan["transformation_id"],
        second_plan["transformation_id"],
    ]
    pair_id = stable_identifier(
        "formal-concept-critical-pair-order",
        base_core["content_digest"],
        order,
    )
    first_delta = first_application["delta"]
    if first_delta is None:
        residual = _seal(
            {
                "residual_id": stable_identifier(
                    "formal-concept-residual", pair_id, "not-coenabled"
                ),
                "transformation_id": second_plan["transformation_id"],
                "against_transformation_id": first_plan[
                    "transformation_id"
                ],
                "source_plan_digest": canonical_digest(second_plan),
                "input_core_digest": base_core["content_digest"],
                "status": "not_coenabled",
                "reason_code": "base_transformation_unavailable",
                "delta": None,
                "replay": _unavailable_replay(
                    base_core["content_digest"], status="not_coenabled"
                ),
            },
            "residual_digest",
        )
        return _seal(
            {
                "critical_pair_id": pair_id,
                "order": order,
                "status": "not_coenabled",
                "reason_code": first_application["reason_code"],
                "first_delta": None,
                "intermediate_replay": first_application["replay"],
                "residual": residual,
                "final_core": None,
                "final_core_digest": None,
                "protected_distinctions_preserved": False,
                "free_completion_detected": False,
                "witness_differences": _witness_differences([]),
            },
            "critical_pair_digest",
        )

    first_quarantine = _quarantine_reason(first_delta)
    if first_quarantine is not None:
        status = (
            "quarantined_protected_erasure"
            if first_quarantine == "protected_observable_erasure"
            else "quarantined_free_completion"
        )
        residual = _seal(
            {
                "residual_id": stable_identifier(
                    "formal-concept-residual", pair_id, status
                ),
                "transformation_id": second_plan["transformation_id"],
                "against_transformation_id": first_plan[
                    "transformation_id"
                ],
                "source_plan_digest": canonical_digest(second_plan),
                "input_core_digest": first_delta["after_core"][
                    "content_digest"
                ],
                "status": "blocked_by_quarantine",
                "reason_code": first_quarantine,
                "delta": None,
                "replay": _unavailable_replay(
                    first_delta["after_core"]["content_digest"],
                    status="blocked_by_quarantine",
                ),
            },
            "residual_digest",
        )
        return _seal(
            {
                "critical_pair_id": pair_id,
                "order": order,
                "status": status,
                "reason_code": first_quarantine,
                "first_delta": copy.deepcopy(first_delta),
                "intermediate_replay": first_application["replay"],
                "residual": residual,
                "final_core": None,
                "final_core_digest": None,
                "protected_distinctions_preserved": False,
                "free_completion_detected": (
                    status == "quarantined_free_completion"
                ),
                "witness_differences": _witness_differences(
                    [first_delta]
                ),
            },
            "critical_pair_digest",
        )

    intermediate = first_delta["after_core"]
    residual_application = _apply_plan(intermediate, second_plan)
    second_delta = residual_application["delta"]
    residual = _seal(
        {
            "residual_id": stable_identifier(
                "formal-concept-residual",
                pair_id,
                second_plan["transformation_id"],
                intermediate["content_digest"],
            ),
            "transformation_id": second_plan["transformation_id"],
            "against_transformation_id": first_plan["transformation_id"],
            "source_plan_digest": canonical_digest(second_plan),
            "input_core_digest": intermediate["content_digest"],
            "status": residual_application["status"],
            "reason_code": residual_application["reason_code"],
            "delta": copy.deepcopy(second_delta),
            "replay": residual_application["replay"],
        },
        "residual_digest",
    )
    if second_delta is None:
        return _seal(
            {
                "critical_pair_id": pair_id,
                "order": order,
                "status": "partial_failure",
                "reason_code": residual_application["reason_code"],
                "first_delta": copy.deepcopy(first_delta),
                "intermediate_replay": first_application["replay"],
                "residual": residual,
                "final_core": None,
                "final_core_digest": None,
                "protected_distinctions_preserved": True,
                "free_completion_detected": False,
                "witness_differences": _witness_differences(
                    [first_delta]
                ),
            },
            "critical_pair_digest",
        )

    second_quarantine = _quarantine_reason(second_delta)
    if second_quarantine is not None:
        status = (
            "quarantined_protected_erasure"
            if second_quarantine == "protected_observable_erasure"
            else "quarantined_free_completion"
        )
        return _seal(
            {
                "critical_pair_id": pair_id,
                "order": order,
                "status": status,
                "reason_code": second_quarantine,
                "first_delta": copy.deepcopy(first_delta),
                "intermediate_replay": first_application["replay"],
                "residual": residual,
                "final_core": copy.deepcopy(second_delta["after_core"]),
                "final_core_digest": second_delta["after_core"][
                    "content_digest"
                ],
                "protected_distinctions_preserved": (
                    second_quarantine != "protected_observable_erasure"
                ),
                "free_completion_detected": (
                    status == "quarantined_free_completion"
                ),
                "witness_differences": _witness_differences(
                    [first_delta, second_delta]
                ),
            },
            "critical_pair_digest",
        )

    return _seal(
        {
            "critical_pair_id": pair_id,
            "order": order,
            "status": "completed",
            "reason_code": None,
            "first_delta": copy.deepcopy(first_delta),
            "intermediate_replay": first_application["replay"],
            "residual": residual,
            "final_core": copy.deepcopy(second_delta["after_core"]),
            "final_core_digest": second_delta["after_core"][
                "content_digest"
            ],
            "protected_distinctions_preserved": True,
            "free_completion_detected": False,
            "witness_differences": _witness_differences(
                [first_delta, second_delta]
            ),
        },
        "critical_pair_digest",
    )


def _strict_core_projection(core: Mapping[str, Any]) -> dict[str, Any]:
    """Ignore only core sealing and harmless collection presentation order."""

    payload = copy.deepcopy(dict(core))
    payload.pop("core_id", None)
    payload.pop("content_digest", None)
    for collection, id_field in _COLLECTION_IDS.items():
        rows = payload[collection]
        if collection == "primitives":
            for row in rows:
                row["member_ids"] = sorted(row["member_ids"])
        elif collection == "relations":
            for row in rows:
                row["action"] = sorted(
                    row["action"], key=lambda item: item["source_member_id"]
                )
        elif collection == "observables":
            for row in rows:
                row["evaluations"] = sorted(
                    row["evaluations"], key=lambda item: item["member_id"]
                )
        payload[collection] = sorted(
            rows, key=lambda row: row[id_field]
        )
    return payload


def _semantic_root(core: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": core["schema_version"],
        "target_id": core["target_id"],
        "obligation_id": core["obligation_id"],
        "physical_carrier": core["physical_carrier"],
        "regime": core["regime"],
        "quantifiers": copy.deepcopy(core["quantifiers"]),
    }


Node = tuple[str, str]
Edge = tuple[Node, str, Node]


def _conceptual_graph(
    core: Mapping[str, Any],
) -> tuple[dict[Node, dict[str, Any]], list[Edge]]:
    nodes: dict[Node, dict[str, Any]] = {}
    edges: list[Edge] = []

    def add_node(kind: str, identifier: str, **attributes: Any) -> Node:
        key = (kind, identifier)
        row = {"kind": kind, **copy.deepcopy(attributes)}
        existing = nodes.get(key)
        if existing is not None and canonical_json(existing) != canonical_json(
            row
        ):
            _fail(
                "conceptual graph contains a typed identifier collision",
                FORMAL_CONCEPT_ISOMORPHISM_INVALID,
            )
        nodes[key] = row
        return key

    for primitive in core["primitives"]:
        primitive_node = add_node(
            "primitive",
            primitive["primitive_id"],
            statement=primitive["statement"],
        )
        for member_id in primitive["member_ids"]:
            member_node = add_node("member", member_id)
            edges.append((primitive_node, "has_member", member_node))

    for relation in core["relations"]:
        relation_node = add_node(
            "relation",
            relation["relation_id"],
            relation_type=relation["relation_type"],
            statement=relation["statement"],
        )
        edges.extend(
            (
                (
                    relation_node,
                    "source_primitive",
                    ("primitive", relation["source_primitive_id"]),
                ),
                (
                    relation_node,
                    "target_primitive",
                    ("primitive", relation["target_primitive_id"]),
                ),
            )
        )
        for index, action in enumerate(relation["action"]):
            action_node = add_node(
                "action",
                f"{relation['relation_id']}:{index}",
            )
            edges.extend(
                (
                    (relation_node, "has_action", action_node),
                    (
                        action_node,
                        "source_member",
                        ("member", action["source_member_id"]),
                    ),
                    (
                        action_node,
                        "target_member",
                        ("member", action["target_member_id"]),
                    ),
                )
            )

    for observable in core["observables"]:
        observable_node = add_node(
            "observable",
            observable["observable_id"],
            statement=observable["statement"],
            protected=observable["protected"],
        )
        edges.append(
            (
                observable_node,
                "carrier_primitive",
                ("primitive", observable["carrier_primitive_id"]),
            )
        )
        for index, evaluation in enumerate(observable["evaluations"]):
            evaluation_node = add_node(
                "evaluation",
                f"{observable['observable_id']}:{index}",
                value=evaluation["value"],
            )
            edges.extend(
                (
                    (observable_node, "has_evaluation", evaluation_node),
                    (
                        evaluation_node,
                        "evaluated_member",
                        ("member", evaluation["member_id"]),
                    ),
                )
            )

    for inhabitant in core["inhabitants"]:
        inhabitant_node = add_node(
            "inhabitant",
            inhabitant["inhabitant_id"],
            level=inhabitant["level"],
            derivation_rule=inhabitant["derivation_rule"],
        )
        boundary_kind = (
            "member" if inhabitant["level"] == 1 else "inhabitant"
        )
        edges.extend(
            (
                (
                    inhabitant_node,
                    "ambient_primitive",
                    ("primitive", inhabitant["ambient_primitive_id"]),
                ),
                (
                    inhabitant_node,
                    "source_boundary",
                    (
                        boundary_kind,
                        inhabitant["source_boundary_id"],
                    ),
                ),
                (
                    inhabitant_node,
                    "target_boundary",
                    (
                        boundary_kind,
                        inhabitant["target_boundary_id"],
                    ),
                ),
            )
        )
        for index, premise_id in enumerate(
            inhabitant["premise_inhabitant_ids"]
        ):
            edges.append(
                (
                    inhabitant_node,
                    f"premise:{index}",
                    ("inhabitant", premise_id),
                )
            )
        for index, evidence_ref in enumerate(inhabitant["evidence_refs"]):
            evidence_node = add_node("evidence", evidence_ref)
            edges.append(
                (
                    inhabitant_node,
                    f"evidence:{index}",
                    evidence_node,
                )
            )

    for burden in core["burdens"]:
        add_node(
            "burden",
            burden["burden_id"],
            statement=burden["statement"],
            status=burden["status"],
        )

    for source, _, target in edges:
        if source not in nodes or target not in nodes:
            _fail(
                "conceptual graph edge leaves the validated core",
                FORMAL_CONCEPT_ISOMORPHISM_INVALID,
            )
    return nodes, edges


def _node_key(node: Node) -> bytes:
    return canonical_json([node[0], node[1]])


def _refined_colors(
    nodes: Mapping[Node, Mapping[str, Any]],
    edges: Sequence[Edge],
) -> dict[Node, str]:
    outgoing: dict[Node, list[tuple[str, Node]]] = defaultdict(list)
    incoming: dict[Node, list[tuple[str, Node]]] = defaultdict(list)
    for source, label, target in edges:
        outgoing[source].append((label, target))
        incoming[target].append((label, source))

    base_signatures = {
        node: canonical_json(attributes)
        for node, attributes in nodes.items()
    }

    def assign(signatures: Mapping[Node, bytes]) -> dict[Node, str]:
        vocabulary = {
            signature: f"c{index}"
            for index, signature in enumerate(
                sorted(set(signatures.values()))
            )
        }
        return {
            node: vocabulary[signature]
            for node, signature in signatures.items()
        }

    colors = assign(base_signatures)
    for _ in range(len(nodes)):
        signatures = {}
        for node in nodes:
            signatures[node] = canonical_json(
                {
                    "attributes": nodes[node],
                    "self": colors[node],
                    "outgoing": sorted(
                        [
                            [label, colors[target]]
                            for label, target in outgoing[node]
                        ],
                        key=canonical_json,
                    ),
                    "incoming": sorted(
                        [
                            [label, colors[source]]
                            for label, source in incoming[node]
                        ],
                        key=canonical_json,
                    ),
                }
            )
        new_colors = assign(signatures)
        old_partition = {
            tuple(sorted(group, key=_node_key))
            for group in _groups_by_color(colors).values()
        }
        new_partition = {
            tuple(sorted(group, key=_node_key))
            for group in _groups_by_color(new_colors).values()
        }
        colors = new_colors
        if old_partition == new_partition:
            break
    return colors


def _groups_by_color(
    colors: Mapping[Node, str],
) -> dict[str, list[Node]]:
    groups: dict[str, list[Node]] = defaultdict(list)
    for node, color in colors.items():
        groups[color].append(node)
    return dict(groups)


def _canonical_graph_form(
    root: Mapping[str, Any],
    nodes: Mapping[Node, Mapping[str, Any]],
    edges: Sequence[Edge],
    *,
    max_permutations: int,
) -> dict[str, Any]:
    colors = _refined_colors(nodes, edges)
    groups = _groups_by_color(colors)
    ordered_groups = [
        sorted(groups[color], key=_node_key) for color in sorted(groups)
    ]
    candidate_count = math.prod(
        math.factorial(len(group)) for group in ordered_groups
    )
    if candidate_count > max_permutations:
        return {
            "status": "ceiling_unavailable",
            "candidate_permutations": candidate_count,
            "checked_permutations": 0,
            "canonical_digest": None,
            "label_map": None,
        }

    best_code: bytes | None = None
    best_labels: dict[Node, str] | None = None
    checked = 0
    permutation_groups = [
        itertools.permutations(group) for group in ordered_groups
    ]
    for ordered_nodes_by_group in itertools.product(
        *permutation_groups
    ):
        labels: dict[Node, str] = {}
        ordinal = 0
        for ordered_nodes in ordered_nodes_by_group:
            for node in ordered_nodes:
                labels[node] = f"node.{ordinal:06d}"
                ordinal += 1
        code = canonical_json(
            {
                "root": root,
                "nodes": [
                    {
                        "canonical_id": labels[node],
                        "attributes": nodes[node],
                    }
                    for node in sorted(nodes, key=lambda item: labels[item])
                ],
                "edges": sorted(
                    [
                        [labels[source], label, labels[target]]
                        for source, label, target in edges
                    ],
                    key=canonical_json,
                ),
            }
        )
        checked += 1
        if best_code is None or code < best_code:
            best_code = code
            best_labels = labels
    if best_code is None or best_labels is None:
        _fail(
            "conceptual graph canonicalization produced no candidate",
            FORMAL_CONCEPT_ISOMORPHISM_INVALID,
        )
    return {
        "status": "available",
        "candidate_permutations": candidate_count,
        "checked_permutations": checked,
        "canonical_digest": bytes_digest(best_code),
        "label_map": best_labels,
    }


def _comparison_record(
    *,
    status: str,
    reason_code: str,
    left_digest: str | None,
    right_digest: str | None,
    semantic_root_equal: bool | None,
    strict_projection_equal: bool | None,
    max_permutations: int,
    left_candidate_permutations: int,
    right_candidate_permutations: int,
    left_checked_permutations: int,
    right_checked_permutations: int,
    canonical_core_digest: str | None,
    identifier_mapping: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return _seal(
        {
            "comparison_status": status,
            "reason_code": reason_code,
            "left_core_digest": left_digest,
            "right_core_digest": right_digest,
            "semantic_root_equal": semantic_root_equal,
            "strict_projection_equal": strict_projection_equal,
            "canonicalization_version": CANONICALIZATION_VERSION,
            "max_permutations": max_permutations,
            "left_candidate_permutations": left_candidate_permutations,
            "right_candidate_permutations": right_candidate_permutations,
            "left_checked_permutations": left_checked_permutations,
            "right_checked_permutations": right_checked_permutations,
            "canonical_core_digest": canonical_core_digest,
            "identifier_mapping": copy.deepcopy(
                list(identifier_mapping)
            ),
        },
        "comparison_digest",
    )


def unavailable_core_comparison(
    *,
    max_permutations: int,
    reason_code: str,
) -> dict[str, Any]:
    """Return a typed comparison absence without implying non-isomorphism."""

    ceiling = _validate_ceiling(max_permutations)
    return _comparison_record(
        status="not_available",
        reason_code=reason_code,
        left_digest=None,
        right_digest=None,
        semantic_root_equal=None,
        strict_projection_equal=None,
        max_permutations=ceiling,
        left_candidate_permutations=0,
        right_candidate_permutations=0,
        left_checked_permutations=0,
        right_checked_permutations=0,
        canonical_core_digest=None,
        identifier_mapping=[],
    )


def compare_conceptual_cores(
    left_raw: Mapping[str, Any],
    right_raw: Mapping[str, Any],
    *,
    max_permutations: int = DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS,
) -> dict[str, Any]:
    """Compare two validated cores up to bounded exact internal relabelling.

    ``ceiling_unavailable`` is epistemically distinct from
    ``not_isomorphic``.  It records that an exact search was deliberately not
    attempted beyond the caller-visible finite ceiling.
    """

    ceiling = _validate_ceiling(max_permutations)
    left = validate_conceptual_core(left_raw, allow_free=True)
    right = validate_conceptual_core(right_raw, allow_free=True)
    left_digest = left["content_digest"]
    right_digest = right["content_digest"]
    roots_equal = canonical_json(_semantic_root(left)) == canonical_json(
        _semantic_root(right)
    )
    if not roots_equal:
        return _comparison_record(
            status="not_isomorphic",
            reason_code="semantic_root_mismatch",
            left_digest=left_digest,
            right_digest=right_digest,
            semantic_root_equal=False,
            strict_projection_equal=False,
            max_permutations=ceiling,
            left_candidate_permutations=0,
            right_candidate_permutations=0,
            left_checked_permutations=0,
            right_checked_permutations=0,
            canonical_core_digest=None,
            identifier_mapping=[],
        )

    strict_equal = canonical_json(_strict_core_projection(left)) == (
        canonical_json(_strict_core_projection(right))
    )
    if strict_equal:
        return _comparison_record(
            status="strictly_equal",
            reason_code="strict_semantic_identity",
            left_digest=left_digest,
            right_digest=right_digest,
            semantic_root_equal=True,
            strict_projection_equal=True,
            max_permutations=ceiling,
            left_candidate_permutations=1,
            right_candidate_permutations=1,
            left_checked_permutations=1,
            right_checked_permutations=1,
            canonical_core_digest=canonical_digest(
                _strict_core_projection(left)
            ),
            identifier_mapping=[],
        )

    left_nodes, left_edges = _conceptual_graph(left)
    right_nodes, right_edges = _conceptual_graph(right)
    if len(left_nodes) != len(right_nodes) or len(left_edges) != len(
        right_edges
    ):
        return _comparison_record(
            status="not_isomorphic",
            reason_code="typed_graph_cardinality_mismatch",
            left_digest=left_digest,
            right_digest=right_digest,
            semantic_root_equal=True,
            strict_projection_equal=False,
            max_permutations=ceiling,
            left_candidate_permutations=0,
            right_candidate_permutations=0,
            left_checked_permutations=0,
            right_checked_permutations=0,
            canonical_core_digest=None,
            identifier_mapping=[],
        )

    left_form = _canonical_graph_form(
        _semantic_root(left),
        left_nodes,
        left_edges,
        max_permutations=ceiling,
    )
    right_form = _canonical_graph_form(
        _semantic_root(right),
        right_nodes,
        right_edges,
        max_permutations=ceiling,
    )
    if (
        left_form["status"] == "ceiling_unavailable"
        or right_form["status"] == "ceiling_unavailable"
    ):
        return _comparison_record(
            status="ceiling_unavailable",
            reason_code="bounded_exact_isomorphism_ceiling_exceeded",
            left_digest=left_digest,
            right_digest=right_digest,
            semantic_root_equal=True,
            strict_projection_equal=False,
            max_permutations=ceiling,
            left_candidate_permutations=left_form[
                "candidate_permutations"
            ],
            right_candidate_permutations=right_form[
                "candidate_permutations"
            ],
            left_checked_permutations=left_form[
                "checked_permutations"
            ],
            right_checked_permutations=right_form[
                "checked_permutations"
            ],
            canonical_core_digest=None,
            identifier_mapping=[],
        )

    if left_form["canonical_digest"] != right_form["canonical_digest"]:
        return _comparison_record(
            status="not_isomorphic",
            reason_code="canonical_conceptual_structure_differs",
            left_digest=left_digest,
            right_digest=right_digest,
            semantic_root_equal=True,
            strict_projection_equal=False,
            max_permutations=ceiling,
            left_candidate_permutations=left_form[
                "candidate_permutations"
            ],
            right_candidate_permutations=right_form[
                "candidate_permutations"
            ],
            left_checked_permutations=left_form[
                "checked_permutations"
            ],
            right_checked_permutations=right_form[
                "checked_permutations"
            ],
            canonical_core_digest=None,
            identifier_mapping=[],
        )

    right_by_label = {
        label: node for node, label in right_form["label_map"].items()
    }
    identifier_mapping = []
    for left_node, label in sorted(
        left_form["label_map"].items(), key=lambda item: _node_key(item[0])
    ):
        right_node = right_by_label[label]
        if (
            left_node[0] in _PUBLIC_NODE_KINDS
            and right_node[0] == left_node[0]
        ):
            identifier_mapping.append(
                {
                    "identifier_kind": left_node[0],
                    "left_id": left_node[1],
                    "right_id": right_node[1],
                }
            )
    return _comparison_record(
        status="isomorphic",
        reason_code="bounded_exact_internal_relabelling",
        left_digest=left_digest,
        right_digest=right_digest,
        semantic_root_equal=True,
        strict_projection_equal=False,
        max_permutations=ceiling,
        left_candidate_permutations=left_form[
            "candidate_permutations"
        ],
        right_candidate_permutations=right_form[
            "candidate_permutations"
        ],
        left_checked_permutations=left_form[
            "checked_permutations"
        ],
        right_checked_permutations=right_form[
            "checked_permutations"
        ],
        canonical_core_digest=left_form["canonical_digest"],
        identifier_mapping=identifier_mapping,
    )


def _coenabledness(
    plans: Sequence[Mapping[str, Any]],
    applications: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    available = [
        plan["transformation_id"]
        for plan, application in zip(plans, applications, strict=True)
        if application["status"] == "applied"
    ]
    unavailable = [
        {
            "transformation_id": plan["transformation_id"],
            "reason_code": application["reason_code"],
        }
        for plan, application in zip(plans, applications, strict=True)
        if application["status"] != "applied"
    ]
    return _seal(
        {
            "status": (
                "coenabled" if len(available) == 2 else "not_coenabled"
            ),
            "applicable_transformation_ids": available,
            "unavailable_transformations": unavailable,
            "both_defined_on_base": len(available) == 2,
        },
        "coenabledness_digest",
    )


def _candidate_difference(
    left_pair: Mapping[str, Any],
    right_pair: Mapping[str, Any],
) -> dict[str, Any]:
    left = left_pair["witness_differences"]
    right = right_pair["witness_differences"]

    def sides(field: str) -> tuple[list[str], list[str]]:
        left_values = list(left[field])
        right_values = list(right[field])
        return (
            [value for value in left_values if value not in right_values],
            [value for value in right_values if value not in left_values],
        )

    left_burdens, right_burdens = sides("burden_statements")
    left_corrections, right_corrections = sides("corrections")
    left_falsifiers, right_falsifiers = sides("falsifiers")
    return _seal(
        {
            "left_critical_pair_id": left_pair["critical_pair_id"],
            "right_critical_pair_id": right_pair["critical_pair_id"],
            "left_only_burden_statements": left_burdens,
            "right_only_burden_statements": right_burdens,
            "left_only_corrections": left_corrections,
            "right_only_corrections": right_corrections,
            "left_only_falsifiers": left_falsifiers,
            "right_only_falsifiers": right_falsifiers,
        },
        "candidate_difference_digest",
    )


def _protected_value_digest(core: Mapping[str, Any]) -> str:
    rows = [
        {
            "statement": observable["statement"],
            "carrier_statement": next(
                primitive["statement"]
                for primitive in core["primitives"]
                if primitive["primitive_id"]
                == observable["carrier_primitive_id"]
            ),
            "evaluations": sorted(
                [
                    {
                        "member_id": evaluation["member_id"],
                        "value": evaluation["value"],
                    }
                    for evaluation in observable["evaluations"]
                ],
                key=canonical_json,
            ),
        }
        for observable in core["observables"]
        if observable["protected"]
    ]
    return canonical_digest(sorted(rows, key=canonical_json))


def _candidate(
    pairs: Sequence[Mapping[str, Any]],
    *,
    canonical_core_digest: str | None,
) -> dict[str, Any]:
    if not pairs or any(pair["final_core"] is None for pair in pairs):
        _fail(
            "a retained candidate requires completed final cores",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    witness_rows = [pair["witness_differences"] for pair in pairs]
    burdens = _dedupe_text(
        [
            value
            for row in witness_rows
            for value in row["burden_statements"]
        ]
    )
    corrections = _dedupe_text(
        [value for row in witness_rows for value in row["corrections"]]
    )
    falsifiers = _dedupe_text(
        [value for row in witness_rows for value in row["falsifiers"]]
    )
    final_digests = [pair["final_core_digest"] for pair in pairs]
    return _seal(
        {
            "candidate_id": stable_identifier(
                "formal-concept-sequence-candidate",
                [pair["critical_pair_id"] for pair in pairs],
                final_digests,
                canonical_core_digest,
            ),
            "critical_pair_ids": [
                pair["critical_pair_id"] for pair in pairs
            ],
            "orders": [copy.deepcopy(pair["order"]) for pair in pairs],
            "final_core_digests": final_digests,
            "canonical_core_digest": canonical_core_digest,
            "witness_digests": _dedupe_text(
                [
                    value
                    for row in witness_rows
                    for value in row["witness_digests"]
                ]
            ),
            "burden_statements": burdens,
            "corrections": corrections,
            "falsifiers": falsifiers,
            "protected_observable_values_digest": canonical_digest(
                [
                    _protected_value_digest(pair["final_core"])
                    for pair in pairs
                ]
            ),
        },
        "candidate_digest",
    )


def _outcome_and_handback(
    base_core: Mapping[str, Any],
    coenabledness: Mapping[str, Any],
    critical_pairs: Sequence[Mapping[str, Any]],
    comparison: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    statuses = [pair["status"] for pair in critical_pairs]
    completed = [
        pair for pair in critical_pairs if pair["status"] == "completed"
    ]
    if coenabledness["status"] != "coenabled":
        outcome_status = "not_coenabled"
    elif len(completed) == 2:
        outcome_status = {
            "strictly_equal": "strictly_commuting",
            "isomorphic": "isomorphic_commuting",
            "not_isomorphic": "productive_noncommutation",
            "ceiling_unavailable": "ceiling_unavailable",
        }.get(comparison["comparison_status"], "invalid_conflict")
    elif len(completed) == 1:
        outcome_status = "partial_failure"
    elif "quarantined_protected_erasure" in statuses:
        outcome_status = "quarantined_protected_erasure"
    elif "quarantined_free_completion" in statuses:
        outcome_status = "quarantined_free_completion"
    else:
        outcome_status = "invalid_conflict"

    retained_pair_ids = [
        pair["critical_pair_id"] for pair in completed
    ]
    quarantined_pair_ids = [
        pair["critical_pair_id"]
        for pair in critical_pairs
        if pair["status"] != "completed"
    ]
    plural_core_digests = (
        [pair["final_core_digest"] for pair in completed]
        if outcome_status
        in {"productive_noncommutation", "ceiling_unavailable"}
        else []
    )
    outcome = _seal(
        {
            "status": outcome_status,
            "retained_critical_pair_ids": retained_pair_ids,
            "quarantined_critical_pair_ids": quarantined_pair_ids,
            "plural_candidate_core_digests": plural_core_digests,
            "decision_change_authorized": False,
            "physics_value_authorized": False,
            "theorem_authorized": False,
            "investment_authorized": False,
        },
        "outcome_digest",
    )

    candidates: list[dict[str, Any]] = []
    handback_status = "not_available"
    eligible = False
    if outcome_status in {"strictly_commuting", "isomorphic_commuting"}:
        candidates = [
            _candidate(
                completed,
                canonical_core_digest=comparison[
                    "canonical_core_digest"
                ],
            )
        ]
        handback_status = "single_commuting_candidate"
        eligible = True
    elif outcome_status == "productive_noncommutation":
        candidates = [
            _candidate(
                [pair],
                canonical_core_digest=None,
            )
            for pair in completed
        ]
        handback_status = "plural_productive_candidates"
        eligible = True
    elif outcome_status == "ceiling_unavailable":
        candidates = [
            _candidate([pair], canonical_core_digest=None)
            for pair in completed
        ]
        handback_status = "comparison_ceiling_unavailable"
    elif outcome_status == "partial_failure":
        candidates = [
            _candidate([completed[0]], canonical_core_digest=None)
        ]
        handback_status = "partial_sequence_quarantined"
    elif outcome_status in {
        "quarantined_protected_erasure",
        "quarantined_free_completion",
        "invalid_conflict",
    }:
        handback_status = "quarantined"

    handback = _seal(
        {
            "handback_status": handback_status,
            "target_id": base_core["target_id"],
            "obligation_id": base_core["obligation_id"],
            "physical_carrier": base_core["physical_carrier"],
            "regime": base_core["regime"],
            "quantifiers": copy.deepcopy(base_core["quantifiers"]),
            "candidates": candidates,
            "candidate_difference": _candidate_difference(
                critical_pairs[0], critical_pairs[1]
            ),
            "eligible_for_precommitted_rule_replay": eligible,
            "decision_change_authorized": False,
            "truth_authority": None,
            "conceptual_merit_authority": None,
            "physics_authority": None,
            "theorem_authority": None,
            "physical_equivalence_authorized": False,
            "continuum_authorized": False,
            "proof_authorized": False,
            "investment_authorized": False,
            "experiment_selection_authorized": False,
        },
        "handback_digest",
    )
    return outcome, handback


def build_formal_transformation_sequence(
    base_core_raw: Mapping[str, Any],
    first_plan_raw: Mapping[str, Any],
    second_plan_raw: Mapping[str, Any],
    *,
    max_isomorphism_permutations: int = (
        DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS
    ),
) -> dict[str, Any]:
    """Construct and classify the exact two-order critical pair."""

    ceiling = _validate_ceiling(max_isomorphism_permutations)
    base_core = validate_conceptual_core(base_core_raw)
    plans = [
        _validate_plan(first_plan_raw),
        _validate_plan(second_plan_raw),
    ]
    if plans[0]["transformation_id"] == plans[1]["transformation_id"]:
        _fail(
            "the two transformation identifiers must be distinct",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )

    applications = [_apply_plan(base_core, plan) for plan in plans]
    application_summaries = [
        _application_summary(plan, application)
        for plan, application in zip(plans, applications, strict=True)
    ]
    coenabledness = _coenabledness(plans, applications)
    critical_pairs = [
        _critical_pair(
            base_core,
            plans[0],
            plans[1],
            applications[0],
        ),
        _critical_pair(
            base_core,
            plans[1],
            plans[0],
            applications[1],
        ),
    ]
    completed = [
        pair for pair in critical_pairs if pair["status"] == "completed"
    ]
    comparison = (
        compare_conceptual_cores(
            completed[0]["final_core"],
            completed[1]["final_core"],
            max_permutations=ceiling,
        )
        if len(completed) == 2
        else unavailable_core_comparison(
            max_permutations=ceiling,
            reason_code=(
                "critical_pair_incomplete"
                if coenabledness["status"] == "coenabled"
                else "transformations_not_coenabled"
            ),
        )
    )
    outcome, handback = _outcome_and_handback(
        base_core,
        coenabledness,
        critical_pairs,
        comparison,
    )
    packet: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "sequence_id": stable_identifier(
            "formal-concept-sequence",
            base_core["content_digest"],
            plans,
            {
                "canonicalization_version": CANONICALIZATION_VERSION,
                "max_permutations": ceiling,
            },
        ),
        "base_core": base_core,
        "transformations": plans,
        "isomorphism_policy": {
            "canonicalization_version": CANONICALIZATION_VERSION,
            "max_permutations": ceiling,
        },
        "initial_applications": application_summaries,
        "coenabledness": coenabledness,
        "critical_pairs": critical_pairs,
        "conceptual_core_comparison": comparison,
        "outcome": outcome,
        "finite_handback": handback,
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    packet["content_digest"] = canonical_digest(packet)
    try:
        validate_instance(packet, SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID)
    return packet


def validate_formal_transformation_sequence(
    raw: Mapping[str, Any],
) -> dict[str, Any]:
    """Schema-check and reconstruct a sequence packet byte-for-byte."""

    packet = copy.deepcopy(
        dict(
            _strict(
                raw,
                {
                    "schema_version",
                    "sequence_id",
                    "base_core",
                    "transformations",
                    "isomorphism_policy",
                    "initial_applications",
                    "coenabledness",
                    "critical_pairs",
                    "conceptual_core_comparison",
                    "outcome",
                    "finite_handback",
                    "authority_boundary",
                    "content_digest",
                },
                "formal transformation sequence",
                reason_code=FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
            )
        )
    )
    try:
        validate_instance(packet, SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID)
    expected_digest = canonical_digest(
        {
            key: value
            for key, value in packet.items()
            if key != "content_digest"
        }
    )
    if packet["content_digest"] != expected_digest:
        _fail(
            "formal transformation sequence content_digest is stale",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    plans = packet["transformations"]
    expected = build_formal_transformation_sequence(
        packet["base_core"],
        plans[0],
        plans[1],
        max_isomorphism_permutations=packet["isomorphism_policy"][
            "max_permutations"
        ],
    )
    if canonical_json(packet) != canonical_json(expected):
        _fail(
            "formal transformation sequence differs from deterministic replay",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    return {
        "status": "valid",
        "sequence_id": packet["sequence_id"],
        "content_digest": packet["content_digest"],
        "coenabledness_status": packet["coenabledness"]["status"],
        "comparison_status": packet["conceptual_core_comparison"][
            "comparison_status"
        ],
        "outcome_status": packet["outcome"]["status"],
        "retained_candidate_count": len(
            packet["finite_handback"]["candidates"]
        ),
        "truth_authority": None,
        "conceptual_merit_authority": None,
        "physics_authority": None,
        "theorem_authority": None,
    }


def _conditioned_step(
    *,
    ordinal: int,
    authored_from_core: Mapping[str, Any],
    plan: Mapping[str, Any],
    delta: Mapping[str, Any],
) -> dict[str, Any]:
    replay = _replay_delta(authored_from_core, delta)
    expected_application = _apply_plan(authored_from_core, plan)
    if (
        expected_application["status"] != "applied"
        or canonical_json(expected_application["delta"]) != canonical_json(delta)
    ):
        _fail(
            "conditioned step delta differs from exact plan replay on its authored core",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    return _seal(
        {
            "step_id": stable_identifier(
                "conditioned-concept-step",
                ordinal,
                authored_from_core["content_digest"],
                plan["transformation_id"],
                delta["content_digest"],
            ),
            "step_ordinal": ordinal,
            "plan": copy.deepcopy(dict(plan)),
            "plan_authored_from_core_digest": authored_from_core[
                "content_digest"
            ],
            "delta": copy.deepcopy(dict(delta)),
            "replay": replay,
        },
        "step_digest",
    )


def build_conditioned_formal_transformation_sequence(
    base_core_raw: Mapping[str, Any],
    first_plan_raw: Mapping[str, Any],
    first_delta_raw: Mapping[str, Any],
    second_plan_raw: Mapping[str, Any],
    second_delta_raw: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay one genuinely intermediate-conditioned order, and only that order.

    This constructor is deliberately distinct from the symmetric critical-pair
    algebra.  A plan authored from the first transformation's output has no
    authority on the original base, so this artifact never applies it there to
    manufacture a reverse path.  A reverse result must arrive as a separately
    authored conditioned packet and can then remain a plural candidate.
    """

    base_core = validate_conceptual_core(base_core_raw)
    first_plan = _validate_plan(first_plan_raw)
    second_plan = _validate_plan(second_plan_raw)
    if first_plan["transformation_id"] == second_plan["transformation_id"]:
        _fail(
            "conditioned transformations must have distinct identifiers",
            FORMAL_CONCEPT_SEQUENCE_INVALID,
        )
    first_delta = copy.deepcopy(dict(first_delta_raw))
    first_step = _conditioned_step(
        ordinal=1,
        authored_from_core=base_core,
        plan=first_plan,
        delta=first_delta,
    )
    intermediate = validate_conceptual_core(
        first_delta["after_core"], allow_free=True
    )
    second_delta = copy.deepcopy(dict(second_delta_raw))
    second_step = _conditioned_step(
        ordinal=2,
        authored_from_core=intermediate,
        plan=second_plan,
        delta=second_delta,
    )
    final_core = validate_conceptual_core(
        second_delta["after_core"], allow_free=True
    )
    protected_base = {
        row["observable_id"]: row
        for row in base_core["observables"]
        if row["protected"]
    }
    protected_final = {
        row["observable_id"]: row
        for row in final_core["observables"]
        if row["protected"]
    }
    protected_preserved = all(
        protected_final.get(observable_id) == observable
        for observable_id, observable in protected_base.items()
    )
    free_completion = any(
        delta["construction"]["construction_origin"]
        == "free_completion_counterfactual"
        or delta["obstruction_transition"]["after_status"]
        == "counterfactual_only"
        for delta in (first_delta, second_delta)
    )
    quarantine_reasons = [
        reason
        for reason in (
            None if protected_preserved else "protected_observable_erasure",
            (
                "free_completion_has_no_inhabitation_authority"
                if free_completion
                else None
            ),
            _quarantine_reason(first_delta),
            _quarantine_reason(second_delta),
        )
        if reason is not None
    ]
    quarantine_reasons = list(dict.fromkeys(quarantine_reasons))
    status = "completed" if not quarantine_reasons else "quarantined"
    witness_differences = _witness_differences([first_delta, second_delta])
    order = [
        first_plan["transformation_id"],
        second_plan["transformation_id"],
    ]
    conditioned_path = _seal(
        {
            "conditioned_path_id": stable_identifier(
                "conditioned-concept-path",
                base_core["content_digest"],
                intermediate["content_digest"],
                final_core["content_digest"],
                order,
            ),
            "status": status,
            "order": order,
            "base_core_digest": base_core["content_digest"],
            "intermediate_core_digest": intermediate["content_digest"],
            "final_core_digest": final_core["content_digest"],
            "exact_first_boundary": first_step["replay"][
                "exact_input_boundary"
            ],
            "exact_intermediate_boundary": second_step["replay"][
                "exact_input_boundary"
            ],
            "protected_distinctions_preserved": protected_preserved,
            "free_completion_detected": free_completion,
            "reverse_order_status": (
                "not_constructed_without_reverse_conditioned_authorship"
            ),
            "witness_differences": witness_differences,
            "quarantine_reasons": quarantine_reasons,
        },
        "path_digest",
    )
    finite_handback = _seal(
        {
            "handback_status": (
                "conditioned_candidate"
                if status == "completed"
                else "conditioned_path_quarantined"
            ),
            "candidate_core_digest": final_core["content_digest"],
            "relation_witness_digests": [
                first_delta["construction"]["witness_digest"],
                second_delta["construction"]["witness_digest"],
            ],
            "burden_statements": witness_differences["burden_statements"],
            "corrections": witness_differences["corrections"],
            "falsifiers": witness_differences["falsifiers"],
            "eligible_for_precommitted_rule_replay": status == "completed",
            "decision_change_authorized": False,
            "truth_authority": None,
            "conceptual_merit_authority": None,
            "physics_authority": None,
            "theorem_authority": None,
            "physical_equivalence_authorized": False,
            "continuum_authorized": False,
            "proof_authorized": False,
            "investment_authorized": False,
            "experiment_selection_authorized": False,
        },
        "handback_digest",
    )
    packet = {
        "schema_version": SCHEMA_VERSION,
        "sequence_kind": "intermediate_conditioned_one_order",
        "sequence_id": stable_identifier(
            "conditioned-formal-concept-sequence",
            base_core["content_digest"],
            first_step["step_digest"],
            second_step["step_digest"],
        ),
        "base_core": base_core,
        "first_step": first_step,
        "second_step": second_step,
        "order": order,
        "conditioned_path": conditioned_path,
        "finite_handback": finite_handback,
        "authority_boundary": copy.deepcopy(_AUTHORITY_BOUNDARY),
    }
    packet["content_digest"] = canonical_digest(packet)
    try:
        validate_instance(packet, CONDITIONED_SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID)
    return packet


def validate_conditioned_formal_transformation_sequence(
    raw: Mapping[str, Any],
) -> dict[str, Any]:
    """Schema-check and byte-replay one conditioned ordered sequence."""

    packet = copy.deepcopy(
        dict(
            _strict(
                raw,
                {
                    "schema_version",
                    "sequence_kind",
                    "sequence_id",
                    "base_core",
                    "first_step",
                    "second_step",
                    "order",
                    "conditioned_path",
                    "finite_handback",
                    "authority_boundary",
                    "content_digest",
                },
                "conditioned formal transformation sequence",
                reason_code=FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
            )
        )
    )
    try:
        validate_instance(packet, CONDITIONED_SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID)
    if packet["content_digest"] != canonical_digest(
        {key: value for key, value in packet.items() if key != "content_digest"}
    ):
        _fail(
            "conditioned sequence content digest is stale",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    expected = build_conditioned_formal_transformation_sequence(
        packet["base_core"],
        packet["first_step"]["plan"],
        packet["first_step"]["delta"],
        packet["second_step"]["plan"],
        packet["second_step"]["delta"],
    )
    if canonical_json(packet) != canonical_json(expected):
        _fail(
            "conditioned sequence differs from exact deterministic replay",
            FORMAL_CONCEPT_SEQUENCE_REPLAY_INVALID,
        )
    return {
        "status": "valid",
        "sequence_id": packet["sequence_id"],
        "content_digest": packet["content_digest"],
        "conditioned_path_id": packet["conditioned_path"][
            "conditioned_path_id"
        ],
        "path_status": packet["conditioned_path"]["status"],
        "reverse_order_status": packet["conditioned_path"][
            "reverse_order_status"
        ],
        "truth_authority": None,
        "conceptual_merit_authority": None,
        "physics_authority": None,
        "theorem_authority": None,
    }
