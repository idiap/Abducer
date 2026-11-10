# Concept-Gap Abstraction Conjectures

This report identifies where current bridge programs are mathematically under-specified and which abstraction types could close those gaps.

## Stats

- Inference mode: conjecture
- Bridges inspected: 12
- Gap clusters: 12
- Abstraction conjectures: 36
- Selection policy: bridge leverage + concept-gap severity + abstraction-family fit + definitional/counterfactual sharpness

## Gap Diagnostics

| bridge | type | gap_score | dominant axes | shared terms |
|---|---|---|---|---|
| bridge.004 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, generator, self-adjoint-operator |
| bridge.009 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, functional-calculus, self-adjoint-operator |
| bridge.007 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | functional-calculus, self-adjoint-operator, spectral-measure |
| bridge.011 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, self-adjoint-operator, spectral-measure |
| bridge.013 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, functional-calculus, self-adjoint-operator |
| bridge.005 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, generator, unitary-group |
| bridge.006 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | Stone-correspondence, generator, unitary-group |
| bridge.014 | structural support bridge | 0.7265 | barrier-pressure, implication-lift | functional-calculus, generator, self-adjoint-operator |
| bridge.001 | structural support bridge | 0.722 | barrier-pressure | Stone-correspondence, self-adjoint-operator, spectral-measure |
| bridge.003 | structural support bridge | 0.722 | barrier-pressure | Stone-correspondence, generator, self-adjoint-operator |
| bridge.008 | structural support bridge | 0.722 | barrier-pressure | Stone-correspondence, generator, self-adjoint-operator |
| bridge.016 | structural support bridge | 0.722 | barrier-pressure | generator, self-adjoint-operator, unitary-group |

### bridge.004 - structural support bridge
- Bridge: `st.thm.unitary-group-implies-self-adjoint-generator` -> `st.thm.stone-correspondence`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group, self-adjoint-generator-characterization, spectral-calculus-unitary-realization
- Missing from source: functional-calculus, spectral-theorem, stone-unitary-group-correspondence, stone-self-adjoint-correspondence, spectral-calculus-interface
- Missing from target: barrier, orbit-differentiability-control, unbounded-operator-domain-control
- Candidate abstraction families: barrier-escaping-representation, self-adjoint-generator-core, functional-calculus-normal-form

### bridge.009 - structural support bridge
- Bridge: `st.thm.self-adjoint-implies-unitary-group` -> `st.thm.stone-correspondence`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group, spectral-calculus-unitary-realization
- Missing from source: generator, self-adjoint-generator-characterization, unbounded-generator-graph, differentiable-unitary-orbit-at-zero, unique-self-adjoint-generator
- Missing from target: barrier
- Candidate abstraction families: barrier-escaping-representation, self-adjoint-generator-core, functional-calculus-normal-form

### bridge.007 - structural support bridge
- Bridge: `st.thm.spectral-theorem-functional-calculus` -> `st.thm.self-adjoint-implies-unitary-group`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group, spectral-calculus-unitary-realization, self-adjoint-operator-definition
- Missing from source: Stone-correspondence, stone-unitary-group-correspondence, unitary-group-definition, strongly-continuous-unitary-group, stone-self-adjoint-correspondence
- Missing from target: generator, yosida-approximation-convergence, Yosida-approximation-scheme, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme
- Candidate abstraction families: barrier-escaping-representation, functional-calculus-normal-form, self-adjoint-generator-core

### bridge.011 - structural support bridge
- Bridge: `st.thm.self-adjoint-implies-unitary-group` -> `st.thm.unitary-group-implies-self-adjoint-generator`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group, spectral-calculus-unitary-realization, self-adjoint-operator-definition, unitary-group-definition
- Missing from source: generator, self-adjoint-generator-characterization, unbounded-generator-graph, differentiable-unitary-orbit-at-zero, unique-self-adjoint-generator, orbit-differentiability-control, unbounded-operator-domain-control
- Missing from target: functional-calculus, spectral-theorem, stone-unitary-group-correspondence, stone-self-adjoint-correspondence, spectral-calculus-interface
- Candidate abstraction families: barrier-escaping-representation, self-adjoint-generator-core, functional-calculus-normal-form

