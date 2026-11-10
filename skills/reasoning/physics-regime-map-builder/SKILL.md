---
name: physics-regime-map-builder
description: Map physical regimes, scale ranges, cutoff and volume status, boundary conditions, perturbative status, and order-of-limit assumptions for qualitative physics relations. Use when a relation might change behavior across UV/IR, finite/continuum, weak/strong, linear/nonlinear, or long-time regimes.
---

# Physics Regime Map Builder

## Conceptual Role

Use this skill when a relation may be true in one regime and false, meaningless, or unlicensed in another. Its purpose is to carve the problem into validity regions before the loop spends proof budget on a qualitative claim.

This is generative regime reasoning. Infer regime boundaries, transition variables, limiting procedures, and failure regimes. Do not just say "finite" versus "continuum"; state what mathematical object exists in each regime and what survives across the transition.

## Procedure

1. Start from the typed variable frame or infer one if absent.
2. Identify regime axes: cutoff, volume, coupling, scale separation, time, temperature, dimension, observable sector, boundary condition, linearity, perturbative status, and limiting order.
3. Partition the space into validity regions and name the transition surfaces or unknown boundaries.
4. For each region, state which equations, estimates, monotonicity claims, symmetries, and observables are valid.
5. Identify regime crossings where qualitative behavior can change sign, saturate, diverge, become nonuniform, or lose transfer.
6. Emit graph annotations that attach relation edges to validity regimes rather than global claims.
7. Hand fragile regime crossings to `limit-convergence-behavior-auditor`, `scale-asymptotic-reasoner`, or `qualitative-physics-falsifier`.

## Mathematical Invariants

- Mathematical object: regime axes, region definitions, transition surfaces, observables, limiting maps, and branch obligations.
- Preserved invariants: regime-local validity, source/target object typing, boundary conditions, and order-of-limit discipline.
- Broken invariants: using a fixed-regulator result as a continuum relation, mixing weak- and strong-coupling behavior without a bridge, or claiming a global relation from one local regime.
- Edge case or counterexample: a relation that is monotone at fixed cutoff but nonmonotone or undefined after cutoff removal must be split into distinct regime-local edges.

## Epistemic Discipline

Assign epistemic status: `regime_typed`, `transition_unknown`, `local_only`, `uniformity_needed`, `transfer_blocked`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, KB IDs, cycle IDs, equations, source artifacts, validators, or explicit unknowns. A regime map licenses where to reason; it does not prove the target.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the map. Run graph builders or validators only after the regime-local edges are specified, then inspect whether the graph preserved regime labels.

## Output Contract

Return:

1. `Regime Axes`: each axis, possible values, mathematical meaning, and why it matters.
2. `Regime Cells`: valid, invalid, unknown, and transition regimes.
3. `Local Relations`: which qualitative claims hold only in which cells.
4. `Cross-Regime Risks`: nonuniformity, noncommuting limits, phase transitions, proxy drift, or boundary-condition dependence.
5. `Graph Updates`: regime-qualified nodes, edges, and relation statuses.
6. `Failure Modes`: edge cases and counterexample regimes.
7. `Validation Handoff`: next skill, relation packet, graph validator, or queue item.

## Failure/Demotion

Demote when a map has no axes, no transition conditions, no invalid regimes, or no order-of-limit statement. Quarantine global claims that are supported only in a local regime.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after regime-qualified relation updates.
