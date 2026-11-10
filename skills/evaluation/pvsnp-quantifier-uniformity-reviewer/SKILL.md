---
name: pvsnp-quantifier-uniformity-reviewer
description: Review P vs NP claims for quantifier and uniformity correctness. Use when a branch may confuse all lengths with infinitely often, all exponents with fixed exponent, uniform algorithms with circuit families, advice-free claims with advice-bearing claims, or P, NP, P/poly, SIZE(n^c), and restricted circuit models.
---

# P vs NP Quantifier Uniformity Reviewer

## Conceptual Role

Use this reviewer when a claim could be true in one quantifier regime but false or insufficient in another. P vs NP progress often fails not because a formula is wrong, but because it proves the wrong quantified statement.

## Workflow

1. Extract the premise quantifiers and conclusion quantifiers.
2. Record length regime: all sufficiently large lengths, all lengths, infinitely often, sparse valid lengths, average case, promise domain, or finite toy regime.
3. Record exponent regime: fixed exponent, bounded window, all constants, subpolynomial, quasipolynomial, or unspecified.
4. Record uniformity and advice: uniform algorithm, nonuniform circuit family, P/poly advice, oracle access, randomized algorithm, or algebraic extension access.
5. Compare premise strength to conclusion strength.
6. Emit the minimum repair lemma needed to preserve the target.

## Mathematical Invariants

Mathematical object: quantified premise, quantified conclusion, complexity class, circuit family or algorithm, advice regime, and length set.

Preserved invariants: same quantifier order, no strengthening from premise to conclusion, same uniformity class, explicit advice accounting, and same length domain.

Broken invariants: fixed exponent promoted to all exponents, infinitely-often promoted to eventually/all lengths, P/poly promoted to P, advice-bearing selection promoted to uniform selection, or restricted circuit lower bound promoted to unrestricted lower bound.

Edge case or counterexample: a proof that excludes `SIZE(n^3)` circuits for SAT on infinitely many lengths is not a proof that `NP` is not contained in `P/poly`.

## Epistemic Discipline

Assign epistemic status: `quantifiers_preserved`, `quantifier_loss`, `uniformity_gap`, `advice_gap`, `length_regime_gap`, `fixed_exponent_only`, `all_exponent_ready`, `repair_required`, or `invalid_strengthening`.

Cite evidence from branch text, transfer packets, symbolic formulas, cycle IDs, theorem references, or explicit unknowns.

## Output Contract

Return:

1. `Premise Quantifiers`: length, exponent, model, advice, oracle, and randomness.
2. `Conclusion Quantifiers`: same fields for the claimed result.
3. `Strength Comparison`: whether the conclusion is equal, weaker, or stronger.
4. `Mismatch Ledger`: exact losses or invalid strengthenings.
5. `Repair Lemma`: minimal additional statement needed.
6. `Validation Handoff`: inference controller, reduction reviewer, proof derivation builder, or quarantine.

## Failure/Demotion

Demote if the output gives generic caveats without naming the quantifier mismatch. Quarantine claims that repeatedly strengthen quantifiers without a repair lemma or evidence.
