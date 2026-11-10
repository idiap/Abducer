# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import ast
import copy
import json
import secrets
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery.blind_conceptual_judge_v3 import (
    AGGREGATION_POLICY,
    CANDIDATE_ORDER_POLICY,
    CRITERIA,
    EVIDENCE_STATUSES,
    INPUT_SCHEMA_NAME,
    MAX_CANDIDATES,
    OUTPUT_SCHEMA_NAME,
    SCHEMA_VERSION,
    SELECTION_POLICY,
    BlindConceptualJudgeError,
    canonical_digest,
    execute_blind_conceptual_judgment,
)
from agentic.discovery.research_worker_isolation import ResearchWorkerAdapter


ROOT = Path(__file__).resolve().parents[2]
JUDGE_MODULE = ROOT / "agentic/discovery/blind_conceptual_judge_v3.py"
JUDGE_WORKER = ROOT / "agentic/scripts/run_blind_conceptual_judge_v3.py"
INPUT_SCHEMA = ROOT / "agentic/spec" / INPUT_SCHEMA_NAME
OUTPUT_SCHEMA = ROOT / "agentic/spec" / OUTPUT_SCHEMA_NAME


def _criterion_row(criterion: str, status: str, marker: str) -> dict[str, Any]:
    row = {
        "criterion": criterion,
        "status": status,
        "support_digest": (
            canonical_digest(["support", marker, criterion])
            if status != "failed"
            else None
        ),
        "counterevidence_digest": (
            canonical_digest(["counterevidence", marker, criterion])
            if status != "satisfied"
            else None
        ),
    }
    row["criterion_digest"] = canonical_digest(row)
    return row


def _candidate(
    nonce: str, statuses: list[str], *, marker: str
) -> dict[str, Any]:
    ledger = [
        _criterion_row(criterion, status, marker)
        for criterion, status in zip(CRITERIA, statuses, strict=True)
    ]
    return {
        "opaque_candidate_nonce": nonce,
        "criterion_evidence_ledger": ledger,
        "evidence_ledger_digest": canonical_digest(ledger),
    }


def _rule() -> dict[str, Any]:
    rule = {
        "criteria": list(CRITERIA),
        "evidence_statuses": list(EVIDENCE_STATUSES),
        "selection_policy": SELECTION_POLICY,
        "aggregation_policy": AGGREGATION_POLICY,
        "ties_allowed": True,
        "candidate_order_policy": CANDIDATE_ORDER_POLICY,
    }
    rule["rule_digest"] = canonical_digest(rule)
    return rule


def _request(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    request = {
        "schema_version": SCHEMA_VERSION,
        "commission_digest": canonical_digest("sealed blind commission"),
        "adjudication_rule": _rule(),
        "opaque_candidates": candidates,
    }
    request["request_digest"] = canonical_digest(request)
    return request


def _reseal(request: dict[str, Any]) -> None:
    rule = request["adjudication_rule"]
    rule["rule_digest"] = canonical_digest(
        {key: value for key, value in rule.items() if key != "rule_digest"}
    )
    for candidate in request["opaque_candidates"]:
        for row in candidate["criterion_evidence_ledger"]:
            row["criterion_digest"] = canonical_digest(
                {
                    key: value
                    for key, value in row.items()
                    if key != "criterion_digest"
                }
            )
        candidate["evidence_ledger_digest"] = canonical_digest(
            candidate["criterion_evidence_ledger"]
        )
    request["request_digest"] = canonical_digest(
        {key: value for key, value in request.items() if key != "request_digest"}
    )


def _numeric_values(value: Any) -> list[int | float]:
    if isinstance(value, bool):
        return []
    if isinstance(value, (int, float)):
        return [value]
    if isinstance(value, dict):
        return [
            item
            for child in value.values()
            for item in _numeric_values(child)
        ]
    if isinstance(value, list):
        return [item for child in value for item in _numeric_values(child)]
    return []


def _string_values(value: Any) -> list[str]:
    """Collect only observable strings, never external binding objects."""

    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [
            item
            for key, child in value.items()
            for item in [key, *_string_values(child)]
        ]
    if isinstance(value, list):
        return [item for child in value for item in _string_values(child)]
    return []


def _schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _local_references(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [
            item
            for key, child in value.items()
            for item in (
                [str(child)]
                if key == "$ref"
                else _local_references(child)
            )
        ]
    if isinstance(value, list):
        return [item for child in value for item in _local_references(child)]
    return []


def test_versioned_schemas_meta_validate_and_match_runtime_packets() -> None:
    input_schema = _schema(INPUT_SCHEMA)
    output_schema = _schema(OUTPUT_SCHEMA)
    assert all(
        reference.startswith("#/")
        for reference in [
            *_local_references(input_schema),
            *_local_references(output_schema),
        ]
    )
    request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="schema parity evidence",
            )
        ]
    )
    Draft202012Validator(input_schema).validate(request)
    Draft202012Validator(output_schema).validate(
        execute_blind_conceptual_judgment(request)
    )


