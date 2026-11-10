---
name: hegelian-conceptual-creativity-reasoner
description: Explain why a Hegelian solver transformation candidate is a creative move rather than a merely corrective one, grounded in its own trigger, preservation map, and expected obligations. Use after candidate generation (and ideally after ranking) when a report needs to classify a candidate's conceptual operation, separate repair from genuine affordance creation, and name what it preserves, risks, and opens up next.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Conceptual Creativity Reasoner

## Purpose

Answer one question per candidate: is this move creative, or does it only restore what the determinate negation broke? "Creative" here is not a vibe — it means the candidate introduces a new constructive resource or affordance the predecessor concept did not have, beyond what was strictly required to fix the trigger. A move that only re-establishes a broken core obligation (preservation, resolution, non-collapse, residual-limit reporting) is a repair, not a creative act, even if it is a good repair.

This is the layer between candidate generation/ranking and the report's narrative sections: it makes the report's later "Concrete Concept Evolution" and "Formal Reasoning Notation" sections legible as *creative* developments rather than opaque renamings.

## Required Inputs

- The candidate's `operator`, `target_concept`, `preservation_map`, `resolution_mechanism`, `changed_structure`, `expected_obligations`, `residual_limits`, `assumptions`, and `unknowns`.
- The trigger that produced the candidate: a `FailureCertificate` (`label`, `failed_obligation`) or `DiscoverySignal` (`label`, `candidate_move`, `evidence`).
- The candidate's `ValidationPacket`, when available, for obligation status and blockers.

## Conceptual Operation Taxonomy

Classify every candidate's operator into exactly one operation. Compare cases across domains by operation, not by operator name:

- `closure_completion`: adjoins a missing result instead of forbidding the case (e.g. completing a structure under an operation).
- `abstraction_interface_discovery`: names a reusable interface or structure shared across cases instead of leaving it implicit.
- `invariance_reparameterization`: re-describes the object so a distinction that used to matter is reparameterized away.
- `quotienting_redundancy_removal`: identifies a distinction that was never load-bearing and collapses it.
- `localization_regime_restriction`: scopes a claim to where it actually holds instead of defending it as universal.
- `externalization_or_tooling`: moves a capability outside the core object and invokes it on demand instead of building it in.
- `bridge_mediation`: introduces an explicit relation connecting two previously separate descriptions or domains.
- `latent_carrier_introduction`: posits a new entity to carry an explanatory role nothing in the current ontology can carry.
- `governance_safety_scaffold`: adds the accountability or control layer a capability needs once it is powerful enough to misfire.

If an operator does not obviously fit one of these, pick the closest one and say so explicitly in `residual_todos` rather than inventing a tenth category silently.

## Repair vs. Affordance Creation

1. List the candidate's `expected_obligations` that are **not** one of the four core obligations (`preservation`, `resolution`, `noncollapse`, `residual_limit`).
2. If that list is empty, the move is a `repair`: it only restores what the trigger broke. Say so plainly; do not manufacture a creativity claim.
3. If the list is non-empty, the move at least partly creates a new affordance. Classify it `affordance_creation` unless the operation is `quotienting_redundancy_removal`, `localization_regime_restriction`, or `governance_safety_scaffold` — those usually read as guardrails or simplifications more than expansions, so classify them `mixed` instead.

## Procedure

1. Identify the source pressure: the trigger's `kind` (`failure` or `discovery_signal`), `id`, `label`, and the exact statement (failed obligation, or candidate move) it asserts. Do not paraphrase away the trigger's own words.
2. State the latent tension in one sentence using the trigger's own label and statement.
3. Classify the operation (see taxonomy above) and state the creative reframing: what shift in framing the operation performs, in plain language, not just the operator's name.
4. Decide repair vs. affordance creation vs. mixed (see above), and name every new affordance explicitly — one phrase per non-core expected obligation.
5. Name what is preserved: the preservation map's `kind`/`relation`, plus any concept-level `preservation` constraints carried into the target.
6. Name the generative payoff: what becomes possible for *future* development once this move exists, not just what it fixes now.
7. Name creative risks: the candidate's `residual_limits`, `unknowns`, and any obligation `blocker` from its validation packet.
8. Name downstream concept seeds: the same residual limits and unknowns, read forward as the next determinate negations the successor concept will face.
9. Write one explicit sentence — `why_creative_not_corrective` — that states the verdict and the reason. If it is a repair, say so without padding.
10. If any of the six required-explicit fields (source pressure, operation, new affordance, preserved invariant, risk/tradeoff, downstream concept seeds) cannot be grounded in an actual artifact, do not fabricate content for it: record the gap as a `residual_todo` instead.

## Style

- Ground every sentence in a named artifact (trigger id, obligation kind, preservation map field, residual limit string). No claim should be unattributable.
- Default to readable prose for the lead explanation; keep the full structured payload (taxonomy, affordances, risks, seeds) collapsible/secondary.
- Do not call a `repair` creative to make the report more exciting. A correctly identified repair is not a failure of the analysis.
- Keep this analysis distinct from the ranking decision: a candidate can be creative and still be rejected, or be a plain repair and still be accepted.

## Output Shape

Return:

```yaml
conceptual_creativity_analysis:
  candidate_id: string
  operator: string
  operation: closure_completion | abstraction_interface_discovery | invariance_reparameterization | quotienting_redundancy_removal | localization_regime_restriction | externalization_or_tooling | bridge_mediation | latent_carrier_introduction | governance_safety_scaffold
  repair_vs_affordance: repair | affordance_creation | mixed
  source_pressure:
    kind: failure | discovery_signal
    id: string
    label: string
    statement: string
  latent_tension: string
  creative_reframing: string
  new_constructive_resource: string
  new_affordance: []
  preservation_under_transformation: []
  generative_payoff: []
  creative_risks: []
  why_creative_not_corrective: string
  downstream_concept_seeds: []
  residual_todos: []
```

## Guardrails

- Never assert a new affordance that isn't backed by an actual non-core expected obligation or declared structural change.
- Never leave `source_pressure`, `operation`, `preservation_under_transformation`, `creative_risks`, or `downstream_concept_seeds` empty without recording the gap in `residual_todos`.
- Do not collapse a `mixed` move into `affordance_creation` just because it has a non-empty new-affordance list; check the operation-kind rule first.
- Do not present this analysis as a validated outcome; it explains a candidate's conceptual shape, not its acceptance status.
