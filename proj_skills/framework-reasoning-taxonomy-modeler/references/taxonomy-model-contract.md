<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# ReasoningTaxonomyModel 1.0.0

This JSON-compatible authoring contract is the shared boundary between the taxonomy modeler and appendix plotter. It describes a provenance-bound classification with artifact interfaces, not an executable type system. Required fields below must be present; use explicit empty arrays for known absence and `null` with an `unknowns` explanation for unavailable facts. A plot renderer may validate structural fields without establishing the truth of their evidence.

## Envelope and provenance

| Field | Meaning |
| --- | --- |
| `schema_version` | `"1.0.0"` |
| `packet_id` | Unique model ID within the paper run |
| `input_digest` | Frozen `RepositoryEvidenceIndex.index_digest`, a `sha256:` digest; not the hash of the serialized index file |
| `source_packet_id` | Exact upstream `PrismWorkflowAppendixSource.packet_id` |
| `scope` | `requested_workflow_ids`, `profile_ids`, and `source_policy`; the IDs are the complete selection, not just successfully modeled workflows |
| `evidence_refs` | Records with `id`, indexed relative `path`, file `digest`, `span` or structured `pointer`, `layer`, and `kind` |
| `layers`, `families`, `artifact_types`, `operations`, `workflows` | Entity arrays defined below |
| `relations` | Additional classification/type relations; never sequence edges |
| `workflow_edges` | Source-backed workflow edges kept separate from taxonomy membership |
| `coverage` | Exactly one row per requested workflow: `workflow_id`, `disposition` (`modeled`, `partial`, `excluded`, `blocked`), `reason`, `evidence_ids` |
| `unknowns`, `non_claims` | Explicit unresolved facts and limitations |

All entity and relation IDs are globally unique opaque strings. Display labels never serve as joins. Each entity has `id`, `label`, `evidence_ids`, `claim_status`, `source_posture`, and `unknowns`. `claim_status` is `declared`, `inferred`, `proposed`, or `unknown`: it describes the modeled claim's relation to evidence. `source_posture` is `declared`, `implemented`, `observed`, `contested`, or `unknown`: it preserves the source evidence's status. These axes cannot substitute for each other. An inferred classification needs an explanation and supporting evidence IDs; a proposed one needs an explicit proposal rationale. Neither becomes native merely by appearing in a plot.

Evidence IDs resolve in `evidence_refs`; their files must belong to the frozen index. Native source signatures and manuscript classifications retain different evidence records. Optional `category_model_id`, `dependent_type_model_id`, and `presentation_overlays` identify aligned mathematical views; they cannot replace native fields or silently strengthen the evidence.

## Entities and ports

- **Layer:** common entity fields. A functional layer is conceptual grouping, not a primitive, execution stage, or subtype.
- **Family:** common fields plus `layer_ids` (possibly multiple), `symbol` (string or null), and `description`. Each `layer_ids` assignment is justified by the family's evidence; where assignments have distinct status/provenance, record these in `membership_details` with `target_id`, `evidence_ids`, and `claim_status`.
- **Artifact type:** common fields plus `source_name`, `kind` (`nominal`, `record`, `alternative`, `wrapper`, `unknown`), `type_arguments` (type IDs), `fields` (named ports), and `alternatives` (type IDs). Preserve distinct nominal IDs even when labels or field shapes coincide. A wrapper has its own ID; its argument is not its supertype. Cyclic/recursive declarations are permitted where source-backed and should be cross-referenced, not infinitely expanded.
- **Operation:** common fields plus `source_name`, `family_ids`, `workflow_ids`, `profile_ids`, `inputs`, and `outputs`. Use one ID per occurrence; keep exact source occurrence ID in `source_occurrence_id`. All selected occurrences appear even if `family_ids` is empty. `membership_details` resolves per-assignment posture/provenance as for families. A repeated source operation in two contexts must retain occurrence identity and profile-specific signatures.
- **Workflow:** common fields plus `operation_ids`, `profile_ids`, `inputs`, `outputs`, and `ordering_status` (`explicit`, `partial`, `unknown`). `operation_ids` is membership, not a schedule. Multiple signature profiles use distinct occurrence records or explicit `profile_interfaces`; never merge incompatible ports into an apparently unconditional input bundle.