def test_closed_judge_returns_the_full_pareto_set_without_scalar_scores() -> None:
    alpha = secrets.token_hex(32)
    beta = secrets.token_hex(32)
    dominated = secrets.token_hex(32)
    request = _request(
        [
            _candidate(
                alpha,
                [
                    "satisfied",
                    "partial",
                    "satisfied",
                    "partial",
                    "satisfied",
                    "partial",
                    "satisfied",
                ],
                marker="alpha evidence",
            ),
            _candidate(
                beta,
                [
                    "partial",
                    "satisfied",
                    "partial",
                    "satisfied",
                    "partial",
                    "satisfied",
                    "partial",
                ],
                marker="beta evidence",
            ),
            _candidate(
                dominated,
                ["failed"] * len(CRITERIA),
                marker="dominated evidence",
            ),
        ]
    )

    result = execute_blind_conceptual_judgment(request)

    assert set(result["preference_set"]) == {alpha, beta}
    assert result["preference_set"] == sorted(result["preference_set"])
    assert result["preference_semantics"] == "set"
    assert _numeric_values(result) == []
    for record in result["records"]:
        assert {
            row["status"]
            for row in record["criterion_statuses"]
        } <= set(EVIDENCE_STATUSES)
        assert record["preference_rank"] is None
        assert record["promotion_authorized"] is False
    authority = result["judge_authority"]
    assert authority["authority_distinct_status"] == "unavailable"
    assert all(
        value is False
        for key, value in authority.items()
        if key != "authority_distinct_status"
    )


def test_formal_and_nonformal_bindings_have_indistinguishable_win_and_cowin_opportunity() -> None:
    formal_nonce = secrets.token_hex(32)
    nonformal_nonce = secrets.token_hex(32)
    equal_statuses = [
        "satisfied",
        "partial",
        "satisfied",
        "partial",
        "satisfied",
        "partial",
        "satisfied",
    ]
    formal = _candidate(
        formal_nonce, equal_statuses, marker="substantive formal evidence"
    )
    nonformal = _candidate(
        nonformal_nonce, equal_statuses, marker="substantive nonformal evidence"
    )
    assert formal["evidence_ledger_digest"] != nonformal["evidence_ledger_digest"]
    request = _request([formal, nonformal])

    first_external_binding = {
        formal_nonce: "formal",
        nonformal_nonce: "capable_nonformal",
    }
    swapped_external_binding = {
        formal_nonce: "capable_nonformal",
        nonformal_nonce: "formal",
    }
    first = execute_blind_conceptual_judgment(request)
    second = execute_blind_conceptual_judgment(copy.deepcopy(request))

    assert set(first["preference_set"]) == {formal_nonce, nonformal_nonce}
    assert first == second
    assert first_external_binding != swapped_external_binding
    observed_strings = set(_string_values(request))
    assert observed_strings.isdisjoint(first_external_binding.values())
    assert observed_strings.isdisjoint(swapped_external_binding.values())

    stronger_nonformal = _request(
        [
            _candidate(
                formal_nonce,
                ["partial"] * len(CRITERIA),
                marker="formal partial evidence",
            ),
            _candidate(
                nonformal_nonce,
                ["satisfied"] * len(CRITERIA),
                marker="nonformal satisfied evidence",
            ),
        ]
    )
    winning_result = execute_blind_conceptual_judgment(stronger_nonformal)
    assert winning_result["preference_set"] == [nonformal_nonce]


