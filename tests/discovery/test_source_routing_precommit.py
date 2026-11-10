# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Causal and adversarial tests for two-phase source-routing authority.

The authoritative phase is a policy sealed after acquisition but before any
warrant, mapping, or assimilation work.  A distinct realization then proves
that the three completed outputs consumed it in order.  The former
post-assimilation ``precommit`` remains only as typed compatibility.  These
tests keep source-state closure, algorithm/config authority, negative-evidence
discipline, replay, and temporal ordering independently executable while the
larger canonical-cycle migration proceeds.
"""

from __future__ import annotations

import copy
from datetime import datetime, timedelta
from typing import Any

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.cycle import validate_source_authority_pair_execution
from agentic.discovery.literature import (
    assimilate_literature,
    bind_source_semantic_warrants,
    run_frontier_literature_cycle,
)
from agentic.discovery.literature_acquisition import (
    LiteratureAcquisitionError,
    build_source_routing_pre_map_policy,
    build_source_routing_precommit_certificate,
    build_source_routing_realization,
    build_source_routing_warrant_validation_packet,
    derive_source_routing_semantic_warrants,
    source_routing_realization_requirements,
    top_level_content_digest,
    validate_source_routing_pre_map_policy,
    validate_source_routing_precommit_certificate,
    validate_source_routing_realization,
    validate_source_routing_warrant_validation_packet,
)
from tests.discovery.test_canonical_discovery_cycle import _live_providers, _mappings, _search_request


TARGET_ID = "target-source-routing-precommit"
RUN_ID = "run-source-routing-precommit"
STATE_VERSION = 0
ASSIMILATION_COMPLETED_AT = "2026-07-22T10:00:00Z"


def _routing_fixture() -> dict[str, Any]:
    """Build one live-provider snapshot and its exact assimilation ancestor."""

    theory_digest = canonical_digest({"theory_state": "routing-state-0"})
    snapshot = run_frontier_literature_cycle(
        _search_request(TARGET_ID, theory_digest),
        providers=_live_providers(TARGET_ID),
    )
    assimilation = assimilate_literature(
        snapshot,
        theory_state_digest=theory_digest,
        theory_mappings=_mappings(snapshot),
    )
    source_ids = sorted(row["source_id"] for row in snapshot["sources"])
    authority = {
        "capture_content_digest": canonical_digest(
            {
                "target_id": TARGET_ID,
                "snapshot_id": snapshot["snapshot_id"],
                "lane_receipts": snapshot["lane_receipts"],
            }
        ),
        "acquisition_content_digest": snapshot["content_digest"],
        "tool_response_content_digests": sorted(
            row["content_digest"] for row in snapshot["lane_receipts"]
        ),
        "version_graph_content_digests": [],
        "source_ids": source_ids,
        "source_routing_eligibility": {
            source_id: "unverified_audit_only" for source_id in source_ids
        },
        "authority_boundary": (
            "fixture-provider observations and exact snapshot validators; "
            "no provider authentication, source truth, novelty, or exhaustiveness"
        ),
    }
    receipt = {
        "status": "succeeded",
        "receipt_id": "receipt-assimilation-routing-001",
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": STATE_VERSION,
        },
        "completed_at": ASSIMILATION_COMPLETED_AT,
    }
    return {
        "snapshot": snapshot,
        "assimilation": assimilation,
        "authority": authority,
        "receipt": receipt,
    }


def _build(fixture: dict[str, Any], *, precommitted_at: str | None = None) -> dict[str, Any]:
    return build_source_routing_precommit_certificate(
        authority=fixture["authority"],
        snapshot=fixture["snapshot"],
        assimilation=fixture["assimilation"],
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        assimilation_producer_receipt=fixture["receipt"],
        precommitted_at=precommitted_at,
    )


def _algorithm_contracts() -> list[dict[str, Any]]:
    """Represent the registry authority that must exist before outputs do."""

    return [
        {
            "stage": stage,
            "component_id": f"source-routing-{stage}.v1",
            "algorithm_id": f"bounded-{stage}-algorithm.v1",
            "config_id": f"source-routing-{stage}-config.v1",
            "config_digest": canonical_digest(
                {"stage": stage, "policy": "fixture-approved-exact-config-v1"}
            ),
            "authority_class": "approved_internal_algorithm_registry",
        }
        for stage in ("warrant_validation", "claim_mapping", "assimilation")
    ]


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _two_phase_fixture() -> dict[str, Any]:
    """Build one complete policy -> three receipts -> realization chain."""

    fixture = _routing_fixture()
    snapshot = fixture["snapshot"]
    acquisition_receipt = {
        "receipt_id": "receipt-validated-acquisition-routing-001",
        "status": "succeeded",
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": STATE_VERSION,
        },
        "completed_at": snapshot["search_completed_at"],
    }
    algorithms = _algorithm_contracts()
    policy = build_source_routing_pre_map_policy(
        authority=fixture["authority"],
        snapshot=snapshot,
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        acquisition_producer_receipt=acquisition_receipt,
        algorithm_contracts=algorithms,
        freshness_max_age_seconds=86_400,
    )
    validated_warrants: list[dict[str, Any]] = []
    claim_mappings = copy.deepcopy(fixture["assimilation"]["theory_mappings"])
    requirements = source_routing_realization_requirements(
        policy=policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=fixture["assimilation"],
    )
    seal_time = datetime.fromisoformat(policy["sealed_at"].replace("Z", "+00:00"))
    stage_receipts = []
    for index, requirement in enumerate(requirements):
        started = seal_time + timedelta(seconds=2 * index + 1)
        completed = started + timedelta(seconds=1)
        stage_receipts.append(
            {
                "receipt_id": f"receipt-{requirement['stage']}-routing-001",
                "stage": requirement["stage"],
                "status": "succeeded",
                "identity": {
                    "target_id": TARGET_ID,
                    "run_id": RUN_ID,
                    "state_version": STATE_VERSION,
                },
                "pre_map_policy_id": policy["policy_id"],
                "pre_map_policy_digest": policy["policy_digest"],
                "algorithm_contract_digest": requirement[
                    "algorithm_contract_digest"
                ],
                "started_at": _iso(started),
                "completed_at": _iso(completed),
                "input_digest": requirement["input_digest"],
                "output_digest": requirement["output_digest"],
            }
        )
    realization = build_source_routing_realization(
        policy=policy,
        authority=fixture["authority"],
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_receipt,
        algorithm_contracts=algorithms,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=fixture["assimilation"],
        stage_receipts=stage_receipts,
    )
    return {
        **fixture,
        "acquisition_receipt": acquisition_receipt,
        "algorithms": algorithms,
        "policy": policy,
        "validated_warrants": validated_warrants,
        "claim_mappings": claim_mappings,
        "requirements": requirements,
        "stage_receipts": stage_receipts,
        "realization": realization,
    }


def _execution_inputs(
    bundle: dict[str, Any],
    *,
    downstream_started_at: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Represent the two causal phases at every exact consumer boundary.

    Assimilation sees only the already sealed policy.  Every later operator
    sees the policy-realization pair, and the adjudicator appears twice because
    parent and synthesis preference are separate authoritative decisions.
    """

    policy = bundle["policy"]
    realization = bundle["realization"]
    operator_ids = list(
        realization["downstream_consumption_contract"]["required_operator_ids"]
    )
    adjudicator = "blind-conceptual-preference-adjudicator"
    operator_ids.insert(operator_ids.index(adjudicator) + 1, adjudicator)
    requests: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    inputs: dict[str, list[dict[str, Any]]] = {}
    assimilation_request_id = "request-assimilation-routing-001"
    requests.append(
        {
            "request_id": assimilation_request_id,
            "operator": {"operator_id": "frontier-literature-assimilator"},
        }
    )
    receipts.append(
        {
            **copy.deepcopy(bundle["receipt"]),
            "request_id": assimilation_request_id,
            "started_at": bundle["stage_receipts"][2]["started_at"],
        }
    )
    inputs[assimilation_request_id] = [
        {"source_routing_pre_map_policy": copy.deepcopy(policy)}
    ]
    if downstream_started_at is None:
        completed = datetime.fromisoformat(
            realization["completed_at"].replace("Z", "+00:00")
        )
        downstream_started_at = _iso(completed + timedelta(seconds=1))
    for index, operator_id in enumerate(operator_ids):
        request_id = f"request-routing-consumer-{index:02d}"
        requests.append(
            {"request_id": request_id, "operator": {"operator_id": operator_id}}
        )
        receipts.append(
            {
                "request_id": request_id,
                "status": "succeeded",
                "started_at": downstream_started_at,
            }
        )
        inputs[request_id] = [
            {
                "source_routing_pre_map_policy": copy.deepcopy(policy),
                "source_routing_realization": copy.deepcopy(realization),
            }
        ]
    return requests, receipts, inputs


