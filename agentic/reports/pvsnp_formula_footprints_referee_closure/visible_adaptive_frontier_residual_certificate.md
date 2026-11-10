<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Visible Adaptive Frontier Residual Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:visible-adaptive-frontier-residual`
- Criteria affected: `C5`, `C7`, `C10`, `C11`
- Result role: `interface_variant_boundary`

## Purpose

This packet narrows the hidden adaptive semantic blocker without pretending to
solve it.  The acyclic Boolean frontier theorem handles exposed circuits.  This
proposition records the corresponding visible-adaptive case: if the proof object
exposes a finite adaptive decision tree over frontier coordinates, then
support-locality is again root plus ordinary pointwise certificate complexity
for the induced Boolean function.

The theorem also explains why a logged transcript is a support object only when
the decision tree itself is checker-visible.  The coordinates queried on the
actual root-to-leaf path form a sufficient certificate, but a hidden controller,
learned-clause mechanism, cyclic semantic dependence, or unlogged adaptive
choice still needs a separate invariant.

## Statement

Let \(T\) be a finite binary decision tree querying frontier coordinates
\(Q\), with leaf labels in \(\{0,1\}\), root coordinate \(r\), and induced
function \(F_T:\{0,1\}^Q\to\{0,1\}\).  The residual frontier relation is
\[
  R_T=\{(y_r,z): y_r=F_T(z)\}.
\]
For a satisfying tuple \(a\in R_T\), a support set
\(S\subseteq\{r\}\cup Q\) is support-local for \(R_T\) at \(a\) iff:

1. \(r\in S\); and
2. \(S\cap Q\) is a standard pointwise certificate forcing
   \(F_T(z)=a_r\) at \(a|_Q\).

Consequently the minimum support cost is
\[
  1+C_{a_r}(F_T,a|_Q).
\]
The actual queried coordinates on the \(a|_Q\)-transcript path give one
sufficient frontier certificate.

## Proof Skeleton

1. If the root coordinate is omitted, flip the root while preserving the
   frontier assignment.
2. If the frontier support does not certify the decision-tree value, choose a
   frontier completion agreeing on the support but reaching output
   \(1-a_r\); with the root fixed, the residual relation fails.
3. Conversely, root plus a frontier certificate forces the residual relation.
4. The transcript-path coordinates are sufficient because preserving them
   follows the same path to the same labeled leaf.

## Boundary

This is a visible-adaptive theorem only.  It assumes the whole finite decision
tree, including all branch tests and leaf labels, is exposed and checker-visible.
It does not prove a hidden adaptive SAT self-reduction invariant, learned-clause
semantic support theorem, cyclic semantic theorem, or lower bound for a proof
system whose adaptive controller is not part of the audited support object.

## Gate Impact

This is C11-admitted as interface-variant boundary work.  It strengthens the
same semantic-frontier spine by showing that adaptivity is harmless only after
the adaptive control object is exposed.  The remaining publication-level blocker
is sharper: prove such visibility or an equivalent semantic invariant for a
stronger proof system, or replace the proof-system route with an explicit
SAT-family/source theorem.
