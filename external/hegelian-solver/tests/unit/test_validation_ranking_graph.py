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

from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.graph import ConceptGraph, edge_from_candidate, node_from_concept
from hegelian_solver.io import read_structured
from hegelian_solver.operators import propose_candidates
from hegelian_solver.ranker import rank_candidates
from hegelian_solver.schemas import FailureCertificate, TransformationCandidate
from hegelian_solver.validators import generate_validation_packet, validate_candidates
from hegelian_solver.validators import default_backend_registry


ROOT = Path(__file__).resolve().parents[2]


def _naturals():
    return formalize_concept(read_structured(ROOT / "hegelian_solver/examples/naturals.yaml"))


def test_unknown_or_partial_obligations_are_not_accepted_as_passed():
    concept = _naturals()
    failure = FailureCertificate(
        id="failure_test",
        label="NonClosure",
        concept=concept.id,
        witness={"value": "3 - 5 not in Nat"},
        failed_obligation="closed subtraction",
        repair_target=["GroupCompletion"],
    )
    candidate = propose_candidates(concept, [failure])[0]
    packet = generate_validation_packet(concept, candidate)
    decision = rank_candidates([candidate], [packet])[0]

    assert any(obligation.status == "partial" for obligation in packet.obligations)
    assert decision.decision == "provisional"


def test_invalid_candidate_fails_hard_gate():
    concept = _naturals()
    candidate = TransformationCandidate(
        id="candidate_invalid",
        operator="BadOperator",
        source_concepts=[concept.id],
        target_concept=concept.model_dump(mode="json"),
        preservation_map={},
        resolution_mechanism="",
        expected_obligations=["preservation", "resolution", "noncollapse", "residual_limit"],
        residual_limits=[],
    )
    packet = generate_validation_packet(concept, candidate)
    decision = rank_candidates([candidate], [packet])[0]

    assert packet.hard_gate_failures
    assert decision.decision == "reject"


def test_graph_save_load_and_queries(tmp_path):
    concept = _naturals()
    failure = FailureCertificate(
        id="failure_test",
        label="NonClosure",
        concept=concept.id,
        witness={"value": "3 - 5 not in Nat"},
        failed_obligation="closed subtraction",
        repair_target=["GroupCompletion"],
    )
    candidate = propose_candidates(concept, [failure])[0]
    packet = validate_candidates(concept, [candidate])[0]
    decision = rank_candidates([candidate], [packet])[0]
    graph = ConceptGraph()
    graph.add_node(node_from_concept(concept))
    graph.add_edge(edge_from_candidate(concept, candidate, packet, decision))
    path = tmp_path / "graph.json"

    graph.save(path)
    loaded = ConceptGraph.load(path)

    assert loaded.successors(concept.id)
    assert loaded.open_residual_limits()


def test_default_validation_backend_registry_is_pluggable():
    registry = default_backend_registry()

    assert {"proof_plan", "smt", "theorem_prover", "simulation", "benchmark"}.issubset(
        set(registry.names())
    )
    assert registry.run("smt", {"id": "candidate"})["status"] == "planned"


def test_number_system_chain_operator_sequence():
    concept = _naturals()
    triggers = [
        FailureCertificate(
            id="f_nat_int",
            label="NonClosure",
            concept="Naturals",
            witness={"value": "3 - 5 not in Nat"},
            failed_obligation="subtraction closure",
            repair_target=["GroupCompletion"],
        ),
        FailureCertificate(
            id="f_int_rat",
            label="NonClosure",
            concept="Integers",
            witness={"value": "3 / 5 not in Int"},
            failed_obligation="division closure",
            repair_target=["FieldOfFractions"],
        ),
        FailureCertificate(
            id="f_rat_real",
            label="Incompleteness",
            concept="Rationals",
            witness={"value": "Cauchy sequence without rational limit"},
            failed_obligation="metric completeness",
            repair_target=["Completion"],
        ),
        FailureCertificate(
            id="f_real_complex",
            label="NonSolvability",
            concept="Reals",
            witness={"value": "x^2 + 1 = 0"},
            failed_obligation="algebraic solvability",
            repair_target=["AlgebraicAdjunction"],
        ),
    ]
    candidates = propose_candidates(concept, triggers)

    assert [candidate.operator for candidate in candidates] == [
        "GroupCompletion",
        "FieldOfFractions",
        "Completion",
        "AlgebraicAdjunction",
    ]
