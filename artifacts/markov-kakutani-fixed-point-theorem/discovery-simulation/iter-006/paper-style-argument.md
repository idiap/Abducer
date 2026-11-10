# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Invariant Fixed-Point Route around st.thm.markov-kakutani)
- Bridge: `bridge.007`
- Conjecture: `conj.001`
- Strategy family: `finite-intersection-compactness-lift`
- Target consequence: `common-fixed-point-for-finite-commuting-family`
- Antecedent schema: `commuting-affine-family-on-compact-convex-set`
- Preserved invariant: `finite-intersection lift in common-fixed-point-correspondence`

## Mathematical Context

Source anchor (`st.thm.markov-kakutani`):

> Let K be a nonempty compact convex subset of a locally convex topological vector space E. If F is a commuting family of continuous affine self-maps of K, then there exists x \in K such that T x = x \text{ for every } T \in F.

Target theorem (`st.ex.interval-commuting-projections`):

> Let K = [0,1] and let F be a commuting family of continuous affine contractions of K. Then the Markov-Kakutani theorem yields a common fixed point in [0,1].

The selected route interprets the target theorem family as a transport from `commuting-affine-family-on-compact-convex-set` to `common-fixed-point-for-finite-commuting-family` through the invariant `finite-intersection lift in common-fixed-point-correspondence`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `commuting-affine-family-on-compact-convex-set` to the target consequence `common-fixed-point-for-finite-commuting-family` while preserving `finite-intersection lift in common-fixed-point-correspondence`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `commuting-affine-family-on-compact-convex-set`
2. preserves `finite-intersection lift in common-fixed-point-correspondence`
3. provides an explicit transfer law or reduction mechanism
4. forces target consequence `common-fixed-point-for-finite-commuting-family`

## Proposition (Conditional common-fixed-point-for-finite-commuting-family via finite-intersection-compactness-lift)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `commuting-affine-family-on-compact-convex-set`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `finite-intersection lift in common-fixed-point-correspondence` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `finite-intersection lift in common-fixed-point-correspondence` yields `common-fixed-point-for-finite-commuting-family`.

Then `common-fixed-point-for-finite-commuting-family` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence` preserves `finite-intersection lift in common-fixed-point-correspondence` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `finite-intersection lift in common-fixed-point-correspondence`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence` implies `common-fixed-point-for-finite-commuting-family`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `common-fixed-point-for-finite-commuting-family` here.

## Proof

Work in the `Invariant Fixed-Point Route around st.thm.markov-kakutani` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `finite-intersection lift in common-fixed-point-correspondence` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `common-fixed-point-for-finite-commuting-family`.
Hence `common-fixed-point-for-finite-commuting-family` follows from the antecedent schema `commuting-affine-family-on-compact-convex-set` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `commuting-affine-family-on-compact-convex-set` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `common-fixed-point-for-finite-commuting-family` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `finite-intersection lift in common-fixed-point-correspondence` (Definitional commitment for the bridge concept.)
- `obl.04`: provides an explicit transfer law or reduction mechanism (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `finite-intersection lift in common-fixed-point-correspondence` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `common-fixed-point-for-finite-commuting-family` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `barrier + finite-intersection-compactness + invariant-subset-propagation` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.001`
- strategy_id: `strat.001`
- bridge_id: `bridge.007`
- anchor_statement_id: `st.thm.markov-kakutani`
- target_statement_id: `st.ex.interval-commuting-projections`
