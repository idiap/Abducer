<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dynamic experiment contract

Start with a probe-triage record. Persist an immutable specification and one
receipt per execution attempt only after the probe is commissioned. Canonical
serialization and digest algorithms are implementation choices, but the chosen
algorithm and versions must be recorded.

```yaml
probe_triage:
  decision: commissioned | no_probe_needed | immature_question | not_identifiable
  target_id: stable identifier or explicit_unknown
  theory_programme_id: stable identifier or explicit_unknown
  conceptual_system_ids: []
  theoretical_question_id: stable identifier or explicit_unknown
  rationale: why computation is, is not, or is not yet appropriate
  missing_maturity_fields: []
  preferable_theory_actions: []
  expected_conceptual_change_if_commissioned: explicit change or null
  forbidden_claims: []
```

For `immature_question`, name the missing maturity fields and return to theory
construction. For `no_probe_needed`, state why reflection, derivation, proof, or
reading is more decision-relevant. For preflight `not_identifiable`, show why
the declared outcomes cannot distinguish the live items and state what theory
work could change that. Do not mark these decisions as execution failure or
epistemic blockage.

```yaml
experiment_spec:
  schema_version: semantic schema version
  experiment_id: stable identifier
  target_id: stable target identifier
  run_id: stable run identifier
  branch_id: stable branch identifier
  state_version: input state version
  theory_programme_id: stable theoretical programme identifier
  conceptual_system_ids: []
  theoretical_question_id: stable mature question identifier
  theoretical_role: formal_support | counterexample | calibration | constraint | discrimination
  theory_generated_justification: why this probe is needed now
  why_theory_alone_is_currently_insufficient: explicit reason
  expected_conceptual_change: how possible outcomes would revise the theory
  question: decision-relevant question
  decision_to_change: theoretical or branch decision
  outcome_implications:
    - live_item_id: stable hypothesis, formal consequence, mechanism, or constraint identifier
      live_item_kind: hypothesis | formal_consequence | mechanism | constraint
      implication_id: stable identifier
      observable_outcome: preregistered outcome or region
      update_if_seen: favor | weaken | falsify | no_change
  decision_rule:
    regions:
      - region_id: stable identifier
        outcome_predicate: machine-checkable or precisely adjudicated predicate
        scientific_result_kind: declared result kind
        theory_updates:
          - live_item_id: stable identifier
            update: favor | weaken | falsify | no_change
    mutual_exclusivity_check: proof, validator, or explicit adjudication rule
    exhaustiveness_argument: why every valid outcome enters exactly one region
    otherwise_region: required inconclusive catch-all when exhaustiveness is not proven
  mode: exact_symbolic | bounded_model | numerical_simulation | parameter_sweep | hybrid
  stages:
    - stage_id: stable ordered identifier
      mode: exact_symbolic | bounded_model | numerical_simulation | parameter_sweep
      consumes_stage_ids: []
  mathematical_model:
    objects: []
    equations: []
    domains: []
    quantifiers: []
    assumptions: []
    invariants_preserved: []
    invariants_broken: []
    initial_conditions: []
    boundary_conditions: []
  variables:
    independent: []
    dependent: []
    controls: []
    hidden_or_constrained: []
    observables: []
  execution:
    command_or_solver: exact executable or solver ID
    source_artifacts: []
    dependency_versions: {}
    seeds: []
    parameter_grid: {}
    tolerances: {}
    resource_budget: {}
  finite_search_plan:
    applicability: required | not_applicable
    carrier_order: declared order
    parameter_bounds: {}
    completeness_argument: explicit argument or unknown
    symmetry_reduction: explicit reduction or none
    minimality_order: declared ordering
    witness_verifier: exact verifier command or solver
  statistical_plan:
    applicability: required | not_applicable
    estimand: explicit quantity
    statistical_model: explicit model
    replication_unit: independent unit
    independence_assumptions: []
    effect_or_decision_thresholds: {}
    sample_size_or_power_rule: explicit rule
    rng_algorithm: named algorithm and version
    seed_derivation_policy: explicit policy
    censoring_rule: explicit rule
    missing_or_failed_run_policy: explicit rule
    uncertainty_method: explicit interval or posterior method
    sequential_stopping_rule: explicit rule
    multiple_comparison_policy: explicit rule
    convergence_and_bias_checks: []
  controls:
    - control_id: stable identifier
      kind: baseline | null_or_knockout | boundary | known_answer | sensitivity
      applicability: required | optional | not_applicable
      specification: explicit case
      waiver_rationale: required when not_applicable
  transfer_boundary:
    model_scope: what the experiment directly addresses
    target_scope: target claim it may inform
    certificate_needed: condition required for transfer
  digest:
    algorithm: sha256
    canonicalization: named canonicalization method
    scope: spec_payload
    excluded_fields: [digest]
    value: canonical specification digest
```

