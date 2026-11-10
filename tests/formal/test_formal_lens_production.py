# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Constructive production tests for the central Category/HoTT reasoning route.

The oracle is intentionally stronger than schema occupancy.  Tests require one
frozen ancestor, a separately sealed decision rule, actual finite obstruction
replay, a coequalizer or path-cell construction, model-derived predicate values,
and an exact physics handback.  They also preserve the negative boundaries:
assumption deletion and unchanged decisions quarantine, the nonformal control
cannot mutate formal facts, thread concurrency is not isolation, and rehashing
an authored result cannot replace executable replay.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery.contracts import canonical_digest, canonical_json, validate_payload
from agentic.discovery.formal_lens_production import (
    FormalLensProductionError,
    _RouteExecutionContext,
    _build_packet,
    produce_capable_nonformal_route,
    produce_categorical_route,
    produce_combined_route,
    produce_hott_route,
    run_formal_lens_production,
    validate_formal_lens_production_bundle,
    validate_formal_lens_production_packet,
    validate_formal_lens_production_request,
)
from agentic.discovery.formal_lens_registry import (
    FormalLensRegistryError,
    ROUTE_ORDER,
    load_formal_lens_producer_registry,
)


ROOT = Path(__file__).resolve().parents[2]
OBLIGATION = "obligation.physics.transport"
PHYSICAL_CARRIER = "gauge-invariant observable algebra over regulated field measures"
REGIME = "cutoff removal before reconstruction and spectral transfer"
QUANTIFIERS = [
    "For every declared regulated gauge-invariant observable.",
    "Uniformly over the declared regulator-removal family.",
]
UNTOUCHED_GATES = [
    "continuum construction",
    "Osterwalder-Schrader reconstruction",
    "uniform positive mass gap",
]


