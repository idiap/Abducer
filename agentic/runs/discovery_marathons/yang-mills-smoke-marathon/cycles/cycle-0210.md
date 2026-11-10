# cycle-0210

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite locked Wilson block, same-theory OS passage after collar removal is equivalent to PSD of q=Nh/Bh. If collar quotients form a continuous Hadamard semigroup, this is certified for all collar scales exactly by a CND logarithmic generator.

## Definitions

- source object: fixed-collar reflected Wilson OS matrices N^{(r)} obtained as RG limits, plus boundary Gram factors B^{(r)} from the mixed hairpin OPE.
- target object: continuum OS matrix M^{(r)} on the same locked Wilson observables at the reflection plane, with no boundary-added algebra.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through finite Schur preimages after collar collapse.
- same-theory condition: N^{(r)}=B^{(r)}\circ M^{(r)} with B only a trace anomaly of the original Wilson observables; no new counterterm, quotient, or loop renormalization.

## Assumptions

- For the chosen finite Wilson family, diagonal entries of N^{(r)} and B^{(r)} are positive and all B^{(r)}_{ij} used in the quotient are nonzero.
- Additive reflected boundary contacts vanish or have already been absorbed by valid diagonal trace continuity; the remaining anomaly is multiplicative.
- The normalized quotients q_r are Hermitian, continuous in r, satisfy q_0=1, and, for the log test, q_{r+s}=q_r\circ q_s.
- RG convergence is valid for every reflected mixed Wilson matrix entry in the finite block, not merely for separated single loops.

## Equations

- Schur preimage obstruction: `M^{(r)}=N^{(r)}\oslash B^{(r)},\qquad M^{(r)}\ge0\Longleftrightarrow q_r:=\widehat N^{(r)}\oslash\widehat B^{(r)}\ge0`. Valid when: B has nonzero entries and positive diagonal; hats denote diagonal normalization, so the equivalence is by positive diagonal congruence.
- Hadamard semigroup generator: `q_{r+s}=q_r\circ q_s,\qquad q_r=\exp_{\circ}(-rK),\qquad \sum_{i,j}\bar z_i z_jK_{ij}\le0\ \ (\sum_i z_i=0)`. Valid when: q_r is a continuous nonvanishing Hermitian Hadamard semigroup; the last condition is the CND criterion for q_r\ge0 for all r.
- finite falsifier test: `\det q_I<0\quad\text{or}\quad \exists z,\ \sum z_i=0,\ \sum_{i,j}\bar z_i z_jK_{ij}>0\ \Longrightarrow\ \text{OS bridge fails}`. Valid when: The determinant test is valid for any realized finite block; the log-quadratic falsifier is valid only under the semigroup hypothesis.

## Attempted Derivation

- Fixed-collar reflection positivity and RG convergence give N^{(r)}\ge0 for every finite reflected Wilson block; this is the already valid closed-cone step.
- The boundary OPE ansatz writes the collar-limit matrix as N^{(r)}=B^{(r)}\circ M^{(r)}. After diagonal normalization, M^{(r)}\ge0 is equivalent to q_r=Nh/Bh\ge0.
- If q_r is a continuous Hadamard semigroup, then q_r=exp_circ(-rK). Differentiating z^*q_r z at r=0 on zero-sum vectors yields the CND sign for K.
- Schoenberg's theorem gives the converse: CND K makes every q_r PSD, hence the same-theory OS form is positive after undoing only a diagonal congruence.

Blocking gap: No Yang-Mills estimate yet proves that mixed reflected Wilson hairpin quotients are nonzero, multiplicative, and Hadamard-semigroup in collar thickness.

## Falsifiers

- falsifier: a locked three-hairpin Wilson family with det(\widehat N\oslash\widehat B)<0 despite N\ge0 from fixed-collar reflection positivity.
- falsifier: q_{r+s}\ne q_r\circ q_s because cusp or shared-footprint interactions depend on the order of collar collapse, making the log-CND certificate invalid.
- falsifier: a zero or discontinuous phase in B_{ij} while N_{ij}\ne0, so the same-theory Schur preimage is not defined in the cutoff-removal topology.
- falsifier: an indefinite additive boundary contact survives in mixed OS entries, showing that the multiplicative boundary Gram model omitted a valid obstruction.

## Learning

Cycle 210 makes log-CND a conditional tool, not a theorem. The exact valid obstruction is finite positivity of q=Nh/Bh. Infinite-divisibility or Hadamard semigroup structure is the extra assumption that turns q>=0 into a generator test; without it, determinants are the real falsifier search.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the reflected Wilson hairpin OPE for three shared-footprint loops at two collar thicknesses; test q_{r+s}=q_r∘q_s and det(\widehat N\oslash\widehat B)>=0.
