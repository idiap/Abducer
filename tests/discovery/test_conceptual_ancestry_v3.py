# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""R1518 process, ancestry, and Yang--Mills adversarial evidence."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

import tests.discovery.test_conceptual_adjudication as adjudication_fixtures
import tests.discovery.test_open_world_creativity as open_world_fixtures
import tests.discovery.test_reflective_conceptual_discovery as reflection_fixtures
from agentic.discovery.conceptual_adjudication import (
    build_adjudication_evidence,
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
)
from agentic.discovery.conceptual_ancestry_v3 import (
    AUTHORITY_NULLS as ANCESTRY_AUTHORITY_NULLS,
    ConceptualAncestryV3Error,
    build_bounded_current_literature_bundle,
    build_conceptual_ancestry_v3,
    build_conceptual_ancestry_literature_basis,
    build_conceptual_ancestry_literature_projection,
    build_grounded_corner_impossibility_record,
    build_literature_conditioned_invention_freeze,
    build_pre_taxonomy_corner_coverage,
    build_registered_corner_impossibility_assessment,
    build_registered_adjacent_abstraction_method_lane,
    validate_adjacent_abstraction_method_lane,
    validate_conceptual_ancestry_cycle_binding,
    validate_conceptual_ancestry_v3,
)
from agentic.discovery.contracts import (
    ContractError,
    SchemaValidationError,
    canonical_digest,
    canonical_json,
    stable_identifier,
)
from agentic.discovery.full_core_reflection_lenses import (
    FullCoreReflectionLensError,
    run_full_core_reflection_lenses,
    run_registered_parent_system_materializations,
    validate_full_core_reflection_lens_execution_bundle,
    validate_parent_system_materialization_receipt,
)
from agentic.discovery.literature import LANE_TYPES
from agentic.discovery.literature_snapshot_capture_bridge import (
    build_literature_snapshot_capture_bridge,
)
from agentic.discovery.open_world_creativity import (
    build_non_saturating_conceptual_merit_evaluation,
    build_open_world_hard_integrity_receipt,
    build_open_world_maturation_portfolio,
    build_parallel_maturation_barrier_receipt,
    build_pre_taxonomy_invention_freeze,
    classify_frozen_inventions,
    run_isolated_parallel_maturation_branches,
)
from agentic.discovery.workflow import build_reflective_discovery_packet
from agentic.discovery.yang_mills.ym21_conceptual_ancestry_adapter import (
    YM21_CAPTURE_COMPLETED_AT_UTC,
    YM21_CAPTURE_ID,
    YM21_CAPTURE_SHA256,
    YM21_LATEST_ALLOWED_CAPTURE_DATE,
    YM21_TARGET_ID,
    YM21ConceptualAncestryAdapterError,
    build_ym21_adjacent_abstraction_method_lane,
    build_ym21_bounded_current_literature_bundle,
    build_ym21_literature_snapshot_capture_bridge,
    validate_ym21_adjacent_abstraction_method_lane,
    validate_ym21_conceptual_ancestry_v3,
)
from tests.domains.test_literature_snapshot_capture_bridge import _generic_fixture


