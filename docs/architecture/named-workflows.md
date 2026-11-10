<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Named Workflows

Abducer uses named workflows to make the purpose, authority, cost, and stopping condition of a reasoning process explicit. A workflow is more than a list of skills: it identifies why work starts, which transformations may occur, what evidence must be produced, and where the result may go next.

The workflow set has two layers:

- active workflows support the current target-navigation, discovery, proof-search, release, and reporting system;
- opt-in workflows give specialized skills a clear home without making the default research loop heavier.

## Design Principles

### Keep the default path light

Routine target navigation should establish the target, dependencies, admissible actions, and release conditions. Expensive conceptual exploration, manuscript work, specialized target programmes, and deep review activate only when their own conditions are met.

### Separate scientific authority

Concept generation, conceptual preference, proof, experimental evidence, and durable state mutation are different authorities. A workflow may prepare evidence for another workflow, but it does not inherit that workflow's authority.

### Preserve typed handoffs

Each workflow should consume a recognizable input and leave a recognizable output. A proof-ready claim, failure certificate, contribution candidate, manuscript insertion, and repair queue are different objects and should not be exchanged as generic prose.

### Make hooks inspectable

Native hooks preserve the behavior of the pre-normalization `f90f0c6f` baseline.
The richer workflow selection, prerequisite, activation-receipt and output
checks live in the explicitly imported `hooks.workflow_local` package; they are
not installed as native hooks. See [hook boundaries](../../hooks/README.md).
Neither surface chooses theories or invents scientific content.

The generated named-workflow task projection lives under
`registry/optional-tasks/named-skill-workflows/`. It is deliberately outside the
native `registry/tasks/*` scan so merely generating a catalog does not authorize
additional skills in the original pre-skill hook. The original named workflow
contracts, step ordering and handoffs remain available to explicit callers.

## Active Lightweight Workflows

### Target navigation

Canonical name: `target_navigation_loop`  
Visible forms: `target-navigation-control-plane`, `p-vs-np-target-navigation-run`

Target navigation turns an open-ended research request into controlled work. It clarifies the target, acceptance conditions, dependency frontier, admissible skill set, and stopping rules before deeper reasoning begins.

The P-vs-NP form is a target-scoped specialization of the same function. It preserves the general control structure while binding the target to the relevant knowledge base, proof queue, and dependency state.

Use it when:

- a new target is introduced;
- the current target or success criteria are ambiguous;
- dependencies or proof obligations need to be refreshed;
- another workflow needs a governed starting state.

It should produce a validated target and dependency frontier, not a theorem or preferred theory.

### Discovery marathon

Canonical name: `discovery_marathon_loop`  
Visible form: `discovery-marathon-control-loop`

The discovery marathon sustains multi-cycle exploration across competing routes. It allocates effort, retains partial successes and failures, prevents one attractive branch from monopolizing the search, and turns cycle results into the next controlled frontier.

Use it when:

- the target needs repeated exploration rather than one proof attempt;
- several routes must mature in parallel;
- progress and failure must be accumulated across cycles;
- a long-horizon stopping or continuation decision is needed.

It coordinates exploration; it does not itself establish proof or scientific truth.

### Abducer work loop

Canonical name: `abducer_work_loop`

The work loop is the persistent theorem-assistance lane. It consumes concrete proof obligations, maintains queues and search state, and coordinates bounded proof or disproof attempts against the active dependency frontier.

Use it when the problem has moved from broad target selection to concrete mathematical work. Its main value is continuity: unfinished obligations, negative results, and dependency changes remain available to later cycles.

### Conceptual hypothesis exploration

Canonical name: `conceptual_hypothesis_exploration_loop`  
Visible form: `conceptual-obstruction-refinement`

This workflow responds to conceptual pressure rather than routine derivation gaps. It turns failures, tensions, and incomplete bridges into candidate mediations, representation changes, weakened or strengthened claims, and new validation obligations.

Use it when:

- proof attempts repeatedly fail for the same structural reason;
- the current representation appears inadequate;
- a missing bridge object or abstraction is suspected;
- several conceptual alternatives need comparison.

Its outputs are candidates and obligations. They return to proof or target navigation only after validation.

### Release promotion

