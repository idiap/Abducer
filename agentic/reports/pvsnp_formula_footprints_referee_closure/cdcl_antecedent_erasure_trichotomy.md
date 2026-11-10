<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# CDCL Antecedent-Erasure Trichotomy

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:cdcl-antecedent-erasure-trichotomy`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: `boundary`

## Claim

An arbitrary CDCL-style log whose learned-clause antecedents and variable-role
provenance are erased is not a free support normalizer for the
formula-footprint theorem.  A support extractor that sees only:

1. the decision/restart skeleton;
2. the replay path;
3. the sequence of learned-clause names and uses; and
4. the untyped displayed clauses

falls into a trichotomy on the same unit-plus-blocking skeleton used for
support erasure:

1. **Provenance branch:** it obtains learned-clause antecedent DAGs, a trusted
   variable-role map, a namespace certificate, a support-locality checker, or
   another system-specific semantic invariant.  Then it is no longer an
   antecedent-erased CDCL extractor; it has supplied the support audit being
   charged.
2. **Conservative branch:** it is sound for every same-skeleton semantic lift.
   Then it must output all variables in the possible label lift and pays the
   role-agnostic support budget.
3. **Unsound branch:** it outputs a strict subset while seeing only the erased
   skeleton.  Then the label lift with the same erased learned-clause skeleton
   falsifies support soundness.

Thus arbitrary provenance-free CDCL syntax does not instantiate the
support-local normalization transfer by itself.

## C11 Admission Card

- Role: `boundary`
- Flagship obstruction strengthened: proof-object support budget for the
  formula-footprint barrier.
- Before/after shift: before, the open problem said to go beyond
  antecedent-complete CDCL; after, the arbitrary-CDCL route is narrowed to a
  trichotomy: add provenance or a non-plain invariant, pay conservative
  support, or lose soundness.
- Boundary clarified: learned-clause antecedent erasure is not a harmless
  presentation choice.  It removes exactly the support object needed by the
  positive CDCL theorem.
- Remaining nonclaim: no arbitrary CDCL lower bound, no Frege/Extended
  Frege/IPS lower bound, no hidden clause-minimization normalizer, and no
  explicit SAT-family/source lower bound.
- Narrative indivisibility: outside the formula-footprint spine this is only
  a proof-log caution.  Inside the paper it identifies why the next
  proof-system theorem must expose or replace the learned-clause support audit.

## Proof Skeleton

1. Reuse the unit-plus-blocking skeleton from the support-erasure separator.
2. Package the ambiguous blocking object as a learned-clause use on the replay
   path.
3. Build two same-skeleton lifts: an auxiliary lift with empty formula-label
   support after roles are known, and a label lift in which the support-audit
   necessity separator forces all variables in the frontier.
4. Erasing learned-clause antecedents and role provenance makes the two lifts
   identical to the CDCL-erased extractor.
5. The extractor must therefore return the same support in both lifts.
6. If it returns all frontier variables, it is conservative but pays the full
   role-agnostic budget.  If it returns a strict subset, the label lift is a
   counterexample.  If it returns different supports, it used extra provenance
   or a semantic invariant beyond erased CDCL syntax.

## Nonclaims

- no arbitrary CDCL lower bound;
- no support extraction from provenance-free learned clauses;
- no hidden clause-minimization normalizer;
- no deleted-clause provenance-gap normalizer;
- no cyclic restart or cyclic search-graph normalizer;
- no Frege, Extended Frege, or IPS lower bound;
- no explicit SAT-carrier lower bound.
