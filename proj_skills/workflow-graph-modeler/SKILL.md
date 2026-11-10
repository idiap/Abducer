---
name: workflow-graph-modeler
description: Model extracted workflow stacks as readable graph structures. Use when Codex needs to classify many workflow stacks into visual groups, preserve family-to-workflow-to-step hierarchy, encode ordered workflow sequence, detect shared skills, identify critic/refiner/guard reflective loops, encode typed edge semantics and output types, and choose static or dynamic graph layouts for large hierarchical agentic workflows.
---

# Workflow Graph Modeler

Use this after `$workflow-contract-extractor`.

## Inputs

- extracted workflow-stack packet
- skill hook names and stack ordering

## Procedure

1. Classify stacks into coarse visual groups:
   - control
   - meta learning
   - source intake
   - generation and scientific artifact semantics
   - execution and runtime
   - testing
   - review and signoff
   - reference and comparison
   - writing and reporting
   - project support
2. Detect reflective loop roles from skill and stack names:
   - critic/review/audit/signoff
   - gap/planning/TODO
   - refiner/refinement/improvement
   - guard/closure
   - feedback/second-order/meta
3. Build four graph views:
   - workflow hierarchy: family -> workflow -> ordered hook steps
   - overview: stack families and their sizes
   - interaction: shared skills and cross-stack reuse
   - reflection: review-to-planning-to-guard-to-update loops
4. Build a dynamic graph model when granular inspection is needed:
   - family nodes
   - workflow/stack nodes
   - ordered workflow-step nodes
   - shared skill nodes where cross-stack reuse matters
   - `family_contains_workflow` edges for hierarchy
   - `workflow_entry` edges for first-hook entry
   - `workflow_sequence` edges for hook-to-hook order
   - `workflow_reflective_loop` edges for guarded refinement returns
   - `stack_uses_skill` edges with hook order and output type
   - `skill_handoff` edges between ordered hooks inside a workflow
   - `reflective_feedback` edges for closed critic/refiner/guard loops
5. Prefer multiple coordinated views over one dense graph when the workflow count is large.

## Handoff

Leave a graph model with workflow descriptions, layout groups, hierarchy nodes, ordered sequence edges, stack summaries, shared-skill edges, typed skill-interaction edges, reflective-loop evidence, and visual-design notes for `$workflow-graph-html-reporter`.
