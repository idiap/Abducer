<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Epistemic Prompt Framework

This document defines the transferable prompt shape for bridge planning, abstraction conjecture, and proof-sketch assessment across mathematical problem spaces.

## Core Principle

All reasoning in these stages is generative and interpretive, but only after theorem-body normalization and assertion licensing.

- Do not treat the task as a lexical or syntactic matching problem.
- Use structured artifacts as evidence, but interpret them as signs of inferential roles, conceptual tensions, regime boundaries, and bridge opportunities.
- Ask what is conceptually missing, what kind of object could carry the inference, and what would show that the route is impossible or mis-specified.

## Intent Gate And Self-Contained Context

Every prompt that uses this framework should begin by making the task self-contained for the model.

Before any substantive reasoning, the prompt or first model step should restate:

- the intent gate: why this prompt is the right skill for the current request rather than an adjacent one;
- the exact problem or `kb_ref`;
- the exact claims, routes, bridge objects, hypotheses, or artifacts in scope;
- the exact decision to make or artifact to produce;
- the evidence policy, constraints, and output shape.

If any of those items are missing, the prompt should say so explicitly rather than relying on hidden repository context, silently broadening the task, or inventing defaults that were never specified.

This is not a stylistic preference.
It is part of the epistemic contract.
A prompt that leaves scope, artifacts, or decision boundaries implicit makes it harder to tell whether a result is grounded, conditional, conjectural, or merely narrative.

## Context Diagnosis And Qualified Certainty

When the task requires a substantive inference rather than pure extraction, formatting, or rendering, prompts should force an explicit self-critical diagnosis before any confident conclusion.

Separate two axes:

- `context_status`: `well-posed` | `partially-ill-posed` | `ill-posed`
- `inference_status`: `determined` | `underdetermined` | `difficult-but-well-posed`

Use `ill-posed` when theorem bodies, routes, bridge objects, models, thresholds, requested outputs, or artifact packets are truncated, schematic, mutually inconsistent, or otherwise not self-contained enough to support the requested inference.

Use `difficult-but-well-posed` only when the packet is explicit enough that a strong reasoner could in principle attempt the step, but the mathematics itself is genuinely hard, unresolved, or blocked.

Do not launder prompt defects, context defects, or representation defects into apparent mathematical depth.

If `context_status` is not `well-posed`, the prompt should require:

- the exact blocking prompt/context defects;
- the smallest repair that would make the task self-contained;
- a statement of which parts of the current output are prompt/context diagnosis rather than mathematical conclusion.

If the prompt expects a report, table, narrative assessment, or recommendation output, it should require a short leading `Prompt/Inference Diagnosis` block before the main result rather than burying the diagnosis later in prose.

Prompts should also require two calibrated certainty estimates:

- `certainty_now`
- `certainty_if_well_posed`

Use only qualified levels:

- `very-low`
- `low`
- `medium`
- `high`

These are calibration labels, not evidence.
They estimate how stable the inference is under the current packet, and how stable it would be if the packet were repaired without changing the substantive theorem pair.

## Meta Prompt: Context-Versus-Inference Diagnosis

When a skill makes a nontrivial inferential move, add a short meta-prompt pre-pass:

1. Is the current packet self-contained enough to support the requested inference?
2. If not, what exact defects make it ill-posed?
3. What is the smallest packet repair that would make the task well behaved?
4. Assuming the packet were repaired but the theorem pair stayed the same, would the inference still look hard?
5. What is the calibrated certainty now, and what would it be under a well-posed packet?

Preferred return fields:

- `context_status`
- `inference_status`
- `blocking_defects`
- `minimal_repair`
- `certainty_now`
- `certainty_if_well_posed`
- `rationale`

## Inference-Quality Probe Stack

When the goal is to prevent spurious inferences rather than merely to score plausibility, use multiple probe surfaces instead of one omnibus critic.

Recommended probe order:

1. `premise-completeness-prober`
   Ask whether every premise actually required by the step is present and explicit.
2. `entailment-gap-auditor`
   Ask whether the cited evidence entails the claim or only supports it heuristically.
3. `regime-shift-auditor`
   Ask whether the move preserves quantifiers, models, thresholds, and representation regime.
4. `counterfactual-route-prober`
   Ask whether the route survives minimal perturbations or is brittle under nearby variants.
5. `counterexample-hunter`
   Ask whether a nearby local failure pattern, barrier analog, or model mismatch already defeats the step.
