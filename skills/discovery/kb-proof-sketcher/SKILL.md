---
name: kb-proof-sketcher
description: Given conjecture, strategy, bridge, and hypothesis artifacts, outline structured proof sketches for the strongest conjectures. Use when the user asks for proof-sketch mode, conjecture-targeted proof outlines, sketching how a bridge concept could be proved, or defining proof-strategy families for a conjectured mathematical object.
---

# KB Proof Sketcher


## Conceptual Role

This skill transforms promising conjectures and strategies into structured proof sketches with obligations, lemmas, checkpoints, and failure modes.

## Framework Contribution

It contributes near-proof organization by turning bridge programs into ordered mathematical argument templates.

## How To Read Outputs

Read its outputs as conditional proof programs: the unresolved obligations indicate exactly why the route is not yet a finished proof.

## Overview

Run the distinct `proof-sketch` inference mode.

This stage does not merely rank strategies. It turns a conjectured bridge object into a testable proof outline:

- chooses a proof-strategy family appropriate to the conjecture
- states the proof obligations required for the conjecture to pay off
- sequences the likely lemma/program structure
- inserts barrier checkpoints and abort conditions so the sketch remains falsifiable
- carries both constructive and negative/impossibility-oriented assessment when that sharpens the bridge object
- emits a structured contradiction/impossibility program rather than only narrative negative-route prose
- renders the top pathway as a paper-style conditional argument with proposition, lemmas, and proof

Use it after `conjecture` and `strategies` when the framework knows which bridge object it wants, but still needs an explicit proof plan.

Read [references/script-usage.md](references/script-usage.md) for the executable interface.
Read [references/prompt-template.md](references/prompt-template.md) when a narrative proof-sketch prompt is needed.

## Workflow

1. Load structured artifacts only: `conjectures`, `strategies`, `bridges`, `phyp`, and optional `analysis`, `coherence`, `hardness`.
2. Match conjectured bridge concepts to the most relevant strategy anchors and bridge programs.
3. Select a proof-strategy family: invariant lift, surrogate reduction, barrier escape, contradiction/collapse, derandomization transfer, or regime split.
4. Derive both constructive and negative/impossibility proof-space assessments for the bridge object.
5. Derive proof obligations, candidate lemmas, barrier checkpoints, and abort conditions.
6. Emit a human-readable proof outline for each prioritized conjecture.
7. When the KB is available, translate the strongest final pathway into a paper-style mathematical argument artifact.

## Guardrails

- Use typed processed outputs rather than raw lexical scans over the KB body.
- Treat proof sketches as executable research plans, not completed proofs.
- Every sketch must expose what would kill the route, not only what would support it.
- Prefer sketches whose obligations are theorem-family specific and traceable to statement IDs, bridge IDs, and conjecture IDs.
- Negative or impossibility-oriented sketches are first-class if they sharpen the status of the bridge object.

## Output Contract

Return:

1. `metadata`
2. `proof_sketches`
3. `recommended_execution_order`

Use `scripts/generate_proof_sketches.py` for deterministic outputs.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Novelty is not value; generated hypotheses must carry status labels and disconfirming observations before receiving active attention.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: candidate bridge, conjecture, entrypoint, proof sketch, route family, or conceptual transformation.
- Preserved invariants: target commitments, source-grounded definitions, bridge compatibility, and explicit proof obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_proof_sketches.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
