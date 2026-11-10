# cycle-0196

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Realized Boundary-Damping Detector

## Candidate Lemma

Let a locked pair of gauge-invariant collar Wilson observables F_1^\delta,F_2^\delta have a reflected collar OS matrix N=\lim_{\delta\downarrow0}\lim_{a,L} S_{a,L}(\Theta F_i^\delta,F_j^\delta)\ge0. Suppose the intended same-theory boundary value M is related to the collar limit by a normalized multiplicative hairpin boundary Gram factor B with N_{ij}=B_{ij}M_{ij}, B_{ii}=1, and 0<|B_{12}|\le1. Then the same-theory OS passage is valid for this two-dimensional realized sector if and only if |N_{12}|^2\le |B_{12}|^2N_{11}N_{22}. Hence a realized pair with |N_{12}|^2>|B_{12}|^2N_{11}N_{22} is a concrete falsifier of the bridge, while a nonrank-one B is harmless on this sector whenever the realized collar correlation is below the boundary damping threshold.

## Definitions

- source object: regulated reflection-positive gauge-invariant Wilson collar Schwinger forms S_{a,L} restricted to a fixed locked two-observable core, with the limits a\downarrow0, L\uparrow\infty, and collar width \delta\downarrow0 taken only through reflected OS matrix entries.
- target object: OS-positive continuum Schwinger functions on the intended zero-collar gauge-invariant Wilson algebra, not on a boundary-renormalized enlargement or quotient.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, mediated by convergence of every finite reflected matrix entry and by an explicit boundary anomaly relation N=B\circ M.
- same-theory condition: the map F_i^\delta\mapsto F_i is fixed before taking the collar limit, and every boundary factor B_{ij} is either already part of the locked observable normalization or must pass the realized determinant test without adding new boundary degrees of freedom.

## Assumptions

- The cutoff Schwinger forms are reflection-positive on the positive-time gauge-invariant test algebra for each regulator pair (a,L).
- For the chosen collar Wilson observables, all reflected finite matrix entries converge in the RG cutoff-removal topology and then in the collar topology.
- The multiplicative boundary anomaly is entrywise nonzero on the tested pair and normalized by diagonal trace continuity, so B_{11}=B_{22}=1 and N_{ii}=M_{ii}.
- The intended zero-collar matrix is obtained by the Hadamard quotient M=B^{[-1]}\circ N rather than by changing the observable algebra.

## Equations

- collar positivity: `N=\lim_{\delta\downarrow0}\lim_{a,L} \big(S_{a,L}(\Theta F_i^\delta,F_j^\delta)\big)_{i,j=1}^2\succeq0`. Valid when: The RG topology controls the reflected collar probes and the positivity cone is closed for these finite OS matrices.
- boundary anomaly relation: `N_{ij}=B_{ij}M_{ij},\qquad B_{11}=B_{22}=1,\qquad 0<|B_{12}|\le 1`. Valid when: Collar collapse produces only a normalized multiplicative reflected Wilson hairpin factor, with no surviving additive contact term.
- same-theory determinant criterion: `M\succeq0\ \Longleftrightarrow\ |M_{12}|^2\le M_{11}M_{22}\ \Longleftrightarrow\ |N_{12}|^2\le |B_{12}|^2N_{11}N_{22}`. Valid when: The two diagonal entries are finite and positive, diagonal trace continuity holds, and M=B^{[-1]}\circ N is the intended target OS matrix.
- realized falsifier inequality: `\rho_N:=\frac{|N_{12}|}{(N_{11}N_{22})^{1/2}}>|B_{12}|\quad\Longrightarrow\quad \det M<0`. Valid when: The observed collar correlation coefficient exceeds the boundary damping supplied by the hairpin Gram factor.

## Attempted Derivation

- Start with regulated reflection positivity: for every collar width \delta and cutoff pair (a,L), the finite OS matrix N_{a,L,\delta,ij}=S_{a,L}(\Theta F_i^\delta,F_j^\delta) is positive semidefinite.
- Use the closed-cone passage only for the actually controlled reflected probes to obtain N\succeq0 in the collar limit; this step is valid but only proves positivity for the collar-limit matrix N.
- Model the remaining boundary collapse by N=B\circ M+A, where M is the intended same-theory zero-collar OS matrix, B is a normalized multiplicative hairpin factor, and A is an additive contact.
- Apply the positive-contact elimination lemma: if A\succeq0 and diagonal trace continuity gives A_{11}=A_{22}=0, then A=0 on this two-observable sector.
- With A=0 and B_{11}=B_{22}=1, compute M_{11}=N_{11}, M_{22}=N_{22}, and M_{12}=N_{12}/B_{12}.
- The two-by-two OS condition for M is det M=N_{11}N_{22}-|N_{12}|^2/|B_{12}|^2\ge0, equivalently |N_{12}|^2\le |B_{12}|^2N_{11}N_{22}.
- Thus nonrank-one boundary covariance is not automatically fatal; it becomes a falsifier only when a realized locked Wilson pair has collar correlation exceeding the boundary damping threshold.

Blocking gap: The derivation still assumes that the boundary anomaly admits the clean finite decomposition N=B\circ M+A with diagonal trace continuity and either positive A or no A. The hard Yang-Mills gap is to derive B_{12} and N_{12} from the actual reflected Wilson OPE/RG construction for a concrete locked pair, rather than postulating them as finite matrices.

## Falsifiers

- Concrete determinant falsifier: a locked pair with |N_{12}|/(N_{11}N_{22})^{1/2}>|B_{12}| gives det M<0, so collar positivity does not imply same-theory OS positivity.
- Boundary-decomposition falsifier: the collar collapse produces an additive contact with zero diagonal but nonzero off-diagonal, showing either positivity of the contact or diagonal trace continuity has failed.
- Topology falsifier: the multiscale convergence controls individual Wilson loop expectations but not the mixed reflected products needed to define N_{12}.
- Same-theory falsifier: the only way to restore positivity is to absorb B into a new boundary Hilbert sector or boundary counterterm not present in the locked gauge-invariant algebra.
- Richness falsifier: every realizable locked Wilson pair has \rho_N\le |B_{12}| even when B is nonrank-one, so the proposed determinant test cannot detect the boundary covariance on the available algebra.

## Learning

Cycle 196 clarifies that the boundary Gram obstruction is a threshold phenomenon, not a yes/no property of B alone. The closed-cone argument is valid for the collar-limit OS matrix N, and positive additive contacts vanish once diagonal trace continuity is valid. The remaining same-theory question is whether the intended target matrix M=B^{[-1]}\circ N stays positive on realized Wilson sectors. For two observables this is exactly the inequality \rho_N\le |B_{12}|. This avoids the earlier overclaim that every nonrank-one boundary Gram factor is automatically fatal, while still giving a concrete falsifier: a realized collar correlation larger than the hairpin damping produces a negative OS determinant.

## Next Experiment

Pick a minimal pair of reflected Wilson hairpin observables sharing a boundary footprint. Compute the leading boundary OPE contribution to B_{12}, normalize B_{ii}=1, and compare it with a rigorous or perturbative bound on the realized collar correlation coefficient \rho_N=|N_{12}|/(N_{11}N_{22})^{1/2}; the first target is to decide whether \rho_N>|B_{12}| can occur.
