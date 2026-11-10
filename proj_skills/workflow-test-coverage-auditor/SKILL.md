---
name: workflow-test-coverage-auditor
description: Audit project-support and workflow features for nearby deterministic test coverage. Use when Codex should periodically compare scripts, workflow code, prompts, and skills against tests to identify untested generators, missing regression coverage, weak audit checks, or stale generated-doc validations.
---

# Workflow Test Coverage Auditor

Use this after script, skill, prompt, and test inventories are available.

## Inputs

- project-support scripts
- `agentic/**/*.py`
- `tests/**/test_*.py`
- skill and prompt inventory

## Procedure

1. Check every `proj_skills/*/scripts/*.py` file for at least one test reference.
2. Check key workflow scripts and routers for direct or indirect test references.
3. Check whether newly introduced report generators have JSON and HTML assertions.
4. Flag broad surfaces that have no obvious nearby tests.
5. Report coverage as an opportunity, not as proof of absence of behavior.

## Handoff

Leave `test_coverage_findings` with feature path, severity, coverage signal, and suggested test target.
