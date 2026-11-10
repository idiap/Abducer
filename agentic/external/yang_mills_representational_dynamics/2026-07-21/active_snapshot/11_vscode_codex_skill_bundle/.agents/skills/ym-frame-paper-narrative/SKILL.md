---
name: ym-frame-paper-narrative
description: Frame the motivation, abstract, contribution statement, and self-contained introduction of a Yang--Mills or mathematical-physics paper from a frozen theorem contract and verified novelty position. Use when a manuscript needs a theorem-led narrative, conceptual motivation, problem-to-result bridge, scope calibration, or removal of research-workflow language.
---

# Frame the Paper Narrative

## Required inputs

Read the frozen theorem statement, claim-status ledger, novelty matrix, intended audience, and closest literature before writing. If any is absent, create a provisional version and label it.

## Build the argument

1. Identify the phenomenon or mathematical tension that matters independently of the project history.
2. State the precise technical bottleneck exposed by that tension.
3. Explain why the closest existing methods do not already settle this bottleneck, citing the literature audit rather than asserting a gap.
4. State the paper's exact result, hypotheses, domain, and consequence.
5. Explain what the result changes in the reader's understanding or available proof strategy.
6. State limitations only where they prevent a likely misreading.

Use this sequence for the introduction:

```text
physical or mathematical motivation
  -> exact unresolved question
  -> closest known approaches
  -> paper theorem/conceptual contribution
  -> proof mechanism
  -> consequences and scope
  -> paper organization
```

## Write the front matter

- Draft a title that names the result rather than the programme.
- Draft a 150--250 word abstract containing the object, theorem, method, and consequence.
- Put the central theorem or contribution in the first two pages.
- Give a numbered contribution list only when the items are genuinely distinct.
- Make the introduction self-contained: define specialized language or point to the exact section that does.
- Replace stage numbers, “next target,” “improvement,” “previous gap,” and package chronology with mathematical relations.
- Prefer affirmative statements of contribution. Use negative scope statements only to block a material overclaim.

## Coherence checks

- Every motivation paragraph must terminate in a question answered by the paper.
- Every claimed gap must map to a literature-matrix row.
- Every abstract claim must map to a theorem, proposition, formal argument, or explicitly labeled interpretation.
- The conclusion must answer the introduction's question using the same quantifiers.
- For Yang--Mills work, distinguish regulated, finite-volume, conditional, continuum, and Hamiltonian claims.

## Output contract

Produce `narrative_contract.md`, `abstract.tex`, `introduction.tex`, and `conclusion.tex`. Include a claim-to-section map and a list of narrative sentences that require citation or proof before submission. Finish Yang--Mills manuscripts with `ym-audit-frontier`.
