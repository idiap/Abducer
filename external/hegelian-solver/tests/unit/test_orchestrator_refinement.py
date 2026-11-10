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

from hegelian_solver.hooks import SolverHooks
from hegelian_solver.orchestrator import _decide_stop, _refinement_triggers, run_solver
from hegelian_solver.schemas import Obligation, RankingDecision, TransformationCandidate, ValidationPacket


ROOT = Path(__file__).resolve().parents[2]


def _candidate(target_id: str = "target_1") -> TransformationCandidate:
    return TransformationCandidate(
        id="candidate_1",
        operator="AbstractInterface",
        source_concepts=["source_1"],
        target_concept={"id": target_id, "name": "Target"},
        preservation_map={"kind": "embedding"},
        resolution_mechanism="AbstractInterface addresses NonRepresentability",
        residual_limits=["provisional"],
    )


def _decision(decision: str, score: float = 0.6) -> RankingDecision:
    return RankingDecision(candidate_id="candidate_1", decision=decision, score=score)


def test_decide_stop_resolved_on_accept():
    reason = _decide_stop(
        decisions=[_decision("accept")],
        candidates=[_candidate()],
        next_triggers=[],
        iteration=1,
        max_iterations=3,
        previous_best_score=None,
    )
    assert reason == "resolved"


def test_decide_stop_no_candidates():
    reason = _decide_stop(
        decisions=[], candidates=[], next_triggers=[], iteration=1, max_iterations=3, previous_best_score=None
    )
    assert reason == "no_candidates"


def test_decide_stop_no_refinement_triggers():
    reason = _decide_stop(
        decisions=[_decision("provisional")],
        candidates=[_candidate()],
        next_triggers=[],
        iteration=1,
        max_iterations=3,
        previous_best_score=None,
    )
    assert reason == "no_refinement_triggers"


def test_decide_stop_plateau_when_score_does_not_improve():
    reason = _decide_stop(
        decisions=[_decision("provisional", score=0.6)],
        candidates=[_candidate()],
        next_triggers=_refinement_triggers(
            _candidate(),
            ValidationPacket(
                candidate_id="candidate_1",
                obligations=[
                    Obligation(id="o1", kind="coverage", statement="needs coverage", status="partial")
                ],
            ),
        ),
        iteration=2,
        max_iterations=3,
        previous_best_score=0.6,
    )
    assert reason == "plateau"


def test_decide_stop_continues_when_score_improves():
    reason = _decide_stop(
        decisions=[_decision("provisional", score=0.65)],
        candidates=[_candidate()],
        next_triggers=_refinement_triggers(
            _candidate(),
            ValidationPacket(
                candidate_id="candidate_1",
                obligations=[
                    Obligation(id="o1", kind="coverage", statement="needs coverage", status="partial")
                ],
            ),
        ),
        iteration=2,
        max_iterations=3,
        previous_best_score=0.5,
    )
    assert reason is None


def test_decide_stop_max_iterations_safety_net():
    reason = _decide_stop(
        decisions=[_decision("provisional", score=0.6)],
        candidates=[_candidate()],
        next_triggers=_refinement_triggers(
            _candidate(),
            ValidationPacket(
                candidate_id="candidate_1",
                obligations=[
                    Obligation(id="o1", kind="coverage", statement="needs coverage", status="partial")
                ],
            ),
        ),
        iteration=3,
        max_iterations=3,
        previous_best_score=None,
    )
    assert reason == "max_iterations"


def test_refinement_triggers_skip_core_and_passed_obligations():
    packet = ValidationPacket(
        candidate_id="candidate_1",
        obligations=[
            Obligation(id="o1", kind="preservation", statement="preserved", status="passed"),
            Obligation(id="o2", kind="coverage", statement="needs coverage", status="partial"),
            Obligation(id="o3", kind="transfer", statement="passed transfer", status="passed"),
        ],
    )
    triggers = _refinement_triggers(_candidate(), packet)

    assert len(triggers) == 1
    assert triggers[0].label == "CaseExplosion"
    assert triggers[0].concept == "target_1"


def test_run_solver_resolves_in_one_iteration_for_metric_space():
    trace = run_solver(ROOT / "hegelian_solver/examples/metric_space.yaml")

    assert trace.refinement["stop_reason"] == "resolved"
    assert trace.refinement["iterations_run"] == 1


def test_run_solver_plateaus_for_naturals():
    trace = run_solver(ROOT / "hegelian_solver/examples/naturals.yaml")

    assert trace.refinement["stop_reason"] == "plateau"
    assert trace.refinement["iterations_run"] == 2
    assert len(trace.refinement["iterations"]) == 2
    # the second iteration re-bases onto the first iteration's best target concept
    assert trace.refinement["iterations"][1]["concept_id"] != trace.refinement["iterations"][0]["concept_id"]


def test_run_solver_max_iterations_caps_the_loop():
    trace = run_solver(ROOT / "hegelian_solver/examples/naturals.yaml", max_iterations=1)

    assert trace.refinement["stop_reason"] == "max_iterations"
    assert trace.refinement["iterations_run"] == 1


def test_run_solver_no_candidates_stop_reason():
    raw = {
        "name": "BareConcept",
        "domain": "mathematical_concept",
        "examples": ["only one example"],
        "tasks": ["inspect it"],
    }
    trace = run_solver(raw)

    assert trace.refinement["stop_reason"] == "no_candidates"
    assert trace.candidates == []


def test_run_solver_fires_hooks_each_iteration():
    events: list[str] = []
    hooks = SolverHooks(
        on_iteration_start=lambda **kwargs: events.append(f"start:{kwargs['iteration']}"),
        on_candidates_generated=lambda **kwargs: events.append(f"candidates:{kwargs['iteration']}"),
        on_validated=lambda **kwargs: events.append(f"validated:{kwargs['iteration']}"),
        on_ranked=lambda **kwargs: events.append(f"ranked:{kwargs['iteration']}"),
        on_iteration_end=lambda **kwargs: events.append(f"end:{kwargs['iteration']}"),
        on_stop=lambda **kwargs: events.append(f"stop:{kwargs['reason']}"),
    )

    trace = run_solver(ROOT / "hegelian_solver/examples/naturals.yaml", hooks=hooks)

    assert events[:5] == ["start:1", "candidates:1", "validated:1", "ranked:1", "end:1"]
    assert events[-1] == f"stop:{trace.refinement['stop_reason']}"
    assert "start:2" in events
