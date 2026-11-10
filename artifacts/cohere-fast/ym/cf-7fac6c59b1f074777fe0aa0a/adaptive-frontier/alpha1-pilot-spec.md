# Alpha=1, p=1 physical-sector carrier pilot

Disposition: bounded falsifier/recovery experiment

Claim ceiling: candidate
Current executability: needs external mathematical and lattice data

## Fixed theory and basis

Use one finite-volume SU(3) heat-kernel lattice measure, one declared coupling
and scale-setting trajectory, one link-reflection plane, one vacuum-subtraction
rule, and no post-hoc observable replacement.

On the first positive-time slice, let (U_p) be a spatial plaquette holonomy.
Use three real class functions:

\[
\phi_{3+}(U)=\frac{1}{3}\operatorname{Re}\operatorname{tr}U,
\quad
\phi_8(U)=\frac{|\operatorname{tr}U|^2-1}{8},
\]

\[
\phi_{6+}(U)=\frac{1}{6}\operatorname{Re}
\left(\frac{(\operatorname{tr}U)^2+\operatorname{tr}(U^2)}{2}\right).
\]

For each channel (R\in\{3+,8,6+\}), form a centered zero-momentum sum

\[
F_R=|\mathcal P^+|^{-1/2}\sum_{p\in\mathcal P^+}
(\phi_R(U_p)-\langle\phi_R(U_p)\rangle).
\]

This is only a three-dimensional (A_1^{++}) visible sector. It is not an
observable-density claim.

## Reflection and fixed-time transfer matrices

For actual physical separation \(\tau_n=k_n a_{t,n}\to t_0>0\), compute

\[
G_{RS}=\langle\Theta F_R F_S\rangle,
\qquad
K_{RS}(\tau_n)=\langle\Theta F_R\,\tau_{k_n}F_S\rangle.
\]

Certify (G\succeq0), quotient only directions whose Gram interval contains
zero under a predeclared rule, retain raw eigenvalue and whitening ledgers, and
solve

\[
K(\tau_n)c=\lambda Gc.
\]

Within this finite carrier, \(\lambda_{\max}\) is the Rayleigh supremum and
\(-\tau_n^{-1}\log\lambda_{\max}\) is a visible-sector mass estimate. It does
not exclude lower-energy states outside the carrier. A trial subspace gives a
lower bound on the full supremum and can falsify a claimed gap; proof requires
a uniform upper bound over an eventually dense inclusion-ordered union.

## Fixed-physical recovery test

Predeclare centered Wilson-loop targets (Q_1,Q_2) with physical side lengths
\(\rho_0\) and (2\rho_0\). Compute

\[
H_{qq'}=\langle\Theta Q_qQ_{q'}\rangle,
\qquad B_{Rq}=\langle\Theta F_RQ_q\rangle,
\]

and the OS projection residual

\[
E_{\rm rec}=H-B^\dagger G^+B\succeq0.
\]

After quotienting null target directions, report the relative residual

\[
\varepsilon_{\rm rec}=\|H^{-1/2}E_{\rm rec}H^{-1/2}\|_2^{1/2}.
\]

At alpha=1 the candidate scaling (r_{\alpha,n}=\rho_0(a_n/\rho_0)^\alpha)
gives (r/a=1). A recovery residual bounded away from zero therefore exposes
UV-proxy collapse and rejects this carrier without rejecting the broader YM
program.

## Decisive falsifiers

- A certified negative eigenvalue of (G), or loss of finite reflection positivity.
- Gram-rank collapse or divergent whitening that hides vanishing raw overlap.
- Fixed-physical recovery residuals that remain nonzero or worsen with cutoff removal.
- Visible energies scaling as (a^{-1}), indicating a cutoff excitation.
- Incompatible cutoff/volume limits or physical-time calibration.
- Mixing matrices from different actions, scale settings, centering rules, or observables.
- Any claim that the three-dimensional visible sector is already Hilbert-dense.

## Missing inputs

The repository has no tuned heat-kernel trajectory, lattice configurations or
exact four-dimensional contraction engine, interval-valued (G,K,B,H\) tables,
scale-setting result, continuum recovery maps, density proof, uniform OS
passage, or common positive physical mass bound. The pilot is therefore a
validator-facing computation contract, not an executed physics result.
