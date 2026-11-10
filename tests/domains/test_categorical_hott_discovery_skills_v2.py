# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executable, receipt-bound tests for category/HoTT conceptual discovery v2."""

from __future__ import annotations

import copy
from functools import lru_cache
import json
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import canonical_digest, stable_identifier
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.literature import (
    LANE_TYPES,
    assimilate_literature,
    run_frontier_literature_cycle,
)
from skills.common.abstraction_discovery_validation import (
    AbstractionValidationError,
    YM_CARRIER_STATUS_DERIVATION_INVALID,
    YM_CONTINUUM_AUTHORITY_REQUIRED,
    YM_CORRECTION_COVERAGE_INVALID,
    YM_EVIDENCE_INFERENCE_INVALID,
    YM_QUANTIFIER_CONTRACT,
    YM_CHANGED_STRUCTURES_INVALID,
    YM_STRUCTURE_CONTRACTS,
    YM_STRUCTURE_IDS,
    _failure_witness_identifier_set,
    _forge_model_identifier_set,
    _theory_atlas_binding,
    build_physics_handback,
    build_ym_preservation_contract,
    forge_subject_digest,
    literature_pressure_digest,
    validate_forge_packet,
    validate_ym_bridge,
    ym_bridge_subject_digest,
)
from skills.common.theory_atlas_defect_compiler import (
    COMPLETION_KINDS,
    MEANING_DIMENSIONS,
    REDESCRIPTION_OPERATORS,
    REFLECTION_LENSES,
    REPAIR_LADDER,
    compile_theory_atlas_defect_packet,
    validate_theory_atlas_defect_packet,
)
from skills.common.abstraction_parallel_evaluation import (
    AbstractionEvaluationError,
    _build_aggregates,
    _build_task_clusters,
    _evaluation_common_input_digest,
    blinded_structural_score,
    run_abstraction_parallel_evaluation,
    validate_abstraction_evaluation_failure_evidence,
    validate_abstraction_parallel_evaluation,
)
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    HOTT_INVERSE_BASE_BOUNDARY_INVALID,
    build_category_model_and_witness,
    build_hott_model_and_witness,
    build_negative_witness,
    build_physical_diagram_and_witness,
    validate_hott_model,
)
from skills.common.formal_dependency_authority import (
    build_formal_dependency_authority,
)
from skills.common.ym_abstraction_calibrations import (
    run_ym_calibration_matrix,
    validate_ym_calibration,
)
from skills.common.discovery_lens_heuristic import (
    build_categorical_pathway_heuristic,
    build_hott_pathway_heuristic,
)


ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads(
    (ROOT / "tests/fixtures/categorical_hott_discovery/cases.json").read_text(encoding="utf-8")
)
GENERIC_TARGET = "representational-transport-target"
YM_TARGET = "yang-mills-existence-and-mass-gap-target"


def _atlas_singleton_map(
    map_id: str,
    domain_set_id: str,
    codomain_set_id: str,
    source: str,
    target: str,
) -> dict:
    return {
        "map_id": map_id,
        "domain_set_id": domain_set_id,
        "codomain_set_id": codomain_set_id,
        "pairs": [{"source": source, "target": target}],
    }


def _atlas_finite_structure(kind: str) -> tuple[list[dict], list[dict]]:
    if kind == "factorization":
        elements = {"D": "d", "M": "m", "C": "c"}
        map_specs = (("f", "D", "M"), ("g", "M", "C"), ("h", "D", "C"))
    elif kind == "finite_representability":
        elements = {"HomX": "hx", "NatX": "nx", "HomY": "hy", "NatY": "ny"}
        map_specs = (
            ("phi_x", "HomX", "NatX"),
            ("phi_x_inverse", "NatX", "HomX"),
            ("phi_y", "HomY", "NatY"),
            ("phi_y_inverse", "NatY", "HomY"),
            ("hom_reindex", "HomX", "HomY"),
            ("nat_reindex", "NatX", "NatY"),
        )
    elif kind == "descent_gluing":
        elements = {
            "Global": "global",
            "LocalU": "local_u",
            "LocalV": "local_v",
            "Overlap": "overlap",
            "CompatiblePairs": "pair",
        }
        map_specs = (
            ("res_u", "Global", "LocalU"),
            ("res_v", "Global", "LocalV"),
            ("res_u_overlap", "LocalU", "Overlap"),
            ("res_v_overlap", "LocalV", "Overlap"),
            ("pair_left", "CompatiblePairs", "LocalU"),
            ("pair_right", "CompatiblePairs", "LocalV"),
            ("restrict_pair", "Global", "CompatiblePairs"),
            ("glue", "CompatiblePairs", "Global"),
        )
    elif kind == "pushout":
        elements = {"C": "c", "A": "a", "B": "b", "P": "p", "Q": "q"}
        map_specs = (
            ("c_to_a", "C", "A"),
            ("c_to_b", "C", "B"),
            ("a_to_p", "A", "P"),
            ("b_to_p", "B", "P"),
            ("a_to_q", "A", "Q"),
            ("b_to_q", "B", "Q"),
            ("p_to_q", "P", "Q"),
        )
    elif kind == "adjunction_naturality":
        elements = {
            "LH00": "lh00",
            "RH00": "rh00",
            "LH10": "lh10",
            "RH10": "rh10",
            "LH01": "lh01",
            "RH01": "rh01",
        }
        map_specs = (
            ("adj00", "LH00", "RH00"),
            ("adj00_inverse", "RH00", "LH00"),
            ("adj10", "LH10", "RH10"),
            ("adj10_inverse", "RH10", "LH10"),
            ("adj01", "LH01", "RH01"),
            ("adj01_inverse", "RH01", "LH01"),
            ("left_domain", "LH00", "LH10"),
            ("right_domain", "RH00", "RH10"),
            ("left_codomain", "LH00", "LH01"),
            ("right_codomain", "RH00", "RH01"),
        )
    elif kind == "lifting_obstruction":
        sets = [
            {"set_id": "A", "elements": ["a"]},
            {"set_id": "B", "elements": ["b0", "b1"]},
            {"set_id": "X", "elements": ["x"]},
            {"set_id": "Y", "elements": ["y0", "y1"]},
        ]
        maps = [
            _atlas_singleton_map("i", "A", "B", "a", "b0"),
            _atlas_singleton_map("u", "A", "X", "a", "x"),
            _atlas_singleton_map("p", "X", "Y", "x", "y0"),
            {
                "map_id": "v",
                "domain_set_id": "B",
                "codomain_set_id": "Y",
                "pairs": [
                    {"source": "b0", "target": "y0"},
                    {"source": "b1", "target": "y1"},
                ],
            },
        ]
        return sets, maps
    else:
        raise AssertionError(f"unregistered fixture completion kind: {kind}")

    sets = [
        {"set_id": set_id, "elements": [element]}
        for set_id, element in elements.items()
    ]
    maps = [
        _atlas_singleton_map(
            map_id,
            domain_set_id,
            codomain_set_id,
            elements[domain_set_id],
            elements[codomain_set_id],
        )
        for map_id, domain_set_id, codomain_set_id in map_specs
    ]
    return sets, maps


def _test_theory_atlas_spec(target_id: str) -> dict:
    evidence = {
        "evidence_id": "atlas.e1",
        "source_path": "tests/domains/test_categorical_hott_discovery_skills_v2.py",
        "exact_claim": "Synthetic finite data exercises the exact theory-atlas compiler contract.",
    }
    evidence["content_digest"] = canonical_digest(evidence)
    signature = {
        "objects": ["source", "target"],
        "morphisms": [
            {"symbol": "arrow", "source_object": "source", "target_object": "target"}
        ],
        "predicates": ["predicate"],
    }

    def fragment(fragment_id: str) -> dict:
        return {
            "fragment_id": fragment_id,
            "signature": copy.deepcopy(signature),
            "axioms": ["The declared arrow is typed from source to target."],
            "models": ["One finite fixture model is declared."],
            "observables": ["One finite replay bit is observed."],
            "scope": {
                "domain": "finite test authority",
                "regime": "fixture-only replay",
                "quantifiers": ["For every member of the declared finite carriers."],
                "exclusions": ["No theorem or physics authority is granted."],
            },
            "evidence_refs": ["atlas.e1"],
            "meaning_profile": {
                dimension: {
                    "statement": f"{dimension} is explicitly fixture-bound.",
                    "evidence_refs": ["atlas.e1"],
                }
                for dimension in MEANING_DIMENSIONS
            },
        }

    total_symbol_map = [
        {"source_symbol": "source", "target_symbol": "source", "symbol_kind": "object"},
        {"source_symbol": "target", "target_symbol": "target", "symbol_kind": "object"},
        {"source_symbol": "arrow", "target_symbol": "arrow", "symbol_kind": "morphism"},
        {
            "source_symbol": "predicate",
            "target_symbol": "predicate",
            "symbol_kind": "predicate",
        },
    ]
    relations = [
        {
            "relation_id": relation_kind,
            "relation_kind": relation_kind,
            "source_fragment_id": "fragment0",
            "target_fragment_id": "fragment1",
            "total": True,
            "symbol_map": copy.deepcopy(total_symbol_map),
            "unmapped_source_symbols": [],
            "preserved_structure": ["Every typed fixture symbol is preserved."],
            "failure_condition": "Fail if any typed fixture symbol is unmapped.",
            "evidence_refs": ["atlas.e1"],
        }
        for relation_kind in ("horizontal", "vertical")
    ]
    relations.append(
        {
            "relation_id": "partial",
            "relation_kind": "partial",
            "source_fragment_id": "fragment0",
            "target_fragment_id": "fragment1",
            "total": False,
            "symbol_map": [copy.deepcopy(total_symbol_map[-1])],
            "unmapped_source_symbols": ["source", "target", "arrow"],
            "preserved_structure": ["Only the declared predicate is mapped."],
            "failure_condition": "Fail if the declared partial map is totalized.",
            "evidence_refs": ["atlas.e1"],
        }
    )
    diagram = {
        "diagram_id": "diagram",
        "diagram_kind": "comparison_square",
        "nodes": [
            {"node_id": "n0", "fragment_id": "fragment0", "object_symbol": "source"},
            {"node_id": "n1", "fragment_id": "fragment0", "object_symbol": "target"},
        ],
        "arrows": [
            {
                "arrow_id": arrow_id,
                "source_node_id": "n0",
                "target_node_id": "n1",
                "arrow_type": "intra_fragment_morphism",
                "symbol_ref": "arrow",
            }
            for arrow_id in ("a1", "a2")
        ],
        "higher_cells": [
            {
                "cell_id": "cell",
                "cell_kind": "coherence_obligation",
                "source_path": ["a1"],
                "target_path": ["a2"],
                "source_node_id": "n0",
                "target_node_id": "n1",
                "status": "open",
                "evidence_refs": ["atlas.e1"],
            }
        ],
    }
    defect_types = {
        "factorization": "factorization",
        "finite_representability": "representability",
        "descent_gluing": "descent",
        "pushout": "coherence",
        "adjunction_naturality": "adjunction",
        "lifting_obstruction": "obstruction",
    }
    structures = {
        "factorization": ("arrow", "morphism"),
        "finite_representability": ("predicate", "predicate"),
        "descent_gluing": ("predicate", "predicate"),
        "pushout": ("source", "object"),
        "adjunction_naturality": ("arrow", "morphism"),
        "lifting_obstruction": ("target", "object"),
    }
    defects = []
    completion_specs = []
    return_squares = []
    for index, kind in enumerate(COMPLETION_KINDS):
        defect_id = f"defect{index}"
        candidate_id = f"candidate{index}"
        structure_id, structure_kind = structures[kind]
        defects.append(
            {
                "defect_id": defect_id,
                "defect_type": defect_types[kind],
                "subject_fragment_id": "fragment0",
                "structure_id": structure_id,
                "structure_kind": structure_kind,
                "diagram_id": "diagram",
                "completion_kind": kind,
                "exact_failure": f"The {kind} completion is absent from the source fragment.",
                "evidence_refs": ["atlas.e1"],
                "metaphor_guard": {
                    "typed_diagram_required": True,
                    "executable_obligation_required": True,
                    "terminology_only": False,
                },
            }
        )
        sets, maps = _atlas_finite_structure(kind)
        completion_specs.append(
            {
                "candidate_id": candidate_id,
                "defect_id": defect_id,
                "completion_kind": kind,
                "subject_fragment_id": "fragment0",
                "structure_id": structure_id,
                "diagram_id": "diagram",
                "claim": f"Finite {kind} replay candidate.",
                "obligation": {
                    "obligation_id": f"obligation{index}",
                    "obligation_type": kind,
                    "subject_fragment_id": "fragment0",
                    "structure_id": structure_id,
                    "diagram_id": "diagram",
                    "evidence_refs": ["atlas.e1"],
                    "sets": sets,
                    "maps": maps,
                    "checks": [
                        {
                            "check_id": f"check{index}",
                            "check_kind": kind,
                            "map_ids": [row["map_id"] for row in maps],
                            "set_ids": [row["set_id"] for row in sets],
                            "expected": True,
                            "observed": True,
                        }
                    ],
                },
            }
        )
        exact = index % 2 == 0
        return_squares.append(
            {
                "square_id": f"square{index}",
                "mode": "exact" if exact else "approximate",
                "subject_fragment_id": "fragment0",
                "completion_candidate_id": candidate_id,
                "abstract_path": [
                    {
                        "step_id": f"abstract{index}",
                        "input_values": [0.0],
                        "output_values": [1.0],
                    }
                ],
                "concrete_path": [
                    {
                        "step_id": f"concrete{index}",
                        "input_values": [0.0],
                        "output_values": [1.0 if exact else 1.05],
                    }
                ],
                "error_bound": 0.0 if exact else 0.1,
                "changed_structure_ids": [structure_id],
            }
        )

    return {
        "target_id": target_id,
        "evidence_registry": [evidence],
        "theory_fragments": [fragment("fragment0"), fragment("fragment1")],
        "relations": relations,
        "diagrams": [diagram],
        "defects": defects,
        "structured_failures": [
            {
                "failure_id": f"failure{attempt}",
                "defect_id": "defect0",
                "structure_id": "arrow",
                "attempt": attempt,
                "failure_class": "completion_failure",
                "exact_failure": f"Completion attempt {attempt} failed on the same structure.",
                "evidence_refs": ["atlas.e1"],
            }
            for attempt in (1, 2)
        ],
        "representation_mutation": {
            "status": "candidate_pending_human",
            "trigger_failure_ids": ["failure1", "failure2"],
            "source_grammar": {
                "objects": ["old_object"],
                "morphisms": ["old_morphism"],
                "rules": ["old_rule"],
            },
            "proposed_grammar": {
                "objects": ["new_object"],
                "morphisms": ["new_morphism"],
                "rules": ["new_rule"],
            },
            "migration_map": [
                {
                    "source_symbol": f"old_{kind}",
                    "target_symbol": f"new_{kind}",
                    "symbol_kind": kind,
                    "preservation_status": status,
                }
                for kind, status in (
                    ("object", "preserved"),
                    ("morphism", "approximated"),
                    ("rule", "lost"),
                )
            ],
            "information_loss": ["One old rule is not promoted."],
            "new_expressivity": ["The new grammar names the missing completion."],
            "human_acceptance_gate": {
                "required": True,
                "decision": "pending",
                "accepted": False,
                "execution_authorized": False,
                "authority": "human_only",
            },
        },
        "return_squares": return_squares,
        "repair_attempts": {
            repair: {
                "outcome": "failed",
                "reason": f"{repair} does not close the typed defect.",
                "evidence_refs": ["atlas.e1"],
            }
            for repair in REPAIR_LADDER
        },
        "reflection_mutations": {
            lens: {
                "source_statement": "The source fragment lacks a typed completion.",
                "mutated_statement": (
                    f"The {lens} lens changes which dependency is treated as primitive."
                ),
                "changed_commitments": [f"{lens} changes one declared commitment."],
                "operator_refs": [REDESCRIPTION_OPERATORS[index % 12]],
                "new_question": f"Which {lens} dependency must become explicit?",
                "new_failure_mode": f"A {lens} mismatch can survive finite replay.",
            }
            for index, lens in enumerate(REFLECTION_LENSES)
        },
        "operator_decisions": {
            operator: {
                "status": "applied",
                "reason": f"{operator} probes one registered completion.",
                "candidate_refs": [f"candidate{index % 6}"],
            }
            for index, operator in enumerate(REDESCRIPTION_OPERATORS)
        },
        "completion_specs": completion_specs,
    }


