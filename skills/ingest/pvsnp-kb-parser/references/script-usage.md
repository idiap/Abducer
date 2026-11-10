<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Script Usage

## Parse Report to Statements JSON

```bash
skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input inputs/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  --source-id src.001
```

## Parse and Write into PvsNP KB

```bash
skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input inputs/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  --source-id src.001 \
  --kb KB/p-vs-np.kb.md \
  --section-policy status \
  --change-note "Parsed deep-research-report.md into PvsNP KB"
```

## Dry-Run Writeback

```bash
skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input inputs/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  --source-id src.001 \
  --kb KB/p-vs-np.kb.md \
  --dry-run
```

If `--kb` is missing, the parser initializes it from `KB/problem-template.kb.md` unless `--init-kb-from-template \"\"` is passed.
