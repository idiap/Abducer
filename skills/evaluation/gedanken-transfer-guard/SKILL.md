---
name: gedanken-transfer-guard
description: Evaluate whether insight from a Gedanken experiment can transfer to the active target without analogy drift, proxy substitution, or proof overclaim. Use before a thought-experiment insight is promoted into a branch decision or follow-up cycle.
---

# Gedanken Transfer Guard

## Conceptual Role

Use this skill to protect the discovery loop from seductive imagined cases. A Gedanken experiment can reveal a mechanism, but transfer to the active target requires a certificate: same object family, same relation type, compatible regime, same-theory map, or a clear statement that the result is only conceptual guidance.

## Functional Generation Requirements

Evaluate transfer against the active target and branch obligation. Name the exact source object in the imagined situation, the exact target object in the branch, and the map or missing map between them. If the map is not available, preserve the insight only as conceptual guidance, graph annotation, queue task, or quarantine.

## Transfer Tests

Check:

- Is the mathematical carrier part of the target theory, a faithful abstraction, or only an analogy?
- Are source and target variables typed in the same way?
- Does the validity regime match the branch obligation?
- Does the expected observation correspond to a target observable or proof obligation?
- What exactly transfers, what does not transfer, and what follow-up artifact could certify it?

## Mathematical Invariants

- Mathematical object: Gedanken packet, target branch, source carrier, target object, and transfer certificate.
- Preserved invariants: same-theory map, typed variables, regime compatibility, explicit non-claims, and evidence paths.
- Broken invariants: proxy object, analogy-only transfer, proof claim without derivation, or hidden regime shift.
- Edge case or counterexample: a transfer is rejected if an equally plausible variant changes the conclusion outside the target regime.

## Epistemic Discipline

Assign epistemic status: `transfer_ready`, `needs_certificate`, `conceptual_only`, `quarantine`, `invalidated`, or `proof_obligation`. Cite packet IDs, source artifacts, qualitative graph edges, KB IDs, cycle IDs, equations, validators, or explicit unknowns. Do not promote thought-experiment insight as theorem progress.

Use `graph_update_action` conservatively. `annotate_edge` and `needs_probe` are normal for conceptual probes, `challenge_edge` or `revise_edge` require a diagnostic variant or failed transfer certificate, `quarantine` is required for analogy-only transfer, and `none` is required when no graph edge is typed.

## Output Contract

Return:

1. `Transfer Verdict`: ready, needs certificate, conceptual only, quarantine, or invalidated.
2. `What Transfers`: mechanism, relation shape, falsifier, variable dependence, or follow-up task.
3. `What Does Not Transfer`: numerical value, proof status, continuum claim, target existence, or same-theory result.
4. `Certificate Needed`: artifact, derivation, computation, prior-art source, or validator.
5. `Graph Update Action`: one of `none`, `needs_probe`, `challenge_edge`, `revise_edge`, `annotate_edge`, or `quarantine`.
6. `Affected Branch Decision`: continue, adapt, backtrack, quarantine, or stop candidate.
7. `Validation Handoff`: packet validator, qualitative graph update, or next-experiment queue item.

## Failure/Demotion

Demote when the carrier is a proxy, the target observable is missing, regimes differ, variables are not aligned, or the situation has no disconfirming variant. Quarantine analogy-only insights until a transfer certificate exists. Reject any claim that the Gedanken experiment proves the target.

## Validation Handoff

Use `python agentic/scripts/validate_gedanken_experiment_packets.py` for packet integrity and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` when a transferred insight updates graph edges.
