# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.hille-yosida-general)
- Bridge: `bridge.003`
- Conjecture: `conj.007`
- Strategy family: `barrier-escape-reencoding`
- Target consequence: `generator-of-exponentially-bounded-c0-semigroup`
- Antecedent schema: `c0-semigroup-definition`
- Preserved invariant: `Yosida approximation convergence in operator-theoretic-Banach-space`

## Mathematical Context

Source anchor (`st.def.c0-semigroup`):

> Let X be a Banach space. A family (T(t))_{t >= 0} subset L(X) is a C_0-semigroup if T(0)=I, T(t+s)=T(t)T(s) for all s,t>=0, and for every x in X: ||T(t)x - x|| -> 0 as t downarrow 0.

Target theorem (`st.thm.hille-yosida-general`):

> Let A be a linear operator on Banach space X, with constants M>=1 and omega in R. Then A generates a C_0-semigroup (T(t))_{t>=0} with ||T(t)|| <= M e^{omega t} iff: (i) A is closed and D(A) is dense; (ii) (omega, +infty) subset rho(A) and for all lambda>omega and all n in N: ||(lambda I - A)^{-n}|| <= M / (lambda-omega)^n.

The selected route interprets the target theorem family as a transport from `c0-semigroup-definition` to `generator-of-exponentially-bounded-c0-semigroup` through the invariant `Yosida approximation convergence in operator-theoretic-Banach-space`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `c0-semigroup-definition` to the target consequence `generator-of-exponentially-bounded-c0-semigroup` while preserving `Yosida approximation convergence in operator-theoretic-Banach-space`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `c0-semigroup-definition`
2. preserves `Yosida approximation convergence in operator-theoretic-Banach-space`
3. forces target consequence `generator-of-exponentially-bounded-c0-semigroup`

## Proposition (Conditional generator-of-exponentially-bounded-c0-semigroup via barrier-escape-reencoding)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `c0-semigroup-definition`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `Yosida approximation convergence in operator-theoretic-Banach-space` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `Yosida approximation convergence in operator-theoretic-Banach-space` yields `generator-of-exponentially-bounded-c0-semigroup`.

Then `generator-of-exponentially-bounded-c0-semigroup` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds` preserves `Yosida approximation convergence in operator-theoretic-Banach-space` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `Yosida approximation convergence in operator-theoretic-Banach-space`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds` implies `generator-of-exponentially-bounded-c0-semigroup`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `generator-of-exponentially-bounded-c0-semigroup` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.hille-yosida-general` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `Yosida approximation convergence in operator-theoretic-Banach-space` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `generator-of-exponentially-bounded-c0-semigroup`.
Hence `generator-of-exponentially-bounded-c0-semigroup` follows from the antecedent schema `c0-semigroup-definition` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `c0-semigroup-definition` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `generator-of-exponentially-bounded-c0-semigroup` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `Yosida approximation convergence in operator-theoretic-Banach-space` (Definitional commitment for the bridge concept.)
- `obl.04`: evades barrier scope `barrier + domain-closure-density + powers-of-resolvent-verification` (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `Yosida approximation convergence in operator-theoretic-Banach-space` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `generator-of-exponentially-bounded-c0-semigroup` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + domain-closure-density + powers-of-resolvent-verification` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.007`
- strategy_id: `strat.001`
- bridge_id: `bridge.003`
- anchor_statement_id: `st.def.c0-semigroup`
- target_statement_id: `st.thm.hille-yosida-general`
