<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Discovery workflow review: a theory-first architecture for conceptual discovery

Review date: 2026-07-21

## Scope and corrected verdict

This review covers the discovery-marathon control plane, target navigation,
conceptual-revision and branch-exploration phases, proof handoffs, symbolic and
numeric probes, state and reports, validators, evaluation, and the available
skill surface.

The repository has an unusually rich collection of useful specialist skills,
but those skills are not composed into a feedback-effective process for deep
theory formation. The main scientific bottleneck is therefore **reflective
conceptual creativity**: discovering a more relevant ontology, distinction,
mediator, representation, mechanism, explanatory principle, or synthesis and
then developing it into a coherent theoretical programme.

This must be distinguished from a second problem:

- **Scientific bottleneck:** reflective creativity, conceptual depth,
  explanatory understanding, relevance, and unification are peripheral to the
  current controller.
- **Integrity bottleneck:** the runtime can describe skill invocations,
  learning, validation, and progress without sufficient executable receipts.

The integrity problem is serious and must be repaired, but execution truth is
not the discovery objective. Truth is the regulative destination and the
constraint on established claims. Early theory formation should instead be
allowed to explore honestly conjectural conceptual systems and converge through
reflection, articulation, opposition, synthesis, formal consequence, and only
then proof or evidence where appropriate.

Experiments consequently have a secondary role. A mature theory may commission
a Gedanken analysis, exact symbolic calculation, finite countermodel, proof
attempt, literature inquiry, or simulation to answer a precise question.
Discovery must also be able to return `no_probe_needed` when deeper theoretical
work is the correct next move.

## What real conceptual discovery should mean here

A substantive conceptual advance is not merely a new phrase, artifact, branch,
score, or locally testable claim. It should satisfy the applicable parts of the
following quality bar.

1. **Essential relevance.** It bears on the real mathematical or scientific
   target rather than a convenient proxy.
2. **Root-tension contact.** It identifies why the inherited conceptual frame
   generates, hides, or cannot express the central difficulty.
3. **Genuine transformation.** It changes a primitive, identity, distinction,
   relation, operation, mechanism, explanatory dependency, equivalence policy,
   regime structure, or generative consequence.
4. **Philosophical depth.** It makes ontology, explanatory ideals, access
   assumptions, modality, representation, and the strongest opposed
   commitments explicit.
5. **Explanatory understanding.** It states precisely what becomes intelligible
   and why, not merely what correlates or can be redescribed.
6. **Unification with preserved difference.** It connects previously separate
   cases, scales, routes, or constraints through a common principle without
   deleting their decisive differences.
7. **Generativity.** It opens consequential definitions, questions,
   mechanisms, formal objects, derivations, or proof obligations.
8. **Reflective resilience.** Serious opposing perspectives cause mutation,
   synthesis, demotion, or explicit unresolved dissent rather than ceremonial
   review.
9. **Truth-aptness.** The theory is inspectable, non-self-sealing, internally
   coherent enough to develop, and exposes correction conditions and formal or
   evidential burdens.
10. **Claim discipline.** A theoretically preferred idea remains conjectural
    until the relevant proof, entailment, source, or evidence authority licenses
    a stronger claim.

Items 1–9 govern conceptual investment. Item 10 governs promotion. An
experiment is not a constitutive gate for conceptual discovery.

This quality bar is not a presumption that every difficult problem needs a new
concept. A control case in which the incumbent framework is adequate should be
routed to calculation, formalization, proof, reading, or measurement. Inventing
a conceptual crisis where none is evidenced is another form of novelty theatre.

## Current workflow and why it stalls conceptually

The effective marathon order is roughly:

```text
target navigation
  -> branch selection, including next-experiment ranking
  -> local conceptual-abstraction revision
  -> literature and target-specific overlays
  -> branch abduction/deduction/induction
  -> inference and proof-depth review
  -> proof delivery, reports, release, and another cycle
```

This order is visible in
`agentic/registries/discovery_marathon_skill_dispatch.yaml:20-46` and
`:99-169`. Experiment ranking occurs during branch selection, while conceptual
quality is embedded later in proof-depth control. The controller therefore
orients work before a theory constellation, conceptual genealogy, or reflective
synthesis exists.

The deterministic KB orchestrator also explicitly does not execute prompt-only
abduction, deduction, explanation, or induction
(`skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py:8-18`). The
workflow has many declared reasoning roles, but no central operator that owns
their conceptual outputs and recursively changes the next theoretical move.

