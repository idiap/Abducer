<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Subworkflow Integration Tests

- Target: `yang-mills-existence-and-mass-gap-target`
- Status: `pass`
- Recent cycle window: `cycle-0345, cycle-0346, cycle-0347, cycle-0348, cycle-0349, cycle-0350, cycle-0351, cycle-0352`

## Current Progress Context

### cycle-0345 - boundary_ope_extraction
- Branch: `marathon.branch.2943978bc7b2` One-sided endpoint-source screen for the post-H,K Wilson gate
- Blocking gap: No actual same-theory seven-point endpoint source intervals or cutoff-uniform T_tail constants have been computed for the positive-D source classes.
- Next experiment: Proof search plus targeted computation: in the heat-kernel SU(N) endpoint boxes of the fixed post-H,K block, evaluate the seven source values F_c(rh) for every positive-D source class, certify M_8(c) and T_tail, then report the interval I_gate as promote, finite falsifier, or continued quarantine.

### cycle-0346 - boundary_ope_extraction
- Branch: `marathon.branch.2943978bc7b2` Endpoint Root-Quartic Screen for Wilson Collar OS Gate
- Blocking gap: The proof still needs cutoff-uniform endpoint remainders epsilon_c, a uniform tail T_tail, and actual source-equivalence data for the positive-D endpoint classes.
- Next experiment: Route to proof search plus targeted source computation: for the heat-kernel plaquette-sheet endpoint classes with D_c>0, evaluate the seven-point connected cumulant witness, certify M_{8,c}, compute the root-quartic cap, add T_tail, and return promote/falsifier/quarantine for the finite post-H,K OS gate.

### cycle-0347 - schur_preimage_determinant
- Branch: `marathon.branch.2943978bc7b2` Endpoint leakage cap for the post-H,K reflected-Wilson gate
- Blocking gap: Actual same-theory endpoint source intervals and a regulator-uniform tail estimate are still missing for the positive-D classes.
- Next experiment: Run the validator-facing heat-kernel endpoint source computation for positive-D classes: compute f_c(jh), certify kappa_c intervals with the seven-point stencil or root-quartic cap, aggregate D_C before clipping, add C_N and T_tail_abs, and return the sign of [I_-,I_+] for promote/falsifier/quarantine.

### cycle-0348 - schur_preimage_determinant
- Branch: `marathon.branch.2943978bc7b2` One-sided endpoint source screen for the post-H,K Wilson OS gate
- Blocking gap: No actual validator-facing table of endpoint source classes, D_c values, epsilon_c bounds, and tau_tail has been computed for the regulated three-hairpin geometry.
- Next experiment: Proof search plus targeted computation: enumerate heat-kernel endpoint source classes for the actual three-hairpin geometry, compute the connected cumulant witness d_s^4 log Z_c by seven-point stencils or root-quartic caps, aggregate D_c before clipping, certify epsilon_c and tau_tail, and return the scalar interval I_gate for promotion, falsifier, or continued quarantine.

### cycle-0349 - boundary_ope_extraction
- Branch: `marathon.branch.2943978bc7b2` Reflection-Positivity Closed-Cone Topology: one-sided endpoint source screen
- Blocking gap: No actual same-theory source stencil intervals or cutoff-uniform tail bound are available for the positive-D endpoint classes, so the branch cannot promote the finite block.
- Next experiment: Run targeted proof search for the positive-D endpoint classes: compute the same-theory connected cumulant witness by the seven-point heat-kernel source stencil, certify M8 and T_tail, then return the interval sign of I_gate; otherwise keep quarantine.

### cycle-0350 - schur_preimage_determinant
- Branch: `marathon.branch.2943978bc7b2` Finite post-H,K Wilson endpoint screen for same-theory OS transfer
- Blocking gap: The actual endpoint source classes, fractional incidences D_c, uniform eighth-derivative bounds, and T_tail for the fixed hairpin geometry have not been computed.
- Next experiment: Proof search plus targeted endpoint source computation: build the C_ep table for the actual heat-kernel three-hairpin endpoints, compute D_c and seven log Z_c samples for every connected cumulant witness class, then certify whether I_gate is positive, negative, or still quarantined.

