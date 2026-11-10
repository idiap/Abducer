---
name: hegelian-obligation-verifier
description: Generate and check validation obligations for Hegelian transformation candidates, including preservation, resolution, non-collapse, conservativity, universality, transfer, adequacy, residual-limit reporting, empirical validation, limiting-case recovery, measurement, risk, and governance. Use before a candidate can be ranked as accepted or called an Aufhebung.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Obligation Verifier

## Overview

Convert a candidate successor into explicit checks. Verification may be formal proof, bounded model search, tests, empirical validation, trace replay, or an open proof plan.

## Obligation Packet

```yaml
validation_packet:
  candidate_id: string
  obligations:
    - id: string
      kind: preservation | resolution | noncollapse | conservativity | universality | transfer | adequacy | residual_limit | formal | empirical | measurement | regime | risk | governance | efficiency
      statement: string
      method: proof | smt | model_finder | theorem_prover | test | simulation | benchmark | trace_replay | review | unavailable
      status: passed | failed | partial | unknown | planned | not_applicable
      evidence: []
      blocker: optional
  hard_gate_failures: []
  summary: string
```

## Core Checks

Always consider:

- Preservation: predecessor embeds, interprets, quotients, instantiates, or limits into successor.
- Resolution: motivating failure is repaired or relocated to a lower-ranked, explicit boundary.
- Non-collapse: protected distinctions, nontriviality, consistency, and safety/regression constraints survive.
- Conservativity: protected old-language truths are not changed by new machinery.
- Universality: universal constructions satisfy their mapping property.
- Transfer: generic theorems or behaviors instantiate back to motivating examples.
- Adequacy: the abstraction captures the target tasks.
- Residual limits: successor states what it still cannot do.

## Domain Checks

For physics:
- dimensional consistency, well-posedness, covariance, gauge independence, conservation, stability, causality/locality, limiting-case recovery, empirical residual reduction, uncertainty calibration, measurement validity, and anti-overfit checks.

For language-model systems:
- source support, citation/provenance accuracy, tool schema validity, side-effect safety, prompt-injection resistance, refusal calibration, helpfulness/honesty/harmlessness regression, latency/cost bounds, monitoring, and governance documentation.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Hard Gates

Mark a candidate blocked if:

- it fails non-collapse;
- it cannot preserve protected predecessor successes;
- a physics successor lacks a declared regime or measurement interface;
- latent ontology is unconstrained and untestable;
- a language-model successor adds unbounded side effects without approval or monitoring;
- a foundational move blocks the contradiction only by making the theory vacuous.

Never upgrade `planned` or `unknown` obligations to `passed`.
