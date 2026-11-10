---
name: ym-draft-heat-kernel-enclosures
description: Develop a rigorous technical note on explicit SU(2) heat-kernel log-derivative, curvature, higher-derivative, normalization, and tail enclosures for lattice-gauge applications. Use to fix conventions, derive analytic image-series remainders, replace sampled numerical bounds with interval certificates, compare constants with existing heat-kernel literature, and decide whether the result is standalone or should be an appendix to a finite-block paper.
---

# Draft the SU(2) Heat-Kernel Enclosure Paper

## Freeze conventions

Declare the metric on SU(2), Haar normalization, class angle, radial measure, Laplacian sign, heat generator, time variable, and cut-locus treatment before stating constants. Maintain a conversion table for alternative conventions in the literature.

## Build the theorem family

1. Derive the character and Poisson-image formulas and prove their equivalence on the required domain.
2. Isolate the principal image and bound all remaining images analytically.
3. Enclose the kernel away from zero before dividing to obtain log derivatives.
4. Prove uniform bounds for the first three derivatives, radial Hessian eigenvalues, and any higher order needed by the intended application.
5. Treat the identity by removable limits and the cut locus by a separate chart or symmetry argument.
6. Derive normalized Haar tail bounds with explicit numerator and denominator enclosures.
7. Supply small-time asymptotics with quantified remainders, not only leading rates.
8. If possible, parameterize derivative order or extend the method to SU(N); otherwise explain why the SU(2) constants solve a recognized downstream problem.

## Numerical rigor

- Use directed-rounding interval arithmetic or symbolic inequalities.
- Prove truncation errors and denominator separation.
- Cover the full domain by verified interval subdivision; do not infer suprema from sampling.
- Emit independently checkable certificate data and verify overlap between subintervals.
- Cross-check character and image expansions in their common stable regime.

## Publication gate

Conduct a primary-source novelty search for heat-kernel actions, compact Lie-group heat-kernel estimates, derivative estimates, and computer-assisted enclosures. Keep the work standalone only if it offers a reusable theorem family, materially sharper explicit constants, an extension beyond existing results, or closure of a recognized constructive estimate. Otherwise prepare it as the analytic appendix of the finite-block paper.

## Manuscript production workflow

Run the specialist skills in this order:

1. Use `ym-develop-paper-proofs` to close the character/image equivalence, derivative remainders, denominator separation, endpoint regimes, and normalized-tail theorem.
2. Use `ym-ground-paper-literature` to compare theorem form, derivative order, domain, constants, and certification with compact-group heat-kernel and lattice-action sources.
3. Apply the standalone publication gate; then use `ym-frame-paper-narrative` either for a technical note or for a major analytic section of the finite-block paper.
4. Use `ym-build-proof-appendix` for image-tail calculations, interval subdivisions, certificate schema, and independent verification.
5. Use `ym-build-latex-paper` to assemble the chosen form, lint all conventions and references, compile, render, and inspect the PDF.
6. Run `ym-audit-frontier` on downstream physics claims before the final build.

## Output contract

Produce a convention-complete manuscript, theorem table, analytic remainder proofs, interval verifier, certificate dataset, benchmark comparison, reproducibility guide, compiled PDF, preview pages, and build report. State no continuum or mass-gap consequence beyond the exact downstream corollary proved.
