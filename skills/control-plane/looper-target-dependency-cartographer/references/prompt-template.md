<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dependency Cartography Prompt

## Intent Gate

Use this prompt only to interpret a validated target packet and dependency
graph for Looper-controlled Abducer navigation. The output should route work,
not assert proof progress without evidence.

## Self-Contained Context Packet

Restate the target ID, graph ID, KB path, evidence artifacts, frontier summary,
and workflow constraints you were given. If node evidence or artifact content is
missing, label it as unknown.

## Prompt-Diagnosis And Qualified Certainty Gate

Before the dependency interpretation, emit a short `Prompt/Inference Diagnosis`
block with context_status, inference_status, missing_context, smallest_repair,
and qualified_certainty. Separate graph incompleteness from real mathematical
obstruction.

You are interpreting an Abducer target dependency graph.

Given the target packet and dependency graph JSON, return:

1. A short target summary.
2. The strongest dependency clusters.
3. Open nodes grouped by mathematical role.
4. Which nodes are terminal, stale, blocked, or high-value.
5. The next workflow route and skill sequence.
6. Required evidence before release.

Ground every claim in dependency node IDs and artifact paths. Never treat graph
centrality or textual similarity as proof support unless an explicit proof,
premise, or route obligation connects the nodes.