def _validate_authority_pair_execution(
    bundle: dict[str, Any],
    *,
    requests: list[dict[str, Any]],
    receipts: list[dict[str, Any]],
    inputs: dict[str, list[dict[str, Any]]],
    require_artifact_producers: bool = False,
) -> dict[str, Any] | None:
    return validate_source_authority_pair_execution(
        active_required=True,
        payloads={
            "literature_snapshot": [bundle["snapshot"]],
            "literature_assimilation": [bundle["assimilation"]],
            "source_routing_pre_map_policy": [bundle["policy"]],
            "source_routing_realization": [bundle["realization"]],
        },
        producers_by_role={"literature_assimilation": [bundle["receipt"]]},
        operator_requests=requests,
        operator_receipts=receipts,
        input_payloads=inputs,
        require_artifact_producers=require_artifact_producers,
    )


def test_precommit_seals_exact_authority_and_all_seven_routing_stages() -> None:
    fixture = _routing_fixture()
    certificate = _build(fixture)
    assert validate_source_routing_precommit_certificate(
        certificate,
        snapshot=fixture["snapshot"],
        assimilation=fixture["assimilation"],
    ) == certificate
    assert [row["stage"] for row in certificate["stage_precommitments"]] == [
        "claim_mapping",
        "warrant_validation",
        "assimilation",
        "high_risk_investment",
        "parallel_scheduling",
        "canonical_commit",
        "theory_gate_acceptance",
    ]
    assert "blind-conceptual-preference-adjudicator" in certificate[
        "downstream_consumption_contract"
    ]["required_operator_ids"]
    assert all(
        row["routing_certificate"]["require_complete_mapping"]
        for row in certificate["stage_precommitments"]
    )


