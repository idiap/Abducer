---
name: lemma-chain-proof-builder
description: Build and attempt dependency-typed lemma chains for proof-delivery queue items. Use when a formalized theorem, transfer result, no-go theorem, finite criterion, or paper subgoal needs an actual proof attempt with established lemmas, conditional lemmas, blocked lemmas, proof steps, edge cases, and counterexample checks.
---

# Lemma Chain Proof Builder

## Role

Use this skill to do proof work. The output should read like a mathematician's proof packet: each lemma has a role, proof status, dependencies, and failure mode.

## Mathematical Invariants

Preserve the mathematical object named in the theorem statement: definitions, carrier/model, quantifiers, parameters, validity regime, and dependency order must remain stable across every lemma. The core mathematical invariant is implication preservation: no proof step may reverse direction, strengthen a conclusion silently, weaken a premise silently, lose an exponent or constant, or move between finite/asymptotic, uniform/nonuniform, analytic/geometric, or semantic/syntactic regimes without an explicit lemma.

Counterexample and edge-case checks are part of the invariant ledger. Boundary regimes, degenerate objects, small-size cases, proxy models, and parameter extremes must either satisfy the lemma hypotheses or be recorded as blocked lemmas, falsifiers, or scope restrictions.

## Epistemic Discipline

Every lemma must carry an epistemic status: `proved`, `conditional`, `blocked`, `false_under_countermodel`, `definition_only`, or `requires_prior_art`. Cite the evidence source artifacts, KB IDs, reports, or cycle IDs that justify each dependency; if a dependency has no evidence citation, treat it as an explicit unknown rather than a hidden premise.

The validation handoff is to `proof-quality-gatekeeper` plus any target-specific reviewer named by the queue item. Demote or quarantine a lemma chain when disconfirming evidence, a counterexample, missing prior art, or a target-equivalent assumption blocks the proof.

## Workflow

1. **Order the lemmas.** Start from definitions and build toward the theorem conclusion. Avoid circular dependencies.
2. **Prove locally.** For each lemma, write proof steps and state exactly where prior lemmas or assumptions enter.
3. **Propagate parameters.** Track exponents, constants, dimensions, ranks, norms, lengths, advice, uniformity, remainders, and validity regimes through every implication.
4. **Check edge cases.** Test degenerate, boundary, small, sparse, nonuniform, proxy, or model-switch cases before promotion.
5. **Classify each lemma.** Use `proved`, `conditional`, `blocked`, `false_under_countermodel`, `definition_only`, or `requires_prior_art`.
6. **Assemble theorem disposition.** The theorem can be delivered only when all required lemmas are proved or explicitly conditional.

## Output Contract

Return:

1. `Theorem`
2. `Lemma Chain`: ordered lemmas with status, dependencies, proof, and failure mode.
3. `Parameter Ledger`: where each quantitative term is introduced and preserved.
4. `Proof Assembly`: final derivation from lemmas.
5. `Blocked Lemmas`: exact missing statement and next proof action.
6. `Counterexample Checks`
7. `Epistemic Status`

## Failure/Demotion

Demote if the proof jumps over a central lemma, reverses an implication, loses a parameter, changes the model, ignores edge cases, or cannot identify the exact place where the proof blocks.
