# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Task and evidence curation.

Runs right after a concept is formalized, before failure classification. Two jobs:
(1) turn each `example`/`counterexample` into a typed `Evidence` record with its claim and
provenance kept separate from axioms; (2) add deterministic "stress tasks" (closure,
solvability, completeness, invariance, rigidity, non-collapse, residual-limit scan) plus
domain-specific tasks (physics: limiting-case recovery, measurement interface; LM: source
provenance, tool use, prompt injection, governance, latency/cost) on top of whatever tasks
the concept already declared. This is what guarantees every concept gets exercised by the
same baseline questions regardless of how thin its own authored tasks are.
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, Evidence, Task


def _task(name: str, kind: str, concept: ConceptNode, **kwargs: Any) -> Task:
    payload = {
        "name": name,
        "kind": kind,
        "goal": kwargs.pop("goal", name.replace("_", " ")),
        "context": {"concept": concept.id, **kwargs.pop("context", {})},
        **kwargs,
    }
    payload["id"] = stable_id("task", payload)
    return Task.model_validate(payload)


def curate_tasks_and_evidence(concept: ConceptNode) -> dict[str, Any]:
    tasks = list(concept.tasks)
    evidence: list[Evidence] = []

    for index, example in enumerate(concept.examples):
        payload = {
            "type": "example",
            "source": concept.id,
            "claim_supported": f"{concept.name} motivating example",
            "notes": [str(example)],
        }
        payload["id"] = stable_id("evidence", {"concept": concept.id, "example": index, "value": example})
        evidence.append(Evidence.model_validate(payload))

    for index, counterexample in enumerate(concept.counterexamples):
        payload = {
            "type": "counterexample",
            "source": concept.id,
            "claim_supported": f"{concept.name} known limitation",
            "notes": [str(counterexample)],
        }
        payload["id"] = stable_id(
            "evidence", {"concept": concept.id, "counterexample": index, "value": counterexample}
        )
        evidence.append(Evidence.model_validate(payload))

    stress = [
        ("closure_check", "construct", "check operation closure"),
        ("solvability_check", "construct", "check solution existence"),
        ("completeness_check", "complete", "check missing limits or completions"),
        ("invariance_check", "check_invariance", "check representation invariance"),
        ("rigidity_check", "classify", "check whether equality is too strict"),
        ("noncollapse_check", "prove", "check protected distinctions"),
        ("residual_limit_scan", "discover", "search remaining limitations"),
    ]
    existing_names = {task.name for task in tasks}
    for name, kind, goal in stress:
        if name not in existing_names:
            tasks.append(_task(name, kind, concept, goal=goal))

    if concept.domain == "physical_concept":
        tasks.append(
            _task(
                "limiting_case_recovery",
                "derive_limit",
                concept,
                goal="recover protected predecessor predictions in declared regimes",
                regime=getattr(concept, "regime", None) or None,
            )
        )
        tasks.append(
            _task(
                "measurement_interface_check",
                "instrumentalize",
                concept,
                goal="map theoretical observables to measurement procedures",
                regime=getattr(concept, "regime", None) or None,
            )
        )

    if concept.domain == "language_model_concept":
        for name, kind, goal in [
            ("source_provenance_check", "check_invariance", "verify claims are source supported"),
            ("tool_use_check", "compute", "validate tool selection and schema correctness"),
            ("prompt_injection_check", "simulate", "test hierarchy and taint resistance"),
            ("governance_check", "classify", "check monitoring and deployment controls"),
            ("latency_cost_check", "compute", "check declared product latency and cost regime"),
        ]:
            tasks.append(_task(name, kind, concept, goal=goal))

    return {
        "tasks": [task.model_dump(mode="json") for task in tasks],
        "evidence": [item.model_dump(mode="json") for item in evidence],
        "examples": concept.examples,
        "counterexamples": concept.counterexamples,
        "trace_refs": getattr(concept, "traces", []),
        "missing_evidence": concept.unknowns,
        "evaluation_notes": ["curated by deterministic MVP heuristics"],
    }
