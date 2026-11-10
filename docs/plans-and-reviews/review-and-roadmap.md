<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Critical Review and Roadmap

This document captures the recent critical review findings, implemented fixes, and next improvement opportunities.

## Implemented Improvements

## 1) Hypothesis Semantics and Loop Safety

Implemented:

- provisional verdicts now map to provisional statuses instead of hard resolved states,
- hard resolved statuses remain only `supported|refuted`,
- evidence-aware scoring added to evaluator (`deduce_class`, `abduce_residual_delta`, `contradiction`, `experimental_success`, `falsified`),
- contradiction detection changed to token-based negation signal,
- refutation loop defaults are conservative:
  - no forced final resolution by default,
  - stops after round 1 when there is no new evidence and annealing is disabled,
  - explicit round evidence support via `--round-evidence-dir`.

## 2) Parser Dry-Run Correctness

Implemented:

- `pvsnp-kb-parser` no longer mutates source index in `--dry-run` mode.

## 3) Status Filtering in Graph and Entrypoint Stages

Implemented:

- connector accepts repeatable `--include-status` and filters statements before graph analysis,
- entrypoint finder accepts `--include-status` and filters KB statements before ranking,
- reports expose filtered counts and included statuses.

## 4) Strategy Stage Uses Hypothesis Status

Implemented:

- strategist indexes phyp statuses and modulates strength:
  - supported boosts,
  - refuted penalizes,
  - provisional downgraded,
- strategy outputs include `hypothesis_status_summary`.

## 5) Deterministic Orchestration Script

Implemented:

- executable orchestrator script with intent routing and artifact defaults,
- integrated pipeline now includes hypothesis evaluation and refutation-loop stages.

## 6) Interoperability Contracts and Tests

Implemented:

- shared contract validators in `skills/common/contracts.py`,
- script integration of contract checks,
- regression tests for:
  - hypothesis provisional semantics,
  - connector status filtering,
  - parser dry-run non-mutation.

## 7) phyp Publication Outputs

Implemented:

- hypothesis evaluator/loop can mirror Markdown outputs directly into `phyp/`,
- orchestrator can auto-export `phyp/*.md` into `.tex` and `.pdf`,
- integrated P vs NP runner now includes phyp document export stage.

## 8) Coherentist Model and Revision Loops

Implemented:

- added `kb-coherence-evaluator` with typed coherence graph (`supports`, `attacks`, `explains`, `reframes`, `blocks`),
- added global coherence profile and per-hypothesis explanatory/coherence signals,
- upgraded evaluator/loop to consume coherence signals and apply belief-revision actions,
- expanded hypothesis language with conceptual-discovery kinds,
- upgraded connector with semantic features and concept graph output,
- added anti-barrier program generation in hardness stage,
- added `kb-revision-loop` and integrated it into `abductive-loop` and `pipeline` orchestrator intents,
- upgraded strategist with concept-fertility scoring.

## 9) Human-Readable Discovery Interpretation Reports

Implemented:

- added `generate_interpretation_reports.py` to synthesize stage artifacts into:
  - `reasoning-process-report.md` (stage-by-stage explanation),
  - `discovery-interpretation-report.md` (plain-language discovery narrative and next actions),
- integrated report generation into orchestrator `pipeline` and `abductive-loop` runs.

## Current Risks and Improvement Opportunities

## 1) Prompt-Driven Skill Execution Gap

Observation:

- `kb-abduce`, `kb-deduce`, `kb-explain`, `kb-induce` are prompt contracts, not deterministic scripts.

Opportunity:

- add executable wrappers and machine-readable outputs for these skills to close the deterministic loop.

## 2) Evidence Production Pipeline

Observation:

- evaluator/loop consume structured evidence, but evidence generation is manual.

Opportunity:

- add a dedicated evidence compiler that converts abduce/deduce run artifacts into `round-<n>.json` automatically.

## 3) KB Dependency Sparsity

Observation:

- sparse `depends_on` links reduce graph reliability and intervention quality.

Opportunity:

- add a dependency-suggestion skill and KB lint checks for unresolved references.

## 4) Statistical Calibration

Observation:

- thresholds are static.

Opportunity:

- fit calibration profiles per domain/problem family and expose profiles via CLI.

## 5) Benchmarking and Evaluation

Observation:

- current tests verify contracts and key regressions, not end-to-end quality metrics.

Opportunity:

- add benchmark fixtures for known theorem corpora with expected pathway/hypothesis ranking behavior.

## 6) Coherentist Calibration and Evaluation

Observation:

- coherentist/explanatory scoring is now implemented, but weights and thresholds are heuristic.

Opportunity:

- calibrate coherence and explanatory-power weights against benchmark fixtures,
- evaluate false-positive/false-negative rates for coherence-based demotions,
- expose domain-specific scoring profiles via CLI.

Next steps:

- Stage 1: create benchmark fixtures with expected retention/demotion outcomes.
- Stage 2: tune profile weights and thresholds (`min_coherence_keep`, severe-negative cutoff).
- Stage 3: add profile presets (for example `complexity-theory`, `algebra`, `combinatorics`).

Literature anchors:

- Thagard, P. (1989). *Explanatory Coherence*. Behavioral and Brain Sciences. https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/explanatory-coherence/60D68F7E30D3A8E9FD4D63C87CE1233A
- Thagard, P., and Verbeurgt, K. (1998). *Coherence as Constraint Satisfaction*. Cognitive Science. https://watarts.uwaterloo.ca/~pthagard/Articles/Pages/Cohere.Constrain.html
- Schupbach, J. N., and Sprenger, J. (2011). *The Logic of Explanatory Power*. Philosophy of Science. https://doi.org/10.1086/658111
- Cohen, A. (2015). *On the Schupbach-Sprenger Measures of Explanatory Power*. Philosophy of Science. https://doi.org/10.1086/682914
- Shogenji, T. (1999). *Is Coherence Truth-Conducive?* Analysis. https://doi.org/10.1093/analys/59.4.338
- Fitelson, B. (2003). *A Probabilistic Theory of Coherence*. Analysis. https://doi.org/10.1093/analys/63.3.194
- Bovens, L., and Hartmann, S. (2003). *Bayesian Epistemology* (coherence analysis and limits of single-measure approaches). https://global.oup.com/academic/product/bayesian-epistemology-9780199270625
