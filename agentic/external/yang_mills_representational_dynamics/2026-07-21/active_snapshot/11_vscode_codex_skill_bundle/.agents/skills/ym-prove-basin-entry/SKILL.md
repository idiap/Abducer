---
name: ym-prove-basin-entry
description: Attempt and conservatively assess the frontier theorem that four-dimensional pure Yang--Mills enters a noncircular infrared rigidity basin along a controlled renormalization trajectory. Use when perturbative asymptotic freedom must be connected to finite physical-scale nonperturbative control without assuming the mass gap.
---

# Prove Basin Entry

## Frontier Target

Given a regulator approaching four-dimensional pure Yang--Mills, prove that after finitely many controlled RG steps the complete effective theory lies in an independently defined rigidity basin at a finite physical scale `ell_*`.

## Required Chain

1. Construct the weak-coupling ultraviolet trajectory with quantitative errors.
2. Control all generated relevant, marginal, irrelevant, and quasilocal interactions uniformly in volume.
3. Extend small-field control to the full measure using summable large-field and polymer estimates.
4. Treat global gauge-orbit and topological sectors.
5. Iterate until a finite physical scale without losing positivity, locality, or observable reconstruction.
6. Verify every clause of the basin predicate using estimates independent of the desired gap.
7. Prove that the entry constants are uniform as cutoff is removed and volume grows.

## Epistemic Rules

Asymptotic freedom alone does not imply basin entry. Numerical evidence, formal RG flows, perturbative series, strong-coupling lattice expansions, or an assumed confinement scale do not close this theorem. Never insert dimensional transmutation as a positive mass gap without a nonperturbative inequality.

## Progressive Outputs

Report the strongest achieved level:

- a finite-step regulated estimate;
- small-field basin entry;
- full-measure finite-volume entry;
- volume-uniform regulated entry;
- cutoff-uniform physical entry;
- full continuum-ready entry.

For the first failed implication, produce the exact missing inequality, its parameter dependencies, known obstructions, and candidate proof mechanisms. A precise blocker is a valid result; an unstated assumption is not.

## Stop Condition

Do not claim the Clay theorem unless this skill's conclusion is combined with continuum construction, OS reconstruction, observable completeness, and rigidity transfer. If the full four-dimensional entry theorem is not proved, mark it open explicitly.
