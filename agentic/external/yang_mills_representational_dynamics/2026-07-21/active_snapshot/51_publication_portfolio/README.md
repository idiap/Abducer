# Five-paper publication portfolio

Date: 21 July 2026

This directory converts the package-wide novelty review into five independent
publication work packages. Independence means that each plan has its own
claim, source corpus, proof obligations, literature audit, manuscript outline,
verification gates, deliverables, and stop/go decision. No paper needs another
paper in this portfolio to be accepted first.

The portfolio is not a claim of four publishable papers today. It is a
controlled route to test four candidates. Papers 1--3 have credible distinct
identities. Paper 4 is intentionally conditional: it becomes standalone only
if its enclosure theorem clears the novelty gate; otherwise its output becomes
an analytic appendix to Paper 2.

## Portfolio map

| ID | Candidate | Current level | Publication thesis | Initial decision |
|---|---|---:|---|---|
| P1 | Frustrated conditioning | C2 | A physically admissible frustrated boundary invalidates worst-conditioning rare-defect domination at weak coupling | **Implemented; submission candidate** |
| P2 | Exact quotient--fiber block | C2 | A finite four-dimensional `SU(2)` block admits an exact tree-gauge quotient, certified local action, and one controlled marginalization | **Implemented; submission candidate** |
| P3 | Representational dynamics | C3 conditional abstract transfer; C0 YM application | A dense recovered Euclidean core with one uniform rate transports spectral rigidity; typed countermodels expose missing completeness and uniformity | **Implemented; submission candidate** |
| P4 | Heat-kernel enclosures | C2 | An arbitrary requested finite derivative order admits explicit paired-image, log-action, endpoint, and normalized-tail enclosures | **Implemented; submission candidate** |
| P5 | Staple dispersion and spillover | C2 | Gauge-covariant Fréchet dispersion is residual link energy, and every centered star displacement has a strictly positive exact spill cost on the test block | **Implemented; hold for external novelty review** |

Claim levels use the package convention: `C0` conceptual, `C1`
computational, `C2` restricted rigorous theorem, and higher levels only for
uniform constructive or continuum achievements. None of these papers is a
Clay-level claim.

## Independent plans

1. [P1: Frustrated boundary conditions](paper_01_frustrated_conditioning_plan.md)
2. [P2: Verified nonlinear quotient--fiber block](paper_02_verified_finite_block_plan.md)
3. [P3: Proof-bearing representational dynamics](paper_03_representational_dynamics_plan.md)
4. [P4: Explicit `SU(2)` heat-kernel enclosures](paper_04_heat_kernel_enclosures_plan.md)
5. [P5: Gauge-covariant staple dispersion and spillover](paper_05_staple_dispersion_plan.md)

The machine-readable [plan registry](plan_registry.json) records source files,
todo counts, skill names, and the fact that cross-paper dependencies are empty.
Run `python3 validate_publication_plans.py` in this directory to verify the
portfolio structure.

The [manuscript automation workflow](MANUSCRIPT_AUTOMATION.md) defines the
shared skills for motivation and introduction, literature grounding, proof
development, proof appendices, and automated LaTeX/PDF production.

Paper 01 is now implemented end to end in
[`paper_01_frustrated_conditioning/`](paper_01_frustrated_conditioning/README.md).
Its blinded manuscript is 21 pages, all 32 plan todos are closed, the exact
incidence supplement passes, and the final frontier level remains `C2`.
The portable submission archive is
`paper_01_frustrated_conditioning_submission.zip` (59 entries; SHA-256
`8378447fcce94db53fb2ac095eb6cb8cdc8b45d241bccc9eba65c4bd0b6d2dab`).

Paper 02 is now implemented end to end in
[`paper_02_verified_finite_block/`](paper_02_verified_finite_block/README.md).
Its blinded manuscript is 18 pages, all 39 plan todos are closed, two
independent exact certificate kernels pass, and the final claim level is `C2`.
The theorem uses rooted tree gauge for exact Haar accounting and proves one
local-cylinder marginalization; the interacting complement and repeated RG
remain open.
The portable submission archive is
`paper_02_verified_finite_block_submission.zip` (68 entries; SHA-256
`9a4bbd51a405e1b58326b12ab5caa74fd0482c9ddff17906a70c1d31927c1e72`).

