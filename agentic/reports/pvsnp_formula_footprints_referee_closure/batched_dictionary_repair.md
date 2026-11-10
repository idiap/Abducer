<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Batched Dictionary Repair

- Status: `patched`
- Affected lemma: batched static dictionary lookup.
- Source issue: symmetry of the final aggregator removes the need to restore original query order, but it does not remove the need to separate query records from dictionary records after sorting.

## Repair Summary

The circuit should use explicitly typed records:

- query records: `(key, is_query=1, index, payload=0)`;
- dictionary records: `(key, is_query=0, index=0, payload=value)`.

Sort lexicographically by `(key, is_query)` with dictionary records before query records for equal keys. A scan propagates the most recent dictionary value across an equal-key block. Each query record then carries its recovered dictionary value or the default value if no dictionary record appeared in its key block.

The output stage must mask by `is_query`. If the aggregator is symmetric, the circuit may aggregate the recovered values over query records in their sorted order, because the multiset of query values is unchanged. If the aggregator is not symmetric, the circuit must perform the second sort by `(is_query, index)` and feed the first `M` query records in original order. In both cases dictionary records are ignored by the output aggregator.

## Bound

Let `N=M+K` and record width `w=O(ell+log N)`.

- First sort: `O(N log^2 N * w)` using Batcher comparators.
- Scan and dictionary-value propagation: `O(N w)`.
- Symmetric aggregation with query masks: `O(N)` or `O(N * size(A_N))` depending on the aggregator encoding; for the draft's use this is absorbed by the stated `O((M+K) polylog(M+K, 2^ell))` term.
- Optional second sort for nonsymmetric aggregation: another `O(N log^2 N * w)`.

Thus the asymptotic bound used by the formula-footprint theorem is unchanged.

## Downstream Audit

| Downstream use | Status after patch | Comment |
|---|---|---|
| Cheap completion from small defect set | `unchanged` | The dictionary still recovers all generated labels from a hardwired exception set. |
| Formula-footprint theorem | `unchanged` | The lower bound still follows after replacing the faulty shortcut by masked query extraction. |
| Threshold corollary | `unchanged` | Only constants and polylog factors are affected. |
| Adaptive transcript proposition | `unchanged` | The proposition uses the theorem after the dictionary repair. |

## Paper Patch

Use `batched_dictionary_repair.tex` to replace the proof paragraph of the batched static dictionary lemma.
