<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hamiltonian Spectral-Gap Derivation

- Target: `yang-mills-existence-and-mass-gap-target`
- Mode: Hamiltonian spectral-gap mathematical derivation

This derives the exact spectral subclaim that the Hamiltonian route must prove. It does not prove Yang-Mills; it exposes the mathematical load-bearing lemmas and the spectral-theorem consequences.

## Route `candidate.7912a73ea5e8`

- Route family: `Hamiltonian spectral-gap route`
- Disposition: `revision_loop`
- Operation: `theorem_weakening`
- Route text: Use a bounded Hamiltonian spectral-gap route endpoint claim only after stating which reconstructed Yang-Mills objects and observables make it meaningful: Use the Hamiltonian formulation as the endpoint check: after the physical Hilbert space, vacuum, and time-translation generator are reconstructed from the same continuum Yang-Mills data, prove that vacuum-orthogonal excitations have energy at least a strictly positive Delta.

### Mathematical Subclaim

Given a reconstructed Wightman/OS Yang-Mills theory with Hilbert space H_YM, vacuum Omega, strongly continuous time translations U(t), and Hamiltonian H satisfying U(t)=exp(-itH), prove that there is Delta>0 with spec(H restricted to Omega^perp) subset [Delta,infty).

### Symbols

- `$H_YM$: physical Hilbert space produced by OS/Wightman reconstruction
- `$Omega$: vacuum vector, normalized and invariant under time translations
- `$U(t)$: strongly continuous unitary time-translation group
- `$H$: positive self-adjoint Hamiltonian, the generator of U(t)
- `$P0$: orthogonal projection onto the vacuum sector C Omega
- `$Pperp$: I-P0, the projection onto the vacuum-orthogonal excitation sector
- `$E_H(B)$: spectral projection of H for Borel set B
- `$Delta$: strictly positive spectral-gap constant

### Assumptions

- `A1` **OS/Wightman reconstruction**: OS-positive Schwinger data reconstructs (H_YM, Omega, U(t), fields). (route assumption, not discharged here; source `st.thm.os-reconstruction`)
- `A2` **Hamiltonian generation**: U(t) is strongly continuous and U(t)=e^{-itH} for a self-adjoint H. (functional-analytic bridge; source `KB/stone-one-parameter-unitary-groups.kb.md::st.app.schrodinger-time-evolution`)
- `A3` **Positive energy and vacuum**: H >= 0, H Omega = 0, and P0 projects onto the vacuum sector. (axiomatic target condition; source `st.def.wightman-qft, st.def.mass-gap`)
- `A4` **Nontrivial excitation sector**: Pperp H_YM != {0}; gauge-invariant observables create non-vacuum states. (essential nontriviality obligation; source `st.prob.yang-mills-existence-mass-gap`)
- `A5` **Spectral lower bound**: there exists Delta>0 such that E_H((0,Delta))Pperp = 0. (the hard lemma to prove; source `st.def.mass-gap-in-hamiltonian-wightman-terms`)

### Derivation

1. **Construct the Hamiltonian object**

From OS/Wightman reconstruction obtain a Hilbert space H_YM, vacuum Omega, and time translations U(t). By Stone's theorem, strong continuity of U(t) yields a self-adjoint generator H with U(t)=exp(-itH).

Equation context:

- Definition: H_YM is the Hilbert space reconstructed from OS-positive continuum Schwinger functions.
- Definition: U(t) is the strongly continuous unitary group implementing real-time translations on H_YM.
- Definition: H is the self-adjoint Stone generator of U(t), with positive energy imposed by the Wightman/OS target axioms.
- Assumptions used: A1, A2, A3
- Valid when: The Schwinger data have already passed to the continuum and satisfy OS positivity strongly enough for reconstruction.
- Valid when: Time translations are represented by a strongly continuous one-parameter unitary group on the reconstructed Hilbert space.
- Valid when: The positive-energy axiom is part of the reconstructed Yang-Mills target, not borrowed from a cutoff transfer matrix alone.

```math
U(t)=e^{-itH},\qquad H=H^*,\qquad H\ge 0.
```

Open obligation: Show this H is obtained after continuum/OS reconstruction, not only at fixed lattice cutoff.

2. **Separate vacuum and excitations**

Normalize the invariant vacuum Omega and set P0=|Omega><Omega|, or the projection onto the full vacuum sector if vacuum uniqueness is not yet known. The excitation space is Pperp H_YM=(I-P0)H_YM.

Equation context:

