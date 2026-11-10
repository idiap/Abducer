---
name: prism-persona-review-orchestrator
description: Coordinate a systematic multi-persona review over the active Prism request. Use when the control stack marks persona review due after 50 committed edit or write code-generation cycles, at a final release gate, when the user asks for a code review through multiple personas, or when execution needs an epistemologist, mathematician, AI researcher, and software engineer pass that ends in concrete TODOs.
---

# Prism Persona Review Orchestrator

Use this skill to coordinate the persona-review lane.

Read:

- [../agents.md](../agents.md)
- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/templates/05d-persona-review.md](../shared/templates/05d-persona-review.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/04b-test-strategy.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05b-refinement-loop.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Inspect `python3 prism_me/scripts/prism_control.py status` and confirm whether persona review is due.
2. Define the current review scope: touched files, active slice, recent checks, and unresolved risks.
3. Route through `prism-epistemologist-review`.
4. Route through `prism-mathematician-review`.
5. Route through `prism-ai-researcher-review`.
6. Route through `prism-software-engineer-review`.
7. Merge the findings into one artifact with explicit per-persona sections and explicit nulls where needed.
8. Consolidate the highest-value TODOs into a short actionable queue.
9. Sync the root `to-do.md` persona-review control fields and note whether implementation may continue before the TODOs land.
10. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.
11. Run `python3 prism_me/scripts/prism_control.py review-complete` once the artifact and `to-do.md` are up to date.

## Guardrails

- Do not skip a persona because another persona seems "close enough."
- Do not blur the findings into one undifferentiated review voice.
- Tie TODOs to evidence in the repo, artifacts, or tests.
- Keep TODOs concrete enough that they can be scheduled or deferred explicitly.
- If the review is blocked, say exactly what blocked it and still record partial findings.

## Output Contract

Produce or update `.prism/<request-slug>/05d-persona-review.md` with:

- trigger summary
- explicit coverage status for all four personas
- evidence-backed findings for each persona
- consolidated TODO queue
- gate decision
