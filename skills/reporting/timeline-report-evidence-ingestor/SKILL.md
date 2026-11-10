---
name: timeline-report-evidence-ingestor
description: Parse the full Abducer discovery timeline report and companion artifacts into a typed paper evidence interpretation IR. Use when a timeline-derived paper needs systematic use of all report tabs, source-unit IDs, argument roles, body/appendix/future/quarantine dispositions, and coverage accounting before paper drafting.
---

# Timeline Report Evidence Ingestor

## Workflow

1. Load the embedded `marathon-data` payload from `agentic/reports/discovery_marathon/full_timeline.html`.
2. Load companion source artifacts: contribution monitor, target literature, macro strategy, strategy judge, parsimonious probes, formal derivation candidates, and timeline paper status.
3. Convert report elements into typed evidence units with mathematical object, source artifact, cycle ID when available, epistemic status, and argument role.
4. Assign each unit to exactly one disposition: main body, appendix, future work, or quarantine.
5. Emit coverage accounting for every report family so no populated tab is silently ignored.

## Epistemic Discipline

Treat report material as evidence with limits. Artifact presence is not proof. Every interpreted claim must cite source artifacts, cycle IDs, equation labels, explicit unknowns, or validation handoff fields. Mark proof-obligation, conjectural, promoted, blocked, refuted, validation-needed, and evidence-backed units explicitly.

Do not turn every report item into paper body prose. Use all information by interpreting and disposing it, not by dumping it.

## Output Contract

Return: interpretation ID, source report path, typed evidence units, mathematical object candidates, report-family coverage, missing-material warnings, disposition counts, epistemic status, validation handoff, and artifact paths.

## Failure/Demotion

Demote the paper workflow if the interpretation cannot name an active mathematical object, contribution candidate, formal derivation material, or validation boundary. Quarantine units that only restate workflow mechanics, lack evidence citation, overclaim, or cannot affect the paper argument.

## Codex Exec Protocol

Run the deterministic builder and validator rather than hand-writing the IR:

```bash
.venv-pmp/bin/python agentic/scripts/build_timeline_paper_interpretation.py
.venv-pmp/bin/python agentic/scripts/validate_timeline_paper_interpretation.py
```

Inspect the generated JSON and Markdown artifacts before using downstream skills.
