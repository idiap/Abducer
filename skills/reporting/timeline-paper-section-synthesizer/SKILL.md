---
name: timeline-paper-section-synthesizer
description: Synthesize coherent paper sections from the timeline paper blueprint, interpreted evidence units, formal derivation artifact, references, and diagrams. Use when the workflow needs main-body prose that follows a physics-paper argument rather than dumping report tabs or chronology.
---

# Timeline Paper Section Synthesizer

## Workflow

1. Read the paper blueprint and section responsibilities.
2. For each section, use only assigned evidence units and source artifacts.
3. Write prose in the function of the section: motivation, related work, route learning, formal core, worked calculation, mechanism, discussion, or appendix.
4. Keep definitions, assumptions, propositions, and validation boundaries explicit.
5. Emit section-level source unit IDs, accepted claims, demoted claims, unresolved obligations, and TeX.

## Epistemic Discipline

Use physics and mathematical language appropriate to the active object. Cite source artifacts and explicit unknowns. Preserve epistemic status and do not overclaim. Main-body prose must support the blueprint thesis; appendix material preserves evidence without controlling the argument.

## Output Contract

Return: section ID, title, purpose, responsible skill, source unit IDs, body prose, LaTeX, accepted claims, demoted claims, unresolved obligations, epistemic status, and validation handoff.

## Failure/Demotion

Demote a section if it is a report dump, repeats chronology, lacks mathematical object definitions, has no evidence citations, hides validation debt, or introduces claims outside the blueprint.

## Codex Exec Protocol

Run:

```bash
.venv-pmp/bin/python agentic/scripts/build_timeline_paper_sections.py
.venv-pmp/bin/python agentic/scripts/validate_timeline_paper_sections.py
```
