---
name: project-evolution-html-assembler
description: Assemble a self-contained, attractive HTML project evolution report from state, git-history, milestone, skill-theme, and SVG figure packets. Use when Codex needs the final readable report with current-state summary, skill-growth and skill-theme figures, commit-theme figures, and collapsible skill-theme sections.
---

# Project Evolution HTML Assembler

Use this as the final rendering hook in the project evolution reporting stack.

## Inputs

- current-state packet from `$project-state-profiler`
- git-history packet from `$git-history-evolution-miner`
- milestone packet from `$functionality-milestone-classifier`
- skill-theme packet from `$project-state-profiler`
- inline SVG figures from `$evolution-figure-builder`

## Procedure

1. Start with the current state summary.
2. Present current functionality as cards with concrete descriptions.
3. Show the timeline figures after the current functionality cards, including skill growth, skills by theme, and commit themes.
4. End with collapsible skill-theme sections containing all skills.
5. Keep the HTML self-contained: inline CSS and inline SVG, no external fonts, scripts, or image assets.

## Handoff

Write a single `.html` file and, when useful, a sibling `.json` metrics file.

The report should be attractive, compact, and narrative. Avoid audit-style headings unless the user asks for a compliance report.
