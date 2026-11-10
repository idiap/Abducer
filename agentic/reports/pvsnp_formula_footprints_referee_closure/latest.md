<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formula Footprints Referee Closure

- Status: `implemented`
- Target: `p-vs-np-target`
- Source draft: `/Users/afreitas/Downloads/formula_footprints_full_rows.tex`
- Source assessment: `/Users/afreitas/Downloads/formula_footprints_acceptance_assessment.md`

## Summary

The 10-item referee-objection TODO queue has been implemented as a closure
packet and extended with publication-level gate work.  The packet does not
pretend the draft is now a selective-theory submission.  Instead, it separates
repairs, upgrades, and demotions: the dictionary issue is patched; the
formula-footprint barrier is now the named flagship theorem; generic
identity-carrier sharpness shows the flagship scale is near-tight in the
standard truth-table model; row-forcing and quotient-distance results are
supporting interface lemmas; SAT magnification is conditional calibration;
and proof-system claims remain restricted to displayed-atom extraction,
explicit-local resolution, support-local auxiliary resolution, and the
support-local extension-resolution, dependency-cone extension-normalizer,
canonical syntactic-cone normalizer, final backward-slice, slice-explicit ER,
displayed acyclic ER, expansion-bounded compressed ER, macro-compressed ER,
support-declared macro ER, support-audited LRAT, provenance-typed LRAT,
namespace-typed LRAT antecedent closure,
strict-prefix Qrep replay, support-erasure boundary, OR-DAG frontier,
acyclic Boolean frontier, visible adaptive frontier, visible adaptive branching-program frontier,
controller-complete adaptive audit,
trace-complete DPLL decision-log,
antecedent-complete CDCL learned-clause,
CDCL antecedent-erasure trichotomy,
RUP-complete CDCL support normalizer,
canonical-namespace RUP-CDCL standardizer,
carrier-independent audit upgrade criterion,
self-auditing RUP-CDCL instantiation,
append-only self-auditing RUP-CDCL instantiation,
prefix-typed append-only RUP-CDCL instantiation,
prefix-typed RUP support-witness necessity,
intrinsic-locality prefix-typed RUP-CDCL instantiation,
novelty-delta accounting,
cone-budget, bounded-depth, and normalization-transfer
theorems unless a concrete stronger normalizer is supplied.

## Artifacts

| TODO | Artifact |
|---|---|
| `pvsnp-ff-referee-001` | `objection_ledger.md`, `objection_ledger.json` |
| `pvsnp-ff-referee-002` | `literature_anchor_table.md`, `literature_anchor_table.json` |
| `pvsnp-ff-referee-003` | `batched_dictionary_repair.md`, `batched_dictionary_repair.tex` |
| `pvsnp-ff-referee-004` | `nonvacuity_examples.md`, `nonvacuity_examples.json` |
| `pvsnp-ff-referee-005` | `sharpness_and_separations.md`, `sharpness_and_separations.tex` |
| `pvsnp-ff-referee-006` | `claim_reset_plan.md`, `reframed_intro_patch.tex` |
| `pvsnp-ff-referee-007` | `proof_system_instantiation_decision.md`, `proof_system_instantiation_decision.json` |
| `pvsnp-ff-referee-008` | `randomized_certificate_scope.md`, `randomized_certificate_scope.json` |
| `pvsnp-ff-referee-009` | `closure_gate_policy.md`, `closure_gate_policy.json` |
| `pvsnp-ff-referee-010` | `acceptance_response.md`, `acceptance_response.json` |

## Publication-Level Gate