@pytest.mark.parametrize("drift", ["omit", "extra"])
def test_precommit_rejects_source_set_omission_or_substitution(drift: str) -> None:
    fixture = _routing_fixture()
    if drift == "omit":
        source_id = fixture["authority"]["source_ids"].pop()
        fixture["authority"]["source_routing_eligibility"].pop(source_id)
    else:
        fixture["authority"]["source_ids"].append("substituted-source")
        fixture["authority"]["source_routing_eligibility"][
            "substituted-source"
        ] = "unverified_audit_only"
    with pytest.raises(LiteratureAcquisitionError) as caught:
        _build(fixture)
    assert caught.value.reason_code == "source_routing_precommit_source_set_mismatch"


def test_precommit_rejects_negative_only_source_used_for_reframing_support() -> None:
    fixture = _routing_fixture()
    first_source = fixture["authority"]["source_ids"][0]
    fixture["authority"]["source_routing_eligibility"][first_source] = (
        "negative_evidence_only"
    )
    with pytest.raises(LiteratureAcquisitionError) as caught:
        _build(fixture)
    assert caught.value.reason_code == "source_routing_negative_only_violation"


def test_precommit_rejects_assimilation_receipt_target_run_or_state_drift() -> None:
    fixture = _routing_fixture()
    fixture["receipt"]["identity"]["state_version"] = 1
    with pytest.raises(LiteratureAcquisitionError) as caught:
        _build(fixture)
    assert caught.value.reason_code == "source_routing_precommit_receipt_identity_mismatch"


def test_validator_rejects_rehashed_eligibility_or_stage_mutation() -> None:
    fixture = _routing_fixture()
    certificate = _build(fixture)
    certificate["acquisition_authority"]["source_routing_eligibility"][
        fixture["authority"]["source_ids"][0]
    ] = "blocked_positive_support"
    certificate["stage_precommitments"][0]["binding_digest"] = "sha256:" + "f" * 64
    certificate["certificate_digest"] = top_level_content_digest(
        certificate, "certificate_digest"
    )
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_precommit_certificate(
            certificate,
            snapshot=fixture["snapshot"],
            assimilation=fixture["assimilation"],
        )
    assert caught.value.reason_code == "source_routing_precommit_replay_mismatch"


