# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Deterministic regressions for the legacy marathon/runtime boundary."""

from __future__ import annotations

import datetime as dt
import inspect
import sys
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "agentic" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agentic.discovery.contracts import ContractError, canonical_digest, stable_identifier  # noqa: E402
from agentic.discovery.ledger import initial_state  # noqa: E402
from agentic.discovery.learning import LearningReducer, initial_branch_state  # noqa: E402
import agentic.discovery.theory_gate as theory_gate  # noqa: E402
from agentic.state.discovery_transaction import DiscoveryTransactionStore  # noqa: E402
from discovery_marathon_common import (  # noqa: E402
    build_skill_dispatch_trace,
    load_dispatch_matrix,
    phase_applies,
)
import run_discovery_marathon as marathon  # noqa: E402
import run_discovery_marathon_job as marathon_job  # noqa: E402
import validate_discovery_marathon_cycle as cycle_validator  # noqa: E402
from validate_discovery_marathon_cycle import validate_receipt_backed_cycle  # noqa: E402
from validate_discovery_marathon_skill_dispatch import (  # noqa: E402
    validate_dispatch_matrix,
    validate_trace,
)


def _verified_gate_fixture(payload: dict) -> dict:
    """Issue a digest-complete, short-lived local capability for unit seams."""

    materialized = dict(payload)
    now, clock_authority, temporal_capability = theory_gate._read_governed_present_instant(  # noqa: SLF001
        theory_gate.SYSTEM_UTC_CLOCK_AUTHORITY_ID
    )

    def stamp(value: dt.datetime) -> str:
        return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    commit_at = now - dt.timedelta(seconds=1)
    consume_before = now + dt.timedelta(minutes=5)
    materialized.setdefault("eligible_branch_ids", [])
    materialized.setdefault("action_ids_by_branch", {})
    materialized.setdefault("action_kinds_by_branch", {})
    materialized.setdefault(
        "authorization_semantics", "bounded_test_exact_schedule_eligibility"
    )
    eligibility = {
        "eligible_branch_ids": materialized["eligible_branch_ids"],
        "action_ids_by_branch": materialized["action_ids_by_branch"],
        "action_kinds_by_branch": materialized["action_kinds_by_branch"],
        "authorization_semantics": materialized["authorization_semantics"],
    }
    literature_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "bounded_test_literature_authority",
        "snapshot_id": "snapshot.test.current",
        "recorded_commit_created_at": stamp(commit_at),
        "recorded_commit_time_authority": "unattested_transaction_manifest_local_time",
        "consume_before": stamp(consume_before),
    }
    literature_basis_digest = canonical_digest(literature_basis)
    authorization_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "bounded_test_canonical_authorization",
        "target_id": materialized.get("target_id", "target.test"),
        "run_id": materialized.get("run_id", "run.test"),
        "cycle_id": materialized.get("cycle_id", "cycle.test"),
        "commit_id": materialized.get("commit_id", "commit.test"),
        "committed_state_version": materialized.get("committed_state_version", 1),
        "schedule_eligibility_derivation_digest": canonical_digest(eligibility),
    }
    authorization_basis_digest = canonical_digest(authorization_basis)
    present_decision = {
        "schema_version": "1.0.0",
        "decision": "authorized_present_investment",
        "evaluated_at": stamp(now),
        "recorded_commit_created_at": stamp(commit_at),
        "recorded_commit_time_authority": "unattested_transaction_manifest_local_time",
        "consume_before": stamp(consume_before),
        "authorization_basis_digest": authorization_basis_digest,
        "literature_authority_basis_digest": literature_basis_digest,
        "clock_authority": clock_authority,
        "clock_authority_digest": clock_authority["authority_digest"],
        "authentication_status": "governed_local_process_time_not_externally_authenticated",
        "reason": "bounded_test_capability_current_at_issue_time",
    }
    materialized.update(
        {
            "literature_consume_before": stamp(consume_before),
            "literature_authority_basis": literature_basis,
            "literature_authority_basis_digest": literature_basis_digest,
            "authorization_basis": authorization_basis,
            "authorization_basis_digest": authorization_basis_digest,
            "present_investment_decision": present_decision,
            "present_investment_decision_digest": canonical_digest(present_decision),
        }
    )
    materialized.pop("authorization_digest", None)
    materialized["authorization_digest"] = canonical_digest(materialized)
    return theory_gate._issue_verified_authorization(  # noqa: SLF001
        materialized,
        present_investment_verified=True,
        temporal_capability=temporal_capability,
    )


