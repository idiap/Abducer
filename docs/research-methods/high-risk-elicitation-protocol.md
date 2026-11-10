<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Repeated High-Risk Elicitation Protocol

The canonical study API is `run_proposal_field_free_high_risk_elicitation`. It runs at least five prompt-sealed repetitions, stores and seals each exact provider proposal deck before evaluation, strips generator identity and candidate self-scores, counterbalances content aliases, and records five distinct internal criteria: essential relevance, conceptual depth, unification, corner diversity, and correction specificity. The former `run_seed_free_high_risk_elicitation` name remains an exact compatibility alias that emits only the v3 terminology.

Version 3 retains three causal identities and adds one global comparison key. `semantic_content_id` hashes only the canonical generated proposal list: it excludes target, theory, prompt, schedule, snapshot, callback authority, adjudication, and raw-response wrapper. Identical exact proposal content therefore has the same key even when it occurs in different repetitions. This is byte-level content identity, not a claim of conceptual equivalence for different formulations. It supplies exact-content provenance and deduplication only; it is not evidence of novelty, creativity, relevance, depth, unification, or efficacy.

`schedule_slot_id` names the precommitted target/theory/prompt/index/count slot and cannot depend on callback output. `semantic_output_id` combines that slot with `semantic_content_id`, so it names the slot-conditioned occurrence and remains unique when the same proposal deck appears in several scheduled repetitions. `evidence_repetition_id` additionally binds the snapshot, generator and adjudicator requests, both executable authorities, both raw responses, and both policy digests. The older `semantic_repetition_id` remains an exact alias of `semantic_output_id`; `repetition_id` remains an exact alias of `evidence_repetition_id`. Global-content forgery, alias drift, causal-identity collisions, reordered ranking, and rehashed evidence all fail closed.

Generation modes are not interchangeable. `operator_instantiated_from_authored_proposals` names the original authored-template/operator path. `proposal_field_free_authored_operator` names a deterministic control with no explicit proposal field and a fixed, digest-bound authored operator atlas. `proposal_field_free_provider` names a caller-bound provider under the same input contract. Every generated portfolio binds its generator policy and blind scoring policy; the internal mode additionally binds the exact operator atlas. The prompt screen detects known repository templates only, so proposal-field-free never means freedom from unknown or latent influence. None of these modes establishes creativity or discovery efficacy.

The copy control checks exact authored mechanism keys, every primitive/relation pair, and token-set similarity. Repetition diversity uses a second semantic signature that removes repetition suffixes and genealogy, preventing run labels alone from satisfying the control. Passing still means protocol differentiation, not novelty, depth, or value.

Validation reconstructs every provider request and blind adjudication request, reruns the supplied callbacks, and requires exact JSON equality for proposals, portfolios, aliases, order, ratings, warrants, means, authorities, and all derived digests. Custom callbacks must therefore be deterministic and declared `exact_callback_replay`; non-replayable providers are unsupported and reported as unverifiable rather than accepted on packet-local hashes. A callable fingerprint is not transitive dependency sealing.

The default adjudicator has a distinct executable authority but is internally correlated. A passed study may authorize only internal exploration and refinement. Theorem investment requires separate formal evidence, physics investment requires separate domain evidence, and efficacy is never authorized by this study. External-human evidence remains `unavailable` until real assessments are supplied.

Every v3 study also builds one equal-count authored incumbent comparison: a structurally valid authored deck scored under the identical blinded rubric. Equal candidate count and scoring do not match generation opportunity or literature exposure. The comparison with repeated proposal-field-free decks is explicitly descriptive, non-IID, non-causal, and cannot support an advantage inference. A digest-bound weighted ranking may select one repetition for internal exploration only; failed protocol controls withhold selection, and neither the incumbent comparison nor the ranking can select a true theory or authorize physics investment.

Run `python agentic/scripts/validate_seed_free_high_risk_elicitation.py` for the compatibility-located exact deterministic replay self-check; its output and packet terminology are proposal-field-free v3.

## Upstream operator integration

Production callers should use `prepare_proposal_field_free_high_risk_envelope` before dispatching `high-risk-hypothesis-forger`. The helper executes at least five equal-count repetitions against mechanism-free hidden prompts, validates and replays the complete study, and writes immutable content-addressed `study.json` and `selection.json` artifacts. Their namespace-bound byte descriptors, the selected provider proposal deck, and its exact generation provenance are then sealed inside the operator input envelope.

The selection artifact is controls-gated. A failed cross-repetition diversity or known-authored-copy control produces no downstream selection. A passing selection authorizes only internal conjectural exploration; it cannot select a true theory or authorize physics investment. The deterministic generator and blind scorer are separate executable identities but remain internally correlated, so this path makes no claim of provider independence or external creativity.

Target-authored proposals belong only in `authored_incumbent_comparison_proposals`. For Yang--Mills, the previous R01--R10 deck is retained under `_authored_domain_template_incumbent_comparison_proposals` and scored as the equal-count incumbent comparison; it is never inserted as the selected proposal-field-free provider output. Legacy callers using the former seed-free API names may still pass `authored_baseline_proposals`, which is translated only by those compatibility aliases.

Strict v1 study packets are upgraded with `migrate_seed_free_high_risk_elicitation_v1`, never by relabelling stored bytes. Migration re-executes the current provider and adjudicator callbacks, requires exact prompt, output, seal, blind-score, copy-control, and diversity replay, binds both study digests in a migration receipt, and explicitly revokes the historical seed-freedom claim. It does not retroactively establish creativity, advantage, or truth.
