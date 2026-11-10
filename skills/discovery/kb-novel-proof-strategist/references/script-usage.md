<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Strategy Design

```bash
skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py \
  --entrypoints artifacts/p-vs-np/entrypoints.json \
  --pathways artifacts/p-vs-np/entrypoint-pathways.json \
  --bridges artifacts/p-vs-np/bridge-plan.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --top-k 6 \
  --output-json artifacts/p-vs-np/proof-strategies.json \
  --output-md artifacts/p-vs-np/proof-strategies.md \
  --output-prompt artifacts/p-vs-np/novelty-maximizing-prompt.txt
```

## Integrated PvsNP Test

```bash
skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py
```

This integrated runner now executes:
1. `kb-epistemic-hardness`
2. `kb-concept-bridge-planner`
3. `kb-novel-proof-strategist`
4. `kb-hypothesis-evaluator`
5. `kb-hypothesis-refutation-loop`
6. `phyp Markdown -> LaTeX/PDF export`
