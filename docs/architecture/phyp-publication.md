<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# phyp Publication

This document defines the publication layer for proof hypotheses under `phyp/`.

## Purpose

The raw YAML files in `phyp/` are machine-oriented. The publication layer adds:

- readable Markdown mirrors for evaluation and review outputs,
- standalone LaTeX documents,
- compiled PDF documents for sharing, review, and archival.

## Produced Files

For a KB slug `<slug>`, the publication outputs are:

- `phyp/<slug>.proof-hypotheses.yaml`
- `phyp/<slug>.hypotheses-evaluated.md`
- `phyp/<slug>.hypotheses-evaluated.tex`
- `phyp/<slug>.hypotheses-evaluated.pdf`
- `phyp/<slug>.hypotheses-reviewed.md`
- `phyp/<slug>.hypotheses-reviewed.tex`
- `phyp/<slug>.hypotheses-reviewed.pdf`
- `phyp/<slug>.hypotheses-reviewed.yaml`

## Where Files Are Produced

### Hypothesis Evaluation

`skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py` can write:

- JSON report in `artifacts/<slug>/`
- Markdown report in `artifacts/<slug>/`
- Markdown mirror in `phyp/` via `--output-phyp-md`
- updated YAML in `phyp/` via `--output-phyp`

Typical mirror path:

- `phyp/<slug>.hypotheses-evaluated.md`

### Hypothesis Refutation Loop

`skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py` can write:

- JSON report in `artifacts/<slug>/`
- Markdown report in `artifacts/<slug>/`
- Markdown mirror in `phyp/` via `--output-phyp-md`
- reviewed YAML in `phyp/` via `--output-phyp`

Typical mirror path:

- `phyp/<slug>.hypotheses-reviewed.md`

### TeX and PDF Export

`skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py` scans Markdown files in `phyp/` and emits:

- `<name>.tex`
- `<name>.pdf`

It uses:

- `pandoc`
- a TeX engine such as `xelatex` or `pdflatex`

## Default Pipeline Behavior

`skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py` exports `phyp/*.md` by default after an orchestrated run.

Relevant flags:

- `--export-phyp-docs | --no-export-phyp-docs`
- `--phyp-doc-pattern "*.md"`
- `--phyp-pdf-engine xelatex`

`skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py` also runs the export stage.

## Standalone Export Command

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  --phyp-dir phyp \
  --pattern "*.md" \
  --pdf-engine xelatex
```

To also export `phyp/README.md`:

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  --phyp-dir phyp \
  --pattern "*.md" \
  --include-readme \
  --pdf-engine xelatex
```

## Title and Naming Policy

The exporter derives a document title from the Markdown filename by:

- removing the extension,
- replacing `_` and `-` with spaces,
- capitalizing tokens.

Example:

- `p-vs-np.hypotheses-reviewed.md`
- title: `P Vs Np.hypotheses Reviewed`

This is acceptable for publication, but not mathematically polished. If stricter titling is needed, the next improvement is explicit metadata injection per file.

## Operational Notes

- Export is non-destructive for YAML/Markdown sources.
- Output files are written next to the source Markdown files.
- `README.md` is excluded by default.
- If no Markdown files match the pattern, the exporter exits successfully.

## Reasoning Logs

Exporter runs write logs under:

- `artifacts/reasoning-logs/phyp-doc-exporter/`

These logs include:

- input arguments,
- matched file count,
- declared `.tex` and `.pdf` outputs.
