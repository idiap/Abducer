---
name: finite-theorem-section-packager
description: Package a discovered finite theorem or obstruction criterion into a self-contained paper section. Use when a result needs definitions, hypotheses, theorem statement, proof skeleton, validity regime, and proof-obligation boundaries rather than further discovery.
---

# Finite Theorem Section Packager

## Workflow

1. Name the finite mathematical object and the ambient category where it lives.
2. State every hypothesis before the theorem, including normalization, quotient, topology, and remainder conditions.
3. Write the theorem as a local result independent of the main open problem.
4. Give a proof skeleton with lemmas, reductions, and where each assumption is used.
5. State what the theorem proves locally and what it does not prove globally.
6. Produce a checklist of missing details needed before publication.

## Output Contract

Return: section title, definitions, hypotheses, theorem statement, proof skeleton, local conclusion, non-claims, validation checklist, and next edit.

## Epistemic Discipline

Treat the theorem as a local contribution until every transfer premise is proved. Mark epistemic status explicitly as proof-obligation, evidence-backed, conjectural, blocked, promoted, or demoted. Cite source artifacts, artifact paths, cycle IDs, KB IDs when available, and explicit unknowns before turning any discovery note into theorem prose. Every claim must name the finite mathematical object it acts on, the allowed transformations, and the exact conclusion.

## Validation Handoff

Hand off to theorem/proof validators by providing a checklist that includes definition completeness, hypothesis use, proof-gap localization, counterexample search, and boundary comparison against the global target. The section is publication-ready only when a reader can verify the theorem without reading the discovery timeline.

## Failure/Demotion

Demote the section if it hides a main-theorem assumption, uses undefined objects, lacks a proof route, or presents a local finite result as a global theorem.