def _receipt(
    branch_id: str,
    *,
    status: str = "succeeded",
    operator_id: str = "legacy-marathon-branch-adapter",
    state_version: int = 0,
) -> dict:
    """Build a schema-valid receipt without claiming an unexecuted matrix skill."""

    namespace = {
        "target_id": "target-a",
        "run_id": "run-a",
        "branch_id": branch_id,
        "state_version": state_version,
    }
    receipt = {
        "schema_version": "1.0.0",
        "request_id": f"request.{branch_id}.{operator_id}",
        "request_digest": canonical_digest({"request": branch_id, "operator": operator_id}),
        "invocation_id": f"invocation.{branch_id}.{operator_id}",
        "attempt": 1,
        "operator": {"operator_id": operator_id, "version": "1.0.0", "kind": "theory"},
        "identity": namespace,
        "required": True,
        "input_digest": canonical_digest({"branch": branch_id}),
        "started_at": "2026-07-21T10:00:00Z",
        "completed_at": "2026-07-21T10:00:01Z",
        "duration_seconds": 1.0,
        "status": status,
        "exit_code": 0 if status == "succeeded" else 3,
        "stdout_digest": canonical_digest("stdout"),
        "stderr_digest": canonical_digest("stderr"),
        "output_artifacts": [],
        "output_history_artifacts": [],
        "explicit_unknowns": ["truth remains unknown"],
        "validator_receipts": [],
    }
    if status == "succeeded":
        receipt["output_artifacts"] = [
            {
                "path": f"outputs/{branch_id}/result.json",
                "sha256": canonical_digest({"result": branch_id}),
                "size_bytes": 2,
                "namespace": namespace,
            }
        ]
        history_prefix = (
            f".discovery-history/{namespace['target_id']}/{namespace['run_id']}/"
            f"{namespace['branch_id']}/state-{namespace['state_version']}/"
            f"{receipt['invocation_id']}/attempt-{receipt['attempt']}"
        )
        history_artifact = {
            **receipt["output_artifacts"][0],
            "path": f"{history_prefix}/outputs/result.json",
        }
        receipt["output_history_artifacts"] = [history_artifact]
        authority_file_digest = canonical_digest(
            {"validator": "branch-validator", "version": "1.0.0"}
        )
        authority = {
            "schema_version": "1.0.0",
            "binding_kind": "callable",
            "validator_id": "branch-validator",
            "validator_version": "1.0.0",
            "runtime_identity": {
                "kind": "callable",
                "module": "tests.orchestration.test_discovery_marathon_runtime_adapter",
                "qualname": "_receipt.fixture_validator",
            },
            "dependency_identities": [],
            "dependency_policy": "declared_only",
            "files": [
                {
                    "roles": ["validator_callable"],
                    "path_scope": "workspace_relative",
                    "runtime_path": "tests/orchestration/test_discovery_marathon_runtime_adapter.py",
                    "sha256": authority_file_digest,
                    "size_bytes": 1,
                    "snapshot_descriptor": {
                        "path": f"{history_prefix}/validators/branch-validator/authority.fixture.py",
                        "sha256": authority_file_digest,
                        "size_bytes": 1,
                        "namespace": namespace,
                    },
                }
            ],
            "coverage": {
                "bound": ["fixture validator callable and exact history artifact bytes"],
                "excluded": ["undeclared transitive imports beyond explicit dependency paths"],
            },
        }
        authority["authority_digest"] = canonical_digest(authority)
        receipt["validator_receipts"] = [
            {
                "validator_id": "branch-validator",
                "validator_version": "1.0.0",
                "validator_code_digest": authority["authority_digest"],
                "validator_authority": authority,
                "request_id": receipt["request_id"],
                "input_digest": receipt["input_digest"],
                "started_at": "2026-07-21T10:00:00Z",
                "completed_at": "2026-07-21T10:00:01Z",
                "status": "passed",
                "artifact_digests": [history_artifact["sha256"]],
                "output_artifacts": receipt["output_history_artifacts"],
            }
        ]
        receipt["validator_receipts"][0]["receipt_digest"] = canonical_digest(
            receipt["validator_receipts"][0]
        )
    else:
        receipt["error"] = {"type": "RuntimeError", "message": "deliberate failure"}
    receipt["receipt_id"] = stable_identifier(
        "opreceipt",
        receipt["request_id"],
        receipt["attempt"],
        canonical_digest(receipt),
    )
    receipt["receipt_digest"] = canonical_digest(receipt)
    return receipt


