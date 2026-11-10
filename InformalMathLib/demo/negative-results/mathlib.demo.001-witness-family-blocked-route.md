<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Witness family blocked route

- Result ID: mathlib.demo.001
- Outcome: blocked
- KB ref: demo
- Queue ID: proofq.demo.001
- Attempt ID: attempt.demo.001
- Bridge ID: bridge.001
- Source statement: st.src
- Target statement: st.tgt
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No admissible Witness family currently realizes the source theorem in a way that preserves the witness complexity profile strongly enough to reach the target theorem.

## Summary

The route is locally blocked by the missing carrier-realization theorem.

## Informal Proof Or Disproof

# Proof Attempt: attempt.demo.001

- Queue ID: proofq.demo.001
- Status: blocked
- Conjecture: There exists an admissible Witness family such that the source theorem reaches the target theorem.
- Bridge: bridge.001
- Source statement: st.src
- Target statement: st.tgt

## Prompt / Inference Diagnosis

- Context status: well-posed
- Inference status: determined
- Blocking defects: 
- Minimal repair: No packet repair is needed; the current state is explicit enough for audit.
- Certainty now: medium
- Certainty if well posed: medium
- Rationale: The current dossier is explicit enough and already records a route verdict that can be audited locally.

## Local Grounding

- Source excerpt: 
- Target excerpt: 

## Queue Context

- Candidate object: Witness family
- Invariant: witness complexity profile
- Route synopsis: 
- Route lemma under test: 

## Local InformalMathLib Hits

- No local InformalMathLib hits were found.

## Web Search Gate

Default policy:

## Knowledge Source Invocation Policy

- Stage: 
- Target: 
- Target kind: 

### Source Order


### Consistency Rules


### Escalation Rules


## PDL Program

- Program ID: attempt.demo.001
- Kind: proof-attempt
- Stage: prove
- Target: There exists an admissible Witness family such that the source theorem reaches the target theorem.
- Nexus: 
- Bridge object: Witness family ()
- Positive route: There exists an admissible Witness family such that the source theorem reaches the target theorem.
- Negative route: 

Anchors:
- source-theorem: st.src
- target-theorem: st.tgt

Tensions:
- The route is locally blocked by the missing carrier-realization theorem.

Proof debt:
- None recorded.

Decision gates:
- Web search gate: not-evaluated -> Stay local until a decisive missing fact forces browsing.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The route is locally blocked by the missing carrier-realization theorem.

Decision: fill this in only if a decisive local gap appears.

## External References To Import Into InformalMathLib

If you use an external theorem, definition, or axiom, record it here in the JSON as an object with:
- `reference_type`: theorem, definition, or axiom
- `title`
- `statement`
- `source_name`
- `source_url`
- `search_query`
- `used_for`
- `notes`

## Informal Proof Or Disproof Attempt

- Theorem statement: There exists an admissible Witness family such that the source theorem reaches the target theorem.
- Route lemma under test: 
- Strategy family: 

### Informal Tactic Playbook

- No tactic playbook recorded.

### Informal Tactic Trace

- No tactic trace recorded.

### Negative-Route Heuristic

- No negative-route heuristic recorded.

### Contradiction / Impossibility Frame

- No contradiction frame recorded.

Stepwise argument:

Positive subgoal package:

- No constructive subgoal package has been recorded yet.

- No stepwise argument recorded.

Local results used:

- No local InformalMathLib results have been imported into the active proof state.

Continuation log:

- No continuation passes recorded yet.

Negative-route analysis:

- Obstruction candidate: 
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: 
- Impossibility claim: 
- Effect on claim: The route remains blocked until the carrier-realization theorem is proved.

## Critique Judges

## Final Assessment

- Outcome: blocked
- Verdict: 
- Novelty assessment: 
- Confidence: 
- Result statement: No admissible Witness family currently realizes the source theorem in a way that preserves the witness complexity profile strongly enough to reach the target theorem.
- Result summary: The route is locally blocked by the missing carrier-realization theorem.

## Major Subresult Assessment

Use this only for terminal `proved` or `disproved` outcomes that might warrant a standalone paper in `artifacts/<kb-ref>/produced_papers`.

Mandatory gates:
- Self-contained statement: False
- Mathematical inspectability: False
- Nontrivial frontier relation: False
- Independent value: False

0-3 axis scores:
- Frontier shift: 0
- Independence: 0
- Transferability: 0
- Barrier clarity: 0
- Proof closure: 0
- Search compression: 0

Threshold rule: all mandatory gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3.

- Paper candidate title: 
- Paper candidate summary: 
- Overall judgment:
