---
name: qualitative-toy-model-builder
description: Choose and solve small concrete models that calibrate qualitative physics intuition, such as finite matrices, spectral measures, heat kernels, simple RG maps, noncommuting limits, or finite-volume probes. Use when a qualitative relation is underdetermined and needs a bounded concrete setting.
---

# Qualitative Toy Model Builder

## Conceptual Role

Use this skill when conceptual reasoning is underdetermined and a small solved setting can reveal a sign, scaling class, failure mode, or transfer boundary. The toy model is a microscope, not a substitute target.

This is a generative construction skill. Choose a minimal carrier that preserves the mechanism under study, solve or compute it when feasible, and explicitly state what does and does not transfer to the active target.

## Procedure

1. State the unresolved qualitative question and the target mechanism it is meant to probe.
2. Choose a minimal mathematical carrier: finite matrix, two-state system, spectral measure, scalar kernel, small graph, recurrence, ODE, RG map, constrained optimization problem, or finite-volume lattice sketch.
3. Name variables, controls, observables, and the regime the toy model represents.
4. Solve analytically when possible; otherwise run a small bounded computation and inspect the result.
5. Compare baseline and at least one variant that removes or reverses the proposed mechanism.
6. Extract only qualitative lessons: direction, threshold, saturation, asymptotic class, obstruction, or falsifier.
7. State the transfer certificate required before the lesson can affect proof obligations or graph edges.

## Mathematical Invariants

- Mathematical object: toy carrier, target mechanism, variables, observable, solved relation, variant, and transfer map.
- Preserved invariants: mechanism isolation, held-fixed controls, bounded scope, and explicit non-claim boundaries.
- Broken invariants: solving a different problem, hiding target assumptions in the toy model, using numerical coincidence as proof, or omitting a transfer certificate.
- Edge case or counterexample: include a variant where the toy lesson disappears, reverses, or becomes ambiguous.

## Epistemic Discipline

Assign epistemic status: `validated_probe`, `calibration_only`, `mechanism_supported`, `mechanism_disconfirmed`, `transfer_needed`, `explicit_unknown`, or `proof_obligation`. Cite code snippets, executed commands, artifact paths, equations, KB IDs, cycle IDs, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the model. Prefer a tiny reproducible command or inline derivation. After execution, inspect outputs and report both the qualitative consequence and the non-transfer boundaries.

## Output Contract

Return:

1. `Probe Question`: the qualitative ambiguity and target mechanism.
2. `Toy Carrier`: chosen model, variables, observables, controls, and why it is minimal.
3. `Solution Or Execution`: derivation or executed command plus inspected artifact.
4. `Baseline And Variant`: what changes and what remains fixed.
5. `Qualitative Lesson`: direction, threshold, asymptotic class, obstruction, or falsifier.
6. `Transfer Boundary`: what transfers, what does not, and certificate needed.
7. `Graph/Queue Handoff`: relation update, falsifier, next experiment, or quarantine.

## Failure/Demotion

Demote when the toy model is decorative, unsolved, changes the target mechanism, lacks a variant, or claims proof progress. Quarantine if the result is analogy-only.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after converting a toy lesson into a relation packet or graph update.
