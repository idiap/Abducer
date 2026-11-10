# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Acceptance and adversarial tests for the source-bound theory-atlas compiler."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.contracts import canonical_digest, stable_identifier
from skills.common import theory_atlas_defect_compiler as atlas


EVIDENCE_ID = "evidence.higher-abductive-design"
SOURCE_FRAGMENT = "fragment.source"
TARGET_FRAGMENT = "fragment.target"
DIAGRAM_ID = "diagram.comparison"
SOURCE_STRUCTURE = "SP"
KINDS = atlas.COMPLETION_KINDS


def _set(set_id: str, *elements: str) -> dict[str, Any]:
    return {"set_id": set_id, "elements": list(elements)}


def _map(
    map_id: str,
    domain: str,
    codomain: str,
    *pairs: tuple[str, str],
) -> dict[str, Any]:
    return {
        "map_id": map_id,
        "domain_set_id": domain,
        "codomain_set_id": codomain,
        "pairs": [{"source": source, "target": target} for source, target in pairs],
    }


def _obligation(kind: str) -> dict[str, Any]:
    if kind == "factorization":
        sets = [_set("D", "d"), _set("M", "m"), _set("C", "c")]
        maps = [
            _map("f", "D", "M", ("d", "m")),
            _map("g", "M", "C", ("m", "c")),
            _map("h", "D", "C", ("d", "c")),
        ]
    elif kind == "finite_representability":
        sets = [
            _set("HomX", "hx"), _set("NatX", "nx"),
            _set("HomY", "hy"), _set("NatY", "ny"),
        ]
        maps = [
            _map("phi_x", "HomX", "NatX", ("hx", "nx")),
            _map("phi_x_inverse", "NatX", "HomX", ("nx", "hx")),
            _map("phi_y", "HomY", "NatY", ("hy", "ny")),
            _map("phi_y_inverse", "NatY", "HomY", ("ny", "hy")),
            _map("hom_reindex", "HomX", "HomY", ("hx", "hy")),
            _map("nat_reindex", "NatX", "NatY", ("nx", "ny")),
        ]
    elif kind == "descent_gluing":
        sets = [
            _set("Global", "global"), _set("LocalU", "u"),
            _set("LocalV", "v"), _set("Overlap", "o"),
            _set("CompatiblePairs", "pair"),
        ]
        maps = [
            _map("res_u", "Global", "LocalU", ("global", "u")),
            _map("res_v", "Global", "LocalV", ("global", "v")),
            _map("res_u_overlap", "LocalU", "Overlap", ("u", "o")),
            _map("res_v_overlap", "LocalV", "Overlap", ("v", "o")),
            _map("pair_left", "CompatiblePairs", "LocalU", ("pair", "u")),
            _map("pair_right", "CompatiblePairs", "LocalV", ("pair", "v")),
            _map("restrict_pair", "Global", "CompatiblePairs", ("global", "pair")),
            _map("glue", "CompatiblePairs", "Global", ("pair", "global")),
        ]
    elif kind == "pushout":
        sets = [
            _set("C", "c"), _set("A", "a"), _set("B", "b"),
            _set("P", "p"), _set("Q", "q"),
        ]
        maps = [
            _map("c_to_a", "C", "A", ("c", "a")),
            _map("c_to_b", "C", "B", ("c", "b")),
            _map("a_to_p", "A", "P", ("a", "p")),
            _map("b_to_p", "B", "P", ("b", "p")),
            _map("a_to_q", "A", "Q", ("a", "q")),
            _map("b_to_q", "B", "Q", ("b", "q")),
            _map("p_to_q", "P", "Q", ("p", "q")),
        ]
    elif kind == "adjunction_naturality":
        sets = [
            _set("LH00", "lh00"), _set("RH00", "rh00"),
            _set("LH10", "lh10"), _set("RH10", "rh10"),
            _set("LH01", "lh01"), _set("RH01", "rh01"),
        ]
        maps = [
            _map("adj00", "LH00", "RH00", ("lh00", "rh00")),
            _map("adj00_inverse", "RH00", "LH00", ("rh00", "lh00")),
            _map("adj10", "LH10", "RH10", ("lh10", "rh10")),
            _map("adj10_inverse", "RH10", "LH10", ("rh10", "lh10")),
            _map("adj01", "LH01", "RH01", ("lh01", "rh01")),
            _map("adj01_inverse", "RH01", "LH01", ("rh01", "lh01")),
            _map("left_domain", "LH00", "LH10", ("lh00", "lh10")),
            _map("right_domain", "RH00", "RH10", ("rh00", "rh10")),
            _map("left_codomain", "LH00", "LH01", ("lh00", "lh01")),
            _map("right_codomain", "RH00", "RH01", ("rh00", "rh01")),
        ]
    elif kind == "lifting_obstruction":
        sets = [
            _set("A", "a"), _set("B", "b1", "b2"),
            _set("X", "x1", "x2"), _set("Y", "y1", "y2"),
        ]
        maps = [
            _map("i", "A", "B", ("a", "b1")),
            _map("u", "A", "X", ("a", "x1")),
            _map("p", "X", "Y", ("x1", "y1"), ("x2", "y1")),
            _map("v", "B", "Y", ("b1", "y1"), ("b2", "y2")),
        ]
    else:  # pragma: no cover - guarded by the public completion registry
        raise AssertionError(kind)
    return {
        "obligation_id": f"obligation.{kind}",
        "obligation_type": kind,
        "subject_fragment_id": SOURCE_FRAGMENT,
        "structure_id": SOURCE_STRUCTURE,
        "diagram_id": DIAGRAM_ID,
        "evidence_refs": [EVIDENCE_ID],
        "sets": sets,
        "maps": maps,
        "checks": [{
            "check_id": f"check.{kind}",
            "check_kind": kind,
            "map_ids": [row["map_id"] for row in maps],
            "set_ids": [row["set_id"] for row in sets],
            "expected": True,
            "observed": True,
        }],
    }


