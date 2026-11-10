# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Pydantic models for public solver artifacts.

These are the canonical types every other module in `hegelian_solver` reads and writes —
`StrictModel` (extra="forbid") is the base for all of them, so a typo'd field name fails
fast instead of silently being dropped. The models roughly follow the solver's own pipeline
stages: `DomainProfile` (routing) -> `ConceptNode`/`PhysicalConcept`/`LanguageModelConcept`
(the concept itself) -> `Task`/`Evidence` (what's being tested) ->
`FailureCertificate`/`DiscoverySignal` (triggers) -> `TransformationCandidate` (a proposed
move) -> `Obligation`/`ValidationPacket` (is the move justified) -> `RankingDecision`
(accept/reject/branch) -> `ConceptGraphNode`/`ConceptGraphEdge` (persisted result) ->
`ReasoningLog`/`SolverTrace` (the full public record of one run). Mechanism reasoning
packets live in the sibling `schemas/mechanisms.py` module to avoid a circular import (see
the `ReasoningLog.mechanisms` field below) but are merged into `all_schema_models()` via
`schemas/__init__.py`.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


DomainName = Literal[
    "mathematical_concept",
    "physical_concept",
    "language_model_concept",
    "generic_concept",
]


class DomainProfile(StrictModel):
    domain: DomainName
    schema_kind: str
    required_fields: list[str] = Field(default_factory=list)
    failure_taxonomy: list[str] = Field(default_factory=list)
    discovery_taxonomy: list[str] = Field(default_factory=list)
    validation_gates: list[str] = Field(default_factory=list)
    ranking_features: list[str] = Field(default_factory=list)
    refs_used: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class Task(StrictModel):
    id: str
    name: str
    kind: str
    context: dict[str, Any] = Field(default_factory=dict)
    goal: str
    required_status: str = "success"
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    regime: dict[str, Any] | None = None
    tolerance: dict[str, Any] | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    expected_output: Any | None = None


class Evidence(StrictModel):
    id: str
    type: str
    source: str
    claim_supported: str
    reliability: str = "unknown"
    regime: dict[str, Any] | None = None
    uncertainty: dict[str, Any] | None = None
    provenance: dict[str, Any] | None = None
    notes: list[str] = Field(default_factory=list)


class ConceptNode(StrictModel):
    id: str
    name: str
    domain: DomainName = "generic_concept"
    role: str = ""
    signature: dict[str, Any] = Field(default_factory=dict)
    axioms_or_constraints: list[Any] = Field(default_factory=list)
    admissible_models: list[Any] = Field(default_factory=list)
    tasks: list[Task] = Field(default_factory=list)
    interface: list[Any] = Field(default_factory=list)
    preservation: list[Any] = Field(default_factory=list)
    examples: list[Any] = Field(default_factory=list)
    counterexamples: list[Any] = Field(default_factory=list)
    reported_failures: list[Any] = Field(default_factory=list)
    invariants: list[Any] = Field(default_factory=list)
    equivalences: list[Any] = Field(default_factory=list)
    representation_maps: list[Any] = Field(default_factory=list)
    history: list[Any] = Field(default_factory=list)
    allowed_operators: list[str] = Field(default_factory=list)
    formal_analysis: dict[str, Any] = Field(default_factory=dict)
    material_analysis: dict[str, Any] = Field(default_factory=dict)
    epistemic_profile: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[str] = Field(default_factory=list)
    status: str = "draft"
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class PhysicalConcept(ConceptNode):
    domain: Literal["physical_concept"] = "physical_concept"
    ontology: dict[str, Any] = Field(default_factory=dict)
    state_space: Any | None = None
    observables: list[Any] = Field(default_factory=list)
    dynamics: dict[str, Any] = Field(default_factory=dict)
    symmetries: dict[str, Any] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    measurement_model: dict[str, Any] = Field(default_factory=dict)
    regime: dict[str, Any] = Field(default_factory=dict)
    evidence_summary: dict[str, Any] = Field(default_factory=dict)
    anomalies: list[Any] = Field(default_factory=list)
    limiting_cases: list[Any] = Field(default_factory=list)
    maturity_status: str = "provisional"


class LanguageModelConcept(ConceptNode):
    domain: Literal["language_model_concept"] = "language_model_concept"
    representation: dict[str, Any] = Field(default_factory=dict)
    architecture: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)
    objective: dict[str, Any] = Field(default_factory=dict)
    interaction: dict[str, Any] = Field(default_factory=dict)
    tools: list[Any] = Field(default_factory=list)
    evaluation: dict[str, Any] = Field(default_factory=dict)
    safety: dict[str, Any] = Field(default_factory=dict)
    governance: dict[str, Any] = Field(default_factory=dict)
    traces: list[Any] = Field(default_factory=list)
    deployment_context: dict[str, Any] = Field(default_factory=dict)