## Assets worth preserving and centralizing

The repository already has strong leaf capabilities. They should be composed,
not reimplemented.

| Theoretical function | Existing skills to reuse |
|---|---|
| Relevance and reflective orientation | `meta`, `main-problem-alignment-auditor`, `physical-relevance-impact-auditor`, `literature-gap-relevance-auditor` |
| Literature collection and prior-art control | `target-literature-source-curator`, `kb-prior-art-pass`, `prior-art-importer`, `results-prior-art-disqualifier-auditor`, `target-literature-evolution-narrator` |
| Deep-pressure diagnosis | `mathematical-concept-gap-revisitor`, `proof-depth-pressure-formalizer`, `abducer-conceptual-pressure-formalizer`, `abducer-failure-signal-cartographer`, `kb-discovery-breakthrough-profiler` |
| Abductive and conceptual divergence | `kb-abduce`, `kb-gap-abstraction-conjecturer`, `abducer-mediation-candidate-generator`, `proof-bridge-object-forger`, `proof-creative-variant-prober` |
| Intuitive and radical variation | `gedanken-counterfactual-variant-builder`, `counterfactual-route-prober`, `review-reasoner-radical-designer`, plus the local abduction and mediation operators above |
| Representation invention | `efficient-representation-requirements-elicitor`, `visual-theorem-conceptualizer`, `kb-concept-bridge-planner` |
| Synthesis and coherence | `abstraction-fit-gap-auditor`, `kb-coherence-evaluator`, `bridge-object-equivalence-checker`, `kb-induce` |
| Hypothesis premortem and later proof-route control | `failed-hypothesis-anticipator`, `kb-novel-proof-strategist`, `kb-hypothesis-evaluator`, `kb-hypothesis-refutation-loop`—used after articulation or formalization, not as the early creativity objective |
| Plural theoretical judgment | `proof-conceptual-quality-heuristic-rater`, `contribution-value-assessor`, concept-logician, epistemologist, mathematician, discovery-scientist, and radical-designer reviews |
| Late truth convergence | `entailment-gap-auditor`, `counterexample-hunter`, `abducer-obligation-gatekeeper`, domain proof critics, proof-delivery skills |
| Optional theory support | Gedanken skills, `qualitative-variable-isolator`, `qualitative-toy-model-builder`, target symbolic auditors, `next-experiment-queue-ranker` |
| Existing execution concurrency | discovery-marathon `--parallel-branches`, API worker pool, frozen branch inputs, and serialized post-worker state update |

The existing `conceptual-obstruction-refinement` task should be retained as a
transformation subroutine. The Hegelian field-tension, conceptual-crisis,
mechanism-hypothesis, transformation, dialectic, explanation, and candidate
ranking skills are useful source material for reflection, but should be adapted
into the repository's contracts rather than creating a second control plane.

## Severity-ranked findings

### Critical scientific finding: reflective creativity has no parent loop

Conceptual revision is currently one phase among many, not the controller of
future work. There is no durable object representing rival conceptual systems,
their ontologies, explanatory ideals, transformation genealogy, reflection
rounds, preserved differences, syntheses, or changes in understanding. As a
result, `meta` and conceptual-quality reviews tend to become post-hoc
commentary, while queues and proof artifacts remain feedback-effective.

Consequence: the system can keep working inside the same ontology while
renaming bridges and obligations. It lacks the recursive process needed to ask
whether the current objects, relations, equivalences, explanatory standards,
or problem formulation are themselves the obstacle.

Required response: make `reflective-conceptual-discovery` the parent loop, with
`reflective-theory-synthesizer` as its mutation-producing philosophical and
mathematical reflection operator.

### Critical scientific finding: literature exists but does not yet change the discovery cycle reliably

The dispatch order performs `branch_selection` before
`avenue_literature_gap_precheck`
(`agentic/registries/discovery_marathon_skill_dispatch.yaml:20-64`). The
scheduler imports literature warrants, but consumes a reduced summary and does
not call the available `branch_warrant_allows_exploration` gate
(`agentic/scripts/discovery_marathon_scheduler.py:243-315`). When no branch
warrant matches, `warrant_for_branch` silently returns the first warrant; its
summary also discards the source-claim detail needed for conceptual revision
(`agentic/scripts/avenue_literature_gap.py:86-135`).

