<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Evaluate Coherence and Explanatory Power

```bash
skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --output-json artifacts/p-vs-np/coherence-report.json \
  --output-md artifacts/p-vs-np/coherence-report.md
```

## Notes

- Run after `kb-proof-connector` and `generate_phyp`.
- Feed output into entrypoint, bridge-planner, strategist, evaluator, and refutation-loop stages.
