# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Replay and integrity tests for cumulative conceptual-discovery state."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, Namespace, canonical_digest
from agentic.discovery.ledger import (
    GENESIS_HASH,
    SYNTHESIS_AUTHORITY_NULLS,
    EpistemicLedger,
    LedgerIntegrityError,
    build_event,
    initial_state,
    reduce_events,
    reduce_from_state,
    replay_fixture,
    validate_event_chain,
)
from tests.discovery.test_reflective_conceptual_discovery import _strict_operator_request


NS = Namespace("target-concept", "run-theory", "main", 0)
SYNTHESIS_AUTHORITY_BOUNDARY = (
    "sealed conceptual preference is internal-only; proof, empirical, "
    "external-validation, source-truth, theorem, mass-gap, and physics-result "
    "authority remain null"
)


def _chain(specs: list[dict]) -> list[dict]:
    events: list[dict] = []
    for index, spec in enumerate(specs, 1):
        namespace = spec.pop("namespace", Namespace(NS.target_id, NS.run_id, spec.pop("branch", "main"), spec.pop("state_version", 0)))
        event = build_event(
            sequence=index,
            previous_event_hash=events[-1]["event_hash"] if events else GENESIS_HASH,
            namespace=namespace,
            actor="test-reducer",
            occurred_at=f"2026-07-21T10:00:{index:02d}Z",
            relations=spec.pop("relations", ()),
            source_receipt_ids=spec.pop("source_receipt_ids", ("receipt.valid",)),
            **spec,
        )
        events.append(event)
    return events


def _full_events() -> list[dict]:
    return _chain(
        [
            {"event_type": "entity_upsert", "entity_type": "conceptual_system", "entity_id": "theory-a", "payload": {"record": {"name": "Constraint geometry", "status": "active", "genealogy": []}}},
            {"event_type": "entity_upsert", "entity_type": "conceptual_system", "entity_id": "theory-b", "payload": {"record": {"name": "Information bottlenecks", "status": "active", "genealogy": []}}},
            {"event_type": "entity_upsert", "entity_type": "branch", "entity_id": "bold-a", "payload": {"record": {"status": "active", "intuition_genealogy": [{"intuition": "complexity is conserved under representation change", "pre_search": True}]}}},
            {"event_type": "entity_upsert", "entity_type": "branch", "entity_id": "bold-b", "payload": {"record": {"status": "active", "intuition_genealogy": [{"intuition": "proof search has a phase transition", "pre_search": True}]}}},
            {"event_type": "perspective_shift", "entity_type": "transformation", "entity_id": "shift-1", "payload": {"transformation_kind": "perspective_shift", "affected_system_ids": ["theory-a", "theory-b"], "result_revision_ids": {"theory-a": "theory-a-r2", "theory-b": "theory-b-r2"}, "parent_revision_ids": {"theory-a": "theory-a-r1", "theory-b": "theory-b-r1"}, "preserved_differences": ["geometric versus informational explanatory ideals"]}},
            {"event_type": "entity_upsert", "entity_type": "hypothesis", "entity_id": "hyp-a", "payload": {"record": {"status": "proposed", "interpretations": ["geometric reading"], "evidence_edges": []}}},
            {"event_type": "entity_upsert", "entity_type": "hypothesis", "entity_id": "hyp-b", "payload": {"record": {"status": "proposed", "interpretations": ["informational reading"], "evidence_edges": []}}},
            {"event_type": "evidence_recorded", "entity_type": "evidence", "entity_id": "evidence-shared", "payload": {"hypothesis_ids": ["hyp-a", "hyp-b"], "claim_id": "claim-shared", "relation": "supports", "decisive": False, "truth_status": "suggestive", "theoretical_interpretation": "same finite witness, distinct theory readings"}},
            {"event_type": "branch_attempt_recorded", "entity_type": "branch_attempt", "entity_id": "attempt-a-1", "branch": "bold-a", "payload": {"branch_id": "bold-a", "outcome": "failed", "parent_branch_ids": ["main"], "conflicts": [], "artifact_digests": []}},
            {"event_type": "branch_attempt_recorded", "entity_type": "branch_attempt", "entity_id": "attempt-b-1", "branch": "bold-b", "payload": {"branch_id": "bold-b", "outcome": "validated", "parent_branch_ids": ["main"], "conflicts": [{"with": "bold-a", "kind": "ontology"}], "artifact_digests": [canonical_digest({"result": "partial"})]}},
            {"event_type": "literature_snapshot_recorded", "entity_type": "literature_snapshot", "entity_id": "literature-2026-07", "state_version": 1, "payload": {"completed_at": "2026-07-21T11:00:00Z", "coverage_cutoff": "2026-07-20T23:59:59Z", "content_digest": canonical_digest(["source-a", "source-b"]), "source_claim_mappings": [{"source": "source-a", "claim": "claim-shared"}], "source_theory_deltas": [{"source": "source-b", "system_id": "theory-b", "delta": "narrows mechanism"}], "affected_branch_ids": ["bold-a", "bold-b"], "survivor_branch_ids": ["bold-b"], "branch_rebases": [{"branch_id": "bold-b", "disposition": "revised", "theory_delta": {"mechanism": "narrowed"}}]}},
            {"event_type": "route_retired", "entity_type": "route", "entity_id": "bold-a", "state_version": 1, "payload": {"falsified_premise": "all representations preserve the hard core", "negative_knowledge": "representation maps can erase the obstruction", "retirement_reason": "validated counterexample"}},
        ]
    )


