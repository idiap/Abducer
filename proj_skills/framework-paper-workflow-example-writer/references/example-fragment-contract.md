<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workflow example fragments and integration

This is a prose output contract for the manual authoring lane, not a newly implemented runtime schema or automatic manuscript insertion command. Its sidecars preserve the existing closed `PaperSectionDraft` boundary.

## Required artifacts

| Artifact | Content |
| --- | --- |
| `examples/<example-id>.tex` | One nested example body for an identified workflow. No document wrapper, section/subsection wrapper, package imports, bibliography command, or appendix switch. A blueprint-approved paragraph heading is optional. |
| `workflow-examples.fragments.json` | `WorkflowExampleFragments` envelope specified below; exactly one coverage row per in-scope workflow and one or more separately identified examples for every complete row. |
| `workflow-examples.provenance.json` | Source/model/plan IDs and digests; paragraph/equation mappings to workflow occurrences, example inputs and steps, claim IDs, evidence references, and source spans; separate evidential posture and formal status. Mark invented facts individually where mixed with observations. |
| `workflow-examples.integration.json` | Manuscript/context identity, blueprint identity, sole final section owner and section ID, per-workflow subsection anchors, review basis, packages/citations/notation requested, outstanding obligations, build status, and file-byte hashes. |

Use safe local filenames derived from reviewed identifiers; reject traversal or arbitrary source-supplied paths. A missing subsection anchor is an integration blocker: ask the main owner to allocate that workflow's subsection through the blueprint/context packet rather than silently dropping the fragment.

## WorkflowExampleFragments v1

The JSON-compatible envelope contains:

- `schema_version`: `1.0.0`; `packet_type`: `WorkflowExampleFragments`; `packet_id`.
- `input_digest`: exact `PaperBlueprint.input_digest`, inherited from `RepositoryEvidenceIndex.index_digest`.
- `source_packet_id`, `source_digest`, `plan_id`, and `model_bindings`: exact values from the consumed reviewed plan. The plan/source `source_digest` equals the evidence-index `input_digest`; neither is a serialized file hash. Bind the reviewed plan's actual bytes using the integration sidecar's `artifact_hashes`, not an invented upstream `plan_digest` field.
- `scope_workflow_ids`: the plan's ordered, unique workflow inventory; `final_section_owner` and `section_id`: assigned by the blueprint.
- `examples`: rows with `example_id`, `workflow_id`, `tex_fragment` (filename), `evidence_posture` (`illustrative`, `observed`, or `mixed`), `consumed_claim_ids`, `notation_ids`, `source_model_refs`, `review_status` (`pass`, `revise`, or `blocked`), and `remaining_obligations`.
- `coverage`: exactly one row per scope ID, containing `workflow_id`, `example_ids`, `subsection_anchor`, `status` (`complete`, `revise`, or `blocked`), and `reason`. Example IDs must resolve to rows for that same workflow; reject duplicates, missing IDs, and out-of-scope rows. Every example row must be referenced by its workflow's coverage row.
- `completion_status`: `complete` only when every workflow has at least one substantive reviewed example, all references and placement anchors resolve, and no coverage row needs revision or is blocked. Otherwise use `incomplete` and return the complete inventory with diagnostics.

Each scientific claim must already be licensed for the final section owner. A plan's scenario is not evidence licensing a new empirical claim. Even illustrative prose must stay within the approved descriptive/expository claim scope; send additional claim needs back to curation. `observed` requires execution evidence for the displayed sequence and outcome, not merely a source declaration or planned test.

The final owner merges these bodies into its existing section TeX and emits **one** section packet using the [PaperSectionDraft schema](../../../agentic/spec/framework_paper_section_draft.schema.json). It updates consumed claims, notation, citations, warnings, and unresolved TODOs rather than adding example fields to that closed schema. Use the existing producer convention `section_digest = canonical_digest([packet_without_section_digest])`; `tex_fragment` remains a filename. Example mappings stay in sidecars. Compute file-byte SHA-256 hashes of every consumed packet and produced fragment/section/provenance file in the integration sidecar; exclude the integration file itself. Rehash and re-review after text changes.

## Example of the required explanatory depth

The following is a **synthetic editorial illustration**, not a Prism run or a claim that any particular native workflow implements these steps. Use it only when the actual source and model license the corresponding mechanism, and adapt the problem to that workflow.

> Consider a greenhouse whose temperature sensor reports 31°C while a nearby independent thermometer reports 24°C. The task is to distinguish local heating of the sensor from excessive heating of the greenhouse. The discrepancy makes the whole-greenhouse explanation less convincing, but the measurements were taken in different places, so it does not eliminate that explanation. A useful next observation is to place both instruments together, shade them equally, and compare readings after they stabilize. If the discrepancy disappears only after shading, local radiant heating becomes more plausible; a persistent discrepancy leaves calibration error open. This case illustrates how comparing explanations can produce a discriminating observation without claiming a diagnosis from insufficient evidence.

Here the information changes a real inference; the outcome is a concrete measurement plan. If a dependent model explicitly defines `Assessment(h, d)` for hypothesis `h` and data `d`, an assessment of “local radiant heating” under the original readings cannot automatically become an assessment of “calibration error” or of the new co-located readings. Show those substitutions and their required premises only as declared by the model. The index is meaningful because it changes which reasoning can be reused; it is not merely a renamed record ID. `Assessment` need not be a proposition of correctness.

The corresponding weak version, “the candidate passes validation, receives a receipt, and proceeds,” fails: it supplies no competing content, evidential change, or useful conclusion. A scientific-looking vignette also fails if every workflow receives this same inference regardless of its defining operation.

## Completion checks

Record pass/fail/blocked for exact inventory coverage, source/model identity, claim ownership, concrete input sufficiency, visible transformation, realistic outcome, representativeness, evidence posture, formal fidelity, placement, and TeX escaping. Coverage is necessary but cannot compensate for an uninformative example. Review a plain-language reading with notation removed: the task and lesson should still make sense. Then inspect whether the notation adds a genuine dependency or composition constraint. Retain diagnostic rows for absent source support; incomplete source evidence never licenses invented successful execution.
