# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.riesz-markov-kakutani)
- Bridge: `bridge.005`
- Conjecture: `conj.006`
- Strategy family: `measure-construction-from-positive-functional`
- Target consequence: `regular-borel-measure-representation`
- Antecedent schema: `positive-linear-functional-on-cc-space`
- Preserved invariant: `regular-Borel representation in compactly-supported-continuous-functions`

## Mathematical Context

Source anchor (`st.def.positive-linear-functional`):

> A linear functional \phi : C_c(X) \to \mathbb{R} is positive if \phi(f) \ge 0 whenever f \ge 0.

Target theorem (`st.thm.riesz-markov-kakutani`):

> Let X be a locally compact Hausdorff space. A positive linear functional \phi on C_c(X) is of the form \phi(f) = \int_X f \, d\mu \quad \text{for all } f \in C_c(X) for a unique regular Borel measure \mu on X.

The selected route interprets the target theorem family as a transport from `positive-linear-functional-on-cc-space` to `regular-borel-measure-representation` through the invariant `regular-Borel representation in compactly-supported-continuous-functions`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for positive-functional-implies-regular-measure`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `positive-linear-functional-on-cc-space` to the target consequence `regular-borel-measure-representation` while preserving `regular-Borel representation in compactly-supported-continuous-functions`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `positive-linear-functional-on-cc-space`
2. preserves `regular-Borel representation in compactly-supported-continuous-functions`
3. provides an explicit transfer law or reduction mechanism
4. forces target consequence `regular-borel-measure-representation`

## Proposition (Conditional regular-borel-measure-representation via measure-construction-from-positive-functional)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `positive-linear-functional-on-cc-space`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `regular-Borel representation in compactly-supported-continuous-functions` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `regular-Borel representation in compactly-supported-continuous-functions` yields `regular-borel-measure-representation`.

Then `regular-borel-measure-representation` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for positive-functional-implies-regular-measure` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for positive-functional-implies-regular-measure` preserves `regular-Borel representation in compactly-supported-continuous-functions` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `regular-Borel representation in compactly-supported-continuous-functions`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for positive-functional-implies-regular-measure` implies `regular-borel-measure-representation`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `regular-borel-measure-representation` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.riesz-markov-kakutani` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `regular-Borel representation in compactly-supported-continuous-functions` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `regular-borel-measure-representation`.
Hence `regular-borel-measure-representation` follows from the antecedent schema `positive-linear-functional-on-cc-space` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `positive-linear-functional-on-cc-space` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `regular-borel-measure-representation` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `regular-Borel representation in compactly-supported-continuous-functions` (Definitional commitment for the bridge concept.)
- `obl.04`: provides an explicit transfer law or reduction mechanism (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `regular-Borel representation in compactly-supported-continuous-functions` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `regular-borel-measure-representation` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.006`
- strategy_id: `strat.001`
- bridge_id: `bridge.005`
- anchor_statement_id: `st.def.positive-linear-functional`
- target_statement_id: `st.thm.riesz-markov-kakutani`
