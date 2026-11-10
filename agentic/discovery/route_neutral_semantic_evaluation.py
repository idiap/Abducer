# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Route-neutral, complete-content semantic evaluation with failure-to-null.

This module separates substantive conceptual comparison from structural
integrity checks.  A caller preregisters nine non-compensatory dimensions and
at least three distinct semantic configurations.  Every configuration receives
an independently counterbalanced allocation containing the *complete*
conceptual content and its sealed evidence.  The same file is also a standalone
worker program, allowing :class:`ResearchWorkerAdapter` to execute each judge
behind the repository's strongest available local process boundary and to
persist an immutable command/dependency/resource receipt.

The protocol deliberately does not use ``blind_conceptual_judge_v3``.  Its
worker reads dimension-specific content paths, checks preregistered semantic
concepts, and returns exact JSON-pointer/value-digest warrants plus a strongest
objection and a correction test.  A panel is sealed before source identities
are rebound.  Sham, decorative, irrelevant, capable-rival, and copied-status
controls then calibrate the panel.  Any malformed judge, failed receipt,
control failure, or post-judge source/evidence mismatch produces a typed NULL
artifact with an empty preference.

Process separation is operational evidence only.  The artifact always keeps
host/provider/model/human/cognitive/semantic independence and every
merit/benefit/truth/physics/generalization authority explicitly null.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


