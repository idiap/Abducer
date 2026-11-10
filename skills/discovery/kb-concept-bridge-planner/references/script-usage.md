<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

```bash
skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --entrypoints artifacts/p-vs-np/entrypoints.json \
  --pathways artifacts/p-vs-np/entrypoint-pathways.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --top-k 20 \
  --output-json artifacts/p-vs-np/bridge-plan.json \
  --output-md artifacts/p-vs-np/bridge-plan.md
```
