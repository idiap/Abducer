# Required fixes from the Stage 68--75 audit

## P0: repair or downgrade the H7 two-chart reconstruction claim

- `reconstruct_overlap_coordinate(atom, chart)` currently ignores `chart` and
  returns the same stored quaternion for both calls.
- Either implement distinct plus/minus chart-coordinate representatives and
  reconstruct each through the declared chart map, including the group-law
  identity on the overlap, or downgrade H7-F5 to “agreement with a shared
  predeclared global label.”
- Add a hostile test that perturbs or reverses one chart map and must fail.

## P1: complete the H2 additive-rate hypotheses

- In H2-AD.2 explicitly assume both
  \(\prod_{j<N}q_j\le C e^{-mL_N}\) for the homogeneous term and the stated
  post-injection tail estimates.
- Keep the exponentially weighted error budget as the separate condition for
  the injected terms.
- Add a countertest where all injected errors vanish but the homogeneous
  product has no rate; the present corollary must not certify decay there.

## P1: align exactness language with arithmetic

- Stages 68 and 69: say “algebraically exact; numerically
  tolerance-certified,” or replace core calculations with rational/interval
  arithmetic.
- Stage 72: remove “represented exactly” from floating-point KL and
  partition-ratio computations.  Preserve “exact theorem” only for the
  mathematical identity and provide a proof separate from examples.
- For the Stage 72 common-bit family, store logarithmic masses or use arbitrary
  precision so `full_support` remains true for the declared asymptotic family.

## P2: certify cross-stage provenance

- Stage 73 should derive its balanced-star matrix from the Stage 70/Paper 05
  operator or verify a canonical source hash and typed projection map.
- Until then, phrase the result as an exact theorem for the displayed rational
  matrix, not an independently reproduced geometric certificate.
- Stage 75 should record that the Stage 19 value of `q` is the exact rational
  encoded by the displayed decimal, rather than an exact recovery of an
  independently defined real number.

## P2: strengthen universal-theorem tests

- Add property-based rational tests for Stage 68's same-measure identity and
  Stage 69's two-sided ceiling theorem, including nearly singular admissible
  inputs handled by interval or exact arithmetic.
- Add an independent proof/checker for Stage 72 data processing rather than
  treating example certificates as a general implementation proof.
- Add a stored-output equality regression to Stage 75 after JSON
  normalization of tuples and fractions.

## Non-negotiable frontier language

Do not infer a temporal or continuum mass gap from any weighted defect,
partition-ratio, atlas, topology, or refinement certificate until a
same-measure observability/coercivity theorem controls every nonvacuum
temporal mode.  No current stage supplies that implication.
