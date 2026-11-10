---
name: timeline-formal-physics-deriver
description: Build formal physics derivation sections from timeline outputs, equations, strategy-judge conclusions, and mathematical assumptions. Use when a timeline-derived paper needs a self-contained derivation with definitions, assumptions, validity conditions, obstruction criteria, and proof-obligation boundaries.
---

# Timeline Formal Physics Deriver

## Workflow

Write a derivation section that exposes the mathematics:

1. Read the narrative goal lock and derive only the mathematics needed by the locked paper subgoal.
2. Define the mathematical objects and validity regime.
3. State assumptions explicitly.
4. Present equations with stated conditions.
5. Derive the finite obstruction or bridge criterion step by step.
6. State what is proved locally and what remains a Yang-Mills proof obligation.

## Mathematical Object

For the current Yang-Mills timeline, the main object is the reflected Wilson Gram quotient near the OS reflection plane, together with its first-order tangent form and Schur-corrected second-order obstruction. For other targets, replace this with the active timeline object.

## Epistemic Discipline

Do not present a formal derivation as a proof of the target theorem unless the source theory, target object, and validation handoff are discharged. Mark local finite statements, continuum-transfer assumptions, and missing estimates separately.

Use evidence citations for every mathematical move: cite the cycle ID, report artifact path, equation source, or explicit unknown that licenses the definition, assumption, equation, or proof-obligation boundary.

## Output Contract

Return: definitions, assumptions, propositions, derivation steps, equations, validity conditions, unresolved obligations, epistemic status, and validation handoff.

## Failure/Demotion

Demote the derivation if equations lack assumptions, if a finite object is confused with a continuum theorem, if a proxy replaces the target theory, or if the proof-obligation boundary is missing.

Do not expand the derivation to adjacent routes unless the expansion is needed to prove the finite theorem, compute the first concrete case, or state the transfer certificate.

## Validation Handoff

The TeX/PDF validator must compile the derivation and find definitions, assumptions, equations, proposition, proof sketch, and unresolved obligations.
