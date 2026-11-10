<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Target Run Separation

- Generated: `2026-07-10T08:41:45+00:00`
- Global active run: `yang-mills-smoke-marathon` for `yang-mills-existence-and-mass-gap-target`

## Targets

### P vs NP

- Target id: `p-vs-np-target`
- Domain: computational complexity theory
- Pointer: `agentic/runs/discovery_marathons/active_targets/p-vs-np-target.json`
- Run: `p-vs-np-marathon` (initialized)
- Branches: 3
- Strategy label: Complexity Strategy
- Story label: Proof Strategy Story

### Yang-Mills existence and mass gap

- Target id: `yang-mills-existence-and-mass-gap-target`
- Domain: mathematical physics
- Pointer: `agentic/runs/discovery_marathons/active_targets/yang-mills-existence-and-mass-gap-target.json`
- Run: `yang-mills-smoke-marathon` (paused)
- Branches: 6
- Strategy label: Physics & Maths Strategy
- Story label: Physics Story

## Separation Contract

- Each target has a separate active pointer under agentic/runs/discovery_marathons/active_targets/.
- The global active_run.json may switch between targets, but target-specific pointers are preserved.
- Marathon branch prompts are generated from target_profiles.py, not from another target's current report.
- Cycle validation checks target-specific consistency markers and rejects known cross-target vocabulary.
