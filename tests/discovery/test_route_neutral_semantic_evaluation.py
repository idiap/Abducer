# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused protocol and adversarial tests for route-neutral semantic judgment."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.route_neutral_semantic_evaluation import (
    AUTHORITY_NULLS,
    CONTROL_KINDS,
    DIMENSIONS,
    RouteNeutralSemanticEvaluationError,
    run_route_neutral_semantic_evaluation,
    seal_semantic_evidence,
    validate_route_neutral_semantic_evaluation,
)


_CONCEPTS = {
    "relevance": ("target pressure", "research relevance"),
    "protected_success": ("protected success", "preserved result"),
    "explanatory_depth": ("explanatory mechanism", "mediates dependency"),
    "unification_with_preserved_difference": (
        "unification map",
        "preserved difference",
    ),
    "philosophical_illumination": (
        "ontological commitment",
        "dialectical tension",
    ),
    "falsifiability": ("decisive falsifier", "countermodel test"),
    "correction": ("correction condition", "revision trigger"),
    "conceptual_risk": ("conceptual risk", "high reward"),
    "exact_physics_return": ("physics return", "changed research decision"),
}


def _strong_content(label: str) -> dict[str, str]:
    return {
        dimension: (
            f"The {first} and {second} are linked by a consequence-bearing "
            f"theoretical relation in {label}; because the relation preserves "
            "the exact target distinction, removing it changes an explicit "
            "research obligation and exposes a discriminating correction."
        )
        for dimension, (first, second) in _CONCEPTS.items()
    }


def _weak_content(kind: str) -> dict[str, str]:
    return {
        dimension: (
            f"This {kind} paragraph uses polished general language but supplies "
            "no task-specific mechanism, discriminating consequence, or exact "
            "conceptual obligation for the requested comparison."
        )
        for dimension in DIMENSIONS
    }


def _source_digest(source_id: str, pointer: str) -> str:
    return "sha256:" + hashlib.sha256(f"{source_id}:{pointer}".encode()).hexdigest()


def _evidence(source_id: str, content: dict[str, str]) -> dict[str, Any]:
    return seal_semantic_evidence(
        content,
        evidence_id=f"evidence-{source_id}",
        pointer_source_digests={
            f"/{dimension}": _source_digest(source_id, f"/{dimension}")
            for dimension in DIMENSIONS
        },
    )


def _candidate(candidate_id: str, content: dict[str, str]) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "content": content,
        "sealed_evidence": _evidence(candidate_id, content),
    }


def _control(
    control_id: str,
    kind: str,
    content: dict[str, str],
    *,
    copied_candidate_id: str | None = None,
) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "control_kind": kind,
        "copied_candidate_id": copied_candidate_id,
        "content": content,
        "sealed_evidence": _evidence(control_id, content),
    }


def _inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates = [
        _candidate("theory-alpha", _strong_content("the first explanatory system")),
        _candidate("theory-beta", _strong_content("the second explanatory system")),
    ]
    controls = [
        _control("control-sham", "sham", _weak_content("sham")),
        _control(
            "control-decorative",
            "decorative",
            _weak_content("decorative"),
        ),
        _control(
            "control-irrelevant",
            "irrelevant",
            _weak_content("irrelevant"),
        ),
        _control(
            "control-capable-rival",
            "capable_rival",
            _strong_content("the capable non-route rival"),
        ),
        _control(
            "control-copied-status",
            "copied_status",
            copy.deepcopy(candidates[0]["content"]),
            copied_candidate_id="theory-alpha",
        ),
    ]
    return candidates, controls


