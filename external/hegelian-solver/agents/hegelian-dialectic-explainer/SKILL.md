---
name: hegelian-dialectic-explainer
description: Explain Hegelian concept transitions in solver-grounded language, mapping typed failures or discovery signals to determinate negation, transformation, preservation, elevation, mediation, residual limits, and graph position. Use when a solver trace or candidate edge needs a concise human-readable rationale without metaphysical overclaiming.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Dialectic Explainer

## Overview

Produce explanations that make the dialectical structure legible while staying grounded in typed solver artifacts and evidence.

## Explanation Map

Use these translations:

- Concept: structured theory, model, system, or interface with tasks and protected meanings.
- Negation: failure, anomaly, or instability that shows the current concept's limit.
- Determinate negation: a typed failure certificate with witness and repair target.
- Contradiction: structured incompatibility between current constraints and intended role, not necessarily a formal logical contradiction.
- Aufhebung: certified transformation that resolves or relocates the failure while preserving predecessor structure and avoiding collapse.
- Preservation: embedding, interpretation, limiting map, regression preservation, effective-theory relation, or protected behavior.
- Elevation: the successor handles tasks or explanations unavailable to the predecessor.
- Mediation: explicit map, quotient, completion, measurement interface, tool layer, retrieval layer, governance layer, or graph edge connecting stages.
- Concrete universal: abstraction that organizes many formerly separate cases while remaining instantiated by them.

## Procedure

1. Name the predecessor concept and its intended role.
2. State the failure or discovery signal with its witness/evidence.
3. Explain why it is determinate: what specific missing structure or abstraction it points toward.
4. State the transformation and successor.
5. State what is preserved.
6. State what is newly resolved, generalized, or made explicit.
7. State non-collapse and domain checks in plain language.
8. State residual limits and future graph seeds.

## Guardrails

- Do not claim a transition is final.
- Do not call unverified candidates an `Aufhebung`; call them candidate repairs or proposed successors.
- Do not anthropomorphize language-model systems or physical theories.
- Do not hide tradeoffs, lost structure, new risk, or narrower regimes.
- Prefer concise explanations with links to certificates and graph edges.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output

Return a short narrative plus a structured `explanation_terms` block mapping source artifact IDs to dialectical terms.
