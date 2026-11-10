<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Concepts

Understand the project model, terminology, and evidence boundaries. This section is for readers learning or using Abducer.

Abducer is a typed, replayable research system for constructing, comparing,
testing, and retaining abductive theories over difficult mathematical and scientific
problems. It preserves a problem's conceptual alternatives, evidence, failed attempts,
proof obligations, and research history rather than treating discovery as a single
answer or confidence score.

The repository has two related execution surfaces: a KB theorem-assistance workflow
and the canonical theory-first discovery runtime. The latter uses typed operator
requests and receipts, isolated branches, semantic events, and single-writer state
commits. [Getting started](../getting-started/README.md) explains which surface to use.

- **Persistent epistemic state:** retain hypotheses, literature, conceptual systems, transformations, failures, and learned results.
- **Plural conceptual exploration:** mature structurally different candidates and preserve dissent and partial failure.
- **Separate authorities:** conceptual preference, executable evidence, proof status, publication, and durable state mutation have different contracts.
- **Replayable transitions:** bind requests, receipts, outputs, and commits to exact target, run, generation, and digest identities.
- **Governed continuation:** use obligations, budgets, stopping rules, and reflection to determine what may happen next.

## Read next

- [Architecture thesis](../architecture/architecture.md) — Problem-centered persistent discovery and proof state.
- [Named workflows](../architecture/named-workflows.md) — Purpose, handoffs, and authority boundaries.
- [Essential reasoning types](../reference/essential-reasoning-types.md) — Compact epistemic vocabulary.
- [Epistemic output types](../reference/epistemic-output-types.md) — Claims, evidence, decisions, obligations, and representations.
- [Research methods](../research-methods/README.md) — Disciplines governing conceptual and proof work.

Return to the [documentation index](../README.md) or consult the
[documentation map](../reference/documentation-map.md) for the complete retained collections.
