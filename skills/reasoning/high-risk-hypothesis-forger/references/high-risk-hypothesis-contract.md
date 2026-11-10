<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# High-risk hypothesis portfolio contract

```yaml
high_risk_hypothesis_portfolio:
  schema_version: 1.0 legacy without generation provenance | 2.0 current
  generation_provenance:
    mode: operator_instantiated_from_authored_proposals | proposal_field_free_authored_operator | proposal_field_free_provider
    proposal_request_digest: exact sealed request digest or null for authored mode
    source_proposals_digest: exact proposal-deck digest
    authored_operator_atlas_digest: exact fixed-atlas digest or null for provider/authored-proposal modes
    generator_policy_digest: exact executable-plus-policy binding or null before elicitation
    scoring_policy_digest: exact blind-rubric-plus-executable binding or null before elicitation
    claim_boundary: no creativity, truth, novelty, or efficacy inference
  portfolio_id: stable identifier
  target_id: stable target identifier
  theory_state_version: immutable version
  literature_snapshot_id: stable identifier or literature_blind_incubation
  generation_policy:
    requested_count: integer
    corner_families_required: []
    anchoring_controls: []
    target_relevance_floor: explicit rule
  hypotheses:
    - hypothesis_id: stable identifier
      corner_family: named family
      concept_lifecycle_state: intuition_seed | conceptually_articulated | literature_rebased | reflectively_supported | incubating | demoted | retired
      maturation_status: theory_question_open | formalization_needed | parallel_ready | support_ready | proof_ready
      truth_status: conjectural | open | supported | refuted | not_assessed
      intuitive_leap: concise leap
      intuition_sources: []
      new_primitives_relations_or_mechanisms: []
      target_pressures_addressed: []
      protected_successes: []
      assumptions_or_invariants_risked: []
      explanatory_upside: explicit understanding gain
      unification_upside: cases unified and differences preserved
      value_if_right: high-upside consequence
      learning_value_if_wrong: reusable negative insight
      probability_status: qualitative and explicitly uncertain
      conceptual_distance: reasoned comparison to incumbent
      literature_relation: relation or pending_rebase
      literature_source_ids: []
      non_claim_boundary: explicit boundary
      maturation_question: next theory question
      correction_conditions: []
      boundary_case: collapse, proxy, or vacuity case
      premortem:
        failure_signatures: []
        earliest_decisive_theory_test: explicit test or artifact
        disposition: invest | artifact_sprint | falsifier_sprint | reframe | demote | quarantine | stop
      branch_independence_signature:
        unique_primitives: []
        unique_mechanism: explicit mechanism
        forbidden_cross_branch_context: []
        overlaps_with_hypothesis_ids: []
  pairwise_distinction_matrix: []
  pareto_assessment: []
  protected_wildcard_ids: []
  control_hypothesis_ids: []
  parallel_branch_seeds: []
  explicit_unknowns: []
```

## Portfolio tests

- Major portfolios cover at least six genuine corner families or explain why
  the target cannot support that diversity.
- At least two protected wildcards remain after the relevance floor when viable.
- No two active seeds share the same primitives, mechanism, and maturation
  question.
- Every candidate is literature-rebased before active investment.
- Probability, reward, conceptual worth, and proof status remain separate.

## Repeated elicitation study boundary

- Preserve four non-interchangeable identities: `schedule_slot_id` for the
  pre-output opportunity, `semantic_content_id` for the exact canonical ordered
  proposal-deck bytes independent of the outer slot, `semantic_output_id` for
  slot-conditioned content, and `evidence_repetition_id` for the exact causal
  generator/adjudicator evidence. The global content identity is deliberately
  not a paraphrase-, permutation-, or formulation-invariant concept identity.
- Store the exact proposal deck, response shape, callback authority, request
  digest, and raw-response digest before adjudication.
- Reconstruct and rerun replayable generator and adjudicator callbacks during
  validation; packet-local rehashing is never causal evidence.
- Counterbalanced aliases, resolutions, ratings, warrants, dimension means,
  statuses, and eligibility are exact derived fields.
- Repetition diversity excludes run suffixes and genealogy from its semantic
  signature. It is a differentiation control, not a novelty or depth measure.
- Internal exploration/refinement may proceed only after controls pass.
  Theorem investment, physics investment, external preference, and efficacy
  require distinct evidence and remain unauthorized here.
