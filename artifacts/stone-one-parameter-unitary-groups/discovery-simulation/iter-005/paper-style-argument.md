# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.stone-correspondence)
- Bridge: `bridge.004`
- Conjecture: `conj.001`
- Strategy family: `spectral-calculus-realization`
- Target consequence: `self-adjoint-operator-on-hilbert-space`
- Antecedent schema: `spectral-theorem-and-functional-calculus`
- Preserved invariant: `self-adjoint generator recovery in unbounded-generator-graph`

## Mathematical Context

Source anchor (`st.thm.unitary-group-implies-self-adjoint-generator`):

> Let (U_t)_{t \in \mathbb{R}} be a strongly continuous one-parameter unitary group on H. Then the operator A x = \frac{1}{i}\lim_{t \to 0}\frac{U_t x - x}{t} is self-adjoint and satisfies U_t = e^{itA} for all t \in \mathbb{R}.

Target theorem (`st.thm.stone-correspondence`):

> A family (U_t)_{t \in \mathbb{R}} is a strongly continuous one-parameter unitary group on H if and only if there exists a unique self-adjoint operator A on H such that U_t = e^{itA} \quad \text{for all } t \in \mathbb{R}.

The selected route interprets the target theorem family as a transport from `spectral-theorem-and-functional-calculus` to `self-adjoint-operator-on-hilbert-space` through the invariant `self-adjoint generator recovery in unbounded-generator-graph`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `spectral-theorem-and-functional-calculus` to the target consequence `self-adjoint-operator-on-hilbert-space` while preserving `self-adjoint generator recovery in unbounded-generator-graph`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `spectral-theorem-and-functional-calculus`
2. preserves `self-adjoint generator recovery in unbounded-generator-graph`
3. forces target consequence `self-adjoint-operator-on-hilbert-space`

## Proposition (Conditional self-adjoint-operator-on-hilbert-space via spectral-calculus-realization)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `spectral-theorem-and-functional-calculus`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `self-adjoint generator recovery in unbounded-generator-graph` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `self-adjoint generator recovery in unbounded-generator-graph` yields `self-adjoint-operator-on-hilbert-space`.

Then `self-adjoint-operator-on-hilbert-space` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` preserves `self-adjoint generator recovery in unbounded-generator-graph` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `self-adjoint generator recovery in unbounded-generator-graph`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` implies `self-adjoint-operator-on-hilbert-space`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `self-adjoint-operator-on-hilbert-space` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.stone-correspondence` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `self-adjoint generator recovery in unbounded-generator-graph` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `self-adjoint-operator-on-hilbert-space`.
Hence `self-adjoint-operator-on-hilbert-space` follows from the antecedent schema `spectral-theorem-and-functional-calculus` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `spectral-theorem-and-functional-calculus` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `self-adjoint-operator-on-hilbert-space` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `self-adjoint generator recovery in unbounded-generator-graph` (Definitional commitment for the bridge concept.)
- `obl.04`: evades barrier scope `barrier + orbit-differentiability-control + spectral-calculus-interface` (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `self-adjoint generator recovery in unbounded-generator-graph` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + orbit-differentiability-control + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.001`
- strategy_id: `strat.001`
- bridge_id: `bridge.004`
- anchor_statement_id: `st.thm.unitary-group-implies-self-adjoint-generator`
- target_statement_id: `st.thm.stone-correspondence`
