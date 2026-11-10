#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Shared policy for when to invoke local memory, local generative search, and external search."""

from __future__ import annotations

from typing import Any


def _clean_text(value: Any) -> str:
    """Normalize a free-form value into a stable one-line policy string."""

    return " ".join(str(value or "").strip().split())


def _ensure_list(value: Any) -> list[Any]:
    """Normalize arbitrary values into list-shaped policy payloads."""

    return value if isinstance(value, list) else []


def build_knowledge_source_policy(
    *,
    stage: str,
    target_label: str = "",
    target_kind: str = "",
    mathlib_hit_count: int = 0,
    external_framework_recommended: bool = False,
) -> dict[str, Any]:
    """Build a stage-aware source-selection rubric for local memory, local generation, and browsing."""

    stage_label = _clean_text(stage).lower() or "analysis"
    target = _clean_text(target_label) or "current route"
    kind = _clean_text(target_kind) or "theorem-shaped target"

    mathlib_policy = {
        "source": "InformalMathLib",
        "role": "local theorem, definition, barrier, and prior-result retrieval",
        "default_action": "query-first",
        "invoke_when": [
            _clean_text(f"The current {kind} may already be locally grounded for `{target}`."),
            "A named theorem, route lemma, barrier, or prior negative result might already exist locally.",
            "Novelty or prior-art status cannot be assessed without checking local memory first.",
        ],
        "do_not_use_for": [
            "inventing a new bridge object by analogy alone",
            "claiming closure when the local hit is only topically related",
        ],
        "success_condition": "Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.",
        "current_signal": f"current_mathlib_hits={max(0, int(mathlib_hit_count))}",
    }

    generative_policy = {
        "source": "IDE generative search",
        "role": "local candidate generation for bridge objects, invariants, decompositions, and representation shifts",
        "default_action": "use-after-local-grounding",
        "invoke_when": [
            _clean_text(f"Local KB and InformalMathLib ground `{target}`, but the missing move is still conceptual rather than factual."),
            "The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate.",
            "The output can remain conjectural until independently grounded or refuted.",
        ],
        "do_not_use_for": [
            "claiming prior art",
            "fabricating exact theorem statements or bibliographic facts",
            "promoting analogy directly into InformalMathLib without proof relevance",
        ],
        "success_condition": "A generative suggestion is admissible only if it sharpens the theorem shape, negative route, or abstraction type; it is not evidence by itself.",
    }

    web_policy = {
        "source": "web search",
        "role": "external exact theorem, prior-art, or framework retrieval",
        "default_action": "last-resort-decisive-only",
        "invoke_when": [
            "A decisive exact theorem statement, prior-art fact, threshold, or barrier is still missing after local KB and InformalMathLib lookup.",
            "A local-search failure has been recorded and materially blocks the proof or novelty decision.",
            "The query can be stated concretely as a named theorem, paper, author, framework, or model-specific fact.",
        ],
        "do_not_use_for": [
            "generic background reading",
            "decorative references",
            "replacing local conceptual search with unbounded browsing",
        ],
        "success_condition": "If an external theorem, definition, axiom, or named framework becomes proof-relevant, record the exact query and import the result into InformalMathLib.",
        "foundation_search_recommended": bool(external_framework_recommended),
    }

    consistency_rules = [
        "Query local KB and InformalMathLib before any web search.",
        "Use IDE/generative search only after theorem grounding is explicit enough to state what kind of missing move is under search.",
        "Do not treat generative candidates as evidence; they remain conjectural until grounded, refuted, or externally validated.",
        "Do not claim novelty until both local memory and any required decisive prior-art gate have been checked.",
        "If browsing changes the proof state, record what exact statement changed and import proof-relevant external results into InformalMathLib.",
    ]
    escalation_rules = [
        "Stay in InformalMathLib/local mode when the issue is retrieval of a known local dependency.",
        "Escalate to IDE/generative search when the issue is missing abstraction or representation, not missing factual attribution.",
        "Escalate to web search only when the issue is exact external prior art, exact theorem text, or a missing external framework foundation that local artifacts cannot settle.",
    ]

    return {
        "stage": stage_label,
        "target_label": target,
        "target_kind": kind,
        "sources": [mathlib_policy, generative_policy, web_policy],
        "consistency_rules": consistency_rules,
        "escalation_rules": escalation_rules,
    }


def render_knowledge_source_policy_markdown(policy: dict[str, Any]) -> list[str]:
    """Render the shared source-selection policy into Markdown lines for dossiers and reports."""

    lines = [
        f"- Stage: {_clean_text(policy.get('stage'))}",
        f"- Target: {_clean_text(policy.get('target_label'))}",
        f"- Target kind: {_clean_text(policy.get('target_kind'))}",
        "",
        "### Source Order",
        "",
    ]
    for row in [item for item in _ensure_list(policy.get("sources")) if isinstance(item, dict)]:
        lines.append(f"- `{_clean_text(row.get('source'))}` | role={_clean_text(row.get('role'))} | default={_clean_text(row.get('default_action'))}")
        invoke_when = [_clean_text(item) for item in _ensure_list(row.get("invoke_when")) if _clean_text(item)]
        if invoke_when:
            lines.append("  Invoke when: " + " ".join(invoke_when))
        do_not = [_clean_text(item) for item in _ensure_list(row.get("do_not_use_for")) if _clean_text(item)]
        if do_not:
            lines.append("  Do not use for: " + " ".join(do_not))
        success = _clean_text(row.get("success_condition"))
        if success:
            lines.append(f"  Success condition: {success}")
        current_signal = _clean_text(row.get("current_signal"))
        if current_signal:
            lines.append(f"  Current signal: {current_signal}")
    lines.extend(["", "### Consistency Rules", ""])
    for item in [_clean_text(value) for value in _ensure_list(policy.get("consistency_rules")) if _clean_text(value)]:
        lines.append(f"- {item}")
    lines.extend(["", "### Escalation Rules", ""])
    for item in [_clean_text(value) for value in _ensure_list(policy.get("escalation_rules")) if _clean_text(value)]:
        lines.append(f"- {item}")
    return lines
