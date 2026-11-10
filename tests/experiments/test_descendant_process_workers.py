# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused process and semantic regressions for descendant support workers.

These tests exercise real ResourceGovernor-v2 child processes.  They establish
bounded operational behavior and deterministic local reduction only; they do
not claim scientific truth, experiment value, process independence, or a
completed N+8 canonical closure.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.budgets import ResourceGovernor
from agentic.discovery.contracts import canonical_digest
from agentic.experiments.descendant_process_workers import (
    WORKER_IDS,
    DescendantProcessContractError,
    build_theory_authored_descendant_experiment_request,
    run_descendant_support_process_wave,
    validate_descendant_support_process_execution,
    validate_theory_authored_descendant_experiment_request,
)


DOMAIN = {
    "quantity": "regulated_state",
    "unit": "dimensionless_regulated_unit",
    "minimum": "-100",
    "maximum": "100",
}


def _budget(worker_id: str) -> dict[str, Any]:
    return {
        "budget_id": f"descendant-{worker_id}",
        "wall_time_seconds": 8.0,
        "grace_period_seconds": 0.1,
        "cpu_seconds": 4.0,
        "memory_bytes": 256 * 1024 * 1024,
        "disk_bytes": 2 * 1024 * 1024,
        "network_bytes": 0,
        "token_count": 0,
        "request_count": 0,
        "cost_usd": 0.0,
        "absolute_deadline": None,
    }


def _symbolic(*, claimed_output: str = "2", coverage: str = "complete") -> dict:
    return {
        "worker_kind": "symbolic_transition_trace",
        "state_quantity": DOMAIN["quantity"],
        "state_unit": DOMAIN["unit"],
        "initial_value": "0",
        "domain": copy.deepcopy(DOMAIN),
        "coverage": coverage,
        "transitions": [
            {
                "step_id": "symbolic-step-1",
                "input": "0",
                "multiplier": "1",
                "offset": "1",
                "claimed_output": "1",
            },
            {
                "step_id": "symbolic-step-2",
                "input": "1",
                "multiplier": "1",
                "offset": "1",
                "claimed_output": claimed_output,
            },
        ],
    }


def _simulation(*, threshold: str = "2") -> dict:
    return {
        "worker_kind": "bounded_simulation",
        "state_quantity": DOMAIN["quantity"],
        "state_unit": DOMAIN["unit"],
        "step_unit": "discrete_regulator_step",
        "domain": copy.deepcopy(DOMAIN),
        "initial_values": ["0", "1"],
        "recurrence": {"multiplier": "1", "offset": "1"},
        "steps": 2,
        "acceptance": {"comparator": ">=", "threshold": threshold},
        "sample_policy": "deterministic_declared_initial_ensemble",
        "seed_policy": {"stochastic": False, "seed": None},
    }


def _request(
    *,
    claimed_output: str = "2",
    coverage: str = "complete",
    threshold: str = "2",
    stdout_limits: dict[str, int] | None = None,
    route_decision: str = "commission",
) -> dict:
    common = {
        "target_id": "descendant-process-target",
        "run_id": "descendant-process-run",
        "branch_id": "root",
        "theory_generation": 17,
        "question_id": "regulated-transition-discriminator",
        "question_statement": (
            "Does the exact transition and its bounded recurrence preserve the "
            "registered regulated-state premise?"
        ),
        "tested_premise_id": "regulated-transition-premise",
        "tested_premise_digest": canonical_digest(
            {"premise": "regulated transition", "generation": 17}
        ),
        "support_interpretation": (
            "Retain only scoped finite consistency for later theoretical reflection."
        ),
        "falsifier_interpretation": (
            "Record the exact failed transition as negative knowledge for a later "
            "reflection; do not rewrite the current theory."
        ),
        "domain_assumption": copy.deepcopy(DOMAIN),
        "source_theory_programme_digest": canonical_digest(
            {"programme": "theory-N"}
        ),
        "source_reflection_digest": canonical_digest(
            {"reflection": "question-author"}
        ),
        "author_receipt_digest": canonical_digest(
            {"producer": "committed-theory-reflection"}
        ),
        "route_decision": route_decision,
    }
    if route_decision == "no_probe":
        return build_theory_authored_descendant_experiment_request(**common)
    return build_theory_authored_descendant_experiment_request(
        **common,
        symbolic_spec=_symbolic(
            claimed_output=claimed_output,
            coverage=coverage,
        ),
        simulation_spec=_simulation(threshold=threshold),
        resource_budgets={
            worker_id: _budget(worker_id) for worker_id in WORKER_IDS
        },
        stdout_limits=stdout_limits,
    )


