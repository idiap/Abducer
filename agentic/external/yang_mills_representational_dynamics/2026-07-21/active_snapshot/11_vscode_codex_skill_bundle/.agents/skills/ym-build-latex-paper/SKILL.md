---
name: ym-build-latex-paper
description: Scaffold, assemble, lint, compile, render, and verify modular LaTeX papers and PDF artifacts for Yang--Mills, mathematical physics, and philosophy of physics. Use when Codex must create a manuscript source tree, integrate sections and proof appendices, resolve BibTeX and cross-references, run latexmk, inspect PDF metadata and text, render preview pages, and emit a machine-readable build report.
---

# Build and Render the LaTeX Paper

## Create the source tree

Use `scripts/scaffold_paper.py` for a new manuscript. It creates modular front matter, main sections, appendices, and a BibTeX file from `assets/paper_template/` without overwriting an existing directory.

```bash
python3 scripts/scaffold_paper.py OUTPUT_DIR --title "Paper title" --author "Author"
```

Read `references/BUILD_CONTRACT.md` before assembling an existing paper.

## Assemble

1. Insert outputs from `ym-frame-paper-narrative` into the abstract, introduction, and conclusion.
2. Insert `ym-ground-paper-literature` outputs into related work and `references.bib`.
3. Insert theorem and proof fragments from `ym-develop-paper-proofs`.
4. Insert modular appendices from `ym-build-proof-appendix` after `\appendix`.
5. Keep package use minimal, notation centralized, labels stable, and all included files under the manuscript root.
6. Do not leave TODOs, placeholder tokens, workflow language, missing citations, or unresolved references.

## Lint and render

Run the source linter first:

```bash
python3 scripts/lint_manuscript.py MANUSCRIPT/main.tex --strict-narrative
```

Compile and validate with:

```bash
python3 scripts/render_paper.py MANUSCRIPT/main.tex --strict
```

The renderer runs `latexmk`, checks the log, inspects PDF metadata, extracts text, renders first/middle/last page previews with Poppler, and writes `build/build_report.json`. Use the `pdf` skill to inspect preview PNGs visually before delivery.

## Acceptance gates

- `latexmk` succeeds from a clean build directory.
- All citations and references resolve.
- PDF has nonzero pages, meaningful extracted text, and a stable SHA-256 hash.
- No TODO, template token, or missing bibliography key remains.
- Overfull boxes are reviewed and either fixed or explicitly accepted.
- First, middle, and last page previews show no clipping, broken glyphs, overlap, or unreadable figures/tables.
- Source, PDF, bibliography, build report, and certificate supplement are version-consistent.

## Output contract

Return the modular LaTeX tree, compiled PDF, preview PNGs, linter report, and `build_report.json`. Preserve compilation logs for diagnosis, but exclude auxiliary files from the submission archive unless the venue requires them.