@lru_cache(maxsize=None)
def _compiled_test_theory_atlas_authority(target_id: str) -> tuple[dict, dict]:
    atlas = compile_theory_atlas_defect_packet(_test_theory_atlas_spec(target_id))
    receipt = validate_theory_atlas_defect_packet(atlas)
    return atlas, receipt


def _bind_test_theory_atlas_authority(packet: dict) -> dict:
    cached_atlas, cached_receipt = _compiled_test_theory_atlas_authority(
        packet["target_id"]
    )
    atlas = copy.deepcopy(cached_atlas)
    receipt = copy.deepcopy(cached_receipt)
    pressure_ids = sorted(
        {
            queue_id
            for row in packet["source_pressure"]["frontier_rows"]
            for queue_id in row["queue_ids"]
        }
    )
    model_ids = sorted(_forge_model_identifier_set(packet))
    witness_ids = sorted(_failure_witness_identifier_set(packet["failure_witness"]))
    obligation_ids = sorted(
        row["obligation_id"]
        for row in packet["translation"]["observable_or_theorem_obligations"]
    )
    candidates_by_defect = {
        row["defect_id"]: row for row in atlas["completion_candidates"]
    }
    squares_by_candidate = {
        row["completion_candidate_id"]: row for row in atlas["return_squares"]
    }
    rows = []
    for defect in atlas["defects"]:
        candidate = candidates_by_defect[defect["defect_id"]]
        square = squares_by_candidate[candidate["candidate_id"]]
        rows.append(
            {
                "defect_id": defect["defect_id"],
                "completion_candidate_id": candidate["candidate_id"],
                "return_square_ids": [square["square_id"]],
                "source_pressure_queue_ids": list(pressure_ids),
                "forge_model_refs": list(model_ids),
                "failure_witness_refs": list(witness_ids),
                "translation_obligation_ids": list(obligation_ids),
            }
        )
    crosswalk = {
        "atlas_packet_id": atlas["packet_id"],
        "atlas_packet_digest": atlas["content_digest"],
        "atlas_validation_receipt_id": receipt["validation_receipt_id"],
        "atlas_validation_receipt_digest": receipt["content_digest"],
        "target_id": packet["target_id"],
        "lens": packet["lens"],
        "source_pressure_digest": canonical_digest(packet["source_pressure"]),
        "rows": rows,
        "authority_class": "finite_pre_forge_structural_pressure_only",
        "automatic_promotion_authorized": False,
    }
    crosswalk["content_digest"] = canonical_digest(crosswalk)
    packet["theory_atlas_packet"] = atlas
    packet["theory_atlas_validation_receipt"] = receipt
    packet["theory_atlas_crosswalk"] = crosswalk
    return _theory_atlas_binding(atlas, receipt, crosswalk)


def _live_basis(target_id: str, cases: list[dict]) -> dict:
    theory_digest = canonical_digest({"target": target_id, "state": "typed-abstraction-v2"})
    request = {
        "target_id": target_id,
        "claim_scope": "category and HoTT conceptual pressures",
        "theory_state_digest": theory_digest,
        "coverage_cutoff": "2026-07-22",
        "coverage_limits": ["Fixture live adapters cover only the exact held-out conceptual tasks."],
        "search_lanes": [
            {
                "lane_type": lane_type,
                "queries": [f"{target_id} exact {lane_type.replace('_', ' ')}"],
                "inclusion_policy": "Include exact target-scoped primary results.",
                "exclusion_policy": "Exclude target mismatch and duplicate versions.",
            }
            for lane_type in LANE_TYPES
        ],
    }
    providers = {}
    for index, lane_type in enumerate(LANE_TYPES):
        def provider(_request: dict, index: int = index, lane_type: str = lane_type) -> dict:
            return {
                "provider": f"fixture-provider-{lane_type}",
                "index": f"fixture-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": "2026-07-22",
                "sources": [{
                    "work_identity": f"{target_id}-work-{lane_type}",
                    "title": f"Primary target source {index} for {lane_type}",
                    "authors": [f"Author {index}"],
                    "publication_date": str(2020 + index),
                    "source_version": "v1",
                    "source_type": "primary",
                    "url": f"https://example.test/{target_id}/{lane_type}",
                    "correction_status": "none_known",
                    "decision_relevant": True,
                    "claims": [f"Source {index} constrains one exact representational pressure."],
                    "limitations": [f"Source {index} is limited to one declared regime."],
                }],
            }
        providers[lane_type] = provider
    snapshot = run_frontier_literature_cycle(request, providers=providers)
    mappings = []
    for index, source in enumerate(snapshot["sources"]):
        mappings.append({
            "source_id": source["source_id"],
            "theory_object_ids": [f"pressure-map-{index}"],
            "object_kinds": ["concept", "mechanism"],
            "relation": "leaves_open",
            "exact_claim": source["claims"][0],
            "source_limitation": source["limitations"][0],
            "conceptual_change": f"Mapping {index} localizes a distinct held-out pressure without closing it.",
            "event_type": "spawn" if index == 0 else "justified_no_change",
            "coverage_limits": snapshot["coverage_limits"],
            "confidence": "medium",
        })
    assimilation = assimilate_literature(
        snapshot, theory_state_digest=theory_digest, theory_mappings=mappings
    )
    portfolio = build_demo_high_risk_portfolio(snapshot)
    runtime_cases = [{**copy.deepcopy(case), "target_id": target_id, "preferred_lens": case["lens"]} for case in cases]
    report = run_abstraction_parallel_evaluation(
        literature_snapshot=snapshot,
        assimilation_packet=assimilation,
        source_portfolio=portfolio,
        cases=runtime_cases,
    )
    return {"snapshot": snapshot, "assimilation": assimilation, "portfolio": portfolio, "report": report}


@pytest.fixture(scope="module")
def generic_basis() -> dict:
    return _live_basis(GENERIC_TARGET, CASES)


@pytest.fixture(scope="module")
def ym_basis() -> dict:
    return _live_basis(YM_TARGET, CASES)


def _pressure_rows(case: dict) -> list[dict]:
    prefix = case["case_id"]
    if case["lens"] == "categorical":
        return [
            {
                "breakthrough_family": f"{prefix} staged map square",
                "queue_ids": [f"{prefix}.q1", f"{prefix}.q2"],
                "required_move": f"Compile the {case['pressure_id']} translation through a typed factor.",
                "abstraction_required": "A universal factor with explicit source and target arrows is required.",
                "minimal_theorem_shape": f"A factor theorem isolates {case['obligation_id']} under composition.",
                "obstruction_class": "formula-size-transport structural failure",
                "search_modes": ["typed compilation square", "universal factor"],
                "sample_theorem_targets": [case["obligation_statement"]],
            },
            {
                "breakthrough_family": f"{prefix} independent map relay",
                "queue_ids": [f"{prefix}.q3"],
                "required_move": "Compare two staged arrows after the same exact source constraint.",
                "abstraction_required": "A mediating factor must expose the first unequal composite.",
                "minimal_theorem_shape": "The two typed composites share endpoints and differ at one named step.",
                "obstruction_class": "local-reduction-barrier in staged compilation",
                "search_modes": ["arrow composition", "mediating object"],
                "sample_theorem_targets": [case["falsifier"]],
            },
        ]
    return [
        {
            "breakthrough_family": f"{prefix} higher sameness problem",
            "queue_ids": [f"{prefix}.q1"],
            "required_move": f"Separate strict identity from equivalent presentations of {case['pressure_id']}.",
            "abstraction_required": "Explicit equivalence data and a two-level coherence witness are required.",
            "minimal_theorem_shape": f"An equivalent substitution preserves {case['obligation_id']} only with a two-path.",
            "obstruction_class": "equivalent-but-not-identical boundary",
            "search_modes": ["identity level audit", "coherence cell"],
            "sample_theorem_targets": [case["obligation_statement"]],
        },
        {
            "breakthrough_family": f"{prefix} predicate substitution problem",
            "queue_ids": [f"{prefix}.q2"],
            "required_move": "Track an invariant predicate across equivalent terms without declaring them identical.",
            "abstraction_required": "A higher coherence cell compares the two predicate substitutions.",
            "minimal_theorem_shape": "The missing two-path is retained before any truncation step.",
            "obstruction_class": "identity-equivalence confusion",
            "search_modes": ["predicate substitution", "higher coherence"],
            "sample_theorem_targets": [case["falsifier"]],
        },
    ]


def _heuristic(lens: str, rows: list[dict]) -> dict:
    full = build_categorical_pathway_heuristic(rows) if lens == "categorical" else build_hott_pathway_heuristic(rows)
    return {key: full[key] for key in (
        "lens_id", "recommended", "score", "threshold", "active_criteria", "active_anti_triggers"
    )}


