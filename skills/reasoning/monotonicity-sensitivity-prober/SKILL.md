---
name: monotonicity-sensitivity-prober
description: Analyze how one physics quantity changes when another is varied, including increasing, decreasing, saturating, diverging, converging, sign-changing, threshold, nonmonotone, or ambiguous behavior. Use when Abducer needs directional qualitative understanding with explicit held-fixed variables and valid regimes.
---

# Monotonicity Sensitivity Prober

## Conceptual Role

Use this skill to infer the directional behavior of one quantity under a controlled variation. It should answer "if this variable changes, what changes, in what direction, at what rate class, under what assumptions, and where can that statement fail?"

This is not a scoring rubric. Generate a local sensitivity story: derivative sign, elasticity, threshold, saturation, divergence, hysteresis, nonmonotonicity, and ambiguity where appropriate.

## Procedure

1. Select one varied variable, one response variable, and the held-fixed conditions.
2. State the candidate relation as `response` versus `driver` within a named regime.
3. Reason through the sign or direction using equations, scaling, variational principles, conservation, convexity, positivity, spectral representation, or a toy calculation.
4. Classify the behavior: increasing, decreasing, saturating, divergent, convergent, thresholded, sign-changing, nonmonotone, hysteretic, or unknown.
5. Estimate the rate class when meaningful: linear, sublinear, polynomial, logarithmic, exponential, stretched exponential, bounded, or singular.
6. Identify sensitivity amplifiers and dampers: hidden couplings, near-criticality, small denominators, degeneracy, normalization, or cutoff effects.
7. Name disconfirming observations and hand unresolved claims to a concrete probe, falsifier, or graph update.

## Mathematical Invariants

- Mathematical object: driver, response, held-fixed controls, derivative or comparison relation, regime, and observable.
- Preserved invariants: one-variable variation, regime-local validity, dimensional consistency, and response/driver direction.
- Broken invariants: changing controls while attributing effect to the driver, using correlation as sensitivity, assuming monotonicity from a single endpoint, or omitting thresholds.
- Edge case or counterexample: a relation can be increasing locally but nonmonotone globally; always test endpoint, near-critical, and singular regimes.

## Epistemic Discipline

Assign epistemic status: `direction_supported`, `rate_supported`, `threshold_suspected`, `nonmonotone_suspected`, `ambiguous`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, KB IDs, cycle IDs, equations, source artifacts, concrete probes, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground sensitivity. If a small numerical or symbolic probe is cheap and relevant, run it, inspect the artifact, then state what transfers and what remains heuristic.

## Output Contract

Return:

1. `Controlled Variation`: driver, response, held-fixed controls, and validity regime.
2. `Direction Claim`: sign, monotonicity class, rate class, and reasoning.
3. `Sensitivity Mechanism`: why the response changes, including amplifiers or dampers.
4. `Failure Modes`: threshold, saturation, sign reversal, nonmonotonicity, hidden coupling, or boundary-regime failure.
5. `Disconfirming Observation`: what would falsify or demote the relation.
6. `Graph Edge`: source node, target node, relation type, regime, epistemic status, and evidence.
7. `Validation Handoff`: relation packet, toy model, falsifier, graph validator, or next experiment.

## Failure/Demotion

Demote when no held-fixed controls are named, the response variable is not typed, the direction is unsupported, or the relation is asserted globally from local reasoning. Quarantine sensitivity claims that depend on analogy-only transfer.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after producing graph-ready sensitivity edges.
