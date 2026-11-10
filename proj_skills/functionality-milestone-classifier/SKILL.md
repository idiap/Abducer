---
name: functionality-milestone-classifier
description: Classify Abducer Git changes into repository-evolution themes. Use when turning commit subjects and changed paths into an intelligible timeline without treating commits as proof that functionality worked.
---

# Functionality Milestone Classifier

Use this after `$git-history-evolution-miner` and before report assembly.

## Inputs

- chronological commit packets and changed paths
- current scientific and project-support skill inventories
- verification or release evidence when available
- [functionality-classification.md](../project-evolution-timeline-reporter/references/functionality-classification.md)

## Procedure

1. Classify changes into Abducer themes: source intake, mathematical discovery/proof, orchestration, evaluation, reporting, project support, documentation, and test infrastructure.
2. Select milestones for a new theme, a material architectural change, or a verified release boundary—not merely for persuasive commit wording.
3. Label each claim as `observed-change`, `inferred-purpose`, or `verified-behavior` and cite verification only when it exists.
4. Keep the full commit list separate from the curated milestone narrative.

## Handoff

Return category counts, selected milestones, per-commit categories, evidence posture, and a one-sentence selection rationale. Never describe Git history alone as functionality proof.
