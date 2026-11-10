# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Failure classification heuristics.

This is the solver's "determinate negation" stage: it turns a concept's counterexamples
and reported failures/anomalies into typed `FailureCertificate`s (witness, failed
obligation, trace, repair target, severity) instead of leaving them as untyped prose. Every
certificate's `label` comes from the relevant domain's failure taxonomy in `domain.py`
(`MATH_FAILURES`/`PHYSICS_FAILURES`/`LM_FAILURES`), and `REPAIR_TARGETS` maps each label to
the operator name(s) in `operators/library.py` that are expected to address it.

NOTE: `REPAIR_TARGETS` here and `FAILURE_TO_OPERATORS` in `operators/library.py` are two
separately maintained copies of the same label -> operator mapping and have already drifted
for a couple of labels (see TODO.md Phase 19) — treat this file's table as documentation/
repair_target hints, and `operators/library.py`'s table as authoritative for which operator
actually gets proposed.
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, FailureCertificate


REPAIR_TARGETS = {
    "NonClosure": ["CompleteClosure", "GroupCompletion"],
    "NonSolvability": ["AlgebraicAdjunction"],
    "Incompleteness": ["Completion"],
    "NonInvariance": ["Invariantize", "Quotient"],
    "Rigidity": ["WeakenEquivalence"],
    "Inconsistency": ["TypeStratify"],
    "NonRepresentability": ["AbstractInterface"],
    "PoorTransfer": ["AbstractInterface"],
    "CaseExplosion": ["WeakenAxioms", "AbstractInterface"],
    "EmpiricalAnomaly": ["IntroduceLatentCarrier", "ReviseDynamics"],
    "Overextension": ["RestrictRegime"],
    "NonCovariance": ["InvariantizeKinematics"],
    "RepresentationDependence": ["GaugeQuotient", "Invariantize"],
    "ScaleMismatch": ["CoarseGrain", "Renormalize"],
    "MeasurementGap": ["MeasurementModelEnrichment"],
    "NoLimitingCase": ["RejectCandidate"],
    "Hallucination": ["Retrieve", "Verify"],
    "NoProvenance": ["Retrieve", "Verify"],
    "PromptInjection": ["SecureRAG", "TaintTracking"],
    "ToolMisuse": ["Toolify", "Verify"],
    "OverRefusal": ["CalibrateSafetyPolicy"],
    "PlanningMyopia": ["Agentify", "AddState"],
    "GovernanceGap": ["Govern"],
}


def _label_from_text(text: str, domain: str) -> str:
    """Guess a failure label from free text when no explicit `label` is given.

    First-match keyword search, scoped per domain; falls back to a domain-appropriate
    default (`EmpiricalAnomaly` / `Hallucination` / `NonRepresentability`) when nothing
    matches. Prefer supplying an explicit `label` on reported failures when authoring
    fixtures — this is a convenience fallback, not a reliable classifier.
    """

    lower = text.lower()
    if domain == "physical_concept":
        if "regime" in lower or "outside" in lower:
            return "Overextension"
        if "covarian" in lower or "lorentz" in lower or "frame" in lower:
            return "NonCovariance"
        if "measurement" in lower:
            return "MeasurementGap"
        if "limit" in lower or "newtonian" in lower:
            return "NoLimitingCase"
        return "EmpiricalAnomaly"
    if domain == "language_model_concept":
        if "source" in lower or "provenance" in lower or "citation" in lower:
            return "NoProvenance"
        if "prompt injection" in lower or "injection" in lower:
            return "PromptInjection"
        if "tool" in lower:
            return "ToolMisuse"
        if "refusal" in lower:
            return "OverRefusal"
        if "plan" in lower or "loop" in lower:
            return "PlanningMyopia"
        if "govern" in lower or "monitor" in lower:
            return "GovernanceGap"
        return "Hallucination"
    if "closure" in lower or "not in" in lower or "partial" in lower:
        return "NonClosure"
    if "solution" in lower or "solv" in lower:
        return "NonSolvability"
    if "complete" in lower or "cauchy" in lower or "limit" in lower:
        return "Incompleteness"
    if "invariant" in lower or "coordinate" in lower or "representation" in lower:
        return "NonInvariance"
    if "rigid" in lower or "equality" in lower or "isomorphism" in lower:
        return "Rigidity"
    if "inconsisten" in lower or "paradox" in lower:
        return "Inconsistency"
    if "transfer" in lower:
        return "PoorTransfer"
    return "NonRepresentability"


