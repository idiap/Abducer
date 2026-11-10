# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executed, receipt-bound reflective assimilation of experiment results."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_payload,
)

from .errors import ExperimentReceiptError, ExperimentRuntimeError
from .runtime import validate_experiment_receipt, validate_experiment_spec


REFLECTION_CONTRACT_VERSION = "post-result-experiment-reflection/1.0.0"
REFLECTION_SCHEMA = "dynamic_experiment_reflection_receipt_v1.schema.json"
_SYNTHESIS_OPERATORS = {
    "reflective-theory-synthesizer",
    "local-reflective-synthesizer",
}


def _top_level_digest(value: Mapping[str, Any], field: str) -> str:
    material = copy.deepcopy(dict(value))
    material.pop(field, None)
    return canonical_digest(material)


def _pending_delta(spec: Mapping[str, Any], receipt: Mapping[str, Any]) -> dict[str, Any]:
    claim = spec["tested_theory_claim"]
    contract = spec["theory_effect_contract"]
    effect = receipt["theory_effect"]
    pending = all(
        (
            receipt["status"] == "counterexample",
            receipt["epistemic_outcome"] == "falsifies_claim",
            claim["claim_kind"] == "theory_premise",
            contract["tested_claim_kind"] == "theory_premise",
            contract["if_falsified"] == "request_registered_premise_revision",
            effect["effect_kind"] == "registered_premise_revision_requested",
            effect["premise_revision_status"] == "requires_reflective_review",
        )
    )
    if pending:
        delta: dict[str, Any] = {
            "status": "pending",
            "kind": "registered_premise_review",
            "tested_claim_id": claim["claim_id"],
            "tested_claim_digest": claim["claim_digest"],
            "theory_programme_id": claim["theory_programme_id"],
            "source_theory_programme_digest": claim["source_theory_programme_digest"],
            "source_reflection_packet_digest": claim["source_reflection_packet_digest"],
            "conceptual_system_ids": list(claim["conceptual_system_ids"]),
            "requested_followup_kind": "reflect",
            "review_reason": "registered_premise_falsified_within_declared_scope",
        }
    else:
        delta = {
            "status": "none", "kind": "none", "tested_claim_id": None,
            "tested_claim_digest": None, "theory_programme_id": None,
            "source_theory_programme_digest": None,
            "source_reflection_packet_digest": None,
            "conceptual_system_ids": [], "requested_followup_kind": None,
            "review_reason": None,
        }
    delta.update(
        {
            "theory_identity_changed": False,
            "ontology_mutation_authorized": False,
            "selection_authorized": False,
            "proof_authorized": False,
            "automatic_evidence_relation_authorized": False,
            "schedule_mutation_authorized": False,
        }
    )
    delta["delta_digest"] = canonical_digest(delta)
    return delta


def _validate_synthesis(
    source_packet: Mapping[str, Any],
    result_packet: Mapping[str, Any],
    experiment_receipt: Mapping[str, Any],
    operator_receipt: Mapping[str, Any],
) -> None:
    validate_payload(dict(source_packet), "reflective_conceptual_discovery_packet.schema.json")
    validate_payload(dict(result_packet), "reflective_conceptual_discovery_packet.schema.json")
    validate_payload(dict(operator_receipt), "discovery_operator_receipt.schema.json")
    operator_id = operator_receipt["operator"]["operator_id"]
    if operator_id not in _SYNTHESIS_OPERATORS or operator_receipt["status"] != "succeeded":
        raise ContractError("post-result reflection lacks a successful synthesizer receipt")
    if result_packet["support_probe"]["disposition"] != "assimilated":
        raise ContractError("post-result synthesizer did not execute assimilation")
    if experiment_receipt["receipt_id"] not in result_packet["support_probe"]["receipt_ids"]:
        raise ContractError("post-result synthesis does not bind the experiment receipt")
    if source_packet["packet_digest"] != experiment_receipt["source_reflection_packet_digest"]:
        raise ContractError("reflection source packet crossed the experiment commission")


