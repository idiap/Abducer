# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executable checks for provider-plural aggressive conceptual search."""

from __future__ import annotations

import copy
import json
import time
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery.aggressive_provider_search import (
    AggressiveProviderSearchError,
    build_aggressive_provider_search_request,
    build_target_predeclared_coverage_problem,
    run_aggressive_provider_search,
    solve_target_predeclared_coverage,
    target_constraint_identifiers,
    validate_aggressive_provider_search_execution,
    verify_target_predeclared_coverage_certificate,
)
from agentic.discovery.conceptual_ancestry_v3 import (
    build_conceptual_ancestry_literature_projection,
)
from agentic.discovery.contracts import ContractError, canonical_digest
from tests.domains.test_literature_snapshot_capture_bridge import _generic_fixture
from tests.discovery.test_open_world_creativity import _deep_reflection


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT / "agentic/spec/aggressive_provider_search_execution_v1.schema.json"
)
PRESENT_USE = "2030-01-02T00:00:00Z"
ROOT_CONTRADICTIONS = [
    "Finite relational control and continuum reconstruction impose different burdens.",
    "Carrier independence and explicit physical representation must both survive.",
]
PROTECTED_SUCCESSES = [
    "Preserve finite-volume positivity with explicit correction terms.",
    "Keep distinct physical carriers visible under any proposed unification.",
]
_INTERVENTIONS = (
    "add",
    "remove",
    "reverse",
    "hold_fixed",
    "localize",
    "quotient",
    "couple",
    "decouple",
)
_DIRECTIONS = (
    "increase",
    "decrease",
    "invariant",
    "bifurcate",
    "permit",
    "obstruct",
)
_CORRECTIONS = (
    "abandon",
    "retype",
    "change_relation",
    "split_scope",
    "add_mediator",
    "retract",
)
_POLARITIES = (
    "positive",
    "negative",
    "constraint",
    "dual",
    "constitutive",
    "emergent",
)
_VOCABULARY = (
    ("anchor", "hinge", "horizon"),
    ("braid", "junction", "lattice"),
    ("cascade", "membrane", "quotient"),
    ("defect", "relay", "spectrum"),
    ("ecology", "selector", "history"),
    ("filtration", "stalk", "boundary"),
    ("gradient", "bridge", "vacuum"),
    ("holonomy", "portal", "sector"),
    ("interface", "sheaf", "current"),
    ("kernel", "transport", "witness"),
)


def _taxonomy() -> dict[str, Any]:
    return {
        "archived_orbit": {
            "name": "Archived Orbit",
            "definition": (
                "A deliberately withheld catalogue entry used only to test "
                "pre-taxonomy vocabulary separation."
            ),
        },
        "latent_fold": {
            "name": "Latent Fold",
            "definition": (
                "A second withheld catalogue entry that is absent from every "
                "provider-authored conceptual record."
            ),
        },
    }


def _signature(index: int) -> dict[str, str]:
    return {
        "intervention_kind": _INTERVENTIONS[index % len(_INTERVENTIONS)],
        "prediction_direction": _DIRECTIONS[index % len(_DIRECTIONS)],
        "correction_kind": _CORRECTIONS[index % len(_CORRECTIONS)],
        "mechanism_topology": "chain",
        "relation_polarity": _POLARITIES[index % len(_POLARITIES)],
        "physics_handback_status": "decision_changed",
    }


def _semantic_core(index: int) -> dict[str, Any]:
    source, bridge, target = _VOCABULARY[index]
    return {
        "primitives": [
            f"{source} physical carrier",
            f"{bridge} relational mediator",
            f"{target} observable regime",
        ],
        "relations": [
            {
                "source": f"{source} physical carrier",
                "polarity": _POLARITIES[index % len(_POLARITIES)],
                "target": f"{target} observable regime",
            }
        ],
        "mechanism_steps": [
            (
                f"{source} passes through {bridge} while preserving the exact "
                f"finite constraint in conceptual route {index}."
            ),
            (
                f"{bridge} transfers its correction into {target} before any "
                f"continuum conclusion is considered in route {index}."
            ),
        ],
        "protected_differences": [
            (
                f"{source} finite control remains distinct from {target} "
                f"continuum reconstruction in route {index}."
            )
        ],
        "boundary_regimes": [
            (
                f"The {bridge} degeneracy regime where route {index} returns "
                "to the incumbent comparison."
            )
        ],
        "counterfactual_consequence": (
            f"Removing {bridge} changes the order of the named physical burden "
            f"for {target} in route {index}."
        ),
        "falsifier": (
            f"A {target} countermodel where {source} bypasses {bridge} while "
            f"all route {index} premises remain valid."
        ),
        "correction_condition": (
            f"Revise route {index} when {bridge} fails to carry the protected "
            f"finite relation into {target}."
        ),
    }


