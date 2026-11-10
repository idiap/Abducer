---
name: prism-quality-criteria-elicitor
description: Elicit explicit quality criteria for an agent or skill under construction. Use when the work needs a concrete quality bar that covers deterministic interface behavior and, especially, generative and content quality such as conceptual clarity, intent fidelity, epistemic discipline, specificity, explanatory richness, and failure-mode awareness.
---

# Prism Quality Criteria Elicitor

This skill turns a vague sense of quality into a usable evaluation packet.

Read:

- [../agents.md](../agents.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/templates/02b-quality-criteria.md](../shared/templates/02b-quality-criteria.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`

## Workflow

1. Identify the capability under construction and its real job.
2. Define deterministic and interface-side quality expectations.
3. Define generative and content-side quality expectations with more detail than the deterministic side.
4. For each quality dimension, write success signals and failure signals.
5. Add realistic probes or test prompts that would expose weak performance.
6. Define pass, conditional, and hold thresholds.
7. Record likely failure modes and likely improvement targets.
8. If the request started from external code or skills, include probes that test whether the proposed Prism shape preserves useful upstream behavior rather than only matching interface expectations.
9. Make the criteria evaluable by a later deterministic and generative test strategy rather than leaving them purely descriptive.
10. Write or update `.prism/<request-slug>/02b-quality-criteria.md`.
11. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not stop at interface cleanliness; the main emphasis is content quality.
- Make criteria concrete enough that another agent can apply them without guessing.
- Good criteria should distinguish shallow, generic output from genuinely useful output.
- Include probes that test edge cases, ambiguity, and interpretive quality, not only schema correctness.

## Output Contract

Produce a quality-criteria packet with:

- capability under construction
- deterministic and interface quality dimensions
- generative and content quality dimensions
- success and failure signals
- test probes
- scoring or verdict method
- common improvement targets
