# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Receipt-bound literature-conditioned pre-taxonomy invention.

The conceptual ancestry pipeline previously accepted an already-authored
invention freeze and caller-authored family labels.  That proves association
with literature bytes, but it does not prove that semantic literature entered
the generative operation.  This module supplies the missing production seam:

* one sealed request contains target constraints and the exact semantic
  claim/span/warrant/correction projection before any invention exists;
* a supervised high-risk worker authors raw inventions and executable
  intervention structures from that request;
* an independent deterministic reopener derives causal-family types from the
  intervention structures rather than trusting worker-supplied family labels;
* the worker receipt, source freeze, conditioned freeze, and bounded
  satisfiability analysis are closed into one replayable execution packet; and
* counterfactual worlds can remove, substitute, correct, supersede, or retract
  literature inputs without changing target constraints or worker authority.

The machinery establishes local request-before-output causality and exact
semantic sensitivity only.  It does not establish source truth, novelty,
creativity, conceptual merit, literature benefit, or physics value.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .budgets import ResourceBudget, contained_path
from .conceptual_ancestry_v3 import (
    build_conceptual_ancestry_literature_projection,
    build_literature_conditioned_invention_freeze,
)
from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from .open_world_creativity import (
    build_pre_taxonomy_invention_freeze,
    known_taxonomy_commitment,
)
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)


SCHEMA_VERSION = "1.0.0"
SCHEMA_NAME = "literature_conditioned_invention_execution_v1.schema.json"
MIN_DISTINCT_FAMILIES = 6
WORKER_CONTRACT = "literature-conditioned-pre-taxonomy-invention.v1"
AUTHORITY_NULLS = {
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "semantic_entailment_authority": None,
    "novelty_authority": None,
    "creativity_authority": None,
    "conceptual_merit_authority": None,
    "literature_benefit_authority": None,
    "physics_value_authority": None,
    "truth_authority": None,
}
AUTHORITY_BOUNDARY = (
    "The packet proves that one supervised local process received exact target "
    "constraints and a sealed semantic literature input before authoring raw "
    "inventions, and that an independent deterministic reopener derived typed "
    "family structure from exact interventions, predictions, corrections, "
    "falsifiers, and physics returns. It grants no source-truth, global-"
    "latestness, semantic-entailment, novelty, creativity, conceptual-merit, "
    "literature-benefit, physics-value, proof, theorem, or truth authority."
)

_PROGRAM_TYPES: dict[str, dict[str, str]] = {
    "introduce_mediator": {
        "primitive_kind": "relation",
        "relation_kind": "constitutive",
        "mechanism_kind": "mediation",
        "intervention_kind": "add",
        "prediction_direction": "permit",
        "correction_kind": "add_mediator",
    },
    "invert_dependence": {
        "primitive_kind": "process",
        "relation_kind": "causal",
        "mechanism_kind": "symmetry_breaking",
        "intervention_kind": "reverse",
        "prediction_direction": "bifurcate",
        "correction_kind": "change_relation",
    },
    "protect_invariant": {
        "primitive_kind": "constraint",
        "relation_kind": "constraint",
        "mechanism_kind": "constraint_propagation",
        "intervention_kind": "hold_fixed",
        "prediction_direction": "invariant",
        "correction_kind": "split_scope",
    },
    "localize_obstruction": {
        "primitive_kind": "observer",
        "relation_kind": "operational",
        "mechanism_kind": "topological_obstruction",
        "intervention_kind": "localize",
        "prediction_direction": "obstruct",
        "correction_kind": "retype",
    },
    "quotient_redundancy": {
        "primitive_kind": "information",
        "relation_kind": "duality",
        "mechanism_kind": "coarse_graining",
        "intervention_kind": "quotient",
        "prediction_direction": "decrease",
        "correction_kind": "retract",
    },
    "close_feedback": {
        "primitive_kind": "entity",
        "relation_kind": "emergent",
        "mechanism_kind": "feedback",
        "intervention_kind": "remove",
        "prediction_direction": "increase",
        "correction_kind": "abandon",
    },
    "split_regime": {
        "primitive_kind": "constraint",
        "relation_kind": "causal",
        "mechanism_kind": "coarse_graining",
        "intervention_kind": "localize",
        "prediction_direction": "bifurcate",
        "correction_kind": "split_scope",
    },
    "dualize_carrier": {
        "primitive_kind": "relation",
        "relation_kind": "duality",
        "mechanism_kind": "mediation",
        "intervention_kind": "reverse",
        "prediction_direction": "invariant",
        "correction_kind": "change_relation",
    },
}

_RAW_INVENTION_FIELDS = frozenset(
    {
        "invention_id",
        "conjecture",
        "primitive_hunches",
        "relation_hunches",
        "mechanism_hunch",
        "root_tension_contact",
        "counterfactual_world",
        "protected_successes",
        "risk_if_wrong",
        "upside_if_right",
        "first_falsifier",
        "correction_path",
    }
)
_FAMILY_EVIDENCE_FIELDS = frozenset(
    {
        "invention_id",
        "literature_causal_input_ids",
        "target_grounding",
        "intervention_program",
        "prediction",
        "correction",
        "falsifier",
        "physics_return",
        "evidence_digest",
    }
)


