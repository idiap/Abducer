# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Separated, request-protocol-blind Pareto adjudication for candidates.

The judge request carries no authored candidate text, route labels, or
privileged candidate metadata.  Its complete request-protocol information
domain is a precommitted rule, opaque 256-bit candidate nonces, and seven typed
evidence-status rows whose evidence is represented only by digests.  This does
not claim host-level denial of the parent process's private nonce mapping.  The
judge performs no scalar aggregation: the only ordered values are ``failed``,
``partial``, and ``satisfied`` and the result is the complete
Pareto-nondominated set.

This is an internal adjudication boundary, not an independent evaluator or a
merit oracle.  Every epistemic and scientific authority remains explicitly
null in the result.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "3.0.0"
INPUT_SCHEMA_NAME = "blind_conceptual_judge_input_v3.schema.json"
OUTPUT_SCHEMA_NAME = "blind_conceptual_judge_output_v3.schema.json"
MAX_CANDIDATES = 1024
CRITERIA = (
    "target_relevance",
    "protected_success_preservation",
    "consequence_specificity",
    "burden_localization",
    "unification_compression",
    "discriminating_falsifier",
    "conceptual_depth",
)
EVIDENCE_STATUSES = ("failed", "partial", "satisfied")
SELECTION_POLICY = "set_valued_pareto_nondomination"
AGGREGATION_POLICY = "no_scalar_aggregation"
CANDIDATE_ORDER_POLICY = "canonical_opaque_nonce_order_order_ignored"

_SHA256_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")
_NONCE_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_REQUEST_KEYS = {
    "schema_version",
    "commission_digest",
    "adjudication_rule",
    "opaque_candidates",
    "request_digest",
}
_RULE_KEYS = {
    "criteria",
    "evidence_statuses",
    "selection_policy",
    "aggregation_policy",
    "ties_allowed",
    "candidate_order_policy",
    "rule_digest",
}
_CANDIDATE_KEYS = {
    "opaque_candidate_nonce",
    "criterion_evidence_ledger",
    "evidence_ledger_digest",
}
_EVIDENCE_KEYS = {
    "criterion",
    "status",
    "support_digest",
    "counterevidence_digest",
    "criterion_digest",
}
_JUDGE_AUTHORITY = {
    "authority_distinct_status": "unavailable",
    "candidate_nonce_randomness_authorized": False,
    "counterbalancing_authorized": False,
    "input_order_authorized": False,
    "candidate_metadata_observed": False,
    "route_labels_observed": False,
    "method_metadata_observed": False,
    "authored_text_observed": False,
    "source_material_observed": False,
    "source_imports_observed": False,
    "count_scoring_applied": False,
    "text_or_length_scoring_applied": False,
    "formal_vocabulary_bonus_applied": False,
    "promotion_authorized": False,
    "external_evidence_authorized": False,
    "evaluator_independence_authorized": False,
    "provider_independence_authorized": False,
    "model_independence_authorized": False,
    "human_independence_authorized": False,
    "hidden_input_independence_authorized": False,
    "cognitive_independence_authorized": False,
    "semantic_independence_authorized": False,
    "creativity_authorized": False,
    "conceptual_merit_authorized": False,
    "relevance_authorized": False,
    "conceptual_depth_authorized": False,
    "philosophical_understanding_authorized": False,
    "unification_power_authorized": False,
    "formal_advantage_authorized": False,
    "category_hott_advantage_authorized": False,
    "physics_value_authorized": False,
    "truth_authorized": False,
    "theorem_authorized": False,
    "continuum_authorized": False,
    "yang_mills_authorized": False,
}


class BlindConceptualJudgeError(ValueError):
    """Raised when the separated judge request is not closed and replayable."""


def canonical_digest(value: Any) -> str:
    """Return the local canonical digest without importing another domain."""

    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise BlindConceptualJudgeError(
            "blind judge input is not canonical-JSON encodable"
        ) from exc
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _fail(message: str) -> None:
    raise BlindConceptualJudgeError(message)


