---
name: results-finite-object-formalizer
description: Formalize the finite or local mathematical object that controls a result candidate. Use when a paper subgoal depends on a new parameter, certificate, obstruction, finite construction, quotient, residual set, interface, or local model that must be defined before proof or validation.
---

# Results Finite Object Formalizer

## Conceptual Role

This skill makes the central object of a result precise enough to prove with. It is for parameters and finite structures that recur across domains: forced-row sets, Schur complements, certificates, exceptional sets, quotient objects, carrier interfaces, local toy models, or finite obstruction witnesses.

## Workflow

1. Extract the object name and the mathematical role it plays.
2. Define the ambient universe, indices, equivalence relation or closure operation, size/complexity measure, and validity regime.
3. Separate local/finite definitions from asymptotic, continuum, or full-theory claims.
4. Build at least one minimal worked example or counterexample showing what the definition includes and excludes.
5. State the proof-use contract: which lemma can use the object, which inequality it supports, and which falsifier it enables.

## Definition Checklist

Every finite object packet must state:

- ambient set or carrier;
- source and target variables;
- closure/forcing/support rule;
- size, norm, rank, count, cost, or exponent measure;
- model and uniformity/advice/regulator assumptions;
- what would falsify the intended use.

## Output Contract

Return: object definition, notation table, ambient universe, validity regime, worked example, non-example, proof-use contract, falsifier, and downstream theorem lemma.

## Epistemic Discipline

Assign an epistemic status to the finite object: definition-ready, example-tested, proof-ready, conditional, inconsistent, or demoted. Cite evidence through source artifacts, KB IDs, cycle IDs, theorem labels, draft sections, validation reports, or explicit unknowns. State the mathematical object, invariant, and edge case or counterexample that controls its use.

## Guardrails

- Do not define a parameter by the conclusion it is meant to prove.
- Do not collapse "touching", "forcing", "supporting", "certifying", and "computing"; distinguish the relation that matters.
- Do not use a finite object to claim a full theorem without the transfer bridge.
- Do not hide nonuniform advice, regulator dependence, or model changes in notation.

## Validation Handoff

Hand off to `results-proof-packet-deriver` for the lemma proof and to domain reviewers for model-specific consistency checks.

## Failure/Demotion

Demote or return to scoping if the object cannot be defined independently of the target theorem, if examples contradict the intended lemma, or if the object only names a vibe rather than a manipulable structure.