The provenance boundary is weaker still. Required literature skills can be
auto-listed as invoked by the generic dispatch trace. The shared
`agentic/reports/target_literature_evolution/latest.json` currently identifies
the Yang–Mills target and has no `source_search_provenance`, while P-vs-NP
warrants and reports also cite that same global path. The builder constructs a
curated source spine; a report timestamp therefore does not establish that the
most recent literature was searched. Search queries, provider or index,
searched-at time, coverage cutoff, inclusion policy, result counts, source
versions, and correction or retraction checks are not bound into a validated
snapshot.

Consequence: literature can decorate a branch after the branch has already won,
and a wrong-target or stale report can appear current. Candidate generation is
literature-blind, while assimilation never has to spawn, merge, split, reframe,
demote, retire, or reprioritize a theory.

Required response: implement `DWF-013`. Before every major portfolio, freeze the
newest validated target-scoped search snapshot, assimilate claim-level source
deltas into theory state, and make the scheduler consume them. Search again
against generated hypotheses and after major results. Preserve one
intuition-first generation pass to prevent anchoring, but require literature
rebase before investment, synthesis, proof routing, or novelty claims.

### Critical scientific finding: candidate creation is shallow and has no protected high-risk mode

`choose_operation` selects one operation from target flags, pressure type, a
hook list, and an index
(`agentic/scripts/build_hypothesis_exploration_map.py:461-478`).
`candidate_text` then emits templates for bridge invention, abstraction,
restriction, theorem weakening, carriers, inversion, analogy, representation,
or factorization (`:481-512`). Candidate metadata reports relevance,
tractability, and novelty (`:515-599`), but does not reconstruct an ontology,
develop explanatory mechanisms, compare rival systems, or measure an
understanding delta.

Consequence: operation labels can vary while conceptual architecture remains
fixed. The process generates local repair suggestions rather than theories and
systematically underexplores counter-consensus ontologies, negative theories,
scale reversals, cross-field mechanisms, and unification conjectures whose
truth probability is low but value and learning potential are high.

Required response: preserve the transformation operators, but apply several of
them to a reconstructed conceptual situation; require materially different
systems and recursive reflection before selecting a provisional synthesis.
Implement `DWF-014`: generate an intuition-led portfolio across at least six
genuine conceptual corners when viable, keep probability, reward, learning
value, conceptual worth, and cost separate, include a conservative control, and
protect at least two relevant nondominated wildcards from immediate scalar
pruning.

### Critical scientific finding: convergence is too scalar and too close to proof

The existing conceptual-quality vector contains many of the right ideas, but it
is placed in proof-depth control and does not govern branch formation. A single
aggregate preference would also be unsafe: depth, unification, relevance,
coherence, and generativity can trade off in ways that should remain visible.

Consequence: easy-to-score or proof-adjacent candidates can prematurely defeat
deeper theories, while hard but essential branches are starved.

Required response: use essential relevance as a floor, then maintain a Pareto
portfolio over root-tension contact, understanding, explanation, unification,
preservation of difference, depth, generativity, coherence, and truth-aptness.
Retain a serious challenger until it fails a target commitment or is genuinely
dominated.

### Integrity-critical finding: declared reasoning is not executed reasoning

The dispatch registry asks every cycle to record whether required skills were
invoked, but the trace builder can construct generic records from phase
membership rather than actual typed requests, artifacts, and validators. The
prompt-only reasoning skills are outside the deterministic orchestrator.

Consequence: reports may imply that a large interdisciplinary panel acted even
when no specialist output became feedback-effective. This does not merely harm
auditability; it makes it impossible to tell whether reflective synthesis
caused the next action.

Required response: add operator requests and receipts containing versions,
input and output digests, state identity, artifacts, status, and validation.
Distinguish documented, registered, routed, executable, exercised,
output-consumed, and feedback-effective reachability.

### Integrity-critical finding: activity and prose can manufacture learning

Cycle validity and learning currently rely partly on elapsed time, generated
learning prose, and state updates whose semantic novelty is not independently
established. The work loop can also mark the creation of a proof-attempt dossier
as a completed step while acknowledging that active attempts lack a direct
continuation executor
(`skills/orchestration/work/scripts/run_work_cycle.py:2489-2518,2541-2621`).

Consequence: long or artifact-rich runs can look like research progress even
when no perspective, concept, explanation, theorem state, or counterpressure
changed.

