---
name: prism-repo-cartographer
description: Map the current repository against a Prism-style spec and contract. Use when an external project needs an evidence-backed picture of relevant modules, tests, docs, reusable assets, risky zones, and a narrow proposed touch set before slice planning starts.
---

# Prism Repo Cartographer

This skill turns an existing repository into a usable implementation map.

Read:

- [../agents.md](../agents.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/documentation-discipline.md](../shared/references/documentation-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/workspace-convention.md](../shared/references/workspace-convention.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/templates/03-repo-map.md](../shared/templates/03-repo-map.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)

## Workflow

1. Read the current spec and contract first.
2. Inspect the relevant code, tests, docs, scripts, and configuration.
3. Record the current surfaces that already solve part of the request.
4. Identify reusable assets and the narrowest plausible touch set.
5. Identify annotation gaps in relevant `.py` and `.md` files, especially where core concept or intent is hard to recover quickly.
6. Identify where the repo already contains content-quality tests, prompt probes, examples, or evaluation surfaces that can feed reflective refinement.
7. Identify where the repo already contains deterministic tests, harnesses, fixtures, or CI surfaces that can support systematic test generation.
8. Identify documentation gaps where the current docs are structural but not explanatory, conceptual, example-rich, or concrete enough for onboarding.
9. Identify candidate dependency surfaces: environment groups, runtimes, KBs, backends, mounts, and source paths that the dependency map should formalize.
10. Mark contracts, APIs, schemas, or runtime assumptions that must stay stable.
11. Record risks, gaps, and blockers with file-backed evidence.
12. Write or update `.prism/<request-slug>/03-repo-map.md`.
13. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Cite real file paths, not vague module descriptions.
- Prefer narrow touch sets over broad refactor suggestions.
- Separate blockers from guesses about what might exist.
- Keep untouched areas explicit so implementation does not sprawl.
- Treat thin explanation in Python and Markdown as a real mapping concern, not a cosmetic note.

## Output Contract

Produce a repo map with:

- current relevant surfaces
- reusable assets
- candidate dependency surfaces
- annotation opportunities
- proposed touch set
- boundary and compatibility notes
- risks, gaps, blockers, and evidence
