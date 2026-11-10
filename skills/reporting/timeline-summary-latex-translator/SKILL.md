---
name: timeline-summary-latex-translator
description: Translate timeline-report summaries, current queue, contribution readiness, strategy judgement, success milestones, and next-analysis state into LaTeX. Use when the report summary tab or executive state needs to become a paper-safe abstract, conclusion, status section, or next-work section.
---

# Timeline Summary LaTeX Translator

## Workflow

1. Extract the current claim boundary, major contribution candidate, readiness state, and decisive next action.
2. Translate queues into next analyses, not operational task lists.
3. State success milestones and stop/pivot criteria in content-specific terms.
4. Preserve non-claims and unresolved obligations.
5. Write summary LaTeX suitable for abstract, conclusion, or future-work sections.

## Epistemic Discipline

Preserve epistemic status: claimable-now, validation-needed, conjectural, proof-obligation, blocked, promoted, demoted, or refuted. Cite source artifacts, queue item IDs, cycle IDs, report paths, and explicit unknowns.

Do not turn a queue item into a result. A next-analysis item is only evidence of control unless it is backed by a completed theorem, calculation, citation check, or validator.

## Output Contract

Return: LaTeX abstract/conclusion/status section, current contribution statement, readiness class, decisive next analyses, success criteria, stop/pivot criteria, non-claims, source citations, epistemic status, and validation handoff.

## Failure/Demotion

Demote the section if it uses generic queue language, omits what is claimable now, hides unresolved obligations, or makes paper readiness sound stronger than the validation state.

## Validation Handoff

The LaTeX must compile and name the current contribution candidate, the strongest next analysis, and the reason the result is or is not paper-ready.
