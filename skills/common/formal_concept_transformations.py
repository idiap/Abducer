# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Relation-specific finite conceptual transformations for Category theory and HoTT.

This additive v2 kernel does not select a lens, infer a task relation, or
integrate with the current producer runtime. Given a frozen finite conceptual
core, a typed relation hypothesis, and an exact witness, it constructs a
replayable before/after delta.

The kernel reuses the theory-atlas defect compiler as the upstream
defect/completion authority. relation_hypothesis_from_theory_atlas validates an
atlas packet and binds its packet, defect, candidate, obligation, and evidence
identities; it does not copy the atlas repair ladder, reflection sweep,
redescription operators, or finite completion implementations.

Protected observables are executable finite functions. Every relation used by a
construction transports those functions explicitly. A map that identifies
members carrying different protected values is retained as a counterexample and
quarantines the transformation. HoTT inhabitants are either already present in
the frozen source core or are marked free_adjoinment. The latter always produces
a counterfactual-only result and can never remove an obstruction or authorize a
decision flip.

All authority is finite and local. No artifact produced here establishes truth,
conceptual merit, a theorem, continuum control, physics value, or investment.
Experiments remain secondary theory-requested falsifiers.
"""

from __future__ import annotations

import copy
import math
import re
from collections import defaultdict
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_instance,
)
from skills.common.theory_atlas_defect_compiler import (
    TheoryAtlasDefectError,
    validate_theory_atlas_defect_packet,
)


SCHEMA = "formal_conceptual_delta_v2.schema.json"
SCHEMA_VERSION = "2.0.0"

CATEGORY_RELATION_KINDS = (
    "noncommuting_composition",
    "mediating_factorization",
    "functorial_transfer",
)
HOTT_RELATION_KINDS = (
    "identity_transport",
    "equivalence_coherence",
    "path_independence",
    "descent_coherence",
)
RELATION_KINDS = CATEGORY_RELATION_KINDS + HOTT_RELATION_KINDS

CONSTRUCTOR_IDS = {
    "noncommuting_composition": "noncommutativity_localizer.v2",
    "mediating_factorization": "mediator_factorizer.v2",
    "functorial_transfer": "functorial_transfer_builder.v2",
    "identity_transport": "identity_transport_builder.v2",
    "equivalence_coherence": "equivalence_coherence_builder.v2",
    "path_independence": "path_independence_builder.v2",
    "descent_coherence": "descent_coherence_builder.v2",
}

FORMAL_CONCEPT_CORE_INVALID = "formal_concept_core_invalid"
FORMAL_CONCEPT_RELATION_INVALID = "formal_concept_relation_invalid"
FORMAL_CONCEPT_WITNESS_INVALID = "formal_concept_witness_invalid"
FORMAL_CONCEPT_PRESERVATION_INVALID = "formal_concept_preservation_invalid"
FORMAL_CONCEPT_REPLAY_INVALID = "formal_concept_replay_invalid"
FREE_COMPLETION_PROMOTION_INVALID = "free_completion_promotion_invalid"

_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,191}$")
_CORE_KEYS = {
    "schema_version",
    "core_id",
    "target_id",
    "obligation_id",
    "physical_carrier",
    "regime",
    "quantifiers",
    "primitives",
    "relations",
    "observables",
    "inhabitants",
    "burdens",
    "content_digest",
}
_CONSEQUENCE_KEYS = {
    "explanatory_gain",
    "new_question",
    "changed_burden",
    "correction",
    "falsifier",
    "physics_next_action",
}
_RELATION_HYPOTHESIS_KEYS = {
    "relation_id",
    "relation_kind",
    "statement",
    "source_primitive_id",
    "target_primitive_id",
    "premise_ids",
}
_WITNESS_KEYS = {
    "noncommuting_composition": {
        "witness_kind",
        "left_path_relation_ids",
        "right_path_relation_ids",
    },
    "mediating_factorization": {
        "witness_kind",
        "direct_relation_id",
        "mediator",
        "first_leg",
        "second_leg",
    },
    "functorial_transfer": {
        "witness_kind",
        "source_relation_id",
        "transferred_source",
        "transferred_target",
        "source_component",
        "target_component",
        "transferred_relation",
    },
    "identity_transport": {
        "witness_kind",
        "construction_origin",
        "transport_relation_id",
        "path_inhabitant_ids",
        "adjoined_paths",
    },
    "equivalence_coherence": {
        "witness_kind",
        "construction_origin",
        "forward_relation_id",
        "inverse_relation_id",
        "left_path_inhabitant_ids",
        "right_path_inhabitant_ids",
        "coherence_cell_ids",
        "adjoined_paths",
        "adjoined_cells",
    },
    "path_independence": {
        "witness_kind",
        "construction_origin",
        "left_path_relation_ids",
        "right_path_relation_ids",
        "path_inhabitant_ids",
        "adjoined_paths",
    },
    "descent_coherence": {
        "witness_kind",
        "construction_origin",
        "left_restriction_relation_id",
        "right_restriction_relation_id",
        "compatible_pairs",
        "adjoined_paths",
    },
}
_WITNESS_KIND = {
    "noncommuting_composition": "noncommutativity_localization",
    "mediating_factorization": "mediator_factorization",
    "functorial_transfer": "functorial_transfer",
    "identity_transport": "identity_transport",
    "equivalence_coherence": "equivalence_coherence",
    "path_independence": "path_independence",
    "descent_coherence": "descent_coherence",
}
_ATLAS_COMPLETION_TO_RELATIONS = {
    "factorization": {"mediating_factorization"},
    "finite_representability": {"functorial_transfer", "equivalence_coherence"},
    "descent_gluing": {"descent_coherence"},
    "pushout": {"noncommuting_composition", "path_independence"},
    "adjunction_naturality": {"functorial_transfer", "equivalence_coherence"},
    "lifting_obstruction": {"noncommuting_composition", "identity_transport"},
}


class FormalConceptTransformationError(ValueError):
    """Typed failure of a finite conceptual transformation or its replay."""

    def __init__(self, message: str, *, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: {message}")


def _fail(message: str, reason_code: str) -> None:
    raise FormalConceptTransformationError(message, reason_code=reason_code)


def _strict(raw: Mapping[str, Any], expected: set[str], label: str, reason: str) -> None:
    if set(raw) != expected:
        missing = sorted(expected - set(raw))
        extra = sorted(set(raw) - expected)
        _fail(f"{label} keys differ; missing={missing}, extra={extra}", reason)


def _mapping(value: Any, label: str, reason: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(f"{label} must be a mapping", reason)
    return value


def _rows(value: Any, label: str, reason: str, *, minimum: int = 0) -> list[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail(f"{label} must be a sequence", reason)
    result = list(value)
    if len(result) < minimum:
        _fail(f"{label} requires at least {minimum} row(s)", reason)
    return result


def _text(value: Any, label: str, reason: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be a nonempty string", reason)
    return value


def _identifier(value: Any, label: str, reason: str) -> str:
    result = _text(value, label, reason)
    if _IDENTIFIER.fullmatch(result) is None:
        _fail(f"{label} is not a valid identifier", reason)
    return result


def _identifiers(
    value: Any,
    label: str,
    reason: str,
    *,
    minimum: int = 0,
) -> list[str]:
    result = [
        _identifier(item, f"{label}[{index}]", reason)
        for index, item in enumerate(_rows(value, label, reason, minimum=minimum))
    ]
    if len(result) != len(set(result)):
        _fail(f"{label} contains duplicate identifiers", reason)
    return result


def _unique(
    rows: Sequence[Mapping[str, Any]],
    key: str,
    label: str,
    reason: str,
) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        identifier = _identifier(row.get(key), f"{label}.{key}", reason)
        if identifier in result:
            _fail(f"{label} contains duplicate {key} {identifier}", reason)
        result[identifier] = row
    return result


def _seal(raw: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(raw))
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def _scalar(value: Any, label: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        _fail(f"{label} is not finite", FORMAL_CONCEPT_CORE_INVALID)
    if value is not None and not isinstance(value, (str, bool, int, float)):
        _fail(f"{label} must be a canonical scalar", FORMAL_CONCEPT_CORE_INVALID)


def _validate_core(raw: Mapping[str, Any], *, allow_free: bool) -> dict[str, Any]:
    core = copy.deepcopy(
        dict(_mapping(raw, "conceptual core", FORMAL_CONCEPT_CORE_INVALID))
    )
    _strict(core, _CORE_KEYS, "conceptual core", FORMAL_CONCEPT_CORE_INVALID)
    if core["schema_version"] != SCHEMA_VERSION:
        _fail(
            "conceptual core schema_version must be 2.0.0",
            FORMAL_CONCEPT_CORE_INVALID,
        )
    for field in ("core_id", "target_id", "obligation_id"):
        _identifier(core[field], field, FORMAL_CONCEPT_CORE_INVALID)
    if core["physical_carrier"] is not None:
        _text(
            core["physical_carrier"],
            "physical_carrier",
            FORMAL_CONCEPT_CORE_INVALID,
        )
    _text(core["regime"], "regime", FORMAL_CONCEPT_CORE_INVALID)
    declared_digest = _text(
        core["content_digest"], "content_digest", FORMAL_CONCEPT_CORE_INVALID
    )
    expected_digest = canonical_digest(
        {key: value for key, value in core.items() if key != "content_digest"}
    )
    if declared_digest != expected_digest:
        _fail(
            "conceptual core content_digest is stale",
            FORMAL_CONCEPT_CORE_INVALID,
        )

    quantifiers = []
    for index, raw_row in enumerate(
        _rows(
            core["quantifiers"],
            "quantifiers",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
    ):
        row = _mapping(
            raw_row, f"quantifiers[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {"quantifier_id", "statement"},
            "quantifier",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["quantifier_id"], "quantifier_id", FORMAL_CONCEPT_CORE_INVALID
        )
        _text(
            row["statement"],
            "quantifier.statement",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        quantifiers.append(row)
    _unique(
        quantifiers, "quantifier_id", "quantifiers", FORMAL_CONCEPT_CORE_INVALID
    )

    primitives = []
    all_members: set[str] = set()
    for index, raw_row in enumerate(
        _rows(
            core["primitives"],
            "primitives",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
    ):
        row = _mapping(
            raw_row, f"primitives[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {"primitive_id", "statement", "member_ids"},
            "primitive",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["primitive_id"], "primitive_id", FORMAL_CONCEPT_CORE_INVALID
        )
        _text(
            row["statement"],
            "primitive.statement",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        members = _identifiers(
            row["member_ids"],
            "primitive.member_ids",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
        overlap = all_members & set(members)
        if overlap:
            _fail(
                f"member identifiers must be globally unique: {sorted(overlap)}",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        all_members.update(members)
        primitives.append(row)
    primitive_by_id = _unique(
        primitives, "primitive_id", "primitives", FORMAL_CONCEPT_CORE_INVALID
    )

    relations = []
    for index, raw_row in enumerate(
        _rows(
            core["relations"],
            "relations",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
    ):
        row = _mapping(
            raw_row, f"relations[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {
                "relation_id",
                "relation_type",
                "statement",
                "source_primitive_id",
                "target_primitive_id",
                "action",
            },
            "relation",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["relation_id"], "relation_id", FORMAL_CONCEPT_CORE_INVALID
        )
        _identifier(
            row["relation_type"], "relation_type", FORMAL_CONCEPT_CORE_INVALID
        )
        _text(
            row["statement"],
            "relation.statement",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        source_id = _identifier(
            row["source_primitive_id"],
            "source_primitive_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        target_id = _identifier(
            row["target_primitive_id"],
            "target_primitive_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if source_id not in primitive_by_id or target_id not in primitive_by_id:
            _fail(
                "relation endpoints must name declared primitives",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        action = []
        for action_index, raw_action in enumerate(
            _rows(
                row["action"],
                "relation.action",
                FORMAL_CONCEPT_CORE_INVALID,
                minimum=1,
            )
        ):
            item = _mapping(
                raw_action,
                f"relation.action[{action_index}]",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            _strict(
                item,
                {"source_member_id", "target_member_id"},
                "action row",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            _identifier(
                item["source_member_id"],
                "source_member_id",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            target_member = _identifier(
                item["target_member_id"],
                "target_member_id",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            if target_member not in primitive_by_id[target_id]["member_ids"]:
                _fail(
                    "relation action leaves its target carrier",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            action.append(item)
        expected_sources = list(primitive_by_id[source_id]["member_ids"])
        if [item["source_member_id"] for item in action] != expected_sources:
            _fail(
                "relation action must be a total ordered function on its source carrier",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        relations.append(row)
    _unique(relations, "relation_id", "relations", FORMAL_CONCEPT_CORE_INVALID)

    observables = []
    protected_count = 0
    for index, raw_row in enumerate(
        _rows(
            core["observables"],
            "observables",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
    ):
        row = _mapping(
            raw_row, f"observables[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {
                "observable_id",
                "carrier_primitive_id",
                "statement",
                "protected",
                "evaluations",
            },
            "observable",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["observable_id"], "observable_id", FORMAL_CONCEPT_CORE_INVALID
        )
        carrier_id = _identifier(
            row["carrier_primitive_id"],
            "carrier_primitive_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if carrier_id not in primitive_by_id:
            _fail(
                "observable carrier is not declared",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        _text(
            row["statement"],
            "observable.statement",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if not isinstance(row["protected"], bool):
            _fail(
                "observable.protected must be boolean",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        protected_count += int(row["protected"])
        evaluations = []
        for eval_index, raw_eval in enumerate(
            _rows(
                row["evaluations"],
                "observable.evaluations",
                FORMAL_CONCEPT_CORE_INVALID,
                minimum=1,
            )
        ):
            item = _mapping(
                raw_eval,
                f"observable.evaluations[{eval_index}]",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            _strict(
                item,
                {"member_id", "value"},
                "observable evaluation",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            _identifier(
                item["member_id"],
                "observable.member_id",
                FORMAL_CONCEPT_CORE_INVALID,
            )
            _scalar(item["value"], "observable.value")
            evaluations.append(item)
        if [item["member_id"] for item in evaluations] != list(
            primitive_by_id[carrier_id]["member_ids"]
        ):
            _fail(
                "observable evaluations must exhaust the carrier in canonical order",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        observables.append(row)
    _unique(
        observables,
        "observable_id",
        "observables",
        FORMAL_CONCEPT_CORE_INVALID,
    )
    if protected_count == 0:
        _fail(
            "at least one observable must be protected",
            FORMAL_CONCEPT_CORE_INVALID,
        )

    inhabitants = []
    for index, raw_row in enumerate(
        _rows(
            core["inhabitants"],
            "inhabitants",
            FORMAL_CONCEPT_CORE_INVALID,
        )
    ):
        row = _mapping(
            raw_row, f"inhabitants[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {
                "inhabitant_id",
                "level",
                "ambient_primitive_id",
                "source_boundary_id",
                "target_boundary_id",
                "derivation_rule",
                "premise_inhabitant_ids",
                "evidence_refs",
            },
            "inhabitant",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["inhabitant_id"],
            "inhabitant_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if row["level"] not in {1, 2}:
            _fail(
                "inhabitant level must be 1 or 2",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        ambient = _identifier(
            row["ambient_primitive_id"],
            "ambient_primitive_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if ambient not in primitive_by_id:
            _fail(
                "inhabitant ambient primitive is absent",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        _identifier(
            row["source_boundary_id"],
            "source_boundary_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["target_boundary_id"],
            "target_boundary_id",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if row["derivation_rule"] not in {
            "reflexivity",
            "declared_domain_constructor",
            "path_composition",
            "declared_coherence_constructor",
            "free_adjoinment",
        }:
            _fail(
                "unsupported inhabitant derivation rule",
                FORMAL_CONCEPT_CORE_INVALID,
            )
        _identifiers(
            row["premise_inhabitant_ids"],
            "premise_inhabitant_ids",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifiers(
            row["evidence_refs"],
            "evidence_refs",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        if row["derivation_rule"] == "free_adjoinment" and not allow_free:
            _fail(
                "a frozen source core cannot contain free-adjoinment inhabitants",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        inhabitants.append(row)
    inhabitant_by_id = _unique(
        inhabitants,
        "inhabitant_id",
        "inhabitants",
        FORMAL_CONCEPT_CORE_INVALID,
    )
    for row in inhabitants:
        ambient_members = set(
            primitive_by_id[row["ambient_primitive_id"]]["member_ids"]
        )
        premises = row["premise_inhabitant_ids"]
        evidence = row["evidence_refs"]
        rule = row["derivation_rule"]
        if row["level"] == 1:
            if (
                row["source_boundary_id"] not in ambient_members
                or row["target_boundary_id"] not in ambient_members
            ):
                _fail(
                    "level-1 path boundaries must be terms of the ambient primitive",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        else:
            left = inhabitant_by_id.get(row["source_boundary_id"])
            right = inhabitant_by_id.get(row["target_boundary_id"])
            if (
                left is None
                or right is None
                or left["level"] != 1
                or right["level"] != 1
            ):
                _fail(
                    "level-2 cell boundaries must be declared level-1 paths",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            if (
                left["ambient_primitive_id"] != row["ambient_primitive_id"]
                or right["ambient_primitive_id"]
                != row["ambient_primitive_id"]
                or left["source_boundary_id"]
                != right["source_boundary_id"]
                or left["target_boundary_id"]
                != right["target_boundary_id"]
            ):
                _fail(
                    "level-2 cell boundaries must be parallel paths in one ambient primitive",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        if rule == "reflexivity":
            if (
                row["level"] != 1
                or row["source_boundary_id"] != row["target_boundary_id"]
                or premises
                or evidence
            ):
                _fail(
                    "reflexivity must be an evidence-free constant level-1 path",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        elif rule == "declared_domain_constructor":
            if row["level"] != 1 or premises or not evidence:
                _fail(
                    "declared domain paths require evidence refs and no hidden premises",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        elif rule == "path_composition":
            if row["level"] != 1 or len(premises) < 2 or evidence:
                _fail(
                    "path composition requires at least two exact path premises",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            premise_rows = [inhabitant_by_id.get(item) for item in premises]
            if any(
                item is None or item["level"] != 1 for item in premise_rows
            ):
                _fail(
                    "path composition cites a missing or non-path premise",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            if any(
                item["ambient_primitive_id"]
                != row["ambient_primitive_id"]
                for item in premise_rows
                if item
            ):
                _fail(
                    "path composition changes ambient primitive",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            if any(
                premise_rows[index]["target_boundary_id"]
                != premise_rows[index + 1]["source_boundary_id"]
                for index in range(len(premise_rows) - 1)
            ):
                _fail(
                    "path composition premises do not compose",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
            if (
                premise_rows[0]["source_boundary_id"]
                != row["source_boundary_id"]
                or premise_rows[-1]["target_boundary_id"]
                != row["target_boundary_id"]
            ):
                _fail(
                    "path composition has stale outer boundaries",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        elif rule == "declared_coherence_constructor":
            if (
                row["level"] != 2
                or premises
                != [
                    row["source_boundary_id"],
                    row["target_boundary_id"],
                ]
                or not evidence
            ):
                _fail(
                    "declared coherence cells require exact boundary premises and evidence refs",
                    FORMAL_CONCEPT_CORE_INVALID,
                )
        elif rule == "free_adjoinment":
            if premises or evidence:
                _fail(
                    "free adjoinment cannot carry derived evidence or premises",
                    FORMAL_CONCEPT_CORE_INVALID,
                )

    burdens = []
    for index, raw_row in enumerate(
        _rows(
            core["burdens"],
            "burdens",
            FORMAL_CONCEPT_CORE_INVALID,
            minimum=1,
        )
    ):
        row = _mapping(
            raw_row, f"burdens[{index}]", FORMAL_CONCEPT_CORE_INVALID
        )
        _strict(
            row,
            {"burden_id", "statement", "status"},
            "burden",
            FORMAL_CONCEPT_CORE_INVALID,
        )
        _identifier(
            row["burden_id"], "burden_id", FORMAL_CONCEPT_CORE_INVALID
        )
        _text(
            row["statement"], "burden.statement", FORMAL_CONCEPT_CORE_INVALID
        )
        if row["status"] not in {
            "open",
            "localized",
            "discharged",
            "quarantined",
        }:
            _fail("unsupported burden status", FORMAL_CONCEPT_CORE_INVALID)
        burdens.append(row)
    _unique(burdens, "burden_id", "burdens", FORMAL_CONCEPT_CORE_INVALID)
    return core


def seal_conceptual_core(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Seal and validate a finite conceptual core for transformation input."""

    payload = copy.deepcopy(
        dict(_mapping(raw, "conceptual core", FORMAL_CONCEPT_CORE_INVALID))
    )
    if "content_digest" not in payload:
        payload["content_digest"] = canonical_digest(payload)
    return _validate_core(payload, allow_free=False)


