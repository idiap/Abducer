<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Acceptance Response After Closure Implementation

- Status: `implemented`
- Overall decision: `not_ready_for_selective_submission`
- Realistic venue after patches: `strong_arXiv_or_ECCC_preprint`, `workshop`, or `focused_structural_note`.

## Point-By-Point Response

| Objection | Response status | Action taken |
|---|---|---|
| Main theorems close to definitions | `demoted` | Row-forcing and quotient results are now supporting lemmas, not headline claims. |
| No nonvacuous explicit instance | `partly_closed` | Added unrestricted and rank-conditioned examples; SAT carrier remains conditional. |
| Incomplete literature comparison | `closed_for_current_scope` | Added nearest-object anchor table, direct references for Partial MCSP, circuit test suites/anti-checkers, teaching/exact specification, and lower-bound-refuter analogues, and explicit nonclaim boundaries. |
| SAT application motivational | `closed_by_demotion` | SAT section is conditional calibration only. |
| No named proof system | `partly_closed_by_restricted_bridges` | Proof-complexity claims remain demoted for strong/arbitrary-compressed standard systems, but displayed-atom, explicit resolution, support-local auxiliary, support-local extension, dependency-cone, canonical syntactic-cone, final backward-slice, slice-explicit ER, displayed acyclic ER length, expansion-bounded compressed ER, macro-compressed ER, support-declared macro ER, support-audited LRAT, provenance-typed LRAT, namespace-typed LRAT antecedent closure, strict-prefix Qrep replay, trace-complete DPLL decision logs, antecedent-complete CDCL learned-clause logs, CDCL antecedent-erasure trichotomy, RUP-complete CDCL support normalizer, canonical-namespace RUP-CDCL standardizer, carrier-independent audit upgrade criterion, self-auditing RUP-CDCL instantiation, append-only self-auditing RUP-CDCL instantiation, prefix-typed append-only RUP-CDCL instantiation, prefix-typed RUP support-witness necessity, support-audit necessity, support-erasure, plain LRAT extraction trichotomy, hidden adaptive transcript insufficiency, controller-complete adaptive audit, cone-budget, bounded-depth, and support-local transfer routes are now proved. |
| Batched dictionary issue | `closed` | Added tagged-record and masked-query patch with unchanged asymptotics. |
| No tightness/separations | `partly_closed` | Added model separations, semantic-relation support costs for nonlinear constraints, acyclic OR-tree, quotiented OR-DAG, acyclic Boolean frontier, visible adaptive frontier, and visible adaptive branching-program frontier certificates, and demoted unmatched lower bounds. |
| Randomized/interactive theorem absent | `partly_closed` | Bounded-error accepting-query union theorem is proved; expected-query and information lower bounds remain open. |
| Exploration loop | `closed` | Added closure gate policy with required result-card fields. |

## Final Theorem-Status Table

