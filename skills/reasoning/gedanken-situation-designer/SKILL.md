---
name: gedanken-situation-designer
description: Design concrete imagined situations that isolate variables, mechanisms, regimes, and expected observations for follow-up discovery cycles. Use when Abducer needs a high-information Gedanken experiment rather than another generic hypothesis or deterministic placeholder.
---

# Gedanken Situation Designer

## Conceptual Role

Use this skill to design an imagined but mathematically concrete situation. The situation should feel like a small laboratory for the concept: enough structure to force an observation, but not so much structure that it quietly changes the target problem.

The design must name the minimal world, mathematical carrier, controlled contrast, variables, held-fixed assumptions, interventions, expected observations, variants, transfer scope, and follow-up tasks.

## Functional Generation Requirements

Generate the situation from the active branch blocker, not from a generic example. The packet must explain why this imagined carrier exposes the blocker better than another deduction, direct computation, literature lookup, or qualitative relation update. If the design cannot name a branch-specific varied variable, held-fixed controls, disconfirming observation, and transfer certificate, demote or defer it.

## Procedure

1. Name the conceptual pressure: hidden variable, ambiguous mechanism, limit-order issue, transfer risk, or competing explanation.
2. Choose the minimal mathematical carrier that can make the pressure visible.
3. State what is varied and what is held fixed.
4. Predict an observation pattern and what would disconfirm it.
5. Add at least one counterfactual variant that changes one condition.
6. State what transfers, what does not transfer, and what certificate is needed.
7. Name originating cycle IDs, branch IDs, affected graph nodes or edges, and the intended `graph_update_action`.
8. Emit a packet compatible with `agentic/spec/gedanken_experiment_packet.schema.json`.

## Mathematical Invariants

- Mathematical object: minimal world, carrier, variables, interventions, observations, variants, and target bridge.
- Preserved invariants: source/target typing, controlled contrast, held-fixed assumptions, validity regime, and non-claim boundaries.
- Broken invariants: target drift, proxy substitution, missing disconfirmation, no variant, or unlicensed transfer.
- Edge case or counterexample: include a variant where the expected observation disappears, reverses, or becomes ambiguous.

## Epistemic Discipline

Label the design as `conceptual_probe`, `conjectural`, `validated_probe`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, qualitative graph edges, cycle IDs, KB IDs, equations, or explicit unknowns. Do not treat an imagined observation as evidence until a follow-up derivation, computation, or source check supports it.

## Output Contract

Return:

1. `Situation`: title, purpose, minimal world, mathematical carrier, controlled contrast, informativeness rationale, and non-claims.
2. `Variables And Controls`: variables, roles, held-fixed assumptions, and validity regimes.
3. `Interventions`: operations, varied variables, predicted direction, and decision value.
4. `Expected Observations`: observable patterns, what they teach, and what disconfirms them.
5. `Variants`: counterfactual changes and predicted shifts.
6. `Transfer Scope`: `transfer_verdict`, transfers, does not transfer, certificate needed.
7. `Graph Linkage`: `affected_node_ids`, `affected_edge_ids`, `graph_update_action`, and `proposed_graph_updates`.
8. `Follow-Up Tasks`: derive, compute, falsify, formalize, update graph, rank next experiment, backtrack, or quarantine.
9. `Validation Handoff`: generated packet and validator command.

## Failure/Demotion

Demote if the design is just an analogy, if variables are not controlled, if the expected observation cannot affect a later cycle, or if the situation cannot be connected to the active target. Quarantine if the carrier solves a different problem. Falsify the design if the proposed variant does not change anything relevant.

## Validation Handoff

Write or inspect `agentic/reports/gedanken_experiments/latest.json`, then run `python agentic/scripts/validate_gedanken_experiment_packets.py`. Pass accepted follow-up tasks to `gedanken-followup-planner`.
