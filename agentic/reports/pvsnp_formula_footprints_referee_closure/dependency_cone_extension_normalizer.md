<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dependency-Cone Extension Normalizer

- Status: `proved_in_revised_tex`
- TeX definition: `Dependency-cone extension package`
- TeX definition label: `def:dependency-cone-extension`
- TeX theorem: `Dependency-cone extension normalizer`
- TeX theorem label: `thm:dependency-cone-extension-normalizer`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Theorem Summary

The revised paper proves that an ER-style extension package becomes support-local when every extension variable carries a syntactic cone of formula labels that upper-bounds its dependencies.  The final contradiction may mention nested extension variables, but the support extracted from the proof object is the union of the declared cones of variables appearing in the final clauses.

If a resolution refutation uses the easy-completion CNF, the extension-definition CNF, and final clauses whose evaluated extension assignment is true under the hard labeling, then the final cone union is a completion-sound formula-label certificate.  The formula-footprint theorem lower-bounds both polarity parts of that cone union.

## Proof Object

- Proof system scope: cone-annotated extension resolution over an easy-completion CNF.
- Normalizer output: declared final support \(S_\Theta\), obtained as the union of syntactic dependency cones of final label and extension variables.
- Measured object: union of declared formula-label dependency cones for final extension contradiction.
- Consequence: if \(|S_\Theta|\le B(|\pi|)\), the proof has a support-local normalization with budget \(B\).

## Boundary

This is not an unrestricted extended-resolution, Extended Frege, Frege, or IPS lower bound.  The theorem requires dependency cones to be part of the auditable proof object.  Extension variables that hide nonlocal semantic dependencies remain outside the proved scope.

## Gate Impact

This strengthens `C5` more than the fixed-support extension theorem because it supplies a syntactic normalizer: the support is extracted from cone annotations rather than chosen in advance.  It also preserves `C11`, since the theorem is still subordinate to the same formula-footprint spine and explains exactly how a proof object must expose local semantic content.
