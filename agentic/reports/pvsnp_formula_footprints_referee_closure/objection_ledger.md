<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formula Footprints Referee-Objection Ledger

- Status: `implemented`
- Target: `p-vs-np-target`
- Source draft: `/Users/afreitas/Downloads/formula_footprints_full_rows.tex`
- Source assessment: `/Users/afreitas/Downloads/formula_footprints_acceptance_assessment.md`
- Closure policy: no new theorem from this branch may be promoted unless it closes, invalidates, or explicitly demotes a ledger item below.

## Theorem Status

| Object | Current status | Promotion condition | Demotion if not closed |
|---|---|---|---|
| Batched dictionary lemma | `patched` | Use tagged query/dictionary records and masked query extraction after sort. | None after patch; remains an elementary circuit primitive. |
| Formula-footprint theorem | `main_candidate_after_reframe` | Keep the batched lookup improvement and add external anchors plus nonvacuity examples. | Demote to a structured certificate lower-bound lemma. |
| Row-forcing theorem | `supporting_lemma` | Add matching examples or a proof-system extraction theorem. | Keep as an aggregator certificate-complexity lemma. |
| Equality quotient theorem | `supporting_lemma` | Add rank/nonvacuity hypotheses and examples separating quotient from occurrence. | Keep as an affine-completion reformulation of sparse patching. |
| SAT magnification application | `motivation_only` | Add an explicit hard SAT-labeled source theorem. | Keep as a calibration application and nonclaim. |
| Proof-system consequence | `not_claimed` | Instantiate a named proof or certificate system and prove extraction. | Remove proof-complexity lower-bound rhetoric. |
| Randomized/interactive extension | `future_work` | Prove a bounded-error distributional or minimax certificate theorem. | Keep as open problem. |

## Objection Cards

### O1: Main theorems look definitional or immediate

- Severity: `critical`
- Affected objects: row-forcing theorem, quotient theorem, SAT application.
- Objection type: `technical_depth`
- Diagnosis: row forcing and quotient distance are consequences of completion to a near-constant function plus sparse row patching. This is useful, but it is not enough by itself for a selective venue.
- Close condition: either prove matching upper bounds/separations, instantiate a named proof system, or demote these results to supporting lemmas.
- Resolution in this implementation: `demoted_to_supporting_lemmas`
- Closing artifacts: `sharpness_and_separations.md`, `claim_reset_plan.md`, `acceptance_response.md`.

### O2: Formula theorem needs a concrete literature boundary

- Severity: `critical`
- Affected object: formula-footprint theorem.
- Objection type: `literature_underaccounting`
- Diagnosis: the batched lookup improvement is the strongest technical move, but it must be positioned against partial functions, Partial MCSP, circuit test suites, anti-checkers, teaching/specification dimension, exact certification, and certificate complexity.
- Close condition: add a nearest-object comparison that states what the theorem does and does not add relative to each nearby line.
- Resolution in this implementation: `closed_by_anchor_table_and_direct_nearest_literature_citations`
- Closing artifacts: `literature_anchor_table.md`, `literature_anchor_table.json`.

### O3: The hardness predicates may be vacuous for the motivating carrier

- Severity: `critical`
- Affected objects: formula-label predicate, quotient predicate, SAT application.
- Objection type: `nonvacuity_gap`
- Diagnosis: the draft assumes a hard induced source function but does not construct a generator and labeling satisfying the premise in the unrestricted model for the SAT-labeled carrier.
- Close condition: add explicit nonvacuity examples, rank/expansion hypotheses, or demote the SAT carrier to conditional motivation.
- Resolution in this implementation: `partly_closed_by_examples_and_demotion`
- Closing artifacts: `nonvacuity_examples.md`, `acceptance_response.md`.

### O4: Batched dictionary proof has a record-separation flaw