def _meaning_profile(prefix: str) -> dict[str, Any]:
    return {
        dimension: {
            "statement": f"{prefix} fixes the source-bound {dimension} commitment.",
            "evidence_refs": [EVIDENCE_ID],
        }
        for dimension in atlas.MEANING_DIMENSIONS
    }


def _fragment(prefix: str, fragment_id: str) -> dict[str, Any]:
    lead = "S" if prefix == "source" else "T"
    return {
        "fragment_id": fragment_id,
        "signature": {
            "objects": [f"{lead}0", f"{lead}1"],
            "morphisms": [{
                "symbol": f"{prefix}.f",
                "source_object": f"{lead}0",
                "target_object": f"{lead}1",
            }],
            "predicates": [f"{lead}P"],
        },
        "axioms": [f"{prefix} composition is defined only on the declared carrier."],
        "models": [f"{prefix} finite witness model with two typed objects."],
        "observables": [f"{prefix} endpoint comparison observable."],
        "scope": {
            "domain": "finite structural calibration",
            "regime": "sealed local example",
            "quantifiers": ["For every element explicitly listed in the finite carrier."],
            "exclusions": ["No continuum, theorem, truth, or physical-value conclusion."],
        },
        "evidence_refs": [EVIDENCE_ID],
        "meaning_profile": _meaning_profile(prefix),
    }