| Artifact | Role |
|---|---|
| `top_paper_criteria.md`, `top_paper_criteria.json` | Defines the criteria for a selective complexity-theory paper. |
| `publication_level_gap_audit.md`, `publication_level_gap_audit.json` | Audits the revised paper against the criteria and selects the next upgrade route. |
| `structured_certificate_lower_bounds_revision.tex`, `structured_certificate_lower_bounds_revision.pdf` | Repo-local revised paper draft with the claim reset, dictionary repair, nonvacuity/sharpness checks, and related-work boundary integrated. |
| `randomized_accepting_union_theorem.md`, `randomized_accepting_union_theorem.json` | Proof packet for the bounded-error accepting-union theorem now integrated into the revised paper. |
| `identity_carrier_generic_sharpness.md`, `identity_carrier_generic_sharpness.json` | Proof packet for generic near-sharpness in the standard identity truth-table carrier. |
| `proof_dependency_audit_map.md`, `proof_dependency_audit_map.json` | Proof-object packet for the internal proof-dependency and nonclaim-boundary map. |
| `proof_system_normalization_target.md`, `proof_system_normalization_target.json` | Defines the controlled local normalization theorem needed for proof-system applications. |
| `assumption_resolution_instantiation.md`, `assumption_resolution_instantiation.json` | Proof packet for the restricted resolution theorem with explicit faithful label assumptions. |
| `resolution_unit_core_lower_bound.md`, `resolution_unit_core_lower_bound.json` | Proof packet for the used-unit-core lower bound in full-assignment resolution refutations. |
| `resolution_local_clause_support.md`, `resolution_local_clause_support.json` | Proof packet for the explicit local-clause support theorem for resolution. |
| `support_local_auxiliary_resolution.md`, `support_local_auxiliary_resolution.json` | Proof packet for the support-local auxiliary resolution theorem. |
| `support_local_extension_resolution.md`, `support_local_extension_resolution.json` | Proof packet for the support-local extension-resolution theorem. |
| `dependency_cone_extension_normalizer.md`, `dependency_cone_extension_normalizer.json` | Proof packet for the dependency-cone extension normalizer theorem. |
| `canonical_syntactic_cone_normalizer.md`, `canonical_syntactic_cone_normalizer.json` | Proof packet for the canonical syntactic-cone normalizer corollary. |
| `final_backward_slice_lower_bound.md`, `final_backward_slice_lower_bound.json` | Proof packet for the final backward-slice lower-bound corollary. |
| `slice_explicit_er_lower_bound.md`, `slice_explicit_er_lower_bound.json` | Proof packet for the slice-explicit extension-resolution lower-bound corollary. |
| `displayed_acyclic_er_length_lower_bound.md`, `displayed_acyclic_er_length_lower_bound.json` | Proof packet for the displayed acyclic ER length lower-bound corollary. |
| `compressed_er_expansion_transfer.md`, `compressed_er_expansion_transfer.json` | Proof packet for the expansion-bounded compressed ER transfer corollary. |
| `macro_compressed_er_reuse_tradeoff.md`, `macro_compressed_er_reuse_tradeoff.json` | Proof packet for the macro-compressed ER reuse tradeoff corollary. |
| `support_declared_macro_er_normalizer.md`, `support_declared_macro_er_normalizer.json` | Proof packet for the support-declared macro ER normalizer corollary. |
| `support_audited_lrat_trace_normalizer.md`, `support_audited_lrat_trace_normalizer.json` | Proof packet for the support-audited LRAT trace normalizer corollary. |
| `provenance_typed_lrat_support_audit.md`, `provenance_typed_lrat_support_audit.json` | Proof packet showing trusted typed LRAT/DRAT-with-LRAT provenance supplies the support audit. |
| `namespace_typed_lrat_antecedent_closure_normalizer.md`, `namespace_typed_lrat_antecedent_closure_normalizer.json` | Proof packet showing a trusted formula-label namespace plus LRAT antecedent closure supplies the used support audit for witnessed auxiliary clauses. |
| `strict_prefix_qrep_normalizer.md`, `strict_prefix_qrep_normalizer.json` | Proof packet for strict-prefix quotient-representative replay: Qrep compression is transparent only when same-theory certificates are charged before use. |
| `strict_prefix_qrep_prefix_scan_examples.md`, `strict_prefix_qrep_prefix_scan_examples.json` | Finite verifier examples: one accepted strict-prefix Qrep merge and one rejected delayed-certificate private-row falsifier. |
| `support_audit_necessity_separator.md`, `support_audit_necessity_separator.json` | Boundary packet showing checked clausal unsatisfiability does not itself certify completion-local support. |
| `support_erasure_indistinguishability_separator.md`, `support_erasure_indistinguishability_separator.json` | Boundary packet showing untyped LRAT syntax does not determine formula-label support without variable-role provenance. |
| `plain_lrat_extraction_trichotomy.md`, `plain_lrat_extraction_trichotomy.json` | Boundary packet showing a plain LRAT extractor must add provenance, pay role-agnostic support, or be unsound on a same-skeleton lift. |
| `semantic_relation_support_certificate.md`, `semantic_relation_support_certificate.json` | Proof packet for local nonlinear semantic-relation support certificates, including SAT self-reduction OR constraints. |
| `acyclic_or_tree_residual_certificate.md`, `acyclic_or_tree_residual_certificate.json` | Proof packet for the acyclic OR-tree frontier residual certificate after internal self-reduction nodes are eliminated. |
| `or_dag_frontier_residual_certificate.md`, `or_dag_frontier_residual_certificate.json` | Proof packet for the quotiented OR-DAG frontier residual certificate after internal pure-OR nodes are eliminated. |
| `acyclic_boolean_frontier_residual_certificate.md`, `acyclic_boolean_frontier_residual_certificate.json` | Proof packet for exposed acyclic Boolean frontier residual certificates via ordinary pointwise certificate complexity. |
| `visible_adaptive_frontier_residual_certificate.md`, `visible_adaptive_frontier_residual_certificate.json` | Proof packet for checker-visible adaptive frontier residual certificates via ordinary pointwise certificate complexity; the transcript path is sufficient support. |
| `visible_adaptive_branching_frontier_residual_certificate.md`, `visible_adaptive_branching_frontier_residual_certificate.json` | Proof packet for checker-visible adaptive branching-program frontier residual certificates via ordinary pointwise certificate complexity; the computation path is sufficient support. |
| `hidden_adaptive_transcript_insufficiency_separator.md`, `hidden_adaptive_transcript_insufficiency_separator.json` | Boundary packet showing uncertified adaptive transcript summaries do not determine sound support and can hide all-frontier OR dependencies. |
| `controller_complete_adaptive_audit_normalizer.md`, `controller_complete_adaptive_audit_normalizer.json` | Proof packet showing hidden adaptive support is sound when a proof object exposes a complete acyclic controller, replay path, and local equivalence certificate. |
| `trace_complete_dpll_decision_log_normalizer.md`, `trace_complete_dpll_decision_log_normalizer.json` | Proof packet showing trace-complete DPLL decision logs supply the controller-complete adaptive audit when the whole controller, replay path, and local clause or propagation witnesses are logged. |
| `antecedent_complete_cdcl_learned_clause_normalizer.md`, `antecedent_complete_cdcl_learned_clause_normalizer.json` | Proof packet showing CDCL learned clauses supply the same audit only when every used learned clause has an acyclic antecedent DAG down to audited local support. |
| `cdcl_antecedent_erasure_trichotomy.md`, `cdcl_antecedent_erasure_trichotomy.json` | Boundary packet showing provenance-free CDCL learned-clause syntax must add equivalent provenance or a non-plain invariant, pay conservative support, or be unsound on a same-skeleton lift. |
| `rup_complete_cdcl_support_normalizer.md`, `rup_complete_cdcl_support_normalizer.json` | Proof packet showing checker-visible RUP propagation certificates over a known live clause database supply the CDCL support audit when formula-label support is parsed and deleted-clause consequences retain their support charge. |
| `canonical_namespace_rup_cdcl_standardizer.md`, `canonical_namespace_rup_cdcl_standardizer.json` | Proof packet showing a deterministic encoding manifest with a reserved formula-label interval and live-database log makes the RUP-CDCL support parser checker-visible. |
| `carrier_independent_audit_upgrade_criterion.md`, `carrier_independent_audit_upgrade_criterion.json` | Proof packet turning the remaining top-paper proof-system route into a system-intrinsic audit-extractor criterion without carrier-specific manifests or hidden role advice. |
| `self_auditing_rup_cdcl_instantiation.md`, `self_auditing_rup_cdcl_instantiation.json` | Proof packet instantiating the carrier-independent audit criterion for an enriched RUP-CDCL certificate format whose proof object contains the label decoder, live-database log, RUP witnesses, and retained support annotations. |
| `append_only_self_auditing_rup_cdcl.md`, `append_only_self_auditing_rup_cdcl.json` | Proof packet for the less-annotated deletion-free self-auditing RUP-CDCL bridge: append-only clause logs remove the need for retained deleted-clause support annotations. |
| `prefix_typed_append_only_rup_cdcl.md`, `prefix_typed_append_only_rup_cdcl.json` | Proof packet for the typed append-only RUP-CDCL bridge: public formula-label syntax removes the proof-internal label decoder as well as retained deleted-clause support annotations. |
| `prefix_typed_rup_support_witness_necessity.md`, `prefix_typed_rup_support_witness_necessity.json` | Boundary packet showing public label syntax and append-only RUP checking do not certify completion-local auxiliary support without a witness or intrinsic invariant. |
| `intrinsic_locality_prefix_typed_rup_cdcl.md`, `intrinsic_locality_prefix_typed_rup_cdcl.json` | Proof packet showing fixed public completion-stable auxiliary rules replace separate support-local witness fields in prefix-typed append-only RUP-CDCL. |
| `novelty_delta_accounting.md`, `novelty_delta_accounting.json` | C7/C11 accounting packet: closest literature, before/after understanding shift, novelty delta, and flagship-role test for the cohered result package. |
| `cone_budget_extension_lower_bound.md`, `cone_budget_extension_lower_bound.json` | Proof packet for the cone-budget extension lower-bound corollary. |
| `bounded_depth_extension_tradeoff.md`, `bounded_depth_extension_tradeoff.json` | Proof packet for the bounded-depth extension tradeoff corollary. |
| `support_local_normalization_transfer.md`, `support_local_normalization_transfer.json` | Proof packet for the general support-local normalizer transfer theorem. |
| `cohered_result_spine.md`, `cohered_result_spine.json` | Operational C11 admission test: new results must be flagship, calibration, interface variant, proof-system bridge, or boundary work around the formula-footprint spine. |
| C11 cohered results criterion | The criteria now require cohered results: one sharp, novel, weighty result package, not a fragmented ensemble of results or disconnected payoffs. |

