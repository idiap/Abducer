---
name: workflow-graph-html-reporter
description: Render HTML and SVG workflow graph reports. Use when Codex needs an attractive visual report for large hierarchical agentic workflows, including workflow descriptions, family-to-workflow-to-step hierarchy, ordered workflow sequence, overview maps, expanded stack lanes, typed interaction edges, hoverable Cytoscape.js graph inspection, and reflective-loop diagrams.
---

# Workflow Graph HTML Reporter

Use this after `$workflow-graph-modeler`.

## Inputs

- graph model from `$workflow-graph-modeler`
- extracted workflow contracts from `$workflow-contract-extractor`

## Procedure

1. Render HTML with inline CSS and inline SVG static views.
2. Start with a compact summary of total stacks, total hooks, unique skills, shared skills, and reflective stacks.
3. Show a workflow hierarchy graph that preserves family, workflow, and ordered step levels.
4. Show an overview graph that groups workflow stacks by family.
5. Show a shared-skill interaction graph so repeated hooks and cross-stack reuse are visible.
6. Show a reflective-loop graph that separates review, planning, refinement, guard, and closure roles.
7. Add an optional Cytoscape.js graph explorer for granular inspection when a JavaScript graph library is acceptable.
8. Provide graph-view controls so readers can switch between workflow sequence/hierarchy and cross-stack interactions.
9. Use hover or selection details for stack descriptions, skill roles, edge type, output type, sequence index, and handoff property.
10. Use collapsible per-stack lanes for detailed ordered hooks.
11. Keep labels readable and avoid forcing all nodes into one hairball diagram.

## Handoff

Write a single `.html` file and, when useful, a sibling `.json` graph model.