def _output(branch_id: str, *, revision: str = "new-mechanism") -> dict:
    """Return the compact structural fields consumed by the semantic adapter."""

    return {
        "branch_id": branch_id,
        "candidate_lemmas": [{"lemma_id": revision}],
        "derivation_steps": [revision],
        "equations": [{"latex": "A\\to B", "valid_when": "under the named model"}],
        "dependency_updates": ["dependency-a"],
        "falsifiers": ["counterexample-a"],
        "mathematical_learning": "The carrier relation changed.",
        "next_experiment": "Test the revised carrier.",
        "control_decision": {"decision": "persist"},
    }


def test_legacy_receipt_cannot_upgrade_advisory_skills_or_replace_theory_gate() -> None:
    receipt = _receipt("branch-a", operator_id="kb-abduce")
    trace = build_skill_dispatch_trace(
        "cycle-000000000001",
        ["branch-a"],
        ["Branch A"],
        target_id="target-a",
        run_id="run-a",
        state_version=0,
        operator_receipts=[receipt],
    )
    exploration = next(row for row in trace if row["phase"] == "branch_exploration")
    assert exploration["invoked_skills"] == []
    assert "kb-abduce" in exploration["legacy_advisory_skills"]
    assert exploration["missing_required_skills"] == []
    assert exploration["dispatch_status"] == "certified"
    summary = validate_trace(trace, Path("cycle-000000000001.json"))
    assert summary["certified"] is False
    assert "current_literature_assimilation_rebase" in summary["blocked_phases"]
    with pytest.raises(SystemExit):
        validate_trace(trace, Path("cycle-000000000001.json"), require_certified=True)


def test_legacy_self_attestation_is_readable_but_never_certified() -> None:
    fixture = Path("tests/fixtures/discovery_marathon/skill_dispatch_valid.json")
    import json

    summary = validate_trace(json.loads(fixture.read_text())["skill_dispatch_trace"], fixture)
    assert summary["certified"] is False
    assert summary["legacy_self_attested_phases"]


def test_registry_is_theory_first_and_target_scopes_are_executable_filters() -> None:
    matrix = load_dispatch_matrix()
    validate_dispatch_matrix(matrix)
    phase_ids = [row["phase"] for row in matrix["phases"]]
    assert phase_ids.index("current_literature_assimilation_rebase") < phase_ids.index("branch_selection")
    assert phase_ids.index("high_risk_intuition_generation") < phase_ids.index("branch_selection")
    assert phase_ids.index("parallel_hypothesis_maturation") < phase_ids.index("branch_selection")
    assert phase_ids.index("reflective_parent_synthesis") < phase_ids.index("branch_selection")
    assert phase_ids.index("theory_requested_symbolic_simulation_support") > phase_ids.index("reflective_parent_synthesis")

    ym_phase = next(
        row for row in matrix["phases"] if row["phase"] == "yang_mills_representational_dynamics_overlay"
    )
    assert phase_applies(ym_phase, "yang-mills-existence-and-mass-gap-target") is True
    assert phase_applies(ym_phase, "p-vs-np-target") is False
    pvsnp_trace = build_skill_dispatch_trace(
        "cycle-scope-a",
        ["branch-a"],
        ["Branch A"],
        target_id="p-vs-np-target",
        run_id="run-a",
        state_version=0,
    )
    assert "yang_mills_representational_dynamics_overlay" not in {
        row["phase"] for row in pvsnp_trace
    }


