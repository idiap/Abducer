# cycle-0193

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Rich-Cone Boundary Gram Test

## Candidate Lemma

Let A_+ be the locked gauge-invariant positive-time Wilson/core test algebra and let T_delta move each observable into a collar t >= delta. Suppose the cutoff-removal topology is valid for all finite reflected collar OS matrix entries, so the collar matrices N_delta(F) converge to positive matrices N(F). Suppose further that the intended zero-collar target matrix M(F) is related to N(F) by a multiplicative boundary Gram factor B(F), N_{ij}=B_{ij}M_{ij}, after additive positive contacts have vanished by diagonal trace continuity. If the realized family of collar OS matrices is locally rich enough to contain all two-dimensional rank-one perturbation directions around each pair of Wilson hairpins, then OS positivity of the intended same-theory target for all finite F forces B to be rank one on the locked Wilson core. Equivalently, the logarithmic cross-ratio K_{ik;jl}=log B_{ij}+log B_{kl}-log B_{il}-log B_{kj} must vanish; any nonzero K is a finite-matrix falsifier of the same-theory OS bridge.

## Definitions

- source object: regulated reflection-positive Schwinger forms S_{a,L} evaluated on the fixed collar algebra T_delta A_+ of gauge-invariant local composites and Wilson hairpin observables, with finite OS matrices N_delta=(S_{a,L}(Theta T_delta F_i,T_delta F_j))_{ij}.
- target object: OS-positive continuum Schwinger functions S on the locked zero-collar algebra A_+, with intended matrices M=(S(Theta F_i,F_j))_{ij} generating the physical Hilbert space, vacuum vector, and positive Hamiltonian by the Osterwalder-Schrader quotient.
- controlled interface: convergence of every finite reflected collar matrix entry N_delta -> N in the cutoff-removal topology, plus a trace comparison N_{ij}=B_{ij}M_{ij}+A_{ij} where A is an additive boundary contact matrix and B is a normalized multiplicative boundary Gram factor from reflected Wilson hairpins.
- same-theory condition: the zero-collar algebra A_+ and its renormalized Wilson-loop/composite observables are fixed before taking delta -> 0; only diagonal congruences already included in the locked observable normalization are allowed, while pair-dependent boundary sectors, cusp factors, or contact counterterms define a different theory.

## Assumptions

- Each cutoff theory is reflection positive on the gauge-invariant lattice/cutoff algebra, so N_delta >= 0 for every finite family and coefficient vector.
- The RG compactness topology dominates finite reflected collar probes: for each fixed delta > 0 and finite F, N_delta(F) has a continuum limit N(F) and positivity passes by closedness of the positive matrix cone.
- Diagonal trace continuity is valid on the locked Wilson core: N_{ii}->M_{ii} after the prescribed individual Wilson renormalizations, so any positive additive contact A with zero diagonal vanishes by Cauchy-Schwarz.
- The multiplicative boundary anomaly is Gram-positive: B_{ij}=<b_i,b_j>_partial with B_{ii}>0, representing a possible boundary Hilbert sector produced by collar collapse.
- Rich-cone hypothesis: for every pair i,j in a dense Wilson hairpin core, the set of realized positive collar matrices N contains enough two-by-two rank-one and small positive perturbation directions that a Schur multiplier preserving positivity on all realized N must pass the usual two-by-two Schur positivity tests.

## Equations

- collar OS matrix: `N^{(\delta)}_{ij}(F)=S(\Theta T_\delta F_i,T_\delta F_j),\qquad N^{(\delta)}(F)\ge 0`. Valid when: T_delta F_i have support in a positive-time collar separated from the reflection plane and regulated reflection positivity has survived the fixed-collar cutoff limit.
- boundary trace decomposition: `\lim_{\delta\downarrow0}N^{(\delta)}_{ij}=N_{ij}=B_{ij}M_{ij}+A_{ij}`. Valid when: The collar limit exists entrywise for the locked finite Wilson/core family and boundary singularities split into multiplicative Wilson hairpin factors plus additive contact terms.
- positive additive contacts vanish: `A\ge0,\quad A_{ii}=0\ \forall i\quad\Longrightarrow\quad |A_{ij}|^2\le A_{ii}A_{jj}=0\quad\Longrightarrow\quad A=0`. Valid when: The contact contribution is itself a positive semidefinite OS boundary form and diagonal trace continuity has already removed all diagonal boundary excess.
- same-theory target from collar limit: `M=B^{[-1]}\circ N,\qquad (B^{[-1]})_{ij}=1/B_{ij}`. Valid when: There are no additive contacts, B has no zero entries on the chosen finite core, and the intended target normalization has not absorbed pair-dependent factors.
- rank-one obstruction invariant: `K_{ik;jl}=\log B_{ij}+\log B_{kl}-\log B_{il}-\log B_{kj};\qquad K\equiv0\iff B_{ij}=r_i\overline{r_j}`. Valid when: A consistent logarithm is chosen on a connected finite core with nonzero B entries; the equivalence is local on finite matrices and modulo diagonal congruence phases.