Required response: classify explicit learning deltas—such as perspective shift,
ontology revision, conceptual deepening, synthesis, unification, explanatory
compression, productive contradiction, falsification, or assumption repair—and
use one versioned reducer to commit state.

### High scientific finding: formative and diagnostic symbolic reasoning are conflated

Symbolic reasoning has two distinct roles:

- **Formative symbolic reasoning** invents definitions, representations,
  invariants, dualities, interfaces, formal languages, and objects. It belongs
  inside theory construction.
- **Diagnostic symbolic execution** checks a derived identity, consequence,
  satisfiability condition, finite countermodel, or exact witness. It belongs to
  optional theory support.

Treating all symbolic work as experiment prematurely requires typed predictions
and can prevent the symbolic invention through which a theory becomes
testable.

Required response: keep formative symbolic construction inside the reflective
loop; give `dynamic-symbolic-simulation-experimenter` only diagnostic execution
authority.

### High scientific finding: existing probes are target-specific sidecars

The symbolic matrix probe fixes a particular normalized three-observable
Hermitian construction (`agentic/scripts/build_symbolic_matrix_probe.py:18-68`).
The bounded numeric runner offers three predetermined Yang–Mills probes and
writes global `latest` files
(`agentic/scripts/run_bounded_numeric_probe.py:13-15,18-115,135-145`). These
can be useful local scientific tools, but they are not dynamically compiled
from a conceptual system, theoretical question, rival consequence, and
model-to-target boundary.

Consequence: available computation can shape the question, and a result may not
round-trip to the theory that supposedly requested it.

Required response: commission immutable, branch-scoped support specifications
from mature theory questions; preregister decision regions, controls, budgets,
transfer limits, and the conceptual change each outcome could cause.

### High finding: theory, marathon, work, proof, and probe state are fragmented

Marathon state, work queues, proof attempts, conceptual artifacts, reports, and
probe outputs live in separate state universes, often connected by prose and
`latest` pointers rather than stable concept, hypothesis, obligation, receipt,
and evidence IDs.

Consequence: a refutation, synthesis, or understanding gain can fail to update
all affected descendants; negative knowledge disappears; equivalent work is
repeated.

Required response: create an append-only theory and epistemic event ledger with
a versioned reducer and projections for every workflow view.

### High operational and scientific finding: parallel execution is not yet a parallel theory portfolio

The marathon already uses a thread pool for API branches and deep-copies branch
inputs (`agentic/scripts/run_discovery_marathon.py:1102-1220`). That is a useful
execution substrate. However, any failed worker raises the whole group after
completion, so valid siblings are not delivered as partial success. State waits
for all packets, branches share a shallow selection and synthesis frame, and the
current synthesis is closer to keyword and next-experiment aggregation than to
comparison of rival ontologies, mechanisms, genealogies, and conflicts.

Consequence: more workers can produce correlated variants rather than greater
conceptual coverage; one failure can erase useful independent learning; and a
new literature snapshot can make branch assumptions inconsistent without an
explicit rebase.

Required response: implement `DWF-015` over the existing worker surface. Freeze
target, theory, and literature digests; assign distinct branch mechanisms and
local namespaces; prevent early cross-talk; validate independently; preserve
partial successes; optionally cross-pollinate after divergence; and submit one
conflict-preserving compare-and-swap merge. Parallel search should similarly
use independent closest-work, recent-frontier, barrier, genealogy,
adjacent-field, and dissent lanes with deterministic deduplication.

### High finding: discovery-quality evaluation is lexical, self-derived, and circular

Current validation can check expected keys and textual markers without proving
that a concept changed, an explanation deepened, or a synthesis preserved
difference. The theorem-discovery simulator also reconstructs hidden targets
from the same KB graph that contains the relevant labels and dependencies,
which is valuable pipeline testing but not independent evidence of discovery.

Consequence: surface novelty, artifact shape, route reconstruction, conceptual
worth, model support, and proof validity are conflated.

Required response: combine executable negative cases with held-out domains and
blinded expert comparison. Experts should assess relevance, depth,
understanding, unification, philosophical clarity, generativity, coherence, and
truth boundaries; proof and evidence status should remain independent axes.

### High operational finding: persistence and validation are not yet a reliable substrate

Direct file writes, shared pointers, cycle identity derived from mutable state,
partial job failure, and inconsistent Python test environments make replay and
recovery fragile. These defects do not define conceptual quality, but they can
corrupt its memory and falsely certify it.

