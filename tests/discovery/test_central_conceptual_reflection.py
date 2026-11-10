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

import copy
import json
import runpy
import shutil
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.central_conceptual_reflection import (
    CentralConceptualReflectionError,
    build_central_conceptual_reflection_commit_binding,
    build_central_conceptual_reflection_intake_claim,
    build_central_conceptual_reflection_request,
    build_central_conceptual_route_reflection_intake,
    consume_committed_central_conceptual_route_reflection_intake,
    decode_central_conceptual_reflection_request,
    decode_central_conceptual_route_reflection_intake,
    recover_central_conceptual_reflection_intake_claim,
    validate_active_prefix_central_conceptual_reflection_request,
    validate_authoritative_central_conceptual_reflection_request,
    validate_central_conceptual_reflection_consumption_receipt,
)
from agentic.discovery.central_conceptual_routes_v3 import (
    ROUTE_ORDER,
    run_central_conceptual_routes,
)
from agentic.discovery.contracts import (
    Namespace,
    artifact_descriptor,
    canonical_digest,
    canonical_json,
    validate_schema_file,
)
from agentic.discovery.receipts import (
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    ValidatorBinding,
    build_operator_request,
)
from agentic.discovery.workflow import (
    DiscoveryWorkflowError,
    build_reflective_discovery_packet,
)
from agentic.state.discovery_transaction import (
    CommitArtifact,
    DiscoveryTransactionStore,
    InjectedFailure,
)
from tests.discovery.test_reflective_conceptual_discovery import major_request


ROOT = Path(__file__).resolve().parents[2]
DESCENDANT_PACKET_PATH = (
    "branches/root/cycles/central-reflection/descendant-packet.json"
)
_CENTRAL_HELPERS = runpy.run_path(
    str(Path(__file__).with_name("test_central_conceptual_routes_v3.py"))
)
_store_with_input = _CENTRAL_HELPERS["_store_with_input"]


def _completed_wave(tmp_path: Path, *, fail_hott: bool = False):
    store, commit, input_path = _store_with_input(tmp_path / "store")
    output_root = tmp_path / "runs"
    faults = None
    if fail_hott:
        faults = {route_id: None for route_id in ROUTE_ORDER}
        faults["hott"] = "exit_nonzero"
    packet = run_central_conceptual_routes(
        store=store,
        verified_commit=commit,
        committed_input_path=input_path,
        output_root=output_root,
        route_fault_modes=faults,
    )
    bundle = output_root / packet["commission_id"]
    request = build_central_conceptual_reflection_request(
        store=store,
        verified_commit=commit,
        packet=packet,
        bundle_root=bundle,
    )
    return store, commit, packet, bundle, request


