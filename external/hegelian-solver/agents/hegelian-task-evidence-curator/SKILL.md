---
name: hegelian-task-evidence-curator
description: Build task, example, counterexample, trace, benchmark, proof, measurement, and evidence packets for Hegelian concept evaluation. Use when a concept node needs explicit intended tasks and evidence sources before failures or discovery signals can be mined.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Task Evidence Curator

## Overview

Curate the demands placed on a concept and the evidence used to evaluate those demands. Keep task requirements, empirical evidence, formal proofs, model claims, and human judgments separate.

## Task Schema

Use:

```yaml
task:
  id: string
  name: string
  kind: prove | construct | compute | decide | classify | transfer | complete | abstract | predict | fit | explain | simulate | check_invariance | check_conservation | stability | discover
  context: {}
  goal: string
  required_status: string
  priority: low | medium | high | critical
  regime: optional
  tolerance: optional
  evidence_refs: []
  expected_output: optional
```

## Evidence Schema

Use:

```yaml
evidence:
  id: string
  type: example | counterexample | theorem | proof_trace | model_finder_result | benchmark_score | measurement | simulation | retrieved_document | tool_result | human_preference | policy_decision | deployment_incident | hypothesis
  source: string
  claim_supported: string
  reliability: low | medium | high | formal | unknown
  regime: optional
  uncertainty: optional
  provenance: optional
  notes: []
```

## Procedure

1. Derive tasks from the concept's intended role and protected meanings.
2. Add stress tasks that probe known limits: closure, solvability, completeness, invariance, rigidity, consistency, representability, transfer, compositionality, and residual limits.
3. Add discovery tasks that search for shared interfaces, invariant patterns, proof compression, universal properties, functoriality, duality, parameter generalization, and anomaly clusters.
4. For physics, attach regime, tolerance, measurement model, uncertainty, and limiting-case tasks to every relevant prediction.
5. For language-model systems, attach traces, retrieval/tool logs, red-team cases, provenance expectations, risk checks, and latency/cost evidence.
6. For retrospective evolution packets, attach source text fragments, web evidence, dates, actors, and transition claims as separate evidence records.
7. Mark gaps explicitly; do not invent experimental data, proof certificates, benchmark results, source citations, or dates.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output

Return a `task_evidence_packet` with `tasks`, `evidence`, `examples`, `counterexamples`, `trace_refs`, `missing_evidence`, and `evaluation_notes`.