def test_execution_rejects_omitted_or_substituted_downstream_authority() -> None:
    bundle = _two_phase_fixture()
    requests, receipts, inputs = _execution_inputs(bundle)
    consumer_request_id = requests[1]["request_id"]
    inputs[consumer_request_id][0].pop("source_routing_realization")
    with pytest.raises(ContractError, match="exact policy-realization pair"):
        _validate_authority_pair_execution(
            bundle,
            requests=requests,
            receipts=receipts,
            inputs=inputs,
        )
    inputs[consumer_request_id][0]["source_routing_realization"] = copy.deepcopy(
        bundle["realization"]
    )
    inputs[consumer_request_id][0]["source_routing_pre_map_policy"] = {
        **copy.deepcopy(bundle["policy"]),
        "policy_id": "source-routing-pre-map-policy.substitution",
    }
    with pytest.raises(ContractError, match="exact policy-realization pair"):
        _validate_authority_pair_execution(
            bundle,
            requests=requests,
            receipts=receipts,
            inputs=inputs,
        )


def test_execution_rejects_realization_created_after_downstream_dispatch() -> None:
    bundle = _two_phase_fixture()
    completed = datetime.fromisoformat(
        bundle["realization"]["completed_at"].replace("Z", "+00:00")
    )
    requests, receipts, inputs = _execution_inputs(
        bundle,
        downstream_started_at=_iso(completed - timedelta(seconds=1)),
    )
    with pytest.raises(ContractError, match="realization was created after .* dispatch"):
        _validate_authority_pair_execution(
            bundle,
            requests=requests,
            receipts=receipts,
            inputs=inputs,
        )


def test_execution_accepts_one_exact_two_phase_authority_for_every_consumer() -> None:
    bundle = _two_phase_fixture()
    requests, receipts, inputs = _execution_inputs(bundle)
    assert _validate_authority_pair_execution(
        bundle,
        requests=requests,
        receipts=receipts,
        inputs=inputs,
    ) == {
        "pre_map_policy": bundle["policy"],
        "realization": bundle["realization"],
    }


def test_execution_rejects_unproduced_authority_when_producers_are_required() -> None:
    bundle = _two_phase_fixture()
    requests, receipts, inputs = _execution_inputs(bundle)
    with pytest.raises(
        ContractError,
        match=(
            "active source authority role source_routing_pre_map_policy "
            "requires exactly one successful producer"
        ),
    ):
        _validate_authority_pair_execution(
            bundle,
            requests=requests,
            receipts=receipts,
            inputs=inputs,
            require_artifact_producers=True,
        )


def test_local_cycle_rejects_any_smuggled_routing_authority() -> None:
    bundle = _two_phase_fixture()
    with pytest.raises(ContractError, match="non-active operator envelope smuggles"):
        validate_source_authority_pair_execution(
            active_required=False,
            payloads={
                "source_routing_pre_map_policy": [],
                "source_routing_realization": [],
            },
            producers_by_role={},
            operator_requests=[],
            operator_receipts=[],
            input_payloads={
                "request-local": [
                    {
                        "source_routing_pre_map_policy": bundle["policy"],
                        "source_routing_realization": bundle["realization"],
                    }
                ]
            },
        )


def _rebuild_realization(
    bundle: dict[str, Any],
    *,
    stage_receipts: list[dict[str, Any]] | None = None,
    claim_mappings: list[dict[str, Any]] | None = None,
    completed_at: str | None = None,
) -> dict[str, Any]:
    return build_source_routing_realization(
        policy=bundle["policy"],
        authority=bundle["authority"],
        snapshot=bundle["snapshot"],
        acquisition_producer_receipt=bundle["acquisition_receipt"],
        algorithm_contracts=bundle["algorithms"],
        validated_warrants=bundle["validated_warrants"],
        claim_mappings=(
            bundle["claim_mappings"]
            if claim_mappings is None
            else claim_mappings
        ),
        assimilation=bundle["assimilation"],
        stage_receipts=(
            bundle["stage_receipts"]
            if stage_receipts is None
            else stage_receipts
        ),
        completed_at=completed_at,
    )