def _literature_basis(basis: dict, pressure_payload: object) -> dict:
    snapshot = basis["snapshot"]
    assimilation = basis["assimilation"]
    mapping_ids = [row["mapping_id"] for row in assimilation["theory_mappings"]]
    snapshot_validator = next(row for row in snapshot["validator_receipts"] if row["status"] == "passed")
    return {
        "target_id": snapshot["target_id"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "search_completed_at": snapshot["search_completed_at"],
        "coverage_cutoff": snapshot["coverage_cutoff"],
        "freshness_status": "current",
        "target_match": "pass",
        "active_investment_gate": "pass",
        "snapshot_validator_receipt": {
            "validator_id": "target-literature-snapshot-validator.v1",
            "receipt_id": snapshot_validator["receipt_id"],
            "target_id": snapshot["target_id"],
            "validated_digest": snapshot["content_digest"],
            "status": "passed",
        },
        "assimilation_packet_id": assimilation["packet_id"],
        "assimilation_digest": assimilation["content_digest"],
        "assimilation_input_snapshot_digest": snapshot["content_digest"],
        "hypothesis_rebase_status": "current",
        "source_mapping_ids": mapping_ids,
        "pressure_mapping_digest": literature_pressure_digest(
            source_mapping_ids=mapping_ids, pressure_payload=pressure_payload
        ),
        "assimilation_validator_receipt": {
            "validator_id": "literature-assimilation-validator.v1",
            "receipt_id": stable_identifier("assimilation-validator", assimilation["content_digest"]),
            "target_id": snapshot["target_id"],
            "validated_assimilation_digest": assimilation["content_digest"],
            "validated_snapshot_digest": snapshot["content_digest"],
            "status": "passed",
        },
    }


def _certificate(witness: dict, result: str) -> dict:
    evidence = witness["evidence"]
    core = {key: copy.deepcopy(value) for key, value in witness.items() if key != "evidence"}
    witness_digest = canonical_digest(core)
    evidence_digest = canonical_digest(evidence)
    return {
        "certificate_id": stable_identifier("witness-certificate", witness["diagram_id"], result),
        "kind": "symbolic_normal_form",
        "result": result,
        "witness_digest": witness_digest,
        "evidence_digest": evidence_digest,
        "validator_receipt": {
            "validator_id": "typed-path-certificate-validator.v1",
            "receipt_id": stable_identifier("witness-validator", witness_digest, evidence_digest),
            "validated_witness_digest": witness_digest,
            "validated_evidence_digest": evidence_digest,
            "status": "passed",
        },
    }


def _witness(prefix: str, kind: str, namespace: str, source: str, target: str,
             left: list[str], right: list[str], left_comp: str, right_comp: str) -> dict:
    payload = {"left_normal_form": left, "right_normal_form": right, "common_endpoints": [source, target]}
    evidence = [{
        "evidence_id": f"{prefix}.evidence",
        "artifact_path": "tests/fixtures/categorical_hott_discovery/cases.json",
        "claim": "Direct symbolic normalization yields distinct composites with common endpoints.",
        "payload": payload,
        "content_digest": canonical_digest(payload),
    }]
    result = {
        "witness_kind": kind,
        "diagram_id": f"{prefix}.diagram",
        "step_namespace": namespace,
        "source_id": source,
        "target_id": target,
        "left_path_ids": left,
        "right_path_ids": right,
        "left_composite_id": left_comp,
        "right_composite_id": right_comp,
        "exact_obstruction": "The two checked normal forms are distinct under the frozen boundary conditions.",
        "boundary_conditions": ["The source and target identifiers are exactly shared.", "Target semantics and quantifiers remain fixed."],
        "exact": True,
        "evidence": evidence,
    }
    result["certificate"] = _certificate(result, "noncommuting" if kind == "noncommutativity" else "noncoherent")
    return result


def _category_model(prefix: str, obligation_id: str) -> tuple[dict, dict]:
    return build_category_model_and_witness(prefix, obligation_id)


def _hott_model(prefix: str, obligation_id: str) -> tuple[dict, dict]:
    return build_hott_model_and_witness(prefix, obligation_id)


def _ablation(report: dict, arm: str) -> dict:
    aggregates = {row["arm"]: row for row in report["aggregates"]}
    condition, baseline = aggregates[arm], aggregates["no_abstraction"]
    paired = condition["paired_differences_vs_no_abstraction"]
    diagnostics = copy.deepcopy(paired["diagnostics"])
    return {
        "same_target_and_evidence": True,
        "evaluation_report": {
            "schema_version": report["schema_version"], "evaluation_id": report["evaluation_id"],
            "content_digest": report["content_digest"], "target_id": report["target_id"],
            "case_suite_id": report["case_suite_id"],
            "literature_snapshot_digest": report["literature_snapshot_digest"], "assimilation_digest": report["assimilation_digest"],
            "condition_arm": arm, "baseline_arm": "no_abstraction", "repetitions_completed": paired["n_matched_repetitions"],
            "minimum_required_matched_repetitions": paired["minimum_required_matched_repetitions"],
            "calibration_status": paired["status"],
            "runtime_portfolio_digest": report["runtime_portfolio_digest"], "evaluator_receipt_id": report["evaluator_evidence"]["receipt_id"],
            "partial_failure_status": "siblings_preserved", "task_cluster_count": report["task_clustered_reporting"]["task_count"],
            "population_inference_authorized": False, "external_human_status": "unavailable",
        },
        "with_abstraction": copy.deepcopy(condition["descriptive_mean_scorecard"]),
        "without_abstraction": copy.deepcopy(baseline["descriptive_mean_scorecard"]),
        "paired_repeatability_diagnostics": diagnostics,
        "net_new_value": None if diagnostics is None else round(sum(diagnostics[field]["descriptive_mean"] for field in diagnostics), 6),
        "frozen_suite_refinement_signal": paired["status"] == "sufficient_internal_calibration" and condition["internal_refinement_eligible"],
        "changed_investment_decision": False,
    }


def _audit_receipt(skill: str, target: str, subject: str, output: dict) -> dict:
    digest = canonical_digest(output)
    return {
        "skill_id": skill, "receipt_id": stable_identifier("audit", skill, target, subject),
        "target_id": target, "subject_digest": subject, "output": output, "output_digest": digest,
        "validator_receipt": {"validator_id": f"{skill}-output-validator.v1", "receipt_id": stable_identifier("audit-validator", skill, digest), "validated_output_digest": digest, "status": "passed"},
    }


def _bind_forge_audits(packet: dict) -> None:
    subject = forge_subject_digest(packet)
    translation = packet["translation"]
    fit = {"verdict": "candidate_advantage", "incumbent_gap": "The incumbent route does not localize either parallel composite.", "candidate_gain": "The candidate names typed endpoints, composites, and one correction burden.", "remaining_gap": "The universal or coherence obligation remains mathematically open.", "failure_case": "Demote if a matched control localizes the same burden with equal specificity."}
    same = {"source_domain": packet["target_contract"]["mathematical_object"], "target_domain": packet["target_contract"]["mathematical_object"], "preserved_structures": packet["target_contract"]["preserved_invariants"], "changed_structures": ["Only representation-level structure and proof obligations change."], "certificate_status": "passed", "failure_case": "Reject any transfer that changes the frozen target or its quantifiers."}
    physical = None
    if packet["domain_kind"] == "physics":
        physical = {"physical_carrier": translation["physical_carrier"], "target_gate": "The exact physical carrier and target quantifiers remain independently frozen.", "obligation_ids": [row["obligation_id"] for row in translation["observable_or_theorem_obligations"]], "correction_test_id": translation["correction_test"]["test_id"], "essential_relevance": "high", "physical_reward": "high", "investment_decision": translation["decision"], "failure_case": "Demote if the abstraction only renames an existing physical estimate."}
    packet["audit_receipts"] = {
        "subject_digest": subject,
        "fit_gap": _audit_receipt("abstraction-fit-gap-auditor", packet["target_id"], subject, fit),
        "same_domain": _audit_receipt("proof-same-domain-transfer-certifier", packet["target_id"], subject, same),
        "physical_relevance": None if physical is None else _audit_receipt("physical-relevance-impact-auditor", packet["target_id"], subject, physical),
    }


def _forge_packet(case: dict, basis: dict) -> dict:
    report = basis["report"]
    rows = _pressure_rows(case)
    prefix = case["case_id"]
    model, witness = _category_model(prefix, case["obligation_id"]) if case["lens"] == "categorical" else _hott_model(prefix, case["obligation_id"])
    packet = {
        "schema_version": "5.0.0", "packet_id": f"packet.{prefix}", "target_id": report["target_id"],
        "domain_kind": case["domain_kind"], "lens": case["lens"],
        "dependency_authority": build_formal_dependency_authority(),
        "literature_basis": _literature_basis(basis, rows),
        "source_pressure": {"frontier_rows": rows, "heuristic": _heuristic(case["lens"], rows)},
        "target_contract": {"target_statement": case["target_statement"], "mathematical_object": case["mathematical_object"], "preserved_invariants": [case["preservation_condition"], "The exact target quantifiers remain unchanged."], "forbidden_target_changes": ["Do not replace the target by notation or analogy.", "Do not weaken universal quantifiers or erase operational distinctions."]},
        "categorical_model": model if case["lens"] == "categorical" else None,
        "hott_model": model if case["lens"] == "hott" else None,
        "failure_witness": witness,
        "translation": {
            "physical_carrier": case["physical_carrier"], "target_burden": case["obligation_statement"],
            "observable_or_theorem_obligations": [{"obligation_id": case["obligation_id"], "burden_kind": "both" if case["domain_kind"] == "physics" else "theorem", "statement": case["obligation_statement"], "enabled_by_abstraction": "Typed parallel composites expose a common endpoint and a certificate-checkable obstruction.", "control_status": "not_reached_without_abstraction", "status": "open"}],
            "correction_test": {"test_id": f"{prefix}.correction", "intervention": case["falsifier"], "expected_if_useful": "The typed witness predicts the first exact failed preservation obligation.", "expected_if_decorative": "The matched control localizes the same failure at lower or equal overhead.", "demotion_trigger": "Demote when task-clustered replay fails to improve two dimensions."},
            "elegance_only": False, "decision": "refine", "decision_rationale": "Internal calibration supports theory refinement but carries no investment authority.",
        },
        "value_ablation": _ablation(report, case["lens"]),
        "reuse_handoffs": {"upstream": ["reflective-conceptual-discovery"], "validators": ["abstraction-fit-gap-auditor", "proof-same-domain-transfer-certifier"] + (["physical-relevance-impact-auditor"] if case["domain_kind"] == "physics" else []), "downstream": ["reflective-theory-synthesizer"]},
        "epistemic_status": "concept_candidate", "evidence_citations": ["tests/fixtures/categorical_hott_discovery/cases.json"],
        "explicit_unknowns": ["The proposed universal property or coherence cell remains unproved."],
        "validation_handoff": "Run transitive semantic validation and domain review before any theory claim.",
    }
    atlas_binding = _bind_test_theory_atlas_authority(packet)
    packet["physics_handback"] = build_physics_handback(
        target_id=packet["target_id"], domain_kind=packet["domain_kind"],
        physical_carrier=packet["translation"]["physical_carrier"],
        burdens=packet["translation"]["observable_or_theorem_obligations"],
        correction_tests=[packet["translation"]["correction_test"]],
        failure_witness=packet["failure_witness"],
        theory_atlas_binding=atlas_binding,
    )
    _bind_forge_audits(packet)
    return packet


def test_real_parallel_factorial_is_complete_blind_and_failure_tolerant(generic_basis: dict) -> None:
    report = generic_basis["report"]
    result = validate_abstraction_parallel_evaluation(report)
    assert result["completed_outputs"] == 29
    assert result["minimum_retained_repetitions_per_arm"] == 5
    assert result["minimum_matched_repetitions_per_arm"] == 5
    assert result["calibration_status"] == "sufficient_internal_calibration"
    assert len(report["attempt_receipts"]) == 30
    assert {row["status"] for row in report["attempt_receipts"]} == {"completed", "failed"}
    assert report["dissent"]["retained_dissent_branch_ids"]
    assert report["dissent"]["contradiction_edges"]
    assert report["evaluator_evidence"]["external_human"]["status"] == "unavailable"
    assert report["decision_authority"]["investment_authorized"] is False
    assert report["evaluator_evidence"]["physics_value_authorized"] is False
    assert report["task_clustered_reporting"]["population_inference_authorized"] is False
    assert report["task_clustered_reporting"]["task_count"] == len(CASES)
    assert {row["control_kind"] for row in report["negative_control_outcomes"]} == {"decorative", "restatement", "sham"}
    assert all(row["all_zero"] for row in report["negative_control_outcomes"])
    assert "score_confidence_intervals" not in report["aggregates"][0]


def test_keyword_rich_and_equal_length_surface_controls_score_identically() -> None:
    evidence = {"typed_obligations": [{"localized": True}], "witness_checks": [{"certificate_bound": True}], "consequences": [{"derived_from_obligation": True}], "unification_links": [{"preserves_difference": True}], "correction_tests": [{"discriminating": True}]}
    rich = {"theory_delta": {"evaluation_evidence": evidence, "surface_form": "category equivalence coherence universal functor transport"}}
    plain = {"theory_delta": {"evaluation_evidence": evidence, "surface_form": "alpha beta gamma delta epsilon zeta"}}
    assert blinded_structural_score(rich) == blinded_structural_score(plain)


def test_arm_swaps_and_self_score_inflation_cannot_create_value_authority(generic_basis: dict) -> None:
    report = generic_basis["report"]
    assert report["decision_authority"]["status"] == "internal_calibration_refinement_only"
    inflated = copy.deepcopy(report)
    inflated["condition_outputs"][0]["scorecard"]["burden_closure"] = 5
    inflated["content_digest"] = canonical_digest({key: value for key, value in inflated.items() if key != "content_digest"})
    with pytest.raises(AbstractionEvaluationError, match="scorecard"):
        validate_abstraction_parallel_evaluation(inflated)
    swapped = copy.deepcopy(report)
    swapped["attempt_receipts"][0]["arm"], swapped["attempt_receipts"][6]["arm"] = swapped["attempt_receipts"][6]["arm"], swapped["attempt_receipts"][0]["arm"]
    swapped["content_digest"] = canonical_digest({key: value for key, value in swapped.items() if key != "content_digest"})
    with pytest.raises(AbstractionEvaluationError):
        validate_abstraction_parallel_evaluation(swapped)


@pytest.mark.parametrize("case", CASES, ids=lambda row: row["case_id"])
def test_case_specific_forge_packets_accept(case: dict, generic_basis: dict) -> None:
    packet = _forge_packet(case, generic_basis)
    result = validate_forge_packet(packet, expected_lens=case["lens"], parallel_evaluation=generic_basis["report"])
    assert result["status"] == "valid"
    assert result["repetitions"] >= 5
    receipt = result["formal_lens_execution_receipt"]
    assert result["validation_receipt_id"] == receipt["receipt_id"]
    assert receipt["authority_version"] == "2.0.0"
    assert receipt["packet_schema_version"] == "5.0.0"
    assert receipt["evaluation_schema_version"] == "4.0.0"
    assert receipt["dependency_authority_version"] == "2.0.0"
    assert receipt["literature_snapshot_digest"] == packet["literature_basis"]["snapshot_digest"]
    assert receipt["assimilation_digest"] == packet["literature_basis"]["assimilation_digest"]
    assert receipt["literature_projection_digest"] == canonical_digest(packet["literature_basis"])
    assert receipt["production_evidence_status"] == "not_attested"
    assert receipt["authority_distinct_evaluation_status"] == "unavailable"
    assert packet["physics_handback"]["continuum_authority"] is None
    assert (
        packet["physics_handback"][
            "authority_distinct_physics_value_evidence_status"
        ]
        == "unavailable"
    )
    assert not packet["physics_handback"][
        "authority_distinct_physics_value_evidence_ids"
    ]
    assert all(
        receipt[field] is False
        for field in (
            "theorem_authorized",
            "continuum_authorized",
            "physics_value_authorized",
            "investment_authorized",
            "cognitive_independence_authorized",
        )
    )


@pytest.mark.parametrize("case", CASES, ids=lambda row: row["case_id"])
def test_lens_selectivity_recommends_only_the_case_lens(case: dict) -> None:
    rows = _pressure_rows(case)
    category = build_categorical_pathway_heuristic(rows)["recommended"]
    hott = build_hott_pathway_heuristic(rows)["recommended"]
    assert (category, hott) == ((True, False) if case["lens"] == "categorical" else (False, True))


@pytest.mark.parametrize("mutation", [
    "dangling_endpoint", "ill_typed_composition", "missing_identity", "tampered_witness_evidence",
    "stale_literature_pressure", "forged_auditor_output", "tampered_parallel_report",
])
def test_categorical_referential_and_receipt_tampering_rejects(mutation: str, generic_basis: dict) -> None:
    case = next(row for row in CASES if row["lens"] == "categorical")
    packet = _forge_packet(case, generic_basis)
    report = generic_basis["report"]
    if mutation == "dangling_endpoint":
        packet["categorical_model"]["morphisms"][3]["codomain_id"] = "missing.object"
    elif mutation == "ill_typed_composition":
        packet["categorical_model"]["compositions"][0]["path_morphism_ids"].reverse()
    elif mutation == "missing_identity":
        packet["categorical_model"]["identities"].pop()
    elif mutation == "tampered_witness_evidence":
        packet["failure_witness"]["evidence"][0]["payload"]["left_normal_form"] = ["altered"]
    elif mutation == "stale_literature_pressure":
        packet["literature_basis"]["pressure_mapping_digest"] = canonical_digest({"stale": True})
    elif mutation == "forged_auditor_output":
        packet["audit_receipts"]["fit_gap"]["output"]["verdict"] = "no_advantage"
    else:
        report = copy.deepcopy(report)
        report["aggregates"][0]["descriptive_mean_scorecard"]["burden_closure"] = 5
    with pytest.raises((AbstractionValidationError, AbstractionEvaluationError)):
        validate_forge_packet(packet, parallel_evaluation=report)


@pytest.mark.parametrize(
    "attack",
    [
        "mapping_identity",
        "search_completion",
        "snapshot_receipt",
        "assimilation_identity",
    ],
)
def test_forge_literature_projection_replays_full_evaluation_artifacts(
    attack: str,
    generic_basis: dict,
) -> None:
    """A locally rehashed projection cannot relabel the executed literature."""

    case = next(row for row in CASES if row["lens"] == "categorical")
    packet = _forge_packet(case, generic_basis)
    basis = packet["literature_basis"]
    if attack == "mapping_identity":
        basis["source_mapping_ids"][0] = "source-theory-map.forged-current-source"
        basis["pressure_mapping_digest"] = literature_pressure_digest(
            source_mapping_ids=basis["source_mapping_ids"],
            pressure_payload=packet["source_pressure"]["frontier_rows"],
        )
    elif attack == "search_completion":
        basis["search_completed_at"] = "2026-07-22T00:00:00Z"
    elif attack == "snapshot_receipt":
        basis["snapshot_validator_receipt"]["receipt_id"] = (
            "snapshot-validator.forged-current-receipt"
        )
    else:
        basis["assimilation_packet_id"] = "literature-assimilation.forged-current"
    _bind_forge_audits(packet)
    with pytest.raises(
        AbstractionValidationError,
        match="literature basis",
    ):
        validate_forge_packet(
            packet,
            parallel_evaluation=generic_basis["report"],
        )


@pytest.mark.parametrize("mutation", ["bad_equivalence", "bad_transport", "low_coherence", "early_truncation", "wrong_witness_endpoint"])
def test_hott_referential_tampering_rejects(mutation: str, generic_basis: dict) -> None:
    case = next(row for row in CASES if row["lens"] == "hott")
    packet = _forge_packet(case, generic_basis)
    model = packet["hott_model"]
    if mutation == "bad_equivalence":
        model["equivalences"][0]["forward_map_id"] = model["equivalences"][0]["inverse_map_id"]
    elif mutation == "bad_transport":
        model["transports"][0]["target_type_id"] = model["types"][2]["type_id"]
    elif mutation == "low_coherence":
        model["coherence_cells"][0]["level"] = 1
    elif mutation == "early_truncation":
        model["truncation_policy"]["retained_through_level"] = 1
    else:
        packet["failure_witness"]["target_id"] = model["types"][1]["type_id"]
    with pytest.raises(AbstractionValidationError):
        validate_forge_packet(packet, parallel_evaluation=generic_basis["report"])


def _rebuild_ym_preservation(bridge: dict) -> None:
    """Re-derive every preservation artifact after an admissible source change."""

    bridge.update(
        build_ym_preservation_contract(
            upstream_packet_bindings=bridge["upstream_packet_bindings"],
            failure_witness=bridge["failure_witness"],
            calibration_matrix=bridge["calibration_matrix"],
            correction_tests=bridge["correction_tests"],
            carrier_translations=bridge["carrier_translations"],
        )
    )
    bridge["physics_handback"] = build_physics_handback(
        target_id=bridge["target_id"], domain_kind="physics",
        physical_carrier=bridge["carrier_translations"][0]["physical_carrier"],
        burdens=bridge["theorem_obligations"], correction_tests=bridge["correction_tests"],
        failure_witness=bridge["failure_witness"], target_contract=bridge["target_contract"],
        preservation_transfer=bridge["same_domain_transfer"],
        quantifier_contract=bridge["quantifier_contract"],
        evidence_registry=bridge["evidence_registry"],
        carrier_translations=bridge["carrier_translations"],
        continuum_authority=bridge["continuum_authority"],
    )
    if bridge.get("literature_basis"):
        pressure = {
            "carrier_translations": bridge["carrier_translations"],
            "theorem_obligations": bridge["theorem_obligations"],
        }
        bridge["literature_basis"]["pressure_mapping_digest"] = literature_pressure_digest(
            source_mapping_ids=bridge["literature_basis"]["source_mapping_ids"],
            pressure_payload=pressure,
        )


def _ym_bridge(ym_basis: dict) -> tuple[dict, list[dict]]:
    cat_case = {**next(row for row in CASES if row["lens"] == "categorical" and row["domain_kind"] == "physics"), "target_id": YM_TARGET}
    hott_case = {**next(row for row in CASES if row["lens"] == "hott" and row["domain_kind"] == "physics"), "target_id": YM_TARGET}
    cat = _forge_packet(cat_case, ym_basis)
    hott = _forge_packet(hott_case, ym_basis)
    cat_result = validate_forge_packet(cat, parallel_evaluation=ym_basis["report"])
    hott_result = validate_forge_packet(hott, parallel_evaluation=ym_basis["report"])
    bindings = []
    for packet, result in ((cat, cat_result), (hott, hott_result)):
        model = packet["categorical_model"] if packet["lens"] == "categorical" else packet["hott_model"]
        bindings.append({"packet_id": packet["packet_id"], "packet_digest": result["packet_digest"], "lens": packet["lens"], "model_digest": canonical_digest(model), "witness_certificate_digest": canonical_digest(packet["failure_witness"]["certificate"]), "validation_receipt_id": result["validation_receipt_id"], "formal_lens_execution_receipt": result["formal_lens_execution_receipt"]})
    prefix = "ym.bridge"
    physical_diagram, witness = build_physical_diagram_and_witness(prefix)
    a, b, c = f"{prefix}.A", f"{prefix}.B", f"{prefix}.C"
    steps = [
        {"step_id": f"{prefix}.cutoff-first", "kind": "morphism", "domain_id": a, "codomain_id": b, "physical_map": "Remove the regulator on the declared observable core with physical normalization fixed."},
        {"step_id": f"{prefix}.extend-second", "kind": "morphism", "domain_id": b, "codomain_id": c, "physical_map": "Extend the continuum observable core after regulated comparison estimates close."},
        {"step_id": f"{prefix}.extend-first", "kind": "morphism", "domain_id": a, "codomain_id": b, "physical_map": "Extend the regulated observable core before removing the cutoff."},
        {"step_id": f"{prefix}.cutoff-second", "kind": "morphism", "domain_id": b, "codomain_id": c, "physical_map": "Remove the cutoff after core extension with limit order recorded."},
        {"step_id": f"{prefix}.left-result", "kind": "morphism", "domain_id": a, "codomain_id": c, "physical_map": "The declared cutoff-then-extension composite on physical observables."},
        {"step_id": f"{prefix}.right-result", "kind": "morphism", "domain_id": a, "codomain_id": c, "physical_map": "The declared extension-then-cutoff composite on physical observables."},
    ]
    left_comp, right_comp = f"{prefix}.left-composition", f"{prefix}.right-composition"
    corrections = [
        {
            "test_id": "ym.test.uniform-density",
            "kind": "theorem",
            "preservation_structure_ids": list(YM_STRUCTURE_IDS),
            "intervention": "Attempt the uniform density and positivity-preservation estimate on the declared core.",
            "expected_if_useful": "One norm bound controls both composite routes without assuming a spectral gap.",
            "demotion_trigger": "Demote when the abstraction only renames the original continuum estimate.",
            "theory_question": "Does one common preservation norm control core extension and cutoff removal?",
        },
        {
            "test_id": "ym.test.hidden-sector",
            "kind": "countermodel",
            "preservation_structure_ids": list(YM_STRUCTURE_IDS),
            "intervention": "Adjoin a hidden gapless sector invisible to the proposed observable family.",
            "expected_if_useful": "The bridge refuses promotion until observable density excludes the hidden sector.",
            "demotion_trigger": "Demote if a sectorial estimate is misreported as a full Hamiltonian gap.",
            "theory_question": "Does the carrier see every reconstructed finite-energy sector?",
        },
    ]
    translations = [
        {
            "abstract_entity_id": cat["packet_id"],
            "abstract_entity": "Categorical regulated-to-continuum comparison object.",
            "entity_kind": "object",
            "physical_carrier_id": a,
            "physical_carrier": "Regulated lattice gauge-field measure and observable algebra.",
            "preservation_structure_ids": [
                "gauge_invariance",
                "locality",
                "observable_algebra",
                "regulator_ledger",
                "volume_ledger",
            ],
            "preserved_invariants": ["Gauge invariance on the observable core."],
            "broken_or_open_invariants": [
                "Uniform reflection positivity after cutoff removal remains open."
            ],
            "target_burden": "Construct the continuum observable algebra without assuming the desired gap.",
        },
        {
            "abstract_entity_id": hott["packet_id"],
            "abstract_entity": "Higher coherence cell for regulator and core transport.",
            "entity_kind": "coherence_cell",
            "physical_carrier_id": b,
            "physical_carrier": "Gauge-invariant observable core with Schwinger correlations.",
            "preservation_structure_ids": [
                "continuum_limit_order",
                "coupling_trajectory",
                "physical_normalization",
                "reflection_positivity",
                "theory_identity",
            ],
            "preserved_invariants": [
                "Local observable correlations remain explicitly typed."
            ],
            "broken_or_open_invariants": [
                "Uniform observable density and OS reconstruction remain open."
            ],
            "target_burden": "Prove the two physical limit routes preserve the same observable predicate.",
        },
    ]
    bindings.sort(key=lambda row: row["packet_id"])
    corrections.sort(key=lambda row: row["test_id"])
    translations.sort(key=lambda row: row["abstract_entity_id"])
    calibrations = sorted(run_ym_calibration_matrix(), key=lambda row: row["case_id"])
    bridge = {
        "schema_version": "7.0.0", "bridge_id": "ym.bridge.receipt-bound", "target_id": YM_TARGET,
        "dependency_authority": build_formal_dependency_authority(),
        "literature_basis": {}, "upstream_packet_bindings": bindings, "lens": "categorical_hott", "claim_level": "C0", "epistemic_status": "concept_candidate",
        "target_contract": {"spacetime_dimension": 4, "pure_gauge": True, "gauge_group_scope": "every declared compact simple gauge group", "continuum_required": True, "mass_gap_required": True},
        "representation_package": {"K": "Regulator and continuum representation class with a fixed physical scale.", "A_phys": "State-separating gauge-invariant observable algebra core.", "S": "Euclidean Schwinger correlation data on the observable core.", "D": "Admissible gauge-field configurations and probability measures.", "G": "Typed regulator-change and continuum comparison morphisms.", "L": "Locality, reflection positivity, and limit-order ledger.", "Q": "Quantitative preservation certificates with explicit error budgets."},
        "physical_diagram": physical_diagram,
        "carrier_translations": translations,
        "failure_witness": witness, "audit_receipts": {}, "correction_tests": corrections, "calibration_matrix": calibrations,
        "value_ablation": _ablation(ym_basis["report"], "combined"),
        "physics_evaluation": {"essential_relevance": "high", "unification_power": "high", "conceptual_depth": "high", "physical_reward": "high", "general_physics_impact": "Clarifies exactly when representation comparison preserves observable and spectral content.", "elegance_only": False, "assessment_status": "post_handback_internal_hypothesis", "physics_value_authorized": False, "investment_authorized": False, "decision": "refine_bridge", "decision_rationale": "Completed calibrations and task-clustered repeatability justify bridge refinement only; authority-distinct physics-value evidence is unavailable."},
        "downstream_handoffs": ["ym-freeze-clay-target", "ym-build-representation-calculus", "ym-build-observable-core", "ym-calibrate-restricted-models", "ym-define-relational-rigidity", "ym-prove-continuum-coherence", "ym-reconstruct-os-gap", "ym-audit-frontier", "physical-relevance-impact-auditor", "proof-same-domain-transfer-certifier"],
        "evidence_citations": ["tests/fixtures/categorical_hott_discovery/cases.json"], "explicit_unknowns": ["Uniform observable density in the continuum remains unproved."], "non_claims": ["No continuum construction or Hamiltonian mass gap is claimed."], "validation_handoff": "Route to continuum coherence, OS reconstruction, and frontier audit before any claim promotion.",
    }
    _rebuild_ym_preservation(bridge)
    pressure = {"carrier_translations": bridge["carrier_translations"], "theorem_obligations": bridge["theorem_obligations"]}
    bridge["literature_basis"] = _literature_basis(ym_basis, pressure)
    _bind_ym_audits(bridge)
    return bridge, [{"packet": cat, "parallel_evaluation": ym_basis["report"]}, {"packet": hott, "parallel_evaluation": ym_basis["report"]}]


def _bind_ym_audits(bridge: dict) -> None:
    subject = ym_bridge_subject_digest(bridge)
    fit = {"verdict": "candidate_advantage", "incumbent_gap": "The incumbent route does not bind both physical composite limits.", "candidate_gain": "The bridge exposes one exact uniformity obligation and a hidden-sector falsifier.", "remaining_gap": "Continuum construction and the Hamiltonian gap remain open.", "failure_case": "Demote if the bridge only renames existing analytic estimates."}
    transfer = bridge["same_domain_transfer"]
    same = {"source_domain": transfer["source_domain"], "target_domain": transfer["target_domain"], "structure_ledger_digest": transfer["structure_ledger_digest"], "changed_structures": transfer["changed_structures"], "certificate_status": {"proved": "passed", "conditional": "conditional", "open": "open", "failed": "failed"}[transfer["certificate_status"]], "certificate_status_basis": transfer["certificate_status_basis"], "quantifier_contract_digest": transfer["quantifier_contract_digest"], "evidence_registry_digest": transfer["evidence_registry_digest"], "carrier_translation_digest": transfer["carrier_translation_digest"], "continuum_authority_digest": transfer["continuum_authority_digest"], "evidence_matrix_version": transfer["evidence_matrix_version"], "preservation_transfer_digest": canonical_digest(transfer), "failure_case": "Reject any route that changes dimension, purity, gauge group, or normalization."}
    physical = {"physical_carrier": bridge["carrier_translations"][0]["physical_carrier"], "target_gate": "Four-dimensional pure Yang-Mills and every target quantifier remain frozen.", "obligation_ids": [row["obligation_id"] for row in bridge["theorem_obligations"]], "correction_test_ids": [row["test_id"] for row in bridge["correction_tests"]], "essential_relevance": "high", "physical_reward": "high", "investment_decision": bridge["physics_evaluation"]["decision"], "failure_case": "Demote if completed calibrations or matched effects cease to pass."}
    bridge["audit_receipts"] = {"subject_digest": subject, "fit_gap": _audit_receipt("abstraction-fit-gap-auditor", YM_TARGET, subject, fit), "same_domain": _audit_receipt("proof-same-domain-transfer-certifier", YM_TARGET, subject, same), "physical_relevance": _audit_receipt("physical-relevance-impact-auditor", YM_TARGET, subject, physical)}


def _rebind_ym_attack(bridge: dict) -> None:
    """Rehash every downstream envelope without re-deriving attacked semantics."""

    transfer = bridge["same_domain_transfer"]
    transfer["structure_ledger_digest"] = canonical_digest(
        transfer["structure_ledger"]
    )
    transfer["evidence_registry_digest"] = canonical_digest(
        bridge["evidence_registry"]
    )
    ledger_digest = transfer["structure_ledger_digest"]
    registry_digest = transfer["evidence_registry_digest"]
    for carrier in bridge["carrier_translations"]:
        carrier["structure_ledger_digest"] = ledger_digest
        carrier["evidence_registry_digest"] = registry_digest
    transfer["carrier_translation_digest"] = canonical_digest(
        bridge["carrier_translations"]
    )
    bridge["physics_handback"] = build_physics_handback(
        target_id=bridge["target_id"],
        domain_kind="physics",
        physical_carrier=bridge["carrier_translations"][0]["physical_carrier"],
        burdens=bridge["theorem_obligations"],
        correction_tests=bridge["correction_tests"],
        failure_witness=bridge["failure_witness"],
        target_contract=bridge["target_contract"],
        preservation_transfer=transfer,
        quantifier_contract=bridge["quantifier_contract"],
        evidence_registry=bridge["evidence_registry"],
        carrier_translations=bridge["carrier_translations"],
        continuum_authority=bridge["continuum_authority"],
    )
    pressure = {
        "carrier_translations": bridge["carrier_translations"],
        "theorem_obligations": bridge["theorem_obligations"],
    }
    bridge["literature_basis"]["pressure_mapping_digest"] = (
        literature_pressure_digest(
            source_mapping_ids=bridge["literature_basis"]["source_mapping_ids"],
            pressure_payload=pressure,
        )
    )
    _bind_ym_audits(bridge)


@pytest.mark.expensive
def test_ym_bridge_requires_transitive_forges_and_completed_calibrations(ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    result = validate_ym_bridge(bridge, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])
    assert result["status"] == "valid"
    assert result["completed_calibrations"] == 9
    assert result["upstream_formal_lens_execution_receipt_ids"] == [
        row["formal_lens_execution_receipt"]["receipt_id"]
        for row in bridge["upstream_packet_bindings"]
    ]
    assert len(bridge["same_domain_transfer"]["structure_ledger"]) == 14
    assert [row["structure_id"] for row in bridge["same_domain_transfer"]["structure_ledger"]] == list(YM_STRUCTURE_IDS)
    assert bridge["quantifier_contract"] == YM_QUANTIFIER_CONTRACT
    statuses = {row["structure_id"]: row["status"] for row in bridge["same_domain_transfer"]["structure_ledger"]}
    assert statuses["four_dimensional_pure_yang_mills"] == "required"
    assert statuses["theory_identity"] == "conditional"
    assert statuses["os_reconstruction_burden"] == "open"
    assert statuses["positive_hamiltonian_gap_target"] == "open"
    assert bridge["same_domain_transfer"]["certificate_status"] == "open"
    assert bridge["physics_handback"]["preservation_structure_ledger_digest"] == bridge["same_domain_transfer"]["structure_ledger_digest"]
    assert bridge["schema_version"] == "7.0.0"
    assert len(bridge["physics_handback"]["physics_burden_matrix"]) == 14
    assert bridge["physics_handback"]["carrier_translations"] == bridge["carrier_translations"]
    assert (
        bridge["physics_handback"]["continuum_authority"]
        == bridge["continuum_authority"]
    )
    assert (
        bridge["physics_handback"]["continuum_authority_digest"]
        == bridge["continuum_authority"]["content_digest"]
    )
    assert (
        bridge["physics_handback"][
            "authority_distinct_physics_value_evidence_status"
        ]
        == "unavailable"
    )
    assert not bridge["physics_handback"][
        "authority_distinct_physics_value_evidence_ids"
    ]
    for binding in bridge["upstream_packet_bindings"]:
        receipt = binding["formal_lens_execution_receipt"]
        assert binding["validation_receipt_id"] == receipt["receipt_id"]
        assert receipt["authority_scope"] == "sealed_finite_formal_lens_execution_only"
        assert receipt["production_evidence_status"] == "not_attested"
        assert receipt["physics_value_authorized"] is False

    forged = copy.deepcopy(bridge)
    forged_receipt = forged["upstream_packet_bindings"][0][
        "formal_lens_execution_receipt"
    ]
    forged_receipt["literature_snapshot_digest"] = canonical_digest(
        "forged-current-literature-projection"
    )
    forged_receipt["content_digest"] = canonical_digest(
        {key: value for key, value in forged_receipt.items() if key != "content_digest"}
    )
    _bind_ym_audits(forged)
    with pytest.raises(
        AbstractionValidationError,
        match="upstream binding",
    ):
        validate_ym_bridge(
            forged,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    correction_ids = [row["test_id"] for row in bridge["correction_tests"]]
    assert all(
        row["correction_test_ids"] == correction_ids
        for row in bridge["same_domain_transfer"]["structure_ledger"]
    )
    assert all(
        row["correction_test_ids"] == correction_ids
        for row in bridge["theorem_obligations"]
    )
    assert all(
        row["quantified_domain_coverage"] == []
        and row["subject_structure_id"] in YM_STRUCTURE_IDS
        for row in bridge["evidence_registry"]
    )
    overclaimed = copy.deepcopy(bridge)
    overclaimed["same_domain_transfer"]["certificate_status"] = "proved"
    _bind_ym_audits(overclaimed)
    with pytest.raises(AbstractionValidationError, match="fail-closed"):
        validate_ym_bridge(overclaimed, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])
    high_reward = copy.deepcopy(bridge)
    high_reward["physics_evaluation"]["decision"] = "invest_high_physics_reward"
    _bind_ym_audits(high_reward)
    with pytest.raises(AbstractionValidationError):
        validate_ym_bridge(high_reward, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])
    planned = copy.deepcopy(bridge)
    planned["calibration_matrix"][0]["result_status"] = "planned"
    planned["calibration_matrix"][0]["output"] = None
    planned["calibration_matrix"][0]["output_digest"] = None
    planned["calibration_matrix"][0]["evidence"] = None
    planned["calibration_matrix"][0]["validator_receipt"] = None
    _rebuild_ym_preservation(planned)
    _bind_ym_audits(planned)
    planned_result = validate_ym_bridge(planned, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])
    assert planned_result["decision"] == "refine_bridge"


