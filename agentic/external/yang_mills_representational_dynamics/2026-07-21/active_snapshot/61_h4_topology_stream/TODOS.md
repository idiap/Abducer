# H4 self-contained TODOs

## Completed in this stream

- [x] Audit Stages 39, 47, 48, and the Stage 52 H4 probe.
- [x] Re-run all 56 inherited tests relevant to the stream.
- [x] Polarize the four-dimensional Pfaffian charge and write its integral
  pairing matrix \(J\).
- [x] Verify \(J^2=I\), \(\det J=-1\), and signature \((3,3)\).
- [x] Prove the contextual-minimality theorem: arbitrary-context charge
  prediction forces an injective retained statistic on \(\mathbb Z^6\).
- [x] Give an associative graded composition law for center, flux, charge, and
  pairing covector.
- [x] Preserve the Stage 52 common-context collision as a regression witness.
- [x] Prove by a two-boundary-channel counterexample that scalar sector weights
  are not sufficient for gluing.
- [x] Specify finite algorithms for carrier refinement and boundary-resolved
  sector-kernel construction.
- [x] Freeze the claim ceiling at `C2` and state every missing physical layer.

## P0: freeze the physical topology problem

- [ ] Choose the first target gauge theory and global form (`SU(2)`, `SO(3)`,
  or another compact simple group); do not mix their sector classifications.
- [ ] Freeze strict-periodic versus twisted boundary conditions and identify
  exactly which center-flux labels are present.
- [ ] Fix the finite block complex, orientation, reflection plane, block map,
  admissibility condition, and external boundary state.
- [ ] State the regulator-specific nonabelian topological classification
  theorem to be used, including all boundary-trivialization hypotheses.
- [ ] Define a gauge-invariant exceptional event for configurations where the
  topological chart or admissibility condition fails.

**Exit criterion:** one typed definition of the one-block topology carrier,
with no ambiguity about group, bundle, boundary, orientation, or exceptions.

## P1: implement the integral finite-cell baseline

- [ ] Build integral coboundary matrices for the chosen block and verify
  consecutive compositions exactly.
- [ ] Compute \(H^2(K;\mathbb Z)\) and relative \(H^2(K,\partial K;\mathbb Z)\)
  by Smith normal form, including torsion.
- [ ] Compute the cellular cup/intersection pairing and test orientation
  reversal.
- [ ] Implement canonical cocycle representatives and mod-two reduction.
- [ ] Implement the induced block chain map and prove naturality on
  cohomology.
- [ ] Implement context-signature refinement; require an explicit witness for
  every failed merge.
- [ ] Check that direct two-block classification equals composed one-block
  classification on an exhaustive bounded catalog.

**Exit criterion:** a machine-checkable finite carrier or an explicit
counterexample showing which additional boundary datum is necessary.

## P2: construct the nonabelian one-block carrier

- [ ] Implement the selected admissible-lattice nonabelian charge with exact
  convention and normalization tests on known representatives.
- [ ] Relate center/twist data, integral charge, and boundary transgression
  without assuming that the embedded-abelian formula is complete.
- [ ] Prove invariance under interior gauge transformations and specify the
  action of boundary gauge transformations.
- [ ] Prove stability of the carrier under the one-block map on the admissible
  set.
- [ ] Quantify the mass of the exceptional complement rather than deleting it.
- [ ] Test instanton-like fields, torons/global holonomy, center twists,
  orientation reversals, and near-admissibility-boundary configurations.

**Exit criterion:** an exhaustive, gauge-invariant one-block classification
with a declared and quantitatively controlled exceptional set.

## P3: replace scalar sector weights by a positive kernel

- [ ] Define the boundary state space and prove it is sufficient for gluing.
- [ ] Define every unnormalized boundary/topology sector integral and its
  common normalization denominator.
- [ ] Prove positivity and rule out zero denominators on the retained domain.
- [ ] Produce certified quadrature or analytic enclosures for all finite kernel
  entries.
- [ ] Verify row normalization and sector exhaustiveness.
- [ ] Compare composed one-block kernels with a direct two-block integral.
- [ ] Apply automatic partition refinement when retained rows differ.
- [ ] Preserve reflection and gauge covariance through the kernel interface.

**Exit criterion:** a normalized, boundary-resolved positive kernel whose
composition law passes an independent two-block check.

## P4: prove a topology-channel bound

- [ ] Choose a topology size functional \(T(\tau)\) that controls every
  retained integer direction and is stable under composition.
- [ ] Choose a positive Lyapunov weight \(V\) without assuming the desired
  suppression.
- [ ] Prove a one-block exponential-moment enclosure uniformly over declared
  boundary states.
- [ ] Separate energetic suppression, fluctuation entropy, boundary entropy,
  and exceptional-set contributions.
- [ ] Fit the normalized topology contribution inside the multichannel defect
  budget, with explicit slack.
- [ ] Repeat the calculation after one additional blocking step.

**Exit criterion:** a strict normalized topology-channel ceiling for two
successive scales, with every constant and supremum explicit.

## P5: uniformity and transfer to the main programme

- [ ] Prove constants uniform in finite volume and all positive-mass retained
  histories.
- [ ] Prove summability of exceptional topology/chart events over blocks and
  scales.
- [ ] Establish cutoff control along the tuned trajectory in physical units.
- [ ] Audit compatibility with locality, reflection positivity, and the
  observable core.
- [ ] Only after these pass, insert the topology kernel into basin-entry and
  repeated-RG theorems.

**Exit criterion:** a regulator-specific nonperturbative topology module with
uniform bounds.  This still does not by itself establish continuum existence
or a Hamiltonian mass gap.

## Mandatory stop conditions

- [ ] Stop if topology is defined only after an unjustified global gauge
  fixing.
- [ ] Stop if the block map can cross the admissibility boundary without a
  quantitative exceptional-set term.
- [ ] Stop if a minimum action is substituted for a normalized partition
  ratio.
- [ ] Stop if scalar sector weights are composed without boundary response.
- [ ] Stop if center twist, embedded-abelian flux, and nonabelian second Chern
  data are treated as interchangeable.
- [ ] Stop if any bound depends silently on volume, cutoff, scale, or retained
  history.

