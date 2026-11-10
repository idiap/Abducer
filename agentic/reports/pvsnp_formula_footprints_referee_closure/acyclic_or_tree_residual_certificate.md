<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Acyclic OR-Tree Residual Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:acyclic-or-tree-residual`
- Criteria affected: `C5`, `C7`, `C10`, `C11`
- Result role: `interface_variant_boundary`

## Purpose

This packet extends the semantic-relation theorem from one local OR tuple to a
bounded global residual-completion statement for an acyclic self-reduction tree.
It keeps the claim honest: the theorem applies after internal OR nodes are
eliminated, so the remaining relation is root equals OR of leaves.  It is not a
full theorem for arbitrary SAT self-reduction DAGs or unrestricted semantic SAT
proofs.

## Statement

Let \(T\) be a finite rooted OR tree with leaf set \(L\) and root \(r\).  Let
\[
  R_T=\{(y_r,(y_\ell)_{\ell\in L}) : y_r=\bigvee_{\ell\in L} y_\ell\}.
\]
For a satisfying tuple \(a\in R_T\), a support set \(S\subseteq \{r\}\cup L\)
is support-local for \(R_T\) at \(a\) iff \(S\) is a standard certificate for
the root OR relation:

- if \(a_r=0\), then \(r\in S\) and every leaf \(\ell\in L\) lies in \(S\);
- if \(a_r=1\), then \(r\in S\) and \(S\) contains at least one leaf
  \(\ell\) with \(a_\ell=1\).

Thus an unsatisfiable branch in an acyclic OR self-reduction tree costs all
frontier leaves after internal nodes are eliminated, while a satisfiable branch
costs the root plus one satisfying witness leaf.

## Proof Skeleton

1. Eliminating internal OR nodes gives the single relation
   \(y_r=\bigvee_{\ell\in L}y_\ell\).
2. Support-locality is exactly membership certification for this finite
   relation.
3. For root \(0\), any unfixed leaf can be flipped to \(1\), violating the
   relation; the root must also be fixed.
4. For root \(1\), fixing the root and one true leaf forces the relation, and
   omitting all true leaves lets all leaves be completed to \(0\), violating it.

## Boundary

This is not a full SAT self-reduction residual-completion theorem.  The
quotiented OR-DAG packet handles the pure shared-OR frontier extension.  The
Boolean-frontier and visible-adaptive packets handle exposed non-OR and exposed
adaptive control.  This tree packet does not handle learned clauses, cyclic
dependencies, arbitrary SAT self-reduction DAGs, or proof systems whose semantic
influence is not exposed as an auditable frontier relation.

## Gate Impact

This improves the nonlinear semantic route from one local relation instance to
a small global residual relation.  It strengthens C10 and C11 because the
before/after shift is clear: bounded acyclic OR self-reduction no longer sits as
a vague caveat; it has an exact certificate cost, and the OR-DAG packet now
shows the same for shared pure-OR frontiers after sound quotienting.  The
remaining top-paper blocker is still a stronger proof-system support audit or
explicit SAT-family theorem.
