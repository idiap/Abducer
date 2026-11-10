# H3 self-contained research todos

The checkboxes distinguish completed stream analysis from new mathematical
work.  A later stage may implement these tasks, but no unchecked item is
claimed in the current report.

## Phase A — Freeze H3 and correct inherited conventions

- [x] **H3-A1 — Freeze the operator order.**  Declare
  `R_l = C_6 O_l S_l d_1` and prohibit import of the superseded Stage 44
  zero-mode convention.
- [x] **H3-A2 — Freeze the spill form.**  Define `R_P`, `U(P)`, `B_P`,
  `h_P`, the induced metric, and the exact nullity identity.
- [x] **H3-A3 — Separate evidence levels.**  Record the exact C2 one-star
  theorem, exact conditional C2 budget, and C1 multi-star signal separately.
- [x] **H3-A4 — Freeze exclusions.**  Exclude nonlinear measure comparison,
  cutoff-uniformity, RG iteration, continuum existence, OS reconstruction,
  confinement, and a Hamiltonian mass gap.
- [x] **H3-A5 — State the first open implication.**  Identify the missing
  step as finite cancellation to an exact growing-polymer boundary law with
  repair coverage.

## Phase B — Build an exact multi-star certificate

- [ ] **H3-B1 — Generalize the Paper 05 exact backend.**  Accept an arbitrary
  oriented rooted-link polymer and build rational `R_P`, `B_P`, coordinate
  metric, and KKT system.
- [ ] **H3-B2 — Certify ranks over the rationals.**  Compute
  `rank(R_P)`, `rank(B_P)`, and `rank([R_P;B_P])`; derive the nullity without
  eigenvalue tolerances.
- [ ] **H3-B3 — Produce exact minimum-cost witnesses.**  Use floating pivoting
  only to locate a nonsingular minor; solve by Bareiss elimination and verify
  every KKT equation by rational substitution.
- [ ] **H3-B4 — Factor generalized characteristic polynomials.**  Store exact
  polynomials over `Q`; allow algebraic eigenvalues instead of assuming all
  spectra are rational.
- [ ] **H3-B5 — Certify the adjacent-pair spectrum.**  Test the numerical
  candidates `(16/19)^3`, `(5/4)^2`, `(3/2)^3`, `(24/11)^2`.
- [ ] **H3-B6 — Certify the central-four system.**  Prove or disprove exact
  nullity four and identify the algebraic positive factors.
- [ ] **H3-B7 — Certify the eight-link system.**  Prove or disprove nullity
  seven and the candidates `(3/4)^6`, `(12/11)^8`, `(10/7)^3`.
- [ ] **H3-B8 — Add orientation-hostile tests.**  Compare the correct operator
  with center-then-orient and sign-erased variants; require the exact
  one-star regression theorem.
- [ ] **H3-B9 — Add automorphism tests.**  Verify spectra and exact witnesses
  under oriented cubical symmetries and link/plaquette basis reversals.
- [ ] **H3-B10 — Emit a canonical certificate.**  Record incidence hashes,
  selected supports, metrics, ranks, KKT witnesses, factorizations, and scope.

**Gate B:** stop if the exact computation removes the four- or eight-link
nullspaces.  Reclassify them as numerical artifacts.

## Phase C — Run the growing-polymer spectral atlas

- [ ] **H3-C1 — Implement scalable sparse operators.**  Separate discovery
  arithmetic from exact certification and avoid forming dense pseudoinverses.
- [ ] **H3-C2 — Define polymer boundary.**  Freeze link boundary, plaquette
  boundary, star-union boundary, and ambient-boundary contact; select the one
  used by the theorem before fitting scaling laws.
- [ ] **H3-C3 — Generate compact open polymers.**  Include rectangular boxes,
  slabs, and approximately cubical Følner sequences over increasing sizes.
- [ ] **H3-C4 — Generate adversarial shapes.**  Include chains, branched
  trees, combs, holes, and boundary-touching polymers.
- [ ] **H3-C5 — Generate periodic and winding families.**  Track harmonic
  modes and center/integer flux separately from local exact modes.
- [ ] **H3-C6 — Record the spectral ledger.**  For each polymer store
  `|P|`, `|U(P)|`, `|boundary P|`, ranks, nullity, positive rank,
  `lambda_min+`, `lambda_max`, trace, and topology.
- [ ] **H3-C7 — Fit only predeclared scaling hypotheses.**  Test
  `r_P-z_P=O(|boundary P|)`, zero-mode density, bounded positive spectrum,
  and trace/volume behavior with finite-size uncertainty.
- [ ] **H3-C8 — Exact-certify representative sizes.**  Every qualitative
  spectral transition discovered numerically must have an exact witness.

**Gate C:** proceed only if compact polymers display a stable boundary-sized
positive sector or an explicit trace factorization.  A few additional zero
modes without a scaling law do not pass.

## Phase D — Explain the spectrum and prove a linear boundary law

- [ ] **H3-D1 — Identify the relative complex.**  Express
  `im(d_1) intersect C^2(U(P))` using relative cochains and record the exact
  role of Bianchi constraints.
- [ ] **H3-D2 — Separate physical kernels.**  Quotient gauge redundancy and
  distinguish compact exact curvature, harmonic modes, winding modes, and
  forbidden topological-sector changes.
- [ ] **H3-D3 — Prove a nullity formula.**  Relate `dim ker(h_P)` to relative
  Betti numbers plus explicitly counted compatibility constraints.
- [ ] **H3-D4 — Construct a boundary trace.**  Define `T_boundary` and prove
  that equal boundary trace gives equal external minimum, or bound the
  resulting defect.
