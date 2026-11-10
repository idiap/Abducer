# cycle-0206

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Schur-Preimage Boundary Test

## Candidate Lemma

After fixed-collar OS positivity has passed to the continuum, the reflection-plane step is valid for a finite Wilson family if the normalized Schur quotient q=\widehat N\oslash\widehat B has coboundary phase and conditionally negative logarithmic modulus. Then the intended same-theory OS matrix M=N\oslash B is positive.

## Definitions

- source object: finite locked gauge-invariant Wilson collar families F_i^\delta with regulated reflection-positive OS matrices and collar-limit matrix N.
- target object: OS-positive continuum Schwinger functions on the same Wilson/local gauge-invariant test algebra, encoded by target matrices M.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, factored through fixed-collar closed-cone passage and reflection-plane Schur preimage.
- same-theory condition: the labels F_i are not changed at the boundary; additive contacts vanish; multiplicative factors B are only trace-renormalization ratios, so the intended matrix is M=N\oslash B rather than a boundary-enlarged theory.
- \widehat X_{ij}=X_{ij}/(X_{ii}X_{jj})^{1/2} for positive diagonal finite matrices.
- A finite real kernel d is conditionally negative definite when \sum_{i,j}\bar z_i z_j d_{ij}\le0 for every \sum_i z_i=0.

## Assumptions

- Regulated reflection positivity holds for the collar observables and RG convergence is valid for every fixed-collar reflected quadratic form.
- The collar limit N_{ij}=\lim_{\delta\downarrow0}S(\Theta F_i^\delta,F_j^\delta) exists and N\ge0.
- Diagonal trace continuity holds; positive additive boundary contacts therefore vanish by Cauchy-Schwarz.
- The boundary OPE produces a Hermitian multiplicative anomaly B with positive diagonal and no zero entry on the tested finite family.
- The quotient phases are coboundaries and d_{ij}=-\log |\widehat N_{ij}/\widehat B_{ij}| is conditionally negative definite.

## Equations

- normalized Schur preimage: `\widehat M_{ij}=q_{ij}:=\frac{\widehat N_{ij}}{\widehat B_{ij}},\qquad M=N\oslash B`. Valid when: Valid when B_{ij}\ne0, diagonals are positive, and the boundary trace defect is purely multiplicative.
- coboundary-CND certificate: `q_{ij}=e^{i(\chi_i-\chi_j)}e^{-d_{ij}},\quad d_{ii}=0,\quad \sum_{i,j}\bar z_i z_jd_{ij}\le0\ (\sum_i z_i=0)\ \Longrightarrow\ q\ge0`. Valid when: Valid by diagonal unitary removal of phases and Schoenberg positivity of e^{-d} for finite CND kernels.
- target positivity reconstruction: `q\ge0\quad\Longleftrightarrow\quad M\ge0\quad\text{for }M_{ii}>0`. Valid when: Valid for finite Hermitian matrices after normalization by the positive diagonal.

## Attempted Derivation

- Start with regulated OS positivity: Q_{a,L}(T_\delta F,c)\ge0 for Wilson collars separated from the reflection plane.
- Use RG convergence valid for reflected collar probes to pass a,L to the continuum at fixed \delta; the finite matrix N^\delta is positive.
- Let \delta\downarrow0. Diagonal trace continuity gives finite diagonal limits; any positive additive contact matrix with zero diagonal vanishes by Cauchy-Schwarz, so only multiplicative boundary anomaly B remains.
- The boundary OPE relation is \widehat N=\widehat B\circ\widehat M, hence the intended same-theory target is positive exactly when q=\widehat N\oslash\widehat B is positive on every realized finite Wilson family.
- Pairwise damping r_{ij}\le1 proves only the 2 by 2 principal minors. The 3 by 3 determinant adds the holonomy term \cos\Phi and gives the first genuine falsifier.
- If all quotient phases are coboundaries, remove them by a diagonal unitary. If d=-\log r is CND, Schoenberg gives r=e^{-d}\ge0 for every finite block, hence all higher principal minors are controlled at once.

Blocking gap: No present Yang-Mills multiscale estimate identifies the boundary Wilson OPE quotient modulus as a CND kernel, nor computes the quotient holonomy for reflected hairpin triples.

## Falsifiers

- A realized three-hairpin Wilson triple with r_{ij}\le1 but 1-r_{12}^2-r_{23}^2-r_{13}^2+2r_{12}r_{23}r_{13}\cos\Phi<0 is an explicit same-theory falsifier.
- A boundary OPE with nonzero quotient cycle holonomy that cannot be removed by diagonal unitary congruence can make the Schur preimage indefinite.
- A finite family with B_{ij}=0 but N_{ij}\ne0 shows the multiplicative trace model is not a valid interface for the intended continuum matrix.
- A quotient modulus d=-\log|q| with a detected CND violation plus a negative principal minor falsifies the proposed CND promotion route.
- If collar collapse requires adding a boundary Wilson algebra or changing Wilson-loop renormalization labels, positivity may hold but not for the same theory.

## Learning

Cycle 206 replaces pairwise damping with a sharper all-minors route. The exact same-theory condition after collar positivity is q=\widehat N\oslash\widehat B\ge0 on realized Wilson blocks. Triangle holonomy is the first falsifier, while a coboundary phase plus CND logarithmic modulus is a valid sufficient certificate for every finite block by Schoenberg. The hard Yang-Mills task is now a boundary OPE computation of holonomy and conditional negative type, not another abstract closed-cone argument.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading boundary OPE for three and four small reflected rectangular Wilson hairpins sharing a footprint; extract q, test the triangle holonomy, and check the CND inequality \sum\bar z_i z_j[-\log|q_{ij}|]\le0 for \sum z_i=0.
