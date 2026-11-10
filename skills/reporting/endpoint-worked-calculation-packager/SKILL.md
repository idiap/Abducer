---
name: endpoint-worked-calculation-packager
description: Turn a concrete endpoint, finite-block, or local model calculation into a paper-ready worked example. Use when a paper needs an explicit table, color/geometric factors, sign or eigenvalue test, numerical/symbolic bound, and reproducible calculation notes rather than open-ended theoretical exploration.
---

# Endpoint Worked Calculation Packager

## Workflow

1. Identify the concrete finite geometry, regulator, variables, and observables.
2. Build the incidence/sign table or finite matrix used in the calculation.
3. Separate universal positive terms, cancelling terms, and dangerous residual terms.
4. Compute or bound the decisive scalar, determinant, eigenvalue, or sign condition.
5. Record how the calculation can be reproduced symbolically or numerically.
6. State exactly what the worked example validates, falsifies, or leaves open.

## Output Contract

Return: calculation target, setup, tables/matrices, formula derivation, computed value or bound, reproducibility notes, validation decision, and unresolved assumptions.

## Epistemic Discipline

Keep the calculation tied to a concrete finite mathematical object or instance. Preserve epistemic status explicitly as exact, controlled approximation, numerical evidence, conjectural interpretation, proof-obligation, blocked, promoted, or demoted. Cite source artifacts, artifact paths, cycle IDs, KB IDs when available, and explicit unknowns before treating a computation as evidence for a mechanism or obstruction. Separate exact algebra, controlled approximation, numerical evaluation, and interpretive consequence under the stated regulator, geometry, observable family, and transfer assumptions.

## Validation Handoff

Hand off reproducibility artifacts: finite inputs, formula sequence, symbolic simplification notes, numerical tolerance if used, sign or eigenvalue criterion, and falsifiers. The calculation is successful only when another agent can rerun or independently check the decisive scalar, determinant, spectrum, or bound.

## Failure/Demotion

Demote the calculation if it only restates the route, omits the finite inputs, hides regulator assumptions, lacks a sign/eigenvalue test, or cannot be reproduced.
