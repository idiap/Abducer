# P2 publication plan: verified nonlinear quotient--fiber block

## 1. Frozen identity

Final working title:

> **An Exact Quotient--Fiber Certificate for One Local Marginalization in
> Four-Dimensional `SU(2)` Heat-Kernel Lattice Gauge Theory**

Publication type: mathematical-physics/computer-assisted proof paper.

Current decision: `IMPLEMENTED_SUBMISSION_CANDIDATE`. Theorem-critical
floating computations have been replaced by exact rational, modular, integer,
or analytic bounds.

Current defensible level: one unambiguously certified `C2` restricted
finite-block theorem.

Core thesis: on one explicitly defined four-dimensional cubical block, gauge
redundancy can be quotiented, retained and fiber variables can be separated,
the exact nonlinear `SU(2)` heat-kernel action can be controlled on a local
chart, and one conditional marginalization can be bounded by a complete,
machine-checkable certificate.

Implementation refinement: the final theorem uses a rooted spanning-tree gauge
rather than a nonlinear Coulomb slice. This makes the quotient Haar
factorization exact and removes an otherwise unbounded Faddeev--Popov density.
The retained variable is explicitly a linear covariant coordinate in cotree
logarithms; the plaquette action and marginalization remain fully nonlinear.

Reusable workflow: `ym-draft-finite-block-certificate`, with
`ym-draft-heat-kernel-enclosures` for the analytic initializer and
`ym-audit-frontier` at claim freeze.

## 2. Minimum theorem contract

The paper must define one block and prove one integrated theorem containing:

1. exact cubical cochain dimensions and ranks;
2. an explicit relative gauge fixing and physical quotient;
3. an explicit retained map and its fiber dimension;
4. a certified Hodge/fiber coercivity lower bound;
5. exact centered Gaussian fiber cancellation and retained covariance
   accounting;
6. a nonlinear plaquette chart with a proved domain and bi-Lipschitz constants;
7. interval-certified heat-kernel Hessian and higher-derivative bounds;
8. strong log-concavity of the conditional fiber throughout the declared
   retained-state cylinder;
9. an exact marginalization identity and a certified bound on the generated
   retained interaction;
10. a local-cylinder/complement statement with its normalization and all
    boundary quantifiers visible.

The theorem is about one RG building block. It must explicitly say that it
does not prove repeated RG closure, a volume-uniform basin, continuum
existence, or a physical spectral gap.

## 3. Novelty hypothesis and known baseline

