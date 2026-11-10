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

from hegelian_solver.discovery import mine_discovery_signals
from hegelian_solver.failures import classify_failures
from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.io import read_structured
from hegelian_solver.operators import propose_candidates
from hegelian_solver.validators import validate_candidates


ROOT = Path(__file__).resolve().parents[2]


def _concept(name: str):
    raw = read_structured(ROOT / f"hegelian_solver/examples/{name}.yaml")
    return formalize_concept(raw)


def test_number_failure_maps_to_group_completion_candidate():
    concept = _concept("naturals")
    failures = classify_failures(concept)
    candidates = propose_candidates(concept, failures)

    assert [failure.label for failure in failures] == ["NonClosure"]
    assert any(candidate.operator == "GroupCompletion" for candidate in candidates)


def test_group_examples_emit_shared_interface_signal():
    concept = _concept("group_examples")
    signals = mine_discovery_signals(concept)

    assert any(signal.label == "SharedInterface" for signal in signals)


def test_physics_candidate_has_regime_measurement_and_limit_obligations():
    concept = _concept("newtonian_mechanics")
    failures = classify_failures(concept)
    candidates = propose_candidates(concept, failures)
    packets = validate_candidates(concept, candidates)
    kinds = {obligation.kind for packet in packets for obligation in packet.obligations}

    assert any(candidate.operator == "InvariantizeKinematics" for candidate in candidates)
    assert {"regime", "measurement", "limiting_case"}.issubset(kinds)


def test_language_model_no_provenance_maps_to_retrieval():
    concept = _concept("assistant")
    failures = classify_failures(concept)
    candidates = propose_candidates(concept, failures)

    assert any(failure.label == "NoProvenance" for failure in failures)
    assert any(candidate.operator == "Retrieve" for candidate in candidates)