- Definition: Omega is the normalized invariant vacuum vector in H_YM.
- Definition: P0 is the orthogonal projection onto C Omega when the vacuum is unique; otherwise it must be replaced by the projection onto the full zero-energy vacuum sector.
- Definition: Pperp is I-P0, the vacuum-orthogonal excitation projection.
- Assumptions used: A1, A3, A4
- Valid when: The vacuum sector has been identified inside the reconstructed continuum theory.
- Valid when: Either vacuum uniqueness is proved, or the formula is read with P0 as the full vacuum-sector projection.
- Valid when: H Omega = 0 follows from time-translation invariance of the reconstructed vacuum.

```math
P_0=\lvert\Omega\rangle\langle\Omega\rvert,\qquad P_\perp=I-P_0,\qquad H\Omega=0.
```

Open obligation: Prove vacuum uniqueness or explicitly work with the whole zero-energy vacuum sector.

3. **State the spectral-gap lemma**

The Hamiltonian mass-gap claim is the spectral exclusion of low positive energies. In projection form, no vacuum-orthogonal state can have spectral support in (0,Delta).

Equation context:

- Definition: E_H(B) is the spectral projection of the self-adjoint Hamiltonian H for the Borel set B.
- Definition: Delta is a fixed positive number, independent of removed cutoffs, proposed as the mass-gap lower bound.
- Definition: H restricted to Pperp H_YM means the part of H acting on the invariant vacuum-orthogonal excitation sector.
- Assumptions used: A2, A3, A5
- Valid when: Pperp commutes with H, as it does when P0 projects onto the H-invariant zero-energy vacuum sector.
- Valid when: The spectral theorem applies to H and the projection statement is made on the reconstructed continuum Hilbert space.
- Valid when: Delta is strictly positive and the interval (0, Delta) is being excluded only away from the vacuum sector.

```math
E_H((0,\Delta))P_\perp=0\quad\Longleftrightarrow\quad \operatorname{spec}(H|_{P_\perp\mathcal H_{\mathrm{YM}}})\subset[\Delta,\infty).
```

Open obligation: Derive this exclusion from constructive/RG/correlator input rather than assuming it.

4. **Convert spectral exclusion to an energy inequality**

By the spectral theorem, if spectral support on Pperp H_YM lies in [Delta,infty), then every vector psi in the quadratic-form domain and orthogonal to the vacuum has energy at least Delta times its norm squared.

Equation context:

- Definition: psi is a vector in the quadratic-form domain of H and orthogonal to the vacuum sector.
- Definition: mu_psi(B)=<psi,E_H(B)psi> is the spectral measure of H associated with psi.
- Definition: The integral is the spectral-theorem expression for the Hamiltonian quadratic form on psi.
- Assumptions used: A2, A3, A5
- Valid when: The low-energy spectral exclusion E_H((0, Delta))Pperp=0 has been established.
- Valid when: psi lies in Pperp H_YM and in the form domain required for <psi,H psi> to be finite.
- Valid when: The support of mu_psi is contained in [Delta, infinity) after removal of the vacuum component.

```math
\psi\perp\Omega \Longrightarrow \langle\psi,H\psi\rangle=\int_{[\Delta,\infty)}\lambda\,d\mu_\psi(\lambda)\ge\Delta\|\psi\|^2.
```

Open obligation: Identify a dense class of physical gauge-invariant excitation states to which this estimate applies.

5. **Convert the same gap to Euclidean decay**

For A with <Omega,A Omega>=0, the Euclidean two-point function has spectral representation. The lower spectral support gives exponential decay with rate at least Delta.

Equation context:

- Definition: A is a reconstructed gauge-invariant observable, vacuum-subtracted so that <Omega,A Omega>=0.
- Definition: C_A(t) is the Euclidean time two-point function produced by OS reconstruction.
- Definition: mu_A(B)=<A Omega,E_H(B)A Omega> is the spectral measure of the excitation A Omega.
- Assumptions used: A1, A2, A3, A5
- Valid when: A Omega belongs to the vacuum-orthogonal sector and to the domain needed for the Euclidean semigroup pairing.
- Valid when: The OS/Wightman reconstruction identifies Euclidean time translation with the semigroup exp(-tH) for t >= 0.
- Valid when: The spectral support of A Omega lies in [Delta, infinity), so the exponential bound follows uniformly in t >= 0.

```math
C_A(t)=\langle A\Omega,e^{-tH}A\Omega\rangle=\int_{[\Delta,\infty)}e^{-t\lambda}\,d\mu_A(\lambda)\le e^{-\Delta t}\|A\Omega\|^2.
```

Open obligation: Specify gauge-invariant observables A and show their reconstructed states control the physical spectrum.

