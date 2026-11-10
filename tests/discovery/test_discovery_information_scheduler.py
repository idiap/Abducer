# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Tests for theory-first, literature-bound Pareto scheduling."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError
from agentic.discovery.contracts import Namespace, canonical_digest
from agentic.discovery.scheduler import consume_action, consume_action_transaction, schedule_discovery_actions
from agentic.state.discovery_transaction import DiscoveryTransactionStore
from tests.discovery.test_reflective_conceptual_discovery import _strict_operator_request


def _branch(branch_id: str, **overrides: object) -> dict:
    row = {
        "branch_id": branch_id,
        "status": "incubating",
        "maturity": "incubating",
        "conceptual_corner": branch_id,
        "semantic_prompt_digest": f"sha256:{branch_id:0<64}"[:71],
        "depends_on": [],
        "dependency_ids": [],
        "theory_virtues": {
            "essential_relevance": 1.0,
            "root_tension_contact": 0.8,
            "expected_understanding_gain": 0.8,
            "expected_unification_gain": 0.5,
            "conceptual_fertility": 0.8,
            "programme_impact": 0.8,
            "maturity": 0.4,
        },
        "estimated_cost": 1.0,
        "premature_closure_risk": 0.2,
    }
    row.update(overrides)
    return row


def _state(*branches: dict, literature: dict | None = None, **overrides: object) -> dict:
    state = {
        "target_id": "target-pvsnp",
        "state_version": 4,
        "literature": literature
        or {"status": "validated_current", "snapshot_id": "snapshot-2", "assimilated_snapshot_id": "snapshot-2"},
        "branches": list(branches),
        "semantic_plateau_limit": 3,
        "required_conceptual_corners": [],
        "new_evidence": [],
    }
    state.update(overrides)
    return state


def _authority_fixture(outcome: str) -> tuple[dict, list[str], list[str]]:
    request, preferred_system_ids = _strict_operator_request(outcome)
    candidate_system_ids = [row["system_id"] for row in request["conceptual_systems"]]
    return (
        {
            "target_id": request["target_id"],
            "run_id": request["run_id"],
            "state_version": request["state_version"],
            "conceptual_systems": copy.deepcopy(request["conceptual_systems"]),
            "reflection_rounds": copy.deepcopy(request["reflection_rounds"]),
            "conceptual_adjudication_evidence": copy.deepcopy(
                request["conceptual_adjudication_evidence"]
            ),
        },
        preferred_system_ids,
        candidate_system_ids,
    )


def _formal_claim_binding(label: str = "one") -> dict:
    digest = lambda value: canonical_digest({"formal-binding": value})
    return {
        "schema_version": 1,
        "binding_kind": "registered_formal_claim_prove_action",
        "producer_operator_id": "formal-claim-producer",
        "producer_request_id": f"opreq.{label}",
        "producer_request_digest": digest(f"request-{label}"),
        "producer_receipt_id": f"opreceipt.{label}",
        "producer_receipt_digest": digest(f"receipt-{label}"),
        "producer_input_digest": digest(f"input-{label}"),
        "consumer_event_id": f"event.{label}",
        "consumer_event_hash": digest(f"event-{label}"),
        "semantic_row_id": f"semantic.formal.{label}",
        "semantic_row_digest": digest(f"semantic-{label}"),
        "output_id": f"formal-output.{label}",
        "output_digest": digest(f"output-{label}"),
        "source_theory_generation": 5,
        "conjecture_id": f"conjecture.{label}",
        "formal_claim_digest": digest(f"claim-{label}"),
        "execution_plan_digest": digest(f"plan-{label}"),
    }


def test_ready_formal_claim_has_exactly_one_bound_prove_action() -> None:
    authority, preferred, _candidates = _authority_fixture("unique")
    binding = _formal_claim_binding()
    schedule = schedule_discovery_actions(
        _state(
            _branch(
                "branch-formal",
                maturity="proof_ready",
                formal_claim_binding=binding,
                conceptual_system_ids=[preferred[0]],
            ),
            **authority,
        )
    )
    prove = [action for action in schedule["actions"] if action["kind"] == "prove"]
    assert len(prove) == 1
    assert prove[0]["branch_ids"] == ["branch-formal"]
    assert prove[0]["payload"]["formal_claim_binding"] == binding
    assert prove[0]["priority_class"] == "registered_formal_claim_continuation"


