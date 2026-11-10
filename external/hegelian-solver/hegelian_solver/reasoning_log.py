# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Public, machine-readable reasoning log construction.

This module records the solver's observable reasoning process: stage purposes,
inputs, outputs, checks, decisions, assumptions, and unknowns. It does not expose
hidden chain-of-thought; it is a structured audit log for users and downstream tools.
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.graph import ConceptGraph
from hegelian_solver.schemas import (
    ConceptNode,
    DiscoverySignal,
    DomainProfile,
    FailureCertificate,
    RankingDecision,
    ReasoningLog,
    ReasoningLogStep,
    TransformationCandidate,
    ValidationPacket,
)


def _ids(items: list[Any]) -> list[str]:
    values: list[str] = []
    for item in items:
        if hasattr(item, "id"):
            values.append(str(item.id))
        elif isinstance(item, dict) and "id" in item:
            values.append(str(item["id"]))
    return values


def _top_decision(decisions: list[RankingDecision]) -> RankingDecision | None:
    for decision in decisions:
        if decision.decision in {"accept", "accept_as_branch", "provisional"}:
            return decision
    return decisions[0] if decisions else None


def _step(
    index: int,
    stage: str,
    title: str,
    human_summary: str,
    public_rationale: str,
    *,
    inputs: list[str] | None = None,
    outputs: list[str] | None = None,
    checks: list[dict[str, Any]] | None = None,
    decision: dict[str, Any] | None = None,
    machine_summary: dict[str, Any] | None = None,
    assumptions: list[str] | None = None,
    unknowns: list[str] | None = None,
    artifact_refs: dict[str, Any] | None = None,
) -> ReasoningLogStep:
    return ReasoningLogStep(
        index=index,
        stage=stage,
        title=title,
        human_summary=human_summary,
        public_rationale=public_rationale,
        inputs=inputs or [],
        outputs=outputs or [],
        checks=checks or [],
        decision=decision or {},
        machine_summary=machine_summary or {},
        assumptions=assumptions or [],
        unknowns=unknowns or [],
        artifact_refs=artifact_refs or {},
    )


