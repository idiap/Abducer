---
name: ym-audit-frontier
description: Conservatively audit Yang--Mills construction and mass-gap programmes for circular definitions, missing quantifiers, incompatible limits, loss of positivity or locality, incomplete observables, theory-identity gaps, and unsupported frontier claims. Use before publication or whenever a conditional chain is presented as progress on the Clay problem.
---

# Audit Yang--Mills Frontier

## Audit Principle

Evaluate the weakest link in the complete implication chain. A correct conditional theorem is valuable, but its hypotheses must not be confused with established properties of four-dimensional pure Yang--Mills.

## Checklist

1. Match the theorem to the exact Clay target: existence plus a positive Hamiltonian mass gap for every compact simple gauge group.
2. Expand all cutoff, volume, distance, observable, and coupling quantifiers.
3. Check physical-unit normalization and uniformity.
4. Search for circular uses of clustering, confinement, dimensional transmutation, or a pre-existing gap.
5. Audit gauge invariance, reflection positivity, locality, and observable completeness at every representation change.
6. Verify limit order and every interchange theorem.
7. Establish that the continuum object is nontrivial pure Yang--Mills and not merely a symmetric subsequential limit.
8. Separate stochastic, transfer-matrix, sectorial, finite-volume, strong-coupling, and continuum Hamiltonian gaps.
9. Compare claims with primary literature and the current problem status.
10. Run countermodels and inspect the machine-checkable finite core.

## Claim Levels

- `C0`: concepts or definitions only.
- `C1`: finite or computational calibration.
- `C2`: rigorous restricted-model theorem.
- `C3`: conditional continuum or transfer theorem.
- `C4`: regulator-specific nonperturbative construction with uniform limits incomplete.
- `C5`: continuum construction and gap for a restricted gauge-group or axiom set.
- `C6`: full Clay-level theorem.

## Output Contract

Return a pass/fail matrix, dependency graph, parameter and limit ledgers, first unproved implication, strongest defensible claim level, and required downgrade language. Any missing basin-entry, continuum-existence, OS, density, or universality theorem blocks `C6`.
