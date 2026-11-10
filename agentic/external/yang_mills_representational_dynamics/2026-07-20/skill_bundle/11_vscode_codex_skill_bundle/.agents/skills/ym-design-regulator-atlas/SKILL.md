---
name: ym-design-regulator-atlas
description: Generate and audit a regulator atlas for constructive Yang--Mills theory without privileging prior finite models. Use when comparing Wilson, heat-kernel, Villain-type, Hamiltonian, flowed-observable, or multiscale regulators for gauge invariance, reflection positivity, locality, RG closure, topology, observable renormalization, and continuum universality.
---

# Design a Yang--Mills Regulator Atlas

## Workflow

1. Freeze the continuum target and observable core before scoring regulators.
2. Specify each candidate's carrier, action/measure, gauge action, positivity structure, boundary conditions, and parameters.
3. Test exact gauge invariance, locality, reflection positivity, transfer construction, and finite-volume well-definedness.
4. Test closure or controlled enlargement under block RG.
5. Audit small-field coordinates, large fields, topological sectors, and gauge-orbit coverage.
6. State renormalization requirements for local composites and extended observables.
7. Separate proved universality from expected universality.
8. Rank candidates by the severity of missing bridges to a nontrivial OS-positive continuum theory.
9. Select a primary regulator and an adversarial alternative; justify the choice with theorem obligations.

## Comparison matrix

Always include: exact invariances; positivity; locality; RG compatibility; large-field control; topology; continuum scaling; observable completeness; known rigorous regime; failure modes; and claim status.

## Guardrails

- Do not select a regulator because prior work already uses it.
- Do not assume regulator independence; formulate a universality theorem target.
- Reject regulators whose positivity loss has no recovery route.
- Mark strong-coupling and weak-coupling regimes separately.
- Treat dual or extra-dimensional regulators as changes of theory until exact equivalence is proved.

## Output contract

Return the atlas, evidence-backed ranking, selected primary and adversarial regulators, required universality theorem, and exact reasons any candidate is excluded.