def classify_failures(concept: ConceptNode, task_packet: dict[str, Any] | None = None) -> list[FailureCertificate]:
    """Build one `FailureCertificate` per counterexample / reported failure / anomaly.

    Three sources, in order: the concept's own `counterexamples`; failures surfaced by
    `evidence.curate_tasks_and_evidence` plus the concept's `reported_failures`/`anomalies`;
    and, only if literally nothing else was found and the concept also has no `examples`, a
    single synthetic low-severity certificate noting the evidence gap (so a thin concept
    still produces at least one trigger for the rest of the pipeline to act on).
    """
    failures: list[FailureCertificate] = []

    for index, item in enumerate(concept.counterexamples):
        text = str(item)
        label = _label_from_text(text, concept.domain)
        payload = {
            "label": label,
            "concept": concept.id,
            "witness": {"type": "counterexample", "value": item},
            "failed_obligation": text,
            "trace": [concept.id, f"counterexamples[{index}]"],
            "repair_target": REPAIR_TARGETS.get(label, ["AbstractInterface"]),
            "severity": "high",
            "regime": getattr(concept, "regime", None) or None,
        }
        payload["id"] = stable_id("failure", payload)
        failures.append(FailureCertificate.model_validate(payload))

    raw_failures = []
    if isinstance(task_packet, dict):
        raw_failures.extend(task_packet.get("failures", []))
    raw_failures.extend(getattr(concept, "reported_failures", []))
    raw_failures.extend(getattr(concept, "anomalies", []))

    for index, item in enumerate(raw_failures):
        if isinstance(item, dict):
            text = str(item.get("failed_obligation") or item.get("description") or item)
            label = item.get("label") or _label_from_text(text, concept.domain)
            payload = {
                "label": label,
                "concept": concept.id,
                "witness": item.get("witness", {"type": "reported_failure", "value": item}),
                "failed_obligation": text,
                "trace": item.get("trace", [concept.id, f"failures[{index}]"]),
                "repair_target": item.get("repair_target", REPAIR_TARGETS.get(label, ["AbstractInterface"])),
                "severity": item.get("severity", "medium"),
                "regime": item.get("regime", getattr(concept, "regime", None) or None),
                "residual": item.get("residual"),
                "uncertainty": item.get("uncertainty"),
            }
        else:
            text = str(item)
            label = _label_from_text(text, concept.domain)
            payload = {
                "label": label,
                "concept": concept.id,
                "witness": {"type": "reported_failure", "value": item},
                "failed_obligation": text,
                "trace": [concept.id, f"failures[{index}]"],
                "repair_target": REPAIR_TARGETS.get(label, ["AbstractInterface"]),
                "severity": "medium",
                "regime": getattr(concept, "regime", None) or None,
            }
        payload["id"] = stable_id("failure", payload)
        failures.append(FailureCertificate.model_validate(payload))

    if not failures and not concept.examples:
        payload = {
            "label": "NonRepresentability",
            "concept": concept.id,
            "witness": {"type": "missing_evidence", "value": "no examples or counterexamples"},
            "failed_obligation": "concept lacks enough evidence for evaluation",
            "trace": [concept.id, "unknowns"],
            "repair_target": ["TaskEvidenceCuration"],
            "severity": "low",
            "unknowns": ["no concrete witness supplied"],
        }
        payload["id"] = stable_id("failure", payload)
        failures.append(FailureCertificate.model_validate(payload))

    return failures
