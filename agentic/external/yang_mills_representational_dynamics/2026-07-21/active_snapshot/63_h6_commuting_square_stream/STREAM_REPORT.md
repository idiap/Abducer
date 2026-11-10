# H6 stream report: commuting-square defects across blocking

## Outcome

H6 survives as an exact diagnostic and yields a useful abstract transport
theorem, but not yet a Yang--Mills estimate.  The word *curvature* should be
reserved for the following typed defect, rather than inferred from mere path
dependence.

At scale `k`, let `X_k` and `Y_k` be normed representation spaces, let

`B_k : X_k -> X_{k+1}`, `T_k : Y_k -> Y_{k+1}`

be the two blocking descriptions, and let `R_k : X_k -> Y_k` be the
representation change.  Define the square defect

`Omega_k = T_k R_k - R_{k+1} B_k : X_k -> Y_{k+1}`.

This typing is essential: centering, orientation, gauge descent, blocking,
and reconstruction generally have different domains and cannot be permuted
as unlabeled matrices.

## Exact H6 calibration

For one six-plaquette star, put

`C = I - 11^T/6`, `O = diag(s)`, `s=(-1,-1,-1,1,1,1)^T`.

Then

`[C,O] = CO-OC = (s1^T-1s^T)/6`.

Because `1/sqrt(6)` and `s/sqrt(6)` are orthonormal, this commutator has
exact rank two and operator norm one.  Thus orient-then-center and
center-then-orient are maximally different on their two-dimensional active
plane.  The Stage 52 numerical covariance spectra were

- raw-centered: approximately `0, 239/630 (x2), 33/70 (x2), 1`;
- orientation-correct: `0, 239/630 (x2), 33/70 (x3)`.

The second spectrum is the exact Paper 05 result.  The first path creates the
previously documented spurious zero-spill conclusion.  This proves an order
defect in a finite linear representation.  It does **not** prove a geometric
connection, a gauge-field curvature theorem, or an RG obstruction.

## The transport theorem H6 actually needs

Write `B_{b:a}=B_{b-1}...B_a` and similarly for `T`, with an empty product
equal to the identity.

**Theorem (typed square-defect transport).** For every `n>=1`,

`T_{n:0} R_0 - R_n B_{n:0}`

`= sum_{j=0}^{n-1} T_{n:j+1} Omega_j B_{j:0}`.

Consequently,

`||T_{n:0} R_0 - R_n B_{n:0}||`

`<= sum_j ||T_{n:j+1}|| ||Omega_j|| ||B_{j:0}||`.             (H6.1)

The identity follows by adding and subtracting the intermediate paths; the
sum telescopes.  The norm bound is the triangle inequality and
submultiplicativity.  It is sharp already for aligned one-dimensional maps.

Recovery must be included explicitly.  If `S_n:Y_n->X_n` is a recovery map,
then

`S_n T_{n:0}R_0-B_{n:0}`

`= (S_nR_n-I)B_{n:0}`

`  + sum_j S_n T_{n:j+1} Omega_j B_{j:0}`,

and hence

`||S_n T_{n:0}R_0-B_{n:0}||_phys`

`<= eta_n ||B_{n:0}||_phys`

`  + sum_j K_{n,j+1} epsilon_j ||B_{j:0}||_phys`,             (H6.2)

where `eta_n` bounds `S_nR_n-I` on the reachable physical subspace,
`epsilon_j=||Omega_j||` on that subspace, and
`K_{n,j+1}=||S_nT_{n:j+1}||` in the declared physical seminorm.  Equation
(H6.2) is the exact next inequality for safe transport across repeated
blocking.

A usable uniform corollary follows if prefix products are bounded by `M`,
`eta_n -> 0`, and either

1. `sum_j sup_{n>j} K_{n,j+1} epsilon_j < infinity`, or
2. `K_{n,j+1} <= C theta^(n-1-j)` with `theta<1` and `epsilon_j -> 0`.

In the second case the defect convolution tends to zero.  If only
`epsilon_j<=epsilon`, it is bounded by `MC epsilon/(1-theta)` and need not
vanish.  Therefore uniformly small one-step squares are not enough.

For local observables, every norm above must be replaced by a
support-indexed seminorm.  The theorem then also needs a support-growth rule
and summability after that growth.  For positivity or reflection positivity,
a norm estimate is insufficient: every blocking arrow must preserve the
relevant cone, or a separate uniformly bounded positive recovery theorem
must be supplied.  Gauge covariance and topology are likewise independent
certificate channels.

## Counterexamples that fix the hypotheses

1. **Small rotations accumulate.** Take `B_k=I`, `R_k=I`, and let `T_k` be a
   rotation by `delta`.  Every square has norm about `delta`, all map norms
   equal one, yet after `n` of order `pi/delta` the two paths differ by order
   one.  Summability or future contraction is necessary.

2. **A locally invisible defect becomes visible.** In `R^2`, inject a defect
   into `e_2`, while the current physical probe observes only `e_1`.  Its
   local observable error is zero.  Let the next block swap `e_1` and `e_2`;
   the final error is one.  One needs future-aware norms or an invariant blind
   subspace, not scale-local projection alone.

3. **Exact but ill-conditioned recovery magnifies error.** Let
   `R_delta=diag(1,delta)` and `S_delta=diag(1,delta^{-1})`.  Although
   `S_delta R_delta=I`, a defect `delta e_2` tends to zero before recovery and
   becomes `e_2` afterward.  Existence of a recovery map is not uniform
   stability.

4. **Support multiplicity defeats scalar control.** A per-cell defect
   `epsilon` can contribute `N epsilon` to an unnormalized block observable.
   Observable normalization and support dependence must be declared before a
   cutoff or volume limit.

## Yang--Mills handoff and claim audit

The first physical target is one concrete gauge-covariant block map with
typed observable pullbacks for which (H6.2) is uniform in volume, boundary
history, and cutoff in physical units.  It must include common-orientation
conversion before centering, local support propagation, a positive or
reflection-positive recovery channel, and topology/sector bookkeeping.

Current classification:

- exact rank/norm calibration: C2 finite linear algebra;
- telescoping and recovered transport theorem: C2 abstract functional
  analysis;
- applicability to an actual nonlinear `SU(2)` block map: open;
- volume/cutoff-uniform Yang--Mills transport: open;
- continuum existence, OS reconstruction, and mass gap: not reached.

H6 should therefore be used as a regression and interface theorem.  It can
prevent an orientation error from propagating through the programme, but it
cannot replace normalized probability estimates, large-field control, RG
stability, or spectral reconstruction.
