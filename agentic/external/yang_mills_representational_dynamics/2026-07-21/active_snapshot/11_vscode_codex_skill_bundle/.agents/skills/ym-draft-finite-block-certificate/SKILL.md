---
name: ym-draft-finite-block-certificate
description: Assemble and rigorously certify a standalone paper on an explicit finite SU(2) lattice-gauge quotient--fiber block and one-step nonlinear marginalization. Use to merge cubical ranks, gauge slicing, Hodge coercivity, heat-kernel derivative bounds, local chart geometry, and effective-action estimates into one theorem while replacing floating-point evidence with interval or exact certificates and positioning the result against constructive renormalization-group literature.
---

# Draft the Verified Finite-Block Certificate Paper

## Freeze one block theorem

Define the cubical block, boundary convention, gauge group, link and plaquette spaces, gauge quotient, retained map, fiber, chart, heat time, radii, norms, and effective action in one notation table. State a single theorem whose conclusions include only the properties proved on that block.

Classify the result as a restricted finite-block certificate. Never call a finite coercivity eigenvalue a physical mass or infer RG iteration, a continuum measure, Osterwalder--Schrader reconstruction, or a mass gap.

## Integrate the proof

1. Prove cochain and retained-map ranks exactly.
2. Define the relative gauge fixing and show Haar/Jacobian accounting.
3. Prove the quotient/fiber Hodge lower bound with a certified spectral enclosure.
4. Derive centered Gaussian fiber cancellation and the retained response formula.
5. Define the nonlinear plaquette chart and prove injectivity or bi-Lipschitz bounds on the declared domain.
6. Insert explicit SU(2) heat-kernel derivative enclosures with consistent Laplacian normalization.
7. Prove strong log-concavity of the conditional fiber and bound generated retained interactions after exact marginalization.
8. State the local-cylinder normalization and defect/complement estimate with all retained-state quantifiers visible.

## Certification policy

- Use exact integer arithmetic for topology and ranks.
- Replace raw `svd`, `eigvalsh`, pseudoinverses, floating root searches, and sampled suprema with rational, interval, or theorem-backed enclosures.
- Make scripts emit inputs, directed-rounding bounds, environment metadata, and a pass/fail certificate.
- Separate theorem-critical constants from exploratory calibrations.
- Re-run hostile tests at chart boundaries and under orientation or gauge-tree changes.

## Literature and positioning

Compare each ingredient with primary constructive RG work, especially small-field effective actions, cluster expansions, large-field operations, gauge propagators, and heat-kernel lattice actions. Claim novelty only for the integrated, explicit, machine-checkable finite certificate or for a genuinely new lemma established by the audit.

## Manuscript production workflow

Run the specialist skills in this order:

1. Use `ym-develop-paper-proofs` to consolidate the exact topology, certified spectra, nonlinear chart, heat-kernel inputs, fiber coercivity, and one-step marginalization into one theorem DAG.
2. Use `ym-ground-paper-literature` to compare every ingredient and the integrated certificate with Balaban and later constructive or computer-assisted work.
3. Use `ym-frame-paper-narrative` to explain why an explicit verified block is useful, state one central contribution, and keep repeated RG and the mass gap outside the claim.
4. Use `ym-build-proof-appendix` for matrix definitions, exact-rank certificates, interval coverage, derivative enclosures, and reproducibility details.
5. Use `ym-build-latex-paper` to assemble, lint, compile, render, and verify the manuscript and certificate supplement.
6. Run `ym-audit-frontier` on the compiled PDF and rebuild after correction.

## Output contract

Produce a self-contained manuscript, interval-certificate appendix, executable verifier, machine-readable theorem graph, exact parameter registry, literature comparison matrix, reproducibility instructions, compiled PDF, preview pages, and build report. Run `ym-audit-frontier` before submission.
