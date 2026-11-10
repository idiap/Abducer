# H8 next-step TODOs

## Completed in Stage 75

- [x] Replace rounded NumPy signatures by exact `Fraction` arithmetic.
- [x] Reproduce the two-round Stage 52 refinement history.
- [x] Prove/check monotonicity, finite termination, stability, and coarsest
  stable refinement.
- [x] Emit and adversarially verify exact split witnesses.
- [x] Add Stage 18 moment-only, Stage 19 weighted-two-state, and Stage 24
  unequal-persistence regressions.
- [x] Check state-permutation equivariance and equal-channel symmetry.
- [x] Exhibit a delayed-distinction family saturating the termination bound.
- [x] Keep the physical SU(2), uniformity, continuum, and mass-gap claims open.

## Target H8.1: physical finite table

- [ ] Freeze one finite block geometry, retained collar, and gauge-invariant
  seed labels.
- [ ] Define every transition numerator and the common conditional partition
  denominator before numerical evaluation.
- [ ] Prove positivity and row normalization uniformly over the retained
  boundary condition.
- [ ] Export the resulting entries as rigorous rational or interval
  enclosures accepted by the refinement checker.
- [ ] Record which initial labels are physically observable; do not seed the
  algorithm with hindsight labels.

## Target H8.2: interval refinement

- [ ] Generalize exact equality to disjoint certified intervals while keeping
  an explicit unresolved relation when intervals overlap.
- [ ] Prove that every interval-certified split remains valid under enclosure
  tightening.
- [ ] Add a fail-closed branch: overlapping intervals may not be treated as
  equality or inequality.
- [ ] Emit the numerical precision needed for each physical split witness.

## Target H8.3: representation-size control

- [ ] Quotient the physical table by exact gauge, lattice, center, and channel
  symmetries before refinement.
- [ ] Bound the number of distinct stable signatures as the collar and volume
  grow.
- [ ] Search explicitly for delayed-distinction chains in the physical table.
- [ ] If uniform boundedness fails, identify a compressed sufficient statistic
  and prove that it preserves the weighted defect inequality.

## Target H8.4: weighted-kernel composition

- [ ] Attach the Stage 19/24 Lyapunov weight to every stable H8 cell.
- [ ] Prove \(QV\le qV\) on the refined physical kernel with strict cluster
  margin.
- [ ] Prove a cutoff-uniform root moment for \(V\).
- [ ] Check that refinement and coarse-graining do not increase the certified
  weighted ceiling.

## Target H8.5: continuum handoff

- [ ] Compose the physical finite certificate with basin entry and
  physical-length scaling.
- [ ] Prove continuum tightness and Osterwalder--Schrader hypotheses
  independently of the finite refinement theorem.
- [ ] Only after those steps, test whether temporal spectral decay follows.
