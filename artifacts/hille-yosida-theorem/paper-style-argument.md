# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.hille-yosida-general)
- Bridge: `bridge.009`
- Conjecture: `conj.001`
- Strategy family: `barrier-escape-reencoding`
- Target consequence: `equivalence`
- Antecedent schema: `equivalence-schema`
- Preserved invariant: `consequence schema equivalence`

## Mathematical Context

Source anchor (`st.thm.hille-yosida-general`):

> Let A be a linear operator on Banach space X, with constants M>=1 and omega in R. Then A generates a C_0-semigroup (T(t))_{t>=0} with ||T(t)|| <= M e^{omega t} iff: (i) A is closed and D(A) is dense; (ii) (omega, +infty) subset rho(A) and for all lambda>omega and all n in N: ||(lambda I - A)^{-n}|| <= M / (lambda-omega)^n.

Target theorem (`st.thm.hille-yosida-contraction`):

> (Contraction case) A generates a contraction C_0-semigroup (||T(t)|| <= 1 for t>=0) iff: (i) A is closed and D(A) is dense; (ii) (0,+infty) subset rho(A) and ||(lambda I-A)^{-1}|| <= 1/lambda for all lambda>0.

The selected route interprets the target theorem family as a transport from `equivalence-schema` to `equivalence` through the invariant `consequence schema equivalence`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `equivalence-schema` to the target consequence `equivalence` while preserving `consequence schema equivalence`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `equivalence-schema`
2. preserves `consequence schema equivalence`
3. provides an explicit transfer law or reduction mechanism
4. forces target consequence `equivalence`

## Proposition (Conditional equivalence via barrier-escape-reencoding)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `equivalence-schema`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `consequence schema equivalence` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `consequence schema equivalence` yields `equivalence`.

Then `equivalence` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification` preserves `consequence schema equivalence` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `consequence schema equivalence`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification` implies `equivalence`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `equivalence` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.hille-yosida-general` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `consequence schema equivalence` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `equivalence`.
Hence `equivalence` follows from the antecedent schema `equivalence-schema` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `equivalence-schema` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `equivalence` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `consequence schema equivalence` (Definitional commitment for the bridge concept.)
- `obl.04`: provides an explicit transfer law or reduction mechanism (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `consequence schema equivalence` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `equivalence` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + powers-of-resolvent-verification` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `equivalence-schema`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.001`
- strategy_id: `strat.001`
- bridge_id: `bridge.009`
- anchor_statement_id: `st.thm.hille-yosida-general`
- target_statement_id: `st.thm.hille-yosida-contraction`
