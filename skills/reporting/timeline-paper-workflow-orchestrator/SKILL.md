---
name: timeline-paper-workflow-orchestrator
description: Orchestrate an independent timeline-report-to-paper workflow that parses Abducer discovery timeline artifacts and assembles a paper-style narrative, TeX source, PDF, evidence packet, and validation handoff. Use when timeline report elements should become a standalone scientific paper draft independent from the main discovery loop.
---

# Timeline Paper Workflow Orchestrator

## Workflow

Coordinate the paper agents in this order:

1. Invoke `timeline-report-evidence-ingestor` to parse the full timeline report into source-backed evidence units, argument roles, and report-family coverage.
2. Invoke `timeline-paper-argument-architect` to choose the paper mode, thesis, contribution matrix, non-claims, section responsibilities, and narrative budget.
3. Invoke `timeline-narrative-coherence-guard` to verify the bounded paper subgoal and demote details outside the paper spine.
4. Invoke `finite-theorem-section-packager` when the paper hinges on a bounded finite theorem, obstruction criterion, or local proof packet.
5. Invoke `endpoint-worked-calculation-packager` when the paper needs the first explicit finite calculation, table, spectrum, sign test, or reproducibility witness.
6. Invoke `prior-art-positioning-packager` and `timeline-reference-manager` before novelty language is allowed into the contribution section.
7. Invoke `timeline-problem-space-narrator`, `timeline-contribution-stater`, and `timeline-contribution-explainer` against the blueprint, not raw tabs.
8. Invoke `timeline-failed-route-interpreter` to compress route failures into scientific learning.
9. Invoke `timeline-formal-physics-deriver` to write the formal derivation section with definitions, assumptions, propositions, equations, validity regimes, and proof-obligation boundaries.
10. Invoke `timeline-organizing-diagram-builder` to build diagrams from blueprint nodes and edges.
11. Invoke `timeline-paper-section-synthesizer` to produce main-body and appendix sections from assigned source units.
12. Invoke `timeline-claim-boundary-auditor` and `timeline-paper-cross-section-reconciler` to demote overclaims, duplicate definitions, dangling references, and narrative-budget violations.
13. Assemble TeX and render PDF through the standalone timeline-paper builder.

## Epistemic Discipline

Preserve epistemic status in every section: proof-obligation, evidence-backed, conjectural, validation-needed, blocked, promoted, or demoted. Cite source artifacts, timeline cycle IDs, report paths, literature references, and explicit unknowns.

Do not let paper prose make the discovery stronger than the report evidence. The paper is a structured scientific argument draft, not a claim that the main theorem is solved.

Do not let the paper body become an infinite exploration digest. A timeline detail belongs in the paper body only when it strengthens the theorem, worked example, transfer certificate, prior-art boundary, or smallest honest contribution claim. Otherwise move it to appendix/future work or quarantine it.

## Output Contract

Return the produced artifact paths, section map, invoked skills, finite theorem section status, worked calculation status, prior-art positioning status, source artifacts, epistemic status, validation handoff, unresolved obligations, and demotion triggers.

## Failure/Demotion

Demote the draft if it cannot state a contribution, cites no evidence, uses decorative references, lacks a formal derivation, turns a local obstruction into an overclaimed proof, or keeps adding exploration details without improving the locked paper subgoal.

## Validation Handoff

Run the standalone workflow runner and validators after generation:

```bash
.venv-pmp/bin/python agentic/scripts/run_timeline_paper_workflow.py --strict
```

The validation handoff must find interpretation, blueprint, sections, formal derivation, diagrams, TeX, PDF, claim boundaries, and report-family coverage. Keep this workflow independent from the main discovery loop unless the user explicitly asks to wire it into marathon execution.
