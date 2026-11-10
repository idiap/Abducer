<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Canonical Syntactic-Cone Normalizer

- Status: `proved_in_revised_tex`
- TeX label: `cor:canonical-syntactic-cone`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper proves that separate dependency-cone annotations are not required for ordinary acyclic extension definitions.  Given an explicit extension circuit \(C\), the canonical syntactic cone of each extension variable is obtained by graph reachability back to formula-label inputs.  The final support is the union of the canonical cones of variables occurring in the final CNF \(\Theta\).

If the extension assignment induced by the hard labeling satisfies \(\Theta\), and
\[
  \Phi_{n,s,A}(Y,Z)\wedge E_C(Y,W)\wedge\Theta(Y,W)
\]
has a resolution refutation, then the final canonical syntactic-cone support is a completion-sound formula-label certificate.  Consequently, each polarity in that support obeys the formula-footprint lower bound, and in the near-threshold regime both polarities have size at least \(n^{a-o(1)}\).

## Proof Skeleton

1. Define \(\operatorname{Syn}_C(Y_u)=\{u\}\) for label variables.
2. Define \(\operatorname{Syn}_C(w)\) as the union of the canonical cones of the inputs to the extension definition of \(w\).
3. Observe that these canonical cones form a valid dependency-cone annotation.
4. Apply the dependency-cone extension normalizer theorem.
5. Read off the support-local normalization budget from the final syntactic-cone support.

## Nonclaim Boundary

This is not an unrestricted lower bound for extended resolution, Extended Frege, Frege, IPS, or implicit proof systems.  It removes the need for external cone annotations, but a nontrivial proof-size consequence still requires a bound on the final canonical syntactic-cone support.  If the final contradiction mentions extension variables with huge syntactic cones, the resulting lower bound may be vacuous.

## Gate Impact

This advances the proof-system route because the normalizer is now extracted from ordinary acyclic extension syntax rather than from a separate proof-object annotation.  It strengthens the cohered formula-footprint spine without adding an independent payoff: local semantic content still has to appear as exposed formula-label support, now measured by syntactic reachability in the extension graph.