def test_committed_canonical_bindings_certify_only_executable_theory_phases() -> None:
    operators = {
        "frontier-literature-assimilator",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
        "blind-conceptual-preference-adjudicator",
    }
    gate = _verified_gate_fixture({
        "status": "verified_active_current",
        "authoritative": True,
        "target_id": "target-a",
        "authorization_digest": canonical_digest({"authorization": "fixture"}),
        "operator_evidence_digest": canonical_digest({"evidence": "fixture"}),
        "commit_id": "commit.fixture",
        "operator_bindings": {
            operator: {
                "receipt_ids": [f"receipt.{operator}"],
                "feedback_edge_ids": [f"feedback.{operator}"],
            }
            for operator in operators
        },
    })
    trace = build_skill_dispatch_trace(
        "cycle-gated-a",
        ["branch-a"],
        ["Branch A"],
        target_id="target-a",
        run_id="run-a",
        state_version=0,
        canonical_theory_gate=gate,
    )
    summary = validate_trace(
        trace,
        Path("cycle-gated-a.json"),
        require_certified=True,
        verified_gate=gate,
    )
    assert summary["certified"] is True
    assert not summary["legacy_self_attested_phases"]
    assert all(
        binding["evidence_kind"] == "canonical_feedback_edge"
        for row in trace
        for binding in row["receipt_bindings"]
    )


def test_research_gate_fails_before_loading_or_selecting_branches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Store:
        root = Path("/tmp/legacy-marathon-state")

        @staticmethod
        def current_generation() -> int:
            return 0

    calls: list[str] = []
    monkeypatch.setattr(marathon, "marathon_transaction_store", lambda _: Store())
    monkeypatch.setattr(marathon, "load_branches", lambda _: calls.append("load") or [])
    monkeypatch.setattr(
        marathon,
        "select_branches",
        lambda *_: calls.append("select") or ([], []),
    )
    with pytest.raises(SystemExit):
        marathon.run_one_cycle(
            {"target_id": "target-a", "run_id": "run-a"},
            execution_mode="research",
        )
    assert calls == []


def test_research_scheduler_sees_only_exactly_authorized_branches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Store:
        root = Path("/tmp/legacy-marathon-state")

        @staticmethod
        def current_generation() -> int:
            return 0

    class ReachedScheduler(RuntimeError):
        pass

    authorization = _verified_gate_fixture({
        "status": "verified_active_current",
        "authoritative": True,
        "target_id": "target-a",
        "run_id": "run-a",
        "eligible_branch_ids": ["branch-authorized"],
    })
    monkeypatch.setattr(marathon, "marathon_transaction_store", lambda _: Store())
    monkeypatch.setattr(marathon, "verify_canonical_theory_cycle", lambda *_, **__: authorization)
    monkeypatch.setattr(
        marathon,
        "load_branches",
        lambda _: [
            {"branch_id": "branch-unbound"},
            {"branch_id": "branch-authorized"},
        ],
    )
    monkeypatch.setattr(marathon, "apply_authoritative_projection", lambda *_: None)

    def observe(branches: list[dict], _: int):
        assert [row["branch_id"] for row in branches] == ["branch-authorized"]
        raise ReachedScheduler

    monkeypatch.setattr(marathon, "select_branches", observe)
    with pytest.raises(ReachedScheduler):
        marathon.run_one_cycle(
            {"target_id": "target-a", "run_id": "run-a", "max_active_branches": 3},
            execution_mode="research",
            canonical_theory_cycle=Path("canonical-cycle-a.json"),
        )


