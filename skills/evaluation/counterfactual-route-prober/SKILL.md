---
name: counterfactual-route-prober
description: Stress-test an inference by minimally perturbing assumptions, carrier choices, or nearby theorem variants and checking whether the conclusion survives. Use when a route looks clean but may be brittle or spuriously phrased.
---

# Counterfactual Route Prober

## Role

This skill tests whether an inference is robust or only accidentally true under one wording or carrier choice.

## When To Use

Use it when:

1. a route seems too smooth and may be hiding brittle dependencies;
2. you need to know which minimal perturbations break the current conclusion;
3. the system may be overfitting to one formulation rather than a real invariant route.

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