def test_candidate_input_permutation_cannot_change_the_judgment() -> None:
    candidates = [
        _candidate(
            secrets.token_hex(32),
            ["partial"] * len(CRITERIA),
            marker=f"candidate {index}",
        )
        for index in range(3)
    ]
    forward = execute_blind_conceptual_judgment(_request(candidates))
    reverse = execute_blind_conceptual_judgment(
        _request(list(reversed(copy.deepcopy(candidates))))
    )
    assert forward == reverse


@pytest.mark.parametrize(
    "injection",
    [
        "top_level_route",
        "candidate_method",
        "criterion_source",
        "rule_order_mapping",
    ],
)
def test_route_method_source_and_order_side_channels_are_rejected(
    injection: str,
) -> None:
    request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="closed evidence",
            )
        ]
    )
    if injection == "top_level_route":
        request["route_id"] = "categorical"
    elif injection == "candidate_method":
        request["opaque_candidates"][0]["method"] = "capable_nonformal"
    elif injection == "criterion_source":
        request["opaque_candidates"][0]["criterion_evidence_ledger"][0][
            "source_path"
        ] = "/tmp/authored-candidate.json"
    else:
        request["adjudication_rule"]["route_order"] = ["formal", "nonformal"]
    _reseal(request)

    assert list(Draft202012Validator(_schema(INPUT_SCHEMA)).iter_errors(request))
    with pytest.raises(BlindConceptualJudgeError, match="fields differ"):
        execute_blind_conceptual_judgment(request)


@pytest.mark.parametrize("invalid_status", [0, 2, "satisfied_by_text_length"])
def test_only_the_three_typed_evidence_statuses_are_accepted(
    invalid_status: Any,
) -> None:
    request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="typed evidence",
            )
        ]
    )
    request["opaque_candidates"][0]["criterion_evidence_ledger"][0][
        "status"
    ] = invalid_status
    _reseal(request)

    with pytest.raises(BlindConceptualJudgeError, match="failed, partial, or satisfied"):
        execute_blind_conceptual_judgment(request)


def test_evidence_and_request_digest_tampering_fail_closed() -> None:
    request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="digest evidence",
            )
        ]
    )
    request["opaque_candidates"][0]["evidence_ledger_digest"] = canonical_digest(
        "substituted ledger"
    )
    request["request_digest"] = canonical_digest(
        {key: value for key, value in request.items() if key != "request_digest"}
    )
    with pytest.raises(BlindConceptualJudgeError, match="ledger digest mismatch"):
        execute_blind_conceptual_judgment(request)

    request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="request digest evidence",
            )
        ]
    )
    request["request_digest"] = canonical_digest("substituted request")
    with pytest.raises(BlindConceptualJudgeError, match="request self digest mismatch"):
        execute_blind_conceptual_judgment(request)


def test_duplicate_nonces_and_reordered_criteria_fail_closed() -> None:
    nonce = secrets.token_hex(32)
    duplicated = _request(
        [
            _candidate(
                nonce,
                ["partial"] * len(CRITERIA),
                marker="first duplicate",
            ),
            _candidate(
                nonce,
                ["satisfied"] * len(CRITERIA),
                marker="second duplicate",
            ),
        ]
    )
    with pytest.raises(BlindConceptualJudgeError, match="nonces must be unique"):
        execute_blind_conceptual_judgment(duplicated)

    reordered = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["partial"] * len(CRITERIA),
                marker="criterion permutation",
            )
        ]
    )
    ledger = reordered["opaque_candidates"][0]["criterion_evidence_ledger"]
    ledger[0], ledger[1] = ledger[1], ledger[0]
    _reseal(reordered)
    assert list(
        Draft202012Validator(_schema(INPUT_SCHEMA)).iter_errors(reordered)
    )
    with pytest.raises(BlindConceptualJudgeError, match="order or identity differs"):
        execute_blind_conceptual_judgment(reordered)