6. **Use decay-to-gap only with a density hypothesis**

Conversely, exponential decay of a sufficiently rich family of vacuum-subtracted observables can imply spectral support above Delta only if the created states are dense in the excitation sector.

Equation context:

- Definition: A_ginv is the reconstructed algebra or dense test family of gauge-invariant observables.
- Definition: The bar denotes Hilbert-space closure in H_YM.
- Definition: (A-<Omega,A Omega>)Omega is the vacuum-subtracted excitation created by A.
- Assumptions used: A1, A4
- Valid when: The observable family A_ginv is part of the same reconstructed continuum Yang-Mills theory.
- Valid when: Gauge-invariant observables are rich enough to generate the physical vacuum-orthogonal excitation sector.
- Valid when: Null vectors from OS reconstruction have already been quotiented out, so closure is taken in the physical Hilbert space.

```math
\overline{\{(A-\langle\Omega,A\Omega\rangle)\Omega:A\in\mathcal A_{\mathrm{ginv}}\}}=P_\perp\mathcal H_{\mathrm{YM}}.
```

Open obligation: Prove the gauge-invariant observable family is spectrally determining after reconstruction.

7. **Attach continuum compatibility**

For lattice/regulated approximants H_a, a bound inf spec(H_a|Pperp_a)>=Delta_a is useful only if liminf_{a->0}Delta_a>0 and the Hilbert spaces, observables, and vacuum sectors converge to the reconstructed continuum theory.

Equation context:

- Definition: a is the ultraviolet cutoff or lattice spacing parameter being removed.
- Definition: H_a and Pperp,a are the regulated Hamiltonian and excitation projection before continuum passage.
- Definition: Delta_a is the regulated gap lower bound, and Delta is the positive lower bound surviving the limit.
- Assumptions used: A1, A4, A5
- Valid when: The regulated Hilbert spaces, observables, vacuum sectors, and Hamiltonians converge to the same OS-reconstructed continuum object.
- Valid when: The spectral or Euclidean decay estimate is uniform in the cutoff and does not deteriorate to zero as a -> 0.
- Valid when: The limiting excitation sector remains nontrivial and interacting, so the bound is not for an empty or Gaussian surrogate.

```math
\inf\sigma(H_a|_{P_{\perp,a}})\ge\Delta_a,\quad \liminf_{a\to0}\Delta_a\ge\Delta>0.
```

Open obligation: Prevent the lattice gap from collapsing in the continuum limit.

### Candidate Derivation

If A1-A4 construct the physical continuum theory and A5 is proved, then the target subclaim follows: Pperp H_YM is the non-vacuum sector and the spectral theorem gives inf spec(H|Pperp H_YM)>=Delta. Equivalently, H has no spectrum in (0,Delta) away from the vacuum, so the reconstructed Yang-Mills theory has a Hamiltonian mass gap.

### What Would Count As Progress

- A precise construction of H_YM, Omega, U(t), and H from OS-positive continuum Schwinger functions.
  Why: This is the mathematical bridge from Euclidean functional data to the Hamiltonian problem. Without reconstructed objects H_YM, Omega, U(t), and a self-adjoint generator H, the phrase 'spectral gap' is only a desired notation, not a claim about the target continuum Yang-Mills theory.
- A proof that gauge-invariant observables create a dense excitation sector.
  Why: A gap detected by a narrow observable family could miss hidden low-energy states. Density is what lets decay estimates or spectral bounds for gauge-invariant observables control the whole vacuum-orthogonal physical sector P_perp H_YM.
- A cutoff-uniform lower spectral bound or equivalent cutoff-uniform Euclidean decay estimate.
  Why: The Clay target is a continuum problem, so a fixed-regulator lattice gap is not enough: it can collapse when the cutoff is removed. Uniformity is the mechanism that transfers a regulated spectral or decay estimate into a positive lower bound for the reconstructed continuum Hamiltonian.
- A nontriviality witness showing the excitation sector belongs to an interacting Yang-Mills theory.
  Why: The mass-gap statement must be about the nontrivial interacting gauge theory, not a free, Gaussian, empty, or mismatched limit. A nontriviality witness ties the excitation sector carrying the gap to the same continuum Yang-Mills object produced by the construction.

### What Does Not Count

- A spectral gap for a fixed lattice spacing without continuum stability.
- A heuristic or numerical lower bound not expressed as a spectral theorem statement.
- A Hamiltonian defined before OS/Wightman reconstruction of the continuum target.
- Decay of observables that do not determine the vacuum-orthogonal spectrum.