def _physics(index: int) -> dict[str, Any]:
    source, bridge, target = _VOCABULARY[index]
    return {
        "status": "decision_changed",
        "physical_carrier": f"{source} comparison carrier {index}",
        "regime_and_quantifiers": (
            f"all declared finite regulators in the {target} regime {index}"
        ),
        "decision_before": (
            f"attempt the incumbent direct estimate before route {index}"
        ),
        "proposed_next_decision": (
            f"first test the {bridge} relation-specific burden in route {index}"
        ),
        "decision_rationale": (
            f"The {bridge} relation changes which exact physics obligation can "
            f"fail first without asserting that route {index} is true."
        ),
        "untouched_physics_gates": [
            "continuum construction remains unproved",
            "positive spectral gap remains unproved",
        ],
        "correction_or_falsifier": (
            f"Return to the incumbent decision if the {bridge} relation in "
            f"route {index} has no discriminating consequence."
        ),
    }


def _family_evidence(
    index: int, constraint_ids: list[str]
) -> dict[str, Any]:
    source, bridge, target = _VOCABULARY[index]
    semantic = _semantic_core(index)
    physics = _physics(index)
    return {
        "mechanism_graph": {
            "nodes": [source, bridge, target],
            "edges": [
                {
                    "source": source,
                    "relation": f"enters-{bridge}",
                    "target": bridge,
                },
                {
                    "source": bridge,
                    "relation": f"conditions-{target}",
                    "target": target,
                },
            ],
        },
        "relation_polarity": _POLARITIES[index % len(_POLARITIES)],
        "intervention": {
            "kind": _INTERVENTIONS[index % len(_INTERVENTIONS)],
            "operation": (
                f"Apply the route {index} transformation at {bridge} while "
                "holding the target identity fixed."
            ),
            "target_constraint_ids": list(constraint_ids),
        },
        "prediction": {
            "observable": f"{target} response observable {index}",
            "direction": _DIRECTIONS[index % len(_DIRECTIONS)],
            "regime": f"{target} finite boundary regime {index}",
            "mechanism_step_index": 1,
        },
        "correction": {
            "kind": _CORRECTIONS[index % len(_CORRECTIONS)],
            "trigger": semantic["correction_condition"],
            "revision": (
                f"Replace the {bridge} step with a separately testable "
                f"relation if route {index} fails."
            ),
        },
        "falsifier": {
            "countermodel": semantic["falsifier"],
            "implicated_mechanism_step_indices": [0, 1],
        },
        "physics_return": {
            "carrier": physics["physical_carrier"],
            "decision_delta": physics["proposed_next_decision"],
            "protected_success_constraint_ids": [
                item
                for item in constraint_ids
                if item.startswith("protected-success-")
            ],
        },
    }


def _raw_invention(request: dict[str, Any]) -> dict[str, Any]:
    index = request["slot"]["slot_index"]
    source, bridge, target = _VOCABULARY[index]
    return {
        "invention_id": request["expected_invention_id"],
        "conjecture": (
            f"The {bridge} relation may reorganize how {source} constrains "
            f"{target} without assuming the desired continuum result."
        ),
        "primitive_hunches": [
            f"{source} carrier hunch",
            f"{bridge} mediator hunch",
        ],
        "relation_hunches": [
            f"{source} enters {bridge} before {target} is reconstructed"
        ],
        "mechanism_hunch": (
            f"Use {bridge} to transfer only correction-stable information "
            f"between {source} and {target}."
        ),
        "root_tension_contact": ROOT_CONTRADICTIONS[index % 2],
        "counterfactual_world": (
            f"In route {index}, removing {bridge} reverses the next theoretical "
            "obligation while the target remains fixed."
        ),
        "protected_successes": list(PROTECTED_SUCCESSES),
        "risk_if_wrong": (
            f"The {bridge} relation may only relocate the incumbent burden."
        ),
        "upside_if_right": (
            f"The {bridge} relation could unify two failures while preserving "
            "their carrier distinction."
        ),
        "first_falsifier": (
            f"A {target} regime where {source} bypasses {bridge} with no changed "
            "prediction."
        ),
        "correction_path": (
            f"Restrict route {index} to the smallest regime where {bridge} has "
            "an independently discriminating consequence."
        ),
    }


