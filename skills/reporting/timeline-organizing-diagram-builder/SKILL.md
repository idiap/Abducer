---
name: timeline-organizing-diagram-builder
description: Build a paper-ready organizing diagram from timeline report structure, strategy families, contribution candidates, validation handoffs, and formal derivation dependencies. Use when a paper draft needs a conceptual map, TikZ diagram, route schematic, or source-to-target flow rather than a prose-only narrative.
---

# Timeline Organizing Diagram Builder

## Workflow

Construct a diagram that is explanatory, not decorative:

1. Identify source objects, bridge objects, target commitments, falsifiers, and validation handoffs.
2. Arrange them as a route flow from problem commitments through timeline outputs to paper contributions.
3. Encode demotion or failure edges distinctly from constructive edges.
4. Emit TikZ-compatible diagram source and a caption that states the interpretation.

## Epistemic Discipline

Each node must correspond to a report artifact, cycle, contribution, literature obligation, or explicit unknown. Mark conjectural or validation-needed edges.

## Output Contract

Return: diagram nodes, edges, TikZ source, caption, evidence citations, epistemic status, and validation handoff.

## Failure/Demotion

Demote the diagram if it has unnamed nodes, decorative arrows, no validation handoffs, or hides the distinction between proof, obstruction, and conjectural route pressure.

## Validation Handoff

The paper validator must compile the TikZ diagram and find source, bridge, contribution, and validation nodes.
