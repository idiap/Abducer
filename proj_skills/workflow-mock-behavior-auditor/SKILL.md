---
name: workflow-mock-behavior-auditor
description: Audit workflow tests and implementation surfaces for mocked, stubbed, fake, or placeholder behavior that could mask weak validation. Use when Codex should periodically find mocks, stubs, monkeypatches, synthetic fixtures, TODO placeholders, and skipped behavior, then distinguish legitimate isolated tests from evidence that should not be presented as full workflow validation.
---

# Workflow Mock Behavior Auditor

Use this as a focused hook in periodic workflow health reviews.

## Inputs

- `tests/**/*.py`
- `agentic/**/*.py`
- project-support scripts
- generated audit context

## Procedure

1. Search for mock, monkeypatch, stub, fake, placeholder, synthetic, skip, xfail, and TODO markers.
2. Classify findings as:
   - test isolation
   - dependency substitute
   - placeholder implementation
   - skipped validation
   - synthetic fixture
3. Flag placeholder implementation and skipped validation higher than ordinary test isolation.
4. Avoid claiming a problem solely because a unit test uses a mock; require context.

## Handoff

Leave `mock_behavior_findings` with severity, path, line, category, and review recommendation.
