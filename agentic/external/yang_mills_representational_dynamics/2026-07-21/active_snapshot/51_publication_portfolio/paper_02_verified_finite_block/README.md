# Paper 02 — exact quotient--fiber certificate

This directory is a self-contained blinded manuscript and reproducibility
package for:

> **An Exact Quotient--Fiber Certificate for One Local Marginalization in
> Four-Dimensional \(SU(2)\) Heat-Kernel Lattice Gauge Theory**

Strongest claim level: C2, a rigorous restricted finite-block theorem. The
paper does not control the full interacting chart complement, repeat an RG
step, construct continuum Yang--Mills theory, or prove a mass gap.

## Main outputs

- main.tex, modular sections, and seven proof appendices
- references.bib
- build/main.pdf — 18 pages
- build/build_report.json and build/lint_report.json
- build/previews — visually checked first, middle, and last pages
- artifacts — theorem, proof, literature, novelty, venue, and frontier files
- supplement — two exact standard-library verifiers, tests, and JSON certificates
- ../paper_02_verified_finite_block_submission.zip — version-locked archive

## Reproduce the certificates

    python3 supplement/verify_finite_block.py \
      --output supplement/finite_block_certificate.json
    python3 supplement/verify_independent.py \
      --output supplement/independent_certificate.json
    python3 -m unittest -v supplement/test_verify_finite_block.py

Expected: eleven tests pass and both JSON files report
all_checks_pass as true.

## Lint and compile

    python3 /root/.codex/skills/remote-skills/skill-6a5f170d60308191aeb5d829f71369af/scripts/lint_manuscript.py \
      main.tex --strict-narrative --json build/lint_report.json
    python3 /root/.codex/skills/remote-skills/skill-6a5f170d60308191aeb5d829f71369af/scripts/render_paper.py \
      main.tex --strict

PDF SHA-256:

    c3461649a17b891cfb1c024564017f38e624b6375459a4a8c2dda7f133075a09

## Submission boundary

Before external submission, replace the blinded author, add affiliation,
ORCID, email, funding, and conflict declarations, and refresh the
subscription-database novelty search. No external submission has been made.
