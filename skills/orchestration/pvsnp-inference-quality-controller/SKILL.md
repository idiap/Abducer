---
name: pvsnp-inference-quality-controller
description: Control the quality of P vs NP inference steps before branch promotion, proof-queue insertion, report claims, or paper-facing conclusions. Use when a P vs NP branch states a transfer, theorem-shaped claim, contradiction, no-go result, barrier diagnosis, source-to-target implication, or publishable subgoal and needs source/target typing, quantifier and model discipline, proof-status routing, and consistency reviewer handoff.
---

# P vs NP Inference Quality Controller

## Conceptual Role

Use this skill as the central gate between creative P vs NP exploration and accepted claims. Its job is to turn a branch claim into a typed inference packet and decide whether it should be derived, repaired, reviewed, quarantined, or rejected.

The controller is generative: it interprets the mathematical move, identifies what kind of inference is being attempted, and routes it to the right reviewer. It is not a proof by itself.

## Workflow

1. **Restate the exact claim.** Name the source statement, target statement, route family, intended inference rule, and current epistemic status.
2. **Type the mathematical objects.** Record the language or carrier, target complexity class, circuit model, proof system if any, oracle/algebraic status, promise/domain regime, and input-length map.
3. **Audit quantifiers and side conditions.** Check all lengths versus infinitely often, all exponents versus fixed exponent, uniform versus nonuniform, advice-free versus advice-bearing, and algorithm versus circuit family.
4. **Classify the inference.** Choose one: transfer inequality, reduction, barrier diagnosis, contradiction, impossibility theorem, proof-complexity transfer, meta-complexity carrier claim, or paper-contribution claim.
5. **Route derivation and reviewers.** Send theorem-shaped claims to `pvsnp-proof-derivation-builder`; send transfer claims to `pvsnp-reduction-consistency-reviewer`; send quantifier-sensitive claims to `pvsnp-quantifier-uniformity-reviewer`; send barrier claims to `pvsnp-barrier-specificity-reviewer`.
6. **Emit a decision.** Use `accept_for_derivation`, `needs_repair`, `review_only`, `quarantine`, or `reject_overclaim`.

## Guardrails

Do not accept a claim because it sounds aligned with the P vs NP target. Do not let a proxy lower bound count as SAT hardness without a transfer theorem. Do not let a branch strengthen its conclusion beyond its premises by switching model, quantifiers, advice, oracle status, or valid-length regime.

Reject overclaim when the branch claims `P != NP`, `NP not subset P/poly`, or all-polynomial circuit lower bounds from a fixed-exponent, sparse-length, promise, nonuniform, advice-bearing, or barrier-diagnostic result without an explicit transfer certificate.

## Epistemic Discipline

Assign epistemic status: `proved`, `conditional_theorem`, `proof-obligation`, `derivation-needed`, `heuristic-pressure`, `barrier-backed`, `falsifier`, `no-go-candidate`, `repaired`, `quarantined`, or `rejected-overclaim`.

Cite evidence from KB IDs, cycle IDs, branch IDs, report sections, theorem references, validator outputs, exact script outputs, or explicit unknowns. A missing premise is evidence only for a proof obligation, not for target progress.

## Codex Exec Protocol

When a deterministic artifact is available, follow `docs/reference/codex-exec-skill-protocol.md`: inspect the packet, run the relevant validator, and interpret the result mathematically. Do not leave validation output uninterpreted. Use executed commands and artifact inspection as evidence, but never treat a passing schema check as a proof.

## Output Contract

Return:

1. `Inference Claim`: source statement, target statement, branch ID, route family, and intended inference rule.
2. `Typing Ledger`: source carrier/language, target class, circuit/proof model, oracle/algebraic status, promise/domain, input lengths, and parameters.
3. `Quantifier Ledger`: length regime, exponent regime, uniformity, advice, randomness, and family/algorithm distinction.
4. `Side Conditions`: theorem hypotheses, transfer assumptions, barrier assumptions, escape conditions, and hidden premises.
5. `Reviewer Routing`: exact reviewer skills required and why.
6. `Decision`: accept for derivation, needs repair, review only, quarantine, or reject overclaim.
7. `Validation Handoff`: packet path, validator, next proof obligation, or report section.

## Failure/Demotion

Demote if source and target are not typed in the same model, if reduction direction is unclear, if quantifiers are stronger in the conclusion than the premises, if advice leakage is hidden, if barrier labels are generic, or if a theorem-shaped claim has no derivation status. Quarantine repeated claims that cannot name source object, target class, transfer rule, side conditions, and validation handoff.