def test_ready_formal_claim_survives_pareto_dominance_and_prompt_collision() -> None:
    authority, preferred, _candidates = _authority_fixture("unique")
    strong = _branch(
        "branch-a",
        semantic_prompt_digest="shared-prompt",
        conceptual_system_ids=[preferred[0]],
    )
    weak_virtues = {key: 0.0 for key in strong["theory_virtues"]}
    formal = _branch(
        "branch-z",
        maturity="proof_ready",
        formal_claim_binding=_formal_claim_binding("dominated"),
        semantic_prompt_digest="shared-prompt",
        conceptual_system_ids=[preferred[0]],
        theory_virtues=weak_virtues,
        estimated_cost=100.0,
        premature_closure_risk=1.0,
    )
    schedule = schedule_discovery_actions(_state(strong, formal, **authority))
    prove = [action for action in schedule["actions"] if action["kind"] == "prove"]
    assert len(prove) == 1
    assert prove[0]["branch_ids"] == ["branch-z"]


def test_scheduler_rejects_multiple_or_unbound_proof_ready_claims() -> None:
    authority, preferred, _candidates = _authority_fixture("unique")
    with pytest.raises(ContractError, match="at most one"):
        schedule_discovery_actions(
            _state(
                _branch(
                    "branch-a",
                    maturity="proof_ready",
                    formal_claim_binding=_formal_claim_binding("a"),
                    conceptual_system_ids=[preferred[0]],
                ),
                _branch(
                    "branch-b",
                    maturity="proof_ready",
                    formal_claim_binding=_formal_claim_binding("b"),
                    conceptual_system_ids=[preferred[0]],
                ),
                **authority,
            )
        )
    with pytest.raises(ContractError, match="requires one exact"):
        schedule_discovery_actions(
            _state(
                _branch(
                    "branch-unbound",
                    maturity="proof_ready",
                    conceptual_system_ids=[preferred[0]],
                ),
                **authority,
            )
        )


def test_scheduler_rejects_inactive_or_unauthorized_formal_claim() -> None:
    authority, preferred, candidates = _authority_fixture("unique")
    binding = _formal_claim_binding("blocked")
    with pytest.raises(ContractError, match="inactive or dependency-blocked"):
        schedule_discovery_actions(
            _state(
                _branch(
                    "branch-inactive",
                    status="operational_failure",
                    maturity="proof_ready",
                    formal_claim_binding=binding,
                    conceptual_system_ids=[preferred[0]],
                ),
                **authority,
            )
        )
    nonpreferred = next(
        system_id for system_id in candidates if system_id not in preferred
    )
    with pytest.raises(ContractError, match="denied its exact prove action"):
        schedule_discovery_actions(
            _state(
                _branch(
                    "branch-unpreferred",
                    maturity="proof_ready",
                    formal_claim_binding=binding,
                    conceptual_system_ids=[nonpreferred],
                ),
                **authority,
            )
        )


def test_absent_formal_claim_schedules_no_prove_action() -> None:
    schedule = schedule_discovery_actions(_state(_branch("branch-reflect")))
    assert all(action["kind"] != "prove" for action in schedule["actions"])
    assert all(
        "formal_claim_binding" not in action.get("payload", {})
        for action in schedule["actions"]
    )


def test_new_literature_forces_assimilation_and_rebase_before_investment() -> None:
    schedule = schedule_discovery_actions(
        _state(
            _branch("branch-a", maturity="mature", synthesis_candidate=True),
            literature={"status": "validated_current", "snapshot_id": "snapshot-3", "assimilated_snapshot_id": "snapshot-2"},
        )
    )
    kinds = [row["kind"] for row in schedule["actions"]]
    assert kinds[:2] == ["assimilate", "rebase"]
    branch_action = next(
        row
        for row in schedule["actions"]
        if row["branch_ids"] == ["branch-a"] and row["priority_class"] != "hard_gate"
    )
    assert branch_action["kind"] == "incubate"
    assert {"literature_blind", "no_novelty_claim", "no_active_investment"}.issubset(branch_action["restrictions"])


