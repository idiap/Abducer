---
name: workflow-orphan-skill-auditor
description: Audit catalog and workflow coverage across scientific, Prism, and project-support skills. Use when checking for missing index entries, absent metadata, or underdocumented hooks while distinguishing specialized skills from true orphans.
---

# Workflow Orphan Skill Auditor

Use this after the workflow and skill inventory is available.

## Inputs

- `skills/*/*/SKILL.md`
- `proj_skills/*/SKILL.md`
- `prism_me/*/SKILL.md`
- [docs/reference/skills.md](../../docs/reference/skills.md)
- [Prism agent contract](../../prism_me/agents.md) and active coverage checklist
- [proj_skills/INDEX.md](../INDEX.md)
- [AGENTS.md](../../AGENTS.md)
- tests and prompt files

## Procedure

1. Count every skill definition.
2. Verify scientific skills against their catalog, Prism skills against its agent contract/checklist, and agent metadata where applicable.
3. Verify each project-support skill appears in [proj_skills/INDEX.md](../INDEX.md).
4. Record whether each skill appears in a workflow hook surface such as [AGENTS.md](../../AGENTS.md) or [proj_skills/INDEX.md](../INDEX.md).
5. Distinguish missing catalog/index entries from intentionally specialized skills that are cataloged but not hooked into a stack.

## Handoff

Leave `orphan_skill_findings` with severity, skill path, missing surface, and repair suggestion.
