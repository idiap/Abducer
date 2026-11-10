<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reflective Discovery Operator Routes

This file is generated from `agentic/registries/discovery_operator_registry.yaml`.
It documents execution and authority boundaries; registry presence alone is not an execution receipt.
Every command below is an argv vector executed without a shell. Each successful route also requires a separate validator subprocess and a digest-valid receipt.

- Registry digest: `sha256:cf81e234bc217f9b60f1fdc3236a6d712dbc134d6aa37ae2300e9b9d0aa86de3`
- Parent operator: `reflective-conceptual-discovery`
- Canonical state writer: `discovery-epistemic-reducer`
- Experiments: conditional, theory-requested support only

## Canonical central conceptual route producer

- Route/version: `central-formal-conceptual-routes-v3` / `3.0.0`
- Production API: `agentic.discovery:run_central_conceptual_routes`
- Invocation: `typed_python_facade_with_live_store_verified_commit_and_process_wave`
- Generic dispatcher: `disabled`
- Exact route registry: `agentic/registries/central_conceptual_route_registry_v3.yaml`
- Matched route order: `["categorical", "hott", "category_then_hott", "hott_then_category", "capable_nonformal"]`
- Structural packet validator: `agentic.discovery:decode_central_conceptual_route_packet`
- Active-current validator: `agentic.discovery:reopen_authoritative_central_conceptual_route_packet`
- Serializable production CLI: `no`
- Execution: five equal-budget process authors with required overlap, a terminal barrier, and one content-only set-valued blind judge.
- Reflection effect: eligible input only for the exact canonical head `N` to compare-and-swap descendant `N+1` intake; no same-generation theory mutation or direct state write.
- Authority: no truth, conceptual-merit, creativity, relevance, depth, philosophical-understanding, unification, formal-advantage, theorem, continuum, Yang–Mills, or physics-value authority.

## Canonical descendant experiment producer

- Route/version: `canonical-descendant-experiment-v3` / `3.0.0`
- Production API: `agentic.experiments:run_canonical_descendant_experiment_v3`
- Invocation: `typed_python_facade_with_parallel_callbacks`
- Generic dispatcher: `disabled`
- Read-only replay command: `["python", "-m", "agentic.scripts.validate_world_v3_descendant_chain", "--workspace", "."]`
- Replay command produces canonical state: `no`
- Chronology: committed theory `N`; anchor `N+1`; five parallel-produced, serially committed worlds `N+2..N+6`; aggregation `N+7`; immutable later-cycle reflection input `N+8`.
- Authority: later-cycle reflection input only; no current-theory mutation, automatic selection, proof, or physics authority.

## reflective-conceptual-discovery

