<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prism Alignment

Use this pack as if you are preparing an external project for eventual Prism onboarding.

## Non-Negotiables

1. Typed boundaries before prompt prose.
   Define inputs, outputs, invocation rules, coordination role, and reasoning-log expectations before talking about implementation style.

2. Invocation is part of the contract.
   Name how the capability is reached: manual, planner-routed, hook-driven, threshold-driven, or evaluation-stage.

3. Durable outputs are primary.
   Specs, plans, reports, ledgers, and generated artifacts are the stable interface. Reasoning logs are required sidecars, not substitutes.

4. Coordination is lifecycle-first.
   Make it obvious whether the capability belongs to intake, execution, maintenance, evaluation, or external-runtime handoff.

5. Provenance stays explicit.
   If a capability wraps an external script, preserved repo subtree, or third-party runtime, keep the boundary visible instead of flattening it away.

6. Dependencies are first-class structure.
   Map dependency bundles, runtime dependencies, reference KBs, backend profiles, workspace mounts, and capability source paths explicitly enough that later Prism import work can preserve them.

7. Validation must be evidence-backed.
   Claims need tests, outputs, file references, or reproducible checks. Unsupported claims belong in open questions or remaining uncertainty.

8. Explanation is part of the deliverable.
   When work touches Python or Markdown, annotate those files so a new agent can quickly understand the core concept, intent, role in the system, and local decision logic.

## Practical Translation

For external projects, keep enough structure that the result can later be translated into:

- planner metadata
- a typed agent contract
- `uv` bundle and runtime dependency mapping
- reference KB and backend profile mapping
- runtime adapter workspace-mount expectations
- imported-runtime adapter metadata
- reasoning-log expectations
- a catalog-facing onboarding bundle

Do not optimize for pretty prose. Optimize for future composability.
