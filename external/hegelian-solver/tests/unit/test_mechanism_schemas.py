# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from hegelian_solver.mechanisms import (
    load_mechanism_dossier,
    load_mechanism_dossiers,
    mechanism_validation_packet,
    mechanism_validation_packet_from_dossier,
)
from hegelian_solver.schemas import MechanismDossier
from hegelian_solver.schemas.mechanisms import all_mechanism_schema_models


ROOT = Path(__file__).resolve().parents[2]
MECHANISMS_FILE = ROOT / "hegelian_solver/examples/mechanisms/abductive_mechanism_requirements.yaml"


def test_mechanism_examples_validate_as_pydantic_dossiers():
    dossiers = load_mechanism_dossiers(MECHANISMS_FILE)

    assert len(dossiers) >= 3
    for dossier in dossiers:
        assert isinstance(dossier, MechanismDossier)
        assert dossier.mechanism_abduction_packet is not None
        assert dossier.mechanism_requirements_packet is not None
        assert dossier.mechanism_counterfactual_critique is not None
        assert dossier.mechanism_todo_packet is not None
        assert dossier.mechanism_abduction_packet.mechanism_hypotheses
        assert dossier.mechanism_requirements_packet.requirements
        assert dossier.mechanism_counterfactual_critique.counterfactual_tests
        assert dossier.mechanism_todo_packet.todo_groups


def test_mechanism_todo_class_alias_round_trips():
    dossiers = load_mechanism_dossiers(MECHANISMS_FILE)
    todo = dossiers[0].mechanism_todo_packet.todo_groups[0].todos[0]

    assert todo.class_ in {
        "formal_work",
        "evidence_work",
        "simulation_or_benchmark",
        "material_design",
        "implementation",
        "validation",
        "decision",
    }
    dumped = todo.model_dump(mode="json", by_alias=True)
    assert "class" in dumped
    assert "class_" not in dumped

    round_tripped = load_mechanism_dossier(dossiers[0].model_dump(mode="json", by_alias=True))
    assert round_tripped.mechanism_todo_packet.todo_groups[0].todos[0].class_ == todo.class_


def test_extra_fields_are_rejected():
    dossiers = load_mechanism_dossiers(MECHANISMS_FILE)
    payload = dossiers[0].model_dump(mode="json", by_alias=True)
    payload["unexpected_field"] = "nope"

    with pytest.raises(Exception):
        load_mechanism_dossier(payload)


def test_mechanism_validation_packet_treats_untested_requirements_as_planned():
    dossier = load_mechanism_dossiers(MECHANISMS_FILE)[0]
    requirements = dossier.mechanism_requirements_packet

    packet = mechanism_validation_packet(requirements)

    assert packet.candidate_id == f"mechanism::{requirements.mechanism_name}"
    assert packet.hard_gate_failures
    assert all(obligation.status == "planned" for obligation in packet.obligations)


def test_mechanism_validation_packet_uses_critique_results():
    dossier = load_mechanism_dossiers(MECHANISMS_FILE)[0]
    requirements = dossier.mechanism_requirements_packet
    critique = dossier.mechanism_counterfactual_critique

    packet = mechanism_validation_packet(requirements, critique)

    failed = {o.kind: o for o in packet.obligations if o.status == "failed"}
    assert failed
    assert any("req_clinical_transport_map" in failure for failure in packet.hard_gate_failures)


def test_mechanism_validation_packet_from_dossier_includes_blocking_todos():
    dossier = load_mechanism_dossiers(MECHANISMS_FILE)[0]

    packet = mechanism_validation_packet_from_dossier(dossier)

    todo_obligations = [o for o in packet.obligations if o.kind == "mechanism_todo"]
    assert todo_obligations
    assert all(o.status == "planned" for o in todo_obligations)
    blocking_todo_ids = {
        todo.id
        for group in dossier.mechanism_todo_packet.todo_groups
        for todo in group.todos
        if todo.blocks_candidate_acceptance
    }
    assert blocking_todo_ids
    assert any(
        any(todo_id in failure for todo_id in blocking_todo_ids) for failure in packet.hard_gate_failures
    )


def test_mechanism_validation_packet_from_dossier_requires_requirements():
    dossier = MechanismDossier(
        id="m1",
        source_tension_ref="t1",
        field="test",
        mechanism_name="Bare",
    )

    with pytest.raises(ValueError):
        mechanism_validation_packet_from_dossier(dossier)


def test_all_mechanism_schema_models_are_exported_for_json_schema():
    from hegelian_solver.schemas import all_schema_models

    exported = set(all_schema_models())
    for model in all_mechanism_schema_models():
        assert model in exported
