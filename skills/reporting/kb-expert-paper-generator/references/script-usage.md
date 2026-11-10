
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
python3 skills/reporting/kb-expert-paper-generator/scripts/generate_expert_paper.py \
  --kb KB/<problem>.kb.md \
  [--artifacts-dir artifacts/<kb-ref>] \
  [--phyp phyp/<kb-ref>.proof-hypotheses.yaml] \
  [--top-k 8] \
  [--min-score 0.52] \
  [--output-json artifacts/<kb-ref>/expert-hypothesis-paper.json] \
  [--output-md artifacts/<kb-ref>/expert-hypothesis-paper.md] \
  [--output-tex artifacts/<kb-ref>/expert-hypothesis-paper.tex]
```

Default behavior:

- resolves canonical `artifacts/<kb-ref>/` from the KB reference name;
- loads final-stage artifacts when present;
- computes detailed per-hypothesis potential/risk decomposition;
- emits machine-readable and paper-style outputs.

