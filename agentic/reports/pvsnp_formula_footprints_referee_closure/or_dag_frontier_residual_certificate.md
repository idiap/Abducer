<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# OR-DAG Frontier Residual Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:or-dag-frontier-residual`
- Criteria affected: `C5`, `C7`, `C10`, `C11`
- Result role: `interface_variant_boundary`

## Purpose

This packet strengthens the acyclic OR-tree theorem to the pure-OR fragment with
shared subproblems and repeated frontier formulas.  The theorem applies to a
finite acyclic OR DAG after all internal OR nodes are eliminated and soundly
equal frontier formulas have been quotiented.  The remaining relation is still a
single root coordinate equal to the OR of the reachable frontier coordinates.

The point is deliberately narrow.  It removes a superficial tree-only caveat for
pure OR self-reduction frontiers, while preserving the boundary against
hidden, cyclic, learned-clause, and arbitrary SAT-semantic proof systems.
Exposed acyclic non-OR frontiers are handled separately by the acyclic Boolean
frontier residual certificate, and exposed adaptive frontiers by the
visible-adaptive frontier residual certificate.

## Statement

Let \(D\) be a finite acyclic directed graph with root \(r\).  Each non-frontier
node computes the OR of its children.  Let \(Q_r\) be the set of distinct
quotient classes of frontier coordinates reachable from \(r\).  After
eliminating internal OR nodes, the residual frontier relation is
\[
  R_D=\{(y_r,(z_q)_{q\in Q_r}) : y_r=\bigvee_{q\in Q_r}z_q\}.
\]

For a tuple \(a\in R_D\), a support set \(S\subseteq \{r\}\cup Q_r\) is
support-local for \(R_D\) at \(a\) iff it is a standard certificate for this
frontier OR relation:

- if \(a_r=0\), then \(r\in S\) and every reachable frontier class \(q\in Q_r\)
  lies in \(S\);
- if \(a_r=1\), then \(r\in S\) and \(S\) contains at least one reachable
  frontier class \(q\) with \(a_q=1\).

Thus sharing inside the OR DAG and equality quotienting among repeated frontier
formulas do not change the exact residual certificate cost.  They only replace
raw leaves by distinct reachable frontier classes.

## Proof Skeleton

1. Topologically eliminate internal OR nodes.  Each internal node becomes the OR
   of all reachable frontier coordinates.
2. Since OR is idempotent, repeated frontier occurrences and shared subgraphs
   collapse to the distinct reachable frontier class set \(Q_r\).
3. The residual relation is therefore the ordinary OR relation on \(Q_r\).
4. The root-zero and root-one support-local certificates are exactly the usual
   OR certificates.

## Boundary

This is not a full SAT self-reduction residual-completion theorem.  It does not
handle alternating AND/OR semantic systems, negations, learned clauses,
arbitrary equality constraints beyond sound frontier quotienting, visible
adaptive control trees, or proof systems whose SAT-semantic influence is hidden
rather than exposed as a finite OR-DAG frontier relation.

## Gate Impact

This is C11-admitted because it is not a separate payoff.  It tightens the same
semantic-frontier interface introduced by the local relation and acyclic OR-tree
theorems.  The before/after shift is that shared pure-OR self-reduction DAGs no
longer remain a vague nonclaim: after frontier quotienting they have the same
exact residual certificate cost.  The remaining top-paper blocker is a support
audit for hidden adaptive semantics in a stronger proof system, a residual
theorem beyond exposed acyclic semantic frontiers, or an explicit
SAT-family/source lower bound.