def _request(
    *,
    category_mode: str = "constructive_finite_completion",
    hott_mode: str = "constructive_finite_completion",
    category_changes_decision: bool = True,
    include_hott_relation: bool = True,
) -> dict:
    incumbent = {
        "decision_id": "decision.incumbent",
        "decision_kind": "continue_route",
        "action": "Continue the incumbent direct route.",
        "target_burden_id": OBLIGATION,
    }
    category_basis = (
        {
            "decision_id": "decision.category",
            "decision_kind": "construct_mediator",
            "action": "Route through the constructed finite mediator.",
            "target_burden_id": OBLIGATION,
        }
        if category_changes_decision
        else copy.deepcopy(incumbent)
    )
    category = {**category_basis, "trigger_relation_id": "relation.category"}
    hott_trigger = "relation.hott" if include_hott_relation else "relation.category"
    hott = {
        "decision_id": "decision.hott",
        "decision_kind": "require_coherence",
        "action": "Require the constructed transport coherence cell.",
        "target_burden_id": OBLIGATION,
        "trigger_relation_id": hott_trigger,
    }
    relations = [
        {
            "relation_id": "relation.category",
            "relation_kind": "noncommuting_composition",
            "statement": "Regulator removal and reconstruction form noncommuting composites.",
            "source_anchor": "regulated observable algebra",
            "target_anchor": "reflection positive reconstruction data",
        }
    ]
    if include_hott_relation:
        relations.append(
            {
                "relation_id": "relation.hott",
                "relation_kind": "equivalence_coherence",
                "statement": "Equivalent presentations induce transports needing a higher coherence cell.",
                "source_anchor": "reconstruction functor",
                "target_anchor": "gauge invariant observable content",
            }
        )
    semantics = {
        "pressure": "Reconcile regulator removal and observable reconstruction without assuming commutation.",
        "formal_pressure": "Two route compositions and two equivalence transports disagree on a finite semantic carrier.",
        "protected_invariants": [
            "gauge invariant observable content",
            "reflection positive reconstruction data",
        ],
        "incumbent_primitives": [
            "regulated observable algebra",
            "reconstruction functor",
            "spectral transfer interface",
        ],
        "physical_carrier": PHYSICAL_CARRIER,
        "regime": REGIME,
        "quantifiers": list(QUANTIFIERS),
        "falsifier": "Exhibit one observable for which the completed routes still disagree.",
        "correction": "Quarantine the abstraction and split the route-specific burdens.",
        "untouched_physics_gates": list(UNTOUCHED_GATES),
        "task_relations": relations,
        "incumbent_decision": incumbent,
        "lens_decisions": {"categorical": category, "hott": hott},
    }
    task_case = {
        "case_id": "case.physics.formal",
        "target_id": "target.physics.formal",
        "obligation_id": OBLIGATION,
        "preferred_lens": "categorical",
        "task_semantics": semantics,
    }
    creativity_content = {
        "conceptual_pressure": semantics["pressure"],
        "high_risk_hypotheses": [
            {
                "hypothesis_id": "hypothesis.mediator",
                "statement": "A coequalizing mediator may separate representational mismatch from physical failure.",
                "relevance_bridge": "The mediator targets the exact route-order burden.",
                "failure_condition": "The quotient fails to equalize the route actions.",
            }
        ],
        "reflective_questions": ["Which mismatch is representational and which is physical?"],
        "convergence_criteria": ["Preserve carrier, quantifiers, correction, and falsifier."],
    }
    literature_content = {
        "projection_cutoff": "2026-07-22T12:00:00Z",
        "source_receipt_ids": ["receipt.source.1"],
        "committed_event_ids": ["event.literature.1"],
        "pressure_updates": ["Current evidence leaves route-order coherence unresolved."],
        "explicit_unknowns": ["Continuum transport remains open."],
    }
    rule = {
        "rule_id": "rule.physics.formal",
        "rule_kind": "ordered_first_match_boolean.v1",
        "predicates": [
            {
                "predicate_id": "predicate.category.removed",
                "baseline_value": False,
                "statement": "The finite categorical obstruction has a constructed completion.",
            },
            {
                "predicate_id": "predicate.hott.removed",
                "baseline_value": False,
                "statement": "The finite HoTT coherence obstruction has a constructed cell.",
            },
        ],
        "obstruction_bindings": {
            "categorical": ["predicate.category.removed"],
            "hott": ["predicate.hott.removed"],
        },
        "clauses": [
            {
                "clause_id": "clause.combined",
                "priority": 0,
                "all_of": [
                    {"predicate_id": "predicate.category.removed", "equals": True},
                    {"predicate_id": "predicate.hott.removed", "equals": True},
                ],
                "decision": {
                    "decision_id": "decision.combined",
                    "decision_kind": "split_route",
                    "action": "Compare the mediator and coherence routes under both constructed obligations.",
                    "target_burden_id": OBLIGATION,
                },
            },
            {
                "clause_id": "clause.category",
                "priority": 1,
                "all_of": [
                    {"predicate_id": "predicate.category.removed", "equals": True}
                ],
                "decision": category_basis,
            },
            {
                "clause_id": "clause.hott",
                "priority": 2,
                "all_of": [
                    {"predicate_id": "predicate.hott.removed", "equals": True}
                ],
                "decision": {
                    key: value for key, value in hott.items() if key != "trigger_relation_id"
                },
            },
        ],
        "default_decision": incumbent,
    }
    rule["rule_digest"] = canonical_digest(rule)
    precommit = {
        "precommit_id": "precommit.physics.formal",
        "rule_id": rule["rule_id"],
        "rule_digest": rule["rule_digest"],
        "authority_class": "separate_local_protocol_precommit_only",
        "committed_before_formal_routes": True,
    }
    precommit["precommit_digest"] = canonical_digest(precommit)
    creativity = {
        "role": "central_reflective_conceptual_creativity",
        "packet_id": "creativity.packet.1",
        "packet_digest": canonical_digest(creativity_content),
        "content": creativity_content,
    }
    literature = {
        "role": "committed_current_literature_projection",
        "projection_id": "literature.projection.1",
        "projection_digest": canonical_digest(literature_content),
        "content": literature_content,
    }
    ancestor = {
        "ancestor_id": "ancestor.physics.formal",
        "state_generation": 4,
        "task_case_digest": canonical_digest(task_case),
        "central_creativity_packet_digest": creativity["packet_digest"],
        "current_literature_projection_digest": literature["projection_digest"],
        "domain_decision_rule_digest": rule["rule_digest"],
    }
    ancestor["ancestor_digest"] = canonical_digest(ancestor)
    request = {
        "schema_version": "1.0.0",
        "formal_request_id": "request.physics.formal",
        "identity": {
            "target_id": "target.physics.formal",
            "run_id": "run.physics.formal",
            "branch_id": "branch.physics.formal",
            "state_version": 4,
        },
        "task_case": task_case,
        "task_case_digest": canonical_digest(task_case),
        "central_creativity_input": creativity,
        "current_literature_projection": literature,
        "frozen_task_semantic_ancestor": ancestor,
        "domain_decision_rule": rule,
        "domain_decision_rule_precommit": precommit,
        "lens_policy": {
            "conditional_parallel_lenses": ["categorical", "hott"],
            "combined_requires_all": ["categorical", "hott"],
            "always_parallel_controls": ["capable_nonformal"],
            "inapplicable_lenses_are_not_executed": True,
            "construction_modes": {
                "categorical": category_mode,
                "hott": hott_mode,
            },
        },
        "experiment_policy": {
            "role": "secondary_theory_requested_falsifier_only",
            "automatic_theory_selection": False,
            "retroactive_theory_selection": False,
        },
    }
    request["request_digest"] = canonical_digest(request)
    return request