def valid_spec(
    target_id: str = "representational-transport-target",
) -> dict[str, Any]:
    """Return a complete compiler input reusable by downstream forge tests."""

    evidence_core = {
        "evidence_id": EVIDENCE_ID,
        "source_path": (
            "agentic/external/higher_abductive_theory_discovery/2026-07-22/"
            "capability_map.json"
        ),
        "exact_claim": (
            "The preserved reference supplies design taxonomies only; this row grants "
            "no runtime, proof, conceptual-value, or physics authority."
        ),
    }
    evidence = {**evidence_core, "content_digest": canonical_digest(evidence_core)}
    total_map = [
        {"source_symbol": "S0", "target_symbol": "T0", "symbol_kind": "object"},
        {"source_symbol": "S1", "target_symbol": "T1", "symbol_kind": "object"},
        {"source_symbol": "source.f", "target_symbol": "target.f", "symbol_kind": "morphism"},
        {"source_symbol": "SP", "target_symbol": "TP", "symbol_kind": "predicate"},
    ]
    relations = [
        {
            "relation_id": "relation.horizontal", "relation_kind": "horizontal",
            "source_fragment_id": SOURCE_FRAGMENT, "target_fragment_id": TARGET_FRAGMENT,
            "total": True, "symbol_map": copy.deepcopy(total_map),
            "unmapped_source_symbols": [],
            "preserved_structure": ["Object, morphism-endpoint, and predicate typing."],
            "failure_condition": "Fail if the translation changes an endpoint or silently drops a predicate.",
            "evidence_refs": [EVIDENCE_ID],
        },
        {
            "relation_id": "relation.vertical", "relation_kind": "vertical",
            "source_fragment_id": SOURCE_FRAGMENT, "target_fragment_id": TARGET_FRAGMENT,
            "total": True, "symbol_map": copy.deepcopy(total_map),
            "unmapped_source_symbols": [],
            "preserved_structure": ["Declared refinement direction and all typed symbols."],
            "failure_condition": "Fail if refinement reverses direction or loses a declared symbol.",
            "evidence_refs": [EVIDENCE_ID],
        },
        {
            "relation_id": "relation.partial", "relation_kind": "partial",
            "source_fragment_id": SOURCE_FRAGMENT, "target_fragment_id": TARGET_FRAGMENT,
            "total": False,
            "symbol_map": [{"source_symbol": "S0", "target_symbol": "T0", "symbol_kind": "object"}],
            "unmapped_source_symbols": ["S1", "source.f", "SP"],
            "preserved_structure": ["Only the explicitly mapped base object."],
            "failure_condition": "Fail if the partial relation is totalized by prose.",
            "evidence_refs": [EVIDENCE_ID],
        },
    ]
    diagram = {
        "diagram_id": DIAGRAM_ID,
        "diagram_kind": "comparison_square",
        "nodes": [
            {"node_id": "node.s0", "fragment_id": SOURCE_FRAGMENT, "object_symbol": "S0"},
            {"node_id": "node.s1", "fragment_id": SOURCE_FRAGMENT, "object_symbol": "S1"},
            {"node_id": "node.t0", "fragment_id": TARGET_FRAGMENT, "object_symbol": "T0"},
            {"node_id": "node.t1", "fragment_id": TARGET_FRAGMENT, "object_symbol": "T1"},
        ],
        "arrows": [
            {"arrow_id": "arrow.source", "source_node_id": "node.s0", "target_node_id": "node.s1", "arrow_type": "intra_fragment_morphism", "symbol_ref": "source.f"},
            {"arrow_id": "arrow.left", "source_node_id": "node.s0", "target_node_id": "node.t0", "arrow_type": "inter_fragment_relation", "symbol_ref": "relation.horizontal"},
            {"arrow_id": "arrow.right", "source_node_id": "node.s1", "target_node_id": "node.t1", "arrow_type": "inter_fragment_relation", "symbol_ref": "relation.horizontal"},
            {"arrow_id": "arrow.target", "source_node_id": "node.t0", "target_node_id": "node.t1", "arrow_type": "intra_fragment_morphism", "symbol_ref": "target.f"},
        ],
        "higher_cells": [{
            "cell_id": "cell.comparison", "cell_kind": "commutativity_obligation",
            "source_path": ["arrow.source", "arrow.right"],
            "target_path": ["arrow.left", "arrow.target"],
            "source_node_id": "node.s0", "target_node_id": "node.t1",
            "status": "open", "evidence_refs": [EVIDENCE_ID],
        }],
    }
    defect_types = {
        "factorization": "factorization",
        "finite_representability": "representability",
        "descent_gluing": "descent",
        "pushout": "coherence",
        "adjunction_naturality": "adjunction",
        "lifting_obstruction": "obstruction",
    }
    defects = []
    completion_specs = []
    for kind in KINDS:
        defect_id = f"defect.{kind}"
        defects.append({
            "defect_id": defect_id,
            "defect_type": defect_types[kind],
            "subject_fragment_id": SOURCE_FRAGMENT,
            "structure_id": SOURCE_STRUCTURE,
            "structure_kind": "predicate",
            "diagram_id": DIAGRAM_ID,
            "completion_kind": kind,
            "exact_failure": f"The declared {kind} structure is absent before completion.",
            "evidence_refs": [EVIDENCE_ID],
            "metaphor_guard": {
                "typed_diagram_required": True,
                "executable_obligation_required": True,
                "terminology_only": False,
            },
        })
        completion_specs.append({
            "candidate_id": f"candidate.{kind}",
            "defect_id": defect_id,
            "completion_kind": kind,
            "subject_fragment_id": SOURCE_FRAGMENT,
            "structure_id": SOURCE_STRUCTURE,
            "diagram_id": DIAGRAM_ID,
            "claim": f"A finite {kind} candidate discharges only its declared local check.",
            "obligation": _obligation(kind),
        })
    repair_attempts = {
        kind: {
            "outcome": "failed",
            "reason": f"The {kind} repair leaves the typed comparison defect open.",
            "evidence_refs": [EVIDENCE_ID],
        }
        for kind in atlas.REPAIR_LADDER
    }
    reflection_mutations = {
        lens: {
            "source_statement": "The two theory fragments should agree by direct translation.",
            "mutated_statement": f"The {lens} lens treats the translation defect as a new structural commitment.",
            "changed_commitments": [f"The {lens} route must expose its own typed failure condition."],
            "operator_refs": ["suspend"],
            "new_question": f"Which {lens} invariant survives the partial relation?",
            "new_failure_mode": f"The {lens} redescription fails when it erases the protected predicate.",
        }
        for lens in atlas.REFLECTION_LENSES
    }
    operator_decisions = {}
    for index, operator in enumerate(atlas.REDESCRIPTION_OPERATORS):
        if index < len(KINDS):
            operator_decisions[operator] = {
                "status": "applied",
                "reason": f"The {operator} operation exposes one registered completion pressure.",
                "candidate_refs": [f"candidate.{KINDS[index]}"],
            }
        else:
            operator_decisions[operator] = {
                "status": "not_applicable",
                "reason": f"The {operator} operation adds no distinct typed completion in this finite case.",
                "candidate_refs": [],
            }
    return_squares = []
    for index, kind in enumerate(KINDS, start=1):
        approximate = index == len(KINDS)
        abstract_output = float(index)
        concrete_output = abstract_output + (0.1 if approximate else 0.0)
        return_squares.append({
            "square_id": f"return.{kind}",
            "mode": "approximate" if approximate else "exact",
            "subject_fragment_id": SOURCE_FRAGMENT,
            "completion_candidate_id": f"candidate.{kind}",
            "abstract_path": [{
                "step_id": f"abstract.{kind}",
                "input_values": [0.0], "output_values": [abstract_output],
            }],
            "concrete_path": [{
                "step_id": f"concrete.{kind}",
                "input_values": [0.0], "output_values": [concrete_output],
            }],
            "error_bound": 0.2 if approximate else 0.0,
            "changed_structure_ids": [SOURCE_STRUCTURE],
        })
    return {
        "target_id": target_id,
        "evidence_registry": [evidence],
        "theory_fragments": [
            _fragment("source", SOURCE_FRAGMENT),
            _fragment("target", TARGET_FRAGMENT),
        ],
        "relations": relations,
        "diagrams": [diagram],
        "repair_attempts": repair_attempts,
        "reflection_mutations": reflection_mutations,
        "operator_decisions": operator_decisions,
        "defects": defects,
        "completion_specs": completion_specs,
        "structured_failures": [
            {"failure_id": "failure.factorization.1", "defect_id": "defect.factorization", "structure_id": SOURCE_STRUCTURE, "attempt": 1, "failure_class": "completion_failure", "exact_failure": "The first factorization attempt has no registered mediator.", "evidence_refs": [EVIDENCE_ID]},
            {"failure_id": "failure.factorization.2", "defect_id": "defect.factorization", "structure_id": SOURCE_STRUCTURE, "attempt": 2, "failure_class": "completion_failure", "exact_failure": "The second factorization attempt repeats the same structured absence.", "evidence_refs": [EVIDENCE_ID]},
        ],
        "representation_mutation": {
            "status": "candidate_pending_human",
            "trigger_failure_ids": ["failure.factorization.1", "failure.factorization.2"],
            "source_grammar": {"objects": ["old.object"], "morphisms": ["old.map"], "rules": ["old.rule"]},
            "proposed_grammar": {"objects": ["new.object"], "morphisms": ["new.map"], "rules": ["new.rule"]},
            "migration_map": [
                {"source_symbol": "old.object", "target_symbol": "new.object", "symbol_kind": "object", "preservation_status": "preserved"},
                {"source_symbol": "old.map", "target_symbol": "new.map", "symbol_kind": "morphism", "preservation_status": "approximated"},
                {"source_symbol": "old.rule", "target_symbol": "new.rule", "symbol_kind": "rule", "preservation_status": "lost"},
            ],
            "information_loss": ["The old rule is not silently identified with the proposed rule."],
            "new_expressivity": ["The proposed grammar names the missing mediator as a first-class typed object."],
            "human_acceptance_gate": {"required": True, "decision": "pending", "accepted": False, "execution_authorized": False, "authority": "human_only"},
        },
        "return_squares": return_squares,
    }