- Role: `theory_parent`
- Version/kind: `1.0.0` / `theory`
- Parent: `root`
- Conditional: `no`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/orchestration/reflective-conceptual-discovery/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "reflective-conceptual-discovery", "--workspace", "."]`
- Independent validators: `reflective-conceptual-discovery-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "reflective-conceptual-discovery", "--workspace", "."] [explicit_local_semantic_closure; 20 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `target_id`, `run_id`, `state_version`, `discovery_charter`, `conceptual_genealogy`
- Domain payload schemas: `agentic/spec/discovery_epistemic_state.schema.json`
- Output schemas: `agentic/spec/reflective_conceptual_discovery_packet.schema.json`
- Required consumers: `discovery-epistemic-reducer`, `discovery-information-scheduler`
- Allowed state effects: `propose_ledger_events`, `request_reducer_commit`
- Feedback effect: Reflection and synthesis alter the canonical theory programme and next theoretical action.

## reflective-theory-synthesizer

- Role: `theory_reflection`
- Version/kind: `1.0.0` / `theory`
- Parent: `reflective-conceptual-discovery`
- Conditional: `yes`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/reasoning/reflective-theory-synthesizer/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "reflective-theory-synthesizer", "--workspace", "."]`
- Independent validators: `reflective-theory-synthesis-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "reflective-theory-synthesizer", "--workspace", "."] [explicit_local_semantic_closure; 20 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `target_id`, `run_id`, `state_version`, `discovery_charter`, `conceptual_genealogy`
- Domain payload schemas: `agentic/spec/reflective_conceptual_discovery_packet.schema.json`
- Output schemas: `agentic/spec/reflective_conceptual_discovery_packet.schema.json`
- Required consumers: `reflective-conceptual-discovery`
- Allowed state effects: `propose_ledger_events`
- Feedback effect: At least two rounds mutate, synthesize, demote, or record an honest plateau before convergence.

## formal-claim-producer

- Role: `typed_formal_claim_compilation`
- Version/kind: `2.0.0` / `proof`
- Parent: `reflective-conceptual-discovery`
- Conditional: `yes`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/reasoning/formal-claim-producer/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "formal-claim-producer", "--workspace", "."]`
- Independent validators: `formal-claim-producer-validator@2.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "formal-claim-producer", "--workspace", "."] [derived_repository_closure_v2; 4 Python roots + 3 semantic roots; recursive closure]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `source_producer_request`, `source_producer_receipt`, `source_semantic_row_id`, `source_theory_programme_id`, `literature_authority`, `theory_ancestry`
- Domain payload schemas: `agentic/spec/discovery_formal_claim_producer_input_v2.schema.json`
- Output schemas: `agentic/spec/discovery_formal_claim_producer_output_v2.schema.json`
- Required consumers: `canonical-discovery-cycle`, `discovery-information-scheduler`
- Allowed state effects: `propose_formal_claim_packet`
- Feedback effect: A sealed typed seed yields a ready-or-not-ready formal-claim packet; only a later committed authority join can make a ready packet eligible for proof scheduling.

## blind-conceptual-preference-adjudicator

