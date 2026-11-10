<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Cycle Failure Archaeology

Target: `p-vs-np-target`
Run: `p-vs-np-marathon`
Cycle set: `failure-set.0e897ad17bb2`
Cycles: `['cycle-0150', 'cycle-0151', 'cycle-0152', 'cycle-0153', 'cycle-0154']`
Failure detected: `True`
Disposition: `persist_with_new_artifact_gate`

## Failure Summary

The route became artifact-bound: the next proof move depends on missing tables, intervals, tails, source data, or explicit certificates.

## Why This Was Hard

Physics hardness:

- The cycle set did not expose enough target-specific physics language to diagnose a physics-hardness channel.

Mathematical hardness:

- Positivity is fragile under projection, Schur/Feshbach reduction, closure topology, endpoint singular terms, and source aggregation.
- The decisive sign or transfer claim depends on interval arithmetic and uniform tail bounds, so qualitative reasoning cannot close the gate.
- Source-derivative data are high-order and equivalence-class dependent; the proof needs exact objects, not narrative source geometry.
- Bridge theorems risk circularity unless source and target properties remain independently meaningful.

Representation hardness:

- The efficient representation must encode endpoint/source equivalence classes and aggregate before clipping; otherwise the sign problem is mislocalized.

## Why It Failed

- The route became artifact-bound: the next proof move depends on missing tables, intervals, tails, source data, or explicit certificates.

## Why We Did Not Anticipate It

- Local progress can hide global fragility: each cycle may sharpen a lemma while delaying the artifact or transfer condition that actually decides the route.
- The workflow previously asked whether the branch was target-linked, but not always whether the precise missing artifact was already visible before the cycle began.
- A successful representation can be misleading when it explains the obstruction after the fact but does not expose the earliest cheap falsifier before investment.

## Anticipatory Heuristics

### artifact_debt

Detected: `True`

Why it matters: A branch cannot move by reasoning alone when promotion depends on a named missing artifact.

Prompt heuristic: Before proof search, ask: which concrete table, interval, bound, code output, or theorem must exist for this hypothesis to become live?

Pre-cycle gate: If the artifact is absent after repeated blockers, route to artifact_sprint, falsifier_sprint, demotion, or quarantine.

### proxy_shift

Detected: `True`

Why it matters: A proof route can become easier by silently changing the object instead of solving the target problem.

Prompt heuristic: Ask whether the source object and target object remain in the same theory, regulator, observable family, and validity regime.

Pre-cycle gate: Quarantine until same-domain transfer or same-theory carrier preservation is explicit.

### finite_to_global_gap

Detected: `True`

Why it matters: Finite support work can be valuable but does not by itself produce continuum, asymptotic, or Clay-level progress.

Prompt heuristic: Ask which finite claim is honest and which continuum/asymptotic/non-claim boundary remains untouched.

Pre-cycle gate: Demote to support-only unless the next artifact directly tests a target-facing transfer gate.

### uniformity_gap

Detected: `True`

Why it matters: A bound that is not uniform across the relevant limit can explain local success and global failure at the same time.

Prompt heuristic: Ask which parameter, cutoff, volume, source, or limit must be uniform, and what would falsify uniformity.

Pre-cycle gate: Require a uniform bound ledger or a quarantine decision before promotion.

### definitional_transfer

Detected: `True`

Why it matters: A transfer theorem is low value if it defines the target property as the image of the source property.

Prompt heuristic: Ask whether source and target properties remain independently meaningful after the bridge is removed.

Pre-cycle gate: Reframe or demote until the transfer has independent source and target content.

### no_decisive_falsifier

Detected: `False`

Why it matters: A hypothesis that cannot fail will usually keep generating plausible but non-decisive cycles.

Prompt heuristic: Ask for the cheapest pass/fail test whose failure changes the route state.

Pre-cycle gate: Block ordinary proof search until a falsifier or artifact sprint exists.

### low_publication_reward

Detected: `False`

Why it matters: A correct lemma can still be a poor investment if it cannot change field understanding or support a major paper.

Prompt heuristic: Ask what a field reader would understand differently if this succeeds, and whether that difference is publication-weighty.

Pre-cycle gate: Do not invest ordinary cycles unless the major-publication gate is invest_high_physics_reward.

### repeated_blocker

Detected: `True`

Why it matters: Repeating the same blocker means the branch has stopped learning unless the next cycle produces the named artifact or a new representation.

Prompt heuristic: Ask whether the next cycle changes the blocker type, produces the missing artifact, or only rephrases the same obligation.

Pre-cycle gate: Route to artifact_sprint, falsifier_sprint, publication_demotion, or quarantine.

## Required Workflow Change

- Attach failure_archaeology after every failed major cycle set.
- Run failed-hypothesis-anticipator before ordinary proof search on any branch emerging from a failed set.
- Expose the disposition in reports and queue selection before another marathon.

## Evidence

- agentic/runs/discovery_marathons/p-vs-np-marathon/run_state.json
- agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0150.json
- agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0151.json
- agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0152.json
- agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0153.json
- agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0154.json

Validation handoff: `agentic/scripts/validate_cycle_failure_archaeology.py`
