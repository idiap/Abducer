---
name: epistemic-status-ledger
description: Build a ledger over active claims, labeling them as grounded, conditional, conjectural, refuted, prior-art, or blocked. Use when the workflow is conflating coherence or novelty with evidence.
---

# Epistemic Status Ledger

## Role

This skill turns a live route portfolio into an explicit claim ledger.
It makes the epistemic status of each active claim inspectable.

## When To Use

Use it when:

1. multiple artifacts make claims at different evidential levels;
2. experts need to know what is grounded versus merely live;
3. a process review needs a truth-tracking summary.

## Workflow

1. Collect active claims from the current artifacts.
2. Label each claim with one status class.
3. Record evidence used, assertion license, overturn conditions, and next test.

Read [references/prompt-template.md](references/prompt-template.md).

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- A score or label is never enough; evaluation must expose what would falsify, demote, or repair the route.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: definitions, bridge objects, candidate hypotheses, entailment gaps, premises, regimes, counterexamples, and proof obligations.
- Preserved invariants: objects compared, assumptions used, preserved invariants, broken invariants, boundary regimes, and witness evidence.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
