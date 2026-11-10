---
name: main-problem-alignment-auditor
description: Audit whether current Abducer strategies, subgoals, equations, probes, analogies, and contribution candidates remain aligned with the main target problem. Use during marathon reports, strategy evaluation, pivot decisions, paper-contribution assessment, or whenever a branch risks becoming a proxy problem, finite-regulator artifact, analogy without transfer, or workflow-only result.
---

# Main Problem Alignment Auditor

## Workflow

Check whether a strategy still touches the target problem in the same theory and with the right commitments.

1. Extract the target commitments from the problem statement and literature evolution.
2. For the active branch, name:
   - source object,
   - target object,
   - transfer map or reconstruction map,
   - assumptions,
   - validation handoff,
   - falsifiers.
3. Decide whether the branch is:
   - `directly_aligned`: acts on a core target commitment.
   - `bridge_aligned`: acts on a required transfer/reconstruction obligation.
   - `proxy_aligned`: useful only with an explicit transfer certificate.
   - `method_aligned`: improves discovery control but is not itself target evidence.
   - `drifting`: cannot state a target-preserving handoff.
4. State exactly what would restore or strengthen alignment.

## Alignment Tests

Use problem-specific language. For Yang-Mills, typical commitments include same-theory continuum construction, gauge-invariant observables, reflection positivity or equivalent reconstruction, nontriviality, physical Hilbert space, vacuum, Hamiltonian, and positive spectral gap. For other targets, replace these with the target's own commitments.

Ask:

- Does the branch preserve the target's objects, not merely a toy proxy?
- Does the branch name which theorem, estimate, obstruction, or construction it would feed?
- Does it avoid fixed-cutoff, finite-volume, or analogy-only claims unless those have transfer conditions?
- Does the next action have a validation handoff into the main proof architecture?
- Does the branch clarify a route even when it fails?
- If the branch claims paper relevance, does it improve conceptual depth, novelty, unblocking power, applicability, or understanding of the main problem rather than only improving internal workflow state?

## Mathematical Invariants

Preserve the main problem's mathematical objects, definitions, target commitments, quantifiers, regimes, and source-to-target handoffs. Alignment is broken when a proof route changes carrier, regulator, observable algebra, topology, semantics, or theory without a transfer map.

Treat edge cases and counterexamples as alignment evidence: fixed-cutoff success, finite-volume artifacts, analogy-only transfer, vacuous solution criteria, and proxy constructions can all falsify alignment.

## Output Contract

Return:

- `alignment_class`
- `target_commitments_touched`
- `source_to_target_handoff`
- `proxy_or_transfer_risk`
- `alignment_gain`
- `alignment_loss`
- `repair_action`
- `decision_effect`: how this should change priority, stop criteria, or paper-readiness judgement.

## Epistemic Discipline

Never punish legitimate bridge work for not being the final theorem. A bridge can be highly aligned if it is a necessary transfer obligation.

Never accept a beautiful calculation as aligned unless it says how it enters the target problem.

State epistemic status as directly aligned, bridge aligned, proxy aligned, method aligned, drifting, blocked, promoted, or validation-needed. Cite evidence from source artifacts, report paths, cycle IDs, KB IDs, literature references, and explicit unknowns.

## Failure/Demotion

Demote, quarantine, backtrack, or pivot when the branch cannot name a source object, target object, transfer condition, validation handoff, or falsifier. Do not demote solely because the branch is intermediate; demote because the handoff to the main target is absent or refuted.
