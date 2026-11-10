<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Endpoint Incidence Certificate

- Target: `yang-mills-existence-and-mass-gap-target`
- Status: `endpoint_incidence_certificate_ready_geometry_pending`
- Source cycles: `cycle-0252, cycle-0253, cycle-0254`

## Dominance Functional

- Formula: `D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v`
- Dangerous part: `[D_v]_+ = max(D_v, 0)`
- Safe condition: `2 B_12,v <= 4 B_13,v + 4 B_23,v`
- Meaning: Only 12-endpoint dominance can lower the Schur-Feshbach scalar through the leading compact-group endpoint kappa_4 term.

## Certified Lower Bound

- Formula: `S_null >= M_G - C_col sum_v chi_v [D_v]_+ - C_col sum_{v,ij} |w_ij| |epsilon_ij,v| - |E_tail|`
- Color factor: `C_col = g_a^4/24 * (T_F/N)^2`
- Promotion: The finite endpoint block passes when the right-hand side is strictly positive in the same regulator window.
- Falsifier: A same-theory falsifier requires certified positive dominance whose prefactored size exceeds M_G plus all remainders and tails.

## Seven-Point Stencil

- Coefficients: `{'-3': '-1/6', '-2': '2', '-1': '-13/2', '0': '28/3', '1': '-13/2', '2': '2', '3': '-1/6'}`
- Moment checks: `{'0': '0', '1': '0', '2': '0', '3': '0', '4': '24', '5': '0', '6': '0', '7': '0', '8': '-1176'}`
- Error bound: `abs(kappa_4 - D_h,7 f) <= (7/240) h^4 M_8`

## Incidence Table To Fill

### left_boundary_endpoint
- Entries: `B_12,v, B_13,v, B_23,v, chi_v, epsilon_12,v, epsilon_13,v, epsilon_23,v, tail_share`
- Dominance: `D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v`
- Status: `geometry_not_yet_enumerated`
- Validation action: Draw the regulated plaquette-sheet endpoint box, record oriented pair incidences, compute B_ij,v, then evaluate [D_v]_+.

### right_boundary_endpoint
- Entries: `B_12,v, B_13,v, B_23,v, chi_v, epsilon_12,v, epsilon_13,v, epsilon_23,v, tail_share`
- Dominance: `D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v`
- Status: `geometry_not_yet_enumerated`
- Validation action: Draw the regulated plaquette-sheet endpoint box, record oriented pair incidences, compute B_ij,v, then evaluate [D_v]_+.

### coalesced_corner_endpoint
- Entries: `B_12,v, B_13,v, B_23,v, chi_v, epsilon_12,v, epsilon_13,v, epsilon_23,v, tail_share`
- Dominance: `D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v`
- Status: `geometry_not_yet_enumerated`
- Validation action: Draw the regulated plaquette-sheet endpoint box, record oriented pair incidences, compute B_ij,v, then evaluate [D_v]_+.

### tail_interface_endpoint
- Entries: `B_12,v, B_13,v, B_23,v, chi_v, epsilon_12,v, epsilon_13,v, epsilon_23,v, tail_share`
- Dominance: `D_v = 2 B_12,v - 4 B_13,v - 4 B_23,v`
- Status: `geometry_not_yet_enumerated`
- Validation action: Draw the regulated plaquette-sheet endpoint box, record oriented pair incidences, compute B_ij,v, then evaluate [D_v]_+.

## Next Work Queue

1. Enumerate actual endpoint boxes for the locked three-hairpin plaquette sheets.
   - Payoff: Fills the B_12,v, B_13,v, B_23,v table required by the endpoint dominance theorem.
   - Stop when: Stop only after every endpoint class has either a certified B-table row or a stated geometry obstruction.
2. Evaluate D_+ = sum_v [2B_12,v - 4B_13,v - 4B_23,v]_+ for the enumerated table.
   - Payoff: Decides whether the compact-group endpoint kappa_4 term is safe, dangerous, or neutral in the actual null channel.
   - Stop when: Stop only when the sign and magnitude of every positive-dominance endpoint are accounted for.
3. Certify epsilon_ij,v and E_tail with the seven-point source-derivative or heat-kernel remainder bounds.
   - Payoff: Turns the symbolic dominance result into a finite paper theorem or a finite falsifier.
   - Stop when: Stop only when the interval for S_null is positive, negative, or explicitly too wide to promote.

## Claim Boundary

- `claimable_now`: A finite endpoint kappa_4 incidence certificate: only [D_v]_+ can be dangerous under the stated heat-kernel asymptotic and cancellation assumptions.
- `not_claimable_yet`: The actual three-hairpin endpoint block passes or fails; the geometric B-table and remainder intervals are still missing.
- `paper_section_target`: Endpoint kappa_4 incidence dominance theorem and worked-calculation protocol.
