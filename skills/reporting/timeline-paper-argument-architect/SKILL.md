---
name: timeline-paper-argument-architect
description: Build a coherent physics-paper argument blueprint from interpreted timeline report evidence. Use when paper creation needs a primary paper mode, thesis, contribution-to-evidence matrix, section responsibilities, non-claims, body/appendix/archive partition, and narrative budget before TeX drafting.
---

# Timeline Paper Argument Architect

## Workflow

1. Read `agentic/reports/timeline_paper_interpretation/latest.json`.
2. Choose one primary paper mode: theorem note, worked-calculation note, obstruction note, method note, negative-result note, or survey-positioning note.
3. State the main thesis, smallest honest contribution claims, mathematical object, and overclaim boundary.
4. Map each contribution to evidence units, novelty-boundary units, validation-burden units, and non-claims.
5. Assign section responsibilities and narrative budget before any prose section is written.

## Epistemic Discipline

The blueprint is a claim license, not a proof. Every contribution claim must cite evidence units and explicit validation handoff obligations. Separate finite/local claims from target-theorem claims. Mark conjectural, proof-obligation, validation-needed, promoted, blocked, and demoted material.

Do not let the paper mode drift during writing. If evidence supports only an obstruction note, do not write as if it were a theorem proof.

## Output Contract

Return: blueprint ID, paper mode, title, abstract claim, main thesis, primary mathematical object, contribution claims, section plan, body/appendix/future/quarantine partitions, claim-reference map, non-claims, narrative budget, epistemic status, and validation handoff.

## Failure/Demotion

Demote or quarantine the paper draft if no smallest honest claim can be stated, if no mathematical object is source-backed, if references are decorative, if validation burdens are absent, or if the body plan becomes raw chronology.

## Codex Exec Protocol

Run:

```bash
.venv-pmp/bin/python agentic/scripts/build_timeline_paper_blueprint.py
.venv-pmp/bin/python agentic/scripts/validate_timeline_paper_blueprint.py
```