SCHEMA_NAME = "route_neutral_semantic_evaluation.schema.json"
DIMENSIONS = (
    "relevance",
    "protected_success",
    "explanatory_depth",
    "unification_with_preserved_difference",
    "philosophical_illumination",
    "falsifiability",
    "correction",
    "conceptual_risk",
    "exact_physics_return",
)
CONTROL_KINDS = (
    "sham",
    "decorative",
    "irrelevant",
    "capable_rival",
    "copied_status",
)
VERDICTS = ("fails", "uncertain", "supports")
AUTHORITY_NULLS = {
    "host_independence": "unavailable",
    "provider_independence": "unavailable",
    "model_independence": "unavailable",
    "human_independence": "unavailable",
    "cognitive_independence": "unavailable",
    "semantic_independence": "unavailable",
    "conceptual_merit_authority": "unavailable_internal_calibration_only",
    "benefit_authority": "unavailable",
    "truth_authority": "unavailable",
    "physics_value_authority": "unavailable",
    "generalization_authority": "unavailable",
}
_FORBIDDEN_CONTENT_KEYS = frozenset(
    {
        "candidate_id",
        "control_id",
        "control_kind",
        "source_id",
        "source_kind",
        "condition_id",
        "route_id",
        "provider_id",
        "model_id",
        "producer_id",
        "proposer_id",
        "winner",
        "preferred",
        "status",
        "lifecycle_status",
        "claimed_score",
        "self_assessment",
    }
)
_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class RouteNeutralSemanticEvaluationError(ValueError):
    """Stable failure at the semantic-evaluation authority boundary."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"route_neutral_semantic_evaluation[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise RouteNeutralSemanticEvaluationError(reason_code, message)


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


def _seal(core: Mapping[str, Any], field: str) -> dict[str, Any]:
    row = copy.deepcopy(dict(core))
    row[field] = _digest(row)
    return row


def _text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _substantive(value: Any, minimum: int = 6) -> bool:
    return len(_WORD.findall(_text(value))) >= minimum


def _normalized_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _pointer(payload: Any, pointer: str) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/") or pointer == "/":
        _fail("invalid_pointer", "semantic warrants require non-root absolute JSON pointers")
    current = payload
    for encoded in pointer[1:].split("/"):
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            _fail("missing_pointer", f"semantic content does not contain {pointer}")
    return current


def _semantic_text(value: Any) -> str:
    if isinstance(value, Mapping):
        return " ".join(_semantic_text(child) for _, child in sorted(value.items()))
    if isinstance(value, list):
        return " ".join(_semantic_text(child) for child in value)
    return _text(value).lower()


def _check_route_neutral_content(
    value: Any, *, source_markers: Sequence[str], path: str = "$"
) -> None:
    """Reject process/status labels while preserving every conceptual field."""

    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            if _normalized_key(key) in _FORBIDDEN_CONTENT_KEYS:
                _fail(
                    "route_label_leak",
                    f"complete conceptual content contains process/status field {path}.{key}",
                )
            _check_route_neutral_content(
                child, source_markers=source_markers, path=f"{path}.{key}"
            )
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _check_route_neutral_content(
                child, source_markers=source_markers, path=f"{path}[{index}]"
            )
        return
    if isinstance(value, str):
        lowered = value.lower()
        for marker in source_markers:
            normalized = marker.strip().lower()
            if len(normalized) >= 8 and re.search(
                rf"(?<![a-z0-9]){re.escape(normalized)}(?![a-z0-9])", lowered
            ):
                _fail(
                    "source_identity_leak",
                    f"complete conceptual content exposes source identity at {path}",
                )


def seal_semantic_evidence(
    content: Mapping[str, Any],
    *,
    evidence_id: str,
    pointer_source_digests: Mapping[str, str],
) -> dict[str, Any]:
    """Seal exact content-pointer claims for later blind and post-judge replay."""

    if not _IDENTIFIER.fullmatch(evidence_id):
        _fail("invalid_evidence_id", "evidence identity is not a canonical identifier")
    if not pointer_source_digests:
        _fail("empty_evidence", "semantic evidence must bind at least one content pointer")
    claims = []
    for pointer, source_digest in sorted(pointer_source_digests.items()):
        if not _DIGEST.fullmatch(str(source_digest)):
            _fail("invalid_source_digest", f"evidence source digest is invalid at {pointer}")
        value = _pointer(content, pointer)
        claims.append(
            {
                "content_pointer": pointer,
                "content_value_digest": _digest(value),
                "source_digest": str(source_digest),
            }
        )
    return _seal(
        {
            "schema_version": "1.0.0",
            "evidence_id": evidence_id,
            "claims": claims,
        },
        "evidence_digest",
    )


def _validate_evidence(content: Mapping[str, Any], evidence: Mapping[str, Any]) -> None:
    required = {"schema_version", "evidence_id", "claims", "evidence_digest"}
    if set(evidence) != required or evidence.get("schema_version") != "1.0.0":
        _fail("malformed_evidence", "sealed semantic evidence has an open or unknown shape")
    if not _IDENTIFIER.fullmatch(str(evidence.get("evidence_id", ""))):
        _fail("malformed_evidence", "sealed semantic evidence lacks a valid identity")
    claims = evidence.get("claims")
    if not isinstance(claims, list) or not claims:
        _fail("malformed_evidence", "sealed semantic evidence has no pointer claims")
    seen: set[str] = set()
    for claim in claims:
        if not isinstance(claim, Mapping) or set(claim) != {
            "content_pointer",
            "content_value_digest",
            "source_digest",
        }:
            _fail("malformed_evidence", "semantic evidence claim is not closed")
        pointer = str(claim["content_pointer"])
        if pointer in seen:
            _fail("duplicate_evidence_pointer", f"duplicate evidence claim at {pointer}")
        seen.add(pointer)
        value = _pointer(content, pointer)
        if claim["content_value_digest"] != _digest(value):
            _fail("evidence_content_mismatch", f"evidence digest differs at {pointer}")
        if not _DIGEST.fullmatch(str(claim["source_digest"])):
            _fail("malformed_evidence", f"source digest is invalid at {pointer}")
    expected = _digest({key: value for key, value in evidence.items() if key != "evidence_digest"})
    if evidence.get("evidence_digest") != expected:
        _fail("evidence_digest_mismatch", "sealed semantic evidence digest does not replay")


def _validate_judge_config(config: Mapping[str, Any]) -> dict[str, Any]:
    required = {"config_id", "perspective", "version", "dimension_rules"}
    if set(config) != required:
        _fail("judge_config_open", "judge configuration must have the exact registered fields")
    if not _IDENTIFIER.fullmatch(str(config.get("config_id", ""))):
        _fail("judge_config_invalid", "judge configuration identity is invalid")
    if not _substantive(config.get("perspective"), 5) or not _text(config.get("version")):
        _fail("judge_config_invalid", "judge perspective/version is not substantive")
    rules = config.get("dimension_rules")
    if not isinstance(rules, Mapping) or tuple(sorted(rules)) != tuple(sorted(DIMENSIONS)):
        _fail("judge_config_dimensions", "judge configuration must preregister all nine dimensions")
    for dimension in DIMENSIONS:
        rule = rules[dimension]
        expected = {
            "pointers",
            "required_concepts",
            "strongest_objection",
            "correction_intervention",
            "expected_if_robust",
            "demotion_trigger",
        }
        if not isinstance(rule, Mapping) or set(rule) != expected:
            _fail("judge_rule_open", f"judge rule is incomplete for {dimension}")
        pointers = rule["pointers"]
        concepts = rule["required_concepts"]
        if (
            not isinstance(pointers, list)
            or not pointers
            or len(set(pointers)) != len(pointers)
            or any(not isinstance(item, str) or not item.startswith("/") for item in pointers)
        ):
            _fail("judge_rule_pointer", f"judge pointers are invalid for {dimension}")
        if (
            not isinstance(concepts, list)
            or not concepts
            or len({_text(item).lower() for item in concepts}) != len(concepts)
            or any(not _text(item) for item in concepts)
        ):
            _fail("judge_rule_concepts", f"judge concepts are invalid for {dimension}")
        for field in (
            "strongest_objection",
            "correction_intervention",
            "expected_if_robust",
            "demotion_trigger",
        ):
            if not _substantive(rule[field], 6):
                _fail(
                    "judge_rule_non_substantive",
                    f"{dimension}/{field} lacks a substantive preregistered test",
                )
    return copy.deepcopy(dict(config))


def _source_rows(
    candidates: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    candidate_ids = [str(row.get("candidate_id", "")) for row in candidates]
    control_ids = [str(row.get("control_id", "")) for row in controls]
    all_ids = [*candidate_ids, *control_ids]
    if (
        len(candidate_ids) < 2
        or len(set(all_ids)) != len(all_ids)
        or any(not _IDENTIFIER.fullmatch(item) for item in all_ids)
    ):
        _fail(
            "source_identity_invalid",
            "semantic evaluation requires at least two uniquely identified candidates and controls",
        )
    rows: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for raw in candidates:
        if set(raw) != {"candidate_id", "content", "sealed_evidence"}:
            _fail("candidate_open", "candidate row must contain only identity, content, and evidence")
        source_id = str(raw["candidate_id"])
        content = copy.deepcopy(raw["content"])
        evidence = copy.deepcopy(raw["sealed_evidence"])
        if not isinstance(content, Mapping) or not isinstance(evidence, Mapping):
            _fail("candidate_malformed", f"candidate {source_id} lacks content/evidence objects")
        _check_route_neutral_content(content, source_markers=all_ids)
        _validate_evidence(content, evidence)
        row = {
            "source_id": source_id,
            "source_kind": "candidate",
            "control_kind": None,
            "copied_candidate_id": None,
            "content": content,
            "content_digest": _digest(content),
            "sealed_evidence": evidence,
            "evidence_digest": evidence["evidence_digest"],
        }
        rows.append(row)
        by_id[source_id] = row
    kinds: list[str] = []
    for raw in controls:
        if set(raw) != {
            "control_id",
            "control_kind",
            "copied_candidate_id",
            "content",
            "sealed_evidence",
        }:
            _fail("control_open", "control row must have the exact calibrated-control fields")
        source_id = str(raw["control_id"])
        control_kind = str(raw["control_kind"])
        kinds.append(control_kind)
        content = copy.deepcopy(raw["content"])
        evidence = copy.deepcopy(raw["sealed_evidence"])
        copied_candidate_id = raw["copied_candidate_id"]
        if control_kind not in CONTROL_KINDS:
            _fail("control_kind_invalid", f"unknown semantic control {control_kind}")
        if not isinstance(content, Mapping) or not isinstance(evidence, Mapping):
            _fail("control_malformed", f"control {source_id} lacks content/evidence objects")
        _check_route_neutral_content(content, source_markers=all_ids)
        _validate_evidence(content, evidence)
        if control_kind == "copied_status":
            if copied_candidate_id not in by_id:
                _fail("copied_status_target", "copied-status control target is not a candidate")
            if _digest(content) != by_id[str(copied_candidate_id)]["content_digest"]:
                _fail(
                    "copied_status_content",
                    "copied-status control must preserve complete conceptual content exactly",
                )
        elif copied_candidate_id is not None:
            _fail("control_copy_marker", "only copied-status control may name a copied candidate")
        row = {
            "source_id": source_id,
            "source_kind": "control",
            "control_kind": control_kind,
            "copied_candidate_id": copied_candidate_id,
            "content": content,
            "content_digest": _digest(content),
            "sealed_evidence": evidence,
            "evidence_digest": evidence["evidence_digest"],
        }
        rows.append(row)
        by_id[source_id] = row
    if Counter(kinds) != Counter({kind: 1 for kind in CONTROL_KINDS}):
        _fail(
            "control_set_incomplete",
            "exactly one sham, decorative, irrelevant, capable-rival, and copied-status control is required",
        )
    return rows, by_id


def _source_binding(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_id": row["source_id"],
        "source_kind": row["source_kind"],
        "control_kind": row["control_kind"],
        "copied_candidate_id": row["copied_candidate_id"],
        "content_digest": row["content_digest"],
        "evidence_digest": row["evidence_digest"],
    }


def _preregistration(configs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return _seal(
        {
            "schema_version": "1.0.0",
            "dimensions": list(DIMENSIONS),
            "noncompensatory": True,
            "minimum_judge_executions": 3,
            "judge_config_digests": [_digest(config) for config in configs],
            "control_kinds": list(CONTROL_KINDS),
            "failure_policy": "typed_NULL_with_empty_preference",
            "aggregation_policy": (
                "per-dimension strict majority with any dissent retained; "
                "all dimensions must support eligibility and Pareto comparison never trades dimensions"
            ),
        },
        "preregistration_digest",
    )


def _allocation(
    source_rows: Sequence[Mapping[str, Any]],
    config: Mapping[str, Any],
    *,
    entropy_seed: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    seed_digest = _digest({"sealed_entropy_seed": entropy_seed})
    config_digest = _digest(config)
    ordered = sorted(
        source_rows,
        key=lambda row: _digest(
            {
                "algorithm": "sha256-sealed-seed-v1",
                "seed_digest": seed_digest,
                "config_digest": config_digest,
                "source_identity_digest": _digest(row["source_id"]),
                "content_digest": row["content_digest"],
            }
        ),
    )
    blind_rows = []
    bindings: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(ordered, 1):
        alias = f"option-{index:02d}"
        blind_rows.append(
            {
                "candidate_alias": alias,
                "content": copy.deepcopy(row["content"]),
                "content_digest": row["content_digest"],
                "sealed_evidence": copy.deepcopy(row["sealed_evidence"]),
                "evidence_digest": row["evidence_digest"],
            }
        )
        bindings[alias] = _source_binding(row)
    core = {
        "schema_version": "1.0.0",
        "config_id": config["config_id"],
        "config_digest": config_digest,
        "counterbalancing": {
            "seed_digest": seed_digest,
            "algorithm": "sha256-sealed-seed-v1",
            "candidate_order_digest": _digest(
                [row["content_digest"] for row in blind_rows]
            ),
            "source_identities_withheld": True,
            "route_and_status_labels_withheld": True,
        },
        "complete_content": True,
        "blind_candidates": blind_rows,
    }
    return _seal(core, "allocation_digest"), bindings


def _evidence_claim_by_pointer(evidence: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row["content_pointer"]): row for row in evidence["claims"]}


def _worker_finding(
    blind_candidate: Mapping[str, Any],
    *,
    dimension: str,
    rule: Mapping[str, Any],
    perspective: str,
) -> dict[str, Any]:
    content = blind_candidate["content"]
    evidence = blind_candidate["sealed_evidence"]
    evidence_by_pointer = _evidence_claim_by_pointer(evidence)
    warrants = []
    combined_parts = []
    for pointer in rule["pointers"]:
        value = _pointer(content, pointer)
        claim = evidence_by_pointer.get(pointer)
        if claim is None or claim["content_value_digest"] != _digest(value):
            _fail(
                "judge_evidence_missing",
                f"judge cannot warrant {dimension} from sealed evidence at {pointer}",
            )
        combined_parts.append(_semantic_text(value))
        warrants.append(
            {
                "pointer": pointer,
                "value_digest": _digest(value),
                "evidence_source_digest": claim["source_digest"],
                "explanation": (
                    f"This exact content path is the preregistered semantic surface "
                    f"used by the {dimension} judgment."
                ),
            }
        )
    combined = " ".join(combined_parts)
    concepts = [_text(item).lower() for item in rule["required_concepts"]]
    matched = [concept for concept in concepts if concept in combined]
    if len(matched) == len(concepts):
        verdict, confidence = "supports", "high"
    elif matched:
        verdict, confidence = "uncertain", "medium"
    else:
        verdict, confidence = "fails", "low"
    anchor = warrants[0]
    return {
        "dimension": dimension,
        "verdict": verdict,
        "confidence_band": confidence,
        "matched_concepts": matched,
        "warrants": warrants,
        "rationale": (
            f"Under the preregistered perspective, {len(matched)} of {len(concepts)} "
            f"dimension-specific concepts are present in the complete warranted content; "
            "no route, status, provider, model, or source identity is available to this judgment."
        ),
        "strongest_objection": {
            "text": _text(rule["strongest_objection"]),
            "pointer": anchor["pointer"],
            "value_digest": anchor["value_digest"],
        },
        "correction_test": {
            "intervention": _text(rule["correction_intervention"]),
            "expected_if_robust": _text(rule["expected_if_robust"]),
            "demotion_trigger": _text(rule["demotion_trigger"]),
            "pointer": anchor["pointer"],
            "value_digest": anchor["value_digest"],
        },
        "perspective_digest": _digest(perspective),
    }


def _worker_report(allocation: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    if allocation.get("config_id") != config.get("config_id"):
        _fail("worker_config_mismatch", "allocation and judge configuration identities differ")
    if allocation.get("config_digest") != _digest(config):
        _fail("worker_config_mismatch", "allocation and judge configuration digests differ")
    findings = []
    for blind_candidate in allocation["blind_candidates"]:
        dimensions = [
            _worker_finding(
                blind_candidate,
                dimension=dimension,
                rule=config["dimension_rules"][dimension],
                perspective=config["perspective"],
            )
            for dimension in DIMENSIONS
        ]
        findings.append(
            {
                "candidate_alias": blind_candidate["candidate_alias"],
                "content_digest": blind_candidate["content_digest"],
                "evidence_digest": blind_candidate["evidence_digest"],
                "dimensions": dimensions,
            }
        )
    return _seal(
        {
            "schema_version": "1.0.0",
            "config_id": config["config_id"],
            "config_digest": _digest(config),
            "allocation_digest": allocation["allocation_digest"],
            "candidate_findings": findings,
        },
        "report_digest",
    )


def _validate_worker_report(
    report: Mapping[str, Any],
    allocation: Mapping[str, Any],
    config: Mapping[str, Any],
) -> None:
    if report != _worker_report(allocation, config):
        _fail(
            "judge_report_replay_mismatch",
            "semantic judge report does not replay from complete content and preregistration",
        )
    for candidate in report["candidate_findings"]:
        if [row["dimension"] for row in candidate["dimensions"]] != list(DIMENSIONS):
            _fail("judge_dimension_coverage", "judge did not cover all dimensions in order")
        for finding in candidate["dimensions"]:
            if finding["verdict"] not in VERDICTS or not finding["warrants"]:
                _fail("judge_finding_invalid", "semantic judge finding is incomplete")
            if not _substantive(finding["strongest_objection"]["text"], 6):
                _fail("judge_objection_missing", "semantic finding lacks a strongest objection")
            correction = finding["correction_test"]
            if any(
                not _substantive(correction[field], 6)
                for field in ("intervention", "expected_if_robust", "demotion_trigger")
            ):
                _fail("judge_correction_missing", "semantic finding lacks a correction test")


def _panel_seal(
    preregistration: Mapping[str, Any],
    allocations: Sequence[Mapping[str, Any]],
    executions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return _seal(
        {
            "schema_version": "1.0.0",
            "preregistration_digest": preregistration["preregistration_digest"],
            "allocation_digests": [row["allocation_digest"] for row in allocations],
            "judge_report_digests": [row["report_digest"] for row in executions],
            "execution_receipt_digests": [
                row["receipt_summary"]["receipt_digest"] for row in executions
            ],
            "unblinding_material_excluded": True,
            "sealed_before_unblinding": True,
        },
        "panel_seal_digest",
    )


def _post_judge_rebinding(
    expected_by_id: Mapping[str, Mapping[str, Any]],
    reopened_by_id: Mapping[str, Mapping[str, Any]],
    private_bindings: Mapping[str, Mapping[str, Mapping[str, Any]]],
) -> dict[str, Any]:
    expected = {key: _source_binding(value) for key, value in expected_by_id.items()}
    reopened = {key: _source_binding(value) for key, value in reopened_by_id.items()}
    if expected != reopened:
        _fail(
            "post_judge_rebinding_mismatch",
            "source content or sealed evidence changed after judge execution",
        )
    bindings = []
    for config_id, rows in sorted(private_bindings.items()):
        for alias, binding in sorted(rows.items()):
            if expected.get(binding["source_id"]) != dict(binding):
                _fail(
                    "private_binding_mismatch",
                    "blind alias binding does not match the reopened source/evidence bytes",
                )
            bindings.append(
                {
                    "config_id": config_id,
                    "candidate_alias": alias,
                    **copy.deepcopy(dict(binding)),
                }
            )
    return _seal(
        {
            "status": "passed",
            "source_set_digest": _digest(
                [expected[source_id] for source_id in sorted(expected)]
            ),
            "bindings": bindings,
        },
        "binding_digest",
    )


def _unblinding_receipt(
    panel_seal: Mapping[str, Any], rebinding: Mapping[str, Any]
) -> dict[str, Any]:
    return _seal(
        {
            "schema_version": "1.0.0",
            "panel_seal_digest": panel_seal["panel_seal_digest"],
            "binding_digest": rebinding["binding_digest"],
            "post_panel_seal": True,
            "binding_count": len(rebinding["bindings"]),
        },
        "unblinding_receipt_digest",
    )


def _aggregate(
    executions: Sequence[Mapping[str, Any]],
    rebinding: Mapping[str, Any],
    source_by_id: Mapping[str, Mapping[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    binding_index = {
        (row["config_id"], row["candidate_alias"]): row
        for row in rebinding["bindings"]
    }
    votes: dict[tuple[str, str], list[str]] = {}
    per_judge_profiles: dict[tuple[str, str], tuple[str, ...]] = {}
    for execution in executions:
        config_id = execution["config_id"]
        for finding in execution["report"]["candidate_findings"]:
            source_id = binding_index[(config_id, finding["candidate_alias"])]["source_id"]
            profile = []
            for dimension in finding["dimensions"]:
                key = (source_id, dimension["dimension"])
                votes.setdefault(key, []).append(dimension["verdict"])
                profile.append(dimension["verdict"])
            per_judge_profiles[(config_id, source_id)] = tuple(profile)
    judge_count = len(executions)
    quorum = judge_count // 2 + 1
    rows = []
    consensus_by_source: dict[str, dict[str, str]] = {}
    uncertainty_rows = []
    agreement_dimensions = []
    for source_id in sorted(source_by_id):
        consensus_by_source[source_id] = {}
        for dimension in DIMENSIONS:
            observed = votes.get((source_id, dimension), [])
            counts = Counter(observed)
            if len(observed) != judge_count:
                _fail("aggregation_missing_vote", f"missing judge vote for {source_id}/{dimension}")
            if counts["supports"] >= quorum and counts["fails"] == 0:
                consensus = "supports"
            elif counts["fails"] >= quorum:
                consensus = "fails"
            else:
                consensus = "uncertain"
            agreement = (
                "unanimous"
                if len(counts) == 1
                else "majority_with_dissent"
                if max(counts.values()) >= quorum
                else "unresolved"
            )
            row = {
                "source_id": source_id,
                "dimension": dimension,
                "supports": counts["supports"],
                "uncertain": counts["uncertain"],
                "fails": counts["fails"],
                "consensus": consensus,
                "agreement": agreement,
            }
            rows.append(row)
            consensus_by_source[source_id][dimension] = consensus
            if consensus == "uncertain" or agreement != "unanimous":
                uncertainty_rows.append(
                    {
                        "source_id": source_id,
                        "dimension": dimension,
                        "consensus": consensus,
                        "agreement": agreement,
                    }
                )
    for dimension in DIMENSIONS:
        dimension_rows = [row for row in rows if row["dimension"] == dimension]
        states = Counter(row["agreement"] for row in dimension_rows)
        agreement_dimensions.append(
            {
                "dimension": dimension,
                "unanimous_sources": states["unanimous"],
                "dissenting_sources": states["majority_with_dissent"],
                "unresolved_sources": states["unresolved"],
            }
        )
    candidate_profiles = []
    for source_id, source in sorted(source_by_id.items()):
        if source["source_kind"] != "candidate":
            continue
        profile = consensus_by_source[source_id]
        candidate_profiles.append(
            {
                "candidate_id": source_id,
                "dimension_consensus": [
                    {"dimension": dimension, "consensus": profile[dimension]}
                    for dimension in DIMENSIONS
                ],
                "noncompensatory_eligible": all(
                    profile[dimension] == "supports" for dimension in DIMENSIONS
                ),
                "pareto_dominated_by": [],
            }
        )
    rank = {"fails": 0, "uncertain": 1, "supports": 2}
    for left in candidate_profiles:
        left_vector = [
            rank[row["consensus"]] for row in left["dimension_consensus"]
        ]
        dominators = []
        for right in candidate_profiles:
            if right["candidate_id"] == left["candidate_id"]:
                continue
            right_vector = [
                rank[row["consensus"]] for row in right["dimension_consensus"]
            ]
            if all(r >= l for l, r in zip(left_vector, right_vector, strict=True)) and any(
                r > l for l, r in zip(left_vector, right_vector, strict=True)
            ):
                dominators.append(right["candidate_id"])
        left["pareto_dominated_by"] = sorted(dominators)
    control_results = []
    control_pass = True
    for source_id, source in sorted(source_by_id.items()):
        if source["source_kind"] != "control":
            continue
        profile = consensus_by_source[source_id]
        kind = source["control_kind"]
        if kind in {"sham", "decorative", "irrelevant"}:
            passed = any(value == "fails" for value in profile.values())
            detail = "weak control fails at least one noncompensatory dimension"
        elif kind == "capable_rival":
            passed = all(value == "supports" for value in profile.values())
            detail = "capable rival remains eligible on every noncompensatory dimension"
        else:
            copied = str(source["copied_candidate_id"])
            aggregate_equal = profile == consensus_by_source[copied]
            per_judge_equal = all(
                per_judge_profiles[(execution["config_id"], source_id)]
                == per_judge_profiles[(execution["config_id"], copied)]
                for execution in executions
            )
            passed = aggregate_equal and per_judge_equal
            detail = "copied-status outcome follows identical content under every judge"
        control_results.append(
            {
                "control_id": source_id,
                "control_kind": kind,
                "status": "passed" if passed else "failed",
                "detail": detail,
            }
        )
        control_pass = control_pass and passed
    if not control_pass:
        _fail(
            "control_calibration_failure",
            "one or more substantive semantic controls failed their preregistered behavior",
        )
    frontier = sorted(
        row["candidate_id"]
        for row in candidate_profiles
        if row["noncompensatory_eligible"] and not row["pareto_dominated_by"]
    )
    agreement = {
        "status": (
            "unanimous"
            if not uncertainty_rows
            else "plural_with_dissent_or_uncertainty"
        ),
        "dimensions": agreement_dimensions,
    }
    uncertainty = {
        "status": "none" if not uncertainty_rows else "retained",
        "candidate_dimensions": uncertainty_rows,
        "reason_codes": (
            []
            if not uncertainty_rows
            else ["judge_dissent_or_nondecisive_dimension"]
        ),
    }
    preference = {
        "status": "plural" if frontier else "empty",
        "candidate_ids": frontier,
        "basis": (
            "noncompensatory_pareto_frontier"
            if frontier
            else "no_candidate_passed_every_noncompensatory_dimension"
        ),
    }
    return rows, candidate_profiles, control_results, agreement, uncertainty, preference


def _null_artifact(
    *,
    study_id: str,
    reason_code: str,
    message: str,
    preregistration: Mapping[str, Any] | None = None,
    input_commitment: Mapping[str, Any] | None = None,
    allocations: Sequence[Mapping[str, Any]] = (),
    executions: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    failure = {
        "reason_code": reason_code,
        "message": _text(message) or reason_code,
    }
    failure["message_digest"] = _digest(failure["message"])
    empty_rebinding = _seal(
        {"status": "not_performed", "source_set_digest": None, "bindings": []},
        "binding_digest",
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "route_neutral_semantic_evaluation",
        "evaluation_id": "",
        "study_id": study_id if _IDENTIFIER.fullmatch(study_id) else "invalid-study",
        "evaluation_status": "NULL",
        "preregistration": copy.deepcopy(preregistration),
        "input_commitment": copy.deepcopy(input_commitment),
        "allocations": copy.deepcopy(list(allocations)),
        "judge_executions": copy.deepcopy(list(executions)),
        "panel_seal": None,
        "entropy_replay": None,
        "post_judge_rebinding": empty_rebinding,
        "unblinding_receipt": None,
        "dimension_aggregation": [],
        "candidate_profiles": [],
        "control_results": [],
        "agreement": {"status": "unavailable", "dimensions": []},
        "uncertainty": {
            "status": "total",
            "candidate_dimensions": [],
            "reason_codes": [reason_code],
        },
        "preference": {
            "status": "empty",
            "candidate_ids": [],
            "basis": "failure_NULL",
        },
        "failure": failure,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
    }
    core["evaluation_id"] = (
        "route-neutral-semantic-evaluation."
        + hashlib.sha256(
            _canonical_json(
                {
                    "study_id": core["study_id"],
                    "status": "NULL",
                    "reason_code": reason_code,
                    "input_commitment": input_commitment,
                }
            )
        ).hexdigest()[:24]
    )
    artifact = _seal(core, "content_digest")
    _validate_schema(artifact)
    return artifact


def _validate_schema(artifact: Mapping[str, Any]) -> None:
    from .contracts import ContractError, validate_instance

    try:
        validate_instance(artifact, SCHEMA_NAME)
    except ContractError as exc:
        _fail("schema_validation_failed", str(exc))


def run_route_neutral_semantic_evaluation(
    *,
    study_id: str,
    run_root: Path | str,
    candidates: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
    judge_configurations: Sequence[Mapping[str, Any]],
    counterbalance_entropy: str,
    post_judge_candidates: Sequence[Mapping[str, Any]] | None = None,
    post_judge_controls: Sequence[Mapping[str, Any]] | None = None,
    judge_fault_modes: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Execute, seal, rebind, calibrate, and aggregate one semantic panel.

    All expected protocol failures return a schema-valid NULL artifact.  The
    optional post-judge rows model an authoritative reopen of the source and
    evidence surface; changing either content or evidence after the judges ran
    therefore empties the preference instead of silently rebinding it.
    """

    preregistration: dict[str, Any] | None = None
    input_commitment: dict[str, Any] | None = None
    allocations: list[dict[str, Any]] = []
    executions: list[dict[str, Any]] = []
    try:
        if not _IDENTIFIER.fullmatch(study_id):
            _fail("study_id_invalid", "study identity is not a canonical identifier")
        if not isinstance(counterbalance_entropy, str) or len(counterbalance_entropy) < 12:
            _fail(
                "entropy_invalid",
                "counterbalance entropy must be a sealed string of at least twelve characters",
            )
        configs = [_validate_judge_config(config) for config in judge_configurations]
        config_ids = [row["config_id"] for row in configs]
        config_digests = [_digest(row) for row in configs]
        perspective_digests = [_digest(row["perspective"]) for row in configs]
        if (
            len(configs) < 3
            or len(set(config_ids)) != len(configs)
            or len(set(config_digests)) != len(configs)
            or len(set(perspective_digests)) != len(configs)
        ):
            _fail(
                "judge_panel_not_separately_configured",
                "at least three judges need distinct identities, complete configurations, and perspectives",
            )
        source_rows, source_by_id = _source_rows(candidates, controls)
        preregistration = _preregistration(configs)
        input_commitment = _seal(
            {
                "source_bindings": [
                    _source_binding(source_by_id[source_id])
                    for source_id in sorted(source_by_id)
                ],
                "judge_config_bindings": [
                    {
                        "config_id": config["config_id"],
                        "config_digest": _digest(config),
                        "perspective_digest": _digest(config["perspective"]),
                    }
                    for config in configs
                ],
                "sealed_entropy_digest": _digest(
                    {"sealed_entropy_seed": counterbalance_entropy}
                ),
                "complete_content_committed": True,
                "sealed_evidence_committed": True,
            },
            "input_commitment_digest",
        )
        private_bindings: dict[str, dict[str, dict[str, Any]]] = {}
        by_config = {config["config_id"]: config for config in configs}
        for config in configs:
            allocation, private = _allocation(
                source_rows,
                config,
                entropy_seed=counterbalance_entropy,
            )
            allocations.append(allocation)
            private_bindings[config["config_id"]] = private

        from .research_worker_isolation import (
            ResearchWorkerAdapter,
            receipt_summary,
        )

        adapter = ResearchWorkerAdapter(
            study_id=study_id,
            run_root=run_root,
            worker_script=Path(__file__).resolve(),
            approved_dependency_paths=(
                Path(__file__).resolve(),
                Path(__file__).resolve().parents[1] / "spec" / SCHEMA_NAME,
            ),
            require_kernel_isolation=False,
        )
        faults = dict(judge_fault_modes or {})
        if set(faults) - set(config_ids):
            _fail("judge_fault_target_invalid", "judge fault map names an unknown configuration")
        for allocation in allocations:
            config = by_config[allocation["config_id"]]
            receipt = adapter.invoke(
                role="judge",
                operation="blind_judgment",
                invocation_context={
                    "study_id": study_id,
                    "config_id": config["config_id"],
                    "config_digest": _digest(config),
                    "allocation_digest": allocation["allocation_digest"],
                    "semantic_evaluator": "route_neutral_complete_content_v1",
                },
                payload={
                    "schema_version": "1.0.0",
                    "allocation": allocation,
                    "judge_configuration": config,
                },
                fault_mode=faults.get(config["config_id"]),
            )
            if receipt["outcome_status"] != "accepted":
                _fail(
                    "judge_execution_failed",
                    f"judge {config['config_id']} ended as {receipt['outcome_status']}",
                )
            output = receipt["response_payload"]["output"]
            report = output.get("semantic_report")
            if not isinstance(report, Mapping):
                _fail("judge_report_missing", "accepted judge receipt lacks a semantic report")
            _validate_worker_report(report, allocation, config)
            summary = receipt_summary(receipt)
            executions.append(
                {
                    "config_id": config["config_id"],
                    "config_digest": _digest(config),
                    "allocation_digest": allocation["allocation_digest"],
                    "run_directory": receipt["workspace"]["run_directory"],
                    "receipt_summary": summary,
                    "report": copy.deepcopy(dict(report)),
                    "report_digest": report["report_digest"],
                }
            )
        seal = _panel_seal(preregistration, allocations, executions)

        reopened_candidates = (
            candidates if post_judge_candidates is None else post_judge_candidates
        )
        reopened_controls = controls if post_judge_controls is None else post_judge_controls
        _, reopened_by_id = _source_rows(reopened_candidates, reopened_controls)
        rebinding = _post_judge_rebinding(source_by_id, reopened_by_id, private_bindings)
        unblinding = _unblinding_receipt(seal, rebinding)
        (
            dimension_rows,
            candidate_profiles,
            control_results,
            agreement,
            uncertainty,
            preference,
        ) = _aggregate(executions, rebinding, source_by_id)
        entropy_replay = _seal(
            {
                "algorithm": "sha256-sealed-seed-v1",
                "revealed_after_panel_seal": True,
                "entropy": counterbalance_entropy,
                "entropy_digest": _digest(
                    {"sealed_entropy_seed": counterbalance_entropy}
                ),
                "replay_status": "passed",
            },
            "entropy_replay_digest",
        )
        core = {
            "schema_version": "1.0.0",
            "artifact_kind": "route_neutral_semantic_evaluation",
            "evaluation_id": "",
            "study_id": study_id,
            "evaluation_status": "completed_internal_calibration",
            "preregistration": preregistration,
            "input_commitment": input_commitment,
            "allocations": allocations,
            "judge_executions": executions,
            "panel_seal": seal,
            "entropy_replay": entropy_replay,
            "post_judge_rebinding": rebinding,
            "unblinding_receipt": unblinding,
            "dimension_aggregation": dimension_rows,
            "candidate_profiles": candidate_profiles,
            "control_results": control_results,
            "agreement": agreement,
            "uncertainty": uncertainty,
            "preference": preference,
            "failure": None,
            "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        }
        core["evaluation_id"] = (
            "route-neutral-semantic-evaluation."
            + hashlib.sha256(
                _canonical_json(
                    {
                        "study_id": study_id,
                        "input_commitment_digest": input_commitment[
                            "input_commitment_digest"
                        ],
                        "panel_seal_digest": seal["panel_seal_digest"],
                        "binding_digest": rebinding["binding_digest"],
                    }
                )
            ).hexdigest()[:24]
        )
        artifact = _seal(core, "content_digest")
        validate_route_neutral_semantic_evaluation(artifact)
        return artifact
    except RouteNeutralSemanticEvaluationError as exc:
        return _null_artifact(
            study_id=study_id,
            reason_code=exc.reason_code,
            message=str(exc),
            preregistration=preregistration,
            input_commitment=input_commitment,
            allocations=allocations,
            executions=executions,
        )
    except Exception as exc:
        return _null_artifact(
            study_id=study_id,
            reason_code="unexpected_protocol_failure",
            message=f"{type(exc).__name__}: {exc}",
            preregistration=preregistration,
            input_commitment=input_commitment,
            allocations=allocations,
            executions=executions,
        )


def validate_route_neutral_semantic_evaluation(
    artifact: Mapping[str, Any], *, reopen_receipts: bool = True
) -> None:
    """Replay schema, seals, reports, receipts, rebinding, controls, and preference."""

    _validate_schema(artifact)
    expected_digest = _digest(
        {key: value for key, value in artifact.items() if key != "content_digest"}
    )
    if artifact.get("content_digest") != expected_digest:
        _fail("artifact_digest_mismatch", "semantic evaluation content digest does not replay")
    if artifact.get("authority_nulls") != AUTHORITY_NULLS:
        _fail("authority_overclaim", "semantic evaluation changes a mandatory authority null")
    preregistration = artifact.get("preregistration")
    if artifact["evaluation_status"] == "NULL":
        if (
            artifact["preference"] != {
                "status": "empty",
                "candidate_ids": [],
                "basis": "failure_NULL",
            }
            or artifact["failure"] is None
            or artifact["panel_seal"] is not None
            or artifact["unblinding_receipt"] is not None
        ):
            _fail("null_artifact_invalid", "failed evaluation did not empty its authority")
        if artifact["failure"]["message_digest"] != _digest(
            artifact["failure"]["message"]
        ):
            _fail("null_failure_digest", "NULL failure message digest differs")
        return
    if not isinstance(preregistration, Mapping):
        _fail("preregistration_missing", "completed evaluation lacks preregistration")
    if preregistration.get("dimensions") != list(DIMENSIONS) or (
        preregistration.get("noncompensatory") is not True
    ):
        _fail("preregistration_drift", "semantic dimensions or noncompensation changed")
    expected_preregistration = _digest(
        {
            key: value
            for key, value in preregistration.items()
            if key != "preregistration_digest"
        }
    )
    if preregistration.get("preregistration_digest") != expected_preregistration:
        _fail("preregistration_digest", "preregistration digest does not replay")
    input_commitment = artifact["input_commitment"]
    if input_commitment["input_commitment_digest"] != _digest(
        {
            key: value
            for key, value in input_commitment.items()
            if key != "input_commitment_digest"
        }
    ):
        _fail("input_commitment_digest", "source/configuration commitment does not replay")
    source_bindings = input_commitment["source_bindings"]
    if len({row["source_id"] for row in source_bindings}) != len(source_bindings):
        _fail("input_source_duplicate", "input commitment repeats a source identity")
    config_bindings = input_commitment["judge_config_bindings"]
    if (
        len({row["config_id"] for row in config_bindings}) != len(config_bindings)
        or len({row["config_digest"] for row in config_bindings})
        != len(config_bindings)
        or len({row["perspective_digest"] for row in config_bindings})
        != len(config_bindings)
    ):
        _fail(
            "input_config_duplicate",
            "input commitment does not bind separately configured judges",
        )
    if preregistration["judge_config_digests"] != [
        row["config_digest"] for row in config_bindings
    ]:
        _fail(
            "preregistration_config_mismatch",
            "preregistered judge configurations differ from the input commitment",
        )
    allocations = artifact["allocations"]
    executions = artifact["judge_executions"]
    if len(allocations) < 3 or len(executions) != len(allocations):
        _fail("judge_floor_unmet", "completed panel lacks three executed semantic judges")
    allocation_by_config = {row["config_id"]: row for row in allocations}
    if len(allocation_by_config) != len(allocations):
        _fail("allocation_config_duplicate", "judge allocation identities are not unique")
    config_binding_by_id = {row["config_id"]: row for row in config_bindings}
    if set(allocation_by_config) != set(config_binding_by_id):
        _fail(
            "allocation_config_set_mismatch",
            "allocation set differs from committed judge configurations",
        )
    for allocation in allocations:
        if allocation["config_digest"] != config_binding_by_id[
            allocation["config_id"]
        ]["config_digest"]:
            _fail("allocation_config_mismatch", "allocation configuration digest changed")
        if allocation["counterbalancing"]["seed_digest"] != input_commitment[
            "sealed_entropy_digest"
        ]:
            _fail("allocation_entropy_mismatch", "allocation crossed its sealed entropy")
        if allocation["allocation_digest"] != _digest(
            {
                key: value
                for key, value in allocation.items()
                if key != "allocation_digest"
            }
        ):
            _fail("allocation_digest_mismatch", "blind allocation digest does not replay")
        if allocation["counterbalancing"]["candidate_order_digest"] != _digest(
            [row["content_digest"] for row in allocation["blind_candidates"]]
        ):
            _fail("allocation_order_digest", "blind candidate order digest does not replay")
        aliases = [
            row["candidate_alias"] for row in allocation["blind_candidates"]
        ]
        if aliases != [
            f"option-{index:02d}" for index in range(1, len(aliases) + 1)
        ]:
            _fail("allocation_alias_order", "blind aliases are not a closed position sequence")
        for candidate in allocation["blind_candidates"]:
            if candidate["content_digest"] != _digest(candidate["content"]):
                _fail("blind_content_digest", "complete blind content digest differs")
            _validate_evidence(candidate["content"], candidate["sealed_evidence"])
            if candidate["evidence_digest"] != candidate["sealed_evidence"][
                "evidence_digest"
            ]:
                _fail("blind_evidence_digest", "blind evidence digest differs")
    # The full configuration is bound in each request receipt.  Reopen the
    # receipt first, then replay the exact report from those committed bytes.
    if reopen_receipts:
        from .research_worker_isolation import (
            receipt_summary,
            validate_research_worker_receipt,
        )
        from .benchmark_process import _load_json_object

    for execution in executions:
        allocation = allocation_by_config.get(execution["config_id"])
        if allocation is None or execution["allocation_digest"] != allocation["allocation_digest"]:
            _fail("execution_allocation_mismatch", "judge execution crossed allocations")
        if execution["report_digest"] != execution["report"]["report_digest"]:
            _fail("execution_report_digest", "judge execution report digest differs")
        report = execution["report"]
        if report["report_digest"] != _digest(
            {key: value for key, value in report.items() if key != "report_digest"}
        ):
            _fail("report_digest_mismatch", "semantic judge report digest does not replay")
        blind_by_alias = {
            row["candidate_alias"]: row for row in allocation["blind_candidates"]
        }
        if [
            row["candidate_alias"] for row in report["candidate_findings"]
        ] != list(blind_by_alias):
            _fail("report_candidate_order", "semantic report crossed blind candidate order")
        for candidate_finding in report["candidate_findings"]:
            blind = blind_by_alias[candidate_finding["candidate_alias"]]
            if (
                candidate_finding["content_digest"] != blind["content_digest"]
                or candidate_finding["evidence_digest"] != blind["evidence_digest"]
            ):
                _fail("report_candidate_binding", "semantic finding crossed content/evidence")
            evidence_by_pointer = _evidence_claim_by_pointer(
                blind["sealed_evidence"]
            )
            for finding in candidate_finding["dimensions"]:
                for warrant in finding["warrants"]:
                    value = _pointer(blind["content"], warrant["pointer"])
                    claim = evidence_by_pointer.get(warrant["pointer"])
                    if (
                        warrant["value_digest"] != _digest(value)
                        or claim is None
                        or warrant["evidence_source_digest"]
                        != claim["source_digest"]
                    ):
                        _fail("report_warrant_mismatch", "semantic warrant bytes differ")
                objection = finding["strongest_objection"]
                correction = finding["correction_test"]
                for row in (objection, correction):
                    if row["value_digest"] != _digest(
                        _pointer(blind["content"], row["pointer"])
                    ):
                        _fail(
                            "report_adversary_binding",
                            "objection or correction test crossed its content",
                        )
        if reopen_receipts:
            receipt_path = (
                Path(execution["run_directory"])
                / execution["receipt_summary"]["receipt_ref"]
            )
            receipt = validate_research_worker_receipt(
                _load_json_object(receipt_path),
                receipt_path=receipt_path,
                require_live_authority=True,
            )
            if receipt_summary(receipt) != execution["receipt_summary"]:
                _fail("receipt_reopen_mismatch", "judge receipt summary does not reopen")
            payload = receipt["request_payload"]["payload"]
            config = payload["judge_configuration"]
            if payload["allocation"] != allocation:
                _fail("receipt_allocation_mismatch", "judge receipt request changed allocation")
            _validate_judge_config(config)
            if _digest(config) != execution["config_digest"]:
                _fail("receipt_config_mismatch", "judge receipt request changed configuration")
            _validate_worker_report(execution["report"], allocation, config)
            if (
                receipt["response_payload"]["output"].get("semantic_report")
                != execution["report"]
            ):
                _fail("receipt_report_mismatch", "judge receipt response changed report")
    expected_seal = _panel_seal(preregistration, allocations, executions)
    if artifact["panel_seal"] != expected_seal:
        _fail("panel_seal_mismatch", "pre-unblinding panel seal does not replay")
    rebinding = artifact["post_judge_rebinding"]
    if rebinding["status"] != "passed":
        _fail("rebinding_not_passed", "completed evaluation lacks post-judge rebinding")
    if rebinding["binding_digest"] != _digest(
        {key: value for key, value in rebinding.items() if key != "binding_digest"}
    ):
        _fail("rebinding_digest_mismatch", "post-judge rebinding digest does not replay")
    deduplicated_rebinding = {
        row["source_id"]: {
            key: value
            for key, value in row.items()
            if key not in {"config_id", "candidate_alias"}
        }
        for row in rebinding["bindings"]
    }
    committed_by_id = {row["source_id"]: row for row in source_bindings}
    if deduplicated_rebinding != committed_by_id:
        _fail(
            "rebinding_source_mismatch",
            "post-judge source/evidence binding differs from the input commitment",
        )
    if rebinding["source_set_digest"] != _digest(
        [committed_by_id[source_id] for source_id in sorted(committed_by_id)]
    ):
        _fail("rebinding_source_set_digest", "rebound source-set digest does not replay")
    if artifact["unblinding_receipt"] != _unblinding_receipt(expected_seal, rebinding):
        _fail("unblinding_order_mismatch", "candidate identities were not bound after panel seal")
    entropy = artifact["entropy_replay"]
    if (
        entropy["entropy_digest"]
        != _digest({"sealed_entropy_seed": entropy["entropy"]})
        or entropy["entropy_digest"]
        != artifact["input_commitment"]["sealed_entropy_digest"]
        or entropy["entropy_replay_digest"]
        != _digest(
            {
                key: value
                for key, value in entropy.items()
                if key != "entropy_replay_digest"
            }
        )
    ):
        _fail("entropy_replay_mismatch", "counterbalance entropy does not replay")
    # Reconstruct source descriptors from the post-seal binding and verify every
    # per-judge order against the revealed entropy without needing source prose.
    bindings_by_config: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rebinding["bindings"]:
        bindings_by_config.setdefault(row["config_id"], {})[
            row["candidate_alias"]
        ] = row
    for allocation in allocations:
        rows = bindings_by_config[allocation["config_id"]]
        expected_order = sorted(
            rows.values(),
            key=lambda row: _digest(
                {
                    "algorithm": "sha256-sealed-seed-v1",
                    "seed_digest": entropy["entropy_digest"],
                    "config_digest": allocation["config_digest"],
                    "source_identity_digest": _digest(row["source_id"]),
                    "content_digest": row["content_digest"],
                }
            ),
        )
        observed = [
            rows[row["candidate_alias"]]["source_id"]
            for row in allocation["blind_candidates"]
        ]
        if observed != [row["source_id"] for row in expected_order]:
            _fail("counterbalance_replay_mismatch", "sealed allocation order does not replay")
    source_by_id = {
        row["source_id"]: {
            "source_id": row["source_id"],
            "source_kind": row["source_kind"],
            "control_kind": row["control_kind"],
            "copied_candidate_id": row["copied_candidate_id"],
        }
        for row in rebinding["bindings"]
    }
    (
        dimension_rows,
        candidate_profiles,
        control_results,
        agreement,
        uncertainty,
        preference,
    ) = _aggregate(executions, rebinding, source_by_id)
    expected_outputs = (
        dimension_rows,
        candidate_profiles,
        control_results,
        agreement,
        uncertainty,
        preference,
    )
    observed_outputs = (
        artifact["dimension_aggregation"],
        artifact["candidate_profiles"],
        artifact["control_results"],
        artifact["agreement"],
        artifact["uncertainty"],
        artifact["preference"],
    )
    if observed_outputs != expected_outputs:
        _fail("aggregation_replay_mismatch", "plural semantic aggregation does not replay")


def _validate_worker_request(request: Mapping[str, Any]) -> None:
    required = {
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
    if set(request) != required or request.get("schema_version") != 1:
        _fail("worker_request_open", "worker request envelope is not exact")
    if request.get("role") != "judge" or request.get("operation") != "blind_judgment":
        _fail("worker_role_invalid", "semantic worker only accepts blind judge executions")
    if request.get("payload_digest") != _digest(request.get("payload")):
        _fail("worker_payload_digest", "worker payload digest does not replay")
    requirement = request.get("isolation_requirement")
    if not isinstance(requirement, Mapping):
        _fail("worker_isolation_missing", "worker isolation requirement is absent")
    expected_requirement = _digest(
        {key: value for key, value in requirement.items() if key != "content_digest"}
    )
    if requirement.get("content_digest") != expected_requirement:
        _fail("worker_isolation_digest", "worker isolation requirement does not replay")


def _worker_main() -> int:
    """Standalone worker entrypoint consumed by ``ResearchWorkerAdapter``."""

    try:
        request = json.load(sys.stdin)
        if not isinstance(request, Mapping):
            _fail("worker_request_type", "worker request must be an object")
        _validate_worker_request(request)
        fault_mode = request["fault_mode"]
        if fault_mode == "exit_nonzero":
            return 17
        if fault_mode == "invalid_json":
            sys.stdout.write("{")
            return 0
        if fault_mode == "hang":
            import time

            time.sleep(60)
        payload = request["payload"]
        if set(payload) != {
            "schema_version",
            "allocation",
            "judge_configuration",
        } or payload.get("schema_version") != "1.0.0":
            _fail("worker_semantic_payload_open", "semantic judge payload is not exact")
        config = _validate_judge_config(payload["judge_configuration"])
        report = _worker_report(payload["allocation"], config)
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": "judge",
            "operation": "blind_judgment",
            "request_nonce": request["request_nonce"],
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": {
                "output_kind": "blind_judgment",
                "semantic_report": report,
                "judge_authority": {
                    "status": "internal_process_blind_only",
                    "condition_labels_withheld": True,
                    "strategy_labels_withheld": True,
                    "arm_labels_withheld": True,
                    "authority_distinct_status": "unavailable",
                    "cognitive_independence_authorized": False,
                },
            },
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


__all__ = [
    "AUTHORITY_NULLS",
    "CONTROL_KINDS",
    "DIMENSIONS",
    "RouteNeutralSemanticEvaluationError",
    "run_route_neutral_semantic_evaluation",
    "seal_semantic_evidence",
    "validate_route_neutral_semantic_evaluation",
]


if __name__ == "__main__":
    raise SystemExit(_worker_main())
