<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Local Auxiliary Resolution

- Status: `proved_in_revised_tex`
- TeX theorem: `Support-local auxiliary resolution`
- TeX label: `thm:support-local-aux-resolution`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Purpose

This packet records the next restricted proof-system bridge after explicit local resolution clauses.  The theorem allows auxiliary variables and mixed clauses, but requires a support-locality invariant: once a fixed label support agrees with the hard labeling, the auxiliary constraints remain satisfiable for every completion of all other labels.

## Statement

Let \(\lambda\) be a hard formula labeling and let \(\Gamma(Y,W)\) be a CNF over formula-label variables \(Y\) and auxiliary variables \(W\).  Suppose there is a support set \(S\) such that every labeling \(\mu\) agreeing with \(\lambda\) on \(S\) has some auxiliary assignment \(w\) satisfying \(\Gamma(\mu,w)\).  If there is a resolution refutation of
\[
  \Phi_{n,s,A}(Y,Z)\wedge\Gamma(Y,W),
\]
then \(\lambda|_S\) is a completion-sound formula-label \(1\)-certificate.  Hence both polarity subsets of \(S\) satisfy the formula-footprint lower inequalities, and in the near-threshold regime each has size \(n^{a-o(1)}\).

## Proof Idea

For any completion \(\mu\) preserving \(S\), support-locality supplies \(w\) satisfying \(\Gamma\).  If \(\mu\) were easy, the easy-completion CNF would supply \(z\) satisfying \(\Phi\).  This would satisfy the whole refuted CNF, contradicting resolution soundness.  Therefore every completion preserving \(S\) is hard, so \(S\) is a certificate.

## Boundary

This theorem does not handle arbitrary auxiliary encodings.  If auxiliary variables encode global information about unexposed labels, support-locality may fail.  Proving support-local normalization for a natural stronger proof system remains the next proof-system blocker.

## Gate Impact

This strengthens `C5` from explicit-local resolution to support-local auxiliary resolution.  The paper is still not top-ready: it still needs a less local recognizable proof-system normalization theorem, or an explicit SAT-family/source lower-bound theorem.
