<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Evaluate a Hypothesis Set

```bash
skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --coherence-report artifacts/p-vs-np/coherence-report.json \
  --evidence-json artifacts/p-vs-np/round-evidence/round-1.json \
  --support-threshold 0.62 \
  --refute-threshold 0.62 \
  --output-json artifacts/p-vs-np/hypothesis-evaluation.json \
  --output-md artifacts/p-vs-np/hypothesis-evaluation.md \
  --output-phyp-md phyp/p-vs-np.hypotheses-evaluated.md \
  --output-phyp phyp/p-vs-np.hypotheses-evaluated.yaml
```

## Force Resolution (No Inconclusive Verdicts)

```bash
skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --force-resolution \
  --output-json artifacts/p-vs-np/hypothesis-evaluation-forced.json \
  --output-md artifacts/p-vs-np/hypothesis-evaluation-forced.md
```