def _synthesis_material(
    outcome: str, *, include_evidence: bool = True
) -> tuple[Namespace, list[dict], dict]:
    request, preferred = _strict_operator_request(outcome)
    systems = copy.deepcopy(request["conceptual_systems"])
    system_ids = [row["system_id"] for row in systems]
    preferred_ids = list(preferred) if include_evidence else []
    evidence = (
        copy.deepcopy(request["conceptual_adjudication_evidence"])
        if include_evidence
        else None
    )
    diagnostic_ids = [] if preferred_ids else (
        list(evidence["preference_set"]["nondominated_system_ids"])
        if evidence is not None and outcome == "revise_all"
        else [system_ids[0]]
    )
    authority_ids = [*preferred_ids, *diagnostic_ids]
    systems_by_id = {row["system_id"]: row for row in systems}
    unification_maps = []
    for system_id in authority_ids:
        claims = copy.deepcopy(systems_by_id[system_id]["unification_claims"])
        unification_maps.append(
            {
                "system_id": system_id,
                "unification_map": claims,
                "preserved_differences": copy.deepcopy(
                    claims.get(
                        "preserved_differences",
                        claims.get("differences_preserved", []),
                    )
                ),
            }
        )
    payload = {
        "component_system_ids": system_ids[:2],
        "unification_maps": unification_maps,
        "conceptual_systems": systems,
        "reflection_rounds": copy.deepcopy(request["reflection_rounds"]),
        "conceptual_adjudication_evidence": evidence,
        "preferred_system_ids": preferred_ids,
        "diagnostic_synthesis_system_ids": diagnostic_ids,
        "preference_authorized": bool(preferred_ids),
        "authority_boundary": SYNTHESIS_AUTHORITY_BOUNDARY,
        "authority_nulls": copy.deepcopy(SYNTHESIS_AUTHORITY_NULLS),
    }
    return (
        Namespace(
            request["target_id"], request["run_id"], "root", request["state_version"]
        ),
        systems,
        payload,
    )


def _synthesis_chain(
    namespace: Namespace, ledger_systems: list[dict], payload: dict
) -> list[dict]:
    specs = [
        {
            "namespace": namespace,
            "event_type": "entity_upsert",
            "entity_type": "conceptual_system",
            "entity_id": system["system_id"],
            "payload": {"record": copy.deepcopy(system)},
        }
        for system in ledger_systems
    ]
    specs.append(
        {
            "namespace": namespace,
            "event_type": "synthesis_recorded",
            "entity_type": "synthesis",
            "entity_id": "synthesis-sealed",
            "payload": copy.deepcopy(payload),
        }
    )
    return _chain(specs)


