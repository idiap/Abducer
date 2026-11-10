<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Literature assimilation contract

```yaml
literature_assimilation_packet:
  packet_id: stable identifier
  target_id: stable target identifier
  theory_state_version: immutable input version
  prior_snapshot_id: stable identifier or null
  refresh:
    disposition: not_needed | requested | completed | partial | failed
    request_id: stable identifier or null
    target_and_claim_scope: explicit scope
    search_lanes:
      - lane_id: stable identifier
        role: closest_work | recent_frontier | negative_barrier | genealogy | adjacent_field | dissent
        queries: []
        providers_or_indexes: []
        publication_cutoff: date or explicit unknown
        inclusion_exclusion_policy: explicit policy
        resource_budget: {}
        receipt_id: stable identifier or null
        status: not_run | completed | partial | failed
    reduction:
      work_identity_policy: DOI, arXiv, title-author, and version lineage policy
      duplicate_groups: []
      claim_conflicts: []
      reducer_receipt_id: stable identifier or null
  selected_snapshot:
    disposition: resolved | refresh_required
    snapshot_id: stable identifier or null
    content_digest: typed digest or null
    search_completed_utc: timestamp or null
    coverage_cutoff: date, explicit unknown, or null
    query_log: []
    sources_searched: []
    inclusion_exclusion_policy: explicit policy
    validator_receipts: []
    coverage_limitations: []
  resolution:
    freshness_status: current | stale | local_only | refresh_required
    candidate_snapshot_ids: []
    selection_reason: explicit reason
    target_match: pass | fail
  source_delta:
    added: []
    removed_or_retracted: []
    corrected_or_superseded: []
    newly_relevant_old_sources: []
    unchanged_decisive_sources: []
  semantic_claim_layer:
    claim_records:
      - claim_id: source/version/correction/claim-bound identifier
        source_id: stable citation identifier
        source_state:
          source_version: exact observed version
          correction_status: none_known | corrected | superseded | retracted | unknown
        exact_claim: exact source-scoped text
        extraction_provenance: exact snapshot claim or explicit missing-claim null
        effective_relation: entails | contradicts | leaves_open | unresolved
        basis_mode: source_level_explicit | bounded_lexical_fallback
        relation_warrants: []
    coverage_audit:
      explicit_warrant_claim_count: 0
      lexical_fallback_claim_count: 0
      unresolved_claim_ids: []
      corrected_or_superseded_source_ids: []
      retracted_source_ids: []
      snapshot_claim_enumeration_complete: true
      semantic_resolution_complete: false
      truth_authorized: false
      exhaustiveness_authorized: false
      novelty_authorized: false
    epistemic_nulls:
      source_truth_authorized: false
      semantic_entailment_authorized: false
      exhaustive_coverage_authorized: false
      novelty_authorized: false
      external_validation_status: unavailable
  theory_mappings:
    - source_id: stable citation identifier
      theory_object_ids: []
      relation: supports | contradicts | absorbs | sharpens | reframes | transfers | leaves_open
      exact_claim: source-scoped claim
      semantic_claim_id: exact semantic-layer claim identifier
      semantic_relation: entails | contradicts | leaves_open | unresolved
      semantic_basis_mode: source_level_explicit | bounded_lexical_fallback
      source_limitation: explicit limitation
      conceptual_change: explicit change or no_change
      confidence: status with rationale
  hypothesis_rebase_status: current | provisional_local_only | not_performed
  hypothesis_rebase:
    - hypothesis_id: stable identifier
      literature_relation: apparently_open | partly_anticipated | known_special_case | absorbed | contradicted | independent | cross_field_bridge | coverage_unknown
      source_ids: []
      required_revision: explicit change or none
      routing_effect: continue | sharpen | hybridize | targeted_reading | demote | retire | incubate
  opportunity_frontier:
    neglected_conceptual_corners: []
    cross_field_connections: []
    unresolved_source_tensions: []
    newly_available_mechanisms: []
  ledger_events: []
  stale_branch_ids: []
  explicit_unknowns: []
  next_theory_actions: []
```

## Invariants

- Resolve snapshot identity by target, validated completion time, and digest.
- Never treat a global `latest` alias as provenance.
- Every scheduling change cites a source-to-theory mapping.
- Every derived mapping cites one exact semantic claim and its warrant digest;
  source version or correction changes rebuild rather than copy the warrant.
- `entails` is a typed audit relation, not proof of mathematical entailment or
  source truth. Lexical fallback remains an internal routing heuristic.
- Coverage-only changes update the audit but remain a theory-decision null when
  no claim, source state, or relation changes.
- An apparent gap remains bounded by the recorded search coverage.
- `provisional_local_only` mappings may guide refresh questions or bounded
  incubation, but they do not satisfy the literature gate for active investment,
  synthesis, proof routing, or novelty claims.
- Rebase all survivors before synthesis when a frozen snapshot is superseded.

## Acquisition and frozen-response replay authority

The three provenance modes are intentionally non-interchangeable:

- `live` means all six lane adapters executed successfully for this acquisition;
  their receipt-backed start and completion times define its freshness origin.
- `frozen_response_replay` means no provider executed. The replay snapshot embeds
  the exact validated `live` acquisition snapshot, and every replay lane embeds
  its exact original acquisition receipt. Sources, policies, coverage metadata,
  lane times, search times, and original validator time are preserved byte for
  byte under the content digest. Replay validation reconstructs the complete
  derived snapshot from that embedded acquisition.
- `local_only` retains its prior meaning. Inline records and absent, failed, or
  mixed adapters cannot satisfy active-investment or novelty gates.

A frozen replay never obtains a new acquisition timestamp and never calls the
ambient `utc_now` clock for freshness. Assimilation requires an explicitly
injected, timezone-aware evaluation instant and a bounded max-age policy.
Present-use resolution also requires an injected trusted clock; it passes only
from the original live search completion through the original `consume_before`
deadline. Once that deadline expires, replay remains valid historical evidence
but returns `blocked_stale`. Replaying again cannot extend the deadline.

Provider output that merely labels itself `frozen_response_replay` has no replay
authority. The only admitted route is the mutually exclusive frozen-snapshot
boundary over a fully validated live acquisition whose target, theory state,
six lane requests, receipts, timestamps, and content match exactly.
