<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Architecture

Understand components, data flow, contracts, and extension points. This section is for readers learning or using Abducer.

```text
problem and literature → conceptual branches → critique and typed evidence
                       → semantic reduction → atomic epistemic-state commit
                       → post-commit proof and delayed experiment work
```

`agentic/` contains the typed discovery runtime and state; `skills/` holds scientific
skills; `KB/` grounds targets; `InformalMathLib/` retains mathematical memory;
`phyp/` publishes proof hypotheses; `artifacts/` holds target outputs.
`proj_skills/` and `prism_me/` support repository maintenance and request controls.

See the [system architecture](architecture.md),
[data contracts](data-contracts.md), and
[research methods](../research-methods/README.md).

## Retained specialist index

Use this section to understand Abducer's system boundaries, artifact flow, orchestration, and publication contracts before changing implementation.

- [System architecture](architecture.md) — normative architecture overview.
- [Data contracts](data-contracts.md) — reference for durable artifact schemas.
- [Orchestration](orchestration.md) — normative workflow and loop semantics.
- [Named workflows](named-workflows.md) — conceptual roles, activation boundaries, and handoffs across active and opt-in workflows.
- [Canonical discovery publication](canonical-discovery-publication.md) — publication transaction contract.
- [`phyp` publication](phyp-publication.md) — proof-hypothesis publication contract.
- [Reasoning traces](reasoning-trace-architecture.md) and [compatibility](reasoning-trace-compatibility.md).
- [Reasoning-trace PDF architecture](reasoning-trace-pdf-architecture.md) and [compatibility](reasoning-trace-pdf-compatibility.md).


Return to the [documentation index](../README.md) or consult the
[documentation map](../reference/documentation-map.md) for the complete retained collections.