def _generation_worker(request: dict[str, Any]) -> dict[str, Any]:
    """A provider-dispatch fixture with one independent terminal failure."""

    time.sleep(0.025)
    if request["slot"]["slot_index"] == 9:
        raise RuntimeError("declared provider channel failed")
    return {
        "output_kind": "aggressive_provider_generation",
        "request_digest": request["request_digest"],
        "raw_invention": _raw_invention(request),
    }


def _maturation_worker(request: dict[str, Any]) -> dict[str, Any]:
    """Produce full open-world maturation content with one sibling failure."""

    time.sleep(0.025)
    index = request["slot"]["slot_index"]
    if index == 8:
        raise RuntimeError("maturation provider failed after author freeze")
    core = _semantic_core(index)
    physics = _physics(index)
    role = (
        "wildcard"
        if request["slot"]["exploration_role"] == "protected_wildcard"
        else "candidate"
    )
    matured = {
        "invention_id": request["raw_invention"]["invention_id"],
        "branch_id": request["branch_id"],
        "exploration_role": role,
        "statement": (
            f"Conceptual route {index} makes the {_VOCABULARY[index][1]} "
            "relation an explicit, correction-bearing physics decision."
        ),
        "semantic_core": core,
        "deep_reflection": _deep_reflection(core, physics),
        "risk_reward": {
            "risk_case": (
                f"Route {index} may add a mediator without reducing the real burden."
            ),
            "high_upside_case": (
                f"Route {index} could unify distinct failures without erasing regimes."
            ),
            "learning_if_false": (
                f"Failure of route {index} identifies a relation that cannot "
                "carry the explanation."
            ),
            "cost_of_unification": (
                f"Route {index} introduces a law whose noncircularity remains open."
            ),
            "wildcard_reason": (
                f"Protected route {index} probes an admissible typed cell before "
                "any merit judgment."
                if role == "wildcard"
                else None
            ),
        },
        "physics_handback": physics,
    }
    return {
        "output_kind": "aggressive_provider_maturation",
        "request_digest": request["request_digest"],
        "matured_invention": matured,
        "typed_family_evidence": _family_evidence(
            index, request["target_constraints"]["constraint_ids"]
        ),
    }


def _projection(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, Any], dict[str, Any]]:
    bundle, snapshot, bridge = _generic_fixture(monkeypatch)
    projection = build_conceptual_ancestry_literature_projection(
        literature_bundle=bundle,
        semantic_snapshot=snapshot,
        literature_snapshot_capture_bridge=bridge,
        present_use_at=PRESENT_USE,
    )
    return projection, bundle


def _coverage(target_id: str, *, cell_count: int = 10) -> dict[str, Any]:
    constraint_ids = target_constraint_identifiers(
        ROOT_CONTRADICTIONS, PROTECTED_SUCCESSES
    )
    return build_target_predeclared_coverage_problem(
        target_id=target_id,
        required_constraint_ids=constraint_ids,
        admissible_cells=[
            {
                "signature": _signature(index),
                "covers_constraint_ids": constraint_ids,
            }
            for index in range(cell_count)
        ],
    )


def _template_corpus() -> list[dict[str, Any]]:
    constraint_ids = target_constraint_identifiers(
        ROOT_CONTRADICTIONS, PROTECTED_SUCCESSES
    )
    return [
        {
            "template_id": "known-template-seven",
            "semantic_core": _semantic_core(7),
            "typed_family_evidence": _family_evidence(7, constraint_ids),
        }
    ]


def _authorities() -> list[dict[str, Any]]:
    return [
        {
            "authority_id": "provider-authority-a",
            "provider_id": "provider-a",
            "model_id": "model-a",
            "human_operator_id": None,
            "declared_channel_id": "channel-a",
        },
        {
            "authority_id": "provider-authority-b",
            "provider_id": "provider-b",
            "model_id": "model-b",
            "human_operator_id": "operator-b",
            "declared_channel_id": "channel-b",
        },
    ]


def _run(
    monkeypatch: pytest.MonkeyPatch, *, coverage_cell_count: int = 10
) -> dict[str, Any]:
    projection, bundle = _projection(monkeypatch)
    return run_aggressive_provider_search(
        target_id=bundle["target_id"],
        run_id=bundle["run_id"],
        state_version=bundle["state_version"],
        target_pressure=(
            "Find a relation-bearing conceptual reorganization that returns an "
            "exact next physics decision without assuming the desired theorem."
        ),
        root_contradictions=ROOT_CONTRADICTIONS,
        protected_successes=PROTECTED_SUCCESSES,
        literature_projection=projection,
        literature_bundle=bundle,
        governed_present_use_at=PRESENT_USE,
        known_taxonomy=_taxonomy(),
        coverage_problem=_coverage(
            bundle["target_id"], cell_count=coverage_cell_count
        ),
        known_template_corpus=_template_corpus(),
        provider_authorities=_authorities(),
        generation_worker=_generation_worker,
        maturation_worker=_maturation_worker,
        requested_count=10,
        max_workers=4,
        branch_wall_seconds=1.0,
        phase_wall_seconds=4.0,
    )