@pytest.fixture(scope="module")
def production_bundle(tmp_path_factory: pytest.TempPathFactory) -> tuple[dict, dict, Path]:
    root = tmp_path_factory.mktemp("constructive-formal")
    request = _request()
    packet = run_formal_lens_production(request, root)
    return request, packet, root


def test_request_and_packet_schemas_are_meta_valid_and_candidate_is_inhabited() -> None:
    for name in (
        "formal_lens_production_request.schema.json",
        "formal_lens_production_packet.schema.json",
    ):
        schema = json.loads((ROOT / "agentic/spec" / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    request = _request()
    validate_payload(request, "formal_lens_production_request.schema.json")
    assert validate_formal_lens_production_request(request) == request
    assert request["task_case"]["task_semantics"]["lens_decisions"]["categorical"][
        "trigger_relation_id"
    ] == "relation.category"


def test_registry_loads_exact_four_routes_and_refuses_isolation_inflation(tmp_path: Path) -> None:
    bindings, record = load_formal_lens_producer_registry()
    assert [row.route_id for row in bindings] == list(ROUTE_ORDER)
    assert [row.callable_name for row in bindings] == [
        "produce_categorical_route",
        "produce_hott_route",
        "produce_combined_route",
        "produce_capable_nonformal_route",
    ]
    assert record["authority_boundary"] == "repository_local_registered_execution_not_external_authority"
    registry = json.loads(
        (ROOT / "agentic/registries/formal_lens_producer_registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    registry["execution_contract"]["process_isolation"] = True
    attacked = tmp_path / "registry.json"
    attacked.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(FormalLensRegistryError, match="execution/isolation contract drift"):
        load_formal_lens_producer_registry(attacked)


def test_four_routes_share_one_ancestor_and_construct_only_bounded_formal_repairs(
    production_bundle: tuple[dict, dict, Path],
) -> None:
    request, packet, _ = production_bundle
    assert packet["production_status"] == "complete_with_quarantine"
    assert packet["execution_contract"]["scheduler"] == "ThreadPoolExecutor"
    assert packet["execution_contract"]["start_barrier_parties"] == 4
    assert packet["execution_contract"]["process_isolation"] is False
    assert packet["terminal_barrier"]["all_routes_terminal"] is True
    assert packet["terminal_barrier"]["failed_routes"] == []
    receipts = {row["route_id"]: row for row in packet["route_receipts"]}
    assert list(receipts) == list(ROUTE_ORDER)
    assert {
        row["frozen_ancestor_digest"] for row in receipts.values()
    } == {request["frozen_task_semantic_ancestor"]["ancestor_digest"]}
    assert {row["request_digest"] for row in receipts.values()} == {request["request_digest"]}
    assert all(row["isolation_assurance"] == {
        "process_isolation": False,
        "kernel_isolation": False,
        "filesystem_isolation": False,
        "network_isolation": False,
        "hidden_input_independence": False,
        "cognitive_independence": False,
        "semantic_independence": False,
    } for row in receipts.values())

    category = receipts["categorical"]["result"]
    category_model = category["formal_components"][0]["intervened_model"]
    assert category_model["construction_kind"] == "finite_coequalizer_commuting_completion"
    assert category_model["commuting_completion"]["left_postcomposition"] == category_model[
        "commuting_completion"
    ]["right_postcomposition"]
    assert all(row["commutes"] for row in category_model["naturality_checks"])
    assert category_model["universal_property"][
        "unique_factorization_for_every_compatible_map"
    ] is True
    assert category["rule_replay"]["replay_status"] == "constructive_decision_change"

    hott = receipts["hott"]["result"]
    hott_model = hott["formal_components"][0]["intervened_model"]
    assert hott_model["construction_kind"] == "finite_pointwise_transport_coherence_completion"
    assert hott_model["coherence_cell"]["all_boundaries_inhabited"] is True
    boundaries = hott_model["equality_boundaries"]
    assert boundaries == {
        "judgmental_equality_claimed": False,
        "identity_paths_constructed": True,
        "equivalences_validated_as_finite_bijections": True,
        "equivalence_collapsed_to_identity": False,
        "transport_scope": "declared_finite_predicate_fibers_only",
        "truncation_scope": "retain_through_constructed_level_2_cell_no_higher_claim",
        "univalence_assumed": False,
        "universe_scope": "one_declared_finite_local_universe_only",
        "higher_coherence_scope": "exact_constructed_cell_only",
    }
    assert receipts["combined"]["result"]["formal_components"][0]["lens"] == "categorical"
    assert receipts["combined"]["result"]["formal_components"][1]["lens"] == "hott"

    control = receipts["capable_nonformal"]["result"]
    assert receipts["capable_nonformal"]["terminal_status"] == "quarantined"
    assert control["formal_components"] == []
    assert control["nonformal_analysis"]["formal_predicates_mutated"] is False
    assert control["rule_replay"]["actual_decision_changed"] is False
    assert control["physics_handback"]["handback_status"] == "quarantined_no_decision_change"


def test_physics_handback_is_exact_and_retains_every_authority_null(
    production_bundle: tuple[dict, dict, Path],
) -> None:
    _, packet, _ = production_bundle
    for receipt in packet["route_receipts"]:
        handback = receipt["result"]["physics_handback"]
        assert handback["physical_carrier"] == PHYSICAL_CARRIER
        assert handback["regime"] == REGIME
        assert handback["quantifiers"] == QUANTIFIERS
        assert handback["untouched_physics_gates"] == UNTOUCHED_GATES
        assert handback["correction"] == "Quarantine the abstraction and split the route-specific burdens."
        assert handback["falsifier"] == "Exhibit one observable for which the completed routes still disagree."
        assert handback["experiment_role"] == "secondary_theory_requested_falsifier_only"
        assert handback["physics_value_authorized"] is False
        assert handback["investment_authorized"] is False
        assert {
            "creativity",
            "conceptual_depth",
            "unification_power",
            "physics_value",
            "physical_equivalence",
            "continuum_construction",
            "theorem",
            "mass_gap",
            "Yang_Mills_result",
        } <= set(handback["authority_nulls"])


def test_bundle_is_atomic_last_exact_and_idempotently_reopenable(
    production_bundle: tuple[dict, dict, Path],
) -> None:
    request, packet, root = production_bundle
    bundle = root / request["formal_request_id"]
    expected_files = {
        "request.json",
        "receipts/categorical.json",
        "receipts/hott.json",
        "receipts/combined.json",
        "receipts/capable_nonformal.json",
        "terminal-barrier.json",
        "formal-lens-production-packet.json",
    }
    assert {
        path.relative_to(bundle).as_posix() for path in bundle.rglob("*") if path.is_file()
    } == expected_files
    assert validate_formal_lens_production_bundle(bundle) == packet
    assert run_formal_lens_production(request, root) == packet


def test_assumption_away_predicate_flip_is_typed_and_quarantined() -> None:
    request = validate_formal_lens_production_request(
        _request(category_mode="unavailable_assumption_away_only")
    )
    category = produce_categorical_route(request, _RouteExecutionContext(None))
    component = category["formal_components"][0]
    assert component["construction_status"] == "hypothetical_assumption_away_sensitivity"
    assert component["intervened_model"] is None
    assert category["rule_replay"]["actual_decision_changed"] is False
    assert category["rule_replay"]["hypothetical_decision_changed"] is True
    assert category["rule_replay"]["replay_status"] == "hypothetical_assumption_away_sensitivity"
    assert category["disposition"] == "quarantined_non_investment"
    assert category["physics_handback"]["handback_status"] == "hypothetical_assumption_away_sensitivity"
    combined = produce_combined_route(request, _RouteExecutionContext(None))
    assert combined["rule_replay"]["actual_decision_changed"] is False
    assert combined["disposition"] == "quarantined_non_investment"


def test_constructed_obstruction_with_unchanged_domain_decision_quarantines() -> None:
    request = validate_formal_lens_production_request(
        _request(category_changes_decision=False)
    )
    result = produce_categorical_route(request, _RouteExecutionContext(None))
    assert result["formal_components"][0]["construction_status"] == "constructively_removed"
    assert result["formal_components"][0]["intervened_model"]["construction_valid"] is True
    assert result["rule_replay"]["actual_decision_changed"] is False
    assert result["rule_replay"]["replay_status"] == "quarantined_no_decision_change"
    assert result["disposition"] == "quarantined_non_investment"


def test_inapplicable_hott_and_combined_routes_do_not_execute_formal_forgers() -> None:
    request = validate_formal_lens_production_request(_request(include_hott_relation=False))
    hott = produce_hott_route(request, _RouteExecutionContext(None))
    combined = produce_combined_route(request, _RouteExecutionContext(None))
    assert hott["formal_components"] == []
    assert combined["formal_components"] == []
    assert hott["disposition"] == combined["disposition"] == "quarantined_non_investment"
    control = produce_capable_nonformal_route(request, _RouteExecutionContext(None))
    assert control["nonformal_analysis"]["formal_predicates_mutated"] is False


def test_rehashed_authored_handback_cannot_replace_executable_route_replay(
    production_bundle: tuple[dict, dict, Path],
) -> None:
    request, packet, _ = production_bundle
    receipts = copy.deepcopy(packet["route_receipts"])
    result = receipts[0]["result"]
    handback = result["physics_handback"]
    handback["changed_burden"] = "A rhetorically improved but unconstructed foreign burden."
    handback["handback_digest"] = canonical_digest(
        {key: value for key, value in handback.items() if key != "handback_digest"}
    )
    result["result_digest"] = canonical_digest(
        {key: value for key, value in result.items() if key != "result_digest"}
    )
    receipts[0]["receipt_digest"] = canonical_digest(
        {key: value for key, value in receipts[0].items() if key != "receipt_digest"}
    )
    attacked = _build_packet(request, packet["registry_binding"], receipts)
    validate_payload(attacked, "formal_lens_production_packet.schema.json")
    with pytest.raises(FormalLensProductionError, match="route receipt differs"):
        validate_formal_lens_production_packet(request, attacked)


def test_changed_literature_bytes_cannot_hide_behind_old_frozen_ancestor() -> None:
    request = _request()
    request["current_literature_projection"]["content"]["pressure_updates"][0] = (
        "A changed projection attempts to enter the old formal ancestor."
    )
    request["current_literature_projection"]["projection_digest"] = canonical_digest(
        request["current_literature_projection"]["content"]
    )
    request["request_digest"] = canonical_digest(
        {key: value for key, value in request.items() if key != "request_digest"}
    )
    with pytest.raises(FormalLensProductionError, match="frozen ancestor"):
        validate_formal_lens_production_request(request)


def test_cli_runs_and_revalidates_the_durable_bundle(tmp_path: Path) -> None:
    request = _request()
    request_path = tmp_path / "request.json"
    request_path.write_bytes(canonical_json(request) + b"\n")
    output_root = tmp_path / "runs"
    script = ROOT / "agentic/scripts/run_formal_lens_production.py"
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    run = subprocess.run(
        [
            sys.executable,
            str(script),
            "run",
            "--request",
            str(request_path),
            "--output-root",
            str(output_root),
        ],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert run.returncode == 0, run.stderr.decode()
    packet = json.loads(run.stdout)
    bundle = output_root / request["formal_request_id"]
    validate = subprocess.run(
        [sys.executable, str(script), "validate", "--bundle", str(bundle)],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert validate.returncode == 0, validate.stderr.decode()
    assert json.loads(validate.stdout) == packet