def test_two_phase_policy_precedes_mapping_and_realization_reopens_exactly() -> None:
    bundle = _two_phase_fixture()
    policy = bundle["policy"]
    realization = bundle["realization"]
    assert derive_source_routing_semantic_warrants(bundle["snapshot"]) == bundle[
        "validated_warrants"
    ]
    assert validate_source_routing_pre_map_policy(
        policy,
        authority=bundle["authority"],
        snapshot=bundle["snapshot"],
        acquisition_producer_receipt=bundle["acquisition_receipt"],
        algorithm_contracts=bundle["algorithms"],
    ) == policy
    assert [row["stage"] for row in policy["algorithm_contracts"]] == [
        "warrant_validation",
        "claim_mapping",
        "assimilation",
    ]
    assert policy["source_state"]["ordered_source_ids"] == bundle["authority"][
        "source_ids"
    ]
    assert all(
        row["positive_support_authorized"] is False
        and row["automatic_investment_authorized"] is False
        for row in policy["effect_permissions"]
    )
    assert validate_source_routing_realization(
        realization,
        policy=policy,
        authority=bundle["authority"],
        snapshot=bundle["snapshot"],
        acquisition_producer_receipt=bundle["acquisition_receipt"],
        algorithm_contracts=bundle["algorithms"],
        validated_warrants=bundle["validated_warrants"],
        claim_mappings=bundle["claim_mappings"],
        assimilation=bundle["assimilation"],
        stage_receipts=bundle["stage_receipts"],
    ) == realization
    assert [row["stage"] for row in realization["stage_receipts"]] == [
        "warrant_validation",
        "claim_mapping",
        "assimilation",
    ]
    assert [
        row["stage"] for row in realization["post_assimilation_authorizations"]
    ] == [
        "high_risk_investment",
        "parallel_scheduling",
        "canonical_commit",
        "theory_gate_acceptance",
    ]


def test_public_warrant_replay_rejects_a_rehashed_unvalidated_snapshot() -> None:
    """The public convenience API must retain snapshot authority, not shape only."""

    bundle = _two_phase_fixture()
    snapshot = copy.deepcopy(bundle["snapshot"])
    snapshot["sources"][0]["semantic_warrants"] = [
        {
            "source_id": snapshot["sources"][0]["source_id"],
            "relation": "supports",
            "claim": "self-authored warrant outside the sealed snapshot",
        }
    ]
    with pytest.raises(ContractError):
        derive_source_routing_semantic_warrants(snapshot)


def test_public_warrant_replay_projects_valid_enclosing_source_identity() -> None:
    bundle = _two_phase_fixture()
    snapshot = bundle["snapshot"]
    source = snapshot["sources"][0]
    enriched = bind_source_semantic_warrants(
        snapshot,
        [
            {
                "source_id": source["source_id"],
                "exact_claim": source["claims"][0],
                "theory_object_ids": ["theory-object-routing-boundary"],
                "relation": "leaves_open",
                "warrant_text": (
                    "The source leaves the target-specific transfer obligation open."
                ),
                "evidence_locator": "fixture source claim 1",
            }
        ],
        authority_id="source-routing-warrant-audit.v1",
    )

    projected = derive_source_routing_semantic_warrants(enriched)

    assert len(projected) == 1
    assert projected[0]["source_id"] == source["source_id"]
    assert "source_id" not in enriched["sources"][0]["semantic_warrants"][0]
    assert projected[0]["warrant_id"] == enriched["sources"][0][
        "semantic_warrants"
    ][0]["warrant_id"]


