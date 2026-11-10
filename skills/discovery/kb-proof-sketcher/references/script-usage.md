
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
python3 skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py \
  --conjectures artifacts/<slug>/concept-gap-abstractions.json \
  --strategies artifacts/<slug>/proof-strategies.json \
  --bridges artifacts/<slug>/bridge-plan.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--kb KB/<problem>.kb.md] \
  [--analysis artifacts/<slug>/connection-analysis.json] \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--hardness artifacts/<slug>/epistemic-hardness.json] \
  [--top-k 6] \
  [--output-json artifacts/<slug>/proof-sketches.json] \
  [--output-md artifacts/<slug>/proof-sketches.md] \
  [--output-paper-md artifacts/<slug>/paper-style-argument.md]
```

