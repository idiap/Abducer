---
name: timeline-cycle-latex-translator
description: Translate discovery-marathon timeline cycle entries into compact, paper-safe LaTeX. Use when cycle-level entries, branch outputs, equations, falsifiers, blocking gaps, or next experiments from the timeline report need to become a LaTeX timeline table, appendix section, or evidence-backed chronology without turning every cycle into paper body prose.
---

# Timeline Cycle LaTeX Translator

## Workflow

1. Select only cycles that change the mathematical object, proof obligation, falsifier, computation target, or paper claim boundary.
2. Translate each selected cycle into a compact LaTeX row or paragraph with cycle ID, branch title, learning, key equation, blocking gap, and next action.
3. Preserve equation validity conditions and avoid naked formulas.
4. Compress repeated cycles into one progression statement instead of copying chronology.
5. Mark whether the cycle belongs in the paper body, appendix, or archive.

## Epistemic Discipline

Preserve epistemic status explicitly: evidence-backed cycle learning, conjectural interpretation, proof-obligation, validation-needed, blocked, promoted, demoted, or refuted. Cite source artifacts, cycle IDs, report paths, and explicit unknowns for every cycle-level claim.

Do not claim mathematical progress from operational progress. A cycle enters LaTeX only when it changes the finite theorem, worked calculation, transfer certificate, prior-art boundary, or honest contribution statement.

## Output Contract

Return: LaTeX section title, selected cycle IDs, one LaTeX table or enumerated timeline, equations with validity regimes, appendix/body placement, epistemic status for each entry, source artifact citations, non-claims, and validation handoff.

## Failure/Demotion

Demote the translation if it becomes a log dump, omits cycle IDs, strips equation assumptions, hides failed/pending obligations, or presents repeated route restatements as new results.

## Validation Handoff

The LaTeX must compile, contain cycle references, avoid unescaped special characters, and keep mathematical claims linked to source cycles and validation-needed obligations.
