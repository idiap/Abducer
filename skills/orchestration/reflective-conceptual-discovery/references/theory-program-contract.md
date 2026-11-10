<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reflective conceptual discovery contract

Use this contract to preserve conceptual genealogy, plural theoretical virtues,
and reflective change. A theory packet may be valid with `no_probe_needed`.

```yaml
reflective_conceptual_discovery_packet:
  schema_version: semantic version
  packet_id: stable identifier
  target_id: stable target identifier
  run_id: stable run identifier
  branch_id: stable branch identifier
  prior_conceptual_state_ref: immutable state reference
  discovery_charter:
    essential_question: central theoretical question
    desired_understanding: what should become intelligible
    bottleneck_diagnosis: conceptual | representational | explanatory | formalization | proof | empirical | mixed | not_conceptual
    bottleneck_evidence: why this diagnosis fits better than the alternatives
    target_commitments: []
    relevance_horizon: why this matters to the target or field
    incumbent_framework: current theory or representation
    conceptual_opacity: what remains unintelligible
    non_claim_boundary: what this cycle will not establish
  conceptual_genealogy:
    inherited_concepts: []
    historical_or_logical_formation: []
    protected_successes: []
    rejected_or_retired_ancestors: []
    hidden_assumptions: []
  literature_basis:
    selected_snapshot_id: stable target-scoped identifier or null
    selected_snapshot_digest: typed digest or null
    search_completed_utc: timestamp or null
    freshness_status: current | stale | local_only | refresh_required | literature_blind_incubation
    search_receipt_ids: []
    assimilation_packet_ref: immutable reference or null
    source_to_theory_delta_summary: []
    literature_generated_questions: []
    coverage_limitations: []
    superseded_snapshot_ids: []
  root_tensions:
    - tension_id: stable identifier
      opposed_commitments: []
      strongest_form_of_each_side: []
      minimal_incompatibility_or_missing_mediation: exact statement
      regime: scope in which tension appears
      why_root_level: relation to essential question
  conceptual_systems:
    - system_id: stable identifier
      relation: incumbent | rival | synthesis | challenger
      lifecycle_state: seed | articulated | reflectively_revised | synthesized | theoretically_preferred | support_ready | formalization_ready | proof_ready | validated | refuted | retired
      conceptual_ancestors: []
      transformation_operations: []
      primitives: []
      ontological_commitments: []
      identities_and_differences: []
      relations_operations_and_dynamics: []
      explanatory_ideal: mechanism, constraint, structure, process, unification, or mixed
      mechanism_or_principle: explicit account
      protected_successes: []
      target_pressures_addressed: []
      formerly_inexpressible_now_visible: []
      unification_claims:
        unified_cases_or_routes: []
        common_principle: explicit principle
        differences_preserved: []
        erasure_risks: []
      implications_and_new_questions: []
      formalization_seeds: []
      correction_conditions: []
      residual_contradictions: []
      non_claims: []
  high_risk_hypothesis_portfolio:
    disposition: not_requested | generated | literature_rebased | routed | incubating
    portfolio_ref: immutable reference or null
    corner_families: []
    selected_hypothesis_ids: []
    protected_wildcard_ids: []
    control_hypothesis_ids: []
    literature_rebase_status: not_requested | pending | current | superseded
  parallel_portfolio:
    disposition: not_needed | planned | running | partially_valid | validated | rebased | merge_conflict
    manifest_ref: immutable reference or null
    frozen_theory_digest: typed digest or null
    frozen_literature_digest: typed digest or null
    branch_ids: []
    valid_receipt_ids: []
    failed_or_invalid_receipt_ids: []
    retained_dissent_ids: []
    literature_rebase_status: not_requested | current | superseded | rebased
    reducer_receipt_id: stable identifier or null
  reflection_rounds:
    - round_id: stable identifier
      system_ids: []
      lenses_used: []
      strongest_objections: []
      blind_spots: []
      mutation_or_synthesis:
        operation: explicit conceptual operation
        changed_primitives_relations_or_explanation: []
        preserved_content: []
        lost_content: []
      result: mutated | synthesized | demoted | no_change
      no_change_reason: null or explicit reason
  provisional_synthesis:
    authority_status: sealed_unique | sealed_plural | sealed_revise_all_diagnostic_only | absent_diagnostic_only | not_conceptual
    investment_authorized: boolean
    preferred_system_id: stable identifier or null
    preferred_system_ids: []
    diagnostic_synthesis_system_ids: []
    nondominated_system_ids: []
    preference_authority_evidence_id: stable identifier or null
    retained_challenger_ids: []
    stable_conceptual_core: []
    unresolved_dissent: []
    why_not_premature_convergence: explicit argument
  theory_quality_pareto:
    dimension_definitions:
      - essential_relevance
      - root_tension_contact
      - conceptual_depth
      - explanatory_understanding
      - unification_power
      - preservation_of_difference
      - generativity
      - coherence
      - truth_aptness
    system_assessments:
      - system_id: stable identifier
        relevance_floor: pass | fail | open
        dimensions:
          essential_relevance: judgment with evidence
          root_tension_contact: judgment with evidence
          conceptual_depth: judgment with evidence
          explanatory_understanding: judgment with evidence
          unification_power: judgment with evidence
          preservation_of_difference: judgment with evidence
          generativity: judgment with evidence
          coherence: judgment with evidence
          truth_aptness: judgment with evidence
        decisive_strengths: []
        decisive_weaknesses: []
        explicit_tradeoffs: []
    nondominated_system_ids: []
    dominated_or_demoted_systems: []
  understanding_delta:
    authority_status: same authority status as provisional_synthesis
    conceptual_system_ids: exact ordered preferred or diagnostic set
    authority_distinct_merit_evidence: false
    claim_boundary: internal_correlated_structural_change_only | ordinary_bottleneck_localization_only
    system_deltas:
      - conceptual_system_id: exact retained system
        before: what was opaque or fragmented
        after: what becomes structurally expressible for this system
        perspective_shifts: []
        explanatory_compressions: []
        new_distinctions: []
        productive_contradictions: []
        remaining_opacity: []
    before: what was opaque or fragmented
    after: set-preserving aggregate structural account, not independent merit evidence
    perspective_shifts: []
    explanatory_compressions: []
    new_distinctions: []
    productive_contradictions: []
    remaining_opacity: []
  theoretical_programme:
    programme_id: stable aggregate identifier
    authority_status: same authority status as provisional_synthesis
    conceptual_system_ids: exact ordered preferred or diagnostic set
    investment_authorized: boolean
    component_programmes:
      - component_programme_id: stable system-bound identifier
        conceptual_system_id: exact retained system
        investment_authorized: boolean
        definitions_to_build: []
        relations_or_mechanisms_to_formalize: []
        consequences_to_derive: []
        proof_or_model_obligations: []
        next_theory_actions: []
    definitions_to_build: []
    relations_or_mechanisms_to_formalize: []
    consequences_to_derive: []
    proof_or_model_obligations: []
    literature_questions: []
    next_theory_actions: []
  support_probe:
    disposition: no_probe_needed | proposed | commissioned | assimilated
    theory_programme_id: exact aggregate programme or null
    theoretical_question_id: stable identifier or null
    conceptual_system_ids: exact complete preferred set or []
    theoretical_question: null or precise mature ambiguity
    role: conceptual_counterfactual | symbolic_derivation | finite_countermodel | proof_attempt | literature_inquiry | simulation
    why_theory_alone_is_currently_insufficient: null or explicit reason
    possible_theory_updates: []
    receipt_ids: []
    reflective_assimilation_event_ids: []
  stage_gates:
    G0_essential_relevance: pass | fail | open
    G0L_literature_rebase: pass | fail | open | not_required
    G1_genuine_transformation: pass | fail | open
    G2_philosophical_depth: pass | fail | open
    G3_unification: pass | fail | open
    G4_understanding_gain: pass | fail | open
    G5_reflective_resilience: pass | fail | open
    G6_truth_apt_articulation: pass | fail | open
    G7_claim_promotion: pass | fail | not_requested
  truth_convergence_status:
    conceptual_preference: status
    internal_coherence: status
    formal_support: status
    model_or_experimental_support: status
    proof_status: status
  plateau:
    materially_empty_rounds: integer
    equivalence_basis: how paraphrases were identified
    action: continue | reframe | incubate | retire
  next_reflective_action:
    kind: reflect | reframe | differentiate | synthesize | formalize | derive | compare | read | prove | probe | incubate | retire
    question: exact question
    expected_conceptual_change: explicit delta
  conceptual_adjudication_evidence: complete sealed object or null
  evaluation_receipt_ids: diagnostic receipt identities only; never preference authority
```

