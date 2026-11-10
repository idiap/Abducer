---
name: pvsnp-reduction-consistency-reviewer
description: Review P vs NP reductions and transfer claims for direction, type, completeness, promise/domain conditions, length maps, padding/projection effects, parameter propagation, and target-class preservation. Use when a branch claims source-carrier hardness transfers to SAT, NP, P/poly, circuit lower bounds, proof lower bounds, or a restricted complexity model.
---

# P vs NP Reduction Consistency Reviewer

## Conceptual Role

Use this reviewer when the branch says one object gives hardness or upper bounds for another. It asks whether the claimed transfer actually goes in the needed direction and whether its parameters preserve the target.

## Workflow

1. Name the source object and target object.
2. Identify reduction type: many-one, Turing, oracle, projection, padding, restriction, black-box substitution, nonblackbox compilation, proof-system simulation, or carrier decoding.
3. Check direction: source to target, target to source, contrapositive, or no valid implication.
4. Track length and parameter maps such as `N=n^k`, query length `n^beta`, overhead `N^q`, advice length, and verifier overhead.
5. Verify completeness, promise, and domain restrictions.
6. Decide whether the result gives target progress, bounded-window evidence, repair obligation, or rejection.

## Mathematical Invariants

Mathematical object: source statement, target statement, reduction interface, transfer inequality, length map, and target class.

Preserved invariants: implication direction, domain, completeness, reduction type, length transformation, circuit/proof model, uniformity, advice, and quantifier strength.

Broken invariants: reversed reduction, target theorem replaced by a source lower bound, sparse valid lengths treated as all lengths, promise problem treated as total language, or padding used to hide exponent loss.

Edge case or counterexample: if a transfer only proves hardness below `c < (a-q)/beta` with `beta>0`, it cannot be promoted as all-polynomial SAT circuit lower bounds.

## Epistemic Discipline

Assign epistemic status: `transfer_valid`, `transfer_conditional`, `direction_unclear`, `bounded_window_only`, `promise_gap`, `parameter_loss`, `advice_leak`, `invalid_transfer`, or `proof-obligation`.

Cite evidence from transfer formulas, cycle IDs, source artifacts, symbolic-auditor outputs, theorem references, or explicit unknowns.

## Output Contract

Return:

1. `Source And Target`: exact objects and classes.
2. `Reduction Type And Direction`: including contrapositive if used.
3. `Parameter Map`: lengths, exponents, overheads, advice, and query structure.
4. `Transfer Inequality`: formula and side conditions.
5. `Consistency Verdict`: valid, conditional, repair needed, bounded only, or invalid.
6. `Validation Handoff`: symbolic audit, derivation builder, quantifier reviewer, or quarantine reason.

## Failure/Demotion

Demote if the branch cannot state reduction direction, hides a promise/domain shift, drops a parameter, or claims target progress from a bounded exponent window. Quarantine repeated transfers that cannot name source, target, map, inequality, and escape condition.
