<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Main-text conceptual writing and integration

For conceptual-organization requests, follow [the shared conceptual inquiry contract](../../framework-core-mechanism-curator/references/conceptual-inquiry-contract.md) and require the re-curated CoreReasoningMechanismModel 2.0.0. This guide specifies editorial artifacts for a manual lane. It does not introduce an executable workflow, runtime schema, or automatic manuscript insertion command.

## Argument before inventory

Prepare `core-mechanisms.outline.md` before drafting, using the reviewed model's `argument_plan`, mechanism cards, and relationship records. State the central question and conceptual thesis in one sentence each; identify the proposed main-text insertion/replacement anchor and sole section owner; list selected mechanisms in explanatory order, with a reason for that order. Describe the role of the running example and composition passage. Identify which exhaustive workflow descriptions, dependent-type derivations, and taxonomy/type figures remain in the appendix, with known anchors or unresolved reference needs. Propose any introduction/contribution changes for their respective owners. Explain the substantive emphasis change, not only a section rename.

Freeze selected main-text mechanism IDs from the reviewed `argument_plan` and `coverage`; bind them to `scope_component_ids` through each card's `component_ids`. Preserve the complete component coverage map, including compressed or appendix dispositions, in provenance. The requirement for a main-text example applies to every selected main-text mechanism; it does not promote all inventoried workflow components to core primitives. Reject unexplained omissions or a purported central core relegated entirely to the appendix.

Organize the inquiry around the incumbent conceptual situation and tension, grounded diagnosis including the not_conceptual exit, alternatives, reflection, preserved successes and differences, plural comparison, and revisable consequences. Revisit earlier questions when the case demands it. This explanatory order neither dictates native execution nor implies that every difficult problem needs new concepts. Give the six conceptual-frontier-deepening source-profile lenses concrete work and record non-applicability where justified; preserve variation with the broader reflective source. Keep operator and formal vocabulary supporting this argument.

## A compact mechanism unit

Use these four moves as connected prose, not mandatory visible headings:

| Move | Reader should learn | Failure to reject |
| --- | --- | --- |
| Problem | Which uncertainty, contradiction, or representational difficulty is present | “This component improves reasoning” |
| Conceptual move | What information or hypothesis changes and on what grounds | Repeating a workflow label |
| Worked case | Concrete inputs, a visible inference, and a useful result | “Candidate passes review” |
| Contrast and limit | Why this move matters and what it cannot establish | Unsupported superiority or guaranteed truth |

The following is an **illustrative local move**, not a substitute for the conceptual inquiry running case: ordinary rival hypotheses may support a not_conceptual diagnosis when the incumbent concepts suffice. It is an **illustrative scenario**, not a framework run or a claim about a native workflow. Use it only if the reviewed core model licenses the corresponding mechanism:

> A greenhouse sensor reads 31°C while an independent thermometer reads 24°C. Abductive reasoning introduces explanations for the discrepancy: local sunlight on the sensor, a calibration offset, or genuinely different air temperatures at the two locations. The disagreement motivates alternatives but does not select one, because the instruments were measured in different places. The result is a small set of explanations with different predictions, rather than the unsupported conclusion that the greenhouse is overheating. Without this move, checking the first overheating explanation could overlook the sensor's environment. Generating alternatives alone still supplies no diagnosis.

For a distinct contrastive-testing mechanism, the case must add a new inference: co-locate both instruments and compare shaded and sunlit conditions; disappearance of the discrepancy under shading favors local radiant heating, while persistence leaves calibration error open. These are conditional predictions, not observed results. A composition passage can explain that alternatives supply the predictions used to choose this comparison. It may only attribute that chain to the framework if the source-backed model supports its operations and connections.

Do not reuse the paragraph as a generic example for every mechanism. For abstraction, show the specific common structure retained and the differences deliberately omitted. For revision, show the particular premise or explanation changed and why. For comparison, name the incompatible predictions or competing accounts. For composition, show a required dependency, not a list connected with arrows. These are writing prompts, not a mandatory core taxonomy.

