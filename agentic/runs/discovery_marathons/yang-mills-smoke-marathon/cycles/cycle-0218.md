# cycle-0218

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson quotient tangent cone

## Candidate Lemma

For a finite locked Wilson OS block whose collar quotient satisfies q_\delta=J+\lambda_\delta H+\lambda_\delta^2K+o(\lambda_\delta^2), same-theory OS positivity near the reflection plane is governed by the PSD tangent cone at the rank-one matrix J. The first necessary condition is PHP\ge0 on 1^\perp; if L=\ker(PHP), the next valid obstruction is the Schur-corrected form P(K-n^{-1}Hu u^*H)P\ge0 on L. A negative vector in either test is a finite Wilson falsifier.

## Definitions

- source object: regulated reflection-positive Schwinger forms for collar-separated gauge-invariant Wilson observables W_i(\delta), with finite collar OS matrices N_\delta\ge0.
- target object: OS-positive continuum Schwinger functions on the uncollared locked Wilson algebra, represented by intended finite matrices M after removing only same-theory boundary factors.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through the normalized Schur quotient q=\widehat N\oslash\widehat B, after fixed-collar closed-cone passage.
- same-theory condition: the observable embeddings are fixed before and after cutoff removal; any boundary factor B may be divided out only if q remains PSD for every realized finite Wilson block, with no added boundary counterterm or algebra change.
- J is the all-ones matrix, u=n^{-1/2}(1,\ldots,1), and P=I-uu^* projects onto 1^\perp.

## Assumptions

- N_\delta is the collar-limit OS matrix obtained from regulated reflection-positive forms, hence N_\delta\ge0 for each fixed collar.
- Diagonal trace continuity has removed additive positive contacts, and all diagonal normalizations are nonzero.
- The reflected Wilson boundary OPE gives a Hermitian expansion q_\delta=J+\lambda_\delta H+\lambda_\delta^2K+o(\lambda_\delta^2), uniformly on the finite block.
- The same-theory boundary multiplier B is the one determined by the locked Wilson renormalization, not chosen after seeing N.

## Equations

- same-theory quotient criterion: `\widehat N_{ij}=\frac{N_{ij}}{(N_{ii}N_{jj})^{1/2}},\quad \widehat B_{ij}=\frac{B_{ij}}{(B_{ii}B_{jj})^{1/2}},\quad q=\widehat N\oslash\widehat B,\quad M\ge0\Longleftrightarrow q\ge0`. Valid when: The diagonal entries are positive, additive contacts vanish, and the only remaining boundary effect is a multiplicative Wilson factor on the same locked algebra.
- rank-one boundary expansion: `q_\delta=J+\lambda_\delta H+\lambda_\delta^2K+o(\lambda_\delta^2),\qquad J_{ij}=1,\quad H=H^*,\ K=K^*`. Valid when: The coincident-footprint reflected Wilson OPE has a two-term finite-matrix asymptotic after normalization.
- first tangent gate: `v^*Hv\ge0\quad\text{for all }v\in 1^\perp\quad\text{equivalently}\quad PHP\ge0`. Valid when: q_\delta\ge0 for all sufficiently small positive collars; a negative value is an immediate falsifier.
- second tangent gate: `\left. P\left(K-\frac1nHu u^*H\right)P\right|_{\ker(PHP)}\ge0`. Valid when: PHP\ge0 and the first-order form has null directions; this is the Schur-complement obstruction after eliminating the large positive J direction.

## Attempted Derivation

- Start from fixed-collar reflection positivity: N_\delta\ge0 is preserved by the closed-cone argument in the OS topology for reflected probes.
- Separate same-theory boundary effects by writing the intended uncollared normalized matrix as q_\delta=\widehat N_\delta\oslash\widehat B_\delta.
- Assume the boundary OPE is close to the rank-one no-defect case: q_\delta=J+\lambda H+\lambda^2K+o(\lambda^2).
- Decompose \mathbb C^n=\mathbb C u\oplus1^\perp. The u-block is n+O(\lambda), hence positive for small collar.
- Take the Schur complement of the u-block. On 1^\perp it is \lambda PHP+\lambda^2P(K-n^{-1}Hu u^*H)P+o(\lambda^2).
- Therefore a negative direction of PHP kills OS positivity at first order. If PHP has null directions, the Schur-corrected second-order form decides the next obstruction on that null space.

Blocking gap: The derivation is finite-dimensional and valid, but Yang-Mills input is missing: no current estimate computes the Wilson hairpin boundary OPE coefficients H,K with enough control to prove the two tangent gates on the locked Wilson core.

## Falsifiers

- A boundary OPE calculation producing v\in1^\perp with v^*Hv<0 is a first-order falsifier of same-theory OS passage.
- If PHP\ge0 but a null vector v has v^*(K-n^{-1}Hu u^*H)v<0, the second-order Schur-complement term is a valid falsifier.
- A collar-removal topology that controls N but not the boundary multiplier B cannot validate q=\widehat N\oslash\widehat B.
- If Wilson renormalization at the reflection plane requires a new boundary counterterm, positivity may hold for a modified theory but not for the target same theory.

## Learning

Cycle 218 learned that the next obstruction is not just PKP on the null space of the first-order kernel. The large rank-one OS direction contributes a necessary negative Schur correction -n^{-1}PHu u^*HP. Thus the valid second-order Wilson falsifier is a Schur-complement boundary OPE form, making the bridge sharper and more computable.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the reflected two- and three-hairpin Wilson boundary OPE to extract H and K, then test the zero-sum and null-space Schur-complement inequalities on the smallest nontrivial finite block.
