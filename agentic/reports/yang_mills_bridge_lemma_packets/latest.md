<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Yang-Mills Bridge-Lemma Packets

- Target: `yang-mills-existence-and-mass-gap-target`
- Quality gate: `pass`
- Long-horizon status: `pass`
- Skill coherence status: `pass`

## RG-to-OS Continuum Passage Bridge Lemma

- Packet: `ym-bridge-lemma.878ef6641eb3`
- Source route: `candidate.99d7c53a3321`
- Route family: `Balaban RG continuum-control route`
- Recursive role: turn construction pressure into a same-theory continuum object

### Lemma Statement

For compact simple gauge group G on four-dimensional Euclidean space, suppose a directed family of regulated Yang-Mills measures or Schwinger distributions has Balaban-style multiscale effective-action bounds strong enough to give tightness/convergence on gauge-invariant observables, and suppose reflection positivity, Euclidean covariance, gauge invariance, and a non-Gaussian observable witness are preserved uniformly through cutoff removal. Then a subsequential continuum family of gauge-invariant Schwinger functions S_n exists, is OS-positive, is nontrivial, and reconstructs a candidate physical Hilbert space H_YM with vacuum Omega and time-translation semigroup.

### Objects

**Source objects**
- regulated Yang-Mills measures dmu_{a,L} or Schwinger distributions S_n^{a,L}
- Balaban effective actions and polymer/small-field estimates across scales
- compact simple gauge group G and gauge-invariant observable algebra A_ginv^{a,L}

**Target objects**
- continuum gauge-invariant Schwinger functions S_n on R^4
- OS-positive reconstruction data for H_YM, Omega, and Euclidean time semigroup
- nontrivial observable witness in the same limiting Yang-Mills object

### Definitions And Assumptions

- Definition: Cutoff removal means a -> 0 and L -> infinity along a directed regulated family.
- Definition: OS positivity is reflection positivity for the limiting Schwinger functions after quotienting null vectors.
- Definition: Same-theory invariant means construction, reconstruction, nontriviality, and gap witnesses refer to the same limiting object S_n.
- Assumption: Uniform multiscale bounds imply tightness or distributional precompactness for gauge-invariant Schwinger functions.
- Assumption: Reflection positivity and Euclidean covariance are stable under the limiting topology used.
- Assumption: There exists a gauge-invariant observable O whose connected limiting cumulant does not vanish in the Gaussian/free pattern.

### Equations

- continuum passage: `S_n^{a,L} -> S_n as a -> 0 and L -> infinity`
  - TeX: `S_n^{a,L}\Longrightarrow S_n\quad(a\to0,\ L\to\infty)`
  - Valid when: The regulated Schwinger functions are uniformly controlled in a topology where OS positivity and Euclidean covariance are closed conditions.
- OS positivity preservation: `sum_i,j c_i conjugate(c_j) S(f_i^theta, f_j) >= 0`
  - TeX: `\sum_{i,j}\overline{c_i}c_j\,S(\Theta f_i,f_j)\ge 0`
  - Valid when: Each regulated object is reflection-positive and the test functions/observable algebra survive the limiting quotient.
- nontriviality witness: `<O_1 ... O_k>_c != 0 in the continuum limit`
  - TeX: `\langle O_1\cdots O_k\rangle_c\ne0`
  - Valid when: The observable O_i are gauge-invariant and belong to the same limiting algebra used for reconstruction.

### Proof Obligations

- Name the exact Balaban estimates that yield precompactness rather than only local small-field control.
- Prove the limiting topology preserves OS positivity for the gauge-invariant observable sector.
- Attach one non-Gaussian gauge-invariant observable witness to rule out triviality.
- Record the reconstructed H_YM, Omega, and semigroup as outputs of S_n, not as independent postulates.

### Failure Tests

- Reject if the limit exists only at finite volume or fixed ultraviolet cutoff.
- Reject if OS positivity is asserted for the regulator but not proved closed in the limiting topology.
- Reject if the nontriviality witness comes from a different approximation scheme than S_n.

### Proof By Contradiction Branches

#### OS-positivity-failure reductio

- Branch: `ym-reductio.166efc89f93d`
- Exact negation: There exists a finite reflected test-observable family f_i and coefficients c_i such that the continuum reflection form sum_i,j conjugate(c_i)c_j S(Theta f_i,f_j) is strictly negative.
- Contradiction carrier: a negative reflection-positivity quadratic form in the limiting gauge-invariant Schwinger functions
- Derived consequence: If the negative continuum form exists while all approximating reflection forms are nonnegative and the cone is closed, the limit would both belong and not belong to the OS-positive cone.
- Conflict target: closedness of reflection positivity under the selected cutoff-removal topology
- Audit skill: `contradiction-route-auditor`
- Learning if failed: Failure would show that the continuum route needs a sharper topology or a different construction of the OS-positive sector before spectral reasoning can be trusted.