def build_reasoning_log(
    *,
    run_id: str,
    profile: DomainProfile,
    concept: ConceptNode,
    task_packet: dict[str, Any],
    failures: list[FailureCertificate],
    signals: list[DiscoverySignal],
    candidates: list[TransformationCandidate],
    validation_packets: list[ValidationPacket],
    decisions: list[RankingDecision],
    graph: ConceptGraph,
    explanation: str,
    refinement_summary: dict[str, Any] | None = None,
    creativity_analyses: list[dict[str, Any]] | None = None,
) -> ReasoningLog:
    refinement_summary = refinement_summary or {"iterations": [], "stop_reason": "n/a", "iterations_run": 1}
    creativity_analyses = creativity_analyses or []
    top = _top_decision(decisions)
    final_status = top.decision if top else "no_candidates"
    accepted_edges = [
        edge.id
        for edge in graph.edges.values()
        if edge.status in {"validated", "provisional", "accept", "accept_as_branch"}
    ]
    rejected = [decision for decision in decisions if decision.decision == "reject"]

    steps = [
        _step(
            1,
            "domain_profile",
            "Select Domain Profile",
            f"Selected `{profile.domain}` with schema `{profile.schema_kind}`.",
            "Domain routing decides the schema fields, failure taxonomy, validation gates, "
            "and ranking features before any concept transformation is attempted.",
            inputs=["raw concept payload"],
            outputs=["domain_profile"],
            checks=[
                {"name": "required_fields_declared", "status": bool(profile.required_fields)},
                {"name": "validation_gates_declared", "status": bool(profile.validation_gates)},
            ],
            decision={
                "domain": profile.domain,
                "schema_kind": profile.schema_kind,
                "validation_gates": profile.validation_gates,
            },
            machine_summary=profile.model_dump(mode="json"),
            assumptions=profile.assumptions,
            unknowns=profile.unknowns,
        ),
        _step(
            2,
            "concept_formalization",
            "Normalize Seed Concept",
            f"Formalized `{concept.name}` as `{concept.id}`.",
            "The raw concept is separated into structure, tasks, examples, preservation "
            "constraints, assumptions, and unknowns so later stages can validate explicit fields.",
            inputs=["raw concept payload", "domain_profile"],
            outputs=[concept.id],
            checks=[
                {"name": "has_tasks", "status": bool(concept.tasks)},
                {"name": "has_preservation_constraints", "status": bool(concept.preservation)},
                {"name": "unknowns_recorded", "status": True, "count": len(concept.unknowns)},
            ],
            decision={"concept_id": concept.id, "status": concept.status},
            machine_summary={
                "domain": concept.domain,
                "task_count": len(concept.tasks),
                "example_count": len(concept.examples),
                "counterexample_count": len(concept.counterexamples),
                "reported_failure_count": len(concept.reported_failures),
                "preservation_count": len(concept.preservation),
                "formal_analysis": concept.formal_analysis,
                "material_analysis": concept.material_analysis,
                "epistemic_profile": concept.epistemic_profile,
                "source_refs": concept.source_refs,
            },
            assumptions=concept.assumptions
            + list(concept.epistemic_profile.get("assumptions", [])),
            unknowns=concept.unknowns + list(concept.epistemic_profile.get("unknowns", [])),
        ),
        _step(
            3,
            "task_evidence",
            "Curate Tasks and Evidence",
            f"Curated {len(task_packet.get('tasks', []))} tasks and "
            f"{len(task_packet.get('evidence', []))} evidence items.",
            "Tasks make the concept's intended role testable; evidence and examples remain "
            "separate from axioms and claims.",
            inputs=[concept.id],
            outputs=["task_evidence_packet"],
            checks=[
                {"name": "stress_tasks_added", "status": len(task_packet.get("tasks", [])) > len(concept.tasks)},
                {"name": "evidence_provenance_preserved", "status": True},
            ],
            decision={
                "task_ids": [task["id"] for task in task_packet.get("tasks", [])],
                "evidence_ids": [item["id"] for item in task_packet.get("evidence", [])],
            },
            machine_summary={
                "task_count": len(task_packet.get("tasks", [])),
                "evidence_count": len(task_packet.get("evidence", [])),
                "missing_evidence": task_packet.get("missing_evidence", []),
            },
            unknowns=task_packet.get("missing_evidence", []),
        ),
        _step(
            4,
            "failure_classification",
            "Classify Determinate Failures",
            f"Classified {len(failures)} failure certificates.",
            "Failures are useful only when typed with witnesses, failed obligations, traces, "
            "repair targets, and severity.",
            inputs=["task_evidence_packet", concept.id],
            outputs=_ids(failures),
            checks=[
                {"name": "each_failure_has_witness", "status": all(bool(f.witness) for f in failures)},
                {
                    "name": "each_failure_has_repair_target",
                    "status": all(bool(f.repair_target) for f in failures),
                },
            ],
            decision={"labels": [failure.label for failure in failures]},
            machine_summary={"failures": [failure.model_dump(mode="json") for failure in failures]},
            unknowns=[unknown for failure in failures for unknown in failure.unknowns],
        ),
        _step(
            5,
            "discovery_mining",
            "Mine Discovery Signals",
            f"Detected {len(signals)} discovery signals.",
            "Discovery signals capture abstraction pressure that is not reducible to a single "
            "failure, such as shared interfaces or invariant patterns.",
            inputs=[concept.id, "task_evidence_packet"],
            outputs=_ids(signals),
            checks=[
                {"name": "signals_have_candidate_moves", "status": all(bool(s.candidate_move) for s in signals)},
                {"name": "signals_have_evidence", "status": all(bool(s.evidence) for s in signals)},
            ],
            decision={"labels": [signal.label for signal in signals]},
            machine_summary={"signals": [signal.model_dump(mode="json") for signal in signals]},
            unknowns=[unknown for signal in signals for unknown in signal.unknowns],
        ),
        _step(
            6,
            "candidate_generation",
            "Generate Candidate Successors",
            f"Generated {len(candidates)} transformation candidates.",
            "Each candidate is a proposal only: it carries a preservation map, resolution "
            "mechanism, expected obligations, and residual limits before ranking.",
            inputs=_ids(failures) + _ids(signals),
            outputs=_ids(candidates),
            checks=[
                {
                    "name": "candidate_preservation_maps_present",
                    "status": all(bool(c.preservation_map) for c in candidates),
                },
                {
                    "name": "candidate_residual_limits_present",
                    "status": all(bool(c.residual_limits) for c in candidates),
                },
            ],
            decision={"operators": [candidate.operator for candidate in candidates]},
            machine_summary={"candidates": [candidate.model_dump(mode="json") for candidate in candidates]},
            assumptions=[assumption for candidate in candidates for assumption in candidate.assumptions],
            unknowns=[unknown for candidate in candidates for unknown in candidate.unknowns],
        ),
        _step(
            7,
            "validation",
            "Generate Validation Obligations",
            f"Generated {sum(len(p.obligations) for p in validation_packets)} obligations across "
            f"{len(validation_packets)} validation packets.",
            "Validation records public proof plans, hard gates, partial checks, failed checks, "
            "and unknowns. Planned or partial obligations are not treated as passed.",
            inputs=_ids(candidates),
            outputs=[packet.candidate_id for packet in validation_packets],
            checks=[
                {
                    "name": "unknown_or_planned_not_passing",
                    "status": all(
                        obligation.status != "passed" or obligation.evidence
                        for packet in validation_packets
                        for obligation in packet.obligations
                    ),
                },
                {
                    "name": "hard_gate_failures_recorded",
                    "status": all(isinstance(packet.hard_gate_failures, list) for packet in validation_packets),
                },
            ],
            decision={
                "hard_gate_failures": {
                    packet.candidate_id: packet.hard_gate_failures for packet in validation_packets
                }
            },
            machine_summary={
                "validation_packets": [packet.model_dump(mode="json") for packet in validation_packets]
            },
        ),
        _step(
            8,
            "ranking",
            "Rank and Gate Candidates",
            f"Ranked {len(decisions)} candidates; top status is `{final_status}`.",
            "Ranking applies hard gates before score interpretation and keeps provisional "
            "status when obligations are still open.",
            inputs=[packet.candidate_id for packet in validation_packets],
            outputs=[decision.candidate_id for decision in decisions],
            checks=[
                {"name": "hard_gates_precede_scores", "status": True},
                {
                    "name": "rejections_have_reasons",
                    "status": all(bool(decision.reasons) for decision in rejected),
                },
            ],
            decision=top.model_dump(mode="json") if top else {"decision": "no_candidates"},
            machine_summary={"decisions": [decision.model_dump(mode="json") for decision in decisions]},
        ),
        _step(
            9,
            "conceptual_creativity",
            "Analyze Conceptual Creativity",
            f"Analyzed {len(creativity_analyses)} candidate(s): "
            f"{sum(1 for item in creativity_analyses if item.get('repair_vs_affordance') != 'repair')} "
            "introduce a new affordance rather than only repairing the trigger.",
            "Every candidate is classified into one of nine conceptual operations (closure "
            "completion, abstraction/interface discovery, invariance reparameterization, "
            "quotienting/redundancy removal, localization/regime restriction, "
            "externalization/tooling, bridge mediation, latent carrier introduction, "
            "governance/safety scaffold) and explicitly separated into repair versus "
            "affordance-creation, grounded in its own trigger, preservation map, and "
            "expected obligations rather than asserted free-form.",
            inputs=[item.get("candidate_id", "") for item in creativity_analyses],
            outputs=[item.get("id", "") for item in creativity_analyses],
            checks=[
                {
                    "name": "every_analysis_names_source_pressure_and_operation",
                    "status": all(item.get("source_pressure") and item.get("operation") for item in creativity_analyses),
                },
                {
                    "name": "unsupported_claims_recorded_as_residual_todos",
                    "status": all(isinstance(item.get("residual_todos"), list) for item in creativity_analyses),
                },
            ],
            decision={
                "repair_count": sum(1 for item in creativity_analyses if item.get("repair_vs_affordance") == "repair"),
                "affordance_creation_count": sum(
                    1 for item in creativity_analyses if item.get("repair_vs_affordance") == "affordance_creation"
                ),
                "mixed_count": sum(1 for item in creativity_analyses if item.get("repair_vs_affordance") == "mixed"),
            },
            machine_summary={"creativity_analyses": creativity_analyses},
        ),
        _step(
            10,
            "reflective_refinement",
            "Run Reflective Refinement Loop",
            f"Ran {refinement_summary.get('iterations_run', 1)} iteration(s); stopped because "
            f"`{refinement_summary.get('stop_reason', 'n/a')}`.",
            "Each iteration treats the best candidate's own open obligations as new "
            "determinate negations of its target concept and re-proposes against it, bounded "
            "by a max-iteration safety net and a score-plateau check (see "
            "hegelian_solver.orchestrator for the stopping-criteria rationale).",
            inputs=[entry["concept_id"] for entry in refinement_summary.get("iterations", [])],
            outputs=[str(entry["top_candidate_id"]) for entry in refinement_summary.get("iterations", []) if entry.get("top_candidate_id")],
            checks=[
                {
                    "name": "bounded_by_max_iterations",
                    "status": refinement_summary.get("iterations_run", 1) <= refinement_summary.get("max_iterations", 1),
                },
                {"name": "stop_reason_recorded", "status": bool(refinement_summary.get("stop_reason"))},
            ],
            decision={"stop_reason": refinement_summary.get("stop_reason")},
            machine_summary=refinement_summary,
        ),
        _step(
            11,
            "graph_update",
            "Serialize Concept Graph Update",
            f"Graph contains {len(graph.nodes)} nodes, {len(graph.edges)} edges, and "
            f"{len(graph.rejected_candidates)} rejected candidates.",
            "Accepted and provisional successors become graph nodes and edges; rejected "
            "candidates are retained as boundary evidence.",
            inputs=[decision.candidate_id for decision in decisions],
            outputs=list(graph.edges),
            checks=[
                {"name": "edge_trigger_ids_present", "status": all(edge.trigger.get("id") for edge in graph.edges.values())},
                {
                    "name": "residual_limits_attached",
                    "status": all(edge.residual_limits for edge in graph.edges.values()),
                },
            ],
            decision={"accepted_or_provisional_edges": accepted_edges},
            machine_summary=graph.to_dict(),
        ),
        _step(
            12,
            "explanation",
            "Render Public Explanation",
            explanation,
            "The explanation summarizes the public dialectical move without exposing hidden "
            "chain-of-thought: trigger, transformation, preservation, obligations, decision, "
            "and residual limits.",
            inputs=list(graph.edges),
            outputs=["explanation"],
            checks=[
                {"name": "distinguishes_verified_from_provisional", "status": "candidate repair" in explanation or "verified Aufhebung" in explanation},
            ],
            decision={"final_status": final_status},
            machine_summary={"explanation": explanation},
        ),
    ]

    machine_index = {
        "concept": concept.id,
        "domain": profile.domain,
        "failures": _ids(failures),
        "discovery_signals": _ids(signals),
        "candidates": _ids(candidates),
        "validation_packets": [packet.candidate_id for packet in validation_packets],
        "ranking_decisions": [decision.candidate_id for decision in decisions],
        "graph_edges": list(graph.edges),
        "graph_nodes": list(graph.nodes),
        "source_refs": concept.source_refs,
        "formal_material_epistemic": {
            "formal": bool(concept.formal_analysis),
            "material": bool(concept.material_analysis),
            "epistemic": bool(concept.epistemic_profile),
        },
    }
    return ReasoningLog(
        run_id=run_id,
        concept_id=concept.id,
        concept_name=concept.name,
        domain=concept.domain,
        summary=explanation,
        final_status=final_status,
        steps=steps,
        machine_index=machine_index,
        provenance={
            "kind": "public_solver_reasoning_log",
            "chain_of_thought": "not included",
            "refs_used": profile.refs_used,
        },
        creativity_analyses=creativity_analyses,
    )
