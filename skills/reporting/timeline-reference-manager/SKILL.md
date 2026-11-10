---
name: timeline-reference-manager
description: Manage references for timeline-derived paper drafts by curating cited literature, report artifacts, cycle evidence, and bibliography entries. Use when a paper workflow needs non-decorative references, consistent citation keys, provenance, and source limits from timeline and literature reports.
---

# Timeline Reference Manager

## Workflow

Build a reference spine:

1. Load literature references from the target literature report.
2. Add artifact references for timeline, strategy judge, contribution monitor, macro strategy, qualitative graph, and derivation packets.
3. Deduplicate by reference ID or URL.
4. Create bibliography keys and TeX bibliography entries.
5. State what each reference supports and what it does not support.

## Epistemic Discipline

References are evidence, not decoration. Cite only sources used in the paper argument. Label artifact citations separately from external literature.

## Output Contract

Return: cited references, artifact references, BibTeX or TeX bibliography block, support/limitation notes, epistemic status, and validation handoff.

## Failure/Demotion

Demote the bibliography if it cites unused sources, omits support roles, lacks URLs for literature entries, or uses sources to support claims beyond their limitations.

## Validation Handoff

The validator must confirm that all paper citation keys resolve to bibliography entries and that at least one artifact reference supports each major contribution.