```yaml
execution_receipt:
  receipt_id: stable normalized receipt identifier
  invocation_id: unique attempt identifier
  experiment_id: specification identifier
  target_id: stable target identifier
  run_id: stable run identifier
  branch_id: stable branch identifier
  state_version: input state version
  theory_programme_id: stable theoretical programme identifier
  conceptual_system_ids: []
  theoretical_question_id: stable mature question identifier
  input_digest: typed digest record
  started_utc: timestamp
  completed_utc: timestamp
  exit_status: integer or solver status
  runtime_environment: {}
  stdout_artifact: path or null
  stderr_artifact: path or null
  result_artifacts:
    - artifact_id: stable identifier
      path: run-scoped path
      media_type: MIME type
      byte_size: integer
      digest: typed digest record
  output_digest: typed digest record
  execution_status: succeeded | failed | partial | not_executed | resource_limited
  validity_status: valid | invalid | pending_validation
  identifiability: identifiable | not_identifiable | unresolved
  state_applicability: current | stale | superseded | incompatible
  control_results: []
  uncertainty_and_sensitivity:
    estimates: []
    intervals_or_posteriors: []
    bias_and_convergence_checks: []
  finite_search_evaluation:
    completeness_status: verified | unverified | not_applicable
    completeness_receipt_id: validator receipt or null
    minimality_status: verified | unverified | not_claimed
    minimality_receipt_id: validator receipt or null
  scientific_results:
    - result_id: stable identifier
      stage_id: producing stage
      kind: certificate | counterexample | no_witness_in_declared_carrier | mechanism_supported_in_model | mechanism_disconfirmed_in_model | region_narrowed | inconclusive
      value_or_witness: typed result
      verifier_or_analysis: exact verifier, proof object, or statistical analysis
      evidence_strength: exact | bounded | statistical | qualitative
      transfer_boundary: explicit boundary
  prediction_comparison:
    - implication_id: stable identifier
      observed_result_id: stable result identifier
      relation: matched | contradicted | not_distinguished | invalid
      estimate: typed estimate or null
      uncertainty: typed uncertainty or null
      decision_threshold: preregistered threshold or null
  affected_hypotheses: []
  permitted_updates: []
  reflective_assimilation_handoff:
    conceptual_systems_affected: []
    interpretation_questions: []
    permitted_theory_revisions: []
    forbidden_automatic_transitions: []
  forbidden_claims: []
  explicit_unknowns: []
  validator_receipts: []
```

Create an `experiment_spec` and `execution_receipt` only after
`probe_triage.decision: commissioned`. Other triage decisions must not fabricate
commands, identifiers, timestamps, specifications, or evidence fields.

## Replay checks

1. Resolve the immutable specification by `experiment_id` and verify its input
   digest.
2. Recreate the recorded environment or document unavoidable version drift.
3. Execute the exact command with the recorded inputs, seeds, budgets, and
   tolerances.
4. Recompute result digests and compare deterministic outputs exactly or
   stochastic summaries within preregistered tolerances.
5. Re-run negative controls and known-answer calibration.
6. Preserve historical receipt validity. If the model, code, decision rule, or
   hypotheses changed after preregistration, mark applicability to the new state
   as stale, superseded, or incompatible and require a new invocation.

## Decision and exact-search gates

- Freeze decision regions before execution. They must be mutually exclusive and
  collectively exhaustive over valid outcomes; use an explicit `inconclusive`
  catch-all when exhaustive scientific regions cannot be proven.
- Map an observation to exactly one decision region before proposing hypothesis
  updates. Outcomes outside an anticipated positive region may not be
  reclassified post hoc.
- Emit `no_witness_in_declared_carrier` only when `completeness_status` is
  `verified` and the completeness validator receipt resolves.
- Claim a smallest counterexample only when `minimality_status` is `verified`,
  the ordering was preregistered, and the minimality receipt verifies every
  preceding case in the declared carrier.

## Evidence boundaries

- Exact certificates apply only to the encoded proposition and assumptions.
- Finite counterexamples can refute a universal claim when the witness satisfies
  its domain; finite positive searches do not prove an unbounded claim.
- Simulations can support or disconfirm a mechanism in their declared model and
  regime; target transfer remains a separate obligation.
- An inconclusive or null result may still narrow a regime and should remain in
  the evidence ledger.
- Every probe must resolve to a theory-generated question and return to
  reflective assimilation. No result may choose an ontology, conceptual
  programme, or theorem status automatically.
