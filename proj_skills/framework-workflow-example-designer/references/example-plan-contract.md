<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# WorkflowExamplePlan 1.0.0

This JSON-compatible authoring contract connects example design to appendix writing. It is not a registered schema, runtime trace, or validation program. Use stable IDs and explicit unknowns with reasons.

## Envelope and coverage

| Field | Meaning |
| --- | --- |
| `schema_version` | Literal `1.0.0` |
| `plan_id` | Stable plan identifier |
| `source_packet_id` | Exact extractor packet ID |
| `source_digest` | Exact extractor `source_digest` (= `input_digest` = evidence index `index_digest`), not the serialized file hash |
| `model_bindings` | Zero or more records with `style` (`category` or `dependent_type`), `model_id`, `source_packet_id`, and `source_digest`; selected styles require their corresponding models |
| `paper_context` | Audience, scientific domain, intended appendix location, selected presentation style and relevant claim-ledger references |
| `scope_workflow_ids` | Ordered, unique workflow IDs from the requested appendix scope |
| `coverage` | Exactly one row for each scoped workflow, with no omitted or extra workflow IDs |
| `examples` | Worked case records below |
| `unresolved` | Source gaps, modeling obligations or factual uncertainties preventing readiness |

A coverage row has `workflow_id`, `profile_ids`, `source_layer`, `example_ids`, `status` (`ready`, `draft`, or `blocked`), and `reason`. A ready row resolves to at least one ready example for that workflow. Shared settings may be reused, but each workflow needs its own trace and representativeness account. Declared coverage remains incomplete while any row is draft or blocked. Scope changes require explicit reconciliation with the paper plan and frozen source packet; dropping a difficult workflow is not a repair.

## Worked case

Each example contains:

- `example_id`, `workflow_id`, `status`, `title`, and `evidence_posture` (`illustrative`, `observed`, or `mixed`). An illustrative case says so in the reader-facing text, including any invented observations or outcomes. Mixed cases identify the posture of each factual step; observed cases need execution evidence rather than only declarations or simulated sample outputs.
- `problem`: concrete question, why its answer matters, and domain assumptions.
- `inputs`: named source ports and readable case values/content, with units and domain constraints when relevant. Inputs may be a focused excerpt rather than an entire large native payload; record omitted fields and make no claim of executability when incomplete.
- `steps`: ordered or partially ordered records with `step_id`, `source_occurrence_ids`, `input_bindings`, `transformation`, `output_bindings`, `content`, `posture`, and `evidence_refs`. Preserve source-supported ordering and explain the actual information gained. Structural adapters may have model adapter IDs instead of occurrence IDs; never fabricate occurrences for explanatory prose.
- `defining_mechanism`: the workflow-specific reasoning feature, its source/model references, and the steps demonstrating it.
- `contrast`: a consequential alternative, rejected shortcut, branch or index mismatch; give its inputs, why it differs, and `kind` (`source_branch`, `reasoning_contrast`, or `index_mismatch`). Cite branch evidence for `source_branch`; other contrasts are explanatory and do not add runtime edges.
- `outcome`: substantive result or changed next scientific action, tied to the question and final source output. A routing enum can accompany the explanation but cannot replace it.
- `limitations`: unresolved claims, untraversed consequential alternatives, domain bounds and source/model gaps. Do not require every branch to be acted out.
- `representativeness`: why this case exercises the workflow's defining mechanism, whether a different workflow would behave differently, and what the case leaves out. A representative example is not evidence of statistical typicality or comparative effectiveness.
- `representation_bindings`: mappings described below, or an explicit reason no formal style was requested.
- `evidence_refs`: source packet evidence IDs for workflow facts, plus precisely identified observation artifacts when present. Invented scenario content is labeled illustrative instead of assigned false repository provenance.

For category presentation, each binding gives `step_id`, `model_id`, `object_ids`, `arrow_or_path_ids`, `adapter_ids`, and retained named inputs. Preserve all modeled effect wrappers and contextual packing. A checked path illustrates endpoint compatibility, not execution or empirical correctness. Exact parallel paths and an equality witness are necessary for any proposed commutation claim.

For dependent-type presentation, give `step_id`, `model_id`, `context_id`, `judgment_ids`, `substitutions`, `instantiated_indices`, and `origin` (`native`, `source_descriptive`, or `proposed_refinement`). Index identities refer to exact claim bindings, not just displayed claim text. Link every assessment's subject and subsequent routing input to the same binding. Proposed indexed families remain proposed even when illustrated with concrete values. Any equality/transport step cites the model obligation and its justification; do not manufacture proof terms from assessment data.

## Choosing a case that teaches something

For an abductive route, an illustrative problem might ask why a graph-search heuristic increasingly chooses high-degree vertices rather than vertices close to a target. Concrete input could state a small graph and the scoring rule. The hypothesis identifies degree bias; deduction predicts which vertex should win under that rule; a counterexample distinguishes the claim “always biased” from a conditional claim about degree and distance. The result is a narrower hypothesis and a discriminating next test, not “the assessment was logged.” Use this only if the frozen workflow supports those transformations; the vignette supplies no evidence about native behavior.

For an index-sensitive example, call the original claim `c₁` and its revised claim `c₂`. Show their actual differing assumptions or conclusions. An assessment addressing the original is useful history but is not a fresh assessment of the revision. A proposed `Assessment(c₁)` family can make this dependency legible without implying that the native nominal contract enforces it.

Before handoff, verify the scope/coverage bijection, source/model digest agreement, source occurrence references, exact inputs and indices, and posture labels. Then assess content: meaningful intermediate changes, realistic assumptions, a decisive workflow-specific mechanism, a useful result, and explicit limits. Revise weak content even when every field is populated. Record manual review as manual; contract conformance alone establishes neither quality nor execution.
