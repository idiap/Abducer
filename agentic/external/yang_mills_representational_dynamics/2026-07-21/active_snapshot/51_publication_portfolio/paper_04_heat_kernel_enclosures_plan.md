# P4 publication plan: explicit `SU(2)` heat-kernel enclosures

## 1. Frozen identity

Working title:

> **Explicit Log-Derivative and Tail Enclosures for the `SU(2)` Heat Kernel**

Publication type: technical mathematical-physics or analysis note.

Current decision: `HOLD/GO`. Execute the analytic work and novelty audit, then
publish independently only if the standalone gate in Section 8 passes.
Otherwise merge the results into P2 as a major analytic appendix.

Current defensible level: `C1` executable calibrations plus local analytic
`C2` claims whose numerical constants need rigorous certification.

Core thesis: a convention-complete image-series analysis can provide explicit,
uniform, computer-verifiable enclosures for the `SU(2)` heat kernel, its log
derivatives, radial Hessian, higher derivatives, and Haar-normalized tails on
the domains needed by nonlinear lattice-gauge estimates.

Reusable workflow: `ym-draft-heat-kernel-enclosures`, with
`ym-mechanize-proof-core`, `ym-calibrate-restricted-models`, and
`ym-audit-frontier`.

## 2. Minimum theorem contract

The technical note must state a theorem family rather than a table of sampled
constants. At minimum it must provide:

1. explicit metric, Haar, class-angle, Laplacian, and heat-time conventions;
2. character-series and Poisson/image representations and their equivalence;
3. analytic truncation bounds for the chosen representation;
4. a positive lower enclosure for the kernel before log differentiation;
5. uniform first-, second-, and third-log-derivative enclosures on a declared
   interval, including the identity limit;
6. radial/tangential Hessian eigenvalue enclosures for the heat-kernel action;
7. a Haar-normalized tail theorem with explicit numerator and denominator
   errors;
8. small-time asymptotics with quantitative, finite-`t` remainders;
9. a certificate format and independently runnable verifier.

For standalone publication, add at least one of: arbitrary derivative-order
bounds, materially sharper constants than the literature, a useful `SU(N)` or
compact-group extension, or closure of a recognized constructive estimate.

## 3. Novelty hypothesis and known baseline

