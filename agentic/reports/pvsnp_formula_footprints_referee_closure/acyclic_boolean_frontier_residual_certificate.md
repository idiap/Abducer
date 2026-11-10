<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Acyclic Boolean Frontier Residual Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:acyclic-boolean-frontier-residual`
- Criteria affected: `C5`, `C7`, `C10`, `C11`
- Result role: `interface_variant_boundary`

## Purpose

This packet strengthens the semantic-frontier route beyond pure OR frontiers.
The earlier OR-tree and OR-DAG theorems solve a collapsed monotone OR
self-reduction frontier exactly.  This theorem states the corresponding
general residual-completion principle for any exposed finite acyclic Boolean
frontier circuit: support-locality is ordinary Boolean certificate complexity
for the induced frontier function.

The theorem is intentionally conditional on the frontier circuit being exposed
and acyclic.  The visible-adaptive packet handles exposed adaptive decision
trees.  This theorem is not a theorem for hidden SAT proof influence, learned
clauses, cyclic dependencies, or arbitrary semantic proof systems.

## Statement

Let \(C\) be a finite acyclic Boolean circuit whose input/frontier coordinates
are \(Q\) and whose output/root coordinate is \(r\).  Let \(F_C:\{0,1\}^Q\to
\{0,1\}\) be the Boolean function computed by \(C\).  The residual frontier
relation is
\[
  R_C=\{(y_r,z): y_r=F_C(z)\}.
\]
For a satisfying tuple \(a\in R_C\), a support set
\(S\subseteq \{r\}\cup Q\) is support-local for \(R_C\) at \(a\) iff:

1. \(r\in S\); and
2. \(S\cap Q\) is a standard certificate for \(F_C(z)=a_r\) at \(a|_Q\).

Consequently the minimum support cost is
\[
  1+C_{a_r}(F_C,a|_Q),
\]
where \(C_b(F_C,a|_Q)\) is ordinary pointwise Boolean certificate complexity
for forcing value \(b\) at the hard frontier assignment.

## Proof Skeleton

1. If \(r\notin S\), keep the frontier fixed and flip the root; the relation
   fails, so \(r\) is required.
2. If \(S\cap Q\) does not certify \(F_C(z)=a_r\), there is a frontier
   completion agreeing on \(S\cap Q\) with \(F_C(z)\ne a_r\); with root fixed
   to \(a_r\), the relation fails.
3. Conversely, if \(r\in S\) and \(S\cap Q\) certifies \(F_C(z)=a_r\), every
   completion preserving \(S\) keeps both the root and the circuit value fixed,
   so the relation holds.

## Boundary

This generalizes the pure OR frontier theorems to exposed finite acyclic
Boolean frontier circuits, including AND/OR/NOT compositions.  It does not
solve full SAT self-reduction residual completion: a proof system still has to
expose the finite acyclic frontier circuit or adaptive control tree, justify
quotienting, and rule out learned or hidden semantic effects not represented in
the support audit.

## Gate Impact

This is C11-admitted interface-variant boundary work.  It strengthens the same
semantic-frontier spine: the nonlinear semantic route now has a general
acyclic-circuit certificate theorem, while the remaining publication-level
blocker is no longer "beyond pure OR" in general, but hidden adaptive SAT
semantics or an explicit SAT-family/source lower bound.
