# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Held-out and negative-control tests for category/HoTT conceptual discovery."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

# Stop collection before parametrization touches the version-3 fixture.  This
# v1 module remains migration history, while the adjacent executable suite owns
# the current fixture contract.
pytest.skip(
    "superseded by receipt-bound v3 abstraction suite",
    allow_module_level=True,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.common.abstraction_discovery_validation import (  # noqa: E402
    AbstractionValidationError,
    validate_forge_packet,
    validate_ym_bridge,
)
from skills.common.discovery_lens_heuristic import (  # noqa: E402
    build_categorical_pathway_heuristic,
    build_hott_pathway_heuristic,
)


CASES = json.loads(
    (ROOT / "tests/fixtures/categorical_hott_discovery/cases.json").read_text(encoding="utf-8")
)
SCORE_WITH = {
    "burden_closure": 4,
    "obstruction_localization": 5,
    "consequence_yield": 4,
    "unification_without_erasure": 4,
    "correction_specificity": 5,
}
SCORE_WITHOUT = {
    "burden_closure": 2,
    "obstruction_localization": 2,
    "consequence_yield": 1,
    "unification_without_erasure": 2,
    "correction_specificity": 2,
}


def _pressure_rows() -> list[dict]:
    return [
        {
            "breakthrough_family": "semantic bridge",
            "queue_ids": ["queue.bridge", "queue.transport"],
            "required_move": "Transport representation identity through a compositional alignment interface",
            "abstraction_required": "A universal mediating object with typed equivalence and coherence data",
            "minimal_theorem_shape": "A correspondence theorem factoring transfer through the mediator",
            "obstruction_class": "target-alignment and formula-size-transport obstruction",
            "search_modes": ["representation translation", "universal factorization"],
            "sample_theorem_targets": ["Functorial transport preserves the declared target invariant"]
        },
        {
            "breakthrough_family": "barrier-aware transfer",
            "queue_ids": ["queue.transport", "queue.coherence"],
            "required_move": "Compose several model shifts while preserving identity and invariant witnesses",
            "abstraction_required": "A correspondence object whose transports obey higher coherence",
            "minimal_theorem_shape": "A nontrivial alignment theorem exposing path-dependent transfer failure",
            "obstruction_class": "characterization-bridge and general-magnification structural failure",
            "search_modes": ["coherence obstruction", "same-domain correspondence"],
            "sample_theorem_targets": ["Parallel transfer paths agree exactly under a named condition"]
        }
    ]


def _heuristic(lens: str, rows: list[dict]) -> dict:
    full = (
        build_categorical_pathway_heuristic(rows)
        if lens == "categorical"
        else build_hott_pathway_heuristic(rows)
    )
    return {
        key: full[key]
        for key in ("lens_id", "recommended", "score", "threshold", "active_criteria", "active_anti_triggers")
    }


def _forge_packet(case: dict) -> dict:
    lens = case["lens"]
    domain = case["domain_kind"]
    rows = _pressure_rows()
    physics_carrier = case.get(
        "physical_carrier",
        "gauge-invariant observable algebra transported between regulated field representations"
        if domain == "physics"
        else "not_applicable_non_physics: theorem transport between formal presentations",
    )
    validators = ["abstraction-fit-gap-auditor", "proof-same-domain-transfer-certifier"]
    if domain == "physics":
        validators.append("physical-relevance-impact-auditor")
    packet = {
        "schema_version": "1.0.0",
        "packet_id": case["case_id"],
        "target_id": "heldout-conceptual-target",
        "domain_kind": domain,
        "lens": lens,
        "source_pressure": {"frontier_rows": rows, "heuristic": _heuristic(lens, rows)},
        "target_contract": {
            "target_statement": "Preserve the exact target while making representation transport compositional",
            "mathematical_object": "A family of target-bearing representations and typed transfer maps",
            "preserved_invariants": ["Exact target semantics remain unchanged", "Quantifiers remain unchanged under transport"],
            "forbidden_target_changes": ["Do not replace the target by equivalence of notation", "Do not weaken universal quantifiers"]
        },
        "categorical_model": None,
        "hott_model": None,
        "failure_witness": {
            "witness_kind": "noncommutativity" if lens == "categorical" else "noncoherence",
            "diagram_id": f"diagram.{case['case_id']}",
            "source_object": "Initial target-bearing representation with frozen semantics",
            "target_object": "Final target-bearing representation with frozen semantics",
            "left_path": ["translate then normalize representation"],
            "right_path": ["normalize then translate representation"],
            "left_composite": "normalize_B composed with translate_A_to_B",
            "right_composite": "translate_normalized_A_to_B composed with normalize_A",
            "exact_obstruction": "normalize_B ∘ translate_A_to_B ≠ translate_normalized_A_to_B ∘ normalize_A",
            "boundary_conditions": ["Both paths use the same source and target objects", "All target quantifiers are held fixed"],
            "exact": True,
            "evidence": ["held-out witness derived by direct symbolic composition"]
        },
        "translation": {
            "physical_carrier": physics_carrier,
            "target_burden": "Prove that the two typed transport composites agree or isolate their exact obstruction",
            "observable_or_theorem_obligations": [{
                "obligation_id": "obligation.path-independence",
                "burden_kind": "both" if domain == "physics" else "theorem",
                "statement": "Establish path-independent transfer for every object in the declared core",
                "enabled_by_abstraction": "The abstraction types both composites and exposes a common obstruction object",
                "control_status": "not_reached_without_abstraction",
                "status": "open"
            }],
            "correction_test": {
                "intervention": "Compute both composites on a held-out boundary object with all target data fixed",
                "expected_if_useful": "The obstruction predicts exactly which invariant or coherence cell fails",
                "expected_if_decorative": "Both routes reproduce the incumbent calculation without a new obligation",
                "demotion_trigger": "Demote when the matched control localizes the same failure with equal specificity"
            },
            "elegance_only": False,
            "decision": "invest",
            "decision_rationale": "The lens exposes a new path-independence obligation and a correction test"
        },
        "value_ablation": {
            "same_target_and_evidence": True,
            "with_abstraction": copy.deepcopy(SCORE_WITH),
            "without_abstraction": copy.deepcopy(SCORE_WITHOUT),
            "net_new_value": 13,
            "strict_improvement": True,
            "changed_investment_decision": True,
            "evidence": ["Matched held-out task and evidence scorecard"]
        },
        "reuse_handoffs": {
            "upstream": ["reflective-conceptual-discovery"],
            "validators": validators,
            "downstream": ["reflective-theory-synthesizer"]
        },
        "epistemic_status": "concept_candidate",
        "evidence_citations": ["tests/fixtures/categorical_hott_discovery/cases.json"],
        "explicit_unknowns": ["Whether the proposed universal or coherence property is provable"],
        "validation_handoff": "Run the deterministic forge validator, then domain-specific review"
    }
    if lens == "categorical":
        packet["categorical_model"] = {
            "objects": ["Target-bearing representation objects", "Shared obstruction object"],
            "morphisms": ["Typed representation translations", "Normalization morphisms preserving semantics"],
            "composition_laws": ["Associative composition on typed representation translations"],
            "universal_property": "The obstruction object mediates every target-preserving path comparison uniquely",
            "new_consequence": "Path independence reduces to vanishing of one named universal obstruction"
        }
    else:
        packet["hott_model"] = {
            "types": ["Type of target-bearing representations", "Identity type of admissible transfers"],
            "equivalences": ["Equivalence between two presentations preserving target semantics"],
            "transport_maps": ["Transport of invariant witnesses along representation equivalence"],
            "coherence_cells": ["Two-cell comparing normalize-then-transport and transport-then-normalize"],
            "truncation_policy": "Retain two-path data through coherence checking; truncate only after the obligation closes",
            "new_consequence": "Path-dependent transfer is isolated as one explicit missing coherence cell"
        }
    return packet


def _mutate(packet: dict, mutation: str) -> None:
    if mutation == "decorative_consequence":
        packet["categorical_model"]["new_consequence"] = "Elegant notation"
    elif mutation == "equal_composites":
        packet["failure_witness"]["right_composite"] = packet["failure_witness"]["left_composite"]
    elif mutation == "inexact_obstruction":
        packet["failure_witness"]["exact_obstruction"] = "coherence is unclear"
    elif mutation == "zero_value_ablation":
        packet["value_ablation"]["with_abstraction"] = copy.deepcopy(SCORE_WITHOUT)
        packet["value_ablation"]["net_new_value"] = 0
        packet["value_ablation"]["strict_improvement"] = False
    elif mutation == "abstract_carrier":
        packet["translation"]["physical_carrier"] = "A higher categorical functor between elegant objects"
    else:  # pragma: no cover - fixture authoring guard
        raise AssertionError(f"unknown mutation {mutation}")


@pytest.mark.parametrize("case", [row for row in CASES if row["expected"] == "accept"], ids=lambda row: row["case_id"])
def test_heldout_generic_cases_accept(case: dict) -> None:
    result = validate_forge_packet(_forge_packet(case), expected_lens=case["lens"])
    assert result["status"] == "valid"
    assert result["net_new_value"] == 13


@pytest.mark.parametrize("case", [row for row in CASES if row["expected"] == "reject"], ids=lambda row: row["case_id"])
def test_decorative_and_inexact_negative_controls_reject(case: dict) -> None:
    packet = _forge_packet(case)
    _mutate(packet, case["mutation"])
    with pytest.raises(AbstractionValidationError):
        validate_forge_packet(packet, expected_lens=case["lens"])


def _ym_bridge() -> dict:
    calibrations = [
        "finite_transfer_matrix", "massive_gaussian", "massless_gaussian",
        "finite_volume_gap_collapse", "hidden_gapless_direct_sum", "spatial_only_decay",
        "topological_theory", "regulated_4d_lattice", "noncommuting_limit_order",
    ]
    return {
        "schema_version": "1.0.0",
        "bridge_id": "ym.bridge.heldout",
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "upstream_packet_ids": ["heldout-category-physics-observable-transport"],
        "lens": "categorical_hott",
        "claim_level": "C0",
        "epistemic_status": "concept_candidate",
        "target_contract": {
            "spacetime_dimension": 4,
            "pure_gauge": True,
            "gauge_group_scope": "every declared compact simple gauge group",
            "continuum_required": True,
            "mass_gap_required": True
        },
        "representation_package": {
            "K": "Regulator and continuum representation class with physical scale",
            "A_phys": "State-separating gauge-invariant observable algebra core",
            "S": "Euclidean Schwinger correlation data on the observable core",
            "D": "Admissible gauge-field configurations and probability measures",
            "G": "Typed regulator-change and continuum comparison morphisms",
            "L": "Locality, reflection positivity, and limit-order ledger",
            "Q": "Quantitative preservation certificates with explicit error budgets"
        },
        "carrier_translations": [
            {
                "abstract_entity": "Object representing one regulated presentation",
                "entity_kind": "object",
                "physical_carrier": "Gauge-invariant observable algebra with its regulated Schwinger correlations",
                "preservation_status": "conditional",
                "preserved_invariants": ["Gauge invariance on the observable core"],
                "broken_or_open_invariants": ["Reflection positivity after the continuum limit remains open"],
                "target_burden": "Construct a regulator-independent continuum observable algebra without assuming a gap"
            },
            {
                "abstract_entity": "Morphism comparing two regulator presentations",
                "entity_kind": "morphism",
                "physical_carrier": "Observable-algebra recovery map between lattice gauge-field measures",
                "preservation_status": "conditional",
                "preserved_invariants": ["Local gauge-invariant correlation functions on a declared core"],
                "broken_or_open_invariants": ["Uniform physical normalization and observable density remain open"],
                "target_burden": "Prove uniform recovery and error bounds before removing cutoff and volume"
            }
        ],
        "same_domain_transfer": {
            "source_domain": "four-dimensional pure Yang-Mills",
            "target_domain": "four-dimensional pure Yang-Mills",
            "preserved_structures": ["gauge_invariance", "locality", "reflection_positivity", "observable_algebra", "physical_normalization"],
            "changed_structures": ["Regulator presentation and approximation topology may change"],
            "certificate_status": "conditional",
            "consequence_delta": "A single noncommuting comparison square isolates the missing continuum preservation theorem"
        },
        "failure_witness": {
            "witness_kind": "noncommutativity",
            "diagram_id": "ym.diagram.cutoff-observable",
            "source_object": "Regulated gauge-invariant observable at cutoff a and volume V",
            "target_object": "Candidate continuum Schwinger observable in physical units",
            "left_path": ["remove cutoff then extend observable core"],
            "right_path": ["extend observable core then remove cutoff"],
            "left_composite": "continuum_limit_a composed with core_extension_a",
            "right_composite": "continuum_core_extension composed with continuum_limit_on_core_a",
            "exact_obstruction": "continuum_limit_a ∘ core_extension_a ≠ continuum_core_extension ∘ continuum_limit_on_core_a without a uniform density estimate",
            "boundary_conditions": ["Gauge group and four-dimensional pure-gauge content fixed", "Physical normalization held fixed"],
            "exact": True,
            "evidence": ["The two composites require different unproved uniformity estimates"]
        },
        "theorem_obligations": [{
            "obligation_id": "ym.obligation.uniform-core-transfer",
            "claim_level": "C3",
            "observable_or_theorem": "both",
            "statement": "Prove uniform observable-core recovery strong enough to pass reflection positivity and temporal rigidity",
            "quantifiers": {
                "cutoff": "For every sufficiently small positive cutoff a tending to zero",
                "volume": "Uniformly over finite volumes before the infinite-volume limit",
                "distance": "For every physical temporal separation in the declared estimate",
                "observable_class": "For every observable in the declared state-separating gauge-invariant core",
                "coupling": "Along the renormalized coupling trajectory fixed by the continuum normalization"
            },
            "status": "open"
        }],
        "correction_tests": [
            {
                "test_id": "ym.test.uniform-density",
                "kind": "theorem",
                "intervention": "Attempt the uniform density and positivity-preservation estimate on the declared core",
                "expected_if_useful": "The categorical square localizes one explicit norm bound sufficient for both paths",
                "demotion_trigger": "Demote if the abstraction only renames the original continuum estimate",
                "theory_question": "Does one common preservation norm control core extension and cutoff removal?"
            },
            {
                "test_id": "ym.test.hidden-sector",
                "kind": "countermodel",
                "intervention": "Adjoin a hidden gapless direct-sum sector invisible to the proposed observable family",
                "expected_if_useful": "The bridge rejects promotion until observable density rules out the hidden sector",
                "demotion_trigger": "Demote if the bridge incorrectly certifies a full gap from a sectorial estimate",
                "theory_question": "Does the proposed carrier see every reconstructed finite-energy sector?"
            }
        ],
        "calibration_matrix": [
            {"case_id": case, "predicted_outcome": "The bridge distinguishes the case from the full continuum mass-gap target", "pass_condition": "No false promotion and the first missing burden is named", "result_status": "planned"}
            for case in calibrations
        ],
        "value_ablation": {
            "same_target_and_evidence": True,
            "with_abstraction": copy.deepcopy(SCORE_WITH),
            "without_abstraction": copy.deepcopy(SCORE_WITHOUT),
            "net_new_value": 13,
            "strict_improvement": True,
            "changed_investment_decision": True,
            "evidence": ["Matched YM obligation scorecard on the same source artifacts"]
        },
        "physics_evaluation": {
            "essential_relevance": "high",
            "unification_power": "high",
            "conceptual_depth": "high",
            "physical_reward": "high",
            "general_physics_impact": "Clarifies when representation equivalence preserves observable and spectral content in constructive field theory",
            "elegance_only": False,
            "decision": "invest_high_physics_reward",
            "decision_rationale": "The bridge isolates a correction-sensitive continuum preservation obligation"
        },
        "downstream_handoffs": [
            "ym-freeze-clay-target", "ym-build-representation-calculus", "ym-build-observable-core",
            "ym-calibrate-restricted-models", "ym-define-relational-rigidity",
            "ym-prove-continuum-coherence", "ym-reconstruct-os-gap", "ym-audit-frontier",
            "physical-relevance-impact-auditor", "proof-same-domain-transfer-certifier"
        ],
        "evidence_citations": ["tests/fixtures/categorical_hott_discovery/cases.json"],
        "explicit_unknowns": ["Uniform observable-core density in the continuum remains unproved"],
        "non_claims": ["No continuum existence theorem or Hamiltonian mass gap is claimed"],
        "validation_handoff": "Run the bridge validator, restricted calibrations, continuum audit, and OS-gap audit"
    }


def test_ym_bridge_accepts_full_physics_translation() -> None:
    result = validate_ym_bridge(_ym_bridge())
    assert result["status"] == "valid"
    assert result["calibration_cases"] == 9
    assert result["claim_level"] == "C0"


@pytest.mark.parametrize("mutation", ["abstract_carrier", "domain_break", "missing_calibration", "elegance_only"])
def test_ym_bridge_rejects_decorative_or_domain_breaking_controls(mutation: str) -> None:
    packet = _ym_bridge()
    if mutation == "abstract_carrier":
        packet["carrier_translations"][0]["physical_carrier"] = "An elegant higher categorical functor"
    elif mutation == "domain_break":
        packet["same_domain_transfer"]["target_domain"] = "three-dimensional topological gauge theory"
    elif mutation == "missing_calibration":
        packet["calibration_matrix"] = packet["calibration_matrix"][:-1]
    else:
        packet["physics_evaluation"]["elegance_only"] = True
    with pytest.raises(AbstractionValidationError):
        validate_ym_bridge(packet)


def test_skill_clis_accept_their_lenses(tmp_path: Path) -> None:
    for lens, script in [
        ("categorical", "skills/discovery/categorical-concept-forger/scripts/validate_categorical_concept_packet.py"),
        ("hott", "skills/discovery/hott-equivalence-coherence-forger/scripts/validate_hott_coherence_packet.py"),
    ]:
        case = next(row for row in CASES if row["expected"] == "accept" and row["lens"] == lens)
        packet_path = tmp_path / f"{lens}.json"
        packet_path.write_text(json.dumps(_forge_packet(case)), encoding="utf-8")
        completed = subprocess.run([sys.executable, str(ROOT / script), str(packet_path)], cwd=ROOT, text=True, capture_output=True)
        assert completed.returncode == 0, completed.stderr


def test_registry_dispatch_docs_and_todo_reachability() -> None:
    names = {
        "categorical-concept-forger",
        "hott-equivalence-coherence-forger",
        "ym-categorical-hott-physics-bridge",
    }
    registry = json.loads((ROOT / "agentic/registries/skill_registry.yaml").read_text())["skills"]
    quality = json.loads((ROOT / "agentic/registries/skill_quality_registry.yaml").read_text())["skill_quality"]
    projections = json.loads((ROOT / "registry/skill_projections/abducer_skill_projections.json").read_text())["skills"]
    assert names <= {row["name"] for row in registry}
    assert names <= {row["name"] for row in quality if row["status"] == "promoted"}
    assert names <= {row["skill_name"] for row in projections if row["skill_depth"]["status"] == "promoted"}

    phases = {row["phase"]: row for row in json.loads((ROOT / "agentic/registries/discovery_marathon_skill_dispatch.yaml").read_text())["phases"]}
    assert {"categorical-concept-forger", "hott-equivalence-coherence-forger"} <= set(phases["parallel_hypothesis_maturation"]["conditional_skills"])
    assert "ym-categorical-hott-physics-bridge" in phases["yang_mills_representational_dynamics_overlay"]["conditional_skills"]
    assert names.isdisjoint(phases["parallel_hypothesis_maturation"]["required_skills"])

    docs = (ROOT / "docs/reference/skills.md").read_text(encoding="utf-8")
    todo = (ROOT / "agentic/todos/categorical_hott_abstraction_todos.yaml").read_text(encoding="utf-8")
    for name in names:
        assert name in docs
        assert name in todo
