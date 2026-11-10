---
name: workflow-health-audit-orchestrator
description: Orchestrate periodic project-support workflow health reviews. Use when Codex should revisit workflow stacks from time to time and systematically check for blind-run leakage, orphaned or underhooked skills, poor prompt control, mocked behavior, weak deterministic testing coverage, and improvement opportunities as HTML and JSON.
---

# Workflow Health Audit Orchestrator

Use this skill to periodically review the health of the workflow framework itself.

This is the orchestrator hook for workflow health auditing:

1. `$workflow-leakage-auditor`
2. `$workflow-orphan-skill-auditor`
3. `$workflow-prompt-control-auditor`
4. `$workflow-mock-behavior-auditor`
5. `$workflow-test-coverage-auditor`
6. `$workflow-health-html-reporter`

## Workflow

1. Run the bundled deterministic audit generator from the repository root:

   ```bash
   audit_dir=$(mktemp -d)
   python proj_skills/workflow-health-audit-orchestrator/scripts/generate_workflow_health_audit.py --repo . --output "$audit_dir/workflow_health_audit.html" --json-output "$audit_dir/workflow_health_audit.json"
   ```

2. Inspect severity counts first, then review the grouped findings.
3. Treat findings as triage inputs. Confirm high-impact changes before editing core workflow behavior.
4. Publish a reviewed report under `docs/generated/` only when it should become a maintained documentation artifact; ad hoc audits stay temporary.

## Review Dimensions

- leakage and blind-run boundary risk
- orphaned, uncataloged, or underhooked skills
- prompt control and output-contract weakness
- mocked, stubbed, skipped, or placeholder behavior
- missing or weak deterministic test coverage

## Hook Discipline

- Keep this under `proj_skills/`; it audits project/workflow health rather than domain scientific artifact semantics directly.
- Prefer diagnostic findings and TODO candidates over silent workflow edits.
- Distinguish intentionally post-hoc reference handling from actual generation-path leakage.
- Distinguish legitimate test isolation from mocked behavior that is being overclaimed as validation.

## Conceptual Explanatory Core

- Explain which audit dimension concentrates the strongest triage signals and why it deserves confirmation.
- Assign each dimension an explicit posture such as repository cross-reference, context-sensitive boundary scan, marker scan, or reference heuristic.
- Keep every health finding at `triage_signal` strength until source context or runtime evidence confirms a defect.
- Give one decision rule: confirm the matched context and owning workflow contract before changing core behavior.
- Use calibration rails suited to audit reasoning. Do not reuse the history, topology, or runtime visual grammar.
