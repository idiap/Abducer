---
name: project-state-profiler
description: Profile the current repository state for a project-support report. Use when Codex needs current key functionality, use-case/reference-project count, skill count, prompt count, prompt-line count, class count, function count, method count, test count, tracked file count, and lines-of-code metrics before building a project evolution timeline.
---

# Project State Profiler

Use this as the first hook in the project evolution reporting stack.

## Inputs

- repository root
- git-tracked file list
- current working tree contents

## Procedure

1. Count scientific skills from `skills/*/*/SKILL.md`, project-support skills from `proj_skills/*/SKILL.md`, and Prism workflow skills from `prism_me/*/SKILL.md`.
2. Count problem knowledge bases from tracked `KB/*.kb.md` documents; do not assume each problem is a directory.
3. Count Python classes from tracked `.py` files.
4. Count top-level Python functions and direct class methods separately.
5. Count prompt/control files from scientific and project-support `SKILL.md`/`agents/openai.yaml` surfaces plus Prism skill contracts, and count their nonblank lines.
6. Count test files from `tests/**/test_*.py` and test cases from `def test_*`.
7. Count nonblank lines for tracked code/config/documentation extensions.
8. Identify current functionality areas from concrete files, not only README prose.
9. Cluster every skill by theme so the final report can end with collapsible skill groups.

## Handoff

Leave a compact current-state packet with:

- `tracked_files`
- `commits`
- `use_cases`
- `skills`
- `classes`
- `functions`
- `methods`
- `prompts`
- `prompt_lines`
- `test_files`
- `test_cases`
- `lines_of_code`
- `key_functionality`
- `skill_theme_clusters`

The packet should be suitable for the first section of a human-readable HTML report.