def _reseal(packet: dict[str, Any]) -> dict[str, Any]:
    sealed = copy.deepcopy(packet)
    sealed.pop("content_digest", None)
    sealed.pop("packet_id", None)
    packet_id = stable_identifier(
        "atlas-packet", sealed["target_id"], canonical_digest(sealed)
    )
    sealed["packet_id"] = packet_id
    sealed["content_digest"] = canonical_digest(sealed)
    return sealed


def test_compiler_emits_source_bound_v2_packet_and_typed_receipt() -> None:
    source = valid_spec()
    packet = atlas.compile_theory_atlas_defect_packet(source)
    receipt = atlas.validate_theory_atlas_defect_packet(packet)

    assert packet["schema_version"] == "2.0.0"
    assert packet["source_archive"]["archive_sha256"] == atlas.SOURCE_ARCHIVE_SHA256
    assert packet["source_archive"]["runtime_imported"] is False
    assert packet["source_archive"]["runtime_executed"] is False
    assert receipt["status"] == "validated"
    assert receipt["packet_id"] == packet["packet_id"]
    assert receipt["packet_digest"] == packet["content_digest"]
    assert receipt["authority_class"] == "finite_pre_forge_structural_pressure_only"
    assert receipt["content_digest"] == canonical_digest(
        {key: value for key, value in receipt.items() if key != "content_digest"}
    )
    assert {row["completion_kind"] for row in packet["completion_candidates"]} == set(KINDS)
    assert all(row["replay"]["source_bound_not_forge_evidence"] for row in packet["completion_candidates"])
    assert [row["obligation"] for row in packet["completion_candidates"]] == [
        row["obligation"] for row in source["completion_specs"]
    ]
    assert {row["mode"] for row in packet["return_squares"]} == {"exact", "approximate"}
    assert packet["authority_boundaries"]["theorem_proved"] is False
    assert packet["authority_boundaries"]["physics_value_authorized"] is False


