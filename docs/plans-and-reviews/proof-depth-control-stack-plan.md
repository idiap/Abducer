<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof Depth Control Stack Plan

This plan turns the current Yang-Mills diagnosis into transferable proof-search
skills. The stack is target-neutral: Yang-Mills supplies the calibration case,
but the same controls should apply to P vs NP, theorem proving, physics
autoformalization, and any proof workflow where many locally valid steps can
still avoid the decisive conceptual pressure.

## Diagnosis

The existing Abducer workflow can already require lemmas, assumptions,
equations, falsifiers, dependency updates, and next experiments. That is useful
against empty cycles, but it is not enough against shallow theorem-shaped work.
A cycle can satisfy those markers while only refining safe algebra, restating
known boundaries, or validating artifacts that do not change the proof state.

The Yang-Mills Route A case exposes the problem clearly. The finite
Schur-Feshbach Wilson-block result is a real bounded contribution, but the deep
frontier is the geometric-collar and same-theory transfer gate. Endpoint
cumulant or OS-positivity refinements are useful only when they are downstream
from explicit paths, normalized same-theory observables, and coefficient
theorems. Otherwise they can become a high-quality loop around the wrong
bottleneck.

## Declarative Learning Requirement

The stack must not treat conceptual learning as a high-level goal such as
"improve understanding" or "find a deeper route." Each cycle should emit
inference-level learning facts that later cycles can reuse. A learning fact has
the shape:

```text
given premises P under regime R, attempted move M failed/succeeded because
constraint C was active; therefore future moves of class K require object,
invariant, certificate, or counterexample W.
```

This makes conceptual progress cumulative. A later cycle should be able to
query the ledger and learn, for example, that a Yang-Mills endpoint calculation
is support-only until geometric collar paths and same-theory normalization have
been certified. For another proof, the same form might say that a reduction
argument is support-only until a uniform carrier, admissible transfer theorem,
or barrier-specific counterexample is supplied.

The key object is not a paragraph of narrative insight. It is a declarative
inference event with source evidence, premises, conclusion, scope, demotion
trigger, and routing consequence.

## Conceptual Quality Heuristics

Depth control should use explicit conceptual heuristics, not only pass/fail
proof gates. Each cycle, learning event, and lock-in candidate should be
classified by a small heuristic vector:

- **Conceptual depth:** Does the move touch the root tension, hidden invariant,
  missing construction, or transfer obstruction, rather than a surface
  bookkeeping lemma?
- **Explanatory power:** Does it explain why a phenomenon, obstruction, or
  constraint occurs, or does it merely record that it occurs?
- **Unification power:** Does it connect previously separate routes, objects,
  regimes, or failure patterns under one controlled principle without erasing
  their distinctions?
- **Mechanism specificity:** Does it name the operative mechanism, mediator,
  enabling condition, and defeater?
- **Compression:** Does it reduce many local cases to a smaller theorem,
  invariant, schema, or calculation pattern?
- **Generativity:** Does it create new proof obligations, variants, falsifiers,
  computations, or bridge objects that were not already obvious?
- **Transfer reach:** Does it travel to another regime, target, or proof family
  with a named transfer certificate and scope limit?
- **Falsifiability:** Does it expose a concrete counterexample class, failed
  estimate, invalidated assumption, or kill condition?
- **Boundary sharpness:** Does it clarify what is not claimed and where the
  result stops?
- **Literature displacement:** Does it change the relation to known work,
  known barriers, or accepted route families?

These are heuristics, not proof substitutes. A high score cannot promote a false
claim. Its role is to prevent the system from mistaking locally valid but
conceptually inert work for meaningful discovery.

## Anti-Definitionality And Transfer Substance

One recurring referee failure mode is a principal theorem that is formally
correct but close to definitional. A transfer theorem can look central while
only expanding the chosen definitions, renaming a source object as a target
object, or baking the desired target property into the bridge object. That is
not a deep transfer result. It is usually exposition, setup, or support-only
infrastructure.

The stack should distinguish four cases:

- **Definitional restatement:** the conclusion follows by expanding the
  definitions and doing no proof work.
- **Notation-preserving translation:** the theorem changes names or
  presentations but preserves no independently specified structure.
- **Conservative unpacking:** the result is useful for clarity or workflow
  hygiene but does not move a hard gate.
- **Substantive transfer:** the argument preserves a nontrivial invariant or
  property across independently specified source and target objects under
  hypotheses that can fail.

A transfer theorem can be promoted only when it supplies:

- source and target objects defined independently of the desired conclusion;
- a target property stated without bridge-specific vocabulary;
- a bridge map, normalization, reduction, representation, or carrier whose
  construction does not already encode the target property;
