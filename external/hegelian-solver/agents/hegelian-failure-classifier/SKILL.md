---
name: hegelian-failure-classifier
description: Classify evaluation failures into typed determinate negation certificates with witnesses, failed obligations, dependency traces, repair targets, regimes, uncertainty, and severity. Use when task evaluation, counterexamples, anomalies, traces, or proof failures need to become solver-actionable failures.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Failure Classifier

## Overview

Turn a failed task into a determinate negation: a precise account of what failed, where, why, and which repair direction it suggests.

## Certificate Shape

```yaml
failure_certificate:
  id: string
  label: string
  concept: string
  witness: {}
  failed_obligation: string
  trace: []
  repair_target: []
  severity: low | medium | high | fatal_inside_regime | overextension_only
  regime: optional
  residual: optional
  uncertainty: optional
  assumptions: []
  unknowns: []
```

## Core Labels

Use these labels for mathematical/generic concepts when applicable:

`NonClosure`, `NonSolvability`, `Incompleteness`, `NonInvariance`, `Rigidity`, `Inconsistency`, `Undecidability`, `NonRepresentability`, `AmbiguousEquivalence`, `NonCompositionality`, `CaseExplosion`, `NoUniversalProperty`, `PoorTransfer`, `OverstrongAxiom`, `MissingCoherence`.

Use physics-specific labels when the failure is empirical, regime-bound, or measurement-bound:

`EmpiricalAnomaly`, `Overextension`, `NonCovariance`, `SymmetryMismatch`, `ConservationViolation`, `NonLocalConflict`, `Singularity`, `UVFailure`, `IRFailure`, `Instability`, `RepresentationDependence`, `ScaleMismatch`, `ParameterAdHocness`, `NonRenormalizability`, `NoLimitingCase`, `MeasurementGap`, `ConceptualUnderdetermination`, `DualDescriptionPressure`, `AnomalyCluster`.

Use language-model labels when the witness is model/system behavior:

`Hallucination`, `NoProvenance`, `ObjectiveInterfaceMismatch`, `ArithmeticWeakness`, `KnowledgeStaleness`, `ContextOverflow`, `PromptInjection`, `OverRefusal`, `SafetyViolation`, `ToolMisuse`, `ObservationMisuse`, `PlanningMyopia`, `RunawayLoop`, `ComputeInefficiency`, `EvaluationSaturation`, `GovernanceGap`.

## Classification Rules

- Require a witness. If the witness is missing, emit `unknown` and request evaluation evidence.
- Distinguish a real failure from a task outside declared regime; classify the latter as `Overextension` unless the regime declaration itself is evasive.
- For representational failures, identify the arbitrary choice that should not affect the result.
- For rigidity, identify the intended classification relation that strict identity blocks.
- For inconsistency, include the smallest known dependency trace or unsat core.
- For language-model failures, separate the layer: representation, architecture, training, interaction, tool/agent, or governance.
- Always attach a `repair_target`, such as `Complete`, `Adjunction`, `Invariantize`, `WeakenEquivalence`, `Stratify`, `Retrieve`, `Toolify`, `Govern`, or `RestrictRegime`.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output Discipline

Return ranked failure certificates, not prose only. Include alternative labels when classification is ambiguous.