## Contract invariants

- A `not_conceptual` diagnosis may route directly to derivation, proof, reading,
  or empirical work and does not require invented rival conceptual systems.
- A conceptual state transition may be substantive with `no_probe_needed` when
  it passes `G0` through the applicable part of `G6`.
- A major portfolio may generate intuition seeds while `G0L` is open, but no
  candidate receives active investment, enters synthesis, or supports a novelty
  claim until the newest admissible target-scoped snapshot is assimilated and
  that candidate is rebased.
- Seal a pre-map policy after acquisition and before mapping, warrants, or
  assimilation. Seal a separate realization over completed assimilation. Later
  operators consume both; a late realization never gains earlier-stage authority.
- The sealed blind adjudicator is the sole internal preference authority. Bind
  final adjudication to complete parent evidence whenever synthesis changes the
  candidate set. Receipt IDs, structural scores, callers, and committers cannot
  choose a preferred system.
- Carry `prefer_unique`, `retain_plural_nondominated`, `revise_all`, and absent
  authority without partial functions. A singular convenience exists only for
  `prefer_unique`; every plural member receives an exact component programme.
- Under `revise_all`, preserve every nondominated diagnostic system, authorize no
  investment or support probe, and emit only correction, differentiation,
  reflection, or incubation work.
- Keep `G2` and `G4` open under locally authored or correlated evaluation.
  Per-system structural deltas do not establish independent philosophical depth,
  understanding, creativity, unification advantage, or physics value.
- `G7` is required only for established-claim promotion. It must never be
  inferred from conceptual preference or simulation support.
- Every reflection round must change a system, synthesize systems, demote a
  system, or record an explicit `no_change` reason.
- Unification must list both unified cases and differences preserved.
- Keep at least one nondominated challenger unless it fails relevance or a
  non-negotiable target commitment.
- Do not invalidate historically useful conceptual ancestors when they are
  superseded; preserve the genealogy and the reason for revision.
- A support probe is commissioned by a theoretical question and returns to
  reflective assimilation. It cannot choose the ontology or write proof status.
- A five-world experiment uses one pre-execution commission and compares complete
  committed theory/schedule projections. Only its registered-premise falsifier
  may request later reflection; no world directly selects theory, proof, or evidence.
- Category Theory and HoTT outputs require executable finite-formal receipts plus
  exact carrier, quantifier, regime, correction, burden, falsifier, overhead, and
  failure handbacks. Finite equivalence never implies continuum or physical equivalence.
- A parallel worker never reads a mutable `latest` alias or writes shared theory
  state. Valid sibling results survive partial failure, and only a
  compare-and-swap reducer may commit their merged events.
