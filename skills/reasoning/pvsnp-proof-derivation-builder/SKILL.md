---
name: pvsnp-proof-derivation-builder
description: Derive P vs NP theorem-shaped claims, transfer inequalities, contradiction lemmas, and no-go statements as far as possible. Use when a P vs NP branch claims a lemma, proof route, impossibility theorem, proof-complexity transfer, hardness-magnification implication, or paper-level mathematical result and needs definitions, assumptions, lemma chain, proof steps, blocked obligations, and counterexample classes.
---

# P vs NP Proof Derivation Builder

## Conceptual Role

Use this skill when a P vs NP claim has become theorem-shaped. The goal is to build the proof, not to decorate a conjecture. If the proof cannot be completed, the output must say exactly which lemma is missing and what would disconfirm the claim.

## Workflow

1. **Normalize the theorem statement.** State the conclusion with all classes, models, input lengths, quantifiers, advice, and oracle/algebraic status.
2. **List definitions and assumptions.** Define `P`, `NP`, `P/poly`, `SIZE(n^c)`, proof system, carrier, reduction type, parameters, and side conditions only as needed for the claim.
3. **Build the lemma chain.** Write each lemma with premise, conclusion, proof idea, dependencies, and whether it is established, conditional, or open.
4. **Derive step by step.** Preserve direction of implication and parameter propagation. Track where each assumption is used.
5. **Search for failure regimes.** Name edge case or counterexample classes: sparse valid lengths, hidden advice, positive target-query exponent, nonuniform row selection, natural property largeness, proof-system shortcut, or oracle separation.
6. **Close or localize the proof debt.** Label the result as proved, conditional theorem, proof sketch, blocked derivation, invalid, or conjectural pressure.

## Mathematical Invariants

Mathematical object: theorem statement, definitions, assumptions, source carrier, target class, reduction or transfer rule, lemma chain, proof obligations, and counterexample classes.

Preserved invariants: source/target identity, implication direction, quantifier order, input-length map, circuit/proof model, uniformity, advice status, oracle/algebraic status, and barrier assumptions.

Broken invariants: proving a proxy lower bound while claiming SAT hardness, deriving all-exponent exclusion from a bounded exponent window, changing proof systems mid-argument, importing advice without accounting for it, or treating a barrier diagnosis as a theorem against P vs NP.

## Epistemic Discipline

Assign epistemic status: `proved`, `conditional_theorem`, `proof_sketch`, `blocked_at_named_lemma`, `counterexample_found`, `invalid_derivation`, `conjectural`, or `explicit_unknown`.

Cite evidence from KB IDs, theorem references, cycle IDs, packet IDs, CAS outputs, proof sketches, validator output, or explicit unknowns. Do not claim proof when a premise is equivalent to the target.

## Output Contract

Return:

1. `Theorem Statement`: precise conclusion and validity regime.
2. `Definitions`: only the definitions needed to verify the proof.
3. `Assumptions`: explicit hypotheses, side conditions, and non-claims.
4. `Lemma Chain`: ordered lemmas with status and dependencies.
5. `Proof Derivation`: stepwise argument preserving direction and parameters.
6. `Failure Search`: edge cases, counterexample classes, and barrier checks.
7. `Epistemic Status`: proved, conditional, blocked, invalid, or conjectural.
8. `Validation Handoff`: next reviewer, validator, theorem body, or proof obligation.

## Failure/Demotion

Demote if the proof skips definitions, hides the hard target inside a lemma, reverses a reduction, changes quantifiers, ignores advice/nonuniformity, or cannot identify where the proof fails. Quarantine a theorem route if two derivation attempts still cannot state a lemma chain and a decisive blocked obligation.