def _registered_validator() -> ValidatorBinding:
    registry = json.loads(
        (ROOT / "agentic/registries/discovery_operator_registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    operator = next(
        row
        for row in registry["operators"]
        if row["operator_id"] == "reflective-conceptual-discovery"
    )
    validator = operator["validators"][0]
    return ValidatorBinding(
        validator_id=validator["validator_id"],
        version=validator["version"],
        command=tuple(validator["command"]),
        dependency_paths=tuple(
            f"repo://{path}" for path in validator["dependency_paths"]
        ),
        dependency_policy=validator["dependency_policy"],
        timeout_seconds=float(validator["timeout_seconds"]),
    )


def _base_workflow_request(source_request: dict[str, Any]) -> dict[str, Any]:
    request = major_request()
    request["target_id"] = source_request["target_id"]
    request["run_id"] = source_request["run_id"]
    request["branch_id"] = "root"
    request["state_version"] = source_request["cycle_input_head_generation"]
    request["prior_conceptual_state_ref"] = (
        f"state:{source_request['cycle_input_head_generation']}"
    )
    request["literature_basis"]["snapshot_target_id"] = source_request[
        "target_id"
    ]
    return request


def _producer_execution(
    root: Path,
    *,
    store: DiscoveryTransactionStore,
    commit: Any,
    source_packet: dict[str, Any],
    bundle: Path,
    source_request: dict[str, Any],
) -> dict[str, Any]:
    workspace = root / "producer-workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    workflow_request = _base_workflow_request(source_request)
    before_packet = build_reflective_discovery_packet(workflow_request)
    producer_output = copy.deepcopy(before_packet)
    selected = {
        row["route_id"]: row for row in source_request["selected_candidate_set"]
    }
    material_dispositions = ("incorporated", "mutated", "synthesized", "demoted")
    material_index = 0
    directives: list[dict[str, Any]] = []
    for route_index, observation in enumerate(source_request["route_observations"]):
        route_id = observation["route_id"]
        is_negative = (
            observation["terminal_status"] == "failed"
            or observation["output_status"] in {"quarantined", "unavailable"}
        )
        if is_negative:
            disposition = "preserved_negative_knowledge"
            system_ids: list[str] = []
            round_ids: list[str] = []
        elif route_id not in selected:
            disposition = "preserved_unselected_candidate"
            system_ids = []
            round_ids = []
        elif material_index < len(material_dispositions):
            disposition = material_dispositions[material_index]
            system = producer_output["conceptual_systems"][route_index]
            system["mechanism_or_principle"] = (
                f"{system['mechanism_or_principle']} | receipt-derived:{route_id}"
            )
            system_ids = [system["system_id"]]
            round_ids = []
            material_index += 1
        else:
            disposition = "no_change"
            system_ids = [
                producer_output["conceptual_systems"][route_index]["system_id"]
            ]
            round_ids = []
        directives.append(
            {
                "route_id": route_id,
                "descendant_disposition": disposition,
                "referenced_system_ids": system_ids,
                "referenced_round_ids": round_ids,
                "reflection_note": (
                    f"Receipt-bound reflection for {route_id}; no caller path input."
                ),
            }
        )
    producer_output["packet_digest"] = canonical_digest(
        producer_output, exclude_keys=("packet_digest",)
    )
    producer_input = {
        "target_id": source_request["target_id"],
        "run_id": source_request["run_id"],
        "state_version": source_request["cycle_input_head_generation"],
        "discovery_charter": copy.deepcopy(workflow_request["discovery_charter"]),
        "conceptual_genealogy": copy.deepcopy(
            workflow_request["conceptual_genealogy"]
        ),
        "central_conceptual_reflection_request": copy.deepcopy(source_request),
        "central_conceptual_reflection_before": {
            "conceptual_systems": copy.deepcopy(before_packet["conceptual_systems"]),
            "reflection_rounds": copy.deepcopy(before_packet["reflection_rounds"]),
        },
        "central_conceptual_route_directives": directives,
    }
    input_path = workspace / "inputs/central-reflection.json"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_bytes(canonical_json(producer_input) + b"\n")
    namespace = Namespace(
        source_request["target_id"],
        source_request["run_id"],
        "root",
        source_request["cycle_input_head_generation"],
    )
    producer_request = build_operator_request(
        operator_id="reflective-conceptual-discovery",
        operator_version="1.0.0",
        kind="theory",
        namespace=namespace,
        invocation_id="central-reflection-producer-v2",
        input_artifacts=[artifact_descriptor(input_path, workspace, namespace)],
        declared_outputs=["outputs/central-reflection.json"],
        parameters={
            "central_conceptual_reflection_request_id": source_request[
                "request_id"
            ],
            "central_conceptual_reflection_request_digest": source_request[
                "content_digest"
            ],
            "central_descendant_effect_commit_generation": source_request[
                "descendant_effect_commit_generation"
            ],
        },
        required=True,
        requested_at="2026-07-23T00:00:00Z",
    )
    claim = build_central_conceptual_reflection_intake_claim(
        central_request=source_request,
        store=store,
        verified_commit=commit,
        bundle_root=bundle,
        producer_request=producer_request,
        producer_input=producer_input,
    )

    def execute(request: dict[str, Any], runtime_workspace: Path) -> dict[str, Any]:
        output_path = runtime_workspace / request["declared_outputs"][0]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(canonical_json(producer_output) + b"\n")
        return {
            "artifacts": [{"path": request["declared_outputs"][0]}],
            "explicit_unknowns": [
                "Registered reflection output has no independent truth authority."
            ],
        }

    dispatcher = DiscoveryOperatorDispatcher(
        [
            OperatorBinding(
                operator_id="reflective-conceptual-discovery",
                version="1.0.0",
                kind="theory",
                function=execute,
                validators=(_registered_validator(),),
            )
        ],
        workspace=workspace,
        receipt_store=ReceiptStore(workspace / "receipts"),
    )
    producer_receipt = dispatcher.dispatch(producer_request)
    assert producer_receipt["status"] == "succeeded", producer_receipt.get("error")
    output_path = workspace / producer_request["declared_outputs"][0]
    retained_output = json.loads(output_path.read_text(encoding="utf-8"))
    workflow_request.update(
        {
            "generation_mode": "operator_generated",
            "conceptual_systems": copy.deepcopy(
                retained_output["conceptual_systems"]
            ),
            "reflection_rounds": copy.deepcopy(retained_output["reflection_rounds"]),
            "central_conceptual_reflection_request": copy.deepcopy(source_request),
        }
    )
    authority = {
        "store": store,
        "verified_commit": commit,
        "bundle_root": bundle,
        "intake_claim": claim,
        "producer_request": producer_request,
        "producer_receipt": producer_receipt,
        "producer_input": producer_input,
        "producer_output": retained_output,
    }
    descendant_packet = build_reflective_discovery_packet(
        workflow_request, central_reflection_authority=authority
    )
    return {
        "store": store,
        "commit": commit,
        "source_packet": source_packet,
        "bundle": bundle,
        "source_request": source_request,
        "workflow_request": workflow_request,
        "authority": authority,
        "producer_input": producer_input,
        "producer_output": retained_output,
        "descendant_packet": descendant_packet,
    }


def _execution(root: Path, *, fail_hott: bool = False) -> dict[str, Any]:
    store, commit, source_packet, bundle, source_request = _completed_wave(
        root, fail_hott=fail_hott
    )
    return _producer_execution(
        root,
        store=store,
        commit=commit,
        source_packet=source_packet,
        bundle=bundle,
        source_request=source_request,
    )


@pytest.fixture(scope="module")
def central_execution(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    return _execution(tmp_path_factory.mktemp("central-reflection-v2"))


def _commit_descendant(
    execution: dict[str, Any],
    *,
    store: DiscoveryTransactionStore | None = None,
    failpoint: str | None = None,
) -> Any:
    active_store = store or execution["store"]
    source_generation = execution["source_request"]["cycle_input_head_generation"]
    source_commit = active_store.read_verified_commit(source_generation)
    packet = execution["descendant_packet"]
    binding = build_central_conceptual_reflection_commit_binding(
        packet=packet,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
    )
    state = copy.deepcopy(dict(source_commit.state))
    state["generation"] = source_generation + 1
    state["central_conceptual_reflection_consumption"] = binding
    active_store.commit(
        expected_generation=source_generation,
        state=state,
        artifacts=[
            CommitArtifact(
                DESCENDANT_PACKET_PATH,
                canonical_json(packet) + b"\n",
                Namespace(
                    active_store.target_id,
                    active_store.run_id,
                    "root",
                    source_generation,
                ),
            )
        ],
        idempotency_key="central-reflection-descendant-v2",
        request_digest=binding["binding_digest"],
        failpoint=failpoint,
    )
    return active_store.read_verified_commit(source_generation + 1)


def _strip_time(packet: dict[str, Any]) -> dict[str, Any]:
    retained = copy.deepcopy(packet)
    retained.pop("created_utc")
    retained.pop("packet_digest")
    return retained


@pytest.mark.expensive
def test_v2_request_roles_authority_and_history_downgrade(
    central_execution: dict[str, Any],
) -> None:
    request = central_execution["source_request"]
    commit = central_execution["commit"]
    assert validate_schema_file(
        "central_conceptual_route_reflection_request_v2.schema.json"
    )["$id"].endswith("central_conceptual_route_reflection_request_v2.schema.json")
    assert decode_central_conceptual_reflection_request(request) == request
    assert validate_authoritative_central_conceptual_reflection_request(
        request,
        store=central_execution["store"],
        verified_commit=commit,
        bundle_root=central_execution["bundle"],
    ) == request
    assert request["central_source_commit_generation"] == commit.generation
    assert request["cycle_input_head_generation"] == commit.generation
    assert request["descendant_effect_commit_generation"] == commit.generation + 1
    assert request["generation_contract"]["same_generation_effect_authorized"] is False
    assert [row["route_id"] for row in request["route_observations"]] == list(
        ROUTE_ORDER
    )
    assert all(value is False for value in request["current_theory_effect"].values())
    assert request["permitted_descendant_effect"].endswith(
        "committed_only_by_exact_n_plus_one_cas"
    )
    legacy = copy.deepcopy(request)
    legacy["schema_version"] = "1.0.0"
    legacy["content_digest"] = canonical_digest(
        legacy, exclude_keys=("content_digest",)
    )
    with pytest.raises(CentralConceptualReflectionError, match="schema"):
        decode_central_conceptual_reflection_request(legacy)


@pytest.mark.expensive
def test_v2_intake_is_receipt_derived_and_workflow_fails_closed(
    central_execution: dict[str, Any],
) -> None:
    packet = central_execution["descendant_packet"]
    intake = packet["central_conceptual_route_reflection_intake"]
    authority = central_execution["authority"]
    workflow_request = central_execution["workflow_request"]
    assert validate_schema_file(
        "central_conceptual_route_reflection_intake_v2.schema.json"
    )["$id"].endswith("central_conceptual_route_reflection_intake_v2.schema.json")
    assert decode_central_conceptual_route_reflection_intake(
        intake,
        conceptual_systems=packet["conceptual_systems"],
        reflection_rounds=packet["reflection_rounds"],
    ) == intake
    assert build_central_conceptual_route_reflection_intake(
        central_request=central_execution["source_request"],
        intake_claim=authority["intake_claim"],
        producer_request=authority["producer_request"],
        producer_receipt=authority["producer_receipt"],
        producer_input=authority["producer_input"],
        producer_output=authority["producer_output"],
        store=authority["store"],
        verified_commit=authority["verified_commit"],
        bundle_root=authority["bundle_root"],
        target_id=workflow_request["target_id"],
        run_id=workflow_request["run_id"],
        state_version=workflow_request["state_version"],
        conceptual_systems=workflow_request["conceptual_systems"],
        reflection_rounds=workflow_request["reflection_rounds"],
    ) == intake
    assert [row["route_id"] for row in intake["route_accounts"]] == list(ROUTE_ORDER)
    assert all(
        "changed_paths" not in row
        for row in central_execution["producer_input"][
            "central_conceptual_route_directives"
        ]
    )
    patches = intake["computed_patch_set"]["patches"]
    assert intake["computed_patch_set"]["changed_paths"] == [
        row["path"] for row in patches
    ]
    assert intake["computed_patch_set"]["patch_count"] == len(patches) == 4
    assert intake["changed_route_ids"] == list(ROUTE_ORDER[:4])
    assert intake["registered_producer_binding"]["operator_id"] == (
        "reflective-conceptual-discovery"
    )
    assert intake["registered_producer_binding"]["validator_receipt_digests"]
    assert all(value is False for value in intake["direct_authority"].values())
    event = next(
        row
        for row in packet["ledger_events"]
        if row["event_type"] == "central_conceptual_route_reflection_intake"
    )
    assert event["intake_claim_id"] == intake["intake_claim"]["claim_id"]
    assert event["computed_patch_set_digest"] == intake["computed_patch_set"][
        "patch_set_digest"
    ]
    assert event["descendant_effect_commit_generation"] == (
        workflow_request["state_version"] + 1
    )

    legacy_accounts = copy.deepcopy(workflow_request)
    legacy_accounts["central_conceptual_route_accounts"] = None
    with pytest.raises(DiscoveryWorkflowError, match="caller-authored"):
        build_reflective_discovery_packet(
            legacy_accounts, central_reflection_authority=authority
        )
    with pytest.raises(DiscoveryWorkflowError, match="live authority"):
        build_reflective_discovery_packet(workflow_request)
    surplus = {**authority, "portable_substitute": {}}
    with pytest.raises(DiscoveryWorkflowError, match="inexact capability shape"):
        build_reflective_discovery_packet(
            workflow_request, central_reflection_authority=surplus
        )
    wrong_generation = copy.deepcopy(workflow_request)
    wrong_generation["state_version"] += 1
    with pytest.raises(DiscoveryWorkflowError, match="input head N"):
        build_reflective_discovery_packet(
            wrong_generation, central_reflection_authority=authority
        )

    bad_claim = copy.deepcopy(authority["intake_claim"])
    bad_claim["claim_status"] = "forged"
    with pytest.raises(DiscoveryWorkflowError, match="claim|schema"):
        build_reflective_discovery_packet(
            workflow_request,
            central_reflection_authority={**authority, "intake_claim": bad_claim},
        )
    bad_receipt = copy.deepcopy(authority["producer_receipt"])
    bad_receipt["receipt_digest"] = canonical_digest("forged receipt")
    with pytest.raises(DiscoveryWorkflowError, match="receipt"):
        build_reflective_discovery_packet(
            workflow_request,
            central_reflection_authority={
                **authority,
                "producer_receipt": bad_receipt,
            },
        )
    bad_output = copy.deepcopy(authority["producer_output"])
    bad_output["conceptual_systems"][0]["mechanism_or_principle"] += " forged"
    bad_output["packet_digest"] = canonical_digest(
        bad_output, exclude_keys=("packet_digest",)
    )
    with pytest.raises(DiscoveryWorkflowError, match="receipt|output"):
        build_reflective_discovery_packet(
            workflow_request,
            central_reflection_authority={**authority, "producer_output": bad_output},
        )

    legacy_intake = copy.deepcopy(intake)
    legacy_intake["schema_version"] = "1.0.0"
    legacy_intake["content_digest"] = canonical_digest(
        legacy_intake, exclude_keys=("content_digest",)
    )
    with pytest.raises(CentralConceptualReflectionError, match="schema"):
        decode_central_conceptual_route_reflection_intake(
            legacy_intake,
            conceptual_systems=packet["conceptual_systems"],
            reflection_rounds=packet["reflection_rounds"],
        )


@pytest.mark.expensive
def test_failed_route_is_preserved_only_as_negative_knowledge(tmp_path: Path) -> None:
    execution = _execution(tmp_path / "failed-route", fail_hott=True)
    intake = execution["descendant_packet"][
        "central_conceptual_route_reflection_intake"
    ]
    assert execution["source_request"]["selected_candidate_set"] == []
    assert intake["negative_knowledge_route_ids"] == ["hott"]
    assert intake["changed_route_ids"] == []
    assert intake["computed_patch_set"]["patch_count"] == 0
    by_route = {row["route_id"]: row for row in intake["route_accounts"]}
    assert by_route["hott"]["causal_directive"]["descendant_disposition"] == (
        "preserved_negative_knowledge"
    )
    assert by_route["hott"]["source_candidate_projection"] is None
    assert all(
        not row["computed_patches"] for row in intake["route_accounts"]
    )


@pytest.mark.expensive
def test_claim_commit_consumption_recovery_fork_crash_and_relocation(
    tmp_path: Path,
) -> None:
    execution = _execution(tmp_path / "canonical")
    source_request = execution["source_request"]
    authority = execution["authority"]
    source_generation = source_request["cycle_input_head_generation"]

    duplicate_claim = build_central_conceptual_reflection_intake_claim(
        central_request=source_request,
        store=execution["store"],
        verified_commit=execution["commit"],
        bundle_root=execution["bundle"],
        producer_request=authority["producer_request"],
        producer_input=authority["producer_input"],
    )
    assert duplicate_claim == authority["intake_claim"]
    pending = recover_central_conceptual_reflection_intake_claim(
        central_request=source_request,
        store=execution["store"],
        verified_commit=execution["commit"],
        bundle_root=execution["bundle"],
        producer_request=authority["producer_request"],
        producer_input=authority["producer_input"],
    )
    assert pending["recovery_disposition"] == (
        "pending_exact_n_plus_one_compare_and_swap"
    )

    crash_root = tmp_path / "crash-store"
    fork_root = tmp_path / "fork-store"
    shutil.copytree(execution["store"].root, crash_root)
    shutil.copytree(execution["store"].root, fork_root)
    crash_bundle = tmp_path / "crash-bundle"
    fork_bundle = tmp_path / "fork-bundle"
    shutil.copytree(execution["bundle"], crash_bundle)
    shutil.copytree(execution["bundle"], fork_bundle)

    descendant_commit = _commit_descendant(execution)
    assert validate_active_prefix_central_conceptual_reflection_request(
        source_request,
        store=execution["store"],
        verified_commit=execution["commit"],
        bundle_root=execution["bundle"],
    ) == source_request
    with pytest.raises(CentralConceptualReflectionError, match="current|head"):
        validate_authoritative_central_conceptual_reflection_request(
            source_request,
            store=execution["store"],
            verified_commit=execution["commit"],
            bundle_root=execution["bundle"],
        )
    recovered = recover_central_conceptual_reflection_intake_claim(
        central_request=source_request,
        store=execution["store"],
        verified_commit=execution["commit"],
        bundle_root=execution["bundle"],
        producer_request=authority["producer_request"],
        producer_input=authority["producer_input"],
    )
    assert recovered["recovery_disposition"] == (
        "matching_n_plus_one_commit_available_for_exact_replay"
    )
    receipt = consume_committed_central_conceptual_route_reflection_intake(
        store=execution["store"],
        descendant_verified_commit=descendant_commit,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    )
    assert consume_committed_central_conceptual_route_reflection_intake(
        store=execution["store"],
        descendant_verified_commit=descendant_commit,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    ) == receipt
    assert validate_central_conceptual_reflection_consumption_receipt(
        receipt,
        store=execution["store"],
        descendant_verified_commit=descendant_commit,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    ) == receipt
    forged_receipt = copy.deepcopy(receipt)
    forged_receipt["consumption_status"] = "forged"
    with pytest.raises(CentralConceptualReflectionError, match="differs"):
        validate_central_conceptual_reflection_consumption_receipt(
            forged_receipt,
            store=execution["store"],
            descendant_verified_commit=descendant_commit,
            packet_artifact_path=DESCENDANT_PACKET_PATH,
            bundle_root=execution["bundle"],
        )

    next_state = copy.deepcopy(dict(descendant_commit.state))
    next_state["generation"] = source_generation + 2
    execution["store"].commit(
        expected_generation=source_generation + 1,
        state=next_state,
        artifacts=(),
        idempotency_key="post-consumption-head-advance",
        request_digest=canonical_digest("post-consumption-head-advance"),
    )
    assert consume_committed_central_conceptual_route_reflection_intake(
        store=execution["store"],
        descendant_verified_commit=descendant_commit,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    ) == receipt
    assert _commit_descendant(execution).generation == source_generation + 1

    relocated_root = tmp_path / "relocated-store"
    relocated_bundle = tmp_path / "relocated-bundle"
    shutil.copytree(execution["store"].root, relocated_root)
    shutil.copytree(execution["bundle"], relocated_bundle)
    relocated_store = DiscoveryTransactionStore(
        relocated_root,
        target_id=execution["store"].target_id,
        run_id=execution["store"].run_id,
    )
    relocated_descendant = relocated_store.read_verified_commit(
        source_generation + 1
    )
    assert consume_committed_central_conceptual_route_reflection_intake(
        store=relocated_store,
        descendant_verified_commit=relocated_descendant,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    ) == receipt
    with pytest.raises(CentralConceptualReflectionError, match="receipt path mismatch"):
        consume_committed_central_conceptual_route_reflection_intake(
            store=relocated_store,
            descendant_verified_commit=relocated_descendant,
            packet_artifact_path=DESCENDANT_PACKET_PATH,
            bundle_root=relocated_bundle,
        )

    crash_store = DiscoveryTransactionStore(
        crash_root,
        target_id=execution["store"].target_id,
        run_id=execution["store"].run_id,
    )
    with pytest.raises(InjectedFailure, match="after_commit_rename"):
        _commit_descendant(
            execution, store=crash_store, failpoint="after_commit_rename"
        )
    reopened_crash_store = DiscoveryTransactionStore(
        crash_root,
        target_id=execution["store"].target_id,
        run_id=execution["store"].run_id,
    )
    assert reopened_crash_store.recover() == source_generation + 1
    crash_descendant = reopened_crash_store.read_verified_commit(
        source_generation + 1
    )
    crash_receipt = consume_committed_central_conceptual_route_reflection_intake(
        store=reopened_crash_store,
        descendant_verified_commit=crash_descendant,
        packet_artifact_path=DESCENDANT_PACKET_PATH,
        bundle_root=execution["bundle"],
    )
    assert crash_receipt["intake_digest"] == receipt["intake_digest"]

    fork_store = DiscoveryTransactionStore(
        fork_root,
        target_id=execution["store"].target_id,
        run_id=execution["store"].run_id,
    )
    fork_source = fork_store.read_verified_commit(source_generation)
    fork_state = copy.deepcopy(dict(fork_source.state))
    fork_state["generation"] = source_generation + 1
    fork_store.commit(
        expected_generation=source_generation,
        state=fork_state,
        artifacts=(),
        idempotency_key="foreign-descendant-winner",
        request_digest=canonical_digest("foreign-descendant-winner"),
    )
    loser = recover_central_conceptual_reflection_intake_claim(
        central_request=source_request,
        store=fork_store,
        verified_commit=fork_source,
        bundle_root=execution["bundle"],
        producer_request=authority["producer_request"],
        producer_input=authority["producer_input"],
    )
    assert loser["recovery_disposition"] == (
        "superseded_by_other_n_plus_one_commit"
    )


def test_no_central_request_stays_compatible_but_legacy_account_port_is_closed() -> None:
    request = major_request()
    baseline = build_reflective_discovery_packet(request)
    explicit_none = copy.deepcopy(request)
    explicit_none["central_conceptual_reflection_request"] = None
    assert _strip_time(build_reflective_discovery_packet(explicit_none)) == _strip_time(
        baseline
    )
    authority_without_request = {key: None for key in (
        "store",
        "verified_commit",
        "bundle_root",
        "intake_claim",
        "producer_request",
        "producer_receipt",
        "producer_input",
        "producer_output",
    )}
    with pytest.raises(DiscoveryWorkflowError, match="exact live authority"):
        build_reflective_discovery_packet(
            request, central_reflection_authority=authority_without_request
        )
    legacy = copy.deepcopy(request)
    legacy["central_conceptual_route_accounts"] = None
    with pytest.raises(DiscoveryWorkflowError, match="caller-authored"):
        build_reflective_discovery_packet(legacy)