@pytest.mark.parametrize(
    ("mutation", "reason_code"),
    [
        ("partial_totalized", "ATLAS_RELATION_INVALID"),
        ("morphism_endpoint_direction", "ATLAS_RELATION_INVALID"),
        ("repair_bypass", "ATLAS_REPAIR_LADDER_INVALID"),
        ("metaphor_only", "ATLAS_SCHEMA_INVALID"),
        ("migration_loss", "ATLAS_MUTATION_GATE_INVALID"),
        ("operator_candidate_gap", "ATLAS_OPERATOR_SWEEP_INVALID"),
        ("universal_obligation_false", "ATLAS_COMPLETION_INVALID"),
        ("return_square_splice", "ATLAS_RETURN_SQUARE_INVALID"),
        ("unknown_changed_structure", "ATLAS_RETURN_SQUARE_INVALID"),
        ("higher_cell_promotion", "ATLAS_SCHEMA_INVALID"),
        ("authority_promotion", "ATLAS_SCHEMA_INVALID"),
        ("nested_evidence_mutation", "ATLAS_EVIDENCE_INVALID"),
    ],
)
def test_fully_rehashed_structural_attacks_fail_closed(
    mutation: str, reason_code: str
) -> None:
    packet = atlas.compile_theory_atlas_defect_packet(valid_spec())
    if mutation == "partial_totalized":
        packet["relations"][2]["total"] = True
    elif mutation == "morphism_endpoint_direction":
        packet["relations"][0]["symbol_map"][0]["target_symbol"] = "T1"
    elif mutation == "repair_bypass":
        packet["repair_ladder"][0]["outcome"] = "repaired"
    elif mutation == "metaphor_only":
        packet["defects"][0]["metaphor_guard"]["terminology_only"] = True
    elif mutation == "migration_loss":
        packet["representation_mutation"]["migration_map"].pop()
    elif mutation == "operator_candidate_gap":
        row = packet["redescription_operator_sweep"][5]
        row["status"] = "not_applicable"
        row["candidate_refs"] = []
    elif mutation == "universal_obligation_false":
        candidate = packet["completion_candidates"][0]
        candidate["obligation"]["sets"][2]["elements"].append("c2")
        candidate["obligation"]["maps"][1]["pairs"][0]["target"] = "c2"
    elif mutation == "return_square_splice":
        packet["return_squares"][0]["completion_candidate_id"] = packet[
            "completion_candidates"
        ][1]["candidate_id"]
    elif mutation == "unknown_changed_structure":
        packet["return_squares"][0]["changed_structure_ids"] = ["unknown.structure"]
    elif mutation == "higher_cell_promotion":
        packet["diagrams"][0]["higher_cells"][0]["status"] = "conditional"
    elif mutation == "authority_promotion":
        packet["authority_boundaries"]["physics_value_authorized"] = True
    elif mutation == "nested_evidence_mutation":
        packet["evidence_registry"][0]["exact_claim"] += " Mutated after sealing."
    attacked = _reseal(packet)
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.validate_theory_atlas_defect_packet(attacked)
    assert error.value.reason_code == reason_code


