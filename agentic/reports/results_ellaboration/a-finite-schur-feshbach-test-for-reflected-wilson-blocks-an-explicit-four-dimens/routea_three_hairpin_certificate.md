<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Route A Three-Hairpin Verification Certificate

All symbolic identities verified.

## Verified Identities

- `A_equals_sigma_bbT`: `True`
- `C_equals_corrected_formula`: `True`
- `determinant_formula`: `True`
- `null_corrected_scalar_z`: `True`
- `null_uncorrected_scalar_z`: `True`
- `spurious_sigma2_removed`: `True`
- `first_reduced_margin_u`: `True`
- `corrected_null_margin_v`: `True`
- `mixed_corrected_uv_zero`: `True`

## Key Scalars

- `det_q`: `4*eps**3*sigma*tau/((eps*sigma + 1)**2*(eps**2*tau + 1))`
- `z_C_z`: `4*tau`
- `z_PKP_z`: `sigma**2 + 4*tau`
- `z_correction_z`: `sigma**2`
- `u_A_u`: `2*sigma`
- `v_C_v`: `2*tau/3`
- `u_C_v`: `0`

## Narrative Consequence

This certificate validates the finite source-collision Route A algebra. It does not validate the geometric collar open modules G1-G4, endpoint modules E1-E2, or continuum/gap modules M1-M2.
