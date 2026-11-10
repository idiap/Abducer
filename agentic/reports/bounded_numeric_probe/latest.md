<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Bounded Numeric Probe

- Status: `falsifier_candidate`
- Probe: `quotient-determinant-search`
- Domain: `rho_ij in [0,1] on 9-point grid; Phi in [0,pi] on 9-point grid`
- Stopping: exhaustive deterministic grid of 6561 points
- Lesson: Pairwise minor bounds do not suffice when the cycle phase and three moduli make the normalized determinant negative.
- Transfer boundary: The result remains a local finite-interface probe until a same-theory analytic transfer certificate is proved.
