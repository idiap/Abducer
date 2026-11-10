---
name: prism-spec-intake
description: Turn a request into a Prism-aligned spec packet for an external repository. Use when the problem, scope, acceptance evidence, constraints, assumptions, risks, or interface sketch need to be made explicit before planning or implementation starts.
---

# Prism Spec Intake

This skill creates or updates the request's spec packet.

Read:

- [../agents.md](../agents.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/workspace-convention.md](../shared/references/workspace-convention.md)
- [../shared/templates/01-spec.md](../shared/templates/01-spec.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)

## Workflow

1. Restate the desired outcome in plain language.
2. Describe the problem without sneaking in implementation decisions.
3. Separate `In Scope`, `Out Of Scope`, `Assumptions`, and `Unknowns`.
4. Name the acceptance evidence before talking about code changes.
5. Capture the interface sketch: inputs, outputs, state transitions, and external dependencies.
6. State any expectation that touched Python and Markdown files should be made more explanatory through concept-and-intent annotations.
7. State whether the request will need explicit generative and content-side quality criteria.
8. Record immediate risks, known debt, and open questions.
9. Write or update `.prism/<request-slug>/01-spec.md`.
10. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not hide unknowns inside confident prose.
- Do not let "acceptance evidence" collapse into "it seems good."
- Do not convert out-of-scope items into implied later promises.
- Keep the spec usable by a later planner or critic without guessing.

## Output Contract

Produce a spec packet that clearly contains:

- outcome
- problem statement
- scope boundaries
- constraints
- assumptions and unknowns
- acceptance evidence
- interface sketch
- risks, debt, and open questions