Required response: use branch-scoped content-addressed artifacts, atomic
journaled commits, compare-and-swap generations, deterministic recovery,
operator budgets, one locked toolchain, a minimum test count, and non-mutating
validation by default.

## Target architecture

The primary workflow should be:

```text
essential target and desired understanding
  -> conceptual genealogy, inherited ontology, and explanatory ideals
  -> newest validated target-scoped literature snapshot
       |-> parallel search lanes: closest work / recent frontier / barriers
       |                         genealogy / adjacent fields / dissent
       '--> source-to-theory assimilation and opportunity frontier
  -> root tension or productive contradiction
  -> intuition-first aggressive hypotheses across conceptual corners
  -> hypothesis-conditioned literature search and mandatory rebase
  -> relevance-constrained high-risk/high-reward Pareto portfolio
  -> isolated parallel maturation of independent conceptual systems
       '--> validate each branch / preserve partial success / retain conflict
  <-> recursive philosophical and mathematical reflection
  -> transformed rivals and provisional syntheses
  -> single-writer conflict-preserving convergence
  -> articulated theoretical programme
       |-> definitions and formative symbolic construction
       |-> derivations and proof obligations
       |-> targeted literature clarification and post-result search
       '--> optional theory-requested support probe
                -> diagnostic symbolic execution / countermodel / simulation
                -> literature-aware reflective assimilation
```

This is a four-part epistemic architecture:

1. **Frontier grounding.** Resolve the newest validated target-scoped search,
   map sources into theory, and expose neglected corners, barriers, transfers,
   and apparent gaps. A global `latest` file is never identity.
2. **Generative license.** Permit broad but typed conceptual speculation. Keep
   one intuition-first pass blind to detailed source mappings, track ancestry
   and non-claims, and do not demand immediate proof or experiment. Rebase every
   survivor before active investment.
3. **Parallel reflective selection.** Mature genuinely independent rivals in
   isolated branches, preserve valid partial results and dissent, and transform them
   through ontological, dialectical, epistemological, explanatory,
   representational, modal, genealogical, unificatory, and reflexive lenses.
   Select a Pareto portfolio by theoretical virtues.
4. **Truth stabilization.** Formalize consequences and use deduction, proof,
   counterexamples, sources, exact computation, or bounded simulation as their
   actual authority permits.

### Canonical theory state

The durable state should include:

- the essential question, desired understanding, relevance horizon, and
  non-claim boundary;
- conceptual genealogy, hidden assumptions, and protected successes;
- immutable target-scoped literature snapshots with query provenance,
  claim-level mappings, coverage limits, source deltas, and assimilation events;
- systems with primitives, ontology, relations, operations, mechanisms,
  explanatory ideals, regimes, and correction conditions;
- high-risk hypothesis packets with intuition provenance, corner family,
  risk/reward axes, literature relation, maturation question, and protected
  wildcard status;
- opposition, transformation, synthesis, unification, preservation,
  contradiction, support, and supersession edges;
- reflection rounds and the exact mutations or `no_change` findings they cause;
- a before/after understanding delta and unification map;
- theoretical consequences, definitions, derivations, proof obligations, and
  literature questions;
- optional support specifications, immutable execution receipts, and transfer
  boundaries;
- parallel manifests, branch input digests, attempt receipts, overlap and
  conflict edges, partial failures, rebase status, and reducer receipts;
- separate conceptual preference, coherence, formal support, model support,
  experimental support, and proof statuses.

Concept lifecycle and truth status must remain independent. Useful lifecycle
states include `seed`, `articulated`, `reflectively_revised`, `synthesized`,
`theoretically_preferred`, `support_ready`, `formalization_ready`,
`proof_ready`, `validated`, `refuted`, and `retired`.

### Reflective recursion

Every major theory cycle should use at least three applicable philosophical or
mathematical lenses, including ontological and dialectical reflection. Each
round must change a candidate, synthesize systems, demote one, or record an
explicit `no_change`. Two materially empty rounds should trigger a reframe or
plateau, not more paraphrase.

Reflection should ask:

- What does the theory say exists, and which identities are merely assumed?
- What counts as explanation or understanding in this framework?
- Which opposed commitments protect genuine successes?
- Is the tension a contradiction, missing mediator, regime mismatch,
  underdetermination, or conflict of explanatory ideals?
