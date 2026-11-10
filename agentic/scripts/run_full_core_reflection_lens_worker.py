#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Author one semantic ancestry transformation in one supervised process.

For ``reflection`` the parent supplies only the exact common candidate core
and a lens identity.  The process itself derives the lens-specific relation
transformation; an upstream reflection record is neither accepted nor echoed.
For ``candidate_generation`` the process consumes one exact matured candidate
plus the six receipt-bound lens outputs and authors the corresponding parent
conceptual system and typed before/after delta.

Both operations are deterministic local semantic producers.  Process-local
authorship is not cognitive independence, conceptual merit, truth, theorem,
or physics-value authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any


LENSES = (
    "ontological",
    "dialectical",
    "genealogical",
    "modal_explanatory",
    "unification",
    "philosophy_of_physics",
)
LENS_RECIPES = {
    "ontological": ("retype_source", "is ontologically retyped as"),
    "dialectical": ("reverse_relation", "is dialectically opposed by"),
    "genealogical": ("trace_origin", "is contingently inherited through"),
    "modal_explanatory": (
        "counterfactualize_relation",
        "counterfactually conditions rather than necessitates",
    ),
    "unification": (
        "factor_common_structure",
        "is mediated while preserving difference from",
    ),
    "philosophy_of_physics": (
        "identify_physical_carrier",
        "is physically carried through",
    ),
}
REQUEST_FIELDS = {
    "schema_version",
    "study_id",
    "role",
    "operation",
    "request_nonce",
    "invocation_context",
    "payload",
    "payload_digest",
    "isolation_requirement",
    "fault_mode",
}
REFLECTION_PAYLOAD_FIELDS = {
    "candidate_id",
    "candidate_core",
    "candidate_core_digest",
    "lens_id",
    "matched_budget_digest",
    "literature_derived_invention_input",
    "literature_derived_invention_input_digest",
    "minimum_residency_seconds",
}
MATERIALIZATION_PAYLOAD_FIELDS = {
    "matured_candidate",
    "matured_candidate_digest",
    "lens_outputs",
    "lens_output_set_digest",
    "matched_budget_digest",
    "literature_derived_invention_input",
    "literature_derived_invention_input_digest",
    "minimum_residency_seconds",
}
MATURED_FIELDS = {
    "invention_id",
    "branch_id",
    "exploration_role",
    "statement",
    "semantic_core",
    "deep_reflection",
    "risk_reward",
    "physics_handback",
    "semantic_core_digest",
    "worker_response_sha256",
    "branch_record_digest",
    "barrier_receipt_digest",
    "content_digest",
}
LENS_OUTPUT_FIELDS = {
    "lens_id",
    "candidate_core_digest",
    "literature_derived_invention_input_digest",
    "reflection",
    "reflection_digest",
    "execution_record_digest",
    "receipt_id",
    "receipt_digest",
    "response_sha256",
}
CORE_FIELDS = {"statement", "semantic_core", "risk_reward", "physics_handback"}
REFLECTION_FIELDS = {
    "named_relation",
    "relation_before",
    "relation_operation",
    "mutation_status",
    "relation_after",
    "exposed_assumption",
    "strongest_opposition",
    "conceptual_mutation",
    "consequence",
    "boundary_or_correction",
    "semantic_core_correction_link",
    "physics_handback_link",
}
RELATION_FIELDS = {"source", "polarity", "target"}
AUTHORITY_BOUNDARY = (
    "one exact common core was transformed by the requested lens inside this "
    "supervised local process; process-local semantic authorship grants no "
    "cognitive independence, semantic independence, conceptual merit, truth, "
    "theorem, experiment, or physics-value authority"
)
MATERIALIZATION_AUTHORITY_BOUNDARY = (
    "one parent conceptual-system byte sequence and typed before/after delta "
    "were authored inside this supervised process from one exact matured "
    "candidate and six exact receipt-bound lens outputs; this grants no "
    "conceptual merit, truth, theorem, experiment, or physics-value authority"
)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _stable_identifier(prefix: str, *parts: Any) -> str:
    suffix = hashlib.sha256(_canonical_json(list(parts))).hexdigest()[:24]
    return f"{prefix}.{suffix}"


