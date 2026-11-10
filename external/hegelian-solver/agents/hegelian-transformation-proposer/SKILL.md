---
name: hegelian-transformation-proposer
description: Propose constructive successor concepts from typed failures or discovery signals using Hegelian transformation operators such as completion, adjunction, quotient, invariantization, abstraction, stratification, regime restriction, quantization, retrieval, toolification, agentification, and governance. Use after failure classification or discovery mining and before obligation verification.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Transformation Proposer

## Overview

Generate candidate successors without declaring them valid. Each proposal must include a preservation map, a resolution mechanism, changed structure, expected obligations, and residual limits.

## Candidate Shape

```yaml
transformation_candidate:
  id: string
  operator: string
  source_concepts: []
  target_concept: {}
  triggered_by: []
  preservation_map: {}
  resolution_mechanism: string
  changed_structure: []
  expected_obligations: []
  residual_limits: []
  rejected_alternatives: []
  assumptions: []
  unknowns: []
```

## Operator Selection

Use core mathematical operators:

- `GroupCompletion` for closure under additive inverse.
- `FieldOfFractions` or `Localization` for division/inversion pressure.
- `Completion` for missing limits or Cauchy convergence.
- `AlgebraicAdjunction` for equations lacking solutions.
- `Invariantize` or `Quotient` for representation dependence.
- `WeakenEquivalence` for rigidity.
- `AbstractInterface` for shared structure across examples.
- `WeakenAxioms` for overstrong assumptions.
- `TypeStratify` for self-reference or inconsistency.
- `Categorify` or `Functorialize` for compositional structure.

Use physics operators when the trigger is regime, empirical, or ontology related:

`RestrictRegime`, `InvariantizeKinematics`, `GeometrizeInteraction`, `FieldifyActionAtDistance`, `QuantizeObservableAlgebra`, `IntroduceLatentCarrier`, `GaugeQuotient`, `LocalizeSymmetry`, `CoarseGrain`, `Renormalize`, `IntroduceOrderParameter`.

Use language-model operators when the trigger concerns model/system behavior:

`InstructionTune`, `PreferenceOptimize`, `Retrieve`, `Verify`, `Toolify`, `Agentify`, `Multimodalize`, `ReasonAtInference`, `Sparsify`, `Distill`, `Govern`, `SecureRAG`, `TaintTracking`, `CalibrateSafetyPolicy`, `AddState`.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Proposal Rules

- Generate at least one conservative repair and one more expressive repair when both are plausible.
- Preserve the predecessor by embedding, interpretation, quotient, forgetful map, limiting map, regression suite, or effective-theory relation.
- Name what the successor gives up: lost order, forgotten metric, weaker equality, higher cost, added risk, narrower regime, or unproved mechanism.
- For physics, declare measurement interface and regime from the start.
- For language-model systems, declare new safety, tool, governance, and monitoring surfaces from the start.

Do not rank or accept candidates in this skill; hand proposals to `hegelian-obligation-verifier`.
