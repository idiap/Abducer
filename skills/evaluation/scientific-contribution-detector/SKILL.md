---
name: scientific-contribution-detector
description: Identify whether a completed or nearly completed subgoal is a standalone scientific contribution candidate. Use when a discovery loop, report, milestone archive, or branch review needs to decide whether a result is independently publishable as a bridge lemma, obstruction, method, benchmark, negative result, conceptual reframing, or reusable evidence packet even if the main target remains open.
---

# Scientific Contribution Detector

## Conceptual Role

Use this skill to detect contribution-shaped subgoals inside a long-horizon discovery process. A contribution candidate is a completed or bounded subresult that could matter to another scientist without requiring the entire target theorem to be solved.

Candidate contribution types include:

- `bridge_lemma`: a reusable implication, transfer theorem, or typed interface.
- `obstruction_or_falsifier`: a negative result, counterexample class, impossibility pressure, or demotion criterion.
- `method_or_workflow`: a reusable reasoning, validation, or exploration method with clear scope.
- `conceptual_reframing`: a new abstraction or explanatory decomposition that changes what the problem is.
- `benchmark_or_probe`: a controlled finite, symbolic, empirical, or Gedanken probe with reusable diagnostic value.
- `evidence_synthesis`: a source-backed packet that changes what is plausible, ruled out, or worth testing.

## Detection Procedure

1. Name the subgoal and its mathematical object: theorem fragment, bridge object, obstruction, finite carrier, method, dataset/probe, or explanatory model.
2. Separate completion status from contribution status. A subgoal can be contribution-shaped while still blocked; it becomes a stronger candidate only when its scope, evidence, and limits are clear.
3. Ask whether the result is independently useful:
   - Does it clarify a previously opaque mechanism?
   - Does it rule out a tempting but wrong route?
   - Does it create a reusable test, criterion, or abstraction?
   - Does it transfer beyond one cycle while preserving target-specific assumptions?
4. Identify the smallest paper claim it could support without overclaiming.
5. State disqualifiers: hidden premise shift, proxy problem, already-known result, missing evidence, unverifiable novelty, or no implications beyond local bookkeeping.

## Publishable Stepping-Stone Maturity

Do not collapse "interesting" into "publishable." Use three maturity levels:

- `contribution_shaped`: an independently meaningful object or obstruction has been named, but it is not yet a paper-level stepping stone.
- `near_stepping_stone`: one or two bounded tasks could make the result paper-note ready, such as a proof skeleton, prior-art boundary, disqualifier check, or finite validation.
- `publishable_handoff_ready`: broad exploration should pause; the candidate has a claim statement, evidence, novelty boundary, validation/disqualifier checks, overclaim boundary, and paper-note shape.

Publishable handoff requires five hard gates:

1. `claim_statement_ready`
2. `evidence_ready`
3. `novelty_boundary_ready`
4. `validation_ready`
5. `overclaim_boundary_ready`

Prior-art unknowns, target-equivalent assumptions, proxy drift, advice leakage, unbounded validation, or missing disqualifier tests demote a candidate to `near_stepping_stone` or lower.

## Good-Enough Paper Relevance Markers

Before calling a candidate a good enough paper subgoal, assess five relevance markers. These markers are content-specific and must be expressed in the target problem's own language.

- `conceptual_depth`: the candidate acts on a deep target commitment, not a surface analogy.
- `conceptual_novelty`: the candidate adds a new obstruction, bridge, exact threshold, certificate interface, worked calculation, or explanatory decomposition relative to nearby literature.
- `unblocking_power`: the candidate changes what the next proof/research move should be; it can promote, adapt, backtrack, pivot, quarantine, or hand off a branch.
- `applicability`: the candidate applies beyond one local cycle under named assumptions, models, carriers, or validity regimes.
- `understanding_gain`: the candidate explains why a route is hard, where proof debt moves, or which barrier/transfer condition actually binds.

For P vs NP, express these markers through source carriers/languages, target complexity classes, circuit models, transfer inequalities, quantifier regimes, advice/nonuniformity leakage, hardness magnification, MCSP/MKtP, proof-complexity bridges, natural proofs, relativization, and algebrization. A P vs NP candidate is paper-relevant only when it says more than "this route is promising": it must name what exact transfer, obstruction, no-go, or certificate bridge would change the field's understanding.

## Mathematical Invariants

- Mathematical object: subgoal, carrier, bridge, obstruction, method, probe, or explanation under contribution assessment.
- Preserved invariants: source object, target object, assumptions, scope, validation status, and same-theory boundaries.
- Broken invariants: contribution claim changes the problem, drops essential assumptions, hides proof debt, or treats workflow success as scientific novelty.
- Edge case or counterexample: test whether the claimed contribution still matters under boundary regimes, negative examples, known prior art, and target-preserving variants.

## Epistemic Discipline

Assign epistemic status: `candidate`, `evidence_backed_candidate`, `near_complete`, `certified_contribution`, `blocked_contribution`, `prior_art_risk`, `proxy_risk`, or `quarantine`.

Every contribution claim must cite evidence: KB IDs, cycle IDs, equations, dependency nodes, report artifacts, validation outputs, source artifacts, or explicit unknowns. Novelty is always provisional until prior-art risk is checked.

## Output Contract

Return:

1. `Subgoal`: name, contribution type, mathematical object, source cycles, and current status.
2. `Smallest Honest Claim`: the minimal scientific claim the subgoal could support.
3. `Why It Could Stand Alone`: independent usefulness, audience, reusable object, and target relation.
4. `Evidence Basis`: artifacts, equations, cycles, validators, sources, or explicit unknowns.
5. `Stepping-Stone Maturity`: contribution_shaped, near_stepping_stone, or publishable_handoff_ready.
6. `Hard Gates`: readiness and evidence for claim, evidence, novelty boundary, validation, and overclaim boundary.
7. `Disqualifiers`: prior-art, proxy drift, target-equivalent assumption, missing validation, hidden premise, boundary regime, or overclaiming risks.
8. `Paper Relevance Markers`: conceptual depth, conceptual novelty, unblocking power, applicability, and understanding gain, each with target-specific evidence and missing work.
9. `Certification Path`: what would promote the candidate to a publishable stepping stone.
10. `Paper Note Shape`: title, theorem/result statement, definitions, proof plan, limitations, and validation artifacts.
11. `Validation Handoff`: validator, report, TODO, source search, paper draft, or stop/quarantine condition.

## Failure/Demotion

Demote or quarantine when the candidate cannot name a mathematical object, has no evidence citation, only restates local workflow progress, lacks implications beyond the current run, or depends on an unacknowledged shift to a weaker problem.

## Validation Handoff

Use `python agentic/scripts/build_scientific_contribution_monitor.py` and `python agentic/scripts/validate_scientific_contribution_monitor.py` after adding or changing contribution candidates.
