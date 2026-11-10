---
name: scale-asymptotic-reasoner
description: Infer qualitative scale behavior, dominant balance, asymptotic class, transition scales, and breakdown conditions. Use when a physics branch needs to compare linear, polynomial, logarithmic, exponential, stretched-exponential, threshold, saturation, or RG-style scale behavior.
---

# Scale Asymptotic Reasoner

## Conceptual Role

Use this skill when the key question is how a quantity behaves as a scale changes or tends to a limit. It should identify dominant balances, crossover scales, asymptotic classes, and failure regimes rather than simply saying "large" or "small".

This is generative asymptotic reasoning. Produce competing asymptotic stories, state which terms dominate, and explain how the conclusion would change if the dominant term, fixed point, or scaling variable is wrong.

## Procedure

1. Identify the scale variable, response quantity, regime, and limiting direction.
2. List candidate asymptotic forms: constant, linear, polynomial, logarithmic, exponential, stretched exponential, power law with corrections, threshold, saturation, or divergent.
3. Derive or motivate dominant balance using dimensions, equations, spectral representations, RG flow, estimates, comparison principles, or a toy model.
4. Identify crossover scales and the parameter combinations that control them.
5. State what is uniform in the asymptotic statement and what is only pointwise or finite-regime.
6. Compare at least two asymptotic alternatives and name an observation that discriminates them.
7. Emit graph edges only as regime-qualified asymptotic relations.

## Mathematical Invariants

- Mathematical object: scale variable, response, asymptotic limit, dominant terms, crossover scale, and validity regime.
- Preserved invariants: dimensional balance, limiting direction, uniformity statement, and source/target object typing.
- Broken invariants: extrapolating finite-scale behavior to a limit, confusing exponential and stretched-exponential decay, suppressing correction terms that dominate in another regime, or changing the limiting object.
- Edge case or counterexample: a pre-asymptotic apparent law can reverse once the true dominant balance takes over.

## Epistemic Discipline

Assign epistemic status: `dominant_balance_supported`, `candidate_asymptotic`, `crossover_unknown`, `preasymptotic_only`, `uniformity_needed`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, KB IDs, cycle IDs, equations, source artifacts, validators, concrete probes, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the asymptotics. Use small symbolic or numerical probes only as calibration, inspect outputs, and mark transfer limits.

## Output Contract

Return:

1. `Scale Setup`: scale variable, response quantity, limiting direction, and held-fixed controls.
2. `Candidate Asymptotics`: plausible forms and why each is possible or excluded.
3. `Dominant Balance`: controlling terms, mechanisms, and crossover scales.
4. `Uniformity Statement`: pointwise, uniform, fixed-regime, continuum, infinite-volume, or unknown.
5. `Discriminating Probe`: observation, calculation, or estimate that separates alternatives.
6. `Failure Modes`: pre-asymptotic trap, nonuniformity, hidden scale, phase transition, or proxy drift.
7. `Validation Handoff`: relation packet, limit auditor, toy model, graph validator, or next experiment.

## Failure/Demotion

Demote when no scale variable is isolated, the asymptotic class is guessed without a mechanism, uniformity is missing, or finite-scale behavior is promoted to a limiting claim. Quarantine analogy-only scaling stories.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` for graph-ready asymptotic claims.
