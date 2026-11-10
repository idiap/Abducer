---
name: ym-build-gauge-covariant-rg
description: Design and audit renormalization-group transformations for constructive Yang--Mills theory that respect gauge-invariant observables and track locality, positivity, running couplings, and reconstruction data. Use when a proof needs a typed scale transformation rather than a formal perturbative beta function alone.
---

# Build Gauge-Covariant RG

## Goal

Construct a scale-change map together with certificates for the physical structures it preserves, approximates, or deliberately forgets. Regard the effective action, observable transport, and state transport as one coupled object.

## Construction Workflow

1. Specify the fine and coarse configuration spaces, gauge groups, boundary conditions, and physical observable algebras.
2. Define the blocking kernel or conditional expectation and prove gauge covariance or formulate it directly on gauge orbits.
3. Derive the coarse effective measure and the dual transport of observables. Do not track the action while leaving observables implicit.
4. Parameterize relevant, marginal, irrelevant, and nonlocal terms with explicit norms and scale factors.
5. Track the running coupling in a declared scheme; separate perturbative control from nonperturbative estimates.
6. Prove locality or quasilocality bounds for the effective interaction uniformly in volume.
7. Track reflection positivity. If a block map does not preserve it, supply a later recovery theorem or mark the OS bridge broken.
8. State reconstruction or comparison maps and quantitative errors for every lossy step.
9. Prove composition laws and error accumulation across many RG steps.

## Minimum Certificate

Every RG morphism must report:

- gauge covariance or orbit-space well-definedness;
- state and observable transport;
- normalization of physical length and energy;
- locality or quasilocality norm;
- positivity status;
- volume dependence;
- coupling flow and remainder bounds;
- reconstruction data and approximation error.

## Failure Modes

- Gauge fixing that ignores Gribov or global orbit information.
- A perturbative flow with no control of the full measure.
- Local estimates restricted to a small-field chart without an exceptional-set theorem.
- Scale-by-scale constants whose product diverges.
- Loss of reflection positivity with no recovery argument.
- Blocking that erases the observables needed for spectral completeness.

## Output Contract

Return the typed RG map, its preservation certificate, effective-interaction norms, recursion inequalities, parameter registry, and unresolved obligations. Label any basin-entry conclusion conditional until large fields, topology, and volume-uniform iteration are controlled.
