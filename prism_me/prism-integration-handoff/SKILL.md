---
name: prism-integration-handoff
description: Package a finished request for future Prism onboarding. Use when the external project needs a final handoff that maps delivered work, artifact paths, candidate agent identity, lifecycle placement, semantic folder, runtime boundaries, and next import steps into Prism.
---

# Prism Integration Handoff

This skill closes the loop and prepares future import work.

Read:

- [../agents.md](../agents.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/documentation-discipline.md](../shared/references/documentation-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/todo-discipline.md](../shared/references/todo-discipline.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/03-repo-map.md`
- `.prism/<request-slug>/03b-dependency-map.md`
- `.prism/<request-slug>/04-slice-plan.md`
- `.prism/<request-slug>/04b-test-strategy.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05b-refinement-loop.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/06-verification.md`
- [../shared/templates/07-handoff.md](../shared/templates/07-handoff.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)

## Workflow

1. Summarize the delivered outcome and the real user or system effect.
2. Build a complete artifact map for the request workspace.
3. Summarize the dependency map so future onboarding work can see bundle alignment, runtime requirements, KBs, backends, mounts, and hidden setup risk.
4. Record which touched Python and Markdown files were made more explanatory and which still need annotation work.
5. Summarize the quality criteria and the reflective refinement history so future onboarding work can see how content quality was shaped.
6. Summarize the testing strategy and test evidence so future onboarding work can see how deterministic and generative validation were handled.
7. Record the documentation surfaces that were added or improved and whether they now explain concepts, examples, and output interpretation clearly.
8. Reconcile `to-do.md` with shipped, deferred, and blocked work so the root control surface matches the handoff.
9. Translate the result into Prism onboarding terms: candidate agent id, lifecycle stage, organization group, entrypoints, semantic folder, runtime boundary.
10. Separate remaining debt from shipped behavior.
11. List the next import or adoption steps in dependency order.
12. Write or update `.prism/<request-slug>/07-handoff.md`.
13. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not blur finished work with future ambitions.
- Keep path mappings explicit if the external repo uses different conventions.
- Preserve runtime boundaries and provenance; do not pretend the capability is already native Prism infrastructure.
- Keep dependency translation explicit enough that a later Prism import can recreate the runtime picture without chat history.
- Make the handoff usable by another agent without needing the full chat history.
- Make annotation coverage explicit so a later onboarding pass knows which files already carry concept-and-intent explanations.
- Make sure `to-do.md` no longer implies unfinished work that was actually completed, or hides work that was deferred.

## Output Contract

Produce a handoff bundle with:

- delivered outcome
- artifact map
- dependency trace
- annotation coverage
- Prism onboarding translation
- remaining debt
- next import steps
