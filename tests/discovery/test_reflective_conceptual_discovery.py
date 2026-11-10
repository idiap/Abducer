# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executable acceptance tests for the theory-first parent discovery loop."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import tests.discovery.test_conceptual_adjudication as adjudication_fixtures

from agentic.discovery.conceptual_adjudication import (
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
)
from agentic.discovery.contracts import canonical_digest
from agentic.discovery.reflection import ReflectionInvariantError, structural_signature, validate_packet_invariants
from agentic.discovery.reflection import system_from_hypothesis
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.workflow import (
    DiscoveryWorkflowError,
    _parallel_reference,
    build_reflective_discovery_packet,
)
from agentic.discovery.parallel import build_parallel_manifest, run_parallel_hypothesis_portfolio
from agentic.scripts.run_discovery_operator_protocol import _conceptual_adjudication


CORNERS = [
    "ontology_inversion", "missing_mediator", "relation_first", "scale_reversal",
    "cross_field_transfer", "unification_conjecture", "negative_theory", "counter_consensus",
]


def hypothesis(index: int, corner: str) -> dict:
    return {
        "hypothesis_id": f"hypothesis.{index}",
        "corner_family": corner,
        "concept_lifecycle_state": "literature_rebased",
        "maturation_status": "parallel_ready",
        "truth_status": "conjectural",
        "intuitive_leap": f"Treat pressure {index} through {corner}.",
        "new_primitives_relations_or_mechanisms": [f"primitive-{index}", f"relation-{index}"],
        "target_pressures_addressed": [f"pressure-{index}", "shared-root-pressure"],
        "protected_successes": ["preserve exact target and incumbent boundary case"],
        "assumptions_or_invariants_risked": [f"incumbent-assumption-{index}"],
        "explanatory_upside": f"Makes hidden dependence {index} expressible.",
        "unification_upside": f"Connects pressure {index} to the shared root while preserving its regime.",
        "value_if_right": f"Reorganizes route family {index}.",
        "learning_value_if_wrong": f"Rules out mechanism family {index} without deleting its genealogy.",
        "probability_status": "low and explicitly uncertain" if index < 2 else "open",
        "conceptual_distance": f"Changes primitive and mechanism family {index}.",
        "literature_relation": "cross_field_bridge" if index == 4 else "apparently_open",
        "literature_source_ids": [f"source.{index}"],
        "non_claim_boundary": "This seed is not a proof or novelty claim.",
        "maturation_question": f"What invariant makes mechanism {index} non-vacuous?",
        "correction_conditions": [f"Retire if boundary witness {index} collapses to the incumbent."],
        "boundary_case": f"At boundary {index}, the mechanism must not become a target proxy.",
        "branch_independence_signature": {
            "unique_primitives": [f"primitive-{index}"],
            "unique_mechanism": f"mechanism-{index}",
            "forbidden_cross_branch_context": ["sibling conclusions during blind divergence"],
            "overlaps_with_hypothesis_ids": [],
        },
    }


