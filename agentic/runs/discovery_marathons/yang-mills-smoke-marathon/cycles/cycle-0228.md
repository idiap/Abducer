# cycle-0228

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite locked Wilson hairpin block whose normalized same-theory quotient q_delta tends to the rank-one vacuum matrix J, OS positivity after collar collapse is equivalent to positivity of an exact vacuum Schur complement. The first negative coefficient in its Feshbach hierarchy is a normalization-safe mixed boundary falsifier; if the first nonzero reduced coefficient is positive with a uniform remainder, the finite block is validly promoted.

## Definitions

- source object: finite regulated reflection-positive Schwinger forms for locked gauge-invariant Wilson collar observables F_{i,\delta}, with continuum collar OS matrices N_\delta and multiplicative boundary Gram matrices B_\delta.
- target object: OS-positive continuum Schwinger functions on the same locked gauge-invariant algebra, equivalently positive finite target matrices M_\delta=B_\delta^{[-1]}\circ N_\delta after diagonal normalization and collar trace.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via finite reflected quadratic forms, Hadamard quotients q_\delta=\widehat N_\delta\oslash\widehat B_\delta, and closed-cone limits.
- same-theory condition: the embeddings of Wilson collar observables into the continuum algebra are fixed before the limit; diagonal one-body renormalizations are allowed only as congruences, while pair-dependent boundary factors must pass q_\delta\ge0.
- Here \widehat X_{ij}=X_{ij}/(X_{ii}X_{jj})^{1/2}, e=n^{-1/2}(1,\ldots,1), P=I-ee^*, and J_{ij}=1=n ee^*_{ij}.
- The vacuum Schur complement removes the rank-one OS vacuum direction before testing mixed boundary OPE data.
- A Feshbach reduced coefficient means the Schur complement onto the null space of the previous leading nonnegative coefficient.

## Assumptions

- Regulated reflection positivity and RG convergence give N_\delta\ge0 for every fixed collar block.
- Diagonal entries are positive and additive boundary contacts have either vanished by diagonal trace continuity or are separated as an earlier obstruction.
- The multiplicative anomaly B_\delta is Hermitian with nonzero entries on the block, so the Hadamard quotient q_\delta is defined.
- For coincident-footprint hairpins there is a uniform boundary OPE expansion q_\delta=J+\eta H+\eta^2K+\eta^3L+O(\eta^4), with \eta=\eta(\delta)\downarrow0.
- The remainder is uniform on the finite block strongly enough that a spectral gap in the first nonzero reduced coefficient dominates it.

## Equations