Most ingredients are classical or standard in isolation: product Hodge
theory, tree/Coulomb gauge fixing, Schur complements, Gaussian conditioning,
strong log-concavity, heat-kernel actions, and local nonlinear charts. Balaban
already constructed localized small-field effective actions, cluster
expansions, and large-field operations in four-dimensional lattice gauge
theory. Mandatory baselines include
[propagators](https://doi.org/10.1007/BF01215753),
[small fields I](https://doi.org/10.1007/BF01215223),
[cluster expansions II](https://doi.org/10.1007/BF01239022), and
[large fields II](https://doi.org/10.1007/BF01238433).

The provisional novelty is the integrated, executable, explicit finite-block
certificate with modern proof artifacts—not a new constructive RG programme.
Any stronger novelty claim must be earned by P2-L1--P2-L6.

## 4. Source corpus inside this package

Core block and marginalization inputs:

- `05_su2_quotient_fiber/su2_quotient_fiber_theorem.tex`
- `05_su2_quotient_fiber/su2_block_linearized.py`
- `06_one_step_effective_action/one_step_effective_action_theorem.tex`
- `06_one_step_effective_action/one_step_effective_action.py`
- `08_su2_nonlinear_block_geometry/su2_nonlinear_block_geometry_theorem.tex`
- `08_su2_nonlinear_block_geometry/su2_nonlinear_block_geometry.py`

Analytic and normalization inputs:

- `07_su2_heat_kernel_initializer/su2_heat_kernel_initializer_theorem.tex`
- `07_su2_heat_kernel_initializer/su2_heat_kernel_initializer.py`
- `20_su2_boundary_state_disintegration/su2_boundary_state_theorem.tex`
- `21_curvature_typical_set_atlas/curvature_typical_set_theorem.tex`
- `22_sharp_nonlinear_overlap/sharp_nonlinear_overlap_theorem.tex`
- `23_local_cylinder_comparison/local_cylinder_comparison_theorem.tex`
- `41_nonlinear_dispersion_geometry/nonlinear_dispersion_geometry_theorem.tex`
- `42_dispersion_tail_transfer/dispersion_tail_transfer_theorem.tex`

Every numerical claim must be traced to its script, test, calibration JSON,
and theorem dependency file.

## 5. Manuscript architecture

1. Main theorem and certificate philosophy.
2. Finite cubical complex and boundary convention.
3. Gauge quotient, relative slice, and retained/fiber decomposition.
4. Exact linear Hodge and Gaussian structure.
5. Nonlinear `SU(2)` curvature chart.
6. Heat-kernel action enclosures.
7. Conditional fiber coercivity and one-step marginalization.
8. Local-cylinder normalization and complement.
9. Machine certificate and independent verification.
10. Comparison with constructive RG and limits of the result.

Target length: 35--50 manuscript pages plus a certificate supplement.

## 6. Self-contained todo graph

All dependencies below are internal to P2.

### A. Freeze the mathematical object

- [x] **P2-A1 — Fix block geometry.** Input: Stages 05 and 08. Action: define
  vertex, link, plaquette, cell orientations, open/relative boundary, and
  inner product. Acceptance: exact incidence matrices are determined without
  code conventions. Output: block specification.
- [x] **P2-A2 — Fix gauge action and quotient.** Input: P2-A1. Action: define
  vertex gauge transformations, stabilizers, boundary treatment, gauge tree or
  Coulomb slice, and physical tangent space. Acceptance: dimension statements
  follow from written definitions. Output: quotient section.
- [x] **P2-A3 — Fix retained and fiber variables.** Input: Stages 05, 06, 20.
  Action: define the retained map, conditional fiber, retained-state cylinder,
  and exact marginal. Acceptance: no “coarse variable” remains informal.
  Output: map diagram and notation table.
- [x] **P2-A4 — Freeze normalization and units.** Input: Stages 07 and 08.
  Action: align Lie-algebra norm, quaternion coordinates, Haar measure,
  Laplacian generator, heat time, and action scaling. Acceptance: all constants
  have a unique convention. Output: conversion table.
- [x] **P2-A5 — State one theorem.** Dependencies: P2-A1--P2-A4. Action:
  combine the intended conclusions with complete quantifiers. Acceptance: no
  theorem refers to a stage or later paper. Output: theorem contract.

### B. Convert topology and linear algebra to exact proof

- [x] **P2-B1 — Certify cochain ranks.** Input: P2-A1. Action: compute ranks
  over the integers/rationals and prove them from a spanning tree or exact
  elimination. Acceptance: portable exact certificate. Output: rank proof and
  JSON.
- [x] **P2-B2 — Certify retained-map rank and fiber dimension.** Input: P2-A3.
  Acceptance: exact arithmetic and independent dimension identity agree.
  Output: proposition and certificate.
- [x] **P2-B3 — Prove gauge-slice uniqueness on the linear domain.** Input:
  P2-A2. Action: characterize the kernel and boundary stabilizer. Acceptance:
  no pseudoinverse assumption substitutes for proof. Output: slice lemma.
- [x] **P2-B4 — Certify Hodge coercivity.** Input: exact matrices. Action:
  replace `eigvalsh` evidence by rational LDL, interval eigenvalue inclusion,
  or a symbolic lower bound. Acceptance: a strict positive lower endpoint is
  independently checkable. Output: spectral certificate.
- [x] **P2-B5 — Prove centered Gaussian cancellation.** Input: P2-B2--P2-B4.
  Action: derive the conditional mean, covariance, Schur complement, and
  centered cross term exactly. Acceptance: dimensions and adjoints match the
  declared inner products. Output: Gaussian theorem.
- [x] **P2-B6 — Audit orientation and gauge-tree invariance.** Input: P2-B1--B5.
  Action: rerun exact certificates under representative orientation and tree
  changes. Acceptance: invariant conclusions are separated from coordinate
  constants. Output: invariance ledger.

### C. Certify nonlinear geometry and heat-kernel inputs

- [x] **P2-C1 — Define the nonlinear plaquette map explicitly.** Input:
  quaternion/BCH implementation. Acceptance: analytic formula, derivative, and
  tangent convention match code. Output: map definition.
- [x] **P2-C2 — Prove a quantitative slice theorem.** Input: P2-B3 and P2-C1.
  Action: apply a quantitative inverse/implicit theorem with explicit domain.
  Acceptance: existence, uniqueness, and constants are rigorous. Output:
  nonlinear slice theorem.
- [x] **P2-C3 — Enclose first through third plaquette derivatives.** Input:
  exact formulas. Action: use analytic inequalities or interval arithmetic over
  the full chart. Acceptance: no sampled supremum. Output: interval certificate.
- [x] **P2-C4 — Certify bi-Lipschitz curvature bounds.** Dependency: P2-C3.
  Acceptance: lower and upper singular values have directed-rounding
  enclosures throughout the chart. Output: chart theorem.
- [x] **P2-C5 — Rebuild heat-kernel initializer rigorously.** Input: Stage 07.
  Action: certify kernel positivity, log derivatives, radial Hessian, third
  derivative, and truncation tails on the declared interval. Acceptance: every
  division has a positive denominator enclosure. Output: analytic/interval
  appendix.
- [x] **P2-C6 — Certify Haar/Jacobian contributions.** Input: P2-A4 and Stage
  21. Action: prove measure-density bounds in the selected coordinates.
  Acceptance: the effective action includes all Jacobians. Output: measure
  lemma.
- [x] **P2-C7 — Stress the chart boundary.** Input: P2-C2--P2-C6. Action:
  subdivide the full boundary and search for worst intervals. Acceptance:
  certificate covers closed domains with overlap and no gaps. Output: coverage
  report.

### D. Prove the one-step certificate

- [x] **P2-D1 — Prove nonlinear fiber coercivity.** Input: P2-B4, P2-C3,
  P2-C5, P2-C6. Action: combine linear floor and nonlinear remainder with
  directed bounds. Acceptance: strict positive uniform margin. Output: theorem.
- [x] **P2-D2 — Bound centered retained/fiber coupling.** Input: Stage 22 and
  P2-C3. Acceptance: norm, centering, and retained-state quantifiers are
  explicit. Output: coupling lemma.
- [x] **P2-D3 — Justify differentiation under the fiber integral.** Input:
  P2-D1. Action: provide domination and boundary treatment. Acceptance: first
  and second retained derivatives of the effective action are rigorous.
  Output: analytic lemma.
- [x] **P2-D4 — Derive the effective Hessian identity.** Input: P2-D3. Action:
  express mean Hessian minus covariance and bound both terms. Acceptance: no
  hidden Gaussian assumption in the nonlinear measure. Output: proposition.
- [x] **P2-D5 — Certify generated-interaction bounds.** Input: P2-D1--P2-D4.
  Acceptance: all norm components in the theorem contract close with positive
  margins. Output: result table and certificates.
- [x] **P2-D6 — Prove local-cylinder normalization.** Input: Stages 21 and 23.
  Action: define reference and nonlinear conditional laws on the same event.
  Acceptance: normalization is local and uniform over the declared retained
  set. Output: comparison theorem.
- [x] **P2-D7 — Bound the declared complement.** Input: Stage 42 if used.
  Acceptance: distinguish a restricted reference tail from the full physical
  link measure; state only what is proved. Output: complement lemma or explicit
  open boundary.
- [x] **P2-D8 — Assemble proof dependency graph.** Input: P2-B1--P2-D7.
  Acceptance: every numerical leaf points to a certificate and every analytic
  leaf to a proof. Output: machine-readable DAG.

### E. Novelty and literature audit

- [x] **P2-L1 — Decompose novelty by ingredient.** Action: create rows for
  gauge fixing, Hodge bound, conditional Gaussian, nonlinear chart,
  heat-kernel estimates, marginalization, and integrated certificate.
  Acceptance: no standard lemma is marketed as new. Output: novelty matrix.
- [x] **P2-L2 — Read Balaban's finite-step constructions.** Action: compare
  block variables, localization, small/large fields, generated actions, and
  proof objectives. Acceptance: exact overlap and difference are cited by
  theorem/section. Output: comparison memo.
- [x] **P2-L3 — Search modern computer-assisted QFT proofs.** Action: locate
  interval/exact certification precedents and reproducibility norms.
  Acceptance: paper follows an appropriate proof-artifact standard. Output:
  methods bibliography.
- [x] **P2-L4 — Search lattice Hodge and gauge-fixing certificates.** Action:
  inspect primary sources for finite cubical complexes and relative gauge.
  Acceptance: exact ranks and slice claims are positioned accurately. Output:
  source table.
- [x] **P2-L5 — Search explicit heat-kernel derivative work.** Action: support
  P2-C5 and coordinate with P4 without depending on it. Acceptance: every
  analytic estimate has a baseline. Output: source table.
- [x] **P2-L6 — Freeze contribution statement.** Dependencies: P2-L1--P2-L5.
  Acceptance: novelty is the integrated explicit certificate unless a stronger
  new lemma is demonstrated. Output: contribution paragraph.

### F. Draft, verify, and submit

- [x] **P2-W1 — Draft theorem-first manuscript.** Dependencies: P2-A5,
  P2-D8, P2-L6. Acceptance: all notation is defined once; results do not refer
  to stage files. Output: manuscript source.
- [x] **P2-W2 — Build certificate supplement.** Action: document input hashes,
  exact formats, interval engine, rounding mode, coverage subdivisions, and
  verifier. Acceptance: a clean machine returns a binary pass/fail result.
  Output: supplement archive.
- [x] **P2-V1 — Independent numerical rerun.** Action: use a second interval or
  exact implementation for theorem-critical constants. Acceptance: overlapping
  rigorous enclosures, not matching decimal prints. Output: cross-check log.
- [x] **P2-V2 — Adversarial theorem audit.** Action: test retained-state
  boundary, chart edge, gauge-tree changes, denominator floors, and norm
  conversions. Acceptance: all hostile cases pass or narrow the theorem.
  Output: audit ledger.
- [x] **P2-V3 — Frontier audit.** Action: use `ym-audit-frontier`. Acceptance:
  manuscript never promotes a finite-block eigenvalue to a mass and labels
  RG iteration open. Output: scope report.
- [x] **P2-S1 — Choose venue after certification.** Acceptance: venue values
  explicit finite/computer-assisted results and manuscript fits scope. Output:
  target/fallback memo.
- [x] **P2-S2 — Build submission archive.** Acceptance: manuscript,
  bibliography, certificate supplement, source, license, data/code statement,
  and cover letter are version-locked. Output: submission bundle.

## 7. Stop/go gates

- **G1—Exactness:** stop if any theorem-critical rank, spectral floor, or
  derivative supremum remains an ordinary floating calculation.
- **G2—Integration:** stop if the final theorem is only a list of unrelated
  constants. It must prove an exact one-step mathematical implication.
- **G3—Literature:** reposition as a reproducibility/certificate paper if
  Balaban or later work already proves the same explicit finite theorem.
- **G4—Scope:** any full-measure, volume-uniform, or repeated-RG sentence must
  be proved separately or removed.

## 8. Definition of done

P2 is submission-ready when a reader can state the block theorem without
opening the package, every theorem-critical number has a rigorous enclosure,
the verifier succeeds in a clean environment, the relation to Balaban is
technically explicit, and the paper's conclusion ends at one certified local
marginalization.