Paper 03 is now implemented end to end in
[`paper_03_representational_dynamics/`](paper_03_representational_dynamics/README.md).
Its blinded manuscript is 27 pages and all 40 plan todos are closed. The
central theorem transports an index-independent Euclidean semigroup rate on a
dense centered recovered core into target spectral exclusion. Exact
countermodels show why completeness, a common rate, and limit-order control
are indispensable. The Yang--Mills application remains methodological and
conditional: no continuum theory or physical mass gap is constructed.
The portable submission archive is
`paper_03_representational_dynamics_submission.zip` (87 entries; SHA-256
`c75a32efe640a9ec6e2ce3d44e18c3a99680189f9e7abc4838a2ca49c8d7d79a`).

Paper 04 is now implemented end to end in
[`paper_04_heat_kernel_enclosures/`](paper_04_heat_kernel_enclosures/README.md).
Its 13-page technical note closes all 42 plan todos. The standalone gate is
passed by an arbitrary requested finite derivative-order theorem with explicit
computable constants. An exact-rational order-eight certificate, a distinct
verifier, 17 hostile tests, and identity/transition/cut-locus charts accompany
the paper. The result is `C2` and local: it does not control an interacting
four-dimensional plaquette marginal, repeated RG, the continuum, or a mass
gap. The portable archive and checksum are stored beside the manuscript.
The archive has 80 entries and SHA-256
`b7d59e11cc295cf824668f6866641ab011af45ebb82d397cb73777f598167a8b`.

Paper 05 is implemented end to end in
[`paper_05_staple_dispersion/`](paper_05_staple_dispersion/README.md).  Its
15-page manuscript closes all 40 plan todos.  A material orientation audit
corrected the exploratory signed-row centering: the exact centered Gaussian
spectrum is `0, 239/630 (x2), 33/70 (x3)`, and the minimum-spill spectrum is
strictly positive, `37/33 (x3), 391/239 (x2)`.  Rational projection and KKT
identities verify all eight interior links.  The theorem is `C2`; submission
is held for an external expert novelty review.  The portable archive has 68
entries and SHA-256
`b1b24d3fbd2c52214d4c90e29e28c7e1b60b34922e36f242d12baed3f1901b67`.

## Shared epistemic rules

- Put one new result in each abstract and title.
- Distinguish analytic proof, exact computation, interval-certified
  computation, exploratory floating-point evidence, and conjecture.
- Treat automated tests as reproducibility evidence, never as a substitute for
  a mathematical proof.
- Search primary literature and citation chains before using “new”, “first”,
  or “previously unknown”.
- Remove stage numbers, pipeline narration, and retrospective task language
  from submitted manuscripts.
- State every cutoff, volume, boundary, gauge-group, heat-time, and retained
  state quantifier.
- Describe the Clay problem as motivation only. Do not imply basin entry,
  repeated RG, continuum construction, Osterwalder--Schrader reconstruction,
  or a mass gap.
- Archive code, certificates, parameter registries, and theorem-dependency
  graphs alongside the manuscript version that uses them.

## Reusable drafting skills

The portable skill bundle contains one workflow for each plan:

- `ym-draft-frustration-obstruction`
- `ym-draft-finite-block-certificate`
- `ym-draft-representational-dynamics`
- `ym-draft-heat-kernel-enclosures`
- `ym-draft-staple-dispersion`

The five orchestrators use five shared publication skills:

- `ym-frame-paper-narrative`
- `ym-ground-paper-literature`
- `ym-develop-paper-proofs`
- `ym-build-proof-appendix`
- `ym-build-latex-paper`

Each can be invoked independently in a VS Code Codex workspace. Every paper
should also finish with `ym-audit-frontier`.

## Portfolio-level decision rule

Do not submit two papers whose novelty statements depend on the same theorem.
If P4 fails its standalone gate, merge its proved enclosures into P2 and count
the result as one stronger paper. If P3 cannot produce a nontrivial formal
result beyond additive errors and Boolean certificate conjunction, recast it
as a philosophy paper centered on epistemic methodology rather than presenting
the calculus as new mathematics.
