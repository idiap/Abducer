<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# YM Artifact-Or-Stop Anti-Incrementality Plan

Created: 2026-07-21

## Diagnosis

The last YM Azure marathon made one useful narrowing: the post-H,K endpoint
Route A branch now points to a one-sided connected-cumulant/source-interval
gate. But it did not close the gate. The repeated blocker is concrete:
endpoint source intervals for positive-D classes and a cutoff-uniform `T_tail`
bound are still missing, so `I_gate` cannot be signed.

This means the next productive move is not another broad API reasoning
marathon. The next productive move is an artifact sprint or an honest stop:
produce the endpoint table, prove the table/tail cannot currently be produced,
or quarantine/demote the branch.

## Control Principle

After a blocker signature repeats across a small number of cycles, the branch
must switch out of reasoning mode. Allowed modes are:

- `artifact_sprint`: produce the missing table, bound, proof object, script, or
  certificate.
- `falsifier_sprint`: produce a counterexample, negative interval, or failure
  witness.
- `publication_demotion`: package the bounded negative/support-only result.
- `quarantine`: explicitly stop the branch until new evidence arrives.

Broad API exploration is forbidden while a repeated blocker lacks its named
artifact.

## Physics Reward Investment Gate

Yang-Mills branches should be funded only when they have high physics
conceptual reward: they must plausibly change what a mathematical physicist or
constructive-QFT reader understands about a named physical carrier and a named
Clay-facing gate. A branch is not worth another discovery cycle merely because
it can produce another finite lemma, estimate, symbolic identity, or local
endpoint calculation.

Future YM branch packets must emit a `major_publication_gate`. Only
`invest_high_physics_reward` branches can keep receiving ordinary proof-search
cycles. Branches classified as `reframe_before_investment`,
`do_not_invest_support_only`, or `quarantine_low_physics_reward` must be
demoted, reframed, pivoted, stopped, quarantined, or routed to a named artifact
sprint whose success would unlock a major physics claim.

## YM Endpoint Sprint Target

For the current Route A bottleneck, the target artifact is:

```text
positive-D endpoint source table for the heat-kernel SU(N) three-hairpin block:
source-equivalence classes, D_c, seven log Z_{a,c}(jh) samples, kappa_c
intervals, M8/M_G or root-quartic cap, C_N, cutoff-uniform T_tail, and final
I_gate interval with promote/falsifier/quarantine disposition.
```

## Success Criteria

The workflow improves when future YM cycles can no longer count as progress
merely by saying "compute the endpoint table next." A cycle must either attach
the table/bound, attach a falsifier, or mark the subgoal as artifact-blocked.

The corresponding implementation TODOs live in
`agentic/todos/ym_artifact_or_stop_anti_incrementality_todos.yaml`.