def test_warrant_validation_packet_seals_explicit_and_missing_coverage() -> None:
    fixture = _routing_fixture()
    snapshot = fixture["snapshot"]
    source = snapshot["sources"][0]
    enriched = bind_source_semantic_warrants(
        snapshot,
        [
            {
                "source_id": source["source_id"],
                "exact_claim": source["claims"][0],
                "theory_object_ids": ["theory-object-routing-boundary"],
                "relation": "leaves_open",
                "warrant_text": (
                    "The exact source claim leaves the protected transfer open."
                ),
                "evidence_locator": "fixture source claim 1",
            }
        ],
        authority_id="source-routing-warrant-audit.v1",
    )
    authority = copy.deepcopy(fixture["authority"])
    authority["acquisition_content_digest"] = enriched["content_digest"]
    acquisition_receipt = {
        "receipt_id": "receipt-validated-warrant-acquisition-001",
        "status": "succeeded",
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": STATE_VERSION,
        },
        "completed_at": enriched["search_completed_at"],
    }
    policy = build_source_routing_pre_map_policy(
        authority=authority,
        snapshot=enriched,
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        acquisition_producer_receipt=acquisition_receipt,
        algorithm_contracts=_algorithm_contracts(),
        freshness_max_age_seconds=86_400,
    )

    packet = build_source_routing_warrant_validation_packet(
        policy=policy,
        snapshot=enriched,
    )

    assert validate_source_routing_warrant_validation_packet(
        packet,
        policy=policy,
        snapshot=enriched,
    ) == packet
    assert packet["explicit_warrant_source_ids"] == [source["source_id"]]
    assert packet["sources_without_explicit_warrants"] == sorted(
        set(packet["ordered_source_ids"]) - {source["source_id"]}
    )
    assert packet["validated_warrants"][0]["source_id"] == source["source_id"]
    assert packet["routing_certificate"]["checked_rows"][0][
        "row_kind"
    ] == "semantic_warrant"
    assert packet["semantic_output_digest"] == canonical_digest(
        packet["validated_warrants"]
    )


def test_warrant_validation_packet_exact_rebuild_rejects_rehashed_coverage() -> None:
    bundle = _two_phase_fixture()
    packet = build_source_routing_warrant_validation_packet(
        policy=bundle["policy"],
        snapshot=bundle["snapshot"],
    )
    assert packet["validated_warrants"] == []
    assert packet["explicit_warrant_source_ids"] == []
    assert packet["sources_without_explicit_warrants"] == packet[
        "ordered_source_ids"
    ]

    forged = copy.deepcopy(packet)
    forged["sources_without_explicit_warrants"] = forged[
        "sources_without_explicit_warrants"
    ][:-1]
    forged["packet_digest"] = canonical_digest(
        forged, exclude_keys=("packet_digest",)
    )
    with pytest.raises(
        LiteratureAcquisitionError,
        match="differs from deterministic replay",
    ):
        validate_source_routing_warrant_validation_packet(
            forged,
            policy=bundle["policy"],
            snapshot=bundle["snapshot"],
        )


@pytest.mark.parametrize("drift", ["omit", "substitute"])
def test_pre_map_policy_rejects_acquired_source_omission_or_substitution(
    drift: str,
) -> None:
    fixture = _routing_fixture()
    receipt = {
        "receipt_id": "receipt-validated-acquisition-routing-002",
        "status": "succeeded",
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": STATE_VERSION,
        },
        "completed_at": fixture["snapshot"]["search_completed_at"],
    }
    if drift == "omit":
        source_id = fixture["authority"]["source_ids"].pop()
        fixture["authority"]["source_routing_eligibility"].pop(source_id)
    else:
        source_id = fixture["authority"]["source_ids"].pop()
        fixture["authority"]["source_routing_eligibility"].pop(source_id)
        fixture["authority"]["source_ids"].append("source-substitution")
        fixture["authority"]["source_routing_eligibility"][
            "source-substitution"
        ] = "unverified_audit_only"
    with pytest.raises(LiteratureAcquisitionError) as caught:
        build_source_routing_pre_map_policy(
            authority=fixture["authority"],
            snapshot=fixture["snapshot"],
            target_id=TARGET_ID,
            run_id=RUN_ID,
            state_version=STATE_VERSION,
            acquisition_producer_receipt=receipt,
            algorithm_contracts=_algorithm_contracts(),
        )
    assert caught.value.reason_code == "source_routing_pre_map_source_set_mismatch"