@pytest.mark.expensive
@pytest.mark.parametrize("field", ["structure_ledger", "theorem_obligations", "carrier_translations", "changed_structures", "correction_tests"])
def test_ym_canonical_orders_reject_permutations(field: str, ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    if field in {"structure_ledger", "changed_structures"}:
        bridge["same_domain_transfer"][field].reverse()
        if field == "structure_ledger":
            bridge["same_domain_transfer"]["structure_ledger_digest"] = canonical_digest(
                bridge["same_domain_transfer"]["structure_ledger"]
            )
    else:
        bridge[field].reverse()
    if field in {"theorem_obligations", "carrier_translations"}:
        pressure = {"carrier_translations": bridge["carrier_translations"], "theorem_obligations": bridge["theorem_obligations"]}
        bridge["literature_basis"]["pressure_mapping_digest"] = literature_pressure_digest(
            source_mapping_ids=bridge["literature_basis"]["source_mapping_ids"], pressure_payload=pressure
        )
    _bind_ym_audits(bridge)
    expected_reason = (
        YM_CHANGED_STRUCTURES_INVALID
        if field == "changed_structures"
        else "canonical|order|obligations|correction"
    )
    with pytest.raises(AbstractionValidationError, match=expected_reason):
        validate_ym_bridge(bridge, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])


