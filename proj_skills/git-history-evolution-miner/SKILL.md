---
name: git-history-evolution-miner
description: Mine the full git log for project evolution reporting. Use when Codex needs commit dates, subjects, changed paths, skill-count history, monthly cadence, and full commit-message data for a timeline report.
---

# Git History Evolution Miner

Use this after `$project-state-profiler` when a report needs history rather than only current state.

## Inputs

- `git log --reverse`
- `git diff-tree --root --name-only -r <commit>`
- `git ls-tree -r --name-only <commit>`

## Procedure

1. Read the full commit history in chronological order.
2. For each commit, record SHA, date, subject, changed paths, and skill count at that commit.
3. Build monthly commit counts.
4. Preserve every commit message in the JSON data model for traceability, but do not require the HTML report to include a commit-message appendix.

## Handoff

Leave:

- `commits`
- `monthly_counts`
- `skill_count_by_commit`
- `all_commit_messages`

Do not drop old commits from the data model, even when the visual timeline later selects only major milestones.
