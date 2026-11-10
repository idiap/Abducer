# cycle-0208

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For any finite locked Wilson collar block, if additive boundary contacts vanish and q=\widehat N\oslash\widehat B has a Hermitian logarithm L that is conditionally positive on zero-sum vectors, then the same-theory zero-collar OS matrix is positive. With valid density this passes OS positivity to the continuum.

## Definitions

- source object: finite collar-regulated reflected Wilson OS matrices N from cutoff Schwinger forms, with boundary Gram factor B extracted by the reflected hairpin OPE.
- target object: continuum zero-collar OS matrices M on the locked gauge-invariant Wilson algebra, hence OS-positive Schwinger functions after density.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via collar limits, boundary quotient q, and closed finite OS cones.
- same-theory condition: the Wilson embeddings, diagonal trace limits, and renormalizations are fixed before the limit; B may encode only removable boundary factors, not a new algebra or boundary counterterm.

## Assumptions

- Fixed-collar RG convergence is strong enough for every reflected finite Wilson quadratic form, so the closed-cone transfer to N is valid.
- The boundary OPE gives a multiplicative normalized factor \widehat B with nonzero entries after diagonal trace continuity; positive additive contacts have zero diagonal and vanish.
- For each realized finite Wilson block, q=\widehat N\oslash\widehat B admits a Hermitian logarithm L with \sum_i z_i=0 implying \sum_{ij}\bar z_i z_j L_{ij}\ge0.
- The mirror-smooth local/Wilson core is OS-dense in the target gauge-invariant test algebra.

## Equations

- collar OS limit: `N_{ij}=\lim_{\delta\downarrow0}\lim_{a,L}S_{a,L}(\Theta F_i^\delta,F_j^\delta),\qquad N\ge0`. Valid when: Regulated reflection positivity holds and RG convergence is valid on fixed-collar reflected probes.
- same-theory boundary quotient: `q_{ij}=\widehat N_{ij}/\widehat B_{ij},\qquad \widehat N_{ij}=N_{ij}/(N_{ii}N_{jj})^{1/2},\quad \widehat B_{ii}=1`. Valid when: Additive contacts vanish and the boundary anomaly is a multiplicative Wilson hairpin factor.
- log-CPD certificate: `e^{L_{ij}}=q_{ij},\quad \sum_i z_i=0\Rightarrow \sum_{ij}\bar z_i z_jL_{ij}\ge0\ \Longrightarrow\ q\ge0`. Valid when: A Hermitian logarithm branch exists; Schoenberg conditional-positivity applies to the finite block.

## Attempted Derivation

- Start with cutoff reflection positivity on F_i^\delta. Fixed-collar RG convergence transfers each finite quadratic form to a positive collar matrix, then δ→0 gives N≥0 if the trace limit exists.
- Use the reflected Wilson boundary OPE to write normalized collar data as \widehat N=\widehat B\circ \widehat M. Diagonal trace continuity and positive-contact compatibility remove additive defects, so the intended target is \widehat M=q.
- Assume q=e^L with L Hermitian and conditionally positive on zero-sum vectors. Schoenberg gives e^{tL}≥0 for all t≥0, hence q≥0 at t=1.
- Restore the unnormalized target matrix by positive diagonal congruence. If this holds on every dense locked block, all OS quadratic forms of the continuum Schwinger functions are nonnegative.

Blocking gap: The finite matrix implication is valid, but Yang-Mills analysis has not proved the reflected Wilson boundary OPE yields no additive contact and log-CPD q for all realized blocks.

## Falsifiers

- falsifier: a three-hairpin Wilson block has q_{ij}=\widehat N_{ij}/\widehat B_{ij} with all 2-by-2 minors valid but det q<0.
- falsifier: diagonal trace continuity holds, yet the boundary OPE leaves a nonzero off-diagonal additive contact; this contradicts the positive-contact vanishing step.
- falsifier: quotient phases admit a Hermitian log, but some zero-sum z gives \sum\bar z_i z_j L_{ij}<0, so the log-CPD certificate fails.
- falsifier: \widehat B_{ij}=0 while \widehat N_{ij}\ne0, or the locked Wilson observable changes across the collar limit; the same-theory Schur quotient is then undefined.

## Learning

Cycle 208 isolates a stronger all-minors route: q=\widehat N\oslash\widehat B is the exact same-theory obstruction, and log-CPD is a compact sufficient certificate. Nonzero phase holonomy is not alone a falsifier; negativity of q or of its log-CPD quadratic form is.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the reflected three-hairpin boundary OPE to extract \widehat B, \widehat N, and L=log(\widehat N\oslash\widehat B); test determinant positivity and the zero-sum log-CPD quadratic form.