def test_pre_map_policy_rejects_stale_seal_after_freshness_boundary() -> None:
    fixture = _routing_fixture()
    completion = datetime.fromisoformat(
        fixture["snapshot"]["search_completed_at"].replace("Z", "+00:00")
    )
    receipt = {
        "receipt_id": "receipt-validated-acquisition-routing-003",
        "status": "succeeded",
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "state_version": STATE_VERSION,
        },
        "completed_at": _iso(completion),
    }
    with pytest.raises(LiteratureAcquisitionError) as caught:
        build_source_routing_pre_map_policy(
            authority=fixture["authority"],
            snapshot=fixture["snapshot"],
            target_id=TARGET_ID,
            run_id=RUN_ID,
            state_version=STATE_VERSION,
            acquisition_producer_receipt=receipt,
            algorithm_contracts=_algorithm_contracts(),
            sealed_at=_iso(completion + timedelta(seconds=2)),
            freshness_max_age_seconds=1,
        )
    assert caught.value.reason_code == "source_routing_pre_map_stale"


@pytest.mark.parametrize("attack", ["source_version", "algorithm_config"])
def test_pre_map_validator_rejects_fully_rehashed_internal_authority_attack(
    attack: str,
) -> None:
    bundle = _two_phase_fixture()
    policy = copy.deepcopy(bundle["policy"])
    if attack == "source_version":
        record = policy["source_state"]["records"][0]
        record["source_version"] = "attacker-version"
        record["record_digest"] = canonical_digest(
            {key: value for key, value in record.items() if key != "record_digest"}
        )
        state = policy["source_state"]
        state["source_state_digest"] = canonical_digest(
            {
                key: value
                for key, value in state.items()
                if key != "source_state_digest"
            }
        )
    else:
        contract = policy["algorithm_contracts"][1]
        contract["config_digest"] = canonical_digest({"attacker": "config"})
        contract["contract_digest"] = canonical_digest(
            {
                key: value
                for key, value in contract.items()
                if key != "contract_digest"
            }
        )
    policy["policy_digest"] = top_level_content_digest(policy, "policy_digest")
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_pre_map_policy(
            policy,
            authority=bundle["authority"],
            snapshot=bundle["snapshot"],
            acquisition_producer_receipt=bundle["acquisition_receipt"],
            algorithm_contracts=bundle["algorithms"],
        )
    assert caught.value.reason_code == "source_routing_pre_map_replay_mismatch"


@pytest.mark.parametrize(
    ("attack", "reason_code"),
    [
        ("omit", "source_routing_realization_stage_cardinality_invalid"),
        ("duplicate", "source_routing_realization_stage_order_invalid"),
        ("reorder", "source_routing_realization_stage_order_invalid"),
        ("policy_substitution", "source_routing_realization_policy_consumption_mismatch"),
        ("algorithm_substitution", "source_routing_realization_stage_binding_mismatch"),
    ],
)
def test_realization_rejects_stage_omission_duplication_reorder_or_substitution(
    attack: str, reason_code: str
) -> None:
    bundle = _two_phase_fixture()
    receipts = copy.deepcopy(bundle["stage_receipts"])
    if attack == "omit":
        receipts.pop()
    elif attack == "duplicate":
        receipts[2] = copy.deepcopy(receipts[1])
    elif attack == "reorder":
        receipts[0], receipts[1] = receipts[1], receipts[0]
    elif attack == "policy_substitution":
        receipts[0]["pre_map_policy_id"] = "source-routing-pre-map-policy.substitute"
    else:
        receipts[0]["algorithm_contract_digest"] = "sha256:" + "f" * 64
    with pytest.raises(LiteratureAcquisitionError) as caught:
        _rebuild_realization(bundle, stage_receipts=receipts)
    assert caught.value.reason_code == reason_code


def test_realization_rejects_stage_before_policy_and_stale_completion() -> None:
    bundle = _two_phase_fixture()
    receipts = copy.deepcopy(bundle["stage_receipts"])
    seal_time = datetime.fromisoformat(
        bundle["policy"]["sealed_at"].replace("Z", "+00:00")
    )
    receipts[0]["started_at"] = _iso(seal_time - timedelta(seconds=1))
    with pytest.raises(LiteratureAcquisitionError) as before_policy:
        _rebuild_realization(bundle, stage_receipts=receipts)
    assert (
        before_policy.value.reason_code
        == "source_routing_realization_stage_order_invalid"
    )

    with pytest.raises(LiteratureAcquisitionError) as stale:
        _rebuild_realization(
            bundle,
            completed_at=bundle["policy"]["freshness_contract"]["consume_before"],
        )
    assert stale.value.reason_code == "source_routing_realization_stale"


