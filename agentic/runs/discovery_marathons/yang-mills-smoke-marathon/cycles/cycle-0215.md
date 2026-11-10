# cycle-0215

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

If a locked finite Wilson hairpin block has normalized same-theory quotient q_delta=Nh_delta\oslash Bh_delta=J+eps_delta H+o(eps_delta), then OS positivity forces H>=0 on 1^perp. A negative zero-sum form is a finite falsifier before any log-CND claim.

## Definitions

- source object: finite collar-separated gauge-invariant Wilson observables W_i^delta with reflected OS matrices N_delta>=0 and boundary anomaly matrices B_delta from collar collapse.
- target object: normalized intended continuum OS matrix q for the same Wilson observables after removing only prelocked diagonal renormalizations.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions via q_delta=Nh_delta\oslash Bh_delta on each finite locked Wilson block.
- same-theory condition: B_delta records only collision artifacts; no new boundary observable, counterterm, or pair-dependent renormalization is inserted into the test algebra.

## Assumptions

- Fixed-collar RG convergence is valid for all reflected pairings in the finite Wilson family.
- Diagonal trace continuity and positive additive-contact compatibility eliminate additive boundary defects.
- Bh_delta has nonzero entries, q_delta is Hermitian, and q_delta,ii=1.
- There are eps_delta down to 0 and Hermitian H with q_delta=J+eps_delta H+r_delta and ||r_delta||/eps_delta ->0.

## Equations

- Schur preimage block: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta`. Valid when: The only remaining collar-collapse mismatch is a multiplicative boundary anomaly B_delta and hats denote diagonal normalization.
- tangent quotient expansion: `q_\delta=J+\varepsilon_\delta H+r_\delta,\qquad \|r_\delta\|=o(\varepsilon_\delta)`. Valid when: The boundary OPE has a valid first-order quotient coefficient H with uniform finite-block remainder.
- zero-sum OS test: `{\bf 1}^*z=0\Rightarrow z^*q_\delta z=\varepsilon_\delta z^*Hz+o(\varepsilon_\delta)\ge0`. Valid when: q_delta is an OS-positive intended block for all small delta.

## Attempted Derivation

- Start from fixed-collar reflection positivity: N_delta>=0. After diagonal trace continuity removes additive contacts, the intended normalized target block is q_delta=Nh_delta\oslash Bh_delta.
- On 1^perp, J contributes nothing since z^*Jz=|sum_i z_i|^2=0; hence first-order positivity is controlled only by H.
- If q_delta is positive for the same theory and r_delta=o(eps_delta), then 0<=z^*q_delta z=eps_delta z^*Hz+o(eps_delta); dividing and limiting gives z^*Hz>=0.
- Contrapositively, a negative zero-sum H-form yields a negative principal OS quadratic form for small collars, so it is a valid finite falsifier.

Blocking gap: No Yang-Mills estimate yet gives the Wilson hairpin quotient expansion with a uniform o(eps_delta) remainder and a correctly isolated B_delta.

## Falsifiers

- falsifier: a boundary OPE computation gives z^*Hz<0 for some zero-sum coefficients in a three- or four-hairpin Wilson block.
- falsifier: q_delta is not Hermitian after quotienting, so B_delta is not the valid same-theory anomaly or reflection was mismatched.
- falsifier: additive boundary contacts have nonzero off-diagonal part despite zero diagonal, violating positive contact compatibility.
- falsifier: RG convergence controls separated collars but gives no uniform o(eps_delta) remainder as supports approach t=0.

## Learning

Cycle 215 isolates the first-order OS obstruction cleanly: near the rank-one quotient J, positivity lives on 1^perp. The valid finite test is H>=0 there; a negative zero-sum boundary OPE coefficient is an immediate same-theory falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading boundary OPE quotient kernel H for three mirror-smooth reflected Wilson hairpins with common footprint and test zero-sum vectors such as (1,-1,0) and (1,1,-2).
