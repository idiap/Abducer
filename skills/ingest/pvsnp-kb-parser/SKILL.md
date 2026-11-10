---
name: pvsnp-kb-parser
description: Parse LaTeX-heavy P vs NP research reports into structured KB statements and write them into `KB/p-vs-np.kb.md`. Use when the user provides files like `deep-research-report.md` containing `\begin{definition}`/`\begin{theorem}` style environments and asks to ingest them into a PvsNP knowledge base.
---


# PvsNP KB Parser


## Conceptual Role

This skill parses structured research notes or deep-research reports into candidate mathematical statements for KB population.

## Framework Contribution

It contributes extraction discipline by separating raw source text from canonicalized statement blocks before ingestion.

## How To Read Outputs

Read its outputs as source-derived candidate statements that still need curation, filtering, or KB writeback.

## Overview

Extract theorem-like environments from a P vs NP report and convert them into KB statement records with stable IDs, provenance, and section context.

Read [references/mapping-rules.md](references/mapping-rules.md) for normalization policy.
Read [references/script-usage.md](references/script-usage.md) for command examples.

## Workflow

1. Ensure target KB exists.
Use `KB/p-vs-np.kb.md`; initialize from `KB/problem-template.kb.md` if needed.

2. Parse report environments.
Run `scripts/parse_report.py` on the input report to extract statement JSON.

3. Normalize and write back.
Use parser `--kb` mode to auto-insert a `# Source Index` row and append statements via `kb_writeback.py`.

4. Validate output.
Confirm IDs are unique, source IDs are attached, and canonical/derived sections were updated.

5. Report ingest summary.
Return statement count, environment breakdown, KB path, and unresolved parsing limits.

## Guardrails

- Do not infer unquoted theorems that are not explicitly present in theorem-like environments.
- Keep `proposition` -> `theorem` and `remark` -> `observation` mapping explicit in `notes`.
- Keep each parsed statement linked to the report source ID.
- Treat this parser as a first pass; use follow-up curation for dependency links.

## Output Contract

When summarizing parser runs, include:

1. Input report path.
2. Output JSON path.
3. Total parsed statements.
4. Counts by environment type.
5. KB file updated and number of canonical vs derived additions.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Ingestion does not validate truth; it only preserves inspectable source structure for later reasoning.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: source statement, theorem body, symbol, definition, citation, normalized KB card, and dependency edge.
- Preserved invariants: source text provenance, symbol identity, statement dependency, confidence status, and explicit missing fields.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `parse_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: normalized statements, source IDs, explicit unknowns, parse failures, artifact paths, validation result, and next repair. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