@pytest.fixture(scope="module")
def process_worlds(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = tmp_path_factory.mktemp("descendant-process-worlds")
    cases = {
        "neutral_inconclusive": _request(coverage="bounded_partial"),
        "misleading_toy_positive": _request(claimed_output="3"),
        "registered_premise_falsifier": _request(
            claimed_output="3",
            threshold="100",
        ),
    }
    return {
        name: (
            request,
            run_descendant_support_process_wave(
                request,
                workspace=root / name,
            ),
        )
        for name, request in cases.items()
    }


def test_real_process_worlds_cover_inconclusive_misleading_and_falsifier(
    process_worlds: dict[str, Any],
) -> None:
    for expected, (request, execution) in process_worlds.items():
        packet = validate_descendant_support_process_execution(execution, request)
        assert packet["semantic_reduction"]["world_classification"] == expected
        assert packet["semantic_reduction"]["complete_process_wave"] is True
        assert packet["terminal_barrier_complete"] is True
        assert packet["descendant_world_product_eligible"] is True
        assert packet["canonical_n_plus_8_closure_authorized"] is False
        assert [row["worker_id"] for row in packet["terminal_receipts"]] == list(
            WORKER_IDS
        )
        for receipt in packet["terminal_receipts"]:
            event = receipt["process_event"]
            assert receipt["terminal_status"] == "succeeded"
            assert receipt["late_write_contained"] is True
            assert event["event_schema_version"] == 2
            assert event["pid"] not in {None, 0}
            assert event["descendant_leak_detected"] is False
            assert (
                event["resource_limit_execution"]["replacement_environment_used"]
                is True
            )
            assert event["post_supervision_acceptance"]["status"] == "accepted"
            assert set(receipt["authority_nulls"].values()) == {False}
        assert packet["semantic_reduction"]["same_cycle_effects"] == {
            "theory": False,
            "preference": False,
            "proof": False,
            "schedule": False,
        }

    misleading = process_worlds["misleading_toy_positive"][1].as_dict()
    assert misleading["semantic_reduction"]["worker_outcomes"] == {
        "symbolic_transition_trace": "premise_falsifier",
        "bounded_simulation": "scoped_support",
    }
    assert len(misleading["semantic_reduction"]["negative_knowledge"]) == 1
    later = misleading["semantic_reduction"]["later_reflection_request"]
    assert later["not_before_generation"] == 25
    assert later["current_cycle_effect_authorized"] is False


def test_no_probe_never_launches_a_worker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = _request(route_decision="no_probe")

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("no_probe attempted to launch a process")

    monkeypatch.setattr(ResourceGovernor, "run_process", forbidden)
    execution = run_descendant_support_process_wave(
        request,
        workspace=tmp_path / "no-probe",
    )
    packet = validate_descendant_support_process_execution(execution, request)

    assert packet["terminal_receipts"] == []
    assert packet["semantic_reduction"]["world_classification"] == "no_probe"
    assert packet["semantic_reduction"]["later_reflection_request"] is None


def test_replay_validator_is_nonproducing_and_rejects_rehashed_semantic_tamper(
    process_worlds: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request, execution = process_worlds["misleading_toy_positive"]

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("read-only replay attempted production")

    monkeypatch.setattr(ResourceGovernor, "run_process", forbidden)
    validated = validate_descendant_support_process_execution(execution, request)
    assert (
        validated["replay_invocation_mode"]
        == "read_only_semantic_replay_validator_never_produces"
    )

    forged = execution.as_dict()
    response = forged["terminal_receipts"][0]["worker_response"]
    response["output"]["epistemic_outcome"] = "scoped_support"
    response["output"]["result_digest"] = canonical_digest(
        {
            key: value
            for key, value in response["output"].items()
            if key != "result_digest"
        }
    )
    response["output_digest"] = canonical_digest(response["output"])
    response["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in response.items()
            if key != "content_digest"
        }
    )
    receipt = forged["terminal_receipts"][0]
    receipt["worker_response_digest"] = response["content_digest"]
    receipt["receipt_digest"] = canonical_digest(
        {
            key: value
            for key, value in receipt.items()
            if key != "receipt_digest"
        }
    )
    forged["packet_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged.items()
            if key != "packet_digest"
        }
    )
    with pytest.raises(
        DescendantProcessContractError,
        match="semantic replay|identity or digest",
    ):
        validate_descendant_support_process_execution(forged, request)


