# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused current proof-execution, protocol, and failure-boundary tests."""

from __future__ import annotations

import inspect
import json
import os
import runpy
import stat
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import agentic.discovery.proof_execution as proof_execution
from agentic.discovery.action_coordination_ledger import (
    ActionCoordinationLedger,
)
from agentic.discovery.budgets import (
    complete_governed_process_environment,
    minimal_replacement_environment,
)
from agentic.discovery.contracts import (
    canonical_digest,
    canonical_json,
    stable_identifier,
)
from agentic.discovery.proof import (
    build_postcommit_proof_handoff,
    issue_proof_prelaunch_capability,
)
from agentic.discovery.proof_execution import (
    ProofExecutionTerminalResult,
    build_proof_execution_terminal_result,
    resolve_proof_runtime_route,
    validate_proof_execution_terminal_result,
)
from agentic.discovery.proof_v3_facade import execute_proof_v3


@pytest.fixture(scope="module")
def proof_source(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    module = runpy.run_path(
        str(Path(__file__).with_name("test_proof_action_coordination_ledger.py"))
    )
    return module["_canonical_proof_source"](
        tmp_path_factory.mktemp("proof-execution-v3-source")
    )


def _canonical_source_with_directive(
    root: Path,
    directive: dict[str, Any],
) -> dict[str, Any]:
    """Build a genuine current theory source with one alternate typed claim."""

    original_run_path = runpy.run_path
    gate_module = original_run_path(
        str(Path(__file__).parents[1] / "discovery" / "test_discovery_theory_gate.py")
    )

    def patched_run_path(path: Any, *args: Any, **kwargs: Any) -> Any:
        result = original_run_path(path, *args, **kwargs)
        if str(path).endswith("test_canonical_discovery_cycle.py"):
            seed = result["FORMAL_CLAIM_DIRECTIVE_PREFIX"] + canonical_json(
                directive
            ).decode("utf-8")
            exercise_type = result["CanonicalExercise"]
            for value in (
                *tuple(result.values()),
                *tuple(exercise_type.__dict__.values()),
            ):
                globals_mapping = getattr(value, "__globals__", None)
                if (
                    isinstance(globals_mapping, dict)
                    and "EXACT_FORMAL_SEED" in globals_mapping
                ):
                    globals_mapping["EXACT_FORMAL_SEED"] = seed
        return result

    runpy.run_path = patched_run_path
    try:
        fixture = gate_module["_canonical_fixture"](
            root, formal_seed_mode="ready_exact"
        )
        authorization = gate_module["_verify"](fixture)
    finally:
        runpy.run_path = original_run_path
    return {
        "fixture": fixture,
        "authorization": authorization,
        "handoff": build_postcommit_proof_handoff(authorization),
    }


@pytest.fixture(scope="module")
def alternate_proof_sources(
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[str, dict[str, Any]]:
    root = tmp_path_factory.mktemp("proof-execution-v3-alternate-sources")
    directives = {
        "counterexample": {
            "display_statement": "1/3 + 1/6 = 2/3",
            "formal_claim": {
                "claim_kind": "exact_equality",
                "operation": "equality",
                "left": "1/3 + 1/6",
                "right": "2/3",
            },
            "proof_adapter": "exact",
            "execution_plan": {"kind": "builtin_worker"},
        },
        "finite_model": {
            "display_statement": "forall x in {0,1,2}, x < 3",
            "formal_claim": {
                "claim_kind": "finite_model",
                "variables": {"x": [0, 1, 2]},
                "predicate": "x < 3",
                "quantifier": "forall",
                "max_states": 3,
            },
            "proof_adapter": "finite_model",
            "execution_plan": {"kind": "builtin_worker"},
        },
        "lean": {
            "display_statement": "True",
            "formal_claim": {
                "claim_kind": "lean_proposition",
                "imports": [],
                "proposition": "True",
                "proof_term": "by trivial",
                "axiom_policy": "no_nonstandard_axioms",
            },
            "proof_adapter": "lean",
            "execution_plan": {"kind": "lean", "executable": "lean"},
        },
        "external": {
            "display_statement": "external finite claim",
            "formal_claim": {
                "claim_kind": "external_checker_claim",
                "claim_id": "external-claim",
                "claim_payload": {"value": 1},
            },
            "proof_adapter": "command",
            "execution_plan": {
                "kind": "external_checker",
                "command": ["/bin/true"],
                "checker_identity": "test-checker",
                "checker_version": "1.0",
                "protocol_version": "claim-bound-checker-result/1.0.0",
                "artifact_policy": "none",
                "controlled_output_path": None,
            },
        },
    }
    return {
        name: _canonical_source_with_directive(root / name, directive)
        for name, directive in directives.items()
    }


def _new_capability(
    source: dict[str, Any],
    coordination_root: Path,
) -> tuple[ActionCoordinationLedger, Any, Any]:
    ledger = ActionCoordinationLedger(
        theory_store=source["fixture"]["store"],
        coordination_root=coordination_root,
    )
    reservation = ledger.reserve_proof_attempt(
        theory_authorization=source["authorization"],
        handoff=source["handoff"],
        attempt_number=1,
    )
    capability = issue_proof_prelaunch_capability(
        coordination_ledger=ledger,
        theory_authorization=source["authorization"],
        handoff=source["handoff"],
        reservation_id=reservation.reservation_id,
    )
    return ledger, reservation, capability


@pytest.fixture(scope="module")
def successful_execution(
    proof_source: dict[str, Any],
    tmp_path_factory: pytest.TempPathFactory,
) -> tuple[ActionCoordinationLedger, Any, Any, ProofExecutionTerminalResult]:
    ledger, reservation, capability = _new_capability(
        proof_source,
        tmp_path_factory.mktemp("proof-execution-v3-success")
        / "coordination",
    )
    terminal = execute_proof_v3(capability)
    return ledger, reservation, capability, terminal


def _retained_terminal_and_attachments(
    terminal: ProofExecutionTerminalResult,
) -> tuple[ProofExecutionTerminalResult, dict[str, bytes]]:
    """Build inert pre-finalization evidence for ledger substitution tests."""

    retained = build_proof_execution_terminal_result(
        terminal.claim_binding,
        terminal_status=terminal.terminal_status,
        execution_status=terminal.execution_status,
        proof_verdict=terminal.proof_verdict,
        reason_code=terminal.reason_code,
        started_at=terminal.started_at,
        completed_at=terminal.completed_at,
        invocation=terminal.invocation,
        process_event=terminal.process_event,
        resource_receipt=terminal.resource_receipt,
        checker_output=terminal.checker_output,
        certificate=terminal.certificate,
        artifacts=terminal.artifacts,
    )
    return retained, proof_execution._terminal_attachment_bytes(retained)


def _worker_execute(
    terminal: ProofExecutionTerminalResult,
    *,
    adapter: str,
    formal_claim: dict[str, Any],
) -> dict[str, Any]:
    if terminal.invocation is None:
        raise AssertionError("successful terminal unexpectedly lacks an invocation")
    request = json.loads(terminal.invocation.stdin.content)
    route = resolve_proof_runtime_route(adapter)
    request["adapter"] = adapter
    request["runtime_route_id"] = route.route_id
    request["runtime_route_digest"] = route.projection()["content_digest"]
    request["formal_claim"] = formal_claim
    request["formal_claim_digest"] = canonical_digest(formal_claim)
    request["request_id"] = stable_identifier(
        "proof-execution-request-v1",
        request["binding_id"],
        request["binding_digest"],
        route.route_id,
        request["attempt_id"],
    )
    request["content_digest"] = proof_execution._self_digest(request)
    worker = runpy.run_path(
        str(
            Path(__file__).parents[2]
            / "agentic/scripts/run_discovery_proof_worker_v3.py"
        )
    )
    return worker["execute"](request)


@pytest.mark.expensive
def test_public_executor_is_capability_only_exact_and_durably_finalized(
    successful_execution: tuple[
        ActionCoordinationLedger,
        Any,
        Any,
        ProofExecutionTerminalResult,
    ],
) -> None:
    ledger, reservation, capability, terminal = successful_execution
    parameters = inspect.signature(execute_proof_v3).parameters
    assert list(parameters) == ["capability"]
    assert parameters["capability"].default is inspect.Parameter.empty

    projection = validate_proof_execution_terminal_result(terminal)
    assert projection["terminal_status"] == "completed"
    assert projection["execution_status"] == "succeeded"
    assert projection["proof_verdict"] == (
        "checker_reported_claim_validated_within_declared_scope"
    )
    assert projection["reason_code"] == "checker_response_accepted"
    assert terminal.durably_finalized is True
    assert terminal.durable_bundle is not None
    assert terminal.durable_commit_reference is not None
    assert terminal.durable_bundle["terminal_projection"] == projection
    assert terminal.durable_bundle["lifecycle_terminalization"][
        "respawn_authorized"
    ] is False
    assert terminal.durable_bundle["pending_n_plus_one_reflection_request"][
        "request_status"
    ] == "pending"
    assert (
        ledger.read_proof_terminal_bundle(reservation.reservation_id).record
        == terminal.durable_bundle
    )

    invocation = terminal.invocation
    assert invocation is not None
    binding = invocation.claim_binding.projection
    runtime_root = (
        ledger.coordination_run_root / binding["proof_runtime_ref"]
    )
    assert runtime_root.resolve(strict=True) == runtime_root
    for artifact in (invocation.stdin, *invocation.files):
        staged = runtime_root / artifact.relative_path
        metadata = os.lstat(staged)
        assert stat.S_ISREG(metadata.st_mode)
        assert not stat.S_ISLNK(metadata.st_mode)
        assert metadata.st_nlink == 1
        assert staged.read_bytes() == artifact.content
        assert bool(metadata.st_mode & 0o111) is artifact.executable

    event = terminal.process_event
    resource = terminal.resource_receipt
    assert event is not None and resource is not None
    assert event["command"] == list(invocation.materialized_argv)
    assert event["command"][0] == invocation.executable_authority["source_path"]
    assert event["command"][0] != str(runtime_root / "executables/python")
    assert event["resource_limit_execution"]["replacement_environment_used"] is True
    expected_environment = complete_governed_process_environment(
        minimal_replacement_environment(
            runtime_root, create_temporary=False
        ),
        deadline=resource["deadline"],
        budget=resource["budget"],
    )
    observed_names = {
        row["name"]
        for row in event["supervision_attempt"]["request"][
            "environment_bindings"
        ]
    }
    assert observed_names == set(expected_environment)
    assert "ABDUCER_PROOF_EXECUTION_CANARY" not in observed_names
    assert invocation.executable_authority[
        "stdlib_byte_closure_complete"
    ] is False
    assert invocation.executable_authority[
        "shared_library_byte_closure_complete"
    ] is False

    generation = ledger.current_generation()
    with pytest.raises(Exception, match="already spent"):
        execute_proof_v3(capability)
    assert ledger.current_generation() == generation


@pytest.mark.expensive
def test_exact_false_claim_emits_bound_counterexample(
    successful_execution: tuple[
        ActionCoordinationLedger,
        Any,
        Any,
        ProofExecutionTerminalResult,
    ],
) -> None:
    terminal = successful_execution[3]
    response = _worker_execute(
        terminal,
        adapter="exact",
        formal_claim={
            "claim_kind": "exact_equality",
            "operation": "equality",
            "left": "1/3 + 1/6",
            "right": "2/3",
        },
    )
    assert response["proof_verdict"] == (
        "counterexample_validated_within_declared_scope"
    )
    assert response["result"]["claim_holds"] is False
    assert response["scoped_certificate"]["claim_holds"] is False
    assert response["artifact"] is None
    assert response["content_digest"] == proof_execution._self_digest(response)


@pytest.mark.expensive
def test_finite_model_route_executes_complete_cartesian_claim(
    successful_execution: tuple[
        ActionCoordinationLedger,
        Any,
        Any,
        ProofExecutionTerminalResult,
    ],
) -> None:
    terminal = successful_execution[3]
    response = _worker_execute(
        terminal,
        adapter="finite_model",
        formal_claim={
            "claim_kind": "finite_model",
            "variables": {"x": [0, 1, 2]},
            "predicate": "x < 3",
            "quantifier": "forall",
            "max_states": 3,
        },
    )
    assert response["proof_verdict"] == (
        "claim_validated_within_declared_scope"
    )
    assert response["result"]["claim_holds"] is True
    assert response["completeness"]["complete"] is True
    assert response["completeness"]["explored"] == 3
    assert response["artifact"] is None


@pytest.mark.expensive
def test_exact_counterexample_executes_end_to_end(
    alternate_proof_sources: dict[str, dict[str, Any]],
    tmp_path: Path,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        alternate_proof_sources["counterexample"],
        tmp_path / "coordination",
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "completed"
    assert terminal.proof_verdict == (
        "checker_reported_counterexample_validated_within_declared_scope"
    )
    assert terminal.certificate["claim_holds"] is False
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_finite_model_executes_end_to_end(
    alternate_proof_sources: dict[str, dict[str, Any]],
    tmp_path: Path,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        alternate_proof_sources["finite_model"],
        tmp_path / "coordination",
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "completed"
    assert terminal.proof_verdict == (
        "checker_reported_claim_validated_within_declared_scope"
    )
    assert terminal.certificate["certificate_kind"] == (
        "finite_model_exhaustion"
    )
    assert terminal.certificate["evidence"]["explored"] == 3
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_retained_terminal_helper_covers_every_exact_attachment(
    successful_execution: tuple[
        ActionCoordinationLedger,
        Any,
        Any,
        ProofExecutionTerminalResult,
    ],
) -> None:
    terminal = successful_execution[3]
    retained, attachments = _retained_terminal_and_attachments(terminal)
    assert retained.durably_finalized is False
    assert set(attachments) == {
        "process_event",
        "resource_receipt",
        "checker_output",
        "certificate",
    }
    assert attachments["process_event"] == canonical_json(
        retained.process_event
    )
    assert attachments["resource_receipt"] == canonical_json(
        retained.resource_receipt
    )
    assert attachments["checker_output"] == retained.checker_output
    assert attachments["certificate"] == canonical_json(retained.certificate)


@pytest.mark.expensive
def test_staging_failure_is_totalized_and_finalized(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )

    def fail_staging(*_args: Any, **_kwargs: Any) -> Any:
        raise OSError("injected staging failure")

    monkeypatch.setattr(
        proof_execution, "_create_runtime_root", fail_staging
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "staging_rejected"
    assert terminal.execution_status == "not_started"
    assert terminal.proof_verdict == "not_evaluated"
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_spawn_exception_is_totalized_without_process_evidence(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )

    def fail_spawn(*_args: Any, **_kwargs: Any) -> Any:
        raise OSError("injected spawn failure")

    monkeypatch.setattr(
        proof_execution.ResourceGovernor, "run_process", fail_spawn
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "spawn_failed"
    assert terminal.execution_status == "not_started"
    assert terminal.process_event is None
    assert terminal.resource_receipt is None
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_prelaunch_resource_failure_is_totalized_without_respawn(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )
    original = proof_execution.ResourceGovernor.run_process

    def exhaust_input(
        self: Any,
        command: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        kwargs["input_limit_bytes"] = 1
        return original(self, command, **kwargs)

    monkeypatch.setattr(
        proof_execution.ResourceGovernor, "run_process", exhaust_input
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "governed_not_started"
    assert terminal.execution_status == "input_exhausted"
    assert terminal.process_event["pid"] is None
    assert terminal.proof_verdict == "not_evaluated"
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_receipt_projection_failure_uses_exact_observed_fallback(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )

    def fail_receipt(*_args: Any, **_kwargs: Any) -> Any:
        raise RuntimeError("injected receipt projection failure")

    monkeypatch.setattr(
        proof_execution.ResourceGovernor, "receipt", fail_receipt
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "completed"
    assert terminal.resource_receipt["events"] == [terminal.process_event]
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_post_spawn_authority_failure_preserves_governed_evidence(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )
    original = proof_execution._revalidate_pre_spawn_authority
    calls = 0

    def reject_second_replay(*args: Any, **kwargs: Any) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected post-spawn byte drift")
        original(*args, **kwargs)

    monkeypatch.setattr(
        proof_execution,
        "_revalidate_pre_spawn_authority",
        reject_second_replay,
    )
    terminal = execute_proof_v3(capability)
    assert calls == 2
    assert terminal.terminal_status == "protocol_rejected"
    assert terminal.reason_code == "post_spawn_authority_rejected"
    assert terminal.execution_status == "succeeded"
    assert terminal.process_event["pid"] > 0
    assert terminal.resource_receipt["events"] == [terminal.process_event]
    assert terminal.proof_verdict == "not_evaluated"
    assert terminal.certificate is None
    assert terminal.durably_finalized is True


@pytest.mark.expensive
def test_transient_finalization_failure_retries_only_the_same_terminal(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger, reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )
    original = ActionCoordinationLedger.finalize_proof_execution
    calls = 0

    def fail_once(
        self: ActionCoordinationLedger,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        nonlocal calls
        if self is ledger:
            calls += 1
            if calls == 1:
                raise OSError("injected precommit finalization failure")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(
        ActionCoordinationLedger, "finalize_proof_execution", fail_once
    )
    terminal = execute_proof_v3(capability)
    assert calls == 2
    assert terminal.terminal_status == "completed"
    assert terminal.durably_finalized is True
    assert (
        ledger.read_proof_terminal_bundle(reservation.reservation_id).record[
            "terminal_projection"
        ]
        == terminal.projection
    )


@pytest.mark.expensive
@pytest.mark.parametrize(
    "replacement",
    [b"", b"{}", b"not-json"],
    ids=("empty", "noop-object", "malformed"),
)
def test_empty_noop_and_malformed_output_are_protocol_rejected(
    proof_source: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement: bytes,
) -> None:
    _ledger, _reservation, capability = _new_capability(
        proof_source, tmp_path / "coordination"
    )
    original = proof_execution.validate_v2_process_event

    def substitute_retained_output(
        event: Any,
        *,
        accepted: bool,
        **kwargs: Any,
    ) -> Any:
        attempt = original(event, accepted=accepted, **kwargs)
        if accepted and attempt is not None:
            return SimpleNamespace(
                stdout=SimpleNamespace(retained_tail=replacement)
            )
        return attempt

    monkeypatch.setattr(
        proof_execution,
        "validate_v2_process_event",
        substitute_retained_output,
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "protocol_rejected"
    assert terminal.execution_status == "succeeded"
    assert terminal.proof_verdict == "not_evaluated"
    assert terminal.certificate is None
    assert terminal.durably_finalized is True


@pytest.mark.expensive
@pytest.mark.parametrize("route_name", ["lean", "external"])
def test_unavailable_route_rejects_without_ambient_path_or_spawn(
    alternate_proof_sources: dict[str, dict[str, Any]],
    tmp_path: Path,
    route_name: str,
) -> None:
    ledger, _reservation, capability = _new_capability(
        alternate_proof_sources[route_name], tmp_path / "coordination"
    )
    terminal = execute_proof_v3(capability)
    assert terminal.terminal_status == "staging_rejected"
    assert terminal.reason_code == "runtime_executable_authority_unavailable"
    assert terminal.process_event is None
    assert terminal.durably_finalized is True
    runtime_root = (
        ledger.coordination_run_root
        / terminal.claim_binding.projection["proof_runtime_ref"]
    )
    assert not runtime_root.exists()
    assert resolve_proof_runtime_route("command").adapter == "external"
    assert (
        resolve_proof_runtime_route("command").projection()[
            "ambient_path_resolution_allowed"
        ]
        is False
    )
