# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused invariants for the native conceptual-frontier composition layer.

The tests reuse the governed aggressive-search fixture rather than simulating
its literature, process, or family logic.  They exercise only the new seam:
total retained-branch conversion, route-neutral plural evaluation, exact
causal/currentness binding, and future-only reflection/formal/proof/experiment
descriptors.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery.conceptual_frontier_deepening import (
    AUTHORITY_NULLS,
    COMPOSITION_ORDER,
    ConceptualFrontierDeepeningError,
    build_route_neutral_frontier_candidates,
    run_conceptual_frontier_deepening,
    validate_conceptual_frontier_deepening,
)
from agentic.discovery.contracts import canonical_digest
from agentic.discovery.route_neutral_semantic_evaluation import (
    CONTROL_KINDS,
    DIMENSIONS,
    seal_semantic_evidence,
)
from tests.discovery.test_aggressive_provider_search import _run as _run_aggressive_search
from tests.discovery.test_aggressive_provider_search import _taxonomy


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT / "agentic/spec/conceptual_frontier_deepening_v1.schema.json"
)


def _judge_configurations() -> list[dict[str, Any]]:
    """Three perspectives share evidence pointers but not authored criteria."""

    rows: list[dict[str, Any]] = []
    perspectives = (
        (
            "frontier-ontological-judge",
            "Ontological analysis tracks the physical carrier and its exact conceptual dependence.",
            "conceptual route",
        ),
        (
            "frontier-dialectical-judge",
            "Dialectical analysis tests whether a contradiction produces a localized theoretical revision.",
            "explicit",
        ),
        (
            "frontier-physics-return-judge",
            "Physics return analysis asks whether abstraction changes a concrete research decision.",
            "physics decision",
        ),
    )
    for config_id, perspective, concept in perspectives:
        rules = {}
        for dimension in DIMENSIONS:
            rules[dimension] = {
                "pointers": ["/statement"],
                "required_concepts": [concept],
                "strongest_objection": (
                    f"The apparent {dimension} gain may only rename the incumbent "
                    "burden without changing a theoretical dependency."
                ),
                "correction_intervention": (
                    f"Remove the claimed {dimension} relation while preserving "
                    "every other target obligation and protected success."
                ),
                "expected_if_robust": (
                    f"A robust {dimension} claim should lose one exact conceptual "
                    "connection under the registered intervention."
                ),
                "demotion_trigger": (
                    f"Demote {dimension} when the same physics decision survives "
                    "the correction without any changed theoretical burden."
                ),
            }
        rows.append(
            {
                "config_id": config_id,
                "perspective": perspective,
                "version": "1.0.0",
                "dimension_rules": rules,
            }
        )
    return rows


def _evidence(evidence_id: str, content: dict[str, Any]) -> dict[str, Any]:
    return seal_semantic_evidence(
        content,
        evidence_id=evidence_id,
        pointer_source_digests={
            "/statement": canonical_digest(
                {"evidence_id": evidence_id, "pointer": "/statement"}
            )
        },
    )


def _control(
    *,
    control_id: str,
    control_kind: str,
    content: dict[str, Any],
    copied_candidate_id: str | None = None,
) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "control_kind": control_kind,
        "copied_candidate_id": copied_candidate_id,
        "content": content,
        "sealed_evidence": _evidence(f"evidence-{control_id}", content),
    }


