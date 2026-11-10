# Proof Sketches

## Stats

- Proof sketches: 6
- Conjectures used: 36
- Strategies used: 6
- Bridges used: 20
- Hypotheses used: 42
- Strategy families: generator-recovery-from-unitary-orbits=1, spectral-calculus-realization=5

## Strategy Families

- `invariant-lift-through-intermediate-object`: Introduce a conjectured intermediate object or invariant, prove that the source regime induces it, then force the target consequence through that invariant.
- `spectral-calculus-realization`: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- `generator-recovery-from-unitary-orbits`: Recover the infinitesimal generator from strongly continuous orbit data, prove the required domain and closure properties, then identify the target operator.
- `domain-core-self-adjointness`: Build a dense core on which the hidden operator is well-defined, prove symmetry or closure there, and upgrade the core data to self-adjointness.
- `surrogate-reduction-transfer`: Define a surrogate object or promise problem, reduce the source statement into it, and transfer the required consequence through the surrogate interface.
- `barrier-escape-reencoding`: Re-encode the conjectured bridge concept in a representation that preserves the intended invariant while sidestepping the currently dominant barrier family.
- `contradiction-via-collapse-or-separation`: Assume the conjectured bridge fails or the target consequence does not hold, then derive a forbidden collapse or contradiction with a known separation profile.
- `bootstrapped-derandomization-transfer`: Use a derandomization or pseudorandomness-style object as the bridge, then bootstrap it into a lower-bound or separation consequence.
- `case-split-regime-transfer`: Partition the argument by regime, model, or threshold case, prove each branch against the same bridge concept, and reassemble the target consequence.

## Sketches

| sketch_id | conjecture_id | strategy_id | family | score | target |
|---|---|---|---|---|---|
| psk.001 | conj.007 | strat.001 | spectral-calculus-realization | 0.8969 | self-adjoint-operator-on-hilbert-space |
| psk.002 | conj.008 | strat.001 | spectral-calculus-realization | 0.8964 | self-adjoint-operator-on-hilbert-space |
| psk.003 | conj.014 | strat.001 | spectral-calculus-realization | 0.8961 | self-adjoint-operator-on-hilbert-space |
| psk.004 | conj.013 | strat.001 | spectral-calculus-realization | 0.8953 | self-adjoint-operator-on-hilbert-space |
| psk.005 | conj.026 | strat.001 | generator-recovery-from-unitary-orbits | 0.8936 | self-adjoint-operator-on-hilbert-space |
| psk.006 | conj.025 | strat.001 | spectral-calculus-realization | 0.8933 | self-adjoint-operator-on-hilbert-space |

### psk.001 - barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus via strat.001
- Conjecture: conj.007
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.007
- Family: spectral-calculus-realization
- Score: 0.8969
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: spectral-theorem-and-functional-calculus
- Invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface
- Family rationale: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- Definitional commitments: realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, evades barrier scope `barrier + spectral-calculus-interface`
- Counterfactual test: Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `spectral-theorem-and-functional-calculus`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.007.lemma.01: Definition lemma: the object `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` is well-defined and mathematically non-superficial.
  - bridge.007.lemma.02: Invariant lemma: `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source statement family.
  - bridge.007.lemma.03: Payoff lemma: realizing `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.007.lemma.04: Spectral lemma: the self-adjoint or spectral data attached to `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` yields a strongly continuous unitary representation.
- Proof outline:
  - step.01: Define `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` with the necessary attributes extracted in `conj.007`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.007` induces `spectral functional-calculus realization in self-adjoint-spectral-calculus` inside `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator. -> A spectral representation lemma yielding a strongly continuous unitary family.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.