def major_request() -> dict:
    hypotheses = [hypothesis(index, corner) for index, corner in enumerate(CORNERS)]
    return {
        "target_id": "target-a",
        "run_id": "run-a",
        "branch_id": "root",
        "state_version": 4,
        "prior_conceptual_state_ref": "state:4",
        "discovery_charter": {
            "essential_question": "What single structure explains the shared obstruction without weakening the target?",
            "desired_understanding": "Explain why apparently distinct route failures recur and which distinctions remain essential.",
            "bottleneck_diagnosis": "conceptual",
            "bottleneck_evidence": "Three mature routes fail at the same unrepresented interface despite completed local derivations.",
            "target_commitments": ["preserve the exact target", "preserve quantifier order"],
            "relevance_horizon": "A successful concept would reorganize multiple essential target routes.",
            "incumbent_framework": "object-first local route decomposition",
            "conceptual_opacity": "The shared obstruction is visible only as unrelated local failures.",
            "non_claim_boundary": "No theorem, empirical law, or literature novelty is established by this cycle."
        },
        "conceptual_genealogy": {
            "inherited_concepts": ["local route", "witness", "barrier"],
            "historical_or_logical_formation": ["Local proof decomposition made route-specific failures primary."],
            "protected_successes": ["known special cases", "target quantifier order"],
            "rejected_or_retired_ancestors": ["one-size-fits-all bridge"],
            "hidden_assumptions": ["local objects are the fundamental explanatory units"]
        },
        "literature_basis": {
            "selected_snapshot_id": "literature.target-a.20260721",
            "snapshot_target_id": "target-a",
            "selected_snapshot_digest": "sha256:" + "1" * 64,
            "search_completed_utc": "2026-07-21T10:00:00Z",
            "freshness_status": "current",
            "search_receipt_ids": ["search.target-a.1"],
            "assimilation_packet_ref": "agentic/runs/reflective_discovery/target-a/run-a/literature/assimilation.json",
            "source_to_theory_delta_summary": ["Source 7 reframed the barrier as a carrier mismatch."],
            "literature_generated_questions": ["Can the carrier mismatch be represented without changing target scope?"],
            "coverage_limitations": ["Provider coverage ends at 2026-07-20."],
            "superseded_snapshot_ids": []
        },
        "root_tensions": [{
            "tension_id": "tension.shared-obstruction",
            "opposed_commitments": ["route-local explanation", "shared obstruction recurrence"],
            "strongest_form_of_each_side": ["Each route has distinct formal objects.", "The same failure relation recurs across routes."],
            "minimal_incompatibility_or_missing_mediation": "No current carrier relates route-specific objects without identifying them.",
            "regime": "all active essential routes",
            "why_root_level": "The missing relation blocks explanation before local proof work begins."
        }],
        "high_risk_portfolio": {
            "portfolio_id": "portfolio.target-a.4",
            "hypotheses": hypotheses,
            "selected_hypothesis_ids": [item["hypothesis_id"] for item in hypotheses],
            "protected_wildcard_ids": ["hypothesis.0", "hypothesis.1"],
            "control_hypothesis_ids": ["hypothesis.7"]
        },
        "operator_receipt_ids": ["receipt.literature", "receipt.high-risk"],
        "explicit_unknowns": ["Whether the proposed mediation admits a nontrivial formal model."]
    }


def _strict_operator_request(outcome: str) -> tuple[dict, list[str]]:
    """Compose the real adjudicator with the workflow over all preference outcomes.

    The closed typed-graph and deep-lens builders are shared with the dedicated
    adjudication adversaries.  This prevents the workflow test from passing with
    a weaker mock representation than the registered operator actually accepts.
    """

    if outcome not in {"unique", "plural", "revise_all"}:
        raise AssertionError(f"unsupported preference outcome fixture: {outcome}")
    request = major_request()
    local_packet = build_reflective_discovery_packet(request)
    systems = copy.deepcopy(local_packet["conceptual_systems"])
    rounds = copy.deepcopy(local_packet["reflection_rounds"])
    qualified_count = 1 if outcome == "unique" else 2 if outcome == "plural" else 0
    qualified_ids: list[str] = []
    conceptual_fields = (
        "primitives",
        "relations_operations_and_dynamics",
        "mechanism_or_principle",
        "target_pressures_addressed",
        "identities_and_differences",
        "unification_claims",
        "implications_and_new_questions",
        "formalization_seeds",
        "correction_conditions",
        "residual_contradictions",
        "non_claims",
    )
    for index, system in enumerate(systems):
        is_qualified = index < qualified_count
        strict_content = adjudication_fixtures._typed_system(
            str(system["system_id"]), deep=is_qualified
        )
        for field in conceptual_fields:
            system[field] = copy.deepcopy(strict_content[field])
        if is_qualified:
            qualified_ids.append(str(system["system_id"]))

    frozen_genealogy: list[dict] = []
    theory_state_digest = canonical_digest(
        {"prior_conceptual_state_ref": request["prior_conceptual_state_ref"]}
    )
    portfolio_digest = canonical_digest(request["high_risk_portfolio"])
    proposer_receipt_ids = list(request["operator_receipt_ids"])
    source_bindings = build_adjudication_source_bindings(
        run_id=request["run_id"],
        state_version=request["state_version"],
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=request["literature_basis"][
            "selected_snapshot_digest"
        ],
        high_risk_portfolio_digest=portfolio_digest,
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=frozen_genealogy,
        proposer_receipt_ids=proposer_receipt_ids,
    )
    blind_packet, candidate_bindings = build_blind_packet(
        target_id=request["target_id"],
        stage_id="post-reflection",
        target_charter={
            "root_tensions": [
                request["root_tensions"][0][
                    "minimal_incompatibility_or_missing_mediation"
                ]
            ]
        },
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity="reflective-operator",
        source_bindings=source_bindings,
        counterbalance_seed=f"workflow-{outcome}-counterbalance",
    )
    reports = [
        build_judge_report(
            blind_packet,
            adjudicator_id=f"workflow-{lens}-judge",
            perspective=lens,
            lens_family=lens,
            version="1.0.0",
            judge=judge,
            created_at="2026-07-22T00:00:00Z",
        )
        for lens, judge in (
            ("ontological", adjudication_fixtures._ontological_judge),
            ("dialectical", adjudication_fixtures._dialectical_judge),
            ("explanatory", adjudication_fixtures._explanatory_judge),
        )
    ]
    evidence, _unknowns = _conceptual_adjudication(
        {
            "identity": {
                "target_id": request["target_id"],
                "run_id": request["run_id"],
                "branch_id": request["branch_id"],
                "state_version": request["state_version"],
            }
        },
        {
            "blind_packet": blind_packet,
            "judge_reports": reports,
            "systems": systems,
            "reflection_rounds": rounds,
            "frozen_genealogy": frozen_genealogy,
            "candidate_bindings": candidate_bindings,
            "theory_state_digest": theory_state_digest,
            "literature_snapshot_digest": request["literature_basis"][
                "selected_snapshot_digest"
            ],
            "high_risk_portfolio_digest": portfolio_digest,
            "proposer_receipt_ids": proposer_receipt_ids,
            "created_at": "2026-07-22T00:00:00Z",
        },
    )
    request.update(
        {
            "generation_mode": "operator_generated",
            "conceptual_systems": systems,
            "reflection_rounds": rounds,
            "conceptual_adjudication_evidence": evidence,
        }
    )
    return request, sorted(qualified_ids)