- Role: `sealed_plural_conceptual_preference`
- Version/kind: `2.0.0` / `evaluation`
- Parent: `reflective-conceptual-discovery`
- Conditional: `no`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/evaluation/blind-conceptual-preference-adjudicator/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "blind-conceptual-preference-adjudicator", "--workspace", "."]`
- Independent validators: `blind-conceptual-preference-adjudication-validator@2.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "blind-conceptual-preference-adjudicator", "--workspace", "."] [explicit_local_semantic_closure; 5 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `blind_packet`, `judge_reports`, `systems`, `reflection_rounds`, `frozen_genealogy`, `candidate_bindings`, `theory_state_digest`, `literature_snapshot_digest`, `high_risk_portfolio_digest`, `proposer_receipt_ids`, `created_at`
- Domain payload schemas: `agentic/spec/conceptual_adjudication.schema.json`, `agentic/spec/conceptual_adjudication_evidence.schema.json`
- Output schemas: `agentic/spec/conceptual_adjudication_evidence.schema.json`
- Required consumers: `reflective-conceptual-discovery`, `discovery-epistemic-reducer`, `discovery-information-scheduler`
- Allowed state effects: `propose_sealed_preference_evidence`
- Feedback effect: A sealed blind panel authorizes only its exact set-valued outcome; plural nondominated and revise-all results remain first-class.

## frontier-literature-assimilator

- Role: `literature_assimilation_and_rebase`
- Version/kind: `1.0.0` / `literature_assimilation`
- Parent: `reflective-conceptual-discovery`
- Conditional: `no`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/reasoning/frontier-literature-assimilator/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "frontier-literature-assimilator", "--workspace", "."]`
- Independent validators: `frontier-literature-assimilation-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "frontier-literature-assimilator", "--workspace", "."] [explicit_local_semantic_closure; 20 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `snapshot`
- Domain payload schemas: `agentic/spec/target_literature_search_snapshot.schema.json`, `agentic/spec/theory_object_catalog.schema.json`, `agentic/spec/literature_claim_mapping_derivation.schema.json`
- Output schemas: `agentic/spec/literature_assimilation_packet.schema.json`
- Required consumers: `high-risk-hypothesis-forger`, `discovery-information-scheduler`, `reflective-conceptual-discovery`
- Allowed state effects: `propose_ledger_events`, `block_stale_investment`
- Feedback effect: Claim-level source mappings can spawn, merge, split, reframe, demote, retire, or reprioritize theory branches.

## high-risk-hypothesis-forger

- Role: `conceptual_divergence`
- Version/kind: `1.0.0` / `hypothesis`
- Parent: `reflective-conceptual-discovery`
- Conditional: `no`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/reasoning/high-risk-hypothesis-forger/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "high-risk-hypothesis-forger", "--workspace", "."]`
- Independent validators: `high-risk-hypothesis-portfolio-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "high-risk-hypothesis-forger", "--workspace", "."] [explicit_local_semantic_closure; 20 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `charter`, `literature_snapshot`
- Domain payload schemas: `agentic/spec/target_literature_search_snapshot.schema.json`, `agentic/spec/literature_assimilation_packet.schema.json`
- Output schemas: `agentic/spec/high_risk_hypothesis_portfolio.schema.json`
- Required consumers: `parallel-hypothesis-portfolio`, `reflective-conceptual-discovery`
- Allowed state effects: `propose_ledger_events`
- Feedback effect: Structurally distinct conceptual corners and protected wildcards alter the live theory portfolio.

## parallel-hypothesis-portfolio

- Role: `isolated_parallel_maturation`
- Version/kind: `1.0.0` / `hypothesis`
- Parent: `reflective-conceptual-discovery`
- Conditional: `yes`
- Dispatch enabled: `yes`
- Production status: `active`
- Skill: `skills/orchestration/parallel-hypothesis-portfolio/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "parallel-hypothesis-portfolio", "--workspace", "."]`
- Independent validators: `parallel-hypothesis-portfolio-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "parallel-hypothesis-portfolio", "--workspace", "."] [explicit_local_semantic_closure; 20 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `high_risk_portfolio`
- Domain payload schemas: `agentic/spec/high_risk_hypothesis_portfolio.schema.json`
- Output schemas: `agentic/spec/parallel_hypothesis_portfolio.schema.json`
- Required consumers: `reflective-conceptual-discovery`, `discovery-epistemic-reducer`
- Allowed state effects: `write_branch_namespace`, `propose_single_cas_merge`
- Feedback effect: Independent valid siblings and dissent survive partial failure and reach one conflict-preserving reducer merge.

## canonical-causal-artifact-producer

- Role: `local_causal_artifact_evidence`
- Version/kind: `1.0.0` / `support_probe`
- Parent: `reflective-conceptual-discovery`
- Conditional: `yes`
- Dispatch enabled: `no`
- Production status: `history_only`
- Skill: `skills/reasoning/dynamic-symbolic-simulation-experimenter/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_causal_artifact_producer", "--workspace", "."]`
- Independent validators: `canonical-causal-artifact-producer-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_causal_artifact_producer", "--workspace", "."] [explicit_local_semantic_closure; 1 local semantic dependencies]`
- Input envelope: no input artifacts; request parameters: `causal_stage_id`, `producer_role`, `artifact_id`, `artifact_digest`, `artifact_value`, `evidence_authority_id`, `authority_boundary`
- Domain payload schemas: none
- Output schemas: none
- Required consumers: `canonical-theory-support-lane`
- Allowed state effects: `write_identity_local_causal_evidence`
- Feedback effect: Binds exact local request, receipt, output history, artifact, dependency, and clock bytes without external, theory-selection, proof, or physics authority.

## dynamic-symbolic-simulation-experimenter

- Role: `optional_theory_support`
- Version/kind: `1.0.0` / `support_probe`
- Parent: `reflective-conceptual-discovery`
- Conditional: `yes`
- Dispatch enabled: `no`
- Production status: `history_only`
- Skill: `skills/reasoning/dynamic-symbolic-simulation-experimenter/SKILL.md`
- Command argv: `["python", "-m", "agentic.scripts.run_discovery_operator_protocol", "--operator-id", "dynamic-symbolic-simulation-experimenter", "--workspace", "."]`
- Independent validators: `dynamic-symbolic-simulation-experiment-validator@1.0.0 ["python", "-m", "agentic.scripts.validate_discovery_operator_protocol", "--operator-id", "dynamic-symbolic-simulation-experimenter", "--workspace", "."] [explicit_local_semantic_closure; 28 local semantic dependencies]`
- Input envelope: exactly 1 digest-bound `application/json` artifact; required fields: `triage_request`, `experiment_request`
- Domain payload schemas: `agentic/spec/dynamic_probe_triage.schema.json`, `agentic/spec/dynamic_experiment_spec_v3.schema.json`
- Output schemas: `agentic/spec/dynamic_experiment_receipt_v3.schema.json`
- Required consumers: `reflective-conceptual-discovery`
- Allowed state effects: `write_branch_namespace`, `propose_evidence_events`
- Feedback effect: Only a commissioned mature theory question can produce model-scoped evidence, which returns to reflection without selecting a theory.

## Post-synthesis derived artifacts

These artifacts are not independently dispatched operators. They are derived by the canonical cycle only after their exact causal inputs have been verified.

### dynamic-experiment-post-result-reflection

- Producer/stage: `canonical-discovery-cycle` / `post_synthesis_after_experiment_result_consumption`
- Schema: `agentic/spec/dynamic_experiment_reflection_receipt_v1.schema.json`
- Exact causal inputs: experiment_spec (artifact_role:experiment_spec[0]), experiment_receipt (artifact_role:experiment_receipt[0]), source_reflection_packet (artifact_role:reflective_packets[0]), result_reflection_packet (artifact_role:reflective_packets[1]), synthesis_operator_receipt (successful_operator_receipt:reflective-theory-synthesizer[None])
- Interpretation: records the executed post-result reflection decision; it cannot mutate theory, ontology, selection, proof, evidence relations, or schedule directly.

## Provenance and commissioning boundaries

- `frontier-literature-assimilator` never performs or fabricates a remote search. It consumes an already frozen, schema-valid snapshot from the explicit provider boundary: receipt-backed `live` provenance can authorize a bounded current rebase, while inline/static inputs remain `local_only` and block active investment and novelty claims.
- `central-formal-conceptual-routes-v3` is reachable only through its typed live-store/verified-commit facade. Its exact five-route registry, structural decoder, and active-current reopener are validator surfaces, not a serializable producer CLI or a generic dispatcher binding.
- `canonical-descendant-experiment-v3` is invoked only through its typed Python facade. Its locator-based command is a read-only active-current replay validator and is never a producer or generic dispatcher binding.
- `dynamic-symbolic-simulation-experimenter` is a history-only reader. New experiment production must use the typed canonical descendant facade.
- `dynamic-experiment-post-result-reflection` is history-only; the canonical descendant route commits the immutable later-cycle reflection input at `N+8`.
- A route is exercised only when the command ran, every declared output was hashed, the independent validator passed the exact hashes, and the resulting receipt validates against `discovery_operator_receipt.schema.json`.

## Reusable batch execution

Use `python -m agentic.scripts.dispatch_discovery_operators --requests <requests.json> --registry <registry.json> --workspace <workspace> --receipts <receipt-root> --manifest <workspace-relative-manifest.json>` to execute caller-prepared digest-bound requests.
The optional manifest records exact receipts and candidate consumers, but fixes `feedback_committed` and every candidate `consumed`/`state_edge_committed` field to `false`. Only the canonical cycle/reducer may later attest those edges.
