---
name: ym-draft-frustration-obstruction
description: Develop a standalone mathematical-physics paper from a frustrated-boundary or worst-conditioning obstruction in weak-coupling lattice gauge theory. Use to freeze the exact conditional theorem, generalize the SU(2) center construction, audit Dobrushin or defect-domination consequences, distinguish an obstruction from a Yang--Mills construction, and produce a submission-ready proof and reproducibility supplement.
---

# Draft the Frustration Obstruction Paper

## Freeze the claim

State one theorem before drafting prose. Specify the lattice, dimension, compact group, central element, heat-kernel normalization, incident-plaquette count, admissible boundary assignment, conditional law, event, and every limit. Label finite computation separately from analytic proof.

Treat the result as an obstruction to a proof mechanism. Never claim basin entry, continuum Yang--Mills, confinement, or a mass gap.

## Build the paper

1. Reprove the finite center-staple realization without relying on code.
2. Derive the conditional density and its small-time rate function.
3. Generalize from six staples in four dimensions to `m=2(d-1)` staples where the geometry permits.
4. For a compact group and central element `z`, formulate the geodesic energy minimization
   \[
   (m-1)d(I,U)^2+d(z,U)^2.
   \]
   State uniqueness only under verified injectivity and geodesic hypotheses.
5. Prove the bad-event concentration and, when justified, asymptotic separation of coherent and frustrated conditional laws.
6. Derive the exact consequence for the proposed uniform conditional or Dobrushin estimate. Do not overstate consequences for unrelated contour methods.
7. Prove positive-measure stability of the boundary perturbation.
8. Compare the theorem against primary literature on weak-coupling lattice gauge theory, heat-kernel actions, boundary-condition sensitivity, Dobrushin methods, center flux, and constructive renormalization.

## Verification gates

- Replace stage labels and programme language with self-contained definitions.
- Keep exact ranks or incidence claims symbolic or independently machine-certified.
- Make every numerical value dispensable to the theorem; move diagnostics to a supplement.
- Test degenerate cases: trivial center, nonunique minimizing geodesics, cut loci, different frustrated multiplicities, and low dimension.
- Include a claim table with `proved`, `computed`, `conjectural`, and `not claimed` rows.
- Run `ym-audit-frontier` before freezing the title and abstract.

## Manuscript production workflow

Run the specialist skills in this order:

1. Use `ym-develop-paper-proofs` to freeze and close the dimension-`d` theorem, positive-measure stability, and any compact-group extension.
2. Use `ym-ground-paper-literature` to audit the exact conditional-concentration and Dobrushin consequence against center-flux, boundary-condition, heat-kernel, and constructive-RG sources.
3. Use `ym-frame-paper-narrative` to write the motivation, abstract, introduction, contribution statement, and conclusion from the proved obstruction—not from the research chronology.
4. Use `ym-build-proof-appendix` for incidence certificates, uniform heat-kernel asymptotics, stability estimates, and optional generalizations.
5. Use `ym-build-latex-paper` to scaffold or assemble the modular source, lint it, compile with `latexmk`, render PDF previews, and emit the build report.
6. Run `ym-audit-frontier` on the compiled manuscript and repeat the build after every material correction.

## Output contract

Produce a manuscript source, bibliography, theorem dependency map, proof-obligation ledger, reproducibility supplement, referee-facing novelty statement, compiled PDF, preview pages, and machine-readable build report. The abstract must name the invalidated quantifier and the replacement strategies left open.
