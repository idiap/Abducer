---
name: prism-implementation-driver
description: Execute one approved slice under Prism-style controls. Use when a spec, contract, repo map, and slice plan already exist and the next step is to make a minimal, traceable change while recording touched files, checks, deviations, and outstanding debt.
---

# Prism Implementation Driver

This skill runs one slice at a time.

Read:

- [../agents.md](../agents.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/documentation-discipline.md](../shared/references/documentation-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/todo-discipline.md](../shared/references/todo-discipline.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/03-repo-map.md`
- `.prism/<request-slug>/03b-dependency-map.md`
- `.prism/<request-slug>/04-slice-plan.md`
- `.prism/<request-slug>/04b-test-strategy.md`
- `.prism/<request-slug>/05d-persona-review.md`
- [../shared/templates/05-execution-log.md](../shared/templates/05-execution-log.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)

## Workflow

1. Pick the active slice and restate its exit criteria.
2. Confirm the expected touch set, dependency state, and current `python3 prism_me/scripts/prism_control.py status` output before editing.
3. Update `to-do.md` so the active slice or task is visibly in progress.
4. Implement the smallest coherent change that satisfies the slice.
5. Whenever you touch `.py` or `.md`, add or improve explanatory annotations so the file communicates its core concept, intent, and role in the system.
6. When building a skill or agent, keep the quality criteria visible during implementation rather than leaving them for the end.
7. Generate or update the deterministic tests and generative probe harnesses promised in the test strategy when the slice touches their coverage area.
8. If implementation introduces, removes, or clarifies a dependency, update `.prism/<request-slug>/03b-dependency-map.md` before closing the slice.
9. When the change affects workflows, concepts, outputs, or onboarding, update the documentation so it explains the concept, gives concrete examples, and tells the reader how to interpret the results.
10. Run the planned checks, or record exactly why a check was not run.
11. If the control stack marks persona review due after 50 committed edit or write cycles, pause the slice, route through `prism-persona-review-orchestrator`, and treat the resulting TODOs as first-class follow-up work. On-demand and final release-gate reviews remain available independently of the counter.
12. Capture deviations from plan, dependency updates, new debt, annotation coverage, and the next recommended step.
13. Update `to-do.md` so completed, blocked, deferred, and persona-review states match the real execution result.
14. Write or update `.prism/<request-slug>/05-execution-log.md`.
15. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not drift outside the approved touch set without updating the repo map or slice plan.
- Do not introduce hidden dependencies; if one appears, name it and update the dependency map.
- Do not declare success without evidence from tests, checks, or inspected artifacts.
- Keep deferred work explicit instead of sneaking it into scope.
- If implementation reveals a contract gap, push the gap back into the earlier artifact chain.
- For touched Python files, prefer module docstrings, class or function docstrings, and meaningful block comments that explain intent.
- For touched Markdown files, add framing and interpretation text so the document works as onboarding material instead of a bare checklist.
- Treat the first coherent draft as input to the reflective refinement loop, not as the final answer.
- Treat test generation as part of implementation, especially when failures should be converted into future regressions.
- Documentation should explain concepts and use real examples; do not leave it at file structure, sections, and links.
- Keep `to-do.md` honest: mark done, blocked, or deferred states only when the evidence matches.
- Treat persona-review TODOs as real scope inputs once the control stack triggers them; do not bury them in chat.

## Output Contract

Produce an execution log with:

- active slice
- planned change
- actual changes made
- files touched
- dependency updates
- annotation updates
- documentation updates
- test generation updates
- tests and checks
- deviations, debt, and next step
