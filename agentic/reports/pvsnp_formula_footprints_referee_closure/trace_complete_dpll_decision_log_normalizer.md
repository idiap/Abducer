<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Trace-Complete DPLL Decision-Log Normalizer

- Status: `proved_in_revised_tex`
- TeX label: `cor:trace-complete-dpll`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Claim

A DPLL-style decision log supplies the controller-complete adaptive audit only
when the proof object is trace-complete.  The log must expose:

1. the finite acyclic decision controller over frontier or formula-label
   coordinates;
2. the replay path followed by the hard tuple;
3. the terminal output on that path;
4. local clause, propagation, or pruning witnesses certifying that the hidden
   solver semantics agrees with the exposed controller on the completion
   cylinder claimed by the support.

Under those hypotheses, the root, replay-path variables, and witness variables
form a support-local set.  Any checker budget that upper-bounds that set is
therefore subject to the same near-threshold formula-footprint lower bound.

## C11 Admission Card

- Role: `proof_system_bridge`
- Flagship obstruction strengthened: proof-object support budget for the
  formula-footprint barrier.
- Before/after shift: before, the positive hidden-adaptive theorem still looked
  like an abstract audit condition; after, a recognizable DPLL-style proof
  object is shown to supply the audit exactly when it logs the whole controller
  and local witnesses.
- Boundary clarified: partial solver transcripts, unaudited learned clauses,
  restarts, cyclic search graphs, and arbitrary CDCL traces do not supply the
  normalizer by syntax alone.
- Remaining nonclaim: no lower bound for arbitrary CDCL, Frege, Extended Frege,
  IPS, or hidden SAT self-reduction semantics.
- Narrative indivisibility: detached from the formula-footprint spine, this is
  only proof-log bookkeeping; inside the paper it is the first recognizable
  adaptive proof-object bridge for the completion-sound support obstruction.

## Proof Skeleton

1. Treat the logged DPLL controller as the exposed acyclic branching program.
2. Treat the hard-tuple execution as the replay path.
3. Add all formula-label variables appearing in local clause, propagation, or
   pruning witnesses to the support.
4. Those witnesses certify local equivalence between hidden solver semantics
   and the exposed controller on the completion cylinder.
5. Apply the controller-complete adaptive audit normalizer.
6. Apply the support-local normalization transfer and formula-footprint
   threshold corollary to obtain the support-budget lower bound.

## Nonclaims

- no arbitrary CDCL lower bound;
- no support extraction from partial DPLL or SAT-solver transcripts;
- no learned-clause theorem without antecedent or local witness provenance;
- no restart or cyclic search-graph normalizer;
- no Frege, Extended Frege, or IPS lower bound;
- no explicit SAT-carrier lower bound.
