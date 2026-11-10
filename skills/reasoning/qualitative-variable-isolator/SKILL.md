---
name: qualitative-variable-isolator
description: Extract typed variables, controls, observables, hidden scales, dependent quantities, constraints, and unresolved unknowns before qualitative physics relation claims. Use when a physics or mathematical-physics branch needs to know what can vary independently, what is held fixed, and what is only a derived response.
---

# Qualitative Variable Isolator

## Conceptual Role

Use this skill before any qualitative relation is asserted. Its job is to turn a vague phrase such as "the gap depends on the scale" into a typed variable frame: independent knobs, dependent responses, hidden couplings, observables, constraints, regimes, and held-fixed assumptions.

This is a generative skill. Do not merely copy variable names from the prompt. Infer missing variables, ask whether they are independent or derived, expose hidden parameters, and split overloaded quantities into separate mathematical objects.

## Procedure

1. Name the mathematical object and the observable being discussed.
2. Build a variable table with `symbol`, `meaning`, `role`, `units_or_scaling`, `allowed_range`, `held_fixed_when`, and `depends_on`.
3. Separate independent variables from response variables, constraints, gauge choices, cutoff parameters, limiting parameters, and purely descriptive labels.
4. Identify hidden couplings: a variable that appears independent but changes another quantity through a definition, conservation law, normalization, boundary condition, or order of limits.
5. State which variables are safe to vary one at a time and which require a regime map before variation.
6. Emit graph-ready node candidates and relation stubs only after roles are typed.
7. Recommend the next qualitative skill: `physics-regime-map-builder`, `monotonicity-sensitivity-prober`, `limit-convergence-behavior-auditor`, or `qualitative-toy-model-builder`.

## Mathematical Invariants

- Mathematical object: the carrier object, variable set, observable algebra, constraints, scales, regimes, and target proof obligation.
- Preserved invariants: source/target typing, dimensional consistency, held-fixed assumptions, allowed ranges, and explicit dependency direction.
- Broken invariants: treating a dependent response as an independent knob, suppressing a cutoff or volume parameter, changing the observable while claiming only the variable changed, or using a proxy quantity without transfer.
- Edge case or counterexample: if varying one variable necessarily changes another through a constraint, the one-variable story is invalid until the constrained path is stated.

## Epistemic Discipline

Assign epistemic status: `typed`, `partially_typed`, `hidden_coupling_suspected`, `proxy_risk`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, KB IDs, cycle IDs, equations, source artifacts, validators, or explicit unknowns for every nontrivial variable role. Do not present a variable frame as theorem progress.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the frame. Use deterministic builders or validators only after identifying the variable roles; then inspect the produced relation packet or graph before drawing a qualitative conclusion.

## Output Contract

Return:

1. `Object And Observable`: carrier, target quantity, branch obligation, and source artifact.
2. `Variable Frame`: independent variables, dependent responses, hidden couplings, controls, constraints, and unknowns.
3. `Held-Fixed Conditions`: what must remain unchanged for each proposed variation.
4. `Safe Variations`: one-variable moves that are meaningful, plus constrained variations that require a path.
5. `Graph Seeds`: graph-ready node IDs, possible edge directions, and why they remain stubs.
6. `Failure Modes`: proxy drift, hidden dependence, dimension mismatch, untyped regime, or noncommuting-limit risk.
7. `Validation Handoff`: packet, graph, validator, or next qualitative skill.

## Failure/Demotion

Demote when the output lists nouns without roles, omits held-fixed assumptions, treats all quantities as independently variable, or fails to name a mathematical object. Quarantine graph seeds when a proxy observable replaces the target object.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py` after relation packets exist, then `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>` and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after graph updates.
