<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Resolution Local-Clause Support

- Status: `proved_in_revised_tex`
- TeX theorem: `Resolution local-clause support`
- TeX label: `thm:resolution-local-clause-support`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Purpose

This packet records the broader restricted-resolution bridge added after the unit-core corollary.  The theorem no longer requires the proof to expose unit label assumptions.  It applies to any resolution refutation of the easy-completion CNF together with faithful clauses over formula-label variables, and lower-bounds the distinct label support of those clauses.

## Statement

Let \(\lambda\) be a hard formula labeling and let \(\Gamma\) be a CNF over formula-label variables only, with \(\lambda\models\Gamma\).  If there is a resolution refutation of
\[
  \Phi_{n,s,A}(Y,Z)\wedge\Gamma,
\]
then the set \(S_\Gamma\) of label variables occurring in \(\Gamma\) is a completion-sound formula-label \(1\)-certificate at \(\lambda\).  Therefore both polarity supports \(S_{\Gamma,0}\) and \(S_{\Gamma,1}\) satisfy the formula-footprint lower inequalities, and in the near-threshold regime each has size \(n^{a-o(1)}\).

## Proof Idea

Any labeling \(\mu\) agreeing with \(\lambda\) on the support of \(\Gamma\) also satisfies \(\Gamma\), since \(\Gamma\) contains only those label variables and \(\lambda\) satisfies it.  If such a \(\mu\) were easy, the easy-completion CNF would have satisfying auxiliary witnesses, contradicting the resolution refutation.  Hence the support assignment is a \(1\)-certificate and the formula-footprint theorem applies.

## Boundary

The theorem applies to explicit local clauses over formula-label variables.  It does not handle encodings that mix label variables with auxiliary variables in a way that hides semantic information outside a fixed label support.  Those encodings remain the target for a stronger normalization theorem.

## Gate Impact

This strengthens the proof-system route from explicit units to explicit local clauses.  It improves `C5` and `C10`, but the top-paper blocker remains: normalize a stronger or less local proof system, or prove an explicit SAT-family/source lower-bound theorem.
