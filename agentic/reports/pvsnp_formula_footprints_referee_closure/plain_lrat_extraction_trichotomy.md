<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Plain LRAT Extraction Trichotomy

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:plain-lrat-extraction-trichotomy`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: `boundary`

## Purpose

This packet consolidates the two LRAT boundary results into an operational
decision theorem.  The support-audit necessity separator shows that a short
checked clausal refutation can still require a large sound support audit.  The
support-erasure separator shows that untyped LRAT syntax does not determine
which variables are formula labels.  The trichotomy states the resulting
publication-level lesson for plain LRAT/DRAT extraction: a raw trace extractor
must either add provenance, pay a role-agnostic worst-case support budget, or
be unsound on some semantic lift of the same trace.

## Statement

Let a `plain extractor` be a procedure that sees only the untyped clauses and
LRAT antecedent hints of a clausal refutation.  Suppose it outputs a set of
variables intended to serve as a completion-local formula-label support.

For the unit-plus-blocking skeleton \(C_T\) used in the support-erasure
separator, any such extractor falls into one of three cases:

1. **Provenance branch:** it obtains a variable-role map, clause provenance, or
   support-locality checker.  Then it is no longer a plain extractor; it has
   supplied the support audit charged by the provenance-typed LRAT theorem.
2. **Conservative branch:** it is sound for every semantic lift of the raw
   trace.  Then on \(C_T\) it must output a support containing every variable
   in \(T\), because the label lift requires all labels.
3. **Unsound branch:** it outputs a strict subset of \(T\) while seeing only
   the raw trace.  Then the same trace with the label lift falsifies its
   claimed completion-local support.

Thus plain LRAT/DRAT syntax alone gives no nontrivial support-extraction
normalizer for this paper.  Any usable theorem must either charge extra
provenance or prove a separate system-specific invariant that rules out the
bad semantic lift.

## Proof Skeleton

1. Use the same skeleton \(C_T\) and the same linear LRAT trace as in
   `prop:support-erasure-indistinguishability`.
2. A plain extractor receives identical input on the auxiliary lift and label
   lift, so it must return the same support set for both.
3. In the label lift, `prop:support-audit-necessity` forces every sound support
   to contain \(T\).
4. If the extractor returns a strict subset, it is unsound on the label lift.
5. If it returns all of \(T\), it is role-agnostically sound for this skeleton
   but pays the full support budget.
6. If it returns different outputs across the two lifts, then it used
   information beyond the plain trace, namely provenance or an equivalent
   semantic invariant.

## Nonclaim Boundary

This is not a lower bound for every LRAT/DRAT refutation.  It is a no-free
support-extraction theorem for extractors whose input is only raw untyped trace
syntax.  A trusted role map, block provenance package, support-locality
checker, or proof-system-specific semantic invariant can still support a
positive theorem, but that object must be stated and charged.

## Gate Impact

This is C11-admitted boundary work, not a new side result.  It changes the next
proof-system route from "try plain LRAT extraction" to a sharper requirement:
either prove a concrete invariant that makes the trace non-plain, or leave the
LRAT route and move to a stronger proof-system normalizer or explicit
SAT-family/source theorem.