**Preserved commitments**
- The regulated approximants are reflection-positive in the same gauge-invariant observable sector.
- The limiting topology is strong enough for the reflection form to be a closed nonnegative cone.
- The limiting Schwinger functions are the same objects used for reconstruction and later gap analysis.

**Proof obligations**
- Specify the topology on gauge-invariant Schwinger distributions.
- Prove reflection positivity is closed in that topology for the chosen observable algebra.
- Show the negative test family survives the OS null-vector quotient.

**Failure modes**
- The limiting topology is too weak to preserve the reflection form.
- The test-observable family changes across the cutoff sequence.
- Gauge fixing or quotienting changes the observable sector.
#### Triviality-collapse reductio

- Branch: `ym-reductio.5c647a12c20d`
- Exact negation: Every continuum subsequential limit of the regulated gauge-invariant Yang-Mills observables is Gaussian/free or has vanishing connected cumulants for the nontriviality witness family.
- Contradiction carrier: a connected gauge-invariant cumulant or Wilson-loop observable in the same limiting Schwinger family
- Derived consequence: The assumed trivial collapse forces the selected connected cumulant to vanish, while the same-theory witness requires a nonzero interacting cumulant in that limit.
- Conflict target: same-theory non-Gaussian or nonzero connected-cumulant witness
- Audit skill: `contradiction-route-auditor`
- Learning if failed: Failure would demote the route to a nontriviality-evidence task rather than allowing the gap analysis to proceed on an empty continuum theory.

**Preserved commitments**
- The nontriviality witness is measured in the same limiting Schwinger functions S_n.
- Connected cumulants are defined after the same cutoff-removal process as OS reconstruction.
- Gauge invariance and Euclidean covariance remain active commitments.

**Proof obligations**
- Select the witness observable family and its normalization.
- Prove the witness belongs to the same continuum object as the OS reconstruction.
- Show the witness distinguishes interacting Yang-Mills from a Gaussian/free limit.

**Failure modes**
- The witness comes from a different approximation scheme.
- The cumulant normalization vanishes or diverges in the limit.
- The branch proves only non-Gaussianity at finite cutoff.

### Conditional Skill Triggers

- `prior-art-importer`: Exact Balaban theorem statements must be imported or normalized before promotion.
- `review-reasoner-fields-medalist`: Stress-test whether the proposed limiting topology is mathematically plausible.
- `kb-contradiction-strategist`: Use when OS positivity or nontriviality is better explored through the negated continuum-construction assumption.
- `contradiction-route-auditor`: Audit reductio branches before they are allowed to justify proof-queue promotion.
- `expert-handoff`: Package the bridge once it has theorem names, assumptions, and one observable witness.

### Next Recursive Subgoals

- Search the KB/prior-art cache for the strongest Balaban precompactness or convergence statement.
- Choose the limiting topology and state the closure lemma for reflection positivity.
- Select a candidate gauge-invariant nontriviality observable.

Promotion condition: Promote only when the lemma names the regulated objects, limiting topology, OS-positivity preservation theorem, and nontriviality witness.

Same-theory invariant: The same Schwinger functions S_n are the sole object from which nontriviality, reconstruction, and any later mass-gap witness must be read.

## Cutoff-Uniform Decay-to-Hamiltonian-Gap Bridge Lemma

- Packet: `ym-bridge-lemma.beaf53753faa`
- Source route: `candidate.3e9a722a8615`
- Route family: `Euclidean correlator-decay to spectral-gap route`
- Recursive role: turn a Euclidean decay witness into a Hamiltonian spectral exclusion

### Lemma Statement

Suppose the same OS-positive continuum Yang-Mills Schwinger functions S_n reconstruct H_YM, Omega, H and a gauge-invariant observable algebra A_ginv. If a spectrally determining vacuum-subtracted family A in A_ginv has connected Euclidean time correlations bounded by C_A exp(-m t) with m >= m0 > 0 uniformly through cutoff removal, then the reconstructed Hamiltonian has no vacuum-orthogonal spectrum in (0,m0), hence Spec(H restricted to P_perp H_YM) subset [m0,infinity).

### Objects

**Source objects**
- OS-positive continuum Yang-Mills Schwinger functions S_n from the RG-to-OS bridge
- gauge-invariant observable algebra A_ginv and vacuum-subtracted vectors (A-<A>)Omega
- cutoff-uniform Euclidean decay estimates for connected two-point functions

**Target objects**
- spectral measure mu_A for A Omega under H
- dense vacuum-orthogonal sector P_perp H_YM
- Hamiltonian spectral exclusion E_H((0,m0))P_perp = 0

### Definitions And Assumptions

- Definition: Spectrally determining means the closure of vacuum-subtracted gauge-invariant observable vectors is P_perp H_YM.
- Definition: Cutoff-uniform means the decay rate has a positive lower bound before taking the continuum limit.
- Definition: P_perp is the projection away from the reconstructed vacuum sector, not a regulator-level excitation space.
- Assumption: OS reconstruction identifies Euclidean time translation with exp(-tH) on H_YM.
- Assumption: The observable family is dense in the physical vacuum-orthogonal sector after quotienting OS null vectors.
- Assumption: The connected correlation decay rate m satisfies liminf m_{a,L} >= m0 > 0.

