---
name: to-prism-document-workflows
description: Produce source-grounded documentation for named Prism workflows and their stages. Use after workflow modeling and before generation when workflow comments must explain purpose and composition without changing behavior.
---
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Document Prism workflows

Turn reviewed workflow evidence into concise descriptions in the approved
generation plan. The deterministic generator places them immediately above
the corresponding Prism reasoning or workflow declaration and materialized
agent. Do not edit generated `.prism` files directly.

## Recover documentation from evidence

Start from the validated project semantic taxonomy, approved generation plan,
workflow graph, and their source evidence. Follow [the semantic typing
protocol](../../references/semantic-typing-protocol.md): documentation consumes
the decisions established by `$to-prism-derive-types`; it cannot replace that
review or turn an unresolved type into an approved one.
Prefer, in order:

1. declared workflow or loop descriptions;
2. entrypoint and router documentation;
3. hook triggers, phases, and contract descriptions; and
4. tests or examples that establish externally visible intent.

Document what the workflow is for and what each stage contributes. Keep
uncertainty explicit. Do not infer guarantees, effects, execution order, or
preservation claims beyond the reviewed graph and contracts. Exclude secrets,
fixture payloads, credentials, and incidental source implementation details.

## Populate the reviewed generation plan

Set `workflows[].description` to a short purpose statement. Set each reviewed
`workflows[].steps[].description`, `reasoning_rationale`, and
`granularity_rationale` only from evidence that supports those distinct
claims. Use each composed skill's `role` and `contribution` to explain its part
in the occurrence without treating a skill boundary as an occurrence boundary.
Preserve the workflow and step identifiers, exact input/output types, semantic
roles, and order selected during modeling; documentation must not create,
remove, reorder, split, merge, or retype occurrences.

The deterministic generator owns formatting and comment escaping. It emits
the reviewed high-level description above the core `reasoning` declaration,
occurrence rationales above topology nodes and abstract signatures, and step
descriptions above materialized agents. For a projected occurrence, it also
emits a concise source-grounded comment naming the reviewed material-step and
skill composition immediately above the exact typed implementation.
`reasoning.prism` remains limited to
imports, comments, and the core reasoning block; supporting declarations live
in `occurrences.prism` and `relations.prism`. Treat comments as explanatory
metadata, never executable instructions.

## Validate the result

Run generation, then check and compile every generated workflow entrypoint.
Confirm that each named workflow has an adjacent source-grounded description,
stage order and exact nominal chains match the reviewed plan, generative
occurrences still return `Generated[T]`, and undocumented facts were not
invented. Because the generation-plan schema requires substantive
descriptions, insufficient evidence blocks plan approval; it does not justify
a generic or fabricated purpose statement.
