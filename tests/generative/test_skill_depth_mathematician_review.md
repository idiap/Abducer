<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Forward Test: Mathematician Review

## Purpose

Validate that representative Abducer skills produce mathematically deep outputs on realistic targets instead of fluent route labels.

## Fixtures

- `tests/fixtures/skill-depth/yang_mills_target_case.json`
- `tests/fixtures/skill-depth/p_vs_np_route_case.json`

## Skills To Probe

- Control-plane: `looper-workflow-contract-governor`
- Discovery: `kb-concept-bridge-planner`
- Evaluation: `bridge-object-equivalence-checker`
- Orchestration: `long-horizon-route-portfolio-manager`
- Reporting: `expert-handoff`

## Probe Prompt

Use the named skill on one fixture. Return a compact route decision that includes:

1. mathematical objects compared or transformed;
2. definitions or target commitments used;
3. preserved invariants;
4. broken or unknown invariants;
5. at least one edge case, counterexample class, or boundary regime;
6. proof obligations needed before promotion;
7. artifact paths or explicit unknowns.

## Shallow Output Rejection

Reject the output and create a follow-up TODO if it:

- uses labels like promising, relevant, or elegant without naming objects and invariants;
- treats an artifact path as proof progress;
- omits counterexample or boundary-regime pressure;
- promotes a route while dropping an essential target commitment;
- fails to distinguish a mathematical witness from a narrative rationale.

## Passing Oracle

The output passes only if a mathematician can identify the precise theorem-shaped object under discussion, the invariants that must survive, the regimes where the route can fail, and the smallest proof obligation that would change the route status.