def test_major_cycle_is_plural_reflective_current_and_probe_optional() -> None:
    packet = build_reflective_discovery_packet(major_request())
    assert len(packet["conceptual_systems"]) >= 4
    assert len({structural_signature(item) for item in packet["conceptual_systems"]}) == len(packet["conceptual_systems"])
    assert [item["result"] for item in packet["reflection_rounds"][:2]] == ["mutated", "synthesized"]
    assert packet["provisional_synthesis"]["preferred_system_id"] is None
    assert packet["provisional_synthesis"]["preferred_system_ids"] == []
    assert packet["conceptual_adjudication_evidence"] is None
    diagnostic_id = packet["provisional_synthesis"]["diagnostic_synthesis_system_ids"][0]
    diagnostic = next(item for item in packet["conceptual_systems"] if item["system_id"] == diagnostic_id)
    assert len(diagnostic["unification_claims"]["unified_cases_or_routes"]) >= 2
    assert diagnostic["unification_claims"]["differences_preserved"]
    assert packet["understanding_delta"]["before"] != packet["understanding_delta"]["after"]
    assert packet["support_probe"]["disposition"] == "no_probe_needed"
    assert packet["generation_mode"] == "local_structural_fallback"
    assert packet["stage_gates"]["G2_philosophical_depth"] == "open"
    assert packet["truth_convergence_status"]["conceptual_preference"].startswith("incubating_structural_set")
    assert packet["provisional_synthesis"]["authority_status"] == "absent_diagnostic_only"
    assert packet["theoretical_programme"]["conceptual_system_ids"] == [diagnostic_id]
    assert packet["theoretical_programme"]["investment_authorized"] is False
    assert packet["understanding_delta"]["authority_distinct_merit_evidence"] is False
    assert packet["stage_gates"]["G7_claim_promotion"] == "not_requested"
    assert len(packet["high_risk_hypothesis_portfolio"]["corner_families"]) == 8
    assert len(packet["high_risk_hypothesis_portfolio"]["protected_wildcard_ids"]) == 2


def test_missing_or_stale_search_blocks_active_theory_investment() -> None:
    for status in ("local_only", "stale", "refresh_required", "literature_blind_incubation"):
        request = major_request()
        request["literature_basis"]["freshness_status"] = status
        with pytest.raises(DiscoveryWorkflowError, match="newest validated"):
            build_reflective_discovery_packet(request)
    request = major_request()
    request["literature_basis"]["search_receipt_ids"] = []
    with pytest.raises(DiscoveryWorkflowError, match="cannot substitute"):
        build_reflective_discovery_packet(request)