6. `bridge-object-equivalence-checker`
   Ask whether multiple bridge carriers are actually equivalent or silently route-breaking.
7. `epistemic-status-ledger`
   Reclassify the surviving claims so support, coherence, and novelty do not masquerade as proof.

Each probe should return one decisive defect, one decisive survival signal, or one exact next test.
If a probe cannot do that, the packet is usually still too vague.

## Three Movements

The prompt system should always separate three epistemic movements.

### Phase 0: Theorem-Body Normalization

Goal:

- restate source-side and target-side statements in theorem-body form rather than topical shorthand;
- disambiguate hypotheses, quantifier regime, ambient model, threshold language, and admissibility conditions;
- classify each active claim as a grounded local theorem, a conditional route claim, a conjectural bridge-object proposal, or a research recommendation;
- state what evidence licenses each claim, what would overturn it, and what would count as decisive progress.

This phase is about saying what can be asserted before inventing bridges.

### Phase 1: Bridge-Object Shaping

Goal:

- identify what conceptual interface is missing;
- hypothesize the object, invariant, representation, certificate, witness, or transport law that would bridge it;
- state what this object would need to preserve;
- state what barrier or impossibility pressure it is exposed to.

This phase is about object formation, not proof completion.

### Phase 2: Proof-Space Assessment

Goal:

- assess whether the hypothesized object could plausibly support a constructive route;
- assess whether the same object is likely blocked by an impossibility, obstruction, collapse, or negative theorem pattern;
- generate proof sketches for both the positive and negative directions when appropriate.

This phase is about feasibility and failure structure, not only support.

## Universal Question Set

Every epistemically informed prompt in this area should force answers to the following.

### 0. Assertion License

- What exact theorem body or artifact excerpt licenses the current claim?
- What is the claim type: grounded local theorem, conditional route claim, conjectural bridge-object proposal, or research recommendation?
- Which quantifiers, models, thresholds, or admissibility conditions are doing real inferential work?
- What observation would overturn the claim?
- What would count as decisive progress rather than additional scaffolding?

### A. Inferential Target

- What exact target consequence is the system trying to make testable?
- What is the smallest non-superficial payoff that would count as success?

### B. Source Support

- Which statements, theorem families, or regimes provide the strongest source-side support?
- Which parts of that support are genuinely inferential rather than topical?

### C. Missing Interface

- What prevents the current source-side material from reaching the target?
- Is the failure due to model mismatch, transfer-law absence, invariant weakness, barrier pressure, or theorem-family mismatch?

### D. Candidate Bridge Object

- What kind of mathematical object would make the bridge more specific?
- Is it a witness, invariant, representation, certificate, normal form, surrogate problem, transport rule, or obstruction object?
- What are its necessary and sufficient attributes?

### E. Positive Route

- If the object exists in the right form, what constructive route becomes available?
- Which lemmas or obligations would then become the main burden?

### F. Negative Route

- What kind of impossibility, obstruction, collapse, or barrier theorem could block the object or the route?
- Could the most informative outcome be a proof that no such object can exist under the current commitments?

### G. Decision Value

- What observation would increase confidence in the object?
- What observation would refute it or force re-encoding?
- Is the object still worth exploring even if the positive route fails, because it sharpens a negative theorem or impossibility frontier?

## Transferable Output Shape

Prompts should prefer the following structure.

1. Theorem-body normalization and assertion license
2. Problem-facing bridge diagnosis
3. Candidate bridge object
4. Positive construction sketch
5. Negative/impossibility sketch
6. Comparative feasibility assessment
7. Revision triggers

## Parallel Mathematical Packet

When a prompt or artifact proposes a theorem-sized bridge, transport law, equivalence, obstruction, or route lemma, the result should not remain purely verbal.

Use a parallel three-layer packet:

- `informal`: the readable mathematician-facing prose statement and gloss;
- `latex`: a compact notation-first theorem statement plus a local symbol ledger;
- `lean_style`: a Lean-style type-theory scaffold that names the types, witnesses, predicates, and theorem shape.

The Lean-style layer is not required to be executable Lean.
It is a notation-disciplined scaffold whose job is to expose:

- the carrier type or family under quantification;
- the admissibility predicate;
- the route-side and target-side objects;
- the bridge witness shape;
- the invariant-preservation predicate;
- the exact theorem type being claimed.

Do not let the Lean-style layer pretend that the theorem is formalized if it is only schematic.
Label it explicitly as a non-executable scaffold when that is the case.

