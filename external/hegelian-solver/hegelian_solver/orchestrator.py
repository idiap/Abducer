# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""End-to-end deterministic orchestration with a bounded reflective refinement loop.

A single propose -> validate -> rank pass rarely reaches a clean `accept`: most operators
in `operators/library.py` add at least one obligation (`coverage`, `transfer`, `adequacy`,
`universality`, ...) that the deterministic validator can only ever mark `partial`, since
there is no proof engine or benchmark runner behind it. Left alone, `run_solver` would
report whatever the first pass produced even when a different operator chain might have
done better, and would have no way to notice that it had nothing left to try.

The reflective refinement loop addresses that: each iteration treats the best candidate's
own *open* obligations as new determinate negations of its target concept and re-runs the
solver on that target, exactly the way the solver already treats a source concept's
counterexamples. This keeps refinement inside the existing typed pipeline (no new
mechanism) instead of bolting on an ad hoc retry.

Stopping criteria (see `_decide_stop` for the implementation):

- `resolved`      -- the best decision reached `accept` or `accept_as_branch`. Success.
- `no_candidates` -- nothing was generated; there is nothing to refine.
- `no_refinement_triggers` -- the best candidate's open obligations don't map to a new
  failure label, so another iteration would just re-run the same inputs.
- `plateau`       -- the best score did not improve by more than `SCORE_IMPROVEMENT_EPS`
  versus the previous iteration. This backend cannot manufacture new evidence, so an
  unimproved score means the next iteration would reproduce the same shape of partial
  obligations (verified by the AbstractInterface/Categorify chains, which regenerate
  identical `coverage`/`transfer`/`universality` obligations on every pass). Stopping here
  avoids burning iterations on a known-unproductive cycle.
- `max_iterations` -- a hard safety net so the loop terminates even if the heuristics above
  fail to detect a cycle.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hegelian_solver.creativity import analyze_candidates, order_by_decision
from hegelian_solver.discovery import mine_discovery_signals
from hegelian_solver.domain import domain_profile
from hegelian_solver.evidence import curate_tasks_and_evidence
from hegelian_solver.explanations import explain_run
from hegelian_solver.failures import classify_failures
from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.graph import ConceptGraph, edge_from_candidate, node_from_concept
from hegelian_solver.hooks import SolverHooks
from hegelian_solver.ids import stable_id
from hegelian_solver.io import read_structured, write_structured
from hegelian_solver.operators import propose_candidates
from hegelian_solver.ranker import rank_candidates
from hegelian_solver.reasoning_log import build_reasoning_log
from hegelian_solver.reports import write_html_report
from hegelian_solver.schemas import (
    ConceptNode,
    DiscoverySignal,
    FailureCertificate,
    RankingDecision,
    SolverTrace,
    TransformationCandidate,
    ValidationPacket,
)
from hegelian_solver.skills_runtime.ledger import RunLedger
from hegelian_solver.validators import validate_candidates

DEFAULT_MAX_ITERATIONS = 3
SCORE_IMPROVEMENT_EPS = 0.01

# Maps a still-open obligation `kind` back onto the failure taxonomy so it can become a
# new determinate negation of the candidate's own target concept. Kinds with no entry here
# fall back to "NonRepresentability", which routes to the generic `AbstractInterface` repair.
OBLIGATION_KIND_TO_FAILURE_LABEL = {
    "universality": "NoUniversalProperty",
    "coverage": "CaseExplosion",
    "transfer": "PoorTransfer",
    "adequacy": "NonRepresentability",
    "governance": "GovernanceGap",
    "risk": "ToolMisuse",
    "efficiency": "ComputeInefficiency",
    "anti_overfit": "ParameterAdHocness",
    "regime": "Overextension",
    "measurement": "MeasurementGap",
    "limiting_case": "NoLimitingCase",
}

# Obligations every candidate carries about the move itself (not the target's own further
# development); refining on these would just re-litigate the same transformation forever.
CORE_OBLIGATION_KINDS = {"preservation", "resolution", "noncollapse", "residual_limit"}


def _refinement_triggers(
    candidate: TransformationCandidate, packet: ValidationPacket
) -> list[FailureCertificate]:
    """Turn a candidate's open, non-core obligations into triggers on its own target."""

    target_id = candidate.target_concept["id"]
    triggers: list[FailureCertificate] = []
    for obligation in packet.obligations:
        if obligation.status == "passed" or obligation.kind in CORE_OBLIGATION_KINDS:
            continue
        label = OBLIGATION_KIND_TO_FAILURE_LABEL.get(obligation.kind, "NonRepresentability")
        payload = {
            "label": label,
            "concept": target_id,
            "witness": {"type": "open_obligation", "value": obligation.statement},
            "failed_obligation": obligation.statement,
            "trace": [candidate.id, obligation.id],
            "repair_target": [],
            "severity": "medium",
            "unknowns": [obligation.blocker] if obligation.blocker else [],
        }
        payload["id"] = stable_id("failure", payload)
        triggers.append(FailureCertificate.model_validate(payload))
    return triggers


