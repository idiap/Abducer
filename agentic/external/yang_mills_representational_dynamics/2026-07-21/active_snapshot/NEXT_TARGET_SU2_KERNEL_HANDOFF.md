# Continuation handoff: physical `SU(2)` kernel and spectral observability

Date: 21 July 2026

## Frozen objective

Construct, first at the smallest nontrivial finite regulator, a normalized
nonlinear `SU(2)` retained-state conditional kernel from the actual lattice
Yang--Mills measure.  The Gibbs conditional law, retained variables, temporal
transfer, vacuum/Doob transform, bad event, and observable probes must belong
to this one measure.  Immediately afterward, prove or falsify a quantitative
same-measure inequality that sees every nonvacuum temporal eigenspace,
including every multiplicity direction.

This is a two-gate target.  A successful kernel without full-spectrum
observability does not establish a gap; Stage 68 gives an exact counterfamily.

## Gate A: normalized nonlinear retained kernel

Freeze explicitly:

1. a finite four-dimensional lattice region, time reflection, boundary/collar,
   gauge group `SU(2)`, and Wilson or heat-kernel action;
2. the actual Gibbs measure and its boundary disintegration;
3. a gauge-invariant retained state containing the interface, topology, and
   observable data needed for gluing;
4. the block map, conditional numerator, common normalizer, admissible
   positive-mass boundary histories, and all chart transitions;
5. a Markov or sub-Markov retained kernel and a named bad-event mask;
6. the temporal transfer operator derived from the same measure.

The kernel certificate must prove normalization, positivity, gauge covariance
or quotient invariance, compatibility with the chosen reflection, and exact
dependence on boundary condition, volume, and lattice spacing.  It must fail
closed at zero conditional or chart mass.  No transition probability, vacuum
weight, or gap may be inserted independently.

## Gate B: same-measure full-spectrum observability

Let `P` be the reversible Doob kernel or normalized temporal transfer on the
finite physical Hilbert space, with vacuum projector `Pi_0`.  Choose a finite
gauge-invariant defect/probe family `D_alpha` derived from Gate A.  The first
finite target is a quantitative estimate of the form

```text
||(I-Pi_0) f||_pi^2
    <= C_obs sum_alpha ||D_alpha f||_pi^2
```

on the complete vacuum-orthogonal space, or an equivalent eigenspace Gram
lower bound.  For every nonvacuum eigenspace `E_lambda`, including degenerate
ones, the restricted probe matrix must have full rank with an explicit
smallest singular-value bound.  A counterexample is also a valid exit if it
identifies the missing physical observable or retained variable.

After observability, decay or coercivity must be proved on the same probe
family using the same measure.  Rates must be converted to physical time;
positivity at each fixed cutoff is insufficient.

## Execution order and skills

Use the exported skills in this order:

1. `ym-freeze-clay-target` -- freeze quantifiers and nonclaims.
2. `ym-build-observable-core` -- name the separating gauge-invariant probes.
3. `ym-design-regulator-atlas` -- construct the retained boundary atlas and
   fail-closed normalization domains.
4. `ym-build-gauge-covariant-rg` -- type the block map and conditional kernel.
5. `ym-prove-conditional-partition-ratio` -- normalize the actual bad/good
   conditional event.
6. `ym-prove-state-weighted-defect-transfer` -- calibrate the same-measure
   Lyapunov or vacuum weight without importing a gap.
7. `ym-define-relational-rigidity` and `ym-prove-rigidity-transfer` -- state
   the representation-invariant observability/coercivity witness.
8. `ym-mechanize-proof-core` -- check normalization, exact finite spectra,
   eigenspace ranks, multiplicities, and interval bounds.
9. `ym-calibrate-restricted-models` -- run hostile finite fixtures without
   promoting numerical evidence to a physical theorem.
10. `ym-audit-frontier` -- enforce the C2/C3 ceiling and locate the first
    remaining implication.

The complete portable implementations are under
`11_vscode_codex_skill_bundle/.agents/skills/`.

## P0 implementation TODOs

- [ ] Select the smallest nonlinear lattice region with a nontrivial temporal
  slice and at least one retained interface degree of freedom.
- [ ] Write the exact finite-volume measure and boundary disintegration.
- [ ] Define intrinsic gauge-orbit representatives or a quotient-valued
  retained state; record all exceptional chart sets.
- [ ] Derive every conditional-kernel row from the same Gibbs numerator and
  common partition function.
- [ ] Prove row normalization, positivity, gauge invariance, and reflection
  compatibility for every positive-mass boundary history.
- [ ] Derive the temporal transfer and Perron/Doob data from this measure.
- [ ] Define the physical bad event and masked subkernel without an independent
  toy mask.
- [ ] Enumerate a product-closed, gauge-invariant probe family and compute its
  action on every nonvacuum temporal eigenspace.
- [ ] Certify full multiplicity-sensitive rank and a quantitative Gram lower
  bound, or emit a minimal hidden-mode counterexample.
- [ ] Attempt the observability inequality and a same-measure decay estimate;
  track physical-time conversion explicitly.
- [ ] Add hostile tests for zero chart mass, normalization amplification,
  gauge-copy dependence, omitted observables, hidden eigenvalue multiplicity,
  gap-closing families, and cutoff-to-physical-time collapse.
- [ ] Emit canonical results JSON, theorem dependencies, proof ledger, open
  implications, and an independent frontier audit.

## Acceptance and stop conditions

Gate A passes only if the normalized kernel and temporal transfer are derived
from one declared nonlinear `SU(2)` lattice measure.  Gate B passes only if
every nonvacuum eigenspace is quantitatively visible to the declared physical
probe family.  Passing both gates at one finite regulator remains a C2 result.

Stop and report an obstruction if normalization fails for an admissible
positive-mass history, the retained state is not closed under gluing, a probe
misses any multiplicity direction, or the physical-time constant collapses.
Do not claim basin entry, continuum existence, OS reconstruction, a uniform
Hamiltonian gap, or the Clay result until the separate volume-, boundary-,
cutoff-, continuum-, and theory-identity gates are proved.

## Starting evidence

- `68_h1_same_measure_calibration/`: same-measure identity and decisive
  gap-closing counterfamily.
- `72_h5_information_partition_ratio/`: normalized bad/good ratio and entropy
  obstructions.
- `74_h7_normalized_atlas_gluing/`: normalized finite chart-gluing template.
- `76_h9_dense_core_spectral/`: multiplicity-sensitive dense-core criterion.
- `77_h10_observable_recovery/`: finite orbit separation and recovery model.
- `78_hypothesis_run_audit/`: conservative claim audit.
- `79_hypothesis_execution_synthesis/`: cross-stream dependency graph and
  reward-ranked continuation.