def test_expected_canonical_binding_mismatch_fails_before_branch_loading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Store:
        root = Path("/tmp/legacy-marathon-state")

        @staticmethod
        def current_generation() -> int:
            return 0

    calls: list[str] = []
    authorization = _verified_gate_fixture(
        {
            "status": "verified_active_current",
            "authoritative": True,
            "target_id": "target-a",
            "run_id": "run-a",
            "authorization_digest": canonical_digest("actual-authorization"),
            "schedule_id": "schedule-a",
        }
    )
    monkeypatch.setattr(marathon, "marathon_transaction_store", lambda _: Store())
    monkeypatch.setattr(
        marathon, "verify_canonical_theory_cycle", lambda *_, **__: authorization
    )
    monkeypatch.setattr(marathon, "load_branches", lambda _: calls.append("load") or [])
    with pytest.raises(SystemExit):
        marathon.run_one_cycle(
            {"target_id": "target-a", "run_id": "run-a"},
            execution_mode="research",
            canonical_theory_cycle=Path("canonical-cycle-a.json"),
            canonical_authorization_basis_digest=canonical_digest("wrong-authorization"),
        )
    assert calls == []


def test_artifact_preflight_blocks_before_identity_allocation_or_reservation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class Store:
        root = Path("/tmp/legacy-marathon-state")

        @staticmethod
        def current_generation() -> int:
            return 0

        @staticmethod
        def allocate_identity(_: str) -> str:
            calls.append("allocate")
            return "cycle-a"

    authorization = _verified_gate_fixture(
        {
            "status": "verified_active_current",
            "authoritative": True,
            "target_id": "target-a",
            "run_id": "run-a",
            "commit_id": "commit-a",
            "eligible_branch_ids": ["branch-a"],
        }
    )
    monkeypatch.setattr(marathon, "marathon_transaction_store", lambda _: Store())
    monkeypatch.setattr(
        marathon, "verify_canonical_theory_cycle", lambda *_, **__: authorization
    )
    monkeypatch.setattr(marathon, "load_branches", lambda _: [{"branch_id": "branch-a"}])
    monkeypatch.setattr(marathon, "apply_authoritative_projection", lambda *_: None)
    monkeypatch.setattr(marathon, "filter_authorized_branches", lambda rows, _: rows)
    monkeypatch.setattr(
        marathon,
        "select_branches",
        lambda *_: ([{"branch_id": "branch-a"}], [{"branch_id": "branch-a"}]),
    )
    monkeypatch.setattr(marathon, "literature_gap_preinvestment_control", lambda _: {})
    monkeypatch.setattr(
        marathon,
        "artifact_or_stop_preflight",
        lambda *_: {"preflight_decision": "block_broad_api_marathon"},
    )
    monkeypatch.setattr(
        marathon,
        "reserve_canonical_theory_actions",
        lambda *_args, **_kwargs: calls.append("reserve"),
    )
    with pytest.raises(SystemExit):
        marathon.run_one_cycle(
            {"target_id": "target-a", "run_id": "run-a", "max_active_branches": 1},
            execution_mode="research",
            branch_engine="api",
            canonical_theory_cycle=Path("canonical-cycle-a.json"),
        )
    assert calls == []


