# End-to-End Proof Plausibility Report

- KB ref: p-vs-np
- Plausibility score: 0.350
- Decision: continue-no-terminal-proof
- Plausible solution detected: False
- Detail: No terminal proved attempt yet carries the leading route to a candidate full solution.

## Context Vs Inference Diagnosis

### Queue Active

- Scope: Active queue rows only.
- Count: 57
- Context counts: well-posed=57, partially-ill-posed=0, ill-posed=0
- Inference counts: determined=0, underdetermined=0, difficult-but-well-posed=57

### Queue

- Scope: Current non-archival queue rows.
- Count: 74
- Context counts: well-posed=74, partially-ill-posed=0, ill-posed=0
- Inference counts: determined=0, underdetermined=0, difficult-but-well-posed=74

### Queue Historical Archive

- Scope: Retired or legacy ill-posed terminal queue rows.
- Count: 35
- Context counts: well-posed=0, partially-ill-posed=0, ill-posed=35
- Inference counts: determined=0, underdetermined=35, difficult-but-well-posed=0
- Common blocking defects: `missing_route_lemma` contains truncation markers, so the theorem state is not self-contained. (21) | `route_synopsis` contains truncation markers, so the theorem state is not self-contained. (18) | `claim_text` contains truncation markers, so the theorem state is not self-contained. (11) | `conjecture_statement` contains truncation markers, so the theorem state is not self-contained. (11) | `claim_text` still uses schema placeholders instead of concrete mathematical content. (8)

### Attempts Active

- Scope: Active attempt dossiers only.
- Count: 1
- Context counts: well-posed=1, partially-ill-posed=0, ill-posed=0
- Inference counts: determined=0, underdetermined=0, difficult-but-well-posed=1

### Attempts

- Scope: Latest current attempt dossiers after collapsing superseded retries.
- Count: 24
- Context counts: well-posed=24, partially-ill-posed=0, ill-posed=0
- Inference counts: determined=23, underdetermined=0, difficult-but-well-posed=1

### Attempts Historical Archive

- Scope: Superseded retries or attempts inherited from archived queue rows.
- Count: 27
- Context counts: well-posed=5, partially-ill-posed=0, ill-posed=22
- Inference counts: determined=5, underdetermined=22, difficult-but-well-posed=0
- Common blocking defects: `route_synopsis` contains truncation markers, so the theorem state is not self-contained. (18) | `missing_route_lemma` contains truncation markers, so the theorem state is not self-contained. (15) | `claim_text` contains truncation markers, so the theorem state is not self-contained. (11) | `conjecture_statement` contains truncation markers, so the theorem state is not self-contained. (11) | `conditional_proposition` contains truncation markers, so the theorem state is not self-contained. (7)

## Mandatory Gates

- grounded_main_conjecture: True
- terminal_proved_attempt: False
- completion_checklist_clear: False
- no_failed_terminal_judges: False

## Signals

- Main grounded: True
- Evidence count: 0
- Proved results: 0
- Disproved results: 0
- Blocked results: 44
- Produced papers: 0
- External references: 8
- Prior-art findings: 0
- Candidate object: MCSP witness family
- Carrier kind: family of instances equipped with a monotone witness measure
- Route consistency note: The bridge portfolio names the carrier as `MCSP witness family`, while the selected proof sketch currently operationalizes the route through `Gap-MCSP promise problem`. This is an unresolved representation shift inside the current macro-proof state, not a proved equivalence.

## Score Caps

- Cap: 0.350 | Reason: No external evidence and no proved local result exist, so the score must remain in low-plausibility territory regardless of programme structure.

## Critic Panel

| Critic | Score | Rationale |
|---|---:|---|
| Main-Claim Closure Critic | 2 | The route target and final grounding implication are explicit, but no terminal route result yet closes the main problem. |
| Dependency-Closure Critic | 2 | The route has explicit obligations and candidate lemmas, but they are not yet discharged. |
| Assumption-Discipline Critic | 2 | The route declares mathematical assumptions, but no terminal proof audit has yet stabilized them. |
| Bridge-Realism Critic | 3 | The bridge object is typed, but multiple operationalizations remain live. |
| Adversarial-Pressure Critic | 2 | At least one negative or blocking result exists, so the route has seen nontrivial stress. |
| Proof-Granularity Critic | 2 | The proof architecture is inspectable through obligations, lemmas, and outline, but it is not yet a proved argument. |
| End-to-End Consistency Critic | 2 | The final implication chain is known, but the route still has an internal consistency defect. |
| Novelty-Discipline Critic | 3 | Terminal attempts exist and none are currently downgraded to prior art, though search trace discipline is not yet maximal. |