| Object | Final status |
|---|---|
| Batched dictionary lemma | `patched` |
| Formula-footprint theorem | `main_candidate_after_reframe` |
| Row-forcing theorem | `supporting_lemma` |
| Equality quotient theorem | `supporting_lemma` |
| SAT magnification application | `conditional_calibration` |
| Unrestricted standard proof-system theorem | `not_claimed` |
| Restricted proof-system bridges | `proved_for_explicit_and_support_local_interfaces` |
| Canonical syntactic-cone normalizer | `proved_for_acyclic_extension_syntax` |
| Final backward-slice lower bound | `proved_as_visible_extension_slice_budget` |
| Slice-explicit ER lower bound | `proved_as_restricted_er_style_size_lower_bound` |
| Displayed acyclic ER length lower bound | `proved_as_displayed_extension_object_length_lower_bound` |
| Expansion-bounded compressed ER transfer | `proved_as_controlled_decompression_budget_tradeoff` |
| Macro-compressed ER reuse tradeoff | `proved_as_macro_reuse_product_tradeoff` |
| Support-declared macro ER normalizer | `proved_as_sound_support_budget_tradeoff` |
| Support-audited LRAT trace normalizer | `proved_as_checker_visible_support_audit_tradeoff` |
| Provenance-typed LRAT support audit | `trusted_typed_provenance_supplies_support_audit_proved` |
| Strict-prefix Qrep replay normalizer | `proved_as_quotient_compression_replay_bridge` |
| Antecedent-complete CDCL learned-clause normalizer | `proved_as_learned_clause_antecedent_dag_bridge` |
| CDCL antecedent-erasure trichotomy | `proved_as_provenance_free_cdcl_boundary` |
| RUP-complete CDCL support normalizer | `proved_as_positive_non_plain_cdcl_bridge` |
| Canonical-namespace RUP-CDCL standardizer | `proved_as_checkable_manifest_standardizer` |
| Carrier-independent audit upgrade criterion | `proved_as_system_intrinsic_audit_extractor_target` |
| Self-auditing RUP-CDCL instantiation | `proved_as_enriched_proof_object_internalizing_decoder_live_database_rup_witnesses_and_support_audit` |
| Append-only self-auditing RUP-CDCL instantiation | `proved_as_deletion_free_self_auditing_rup_cdcl_without_retained_deleted_clause_support_annotations` |
| Prefix-typed append-only RUP-CDCL instantiation | `proved_as_typed_append_only_rup_cdcl_without_proof_internal_label_decoder_or_retained_deleted_clause_support_annotations` |
| Prefix-typed RUP support-witness necessity | `proved_boundary_public_label_typing_and_append_only_rup_checking_do_not_certify_auxiliary_support_locality` |
| Plain LRAT extraction trichotomy | `proved_as_raw_trace_add_provenance_or_pay_worst_case_or_unsound_boundary` |
| Acyclic OR-tree residual certificate | `proved_as_bounded_or_frontier_certificate` |
| OR-DAG frontier residual certificate | `proved_as_quotiented_shared_or_frontier_certificate` |
| Acyclic Boolean frontier residual certificate | `proved_as_exposed_boolean_frontier_certificate_complexity_boundary` |
| Visible adaptive frontier residual certificate | `proved_as_checker_visible_adaptive_frontier_certificate_complexity_boundary` |
| Visible adaptive branching-program frontier residual certificate | `proved_as_checker_visible_adaptive_branching_frontier_certificate_complexity_boundary` |
| Hidden adaptive transcript insufficiency separator | `proved_as_transcript_only_hidden_adaptive_boundary` |
| Randomized/interactive theorem | `bounded_error_union_footprint_proved_expected_variants_open` |
| Explicit hard SAT carrier | `future_work_quarantine` |

## Remaining Blockers Before Any Selective Submission

1. Supply an intrinsic support-locality invariant for touched auxiliary clauses, handle deletion-bearing or untyped RUP-CDCL traces, or move to a stronger recognizable proof artifact whose ordinary syntax computes support, support-locality evidence, and budget.
2. Or construct/import an explicit SAT-family or source lower-bound theorem strong enough to replace the proof-system payoff.
3. Keep bibliography synchronization as a style-level task when the decisive route is chosen.

## Venue Recommendation

- arXiv/ECCC technical report: suitable after final proofread; the current nearest-literature citation debt is resolved for this scope.
- Workshop: strong after the reframe and displayed acyclic ER bridge.
- Specialist journal note: possible if literature positioning is strengthened.
- ITCS/CCC/ICALP/LICS/STACS: still unlikely without a stronger proof-system budget theorem or explicit SAT-family theorem.
- STOC/FOCS: not competitive until the external mathematical payoff is stronger.

## Bottom Line

The loop is now closed at the strong-preprint level: the draft has a coherent
formula-footprint spine, displayed acyclic, expansion-bounded compressed ER, macro-compressed ER, support-declared macro ER, support-audited LRAT, provenance-typed LRAT, namespace-typed LRAT antecedent closure, strict-prefix Qrep replay, trace-complete DPLL decision-log bridge, antecedent-complete CDCL learned-clause bridge, CDCL antecedent-erasure boundary, RUP-complete CDCL positive bridge, canonical-namespace RUP-CDCL standardizer, carrier-independent audit upgrade criterion, self-auditing RUP-CDCL instantiation, append-only self-auditing RUP-CDCL instantiation, prefix-typed append-only RUP-CDCL instantiation, prefix-typed RUP support-witness necessity, support-audit necessity, support-erasure indistinguishability, plain LRAT extraction trichotomy, semantic-relation support, acyclic OR-frontier, quotiented OR-DAG frontier, acyclic Boolean-frontier, visible adaptive-frontier, visible adaptive branching-program-frontier, hidden adaptive transcript boundary, and controller-complete adaptive audit bridges, explicit nonclaim
boundaries, and a promotion gate.  The mathematical paper still needs one
external-weight theorem before selective top-paper submission.
