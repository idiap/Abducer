<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Epistemic Systems Visual Language

Library: Cytoscape.js

## Design

A typed directed graph with a stable preset layout fits epistemic circuits better than a force layout because the agent society has known phases, persistent stores, recurrent control loops, and a process spine that should remain legible across runs.

The map binds platform-specific agents to universal inference functions: grounding, generation, aggregation, critique, persistence, routing, and reflection.

## Lanes

- `\mathcal{K}` **Grounding**: Normalize claims, anchor them in source theorems, and control what can be asserted. Question: What can be asserted from the source material once theorem bodies, quantifiers, and models are explicit? System role: License and stabilize the inferential material before discovery begins.
- `\rightsquigarrow` **Discovery**: Generate route hypotheses, bridge objects, invariants, and new search branches. Question: What bridge object, invariant, abstraction, or route could mediate the current tension? System role: Generate and reshape the conceptual frontier rather than proving everything immediately.
- `\vdash` **Prove**: Attempt tactic-guided informal proofs, critique them, and persist usable results. Question: Which theorem-shaped subgoals, tactics, contradictions, or imports would actually close or block the route? System role: Subject discovery programmes to tactic-structured informal proof pressure.
- `\Sigma` **Governance**: Control loops, score progress, reopen promising directions, and avoid unbounded drift. Question: Should the system branch, continue, reopen, defer, or stop? System role: Control recursion, memory, prioritization, and bounded continuation.
- `\Delta` **Reflection**: Synthesize what changed, what persists, and what an expert should inspect next. Question: What changed in understanding, what remained hard, and what should an expert inspect next? System role: Turn process state into expert-visible interpretation and public reasoning surfaces.

## Epistemic Process Spine

1. `\vdash` **License Claims**: The system begins by normalizing raw statements, exposing quantifiers and models, and refusing unlicensed assertions. Guiding question: What is actually assertable from the local theorem bodies?
2. `\rightsquigarrow` **Select Leverage**: Discovery chooses entrypoints and route candidates using theorem grounding, anti-hub checks, and first kill conditions. Guiding question: Which theorem pair or tension is mathematically leverageful rather than merely central?
3. `\Sigma` **Form Conceptual Nexus**: Bridge planning, abstraction conjecture, and proof sketching turn a raw gap into a coherent discovery programme with explicit proof debt. Guiding question: What bridge object, abstraction family, or invariant would connect the source and target?
4. `\dashv` **Apply Proof Pressure**: The proof queue and prove cycle turn programmes into tactic-structured attempts, while the critic applies adversarial pressure. Guiding question: Which subgoals, tactics, contradictions, or external results decide whether the route survives?
5. `\circlearrowleft` **Govern Recursion**: Discovery branches, the work loop, and the high-reward watch prevent both premature stopping and uncontrolled depth-first drift. Guiding question: Should the system branch, continue, reopen, or stop?
6. `\Delta` **Reflect and Publish**: Expert papers, meta reflection, logs, and reasoning surfaces turn internal control state into inspectable scientific narrative. Guiding question: What changed in understanding, what remains blocked, and what should a mathematician inspect next?

## Node Types

- `\mathcal{K}` **Knowledge Store**: Persistent epistemic memory: statements, proofs, queues, logs, and reusable theorems. Epistemic move: Retain and reactivate what has already been grounded or learned.
- `\equiv` **Normalizer**: Re-expresses raw statements into typed, licensed, inspectable claims. Epistemic move: Type and license material before the rest of the system reasons with it.
- `\rightsquigarrow` **Generator**: Produces candidate routes, abstractions, branches, or proof attempts. Epistemic move: Expand the search space by proposing new inferential material.
- `\Sigma` **Aggregator**: Collects many local results into a ranked or synthesized frontier. Epistemic move: Compress many local signals into a coherent frontier or watch state.
- `\dashv` **Critic**: Tests soundness, plausibility, fidelity, or adversarial weakness. Epistemic move: Apply back-pressure so coherence does not masquerade as evidence.
- `\circlearrowleft` **Controller**: Routes work across phases, handles loops, and decides when to continue or stop. Epistemic move: Govern recursion and decide whether more work is justified.
- `\Rightarrow` **Publisher**: Turns process state into expert-facing reports, surfaces, or maps. Epistemic move: Expose internal state as an inspectable narrative or surface.
- `\Omega` **External Source**: Web or prior-art source used only when local evidence is insufficient and the search gate allows it. Epistemic move: Import decisive external structure only when local material is exhausted.

## Edge Types

- `\vdash` **Grounds**: Supplies typed source material, theorem bodies, or licensed evidence.
- `\rightsquigarrow` **Proposes**: Generates candidate claims, carriers, proof tasks, or branch programmes.
- `\Sigma` **Aggregates**: Collects many local artefacts into a unified frontier or report.
- `\dashv` **Critiques**: Evaluates consistency, evidence, plausibility, or tactical discipline.
- `\Rightarrow` **Routes**: Directs control flow across phases, queues, and search branches.
- `\parallel` **Persists**: Writes durable memory so the search does not forget what it already learned.
- `\leftarrow` **Imports**: Brings external mathematics into InformalMathLib in a reusable normalized form.
- `\circlearrowleft` **Loops**: Feeds reflected or judged state back into discovery and prove as a controlled recursion.