- What does the representation reveal or make inexpressible?
- Which cases can be unified, and which differences must remain?
- Is the research method itself manufacturing the apparent bottleneck?
- What new questions and obligations become possible after the transformation?

### Continuous literature policy

Literature is a recurrent theory operator, not one preflight gate. Refresh and
assimilate it at five points: before a major portfolio opens, after intuition
seeds create hypothesis-specific queries, whenever a newer snapshot arrives,
before novelty or contribution claims, and after a major proof, derivation, or
support result. Each pass freezes an exact target-scoped snapshot and must
produce source-to-theory mappings plus an action delta or a source-grounded
`justified_no_change`.

Parallel search lanes should cover closest known results, recent frontier and
preprints, barriers and negative results, conceptual genealogy, adjacent-field
mechanisms, and dissent. Their receipts remain immutable and are reduced by
source identity and claim, not citation count. Search recency and publication
recency remain distinct. Failure to find a match means only `apparently_open`
within recorded coverage, never established novelty.

### High-risk portfolio and parallel-maturation policy

A major cycle should attempt 8–12 hypotheses across at least six genuine
conceptual corners when the target permits, including ontology inversion,
mediation, process or constraint primacy, scale reversal, cross-field transfer,
unification, a negative theory, and a counter-consensus variant. Keep a
conservative control. Protect at least two relevant nondominated wildcards, and
separate estimated truth probability from value if right, learning if wrong,
conceptual worth, and maturation cost.

Independent seeds can run concurrently only from frozen theory and literature
digests. Workers write branch-local artifacts, receive distinct mechanisms and
questions, and cannot commit shared state. Validate packets independently,
preserve valid siblings after failure, optionally cross-pollinate after blind
divergence, rebase survivors when literature changes, and perform one
single-writer compare-and-swap merge that preserves conflicts and dissent.

A concrete forward-test portfolio for the active P-vs-NP target is recorded in
[`artifacts/p-vs-np/high-risk-conceptual-portfolio-2026-07-21.md`](../../artifacts/p-vs-np/high-risk-conceptual-portfolio-2026-07-21.md).
It contains eight distinct seeds, two protected wildcards, a conservative
control, literature-rebase boundaries, and a parallel maturation manifest. It
is explicitly conjectural and `planned_not_executed`.

### Optional support-probe policy

Commission a probe only when:

1. a mature theory programme and exact theoretical question exist;
2. the probe has a declared role such as formal support, counterexample,
   calibration, constraint, or discrimination;
3. reflection or analytic derivation cannot currently answer it more directly;
4. possible outcomes imply different conceptual revisions;
5. the carrier, variables, assumptions, regime, controls, decision rule,
   resource budget, and model-to-target boundary are typed;
6. results return to reflective assimilation rather than automatically choosing
   an ontology or establishing a theorem.

Prefer theoretical counterfactual and Gedanken analysis first, exact symbolic
reasoning or finite countermodels second, and bounded numerical simulation only
when it is the appropriate model-scoped instrument. An immature or irrelevant
request should return `no_probe_needed` or `immature_question` without a fake
execution receipt.

## New skill surfaces

Six custom roles now define the missing control surface while reusing the
repository's existing specialist leaves:

1. `skills/orchestration/reflective-conceptual-discovery/` owns the theory
   constellation, recursive creative loop, Pareto convergence, theoretical
   programme, and optional support commissioning.
2. `skills/reasoning/reflective-theory-synthesizer/` turns deep philosophical
   reflection into concrete changes in primitives, distinctions, relations,
   explanatory structure, syntheses, and implications.
3. `skills/reasoning/dynamic-symbolic-simulation-experimenter/` owns only
   theory-requested diagnostic computation, preregistration, execution
   provenance, and evidence packaging.
4. `skills/reasoning/frontier-literature-assimilator/` refreshes or resolves the
   newest admissible target-scoped search snapshot through differentiated
   parallel lanes and turns source deltas into theory, hypothesis, genealogy,
   and scheduling events.
5. `skills/reasoning/high-risk-hypothesis-forger/` composes aggressive,
   intuition-led, high-risk/high-reward portfolios across structurally different
   conceptual corners and performs a two-pass literature relation.
6. `skills/orchestration/parallel-hypothesis-portfolio/` freezes shared inputs,
   runs independent branch-local maturation, preserves partial success and
   dissent, rebases literature, and proposes one serialized merge.

