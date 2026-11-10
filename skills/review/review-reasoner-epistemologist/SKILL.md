---
name: review-reasoner-epistemologist
description: Review the reasoner as an epistemologist specialized in mathematical discovery. Use when the user wants a code-first assessment of whether the system earns its claims, licenses assertions correctly, distinguishes evidence from organization, and applies enough falsification pressure in discovery and proof.
---

# Review Reasoner Epistemologist

## Conceptual Role

Review the reasoner as a system of mathematical knowledge production.
Inspect whether it is actually learning, or just building structured stories.

## Required Evidence

Review code first:

1. `skills/common`
2. discovery, prove, work, meta, and prior-art scripts
3. scoring, queueing, logging, and persistence code
4. tests that claim to validate those mechanisms
5. live `artifacts/<kb-ref>` and `InformalMathLib/<kb-ref>` state when available

Use docs only to compare claim versus implementation.

## Workflow

1. Inspect how theorem grounding and assertion licensing are implemented.
2. Inspect where evidence is gathered, scored, imported, or merely inferred.
3. Inspect whether blocked results, negative findings, and counterexample pressure materially change the search.
4. Inspect stop rules, continuation rules, and reward-sensitive control.
5. Judge whether the system mistakes coherence, novelty, or rich artifacts for evidence.

Read [references/prompt-template.md](references/prompt-template.md).

## Output Contract

State:

1. what the reasoner genuinely knows how to justify;
2. where it overclaims;
3. where epistemic discipline is strongest;
4. where the system still lacks decisive tests.

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