@pytest.mark.expensive
def test_ym_fixed_status_and_declaration_only_proof_reject(ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    fixed = bridge["same_domain_transfer"]["structure_ledger"][0]
    fixed["status"] = "open"
    _bind_ym_audits(bridge)
    with pytest.raises(AbstractionValidationError):
        validate_ym_bridge(bridge, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])


@pytest.mark.expensive
@pytest.mark.parametrize(
    "structure_id",
    [
        structure_id
        for structure_id in YM_STRUCTURE_IDS
        if YM_STRUCTURE_CONTRACTS[structure_id]["kind"]
        != "fixed_target_commitment"
    ],
)
def test_ym_finite_only_evidence_cannot_prove_continuum_claims(
    structure_id: str,
    ym_basis: dict,
) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    ledger = bridge["same_domain_transfer"]["structure_ledger"]
    structure = next(
        row for row in ledger if row["structure_id"] == structure_id
    )
    structure["status"] = "proved"
    structure["status_rationale"] = (
        "Proof is limited to the sealed finite bridge representation and grants "
        "no continuum physical theorem."
    )
    obligation = next(
        row
        for row in bridge["theorem_obligations"]
        if row["preservation_structure_ids"] == [structure_id]
    )
    obligation["status"] = "proved"
    bridge["same_domain_transfer"]["structure_ledger_digest"] = canonical_digest(
        ledger
    )
    pressure = {
        "carrier_translations": bridge["carrier_translations"],
        "theorem_obligations": bridge["theorem_obligations"],
    }
    bridge["literature_basis"]["pressure_mapping_digest"] = literature_pressure_digest(
        source_mapping_ids=bridge["literature_basis"]["source_mapping_ids"],
        pressure_payload=pressure,
    )

    with pytest.raises(AbstractionValidationError) as caught:
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    assert caught.value.reason_code == YM_CONTINUUM_AUTHORITY_REQUIRED



