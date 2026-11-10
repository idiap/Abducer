---
name: prism-generative-validation-runner
description: Run systematic deterministic and generative validation in a Codex-style environment. Use when implementation should be tested against expected outcomes, content-quality criteria, adversarial probes, and failure-to-regression loops, with evidence written down in a reusable test record.
---

# Prism Generative Validation Runner

This skill turns the testing strategy into actual evidence.

Read:

- [../agents.md](../agents.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- [../shared/templates/05c-test-evidence.md](../shared/templates/05c-test-evidence.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/04b-test-strategy.md`
- `.prism/<request-slug>/05-execution-log.md`
- `.prism/<request-slug>/05d-persona-review.md`

## Workflow

1. Run or inspect the deterministic tests named in the test strategy.
2. Run the planned generative probe families and record expected versus observed outcomes.
3. Use Codex-style judgment anchored in the spec and quality criteria to evaluate content quality, not just structure.
4. Localize failure clusters rather than reporting undifferentiated disappointment.
5. Convert important failures into new deterministic regressions or repeatable generative probes.
6. When persona-review findings name hypothesis, mathematical, research-design, or engineering risks, probe those risks directly instead of leaving them as prose-only concerns.
7. Record coverage confidence and remaining weak zones.
8. Write or update `.prism/<request-slug>/05c-test-evidence.md`.
9. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Generative validation must still be evidence-backed and oracle-backed.
- Record the prompts or probe families in a reusable way.
- Do not stop at "tests passed" if generative outputs are still weak.
- Important failures should change the future test surface, not vanish into prose.

## Output Contract

Produce a test-evidence artifact with:

- deterministic test evidence
- generative validation evidence
- failure-to-test conversions
- coverage assessment
- recommended follow-up