def test_reducer_preserves_genealogy_multi_hypothesis_evidence_and_negative_knowledge() -> None:
    state = reduce_events(_full_events())
    assert state["active_theory_constellation"] == ["theory-a", "theory-b"]
    assert state["conceptual_systems"]["theory-a"]["current_revision_id"] == "theory-a-r2"
    assert state["conceptual_systems"]["theory-b"]["current_revision_id"] == "theory-b-r2"
    assert state["conceptual_systems"]["theory-a"]["genealogy"][0]["preserved_differences"]
    assert state["hypotheses"]["hyp-a"]["evidence_edges"][0]["evidence_id"] == "evidence-shared"
    assert state["hypotheses"]["hyp-b"]["interpretations"][0] == "informational reading"
    assert state["retired_routes"]["bold-a"]["falsified_premise"].startswith("all representations")


def test_literature_supersession_marks_stale_and_rebases_without_erasing_intuition() -> None:
    state = reduce_events(_full_events())
    assert state["current_literature_snapshot_id"] == "literature-2026-07"
    assert state["stale_branches"] == ["bold-a"]
    assert state["branches"]["bold-b"]["literature_snapshot_id"] == "literature-2026-07"
    assert state["branches"]["bold-b"]["intuition_genealogy"][0]["pre_search"] is True
    assert state["rebase_history"][0]["branch_id"] == "bold-b"


def test_parallel_failure_conflict_and_valid_partial_result_are_reconstructable() -> None:
    state = reduce_events(_full_events())
    assert state["branch_attempts"]["attempt-a-1"]["outcome"] == "failed"
    assert state["branch_attempts"]["attempt-b-1"]["outcome"] == "validated"
    assert state["branches"]["bold-a"]["operational_failures"] == ["attempt-a-1"]
    assert state["branches"]["bold-b"]["validated_attempts"] == ["attempt-b-1"]
    assert state["branches"]["bold-b"]["conflicts"][0]["with"] == "bold-a"


@pytest.mark.parametrize(
    ("outcome", "expected_status"),
    [
        ("unique", "sealed_unique"),
        ("plural", "sealed_plural"),
        ("revise_all", "sealed_revise_all_diagnostic_only"),
    ],
)
def test_synthesis_reducer_preserves_complete_set_valued_preference_algebra(
    outcome: str, expected_status: str
) -> None:
    namespace, systems, payload = _synthesis_material(outcome)
    state = reduce_events(_synthesis_chain(namespace, systems, payload))
    synthesis = state["syntheses"]["synthesis-sealed"]
    authority = synthesis["conceptual_preference_authority"]

    assert authority["status"] == expected_status
    assert authority["preferred_system_ids"] == payload["preferred_system_ids"]
    assert synthesis["conceptual_adjudication_evidence"] == payload[
        "conceptual_adjudication_evidence"
    ]
    assert authority["authority_nulls"] == SYNTHESIS_AUTHORITY_NULLS
    assert [row["system_id"] for row in authority["unification_maps"]] == [
        *payload["preferred_system_ids"],
        *payload["diagnostic_synthesis_system_ids"],
    ]
    for system in systems:
        reduced = state["conceptual_systems"][system["system_id"]]
        assert reduced["lifecycle_state"] == system["lifecycle_state"]
        if system["system_id"] in payload["preferred_system_ids"]:
            assert reduced["preference_synthesis_memberships"] == ["synthesis-sealed"]
            assert reduced["conceptual_preference_evidence_ids"] == [
                payload["conceptual_adjudication_evidence"]["evidence_id"]
            ]
            assert "diagnostic_synthesis_memberships" not in reduced
        elif system["system_id"] in payload["diagnostic_synthesis_system_ids"]:
            assert reduced["diagnostic_synthesis_memberships"] == ["synthesis-sealed"]
            assert "preference_synthesis_memberships" not in reduced
        else:
            assert "preference_synthesis_memberships" not in reduced
            assert "diagnostic_synthesis_memberships" not in reduced


def test_null_adjudication_records_only_diagnostic_synthesis_membership() -> None:
    namespace, systems, payload = _synthesis_material("unique", include_evidence=False)
    state = reduce_events(_synthesis_chain(namespace, systems, payload))
    authority = state["syntheses"]["synthesis-sealed"][
        "conceptual_preference_authority"
    ]
    diagnostic_id = payload["diagnostic_synthesis_system_ids"][0]
    assert authority["status"] == "absent_diagnostic_only"
    assert authority["evidence_id"] is None
    assert authority["preferred_system_ids"] == []
    assert state["conceptual_systems"][diagnostic_id][
        "diagnostic_synthesis_memberships"
    ] == ["synthesis-sealed"]


