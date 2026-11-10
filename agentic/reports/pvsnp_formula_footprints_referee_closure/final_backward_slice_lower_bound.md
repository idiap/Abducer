<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Final Backward-Slice Lower Bound

- Status: `proved_in_revised_tex`
- TeX label: `cor:final-backward-slice`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper proves the proof-object budget form of the canonical syntactic-cone normalizer.  For an explicit acyclic extension circuit \(C\) and final CNF \(\Theta\), let \(\operatorname{Slice}_C(\Theta)\) be the backward slice of the extension-definition graph reaching variables in \(\Theta\).  Its formula-label boundary is the set of labels \(Y_u\) occurring in that slice.

If the hard-label extension assignment satisfies \(\Theta\), and
\[
  \Phi_{n,s,A}(Y,Z)\wedge E_C(Y,W)\wedge\Theta(Y,W)
\]
has a resolution refutation, then the label boundary of the final backward slice is a completion-sound formula-label certificate.  Therefore both polarities in that boundary obey the formula-footprint lower bound, and in the near-threshold regime each polarity has size at least \(n^{a-o(1)}\).

## Proof Skeleton

1. The formula-label boundary of the final backward slice is exactly the canonical syntactic-cone support \(S^{\mathrm{syn}}_\Theta\).
2. Apply the canonical syntactic-cone normalizer.
3. Use the formula-footprint theorem to obtain the two polarity lower bounds.
4. Since the two polarity subsets are disjoint, any explicit proof representation counting distinct formula-label inputs in the final backward slice has length at least \(2n^{a-o(1)}\).

## Nonclaim Boundary

This is not an unrestricted lower bound for extended resolution, Extended Frege, Frege, IPS, or implicit proofs.  It proves that an explicit acyclic extension proof cannot end in a small local backward slice.  A stronger proof system can still escape if it compresses semantic information outside such an acyclic label-dependency slice, or if the final backward slice is already large.

## Gate Impact

This strengthens the proof-system route because it converts the canonical cone normalizer into an auditable proof-object budget: the final extension slice must visibly contain near-threshold many formula-label inputs of both polarities.  It remains subordinate to the formula-footprint spine and does not create a separate result package.
