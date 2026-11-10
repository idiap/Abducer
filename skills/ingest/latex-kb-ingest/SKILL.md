---
name: latex-kb-ingest
description: Build or update a single-file mathematical knowledge base from informal LaTeX sources. Use when the user provides web pages, PDFs, notes, or pasted text and asks to extract definitions, axioms, theorems, lemmas, assumptions, or symbol meanings into a structured KB file in the `KB/` folder.
---


# LaTeX KB Ingest


## Conceptual Role

This skill ingests source documents or extracted statement payloads and writes them back into the KB in the framework's canonical statement format.

## Framework Contribution

It contributes the disciplined acquisition layer that turns external mathematical material into reusable KB statements.

## How To Read Outputs

Read its outputs as canonicalized knowledge assets; the important property is structural fidelity to the source, not interpretive novelty.

## Overview

Create a normalized KB file for one problem space. Extract math statements from sources, preserve citations, and store each statement as a canonical record.

Read [references/kb-schema.md](references/kb-schema.md) before editing KB files.
Read [references/prompt-template.md](references/prompt-template.md) when running extraction prompts.
Read [references/script-usage.md](references/script-usage.md) before automating chunking and writeback.

## Workflow

1. Confirm the target KB file.
Create `KB/<problem-slug>.kb.md` from `KB/problem-template.kb.md` if missing.

2. Build the source index first.
Assign stable IDs (`src.001`, `src.002`, ...), keep locators precise (section, theorem number, page range).

3. Extract candidate statements from each source chunk.
Use `scripts/chunk_sources.py` to create source chunks from URLs/files (including PDFs when a PDF parser is installed).
Capture exact LaTeX, an informal paraphrase, dependencies, symbols, and confidence.

4. Normalize and deduplicate.
Merge equivalent statements, keep one canonical ID, and record alternates in `notes`.

5. Commit accepted statements.
Use `scripts/kb_writeback.py` to append normalized statement records into canonical/derived KB sections.
Write definitions, axioms, and high-confidence theorems under `# Canonical Statements`.
Place uncertain or inferred items in `# Derived Statements` with `status: tentative`.

6. Close with a consistency pass.
Check undefined symbols, broken dependencies, missing citations, and ID collisions.
Move unresolved items into `# Open Gaps`.

## Quality Gates

Enforce these checks before finalizing changes:

- Every statement has at least one `source_id` unless explicitly derived.
- Every symbol in `used_symbols` exists in `# Symbol Glossary`.
- Every `depends_on` ID exists in the same KB file.
- `confidence` is between `0.00` and `1.00`.
- `kind` is one of: `definition`, `axiom`, `theorem`, `lemma`, `corollary`, `conjecture`, `observation`.

## Bundled Scripts

- `scripts/chunk_sources.py`: chunk URL/file/PDF sources into JSONL records with source IDs and locators.
- `scripts/kb_writeback.py`: append normalized statement JSON records into a KB file and update `# Change Log`.

## Output Contract

When asked to summarize ingest work, report:

1. KB file path.
2. Number of sources indexed.
3. Number of statements added/updated by `kind`.
4. Number of unresolved gaps.
5. Highest-risk uncertainty (one sentence).

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `chunk_sources.py, kb_writeback.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: normalized statements, source IDs, explicit unknowns, parse failures, artifact paths, validation result, and next repair. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