def _text(value: Any, field: str) -> str:
    result = " ".join(str(value or "").strip().split())
    if not result:
        raise ValueError(f"{field} must be substantive")
    return result


def _validate_relation(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != RELATION_FIELDS:
        raise ValueError(f"{field} must be one closed typed relation")
    result = dict(value)
    for key in RELATION_FIELDS:
        _text(result[key], f"{field}.{key}")
    return result


def _candidate_core(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != CORE_FIELDS:
        raise ValueError("candidate_core must repeat the complete closed core")
    core = dict(value)
    _text(core["statement"], "candidate_core.statement")
    for field in ("semantic_core", "risk_reward", "physics_handback"):
        if not isinstance(core[field], Mapping):
            raise ValueError(f"candidate_core.{field} must be an object")
    semantic_core = core["semantic_core"]
    relations = semantic_core.get("relations")
    if not isinstance(relations, list) or not relations:
        raise ValueError("candidate semantic_core must contain typed relations")
    for index, relation in enumerate(relations):
        _validate_relation(relation, f"semantic_core.relations[{index}]")
    _text(semantic_core.get("correction_condition"), "semantic correction")
    _text(semantic_core.get("falsifier"), "semantic falsifier")
    return core


def _literature_input(value: Any, expected_digest: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("literature-derived invention input must be an object")
    result = dict(value)
    if (
        result.get("artifact_kind") != "literature_derived_invention_input"
        or result.get("content_digest")
        != _digest(
            {
                key: item
                for key, item in result.items()
                if key != "content_digest"
            }
        )
        or expected_digest != result["content_digest"]
        or not isinstance(result.get("causal_inputs"), list)
        or not result["causal_inputs"]
    ):
        raise ValueError(
            "literature-derived invention input digest or causal rows changed"
        )
    for index, row in enumerate(result["causal_inputs"]):
        if (
            not isinstance(row, Mapping)
            or not isinstance(row.get("assimilation_delta"), Mapping)
        ):
            raise ValueError(
                f"literature causal input {index} lacks an assimilation delta"
            )
        _text(row.get("causal_input_id"), "literature causal input id")
        _text(
            row["assimilation_delta"].get("event_type"),
            "literature assimilation event",
        )
    return result


def _physics_link(core: Mapping[str, Any]) -> str:
    handback = core["physics_handback"]
    for field in (
        "correction_or_falsifier",
        "proposed_next_decision",
        "decision_rationale",
        "physical_carrier",
        "regime_and_quantifiers",
    ):
        value = handback.get(field)
        if isinstance(value, str) and value.strip():
            return value
    raise ValueError("physics_handback has no exact nonempty link target")


def _derive_reflection(core: Mapping[str, Any], lens_id: str) -> dict[str, Any]:
    """Derive a lens record solely from the common core inside this process."""

    semantic_core = core["semantic_core"]
    relation_index = LENSES.index(lens_id) % len(semantic_core["relations"])
    before = dict(semantic_core["relations"][relation_index])
    operation, polarity = LENS_RECIPES[lens_id]
    if lens_id == "dialectical":
        after = {
            "source": before["target"],
            "polarity": polarity,
            "target": before["source"],
        }
    elif lens_id == "genealogical":
        after = {
            "source": f"historical conditions of {before['source']}",
            "polarity": polarity,
            "target": before["target"],
        }
    elif lens_id == "unification":
        after = {
            "source": f"shared structure across {before['source']}",
            "polarity": polarity,
            "target": before["target"],
        }
    elif lens_id == "philosophy_of_physics":
        carrier = _physics_link(core)
        after = {
            "source": before["source"],
            "polarity": polarity,
            "target": f"{before['target']} on {carrier}",
        }
    else:
        after = {
            "source": (
                f"ontologically retyped {before['source']}"
                if lens_id == "ontological"
                else before["source"]
            ),
            "polarity": polarity,
            "target": before["target"],
        }
    named = (
        f"{before['source']} --{before['polarity']}--> {before['target']}"
    )
    correction = str(semantic_core["correction_condition"])
    return {
        "named_relation": named,
        "relation_before": before,
        "relation_operation": operation,
        "mutation_status": "changed",
        "relation_after": after,
        "exposed_assumption": (
            f"The {lens_id} producer exposes the assumption that {named} "
            "must retain its inherited explanatory type."
        ),
        "strongest_opposition": (
            f"The strongest opposition is that the {lens_id} transformation "
            "may relocate vocabulary without changing a target burden."
        ),
        "conceptual_mutation": (
            f"The {lens_id} operation replaces the inherited relation with "
            f"{after['source']} --{after['polarity']}--> {after['target']}."
        ),
        "consequence": (
            f"The {lens_id} transformation requires the next theory action "
            "to test the changed relation rather than the supplied wording."
        ),
        "boundary_or_correction": correction,
        "semantic_core_correction_link": correction,
        "physics_handback_link": _physics_link(core),
    }


def _validate_reflection_payload(
    raw: Mapping[str, Any],
) -> tuple[str, dict[str, Any], str, dict[str, Any], float]:
    if set(raw) != REFLECTION_PAYLOAD_FIELDS:
        raise ValueError("lens payload is not closed or supplies a reflection")
    candidate_id = _text(raw["candidate_id"], "candidate_id")
    lens_id = _text(raw["lens_id"], "lens_id")
    if lens_id not in LENSES:
        raise ValueError("lens_id is not one of the six exact lenses")
    core = _candidate_core(raw["candidate_core"])
    if raw["candidate_core_digest"] != _digest(core):
        raise ValueError("candidate_core_digest does not bind the complete core")
    if not isinstance(raw["matched_budget_digest"], str):
        raise ValueError("matched_budget_digest is absent")
    literature_input = _literature_input(
        raw["literature_derived_invention_input"],
        raw["literature_derived_invention_input_digest"],
    )
    residency = raw["minimum_residency_seconds"]
    if (
        not isinstance(residency, (int, float))
        or isinstance(residency, bool)
        or not 0.0 <= float(residency) <= 1.0
    ):
        raise ValueError("minimum_residency_seconds is outside [0, 1]")

    return candidate_id, core, lens_id, literature_input, float(residency)


def _lens_output(
    candidate_id: str,
    core: Mapping[str, Any],
    lens_id: str,
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    reflection = _derive_reflection(core, lens_id)
    before = reflection["relation_before"]
    after = reflection["relation_after"]
    causal_rows = literature_input["causal_inputs"]
    selected_input = causal_rows[LENSES.index(lens_id) % len(causal_rows)]
    return {
        "output_kind": "reflection",
        "candidate_id": candidate_id,
        "lens_id": lens_id,
        "candidate_core_digest": _digest(core),
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "literature_causal_input_id": selected_input["causal_input_id"],
        "literature_assimilation_delta": dict(
            selected_input["assimilation_delta"]
        ),
        "reflection": reflection,
        "reflection_digest": _digest(reflection),
        "operation_witness": {
            "lens_operation": reflection["relation_operation"],
            "named_relation": reflection["named_relation"],
            "relation_before_digest": _digest(before),
            "relation_after_digest": _digest(after),
            "mutation_status": "changed",
            "complete_core_fields_replayed": sorted(CORE_FIELDS),
        },
        "semantic_authorship": {
            "status": "authored_inside_supervised_process",
            "upstream_reflection_supplied": False,
            "input_scope": (
                "exact_common_core_plus_lens_identity_plus_semantic_literature_input"
            ),
            "producer_algorithm": "closed_lens_specific_relation_transformation_v1",
        },
        "authority_boundary": AUTHORITY_BOUNDARY,
    }


def _validate_lens_output_row(
    row: Mapping[str, Any],
    *,
    core: Mapping[str, Any],
    expected_lens: str,
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    if set(row) != LENS_OUTPUT_FIELDS or row["lens_id"] != expected_lens:
        raise ValueError("materialization lens output is not the exact ordered row")
    if row["candidate_core_digest"] != _digest(core):
        raise ValueError("materialization lens output crossed candidate cores")
    if (
        row["literature_derived_invention_input_digest"]
        != literature_input["content_digest"]
    ):
        raise ValueError("materialization lens output crossed literature inputs")
    reflection = row["reflection"]
    if (
        not isinstance(reflection, Mapping)
        or set(reflection) != REFLECTION_FIELDS
        or row["reflection_digest"] != _digest(reflection)
        or dict(reflection) != _derive_reflection(core, expected_lens)
    ):
        raise ValueError("materialization lens output is not process-derived")
    for field in ("execution_record_digest", "receipt_id", "receipt_digest"):
        _text(row[field], f"lens_outputs.{expected_lens}.{field}")
    if row["response_sha256"] is not None:
        _text(row["response_sha256"], "lens response_sha256")
    return dict(row)


def _parent_system(
    candidate: Mapping[str, Any],
    lens_outputs: list[dict[str, Any]],
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    candidate_id = str(candidate["invention_id"])
    semantic_core = candidate["semantic_core"]
    reflections = [row["reflection"] for row in lens_outputs]
    transformed_relations = [
        (
            f"{row['relation_after']['source']} "
            f"{row['relation_after']['polarity']} "
            f"{row['relation_after']['target']}"
        )
        for row in reflections
    ]
    primitives = [str(value) for value in semantic_core["primitives"]]
    protected = [
        str(value) for value in semantic_core["protected_differences"]
    ]
    mechanism_steps = [
        str(value) for value in semantic_core["mechanism_steps"]
    ]
    corrections = [str(semantic_core["correction_condition"])]
    corrections.extend(str(row["boundary_or_correction"]) for row in reflections)
    causal_rows = list(literature_input["causal_inputs"])
    causal_ids = [
        str(row["causal_input_id"])
        for row in causal_rows[: len(LENSES)]
    ]
    assimilation_events = [
        str(row["assimilation_delta"]["event_type"])
        for row in causal_rows[: len(LENSES)]
    ]
    exact_claims = [
        str(row["exact_claim"])
        for row in causal_rows[: len(LENSES)]
        if isinstance(row.get("exact_claim"), str)
        and str(row["exact_claim"]).strip()
    ]
    corrections.extend(
        (
            f"Literature input {causal_id} requires {event} under its "
            "retained correction state."
        )
        for causal_id, event in zip(
            causal_ids, assimilation_events, strict=True
        )
    )
    system_id = _stable_identifier(
        "parent-conceptual-system",
        _digest(candidate),
        [row["reflection_digest"] for row in lens_outputs],
        literature_input["content_digest"],
    )
    source_case_ids = [
        "matured-candidate-case",
        "six-lens-transformation-case",
    ]
    before_graph = {
        "nodes": [
            {
                "node_id": source_case_ids[0],
                "node_kind": "source_case",
                "label": "Exact matured candidate before semantic reflection",
                "content_paths": ["/conceptual_ancestors/0"],
            },
            {
                "node_id": source_case_ids[1],
                "node_kind": "source_case",
                "label": "Six process-authored reflection transformations",
                "content_paths": ["/transformation_operations"],
            },
        ],
        "edges": [],
    }
    mediator_node = {
        "node_id": "process-authored-parent-system",
        "node_kind": "mediator",
        "label": "Registered process-authored parent conceptual system",
        "content_paths": [
            "/mechanism_or_principle",
            "/unification_claims/mediator/statement",
        ],
    }
    added_edges = [
        {
            "edge_id": "candidate-to-parent-mediator",
            "source_node_id": source_case_ids[0],
            "relation_kind": "mediates",
            "target_node_id": mediator_node["node_id"],
            "statement": (
                "The exact matured candidate supplies the protected source "
                "content materialized into the parent system."
            ),
            "warrant_paths": ["/conceptual_ancestors/0"],
        },
        {
            "edge_id": "lenses-to-parent-mediator",
            "source_node_id": source_case_ids[1],
            "relation_kind": "transports",
            "target_node_id": mediator_node["node_id"],
            "statement": (
                "Six exact lens outputs transform the candidate relations "
                "before parent conceptual adjudication."
            ),
            "warrant_paths": ["/transformation_operations"],
        },
    ]
    after_graph = {
        "nodes": [*before_graph["nodes"], mediator_node],
        "edges": added_edges,
    }
    typed_unification = {
        "unification_kind": "regime_indexed_mediation",
        "source_case_ids": source_case_ids,
        "mediator": {
            "statement": (
                "A registered parent materializer relates the matured "
                "candidate and six process-authored transformations without "
                "identifying their distinct evidential roles."
            ),
            "primitive_refs": [
                (
                    f"Candidate primitive commitment {index + 1} retains "
                    f"{primitive} within the registered parent mediator."
                )
                for index, primitive in enumerate(primitives)
            ],
            "relation_refs": transformed_relations,
            "node_ids": [mediator_node["node_id"]],
        },
        "mappings": [
            {
                "mapping_id": "candidate-parent-materialization-map",
                "source_case_id": source_case_ids[0],
                "target_node_id": mediator_node["node_id"],
                "map_kind": "production",
                "bridge_statement": (
                    "Candidate primitives and protected differences enter "
                    "through the exact matured-candidate digest."
                ),
                "warrant_paths": [
                    "/conceptual_ancestors/0",
                    "/primitives",
                ],
            },
            {
                "mapping_id": "lens-parent-transformation-map",
                "source_case_id": source_case_ids[1],
                "target_node_id": mediator_node["node_id"],
                "map_kind": "interpretation",
                "bridge_statement": (
                    "Each lens contributes its exact relation operation and "
                    "correction link before adjudication."
                ),
                "warrant_paths": [
                    "/transformation_operations",
                    "/correction_conditions",
                ],
            },
        ],
        "preserved_differences": [
            {
                "difference_id": "candidate-not-lens-output",
                "source_case_ids": [source_case_ids[0]],
                "statement": (
                    "The matured candidate remains distinct from the six "
                    "transformations applied to it."
                ),
                "preservation_witness_paths": [
                    "/conceptual_ancestors/0"
                ],
                "witness_node_ids": [
                    source_case_ids[0],
                    mediator_node["node_id"],
                ],
                "witness_edge_ids": ["candidate-to-parent-mediator"],
            },
            {
                "difference_id": "lens-output-not-candidate",
                "source_case_ids": [source_case_ids[1]],
                "statement": (
                    "Process-authored lens outputs remain distinct from the "
                    "candidate content they transform."
                ),
                "preservation_witness_paths": [
                    "/transformation_operations"
                ],
                "witness_node_ids": [
                    source_case_ids[1],
                    mediator_node["node_id"],
                ],
                "witness_edge_ids": ["lenses-to-parent-mediator"],
            },
        ],
        "explanatory_graph_transition": {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_graph_digest": _digest(before_graph),
            "after_graph_digest": _digest(after_graph),
            "added_nodes": [mediator_node],
            "added_edges": added_edges,
            "new_explanatory_dependencies": [
                "Parent authorship now depends on both the matured candidate "
                "and six exact process-authored lens outputs."
            ],
        },
        "scope_conditions": [
            "The mediation applies only to the exact candidate and receipt set."
        ],
        "transfer_obligations": [
            "Reopen all seven producer inputs before conceptual promotion."
        ],
        "erasure_risks": [
            str(candidate["risk_reward"]["cost_of_unification"])
        ],
        "failure_conditions": [
            "Reject the parent if any source case, lens output, or protected "
            "difference is omitted or substituted."
        ],
    }
    return {
        "system_id": system_id,
        "relation": "challenger",
        "lifecycle_state": "reflectively_revised",
        "structural_identity": {
            "primitive_ids": [
                _stable_identifier("primitive", candidate_id, value)
                for value in primitives
            ],
            "relation_ids": [
                _stable_identifier("relation", candidate_id, value)
                for value in transformed_relations
            ],
            "mechanism_id": _stable_identifier(
                "mechanism", candidate_id, mechanism_steps
            ),
            "maturation_question_id": _stable_identifier(
                "maturation-question",
                candidate_id,
                semantic_core["counterfactual_consequence"],
            ),
            "genealogy_ids": [candidate_id, literature_input["input_id"]],
        },
        "conceptual_ancestors": [candidate_id, literature_input["input_id"]],
        "transformation_operations": [
            f"{row['lens_id']}:{row['reflection']['relation_operation']}"
            for row in lens_outputs
        ]
        + [
            f"literature:{event}:{causal_id}"
            for causal_id, event in zip(
                causal_ids, assimilation_events, strict=True
            )
        ],
        "primitives": primitives,
        "ontological_commitments": [
            f"Treat {value} as an explicit correctable commitment."
            for value in primitives
        ],
        "identities_and_differences": protected,
        "relations_operations_and_dynamics": transformed_relations,
        "explanatory_ideal": "mixed",
        "mechanism_or_principle": " ".join(mechanism_steps),
        "protected_successes": protected,
        "target_pressures_addressed": [
            str(candidate["statement"]),
            str(semantic_core["counterfactual_consequence"]),
        ]
        + exact_claims,
        "formerly_inexpressible_now_visible": [
            str(row["conceptual_mutation"]) for row in reflections
        ]
        + [
            (
                f"Semantic literature input {causal_id} enters as a bounded "
                f"{event} delta rather than an untyped citation."
            )
            for causal_id, event in zip(
                causal_ids, assimilation_events, strict=True
            )
        ],
        "unification_claims": typed_unification,
        "implications_and_new_questions": [
            str(row["consequence"]) for row in reflections
        ]
        + [
            (
                f"Which target-preserving consequence follows if {causal_id} "
                f"retains assimilation event {event}?"
            )
            for causal_id, event in zip(
                causal_ids, assimilation_events, strict=True
            )
        ],
        "formalization_seeds": transformed_relations,
        "correction_conditions": list(dict.fromkeys(corrections)),
        "residual_contradictions": [
            str(candidate["risk_reward"]["risk_case"]),
            str(semantic_core["falsifier"]),
        ],
        "non_claims": [
            "This process-authored conceptual system establishes no theorem, "
            "physics value, mass gap, or Yang--Mills result.",
            "Semantic literature inputs grant no source truth, exhaustive "
            "coverage, global latestness, creativity, or benefit authority.",
        ],
    }


def _validate_materialization_payload(
    raw: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], float]:
    if set(raw) != MATERIALIZATION_PAYLOAD_FIELDS:
        raise ValueError("parent materialization payload is not closed")
    candidate = raw["matured_candidate"]
    if not isinstance(candidate, Mapping) or set(candidate) != MATURED_FIELDS:
        raise ValueError("materialization requires one exact matured candidate")
    candidate = dict(candidate)
    candidate_id = _text(candidate["invention_id"], "invention_id")
    _text(candidate["branch_id"], "branch_id")
    core = _candidate_core(
        {
            field: candidate[field]
            for field in ("statement", "semantic_core", "risk_reward", "physics_handback")
        }
    )
    if raw["matured_candidate_digest"] != _digest(candidate):
        raise ValueError("matured_candidate_digest mismatch")
    rows = raw["lens_outputs"]
    if not isinstance(rows, list) or len(rows) != len(LENSES):
        raise ValueError("materialization requires exactly six lens outputs")
    literature_input = _literature_input(
        raw["literature_derived_invention_input"],
        raw["literature_derived_invention_input_digest"],
    )
    validated = [
        _validate_lens_output_row(
            row,
            core=core,
            expected_lens=lens_id,
            literature_input=literature_input,
        )
        for row, lens_id in zip(rows, LENSES, strict=True)
    ]
    if raw["lens_output_set_digest"] != _digest(validated):
        raise ValueError("lens_output_set_digest mismatch")
    if not isinstance(raw["matched_budget_digest"], str):
        raise ValueError("matched_budget_digest is absent")
    residency = raw["minimum_residency_seconds"]
    if (
        not isinstance(residency, (int, float))
        or isinstance(residency, bool)
        or not 0.0 <= float(residency) <= 1.0
    ):
        raise ValueError("minimum_residency_seconds is outside [0, 1]")
    _text(candidate_id, "candidate_id")
    return candidate, validated, literature_input, float(residency)


def _materialization_output(
    candidate: Mapping[str, Any],
    lens_outputs: list[dict[str, Any]],
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    parent = _parent_system(candidate, lens_outputs, literature_input)
    candidate_digest = _digest(candidate)
    parent_digest = _digest(parent)
    lens_set_digest = _digest(lens_outputs)
    delta = {
        "delta_kind": (
            "matured_candidate_plus_six_lens_outputs_to_parent_conceptual_system"
        ),
        "source_candidate_id": candidate["invention_id"],
        "source_candidate_digest": candidate_digest,
        "lens_output_set_digest": lens_set_digest,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "before": {
            "artifact_kind": "matured_candidate",
            "content": dict(candidate),
            "content_digest": candidate_digest,
        },
        "after": {
            "artifact_kind": "parent_conceptual_system",
            "content": parent,
            "content_digest": parent_digest,
        },
        "changed_paths": [
            f"/lens_outputs/{index}/reflection/relation_after"
            for index in range(len(LENSES))
        ],
        "preserved_source_paths": [
            "/statement",
            "/semantic_core/protected_differences",
            "/semantic_core/correction_condition",
            "/physics_handback",
        ],
    }
    return {
        "output_kind": "candidate_generation",
        "candidate_id": candidate["invention_id"],
        "matured_candidate_digest": candidate_digest,
        "lens_output_set_digest": lens_set_digest,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "parent_conceptual_system": parent,
        "parent_conceptual_system_digest": parent_digest,
        "conceptual_delta": delta,
        "conceptual_delta_digest": _digest(delta),
        "semantic_authorship": {
            "status": "authored_inside_registered_supervised_process",
            "input_scope": (
                "exact_matured_candidate_plus_six_lens_outputs_plus_semantic_literature_input"
            ),
            "producer_algorithm": "closed_parent_system_materialization_v1",
        },
        "authority_boundary": MATERIALIZATION_AUTHORITY_BOUNDARY,
    }


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, Mapping) or set(request) != REQUEST_FIELDS:
            raise ValueError("worker request must be the exact closed envelope")
        if (
            request["schema_version"] != 1
            or request["role"] != "candidate"
            or request["operation"] not in {"reflection", "candidate_generation"}
            or not isinstance(request["invocation_context"], Mapping)
            or not isinstance(request["payload"], Mapping)
            or request["payload_digest"] != _digest(request["payload"])
        ):
            raise ValueError("worker request identity or payload digest mismatch")
        fault_mode = request["fault_mode"]
        if fault_mode not in {None, "exit_nonzero", "invalid_json", "hang"}:
            raise ValueError("unknown worker fault mode")
        if fault_mode == "exit_nonzero":
            return 17
        if fault_mode == "invalid_json":
            sys.stdout.write("{")
            return 0
        if fault_mode == "hang":
            time.sleep(60.0)

        if request["operation"] == "reflection":
            candidate_id, core, lens_id, literature_input, residency = (
                _validate_reflection_payload(request["payload"])
            )
            output = _lens_output(
                candidate_id, core, lens_id, literature_input
            )
        else:
            candidate, lens_outputs, literature_input, residency = (
                _validate_materialization_payload(request["payload"])
            )
            output = _materialization_output(
                candidate, lens_outputs, literature_input
            )
        time.sleep(residency)
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": "candidate",
            "operation": str(request["operation"]),
            "request_nonce": str(request["request_nonce"]),
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": output,
        }
        sys.stdout.buffer.write(_canonical_json(response) + b"\n")
        return 0
    except Exception as exc:
        error = {
            "status": "worker_protocol_error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }
        sys.stderr.buffer.write(_canonical_json(error) + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
