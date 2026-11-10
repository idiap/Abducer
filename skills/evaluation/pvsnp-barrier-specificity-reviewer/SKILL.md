---
name: pvsnp-barrier-specificity-reviewer
description: Review P vs NP barrier diagnoses for branch-specific correctness. Use when a branch invokes relativization, algebrization, natural proofs, black-boxness, diagonalization limits, proof-complexity barriers, or nonblackbox escape conditions and needs to avoid generic barrier slogans.
---

# P vs NP Barrier Specificity Reviewer

## Conceptual Role

Use this reviewer when a branch says a route hits or escapes a known barrier. The job is not to recite barriers, but to identify the exact feature of the branch that triggers or avoids the barrier.

## Workflow

1. State the route mechanism and claimed barrier.
2. Identify the trigger property: relativizing proof step, algebraic oracle access, large constructive useful property, black-box use of target circuits, diagonalization, or proof-system-specific bottleneck.
3. Check whether the branch has an escape condition: nonblackbox use, non-large property, nonconstructive property, semantic ingredient, advice-free carrier, or nonrelativizing step.
4. Decide whether the barrier blocks the route, only warns, suggests no-go theorem formation, or is inapplicable.
5. State what would make the barrier diagnosis rigorous.

## Mathematical Invariants

Mathematical object: route family, method class, barrier hypothesis, escape condition, target class, and conclusion.

Preserved invariants: barrier applies only to the method class it actually covers; escape conditions remain explicit; branch value is separated from target proof.

Broken invariants: using natural proofs against a non-large property, using relativization as a blanket objection, ignoring algebraic access, treating a black-box no-go as covering nonblackbox methods, or claiming a barrier proves `P != NP` impossible.

Edge case or counterexample: a property may be useful and constructive but not large; calling it natural without the largeness condition is an invalid barrier diagnosis.

## Epistemic Discipline

Assign epistemic status: `barrier_applicable`, `barrier_warning`, `escape_condition_present`, `barrier_inapplicable`, `no_go_candidate`, `overbroad_barrier`, or `explicit_unknown`.

Cite evidence from route description, theorem references, cycle IDs, prior-art packets, source artifacts, or explicit unknowns.

## Output Contract

Return:

1. `Route And Barrier`: method family and candidate barrier.
2. `Trigger Check`: exact property that activates the barrier.
3. `Escape Conditions`: properties that keep the route alive.
4. `Scope`: what the barrier rules out and what it does not.
5. `Verdict`: applicable, warning, inapplicable, no-go candidate, or overbroad.
6. `Validation Handoff`: negative tactic selector, impossibility theorem forger, derivation builder, or branch repair.

## Failure/Demotion

Demote if the review only says "relativization", "natural proofs", or "algebrization" without branch-specific hypotheses. Quarantine barrier claims that suppress valid escape conditions or overstate method-family no-go results.
