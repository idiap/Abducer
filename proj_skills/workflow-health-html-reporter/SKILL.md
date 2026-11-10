---
name: workflow-health-html-reporter
description: Render periodic workflow health audit findings as concise HTML and JSON. Use when Codex needs to present leakage, orphan-skill, prompt-control, mocked-behavior, and testing-coverage findings with severity counts, actionable recommendations, and readable grouped details.
---

# Workflow Health HTML Reporter

Use this after the focused audit hooks have produced findings.

## Inputs

- `leakage_findings`
- `orphan_skill_findings`
- `prompt_control_findings`
- `mock_behavior_findings`
- `test_coverage_findings`
- workflow and skill inventory summary

## Procedure

1. Start with overall severity counts.
2. Group findings by audit dimension.
3. Show actionable recommendations before detailed rows.
4. Use collapsible finding lists for each dimension.
5. Keep the report diagnostic and periodic; do not overstate review findings as proofs.

## Handoff

Write self-contained HTML and optional JSON for periodic workflow review.
