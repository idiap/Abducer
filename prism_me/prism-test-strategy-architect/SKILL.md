---
name: prism-test-strategy-architect
description: Build a systematic test strategy for a skill, agent, or feature under construction. Use when the work needs an explicit deterministic and generative test matrix, Codex-based validation protocol, content-quality oracles, and a failure-to-regression plan before implementation is considered mature.
---

# Prism Test Strategy Architect

This skill defines the testing shape of the work.

Read:

- [../agents.md](../agents.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/templates/04b-test-strategy.md](../shared/templates/04b-test-strategy.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/03-repo-map.md`
- `.prism/<request-slug>/03b-dependency-map.md`
- `.prism/<request-slug>/04-slice-plan.md`

## Workflow

1. Identify the capability, slices, and acceptance evidence that need testing.
2. Define the deterministic test matrix: unit, integration, regression, invariant, contract checks, and dependency-sensitive checks where setup matters.
3. Define the generative test matrix: probe families, adversarial cases, ambiguity cases, and content-quality probes.
4. Define the oracle for judging generative outputs using the spec, quality criteria, and explicit expected outcomes.
5. Define how dependency assumptions will be validated or smoke-tested when the work depends on bundles, KBs, backends, or mounts.
6. Define a Codex validation protocol for generating probes, judging results, localizing failures, and converting failures into repeatable tests.
7. State coverage goals and exit criteria.
8. Write or update `.prism/<request-slug>/04b-test-strategy.md`.
9. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Deterministic tests are necessary but not sufficient for generative capabilities.
- Generative probes must still be anchored in a real oracle.
- Hidden dependency assumptions weaken test confidence; make them explicit or test them directly.
- Do not leave failure conversion implicit; say how important failures will become regressions.
- Prefer a systematic matrix over a grab bag of test ideas.

## Output Contract

Produce a test-strategy artifact with:

- testing scope
- deterministic test matrix
- generative test matrix
- dependency assumptions under test
- Codex validation protocol
- coverage gaps
- exit criteria
