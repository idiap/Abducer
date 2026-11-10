# Countermodel ledger

## X1 — hidden low-energy sector

Take `H=diag(0,1,1/2)` with vacuum the first basis vector.  The observable
core spanning only the energy-one vector has exact decay `e^{-t}` yet the
physical gap is `1/2`.  The missing hypothesis is density/completeness of the
centered observable core.

## X2 — finite gaps with no uniform physical floor

Let `H_n=diag(0,1,1/2,...,1/n)` and include each finite Hilbert space in
`C Omega + ell^2(N)`.  Every finite generator has a positive gap `1/n`; each
finite-support vector and its semigroup correlation are eventually recovered
exactly.  The direct-limit generator has energies `1/k` accumulating at zero.
The missing hypothesis is one index-independent rate `m>0` in physical units.

## X3 — noncommuting cutoff and volume limits

For `d(n,L)=1[L>n]`, every fixed volume has `d(n,L)->0` as the cutoff index
grows, while for every fixed cutoff `d(n,L)->1` as volume grows.  Hence
`lim_L lim_n d=0`, `lim_n lim_L d=1`, and `sup_L d(n,L)=1` for all `n`.
Pointwise recovery is not a uniform recovery certificate.

## X4 — auxiliary stochastic gap

Multiplying the generator of a Monte Carlo dynamics by a positive constant
changes its Poincare gap without changing the Euclidean field theory.  A
sampling gap is therefore not typed as a Hamiltonian spectral certificate.

## X5 — forgotten normalization

A deterministic action cost in a defect numerator does not control a
conditional probability until the corresponding partition-function ratio is
bounded.  Erasing the denominator forgets entropy/free energy, not a small
additive correction.
