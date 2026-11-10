---
name: ym-build-proof-appendix
description: Design and write self-contained proof appendices for mathematical-physics and Yang--Mills papers. Use when detailed lemmas, calculations, interval certificates, finite matrix constructions, or technical estimates should move out of the main narrative without hiding assumptions, weakening verifiability, or breaking theorem dependencies and cross-references.
---

# Build the Proof Appendix

## Decide what moves

Keep in the main text the theorem, conceptual mechanism, essential definitions, decisive estimate, proof architecture, and the part needed to assess novelty. Move repetitive estimates, long exact calculations, certificate formats, auxiliary regularity lemmas, exhaustive cases, and implementation details to appendices.

Never move a theorem hypothesis, convention, domain restriction, or logical gap merely to make the main text look cleaner.

## Construct the appendix graph

1. Read the theorem dependency graph from `ym-develop-paper-proofs`.
2. Topologically order appendix lemmas so that each proof uses only earlier definitions, earlier appendix results, main-text results, or explicit citations.
3. Assign stable labels to every appendix section, lemma, equation, table, and algorithm.
4. Replace “it is easy to see,” “standard,” and omitted calculations when they carry theorem-critical content.
5. State normalization, notation, and parameter domains at the point of use, while avoiding inconsistent redefinition.
6. Put computer-assisted proofs in a certificate appendix that specifies inputs, trusted kernel, rounding model, coverage, hashes, and independent verification.
7. Put reproducibility instructions after the mathematical certificate, not in place of it.

## Main-text integration

Each deferred proof must have a main-text proof sketch naming the mechanism and an exact appendix reference. Each appendix proof must begin by identifying the main result it supports. Verify that removing the appendix would leave a readable argument, while reading it restores full proof detail.

## Appendix audit

- No orphan lemma or unused calculation.
- No forward reference cycle.
- No new unannounced assumption.
- No notation collision with the main text.
- All equations and citations resolve after compilation.
- The appendix states whether each numerical datum is exact, interval-certified, or exploratory.
- Page length remains proportionate; move bulky raw data to a supplement.

## Output contract

Produce `appendix_map.md`, modular files under `appendices/`, an updated proof dependency graph, and a main-text-to-appendix cross-reference table. Hand the complete source tree to `ym-build-latex-paper` for strict compilation and rendered-PDF inspection.
