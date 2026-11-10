<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Iterative Hypothesis Validation Loop

```bash
skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --rounds 3 \
  --start-support-threshold 0.66 \
  --start-refute-threshold 0.66 \
  --threshold-step 0.05 \
  --round-evidence-dir artifacts/p-vs-np/round-evidence \
  --output-json artifacts/p-vs-np/hypothesis-refutation-loop.json \
  --output-md artifacts/p-vs-np/hypothesis-refutation-loop.md \
  --output-phyp-md phyp/p-vs-np.hypotheses-reviewed.md \
  --output-phyp phyp/p-vs-np.hypotheses-reviewed.yaml
```

`--force-final-resolution` is disabled by default. Provide round evidence files
`round-1.json`, `round-2.json`, ... in `--round-evidence-dir` to drive real multi-round updates.

## Annealing Mode (Without New Evidence)

```bash
skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --rounds 4 \
  --anneal-without-new-evidence \
  --force-final-resolution \
  --output-json artifacts/p-vs-np/hypothesis-refutation-loop.conservative.json \
  --output-md artifacts/p-vs-np/hypothesis-refutation-loop.conservative.md \
  --output-phyp phyp/p-vs-np.hypotheses-reviewed.conservative.yaml
```
