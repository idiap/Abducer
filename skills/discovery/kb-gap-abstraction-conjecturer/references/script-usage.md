
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Script Usage

```bash
python3 skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py \
  --analysis artifacts/<slug>/connection-analysis.json \
  --entrypoints artifacts/<slug>/entrypoints.json \
  --pathways artifacts/<slug>/entrypoint-pathways.json \
  --bridges artifacts/<slug>/bridge-plan.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--hardness artifacts/<slug>/epistemic-hardness.json] \
  [--top-bridges 12] \
  [--max-conjectures-per-bridge 3] \
  [--output-json artifacts/<slug>/concept-gap-abstractions.json] \
  [--output-md artifacts/<slug>/concept-gap-abstractions.md]
```

