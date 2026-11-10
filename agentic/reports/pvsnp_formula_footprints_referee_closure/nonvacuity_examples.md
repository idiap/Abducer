<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Nonvacuity Examples

- Status: `implemented`
- Decision: the abstract hardness predicates are nonempty in simple unrestricted or rank-conditioned models, but the motivating SAT-labeled carrier remains conditional and must not be promoted.

## Example A: Formula-label nonvacuity by an injective generator

Let \(M_n=1\).  Let \(G_n(x)\) be an injective encoding of \(x\) into a string
of length \(\ell_n\ge n+O(1)\), and let the aggregator be the identity.  A
formula labeling \(\lambda\) induces exactly the source truth table
\[
  F^\lambda_n(x)=\lambda(G_n(x)).
\]
By counting, for every circuit threshold below the number of Boolean functions
on \(n\) bits, there exist labelings whose induced source function has circuit
complexity greater than the threshold.  Therefore the formula-label hardness
predicate is nonempty for this unrestricted generated-label model.

- Type: `existence_by_counting`
- Strength: nonempty in the unrestricted label model.
- Limitation: not explicit, and not a SAT-labeled carrier.
- Paper use: supports nonvacuity of the abstract predicate, not the SAT application.

## Example B: Occurrence-label nonvacuity for arbitrary source truth tables

Let \(M_n=1\) in the occurrence model, or let \(M_n>1\) with parity aggregator
and set one coordinate to carry the source truth table while the remaining
coordinates are fixed to zero.  Because occurrence labels are private to
\((x,j)\), any source truth table \(h:\{0,1\}^n\to\{0,1\}\) can be realized by
choosing occurrence labels with
\[
  A(z(x,1),\ldots,z(x,M_n))=h(x).
\]
Taking \(h\) to be a hard function by counting gives a nonempty occurrence
hardness predicate.

- Type: `existence_by_counting`
- Strength: nonempty in the unrestricted occurrence-label model.
- Limitation: does not say that the SAT-generated occurrence labels are hard.
- Paper use: supports the row-forcing theorem as a structural certificate lemma.

## Example C: Quotient-label nonvacuity under a full-rank incidence hypothesis

For parity quotient labels, let
\[
  L_E:\mathbb F_2^{\mathcal C_n}\to\mathbb F_2^{2^n}
\]
be the quotient incidence map.  If \(L_E\) has full row rank, then every source
truth table lies in its image.  By counting, some quotient labeling induces a
source function of circuit complexity greater than any sub-counting threshold.
More generally, if the image code contains a word outside the size-\(s\)
circuit ball, then the quotient hardness predicate is nonempty.

- Type: `rank_conditioned`
- Strength: nonempty under an explicit linear-algebraic image condition.
- Limitation: if the image code is low rank or contained in an easy circuit
class, the predicate can be empty.
- Paper use: supports the quotient theorem only after the rank/image condition
is stated.

## Rejected Example: The actual SAT parity carrier

The statement
\[
  \Ckt(H_n^{\mathrm{SAT}})>n^{1+\epsilon-o(1)}
\]
would make the SAT-labeled hardness predicate nonempty at the desired threshold.
But this is exactly the source lower bound whose consequences the paper is
calibrating.  It cannot be used as a nonvacuity example unless it is labelled
as a conditional assumption.

- Type: `source_lower_bound_conditional`
- Status: `rejected_for_promotion`
- Paper use: motivation only.

## Promotion Consequence

The abstract certificate theorems are not vacuous, but their nonvacuity is
currently supported by unrestricted or rank-conditioned examples.  The paper
must say that no explicit hard SAT-labeled carrier is supplied.  This closes the
nonvacuity criticism only for a conservative certificate-complexity note, not
for a SAT lower-bound or proof-system paper.
