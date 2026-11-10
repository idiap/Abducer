<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# phyp

`phyp/` stores proof hypotheses generated from KB relational analysis.

## File Convention

- `<kb-slug>.proof-hypotheses.yaml`
- `<kb-slug>.hypotheses-evaluated.md`
- `<kb-slug>.hypotheses-reviewed.md`
- `<kb-slug>.hypotheses-evaluated.tex|pdf`
- `<kb-slug>.hypotheses-reviewed.tex|pdf`

Example:

- `phyp/p-vs-np.proof-hypotheses.yaml`
- `phyp/p-vs-np.hypotheses-evaluated.md`
- `phyp/p-vs-np.hypotheses-evaluated.tex`
- `phyp/p-vs-np.hypotheses-evaluated.pdf`

## Hypothesis Types

- `bridge-link`: conjectural support connection between two statement IDs.
- `intervention-focus`: high-priority abductive target statement.

## Lifecycle

1. Run `kb-proof-connector` to produce connection analysis.
2. Run `generate_phyp.py` to synthesize hypothesis records.
3. Validate hypotheses through `kb-abduce` + `kb-deduce` loop.
4. Run `kb-hypothesis-evaluator` for per-hypothesis verdict classification.
5. Run `kb-hypothesis-refutation-loop` for multi-round status convergence.
6. Promote successful hypotheses into KB `Derived Statements` as tentative conjectures.
7. Export `phyp/*.md` to `.tex`/`.pdf` using `skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py`.