At minimum, a theorem packet should carry:

- `quantifier_signature`
- `object_signature`
- `symbol_ledger`
- `latex.theorem_statement`
- `lean_style.scaffold`

Terms such as `equivalence`, `transport`, `coherence`, `factorization`, or `commutativity` are not epistemically acceptable on prose alone.
If those words appear, the packet should also say what the witness is, what its domain and codomain are, and what exact law it satisfies in notation.

## Lean/Lake Bounded Search Contract

When discovery artifacts include a `lean_symbolic_search` packet, prompts should treat it as a bounded symbolic search layer over a finite typed fragment, not as an already formalized proof.

Keep three representations separate:

- `informal` and `mathematical_layers`: human-inspectable theorem packets;
- `lean_symbolic_search`: bounded search diagnostics over typed route signatures;
- executable formal proof objects: only present if a real Lean theorem has actually been proved.

Prompts that consume discovery branch executions, routed theorem packets, or governor reports should read at least:

- `lean_symbolic_search.build_ok`
- `lean_symbolic_search.routes[*].readiness.mode`
- `lean_symbolic_search.routes[*].readiness.blockers`
- `lean_symbolic_search.routes[*].search_shapes`
- `lean_symbolic_search.routes[*].candidate_count`
- `lean_symbolic_search.candidates[*]`

Readiness modes should be interpreted explicitly:

- `llm-first`: the route is still too under-typed for useful bounded symbolic search;
- `hybrid-llm-plus-symbolic`: the route is partially typed and symbolic search is informative but not sufficient;
- `symbolic-search-ready`: the route is typed enough that bounded search over bridge shapes is a meaningful discovery move.

Search shapes such as `realization`, `transport`, `equivalence`, `factorization`, and `obstruction` are route-shaping evidence.
They are not by themselves proof.
They should guide which theorem packets to generate, which branch family to deepen, and which obstruction family is locally active.

Prompts should enforce the following interpretation rules:

- `build_ok = false` is a tooling or context defect unless the artifact explicitly proves a mathematical impossibility;
- `search_shapes` and generated symbolic candidates are evidence about the local search space, not proof that the corresponding theorem holds;
- `candidate_count = 0` is only weak negative evidence, and only when the route was `symbolic-search-ready` and the build succeeded;
- the model should say whether a claim is licensed by theorem bodies, by bounded symbolic search, or only by prose conjecture.

Do not let the presence of a Lean module path, generated scaffold, or successful build masquerade as theorem formalization.
Only call a result formalized or proved in Lean when the artifact contains an actual checked proof object for the specific theorem.

## Mandatory Claim Discipline

Every prompt in this framework should explicitly declare five things for the main claims it emits:

- evidence used;
- claim type;
- assertion license;
- overturn conditions;
- decisive progress condition.

Coherence, novelty, and structural fit are not themselves evidence.
They are at most reasons to keep a claim live.

## Knowledge-Source Order

Every stage that searches for similar results, objects, or frameworks should follow the same source order.

1. local KB statement bodies and current artifacts
2. local InformalMathLib retrieval
3. IDE-based generative search for candidate abstractions or similar structural solutions
4. web search for decisive exact prior art or external foundations

This order is epistemic, not merely operational.

- InformalMathLib is a local memory and retrieval layer.
  Use it first for exact theorems, definitions, barriers, and prior negative results.
- IDE-based generative search is a local conjecture-forming layer.
  Use it to propose carriers, invariants, decompositions, representation shifts, or similar frameworks only after theorem grounding is explicit enough to state the missing move.
- Web search is a last-resort exact-fact layer.
  Use it only after a recorded local failure and only when an exact theorem statement, prior-art fact, threshold, named framework, or barrier result is decisive.

Generative similarity is never by itself evidence.
If an externally found theorem, definition, axiom, or named framework becomes proof-relevant, it must be imported into InformalMathLib rather than left as loose inspiration.

## Evidence Classes

Every narrative artifact should be readable through the following classes:

- grounded local theorem: directly licensed by a local KB or InformalMathLib statement body;
- conditional route claim: licensed by a theorem pair plus explicit missing obligations;
- conjectural bridge-object proposal: typed but not yet established;
- research recommendation: governance, prioritization, or next-step advice rather than mathematical content.

If a sentence cannot be placed into one of these classes, it is likely too vague.

## Positive and Negative Symmetry

The prompt should not treat negative reasoning as a fallback.