def test_not_conceptual_control_routes_without_philosophical_theatre() -> None:
    request = major_request()
    request["discovery_charter"]["bottleneck_diagnosis"] = "not_conceptual"
    request["discovery_charter"]["bottleneck_evidence"] = "All required concepts are stable; one finite derivation remains."
    request["ordinary_handoff"] = "derive"
    packet = build_reflective_discovery_packet(request)
    assert packet["conceptual_systems"] == []
    assert packet["reflection_rounds"] == []
    assert packet["next_reflective_action"]["kind"] == "derive"
    assert packet["high_risk_hypothesis_portfolio"]["disposition"] == "not_requested"
    assert packet["provisional_synthesis"]["authority_status"] == "not_conceptual"
    assert packet["theoretical_programme"]["component_programmes"] == []
    assert packet["understanding_delta"]["system_deltas"] == []


def test_structurally_duplicate_renaming_is_not_a_plural_system() -> None:
    packet = build_reflective_discovery_packet(major_request())
    duplicate = copy.deepcopy(packet["conceptual_systems"][1])
    duplicate["system_id"] = "system.renamed"
    packet["conceptual_systems"] = [packet["conceptual_systems"][0], packet["conceptual_systems"][1], duplicate]
    with pytest.raises(ReflectionInvariantError, match="structurally different"):
        validate_packet_invariants(packet)


def test_typed_structural_identity_is_invariant_to_prose_rename_and_order() -> None:
    packet = build_reflective_discovery_packet(major_request())
    original = packet["conceptual_systems"][1]
    renamed = copy.deepcopy(original)
    renamed["system_id"] = "system.display-renamed"
    renamed["mechanism_or_principle"] = "Completely different display prose for the same typed mechanism."
    renamed["primitives"] = list(reversed(renamed["primitives"]))
    renamed["structural_identity"]["primitive_ids"] = list(reversed(renamed["structural_identity"]["primitive_ids"]))
    assert structural_signature(original) == structural_signature(renamed)


def test_philosophical_vapour_and_unification_by_erasure_fail() -> None:
    packet = build_reflective_discovery_packet(major_request())
    packet["reflection_rounds"][0]["mutation_or_synthesis"]["changed_primitives_relations_or_explanation"] = []
    with pytest.raises(ReflectionInvariantError, match="without structural change"):
        validate_packet_invariants(packet)
    packet = build_reflective_discovery_packet(major_request())
    diagnostic_id = packet["provisional_synthesis"]["diagnostic_synthesis_system_ids"][0]
    diagnostic = next(item for item in packet["conceptual_systems"] if item["system_id"] == diagnostic_id)
    diagnostic["unification_claims"]["differences_preserved"] = []
    with pytest.raises(ReflectionInvariantError, match="erasure"):
        validate_packet_invariants(packet)


def test_commissioned_support_is_programme_bound_and_reflectively_assimilated() -> None:
    request, preferred_ids = _strict_operator_request("unique")
    preview = build_reflective_discovery_packet(request)
    request["support_probe"] = {
        "disposition": "assimilated", "theory_programme_id": preview["theoretical_programme"]["programme_id"],
        "theoretical_question_id": "question.discriminating", "conceptual_system_ids": preferred_ids,
        "theoretical_question": "Does the proposed mediator preserve the declared invariant on the finite carrier?",
        "role": "finite_countermodel", "why_theory_alone_is_currently_insufficient": "The finite compatibility equations remain undecided.",
        "possible_theory_updates": ["Reframe the mediator if a verified witness violates compatibility."],
        "receipt_ids": ["experiment.receipt.1"], "reflective_assimilation_event_ids": ["event.assimilate.1"]
    }
    packet = build_reflective_discovery_packet(request)
    assert packet["support_probe"]["theory_programme_id"]
    assert packet["support_probe"]["reflective_assimilation_event_ids"]
    packet["support_probe"]["reflective_assimilation_event_ids"] = []
    with pytest.raises(ReflectionInvariantError, match="reflective assimilation"):
        validate_packet_invariants(packet)


