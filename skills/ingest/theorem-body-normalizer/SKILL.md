---
name: theorem-body-normalizer
description: Normalize theorem-like statements into typed hypotheses, conclusion, quantifier regime, model assumptions, and assertion license. Use when discovery or proof work is drifting on topical labels rather than statement bodies.
---

# Theorem-Body Normalizer

## Role

This skill is the mandatory Phase 0 epistemic gate.
It turns raw statements into theorem-body form before bridge planning, pathway ranking, or proof claims.

## When To Use

Use it when:

1. source or target claims are being referred to by topic labels;
2. model or quantifier ambiguity is blocking route design;
3. a route needs assertion licensing before further reasoning.

## Workflow

1. Extract the raw statement text.
2. Separate hypotheses, conclusion, quantifier regime, model assumptions, and thresholds.
3. State the claim type and assertion license.
4. Record overturn conditions and decisive progress conditions.

Read [references/prompt-template.md](references/prompt-template.md) for the prompt contract.

## Output Contract

Return:

1. normalized theorem body
2. typed hypotheses
3. typed conclusion
4. quantifier and model regime
5. claim type and assertion license
6. overturn conditions

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Ingestion does not validate truth; it only preserves inspectable source structure for later reasoning.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: source statement, theorem body, symbol, definition, citation, normalized KB card, and dependency edge.
- Preserved invariants: source text provenance, symbol identity, statement dependency, confidence status, and explicit missing fields.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: normalized statements, source IDs, explicit unknowns, parse failures, artifact paths, validation result, and next repair. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
