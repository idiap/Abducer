---
name: prism-reflective-refinement-loop
description: Run reflective refinement loops against explicit quality criteria while a skill or agent is being built. Use when a current draft should be tested against deterministic and generative criteria, weak points localized, targeted revisions applied, and the result re-tested for at least two cycles.
---

# Prism Reflective Refinement Loop

This skill forces iterative quality improvement instead of one-shot optimism.

Read:

- [../agents.md](../agents.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/templates/05b-refinement-loop.md](../shared/templates/05b-refinement-loop.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/04-slice-plan.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Choose the current draft, skill, prompt surface, or artifact to evaluate.
2. Select the highest-priority criteria dimensions and probes.
3. Run evaluation cycle 1 against the current draft.
4. Localize concrete weaknesses instead of giving diffuse criticism.
5. Apply targeted refinements to the draft or to the skill instructions.
6. Re-test and record whether the changes improved the weak points.
7. Run cycle 2 with fresh attention on the remaining gaps.
8. If major weaknesses remain, run additional cycles until the result is clearly improved or explicitly blocked.
9. If the source started outside Prism, explicitly test whether the shaped agent still preserves the useful behavior and boundaries of the upstream source.
10. Use deterministic and generative test evidence to localize the highest-value refinements, not just subjective impressions.
11. When a persona review is due or fresh persona findings exist, use them as explicit cycle inputs instead of folding them into vague "remaining gaps."
12. Write or update `.prism/<request-slug>/05b-refinement-loop.md`.
13. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- At least two cycles are the default expectation once a meaningful draft exists.
- Use the criteria packet actively; do not cite it ceremonially.
- Each cycle must localize weaknesses to specific content issues, not vague dissatisfaction.
- Revisions should be targeted and testable, not just more verbose.
- Stop only with a clear verdict: improved, blocked, or still weak.

## Output Contract

Produce a refinement-loop artifact with:

- criteria in use
- at least two documented cycles
- localized improvement themes
- current verdict
- next step