def test_caller_winner_and_receipt_id_cannot_authorize_operator_preference() -> None:
    local = build_reflective_discovery_packet(major_request())
    request = major_request()
    request["generation_mode"] = "operator_generated"
    request["conceptual_systems"] = local["conceptual_systems"]
    request["reflection_rounds"] = local["reflection_rounds"]
    request["preferred_system_id"] = local["provisional_synthesis"][
        "diagnostic_synthesis_system_ids"
    ][0]
    with pytest.raises(DiscoveryWorkflowError, match="caller-selected"):
        build_reflective_discovery_packet(request)
    request.pop("preferred_system_id")
    request["evaluation_receipt_ids"] = ["evaluation.independent.1"]
    packet = build_reflective_discovery_packet(request)
    assert packet["provisional_synthesis"]["preferred_system_ids"] == []
    assert packet["provisional_synthesis"]["preferred_system_id"] is None
    assert packet["stage_gates"]["G2_philosophical_depth"] == "open"
    assert packet["truth_convergence_status"]["conceptual_preference"].startswith(
        "incubating_structural_set"
    )
    forged = copy.deepcopy(packet)
    forged["provisional_synthesis"]["preferred_system_id"] = forged[
        "provisional_synthesis"
    ]["diagnostic_synthesis_system_ids"][0]
    forged["provisional_synthesis"]["preferred_system_ids"] = [
        forged["provisional_synthesis"]["preferred_system_id"]
    ]
    with pytest.raises(ReflectionInvariantError, match="sealed conceptual adjudication"):
        validate_packet_invariants(forged)


@pytest.mark.parametrize(
    ("outcome", "expected_decision"),
    [
        ("unique", "prefer_unique"),
        ("plural", "retain_plural_nondominated"),
        ("revise_all", "revise_all"),
    ],
)
def test_registered_adjudicator_controls_the_complete_workflow_preference_algebra(
    outcome: str, expected_decision: str
) -> None:
    request, expected_preferred_ids = _strict_operator_request(outcome)
    packet = build_reflective_discovery_packet(request)
    evidence = packet["conceptual_adjudication_evidence"]
    synthesis = packet["provisional_synthesis"]

    assert evidence["preference_set"]["decision"] == expected_decision
    assert synthesis["preferred_system_ids"] == expected_preferred_ids
    assert synthesis["preferred_system_id"] == (
        expected_preferred_ids[0] if len(expected_preferred_ids) == 1 else None
    )
    assert synthesis["preference_authority_evidence_id"] == evidence["evidence_id"]
    expected_status = {
        "prefer_unique": "sealed_unique",
        "retain_plural_nondominated": "sealed_plural",
        "revise_all": "sealed_revise_all_diagnostic_only",
    }[expected_decision]
    assert synthesis["authority_status"] == expected_status
    assert synthesis["investment_authorized"] is bool(expected_preferred_ids)
    authority_ids = expected_preferred_ids or evidence["preference_set"][
        "nondominated_system_ids"
    ]
    assert packet["theoretical_programme"]["conceptual_system_ids"] == authority_ids
    assert [
        row["conceptual_system_id"]
        for row in packet["theoretical_programme"]["component_programmes"]
    ] == authority_ids
    assert packet["understanding_delta"]["conceptual_system_ids"] == authority_ids
    assert packet["stage_gates"]["G2_philosophical_depth"] == "open"
    assert packet["stage_gates"]["G4_understanding_gain"] == "open"
    validate_packet_invariants(packet)

    if expected_preferred_ids:
        assert synthesis["diagnostic_synthesis_system_ids"] == []
        preference_events = [
            event
            for event in packet["ledger_events"]
            if event["event_type"] == "conceptual_preference_sealed"
        ]
        assert len(preference_events) == 1
        assert preference_events[0]["entity_ids"] == expected_preferred_ids
        assert packet["truth_convergence_status"]["conceptual_preference"] == (
            f"sealed_preference_set:{','.join(expected_preferred_ids)}"
        )
    else:
        assert synthesis["diagnostic_synthesis_system_ids"] == evidence[
            "preference_set"
        ]["nondominated_system_ids"]
        assert packet["support_probe"]["conceptual_system_ids"] == []
        assert packet["support_probe"]["theory_programme_id"] is None
        assert packet["theoretical_programme"]["proof_or_model_obligations"] == []
        assert packet["next_reflective_action"]["kind"] == "reframe"
        assert not any(
            event["event_type"] == "conceptual_preference_sealed"
            for event in packet["ledger_events"]
        )
        diagnostic = next(
            event
            for event in packet["ledger_events"]
            if event["event_type"] == "diagnostic_theory_set_retained"
        )
        assert diagnostic["entity_ids"] == synthesis[
            "diagnostic_synthesis_system_ids"
        ]
        assert diagnostic["preference_authorized"] is False
        assert packet["truth_convergence_status"]["conceptual_preference"] == (
            "sealed_revise_all"
        )


