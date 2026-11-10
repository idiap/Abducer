<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Audited LRAT Trace Normalizer

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:support-audited-lrat`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper now gives a checkable-trace version of the support-declaration route.

Suppose an LRAT-style clausal trace certifies unsatisfiability of
\[
  \Phi_{n,s,A}(Y,Z)\wedge\Gamma_\tau(Y,W),
\]
and the trace carries a support audit with a declared formula-label support \(S_\tau\).  If the audit proves that for every formula labeling \(\mu\) agreeing with the hard labeling \(\lambda\) on \(S_\tau\), some auxiliary assignment satisfies \(\Gamma_\tau(\mu,W)\), then \(S_\tau\) is a completion-sound formula-label certificate.

Therefore, for each polarity \(b\),
\[
  g_n+c\mathrm{Lookup}(M_n,|S_{\tau,b}|,\ell_n)+cM_n>s.
\]

Near threshold,
\[
  |S_{\tau,0}|,|S_{\tau,1}|\ge n^{a-o(1)}.
\]

If the trace size or checker-visible annotation size bounds the declared support by \(|S_\tau|\le B(|\tau|)\), then
\[
  B(|\tau|)\ge 2n^{a-o(1)}.
\]

## Proof Skeleton

1. LRAT soundness turns the accepted trace into an actual clausal refutation.
2. The support audit says \(\Gamma_\tau\) is support-local at \(\lambda\) over \(S_\tau\).
3. Apply the support-local auxiliary-resolution theorem.
4. Use the formula-footprint theorem and near-threshold corollary.
5. Convert the two polarity lower bounds into a support-budget lower bound.

## Nonclaim Boundary

This is not a lower bound for arbitrary LRAT, DRAT, Frege, Extended Frege, IPS, implicit proofs, or proof traces without a sound support audit.  It applies to checkable clausal traces only when the trace or an independently verified annotation proves the completion-stable support invariant.

## Gate Impact

This is a C11-admitted proof-system bridge.  It makes the support-declaration route more recognizable by moving from abstract macro support to a verifier-facing LRAT-style trace object, while preserving the same nonclaim boundary: support must be soundly audited, not merely named.