class FailureCertificate(StrictModel):
    id: str
    label: str
    concept: str
    witness: dict[str, Any] = Field(default_factory=dict)
    failed_obligation: str
    trace: list[Any] = Field(default_factory=list)
    repair_target: list[str] = Field(default_factory=list)
    severity: str = "medium"
    regime: dict[str, Any] | None = None
    residual: dict[str, Any] | None = None
    uncertainty: dict[str, Any] | None = None
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class DiscoverySignal(StrictModel):
    id: str
    label: str
    evidence: list[Any] = Field(default_factory=list)
    latent_structure: dict[str, Any] = Field(default_factory=dict)
    candidate_move: str
    candidate_concept: str | None = None
    expected_obligations: list[str] = Field(default_factory=list)
    score: dict[str, float] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class TransformationCandidate(StrictModel):
    id: str
    operator: str
    source_concepts: list[str] = Field(default_factory=list)
    target_concept: dict[str, Any]
    triggered_by: list[str] = Field(default_factory=list)
    preservation_map: dict[str, Any] = Field(default_factory=dict)
    resolution_mechanism: str
    changed_structure: list[str] = Field(default_factory=list)
    expected_obligations: list[str] = Field(default_factory=list)
    residual_limits: list[str] = Field(default_factory=list)
    rejected_alternatives: list[str] = Field(default_factory=list)
    ranking_features: dict[str, float] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)


class Obligation(StrictModel):
    id: str
    kind: str
    statement: str
    method: str = "review"
    status: Literal["passed", "failed", "partial", "unknown", "planned", "not_applicable"]
    evidence: list[Any] = Field(default_factory=list)
    blocker: str | None = None


class ValidationPacket(StrictModel):
    candidate_id: str
    obligations: list[Obligation] = Field(default_factory=list)
    hard_gate_failures: list[str] = Field(default_factory=list)
    summary: str = ""


class RankingDecision(StrictModel):
    candidate_id: str
    decision: Literal["accept", "accept_as_branch", "provisional", "defer", "reject"]
    score: float
    scores: dict[str, float] = Field(default_factory=dict)
    gate_results: dict[str, str] = Field(default_factory=dict)
    reasons: list[str] = Field(default_factory=list)


class ConceptGraphNode(StrictModel):
    id: str
    name: str
    domain: DomainName
    schema_version: str = "0.1"
    concept: dict[str, Any]
    status: str = "draft"
    created_from: list[str] = Field(default_factory=list)
    validation_status: dict[str, Any] = Field(default_factory=dict)


class ConceptGraphEdge(StrictModel):
    id: str
    source: str
    target: str
    relation: str
    trigger: dict[str, Any]
    operator: str
    map: dict[str, Any] = Field(default_factory=dict)
    regime: dict[str, Any] | None = None
    obligations: list[Any] = Field(default_factory=list)
    certificates: list[Any] = Field(default_factory=list)
    residual_limits: list[str] = Field(default_factory=list)
    ranking: dict[str, Any] = Field(default_factory=dict)
    status: str = "proposed"


class LedgerEntry(StrictModel):
    stage: str
    artifact_type: str
    payload: dict[str, Any]


class RunLedger(StrictModel):
    run_id: str
    entries: list[LedgerEntry] = Field(default_factory=list)

    def record(self, stage: str, artifact_type: str, payload: dict[str, Any]) -> None:
        self.entries.append(LedgerEntry(stage=stage, artifact_type=artifact_type, payload=payload))

    def latest(self, stage: str) -> LedgerEntry | None:
        for entry in reversed(self.entries):
            if entry.stage == stage:
                return entry
        return None

    def completed_stages(self) -> list[str]:
        return [entry.stage for entry in self.entries]

    def resume_payload(self) -> dict[str, Any]:
        return {entry.stage: entry.payload for entry in self.entries}

    def save(self, path: str) -> None:
        from hegelian_solver.io import write_structured

        write_structured(path, self.model_dump(mode="json"))

    @classmethod
    def load(cls, path: str) -> "RunLedger":
        from hegelian_solver.io import read_structured

        return cls.model_validate(read_structured(path))


