# Next-target plan and todo ledger

## Frozen target

Construct the smallest genuinely four-dimensional, nonabelian-compatible
finite block on which the retained-base/conditional-fiber distinction can be
stated without gauge zero modes. Prove the exact Gaussian tangent theorem,
derive a nonlinear local stability criterion, and expose rather than assume
the remaining full-measure and RG-iteration estimates.

## Implemented todos

- [x] Freeze a `2^4` hypercubic block with 81 vertices, 216 oriented links,
  and 216 oriented plaquettes.
- [x] Construct the scalar coboundaries `d0` and `d1` and verify `d1 d0 = 0`.
- [x] Tensor the scalar complex with the three-dimensional Lie algebra
  `su(2)`.
- [x] Remove infinitesimal gauge directions by passing to `ker(d0^T)`.
- [x] Define 24 displayed retained curvature fluxes through the boundary
  `2x2` coarse faces.
- [x] Compute the 17 independent scalar retained modes and the corresponding
  119-dimensional scalar conditional fiber.
- [x] Prove an analytic coercivity lower bound `2` on the physical quotient;
  the same bound holds on the smaller fiber.
- [x] Compute the sharper numerical fiber minimum eigenvalue.
- [x] Prove that a Gaussian conditional law has a base-dependent mean but a
  base-independent centered covariance.
- [x] Formulate and prove the nonlinear Hessian-stability theorem.
- [x] Formulate the centered-measure transport theorem from strong convexity
  and a cross-gradient bound.
- [x] Add hostile tests showing the unquotiented Hessian has gauge zero modes
  and that the 24 displayed coarse fluxes contain dependencies.
- [x] Record large-field, topology, reflection-positivity, iteration, and
  continuum obligations.
- [x] Build a self-contained LaTeX/PDF dossier and reproducible data package.

## Open frontier beyond this completed bounded target

These are research obstructions recorded for the next target, not unimplemented
tasks in the present work package:

- Derive explicit nonlinear constants `C_B`, `rho_0`, and `t_0` for the
  exact `SU(2)` heat-kernel action rather than leaving them as finite-block
  derivative suprema.
- Replace the local Coulomb slice by a gauge-covariant block
  disintegration with an overlap atlas.
- Prove a dependent bad-block polymer bound for the complement of the
  small-curvature tube.
- Show stability of the fiber certificate for the generated Balaban-type
  effective-action class.
- Iterate through `k(a) ~ log(ell_*/a)` ultraviolet scales with summable
  errors.
- Prove the nonperturbative crossover of the retained base into a massive
  terminal basin.
- Construct the nontrivial regulator-independent OS continuum theory and
  transfer physical-unit decay to its Hamiltonian spectrum.
