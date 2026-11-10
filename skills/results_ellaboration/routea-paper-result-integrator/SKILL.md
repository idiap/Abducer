---
name: routea-paper-result-integrator
description: Integrate validated Route A module results back into the SU(2) Wilson-block paper as theorem, proposition, lemma, certificate, or demotion text. Use after a Route A paper-attack skill produces a mathematical artifact and the manuscript must be updated without leaking workflow, pipeline, TODO, or process-management language.
---

# Route A Paper Result Integrator

## Purpose

This skill converts a validated Route A module artifact into paper-native scientific prose. It is used only after a mathematical object has been produced or demoted: edge-list construction, normalization certificate, coefficient theorem, margin bound, endpoint estimate, continuum handoff, or spectral handoff.

## Paper-Native Result Forms

Use the smallest honest form supported by the artifact:

- **Definition** for new paths, cutoff regimes, normalizations, endpoint boxes, or source domains.
- **Lemma** for support, footprint, reflection, congruence, coefficient identity, null-channel identity, or stencil bounds.
- **Proposition** for same-theory normalization, finite certificate, endpoint estimator, or lower-bound protocol.
- **Theorem** only for a complete construction or estimate with all hypotheses stated.
- **Remark/Open module** when the artifact demotes a route or clarifies an obstruction.

## Integration Procedure

1. Read the target module and the validated artifact.
2. Determine the honest result form and exact insertion point in the paper.
3. State definitions before claims.
4. State assumptions and validity regime in the theorem/proposition statement.
5. Use proof text only for what the artifact establishes.
6. Update abstract, introduction, table, and conclusion only if the paper's claim actually changes.
7. Compile the TeX and audit references, labels, and claim boundary.

## Forbidden Paper Language

Do not insert any of these into the manuscript body, theorem statements, proof prose, abstract, conclusion, or captions:

- pipeline
- workflow
- TODO or todo
- result-elaboration
- implementation packet
- agent
- skill
- queue

These words may appear in external planning files, but never in the paper narrative.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: result form, insertion point, manuscript patch, changed claim summary, unchanged non-claims, forbidden-language audit, TeX compile status, and unresolved proof obligations.

## Failure/Demotion

Demote the integration if the artifact is only a plan, if the patch describes work management instead of mathematics, if the conclusion becomes stronger than the theorem, or if the patch changes non-targeted sections without a claim-level reason.