class ReasoningLogStep(StrictModel):
    index: int
    stage: str
    title: str
    human_summary: str
    public_rationale: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    checks: list[dict[str, Any]] = Field(default_factory=list)
    decision: dict[str, Any] = Field(default_factory=dict)
    machine_summary: dict[str, Any] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    artifact_refs: dict[str, Any] = Field(default_factory=dict)


class ReasoningLog(StrictModel):
    run_id: str
    concept_id: str
    concept_name: str
    domain: DomainName
    summary: str
    final_status: str
    steps: list[ReasoningLogStep] = Field(default_factory=list)
    machine_index: dict[str, Any] = Field(default_factory=dict)
    provenance: dict[str, Any] = Field(default_factory=dict)
    # Provisional MechanismDossier dicts; stored loose here to avoid a schema-module
    # circular import, validate with MechanismDossier.model_validate(...) at point of use.
    mechanisms: list[dict[str, Any]] = Field(default_factory=list)
    # ConceptualCreativityAnalysis dicts, one per candidate (see hegelian_solver.creativity).
    creativity_analyses: list[dict[str, Any]] = Field(default_factory=list)

    def save(self, path: str) -> None:
        from hegelian_solver.io import write_structured

        write_structured(path, self.model_dump(mode="json"))

    @classmethod
    def load(cls, path: str) -> "ReasoningLog":
        from hegelian_solver.io import read_structured

        return cls.model_validate(read_structured(path))


class SolverTrace(StrictModel):
    run_id: str
    seed_nodes: list[dict[str, Any]] = Field(default_factory=list)
    tasks: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    failures: list[dict[str, Any]] = Field(default_factory=list)
    discovery_signals: list[dict[str, Any]] = Field(default_factory=list)
    candidates: list[dict[str, Any]] = Field(default_factory=list)
    validation_packets: list[dict[str, Any]] = Field(default_factory=list)
    ranking_decisions: list[dict[str, Any]] = Field(default_factory=list)
    graph_updates: dict[str, Any] = Field(default_factory=dict)
    reasoning_log: dict[str, Any] = Field(default_factory=dict)
    # Per-iteration history of the reflective refinement loop (see hegelian_solver.orchestrator).
    refinement: dict[str, Any] = Field(default_factory=dict)
    creativity_analyses: list[dict[str, Any]] = Field(default_factory=list)
    explanation: str = ""


class UseCaseSuiteItem(StrictModel):
    id: str
    name: str
    domain: DomainName
    status: Literal["passed", "failed"]
    run_id: str | None = None
    output_dir: str | None = None
    trace_file: str | None = None
    reasoning_log_file: str | None = None
    report_file: str | None = None
    final_status: str | None = None
    failure_count: int = 0
    discovery_signal_count: int = 0
    candidate_count: int = 0
    validation_packet_count: int = 0
    ranking_decision_count: int = 0
    formal_material_epistemic: dict[str, bool] = Field(default_factory=dict)
    error: str | None = None


class UseCaseSuiteResult(StrictModel):
    source_path: str
    output_dir: str
    total: int
    passed: int
    failed: int
    domain_counts: dict[str, int] = Field(default_factory=dict)
    validation_errors: list[str] = Field(default_factory=list)
    items: list[UseCaseSuiteItem] = Field(default_factory=list)


def all_schema_models() -> list[type[BaseModel]]:
    return [
        DomainProfile,
        Task,
        Evidence,
        ConceptNode,
        PhysicalConcept,
        LanguageModelConcept,
        FailureCertificate,
        DiscoverySignal,
        TransformationCandidate,
        Obligation,
        ValidationPacket,
        RankingDecision,
        ConceptGraphNode,
        ConceptGraphEdge,
        LedgerEntry,
        RunLedger,
        ReasoningLogStep,
        ReasoningLog,
        SolverTrace,
        UseCaseSuiteItem,
        UseCaseSuiteResult,
    ]
