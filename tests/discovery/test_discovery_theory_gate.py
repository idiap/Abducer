# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for the canonical-theory compatibility authorization.

The fixture builds the current canonical cycle through its real constructors,
then reopens the immutable commit and authorization projection. Tests corrupt
one boundary at a time without relying on a mutable checked-in research run.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import runpy
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    file_digest,
)
from agentic.discovery.proof import (
    build_postcommit_proof_handoff,
    build_proof_handoff,
    reopen_current_proof_handoff,
    validate_proof_handoff,
)
from agentic.discovery.cycle import run_canonical_discovery_cycle
import agentic.discovery.theory_gate as theory_gate
from agentic.discovery.theory_gate import (
    REQUIRED_THEORY_OPERATOR_IDS,
    SYSTEM_UTC_CLOCK_AUTHORITY_ID,
    VerifiedTheoryAuthorization,
    authorization_is_runtime_verified,
    authorization_projection,
    filter_authorized_branches,
    reserve_canonical_theory_actions,
    verify_canonical_theory_cycle,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


def _json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n"


def _event_spec(operator_id: str, branch_id: str) -> tuple[str, str, str, dict[str, Any]]:
    """Return the role-specific semantic event shape required by the gate."""

    if operator_id == "frontier-literature-assimilator":
        return (
            "literature_snapshot_recorded",
            "literature_snapshot",
            "snapshot-active",
            {
                "completed_at": "2026-07-21T10:00:00Z",
                "coverage_cutoff": "2026-07-21T10:00:00Z",
                "content_digest": canonical_digest({"snapshot": "active"}),
                "source_claim_mappings": [],
                "source_theory_deltas": [],
                "affected_branch_ids": [branch_id],
                "survivor_branch_ids": [branch_id],
                "branch_rebases": [
                    {
                        "branch_id": branch_id,
                        "disposition": "survives",
                        "theory_delta": {"effect": "explicitly unchanged"},
                    }
                ],
            },
        )
    if operator_id == "high-risk-hypothesis-forger":
        return (
            "entity_upsert",
            "hypothesis",
            "hypothesis-a",
            {"record": {"status": "proposed", "branch_id": branch_id}},
        )
    if operator_id == "parallel-hypothesis-portfolio":
        return (
            "branch_attempt_recorded",
            "branch_attempt",
            "attempt-a",
            {
                "branch_id": branch_id,
                "outcome": "validated",
                "parent_branch_ids": [],
                "conflicts": [],
                "artifact_digests": [canonical_digest({"attempt": "a"})],
            },
        )
    if operator_id == "reflective-conceptual-discovery":
        return (
            "reflection_recorded",
            "reflection",
            "reflection-parent",
            {"kind": "parent_reflection", "material_mutation": True},
        )
    return (
        "reflection_recorded",
        "reflection",
        "reflection-synthesis",
        {"kind": "parallel_branch_delta_integration", "dissent_preserved": True},
    )


def _canonical_fixture(
    tmp_path: Path,
    *,
    literature_mode: str = "active_current",
    proof: bool = False,
    bound_conceptual_evidence: bool = False,
    adjudication_outcome: str = "unique",
    formal_seed_mode: str = "absent",
) -> dict[str, Any]:
    """Commit a minimal but genuine canonical cycle and return its addresses."""

    exercise_module = runpy.run_path(
        str(Path(__file__).with_name("test_canonical_discovery_cycle.py"))
    )
    exercise_type = exercise_module["CanonicalExercise"]
    tmp_path.mkdir(parents=True, exist_ok=True)
    exercise = exercise_type(
        tmp_path,
        live=literature_mode == "active_current",
        experiment=False,
        registry_routes=formal_seed_mode != "absent",
        bound_conceptual_evidence=bound_conceptual_evidence,
        adjudication_outcome=adjudication_outcome,
        formal_seed_mode=formal_seed_mode,
    )
    formal = (
        exercise_module["_attach_formal_claim"](exercise)
        if formal_seed_mode != "absent"
        else None
    )
    proof_request = exercise_module["_proof_request"](exercise) if proof else None
    projection = run_canonical_discovery_cycle(
        **exercise.cycle_kwargs(),
        **({"proof_request": proof_request} if proof_request else {}),
    )
    projection_path = tmp_path / "canonical-cycle-theory-a.json"
    projection_path.write_bytes(_json_bytes(projection))
    branch_id = projection["parallel_outcome"]["valid_branch_ids"][0]
    return {
        "target_id": exercise.target_id,
        "run_id": exercise.run_id,
        "branch_id": branch_id,
        "state_root": exercise.state_root,
        "store": DiscoveryTransactionStore(
            exercise.state_root,
            target_id=exercise.target_id,
            run_id=exercise.run_id,
        ),
        "projection": projection,
        "projection_path": projection_path,
        "commit_path": Path(projection["commit_path"]),
        "exercise": exercise,
        "formal": formal,
    }


def _rewrite_committed_artifact(fixture: dict[str, Any], role: str, payload: Any) -> None:
    """Rewrite one test artifact and consistently refresh nonsemantic digests."""

    projection = fixture["projection"]
    relative = projection["artifact_paths"][role]
    artifact = fixture["commit_path"] / "artifacts" / relative
    artifact.write_bytes(_json_bytes(payload))
    digest = file_digest(artifact)
    projection["artifact_digests"][role] = digest
    manifest_path = fixture["commit_path"] / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    descriptor = next(row for row in manifest["artifacts"] if row["path"] == relative)
    descriptor["sha256"] = digest
    descriptor["size_bytes"] = artifact.stat().st_size
    manifest_path.write_bytes(_json_bytes(manifest))
    projection["manifest_digest"] = file_digest(manifest_path)
    fixture["projection_path"].write_bytes(_json_bytes(projection))


def _verify(fixture: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    return verify_canonical_theory_cycle(
        fixture["projection_path"],
        target_id=fixture["target_id"],
        run_id=fixture["run_id"],
        state_root=fixture["state_root"],
        **kwargs,
    )


def test_gate_rejects_same_generation_experiment_roles_in_valid_core_closure(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path)
    projection = fixture["projection"]
    commit_path = fixture["commit_path"]
    manifest = json.loads(
        (commit_path / "manifest.json").read_text(encoding="utf-8")
    )
    committed = theory_gate._verify_committed_artifacts(  # noqa: SLF001
        projection,
        commit_path=commit_path,
        manifest=manifest,
    )
    evidence_index = theory_gate._verify_operator_evidence(  # noqa: SLF001
        projection,
        committed=committed,
        commit_path=commit_path,
    )
    role_payloads = copy.deepcopy(evidence_index["role_payloads"])
    role_payloads["experiment_spec"] = [
        {"historical_kind": "same_generation_experiment_spec"}
    ]
    role_payloads["experiment_receipt"] = [
        {"historical_kind": "same_generation_experiment_receipt"}
    ]

    with pytest.raises(
        ContractError,
        match="same-generation experiment roles.*descendant support",
    ):
        theory_gate._validate_role_payloads(role_payloads)  # noqa: SLF001


def test_gate_replays_ready_formal_claim_join_from_committed_bytes(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="ready_exact")
    formal = fixture["formal"]
    prove = next(
        action
        for action in fixture["projection"]["schedule"]["actions"]
        if action["kind"] == "prove"
    )
    fixture["exercise"].workspace.rename(tmp_path / "detached-original-workspace")
    authorization = _verify(fixture)
    join = authorization["formal_claim_schedule_join"]

    assert join["status"] == "ready_prove_pending"
    assert join["output_id"] == formal["output"]["output_id"]
    assert join["producer_receipt_id"] == formal["receipt"]["receipt_id"]
    assert join["producer_receipt_id"] != fixture["exercise"].synthesis_receipt[
        "receipt_id"
    ]
    assert join["action_id"] == prove["action_id"]
    assert join["binding_digest"] == canonical_digest(
        prove["payload"]["formal_claim_binding"]
    )
    assert authorization["authorization_basis"][
        "formal_claim_schedule_join_digest"
    ] == join["join_digest"]
    assert join["authority_nulls"] == {
        "claim_truth": False,
        "checker_soundness": False,
        "theorem_status": False,
        "physics_value": False,
    }


def test_postcommit_handoff_is_exact_deterministic_and_projection_only(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="ready_exact")
    fixture["exercise"].workspace.rename(tmp_path / "detached-producer-workspace")
    authorization = _verify(fixture)

    first = build_postcommit_proof_handoff(authorization)
    second = build_proof_handoff(authorization)
    assert first == second
    assert reopen_current_proof_handoff(authorization, first) == first
    prove = next(
        action for action in authorization["schedule"]["actions"]
        if action["kind"] == "prove"
    )
    binding = prove["payload"]["formal_claim_binding"]
    assert first["schema_version"] == 3
    assert first["scheduled_action"] == prove
    assert first["scheduled_action_id"] == prove["action_id"]
    assert first["formal_claim_schedule_binding"] == binding
    assert first["producer_receipt_id"] == binding["producer_receipt_id"]
    assert first["producer_output_id"] == binding["output_id"]
    assert first["formal_claim_digest"] == binding["formal_claim_digest"]
    assert first["execution_plan_digest"] == binding["execution_plan_digest"]
    assert first["source_commit_id"] == authorization["commit_id"]
    assert first["source_commit_generation"] == authorization[
        "committed_state_version"
    ]
    assert first["scheduled_action"]["state_version"] + 1 == first[
        "theory_generation"
    ]
    assert first["resource_budget"]["absolute_deadline"] == first[
        "literature_consume_before"
    ]
    assert first["projection_only"] is True
    assert first["postcommit_reopen_required"] is True
    assert first["authority_nulls"] == {
        "truth_authority": False,
        "checker_soundness_authority": False,
        "theorem_authority": False,
        "physics_authority": False,
        "theory_selection_authority": False,
        "same_cycle_theory_mutation": False,
        "serialized_execution_authority": False,
        "cryptographic_authenticity": False,
    }

    with pytest.raises(ContractError, match="raw caller-built proof handoffs"):
        build_proof_handoff(first)

    forged = copy.deepcopy(first)
    forged["display_statement"] = "caller-authored detached replacement"
    forged["content_digest"] = canonical_digest(
        {key: value for key, value in forged.items() if key != "content_digest"}
    )
    assert validate_proof_handoff(forged) == forged
    with pytest.raises(ContractError, match="current committed reconstruction"):
        reopen_current_proof_handoff(authorization, forged)


def test_not_ready_formal_output_cannot_mint_postcommit_handoff(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="untyped_ready")
    authorization = _verify(fixture)
    with pytest.raises(
        ContractError,
        match="not-ready formalization has no current claim authority",
    ):
        build_postcommit_proof_handoff(authorization)


def test_gate_replays_not_ready_formal_claim_without_prove(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="untyped_ready")
    authorization = _verify(fixture)
    join = authorization["formal_claim_schedule_join"]
    assert join["status"] == "not_ready_no_prove"
    assert join["output_id"] == fixture["formal"]["output"]["output_id"]
    assert join["producer_receipt_id"] == fixture["formal"]["receipt"][
        "receipt_id"
    ]
    assert join["action_id"] is None
    assert join["binding_digest"] is None
    assert all(
        action["kind"] != "prove"
        for action in authorization["schedule"]["actions"]
    )


def _formal_join_replay_inputs(
    fixture: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = json.loads((fixture["commit_path"] / "manifest.json").read_text())
    committed = theory_gate._verify_committed_artifacts(
        fixture["projection"],
        commit_path=fixture["commit_path"],
        manifest=manifest,
    )
    evidence_index = theory_gate._verify_operator_evidence(
        fixture["projection"],
        committed=committed,
        commit_path=fixture["commit_path"],
    )
    operator_bindings = theory_gate._verify_feedback_lineage(
        fixture["projection"], evidence_index
    )
    return evidence_index, operator_bindings


def test_gate_formal_join_rejects_action_omission_duplicate_and_substitution(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="ready_exact")
    evidence_index, operator_bindings = _formal_join_replay_inputs(fixture)
    original = fixture["projection"]
    prove = next(
        action for action in original["schedule"]["actions"]
        if action["kind"] == "prove"
    )

    omitted = copy.deepcopy(original)
    omitted["schedule"]["actions"] = [
        action for action in omitted["schedule"]["actions"]
        if action["action_id"] != prove["action_id"]
    ]
    with pytest.raises(
        ContractError,
        match="ready formal-claim output does not have exactly one bound prove action",
    ):
        theory_gate._verify_formal_claim_schedule_join(
            omitted, evidence_index, operator_bindings
        )

    duplicated = copy.deepcopy(original)
    duplicate = copy.deepcopy(prove)
    duplicate["action_id"] = "action.duplicate-formal-prove"
    duplicated["schedule"]["actions"].append(duplicate)
    with pytest.raises(
        ContractError,
        match="ready formal-claim output does not have exactly one bound prove action",
    ):
        theory_gate._verify_formal_claim_schedule_join(
            duplicated, evidence_index, operator_bindings
        )

    substitutions = {
        "producer receipt": (
            "producer_receipt_id",
            fixture["formal"]["output"]["source_operator_receipt_id"],
        ),
        "output digest": ("output_digest", canonical_digest("wrong-output")),
        "claim digest": (
            "formal_claim_digest",
            canonical_digest("wrong-claim"),
        ),
        "plan digest": (
            "execution_plan_digest",
            canonical_digest("wrong-plan"),
        ),
        "generation": ("source_theory_generation", 99),
    }
    for field, value in substitutions.values():
        tampered = copy.deepcopy(original)
        target = next(
            action for action in tampered["schedule"]["actions"]
            if action["kind"] == "prove"
        )
        target["payload"]["formal_claim_binding"][field] = value
        with pytest.raises(
            ContractError,
            match="ready formal-claim action differs from the independently replayed committed join",
        ):
            theory_gate._verify_formal_claim_schedule_join(
                tampered, evidence_index, operator_bindings
            )

    for field, value in (
        ("status", "consumed"),
        ("restrictions", ["no_active_investment"]),
        ("branch_ids", ["branch.substituted"]),
    ):
        tampered = copy.deepcopy(original)
        target = next(
            action for action in tampered["schedule"]["actions"]
            if action["kind"] == "prove"
        )
        target[field] = value
        with pytest.raises(
            ContractError,
            match="ready formal-claim action differs from the independently replayed committed join",
        ):
            theory_gate._verify_formal_claim_schedule_join(
                tampered, evidence_index, operator_bindings
            )


def test_gate_rejects_prove_injected_for_not_ready_formal_output(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, formal_seed_mode="untyped_ready")
    evidence_index, operator_bindings = _formal_join_replay_inputs(fixture)
    tampered = copy.deepcopy(fixture["projection"])
    injected = copy.deepcopy(tampered["schedule"]["actions"][0])
    injected["action_id"] = "action.injected-not-ready-prove"
    injected["kind"] = "prove"
    injected["payload"]["formal_claim_binding"] = {
        "injected": "untrusted"
    }
    tampered["schedule"]["actions"].append(injected)
    with pytest.raises(
        ContractError,
        match="not-ready formal-claim output leaked a prove action",
    ):
        theory_gate._verify_formal_claim_schedule_join(
            tampered, evidence_index, operator_bindings
        )


@pytest.mark.parametrize(
    "corruption",
    ["omit_spec", "omit_receipt", "duplicate_spec", "duplicate_receipt", "foreign_id", "digest_drift"],
)
@pytest.mark.skip(
    reason="historical experiment-v1 pairing is quarantined; v2 pre-execution commission tests own this surface"
)
def test_experiment_pair_is_exact_and_rejected_before_any_commit(
    tmp_path: Path,
    corruption: str,
) -> None:
    """Every malformed experiment pair fails while generation zero is intact."""

    exercise_module = runpy.run_path(
        str(Path(__file__).with_name("test_canonical_discovery_cycle.py"))
    )
    exercise = exercise_module["CanonicalExercise"](
        tmp_path,
        live=True,
        experiment=True,
    )
    roles = copy.deepcopy(exercise.roles)
    if corruption == "omit_spec":
        roles.pop("experiment_spec")
    elif corruption == "omit_receipt":
        roles.pop("experiment_receipt")
    elif corruption == "duplicate_spec":
        roles["experiment_spec"] = [roles["experiment_spec"], roles["experiment_spec"]]
    elif corruption == "duplicate_receipt":
        roles["experiment_receipt"] = [
            roles["experiment_receipt"],
            roles["experiment_receipt"],
        ]
    else:
        spec_path = exercise.workspace / roles["experiment_spec"]
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        if corruption == "foreign_id":
            spec["experiment_id"] = "experiment.foreign"
            spec["spec_digest"] = canonical_digest(
                spec,
                exclude_keys=("spec_digest", "created_at"),
            )
        else:
            spec["spec_digest"] = canonical_digest({"forged": "spec-digest"})
        spec_path.write_bytes(_json_bytes(spec))

    kwargs = exercise.cycle_kwargs()
    kwargs["artifact_roles"] = roles
    store = DiscoveryTransactionStore(
        exercise.state_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    with pytest.raises(ContractError, match="experiment|specification|receipt"):
        run_canonical_discovery_cycle(**kwargs)
    assert store.current_generation() == 0
    assert list(store.commits_dir.iterdir()) == []


@pytest.mark.skip(
    reason="historical post-execution experiment-v1 causality is non-authoritative in the canonical gate"
)
def test_theory_gate_shared_causality_root_rejects_rehashed_experiment_disconnects(
    tmp_path: Path,
) -> None:
    """The gate replays parent question, registered claim, and synthesis use."""

    exercise_module = runpy.run_path(
        str(Path(__file__).with_name("test_canonical_discovery_cycle.py"))
    )
    exercise = exercise_module["CanonicalExercise"](
        tmp_path,
        live=True,
        experiment=True,
    )
    requests = copy.deepcopy(exercise.requests)
    inputs = {
        request["request_id"]: [
            json.loads(
                (
                    exercise.workspace
                    / request["input_artifacts"][0]["path"]
                ).read_text(encoding="utf-8")
            )
        ]
        for request in requests
    }
    payloads = {
        "literature_snapshot": [copy.deepcopy(exercise.snapshot)],
        "literature_assimilation": [copy.deepcopy(exercise.assimilation)],
        "high_risk_portfolio": [copy.deepcopy(exercise.portfolio)],
        "parallel_portfolio": [copy.deepcopy(exercise.parallel)],
        "reflective_packets": [
            copy.deepcopy(exercise.parent_packet),
            copy.deepcopy(exercise.synthesis_packet),
        ],
        "experiment_spec": [copy.deepcopy(exercise.experiment_spec)],
        "experiment_receipt": [copy.deepcopy(exercise.experiment_receipt)],
    }

    def validate(
        request_rows: list[dict[str, Any]],
        input_rows: dict[str, list[dict[str, Any]]],
        payload_rows: dict[str, list[dict[str, Any]]],
    ) -> None:
        theory_gate._validate_stage_causality(  # noqa: SLF001
            operator_requests=request_rows,
            input_payloads=input_rows,
            payloads=payload_rows,
        )

    validate(requests, inputs, payloads)

    experiment_request = next(
        row
        for row in requests
        if row["operator"]["operator_id"]
        == "dynamic-symbolic-simulation-experimenter"
    )
    forged_inputs = copy.deepcopy(inputs)
    forged_claim = forged_inputs[experiment_request["request_id"]][0][
        "triage_request"
    ]["registered_theory_claims"][0]
    forged_claim["statement"] = "A disconnected registered claim"
    forged_claim["claim_digest"] = canonical_digest(
        forged_claim,
        exclude_keys=("claim_digest",),
    )
    with pytest.raises(
        ContractError,
        match="valid theory commission|specification|tested claim",
    ):
        validate(requests, forged_inputs, payloads)

    synthesis_request = next(
        row
        for row in requests
        if row["operator"]["operator_id"] == "reflective-theory-synthesizer"
    )
    omitted_result_inputs = copy.deepcopy(inputs)
    omitted_result_inputs[synthesis_request["request_id"]][0].pop(
        "experiment_result"
    )
    with pytest.raises(ContractError, match="exactly once"):
        validate(requests, omitted_result_inputs, payloads)

    wrong_final_payloads = copy.deepcopy(payloads)
    final_packet = wrong_final_payloads["reflective_packets"][-1]
    final_packet["support_probe"]["receipt_ids"] = ["opreceipt.wrong-result"]
    final_packet["packet_digest"] = canonical_digest(
        final_packet,
        exclude_keys=("packet_digest",),
    )
    with pytest.raises(ContractError, match="exact experiment receipt"):
        validate(requests, inputs, wrong_final_payloads)

    duplicated_requests = copy.deepcopy(requests)
    duplicated_inputs = copy.deepcopy(inputs)
    duplicate = copy.deepcopy(synthesis_request)
    duplicate["request_id"] = "opreq.duplicate-post-result-synthesis"
    duplicated_requests.append(duplicate)
    duplicated_inputs[duplicate["request_id"]] = copy.deepcopy(
        inputs[synthesis_request["request_id"]]
    )
    with pytest.raises(ContractError, match="exactly once"):
        validate(duplicated_requests, duplicated_inputs, payloads)

    no_probe_payloads = copy.deepcopy(payloads)
    parent_packet = no_probe_payloads["reflective_packets"][0]
    parent_packet["support_probe"]["disposition"] = "no_probe_needed"
    parent_packet["packet_digest"] = canonical_digest(
        parent_packet,
        exclude_keys=("packet_digest",),
    )
    with pytest.raises(
        ContractError,
        match="exact parent packet|identity is missing|no_probe",
    ):
        validate(requests, inputs, no_probe_payloads)


def test_governed_clock_factory_and_temporal_boundaries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Clock authority is closed, microsecond-precise, and non-renewing."""

    with pytest.raises(TypeError, match="issued only"):
        VerifiedTheoryAuthorization({"authoritative": True})

    fixture = _canonical_fixture(tmp_path)
    consume_before = dt.datetime.fromisoformat(
        fixture["projection"]["literature_basis"]["consume_before"].replace(
            "Z", "+00:00"
        )
    )
    first_instant = consume_before - dt.timedelta(microseconds=1)
    monkeypatch.setattr(theory_gate, "_system_utc_now", lambda: first_instant)
    first = _verify(fixture)
    assert first["present_investment_decision"]["clock_authority"]["authority_id"] == (
        SYSTEM_UTC_CLOCK_AUTHORITY_ID
    )
    assert first["present_investment_decision"]["clock_authority"][
        "caller_supplied_instants_allowed"
    ] is False
    assert first["present_investment_decision"]["evaluated_at"].endswith("999999Z")

    monkeypatch.setattr(theory_gate, "_system_utc_now", lambda: consume_before)
    at_boundary = _verify(fixture)
    assert at_boundary["authorization_basis_digest"] == first[
        "authorization_basis_digest"
    ]
    assert at_boundary["present_investment_decision_digest"] != first[
        "present_investment_decision_digest"
    ]

    monkeypatch.setattr(
        theory_gate,
        "_system_utc_now",
        lambda: consume_before + dt.timedelta(microseconds=1),
    )
    with pytest.raises(ContractError, match="consume_before_expired"):
        _verify(fixture)

    with pytest.raises(ContractError, match="unregistered present clock authority"):
        _verify(fixture, clock_authority_id="caller-forged-clock.v1")


def test_backward_or_naive_clock_fails_and_historical_replay_never_reads_it(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = _canonical_fixture(tmp_path)
    commit = json.loads(
        (fixture["commit_path"] / "manifest.json").read_text(encoding="utf-8")
    )
    commit_at = dt.datetime.fromisoformat(commit["created_at"].replace("Z", "+00:00"))

    monkeypatch.setattr(theory_gate, "_system_utc_now", lambda: dt.datetime(2026, 7, 22))
    with pytest.raises(ContractError, match="timezone-naive"):
        _verify(fixture)
    monkeypatch.setattr(
        theory_gate,
        "_system_utc_now",
        lambda: commit_at - dt.timedelta(microseconds=1),
    )
    with pytest.raises(ContractError, match="precedes the immutable canonical commit"):
        _verify(fixture)

    def forbidden_clock_read() -> dt.datetime:
        raise AssertionError("historical replay must not read a present clock")

    monkeypatch.setattr(theory_gate, "_system_utc_now", forbidden_clock_read)
    historical = _verify(fixture, require_current=False)
    assert authorization_is_runtime_verified(historical) is False
    assert historical["historical_investment_eligibility"] == "not_authorized"
    assert "eligible_branch_ids" not in historical
    assert historical["counterfactual_eligible_branch_ids"]
    assert historical["present_investment_decision"] is None


def test_exact_commit_authorizes_only_bound_scheduled_legacy_branches(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    authorization = _verify(fixture)
    assert fixture["branch_id"] in authorization["eligible_branch_ids"]
    assert set(authorization["operator_bindings"]).issuperset(REQUIRED_THEORY_OPERATOR_IDS)
    assert all(
        binding["producer_output_artifacts"]
        for binding in authorization["operator_bindings"].values()
    )
    branches = [
        {"branch_id": "unbound-branch", "title": "Must not reach the scheduler"},
        {"branch_id": fixture["branch_id"], "title": "Explicitly authorized"},
    ]
    assert filter_authorized_branches(branches, authorization) == [branches[1]]


@pytest.mark.parametrize(
    ("literature_mode", "adjudication_outcome", "expected_status", "investable"),
    [
        ("active_current", "unique", "sealed_unique", True),
        ("active_current", "plural", "sealed_plural", True),
        (
            "active_current",
            "revise_all",
            "sealed_revise_all_diagnostic_only",
            False,
        ),
        (
            "local_only_incubation",
            "unique",
            "absent_diagnostic_only",
            False,
        ),
    ],
)
def test_gate_replays_total_set_valued_authority_matrix(
    tmp_path: Path,
    literature_mode: str,
    adjudication_outcome: str,
    expected_status: str,
    investable: bool,
) -> None:
    fixture = _canonical_fixture(
        tmp_path,
        literature_mode=literature_mode,
        adjudication_outcome=adjudication_outcome,
    )
    authorization = _verify(fixture)
    authority = authorization["conceptual_authority"]
    assert authority["status"] == expected_status
    assert authorization["investment_authorized"] is investable
    assert authorization["authoritative"] is investable
    assert authorization_is_runtime_verified(authorization) is investable
    if investable:
        assert authorization["status"] == "verified_active_current"
        assert authorization["eligible_branch_ids"]
        assert len(
            authorization["operator_bindings"][
                "blind-conceptual-preference-adjudicator"
            ]["receipt_ids"]
        ) == 2
        assert authorization["source_routing_pre_map_policy_digest"]
        assert authorization["source_routing_realization_digest"]
    else:
        assert authorization["eligible_branch_ids"] == []
        assert authorization["action_ids_by_branch"] == {}
        assert authorization["action_kinds_by_branch"] == {}
        with pytest.raises(
            ContractError, match="live runtime-verified authorization"
        ):
            filter_authorized_branches(
                [{"branch_id": fixture["branch_id"]}], authorization
            )
    if literature_mode == "local_only_incubation":
        assert authorization["status"] == "verified_local_incubation"
        assert authorization["source_routing_pre_map_policy_id"] is None
        assert authorization["source_routing_realization_id"] is None
        assert set(authorization["operator_bindings"]) == (
            theory_gate.LOCAL_REQUIRED_THEORY_OPERATOR_IDS
        )


def test_absent_wrong_target_and_local_only_projections_fail_closed(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path / "active")
    with pytest.raises(ContractError, match="does not exist"):
        verify_canonical_theory_cycle(
            tmp_path / "absent-cycle.json",
            target_id=fixture["target_id"],
            run_id=fixture["run_id"],
            state_root=fixture["state_root"],
        )
    with pytest.raises(ContractError, match="target identity mismatch"):
        verify_canonical_theory_cycle(
            fixture["projection_path"],
            target_id="wrong-target",
            run_id=fixture["run_id"],
            state_root=fixture["state_root"],
        )
    local = _canonical_fixture(tmp_path / "local", literature_mode="local_only_incubation")
    local_authorization = _verify(local)
    assert local_authorization["status"] == "verified_local_incubation"
    assert local_authorization["authoritative"] is False
    assert local_authorization["eligible_branch_ids"] == []


def test_stale_generation_and_reused_lineage_are_rejected(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    authorization = _verify(fixture)
    state = fixture["store"].read_state(1)
    assert state is not None
    advanced = copy.deepcopy(state)
    advanced["generation"] = 2
    fixture["store"].commit(
        expected_generation=1,
        state=advanced,
        artifacts=[],
        idempotency_key="advance-canonical-state",
        request_digest=canonical_digest({"advance": 2}),
    )
    with pytest.raises(ContractError, match="is stale"):
        _verify(fixture)

    fresh = _canonical_fixture(tmp_path / "reuse")
    first = _verify(fresh)
    with pytest.raises(ContractError, match="does not continue|already consumed"):
        verify_canonical_theory_cycle(
            fresh["projection_path"],
            target_id=fresh["target_id"],
            run_id=fresh["run_id"],
            state_root=fresh["state_root"],
            previous_lineage=first,
        )


def test_manifest_and_event_hash_tampering_are_independently_rejected(tmp_path: Path) -> None:
    manifest_fixture = _canonical_fixture(tmp_path / "manifest")
    manifest_path = manifest_fixture["commit_path"] / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["request_digest"] = canonical_digest({"tampered": True})
    manifest_path.write_bytes(_json_bytes(manifest))
    with pytest.raises(ContractError, match="content-derived commit ID mismatch"):
        _verify(manifest_fixture)

    event_fixture = _canonical_fixture(tmp_path / "event")
    tampered_events = copy.deepcopy(event_fixture["projection"]["events"])
    tampered_events[-1]["payload"]["dissent_preserved"] = False
    event_fixture["projection"]["events"] = tampered_events
    _rewrite_committed_artifact(event_fixture, "events", tampered_events)
    with pytest.raises(ContractError, match="content-derived commit ID mismatch"):
        _verify(event_fixture)


def test_schedule_and_branch_bindings_must_jointly_authorize_investment(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    schedule = copy.deepcopy(fixture["projection"]["schedule"])
    schedule["actions"][0]["branch_ids"] = ["unbound-branch"]
    schedule["schedule_digest"] = canonical_digest(
        schedule,
        exclude_keys=("schedule_digest", "created_at", "consumption_log"),
    )
    fixture["projection"]["schedule"] = schedule
    _rewrite_committed_artifact(fixture, "schedule", schedule)
    with pytest.raises(ContractError, match="content-derived commit ID mismatch"):
        _verify(fixture)


def test_filter_refuses_lexical_or_target_wide_guessing(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    authorization = _verify(fixture)
    with pytest.raises(ContractError, match="explicit binding is required"):
        filter_authorized_branches(
            [
                {
                    "branch_id": "near-name-only",
                    "title": fixture["branch_id"],
                    "target_id": fixture["target_id"],
                }
            ],
            authorization,
        )


def test_runtime_marker_and_atomic_reservation_close_forgery_and_reuse(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    authorization = _verify(fixture)
    assert authorization_is_runtime_verified(authorization)
    forged = dict(authorization)
    assert not authorization_is_runtime_verified(forged)
    with pytest.raises(TypeError, match="immutable"):
        authorization["eligible_branch_ids"] = ["branch-forged"]  # type: ignore[index]
    original_eligible_branch_ids = authorization["eligible_branch_ids"]
    detached = authorization_projection(authorization)
    detached["eligible_branch_ids"] = ["branch-forged"]
    assert authorization["eligible_branch_ids"] == original_eligible_branch_ids
    with pytest.raises(
        ContractError,
        match="live runtime-verified authorization|verified active-current",
    ):
        filter_authorized_branches(
            [{"branch_id": fixture["branch_id"]}], forged
        )

    reserved = reserve_canonical_theory_actions(
        authorization,
        branch_ids=[fixture["branch_id"]],
        consumer_receipt_id="consumer.marathon.001",
        consumer_scope="legacy_marathon",
    )
    assert reserved["status"] == "actions_reserved"
    assert reserved["reserved_branch_ids"] == [fixture["branch_id"]]
    assert reserved["committed_state_version"] == 2
    assert reserved["reservation"]["status"] == "reserved_before_investment"
    assert reserved["authorization_basis_digest"] == authorization[
        "authorization_basis_digest"
    ]
    assert reserved["reservation_authorization_basis_digest"]
    assert reserved["reservation"]["temporal_evaluation"]["authentication_status"] == (
        "governed_local_process_time_not_externally_authenticated"
    )
    with pytest.raises(ContractError, match="state changed|compare-and-swap"):
        reserve_canonical_theory_actions(
            authorization,
            branch_ids=[fixture["branch_id"]],
            consumer_receipt_id="consumer.marathon.002",
            consumer_scope="legacy_marathon",
        )


def test_structural_fallback_is_maturation_only_and_cannot_expose_proof(tmp_path: Path) -> None:
    fixture = _canonical_fixture(tmp_path)
    authorization = _verify(fixture)
    authority = authorization["conceptual_authority"]
    assert authority["fallback_disposition"] == "not_applicable"
    assert authority["status"] == "sealed_unique"
    assert authority["internal_correlated_preference"] is True
    assert authority["philosophical_depth_authority"] is None
    assert authority["understanding_gain_authority"] is None
    assert authority["unification_power_authority"] is None
    assert authority["creativity_authority"] is None
    assert authority["relevance_authority"] is None
    assert all(
        "prove" not in kinds and "probe" not in kinds
        for kinds in authorization["action_kinds_by_branch"].values()
    )


def test_bound_conceptual_receipt_controls_verified_internal_authority(
    tmp_path: Path,
) -> None:
    fixture = _canonical_fixture(tmp_path, bound_conceptual_evidence=True)
    generated_decisions = [
        receipt["creative_worth_decision"]
        for receipt in fixture["projection"]["evaluation_receipts"]
    ]
    assert generated_decisions == []

    authorization = _verify(fixture)
    authority = authorization["conceptual_authority"]
    assert authority["status"] == "sealed_unique"
    assert authority["internal_correlated_preference"] is True
    assert authority["synthesis_evidence"] is not None
    assert authority["synthesis_preference_set"]["decision"] == "prefer_unique"
    assert authority["external_depth_validation_status"] == "unavailable"
    assert authority["external_understanding_validation_status"] == "unavailable"
