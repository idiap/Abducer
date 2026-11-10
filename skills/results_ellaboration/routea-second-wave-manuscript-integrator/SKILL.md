---
name: routea-second-wave-manuscript-integrator
description: Integrate second-wave Route A open-point results into the SU(2) Wilson-block manuscript. Use when focused result artifacts from collar redesign, finite margins, endpoint derivation, or endpoint error certification must update the paper without process language or overclaiming.
---

# Route A Second-Wave Manuscript Integrator

## Purpose

Convert second-wave result artifacts into clean paper revisions. This skill decides whether a result changes the abstract, introduction, status table, open-module section, appendix checklist, conclusion, or only a local appendix.

## Input Result Schema

Each result must state:

- source artifact;
- result type: theorem, proposition, lemma, finite certificate, obstruction, appendix calculation, or no-change;
- TeX block;
- assumptions and validity regime;
- affected labels/sections;
- claim-change flag;
- non-claims.

## Deterministic Support

Use `integrate_routea_second_wave_results.py` to insert validated TeX blocks, scan forbidden paper language, compile, and emit a revision manifest.

## Integration Rules

- Strengthen the abstract only for theorem-level or central finite-certificate changes.
- Update the status table when a module is resolved, sharpened, or demoted.
- Update the checklist when a checklist item is satisfied or made impossible by an obstruction.
- Keep continuum and mass-gap non-claims unless a same-theory transfer theorem exists.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: integrated TeX path, PDF path if compiled, revision manifest, changed claims, unchanged non-claims, forbidden-language audit, compile status, and next manuscript action.

## Failure/Demotion

Demote if the TeX block contains planning language, if a claim is stronger than the source artifact, or if references/labels fail after compilation.
