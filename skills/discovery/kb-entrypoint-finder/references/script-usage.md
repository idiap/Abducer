<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Rank Entry Points

```bash
skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py \
  --kb KB/p-vs-np.kb.md \
  --include-status accepted \
  --include-status tentative \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --top-k 20 \
  --output-json artifacts/p-vs-np/entrypoints.json \
  --output-md artifacts/p-vs-np/entrypoints.md
```

## Minimal Run

```bash
skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml
```
