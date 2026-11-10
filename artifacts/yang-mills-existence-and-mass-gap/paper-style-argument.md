# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.def.os-euclidean-qft)
- Bridge: `bridge.001`
- Conjecture: `conj.003`
- Strategy family: `barrier-escape-reencoding`
- Target consequence: `positive-self-adjoint-Hamiltonian`
- Antecedent schema: `reflection-positivity-and-transfer-matrix`
- Preserved invariant: `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`

## Mathematical Context

Source anchor (`st.def.os-euclidean-qft`):

> An Osterwalder--Schrader Euclidean QFT is specified by Euclidean Schwinger functions satisfying Euclidean invariance, symmetry, reflection positivity, regularity, and clustering/analyticity conditions.

Target theorem (`st.thm.os-reconstruction-and-equivalence-with-wightman-`):

> If $(S_n)$ satisfy the OS axioms, then there exists a corresponding Wightman QFT on Minkowski space whose Wightman distributions analytically continue to $(S_n)$. Conversely, (under standard hypotheses) Wightman theories yield OS Schwinger functions via analytic continuation \cite{OsterwalderSchrader1973,OsterwalderSchrader1975}.\\ \textit{Assumptions.} OS axioms (including reflection positivity) and temperedness/regularity; vacuum setting.\\ \textit{Limitations/barriers.} For gauge theories, one must formulate OS/Wightman data in terms of \emph{gauge-invariant observables} (or a carefully controlled gauge-fixed framework) while preserving reflection positivity; ensuring this in $4$D non-Abelian continuum limits is a core unsolved obstacle \cite{JaffeWitten2000,Seiler1982}.

The selected route interprets the target theorem family as a transport from `reflection-positivity-and-transfer-matrix` to `positive-self-adjoint-Hamiltonian` through the invariant `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`.

## Definition

Let $\mathcal{B}$ denote the conjectured bridge object called `continuum-limit evasive representation for reflection-positivity-and-transfer-matrix`. It is intended to encode exactly the amount of `MCSP`-type structure needed to carry the antecedent schema `reflection-positivity-and-transfer-matrix` to the target consequence `positive-self-adjoint-Hamiltonian` while preserving `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. realizes antecedent schema `reflection-positivity-and-transfer-matrix`
2. preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`
3. forces target consequence `positive-self-adjoint-Hamiltonian`

## Proposition (Conditional positive-self-adjoint-Hamiltonian via barrier-escape-reencoding)

Assume there exists a realization of $\mathcal{B}$ satisfying the following transport conditions:

1. `Antecedent realization.` Whenever the relevant near-threshold `MCSP` regime exhibits the schema `reflection-positivity-and-transfer-matrix`, the object $\mathcal{B}$ is instantiated.
2. `Invariant transport.` Every realization of $\mathcal{B}$ preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` from the source regime into the bridge object.
3. `Payoff law.` Every realization of $\mathcal{B}$ carrying `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` yields `positive-self-adjoint-Hamiltonian`.

Then `positive-self-adjoint-Hamiltonian` follows.

## Lemmas

### Lemma 1 (Antecedent realization lemma)

Definition lemma: the object `continuum-limit evasive representation for reflection-positivity-and-transfer-matrix` is well-defined and mathematically non-superficial.

This lemma isolates the exact point at which the antecedent magnification schema yields an explicit bridge object.

### Lemma 2 (Invariant transport lemma)

Invariant lemma: `continuum-limit evasive representation for reflection-positivity-and-transfer-matrix` preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` from the source statement family.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`.

### Lemma 3 (Payoff lemma)

Payoff lemma: realizing `continuum-limit evasive representation for reflection-positivity-and-transfer-matrix` implies `positive-self-adjoint-Hamiltonian`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `positive-self-adjoint-Hamiltonian` here.

## Proof

Work in the `Cross-Model Strategy around st.def.os-euclidean-qft` regime. By the antecedent assumption and Lemma 1, the selected near-threshold `MCSP` hardness hypothesis realizes the bridge object $\mathcal{B}$.
By Lemma 2, this realization transports the invariant `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` from the source side of the magnification route into $\mathcal{B}$.
Lemma 3 then converts the realized bridge object, together with the transported invariant, into the target consequence `positive-self-adjoint-Hamiltonian`.
Hence `positive-self-adjoint-Hamiltonian` follows from the antecedent schema `reflection-positivity-and-transfer-matrix` once the bridge object $\mathcal{B}$ is available with the stated transport properties. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: realizes antecedent schema `reflection-positivity-and-transfer-matrix` (Definitional commitment for the bridge concept.)
- `obl.02`: forces target consequence `positive-self-adjoint-Hamiltonian` (Definitional commitment for the bridge concept.)
- `obl.03`: preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` (Definitional commitment for the bridge concept.)
- `obl.04`: evades barrier scope `continuum-limit` (Definitional commitment for the bridge concept.)
- `obl.05`: Show that the conjectured object preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap` from the source side. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that the conjectured object forces `positive-self-adjoint-Hamiltonian` once the preserved invariant is realized. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Demonstrate that the sketch avoids the `continuum-limit` barrier or explain why the barrier does not apply in this encoding. (A bridge that triggers a known barrier without explanation is not a credible proof route.)

## Counterfactual Check

If one performs the intervention `Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.003`
- strategy_id: `strat.001`
- bridge_id: `bridge.001`
- anchor_statement_id: `st.def.os-euclidean-qft`
- target_statement_id: `st.thm.os-reconstruction-and-equivalence-with-wightman-`
