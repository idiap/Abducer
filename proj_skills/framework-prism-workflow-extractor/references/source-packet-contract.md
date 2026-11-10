<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# PrismWorkflowAppendixSource 1.0.0

This is a JSON-compatible exchange contract for the appendix skill lane. It is a documented contract, not a claim that an executable schema or automatic pipeline stage already exists. Use stable local IDs, arrays for repeated records, JSON `null` for unknown values, and explicit explanations for unknowns. Digests use `sha256:<64 lowercase hexadecimal characters>`.

## Packet envelope

| Field | Type and meaning |
| --- | --- |
| `schema_version` | String, `1.0.0` |
| `packet_id` | Unique string within the paper run |
| `input_digest` | Frozen `RepositoryEvidenceIndex.index_digest`, matching the paper pipeline's snapshot field; not the hash of the serialized index file |
| `source_digest` | Same `RepositoryEvidenceIndex.index_digest`; explicit join key for category modeling |
| `scope` | Object containing requested workflow IDs, source policy, included profiles, and exclusions |
| `evidence_refs` | Array of evidence records: `id`, indexed relative `path`, file `digest`, source span or structured pointer, `layer`, and evidence `kind` |
| `artifact_types` | Array of nominal type records, including wrappers and named record fields |
| `workflows` | Array of workflow records described below |
| `coverage` | Array of requested workflow ID, disposition, reason, and evidence IDs |
| `warnings` | Array of unresolved ambiguities, stale sources, and contradictory declarations |

Each type record has `id`, `name`, `kind` (`nominal`, `record`, `alternative`, `wrapper`, or `unknown`), `fields` (named typed bindings), `alternatives`, `type_arguments`, `evidence_ids`, and `unknowns`. Empty arrays mean no known entries; explain an incomplete declaration in `unknowns` rather than treating an empty list as proof of absence.

## Workflow records

Each workflow has `id`, `name`, `purpose`, `profile_ids`, `inputs`, `outputs`, `occurrences`, `relations`, `edges`, `control_annotations`, `order_constraints`, `projections`, `evidence_ids`, `non_claims`, and `unknowns`.

- Ports in `inputs` and `outputs`: `name`, `type_id` (or null), `wrapper` (or null), `evidence_ids`. Retain the literal source signature as well when its meaning is unresolved.
- Occurrences: `id`, `operation_name`, `operator_family` (or null), named `inputs` and `outputs`, `source_binding`, `layer`, `posture`, `evidence_ids`, and `unknowns`. Include explicit adapter/unwrapping records when the source expresses them; an unknown adapter is a gap, not a fabricated operation.
- Relations: `id`, `name`, typed endpoints, certificate/output type, `layer`, `posture`, and `evidence_ids`. A relation licensing an edge is distinct from an operation generating an artifact.
- Edges: `id`, `source_id`, `target_id`, `kind`, `guard` (or null), `profile_ids`, `layer`, `posture`, and `evidence_ids`. Reuse existing graph-model edge meanings for compatible graph edges; use a separate `control_annotations` record for language-specific semantics that do not fit that vocabulary.
- Control annotations: `id`, `kind` (`branch`, `switch`, `stop`, `failure`, `feedback`, `parallel`, `delegation`, or `unknown`), affected IDs, source condition or outcome, profile scope, `layer`, and evidence IDs. An unknown condition is null with a reason.
- Order constraints: `before_id`, `after_id`, `basis`, `profile_ids`, and `evidence_ids`. Record only supported constraints. Also record `ordering_status` as `explicit`, `partial`, or `unknown` per workflow/profile; source presentation order alone is not a total order.
- Projections: original/native/source-contract IDs, preserved features, omitted features, conflicts, and evidence IDs. Do not resolve contradictions by preferring the prettiest diagram.

`posture` distinguishes `declared`, `implemented`, `observed`, `contested`, and `unknown`; retain source-specific qualifiers in a separate field. For example, a curated simulated output can be declared documentation without becoming an observed execution. A structural smoke test cannot raise a scientific claim's authority.

## Repository-specific interpretation example

For `abducer_work_loop`, inspect native nominal types and occurrence signatures plus the original ERFL routing clauses. The calibration occurrence consumes both the derived claim and the refutation assessment via `ProofWorkRoutingInput`. A chain that discards the claim after refutation is an invalid projection. Preserve `Generated[ProofRouteDerivedClaim]` and the declared `.value` access explicitly.

The original ERFL's release, reframe, retarget, and refuted-stop outcomes belong in routing annotations with original-layer provenance even when native `reasoning.prism` only returns `work_routing`. This records the projection difference without claiming that the native specification executes those branches. Any `sample_outputs.prism` payload retains its documented simulated status.