Instead:

- constructive proof sketches and impossibility sketches are parallel assessments of the same bridge object;
- negative results are productive when they expose a missing invariant, a forbidden transport law, or a theorem-family incompatibility;
- impossibility-oriented sketches should be evaluated for epistemic payoff, not just for refutation power.

## Assessment Axes

For every bridge object or proof sketch, evaluate at least:

- inferential specificity;
- constructive feasibility;
- negative/impossibility plausibility;
- barrier exposure;
- theorem-family alignment;
- operationalizability on current artifacts;
- revision value if the route fails.

## Broader Discovery Patterns

Bridge-object search is central, but it is not the whole discovery landscape.
When a route remains blocked, prompts should also be able to shift into broader epistemic modes.

### Invariant Discovery

- search for the quantity, structure, or monotone property that the route is really trying to preserve;
- ask whether the right breakthrough is a better invariant rather than a better carrier name;
- prefer invariants that both sharpen positive routes and make negative routes more decisive.

### Regime Localization

- search for the smallest threshold, promise-gap, model restriction, or asymptotic regime in which the route may first become true;
- treat localized theorems as legitimate discovery targets when they would already restructure the search space.

### Problem Representation Shift

- ask whether the current language of the problem is obscuring the inferential structure;
- search for normal forms, dual encodings, or alternative object classes that preserve the mathematical content while exposing a clearer route.

### Counterexample-Led Concept Formation

- use nearby failure patterns, barrier analogs, or near-counterexamples to induce a better concept;
- ask what concept would separate the surviving positive cases from the failures.

### Route Decomposition

- split a blocked route into smaller interfaces when one bridge object is carrying too many inferential roles at once;
- identify which decomposed interface would already yield a standalone contribution if resolved.

### Hybridization Of Partial Bridges

- do not assume that one bridge object must do all the work;
- search for compositions of partial bridges, each carrying a distinct inferential burden, with an explicit intermediate theorem connecting them.

## Prompt Language Guidance

Prefer verbs such as:

- identify
- isolate
- articulate
- preserve
- transport
- obstruct
- falsify
- sharpen
- certify
- rule out

Avoid prompts that mainly ask for:

- similarity,
- analogy without transfer,
- topical overlap,
- or generic brainstorming detached from theorem-family commitments.

## Skill-Specific Emphasis

### Bridge Planner

Focus on:

- which interfaces deserve bridge-object shaping;
- which bridges are likely to produce either constructive routes or informative impossibility frontiers.

### Conjecturer

Focus on:

- what object families would close the conceptual gap;
- how those objects differ from superficial analogies;
- which negative theorem or barrier pressure should already be attached to the object proposal.

### Proof Sketcher

Focus on:

- paired positive and negative proof sketches around the same bridge object;
- what would make the object constructive, and what would prove it impossible, unstable, or non-payoff-generating.

### Expert Paper Generator

Focus on:

- explaining why the current bridge portfolio, rather than isolated hypotheses, is the right unit of expert attention;
- showing how positive and negative proof-space assessments justify the ranking of those bridges;
- distinguishing well-grounded bridge commitments from conjectural scaffolding and open failure probes.

## Artifact Grounding

Prompt judgments should be tied to the artifact family that licenses them.

### Connector Analysis

Use for:

- source-side inferential support;
- theorem-family alignment already visible in the KB graph;
- the current interface mismatch between statements, methods, and barriers.

Do not use connector similarity alone to justify a bridge object.

### Entrypoints and Pathways

Use for:

- leverage ordering;
- sequencing of bridge programs;
- whether a bridge sits on an active route rather than an isolated conceptual curiosity.

### Hardness and Barrier Reports

Use for:

- likely impossibility or obstruction families;
- barrier pressure already attached to a route;
- whether a negative result would be epistemically central rather than merely eliminative.

### Bridge Plans

Use for:

- the highest-value missing interfaces;
- candidate transport programs;
- early ranking of where bridge-object shaping should happen first.

### Abstraction Conjectures

Use for:

- candidate object families;
- necessary and sufficient attributes;
- counterfactual probes that separate genuine bridge objects from superficial analogies.

### Strategies and Proof Sketches

Use for:

- constructive family selection;
- proof obligations and candidate lemmas;
- abort conditions and negative-route checkpoints.

### Hypothesis and Coherence Artifacts

Use for:

- global fit of a bridge within the broader research program;
- whether a bridge sharpens coherence or introduces unsupported tension;
- whether failure is still revision-worthy.

