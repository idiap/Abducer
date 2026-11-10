---
name: timeline-report-latex-composer
description: Compose timeline report tabs into a coherent LaTeX packet by coordinating timeline-cycle-latex-translator, timeline-story-latex-translator, timeline-problem-literature-latex-translator, and timeline-summary-latex-translator. Use when full timeline report content including timeline, story, problem/literature, summary, queue, and contribution state must become TeX sections or a paper draft input.
---

# Timeline Report LaTeX Composer

## Workflow

1. Load the report JSON/HTML payload and identify available tabs: summary, timeline, accumulated story, problem/literature, macro strategies, paper status, and queues.
2. Prefer the interpretation IR and blueprint when they exist; raw tab translation is appendix evidence, not the paper spine.
3. Invoke `timeline-summary-latex-translator` for abstract/conclusion/status material.
4. Invoke `timeline-problem-literature-latex-translator` for introduction/background/related work.
5. Invoke `timeline-story-latex-translator` for strategy progression and conceptual narrative.
6. Invoke `timeline-cycle-latex-translator` for selected timeline evidence rows or appendix material.
7. Compose the sections into one LaTeX packet with a section map, citation map, non-claims, source-unit IDs, body/appendix roles, and validation handoff.

## Epistemic Discipline

Preserve epistemic status across all sections: evidence-backed, conjectural, proof-obligation, validation-needed, blocked, promoted, demoted, refuted, or claimable-now. Cite source artifacts, cycle IDs, report paths, literature references, and explicit unknowns.

Do not let the composed LaTeX become an indiscriminate report dump. Body text must support the paper thesis; detailed chronology belongs in an appendix or archive.

## Output Contract

Return: section map, composed LaTeX packet, source artifact map, citation map, selected cycle IDs, appendix/body split, current claim boundary, non-claims, epistemic status, and validation handoff.

## Failure/Demotion

Demote the packet if it fails to compile, has duplicate or contradictory sections, omits citations, hides uncertainty, or lets low-value timeline details overwhelm the coherent paper argument.

## Validation Handoff

Run the timeline LaTeX-section builder and validator when available. The output must compile, include all four content families, and preserve bounded paper claims.