## Core Nodes

- **Problem KB** (`kb`): Persistent theorem bodies, definitions, axioms, and statement references for a specific problem. Universal binding: Material memory: the declarative corpus that licenses all later inference.
- **Theorem-Body Normalizer** (`theorem_body_normalizer`): Converts raw theorem prose into typed hypotheses, conclusions, quantifier regimes, and assertion licenses. Universal binding: Formal normalization: turns text into inspectable inferential units.
- **InformalMathLib** (`mathlib`): Problem-scoped memory of proved, disproved, imported, and reusable mathematical results. Universal binding: Reusable formal-material memory: local theorem inventory and prior-art cache.
- **Prior-Art Pass** (`prior_art_pass`): Targets external mathematical frameworks or theorems only when local search and InformalMathLib fail to close a decisive gap. Universal binding: External grounding: controlled import of prior formal structure.
- **Entrypoint Finder** (`entrypoint_finder`): Selects leverageful statements rather than ontology hubs, using theorem grounding and anti-hub checks. Universal binding: Epistemic targeting: where the search should start.
- **Entrypoint Pathfinder** (`pathfinder`): Builds candidate theorem-to-theorem routes together with deltas, first kill conditions, and pathway rationale. Universal binding: Inferential path search: plausible routes through the statement space.
- **Proof Connector** (`proof_connector`): Separates graph leverage from mathematical leverage and compresses candidate routes into connectable proof programmes. Universal binding: Programme assembly: connect local routes into inspection-ready search units.
- **Concept Bridge Planner** (`bridge_planner`): Posits bridge objects, statement deltas, invariants, and concrete route claims; marks underspecified carriers explicitly. Universal binding: Abductive bridge search: identify what object could support the missing inference.
- **Gap Abstraction Conjecturer** (`gap_conjecturer`): Turns blocked routes into typed conjectural objects, repair abstractions, and breakthrough-family diagnoses. Universal binding: Concept formation: move from missing step to missing abstraction type.
- **Proof Sketcher** (`proof_sketcher`): Builds theorem-shaped informal proof programmes with tactic-friendly subgoals, lemma chains, and failure probes. Universal binding: Informal derivation design: what an eventual proof would have to look like.
- **Discovery Cycle** (`discovery_cycle`): Coordinates discovery, reopens blocked routes, and enqueues search work without repeating exhausted local moves. Universal binding: Recursive search control: when and how to continue exploration.
- **Discovery Branch Queue** (`discovery_branch_queue`): Persistent branch-level memory for distinct discovery patterns, families, attempts, and status transitions. Universal binding: Search branch memory: keeps breadth-first discovery from collapsing into a single route.
- **Discovery Branch Executor** (`branch_executor`): Executes discovery branches as separate search runs and records what conceptual move each branch actually tested. Universal binding: Branch realization: turn a discovery pattern into concrete exploratory work.
- **Proof Queue** (`proof_queue`): Persistent queue of self-contained conjectures, route lemmas, and branch-promoted proof tasks. Universal binding: Task memory: what remains to be proved, disproved, or blocked.
- **Prove Cycle** (`prove_cycle`): Runs tactic-structured informal proofs, critiques each move, and finalizes results as proved, disproved, or blocked. Universal binding: Structured informal inference: controlled proof search rather than free-form prose.
- **End-to-End Proof Critic** (`proof_critic`): Assesses whether local proof state closes the main claim, respects assumptions, and survives adversarial scrutiny. Universal binding: Global proof judgment: whether the current route is actually becoming a complete solution.
- **High-Reward Watch** (`high_reward_watch`): Detects major subresults that justify bounded continuation rather than an early budget stop. Universal binding: Reward-sensitive control: protect genuinely valuable local breakthroughs from premature termination.
- **Work Loop** (`work_loop`): Alternates discovery and prove, invokes meta at key stop points, and decides whether the research programme keeps going. Universal binding: Outer epistemic control: the recursive agent society seen as one system.
- **Expert Paper Generator** (`expert_paper`): Turns the live route and its proof debt into a human-inspectable research paper narrative. Universal binding: Expert-facing synthesis: convert internal search state into mathematical exposition.
- **Meta Reflection** (`meta`): Reflects on why the problem is hard, what conceptual shift occurred, and whether the process is learning or merely organizing. Universal binding: Epistemic self-interpretation: what changed in understanding.
- **Reasoning Logs** (`reasoning_logs`): Stores fine-grained provenance of each agent action, prompt context, and emitted artefact. Universal binding: Process observability: trace what happened and when.
- **Reasoning Surfaces** (`reasoning_surfaces`): Publishes dashboards, maps, papers, and diagrams that expose the current state of the agent society to experts. Universal binding: Public epistemic surface: the inspectable big picture.
