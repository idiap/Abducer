---
name: review-reasoner-fields-medalist
description: Review the reasoner as a Fields Medalist mathematician. Use when the user wants a code-first assessment of whether the mathematical objects, proof burdens, abstractions, route lemmas, and generated claims are mathematically substantive rather than merely schematic.
---

# Review Reasoner Fields Medalist

## Conceptual Role

Review the reasoner as an expert mathematician would:
is there real mathematics here, or only scaffolding around open problems?

## Required Evidence

Inspect:

1. theorem-grounding code
2. bridge planning and abstraction generation
3. proof sketching and prove-cycle dossiers
4. InformalMathLib entries and imported external theorems
5. live proof attempts, macro-proof state, and expert-facing papers

Read [references/prompt-template.md](references/prompt-template.md).

## Output Contract

Focus on:

1. mathematical sharpness of objects and lemmas;
2. whether subresults would interest experts independently;
3. where the route collapses into placeholders;
4. what mathematical strengthening is needed next.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Review should create actionable obligations, not aesthetic commentary or generic caution.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: reviewed claim, definition, invariant, route, evidence packet, and falsifier.
- Preserved invariants: object identity, assumptions, preserved/broken invariants, evidence status, and review scope.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: severity-ranked findings, mathematical objects, epistemic statuses, evidence paths, falsification tests, demotion reasons, and concrete TODOs. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