def test_plural_support_cannot_silently_target_only_the_first_member() -> None:
    request, preferred_ids = _strict_operator_request("plural")
    preview = build_reflective_discovery_packet(request)
    assert len(preferred_ids) == 2
    request["support_probe"] = {
        "disposition": "no_probe_needed",
        "theory_programme_id": preview["theoretical_programme"]["programme_id"],
        "theoretical_question_id": None,
        "conceptual_system_ids": preferred_ids[:1],
        "theoretical_question": None,
        "role": "none",
        "why_theory_alone_is_currently_insufficient": None,
        "possible_theory_updates": [],
        "receipt_ids": [],
        "reflective_assimilation_event_ids": [],
    }
    with pytest.raises(DiscoveryWorkflowError, match="complete ordered sealed preference"):
        build_reflective_discovery_packet(request)


def test_set_indexed_programme_and_understanding_tamper_fail_closed() -> None:
    request, _preferred_ids = _strict_operator_request("plural")
    packet = build_reflective_discovery_packet(request)
    packet["theoretical_programme"]["component_programmes"][1][
        "definitions_to_build"
    ] = ["first-member-smuggling"]
    with pytest.raises(ReflectionInvariantError, match="exact system obligations"):
        validate_packet_invariants(packet)

    packet = build_reflective_discovery_packet(request)
    packet["understanding_delta"]["system_deltas"] = packet[
        "understanding_delta"
    ]["system_deltas"][:1]
    with pytest.raises(ReflectionInvariantError, match="ordered bijection"):
        validate_packet_invariants(packet)


def test_generative_case_set_covers_required_failure_families() -> None:
    path = Path(__file__).parents[1] / "generative/reflective_conceptual_discovery_cases.jsonl"
    rows = [__import__("json").loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = {row["case_id"] for row in rows}
    assert {"philosophical-vapour", "unification-by-erasure", "premature-convergence", "wrong-target-latest", "experiment-without-theory-question"} <= ids
    assert any(row["expected"] == "accept_not_conceptual" for row in rows)


def test_executable_high_risk_contract_compiles_into_reflective_system() -> None:
    portfolio = build_demo_high_risk_portfolio()
    candidate = portfolio["hypotheses"][0]
    system = system_from_hypothesis(candidate, major_request()["conceptual_genealogy"])
    assert system["conceptual_ancestors"] == [candidate["hypothesis_id"]]
    assert set(candidate["ontology_delta"]["new_primitives"]).issubset(system["primitives"])
    assert system["mechanism_or_principle"] == candidate["mechanism"]
    assert not set(candidate["ontology_delta"]["new_relations"]).intersection(
        system["primitives"]
    )
    assert set(candidate["ontology_delta"]["new_relations"]).issubset(
        system["relations_operations_and_dynamics"]
    )


def test_executable_parallel_packet_projects_to_valid_reflective_disposition() -> None:
    portfolio = build_demo_high_risk_portfolio()
    manifest = build_parallel_manifest(portfolio, base_theory_state_version=0)

    def worker(request: dict) -> dict:
        return {
            "theory_delta": {
                "delta_class": "perspective_shift",
                "mechanism_key": request["mechanism_key"],
            },
            "claims": [], "genealogy": [request["hypothesis_id"]],
            "conceptual_learning": True,
        }

    packet = run_parallel_hypothesis_portfolio(manifest, worker)
    projected = _parallel_reference(packet)
    assert projected["disposition"] == "validated"
    assert projected["literature_rebase_status"] == "current"
    assert projected["valid_receipt_ids"]


def test_reflection_rejects_portfolio_bound_to_another_literature_digest() -> None:
    request = major_request()
    request["high_risk_portfolio"]["literature_snapshot_digest"] = "sha256:" + "2" * 64
    with pytest.raises(DiscoveryWorkflowError, match="different literature snapshots"):
        build_reflective_discovery_packet(request)
