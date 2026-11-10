<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning-trace PDF compatibility boundary

The expert PDF is an additive projection of the same validated workflow-neutral
monitor packet consumed by the HTML report. The packet—not the HTML DOM, page
layout, or renderer prose—is the sole semantic source. Its canonical JSON
SHA-256 is recorded in the print inventory, TeX provenance, and PDF manifest.

Existing HTML output paths, defaults, controls, visual grammar, and established
main-workflow visualizers remain unchanged. PDF generation neither imports nor
parses the HTML renderer. It is opt-in until its separate release gates pass.

## Expert-view parity

| HTML expert view | PDF disposition |
| --- | --- |
| Overview | Cover identity and lens; reading contract; validation dashboard; inference dossiers; specialized-projection appendix |
| Workflow Route | Declared route and topology body section |
| Inference Graph | Typed graph summary and complete node/edge appendix |
| Timeline | Complete chronological lifecycle appendix |
| Claims & Evidence | Complete claim and typed-evidence appendices, cross-linked from dossiers |
| Alternatives & Failures | Equal-visibility negative-path body section |
| Scope | Cross-cutting scope ledger and per-inference scope |
| Decisions & Gates | Complete decision/gate appendix |
| Obligations | Body ledger, complete appendix detail, and dossier links |
| Artifacts & Receipts | Complete appendix and dossier links |
| Authority | Body ledger and per-inference exercised/absent authority |
| Handoffs | Body ledger and per-inference handoff |
| Trace Coverage | Validation dashboard and explicit field-disposition appendix |

An empty lane is rendered as an explicit not-applicable record. A compact body
may summarize a lane only when its appendix is complete. Every packet field has
one of: `rendered`, `summarized_with_complete_appendix`, `not_applicable`, or
`omitted_with_reason`.

## Semantic invariants

- Artifact integrity, scientific epistemic status, and workflow disposition
  remain independent.
- Chronology does not imply support or entailment. Typed edges keep their
  declared meanings.
- Control authorization and handoff conclusions are not scientific claims.
- Negative, refuting, quarantined, minority, failed, and open paths remain
  visible alongside accepted paths.
- Workflow and Route-A terminology comes from declarative print lenses, not
  renderer branches.
- The report contains bounded public rationale, not private chain-of-thought.

The projection must not derive new claims, strengthen statuses, widen scope,
grant authority, or infer scientific meaning from visual placement. No
packet-derived value may enter a TeX preamble, command name, package directive,
path argument, or other executable context.

