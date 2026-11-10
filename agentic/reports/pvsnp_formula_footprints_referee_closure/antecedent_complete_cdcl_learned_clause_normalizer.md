<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Antecedent-Complete CDCL Learned-Clause Normalizer

- Status: `proved_in_revised_tex`
- TeX label: `cor:antecedent-complete-cdcl`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Claim

A CDCL-style learned-clause log supplies the controller-complete adaptive audit
only when the proof object is antecedent-complete.  The log must expose:

1. the finite acyclic decision and restart controller;
2. the replay path followed by the hard tuple;
3. the terminal output on that path;
4. every learned clause, propagation, or pruning step used on the replay path;
5. an acyclic antecedent DAG for each used learned clause, with leaves in
   original support-local clauses, explicit decisions, unit-propagation
   witnesses, or lower-rank learned clauses.

Under those hypotheses, expanding the learned clauses through their antecedent
DAGs yields the same controller-complete audit as in the trace-complete DPLL
case.  The root, replay-path variables, and all formula-label variables in the
used antecedent closure form a support-local set.  Any checker budget that
upper-bounds this set is therefore subject to the near-threshold
formula-footprint lower bound.

## C11 Admission Card

- Role: `proof_system_bridge`
- Flagship obstruction strengthened: proof-object support budget for the
  formula-footprint barrier.
- Before/after shift: before, CDCL was excluded as arbitrary learned-clause
  compression; after, the paper states the exact provenance condition under
  which learned clauses are admissible.
- Boundary clarified: learned clauses are not free support compression.  They
  count only when every used learned clause has acyclic antecedent provenance
  down to audited local support.
- Remaining nonclaim: arbitrary CDCL, hidden clause minimization, deleted
  antecedent provenance, cyclic restart/search graphs, and clause-database
  summaries are not normalized by syntax alone.
- Narrative indivisibility: outside the formula-footprint spine this is only a
  proof-log provenance convention; inside the paper it shows how learned-clause
  compression must pay for the same completion-sound support obstruction.

## Proof Skeleton

1. Expand each learned clause used on the replay path along its antecedent DAG.
2. Acyclic rank order ensures the expansion terminates in original local
   clauses, explicit decisions, unit-propagation witnesses, or lower-rank
   learned clauses.
3. Add all formula-label frontier coordinates in this antecedent closure to the
   support.
4. The expanded antecedent closure certifies local controller equivalence on
   the completion cylinder.
5. Apply the controller-complete adaptive audit normalizer, equivalently the
   trace-complete DPLL normalizer after expansion.
6. Apply the support-local normalization transfer and formula-footprint
   threshold corollary to obtain the support-budget lower bound.

## Nonclaims

- no arbitrary CDCL lower bound;
- no support extraction from learned clauses without antecedent provenance;
- no hidden clause-minimization normalizer;
- no deleted-clause provenance-gap theorem;
- no cyclic restart or cyclic search-graph normalizer;
- no Frege, Extended Frege, or IPS lower bound;
- no explicit SAT-carrier lower bound.
