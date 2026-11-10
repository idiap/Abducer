---
name: results-paper-readiness-gatekeeper
description: Gate a scoped result candidate before paper handoff. Use when theorem scope, finite-object definitions, proof packet, prior-art boundary, disqualifier matrix, and narrative insertion must be checked before calling a subgoal publishable or manuscript-ready.
---

# Results Paper Readiness Gatekeeper

## Conceptual Role

This skill is the final promotion gate for a result-elaboration subgoal. It does not discover new mathematics. It decides whether the available artifacts justify a paper handoff, a scoped note, a limitation paragraph, or further proof work.

## Workflow

1. Collect the theorem scope, finite-object definitions, proof packet, prior-art audit, disqualifier matrix, and narrative integration plan.
2. Check hard gates:
   - claim statement ready;
   - definitions and assumptions ready;
   - proof or conditional proof status ready;
   - prior-art boundary ready;
   - disqualifiers closed or explicitly blocking;
   - overclaim boundary ready;
   - manuscript insertion point ready.
3. Assign one decision:
   - `paper_handoff_ready`
   - `scoped_note_ready`
   - `needs_finite_repair`
   - `demote_to_limitation`
   - `not_claimable`
4. State the next action and the exact artifact that should change.

## Output Contract

Return: readiness decision, gate table, missing blockers, permitted paper claim, forbidden language, insertion plan, validator/handoff command, and next action.

## Epistemic Discipline

Assign an epistemic status before promotion: paper handoff ready, scoped note ready, finite repair needed, demoted to limitation, or not claimable. Cite evidence through theorem packets, proof reports, prior-art audits, disqualifier matrices, KB IDs, cycle IDs, draft sections, validation reports, or explicit unknowns. State which mathematical object and invariant the paper is allowed to claim.

## Guardrails

- Do not mark a result paper-ready while live inference/proof-quality packets are absent.
- Do not let narrative coherence compensate for missing proof or prior-art evidence.
- Do not permit broad claims when only a scoped method class is proved.
- Do not leave "needs more work" unbounded; name the finite repair or demote.

## Validation Handoff

If ready, hand off to `results-narrative-integrator` or the paper-writing workflow. If blocked, return to the specific upstream skill responsible for the missing gate.

## Failure/Demotion

Demote to limitation or not-claimable when proof status, prior-art boundary, or disqualifier closure is unresolved and no finite repair remains.
