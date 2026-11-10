# P1 publication plan: frustrated boundary conditions

## 1. Frozen identity

Working title:

> **Frustrated Boundary Conditions and the Failure of Uniform Local Defect
> Domination in Weak-Coupling Lattice Gauge Theory**

Publication type: standalone mathematical-physics theorem paper.

Current decision: strong `GO`.

Implementation status (21 July 2026): all 32 scientific and production todos
are complete in `paper_01_frustrated_conditioning/`.  The blinded manuscript
compiles to a 21-page PDF and passes strict lint, exact-code, visual, and
frontier audits.  External submission still requires user-supplied author
metadata and a final subscription-database refresh.

Current defensible level: `C2`, a rigorous restricted lattice theorem. The
paper does not construct continuum Yang--Mills theory and does not establish a
mass gap.

Core thesis: a weak-coupling one-plaquette tail can be exponentially small
while a physically admissible microscopic boundary conditioning forces a
selected plaquette to be bad with probability tending to one. Therefore a
uniform-over-all-boundaries rare-defect estimate has the wrong quantifier for
initializing a Dobrushin or adaptive domination argument.

Reusable workflow: `ym-draft-frustration-obstruction`, followed by
`ym-audit-frontier`.

## 2. Minimum theorem contract

The submitted paper must prove, without depending on exploratory numerics:

1. On a specified open hypercubic block in dimension `d`, an interior link has
   `m=2(d-1)` incident plaquettes.
2. For `SU(2)`, a center-valued assignment of the other links realizes a
   prescribed incident staple pattern with `m-1` identity staples and one
   `-I` staple.
3. Under the heat-kernel plaquette action, the one-link conditional law is
   \[
   \gamma_t(dU)=Z_t^{-1}p_t(U)^{m-1}p_t(-U)\,dU.
   \]
4. Its class-angle rate is
   \[
   I_m(\theta)=(m-1)\theta^2+(\pi-\theta)^2
   =m\left(\theta-\frac{\pi}{m}\right)^2
   +\frac{m-1}{m}\pi^2.
   \]
5. Hence the selected link concentrates at `pi/m` and the frustrated
   plaquette at `(m-1)pi/m`; every smaller good-curvature radius has bad
   probability tending to one.
6. The conclusion persists on an open, positive-Haar-measure neighborhood of
   the center boundary assignment.
7. The precise proposed uniform conditional estimate, and only that estimate,
   is falsified.

The four-dimensional `m=6` theorem is the minimum publishable unit. The
dimension-`d` statement is the preferred theorem. A compact-group extension
is a stretch theorem and must state geodesic uniqueness and cut-locus
hypotheses explicitly.

## 3. Novelty hypothesis and known baseline

The exact ingredients—compact-group heat kernels, center-valued link
assignments, Laplace principles, and Dobrushin-style conditioning—are known.
The novelty hypothesis is their combination into an explicit admissible gauge
boundary showing asymptotic failure of worst-conditioning rare-defect
domination, together with the identification of the boundary charge that a
successful dependent contour method must retain.