def test_one_output_exhaustion_is_terminal_partial_failure_without_authority(
    tmp_path: Path,
) -> None:
    request = _request(
        stdout_limits={
            "symbolic_transition_trace": 128 * 1024,
            "bounded_simulation": 64,
        }
    )
    execution = run_descendant_support_process_wave(
        request,
        workspace=tmp_path / "partial-failure",
    )
    packet = validate_descendant_support_process_execution(execution, request)
    receipts = {row["worker_id"]: row for row in packet["terminal_receipts"]}

    assert receipts["symbolic_transition_trace"]["terminal_status"] == "succeeded"
    assert receipts["bounded_simulation"]["terminal_status"] == "operational_failure"
    assert (
        receipts["bounded_simulation"]["process_event"]["status"]
        in {"output_exhausted", "terminated", "killed"}
    )
    assert packet["semantic_reduction"]["world_classification"] == (
        "operational_failure"
    )
    assert packet["semantic_reduction"]["failed_worker_ids"] == [
        "bounded_simulation"
    ]
    assert packet["semantic_reduction"]["later_reflection_request"] is None
    assert packet["descendant_world_product_eligible"] is False
    assert packet["canonical_n_plus_8_closure_authorized"] is False


def test_reduction_is_deterministic_across_distinct_process_runs(
    tmp_path: Path,
    process_worlds: dict[str, Any],
) -> None:
    request, first = process_worlds["registered_premise_falsifier"]
    second = run_descendant_support_process_wave(
        request,
        workspace=tmp_path / "deterministic-replay",
    )
    first_packet = first.as_dict()
    second_packet = second.as_dict()

    assert first_packet["packet_digest"] != second_packet["packet_digest"]
    assert (
        first_packet["semantic_reduction"]
        == second_packet["semantic_reduction"]
    )
    assert (
        first_packet["semantic_reduction"]["reduction_digest"]
        == second_packet["semantic_reduction"]["reduction_digest"]
    )


def test_unit_domain_and_direct_authority_attacks_fail_before_execution() -> None:
    wrong_unit = _symbolic()
    wrong_unit["state_unit"] = "metres"
    with pytest.raises(
        DescendantProcessContractError,
        match="domain unit differs|differs from the theory-authored",
    ):
        build_theory_authored_descendant_experiment_request(
            **{
                key: value
                for key, value in _request().items()
                if key
                not in {
                    "schema_version",
                    "contract_version",
                    "message_kind",
                    "question",
                    "worker_specs",
                    "resource_budgets",
                    "execution_policy",
                    "required_descendant_chronology",
                    "authority_nulls",
                    "request_id",
                    "content_digest",
                }
            },
            question_id="regulated-transition-discriminator",
            question_statement="Does the declared transition preserve its unit?",
            tested_premise_id="regulated-transition-premise",
            tested_premise_digest=canonical_digest({"premise": "unit"}),
            support_interpretation="Scoped consistency only.",
            falsifier_interpretation="Request later reflection only.",
            domain_assumption=copy.deepcopy(DOMAIN),
            source_theory_programme_digest=canonical_digest({"programme": "N"}),
            source_reflection_digest=canonical_digest({"reflection": "N"}),
            author_receipt_digest=canonical_digest({"receipt": "N"}),
            symbolic_spec=wrong_unit,
            simulation_spec=_simulation(),
            resource_budgets={
                worker_id: _budget(worker_id) for worker_id in WORKER_IDS
            },
        )

    outside = _simulation()
    outside["initial_values"] = ["101"]
    base = _request()
    with pytest.raises(
        DescendantProcessContractError,
        match="outside its declared domain",
    ):
        build_theory_authored_descendant_experiment_request(
            target_id=base["target_id"],
            run_id=base["run_id"],
            branch_id=base["branch_id"],
            theory_generation=base["theory_generation"],
            question_id="domain-attack-question",
            question_statement="Does the trace remain inside its exact domain?",
            tested_premise_id="regulated-transition-premise",
            tested_premise_digest=canonical_digest({"premise": "domain"}),
            support_interpretation="Scoped consistency only.",
            falsifier_interpretation="Request later reflection only.",
            domain_assumption=copy.deepcopy(DOMAIN),
            source_theory_programme_digest=canonical_digest({"programme": "N"}),
            source_reflection_digest=canonical_digest({"reflection": "N"}),
            author_receipt_digest=canonical_digest({"receipt": "N"}),
            route_decision="commission",
            symbolic_spec=_symbolic(),
            simulation_spec=outside,
            resource_budgets={
                worker_id: _budget(worker_id) for worker_id in WORKER_IDS
            },
        )

    inflated = copy.deepcopy(base)
    inflated["authority_nulls"]["current_theory_mutation_authorized"] = True
    inflated["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in inflated.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(
        DescendantProcessContractError,
        match="authority",
    ):
        validate_theory_authored_descendant_experiment_request(inflated)
