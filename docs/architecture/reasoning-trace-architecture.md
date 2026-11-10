<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Public reasoning trace architecture

The public reasoning trace is a workflow-neutral, expert-facing account of inspectable inferences. It connects workflow control, artifact provenance, evidence, scientific claims, scope, authority, and handoffs without storing private model deliberation.

## Data flow

```text
named workflow registry ───────────────┐
trace contracts and lenses ───────────┤
hook lifecycle events ────────────────┤
skill public-inference events ────────┼─> trace assembler ─> monitor packet ─> offline HTML
artifacts, digests, receipts ─────────┤          │                  │
legacy reasoning surfaces (adapter) ──┘          └─> validator ─────┴─> coverage report
```

The append-only store is the event authority. Latest-event files are compatibility views, not history. The assembler overlays observed events on the workflow’s declared route. It may expose a missing event as a gap but must never manufacture a scientific rationale.

## Semantic separation

Three independent states prevent misleading visual conclusions:

- Artifact validation reports schema, identity, digest, and receipt integrity.
- Claim epistemic status reports the scientific standing of a claim.
- Workflow disposition reports routing, quarantine, rejection, acceptance, or handoff.

A receipt may therefore be integrity-valid while its claim remains conjectural or refuted. An allowed hook decision means only that control policy permitted an action.

Control events describe activation, authorization, tools, completion, skips, failures, gates, and handoffs. Inference events describe a public question, typed premises, transformation, inspectable warrant, conclusion, evidence polarity, alternatives, falsifiers, uncertainty, scope, and authority. Both are needed; control coverage alone is not semantic coverage.

## Generic graph and lenses

The monitor packet uses workflow, profile, step, skill, artifact, claim, evidence, obligation, gate, and handoff nodes. Typed edges include `consumes`, `produces`, `supports`, `refutes`, `constrains`, `refines`, `validates`, `blocks`, `branches`, `hands_off`, and `precedes`.

Declarative lenses choose labels, mandatory trace spines, metrics, and emphasized views. They do not change event meaning. Route-A is a profile of manuscript elaboration: its specialist fan-out and join remain visible, followed by the parent workflow’s validation tail.

## Safety and compatibility

All repository artifacts use portable relative paths. HTML is self-contained, escapes untrusted values, and uses no network assets. Large tool outputs, prompts, credentials, or private chain-of-thought are excluded. Public warrants should be bounded and artifact-grounded.

The established main-workflow visualizers remain the default. Generic reports are additive and opt-in until compatibility, semantic validation, security, and expert-readability gates pass. See [Reasoning trace compatibility boundary](reasoning-trace-compatibility.md).

## Release invariants

1. Event IDs are stable, sequences are monotonic, and causal parents resolve within one run.
2. The causal graph is acyclic and handoffs resolve to typed terminal dispositions.
3. Scope widening and epistemic upgrades require evidence and suitable authority.
4. Conditional steps are executed, justified as not applicable, or reported missing.
5. Every substantive claim resolves to evidence, an explicit unknown, or an open obligation.
6. Coverage percentages remain traceable to individual workflow-step requirements.
