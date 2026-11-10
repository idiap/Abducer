<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Proof Discovery Language

PDL is a language for discovery programmes rather than only arguments of correctness. It treats coherence, conceptual nexus, material inference, obstruction, and governed recursion as first-class logical objects, and it distinguishes structural notation from the operations that materially transform one epistemic state into another.

## Core Claim

The language is not centered on correctness-style proofs alone. It is centered on discovery programs: coherent nexuses of anchors, tensions, bridge objects, obstructions, and governed decisions over proof debt.

## Design Principles

- Prioritize conceptual nexus before closure.
- Represent tensions and obstructions explicitly.
- Treat bridge objects as typed inferential interfaces.
- Make negative and impossibility reasoning first-class.
- Make the underlying material-inference operators explicit rather than hiding them in prose.
- Embed persistence, aggregation, and loops into the logic itself.

## Notation Layers

- **Structural Layer**: Names the epistemic objects under search: anchors, targets, tensions, nexuses, bridge objects, obstructions, programmes, debt, and gates.
  Binding: This layer says what kind of thing is currently in play.
- **Material-Inference Layer**: Names the operations that transform one epistemic object into another by licensed, non-monotonic, theorem-grounded moves.
  Binding: This layer says what inferential move is being performed underneath the structural notation.
- **Governance Layer**: Names persistence, aggregation, revision, continuation, and stop-control over discovery programmes.
  Binding: This layer says how the process keeps state, loops, and changes direction without losing epistemic discipline.

## Primitives

- `A` **Anchor**: Grounded theorem body, definition, axiom, or imported result that licenses later moves.
  Material binding: Material inference starts from anchors, not from topic labels.
  Platform binding: KB statements and InformalMathLib entries.
- `T` **Target**: The smallest nontrivial payoff or consequence worth organizing the search around.
  Material binding: Discovery is guided by consequence pressure rather than free exploration.
  Platform binding: Route target claims and queued conjectures.
- `X` **Tension**: A typed gap showing why anchors do not yet reach the target: model mismatch, invariant weakness, transport loss, or barrier pressure.
  Material binding: Tension is the primitive of discovery, because it identifies where reasoning must change form.
  Platform binding: Statement deltas, obstruction classes, and failure diagnoses.
- `N` **Conceptual Nexus**: A coherent local cluster of anchors, tensions, bridge objects, and barriers that can be reasoned over together.
  Material binding: Discovery first asks whether there is a coherent nexus before demanding correctness-style closure.
  Platform binding: Bridge portfolios, conceptual dynamics, and discovery branches.
- `B` **Bridge Object**: A witness, invariant, certificate, transport law, normal form, or surrogate problem that could make the target reachable.
  Material binding: Bridge objects express the conceptual breakthrough required by the search.
  Platform binding: Bridge plans, abstraction conjectures, and candidate carriers.
- `O` **Obstruction**: A barrier, counterexample pattern, impossibility theorem, or non-realization diagnosis that blocks a route.
  Material binding: Negative mathematics is first-class discovery content, not only a failed proof attempt.
  Platform binding: Blocked results, negative programs, and obstruction maps.
- `P` **Discovery Program**: A paired positive/negative route over a nexus, together with proof debt, decision criteria, and revision triggers.
  Material binding: A discovery program is the unit of guided scientific work, not an isolated proposition.
  Platform binding: Proof sketches, queue entries, and branch dossiers.
- `D` **Proof Debt**: The set of missing lemmas, unrealized carriers, transport laws, and closure obligations still required for completion.
  Material binding: Debt is what makes discovery governable instead of open-ended.
  Platform binding: Macro-strategy reports, proof obligations, and critique findings.
- `G` **Decision Gate**: A criterion for continue, revise, import prior art, split regimes, or stop.
  Material binding: Scientific discovery requires explicit transition rules, not only local generation.
  Platform binding: Work loop, web-search gate, high-reward watch, and meta triggers.

## Material-Inference Operations

- `ext(A => c)` **Extract**: Read a theorem body, definition, or axiom as a usable local commitment rather than as raw text.
  Effect: Turns a grounded anchor into claim-bearing content.
  Universal binding: licensed material consequence extraction
  Platform binding: Phase 0 normalization, statement excerpts, theorem-body normalizer