def test_candidate_ceiling_and_output_authority_adversaries_fail_closed() -> None:
    oversized = _request(
        [
            _candidate(
                f"{index:064x}",
                ["partial"] * len(CRITERIA),
                marker=f"bounded candidate {index}",
            )
            for index in range(MAX_CANDIDATES + 1)
        ]
    )
    assert list(Draft202012Validator(_schema(INPUT_SCHEMA)).iter_errors(oversized))
    with pytest.raises(BlindConceptualJudgeError, match="between one and 1024"):
        execute_blind_conceptual_judgment(oversized)

    valid_request = _request(
        [
            _candidate(
                secrets.token_hex(32),
                ["satisfied"] * len(CRITERIA),
                marker="output authority boundary",
            )
        ]
    )
    valid_output = execute_blind_conceptual_judgment(valid_request)
    output_validator = Draft202012Validator(_schema(OUTPUT_SCHEMA))
    output_validator.validate(valid_output)
    authority_escalation = copy.deepcopy(valid_output)
    authority_escalation["judge_authority"]["truth_authorized"] = True
    scalar_rank = copy.deepcopy(valid_output)
    scalar_rank["records"][0]["preference_rank"] = 1
    invented_metadata = copy.deepcopy(valid_output)
    invented_metadata["records"][0]["privileged_binding"] = "withheld"
    for adversary in (authority_escalation, scalar_rank, invented_metadata):
        assert list(output_validator.iter_errors(adversary))


def test_source_import_closure_has_no_author_or_registry_dependency() -> None:
    for path in (JUDGE_MODULE, JUDGE_WORKER):
        source = path.read_text(encoding="utf-8")
        assert "central_conceptual_routes_v3" not in source
        assert "ROUTE_ORDER" not in source
        assert "registries" not in source
        tree = ast.parse(source)
        imported_modules = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            node.module or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        }
        assert not any(
            "central_conceptual" in module or "registr" in module
            for module in imported_modules
        )
    judge_imports = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(ast.parse(JUDGE_MODULE.read_text(encoding="utf-8")))
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        (node.module or "").split(".", 1)[0]
        for node in ast.walk(ast.parse(JUDGE_MODULE.read_text(encoding="utf-8")))
        if isinstance(node, ast.ImportFrom)
    }
    assert judge_imports <= {
        "__future__",
        "copy",
        "hashlib",
        "json",
        "re",
        "typing",
    }


def test_sealed_research_worker_accepts_only_the_judge_operation(
    tmp_path: Path,
) -> None:
    candidate_nonce = secrets.token_hex(32)
    request = _request(
        [
            _candidate(
                candidate_nonce,
                ["satisfied"] * len(CRITERIA),
                marker="worker evidence",
            )
        ]
    )
    adapter = ResearchWorkerAdapter(
        study_id="blind-conceptual-judge-v3",
        run_root=tmp_path / "worker-runs",
        worker_script=JUDGE_WORKER,
        approved_dependency_paths=[JUDGE_MODULE],
    )

    receipt = adapter.invoke(
        role="judge",
        operation="blind_judgment",
        invocation_context={
            "commission_digest": request["commission_digest"],
        },
        payload=request,
    )
    assert receipt["outcome_status"] == "accepted"
    output = receipt["response_payload"]["output"]
    assert output["preference_set"] == [candidate_nonce]
    assert output["judge_authority"]["cognitive_independence_authorized"] is False

    author_receipt = adapter.invoke(
        role="formal_lens",
        operation="formal_lens",
        invocation_context={
            "commission_digest": request["commission_digest"],
        },
        payload=request,
    )
    assert author_receipt["outcome_status"] == "operational_failure"
    assert author_receipt["response_payload"] is None

    side_channel_receipt = adapter.invoke(
        role="judge",
        operation="blind_judgment",
        invocation_context={
            "commission_digest": request["commission_digest"],
            "route_id": "categorical",
        },
        payload=request,
    )
    assert side_channel_receipt["outcome_status"] == "operational_failure"
    assert side_channel_receipt["response_payload"] is None