def validate_conceptual_core(
    raw: Mapping[str, Any], *, allow_free: bool = False
) -> dict[str, Any]:
    """Validate a sealed core and return a mutation-safe copy."""

    return _validate_core(raw, allow_free=allow_free)


def _validate_relation_hypothesis(
    raw: Mapping[str, Any], core: Mapping[str, Any]
) -> dict[str, Any]:
    relation = copy.deepcopy(
        dict(
            _mapping(
                raw,
                "relation hypothesis",
                FORMAL_CONCEPT_RELATION_INVALID,
            )
        )
    )
    _strict(
        relation,
        _RELATION_HYPOTHESIS_KEYS,
        "relation hypothesis",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    _identifier(
        relation["relation_id"],
        "relation_id",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    kind = relation["relation_kind"]
    if kind not in RELATION_KINDS:
        _fail("unsupported relation kind", FORMAL_CONCEPT_RELATION_INVALID)
    _text(
        relation["statement"],
        "relation.statement",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    primitive_ids = {row["primitive_id"] for row in core["primitives"]}
    source = _identifier(
        relation["source_primitive_id"],
        "source_primitive_id",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    target = _identifier(
        relation["target_primitive_id"],
        "target_primitive_id",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    if source not in primitive_ids or target not in primitive_ids:
        _fail(
            "relation hypothesis endpoints must exist in the frozen core",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    _identifiers(
        relation["premise_ids"],
        "premise_ids",
        FORMAL_CONCEPT_RELATION_INVALID,
        minimum=1,
    )
    return relation


def _validate_consequence(raw: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(
        dict(
            _mapping(
                raw,
                "consequence contract",
                FORMAL_CONCEPT_RELATION_INVALID,
            )
        )
    )
    _strict(
        result,
        _CONSEQUENCE_KEYS,
        "consequence contract",
        FORMAL_CONCEPT_RELATION_INVALID,
    )
    for field in sorted(_CONSEQUENCE_KEYS):
        _text(
            result[field],
            f"consequence.{field}",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    return result


def _validate_witness_shape(
    raw: Mapping[str, Any], kind: str
) -> dict[str, Any]:
    witness = copy.deepcopy(
        dict(_mapping(raw, "witness", FORMAL_CONCEPT_WITNESS_INVALID))
    )
    _strict(
        witness,
        _WITNESS_KEYS[kind],
        "witness",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    if witness["witness_kind"] != _WITNESS_KIND[kind]:
        _fail(
            "witness kind does not match relation kind",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        kind in HOTT_RELATION_KINDS
        and witness["construction_origin"]
        not in {
            "derived_inhabitant",
            "free_completion_counterfactual",
        }
    ):
        _fail(
            "HoTT construction origin is invalid",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    return witness


def _raw_core(core: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(core))
    result.pop("content_digest", None)
    return result


def _primitive_index(
    core: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    return {row["primitive_id"]: row for row in core["primitives"]}


def _relation_index(
    core: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    return {row["relation_id"]: row for row in core["relations"]}


def _inhabitant_index(
    core: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    return {row["inhabitant_id"]: row for row in core["inhabitants"]}


def _observable_index(
    core: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    return {row["observable_id"]: row for row in core["observables"]}


def _all_member_ids(core: Mapping[str, Any]) -> set[str]:
    return {
        member
        for row in core["primitives"]
        for member in row["member_ids"]
    }


def _add_primitive(core: dict[str, Any], raw: Mapping[str, Any]) -> str:
    row = copy.deepcopy(
        dict(_mapping(raw, "primitive", FORMAL_CONCEPT_WITNESS_INVALID))
    )
    _strict(
        row,
        {"primitive_id", "statement", "member_ids"},
        "primitive",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    primitive_id = _identifier(
        row["primitive_id"], "primitive_id", FORMAL_CONCEPT_WITNESS_INVALID
    )
    _text(
        row["statement"],
        "primitive.statement",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    members = _identifiers(
        row["member_ids"],
        "primitive.member_ids",
        FORMAL_CONCEPT_WITNESS_INVALID,
        minimum=1,
    )
    if primitive_id in _primitive_index(core):
        _fail(
            f"primitive {primitive_id} already exists",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    overlap = set(members) & _all_member_ids(core)
    if overlap:
        _fail(
            f"new primitive reuses member identifiers {sorted(overlap)}",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    core["primitives"].append(row)
    return primitive_id


def _add_relation(
    core: dict[str, Any],
    *,
    relation_id: str,
    relation_type: str,
    statement: str,
    source_primitive_id: str,
    target_primitive_id: str,
    action: Sequence[Mapping[str, Any]],
) -> str:
    relation_id = _identifier(
        relation_id, "relation_id", FORMAL_CONCEPT_WITNESS_INVALID
    )
    _identifier(
        relation_type, "relation_type", FORMAL_CONCEPT_WITNESS_INVALID
    )
    _text(
        statement, "relation.statement", FORMAL_CONCEPT_WITNESS_INVALID
    )
    if relation_id in _relation_index(core):
        _fail(
            f"relation {relation_id} already exists",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    primitives = _primitive_index(core)
    if (
        source_primitive_id not in primitives
        or target_primitive_id not in primitives
    ):
        _fail(
            "new relation endpoints are absent",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    expected_sources = list(primitives[source_primitive_id]["member_ids"])
    target_members = set(primitives[target_primitive_id]["member_ids"])
    copied_action = []
    for raw_row in action:
        row = copy.deepcopy(
            dict(
                _mapping(
                    raw_row,
                    "action row",
                    FORMAL_CONCEPT_WITNESS_INVALID,
                )
            )
        )
        _strict(
            row,
            {"source_member_id", "target_member_id"},
            "action row",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
        copied_action.append(row)
    if [row["source_member_id"] for row in copied_action] != expected_sources:
        _fail(
            "new relation action is not total in source-member order",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if any(
        row["target_member_id"] not in target_members
        for row in copied_action
    ):
        _fail(
            "new relation action leaves its target carrier",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    core["relations"].append(
        {
            "relation_id": relation_id,
            "relation_type": relation_type,
            "statement": statement,
            "source_primitive_id": source_primitive_id,
            "target_primitive_id": target_primitive_id,
            "action": copied_action,
        }
    )
    return relation_id


def _leg_relation(
    core: dict[str, Any],
    raw_leg: Mapping[str, Any],
    *,
    relation_type: str,
    source: str,
    target: str,
) -> str:
    leg = _mapping(
        raw_leg, "relation leg", FORMAL_CONCEPT_WITNESS_INVALID
    )
    _strict(
        leg,
        {"relation_id", "statement", "action"},
        "relation leg",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    return _add_relation(
        core,
        relation_id=leg["relation_id"],
        relation_type=relation_type,
        statement=leg["statement"],
        source_primitive_id=source,
        target_primitive_id=target,
        action=leg["action"],
    )


def _add_burden(
    core: dict[str, Any],
    relation: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> str:
    burden_id = stable_identifier(
        "conceptual-burden",
        core["core_id"],
        relation["relation_id"],
        consequence["changed_burden"],
    )
    if burden_id in {row["burden_id"] for row in core["burdens"]}:
        _fail(
            "derived burden identifier collides",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    core["burdens"].append(
        {
            "burden_id": burden_id,
            "statement": consequence["changed_burden"],
            "status": "open",
        }
    )
    return burden_id


def _compose_path(
    core: Mapping[str, Any], relation_ids: Sequence[str]
) -> dict[str, Any]:
    ids = _identifiers(
        relation_ids,
        "path relation ids",
        FORMAL_CONCEPT_WITNESS_INVALID,
        minimum=1,
    )
    relations = _relation_index(core)
    try:
        path = [relations[relation_id] for relation_id in ids]
    except KeyError as exc:
        _fail(
            f"path names unknown relation {exc.args[0]}",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if any(
        path[index]["target_primitive_id"]
        != path[index + 1]["source_primitive_id"]
        for index in range(len(path) - 1)
    ):
        _fail(
            "relation path is not composable",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    primitives = _primitive_index(core)
    source_members = list(
        primitives[path[0]["source_primitive_id"]]["member_ids"]
    )
    current = {member: member for member in source_members}
    for relation in path:
        action = {
            row["source_member_id"]: row["target_member_id"]
            for row in relation["action"]
        }
        current = {
            source: action[target] for source, target in current.items()
        }
    return {
        "source_primitive_id": path[0]["source_primitive_id"],
        "target_primitive_id": path[-1]["target_primitive_id"],
        "action": [
            {
                "source_member_id": source,
                "target_member_id": current[source],
            }
            for source in source_members
        ],
        "path_relation_ids": ids,
    }


def _action_dict(rows: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    return {
        row["source_member_id"]: row["target_member_id"] for row in rows
    }


def _dedupe(items: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(items))


def _check(kind: str, statement: str, evidence: Any) -> dict[str, Any]:
    digest = canonical_digest(evidence)
    return {
        "check_id": stable_identifier("concept-check", kind, digest),
        "check_kind": kind,
        "status": "passed",
        "statement": statement,
        "evidence_digest": digest,
    }


def _split(
    source_id: str, replacement_ids: Sequence[str], reason: str
) -> dict[str, Any]:
    replacements = _dedupe(list(replacement_ids))
    if len(replacements) < 2:
        _fail(
            "a conceptual split requires at least two distinct replacements",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    return {
        "split_id": stable_identifier(
            "concept-split", source_id, replacements, reason
        ),
        "entity_kind": "relation",
        "source_id": source_id,
        "replacement_ids": replacements,
        "reason": reason,
    }


def _free_path(spec: Mapping[str, Any]) -> dict[str, Any]:
    row = _mapping(
        spec, "adjoined path", FORMAL_CONCEPT_WITNESS_INVALID
    )
    expected = {
        "inhabitant_id",
        "ambient_primitive_id",
        "source_boundary_id",
        "target_boundary_id",
    }
    _strict(
        row,
        expected,
        "adjoined path",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    return {
        **copy.deepcopy(dict(row)),
        "level": 1,
        "derivation_rule": "free_adjoinment",
        "premise_inhabitant_ids": [],
        "evidence_refs": [],
    }


def _free_cell(spec: Mapping[str, Any]) -> dict[str, Any]:
    row = _mapping(
        spec, "adjoined cell", FORMAL_CONCEPT_WITNESS_INVALID
    )
    expected = {
        "inhabitant_id",
        "ambient_primitive_id",
        "source_boundary_id",
        "target_boundary_id",
    }
    _strict(
        row,
        expected,
        "adjoined cell",
        FORMAL_CONCEPT_WITNESS_INVALID,
    )
    return {
        **copy.deepcopy(dict(row)),
        "level": 2,
        "derivation_rule": "free_adjoinment",
        "premise_inhabitant_ids": [],
        "evidence_refs": [],
    }


def _boundary(row: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(row["ambient_primitive_id"]),
        str(row["source_boundary_id"]),
        str(row["target_boundary_id"]),
    )


def _resolve_paths(
    before: Mapping[str, Any],
    after: dict[str, Any],
    *,
    origin: str,
    existing_ids: Sequence[str],
    adjoined_specs: Sequence[Mapping[str, Any]],
    required_boundaries: Sequence[tuple[str, str, str]],
) -> list[str]:
    required = set(required_boundaries)
    if not required:
        _fail(
            "HoTT construction has no required path boundaries",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if origin == "derived_inhabitant":
        if adjoined_specs:
            _fail(
                "derived inhabitants cannot be supplied by free adjoinment",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        ids = _identifiers(
            existing_ids,
            "path_inhabitant_ids",
            FORMAL_CONCEPT_WITNESS_INVALID,
            minimum=1,
        )
        source = _inhabitant_index(before)
        try:
            rows = [source[identifier] for identifier in ids]
        except KeyError as exc:
            _fail(
                f"derived path {exc.args[0]} is absent from the frozen source",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        if any(
            row["level"] != 1
            or row["derivation_rule"] == "free_adjoinment"
            for row in rows
        ):
            _fail(
                "derived path set contains a non-path or free inhabitant",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
    else:
        if existing_ids:
            _fail(
                "free completion cannot relabel source inhabitants as adjoined paths",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        specs = _rows(
            adjoined_specs,
            "adjoined_paths",
            FORMAL_CONCEPT_WITNESS_INVALID,
            minimum=1,
        )
        rows = [_free_path(spec) for spec in specs]
        ids = [row["inhabitant_id"] for row in rows]
        if len(ids) != len(set(ids)):
            _fail(
                "adjoined path identifiers are duplicated",
                FORMAL_CONCEPT_WITNESS_INVALID,
            )
        occupied = set(_inhabitant_index(after))
        if occupied & set(ids):
            _fail(
                "adjoined path identifier already exists",
                FORMAL_CONCEPT_WITNESS_INVALID,
            )
        after["inhabitants"].extend(rows)
    observed = {_boundary(row) for row in rows}
    if observed != required:
        _fail(
            "path evidence does not cover the exact required boundaries",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    return ids


def _resolve_cells(
    before: Mapping[str, Any],
    after: dict[str, Any],
    *,
    origin: str,
    existing_ids: Sequence[str],
    adjoined_specs: Sequence[Mapping[str, Any]],
    selected_path_ids: Sequence[str],
) -> list[str]:
    selected = set(selected_path_ids)
    if origin == "derived_inhabitant":
        if adjoined_specs:
            _fail(
                "derived coherence cannot contain adjoined cells",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        ids = _identifiers(
            existing_ids,
            "coherence_cell_ids",
            FORMAL_CONCEPT_WITNESS_INVALID,
            minimum=1,
        )
        source = _inhabitant_index(before)
        try:
            rows = [source[identifier] for identifier in ids]
        except KeyError as exc:
            _fail(
                f"derived coherence cell {exc.args[0]} is absent from the source",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        if any(
            row["level"] != 2
            or row["derivation_rule"] == "free_adjoinment"
            for row in rows
        ):
            _fail(
                "derived coherence set contains a non-cell or free inhabitant",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
    else:
        if existing_ids:
            _fail(
                "free completion cannot relabel source cells as adjoined",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        specs = _rows(
            adjoined_specs,
            "adjoined_cells",
            FORMAL_CONCEPT_WITNESS_INVALID,
            minimum=1,
        )
        rows = [_free_cell(spec) for spec in specs]
        ids = [row["inhabitant_id"] for row in rows]
        if (
            len(ids) != len(set(ids))
            or set(ids) & set(_inhabitant_index(after))
        ):
            _fail(
                "adjoined coherence cell identifiers collide",
                FORMAL_CONCEPT_WITNESS_INVALID,
            )
        after["inhabitants"].extend(rows)
    if any(
        row["source_boundary_id"] not in selected
        or row["target_boundary_id"] not in selected
        for row in rows
    ):
        _fail(
            "coherence cells must connect selected parallel path witnesses",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    return ids


def _group_by(
    rows: Sequence[Mapping[str, Any]], field: str
) -> dict[str, list[Mapping[str, Any]]]:
    result: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        result[str(row[field])].append(row)
    return dict(result)


def _materialize_paths(
    after: dict[str, Any],
    path_ids: Sequence[str],
    cell_ids: Sequence[str],
    *,
    construction_key: str,
) -> list[str]:
    inhabitants = _inhabitant_index(after)
    path_rows = [inhabitants[path_id] for path_id in path_ids]
    relation_ids: list[str] = []
    path_member: dict[str, str] = {}
    path_primitive: dict[str, str] = {}
    for ambient, rows in sorted(
        _group_by(path_rows, "ambient_primitive_id").items()
    ):
        primitive_id = stable_identifier(
            "path-witness-object",
            construction_key,
            ambient,
            [row["inhabitant_id"] for row in rows],
        )
        members = [
            stable_identifier(
                "path-witness-member",
                construction_key,
                row["inhabitant_id"],
            )
            for row in rows
        ]
        _add_primitive(
            after,
            {
                "primitive_id": primitive_id,
                "statement": (
                    f"Explicit selected path witnesses in ambient primitive {ambient}."
                ),
                "member_ids": members,
            },
        )
        path_primitive[ambient] = primitive_id
        for row, member in zip(rows, members, strict=True):
            path_member[row["inhabitant_id"]] = member
        for boundary_name in ("source", "target"):
            relation_id = stable_identifier(
                "path-boundary-map",
                construction_key,
                ambient,
                boundary_name,
                members,
            )
            relation_ids.append(
                _add_relation(
                    after,
                    relation_id=relation_id,
                    relation_type=f"path_{boundary_name}_boundary",
                    statement=(
                        f"Map each selected path witness to its {boundary_name} boundary."
                    ),
                    source_primitive_id=primitive_id,
                    target_primitive_id=ambient,
                    action=[
                        {
                            "source_member_id": member,
                            "target_member_id": row[
                                f"{boundary_name}_boundary_id"
                            ],
                        }
                        for row, member in zip(rows, members, strict=True)
                    ],
                )
            )
    cell_rows = [inhabitants[cell_id] for cell_id in cell_ids]
    for ambient, rows in sorted(
        _group_by(cell_rows, "ambient_primitive_id").items()
    ):
        primitive_id = stable_identifier(
            "coherence-cell-object",
            construction_key,
            ambient,
            [row["inhabitant_id"] for row in rows],
        )
        members = [
            stable_identifier(
                "coherence-cell-member",
                construction_key,
                row["inhabitant_id"],
            )
            for row in rows
        ]
        _add_primitive(
            after,
            {
                "primitive_id": primitive_id,
                "statement": (
                    f"Explicit level-2 coherence cells in ambient primitive {ambient}."
                ),
                "member_ids": members,
            },
        )
        for boundary_name in ("source", "target"):
            relation_id = stable_identifier(
                "cell-boundary-map",
                construction_key,
                ambient,
                boundary_name,
                members,
            )
            relation_ids.append(
                _add_relation(
                    after,
                    relation_id=relation_id,
                    relation_type=f"cell_{boundary_name}_boundary",
                    statement=(
                        f"Map each coherence cell to its {boundary_name} path boundary."
                    ),
                    source_primitive_id=primitive_id,
                    target_primitive_id=path_primitive[ambient],
                    action=[
                        {
                            "source_member_id": member,
                            "target_member_id": path_member[
                                row[f"{boundary_name}_boundary_id"]
                            ],
                        }
                        for row, member in zip(rows, members, strict=True)
                    ],
                )
            )
    return relation_ids


def _algorithm_noncommuting(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    left = _compose_path(after, witness["left_path_relation_ids"])
    right = _compose_path(after, witness["right_path_relation_ids"])
    if (
        left["source_primitive_id"] != right["source_primitive_id"]
        or left["target_primitive_id"] != right["target_primitive_id"]
        or left["source_primitive_id"] != relation["source_primitive_id"]
        or left["target_primitive_id"] != relation["target_primitive_id"]
    ):
        _fail(
            "noncommuting paths do not share the relation-hypothesis boundary",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    left_action = _action_dict(left["action"])
    right_action = _action_dict(right["action"])
    disagreements = [
        source
        for source in left_action
        if left_action[source] != right_action[source]
    ]
    if not disagreements:
        _fail(
            "noncommutativity localization requires an exact disagreement",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    primitive_id = stable_identifier(
        "noncommuting-obstruction",
        before["content_digest"],
        relation,
        witness,
    )
    members = [
        stable_identifier("noncommuting-case", primitive_id, source)
        for source in disagreements
    ]
    _add_primitive(
        after,
        {
            "primitive_id": primitive_id,
            "statement": (
                "Finite members at which the two declared composites disagree."
            ),
            "member_ids": members,
        },
    )
    trace_ids = []
    for side, action in (("left", left_action), ("right", right_action)):
        trace_ids.append(
            _add_relation(
                after,
                relation_id=stable_identifier(
                    "noncommuting-trace", primitive_id, side
                ),
                relation_type=f"{side}_localized_trace",
                statement=(
                    f"Localized {side} output of the noncommuting composite."
                ),
                source_primitive_id=primitive_id,
                target_primitive_id=left["target_primitive_id"],
                action=[
                    {
                        "source_member_id": member,
                        "target_member_id": action[source],
                    }
                    for member, source in zip(
                        members, disagreements, strict=True
                    )
                ],
            )
        )
    burden_id = _add_burden(after, relation, consequence)
    evidence = {
        source: {
            "left": left_action[source],
            "right": right_action[source],
        }
        for source in disagreements
    }
    return {
        "after": after,
        "origin": "derived_finite_witness",
        "base_outcome": "localized",
        "burden_id": burden_id,
        "required_relations": _dedupe(
            left["path_relation_ids"] + right["path_relation_ids"]
        ),
        "required_paths": [],
        "checks": [
            _check(
                "parallel_path_boundary",
                "Both paths have the exact same typed source and target.",
                [
                    left["source_primitive_id"],
                    left["target_primitive_id"],
                ],
            ),
            _check(
                "noncommuting_action_replay",
                "At least one finite source member has unequal composite outputs.",
                evidence,
            ),
            _check(
                "obstruction_localization",
                "Every disagreement is materialized without quotienting either output.",
                trace_ids,
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                trace_ids,
                "Separate the two noncommuting route outputs at their finite witnessed disagreement.",
            )
        ],
    }


def _algorithm_mediator(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    direct = _relation_index(after).get(witness["direct_relation_id"])
    if direct is None:
        _fail(
            "mediator witness names an unknown direct relation",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        direct["source_primitive_id"] != relation["source_primitive_id"]
        or direct["target_primitive_id"] != relation["target_primitive_id"]
    ):
        _fail(
            "direct relation does not match the factorization hypothesis",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    mediator_id = _add_primitive(after, witness["mediator"])
    first_id = _leg_relation(
        after,
        witness["first_leg"],
        relation_type="mediator_first_leg",
        source=direct["source_primitive_id"],
        target=mediator_id,
    )
    second_id = _leg_relation(
        after,
        witness["second_leg"],
        relation_type="mediator_second_leg",
        source=mediator_id,
        target=direct["target_primitive_id"],
    )
    factored = _compose_path(after, [first_id, second_id])
    if factored["action"] != direct["action"]:
        _fail(
            "mediator legs do not compose to the direct finite action",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    burden_id = _add_burden(after, relation, consequence)
    return {
        "after": after,
        "origin": "derived_finite_witness",
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": [first_id, second_id],
        "required_paths": [],
        "checks": [
            _check(
                "factorization_boundary",
                "The two legs are typed through one explicit mediator.",
                [
                    direct["source_primitive_id"],
                    mediator_id,
                    direct["target_primitive_id"],
                ],
            ),
            _check(
                "factorization_action_replay",
                "The leg composite equals the direct action on every finite member.",
                [direct["action"], factored["action"]],
            ),
            _check(
                "mediator_materialization",
                "The mediator and both legs are present in the after core.",
                [mediator_id, first_id, second_id],
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                [first_id, second_id],
                "Replace one opaque direct burden by two independently typed mediator legs.",
            )
        ],
    }


def _algorithm_functorial(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    source_relation = _relation_index(after).get(
        witness["source_relation_id"]
    )
    if source_relation is None:
        _fail(
            "functorial witness names an unknown source relation",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        source_relation["source_primitive_id"]
        != relation["source_primitive_id"]
        or source_relation["target_primitive_id"]
        != relation["target_primitive_id"]
    ):
        _fail(
            "source relation does not match the transfer hypothesis",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    transferred_source = _add_primitive(
        after, witness["transferred_source"]
    )
    transferred_target = _add_primitive(
        after, witness["transferred_target"]
    )
    source_component = _leg_relation(
        after,
        witness["source_component"],
        relation_type="functor_source_component",
        source=source_relation["source_primitive_id"],
        target=transferred_source,
    )
    target_component = _leg_relation(
        after,
        witness["target_component"],
        relation_type="functor_target_component",
        source=source_relation["target_primitive_id"],
        target=transferred_target,
    )
    transferred_relation = _leg_relation(
        after,
        witness["transferred_relation"],
        relation_type="transferred_relation",
        source=transferred_source,
        target=transferred_target,
    )
    left = _compose_path(
        after, [source_relation["relation_id"], target_component]
    )
    right = _compose_path(
        after, [source_component, transferred_relation]
    )
    if left["action"] != right["action"]:
        _fail(
            "functorial naturality square does not commute pointwise",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    burden_id = _add_burden(after, relation, consequence)
    return {
        "after": after,
        "origin": "derived_finite_witness",
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": [
            source_component,
            transferred_relation,
            target_component,
        ],
        "required_paths": [],
        "checks": [
            _check(
                "functorial_boundary",
                "Source and target components form a typed transfer square.",
                [
                    source_relation["relation_id"],
                    source_component,
                    target_component,
                    transferred_relation,
                ],
            ),
            _check(
                "naturality_action_replay",
                "Both routes around the transfer square agree on every finite source member.",
                [left["action"], right["action"]],
            ),
            _check(
                "transfer_materialization",
                "Transferred source, target, and relation are explicit after-core entities.",
                [
                    transferred_source,
                    transferred_target,
                    transferred_relation,
                ],
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                [
                    source_component,
                    transferred_relation,
                    target_component,
                ],
                "Separate representation change, relation transport, and target comparison.",
            )
        ],
    }


def _required_boundaries_from_action(
    relation: Mapping[str, Any],
) -> list[tuple[str, str, str]]:
    if (
        relation["source_primitive_id"]
        != relation["target_primitive_id"]
    ):
        _fail(
            "identity transport must be an endorelation on one primitive",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    ambient = relation["source_primitive_id"]
    return [
        (
            ambient,
            row["source_member_id"],
            row["target_member_id"],
        )
        for row in relation["action"]
    ]


def _algorithm_identity_transport(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    transport = _relation_index(after).get(
        witness["transport_relation_id"]
    )
    if transport is None:
        _fail(
            "identity-transport witness names an unknown relation",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        transport["source_primitive_id"]
        != relation["source_primitive_id"]
        or transport["target_primitive_id"]
        != relation["target_primitive_id"]
        or relation["source_primitive_id"]
        != relation["target_primitive_id"]
    ):
        _fail(
            "identity transport and relation hypothesis have different boundaries",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    required = _required_boundaries_from_action(transport)
    paths = _resolve_paths(
        before,
        after,
        origin=witness["construction_origin"],
        existing_ids=witness["path_inhabitant_ids"],
        adjoined_specs=witness["adjoined_paths"],
        required_boundaries=required,
    )
    material = _materialize_paths(
        after,
        paths,
        [],
        construction_key=stable_identifier(
            "identity-transport",
            before["content_digest"],
            relation,
            witness,
        ),
    )
    burden_id = _add_burden(after, relation, consequence)
    return {
        "after": after,
        "origin": witness["construction_origin"],
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": [transport["relation_id"]],
        "required_paths": paths,
        "checks": [
            _check(
                "identity_transport_boundary",
                "Every finite transport action has one explicit path boundary.",
                required,
            ),
            _check(
                "identity_transport_origin",
                "Path inhabitants are frozen-source derivations or explicit free counterfactuals.",
                [witness["construction_origin"], paths],
            ),
            _check(
                "identity_transport_materialization",
                "Selected paths have explicit source and target boundary maps.",
                material,
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                material[:2],
                "Separate strict endomap action from explicit identity-path boundaries.",
            )
        ],
    }


def _composite_boundaries(
    core: Mapping[str, Any], first_id: str, second_id: str
) -> tuple[list[tuple[str, str, str]], dict[str, Any]]:
    composite = _compose_path(core, [first_id, second_id])
    return (
        [
            (
                composite["source_primitive_id"],
                row["source_member_id"],
                row["target_member_id"],
            )
            for row in composite["action"]
        ],
        composite,
    )


def _algorithm_equivalence(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    relations = _relation_index(after)
    forward = relations.get(witness["forward_relation_id"])
    inverse = relations.get(witness["inverse_relation_id"])
    if forward is None or inverse is None:
        _fail(
            "equivalence witness lacks a declared forward or inverse map",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        forward["source_primitive_id"]
        != relation["source_primitive_id"]
        or forward["target_primitive_id"]
        != relation["target_primitive_id"]
        or inverse["source_primitive_id"]
        != forward["target_primitive_id"]
        or inverse["target_primitive_id"]
        != forward["source_primitive_id"]
    ):
        _fail(
            "forward/inverse maps do not type the hypothesized equivalence",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    left_required, left_composite = _composite_boundaries(
        after, forward["relation_id"], inverse["relation_id"]
    )
    right_required, right_composite = _composite_boundaries(
        after, inverse["relation_id"], forward["relation_id"]
    )
    origin = witness["construction_origin"]
    if origin == "derived_inhabitant":
        if witness["adjoined_paths"] or witness["adjoined_cells"]:
            _fail(
                "derived equivalence coherence cannot adjoin paths or cells",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        left_paths = _resolve_paths(
            before,
            after,
            origin=origin,
            existing_ids=witness["left_path_inhabitant_ids"],
            adjoined_specs=[],
            required_boundaries=left_required,
        )
        right_paths = _resolve_paths(
            before,
            after,
            origin=origin,
            existing_ids=witness["right_path_inhabitant_ids"],
            adjoined_specs=[],
            required_boundaries=right_required,
        )
    else:
        if (
            witness["left_path_inhabitant_ids"]
            or witness["right_path_inhabitant_ids"]
        ):
            _fail(
                "free equivalence completion cannot relabel source paths",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        all_paths = _resolve_paths(
            before,
            after,
            origin=origin,
            existing_ids=[],
            adjoined_specs=witness["adjoined_paths"],
            required_boundaries=left_required + right_required,
        )
        rows = _inhabitant_index(after)
        left_boundary_set = set(left_required)
        left_paths = [
            path_id
            for path_id in all_paths
            if _boundary(rows[path_id]) in left_boundary_set
        ]
        right_paths = [
            path_id
            for path_id in all_paths
            if path_id not in set(left_paths)
        ]
    selected_paths = left_paths + right_paths
    cells = _resolve_cells(
        before,
        after,
        origin=origin,
        existing_ids=witness["coherence_cell_ids"],
        adjoined_specs=witness["adjoined_cells"],
        selected_path_ids=selected_paths,
    )
    material = _materialize_paths(
        after,
        selected_paths,
        cells,
        construction_key=stable_identifier(
            "equivalence-coherence",
            before["content_digest"],
            relation,
            witness,
        ),
    )
    burden_id = _add_burden(after, relation, consequence)
    return {
        "after": after,
        "origin": origin,
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": [
            forward["relation_id"],
            inverse["relation_id"],
        ],
        "required_paths": selected_paths,
        "checks": [
            _check(
                "equivalence_inverse_boundaries",
                "Both inverse composites have explicit path inhabitants on every finite member.",
                [left_required, right_required],
            ),
            _check(
                "equivalence_coherence_cells",
                "Explicit level-2 cells compare selected parallel inverse paths.",
                cells,
            ),
            _check(
                "equivalence_not_identity",
                "Forward, inverse, path, and coherence data remain separately materialized.",
                [
                    forward["relation_id"],
                    inverse["relation_id"],
                    left_composite,
                    right_composite,
                    material,
                ],
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                [
                    forward["relation_id"],
                    inverse["relation_id"],
                    *material,
                ],
                "Separate equivalence maps, path homotopies, and level-2 coherence.",
            )
        ],
    }


def _parallel_boundaries(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> list[tuple[str, str, str]]:
    if (
        left["source_primitive_id"] != right["source_primitive_id"]
        or left["target_primitive_id"] != right["target_primitive_id"]
    ):
        _fail(
            "parallel-path witness lacks a common typed boundary",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    left_action = _action_dict(left["action"])
    right_action = _action_dict(right["action"])
    return [
        (
            left["target_primitive_id"],
            left_action[source],
            right_action[source],
        )
        for source in left_action
    ]


def _algorithm_path_independence(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    left = _compose_path(after, witness["left_path_relation_ids"])
    right = _compose_path(after, witness["right_path_relation_ids"])
    if (
        left["source_primitive_id"] != relation["source_primitive_id"]
        or left["target_primitive_id"] != relation["target_primitive_id"]
    ):
        _fail(
            "path-independence routes do not match the hypothesis boundary",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    boundaries = _parallel_boundaries(left, right)
    paths = _resolve_paths(
        before,
        after,
        origin=witness["construction_origin"],
        existing_ids=witness["path_inhabitant_ids"],
        adjoined_specs=witness["adjoined_paths"],
        required_boundaries=boundaries,
    )
    material = _materialize_paths(
        after,
        paths,
        [],
        construction_key=stable_identifier(
            "path-independence",
            before["content_digest"],
            relation,
            witness,
        ),
    )
    burden_id = _add_burden(after, relation, consequence)
    replacements = _dedupe(
        left["path_relation_ids"] + right["path_relation_ids"]
    )
    if len(replacements) < 2:
        _fail(
            "path independence requires two structurally distinct paths",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    return {
        "after": after,
        "origin": witness["construction_origin"],
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": replacements,
        "required_paths": paths,
        "checks": [
            _check(
                "path_independence_boundary",
                "Both relation paths share an exact finite source and target.",
                [
                    left["source_primitive_id"],
                    left["target_primitive_id"],
                ],
            ),
            _check(
                "path_inhabitant_coverage",
                "Every pair of route outputs has an explicit path witness.",
                boundaries,
            ),
            _check(
                "path_choice_materialization",
                "Route actions and path boundaries remain separately inspectable.",
                [replacements, material],
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                replacements,
                "Retain both route choices and compare outputs by explicit paths.",
            )
        ],
    }


def _algorithm_descent(
    before: Mapping[str, Any],
    relation: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence: Mapping[str, Any],
) -> dict[str, Any]:
    after = _raw_core(before)
    relations = _relation_index(after)
    left = relations.get(witness["left_restriction_relation_id"])
    right = relations.get(witness["right_restriction_relation_id"])
    if left is None or right is None:
        _fail(
            "descent witness names an unknown restriction map",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if left["target_primitive_id"] != right["target_primitive_id"]:
        _fail(
            "descent restrictions do not land in one overlap primitive",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    if (
        relation["source_primitive_id"]
        != left["source_primitive_id"]
        or relation["target_primitive_id"]
        != left["target_primitive_id"]
    ):
        _fail(
            "descent hypothesis must bind the left-local to overlap interface",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
    pair_rows = []
    required_boundaries = []
    seen_pairs: set[tuple[str, str]] = set()
    left_action = _action_dict(left["action"])
    right_action = _action_dict(right["action"])
    for index, raw_pair in enumerate(
        _rows(
            witness["compatible_pairs"],
            "compatible_pairs",
            FORMAL_CONCEPT_WITNESS_INVALID,
            minimum=1,
        )
    ):
        pair = copy.deepcopy(
            dict(
                _mapping(
                    raw_pair,
                    f"compatible_pairs[{index}]",
                    FORMAL_CONCEPT_WITNESS_INVALID,
                )
            )
        )
        _strict(
            pair,
            {
                "pair_id",
                "left_member_id",
                "right_member_id",
                "path_inhabitant_id",
            },
            "compatible pair",
            FORMAL_CONCEPT_WITNESS_INVALID,
        )
        for field in (
            "pair_id",
            "left_member_id",
            "right_member_id",
            "path_inhabitant_id",
        ):
            _identifier(
                pair[field], field, FORMAL_CONCEPT_WITNESS_INVALID
            )
        local_pair = (
            pair["left_member_id"],
            pair["right_member_id"],
        )
        if local_pair in seen_pairs:
            _fail(
                "descent compatible local pair is duplicated",
                FORMAL_CONCEPT_WITNESS_INVALID,
            )
        seen_pairs.add(local_pair)
        if (
            pair["left_member_id"] not in left_action
            or pair["right_member_id"] not in right_action
        ):
            _fail(
                "descent pair leaves a declared local carrier",
                FORMAL_CONCEPT_WITNESS_INVALID,
            )
        required_boundaries.append(
            (
                left["target_primitive_id"],
                left_action[pair["left_member_id"]],
                right_action[pair["right_member_id"]],
            )
        )
        pair_rows.append(pair)
    origin = witness["construction_origin"]
    if origin == "derived_inhabitant":
        if witness["adjoined_paths"]:
            _fail(
                "derived descent cannot adjoin overlap paths",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        resolved = _resolve_paths(
            before,
            after,
            origin=origin,
            existing_ids=[
                row["path_inhabitant_id"] for row in pair_rows
            ],
            adjoined_specs=[],
            required_boundaries=required_boundaries,
        )
    else:
        path_ids = [
            row["path_inhabitant_id"] for row in pair_rows
        ]
        spec_ids = [
            row["inhabitant_id"] for row in witness["adjoined_paths"]
        ]
        if path_ids != spec_ids:
            _fail(
                "free descent paths must follow adjoined-path order",
                FREE_COMPLETION_PROMOTION_INVALID,
            )
        resolved = _resolve_paths(
            before,
            after,
            origin=origin,
            existing_ids=[],
            adjoined_specs=witness["adjoined_paths"],
            required_boundaries=required_boundaries,
        )
    descent_primitive = stable_identifier(
        "descent-compatible-pairs",
        before["content_digest"],
        relation,
        witness,
    )
    pair_members = [row["pair_id"] for row in pair_rows]
    _add_primitive(
        after,
        {
            "primitive_id": descent_primitive,
            "statement": (
                "Local pairs equipped with explicit overlap path inhabitants."
            ),
            "member_ids": pair_members,
        },
    )
    projection_ids = []
    for side, target, member_field in (
        ("left", left["source_primitive_id"], "left_member_id"),
        ("right", right["source_primitive_id"], "right_member_id"),
    ):
        projection_ids.append(
            _add_relation(
                after,
                relation_id=stable_identifier(
                    "descent-projection", descent_primitive, side
                ),
                relation_type=f"descent_{side}_projection",
                statement=(
                    f"Project a coherent descent pair to its {side} component."
                ),
                source_primitive_id=descent_primitive,
                target_primitive_id=target,
                action=[
                    {
                        "source_member_id": row["pair_id"],
                        "target_member_id": row[member_field],
                    }
                    for row in pair_rows
                ],
            )
        )
    material = _materialize_paths(
        after,
        resolved,
        [],
        construction_key=stable_identifier(
            "descent-coherence",
            before["content_digest"],
            relation,
            witness,
        ),
    )
    burden_id = _add_burden(after, relation, consequence)
    return {
        "after": after,
        "origin": origin,
        "base_outcome": "constructively_removed",
        "burden_id": burden_id,
        "required_relations": [
            left["relation_id"],
            right["relation_id"],
        ],
        "required_paths": resolved,
        "checks": [
            _check(
                "descent_overlap_boundary",
                "Both restriction maps land in one overlap primitive.",
                left["target_primitive_id"],
            ),
            _check(
                "descent_compatible_pairs",
                "Every retained local pair carries an overlap path inhabitant.",
                [pair_rows, required_boundaries],
            ),
            _check(
                "descent_projection_materialization",
                "Descent object, projections, and overlap paths are explicit.",
                [descent_primitive, projection_ids, material],
            ),
        ],
        "splits": [
            _split(
                relation["relation_id"],
                [
                    *projection_ids,
                    left["relation_id"],
                    right["relation_id"],
                ],
                "Separate local data, restrictions, paths, and projections.",
            )
        ],
    }


_ALGORITHMS = {
    "noncommuting_composition": _algorithm_noncommuting,
    "mediating_factorization": _algorithm_mediator,
    "functorial_transfer": _algorithm_functorial,
    "identity_transport": _algorithm_identity_transport,
    "equivalence_coherence": _algorithm_equivalence,
    "path_independence": _algorithm_path_independence,
    "descent_coherence": _algorithm_descent,
}


def _value_key(value: Any) -> bytes:
    return canonical_json(value)


def _receipt(raw: Mapping[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(dict(raw))
    payload["receipt_id"] = stable_identifier(
        "observable-preservation", payload
    )
    return _seal(payload, "receipt_digest")


def _audit_observable_preservation(
    before: Mapping[str, Any],
    after: dict[str, Any],
    required_relation_ids: Sequence[str],
    required_path_ids: Sequence[str],
) -> dict[str, Any]:
    receipts: list[dict[str, Any]] = []
    before_observables = _observable_index(before)
    after_observables = _observable_index(after)
    for observable_id, observable in before_observables.items():
        if not observable["protected"]:
            continue
        retained = after_observables.get(observable_id)
        if (
            retained is None
            or canonical_json(retained) != canonical_json(observable)
        ):
            _fail(
                "constructor removed or modified a protected source observable",
                FORMAL_CONCEPT_PRESERVATION_INVALID,
            )
        receipts.append(
            _receipt(
                {
                    "receipt_kind": "identity_retention",
                    "source_observable_id": observable_id,
                    "target_observable_id": observable_id,
                    "map_or_inhabitant_id": f"identity:{observable_id}",
                    "source_primitive_id": observable[
                        "carrier_primitive_id"
                    ],
                    "target_primitive_id": observable[
                        "carrier_primitive_id"
                    ],
                    "checked_pairs": len(observable["evaluations"]),
                    "value_preserved": True,
                    "protected_distinctions_preserved": True,
                    "counterexamples": [],
                }
            )
        )

    for relation_id in _dedupe(list(required_relation_ids)):
        relation = _relation_index(after).get(relation_id)
        if relation is None:
            _fail(
                "preservation audit names an absent relation",
                FORMAL_CONCEPT_PRESERVATION_INVALID,
            )
        source_observables = [
            row
            for row in after["observables"]
            if row["protected"]
            and row["carrier_primitive_id"]
            == relation["source_primitive_id"]
        ]
        if not source_observables:
            _fail(
                f"required relation {relation_id} has no protected source observable",
                FORMAL_CONCEPT_PRESERVATION_INVALID,
            )
        action = _action_dict(relation["action"])
        target_members = list(
            _primitive_index(after)[
                relation["target_primitive_id"]
            ]["member_ids"]
        )
        for observable in list(source_observables):
            values = {
                row["member_id"]: row["value"]
                for row in observable["evaluations"]
            }
            fibers: dict[str, list[str]] = defaultdict(list)
            for source_member, target_member in action.items():
                fibers[target_member].append(source_member)
            counterexamples = []
            for target_member, source_members in fibers.items():
                distinct = []
                seen: set[bytes] = set()
                for source_member in source_members:
                    value = values[source_member]
                    key = _value_key(value)
                    if key not in seen:
                        seen.add(key)
                        distinct.append(value)
                if len(distinct) > 1:
                    counterexamples.append(
                        {
                            "counterexample_id": stable_identifier(
                                "protected-value-collision",
                                relation_id,
                                observable["observable_id"],
                                target_member,
                                source_members,
                                distinct,
                            ),
                            "reason_code": "protected_value_collision",
                            "source_member_ids": source_members,
                            "target_member_ids": [target_member],
                            "source_values": [
                                values[source_member]
                                for source_member in source_members
                            ],
                            "target_values": [None],
                        }
                    )
            target_observable_id: str | None = None
            if not counterexamples:
                target_observable_id = stable_identifier(
                    "transported-observable",
                    observable["observable_id"],
                    relation_id,
                    relation["action"],
                )
                evaluations = []
                for target_member in target_members:
                    source_members = fibers.get(target_member, [])
                    value = (
                        values[source_members[0]]
                        if source_members
                        else (
                            f"unconstrained:{observable['observable_id']}:"
                            f"{target_member}"
                        )
                    )
                    evaluations.append(
                        {"member_id": target_member, "value": value}
                    )
                target_observable = {
                    "observable_id": target_observable_id,
                    "carrier_primitive_id": relation[
                        "target_primitive_id"
                    ],
                    "statement": (
                        f"Protected transport of {observable['observable_id']} "
                        f"along {relation_id}."
                    ),
                    "protected": True,
                    "evaluations": evaluations,
                }
                existing = _observable_index(after).get(
                    target_observable_id
                )
                if existing is None:
                    after["observables"].append(target_observable)
                elif canonical_json(existing) != canonical_json(
                    target_observable
                ):
                    _fail(
                        "transported observable identifier collides",
                        FORMAL_CONCEPT_PRESERVATION_INVALID,
                    )
            receipts.append(
                _receipt(
                    {
                        "receipt_kind": "relation_transport",
                        "source_observable_id": observable[
                            "observable_id"
                        ],
                        "target_observable_id": target_observable_id,
                        "map_or_inhabitant_id": relation_id,
                        "source_primitive_id": relation[
                            "source_primitive_id"
                        ],
                        "target_primitive_id": relation[
                            "target_primitive_id"
                        ],
                        "checked_pairs": len(relation["action"]),
                        "value_preserved": not counterexamples,
                        "protected_distinctions_preserved": not counterexamples,
                        "counterexamples": counterexamples,
                    }
                )
            )

    inhabitants = _inhabitant_index(after)
    for path_id in _dedupe(list(required_path_ids)):
        path = inhabitants.get(path_id)
        if path is None or path["level"] != 1:
            _fail(
                "path preservation audit names an absent level-1 inhabitant",
                FORMAL_CONCEPT_PRESERVATION_INVALID,
            )
        path_observables = [
            row
            for row in after["observables"]
            if row["protected"]
            and row["carrier_primitive_id"]
            == path["ambient_primitive_id"]
        ]
        if not path_observables:
            _fail(
                "required path has no protected ambient observable",
                FORMAL_CONCEPT_PRESERVATION_INVALID,
            )
        for observable in path_observables:
            values = {
                row["member_id"]: row["value"]
                for row in observable["evaluations"]
            }
            source_value = values[path["source_boundary_id"]]
            target_value = values[path["target_boundary_id"]]
            equal = _value_key(source_value) == _value_key(target_value)
            counterexamples = []
            if not equal:
                counterexamples.append(
                    {
                        "counterexample_id": stable_identifier(
                            "path-observable-mismatch",
                            path_id,
                            observable["observable_id"],
                            source_value,
                            target_value,
                        ),
                        "reason_code": "path_boundary_value_mismatch",
                        "source_member_ids": [
                            path["source_boundary_id"]
                        ],
                        "target_member_ids": [
                            path["target_boundary_id"]
                        ],
                        "source_values": [source_value],
                        "target_values": [target_value],
                    }
                )
            receipts.append(
                _receipt(
                    {
                        "receipt_kind": "path_boundary",
                        "source_observable_id": observable[
                            "observable_id"
                        ],
                        "target_observable_id": observable[
                            "observable_id"
                        ],
                        "map_or_inhabitant_id": path_id,
                        "source_primitive_id": path[
                            "ambient_primitive_id"
                        ],
                        "target_primitive_id": path[
                            "ambient_primitive_id"
                        ],
                        "checked_pairs": 1,
                        "value_preserved": equal,
                        "protected_distinctions_preserved": equal,
                        "counterexamples": counterexamples,
                    }
                )
            )
    failures = [
        counterexample
        for receipt in receipts
        for counterexample in receipt["counterexamples"]
    ]
    all_preserve = all(
        receipt["value_preserved"]
        and receipt["protected_distinctions_preserved"]
        for receipt in receipts
    )
    return {
        "status": (
            "preserved"
            if all_preserve
            else "quarantined_protected_erasure"
        ),
        "required_relation_ids": _dedupe(list(required_relation_ids)),
        "required_path_inhabitant_ids": _dedupe(
            list(required_path_ids)
        ),
        "receipts": receipts,
        "all_source_protected_observables_retained": True,
        "all_required_maps_preserve": all_preserve,
        "protected_erasure_detected": not all_preserve,
        "counterexamples_digest": canonical_digest(failures),
    }


def _diff_rows(
    before: Sequence[Mapping[str, Any]],
    after: Sequence[Mapping[str, Any]],
    key: str,
) -> tuple[list[str], list[str], list[str]]:
    left = {row[key]: row for row in before}
    right = {row[key]: row for row in after}
    added = sorted(set(right) - set(left))
    removed = sorted(set(left) - set(right))
    modified = sorted(
        identifier
        for identifier in set(left) & set(right)
        if canonical_json(left[identifier])
        != canonical_json(right[identifier])
    )
    return added, removed, modified


def _loss_ledger(
    relation: Mapping[str, Any],
    preservation: Mapping[str, Any],
    origin: str,
    outcome: str,
) -> list[dict[str, Any]]:
    losses: list[dict[str, Any]] = []
    failed_receipts = [
        receipt
        for receipt in preservation["receipts"]
        if not receipt["value_preserved"]
        or not receipt["protected_distinctions_preserved"]
    ]
    for receipt in failed_receipts:
        losses.append(
            {
                "loss_id": stable_identifier(
                    "concept-loss",
                    relation["relation_id"],
                    receipt["receipt_id"],
                ),
                "statement": (
                    f"Protected observable {receipt['source_observable_id']} "
                    f"is erased or changed by "
                    f"{receipt['map_or_inhabitant_id']}."
                ),
                "protected": True,
                "disposition": "quarantined",
            }
        )
    if origin == "free_completion_counterfactual":
        losses.append(
            {
                "loss_id": stable_identifier(
                    "concept-loss",
                    relation["relation_id"],
                    "free-completion",
                ),
                "statement": (
                    "Path or coherence inhabitation is freely adjoined rather "
                    "than derived from the frozen source core."
                ),
                "protected": False,
                "disposition": "counterfactual_only",
            }
        )
    if not failed_receipts:
        losses.append(
            {
                "loss_id": stable_identifier(
                    "concept-loss",
                    relation["relation_id"],
                    "no-protected-erasure",
                ),
                "statement": (
                    "No protected finite observable distinction is erased by "
                    "the executable maps."
                ),
                "protected": False,
                "disposition": "none_detected",
            }
        )
    losses.append(
        {
            "loss_id": stable_identifier(
                "concept-loss",
                relation["relation_id"],
                "authority-limit",
                outcome,
            ),
            "statement": (
                "Universal, continuum, theorem, truth, and physics-value "
                "consequences remain open outside this finite transformation."
            ),
            "protected": False,
            "disposition": "retained_open",
        }
    )
    return losses


def _construct_internal(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness_raw: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
    *,
    expected_lens: str,
) -> dict[str, Any]:
    before = _validate_core(source_core, allow_free=False)
    relation = _validate_relation_hypothesis(
        relation_hypothesis, before
    )
    consequence = _validate_consequence(consequence_contract)
    kind = relation["relation_kind"]
    lens = "categorical" if kind in CATEGORY_RELATION_KINDS else "hott"
    if lens != expected_lens:
        _fail(
            f"{kind} is not a {expected_lens} relation",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    witness = _validate_witness_shape(witness_raw, kind)
    artifacts = _ALGORITHMS[kind](
        before, relation, witness, consequence
    )
    after_raw = artifacts["after"]
    after_raw["core_id"] = stable_identifier(
        "transformed-concept-core",
        before["core_id"],
        relation,
        witness,
        consequence,
    )
    preservation = _audit_observable_preservation(
        before,
        after_raw,
        artifacts["required_relations"],
        artifacts["required_paths"],
    )
    if preservation["protected_erasure_detected"]:
        after_status = "quarantined_protected_erasure"
        reason_code = "protected_observable_erasure"
        removal_authorized = False
        decision_flip_authorized = False
        burden_status = "quarantined"
    elif artifacts["origin"] == "free_completion_counterfactual":
        after_status = "counterfactual_only"
        reason_code = "free_completion_has_no_inhabitation_authority"
        removal_authorized = False
        decision_flip_authorized = False
        burden_status = "open"
    elif artifacts["base_outcome"] == "localized":
        after_status = "localized"
        reason_code = "exact_obstruction_localized_not_removed"
        removal_authorized = False
        decision_flip_authorized = False
        burden_status = "localized"
    else:
        after_status = "constructively_removed"
        reason_code = "exact_relation_specific_construction"
        removal_authorized = True
        decision_flip_authorized = True
        burden_status = "discharged"
    for burden in after_raw["burdens"]:
        if burden["burden_id"] == artifacts["burden_id"]:
            burden["status"] = burden_status
            break
    else:
        _fail(
            "derived burden disappeared before sealing",
            FORMAL_CONCEPT_REPLAY_INVALID,
        )
    after_raw["content_digest"] = canonical_digest(after_raw)
    after = _validate_core(after_raw, allow_free=True)

    primitive_delta = _diff_rows(
        before["primitives"], after["primitives"], "primitive_id"
    )
    relation_delta = _diff_rows(
        before["relations"], after["relations"], "relation_id"
    )
    observable_delta = _diff_rows(
        before["observables"], after["observables"], "observable_id"
    )
    inhabitant_delta = _diff_rows(
        before["inhabitants"],
        after["inhabitants"],
        "inhabitant_id",
    )
    losses = _loss_ledger(
        relation, preservation, artifacts["origin"], after_status
    )
    semantic_delta = {
        "added_primitive_ids": primitive_delta[0],
        "removed_primitive_ids": primitive_delta[1],
        "modified_primitive_ids": primitive_delta[2],
        "added_relation_ids": relation_delta[0],
        "removed_relation_ids": relation_delta[1],
        "modified_relation_ids": relation_delta[2],
        "added_observable_ids": observable_delta[0],
        "removed_observable_ids": observable_delta[1],
        "modified_observable_ids": observable_delta[2],
        "added_inhabitant_ids": inhabitant_delta[0],
        "removed_inhabitant_ids": inhabitant_delta[1],
        "modified_inhabitant_ids": inhabitant_delta[2],
        "splits": artifacts["splits"],
        "explanatory_gain": consequence["explanatory_gain"],
        "loss_ledger": losses,
        "new_question": consequence["new_question"],
        "changed_burden": consequence["changed_burden"],
        "correction": consequence["correction"],
        "falsifier": consequence["falsifier"],
    }
    preservation_check = {
        "check_id": stable_identifier(
            "concept-check",
            "protected-observable-preservation",
            preservation,
        ),
        "check_kind": "protected_observable_preservation",
        "status": (
            "failed"
            if preservation["protected_erasure_detected"]
            else "passed"
        ),
        "statement": (
            "Every required finite map and path preserves protected values."
            if not preservation["protected_erasure_detected"]
            else (
                "A required finite map or path erases a protected "
                "observable distinction."
            )
        ),
        "evidence_digest": canonical_digest(preservation),
    }
    checks = [*artifacts["checks"], preservation_check]
    construction = {
        "construction_id": stable_identifier(
            "formal-concept-construction",
            before["content_digest"],
            relation,
            witness,
            consequence,
        ),
        "constructor_id": CONSTRUCTOR_IDS[kind],
        "construction_origin": artifacts["origin"],
        "witness_digest": canonical_digest(witness),
        "checks": checks,
        "local_authority_scope": (
            "finite_relation_specific_conceptual_transformation_only"
        ),
    }
    transition_evidence = canonical_digest(
        {
            "construction": construction,
            "preservation": preservation,
            "after_core_digest": after["content_digest"],
        }
    )
    transition = {
        "before_status": "open",
        "after_status": after_status,
        "removal_authorized": removal_authorized,
        "decision_flip_authorized": decision_flip_authorized,
        "reason_code": reason_code,
        "evidence_digest": transition_evidence,
    }
    failed_observable_ids = {
        receipt["source_observable_id"]
        for receipt in preservation["receipts"]
        if not receipt["value_preserved"]
        or not receipt["protected_distinctions_preserved"]
    }
    protected_ids = [
        row["observable_id"]
        for row in before["observables"]
        if row["protected"]
        and row["observable_id"] not in failed_observable_ids
    ]
    physics_handback = {
        "target_id": before["target_id"],
        "obligation_id": before["obligation_id"],
        "physics_applicability": (
            "candidate_physics_handback"
            if before["physical_carrier"] is not None
            else "not_applicable_non_physics"
        ),
        "physical_carrier": before["physical_carrier"],
        "regime": before["regime"],
        "quantifiers": copy.deepcopy(before["quantifiers"]),
        "abstract_change": (
            f"{kind} added {len(primitive_delta[0])} primitive(s), "
            f"{len(relation_delta[0])} relation(s), and "
            f"{len(inhabitant_delta[0])} inhabitant(s); "
            f"outcome={after_status}."
        ),
        "physics_next_action": consequence["physics_next_action"],
        "preserved_observable_ids": protected_ids,
        "open_or_changed_obligations": [
            consequence["changed_burden"],
            *[row["statement"] for row in losses],
        ],
        "correction": consequence["correction"],
        "falsifier": consequence["falsifier"],
        "experiment_role": (
            "secondary_theory_requested_falsifier_only"
        ),
        "physics_value_authorized": False,
        "theorem_authorized": False,
        "continuum_authorized": False,
        "investment_authorized": False,
    }
    packet: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "delta_id": stable_identifier(
            "formal-concept-delta",
            before["content_digest"],
            relation,
            witness,
            consequence,
        ),
        "lens": lens,
        "relation_hypothesis": relation,
        "witness": witness,
        "consequence_contract": consequence,
        "before_core": before,
        "after_core": after,
        "construction": construction,
        "semantic_delta": semantic_delta,
        "observable_preservation": preservation,
        "obstruction_transition": transition,
        "physics_handback": physics_handback,
        "authority_boundary": {
            "finite_local_only": True,
            "truth_authorized": False,
            "conceptual_value_authorized": False,
            "physics_value_authorized": False,
            "theorem_authorized": False,
            "continuum_authorized": False,
            "investment_authorized": False,
            "experiment_selection_authorized": False,
        },
    }
    packet["content_digest"] = canonical_digest(packet)
    try:
        validate_instance(packet, SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_REPLAY_INVALID)
    return packet


def construct_categorical_transformation(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct one of the three Category-specific transformations."""

    return _construct_internal(
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
        expected_lens="categorical",
    )


def construct_hott_transformation(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct one of the four HoTT-specific transformations."""

    return _construct_internal(
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
        expected_lens="hott",
    )


def _specific(
    kind: str,
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    if relation_hypothesis.get("relation_kind") != kind:
        _fail(
            f"specific constructor requires relation_kind={kind}",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    constructor = (
        construct_categorical_transformation
        if kind in CATEGORY_RELATION_KINDS
        else construct_hott_transformation
    )
    return constructor(
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_noncommutativity_localization(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "noncommuting_composition",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_mediator_factorization(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "mediating_factorization",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_functorial_transfer(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "functorial_transfer",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_identity_transport(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "identity_transport",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_equivalence_coherence(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "equivalence_coherence",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_path_independence(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "path_independence",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def construct_descent_coherence(
    source_core: Mapping[str, Any],
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    consequence_contract: Mapping[str, Any],
) -> dict[str, Any]:
    return _specific(
        "descent_coherence",
        source_core,
        relation_hypothesis,
        witness,
        consequence_contract,
    )


def validate_semantic_delta(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Schema-check and reconstruct a delta byte-for-byte."""

    packet = copy.deepcopy(
        dict(_mapping(raw, "semantic delta", FORMAL_CONCEPT_REPLAY_INVALID))
    )
    try:
        validate_instance(packet, SCHEMA)
    except ContractError as exc:
        _fail(str(exc), FORMAL_CONCEPT_REPLAY_INVALID)
    expected_digest = canonical_digest(
        {
            key: value
            for key, value in packet.items()
            if key != "content_digest"
        }
    )
    if packet["content_digest"] != expected_digest:
        _fail(
            "semantic delta content_digest is stale",
            FORMAL_CONCEPT_REPLAY_INVALID,
        )
    expected = _construct_internal(
        packet["before_core"],
        packet["relation_hypothesis"],
        packet["witness"],
        packet["consequence_contract"],
        expected_lens=packet["lens"],
    )
    if canonical_json(packet) != canonical_json(expected):
        _fail(
            "semantic delta differs from deterministic reconstruction",
            FORMAL_CONCEPT_REPLAY_INVALID,
        )
    return {
        "status": "valid",
        "delta_id": packet["delta_id"],
        "content_digest": packet["content_digest"],
        "lens": packet["lens"],
        "relation_kind": packet["relation_hypothesis"][
            "relation_kind"
        ],
        "constructor_id": packet["construction"]["constructor_id"],
        "construction_origin": packet["construction"][
            "construction_origin"
        ],
        "after_status": packet["obstruction_transition"][
            "after_status"
        ],
        "decision_flip_authorized": packet[
            "obstruction_transition"
        ]["decision_flip_authorized"],
        "protected_erasure_detected": packet[
            "observable_preservation"
        ]["protected_erasure_detected"],
    }


def relation_hypothesis_from_theory_atlas(
    atlas_packet: Mapping[str, Any],
    *,
    candidate_id: str,
    relation_kind: str,
    source_primitive_id: str,
    target_primitive_id: str,
) -> dict[str, Any]:
    """Bind a validated atlas completion into a relation hypothesis."""

    try:
        validate_theory_atlas_defect_packet(atlas_packet)
    except TheoryAtlasDefectError as exc:
        _fail(str(exc), FORMAL_CONCEPT_RELATION_INVALID)
    if relation_kind not in RELATION_KINDS:
        _fail(
            "atlas adapter received an unsupported relation kind",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    candidate = next(
        (
            row
            for row in atlas_packet["completion_candidates"]
            if row["candidate_id"] == candidate_id
        ),
        None,
    )
    if candidate is None:
        _fail(
            "atlas candidate_id is absent",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    allowed = _ATLAS_COMPLETION_TO_RELATIONS[
        candidate["completion_kind"]
    ]
    if relation_kind not in allowed:
        _fail(
            (
                f"atlas completion {candidate['completion_kind']} "
                f"is incompatible with {relation_kind}"
            ),
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    defect = next(
        (
            row
            for row in atlas_packet["defects"]
            if row["defect_id"] == candidate["defect_id"]
        ),
        None,
    )
    if defect is None:
        _fail(
            "validated atlas lacks the selected defect",
            FORMAL_CONCEPT_RELATION_INVALID,
        )
    premises = _dedupe(
        [
            atlas_packet["packet_id"],
            atlas_packet["content_digest"],
            defect["defect_id"],
            candidate["candidate_id"],
            candidate["obligation"]["obligation_id"],
            *defect["evidence_refs"],
            *candidate["obligation"]["evidence_refs"],
        ]
    )
    return {
        "relation_id": stable_identifier(
            "atlas-relation-hypothesis",
            atlas_packet["content_digest"],
            candidate_id,
            relation_kind,
            source_primitive_id,
            target_primitive_id,
        ),
        "relation_kind": relation_kind,
        "statement": candidate["claim"],
        "source_primitive_id": source_primitive_id,
        "target_primitive_id": target_primitive_id,
        "premise_ids": premises,
    }


__all__ = [
    "CATEGORY_RELATION_KINDS",
    "CONSTRUCTOR_IDS",
    "FORMAL_CONCEPT_CORE_INVALID",
    "FORMAL_CONCEPT_PRESERVATION_INVALID",
    "FORMAL_CONCEPT_RELATION_INVALID",
    "FORMAL_CONCEPT_REPLAY_INVALID",
    "FORMAL_CONCEPT_WITNESS_INVALID",
    "FREE_COMPLETION_PROMOTION_INVALID",
    "FormalConceptTransformationError",
    "HOTT_RELATION_KINDS",
    "RELATION_KINDS",
    "construct_categorical_transformation",
    "construct_descent_coherence",
    "construct_equivalence_coherence",
    "construct_functorial_transfer",
    "construct_hott_transformation",
    "construct_identity_transport",
    "construct_mediator_factorization",
    "construct_noncommutativity_localization",
    "construct_path_independence",
    "relation_hypothesis_from_theory_atlas",
    "seal_conceptual_core",
    "validate_conceptual_core",
    "validate_semantic_delta",
]
