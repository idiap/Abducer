<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Assumption-Resolution Instantiation

- Status: `proved_in_revised_tex`
- TeX theorem: `Resolution with explicit label assumptions`
- TeX label: `thm:assumption-resolution`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Purpose

This packet records the first named proof-system instantiation in the revised paper.  It is deliberately restricted: the theorem applies to resolution refutations of an easy-completion CNF when faithful formula-label assumptions are explicitly listed and counted as part of the proof object.

## Theorem Content

Given a hard formula labeling \(\lambda\), an easy-completion CNF \(\Phi_{n,s,A}\), and a resolution refutation of \(\Phi_{n,s,A}\wedge\Gamma\), where \(\Gamma\) consists of faithful unit assumptions \(Y_u=\lambda(u)\), the displayed assumption set \(\Gamma\) is a completion-sound \(1\)-certificate for \(\HardF_{n,s,A}\).  Therefore the formula-footprint theorem applies:

- both \(0\)- and \(1\)-assumption footprints satisfy the same lower inequalities as formula-label certificates;
- in the near-threshold regime, each polarity has size \(n^{a-o(1)}\);
- any proof format that explicitly lists those assumptions must display at least the corresponding number of label assumptions and label-atom bits.

## Boundary

The theorem is a genuine resolution statement, but only for assumption-based encodings where faithful local label facts are explicit and measured.  It does not lower-bound unrestricted resolution encodings, Frege, Extended Frege, IPS, implicit proofs, or compressed/nonlocal proof systems.  Its role is to turn the abstract displayed-atom bridge into a named, checkable restricted proof-system case.

## Gate Impact

This improves `C5` from a purely abstract displayed-atom bridge to a restricted named-system instantiation.  The paper still remains `strong_preprint_not_top_ready`: top-paper status still needs either a stronger proof-system normalization theorem, preferably for a less local recognizable system, or an explicit SAT-family/source lower-bound theorem.
