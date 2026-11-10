<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hidden Adaptive Transcript Insufficiency Separator

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:hidden-adaptive-transcript-insufficiency`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: `boundary`

## Purpose

This packet closes a tempting but invalid shortcut: a small reported adaptive
transcript is not automatically a support certificate when the adaptive
controller is hidden.  The visible-adaptive decision-tree and branching-program
theorems are positive because the whole control object is checker-visible and
the path is certified complete.  Without that completeness guarantee, the same
reported transcript can be compatible with a low-support function and a
function whose all-zero certificate requires every frontier coordinate.

## Statement

Fix \(m\ge 2\), frontier coordinates \(Q=\{q_1,\ldots,q_m\}\), root coordinate
\(r\), and hard tuple \(a_r=0\), \(a_{q_i}=0\) for every \(i\).  Consider the
reported adaptive transcript summary
\[
  \tau=(q_1=0,\mathrm{output}=0),
\]
with no certified claim that it is a complete computation path.  The same
summary is compatible at \(a\) with:
\[
  R_1=\{(y_r,z):y_r=z_{q_1}\}
\]
and
\[
  R_{\vee}=\{(y_r,z):y_r=\bigvee_{i=1}^m z_{q_i}\}.
\]

For \(R_1\), the support \(\{r,q_1\}\) is support-local at \(a\).  For
\(R_{\vee}\), every support-local set at \(a\) must contain \(r\) and all
frontier coordinates in \(Q\).  Therefore any extractor that sees only
\(\tau\) and returns a proper subset of \(\{r\}\cup Q\) is unsound for some
hidden adaptive controller compatible with the same reported transcript.

## Proof Skeleton

1. Both relations agree with the reported transcript summary at the all-zero
   tuple.
2. For \(R_1\), fixing \(r=0\) and \(q_1=0\) forces the residual relation.
3. For \(R_{\vee}\), omitting the root permits a root flip, and omitting any
   frontier coordinate permits setting that coordinate to \(1\) while the root
   remains \(0\).
4. Hence a transcript-only extractor cannot distinguish the small-support case
   from the all-frontier-support case.

## Boundary

This is a separator, not a hidden-adaptive positive theorem.  It does not prove
a hidden adaptive SAT self-reduction invariant, a learned-clause support
theorem, a cyclic semantic theorem, or a lower bound for a stronger proof
system.  It proves that a sound hidden-adaptive normalizer must add more
structure: certified controller/path completeness, exposed dependency support,
or worst-case frontier support.

## Gate Impact

This is C11-admitted boundary work.  It strengthens the same formula-footprint
spine by explaining why the visible-adaptive theorems require visibility.  The
before/after shift is concrete: "use the logged transcript" is no longer an
ambiguous possible shortcut; without a completeness audit it is formally
unsound.