def test_synthesis_schema_rejects_singular_id_only_or_non_null_truth_authority() -> None:
    namespace, systems, payload = _synthesis_material("unique")
    singular = copy.deepcopy(payload)
    singular["preferred_system_id"] = singular["preferred_system_ids"][0]
    with pytest.raises(ContractError, match="schema validation"):
        _synthesis_chain(namespace, systems, singular)

    detached = copy.deepcopy(payload)
    detached.pop("conceptual_adjudication_evidence")
    detached["conceptual_adjudication_evidence_id"] = "evidence.detached"
    with pytest.raises(ContractError, match="schema validation"):
        _synthesis_chain(namespace, systems, detached)

    overclaimed = copy.deepcopy(payload)
    overclaimed["authority_nulls"]["proof_authority"] = "claimed"
    with pytest.raises(ContractError, match="schema validation"):
        _synthesis_chain(namespace, systems, overclaimed)


def test_synthesis_reducer_rejects_preference_and_recursive_input_forgery() -> None:
    namespace, systems, payload = _synthesis_material("unique")
    forged_preference = copy.deepcopy(payload)
    forged_preference["preferred_system_ids"] = [
        next(
            row["system_id"]
            for row in systems
            if row["system_id"] not in payload["preferred_system_ids"]
        )
    ]
    with pytest.raises(LedgerIntegrityError, match="recomputed sealed set"):
        reduce_events(_synthesis_chain(namespace, systems, forged_preference))

    spliced_systems = copy.deepcopy(payload)
    spliced_systems["conceptual_systems"][0]["mechanism_or_principle"] += " forged"
    with pytest.raises(LedgerIntegrityError, match="sealed candidate set"):
        reduce_events(
            _synthesis_chain(
                namespace, spliced_systems["conceptual_systems"], spliced_systems
            )
        )

    spliced_rounds = copy.deepcopy(payload)
    spliced_rounds["reflection_rounds"][0]["strongest_objections"][0] += " forged"
    with pytest.raises(LedgerIntegrityError, match="sealed reflection input"):
        reduce_events(_synthesis_chain(namespace, systems, spliced_rounds))


def test_synthesis_unification_rows_are_exact_set_indexed_and_ordered() -> None:
    namespace, systems, payload = _synthesis_material("plural")
    assert len(payload["unification_maps"]) == 2

    omitted = copy.deepcopy(payload)
    omitted["unification_maps"] = omitted["unification_maps"][:1]
    with pytest.raises(LedgerIntegrityError, match="ordered bijection"):
        reduce_events(_synthesis_chain(namespace, systems, omitted))

    reordered = copy.deepcopy(payload)
    reordered["unification_maps"] = list(reversed(reordered["unification_maps"]))
    with pytest.raises(LedgerIntegrityError, match="ordered bijection"):
        reduce_events(_synthesis_chain(namespace, systems, reordered))

    substituted = copy.deepcopy(payload)
    substituted["unification_maps"][1]["unification_map"]["mediator"][
        "statement"
    ] += " coherently rehashed but foreign"
    with pytest.raises(LedgerIntegrityError, match="differs from its exact system claim"):
        reduce_events(_synthesis_chain(namespace, systems, substituted))

    legacy_singular = copy.deepcopy(payload)
    row = legacy_singular.pop("unification_maps")[0]
    legacy_singular["unification_map"] = row["unification_map"]
    legacy_singular["preserved_differences"] = row["preserved_differences"]
    with pytest.raises(ContractError, match="schema validation"):
        _synthesis_chain(namespace, systems, legacy_singular)


