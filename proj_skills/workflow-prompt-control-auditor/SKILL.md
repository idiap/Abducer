---
name: workflow-prompt-control-auditor
description: Audit prompt-control quality for workflow prompts and agent instructions. Use when Codex should periodically check Abducer prompt files and coordination docs for weak output contracts, missing source-boundary discipline, missing schema/JSON constraints, excessive length, vague instructions, or uncontrolled reflective loops.
---

# Workflow Prompt Control Auditor

Use this after prompt files and coordination docs are inventoried.

## Inputs

- `skills/**/SKILL.md` and `skills/**/agents/openai.yaml`
- `proj_skills/**/SKILL.md`, `proj_skills/**/agents/openai.yaml`, and `prism_me/*/SKILL.md`
- `.codex/hooks.json`, Prism templates, and active request contracts where relevant
- [AGENTS.md](../../AGENTS.md)
- relevant skill orchestrator docs

## Procedure

1. Check for explicit output-shape control such as JSON, schema, or artifact contracts.
2. Check for source-boundary language around blind runs, reference material, and post-hoc stages.
3. Check for bounded reflection language such as stopping criteria, iteration limit, closure gate, or guard.
4. Flag very large prompts for review because long prompts are harder to keep controlled.
5. Flag vague prompt surfaces that lack evidence, source, artifact, or validation constraints.

## Handoff

Leave `prompt_control_findings` with path, severity, prompt-control dimension, and suggested repair.
