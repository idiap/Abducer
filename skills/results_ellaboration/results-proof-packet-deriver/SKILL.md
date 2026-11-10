---
name: results-proof-packet-deriver
description: Derive a scoped paper-result theorem packet from definitions and hypotheses, exposing proof steps, proof debt, countermodels, and manuscript-ready theorem/proof text. Use when a result candidate needs proof closure rather than more exploration.
---

# Results Proof Packet Deriver

## Conceptual Role

This skill turns a scoped theorem and formalized objects into a proof packet. It is deliberately narrower than discovery: it proves, blocks, or demotes the result candidate.

## Workflow

1. Read the theorem scope packet and finite-object definitions.
2. Normalize theorem statement, hypotheses, conclusion, and non-claims.
3. Derive the proof step by step. For each step, state:
   - input definitions or assumptions;
   - inference rule or known theorem;
   - resulting equation, inequality, construction, or contradiction.
4. If the proof fails, localize the exact missing lemma or countermodel.
5. Produce manuscript-facing theorem/proof text only for proved or conditional pieces.

## Proof Status Labels

Use exactly one primary status:

- `proved_scoped_theorem`
- `conditional_theorem`
- `finite_certificate`
- `proof_obligation_localized`
- `countermodel_found`
- `demoted_overclaim`

## Output Contract

Return: theorem statement, proof status, definitions used, hypotheses used, proof steps, equations/inequalities, blocked step or countermodel, manuscript theorem text, manuscript proof text, limitations paragraph, and validation handoff.

## Epistemic Discipline

Assign an epistemic status to every theorem packet: proved scoped theorem, conditional theorem, finite certificate, proof obligation localized, countermodel found, or demoted overclaim. Cite evidence through source artifacts, KB IDs, cycle IDs, theorem labels, draft sections, validation reports, or explicit unknowns. State the mathematical object, invariant, and counterexample class used to justify proof or demotion.

## Guardrails

- Do not replace a missing proof with a narrative of why the result feels plausible.
- Do not promote a theorem when the proof only covers a restricted model unless the theorem statement says so.
- Do not omit constants, exponent losses, regulator/model assumptions, or advice costs when they control the result.
- Do not call a proof "complete" if a domain reviewer must still decide model preservation.

## Validation Handoff

Hand off to `results-prior-art-disqualifier-auditor` for novelty/disqualifier closure and to `results-paper-readiness-gatekeeper` before manuscript promotion.

## Failure/Demotion

Demote when a hypothesis is equivalent to the target claim, when a proof step changes the model or target class, when a counterexample invalidates the statement, or when the proof remains schematic after the claimed derivation.
