# cycle-0211

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For each finite locked Wilson collar family, after diagonal normalization and removal of additive contacts, same-theory OS positivity is equivalent to PSD of \(\widehat Q=\widehat N\oslash\widehat B\). If \(Q_t\) is a valid Hadamard semigroup, log-CND is a sufficient all-minors certificate.

## Definitions

- source object: finite reflected Wilson collar OS matrices \(N_\delta=(S_\delta(\Theta F_i^\delta,F_j^\delta))\) with \(N_\delta\ge0\).
- target object: continuum OS matrices \(M=(S(\Theta F_i,F_j))\) on the locked gauge-invariant Wilson/local algebra.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via the quotient \(M=N\oslash B\).
- same-theory condition: collar removal uses the predeclared Wilson renormalization and embeddings; no boundary counterterm, algebra enlargement, or pair-dependent redefinition is allowed.

## Assumptions

- Fixed-collar RG convergence is valid for every reflected finite Wilson block.
- The boundary OPE gives an entrywise nonzero multiplicative factor \(B\) after diagonal normalization.
- Additive contacts vanish, e.g. positivity plus zero diagonal, or are already included in the locked target.
- The realized Wilson core is closed under the finite collar probes used in the quotient test.

## Equations

- boundary quotient factorization: `\widehat N_{ij}=\widehat B_{ij}\widehat M_{ij},\qquad \widehat M=\widehat N\oslash\widehat B`. Valid when: The boundary anomaly is purely multiplicative, entries of \(\widehat B\) are nonzero, and additive contacts have been eliminated.
- exact finite OS test: `\widehat M\ge0\Longleftrightarrow \sum_{i,j}\overline c_i c_j\,{\widehat N_{ij}\over \widehat B_{ij}}\ge0\quad\forall c`. Valid when: The finite Wilson family belongs to the locked same-theory test algebra; this is the exact valid criterion, not a heuristic.
- semigroup certificate: `q_t=e^{-t h},\ q_{s+t}=q_s\circ q_t,\ q_t\ge0\ \forall t\ge0\Longleftrightarrow \sum_{i,j}\overline z_i z_j h_{ij}\le0\ (\sum_i z_i=0)`. Valid when: Only for a continuous normalized Hermitian Hadamard semigroup; it is not valid evidence from one quotient matrix alone.

## Attempted Derivation

- Fixed-collar reflection positivity and RG convergence give a PSD collar-limit matrix \(\widehat N\) by the closed-cone argument.
- Boundary OPE analysis is inserted only at collar collapse: if it is multiplicative, \(\widehat N=\widehat B\circ\widehat M\), so the intended target is \(\widehat M=\widehat N\oslash\widehat B\).
- Therefore same-theory OS positivity is exactly finite PSD of the quotient on realized Wilson blocks; pairwise damping is necessary but not sufficient.
- If collar quotients form a continuous Hadamard semigroup, Schoenberg converts the all-minors test to log-CND; without that structure, determinants remain the valid tests.

Blocking gap: Hadamard-semigroup and boundary-OPE factorization gap: Yang-Mills estimates do not yet prove multiplicative nonzero \(B\), vanishing additive contacts, or infinite divisibility of the quotient.

## Falsifiers

- falsifier: a realized three-hairpin Wilson block has \(\det(\widehat N\oslash\widehat B)<0\) although every 2-by-2 quotient minor is nonnegative.
- falsifier: the boundary OPE contains a nonpositive additive contact with zero diagonal, so the entrywise multiplicative quotient model is invalid.
- falsifier: collar quotients fail \(q_{s+t}=q_s\circ q_t\); then log-CND is not a valid certificate, only direct finite minors remain.
- falsifier: reflection-plane removal forces a new cusp or boundary counterterm outside the locked gauge-invariant algebra, violating same-theory.

## Learning

Cycle 211 separates the exact bridge from a tempting overclaim: OS positivity after Wilson collar collapse is finite PSD of \(\widehat N\oslash\widehat B\). Log-CND is useful only if a valid Hadamard semigroup is proved. The next real work is boundary OPE computation, not topology naming.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE for three reflected Wilson hairpins with common footprint; extract \(\widehat B\), form \(\widehat N\oslash\widehat B\), and test the 3-by-3 determinant before invoking any semigroup certificate.
