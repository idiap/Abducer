# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Check probe contracts against the documentation's current thematic paths."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
DOCS = ROOT / "docs"
PROBE_SKILLS = [
    "premise-completeness-prober",
    "entailment-gap-auditor",
    "regime-shift-auditor",
    "counterfactual-route-prober",
]


def test_inference_probe_skills_exist_with_prompt_contracts() -> None:
    for skill in PROBE_SKILLS:
        matches = sorted(SKILLS.glob(f"*/{skill}/SKILL.md"))
        assert matches, f"Missing skill definition for {skill}"
        skill_dir = matches[0].parent
        assert (
            skill_dir / "references" / "prompt-template.md"
        ).exists(), f"Missing prompt template for {skill}"
        assert (
            skill_dir / "agents" / "openai.yaml"
        ).exists(), f"Missing OpenAI agent metadata for {skill}"


def test_inference_probe_stack_is_documented() -> None:
    skills_doc = (DOCS / "reference/skills.md").read_text(encoding="utf-8")
    explainer_doc = (DOCS / "reference/code-and-skills-explainer.md").read_text(
        encoding="utf-8"
    )
    framework_doc = (DOCS / "research-methods/epistemic-prompt-framework.md").read_text(
        encoding="utf-8"
    )

    for skill in PROBE_SKILLS:
        assert skill in skills_doc, f"{skill} missing from docs/reference/skills.md"
        assert (
            skill in explainer_doc
        ), f"{skill} missing from docs/reference/code-and-skills-explainer.md"
        assert (
            skill in framework_doc
        ), f"{skill} missing from docs/research-methods/epistemic-prompt-framework.md"
    assert "## Inference-Quality Probe Stack" in framework_doc