@pytest.mark.expensive
def test_ym_declarations_alone_cannot_condition_transport(ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    ledger = bridge["same_domain_transfer"]["structure_ledger"]
    row = next(item for item in ledger if item["structure_id"] == "gauge_invariance")
    evidence_by_ref = {
        item["evidence_ref"]: item for item in bridge["evidence_registry"]
    }
    refs = sorted(
        ref
        for ref, evidence in evidence_by_ref.items()
        if evidence["subject_structure_id"] == "gauge_invariance"
        and evidence["evidence_kind"] == "target_declaration"
    )
    row["evidence_refs"] = refs
    row["evidence_binding_digest"] = canonical_digest(
        [evidence_by_ref[ref] for ref in refs]
    )
    obligation = next(
        item
        for item in bridge["theorem_obligations"]
        if item["preservation_structure_ids"] == ["gauge_invariance"]
    )
    obligation["evidence_refs"] = refs
    obligation["evidence_binding_digest"] = row["evidence_binding_digest"]
    bridge["same_domain_transfer"]["structure_ledger_digest"] = canonical_digest(
        ledger
    )
    pressure = {
        "carrier_translations": bridge["carrier_translations"],
        "theorem_obligations": bridge["theorem_obligations"],
    }
    bridge["literature_basis"]["pressure_mapping_digest"] = literature_pressure_digest(
        source_mapping_ids=bridge["literature_basis"]["source_mapping_ids"],
        pressure_payload=pressure,
    )
    _bind_ym_audits(bridge)
    with pytest.raises(AbstractionValidationError, match="declarations alone"):
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )


@pytest.mark.expensive
@pytest.mark.parametrize("attack", ["dropped", "added", "misrouted"])
def test_ym_correction_scope_is_exact_and_bidirectional(
    attack: str,
    ym_basis: dict,
) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    hidden = next(
        row
        for row in bridge["correction_tests"]
        if row["test_id"] == "ym.test.hidden-sector"
    )
    if attack == "dropped":
        hidden["preservation_structure_ids"].remove("theory_identity")
    elif attack == "added":
        hidden["preservation_structure_ids"][:2] = reversed(
            hidden["preservation_structure_ids"][:2]
        )
    else:
        hidden["preservation_structure_ids"][-1] = "foreign_structure"
    _bind_ym_audits(bridge)
    with pytest.raises(AbstractionValidationError) as caught:
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    assert caught.value.reason_code == YM_CORRECTION_COVERAGE_INVALID


@pytest.mark.expensive
def test_ym_one_obligation_cannot_drop_a_correction_while_union_stays_complete(
    ym_basis: dict,
) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    ledger_row = bridge["same_domain_transfer"]["structure_ledger"][0]
    obligation = bridge["theorem_obligations"][0]
    dropped = ledger_row["correction_test_ids"].pop()
    obligation["correction_test_ids"].remove(dropped)
    assert {
        correction_id
        for row in bridge["theorem_obligations"]
        for correction_id in row["correction_test_ids"]
    } == {row["test_id"] for row in bridge["correction_tests"]}
    _rebind_ym_attack(bridge)
    with pytest.raises(AbstractionValidationError) as caught:
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    assert caught.value.reason_code == YM_CORRECTION_COVERAGE_INVALID


@pytest.mark.expensive
@pytest.mark.parametrize(
    "attack",
    ["subject", "claim", "polarity", "conclusion", "quantifier_coverage"],
)
def test_ym_fully_rehashed_evidence_inference_mutations_reject(
    attack: str,
    ym_basis: dict,
) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    evidence = next(
        row
        for row in bridge["evidence_registry"]
        if row["evidence_kind"] == "validated_finite_forge"
    )
    if attack == "subject":
        evidence["subject_structure_id"] = "positive_hamiltonian_gap_target"
    elif attack == "claim":
        evidence["exact_claim"] += " Forged cross-claim inference."
    elif attack == "polarity":
        evidence["polarity"] = "calibrates"
    elif attack == "conclusion":
        evidence["conclusion"] = "restricted_symbolic_boundary_only"
    else:
        evidence["quantified_domain_coverage"] = [
            YM_STRUCTURE_CONTRACTS[evidence["subject_structure_id"]][
                "quantifier_refs"
            ][0]
        ]
    evidence["content_digest"] = canonical_digest(
        {key: value for key, value in evidence.items() if key != "content_digest"}
    )
    registry_by_ref = {
        row["evidence_ref"]: row for row in bridge["evidence_registry"]
    }
    for structure in bridge["same_domain_transfer"]["structure_ledger"]:
        if evidence["evidence_ref"] in structure["evidence_refs"]:
            structure["evidence_binding_digest"] = canonical_digest(
                [registry_by_ref[ref] for ref in structure["evidence_refs"]]
            )
            obligation = next(
                row
                for row in bridge["theorem_obligations"]
                if row["obligation_id"] == structure["obligation_ids"][0]
            )
            obligation["evidence_binding_digest"] = structure[
                "evidence_binding_digest"
            ]
    for carrier in bridge["carrier_translations"]:
        if evidence["evidence_ref"] in carrier["evidence_refs"]:
            carrier["evidence_binding_digest"] = canonical_digest(
                [registry_by_ref[ref] for ref in carrier["evidence_refs"]]
            )
    bridge["evidence_registry_digest"] = canonical_digest(
        bridge["evidence_registry"]
    )
    _rebind_ym_attack(bridge)
    with pytest.raises(AbstractionValidationError) as caught:
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    assert caught.value.reason_code == YM_EVIDENCE_INFERENCE_INVALID


@pytest.mark.expensive
@pytest.mark.parametrize("attack", ["status_promotion", "basis_swap"])
def test_ym_fully_rehashed_carrier_derivation_mutations_reject(
    attack: str,
    ym_basis: dict,
) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    carrier = bridge["carrier_translations"][0]
    if attack == "status_promotion":
        carrier["preservation_status"] = "proved"
    else:
        carrier["preservation_status_basis"]["structure_statuses"][0][
            "status"
        ] = "open"
        carrier["preservation_status_basis_digest"] = canonical_digest(
            carrier["preservation_status_basis"]
        )
    _rebind_ym_attack(bridge)
    with pytest.raises(AbstractionValidationError) as caught:
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )
    assert caught.value.reason_code == YM_CARRIER_STATUS_DERIVATION_INVALID


