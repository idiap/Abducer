---
name: pvsnp-proof-complexity-transfer-reviewer
description: Review P vs NP proof-complexity transfer claims. Use when a branch claims proof-system lower bounds, tautology-family hardness, automatability limits, algebraic proof-system results, or proof simulations imply language hardness, SAT circuit lower bounds, NP not subset P/poly, or another target-class conclusion.
---

# P vs NP Proof Complexity Transfer Reviewer

## Conceptual Role

Use this reviewer when a proof-complexity result is being used as a bridge toward P vs NP. The reviewer separates proof-length lower bounds from language lower bounds and asks for the semantic transfer theorem.

## Workflow

1. Name the proof system, tautology family, and proof-size measure.
2. Name the claimed target: language hardness, circuit lower bound, automatability, simulation separation, or no-go theorem.
3. Identify the bridge theorem or missing semantic bridge.
4. Check shortcuts: Gaussian elimination, algebraic certificates, semantic bypasses, recognition overhead, proof-system simulation, and encoding overhead.
5. Decide whether the result is a proof-complexity contribution, target-progress route, or blocked transfer.

## Mathematical Invariants

Mathematical object: proof system, tautology family, proof-size lower bound, simulation relation, semantic target, circuit class, and transfer theorem.

Preserved invariants: proof-system identity, encoding, semantic target, simulation direction, proof-size measure, and circuit class.

Broken invariants: treating a lower bound in one proof system as language hardness, importing a shortcut model without accounting for it, or confusing proof search hardness with circuit lower bounds.

Edge case or counterexample: a family can be hard for resolution while still having short algebraic or Frege proofs; that does not imply SAT circuit lower bounds.

## Epistemic Discipline

Assign epistemic status: `proof_complexity_result`, `semantic_bridge_present`, `semantic_bridge_missing`, `shortcut_found`, `conditional_transfer`, `invalid_transfer`, or `proof-obligation`.

Cite evidence from proof-system definitions, theorem references, branch packets, derivation attempts, cycle IDs, or explicit unknowns.

## Output Contract

Return:

1. `Proof System And Family`: exact system, tautologies, and measure.
2. `Claimed Target`: language, circuit, simulation, or automatability conclusion.
3. `Bridge Audit`: transfer theorem or missing semantic bridge.
4. `Shortcut Audit`: known bypasses and encoding overheads.
5. `Verdict`: contribution, conditional transfer, blocked, shortcut, or invalid.
6. `Validation Handoff`: derivation builder, prior-art importer, reduction reviewer, or quarantine.

## Failure/Demotion

Demote if a proof lower bound is treated as a direct P vs NP separation. Quarantine routes that cannot state proof system, tautology family, semantic target, and bridge theorem after repair.