def test_missing_literature_plans_refresh_assimilation_rebase_chain() -> None:
    schedule = schedule_discovery_actions(_state(_branch("branch-a"), literature={"status": "missing"}))
    gates = [row for row in schedule["actions"] if row["priority_class"] == "hard_gate"]
    assert [row["kind"] for row in gates] == ["refresh_literature", "assimilate", "rebase"]
    assert gates[1]["depends_on"] == [gates[0]["action_id"]]
    assert gates[2]["depends_on"] == [gates[1]["action_id"]]


def test_immature_probe_is_replaced_by_theory_formalization() -> None:
    branch = _branch("branch-a", requested_action="probe", theoretical_question_maturity="immature")
    schedule = schedule_discovery_actions(_state(branch))
    action = next(row for row in schedule["actions"] if row["branch_ids"] == ["branch-a"])
    assert action["kind"] == "incubate"
    assert action["payload"]["requested_kind"] == "formalize"
    assert "conceptual_preference_unsealed" in action["restrictions"]
    assert all(row["kind"] != "probe" for row in schedule["actions"])


def test_no_probe_needed_continues_reflection_without_placeholder() -> None:
    branch = _branch("branch-a", requested_action="probe", probe_decision="no_probe_needed", theoretical_question_maturity="mature")
    schedule = schedule_discovery_actions(_state(branch))
    assert next(row for row in schedule["actions"] if row["branch_ids"])["kind"] == "reflect"
    assert all(row["kind"] != "probe" for row in schedule["actions"])


def test_independent_nondominated_branches_form_parallel_wave_without_duplicate_prompts() -> None:
    left = _branch("branch-a", semantic_prompt_digest="prompt-a")
    right = _branch("branch-b", semantic_prompt_digest="prompt-b", theory_virtues={**_branch("x")["theory_virtues"], "expected_unification_gain": 0.9, "expected_understanding_gain": 0.5})
    duplicate = _branch("branch-c", semantic_prompt_digest="prompt-a")
    schedule = schedule_discovery_actions(_state(left, right, duplicate))
    branch_actions = [row for row in schedule["actions"] if row["branch_ids"]]
    assert len({row["payload"]["semantic_prompt_digest"] for row in branch_actions}) == len(branch_actions)
    assert any(wave["mode"] == "parallel" and len(wave["action_ids"]) >= 2 for wave in schedule["waves"])


def test_protected_wildcard_survives_scalar_dominance() -> None:
    strong = _branch("branch-a")
    wildcard = _branch(
        "branch-b",
        protected_wildcard=True,
        theory_virtues={key: 0.1 for key in strong["theory_virtues"]},
        estimated_cost=10,
        premature_closure_risk=0.9,
    )
    schedule = schedule_discovery_actions(_state(strong, wildcard))
    wildcard_action = next(row for row in schedule["actions"] if row["branch_ids"] == ["branch-b"])
    assert wildcard_action["priority_class"] == "protected_wildcard"


def test_two_protected_wildcards_survive_when_both_are_available() -> None:
    strong = _branch("branch-a")
    weak_virtues = {key: 0.1 for key in strong["theory_virtues"]}
    first = _branch(
        "branch-b",
        protected_wildcard=True,
        theory_virtues=weak_virtues,
        estimated_cost=10,
        premature_closure_risk=0.9,
    )
    second = _branch(
        "branch-c",
        protected_wildcard=True,
        theory_virtues=weak_virtues,
        estimated_cost=11,
        premature_closure_risk=0.9,
    )
    schedule = schedule_discovery_actions(_state(strong, first, second))
    selected = {
        row["branch_ids"][0]
        for row in schedule["actions"]
        if row["branch_ids"] and row["priority_class"] == "protected_wildcard"
    }
    assert selected == {"branch-b", "branch-c"}


def test_semantic_plateau_pivots_then_retires() -> None:
    pivot = schedule_discovery_actions(_state(_branch("branch-a", equivalent_output_count=3)))
    assert next(row for row in pivot["actions"] if row["branch_ids"])["kind"] == "reframe"
    retire = schedule_discovery_actions(_state(_branch("branch-a", equivalent_output_count=4)))
    retirement = next(row for row in retire["actions"] if row["branch_ids"])
    assert retirement["kind"] == "incubate"
    assert retirement["payload"]["requested_kind"] == "retire"
    assert "no_active_investment" in retirement["restrictions"]