### psk.002 - spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme via strat.001
- Conjecture: conj.008
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.007
- Family: spectral-calculus-realization
- Score: 0.8964
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: spectral-theorem-and-functional-calculus
- Invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface
- Family rationale: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- Definitional commitments: realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, evades barrier scope `barrier + spectral-calculus-interface`
- Counterfactual test: Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `spectral-theorem-and-functional-calculus`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.007.lemma.01: Definition lemma: the object `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme` is well-defined and mathematically non-superficial.
  - bridge.007.lemma.02: Invariant lemma: `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme` preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source statement family.
  - bridge.007.lemma.03: Payoff lemma: realizing `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.007.lemma.04: Spectral lemma: the self-adjoint or spectral data attached to `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme` yields a strongly continuous unitary representation.
- Proof outline:
  - step.01: Define `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme` with the necessary attributes extracted in `conj.008`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.007` induces `spectral functional-calculus realization in self-adjoint-spectral-calculus` inside `spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator. -> A spectral representation lemma yielding a strongly continuous unitary family.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.

### psk.003 - barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus via strat.001
- Conjecture: conj.014
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.001
- Family: spectral-calculus-realization
- Score: 0.8961
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: self-adjoint-operator-on-hilbert-space
- Invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Family rationale: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- Definitional commitments: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`
- Counterfactual test: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface + unbounded-operator-domain-control` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.001.lemma.01: Definition lemma: the object `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus` is well-defined and mathematically non-superficial.
  - bridge.001.lemma.02: Invariant lemma: `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus` preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source statement family.
  - bridge.001.lemma.03: Payoff lemma: realizing `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.001.lemma.04: Spectral lemma: the self-adjoint or spectral data attached to `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus` yields a strongly continuous unitary representation.
- Proof outline:
  - step.01: Define `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus` with the necessary attributes extracted in `conj.014`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.001` induces `spectral functional-calculus realization in self-adjoint-spectral-calculus` inside `barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator. -> A spectral representation lemma yielding a strongly continuous unitary family.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface + unbounded-operator-domain-control` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface + unbounded-operator-domain-control` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.

### psk.004 - spectral-theorem-and-functional-calculus self-adjoint generator core via strat.001
- Conjecture: conj.013
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.001
- Family: spectral-calculus-realization
- Score: 0.8953
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: self-adjoint-operator-on-hilbert-space
- Invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Family rationale: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- Definitional commitments: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`
- Counterfactual test: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface + unbounded-operator-domain-control` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.001.lemma.01: Definition lemma: the object `spectral-theorem-and-functional-calculus self-adjoint generator core` is well-defined and mathematically non-superficial.
  - bridge.001.lemma.02: Invariant lemma: `spectral-theorem-and-functional-calculus self-adjoint generator core` preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source statement family.
  - bridge.001.lemma.03: Payoff lemma: realizing `spectral-theorem-and-functional-calculus self-adjoint generator core` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.001.lemma.04: Spectral lemma: the self-adjoint or spectral data attached to `spectral-theorem-and-functional-calculus self-adjoint generator core` yields a strongly continuous unitary representation.
- Proof outline:
  - step.01: Define `spectral-theorem-and-functional-calculus self-adjoint generator core` with the necessary attributes extracted in `conj.013`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.001` induces `spectral functional-calculus realization in self-adjoint-spectral-calculus` inside `spectral-theorem-and-functional-calculus self-adjoint generator core`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator. -> A spectral representation lemma yielding a strongly continuous unitary family.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface + unbounded-operator-domain-control` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface + unbounded-operator-domain-control` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.

### psk.005 - spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space via strat.001
- Conjecture: conj.026
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.002
- Family: generator-recovery-from-unitary-orbits
- Score: 0.8936
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: strongly-continuous-unitary-group
- Invariant: spectral functional-calculus realization in strongly-continuous-unitary-group
- Barrier scope: barrier + spectral-calculus-interface
- Family rationale: Recover the infinitesimal generator from strongly continuous orbit data, prove the required domain and closure properties, then identify the target operator.
- Definitional commitments: realizes antecedent schema `strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, evades barrier scope `barrier + spectral-calculus-interface`
- Counterfactual test: Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `strongly-continuous-unitary-group`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in strongly-continuous-unitary-group` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.002.lemma.01: Definition lemma: the object `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space` is well-defined and mathematically non-superficial.
  - bridge.002.lemma.02: Invariant lemma: `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space` preserves `spectral functional-calculus realization in strongly-continuous-unitary-group` from the source statement family.
  - bridge.002.lemma.03: Payoff lemma: realizing `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.002.lemma.04: Generator lemma: differentiable orbit data for `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space` determines the hidden infinitesimal generator uniquely.
