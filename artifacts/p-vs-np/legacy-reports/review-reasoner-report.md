# Review Reasoner Report

- KB ref: p-vs-np
- Date: 2026-03-17
- Review mode: code-first, state-aware
- Reviewer stack: epistemologist of mathematical discovery; Fields Medalist mathematician; DeepMind-style mathematical discovery scientist; concept-discovery logician; radical systems designer

## Findings

### 1. The live state is not globally consistent, which weakens all higher-level governance.

Severity: critical

Evidence:

- `proof-queue.md` reports `Pending: 6` and `In progress: 1`.
- `proof-cycle-summary.md` simultaneously reports `Pending queue items: 0` and `In progress: 0`.

Why this matters:

- The system has no trustworthy single frontier.
- Any score, meta reflection, stop rule, or expert-facing report built on stale summaries can misstate the real research state.
- The work loop can appear more settled than the queue actually is.

Interpretation:

- The platform has strong persistence objects, but not yet a global consistency contract across derived artifacts.
- This is not just a reporting defect; it is an epistemic defect because stop/continue judgments depend on derived state.

### 2. Discovery branch execution is still mostly descriptive rather than generative.

Severity: critical

Evidence:

- `execute_discovery_branches.py` builds reports with status `completed-local-pass`.
- The execution report is composed from linked queue items, InformalMathLib hits, candidate claims, required questions, and stop criteria, but it does not actually synthesize new theorem objects, revise concepts, or discharge branch-local obligations.

Why this matters:

- The system now has branch routing, branch dossiers, and branch executions, but the execution layer still mainly records what the branch should think about.
- That creates a risk of confusing better orchestration with deeper discovery.

Interpretation:

- The discovery process is mature as governance and bookkeeping.
- It is not yet mature as branch-local concept formation or theorem invention.

### 3. The prove cycle remains a scaffold constructor more than an autonomous proof engine.

Severity: critical

Evidence:

- `start_proof_cycle.py` creates a dossier with a tactic playbook, tactic trace, blank stepwise argument slots, pending judges, and `final_assessment.outcome = "in_progress"`.
- The prove phase is rich in structure, but the mathematical content is still expected to be supplied afterwards.

Why this matters:

- The system is excellent at defining what a proof attempt should contain.
- It is still weak at actually generating or refining the proof itself under that structure.

Interpretation:

- The reasoner has implemented proof governance and proof audit discipline.
- It has not yet implemented strong proof production.

### 4. The plausibility score is too generous relative to the available mathematical evidence.

Severity: high

Evidence:

- `end-to-end-proof-plausibility.md` reports `Plausibility score: 0.594`.
- The same report also reports `Evidence count: 0`, `Proved results: 0`, and `Blocked results: 24`.
- In `end_to_end_plausibility.py`, the adversarial-pressure critic assigns a nontrivial score once blocking results exist, and the overall normalized score is an average over architecture-level critics, not a proof-evidence-weighted posterior.

Why this matters:

- A score near `0.6` can be read as meaningful progress toward proof, even when there is no terminal proved attempt and no evidence count.
- The current critic is better viewed as a route-organization score than a proof-likelihood score.

Interpretation:

- The critic is useful for programme maturity.
- It is not yet calibrated for truth-tracking mathematical plausibility.

### 5. InformalMathLib currently functions more as a prior-art cache than as the system's own learned theorem memory.

Severity: high

Evidence:

- `InformalMathLib/p-vs-np/catalog.md` reports `Positive results: 0`, `Negative or blocking results: 0`, and `External references: 8`.
- `proof-cycle-summary.md` reports `Blocked negative findings: 24`.

Why this matters:

- The system has learned many route obstructions, but those obstructions are not materialized in InformalMathLib as durable local mathematical memory.
- As a result, the platform imports the literature better than it consolidates its own negative knowledge.

Interpretation:

- Persistent memory exists, but internal theorem learning is weaker than external reference accumulation.

### 6. The best new queue items are still mathematically schematic at the exact point where an expert needs specificity.

Severity: high

Evidence:

- `proofq.p-vs-np.032` is the top live item, but its claim is still of the form: “If source theorem S holds in regime R, then one can construct an explicit carrier C ... preserving invariant I ... to target T.”
- Several branch-promoted queue items use placeholders `S`, `R`, `C`, `I`, `T`, `G`, `L`, `W`, `B`, `D`, `P`, `Q`.

Why this matters:

- This is good as a search-program description.
- It is not yet acceptable as an expert-facing mathematical conjecture.

Interpretation:

- The discovery layer is producing theorem-shaped placeholders rather than theorem-level mathematical statements.

## Perspective Reviews

### 1. Epistemologist Of Mathematical Discovery

What the reasoner is actually doing well:

- It has real assertion-licensing machinery in `statement_text.py`.
- It persists queues, branches, logs, InformalMathLib, and work state instead of forgetting what happened.
- It treats failure as informative and makes blocked routes first-class.

What it overclaims:

- Discovery branch execution sounds like discovery progress, but is still mostly structured reframing.
- The plausibility score sounds epistemic, but is still heavily a coherence/programme score.

Most serious missing mechanism:

- A repository-wide claim-status ledger tying every active claim to one of: grounded, conjectural, blocked, imported prior art, disproved, or merely organizational.

Failure mode:

- The system may mistake richer control structure for deeper knowledge acquisition.

Recommendation:

- Add a consistency-checked epistemic-status ledger and downgrade every surface that is not directly evidence-bearing.

### 2. Fields Medalist Mathematician

What the reasoner is actually doing well:

- It has correctly localized the major live burdens: carrier realization, formula-size transport, target alignment, semantic bridge, explicitness, and constructive instantiation.
- The negative results are more informative than the positive route rhetoric.
- The theorem-pair discipline is better than a generic brainstorming system.

