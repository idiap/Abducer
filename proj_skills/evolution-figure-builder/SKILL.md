---
name: evolution-figure-builder
description: Build embedded visual figures for project evolution reports. Use when Codex needs inline, self-contained SVG charts for skill growth, aggregate skill-theme distribution, functionality-theme commit volume, or timeline milestones without external image assets.
---

# Evolution Figure Builder

Use this after `$functionality-milestone-classifier`.

## Inputs

- skill count over commits
- skill-theme cluster counts
- selected milestones
- category counts
- monthly cadence

## Procedure

1. Render figures as inline SVG, not external image files.
2. Include a skill-growth line chart over git history.
3. Include an aggregate skills-by-theme bar chart sourced from the same clusters used by the final skill list.
4. Include a functionality-theme bar chart.
5. Keep labels short enough for the report layout.
6. Use SVG `<title>` elements for milestone dots when helpful.

## Handoff

Leave embeddable SVG strings and chart captions ready for `$project-evolution-html-assembler`.

The visual style should feel polished and readable, not like an exported spreadsheet.
