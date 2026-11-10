<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Run Revision Loop

```bash
skills/evaluation/kb-revision-loop/scripts/revise_ontology.py \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.hypotheses-reviewed.yaml \
  --hypothesis-loop artifacts/p-vs-np/hypothesis-refutation-loop.json \
  --coherence-report artifacts/p-vs-np/coherence-report.json \
  --hardness artifacts/p-vs-np/epistemic-hardness.json \
  --output-json artifacts/p-vs-np/revision-loop.json \
  --output-md artifacts/p-vs-np/revision-loop.md
```

## Notes

- Intended to run after `kb-hypothesis-refutation-loop`.
- Use output priority program as next-cycle orchestration input.
