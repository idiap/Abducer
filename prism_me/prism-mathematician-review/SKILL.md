---
name: prism-mathematician-review
description: Review the active Prism request through a mathematical lens. Use when definitions, invariants, edge cases, complexity claims, numerical reasoning, or formal consistency need to be checked and converted into concrete TODOs.
---

# Prism Mathematician Review

Read:

- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Extract the formal, quantitative, or algorithmic claims in play.
2. Check for undefined objects, inconsistent assumptions, and missing invariants.
3. Inspect edge cases, bounds, and complexity or scaling claims where relevant.
4. Localize places where the code or docs imply stronger mathematical guarantees than the evidence supports.
5. Turn the highest-value issues into concrete TODOs for the persona-review artifact.

## Guardrails

- Do not fabricate formalism where the request is not mathematical.
- Use explicit nulls when no material mathematical issue exists.
- Prefer precise local findings over grand abstraction.

## Output Contract

Produce:

- formal or quantitative claims reviewed
- consistency or edge-case gaps
- missing invariants, bounds, or complexity checks
- concrete TODOs
