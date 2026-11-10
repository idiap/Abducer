# Stage 06 plan and completed todo ledger

## Frozen target

Prove a one-step, finite-dimensional effective-action transfer theorem for the
retained/fiber split produced in Stage 05.  The theorem must integrate the
fiber exactly, express every output bound in a declared derivative norm,
transport observables and state normalization, and expose the defect channel.
It does not assume or claim that the full Yang--Mills measure already satisfies
the input norm.

## Implemented todos

- [x] Freeze retained space `Y`, fiber space `F`, heat-time normalization, and
  a Gaussian conditional-mean splitting with no leading mixed Hessian.
- [x] Define the five-component scaled local action norm
  `(eps_fiber, eps_cross, eps_base, tau_fiber, tau_cross)`.
- [x] Prove preservation of fiber coercivity with explicit margin
  `mu = lambda_fiber - eps_fiber`.
- [x] Prove the conditional-minimizer response bound
  `||Dz_*|| <= eps_cross/mu`.
- [x] Derive the explicit centered cross-gradient and Wasserstein coefficients.
- [x] Differentiate the exact marginal and use the Brascamp--Lieb covariance
  inequality to derive the generated Hessian recursion.
- [x] Prove exact transport of state normalization and conditional expectation
  of observables.
- [x] Prove covariance under orthogonal residual gauge/frame actions.
- [x] Define a gauge-invariant defect ratio and derive its explicit scaled
  `C^2` contribution to the generated action.
- [x] Record positivity, locality, scale normalization, reflection positivity,
  and reconstruction status in a typed certificate table.
- [x] Implement the recursion calculator, exact Gaussian Schur-complement
  witness, and covariance checks.
- [x] Add hostile tests for lost coercivity, noncontractive tubes, invalid
  positivity, nonorthogonal recodings, and false mass-gap inference.
- [x] Produce a machine-readable dependency graph and conservative frontier
  ledger.
- [x] Write and compile a self-contained LaTeX/PDF theorem dossier.
- [x] Integrate the stage into the complete research package and verify it.

## Open frontier beyond this completed target

The following are the next analytic obligations rather than unchecked Stage 06
implementation tasks:

- Initialize the five derivative budgets with explicit, cutoff-aware constants
  for the exact nonlinear `SU(2)` heat-kernel action and its local chart.
- Construct a global gauge-covariant orbit disintegration or control all chart
  overlaps, exceptional stabilizers, and Gribov-type obstructions.
- Prove the declared defect `C^2` activity from the full large-field measure,
  including dependent polymers and topological sectors.
- Propagate locality, observable support, reflection positivity or a recovery
  certificate, and physical scale through repeated RG steps.
- Prove that the retained base enters a regulator-uniform massive basin.
- Construct the nontrivial Osterwalder--Schrader continuum theory and transfer
  physical-unit clustering to its Hamiltonian spectrum.
