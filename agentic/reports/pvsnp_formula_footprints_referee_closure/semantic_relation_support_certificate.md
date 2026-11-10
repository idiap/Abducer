<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Semantic-Relation Support Certificate

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:semantic-relation-support`
- Criteria affected: `C5`, `C7`, `C10`, `C11`

## Result

The revised paper now includes a local theorem for nonlinear semantic
constraints.  Let a Boolean relation \(R\subseteq\{0,1\}^J\) be imposed on a
finite tuple of formula-label variables, and let the hard labeling restricted to
that tuple be \(a\in R\).  If a declared support \(S\) is sound in the
completion-local sense that every labeling agreeing with \(a\) on \(S\cap J\)
still satisfies \(R\), then \(S\cap J\) is a standard \(1\)-certificate for
membership of \(a\) in \(R\).

For the SAT self-reduction relation
\[
  y = y_0 \vee y_1,
\]
this gives concrete certificate costs:

- for \((y,y_0,y_1)=(1,1,0)\) or \((1,1,1)\), fixing \(y=1\) and \(y_0=1\)
  is enough;
- for \((1,0,1)\), fixing \(y=1\) and \(y_1=1\) is enough;
- for \((0,0,0)\), all three labels must be fixed.

## Proof Skeleton

1. Support-locality says every completion preserving the declared coordinates
   stays inside \(R\).
2. That is exactly the definition of a certificate for the relation \(R\) at
   the hard tuple.
3. The OR examples follow by checking which partial assignments force
   \(y=y_0\vee y_1\).

## Gate Impact

This is not a full residual-completion theorem for SAT self-reduction.  It is a
local audit theorem: nonlinear semantic constraints are admissible only when the
declared support already contains a certificate for each relation instance.
This converts part of the nonlinear-SAT gap into a checkable support-accounting
obligation.