def build_experiment_reflection_receipt(
    spec: Mapping[str, Any],
    experiment_receipt: Mapping[str, Any],
    source_reflection_packet: Mapping[str, Any],
    result_reflection_packet: Mapping[str, Any],
    synthesis_operator_receipt: Mapping[str, Any],
    *,
    work_directory: Path | None = None,
) -> dict[str, Any]:
    """Seal proof that a synthesizer actually consumed and reflected on a result."""

    validate_experiment_spec(spec)
    validate_experiment_receipt(
        experiment_receipt, spec, work_directory=work_directory
    )
    _validate_synthesis(
        source_reflection_packet,
        result_reflection_packet,
        experiment_receipt,
        synthesis_operator_receipt,
    )
    operator_id = synthesis_operator_receipt["operator"]["operator_id"]
    reflection_id = stable_identifier(
        "experiment-reflection",
        experiment_receipt["receipt_id"],
        synthesis_operator_receipt["receipt_id"],
        result_reflection_packet["packet_digest"],
    )
    delta = _pending_delta(spec, experiment_receipt)
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "contract_version": REFLECTION_CONTRACT_VERSION,
        "reflection_receipt_id": reflection_id,
        "target_id": spec["target_id"],
        "run_id": spec["run_id"],
        "state_version": spec["state_version"],
        "experiment_binding": {
            "spec_id": spec["spec_id"],
            "execution_id": spec["execution_id"],
            "receipt_id": experiment_receipt["receipt_id"],
            "spec_digest": spec["spec_digest"],
            "receipt_content_digest": experiment_receipt["receipt_content_digest"],
            "output_digest": experiment_receipt["output_digest"],
            "tested_claim_id": spec["tested_theory_claim"]["claim_id"],
            "tested_claim_digest": spec["tested_theory_claim"]["claim_digest"],
            "theory_effect_contract_digest": experiment_receipt[
                "theory_effect_contract_digest"
            ],
        },
        "synthesis_binding": {
            "operator_id": operator_id,
            "operator_receipt_id": synthesis_operator_receipt["receipt_id"],
            "operator_receipt_digest": synthesis_operator_receipt["receipt_digest"],
            "source_reflection_packet_digest": source_reflection_packet["packet_digest"],
            "result_reflection_packet_digest": result_reflection_packet["packet_digest"],
            "experiment_result_consumed": True,
        },
        "epistemic_outcome": experiment_receipt["epistemic_outcome"],
        "decision": (
            "pending_registered_premise_review"
            if delta["status"] == "pending"
            else "record_only"
        ),
        "typed_delta": delta,
        "recommendation_digest": canonical_digest(
            experiment_receipt["reflective_assimilation"]
        ),
        "authority_boundary": {
            "experiment_subordinate_to_theory": True,
            "theory_identity_changed": False,
            "ontology_mutation_authorized": False,
            "theory_selected": False,
            "proof_authorized": False,
            "physical_target_support_authorized": False,
            "automatic_evidence_relation_authorized": False,
            "schedule_mutation_authorized": False,
        },
        "created_at": synthesis_operator_receipt["completed_at"],
    }
    record["reflection_digest"] = _top_level_digest(record, "reflection_digest")
    validate_experiment_reflection_receipt(
        record,
        spec,
        experiment_receipt,
        source_reflection_packet,
        result_reflection_packet,
        synthesis_operator_receipt,
        work_directory=work_directory,
    )
    return record


def validate_experiment_reflection_receipt(
    reflection_receipt: Mapping[str, Any],
    spec: Mapping[str, Any],
    experiment_receipt: Mapping[str, Any],
    source_reflection_packet: Mapping[str, Any],
    result_reflection_packet: Mapping[str, Any],
    synthesis_operator_receipt: Mapping[str, Any],
    *,
    work_directory: Path | None = None,
) -> None:
    """Validate a sealed reflection without treating it as theory authority."""

    try:
        record = dict(reflection_receipt)
        # A reflection receipt is not independently meaningful if its sealed
        # experiment chain no longer validates.  Recheck both endpoints here,
        # including replay/work-directory requirements, before trusting any
        # post-result synthesis or typed delta.
        validate_experiment_spec(spec)
        validate_experiment_receipt(
            experiment_receipt, spec, work_directory=work_directory
        )
        validate_payload(record, REFLECTION_SCHEMA)
        _validate_synthesis(
            source_reflection_packet,
            result_reflection_packet,
            experiment_receipt,
            synthesis_operator_receipt,
        )
        expected_delta = _pending_delta(spec, experiment_receipt)
        if record["typed_delta"] != expected_delta:
            raise ContractError("reflection typed delta is not derived from the registered premise")
        if record["reflection_digest"] != _top_level_digest(record, "reflection_digest"):
            raise ContractError("reflection receipt digest mismatch")
        expected_id = stable_identifier(
            "experiment-reflection",
            experiment_receipt["receipt_id"],
            synthesis_operator_receipt["receipt_id"],
            result_reflection_packet["packet_digest"],
        )
        if record["reflection_receipt_id"] != expected_id:
            raise ContractError("reflection receipt identity mismatch")
        checks = {
            "target_id": spec["target_id"],
            "run_id": spec["run_id"],
            "state_version": spec["state_version"],
            "epistemic_outcome": experiment_receipt["epistemic_outcome"],
            "recommendation_digest": canonical_digest(
                experiment_receipt["reflective_assimilation"]
            ),
        }
        if any(record[key] != value for key, value in checks.items()):
            raise ContractError("reflection receipt crossed its experiment namespace")
        binding = record["experiment_binding"]
        if binding != {
            "spec_id": spec["spec_id"],
            "execution_id": spec["execution_id"],
            "receipt_id": experiment_receipt["receipt_id"],
            "spec_digest": spec["spec_digest"],
            "receipt_content_digest": experiment_receipt["receipt_content_digest"],
            "output_digest": experiment_receipt["output_digest"],
            "tested_claim_id": spec["tested_theory_claim"]["claim_id"],
            "tested_claim_digest": spec["tested_theory_claim"]["claim_digest"],
            "theory_effect_contract_digest": experiment_receipt[
                "theory_effect_contract_digest"
            ],
        }:
            raise ContractError("reflection receipt experiment binding mismatch")
        synthesis = record["synthesis_binding"]
        if synthesis != {
            "operator_id": synthesis_operator_receipt["operator"]["operator_id"],
            "operator_receipt_id": synthesis_operator_receipt["receipt_id"],
            "operator_receipt_digest": synthesis_operator_receipt["receipt_digest"],
            "source_reflection_packet_digest": source_reflection_packet["packet_digest"],
            "result_reflection_packet_digest": result_reflection_packet["packet_digest"],
            "experiment_result_consumed": True,
        }:
            raise ContractError("reflection receipt synthesis binding mismatch")
    except ExperimentRuntimeError:
        raise
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise ExperimentReceiptError(
            "experiment_reflection_receipt_invalid", str(exc)
        ) from exc


__all__ = [
    "REFLECTION_CONTRACT_VERSION",
    "build_experiment_reflection_receipt",
    "validate_experiment_reflection_receipt",
]
