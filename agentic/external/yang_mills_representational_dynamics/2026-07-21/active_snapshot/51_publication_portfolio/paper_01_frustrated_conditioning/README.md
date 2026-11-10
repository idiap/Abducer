# Paper 01 — central-frustration obstruction

This directory is a self-contained blinded manuscript and reproducibility package for:

> **Central Frustration Obstructs Boundary-Uniform Local Control in Heat-Kernel Lattice Gauge Theory**

Strongest claim level: `C2`, a rigorous finite-lattice theorem. The paper does not construct continuum Yang–Mills theory or prove a mass gap.

## Main outputs

- `main.tex` and modular files under `sections/` and `appendices/`
- `references.bib`
- `build/main.pdf` — 21 pages
- `build/build_report.json` and `build/lint_report.json`
- `build/previews/` — first, middle, and last page renders
- `artifacts/` — theorem, proof, literature, novelty, appendix, venue, and frontier ledgers
- `supplement/` — exact standard-library incidence verifier, tests, and certificate
- `../paper_01_frustrated_conditioning_submission.zip` — source/PDF submission archive

## Reproduce the exact finite certificate

```bash
python3 supplement/verify_incidence.py \
  --output supplement/incidence_certificate.json
python3 -m unittest -v supplement/test_verify_incidence.py
```

Expected: five tests pass and the JSON field `all_checks_pass` is `true`.

## Lint and compile

The commands below use the exported manuscript-automation skill scripts:

```bash
python3 /root/.codex/skills/remote-skills/skill-6a5f170d60308191aeb5d829f71369af/scripts/lint_manuscript.py \
  main.tex --strict-narrative --json build/lint_report.json
python3 /root/.codex/skills/remote-skills/skill-6a5f170d60308191aeb5d829f71369af/scripts/render_paper.py \
  main.tex --strict
```

Direct fallback:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Final PDF SHA-256:

```text
a2f339a7bad9b02c5ec9c53973ac09006c530ffc7311effd39d3a10c4063812a
```

## Submission boundary

The source is blinded. Before external submission, the user must supply author identity, affiliation, ORCID, email, funding, and conflict declarations, and refresh the subscription-database novelty search.