The previous experiment-centred orchestration skill was removed because keeping
two parent loops would leave authority ambiguous. Existing specialist skills
remain the leaves of the new theory-first composition.

## TODO-backlog review and improvements

The original 13 TODOs covered the reflective kernel, truthful execution,
canonical memory, evaluation, scheduling, persistence, optional experiments,
and resource control. The audit exposed three uncovered outcomes, now added as
`DWF-013` through `DWF-015`:

- `DWF-013` makes recent literature continuous, target-scoped, provenance-rich,
  and causally effective rather than a post-selection report.
- `DWF-014` establishes an explicit high-risk/high-reward hypothesis operator
  with conceptual-corner coverage, protected wildcards, and separate risk,
  reward, learning, and truth axes.
- `DWF-015` upgrades existing worker concurrency into a safe parallel theory
  portfolio with partial-success recovery, literature rebasing, and
  conflict-preserving reduction.

The existing cards were strengthened rather than bypassed. `DWF-000` now owns
the full literature → intuition → rebase → parallel maturation → reflection
cycle. `DWF-001` requires real search and branch receipts. `DWF-002` and
`DWF-003` retain source, intuition, risk/reward, branch, and learning ancestry.
`DWF-005`, `DWF-009`, and `DWF-011` add pseudo-radical, stale/wrong-target
literature, correlated-branch, partial-failure, and time-sliced literature
tests. `DWF-006` schedules search and high-risk theory actions before probes.
`DWF-007`, `DWF-008`, `DWF-010`, and `DWF-012` now enforce transactional
parallel integration and selective retry.

One dependency was deliberately relaxed: `DWF-012` no longer requires the
optional experiment runtime merely to impose general job budgets. It instead
depends on the parallel portfolio runtime, while experiment adapters remain one
budgeted consumer. All 16 cards remain open; this review changes architecture
and acceptance evidence, not implementation status.

## Ordered implementation plan

### Wave 1 — Install the creative parent loop and execution truth

- Implement `DWF-000` as the controlling theory loop, not a report-only phase.
- Implement minimal real operator requests and receipts in `DWF-001`; remove
  generic auto-attestation.
- Start `DWF-009` with one locked validation command and executable negative
  fixtures so later milestones cannot be self-certified.
- Make `no_probe_needed` a successful theory-cycle disposition.

Milestone: a live target produces rival conceptual systems, mutation-producing
reflection, an understanding delta, and a changed next theory action with real
operator receipts and no mandatory experiment.

### Wave 2 — Build cumulative, transactional theory memory

- Implement `DWF-002` for canonical theory, concept, literature, hypothesis,
  branch, obligation, and evidence events.
- Implement `DWF-003` for semantic learning and one authoritative reducer.
- Implement `DWF-005` for plural creative-worth assessment independent of
  established truth.
- Implement `DWF-008` for content-addressed state, immutable snapshots,
  branch-local writes, recovery, and compare-and-swap.

Milestone: theory state can be replayed across crashes and concurrent attempts,
while conceptual promise, literature status, branch completion, and truth
status remain distinct.

### Wave 3 — Make frontier literature and aggressive intuition causal

- Implement `DWF-013` first: parallel target-scoped horizon search, exact search
  receipts, source-to-theory assimilation, hypothesis-conditioned search, and
  scheduler-visible deltas.
- Implement `DWF-014` on that basis: 8–12 intuition-led hypotheses across at
  least six genuine corners when viable, a control, protected wildcards, and
  mandatory second-pass literature rebase.
- Test target mismatch, stale and superseded snapshots, literature absorption,
  pseudo-radical variants, analogy failure, and high-upside low-confidence
  incubation.

Milestone: the newest literature can change the theory constellation, while
bold hypotheses can escape consensus anchoring without escaping relevance,
genealogy, or correction conditions.

### Wave 4 — Schedule and mature rival theories in parallel

- Implement `DWF-006` over literature-aware high-risk theory actions rather than
  an experiment queue.
- Implement `DWF-015` by adapting the existing worker pool to frozen inputs,
  conceptually distinct lanes, partial-success recovery, optional delayed
  cross-pollination, literature rebase, and a single-writer merge.
- Complete `DWF-007` so parallel theory deltas, formalization, proof, and later
  support all return to the same theory state.
- Complete `DWF-010` only when all six new skills are routed, exercised,
  output-consumed, and authority-correct. Complete general job budgets and
  selective retry in `DWF-012`.

