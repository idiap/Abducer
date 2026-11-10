<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Namespace-Typed LRAT Antecedent-Closure Normalizer

- Status: `proved_in_revised_tex`
- TeX label: `cor:namespace-typed-lrat`
- Criteria affected: `C5`, `C8`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Claim

An LRAT-style checked trace with a trusted formula-label variable namespace can
supply a support audit without a separate derived-clause provenance package.
Take the LRAT antecedent closure of the final empty clause, restrict to the
actually used auxiliary clauses, and collect the formula-label variables that
occur in those clauses.  If those used auxiliary clauses have a hard auxiliary
witness, then this collected set is support-local.

Near the formula-footprint threshold, the namespace/antecedent-closure support
must contain \(n^{a-o(1)}\) labels of each polarity, and any checker-visible
support budget must be at least \(2n^{a-o(1)}\).

## Why This Is Stronger Than The Previous LRAT Bridge

The provenance-typed LRAT corollary requires an explicit provenance package for
derived clauses.  This corollary uses only:

1. LRAT antecedent closure of the empty clause;
2. a trusted namespace that identifies formula-label variables \(Y_u\);
3. the formula-label variables appearing in the used original auxiliary
   clauses;
4. a hard witness satisfying those used auxiliary clauses.

It is still not plain untyped LRAT: erasing the namespace recreates the
support-erasure ambiguity.

## Proof Skeleton

1. Delete all clauses outside the LRAT antecedent closure of the empty clause.
2. Let \(S_\tau\) be the labels whose variables occur in the used auxiliary
   clauses.
3. Any labeling agreeing with the hard labeling on \(S_\tau\) gives the same
   truth values to all label literals in the used auxiliary clauses.
4. Reuse the hard auxiliary witness to satisfy the used auxiliary clauses under
   every such completion.
5. This is precisely the support audit required by the support-audited LRAT
   normalizer.
6. Apply the formula-footprint threshold.

## Nonclaim Boundary

- no lower bound for plain untyped LRAT or DRAT;
- no support extraction after erasing the formula-label namespace;
- no theorem for auxiliary clauses without a hard witness or separate
  support-locality proof;
- no Frege, Extended Frege, IPS, or arbitrary compressed proof lower bound.
