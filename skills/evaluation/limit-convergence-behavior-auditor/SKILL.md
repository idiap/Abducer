---
name: limit-convergence-behavior-auditor
description: Audit qualitative claims about limits, convergence, divergence, saturation, noncommuting limits, and uniformity. Use when a physics branch moves from fixed cutoff, finite volume, finite time, toy setting, or local estimate to continuum, infinite-volume, long-time, or spectral conclusions.
---

# Limit Convergence Behavior Auditor

## Conceptual Role

Use this skill whenever a qualitative claim crosses a limit. Its job is to decide whether the relation survives the passage from fixed regulator, finite volume, finite time, toy model, or pointwise estimate to the target limiting object.

This is not a generic caution. Identify the actual limiting map, the topology or mode of convergence, uniformity requirements, order-of-limit choices, and what breaks if the limits do not commute.

## Procedure

1. Name the source object, target limiting object, limit parameters, and order of limits.
2. Classify the convergence claim: pointwise, uniform, weak, distributional, norm, tightness, subsequential, limsup/liminf, or unknown.
3. State which qualitative relation is being transported across the limit.
4. Audit uniformity: constants, estimates, positivity, observable density, support bounds, or decay rates that must not vanish or blow up.
5. Check noncommuting limits by swapping order or holding one parameter fixed.
6. Identify leakage: mass to zero, spectral weight escaping, loss of compactness, boundary effects, renormalization drift, or observable collapse.
7. Emit a verdict and next proof obligation.

## Mathematical Invariants

- Mathematical object: source family, target limit, topology, limit parameters, estimates, observables, and transported relation.
- Preserved invariants: same-theory transfer, uniform constants, closed positivity cones, observable survival, and typed order of limits.
- Broken invariants: fixed-cutoff overreach, vanishing constants, loss of density, noncommuting limits, or convergence in a topology too weak for the claimed relation.
- Edge case or counterexample: a relation can hold for every finite cutoff while failing in the limit because the witness escapes, constants collapse, or the observable sector changes.

## Epistemic Discipline

Assign epistemic status: `limit_safe`, `uniformity_needed`, `order_of_limits_blocked`, `pointwise_only`, `leakage_suspected`, `invalidated`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, equations, KB IDs, cycle IDs, source artifacts, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground a finite-to-limit probe. Inspect produced artifacts before deciding whether the result is merely finite-regime evidence or a transferable limit statement.

## Output Contract

Return:

1. `Limit Map`: source family, target object, parameters, topology, and order of limits.
2. `Transported Relation`: qualitative claim being moved across the limit.
3. `Uniformity Audit`: constants, estimates, support, density, positivity, or decay that must survive.
4. `Noncommuting-Limit Test`: swapped order, fixed-parameter trap, or missing comparison.
5. `Leakage Modes`: what can vanish, escape, blow up, or change object.
6. `Verdict`: limit safe, needs uniformity, pointwise only, blocked, challenged, or invalidated.
7. `Validation Handoff`: proof obligation, graph status, falsifier, toy model, or queue item.

## Failure/Demotion

Demote when a claim moves from finite to infinite or cutoff to continuum without topology, uniformity, or order-of-limit control. Quarantine results that are only fixed-regime evidence.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after limit-audited relation updates.