def test_unique_sealed_preference_authorizes_only_the_bound_candidate() -> None:
    authority, preferred, candidates = _authority_fixture("unique")
    nonpreferred = next(system_id for system_id in candidates if system_id not in preferred)
    state = _state(
        _branch(
            "branch-preferred",
            requested_action="probe",
            theoretical_question_maturity="immature",
            conceptual_system_ids=[preferred[0]],
        ),
        _branch(
            "branch-other",
            requested_action="probe",
            theoretical_question_maturity="immature",
            conceptual_system_ids=[nonpreferred],
        ),
        **authority,
    )
    schedule = schedule_discovery_actions(state)
    by_branch = {
        row["branch_ids"][0]: row for row in schedule["actions"] if row["branch_ids"]
    }
    assert by_branch["branch-preferred"]["kind"] == "formalize"
    assert by_branch["branch-preferred"]["payload"]["conceptual_preference_applied"] is True
    assert by_branch["branch-other"]["kind"] == "incubate"
    assert by_branch["branch-other"]["payload"]["sealed_preference_intersection"] == []
    assert schedule["conceptual_preference_authority"]["status"] == "sealed_unique"
    assert schedule["conceptual_preference_authority"]["evidence"] == authority[
        "conceptual_adjudication_evidence"
    ]


def test_plural_sealed_preference_authorizes_every_member_equally_in_parallel() -> None:
    authority, preferred, _candidates = _authority_fixture("plural")
    state = _state(
        *[
            _branch(
                f"branch-{index}",
                requested_action="probe",
                theoretical_question_maturity="immature",
                conceptual_system_ids=[system_id],
            )
            for index, system_id in enumerate(preferred)
        ],
        **authority,
    )
    schedule = schedule_discovery_actions(state)
    branch_actions = [row for row in schedule["actions"] if row["branch_ids"]]
    assert schedule["conceptual_preference_authority"]["status"] == "sealed_plural"
    assert {row["kind"] for row in branch_actions} == {"formalize"}
    assert {
        row["payload"]["sealed_preference_intersection"][0] for row in branch_actions
    } == set(preferred)
    assert any(
        wave["mode"] == "parallel" and len(wave["action_ids"]) == len(preferred)
        for wave in schedule["waves"]
    )


def test_plural_preference_never_becomes_automatic_synthesis_or_singular_winner() -> None:
    authority, preferred, _candidates = _authority_fixture("plural")
    schedule = schedule_discovery_actions(
        _state(
            _branch(
                "branch-plural",
                maturity="mature",
                synthesis_candidate=True,
                conceptual_system_ids=[preferred[0]],
            ),
            **authority,
        )
    )
    action = next(row for row in schedule["actions"] if row["branch_ids"])
    assert action["kind"] == "differentiate"
    assert "no_automatic_synthesis" in action["restrictions"]
    assert action["payload"]["conceptual_preference_applied"] is False
    assert schedule["conceptual_preference_authority"]["preference_set"][
        "preferred_system_ids"
    ] == preferred


def test_revise_all_is_diagnostic_and_blocks_every_active_investment() -> None:
    authority, preferred, candidates = _authority_fixture("revise_all")
    assert preferred == []
    schedule = schedule_discovery_actions(
        _state(
            *[
                _branch(
                    f"branch-{index}",
                    requested_action="probe",
                    theoretical_question_maturity="mature",
                    conceptual_system_ids=[system_id],
                )
                for index, system_id in enumerate(candidates[:2])
            ],
            **authority,
        )
    )
    branch_actions = [row for row in schedule["actions"] if row["branch_ids"]]
    assert schedule["conceptual_preference_authority"]["status"] == (
        "sealed_revise_all_diagnostic_only"
    )
    assert {row["kind"] for row in branch_actions} == {"incubate"}
    assert all("sealed_revise_all" in row["restrictions"] for row in branch_actions)
    assert all(row["payload"]["conceptual_preference_applied"] is False for row in branch_actions)


def test_scheduler_rejects_detached_or_caller_authored_preference_authority() -> None:
    with pytest.raises(ContractError, match="ID-only"):
        schedule_discovery_actions(
            _state(
                _branch("branch-a"),
                conceptual_adjudication_evidence_id="conceptual-adjudication-evidence.detached",
            )
        )
    with pytest.raises(ContractError, match="caller-authored"):
        schedule_discovery_actions(
            _state(_branch("branch-a"), preferred_system_ids=["system.caller"])
        )
    with pytest.raises(ContractError, match="plural conceptual_system_ids"):
        schedule_discovery_actions(
            _state(_branch("branch-a", conceptual_system_id="system.singular"))
        )


