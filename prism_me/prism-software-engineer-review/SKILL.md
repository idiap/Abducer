---
name: prism-software-engineer-review
description: Review the active Prism request through a software-engineering lens. Use when architecture, dependency integrity, maintainability, testing, developer workflow, or operational hardening need a focused review that ends in concrete TODOs.
---

# Prism Software Engineer Review

Read:

- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- `.prism/<request-slug>/03-repo-map.md`
- `.prism/<request-slug>/03b-dependency-map.md`
- `.prism/<request-slug>/04-slice-plan.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Inspect the touched architecture, dependencies, tests, and developer workflow surfaces.
2. Check for maintainability, readability, regression, or operational risks.
3. Check whether the implementation created hidden setup, hidden coupling, or thin documentation.
4. Localize the highest-value hardening and developer-experience work.
5. Turn the most important issues into concrete TODOs for the persona-review artifact.

## Guardrails

- Prefer concrete codebase risks over generic style commentary.
- Treat missing tests, weak docs, and hidden dependencies as real engineering concerns.
- Use explicit nulls when no material engineering issue exists.

## Output Contract

Produce:

- architecture and implementation surfaces reviewed
- maintainability, dependency, test, or operational risks
- missing hardening or developer-experience work
- concrete TODOs
