---
name: kb-expert-paper-generator
description: Transform final KB reasoning artifacts into a bridge-first expert report that explains the main conceptual bridges, their proof sketches, and the supporting high-potential hypotheses using transparent generative justification. Use when the user asks for a final scientific report, an expert-facing explanation of the leading bridge programs, or a rigorous explanation of why specific bridges/hypotheses deserve expert attention.
---

# KB Expert Paper Generator

## Conceptual Role

This skill converts the final inferential state into a paper-level argument centered on conceptual bridges and the proof sketches attached to them, together with a ranked expert recommendation portfolio over hypotheses.

## Framework Contribution

It operationalizes an explicit generative function for expert hypothesis selection, and a complementary bridge-priority model that balances bridge strength, abstraction maturity, proof-sketch quality, linked support, and proof readiness.

## How To Read Outputs

Read outputs as a decision paper: each highlighted bridge includes a conceptual explanation, attached proof-sketch rationale, failure logic, and concrete expert actions; each recommended hypothesis includes score decomposition, risk decomposition, and how it supports the bridge portfolio.

## Overview

Run this stage after pipeline artifacts are available.

It consumes final analysis artifacts and emits:

1. A machine-readable recommendation report (`expert-hypothesis-paper.json`).
2. A human-readable paper (`expert-hypothesis-paper.md`).
3. A publication-ready LaTeX draft (`expert-hypothesis-paper.tex`).

Read [references/script-usage.md](references/script-usage.md) for deterministic execution.
Read [references/generative-function.md](references/generative-function.md) for the scoring policy.
Read [references/prompt-template.md](references/prompt-template.md) for prompt-mode narrative rendering.

## Workflow

1. Load final artifacts (`coherence`, `entrypoints`, `pathways`, `hardness`, `strategies`, `proof-sketches`, `hypothesis-eval`, `hypothesis-loop`, `revision-loop`, `phyp`).
2. Build per-hypothesis feature vectors from typed signals only.
3. Compute potential and risk with the generative function.
4. Synthesize a bridge-first portfolio from bridge-plan, abstraction conjectures, and proof sketches.
5. Rank and tier hypotheses for expert review.
6. Write detailed bridge justifications, proof-sketch interpretations, and expert action plans.
7. Render scientific paper artifacts (`.md`, `.tex`) and full JSON provenance.

## Guardrails

- Use only structured, already-processed outputs as evidence.
- Keep lexical matches as structural references, not semantic substitutes.
- Every highlighted bridge must expose both constructive payoff and negative/impossibility pressure.
- Every recommendation must expose both upside and risk.
- Avoid hidden scoring; always include factor-level decomposition.

## Output Contract

Return:

1. `metadata`
2. `generative_function`
3. `bridge_selection_function`
4. `bridge_portfolio`
5. `recommended_bridges`
6. `hypothesis_scores`
7. `recommended_hypotheses`
8. `paper_markdown`
9. `paper_tex`

Use `scripts/generate_expert_paper.py` for deterministic outputs.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Reporting must not launder conjectural, blocked, or low-relevance routes into conclusions.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: report section, handoff claim, expert summary, proof narrative, table, and cited artifact.
- Preserved invariants: claim-to-evidence mapping, status labels, target commitments, source limits, and unresolved obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_expert_paper.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: claims with evidence paths or unknowns, epistemic status, target relevance, unresolved debt, demotion triggers, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