@pytest.mark.expensive
def test_ym_physics_handback_matrix_tamper_rejects(ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    bridge["physics_handback"]["physics_burden_matrix"][10][
        "carrier_translation_ids"
    ] = []
    _bind_ym_audits(bridge)
    with pytest.raises(AbstractionValidationError, match="handback"):
        validate_ym_bridge(
            bridge,
            upstream_packets=upstream,
            parallel_evaluation=ym_basis["report"],
        )


def test_ym_validator_cli_emits_stable_json_reason_code(tmp_path: Path) -> None:
    packet = tmp_path / "invalid-packet.json"
    evaluation = tmp_path / "evaluation.json"
    upstream = tmp_path / "upstream.json"
    packet.write_text("{", encoding="utf-8")
    evaluation.write_text("{}", encoding="utf-8")
    upstream.write_text("{}", encoding="utf-8")
    script = ROOT / "skills/yang_mills/ym-categorical-hott-physics-bridge/scripts/validate_ym_categorical_hott_bridge.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            str(packet),
            str(evaluation),
            "--upstream-packet",
            str(upstream),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    diagnostic = json.loads(completed.stderr)
    assert completed.returncode == 1
    assert diagnostic["status"] == "invalid"
    assert diagnostic["reason_code"] == "input_document_invalid"


@pytest.mark.expensive
@pytest.mark.parametrize("attack", ["ledger_quantifier", "ledger_evidence", "transfer_quantifier", "transfer_evidence", "transfer_carrier", "handback_binding"])
def test_ym_cross_digest_attacks_reject(attack: str, ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    forged = canonical_digest({"attack": attack})
    if attack == "ledger_quantifier":
        bridge["same_domain_transfer"]["structure_ledger"][2]["quantifier_binding_digest"] = forged
        bridge["same_domain_transfer"]["structure_ledger_digest"] = canonical_digest(bridge["same_domain_transfer"]["structure_ledger"])
    elif attack == "ledger_evidence":
        bridge["same_domain_transfer"]["structure_ledger"][2]["evidence_binding_digest"] = forged
        bridge["same_domain_transfer"]["structure_ledger_digest"] = canonical_digest(bridge["same_domain_transfer"]["structure_ledger"])
    elif attack == "transfer_quantifier":
        bridge["same_domain_transfer"]["quantifier_contract_digest"] = forged
    elif attack == "transfer_evidence":
        bridge["same_domain_transfer"]["evidence_registry_digest"] = forged
    elif attack == "transfer_carrier":
        bridge["same_domain_transfer"]["carrier_translation_digest"] = forged
    else:
        bridge["physics_handback"]["preservation_binding_digest"] = forged
    _bind_ym_audits(bridge)
    with pytest.raises(AbstractionValidationError):
        validate_ym_bridge(bridge, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])


@pytest.mark.expensive
def test_ym_quantifier_text_is_canonical(ym_basis: dict) -> None:
    bridge, upstream = _ym_bridge(ym_basis)
    bridge["quantifier_contract"]["cutoff"]["statement"] += " Altered."
    with pytest.raises(AbstractionValidationError):
        validate_ym_bridge(bridge, upstream_packets=upstream, parallel_evaluation=ym_basis["report"])


def test_registered_forgers_repeat_same_suite_and_controls_score_zero(generic_basis: dict) -> None:
    report = generic_basis["report"]
    assert report["schema_version"] == "4.0.0"
    suite_ids = {row["case_suite_id"] for row in report["attempt_receipts"]}
    assert suite_ids == {report["case_suite_id"]}
    assert all("case_id" not in row for row in report["attempt_receipts"])
    assert suite_ids == {row["case_suite_id"] for row in report["condition_outputs"]}
    assert suite_ids.isdisjoint({row["case_id"] for row in report["held_out_cases"]})
    for output in report["condition_outputs"]:
        execution = output["sealed_output"]["theory_delta"]["forger_execution"]
        assert execution["case_suite_digest"] == report["held_out_case_suite_digest"]
        assert execution["authority_class"] == "internal_protocol_calibration"
        authority_digest = execution["dependency_authority"]["content_digest"]
        assert all(
            artifact["dependency_authority_digest"] == authority_digest
            and "dependency_authority" not in artifact
            for artifact in execution["artifacts"]
        )
        assert all(
            not any(blinded_structural_score(control["candidate"]).values())
            for control in execution["negative_controls"]
        )


def test_paired_aggregation_uses_exact_intersections_and_types_insufficiency(
    generic_basis: dict,
) -> None:
    report = generic_basis["report"]
    outputs = copy.deepcopy(report["condition_outputs"])
    attempts = copy.deepcopy(report["attempt_receipts"])
    missing_baseline = next(
        row
        for row in outputs
        if row["arm"] == "no_abstraction" and row["repetition"] == 1
    )
    outputs = [
        row for row in outputs if row["branch_id"] != missing_baseline["branch_id"]
    ]
    next(
        row for row in attempts if row["branch_id"] == missing_baseline["branch_id"]
    )["status"] = "failed"

    clusters = _build_task_clusters(outputs, report["held_out_cases"])
    aggregates = {
        row["arm"]: row
        for row in _build_aggregates(
            outputs,
            attempts,
            report["repetitions_scheduled_per_arm"],
            clusters,
            report["held_out_cases"],
        )
    }
    categorical = aggregates["categorical"]["paired_differences_vs_no_abstraction"]
    assert categorical["matched_repetitions"] == [2, 3, 4, 5]
    assert categorical["n_matched_repetitions"] == 4
    assert categorical["status"] == "insufficient_internal_calibration"
    assert categorical["diagnostics"] is None
    assert aggregates["categorical"]["internal_refinement_eligible"] is False

    hott = aggregates["hott"]["paired_differences_vs_no_abstraction"]
    assert hott["matched_repetitions"] == [2, 3, 4, 5, 6]
    assert hott["status"] == "sufficient_internal_calibration"
    assert all(
        diagnostic["n_executions"] == 5
        and diagnostic["iid_assumption"] is False
        and diagnostic["population_inference_authorized"] is False
        for diagnostic in hott["diagnostics"].values()
    )


def test_inadequate_arm_retention_hard_fails_with_separate_evidence(
    generic_basis: dict,
) -> None:
    basis_report = generic_basis["report"]
    with pytest.raises(
        AbstractionEvaluationError,
        match="fewer than five completed executions",
    ) as exc_info:
        run_abstraction_parallel_evaluation(
            literature_snapshot=generic_basis["snapshot"],
            assimilation_packet=generic_basis["assimilation"],
            source_portfolio=generic_basis["portfolio"],
            cases=basis_report["held_out_cases"],
            precommitted_failure_cells=[
                ("categorical", 4),
                ("categorical", 5),
                ("categorical", 6),
            ],
        )

    evidence = exc_info.value.failure_evidence
    assert evidence is not None
    assert evidence["status"] == "insufficient_retained_executions"
    assert evidence["minimum_required_per_arm"] == 5
    assert evidence["completed_by_arm"]["categorical"] == 3
    assert evidence["under_retained_arms"] == {"categorical": 3}
    assert len(evidence["failed_attempts"]) == 3
    assert len(evidence["completed_sibling_branch_ids"]) == 27
    assert evidence["unexpected_failure_branch_ids"] == []
    assert len(evidence["attempt_receipts"]) == 30
    assert all(
        row["status"] == "failed"
        and row["failure_class"] == "RuntimeError"
        and "precommitted partial-failure injection" in row["failure_detail"]
        for row in evidence["failed_attempts"]
    )
    assert validate_abstraction_evaluation_failure_evidence(evidence) == {
        "status": "valid_hard_floor_failure",
        "failure_id": evidence["failure_id"],
        "completed_sibling_count": 27,
        "failed_attempt_count": 3,
        "under_retained_arms": {"categorical": 3},
    }
    core = {key: value for key, value in evidence.items() if key != "content_digest"}
    assert evidence["content_digest"] == canonical_digest(core)
    tampered = copy.deepcopy(evidence)
    tampered["failed_attempts"][0]["failure_detail"] = "forged diagnosis"
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(AbstractionEvaluationError, match="failure|ledger"):
        validate_abstraction_evaluation_failure_evidence(tampered)

    forged_rubric = copy.deepcopy(evidence)
    forged_rubric["rubric_digest"] = canonical_digest("forged-rubric")
    forged_rubric["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_rubric.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(AbstractionEvaluationError, match="rubric digest"):
        validate_abstraction_evaluation_failure_evidence(forged_rubric)

    relabelled_schedule = copy.deepcopy(evidence)
    completed = next(
        row
        for row in relabelled_schedule["attempt_receipts"]
        if row["arm"] == "categorical" and row["status"] == "completed"
    )
    relabelled_schedule["precommitted_failures"][0] = {
        "arm": completed["arm"],
        "repetition": completed["repetition"],
        "branch_id": completed["branch_id"],
    }
    relabelled_schedule["common_input_digest"] = _evaluation_common_input_digest(
        target_id=relabelled_schedule["target_id"],
        literature_snapshot_digest=relabelled_schedule["literature_snapshot_digest"],
        assimilation_digest=relabelled_schedule["assimilation_digest"],
        source_portfolio_digest=relabelled_schedule["source_portfolio_digest"],
        cases=relabelled_schedule["held_out_cases"],
        repetitions=relabelled_schedule["repetitions_scheduled_per_arm"],
        failure_schedule=relabelled_schedule["precommitted_failures"],
        dependency_authority_digest=relabelled_schedule[
            "dependency_authority_digest"
        ],
    )
    relabelled_schedule["failure_id"] = stable_identifier(
        "abstraction-evaluation-failure",
        relabelled_schedule["common_input_digest"],
        relabelled_schedule["runtime_portfolio_digest"],
    )
    relabelled_schedule["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in relabelled_schedule.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(AbstractionEvaluationError, match="precommitted"):
        validate_abstraction_evaluation_failure_evidence(relabelled_schedule)

    forged_unexpected = copy.deepcopy(evidence)
    forged_unexpected["unexpected_failure_branch_ids"] = [
        evidence["completed_sibling_branch_ids"][0]
    ]
    forged_unexpected["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_unexpected.items()
            if key != "content_digest"
        }
    )
    with pytest.raises(AbstractionEvaluationError, match="unexpected-branch"):
        validate_abstraction_evaluation_failure_evidence(forged_unexpected)


def test_task_clusters_and_physics_handback_fail_closed(generic_basis: dict) -> None:
    report = generic_basis["report"]
    assert {row["case_id"] for row in report["task_clustered_reporting"]["clusters"]} == {row["case_id"] for row in CASES}
    assert all(
        diagnostic["iid_assumption"] is False
        and diagnostic["population_inference_authorized"] is False
        for aggregate in report["aggregates"]
        for diagnostic in aggregate["score_repeatability"].values()
    )
    case = next(row for row in CASES if row["domain_kind"] == "physics")
    packet = _forge_packet(case, generic_basis)
    assert packet["physics_handback"]["investment_authorized"] is False
    packet["physics_handback"]["failure_witness_digest"] = canonical_digest("forged")
    _bind_forge_audits(packet)
    with pytest.raises(AbstractionValidationError, match="handback"):
        validate_forge_packet(packet, parallel_evaluation=report)


def test_executable_category_laws_and_cone_reject_tampering(generic_basis: dict) -> None:
    case = next(row for row in CASES if row["lens"] == "categorical")
    packet = _forge_packet(case, generic_basis)
    packet["categorical_model"]["morphisms"][0]["action"][0]["target_element_id"] = packet["categorical_model"]["objects"][0]["element_ids"][1]
    _bind_forge_audits(packet)
    with pytest.raises(AbstractionValidationError, match="identity"):
        validate_forge_packet(packet, parallel_evaluation=generic_basis["report"])
    packet = _forge_packet(case, generic_basis)
    packet["categorical_model"]["universal_property"]["cone_checks"][0]["commutes"] = False
    _bind_forge_audits(packet)
    with pytest.raises(AbstractionValidationError, match="commutation"):
        validate_forge_packet(packet, parallel_evaluation=generic_basis["report"])


def test_hott_inverse_fiber_boundary_and_truncation_reject_tampering(generic_basis: dict) -> None:
    case = next(row for row in CASES if row["lens"] == "hott")
    for mutation in ("inverse", "fiber", "boundary", "truncation"):
        packet = _forge_packet(case, generic_basis)
        model = packet["hott_model"]
        if mutation == "inverse":
            path_id = model["equivalences"][0]["left_inverse_homotopy_ids"][0]
            next(row for row in model["paths"] if row["path_id"] == path_id)["target_term_id"] = model["types"][0]["term_ids"][1]
        elif mutation == "fiber":
            model["transports"][0]["fiber_action"][0]["target_truth"] = not model["transports"][0]["fiber_action"][0]["target_truth"]
        elif mutation == "boundary":
            model["coherence_cells"][0]["target_transport_ids"][-1] = model["transports"][0]["transport_id"]
        else:
            model["truncation_policy"]["application_status"] = "applied"
        _bind_forge_audits(packet)
        with pytest.raises(AbstractionValidationError):
            validate_forge_packet(packet, parallel_evaluation=generic_basis["report"])


def test_hott_inverse_homotopy_rejects_rehashed_nonnull_base_boundary() -> None:
    model, witness = build_hott_model_and_witness(
        "inverse-base-boundary",
        "obligation.inverse-base-boundary",
    )
    inverse_path_id = model["equivalences"][0]["left_inverse_homotopy_ids"][0]
    inverse_path = next(
        row for row in model["paths"] if row["path_id"] == inverse_path_id
    )
    indexed_fiber = next(
        row
        for row in model["path_fibers"]
        if row["fiber_id"] == inverse_path["ambient_fiber_id"]
    )
    for row in (inverse_path, indexed_fiber):
        row["source_fiber_truth"] = False
        row["target_fiber_truth"] = False

    with pytest.raises(FormalReasoningError) as caught:
        validate_hott_model(
            model,
            witness,
            {"obligation.inverse-base-boundary"},
        )
    assert caught.value.reason_code == HOTT_INVERSE_BASE_BOUNDARY_INVALID


@pytest.mark.parametrize("mutation", ["foreign", "duplicate", "missing", "boundary_swapped"])
def test_hott_proved_cell_requires_exact_unique_pointwise_paths(mutation: str) -> None:
    model, witness = build_hott_model_and_witness("path-adversary", "obligation.path")
    cell = next(row for row in model["coherence_cells"] if row["status"] == "proved")
    if mutation == "foreign":
        cell["pointwise_path_ids"][0] = model["equivalences"][0]["left_inverse_homotopy_ids"][0]
    elif mutation == "duplicate":
        cell["pointwise_path_ids"][1] = cell["pointwise_path_ids"][0]
    elif mutation == "missing":
        cell["pointwise_path_ids"][0] = "path-adversary.path.does-not-exist"
    else:
        cell["pointwise_path_ids"].reverse()
    with pytest.raises(FormalReasoningError, match="pointwise|proof"):
        validate_hott_model(model, witness, {"obligation.path"})


def test_every_hott_homotopy_path_has_one_exact_indexed_fiber() -> None:
    model, witness = build_hott_model_and_witness(
        "fiber-index", "obligation.fiber-index"
    )
    fibers = {row["fiber_id"]: row for row in model["path_fibers"]}
    assert len(fibers) == len(model["path_fibers"]) == len(model["paths"])
    assert {row["ambient_fiber_id"] for row in model["paths"]} == set(fibers)
    boundary_fields = {
        "level",
        "ambient_type_id",
        "source_term_id",
        "target_term_id",
        "source_fiber_truth",
        "target_fiber_truth",
    }
    for path in model["paths"]:
        fiber = fibers[path["ambient_fiber_id"]]
        assert all(path[field] == fiber[field] for field in boundary_fields)
    assert validate_hott_model(
        model, witness, {"obligation.fiber-index"}
    )["result"] == "noncoherent"


@pytest.mark.parametrize(
    "case", ["direct", "inverse", "multihop", "wrong_boundary", "missing_inhabitant"]
)
def test_hott_refutation_decides_exact_finite_path_inhabitance(case: str) -> None:
    prefix = f"path-closure-{case}"
    obligation_id = f"obligation.path-closure-{case}"
    model, witness = build_hott_model_and_witness(prefix, obligation_id)
    cell = next(row for row in model["coherence_cells"] if row["status"] == "refuted")
    source_term = cell["missing_path_term_ids"][0]
    compositions = {row["composition_id"]: row for row in model["transport_compositions"]}
    transports = {row["transport_id"]: row for row in model["transports"]}

    def boundary(composition_id: str) -> tuple[str, bool]:
        result_id = compositions[composition_id]["result_transport_id"]
        row = next(
            item
            for item in transports[result_id]["fiber_action"]
            if item["source_term_id"] == source_term
        )
        return row["target_term_id"], row["target_truth"]

    source = boundary(cell["source_composition_id"])
    target = boundary(cell["target_composition_id"])

    def add_path(tag: str, start: tuple[str, bool], end: tuple[str, bool]) -> None:
        path_id = f"{prefix}.rehashed-{tag}"
        fiber_id = f"{path_id}.fiber"
        indexed_boundary = {
            "level": 1,
            "ambient_type_id": cell["target_type_id"],
            "source_term_id": start[0],
            "target_term_id": end[0],
            "source_fiber_truth": start[1],
            "target_fiber_truth": end[1],
        }
        model["path_fibers"].append({"fiber_id": fiber_id, **indexed_boundary})
        model["paths"].append(
            {
                "path_id": path_id,
                "ambient_fiber_id": fiber_id,
                **indexed_boundary,
                "constructor": "Adversarial rehashed inhabitant of one exact finite indexed boundary.",
            }
        )

    if case == "direct":
        add_path("direct", source, target)
    elif case == "inverse":
        add_path("inverse", target, source)
    elif case == "multihop":
        intermediate = (source[0], not source[1])
        add_path("multihop-left", source, intermediate)
        add_path("multihop-right", intermediate, target)
    elif case == "wrong_boundary":
        add_path("wrong-boundary", source, (target[0], not target[1]))

    if case in {"direct", "inverse", "multihop"}:
        with pytest.raises(FormalReasoningError, match="exact indexed path space is inhabited"):
            validate_hott_model(model, witness, {obligation_id})
        return

    if case == "wrong_boundary":
        witness = build_negative_witness(
            model=model,
            validator_id="finite-hott-countermodel.v1",
            witness_kind=witness["witness_kind"],
            step_namespace=witness["step_namespace"],
            prefix=prefix,
            source_id=witness["source_id"],
            target_id=witness["target_id"],
            left_path_ids=witness["left_path_ids"],
            right_path_ids=witness["right_path_ids"],
            left_composite_id=witness["left_composite_id"],
            right_composite_id=witness["right_composite_id"],
        )
    assert validate_hott_model(model, witness, {obligation_id})["result"] == "noncoherent"


def test_term_endpoint_hott_paths_and_fibers_are_exactly_level_one() -> None:
    model, witness = build_hott_model_and_witness(
        "path-level", "obligation.path-level"
    )
    path_id = model["equivalences"][0]["left_inverse_homotopy_ids"][0]
    path = next(row for row in model["paths"] if row["path_id"] == path_id)
    fiber = next(
        row
        for row in model["path_fibers"]
        if row["fiber_id"] == path["ambient_fiber_id"]
    )
    path["level"] = 2
    fiber["level"] = 2
    with pytest.raises(FormalReasoningError, match="level 1"):
        validate_hott_model(model, witness, {"obligation.path-level"})


@pytest.mark.parametrize("mutation", ["empty_missing", "duplicate_policy", "permuted_policy"])
def test_hott_refutation_and_path_policy_are_canonical(mutation: str) -> None:
    model, witness = build_hott_model_and_witness("path-policy", "obligation.path-policy")
    if mutation == "empty_missing":
        next(row for row in model["coherence_cells"] if row["status"] == "refuted")["missing_path_term_ids"] = []
    elif mutation == "duplicate_policy":
        model["path_space_policy"]["closure_rules"] = ["reflexivity", "inversion", "inversion"]
    else:
        model["path_space_policy"]["closure_rules"] = ["inversion", "reflexivity", "concatenation"]
    with pytest.raises(FormalReasoningError, match="missing|policy|contract"):
        validate_hott_model(model, witness, {"obligation.path-policy"})


def test_hott_negative_witness_builder_rejects_rehashed_inhabitant() -> None:
    prefix = "path-builder-adversary"
    model, witness = build_hott_model_and_witness(prefix, "obligation.path-builder")
    cell = next(row for row in model["coherence_cells"] if row["status"] == "refuted")
    source_term = cell["missing_path_term_ids"][0]
    compositions = {row["composition_id"]: row for row in model["transport_compositions"]}
    transports = {row["transport_id"]: row for row in model["transports"]}
    boundaries = []
    for composition_id in (cell["source_composition_id"], cell["target_composition_id"]):
        result_id = compositions[composition_id]["result_transport_id"]
        action = next(row for row in transports[result_id]["fiber_action"] if row["source_term_id"] == source_term)
        boundaries.append((action["target_term_id"], action["target_truth"]))
    path_id = f"{prefix}.rehashed-direct"
    fiber_id = f"{path_id}.fiber"
    boundary = {"level": 1, "ambient_type_id": cell["target_type_id"], "source_term_id": boundaries[0][0], "target_term_id": boundaries[1][0], "source_fiber_truth": boundaries[0][1], "target_fiber_truth": boundaries[1][1]}
    model["path_fibers"].append({"fiber_id": fiber_id, **boundary})
    model["paths"].append({"path_id": path_id, "ambient_fiber_id": fiber_id, **boundary, "constructor": "Rehashed direct inhabitant of the exact indexed boundary."})
    with pytest.raises(FormalReasoningError, match="exact indexed path space is inhabited"):
        build_negative_witness(
            model=model, validator_id="finite-hott-countermodel.v1",
            witness_kind=witness["witness_kind"], step_namespace=witness["step_namespace"],
            prefix=prefix, source_id=witness["source_id"], target_id=witness["target_id"],
            left_path_ids=witness["left_path_ids"], right_path_ids=witness["right_path_ids"],
            left_composite_id=witness["left_composite_id"], right_composite_id=witness["right_composite_id"],
        )


def test_raw_self_digested_dependency_mapping_cannot_enter_cached_path() -> None:
    forged = {"scope": "caller-minted-not-a-derived-closure"}
    forged["content_digest"] = canonical_digest(forged)
    with pytest.raises(FormalReasoningError, match="validated run context"):
        build_hott_model_and_witness(
            "authority-adversary",
            "obligation.authority",
            _dependency_context=forged,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("mutation", ["foreign", "missing", "wrong_fiber", "wrong_ambient"])
def test_hott_general_paths_reject_invalid_indexed_fibers(mutation: str) -> None:
    model, witness = build_hott_model_and_witness(
        "fiber-adversary", "obligation.fiber"
    )
    path = model["paths"][0]
    original_fiber_id = path["ambient_fiber_id"]
    if mutation == "foreign":
        path["ambient_fiber_id"] = model["path_fibers"][1]["fiber_id"]
    elif mutation == "missing":
        model["path_fibers"] = [
            row
            for row in model["path_fibers"]
            if row["fiber_id"] != original_fiber_id
        ]
    elif mutation == "wrong_fiber":
        fiber = next(
            row
            for row in model["path_fibers"]
            if row["fiber_id"] == original_fiber_id
        )
        fiber["target_term_id"] = model["types"][0]["term_ids"][1]
    else:
        wrong_ambient = model["types"][1]["type_id"]
        path["ambient_type_id"] = wrong_ambient
        next(
            row
            for row in model["path_fibers"]
            if row["fiber_id"] == original_fiber_id
        )["ambient_type_id"] = wrong_ambient
    with pytest.raises(FormalReasoningError, match="indexed fiber|term-level typed"):
        validate_hott_model(model, witness, {"obligation.fiber"})


def test_bounded_dependency_authority_rejects_transitive_mutation(generic_basis: dict) -> None:
    report = copy.deepcopy(generic_basis["report"])
    report["dependency_authority"]["entries"][0]["content_digest"] = canonical_digest("mutated-contract")
    report["content_digest"] = canonical_digest({key: value for key, value in report.items() if key != "content_digest"})
    with pytest.raises(AbstractionEvaluationError, match="dependency authority"):
        validate_abstraction_parallel_evaluation(report)
    row = copy.deepcopy(run_ym_calibration_matrix()[0])
    row["dependency_authority"]["entries"][-1]["byte_size"] += 1
    with pytest.raises(Exception, match="dependency authority"):
        validate_ym_calibration(row)


def test_ym_calibrations_are_registered_replays_not_assertions() -> None:
    rows = run_ym_calibration_matrix()
    assert len(rows) == 9
    assert {row["runner_kind"] for row in rows} == {"symbolic", "countermodel", "boundary_fixture"}
    assert all(validate_ym_calibration(row)["status"] == "passed" for row in rows)
    tampered = copy.deepcopy(rows[0])
    tampered["output"]["promotion_authorized"] = True
    with pytest.raises(Exception, match="replay"):
        validate_ym_calibration(tampered)


def test_registry_bindings_cover_all_three_skills() -> None:
    names = {"categorical-concept-forger", "hott-equivalence-coherence-forger", "ym-categorical-hott-physics-bridge"}
    registry = json.loads((ROOT / "agentic/registries/skill_registry.yaml").read_text())["skills"]
    assert names <= {row["name"] for row in registry}


def test_quality_registry_projects_formal_contracts_by_exact_skill_identity() -> None:
    rows = json.loads((ROOT / "agentic/registries/skill_quality_registry.yaml").read_text())["skill_quality"]
    by_name = {row["name"]: row for row in rows}
    assert len(by_name) == len(rows)
    assert "finite carrier/action totality" in by_name["categorical-concept-forger"]["deterministic_boundary"]
    assert "exact pointwise-path boundaries" in by_name["hott-equivalence-coherence-forger"]["deterministic_boundary"]
    assert "boundary-fixture typing" in by_name["ym-categorical-hott-physics-bridge"]["deterministic_boundary"]
    assert by_name["categorical-concept-forger"]["contract_versions"] == {
        "formal_dependency_authority": "2.0.0",
        "formal_lens_execution_receipt": "2.0.0",
        "forge_packet": "5.0.0",
        "parallel_evaluation": "4.0.0",
    }
    assert by_name["hott-equivalence-coherence-forger"]["contract_versions"] == by_name["categorical-concept-forger"]["contract_versions"]
    assert by_name["ym-categorical-hott-physics-bridge"]["contract_versions"] == {
        "bridge_packet": "7.0.0",
        "continuum_authority": "1.0.0",
        "formal_dependency_authority": "2.0.0",
        "formal_lens_execution_receipt": "2.0.0",
        "parallel_evaluation": "4.0.0",
        "upstream_forge_packet": "5.0.0",
    }
    projections = json.loads(
        (ROOT / "registry/skill_projections/abducer_skill_projections.json").read_text()
    )["skills"]
    projected = {row["skill_name"]: row for row in projections}
    assert projected["categorical-concept-forger"]["contract_versions"] == by_name["categorical-concept-forger"]["contract_versions"]
    assert projected["hott-equivalence-coherence-forger"]["contract_versions"] == by_name["hott-equivalence-coherence-forger"]["contract_versions"]
    assert projected["ym-categorical-hott-physics-bridge"]["contract_versions"] == by_name["ym-categorical-hott-physics-bridge"]["contract_versions"]
    categorical_skill = (
        ROOT / "skills/discovery/categorical-concept-forger/SKILL.md"
    ).read_text()
    hott_skill = (
        ROOT / "skills/discovery/hott-equivalence-coherence-forger/SKILL.md"
    ).read_text()
    ym_bridge_skill = (
        ROOT / "skills/yang_mills/ym-categorical-hott-physics-bridge/SKILL.md"
    ).read_text()
    for skill_text in (categorical_skill, hott_skill):
        assert "v5 forge packet" in skill_text
        assert "v2 `formal_lens_execution_receipt`" in skill_text
        assert "parallel evaluation v4" in skill_text
        assert "v4 packet" not in skill_text
        assert "v1 `formal_lens_execution_receipt`" not in skill_text
    assert "upstream v5" in ym_bridge_skill
    assert "v2 `formal_lens_execution_receipt`" in ym_bridge_skill
    assert "bridge packet v7" in ym_bridge_skill
    assert "v1 formal-lens execution receipt" not in ym_bridge_skill
    assert "packet v4" not in ym_bridge_skill
    for looper in (
        "looper-hook-policy-maintainer",
        "looper-release-promoter",
        "looper-target-dependency-cartographer",
    ):
        assert by_name[looper]["deterministic_boundary"] == "Schema, path, artifact, and lifecycle checks are deterministic."
        assert "finite carrier" not in by_name[looper]["representation_contract"].lower()
