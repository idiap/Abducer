---
name: gedanken-counterfactual-variant-builder
description: Generate counterfactual variants of a Gedanken experiment to test which variable, assumption, regime, or mechanism is actually responsible for the expected observation. Use when a thought experiment needs sharper contrasts before it can guide a follow-up cycle.
---

# Gedanken Counterfactual Variant Builder

## Conceptual Role

Use this skill after a candidate situation exists. The goal is to prevent one-story explanations by changing one condition at a time and predicting how the observation should change. Variants reveal whether the claimed insight depends on a phase, cutoff, boundary condition, hidden variable, observable sector, limit order, or transfer assumption.

## Functional Generation Requirements

Build variants against the current packet's decisive mechanism. At least one variant must be capable of demoting the baseline by preserving the target setup while removing, reversing, delaying, or weakening the alleged mechanism. Avoid decorative variants that merely rename the situation.

## Procedure

1. Identify the baseline situation and its expected observation.
2. Select one condition to change: variable value, held-fixed assumption, regime, symmetry, boundary, observable, or limit order.
3. Predict the changed observation and the reason.
4. Say whether the variant sharpens, disconfirms, or quarantines the baseline situation.
5. Add the variant to the Gedanken packet and any qualitative graph edge it challenges.

## Mathematical Invariants

- Mathematical object: baseline situation, changed condition, expected observation, and target relation.
- Preserved invariants: one-change-at-a-time contrast, source/target typing, validity regime, and held-fixed controls.
- Broken invariants: changing many variables at once, losing the target object, or explaining the same outcome under all variants.
- Edge case or counterexample: include at least one variant designed to reverse, erase, or delay the expected observation.

## Epistemic Discipline

Assign an explicit epistemic status to each variant: `diagnostic`, `falsifying`, `rescue`, `transfer_test`, or `explicit_unknown`. Cite source artifacts, packet IDs, graph edges, equations, or explicit unknowns. A variant that cannot change the observation is not informative unless it explains invariance.

The packet validator treats variants with empty or non-diagnostic `predicted_change` values such as `none`, `no change`, or `unchanged` as failures. If invariance itself is the claim, spell out why invariance is diagnostic and what would falsify that invariance.

## Output Contract

Return:

1. `Baseline`: packet or situation being varied.
2. `Changed Condition`: exactly one change and why it matters.
3. `Held Fixed`: what remains unchanged.
4. `Predicted Change`: expected observation shift.
5. `Diagnostic Value`: what this teaches about mechanism or transfer.
6. `Demotion Trigger`: what result would challenge the baseline.
7. `Graph Consequence`: whether the variant should `challenge_edge`, `revise_edge`, `annotate_edge`, `needs_probe`, or `quarantine`.
8. `Validation Handoff`: updated packet and validator command.

## Failure/Demotion

Demote variants that alter the target problem, change too many assumptions, have no predicted observational difference, or only make the story more vivid. Falsify a baseline if the decisive observation persists after the purported mechanism is removed.

## Validation Handoff

Run `python agentic/scripts/validate_gedanken_experiment_packets.py` after adding variants. If a variant suggests a concrete calculation, hand it to `qualitative-toy-model-builder` or the ranked next-experiment queue.
