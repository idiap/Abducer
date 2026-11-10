# cycle-0212

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Finite Wilson collar collapse preserves same-theory OS positivity exactly when the normalized Schur preimage q=\widehat N\oslash\widehat B is positive semidefinite on every realized locked Wilson block.

## Definitions

- source object: a finite locked gauge-invariant Wilson collar family F_i^\delta supported in t>\delta, its reflected collar-limit OS matrix N, and the multiplicative boundary Gram factor B from reflected Wilson hairpin OPE.
- target object: the intended continuum OS matrix M_{ij}=S(\Theta F_i,F_j) on the same Wilson observables, hence the pre-Hilbert OS form before null quotient.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through convergence of finite reflected quadratic forms plus a collar trace limit.
- same-theory condition: collar collapse may change observables only by diagonal/unitary congruence already present in the locked renormalization; any pair-dependent boundary factor must be divided out without adding boundary observables.

## Assumptions

- For each fixed collar, regulated reflection positivity and RG convergence give a valid PSD limit matrix N.
- Diagonal Wilson trace limits exist with positive diagonal entries, and positive additive boundary contacts have been eliminated or proved zero.
- The boundary OPE is multiplicative on the finite block: N_{ij}=B_{ij}M_{ij}, with B Hermitian, B_{ii}>0, and B_{ij}\ne0 on the tested block.
- The finite family belongs to the locked gauge-invariant test algebra before and after collar collapse.

## Equations

- multiplicative boundary factor: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta F_i^\delta,F_j^\delta),\qquad N_{ij}=B_{ij}M_{ij}`. Valid when: The reflected Wilson collar OPE has no surviving additive contact and its pair-dependent part is a multiplicative boundary factor.
- normalized Schur preimage: `q_{ij}=\frac{N_{ij}}{B_{ij}}\left(\frac{B_{ii}B_{jj}}{N_{ii}N_{jj}}\right)^{1/2}=\widehat N_{ij}/\widehat B_{ij},\qquad M\ge0\Longleftrightarrow q\ge0`. Valid when: All tested diagonal entries are positive and diagonal congruences are regarded as same-theory normalizations.
- three-hairpin determinant: `\det q=1+2r_{12}r_{23}r_{13}\cos\Phi-r_{12}^2-r_{23}^2-r_{13}^2,\quad \Phi=\arg(q_{12}q_{23}\overline{q_{13}})`. Valid when: q is a normalized Hermitian 3-by-3 quotient matrix with q_{ij}=r_{ij}e^{i\phi_{ij}}.
- infinitesimal quotient test: `q(\lambda)=\mathbf 1\mathbf 1^*+\lambda H+o(\lambda),\quad q(\lambda)\ge0\ (0<\lambda\ll1)\Rightarrow c^*Hc\ge0\ \forall c:\sum_i c_i=0`. Valid when: A physical or auxiliary parameter \lambda gives a differentiable family of realized quotient blocks with q(0) the rank-one all-ones matrix.

## Attempted Derivation

- Fix a finite locked Wilson collar family F_i^\delta and form N^\delta_{ij}=S(\Theta F_i^\delta,F_j^\delta).
- Regulated reflection positivity gives N^\delta\ge0; fixed-collar RG convergence transfers this to N\ge0 by closedness of the finite OS cone.
- Assume diagonal trace continuity, so any positive additive contact with zero diagonal vanishes by Cauchy-Schwarz; remaining boundary effect is tested as N=B\circ M.
- Since diagonal congruence is same-theory harmless, normalize N, B, and M. Then \widehat M=\widehat N\oslash\widehat B=q, so intended OS positivity on this block is exactly q\ge0.
- For three Wilson hairpins, compute det q explicitly; the quotient phase holonomy \arg(q_{12}q_{23}\overline{q_{13}}) enters at the first phase-sensitive minor.
- For a differentiable quotient q(\lambda)=\mathbf1\mathbf1^*+\lambda H+o(\lambda), zero-sum test vectors annihilate the rank-one part, so positivity for small \lambda forces H to be PSD on the zero-sum subspace.

Blocking gap: The Yang-Mills boundary OPE for reflected Wilson triples has not been computed in the locked algebra, so B, N, and the leading quotient kernel H are not yet known to exist with the required uniform collar limits.

## Falsifiers

- A realized reflected Wilson triple with 1+2r12 r23 r13 cos(Phi)-r12^2-r23^2-r13^2<0 is a direct same-theory falsifier.
- A leading boundary quotient kernel H with a zero-sum vector c satisfying c^*Hc<0 falsifies any valid small-parameter Schur-preimage passage.
- A boundary factor B_{ij}=0 while N_{ij}\ne0 makes the quotient singular and signals that the collar algebra is not the same theory.
- A proof that positivity survives only by retaining the dressed matrix N=B\circ M, instead of the intended M, shows that a new boundary theory has been introduced.
- An indefinite additive contact term at the reflection plane invalidates the reduction to a multiplicative Schur quotient.
- The cutoff-removal topology might control fixed collars but fail to control the simultaneous reflected Wilson collar collapse.

## Learning

Cycle 212 converts the Wilson boundary obstruction into an exact finite Schur-preimage bridge plus a perturbative tangent detector. The valid criterion remains q=\widehat N\oslash\widehat B\ge0 on realized Wilson blocks; log-CND/CPD is justified only if a Hadamard semigroup is proved. The first concrete falsifier is now either a negative three-hairpin quotient determinant or a zero-sum negative leading quotient kernel from the boundary OPE.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading boundary quotient H for three mirror-smooth Wilson hairpins with a common reflection-plane footprint; evaluate the determinant formula and the zero-sum quadratic forms before attempting any higher-minor theorem.