## Final Claim State

| Object | Status |
|---|---|
| Batched dictionary lemma | `patched` |
| Formula-footprint barrier theorem | `named_flagship_standard_certificate_lower_bound` |
| Identity-carrier generic sharpness | `proved_in_revised_tex` |
| Row-forcing theorem | `supporting_lemma` |
| Equality quotient theorem | `supporting_lemma` |
| Semantic-relation support certificate | `proved_local_nonlinear_relation_support_boundary` |
| Acyclic OR-tree residual certificate | `proved_bounded_global_or_frontier_certificate` |
| OR-DAG frontier residual certificate | `proved_bounded_shared_or_frontier_certificate` |
| Acyclic Boolean frontier residual certificate | `proved_exposed_acyclic_boolean_frontier_certificate_complexity_boundary` |
| Visible adaptive frontier residual certificate | `proved_checker_visible_adaptive_frontier_certificate_complexity_boundary` |
| Visible adaptive branching-program frontier residual certificate | `proved_checker_visible_adaptive_branching_frontier_certificate_complexity_boundary` |
| Hidden adaptive transcript insufficiency separator | `proved_boundary_transcript_only_hidden_adaptive_extraction_is_unsound` |
| Controller-complete adaptive audit normalizer | `proved_positive_audited_hidden_adaptive_normalizer_condition` |
| Trace-complete DPLL decision-log normalizer | `trace_complete_dpll_controller_log_normalizer_proved` |
| Antecedent-complete CDCL learned-clause normalizer | `antecedent_complete_cdcl_learned_clause_normalizer_proved` |
| CDCL antecedent-erasure trichotomy | `cdcl_antecedent_erasure_trichotomy_proved` |
| RUP-complete CDCL support normalizer | `rup_complete_cdcl_support_normalizer_proved` |
| Canonical-namespace RUP-CDCL standardizer | `canonical_namespace_rup_cdcl_standardizer_proved` |
| Carrier-independent audit upgrade criterion | `carrier_independent_audit_upgrade_criterion_proved` |
| Self-auditing RUP-CDCL instantiation | `self_auditing_rup_cdcl_instantiation_proved` |
| Append-only self-auditing RUP-CDCL instantiation | `append_only_self_auditing_rup_cdcl_proved` |
| Prefix-typed append-only RUP-CDCL instantiation | `prefix_typed_append_only_rup_cdcl_proved` |
| Prefix-typed RUP support-witness necessity | `prefix_typed_rup_support_witness_necessity_proved` |
| Intrinsic-locality prefix-typed RUP-CDCL instantiation | `intrinsic_locality_prefix_typed_rup_cdcl_proved` |
| Novelty-delta accounting | `integrated_in_revised_tex_as_C7_C11_before_after_shift` |
| SAT magnification application | `conditional_calibration` |
| Unrestricted standard proof-system theorem | `not_claimed` |
| Displayed-atom extraction theorem | `restricted_bridge_added_not_standard_system` |
| Assumption-resolution theorem | `restricted_named_resolution_instantiation_proved` |
| Resolution unit-core corollary | `restricted_full_assignment_resolution_support_bound_proved` |
| Resolution local-clause theorem | `restricted_explicit_local_clause_support_bound_proved` |
| Support-local auxiliary resolution theorem | `restricted_support_local_auxiliary_resolution_bound_proved` |
| Support-local extension-resolution theorem | `restricted_support_local_extension_resolution_bound_proved` |
| Dependency-cone extension normalizer theorem | `cone_annotated_extension_normalizer_proved` |
| Canonical syntactic-cone normalizer | `automatic_syntactic_cone_normalizer_proved` |
| Final backward-slice lower bound | `final_extension_slice_budget_proved` |
| Slice-explicit ER lower bound | `restricted_er_style_slice_explicit_lower_bound_proved` |
| Displayed acyclic ER length lower bound | `displayed_acyclic_er_length_lower_bound_proved` |
| Expansion-bounded compressed ER transfer | `expansion_bounded_compressed_er_transfer_proved` |
| Macro-compressed ER reuse tradeoff | `macro_compressed_er_reuse_tradeoff_proved` |
| Support-declared macro ER normalizer | `support_declared_macro_er_normalizer_proved` |
| Support-audited LRAT trace normalizer | `support_audited_lrat_trace_normalizer_proved` |
| Provenance-typed LRAT support audit | `trusted_typed_provenance_supplies_support_audit_proved` |
| Namespace-typed LRAT antecedent-closure normalizer | `trusted_namespace_and_lrat_antecedent_closure_supplies_support_audit_proved` |
| Strict-prefix Qrep replay normalizer | `strict_prefix_qrep_replay_normalizer_proved` |
| Strict-prefix Qrep prefix-scan examples | `finite_verifier_examples_validated` |
| Support-audit necessity separator | `proved_boundary_unsat_checking_does_not_imply_support_locality` |
| Support-erasure indistinguishability separator | `proved_boundary_untyped_lrat_syntax_does_not_determine_support` |
| Plain LRAT extraction trichotomy | `proved_boundary_plain_trace_extraction_requires_provenance_or_worst_case_support` |
| Cone-budget extension lower bound | `cone_budget_extension_tradeoff_proved` |
| Bounded-depth extension tradeoff | `bounded_depth_extension_tradeoff_proved` |
| Support-local normalization transfer theorem | `conditional_general_transfer_proved_normalizer_not_instantiated_for_strong_systems` |
| Randomized/interactive theorem | `bounded_error_union_footprint_proved; stronger_expected_variants_not_claimed` |
| Proof dependency audit map | `integrated_in_revised_tex` |
| Proof-system normalization target | `integrated_in_revised_tex` |
| Explicit hard SAT carrier | `future_work_quarantine` |