def _reseal(value: dict[str, Any]) -> None:
    value["content_digest"] = canonical_digest(
        {key: child for key, child in value.items() if key != "content_digest"}
    )


def test_schema_is_strict_valid_and_contains_no_authored_programme_atlas() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    assert schema["additionalProperties"] is False
    source = (
        ROOT / "agentic/discovery/aggressive_provider_search.py"
    ).read_text(encoding="utf-8")
    assert "_PROGRAM_TYPES" not in source
    assert "DEFAULT_CORNERS" not in source
    assert "caller_supplied_family_labels" in source


def test_finite_solver_returns_replayable_sat_and_minimal_unsat() -> None:
    sat_problem = _coverage("finite-coverage-target", cell_count=6)
    sat = solve_target_predeclared_coverage(sat_problem)
    assert sat["status"] == "sat"
    assert len(sat["sat_witness"]["selected_cell_ids"]) == 6
    assert (
        verify_target_predeclared_coverage_certificate(sat_problem, sat) == sat
    )

    unsat_problem = _coverage("finite-unsat-target", cell_count=5)
    unsat = solve_target_predeclared_coverage(unsat_problem)
    assert unsat["status"] == "unsat"
    assert unsat["sat_witness"] is None
    assert unsat["minimal_unsat_core"] == [
        {
            "obligation_id": "minimum-distinct-family-count",
            "kind": "minimum_distinct_family_count",
            "value": 6,
        }
    ]
    assert unsat["countermodel"]["maximum_distinct_family_count"] == 5
    forged = copy.deepcopy(unsat)
    forged["minimal_unsat_core"] = [
        {
            "obligation_id": "cover-target-pressure",
            "kind": "cover_constraint",
            "constraint_id": "target-pressure",
        }
    ]
    _reseal(forged)
    with pytest.raises(AggressiveProviderSearchError) as raised:
        verify_target_predeclared_coverage_certificate(
            unsat_problem, forged
        )
    assert raised.value.reason_code == "coverage_certificate_replay_mismatch"


def test_two_process_waves_preserve_partial_failures_and_replay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet = _run(monkeypatch)
    assert (
        validate_aggressive_provider_search_execution(
            packet, known_taxonomy=_taxonomy()
        )
        == packet
    )
    summary = packet["process_summary"]
    assert summary == {
        "actual_killable_process_waves": 2,
        "scheduled_author_slots": 10,
        "accepted_author_slots": 9,
        "accepted_maturation_slots": 8,
        "terminal_receipt_count": 20,
        "partial_failure": True,
        "max_workers": 4,
        "overlap_measurement_authority": None,
    }
    assert [row["status"] for row in packet["author_receipts"]].count(
        "failed"
    ) == 1
    assert [row["status"] for row in packet["maturation_receipts"]].count(
        "failed"
    ) == 1
    assert [row["status"] for row in packet["maturation_receipts"]].count(
        "dependency_blocked"
    ) == 1
    assert all(
        row["terminal_process_group_status"]
        == "reaped_no_background_authority"
        for row in [
            *packet["author_receipts"],
            *packet["maturation_receipts"],
        ]
    )
    assert all(
        row["sibling_invention_digests"]
        and row["caller_supplied_family_labels"] is False
        and "known_template_corpus" not in row
        for row in packet["maturation_requests"]
        if row["dependency_status"] == "ready"
    )


def test_complete_content_assessor_copy_attack_and_protected_routes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet = _run(monkeypatch)
    assessment = packet["family_assessment"]
    assert assessment["worker_family_labels_consumed"] is False
    assert assessment["slot_role_provider_metadata_consumed"] is False
    assert assessment["distinct_typed_family_count"] == 8
    assert all(
        set(row).isdisjoint(
            {"slot_id", "exploration_role", "provider_id", "model_id", "family_label"}
        )
        for row in assessment["candidate_assessments"]
    )
    copy_control = packet["copy_control"]
    assert len(copy_control["quarantined_copy_aliases"]) == 1
    copied = next(
        row for row in copy_control["candidate_results"] if row["copy_detected"]
    )
    assert copied["nearest_template_id"] == "known-template-seven"
    assert copied["exact_identity_erased_projection_copy"] is True
    witness = packet["coverage_verification"]["candidate_sat_witness"]
    assert len(witness["selected_candidate_aliases"]) == 6
    assert not set(witness["selected_candidate_aliases"]).intersection(
        copy_control["quarantined_copy_aliases"]
    )
    assert len(packet["retention"]["protected_wildcard_aliases"]) == 2
    assert packet["retention"]["capable_conservative_control_alias"]
    assert packet["retention"]["merit_or_truth_selection_authorized"] is False
    assert all(value is None for value in packet["authority_nulls"].values())