def _controls(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    weak = {
        "statement": (
            "Polished general prose gestures toward broad insight but provides "
            "no task-specific mechanism or discriminating theoretical consequence."
        )
    }
    capable = {
        "statement": (
            "A conceptual route makes one competing mediator explicit and "
            "changes the next physics decision without asserting that it is true."
        )
    }
    copied = copy.deepcopy(candidates[0])
    return [
        _control(
            control_id="frontier-control-sham",
            control_kind="sham",
            content=copy.deepcopy(weak),
        ),
        _control(
            control_id="frontier-control-decorative",
            control_kind="decorative",
            content=copy.deepcopy(weak),
        ),
        _control(
            control_id="frontier-control-irrelevant",
            control_kind="irrelevant",
            content=copy.deepcopy(weak),
        ),
        _control(
            control_id="frontier-control-capable",
            control_kind="capable_rival",
            content=capable,
        ),
        _control(
            control_id="frontier-control-copied",
            control_kind="copied_status",
            copied_candidate_id=copied["candidate_id"],
            content=copied["content"],
        ),
    ]


def _authorship() -> dict[str, Any]:
    return {
        "authorship_id": "frontier-control-set-authorship",
        "author_id": "separate-control-author",
        "author_configuration_digest": canonical_digest(
            {"configuration": "five-control-set-v1"}
        ),
        "authored_before_semantic_evaluation": True,
        "composition_runtime_authored_controls": False,
    }


def _reseal(value: dict[str, Any]) -> None:
    value["content_digest"] = canonical_digest(
        {key: child for key, child in value.items() if key != "content_digest"}
    )


@pytest.fixture(scope="module")
def aggressive_search() -> dict[str, Any]:
    with pytest.MonkeyPatch.context() as monkeypatch:
        return _run_aggressive_search(monkeypatch)


@pytest.fixture(scope="module")
def composition(
    aggressive_search: dict[str, Any],
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[str, Any]:
    configs = _judge_configurations()
    candidates = build_route_neutral_frontier_candidates(
        aggressive_search_execution=aggressive_search,
        known_taxonomy=_taxonomy(),
        judge_configurations=configs,
    )
    return run_conceptual_frontier_deepening(
        aggressive_search_execution=aggressive_search,
        known_taxonomy=_taxonomy(),
        controls=_controls(candidates),
        control_set_authorship=_authorship(),
        judge_configurations=configs,
        semantic_run_root=tmp_path_factory.mktemp("conceptual-frontier"),
        counterbalance_entropy="sealed-conceptual-frontier-counterbalance-v1",
        central_abstraction_modes=("category_theory", "hott"),
        request_proof_v3=True,
        request_descendant_experiment=True,
    )


def test_exact_schema_and_total_route_neutral_projection(
    composition: dict[str, Any],
    aggressive_search: dict[str, Any],
) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    assert schema["additionalProperties"] is False
    validate_conceptual_frontier_deepening(
        composition,
        known_taxonomy=_taxonomy(),
    )
    inputs = composition["semantic_inputs"]
    retained = sorted(
        aggressive_search["retention"]["retained_candidate_aliases"]
    )
    assert [row["candidate_id"] for row in inputs["candidate_rows"]] == retained
    assert inputs["conversion_receipt"]["converted_candidate_ids"] == retained
    assert inputs["conversion_receipt"]["all_retained_branches_converted"] is True
    assert inputs["conversion_receipt"]["typed_family_evidence_preserved"] is True
    assert sorted(row["control_kind"] for row in inputs["control_rows"]) == sorted(
        CONTROL_KINDS
    )

    def keys(value: Any) -> set[str]:
        if isinstance(value, dict):
            return set(value).union(*(keys(child) for child in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(child) for child in value))
        return set()

    assert all(
        keys(row["content"]).isdisjoint(
            {
                "status",
                "mutation_status",
                "candidate_id",
                "branch_id",
                "invention_id",
                "exploration_role",
            }
        )
        for row in inputs["candidate_rows"]
    )


def test_plural_outcome_has_exact_currentness_and_future_only_children(
    composition: dict[str, Any],
) -> None:
    evaluation = composition["semantic_evaluation"]
    plural = composition["plural_outcome"]
    causal = composition["causal_order_currentness_binding"]
    future = composition["future_requests"]
    effects = composition["effect_policy"]
    assert evaluation["evaluation_status"] == "completed_internal_calibration"
    assert evaluation["preference"]["status"] == "plural"
    assert plural["status"] == "plural_internal_calibration_only"
    assert len(plural["candidate_ids"]) >= 2
    assert causal["composition_order"] == list(COMPOSITION_ORDER)
    assert (
        causal["governed_present_use_at"]
        == composition["aggressive_search_execution"]["request"][
            "literature_authority"
        ]["governed_present_use_at"]
    )
    assert {
        row["formal_language"]
        for row in future["central_abstraction_requests"]
    } == {"category_theory", "hott"}
    assert all(
        row["physics_return_required"]
        and not row["formal_vocabulary_preference_bonus"]
        and row["nonauthoritative_future_request"]
        and not row["direct_current_effect"]
        for row in future["central_abstraction_requests"]
    )
    assert future["proof_v3_requests"][0]["canonical_route"] == "proof_v3"
    descendant = future["descendant_experiment_requests"][0]
    assert (
        descendant["required_terminal_reflection_generation"]
        == descendant["future_parent_theory_generation"] + 8
    )
    assert descendant["launch_only_after_future_theory_commit"] is True
    assert all(value is False for key, value in effects.items() if key.endswith("effect"))
    assert effects["proof_and_experiment_children_authoritative_now"] is False
    assert composition["authority_nulls"] == AUTHORITY_NULLS


def test_replay_rejects_a_missing_retained_branch(
    composition: dict[str, Any],
) -> None:
    forged = copy.deepcopy(composition)
    forged["semantic_inputs"]["candidate_rows"].pop()
    _reseal(forged["semantic_inputs"])
    _reseal(forged)
    with pytest.raises(ConceptualFrontierDeepeningError) as raised:
        validate_conceptual_frontier_deepening(
            forged,
            known_taxonomy=_taxonomy(),
            reopen_semantic_receipts=False,
        )
    assert raised.value.reason_code == "retained_candidate_conversion_mismatch"


def test_caller_winners_family_labels_and_same_cycle_effects_are_rejected(
    aggressive_search: dict[str, Any],
    composition: dict[str, Any],
    tmp_path: Path,
) -> None:
    configs = _judge_configurations()
    candidates = build_route_neutral_frontier_candidates(
        aggressive_search_execution=aggressive_search,
        known_taxonomy=_taxonomy(),
        judge_configurations=configs,
    )
    common = {
        "aggressive_search_execution": aggressive_search,
        "known_taxonomy": _taxonomy(),
        "controls": _controls(candidates),
        "control_set_authorship": _authorship(),
        "judge_configurations": configs,
        "semantic_run_root": tmp_path,
        "counterbalance_entropy": "sealed-conceptual-frontier-counterbalance-v1",
    }
    with pytest.raises(ConceptualFrontierDeepeningError) as winner:
        run_conceptual_frontier_deepening(
            **common,
            caller_authored_winners=[candidates[0]["candidate_id"]],
        )
    assert winner.value.reason_code == "caller_authored_selection_forbidden"
    with pytest.raises(ConceptualFrontierDeepeningError) as family:
        run_conceptual_frontier_deepening(
            **common,
            caller_authored_family_labels={
                candidates[0]["candidate_id"]: "invented-family"
            },
        )
    assert family.value.reason_code == "caller_authored_selection_forbidden"

    forged = copy.deepcopy(composition)
    forged["effect_policy"]["same_cycle_experiment_effect"] = True
    _reseal(forged)
    with pytest.raises(ConceptualFrontierDeepeningError) as same_cycle:
        validate_conceptual_frontier_deepening(
            forged,
            known_taxonomy=_taxonomy(),
            reopen_semantic_receipts=False,
        )
    assert same_cycle.value.reason_code in {
        "schema_invalid",
        "same_cycle_effect_forbidden",
    }


def test_route_leakage_and_semantic_null_never_become_preference(
    aggressive_search: dict[str, Any],
    tmp_path: Path,
) -> None:
    configs = _judge_configurations()
    candidates = build_route_neutral_frontier_candidates(
        aggressive_search_execution=aggressive_search,
        known_taxonomy=_taxonomy(),
        judge_configurations=configs,
    )
    leaked_controls = _controls(candidates)
    leaked_controls[0]["content"]["route_id"] = "caller-visible-route"
    with pytest.raises(ConceptualFrontierDeepeningError) as leaked:
        run_conceptual_frontier_deepening(
            aggressive_search_execution=aggressive_search,
            known_taxonomy=_taxonomy(),
            controls=leaked_controls,
            control_set_authorship=_authorship(),
            judge_configurations=configs,
            semantic_run_root=tmp_path / "leaked",
            counterbalance_entropy="sealed-conceptual-frontier-leakage-v1",
        )
    assert leaked.value.reason_code == "route_leakage"

    null_controls = _controls(candidates)
    capable = next(
        row for row in null_controls if row["control_kind"] == "capable_rival"
    )
    capable["content"] = {
        "statement": (
            "Polished generic prose offers no mechanism or discriminating "
            "consequence for this target."
        )
    }
    capable["sealed_evidence"] = _evidence(
        "evidence-frontier-control-capable-null", capable["content"]
    )
    with pytest.raises(ConceptualFrontierDeepeningError) as null:
        run_conceptual_frontier_deepening(
            aggressive_search_execution=aggressive_search,
            known_taxonomy=_taxonomy(),
            controls=null_controls,
            control_set_authorship=_authorship(),
            judge_configurations=configs,
            semantic_run_root=tmp_path / "null",
            counterbalance_entropy="sealed-conceptual-frontier-null-v1",
        )
    assert null.value.reason_code == "semantic_evaluator_null"