Milestone: several independent conceptual corners advance concurrently; a
worker failure or new literature snapshot does not erase valid learning or
collapse unresolved dissent.

### Wave 5 — Add optional theory-requested symbolic and simulation support

- Implement `DWF-004` only against mature questions from the canonical theory
  ledger.
- Add exact, finite-model, numeric, sweep, and hybrid adapters with immutable
  specifications, hard budgets, receipts, and model-to-target boundaries.
- Return every validated result through the same literature-aware reflective
  assimilation path.

Milestone: an exact counterexample or model-scoped simulation can revise a
theory, while an immature request is declined without penalizing conceptual
progress.

### Wave 6 — Earn claims about discovery quality

- Implement `DWF-011` using independently authored held-out tasks, time-sliced
  literature, withheld later breakthroughs, leakage controls, ablations, and
  blinded expert comparison.
- Compare conservative local variation, random, lexical, current,
  no-reflection, no-literature-rebase, no-high-risk, no-parallel, and no-symbolic
  baselines at matched budgets.
- Report conceptual transformation and understanding separately from
  literature novelty, route reconstruction, empirical/model support, and proof
  validity.

Milestone: claims of conceptual discovery rest on held-out and time-sliced
evidence plus expert judgment over explicit theoretical virtues, not artifact
count, consensus departure, or philosophical vocabulary.

## TODO index

The executable backlog is `agentic/todos/discovery_workflow_todos.yaml`.

| ID | Priority | Outcome |
|---|---:|---|
| `DWF-000` | Critical | Reflective conceptual creativity becomes the parent discovery operator |
| `DWF-001` | High | Actual operator requests and receipts replace self-attested dispatch |
| `DWF-002` | Critical | Canonical theory, concept-genealogy, and evidence ledger |
| `DWF-003` | High | Theory-aware learning deltas and one state reducer |
| `DWF-004` | Medium | Optional theory-requested symbolic and simulation support runtime |
| `DWF-005` | High | Creative worth is assessed separately from established truth |
| `DWF-006` | High | General theory-action portfolio replaces experiment-first scheduling |
| `DWF-007` | High | Theory formation, work, proof, and support results share one loop |
| `DWF-008` | High | Atomic, versioned, recoverable discovery state |
| `DWF-009` | High | Reproducible executable quality suite |
| `DWF-010` | High | Evidence-sensitive integration and feedback-effective reachability |
| `DWF-011` | High | Held-out and blinded expert evaluation of conceptual discovery |
| `DWF-012` | Medium | Hard budgets for supporting computation and marathons |
| `DWF-013` | Critical | Continuous target-scoped frontier search and theory assimilation |
| `DWF-014` | Critical | Aggressive high-risk/high-reward conceptual hypothesis portfolios |
| `DWF-015` | High | Isolated parallel maturation with partial-success and dissent preservation |

## Validation evidence for this review

- All six custom skill folders pass the system `quick_validate.py` check and the
  repository's scoped skill-depth validator with zero critical findings.
- The 16-card TODO file passes `validate_todo_file`; all blockers resolve and
  its dependency graph is acyclic.
- A literature-assimilator forward test on the active P-vs-NP target rejected
  the Yang–Mills global `latest`, treated the local prior-art packet as bounded
  evidence, and returned `refresh_required` with novelty and broad investment
  blocked.
- A high-risk-forger forward test generated eight distinct P-vs-NP hypotheses,
  covered more than six conceptual corners, retained two wildcards and a
  control, preserved the target quantifiers, and left all literature relations
  pending rather than claiming novelty.
- A parallel-portfolio forward test preserved five valid branch packets after
  one simulated timeout, kept the timeout distinct from refutation, marked all
  survivors `literature_superseded` when a newer snapshot arrived, and refused
  merge until rebase receipts existed.
- The repository-wide TODO validator remains blocked by a pre-existing YAML
  parse error in
  `agentic/todos/cumulative_result_subgoal_atlas_todos.yaml:420`; the scoped
  discovery-workflow TODO validation passes.

## Claim boundary

This review establishes an architecture, reusable skill composition, new skill
contracts, and an ordered implementation backlog. It does not establish that
the current runtime already performs reflective conceptual discovery, that its
current global literature report represents a live recent search, that its
existing symbolic or simulation outputs validate a theory, or that any target
theorem has advanced. No new external literature search was performed for this
workflow review. Those claims require the implementation and acceptance
evidence specified by the TODOs.
