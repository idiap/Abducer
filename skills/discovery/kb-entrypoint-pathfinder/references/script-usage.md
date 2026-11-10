<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Build Pathways

```bash
skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py \
  --recommendations artifacts/p-vs-np/entrypoints.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --top-entrypoints 8 \
  --max-hypotheses-per-path 4 \
  --max-links-per-path 3 \
  --output-json artifacts/p-vs-np/entrypoint-pathways.json \
  --output-md artifacts/p-vs-np/entrypoint-pathways.md
```
