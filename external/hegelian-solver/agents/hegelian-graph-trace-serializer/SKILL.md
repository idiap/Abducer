---
name: hegelian-graph-trace-serializer
description: Serialize Hegelian concept graph nodes, transformation edges, failure and discovery triggers, validation certificates, residual limits, rejected candidates, and solver-readable traces. Use when a solver run needs durable JSON/YAML artifacts or graph updates for later reasoning, testing, or explanation.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Graph Trace Serializer

## Overview

Emit durable concept-graph artifacts that preserve the full path from trigger to candidate to obligations to ranking decision.

## Node Shape

```yaml
node:
  id: string
  name: string
  domain: string
  schema_version: string
  concept: {}
  status: draft | active | provisional | validated | effective | rejected
  created_from: []
  validation_status: {}
```

## Edge Shape

```yaml
edge:
  id: string
  source: string
  target: string
  relation: extends | embeds | abstracts | completes | quotients | localizes | weakens | stratifies | limits_to | effective_of | coarse_grains_to | quantizes | geometrizes | gauge_quotients | unifies | dual_to | agentifies | toolifies | retrieves | governs
  trigger:
    type: FailureCertificate | DiscoverySignal
    id: string
    label: string
  operator: string
  map: {}
  regime: optional
  obligations: []
  certificates: []
  residual_limits: []
  ranking: {}
  status: proposed | validated | effective | provisional | rejected
```

## Trace Shape

For each run, emit:

```yaml
solver_trace:
  run_id: string
  seed_nodes: []
  tasks: []
  evidence: []
  failures: []
  discovery_signals: []
  candidates: []
  validation_packets: []
  ranking_decision: {}
  graph_updates:
    added_nodes: []
    added_edges: []
    rejected_candidates: []
  explanation_ref: optional
```

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Serialization Rules

- Keep IDs stable and deterministic where possible.
- Store both accepted and rejected candidates; rejected candidates teach the solver boundaries.
- Include exact trigger IDs on every edge.
- Include residual limits even for successful transformations.
- For conceptual crises, store the tension formalization as a graph seed with explicit commitments, failed mediations, crisis type, and validation obligations before adding repair edges.
- For abductive mechanisms, store hypotheses, requirements, counterfactual critiques, and TODO packets as provisional mechanism nodes or annotations, not as accepted repair edges.
- For retrospective evolution, store stage edges as provisional historical reconstruction unless validation has checked chronology, source support, preservation, and transition mechanism.
- For physics edges, include valid and invalid regimes plus limiting maps.
- For language-model edges, include evidence-trace references, risk gates, and monitoring obligations.
- Preserve provenance to source refs or external evidence when available.

Prefer YAML for human-authored fixtures and JSON for machine API outputs.
