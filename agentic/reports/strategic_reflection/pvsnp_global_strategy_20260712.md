<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Global Strategic Reflection

- Generated UTC: 2026-07-12T11:40:32Z
- Target: `p-vs-np-target`
- Current decision: `restrategize_to_proof_convergence`
- Scope: current P vs NP marathon, proof-delivery queue, inference-quality gate, and paper project

## Evidence Surfaces

- Latest proof queue: `agentic/reports/pvsnp_proof_delivery_queue/latest.md`
- Inference-quality status: `agentic/reports/pvsnp_inference_quality/latest.md`
- Result-refinement packet: `agentic/reports/results_ellaboration/p-vs-np-transfer-obstruction-certificate/latest.md`
- Enriched draft: `agentic/reports/paper_projects/p-vs-np-transfer-obstruction-certificate/parity_magnification_full_row_barrier/parity_magnification_full_row_barrier_semantic_links.tex`
- Latest focused cycles: `agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0085.json`, `agentic/runs/discovery_marathons/p-vs-np-marathon/cycles/cycle-0086.json`

## Current Scientific State

The project has moved from broad P vs NP exploration into a narrower and more valuable paper-shaped subproblem: route-specific transfer obstruction for hardness-magnification style approaches, especially the beta-zero parity carrier and formula-semantic extraction fork.

The strongest current contribution candidate is not a proof of P != NP and not a SAT lower bound. It is a scoped obstruction and classification framework:

1. Transfer envelopes explain why a source lower bound of the form `SIZE(H_N) > N^a` only rules out target circuits of exponent `c` when the transfer inequality satisfies `a > q + beta c`.
2. Positive `beta` creates a bounded-window obstruction rather than an all-exponent separation.
3. The beta-zero parity/full-row route gives a sharper finite obstruction for occurrence-local or functional-row-local certificates.
4. Formula-semantic proof systems remain the decisive open region: a strong proof may exploit real SAT syntax, equality, padding, self-reduction, or extensionality in ways not captured by raw occurrence labels.

This is real progress because the problem has been transformed from a diffuse "find a P vs NP route" search into a finite set of theorem-shaped gates: compute the transfer envelope, prove or refute extraction, audit advice and quantifiers, and isolate the first semantic rule that escapes occurrence/full-row accounting.

## What Has Genuinely Shifted

### 1. The target is no longer broad exploration

The old mode treated many branches as plausible discovery avenues. The current artifacts show that this is now too loose. The proof-delivery queue already identifies a highest-priority target: resolve the formula-semantic extraction fork. Broad marathons are now useful only if they discharge that queue, not if they add more adjacent narratives.

### 2. The main value is a publishable subgoal, not the global separation

The plausible paper contribution is a route-classification or obstruction result. It can be valuable if it cleanly states:

- which bridge routes lose all-exponent strength;
- which occurrence-local proof certificates must pay full-row cost;
- which SAT-semantic mechanisms remain outside the obstruction;
- exactly what a successful nonrelativizing route must use.

That is a paper-grade stepping stone if the proof chain and prior-art boundary are clean. It is not yet a full paper claim until the live inference-quality packet and prior-art comparison are completed.

### 3. The hard problem has localized into semantic extraction

The technical pressure is now precise. Occurrence-only reasoning breaks for systems with explicit equality or semantic rules. The repaired invariant is semantic row support or witnessed-extensionality cover. The next strategic question is not "can this route work?" but:

Can every relevant proof-system rule be charged to a bounded row-support or cover object, or is there a named SAT-semantic principle that fundamentally escapes that accounting?

That question is finite enough to attack.

## What Has Not Yet Shifted

### 1. There is still no live inference-quality packet

The inference-quality report says `live_packet_count: 0`. This blocks promotion. The next theorem-shaped claim must produce a live packet with source statement, target statement, model context, quantifier regime, transfer direction, advice status, derivation status, and reviewer findings.

### 2. Full EF+SAT_U remains outside the proved scope

The enriched draft is stronger than before, but it still preserves the correct boundary: occurrence-local and witnessed fragments can be audited; full SAT-semantic proof systems may escape unless a parser/extraction theorem is proved or a nonrelativizing semantic principle is named.

### 3. Prior-art boundary is not closed

The result-refinement packet still says nearest-work comparison is incomplete. That prevents strong novelty language. The comparison must be exact, not broad: hardness magnification, MCSP/MKtP, natural proofs, relativization, algebrization, proof complexity, and EF/reflection routes must be checked against the actual hypotheses.