def test_scheduler_rejects_post_seal_system_or_reflection_splicing() -> None:
    authority, preferred, _candidates = _authority_fixture("unique")
    branch = _branch("branch-a", conceptual_system_ids=[preferred[0]])
    spliced_systems = copy.deepcopy(authority)
    spliced_systems["conceptual_systems"][0]["mechanism_or_principle"] += " forged"
    with pytest.raises(ContractError, match="conceptual-system content differs"):
        schedule_discovery_actions(_state(branch, **spliced_systems))

    spliced_rounds = copy.deepcopy(authority)
    spliced_rounds["reflection_rounds"][0]["strongest_objections"][0] += " forged"
    with pytest.raises(ContractError, match="reflection content differs"):
        schedule_discovery_actions(_state(branch, **spliced_rounds))


def test_evidence_updates_every_linked_route_and_quarantine_needs_reactivation() -> None:
    evidence = [{"evidence_id": "ev-1", "validated": True, "affected_dependency_ids": ["dep-x"], "direction": "raise"}]
    quarantined = _branch("branch-c", status="quarantined", dependency_ids=["dep-x"])
    schedule = schedule_discovery_actions(_state(_branch("branch-a", dependency_ids=["dep-x"]), _branch("branch-b", dependency_ids=["dep-x"]), quarantined, new_evidence=evidence))
    assert {row["branch_id"] for row in schedule["priority_updates"]} == {"branch-a", "branch-b", "branch-c"}
    assert all("branch-c" not in row["branch_ids"] for row in schedule["actions"])
    reactivated = schedule_discovery_actions(_state(_branch("branch-c", status="quarantined", reactivation_event_id="event-7")))
    assert any(row["branch_ids"] == ["branch-c"] for row in reactivated["actions"])


def test_action_consumption_is_compare_and_swap_and_exactly_once() -> None:
    schedule = schedule_discovery_actions(_state(_branch("branch-a")))
    action = next(row for row in schedule["actions"] if not row["depends_on"])
    consumed = consume_action(schedule, action["action_id"], expected_state_version=4, consumer_receipt_id="receipt-1")
    assert next(row for row in consumed["actions"] if row["action_id"] == action["action_id"])["status"] == "consumed"
    assert consumed["consumed_schedule_digest"] == canonical_digest(
        consumed,
        exclude_keys=("consumed_schedule_digest", "created_at"),
    )
    assert consumed["consumed_schedule_digest"] != schedule["schedule_digest"]
    with pytest.raises(ContractError, match="already"):
        consume_action(consumed, action["action_id"], expected_state_version=4, consumer_receipt_id="receipt-2")
    with pytest.raises(ContractError, match="stale"):
        consume_action(schedule, action["action_id"], expected_state_version=3, consumer_receipt_id="receipt-3")


def test_action_consumption_commits_through_canonical_transaction_store(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-pvsnp", run_id="run-scheduler")
    store.commit(
        expected_generation=0,
        state={"target_id": "target-pvsnp", "run_id": "run-scheduler", "generation": 1},
        artifacts=(),
        idempotency_key="initialize-scheduler-state",
        request_digest=canonical_digest({"initialize": True}),
    )
    schedule = schedule_discovery_actions({**_state(_branch("branch-a")), "state_version": 1})
    action = next(row for row in schedule["actions"] if not row["depends_on"])
    updated, result = consume_action_transaction(
        store,
        schedule,
        action["action_id"],
        expected_generation=1,
        consumer_receipt_id="receipt-transaction-1",
    )
    assert result.generation == 2
    assert store.read_state()["next_action_schedule"] == updated
    replayed, replay_result = consume_action_transaction(
        store,
        schedule,
        action["action_id"],
        expected_generation=1,
        consumer_receipt_id="receipt-transaction-1",
    )
    assert replayed == updated
    assert replay_result.idempotent is True
    with pytest.raises(ContractError, match="compare-and-swap"):
        consume_action_transaction(
            store,
            schedule,
            action["action_id"],
            expected_generation=1,
            consumer_receipt_id="receipt-transaction-2",
        )
