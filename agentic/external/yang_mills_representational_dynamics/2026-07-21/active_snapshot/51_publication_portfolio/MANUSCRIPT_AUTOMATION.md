# Manuscript automation workflow

This layer converts each publication plan into a reproducible LaTeX manuscript
and rendered PDF. The four paper-specific skills remain scientific
orchestrators; five shared skills own distinct manuscript functions.

## Skill graph

```text
paper-specific theorem and scope
  |
  +--> ym-develop-paper-proofs
  |      theorem contract, proof DAG, obligations, countermodels, certificates
  |
  +--> ym-ground-paper-literature
  |      search ledger, claim-source matrix, closest results, BibTeX
  |
  +--> ym-frame-paper-narrative
  |      motivation, abstract, introduction, contribution, conclusion
  |
  +--> ym-build-proof-appendix
  |      topologically ordered details, certificates, cross-reference map
  |
  +--> ym-build-latex-paper
         modular source, lint report, PDF, previews, build report
  |
  +--> ym-audit-frontier
         final Yang--Mills claim and quantifier audit
```

Proof development precedes final narrative framing because the abstract and
introduction must describe results that actually close. Literature grounding
can begin earlier, but its novelty matrix must be refreshed after the theorem
is frozen. Appendix construction follows the proof dependency graph rather
than manuscript chronology.

## Shared skills

### `ym-frame-paper-narrative`

Owns motivation, title, abstract, contribution statement, introduction, and
conclusion. It enforces the chain from phenomenon through technical bottleneck
to theorem and consequence. It removes stage numbers, pipeline language,
revision history, and unsupported gap claims.

Expected artifacts:

- `narrative_contract.md`
- `abstract.tex`
- `introduction.tex`
- `conclusion.tex`
- claim-to-section map

### `ym-ground-paper-literature`

Owns current primary-source searching, citation-chain review, novelty
classification, related work, and bibliography quality. It distinguishes
theorem, method, constant/certification, application, conceptual, and
expository novelty.

Expected artifacts:

- `literature_search_ledger.md`
- `claim_source_matrix.md`
- `closest_results.md`
- `citation_graph.json`
- `related_work.tex`
- `references.bib`

### `ym-develop-paper-proofs`

Owns theorem freezing, proof search, dependency closure, hostile cases,
uniformity, numerical rigor, and proof status. It never treats test success or
ordinary floating-point output as a proof.

Expected artifacts:

- `theorem_contract.tex`
- `proof_dependency_graph.json`
- `proof_obligation_ledger.md`
- `countermodel_ledger.md`
- `certificate_registry.json`
- theorem and lemma fragments

### `ym-build-proof-appendix`

Owns the boundary between the readable main argument and complete proof
details. It topologically orders deferred lemmas and prevents assumptions,
normalizations, or gaps from being hidden in appendices.

Expected artifacts:

- `appendix_map.md`
- modular `appendices/*.tex`
- main-text-to-appendix cross-reference table
- updated proof DAG

### `ym-build-latex-paper`

Owns deterministic scaffolding, manuscript linting, `latexmk` compilation,
PDF metadata and text validation, preview rendering, and build reporting. It
contains three scripts and a modular article template.

Create a source tree:

```bash
python3 scripts/scaffold_paper.py OUTPUT_DIR \
  --title "Paper title" --author "Author"
```

Lint it:

```bash
python3 scripts/lint_manuscript.py OUTPUT_DIR/main.tex --strict-narrative
```

Compile and verify it:

```bash
python3 scripts/render_paper.py OUTPUT_DIR/main.tex --strict
```

The renderer:

1. blocks TODOs, missing BibTeX keys, missing/duplicate labels, and unresolved
   template tokens;
2. optionally blocks stage and workflow narration;
3. runs `latexmk` with fatal-error handling;
4. checks the final log for unresolved citations and references;
5. validates page count and metadata with `pdfinfo`;
6. extracts and checks text with `pdftotext`;
7. renders first, middle, and last pages with `pdftoppm`;
8. records the PDF hash, byte size, pages, checks, and preview paths in
   `build/build_report.json`.

The rendered previews must then be inspected visually using the PDF workflow.
A successful build does not certify mathematical correctness.

## Paper-specific entry points

- P1: `ym-draft-frustration-obstruction`
- P2: `ym-draft-finite-block-certificate`
- P3: `ym-draft-representational-dynamics`
- P4: `ym-draft-heat-kernel-enclosures`

Each orchestrator now invokes the five shared skills in an order adapted to
its scientific contribution and finishes with `ym-audit-frontier`.

## Acceptance contract for every paper

- The motivation terminates in the question answered by the paper.
- Every novelty sentence is grounded in the closest-result matrix.
- Every abstract claim maps to a theorem, formal argument, or labeled
  interpretation.
- Proof details are complete in the main text plus appendix.
- The LaTeX tree compiles cleanly from a reproducible environment.
- Citations and cross-references resolve.
- The PDF passes metadata, text, and visual inspection.
- The final Yang--Mills scope audit agrees with the title, abstract, and
  conclusion.
