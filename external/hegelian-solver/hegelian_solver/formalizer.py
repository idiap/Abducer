# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Concept formalization from raw YAML/JSON/prose dictionaries.

`formalize_concept` is the prose-to-draft adapter: it takes whatever shape a user or
fixture handed in (a dict with author-chosen key names, a bare string, or an already-typed
`ConceptNode`) and produces a strict `ConceptNode`/`PhysicalConcept`/`LanguageModelConcept`.
It accepts many historical/alternate key spellings (`axioms` or `axioms_or_constraints`,
`preserve` or `preservation`, `models` or `admissible_models`, ...) so existing fixtures
don't need to be rewritten when the canonical schema field names settle. Required fields
declared by the `DomainProfile` that are still missing after this pass are recorded as
explicit `unknowns` rather than silently defaulted or hallucinated.
"""

from __future__ import annotations

from typing import Any

from hegelian_solver.domain import domain_profile
from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, DomainProfile, LanguageModelConcept, PhysicalConcept, Task


def _task_from_raw(raw: Any, index: int) -> Task:
    if isinstance(raw, Task):
        return raw
    if isinstance(raw, str):
        payload = {"name": raw, "kind": "prove", "goal": raw}
    elif isinstance(raw, dict):
        payload = dict(raw)
    else:
        payload = {"name": f"task-{index}", "kind": "inspect", "goal": str(raw)}
    payload.setdefault("id", stable_id("task", payload))
    payload.setdefault("name", payload["id"])
    payload.setdefault("kind", "inspect")
    payload.setdefault("goal", payload.get("formula") or payload.get("target") or payload["name"])
    payload.setdefault("required_status", payload.get("required", "success"))
    return Task.model_validate(payload)


def _base_payload(raw: dict[str, Any], profile: DomainProfile) -> dict[str, Any]:
    name = str(raw.get("name") or raw.get("concept") or raw.get("id") or "UnnamedConcept")
    payload = {
        "id": raw.get("id") or stable_id("concept", {"name": name, "domain": profile.domain}),
        "name": name,
        "domain": profile.domain,
        "role": raw.get("role") or raw.get("description", ""),
        "signature": raw.get("signature", raw.get("typed_signature", {})),
        "axioms_or_constraints": raw.get("axioms_or_constraints", raw.get("axioms", [])),
        "admissible_models": raw.get("admissible_models", raw.get("models", [])),
        "tasks": [_task_from_raw(task, i) for i, task in enumerate(raw.get("tasks", []))],
        "interface": raw.get("interface", raw.get("operations", [])),
        "preservation": raw.get("preservation", raw.get("preserve", [])),
        "examples": raw.get("examples", []),
        "counterexamples": raw.get("counterexamples", []),
        "reported_failures": raw.get("reported_failures", raw.get("anomalies", raw.get("failures", []))),
        "invariants": raw.get("invariants", []),
        "equivalences": raw.get("equivalences", []),
        "representation_maps": raw.get("representation_maps", []),
        "history": raw.get("history", []),
        "allowed_operators": raw.get("allowed_operators", raw.get("operators", [])),
        "formal_analysis": raw.get("formal_analysis", {}),
        "material_analysis": raw.get("material_analysis", {}),
        "epistemic_profile": raw.get("epistemic_profile", {}),
        "source_refs": raw.get("source_refs", []),
        "status": raw.get("status", "draft"),
        "assumptions": raw.get("assumptions", []),
        "unknowns": raw.get("unknowns", []),
    }
    missing = [field for field in profile.required_fields if not payload.get(field) and field in payload]
    payload["unknowns"].extend([f"missing required field: {field}" for field in missing])
    return payload


def formalize_concept(raw: Any, profile: DomainProfile | None = None) -> ConceptNode:
    if isinstance(raw, ConceptNode):
        return raw
    if not isinstance(raw, dict):
        raw = {"name": "ProseConcept", "description": str(raw)}
    profile = profile or domain_profile(raw)
    payload = _base_payload(raw, profile)

    if profile.domain == "physical_concept":
        payload.update(
            {
                "ontology": raw.get("ontology", {}),
                "state_space": raw.get("state_space"),
                "observables": raw.get("observables", raw.get("quantities", {}).get("observables", [])),
                "dynamics": raw.get("dynamics", {}),
                "symmetries": raw.get("symmetries", {}),
                "parameters": raw.get("parameters", {}),
                "measurement_model": raw.get("measurement_model", raw.get("measurement", {})),
                "regime": raw.get("regime", {}),
                "evidence_summary": raw.get("evidence_summary", raw.get("evidence", {})),
                "anomalies": raw.get("anomalies", []),
                "limiting_cases": raw.get("limiting_cases", []),
                "maturity_status": raw.get("maturity_status", raw.get("status", "provisional")),
            }
        )
        return PhysicalConcept.model_validate(payload)

    if profile.domain == "language_model_concept":
        payload.update(
            {
                "representation": raw.get("representation", {}),
                "architecture": raw.get("architecture", {}),
                "data": raw.get("data", {}),
                "objective": raw.get("objective", {}),
                "interaction": raw.get("interaction", {}),
                "tools": raw.get("tools", []),
                "evaluation": raw.get("evaluation", {}),
                "safety": raw.get("safety", {}),
                "governance": raw.get("governance", {}),
                "traces": raw.get("traces", []),
                "deployment_context": raw.get("deployment_context", {}),
            }
        )
        return LanguageModelConcept.model_validate(payload)

    return ConceptNode.model_validate(payload)