Canonical name: `release_promotion_loop`

Release promotion interprets workflow, dependency, compliance, drift, and validation evidence. It decides whether a controlled iteration may be promoted, quarantined, rolled back, or escalated.

Use it only when durable state or an official iteration status may change. Ordinary reports, drafts, and local reasoning artifacts do not need release promotion.

### Timeline paper

Visible form: `timeline-paper-independent-workflow`

The timeline-paper workflow translates accumulated research evidence into a coherent paper narrative. It selects relevant episodes, explains conceptual change, packages finite results and worked calculations, manages claim boundaries, and reconciles sections into a consistent manuscript.

It is intentionally independent from discovery: writing the story must not mutate the theory state or retroactively upgrade evidence.

### Yang–Mills representational dynamics

Visible form: `ym-representational-dynamics-overlay`

This is a target-specific research programme for Yang–Mills existence and mass gap. It organizes observable construction, representation calculus, regulator and renormalization-group reasoning, infrared control, continuum coherence, restricted-model calibration, and proof-facing handoffs.

The overlay specializes the general discovery framework. It does not redefine the shared authority rules, and its finite or regulated results must not be promoted automatically to continuum or mass-gap claims.

## Opt-In Workflows

These workflows provide explicit homes for specialized skills that should not burden the active lightweight path.

### Evidence-to-proof-route onramp

Name: `evidence_to_proof_route_onramp`

This workflow turns source material into a defensible proof agenda. It ingests mathematical text, normalizes theorem bodies, grounds statements in the main conjecture, builds relational connections, evaluates hypotheses, corrects hub bias, ranks entrypoints, audits regime changes, and subjects candidate routes to counterexample pressure.

Conceptual transformation:

```text
source material -> normalized claims -> target-grounded graph
                -> debiased entrypoints -> adversarially tested route dossier
```

Activate it when the knowledge base is missing or stale, new mathematical sources arrive, or the user asks where proof work should begin.

Exit only when every promoted route has provenance, an explicit target implication, and a falsifier or stopping condition.

### Conceptual frontier deepening

Name: `conceptual_frontier_deepening`

This is the expensive theory-first lane. It conditions invention on the current literature, matures diverse hypotheses independently, applies reflective transformation, compares complete conceptual systems blindly, invokes formal abstraction only where structural pressure justifies it, and produces a ready-or-not-ready formal claim.

Conceptual transformation:

```text
frozen discovery context -> literature-conditioned inventions
                         -> reflected conceptual systems
                         -> plural adjudicated routes
                         -> formal claim readiness decision
```

Activate it only after repeated conceptual blockage, representation failure, or an explicit request for aggressive conceptual search. It requires a frozen context and approved budget.

Experiments remain subordinate: they may constrain later reflection but cannot select the theory that commissioned them.

### Theorem proof delivery

Name: `theorem_proof_delivery`

The proof-delivery workflow converts a theorem-shaped queue item into a formal obligation structure, lemma chain, proof attempt, gap disposition, domain-specific inference review, and proof-quality decision.

Conceptual transformation:

```text
exact claim -> formal obligations -> lemma chain
            -> proof or named obstruction -> quality-gated disposition
```

Activate it when exploration is no longer the main task and the claim has exact source, target, quantifier, and model bindings.

It may return a proof candidate, conditional result, repair obligation, countermodel, or no-go result. Only quality-gated claims move toward contribution or publication workflows.

### Scientific contribution cultivation

Name: `scientific_contribution_cultivation`

This workflow asks whether an achieved subgoal is scientifically valuable in its own right and whether it genuinely enables the larger target. It separates local progress, reusable bridges, side contributions, negative results, and target-critical gates.

Conceptual transformation:

```text
result-atlas change -> contribution candidate -> value assessment
                    -> target-enablement audit -> honest handoff
```

Activate it at meaningful result milestones rather than every cycle. Paper handoff requires a smallest honest claim, a prior-art boundary, evidence for the contribution's value, and a clear account of what remains unresolved.

### Manuscript result elaboration

Name: `manuscript_result_elaboration`

