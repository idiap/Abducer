---
name: review-reasoner-discovery-scientist
description: Review the reasoner as a DeepMind-style scientist of mathematical discovery systems. Use when the user wants a code-first assessment of the search decomposition, routing, memory, evaluation, branch execution, reward signals, and overall research-system design behind the reasoner.
---

# Review Reasoner Discovery Scientist

## Conceptual Role

Review the reasoner as an implemented research system for mathematical discovery.

## Required Evidence

Inspect:

1. work-loop and orchestrator control
2. discovery cycle, branch queue, branch execution, and promotion logic
3. prove-cycle control and critique
4. prior-art pass and knowledge-source policies
5. evaluation surfaces in tests and persisted artifacts

Read [references/prompt-template.md](references/prompt-template.md).

## Output Contract

Focus on:

1. search quality;
2. branch diversity and replay;
3. memory reuse;
4. evaluation discipline;
5. what the architecture learns versus what it only stores.

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