- same-theory quotient: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta,\qquad \widehat X_{ij}=\frac{X_{ij}}{(X_{ii}X_{jj})^{1/2}}`. Valid when: The boundary defect is multiplicative after diagonal normalization and no additive contact term remains hidden.
- rank-one boundary expansion: `q_\delta=J+\eta H+\eta^2K+\eta^3L+O(\eta^4),\qquad J={\bf 1}{\bf 1}^*=n ee^*`. Valid when: The reflected Wilson collars have a uniform coincident-footprint boundary OPE.
- exact vacuum Schur test: `q_\delta\ge0\Longleftrightarrow e^*q_\delta e>0\ \text{ and }\ T_\delta:=Pq_\delta P-Pq_\delta e\,(e^*q_\delta e)^{-1}e^*q_\delta P\ge0`. Valid when: q_\delta is Hermitian and e^*q_\delta e>0, which holds for small \delta near J.
- first three Schur coefficients: `T_\delta=\eta A+\eta^2B+\eta^3C+O(\eta^4),\quad A=PHP,\quad B=P(K-n^{-1}Hee^*H)P,\quad C=P\{L-n^{-1}(Hee^*K+Kee^*H)+n^{-2}(e^*He)Hee^*H\}P`. Valid when: The OPE expansion is valid through third order and e is the unit constant vector.
- first Feshbach reduction: `\mathcal F_\eta=\Pi\left[(T_\delta/\eta)-(T_\delta/\eta)(1-\Pi)((1-\Pi)(T_\delta/\eta)(1-\Pi))^{-1}(1-\Pi)(T_\delta/\eta)\right]\Pi=\eta\Pi B\Pi+\eta^2\Pi(C-BA^\dagger B)\Pi+O(\eta^3)`. Valid when: A=PHP\ge0, \Pi is projection onto \ker A, and A has a positive spectral gap on (1-\Pi)P\mathbb C^n.

## Attempted Derivation

- Fix a finite locked Wilson collar family F_{1,\delta},...,F_{n,\delta}. Regulated reflection positivity and the closed-cone collar passage give a positive collar matrix N_\delta.
- Separate additive contacts. A positive additive contact with zero diagonal vanishes by Cauchy-Schwarz; an indefinite or nonzero zero-diagonal contact is already a falsifier before quotienting.
- Encode the remaining boundary discrepancy as a multiplicative Gram factor B_\delta. After diagonal normalization, same-theory OS positivity is the finite matrix condition q_\delta=\widehat N_\delta\oslash\widehat B_\delta\ge0.
- For coincident-footprint hairpins, assume the boundary OPE gives q_\delta=J+\eta H+\eta^2K+\eta^3L+O(\eta^4). Pure one-body factors have the form h_i+\overline h_j and disappear from the zero-sum sector after the vacuum Schur step.
- Apply the exact Schur complement along e. This gives T_\delta\ge0 as the exact test and yields A=PHP, B=P(K-n^{-1}Hee^*H)P, and the displayed third coefficient C.
- If A has a negative zero-sum vector, q_\delta is indefinite for small \delta. If A is strictly positive on P\mathbb C^n, q_\delta is positive for small \delta with a uniform remainder.
- If A\ge0 has kernel, take the Feshbach complement onto \ker A. The next coefficient is \Pi B\Pi; if it has a negative vector, this is the second-order mixed Wilson falsifier. On null directions of \Pi B\Pi, the next valid coefficient contains the correction -BA^\dagger B, not merely C.
- Iterating gives a finite hierarchy: the first negative reduced coefficient produces a negative OS quadratic form; the first positive reduced coefficient with a gap promotes that finite block.

Blocking gap: The finite-matrix argument is valid, but Yang-Mills input is missing: a uniform reflected Wilson boundary OPE for q_\delta, identification of B_\delta without changing the locked algebra, and cutoff-removal control of the reflected products through the collar trace.

## Falsifiers

- First-order falsifier: a zero-sum vector c with c^*PHPc<0 for a realized Wilson hairpin block.
- Second-order falsifier: A=PHP\ge0 but some c\in\ker A has c^*P(K-n^{-1}Hee^*H)Pc<0.
- Third-order falsifier: on the reduced null space, c^*\Pi(C-BA^\dagger B)\Pi c<0; this detects mixed boundary OPE coupling to the positive first-order sector.
- Additive-contact falsifier: a boundary contact matrix survives with zero diagonal but nonzero mixed entry, contradicting positive contact compatibility.
- Topology falsifier: the cutoff-removal topology is valid for unreflected Wilson expectations but not for the reflected products defining N_\delta.
- Same-theory falsifier: B_\delta is made positive only by adding a boundary counterterm or changing Wilson-loop renormalization at t=0.

## Learning

Cycle 228 turns the Wilson boundary obstruction into an exact finite-matrix algorithm. The vacuum direction must be removed first by a Schur complement; then PHP, P(K-n^{-1}Hee^*H)P, and higher Feshbach reductions give normalization-safe tests. The valid falsifier is not a raw anomaly or PKP alone, but the first negative reduced coefficient after all rank-one and positive-sector couplings are eliminated. The remaining Yang-Mills work is now concrete: compute the reflected Wilson hairpin boundary OPE with uniform remainders.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE for a minimal three- or four-hairpin Wilson block with common reflection-plane footprint, extract H,K,L, and test PHP, P(K-n^{-1}Hee^*H)P, then C-BA^\dagger B on the reduced null space.
