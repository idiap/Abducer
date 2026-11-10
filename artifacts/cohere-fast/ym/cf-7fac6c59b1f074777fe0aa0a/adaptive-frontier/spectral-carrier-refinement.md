# Cohere-fast YM adaptive frontier: two-axis spectral carrier

Run: `cf-7fac6c59b1f074777fe0aa0a`

Disposition: frontier specification accepted; proof promotion quarantined
Claim ceiling: candidate

## Outcome

Separate geometric resolution \(\alpha\) from algebraic inclusion degree \(p\).
For each admitted alpha, order centered gauge-invariant Wilson-net spaces by
actual inclusion after recovery and OS quotienting:

\[
V_{\alpha,1} \subset V_{\alpha,2} \subset \cdots.
\]

on one fixed SU(3) heat-kernel cutoff/volume trajectory. Choose integer
\(k_n\) so the actual separation \(\tau_n=k_n a_{t,n}\) approaches one fixed
physical time \(t_0>0\). For Euclidean-time transfer on the OS quotient, define

\[
\rho_{\alpha,p,n}(\tau_n)=\sup_{0\ne\psi\in J_{n,\alpha,p}V_{\alpha,p}}
\frac{\langle\psi,T_n(\tau_n)\psi\rangle}{\|\psi\|^2},\qquad
m^{\rm phys}_{\alpha,p,n}(\tau_n)=-\frac{1}{\tau_n}
\log\rho_{\alpha,p,n}(\tau_n).
\]

If the actual OS quotient images are nested with identical centering and null
quotient, and use the same positive self-adjoint \(T_n(\tau_n)\), then rho is
nondecreasing and the mass estimate is nonincreasing in p. No monotonicity is
inferred from numerical alpha. The meaningful candidate gate is

\[
\inf_{\alpha,p}\liminf_n m^{\rm phys}_{\alpha,p,n}(\tau_n)>0,
\]

together with same-theory recovery, density in the vacuum-orthogonal OS
Hilbert space, reflection-form convergence, a nonzero carrier, and commuting
cutoff, volume, refinement, and reconstruction limits.

## Conditional bridge

If a dense set of vacuum-orthogonal OS vectors has spectral support outside
\([0,m)\) for one common \(m>0\), boundedness of the spectral projection
\(E_H([0,m))\) extends its vanishing to the closure and excludes additional
zero modes. The run does not prove
the hypotheses.

## Alpha=1 falsifier calibration

As a candidate calibration, set \(\epsilon_n=a_n/\rho_0\) and
\(r_{\alpha,n}=\rho_0\epsilon_n^\alpha\). Then alpha=1 has \(r/a=1\):
its shape repertoire stays one-cell and cannot establish density merely by
cutoff refinement. It should test UV collapse and recovery against
fixed-physical Wilson loops. Values \(0<\alpha<1\) permit a growing number of
lattice cells but still require a genuine p-density proof.

## Critical refinements

- Strict OS positivity margins are unnecessary; nonnegativity and convergence
  of reflection forms are the relevant closed-cone properties.
- Nonzero OS norm is the minimal anti-vacuity witness. A connected higher
  cumulant is a separate interaction/non-Gaussian witness.
- A functional inequality for auxiliary Langevin dynamics is rejected unless
  it is rigorously intertwined with physical Euclidean-time transfer.
- Changing the regulator, normalization, recovery map, or evolution while
  refining alpha is a proxy shift.

## Current gate and next action

No alpha-indexed recovery ledger, OS/transfer matrices, density residuals,
nontriviality witness, or common physical mass floor is present. Freeze
alpha=1 and p=1 with three centered spatial-plaquette SU(3) character channels:
charge-even fundamental, adjoint, and charge-even sextet. Produce their OS Gram
and fixed-physical-time transfer matrices, null-quotient and time-rounding
ledgers, and recovery residuals against fixed-physical Wilson loops. A
trial-vector lower bound on rho can falsify a proposed gap; promotion requires
a rigorous upper bound and, eventually, p-density.
