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
skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py \
  --problem "P vs NP" \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --entrypoints artifacts/p-vs-np/entrypoints.json \
  --pathways artifacts/p-vs-np/entrypoint-pathways.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --output-json artifacts/p-vs-np/epistemic-hardness.json \
  --output-md artifacts/p-vs-np/epistemic-hardness.md
```
