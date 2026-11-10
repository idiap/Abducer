---
name: project-workflow-graph-reporter
description: Orchestrate project-support workflow graph reporting. Use when Codex should visualize declared Prism and project-support topology from repository coordination contracts as offline HTML and JSON, while distinguishing declarations from observed runtime behavior.
---

# Project Workflow Graph Reporter

Use this skill to understand the current workflow system visually.

This is the orchestrator hook for workflow graph reporting:

1. `$workflow-contract-extractor`
2. `$workflow-graph-modeler`
3. `$workflow-graph-html-reporter`

## Workflow

1. Run the bundled deterministic generator from the repository root:

   ```bash
   python proj_skills/project-workflow-graph-reporter/scripts/generate_workflow_graph_report.py --repo . --output docs/reports/project_workflow_graphs.html --json-output docs/reports/project_workflow_graphs.json
   ```

2. Confirm that [Project Support Skill Index](../INDEX.md) is included as the
   supplemental architecture source when it exists.
3. Inspect the generated HTML in a browser.
4. Use the JSON model when you need exact stack, hook, shared-skill, or reflective-loop data.

## Representation Strategy

- Use multiple coordinated views instead of one giant graph.
- Use workflow hierarchy as the default dynamic view: family -> workflow -> ordered hook step.
- Use sequence edges to show first-hook entry, hook-to-hook order, and guarded reflective loop returns.
- Use overview grouping for orientation.
- Use shared-skill edges for interaction.
- Use a separate reflective-loop diagram for critic, planner, refiner, guard, and closure roles.
- Keep static SVG and JSON complete and offline. Add interactivity only when its implementation is locally bundled and safely escapes repository-controlled labels.
- Encode edge meaning explicitly:
  - `family_contains_workflow`: workflow family contains a workflow stack.
  - `workflow_entry`: workflow starts at its first hook.
  - `workflow_sequence`: ordered hook output feeds the next hook step.
  - `workflow_reflective_loop`: guarded critique/refinement can return to earlier workflow criteria or hooks.
  - `stack_uses_skill`: workflow stack invokes a hook.
  - `skill_handoff`: ordered hook output feeds the next hook.
  - `reflective_feedback`: critique/refinement/guard findings can update the workflow.
- Use collapsible stack lanes for detailed ordered hooks.

## Hook Discipline

- Keep project-support visualization skills under `proj_skills/`.
- Do not change scientific discovery workflow semantics while generating graphs.
- Treat [AGENTS.md](../../AGENTS.md) as an onboarding pointer, `prism_me/agents.md` plus the active Prism request as the control contract, and [Project Support Skill Index](../INDEX.md) as the project-support topology.
- Keep workflow descriptions visible in both JSON and HTML so the graph does not become only a topology diagram.

## Conceptual Explanatory Core

- Explain the declared architecture as ordered typed handoffs, cross-stack shared hooks, and guarded feedback returns.
- Preserve forward sequence and feedback-loop semantics as different edge kinds.
- Name the highest-fanout shared hooks and representative reflective workflows without duplicating the full graph model.
- State that the graph describes declared topology, not runtime activation, success, or cost.
- Use a topology legend and coupling reading suited to graph reasoning. Do not reuse the evolution trace, health calibration rails, or runtime transition view.
