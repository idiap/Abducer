<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Local Extension Resolution

- Status: `proved_in_revised_tex`
- TeX theorem: `Support-local extension resolution`
- TeX label: `thm:support-local-extension-resolution`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Theorem Summary

The revised paper proves a restricted extended-resolution-style instantiation of the support-local bridge.  An acyclic extension circuit may introduce auxiliary variables, but its inputs must be formula-label variables inside a fixed support \(S\).  If the final extension clauses are satisfied by the extension values induced by the hard labeling on \(S\), then every completion preserving \(\lambda|_S\) also satisfies the extension package.

Consequently, a resolution refutation of the easy-completion CNF together with this extension package turns \(\lambda|_S\) into a completion-sound formula-label certificate.  The formula-footprint barrier then lower-bounds both polarity parts of \(S\), and in the near-threshold regime each polarity support has size \(n^{a-o(1)}\).

## Proof Object

- Proof system scope: resolution over an easy-completion CNF plus support-local extension definitions.
- Extension object: acyclic Boolean extension circuit whose inputs are exactly formula-label variables from a fixed support.
- Measured object: fixed formula-label support driving acyclic extension definitions and final extension clauses.
- Consequence: lower bound on both polarity supports whenever such a refutation exists.

## Boundary

This is not a lower bound for unrestricted Extended Frege, unrestricted extended resolution, IPS, or proof systems whose extension variables encode nonlocal information about unexposed labels.  It proves the next coherent restricted case: extension variables are allowed, but only when their semantic content is already determined by the exposed support.

## Gate Impact

This strengthens `C5` without weakening `C11`: the new theorem does not create a competing result.  It extends the same completion-soundness spine from explicit support-local auxiliary clauses to ER-style local extension definitions.