def test_hash_chain_detects_payload_predecessor_and_cross_target_tampering() -> None:
    events = _full_events()
    tampered = copy.deepcopy(events)
    tampered[2]["payload"]["record"]["status"] = "rewritten"
    with pytest.raises(LedgerIntegrityError, match="hash mismatch"):
        validate_event_chain(tampered)
    tampered = copy.deepcopy(events)
    tampered[4]["previous_event_hash"] = GENESIS_HASH
    with pytest.raises(LedgerIntegrityError, match="predecessor"):
        validate_event_chain(tampered)
    tampered = copy.deepcopy(events)
    tampered[-1]["identity"]["target_id"] = "other-target"
    # Re-hashing only the modified event cannot hide a cross-target splice.
    from agentic.discovery.ledger import event_hash

    tampered[-1]["deduplication_key"] = canonical_digest({
        "event_type": tampered[-1]["event_type"], "entity_type": tampered[-1]["entity_type"],
        "entity_id": tampered[-1]["entity_id"], "identity": tampered[-1]["identity"],
        "payload": tampered[-1]["payload"], "relations": tampered[-1]["relations"],
        "source_receipt_ids": tampered[-1]["source_receipt_ids"],
    })
    tampered[-1]["event_hash"] = event_hash(tampered[-1])
    with pytest.raises(LedgerIntegrityError, match="cross-target"):
        validate_event_chain(tampered)


def test_equivalent_append_is_idempotent_and_conflicting_log_is_rejected(tmp_path: Path) -> None:
    ledger = EpistemicLedger(tmp_path / "ledger.jsonl")
    kwargs = dict(
        namespace=NS,
        event_type="entity_upsert",
        entity_type="hypothesis",
        entity_id="hyp-repeat",
        payload={"record": {"status": "proposed"}},
        actor="operator-a",
        source_receipt_ids=("receipt.1",),
    )
    first, appended = ledger.append_semantic(**kwargs, occurred_at="2026-07-21T12:00:00Z")
    repeated, appended_again = ledger.append_semantic(**kwargs, occurred_at="2026-07-21T12:01:00Z")
    assert appended is True and appended_again is False
    assert repeated["event_id"] == first["event_id"]
    assert len(ledger.read()) == 1


def test_replay_is_deterministic_across_input_object_key_order() -> None:
    events = _full_events()
    state1 = reduce_events(events)
    reordered = [json.loads(json.dumps(event, sort_keys=True)) for event in events]
    state2 = reduce_events(reordered)
    assert canonical_digest(state1) == canonical_digest(state2)


def test_versioned_fixture_replays_expected_constellation() -> None:
    fixture = json.loads(
        (Path(__file__).parents[1] / "fixtures" / "discovery_epistemic_ledger" / "replay.json").read_text(
            encoding="utf-8"
        )
    )
    state = replay_fixture(fixture)
    assert state["active_theory_constellation"] == ["fixture-theory"]
    assert state["retired_routes"]["fixture-route"]["negative_knowledge"]


def test_event_suffix_advances_verified_state_without_global_latest() -> None:
    first = build_event(
        sequence=1,
        previous_event_hash=GENESIS_HASH,
        namespace=Namespace("target-a", "run-a", "root", 0),
        event_type="entity_upsert",
        entity_type="conceptual_system",
        entity_id="system-a",
        payload={"record": {"status": "active", "ontology": {"primitives": ["relation"]}}},
        actor="reflective-conceptual-discovery",
        source_receipt_ids=["receipt-a"],
    )
    generation_one = reduce_from_state(initial_state("target-a", "run-a"), [first])
    assert generation_one["generation"] == 1
    second = build_event(
        sequence=2,
        previous_event_hash=first["event_hash"],
        namespace=Namespace("target-a", "run-a", "root", 1),
        event_type="reflection_recorded",
        entity_type="reflection",
        entity_id="reflection-a",
        payload={"result": "mutated", "changed_system_ids": ["system-a"]},
        actor="reflective-theory-synthesizer",
        source_receipt_ids=["receipt-b"],
    )
    generation_two = reduce_from_state(generation_one, [second])
    assert generation_two["generation"] == 2
    assert generation_two["event_count"] == 2
    assert "system-a" in generation_two["conceptual_systems"]
    assert "reflection-a" in generation_two["reflections"]


def test_event_suffix_rejects_broken_sequence_boundary() -> None:
    event = build_event(
        sequence=2,
        previous_event_hash=GENESIS_HASH,
        namespace=Namespace("target-a", "run-a", "root", 0),
        event_type="reflection_recorded",
        entity_type="reflection",
        entity_id="reflection-a",
        payload={"result": "mutated"},
        actor="reflective-theory-synthesizer",
    )
    with pytest.raises(LedgerIntegrityError, match="starts at sequence"):
        reduce_from_state(initial_state("target-a", "run-a"), [event])