def _decide_stop(
    *,
    decisions: list[RankingDecision],
    candidates: list[TransformationCandidate],
    next_triggers: list[FailureCertificate],
    iteration: int,
    max_iterations: int,
    previous_best_score: float | None,
) -> str | None:
    """Return a stop reason if the loop should end after this iteration, else None."""

    top = decisions[0] if decisions else None
    if top and top.decision in {"accept", "accept_as_branch"}:
        return "resolved"
    if not candidates:
        return "no_candidates"
    if not next_triggers:
        return "no_refinement_triggers"
    best_score = top.score if top else 0.0
    if previous_best_score is not None and best_score <= previous_best_score + SCORE_IMPROVEMENT_EPS:
        return "plateau"
    if iteration >= max_iterations:
        return "max_iterations"
    return None


def run_solver(
    raw: Any,
    output_dir: str | Path | None = None,
    *,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    hooks: SolverHooks | None = None,
) -> SolverTrace:
    if isinstance(raw, (str, Path)) and Path(raw).exists():
        raw = read_structured(raw)

    hooks = hooks or SolverHooks()
    profile = domain_profile(raw)
    seed_concept = formalize_concept(raw, profile)
    task_packet = curate_tasks_and_evidence(seed_concept)
    base_failures = classify_failures(seed_concept, task_packet)
    base_signals = mine_discovery_signals(seed_concept)

    iteration_concepts: list[ConceptNode] = []
    all_candidates: list[TransformationCandidate] = []
    all_packets: list[ValidationPacket] = []
    all_decisions: list[RankingDecision] = []
    all_triggers: list[FailureCertificate | DiscoverySignal] = []
    iteration_log: list[dict[str, Any]] = []

    current_concept = seed_concept
    triggers = base_failures + base_signals
    previous_best_score: float | None = None
    stop_reason = "max_iterations"
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        hooks.fire("on_iteration_start", iteration=iteration, concept=current_concept, triggers=triggers)

        candidates = propose_candidates(current_concept, triggers)
        hooks.fire("on_candidates_generated", iteration=iteration, candidates=candidates)

        packets = validate_candidates(current_concept, candidates)
        hooks.fire("on_validated", iteration=iteration, packets=packets)

        decisions = rank_candidates(candidates, packets)
        hooks.fire("on_ranked", iteration=iteration, decisions=decisions)

        iteration_concepts.append(current_concept)
        all_candidates.extend(candidates)
        all_packets.extend(packets)
        all_decisions.extend(decisions)
        all_triggers.extend(triggers)

        top = decisions[0] if decisions else None
        packet_by_id = {packet.candidate_id: packet for packet in packets}
        candidate_by_id = {candidate.id: candidate for candidate in candidates}
        next_triggers: list[FailureCertificate] = []
        if top and top.candidate_id in candidate_by_id:
            next_triggers = _refinement_triggers(candidate_by_id[top.candidate_id], packet_by_id[top.candidate_id])

        iteration_log.append(
            {
                "iteration": iteration,
                "concept_id": current_concept.id,
                "trigger_count": len(triggers),
                "candidate_count": len(candidates),
                "top_candidate_id": top.candidate_id if top else None,
                "top_decision": top.decision if top else "no_candidates",
                "top_score": top.score if top else 0.0,
            }
        )
        hooks.fire("on_iteration_end", iteration=iteration, summary=iteration_log[-1])

        stop_reason = _decide_stop(
            decisions=decisions,
            candidates=candidates,
            next_triggers=next_triggers,
            iteration=iteration,
            max_iterations=max_iterations,
            previous_best_score=previous_best_score,
        )
        if stop_reason:
            hooks.fire("on_stop", reason=stop_reason, iteration=iteration)
            break

        previous_best_score = top.score if top else 0.0
        current_concept = formalize_concept(candidate_by_id[top.candidate_id].target_concept, profile)
        triggers = next_triggers

    graph = ConceptGraph()
    graph.add_node(node_from_concept(seed_concept, status="active"))

    # Map each candidate back to the concept it was proposed against (iterations can
    # re-base onto a previous candidate's target, so this isn't always `seed_concept`).
    candidate_iteration: dict[str, ConceptNode] = {}
    offset = 0
    for entry, source_concept in zip(iteration_log, iteration_concepts):
        count = entry["candidate_count"]
        for candidate in all_candidates[offset : offset + count]:
            candidate_iteration[candidate.id] = source_concept
        offset += count

    packet_by_id = {packet.candidate_id: packet for packet in all_packets}
    decision_by_id = {decision.candidate_id: decision for decision in all_decisions}
    for candidate in all_candidates:
        decision = decision_by_id.get(candidate.id)
        packet = packet_by_id.get(candidate.id)
        source_concept = candidate_iteration[candidate.id]
        if not decision or not packet:
            continue
        if decision.decision in {"accept", "accept_as_branch", "provisional"}:
            target_node = node_from_concept(
                formalize_concept(candidate.target_concept, profile),
                status="validated" if decision.decision != "provisional" else "provisional",
            )
            graph.add_node(target_node)
            graph.add_edge(edge_from_candidate(source_concept, candidate, packet, decision))
        else:
            graph.rejected_candidates.append(
                {
                    "candidate": candidate.model_dump(mode="json"),
                    "decision": decision.model_dump(mode="json"),
                    "validation": packet.model_dump(mode="json"),
                }
            )

    triggers_by_id = {trigger.id: trigger for trigger in all_triggers}
    creativity_analyses = order_by_decision(
        analyze_candidates(all_candidates, triggers_by_id, packet_by_id), decision_by_id
    )

    explanation = explain_run(seed_concept, all_candidates, all_packets, all_decisions)
    run_id = stable_id("run", {"concept": seed_concept.id, "candidates": [c.id for c in all_candidates]})
    refinement_summary = {
        "max_iterations": max_iterations,
        "iterations_run": iteration,
        "stop_reason": stop_reason,
        "iterations": iteration_log,
    }
    creativity_payload = [analysis.model_dump(mode="json") for analysis in creativity_analyses]

    ledger = RunLedger(run_id=run_id)
    ledger.record("domain_profile", "DomainProfile", profile.model_dump(mode="json"))
    ledger.record("concept_formalization", seed_concept.__class__.__name__, seed_concept.model_dump(mode="json"))
    ledger.record("task_evidence", "TaskEvidencePacket", task_packet)
    ledger.record("failure_classification", "FailureCertificateList", {"items": [f.model_dump(mode="json") for f in base_failures]})
    ledger.record("discovery_mining", "DiscoverySignalList", {"items": [s.model_dump(mode="json") for s in base_signals]})
    ledger.record("candidate_generation", "TransformationCandidateList", {"items": [c.model_dump(mode="json") for c in all_candidates]})
    ledger.record("validation", "ValidationPacketList", {"items": [p.model_dump(mode="json") for p in all_packets]})
    ledger.record("ranking", "RankingDecisionList", {"items": [d.model_dump(mode="json") for d in all_decisions]})
    ledger.record("reflective_refinement", "RefinementSummary", refinement_summary)
    ledger.record("conceptual_creativity", "ConceptualCreativityAnalysisList", {"items": creativity_payload})
    ledger.record("graph_update", "ConceptGraph", graph.to_dict())
    ledger.record("explanation", "Text", {"value": explanation})
    reasoning_log = build_reasoning_log(
        run_id=run_id,
        profile=profile,
        concept=seed_concept,
        task_packet=task_packet,
        failures=base_failures,
        signals=base_signals,
        candidates=all_candidates,
        validation_packets=all_packets,
        decisions=all_decisions,
        graph=graph,
        explanation=explanation,
        refinement_summary=refinement_summary,
        creativity_analyses=creativity_payload,
    )
    ledger.record("reasoning_log", "ReasoningLog", reasoning_log.model_dump(mode="json"))

    trace_payload = {
        "run_id": run_id,
        "seed_nodes": [seed_concept.model_dump(mode="json")],
        "tasks": task_packet["tasks"],
        "evidence": task_packet["evidence"],
        "failures": [failure.model_dump(mode="json") for failure in base_failures],
        "discovery_signals": [signal.model_dump(mode="json") for signal in base_signals],
        "candidates": [candidate.model_dump(mode="json") for candidate in all_candidates],
        "validation_packets": [packet.model_dump(mode="json") for packet in all_packets],
        "ranking_decisions": [decision.model_dump(mode="json") for decision in all_decisions],
        "graph_updates": graph.to_dict(),
        "reasoning_log": reasoning_log.model_dump(mode="json"),
        "refinement": refinement_summary,
        "creativity_analyses": creativity_payload,
        "explanation": explanation,
    }
    trace = SolverTrace.model_validate(trace_payload)

    if output_dir:
        target = Path(output_dir)
        write_structured(target / "traces" / f"{trace.run_id}.json", trace)
        graph.save(target / "graphs" / f"{trace.run_id}.json")
        ledger.save(target / "run_ledgers" / f"{trace.run_id}.json")
        reasoning_log.save(target / "reasoning_logs" / f"{trace.run_id}.json")
        write_html_report(reasoning_log, target / "reports" / f"{trace.run_id}.html")
        for candidate in all_candidates:
            write_structured(target / "candidates" / f"{candidate.id}.json", candidate)
        for packet in all_packets:
            write_structured(target / "certificates" / f"{packet.candidate_id}.json", packet)

    return trace
