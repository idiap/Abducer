<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Forward Test: Epistemologist Review

## Purpose

Validate that representative Abducer skills preserve claim-to-evidence discipline during long-horizon creative exploration.

## Fixtures

- `tests/fixtures/skill-depth/yang_mills_target_case.json`
- `tests/fixtures/skill-depth/p_vs_np_route_case.json`

## Skills To Probe

- Control-plane: `looper-release-promoter`
- Discovery: `abducer-mediation-candidate-generator`
- Evaluation: `epistemic-status-ledger`
- Orchestration: `long-horizon-route-portfolio-manager`
- Reporting: `kb-expert-paper-generator`

## Probe Prompt

Use the named skill on one fixture. Return a route-status judgment that includes:

1. claim text;
2. epistemic status: conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive;
3. evidence paths, KB IDs, dependency nodes, or explicit unknowns;
4. disconfirming observations;
5. demotion or falsification triggers;
6. uncertainty and source limits;
7. next action with a validator, artifact, TODO, or stop condition.

## Shallow Output Rejection

Reject the output and create a follow-up TODO if it:

- converts conjectural material into a conclusion without evidence;
- hides unknowns in generic caveats;
- lacks disconfirming observations or demotion triggers;
- recommends promotion without a validation handoff;
- lets a low-relevance or high-drift route consume active budget.

## Passing Oracle

The output passes only if an epistemologist can trace every substantive claim to evidence or an explicit unknown, see what would falsify the route, and understand why the next action controls drift rather than rewarding fluency.
