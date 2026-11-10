---
name: hegelian-discovery-signal-miner
description: Detect concept discovery signals from examples, proof traces, anomalies, invariants, analogies, repeated constructions, shared interfaces, transfer pressure, and trace clusters. Use when the solver should invent or abstract new concepts, not only repair an explicit failure.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Discovery Signal Miner

## Overview

Find constructive abstraction pressure: patterns that justify a new concept even when no single failure forces it.

## Signal Shape

```yaml
discovery_signal:
  id: string
  label: string
  evidence: []
  latent_structure: {}
  candidate_move: string
  candidate_concept: optional
  expected_obligations: []
  score:
    coverage: float
    compression: float
    transfer: float
    predictive_power: float
    canonicality: float
    complexity_penalty: float
    overfit_penalty: float
  assumptions: []
  unknowns: []
```

## Generic Signals

Look for:

- `SharedInterface`: many examples support the same operations and laws.
- `InvariantPattern`: a property survives transformations.
- `ProofCompression`: multiple proofs share a skeleton.
- `RepresentationRedundancy`: presentations encode the same object.
- `EquivalencePressure`: classification ignores irrelevant differences.
- `UniversalPattern`: constructions share a mapping property.
- `FunctorialBehavior`: object-level construction also respects maps.
- `DualityPattern`: reversed arrows or operations yield parallel theorems.
- `ParameterGeneralization`: theorem holds across a family.
- `AnomalyCluster`: several failures share a repair target.

## Domain Signals

For physics, also detect `SymmetryPattern`, `UnificationPressure`, `LatentCarrier`, `FieldPattern`, `GeometricPattern`, `QuantizationPressure`, `OrderParameterPattern`, `ScaleUniversality`, `DualDescription`, `EffectiveDegreePattern`, `VariationalCompression`, and `GaugeRedundancy`.

For language-model systems, also detect recurrent pressures such as external evidence, tool APIs, context-window memory, preference/interface mismatch, reasoning-time compute, governed deployment, and agentic state.

## Guardrails

- Do not invent a concept from a single weak analogy unless the user explicitly asks for speculative ideation.
- For latent ontology, require constrained properties, multiple linked failures or signals, and testable consequences.
- Penalize patterns that only rename existing concepts without improving transfer, compression, or prediction.
- Separate discovery evidence from proposed explanation.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output

Return discovery signals with evidence references, candidate moves, expected obligations, and a confidence/risk note.
