
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Script Usage

Generate the current macro-proof state report for a problem workspace:

```text
python skills/reporting/kb-macro-proof-paper-writer/scripts/generate_macro_proof_state_report.py --kb kb/p-vs-np.kb.md --artifacts-dir artifacts/p-vs-np
```

Generate the expert-facing macro-strategy report answering what is still missing for completion:

```text
python skills/reporting/kb-macro-proof-paper-writer/scripts/generate_macro_strategy_report.py --kb kb/p-vs-np.kb.md --artifacts-dir artifacts/p-vs-np
```

Optional flags:

```text
  [--preferred-engine auto|xelatex|pdflatex|lualatex]
  [--no-pdf]
```

