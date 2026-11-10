<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Local Normalization Transfer

- Status: `proved_in_revised_tex`
- TeX theorem: `Support-local normalization transfer`
- TeX label: `thm:support-local-normalization-transfer`
- TeX definition: `Support-local normalization with support budget`
- TeX definition label: `def:support-local-normalizer`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Purpose

This packet records the reusable proof-system transfer theorem.  Earlier resolution theorems prove concrete support-local cases.  This theorem abstracts the common mechanism: any proof system that normalizes accepted proofs into support-local constraints with a controlled support budget inherits the formula-footprint lower bound.

## Statement

Fix an easy-completion CNF \(\Phi_{n,s,A}\) and a hard formula labeling \(\lambda\).  Suppose a proof or certificate system \(\mathcal P\) has a support-local normalization with support budget \(B\): every accepted proof \(\pi\) yields a support set \(S_\pi\), a support-local CNF \(\Gamma_\pi(Y,W)\), a sound refutation of \(\Phi_{n,s,A}\wedge\Gamma_\pi\), and \(|S_\pi|\le B(|\pi|)\).

Then each polarity subset of \(S_\pi\) satisfies the formula-footprint lower inequalities.  In the near-threshold regime:

- \(|S_{\pi,0}|,|S_{\pi,1}|\ge n^{a-o(1)}\);
- \(B(|\pi|)\ge 2n^{a-o(1)}\);
- if \(B(L)=O(L)\), every accepted proof has length \(n^{a-o(1)}\).

## Proof Idea

The sound refutation makes \(\Phi\wedge\Gamma_\pi\) unsatisfiable.  Support-locality says that every completion preserving \(S_\pi\) can satisfy \(\Gamma_\pi\).  If such a completion were easy, the easy-completion CNF would supply a satisfying witness for \(\Phi\), contradicting unsatisfiability.  Hence \(S_\pi\) is a completion-sound certificate, and the formula-footprint theorem applies.

## Boundary

This is a conditional transfer theorem, not a Frege, Extended Frege, IPS, or unrestricted resolution lower bound.  A concrete proof-system theorem must still construct the support-local normalizer and prove the support budget.

## Gate Impact

This strengthens `C5` by turning the proof-system route into a precise reusable theorem.  The remaining top-paper blocker is now sharply localized: instantiate the normalizer for a less local recognizable proof system, or prove an explicit SAT-family/source lower-bound theorem.