This priority claim is provisional until P1-L1--P1-L5 are complete. Mandatory
starting points include the Menotti--Onofri heat-kernel action
([DOI](https://doi.org/10.1016/0550-3213(81)90560-5)), Balaban's small-field
and large-field RG papers
([Part I](https://doi.org/10.1007/BF01215223),
[Part II](https://doi.org/10.1007/BF01239022),
[large fields II](https://doi.org/10.1007/BF01238433)), and primary work on
center flux, twisted boundaries, conditional uniqueness, and dependent
polymer domination located through their citation chains.

Do not claim that center frustration itself is new. The candidate novelty is
the conditional concentration theorem and its exact quantifier consequence.

## 4. Source corpus inside this package

Primary inputs:

- `10_frustrated_conditioning_obstruction/frustrated_conditioning_theorem.tex`
- `10_frustrated_conditioning_obstruction/frustrated_conditioning.py`
- `10_frustrated_conditioning_obstruction/test_frustrated_conditioning.py`
- `10_frustrated_conditioning_obstruction/theorem_dependencies_frustrated.json`
- `10_frustrated_conditioning_obstruction/frustrated_conditioning_frontier_ledger.md`

Supporting inputs:

- `03_heat_kernel_basin_entry/heat_kernel_basin_entry_attack.tex`
- `11_good_collar_coherence/good_collar_coherence_theorem.tex`
- `12_center_contour_charging/center_contour_charging_theorem.tex`
- `15_nonasymptotic_good_collar/nonasymptotic_good_collar_theorem.tex`
- `16_continuous_collar_charging/continuous_collar_charging_theorem.tex`
- `31_frechet_collar_charge/frechet_collar_charge_theorem.tex`
- `32_dispersion_conditional_optimizer/dispersion_conditional_optimizer_theorem.tex`
- `44_link_lift_spillover/link_lift_spillover_theorem.tex`

The supporting stages may motivate viable replacements, but the P1 theorem
must not depend on the later programme.

## 5. Manuscript architecture

1. Introduction: state the bad quantifier and the main theorem.
2. Lattice and heat-kernel conventions.
3. Exact realization of frustrated incident staples.
4. One-link conditional law.
5. Small-time large-deviation theorem.
6. Stability under boundary perturbations.
7. Dimension and compact-group generalizations.
8. Consequences for conditional domination and what remains viable.
9. Relation to constructive RG, center flux, and boundary-condition methods.
10. Appendix: exact incidence certificate and reproducibility.

Target length: 25--35 manuscript pages plus supplement. The theorem and proof
should occupy most of the paper; programme history should occupy none.

## 6. Self-contained todo graph

All dependencies below are internal to P1.

### A. Freeze definitions and reconstruct the core

- [x] **P1-A1 — Freeze conventions.** Input: Stage 10 source. Action: define
  block geometry, orientation, heat generator, Haar measure, class angle,
  staple convention, conditional probability, and good event. Acceptance: a
  reader can reproduce every factor in the conditional density. Output:
  `p1_notation.tex`.
- [x] **P1-A2 — Remove stage dependence.** Input: P1-A1 and Stage 10 theorem.
  Action: replace all “Stage 09/10” and programme references by definitions or
  citations. Acceptance: no stage language remains in theorem-bearing prose.
  Output: clean core draft.
- [x] **P1-A3 — Prove incident-staple surjectivity geometrically.** Input:
  oriented hypercubic incidence. Action: exhibit distinct opposite links and
  prove the relevant center map has full row rank. Acceptance: proof works for
  every declared `d`, block size, and chosen interior link. Output: lemma and
  diagram.
- [x] **P1-A4 — Cross-check exact incidence.** Input: P1-A3 and existing code.
  Action: recompute the finite matrix with exact `GF(2)` arithmetic.
  Acceptance: symbolic proof and machine certificate agree; orientation
  permutations do not change rank. Output: certificate JSON.
- [x] **P1-A5 — Derive the conditional law from the full measure.** Input:
  P1-A1 and P1-A3. Action: cancel nonincident factors and use centrality and
  inversion symmetry. Acceptance: every normalization and conjugation step is
  written explicitly. Output: proposition.
- [x] **P1-A6 — Derive radial reduction.** Input: P1-A5. Action: include the
  exact radial Haar factor and target-plaquette angle relation. Acceptance: no
  hidden proportionality affects the rate proof. Output: radial density lemma.

### B. Prove and generalize the asymptotics

- [x] **P1-B1 — State the required heat-kernel Laplace bound.** Input: primary
  compact-group heat-kernel literature. Action: state a uniform small-time
  result sufficient for numerator and denominator sets. Acceptance: endpoints
  and the cut locus are covered or excluded explicitly. Output: cited lemma.
- [x] **P1-B2 — Prove the `SU(2)` rate principle.** Dependencies: P1-A6,
  P1-B1. Action: prove upper and lower large-deviation bounds including the
  subexponential Haar zero. Acceptance: not merely pointwise asymptotics.
  Output: theorem proof.
- [x] **P1-B3 — Optimize the `m`-staple rate exactly.** Dependency: P1-B2.
  Action: complete the square and compute the good-event constrained minimum.
  Acceptance: all threshold cases in `rho` are stated. Output: corollary.
- [x] **P1-B4 — Prove bad-probability convergence.** Dependency: P1-B3.
  Action: obtain the exponential good-event rate and bad-event limit.
  Acceptance: the event and orientation match P1-A1. Output: main theorem.
- [x] **P1-B5 — Prove positive-measure stability.** Dependencies: P1-A5,
  P1-B3. Action: control movement of conditional minimizers under neighboring
  boundary staples. Acceptance: give a uniform open neighborhood and a
  retained rate margin. Output: stability theorem.
- [x] **P1-B6 — Establish coherent/frustrated separation.** Dependency:
  P1-B4. Action: compare a coherent boundary conditional law with the
  frustrated law using disjoint concentration neighborhoods. Acceptance:
  total variation tends to one, with conventions visible. Output: corollary.
- [x] **P1-B7 — Audit the Dobrushin consequence.** Dependency: P1-B6. Action:
  map the pair of boundary conditions to the exact influence coefficient used
  in the chosen convention. Acceptance: prove a limit only for the coefficient
  actually defined; avoid extrapolation to every uniqueness method. Output:
  proposition or carefully limited remark.
- [x] **P1-B8 — Attempt the compact-group theorem.** Input: center element `z`
  and bi-invariant metric. Action: minimize the sum of squared distances and
  identify sufficient injectivity/geodesic hypotheses. Acceptance: either a
  correct general theorem or a documented counterexample/limitation. Output:
  theorem or scope ledger.

### C. Stress tests and consequences

- [x] **P1-C1 — Vary the number of frustrated staples.** Input: rate
  construction. Action: solve the `k` versus `m-k` center competition.
  Acceptance: symmetry, degeneracy, and multiple-minimizer cases are recorded.
  Output: proposition or appendix table.
- [x] **P1-C2 — Test low-dimensional cases.** Input: P1-A3. Action: verify
  `d=2,3` geometry and identify any boundary-size exceptions. Acceptance: the
  dimension theorem has no false universal quantifier. Output: test ledger.
- [x] **P1-C3 — Test trivial-center groups.** Input: P1-B8. Action: determine
  which mechanism survives without a nontrivial center. Acceptance: the paper
  does not imply universality across all compact simple groups. Output: scope
  remark.
- [x] **P1-C4 — Separate obstruction from replacement.** Input: Stages 11, 12,
  15, 16, 31, 32, 44. Action: classify good collars, block integration, and
  labeled contours as open alternatives. Acceptance: no replacement theorem
  is claimed unless fully proved in P1. Output: discussion section.
- [x] **P1-C5 — Build the claim ledger.** Input: all P1 results. Action: label
  analytic proof, exact computation, exploratory numerics, conjecture, and not
  claimed. Acceptance: every abstract sentence maps to a proved row. Output:
  claim table.

### D. Establish novelty and positioning

- [x] **P1-L1 — Search exact theorem language.** Action: search MathSciNet,
  zbMATH, INSPIRE, arXiv, and journal full text for heat-kernel conditional
  concentration under frustrated staples. Acceptance: queries and screened
  results are logged. Output: search ledger.
- [x] **P1-L2 — Follow center/twisted-boundary citation chains.** Action:
  inspect primary work on center flux and boundary free energies. Acceptance:
  distinguish global twists from the local conditional theorem. Output:
  comparison matrix.
- [x] **P1-L3 — Follow Dobrushin/domination citation chains.** Action: identify
  the exact boundary-uniform hypotheses used in lattice gauge or continuous
  spin systems. Acceptance: claims about invalidated methods quote formal
  hypotheses, not slogans. Output: literature notes.
- [x] **P1-L4 — Compare with constructive RG.** Action: read Balaban's relevant
  small/large-field papers and later expositions. Acceptance: explain why
  Balaban's machinery is not displaced by this obstruction. Output: positioning
  subsection.
- [x] **P1-L5 — Freeze novelty language.** Dependencies: P1-L1--P1-L4. Action:
  write a one-paragraph contribution statement with no unverified priority
  word. Acceptance: each clause has a source comparison or theorem pointer.
  Output: novelty statement.

### E. Draft, verify, and submit

- [x] **P1-W1 — Draft theorem-first abstract.** Dependencies: P1-B4, P1-B5,
  P1-L5. Acceptance: contains the law, minimizer, invalidated quantifier, and
  explicit nonclaim. Output: abstract.
- [x] **P1-W2 — Draft full manuscript.** Dependencies: P1-A1--P1-L5. Action:
  follow the architecture above. Acceptance: self-contained proof flow and no
  package-stage narration. Output: manuscript source.
- [x] **P1-W3 — Build figures.** Action: create one lattice incidence figure
  and one rate-function figure only if they carry proof or intuition.
  Acceptance: captions define conventions independently. Output: vector
  figures.
- [x] **P1-V1 — Run symbolic and exact-code checks.** Input: appendix code.
  Acceptance: fresh environment reproduces ranks and algebraic identities.
  Output: verification log.
- [x] **P1-V2 — Conduct proof audit.** Action: check quantifiers, rate lower
  bounds, positive-measure stability, and Dobrushin definitions. Acceptance:
  no result depends on sampled floating values. Output: audit report.
- [x] **P1-V3 — Conduct frontier audit.** Action: use `ym-audit-frontier`.
  Acceptance: title, abstract, introduction, and conclusion remain `C2`.
  Output: claim-level report.
- [x] **P1-S1 — Select venue band.** Input: final theorem strength and length.
  Action: compare scope of mathematical-physics journals; choose one target and
  two fallbacks. Acceptance: formatting and length fit. Output: venue memo.
- [x] **P1-S2 — Create submission bundle.** Dependencies: all previous tasks.
  Acceptance: manuscript, bibliography, supplement, code archive, certificates,
  data statement, and cover letter compile and cross-reference correctly.
  Output: versioned submission archive.

## 7. Stop/go gates

- **G1—Core correctness:** stop if P1-B2 cannot justify uniform setwise
  large-deviation bounds. Repair before drafting.
- **G2—Novelty:** stop or reposition as a short note if P1-L1--P1-L4 locate the
  same theorem and consequence.
- **G3—Generalization:** failure of P1-B8 does not block the `SU(2)` or
  dimension-`d` paper; it must be reported as a boundary of scope.
- **G4—Submission:** proceed only when positive-measure stability is proved,
  not merely asserted by continuity.

## 8. Definition of done

P1 is submission-ready when the minimum theorem contract is proved in the
manuscript, the incidence calculation is exact, the novelty audit is archived,
the code is supplementary rather than logically necessary, all Clay-adjacent
claims pass frontier audit, and the complete submission bundle reproduces from
a clean environment.
