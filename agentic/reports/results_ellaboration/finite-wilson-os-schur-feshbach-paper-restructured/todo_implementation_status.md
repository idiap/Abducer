<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Result TODO Implementation Status

All eight result-elaboration TODOs were implemented into the expanded manuscript draft.
Where the original draft lacked regulator-specific Wilson data, the implementation uses a rigorous finite certificate and records the residual claim boundary instead of promoting an unsupported Wilson result.

## Status

### todo-001 `slot:same-theory-quotient`

- Status: `implemented_as_finite_certificate`
- Artifact: Proposition \ref{prop:same-theory-normalization}
- Residual boundary: Pair-dependent quotient remains demoted unless certified by congruence, positive kernel, or direct Gram realization.

### todo-002 `slot:HK-theorem`

- Status: `implemented_as_coefficient_conversion_theorem`
- Artifact: Proposition \ref{prop:HK-extraction}
- Residual boundary: The theorem converts coefficients; it does not derive regulator-specific Wilson OPE data.

### todo-003 `slot:regulator-observable`

- Status: `implemented_as_regulated_data_proposition`
- Artifact: Proposition \ref{prop:regulator-observable-data}
- Residual boundary: A concrete application must still name the lattice, reflection plane, group, representation, and paths.

### todo-004 `slot:nontrivial-outcome`

- Status: `implemented_as_exact_finite_model`
- Artifact: Proposition \ref{prop:three-observable-certificate}
- Residual boundary: Not promoted to a Wilson calculation until H,K are derived from a regulator-specific block.

### todo-005 `slot:color-factor`

- Status: `implemented_as_source_derivative_formula`
- Artifact: Proposition \ref{prop:endpoint-prefactor}
- Residual boundary: The numerical prefactor remains conditional until the endpoint measure and incidence tensor are specified.

### todo-006 `slot:uniform-remainder`

- Status: `implemented_as_uniform_remainder_criterion`
- Artifact: Proposition \ref{prop:uniform-endpoint-remainder}
- Residual boundary: The paper must keep endpoint claims conditional if the sixth-derivative/tail hypotheses are not verified.

### todo-007 `slot:three-hairpin-table`

- Status: `implemented_as_reproducible_finite_table`
- Artifact: Three-hairpin table and exact JSON certificate
- Residual boundary: Finite coefficient table, not yet a named Wilson-path table.

### todo-008 `slot:prior-art`

- Status: `implemented_as_claim_boundary_remark`
- Artifact: Remark \ref{rem:prior-art-boundary}
- Residual boundary: Novelty remains bounded to finite packaging unless regulator-specific Wilson coefficients are proved.
