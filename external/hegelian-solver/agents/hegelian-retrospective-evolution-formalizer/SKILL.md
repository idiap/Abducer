---
name: hegelian-retrospective-evolution-formalizer
description: "Formalize a past evolutionary process described in prose into Hegelian solver artifacts: stages, predecessor and successor concept nodes, determinate failures, discovery pressures, transition hypotheses, preservation maps, evidence refs, and graph seeds. Use when the user provides historical narrative text about how a concept, theory, technology, scientific model, language-model system, or institution evolved and wants it represented formally and materially."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Retrospective Evolution Formalizer

## Overview

Convert historical prose into a structured reconstruction of concept evolution. The goal is not to retell history, but to make the development reason-able: stages, tensions, transformations, evidence, assumptions, and residual uncertainty.

## Workflow

1. Run after `hegelian-input-typology` identifies `retrospective_evolution_text`.
2. If the input lacks dates, source refs, named-event support, or primary evidence, call `hegelian-web-expansion-scout` before finalizing.
3. Segment the narrative into stages:
   - predecessor concept or practice;
   - stress, anomaly, failure, discovery pressure, or external demand;
   - transformation or abstraction;
   - successor concept;
   - what was preserved, lost, or relocated.
4. Build a concept node for each stable stage using the normal domain fields where possible.
5. Build transition records that can become failure certificates, discovery signals, or candidate graph edges.
6. Attach material evidence to every stage and transition. If evidence is only narrative testimony, mark it as such.
7. Produce a graph seed suitable for downstream domain adaptation, formalization, validation, and explanation.

## Stage Extraction

For each stage, capture:

- `stage_id`, `name`, `time_span`, `domain`, `role`;
- formal structure: signature, axioms, model assumptions, architecture, state variables, interface, or governance layer;
- material setting: actors, instruments, datasets, institutions, practices, experiments, use cases, benchmarks, or deployment context;
- epistemic profile: knowns, assumptions, contested claims, unknowns, uncertainty, and possible falsifiers.

## Transition Extraction

Classify each transition as one or more of:

- `failure_driven`: a determinate limit, contradiction, anomaly, counterexample, benchmark failure, or deployment incident.
- `discovery_driven`: invariant pattern, shared interface, proof compression, analogy, latent carrier, scaling law, or repeated practice.
- `external_pressure`: institutional, experimental, computational, economic, safety, or governance demand.
- `integration`: previously separate lines become one conceptual system.
- `differentiation`: one concept splits into specialized branches.
- `regime_restriction`: a former universal claim becomes an effective theory or bounded practice.

## Output

Return:

```yaml
retrospective_evolution_packet:
  source_text_summary: string
  input_intake_ref: optional
  web_expansion_ref: optional
  stages:
    - stage_id: string
      name: string
      time_span: string | null
      concept_node: {}
      material_context: {}
      epistemic_profile: {}
      evidence_refs: []
  transitions:
    - transition_id: string
      source_stage: string
      target_stage: string
      transition_kind: []
      trigger:
        failure_certificate: optional
        discovery_signal: optional
        external_pressure: optional
      preservation_map: {}
      formal_analysis: {}
      material_analysis: {}
      epistemic_profile: {}
      evidence_refs: []
      residual_limits: []
  graph_seed:
    nodes: []
    edges: []
  assumptions: []
  unknowns: []
```

## Integration Rules

- Feed each `concept_node` into `hegelian-domain-adapter` and `hegelian-concept-formalizer`.
- Feed transition triggers into `hegelian-failure-classifier` and `hegelian-discovery-signal-miner`.
- Feed preservation maps and residual limits into `hegelian-obligation-verifier`.
- Feed graph seeds into `hegelian-graph-trace-serializer`.

## Epistemic Discipline

- Keep chronology, causality, and conceptual necessity separate.
- Treat "A led to B" as a hypothesis unless sources establish mechanism.
- Preserve branches and dead ends instead of forcing a single linear story.
- Mark anachronism risk when later concepts are projected onto earlier actors.
- Distinguish formal reconstructive adequacy from historical-material adequacy.
