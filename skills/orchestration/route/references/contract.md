<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Rigid capability-binding contract

`route` joins three authorities:

1. the `.prism` program declares required reasoning occurrences;
2. `essential_reasoning_types.yaml` declares which skills materialize each
   reasoning type and whether the mapping is primary or secondary;
3. `skill_registry.yaml` declares whether the concrete skill exists.

The `default` profile in `reasoning_capability_routes.yaml` is an explicit
policy, not a learned ranking. An occurrence-level binding overrides the
profile only when the requested skill is registered and mapped to that type.

A binding plan is executable only when all occurrences are typed and bound.
Unresolved `_` occurrences remain blockers. Compilation neither invokes skills
nor validates their eventual outputs.