- a preserved invariant, inequality, semantic condition, or structural law;
- at least one nontrivial hypothesis that is used in the proof;
- a stress case or boundary regime where preservation is not automatic;
- a failure case, countermodel, or admissible variation showing what breaks
  without the substantive hypothesis;
- a consequence delta: what the reader can now infer that was not already
  available from the definitions;
- a prior-art delta: how the theorem differs from known transfer, equivalence,
  embedding, or normalization results.

The anti-definitionality audit should run a definition-expansion test,
independence test, source-variation test, stress-regime test, consequence-delta
test, and prior-art-delta test. If a theorem survives only because the target
predicate was defined to be the image of the source predicate, the theorem must
be demoted to support-only until an independent preservation law is supplied.

## Exploration And Lock-In Rhythm

The proof-depth stack should not remain in open exploration forever. Once the
learning ledger has enough pressure convergence, the system should deliberately
lock into a bounded proof-strategy cycle set. The lock-in mode is not a claim
that the main problem is solved. It is a temporary commitment to complete,
publish, or demote a meaningful subgoal before returning to broader conceptual
exploration.

Exploratory critical mass exists when the ledger has:

- repeated pressure on the same hard gate;
- at least one candidate object, invariant, falsifier, or transfer certificate
  with clear decision value;
- enough negative learning to rule out shallow variants;
- a smallest honest theorem, proposition, certificate, obstruction, or worked
  example that could stand as a publication subgoal;
- for Yang-Mills and other physics targets, a high physics conceptual reward:
  the pathway must plausibly change understanding around a named physical
  carrier and target gate, not merely add an incremental finite calculation;
- a bounded cycle budget and stop condition.

When those conditions hold, the workflow should enter proof-strategy lock-in:

1. Freeze the subgoal statement and its non-claims.
2. Freeze the small set of hard gates that can change the subgoal.
3. Run a bounded sequence of completion cycles: proof, counterexample,
   computation, prior-art boundary, manuscript integration.
4. Stop with one of three outcomes: publication-ready subgoal, precise demotion,
   or blocked lemma with evidence.
5. Push the resulting learning back into the ledger.
6. Reopen conceptual exploration only after the subgoal is completed, demoted,
   or explicitly blocked.

The default publication-consolidation limit is four completion cycles and
recursion depth one. A consolidation may use proof completion,
counterexample/falsifier work, finite computation or symbolic
parameterization, prior-art boundary work, and manuscript integration, but it
may not spawn a nested publication-consolidation loop. If a side lemma,
appendix, or auxiliary calculation does not fit inside the current budget, it
must be deferred to conceptual exploration or converted into a named blocked
lemma. At budget exhaustion the workflow must write a handoff, demote or block
the subgoal, and return to conceptual exploration before another consolidation
window can start. Re-entry requires a new live learning event that changes a
hard gate, supplies a missing object, or resolves a named blocker.

For Yang-Mills specifically, a consolidation window is opened only for branches
whose `major_publication_gate` is `invest_high_physics_reward`, or for a named
artifact/falsifier sprint whose success would decide such a branch. If the
packet is `reframe_before_investment`, `do_not_invest_support_only`, or
`quarantine_low_physics_reward`, the correct action is reframe, demote, pivot,
stop, or quarantine before spending more proof-search cycles.

This prevents two opposite failures: endless exploration that never crystallizes
into a paper, and premature lock-in that turns a weak route into a forced proof
attempt before the conceptual field has matured.

## Transferable Control Stack

The reusable stack should add twelve control points before a cycle can be
promoted:

1. **Conceptual pressure packet.** Name the tension being attacked: object
   mismatch, hidden normalization, missing construction, weak invariant,
   transfer failure, circularity, boundary-regime instability, or literature
   displacement.
2. **Hard-gate selection.** Require the cycle to choose one hard gate and state
   how success or failure changes that gate.
3. **Nontriviality audit.** Check whether the proposed proof object changes the
   theorem body, removes an assumption, constructs an object, proves an
   invariant, creates a falsifier, or closes a transfer certificate.
4. **Conceptual quality rating.** Score conceptual depth, explanatory power,
   unification power, mechanism specificity, compression, generativity,
   transfer reach, falsifiability, boundary sharpness, and literature
   displacement.
5. **Anti-definitionality audit.** Test whether the principal theorem survives
   definition expansion, has independently specified source and target objects,
   uses a nontrivial hypothesis, supplies stress and failure cases, and yields a
   consequence not already built into the definitions.
6. **Bridge-object generation.** When the pressure is not a missing lemma,
   design the missing carrier, interface, representation, invariant, toy model,
   or transfer law.
7. **Same-domain transfer certification.** Check whether the proof stayed in
   the same model, category, representation, regulator, complexity class, or
   semantic regime.