class LiteratureConditionedInventionError(ContractError):
    """Stable fail-closed error for invention production and replay."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(
            f"literature_conditioned_invention[{reason_code}]: {message}"
        )


def _fail(reason_code: str, message: str) -> None:
    raise LiteratureConditionedInventionError(reason_code, message)


def _seal(core: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(core))
    return {**value, "content_digest": canonical_digest(value)}


def _verify_seal(
    value: Mapping[str, Any], digest_field: str, label: str
) -> None:
    retained = value.get(digest_field)
    expected = canonical_digest(
        {key: item for key, item in value.items() if key != digest_field}
    )
    if retained != expected:
        _fail("digest_mismatch", f"{label} digest changed")


def _text(value: Any, field: str) -> str:
    result = " ".join(str(value or "").split())
    if not result:
        _fail("request_invalid", f"{field} must be nonempty")
    return result


def _text_list(value: Any, field: str) -> list[str]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
    ):
        _fail("request_invalid", f"{field} must be a sequence")
    rows = [_text(item, field) for item in value]
    if not rows or len(rows) != len(set(rows)):
        _fail("request_invalid", f"{field} must be nonempty and unique")
    return rows


def _literature_input(
    literature_projection: Mapping[str, Any],
) -> dict[str, Any]:
    projection = copy.deepcopy(dict(literature_projection))
    _verify_seal(projection, "content_digest", "literature projection")
    if projection.get("artifact_kind") != "literature_only_projection_v3":
        _fail(
            "literature_projection_invalid",
            "invention requires the exact v3 semantic literature projection",
        )
    value = copy.deepcopy(
        dict(projection.get("literature_derived_invention_input", {}))
    )
    _verify_seal(value, "content_digest", "literature invention input")
    if (
        value.get("artifact_kind") != "literature_derived_invention_input"
        or not isinstance(value.get("causal_inputs"), list)
        or not value["causal_inputs"]
    ):
        _fail(
            "literature_input_invalid",
            "semantic claim/warrant/correction input is absent",
        )
    identifiers = [str(row.get("causal_input_id", "")) for row in value["causal_inputs"]]
    if (
        any(not identifier for identifier in identifiers)
        or len(identifiers) != len(set(identifiers))
    ):
        _fail(
            "literature_input_invalid",
            "semantic causal input identities are empty or duplicated",
        )
    return value


def _reopen_literature_authority(
    *,
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
) -> dict[str, Any]:
    """Rebuild the raw/bridge/snapshot projection at the consumption time."""

    projection = copy.deepcopy(dict(literature_projection))
    bundle = copy.deepcopy(dict(literature_bundle))
    try:
        expected = build_conceptual_ancestry_literature_projection(
            literature_bundle=bundle,
            semantic_snapshot=projection["semantic_snapshot"],
            literature_snapshot_capture_bridge=projection[
                "semantic_bridge"
            ],
            present_use_at=_text(
                governed_present_use_at,
                "governed_present_use_at",
            ),
        )
    except (KeyError, ContractError) as exc:
        raise LiteratureConditionedInventionError(
            "literature_authority_reopen_failed",
            "raw capture, semantic bridge, snapshot, bundle, or currentness failed replay",
        ) from exc
    if projection != expected:
        _fail(
            "literature_authority_replay_mismatch",
            "literature projection is not derived from the supplied current bundle",
        )
    core = {
        "authority_kind": "transitively_reopened_bounded_literature_v1",
        "governed_present_use_at": governed_present_use_at,
        "literature_bundle": bundle,
        "literature_bundle_digest": bundle["content_digest"],
        "literature_projection": expected,
        "literature_projection_digest": expected["content_digest"],
        "raw_capture_sha256": expected["raw_capture_root"]["sha256"],
        "semantic_bridge_digest": expected["semantic_bridge_digest"],
        "semantic_snapshot_digest": expected["semantic_snapshot_root"][
            "content_digest"
        ],
        "global_latestness_authority": None,
        "source_truth_authority": None,
        "literature_benefit_authority": None,
        "clock_attestation_authority": None,
    }
    return _seal(core)


def _normalized_budget(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    candidate = (
        ResearchWorkerAdapter.default_budget()
        if raw is None
        else copy.deepcopy(dict(raw))
    )
    try:
        return asdict(ResourceBudget.from_mapping(candidate))
    except (TypeError, ValueError) as exc:
        raise LiteratureConditionedInventionError(
            "budget_invalid", "worker budget is invalid"
        ) from exc


def build_literature_conditioned_invention_request(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    target_pressure: str,
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
    known_taxonomy: Mapping[str, Any],
    requested_count: int = 8,
) -> dict[str, Any]:
    """Seal the exact pre-output request consumed by the invention worker."""

    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    if (
        isinstance(state_version, bool)
        or not isinstance(state_version, int)
        or state_version < 0
    ):
        _fail("request_invalid", "state_version must be nonnegative")
    if (
        isinstance(requested_count, bool)
        or not isinstance(requested_count, int)
        or not MIN_DISTINCT_FAMILIES <= requested_count <= len(_PROGRAM_TYPES)
    ):
        _fail(
            "request_invalid",
            "requested_count must cover six through eight structural programmes",
        )
    literature_authority = _reopen_literature_authority(
        literature_projection=literature_projection,
        literature_bundle=literature_bundle,
        governed_present_use_at=governed_present_use_at,
    )
    literature_input = _literature_input(
        literature_authority["literature_projection"]
    )
    if literature_input.get("target_id") != target_id:
        _fail(
            "literature_identity_mismatch",
            "literature invention input crossed targets",
        )
    constraints = {
        "target_pressure": _text(target_pressure, "target_pressure"),
        "root_contradictions": _text_list(
            root_contradictions, "root_contradictions"
        ),
        "protected_successes": _text_list(
            protected_successes, "protected_successes"
        ),
    }
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "literature_conditioned_invention_request",
        "request_id": stable_identifier(
            "literature-conditioned-invention-request",
            target_id,
            run_id,
            state_version,
            constraints,
            literature_input["content_digest"],
            known_taxonomy_commitment(known_taxonomy),
            requested_count,
        ),
        "namespace": {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
        },
        "target_constraints": constraints,
        "requested_count": requested_count,
        "minimum_distinct_family_count": MIN_DISTINCT_FAMILIES,
        "literature_derived_invention_input": literature_input,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "literature_authority": literature_authority,
        "known_taxonomy_commitment_digest": known_taxonomy_commitment(
            known_taxonomy
        ),
        "taxonomy_visibility": "withheld_by_commitment_only",
        "required_output_contract": WORKER_CONTRACT,
        "caller_supplied_inventions": False,
        "caller_supplied_family_labels": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
    }
    return _seal(core)


def _validate_worker_output(
    output: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    value = copy.deepcopy(dict(output))
    if (
        value.get("output_kind") != "high_risk_generation"
        or value.get("output_contract") != WORKER_CONTRACT
        or value.get("request_id") != request["request_id"]
        or value.get("request_digest") != request["content_digest"]
        or value.get("literature_derived_invention_input_digest")
        != request["literature_derived_invention_input_digest"]
        or value.get("known_taxonomy_commitment_digest")
        != request["known_taxonomy_commitment_digest"]
        or value.get("caller_supplied_inventions_consumed") is not False
        or value.get("caller_supplied_family_labels_consumed") is not False
    ):
        _fail(
            "worker_output_binding_mismatch",
            "worker output does not bind the sealed pre-output request",
        )
    inventions = value.get("raw_inventions")
    evidence = value.get("family_evidence")
    if (
        not isinstance(inventions, list)
        or not isinstance(evidence, list)
        or len(inventions) != request["requested_count"]
        or len(evidence) != len(inventions)
    ):
        _fail(
            "worker_output_cardinality_invalid",
            "worker must emit one evidence row per requested invention",
        )
    invention_rows: list[dict[str, Any]] = []
    invention_ids: list[str] = []
    for raw in inventions:
        if not isinstance(raw, Mapping) or set(raw) != _RAW_INVENTION_FIELDS:
            _fail(
                "worker_invention_invalid",
                "worker invention has an open or incomplete shape",
            )
        row = copy.deepcopy(dict(raw))
        validate_identifier(str(row["invention_id"]), "invention_id")
        invention_ids.append(str(row["invention_id"]))
        invention_rows.append(row)
    if len(invention_ids) != len(set(invention_ids)):
        _fail("worker_invention_invalid", "worker invention IDs repeat")
    evidence_rows: list[dict[str, Any]] = []
    for raw in evidence:
        if not isinstance(raw, Mapping) or set(raw) != _FAMILY_EVIDENCE_FIELDS:
            _fail(
                "family_evidence_invalid",
                "family evidence has an open or incomplete shape",
            )
        row = copy.deepcopy(dict(raw))
        _verify_seal(row, "evidence_digest", "family evidence")
        evidence_rows.append(row)
    if sorted(row["invention_id"] for row in evidence_rows) != sorted(
        invention_ids
    ):
        _fail(
            "family_evidence_bijection_invalid",
            "family evidence is not a bijection over worker inventions",
        )
    expected_signature = canonical_digest(
        [
            {
                "intervention_program": row["intervention_program"],
                "prediction": row["prediction"],
                "correction": row["correction"],
                "falsifier": row["falsifier"],
                "physics_return": row["physics_return"],
            }
            for row in sorted(evidence_rows, key=lambda item: item["invention_id"])
        ]
    )
    if value.get("semantic_output_signature") != expected_signature:
        _fail(
            "semantic_output_signature_mismatch",
            "worker semantic signature does not replay",
        )
    expected_identity_erased = _identity_erased_conceptual_signature(
        evidence_rows
    )
    if (
        value.get("identity_erased_conceptual_signature")
        != expected_identity_erased
    ):
        _fail(
            "identity_erased_signature_mismatch",
            "worker conceptual signature changed under independent replay",
        )
    return invention_rows, evidence_rows


def _identity_erased_conceptual_signature(
    evidence_rows: Sequence[Mapping[str, Any]],
) -> str:
    """Digest only theory-facing structure, never source or receipt identity."""

    projection: list[dict[str, Any]] = []
    for raw in evidence_rows:
        row = dict(raw)
        grounding = dict(row["target_grounding"])
        programme = dict(row["intervention_program"])
        transformation = dict(programme["transformation"])
        prediction = dict(row["prediction"])
        correction = dict(row["correction"])
        falsifier = dict(row["falsifier"])
        physics_return = dict(row["physics_return"])
        projection.append(
            {
                "operation": programme["operation"],
                "target_constraint_path": programme[
                    "target_constraint_path"
                ],
                "root_contradiction_index": grounding[
                    "root_contradiction_index"
                ],
                "protected_success_index": grounding[
                    "protected_success_index"
                ],
                "transformation_verb": transformation["verb"],
                "prediction_observable_path": prediction[
                    "observable_path"
                ],
                "prediction_decisive_change": prediction[
                    "decisive_change"
                ],
                "correction_trigger": correction["trigger"],
                "falsifier_decisive_outcome": falsifier[
                    "decisive_outcome"
                ],
                "physics_protected_success_path": physics_return[
                    "protected_success_path"
                ],
                "physics_next_theory_action": physics_return[
                    "next_theory_action"
                ],
                "physics_value_condition": physics_return[
                    "value_condition"
                ],
            }
        )
    projection.sort(key=canonical_digest)
    return canonical_digest(projection)


def _derive_family_contracts(
    *,
    request: Mapping[str, Any],
    inventions: Sequence[Mapping[str, Any]],
    evidence: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive closed family types from grounded intervention programmes."""

    invention_by_id = {
        str(row["invention_id"]): copy.deepcopy(dict(row))
        for row in inventions
    }
    causal_rows = request["literature_derived_invention_input"]["causal_inputs"]
    causal_ids = {
        str(row["causal_input_id"]) for row in causal_rows
    }
    constraints = request["target_constraints"]
    contracts: list[dict[str, Any]] = []
    semantic_signatures: list[dict[str, Any]] = []
    for raw in evidence:
        row = copy.deepcopy(dict(raw))
        invention_id = str(row["invention_id"])
        if invention_id not in invention_by_id:
            _fail(
                "family_evidence_bijection_invalid",
                "family evidence names an unknown invention",
            )
        grounding = row["target_grounding"]
        if (
            not isinstance(grounding, Mapping)
            or set(grounding)
            != {
                "target_pressure_digest",
                "root_contradiction_index",
                "root_contradiction_digest",
                "protected_success_index",
                "protected_success_digest",
            }
        ):
            _fail("target_grounding_invalid", "target grounding is not closed")
        contradiction_index = grounding["root_contradiction_index"]
        success_index = grounding["protected_success_index"]
        if (
            isinstance(contradiction_index, bool)
            or not isinstance(contradiction_index, int)
            or not 0
            <= contradiction_index
            < len(constraints["root_contradictions"])
            or isinstance(success_index, bool)
            or not isinstance(success_index, int)
            or not 0 <= success_index < len(constraints["protected_successes"])
            or grounding["target_pressure_digest"]
            != canonical_digest(constraints["target_pressure"])
            or grounding["root_contradiction_digest"]
            != canonical_digest(
                constraints["root_contradictions"][contradiction_index]
            )
            or grounding["protected_success_digest"]
            != canonical_digest(constraints["protected_successes"][success_index])
        ):
            _fail(
                "target_grounding_invalid",
                "family evidence does not resolve exact target constraints",
            )
        input_ids = row["literature_causal_input_ids"]
        if (
            not isinstance(input_ids, list)
            or not input_ids
            or len(input_ids) != len(set(input_ids))
            or not set(input_ids) <= causal_ids
        ):
            _fail(
                "literature_derivation_invalid",
                "family evidence does not cite exact semantic causal inputs",
            )
        program = row["intervention_program"]
        if not isinstance(program, Mapping):
            _fail("intervention_program_invalid", "intervention is not an object")
        operation = str(program.get("operation", ""))
        if operation not in _PROGRAM_TYPES:
            _fail(
                "intervention_program_invalid",
                "intervention operation is outside the registered programme set",
            )
        if (
            program.get("literature_input_path")
            not in {
                f"/literature_derived_invention_input/causal_inputs/{index}"
                for index, causal_row in enumerate(causal_rows)
                if causal_row["causal_input_id"] in input_ids
            }
            or program.get("target_constraint_path")
            not in {
                "/target_constraints/target_pressure",
                f"/target_constraints/root_contradictions/{contradiction_index}",
                f"/target_constraints/protected_successes/{success_index}",
            }
            or not isinstance(program.get("transformation"), Mapping)
        ):
            _fail(
                "intervention_program_invalid",
                "intervention paths or transformation are not task grounded",
            )
        prediction = row["prediction"]
        correction = row["correction"]
        falsifier = row["falsifier"]
        physics_return = row["physics_return"]
        if any(
            not isinstance(item, Mapping)
            for item in (prediction, correction, falsifier, physics_return)
        ):
            _fail(
                "family_semantics_invalid",
                "prediction, correction, falsifier, and physics return are required",
            )
        if (
            prediction.get("observable_path")
            not in {
                "/target_constraints/target_pressure",
                f"/target_constraints/root_contradictions/{contradiction_index}",
                f"/target_constraints/protected_successes/{success_index}",
            }
            or physics_return.get("protected_success_path")
            != f"/target_constraints/protected_successes/{success_index}"
            or not all(
                isinstance(item.get(field), str) and item[field].strip()
                for item, field in (
                    (prediction, "decisive_change"),
                    (correction, "trigger"),
                    (correction, "revision_action"),
                    (falsifier, "countermodel"),
                    (falsifier, "decisive_outcome"),
                    (physics_return, "next_theory_action"),
                    (physics_return, "value_condition"),
                )
            )
        ):
            _fail(
                "family_semantics_invalid",
                "semantic family return is not exact or decision bearing",
            )
        derived = _PROGRAM_TYPES[operation]
        source = invention_by_id[invention_id]
        contract_core = {
            "invention_id": invention_id,
            "source_invention_digest": canonical_digest(source),
            **copy.deepcopy(derived),
            "target_grounding_paths": [
                "/invention_request/target_pressure",
                f"/invention_request/root_contradictions/{contradiction_index}",
                f"/invention_request/protected_successes/{success_index}",
            ],
            "literature_causal_input_ids": copy.deepcopy(input_ids),
        }
        contracts.append(
            {
                **contract_core,
                "contract_digest": canonical_digest(contract_core),
            }
        )
        semantic_signatures.append(
            {
                "invention_id": invention_id,
                "operation": operation,
                "literature_causal_input_ids": copy.deepcopy(input_ids),
                "root_contradiction_index": contradiction_index,
                "protected_success_index": success_index,
                "transformation_digest": canonical_digest(
                    program["transformation"]
                ),
                "prediction_digest": canonical_digest(prediction),
                "correction_digest": canonical_digest(correction),
                "falsifier_digest": canonical_digest(falsifier),
                "physics_return_digest": canonical_digest(physics_return),
            }
        )
    contracts.sort(key=lambda item: item["invention_id"])
    semantic_signatures.sort(key=lambda item: item["invention_id"])
    distinct = {
        canonical_digest(
            {
                key: value
                for key, value in row.items()
                if key != "invention_id"
            }
        )
        for row in semantic_signatures
    }
    feasible_count = (
        len(_PROGRAM_TYPES)
        * len(causal_rows)
        * len(constraints["root_contradictions"])
        * len(constraints["protected_successes"])
    )
    if len(distinct) < MIN_DISTINCT_FAMILIES and feasible_count >= MIN_DISTINCT_FAMILIES:
        _fail(
            "semantic_family_floor_unsatisfied",
            "worker collapsed families although six task-grounded signatures are feasible",
        )
    certificate = (
        {
            "certificate_kind": "finite_target_constraint_unsat",
            "required_family_count": MIN_DISTINCT_FAMILIES,
            "feasible_signature_count": feasible_count,
            "operation_count": len(_PROGRAM_TYPES),
            "literature_input_count": len(causal_rows),
            "root_contradiction_count": len(
                constraints["root_contradictions"]
            ),
            "protected_success_count": len(
                constraints["protected_successes"]
            ),
            "enumeration_digest": canonical_digest(
                {
                    "operations": sorted(_PROGRAM_TYPES),
                    "literature_input_ids": sorted(causal_ids),
                    "root_contradiction_count": len(
                        constraints["root_contradictions"]
                    ),
                    "protected_success_count": len(
                        constraints["protected_successes"]
                    ),
                }
            ),
        }
        if feasible_count < MIN_DISTINCT_FAMILIES
        else None
    )
    assessment_core = {
        "assessment_kind": "independently_derived_task_grounded_families",
        "semantic_signatures": semantic_signatures,
        "semantic_signature_count": len(distinct),
        "minimum_required": MIN_DISTINCT_FAMILIES,
        "status": (
            "six_or_more_semantically_distinct_families"
            if len(distinct) >= MIN_DISTINCT_FAMILIES
            else "bounded_target_constraint_unsat"
        ),
        "bounded_satisfiability": {
            "feasible_signature_count": feasible_count,
            "unsat_certificate": certificate,
        },
        "worker_family_labels_consumed": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
    }
    return contracts, _seal(assessment_core)


