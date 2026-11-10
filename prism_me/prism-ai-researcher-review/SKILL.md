---
name: prism-ai-researcher-review
description: Review the active Prism request through an AI-research lens. Use when evaluation design, baselines, ablations, benchmark claims, literature positioning, generalization claims, or data and protocol assumptions need to be scrutinized and turned into concrete TODOs.
---

# Prism AI Researcher Review

Read:

- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/04b-test-strategy.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Extract the experimental and benchmarking claims implied by the current work.
2. Check baseline quality, ablation adequacy, dataset and protocol assumptions, and generalization claims.
3. Check whether the work is positioned against the relevant research surface without inflated novelty claims.
4. Surface evaluation blind spots that could mislead future users or readers.
5. Turn the most important issues into concrete TODOs for the persona-review artifact.

## Guardrails

- Critique the research logic, not just the amount of testing.
- Separate missing evidence from missing literature.
- Use explicit nulls when no material research-design issue exists.

## Output Contract

Produce:

- research framing and benchmark claims reviewed
- evaluation, baseline, ablation, or generalization risks
- data, protocol, or literature-positioning gaps
- concrete TODOs