def test_reservation_terminal_transition_is_exact_cas(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    state = initial_state("target-a", "run-a")

    class Store:
        target_id = "target-a"
        run_id = "run-a"
        root = tmp_path
        generation = 0

        def current_generation(self) -> int:
            return self.generation

        @staticmethod
        def read_state(generation: int) -> dict:
            assert generation == 0
            return state

        def commit(self, *, expected_generation: int, state: dict, **_: object):
            assert expected_generation == 0
            assert state["generation"] == 1
            self.generation = 1
            return SimpleNamespace(
                commit_id="terminal-commit-a",
                manifest_digest=canonical_digest("terminal-manifest"),
                commit_path=tmp_path / "terminal-commit-a",
            )

    store = Store()
    monkeypatch.setattr(marathon, "DiscoveryTransactionStore", lambda *_args, **_kwargs: store)
    authorization = {
        "target_id": "target-a",
        "run_id": "run-a",
        "committed_state_version": 0,
        "transaction_root": str(tmp_path),
        "reservation": {
            "reservation_id": "reservation-a",
            "reservation_digest": canonical_digest("reservation-a"),
            "action_ids": ["action-a"],
        },
    }
    terminal = marathon.finalize_canonical_action_reservation(
        authorization,
        terminal_status="completed",
        outcome_receipt_id="receipt-a",
        detail="compatibility commit complete",
    )
    assert terminal["terminal_status"] == "completed"
    assert terminal["terminal_state_generation"] == 1
    assert terminal["action_reuse_allowed"] is False
    with pytest.raises(ContractError, match="state changed"):
        marathon.finalize_canonical_action_reservation(
            authorization,
            terminal_status="failed",
            outcome_receipt_id="receipt-b",
            detail="stale retry",
        )


def test_job_command_and_reports_are_exactly_target_run_bound() -> None:
    args = Namespace(
        max_active_branches=2,
        branch_engine="api",
        min_cycle_seconds=60,
        api_key_config=None,
        parallel_branches=True,
        api_max_workers=2,
        api_request_spacing_seconds=0.25,
    )
    binding = marathon_job.ResearchJobBinding(
        target_id="yang-mills-existence-and-mass-gap-target",
        run_id="run-a",
        canonical_theory_cycle="/exact/cycle.json",
        canonical_theory_state_root="/exact/state",
        authorization_basis_digest=canonical_digest("authorization-basis"),
        source_present_decision_digest=canonical_digest("present-decision"),
        schedule_id="schedule-a",
        canonical_cycle_id="cycle-a",
        canonical_commit_id="commit-a",
    )
    command = marathon_job.build_cycle_command(args, binding)
    for flag, value in {
        "--target": binding.target_id,
        "--run-id": binding.run_id,
        "--canonical-theory-cycle": binding.canonical_theory_cycle,
        "--canonical-theory-state-root": binding.canonical_theory_state_root,
        "--canonical-authorization-basis-digest": binding.authorization_basis_digest,
        "--canonical-source-present-decision-digest": binding.source_present_decision_digest,
        "--canonical-schedule-id": binding.schedule_id,
    }.items():
        assert command[command.index(flag) + 1] == value
    reports = marathon.report_rebuild_commands(binding.run_id, binding.target_id)
    rendered = [" ".join(row) for row in reports]
    assert not any("pvsnp_inference" in row or "reasoning_monitor" in row for row in rendered)
    assert any(
        "build_discovery_marathon_report.py" in row
        and f"--run-id {binding.run_id}" in row
        and f"--target-id {binding.target_id}" in row
        for row in rendered
    )


def test_job_rejects_remote_limits_it_cannot_observe() -> None:
    args = Namespace(network_bytes=1, token_count=0, request_count=0, cost_usd=0.0)
    with pytest.raises(marathon_job.JobConfigurationError, match="cannot be enforced honestly"):
        marathon_job.validate_remote_budget_contract(args)


def test_cycle_validator_replays_modern_gate_and_rejects_unbound_selection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stable = {
        "target_id": "target-a",
        "run_id": "run-a",
        "cycle_id": "canonical-cycle-a",
        "prior_state_version": 0,
        "committed_state_version": 1,
        "commit_id": "commit-a",
        "manifest_digest": canonical_digest({"manifest": "a"}),
        "transaction_root": "/tmp/canonical-state",
        "commit_path": "/tmp/canonical-state/commit-a",
        "manifest_path": "/tmp/canonical-state/commit-a/manifest.json",
        "projection_path": "/tmp/canonical-cycle-a.json",
        "projection_digest": canonical_digest({"projection": "a"}),
        "literature_snapshot_id": "snapshot-a",
        "literature_snapshot_digest": canonical_digest({"snapshot": "a"}),
        "schedule_id": "schedule-a",
        "operator_bindings": {"frontier-literature-assimilator": {"receipt_ids": ["receipt-a"]}},
        "eligible_branch_ids": ["branch-authorized"],
        "action_ids_by_branch": {"branch-authorized": ["action-a"]},
        "action_kinds_by_branch": {"branch-authorized": ["reflect"]},
        "authorization_semantics": "exact binding",
    }
    gate = {
        "schema_version": "1.0.0",
        "status": "verified_active_current",
        "authoritative": True,
        **stable,
    }
    cycle = {
        "target_id": "target-a",
        "run_id": "run-a",
        "execution_mode": "research",
        "selected_branch_ids": ["branch-authorized"],
        "skill_dispatch_trace": [{"phase": "current_literature_assimilation_rebase"}],
        "canonical_theory_gate": gate,
    }
    monkeypatch.setattr(
        cycle_validator,
        "verify_canonical_theory_cycle",
        lambda *_, **__: {"status": "verified_active_current", "authoritative": True, **stable},
    )
    cycle_validator.validate_canonical_theory_gate(cycle, Path("cycle-modern-a.json"))
    cycle["selected_branch_ids"] = ["branch-unbound"]
    with pytest.raises(SystemExit):
        cycle_validator.validate_canonical_theory_gate(cycle, Path("cycle-modern-a.json"))


def test_semantic_reducer_preserves_success_and_operational_failure() -> None:
    selected = [{"branch_id": "branch-a"}, {"branch_id": "branch-b"}]
    receipts = [_receipt("branch-a"), _receipt("branch-b", status="failed")]
    states = {
        branch["branch_id"]: initial_branch_state(
            target_id="target-a", run_id="run-a", branch_id=branch["branch_id"]
        )
        for branch in selected
    }
    deltas = marathon.build_marathon_learning_deltas(
        target_id="target-a",
        run_id="run-a",
        cycle_id="cycle-000000000001",
        state_version=0,
        execution_mode="research",
        selected=selected,
        outputs=[_output("branch-a")],
        branch_records=[
            {"branch_id": "branch-a", "status": "complete", "elapsed_seconds": 0.01},
            {"branch_id": "branch-b", "status": "failed", "elapsed_seconds": 0.02},
        ],
        operator_receipts=receipts,
        prior_branch_states=states,
    )
    assert [row["classification"] for row in deltas] == [
        "conceptual_deepening",
        "operational_failure",
    ]
    _, learned = LearningReducer().reduce(states["branch-a"], deltas[0], expected_generation=0)
    failed_state, failed = LearningReducer().reduce(states["branch-b"], deltas[1], expected_generation=0)
    assert learned["learning_recognized"] is True
    assert failed["learning_recognized"] is False
    assert failed_state["operational_outcomes"][0]["worker_status"] == "failed"


def test_cycle_commit_is_one_cas_generation_with_both_siblings(tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")
    selected = [{"branch_id": "branch-a"}, {"branch_id": "branch-b"}]
    states, deltas, reducer_receipts, transaction = marathon.commit_marathon_cycle(
        store,
        cycle_id="cycle-000000000001",
        selected=selected,
        outputs=[_output("branch-a")],
        branch_records=[
            {"branch_id": "branch-a", "status": "complete", "elapsed_seconds": 0.01},
            {"branch_id": "branch-b", "status": "failed", "elapsed_seconds": 0.02},
        ],
        operator_receipts=[_receipt("branch-a"), _receipt("branch-b", status="failed")],
        execution_mode="research",
    )
    assert store.current_generation() == 1
    assert transaction["generation"] == 1
    assert set(states) == {"branch-a", "branch-b"}
    assert len(deltas) == len(reducer_receipts) == 2
    committed = store.read_state()
    assert committed["cycle_history"][0]["successful_branch_ids"] == ["branch-a"]
    assert committed["cycle_history"][0]["operational_failure_branch_ids"] == ["branch-b"]


def test_partial_execution_keeps_successful_sibling(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    store = DiscoveryTransactionStore(tmp_path, target_id="target-a", run_id="run-a")

    def fake_execute(branch: dict, **_: object):
        receipt = _receipt(branch["branch_id"], status="failed" if branch["branch_id"] == "branch-a" else "succeeded")
        record = {
            "branch_id": branch["branch_id"],
            "status": "failed" if branch["branch_id"] == "branch-a" else "complete",
            "operator_receipt_id": receipt["receipt_id"],
            "operator_receipt_status": receipt["status"],
        }
        return (None if branch["branch_id"] == "branch-a" else _output("branch-b")), record, receipt

    monkeypatch.setattr(marathon, "execute_branch_with_receipt", fake_execute)
    outputs, records, receipts = marathon.execute_selected_branches(
        [{"branch_id": "branch-a"}, {"branch_id": "branch-b"}],
        cycle_index=1,
        branch_budget_seconds=1,
        execution_mode="research",
        branch_engine="codex",
        api_key_config=None,
        api_parallel_config={"enabled": False},
        cycle_id="cycle-000000000001",
        target_id="target-a",
        run_id="run-a",
        state_version=0,
        transaction_store=store,
    )
    assert [row["branch_id"] for row in outputs] == ["branch-b"]
    assert [row["status"] for row in records] == ["failed", "complete"]
    assert [row["status"] for row in receipts] == ["failed", "succeeded"]


def test_receipt_backed_validity_ignores_duration_padding() -> None:
    selected = [{"branch_id": "branch-a"}, {"branch_id": "branch-b"}]
    receipts = [_receipt("branch-a"), _receipt("branch-b", status="failed")]
    states = {
        row["branch_id"]: initial_branch_state(
            target_id="target-a", run_id="run-a", branch_id=row["branch_id"]
        )
        for row in selected
    }
    deltas = marathon.build_marathon_learning_deltas(
        target_id="target-a",
        run_id="run-a",
        cycle_id="cycle-000000000001",
        state_version=0,
        execution_mode="research",
        selected=selected,
        outputs=[_output("branch-a")],
        branch_records=[
            {"branch_id": "branch-a", "status": "complete", "elapsed_seconds": 0.001},
            {"branch_id": "branch-b", "status": "failed", "elapsed_seconds": 0.001},
        ],
        operator_receipts=receipts,
        prior_branch_states=states,
    )
    reducer_receipts = [
        LearningReducer().reduce(states[row["identity"]["branch_id"]], row, expected_generation=0)[1]
        for row in deltas
    ]
    recognized = [row["delta_id"] for row in reducer_receipts if row["learning_recognized"]]
    cycle = {
        "target_id": "target-a",
        "run_id": "run-a",
        "execution_mode": "research",
        "selected_branch_ids": ["branch-a", "branch-b"],
        "operator_receipts": receipts,
        "learning_deltas": deltas,
        "learning_reducer_receipts": reducer_receipts,
        "transaction_receipt": {"commit_id": "commit.1"},
        "research_validity_basis": {
            "policy": "semantic_receipts_not_elapsed_time",
            "recognized_learning_delta_ids": recognized,
            "operator_receipt_ids": [row["receipt_id"] for row in receipts],
        },
        "valid_as_research_cycle": True,
        "successful_branch_ids": ["branch-a"],
        "operational_failure_branch_ids": ["branch-b"],
        "research_seconds_target": 3600,
        "research_seconds_elapsed": 0.001,
    }
    validate_receipt_backed_cycle(cycle, Path("cycle-000000000001.json"))
    assert "time.sleep" not in inspect.getsource(marathon.run_one_cycle)


def test_job_outcomes_keep_report_and_resource_failures_distinct() -> None:
    report_status, report_code = marathon_job.classify_job_outcome(
        completed=1,
        failed=0,
        terminal_worker_statuses=["succeeded"],
        report_results=[{"status": "report_failed"}],
    )
    assert (report_status, report_code) == ("completed_with_report_failures", 2)
    deadline_status, deadline_code = marathon_job.classify_job_outcome(
        completed=1,
        failed=1,
        terminal_worker_statuses=["succeeded", "deadline_exhausted"],
        report_results=[{"status": "succeeded"}],
    )
    assert (deadline_status, deadline_code) == ("deadline_exhausted", 3)
