<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Gedanken Experiment Workflow

Gedanken experiments in Abducer are controlled conceptual probes. They are used when a branch has a real conceptual blocker and an imagined concrete situation can isolate a variable, mechanism, validity regime, counterfactual contrast, or transfer boundary. They are not proof artifacts and they are not generic brainstorming.

## Workflow Slot

The normal slot is after qualitative physics reasoning has typed the relevant quantities and before falsifier generation, contradiction routing, or branch promotion. A good packet starts from the current branch, qualitative graph edge, blocking gap, and next-experiment queue context.

The loop is:

1. `gedanken-need-assessor` decides whether to design now, run a concrete probe first, defer until variables or regimes are typed, quarantine as analogy, or mark the move not needed.
2. `gedanken-situation-designer` builds a minimal imagined situation with variables, held-fixed controls, interventions, expected observations, disconfirming observations, transfer scope, and graph linkage.
3. `gedanken-counterfactual-variant-builder` changes one condition at a time and checks whether the expected observation reverses, disappears, delays, or becomes ambiguous.
4. `gedanken-transfer-guard` decides what transfers, what does not transfer, and which certificate is needed before any insight affects proof obligations.
5. `gedanken-followup-planner` emits ranked next-experiment queue items, graph annotations, branch-control advice, or quarantine actions.

## Invocation Decisions

Use `design_now` when at least two positive criteria hold: the mechanism is opaque, variables or regimes can be typed locally, a controlled contrast can separate competing explanations, the expected observation would alter a next-cycle action, and transfer can be guarded by a certificate.

Use `run_concrete_probe_first` when a small derivation, computation, source check, or toy model would be more informative than imagining a situation.

Use `defer_until_variable_typed` or `defer_until_regime_typed` when the imagined situation would merely conceal missing definitions.

Use `quarantine_as_analogy` when the situation is interesting but cannot state a same-target transfer path.

Use `not_needed` when ordinary deduction, the qualitative graph, or existing evidence already determines the next action.

## Packet Requirements

Every packet must include:

- `need_assessment` with `decision`, `criteria_met`, `criteria_missing`, `rejected_alternatives`, and `why_not_direct_derivation_or_probe`.
- `originating_cycle_ids` and `originating_branch_ids`.
- Variables, controls, interventions, observations, variants, transfer scope, and follow-up tasks.
- `affected_node_ids`, `affected_edge_ids`, `graph_update_action`, and `proposed_graph_updates` when graph learning is intended.
- Queue-ready follow-up fields: `packet_id`, `situation_title`, `transfer_verdict`, `success_criterion`, `failure_or_demotion_criterion`, and `required_skills`.

## Anti-Overclaim Rules

A thought experiment may reveal a mechanism, falsifier, contrast, or transfer boundary. It does not prove the target. Promotion requires a later derivation, computation, source-backed certificate, or validator-backed graph update.

Conceptual probes normally use graph actions such as `annotate_edge` or `needs_probe`. Use `challenge_edge` or `revise_edge` only when a diagnostic variant or failed transfer certificate warrants it. Use `quarantine` for analogy-only packets. Use `none` when no graph edge has been typed.

## Reports And Commands

Build and validate packets:

```bash
python agentic/scripts/build_gedanken_experiment_packets.py --target yang-mills-existence-and-mass-gap-target
python agentic/scripts/validate_gedanken_experiment_packets.py
```

Build and validate the graph/report integration:

```bash
python agentic/scripts/build_qualitative_mechanistic_graph.py --target yang-mills-existence-and-mass-gap-target
python agentic/scripts/validate_qualitative_mechanistic_graph.py
python agentic/scripts/generate_discovery_marathon_html.py
python agentic/scripts/validate_discovery_marathon_report.py
```

Run the full gate:

```bash
python agentic/scripts/agentic_check.py
```

Visible artifacts:

- `agentic/spec/gedanken_experiment_packet.schema.json`
- `agentic/reports/gedanken_experiments/latest.json`
- `agentic/reports/gedanken_experiments/latest.md`
- `agentic/reports/discovery_marathon/full_timeline.html`
- `agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json`