@pytest.mark.parametrize("attack", ["omit", "substitute"])
def test_realization_rejects_mapping_output_omission_or_substitution(
    attack: str,
) -> None:
    bundle = _two_phase_fixture()
    mappings = copy.deepcopy(bundle["claim_mappings"])
    if attack == "omit":
        mappings.pop()
    else:
        mappings[0]["source_id"] = "source-substitution"
    with pytest.raises(LiteratureAcquisitionError) as caught:
        _rebuild_realization(bundle, claim_mappings=mappings)
    assert caught.value.reason_code == "source_routing_realization_mapping_output_mismatch"


def test_realization_rejects_negative_only_source_reframed_as_support() -> None:
    bundle = _two_phase_fixture()
    source_id = bundle["authority"]["source_ids"][0]
    bundle["authority"]["source_routing_eligibility"][source_id] = (
        "negative_evidence_only"
    )
    bundle["policy"] = build_source_routing_pre_map_policy(
        authority=bundle["authority"],
        snapshot=bundle["snapshot"],
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        acquisition_producer_receipt=bundle["acquisition_receipt"],
        algorithm_contracts=bundle["algorithms"],
        freshness_max_age_seconds=86_400,
    )
    with pytest.raises(LiteratureAcquisitionError) as caught:
        source_routing_realization_requirements(
            policy=bundle["policy"],
            snapshot=bundle["snapshot"],
            validated_warrants=bundle["validated_warrants"],
            claim_mappings=bundle["claim_mappings"],
            assimilation=bundle["assimilation"],
        )
    assert caught.value.reason_code == "source_routing_negative_only_violation"


def test_realization_validator_rejects_rehashed_completed_output_attack() -> None:
    bundle = _two_phase_fixture()
    realization = copy.deepcopy(bundle["realization"])
    realization["completed_outputs"]["claim_mapping"]["mapping_count"] += 1
    realization["realization_digest"] = top_level_content_digest(
        realization, "realization_digest"
    )
    with pytest.raises(LiteratureAcquisitionError) as caught:
        validate_source_routing_realization(
            realization,
            policy=bundle["policy"],
            authority=bundle["authority"],
            snapshot=bundle["snapshot"],
            acquisition_producer_receipt=bundle["acquisition_receipt"],
            algorithm_contracts=bundle["algorithms"],
            validated_warrants=bundle["validated_warrants"],
            claim_mappings=bundle["claim_mappings"],
            assimilation=bundle["assimilation"],
            stage_receipts=bundle["stage_receipts"],
        )
    assert caught.value.reason_code == "source_routing_realization_replay_mismatch"


def test_legacy_post_assimilation_certificate_is_typed_compatibility_only() -> None:
    fixture = _routing_fixture()
    certificate = _build(fixture)
    assert certificate["compatibility"] == {
        "status": "post_assimilation_compatibility_only",
        "pre_map_authority_authorized": False,
        "replacement_envelope_fields": [
            "source_routing_pre_map_policy",
            "source_routing_realization",
        ],
        "boundary": (
            "post-assimilation compatibility artifact only; pre-map policy authority "
            "is false and consumers must migrate to source_routing_pre_map_policy "
            "plus source_routing_realization"
        ),
    }
    with pytest.raises(
        ContractError,
        match="active source routing requires one exact pre-map policy and realization",
    ):
        validate_source_authority_pair_execution(
            active_required=True,
            payloads={
                "literature_snapshot": [fixture["snapshot"]],
                "literature_assimilation": [fixture["assimilation"]],
                "source_routing_precommit": [certificate],
                "source_routing_pre_map_policy": [],
                "source_routing_realization": [],
            },
            producers_by_role={},
            operator_requests=[],
            operator_receipts=[],
            input_payloads={},
        )
