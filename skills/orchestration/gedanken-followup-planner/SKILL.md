---
name: gedanken-followup-planner
description: Convert accepted Gedanken experiment insights into concrete follow-up discovery-cycle tasks, ranked queue items, graph updates, or branch-control decisions. Use after a thought experiment has passed transfer guarding and needs to affect the workflow.
---

# Gedanken Follow-Up Planner

## Conceptual Role

Use this skill to make Gedanken experiments operational. The output is not a story; it is a follow-up plan that tells the discovery loop what to derive, compute, falsify, formalize, search, update, backtrack, quarantine, or rank next.

## Functional Generation Requirements

Convert the packet into an executable next move. A valid follow-up must name the branch, packet, transfer verdict, required skills, success criterion, demotion criterion, artifact to update, and validation command. If the packet is conceptual-only, the follow-up should request a certificate, falsifier, or graph annotation rather than proof promotion.

## Guardrails

- Do not let a thought experiment bypass branch validators.
- Do not promote conceptual insight to proof progress.
- Do not create follow-up tasks without success and demotion criteria.
- Do not stop a branch if the Gedanken experiment newly sharpens variables, regimes, mechanisms, or falsifiers.
- Do not continue a branch solely because the story is elegant.

## Planning Procedure

1. Read the packet, transfer verdict, active branch, and qualitative graph edge.
2. Select the next action: derive, compute, falsify, formalize, search prior art, update graph, rank next experiment, backtrack, or quarantine.
3. State success, failure, demotion, and anti-drift criteria.
4. Attach required skills and validators.
5. Emit queue-ready fields: `packet_id`, `situation_title`, `transfer_verdict`, `success_criterion`, `failure_or_demotion_criterion`, and `required_skills`.
6. Decide whether the task should enter the ranked next-experiment queue or immediately backtrack/quarantine a branch.

## Epistemic Discipline

Assign an explicit epistemic status to each follow-up task: `ready_to_run`, `needs_certificate`, `conceptual_only`, `proof_obligation`, `evidence_task`, `backtrack`, or `quarantine`. Cite packet IDs, source artifacts, cycle IDs, qualitative graph edges, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the plan. Run `python agentic/scripts/validate_gedanken_experiment_packets.py` after packet changes. Run `python agentic/scripts/generate_discovery_marathon_html.py` and `python agentic/scripts/validate_discovery_marathon_report.py` after queue/report integration changes.

## Output Contract

Return:

1. `Follow-Up Queue Items`: action, description, packet ID, target branch, and priority rationale.
2. `Success Criteria`: what result would promote or persist/adapt.
3. `Failure/Demotion Criteria`: what result would backtrack, quarantine, or stop after repeat low payoff.
4. `Required Skills`: skill sequence and why.
5. `Queue Provenance`: `packet_id`, `situation_title`, `transfer_verdict`, originating cycle ID, originating branch ID, and affected graph edge when available.
6. `Graph/Packet Updates`: relation edge or packet artifact to update.
7. `Branch Control`: continue, adapt, backtrack, quarantine, watch/archive, or stop candidate.
8. `Validation Handoff`: exact report or validator.

## Failure/Demotion

Demote plans that lack criteria, do not reference a packet, cannot affect a branch decision, or use the thought experiment as proof. Quarantine tasks when transfer guard says the insight is analogy-only. Falsify the plan if validators reject packet shape or report queue criteria.

## Validation Handoff

The handoff is the ranked next-experiment queue, `agentic/reports/gedanken_experiments/latest.json`, and the validators `python agentic/scripts/validate_gedanken_experiment_packets.py` plus `python agentic/scripts/validate_discovery_marathon_report.py` when queue ranking changes.
