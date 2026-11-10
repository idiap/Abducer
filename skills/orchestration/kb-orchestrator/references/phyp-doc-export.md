<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# phyp Markdown Export

Use `export_phyp_docs.py` to compile Markdown files in `phyp/` into both LaTeX and PDF.

## Export All phyp Markdown Files (excluding README)

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  --phyp-dir phyp \
  --pattern "*.md" \
  --pdf-engine xelatex
```

## Include README.md

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  --phyp-dir phyp \
  --pattern "*.md" \
  --include-readme \
  --pdf-engine xelatex
```

Outputs are created next to each Markdown file:

- `<name>.tex`
- `<name>.pdf`
