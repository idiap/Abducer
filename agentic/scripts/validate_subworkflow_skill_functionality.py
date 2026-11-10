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

"""Validate that recent qualitative and Gedanken subworkflow skills are functional, not clone stubs."""

from __future__ import annotations

import re
from pathlib import Path

from agentic_common import ROOT, fail, rel


QUALITATIVE_SKILLS = {
    "skills/reasoning/qualitative-variable-isolator/SKILL.md": [
        "variable table",
        "independent variables",
        "hidden couplings",
        "safe variations",
    ],
    "skills/reasoning/physics-regime-map-builder/SKILL.md": [
        "regime axes",
        "transition surfaces",
        "regime cells",
        "cross-regime risks",
    ],
    "skills/reasoning/monotonicity-sensitivity-prober/SKILL.md": [
        "controlled variation",
        "driver",
        "response",
        "rate class",
        "sensitivity mechanism",
    ],
    "skills/reasoning/scale-asymptotic-reasoner/SKILL.md": [
        "candidate asymptotic",
        "dominant balance",
        "crossover scales",
        "uniformity statement",
    ],
    "skills/reasoning/qualitative-toy-model-builder/SKILL.md": [
        "toy carrier",
        "solution or execution",
        "baseline and variant",
        "transfer boundary",
    ],
    "skills/evaluation/dimensional-symmetry-constraint-checker/SKILL.md": [
        "dimensional check",
        "symmetry/invariance check",
        "constraint check",
        "conservation",
        "positivity",
    ],
    "skills/evaluation/limit-convergence-behavior-auditor/SKILL.md": [
        "limit map",
        "uniformity audit",
        "noncommuting-limit test",
        "leakage modes",
    ],
    "skills/evaluation/qualitative-physics-falsifier/SKILL.md": [
        "claim under attack",
        "weakest premises",
        "falsifier set",
        "disconfirmation criteria",
    ],
}


GEDANKEN_SKILLS = {
    "skills/evaluation/gedanken-need-assessor/SKILL.md": [
        "functional generation requirements",
        "live branch context",
        "why_not_direct_derivation_or_probe",
        "originating cycle ids",
    ],
    "skills/reasoning/gedanken-situation-designer/SKILL.md": [
        "functional generation requirements",
        "active branch blocker",
        "graph_update_action",
        "transfer certificate",
    ],
    "skills/reasoning/gedanken-counterfactual-variant-builder/SKILL.md": [
        "functional generation requirements",
        "demoting the baseline",
        "one-change-at-a-time",
        "predicted_change",
    ],
    "skills/evaluation/gedanken-transfer-guard/SKILL.md": [
        "functional generation requirements",
        "exact source object",
        "exact target object",
        "graph_update_action",
    ],
    "skills/orchestration/gedanken-followup-planner/SKILL.md": [
        "functional generation requirements",
        "success criterion",
        "demotion criterion",
        "validation command",
    ],
}


UI_PROMPTS = {
    "skills/reasoning/qualitative-variable-isolator/agents/openai.yaml": ["typed variable frame", "hidden couplings"],
    "skills/reasoning/physics-regime-map-builder/agents/openai.yaml": ["validity regimes", "transition surfaces"],
    "skills/reasoning/monotonicity-sensitivity-prober/agents/openai.yaml": ["driver-response", "rate class"],
    "skills/reasoning/scale-asymptotic-reasoner/agents/openai.yaml": ["candidate asymptotic", "dominant balance"],
    "skills/reasoning/qualitative-toy-model-builder/agents/openai.yaml": ["minimal concrete model", "baseline and variant"],
    "skills/evaluation/dimensional-symmetry-constraint-checker/agents/openai.yaml": ["dimensions", "symmetry", "positivity"],
    "skills/evaluation/limit-convergence-behavior-auditor/agents/openai.yaml": ["finite-to-limit", "uniformity"],
    "skills/evaluation/qualitative-physics-falsifier/agents/openai.yaml": ["weakest premises", "disconfirmation criteria"],
}


GENERIC_STUB_PHRASES = [
    "Use this skill to build qualitative physics understanding as typed relation work, not as loose explanatory prose.",
    "Always identify the mathematical object, variables, regimes, assumptions, relation behavior, edge cases, and validation handoff before claiming insight.",
]


def norm_words(text: str) -> set[str]:
    body = re.sub(r"^---.*?---", "", text, flags=re.DOTALL)
    return {word for word in re.findall(r"[a-z][a-z0-9-]{3,}", body.lower())}


def require_phrases(path: str, phrases: list[str]) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"missing skill artifact: {path}")
    text = full.read_text(encoding="utf-8-sig")
    lower = text.lower()
    for phrase in phrases:
        if phrase.lower() not in lower:
            fail(f"{path} missing functional phrase `{phrase}`")
    return text


def check_no_generic_stub(path: str, text: str) -> None:
    for phrase in GENERIC_STUB_PHRASES:
        if phrase in text:
            fail(f"{path} still contains generic cloned stub phrase")


def check_qualitative_distinctiveness(texts: dict[str, str]) -> None:
    paths = list(texts)
    word_sets = {path: norm_words(text) for path, text in texts.items()}
    for index, left in enumerate(paths):
        for right in paths[index + 1 :]:
            a = word_sets[left]
            b = word_sets[right]
            if not a or not b:
                fail(f"empty skill body while checking {left} and {right}")
            similarity = len(a & b) / len(a | b)
            if similarity > 0.72:
                fail(f"{rel(ROOT / left)} and {rel(ROOT / right)} are too similar for distinct qualitative functions ({similarity:.2f})")


def main() -> int:
    qualitative_texts = {}
    for path, phrases in QUALITATIVE_SKILLS.items():
        text = require_phrases(path, phrases)
        check_no_generic_stub(path, text)
        qualitative_texts[path] = text
    check_qualitative_distinctiveness(qualitative_texts)
    for path, phrases in GEDANKEN_SKILLS.items():
        require_phrases(path, phrases)
    for path, phrases in UI_PROMPTS.items():
        require_phrases(path, phrases)
    print(
        "validated functional subworkflow skills: "
        f"{len(QUALITATIVE_SKILLS)} qualitative, {len(GEDANKEN_SKILLS)} Gedanken"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
