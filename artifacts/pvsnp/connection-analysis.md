# KB Connection Analysis: `KB/p-vs-np.kb.md`

## Stats

- Included statuses: accepted, tentative
- Statements: 64
- Filtered out statements: 0
- Dependency edges: 0
- Components: 64
- Missing dependencies: 0
- Avg semantic connection score: 0.3254
- Concept graph nodes: 85

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | partner |
|---|---|---|---|---|---|
| st.def.item | definition | 0.15 | 0 | 0 | st.def.item-2 |
| st.def.item-2 | definition | 0.15 | 0 | 0 | st.def.item |
| st.def.item-4 | definition | 0.1436 | 0 | 0 | st.def.item |
| st.def.item-3 | definition | 0.1412 | 0 | 0 | st.def.item-2 |
| st.def.exponential-time-classes | definition | 0.1385 | 0 | 0 | st.def.item-2 |
| st.def.polynomial-time-many-one-karp-reduction | definition | 0.1295 | 0 | 0 | st.def.item-2 |
| st.def.deterministic-communication-complexity | definition | 0.1291 | 0 | 0 | st.def.deterministic-decision-tree-complexity |
| st.def.deterministic-decision-tree-complexity | definition | 0.1291 | 0 | 0 | st.def.deterministic-communication-complexity |
| st.def.polynomially-bounded-proof-system | definition | 0.1279 | 0 | 0 | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 |
| st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | theorem | 0.1279 | 0 | 0 | st.def.polynomially-bounded-proof-system |
| st.def.cook-reckhow-propositional-proof-system | definition | 0.1274 | 0 | 0 | st.def.polynomially-bounded-proof-system |
| st.def.polynomial-hierarchy | definition | 0.1274 | 0 | 0 | st.def.item-3 |
| st.def.np-completeness | definition | 0.1216 | 0 | 0 | st.def.item-2 |
| st.def.boolean-formulas | definition | 0.1187 | 0 | 0 | st.def.circuit-family-s-n |
| st.def.circuit-family-s-n | definition | 0.1187 | 0 | 0 | st.def.boolean-formulas |
| st.def.monotone-circuits | definition | 0.1187 | 0 | 0 | st.def.boolean-formulas |
| st.thm.bounded-depth-frege-php-lower-bounds-beamepitass | theorem | 0.1187 | 0 | 0 | st.thm.resolution-php-lower-bounds-exemplar-buss1988 |
| st.thm.resolution-php-lower-bounds-exemplar-buss1988 | theorem | 0.1187 | 0 | 0 | st.thm.bounded-depth-frege-php-lower-bounds-beamepitass |
| st.def.algebrising-proof-technique-informal | definition | 0.1138 | 0 | 0 | st.def.relativising-proof-technique-informal |
| st.def.relativising-proof-technique-informal | definition | 0.1138 | 0 | 0 | st.def.algebrising-proof-technique-informal |

## Top Connection Candidates

| from_id | to_id | score | similarity | semantic | relation | evidence_terms |
|---|---|---|---|---|---|---|
| st.def.item | st.def.item-2 | 0.5779 | 0.6316 | 0.3834 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.item | st.def.item-4 | 0.5692 | 0.6047 | 0.3822 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.polynomially-bounded-proof-system | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 0.566 | 0.5385 | 0.3265 | definitional-expansion | users, user, source_citation, section, research, report |
| st.def.cook-reckhow-propositional-proof-system | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 0.5576 | 0.4773 | 0.3765 | definitional-expansion | users, user, source_citation, section, research, report |
| st.def.item-2 | st.def.item-4 | 0.554 | 0.5581 | 0.3801 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.exponential-time-classes | st.def.item-3 | 0.5532 | 0.5556 | 0.38 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.np-completeness | st.thm.cook-levin-sat-is-np-complete-cook1971 | 0.551 | 0.4 | 0.3955 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.deterministic-communication-complexity | st.def.deterministic-decision-tree-complexity | 0.5503 | 0.5435 | 0.3845 | definitional-expansion | users, user, source_citation, section, research, report |
| st.def.item-2 | st.def.polynomial-time-many-one-karp-reduction | 0.5499 | 0.5455 | 0.3795 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.cook-reckhow-propositional-proof-system | st.def.polynomially-bounded-proof-system | 0.543 | 0.5366 | 0.3613 | definitional-expansion | users, user, source_citation, section, research, report |
| st.def.item-2 | st.def.polynomial-hierarchy | 0.5428 | 0.5238 | 0.3786 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.item-2 | st.def.item-3 | 0.5384 | 0.5946 | 0.2568 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.algebrising-proof-technique-informal | st.def.relativising-proof-technique-informal | 0.5382 | 0.4792 | 0.4216 | definitional-expansion | users, user, source_citation, section, research, report |
| st.def.item | st.def.polynomial-hierarchy | 0.5351 | 0.5 | 0.3775 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.exponential-time-classes | st.def.item-2 | 0.5347 | 0.5833 | 0.2563 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.item | st.def.polynomial-time-many-one-karp-reduction | 0.5316 | 0.4894 | 0.377 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.item-3 | st.def.np-completeness | 0.5311 | 0.4878 | 0.377 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.exponential-time-classes | st.def.np-completeness | 0.5269 | 0.475 | 0.3764 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.exponential-time-classes | st.def.item | 0.5247 | 0.5526 | 0.2549 | potential-equivalence | users, user, source_citation, section, research, report |
| st.def.item-3 | st.def.polynomial-hierarchy | 0.5195 | 0.5366 | 0.2541 | potential-equivalence | users, user, source_citation, section, research, report |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.def.item, st.def.item-2, st.def.item-4, st.def.item-3, st.def.exponential-time-classes, st.def.polynomial-time-many-one-karp-reduction
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value cross-component links as abductive support hypotheses.
- Candidate connections: st.def.item->st.def.item-2 (0.5779), st.def.item->st.def.item-4 (0.5692), st.def.polynomially-bounded-proof-system->st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (0.566), st.def.cook-reckhow-propositional-proof-system->st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (0.5576), st.def.item-2->st.def.item-4 (0.554), st.def.exponential-time-classes->st.def.item-3 (0.5532)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
