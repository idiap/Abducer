<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Discovery Loop Review

This note reviews the current discovery loop from an epistemological and conceptual-modeling perspective, with emphasis on bridge formation across the landscape of axioms, definitions, theorems, barriers, and the main conjecture.

## Current Conceptualization

The current framework already has the right global intuition:

- the evolving KB is treated as the central epistemic object;
- discovery is not reduced to one-shot proof search;
- the pipeline explicitly models concepts, methods, barriers, hypotheses, coherence, and revision;
- bridge planning and gap-abstraction conjecture already push beyond fact retrieval into concept formation.

In practical terms, the discovery loop is:

1. landscape formation from KB statements and concept profiles;
2. bridge-hypothesis generation over promising interfaces;
3. coherentist evaluation of local moves against global fit;
4. entrypoint and pathway ranking;
5. hardness diagnosis and barrier articulation;
6. bridge-program planning;
7. abstraction conjecture for missing intermediate objects;
8. proof-sketching, hypothesis testing, and revision.

That is already a strong epistemological framing. The main remaining gap is not that the system lacks a discovery view, but that the discovery view is still only partially encoded in the data structures.

## Spirit-Aligned Limitations

These are the limitations that matter most if the goal is to create conceptual bridges from the existing theorem-and-axiom landscape.

### 1) Bridges Are Still Mostly Pairwise Programs

The current bridge machinery is strongest at ranking statement-to-statement interfaces, but a mature discovery framework needs bridge objects to be first-class evolving entities.

Current pattern:

- `analyze_kb_graph.py` produces `connection_candidates` between statements;
- `plan_bridges.py` ranks `from_id -> to_id` programs;
- `conjecture_gap_abstractions.py` repairs gaps after those pairs are chosen.

Opportunity:

- represent a bridge as its own object with source regime, target regime, transport law, preserved invariant, failure modes, and admissible abstraction families;
- let bridges persist across iterations as evolving conceptual commitments, not just one-round ranked links.

### 2) Concept Profiles Are Richer Than Topics but Still Too Flat

The connector already extracts claim, antecedent, consequence, model, reduction, regime, and barrier signatures. That is a real strength. But these fields still behave mostly like aligned signature bags rather than structured conceptual models.

Opportunity:

- add explicit causal or inferential roles such as witness object, transport mechanism, reconstruction rule, observable, obstruction, and admissible deformation;
- model when two statements share vocabulary but not inferential identity;
- distinguish bridgeability from mere similarity.

### 3) The Axiom-to-Theorem Landscape Is Under-Explicit

The framework can represent definitions and theorems, but the discovery loop would benefit from a more explicit landscape layer over:

- axiomatic regimes,
- reconstruction interfaces,
- admissible model transitions,
- theorem-family templates,
- theorem-to-barrier exposure.

Opportunity:

- build a dedicated theorem-landscape atlas that exposes which axioms feed which theorem schemas and where the conjecture sits relative to those interfaces;
- represent regime boundaries directly in the graph instead of inferring them only from tags.

### 4) Barriers Are Diagnosed but Not Yet Geometrized

`kb-epistemic-hardness` is useful, but hardness mainly appears as a downstream report rather than as a central geometric structure in the discovery space.

Opportunity:

- treat barriers as regions, cuts, or forbidden transfers in the conceptual graph;
- make barrier pressure visible at the exact interfaces where bridge programs fail;
- expose which conjectured abstractions neutralize which barrier families.

### 5) Revision Is Still More Local Than Conceptual

The revision loop proposes ontology or representation repair, but it does not yet fully close the loop between:

- failed bridge programs,
- missing bridge-object attributes,
- theorem-landscape distortions,
- and revised conceptual encodings.

Opportunity:

- feed bridge failure explanations directly into ontology revision;
- revise not only nodes and definitions, but also the conceptual bridge schema itself.

### 6) The Process View Is Stronger Than the Discovery-Space View

The repo already visualizes process execution and reasoning dynamics well. What is weaker is a visualization of the evolving conceptual space itself.

Opportunity:

- replay not only which stage ran, but which conceptual entities entered the space at each stage;
- show hypotheses, bridge programs, abstraction conjectures, and hardness elements as they appear;
- present discovery as expansion and restructuring of a conceptual graph, not only as orchestration telemetry.

