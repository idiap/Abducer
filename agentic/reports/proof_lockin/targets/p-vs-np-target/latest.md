<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof Lock-In Report

Target: `p-vs-np-target`
Mode: `exploration_continue`
Paper relevance: `not_locked`
Transfer substance: `blocked`
Cycle budget: `0`

## Subgoal

No frozen subgoal is active.

## Non-Claims

- Do not claim the main problem is solved from a subgoal.
- Do not promote a definition-built transfer theorem.
- Do not advertise a local subgoal as the full target theorem.
- Do not replace a missing transfer theorem by narrative continuity.

## Main-Problem Balance

- Local scope: Carrier transfer remains blocked until uniformity and advice discipline are certified.
- Larger boundary: The main target remains open until the target theorem, transfer, and non-claim boundaries are proved in the original problem setting.
- Allowed claim: Claim only the local theorem, obstruction, worked example, transfer boundary, or demotion supported by the live ledger.
- Balance test: Every consolidation must state what larger-problem gate it changes and which gate remains untouched.

## Publication Consolidation Limit

- Max completion cycles: `4`
- Max recursion depth: `1`
- Stop conditions: `publication_ready_subgoal, precise_demotion, blocked_named_lemma, budget_exhausted_release_to_exploration`
- Recursion guard: No nested publication-consolidation loop is allowed; side work must fit the current budget or return to exploration.
- Re-entry condition: only a new live learning event that changes a hard gate, supplies a missing object, or resolves a named blocker may start a fresh consolidation window

## Next Action

`proof-depth-pressure-formalizer`

Return note: write a handoff, demote or block the subgoal, and return to conceptual exploration before any new publication consolidation

Validation handoff: `agentic/scripts/validate_proof_lockin_report.py`