## Bridge-Object Contract

Every reusable epistemic prompt should force explicit statements of:

- target consequence;
- source regime and target regime;
- missing interface;
- candidate bridge object, witness, invariant, or transport law;
- preserved quantity, structure, or admissible transformation;
- minimal existence or realizability conditions;
- main constructive obligation;
- main impossibility or obstruction probe;
- revision trigger if the route fails.

If these fields cannot be filled with theorem-family-specific content, the prompt is still too vague.

## Failure Mode Taxonomy

When a route fails, prompts should classify the failure rather than collapsing all failure into "insufficient evidence."

### Model Mismatch

- the source and target live in incompatible object classes, quantifier regimes, or semantic settings.

### Missing Transport Law

- the right object type may be visible, but no valid reduction, simulation, reconstruction, or transfer principle is available.

### Invariant Weakness

- the proposed object does not preserve what the target consequence actually depends on.

### Barrier Collision

- the route falls directly into a known obstruction, lower-bound pattern, collapse argument, or impossibility family.

### Theorem-Family Mismatch

- the route borrows the wrong style of proof and therefore asks the object to do work outside its legitimate regime.

### Payoff Collapse

- the object may exist, but even in the best case it would not force a nontrivial target consequence.

## Minimal Reusable Prompt Scaffold

The shared framework can be instantiated with the following minimal skeleton.

```markdown
Inputs:
- artifacts: {{artifacts}}
- target regime: {{target_regime}}
- current bridge candidates: {{bridges}}

Task:
1. Diagnose the highest-value missing interface.
2. Propose the bridge object, invariant, witness, certificate, or transport law that would make the interface testable.
3. State the exact target consequence this object would make reachable.
4. Give both:
   - a constructive route if the object exists in the right form;
   - a negative or impossibility route if the object cannot exist or cannot preserve the needed structure.
5. Compare this bridge against nearby alternatives.
6. State revision triggers.

Required output:
### Bridge Diagnosis
- target consequence
- source-side support
- missing interface

### Candidate Bridge Object
- object type
- preserved invariant
- necessary attributes
- sufficient attributes

### Positive Route
- proof-family choice
- main obligations
- candidate lemmas

### Negative Route
- obstruction family
- targeted assumption
- decisive falsifier

### Decision
- why this bridge is worth continuing, sharpening, splitting, or abandoning
```

## Mathematical Content Contract

Intermediate artifacts must be strong enough for a mathematician to inspect the inferred route without reverse-engineering the orchestration layer.

Every bridge, conjecture, and proof-sketch artifact should therefore expose:

- source regime and target regime in mathematical, not procedural, terms;
- a conditional theorem template of the form "if this object exists and preserves this invariant, then this consequence follows";
- a bridge-object definition or admissibility profile, even if provisional;
- theorem-shaped obligations and lemma statements, not only labels or execution commands;
- an explicit obstruction or failure mode stated in the same mathematical vocabulary.

If an expert can only recover the route by reading `run kb-deduce`, `retain only if`, or other pipeline-control language, the artifact is still too execution-oriented.

## Expert-Inspectable Logging

Reasoning logs should summarize content-bearing claims, not only stage progress.

For each stage, log:

- the top theorem templates or conditional claims under consideration;
- the bridge object currently being proposed or tested;
- the invariant being transported;
- the first unresolved mathematical obligation;
- the most informative failure mode or barrier collision.

The log should let an expert answer "what is the mathematical claim here?" before "what script was run?".

## Prompt Quality Checks

Before finalizing a prompt, ask:

- Does the prompt force a theorem-family-specific bridge object rather than a thematic analogy?
- Does it make the target consequence testable rather than merely interesting?
- Does it force theorem-shaped intermediate content rather than schema names alone?
- Does it require an explicit negative route, not just a constructive hope?
- Would two genuinely different bridge objects receive distinguishable evaluations under this prompt?
- Does it say what observation would trigger revision, not only continuation?

## Revision Semantics

The framework should make downstream action clear.

- Continue when the object is inferentially specific, the constructive route is nontrivial, and the negative route is still informative.
- Sharpen when the object family looks right but the preserved invariant or realizability conditions are under-specified.
- Split when one proposed bridge object is carrying multiple incompatible inferential roles.
- Re-encode when repeated failure traces back to representation or regime mismatch rather than to the object itself.
- Abandon when both the positive and negative routes have low epistemic payoff.
