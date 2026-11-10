# Ten cohere-fast YM inference cycles

Claim ceiling: candidate

Final disposition: conditional route retained; proof promotion blocked

## Cycle 01: Fixed-rank recovery obstruction

**Question.** Can the three-channel alpha=1,p=1 carrier ever establish observable density?

**Result.** No, conditionally on coherent Hilbert-norm recovery and a physical sector of dimension greater than three. Its limit span is closed and has rank at most three.

**Warrant.** A span of at most three recovered limits is finite-dimensional and closed.

**Falsifiers.**

- The alleged physical sector has dimension at most three.
- The recovery maps do not converge coherently, which instead fails the recovery gate.

**Next obligation.** Let inclusion degree p grow without bound.

Status: `conditional_obstruction`

## Cycle 02: Diagonal carrier-growth lemma

**Question.** Can fixed-p recovery estimates be assembled into one p(n) tending to infinity?

**Result.** Yes conditionally. If approximation error A(p) tends to zero and recovery error R(p,n) tends to zero for each fixed p, a nondecreasing diagonal schedule p(n) can be chosen so A(p(n))+R(p(n),n) tends to zero.

**Warrant.** Choose N_p so R(p,n)<=1/p for n>=N_p, make N_p increasing, and set p(n) to the largest p with N_p<=n.

**Falsifiers.**

- A(p) does not tend to zero.
- For some fixed p, recovery error fails to vanish with cutoff removal.

**Next obligation.** Control Gram conditioning and all other errors on the same diagonal schedule.

Status: `conditional_lemma`

## Cycle 03: Gram-rank stability gate

**Question.** When does increasing p preserve the intended OS quotient rather than amplify null directions?

**Result.** For fixed p, rank is stable if the exact limiting Gram matrix has smallest retained eigenvalue gamma_p>0 and the matrix error is eventually below gamma_p/2. Along p(n), the ratio ||Delta G||/gamma_p must still tend to zero.

**Warrant.** Weyl eigenvalue bounds prevent a perturbation smaller than gamma_p/2 from crossing zero.

**Falsifiers.**

- gamma_p collapses faster than Gram errors.
- Whitening factors diverge and conceal vanishing raw OS norm.

**Next obligation.** Record raw eigenvalue intervals and couple p-growth to a conditioning budget.

Status: `candidate_gate`

## Cycle 04: Recovery residual to density

**Question.** What does the Schur recovery residual actually prove?

**Result.** Vanishing normalized residuals for every member of a separately dense target dictionary imply density of the carrier union in the dictionary closure. Residuals for two Wilson loops alone do not imply Hilbert-space density.

**Warrant.** The Schur complement is the squared OS distance to the carrier projection; density follows only after quantifying over a dense target family.

**Falsifiers.**

- The target dictionary is not independently dense.
- Residual convergence is only pointwise with no diagonal schedule.

**Next obligation.** Predeclare a countable Wilson-net target dictionary and its density theorem.

Status: `conditional_bridge`

## Cycle 05: Visible Ritz bound polarity

**Question.** Can finite generalized eigenvalues certify the physical transfer gap?

**Result.** Not alone. A trial carrier gives a lower bound on the full transfer Rayleigh supremum, so it can falsify a proposed upper bound. Gap promotion needs an upper bound including the carrier complement and off-diagonal leakage.

**Warrant.** A supremum over a subspace cannot exceed the supremum over the full physical sector.

**Falsifiers.**

- A computed trial value exceeds exp(-m*tau), refuting the proposed mass floor m.
- Complement or leakage estimates remain uncontrolled.

**Next obligation.** Bound the complement transfer norm and carrier-complement coupling.

Status: `polarity_correction`

## Cycle 06: Transfer complement obstruction

**Question.** What finite-data inequality would suffice for a full transfer upper bound?

**Result.** With physical-sector decomposition W plus W-perp, bounds q_W, q_C, and b on the two diagonal transfer blocks and off-diagonal block imply an operator upper bound given by the largest eigenvalue of [[q_W,b],[b,q_C]].

**Warrant.** The quadratic form is dominated by the corresponding two-by-two scalar majorant; its largest eigenvalue bounds the full contraction.

**Falsifiers.**

- No q_C<1 is available on the complement.
- Leakage b does not vanish or remain below the reserved margin.

**Next obligation.** Produce a noncircular complement estimate; density alone at finite p is insufficient.

Status: `conditional_operator_bound`

## Cycle 07: OS closed-cone versus semigroup convergence

**Question.** Does convergence of reflection-positive Gram matrices construct the continuum Hamiltonian?

**Result.** No. Entrywise convergence of every recovered finite reflection matrix preserves OS nonnegativity, but Hamiltonian transfer also requires a consistent strongly continuous time-translation semigroup and convergence across physical times.

**Warrant.** Closedness of the PSD cone preserves positivity but supplies no semigroup law or generator convergence.

**Falsifiers.**

- Positive-time matrices are mutually inconsistent.
- The limiting translations lack strong continuity or the semigroup composition law.

**Next obligation.** Add multi-time correlation consistency and semigroup convergence to the recovery packet.

Status: `boundary_separation`

## Cycle 08: Nontriviality witness separation

**Question.** Which witnesses prevent a vacuous or Gaussian limit?

**Result.** A nonzero recovered OS norm prevents the carrier from vanishing. A surviving connected higher cumulant is a stronger non-Gaussian witness. Neither proves density, OS reconstruction, or a positive gap.

**Warrant.** These witnesses answer different logical questions and cannot substitute for one another.

**Falsifiers.**

- All centered recovered norms vanish.
- The connected witness survives only after a proxy normalization or theory change.

**Next obligation.** Track norm survival and interaction witnesses as separate fields through the same trajectory.

Status: `obligation_factorization`

## Cycle 09: Geometric alpha versus algebraic p

**Question.** Which refinement variable can plausibly support density?

**Result.** At alpha=1 in the candidate radius model, the number of lattice cells per shape stays bounded, making the pilot a UV-proxy falsifier. Values 0<alpha<1 permit growing shapes, but only explicit p-inclusion supplies the monotone density axis.

**Warrant.** Geometric scale and algebraic closure are independent controls and must not be conflated.

**Falsifiers.**

- Changing alpha also changes the action, normalization, or recovery convention.
- Growing geometric radius fails to enlarge the OS carrier after quotienting.

**Next obligation.** Predeclare an alpha family and a separate degree-growth law p(n).

Status: `route_refinement`

## Cycle 10: Consolidated YM route decision

**Question.** After ten bounded cycles, what remains viable and what is blocked?

**Result.** Retain the two-axis alpha/p spectral-carrier route as a conditional research programme. The fixed-rank pilot is demoted to falsification. Proof promotion is blocked until actual same-theory SU(3) matrices, unbounded p-density, Gram stability, complement transfer control, OS semigroup convergence, and uniform cutoff/volume limits are supplied.

**Warrant.** Every finite or conceptual shortcut encountered has a named countermodel or missing transfer gate.

**Falsifiers.**

- The required data cannot be produced without changing theory.
- The mass floor collapses under p, volume, or cutoff refinement.
- The recovered carrier is null, nondense, or limit-order dependent.

**Next obligation.** Produce the first actual alpha=1 Gram/recovery table and, independently, a quantitative p(n) error schedule; otherwise keep the route quarantined.

Status: `conditional_route_retained_proof_blocked`
