<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# CoreReasoningMechanismModel 2.0.0

This JSON-compatible manual authoring contract implements [the shared conceptual inquiry contract](conceptual-inquiry-contract.md). It is not a registered runtime schema, executable proof, or new fixed-runner stage. Version 2 removes the closed operator-first kind taxonomy and adds a source-grounded conceptual inquiry as the organizing structure. Version 1 packets remain historical records; this lane requires re-curation, not relabeling.

## Envelope

| Field | Content |
| --- | --- |
| `schema_version`, `model_id` | Literal `2.0.0` and stable model ID |
| `source_bindings` | Packet/model IDs, artifact kinds and exact evidence-index digests; distinguish source digest from artifact byte hash |
| `paper_context` | Audience, question, contribution, scope, and length guidance |
| `conceptual_inquiry` | Situation, tension, diagnosis, alternatives, reflection, comparison, and revision records below |
| `inventory` | Explanatory component records: `component_id`, name, open `conceptual_role`, sources, selection (`selected`, `excluded`, `deferred`, `blocked`), and reason |
| `scope_component_ids` | Unique selected component IDs, retaining blocked requested components |
| `mechanisms` | Explanatory cards below; the historical field name does not impose an operator ontology |
| `coverage` | One row per scoped component with card, placement, status, reason |
| `relationships` | Source-bound conceptual links, with dependency, revisitation, and native execution order distinguished |
| `native_annotations` | Optional many-to-many mapping from inquiry/card IDs to source operator/binding IDs, with relationship, origin, limitation, and evidence |
| `argument_plan` | Question-led anchors, explanatory dependencies, narrative order, formal support placement, appendix preservation |
| `candidate_claims` | Proposed wording, affected IDs, support/counterevidence, scope, caveats, requested section |
| `unresolved` | Missing inputs, disagreements, and obligations with affected IDs and reasons |

Source references resolve to the frozen evidence index and identify packet/model, exact evidence/construct ID, applicable layer/profile, and origin (`native`, `source_descriptive`, `proposed_refinement`). An existing manuscript taxonomy establishes its chosen notation, not universal cognition or observed execution. Refresh stale inputs before review.

## Conceptual inquiry record

- `situation`: target question/identity, incumbent primitives, identities and differences, relations, representations, explanatory ideal, protected successes, genealogy, current opacity, and sources.
- `tensions`: IDs, strongest opposed commitments, protected content on each side, regime, precise incompatibility or missing mediation, and why it is central. Do not caricature a rival or assume all tensions are contradictions.
- `diagnosis`: `kind` (`conceptual`, `representational`, `explanatory`, `mixed`, `not_conceptual`, `unresolved`), grounds, counterevidence, and `next_task`. A `not_conceptual` record includes an actual calculation/proof/reading/formalization/measurement handoff and marks downstream invention records `not_applicable` with reason; no fabricated rivals are required. `unresolved` remains blocked where evidence is necessary.
- `alternatives`: stable system IDs including incumbent; changed primitives/identities/relations/representations/mechanisms, explanatory differences, ancestors, protected successes, preserved differences, lost structure, regimes, non-claims, and sources. Explain why each change is more than renaming.
- `reflection`: rows for the six focus lenses in the shared contract, each with `lens`, `system_ids`, disposition (`applied`, `not_applicable`, `blocked`), reason, exposed assumption, protected content, mutation or justified `no_change`, new risk, and source refs. Additional source lenses may be recorded. These rows are not six executed stages.
- `comparison`: systems compared, relevance floor, criterion-specific reasons/evidence, explicit trade-offs, nondominated/retained rivals, unresolved dissent, and preference authority or its absence. No scalar score or list order silently decides the outcome.
- `understanding_delta`: before, after, newly expressible distinctions, unified cases, differences preserved, remaining opacity, and illustrative/observed posture.
- `consequences_and_revision`: new questions, formalization or support obligations, boundary cases, correction conditions, revision triggers, and next action. Separate conceptual preference from formal/model/experimental support and proof.

Each record has source refs and clear reconstruction/interpretation/proposal status. Requested inquiry dimensions need explicit dispositions even where blocked or not applicable.

## Explanatory card

Each card has stable `mechanism_id`, `component_ids`, name, open `conceptual_role`, inquiry record IDs, and status (`ready`, `draft`, `blocked`). Roles describe the source-grounded explanatory work, such as diagnosing a representational bottleneck or preserving a difference through synthesis; this is not a closed classification.

Retain `problem`, `input_state`, `conceptual_move`, `output_state`, `changed_knowledge`, `warrant_and_invariants`, `why_needed`, `example`, `claim_ceiling`, `source_refs`, and `candidate_claim_ids`. An example contains posture, concrete inputs, substantive intermediate reasoning, outcome, contrast, limits, and evidence refs. Mixed examples label each observation or invented transition. Explain a real alternative, boundary, or changed condition and its consequence; an arrow or field list is insufficient.

An optional `native_annotations` reference can connect a card to several operator families, while one family can annotate multiple cards. Unmapped conceptual work remains explicitly unmapped. Domain primitives under reconsideration are not the same thing as the framework's inference operators. Existing primitive/composition/motif descriptions may be preserved as source annotations, but are not required card kinds or narrative stages.

## Coverage, argument, and review

A coverage row records component/card IDs, placement (`anchor`, `compressed_main_text`, `appendix`, `unresolved`), status, and reason. Main-text anchors each need substantive explanation and example content, which may be shared within the continuous case. Blocked rows state the missing evidence instead of supplying fictional completion. Reconcile scope changes with the blueprint.

Relationships name involved IDs, relation meaning, retained context, source refs, origin, and order status. Separate reader prerequisites, conceptual revisitation, native topology, and actual execution. Matching type endpoints do not establish equivalence. `argument_plan` explains why situation/tension and diagnosis precede the paper's supporting operator notation, where the running case makes alternatives and reflection concrete, and how comparison leads to revisable consequences. This is an expository organization, not a universal method chronology.

Keep exhaustive workflow/type/operator material subordinate while preserving complete frozen appendix scope and all occurrence explanations under the step contract. Manual review checks diagnostic exit, substantive alternatives, each focus-lens disposition, preservation/loss, plural comparison, consequences/correction, exact sources, authorized claims, and whether readers understand the argument without operator symbols. Counts, packet completeness, compilation, and locally authored judgments do not establish conceptual depth, efficacy, or truth. Record review as manual and return weak or operator-first cards for revision.

## Optional manual recursion and workflow supplement

For a requested account of recursive goals or workflow relationships, accompany the reviewed model with a separately identified supplement governed by [the shared contract](recursive-goals-and-workflow-relations.md). Keep the 2.0.0 envelope and existing closed runner schemas unchanged. The supplement records goal revisions, bounded attempts, parent enablement, AND/OR dependency meanings, stop/reopen conditions, all scoped workflow relationship rows, and the continuous example trace. Bind it to exact source/model hashes and state which relations are source-declared or editorial. Review it manually with the model and blueprint; its existence is not automated schema acceptance.