def _judge_configurations() -> list[dict[str, Any]]:
    perspectives = (
        (
            "judge-ontological",
            "Ontological analysis asks which explanatory entities carry the exact physical burden.",
        ),
        (
            "judge-dialectical",
            "Dialectical analysis asks which contradiction drives conceptual revision and repair.",
        ),
        (
            "judge-physics-return",
            "Philosophy of physics analysis asks how abstractions return to research decisions.",
        ),
    )
    configurations = []
    for index, (config_id, perspective) in enumerate(perspectives):
        dimension_rules = {}
        for dimension, concepts in _CONCEPTS.items():
            required = (
                [concepts[0]]
                if index == 0
                else [concepts[1]]
                if index == 1
                else list(concepts)
            )
            dimension_rules[dimension] = {
                "pointers": [f"/{dimension}"],
                "required_concepts": required,
                "strongest_objection": (
                    f"The apparent {dimension} gain may merely rename the incumbent "
                    "structure without changing any explanatory dependency or burden."
                ),
                "correction_intervention": (
                    f"Remove the claimed {dimension} relation while preserving every "
                    "other conceptual and physical obligation in the packet."
                ),
                "expected_if_robust": (
                    f"A robust {dimension} proposal should lose a specific explanatory "
                    "connection under that controlled content-level removal."
                ),
                "demotion_trigger": (
                    f"Demote the {dimension} claim if the same physics research "
                    "decision survives unchanged after the registered intervention."
                ),
            }
        configurations.append(
            {
                "config_id": config_id,
                "perspective": perspective,
                "version": "1.0.0",
                "dimension_rules": dimension_rules,
            }
        )
    return configurations


