# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group)
- Bridge: `bridge.007`
- Conjecture: `conj.004`
- Strategy family: `spectral-calculus-realization`
- Target consequence: `self-adjoint-operator-on-hilbert-space`
- Antecedent schema: `spectral-theorem-and-functional-calculus`
- Preserved invariant: `spectral functional-calculus realization in self-adjoint-spectral-calculus`

## Mathematical Context

Source anchor (`st.thm.spectral-theorem-functional-calculus`):

> If A is self-adjoint on H, then there exists a projection-valued measure E_A such that A = \int_{\mathbb{R}} \lambda \, dE_A(\lambda). For every t \in \mathbb{R}, the operator U_t := e^{itA} = \int_{\mathbb{R}} e^{it\lambda} \, dE_A(\lambda) is unitary.

Target theorem (`st.thm.self-adjoint-implies-unitary-group`):

> If A is self-adjoint on H, then U_t := e^{itA} defines a strongly continuous one-parameter unitary group on H.

The selected route interprets the target theorem family as a transport from `spectral-theorem-and-functional-calculus` to `self-adjoint-operator-on-hilbert-space` through the invariant `spectral functional-calculus realization in self-adjoint-spectral-calculus`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `spectral-theorem-and-functional-calculus` to the target consequence `self-adjoint-operator-on-hilbert-space` while preserving `spectral functional-calculus realization in self-adjoint-spectral-calculus`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `spectral-theorem-and-functional-calculus`
2. preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`
3. forces target consequence `self-adjoint-operator-on-hilbert-space`

## Proposition (Conditional self-adjoint-operator-on-hilbert-space via spectral-calculus-realization)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `spectral-theorem-and-functional-calculus`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `spectral functional-calculus realization in self-adjoint-spectral-calculus` yields `self-adjoint-operator-on-hilbert-space`.

Then `self-adjoint-operator-on-hilbert-space` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `spectral functional-calculus realization in self-adjoint-spectral-calculus`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus` implies `self-adjoint-operator-on-hilbert-space`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `self-adjoint-operator-on-hilbert-space` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `self-adjoint-operator-on-hilbert-space`.
Hence `self-adjoint-operator-on-hilbert-space` follows from the antecedent schema `spectral-theorem-and-functional-calculus` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `spectral-theorem-and-functional-calculus` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `self-adjoint-operator-on-hilbert-space` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` (Definitional commitment for the bridge concept.)
- `obl.04`: evades barrier scope `barrier + spectral-calculus-interface` (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `self-adjoint-operator-on-hilbert-space` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + spectral-calculus-interface` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.004`
- strategy_id: `strat.001`
- bridge_id: `bridge.007`
- anchor_statement_id: `st.thm.spectral-theorem-functional-calculus`
- target_statement_id: `st.thm.self-adjoint-implies-unitary-group`