## Outputs and closed-schema boundary

Both ownership modes emit:

- `core-mechanisms.outline.md` with the argument and placement proposal.
- Controlled TeX with no document wrapper, package imports, bibliography command, or appendix switch. Use only approved labels; escape source text as inert TeX.
- `core-mechanisms.provenance.json` recording `schema_version: 2.0.0`, `input_digest`, model identity and consumed bindings, and paragraph/equation/example mappings to selected mechanism IDs, conceptual roles, inquiry record IDs, optional many-to-many native annotations, model records, licensed claims, and evidence. Record illustrative/observed/mixed status locally and list each invented fact in mixed cases. Include one coverage row per selected mechanism with example and paragraph IDs and pass/revise/blocked status.
- `core-mechanisms.integration.json` with manuscript/context and blueprint identities, model binding, ownership mode, sole final owner, section ID, insertion/replacement anchor, appendix cross-references, package/notation/citation requests, review basis, remaining obligations, build status, and `artifact_hashes`.

In **sole-owner mode**, emit `core-mechanisms.tex` and `core-mechanisms.section.json` conforming to the existing [PaperSectionDraft schema](../../../agentic/spec/framework_paper_section_draft.schema.json). Set `section_owner` to `framework-paper-core-mechanism-writer`; `tex_fragment` is the filename `core-mechanisms.tex`, never inline TeX. Keep extra editorial fields in sidecars. Set `input_digest` to the exact `PaperBlueprint.input_digest` inherited from `RepositoryEvidenceIndex.index_digest`. Use `section_digest = canonical_digest([packet_without_section_digest])`, importing `canonical_digest` from `framework-paper-blueprint-author/scripts/generate_paper_packets.py`.

In **child mode**, emit safe local `core-mechanisms/<mechanism-id>.tex` bodies and a composition fragment without section/subsection wrappers, plus `core-mechanisms.fragments.json`. This manually versioned prose-contract envelope contains `schema_version: 2.0.0`, `packet_type: CoreMechanismFragments`, packet ID, `input_digest`, model binding, final owner, section ID, ordered selected mechanism IDs, and fragment rows. Each row records fragment ID, local filename, mechanism IDs, insertion anchor, claim/notation/citation IDs, evidential posture, review status, and remaining obligations. Add exact mechanism coverage rows referencing their example/fragment IDs. The final owner is `framework-paper-method-writer`; it merges the child material into its existing section and emits one `PaperSectionDraft`. No competing section packet is produced here.

Hash the actual bytes of all consumed packets and produced outline, TeX, section-or-fragment envelope, and provenance files using SHA-256 in the integration sidecar; exclude that sidecar itself. File hashes and source-snapshot/section digests have different meanings. Rehash and re-review after revisions. Require exact selected mechanism coverage and resolvable IDs; retain blocked rows instead of dropping difficult mechanisms. A composition fragment may reference multiple covered IDs but does not replace each mechanism's own worked explanation.

## Review criteria

Record pass/revise/blocked for main-text prominence, conceptual distinctness, diagnostic exit, substantive alternatives, source-profile lens fidelity, preserved differences, plural comparison, revision conditions, complete selected-core coverage, actual inference in each example, concrete input sufficiency, informative outcome, concise prose, meaningful contrast, supported composition, evidence posture, notation restraint, exact source/model binding, permitted claim ownership, unique placement/labels, TeX escaping, packet schema, and digest/hash consistency. Read the draft with symbols removed to test conceptual clarity. Check that a main-text reader learns the mechanisms without consulting the appendix.

If an engine is available, compile an isolated assembled probe and record the actual result; otherwise record the missing dependency. Compilation does not establish execution, formal soundness, or improved reasoning. Send the reviewed packet to the paper consistency/review lane and assembler; do not overwrite the manuscript or current PDF as part of skill drafting.