## Strategic Diagnosis

The project is at risk of two opposite failures:

1. Under-claiming: leaving a meaningful scoped obstruction as an internal report instead of turning it into a clear theorem packet and paper narrative.
2. Over-claiming: presenting the scoped obstruction as P vs NP progress without proving formula-semantic extraction, a source lower bound, or full proof-system consequences.

The right move is proof-convergence mode. The next cycles should not explore new conceptual families unless they directly serve one of the proof-convergence gates below.

## Restrategy

### New operating mode: proof-convergence over broad discovery

Until the gates below are discharged, every P vs NP run should select from this ordered agenda:

1. **Formula-semantic extraction fork.**
   Fix one concrete proof-system fragment, such as an equality fragment, witnessed-extensionality fragment, or EF+SAT_U occurrence fragment. Prove extraction, prove a countermodel, or name the exact semantic principle that escapes row-support accounting.

2. **Proof-chain audit of the existing draft.**
   Treat the beta-zero transfer, sparse-row patching, naturalization, row-forcing, parity full-row, parser-to-query, semantic-link, and witnessed-extensionality arguments as a dependency graph. Every theorem must have definitions, hypotheses, proof dependencies, non-claims, and barrier status.

3. **Live inference-quality packet.**
   Emit the first live packet for the actual theorem candidate. No promotion until the packet exists and passes validation.

4. **Prior-art and novelty boundary.**
   Compare the exact theorem statement against known magnification and meta-complexity lines. The output must say whether the result is novel, partially known, known under different terminology, or not claimable.

5. **Paper narrative repair.**
   Convert the result into a clean paper spine: problem pressure, transfer-envelope obstruction, beta-zero/full-row barrier, formula-semantic fork, semantic-link repair, witnessed-extensionality cover, non-claims, and next theorem obligations.

### Branch control

Continue a branch only if it names:

- a concrete source object, target object, proof system, and lower-bound sentence;
- the exact extraction map, semantic support object, or transfer inequality being proved;
- the reviewer gate that will certify or demote it.

Backtrack if:

- it repeats the formula-semantic fork without choosing a proof-system fragment;
- it treats occurrence-label reasoning as full SAT semantics;
- it hides advice, nonuniformity, or valid-length restrictions;
- it says "barrier" without identifying the branch-specific mechanism.

Pivot only if:

- a concrete fragment fails by a minimal countermodel;
- a prior-art check shows the theorem is already known;
- a named semantic rule demonstrably escapes row-support accounting and becomes the better paper contribution.

Do not pivot merely because the formula-semantic problem is hard. That is now the central problem.

## Decisive Next Work

The next run should not be a generic one-hour marathon. It should be a constrained proof-delivery run with this prompt-level target:

> Work on `pvsnp.paper.formula-semantic-extraction-open-problem`. Choose one concrete fragment, preferably `EF+SAT_U^{occ}` plus explicit `EqSAT` or witnessed extensionality. Define the proof syntax, allowed SAT facts, transcript parser, semantic row-support or witness-cover object, and prove one theorem: extraction succeeds with a quantitative bound, or extraction fails by a minimal named semantic rule. Emit a live `pvsnp_inference_quality` packet.

The first acceptable output is not another narrative. It is one of:

- `scoped_extraction_theorem_ready`;
- `minimal_countermodel_found`;
- `semantic_escape_principle_identified`;
- `blocked_at_named_lemma_with_counterexample_search_target`.

## Paper-Readiness Judgment

Current readiness: `promising_but_not_yet_publishable_as_a_strong_claim`.

It may already be enough for a scoped research note after repairs, but not for a strong paper until:

- the theorem chain is audited;
- one live inference-quality packet exists;
- novelty is checked against nearest work;
- the formula-semantic open problem is either advanced or honestly framed as the main remaining boundary.

The most honest near-term paper title would be close to:

> Transfer-envelope obstructions and semantic certificate gates for P vs NP hardness-magnification routes

The paper should not claim separation progress. It should claim a route-control theorem and a precise semantic obstruction map.

## Validation Handoff

Run or produce:

- `agentic/scripts/validate_pvsnp_proof_delivery_queue.py`
- `agentic/scripts/validate_pvsnp_inference_quality.py`
- `agentic/scripts/validate_pvsnp_result_refinement_packet.py`
- a live theorem packet under `agentic/reports/pvsnp_inference_quality/live/`
- a proof-chain dependency audit for the enriched draft
