<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Analyze KB Graph and Export Reports

```bash
skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py \
  --kb KB/p-vs-np.kb.md \
  --include-status accepted \
  --include-status tentative \
  --top-k 20 \
  --min-similarity 0.12 \
  --max-connections 40 \
  --loop-rounds 3 \
  --output-json artifacts/p-vs-np/connection-analysis.json \
  --output-md artifacts/p-vs-np/connection-analysis.md
```

## Minimal Run

```bash
skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py \
  --kb KB/p-vs-np.kb.md
```

## Recommended Next Step

Run `kb-coherence-evaluator` on generated hypotheses, then feed `top_interventions` and `connection_candidates` into `kb-abduce`, and validate proposed links with `kb-deduce`.

## Generate Proof Hypotheses in `phyp/`

```bash
skills/discovery/kb-proof-connector/scripts/generate_phyp.py \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --kb KB/p-vs-np.kb.md \
  --output phyp/p-vs-np.proof-hypotheses.yaml \
  --top-links 20 \
  --top-interventions 12 \
  --top-conceptual 12
```
