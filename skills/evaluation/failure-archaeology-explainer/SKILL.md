---
name: failure-archaeology-explainer
description: Build a deep post-failure explanation for a major proof or discovery cycle set. Use when a Yang-Mills, mathematical-physics, P vs NP, or other proof-search marathon stalls, fails a hard gate, repeats a blocker, gets demoted/quarantined, or needs to explain why the failed hypothesis was genuinely hard, why it failed, why the failure was not anticipated, and what future hypotheses should learn from it.
---

# Failure Archaeology Explainer

## Purpose

Turn a failed or stalled cycle set into strategic mathematical knowledge. Do not
write a shallow postmortem. Explain the physics and mathematics that made the
problem hard, why the attempted representation or proof pathway failed, and
which warning signs should become future premortem heuristics.

## Mathematical Invariants

Preserve the failed mathematical object while explaining it: source object, target object, carrier, model/theory, transfer interface, quantifiers, hard gate, and claim level. The archaeology should say which invariant failed, which invariant was silently changed, or which invariant was too weak to support the intended theorem.

Required edge cases and counterexamples include toy models, proxy theories, finite/cutoff artifacts, noncommuting limits, hidden compactness or regularity assumptions, prior-art collisions, and examples where the proposed bridge becomes definitional.

## Epistemic Discipline

Every diagnosis must state epistemic status, evidence citation, source artifacts, cycle IDs, explicit unknowns, and validation handoff. Separate genuine mathematical or physical difficulty from prompt/context failure, missing artifact debt, and workflow control failure.

Disconfirming evidence should become a declarative heuristic for future cycles. If a failure cannot teach a route decision, demote it to support-only history rather than turning it into another broad exploration prompt.

## Procedure

1. Identify the failed cycle set:
   - target id, run id, cycle ids, branch ids, branch titles;
   - promoted, demoted, quarantined, repeated-blocker, or artifact-blocked
     status;
   - exact hard gate that did not move.
2. State the smallest honest failed hypothesis:
   - source object;
   - target object;
   - intended bridge or carrier;
   - non-claims.
3. Explain why this was a hard problem:
   - physics hardness: same-theory transfer, gauge invariance, observable
     carrier, continuum/cutoff limit, OS/Wightman reconstruction,
     nontriviality, spectral gap interface, regulator/RG basin, topology, or
     noncommuting limits;
   - mathematical hardness: positivity, compactness, coercivity, uniformity,
     spectral estimates, source derivatives, interval tails, closure
     topology, singular endpoint terms, hidden equivalence classes, or
     definitional circularity;
   - representation hardness: current objects were too weak, too strong,
     fragmented, proxy-like, or missing efficient operations.
4. Explain why it failed:
   - missing artifact, missing theorem, failed sign, failed transfer, failed
     uniformity, wrong carrier, proxy drift, low physics reward, or literature
     displacement;
   - distinguish genuine mathematical difficulty from prompt/context defects.
5. Explain why it was not anticipated:
   - name the misleading local success or analogy;
   - name the absent heuristic that would have flagged the risk;
   - name the evidence that arrived too late.
6. Extract anticipation heuristics:
   - each heuristic must have a declarative failure signature, a prompt
     question, a pre-cycle gate, and the demotion/pivot condition.
7. Emit a disposition:
   - `persist_with_new_artifact_gate`;
   - `reframe_before_investment`;
   - `demote_to_support_only`;
   - `falsifier_or_negative_result`;
   - `quarantine_until_new_evidence`;
   - `stop`.

## Output Contract

Return a `failure_archaeology` object with:

- `cycle_set`
- `failure_detected`
- `smallest_honest_failed_hypothesis`
- `hard_problem_diagnosis`
- `why_failed`
- `why_not_anticipated`
- `anticipation_heuristics`
- `learning_for_future_cycles`
- `required_workflow_change`
- `route_disposition`
- `evidence_paths`
- `validation_handoff`

## Quality Bar

The explanation passes only if a skeptical mathematical physicist can see what
was difficult in the actual field problem. Phrases like "the proof is hard" or
"more work is needed" fail. The packet must name the object, the hard gate, the
failed bridge, the missing evidence, and the next control action.

## Failure/Demotion

Demote the explanation if it gives generic lessons, hides the failed object, omits evidence, fails to name the hard gate, or cannot produce an anticipation heuristic. Quarantine routes whose failure shows low target relevance, definitional transfer, prior-art absorption, or no plausible major publication reward.