### bridge.013 - structural support bridge
- Bridge: `st.thm.self-adjoint-implies-unitary-group` -> `st.app.schrodinger-time-evolution`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group, spectral-calculus-unitary-realization
- Missing from source: Hamiltonian, generator, quantum-time-evolution, Hamiltonian-time-evolution-model, unbounded-operator-domain-control
- Missing from target: unitary-group-definition, barrier
- Candidate abstraction families: barrier-escaping-representation, functional-calculus-normal-form, self-adjoint-generator-core

### bridge.005 - structural support bridge
- Bridge: `st.def.unitary-group` -> `st.thm.unitary-group-implies-self-adjoint-generator`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `strongly-continuous-unitary-group` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: self-adjoint-operator, spectral-measure, unbounded-operator, self-adjoint-generator-characterization, spectral-calculus-unitary-realization, self-adjoint-operator-definition, self-adjoint-spectral-calculus, spectral-functional-calculus
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Candidate abstraction families: self-adjoint-generator-core, barrier-escaping-representation, functional-calculus-normal-form

### bridge.006 - structural support bridge
- Bridge: `st.def.unitary-group` -> `st.thm.stone-correspondence`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `strongly-continuous-unitary-group` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, self-adjoint-generator-characterization, spectral-calculus-unitary-realization, stone-unitary-group-correspondence
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Candidate abstraction families: self-adjoint-generator-core, barrier-escaping-representation, functional-calculus-normal-form

### bridge.014 - structural support bridge
- Bridge: `st.thm.spectral-theorem-functional-calculus` -> `st.thm.stone-correspondence`
- Gap score: 0.7265
- Gap axes:
  - barrier-pressure (0.84): The conjectured move is exposed to barrier scope `barrier + spectral-calculus-interface` and needs a barrier-evading abstraction.
  - implication-lift (0.58): The bridge must lift antecedent `spectral-theorem-and-functional-calculus` into target consequence `self-adjoint-operator-on-hilbert-space`.
- Shared typed terms: functional-calculus, generator, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group, spectral-calculus-unitary-realization
- Missing from source: Stone-correspondence, self-adjoint-generator-characterization, stone-unitary-group-correspondence, unitary-group-definition, strongly-continuous-unitary-group, unbounded-generator-graph, differentiable-unitary-orbit-at-zero, stone-self-adjoint-correspondence
- Missing from target: yosida-approximation-convergence, Yosida-approximation-scheme, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, barrier
- Candidate abstraction families: barrier-escaping-representation, self-adjoint-generator-core, functional-calculus-normal-form

## Abstraction Conjectures

