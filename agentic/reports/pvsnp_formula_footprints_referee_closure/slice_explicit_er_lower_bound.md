<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Slice-Explicit Extension-Resolution Lower Bound

- Status: `proved_in_revised_tex`
- TeX definition label: `def:slice-explicit-er`
- TeX corollary label: `cor:slice-explicit-er`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper proves a restricted ER-style proof-size lower bound for explicit acyclic extension refutations whose proof-size measure charges the formula-label boundary of the final backward slice.

A slice-explicit extension refutation consists of an explicit acyclic extension circuit \(C\), its CNF definition \(E_C\), a final CNF \(\Theta\), and a resolution refutation of
\[
  \Phi_{n,s,A}(Y,Z)\wedge E_C(Y,W)\wedge\Theta(Y,W).
\]
If the hard-label extension assignment satisfies \(\Theta\), then the final backward-slice boundary obeys the formula-footprint lower bound.  In the near-threshold regime, any slice-size measure charging the distinct formula-label inputs in that boundary is at least \(2n^{a-o(1)}\).

## Proof Skeleton

1. Apply the final backward-slice lower bound to the final CNF \(\Theta\).
2. Both polarities in the boundary of the final backward slice have size at least \(n^{a-o(1)}\).
3. The two polarity sets are disjoint.
4. The slice-explicit proof-size measure is assumed to charge every distinct formula-label input in the final backward slice.
5. Therefore the slice-explicit proof has size at least \(2n^{a-o(1)}\).

## Nonclaim Boundary

This is not an unrestricted lower bound for extended resolution, Extended Frege, Frege, IPS, or compressed proof systems.  It applies to ER-style proof representations only when the acyclic extension graph is explicit and the proof-size measure charges the final formula-label slice boundary.  If a proof system hides semantic content outside this explicit slice, or does not charge the boundary, this theorem does not apply.

## Gate Impact

This is the current strongest proof-system-facing payoff in the package: it turns the final-slice budget into a restricted ER-style proof-size lower bound.  It remains subordinate to the formula-footprint spine because the entire lower bound is still the statement that completion soundness forces a large formula-label footprint.