- Proof outline:
  - step.01: Define `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space` with the necessary attributes extracted in `conj.026`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.002` induces `spectral functional-calculus realization in strongly-continuous-unitary-group` inside `spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Recover the infinitesimal generator from unitary-orbit data and verify uniqueness at the operator level. -> A generator-recovery lemma with explicit domain and closure commitments.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.

### psk.006 - barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus via strat.001
- Conjecture: conj.025
- Strategy: strat.001 (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: bridge.002
- Family: spectral-calculus-realization
- Score: 0.8933
- Target consequence: self-adjoint-operator-on-hilbert-space
- Antecedent: strongly-continuous-unitary-group
- Invariant: spectral functional-calculus realization in strongly-continuous-unitary-group
- Barrier scope: barrier + spectral-calculus-interface
- Family rationale: Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation.
- Definitional commitments: realizes antecedent schema `strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, evades barrier scope `barrier + spectral-calculus-interface`
- Counterfactual test: Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails
- Proof obligations:
  - obl.01: realizes antecedent schema `strongly-continuous-unitary-group`
  - obl.02: forces target consequence `self-adjoint-operator-on-hilbert-space`
  - obl.03: preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`
  - obl.04: evades barrier scope `barrier + spectral-calculus-interface`
  - obl.05: Show that the conjectured object preserves `spectral functional-calculus realization in strongly-continuous-unitary-group` from the source side.
  - obl.06: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized.
  - obl.07: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding.
  - obl.08: Keep the argument faithful to the `Current Bridge Agenda` regime while linking to the target bridge consequence.
- Candidate lemmas:
  - bridge.002.lemma.01: Definition lemma: the object `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus` is well-defined and mathematically non-superficial.
  - bridge.002.lemma.02: Invariant lemma: `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus` preserves `spectral functional-calculus realization in strongly-continuous-unitary-group` from the source statement family.
  - bridge.002.lemma.03: Payoff lemma: realizing `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus` implies `self-adjoint-operator-on-hilbert-space`.
  - bridge.002.lemma.04: Spectral lemma: the self-adjoint or spectral data attached to `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus` yields a strongly continuous unitary representation.
- Proof outline:
  - step.01: Define `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus` with the necessary attributes extracted in `conj.025`. -> A non-superficial bridge object with theorem-family-specific commitments.
  - step.02: Show that the source side of `bridge.002` induces `spectral functional-calculus realization in strongly-continuous-unitary-group` inside `barrier + spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus`. -> An invariant-preservation lemma for the conjectured object.
  - step.03: Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator. -> A spectral representation lemma yielding a strongly continuous unitary family.
  - step.04: Use the realized bridge object to force `self-adjoint-operator-on-hilbert-space`. -> A payoff theorem candidate or a sharply localized remaining obstruction.
  - step.05: Run the designated counterfactual probe to verify that the bridge is structurally necessary rather than rhetorically similar. -> A falsifiability check distinguishing a genuine bridge concept from a superficial one.
- Barrier checkpoints:
  - barrier.01: Check whether `barrier + spectral-calculus-interface` blocks the proposed bridge object or proof tactic. / Re-encode the bridge object or abort the route if the barrier remains active.
- Abort conditions:
  - Abort if counterfactual probe fails to change bridge behavior: Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails.
  - Abort if the sketch still falls inside the `barrier + spectral-calculus-interface` barrier after re-encoding attempts.
  - Abort if the conjectured object cannot be defined without collapsing back into a generic topic label.
  - Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.
- Success signal: A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe.
