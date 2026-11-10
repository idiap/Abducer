---
name: prism-spec-verification-critic
description: Critique whether implementation actually satisfies the Prism-style spec and contract. Use when a request needs severity-ranked findings, supported and unsupported claims, missing evidence, residual risk, and an explicit release gate before handoff.
---

# Prism Spec Verification Critic

This skill is the release gate for the pack.

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
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05b-refinement-loop.md`
- `.prism/<request-slug>/05c-test-evidence.md`
- `.prism/<request-slug>/05d-persona-review.md`
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/templates/06-verification.md](../shared/templates/06-verification.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)

## Workflow

1. Compare the requested outcome against the actual changes and evidence.
2. Check for spec drift, contract drift, missing validation, hidden runtime assumptions, dependency drift, and weak explanation in touched `.py` or `.md` files.
3. Check whether the quality criteria were actually applied, especially on the generative and content side.
4. Check whether dependency claims are explicit, verified, and still consistent with implementation, tests, and runtime setup.
5. Check whether deterministic and generative testing were both planned and actually executed with meaningful evidence.
6. Check whether important generative failures were converted into repeatable tests or documented future regressions.
7. Check whether the reflective refinement loop completed at least two meaningful cycles or was credibly blocked.
8. Check whether due persona reviews actually happened, whether the four lenses were covered, and whether their TODOs were either resolved or explicitly deferred.
9. Check whether `to-do.md` reflects the real finished, deferred, blocked, and persona-review state of the request.
10. Rank findings by severity and back them with evidence.
11. Separate supported claims from unsupported claims.
12. Review whether Python and Markdown files now explain their core concept, intent, and local role clearly enough for a new agent.
13. Review whether the documentation is concept-driven, explanatory, example-rich, concrete, and useful without chat history.
14. Record missing evidence and residual risk even if the verdict is positive.
15. Set the release gate to `pass`, `conditional`, or `hold`.
16. Write or update `.prism/<request-slug>/06-verification.md`.
17. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Findings first.
- Do not reward polished explanations that lack evidence.
- Distinguish verified facts from inference and from absence of evidence.
- A clean result still needs residual-risk language if anything remains untested or unobserved.
- Treat hidden, under-verified, or contradictory dependency setup as a real release risk.
- Treat stale `to-do.md` state as a coordination weakness when it no longer matches delivered evidence.
- Treat missing explanatory annotation in touched Python and Markdown files as a real quality issue when it harms onboarding or future modification.
- Treat missing or superficial content-quality criteria as a real weakness in skill-construction work.
- Treat shallow testing, especially missing generative validation for generative capabilities, as a real release risk.
- Treat structural but non-explanatory documentation as a real weakness when the change needs conceptual onboarding.

## Output Contract

Produce a verification report with:

- severity-ranked findings
- supported claims
- annotation review
- dependency review
- quality criteria review
- testing review
- unsupported claims
- missing evidence
- residual risk
- required follow-up
- explicit release gate
