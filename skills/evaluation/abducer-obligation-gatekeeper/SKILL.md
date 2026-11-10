---
name: abducer-obligation-gatekeeper
description: Convert creative Abducer hypothesis candidates into hard validation obligations and route-safety gates. Use when bridge, abstraction, regime, weakening, strengthening, carrier, analogy, inversion, factorization, or representation-shift candidates need preservation, activation, non-collapse, barrier, source, and proof-readiness checks.
---

# Abducer Obligation Gatekeeper

## Role

Prevent conceptual creativity from bypassing proof discipline. Every candidate
must become a validation packet before ranking or queue promotion.

## Hard Gates

- `preservation`: the candidate preserves commitments it claims to mediate.
- `target_activation`: the candidate can still affect the target.
- `non_collapse`: the candidate does not trivialize or conflate distinct objects.
- `barrier_compatibility`: known barriers or mismatch risks are stated.
- `source_grounding`: source artifacts and KB IDs support the move.
- `proof_queue_readiness`: theorem-shaped obligations are explicit when proof queue is requested.

## Workflow

1. Read candidate and creativity-analysis objects.
2. Emit one validation packet per candidate.
3. Add obligations for every hard gate.
4. Force quarantine or rejection when hard-gate failure remains.
5. Distinguish proof-queue candidates from discovery branches and revision items.

## Guardrails

- Do not restate the candidate as its own validation.
- Do not allow proof queue disposition with missing preservation, non-collapse, source, or proof-readiness obligations.
- Demote attractive but ungrounded mediators.

## Output Contract

Emit objects conforming to `agentic/spec/abducer_validation_packet.schema.json`.

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

## Subgoal Control Decision

Every validation packet should either attach or preserve a `Subgoal Control Decision`. Include the decision, target-object link, preserved commitments, blocker, learning from failure, next action, and demotion triggers. A hard-gate failure must lead to `quarantine`, `reject`, or `stop`; a warning may justify `persist_adapt` only if the missing obligation is named as informative proof debt.

## Best Machinery Assessment

Every validation packet should attach or preserve a `Best Machinery Assessment`: `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. Reject or quarantine method-name-only claims, proxy-solving claims, endpoint notation used as construction machinery, and witness machinery that lacks constructed target object or transfer bridge.
