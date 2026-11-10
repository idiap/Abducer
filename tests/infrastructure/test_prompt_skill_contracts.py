# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
PROMPT_PREFIX = (
    "First restate the intent gate, exact inputs and artifacts in scope, "
    "required output shape, and any missing context explicitly; do not assume "
    "hidden repository context. When the task involves substantive inference, "
    "explicitly separate prompt/context defects from genuine mathematical "
    "difficulty: classify context_status as well-posed / partially-ill-posed / "
    "ill-posed, inference_status as determined / underdetermined / "
    "difficult-but-well-posed, give the smallest repair, and report qualified "
    "certainty both now and assuming a well-posed context, and when applicable "
    "emit a short Prompt/Inference Diagnosis block before the main result."
)


def test_all_prompt_templates_declare_intent_gate_and_context_packet() -> None:
    prompt_templates = sorted(SKILLS.glob("*/*/references/prompt-template.md"))
    assert prompt_templates, "Expected prompt templates to exist."
    for path in prompt_templates:
        text = path.read_text(encoding="utf-8")
        assert "## Intent Gate" in text, f"{path} is missing the intent gate contract."
        assert (
            "## Self-Contained Context Packet" in text
        ), f"{path} is missing the self-contained context packet contract."
        assert (
            "## Prompt-Diagnosis And Qualified Certainty Gate" in text
        ), f"{path} is missing the prompt-diagnosis certainty gate."
        assert (
            "Prompt/Inference Diagnosis" in text
        ), f"{path} does not force the diagnosis block into the output shape."


def test_all_openai_agent_prompts_start_with_shared_context_prefix() -> None:
    agent_files = sorted(SKILLS.glob("*/*/agents/openai.yaml"))
    assert agent_files, "Expected OpenAI agent YAML files to exist."
    for path in agent_files:
        text = path.read_text(encoding="utf-8")
        assert PROMPT_PREFIX in text, f"{path} is missing the shared self-contained prompt prefix."
