<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Literature-Gap Preinvestment Gate Plan

## Purpose

New proof or discovery avenues should not enter ordinary API marathon cycles
because they sound interesting. They should first pass a literature-gap and
relevance gate that shows the avenue addresses a real gap, not a rediscovered
known result, a proxy problem, or an incremental local calculation with weak
field value.

The gate is not a bibliography chore. It is an investment warrant: it explains
why this avenue deserves research budget now.

## Diagnosis

The current workflow already has target-level literature context and
prior-art checks, but these mostly act after a target or result is already
active. That leaves a failure mode:

- a new avenue is selected from internal conceptual pressure;
- proof-search cycles begin;
- prior art is checked only when a result is near paper-ready or blocked;
- the route can spend substantial cycles before discovering that the gap is
  already known, too weak, physically irrelevant, or not publication-weighted.

For Yang-Mills this is especially dangerous because a local finite theorem,
restricted model, endpoint estimate, visual analogy, or representation
mechanism can be mathematically correct while failing to change the physics
understanding of the Clay problem. A literature gap must therefore be tied to
the target commitments: same-theory construction, nontriviality,
OS/Wightman reconstruction, gauge-invariant observable content, continuum
control, and positive spectral-gap interface.

## Gate Principle

Before broad exploration, proof lock-in, or a long API marathon invests in a
new avenue, the workflow must produce an `avenue_literature_gap_warrant`.

The warrant must answer:

1. What is the smallest honest avenue claim?
2. Which closest known results, route families, or expert surveys already touch
   this object?
3. What is the specific gap, stated as an unmet hypothesis, missing transfer,
   absent computation, unproved estimate, conceptual tension, or unresolved
   representation problem?
4. Why is this gap relevant enough to justify research investment?
5. What would change in field understanding if the gap were closed or
   decisively falsified?
6. What disqualifiers would demote the avenue before further proof search?

## Required Warrant Fields

- `target_id`
- `avenue_id`
- `smallest_honest_claim`
- `mathematical_or_physical_object`
- `target_commitments_touched`
- `closest_known_results`
- `source_search_provenance`
- `gap_statement`
- `why_not_already_known`
- `relevance_threshold`
- `physics_or_field_impact`
- `unification_power`
- `route_decision_power`
- `novelty_boundary`
- `disqualifier_matrix`
- `explicit_unknowns`
- `allowed_next_modes`
- `investment_decision`
- `validation_handoff`

## Decision Classes

- `invest_in_avenue`: the literature gap is cited, specific, target-relevant,
  and potentially publication-weighted.
- `artifact_sprint_only`: the gap may matter, but the next action must be a
  bounded computation, source import, theorem statement, or falsifier before
  broad reasoning.
- `reframe_gap_before_investment`: the sources suggest a possible gap, but the
  claim is too vague, too broad, or not tied to a target commitment.
- `do_not_invest_prior_art_collision`: nearby literature already covers the
  claim, or a stronger known result subsumes it.
- `quarantine_low_relevance`: the avenue may be mathematically interesting but
  does not have enough target, physics, or publication relevance.

## Relevance Heuristics

A gap is relevant enough only if it satisfies most of these conditions:

- It touches a named target commitment, not just a local proof convenience.
- It would change a route decision: promote, pivot, backtrack, quarantine, or
  convert to paper handoff.
- It has conceptual depth: it acts on a genuine tension such as same-theory
  transfer, nontriviality, continuum control, barrier escape, or spectral
  reconstruction.
- It has explanatory power: success or failure would explain why a route works
  or fails.
- It has unification power: one mechanism, representation, estimate, or carrier
  compresses multiple pressures rather than adding an adjacent lemma.
- It has a novelty boundary against closest known work.
- It has a finite next validation action.

## Integration Point

The new gate should sit between `branch_selection` and `branch_exploration`,
and also run whenever a visual analogy, failure archaeology packet, or
conceptual abstraction proposes a new avenue.

Default routing rule:

- no warrant: run only literature-gap precheck;
- warrant says `invest_in_avenue`: allow ordinary branch exploration;
- warrant says `artifact_sprint_only`: run only the named artifact sprint;
- warrant says reframe, do not invest, or quarantine: block broad API proof
  search for that avenue.

## Non-Goals

- Do not require exhaustive literature review before every small local repair.
- Do not treat lack of found literature as proof of novelty.
- Do not block conceptual exploration after a branch is released, demoted, or
  quarantined; instead require a new warrant before the next avenue receives
  ordinary research budget.
- Do not let a generic literature paragraph satisfy the gate.

## Validation Standard

The implementation is complete only when:

- a schema and validator reject uncited or vague gap warrants;
- the scheduler refuses broad exploration for new avenues without a warrant;
- target reports show the warrant and decision class visibly;
- fixtures cover a valid gap, prior-art collision, vague gap, low-relevance
  gap, and artifact-sprint-only case;
- the Yang-Mills workflow can apply the gate to Route A, representational
  dynamics, and visual-conceptualization-inspired avenues without cross-target
  contamination.
