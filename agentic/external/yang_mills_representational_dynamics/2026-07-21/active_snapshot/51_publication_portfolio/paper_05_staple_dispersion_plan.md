# P5 publication plan: gauge-covariant staple dispersion and spillover

## 1. Frozen identity

Working title:

> **Staple Dispersion and Curvature Spillover in `SU(2)` Lattice Gauge
> Theory: Nonlinear Comparison and Exact Finite-Block Certificates**

Publication type: mathematical-physics note with exact computational
certificates.

Final internal decision: `IMPLEMENTED / HOLD FOR EXTERNAL NOVELTY REVIEW`.
The result is a defensible `C2` finite-block theorem.  It is not a claim about
an interacting nonlinear measure, a scale-uniform repair, the continuum, or a
mass gap.

Core thesis: Fréchet dispersion is the invariant residual energy of a link
star; its dependent Gaussian law and the minimum external-curvature cost of
lifting a centered star operation can be evaluated exactly on the open
side-two four-cube.

Reusable workflow: `ym-draft-staple-dispersion`, orchestrating
`ym-develop-paper-proofs`, `ym-ground-paper-literature`,
`ym-frame-paper-narrative`, `ym-build-proof-appendix`,
`ym-build-latex-paper`, and `ym-audit-frontier`.

## 2. Self-contained todo graph

### A. Freeze geometry and claims

- [x] **P5-A1 — Define the transport bitorsor.**  State the left/right gauge
  action on complementary paths and identify invariant distances.
- [x] **P5-A2 — Freeze the metric convention.**  Use the unit-round `S^3`
  normalization of `SU(2)` and explain rescaling.
- [x] **P5-A3 — Orient every incident plaquette.**  Insert the incidence-sign
  matrix before centering and audit all inherited calculations.
- [x] **P5-A4 — Define Fréchet staple dispersion.**  Specify its minimizer,
  gauge invariance, and domain.
- [x] **P5-A5 — Define the test complex.**  Record open boundary, side two,
  cochain counts, rank, and the eight interior links.
- [x] **P5-A6 — Freeze exclusions.**  Exclude nonlinear measure comparison,
  repeated RG, continuum construction, and mass-gap consequences.

### B. Develop the nonlinear theorem suite

- [x] **P5-B1 — Prove the residual-energy identity.**  Identify dispersion
  with the minimum local geodesic-quadratic action over the central link.
- [x] **P5-B2 — Prove the diameter witness.**  Keep its one-sided logical
  direction explicit.
- [x] **P5-B3 — Derive the Karcher stationarity equation.**  State cut-locus
  and radius hypotheses.
- [x] **P5-B4 — Prove exponential-map contraction.**  Use exact spherical
  differential singular values.
- [x] **P5-B5 — Prove inverse-log control.**  Use strong convexity of balls of
  radius below `pi/2`; do not infer a lower Lipschitz bound from path length in
  the wrong direction.
- [x] **P5-B6 — Prove pairwise/Fréchet comparison.**  Obtain the factor
  `(sin r/r)^2` and the Euclidean variance identity.
- [x] **P5-B7 — State deterministic coordinate transfer.**  Isolate the exact
  centered-error premise required for a Gaussian comparison.

### C. Exact dependent-Gaussian calculation

- [x] **P5-C1 — Build the integer cubical coboundary.**  Hash the matrix and
  verify counts and ranks.
- [x] **P5-C2 — Characterize the quotient covariance.**  Use the orthogonal
  projection onto `im d1`, retaining all dependence.
- [x] **P5-C3 — Restrict, orient, and center the star covariance.**  Apply
  `C6 O_l S_l` in the theorem-correct order.
- [x] **P5-C4 — Produce rational projection witnesses.**  Verify image and
  normal equations exactly for all eight links.
- [x] **P5-C5 — Factor the covariance characteristic polynomial.**  Prove the
  rational spectrum and multiplicities.
- [x] **P5-C6 — Derive the weighted-chi-square law and tail.**  Give the exact
  moment generating function and optimized determinant Chernoff bound.