Heat kernels on compact Lie groups and the heat-kernel lattice action are
classical. Menotti and Onofri introduced the lattice action
([DOI](https://doi.org/10.1016/0550-3213(81)90560-5)). Gaussian bounds,
small-time asymptotics, derivative estimates, character expansions, and image
formulas have substantial literatures.

Therefore “we computed explicit constants” is not enough. The provisional
novelty lies in a reusable theorem family with rigorous uniform enclosures
tailored to nonlinear marginalization. P4-L1--P4-L6 decide whether that is a
paper or an appendix.

## 4. Source corpus inside this package

Primary sources:

- `07_su2_heat_kernel_initializer/su2_heat_kernel_initializer_theorem.tex`
- `07_su2_heat_kernel_initializer/su2_heat_kernel_initializer.py`
- `07_su2_heat_kernel_initializer/test_su2_heat_kernel_initializer.py`
- `07_su2_heat_kernel_initializer/su2_heat_kernel_calibration.json`
- `07_su2_heat_kernel_initializer/theorem_dependencies_heat_kernel.json`

Supporting sources:

- `03_heat_kernel_basin_entry/heat_kernel_basin_entry_attack.tex`
- `08_su2_nonlinear_block_geometry/su2_nonlinear_block_geometry_theorem.tex`
- `09_su2_uv_overlap/su2_uv_overlap_theorem.tex`
- `15_nonasymptotic_good_collar/nonasymptotic_good_collar_theorem.tex`
- `27_su2_haar_entropy/su2_haar_entropy_theorem.tex`
- `28_coherent_partition_optimizer/coherent_partition_optimizer_theorem.tex`
- `41_nonlinear_dispersion_geometry/nonlinear_dispersion_geometry_theorem.tex`

The nonlinear block material supplies applications, not assumptions for the
heat-kernel theorem.

## 5. Manuscript architecture

1. Conventions and main enclosure theorems.
2. Character and image formulas on `SU(2)`.
3. Principal-image isolation and analytic remainders.
4. Kernel lower bounds and log-derivative calculus.
5. Hessian and higher-derivative enclosures.
6. Identity and cut-locus regimes.
7. Haar-normalized tail bounds.
8. Interval certification and independent verification.
9. Comparison with existing estimates.
10. Lattice-gauge corollary and limitations.

Target length: 20--30 pages plus code/certificate supplement if standalone;
12--18 pages as a P2 appendix.

## 6. Self-contained todo graph

All dependencies below are internal to P4.

### A. Freeze conventions and exact formulas

- [x] **P4-A1 — Declare geometry and normalization.** Input: Stage 07. Action:
  define `SU(2)` metric radius, class angle, Haar probability, radial measure,
  Laplacian sign, generator factor, and time. Acceptance: a reader can convert
  to common alternative conventions. Output: convention table.
- [x] **P4-A2 — Derive the character expansion.** Input: representation theory
  of `SU(2)`. Acceptance: coefficients and eigenvalues follow the declared
  generator. Output: proposition.
- [x] **P4-A3 — Derive the image formula.** Input: P4-A2 or a cited Poisson
  summation theorem. Acceptance: constants, sine denominator, image signs, and
  endpoint limits are exact. Output: proposition.
- [x] **P4-A4 — Prove formula equivalence.** Inputs: P4-A2, P4-A3. Acceptance:
  not based on numerical agreement. Output: theorem or authoritative citation
  with convention conversion.
- [x] **P4-A5 — Partition the domain.** Action: choose identity, interior,
  transition, and cut-locus regions suited to stable formulas. Acceptance:
  closed intervals cover `[0,pi]` with verified overlaps. Output: domain map.

### B. Prove analytic remainder bounds

- [x] **P4-B1 — Isolate the principal image.** Input: P4-A3. Action: factor its
  exponential and polynomial prefactor. Acceptance: signs and zeros are
  controlled on each region. Output: lemma.
- [x] **P4-B2 — Bound image tails.** Input: P4-B1. Action: dominate all omitted
  images by explicit geometric/Gaussian series. Acceptance: bound remains valid
  after required differentiations. Output: tail theorem.
- [x] **P4-B3 — Bound differentiated tails.** Input: P4-B2. Action: derive
  first through third derivative remainders, or general order `k` if feasible.
  Acceptance: polynomial image factors are included. Output: theorem family.
- [x] **P4-B4 — Prove kernel positivity floor.** Input: principal and tail
  bounds. Acceptance: strict denominator separation on every log-derivative
  interval. Output: enclosure lemma.
- [x] **P4-B5 — Treat the identity.** Action: use parity/Taylor expansions and
  removable limits. Acceptance: derivative enclosures join the interior
  intervals continuously. Output: identity lemma.
- [x] **P4-B6 — Treat the cut locus.** Action: use paired shortest images,
  symmetry, or a character expansion. Acceptance: multiplicity is handled and
  no false single-image bound crosses `pi`. Output: cut-locus lemma.
- [x] **P4-B7 — Quantify small-time asymptotics.** Input: P4-B1--P4-B6.
  Acceptance: explicit finite-time remainder with declared uniform domain.
  Output: asymptotic theorem.

### C. Build log-derivative and action theorems

- [x] **P4-C1 — Enclose the first log derivative.** Input: P4-B3, P4-B4.
  Acceptance: interval quotient propagation includes correlations or safe
  over-enclosure. Output: theorem.
- [x] **P4-C2 — Enclose the second log derivative.** Input: P4-C1 and kernel
  derivatives. Acceptance: uniform radial curvature bounds. Output: theorem.
- [x] **P4-C3 — Enclose the third log derivative.** Input: derivative tails.
  Acceptance: theorem covers the full declared nonlinear chart. Output:
  theorem.
- [x] **P4-C4 — Derive radial/tangential Hessian eigenvalues.** Input: geometry
  of radial functions on `S^3`. Acceptance: the identity limit and metric
  convention are correct. Output: action-Hessian proposition.
- [x] **P4-C5 — Parameterize derivative order.** Action: determine whether a
  recursive Bell-polynomial or logarithmic derivative scheme yields arbitrary
  `k`. Acceptance: either a proved general theorem or a documented reason to
  retain order three. Output: theorem or limitation ledger.
- [x] **P4-C6 — Translate to lattice-action budgets.** Input: P4-C1--P4-C4.
  Action: state exact corollaries for local convexity and nonlinear remainders.
  Acceptance: no RG or continuum implication. Output: application corollary.

### D. Prove normalized tails

- [x] **P4-D1 — Derive exact radial Haar volume.** Action: integrate the class
  measure and align normalization. Acceptance: endpoint and cubic small-radius
  expansion are correct. Output: lemma.
- [x] **P4-D2 — Bound tail numerator.** Input: P4-B2 and P4-D1. Acceptance:
  all images and Haar factors are enclosed. Output: numerator theorem.
- [x] **P4-D3 — Bound normalizing denominator.** Input: P4-B4 and P4-D1.
  Acceptance: positive explicit lower bound optimized or safely chosen. Output:
  denominator theorem.
- [x] **P4-D4 — Form normalized tail ratio.** Input: P4-D2, P4-D3. Acceptance:
  directed division and declared `t,rho` domain. Output: tail theorem.
- [x] **P4-D5 — Compare asymptotic and finite-time regimes.** Input: P4-B7,
  P4-D4. Acceptance: crossover domains are explicit. Output: regime table.

### E. Construct rigorous numerical certificates

- [x] **P4-E1 — Select interval backend.** Action: choose a directed-rounding
  library or exact rational-enclosure method. Acceptance: rounding guarantees
  are documented and testable. Output: methods decision.
- [x] **P4-E2 — Implement certified elementary functions.** Input: P4-E1.
  Acceptance: exponential, trigonometric, and division operations preserve
  enclosures. Output: verified primitives or trusted dependency statement.
- [x] **P4-E3 — Implement adaptive interval subdivision.** Input: P4-A5.
  Acceptance: full-domain coverage, overlap checks, and termination criteria.
  Output: certificate generator.
- [x] **P4-E4 — Emit proof certificates.** Action: store domain, formula,
  truncation order, bounds, rounding metadata, and hashes. Acceptance: verifier
  does not trust a final decimal alone. Output: certificate schema/data.
- [x] **P4-E5 — Cross-check character and image formulas.** Input: common
  stable region. Acceptance: rigorous enclosures overlap on every validation
  cell. Output: cross-check report.
- [x] **P4-E6 — Reproduce Stage 07 constants.** Input: certified engine.
  Acceptance: old floating estimates lie inside new enclosures; discrepancies
  are resolved. Output: migration report.
- [x] **P4-E7 — Hostile boundary tests.** Action: test identity, cut locus,
  smallest time, largest chart radius, and denominator minima. Acceptance: no
  uncovered or undefined cells. Output: test log.

### F. Novelty, drafting, and decision

- [x] **P4-L1 — Search heat-kernel derivative estimates.** Action: search
  primary literature for compact Lie-group Gaussian, gradient, Hessian, and
  higher-derivative bounds. Acceptance: theorem-by-theorem comparison. Output:
  literature matrix.
- [x] **P4-L2 — Search explicit `SU(2)` formulas and enclosures.** Action:
  inspect analysis, lattice gauge, numerical proof, and Lie-group computation
  sources. Acceptance: no rediscovery is marketed as novelty. Output: ledger.
- [x] **P4-L3 — Search heat-kernel lattice applications.** Action: follow
  Menotti--Onofri citations and constructive uses. Acceptance: downstream need
  is documented. Output: application bibliography.
- [x] **P4-L4 — Benchmark constants.** Input: P4-C and P4-D results. Action:
  compare domain, order, explicitness, and sharpness with closest sources.
  Acceptance: advantage is quantitative and relevant. Output: benchmark table.
- [x] **P4-L5 — Attempt generalization.** Action: explore arbitrary derivative
  order, `SU(N)`, or a class of compact groups. Acceptance: prove something
  reusable or document the obstruction. Output: extension theorem/ledger.
- [x] **P4-L6 — Decide standalone versus merge.** Dependencies:
  P4-L1--P4-L5. Acceptance: apply Section 8 gate in writing. Output: signed
  decision memo.
- [x] **P4-W1 — Draft chosen form.** If standalone, follow the architecture;
  if merge, produce a self-contained P2 appendix. Acceptance: theorem family
  and proof precede application constants. Output: manuscript or appendix.
- [x] **P4-V1 — Independent verifier.** Action: implement or run a second
  method. Acceptance: rigorous overlaps for all theorem-critical bounds.
  Output: verification report.
- [x] **P4-V2 — Analytic proof audit.** Action: inspect truncation interchange,
  endpoint limits, denominator positivity, and convention conversions.
  Acceptance: no sampled inference. Output: audit report.
- [x] **P4-V3 — Frontier audit.** Action: use `ym-audit-frontier`. Acceptance:
  the only physics consequence is the proved finite-action corollary. Output:
  scope report.
- [x] **P4-S1 — Select venue if standalone.** Acceptance: scope values explicit
  estimates or computer-assisted analysis. Output: venue memo.
- [x] **P4-S2 — Build final archive.** Acceptance: source, bibliography,
  interval engine, certificates, tests, data statement, and manuscript/appendix
  are version-locked. Output: release bundle.

## 7. Risks

- Existing compact-group heat-kernel estimates may dominate the analytic
  theorem, leaving only application-specific constants.
- Cut-locus behavior may require a separate formula and weaken a global
  theorem.
- Interval dependency can make naive derivative enclosures too wide.
- An `SU(N)` extension may be much more than a paper-sized task.
- Sharpness may be irrelevant if P2 needs only a coarse strict margin.

## 8. Stop/go gates: standalone publication decision

P4 becomes an independent paper only if at least one condition is satisfied:

1. a general derivative-order theorem with explicit computable constants;
2. a nontrivial extension beyond `SU(2)`;
3. substantially sharper uniform bounds on a domain used in constructive QFT;
4. the first rigorous interval-certified enclosure suite of this exact type,
   after a complete literature audit;
5. closure of a recognized analytic estimate not specific to this package.

If none holds, all completed work remains valuable but is merged into P2.
That outcome is success for the portfolio, not failure.

## 9. Definition of done

P4 is complete when all formulas and constants share one convention, analytic
remainder proofs cover the full domain, an independent verifier certifies the
claims, the literature comparison is theorem-specific, and the standalone or
merge decision is documented by the gate above.