### cycle-0351 - schur_preimage_determinant
- Branch: `marathon.branch.2943978bc7b2` Finite post-H,K endpoint cumulant screen for reflected Wilson OS transfer
- Blocking gap: The branch lacks actual endpoint source intervals for the positive-D classes and a cutoff-uniform T_tail bound; without them I_gate cannot be signed.
- Next experiment: Compute the positive-D endpoint source table for the heat-kernel SU(N) three-hairpin block: seven log Z_{a,c}(jh) values per source-equivalence class, kappa_c intervals, D_c, C_N, M_G, and T_tail; route result to proof search if I_->=0, to falsifier write-up if I_+<0, and to quarantine if intervals overlap zero.

### cycle-0352 - schur_preimage_determinant
- Branch: `marathon.branch.01ac559ac937` Finite OS spectral-support theorem with Wilson-density gate quarantine
- Blocking gap: The analytic proof is complete locally, but the Clay-facing gap is gauge-invariant observable density with cutoff-uniform decay and same-theory recovery. The current branch has no independent continuum Schwinger construction, RG basin entry, large-field/topology summability, or nontrivial connected cumulant witness.
- Next experiment: Route to abstraction refit plus validator-facing falsifier sprint: instantiate the spectral-carrier packet for the SU(3) heat-kernel Wilson-net thought experiment, varying only alpha, and record recovery errors, OS positivity margins, connected cumulant witness/non-Gaussian Schwinger family marker, gauge-invariant observable density status, and physical-unit decay constants. Promote if a dense spectral measure witness with common m survives; demote or quarantine on uniformity_gap, proxy_shift, missing_carrier, or noncommuting_limits.

## Qualitative Tests

- `PASS` qualitative_packets_use_recent_cycle_window: 8/8 recent cycles cited
- `PASS` qualitative_relations_reflect_current_boundary_progress: requires boundary, quotient, phase, and determinant relation language from cycles 198-205
- `PASS` qualitative_relations_overlap_cycle_content: relation text shares substantive terms with the recent branch outputs
- `PASS` qualitative_graph_preserves_cycle_ids: graph source cycles: cycle-0345, cycle-0346, cycle-0347, cycle-0348, cycle-0349, cycle-0350, cycle-0351, cycle-0352

## Gedanken Tests

- `PASS` gedanken_packets_cover_recent_cycles: 8/8 recent cycles have packets
- `PASS` gedanken_packets_are_cycle_grounded: 16/16 packet-cycle links match source artifact, focus, and content overlap
- `PASS` gedanken_packets_preserve_progression_diversity: packet focus counts: {'boundary_ope_extraction': 6, 'schur_preimage_determinant': 10}; cycle focus counts: {'boundary_ope_extraction': 3, 'schur_preimage_determinant': 5}
- `PASS` gedanken_followups_use_qualitative_skills: every packet has at least one follow-up requiring the qualitative subworkflow

## Cross Workflow Tests

- `PASS` gedanken_affected_edges_exist_in_qualitative_graph: 16/16 affected edges exist
- `PASS` qualitative_graph_links_gedanken_packets: 16/16 packets linked from graph edges
- `PASS` graph_links_remain_conceptual_not_proof: Gedanken-origin graph updates must remain conceptual probes

## Parsimonious Probe Tests

- `PASS` pmp_symbolic_before_numeric: parsimonious symbolic-before-numeric decision is recorded for the finite quotient determinant
- `PASS` pmp_obligations_precede_numeric_probe: analytic estimate queue items are ranked before any bounded numeric calibration
- `PASS` esr_finite_interface_has_side_conditions_and_falsifiers: finite algebra packet records side-condition ledger and formula-derived falsifier shapes
- `PASS` esr_no_lean_or_proof_overclaim: equational symbolic packet explicitly excludes Lean/theorem-prover/proof-promotion status
- `PASS` pmp_graph_carries_symbolic_and_obligation_status: qualitative graph includes symbolic formula, finite interface, falsifier shape, and analytic obligation edges
- `PASS` pmp_bounded_numeric_probe_is_non_proof_when_present: bounded numeric outputs remain non-proof statuses

## Refinements

- Gedanken packet generation is cycle-sensitive, so repeated branch titles no longer overwrite distinct previous-cycle progress.
- Reflection-positive Gedanken packets now distinguish boundary OPE extraction from quotient-holonomy progress.
- The integration gate checks semantic overlap with recent cycle outputs, not only artifact existence.
- PMP/ESR now routes exact finite algebra through side-condition ledgers, falsifier shapes, and analytic obligation queues before any bounded numeric probe.