@pytest.fixture(scope="module")
def semantic_evaluation(
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[str, Any]:
    candidates, controls = _inputs()
    return run_route_neutral_semantic_evaluation(
        study_id="route-neutral-semantic-focused",
        run_root=tmp_path_factory.mktemp("semantic-evaluation"),
        candidates=candidates,
        controls=controls,
        judge_configurations=_judge_configurations(),
        counterbalance_entropy="sealed-replayable-semantic-entropy-v1",
    )


def test_complete_content_panel_executes_and_reopens_exact_receipts(
    semantic_evaluation: dict[str, Any],
) -> None:
    assert semantic_evaluation["evaluation_status"] == "completed_internal_calibration"
    assert semantic_evaluation["failure"] is None
    assert semantic_evaluation["preregistration"]["dimensions"] == list(DIMENSIONS)
    assert semantic_evaluation["preregistration"]["noncompensatory"] is True
    assert len(semantic_evaluation["judge_executions"]) == 3
    assert len(
        {row["config_digest"] for row in semantic_evaluation["judge_executions"]}
    ) == 3
    assert all(
        row["receipt_summary"]["outcome_status"] == "accepted"
        and row["receipt_summary"]["semantic_independence_authorized"] is False
        for row in semantic_evaluation["judge_executions"]
    )
    assert semantic_evaluation["panel_seal"]["sealed_before_unblinding"] is True
    assert (
        semantic_evaluation["unblinding_receipt"]["panel_seal_digest"]
        == semantic_evaluation["panel_seal"]["panel_seal_digest"]
    )
    validate_route_neutral_semantic_evaluation(semantic_evaluation)


def test_every_dimension_has_exact_warrants_objection_and_correction(
    semantic_evaluation: dict[str, Any],
) -> None:
    for execution in semantic_evaluation["judge_executions"]:
        for candidate in execution["report"]["candidate_findings"]:
            assert [row["dimension"] for row in candidate["dimensions"]] == list(
                DIMENSIONS
            )
            for finding in candidate["dimensions"]:
                assert finding["warrants"]
                warrant = finding["warrants"][0]
                assert warrant["pointer"] == f"/{finding['dimension']}"
                assert warrant["value_digest"].startswith("sha256:")
                assert warrant["evidence_source_digest"].startswith("sha256:")
                assert (
                    finding["strongest_objection"]["value_digest"]
                    == warrant["value_digest"]
                )
                assert finding["correction_test"]["pointer"] == warrant["pointer"]
                assert len(finding["correction_test"]["demotion_trigger"].split()) >= 6


def test_plural_noncompensatory_preference_and_all_controls_calibrate(
    semantic_evaluation: dict[str, Any],
) -> None:
    assert semantic_evaluation["preference"] == {
        "status": "plural",
        "candidate_ids": ["theory-alpha", "theory-beta"],
        "basis": "noncompensatory_pareto_frontier",
    }
    results = {
        row["control_kind"]: row["status"]
        for row in semantic_evaluation["control_results"]
    }
    assert tuple(sorted(results)) == tuple(sorted(CONTROL_KINDS))
    assert set(results.values()) == {"passed"}
    copied_rows = {
        (row["source_id"], row["dimension"]): row["consensus"]
        for row in semantic_evaluation["dimension_aggregation"]
    }
    assert all(
        copied_rows[("control-copied-status", dimension)]
        == copied_rows[("theory-alpha", dimension)]
        for dimension in DIMENSIONS
    )
    assert semantic_evaluation["authority_nulls"] == AUTHORITY_NULLS


def test_process_failure_returns_typed_null_and_empty_preference(
    tmp_path: Path,
) -> None:
    candidates, controls = _inputs()
    artifact = run_route_neutral_semantic_evaluation(
        study_id="route-neutral-semantic-failed-judge",
        run_root=tmp_path,
        candidates=candidates,
        controls=controls,
        judge_configurations=_judge_configurations(),
        counterbalance_entropy="sealed-replayable-semantic-entropy-v1",
        judge_fault_modes={"judge-dialectical": "exit_nonzero"},
    )
    assert artifact["evaluation_status"] == "NULL"
    assert artifact["failure"]["reason_code"] == "judge_execution_failed"
    assert artifact["preference"] == {
        "status": "empty",
        "candidate_ids": [],
        "basis": "failure_NULL",
    }
    assert artifact["panel_seal"] is None
    assert artifact["unblinding_receipt"] is None
    validate_route_neutral_semantic_evaluation(artifact)


def test_post_judge_source_or_evidence_change_returns_null(
    tmp_path: Path,
) -> None:
    candidates, controls = _inputs()
    reopened = copy.deepcopy(candidates)
    reopened[0]["content"]["relevance"] += (
        " This later mutation changes the committed conceptual surface."
    )
    reopened[0]["sealed_evidence"] = _evidence(
        reopened[0]["candidate_id"], reopened[0]["content"]
    )
    reopened_controls = copy.deepcopy(controls)
    copied = next(
        row
        for row in reopened_controls
        if row["control_kind"] == "copied_status"
    )
    copied["content"] = copy.deepcopy(reopened[0]["content"])
    copied["sealed_evidence"] = _evidence(copied["control_id"], copied["content"])
    artifact = run_route_neutral_semantic_evaluation(
        study_id="route-neutral-semantic-rebinding-failure",
        run_root=tmp_path,
        candidates=candidates,
        controls=controls,
        judge_configurations=_judge_configurations(),
        counterbalance_entropy="sealed-replayable-semantic-entropy-v1",
        post_judge_candidates=reopened,
        post_judge_controls=reopened_controls,
    )
    assert artifact["evaluation_status"] == "NULL"
    assert artifact["failure"]["reason_code"] == "post_judge_rebinding_mismatch"
    assert artifact["preference"]["candidate_ids"] == []
    assert artifact["post_judge_rebinding"]["status"] == "not_performed"


def test_capable_rival_failure_nulls_instead_of_selecting_candidates(
    tmp_path: Path,
) -> None:
    candidates, controls = _inputs()
    capable = next(
        row for row in controls if row["control_kind"] == "capable_rival"
    )
    capable["content"] = _weak_content("incapable-rival")
    capable["sealed_evidence"] = _evidence(
        capable["control_id"], capable["content"]
    )
    artifact = run_route_neutral_semantic_evaluation(
        study_id="route-neutral-semantic-control-failure",
        run_root=tmp_path,
        candidates=candidates,
        controls=controls,
        judge_configurations=_judge_configurations(),
        counterbalance_entropy="sealed-replayable-semantic-entropy-v1",
    )
    assert artifact["evaluation_status"] == "NULL"
    assert artifact["failure"]["reason_code"] == "control_calibration_failure"
    assert artifact["preference"]["status"] == "empty"


def test_report_objection_tamper_is_rejected_before_aggregation(
    semantic_evaluation: dict[str, Any],
) -> None:
    forged = copy.deepcopy(semantic_evaluation)
    forged["judge_executions"][0]["report"]["candidate_findings"][0][
        "dimensions"
    ][0]["strongest_objection"]["text"] = "This objection was replaced."
    # Schema and digest replay are both ahead of aggregation, so an objection or
    # correction substitution cannot affect a preference even if one check
    # catches it before the other.
    with pytest.raises(
        RouteNeutralSemanticEvaluationError,
        match="schema validation|artifact digest",
    ):
        validate_route_neutral_semantic_evaluation(forged)