def _strict_mapping(
    raw: Any, expected_keys: set[str], label: str
) -> Mapping[str, Any]:
    if not isinstance(raw, Mapping):
        _fail(f"{label} must be a mapping")
    actual_keys = set(raw)
    if actual_keys != expected_keys:
        _fail(
            f"{label} fields differ; missing={sorted(expected_keys - actual_keys)}, "
            f"extra={sorted(actual_keys - expected_keys)}"
        )
    return raw


def _digest(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        _fail(f"{label} must be a canonical sha256 digest")
    return value


def _self_digest(raw: Mapping[str, Any], field: str, label: str) -> None:
    observed = _digest(raw[field], f"{label}.{field}")
    expected = canonical_digest({key: value for key, value in raw.items() if key != field})
    if observed != expected:
        _fail(f"{label} self digest mismatch")


def validate_adjudication_rule(raw: Any) -> dict[str, Any]:
    """Validate the complete nonaggregating rule frozen before adjudication."""

    rule = copy.deepcopy(
        dict(_strict_mapping(raw, _RULE_KEYS, "adjudication rule"))
    )
    if rule["criteria"] != list(CRITERIA):
        _fail("adjudication rule must name the exact ordered seven criteria")
    if rule["evidence_statuses"] != list(EVIDENCE_STATUSES):
        _fail("adjudication rule may score only failed, partial, and satisfied")
    if (
        rule["selection_policy"] != SELECTION_POLICY
        or rule["aggregation_policy"] != AGGREGATION_POLICY
        or rule["ties_allowed"] is not True
        or rule["candidate_order_policy"] != CANDIDATE_ORDER_POLICY
    ):
        _fail("adjudication rule weakens set-valued order-independent Pareto selection")
    _self_digest(rule, "rule_digest", "adjudication rule")
    return rule


def _validate_evidence_row(
    raw: Any, expected_criterion: str
) -> dict[str, Any]:
    row = copy.deepcopy(
        dict(_strict_mapping(raw, _EVIDENCE_KEYS, "criterion evidence row"))
    )
    if row["criterion"] != expected_criterion:
        _fail("criterion evidence ledger order or identity differs")
    status = row["status"]
    if status not in EVIDENCE_STATUSES:
        _fail("criterion evidence status must be failed, partial, or satisfied")
    support = _digest(
        row["support_digest"], "criterion evidence support", nullable=True
    )
    counterevidence = _digest(
        row["counterevidence_digest"],
        "criterion evidence counterevidence",
        nullable=True,
    )
    if status == "failed" and counterevidence is None:
        _fail("failed criterion evidence requires counterevidence")
    if status == "partial" and (support is None or counterevidence is None):
        _fail("partial criterion evidence requires support and counterevidence")
    if status == "satisfied" and support is None:
        _fail("satisfied criterion evidence requires support")
    _self_digest(row, "criterion_digest", "criterion evidence row")
    return row


def _validate_candidate(raw: Any) -> dict[str, Any]:
    candidate = copy.deepcopy(
        dict(_strict_mapping(raw, _CANDIDATE_KEYS, "opaque candidate"))
    )
    nonce = candidate["opaque_candidate_nonce"]
    if not isinstance(nonce, str) or _NONCE_PATTERN.fullmatch(nonce) is None:
        _fail("opaque candidate nonce must be exactly 256 bits of lowercase hex")
    ledger = candidate["criterion_evidence_ledger"]
    if not isinstance(ledger, list) or len(ledger) != len(CRITERIA):
        _fail("candidate must carry exactly seven criterion evidence rows")
    candidate["criterion_evidence_ledger"] = [
        _validate_evidence_row(row, criterion)
        for row, criterion in zip(ledger, CRITERIA, strict=True)
    ]
    expected_digest = canonical_digest(candidate["criterion_evidence_ledger"])
    if (
        _digest(
            candidate["evidence_ledger_digest"], "candidate evidence ledger digest"
        )
        != expected_digest
    ):
        _fail("candidate evidence ledger digest mismatch")
    return candidate


def validate_judgment_request(raw: Any) -> dict[str, Any]:
    """Validate and defensively copy the judge's complete information domain.

    This standard-library validator deliberately mirrors the versioned input
    schema without loading a schema engine into the isolated judge process.
    """

    request = copy.deepcopy(
        dict(_strict_mapping(raw, _REQUEST_KEYS, "blind judgment request"))
    )
    if request["schema_version"] != SCHEMA_VERSION:
        _fail("blind judgment schema version drift")
    _digest(request["commission_digest"], "commission digest")
    request["adjudication_rule"] = validate_adjudication_rule(
        request["adjudication_rule"]
    )
    candidates = request["opaque_candidates"]
    if (
        not isinstance(candidates, list)
        or not candidates
        or len(candidates) > MAX_CANDIDATES
    ):
        _fail(
            "blind judgment requires between one and "
            f"{MAX_CANDIDATES} opaque candidates"
        )
    request["opaque_candidates"] = [_validate_candidate(row) for row in candidates]
    nonces = [
        candidate["opaque_candidate_nonce"]
        for candidate in request["opaque_candidates"]
    ]
    if len(set(nonces)) != len(nonces):
        _fail("opaque candidate nonces must be unique")
    _self_digest(request, "request_digest", "blind judgment request")
    return request


def _weakly_at_least(left: str, right: str) -> bool:
    """Compare only the declared three-valued evidence statuses."""

    if left == right or left == "satisfied":
        return True
    return left == "partial" and right == "failed"


def _dominates(
    left: Sequence[Mapping[str, Any]], right: Sequence[Mapping[str, Any]]
) -> bool:
    left_statuses = [row["status"] for row in left]
    right_statuses = [row["status"] for row in right]
    return all(
        _weakly_at_least(left_status, right_status)
        for left_status, right_status in zip(
            left_statuses, right_statuses, strict=True
        )
    ) and any(
        left_status != right_status
        for left_status, right_status in zip(
            left_statuses, right_statuses, strict=True
        )
    )


def execute_blind_conceptual_judgment(raw: Any) -> dict[str, Any]:
    """Return every Pareto-nondominated opaque nonce in canonical set order."""

    request = validate_judgment_request(raw)
    candidates = sorted(
        request["opaque_candidates"],
        key=lambda candidate: candidate["opaque_candidate_nonce"],
    )
    preference_set = [
        candidate["opaque_candidate_nonce"]
        for candidate in candidates
        if not any(
            other["opaque_candidate_nonce"]
            != candidate["opaque_candidate_nonce"]
            and _dominates(
                other["criterion_evidence_ledger"],
                candidate["criterion_evidence_ledger"],
            )
            for other in candidates
        )
    ]
    records = [
        {
            "opaque_candidate_nonce": candidate["opaque_candidate_nonce"],
            "criterion_statuses": [
                {
                    "criterion": row["criterion"],
                    "status": row["status"],
                    "criterion_digest": row["criterion_digest"],
                }
                for row in candidate["criterion_evidence_ledger"]
            ],
            "evidence_ledger_digest": candidate["evidence_ledger_digest"],
            "pareto_nondominated": (
                candidate["opaque_candidate_nonce"] in preference_set
            ),
            "preference_rank": None,
            "promotion_authorized": False,
        }
        for candidate in candidates
    ]
    core = {
        "output_kind": "blind_judgment",
        "schema_version": SCHEMA_VERSION,
        "commission_digest": request["commission_digest"],
        "adjudication_rule_digest": request["adjudication_rule"]["rule_digest"],
        "selection_policy": SELECTION_POLICY,
        "preference_semantics": "set",
        "records": records,
        "preference_set": preference_set,
        "judge_authority": copy.deepcopy(_JUDGE_AUTHORITY),
    }
    return {**core, "output_digest": canonical_digest(core)}


def execute_blind_judgment_payload(raw: Any) -> dict[str, Any]:
    """Compatibility spelling for callers of the isolated worker boundary."""

    return execute_blind_conceptual_judgment(raw)


__all__ = [
    "AGGREGATION_POLICY",
    "BlindConceptualJudgeError",
    "CANDIDATE_ORDER_POLICY",
    "CRITERIA",
    "EVIDENCE_STATUSES",
    "INPUT_SCHEMA_NAME",
    "MAX_CANDIDATES",
    "OUTPUT_SCHEMA_NAME",
    "SCHEMA_VERSION",
    "SELECTION_POLICY",
    "canonical_digest",
    "execute_blind_conceptual_judgment",
    "execute_blind_judgment_payload",
    "validate_adjudication_rule",
    "validate_judgment_request",
]