def test_under_six_requires_target_predeclared_unsat_countermodel(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet = _run(monkeypatch, coverage_cell_count=5)
    coverage = packet["coverage_verification"]
    assert coverage["status"] == (
        "target_predeclared_unsat_countermodel_verified"
    )
    assert coverage["under_six_route_authorized"] is True
    assert coverage["candidate_sat_witness"] is None
    certificate = coverage["target_problem_certificate"]
    assert certificate["status"] == "unsat"
    assert certificate["minimal_unsat_core"] == [
        {
            "obligation_id": "minimum-distinct-family-count",
            "kind": "minimum_distinct_family_count",
            "value": 6,
        }
    ]
    assert packet["family_assessment"]["distinct_typed_family_count"] == 5
    assert (
        validate_aggressive_provider_search_execution(
            packet, known_taxonomy=_taxonomy()
        )
        == packet
    )


def test_replay_rejects_family_label_and_copy_control_forgery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet = _run(monkeypatch)
    family_forgery = copy.deepcopy(packet)
    family_forgery["family_assessment"]["candidate_assessments"][0][
        "family_label"
    ] = "caller-awarded-family"
    _reseal(family_forgery["family_assessment"])
    _reseal(family_forgery)
    with pytest.raises(ContractError):
        validate_aggressive_provider_search_execution(
            family_forgery, known_taxonomy=_taxonomy()
        )

    copy_forgery = copy.deepcopy(packet)
    copied = next(
        row
        for row in copy_forgery["copy_control"]["candidate_results"]
        if row["copy_detected"]
    )
    copied["copy_detected"] = False
    copy_forgery["copy_control"]["quarantined_copy_aliases"] = []
    copy_forgery["copy_control"]["eligible_candidate_aliases"].append(
        copied["candidate_alias"]
    )
    copy_forgery["copy_control"]["eligible_candidate_aliases"].sort()
    _reseal(copy_forgery["copy_control"])
    _reseal(copy_forgery)
    with pytest.raises(AggressiveProviderSearchError) as raised:
        validate_aggressive_provider_search_execution(
            copy_forgery, known_taxonomy=_taxonomy()
        )
    assert raised.value.reason_code == "copy_control_replay_mismatch"


def test_request_requires_exact_six_family_target_problem_and_current_literature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    projection, bundle = _projection(monkeypatch)
    constraint_ids = target_constraint_identifiers(
        ROOT_CONTRADICTIONS, PROTECTED_SUCCESSES
    )
    weak_problem = build_target_predeclared_coverage_problem(
        target_id=bundle["target_id"],
        required_constraint_ids=constraint_ids,
        admissible_cells=[
            {
                "signature": _signature(index),
                "covers_constraint_ids": constraint_ids,
            }
            for index in range(5)
        ],
        minimum_distinct_family_count=5,
    )
    kwargs = {
        "target_id": bundle["target_id"],
        "run_id": bundle["run_id"],
        "state_version": bundle["state_version"],
        "target_pressure": (
            "Return a target-specific theoretical decision from exact literature."
        ),
        "root_contradictions": ROOT_CONTRADICTIONS,
        "protected_successes": PROTECTED_SUCCESSES,
        "literature_projection": projection,
        "literature_bundle": bundle,
        "governed_present_use_at": PRESENT_USE,
        "known_taxonomy": _taxonomy(),
        "coverage_problem": weak_problem,
        "known_template_corpus": _template_corpus(),
        "provider_authorities": _authorities(),
        "requested_count": 8,
    }
    with pytest.raises(AggressiveProviderSearchError) as raised:
        build_aggressive_provider_search_request(**kwargs)
    assert raised.value.reason_code == "coverage_problem_invalid"

    kwargs["coverage_problem"] = _coverage(bundle["target_id"], cell_count=6)
    kwargs["governed_present_use_at"] = "2040-01-01T00:00:00Z"
    with pytest.raises(AggressiveProviderSearchError) as stale:
        build_aggressive_provider_search_request(**kwargs)
    assert stale.value.reason_code == "literature_authority_reopen_failed"
