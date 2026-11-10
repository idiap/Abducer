# cycle-0207

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For any finite locked Wilson hairpin block, after fixed-collar OS positivity and after additive boundary contacts vanish, the same-theory target OS matrix is positive if its normalized boundary quotient q has a Hermitian logarithm h=Log q that is conditionally positive on the zero-sum subspace. This complex log-CPD test is a valid Schoenberg certificate and strictly sharpens the previous coboundary-phase plus CND-modulus sufficient condition.

## Definitions

- source object: regulated reflection-positive gauge-invariant Schwinger forms S_{a,L} on a locked Wilson/local observable core, with collar supports t\ge \delta and RG convergence for all reflected finite pairings.
- target object: continuum OS-positive Schwinger functions on the same gauge-invariant observable core, with the intended reflection-plane Wilson limits and no added boundary degrees of freedom.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, first by fixed-collar closed-cone transfer and then by a finite Schur quotient across the collar trace.
- same-theory condition: the collar-to-plane map identifies each Wilson observable with its predeclared continuum renormalization; multiplicative boundary factors may only be divided out if the resulting quotient matrix is positive on the realized locked algebra, not by changing the algebra.

## Assumptions

- For each finite family W_i, the fixed-collar matrices converge to a positive matrix N.
- Diagonal trace continuity eliminates positive additive contacts; any remaining boundary anomaly is multiplicative and nonzero on the block.
- The normalized intended target block is q=\widehat N\oslash \widehat B with q_{ii}=1 and q_{ji}=\overline{q_{ij}}.
- A continuous Hermitian logarithm h_{ij}=\operatorname{Log} q_{ij}, h_{ii}=0, is selected by the collar deformation.
- h is conditionally positive: \sum_{i,j}\overline z_i z_j h_{ij}\ge0 whenever \sum_i z_i=0.

## Equations

- multiplicative boundary quotient: `M_{ij}=N_{ij}/B_{ij},\qquad q_{ij}=M_{ij}/(M_{ii}M_{jj})^{1/2}=\widehat N_{ij}\oslash\widehat B_{ij}`. Valid when: Additive boundary contacts have vanished and B_{ij}\ne0 on the finite Wilson block.
- log-Schoenberg certificate: `h_{ij}=\operatorname{Log}q_{ij},\quad h_{ii}=0,\quad z^*hz\ge0\ (\sum_i z_i=0)\ \Longrightarrow\ [e^{h_{ij}}]_{ij}=q\ge0`. Valid when: The logarithm is Hermitian on the chosen branch; this is the complex Schoenberg theorem for normalized positive kernels.
- three-point determinant test: `\det q=1+2\operatorname{Re}(q_{12}q_{23}\overline{q_{13}})-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2\ge0`. Valid when: q is a normalized 3 by 3 quotient block; failure is a direct OS falsifier for that realized triple.

## Attempted Derivation

- Start with cutoff reflection positivity: Q_{a,L}(F,c)=\sum\overline c_i c_j S_{a,L}(\Theta F_i,F_j)\ge0 for collar-supported Wilson observables.
- Use RG convergence valid for reflected collar probes to pass to continuum fixed-collar matrices N^{\delta}\ge0 by the closed-cone argument.
- Let \delta\downarrow0. Diagonal trace continuity plus positivity kills positive additive contact matrices, so any remaining obstruction is multiplicative: N=B\circ M.
- Normalize diagonals to get the intended target quotient q=\widehat M=\widehat N\oslash\widehat B. The same-theory problem is exactly q\ge0 on every realized finite Wilson block.
- Instead of requiring quotient phases to be coboundaries, choose the collar-continuous Hermitian logarithm h=Log q. If h is conditionally positive on zero-sum vectors, Schoenberg gives e^{h}=q\ge0; hence the target block is OS positive.
- If the Wilson algebra realizes q(t)=e^{t h} through same-theory amplification, positivity of q(t) for small t forces h to be conditionally positive by differentiating z^*q(t)z on z\perp1.

Blocking gap: The proof still lacks a Yang-Mills construction of the amplification parameter and the factorization q(t)=e^{t h} inside the locked nonabelian Wilson algebra; trace products may decompose into representations with extra self-intersection or boundary renormalizations.

## Falsifiers

- Direct finite falsifier: a realized three-hairpin quotient with 1+2Re(q12 q23 conjugate(q13))-|q12|^2-|q23|^2-|q13|^2<0.
- Infinitesimal falsifier: an amplified family with z^*Log(q)z<0 for some zero-sum z, giving negative OS norm for small amplification t.
- Branch falsifier: zeros of B or q appear in the collar limit, so the logarithmic Schur quotient is not a same-theory boundary trace but a boundary superselection collapse.
- Algebra falsifier: replicated or Poissonized hairpins require adding observables or boundary counterterms not present in the original gauge-invariant test algebra.
- Topology falsifier: RG convergence remains valid for fixed collars but not for the logarithmic boundary OPE needed to identify h.

## Learning

Cycle 207 corrects and sharpens the previous two-stage obstruction. Vanishing triangle phase holonomy plus CND modulus is a useful sufficient certificate, but the more intrinsic finite bridge is complex logarithmic conditional positivity of q=\widehat N\oslash\widehat B. Nonzero phase holonomy is therefore not automatically a falsifier; it is detected through the full determinant or log-CPD quadratic form. If same-theory Wilson amplifications are valid, log-CPD becomes necessary by an infinitesimal zero-sum test.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the reflected three-hairpin boundary quotient to first nontrivial order, extract h=Log q, and test z^*hz on the two-dimensional zero-sum subspace; compare with the determinant falsifier at t=1.
