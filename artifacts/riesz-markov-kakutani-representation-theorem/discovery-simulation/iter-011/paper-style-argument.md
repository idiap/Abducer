# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.thm.positive-functional-implies-measure)
- Bridge: `bridge.004`
- Conjecture: `conj.004`
- Strategy family: `regularity-via-compact-open-approximation`
- Target consequence: `positive-linear-functional-on-cc-space`
- Antecedent schema: `regular-borel-measure-on-lch-space`
- Preserved invariant: `compact-open regularity control in compactly-supported-continuous-functions`

## Mathematical Context

Source anchor (`st.lem.uniqueness-from-cc-separation`):

> If \mu and \nu are regular Borel measures on X and \int_X f \, d\mu = \int_X f \, d\nu \quad \text{for all } f \in C_c(X), then \mu = \nu.

Target theorem (`st.thm.positive-functional-implies-measure`):

> Let \phi : C_c(X) \to \mathbb{R} be a positive linear functional. Then there exists a regular Borel measure \mu on X such that \phi(f) = \int_X f \, d\mu \quad \text{for all } f \in C_c(X).

The selected route interprets the target theorem family as a transport from `regular-borel-measure-on-lch-space` to `positive-linear-functional-on-cc-space` through the invariant `compact-open regularity control in compactly-supported-continuous-functions`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `regular-borel-measure-on-lch-space` to the target consequence `positive-linear-functional-on-cc-space` while preserving `compact-open regularity control in compactly-supported-continuous-functions`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `regular-borel-measure-on-lch-space`
2. preserves `compact-open regularity control in compactly-supported-continuous-functions`
3. forces target consequence `positive-linear-functional-on-cc-space`

## Proposition (Conditional positive-linear-functional-on-cc-space via regularity-via-compact-open-approximation)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `regular-borel-measure-on-lch-space`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `compact-open regularity control in compactly-supported-continuous-functions` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `compact-open regularity control in compactly-supported-continuous-functions` yields `positive-linear-functional-on-cc-space`.

Then `positive-linear-functional-on-cc-space` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional` preserves `compact-open regularity control in compactly-supported-continuous-functions` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `compact-open regularity control in compactly-supported-continuous-functions`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional` implies `positive-linear-functional-on-cc-space`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `positive-linear-functional-on-cc-space` here.

## Proof

Work in the `Cross-Model Strategy around st.thm.positive-functional-implies-measure` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `compact-open regularity control in compactly-supported-continuous-functions` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `positive-linear-functional-on-cc-space`.
Hence `positive-linear-functional-on-cc-space` follows from the antecedent schema `regular-borel-measure-on-lch-space` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `regular-borel-measure-on-lch-space` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `positive-linear-functional-on-cc-space` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `compact-open regularity control in compactly-supported-continuous-functions` (Definitional commitment for the bridge concept.)
- `obl.04`: evades barrier scope `barrier + compact-open-approximation + positivity-to-sigma-additivity` (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `compact-open regularity control in compactly-supported-continuous-functions` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `positive-linear-functional-on-cc-space` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + compact-open-approximation + positivity-to-sigma-additivity` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.004`
- strategy_id: `strat.001`
- bridge_id: `bridge.004`
- anchor_statement_id: `st.lem.uniqueness-from-cc-separation`
- target_statement_id: `st.thm.positive-functional-implies-measure`