### D. Minimum-spill lifting theorem

- [x] **P5-D1 — Define the abstract spill form.**  Minimize external curvature
  over link lifts of a prescribed centered star displacement.
- [x] **P5-D2 — Prove quadraticity and the kernel criterion.**  Identify
  no-spill operations with an exact intersection of affine constraints.
- [x] **P5-D3 — Choose rational centered coordinates.**  Track the generalized
  metric `G=I+11^T` rather than hiding square roots in an orthonormal basis.
- [x] **P5-D4 — Solve the exact KKT system.**  Use QR only to locate a minor,
  then Bareiss elimination and full rational substitution.
- [x] **P5-D5 — Factor the generalized characteristic polynomial.**  Prove the
  spectra `37/33` and `391/239` with correct multiplicities.
- [x] **P5-D6 — Derive the repair budget.**  Distinguish no-spill obstruction,
  possible total-action decrease, ideal-coordinate Jacobian, and unresolved
  nonlinear link-map Jacobian.

### E. Literature, novelty, and proof governance

- [x] **P5-E1 — Search primary smoothing and update literature.**  Cover
  overrelaxation, cooling/staples, stout smearing, and Wilson flow.
- [x] **P5-E2 — Search Riemannian center-of-mass literature.**  Separate the
  classical geometric input from the lattice interpretation.
- [x] **P5-E3 — Search for direct staple-dispersion precedents.**  Record the
  absence of a direct hit as a search result, not proof of novelty.
- [x] **P5-E4 — Build the closest-results comparison.**  Compare tasks,
  hypotheses, and outputs theorem by theorem.
- [x] **P5-E5 — Audit the orientation correction.**  Document why the earlier
  signed-row centering produced a spurious zero-spill mode.
- [x] **P5-E6 — Run a frontier audit.**  Fix the final claim at `C2` and list
  every missing physical implication.

### F. Manuscript, appendix, verification, and package

- [x] **P5-F1 — Frame one paper-level narrative.**  Lead with residual energy
  and exact spillover rather than the broader research pipeline.
- [x] **P5-F2 — Write the self-contained main text.**  Remove stage numbers and
  define every operator locally.
- [x] **P5-F3 — Write complete proof appendices.**  Include covariance and KKT
  certificate logic, not just matrices.
- [x] **P5-F4 — Implement exact certificate generation.**  Emit canonical JSON
  for every interior link.
- [x] **P5-F5 — Implement hostile tests.**  Test counts, spectra, polynomial
  arithmetic, full KKT substitution, and stored-certificate equality.
- [x] **P5-F6 — Build and lint LaTeX.**  Resolve citations, labels,
  placeholders, and substantive overfull boxes.
- [x] **P5-F7 — Render and inspect PDF pages.**  Inspect first, theorem-dense,
  matrix-dense, and final pages.
- [x] **P5-F8 — Assemble reproducibility and submission artifacts.**  Include
  README, scope notices, audits, reports, archive, and checksum.
- [x] **P5-F9 — Update the five-paper portfolio and portable skill bundle.**
  Register P5 independently and export its orchestrating skill.

Todo count: **40**.  Completed: **40**.

## 3. Stop/go gates

The manuscript is technically complete, but submission should wait for a
human-led citation-chain review in lattice algorithm and discrete Hodge
literatures.  Proceed as a standalone note only if that review confirms that
the orientation-correct exact minimum-spill spectrum and the residual-energy
interpretation are not already explicit.  Otherwise merge the exact theorem
as a methods section or appendix in a larger constructive paper.

## 4. Definition of done

The work package is done when all 40 todos are checked, every theorem-critical
spectrum is certified for all eight interior links, the orientation correction
is explicit, analytic proofs and conditional premises are separated, the
LaTeX build and tests pass, representative PDF pages are visually inspected,
the portable skill bundle validates, and the submission archive has a recorded
checksum.  External novelty review remains a submission gate rather than an
unfinished implementation todo.