Every port contains `name`, `type_id` (ID or null), `source_type_expression` (exact string, or the display sentinel `unknown` when no expression is available), `wrapper` (exact wrapper string or null), and `evidence_ids`. Add `unknown_reason` whenever `type_id` is null; use `unknowns` to record further unavailable facts. The sentinel is not a native type declaration. If a port's exact expression is `Generated[Claim]`, its `type_id` identifies the wrapper type; the `Claim` argument remains a different artifact type. A named record input remains one port with separately documented fields. Multiple named ports remain separate required bindings; flattening them into one unnamed type loses their contract. Workflow boundary ports and internal occurrence ports are different tables and may legitimately differ.

## Relations without accidental semantics

Membership is encoded by `families.layer_ids` and `operations.family_ids`, and workflow membership by `operations.workflow_ids`/`workflows.operation_ids`. Do not duplicate membership in `relations`; reconcile both sides of workflow membership. Each additional relation has `id`, `source_id`, `target_id`, `kind`, `label`, `evidence_ids`, `claim_status`, `source_posture`, and `unknowns`.

- `conceptual_grouping` connects compatible conceptual entities and says only that they are grouped; no inferred is-a or causal meaning.
- `declared_subtype` connects artifact types, from subtype to supertype, only when the source explicitly declares this relation. Include the exact declaration and scope. Inferred compatibility, field inclusion, wrappers, and DTT refinements are insufficient.

Actual dependency, routing, and control edges go in `workflow_edges` with the upstream edge kind, endpoints, workflow/profile IDs, guard, source layer, posture, and evidence IDs. The plotter must not render them using taxonomy membership styles. Source presentation order, left-to-right layout, and the paper's numbered layers never establish an execution order.

## Representative interpretation

[The native rendering probe](native-taxonomy-example.json) records these four occurrence signatures and all eight manuscript families with file digests. It intentionally leaves production index/source-packet binding null, lists extraction omissions, and is not a valid production handoff packet. Use it to check figure content and layout; a real authoring run must perform the extractor/index binding before publication.

Consider the native `abducer_work_loop`: abduction generates `Generated[ProofRouteHypothesis]`, while deduction consumes the unwrapped hypothesis and generates `Generated[ProofRouteDerivedClaim]`. Source-declared `.value` adapters expose the underlying values. Refutation evaluates a retained claim, and calibration consumes the claim together with its assessment through `ProofWorkRoutingInput`. Copy the current source's exact occurrence names and signatures before modeling this example; this paragraph is an interpretation guide, not a replacement evidence packet.

The taxonomy connects the abductive occurrence to Abduction and the calibration occurrence to Evidential calibration. It does not connect Abduction to calibration as a subtype or sequence arrow. The interface plot shows the generation wrapper, explicit adapter, and the named record input with its claim and assessment fields. An optional DTT overlay can propose an assessment indexed by the claim, labeled `proposed`; it cannot rewrite the native record declaration or claim a proof. Unknown family membership stays visible as unclassified. If source declarations differ by profile, show separate panels rather than one fabricated common signature.

## Delivery checks and figure handoff

Require complete ID/reference resolution, digest binding, all requested coverage rows, agreement of bidirectional workflow membership, and evidence-backed signatures. Every selected occurrence is either modeled or explicitly unresolved; every excluded/blocked workflow retains its coverage row. Nonempty `inputs`/`outputs` are not mandatory for genuine nullary/terminal operations, but unknown interfaces need explicit explanations. Do not interpret an empty list caused by failed extraction as a known nullary signature.

Send the packet and a report of manual versus executed checks to the plotter. Request a taxonomy view and per-workflow input/output view with a legend distinguishing membership, declared subtyping, wrappers, unknowns, and optional mathematical overlays. A representative preview may show a subset only when its caption and coverage account for the remaining selected scope. Figures cannot claim complete native behavior, global taxonomy exhaustiveness, runtime validity, or a machine-checked dependent type theory from this packet alone.
