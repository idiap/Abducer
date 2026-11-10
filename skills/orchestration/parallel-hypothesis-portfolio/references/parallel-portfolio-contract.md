<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Parallel hypothesis portfolio contract

```yaml
parallel_hypothesis_portfolio:
  portfolio_id: stable identifier
  target_id: stable target identifier
  base_theory_state_version: immutable version
  base_theory_digest: typed digest
  literature_snapshot_id: stable identifier
  literature_snapshot_digest: typed digest
  created_utc: timestamp
  dependency_dag: []
  resource_budget:
    wall_time: bound
    workers: bound
    tokens_or_cost: bound
    storage: bound
  diversity_matrix: []
  waves:
    - wave_id: stable ordered identifier
      purpose: blind_divergence | cross_pollination | maturation | synthesis_support
      depends_on_wave_ids: []
      branch_requests:
        - invocation_id: unique identifier
          branch_id: stable branch identifier
          hypothesis_id: stable hypothesis identifier
          input_digest: typed digest
          artifact_namespace: branch-local path
          allowed_skills: []
          forbidden_shared_reads: []
          budget: {}
          stop_conditions: []
          expected_theory_delta: explicit delta
      branch_receipts:
        - invocation_id: matching request identifier
          branch_id: stable branch identifier
          status: completed | timeout | failed | cancelled | invalid
          output_digest: typed digest or null
          theory_delta_ref: immutable reference or null
          failure_class: null or explicit operational class
          resource_usage: {}
          validator_receipt_ids: []
      validation_barrier:
        valid_branch_ids: []
        failed_branch_ids: []
        invalid_branch_ids: []
        partial_success_preserved: true
  partial_failure_ledger:
    preserved_branch_ids: []
    retry_branch_ids: []
    invalidated_by_dependency_ids: []
    operational_failures: []
  literature_rebase:
    frozen_snapshot_id: stable identifier
    frozen_snapshot_digest: typed digest
    newest_snapshot_id: stable identifier
    newest_snapshot_digest: typed digest
    status: current | literature_superseded | rebased
    rebase_receipt_ids: []
    required_branch_ids: []
    rebased_branch_ids: []
    blocked_branch_ids: []
  merge_proposal:
    ancestry_edges: []
    opposition_edges: []
    synthesis_edges: []
    duplicate_edges: []
    contradiction_edges: []
    pareto_frontier_ids: []
    retained_dissent_ids: []
    proposed_ledger_events: []
  reducer_receipt:
    reducer_id: stable identifier
    expected_state_version: immutable version
    committed_state_version: version or null
    compare_and_swap_status: committed | conflict | not_executed
  next_dependency_ready_wave: stable identifier or null
```

## Runtime invariants

1. Workers receive deep-copied or immutable inputs and branch-local namespaces.
2. No worker commits shared theory, literature, branch, or report state.
3. Every attempt returns a receipt, including timeout and failure.
4. Valid sibling outputs survive a partial failure.
5. Merge is single-writer and compare-and-swap guarded.
6. A newer literature snapshot forces rebase before synthesis or promotion.
7. Renderer order is deterministic but does not determine theory preference.