This workflow expands a result-bearing draft without reopening the discovery marathon. It interprets the paper's argument, extracts open modules and result slots, creates a bounded elaboration plan, certifies theorem scope, formalizes finite objects, derives proof packets, checks prior-art disqualifiers, integrates the result into the narrative, and assesses paper readiness.

Conceptual transformation:

```text
paper draft -> bounded result obligations -> scoped result packets
            -> validated narrative insertions -> readiness decision
```

Activate it when a draft contains explicit expansion markers or open modules. Finite, asymptotic, and continuum claims must remain separate throughout.

#### Route-A results closure profile

The Route-A profile specializes manuscript result elaboration for the reflected Wilson-block programme. It selects among collar construction, normalization, coefficient extraction, finite margins, endpoint analysis, symbolic checking, factorization, redesign, and continuum-gap review.

Target-specific specialists return the same generic result-candidate object consumed by the common manuscript validation tail. This keeps Route-A work integrated without turning it into a global default workflow.

### Deep review and reorientation

Name: `deep_review_and_reorientation`

This workflow examines the reasoning system itself. It formalizes the current framework state, collects independent reviewer perspectives, interprets what has genuinely changed in the problem understanding, and converts findings into a governed repair or reorientation queue.

Conceptual transformation:

```text
run evidence -> formal framework state -> independent critiques
             -> reflective decision -> governed repair queue
```

Activate it after repeated blockage, contradictory evidence, low explanatory power, a major architectural change, or an explicit deep-review request.

Review may recommend continuation, repair, pivot, quarantine, or stopping. It cannot establish a proof or upgrade epistemic status by itself.

## How Workflows Connect

The common progression is:

```text
target navigation
  -> evidence-to-proof-route onramp or discovery marathon
  -> conceptual exploration or conceptual frontier deepening
  -> theorem proof delivery
  -> scientific contribution cultivation
  -> manuscript result elaboration or timeline paper
  -> release promotion only when durable state must change
```

This is not a mandatory linear pipeline. Failure certificates may return proof work to conceptual exploration; a valuable local result may enter contribution cultivation without solving the main target; deep review may redirect any active lane; target-specific overlays may specialize a stage while preserving its shared gates.

## Workflow Selection Guide

| Need | Workflow |
|---|---|
| Clarify a target and its dependencies | Target navigation |
| Sustain diverse exploration over many cycles | Discovery marathon |
| Work through concrete queued obligations | Abducer work loop |
| Invent a bridge after structural failure | Conceptual hypothesis exploration |
| Convert sources into ranked proof routes | Evidence-to-proof-route onramp |
| Run expensive theory-first invention | Conceptual frontier deepening |
| Attempt and quality-gate an exact theorem | Theorem proof delivery |
| Assess whether a result is independently valuable | Scientific contribution cultivation |
| Expand open result modules in a draft | Manuscript result elaboration |
| Write the accumulated research story | Timeline paper |
| Run the Yang–Mills-specific programme | Yang–Mills representational dynamics |
| Reassess the reasoning system and direction | Deep review and reorientation |
| Promote or quarantine durable state | Release promotion |

## Completion Standard

A workflow is integrated only when its trigger, ordered skill roles, typed inputs and outputs, deterministic hook bindings, exit gate, and downstream handoffs agree. Listing a skill in a catalog or mentioning it in a dispatch phase is useful metadata, but it is not by itself evidence that the skill is executable, exercised, consumed, or feedback-effective.

## Integration Scenario Coverage

The deterministic integration suite contains one realistic positive lifecycle for each of the six named workflows and one for the Route-A profile. The cases cover a provenance-bound P-vs-NP source onramp, Yang--Mills carrier deepening, exact theorem delivery, finite-result contribution assessment, manuscript module elaboration, contradictory-run reorientation, and Route-A collar/endpoint closure.

Each lifecycle exercises structured routing, explicit activation, ordered required and conditional steps, workflow-local tool authorization, schema-valid artifact envelopes, digest-bound receipts, premature-exit rejection, the final exit gate, and a declared handoff or adapter. Negative cases cover prohibited triggers, borrowed receipts, advisory-review bypass, premature specialist use, deletion, and unapproved budgets.

These are control-plane integration tests with realistic fixture evidence. They do not execute every scientific skill or establish that a fixture claim is mathematically or empirically correct.
