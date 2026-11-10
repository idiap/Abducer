<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Visible Adaptive Branching-Program Frontier Residual Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:visible-adaptive-branching-frontier-residual`
- Criteria affected: `C5`, `C7`, `C10`, `C11`
- Result role: `interface_variant_boundary`

## Purpose

This packet removes the tree-only caveat from the visible-adaptive frontier
theorem.  A checker-visible adaptive decision tree may be exponentially larger
than a shared adaptive proof object.  The branching-program theorem handles the
shared-state case: if the proof object exposes a finite acyclic deterministic
branching program over frontier coordinates, support-locality is again root plus
ordinary pointwise certificate complexity for the induced Boolean function.

The theorem is still deliberately visible.  Sharing is allowed, and the actual
computation path gives sufficient support, but hidden controllers, learned
clauses, cyclic semantic dependence, and unlogged adaptive choices still require
a separate invariant.

## Statement

Let \(B\) be a finite acyclic deterministic branching program with start node
\(s\), internal nodes querying frontier coordinates \(Q\), and bit-labelled
sinks.  Let \(r\) be the root/output coordinate, and let
\(F_B:\{0,1\}^Q\to\{0,1\}\) be the Boolean function computed by following the
queried edge labels from \(s\) to a sink.  The residual frontier relation is
\[
  R_B=\{(y_r,z): y_r=F_B(z)\}.
\]
For a satisfying tuple \(a\in R_B\), a support set
\(S\subseteq\{r\}\cup Q\) is support-local for \(R_B\) at \(a\) iff:

1. \(r\in S\); and
2. \(S\cap Q\) is a standard pointwise certificate forcing
   \(F_B(z)=a_r\) at \(a|_Q\).

Consequently the minimum support cost is
\[
  1+C_{a_r}(F_B,a|_Q).
\]
The actual queried coordinates on the \(a|_Q\)-computation path give one
sufficient frontier certificate.

## Proof Skeleton

1. If the root coordinate is omitted, flip the root while preserving the
   frontier assignment.
2. If the frontier support does not certify the branching-program value, choose
   a frontier completion agreeing on the support but reaching output
   \(1-a_r\); with the root fixed, the residual relation fails.
3. Conversely, root plus a frontier certificate forces the residual relation.
4. The computation-path coordinates are sufficient because preserving them
   follows the same visible branching-program edges to the same sink.

## Boundary

This is a visible shared-adaptive theorem only.  It assumes the whole finite
acyclic branching program, including all query nodes, branch edges, start node,
and sink labels, is exposed and checker-visible.  It does not prove a hidden
adaptive SAT self-reduction invariant, learned-clause semantic support theorem,
cyclic semantic theorem, or lower bound for a proof system whose adaptive
controller is not part of the audited support object.

## Gate Impact

This is C11-admitted as interface-variant boundary work.  It strengthens the
same semantic-frontier spine by showing that shared adaptive control is harmless
only after the branching program itself is exposed.  The remaining
publication-level blocker is sharper: prove such visibility or an equivalent
semantic invariant for a stronger proof system, or replace the proof-system
route with an explicit SAT-family/source theorem.
