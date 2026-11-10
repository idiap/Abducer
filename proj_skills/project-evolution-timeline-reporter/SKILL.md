---
name: project-evolution-timeline-reporter
description: Orchestrate the granular project evolution reporting stack. Use when Codex should run project-state profiling, git-history mining, milestone classification, inline figure building, skill-theme clustering, and HTML assembly to produce an attractive, self-contained project history report with current metrics, skill-count timeline, aggregate skill-theme plot, functionality milestones, and collapsible skill-theme sections.
---

# Project Evolution Timeline Reporter

Use this skill to turn the current repository and its full git history into a readable project-evolution report.

This is the orchestrator hook for the project support stack:

1. `$project-state-profiler`
2. `$git-history-evolution-miner`
3. `$functionality-milestone-classifier`
4. `$evolution-figure-builder`
5. `$project-evolution-html-assembler`

## Workflow

1. Use the stack above conceptually, then run the bundled deterministic generator from the repository root:

   ```bash
   report_dir=$(mktemp -d)
   python proj_skills/project-evolution-timeline-reporter/scripts/generate_project_evolution_report.py --repo . --output "$report_dir/project_evolution_timeline.html" --json-output "$report_dir/project_evolution_timeline.json"
   ```

2. Inspect the generated HTML in a browser, or read the JSON if you need exact counts.
3. If the report is too noisy, rerun with `--max-milestones N` to limit the visible milestone cards. The full commit history remains available in the collapsible appendix.

## What The Report Must Include

- A current-state summary first: key functionality areas, number of skills, use cases/reference projects, prompts, prompt lines, classes, functions, methods, test files, test cases, tracked files, commits, and lines of code.
- A timeline-oriented evolution section with embedded inline SVG figures:
  - skill count over git history
  - skills grouped by theme
  - commit volume by functionality area
- Key functionality milestones inferred from commit messages and changed paths.
- A final collapsible set of all skills clustered by theme.

## Hook Discipline

- Do not merge project support skills into the domain-scientific `skills/` catalog.
- Keep reusable project-maintenance skills under `proj_skills/`.
- Let the script provide deterministic execution; let the granular skills explain the reasoning surfaces and handoffs.
- If a future report needs a new stage, add it as a new `proj_skills/<stage-name>/SKILL.md` and list it in [proj_skills/INDEX.md](../INDEX.md).

## Interpretation Rules

- Treat `skills/*/*/SKILL.md`, `proj_skills/*/SKILL.md`, and `prism_me/*/SKILL.md` as distinct skill-definition surfaces.
- Treat tracked `KB/*.kb.md` files as problem knowledge bases; do not infer use cases from nonexistent directories.
- Treat `tests/**/test_*.py` files and `def test_*` functions as the test surface.
- Treat Python `class` declarations as class count evidence.
- Treat top-level Python `def` and `async def` as function-count evidence.
- Treat direct `def` and `async def` under a class as method-count evidence.
- Treat scientific/project-support skill and agent metadata plus Prism contracts as prompt/control files and count nonblank lines as prompt-line evidence.
- Cluster every scientific, project-support, and Prism skill entry by theme and render each theme as a collapsible section.
- Use git-tracked files for current-state metrics so ignored run artifacts do not dominate the report.
- Use commit subjects and changed paths to classify milestones; the classification is an explanatory summary, not a release-note substitute.

## Conceptual Explanatory Core

- Build an evolution thesis from selected commits, changed paths, and the current capability inventory.
- Explain a bounded set of milestone transitions as changes in repository emphasis: prior focus, new focus, change subject, date, and commit anchor.
- Keep current metrics and exhaustive skill themes outside the explanatory core.
- State that history classification supports chronology and change-surface interpretation; it does not prove release quality, adoption, or unstated author intent.
- Use a transition trace suited to historical reasoning. Do not reuse the topology, health-audit, or runtime visual grammar.

## Output Standard

The report should feel like a product history poster: visual, compact, and readable. Avoid bureaucratic audit language. The appendix can be exhaustive, but the main narrative should focus on what changed and why it matters.
