<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Public reasoning trace visual grammar

The generic trace report is an additive expert-inspection surface. It does not
replace the established main-workflow reports or the specialized Yang–Mills
monitor. Its source is the workflow-neutral monitor packet; workflow language
comes from `reasoning_trace_lenses.yaml`, not renderer branches.

## Reading order

The header identifies the run, workflow, profile, target, and selected lens.
The first viewport separates control coverage, semantic coverage, evidence
resolution, and visible trace gaps. These quantities must not be conflated.

The workflow route overlays observed control and inference events on declared
steps. A missing public rationale remains a visible amber gap. Conditional
steps are shown as executed, justified not-applicable, unexplained skip, or
missing. Route-A appears as a manuscript profile: specialist work fans out
after its declared fork, joins through a typed result packet, and then enters
the parent workflow's common validation tail.

The inference view uses a bounded public explanation:

`premises → operator + public warrant → conclusion`

It also exposes assumptions, uncertainty, scope, alternatives, falsifiers,
evidence polarity, authority, and open obligations. This is an artifact-grounded
rationale, never private model deliberation or hidden chain-of-thought.

## Status and edge semantics

Artifact integrity, claim epistemic status, and workflow disposition occupy
separate fields and visual rows. A valid digest therefore cannot appear as a
validated theorem. Claims without resolved evidence must point to an explicit
open obligation or be marked trace-incomplete.

Graph nodes are typed as workflow steps, events, claims, evidence, artifacts,
obligations, gates, and handoffs. Edges use the portable vocabulary `consumes`,
`produces`, `supports`, `refutes`, `constrains`, `background`, `precedes`,
`branches`, `joins`, and `refines`. Chronology is not presented as scientific
entailment.

## Accessibility and safety

The generated file has no remote scripts, styles, fonts, images, or network
requests. Tabs are native buttons with tab roles; search has an accessible
label; narrow layouts collapse to one column. Packet values are JSON-escaped
before embedding and HTML-escaped before insertion. The report is deterministic
apart from differences already present in its validated input packet.
