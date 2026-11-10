<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Scoring Model

## Intervention Score

For statement `s`:

`score(s) = 0.40*downstream_impact + 0.25*bridge_centrality + 0.20*unresolved_dependency_pressure + 0.15*cross_component_potential`

All metrics are normalized to `[0,1]` before weighting.

## Metric Definitions

- `downstream_impact`: number of statements reachable from `s` through dependency edges.
- `bridge_centrality`: directed betweenness centrality (Brandes, unweighted).
- `unresolved_dependency_pressure`: count of missing `depends_on` IDs.
- `cross_component_potential`: strongest structure-level bridge opportunity to another weak component.

## Connection Candidate Score

For candidate pair `(a,b)`:

`score = 0.34*semantic_score + 0.20*component_gain + 0.14*influence + 0.12*kind_compatibility + 0.10*structural_similarity + 0.10*equiv_or_def_signal`

Where:

- `structural_similarity`: weighted structure-first proximity from typed symbol/method/family signals.
- `semantic_score`: weighted semantic signal.
  - `0.36*symbol_role_alignment + 0.24*method_overlap + 0.20*theorem_family_overlap + 0.12*equivalence_reduction + 0.08*definitional_expansion`
- `component_gain`: relative gain of linking their disconnected components.
- `influence`: max normalized downstream impact of either endpoint.
- `kind_compatibility`: prior favoring premise-to-target kind pairs.
- `equiv_or_def_signal`: max of equivalence/reduction and definitional-expansion signals.

Relation typing heuristics:

- `potential-equivalence` when equivalence/reduction signal is strong.
- `definitional-expansion` when definition alignment is strong.
- `method-transfer` when method overlap dominates.
- `analogy-transfer` when family overlap is high with low symbol overlap.
- otherwise `potential-support`.

## Interpretation Rule

Use top intervention points as abductive targets first; use top connection candidates as bridge and conceptual hypothesis proposals second.