def _receipt_path(receipt: Mapping[str, Any]) -> Path:
    try:
        return contained_path(
            Path(str(receipt["workspace"]["run_directory"])),
            *Path(str(receipt["receipt_ref"])).parts,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise LiteratureConditionedInventionError(
            "receipt_path_invalid", "worker receipt path is invalid"
        ) from exc


def build_literature_conditioned_invention_execution(
    *,
    request: Mapping[str, Any],
    registered_receipt: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
) -> dict[str, Any]:
    """Close one accepted worker receipt into an ancestry-ready packet."""

    request_value = copy.deepcopy(dict(request))
    _verify_seal(request_value, "content_digest", "invention request")
    if (
        request_value.get("artifact_kind")
        != "literature_conditioned_invention_request"
        or request_value.get("known_taxonomy_commitment_digest")
        != known_taxonomy_commitment(known_taxonomy)
    ):
        _fail(
            "request_replay_mismatch",
            "request kind or withheld taxonomy commitment changed",
        )
    authority = copy.deepcopy(
        dict(request_value.get("literature_authority", {}))
    )
    _verify_seal(authority, "content_digest", "literature authority")
    reopened_authority = _reopen_literature_authority(
        literature_projection=authority["literature_projection"],
        literature_bundle=authority["literature_bundle"],
        governed_present_use_at=authority["governed_present_use_at"],
    )
    if (
        authority != reopened_authority
        or request_value["literature_derived_invention_input"]
        != reopened_authority["literature_projection"][
            "literature_derived_invention_input"
        ]
    ):
        _fail(
            "literature_authority_request_mismatch",
            "invention request detached from its reopened current literature roots",
        )
    try:
        receipt_path = _receipt_path(registered_receipt)
        receipt = validate_research_worker_receipt(
            registered_receipt,
            receipt_path=receipt_path,
            require_live_authority=True,
        )
        summary = receipt_summary(receipt, receipt_path=receipt_path)
    except (OSError, ResearchWorkerIntegrityError) as exc:
        raise LiteratureConditionedInventionError(
            "receipt_replay_failed",
            "registered invention worker receipt failed exact replay",
        ) from exc
    payload = receipt["request_payload"]["payload"]
    expected_payload = {
        "invention_request": request_value,
        "invention_request_digest": request_value["content_digest"],
    }
    expected_context = {
        "request_id": request_value["request_id"],
        "invention_request_digest": request_value["content_digest"],
        "literature_derived_invention_input_digest": request_value[
            "literature_derived_invention_input_digest"
        ],
        "known_taxonomy_commitment_digest": request_value[
            "known_taxonomy_commitment_digest"
        ],
    }
    if (
        receipt["role"] != "high_risk"
        or receipt["operation"] != "high_risk_generation"
        or receipt["outcome_status"] != "accepted"
        or payload != expected_payload
        or receipt["request_payload"]["invocation_context"]
        != expected_context
    ):
        _fail(
            "receipt_request_binding_mismatch",
            "worker receipt changed the sealed invention request",
        )
    inventions, evidence = _validate_worker_output(
        receipt["response_payload"]["output"],
        request=request_value,
    )
    contracts, assessment = _derive_family_contracts(
        request=request_value,
        inventions=inventions,
        evidence=evidence,
    )
    namespace = request_value["namespace"]
    constraints = request_value["target_constraints"]
    source_freeze = build_pre_taxonomy_invention_freeze(
        target_id=namespace["target_id"],
        run_id=namespace["run_id"],
        state_version=namespace["state_version"],
        target_pressure=constraints["target_pressure"],
        root_contradictions=constraints["root_contradictions"],
        protected_successes=constraints["protected_successes"],
        raw_inventions=inventions,
        known_taxonomy=known_taxonomy,
        generator_authority_digest=receipt["content_digest"],
    )
    projection = {
        "schema_version": "3.0.0",
        "artifact_kind": "literature_only_projection_v3",
        "literature_derived_invention_input": request_value[
            "literature_derived_invention_input"
        ],
    }
    projection = {**projection, "content_digest": canonical_digest(projection)}
    conditioned_freeze = build_literature_conditioned_invention_freeze(
        source_freeze,
        literature_projection=projection,
        causal_family_contracts=contracts,
    )
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "literature_conditioned_invention_execution",
        "execution_id": stable_identifier(
            "literature-conditioned-invention-execution",
            request_value["content_digest"],
            receipt["content_digest"],
            conditioned_freeze["content_digest"],
            assessment["content_digest"],
        ),
        "request": request_value,
        "request_digest": request_value["content_digest"],
        "registered_receipt": copy.deepcopy(receipt),
        "receipt_file_sha256": summary["receipt_file_sha256"],
        "receipt_byte_length": summary["receipt_byte_length"],
        "worker_output": copy.deepcopy(
            receipt["response_payload"]["output"]
        ),
        "source_invention_freeze": source_freeze,
        "derived_causal_family_contracts": contracts,
        "conditioned_invention_freeze": conditioned_freeze,
        "task_grounded_family_assessment": assessment,
        "causal_order": [
            "semantic_literature_and_target_request_sealed",
            "registered_worker_invoked",
            "raw_inventions_authored",
            "independent_family_structure_derived",
            "conditioned_freeze_sealed",
        ],
        "direct_theory_preference_proof_schedule_experiment_effect": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    packet = _seal(core)
    validate_payload(packet, SCHEMA_NAME)
    return packet


def validate_literature_conditioned_invention_execution(
    packet: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen the registered worker and rebuild the complete execution."""

    value = copy.deepcopy(dict(packet))
    validate_payload(value, SCHEMA_NAME)
    _verify_seal(value, "content_digest", "invention execution")
    expected = build_literature_conditioned_invention_execution(
        request=value["request"],
        registered_receipt=value["registered_receipt"],
        known_taxonomy=known_taxonomy,
    )
    if value != expected:
        _fail(
            "execution_replay_mismatch",
            "request, receipt, output, family derivation, or freeze changed",
        )
    return copy.deepcopy(value)


def run_registered_literature_conditioned_invention(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    target_pressure: str,
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
    known_taxonomy: Mapping[str, Any],
    run_root: Path | str,
    requested_count: int = 8,
    matched_budget: Mapping[str, Any] | None = None,
    require_kernel_isolation: bool = False,
) -> dict[str, Any]:
    """Execute the registered semantic-literature invention producer."""

    request = build_literature_conditioned_invention_request(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        target_pressure=target_pressure,
        root_contradictions=root_contradictions,
        protected_successes=protected_successes,
        literature_projection=literature_projection,
        literature_bundle=literature_bundle,
        governed_present_use_at=governed_present_use_at,
        known_taxonomy=known_taxonomy,
        requested_count=requested_count,
    )
    budget = _normalized_budget(matched_budget)
    study_id = stable_identifier(
        "literature-conditioned-invention-study",
        request["content_digest"],
        budget,
        require_kernel_isolation,
    )
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_literature_conditioned_invention_worker_v1.py"
    )
    adapter = ResearchWorkerAdapter(
        study_id=study_id,
        run_root=run_root,
        worker_script=worker_script,
        approved_dependency_paths=(
            Path(__file__).resolve(),
            Path(__file__).resolve().parents[1] / "spec" / SCHEMA_NAME,
        ),
        require_kernel_isolation=require_kernel_isolation,
    )
    receipt = adapter.invoke(
        role="high_risk",
        operation="high_risk_generation",
        invocation_context={
            "request_id": request["request_id"],
            "invention_request_digest": request["content_digest"],
            "literature_derived_invention_input_digest": request[
                "literature_derived_invention_input_digest"
            ],
            "known_taxonomy_commitment_digest": request[
                "known_taxonomy_commitment_digest"
            ],
        },
        payload={
            "invention_request": request,
            "invention_request_digest": request["content_digest"],
        },
        budget=budget,
    )
    return build_literature_conditioned_invention_execution(
        request=request,
        registered_receipt=receipt,
        known_taxonomy=known_taxonomy,
    )


def build_literature_counterfactual_inputs(
    current_input: Mapping[str, Any],
    *,
    historical_input: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    """Build the required semantic literature intervention worlds."""

    current = copy.deepcopy(dict(current_input))
    _verify_seal(current, "content_digest", "current literature input")
    causal_rows = current["causal_inputs"]
    worlds: list[dict[str, Any]] = [
        {
            "world_id": "current",
            "intervention": "identity",
            "input": current,
            "predicted_effect": "semantic_output_may_change_or_explicit_null",
        },
        {
            "world_id": "historical",
            "intervention": "historical_snapshot_substitution",
            "input": copy.deepcopy(dict(historical_input))
            if historical_input is not None
            else None,
            "predicted_effect": "semantic_output_may_change_or_explicit_null",
        },
        {
            "world_id": "no_literature",
            "intervention": "remove_all_semantic_literature",
            "input": None,
            "predicted_effect": "semantic_output_must_change_or_explicit_null",
        },
    ]
    for index, row in enumerate(causal_rows):
        retained = [
            copy.deepcopy(item)
            for other_index, item in enumerate(causal_rows)
            if other_index != index
        ]
        variant = copy.deepcopy(current)
        variant["causal_inputs"] = retained
        variant["input_id"] = stable_identifier(
            "literature-counterfactual-removal",
            current["input_id"],
            row["causal_input_id"],
        )
        variant.pop("content_digest", None)
        variant = _seal(variant)
        worlds.append(
            {
                "world_id": f"removal.{index}",
                "intervention": "remove_one_semantic_input",
                "input": variant,
                "predicted_effect": (
                    "semantic_output_must_change_or_explicit_null"
                ),
            }
        )
    for status in ("substituted", "corrected", "superseded", "retracted"):
        altered = copy.deepcopy(causal_rows)
        source_row = altered[0]
        if status in {"superseded", "retracted"}:
            altered = altered[1:]
        else:
            altered[0] = _normalize_counterfactual_causal_row(
                source_row,
                intervention=status,
            )
        variant = _counterfactual_literature_input(
            current,
            rows=altered,
            world_id=status,
            removed_source_id=(
                str(source_row["source_id"])
                if status in {"superseded", "retracted"}
                else None
            ),
        )
        worlds.append(
            {
                "world_id": status,
                "intervention": f"semantic_input_{status}",
                "input": variant,
                "predicted_effect": (
                    "semantic_output_must_change_or_explicit_null"
                ),
            }
        )
    if historical_input is not None:
        historical = copy.deepcopy(dict(historical_input))
        _verify_seal(historical, "content_digest", "historical literature input")
        worlds[1]["input"] = historical
    return worlds


def _normalize_counterfactual_causal_row(
    raw: Mapping[str, Any],
    *,
    intervention: str,
) -> dict[str, Any]:
    """Recompute a coherent study-only claim/warrant/assimilation row."""

    if intervention not in {"substituted", "corrected"}:
        _fail(
            "counterfactual_intervention_invalid",
            "only replacement worlds can normalize an active causal row",
        )
    row = copy.deepcopy(dict(raw))
    prior_claim_digest = _text(row.get("claim_digest"), "claim_digest")
    replacement = {
        "study_intervention": intervention,
        "replaces_claim_digest": prior_claim_digest,
        "replacement_claim": (
            "A counterfactual source makes the opposite target-relevant "
            "distinction explicit."
            if intervention == "substituted"
            else "A corrected source narrows the claim to its warranted scope."
        ),
    }
    replacement_digest = canonical_digest(replacement)
    row["exact_claim"] = replacement
    row["claim_digest"] = replacement_digest
    if "claim_provenance" in row:
        row["claim_provenance"] = {
            "provenance_kind": "counterfactual_study_replacement",
            "intervention": intervention,
            "replaces_claim_digest": prior_claim_digest,
            "truth_authority": None,
        }
    warrants = []
    for index, raw_warrant in enumerate(row.get("semantic_warrants", [])):
        warrant = copy.deepcopy(dict(raw_warrant))
        warrant["claim_digest"] = replacement_digest
        if "warrant_id" in warrant:
            warrant["warrant_id"] = stable_identifier(
                "counterfactual-semantic-warrant",
                intervention,
                prior_claim_digest,
                index,
            )
        if "relation" in warrant:
            warrant["relation"] = (
                "contradicts"
                if intervention == "substituted"
                else "leaves_open"
            )
        warrants.append(warrant)
    row["semantic_warrants"] = warrants
    row["semantic_warrant_set_digest"] = canonical_digest(warrants)
    correction_status = (
        "corrected"
        if intervention == "corrected"
        else str(row.get("source_correction_status") or "none_known")
    )
    row["source_correction_status"] = correction_status
    row["counterfactual_intervention"] = intervention
    row["assimilation_delta"] = {
        "event_type": (
            "reframe" if intervention == "corrected" else "reprioritize"
        ),
        "source_correction_status": correction_status,
        "semantic_relations": sorted(
            {
                str(warrant.get("relation") or "unresolved")
                for warrant in warrants
            }
        ),
        "correction_or_supersession_active": intervention == "corrected",
        "authority": "bounded_counterfactual_study_input_only",
    }
    row["causal_input_id"] = stable_identifier(
        "literature-counterfactual-causal-input",
        row.get("source_id"),
        row.get("source_version"),
        intervention,
        replacement_digest,
    )
    row.pop("causal_input_digest", None)
    return {
        **row,
        "causal_input_digest": canonical_digest(row),
    }


def _counterfactual_literature_input(
    current: Mapping[str, Any],
    *,
    rows: Sequence[Mapping[str, Any]],
    world_id: str,
    removed_source_id: str | None,
) -> dict[str, Any]:
    """Rebuild input identity and correction indexes from normalized rows."""

    variant = copy.deepcopy(dict(current))
    normalized_rows = [copy.deepcopy(dict(row)) for row in rows]
    variant["causal_inputs"] = normalized_rows
    variant["input_id"] = stable_identifier(
        "literature-counterfactual-input",
        current["input_id"],
        world_id,
        [row.get("causal_input_digest") for row in normalized_rows],
    )
    if "corrected_or_superseded_source_ids" in variant:
        variant["corrected_or_superseded_source_ids"] = sorted(
            {
                str(row["source_id"])
                for row in normalized_rows
                if row.get("source_correction_status")
                in {"corrected", "superseded"}
            }
            | ({removed_source_id} if world_id == "superseded" else set())
        )
    if "retracted_source_ids" in variant:
        variant["retracted_source_ids"] = sorted(
            {
                str(row["source_id"])
                for row in normalized_rows
                if row.get("source_correction_status") == "retracted"
            }
            | ({removed_source_id} if world_id == "retracted" else set())
        )
    limits = list(variant.get("coverage_limits", []))
    limits.append(
        f"Counterfactual {world_id} world; no source-truth authority."
    )
    variant["coverage_limits"] = limits
    variant.pop("content_digest", None)
    return _seal(variant)


def run_literature_invention_counterfactual_study(
    *,
    base_request: Mapping[str, Any],
    historical_literature_input: Mapping[str, Any] | None,
    run_root: Path | str,
    matched_budget: Mapping[str, Any] | None = None,
    max_workers: int = 4,
) -> dict[str, Any]:
    """Run all required literature interventions with one sealed target."""

    request = copy.deepcopy(dict(base_request))
    _verify_seal(request, "content_digest", "base invention request")
    worlds = build_literature_counterfactual_inputs(
        request["literature_derived_invention_input"],
        historical_input=historical_literature_input,
    )
    if not 1 <= max_workers <= len(worlds):
        _fail("worker_count_invalid", "counterfactual worker count is invalid")
    budget = _normalized_budget(matched_budget)
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_literature_conditioned_invention_worker_v1.py"
    )
    study_id = stable_identifier(
        "literature-invention-counterfactual-study",
        request["content_digest"],
        [
            {
                "world_id": world["world_id"],
                "input_digest": (
                    world["input"]["content_digest"]
                    if world["input"] is not None
                    else None
                ),
            }
            for world in worlds
        ],
        budget,
    )
    adapter = ResearchWorkerAdapter(
        study_id=study_id,
        run_root=run_root,
        worker_script=worker_script,
        approved_dependency_paths=(Path(__file__).resolve(),),
    )

    def invoke(world: Mapping[str, Any]) -> dict[str, Any]:
        world_request = copy.deepcopy(request)
        if world["input"] is None:
            world_request["literature_derived_invention_input"] = {
                "schema_version": "1.0.0",
                "artifact_kind": "literature_derived_invention_input",
                "input_id": stable_identifier(
                    "no-literature-input", request["request_id"]
                ),
                "target_id": request["namespace"]["target_id"],
                "causal_inputs": [],
                "coverage_limits": [
                    "Counterfactual no-literature world."
                ],
            }
            world_request["literature_derived_invention_input"] = _seal(
                world_request["literature_derived_invention_input"]
            )
        else:
            world_request["literature_derived_invention_input"] = copy.deepcopy(
                world["input"]
            )
        world_request["literature_derived_invention_input_digest"] = (
            world_request["literature_derived_invention_input"][
                "content_digest"
            ]
        )
        world_request["request_id"] = stable_identifier(
            "literature-invention-counterfactual-request",
            request["request_id"],
            world["world_id"],
            world_request["literature_derived_invention_input_digest"],
        )
        world_request.pop("content_digest", None)
        world_request = _seal(world_request)
        receipt = adapter.invoke(
            role="high_risk",
            operation="high_risk_generation",
            invocation_context={
                "request_id": world_request["request_id"],
                "invention_request_digest": world_request["content_digest"],
                "literature_derived_invention_input_digest": world_request[
                    "literature_derived_invention_input_digest"
                ],
                "known_taxonomy_commitment_digest": world_request[
                    "known_taxonomy_commitment_digest"
                ],
            },
            payload={
                "invention_request": world_request,
                "invention_request_digest": world_request["content_digest"],
            },
            budget=budget,
        )
        output = receipt["response_payload"]["output"]
        return {
            "world_id": world["world_id"],
            "intervention": world["intervention"],
            "predicted_effect": world["predicted_effect"],
            "request_digest": world_request["content_digest"],
            "literature_input_digest": world_request[
                "literature_derived_invention_input_digest"
            ],
            "receipt_id": receipt["receipt_id"],
            "receipt_digest": receipt["content_digest"],
            "semantic_output_signature": output[
                "semantic_output_signature"
            ],
            "identity_erased_conceptual_signature": output[
                "identity_erased_conceptual_signature"
            ],
            "worker_explicit_null": output.get("literature_effect_null"),
        }

    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(invoke, world): world["world_id"] for world in worlds
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    ordered = [results[world["world_id"]] for world in worlds]
    current_receipt_signature = results["current"][
        "semantic_output_signature"
    ]
    current_conceptual_signature = results["current"][
        "identity_erased_conceptual_signature"
    ]
    for row in ordered:
        if row["world_id"] == "current":
            row["observed_effect"] = "reference"
            row["provenance_only_change"] = False
            row["comparative_null"] = None
        elif (
            row["identity_erased_conceptual_signature"]
            != current_conceptual_signature
        ):
            row["observed_effect"] = "semantic_output_changed"
            row["provenance_only_change"] = False
            row["comparative_null"] = None
        else:
            row["observed_effect"] = "explicit_null"
            row["provenance_only_change"] = (
                row["semantic_output_signature"]
                != current_receipt_signature
            )
            row["comparative_null"] = {
                "status": "explicit_identity_erased_conceptual_null",
                "reason": (
                    "The intervention changed no identity-erased conceptual "
                    "operation, target grounding, prediction, correction "
                    "trigger, falsifier outcome, or physics-facing action."
                ),
            }
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "literature_invention_counterfactual_study",
        "study_id": study_id,
        "base_request_digest": request["content_digest"],
        "matched_budget": budget,
        "world_order": [world["world_id"] for world in worlds],
        "world_results": ordered,
        "semantic_comparison": {
            "comparator": "identity_and_provenance_erased_conceptual_projection",
            "request_identity_counts_as_effect": False,
            "receipt_identity_counts_as_effect": False,
            "source_or_claim_digest_counts_as_effect": False,
            "correction_status_alone_counts_as_effect": False,
            "explicit_nulls_permitted": True,
        },
        "all_interventions_accounted": True,
        "comparative_benefit_authorized": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    return _seal(core)


__all__ = [
    "AUTHORITY_BOUNDARY",
    "AUTHORITY_NULLS",
    "LiteratureConditionedInventionError",
    "MIN_DISTINCT_FAMILIES",
    "SCHEMA_NAME",
    "SCHEMA_VERSION",
    "build_literature_conditioned_invention_execution",
    "build_literature_conditioned_invention_request",
    "build_literature_counterfactual_inputs",
    "run_literature_invention_counterfactual_study",
    "run_registered_literature_conditioned_invention",
    "validate_literature_conditioned_invention_execution",
]