ROOT = Path(__file__).resolve().parents[2]
LENS_SCHEMA = (
    ROOT
    / "agentic/spec/full_core_reflection_lens_execution_v1.schema.json"
)
YM_CAPTURE_PATH = (
    ROOT
    / "agentic/evals/ym_representational_dynamics_20260721"
    / "frontier_search_live_capture_20260721.json"
)
YM_SEMANTIC_SNAPSHOT_PATH = (
    ROOT
    / "agentic/reports/ym_representational_dynamics_integration/2026-07-21"
    / "canonical_parent_cycle/workspace/artifacts"
    / "00-frozen-live-literature-snapshot.json"
)
GENERIC_TARGET = "generic-conceptual-ancestry-target"
GENERIC_RUN = "generic-conceptual-ancestry-run"
GENERIC_STATE = 7
GENERIC_CAPTURE_TIME = "2030-01-01T00:00:00Z"
GENERIC_PRESENT_USE = "2030-01-02T00:00:00Z"
YM_RUN = "ym21-conceptual-ancestry-run"
YM_STATE = 7
YM_PRESENT_USE = "2026-07-21T21:16:00Z"
CONCEPTUAL_FIELDS = (
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


def _corner_freeze(raw_inventions: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a small exact freeze for corner-coverage counterexamples."""

    return build_pre_taxonomy_invention_freeze(
        target_id="typed-corner-coverage-target",
        run_id="typed-corner-coverage-run",
        state_version=7,
        target_pressure=(
            "Explain how continuum control could arise without assuming the desired result."
        ),
        root_contradictions=[
            "Finite control and continuum reconstruction pull in different directions."
        ],
        protected_successes=[
            "Retain exact finite-volume positivity and explicit corrections."
        ],
        raw_inventions=raw_inventions,
        known_taxonomy=open_world_fixtures._taxonomy(),
        generator_authority_digest=canonical_digest(
            {"generator": "typed-corner-test-fixture"}
        ),
    )


def _corner_projection() -> dict[str, Any]:
    causal_row = {
        "causal_input_id": "literature-causal-input.corner-fixture",
        "assimilation_delta": {"event_type": "justified_no_change"},
    }
    input_core = {
        "schema_version": "1.0.0",
        "artifact_kind": "literature_derived_invention_input",
        "input_id": "literature-derived-invention-input.corner-fixture",
        "causal_inputs": [causal_row],
    }
    literature_input = {
        **input_core,
        "content_digest": canonical_digest(input_core),
    }
    projection_core = {
        "schema_version": "3.0.0",
        "artifact_kind": "literature_only_projection_v3",
        "literature_derived_invention_input": literature_input,
    }
    return {
        **projection_core,
        "content_digest": canonical_digest(projection_core),
    }


def _causal_family_contracts(
    freeze: dict[str, Any],
    literature_input: dict[str, Any],
    *,
    identical: bool = False,
) -> list[dict[str, Any]]:
    values = {
        "primitive_kind": (
            "entity",
            "process",
            "relation",
            "constraint",
            "information",
            "observer",
        ),
        "relation_kind": (
            "causal",
            "constitutive",
            "constraint",
            "duality",
            "emergent",
            "operational",
        ),
        "mechanism_kind": (
            "mediation",
            "symmetry_breaking",
            "coarse_graining",
            "constraint_propagation",
            "topological_obstruction",
            "feedback",
        ),
        "intervention_kind": (
            "add",
            "remove",
            "hold_fixed",
            "reverse",
            "localize",
            "quotient",
        ),
        "prediction_direction": (
            "increase",
            "decrease",
            "invariant",
            "bifurcate",
            "obstruct",
            "permit",
        ),
        "correction_kind": (
            "retract",
            "retype",
            "split_scope",
            "add_mediator",
            "change_relation",
            "abandon",
        ),
    }
    input_ids = [
        row["causal_input_id"] for row in literature_input["causal_inputs"]
    ]
    rows = []
    for index, invention in enumerate(freeze["raw_inventions"]):
        typed_index = 0 if identical else index % 6
        rows.append(
            {
                "invention_id": invention["invention_id"],
                "source_invention_digest": canonical_digest(invention),
                **{
                    field: options[typed_index]
                    for field, options in values.items()
                },
                "target_grounding_paths": [
                    "/invention_request/target_pressure",
                    "/invention_request/protected_successes/0",
                ],
                "literature_causal_input_ids": [
                    input_ids[index % len(input_ids)]
                ],
            }
        )
    return rows


def _generic_capture_bytes() -> bytes:
    lanes: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    for index, lane_type in enumerate(LANE_TYPES):
        result_id = f"generic-ancestry-result-{index}"
        lanes.append(
            {
                "lane_id": f"generic-ancestry-lane-{index}",
                "lane_type": lane_type,
                "queries": [f"generic ancestry query {index}"],
                "query_policy": "Target-scoped fixture query without result identifiers.",
                "status": "completed",
                "raw_result_ids": [result_id],
            }
        )
        results.append(
            {
                "result_id": result_id,
                "source_id": f"generic-ancestry-source-{index}",
                "title": f"Generic ancestry source {index}",
                "url": f"https://example.test/ancestry/{index}",
                "retrieval_status": "fixture_metadata",
                "disposition": "included_fixture_source",
                "reason": "Retain one deterministic target-scoped source.",
                "claim_status": "fixture_only",
            }
        )
    capture = {
        "schema_version": "1.0",
        "capture_id": "generic-conceptual-ancestry-capture",
        "target_id": GENERIC_TARGET,
        "capture_started_at": GENERIC_CAPTURE_TIME,
        "capture_completed_at": GENERIC_CAPTURE_TIME,
        "coverage_cutoff": GENERIC_CAPTURE_TIME,
        "capture_mode": "live_external_web_search_frozen_for_replay",
        "provider": {
            "provider_id": "generic-ancestry-provider",
            "name": "Generic ancestry fixture provider",
            "index": "deterministic fixture index",
            "execution_boundary": (
                "Fixture metadata represents a frozen external execution."
            ),
            "raw_payload_retention": "Normalized fixture metadata only.",
            "receipt_status": "externally_executed_then_frozen",
            "executable_replay_status": "frozen_response_adapter_only",
        },
        "lanes": lanes,
        "raw_results": results,
        "inclusion_policy": "Include six target-scoped fixture sources.",
        "exclusion_policy": "Exclude unrelated fixture sources.",
        "coverage_limits": ["Only deterministic fixture sources exist."],
        "exhaustive_coverage_claim": False,
        "source_correctness_claim": False,
        "peer_validation_claim": False,
    }
    return canonical_json(capture)


def _build_open_world_inputs(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    run_root: Path,
) -> dict[str, Any]:
    taxonomy = open_world_fixtures._taxonomy()
    freeze = build_pre_taxonomy_invention_freeze(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        target_pressure=(
            "Explain how continuum control could arise without assuming the desired result."
        ),
        root_contradictions=[
            "Finite control and continuum reconstruction pull in different directions."
        ],
        protected_successes=[
            "Retain exact finite-volume positivity and explicit corrections."
        ],
        raw_inventions=[
            open_world_fixtures._raw_invention(index) for index in range(3)
        ],
        known_taxonomy=taxonomy,
        generator_authority_digest=canonical_digest(
            {"generator": "ancestry-fixture"}
        ),
    )
    classification = classify_frozen_inventions(
        freeze,
        known_taxonomy=taxonomy,
        decisions=open_world_fixtures._decisions(),
        classifier_authority_digest=canonical_digest(
            {"classifier": "ancestry-fixture"}
        ),
    )
    matured = [
        open_world_fixtures._matured(
            index,
            stable_identifier(
                "open-world-branch",
                freeze["freeze_id"],
                f"invention-{index}",
            ),
        )
        for index in range(3)
    ]
    records, barrier = run_isolated_parallel_maturation_branches(
        freeze,
        classification,
        known_taxonomy=taxonomy,
        matured_inventions=matured,
        maturation_questions=open_world_fixtures._maturation_questions(),
        run_root=run_root,
    )
    barrier = build_parallel_maturation_barrier_receipt(
        freeze,
        classification,
        known_taxonomy=taxonomy,
        branch_execution_records=records,
    )
    portfolio = build_open_world_maturation_portfolio(
        freeze,
        classification,
        known_taxonomy=taxonomy,
        matured_inventions=matured,
        branch_execution_records=records,
        parallel_barrier_receipt=barrier,
    )
    integrity = build_open_world_hard_integrity_receipt(
        portfolio,
        freeze=freeze,
        classification=classification,
        known_taxonomy=taxonomy,
    )
    controls, blind, private = open_world_fixtures._blind_bundle(
        portfolio, integrity
    )
    merit = build_non_saturating_conceptual_merit_evaluation(
        portfolio,
        controls=controls,
        hard_integrity_receipt=integrity,
        blind_packet=blind,
        private_binding=private,
        evaluator_reports=open_world_fixtures._reports(
            blind, private, controls
        ),
    )
    return {
        "known_taxonomy": taxonomy,
        "invention_freeze": freeze,
        "taxonomy_classification": classification,
        "maturation_portfolio": portfolio,
        "hard_integrity_receipt": integrity,
        "merit_evaluation": merit,
    }


def _parent_packet(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    literature_projection: dict[str, Any],
    systems: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    request = reflection_fixtures.major_request()
    request.update(
        {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
            "prior_conceptual_state_ref": f"state:{state_version}",
            "literature_basis": build_conceptual_ancestry_literature_basis(
                literature_projection
            ),
        }
    )
    local = build_reflective_discovery_packet(request)
    rounds = copy.deepcopy(local["reflection_rounds"])
    source_ids = list(
        dict.fromkeys(
            system_id
            for round_row in rounds
            for system_id in round_row["system_ids"]
        )
    )
    if len(source_ids) != len(systems):
        raise AssertionError(
            "fixture rounds and registered parent systems must be bijective"
        )
    replacements = {
        source_id: system["system_id"]
        for source_id, system in zip(source_ids, systems, strict=True)
    }

    def replace_system_ids(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: replace_system_ids(child)
                for key, child in value.items()
            }
        if isinstance(value, list):
            return [replace_system_ids(child) for child in value]
        if isinstance(value, str):
            return replacements.get(value, value)
        return value

    rounds = replace_system_ids(rounds)
    request.update(
        {
            "generation_mode": "operator_generated",
            "conceptual_systems": copy.deepcopy(systems),
            "reflection_rounds": rounds,
            "conceptual_adjudication_evidence": None,
        }
    )
    return request, build_reflective_discovery_packet(request)


def _adjudication(
    *,
    packet: dict[str, Any],
    stage_id: str,
    theory_state_digest: str,
    literature_digest: str,
    portfolio_digest: str,
    proposer_receipt_ids: list[str],
    previous_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    systems = copy.deepcopy(packet["conceptual_systems"])
    rounds = copy.deepcopy(packet["reflection_rounds"])
    genealogy: list[dict[str, Any]] = []
    source_bindings = build_adjudication_source_bindings(
        run_id=packet["run_id"],
        state_version=packet["state_version"],
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_digest,
        high_risk_portfolio_digest=portfolio_digest,
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=genealogy,
        proposer_receipt_ids=proposer_receipt_ids,
    )
    blind, bindings = build_blind_packet(
        target_id=packet["target_id"],
        stage_id=stage_id,
        target_charter={
            "root_tensions": [
                "Construction and interpretation remain non-substitutable."
            ]
        },
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity="conceptual-ancestry-fixture",
        source_bindings=source_bindings,
        counterbalance_seed=f"{stage_id}-counterbalance",
    )
    reports = [
        build_judge_report(
            blind,
            adjudicator_id=f"{stage_id}-{lens}-judge",
            perspective=lens,
            lens_family=lens,
            version="1.0.0",
            judge=judge,
            created_at="2026-07-21T20:30:00Z",
        )
        for lens, judge in (
            ("ontological", adjudication_fixtures._ontological_judge),
            ("dialectical", adjudication_fixtures._dialectical_judge),
            ("explanatory", adjudication_fixtures._explanatory_judge),
        )
    ]
    return build_adjudication_evidence(
        packet=blind,
        reports=reports,
        candidate_bindings=bindings,
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=genealogy,
        run_id=packet["run_id"],
        state_version=packet["state_version"],
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_digest,
        high_risk_portfolio_digest=portfolio_digest,
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=previous_evidence,
        created_at="2026-07-21T20:30:00Z",
    )


def _build_full_ancestry(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    present_use_at: str,
    literature_bundle: dict[str, Any],
    semantic_snapshot: dict[str, Any],
    literature_bridge: dict[str, Any],
    run_root: Path,
) -> dict[str, Any]:
    open_world = _build_open_world_inputs(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        run_root=run_root / "maturation",
    )
    portfolio = open_world["maturation_portfolio"]
    projection = build_conceptual_ancestry_literature_projection(
        literature_bundle=literature_bundle,
        semantic_snapshot=semantic_snapshot,
        literature_snapshot_capture_bridge=literature_bridge,
        present_use_at=present_use_at,
    )
    literature_input = projection["literature_derived_invention_input"]
    contracts = _causal_family_contracts(
        open_world["invention_freeze"], literature_input
    )
    conditioned_freeze = build_literature_conditioned_invention_freeze(
        open_world["invention_freeze"],
        literature_projection=projection,
        causal_family_contracts=contracts,
    )
    open_world["grounded_corner_impossibility"] = (
        build_registered_corner_impossibility_assessment(
            conditioned_freeze,
            run_root=run_root / "corner-assessor",
        )
    )
    lens_execution_bundles = [
        run_full_core_reflection_lenses(
            candidate,
            run_root=run_root / "literature-bound-lenses",
            literature_derived_invention_input=literature_input,
            minimum_residency_seconds=0.3,
        )
        for candidate in portfolio["matured_inventions"]
    ]
    materialization_receipts = (
        run_registered_parent_system_materializations(
            portfolio["matured_inventions"],
            lens_execution_bundles=lens_execution_bundles,
            run_root=run_root / "parent-materialization",
            minimum_residency_seconds=0.03,
        )
    )
    candidate_by_id = {
        row["invention_id"]: row
        for row in portfolio["matured_inventions"]
    }
    lens_by_id = {
        row["candidate_id"]: row for row in lens_execution_bundles
    }
    materialization_records = []
    for receipt in materialization_receipts:
        candidate_id = receipt["request_payload"]["invocation_context"][
            "candidate_id"
        ]
        materialization_records.append(
            validate_parent_system_materialization_receipt(
                receipt,
                candidate=candidate_by_id[candidate_id],
                lens_execution_bundle=lens_by_id[candidate_id],
            )
        )
    request, parent = _parent_packet(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_projection=projection,
        systems=[
            row["parent_conceptual_system"]
            for row in materialization_records
        ],
    )
    proposer_ids = sorted(
        row["terminal_receipt"]["worker_receipt_id"]
        for row in portfolio["branch_execution_records"]
    )
    theory_digest = canonical_digest(
        {"target_id": target_id, "state_version": state_version}
    )
    literature_digest = semantic_snapshot["content_digest"]
    parent_evidence = _adjudication(
        packet=parent,
        stage_id="parent-conceptual-adjudication",
        theory_state_digest=theory_digest,
        literature_digest=literature_digest,
        portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_ids,
    )
    synthesis_request = copy.deepcopy(request)
    synthesis_request["conceptual_adjudication_evidence"] = parent_evidence
    synthesis = build_reflective_discovery_packet(synthesis_request)
    final_evidence = _adjudication(
        packet=synthesis,
        stage_id="synthesis-conceptual-adjudication",
        theory_state_digest=theory_digest,
        literature_digest=literature_digest,
        portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_ids,
        previous_evidence=parent_evidence,
    )
    build_arguments = {
        "target_id": target_id,
        "run_id": run_id,
        "source_state_version": state_version,
        "theory_state_digest": theory_digest,
        "present_use_at": present_use_at,
        "bounded_literature_bundle": literature_bundle,
        "semantic_literature_snapshot": semantic_snapshot,
        "literature_snapshot_capture_bridge": literature_bridge,
        "causal_family_contracts": contracts,
        **open_world,
        "lens_execution_bundles": lens_execution_bundles,
        "parent_materialization_receipts": materialization_receipts,
        "parent_reflection_packet": parent,
        "parent_adjudication_evidence": parent_evidence,
        "parent_frozen_genealogy": [],
        "synthesis_packet": synthesis,
        "final_adjudication_evidence": final_evidence,
        "final_frozen_genealogy": [],
    }
    ancestry = build_conceptual_ancestry_v3(**build_arguments)
    return {
        "ancestry": ancestry,
        "build_arguments": build_arguments,
        "materialization_records": materialization_records,
    }


@pytest.fixture(scope="module")
def lens_material(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    run_root = tmp_path_factory.mktemp("six-lens-workers")
    candidates = [
        open_world_fixtures._matured(index, f"lens-fixture-branch-{index}")
        for index in range(3)
    ]
    bundles = [
        run_full_core_reflection_lenses(
            candidate,
            run_root=run_root,
            minimum_residency_seconds=0.3,
        )
        for candidate in candidates
    ]
    return {"run_root": run_root, "candidates": candidates, "bundles": bundles}


@pytest.fixture(scope="module")
def generic_ancestry(
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[str, Any]:
    with pytest.MonkeyPatch.context() as monkeypatch:
        literature, semantic_snapshot, bridge = _generic_fixture(monkeypatch)
    return _build_full_ancestry(
        target_id=literature["target_id"],
        run_id=literature["run_id"],
        state_version=literature["state_version"],
        present_use_at=GENERIC_PRESENT_USE,
        literature_bundle=literature,
        semantic_snapshot=semantic_snapshot,
        literature_bridge=bridge,
        run_root=tmp_path_factory.mktemp("generic-ancestry"),
    )


@pytest.fixture(scope="module")
def ym_ancestry(
    tmp_path_factory: pytest.TempPathFactory,
) -> dict[str, Any]:
    literature = build_ym21_bounded_current_literature_bundle(
        capture_bytes=YM_CAPTURE_PATH.read_bytes(),
        run_id=YM_RUN,
        state_version=YM_STATE,
        present_use_at=YM_PRESENT_USE,
    )
    semantic_snapshot = json.loads(
        YM_SEMANTIC_SNAPSHOT_PATH.read_bytes()
    )
    bridge = build_ym21_literature_snapshot_capture_bridge(
        literature_bundle=literature,
        semantic_snapshot=semantic_snapshot,
        present_use_at=YM_PRESENT_USE,
    )
    return _build_full_ancestry(
        target_id=YM21_TARGET_ID,
        run_id=YM_RUN,
        state_version=YM_STATE,
        present_use_at=YM_PRESENT_USE,
        literature_bundle=literature,
        semantic_snapshot=semantic_snapshot,
        literature_bridge=bridge,
        run_root=tmp_path_factory.mktemp("ym-ancestry"),
    )


def test_six_lens_schema_and_positive_process_barrier(
    lens_material: dict[str, Any],
) -> None:
    Draft202012Validator.check_schema(json.loads(LENS_SCHEMA.read_text()))
    for candidate, bundle in zip(
        lens_material["candidates"], lens_material["bundles"], strict=True
    ):
        assert (
            validate_full_core_reflection_lens_execution_bundle(
                bundle,
                candidate=candidate,
                require_promotion_eligible=True,
            )
            == bundle
        )
        barrier = bundle["all_terminal_barrier"]
        assert barrier["accepted_lens_count"] == 6
        assert barrier["distinct_receipt_count"] == 6
        assert barrier["distinct_process_count"] == 6
        assert barrier["observed_peak_parallelism"] == 6
        assert barrier["all_six_intervals_overlap"] is True
        assert bundle["authority_nulls"]["cognitive_independence"] == "unavailable"
        assert bundle["authority_nulls"]["semantic_independence"] == "unavailable"


def test_cosmetic_suffixes_do_not_create_six_structural_families() -> None:
    base = open_world_fixtures._raw_invention(0)
    labels = ("amber", "bronze", "cobalt", "denim", "ember", "fuchsia")
    inventions = []
    for index, label in enumerate(labels):
        raw = copy.deepcopy(base)
        raw["invention_id"] = f"cosmetic-suffix-family-{index}"
        for field in ("primitive_hunches", "relation_hunches"):
            raw[field] = [
                f"{value} cosmetic suffix marker {label}"
                for value in raw[field]
            ]
        for field in (
            "mechanism_hunch",
            "counterfactual_world",
            "first_falsifier",
            "correction_path",
        ):
            raw[field] = f"{raw[field]} Cosmetic suffix marker {label}."
        inventions.append(raw)

    freeze = _corner_freeze(inventions)
    projection = _corner_projection()
    conditioned = build_literature_conditioned_invention_freeze(
        freeze,
        literature_projection=projection,
        causal_family_contracts=_causal_family_contracts(
            freeze,
            projection["literature_derived_invention_input"],
            identical=True,
        ),
    )
    with pytest.raises(
        ConceptualAncestryV3Error,
        match="conceptual_corner_coverage_insufficient",
    ):
        build_pre_taxonomy_corner_coverage(conditioned)


def test_caller_prose_cannot_self_attest_corner_impossibility(
    tmp_path: Path,
) -> None:
    freeze = _corner_freeze(
        [open_world_fixtures._raw_invention(index) for index in range(3)]
    )
    projection = _corner_projection()
    conditioned = build_literature_conditioned_invention_freeze(
        freeze,
        literature_projection=projection,
        causal_family_contracts=_causal_family_contracts(
            freeze, projection["literature_derived_invention_input"]
        ),
    )
    with pytest.raises(
        ConceptualAncestryV3Error,
        match="corner_impossibility_caller_authorship_forbidden",
    ):
        build_grounded_corner_impossibility_record(
            conditioned,
            grounding_paths=[
                "/invention_request/target_pressure",
                "/invention_request/protected_successes/0",
            ],
            blocking_constraints=[
                "Caller says no fourth family can preserve the target success.",
                "Caller says all additional mechanisms would be cosmetic variants.",
            ],
            reason=(
                "Caller-authored prose cannot independently establish that the "
                "sealed generation has exhausted all structurally distinct families."
            ),
            reopen_condition=(
                "Caller will reopen if another family becomes convenient."
            ),
        )

    with pytest.raises(
        ConceptualAncestryV3Error,
        match="corner_impossibility_execution_required",
    ):
        build_registered_corner_impossibility_assessment(conditioned)
    assessment = build_registered_corner_impossibility_assessment(
        conditioned, run_root=tmp_path / "assessor"
    )
    assert assessment["status"] == "registered_freeze_bounded_impossibility"
    separation = assessment["authority_separation"]
    assert separation["execution_separation"] == (
        "distinct_supervised_assessor_process"
    )
    assert isinstance(separation["process_pid"], int)
    assert separation["cognitive_independence"] == "unavailable"
    assert (
        assessment["authority_nulls"]["semantic_impossibility_authority"]
        is None
    )
    caller_reworded = copy.deepcopy(assessment)
    caller_reworded["assessment_output"]["scope"] = (
        "Caller replaces the registered result with a preferred impossibility story."
    )
    caller_reworded["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in caller_reworded.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(
        ConceptualAncestryV3Error,
        match="corner_impossibility_assessment_replay_mismatch",
    ):
        build_pre_taxonomy_corner_coverage(
            conditioned, grounded_impossibility=caller_reworded
        )

    coverage = build_pre_taxonomy_corner_coverage(
        conditioned, grounded_impossibility=assessment
    )
    assert coverage["status"] == (
        "receipt_bound_freeze_bounded_impossibility_accepted"
    )


def test_crashed_lens_still_closes_six_member_terminal_barrier(
    tmp_path: Path,
) -> None:
    candidate = open_world_fixtures._matured(0, "crash-branch")
    bundle = run_full_core_reflection_lenses(
        candidate,
        run_root=tmp_path,
        minimum_residency_seconds=0.25,
        fault_plan={"genealogical": "exit_nonzero"},
    )
    barrier = bundle["all_terminal_barrier"]
    assert bundle["status"] == "all_terminal_not_promotion_eligible"
    assert barrier["terminal_lens_count"] == 6
    assert barrier["accepted_lens_count"] == 5
    assert len(barrier["terminal_members"]) == 6
    assert {row["outcome_status"] for row in barrier["terminal_members"]} == {
        "accepted",
        "operational_failure",
    }
    with pytest.raises(
        FullCoreReflectionLensError,
        match="lens_process_barrier_ineligible",
    ):
        validate_full_core_reflection_lens_execution_bundle(
            bundle,
            candidate=candidate,
            require_promotion_eligible=True,
        )


def test_duplicate_missing_and_mismatched_core_fail_closed(
    lens_material: dict[str, Any],
) -> None:
    candidate = lens_material["candidates"][0]
    original = lens_material["bundles"][0]

    duplicate = copy.deepcopy(original)
    duplicate["lens_executions"][-1] = copy.deepcopy(
        duplicate["lens_executions"][0]
    )
    duplicate["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in duplicate.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(FullCoreReflectionLensError):
        validate_full_core_reflection_lens_execution_bundle(
            duplicate, candidate=candidate
        )

    missing = copy.deepcopy(original)
    missing["lens_executions"].pop()
    missing["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in missing.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(SchemaValidationError):
        validate_full_core_reflection_lens_execution_bundle(
            missing, candidate=candidate
        )

    mismatched = copy.deepcopy(original)
    mismatched["candidate_core"]["statement"] += " substituted"
    mismatched["candidate_core_digest"] = canonical_digest(
        mismatched["candidate_core"]
    )
    mismatched["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in mismatched.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(FullCoreReflectionLensError):
        validate_full_core_reflection_lens_execution_bundle(
            mismatched, candidate=candidate
        )


def test_nonoverlapping_six_processes_are_not_promotion_eligible(
    tmp_path: Path,
) -> None:
    candidate = open_world_fixtures._matured(1, "serial-branch")
    bundle = run_full_core_reflection_lenses(
        candidate,
        run_root=tmp_path,
        max_workers=1,
        minimum_residency_seconds=0.03,
    )
    barrier = bundle["all_terminal_barrier"]
    assert barrier["terminal_lens_count"] == 6
    assert barrier["distinct_process_count"] == 6
    assert barrier["observed_peak_parallelism"] == 1
    assert barrier["all_six_intervals_overlap"] is False
    assert barrier["promotion_eligible"] is False
    with pytest.raises(
        FullCoreReflectionLensError,
        match="lens_process_barrier_ineligible",
    ):
        validate_full_core_reflection_lens_execution_bundle(
            bundle,
            candidate=candidate,
            require_promotion_eligible=True,
        )


@pytest.mark.expensive
def test_full_generic_ancestry_requires_exact_six_process_bundles(
    generic_ancestry: dict[str, Any],
) -> None:
    ancestry = generic_ancestry["ancestry"]
    assert (
        validate_conceptual_ancestry_v3(
            ancestry, present_use_at=GENERIC_PRESENT_USE
        )
        == ancestry
    )
    stages = {
        row["stage_id"]: row["artifact"] for row in ancestry["stages"]
    }
    reflection = stages["six_sibling_full_core_reflections"]
    assert len(reflection["source_lens_execution_bundles"]) == 3
    assert all(
        row["all_terminal_barrier"]["promotion_eligible"]
        for row in reflection["source_lens_execution_bundles"]
    )
    assert ANCESTRY_AUTHORITY_NULLS["lens_process_isolation"] == (
        "six_distinct_supervised_local_process_receipts_only"
    )
    assert ancestry["authority_nulls"]["cognitive_isolation"] == "unavailable"
    assert ancestry["authority_nulls"]["semantic_isolation"] == "unavailable"


@pytest.mark.expensive
def test_full_ym_ancestry_reopens_exact_july_21_capture_and_method_lane(
    ym_ancestry: dict[str, Any],
) -> None:
    ancestry = ym_ancestry["ancestry"]
    assert (
        validate_ym21_conceptual_ancestry_v3(
            ancestry, present_use_at=YM_PRESENT_USE
        )
        == ancestry
    )
    stages = {
        row["stage_id"]: row["artifact"] for row in ancestry["stages"]
    }
    literature = stages["current_bounded_literature"]
    assert literature["capture"]["capture_id"] == YM21_CAPTURE_ID
    assert literature["capture_descriptor"]["sha256"] == YM21_CAPTURE_SHA256
    assert (
        literature["currentness"]["latest_allowed_capture_date"]
        == YM21_LATEST_ALLOWED_CAPTURE_DATE
    )


def test_ym_rejects_july_22_capture_and_method_authority_escalation() -> None:
    future_capture = json.loads(YM_CAPTURE_PATH.read_bytes())
    future_capture["capture_started_at"] = "2026-07-22T08:00:00Z"
    future_capture["capture_completed_at"] = "2026-07-22T08:10:00Z"
    with pytest.raises(ContractError):
        build_ym21_bounded_current_literature_bundle(
            capture_bytes=canonical_json(future_capture),
            run_id=YM_RUN,
            state_version=YM_STATE,
            present_use_at="2026-07-22T08:11:00Z",
        )

    lane = build_ym21_adjacent_abstraction_method_lane()
    escalated = copy.deepcopy(lane)
    escalated["authority"]["direct_target_claim_authority"] = True
    escalated["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in escalated.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(
        YM21ConceptualAncestryAdapterError,
        match="adjacent_lane_contract_invalid",
    ):
        validate_ym21_adjacent_abstraction_method_lane(escalated)


@pytest.mark.expensive
def test_same_cycle_proof_and_experiment_inputs_remain_excluded(
    generic_ancestry: dict[str, Any],
) -> None:
    args = generic_ancestry["build_arguments"]
    ancestry = generic_ancestry["ancestry"]
    with pytest.raises(
        ConceptualAncestryV3Error, match="same_cycle_experiment_forbidden"
    ):
        validate_conceptual_ancestry_cycle_binding(
            ancestry,
            target_id=args["target_id"],
            run_id=args["run_id"],
            source_state_version=args["source_state_version"],
            parent_reflection_packet=args["parent_reflection_packet"],
            synthesis_packet=args["synthesis_packet"],
            parent_adjudication_evidence=args[
                "parent_adjudication_evidence"
            ],
            final_adjudication_evidence=args[
                "final_adjudication_evidence"
            ],
            present_use_at=GENERIC_PRESENT_USE,
            experiment_specs=[{"experiment_id": "same-cycle-forbidden"}],
        )

    proof_args = copy.deepcopy(args)
    proof_packet = proof_args["parent_reflection_packet"]
    proof_packet["conceptual_systems"][0]["lifecycle_state"] = "proof_ready"
    proof_packet["packet_digest"] = canonical_digest(
        {
            key: value
            for key, value in proof_packet.items()
            if key != "packet_digest"
        }
    )
    with pytest.raises(ContractError):
        build_conceptual_ancestry_v3(**proof_args)