## Remaining Non-TODO Mathematical Work

The closure packet leaves two decisive upgrade routes.  Each route must now satisfy the C11 cohered-result gate: it has to strengthen the single completion-soundness spine rather than add a fragmented result.

1. instantiate the intrinsic-locality rule discipline in a natural solver/proof format, handle deletion-bearing or untyped RUP-CDCL traces, or move to a stronger recognizable proof/certificate system whose ordinary proof artifact forces the support audit;
2. construct or import an explicit SAT-family/source lower-bound theorem that turns the conditional SAT calibration into an explicit hard-family statement.

Until one of these is done, the honest destination is a strong arXiv/ECCC
technical report or workshop presentation rather than a top selective-theory
submission.

## Top-Paper Gate Result

The criteria audit classifies the current revised paper as `strong_preprint_not_top_ready`.
The bounded-error randomized union-footprint gap is now closed by the accepting-union theorem.
The criteria now explicitly treat cohered results as a criterion around a sharp, novel, weighty result, and they now mark fragmented ensembles of results as a failure mode even when the individual components are technically correct.  The cohered-result spine and novelty-delta accounting make this operational: a next theorem only helps if it is flagship, calibration, interface-variant, proof-system-bridge, or boundary work that strengthens the flagship formula-footprint spine, clarifies its sharpness, proof-system reach, before/after understanding shift, or nonclaim boundary, and identifies the closest literature object it changes.  It also adds a narrative-indivisibility test: an admitted theorem should lose force, or become misleadingly motivated, if detached from the flagship theorem arc.
The revised paper now has that spine, a named formula-footprint barrier theorem, generic
identity-carrier sharpness, an internal proof-dependency audit map, a formal proof-system normalization target, a restricted displayed-atom extraction theorem, explicit-unit resolution bounds, local and auxiliary resolution bridges, extension and compressed-proof tradeoffs, support-audited and provenance/namespace-typed clausal-trace bridges, strict-prefix Qrep replay, trace-complete DPLL, antecedent-complete and RUP-complete CDCL bridges, a canonical-namespace RUP-CDCL standardizer, a carrier-independent audit upgrade criterion, a self-auditing RUP-CDCL instantiation that internalizes the decoder and support audit into the proof object itself, an append-only self-auditing RUP-CDCL instantiation that removes retained deleted-clause support records in the deletion-free case, a prefix-typed append-only RUP-CDCL instantiation that also removes the proof-internal label decoder by making formula-label variables public syntax, a prefix-typed RUP support-witness necessity result showing that public syntax alone does not certify auxiliary support-locality, an intrinsic-locality prefix-typed RUP-CDCL instantiation replacing separate auxiliary witness fields by fixed public completion-stable rules, the corresponding raw-trace and hidden-transcript separators, semantic-frontier certificate theorems, cone-budget and bounded-depth tradeoffs, and the general support-local normalization transfer theorem.  The remaining top-paper blocker is now sharper: instantiate that intrinsic rule discipline in a natural solver/proof format, handle deletion-bearing or untyped traces, or use an explicit SAT-family/source lower-bound theorem as the fallback route.
