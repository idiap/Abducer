<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Appendix packet and integration guide

Read this when preparing the fragment and review handoff. The appendix uses the existing section packet contract; provenance and insertion instructions live in separate JSON-compatible sidecars so the section schema remains closed.

## Required artifacts

| Artifact | Required content |
| --- | --- |
| `workflow-appendix.tex` | A controlled section fragment, with blueprint-owned title/labels and no document wrapper, package imports, bibliography command, or `\appendix` switch |
| `workflow-appendix.section.json` | `PaperSectionDraft` schema `1.0.0`, `tex_fragment` set to the filename `workflow-appendix.tex`, allowed consumed claim IDs, approved notation/citation/figure/table IDs, warnings, unresolved TODOs, snapshot `input_digest`, and a computed `section_digest` |
| `workflow-appendix.provenance.json` | Envelope `schema_version`, `input_digest`, source packet ID and category model ID; `mappings` from paragraph/table-row/equation/diagram IDs to workflow, occurrence/object/path/control IDs, claim IDs, evidence IDs, source spans, and mathematical status |
| `workflow-appendix.integration.json` | Target manuscript identifier, frozen context digest, insertion/replacement anchor, section ID, required packages, labels and cross-references, bibliography dependencies, review/build status, remaining obligations, and intended assembler handoff |

Follow the existing section producer convention: `section_digest = canonical_digest([packet_without_section_digest])`, using `canonical_digest` from `framework-paper-blueprint-author/scripts/generate_paper_packets.py`. This is the canonical packet digest, not a hash of the TeX contents. The actual fragment lives in the separate `.tex` file. Add `artifact_hashes` to the integration sidecar for input and output file-byte SHA-256 hashes, especially the TeX file, so a prose edit cannot retain stale review authority merely because its filename is unchanged. Do not reuse stale hashes after revisions.

For scientific claim mappings, record the category model's equation/semantic status and any witness or obligation IDs, separately from source posture. A syntactically valid composition does not mean the workflow was executed; an observed execution does not prove a categorical equation. A category construction used only for exposition is labeled as such.

## Suggested narrative, adjusted to the paper

Introduce the evidence boundary and categorical vocabulary, then a coverage table grouped by reasoning role. Explain one simple chain and one multi-input or guarded example before compactly describing remaining workflows. Close with exact unresolved structure and interpretation limits rather than an efficacy claim. If space requires grouping, retain an individual mapping row for every workflow in scope.

A multi-input example must make retained context visible. If `f : A \to B` and `g : B \to C`, their path is `g\circ f : A\to C`. If the next operation consumes both `B` and `C`, the previous path alone is insufficient: use the category model's explicitly defined boundary bundle and source-backed context-preserving adapter. Do not silently replace the next domain by `C` or assert a categorical product just because the implementation uses a record.

An appropriate no-new-package diagram is a display of one validated arrow chain accompanied by a separate routing table. A square with two paths can depict a comparison obligation, but its caption must say that commutativity remains unproved unless a model witness licenses the equation.

Every workflow's subsection also includes its accepted worked example from the example
writer. Grouping can shorten repeated formal explanations but must preserve a concrete
case for each scoped workflow. Merge child content and provenance under one final section
owner; the parent hashes must change when an example changes.

## Review and build accounting

Record pass/fail/blocked for source coverage, all claimed endpoint matches, unresolved projection preservation, law-status fidelity, notation and label uniqueness, claim ownership, and section-schema validation. Compile only an isolated assembled draft with its declared packages when an engine is available; otherwise record compilation as not run and why. Never infer paper validity from successful compilation.

When integrating into the current standalone manuscript, the manuscript context packet must retain its existing canonical-flow coverage and identify the intended relationship to the new section. Requesting an insertion is distinct from promoting a new current PDF. The writer delivers reviewable text; the coordinating task performs only integration already authorized by the user.
