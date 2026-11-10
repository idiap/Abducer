<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Displayed Acyclic ER Length Lower Bound

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:displayed-er-length`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper removes the separate slice-size charging convention for explicitly displayed acyclic extension refutations.

If a slice-explicit extension refutation writes the extension definitions \(E_C\) and final CNF \(\Theta\) as ordinary displayed clauses, with operand variables written explicitly, then every formula-label input in the final backward slice appears as at least one displayed literal in \(E_C\cup\Theta\).  Therefore ordinary displayed extension-object length lower-bounds the final slice boundary.

In the near-threshold regime, the displayed length is at least
\[
  2n^{a-o(1)}.
\]

## Proof Skeleton

1. Apply the final backward-slice lower bound.
2. The final slice contains at least \(n^{a-o(1)}\) labels of each polarity.
3. If a label input is in the final backward slice, it either appears directly in \(\Theta\) or appears as an explicitly written operand in the first extension definition on a path to \(\Theta\).
4. Thus each distinct label in the slice contributes at least one literal occurrence to the displayed extension object.
5. The two polarity sets are disjoint, so displayed length is at least \(2n^{a-o(1)}\).

## Nonclaim Boundary

This is not a lower bound for Frege, Extended Frege, IPS, implicit proofs, compressed proof formats, or unrestricted ER encodings whose effective dependency support is not visible in displayed acyclic extension clauses.  The result applies to displayed acyclic ER-style proof objects.

## Gate Impact

This strengthens the C11 proof-system route: the paper no longer needs a special proof-size convention for explicit acyclic extension objects.  The next bridge is the expansion-bounded compressed ER transfer; the remaining top-paper blocker is to prove controlled expansion/support for a stronger proof system or supply an explicit SAT-family/source lower-bound theorem.
