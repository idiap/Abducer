# H9 temporal-density stream report

## Status and corrected interpretation

H9 remains a downstream spectral bridge, not a completed Yang--Mills gap argument. The decisive finite warning is already clear: an incomplete temporal observable core can report decay rate (1.2) while the true lowest nonzero spectral rate is (0.4). This is not merely numerical looseness. It is a structural failure of observability. If the chosen operators do not create vectors with nonzero projection onto the lowest excited spectral subspace, their connected correlations omit that subspace and decay according to a higher spectral threshold.

The correct conclusion is therefore one-sided. Fast decay on a restricted core can certify the absence of slow modes visible to that core, but cannot exclude slower physical modes orthogonal to it. Equivalently, minimizing a Hamiltonian Rayleigh quotient over an incomplete trial space can only overestimate the gap. H9 should be treated as a requirement on the completeness of the temporal probes before their decay rate is promoted to a statement about the spectrum.

## Required observable core

Let OS reconstruction produce a physical Hilbert space (mathcal H_{mathrm{phys}}), vacuum (Omega), positive-time semigroup (T(t)=e^{-tH}), and vacuum-orthogonal space (mathcal H_0=Omega^perp). A candidate gauge-invariant temporal core (mathfrak A_{mathrm{temp}}) is adequate only if

\[
  \mathcal D_0=
  \operatorname{span}\{(A-\langle\Omega,A\Omega\rangle)\Omega:
  A\in\mathfrak A_{\mathrm{temp}}\}
\]

is dense in (mathcal H_0). The associated matrix elements must also be state-separating: no nonzero physical state or nonzero spectral sector may be annihilated by every probe in the core. Density is the operational condition needed to approximate arbitrary excited vectors; separation makes explicit the failure mode exhibited by the (1.2) versus (0.4) example.

Neither a large finite list of Wilson-loop-like observables nor closure under a convenient blocking algebra establishes this condition by itself. The proof must occur in the reconstructed physical norm, including quotienting by OS null vectors. Algebraic density before reconstruction, pointwise convergence of expectations, or separation of classical configurations is insufficient.

## Uniform decay in physical time

The needed decay estimate must be stated in physical time and with a norm that survives closure. A useful target is a constant (m>0) and a seminorm (N) on the core such that, for centered (A,B),

\[
  |\langle A\Omega,T(t)B\Omega\rangle|
  \le N(A)N(B)e^{-mt},\qquad t\ge0.
\]

At regulated level, the rate and comparison constants must be uniform in cutoff, volume, boundary data, and every retained history admitted by the construction. A bound per transfer step is not enough: the number of steps per unit physical time changes with the cutoff, so a positive lattice-step rate can collapse after rescaling. Short-time errors, normalization errors, and finite-volume remainders must likewise be controlled uniformly or shown to vanish in the continuum limit.

The seminorm cannot be an arbitrary stronger topology unrelated to (mathcal H_{mathrm{phys}}). There must be a closure argument that turns core estimates into the operator bound

\[
  \|T(t)|_{\mathcal H_0}\|\le e^{-mt}.
\]

Once that bound is justified, the spectral theorem gives (operatorname{spec}(H)\cap(0,m)=\varnothing). Without the density-and-extension step, the estimate applies only to the core-visible spectral measure and leaves the true gap undetermined.

## OS continuum and theory identity

The final bridge has two logically distinct parts. First, the limiting Euclidean correlations must satisfy the hypotheses needed for OS reconstruction, and the regulated temporal observables and transfer evolutions must converge to the reconstructed vectors and semigroup. Second, the resulting OS theory must be identified with the intended continuum Yang--Mills theory, with the correct gauge-invariant observable algebra, vacuum sector, physical time normalization, and Hamiltonian.

This identity requirement blocks a common substitution: proving a gap for an auxiliary reconstructed theory, a restricted sector, or a subsequential limit does not establish the Yang--Mills mass gap. Uniqueness or an equally strong identification theorem is required if different regulator-removal sequences could yield inequivalent reconstructed dynamics.

## Decisive next theorem

The next target should be a **Dense-Core Uniform-Decay Transfer Theorem**. Under explicit OS reconstruction and theory-identity hypotheses, it should assume: (i) convergence of regulated centered temporal observables into a state-separating core; (ii) density of their generated vectors in (mathcal H_0); (iii) a cutoff-, volume-, history-, and boundary-uniform connected-correlation estimate with rate (m>0) measured in physical time; and (iv) a norm-compatible extension bound. It should conclude that the reconstructed Yang--Mills semigroup contracts by (e^{-mt}) on (mathcal H_0), hence that its Hamiltonian has spectral gap at least (m).

The theorem should include a converse diagnostic: if density is absent, the same hypotheses imply only a gap for the closed core-generated subspace. That clause formally captures the H9 counterexample and prevents accidental promotion of a restricted spectral threshold.

## Claim guardrails

At C2, one may prove the abstract conditional theorem and a regulated-to-continuum transfer conditional on OS existence, density, uniformity, and theory identity. One may also report a restricted-sector gap when the invariant subspace is named precisely. One must not call core decay alone the physical Yang--Mills mass gap.

At C3, the obligations are cumulative: construct the continuum theory; verify the OS hypotheses; identify the reconstruction with Yang--Mills; prove the temporal core dense and state-separating in the physical Hilbert space; establish uniform positive decay in physical time; and extend it to all of (mathcal H_0). Missing any one of these steps lowers the claim. The immediate H9 status therefore remains C1 evidence supporting an abstract conditional C3 route, with the next publishable advance properly framed at C2.
