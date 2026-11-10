---
name: paper-contribution-readiness-judge
description: Assess whether a current Abducer subgoal is close to a paper-level scientific contribution. Use when a discovery branch, obstruction, bridge lemma, qualitative mechanism, finite probe, literature synthesis, or workflow method might stand as an independent result and needs evaluation for novelty, explanatory power, implications, validation burden, and paper packaging readiness.
---

# Paper Contribution Readiness Judge

## Workflow

Treat paper readiness as a scientific-content judgement, not as a score alone.

1. Name the smallest honest contribution claim.
2. Identify the contribution type: theorem/lemma, obstruction, finite falsifier, calculational method, conceptual reframing, benchmark/probe, literature synthesis, or workflow method.
3. Compare it against the target problem and historical development:
   - What known bottleneck does it address?
   - Why is the result not merely an internal workflow artifact?
   - What prior route or conceptual ambiguity does it clarify?
4. Evaluate readiness dimensions from 0 to 5:
   - `conceptual_novelty`
   - `technical_depth`
   - `explanatory_power`
   - `target_alignment`
   - `validation_readiness`
   - `paper_packaging_readiness`
5. Evaluate good-enough paper relevance markers:
   - `conceptual_depth`: whether the candidate reaches a core proof obligation or conceptual pressure point.
   - `conceptual_novelty`: whether the contribution is new relative to adjacent literature or known route families.
   - `unblocking_power`: whether it changes a concrete continue/adapt/backtrack/pivot/handoff decision.
   - `applicability`: whether it is reusable across a meaningful family of cases, models, carriers, or abstractions.
   - `understanding_gain`: whether it explains why the problem or route is hard, where proof debt moves, or which obstruction binds.
6. State the missing work required to turn it into a paper section, note, or standalone argument.

For P vs NP, a good enough paper relevance judgement must be complexity-theoretic: name source carrier or language, target class, circuit model, transfer inequality, quantifier regime, and barrier/nonuniformity status when they are part of the claim. Generic statements about "progress toward P vs NP" are not enough.

## Paper-Level Threshold

A subgoal is paper-level only when it can be stated without overclaiming the main theorem and still teaches something externally useful.

It must have:

- A precise object and claim.
- Explicit assumptions and validity regime.
- A proof sketch, computation, falsifier, or empirical/source-backed evidence packet.
- A novelty boundary against the literature.
- A clear implication for the main problem or a reusable neighboring problem.
- A finite validation plan.

## Mathematical Invariants

Preserve the contribution's mathematical object, definitions, assumptions, validity regime, and carrier. If the claim depends on a finite matrix, quotient, kernel, estimate, simulation, analogy, or empirical source, state which invariant makes it relevant outside that local setting.

Check edge case and counterexample pressure before promotion: fixed-regulator artifacts, empty limits, proxy theory shifts, vacuous assumptions, unbounded constants, and literature rediscovery.

## Output Contract

Return:

- `candidate_title`
- `smallest_honest_claim`
- `paper_contribution_type`
- `readiness_level`: not_ready, developing, near_paper_note, paper_note_ready, or paper_argument_ready.
- `dimension_scores`
- `paper_relevance_markers`: conceptual depth, conceptual novelty, unblocking power, applicability, understanding gain.
- `good_enough_paper_relevance`: paper_relevance_ready, strong_relevance_certification_pending, moderate_relevance_needs_sharpening, or weak_relevance.
- `novelty_argument`
- `explanatory_power`
- `main_problem_implication`
- `validation_burden`
- `overclaim_boundary`
- `paper_skeleton`: title, abstract claim, core sections, decisive figures/tables/equations, and open caveats.

## Epistemic Discipline

Do not call a subgoal paper-ready just because it is interesting. Paper readiness requires bounded validation and a crisp smallest honest claim.

Do not require solving the main problem. Many valuable contributions are bridge lemmas, obstructions, falsifiers, or conceptual mechanisms that reduce future uncertainty.

State epistemic status as not-ready, conjectural, proof-obligation, promoted, blocked, or validation-needed. Cite source artifacts, cycle IDs, report paths, KB IDs, literature references, and explicit unknowns.

## Failure/Demotion

Reject, demote, or quarantine a paper-readiness claim when novelty is unsupported, the mathematical object is unstable, the proof sketch has no validator, the result only repackages workflow bookkeeping, or the overclaim boundary cannot protect the main theorem.

A candidate can still be developing when it has a bounded next action, a named validation handoff, and a clear failure regime that has not yet falsified it.
