---
name: qualitative-physics-falsifier
description: Generate relation-specific edge cases, counter-regimes, and falsifiers for qualitative physics claims. Use when a variable relation needs tests for sign reversal, nonmonotonicity, nonuniform convergence, singular perturbation, hidden variables, symmetry violation, positivity failure, or proxy drift.
---

# Qualitative Physics Falsifier

## Conceptual Role

Use this skill to attack a qualitative relation before the loop relies on it. It should generate the smallest counter-regime, variant, or disconfirming observation that would demote the claim.

This is adversarial generative reasoning. Do not merely list generic risks. Construct relation-specific falsifiers tied to the actual variables, regimes, constraints, and transfer claims.

## Procedure

1. Restate the relation claim, variables, regime, graph edge, and evidence basis.
2. Identify the weakest premise the claim depends on.
3. Generate falsifier families: sign reversal, nonmonotonicity, threshold failure, singular perturbation, hidden coupling, symmetry violation, positivity failure, boundary-condition dependence, nonuniform limit, or proxy drift.
4. For each falsifier, state the concrete observation or calculation that would trigger demotion.
5. Rank falsifiers by discriminating power and feasibility.
6. Decide branch effect: adapt, backtrack, quarantine, stop candidate after repeat failure, or keep as proof obligation.
7. Emit graph update advice and queue-ready next experiment when a falsifier is high value.

## Mathematical Invariants

- Mathematical object: challenged relation, weakest premise, counter-regime, disconfirming observation, and graph edge.
- Preserved invariants: target relevance, source/target typing, regime labeling, and explicit demotion criteria.
- Broken invariants: generic skepticism without a test, falsifier that changes the target problem, or counterexample that only attacks an analogy.
- Edge case or counterexample: a falsifier is strongest when it preserves the claimed setup but changes exactly the premise alleged to control the behavior.

## Epistemic Discipline

Assign epistemic status: `falsifier_ready`, `counter_regime_suspected`, `needs_probe`, `challenged`, `invalidated`, `quarantine`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, KB IDs, cycle IDs, graph edges, equations, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when a small calculation or validator can test a falsifier. Run the smallest relevant command, inspect the artifact, and separate disconfirmation from unresolved uncertainty.

## Output Contract

Return:

1. `Claim Under Attack`: relation, variables, regime, edge, and evidence.
2. `Weakest Premises`: assumptions that would collapse the relation if false.
3. `Falsifier Set`: concrete counter-regimes, variants, or observations.
4. `Disconfirmation Criteria`: exact result that demotes, quarantines, or invalidates the claim.
5. `Priority`: which falsifier should be tested first and why.
6. `Branch/Graph Effect`: adapt, backtrack, challenge edge, quarantine, or stop candidate with rescue condition.
7. `Validation Handoff`: validator, toy model, queue item, or graph update.

## Failure/Demotion

Demote falsifier plans that are generic, impossible to observe, unrelated to the target relation, or require changing the mathematical object. Quarantine analogy-only attacks separately from same-target counterexamples.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after falsifier-driven graph updates.
