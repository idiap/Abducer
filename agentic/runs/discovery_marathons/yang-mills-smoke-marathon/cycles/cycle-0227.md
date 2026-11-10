# cycle-0227

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Third-order tangent-cone bridge for locked Wilson collar quotients. For a finite Wilson hairpin block with normalized Schur-preimage q_eta=J+eta H+eta^2 K+eta^3 L+o(eta^3), OS positivity of the intended same-theory matrix forces a vacuum Feshbach hierarchy: A>=0 on 1^perp, then the corrected B is >=0 on ker A, then the corrected C-B A^dagger B is >=0 on the null of that B. Any negative form at the first failing level is a finite Wilson falsifier.

## Definitions

- source object: regulated reflection-positive collar Wilson/local Schwinger matrices N_eta together with boundary anomaly matrices B_eta for a fixed locked gauge-invariant finite family.
- target object: OS-positive continuum Schwinger functions on the same locked gauge-invariant Wilson/local test algebra.
- controlled interface: normalized Schur-preimage q_eta=\widehat N_eta\oslash\widehat B_eta, projected off the vacuum vector e=n^{-1/2}(1,...,1).
- same-theory condition: collar collapse identifies the same renormalized Wilson/local observables; diagonal congruences already in the locked normalization are allowed, but no boundary counterterm, quotient algebra change, or extra boundary state is allowed.
- J=11^*=n ee^*, P=I-ee^*, eta is the collar scale or first valid asymptotic scale.

## Assumptions

- For every eta>0 before collapse the regulated/collar OS matrix is positive and the Schur-preimage q_eta is the intended same-theory target matrix.
- q_eta is Hermitian and admits a uniform expansion q_eta=J+eta H+eta^2 K+eta^3 L+o(eta^3) on the finite block.
- The vacuum block e^*q_eta e remains positive for small eta.
- A=PHP has closed range in the finite-dimensional block; A^dagger is its Moore-Penrose inverse on P-space.

## Equations

- Schur-preimage interface: `q_\eta=\widehat N_\eta\oslash \widehat B_\eta,\qquad (q_\eta)_{ii}=1`. Valid when: The boundary anomaly is multiplicative on the finite Wilson block after additive positive contacts have been eliminated and diagonal normalizations are locked.
- vacuum Feshbach reduction: `R_\eta=Pq_\eta P-Pq_\eta e\,(e^*q_\eta e)^{-1}e^*q_\eta P`. Valid when: e^*q_eta e>0; then q_eta>=0 is equivalent to R_eta>=0 by the Schur complement.
- first three reduced coefficients: `R_\eta=\eta A+\eta^2 B+\eta^3 C+o(\eta^3)`. Valid when: The expansion of q_eta is uniform through order eta^3.
- coefficients: `A=PHP,\quad B=PKP-n^{-1}PHee^*HP`. Valid when: J=nee^* is the rank-one vacuum matrix and e is unit normalized.
- third coefficient: `C=PLP-n^{-1}(PHee^*KP+PKee^*HP)+n^{-2}(e^*He)PHee^*HP`. Valid when: H,K,L are Hermitian coefficient matrices in q_eta=J+eta H+eta^2K+eta^3L+o(eta^3).
- third-order null test: `\Omega\left(\Pi C\Pi-\Pi B A^\dagger B\Pi\right)\Omega\ge0`. Valid when: A>=0, Pi projects onto ker A, Pi B Pi>=0, and Omega projects onto ker(Pi B Pi).

## Attempted Derivation

- Start with the exact finite same-theory criterion q_eta=\widehat N_eta\oslash\widehat B_eta>=0 for each locked Wilson block after additive contacts are removed.
- Normalize the common boundary footprint so q_eta tends to J=11^*=nee^* as the collar collapses.
- Decompose the matrix into the vacuum direction e and P=I-ee^*. Since e^*q_eta e=n+O(eta)>0, apply the Schur complement.
- Expand the Schur complement R_eta. The eta^2 coefficient is not PKP alone; the rank-one vacuum direction subtracts n^{-1}PHee^*HP, recovering the cycle-226 correction.
- Keep one more order. The eta^3 coefficient acquires two mixed vacuum terms and one scalar inverse term: C=PLP-n^{-1}(PHee^*KP+PKee^*HP)+n^{-2}(e^*He)PHee^*HP.
- Now reduce R_eta first by the positive range of A=PHP. If A has kernel Pi, positivity forces Pi B Pi>=0. If Pi B Pi has null space Omega, the next necessary test is Omega(Pi C Pi-Pi B A^dagger B Pi)Omega>=0.
- This shows cycle 226 was the correct second-order gate but not the final null-direction gate; a third-order Wilson boundary OPE can be the first valid falsifier.

Blocking gap: No Yang-Mills estimate yet supplies H,K,L with a uniform collar remainder for reflected Wilson hairpin products in the locked algebra.

## Falsifiers

- First-order falsifier: there exists x in 1^perp with x^*PHPx<0 for a realized reflected Wilson block.
- Second-order falsifier: PHP>=0 but some y in ker(PHP) has y^*(PKP-n^{-1}PHee^*HP)y<0.
- Third-order falsifier: the first two gates pass but some z in ker(Pi B Pi) has z^*(Pi C Pi-Pi B A^dagger B Pi)z<0.
- Topology falsifier: RG convergence is too weak to produce a valid uniform expansion for q_eta on reflected Wilson collar products.
- Same-theory falsifier: the expansion becomes positive only after adding a boundary counterterm or changing Wilson-loop renormalization at the reflection plane.

## Learning

Cycle 227 adds the next valid obstruction after the second-order correction. Once the vacuum rank-one direction is removed, null directions of PHP require a genuine Feshbach hierarchy: the third-order test contains -Pi B A^dagger B Pi from coupling to the positive first-order sector. Thus PKP and PLP alone are not reliable Wilson falsifier tests. A positive first-order reduced kernel promotes a finite block immediately, while any negative reduced coefficient at the first nonzero Feshbach level is a normalization-safe mixed boundary falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading H,K,L boundary OPE coefficients for a three- or four-hairpin reflected Wilson block with common footprint, then evaluate PHP, Pi B Pi, and Pi C Pi-Pi B A^dagger B Pi for an explicit zero-sum vector.