def test_preserved_archive_byte_tamper_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = atlas.compile_theory_atlas_defect_packet(valid_spec())
    original_source_file = atlas._source_file
    tampered = tmp_path / "higher_abductive_theory_discovery_system.zip"
    tampered.write_bytes(
        original_source_file(atlas.SOURCE_ARCHIVE_PATH).read_bytes() + b"tamper"
    )

    def source_file(relative_path: str) -> Path:
        return tampered if relative_path == atlas.SOURCE_ARCHIVE_PATH else original_source_file(relative_path)

    monkeypatch.setattr(atlas, "_source_file", source_file)
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.validate_theory_atlas_defect_packet(packet)
    assert error.value.reason_code == "ATLAS_PROVENANCE_INVALID"


def test_compiler_rejects_unexhausted_repairs_and_failed_physics_return() -> None:
    missing_repair = valid_spec()
    missing_repair["repair_attempts"].pop(atlas.REPAIR_LADDER[-1])
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.compile_theory_atlas_defect_packet(missing_repair)
    assert error.value.reason_code == "ATLAS_INPUT_INVALID"

    failed_return = valid_spec()
    failed_return["return_squares"][-1]["error_bound"] = 0.01
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.compile_theory_atlas_defect_packet(failed_return)
    assert error.value.reason_code == "ATLAS_RETURN_SQUARE_INVALID"


@pytest.mark.parametrize("attack", ["missing_candidate", "duplicate_square_id"])
def test_rehashed_return_coverage_cannot_drop_or_alias_a_candidate(attack: str) -> None:
    packet = atlas.compile_theory_atlas_defect_packet(valid_spec())
    if attack == "missing_candidate":
        packet["return_squares"].pop(0)
    else:
        packet["return_squares"][1]["square_id"] = packet["return_squares"][0]["square_id"]
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.validate_theory_atlas_defect_packet(_reseal(packet))
    assert error.value.reason_code == "ATLAS_RETURN_SQUARE_INVALID"


def test_compiler_owned_authority_cannot_be_supplied_by_callers() -> None:
    supplied = valid_spec()
    supplied["authority_boundaries"] = {"physics_value_authorized": True}
    with pytest.raises(atlas.TheoryAtlasDefectError) as error:
        atlas.compile_theory_atlas_defect_packet(supplied)
    assert error.value.reason_code == "ATLAS_INPUT_INVALID"