What it overclaims:

- The top live queue still speaks in schematic metavariables rather than mathematical content.
- Several carriers remain role-descriptions (`MCSP obstruction family`, `PIT certificate family`, `TAUT transport normal form`) rather than actual structures.

Most serious missing mechanism:

- A theorem concretizer that rewrites promoted branch claims into parameterized, expert-readable mathematical statements before they enter the live proof queue.

Failure mode:

- An expert sees a sharp research programme but still cannot evaluate the mathematics directly.

Recommendation:

- Do not allow branch-promoted prove targets to stay in the queue with metavariables `S/R/C/I/T`; force theorem-body substitution or mark them as discovery-only.

### 3. DeepMind-Style Discovery Scientist

What the reasoner is actually doing well:

- Search is decomposed into queue items, branch queues, branch executions, synthesis, promotions, work loops, high-reward continuation, and meta triggers.
- The system records replayable state rather than ephemeral chain-of-thought.
- Prior-art import and local-memory-first policy are real.

What it overclaims:

- Branch execution is reported as execution, but is not yet a strong search operator.
- Evaluation remains weakly calibrated because branch outputs are not tied to downstream proof payoffs robustly enough.

Most serious missing mechanism:

- Branch-level ablations and payoff accounting: which branch changed the queue, the plausibility score, the proof debt, or the obstruction taxonomy?

Failure mode:

- The architecture becomes a sophisticated task manager whose search operators are too weak relative to the complexity of the control system.

Recommendation:

- Measure branch value by frontier delta, not by existence of a branch report. A branch should justify itself by emitting a sharper theorem, sharper obstruction, or lower proof debt.

### 4. Concept-Discovery Logician

What the reasoner is actually doing well:

- It recognizes that the real frontier is often an abstraction type, not the next theorem.
- It now classifies breakthrough families and epistemic patterns explicitly.
- It records representation shifts and object-alignment problems as first-class issues.

What it overclaims:

- Typed labels are often treated as if they already stabilize a concept.
- Object equivalence and representation coherence remain mostly diagnosed rather than solved.

Most serious missing mechanism:

- A concept stabilization pass that decides whether a candidate object is:
  identical,
  equivalent,
  incomparable,
  under-typed,
  or route-breaking relative to neighboring objects.

Failure mode:

- The reasoner proliferates near-duplicate bridge objects and route labels without concept closure.

Recommendation:

- Make concept-equivalence and concept-refinement explicit transitions in the queue and branch system, not just prose in diagnoses.

### 5. Radical Systems Designer

What the reasoner is actually doing well:

- The platform already behaves like a multi-agent scientific operating system.
- The new epistemic-process map and process spine move in the right direction by exposing the whole circuit.

What it overclaims:

- The architecture still privileges stage completion over state transformation.
- Too much epistemic meaning is inferred from artifact production.

Most serious missing mechanism:

- A first-class state-transition language in which each cycle must declare:
  what changed,
  what was ruled out,
  what was compressed,
  and what new invariant became visible.

Failure mode:

- The system keeps generating polished surfaces while hidden debt and non-progress remain hard to see.

Recommendation:

- Rebase the outer loop on state deltas rather than stage outputs. A cycle without a meaningful state delta should count as epistemically idle, no matter how many reports it emitted.

## Convergence

Shared concerns:

- The system is stronger at organization than at theorem production.
- Mathematical specificity remains the main bottleneck.
- Internal consistency across artifacts is not yet strong enough for full trust.
- Negative findings are genuinely valuable and should become first-class theorem memory.

Lens-specific concerns:

- Epistemologist: evidence versus coherence.
- Fields Medalist: theorem-level specificity and carrier realism.
- Discovery scientist: weak branch payoffs and weak calibration.
- Concept logician: concept stabilization and equivalence.
- Radical designer: state-delta blindness under a large artifact ecology.

Structurally important disagreements:

- The discovery scientist sees the architecture as close to useful if branch operators improve.
- The Fields-style review is harsher: without concrete mathematical statements, the live frontier is still too schematic.
- The radical designer would redesign the control language itself, while the epistemologist is willing to keep the architecture if evidence-accounting is fixed.

## Prioritized Redesign Agenda

### Fix Now

1. Enforce cross-artifact consistency checks, especially queue state versus proof summary versus work state.
2. Downgrade branch execution language unless it emits a real theorem delta, concept delta, or obstruction delta.
3. Recalibrate plausibility scoring so `evidence_count = 0` and `proved_count = 0` cap the score more sharply.
4. Persist blocked results into InformalMathLib as first-class negative local theorems.

### Instrument Next

1. Add branch payoff accounting: queue delta, proof-debt delta, concept delta, plausibility delta.
2. Add a claim-status ledger across all live claims and artifacts.
3. Add theorem concretization before branch promotions become prove tasks.
4. Add concept-equivalence / representation-coherence adjudication for bridge objects.

### Reconsider Architecturally

1. Treat stage outputs as secondary; treat state transitions as primary.
2. Distinguish organizational maturity from mathematical maturity in every score and report.
3. Rebuild the discovery executor so branch execution can actually generate or refute concepts, not just summarize the frontier.

## Bottom Line

This reasoner is already a substantial discovery-governance system.
It is not yet a strong autonomous theorem-discovery system.

Its most original contribution today is not a proof of `P vs NP`, but a highly inspectable process for:

- theorem-grounded route formation,
- obstruction localization,
- persistent search governance,
- and expert-auditable negative knowledge.

To become a real mathematical discovery engine, it now needs stronger theorem production, stronger concept closure, stronger memory of its own negative results, and much tighter evidence calibration.
