---
name: ym-develop-paper-proofs
description: Develop, stress-test, and close theorem proofs for Yang--Mills and mathematical-physics papers. Use to freeze theorem contracts, expose quantifiers, construct proof-dependency graphs, select proof mechanisms, falsify candidate lemmas, certify numerical steps, distinguish conditional from established results, and prepare a proof package for the main text and appendix.
---

# Develop the Paper Proofs

## Freeze before proving

Write the theorem with every object, hypothesis, domain, cutoff, volume, boundary condition, parameter range, observable class, and limit order explicit. Assign each conclusion a claim level and define what would falsify it.

Build a dependency graph whose leaves are definitions, cited theorems with checked hypotheses, exact finite computations, or separately certified numerical bounds. A test suite is evidence about code, not a proof leaf.

## Proof workflow

1. Normalize the theorem into atomic conclusions.
2. Identify invariants, coercive quantities, compactness inputs, probabilistic comparisons, or spectral mechanisms that could imply each conclusion.
3. Generate at least one hostile boundary case or countermodel for every nontrivial intermediate lemma.
4. Prove structural lemmas symbolically before inserting constants.
5. Track uniformity and parameter dependence through every inequality.
6. Replace sampled extrema and ordinary floating linear algebra by analytic, exact, rational, or interval-certified bounds when theorem-critical.
7. Check every imported theorem's normalization and hypotheses.
8. Record failed proof routes when they constrain the theorem, but remove workflow narration from the paper.
9. Reassemble the dependencies and verify that no conclusion is used upstream of its proof.

## Proof-status language

Use only: `proved`, `proved with certified computation`, `conditional`, `computational calibration`, `counterexample`, `conjecture`, or `open`. Do not let “verified by tests” replace a theorem status.

For Yang--Mills work, audit gauge invariance, locality, positivity, observable completeness, physical units, boundary uniformity, volume/cutoff limits, and any spectral transfer. A finite-block coercivity constant is not a physical mass.

## Main-text handoff

For each major theorem, provide:

- a one-paragraph proof idea;
- the indispensable mechanism or estimate;
- the dependency list;
- the full proof or an exact appendix pointer;
- a statement of where each hypothesis is used.

## Output contract

Produce `theorem_contract.tex`, `proof_dependency_graph.json`, `proof_obligation_ledger.md`, `countermodel_ledger.md`, `certificate_registry.json`, and theorem/lemma LaTeX fragments. Mark which details belong in the main text and which transfer to `ym-build-proof-appendix`. Finish with `ym-audit-frontier`.
