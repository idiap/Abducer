---
name: diagnose-incident
description: Diagnose a service incident from operator reports and telemetry.
---

Extract attributed operator statements and timestamped telemetry observations.
Propose candidate root-cause hypotheses. Return the hypotheses ranked by
evidential fit, including score, supporting observations, and ties.

Send the ranking and evidence to an independent critic. The critic returns
targeted critiques and undercutting or rebutting defeaters. Produce a root-cause
judgment only after addressing those critiques. Return a remediation decision
and proposed action for explicit operator approval; never execute the action.