8. **Inference-level learning extraction.** Record what the cycle taught as a
   declarative inference event: premises, attempted move, learned constraint,
   scope condition, and future routing effect.
9. **Learning-ledger update.** Deduplicate and accumulate learning events into
   target-scoped rules that later branch selection and demotion can consume.
10. **Exploratory critical-mass check.** Decide whether the ledger now supports a
   bounded proof-strategy lock-in around a meaningful publication subgoal.
11. **Proof-strategy lock-in orchestration.** Temporarily freeze the subgoal,
   gate set, cycle budget, non-claims, and publication target until completion,
   demotion, or blocked-lemma handoff.
12. **Depth release gate.** Promote only if the cycle moved a hard gate. Demote,
   quarantine, or reroute cycles that are locally valid but strategically
   shallow.

## General Skill Families

- `proof-depth-pressure-formalizer`: converts a stalled or looping proof state
  into pressure packets.
- `proof-hard-gate-selector`: maps pressure packets to target-specific gates and
  rejects gate-free continuation.
- `proof-nontriviality-auditor`: evaluates whether a proof object is
  mathematically load-bearing.
- `proof-conceptual-quality-heuristic-rater`: rates conceptual depth,
  explanatory power, unification power, mechanism specificity, compression,
  generativity, transfer reach, falsifiability, boundary sharpness, and
  literature displacement.
- `proof-transfer-substance-auditor`: rejects principal transfer theorems whose
  conclusions follow by definition expansion, notation changes, or bridge
  predicates that already encode the target claim.
- `proof-bridge-object-forger`: designs missing objects or representation
  shifts when direct lemma proving is underdetermined.
- `proof-same-domain-transfer-certifier`: checks that the argument has not
  changed domain while preserving notation.
- `proof-creative-variant-prober`: creates controlled counterfactual or toy
  variants that expose which assumption is doing work.
- `proof-inference-learning-extractor`: turns each cycle into declarative
  inference-level learning facts rather than broad learning prose.
- `proof-learning-ledger-maintainer`: accumulates target-scoped learning facts
  and makes them available to queueing, gate selection, and demotion.
- `proof-exploration-critical-mass-assessor`: decides when conceptual
  exploration has enough concrete learning to justify lock-in.
- `proof-strategy-lockin-orchestrator`: runs bounded completion cycles for a
  publication-worthy subgoal, then releases the workflow back to exploration.
- `proof-depth-release-gate`: decides promotion, demotion, quarantine, or proof
  delivery based on hard-gate movement.

## Calibration Targets

For Yang-Mills, the hard gates are:

- geometric collar realization;
- same-theory normalization;
- geometric coefficient extraction;
- strict finite or cutoff-family margin;
- same-regulator endpoint estimate;
- continuum and spectral transfer boundary.

For P vs NP, the hard gates should be target supplied, for example:

- carrier transparency;
- all-exponent uniformity;
- barrier specificity;
- reduction preservation;
- proof-complexity transfer;
- meta-complexity carrier soundness.

## Implementation Policy

These skills should be narrow and composable rather than one large
"be creative" skill. Creativity becomes operational only when it produces a
typed object, transfer law, variant, falsifier, or hard-gate decision. The stack
should preserve the existing proof-delivery and result-elaboration workflows,
but insert a depth gate before new cycles are treated as progress.

The learning ledger should be target-scoped and append-only. It should preserve
negative learning, not just successes: failed transfers, missing objects,
invalid analogies, and demoted local calculations are often the facts that make
later creative jumps possible.

Publication subgoals should be treated as a rhythm, not the end of discovery.
A completed finite theorem, obstruction certificate, worked example, or
same-domain transfer result can be meaningful as a paper even when the main
problem remains open. After that subgoal is packaged, the system should return
to conceptual exploration with a sharper map of what was actually learned.

For Yang-Mills specifically, every publication consolidation must keep two
levels visible. The local level is a finite Route A subgoal: the reflected-Wilson
Schur-Feshbach theorem, an explicit H,K collar or hairpin object, or the
post-H,K endpoint-box R/kappa_4 sign or interval certificate. The larger level
is the Clay target: construction of a four-dimensional Yang-Mills quantum field
theory satisfying OS/Wightman axioms, nontrivial continuum limit, and positive
Hamiltonian mass gap in the same theory. A local consolidation may explain,
compute, or certify one gate, but it must also state which larger gates remain
untouched. Fixed-cutoff positivity, endpoint estimates, symbolic collars, and
same-theory markers must never be presented as a continuum mass-gap proof
without the missing transfer and spectral certificates.

The structured implementation backlog is:

`agentic/todos/proof_depth_control_stack_todos.yaml`