- Severity: `critical`
- Affected object: batched static dictionary lemma.
- Objection type: `technical_error`
- Diagnosis: sorting query records together with dictionary records leaves dictionary records in the sorted list. Symmetry removes the need to restore original query order, but not the need to identify and extract query outputs.
- Close condition: add query/dictionary tags or masks, propagate dictionary values, and aggregate only query records.
- Resolution in this implementation: `closed_by_patch`
- Closing artifacts: `batched_dictionary_repair.md`, `batched_dictionary_repair.tex`.

### O5: No matching upper bounds or model separations are supplied

- Severity: `high`
- Affected objects: formula theorem, occurrence theorem, quotient theorem.
- Objection type: `sharpness_gap`
- Diagnosis: lower bounds are necessary conditions. Without matching constructions or separations, the theory is not yet a tight model of certificate complexity.
- Close condition: give explicit upper bounds/separations where possible and demote claims where not possible.
- Resolution in this implementation: `partly_closed_by_toy_separations_and_demotion`
- Closing artifacts: `sharpness_and_separations.md`, `sharpness_and_separations.tex`.

### O6: The title and introduction overstate the contribution

- Severity: `high`
- Affected objects: abstract, introduction, related-work framing.
- Objection type: `venue_framing`
- Diagnosis: completion-barrier language suggests a broader method-class theorem than the draft proves.
- Close condition: retitle and reframe around structured certificate lower bounds for label-induced hardness predicates.
- Resolution in this implementation: `closed_by_reframe_patch`
- Closing artifacts: `claim_reset_plan.md`, `reframed_intro_patch.tex`.

### O7: No named proof system is instantiated

- Severity: `high`
- Affected objects: proof-complexity motivation and SAT application.
- Objection type: `proof_system_scope`
- Diagnosis: occurrence-local or formula-local certificates do not automatically follow from Resolution, Frege, Extended Frege, IPS, or another standard system.
- Close condition: prove an extraction theorem for a named restricted system, or demote proof-complexity claims.
- Resolution in this implementation: `partly_closed_by_restricted_bridges`
- Closing artifacts: `proof_system_instantiation_decision.md`, `proof_system_instantiation_decision.json`, `assumption_resolution_instantiation.md`, `support_local_extension_resolution.md`, `canonical_syntactic_cone_normalizer.md`, `slice_explicit_er_lower_bound.md`, `displayed_acyclic_er_length_lower_bound.md`, `compressed_er_expansion_transfer.md`, `macro_compressed_er_reuse_tradeoff.md`.

### O8: Randomized and interactive variants are not covered

- Severity: `medium`
- Affected objects: future-work theorem suggestions.
- Objection type: `randomized_overreach`
- Diagnosis: deterministic accepted transcripts are certificates only under perfect soundness. Bounded error needs distributional, minimax, or information-theoretic reasoning.
- Close condition: define a bounded-error model and either prove a theorem or mark it as future work.
- Resolution in this implementation: `partly_closed_by_accepting_union_theorem`
- Closing artifacts: `randomized_certificate_scope.md`, `randomized_certificate_scope.json`, `randomized_accepting_union_theorem.md`, `randomized_accepting_union_theorem.json`.

### O9: Open-ended exploration keeps generating nearby abstractions

- Severity: `critical`
- Affected objects: all future P vs NP marathon outputs touching this draft.
- Objection type: `workflow_loop`
- Diagnosis: the branch can keep generating theorem-shaped abstractions while never closing the concrete referee objections.
- Close condition: require every new result card to include external anchor, nonvacuity witness, sharpness status, demotion boundary, and paper-claim status.
- Resolution in this implementation: `closed_by_gate_policy`
- Closing artifacts: `closure_gate_policy.md`, `closure_gate_policy.json`.

## Promotion Decision

The branch is not ready for selective-theory submission. It is ready for a conservative preprint or internal paper module only after the source draft incorporates the dictionary patch, claim reset, literature anchor table, nonvacuity examples, and theorem-status table.
