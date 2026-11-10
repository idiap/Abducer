# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compile declared task meaning into replayable Category/HoTT obligations.

The finite formal engines prove local structural facts, but a structurally valid
diagram is not yet about the task that motivated it.  This module supplies that
missing boundary.  It compiles explicit semantic anchors and typed relations,
selects only consequences native to the requested lens, and binds the resulting
meaning to a finite model without treating presentation identifiers as meaning.

Replay canonicalizes finite carriers up to bijective relabelling.  Consequently,
two isomorphic presentations have one signature, while a model carrying another
task's relation binding is rejected even if its normalized diagram is identical.
The final handback compares a declared incumbent decision with a declared,
relation-triggered candidate.  Missing or substantively unchanged decisions are
typed quarantine results.  No result in this module grants theorem, continuum,
Yang--Mills, physics-value, or investment authority.
"""

from __future__ import annotations

import copy
import json
from itertools import permutations, product
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_instance,
)


class TaskRelationCompilerError(ValueError):
    """Raised when task meaning cannot be compiled or replayed exactly."""

    def __init__(self, message: str, *, reason_code: str = "task_relation_compiler_invalid") -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _fail(message: str, *, reason_code: str = "task_relation_compiler_invalid") -> None:
    raise TaskRelationCompilerError(message, reason_code=reason_code)


TASK_RELATION_COMPILATION_INVALID = "task_relation_compilation_invalid"
TASK_RELATION_MODEL_BINDING_INVALID = "task_relation_model_binding_invalid"
TASK_RELATION_DECISION_INVALID = "task_relation_decision_invalid"

_LENS_RELATIONS = {
    "categorical": {
        "noncommuting_composition": (
            "ordered_composite_comparison",
            "Compare the two typed composites and localize the first failed commuting square.",
            "route_order",
        ),
        "mediating_factorization": (
            "mediator_existence_uniqueness",
            "Construct and test the mediator before transporting the target burden.",
            "mediator_choice",
        ),
        "functorial_transfer": (
            "functorial_preservation",
            "Test which declared invariant is preserved by the proposed functorial transfer.",
            "transfer_route",
        ),
    },
    "hott": {
        "identity_transport": (
            "identity_transport_coherence",
            "Construct the missing transport coherence without collapsing identity into equivalence.",
            "coherence_obligation",
        ),
        "equivalence_coherence": (
            "equivalence_coherence_cell",
            "Construct the pointwise higher cell relating the two equivalence-induced transports.",
            "coherence_obligation",
        ),
        "path_independence": (
            "path_independence",
            "Test path independence on every declared predicate fiber before quotienting presentations.",
            "path_choice",
        ),
        "descent_coherence": (
            "descent_coherence",
            "Retain the descent obstruction until its overlap coherence data are constructed.",
            "descent_route",
        ),
    },
}

_DECISION_KINDS = {
    "continue_route",
    "compare_route_order",
    "construct_mediator",
    "require_coherence",
    "split_route",
    "run_secondary_falsifier",
    "revise_translation",
    "quarantine_route",
}

_DEFAULT_GATES = [
    "physical equivalence",
    "same-theory continuum construction",
    "Osterwalder-Schrader reconstruction",
    "theorem status",
    "Hamiltonian or spectral result",
    "uniform positive mass gap",
    "Yang-Mills existence",
]


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be a nonempty string", reason_code=TASK_RELATION_COMPILATION_INVALID)
    return " ".join(value.split())


def _texts(value: Any, label: str, *, minimum: int = 1) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail(f"{label} must be a sequence", reason_code=TASK_RELATION_COMPILATION_INVALID)
    rows = [_text(item, label) for item in value]
    if len(rows) < minimum or len(rows) != len(set(rows)):
        _fail(f"{label} is incomplete or duplicated", reason_code=TASK_RELATION_COMPILATION_INVALID)
    return rows


def _strict_keys(raw: Mapping[str, Any], allowed: set[str], label: str) -> None:
    if set(raw) - allowed:
        _fail(
            f"{label} has undeclared fields: {sorted(set(raw) - allowed)}",
            reason_code=TASK_RELATION_COMPILATION_INVALID,
        )


def _decision(raw: Any, *, label: str, candidate: bool) -> dict[str, Any] | None:
    if raw is None:
        return None
    if not isinstance(raw, Mapping):
        _fail(f"{label} must be a mapping", reason_code=TASK_RELATION_DECISION_INVALID)
    allowed = {"decision_id", "decision_kind", "action", "target_burden_id"}
    if candidate:
        allowed.add("trigger_relation_id")
    _strict_keys(raw, allowed, label)
    required = allowed
    if set(raw) != required:
        _fail(f"{label} must declare exactly {sorted(required)}", reason_code=TASK_RELATION_DECISION_INVALID)
    kind = _text(raw.get("decision_kind"), f"{label}.decision_kind")
    if kind not in _DECISION_KINDS:
        _fail(f"{label} has an unsupported decision_kind", reason_code=TASK_RELATION_DECISION_INVALID)
    result = {
        "decision_id": _text(raw.get("decision_id"), f"{label}.decision_id"),
        "decision_kind": kind,
        "action": _text(raw.get("action"), f"{label}.action"),
        "target_burden_id": _text(raw.get("target_burden_id"), f"{label}.target_burden_id"),
        "trigger_relation_id": (
            _text(raw.get("trigger_relation_id"), f"{label}.trigger_relation_id")
            if candidate
            else None
        ),
    }
    return result


def _semantic_nodes(
    *,
    case_id: str,
    pressure: str,
    formal_pressure: str,
    primitives: Sequence[str],
    invariants: Sequence[str],
    physical_carrier: str | None,
    regime: str,
    quantifiers: Sequence[str],
    falsifier: str,
) -> list[dict[str, Any]]:
    rows: list[tuple[str, str]] = [
        ("pressure", pressure),
        ("formal_pressure", formal_pressure),
        *(("incumbent_primitive", value) for value in primitives),
        *(("protected_invariant", value) for value in invariants),
        ("regime", regime),
        *(("quantifier", value) for value in quantifiers),
        ("falsifier", falsifier),
    ]
    if physical_carrier is not None:
        rows.append(("physical_carrier", physical_carrier))
    return [
        {
            "node_id": stable_identifier("task-semantic-node", case_id, kind, ordinal, statement),
            "node_kind": kind,
            "ordinal": ordinal,
            "statement": statement,
            "statement_digest": canonical_digest(statement),
        }
        for ordinal, (kind, statement) in enumerate(rows)
    ]


def _compile_relations(
    raw: Any,
    *,
    case_id: str,
    nodes: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    # Defaults can assign the same text to different semantic roles (notably
    # pressure and regime). Resolve textual endpoints only for declared
    # relations; absent relations need no ambiguous text-to-node lookup.
    if raw is None:
        return []
    by_statement: dict[str, str] = {}
    for row in nodes:
        statement = str(row["statement"])
        if statement in by_statement:
            _fail(
                "semantic anchors must be textually distinct before relation compilation",
                reason_code=TASK_RELATION_COMPILATION_INVALID,
            )
        by_statement[statement] = str(row["node_id"])
    if isinstance(raw, (str, bytes)) or not isinstance(raw, Sequence) or not raw:
        _fail("task_relations must be a nonempty sequence when declared", reason_code=TASK_RELATION_COMPILATION_INVALID)
    result: list[dict[str, Any]] = []
    for ordinal, item in enumerate(raw):
        if not isinstance(item, Mapping):
            _fail("each task relation must be a mapping", reason_code=TASK_RELATION_COMPILATION_INVALID)
        _strict_keys(
            item,
            {"relation_id", "relation_kind", "statement", "source_anchor", "target_anchor"},
            "task relation",
        )
        if set(item) != {"relation_id", "relation_kind", "statement", "source_anchor", "target_anchor"}:
            _fail("each task relation must declare the complete relation contract", reason_code=TASK_RELATION_COMPILATION_INVALID)
        kind = _text(item["relation_kind"], "relation_kind")
        supported = set().union(*_LENS_RELATIONS.values())
        if kind not in supported:
            _fail(f"unsupported task relation kind {kind}", reason_code=TASK_RELATION_COMPILATION_INVALID)
        source = _text(item["source_anchor"], "source_anchor")
        target = _text(item["target_anchor"], "target_anchor")
        if source not in by_statement or target not in by_statement or source == target:
            _fail(
                "task relation endpoints must be two distinct declared semantic anchors",
                reason_code=TASK_RELATION_COMPILATION_INVALID,
            )
        relation_id = _text(item["relation_id"], "relation_id")
        result.append(
            {
                "relation_id": relation_id,
                "ordinal": ordinal,
                "relation_kind": kind,
                "statement": _text(item["statement"], "relation statement"),
                "source_node_id": by_statement[source],
                "target_node_id": by_statement[target],
                "source_statement": source,
                "target_statement": target,
                "applicable_lens": next(
                    lens for lens, contracts in _LENS_RELATIONS.items() if kind in contracts
                ),
            }
        )
    if len({row["relation_id"] for row in result}) != len(result):
        _fail("task relation identifiers must be unique", reason_code=TASK_RELATION_COMPILATION_INVALID)
    return result


def _binding_rows(
    *,
    case_id: str,
    lens: str,
    kind: str,
    statements: Sequence[str],
    formal_role: str,
    formal_id: str,
    member_ids: Sequence[str],
) -> list[dict[str, Any]]:
    return [
        {
            "binding_id": stable_identifier("task-semantic-binding", case_id, lens, kind, index, statement),
            "semantic_kind": kind,
            "ordinal": index,
            "statement": statement,
            "canonical_formal_role": formal_role,
            "canonical_member_slot": index % len(member_ids),
            # Presentation hints aid inspection but are deliberately absent from
            # the isomorphism signature and the model relation binding.
            "formal_id": formal_id,
            "formal_member_id": member_ids[index % len(member_ids)],
        }
        for index, statement in enumerate(statements)
    ]


def _schema(payload: Mapping[str, Any], schema_name: str) -> None:
    try:
        validate_instance(dict(payload), schema_name)
    except ContractError as exc:
        _fail(str(exc), reason_code=TASK_RELATION_COMPILATION_INVALID)


def compile_task_relation(case: Mapping[str, Any], lens: str) -> dict[str, Any]:
    """Compile one explicit task relation graph into a lens-specific blueprint."""

    semantics = case.get("task_semantics")
    if lens not in _LENS_RELATIONS or not isinstance(semantics, Mapping):
        _fail(
            "task-relation compilation needs categorical or hott task_semantics",
            reason_code=TASK_RELATION_COMPILATION_INVALID,
        )
    case_id = _text(case.get("case_id"), "case_id")
    target_id = _text(case.get("target_id"), "target_id")
    obligation_id = _text(case.get("obligation_id"), "obligation_id")
    pressure = _text(semantics.get("pressure"), "pressure")
    formal_pressure = _text(semantics.get("formal_pressure"), "formal_pressure")
    primitives = _texts(semantics.get("incumbent_primitives"), "incumbent_primitives", minimum=2)
    invariants = _texts(semantics.get("protected_invariants"), "protected_invariants", minimum=2)
    physical_carrier_raw = semantics.get("physical_carrier")
    physical_carrier = None if physical_carrier_raw is None else _text(physical_carrier_raw, "physical_carrier")
    nonphysics_marker = bool(
        physical_carrier is None or physical_carrier.startswith("not_applicable_non_physics:")
    )
    formal_carrier = pressure if physical_carrier is None else physical_carrier
    regime_origin = "declared" if semantics.get("regime") is not None else "pressure_boundary"
    regime = _text(semantics.get("regime", pressure), "regime")
    raw_quantifiers = semantics.get("quantifiers")
    quantifiers = (
        _texts(raw_quantifiers, "quantifiers")
        if raw_quantifiers is not None
        else [
            "For every declared primitive, the finite quotient retains its task binding.",
            "Every protected invariant remains an explicit open preservation obligation.",
        ]
    )
    falsifier = _text(semantics.get("falsifier"), "falsifier")
    correction = _text(
        semantics.get(
            "correction",
            "Quarantine the formal route and revise its task translation if the falsifier is observed.",
        ),
        "correction",
    )
    gates = _texts(semantics.get("untouched_physics_gates", _DEFAULT_GATES), "untouched_physics_gates")
    nodes = _semantic_nodes(
        case_id=case_id,
        pressure=pressure,
        formal_pressure=formal_pressure,
        primitives=primitives,
        invariants=invariants,
        physical_carrier=physical_carrier,
        regime=regime,
        quantifiers=quantifiers,
        falsifier=falsifier,
    )
    relations = _compile_relations(semantics.get("task_relations"), case_id=case_id, nodes=nodes)
    selected = [row for row in relations if row["applicable_lens"] == lens]
    consequences = []
    for row in selected:
        consequence_kind, instruction, dimension = _LENS_RELATIONS[lens][str(row["relation_kind"])]
        consequences.append(
            {
                "consequence_id": stable_identifier(
                    "task-lens-consequence", case_id, lens, row["relation_id"], consequence_kind
                ),
                "relation_id": row["relation_id"],
                "consequence_kind": consequence_kind,
                "statement": f"{instruction} Relation: {row['statement']}",
                "changed_burden": (
                    f"{instruction} Preserve the declared target obligation {obligation_id}."
                ),
                "decision_dimension": dimension,
            }
        )
    incumbent = _decision(
        semantics.get("incumbent_decision"), label="incumbent_decision", candidate=False
    )
    raw_lens_decisions = semantics.get("lens_decisions", {})
    if not isinstance(raw_lens_decisions, Mapping) or set(raw_lens_decisions) - set(_LENS_RELATIONS):
        _fail("lens_decisions must be keyed only by categorical or hott", reason_code=TASK_RELATION_DECISION_INVALID)
    lens_decisions = [
        {"lens": declared_lens, **decision}
        for declared_lens, raw in sorted(raw_lens_decisions.items())
        if (decision := _decision(raw, label=f"lens_decisions.{declared_lens}", candidate=True))
        is not None
    ]
    candidate = next((row for row in lens_decisions if row["lens"] == lens), None)
    selected_relation_ids = [str(row["relation_id"]) for row in selected]
    if candidate is not None and candidate["trigger_relation_id"] not in {
        str(row["relation_id"]) for row in relations
    }:
        _fail("lens decision cites an unknown task relation", reason_code=TASK_RELATION_DECISION_INVALID)
    if not selected:
        selection_status = "inapplicable"
        selection_reason = "No declared relation has semantics native to the requested lens."
    elif candidate is not None and candidate["trigger_relation_id"] not in selected_relation_ids:
        selection_status = "inapplicable"
        selection_reason = "The declared lens decision is triggered by a relation belonging to another lens."
    else:
        selection_status = "applicable"
        selection_reason = "At least one declared task relation selects a native consequence for this lens."

    seed = {
        "lens": lens,
        "case_id": case_id,
        "target_id": target_id,
        "obligation_id": obligation_id,
        "task_semantics_digest": canonical_digest(semantics),
    }
    prefix = f"runtime.task-relation.{lens}.{canonical_digest(seed).removeprefix('sha256:')[:24]}"
    source_id, mediator_id, target_formal_id = (
        f"{prefix}.A",
        f"{prefix}.B",
        f"{prefix}.C",
    )
    members = {
        "source": [f"{prefix}.a0", f"{prefix}.a1"],
        "mediator": [f"{prefix}.b0", f"{prefix}.b1"],
        "target": [f"{prefix}.c0", f"{prefix}.c1"]
        + ([f"{prefix}.c2"] if lens == "categorical" else []),
    }
    target_anchors = [formal_carrier, regime, *quantifiers, falsifier]
    left = [f"{prefix}.f1", f"{prefix}.f2"] if lens == "categorical" else [f"{prefix}.tAB1", f"{prefix}.tBC1"]
    right = [f"{prefix}.g1", f"{prefix}.g2"] if lens == "categorical" else [f"{prefix}.tAB2", f"{prefix}.tBC2"]
    quantifier_rows = [
        {
            "quantifier_id": stable_identifier("task-quantifier", case_id, index, statement),
            "statement": statement,
            "origin": "declared" if raw_quantifiers is not None else "finite_translation_boundary",
        }
        for index, statement in enumerate(quantifiers)
    ]
    contract = {
        "lens": lens,
        "case_id": case_id,
        "target_id": target_id,
        "obligation_id": obligation_id,
        "pressure": pressure,
        "formal_pressure": formal_pressure,
        "primitives": primitives,
        "invariants": invariants,
        "physical_carrier": physical_carrier,
        "domain_kind": "non_physics" if nonphysics_marker else "physics",
        "formal_carrier": formal_carrier,
        "regime": regime,
        "regime_origin": regime_origin,
        "quantifiers": quantifiers,
        "quantifier_bindings": quantifier_rows,
        "falsifier": falsifier,
        "correction": correction,
        "untouched_physics_gates": gates,
        "incumbent_decision": incumbent,
        "lens_decisions": lens_decisions,
    }
    compilation: dict[str, Any] = {
        "schema_version": "1.0.0",
        "compiler_id": "meaning-derived-task-relation-compiler.v1",
        "mode": "task_derived_finite_semantic_translation",
        "lens": lens,
        "case_id": case_id,
        "target_id": target_id,
        "obligation_id": obligation_id,
        "case_digest": canonical_digest(case),
        "task_semantics_digest": canonical_digest(semantics),
        "semantic_nodes": nodes,
        "task_relations": relations,
        "selected_relation_ids": selected_relation_ids,
        "lens_selection": {
            "status": selection_status,
            "reason": selection_reason,
            "native_relation_kinds": sorted(_LENS_RELATIONS[lens]),
        },
        "lens_consequences": consequences,
        "task_contract": contract,
        "primitive_bindings": _binding_rows(
            case_id=case_id,
            lens=lens,
            kind="incumbent_primitive",
            statements=primitives,
            formal_role="source",
            formal_id=source_id,
            member_ids=members["source"],
        ),
        "invariant_bindings": _binding_rows(
            case_id=case_id,
            lens=lens,
            kind="protected_invariant",
            statements=invariants,
            formal_role="mediator",
            formal_id=mediator_id,
            member_ids=members["mediator"],
        ),
        "target_bindings": _binding_rows(
            case_id=case_id,
            lens=lens,
            kind="target_anchor",
            statements=target_anchors,
            formal_role="target",
            formal_id=target_formal_id,
            member_ids=members["target"],
        ),
        "formal_projection": {
            "formal_profile_id": f"finite-{lens}-obstruction-profile.v1",
            "semantic_prefix": prefix,
            "canonical_role_order": ["source", "mediator", "target"],
            "carriers": [
                {"role": "source", "formal_id": source_id, "member_ids": members["source"]},
                {"role": "mediator", "formal_id": mediator_id, "member_ids": members["mediator"]},
                {"role": "target", "formal_id": target_formal_id, "member_ids": members["target"]},
            ],
            "source_id": source_id,
            "target_id": target_formal_id,
            "left_path_ids": left,
            "right_path_ids": right,
            "left_composite_id": f"{prefix}.{'compose-left' if lens == 'categorical' else 'transport-left'}",
            "right_composite_id": f"{prefix}.{'compose-right' if lens == 'categorical' else 'transport-right'}",
            "formal_pressure": formal_pressure,
        },
        "finite_quotient_boundary": (
            "Semantic anchors bind canonical roles and member slots; finite carrier membership does not establish physical equivalence."
        ),
        "authority_boundary": (
            "Meaning-derived finite structural translation only; formal elegance supplies no theorem, continuum, Yang-Mills, physics-value, or investment authority."
        ),
    }
    compilation["compilation_digest"] = canonical_digest(compilation)
    _schema(compilation, "task_relation_compilation.schema.json")
    return compilation


def build_task_relation_model_binding(compilation: Mapping[str, Any]) -> dict[str, Any]:
    """Project only presentation-independent task meaning into a model binding."""

    _schema(compilation, "task_relation_compilation.schema.json")
    return {
        "binding_version": "1.0.0",
        "compiler_id": compilation["compiler_id"],
        "compilation_digest": compilation["compilation_digest"],
        "lens": compilation["lens"],
        "formal_profile_id": compilation["formal_projection"]["formal_profile_id"],
        "selected_relation_ids": copy.deepcopy(compilation["selected_relation_ids"]),
        "lens_consequence_digest": canonical_digest(compilation["lens_consequences"]),
        "formal_elegance_authority": False,
        "physics_authority": False,
        "theorem_authority": False,
        "yang_mills_authority": False,
    }


def _json_sorted(rows: Sequence[Any]) -> list[Any]:
    return sorted(copy.deepcopy(list(rows)), key=canonical_json)


def _role_members(
    rows: Sequence[Mapping[str, Any]],
    *,
    id_field: str,
    members_field: str,
    source_id: str,
    target_id: str,
) -> tuple[dict[str, Mapping[str, Any]], dict[str, str], dict[str, list[str]]]:
    by_id = {str(row[id_field]): row for row in rows}
    if len(by_id) != 3 or source_id not in by_id or target_id not in by_id or source_id == target_id:
        _fail("formal profile must have distinct source, mediator, and target carriers", reason_code=TASK_RELATION_MODEL_BINDING_INVALID)
    middle = set(by_id) - {source_id, target_id}
    if len(middle) != 1:
        _fail("formal profile does not have one mediator", reason_code=TASK_RELATION_MODEL_BINDING_INVALID)
    mediator_id = next(iter(middle))
    roles = {source_id: "source", mediator_id: "mediator", target_id: "target"}
    members = {
        roles[row_id]: [str(value) for value in by_id[row_id][members_field]]
        for row_id in by_id
    }
    return by_id, roles, members


def _category_code(model: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    _, roles, members = _role_members(
        model["objects"],
        id_field="object_id",
        members_field="element_ids",
        source_id=str(witness["source_id"]),
        target_id=str(witness["target_id"]),
    )
    morphisms = {str(row["morphism_id"]): row for row in model["morphisms"]}
    compositions = {str(row["composition_id"]): row for row in model["compositions"]}
    candidates: list[bytes] = []
    for ordered in product(*(permutations(members[role]) for role in ("source", "mediator", "target"))):
        slots = {
            member: index
            for role_members in ordered
            for index, member in enumerate(role_members)
        }

        def arrow_signature(arrow_id: str) -> dict[str, Any]:
            row = morphisms[arrow_id]
            return {
                "domain": roles[str(row["domain_id"])],
                "codomain": roles[str(row["codomain_id"])],
                "kind": row["kind"],
                "identity": bool(row["is_identity"]),
                "action": sorted(
                    [slots[str(item["source_element_id"])], slots[str(item["target_element_id"])]]
                    for item in row["action"]
                ),
            }

        arrow_signatures = {arrow_id: arrow_signature(arrow_id) for arrow_id in morphisms}
        composition_signatures = {
            composition_id: {
                "path": [arrow_signatures[str(value)] for value in row["path_morphism_ids"]],
                "result": arrow_signatures[str(row["result_morphism_id"])],
            }
            for composition_id, row in compositions.items()
        }
        universal = model["universal_property"]
        cone_rows = []
        for row in universal["cone_checks"]:
            cone_rows.append(
                {
                    "candidate": arrow_signatures[str(row["candidate_morphism_id"])],
                    "composition": composition_signatures[str(row["composition_id"])],
                    "commutes": bool(row["commutes"]),
                }
            )
        code = {
            "profile": "finite-categorical-obstruction-profile.v1",
            "carrier_cardinalities": {role: len(members[role]) for role in sorted(members)},
            "morphisms": _json_sorted(list(arrow_signatures.values())),
            "compositions": _json_sorted(list(composition_signatures.values())),
            "universal_property": {
                "source_role": roles[str(universal["source_object_id"])],
                "mediator_role": roles[str(universal["apex_object_id"])],
                "target_role": roles[str(universal["target_object_id"])],
                "target_morphism": arrow_signatures[str(universal["target_morphism_id"])],
                "factor_out": arrow_signatures[str(universal["factor_out_morphism_id"])],
                "mediators": _json_sorted(
                    [arrow_signatures[str(value)] for value in universal["mediating_morphism_ids"]]
                ),
                "unique_mediator": arrow_signatures[str(universal["unique_mediator_id"])],
                "cone_checks": _json_sorted(cone_rows),
                "scope_complete": bool(universal["scope_complete"]),
                "status": universal["status"],
            },
            "witness": {
                "source_role": roles[str(witness["source_id"])],
                "target_role": roles[str(witness["target_id"])],
                "left_path": [arrow_signatures[str(value)] for value in witness["left_path_ids"]],
                "right_path": [arrow_signatures[str(value)] for value in witness["right_path_ids"]],
                "left_composite": composition_signatures[str(witness["left_composite_id"])],
                "right_composite": composition_signatures[str(witness["right_composite_id"])],
            },
        }
        candidates.append(canonical_json(code))
    return json.loads(min(candidates))


def _hott_code(model: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    _, roles, members = _role_members(
        model["types"],
        id_field="type_id",
        members_field="term_ids",
        source_id=str(witness["source_id"]),
        target_id=str(witness["target_id"]),
    )
    maps = {str(row["map_id"]): row for row in model["maps"]}
    paths = {str(row["path_id"]): row for row in model["paths"]}
    equivalences = {str(row["equivalence_id"]): row for row in model["equivalences"]}
    transports = {str(row["transport_id"]): row for row in model["transports"]}
    compositions = {str(row["composition_id"]): row for row in model["transport_compositions"]}
    candidates: list[bytes] = []
    for ordered in product(*(permutations(members[role]) for role in ("source", "mediator", "target"))):
        slots = {
            member: index
            for role_members in ordered
            for index, member in enumerate(role_members)
        }

        def map_signature(map_id: str) -> dict[str, Any]:
            row = maps[map_id]
            return {
                "domain": roles[str(row["domain_type_id"])],
                "codomain": roles[str(row["codomain_type_id"])],
                "action": sorted(
                    [slots[str(item["source_term_id"])], slots[str(item["target_term_id"])]]
                    for item in row["term_action"]
                ),
            }

        def path_signature(path_id: str) -> dict[str, Any]:
            row = paths[path_id]
            return {
                "level": int(row["level"]),
                "ambient_role": roles[str(row["ambient_type_id"])],
                "source_slot": slots[str(row["source_term_id"])],
                "target_slot": slots[str(row["target_term_id"])],
                "source_truth": row["source_fiber_truth"],
                "target_truth": row["target_fiber_truth"],
            }

        map_signatures = {map_id: map_signature(map_id) for map_id in maps}
        path_signatures = {path_id: path_signature(path_id) for path_id in paths}
        equivalence_signatures = {
            equivalence_id: {
                "domain": roles[str(row["domain_type_id"])],
                "codomain": roles[str(row["codomain_type_id"])],
                "forward": map_signatures[str(row["forward_map_id"])],
                "inverse": map_signatures[str(row["inverse_map_id"])],
                "left_homotopies": _json_sorted(
                    [path_signatures[str(value)] for value in row["left_inverse_homotopy_ids"]]
                ),
                "right_homotopies": _json_sorted(
                    [path_signatures[str(value)] for value in row["right_inverse_homotopy_ids"]]
                ),
                "status": row["status"],
            }
            for equivalence_id, row in equivalences.items()
        }
        transport_signatures: dict[str, dict[str, Any]] = {}
        for transport_id, row in transports.items():
            transport_signatures[transport_id] = {
                "equivalence": equivalence_signatures[str(row["equivalence_id"])],
                "predicate_roles": [
                    roles[str(row["source_type_id"])],
                    roles[str(row["target_type_id"])],
                ],
                "fiber_action": sorted(
                    [
                        slots[str(item["source_term_id"])],
                        slots[str(item["target_term_id"])],
                        bool(item["source_truth"]),
                        bool(item["target_truth"]),
                    ]
                    for item in row["fiber_action"]
                ),
            }
        composition_signatures = {
            composition_id: {
                "path": [transport_signatures[str(value)] for value in row["path_transport_ids"]],
                "result": transport_signatures[str(row["result_transport_id"])],
            }
            for composition_id, row in compositions.items()
        }
        predicate_signatures = []
        for row in model["transported_predicates"]:
            predicate_signatures.append(
                {
                    "base_role": roles[str(row["base_type_id"])],
                    "target_role": roles[str(row["target_type_id"])],
                    "source_truth": sorted(
                        [slots[str(item["term_id"])], bool(item["truth_value"])]
                        for item in row["source_fiber"]
                    ),
                    "target_truth": sorted(
                        [slots[str(item["term_id"])], bool(item["truth_value"])]
                        for item in row["target_fiber"]
                    ),
                }
            )
        cell_signatures = []
        for row in model["coherence_cells"]:
            cell_signatures.append(
                {
                    "level": int(row["level"]),
                    "source_path": [transport_signatures[str(value)] for value in row["source_transport_ids"]],
                    "target_path": [transport_signatures[str(value)] for value in row["target_transport_ids"]],
                    "source_composition": composition_signatures[str(row["source_composition_id"])],
                    "target_composition": composition_signatures[str(row["target_composition_id"])],
                    "source_role": roles[str(row["source_type_id"])],
                    "target_role": roles[str(row["target_type_id"])],
                    "pointwise_paths": _json_sorted(
                        [path_signatures[str(value)] for value in row["pointwise_path_ids"]]
                    ),
                    "missing_source_slots": sorted(slots[str(value)] for value in row["missing_path_term_ids"]),
                    "status": row["status"],
                }
            )
        code = {
            "profile": "finite-hott-obstruction-profile.v1",
            "carrier_cardinalities": {role: len(members[role]) for role in sorted(members)},
            "maps": _json_sorted(list(map_signatures.values())),
            "paths": _json_sorted(list(path_signatures.values())),
            "equivalences": _json_sorted(list(equivalence_signatures.values())),
            "predicates": _json_sorted(predicate_signatures),
            "transports": _json_sorted(list(transport_signatures.values())),
            "compositions": _json_sorted(list(composition_signatures.values())),
            "coherence_cells": _json_sorted(cell_signatures),
            "truncation": {
                "default_level": int(model["truncation_policy"]["default_level"]),
                "retained_through_level": int(model["truncation_policy"]["retained_through_level"]),
                "application_status": model["truncation_policy"]["application_status"],
                "open_cell_count": len(model["truncation_policy"]["open_cell_ids"]),
            },
            "witness": {
                "source_role": roles[str(witness["source_id"])],
                "target_role": roles[str(witness["target_id"])],
                "left_path": [transport_signatures[str(value)] for value in witness["left_path_ids"]],
                "right_path": [transport_signatures[str(value)] for value in witness["right_path_ids"]],
                "left_composite": composition_signatures[str(witness["left_composite_id"])],
                "right_composite": composition_signatures[str(witness["right_composite_id"])],
            },
        }
        candidates.append(canonical_json(code))
    return json.loads(min(candidates))


def canonical_formal_projection(
    lens: str, model: Mapping[str, Any], witness: Mapping[str, Any]
) -> dict[str, Any]:
    """Return an identifier-free normal form over all finite carrier bijections."""

    if lens == "categorical":
        code = _category_code(model, witness)
    elif lens == "hott":
        code = _hott_code(model, witness)
    else:
        _fail("unknown formal lens", reason_code=TASK_RELATION_MODEL_BINDING_INVALID)
    return {
        "canonicalization_version": "finite-carrier-isomorphism.v1",
        "lens": lens,
        "canonical_code_digest": canonical_digest(code),
    }


def validate_task_relation_model_binding(
    compilation: Mapping[str, Any], model: Mapping[str, Any], witness: Mapping[str, Any]
) -> dict[str, Any]:
    """Replay exact task meaning while accepting harmless formal relabellings."""

    expected = build_task_relation_model_binding(compilation)
    if model.get("task_relation_binding") != expected:
        _fail(
            "formal model carries a missing, foreign, or stale task relation binding",
            reason_code=TASK_RELATION_MODEL_BINDING_INVALID,
        )
    projection = canonical_formal_projection(str(compilation["lens"]), model, witness)
    return {
        "task_relation_binding_digest": canonical_digest(expected),
        "canonical_isomorphism_digest": projection["canonical_code_digest"],
        "formal_projection_digest": canonical_digest(projection),
    }


def _decision_basis(decision: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if decision is None:
        return None
    return {
        "decision_kind": decision["decision_kind"],
        "action": decision["action"],
        "target_burden_id": decision["target_burden_id"],
    }


def build_formal_delta_and_handback(
    compilation: Mapping[str, Any],
    model_identity: Mapping[str, Any],
    replay: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a consequence and exact incumbent comparison, never value authority."""

    _schema(compilation, "task_relation_compilation.schema.json")
    contract = compilation["task_contract"]
    lens = str(compilation["lens"])
    consequences = copy.deepcopy(compilation["lens_consequences"])
    selected = set(compilation["selected_relation_ids"])
    incumbent = copy.deepcopy(contract["incumbent_decision"])
    candidate = next(
        (copy.deepcopy(row) for row in contract["lens_decisions"] if row["lens"] == lens),
        None,
    )
    applicable = compilation["lens_selection"]["status"] == "applicable"
    candidate_triggered = bool(candidate and candidate["trigger_relation_id"] in selected)
    incumbent_basis = _decision_basis(incumbent)
    candidate_basis = _decision_basis(candidate)
    substantive_change = bool(
        contract["domain_kind"] == "physics"
        and applicable
        and candidate_triggered
        and incumbent_basis is not None
        and candidate_basis is not None
        and incumbent_basis != candidate_basis
    )
    if contract["domain_kind"] != "physics":
        status = "quarantined_non_physics"
        quarantine_reason = "The task has no declared physical carrier, so no physics decision is available."
    elif not applicable or not candidate_triggered:
        status = "quarantined_lens_inapplicable"
        quarantine_reason = "No declared relation-triggered decision is native to this lens."
    elif incumbent_basis is None or candidate_basis is None:
        status = "quarantined_missing_decision_declaration"
        quarantine_reason = "An exact incumbent and relation-triggered candidate decision were not both declared."
    elif not substantive_change:
        status = "quarantined_no_decision_change"
        quarantine_reason = "The proposed action is substantively identical to the declared incumbent action."
    else:
        status = "decision_changed"
        quarantine_reason = None
    burden = (
        " ".join(str(row["changed_burden"]) for row in consequences)
        if consequences
        else "No lens-native burden was compiled; retain the incumbent route under quarantine."
    )
    delta: dict[str, Any] = {
        "schema_version": "1.0.0",
        "delta_kind": f"task_relation_finite_{lens}_obstruction",
        "compilation_digest": compilation["compilation_digest"],
        "model_identity": copy.deepcopy(dict(model_identity)),
        "countermodel_result": replay["result"],
        "counterexample_count": len(replay["counterexamples"]),
        "counterexamples_digest": canonical_digest(replay["counterexamples"]),
        "formal_carrier": contract["formal_carrier"],
        "physical_carrier": contract["physical_carrier"],
        "regime": {"statement": contract["regime"], "origin": contract["regime_origin"]},
        "quantifiers": copy.deepcopy(contract["quantifier_bindings"]),
        "selected_relation_ids": copy.deepcopy(compilation["selected_relation_ids"]),
        "lens_consequences": consequences,
        "changed_theoretical_burden": burden,
        "falsifier": contract["falsifier"],
        "correction": contract["correction"],
        "physics_decision_status": status,
        "finite_only": True,
    }
    delta["content_digest"] = canonical_digest(delta)
    _schema(delta, "task_derived_formal_delta.schema.json")
    handback: dict[str, Any] = {
        "schema_version": "1.0.0",
        "handback_kind": "finite_formal_witness_to_exact_physics_decision",
        "handback_status": status,
        "lens": lens,
        "case_id": compilation["case_id"],
        "target_id": compilation["target_id"],
        "task_relation_compilation_digest": compilation["compilation_digest"],
        "task_derived_formal_delta_digest": delta["content_digest"],
        "physical_carrier": contract["physical_carrier"],
        "formal_carrier": contract["formal_carrier"],
        "regime": copy.deepcopy(delta["regime"]),
        "quantifiers": copy.deepcopy(delta["quantifiers"]),
        "lens_consequences": consequences,
        "incumbent_decision": incumbent,
        "proposed_next_decision": candidate if substantive_change else None,
        "decision_comparison": {
            "incumbent_basis_digest": canonical_digest(incumbent_basis),
            "candidate_basis_digest": canonical_digest(candidate_basis),
            "substantive_change": substantive_change,
            "comparison_rule": "decision_kind + normalized action + target_burden_id",
        },
        "changed_next_physics_decision": candidate["action"] if substantive_change else None,
        "changed_next_theory_decision": burden,
        "quarantine_reason": quarantine_reason,
        "route_control_disposition": (
            "return_to_reflective_theory" if substantive_change else "quarantine_non_investment"
        ),
        "investment_disposition": "non_investment_formal_evidence_only",
        "falsifier": contract["falsifier"],
        "correction": contract["correction"],
        "untouched_physics_gates": copy.deepcopy(contract["untouched_physics_gates"]),
        "experiment_role": "secondary_precommitted_falsifier_test_only",
        "authority_nulls": [
            "physical_equivalence",
            "continuum",
            "OS_reconstruction",
            "theorem",
            "spectral_result",
            "mass_gap",
            "Yang-Mills_result",
            "physics_value",
        ],
        "formal_elegance_authorized": False,
        "theorem_authorized": False,
        "yang_mills_authorized": False,
        "physics_value_authorized": False,
        "investment_authorized": False,
    }
    handback["content_digest"] = canonical_digest(handback)
    _schema(handback, "formal_physics_decision_handback.schema.json")
    return delta, handback


__all__ = [
    "TASK_RELATION_COMPILATION_INVALID",
    "TASK_RELATION_DECISION_INVALID",
    "TASK_RELATION_MODEL_BINDING_INVALID",
    "TaskRelationCompilerError",
    "build_formal_delta_and_handback",
    "build_task_relation_model_binding",
    "canonical_formal_projection",
    "compile_task_relation",
    "validate_task_relation_model_binding",
]