### conj.001 - barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus
- Bridge: bridge.004 (`st.thm.unitary-group-implies-self-adjoint-generator` -> `st.thm.stone-correspondence`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7477
- Gap target: barrier-pressure, implication-lift
- Role: A representation change designed to expose `self-adjoint generator recovery in unbounded-generator-graph` without re-entering barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in unbounded-generator-graph; barrier=barrier + orbit-differentiability-control + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: functional-calculus, spectral-theorem, stone-unitary-group-correspondence, stone-self-adjoint-correspondence, spectral-calculus-interface
- Missing from target: barrier, orbit-differentiability-control, unbounded-operator-domain-control
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.004` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in unbounded-generator-graph`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `self-adjoint generator recovery in unbounded-generator-graph` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in unbounded-generator-graph` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.002 - spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core
- Bridge: bridge.004 (`st.thm.unitary-group-implies-self-adjoint-generator` -> `st.thm.stone-correspondence`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7477
- Gap target: barrier-pressure, implication-lift
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in unbounded-generator-graph; barrier=barrier + orbit-differentiability-control + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: functional-calculus, spectral-theorem, stone-unitary-group-correspondence, stone-self-adjoint-correspondence, spectral-calculus-interface
- Missing from target: barrier, orbit-differentiability-control, unbounded-operator-domain-control
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.004` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in unbounded-generator-graph`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `self-adjoint generator recovery in unbounded-generator-graph` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in unbounded-generator-graph` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.007 - barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus
- Bridge: bridge.007 (`st.thm.spectral-theorem-functional-calculus` -> `st.thm.self-adjoint-implies-unitary-group`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7332
- Gap target: barrier-pressure, implication-lift
- Role: A representation change designed to expose `spectral functional-calculus realization in self-adjoint-spectral-calculus` without re-entering barrier scope `barrier + spectral-calculus-interface`.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in self-adjoint-spectral-calculus; barrier=barrier + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group
- Missing from source: Stone-correspondence, stone-unitary-group-correspondence, unitary-group-definition, strongly-continuous-unitary-group, stone-self-adjoint-correspondence
- Missing from target: generator, yosida-approximation-convergence, Yosida-approximation-scheme, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.007` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `spectral functional-calculus realization in self-adjoint-spectral-calculus` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.013 - spectral-theorem-and-functional-calculus self-adjoint generator core
- Bridge: bridge.001 (`st.def.self-adjoint-operator` -> `st.thm.self-adjoint-implies-unitary-group`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7301
- Gap target: barrier-pressure
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=self-adjoint-operator-on-hilbert-space; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in self-adjoint-spectral-calculus; barrier=barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group, stone-unitary-group-correspondence
- Missing from source: functional-calculus, spectral-theorem, spectral-calculus-unitary-realization, unitary-group-definition, spectral-functional-calculus, spectral-theorem-and-functional-calculus
- Missing from target: generator, generator-symmetry, operator-theoretic-Banach-space, differentiable-unitary-orbit-at-zero, symmetric-generator, unbounded-operator-domain-control
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.001` is a mathematical object or abstraction that realizes `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `self-adjoint-operator-on-hilbert-space`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.003 - spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in self-adjoint-spectral-calculus
- Bridge: bridge.004 (`st.thm.unitary-group-implies-self-adjoint-generator` -> `st.thm.stone-correspondence`)
- Abstraction type: functional-calculus-normal-form
- Priority: 0.7297
- Gap target: barrier-pressure, implication-lift
- Role: A normal form for exponentiating self-adjoint operators so the bridge to `self-adjoint-operator-on-hilbert-space` becomes a typed functional-calculus obligation.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in unbounded-generator-graph; barrier=barrier + orbit-differentiability-control + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: functional-calculus, spectral-theorem, stone-unitary-group-correspondence, stone-self-adjoint-correspondence, spectral-calculus-interface
- Missing from target: barrier, orbit-differentiability-control, unbounded-operator-domain-control
- Definition: An adequate `functional-calculus-normal-form` bridge concept for `bridge.004` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in unbounded-generator-graph`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-express the bridge through a canonical functional-calculus normal form.
  - Verify that the normal form preserves `self-adjoint generator recovery in unbounded-generator-graph` while making the target consequence `self-adjoint-operator-on-hilbert-space` explicit.
  - Check whether continuity, domain, and group-law obligations become theorem-schema matches after the re-expression.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in unbounded-generator-graph` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.022 - spectral-theorem-and-functional-calculus self-adjoint generator core
- Bridge: bridge.005 (`st.def.unitary-group` -> `st.thm.unitary-group-implies-self-adjoint-generator`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7279
- Gap target: barrier-pressure, implication-lift
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=strongly-continuous-unitary-group; consequence=self-adjoint-operator-on-hilbert-space; invariant=unitary orbit infinitesimal control in strongly-continuous-unitary-group; barrier=barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: self-adjoint-operator, spectral-measure, unbounded-operator, self-adjoint-generator-characterization, spectral-calculus-unitary-realization, self-adjoint-operator-definition
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.005` is a mathematical object or abstraction that realizes `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `strongly-continuous-unitary-group`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `unitary orbit infinitesimal control in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.025 - spectral-theorem-and-functional-calculus self-adjoint generator core
- Bridge: bridge.006 (`st.def.unitary-group` -> `st.thm.stone-correspondence`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7276
- Gap target: barrier-pressure, implication-lift
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=strongly-continuous-unitary-group; consequence=self-adjoint-operator-on-hilbert-space; invariant=unitary orbit infinitesimal control in strongly-continuous-unitary-group; barrier=spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, self-adjoint-generator-characterization
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.006` is a mathematical object or abstraction that realizes `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `strongly-continuous-unitary-group`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `spectral-calculus-interface`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `unitary orbit infinitesimal control in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.019 - spectral-theorem-and-functional-calculus self-adjoint generator core
- Bridge: bridge.003 (`st.def.self-adjoint-operator` -> `st.thm.unitary-group-implies-self-adjoint-generator`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7271
- Gap target: barrier-pressure
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=self-adjoint-operator-on-hilbert-space; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in self-adjoint-spectral-calculus; barrier=barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: self-adjoint-generator-characterization, spectral-calculus-unitary-realization, unitary-group-definition, spectral-functional-calculus, unbounded-generator-graph, spectral-theorem-and-functional-calculus
- Missing from target: stone-unitary-group-correspondence, generator-symmetry, operator-theoretic-Banach-space, stone-self-adjoint-correspondence, symmetric-generator
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.003` is a mathematical object or abstraction that realizes `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `self-adjoint-operator-on-hilbert-space`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.028 - spectral-theorem-and-functional-calculus self-adjoint generator core
- Bridge: bridge.008 (`st.def.self-adjoint-operator` -> `st.thm.stone-correspondence`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7251
- Gap target: barrier-pressure
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=self-adjoint-operator-on-hilbert-space; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in self-adjoint-spectral-calculus; barrier=spectral-calculus-interface + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: functional-calculus, spectral-theorem, self-adjoint-generator-characterization, spectral-calculus-unitary-realization, unitary-group-definition, spectral-functional-calculus
- Missing from target: generator-symmetry, operator-theoretic-Banach-space, symmetric-generator, unbounded-operator-domain-control
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.008` is a mathematical object or abstraction that realizes `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `spectral-calculus-interface + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `self-adjoint-operator-on-hilbert-space`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `spectral-calculus-interface + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `spectral-calculus-interface + unbounded-operator-domain-control`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `spectral-calculus-interface + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.014 - barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus
- Bridge: bridge.001 (`st.def.self-adjoint-operator` -> `st.thm.self-adjoint-implies-unitary-group`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7181
- Gap target: barrier-pressure
- Role: A representation change designed to expose `spectral functional-calculus realization in self-adjoint-spectral-calculus` without re-entering barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`.
- Commitments: antecedent=self-adjoint-operator-on-hilbert-space; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in self-adjoint-spectral-calculus; barrier=barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group, stone-unitary-group-correspondence
- Missing from source: functional-calculus, spectral-theorem, spectral-calculus-unitary-realization, unitary-group-definition, spectral-functional-calculus, spectral-theorem-and-functional-calculus
- Missing from target: generator, generator-symmetry, operator-theoretic-Banach-space, differentiable-unitary-orbit-at-zero, symmetric-generator, unbounded-operator-domain-control
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.001` is a mathematical object or abstraction that realizes `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `self-adjoint-operator-on-hilbert-space`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `spectral functional-calculus realization in self-adjoint-spectral-calculus` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.004 - barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus
- Bridge: bridge.009 (`st.thm.self-adjoint-implies-unitary-group` -> `st.thm.stone-correspondence`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7176
- Gap target: barrier-pressure, implication-lift
- Role: A representation change designed to expose `spectral functional-calculus realization in strongly-continuous-unitary-group` without re-entering barrier scope `barrier + spectral-calculus-interface`.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in strongly-continuous-unitary-group; barrier=barrier + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator
- Missing from source: generator, self-adjoint-generator-characterization, unbounded-generator-graph, differentiable-unitary-orbit-at-zero, unique-self-adjoint-generator
- Missing from target: barrier
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.009` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `spectral functional-calculus realization in strongly-continuous-unitary-group` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.005 - spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core
- Bridge: bridge.009 (`st.thm.self-adjoint-implies-unitary-group` -> `st.thm.stone-correspondence`)
- Abstraction type: self-adjoint-generator-core
- Priority: 0.7176
- Gap target: barrier-pressure, implication-lift
- Role: A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `self-adjoint-operator-on-hilbert-space`.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in strongly-continuous-unitary-group; barrier=barrier + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator
- Missing from source: generator, self-adjoint-generator-characterization, unbounded-generator-graph, differentiable-unitary-orbit-at-zero, unique-self-adjoint-generator
- Missing from target: barrier
- Definition: An adequate `self-adjoint-generator-core` bridge concept for `bridge.009` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.
  - Show that the core preserves `spectral functional-calculus realization in strongly-continuous-unitary-group` and is strong enough to force self-adjointness or an equivalent closure property.
  - Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.023 - barrier + orbit-differentiability-control + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus
- Bridge: bridge.005 (`st.def.unitary-group` -> `st.thm.unitary-group-implies-self-adjoint-generator`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7159
- Gap target: barrier-pressure, implication-lift
- Role: A representation change designed to expose `unitary orbit infinitesimal control in strongly-continuous-unitary-group` without re-entering barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Commitments: antecedent=strongly-continuous-unitary-group; consequence=self-adjoint-operator-on-hilbert-space; invariant=unitary orbit infinitesimal control in strongly-continuous-unitary-group; barrier=barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: self-adjoint-operator, spectral-measure, unbounded-operator, self-adjoint-generator-characterization, spectral-calculus-unitary-realization, self-adjoint-operator-definition
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.005` is a mathematical object or abstraction that realizes `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `strongly-continuous-unitary-group`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `unitary orbit infinitesimal control in strongly-continuous-unitary-group` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `unitary orbit infinitesimal control in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.026 - spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus
- Bridge: bridge.006 (`st.def.unitary-group` -> `st.thm.stone-correspondence`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7156
- Gap target: barrier-pressure, implication-lift
- Role: A representation change designed to expose `unitary orbit infinitesimal control in strongly-continuous-unitary-group` without re-entering barrier scope `spectral-calculus-interface`.
- Commitments: antecedent=strongly-continuous-unitary-group; consequence=self-adjoint-operator-on-hilbert-space; invariant=unitary orbit infinitesimal control in strongly-continuous-unitary-group; barrier=spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, unitary-group, unitary-group-definition, strongly-continuous-unitary-group
- Missing from source: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, self-adjoint-generator-characterization
- Missing from target: Hilbert-space, operator-theoretic-Hilbert-space
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.006` is a mathematical object or abstraction that realizes `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `strongly-continuous-unitary-group`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `spectral-calculus-interface`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `unitary orbit infinitesimal control in strongly-continuous-unitary-group` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `unitary orbit infinitesimal control in strongly-continuous-unitary-group` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.008 - spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme
- Bridge: bridge.007 (`st.thm.spectral-theorem-functional-calculus` -> `st.thm.self-adjoint-implies-unitary-group`)
- Abstraction type: functional-calculus-normal-form
- Priority: 0.7152
- Gap target: barrier-pressure, implication-lift
- Role: A normal form for exponentiating self-adjoint operators so the bridge to `self-adjoint-operator-on-hilbert-space` becomes a typed functional-calculus obligation.
- Commitments: antecedent=spectral-theorem-and-functional-calculus; consequence=self-adjoint-operator-on-hilbert-space; invariant=spectral functional-calculus realization in self-adjoint-spectral-calculus; barrier=barrier + spectral-calculus-interface
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group
- Missing from source: Stone-correspondence, stone-unitary-group-correspondence, unitary-group-definition, strongly-continuous-unitary-group, stone-self-adjoint-correspondence
- Missing from target: generator, yosida-approximation-convergence, Yosida-approximation-scheme, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme
- Definition: An adequate `functional-calculus-normal-form` bridge concept for `bridge.007` is a mathematical object or abstraction that realizes `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + spectral-calculus-interface`.
- Necessary attributes:
  - realizes antecedent schema `spectral-theorem-and-functional-calculus`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + spectral-calculus-interface`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + spectral-calculus-interface`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + spectral-calculus-interface`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-express the bridge through a canonical functional-calculus normal form.
  - Verify that the normal form preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` while making the target consequence `self-adjoint-operator-on-hilbert-space` explicit.
  - Check whether continuity, domain, and group-law obligations become theorem-schema matches after the re-expression.
- Validation questions:
  - Does the proposed abstraction make `spectral functional-calculus realization in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

### conj.020 - barrier + orbit-differentiability-control + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus
- Bridge: bridge.003 (`st.def.self-adjoint-operator` -> `st.thm.unitary-group-implies-self-adjoint-generator`)
- Abstraction type: barrier-escaping-representation
- Priority: 0.7151
- Gap target: barrier-pressure
- Role: A representation change designed to expose `self-adjoint generator recovery in self-adjoint-spectral-calculus` without re-entering barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Commitments: antecedent=self-adjoint-operator-on-hilbert-space; consequence=self-adjoint-operator-on-hilbert-space; invariant=self-adjoint generator recovery in self-adjoint-spectral-calculus; barrier=barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Definitional completeness: 1.0; counterfactual sharpness: 1.0
- Shared terms: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Missing from source: self-adjoint-generator-characterization, spectral-calculus-unitary-realization, unitary-group-definition, spectral-functional-calculus, unbounded-generator-graph, spectral-theorem-and-functional-calculus
- Missing from target: stone-unitary-group-correspondence, generator-symmetry, operator-theoretic-Banach-space, stone-self-adjoint-correspondence, symmetric-generator
- Definition: An adequate `barrier-escaping-representation` bridge concept for `bridge.003` is a mathematical object or abstraction that realizes `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, and is strong enough to force `self-adjoint-operator-on-hilbert-space` while evading barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`.
- Necessary attributes:
  - realizes antecedent schema `self-adjoint-operator-on-hilbert-space`: The abstraction must instantiate the support-side theorem schema rather than merely mention it.
  - forces target consequence `self-adjoint-operator-on-hilbert-space`: A bridging concept is not sufficient unless it materially contributes to the target theorem-family consequence.
  - preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`: The bridge must keep the core mathematical quantity or structure stable across the source-target move.
  - evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`: The abstraction must avoid collapsing back into the known blocked proof regime.
  - remains operationalizable on current bridge/pathway anchors: The abstraction should be testable on the current KB, not only in an abstract future theory.
- Sufficient attribute sets:
  - transport set: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
  - witness set: preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
  - barrier-evasion set: evades barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, remains operationalizable on current bridge/pathway anchors
- Counterfactual probes:
  - Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction. => bridge-degrades-or-fails (Tests whether the leading definitional attribute is genuinely necessary rather than a descriptive embellishment.)
  - Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space` => bridge-becomes-testable (Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.)
  - Replace the abstraction with one that stays inside barrier scope `barrier + orbit-differentiability-control + unbounded-operator-domain-control`. => bridge-blocked-by-known-barrier (Checks that the bridge concept is not merely restating a blocked proof style under a new name.)
- Construction template:
  - Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.
  - Check that `self-adjoint generator recovery in self-adjoint-spectral-calculus` remains observable after the representation change.
  - Run coherence and bridge validation on the re-encoded statements before promoting the move.
- Validation questions:
  - Does the proposed abstraction make `self-adjoint generator recovery in self-adjoint-spectral-calculus` more discriminating than the current bridge commitment?
  - If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `self-adjoint-operator-on-hilbert-space`?
  - Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?

## Recommended Run Order

1. `conj.001`
2. `conj.002`
3. `conj.007`
4. `conj.013`
5. `conj.003`
6. `conj.022`
7. `conj.025`
8. `conj.019`
9. `conj.028`
10. `conj.014`
11. `conj.004`
12. `conj.005`
