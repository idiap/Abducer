<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof-System Instantiation Decision

- Status: `implemented`
- Decision: `demote_standard_proof_complexity_claims_but_keep_restricted_bridges`

## Decision

Do not claim a lower bound for Cutting Planes, Polynomial Calculus, Frege,
Extended Frege, IPS, implicit proofs, unrestricted extended resolution, or any
other less-local standard proof system in the current paper.

The draft currently proves lower bounds for abstract completion-sound
certificate models:

- formula-label certificates;
- private occurrence-label certificates;
- equality-quotient parity certificates.

Those models are useful, but a standard proof-system theorem would require an
extraction or normalization statement:

\[
  \text{short proof in system } P
  \quad\Longrightarrow\quad
  \text{small completion-sound certificate in one of the paper's models}.
\]

The revised paper now proves several restricted extraction and normalization
statements: displayed atoms, explicit resolution assumptions, full-assignment
resolution unit core, explicit local resolution clauses, support-local auxiliary
resolution, support-local extension resolution, dependency-cone extension
normalization, canonical syntactic-cone normalization, final backward-slice
lower bounds, slice-explicit ER lower bounds, displayed acyclic ER length lower bounds,
expansion-bounded compressed ER transfer, macro-compressed ER reuse tradeoff,
support-declared macro ER normalizer, support-audited LRAT trace normalizer, cone-budget,
provenance-typed LRAT support audit, namespace-typed LRAT antecedent closure, strict-prefix Qrep replay, trace-complete DPLL decision-log normalizer, antecedent-complete CDCL learned-clause normalizer, CDCL antecedent-erasure trichotomy, RUP-complete CDCL support normalizer, canonical-namespace RUP-CDCL standardization, self-auditing RUP-CDCL instantiation, append-only self-auditing RUP-CDCL instantiation, prefix-typed append-only RUP-CDCL instantiation, plain LRAT extraction trichotomy, exposed acyclic Boolean frontier support, visible adaptive frontier support, bounded-depth tradeoffs, and a general support-local transfer theorem.  These
still do not amount to a lower bound for a less-local standard system, because
the current concrete CDCL bridge is enriched by checker-visible audit fields.
The top-paper route therefore needs a proof format that removes the remaining
support-local witness obligation, handles deletion-bearing or untyped traces, or
has fewer typed audit obligations than the prefix-typed append-only RUP-CDCL bridge,
a controlled expansion theorem for that proof format, or a non-plain
system-specific invariant that supplies the hidden adaptive semantic support
missing from raw trace syntax, partial solver traces, raw RUP/DRUP without
support parsing, or arbitrary CDCL logs.

## Why A Toy System Is Not Enough

One could define a restricted explicit-atom oracle system whose proof lines are
only displayed formula labels, occurrence labels, or equality links.  But if
the rules simply require occurrence locality by definition, the resulting lower
bound is tautological: it restates the certificate model rather than deriving it
from proof rules.

To be claimable, the system must satisfy at least one of:

1. It is a recognizable restriction of a standard proof system.
2. Its locality follows from proof rules rather than being stipulated.
3. It proves an extraction theorem with controlled overhead from proof length
   to certificate size.

The current draft satisfies these requirements only for deliberately restricted
interfaces where faithful formula-label information is explicit,
support-local, or syntactically reachable in an acyclic extension graph.

## Updated Theorem Status

| Claim | Status |
|---|---|
| Formula-label certificate lower bound | `kept` |
| Occurrence-label certificate lower bound | `kept_as_supporting` |
| Equality-quotient certificate lower bound | `kept_as_supporting` |
| Proof-size lower bound for a named system | `not_claimed` |
| Restricted resolution/support-local bridges | `proved_in_revised_tex` |
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
| Trace-complete DPLL decision-log normalizer | `proved_as_controller_complete_DPLL_log_bridge` |
| Antecedent-complete CDCL learned-clause normalizer | `proved_as_learned_clause_antecedent_dag_bridge` |
| CDCL antecedent-erasure trichotomy | `proved_as_provenance_free_cdcl_boundary` |
| RUP-complete CDCL support normalizer | `proved_as_positive_non_plain_cdcl_bridge` |
| Canonical-namespace RUP-CDCL standardizer | `proved_as_checkable_manifest_standardizer` |
| Carrier-independent audit upgrade criterion | `proved_as_system_intrinsic_extractor_target` |
| Self-auditing RUP-CDCL instantiation | `proved_as_enriched_proof_object_internalizing_decoder_live_database_rup_witnesses_and_support_audit` |
| Append-only self-auditing RUP-CDCL instantiation | `proved_as_deletion_free_self_auditing_rup_cdcl_without_retained_deleted_clause_support_annotations` |
| Prefix-typed append-only RUP-CDCL instantiation | `proved_as_typed_append_only_rup_cdcl_without_proof_internal_label_decoder_or_retained_deleted_clause_support_annotations` |
| Prefix-typed RUP support-witness necessity | `proved_boundary_public_label_typing_and_append_only_rup_checking_do_not_certify_auxiliary_support_locality` |
| Plain LRAT extraction trichotomy | `proved_as_raw_trace_add_provenance_or_pay_worst_case_or_unsound_boundary` |
| Exposed acyclic Boolean frontier support | `proved_as_interface_boundary_not_hidden_adaptive_sat_semantics` |
| Visible adaptive frontier support | `proved_as_interface_boundary_for_checker_visible_adaptive_control_not_hidden_adaptive_semantics` |
| Proof-complexity motivation | `allowed_with_explicit_normalization_boundary` |

## Paper Text To Add

Any sentence suggesting proof-complexity significance should be followed by:

> Turning these restricted certificate lower bounds into lower bounds for a
> less-local standard proof system requires a nontrivial normalization theorem
> that proves controlled expansion or a non-plain semantic invariant for the
> proof objects of that system.
> We do not prove that
> stronger theorem here.

## Future Work Entry

Open problem: supply an intrinsic support-locality invariant for touched
auxiliary clauses, handle deletion-bearing or untyped RUP-CDCL traces, or move
toward a less annotated or arbitrary-compressed recognizable proof system by
deriving support, support-locality evidence, and budget from the ordinary proof
artifact itself.  The prefix-typed support-witness necessity proposition shows
that public label syntax plus append-only RUP checking cannot remove the
support-locality assumption by itself.
Alternatively, replace the proof-system route with an explicit
SAT-family/source lower-bound theorem.  The budget must be a theorem, not a
definition of the system.