- `foc(A, T => X)` **Focus**: Localize the exact tension between grounded anchors and the intended target.
  Effect: Turns diffuse mismatch into a typed tension object.
  Universal binding: problem localization / abductive targeting
  Platform binding: statement deltas, failure diagnoses, obstruction classes
- `conc(N => B)` **Concretize**: Turn a coherent conceptual nexus into a candidate bridge object, interface, or surrogate problem.
  Effect: Moves from coherence pressure to an inspectable candidate object.
  Universal binding: abductive bridge-object formation
  Platform binding: abstraction conjectures, expert conjectures, branch-to-definition outputs
- `tr_I(B, s ~> t)` **Transport**: Move an invariant, witness condition, or theorem payload across a regime shift, representation change, or equivalence.
  Effect: Makes cross-model or cross-language claims explicit and testable.
  Universal binding: material transfer / invariant-preserving passage
  Platform binding: transport lemmas, alignment work, HoTT/coherence routes
- `fac(r => r1 o r2)` **Factor**: Split one overloaded route into smaller theorem-sized interfaces or intermediate programmes.
  Effect: Exposes hidden composition and missing middle objects.
  Universal binding: decomposition / factorization reasoning
  Platform binding: route decomposition, macro-strategy repair, categorical reframing
- `comp(B1, B2 => B)` **Compose**: Assemble several partial bridges, lemmas, or regime results into one route.
  Effect: Promotes local inferential fragments into an end-to-end programme.
  Universal binding: compositional synthesis
  Platform binding: bridge portfolios, hybridization-of-partial-bridges, route composition
- `obs(B => O)` **Obstruct**: Derive the barrier, counterexample pattern, incoherence, or non-realization result that blocks a bridge.
  Effect: Turns failed progress into explicit negative mathematics.
  Universal binding: barrier derivation / impossibility localization
  Platform binding: negative routes, blocked local theorems, contradiction-first probes
- `rev(P, O => P')` **Revise**: Update a discovery programme after an obstruction, failed proof step, or new prior-art import.
  Effect: Makes conceptual change itself explicit rather than leaving it as narrative drift.
  Universal binding: non-monotonic theory revision
  Platform binding: revision loops, branch regeneration, meta-guided restarts
- `agg({Ri} => N*)` **Aggregate**: Combine many local results, failed routes, or branch outcomes into a single higher-order nexus or search diagnosis.
  Effect: Produces a global picture rather than isolated route state.
  Universal binding: scientific synthesis / evidence aggregation
  Platform binding: branch synthesis, breakthrough profiles, plausibility aggregation
- `mem(R => M)` **Persist**: Turn a proved, disproved, blocked, or imported result into durable problem memory.
  Effect: Stops the system from rediscovering the same local mathematics repeatedly.
  Universal binding: epistemic memory consolidation
  Platform binding: InformalMathLib persistence, queue state, produced papers, prior-art imports
- `route(P => next)` **Route**: Send a discovery programme to prove, further discovery, prior-art search, or stop.
  Effect: Connects local reasoning to governance decisions.
  Universal binding: controlled transition / research governance
  Platform binding: work loop, meta triggers, high-reward continuation, queue promotion

## Relations

- `|-` **grounds**: An anchor licenses a claim or program component.
- `~` **coheres**: Items form a stable conceptual nexus under the current representation.
- `~>` **bridges**: A bridge object makes a route from anchor side to target side materially available.
- `[]` **preserves**: An invariant survives a transport or re-encoding step.
- `-|` **obstructs**: A barrier or impossibility pattern blocks a route or object.
- `=>` **reframes**: A representation shift or decomposition changes the search unit.
- `o` **composes**: Several partial bridges or programmes combine into one route.
- `||` **persists**: A discovery result becomes durable memory.
- `@` **loops**: The process re-enters discovery/prove under governed recursion.

## Judgments

