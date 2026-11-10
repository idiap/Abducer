---
name: timeline-definition-assumption-elicitor
description: Elicit and surface missing definitions, assumptions, validity regimes, and non-claim boundaries for Abducer discovery timeline entries. Use when marathon cycles, timeline reports, paper timelines, equations, derivation steps, candidate lemmas, or story beats need to be self-contained for an expert reader instead of relying on hidden context.
---

# Timeline Definition Assumption Elicitor

## Role

Use this skill whenever a timeline entry contains a formula, derivation step, bridge claim, falsifier, or route-control decision whose meaning depends on unstated objects or conditions. The goal is to make the timeline scientifically readable: an expert should know what the symbols denote, what assumptions hold, which validity regime is being used, and what the entry does not claim.

## Elicitation Procedure

1. **Detect definition pressure.**
   Ask whether the entry names a mathematical object, carrier, class, observable, operator, route family, or parameter that is not defined in the same card or linked result. If yes, elicit the minimal local definitions.

2. **Detect assumption pressure.**
   Ask whether a derivation, equation, transfer, obstruction, or falsifier only holds under model, regime, uniformity, density, cutoff, advice, naturalness, or same-theory assumptions. If yes, elicit those assumptions before interpreting the step.

3. **Attach validity regimes.**
   Every displayed equation should state when it is valid. Prefer content-specific regimes such as "for a fixed circuit class with target-query exponent beta" or "for reflected Wilson collars with the same boundary footprint" over generic "under assumptions".

4. **Name non-claims.**
   If the entry is a sketch, analogy, finite witness, restricted-model result, or branch-control diagnosis, state what it does not prove. This protects the timeline from overclaiming.

5. **Feed the next analysis.**
   Convert missing definitions and assumptions into next-analysis obligations. A branch should continue only if the next step sharpens a definition, tests an assumption, validates a regime, or closes a proof obligation.

## Epistemic Discipline

Assign an epistemic status to the elicited context: `defined`, `assumption_explicit`, `validity_regime_explicit`, `hidden_assumption_suspected`, `underdefined`, `proxy_risk`, or `proof_obligation`. Cite evidence paths, cycle IDs, branch IDs, equations, validator outputs, KB IDs, or explicit unknowns. Do not use elicited assumptions as proof; they are conditions that make proof obligations legible.

## Output Contract

Return:

- `definitions_needed`: missing objects or symbols and the local definition to add.
- `assumptions_needed`: hypotheses, regimes, or model commitments required for validity.
- `validity_regime`: when the formula, derivation, transfer, or falsifier applies.
- `non_claim_boundary`: what the timeline entry does not prove.
- `timeline_patch`: concise text suitable for the timeline card.
- `next_obligation`: the next proof, calculation, prior-art, or validation step.
- `evidence`: cycle IDs, branch IDs, report paths, or explicit unknowns.
- `validation_handoff`: the validator or report artifact that should enforce the elicitation.

## Failure/Demotion

Demote or quarantine a timeline entry when it uses formulas without symbol definitions, derives a conclusion without assumptions, hides a model switch, omits a validity regime, or turns a restricted/proxy statement into a main-problem claim. Falsify the timeline patch if `agentic/scripts/validate_discovery_marathon_cycle.py` or `agentic/scripts/validate_discovery_marathon_report.py` rejects the rendered definitions, assumptions, or MathJax output.
