# cycle-0225

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a locked finite Wilson collar block, same-theory OS positivity after boundary-factor removal is governed near the rank-one vacuum matrix by PHP on 1^perp and, on its null space, by the Schur-corrected second boundary OPE coefficient.

## Definitions

- source object: finite reflected Wilson collar OS matrices N_delta with cutoff limits already valid by closed-cone positivity.
- target object: normalized same-theory OS block q_delta whose PSD property is the continuum OS positivity test for the locked Wilson observables.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions through finite reflected quadratic forms and collar collapse.
- same-theory condition: boundary factors may be removed only by diagonal congruence already present in the locked Wilson normalization; no boundary algebra or counterterm is added.

## Assumptions

- A fixed finite Wilson family has normalized quotient q_delta with Hermitian uniform expansion through order eps^2, eps=delta^alpha.
- Additive boundary contacts vanish after diagonal trace continuity; remaining anomaly is multiplicative with nonzero entries.
- P is the orthogonal projection onto 1^perp and e=n^{-1/2}1; q_delta is the realized target block, not an arbitrary Schur multiplier cone.

## Equations

- normalized quotient expansion: `q_\delta=\widehat N_\delta\oslash\widehat B_\delta=11^*+\varepsilon H+\varepsilon^2K+o(\varepsilon^2)`. Valid when: The boundary Wilson OPE is uniform for the finite reflected collar block and all normalized entries are defined.
- first tangent gate: `q_\delta\ge0\ \forall\delta\downarrow0\quad\Longrightarrow\quad PHP\ge0\text{ on }1^\perp`. Valid when: The expansion above is valid and the rank-one term 11^* is the vacuum OS direction.
- second tangent gate: `z^*\left(PKP-n^{-1}PHee^*HP\right)z\ge0\quad(z\in\ker PHP)`. Valid when: q_delta is PSD for small delta; this is the Schur complement of the large rank-one direction.

## Attempted Derivation

- Use fixed-collar RG convergence to pass regulated reflection positivity to a collar-limit matrix N_delta>=0 for the locked Wilson block.
- Separate harmless diagonal Wilson normalizations and multiplicative boundary Gram factors; after normalization the intended same-theory block is q_delta=Nhat_delta oslash Bhat_delta.
- Decompose C^n=Ce oplus 1^perp. The Schur complement of the Ce block gives eps PHP + eps^2(PKP-n^{-1}PHee^*HP)+o(eps^2).
- PSD of q_delta forces PHP>=0; if PHP has null vectors, the eps^2 Schur-complement form must be nonnegative on ker(PHP).

Blocking gap: Yang-Mills analysis has not supplied a uniform reflected Wilson boundary OPE giving H,K and the o(eps^2) remainder for coincident hairpin footprints.

## Falsifiers

- First-order falsifier: compute a reflected Wilson hairpin block with z^*PHPz<0 for some z in 1^perp.
- Second-order falsifier: PHP>=0 but z^*(PKP-n^{-1}PHee^*HP)z<0 on ker(PHP).
- Expansion falsifier: cusp logarithms or perimeter terms make the remainder nonuniform, so the tangent test is not valid for cutoff removal.
- Same-theory falsifier: collar collapse needs a boundary counterterm or enlarged Wilson algebra before q_delta becomes PSD.

## Learning

Cycle 225 converts the Wilson obstruction into a valid normalization-safe tangent-cone bridge. The rank-one OS vacuum direction forces the correction -n^{-1}PHee^*HP, so PKP alone is not the right test. Pure one-body renormalizations cancel; a negative corrected form is a genuine mixed boundary falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the boundary OPE for a three- or four-hairpin reflected Wilson block, extract H,K, and test PHP and the Schur-corrected K-form on 1^perp.