- [ ] **H3-D5 — Construct a controlled right inverse.**  Produce `J_P` with
  `R_P J_P y = delta y` and a uniform boundary-energy estimate.
- [ ] **H3-D6 — Prove a discrete extension inequality.**  Control the norm of
  the lift and its boundary curvature uniformly over the allowed shape class.
- [ ] **H3-D7 — Run localized and oscillatory countermodes.**  Search for
  small boundary trace with order-one spill and for modes whose constants
  deteriorate with aspect ratio.
- [ ] **H3-D8 — State the sharp theorem.**  Specify shape, topology, boundary,
  metric, coverage subspace, and every size quantifier.

**Gate D:** if the strong boundary law fails, test a weaker special-channel
theorem.  Do not average away a worst-mode obstruction needed by the bad-event
repair.

## Phase E — Prove repair relevance and complete the linear budget

- [ ] **H3-E1 — Freeze the nonlinear bad predicate at tangent level.**  Map
  the declared dispersion event to a cone `Y_P^bad` without using clustering
  or a desired gap.
- [ ] **H3-E2 — Compute coverage constants.**  Bound the principal angles
  between `Y_P^bad` and the zero/low-spill repair sector.
- [ ] **H3-E3 — Design the contraction.**  Define the repaired component,
  unchanged component, and boundary correction so compatibility is exact.
- [ ] **H3-E4 — Charge every plaquette.**  Include selected-star action,
  internal-unselected action, external action, and cross terms with arbitrary
  pre-existing curvature.
- [ ] **H3-E5 — Compute the true tangent Jacobian.**  Work on independent link
  variables after quotienting gauge fibers; do not multiply duplicated
  star-coordinate determinants.
- [ ] **H3-E6 — Derive a polymer free-energy inequality.**  Prove a net lower
  bound of the form `gamma |P| - C_boundary |boundary P| - C_0`.
- [ ] **H3-E7 — Beat connected-polymer entropy.**  Insert the exact graph
  counting constant and require a strict, not critical, inequality.
- [ ] **H3-E8 — Recompute the Stage 45 budget.**  Use the corrected multi-star
  operator, true repaired rank, and all logarithmic losses.

**Gate E:** a growing zero-spill sector is insufficient if coverage vanishes,
the Jacobian consumes the action gain, or the net gain does not beat polymer
entropy.

## Phase F — Lift to finite `SU(2)` geometry

- [ ] **H3-F1 — Define a finite link map.**  Integrate the tangent repair in
  a covariant exponential/Karcher atlas and state its domain.
- [ ] **H3-F2 — Prove gauge covariance.**  Verify boundary gauge action and
  reflection-plane compatibility exactly.
- [ ] **H3-F3 — Control noncommutative remainders.**  Bound BCH, curvature,
  and transport errors with their polymer-size dependence.
- [ ] **H3-F4 — Prove chart coverage.**  Include the two-center atlas,
  cut-locus/orbit exceptions, and boundary-history-uniform exceptional mass.
- [ ] **H3-F5 — Control topology.**  Preserve or explicitly update center
  cocycles, integer flux lifts, transition data, and winding sectors.
- [ ] **H3-F6 — Prove injectivity or bounded multiplicity.**  State the
  inverse domain and count every preimage.
- [ ] **H3-F7 — Prove the full Haar/Jacobian bound.**  Include coordinate,
  gauge-fiber, and overlap factors uniformly in polymer size.
- [ ] **H3-F8 — Compare finite and tangent energy.**  Establish a remainder
  small enough to preserve the strict free-energy margin.

**Gate F:** failure of a uniform finite map leaves H3 as a linearized
finite-complex theorem only.

## Phase G — Insert H3 into the normalized retained-state programme

- [ ] **H3-G1 — Type the retained boundary state.**  Include all continuous,
  center, cut/orbit, and integer-topology data needed for conditional
  sufficiency.
- [ ] **H3-G2 — Prove a normalized good-channel ratio.**  Control conditional
  partition functions, not only pointwise action changes.
- [ ] **H3-G3 — Define the H3 bad subkernel.**  Record exploration order,
  root state, polymer state, and the exact event being suppressed.
- [ ] **H3-G4 — Combine with positive weights.**  Establish `Q V <= q V` and
  a volume-uniform root `V` moment without deriving `V` from a desired gap.
- [ ] **H3-G5 — Prove strict cluster summability.**  Include polymer
  multiplicity and require the strict package threshold.
- [ ] **H3-G6 — Audit scale uniformity.**  Express all rates in physical units
  and quantify volume, cutoff, heat-time, and boundary-history dependence.

**Gate G:** only after these tasks may H3 be called a physical one-scale
defect-transfer mechanism.

## Phase H — Downstream work, explicitly conditional

- [ ] **H3-H1 — Prove basin entry and repeated RG compatibility.**  Preserve
  gauge invariance, locality, reflection positivity, and topology at every
  step.
- [ ] **H3-H2 — Construct the continuum limit.**  Prove tightness,
  consistency, nontriviality, and identification with pure Yang--Mills.
- [ ] **H3-H3 — Transfer decay through OS reconstruction.**  Establish
  uniform physical-time estimates on a dense vacuum-orthogonal observable
  core.
- [ ] **H3-H4 — Exclude hidden sectors.**  Prove observable density, vacuum
  uniqueness as required, and nonempty nonvacuum spectrum.
- [ ] **H3-H5 — Run a final Clay audit.**  Match every quantifier and compact
  simple gauge-group requirement before making any mass-gap claim.

These downstream items are not part of the current H3 evidence.  They are
included to prevent a finite boundary-law theorem from being mistaken for a
continuum spectral result.