- `K ; M |- A : grounded`: The KB plus InformalMathLib licenses anchor A as a grounded theorem-body object.
- `A, X => N : coherent`: Anchors and tensions form a coherent conceptual nexus worth exploring.
- `N ~> B`: The nexus suggests a bridge object B as the best conceptual move.
- `B [] I`: Bridge object B preserves invariant I across the intended route.
- `B ~> T`: If realized, bridge object B materially supports the target consequence T.
- `B -| O`: Bridge object B is blocked or sharpened by obstruction O.
- `N ; B |- P`: A coherent nexus and bridge object together induce a discovery program P.
- `P |- D`: A discovery program exposes its proof debt explicitly.
- `P ; O |- impossibility(T)`: A negative route yields a theorem-shaped impossibility or non-realization claim.
- `P ; G @ next`: A decision gate routes the programme into prove, revision, prior-art import, or stop.

## Operational Judgments

- `A ; T |-m X`: Materially focus the mismatch between anchors and target into an explicit tension X.
- `A ; X |-m N`: Stabilize anchors and tensions into a coherent conceptual nexus N.
- `N |-m B`: Concretize the nexus into a bridge object, map, witness family, or surrogate problem B.
- `B ; I ; s->t |-m tr_I(B)`: Transport invariant I through bridge B from source regime s to target regime t.
- `r |-m fac(r1,...,rn)`: Factor a route r into smaller theorem-sized route fragments.
- `B |-m O`: Derive an obstruction O from the current bridge or route proposal.
- `P ; O |-m P'`: Revise programme P into a new programme P' after a negative result or barrier localization.
- `{Ri} |-m N*`: Aggregate many local route outcomes into a higher-order nexus or diagnosis N*.
- `R |-m M`: Persist result R into durable memory object M.

## Coordination Logic

- **Coherence Before Closure**: A route is first judged as a coherent nexus of anchors, tensions, and bridge commitments before it is judged as correct.
- **Positive/Negative Symmetry**: Every discovery program carries both a constructive route and a negative/impossibility route, each capable of yielding mathematical value.
- **Material Inference First**: Inference moves are justified by theorem bodies, model regimes, barriers, and transport obligations before any correctness-style closure is attempted.
- **Persistent Scientific Memory**: Queues, InformalMathLib, logs, and branch states are part of the logic itself because discovery depends on not forgetting failed and partial routes.
- **Governed Recursion**: Loops are legitimate only when proof debt, obstruction pressure, or high-value subresults justify another cycle.

## Control Objects

- **Problem KB** (`kb`): Anchor store and source corpus.
- **InformalMathLib** (`mathlib`): Persistent theorem memory and imported prior art.
- **Proof Queue** (`proof_queue`): Theorem-shaped frontier for proof or disproof.
- **Discovery Branch Queue** (`discovery_branch_queue`): Pattern-shaped frontier for conceptual exploration.
- **High-Reward Watch** (`high_reward_watch`): Continuation control for major subresults.
- **Meta Reflection** (`meta`): Interpretive layer over what changed in understanding.

## Well-Formed Discovery Program

- At least one grounded anchor and one explicit target.
- A typed tension explaining why the route is not immediate.
- A coherent nexus rather than a bag of related statements.
- A positive route, a negative route, and explicit proof debt.
- A decision gate specifying continue, revise, import, split, or stop.

## Example Program

```text
A1: source theorem body
A2: target theorem body
A3: local barrier theorem
X1: transport from source regime to target regime loses the intended invariant
N1 := cohere(A1, A2, X1, barrier=A3)
B1 := witness family preserving the source-side hardness profile
Operations:
- ext(A1 => c1): extract the usable lower-bound content from the source theorem body
- foc(A1, T1 => X1): isolate the exact transport loss between source and target
- conc(N1 => B1): propose the witness family as the bridge object demanded by the nexus
- tr_I(B1, source ~> target): test whether the invariant survives the intended transport
- obs(B1 => O1): derive the non-realization barrier if the witness family collapses
- rev(P1, O1 => P2): revise the route into a transport-obstruction programme
- mem(O1 => M1): persist the blocked result into InformalMathLib as negative local theorem memory
If B1 is realizable and preserves the invariant, reduce target T to one route lemma L
If every realization of B1 collapses into the barrier, derive impossibility(B1 -> T)
Debt:
- L1: carrier realization
- L2: transport theorem
- L3: payoff forcing theorem
Gate:
If L1 sharpens but L2 fails under barrier A3, reframe as transport-obstruction rather than continue constructive forcing
```