### Equations

- spectral representation: `C_A(t) = integral exp(-t lambda) d mu_A(lambda)`
  - TeX: `C_A(t)=\int_0^\infty e^{-t\lambda}\,d\mu_A(\lambda)`
  - Valid when: A Omega is a reconstructed vacuum-orthogonal vector and Euclidean time is represented by exp(-tH).
- uniform decay: `|C_A^{a,L}(t)| <= C_A exp(-m_{a,L} t), liminf m_{a,L} >= m0 > 0`
  - TeX: `|C_A^{a,L}(t)|\le C_Ae^{-m_{a,L}t},\qquad \liminf_{a\to0,L\to\infty}m_{a,L}\ge m_0>0`
  - Valid when: The constants are controlled uniformly for the same observable family that survives reconstruction.
- Hamiltonian gap conclusion: `E_H((0,m0)) P_perp = 0`
  - TeX: `E_H((0,m_0))P_\perp=0`
  - Valid when: The observable family is spectrally determining, so decay support restrictions extend from A Omega vectors to P_perp H_YM.

### Proof Obligations

- Specify the gauge-invariant observable family and prove its density in P_perp H_YM.
- Prove decay constants stay bounded below through cutoff removal.
- Show the spectral measure support implication is valid for the reconstructed continuum Hamiltonian.
- Check the nontriviality witness is compatible with the same observable algebra.

### Failure Tests

- Reject if the decay is only a strong-coupling or finite-lattice estimate.
- Reject if observables do not determine all physical non-vacuum excitations.
- Reject if the continuum construction and spectral estimate refer to different limiting objects.

### Proof By Contradiction Branches

#### No-gap spectral reductio

- Branch: `ym-reductio.c3895125c2cd`
- Exact negation: For every epsilon > 0 there exists psi_epsilon in P_perp H_YM with ||psi_epsilon|| = 1 and <psi_epsilon,H psi_epsilon> < epsilon; equivalently the vacuum-orthogonal spectral support of H meets (0,epsilon) for arbitrarily small epsilon.
- Contradiction carrier: low-energy vacuum-orthogonal spectral measures or observable-generated approximants in the reconstructed H_YM
- Derived consequence: The no-gap assumption puts spectral mass arbitrarily close to zero, while a spectrally determining observable family with cutoff-uniform e^{-m0 t} decay forces its spectral measures to have no support in (0,m0).
- Conflict target: spectral support exclusion E_H((0,m0))P_perp = 0 obtained from OS reconstruction, density, and uniform Euclidean decay
- Audit skill: `contradiction-route-auditor`
- Learning if failed: Failure would identify whether the next pivot should attack observable density, uniform decay, or same-theory reconstruction rather than continuing a generic mass-gap slogan.

**Preserved commitments**
- H, Omega, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.
- Gauge-invariant vacuum-subtracted observables are dense in P_perp H_YM.
- The Euclidean connected two-point decay bound holds uniformly with rate bounded below by m0 > 0.

**Proof obligations**
- Prove the gauge-invariant observable family is dense in the physical vacuum-orthogonal sector.
- Show the low-energy vectors can be approximated by vacuum-subtracted observable vectors.
- Prove the Laplace-transform spectral support lemma for the reconstructed Hamiltonian.
- Transport the cutoff-uniform decay estimate to the continuum without changing the object.

**Failure modes**
- The no-gap vectors live outside the observable-generated sector.
- The decay estimate is finite-cutoff, strong-coupling, or not uniform in the continuum limit.
- The route silently changes from the reconstructed H_YM to a different Hamiltonian or subsequence.

### Conditional Skill Triggers

- `evidence-acquisition-planner`: Locate precise correlator-decay, reflection-positivity, and transfer-matrix evidence.
- `review-reasoner-epistemologist`: Audit whether decay evidence is being over-transported across cutoff removal.
- `kb-contradiction-strategist`: Use when the no-gap negation can expose low-energy spectral mass obligations.
- `contradiction-route-auditor`: Audit the exact no-gap negation, carrier, density obligation, and same-theory invariant.
- `kb-macro-proof-paper-writer`: Summarize the bridge only after its assumptions and failure tests are explicit.

### Next Recursive Subgoals

- Formalize the density condition for gauge-invariant observables.
- Write the spectral-support lemma from exponential decay using the reconstructed Hamiltonian.
- Connect m0 to the Delta used by the Hamiltonian derivation report.

Promotion condition: Promote only when the decay estimate is cutoff-uniform and the observable family is spectrally determining in the reconstructed continuum theory.

Same-theory invariant: The decay estimates, spectral measure, observable density claim, and Hamiltonian H must all be attached to the same reconstructed Yang-Mills S_n.
