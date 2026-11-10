<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Resolution Unit-Core Lower Bound

- Status: `proved_in_revised_tex`
- TeX corollary: `Resolution unit-core lower bound`
- TeX label: `cor:resolution-unit-core`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Purpose

This packet records the upgrade from a preselected explicit-assumption resolution theorem to a more natural full-assignment resolution support statement.  Instead of choosing a small assumption set in advance, the corollary applies to any resolution refutation of the easy-completion CNF together with the full hard labeling, and lower-bounds the distinct faithful label-unit leaves actually used by the proof.

## Statement

Let \(\lambda\) be a hard formula labeling and let \(\Lambda_\lambda\) be the full set of unit clauses \(Y_u=\lambda(u)\).  For any resolution refutation \(\Pi\) of
\[
  \Phi_{n,s,A}(Y,Z)\wedge\Lambda_\lambda,
\]
let \(T_\Pi\) be the set of formula-label units from \(\Lambda_\lambda\) used as initial clauses in \(\Pi\).  Then the two polarity classes \(T_{\Pi,0}\) and \(T_{\Pi,1}\) satisfy the same formula-footprint lower inequalities as ordinary completion-sound certificates.  In the near-threshold regime, each polarity has size \(n^{a-o(1)}\).

## Proof Idea

Delete every unused full-assignment unit from the proof.  The remaining used unit core is still a resolution refutation of the easy-completion CNF plus a faithful explicit assumption set.  The assumption-resolution theorem applies to that core.

## Boundary

This is stronger than the preselected-assumption theorem, but still local.  It lower-bounds explicit faithful label-unit leaves used by full-assignment resolution refutations.  It does not lower-bound resolution derivations that encode the labeling nonlocally, nor Frege, Extended Frege, IPS, or implicit proof systems.

## Gate Impact

The paper now has two named restricted resolution consequences: explicit assumptions and used-unit cores of full-assignment refutations.  This strengthens `C5` and `C10`, but the top-paper blocker remains: normalize a stronger or less local proof system, or prove an explicit SAT-family/source lower-bound theorem.
