<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Cycle Failure Archaeology

Target: `yang-mills-existence-and-mass-gap-target`
Run: `yang-mills-smoke-marathon`
Cycle set: `failure-set.062bcf6856c4`
Cycles: `['cycle-0348', 'cycle-0349', 'cycle-0350', 'cycle-0351', 'cycle-0352']`
Failure detected: `True`
Disposition: `persist_with_new_artifact_gate`

## Failure Summary

The route became artifact-bound: the next proof move depends on missing tables, intervals, tails, source data, or explicit certificates.

## Why This Was Hard

Physics hardness:

- Same-theory transfer is hard because the carrier must survive without changing regulator, observable algebra, boundary sector, or normalization.
- The route must connect gauge-invariant Euclidean observables to OS/Wightman reconstruction or spectral data without smuggling in a proxy object.
- Cutoff, volume, and regulator limits are not passive bookkeeping; they can destroy local positivity, cumulant witnesses, or spectral carriers.
- Nontriviality has to be carried by a same-theory observable witness, not by formal nonzero terms in a changed or fixed-regulator model.

Mathematical hardness:

- Positivity is fragile under projection, Schur/Feshbach reduction, closure topology, endpoint singular terms, and source aggregation.
- The decisive sign or transfer claim depends on interval arithmetic and uniform tail bounds, so qualitative reasoning cannot close the gate.
- Source-derivative data are high-order and equivalence-class dependent; the proof needs exact objects, not narrative source geometry.
- Bridge theorems risk circularity unless source and target properties remain independently meaningful.

Representation hardness:

- The failed cycles exposed a representation-fit problem: some carriers were too coarse to decide the gate, while raw local objects were too fragmented to transfer.
- The efficient representation must encode endpoint/source equivalence classes and aggregate before clipping; otherwise the sign problem is mislocalized.

## Why It Failed

- The route became artifact-bound: the next proof move depends on missing tables, intervals, tails, source data, or explicit certificates.

## Why We Did Not Anticipate It

- Local progress can hide global fragility: each cycle may sharpen a lemma while delaying the artifact or transfer condition that actually decides the route.
- The workflow previously asked whether the branch was target-linked, but not always whether the precise missing artifact was already visible before the cycle began.
- A successful representation can be misleading when it explains the obstruction after the fact but does not expose the earliest cheap falsifier before investment.
- In YM, finite Wilson/OS vocabulary can look physically promising before same-theory carrier survival, cutoff-uniformity, and continuum/spectral gates are separately certified.

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

### missing_physical_carrier

Detected: `False`

Why it matters: YM work without a physical carrier can drift into mathematically tidy but physically irrelevant estimates.

Prompt heuristic: Ask which gauge-invariant observable, Schwinger family, OS Hilbert object, spectral object, or cumulant witness carries the claim.

Pre-cycle gate: Reframe or quarantine until the physical carrier is named.

### noncommuting_limits

Detected: `True`

Why it matters: YM routes often fail because local regulator arguments do not commute with continuum, volume, or reconstruction limits.

Prompt heuristic: Ask for an order-of-limits ledger and the first limit where the carrier might disappear.

Pre-cycle gate: Require limit-order assumptions and a falsifier before claiming physics relevance.

## Required Workflow Change

- Attach failure_archaeology after every failed major cycle set.
- Run failed-hypothesis-anticipator before ordinary proof search on any branch emerging from a failed set.
- Expose the disposition in reports and queue selection before another marathon.

## Evidence

- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/run_state.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0348.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0349.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0350.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0351.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0352.json

Validation handoff: `agentic/scripts/validate_cycle_failure_archaeology.py`
