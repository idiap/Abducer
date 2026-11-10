<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# YM Endpoint Source Table Contract

Target: `yang-mills-existence-and-mass-gap-target`
Artifact: `endpoint_source_table_contract`

## Fixed Setup

- Geometry: heat-kernel SU(N) post-H,K reflected-Wilson three-hairpin endpoint block with fixed collar geometry
- Gauge group: SU(N), with SU(2) or SU(3) rows permitted only when the N-dependence boundary is explicit
- Regulator: same-regulator heat-kernel lattice/cutoff window used by the finite Route A Wilson block
- Source classes: C_ep classes identified by regulated endpoint source data before clipping aggregated D_c

## Required Row Fields

- `D_c`: interval or exact fractional incidence; aggregate within each source-equivalence class before positive-part clipping
- `kappa_c_intervals`: outward-rounded fourth cumulant intervals from the seven-point stencil or root-quartic cap, with validity regime recorded per row
- `M8`: uniform eighth-derivative or remainder bound per source class
- `M_G`: geometry/regulator margin term for the fixed post-H,K endpoint block
- `C_N`: color factor with N-dependence separated from finite SU(2)/SU(3) pilot rows
- `T_tail`: cutoff-uniform tail/remainder interval; promotion is forbidden without this field
- `I_gate_interval`: final outward-rounded scalar interval after class aggregation, color factor, geometry margin, and T_tail

Seven `log Z` sample slots:

- Slot 1: `log Z_{a,c}(-3h)` (required)
- Slot 2: `log Z_{a,c}(-2h)` (required)
- Slot 3: `log Z_{a,c}(-1h)` (required)
- Slot 4: `log Z_{a,c}(0h)` (required)
- Slot 5: `log Z_{a,c}(1h)` (required)
- Slot 6: `log Z_{a,c}(2h)` (required)
- Slot 7: `log Z_{a,c}(3h)` (required)

## Outcome Rules

- Promote: If I_gate lower endpoint is >= 0 with cutoff-uniform T_tail, promote only the finite post-H,K endpoint gate as a support theorem.
- Finite falsifier: If I_gate upper endpoint is < 0, emit a finite same-regulator Route A endpoint falsifier and block positive promotion.
- Quarantine: If I_gate overlaps zero, T_tail is nonuniform, or a required row is not instantiable, quarantine the endpoint branch before more broad reasoning.

## Physical Boundary

This endpoint table can support a finite reflected-Wilson OS gate only. It does not prove continuum existence, OS/Wightman reconstruction, nontriviality, gauge-invariant observable density, or the spectral mass gap.
