# LaTeX paper build contract

## Required manuscript structure

The renderer accepts any LaTeX layout, but the bundled scaffold uses:

```text
main.tex
references.bib
sections/
  abstract.tex
  introduction.tex
  results.tex
  related_work.tex
  discussion.tex
  conclusion.tex
appendices/
  proof_details.tex
build/
```

## Build sequence

1. Run `lint_manuscript.py`.
2. Run `render_paper.py --strict`.
3. Inspect `build/build_report.json`.
4. Inspect the preview PNGs visually.
5. Correct source defects and rebuild until all gates pass.

`latexmk` manages repeated LaTeX and BibTeX passes. A project requiring Biber
also requires the `biber` executable; the renderer reports compilation failure
if the declared toolchain is unavailable.

## Submission artifacts

Retain `main.tex`, all included sources, `references.bib`, figures, custom
style files, the final PDF, and the build report. Include proof-certificate
data and its verifier when theorem-critical computations appear. Do not submit
temporary auxiliary files unless requested by the venue.

## Interpretation of checks

- Missing citation keys, missing labels, duplicate labels, TODO markers, and
  unreplaced template tokens are errors.
- Workflow language and overfull boxes are warnings that require review.
- Successful compilation does not certify mathematical correctness.
- Successful text extraction does not certify visual layout; inspect previews.
