---
name: workflow-leakage-auditor
description: Audit Abducer workflow boundaries for inappropriate evidence or hidden-context flow. Use when checking whether evaluation answers, private reasoning traces, prior-art conclusions, or post-hoc review material can reach generation and discovery inputs.
---

# Workflow Leakage Auditor

Use this focused hook within `$workflow-health-audit-orchestrator`. Its findings are review leads, not automatic defects.

## Inputs

- [AGENTS.md](../../AGENTS.md) and active `.prism/<request>/` contracts
- `agentic/evals/`, `agentic/operations/`, `agentic/traces/`, `external/`, and trace/evidence-loading code
- scientific `skills/` plus project-support `proj_skills/`
- ingest, prior-art, evaluation, and publication handoffs

## Procedure

1. Draw explicit boundaries between generation/discovery input, local evaluation, external evidence, private traces, and publication output.
2. Look for expected answers, evaluation fixtures, prior-art conclusions, or hidden reasoning being loaded before the stage that is allowed to see them.
3. Treat references inside tests, explicit post-hoc evaluation, and adversarial review as context requiring confirmation—not as leakage by themselves.
4. Verify that surfaced reasoning and publications expose licensed claims and evidence, not private chain-of-thought or unreviewed intermediate state.
5. Report the path, line, direction of possible flow, severity, evidence, and the smallest confirmation step.

## Handoff

Return `leakage_findings` with `source_surface`, `destination_surface`, `path`, `line`, `severity`, `evidence`, and `review_action`.
