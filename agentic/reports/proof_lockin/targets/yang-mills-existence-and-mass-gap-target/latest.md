<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof Lock-In Report

Target: `yang-mills-existence-and-mass-gap-target`
Mode: `released_to_exploration`
Paper relevance: `support_only_or_appendix_note`
Transfer substance: `substantive_transfer`
Cycle budget: `0`

## Subgoal

No frozen subgoal is active.

## Non-Claims

- Do not claim the main problem is solved from a subgoal.
- Do not promote a definition-built transfer theorem.
- A finite reflected-Wilson obstruction proves the continuum mass gap.
- Endpoint-box positivity at fixed cutoff supplies OS/Wightman reconstruction.
- A same-theory marker replaces a continuum transfer theorem.
- A symbolic collar or toy calculation stands in for a gauge-invariant Wilson construction.

## Main-Problem Balance

- Local scope: Finite Route A subgoals: the reflected-Wilson Schur-Feshbach theorem, explicit H,K collar or hairpin objects, and post-H,K endpoint-box R/kappa_4 sign or interval certificates.
- Larger boundary: The Clay problem still requires a four-dimensional Yang-Mills quantum field theory satisfying the OS/Wightman axioms, a nontrivial continuum limit, and a positive Hamiltonian mass gap in the same theory.
- Allowed claim: A consolidation may claim only a finite theorem, worked Wilson calculation, same-theory transfer boundary, or route-deciding obstruction whose assumptions and non-claims are explicit.
- Balance test: Every local subgoal must name which larger YM gate it changes, which gate remains untouched, and why the local claim is still valuable without implying the full mass gap theorem.

## Publication Consolidation Limit

- Max completion cycles: `4`
- Max recursion depth: `1`
- Stop conditions: `publication_ready_subgoal, precise_demotion, blocked_named_lemma, budget_exhausted_release_to_exploration`
- Recursion guard: Do not open a nested publication-consolidation loop from inside a consolidation loop. Any sublemma, appendix, or side calculation must fit inside the current cycle budget or be deferred to conceptual exploration.
- Re-entry condition: only a new live learning event that changes a hard gate, supplies a missing object, or resolves a named blocker may start a fresh consolidation window

## Artifact-Or-Stop Finalization

- Completed cycles: `104`
- Blocked named artifact: endpoint_source_table with seven log Z samples, kappa_c intervals, D_c, C_N, M_G, T_tail, and I_gate interval
- No nested consolidation: `True`
- Release to exploration: after demotion/quarantine, select a conceptually distinct YM route with high physics reward rather than another endpoint API marathon
- Demotion boundary: Without the endpoint table and cutoff-uniform T_tail, the result is support-only route control, not a major YM subgoal completion.

## Next Action

`conceptual_exploration_after_release`

Return note: write a handoff, demote or block the subgoal, and return to conceptual exploration before any new publication consolidation

Validation handoff: `agentic/scripts/validate_proof_lockin_report.py`