## Highest-Value Improvements In This Spirit

These are the most aligned next moves if the goal is concept-driven bridge formation.

### 1) Introduce a First-Class Bridge Object Schema

Each bridge should carry:

- source statement or regime;
- target statement or regime;
- transport law;
- preserved invariant;
- bridge type;
- barrier scope;
- abstraction gap profile;
- testability conditions;
- revision history.

This would unify bridge planning, conjecture, proof-sketching, and revision around the same conceptual object.

### 2) Build a Theorem-Landscape Layer

Add an explicit layer over the KB for:

- axioms and axiom systems;
- theorem families;
- reconstruction theorems;
- reduction regimes;
- boundary theorems and impossibility interfaces;
- target-conjecture adjacency.

This would make the main conjecture legible as a location in a landscape, not just a target statement.

### 3) Make Bridge Failure Productive

When a bridge fails, the system should say whether the failure is due to:

- model mismatch;
- missing invariant;
- lack of transport rule;
- barrier conflict;
- wrong abstraction family;
- or underdetermined theorem schema.

Those failure modes should directly generate:

- revised bridge-object definitions;
- new conjectured abstraction families;
- or KB revision actions.

### 4) Promote Abstractions to Visible Discovery Objects

The conjecturer already produces definitional profiles and counterfactual probes. Those should be visually and operationally central.

Needed upgrade:

- abstraction conjectures should be visible beside statements and bridge programs;
- each abstraction family should be linked to the exact gap axes it addresses;
- users should be able to inspect which abstractions are conjectural repair attempts versus structural discoveries.

### 5) Add Frontier Metrics for Conceptual Exploration

In addition to coherence and graph growth, the framework should track:

- frontier width: how many plausible unexplored bridges remain;
- barrier tension: how much high-value activity is clustered near obstruction zones;
- abstraction pressure: how many top bridges are blocked by missing intermediate objects;
- regime distance: how far current candidates try to jump across incompatible theorem regions.

These would better express the dynamics of discovery than execution counts alone.

## Other Improvement Opportunities

These are important, but they are less central to the conceptual-bridge spirit.

### 1) Close the Executable Gap for Prompt-Only Skills

Executable wrappers for `kb-abduce`, `kb-deduce`, `kb-explain`, and `kb-induce` would make the loop more auditable and easier to benchmark end-to-end.

### 2) Add Automatic Evidence Compilation

The evaluator already consumes evidence well. An evidence compiler would reduce manual glue between stages.

### 3) Strengthen Dependency Hygiene

Sparse `depends_on` structure still limits graph reliability. A dependency linter and dependency-suggestion stage would improve the landscape quality.

### 4) Calibrate by Domain

Complexity theory, constructive QFT, operator theory, and fixed-point theorems have different bridge geometries. Domain profiles should tune scoring and thresholds.

### 5) Benchmark Discovery Quality, Not Only Contracts

The current test suite is strong on contracts and regressions. The next evaluation layer should measure:

- whether top bridges match known discovery routes;
- whether conjectured abstractions resemble known intermediate objects;
- whether revision actions improve later-stage conceptual fit.

## Visualization Direction

The preferred discovery visualization should show:

- the base theorem landscape first;
- then the explicit hypothesis layer;
- then coherence links;
- then barrier and hardness overlays;
- then bridge programs;
- then abstraction conjectures.

The visual grammar should make clear:

- what is known,
- what is proposed,
- what is blocked,
- what is being used as a transport object,
- and what is still conjectural.

That is the motivation for the new `generate_discovery_graph_explorer.py` utility added in this revision. It complements the existing process-graph and reasoning-dynamics views by replaying the emergence of conceptual entities over the discovery stages themselves.

## Immediate Next Steps

1. Adopt a first-class bridge-object contract shared across bridge planning, conjecture, proof sketches, and revision.
2. Extend the KB representation with a theorem-landscape layer over axioms, theorem families, and regime boundaries.
3. Promote abstraction conjectures and bridge failures to central artifacts rather than downstream explanations.
4. Benchmark whether the refined loop improves recovery of known discovery trajectories, not just artifact consistency.
