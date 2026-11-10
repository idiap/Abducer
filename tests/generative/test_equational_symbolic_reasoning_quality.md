<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Equational Symbolic Reasoning Quality Checks

Use these checks when reviewing ESR outputs:

- The packet names a finite carrier and all side conditions under which the
  identities are valid.
- Exact identities include formula, LaTeX, validity conditions, derivation
  method, backend or manual fallback, and `symbolic_formula` status.
- Falsifier shapes are formula-derived and preserve the target carrier instead
  of changing the problem.
- Analytic obligations cite the finite interface and name the Yang-Mills content
  still needed.
- The packet explicitly excludes Lean/theorem-prover status and continuum proof
  progress for this phase.