## Attempted Derivation

- Start with regulated positivity Q_{a,L}(f,c)>=0. For fixed collar delta, RG convergence of reflected finite matrix entries gives N^{(delta)}(F)>=0 in the continuum because the positive semidefinite matrix cone is closed.
- Let delta down to zero. The formal closed-cone argument alone gives positivity of the collar-limit matrix N, not of the intended target matrix M, because boundary singularities may relate them by N=B circ M + A.
- Use diagonal trace continuity on locked Wilson observables. If A is a positive additive boundary contact, then A_{ii}=0 for all i; Cauchy-Schwarz gives A_{ij}=0. Therefore additive positive contacts cannot be the surviving obstruction once the diagonal trace theorem is valid.
- The remaining relation is M=B^{[-1]} circ N. If B^{[-1]} is a positive Schur multiplier on the relevant matrices, then M>=0 follows from N>=0. If this must hold for all positive matrices, the Schur product theorem requires B^{[-1]}>=0.
- Combine B>=0 from the boundary Gram representation with B^{[-1]}>=0. For a normalized two-by-two principal minor, B=[[1,b],[conj(b),1]] and B^{[-1]}=[[1,1/b],[1/conj(b),1]] being positive forces |b|<=1 and |1/b|<=1, hence |b|=1; Cauchy-Schwarz then makes b_i and b_j collinear. Repeating over pairs makes B rank one and K=0.
- The correction in this cycle is that the universal Schur step is stronger than the physical hypothesis unless the realized collar OS cone is rich. Therefore the valid bridge lemma must include richness of Wilson hairpin matrix directions, or replace universal positivity by an explicit realized finite-matrix determinant falsifier.

Blocking gap: The missing Yang-Mills estimate is now twofold: prove the rich-cone hypothesis for the locked Wilson/core algebra near reflected hairpin collars, and prove the boundary Gram factor B is validly isolated from the actual RG/collar limit. Without richness, nonzero K suggests an obstruction but is not yet a proof of OS failure for realized observables.

## Falsifiers

- A direct two-by-two realized Wilson hairpin matrix N with N>=0 but det(B^{[-1]} circ N)<0; this is the cleanest finite falsifier of the same-theory OS bridge.
- A four-observable Wilson hairpin family with nonzero logarithmic cross-ratio K after all allowed individual renormalizations, together with richness witnesses showing that this K is tested by realized OS matrices.
- A positive collar limit whose zero-collar comparison requires an additive contact A with zero diagonal but nonzero off-diagonal; this would falsify the assumed positive-boundary-contact decomposition itself.
- A boundary Gram factor B that is nonrank-one but the realized OS cone C_B is too small to detect it; this falsifier targets the necessity of the rank-one conclusion rather than OS positivity itself.
- A change of Wilson-loop renormalization at the reflection plane that absorbs B by pair-dependent counterterms; this preserves a modified positive theory but violates the same-theory condition.

## Learning

Cycle 193 found an important correction to the previous rank-one conclusion. The finite-dimensional theorem is valid when reciprocal Schur positivity is required on a rich enough cone of OS matrices; then a positive boundary Gram factor must be rank one and K=0. But the physical problem only gives realized Wilson OS matrices, not arbitrary positive matrices. Thus the next real bridge lemma must include a rich-cone/density hypothesis, or else produce an actual realized determinant falsifier. This is substantive progress because it prevents overclaiming: nonzero boundary covariance is a decisive same-theory obstruction only after the locked Wilson algebra can test it.

## Next Experiment

Work on a two-observable Wilson hairpin model: define F_1,F_2 with coincident boundary footprints, compute the normalized collar matrix N and candidate Gram factor B to first nontrivial boundary-OPE order, and test whether the determinant inequality det(B^{[-1]} circ N)>=0 is automatic, violated, or dependent on a richness/density assumption.
