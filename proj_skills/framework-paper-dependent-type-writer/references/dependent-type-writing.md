<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dependent typing exposition and section handoff

Read while drafting mathematical prose and preparing the section packet. The model owns the formal declarations; this guide explains how to communicate them without promoting assumptions into guarantees.

## Judgments that carry explanatory work

Use the model's universe convention and distinguish an ordered context `Gamma ctx`, type formation `Gamma |- A type`, and typing `Gamma |- t : A`. State whether any displayed rule is assumed, manually checked against the model, or verified by a named checker with a retained result. This lane supplies no checker by default.

An example proposed refinement has `C type`, `Vhat : C -> Type`, and `assess* : Pi(c:C). Generated[Vhat(c)]`. Then `c:C |- assess*(c):Generated[Vhat(c)]`. Read this aloud: the generated result is indexed by this exact candidate, while its generation boundary remains visible. To discuss a successful value `v:Vhat(c)`, state a separate proposed projection with its success/admissibility premises, such as `extract_c : Pi(y:Generated[Vhat(c)]). Success_c(y) -> Vhat(c)` and `v = extract_c(assess*(c),s)` for a supplied `s:Success_c(assess*(c))`. These declarations and their realization obligations must appear in the model; they do not assert that native wrappers provide this operation or predicate. Only then form `(c,v) : Sigma(c:C). Vhat(c)`. These are expository declarations unless source-backed implementations establish more; `Vhat(c)` need not be a correctness proposition.

Keep the native boundary alongside this example. If native assessment is `R:C -> Generated[V]`, neither its return type nor runtime evidence alone establishes `Pi(c:C). Generated[Vhat(c)]` or an operation extracting `Vhat(c)`. Specify the proposed family, linking relation, wrapper policy, and adapter obligations. A native `.value` accessor observed for one payload type does not establish an accessor for a proposed indexed payload: mark that new projection as proposed with an unresolved realization unless separately supported. An indexed proposal may preserve provenance without proving semantic validity.

Explain substitution, not just adjacent arrows. For `Gamma,x:A |- t:B(x)` and `Gamma |- a:A`, display `Gamma |- t[a/x]:B(a)` with capture-avoiding substitution. If the next operation needs `c:C` and `v:Vhat(c)`, retain both in context; `v` alone cannot silently supply `c`. For a different candidate `c'`, an assessment of `c` cannot be consumed as an assessment of `c'` without an explicit permitted conversion or an identity witness and transport. Hash equality is not automatically such a witness.

Represent a guard as a premise only if its proposition, witness, and operational interpretation are defined. Otherwise put routing conditions in a separate control annotation. A boolean pass flag cannot stand in for an arbitrary proof. A stochastic or fallible producer may require an explicit wrapper or effect model; do not erase that behavior to obtain a total function.

## Suggested narrative

Open with scope and the native/refined distinction; introduce only needed judgments; explain the simple derivation and the value-sensitive retained-context case; provide the workflow coverage table; close with specific unresolved formal and implementation obligations. A rejected index mismatch is often more informative than an elaborate diagram. The dependency structure must change what may compose, not merely the symbols used to draw a path.

Use established mathematical references supplied by the model/context packet for claims about the calculus; verify any new precise external attribution against a primary source. Repository citations establish repository behavior, not general type theory. Do not infer a Curry--Howard interpretation or categorical semantics unless the paper defines the relevant propositions, proof terms, and interpretation.

For every workflow subsection, incorporate an accepted example child fragment. Instantiate
the displayed claim/index with the scenario's actual values and explain what mismatched
input would invalidate the step. Do not replace the worked case with a notation legend
or coverage row. The parent writer owns the final section and merges child claims and
provenance before computing fresh hashes.

## Required artifacts

| Artifact | Contents |
| --- | --- |
| `dependent-type-section.tex` | Controlled fragment with blueprint-owned title and labels; no document wrapper, package import, bibliography command, or `\appendix` switch |
| `dependent-type-section.section.json` | Existing [PaperSectionDraft schema](../../../agentic/spec/framework_paper_section_draft.schema.json) `1.0.0`; owner `framework-paper-dependent-type-writer`; `tex_fragment` = `dependent-type-section.tex`; allowed claim, notation, citation, figure/table IDs; warnings and unresolved TODOs |
| `dependent-type-section.provenance.json` | `schema_version`, `input_digest`, source/model IDs and digests; mappings from paragraph, equation, and table-row IDs to workflows, model contexts/type families/judgments/derivations/adapters/control annotations/obligations, claims, evidence, and source spans; separate source posture and formal status |
| `dependent-type-section.integration.json` | Manuscript/context identity and digest, section ID, insertion anchor, supplement/replacement relation, review basis, labels and cross-references, packages, bibliography needs, build/review status, obligations, and assembler handoff |

Use the existing producer convention: `section_digest = canonical_digest([packet_without_section_digest])`, importing `canonical_digest` from `framework-paper-blueprint-author/scripts/generate_paper_packets.py`. This canonical packet digest is distinct from the TeX file-byte hash. Put `artifact_hashes` in the integration sidecar with file-byte SHA-256 hashes for all consumed source/model/context/blueprint/claim packets and produced TeX, section, and provenance files. Exclude the integration file itself to avoid self-reference; rehash all changed files after revisions. A filename unchanged by a prose revision does not preserve review authority.

Record pass/fail/blocked for section-schema validation, digest consistency, source/model identity, coverage, context and index fidelity, substitution and adapter premises, equality/transport obligations, native/refinement separation, claim ownership, notation and label uniqueness, and source escaping. Build an isolated assembled draft when an engine is available; otherwise say why compilation was not run. Neither a build nor a packet validator proves mathematical consistency or an implemented dependent-type discipline.
