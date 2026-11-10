---
name: abducer-failure-signal-cartographer
description: Separate Abducer conceptual pressure packets into failure certificates, discovery signals, opportunities, and open questions with witnesses, falsifiers, and successor hooks. Use when blocked routes must be distinguished from positive structural pressure before hypothesis generation.
---

# Abducer Failure Signal Cartographer

## Role

Build the classification layer between pressure formalization and creative
hypothesis generation.

## Workflow

1. Read pressure packets and their source artifacts.
2. Emit failure certificates for blocked or missing obligations.
3. Emit discovery signals for repeated structures, bridge opportunities, or route patterns.
4. Preserve opportunity and open-question items when neither failure nor signal is justified.
5. Attach falsifiers and demotion conditions to every classification.

## Guardrails

- Do not route every blocker to invention; some blockers should become revision, evidence, or stop items.
- Do not promote a discovery signal without pattern evidence.
- Preserve unknowns rather than smoothing them into confident prose.

## Output Contract

Emit `abducer_failure_certificate` and `abducer_discovery_signal` objects. Validate with `agentic/scripts/validate_hypothesis_exploration.py`.

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
